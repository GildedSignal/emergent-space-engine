//! `gravity-gate`: the step 2 gate harness (docs/gravity-law.md, gates G2.1 to G2.5) against
//! the frozen reference answers (artifacts/evidence/g2-reference-20260928).
//!
//! ```text
//! cargo run --release -p xtask -- gravity-gate [out-dir] [--rung R0..R5] [--evaluator NAME]
//!     [--gates 1,2,3,4,5] [--evidence DIR] [--chunk-secs N] [--adjudicate ID[:check],...] [--literal]
//! ```
//! - `--rung Rk` stops the G2.1 climb after Rk. The climb always starts at R0 and stops at the
//!   first failing rung. Any run that is not the whole of G2.1 to G2.5 can fail, but it ends
//!   PARTIAL PASS, never GATES PASS.
//! - `--evaluator`: `crate` (default; the adapter, unwired until the integrator wires it),
//!   `echo`, `planted`, `planted:<chart>`, `planted-g22`, `planted-g23`, `planted-g24`, `hang`
//!   (see eval.rs). The built-ins prove the harness can fail; they are not physics.
//! - G2.2 adjudications (an oracle function and the judge disagree, so no evaluator can satisfy
//!   both) come from `adjudicated.txt` and `--adjudicate`; `--literal` ignores the file. Every run
//!   prints and records the adjudications it used.
//! - Every unit of work runs in chunks sized to about `--chunk-secs` (default 30); a chunk that
//!   runs `--hard-secs` (default 60) is killed and the gate fails.
//! - Output: `rows.jsonl` (every disagreement, chunk, case and machine-state row),
//!   `G2.1.verdict.json` .. `G2.5.verdict.json`, `verdict.json`, and a last stdout line that is
//!   GATES PASS or GATES FAIL (exit 1).
mod adapter;
mod eval;
mod frozen;
mod g21;
mod g22;
mod g23;
mod g24;
mod g25;
mod oracle;
mod run;
#[cfg(test)]
mod tests;
mod types;

use crate::Result;
use frozen::*;
use run::*;
use serde_json::{json, Value};
use std::{
    path::{Path, PathBuf},
    time::Duration,
};
use types::*;

/// The integrator's adjudications of G2.2 oracle-versus-judge gaps (adjudicated.txt).
pub const REGISTER: &str = include_str!("adjudicated.txt");
/// (entry, reason) per register line: `ID[:check] | reason`.
pub fn register() -> Vec<(String, String)> {
    REGISTER
        .lines()
        .filter(|l| !l.trim().is_empty() && !l.starts_with('#'))
        .map(|l| {
            let (entry, reason) = l.split_once('|').unwrap_or((l, ""));
            (entry.trim().to_string(), reason.trim().to_string())
        })
        .collect()
}

pub const USAGE: &str = "usage: gravity-gate [out-dir] [--rung R0..R5] [--evaluator crate|echo|planted|planted:CHART|planted-g22|planted-g23|planted-g24] [--gates 1,2,3,4,5] [--evidence DIR] [--chunk-secs N] [--adjudicate ID[:check],...] [--literal] [--hard-secs N]";

#[derive(Clone, Debug)]
pub struct Selection {
    /// The climb stops after RUNGS[upto].
    pub upto: usize,
    pub gates: [bool; 5],
}
impl Selection {
    pub fn everything() -> Selection {
        Selection { upto: 5, gates: [true; 5] }
    }
    /// Every set the selected gates read.
    pub fn sets(&self) -> Vec<&'static str> {
        let mut v = Vec::new();
        if self.gates[0] {
            v.extend(g21::sets_needed(self.upto));
        }
        if self.gates[1] {
            v.extend(["G22", "G24", "G24edge"]);
        }
        if self.gates[2] {
            v.extend(["R3", "R5"]);
        }
        if self.gates[3] {
            v.extend(["G24", "G24edge"]);
        }
        if self.gates[4] {
            v.extend(ALL_SETS.iter().copied());
        }
        ALL_SETS.iter().copied().filter(|s| v.contains(s)).collect()
    }
}

