//! G2.2 oracle agreement, on the G2.2 set (bound R3 anchors with (p - p_sep)/p >= 1e-4, and
//! null anchors), at the contract's tolerances. Every quantity is compared with BOTH the oracle
//! function (evaluated at the judge's (p, e) or impact parameter) and the judge's recorded
//! diagnostic; the evaluator must be within the tolerance of each.
//!
//! Tolerances (frozen, docs/gravity-law.md): advance and radial periods 1e-9; clock rates
//! 1e-12; deflection 1e-8; Shapiro delay 1e-7; proper_time at each of 16 sampled T 1e-9,
//! relative to the judge, and equal to tau(T_h) at and after absorption.
//! Recorded but not gating (the contract fixes no tolerance): E, L, p, e, class.
//!
//! Adjudication. If the oracle function and the judge disagree with each other beyond the
//! tolerance on a check, no evaluator can be within the tolerance of both, and the check is
//! reported as `reference_gap` and FAILS. Only the integrator can adjudicate it (`--adjudicate
//! ID[:check]`): the check is then decided against the judge alone and the verdict lists it.
//! (H0192 froze the judge; the oracle function is the H0183 code, unchanged.)
use super::{frozen::*, oracle, run::*, types::*};
use serde_json::{json, Value};
use std::collections::BTreeMap;

pub const TOL_PERIODS_ADVANCE: f64 = 1e-9;
pub const TOL_CLOCK: f64 = 1e-12;
pub const TOL_DEFLECTION: f64 = 1e-8;
pub const TOL_SHAPIRO: f64 = 1e-7;
pub const TOL_TAU: f64 = 1e-9;
/// The selection rule of the G2.2 bound anchors: (p - p_sep)/p >= this.
pub const MIN_SEP_MARGIN: f64 = 1e-4;

#[derive(Clone, Debug, Default)]
pub struct CheckTally {
    pub n: usize,
    pub fail: usize,
    /// The evaluator gave NaN or nothing where the judge requires a value.
    pub missing: usize,
    pub max_rel_oracle: f64,
    pub max_rel_judge: f64,
    /// Oracle function versus judge diagnostic, beyond the tolerance (adjudication needed).
    pub reference_gap: usize,
    pub max_reference_gap: f64,
    /// Reference gaps decided against the judge alone by the integrator's adjudication.
    pub adjudicated: usize,
}
#[derive(Default)]
pub struct G22Report {
    pub cases: usize,
    pub checks: BTreeMap<String, CheckTally>,
    /// Recorded, not gating.
    pub info: BTreeMap<String, f64>,
    /// "id:check" of every adjudication that applied, and of the ones that never matched a gap.
    pub adjudications_applied: Vec<String>,
    pub unused_adjudications: Vec<String>,
    pub tau_queries: usize,
    pub tau_skipped_no_reference: usize,
    pub failed_cases: usize,
    pub chunks: Vec<Chunk>,
    pub pass: bool,
}

/// True when `r` is above `tol` or is NaN (a missing value fails).
fn exceeds(r: f64, tol: f64) -> bool {
    r.is_nan() || r > tol
}

/// Relative difference of `got` from `exp`. NaN when `got` is missing. exp = 0 needs got = 0.
pub fn rel(got: f64, exp: f64) -> f64 {
    if got.is_nan() || exp.is_nan() {
        f64::NAN
    } else if exp == 0.0 {
        if got == 0.0 {
            0.0
        } else {
            f64::INFINITY
        }
    } else {
        ((got - exp) / exp).abs()
    }
}
fn fnum(d: &Value, k: &str) -> f64 {
    d[k].as_str().and_then(|s| s.parse().ok()).unwrap_or(f64::NAN)
}
fn jf(x: f64) -> Value {
    if x.is_finite() {
        json!(x)
    } else {
        json!(x.to_string())
    }
}

