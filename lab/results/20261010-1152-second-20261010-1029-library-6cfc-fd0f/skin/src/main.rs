//! Second author on 20261010-1029-library-6cfc (checker's named experiment for gold):
//! the metric-vs-phase-rank skin comparison on the engine's REAL encounter path, in
//! crates/encounters' own machinery (Body, Sorted U-scan, Binet cone, sections, pair_events).
//!
//! Workloads: `belt` (kick()'s regime) and the taleb-09b5 formation (`fleet`: 400 ships,
//! a half-width 1e-5, e~Rayleigh(0.001), apsides within +-0.1, lambda uniform + 3600 sea),
//! station-kept (lambda re-packed every orbit) with kick churn on fleet bodies.
//!
//! Skins:
//!   metric — the engine's implicit set today: the Binet-cone candidates from the sorted U-range
//!            scan (element-space neighbourhood; lambda-independent).
//!   phase  — the taleb-09b5 train certificate one layer down: k nearest in mean longitude,
//!            rebuilt on a sound schedule (interval = boundary gap / (2 * max relative rate
//!            over the WHOLE clump — non-members cannot cross uncounted).
//!
//! Accounting is end-to-end per kick: range scan, cone tests, section/window setup evals,
//! Diophantine query steps, exact checks, wall microseconds; plus rebuild events (setups)
//! and their pair work for the phase skin. One JSON object per line on stdout.
//!
//! Never edits the crates; path-depends on the public library only.

use emergent_encounters::belt::Rng;
use emergent_encounters::kepler::Body;
use emergent_encounters::method::{pair_events, run_section, Stats};
use emergent_encounters::pairs::{is_candidate, sections, Sorted};
use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::f64::consts::TAU;

/// The coordinate a phase skin ranks neighbours in.
#[derive(Clone, Copy, PartialEq)]
enum RankBy {
    MeanLam,
    TrueLam,
}

/// True longitude at time t (atan2 of the position; one Newton solve).
fn theta(b: &Body, t: f64) -> f64 {
    let st = b.state_at_mean(b.mean_anomaly(t));
    st[1].atan2(st[0])
}

/// Heap key: time ordered by bit pattern (finite, non-negative), then body id.
type TE = Reverse<(u64, u32)>;

#[inline]
fn te(t: f64, i: u32) -> TE {
    Reverse((t.to_bits(), i))
}

const RHO: f64 = 1e-4;
const SAFETY: f64 = 1.1;
/// Partners watched by the phase skin (taleb-09b5 measured distance-rank <= 4 at every
/// encounter, so k = 5 partners covers rank-4 partners; `truth` measures it under churn).
const K: usize = 5;

fn rayleigh(rng: &mut Rng, s: f64, cap: f64) -> f64 {
    let u = rng.f64();
    (s * (-2.0 * (1.0 - u).ln()).sqrt()).min(cap)
}

/// Mean longitude at time t (rad, not reduced).
fn lam(b: &Body, t: f64) -> f64 {
    b.mean_anomaly(t) + b.pom
}

fn ring_dist(a: f64, b: f64) -> f64 {
    let d = (a - b).rem_euclid(TAU);
    d.min(TAU - d)
}

fn pct(v: &mut [f64], f: f64) -> f64 {
    if v.is_empty() {
        return f64::NAN;
    }
    v.sort_by(|x, y| x.total_cmp(y));
    v[((v.len() as f64 - 1.0) * f) as usize]
}

/// Belt in kick()'s regime: a in [1.0, 1.5], e ~ Rayleigh(sigma_e), angles uniform.
fn make_belt(n: usize, sigma_e: f64, seed: u64) -> Vec<Body> {
    let mut rng = Rng(seed);
    (0..n)
        .map(|_| {
            let a = 1.0 + 0.5 * rng.f64();
            let e = rayleigh(&mut rng, sigma_e, 0.5);
            Body::new(a, e, TAU * rng.f64(), TAU * rng.f64())
        })
        .collect()
}

/// The taleb-09b5 formation: nc ships (a = 1 +- a_hw, e ~ Rayleigh(0.001) cap 0.01,
/// apsides within +-0.1 of one periapsis, lambda uniform or bunched at sig_lam) + sea.
/// Returns (bodies, nc) with the fleet first.
fn make_fleet(nc: usize, a_hw: f64, sig_lam: f64, n_sea: usize, seed: u64) -> (Vec<Body>, usize) {
    let mut rng = Rng(seed);
    let pom0 = TAU * rng.f64();
    let lam0 = TAU * rng.f64();
    let mut b = Vec::with_capacity(nc + n_sea);
    for _ in 0..nc {
        let a = 1.0 + (2.0 * rng.f64() - 1.0) * a_hw;
        let e = rayleigh(&mut rng, 0.001, 0.01);
        let pom = pom0 + (2.0 * rng.f64() - 1.0) * 0.1;
        let lam = if sig_lam <= 0.0 {
            TAU * rng.f64()
        } else {
            let (u1, u2) = (rng.f64(), rng.f64());
            let z = (-2.0 * (1e-12 + u1).ln()).sqrt() * (TAU * u2).cos();
            lam0 + sig_lam * z
        };
        b.push(Body::new(a, e, pom, lam));
    }
    for _ in 0..n_sea {
        let a = 0.9 + 0.2 * rng.f64();
        let e = rayleigh(&mut rng, 0.05, 0.5);
        b.push(Body::new(a, e, TAU * rng.f64(), TAU * rng.f64()));
    }
    (b, nc)
}

/// The schedule: kicks on fleet bodies at t_q, station-keeps (lambda re-pack) every orbit.
struct Sched {
    h_run: f64,
    nk: usize,
    nc: usize,
}