#[derive(Default)]
pub struct Outcome {
    pub g21: Option<g21::G21Report>,
    pub g22: Option<g22::G22Report>,
    pub g23: Option<g23::G23Report>,
    pub g24: Option<g24::G24Report>,
    pub g25: Option<g25::G25Report>,
}
impl Outcome {
    fn passes(&self) -> [Option<bool>; 5] {
        [
            self.g21.as_ref().map(|r| r.pass()),
            self.g22.as_ref().map(|r| r.pass),
            self.g23.as_ref().map(|r| r.pass),
            self.g24.as_ref().map(|r| r.pass),
            self.g25.as_ref().map(|r| r.pass()),
        ]
    }
    /// All five gates ran, and G2.1 reached R5.
    pub fn complete(&self) -> bool {
        self.passes().iter().all(|p| p.is_some()) && self.g21.as_ref().is_some_and(|r| r.complete)
    }
    pub fn failed(&self) -> bool {
        self.passes().contains(&Some(false))
    }
    pub fn label(&self) -> &'static str {
        if self.failed() {
            "GATES FAIL"
        } else if self.complete() {
            "GATES PASS"
        } else {
            "PARTIAL PASS (not a gate verdict: not every gate ran to the end)"
        }
    }
}

/// Runs the selected gates. G2.1 to G2.5 are independent: a failure of one does not stop the others
/// (G2.1's climb itself stops at its first failing rung).
pub fn execute(ev: &dyn Evaluator, fz: &Frozen, ctx: &Ctx, sel: &Selection) -> Outcome {
    let mut out = Outcome::default();
    if sel.gates[0] {
        out.g21 = Some(g21::climb(ev, fz, ctx, sel.upto));
        let r = out.g21.as_ref().unwrap();
        ctx.say(&format!(
            "G2.1 {}",
            match (&r.failed_at, r.complete) {
                (Some(at), _) => format!("FAIL at {at}; the climb stopped there"),
                (None, true) => "PASS (R0 to R5)".into(),
                (None, false) => format!("passed up to {} (partial climb)", r.rungs.last().map(|x| x.rung.as_str()).unwrap_or("-")),
            }
        ));
    }
    if sel.gates[1] {
        let r = g22::run(ev, fz, ctx);
        ctx.rows.write(&r.to_json());
        ctx.say(&format!("G2.2: {} cases, {} failed; {}", r.cases, r.failed_cases, if r.pass { "PASS" } else { "FAIL" }));
        for (k, t) in r.checks.iter().filter(|(_, t)| t.fail > 0) {
            ctx.say(&format!(
                "    {k}: {} of {} failed ({} missing; the oracle function and the judge differ by more than the tolerance on {})",
                t.fail,
                t.n,
                t.missing,
                t.reference_gap - t.adjudicated
            ));
        }
        if !r.adjudications_applied.is_empty() {
            ctx.say(&format!("    ADJUDICATED by the integrator (decided against the judge alone): {}", r.adjudications_applied.join(", ")));
        }
        if !r.unused_adjudications.is_empty() {
            ctx.say(&format!("    adjudications that matched no oracle-versus-judge gap: {}", r.unused_adjudications.join(", ")));
        }
        out.g22 = Some(r);
    }
    if sel.gates[2] {
        let r = g23::run(ev, fz, ctx);
        ctx.rows.write(&r.to_json());
        ctx.say(&format!(
            "G2.3: {} cases x {} intermediates, {} failed; {}",
            r.cases,
            g23::DISTINCT + g23::REPEATS,
            r.failed,
            if r.pass { "PASS" } else { "FAIL" }
        ));
        out.g23 = Some(r);
    }
    if sel.gates[3] {
        let r = g24::run(ev, fz, ctx);
        ctx.rows.write(&r.to_json());
        ctx.say(&format!(
            "G2.4: {} cases, {} disagreements, {} reference inconsistencies; {}",
            r.cases,
            r.disagreements,
            r.reference_inconsistent,
            if r.pass { "PASS" } else { "FAIL" }
        ));
        out.g24 = Some(r);
    }
    if sel.gates[4] {
        let r = g25::run(ev, fz, ctx);
        ctx.rows.write(&r.to_json());
        ctx.say(&format!(
            "G2.5a natural: median {:.3} us (limit 50), p99 {:.3} us (limit 500) over {} calls: {}; G2.5b all: max {:.1} us (limit 5000) over {} calls: {}; {} cases untimed",
            r.median_us, r.p99_us, r.natural_ns.len(), if r.pass_a { "PASS" } else { "FAIL" }, r.max_ns as f64 / 1e3, r.all_calls, if r.pass_b { "PASS" } else { "FAIL" }, r.untimed_cases
        ));
        out.g25 = Some(r);
    }
    ctx.rows.flush();
    out
}

