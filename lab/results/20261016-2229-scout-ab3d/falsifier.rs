// The two-stage angular certificate for the player's in-belt scan, against the float twin of
// the shipped predicate. One file, no deps: rustc -O falsifier.rs -o falsifier && ./falsifier
//
// Scene: the shipped belt's own genesis (crates/universe/src/scenario.rs::ladder_ship):
//   a uniform in [2,3) AU, e Rayleigh(sigma 0.07) re-drawn above 0.4, omega uniform, phase
//   uniform, prograde in the star's doll. Ladder ship radius 34*2^8 root units, root unit
//   AU/101_300_000 = 1477 m -> r_ship = 12,850 km, near = 2^10*(r_a+r_b) = 0.176 AU (the
//   SHIPPED operating point); the ROCK point is 25-m rocks -> near = 3.42e-7 AU (the
//   encounters page's belt class).
// Predicate (crates/universe/src/encounter.rs::compute): min over tau in [0,h] of |d0+w*tau|
//   <= near, d0/w the exact relative position/velocity at t (the lattice law's linear form).
//   h = the player's binding step (the belt interval 28,141.5 s = 8.9164e-4 yr; also 1,000 s).
//
// Stage 1 (no anomaly solve): mean longitude lam(t) = om + m0 + n*t is exact and linear;
//   |theta_j - theta_q|(t) <= |lam_j - lam_q|(t) + margin_j + margin_q, margin = the body's
//   exact max|nu - M| over M (tabulated once per e, sound-loose at the bin's top e).
// Stage 2: solve the anomaly (Newton exact, or the 4-term series widened by a tabulated
//   tail x1.5), keep iff |wrap(theta_j - theta_q)(t)| <= (pi/2)(near + (vmax_j+vmax_q)h)/min(peri)
//   + 1e-6. Sound for the linear predicate: min_tau |d0+w tau| >= |d0| - |w|h >=
//   (2/pi) r_min |dtheta(t)| - (vmax_j+vmax_q) h.
// Truth: the predicate on exact Kepler states, for every body (catches any rejection).
use std::f64::consts::{PI, TAU};
use std::hint::black_box;
use std::time::Instant;

const MU: f64 = 4.0 * PI * PI; // AU^3/yr^2
const ROOT_UNIT_AU: f64 = 1.0 / 101_300_000.0;
const NEAR_SHIP: f64 = 1024.0 * 2.0 * (34.0 * 256.0 * ROOT_UNIT_AU); // 0.1759 AU
const NEAR_ROCK: f64 = 1024.0 * 2.0 * (25.0 / 1.496e11); // 3.42e-7 AU
const H_LONG_YR: f64 = 28_141.5 / 31_557_600.0;
const H_SHORT_YR: f64 = 1_000.0 / 31_557_600.0;

struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        let mut x = self.0;
        x ^= x >> 12;
        x ^= x << 25;
        x ^= x >> 27;
        self.0 = x;
        x.wrapping_mul(0x2545F4914F6CDD1D)
    }
    fn f01(&mut self) -> f64 {
        (self.next() >> 11) as f64 * (1.0 / (1u64 << 53) as f64)
    }
}

#[derive(Clone, Copy)]
struct Body {
    a: f64,
    e: f64,
    om: f64,
    m0: f64,
    n: f64,    // rad/yr
    l: f64,    // AU^2/yr
    peri: f64, // AU
    vmax: f64, // AU/yr (vis-viva at periapsis)
    margin: f64
}

fn newton_e(e: f64, m: f64) -> f64 {
    let mut ek = m + e * m.sin();
    for _ in 0..6 {
        let f = ek - e * ek.sin() - m;
        ek -= f / (1.0 - e * ek.cos());
    }
    ek
}

fn nu_of(e: f64, m: f64) -> f64 {
    let ek = newton_e(e, m);
    2.0 * ((1.0 + e).sqrt() * (0.5 * ek).sin()).atan2((1.0 - e).sqrt() * (0.5 * ek).cos())
}

// M of a given nu, by bisection on the monotone map (exact to 1e-14; construction-time only).
fn m_of_nu(e: f64, nu: f64) -> f64 {
    let (mut lo, mut hi) = (nu - 1.0, nu + 1.0);
    for _ in 0..60 {
        let mid = 0.5 * (lo + hi);
        if nu_of(e, mid) < nu { lo = mid; } else { hi = mid; }
    }
    0.5 * (lo + hi)
}