impl Sched {
    fn kick_time(&self, q: usize) -> f64 {
        (q as f64 + 0.5) * self.h_run / self.nk as f64
    }
    fn kicked(&self, q: usize) -> usize {
        (q * 97 + 13) % self.nc
    }
}

/// A kick in kick()'s exact form: a *= (1+eps) at time t, mean longitude preserved.
fn kick_body(old: &Body, eps: f64, t: f64) -> Body {
    let lam_k = old.mean_anomaly(t) + old.pom;
    let a_new = old.a * (1.0 + eps);
    let n_new = a_new.powf(-1.5);
    Body::new(a_new, old.e, old.pom, lam_k - n_new * t)
}

/// Station-keep: redraw lambda uniform on [0, TAU) (or the fleet's bunch), keep a, e, pom.
fn station_keep(b: &mut Body, rng: &mut Rng, sig_lam: f64, lam0: f64) {
    let lam = if sig_lam <= 0.0 {
        TAU * rng.f64()
    } else {
        let (u1, u2) = (rng.f64(), rng.f64());
        let z = (-2.0 * (1e-12 + u1).ln()).sqrt() * (TAU * u2).cos();
        lam0 + sig_lam * z
    };
    let m0 = (lam - b.pom).rem_euclid(TAU);
    let tpf = (-(m0 / TAU) * b.period as f64).rem_euclid(b.period as f64);
    let tp = (tpf.round() as u64) % b.period;
    b.tp = tp;
}

// ---------------------------------------------------------------------------
// The phase-rank skin (the train), sound rebuild schedule.
// ---------------------------------------------------------------------------

struct PhaseSkin {
    k: usize,
    by: RankBy,
    /// Per body: partners (ids), boundary slack (rad), build time, next rebuild time.
    sets: Vec<Vec<u32>>,
    slack: Vec<f64>,
    built_t: Vec<f64>,
    next_rb: Vec<f64>,
    pub rebuilds: u64,
    pub sel_ops: u64,
    pub pair_runs: u64,
    pub pair_runs_capped: u64,
    cap: u64,
}

impl PhaseSkin {
    fn new(n: usize, k: usize, cap: u64, by: RankBy) -> Self {
        PhaseSkin {
            k,
            by,
            sets: vec![Vec::new(); n],
            slack: vec![0.0; n],
            built_t: vec![0.0; n],
            next_rb: vec![f64::INFINITY; n],
            rebuilds: 0,
            sel_ops: 0,
            pair_runs: 0,
            pair_runs_capped: 0,
            cap,
        }
    }


    /// Select the k nearest in mean longitude at time t, extending past ties.
    ///
    /// Sound Verlet rule: any body among the k nearest at t' > t had distance at most
    /// d[k-1](t) + 2*dn_max*(t'-t) at build time (each distance changes at <= dn_max).
    /// So the set is valid while it contains every body within d[k-1] + allowance; we
    /// extend membership until the next body lies beyond d[k-1] + 2*dn_max*DELTA_TARGET
    /// (or the clump runs out), and the validity returned is (d[k'] - d[k-1])/(2*dn_max),
    /// which is >= DELTA_TARGET whenever we stopped because of the allowance. Extending
    /// past ties is what makes the rule terminate: a frozen near-tie grows the set
    /// instead of forcing a zero-interval rebuild loop.
    fn select_valid(b: &[Body], i: usize, t: f64, k: usize, dn: f64, by: RankBy) -> (Vec<u32>, f64) {
        const DELTA_TARGET: f64 = 1.0; // time units; ties rebuild at most this often
        let xi = if by == RankBy::MeanLam { lam(&b[i], t) } else { theta(&b[i], t) };
        let mut d: Vec<(f64, u32)> = (0..b.len())
            .filter(|&j| j != i)
            .map(|j| {
                let xj = if by == RankBy::MeanLam { lam(&b[j], t) } else { theta(&b[j], t) };
                (ring_dist(xi, xj), j as u32)
            })
            .collect();
        d.sort_by(|x, y| x.0.total_cmp(&y.0).then(x.1.cmp(&y.1)));
        if d.len() <= k {
            return (d.iter().map(|x| x.1).collect(), f64::INFINITY);
        }
        let base = d[k - 1].0;
        let allow = 2.0 * dn * DELTA_TARGET;
        let mut k2 = k;
        while k2 < d.len() && d[k2].0 < base + allow {
            k2 += 1;
        }
        let partners: Vec<u32> = d[..k2].iter().map(|x| x.1).collect();
        if k2 >= d.len() {
            return (partners, f64::INFINITY);
        }
        // the drift headroom (rad) to the first excluded body; the validity interval is
        // headroom / (2*dn) — stored as headroom so tighten() can rescale it on rate changes
        (partners, d[k2].0 - base)
    }

    /// k nearest, ignoring ties (used only for coverage/rank bookkeeping).
    fn select(b: &[Body], i: usize, t: f64, k: usize) -> (Vec<u32>, f64) {
        let li = lam(&b[i], t);
        let mut d: Vec<(f64, u32)> = (0..b.len())
            .filter(|&j| j != i)
            .map(|j| (ring_dist(li, lam(&b[j], t)), j as u32))
            .collect();
        d.sort_by(|x, y| x.0.total_cmp(&y.0).then(x.1.cmp(&y.1)));
        let partners: Vec<u32> = d.iter().take(k).map(|x| x.1).collect();
        let slack = if d.len() >= k + 1 { (d[k].0 - d[k - 1].0).max(0.0) } else { f64::INFINITY };
        (partners, slack)
    }

    /// Max |n_j - n_i| over the whole clump (non-members too: no uncounted crossings).
    fn dn_max(b: &[Body], i: usize) -> f64 {
        b.iter()
            .enumerate()
            .filter(|&(j, _)| j != i)
            .map(|(_, x)| (x.n - b[i].n).abs())
            .fold(0.0, f64::max)
    }