fn write_json(path: &Path, v: &Value) -> Result<()> {
    std::fs::write(path, serde_json::to_vec_pretty(v)?)?;
    Ok(())
}
/// One machine-readable verdict per gate, and the overall one.
pub fn write_verdicts(dir: &Path, out: &Outcome, meta: &Value) -> Result<()> {
    let with = |mut v: Value, pass: bool| {
        v["pass"] = json!(pass);
        v["run"] = meta.clone();
        v
    };
    if let Some(r) = &out.g21 {
        let rungs: Vec<Value> = r.rungs.iter().map(|x| x.to_json()).collect();
        write_json(
            &dir.join("G2.1.verdict.json"),
            &with(json!({"gate": "G2.1", "failed_at": r.failed_at, "reached_R5": r.complete, "rungs": rungs}), r.pass()),
        )?;
    }
    if let Some(r) = &out.g22 {
        write_json(&dir.join("G2.2.verdict.json"), &with(r.to_json(), r.pass))?;
    }
    if let Some(r) = &out.g23 {
        write_json(&dir.join("G2.3.verdict.json"), &with(r.to_json(), r.pass))?;
    }
    if let Some(r) = &out.g24 {
        write_json(&dir.join("G2.4.verdict.json"), &with(r.to_json(), r.pass))?;
    }
    if let Some(r) = &out.g25 {
        write_json(&dir.join("G2.5.verdict.json"), &with(r.to_json(), r.pass()))?;
    }
    let names = ["G2.1", "G2.2", "G2.3", "G2.4", "G2.5"];
    let gates: serde_json::Map<String, Value> = names.iter().zip(out.passes()).map(|(n, p)| (n.to_string(), json!(p))).collect();
    write_json(&dir.join("verdict.json"), &json!({"result": out.label(), "complete": out.complete(), "gates": gates, "run": meta}))?;
    Ok(())
}

pub fn make_evaluator(name: &str, fz: &Frozen) -> Result<Box<dyn Evaluator>> {
    match name {
        "crate" => Ok(Box::new(adapter::CrateEvaluator)),
        n => Ok(Box::new(eval::Replay::new(fz, n)?)),
    }
}

fn parse_gates(s: &str) -> Result<[bool; 5]> {
    let mut g = [false; 5];
    for part in s.split(',') {
        let digit = part.trim().trim_start_matches(['g', 'G']).trim_start_matches("2.").parse::<usize>().map_err(|_| format!("bad gate {part:?}; use 1..5"))?;
        if !(1..=5).contains(&digit) {
            return Err(format!("bad gate {part:?}; use 1..5").into());
        }
        g[digit - 1] = true;
    }
    Ok(g)
}

