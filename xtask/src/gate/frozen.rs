//! The frozen reference answers (artifacts/evidence/g2-reference-20260928/PROVENANCE.md).
//! Files are gzip JSON lines, read by shelling out to `gzip -dc`.
use super::types::*;
use crate::Result;
use serde_json::Value;
use std::{collections::HashMap, path::Path, process::Command};

pub const DEFAULT_DIR: &str = concat!(env!("CARGO_MANIFEST_DIR"), "/../artifacts/evidence/g2-reference-20260928");
/// In canonical order. R2 is stored as answers only, and R5 in ten slices.
pub const ALL_SETS: &[&str] = &["R0", "R1", "R2", "R3", "R4", "R5", "G22", "G24", "G24edge", "FB"];

#[derive(Clone, Debug)]
pub struct Case {
    pub id: String,
    pub class: Vec<String>,
    pub m: i128,
    pub q: i128,
    pub t0: i128,
    pub x: [i128; 2],
    pub k: [i128; 2],
    pub motion: Motion,
    pub times: Vec<i128>,
    /// The record's other fields: construction notes, T_h_closed_form, L_over_4M, ...
    pub extra: Value,
}
#[derive(Clone, Debug)]
pub struct Answer {
    pub t: i128,
    pub expect: Expect,
    /// Proper time in chronons at t (absent for OutOfRange and Before).
    pub tau: Option<f64>,
    /// log2 of each coordinate's distance to the nearest integer (None: exactly an integer, or absent).
    pub dist: [Option<f64>; 2],
}
#[derive(Clone, Debug)]
pub struct Judged {
    pub case: Case,
    pub answers: Vec<Answer>,
    pub diag: Option<Value>,
}
impl Case {
    pub fn field(&self) -> Field {
        Field { m: self.m }
    }
    pub fn anchor(&self) -> Anchor {
        Anchor { t: self.t0, x: self.x, k: self.k }
    }
    pub fn has_class(&self, c: &str) -> bool {
        self.class.iter().any(|s| s == c)
    }
}

pub struct Frozen {
    sets: HashMap<String, Vec<Judged>>,
    /// FB.widths records by case id.
    pub fb_widths: HashMap<String, Value>,
}

/// `gzip -dc path`, as lines.
pub fn gz_lines(path: &Path) -> Result<Vec<String>> {
    let out = Command::new("gzip").arg("-dc").arg(path).output().map_err(|e| format!("cannot run gzip: {e}"))?;
    if !out.status.success() {
        return Err(format!("gzip -dc {} failed: {}", path.display(), String::from_utf8_lossy(&out.stderr)).into());
    }
    let text = String::from_utf8(out.stdout).map_err(|e| format!("{}: not UTF-8: {e}", path.display()))?;
    Ok(text.lines().filter(|l| !l.trim().is_empty()).map(String::from).collect())
}
fn gz_records(path: &Path) -> Result<Vec<Value>> {
    gz_lines(path)?.iter().enumerate().map(|(i, l)| serde_json::from_str(l).map_err(|e| format!("{}:{}: {e}", path.display(), i + 1).into())).collect()
}

pub fn case_of(v: &Value) -> Result<Case> {
    let id = v["id"].as_str().ok_or("case without id")?.to_string();
    let ctx = |e: Box<dyn std::error::Error>| -> Box<dyn std::error::Error> { format!("{id}: {e}").into() };
    let motion = match v["motion"].as_str() {
        Some("timelike") => Motion::Timelike,
        Some("null") => Motion::Null,
        other => return Err(format!("{id}: bad motion {other:?}").into()),
    };
    let class = v["class"].as_array().map(|a| a.iter().filter_map(|c| c.as_str().map(String::from)).collect()).unwrap_or_default();
    let times = v["T"].as_array().ok_or_else(|| format!("{id}: no T"))?.iter().map(|t| int_of(t).map_err(ctx)).collect::<Result<Vec<_>>>()?;
    let mut extra = v.clone();
    if let Some(o) = extra.as_object_mut() {
        for k in ["id", "rung", "class", "M", "Q", "t0", "x", "k", "motion", "T"] {
            o.remove(k);
        }
    }
    Ok(Case {
        m: int_of(&v["M"]).map_err(ctx)?,
        q: int_of(&v["Q"]).map_err(ctx)?,
        t0: int_of(&v["t0"]).map_err(ctx)?,
        x: int_pair(&v["x"]).map_err(ctx)?,
        k: int_pair(&v["k"]).map_err(ctx)?,
        id,
        class,
        motion,
        times,
        extra,
    })
}

fn join(cases: Vec<Case>, answers: Vec<Value>, set: &str) -> Result<Vec<Judged>> {
    let mut by_id: HashMap<String, Value> = HashMap::new();
    for a in answers {
        let id = a["id"].as_str().ok_or("answer without id")?.to_string();
        if by_id.insert(id.clone(), a).is_some() {
            return Err(format!("{set}: duplicate answer for {id}").into());
        }
    }
    let mut out = Vec::with_capacity(cases.len());
    for case in cases {
        let rec = by_id.remove(&case.id).ok_or_else(|| format!("{set}: no answer for {}", case.id))?;
        let list = rec["answers"].as_array().ok_or_else(|| format!("{}: no answers", case.id))?;
        if list.len() != case.times.len() {
            return Err(format!("{}: {} answers for {} queries", case.id, list.len(), case.times.len()).into());
        }
        let mut answers = Vec::with_capacity(list.len());
        for (a, t) in list.iter().zip(&case.times) {
            if int_of(&a["T"])? != *t {
                return Err(format!("{}: answer T {} differs from the case's {t}", case.id, a["T"]).into());
            }
            let tau = a["tau"].as_str().and_then(|s| s.parse::<f64>().ok());
            let dist = [a["dist"][0].as_f64(), a["dist"][1].as_f64()];
            answers.push(Answer { t: *t, expect: expect_of(a)?, tau, dist });
        }
        out.push(Judged { case, answers, diag: rec.get("diag").cloned() });
    }
    if !by_id.is_empty() {
        return Err(format!("{set}: {} answers without a case", by_id.len()).into());
    }
    Ok(out)
}