    fn build(&mut self, b: &[Body], i: usize, t: f64, st: Option<(&mut Stats, f64, f64)>) {
        // pairwise bound on the ranking coordinate's relative rate:
        // mean longitude: |n_i - n_j|; true longitude: w_i + w_j with w = n(1+e)/(1-e)^2.
        let dn = match self.by {
            RankBy::MeanLam => Self::dn_max(b, i),
            RankBy::TrueLam => 2.0 * b.iter().map(|x| x.n * (1.0 + x.e) / (1.0 - x.e).powi(2)).fold(0.0f64, f64::max),
        };
        let (partners, headroom) = Self::select_valid(b, i, t, self.k, if dn > 0.0 { dn } else { 1e-300 }, self.by);
        self.sel_ops += b.len() as u64;
        self.sets[i] = partners;
        self.slack[i] = headroom;
        self.built_t[i] = t;
        self.next_rb[i] = if headroom.is_finite() && dn > 0.0 { t + headroom / (2.0 * dn) } else { f64::INFINITY };
        if let Some((st, t0, t1)) = st {
            self.pair_runs += self.sets[i].len() as u64;
            if self.pair_runs <= self.cap {
                let mut out = Vec::new();
                for &j in &self.sets[i] {
                    pair_events(&b[i], &b[j as usize], RHO, SAFETY, t0, t1, st, &mut out);
                }
            } else {
                self.pair_runs_capped += self.sets[i].len() as u64;
            }
        }
    }

    /// After a kick changes rates, tighten every next_rb against the new global dn_max.
    fn tighten(&mut self, dn: f64) {
        for i in 0..self.sets.len() {
            let s = self.slack[i];
            if s.is_finite() && dn > 0.0 {
                let t = self.built_t[i] + s / (2.0 * dn.max(1e-300));
                if t < self.next_rb[i] {
                    self.next_rb[i] = t;
                }
            }
        }
    }

    /// Drain scheduled rebuilds with time < until. `work`: also re-certify partners.
    fn drain(&mut self, b: &[Body], until: f64, heap: &mut BinaryHeap<TE>, st: &mut Stats, h_cert: f64, work: bool) {
        while let Some(&Reverse((tb, i))) = heap.peek() {
            let t = f64::from_bits(tb);
            if t >= until {
                break;
            }
            heap.pop();
            if t < self.next_rb[i as usize] {
                continue; // stale entry
            }
            self.rebuilds += 1;
            let tt = t.max(0.0);
            self.build(b, i as usize, tt, if work { Some((st, tt, tt + h_cert)) } else { None });
            let nt = self.next_rb[i as usize];
            if nt.is_finite() {
                heap.push(te(nt, i as u32));
            }
        }
    }
}

// ---------------------------------------------------------------------------
// cost: per-kick end-to-end re-certification cost, both skins, both workloads.
// ---------------------------------------------------------------------------

fn run_metric(bodies: &[Body], sched: &Sched, eps: f64, h_cert: f64, sig_lam: f64, seed: u64) {
    let mut b = bodies.to_vec();
    let mut rng = Rng(seed ^ 0x5a5a);
    let mut st = Stats::default();
    let mut scanned = 0u64;
    let mut cone_tests = 0u64;
    let mut sets: Vec<f64> = Vec::new();
    let mut secs = 0.0f64;
    let nk = sched.nk;
    let mut sk_events = 0u64;
    for q in 0..nk {
        let tq = sched.kick_time(q);
        // station-keeps strictly before tq (metric set is element-based; they cost nothing)
        while (sk_events + 1) as f64 * TAU <= tq {
            sk_events += 1;
            for i in 0..sched.nc {
                station_keep(&mut b[i], &mut rng, sig_lam, 0.0);
            }
        }
        let i = sched.kicked(q);
        let new = kick_body(&b[i], eps, tq);
        b[i] = new;
        let sorted = Sorted::new(&b, RHO); // O(n log n); excluded (identical for both skins, amortizable)
        let t0 = std::time::Instant::now();
        let (lo, hi) = sorted.range(new.binet()[0], sorted.reach(&new));
        let mut out = Vec::new();
        let mut kset = 0u64;
        for &(_, j) in &sorted.order[lo..hi] {
            let ju = j as usize;
            if ju == i {
                continue;
            }
            scanned += 1;
            cone_tests += 1;
            if !is_candidate(&new, &b[ju], RHO) {
                continue;
            }
            kset += 1;
            pair_events(&new, &b[ju], RHO, SAFETY, tq, tq + h_cert, &mut st, &mut out);
        }
        secs += t0.elapsed().as_secs_f64();
        sets.push(kset as f64);
    }
    println!(
        "{{\"exp\":\"skin-cost\",\"skin\":\"metric\",\"eps\":{:.0e},\"kicks\":{},\"pairs_per_kick\":{:.1},\"set_p50\":{:.1},\"set_p99\":{:.1},\"set_max\":{:.0},\"scanned_per_kick\":{:.1},\"cone_tests_per_kick\":{:.1},\"evals_per_kick\":{:.0},\"qsteps_per_kick\":{:.1},\"checks_per_kick\":{:.1},\"hits\":{},\"us_per_kick\":{:.0},\"us_per_pair\":{:.2}}}",
        eps, nk,
        sets.iter().sum::<f64>() / nk as f64,
        pct(&mut sets.clone(), 0.5), pct(&mut sets.clone(), 0.99),
        sets.iter().cloned().fold(0.0, f64::max),
        scanned as f64 / nk as f64, cone_tests as f64 / nk as f64,
        st.evals as f64 / nk as f64, st.qsteps as f64 / nk as f64, st.checks_total() as f64 / nk as f64,
        st.hits_total(), secs * 1e6 / nk as f64, if st.pairs > 0 { secs * 1e6 / st.pairs as f64 } else { 0.0 },
    );
}

