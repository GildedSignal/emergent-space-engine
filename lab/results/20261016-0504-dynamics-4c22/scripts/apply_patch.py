#!/usr/bin/env python3
"""The run's tree edits: the Linux footprint fallback + per-frame rows + event attribution
(ES_ATTRIB) in nladder.rs, and the two locals levers in step.rs (ES_LOCAL_STAGGER, ES_LOCAL_PHASE).
Every lever is env-gated and default-off: with no env set the engine's behaviour is bit-identical
to shipped main (the arms below verify that on the digests' anchors)."""
import pathlib

root = pathlib.Path(__file__).resolve().parents[4]

def sub(path, old, new, count=1):
    p = root / path
    s = p.read_text()
    if new in s:
        return  # already applied (the script is resumable)
    assert s.count(old) == count, (path, old[:60], s.count(old))
    p.write_text(s.replace(old, new, count))

# ---- step.rs: the locals' levers -----------------------------------------------------------------
sub("crates/universe/src/step.rs", """pub(crate) fn passage_edge(ctx: &Ctx, doll: u16) -> Option<Scalar> {
    (doll != 0).then(|| ctx.dolls[doll as usize].edge.scale(2).ok()).flatten()
}""",
"""pub(crate) fn passage_edge(ctx: &Ctx, doll: u16) -> Option<Scalar> {
    (doll != 0).then(|| ctx.dolls[doll as usize].edge.scale(2).ok()).flatten()
}

// ---- lab levers (env-gated, default off; run 20261016-0504-dynamics-4c22) ------------------------
// The doll-0 clock law chains each kick's time from the kick before it (plan_clock: t + half at the
// kick's own tick), so a birth-time phase offset persists forever. The interval law instead anchors
// every interval to the ABSOLUTE power-of-two grid (aligned), so a planet-doll population born at one
// tick phase-locks to that grid: same step => same kick ticks, forever (a standing comb). The two
// levers below are the two hypotheses about that comb, both measured in the run's dossier:
//  - ES_LOCAL_STAGGER: the one-shot spread (the belt wave's cure) applied to a planet-doll ship's
//    FIRST interval only. Prediction: aligned re-absorbs the offset within one step; the comb returns.
//  - ES_LOCAL_PHASE: a PERMANENT per-body phase, a constant id-derived fraction of the body's own
//    step, added to the grid (the body's intervals stay equally spaced; cross-body coincidence breaks).
//    This gives up "every pair shares boundaries": a law change, priced here for its cost effect only.
fn env_flag(name: &str) -> bool {
    name.parse::<bool>().map(|v| v).unwrap_or(false) || std::env::var(name).is_ok_and(|v| v != "0")
}
fn local_stagger_on() -> bool {
    static ON: std::sync::LazyLock<bool> = std::sync::LazyLock::new(|| env_flag("ES_LOCAL_STAGGER"));
    *ON
}
fn local_phase_on() -> bool {
    static ON: std::sync::LazyLock<bool> = std::sync::LazyLock::new(|| env_flag("ES_LOCAL_PHASE"));
    *ON
}
/// A uniform 64-bit draw from a body id (splitmix64's finalizer): a lever's fraction of one step.
pub(crate) fn stagger_hash(mut x: u64) -> u64 {
    x = x.wrapping_add(0x9E3779B97F4A7C15);
    x = (x ^ (x >> 30)).wrapping_mul(0xBF58476D1CE4E5B9);
    x = (x ^ (x >> 27)).wrapping_mul(0x94D049BB133111EB);
    x ^ (x >> 31)
}
/// [`aligned`] on the body's own phase-shifted grid: the interval from `t` to the next multiple of
/// `step` offset by `ph` (the same stub and MIN_STEP join as the absolute grid).
fn aligned_phase(step: i64, t: Tick, ph: i64) -> i64 {
    let off = (t - ph).rem_euclid(step);
    if off == 0 {
        return step;
    }
    let stub = step - off;
    if stub < MIN_STEP {
        stub + step
    } else {
        stub
    }
}""")

# the one-shot spread: a planet-doll ship's first plan starts at t + off (off < one step)
sub("crates/universe/src/step.rs", """    fn plan_interval(&mut self, t: Tick) -> Res<()> {
        self.plan_interval_inner(t)?;
        self.plan_terminal(t)
    }""",
"""    fn plan_interval(&mut self, t: Tick) -> Res<()> {
        let t = if self.rec.step == 0 && local_stagger_on() && self.rec.b.doll != 0 && matches!(self.rec.kind, Kind::Ship) {
            // ES_LOCAL_STAGGER: the first interval of a planet-doll ship is planned from a uniform
            // id-derived fraction of its own step later; aligned() then snaps the second interval
            // back to the absolute grid (the hypothesis: the comb re-forms within one step).
            let edge = (self.rec.b.doll != 0 && matches!(self.rec.kind, Kind::Ship | Kind::Player)).then(|| self.doll().edge);
            let want = step_for(&self.rec.b, self.ctx.cfg.step_log2, edge)?;
            let off = ((stagger_hash(self.i as u64) as u128 * want as u128) >> 64) as i64;
            t + off
        } else {
            t
        };
        self.plan_interval_inner(t)?;
        self.plan_terminal(t)
    }""")