fn eoc_series(e: f64, m: f64) -> f64 {
    let (s1, c1) = (m.sin(), m.cos());
    let s2 = 2.0 * s1 * c1;
    let s3 = s2 * c1 - s1 * (2.0 * c1 * c1 - 1.0);
    (2.0 * e - e * e * e / 4.0) * s1 + 1.25 * e * e * s2 + (13.0 / 12.0) * e * e * e * s3
}

// The series tail bound per e (256 bins, sound at the bin's top e): |series - exact| over M.
fn tail_table() -> [f64; 256] {
    let mut t = [0.0f64; 256];
    for (k, v) in t.iter_mut().enumerate() {
        let e = 0.4 * (k + 1) as f64 / 256.0;
        let mut m = 0.0;
        while m < TAU {
            let g = (eoc_series(e, m) - wrap(nu_of(e, m) - m)).abs();
            if g > *v { *v = g; }
            m += TAU / 8192.0;
        }
    }
    t
}
static TAILS: std::sync::LazyLock<[f64; 256]> = std::sync::LazyLock::new(tail_table);

fn tail_of(e: f64) -> f64 {
    let k = ((e / 0.4 * 256.0).ceil() as usize).clamp(1, 256);
    TAILS[k - 1]
}

fn wrap(x: f64) -> f64 {
    let mut r = x.rem_euclid(TAU);
    if r > PI {
        r -= TAU;
    }
    r
}

// margin(e) = max over M of |nu - M|, tabulated once on 256 e-bins, sound at the bin's top e.
fn margin_table() -> [f64; 256] {
    let mut t = [0.0f64; 256];
    for (k, v) in t.iter_mut().enumerate() {
        let e = 0.4 * (k + 1) as f64 / 256.0;
        let mut m = 0.0;
        while m < TAU {
            let g = wrap(nu_of(e, m) - m).abs();
            if g > *v { *v = g; }
            m += TAU / 8192.0;
        }
    }
    t
}
static MARGINS: std::sync::LazyLock<[f64; 256]> = std::sync::LazyLock::new(margin_table);

fn margin_of(e: f64) -> f64 {
    let k = ((e / 0.4 * 256.0).ceil() as usize).clamp(1, 256);
    MARGINS[k - 1]
}

fn make_body(a: f64, e: f64, om: f64, m0: f64) -> Body {
    let n = TAU / a.powi(3).sqrt();
    let l = (MU * a * (1.0 - e * e)).sqrt();
    let peri = a * (1.0 - e);
    Body { a, e, om, m0, n, l, peri, vmax: (MU * (2.0 / peri - 1.0 / a)).sqrt(), margin: margin_of(e) }
}

fn make_belt(n: usize, seed: u64, e_override: Option<f64>) -> Vec<Body> {
    let mut r = Rng(seed ^ 0x9E3779B97F4A7C15);
    (0..n)
        .map(|_| {
            let a = 2.0 + r.f01();
            let e = e_override.unwrap_or_else(|| loop {
                let e = 0.07 * (-2.0 * (1.0 - r.f01()).ln()).sqrt();
                if e <= 0.4 { return e; }
            });
            make_body(a, e, r.f01() * TAU, r.f01() * TAU)
        })
        .collect()
}

fn state(b: &Body, t: f64) -> ([f64; 2], [f64; 2], f64) {
    let m = b.m0 + b.n * t;
    let nu = nu_of(b.e, m);
    let th = nu + b.om;
    let ek = newton_e(b.e, m);
    let rr = b.a * (1.0 - b.e * ek.cos());
    let (st, ct) = (th.sin(), th.cos());
    let vr = MU * b.e * nu.sin() / b.l;
    let vt = b.l / rr;
    ([rr * ct, rr * st], [vr * ct - vt * st, vr * st + vt * ct], th)
}

fn predicate(d0: [f64; 2], w: [f64; 2], near: f64) -> bool {
    let ww = w[0] * w[0] + w[1] * w[1];
    let tstar = if ww > 0.0 { (-(d0[0] * w[0] + d0[1] * w[1]) / ww).clamp(0.0, 1.0) } else { 0.0 };
    let (dx, dy) = (d0[0] + w[0] * tstar, d0[1] + w[1] * tstar);
    dx * dx + dy * dy <= near * near
}

fn theta_keep(j: &Body, q: &Body, h: f64, near: f64) -> f64 {
    let rmin = j.peri.min(q.peri);
    0.5 * PI * (near + (j.vmax + q.vmax) * h) / rmin + 1e-6
}