fn run_phase(bodies: &[Body], sched: &Sched, eps: f64, h_cert: f64, sig_lam: f64, lam0: f64, seed: u64, by: RankBy) {
    let n = bodies.len();
    let mut b = bodies.to_vec();
    let mut rng = Rng(seed ^ 0x5a5a);
    let mut st = Stats::default();
    let mut skin = PhaseSkin::new(n, K, 30_000, by);
    let mut heap = BinaryHeap::new();
    // initial build (t=0): everyone
    for i in 0..n {
        skin.build(&b, i, 0.0, Some((&mut st, 0.0, h_cert)));
        let nt = skin.next_rb[i];
        if nt.is_finite() {
            heap.push(te(nt, i as u32));
        }
    }
    let mut kick_secs = 0.0f64;
    let mut kick_pairs = 0u64;
    let mut kick_sets: Vec<f64> = Vec::new();
    let mut sk_events = 0u64;
    for q in 0..sched.nk {
        let tq = sched.kick_time(q);
        skin.drain(&b, tq, &mut heap, &mut st, h_cert, true);
        while (sk_events + 1) as f64 * TAU <= tq {
            sk_events += 1;
            let t = sk_events as f64 * TAU;
            for i in 0..sched.nc {
                station_keep(&mut b[i], &mut rng, sig_lam, lam0);
            }
            // a station-keep moves every lambda: rebuild every set
            for i in 0..n {
                skin.rebuilds += 1;
                skin.build(&b, i, t, Some((&mut st, t, t + h_cert)));
                let nt = skin.next_rb[i];
                if nt.is_finite() {
                    heap.push(te(nt, i as u32));
                }
            }
            skin.drain(&b, tq, &mut heap, &mut st, h_cert, true);
        }
        let i = sched.kicked(q);
        let new = kick_body(&b[i], eps, tq);
        b[i] = new;
        // kicked body: re-select + re-certify its k partners over the certificate horizon
        let t0 = std::time::Instant::now();
        skin.rebuilds += 1;
        skin.build(&b, i, tq, Some((&mut st, tq, tq + h_cert)));
        kick_secs += t0.elapsed().as_secs_f64();
        kick_pairs += skin.sets[i].len() as u64;
        kick_sets.push(skin.sets[i].len() as f64);
        heap.push(te(skin.next_rb[i], i as u32));
        // the kick changed one rate: tighten everyone against the new global rate bound
        let dn = if by == RankBy::MeanLam {
            (0..sched.nc).map(|j| (b[j].n - 1.0).abs()).fold(0.0, f64::max) * 2.0
        } else {
            2.0 * b.iter().map(|x| x.n * (1.0 + x.e) / (1.0 - x.e).powi(2)).fold(0.0f64, f64::max)
        };
        skin.tighten(dn);
        for j in 0..n {
            let nt = skin.next_rb[j];
            if nt.is_finite() {
                heap.push(te(nt, j as u32));
            }
        }
    }
    let orbits = sched.h_run / TAU;
    println!(
        "{{\"exp\":\"skin-cost\",\"skin\":\"phase\",\"rank_by\":\"{}\",\"eps\":{:.0e},\"kicks\":{},\"k\":{},\"pairs_per_kick\":{:.1},\"set_p50\":{:.1},\"scanned_per_kick\":{:.0},\"evals_per_kick\":{:.0},\"qsteps_per_kick\":{:.1},\"checks_per_kick\":{:.1},\"hits\":{},\"us_per_kick\":{:.0},\"us_per_pair\":{:.2},\"rebuilds_per_body_per_orbit\":{:.2},\"sel_ops_per_orbit\":{:.0},\"rebuild_pair_runs\":{},\"rebuild_pair_runs_capped\":{},\"pair_runs_total\":{}}}",
        if by == RankBy::MeanLam { "mean_lam" } else { "true_lam" }, eps, sched.nk, K,
        kick_pairs as f64 / sched.nk as f64,
        pct(&mut kick_sets.clone(), 0.5),
        0.0, // no U-range scan: selection is over the clump
        st.evals as f64 / sched.nk as f64, st.qsteps as f64 / sched.nk as f64, st.checks_total() as f64 / sched.nk as f64,
        st.hits_total(), kick_secs * 1e6 / sched.nk as f64,
        if st.pairs > 0 { kick_secs * 1e6 / kick_pairs as f64 } else { 0.0 },
        skin.rebuilds as f64 / n as f64 / orbits,
        skin.sel_ops as f64 / orbits,
        skin.pair_runs - skin.pair_runs_capped, skin.pair_runs_capped, skin.pair_runs,
    );
}

