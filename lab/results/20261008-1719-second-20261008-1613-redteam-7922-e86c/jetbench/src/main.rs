//! Second-author experiment (run 20261008-1719): the re-anchor horizon of the
//! cycle-derivative jet on the SHIPPED integer law (`space-darwin16-v1`,
//! `crates/space` `Orbit::compile`), across the e-tail, with the belt's kick
//! channels, on belt scenes that exist in the tree, plus the author's proposed
//! criterion with its planted negative control.
//!
//! Exact record: the cycle is recompiled from `OrbitKey::bound(p, e)` at every
//! kick step and the periods (integer `Scalar`s) summed in f64 (63-bit
//! significands; float noise ~1e-16/orbit is 10 orders under the 1e-6 floor).
//! Jet: the anchor cycle's period plus its stored first derivative — obtained
//! as a central finite difference of compiled integer periods (the memo's
//! d/de of dt, not yet implemented in the crate).
//!
//! Channels (kick = absolute step in g = 1-e^2 of EPS per orbit):
//!   corrE  secular energy kicks at fixed semi-latus rectum p (fixed L)
//!   randE  random-sign residual kicks at fixed p (the H0190 residual mode)
//!   corrL  the secular tide: e pumped at fixed a (E conserved; Kepler-blind)
#![allow(clippy::needless_range_loop)]

use emergent_space::orbit::{Orbit, OrbitKey};
use emergent_space::scaled::Scalar;
use std::f64::consts::PI;

const EPS: f64 = 1e-7; // kick size per orbit in g = 1-e^2 units (first run's tide scale)
const FLOOR: f64 = 1e-6; // law.md's per-cycle floor
const NMAX: usize = 30_000;
const P0: f64 = 2304.0; // mid-band semi-latus rectum of the frozen belt (M units)
const A0: f64 = 2304.0; // semi-major axis for the tide channel

fn to_f64(s: Scalar) -> f64 {
    s.significand() as f64 * 2f64.powi(s.exponent() as i32 - 62)
}

fn e_q48(e: f64) -> u64 {
    debug_assert!((0.0..1.0).contains(&e));
    (e.min(0.999_999_999) * (1u64 << 48) as f64) as u64
}

/// Period and knot count of the shipped compiled cycle at (p, e).
fn cycle(p: f64, e: f64) -> (f64, usize) {
    // 30 fraction bits: quantum 2^-30 in M units, 13 orders under the floor;
    // rounded, not truncated, so no bias.
    let p_s = Scalar::raw((p * (1i128 << 30) as f64).round() as i128, -30).unwrap();
    let key = OrbitKey::bound(p_s, e_q48(e)).unwrap();
    let o = Orbit::compile(key).unwrap();
    (to_f64(o.period().unwrap()), o.shape().knots().len())
}

/// Kepler control: T = 2*pi*a^{3/2}, a = p/(1-e^2).
fn kepler_t(p: f64, e: f64) -> f64 {
    2.0 * PI * (p / (1.0 - e * e)).powf(1.5)
}

struct Path {
    /// true: fixed a (tide channel); false: fixed p (energy channel)
    fixed_a: bool,
    fixed: f64,
    e0: f64,
}

impl Path {
    fn g(e: f64) -> f64 {
        1.0 - e * e
    }
    /// compile input (p, e) for eccentricity e on this path
    fn at(&self, e: f64) -> (f64, f64) {
        if self.fixed_a {
            (self.fixed * Self::g(e), e) // p = a(1-e^2)
        } else {
            (self.fixed, e)
        }
    }
    fn period(&self, e: f64) -> f64 {
        cycle(self.at(e).0, self.at(e).1).0
    }
}

struct Anchors {
    t0: f64,
    dtdg: f64,
    d2tdg2: f64,
}