fn scene(belt: &[Body], q: &Body, t: f64, h: f64, near: f64, tail: f64, tag: &str, check: bool) -> [f64; 5] {
    let (xq, vq, thq) = state(q, t);
    let lamq = wrap(q.om + q.m0 + q.n * t);
    let (mut k1, mut k2n, mut k2s, mut hits, mut miss) = (0u64, 0, 0, 0, 0);
    for j in belt {
        let tk = theta_keep(j, q, h, near);
        let m = j.m0 + j.n * t;
        let keep1 = wrap(wrap(j.om + m) - lamq).abs() <= tk + j.margin + q.margin;
        let keep2n = wrap(wrap(j.om + m - thq) + wrap(nu_of(j.e, m) - m)).abs() <= tk;
        let keep2s = wrap(wrap(j.om + m - thq) + eoc_series(j.e, m)).abs() <= tk + tail_of(j.e) * 1.5;
        k1 += keep1 as u64;
        k2n += keep2n as u64;
        k2s += keep2s as u64;
        if check {
            let (xj, vj, _) = state(j, t);
            if predicate([xj[0] - xq[0], xj[1] - xq[1]], [(vj[0] - vq[0]) * h, (vj[1] - vq[1]) * h], near) {
                hits += 1;
                if !keep1 || !keep2n || !keep2s {
                    miss += 1;
                }
            }
        }
    }
    let n = belt.len() as f64;
    println!(
        "{{\"scene\":\"{tag}\",\"n\":{n},\"h_yr\":{h:.3e},\"near_AU\":{near:.3e},\"keep1\":{:.5},\"keep2_newton\":{:.6},\"keep2_series\":{:.6},\"truth_hits\":{hits},\"miss\":{miss}}}",
        k1 as f64 / n, k2n as f64 / n, k2s as f64 / n
    );
    [k1 as f64, k2n as f64, k2s as f64, hits as f64, miss as f64]
}

fn timed<F: FnMut() -> usize>(mut f: F, reps: usize) -> (f64, u64) {
    let mut kept = 0u64;
    let t0 = Instant::now();
    for _ in 0..reps {
        kept = black_box(f()) as u64;
    }
    (t0.elapsed().as_nanos() as f64 / reps as f64, kept) // ns per CALL
}