# the permanent per-body phase: the grid every interval of THIS body anchors to is shifted
sub("crates/universe/src/step.rs", """        self.rec.anchor = t;
        let mut h = aligned(self.rec.step, t);""",
"""        self.rec.anchor = t;
        let mut h = if local_phase_on() && d != 0 && matches!(self.rec.kind, Kind::Ship) {
            // ES_LOCAL_PHASE: a constant id-derived fraction of the body's OWN step (so it survives
            // step changes) offsets this body's grid; the interval lengths and the stub rules are
            // unchanged, only the absolute coincidence of same-step bodies is broken.
            let ph = ((stagger_hash(self.i as u64) as u128 * self.rec.step as u128) >> 64) as i64;
            aligned_phase(self.rec.step, t, ph)
        } else {
            aligned(self.rec.step, t)
        };""")

# ---- universe.rs: event attribution (doll x what), env ES_ATTRIB, never read by the engine --------
sub("crates/universe/src/universe.rs", """    fn resolve_body(&mut self, i: usize) {
        let Some(key) = self.key_of(i) else { return };
        let kind = self.info[i].kind;""",
"""    fn resolve_body(&mut self, i: usize) {
        let Some(key) = self.key_of(i) else { return };
        let kind = self.info[i].kind;
        if attrib::on() {
            let rec0 = self.bodies.rec(i);
            if let Some(w) = rec0.plan.first().map(|it| it.what) {
                let cls = match w { What::Kick(_) => 0u8, What::Open(_) => 1, What::Crash => 2, What::Boundary => 3 };\n                attrib::hit(rec0.b.doll, cls);
            }
        }""")

# the attribution counters themselves, top-level after the use block
sub("crates/universe/src/universe.rs", "use std::collections::VecDeque;", """use std::collections::VecDeque;

/// Lab instrument (run 20261016-0504-dynamics-4c22, env `ES_ATTRIB`): per-frame event attribution
/// by doll and item kind, atomic counters the example drains each frame. Never read by the engine.
pub mod attrib {
    use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
    pub const DOLLS: usize = 16;
    pub const WHATS: usize = 4; // Kick, Open, Crash, Boundary
    static ON: AtomicBool = AtomicBool::new(false);
    static COUNTS: [[AtomicU64; WHATS]; DOLLS] = [[AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0)],
    [AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0)],
    [AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0)],
    [AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0)],
    [AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0)],
    [AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0)],
    [AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0)],
    [AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0)],
    [AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0)],
    [AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0)],
    [AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0)],
    [AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0)],
    [AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0)],
    [AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0)],
    [AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0)],
    [AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0)]];
    pub fn arm() {
        ON.store(true, Ordering::Relaxed);
    }
    pub fn on() -> bool {
        ON.load(Ordering::Relaxed)
    }
    pub(crate) fn hit(doll: u16, what: u8) {
        if on() {
            COUNTS[(doll as usize).min(DOLLS - 1)][(what as usize).min(WHATS - 1)].fetch_add(1, Ordering::Relaxed);
        }
    }
    /// Drain the counters (the caller reads one frame's worth).
    pub fn take() -> [[u64; WHATS]; DOLLS] {
        std::array::from_fn(|d| std::array::from_fn(|w| COUNTS[d][w].swap(0, Ordering::Relaxed)))
    }
}""")
# ---- nladder.rs: Linux footprint, ES_TLIMIT, ES_ROWS + per-frame attribution ---------------------
sub("crates/universe/examples/nladder.rs", """extern "C" {
    fn proc_pid_rusage(pid: i32, flavor: i32, buffer: *mut u64) -> i32;
}""",
"""
fn linux_flag() -> bool {
    cfg!(target_os = "linux")
}""")