fn cost(which: &str) {
    let h_run = 20.0 * TAU;
    let h_cert = 20.0 * TAU;
    let epss = [1e-9, 1e-7, 1e-5, 1e-3];
    match which {
        "belt" => {
            let n = 4000;
            let b = make_belt(n, 0.01, 5);
            let sched = Sched { h_run, nk: 100, nc: n };
            for &eps in &epss {
                run_metric(&b, &sched, eps, h_cert, 0.0, 5);
            }
            // phase skin on the belt: analytic rebuild rate (event iteration would be ~1e9 events)
            let mut rates = Vec::new();
            let mut slacks = Vec::new();
            for i in 0..n {
                let (_, slack) = PhaseSkin::select(&b, i, 0.0, K);
                let dn = PhaseSkin::dn_max(&b, i);
                slacks.push(slack);
                rates.push(if slack.is_finite() && dn > 0.0 { 2.0 * dn / slack } else { 0.0 });
            }
            println!(
                "{{\"exp\":\"skin-cost\",\"skin\":\"phase-analytic\",\"workload\":\"belt\",\"n\":{},\"k\":{},\"rebuilds_per_body_per_orbit_mean\":{:.3e},\"rebuilds_per_body_per_orbit_p99\":{:.3e},\"slack_p50\":{:.3e}}}",
                n, K,
                rates.iter().sum::<f64>() / n as f64 * TAU,
                pct(&mut rates, 0.99) * TAU,
                pct(&mut slacks, 0.5),
            );
        }
        "fleet" => {
            let (b, nc) = make_fleet(400, 1e-5, 0.0, 3600, 11);
            let sched = Sched { h_run, nk: 100, nc };
            for &eps in &epss {
                run_metric(&b, &sched, eps, h_cert, 0.0, 11);
            }
            // the train owns the co-orbital clump only; the sea stays with the cone
            let clump: Vec<Body> = b[..nc].to_vec();
            for &eps in &epss {
                run_phase(&clump, &sched, eps, h_cert, 0.0, 0.0, 11, RankBy::MeanLam);
            }
        }
        "phalanx" => {
            // the concentrated regime where the encounters live: 200 ships, sigma_lam = 0.01
            let (b, nc) = make_fleet(200, 1e-5, 0.01, 0, 27);
            let sched = Sched { h_run, nk: 100, nc };
            for &eps in &epss {
                run_metric(&b, &sched, eps, h_cert, 0.01, 27);
            }
            for &eps in &epss {
                run_phase(&b, &sched, eps, h_cert, 0.01, 0.0, 27, RankBy::MeanLam);
            }
            for &eps in &epss {
                run_phase(&b, &sched, eps, h_cert, 0.01, 0.0, 27, RankBy::TrueLam);
            }
        }
        _ => eprintln!("cost belt|fleet|phalanx"),
    }
}

// ---------------------------------------------------------------------------
// truth: brute-force sub-rho encounters of a churned, station-kept fleet; partner
// distance-rank and longitude-rank at each encounter; phase-skin misses by replay.
// ---------------------------------------------------------------------------

/// Update the per-pair best (closest approach) with ranks and skin coverage computed
/// INLINE: elements and sets are those in force at time t of this step.
fn record_best(
    b: &[Body],
    skins: &[PhaseSkin],
    i: usize,
    j: usize,
    t: f64,
    d: f64,
    best: &mut std::collections::HashMap<(u32, u32), (f64, f64, u32, u32, u32, [bool; 6])>,
    rank_computes: &mut u64,
) {
    let key = (i as u32, j as u32);
    let improve = match best.get(&key) {
        Some(&(d0, ..)) => d < d0,
        None => true,
    };
    if !improve {
        return;
    }
    *rank_computes += 1;
    let nc = b.len();
    let li = lam(&b[i], t);
    let lj = lam(&b[j], t);
    let dl = ring_dist(li, lj);
    let si = b[i].state_at_mean(b[i].mean_anomaly(t));
    let pi = [si[0], si[1]];
    let mut dr = 0u32;
    for k2 in 0..nc {
        if k2 == i || k2 == j {
            continue;
        }
        let sk_ = b[k2].state_at_mean(b[k2].mean_anomaly(t));
        if ((sk_[0] - pi[0]).hypot(sk_[1] - pi[1])) < d {
            dr += 1;
        }
    }
    let mut lr = 0u32;
    for k2 in 0..nc {
        if k2 == i || k2 == j {
            continue;
        }
        if ring_dist(li, lam(&b[k2], t)) < dl {
            lr += 1;
        }
    }
    let ti = theta(&b[i], t);
    let tj = theta(&b[j], t);
    let dt_ = ring_dist(ti, tj);
    let mut tr = 0u32;
    for k2 in 0..nc {
        if k2 == i || k2 == j {
            continue;
        }
        if ring_dist(ti, theta(&b[k2], t)) < dt_ {
            tr += 1;
        }
    }
    let mut cov = [false; 6];
    for (s, skin) in skins.iter().enumerate() {
        cov[s] = skin.sets[i].contains(&(j as u32)) || skin.sets[j].contains(&(i as u32));
    }
    if std::env::var("SKIN_DEBUG").is_ok() && !cov[5] {
        eprintln!(
            "[miss t8] i={} j={} t={:.4} d={:.2e} set_i={} set_j={} built_i={:.3} next_rb_i={:.4} built_j={:.3} next_rb_j={:.4}",
            i, j, t, d, skins[5].sets[i].len(), skins[5].sets[j].len(),
            skins[5].built_t[i], skins[5].next_rb[i], skins[5].built_t[j], skins[5].next_rb[j],
        );
    }
    best.insert(key, (d, t, dr, lr, tr, cov));
}