/// One case's check results.
struct Acc<'a> {
    checks: Vec<(String, Value)>,
    ok: bool,
    id: &'a str,
    adjudicated: &'a [String],
}
impl Acc<'_> {
    fn cmp(&mut self, rep: &mut G22Report, name: &'static str, got: f64, oracle: f64, judge: f64, tol: f64) {
        let (ro, rj, gap) = (rel(got, oracle), rel(got, judge), rel(judge, oracle));
        let adjudicated = gap > tol && self.adjudicated.iter().any(|a| *a == self.id || *a == format!("{}:{name}", self.id));
        // NaN comparisons are false, so a missing value fails. An adjudicated gap is decided by the judge alone.
        // (The circular clock rate and the Shapiro delay are not recorded by the judge: oracle only.)
        let judge_optional = matches!(name, "circular_clock" | "shapiro_delay");
        let pass = (adjudicated || ro <= tol) && (judge_optional || rj <= tol);
        if adjudicated {
            rep.adjudications_applied.push(format!("{}:{name}", self.id));
        }
        let t = rep.checks.entry(name.to_string()).or_default();
        t.n += 1;
        t.fail += !pass as usize;
        t.missing += got.is_nan() as usize;
        if ro.is_finite() {
            t.max_rel_oracle = t.max_rel_oracle.max(ro);
        }
        if rj.is_finite() {
            t.max_rel_judge = t.max_rel_judge.max(rj);
        }
        t.reference_gap += (gap > tol) as usize;
        t.adjudicated += adjudicated as usize;
        if gap.is_finite() {
            t.max_reference_gap = t.max_reference_gap.max(gap);
        }
        self.ok &= pass;
        self.checks.push((name.to_string(), json!({"got": jf(got), "oracle": jf(oracle), "judge": jf(judge), "rel_oracle": jf(ro), "rel_judge": jf(rj), "reference_gap": jf(gap), "adjudicated": adjudicated, "tol": tol, "pass": pass})));
    }
}

fn info(rep: &mut G22Report, name: &str, got: f64, judge: f64) {
    let r = rel(got, judge);
    let e = rep.info.entry(name.to_string()).or_insert(0.0);
    *e = e.max(if r.is_nan() { f64::INFINITY } else { r });
}

