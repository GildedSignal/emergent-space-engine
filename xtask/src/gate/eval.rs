//! The two built-in test evaluators (more planted variants share their code). They exist to
//! prove the harness can fail. Neither is a physics evaluator.
//!
//! - `echo` replays the judge: the recorded answer for every (anchor, T) the frozen files
//!   hold, the judge's diagnostics for `orbit()` and its tau for `proper_time`. It has a pure
//!   per-body memo, which is correct and must not fail G2.3. The judge does not record the
//!   circular clock rate or the Shapiro delay, so echo takes those from the oracle functions.
//!   For a T the judge never answered it returns a deterministic pseudo position (or the
//!   permanent Absorbed/OutOfRange answer when a later recorded answer implies it).
//! - `planted` flips one floor (+1 on x0) in one chart, at one recorded (anchor, T): the first
//!   Free answer of the first case of the first rung whose class holds the chart
//!   (`planted` = three-root: R3; `planted:radial` or `planted:circular`: R1). Variants
//!   `planted-g22` (a relative 1e-6 error in proper_time, standing for the sign flip),
//!   `planted-g23` (a corrupting cache: after ten distinct queries a Free answer is off by one)
//!   `planted-g24` (the absorption chronon is one too late) and `planted-range` (the range-exit
//!   chronon is one too late) plant the other gates' bugs.
//! - `hang` is echo whose first `position` call never returns: it proves the 60 s kill (use
//!   `--hard-secs 2`).
use super::frozen::*;
use super::oracle;
use super::types::*;
use crate::Result;
use serde_json::Value;
use std::{
    cell::RefCell,
    collections::{BTreeMap, BTreeSet, HashMap},
    sync::Arc,
};

#[derive(Clone, PartialEq, Eq, Hash)]
struct Key {
    m: i128,
    q: i128,
    anchor: Anchor,
    motion: Motion,
}
struct Entry {
    m: i128,
    x0: [i128; 2],
    t0: i128,
    answers: BTreeMap<i128, (At, Option<f64>)>,
    diag: Option<Value>,
}
#[derive(Clone)]
enum Plant {
    None,
    Floor { key: Key, t: i128 },
    Clock,
    Cache,
    Absorb,
    Range,
    Hang,
}
pub struct Replay {
    label: String,
    index: HashMap<Key, Arc<Entry>>,
    plant: Plant,
    /// The (case id, T) the floor plant flips, for the tests and the run's record.
    pub planted_target: Option<(String, i128)>,
}

fn key_of(c: &Case) -> Key {
    Key { m: c.m, q: c.q, anchor: c.anchor(), motion: c.motion }
}
fn f(d: &Value, k: &str) -> f64 {
    d[k].as_str().and_then(|s| s.parse().ok()).unwrap_or(f64::NAN)
}

impl Replay {
    /// Builds the replay index from every loaded set (in canonical order). Two files that
    /// answer the same (anchor, T) differently are an error in the frozen evidence.
    pub fn new(frozen: &Frozen, label: &str) -> Result<Replay> {
        let mut index: HashMap<Key, Entry> = HashMap::new();
        for name in ALL_SETS.iter().filter(|n| frozen.has(n)) {
            for j in frozen.set(name) {
                let c = &j.case;
                let e = index.entry(key_of(c)).or_insert_with(|| Entry { m: c.m, x0: c.x, t0: c.t0, answers: BTreeMap::new(), diag: None });
                for a in &j.answers {
                    let Expect::Known(at) = &a.expect else { continue };
                    if let Some((old, _)) = e.answers.get(&a.t) {
                        if old != at {
                            return Err(format!("frozen files disagree at {} T={}: {old:?} versus {at:?}", c.id, a.t).into());
                        }
                    }
                    e.answers.insert(a.t, (*at, a.tau));
                }
                if e.diag.is_none() {
                    e.diag = j.diag.clone();
                }
            }
        }
        let index = index.into_iter().map(|(k, v)| (k, Arc::new(v))).collect();
        let mut r = Replay { label: label.to_string(), index, plant: Plant::None, planted_target: None };
        match label {
            "echo" => {}
            "planted-g22" => r.plant = Plant::Clock,
            "planted-g23" => r.plant = Plant::Cache,
            "planted-g24" => r.plant = Plant::Absorb,
            "planted-range" => r.plant = Plant::Range,
            "hang" => r.plant = Plant::Hang,
            l if l == "planted" || l.starts_with("planted:") => {
                let chart = l.strip_prefix("planted:").unwrap_or("three-root");
                for name in ["R0", "R1", "R3", "R4", "R5"].iter().filter(|n| frozen.has(n)) {
                    let hit = frozen
                        .set(name)
                        .iter()
                        .find(|j| j.case.has_class(chart) && j.answers.iter().any(|a| a.t != j.case.t0 && matches!(a.expect, Expect::Known(At::Free(_)))));
                    if let Some(j) = hit {
                        let a = j.answers.iter().find(|a| a.t != j.case.t0 && matches!(a.expect, Expect::Known(At::Free(_)))).unwrap();
                        r.plant = Plant::Floor { key: key_of(&j.case), t: a.t };
                        r.planted_target = Some((j.case.id.clone(), a.t));
                        break;
                    }
                }
                if r.planted_target.is_none() {
                    return Err(format!("no case of chart {chart:?} in the loaded sets: nothing to plant").into());
                }
            }
            other => return Err(format!("unknown built-in evaluator {other:?}").into()),
        }
        Ok(r)
    }
}