fn truth(nc: usize, sig_lam: f64, eps: f64, seed: u64) {
    let (mut b, _) = make_fleet(nc, 1e-5, sig_lam, 0, seed);
    let (cs, sn) = (0..nc).fold((0.0f64, 0.0f64), |(a, c), i| {
        let l = lam(&b[i], 0.0);
        (a + l.cos(), c + l.sin())
    });
    let lam0 = sn.atan2(cs).rem_euclid(TAU); // the bunch's centre, for station-keeps
    let h_run = 3.0 * TAU;
    let nk = 30usize;
    let dt = 5e-5;
    let sched = Sched { h_run, nk, nc };
    let mut rng = Rng(99);
    let ks = [4usize, 5, 8];
    let mut skins: Vec<PhaseSkin> = (0..6)
        .map(|s| PhaseSkin::new(nc, ks[s % 3], u64::MAX, if s < 3 { RankBy::MeanLam } else { RankBy::TrueLam }))
        .collect();
    let mut heaps: Vec<BinaryHeap<TE>> = (0..6).map(|_| BinaryHeap::new()).collect();
    for s in 0..6 {
        for i in 0..nc {
            skins[s].build(&b, i, 0.0, None);
            let nt = skins[s].next_rb[i];
            if nt.is_finite() {
                heaps[s].push(te(nt, i as u32));
            }
        }
    }
    // events: kicks at t_q, station-keeps at m*TAU; brute force between events
    let mut evs: Vec<(f64, usize, u8)> = Vec::new(); // (t, body, 0=kick)
    let mut sks: Vec<f64> = Vec::new();
    for q in 0..nk {
        evs.push((sched.kick_time(q), sched.kicked(q), 0));
    }
    let mut m = 1;
    while m as f64 * TAU < h_run {
        sks.push(m as f64 * TAU);
        m += 1;
    }
    let mut all_events: Vec<(f64, u8, usize)> = evs.iter().map(|&(t, i, _)| (t, 0u8, i)).chain(sks.iter().map(|&t| (t, 1u8, 0usize))).collect();
    all_events.sort_by(|x, y| x.0.total_cmp(&y.0));
    let nb = 32768usize;
    let binsz = TAU / nb as f64; // ~1.9e-4 rad ~ 2 rho at r ~ 1
    let mut head = vec![-1i64; nb];
    let mut nxt = vec![-1i64; nc];
    let mut pos = vec![[0.0f64; 2]; nc];
    /// pair -> (d_min, t, dist_rank, mean-lam rank, true-lam rank, covered@mean k4/5/8,true k4/5/8).
    let mut best: std::collections::HashMap<(u32, u32), (f64, f64, u32, u32, u32, [bool; 6])> = std::collections::HashMap::new();
    let mut hits_raw = 0u64;
    let mut rank_computes = 0u64;
    let mut t = 0.0f64;
    let mut ei = 0usize;
    let t_start = std::time::Instant::now();
    loop {
        // next event time
        let t_ev = if ei < all_events.len() { all_events[ei].0 } else { h_run };
        let t_end = t_ev.min(h_run);
        while t < t_end {
            // one brute step
            let mut occupied: Vec<usize> = Vec::with_capacity(nc);
            for i in 0..nc {
                let mm = b[i].mean_anomaly(t);
                let st_ = b[i].state_at_mean(mm);
                pos[i] = [st_[0], st_[1]];
                let th = st_[1].atan2(st_[0]).rem_euclid(TAU);
                let bin = ((th / binsz) as usize).min(nb - 1);
                if head[bin] < 0 {
                    occupied.push(bin);
                }
                nxt[i] = head[bin];
                head[bin] = i as i64;
            }
            for &bin in &occupied {
                let nb2 = (bin + 1) % nb;
                let mut p = head[bin];
                while p >= 0 {
                    let mut q2 = nxt[p as usize];
                    while q2 >= 0 {
                        let (i, j) = (p as usize, q2 as usize);
                        let d = (pos[i][0] - pos[j][0]).hypot(pos[i][1] - pos[j][1]);
                        if d < RHO {
                            hits_raw += 1;
                            record_best(&b, &skins, i, j, t, d, &mut best, &mut rank_computes);
                        }
                        q2 = nxt[q2 as usize];
                    }
                    p = nxt[p as usize];
                }
                let mut p = head[bin];
                while p >= 0 {
                    let mut q2 = head[nb2];
                    while q2 >= 0 {
                        let (i, j) = (p as usize, q2 as usize);
                        let d = (pos[i][0] - pos[j][0]).hypot(pos[i][1] - pos[j][1]);
                        if d < RHO {
                            hits_raw += 1;
                            record_best(&b, &skins, i, j, t, d, &mut best, &mut rank_computes);
                        }
                        q2 = nxt[q2 as usize];
                    }
                    p = nxt[p as usize];
                }
            }
            for &bin in &occupied {
                head[bin] = -1;
            }
            t += dt;
        }
        // process the event at t_ev (if any)
        if ei >= all_events.len() || t_ev >= h_run {
            break;
        }
        let (tev, kind, arg) = all_events[ei];
        ei += 1;
        // drain skins to tev
        for s in 0..6 {
            let mut st_dummy = Stats::default();
            skins[s].drain(&b, tev, &mut heaps[s], &mut st_dummy, 0.0, false);
        }
        if kind == 0 {
            let i = arg;
            b[i] = kick_body(&b[i], eps, tev);
        } else {
            for i in 0..nc {
                station_keep(&mut b[i], &mut rng, sig_lam, lam0);
            }
        }
        // rebuild the touched sets (kick: one body; station-keep: all)
        let touched: Vec<usize> = if kind == 0 { vec![arg] } else { (0..nc).collect() };
        for s in 0..6 {
            for &i in &touched {
                skins[s].rebuilds += 1;
                skins[s].build(&b, i, tev, None);
                let nt = skins[s].next_rb[i];
                if nt.is_finite() {
                    heaps[s].push(te(nt, i as u32));
                }
            }
            let dn = if skins[s].by == RankBy::MeanLam {
                (0..nc).map(|j| (b[j].n - 1.0).abs()).fold(0.0, f64::max) * 2.0
            } else {
                2.0 * b.iter().map(|x| x.n * (1.0 + x.e) / (1.0 - x.e).powi(2)).fold(0.0f64, f64::max)
            };
            skins[s].tighten(dn);
            for j in 0..nc {
                let nt = skins[s].next_rb[j];
                if nt.is_finite() {
                    heaps[s].push(te(nt, j as u32));
                }
            }
        }
    }
    let brute_us = t_start.elapsed().as_micros();
    let mut dist_ranks = Vec::new();
    let mut lam_ranks = Vec::new();
    let mut miss = [0u64; 6];
    let mut miss_examples: Vec<(u32, u32, f64, String, f64)> = Vec::new();
    let mut keys: Vec<_> = best.keys().copied().collect();
    keys.sort_unstable();
    let mut theta_ranks = Vec::new();
    for &(i, j) in &keys {
        let (_, _, dr, lr, tr, cov) = best[&(i, j)];
        dist_ranks.push(dr as f64);
        lam_ranks.push(lr as f64);
        theta_ranks.push(tr as f64);
        for (s, c) in cov.iter().enumerate() {
            if !c {
                miss[s] += 1;
                if miss_examples.len() < 20 {
                    let name = if s < 3 { format!("m{}", [4usize, 5, 8][s]) } else { format!("t{}", [4usize, 5, 8][s - 3]) };
                    miss_examples.push((i, j, best[&(i, j)].1, name, best[&(i, j)].0));
                }
            }
        }
    }
    println!(
        "{{\"exp\":\"skin-truth\",\"nc\":{},\"sig_lam\":{},\"eps_churn\":{:.0e},\"orbits\":{:.0},\"dt\":{:.0e},\"seed\":{},\"brute_us\":{},\"raw_hits\":{},\"encounters\":{},\"dist_rank_max\":{:.0},\"dist_rank_p99\":{:.1},\"lam_rank_max\":{:.0},\"lam_rank_p99\":{:.1},\"theta_rank_max\":{:.0},\"theta_rank_p99\":{:.1},\"misses_mean_k4\":{},\"misses_mean_k5\":{},\"misses_mean_k8\":{},\"misses_true_k4\":{},\"misses_true_k5\":{},\"misses_true_k8\":{},\"rank_computes\":{},\"miss_examples\":{}}}",
        nc, sig_lam, eps, h_run / TAU, dt, seed, brute_us, hits_raw, best.len(),
        dist_ranks.iter().cloned().fold(0.0, f64::max), pct(&mut dist_ranks, 0.99),
        lam_ranks.iter().cloned().fold(0.0, f64::max), pct(&mut lam_ranks, 0.99),
        theta_ranks.iter().cloned().fold(0.0, f64::max), pct(&mut theta_ranks, 0.99),
        miss[0], miss[1], miss[2], miss[3], miss[4], miss[5], rank_computes,
        miss_examples
            .iter()
            .map(|&(i, j, tt, ref k, d)| format!("{{\"i\":{},\"j\":{},\"t\":{:.3},\"k\":{},\"d\":{:.2e}}}", i, j, tt, k, d))
            .collect::<Vec<_>>()
            .join(","),
    );
}