/// R2: M = 1, Q = 25, t0 = 0, T = 1..8; one line per anchor [x, y, kx, ky, [answers]].
fn load_r2(dir: &Path) -> Result<Vec<Judged>> {
    let lines = gz_lines(&dir.join("R2.answers.jsonl.gz"))?;
    let head: Value = serde_json::from_str(lines.first().ok_or("R2.answers is empty")?)?;
    if int_of(&head["M"])? != 1 || int_of(&head["Q"])? != 25 || int_of(&head["t0"])? != 0 || head["T"] != serde_json::json!([1, 2, 3, 4, 5, 6, 7, 8]) {
        return Err(format!("R2 header differs from the contract's small world: {head}").into());
    }
    let mut out = Vec::with_capacity(lines.len() - 1);
    for (n, line) in lines.iter().enumerate().skip(1) {
        let rec: Value = serde_json::from_str(line).map_err(|e| format!("R2.answers:{}: {e}", n + 1))?;
        let a = rec.as_array().filter(|a| a.len() == 5).ok_or_else(|| format!("R2.answers:{}: bad record", n + 1))?;
        let (x, k) = ([int_of(&a[0])?, int_of(&a[1])?], [int_of(&a[2])?, int_of(&a[3])?]);
        let list = a[4].as_array().filter(|l| l.len() == 8).ok_or_else(|| format!("R2.answers:{}: need 8 answers", n + 1))?;
        let times: Vec<i128> = (1..=8).collect();
        let answers =
            list.iter().zip(&times).map(|(v, t)| Ok(Answer { t: *t, expect: expect_of_r2(v)?, tau: None, dist: [None, None] })).collect::<Result<Vec<_>>>()?;
        let case = Case {
            id: format!("R2[{},{};{},{}]", x[0], x[1], k[0], k[1]),
            class: vec!["R2".into()],
            m: 1,
            q: 25,
            t0: 0,
            x,
            k,
            motion: Motion::Timelike,
            times,
            extra: Value::Null,
        };
        out.push(Judged { case, answers, diag: None });
    }
    Ok(out)
}

impl Frozen {
    /// Loads the named sets (see ALL_SETS). Fails on any inconsistency between cases and answers.
    pub fn load(dir: &Path, names: &[&str]) -> Result<Frozen> {
        let mut sets = HashMap::new();
        let mut fb_widths = HashMap::new();
        for &name in names {
            let judged = match name {
                "R2" => load_r2(dir)?,
                "R5" => {
                    let cases = gz_records(&dir.join("R5.cases.jsonl.gz"))?.iter().map(case_of).collect::<Result<Vec<_>>>()?;
                    let mut answers = Vec::new();
                    for i in 0..10 {
                        answers.extend(gz_records(&dir.join(format!("R5-slice{i}.answers.jsonl.gz")))?);
                    }
                    join(cases, answers, name)?
                }
                _ => {
                    let cases = gz_records(&dir.join(format!("{name}.cases.jsonl.gz")))?.iter().map(case_of).collect::<Result<Vec<_>>>()?;
                    join(cases, gz_records(&dir.join(format!("{name}.answers.jsonl.gz")))?, name)?
                }
            };
            if name == "FB" {
                for w in gz_records(&dir.join("FB.widths.jsonl.gz"))? {
                    fb_widths.insert(w["id"].as_str().ok_or("FB.widths without id")?.to_string(), w);
                }
            }
            sets.insert(name.to_string(), judged);
        }
        Ok(Frozen { sets, fb_widths })
    }
    /// A frozen set built in memory (tests).
    #[cfg(test)]
    pub fn synthetic(name: &str, judged: Vec<Judged>) -> Frozen {
        Frozen { sets: HashMap::from([(name.to_string(), judged)]), fb_widths: HashMap::new() }
    }
    pub fn set(&self, name: &str) -> &[Judged] {
        self.sets.get(name).unwrap_or_else(|| panic!("frozen set {name} was not loaded")).as_slice()
    }
    pub fn has(&self, name: &str) -> bool {
        self.sets.contains_key(name)
    }
}

/// Verifies SHA256SUMS in the evidence directory (`shasum -a 256 -c`, or `sha256sum -c`).
/// The gate must not run against answers that differ from the frozen ones.
pub fn verify_hashes(dir: &Path) -> Result<String> {
    for (prog, args) in [("shasum", &["-a", "256", "-c", "SHA256SUMS"][..]), ("sha256sum", &["-c", "SHA256SUMS"][..])] {
        if let Ok(out) = Command::new(prog).args(args).current_dir(dir).output() {
            let text = String::from_utf8_lossy(&out.stdout).to_string();
            if !out.status.success() {
                let bad: Vec<&str> = text.lines().filter(|l| !l.ends_with(": OK")).collect();
                return Err(format!("frozen evidence differs from SHA256SUMS: {}", bad.join("; ")).into());
            }
            return Ok(format!("{} files verified by {prog}", text.lines().filter(|l| l.ends_with(": OK")).count()));
        }
    }
    Err("neither shasum nor sha256sum could run".into())
}