pub fn run(args: Vec<String>) -> Result<u8> {
    let (mut out_dir, mut sel, mut evaluator, mut evidence, mut chunk_secs) =
        (None, Selection::everything(), "crate".to_string(), PathBuf::from(DEFAULT_DIR), 30.0f64);
    let (mut adjudicated, mut literal, mut hard_secs): (Vec<String>, bool, f64) = (Vec::new(), false, 60.0);
    let mut it = args.into_iter();
    while let Some(a) = it.next() {
        let mut value = |flag: &str| it.next().ok_or_else(|| format!("{flag} needs a value; {USAGE}"));
        match a.as_str() {
            "--rung" => {
                let r = value("--rung")?;
                sel.upto = g21::RUNGS.iter().position(|x| *x == r).ok_or_else(|| format!("bad rung {r:?}; use R0..R5"))?;
            }
            "--evaluator" => evaluator = value("--evaluator")?,
            "--gates" => sel.gates = parse_gates(&value("--gates")?)?,
            "--evidence" => evidence = PathBuf::from(value("--evidence")?),
            "--literal" => literal = true,
            "--hard-secs" => hard_secs = value("--hard-secs")?.parse().map_err(|_| "bad --hard-secs")?,
            "--adjudicate" => adjudicated = value("--adjudicate")?.split(',').map(|s| s.trim().to_string()).filter(|s| !s.is_empty()).collect(),
            "--chunk-secs" => chunk_secs = value("--chunk-secs")?.parse().map_err(|_| "bad --chunk-secs")?,
            f if f.starts_with("--") => return Err(format!("unknown option {f}; {USAGE}").into()),
            _ if out_dir.is_none() => out_dir = Some(PathBuf::from(a)),
            _ => return Err(USAGE.into()),
        }
    }
    if !literal {
        adjudicated.extend(register().into_iter().map(|(e, _)| e));
    }
    let out_dir = out_dir.unwrap_or_else(|| PathBuf::from("artifacts/runs/gravity-gate"));
    std::fs::create_dir_all(&out_dir)?;
    // A verdict left by an earlier run must not pass for this one.
    for f in ["G2.1.verdict.json", "G2.2.verdict.json", "G2.3.verdict.json", "G2.4.verdict.json", "G2.5.verdict.json", "verdict.json"] {
        let _ = std::fs::remove_file(out_dir.join(f));
    }
    let rows = Rows::create(&out_dir.join("rows.jsonl"))?;

    // Evidence that differs from what was frozen, or does not parse, is a failure of the run, not an error of usage.
    let early = |why: String| -> Result<u8> {
        rows.write(&json!({"kind": "evidence_error", "why": why}));
        rows.flush();
        write_json(&out_dir.join("verdict.json"), &json!({"result": "GATES FAIL", "reason": why}))?;
        println!("gravity-gate: {why}\nGATES FAIL");
        Ok(1)
    };
    let hashes = match verify_hashes(&evidence) {
        Ok(h) => h,
        Err(e) => return early(e.to_string()),
    };
    println!("gravity-gate: frozen evidence {} ({hashes})", evidence.display());
    let builtin = evaluator != "crate";
    let sets: Vec<&str> = if builtin { ALL_SETS.to_vec() } else { sel.sets() };
    let fz = match Frozen::load(&evidence, &sets) {
        Ok(f) => f,
        Err(e) => return early(format!("the frozen evidence does not load: {e}")),
    };
    let ev = make_evaluator(&evaluator, &fz)?;
    let start = machine_state("start");
    rows.write(&start);
    println!(
        "gravity-gate: evaluator {}; {} of {} rungs; gates {:?}; machine: {} | {} | {}",
        ev.name(),
        sel.upto + 1,
        6,
        sel.gates.iter().enumerate().filter(|(_, g)| **g).map(|(i, _)| format!("G2.{}", i + 1)).collect::<Vec<_>>(),
        start["power_source"].as_str().unwrap_or("?"),
        start["swap"].as_str().unwrap_or("?"),
        start["loadavg"].as_str().unwrap_or("?")
    );

    let meta = json!({"evaluator": ev.name(), "evidence": evidence.display().to_string(), "evidence_check": hashes, "rung_limit": g21::RUNGS[sel.upto],
        "gates": sel.gates, "chunk_secs": chunk_secs, "hard_secs": hard_secs, "adjudicated": adjudicated, "adjudication_register": if literal { Value::Null } else { json!(REGISTER.lines().filter(|l| !l.starts_with('#') && !l.trim().is_empty()).collect::<Vec<_>>()) }, "machine_start": start});
    let watch = {
        let (rows, dir, meta) = (rows.clone(), out_dir.clone(), meta.clone());
        Watch::spawn(Duration::from_secs_f64(hard_secs), move |label, secs| {
            rows.write(&json!({"kind": "timeout", "label": label, "secs": secs}));
            rows.flush();
            let _ = write_json(
                &dir.join("verdict.json"),
                &json!({"result": "GATES FAIL", "reason": format!("a chunk ran past {hard_secs} s and was killed: {label}"), "run": meta}),
            );
            println!("gravity-gate: {label} ran {secs:.1} s, past the {hard_secs} s limit; killed\nGATES FAIL");
            std::process::exit(1);
        })
    };
    let ctx = Ctx { rows: rows.clone(), chunk_secs, hard_secs, watch: Some(watch), console: true, adjudicated: adjudicated.clone() };

    if !ev.wired() {
        rows.write(&json!({"kind": "unwired", "evaluator": ev.name()}));
        rows.flush();
        write_json(
            &out_dir.join("verdict.json"),
            &json!({"result": "GATES FAIL", "reason": "the crate adapter is not wired (xtask/src/gate/adapter.rs)", "run": meta}),
        )?;
        println!("gravity-gate: the crate adapter is not wired (xtask/src/gate/adapter.rs); nothing was run\nGATES FAIL");
        return Ok(1);
    }
    let out = execute(ev.as_ref(), &fz, &ctx, &sel);
    let end = machine_state("end");
    rows.write(&end);
    rows.flush();
    let mut meta = meta;
    meta["machine_end"] = end;
    write_verdicts(&out_dir, &out, &meta)?;
    println!("gravity-gate: rows and verdicts in {}", out_dir.display());
    println!("{}", out.label());
    Ok(out.failed() as u8)
}
