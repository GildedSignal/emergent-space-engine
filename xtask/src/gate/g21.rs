//! G2.1 canonical exactness: `position` equals the frozen reference floors on every case.
//! The ladder climbs R0 to R5 in order and stops at the first failing rung, after reporting
//! every disagreement of that rung. Each rung runs in chunks of under 60 s.
use super::{frozen::*, run::*, types::*};
use serde_json::{json, Value};

pub const RUNGS: [&str; 6] = ["R0", "R1", "R2", "R3", "R4", "R5"];

/// The sets that make up a rung. R5 is the new material (R5 itself, and the two G2.4 files): the
/// full set of G2.1 is R0..R4 (already passed in the climb) plus this. The fallback cases (FB)
/// run as the last stage of R5.
pub fn rung_sets(rung: &str) -> &'static [&'static str] {
    match rung {
        "R0" => &["R0"],
        "R1" => &["R1"],
        "R2" => &["R2"],
        "R3" => &["R3"],
        "R4" => &["R4"],
        _ => &["R5", "G24", "G24edge"],
    }
}
/// Every set the climb up to `upto` (an index into RUNGS) needs.
pub fn sets_needed(upto: usize) -> Vec<&'static str> {
    let mut v: Vec<&str> = RUNGS[..=upto].iter().flat_map(|r| rung_sets(r).iter().copied()).collect();
    if upto == 5 {
        v.push("FB");
    }
    v
}

#[derive(Clone, Debug, Default)]
pub struct RungReport {
    pub rung: String,
    pub cases: usize,
    pub queries: usize,
    pub agree: usize,
    pub disagree: usize,
    /// Queries whose expected answer is UNSETTLED (each counts as a failure).
    pub unsettled: usize,
    /// Cases the evaluator refused to construct (every query of such a case is a disagreement).
    pub anchor_errors: usize,
    pub chunks: Vec<Chunk>,
    pub secs: f64,
    pub pass: bool,
    /// The first few disagreements, for the console.
    pub first: Vec<Value>,
    /// Stage notes: the R2 spec check, the FB stage.
    pub notes: Vec<Value>,
}
impl RungReport {
    pub fn to_json(&self) -> Value {
        json!({"kind": "rung", "gate": "G2.1", "rung": self.rung, "cases": self.cases, "queries": self.queries, "agree": self.agree,
            "disagree": self.disagree, "unsettled_expected": self.unsettled, "anchor_errors": self.anchor_errors,
            "chunks": self.chunks.len(), "chunk_list": self.chunks.iter().map(Chunk::to_json).collect::<Vec<_>>(), "max_chunk_secs": (max_secs(&self.chunks) * 1e3).round() / 1e3,
            "secs": (self.secs * 1e3).round() / 1e3, "pass": self.pass, "notes": self.notes})
    }
}

pub struct G21Report {
    pub rungs: Vec<RungReport>,
    pub failed_at: Option<String>,
    /// True when the climb reached R5 (the full set), whether or not it passed.
    pub complete: bool,
}
impl G21Report {
    pub fn pass(&self) -> bool {
        self.failed_at.is_none() && !self.rungs.is_empty()
    }
}

fn disagreement(gate_rung: &str, j: &Judged, t: i128, expected: Value, got: Value) -> Value {
    json!({"kind": "disagreement", "gate": "G2.1", "rung": gate_rung, "id": j.case.id, "class": j.case.class, "T": t.to_string(), "expected": expected, "got": got})
}

/// Builds the body once and asks every recorded T.
fn check_case(ev: &dyn Evaluator, j: &Judged, rung: &str, ctx: &Ctx, r: &mut RungReport) {
    let c = &j.case;
    let body = ev.new_body(c.field(), c.q, c.anchor(), c.motion);
    let mut refused = false;
    for a in &j.answers {
        r.queries += 1;
        if matches!(a.expect, Expect::Unsettled(_)) {
            r.unsettled += 1;
        }
        let got = match &body {
            Ok(b) => Ok(b.position(a.t)),
            Err(e) => {
                refused = true;
                Err(e.0.clone())
            }
        };
        match &got {
            Ok(at) if a.expect.matches(at) => r.agree += 1,
            _ => {
                r.disagree += 1;
                let got_json = match &got {
                    Ok(at) => at.to_json(),
                    Err(e) => json!({"at": "AnchorError", "message": e}),
                };
                let row = disagreement(rung, j, a.t, a.expect.to_json(), got_json);
                if r.first.len() < 5 {
                    r.first.push(row.clone());
                }
                ctx.rows.write(&row);
            }
        }
    }
    r.anchor_errors += refused as usize;
}