sub("crates/universe/examples/nladder.rs", """/// (physical footprint now, its peak over the process's life) in bytes: the memory the process holds, compressed pages
/// included (the resident size alone drops pages the machine has compressed or swapped, and this machine does under load).
fn footprint() -> (u64, u64) {
    let mut buf = [0u64; 64];
    // flavor 4: rusage_info_v4; ri_phys_footprint is word 9, ri_lifetime_max_phys_footprint word 30.
    let ok = unsafe { proc_pid_rusage(std::process::id() as i32, 4, buf.as_mut_ptr()) };
    if ok != 0 {
        return (0, 0);
    }
    (buf[9], buf[30])
}""",
"""/// (physical footprint now, its peak over the process's life) in bytes: the memory the process holds, compressed pages
/// included (the resident size alone drops pages the machine has compressed or swapped, and this machine does under load).
/// On Linux (the lab's boxes) VmRSS/VmHWM stand in: the resident size alone, the lab's numbers are orders of magnitude.
fn footprint() -> (u64, u64) {
    if linux_flag() {
        let status = std::fs::read_to_string("/proc/self/status").unwrap_or_default();
        let mut now = 0u64;
        let mut peak = 0u64;
        for line in status.lines() {
            if let Some(rest) = line.strip_prefix("VmRSS:") {
                now = rest.trim_end().trim_end_matches("kB").trim().parse().unwrap_or(0) * 1000;
            } else if let Some(rest) = line.strip_prefix("VmHWM:") {
                peak = rest.trim_end().trim_end_matches("kB").trim().parse().unwrap_or(0) * 1000;
            }
        }
        return (now, peak);
    }
    let mut buf = [0u64; 64];
    // flavor 4: rusage_info_v4; ri_phys_footprint is word 9, ri_lifetime_max_phys_footprint word 30.
    extern "C" {
        fn proc_pid_rusage(pid: i32, flavor: i32, buffer: *mut u64) -> i32;
    }
    let ok = unsafe { proc_pid_rusage(std::process::id() as i32, 4, buf.as_mut_ptr()) };
    if ok != 0 {
        return (0, 0);
    }
    (buf[9], buf[30])
}""")

sub("crates/universe/examples/nladder.rs", """        if t_start.elapsed() > Duration::from_secs(55) {""",
"""        if t_start.elapsed() > Duration::from_secs_f64(std::env::var("ES_TLIMIT").ok().and_then(|s| s.parse().ok()).unwrap_or(55.0)) {""")

sub("crates/universe/examples/nladder.rs", """    let mut rows: Vec<(usize, f64, u64, f64)> = Vec::new(); // frame, ms, events, lag s""",
"""    let mut rows: Vec<(usize, f64, u64, f64)> = Vec::new(); // frame, ms, events, lag s
    let mut attribs: Vec<[[u64; 4]; 16]> = Vec::new(); // per frame: [doll][Kick,Open,Crash,Boundary] (ES_ATTRIB)
    if std::env::var_os("ES_ATTRIB").is_some() {
        emergent_universe::universe::attrib::arm();
    }""")

sub("crates/universe/examples/nladder.rs", """        rows.push((f, took.as_secs_f64() * 1e3, frame.events, (frame.target - frame.presented) as f64 * TICK_SECONDS));""",
"""        rows.push((f, took.as_secs_f64() * 1e3, frame.events, (frame.target - frame.presented) as f64 * TICK_SECONDS));
        if emergent_universe::universe::attrib::on() {
            attribs.push(emergent_universe::universe::attrib::take());
        }""")

sub("crates/universe/examples/nladder.rs", """    println!("worst frames (frame, ms, events, lag s): {}", worst.iter().take(5).map(|r| format!("({}, {:.2}, {}, {:.3})", r.0, r.1, r.2, r.3)).collect::<Vec<_>>().join(" "));""",
"""    println!("worst frames (frame, ms, events, lag s): {}", worst.iter().take(5).map(|r| format!("({}, {:.2}, {}, {:.3})", r.0, r.1, r.2, r.3)).collect::<Vec<_>>().join(" "));
    // the worst EVENT frames' composition (doll x what), and the full per-frame rows when asked
    let mut by_events: Vec<usize> = (0..rows.len()).collect();
    by_events.sort_by_key(|&i| std::cmp::Reverse(rows[i].2));
    for &i in by_events.iter().take(6) {
        if let Some(a) = attribs.get(i) {
            let mut parts = Vec::new();
            for (d, w) in a.iter().enumerate() {
                let tot: u64 = w.iter().sum();
                if tot > 0 {
                    parts.push(format!("d{} k{} o{} c{} b{}", d, w[0], w[1], w[2], w[3]));
                }
            }
            println!("attrib frame {} events {} :: {}", rows[i].0, rows[i].2, parts.join(" | "));
        }
    }
    if std::env::var_os("ES_ROWS").is_some() {
        for (i, r) in rows.iter().enumerate() {
            let att = attribs.get(i).map(|a| {
                let mut s = Vec::new();
                for (d, w) in a.iter().enumerate() {
                    let tot: u64 = w.iter().sum();
                    if tot > 0 {
                        s.push(format!("{}:{},{},{},{}", d, w[0], w[1], w[2], w[3]));
                    }
                }
                s.join(",")
            }).unwrap_or_default();
            println!("row {} {:.1} {:.3} {} {:.3} {}", r.0, r.0 as f64 * rtf / 60.0, r.1, r.2, r.3, att);
        }
    }""")
print("patch applied")