fn main() {
    // The series tail bound on a dense (e, M) grid, fixed before any miss is counted.
    let mut tail = 0.0f64;
    for k in 0..200 {
        let e = 0.4 * k as f64 / 199.0;
        let mut m = 0.0;
        while m < TAU {
            let g = (eoc_series(e, m) - wrap(nu_of(e, m) - m)).abs();
            if g > tail { tail = g; }
            m += TAU / 8192.0;
        }
    }
    println!("{{\"tail_max_rad\":{tail:.3e},\"near_ship_AU\":{NEAR_SHIP:.6},\"near_rock_AU\":{NEAR_ROCK:.3e}}}");

    let n = 100_000usize;
    let t0y = 0.3;

    // SHIPPED operating point (12,850-km ships): seeds 1 (checked), 2 and 3 held out.
    for seed in [1u64, 2, 3] {
        let belt = make_belt(n, seed, None);
        let qs: [(String, Body); 3] = [
            ("belt12345".into(), belt[12_345]),
            ("player-e001".into(), make_body(2.5, 0.01, 1.1, 2.0)),
            ("belt-highe".into(), make_body(2.9, 0.39, 0.4, 5.0)),
        ];
        for (name, q) in &qs {
            for (h, hn) in [(H_LONG_YR, "long"), (H_SHORT_YR, "short")] {
                scene(&belt, q, t0y, h, NEAR_SHIP, tail, &format!("ship-seed{seed}-{name}-{hn}"), seed == 1);
            }
        }
    }

    // ROCK operating point (25-m rocks), both horizons, seeds 1 (checked) and 2 held out.
    for seed in [1u64, 2] {
        let belt = make_belt(n, seed, None);
        for (h, hn) in [(H_LONG_YR, "long"), (H_SHORT_YR, "short")] {
            scene(&belt, &belt[12_345], t0y, h, NEAR_ROCK, tail, &format!("rock-seed{seed}-{hn}"), seed == 1);
        }
    }
    // Positive control: 500 bodies clustered at the querent's own longitude at t0y.
    let mut r = Rng(77);
    let q = make_body(2.5, 0.05, 1.0, 2.0);
    let th0 = state(&q, t0y).2;
    let form: Vec<Body> = (0..500)
        .map(|_| {
            let a = q.a * (1.0 + 1e-3 * (r.f01() - 0.5));
            let e = 0.02;
            let nu = wrap(th0 - q.om + 1e-3 * (r.f01() - 0.5));
            let m0 = wrap(m_of_nu(e, nu) - (TAU / a.powi(3).sqrt()) * t0y);
            make_body(a, e, q.om, m0)
        })
        .collect();
    scene(&form, &q, t0y, H_LONG_YR, NEAR_SHIP, tail, "formation-pos", true);

    // Negative control: the all-e=0.4 tail regime.
    let belt4 = make_belt(n, 42, Some(0.4));
    scene(&belt4, &make_body(2.5, 0.01, 1.1, 2.0), t0y, H_LONG_YR, NEAR_SHIP, tail, "all-e04-neg", true);

    // Fractions at 1e6 at both operating points, and hot-loop costs on the 1e6 data.
    let big = make_belt(1_000_000, 1, None);
    let qm = make_body(2.5, 0.08, 1.7, 3.1);
    let f = scene(&big, &qm, t0y, H_LONG_YR, NEAR_SHIP, tail, "ship-n1e6-seed1", true);
    let fr = scene(&big, &qm, t0y, H_LONG_YR, NEAR_ROCK, tail, "rock-n1e6-seed1", true);
    let (k1f, k2f) = (f[0] / 1e6, f[1] / 1e6);
    let (k1rf, k2rf) = (fr[0] / 1e6, fr[1] / 1e6);

    let lams: Vec<f64> = big.iter().map(|b| wrap(b.om + b.m0 + b.n * t0y)).collect();
    let tks: Vec<f64> = big.iter().map(|b| theta_keep(b, &qm, H_LONG_YR, NEAR_SHIP) + b.margin + qm.margin).collect();
    let lamq = wrap(qm.om + qm.m0 + qm.n * t0y);
    let (ns1, _) = timed(|| lams.iter().zip(&tks).filter(|(l, k)| wrap(*l - lamq).abs() <= **k).count(), 50);
    let c1 = ns1 / lams.len() as f64;

    let surv: Vec<Body> = big
        .iter()
        .copied()
        .filter(|j| wrap(wrap(j.om + j.m0 + j.n * t0y) - lamq).abs() <= theta_keep(j, &qm, H_LONG_YR, NEAR_SHIP) + j.margin + qm.margin)
        .collect();
    let thq = state(&qm, t0y).2;
    let pool: Vec<Body> = (0..40).flat_map(|_| surv.iter().copied()).collect();
    let tk2 = |j: &Body| theta_keep(j, &qm, H_LONG_YR, NEAR_SHIP);
    let (ns2n, keptn) = timed(|| pool.iter().filter(|j| { let m = j.m0 + j.n * t0y; wrap(wrap(j.om + m - thq) + wrap(nu_of(j.e, m) - m)).abs() <= tk2(j) }).count(), 5);
    let (ns2s, kepts) = timed(|| pool.iter().filter(|j| { let m = j.m0 + j.n * t0y; wrap(wrap(j.om + m - thq) + eoc_series(j.e, m)).abs() <= tk2(j) + tail_of(j.e) * 1.5 }).count(), 5);
    let c2n = ns2n / pool.len() as f64;
    let c2s = ns2s / pool.len() as f64;
    println!("{{\"cost_c1_ns\":{:.2},\"cost_c2_newton_ns\":{:.2},\"cost_c2_series_ns\":{:.2},\"timed_pool\":{},\"kept_newton\":{keptn},\"kept_series\":{kepts}}}", c1, c2n, c2s, pool.len());

    for (nn, point, kk1, kk2, hitsf) in [
        (100_000f64, "ship", k1f, k2f, f[3] / 1e6),
        (1_000_000.0, "ship", k1f, k2f, f[3] / 1e6),
        (100_000.0, "rock", k1rf, k2rf, fr[3] / 1e5),
        (1_000_000.0, "rock", k1rf, k2rf, fr[3] / 1e6),
    ] {
        let (k1n, k2n_, hitsn) = (kk1 * nn, kk2 * nn, hitsf * nn);
        let s_lin = |ro: f64| (c1 * nn + c2s * k1n + ro * k2n_) / 1e6;
        let s_exact = (c1 * nn + c2s * k1n + 0.4e3 * k2n_ + 4.2e3 * hitsn) / 1e6;
        println!("{{\"N\":{nn:.0e},\"point\":\"{point}\",\"stage1_pass\":{k1n:.0},\"stage2_pass\":{k2n_:.0},\"true_hits\":{hitsn:.0},\"S_ms_readout4200\":{:.3},\"S_ms_readout500\":{:.3},\"S_ms_float_then_exact\":{s_exact:.3},\"bar_ms\":6.0}}", s_lin(4200.0), s_lin(500.0));
    }
}