/// Belt control: phase-rank of belt-encounter partners (coverage of a longitude skin there).
fn truth_belt() {
    let n = 4000;
    let b = make_belt(n, 0.01, 5);
    let sample: Vec<usize> = (0..n).step_by(n / 150).collect();
    let mut st = Stats::default();
    let mut encs = 0u64;
    let mut ranks = Vec::new();
    let h = 20.0 * TAU;
    let t0 = std::time::Instant::now();
    for &i in &sample {
        let sorted = Sorted::new(&b, RHO);
        let bi = &b[i];
        let (lo, hi) = sorted.range(bi.binet()[0], sorted.reach(bi));
        let mut out = Vec::new();
        for &(_, j) in &sorted.order[lo..hi] {
            let ju = j as usize;
            if ju == i || !is_candidate(bi, &b[ju], RHO) {
                continue;
            }
            out.clear();
            pair_events(bi, &b[ju], RHO, SAFETY, 0.0, h, &mut st, &mut out);
            for &(tt, _d) in &out {
                encs += 1;
                let li = lam(bi, tt);
                let dl = ring_dist(li, lam(&b[ju], tt));
                let r = (0..n)
                    .filter(|&k2| k2 != i && k2 != ju)
                    .filter(|&k2| ring_dist(li, lam(&b[k2], tt)) < dl)
                    .count();
                ranks.push(r as f64);
            }
        }
    }
    let secs = t0.elapsed().as_secs_f64();
    println!(
        "{{\"exp\":\"skin-truth-belt\",\"n\":{},\"sampled\":{},\"encounters\":{},\"lam_rank_max\":{:.0},\"lam_rank_p99\":{:.1},\"lam_rank_p50\":{:.0},\"secs\":{:.1}}}",
        n, sample.len(), encs,
        ranks.iter().cloned().fold(0.0, f64::max), pct(&mut ranks, 0.99), pct(&mut ranks, 0.5), secs,
    );
}

// ---------------------------------------------------------------------------
// slack: does the slack-skin lever (components-4643's 12.6x) survive concentration?
// kick()-style budget bisection on belt pairs vs fleet pairs vs phase partners.
// ---------------------------------------------------------------------------

fn budget_of(bi: &Body, bj: &Body, horizon: f64) -> (u64, f64) {
    let mut out = Vec::new();
    let mut st = Stats::default();
    pair_events(bi, bj, RHO, SAFETY, 10.0 * TAU, 10.0 * TAU + horizon, &mut st, &mut out);
    let proposals = st.checks_total();
    if proposals > 0 {
        return (proposals, 0.0);
    }
    let mut budget = f64::INFINITY;
    for sec in sections(bi, bj, RHO, SAFETY, &mut 0) {
        let (mut lo_g, mut hi_g) = (0i64, (bi.period as i64) / 4);
        for _ in 0..40 {
            let mid = (lo_g + hi_g) / 2;
            let mut s2 = sec.clone();
            s2.w1 += mid;
            s2.w2 += mid;
            let mut st3 = Stats::default();
            let mut scratch = Vec::new();
            run_section(bi, bj, &s2, RHO, 10.0 * TAU, 10.0 * TAU + horizon, &mut st3, &mut scratch);
            if st3.checks_total() > 0 {
                hi_g = mid;
            } else {
                lo_g = mid;
            }
        }
        budget = budget.min(lo_g as f64 / (horizon * 4_294_967_296.0));
    }
    (proposals, budget)
}