/// The exhaustive small world of R2, regenerated from its spec (Q = 25, M = 1, x in [-8, 8]^2,
/// k in [-4, 4]^2, every valid timelike anchor, lexicographic), and compared with R2.answers.
/// Valid: r > 2M and |k - beta(x)| < Q, with beta = -Q sqrt(2M/r) x/r. The strict inequality is
/// decided in f64 here, and the smallest margin is reported (an f64 decision is safe only when
/// the margin is far above rounding).
pub fn r2_spec_check(fz: &Frozen) -> Value {
    let (mut spec, mut min_margin) = (Vec::new(), f64::INFINITY);
    for x in -8i64..=8 {
        for y in -8i64..=8 {
            let n = (x * x + y * y) as f64;
            if n <= 4.0 {
                continue;
            }
            let (r, q) = (n.sqrt(), 25.0f64);
            let s = (2.0 / r).sqrt();
            for kx in -4i64..=4 {
                for ky in -4i64..=4 {
                    let (kk, d) = ((kx * kx + ky * ky) as f64, (kx * x + ky * y) as f64);
                    let v = kk + 2.0 * q * s * d / r + 2.0 * q * q / r - q * q;
                    min_margin = min_margin.min(v.abs() / (q * q));
                    if v < 0.0 {
                        spec.push(([x as i128, y as i128], [kx as i128, ky as i128]));
                    }
                }
            }
        }
    }
    let file: Vec<_> = fz.set("R2").iter().map(|j| (j.case.x, j.case.k)).collect();
    json!({"stage": "R2 spec", "spec_anchors": spec.len(), "file_anchors": file.len(), "identical": spec == file, "min_margin_over_Q2": min_margin,
        "f64_decision_safe": min_margin > 1e-9})
}

pub fn run_rung(ev: &dyn Evaluator, fz: &Frozen, ctx: &Ctx, rung: &str) -> RungReport {
    let start = std::time::Instant::now();
    let items: Vec<&Judged> = rung_sets(rung).iter().flat_map(|s| fz.set(s).iter()).collect();
    let mut r = RungReport { rung: rung.to_string(), cases: items.len(), ..Default::default() };
    let label = format!("G2.1 {rung}");
    r.chunks = chunked(ctx, &label, &items, |chunk| {
        for j in chunk {
            ctx.note(&j.case.id);
            check_case(ev, j, rung, ctx, &mut r);
        }
    });
    let mut pass = r.disagree == 0 && r.unsettled == 0 && max_secs(&r.chunks) < ctx.hard_secs;
    if rung == "R2" {
        let note = r2_spec_check(fz);
        pass &= note["identical"] == true;
        ctx.rows.write(&json!({"kind": "check", "gate": "G2.1", "rung": rung, "check": note}));
        r.notes.push(note);
    }
    if rung == "R5" && fz.has("FB") {
        let fb = run_fallback(ev, fz, ctx);
        pass &= fb["pass"] == true;
        ctx.rows.write(&json!({"kind": "check", "gate": "G2.1", "rung": rung, "check": fb}));
        r.notes.push(fb);
    }
    r.pass = pass;
    r.secs = start.elapsed().as_secs_f64();
    ctx.rows.write(&r.to_json());
    ctx.rows.flush();
    ctx.say(&format!(
        "G2.1 {rung}: {} cases, {} queries: {} agree, {} disagree, {} UNSETTLED, {} refused; {} chunks (max {:.1} s), {:.1} s: {}",
        r.cases,
        r.queries,
        r.agree,
        r.disagree,
        r.unsettled,
        r.anchor_errors,
        r.chunks.len(),
        max_secs(&r.chunks),
        r.secs,
        if pass { "PASS" } else { "FAIL" }
    ));
    for row in &r.first {
        ctx.say(&format!("    {} T={} expected {} got {}", row["id"], row["T"], row["expected"], row["got"]));
    }
    for note in &r.notes {
        if note["pass"] == false || note["identical"] == false {
            ctx.say(&format!("    {} FAILED: {note}", note["stage"]));
        }
    }
    r
}

pub fn climb(ev: &dyn Evaluator, fz: &Frozen, ctx: &Ctx, upto: usize) -> G21Report {
    let mut rep = G21Report { rungs: Vec::new(), failed_at: None, complete: false };
    for rung in &RUNGS[..=upto] {
        let r = run_rung(ev, fz, ctx, rung);
        let pass = r.pass;
        rep.rungs.push(r);
        rep.complete = *rung == "R5";
        if !pass {
            rep.failed_at = Some(rung.to_string());
            break;
        }
    }
    rep
}

// ---- the fallback cases ------------------------------------------------------------------

/// The test-only reduced schedule (fractional bits) of the contract.
pub const REDUCED_SCHEDULE: [u32; 3] = [16, 32, 64];
const THREADS: usize = 4;

fn fb_one(ev: &dyn Evaluator, c: &Case) -> Result<At, String> {
    match ev.new_body_reduced(c.field(), c.q, c.anchor(), c.motion, &REDUCED_SCHEDULE) {
        None => Err("no reduced-schedule hook".into()),
        Some(Err(e)) => Err(format!("AnchorError: {e}")),
        Some(Ok(b)) => Ok(b.position(c.times[0])),
    }
}