impl Evaluator for Replay {
    fn name(&self) -> String {
        self.label.clone()
    }
    fn new_body(&self, field: Field, q: i128, anchor: Anchor, motion: Motion) -> Built {
        let key = Key { m: field.m, q, anchor, motion };
        let entry = self.index.get(&key).ok_or_else(|| AnchorError(format!("{}: anchor not in the frozen files", self.label)))?;
        Ok(Box::new(ReplayBody {
            entry: entry.clone(),
            key,
            q,
            plant: self.plant.clone(),
            memo: RefCell::new(HashMap::new()),
            seen: RefCell::new(BTreeSet::new()),
        }))
    }
    fn new_body_reduced(&self, field: Field, q: i128, anchor: Anchor, motion: Motion, schedule: &[u32]) -> Option<Built> {
        // Echo's answers do not depend on any schedule, and they lie in the admissible set.
        (schedule == [16, 32, 64]).then(|| self.new_body(field, q, anchor, motion))
    }
}

struct ReplayBody {
    entry: Arc<Entry>,
    key: Key,
    q: i128,
    plant: Plant,
    memo: RefCell<HashMap<i128, At>>,
    seen: RefCell<BTreeSet<i128>>,
}
fn splitmix(mut z: u64) -> u64 {
    z = z.wrapping_add(0x9E37_79B9_7F4A_7C15);
    z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
    z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
    z ^ (z >> 31)
}
impl ReplayBody {
    /// The judge's answer, or a deterministic stand-in where the judge never answered.
    fn recorded(&self, t: i128) -> At {
        let e = &*self.entry;
        if let Some((at, _)) = e.answers.get(&t) {
            return *at;
        }
        if t < e.t0 {
            return At::Before;
        }
        // The first permanent answer (absorption or range exit) the judge recorded.
        let cut = e.answers.values().filter_map(|(a, _)| matches!(a, At::Absorbed { .. } | At::OutOfRange { .. }).then_some(*a)).min_by_key(|a| a.chronon());
        if let Some(a) = cut {
            if t >= a.chronon().unwrap() {
                return a;
            }
        }
        let h = |s: u64| (splitmix((t as u64) ^ ((t >> 64) as u64) ^ s) >> 8) as i128;
        At::Free([h(1) - (1 << 55), h(2) - (1 << 55)])
    }
}
impl Body for ReplayBody {
    fn position(&self, t: i128) -> At {
        self.seen.borrow_mut().insert(t);
        let mut at = *self.memo.borrow_mut().entry(t).or_insert_with(|| self.recorded(t));
        match &self.plant {
            Plant::None | Plant::Clock => {}
            Plant::Hang => loop {
                std::thread::sleep(std::time::Duration::from_secs(3600));
            },
            Plant::Floor { key, t: pt } => {
                if let (true, At::Free(x)) = (*key == self.key && *pt == t, at) {
                    at = At::Free([x[0] + 1, x[1]]);
                }
            }
            Plant::Cache => {
                if let (true, At::Free(x)) = (self.seen.borrow().len() > 10, at) {
                    at = At::Free([x[0] + 1, x[1]]);
                }
            }
            Plant::Absorb | Plant::Range => {
                let absorb = matches!(self.plant, Plant::Absorb);
                at = match at {
                    // One chronon late: Free at the true chronon, and the shifted chronon after it.
                    At::Absorbed { chronon: c } if absorb => {
                        if t == c {
                            At::Free([0, 0])
                        } else {
                            At::Absorbed { chronon: c + 1 }
                        }
                    }
                    At::OutOfRange { chronon: c } if !absorb => {
                        if t == c {
                            At::Free([0, 0])
                        } else {
                            At::OutOfRange { chronon: c + 1 }
                        }
                    }
                    other => other,
                };
            }
        }
        at
    }
    fn orbit(&self) -> Orbit {
        let Some(d) = &self.entry.diag else { return Orbit::nothing() };
        let kind = d["kind"].as_str().unwrap_or("");
        let class = match kind {
            "bound" => OrbitClass::Bound,
            "unbound" => OrbitClass::Unbound,
            "plunging" => OrbitClass::Plunging,
            k if k.starts_with("radial") => OrbitClass::Radial,
            "circular" => OrbitClass::Circular,
            _ => OrbitClass::Marginal,
        };
        Orbit {
            energy: f(d, "E"),
            angular_momentum: f(d, "L_quanta"),
            class,
            p: f(d, "p_over_M"),
            e: f(d, "e"),
            radial_period: f(d, "period_T_chronons"),
            proper_radial_period: f(d, "period_tau_chronons"),
            periapsis_advance: f(d, "advance_rad"),
            deflection: f(d, "deflection_rad"),
            static_clock_rate: f(d, "static_clock_rate_r0"),
            circular_clock_rate: oracle::circular_clock_rate(oracle::radius_over_m(self.entry.x0, self.entry.m)),
        }
    }
    fn proper_time(&self, t: i128) -> f64 {
        let tau = self.entry.answers.get(&t).and_then(|(_, tau)| *tau).unwrap_or(f64::NAN);
        if matches!(self.plant, Plant::Clock) {
            tau * (1.0 + 1e-6)
        } else {
            tau
        }
    }
    fn shapiro_delay(&self, r1: f64, r2: f64) -> Option<f64> {
        let d = self.entry.diag.as_ref()?;
        let b = f(d, "b_over_M");
        if b.is_nan() {
            return None;
        }
        let (m, r0) = (self.entry.m as f64, oracle::null_turning_radius(b));
        Some(oracle::shapiro(r0, r1 / m, r2 / m) * m / self.q as f64)
    }
}