fn check_case(ev: &dyn Evaluator, j: &Judged, ctx: &Ctx, rep: &mut G22Report) {
    let c = &j.case;
    let mut acc = Acc { checks: Vec::new(), ok: true, id: &c.id, adjudicated: &ctx.adjudicated };
    let Some(d) = j.diag.as_ref() else {
        rep.failed_cases += 1;
        ctx.rows.write(&json!({"kind": "case", "gate": "G2.2", "id": c.id, "pass": false, "why": "no judge diagnostics"}));
        return;
    };
    let body = match ev.new_body(c.field(), c.q, c.anchor(), c.motion) {
        Ok(b) => b,
        Err(e) => {
            rep.failed_cases += 1;
            ctx.rows.write(&json!({"kind": "case", "gate": "G2.2", "id": c.id, "pass": false, "why": format!("AnchorError: {e}")}));
            return;
        }
    };
    let o = body.orbit();
    let unit = c.m as f64 / c.q as f64; // chronons per GM/c^3
    let r0 = oracle::radius_over_m(c.x, c.m);
    acc.cmp(rep, "static_clock", o.static_clock_rate, oracle::static_clock_rate(r0), fnum(d, "static_clock_rate_r0"), TOL_CLOCK);
    if r0 > 3.0 {
        acc.cmp(rep, "circular_clock", o.circular_clock_rate, oracle::circular_clock_rate(r0), f64::NAN, TOL_CLOCK);
    }
    match c.motion {
        Motion::Timelike => {
            let (p, e) = (fnum(d, "p_over_M"), fnum(d, "e"));
            if fnum(d, "sep_margin") < MIN_SEP_MARGIN {
                acc.ok = false;
                acc.checks.push(("selection".into(), json!({"pass": false, "why": "sep_margin below 1e-4: not a G2.2 anchor"})));
            }
            let (t_o, tau_o) = oracle::radial_periods(p, e);
            acc.cmp(rep, "periapsis_advance", o.periapsis_advance, oracle::periapsis_advance(p, e), fnum(d, "advance_rad"), TOL_PERIODS_ADVANCE);
            acc.cmp(rep, "radial_period_T", o.radial_period, t_o * unit, fnum(d, "period_T_chronons"), TOL_PERIODS_ADVANCE);
            acc.cmp(rep, "radial_period_tau", o.proper_radial_period, tau_o * unit, fnum(d, "period_tau_chronons"), TOL_PERIODS_ADVANCE);
            info(rep, "energy", o.energy, fnum(d, "E"));
            info(rep, "angular_momentum", o.angular_momentum, fnum(d, "L_quanta"));
            info(rep, "p", o.p, p);
            info(rep, "e", o.e, e);
            if o.class.name() != d["kind"].as_str().unwrap_or("") {
                *rep.info.entry("class_mismatches".into()).or_insert(0.0) += 1.0;
            }
        }
        Motion::Null => {
            let b = fnum(d, "b_over_M");
            let r0n = oracle::null_turning_radius(b);
            acc.cmp(rep, "light_deflection", o.deflection, oracle::deflection(b), fnum(d, "deflection_rad"), TOL_DEFLECTION);
            let (a1, a2) = oracle::SHAPIRO_ENDPOINTS;
            let got = body.shapiro_delay(a1 * r0n * c.m as f64, a2 * r0n * c.m as f64).unwrap_or(f64::NAN);
            acc.cmp(rep, "shapiro_delay", got, oracle::shapiro(r0n, a1 * r0n, a2 * r0n) * unit, f64::NAN, TOL_SHAPIRO);
            // The oracle's turning radius must be the judge's r_min, or the Shapiro row is misplaced.
            info(rep, "oracle_r0_vs_judge_rmin", r0n, fnum(d, "r_min_over_M"));
            info(rep, "energy", o.energy, fnum(d, "E"));
            info(rep, "angular_momentum", o.angular_momentum, fnum(d, "L_quanta"));
        }
    }
    // proper_time at every sampled T the judge recorded a tau for.
    let (mut worst, mut bad) = (0.0f64, 0usize);
    for a in &j.answers {
        let Some(exp) = a.tau else {
            rep.tau_skipped_no_reference += 1;
            continue;
        };
        rep.tau_queries += 1;
        let r = rel(body.proper_time(a.t), exp);
        // NaN (missing) fails.
        if exceeds(r, TOL_TAU) {
            bad += 1;
        }
        if r.is_nan() {
            worst = f64::INFINITY;
        } else {
            worst = worst.max(r);
        }
    }
    {
        let t = rep.checks.entry("proper_time".into()).or_default();
        t.n += 1;
        t.fail += (bad > 0) as usize;
        t.max_rel_judge = t.max_rel_judge.max(worst);
    }
    acc.ok &= bad == 0;
    rep.failed_cases += !acc.ok as usize;
    ctx.rows.write(&json!({"kind": "case", "gate": "G2.2", "id": c.id, "class": c.class, "pass": acc.ok,
        "checks": acc.checks.into_iter().collect::<serde_json::Map<_, _>>(), "proper_time": {"queries": j.answers.len(), "worst_rel": jf(worst), "failed": bad}}));
}