/// The stored derivatives at e0, from compiled integer periods (central FD).
fn anchors(path: &Path, e0: f64) -> Anchors {
    let g0 = Path::g(e0);
    let h = (1e-3 * g0).min(0.45 * (1.0 - g0));
    let t0 = path.period(e0);
    let e_plus = ((1.0 - (g0 + h)).max(0.0)).sqrt();
    let e_minus = ((1.0 - (g0 - h).clamp(1e-12, 1.999)).max(0.0)).sqrt();
    let tp = path.period(e_plus);
    let tm = path.period(e_minus);
    Anchors {
        t0,
        dtdg: (tp - tm) / (2.0 * h),
        d2tdg2: (tp - 2.0 * t0 + tm) / (h * h),
    }
}

struct Rng(u64);
impl Rng {
    fn b(&mut self) -> bool {
        self.mix() & 1 == 1
    }
    fn f(&mut self) -> f64 {
        self.mix() as f64 / u64::MAX as f64
    }
    fn mix(&mut self) -> u64 {
        self.0 ^= self.0 << 13;
        self.0 ^= self.0 >> 7;
        self.0 ^= self.0 << 17;
        self.0
    }
}

/// Horizon: kicks survived before |t_jet - t_exact|/T crosses FLOOR.
/// mode 0 = correlated, 1 = random-sign.
fn horizon(path: &Path, eps: f64, mode: u8, seed: u64, nmax: usize) -> Option<usize> {
    let a = anchors(path, path.e0);
    let g0 = Path::g(path.e0);
    let mut rng = Rng(seed);
    let mut g = g0;
    let (mut t_exact, mut sum_off) = (0.0, 0.0);
    for k in 1..=nmax {
        let dg = if mode == 0 { -eps } else if rng.b() { eps } else { -eps };
        g = (g + dg).max(1e-9).min(1.0);
        let tn = path.period((1.0 - g).sqrt());
        t_exact += tn;
        sum_off += g - g0;
        let t_jet = k as f64 * a.t0 + a.dtdg * sum_off;
        if (t_jet - t_exact).abs() / tn > FLOOR {
            return Some(k);
        }
    }
    None
}

/// Trigger run (correlated kicks): mode 0 = global interval K, 1 = per-cycle
/// (re-anchor when the curvature error bound 0.5*|T''|*sum((g-ga)^2) crosses
/// floor/2). Returns (max relative error, recompiles, kicks).
fn trigger_run(path: &Path, mode: u8, k_global: usize, n_run: usize) -> (f64, usize, usize) {
    let mut a = anchors(path, path.e0);
    let g0 = Path::g(path.e0);
    let mut g = g0;
    let mut ga = g0;
    let (mut t_exact, mut t_jet, mut sum_sq) = (0.0, 0.0, 0.0);
    let (mut max_err, mut recompiles) = (0.0f64, 0usize);
    for k in 1..=n_run {
        g = (g - EPS).max(1e-9);
        let e = (1.0 - g).sqrt();
        let tn = path.period(e);
        t_exact += tn;
        t_jet += a.t0 + a.dtdg * (g - ga);
        sum_sq += (g - ga) * (g - ga);
        max_err = max_err.max((t_jet - t_exact).abs() / tn);
        let trip = if mode == 0 {
            k % k_global == 0
        } else {
            0.5 * a.d2tdg2.abs() * sum_sq / a.t0 > FLOOR / 2.0
        };
        if trip {
            // Re-anchor: recompile exactly at the current state; epochs re-sync.
            recompiles += 1;
            a = anchors(path, e);
            ga = g;
            t_jet = t_exact;
            sum_sq = 0.0;
        }
    }
    (max_err, recompiles, n_run)
}

fn fmt_n(n: Option<usize>) -> String {
    match n {
        Some(k) => format!("{k}"),
        None => format!(">cap"),
    }
}

