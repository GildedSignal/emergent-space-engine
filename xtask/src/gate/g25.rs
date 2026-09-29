//! G2.5 cost, per `position` call, on one performance core (the harness runs one thread and asks
//! macOS for the user-interactive QoS class, which keeps it on a P core; it cannot pin).
//! - G2.5a, natural anchors (the 20,000 random-class cases of R5: bound, unbound, plunging,
//!   radial, null): median <= 50 us and p99 <= 500 us over all timed calls.
//! - G2.5b, every case (R0 to R5, G2.2, G2.4, FB; every recorded query): max <= 5 ms.
//!
//! The median of an even count is the mean of the two middle values; p99 is the nearest rank.
//! `Geodesic::new` is not inside the timed region: it is the once-per-body cost. The verdict is
//! taken as measured, with the machine state recorded before and after.
use super::{frozen::*, run::*, types::*};
use serde_json::{json, Value};
use std::{collections::BTreeMap, hint::black_box, time::Instant};

pub const MEDIAN_US: f64 = 50.0;
pub const P99_US: f64 = 500.0;
pub const MAX_US: f64 = 5000.0;
const NATURAL_TAGS: [&str; 5] = ["bound", "unbound", "plunging", "radial", "null"];

#[derive(Default)]
pub struct G25Report {
    pub natural_ns: Vec<u64>,
    /// `Geodesic::new` on the natural anchors: recorded, not gating (G2.5 times `position`), so that
    /// cost hidden in construction is visible.
    pub construct_ns: Vec<u64>,
    pub by_class: BTreeMap<String, Vec<u64>>,
    pub all_calls: usize,
    pub max_ns: u64,
    pub max_at: (String, String),
    pub over_5ms: usize,
    /// Cases the evaluator refused: not timed, and a coverage failure.
    pub untimed_cases: usize,
    pub timer_overhead_ns: f64,
    pub qos: String,
    pub chunks: Vec<Chunk>,
    pub machine_before: Value,
    pub machine_after: Value,
    pub median_us: f64,
    pub p99_us: f64,
    pub pass_a: bool,
    pub pass_b: bool,
}
impl G25Report {
    pub fn pass(&self) -> bool {
        self.pass_a && self.pass_b
    }
}

#[cfg(target_os = "macos")]
fn set_qos() -> String {
    // SAFETY: a libc call with a valid class constant and no pointers; it only affects this thread.
    let rc = unsafe { libc::pthread_set_qos_class_self_np(libc::qos_class_t::QOS_CLASS_USER_INTERACTIVE, 0) };
    if rc == 0 {
        "user-interactive".into()
    } else {
        format!("pthread_set_qos_class_self_np failed: {rc}")
    }
}
#[cfg(not(target_os = "macos"))]
fn set_qos() -> String {
    "not macOS: not set".into()
}
fn timer_overhead() -> f64 {
    let n = 200_000u32;
    let t = Instant::now();
    for _ in 0..n {
        let a = Instant::now();
        black_box(a.elapsed());
    }
    t.elapsed().as_nanos() as f64 / n as f64
}

pub fn is_natural(j: &Judged) -> bool {
    j.case.class.first().is_some_and(|t| NATURAL_TAGS.contains(&t.as_str()))
}

pub fn run(ev: &dyn Evaluator, fz: &Frozen, ctx: &Ctx) -> G25Report {
    let mut rep = G25Report { qos: set_qos(), timer_overhead_ns: timer_overhead(), machine_before: machine_state("G2.5 start"), ..Default::default() };
    ctx.rows.write(&rep.machine_before);
    // Natural first (R5's random classes), then every other case. The natural ones also count for G2.5b.
    let mut items: Vec<(&Judged, bool)> = Vec::new();
    if fz.has("R5") {
        items.extend(fz.set("R5").iter().filter(|j| is_natural(j)).map(|j| (j, true)));
    }
    for name in ALL_SETS.iter().filter(|n| fz.has(n)) {
        items.extend(fz.set(name).iter().filter(|j| !(*name == "R5" && is_natural(j))).map(|j| (j, false)));
    }
    rep.chunks = chunked(ctx, "G2.5", &items, |chunk| {
        for (j, natural) in chunk {
            ctx.note(&j.case.id);
            let c = &j.case;
            let built = Instant::now();
            let Ok(body) = ev.new_body(c.field(), c.q, c.anchor(), c.motion) else {
                rep.untimed_cases += 1;
                continue;
            };
            if *natural {
                rep.construct_ns.push(built.elapsed().as_nanos() as u64);
            }
            for a in &j.answers {
                let t = Instant::now();
                let r = body.position(a.t);
                let ns = t.elapsed().as_nanos() as u64;
                black_box(r);
                rep.all_calls += 1;
                if ns > rep.max_ns {
                    rep.max_ns = ns;
                    rep.max_at = (c.id.clone(), a.t.to_string());
                }
                rep.over_5ms += (ns as f64 > MAX_US * 1e3) as usize;
                if *natural {
                    rep.natural_ns.push(ns);
                    rep.by_class.entry(c.class[0].clone()).or_default().push(ns);
                }
            }
        }
    });
    rep.machine_after = machine_state("G2.5 end");
    ctx.rows.write(&rep.machine_after);
    let mut sorted = rep.natural_ns.clone();
    sorted.sort_unstable();
    rep.median_us = median(&sorted) / 1e3;
    rep.p99_us = percentile(&sorted, 99.0) / 1e3;
    let covered = rep.untimed_cases == 0 && max_secs(&rep.chunks) < ctx.hard_secs;
    rep.pass_a = covered && !sorted.is_empty() && rep.median_us <= MEDIAN_US && rep.p99_us <= P99_US;
    rep.pass_b = covered && rep.all_calls > 0 && rep.max_ns as f64 <= MAX_US * 1e3;
    rep
}
impl G25Report {
    pub fn to_json(&self) -> Value {
        let class = |v: &Vec<u64>| {
            let mut s = v.clone();
            s.sort_unstable();
            json!({"calls": s.len(), "median_us": median(&s) / 1e3, "p99_us": percentile(&s, 99.0) / 1e3, "max_us": s.last().copied().unwrap_or(0) as f64 / 1e3})
        };
        json!({"gate": "G2.5", "pass": self.pass(),
            "G2.5a": {"pass": self.pass_a, "natural_calls": self.natural_ns.len(), "median_us": self.median_us, "median_limit_us": MEDIAN_US, "p99_us": self.p99_us, "p99_limit_us": P99_US,
                "by_class": self.by_class.iter().map(|(k, v)| (k.clone(), class(v))).collect::<serde_json::Map<_, _>>()},
            "G2.5b": {"pass": self.pass_b, "calls": self.all_calls, "max_us": self.max_ns as f64 / 1e3, "max_limit_us": MAX_US, "max_at": {"id": self.max_at.0, "T": self.max_at.1}, "calls_over_limit": self.over_5ms},
            "construction_not_gating": class(&self.construct_ns),
            "untimed_cases": self.untimed_cases, "timer_overhead_ns": self.timer_overhead_ns, "qos": self.qos, "one_thread": true,
            "chunks": self.chunks.len(), "max_chunk_secs": max_secs(&self.chunks), "machine_before": self.machine_before, "machine_after": self.machine_after})
    }
}