fn slack(which: &str) {
    let horizon = 100.0 * TAU;
    let epss = [1e-9, 1e-7, 1e-5, 1e-3];
    match which {
        "belt" => {
            let b = make_belt(4000, 0.01, 5);
            let sorted = Sorted::new(&b, RHO);
            let sampled: Vec<(usize, u32)> = {
                let mut v = Vec::new();
                'outer: for i in 0..b.len() {
                    let bi = &b[i];
                    let (lo, hi) = sorted.range(bi.binet()[0], sorted.reach(bi));
                    for &(_, j) in &sorted.order[lo..hi] {
                        let ju = j as usize;
                        if ju != i && is_candidate(bi, &b[ju], RHO) {
                            v.push((i, j));
                            if v.len() >= 200 {
                                break 'outer;
                            }
                        }
                    }
                }
                v
            };
            report_slack("belt", "metric", &b, &sampled, horizon, &epss);
        }
        "fleet" => {
            let (b, nc) = make_fleet(400, 1e-5, 0.0, 3600, 11);
            // kicked bodies' metric sets: fleet-fleet and fleet-sea strata
            let sched = Sched { h_run: 20.0 * TAU, nk: 10, nc };
            let mut ff: Vec<(usize, u32)> = Vec::new();
            let mut fx: Vec<(usize, u32)> = Vec::new();
            let sorted = Sorted::new(&b, RHO);
            for q in 0..sched.nk {
                let i = sched.kicked(q);
                let bi = &b[i];
                let (lo, hi) = sorted.range(bi.binet()[0], sorted.reach(bi));
                for &(_, j) in &sorted.order[lo..hi] {
                    let ju = j as usize;
                    if ju == i || !is_candidate(bi, &b[ju], RHO) {
                        continue;
                    }
                    if ju < nc {
                        if ff.len() < 100 {
                            ff.push((i, j));
                        }
                    } else if fx.len() < 100 {
                        fx.push((i, j));
                    }
                }
            }
            // phase partners of the same kicked bodies
            let ph: Vec<(usize, u32)> = (0..sched.nk)
                .flat_map(|q| {
                    let i = sched.kicked(q);
                    PhaseSkin::select(&b, i, 10.0 * TAU, K).0.into_iter().map(move |j| (i, j)).collect::<Vec<_>>()
                })
                .collect();
            report_slack("fleet", "metric-ff", &b, &ff, horizon, &epss);
            report_slack("fleet", "metric-fx", &b, &fx, horizon, &epss);
            report_slack("fleet", "phase-partners", &b, &ph, horizon, &epss);
        }
        _ => eprintln!("slack belt|fleet"),
    }
}

fn report_slack(workload: &str, class: &str, b: &[Body], pairs: &[(usize, u32)], horizon: f64, epss: &[f64]) {
    let mut budgets = Vec::new();
    let mut silent = 0u64;
    let t0 = std::time::Instant::now();
    for &(i, j) in pairs {
        let (p, bud) = budget_of(&b[i], &b[j as usize], horizon);
        if p == 0 {
            silent += 1;
        }
        budgets.push(bud);
    }
    let secs = t0.elapsed().as_secs_f64();
    let finite: Vec<f64> = budgets.iter().filter(|x| x.is_finite() && **x > 0.0).copied().collect();
    let sk: Vec<String> = epss
        .iter()
        .map(|&e| {
            let rel_dt = e;
            let n = budgets.iter().filter(|x| **x > rel_dt * 1.5).count();
            format!("{:.1e}:{}", rel_dt, n)
        })
        .collect();
    println!(
        "{{\"exp\":\"skin-slack\",\"workload\":\"{}\",\"class\":\"{}\",\"pairs\":{},\"horizon_orbits\":{:.0},\"silent_frac\":{:.3},\"budget_median\":{:.3e},\"budget_p10\":{:.3e},\"skippable\":{},\"secs\":{:.1}}}",
        workload, class, pairs.len(), horizon / TAU,
        silent as f64 / pairs.len().max(1) as f64,
        pct(&mut finite.clone(), 0.5), pct(&mut finite.clone(), 0.1),
        sk.join(","), secs,
    );
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    match args.get(1).map(|x| x.as_str()) {
        Some("cost") => cost(args.get(2).map(|x| x.as_str()).unwrap_or("fleet")),
        Some("truth") => match args.get(2).map(|x| x.as_str()).unwrap_or("") {
            "uniform-low" => truth(200, 0.0, 1e-5, 27),
            "uniform-high" => truth(200, 0.0, 1e-3, 27),
            "phalanx-low" => truth(200, 0.01, 1e-5, 27),
            "phalanx-high" => truth(200, 0.01, 1e-3, 27),
            "belt" => truth_belt(),
            _ => eprintln!("truth uniform-low|uniform-high|phalanx-low|phalanx-high|belt"),
        },
        Some("slack") => slack(args.get(2).map(|x| x.as_str()).unwrap_or("fleet")),
        Some("smoke") => {
            let (b, nc) = make_fleet(60, 1e-5, 0.0, 100, 3);
            let sched = Sched { h_run: 2.0 * TAU, nk: 5, nc };
            run_metric(&b, &sched, 1e-7, 2.0 * TAU, 0.0, 3);
            let clump: Vec<Body> = b[..nc].to_vec();
            run_phase(&clump, &sched, 1e-7, 2.0 * TAU, 0.0, 0.0, 3, RankBy::MeanLam);
        }
        _ => eprintln!("skin-probe cost|truth|slack|smoke"),
    }
}
