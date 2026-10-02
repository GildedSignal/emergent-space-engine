//! The Verlet skin on the Binet cone (lens: encounters without a setup per element change).
//!
//! A pair's certificate (sections + windows + the integer first-hit query) is set up once. A kick
//! moves the body's Binet point; the certificate is re-set up only when the kicks accumulated since
//! its setup exceed the skin s (molecular dynamics' Verlet list), and the cone test at each scan is
//! padded by s so pairs that were skipped cannot have become candidates in between (cone_gap is
//! 2-Lipschitz in the Binet-point difference).
//!
//! Soundness between re-setups needs slack in the certificate itself, not only in the cone:
//!  - the arcs are built with eps_u + s (sections_pad): drift moves |Δu(θ)| by at most the drift;
//!  - the query window is widened by the accumulated |Δperiod| since setup times the revolutions
//!    since setup (the integer circle rotation's step and anchors drift by that much);
//!  - the check intervals are stretched by the period drift fraction.
//!
//! Configurations:
//!  - `always`: r8 v3's behaviour — every kick re-scans and re-sets up its body's candidate pairs.
//!  - `skin`:   the padded, slack-protected deferral above.
//!  - `naive`:  the lens read literally — cone padded, re-setup on the drift trigger, but stored
//!              sections and windows used as they are (no padding, no widening). Falsifier.
//!
//! One JSON object per line on stdout.

use emergent_encounters::belt::{make_belt, Rng, Spec};
use emergent_encounters::kepler::{Body, TICKS};
use emergent_encounters::method::{run_section, Stats};
use emergent_encounters::pairs::{cone_gap, eps_u, sections_pad, Section, Sorted};
use emergent_encounters::truth::{truth_pair, TruthStats};
use std::collections::HashMap;
use std::f64::consts::TAU;
use std::time::Instant;

const SAFETY: f64 = 1.1;
/// Horizon of the query done at (re)setup: the engine certifies the pair's next events this far.
const HQ: f64 = 100.0 * TAU;
/// Segment length (kicks are quantized to segment boundaries; elements are constant within).
const SEG: f64 = TAU;

#[derive(Clone, Copy, PartialEq, Debug)]
enum Mode {
    Always,
    Skin,
    Naive,
}

impl Mode {
    fn name(self) -> &'static str {
        match self {
            Mode::Always => "always",
            Mode::Skin => "skin",
            Mode::Naive => "naive",
        }
    }
}

struct Cert {
    i: u32,
    j: u32,
    /// dbin anchors at setup.
    b0: [f64; 2],
    /// accumulated |Δperiod| anchors at setup (ticks).
    p0: [f64; 2],
    /// setup time (time units).
    t0: f64,
    secs: Vec<Section>,
}

#[derive(Default)]
struct Counters {
    kicks: u64,
    scans: u64,
    cone_tests: u64,
    setups: u64,
    trig_resets: u64,
    sat_resets: u64,
    cert_samples: u64,
    false_cand: u64,
    events: u64,
    /// query work in the per-segment maintenance pass
    pass_checks: u64,
    pass_queries: u64,
    us_scan: f64,
    us_setup: f64,
    us_pass: f64,
    st: Stats,
}

struct World {
    b: Vec<Body>,
    dbin: Vec<f64>,
    dper: Vec<f64>,
    scan_anchor: Vec<f64>,
    certs: HashMap<(u32, u32), Cert>,
    rho: f64,
    s: f64,
    /// extra U-reach for the within-segment staleness of the sorted index (per kick |δU| ≤ eps).
    reach_extra: f64,
    mode: Mode,
    c: Counters,
}

fn key(i: u32, j: u32) -> (u32, u32) {
    (i.min(j), i.max(j))
}