/// proper_time at and after absorption equals tau(T_h): every Absorbed query of the G2.4
/// files has the judge's tau (within 1e-9) and the same bits as the case's other Absorbed
/// queries. (The G2.2 set has no absorbed queries, so this reads the G2.4 files.)
fn absorbed_clock(ev: &dyn Evaluator, j: &Judged, ctx: &Ctx, rep: &mut G22Report) {
    let c = &j.case;
    let absorbed = j.answers.iter().filter(|a| matches!(a.expect, Expect::Known(At::Absorbed { .. }))).count();
    let Ok(body) = ev.new_body(c.field(), c.q, c.anchor(), c.motion) else {
        // A refused case is a failure of every absorbed query it holds, not a skip.
        let t = rep.checks.entry("absorbed_clock".into()).or_default();
        t.n += absorbed;
        t.fail += absorbed;
        return;
    };
    let (mut first, mut bad, mut n) = (None::<f64>, 0usize, 0usize);
    for a in j.answers.iter().filter(|a| matches!(a.expect, Expect::Known(At::Absorbed { .. }))) {
        n += 1;
        let got = body.proper_time(a.t);
        if exceeds(rel(got, a.tau.unwrap_or(f64::NAN)), TOL_TAU) || first.is_some_and(|f| f.to_bits() != got.to_bits()) {
            bad += 1;
            ctx.rows.write(&json!({"kind": "disagreement", "gate": "G2.2", "check": "absorbed_clock", "id": c.id, "T": a.t.to_string(), "expected_tau": jf(a.tau.unwrap_or(f64::NAN)), "got": jf(got)}));
        }
        first.get_or_insert(got);
    }
    if n > 0 {
        let t = rep.checks.entry("absorbed_clock".into()).or_default();
        t.n += n;
        t.fail += bad;
    }
}

pub fn run(ev: &dyn Evaluator, fz: &Frozen, ctx: &Ctx) -> G22Report {
    let mut rep = G22Report::default();
    let items: Vec<&Judged> = fz.set("G22").iter().collect();
    rep.cases = items.len();
    let mut chunks = chunked(ctx, "G2.2", &items, |chunk| {
        for j in chunk {
            ctx.note(&j.case.id);
            check_case(ev, j, ctx, &mut rep);
        }
    });
    let abs: Vec<&Judged> = ["G24", "G24edge"].iter().filter(|s| fz.has(s)).flat_map(|s| fz.set(s).iter()).collect();
    chunks.extend(chunked(ctx, "G2.2 absorbed clock", &abs, |chunk| {
        for j in chunk {
            absorbed_clock(ev, j, ctx, &mut rep);
        }
    }));
    let unused: Vec<String> =
        ctx.adjudicated.iter().filter(|a| !rep.adjudications_applied.iter().any(|u| u == *a || u.starts_with(&format!("{a}:")))).cloned().collect();
    rep.unused_adjudications = unused;
    rep.pass = rep.failed_cases == 0 && rep.checks.values().all(|t| t.fail == 0) && max_secs(&chunks) < ctx.hard_secs && !items.is_empty();
    rep.chunks = chunks;
    rep
}
impl G22Report {
    pub fn to_json(&self) -> Value {
        json!({"gate": "G2.2", "cases": self.cases, "failed_cases": self.failed_cases, "pass": self.pass,
            "adjudicated": self.adjudications_applied, "adjudications_that_matched_no_gap": self.unused_adjudications, "proper_time_queries": self.tau_queries, "proper_time_skipped_no_judge_tau": self.tau_skipped_no_reference,
            "checks": self.checks.iter().map(|(k, t)| (k.clone(), json!({"n": t.n, "fail": t.fail, "missing": t.missing, "max_rel_oracle": jf(t.max_rel_oracle),
                "max_rel_judge": jf(t.max_rel_judge), "oracle_vs_judge_over_tol": t.reference_gap, "adjudicated": t.adjudicated, "max_oracle_vs_judge": jf(t.max_reference_gap)}))).collect::<serde_json::Map<_, _>>(),
            "recorded_not_gating_max_rel": self.info.iter().map(|(k, v)| (k.clone(), jf(*v))).collect::<serde_json::Map<_, _>>(),
            "chunks": self.chunks.len(), "max_chunk_secs": max_secs(&self.chunks)})
    }
}
