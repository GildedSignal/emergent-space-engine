//! G2.3 observation invariance: on 1,000 cases, `position` at T_final is bitwise equal whether
//! or not 100 intermediate queries are made first. The intermediates are 80 distinct times in
//! the working domain [T0, T_final) plus 20 repeats, in random order (seeded). Distinct times
//! are log-uniform after T0 (about 4 in 7 of the draws), log-uniform before T_final (3 in 7), and
//! fixed edge times (T0, T0 + 1, T_final - 1 to -3, and fractions of the span). A repeat must answer exactly as its first query did, and every intermediate must be
//! Free (absorption and range exit are permanent, so a Free T_final makes the whole interval
//! [T0, T_final] Free).
use super::{frozen::*, run::*, types::*};
use serde_json::{json, Value};
use std::collections::BTreeSet;

pub const CASES: usize = 1000;
pub const DISTINCT: usize = 80;
pub const REPEATS: usize = 20;
/// Pinned before the first run.
pub const SEED: u64 = 0x2026_0929_0000_0023;

pub struct Rng(u64);
impl Rng {
    pub fn new(seed: u64) -> Rng {
        Rng(seed)
    }
    pub fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
    pub fn unit(&mut self) -> f64 {
        (self.next() >> 11) as f64 / (1u64 << 53) as f64
    }
    /// A log-uniform integer in [1, n].
    pub fn log_uniform(&mut self, n: i128) -> i128 {
        ((n as f64).powf(self.unit()) as i128).clamp(1, n)
    }
}
fn fnv(s: &str) -> u64 {
    s.bytes().fold(0xcbf2_9ce4_8422_2325, |h, b| (h ^ b as u64).wrapping_mul(0x100_0000_01b3))
}

/// The 100 intermediate queries for a case with the anchor time t0 and final time tf
/// (tf - t0 >= 100): 80 distinct in [t0, tf), then 20 repeats, shuffled.
pub fn intermediates(t0: i128, tf: i128, rng: &mut Rng) -> Vec<i128> {
    let span = tf - t0;
    let mut set: BTreeSet<i128> = BTreeSet::new();
    let edges = [t0, t0 + 1, tf - 1, tf - 2, tf - 3, t0 + span / 2, t0 + span / 2 + 1, t0 + span / 4, t0 + span / 8, t0 + span - span / 8];
    set.extend(edges.iter().copied().filter(|t| (t0..tf).contains(t)));
    let mut n = 0;
    while set.len() < DISTINCT {
        n += 1;
        // 40 after t0, 30 before tf, then whichever still fills the set.
        let t = if n > 5000 {
            t0 + (n as i128) % span // a tiny span cannot fill 80 log-uniform draws quickly: sweep
        } else if n % 7 < 4 {
            t0 + rng.log_uniform(span) - 1
        } else {
            tf - rng.log_uniform(span)
        };
        if (t0..tf).contains(&t) {
            set.insert(t);
        }
    }
    let mut v: Vec<i128> = set.into_iter().collect();
    for _ in 0..REPEATS {
        let i = (rng.next() % v.len() as u64) as usize;
        v.push(v[i]);
    }
    for i in (1..v.len()).rev() {
        v.swap(i, (rng.next() % (i as u64 + 1)) as usize);
    }
    v
}

/// The 1,000 cases: those of R3 and R5 with one Free answer at least 100 chronons after T0,
/// in the order of splitmix(SEED ^ fnv(id)).
pub fn select(fz: &Frozen) -> Vec<(&Judged, i128)> {
    let mut eligible: Vec<(u64, &Judged, i128)> = ["R3", "R5"]
        .iter()
        .filter(|s| fz.has(s))
        .flat_map(|s| fz.set(s).iter())
        .filter_map(|j| match (&j.answers[..], j.case.times.first()) {
            ([a], Some(&tf)) if matches!(a.expect, Expect::Known(At::Free(_))) && tf - j.case.t0 >= 100 => {
                Some((Rng::new(SEED ^ fnv(&j.case.id)).next(), j, tf))
            }
            _ => None,
        })
        .collect();
    eligible.sort_by_key(|(k, _, _)| *k);
    eligible.into_iter().take(CASES).map(|(_, j, tf)| (j, tf)).collect()
}

#[derive(Default)]
pub struct G23Report {
    pub cases: usize,
    pub failed: usize,
    pub domain_violations: usize,
    pub repeat_inconsistent: usize,
    pub queries: usize,
    pub chunks: Vec<Chunk>,
    pub pass: bool,
    pub first: Vec<Value>,
}

fn one(ev: &dyn Evaluator, j: &Judged, tf: i128, ctx: &Ctx, rep: &mut G23Report) {
    let c = &j.case;
    let (a, b) = (ev.new_body(c.field(), c.q, c.anchor(), c.motion), ev.new_body(c.field(), c.q, c.anchor(), c.motion));
    let (Ok(a), Ok(b)) = (a, b) else {
        rep.failed += 1;
        ctx.rows.write(&json!({"kind": "case", "gate": "G2.3", "id": c.id, "pass": false, "why": "AnchorError"}));
        return;
    };
    let direct = a.position(tf);
    let qs = intermediates(c.t0, tf, &mut Rng::new(SEED ^ fnv(&c.id)));
    let mut first: std::collections::HashMap<i128, At> = Default::default();
    let (mut domain, mut repeats) = (0, 0);
    for &t in &qs {
        let r = b.position(t);
        domain += !matches!(r, At::Free(_)) as usize;
        if *first.entry(t).or_insert(r) != r {
            repeats += 1;
        }
    }
    let (after, again) = (b.position(tf), b.position(tf));
    rep.queries += qs.len() + 3;
    let pass = direct == after && after == again && domain == 0 && repeats == 0;
    rep.domain_violations += domain;
    rep.repeat_inconsistent += repeats;
    rep.failed += !pass as usize;
    let row = json!({"kind": "case", "gate": "G2.3", "id": c.id, "T_final": tf.to_string(), "intermediates": qs.len(), "distinct": first.len(), "pass": pass,
        "direct": direct.to_json(), "after_intermediates": after.to_json(), "after_again": again.to_json(), "not_free_intermediates": domain, "inconsistent_repeats": repeats});
    if !pass && rep.first.len() < 5 {
        rep.first.push(row.clone());
    }
    if !pass {
        ctx.rows.write(&row);
    }
}

pub fn run(ev: &dyn Evaluator, fz: &Frozen, ctx: &Ctx) -> G23Report {
    let mut rep = G23Report::default();
    let items = select(fz);
    rep.cases = items.len();
    rep.chunks = chunked(ctx, "G2.3", &items, |chunk| {
        for (j, tf) in chunk {
            ctx.note(&j.case.id);
            one(ev, j, *tf, ctx, &mut rep);
        }
    });
    rep.pass = rep.cases == CASES && rep.failed == 0 && max_secs(&rep.chunks) < ctx.hard_secs;
    rep
}
impl G23Report {
    pub fn to_json(&self) -> Value {
        json!({"gate": "G2.3", "cases": self.cases, "required_cases": CASES, "failed": self.failed, "queries": self.queries,
            "intermediates_per_case": DISTINCT + REPEATS, "distinct": DISTINCT, "repeats": REPEATS,
            "not_free_intermediates": self.domain_violations, "inconsistent_repeats": self.repeat_inconsistent,
            "pass": self.pass, "chunks": self.chunks.len(), "max_chunk_secs": max_secs(&self.chunks)})
    }
}