fn dist3(a: [f64; 3], b: [f64; 3]) -> f64 {
    let d = [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
    (d[0] * d[0] + d[1] * d[1] + d[2] * d[2]).sqrt()
}

impl World {
    fn new(b: Vec<Body>, rho: f64, s: f64, mode: Mode, reach_extra: f64) -> Self {
        let n = b.len();
        World {
            b,
            dbin: vec![0.0; n],
            dper: vec![0.0; n],
            scan_anchor: vec![0.0; n],
            certs: HashMap::new(),
            rho,
            s,
            reach_extra,
            mode,
            c: Counters::default(),
        }
    }

    /// A full (re)set up: padded sections plus the horizon query. The expensive unit.
    fn setup(&mut self, i: u32, j: u32, t: f64) {
        let t0 = Instant::now();
        let (i, j) = (i.min(j), i.max(j));
        let bi = self.b[i as usize];
        let bj = self.b[j as usize];
        let pad = if self.mode == Mode::Skin { self.s } else { 0.0 };
        let mut secs = sections_pad(&bi, &bj, self.rho, SAFETY, pad, &mut self.c.st.evals);
        let mut ev = Vec::new();
        for sec in &secs {
            run_section(&bi, &bj, sec, self.rho, t, t + HQ, &mut self.c.st, &mut ev);
        }
        self.c.events += ev.len() as u64;
        secs.shrink_to_fit();
        let cert = Cert {
            i,
            j,
            b0: [self.dbin[i as usize], self.dbin[j as usize]],
            p0: [self.dper[i as usize], self.dper[j as usize]],
            t0: t,
            secs,
        };
        self.certs.insert(key(i, j), cert);
        self.c.setups += 1;
        self.c.us_setup += t0.elapsed().as_secs_f64();
    }

    /// The certificate's sections widened for the drift accumulated since setup.
    /// None: saturated (the widened window would swallow a quarter of the period).
    fn widened(&self, cert: &Cert, t1: f64) -> Option<Vec<Section>> {
        let dpi = self.dper[cert.i as usize] - cert.p0[0];
        let dpj = self.dper[cert.j as usize] - cert.p0[1];
        let dp = (dpi + dpj).max(0.0);
        let pj = self.b[cert.j as usize].period as f64;
        let pi = self.b[cert.i as usize].period as i64;
        let revs = (((t1 - cert.t0) * TICKS / pj).max(1.0) + 1.0) * 1.5;
        let w = (revs * dp).ceil() as i64;
        let f = 2.0 * dp / pj;
        let wt = w as f64 / TICKS;
        let mut out = Vec::with_capacity(cert.secs.len());
        for sec in &cert.secs {
            let mut s2 = sec.clone();
            if s2.w1 + s2.w2 + 2 * w > pi / 4 {
                return None;
            }
            s2.w1 = (s2.w1 + w).max(0);
            s2.w2 = (s2.w2 + w).max(0);
            // the drifted conjunction lies within ±wt of the proposed offset: the check interval
            // must stretch with it, and its bracketing resolution with the interval.
            let span = s2.di.0 + s2.di.1 + s2.dj.0 + s2.dj.1;
            let span = if span > 1e-9 { span } else { pj / TICKS };
            s2.kscale = 1.0 + 4.0 * wt / span;
            s2.di = (s2.di.0 * (1.0 + f) + wt, s2.di.1 * (1.0 + f) + wt);
            s2.dj = (s2.dj.0 * (1.0 + f) + wt, s2.dj.1 * (1.0 + f) + wt);
            out.push(s2);
        }
        Some(out)
    }

    /// One body's range scan: fresh certs for pairs entering the (padded) cone, drops for pairs
    /// that left it. `sorted` is rebuilt once per segment; `reach_extra` covers its staleness.
    fn scan(&mut self, sorted: &Sorted, i: u32, t: f64) {
        let t0 = Instant::now();
        if self.mode == Mode::Always {
            // the baseline: every kick re-sets up all of its body's candidate pairs
            let drop: Vec<(u32, u32)> = self.certs.keys().copied().filter(|&k| k.0 == i || k.1 == i).collect();
            for k in drop {
                self.certs.remove(&k);
            }
        }
        let bi = self.b[i as usize];
        let pad = if self.mode == Mode::Always { 0.0 } else { self.s };
        let (lo, hi) = sorted.range(bi.binet()[0], sorted.reach(&bi) + self.reach_extra + pad);
        let mut drop_later = Vec::new();
        let mut setup_later = Vec::new();
        for &(_, j) in &sorted.order[lo..hi] {
            if j == i {
                continue;
            }
            self.c.cone_tests += 1;
            let bj = self.b[j as usize];
            if cone_gap(&bi, &bj) < eps_u(&bi, &bj, self.rho) + pad {
                if !self.certs.contains_key(&key(i, j)) {
                    setup_later.push(j);
                }
            } else if self.certs.contains_key(&key(i, j)) {
                drop_later.push(j);
            }
        }
        self.c.scans += 1;
        self.c.us_scan += t0.elapsed().as_secs_f64();
        for j in setup_later {
            self.setup(i, j, t);
        }
        for j in drop_later {
            self.certs.remove(&key(i, j));
        }
    }

    /// A kick at time `t`: elements change (a scaled, e, ϖ and mean longitude continuous).
    fn kick(&mut self, i: usize, t: f64, frac: f64) {
        let old = self.b[i];
        let lam = old.mean_anomaly(t) + old.pom;
        let a_new = old.a * (1.0 + frac);
        let n_new = a_new.powf(-1.5);
        let new = Body::new(a_new, old.e, old.pom, lam - n_new * t);
        self.dbin[i] += dist3(new.binet(), old.binet());
        self.dper[i] += (new.period as f64 - old.period as f64).abs();
        self.b[i] = new;
        self.c.kicks += 1;
    }

    /// The per-segment maintenance pass: drift triggers, false-candidate census, and the short
    /// query over [t0, t1] that yields the segment's events.
    fn segment_pass(&mut self, t0: f64, t1: f64, out: &mut Vec<(u32, u32, f64, f64)>) {
        let ts = Instant::now();
        let keys: Vec<(u32, u32)> = self.certs.keys().copied().collect();
        for k in keys {
            // drift trigger first
            let (i, j) = k;
            let (bi, bj) = (self.b[i as usize], self.b[j as usize]);
            self.c.cert_samples += 1;
            self.c.false_cand += (cone_gap(&bi, &bj) >= eps_u(&bi, &bj, self.rho)) as u64;
            if self.mode != Mode::Always {
                let cert = &self.certs[&k];
                let drift = (self.dbin[i as usize] - cert.b0[0]) + (self.dbin[j as usize] - cert.b0[1]);
                if 2.0 * drift >= self.s {
                    self.c.trig_resets += 1;
                    self.setup(i, j, t0);
                }
            }
            let cert = match self.certs.get(&k) {
                Some(c) => c,
                None => continue,
            };
            let secs = match self.mode {
                Mode::Always => Some(cert.secs.clone()),
                Mode::Skin => match self.widened(cert, t1) {
                    Some(x) => Some(x),
                    None => {
                        self.c.sat_resets += 1;
                        self.setup(i, j, t0);
                        self.certs.get(&k).map(|c| c.secs.clone())
                    }
                },
                Mode::Naive => Some(cert.secs.clone()),
            };
            let secs = match secs {
                Some(x) => x,
                None => continue,
            };
            let mut ev = Vec::new();
            for sec in &secs {
                let before = self.c.st.checks_total();
                run_section(&bi, &bj, sec, self.rho, t0, t1, &mut self.c.st, &mut ev);
                self.c.pass_checks += self.c.st.checks_total() - before;
                self.c.pass_queries += 1;
            }
            self.c.events += ev.len() as u64;
            for &(t, d) in &ev {
                out.push((i, j, t, d));
            }
        }
        self.c.us_pass += ts.elapsed().as_secs_f64();
    }
}

/// The kick schedule, drawn once so every configuration receives the identical kicks.
fn schedule(n: usize, segments: usize, kappa: f64, eps: f64, seed: u64) -> Vec<Vec<(usize, f64)>> {
    let mut r = Rng(seed);
    let whole = kappa.floor() as usize;
    let frac = kappa - kappa.floor();
    (0..segments)
        .map(|_| {
            let mut v = Vec::new();
            for i in 0..n {
                let mut count = whole + (r.f64() < frac) as usize;
                while count > 0 {
                    count -= 1;
                    let sign = if r.f64() < 0.5 { -1.0 } else { 1.0 };
                    v.push((i, eps * sign));
                }
            }
            v
        })
        .collect()
}

struct Case {
    name: String,
    bodies: Vec<Body>,
    rho: f64,
    orbits: f64,
}

fn make_case(name: &str, seed: u64) -> Case {
    match name {
        "belt" => {
            let sp = Spec {
                name: "belt".into(),
                n: 2000,
                sigma_e: 1e-2,
                rho: 1e-4,
                a_lo: 1.0,
                a_hi: 1.5,
                keys: 0,
                seed,
                orbits: 20.0,
            };
            Case { name: "belt".into(), bodies: make_belt(&sp), rho: sp.rho, orbits: 20.0 }
        }
        "belt10k" => {
            let sp = Spec {
                name: "belt10k".into(),
                n: 10_000,
                sigma_e: 1e-2,
                rho: 1e-4,
                a_lo: 1.0,
                a_hi: 1.5,
                keys: 0,
                seed,
                orbits: 6.0,
            };
            Case { name: "belt10k".into(), bodies: make_belt(&sp), rho: sp.rho, orbits: 6.0 }
        }
        "ring" => {
            let sp = Spec {
                name: "ring".into(),
                n: 400,
                sigma_e: 0.025,
                rho: 3e-3,
                a_lo: 1.0,
                a_hi: 1.0025,
                keys: 0,
                seed,
                orbits: 10.0,
            };
            Case { name: "ring".into(), bodies: make_belt(&sp), rho: sp.rho, orbits: 10.0 }
        }
        "fleet" => {
            // A fleet in formation: nearby orbits, near-circular, clustered periapses and phases.
            let mut r = Rng(seed);
            let bodies = (0..400)
                .map(|_| {
                    let a = 1.0 + 0.01 * r.f64();
                    let e = (3e-4 * (-2.0 * (1.0 - r.f64()).ln()).sqrt()).min(0.5);
                    let pom = 0.2 * (r.f64() - 0.5) * TAU;
                    let lam = 0.1 * (r.f64() - 0.5) * TAU;
                    Body::new(a, e, pom, lam)
                })
                .collect();
            Case { name: "fleet".into(), bodies, rho: 1e-3, orbits: 10.0 }
        }
        _ => panic!("unknown case"),
    }
}

struct RunResult {
    events: Vec<(usize, u32, u32, f64, f64)>,
    c: Counters,
    wall: f64,
}

fn run(case: &Case, mode: Mode, s: f64, eps: f64, kappa: f64, seed: u64) -> RunResult {
    let segments = (case.orbits * TAU / SEG).round() as usize;
    let sched = schedule(case.bodies.len(), segments, kappa, eps, seed);
    let mut w = World::new(case.bodies.clone(), case.rho, s, mode, 4.0 * eps * (kappa + 1.0));
    let wall = Instant::now();
    // initial scan: every padded-candidate pair once
    {
        let sorted = Sorted::new(&w.b, w.rho);
        let pad = if mode == Mode::Always { 0.0 } else { s };
        let mut setup_later = Vec::new();
        for (k, &(u, i)) in sorted.order.iter().enumerate() {
            let bi = w.b[i as usize];
            let (lo, hi) = sorted.range(u, sorted.reach(&bi) + pad);
            for &(_, j) in &sorted.order[lo.max(k + 1)..hi] {
                w.c.cone_tests += 1;
                let bj = &w.b[j as usize];
                if cone_gap(&bi, bj) < eps_u(&bi, bj, w.rho) + pad {
                    setup_later.push((i, j));
                }
            }
        }
        w.c.scans += case.bodies.len() as u64;
        for (i, j) in setup_later {
            w.setup(i, j, 0.0);
        }
    }
    let mut all_events = Vec::new();
    for (sg, seg_kicks) in sched.iter().enumerate() {
        let t_a = sg as f64 * SEG;
        let t_b = t_a + SEG;
        // apply this segment's kicks
        for &(i, frac) in seg_kicks {
            w.kick(i, t_a, frac);
        }
        // scans
        let sorted = Sorted::new(&w.b, w.rho);
        match mode {
            Mode::Always => {
                let mut done = vec![false; w.b.len()];
                for &(i, _) in seg_kicks {
                    if done[i] {
                        continue;
                    }
                    done[i] = true;
                    w.scan(&sorted, i as u32, t_a);
                }
            }
            _ => {
                for &(i, _) in seg_kicks {
                    if w.dbin[i] - w.scan_anchor[i] >= s / 4.0 {
                        w.scan_anchor[i] = w.dbin[i];
                        w.scan(&sorted, i as u32, t_a);
                    }
                }
            }
        }
        // maintenance pass: triggers + short query
        let mut ev = Vec::new();
        w.segment_pass(t_a, t_b, &mut ev);
        for &(i, j, t, d) in &ev {
            all_events.push((sg, i, j, t, d));
        }
    }
    RunResult { events: all_events, c: w.c, wall: wall.elapsed().as_secs_f64() }
}

/// Match two event lists per (segment, pair): misses and false, tolerance `tol` in time units.
fn compare(truth: &[(usize, u32, u32, f64, f64)], other: &[(usize, u32, u32, f64, f64)], tol: f64) -> (u64, u64, u64) {
    let mut by_pair: HashMap<(usize, u32, u32), Vec<f64>> = HashMap::new();
    for &(sg, i, j, t, _) in other {
        by_pair.entry((sg, i, j)).or_default().push(t);
    }
    let mut missed = 0u64;
    for &(sg, i, j, t, _) in truth {
        if !by_pair.get(&(sg, i, j)).is_some_and(|v| v.iter().any(|&x| (x - t).abs() < tol)) {
            missed += 1;
        }
    }
    let mut tby: HashMap<(usize, u32, u32), Vec<f64>> = HashMap::new();
    for &(sg, i, j, t, _) in truth {
        tby.entry((sg, i, j)).or_default().push(t);
    }
    let mut false_ = 0u64;
    for &(sg, i, j, t, _) in other {
        if !tby.get(&(sg, i, j)).is_some_and(|v| v.iter().any(|&x| (x - t).abs() < tol)) {
            false_ += 1;
        }
    }
    (missed, false_, truth.len() as u64)
}

/// Independent dense truth for one segment: phase-reanchored copies, conservative advancement.
fn segment_truth(b: &[Body], pairs: &[(u32, u32)], rho: f64, t_a: f64, seg: f64, out: &mut Vec<(u32, u32, f64, f64)>) {
    let shifted: Vec<Body> = b
        .iter()
        .map(|x| {
            let lam = x.mean_anomaly(t_a) + x.pom;
            Body::new(x.a, x.e, x.pom, lam)
        })
        .collect();
    let mut st = TruthStats::default();
    for &(i, j) in pairs {
        let mut v = Vec::new();
        truth_pair(&shifted[i as usize], &shifted[j as usize], rho, seg, &mut v, &mut st);
        for &(t, d) in &v {
            out.push((i, j, t + t_a, d));
        }
    }
}

fn radial_pairs(b: &[Body], rho: f64) -> Vec<(u32, u32)> {
    emergent_encounters::pairs::radial_pairs(b, rho)
}

fn median_eps_u(b: &[Body], rho: f64) -> f64 {
    let mut v: Vec<f64> = b.iter().map(|x| eps_u(x, x, rho)).collect();
    v.sort_by(|a, c| a.total_cmp(c));
    v[v.len() / 2]
}

#[allow(clippy::too_many_arguments)]
fn report(case: &str, mode: Mode, s_frac: f64, eps: f64, kappa: f64, r: &RunResult, missed: u64, false_e: u64, truth_n: u64) {
    let c = &r.c;
    let kicks = c.kicks.max(1) as f64;
    let us_kick = (c.us_scan + c.us_setup + c.us_pass) * 1e6 / kicks;
    println!(
        "{{\"case\":\"{}\",\"mode\":\"{}\",\"s_frac\":{},\"eps\":{:e},\"kappa\":{},\"kicks\":{},\"scans_per_kick\":{:.4},\"setups_per_kick\":{:.4},\
\"us_per_kick\":{:.2},\"us_setup_per_kick\":{:.2},\"us_scan_per_kick\":{:.2},\"us_pass_per_kick\":{:.2},\"checks_per_kick\":{:.2},\
\"trig_resets\":{},\"sat_resets\":{},\"false_cand_frac\":{:.4},\"events\":{},\"missed\":{},\"false\":{},\"truth_n\":{},\"wall_s\":{:.1}}}",
        case,
        mode.name(),
        s_frac,
        eps,
        kappa,
        c.kicks,
        c.scans as f64 / kicks,
        c.setups as f64 / kicks,
        us_kick,
        c.us_setup * 1e6 / kicks,
        c.us_scan * 1e6 / kicks,
        c.us_pass * 1e6 / kicks,
        c.st.checks_total() as f64 / kicks,
        c.trig_resets,
        c.sat_resets,
        c.false_cand as f64 / c.cert_samples.max(1) as f64,
        c.events,
        missed,
        false_e,
        truth_n,
        r.wall
    );
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let seed = 20261002u64;
    match args.get(1).map(|s| s.as_str()) {
        Some("sweep") => {
            let case_name = &args[2];
            let eps: f64 = args[3].parse().unwrap();
            let kappa: f64 = args[4].parse().unwrap();
            let s_fracs: Vec<f64> = args[5..].iter().map(|x| x.parse().unwrap()).collect();
            let case = make_case(case_name, seed + 7);
            let eps_scale = median_eps_u(&case.bodies, case.rho);
            let base = run(&case, Mode::Always, 0.0, eps, kappa, seed + 11);
            for &sf in &s_fracs {
                let s = sf * eps_scale;
                for mode in [Mode::Skin, Mode::Naive] {
                    let r = run(&case, mode, s, eps, kappa, seed + 11);
                    let (missed, false_e, tn) = compare(&base.events, &r.events, 1e-3);
                    report(case_name, mode, sf, eps, kappa, &r, missed, false_e, tn);
                }
            }
            report(case_name, Mode::Always, 0.0, eps, kappa, &base, 0, 0, base.events.len() as u64);
        }
        Some("truth") => {
            // Small case: always and skin against the independent dense truth, per segment.
            let case_name = &args[2];
            let eps: f64 = args[3].parse().unwrap();
            let kappa: f64 = args[4].parse().unwrap();
            let s_frac: f64 = args[5].parse().unwrap();
            let case = make_case(case_name, seed + 7);
            let eps_scale = median_eps_u(&case.bodies, case.rho);
            let s = s_frac * eps_scale;
            let segments = (case.orbits * TAU / SEG).round() as usize;
            let sched = schedule(case.bodies.len(), segments, kappa, eps, seed + 11);
            for mode in [Mode::Always, Mode::Skin] {
                let mut w = World::new(case.bodies.clone(), case.rho, s, mode, 4.0 * eps * (kappa + 1.0));
                // initial certs exactly as `run`
                {
                    let sorted = Sorted::new(&w.b, w.rho);
                    let pad = if mode == Mode::Always { 0.0 } else { s };
                    let mut setup_later = Vec::new();
                    for (k, &(u, i)) in sorted.order.iter().enumerate() {
                        let bi = w.b[i as usize];
                        let (lo, hi) = sorted.range(u, sorted.reach(&bi) + pad);
                        for &(_, j) in &sorted.order[lo.max(k + 1)..hi] {
                            let bj = &w.b[j as usize];
                            if cone_gap(&bi, bj) < eps_u(&bi, bj, w.rho) + pad {
                                setup_later.push((i, j));
                            }
                        }
                    }
                    for (i, j) in setup_later {
                        w.setup(i, j, 0.0);
                    }
                }
                let (mut tot_miss, mut tot_false, mut tot_truth, mut tot_ev) = (0u64, 0u64, 0u64, 0u64);
                for (sg, seg_kicks) in sched.iter().enumerate() {
                    let t_a = sg as f64 * SEG;
                    let t_b = t_a + SEG;
                    for &(i, frac) in seg_kicks {
                        w.kick(i, t_a, frac);
                    }
                    let sorted = Sorted::new(&w.b, w.rho);
                    match mode {
                        Mode::Always => {
                            let mut done = vec![false; w.b.len()];
                            for &(i, _) in seg_kicks {
                                if !done[i] {
                                    done[i] = true;
                                    w.scan(&sorted, i as u32, t_a);
                                }
                            }
                        }
                        _ => {
                            for &(i, _) in seg_kicks {
                                if w.dbin[i] - w.scan_anchor[i] >= s / 4.0 {
                                    w.scan_anchor[i] = w.dbin[i];
                                    w.scan(&sorted, i as u32, t_a);
                                }
                            }
                        }
                    }
                    let mut ev = Vec::new();
                    w.segment_pass(t_a, t_b, &mut ev);
                    let mut truth = Vec::new();
                    segment_truth(&w.b, &radial_pairs(&w.b, w.rho), w.rho, t_a, SEG, &mut truth);
                    // the truth sees events in [t_a + margin, t_b - margin] reliably
                    let ev_f: Vec<(usize, u32, u32, f64, f64)> =
                        ev.iter().filter(|e| e.2 > t_a + 0.05 && e.2 < t_b - 0.05).map(|e| (sg, e.0, e.1, e.2, e.3)).collect();
                    let truth_f: Vec<(usize, u32, u32, f64, f64)> =
                        truth.iter().filter(|e| e.2 > t_a + 0.05 && e.2 < t_b - 0.05).map(|e| (sg, e.0, e.1, e.2, e.3)).collect();
                    let (m, f, tn) = compare(&truth_f, &ev_f, 1e-3);
                    tot_miss += m;
                    tot_false += f;
                    tot_truth += tn;
                    tot_ev += ev_f.len() as u64;
                }
                println!(
                    "{{\"exp\":\"truth-check\",\"case\":\"{}\",\"mode\":\"{}\",\"s_frac\":{},\"eps\":{:e},\"kappa\":{},\"truth_events\":{},\"method_events\":{},\"missed\":{},\"false\":{}}}",
                    case_name,
                    mode.name(),
                    s_frac,
                    eps,
                    kappa,
                    tot_truth,
                    tot_ev,
                    tot_miss,
                    tot_false
                );
            }
        }
        Some("debug1") => {
            // Does the crate's pair_events over a 1-orbit window find what the dense truth finds?
            let case = make_case("ring", seed + 7);
            let b = &case.bodies;
            let pairs = radial_pairs(b, case.rho);
            for seg in 0..3usize {
                let t0 = seg as f64 * SEG;
                let t1 = t0 + SEG;
                let mut ev = Vec::new();
                let mut st = Stats::default();
                for &(i, j) in &pairs {
                    let mut v = Vec::new();
                    emergent_encounters::method::pair_events(&b[i as usize], &b[j as usize], case.rho, SAFETY, t0, t1, &mut st, &mut v);
                    for &(t, d) in &v {
                        if t > t0 + 0.05 && t < t1 - 0.05 {
                            ev.push((i, j, t, d));
                        }
                    }
                }
                let mut truth = Vec::new();
                segment_truth(b, &pairs, case.rho, t0, SEG, &mut truth);
                let truth_f: Vec<_> = truth.iter().filter(|e| e.2 > t0 + 0.05 && e.2 < t1 - 0.05).cloned().collect();
                let (m, f, tn) = compare(&truth_f.iter().map(|e| (seg, e.0, e.1, e.2, e.3)).collect::<Vec<_>>(), &ev.iter().map(|e| (seg, e.0, e.1, e.2, e.3)).collect::<Vec<_>>(), 1e-3);
                println!("{{\"exp\":\"debug1\",\"seg\":{},\"truth\":{},\"method\":{},\"missed\":{},\"false\":{}}}", seg, tn, ev.len(), m, f);
                if seg == 0 && m > 0 {
                    let mut shown = 0;
                    for &(i, j, t, _) in &truth_f {
                        if !ev.iter().any(|e| e.0 == i && e.1 == j && (e.2 - t).abs() < 1e-3) {
                            println!("  missed pair ({},{}) at t={} seg-local={}", i, j, t, t - t0);
                            let secs = sections_pad(&b[i as usize], &b[j as usize], case.rho, SAFETY, 0.0, &mut 0);
                            for sc in &secs {
                                println!("    kind={:?} theta={:.4} w1={} w2={} di=({:.4},{:.4}) dj=({:.4},{:.4}) pi={} pj={}", sc.kind, sc.theta, sc.w1, sc.w2, sc.di.0, sc.di.1, sc.dj.0, sc.dj.1, b[i as usize].period, b[j as usize].period);
                            }
                            let dist = {
                                let x = b[i as usize].state(t);
                                let y = b[j as usize].state(t);
                                let dx = x[0] - y[0];
                                let dy = x[1] - y[1];
                                (dx * dx + dy * dy).sqrt()
                            };
                            println!("    dist at t: {:.6} rho={}", dist, case.rho);
                            shown += 1;
                            if shown >= 3 { break; }
                        }
                    }
                }
            }
        }
        _ => {
            eprintln!("usage: skin debug1 | sweep ... | truth ...");
        }
    }
}