/// Is `got` an admissible answer? For the boundary coordinate: one of the widths file's two
/// integers adjacent to the nearest integer boundary. For the other coordinate: the judge's
/// floor, unless the judge puts it within 1/4 quantum of an integer (the reduced width bound),
/// where the neighbours of the floor are allowed too.
fn fb_admissible(j: &Judged, w: &Value, got: &At) -> Result<(), String> {
    let (Expect::Known(At::Free(f)), At::Free(g)) = (&j.answers[0].expect, got) else {
        return Err(format!("expected a Free floor, got {got:?}"));
    };
    let c = w["coord"].as_u64().ok_or("FB.widths: no coord")? as usize;
    let allowed: Vec<i128> = w["allowed"].as_array().ok_or("FB.widths: no allowed")?.iter().map(|v| int_of(v).unwrap_or(i128::MIN)).collect();
    if !allowed.contains(&g[c]) {
        return Err(format!("coordinate {c} is {} but only {allowed:?} are admissible", g[c]));
    }
    let o = 1 - c;
    let near = j.answers[0].dist[o].is_some_and(|d| d < -2.0);
    if !(g[o] == f[o] || (near && (g[o] - f[o]).abs() == 1)) {
        return Err(format!("coordinate {o} is {} but the judge's floor is {}", g[o], f[o]));
    }
    Ok(())
}

/// The FB stage: with the reduced schedule, every eligible case (the judge certified its
/// 64-bit width below 1/4 quantum) must give an admissible floor, identical across three runs
/// and across thread counts (one thread, and four).
pub fn run_fallback(ev: &dyn Evaluator, fz: &Frozen, ctx: &Ctx) -> Value {
    let all = fz.set("FB");
    let (eligible, skipped): (Vec<&Judged>, Vec<&Judged>) =
        all.iter().partition(|j| fz.fb_widths.get(&j.case.id).is_some_and(|w| w["width_64_below_quarter"] == true));
    let may_force = eligible.iter().filter(|j| fz.fb_widths[&j.case.id]["may_force_fallback_at_64"] == true).count();
    let (mut bad, mut unstable, mut hook) = (0usize, 0usize, true);
    let chunks = chunked(ctx, "G2.1 R5 FB", &eligible, |chunk| {
        let a: Vec<_> = chunk.iter().map(|j| fb_one(ev, &j.case)).collect();
        let b: Vec<_> = chunk.iter().map(|j| fb_one(ev, &j.case)).collect();
        let c: Vec<_> = chunk.iter().map(|j| fb_one(ev, &j.case)).collect();
        let d: Vec<_> = std::thread::scope(|s| {
            let parts: Vec<_> = (0..THREADS)
                .map(|t| s.spawn(move || chunk.iter().enumerate().filter(|(i, _)| i % THREADS == t).map(|(i, j)| (i, fb_one(ev, &j.case))).collect::<Vec<_>>()))
                .collect();
            let mut out: Vec<(usize, Result<At, String>)> = parts.into_iter().flat_map(|h| h.join().unwrap()).collect();
            out.sort_by_key(|(i, _)| *i);
            out.into_iter().map(|(_, r)| r).collect()
        });
        for (i, j) in chunk.iter().enumerate() {
            ctx.note(&j.case.id);
            if a[i] == Err("no reduced-schedule hook".into()) {
                hook = false;
            }
            let same = a[i] == b[i] && a[i] == c[i] && a[i] == d[i];
            let verdict = match &a[i] {
                Ok(at) => fb_admissible(j, &fz.fb_widths[&j.case.id], at),
                Err(e) => Err(e.clone()),
            };
            if !same || verdict.is_err() {
                bad += verdict.is_err() as usize;
                unstable += !same as usize;
                ctx.rows.write(&json!({"kind": "disagreement", "gate": "G2.1", "rung": "R5", "stage": "FB", "id": j.case.id, "T": j.case.times[0].to_string(),
                    "expected": j.answers[0].expect.to_json(), "got": format!("{:?}", a[i]), "why": verdict.err(), "runs_identical": same,
                    "runs": [format!("{:?}", a[i]), format!("{:?}", b[i]), format!("{:?}", c[i]), format!("{:?}", d[i])]}));
            }
        }
    });
    json!({"stage": "FB", "eligible": eligible.len(), "skipped_ineligible": skipped.iter().map(|j| j.case.id.clone()).collect::<Vec<_>>(),
        "may_force_midpoint_at_64": may_force, "hook_implemented": hook, "inadmissible": bad, "not_identical_across_runs_or_threads": unstable,
        "runs": "3 single-thread runs and 1 run on 4 threads", "max_chunk_secs": max_secs(&chunks), "pass": hook && bad == 0 && unstable == 0 && !eligible.is_empty()})
}
