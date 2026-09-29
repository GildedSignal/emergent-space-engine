//! G2.4 horizon, from the G2.4 files (G24 and G24edge). The comparison is on the kind of answer
//! and its chronon (Free, Absorbed at c, OutOfRange at c); coordinates are G2.1's business.
//! - Infall from rest at 10M and 100M: absorbed at ceil(T_h), T_h from the closed form stored
//!   with the case (the reference's independent computation): Free before it, Absorbed{ceil(T_h)}
//!   from it on. The judge's own answers are checked against the closed form too.
//! - Timelike E = 1 anchors moving inward on the branch connected to infinity: |L| <= 4M(1-1e-6)
//!   is absorbed and |L| >= 4M(1+1e-6) escapes. The band-edge file (|L|/4M - 1 from 1.5e-6 to
//!   9.9e-6) tests the sides. The sides are also checked against each case's stored L/4M.
use super::{frozen::*, run::*, types::*};
use serde_json::{json, Value};

pub const BAND: f64 = 1e-6;

#[derive(Default)]
pub struct G24Report {
    pub cases: usize,
    pub queries: usize,
    pub infall: usize,
    pub absorbed_side: usize,
    pub escape_side: usize,
    pub edge: usize,
    /// Cases whose absorption chronon is T0 + 1 (no free query before absorption).
    pub absorbed_at_first_chronon: usize,
    pub failed_cases: usize,
    pub disagreements: usize,
    /// The frozen files contradict each other or the band (an error of the reference, not the evaluator).
    pub reference_inconsistent: usize,
    pub chunks: Vec<Chunk>,
    pub pass: bool,
    pub first: Vec<Value>,
}

/// Kind and chronon of an answer, coordinates ignored.
fn shape(a: &At) -> (&'static str, Option<i128>) {
    (a.kind(), a.chronon())
}

fn check_case(ev: &dyn Evaluator, j: &Judged, ctx: &Ctx, rep: &mut G24Report) {
    let c = &j.case;
    let judged: Vec<At> = j.answers.iter().filter_map(|a| if let Expect::Known(at) = &a.expect { Some(*at) } else { None }).collect();
    let mut inconsistent = Vec::<String>::new();
    if judged.len() != j.answers.len() {
        inconsistent.push("UNSETTLED answer".into());
    }
    // What is expected, per T.
    let mut expected: Vec<(&'static str, Option<i128>)> = judged.iter().map(shape).collect();
    if let Some(th) = c.extra["T_h_closed_form"].as_str() {
        rep.infall += 1;
        match ceil_decimal(th) {
            Ok(h) => {
                let from_closed: Vec<_> = j.answers.iter().map(|a| if a.t >= h { ("Absorbed", Some(h)) } else { ("Free", None) }).collect();
                if from_closed != expected {
                    inconsistent.push(format!("judge's answers differ from the closed form (ceil T_h = {h})"));
                }
                expected = from_closed;
                rep.absorbed_at_first_chronon += (h == c.t0 + 1) as usize;
            }
            Err(e) => inconsistent.push(format!("bad T_h_closed_form: {e}")),
        }
    } else if c.has_class("E=1") {
        let lf = c.extra["L_over_4M"].as_str().and_then(|s| s.parse::<f64>().ok()).unwrap_or(f64::NAN);
        let any_absorbed = judged.iter().any(|a| matches!(a, At::Absorbed { .. }));
        let (absorbed_side, escape_side) = (c.has_class("absorbed"), c.has_class("escapes"));
        rep.absorbed_side += absorbed_side as usize;
        rep.escape_side += escape_side as usize;
        rep.edge += c.has_class("band-edge") as usize;
        if absorbed_side && (lf > 1.0 - BAND || lf.is_nan() || !any_absorbed) {
            inconsistent.push(format!("absorbed side with L/4M = {lf} and absorbed answers = {any_absorbed}"));
        }
        if escape_side && (lf < 1.0 + BAND || lf.is_nan() || any_absorbed) {
            inconsistent.push(format!("escape side with L/4M = {lf} and absorbed answers = {any_absorbed}"));
        }
        if let Some(At::Absorbed { chronon }) = judged.iter().find(|a| matches!(a, At::Absorbed { .. })) {
            rep.absorbed_at_first_chronon += (*chronon == c.t0 + 1) as usize;
        }
    }
    rep.reference_inconsistent += !inconsistent.is_empty() as usize;
    let mut bad = Vec::new();
    match ev.new_body(c.field(), c.q, c.anchor(), c.motion) {
        Err(e) => bad.push(json!({"why": format!("AnchorError: {e}")})),
        Ok(b) => {
            for (a, exp) in j.answers.iter().zip(&expected) {
                rep.queries += 1;
                let got = b.position(a.t);
                if shape(&got) != *exp {
                    bad.push(json!({"T": a.t.to_string(), "expected": {"at": exp.0, "chronon": exp.1.map(|c| c.to_string())}, "got": got.to_json()}));
                }
            }
        }
    }
    rep.disagreements += bad.len();
    rep.failed_cases += !bad.is_empty() as usize;
    if !bad.is_empty() || !inconsistent.is_empty() {
        let row = json!({"kind": "case", "gate": "G2.4", "id": c.id, "class": c.class, "pass": bad.is_empty() && inconsistent.is_empty(), "disagreements": bad, "reference_inconsistent": inconsistent});
        if rep.first.len() < 5 {
            rep.first.push(row.clone());
        }
        ctx.rows.write(&row);
    }
}

pub fn run(ev: &dyn Evaluator, fz: &Frozen, ctx: &Ctx) -> G24Report {
    let mut rep = G24Report::default();
    let items: Vec<&Judged> = ["G24", "G24edge"].iter().flat_map(|s| fz.set(s).iter()).collect();
    rep.cases = items.len();
    rep.chunks = chunked(ctx, "G2.4", &items, |chunk| {
        for j in chunk {
            ctx.note(&j.case.id);
            check_case(ev, j, ctx, &mut rep);
        }
    });
    rep.pass = rep.failed_cases == 0 && rep.reference_inconsistent == 0 && !items.is_empty() && max_secs(&rep.chunks) < ctx.hard_secs;
    rep
}
impl G24Report {
    pub fn to_json(&self) -> Value {
        json!({"gate": "G2.4", "cases": self.cases, "queries": self.queries, "infall_from_rest": self.infall, "E1_absorbed_side": self.absorbed_side,
            "E1_escape_side": self.escape_side, "band_edge": self.edge, "absorbed_at_first_chronon": self.absorbed_at_first_chronon,
            "failed_cases": self.failed_cases, "disagreements": self.disagreements, "reference_inconsistent": self.reference_inconsistent,
            "pass": self.pass, "chunks": self.chunks.len(), "max_chunk_secs": max_secs(&self.chunks)})
    }
}