fn main() {
    let t_start = std::time::Instant::now();
    let es: Vec<f64> = vec![0.001, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 0.995];
    let mut m = String::new();

    // ---------- E1: horizons on the shipped integer cycles ----------
    println!("== E1: re-anchor horizon on the shipped integer cycles (law {})", emergent_space::LAW_ID);
    println!("kick = {EPS:.0e} per orbit in g=1-e^2; floor {FLOOR:.0e}; p/a = {P0}");
    let (t_int, kn) = cycle(P0, 0.5);
    let t_k = kepler_t(P0, 0.5);
    println!("cross-check T(p=2304,e=0.5): integer {:.6} vs Kepler {:.6} (rel {:.2e}); knots {kn}", t_int, t_k, (t_int - t_k).abs() / t_k);
    m += &format!("{{\"law\":\"{}\",\"eps\":{EPS},\"floor\":{FLOOR},\"p0\":{P0},\"nmax\":{NMAX},\"T_check_rel\":{:.3e},\"e1_rows\":[", emergent_space::LAW_ID, (t_int - t_k).abs() / t_k);

    println!("{:>6} {:>8} {:>8} {:>8} {:>7} {:>8}", "e", "n*_corrE", "n*_randE", "n*_corrL", "knots", "b9form");
    let mut first = true;
    for &e in &es {
        let pe = Path { fixed_a: false, fixed: P0, e0: e };
        let pa = Path { fixed_a: true, fixed: A0, e0: e };
        let nc = horizon(&pe, EPS, 0, 7922, NMAX);
        let nr = if e < 0.05 { None } else { horizon(&pe, EPS, 1, 7922, NMAX) };
        let nl = horizon(&pa, EPS, 0, 7922, 300 * NMAX);
        let b9 = 32.0 * ((1.0 + e) / (1.0 - e)).log2() + 8.0;
        let knots_measured = cycle(P0, e).1;
        println!("{e:>6} {:>8} {:>8} {:>8} {:>7} {:>8.1}", fmt_n(nc), fmt_n(nr), fmt_n(nl), knots_measured, b9);
        m += &format!("{}{{\"e\":{e},\"n_corrE\":{},\"n_randE\":{},\"n_corrL\":{},\"knots\":{}}}", if first { "" } else { "," }, opt_j(nc), opt_j(nr), opt_j(nl), knots_measured);
        first = false;
    }
    m += "]";

    // scaling checks on the integer law (recompute to keep the record self-contained)
    let h_of = |e: f64| horizon(&Path { fixed_a: false, fixed: P0, e0: e }, EPS, 0, 7922, NMAX).unwrap_or(NMAX);
    let (n5, n50, n0, n6) = (h_of(0.99), h_of(0.5), h_of(0.001), h_of(0.6));
    let (r1, r2) = (n5 as f64 / n50 as f64, n0 as f64 / n50 as f64);
    println!("scaling: n*(0.99)/n*(0.5) = {r1:.3} vs (1-e^2)^(2/3) = {:.3}; n*(0+)/n*(0.5) = {r2:.3} vs (1/0.75)^(2/3) = {:.3}",
        ((1.0 - 0.99f64 * 0.99) / 0.75f64).powf(2.0 / 3.0), (1.0f64 / 0.75f64).powf(2.0 / 3.0));
    m += &format!(",\"ratio_99_50\":{r1:.4},\"ratio_0_50\":{r2:.4}");

    // ---------- E1b: kick-size sweep (scale invariance on the integer law) ----------
    println!("\n== E1b: kick-size sweep (horizon ~ eps^(-2/3))");
    m += ",\"e1b_sweep\":[";
    let mut first = true;
    for &(e, eps) in &[(0.5f64, 1e-5f64), (0.5, 1e-8), (0.99, 1e-5), (0.99, 1e-8)] {
        let pe = Path { fixed_a: false, fixed: P0, e0: e };
        let n = horizon(&pe, eps, 0, 7922, 3_000_000);
        let base = h_of(e) as f64;
        let ratio = n.map(|x| x as f64 / base).unwrap_or(f64::NAN);
        println!("e={e}: eps={eps:.0e} n*={} ratio vs eps=1e-7: {:.4} (predicted {:.4})", fmt_n(n), ratio, (eps / 1e-7).powf(-2.0 / 3.0));
        m += &format!("{}{{\"e\":{e},\"eps\":{eps},\"n\":{}}}", if first { "" } else { "," }, opt_j(n));
        first = false;
    }
    m += "]";

    // ---------- E3: the criterion and its negative control ----------
    println!("\n== E3: re-anchor triggers (the author's proposed criterion)");
    let k_global = n6 / 2; // calibrated on the frozen scene (all e <= 0.6)
    println!("global trigger: K = n*(0.6)/2 = {k_global} kicks between re-anchors (frozen scene e<=0.6)");
    println!("{:>6} {:>28} {:>28}", "e", "global maxerr/floor (rate)", "per-cycle maxerr/floor (rate)");
    m += &format!(",\"k_global\":{k_global},\"e3_triggers\":[");
    let mut first = true;
    for &e in &[0.5f64, 0.9, 0.95, 0.99, 0.995] {
        let pe = Path { fixed_a: false, fixed: P0, e0: e };
        let n_run = 20 * k_global;
        let g = trigger_run(&pe, 0, k_global, n_run);
        let pc = trigger_run(&pe, 1, k_global, n_run);
        println!("{e:>6} {:>13.1}x ({:.5}/k) {:>13.1}x ({:.5}/k)",
            g.0 / FLOOR, g.1 as f64 / g.2 as f64, pc.0 / FLOOR, pc.1 as f64 / pc.2 as f64);
        m += &format!("{}{{\"e\":{e},\"global\":{{\"max_err\":{:.3e},\"rate\":{:.5}}},\"per_cycle\":{{\"max_err\":{:.3e},\"rate\":{:.5}}}}}",
            if first { "" } else { "," }, g.0, g.1 as f64 / g.2 as f64, pc.0, pc.1 as f64 / pc.2 as f64);
        first = false;
    }
    m += "]";

    // ---------- E2: belt scenes that exist in the tree ----------
    println!("\n== E2: belt scenes (0.285 kicks/orbit, H0190 K2; compiles/kick = 1/n*(e); crossings = measured knots)");
    // knots(e): measured on a subgrid, linear in ln((1+e)/(1-e)) (r_a/r_p at fixed p)
    let sub: Vec<f64> = (0..=39).map(|i| i as f64 * 0.025).chain([0.999, 0.9995]).collect();
    let ks: Vec<(f64, f64)> = sub.iter().map(|&e| (((1.0 + e) / (1.0 - e)).ln(), cycle(P0, e).1 as f64)).collect();
    let ns = ks.len() as f64;
    let sx: f64 = ks.iter().map(|r| r.0).sum();
    let sy: f64 = ks.iter().map(|r| r.1).sum();
    let sxx: f64 = ks.iter().map(|r| r.0 * r.0).sum();
    let sxy: f64 = ks.iter().map(|r| r.0 * r.1).sum();
    let slope = (ns * sxy - sx * sy) / (ns * sxx - sx * sx);
    let icept = (sy - slope * sx) / ns;
    let max_resid = ks.iter().map(|r| (slope * r.0 + icept - r.1).abs()).fold(0.0f64, f64::max);
    let knots_at = |e: f64| -> f64 { slope * ((1.0 + e) / (1.0 - e)).ln() + icept };
    println!("knots fit: {slope:.2}*ln((1+e)/(1-e)) + {icept:.1}, max resid {max_resid:.2} (B9: 46.17*ln + 8)");
    m += &format!(",\"knots_slope\":{slope:.4},\"knots_icept\":{icept:.3},\"knots_max_resid\":{max_resid:.3}");

    // n*(e) tables, precomputed once per channel: log-linear in ln g = ln(1-e^2)
    let table = |rand: bool| -> Vec<(f64, f64)> {
        let mut pts: Vec<(f64, f64)> = es.iter().filter(|&&x| !rand || x >= 0.3).filter_map(|&x| {
            let pe = Path { fixed_a: false, fixed: P0, e0: x };
            let n = horizon(&pe, EPS, u8::from(rand), 7922, NMAX)?;
            Some(((1.0 - x * x).ln(), n as f64))
        }).collect();
        pts.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());
        pts
    };
    let interp = |e: f64, pts: &[(f64, f64)]| -> f64 {
        let x = (1.0 - e * e).ln();
        if x <= pts[0].0 {
            return pts[0].1;
        }
        if x >= pts[pts.len() - 1].0 {
            return pts[pts.len() - 1].1;
        }
        for w in pts.windows(2) {
            if x >= w[0].0 && x <= w[1].0 {
                let t = (x - w[0].0) / (w[1].0 - w[0].0);
                return 10f64.powf(w[0].1.log10() * (1.0 - t) + w[1].1.log10() * t);
            }
        }
        unreachable!()
    };
    let (tab_c, tab_r) = (table(false), table(true));

    let scenes: [(&str, f64, f64); 3] = [
        ("b18b (frozen: sigma 0.07, cap 0.6)", 0.07, 0.6),
        ("encounters (sigma 0.03, cap 0.5)", 0.03, 0.5),
        ("hot tail (sigma 0.3, cap 0.995)", 0.3, 0.995),
    ];
    m += ",\"e2_scenes\":[";
    let mut first = true;
    for (name, sig, cap) in scenes {
        for rand in [false, true] {
            let mut rng = Rng(1719);
            let n_draw = 1usize << 20;
            let mut costs = Vec::with_capacity(n_draw);
            let (mut tail_cost, mut total, mut n_tail) = (0.0f64, 0.0f64, 0usize);
            for _ in 0..n_draw {
                let v = rng.f().clamp(1e-17, 1.0);
                let e = (sig * (-2.0 * v.ln()).sqrt()).min(cap);
                let cost = 0.285 / interp(e, if rand { &tab_r } else { &tab_c }) * knots_at(e);
                if e > 0.9 {
                    tail_cost += cost;
                    n_tail += 1;
                }
                total += cost;
                costs.push(cost);
            }
            costs.sort_by(|a, b| a.partial_cmp(b).unwrap());
            let med = costs[n_draw / 2];
            let q = |f: f64| costs[((f * n_draw as f64) as usize).min(n_draw - 1)];
            let hot99 = 0.285 / interp(0.99, if rand { &tab_r } else { &tab_c }) * knots_at(0.99);
            println!("{name:<35} {:<6}: median {:.5}, p99 {:5.1}x, p99.9 {:5.1}x, share(e>0.9) {:5.1}% ({:.4}% bodies), e=0.99 body {:4.0}x",
                if rand { "randE" } else { "corrE" }, med, q(0.99) / med, q(0.999) / med, 100.0 * tail_cost / total, 100.0 * n_tail as f64 / n_draw as f64, hot99 / med);
            if !rand {
                m += &format!("{}{{\"scene\":\"{name}\",\"sigma\":{sig},\"cap\":{cap},\"median\":{med:.6},\"p99_x\":{:.3},\"p999_x\":{:.3},\"share_e_gt_09\":{:.5},\"e99_x\":{:.1}}}",
                    if first { "" } else { "," }, q(0.99) / med, q(0.999) / med, tail_cost / total, hot99 / med);
                first = false;
            }
        }
    }
    m += "]";

    let wall = t_start.elapsed().as_secs_f64();
    m += &format!(",\"wall_s\":{wall:.1}}}");
    std::fs::write("metrics2.json", m).unwrap();
    println!("\nwall {wall:.1} s");
}

fn opt_j(n: Option<usize>) -> String {
    match n {
        Some(k) => format!("{k}"),
        None => "null".into(),
    }
}

