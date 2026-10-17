// The two-stage angular certificate at the TRUE shipped operating point, against the float twin of
// the shipped predicate. One file, no deps: rustc -O falsifier2.rs -o falsifier2 && ./falsifier2
//
// Second-author corrections carried by this record (checker of 20261016-2229-scout-ab3d):
//   1. Constants re-derived from the shipping code: root unit = AU/101_300_000 (scenario.rs::AU,
//      = 1,476.9 m; the Moon's 260,000-root periapsis = 383,990 m checks it), belt branch ships
//      Scalar::raw(34, -10) = 34·2^-10 root units = 49.06 m (scenario.rs:344, doll 0; the 34·2^8
//      constant is the same radius in Home-doll units), near = 2^ENCOUNTER_LOG2·(r_a+r_b)
//      (encounter.rs:18,143) = 2^10·2·49.06 m = 68 root units = 6.7127e-7 AU. The silver run's
//      12,850-km "shipped radii" were wrong by 2^18; one counterfactual row keeps that point on
//      the record (where its "0.53%·N truth wall" lives).
//   2. Truth checks on EVERY scene, every seed (the silver run checked seed 1 only).
//   3. The margin no longer clamps at e = 0.4: max|nu - M| has the closed form
//      (1 + e·cos nu*)^2 = (1 - e^2)^{3/2}  =>  cos nu* = ((1-e^2)^{3/4} - 1)/e,
//      margin = nu* - M* with M* = E* - e·sin E* — exact for any e < 1, cross-checked against the
//      dense grid table on (0, 0.99] (row "margins"). The player can fly e > 0.4; the belt cannot
//      (genesis redraws above 0.4).
//   4. Series tail table extended to e <= 0.99 (belt bodies need <= 0.4; the querent enters
//      stage 2 exactly through state(), so only belt tails apply there).
//   5. Adversarial co-located hits at querent e in {0.6, 0.8, 0.95}: a belt body at periapsis
//      placed exactly on the querent's position (d0 = 0, truth hit by construction), querent at
//      its max-margin phase. `miss` uses exact margins (must be 0); `miss_old_margin` uses the
//      silver run's e=0.4 clamped margin (must be >= 1: the fix is load-bearing).
use std::f64::consts::{PI, TAU};
use std::hint::black_box;
use std::time::Instant;

const MU: f64 = 4.0 * PI * PI; // AU^3/yr^2
const ROOT_UNIT_AU: f64 = 1.0 / 101_300_000.0; // scenario.rs::AU
const NEAR_TRUE: f64 = 68.0 * ROOT_UNIT_AU; // 2^10 · (34·2^-10 + 34·2^-10) root units = 6.7127e-7 AU
const NEAR_COUNTERFACTUAL: f64 = 1024.0 * 2.0 * (34.0 * 256.0 * ROOT_UNIT_AU); // the silver run's 2^18 misread
const H_LONG_YR: f64 = 28_141.5 / 31_557_600.0;
const H_SHORT_YR: f64 = 1_000.0 / 31_557_600.0;
const E_TABLE_MAX: f64 = 0.99;

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
    margin: f64,
}

fn newton_e(e: f64, m: f64) -> f64 {
    let mut ek = m + e * m.sin();
    for _ in 0..12 {
        let f = ek - e * ek.sin() - m;
        ek -= f / (1.0 - e * ek.cos());
        if f.abs() < 1e-14 {
            return ek;
        }
    }
    // High-e fallback: bisect the monotone map (exact to 1e-18; only the crafted querents hit it).
    let (mut lo, mut hi) = (m - 1.0f64, m + 1.0f64);
    for _ in 0..100 {
        let mid = 0.5 * (lo + hi);
        if mid - e * mid.sin() < m { lo = mid; } else { hi = mid; }
    }
    0.5 * (lo + hi)
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

// Exact max|nu - M| for any e < 1, in closed form: d(nu - M)/dM = (1 + e·cos nu)^2/(1 - e^2)^{3/2}
// equals 1 exactly when cos nu* = ((1 - e^2)^{3/4} - 1)/e; nu - M is odd in M, rises to its max at
// nu* in (pi/2, pi), so max|nu - M| = nu* - M* with M* = E* - e·sin E* (all closed form).
// Widened by 1e-9 (float hygiene). Belt and querent alike.
fn margin_exact(e: f64) -> f64 {
    if e < 1e-9 {
        return 0.0;
    }
    let cos_nu = ((1.0 - e * e).powf(0.75) - 1.0) / e;
    let nu = cos_nu.acos();
    let ek = 2.0 * ((0.5 * nu).tan() * ((1.0 - e) / (1.0 + e)).sqrt()).atan();
    let m = ek - e * ek.sin();
    nu - m + 1e-9
}


// The silver run's clamped lookup (the bug this run fixes): bins over (0, 0.4], e > 0.4 clamps.
fn margin_table04() -> [f64; 256] {
    let mut t = [0.0f64; 256];
    for (k, v) in t.iter_mut().enumerate() {
        let e = 0.4 * (k + 1) as f64 / 256.0;
        let mut m = 0.0;
        while m < TAU {
            let g = wrap(nu_of(e, m) - m).abs();
            if g > *v { *v = g; }
            m += TAU / 32768.0;
        }
    }
    t
}
static MARGINS04: std::sync::LazyLock<[f64; 256]> = std::sync::LazyLock::new(margin_table04);
fn margin_of_old(e: f64) -> f64 {
    let k = ((e.min(0.4) / 0.4 * 256.0).ceil() as usize).clamp(1, 256);
    MARGINS04[k - 1]
}

// The series tail bound per e (512 bins over (0, E_TABLE_MAX], sound at the bin's top e):
// |series - exact| over M; e above the table keeps everything (tail = pi).
fn tail_table() -> [f64; 512] {
    let mut t = [0.0f64; 512];
    for (k, v) in t.iter_mut().enumerate() {
        let e = E_TABLE_MAX * (k + 1) as f64 / 512.0;
        let mut m = 0.0;
        while m < TAU {
            let g = (eoc_series(e, m) - wrap(nu_of(e, m) - m)).abs();
            if g > *v { *v = g; }
            m += TAU / 32768.0;
        }
    }
    t
}
static TAILS: std::sync::LazyLock<[f64; 512]> = std::sync::LazyLock::new(tail_table);

fn tail_of(e: f64) -> f64 {
    if e >= E_TABLE_MAX {
        return PI;
    }
    let k = ((e / E_TABLE_MAX * 512.0).ceil() as usize).clamp(1, 512);
    TAILS[k - 1]
}

fn wrap(x: f64) -> f64 {
    let mut r = x.rem_euclid(TAU);
    if r > PI {
        r -= TAU;
    }
    r
}

fn make_body(a: f64, e: f64, om: f64, m0: f64) -> Body {
    let n = TAU / a.powi(3).sqrt();
    let l = (MU * a * (1.0 - e * e)).sqrt();
    let peri = a * (1.0 - e);
    Body { a, e, om, m0, n, l, peri, vmax: (MU * (2.0 / peri - 1.0 / a)).sqrt(), margin: margin_exact(e) }
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

fn scene(belt: &[Body], q: &Body, t: f64, h: f64, near: f64, tag: &str) -> [f64; 5] {
    scene_skipping(belt, usize::MAX, q, t, h, near, tag)
}

// `skip` is the querent's own index in the belt: the shipped scan never returns the player
// itself (encounter.rs: `j == body ... continue`), so the self-pair (d0 = 0, a trivial "hit")
// is excluded from truth and keeps alike.
fn scene_skipping(belt: &[Body], skip: usize, q: &Body, t: f64, h: f64, near: f64, tag: &str) -> [f64; 5] {
    let qm_old = margin_of_old(q.e); // the silver run's clamped querent margin
    let (xq, vq, thq) = state(q, t);
    let lamq = wrap(q.om + q.m0 + q.n * t);
    let (mut k1, mut k2n, mut k2s, mut hits, mut miss, mut miss_old) = (0u64, 0, 0, 0, 0, 0);
   for (ij, j) in belt.iter().enumerate() {
       if ij == skip { continue; }
        let tk = theta_keep(j, q, h, near);
        let m = j.m0 + j.n * t;
        let lam = wrap(j.om + m);
        let keep1 = wrap(lam - lamq).abs() <= tk + j.margin + q.margin;
        let keep1_old = wrap(lam - lamq).abs() <= tk + j.margin + qm_old;
        let keep2n = wrap(wrap(j.om + m - thq) + wrap(nu_of(j.e, m) - m)).abs() <= tk;
        let keep2s = wrap(wrap(j.om + m - thq) + eoc_series(j.e, m)).abs() <= tk + tail_of(j.e) * 1.5;
        k1 += keep1 as u64;
        k2n += keep2n as u64;
        k2s += keep2s as u64;
        let (xj, vj, _) = state(j, t);
        if predicate([xj[0] - xq[0], xj[1] - xq[1]], [(vj[0] - vq[0]) * h, (vj[1] - vq[1]) * h], near) {
            hits += 1;
            if !keep1 || !keep2n || !keep2s {
                miss += 1;
            }
            if !keep1_old {
                miss_old += 1;
            }
        }
    }
    let n = belt.len() as f64;
    println!(
        "{{\"scene\":\"{tag}\",\"n\":{n},\"h_yr\":{h:.3e},\"near_AU\":{near:.3e},\"keep1\":{:.5},\"keep2_newton\":{:.6},\"keep2_series\":{:.6},\"truth_hits\":{hits},\"miss\":{miss},\"miss_old_margin\":{miss_old}}}",
        k1 as f64 / n, k2n as f64 / n, k2s as f64 / n
    );
    [k1 as f64, k2n as f64, k2s as f64, hits as f64, miss as f64]
}

// The adversarial pair: querent (e > 0.4, the player can fly it) at its MAX-margin phase, and a
// belt body at periapsis placed exactly on the querent's position (d0 = 0: a guaranteed truth
// hit). At the extremum, |lam_j - lam_q| = margin(e_q) exactly: the clamped 0.4 margin cannot
// cover it, the exact margin can.
fn colocated_pair(e_q: f64, a_q: f64) -> (Body, Body) {
    let cos_nu = ((1.0 - e_q * e_q).powf(0.75) - 1.0) / e_q;
    let nu_s = cos_nu.acos();
    let ek = 2.0 * ((0.5 * nu_s).tan() * ((1.0 - e_q) / (1.0 + e_q)).sqrt()).atan();
    let m_s = ek - e_q * ek.sin();
    let q = make_body(a_q, e_q, 0.0, m_s); // t = 0: M_q(0) = M*
    let r_q = a_q * (1.0 - e_q * e_q) / (1.0 + e_q * cos_nu);
    let e_j = 0.1;
    let a_j = r_q / (1.0 - e_j); // belt-legal: peri = r_q in [1.2, 3) AU, apo < 3 AU
    let j = make_body(a_j, e_j, nu_s, 0.0); // nu_j(0) = 0, M_j = 0, omega_j = theta_q
    (q, j)
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
    // Margin closed form vs a dense same-e grid max on (0, E_TABLE_MAX]: the closed form is the
    // true supremum, the grid only underestimates it by its own resolution, so closed - grid must
    // sit in [-1e-6, small+]; a negative beyond -1e-6 means the derivation is wrong (K0).
    let (mut gmin, mut gmax) = (f64::INFINITY, f64::NEG_INFINITY);
    for k in 0..500 {
        let e = 0.002 + E_TABLE_MAX * k as f64 / 500.0;
        let mut grid = 0.0f64;
        let mut m = 0.0;
        while m < TAU {
            let g = wrap(nu_of(e, m) - m).abs();
            if g > grid { grid = g; }
            m += TAU / 8192.0;
        }
        let d = margin_exact(e) - grid;
        gmin = gmin.min(d);
        gmax = gmax.max(d);
    }
    println!(
        "{{\"near_true_AU\":{:.4e},\"near_counterfactual_AU\":{NEAR_COUNTERFACTUAL:.6},\"margin_e007\":{:.4},\"margin_e04\":{:.4},\"margin_e06\":{:.4},\"margin_e08\":{:.4},\"margin_e095\":{:.4},\"margin_closed_minus_grid_min\":{:.2e},\"margin_closed_minus_grid_max\":{:.2e},\"tail04_rad\":{:.3e},\"tail099_rad\":{:.3e}}}",
        NEAR_TRUE, margin_exact(0.07), margin_exact(0.4), margin_exact(0.6), margin_exact(0.8), margin_exact(0.95),
        gmin, gmax, TAILS[207], TAILS[511]
    );

    let n = 100_000usize;
    let t0y = 0.3;

    // TRUE operating point (49-m ships): every scene truth-checked, seeds 1-3 plus held-out 5, 7.
    for seed in [1u64, 2, 3, 5, 7] {
        let belt = make_belt(n, seed, None);
        let mut qs: Vec<(String, Body)> = vec![
            ("belt12345".into(), belt[12_345]),
            ("player-e001".into(), make_body(2.5, 0.01, 1.1, 2.0)),
            ("belt-highe".into(), make_body(2.9, 0.39, 0.4, 5.0)),
        ];
        if seed > 3 {
            qs.truncate(2); // held-out seeds: belt querent and player querent, long h only
        }
        for (name, q) in &qs {
            let skip = if name == "belt12345" { 12_345 } else { usize::MAX };
            for (h, hn) in [(H_LONG_YR, "long"), (H_SHORT_YR, "short")] {
                if seed > 3 && hn != "long" { continue; }
                scene_skipping(&belt, skip, q, t0y, h, NEAR_TRUE, &format!("true-seed{seed}-{name}-{hn}"));
            }
        }
    }

    // Positive control at the true scale: 500 bodies within near/2 of the querent's position.
    let mut r = Rng(77);
    let q = make_body(2.5, 0.05, 1.0, 2.0);
    let (xq, _vq, _thq) = state(&q, t0y);
    let form: Vec<Body> = (0..500)
        .map(|_| {
            let ang = r.f01() * TAU;
            let rad = r.f01().sqrt() * NEAR_TRUE * 0.5;
            let pr = ((xq[0] + rad * ang.cos()).hypot(xq[1] + rad * ang.sin())).max(1e-9);
            let pth = (xq[1] + rad * ang.sin()).atan2(xq[0] + rad * ang.cos());
            let (e_j, nu_j): (f64, f64) = (0.05, 1.0);
            let a_j = pr * (1.0 + e_j * nu_j.cos()) / (1.0 - e_j * e_j); // r(nu) = a(1-e^2)/(1+e cos nu), inverted
            let om_j = pth - nu_j;
            let m0 = wrap(m_of_nu(e_j, nu_j) - (TAU / a_j.powi(3).sqrt()) * t0y);
            make_body(a_j, e_j, om_j, m0)
        })
        .collect();
    scene(&form, &q, t0y, H_LONG_YR, NEAR_TRUE, "formation-true-scale");

    // Negative control (cost, not soundness): the all-e=0.4 tail regime at the true point.
    let belt4 = make_belt(n, 42, Some(0.4));
    scene(&belt4, &make_body(2.5, 0.01, 1.1, 2.0), t0y, H_LONG_YR, NEAR_TRUE, "all-e04-neg");

    // Counterfactual Earth-sized belt (the silver run's misread near): where its "0.53%·N truth
    // wall" lives. Not the shipped point; kept so the old claim's domain stays measured.
    let beltc = make_belt(n, 1, None);
    scene_skipping(&beltc, 12_345, &beltc[12_345], t0y, H_LONG_YR, NEAR_COUNTERFACTUAL, "counterfactual-0.176AU");

    // Adversarial co-located hits, querent e in {0.6, 0.8, 0.95}: miss must be 0 with exact
    // margins, >= 1 under the silver run's clamped table (the fix is load-bearing).
    for (e_q, a_q) in [(0.6f64, 2.2f64), (0.8, 3.5), (0.95, 4.0)] {
        let mut belt = make_belt(n, 11, None);
        let (q, j) = colocated_pair(e_q, a_q);
        belt[0] = j;
        scene(&belt, &q, 0.0, H_LONG_YR, NEAR_TRUE, &format!("colocated-e{e_q:.2}"));
    }

    // Querent-e degradation (cost, not soundness): full scenes at e = 0.6 and e = 0.95.
    let belt = make_belt(n, 1, None);
    let fe06 = scene(&belt, &make_body(2.2, 0.6, 0.7, 1.3), t0y, H_LONG_YR, NEAR_TRUE, "querent-e06-cost");
    let fe095 = scene(&belt, &make_body(4.0, 0.95, 0.7, 1.3), t0y, H_LONG_YR, NEAR_TRUE, "querent-e095-cost");

    // Fractions at 1e6 at the true point, seed 1 and held-out seed 7, both truth-checked.
    let mut k1f = 0.0;
    let mut k2sf = 0.0;
    for seed in [1u64, 7] {
        let big = make_belt(1_000_000, seed, None);
        let qm = make_body(2.5, 0.08, 1.7, 3.1);
        let f = scene(&big, &qm, t0y, H_LONG_YR, NEAR_TRUE, &format!("true-n1e6-seed{seed}"));
        if seed == 1 {
            k1f = f[0] / 1e6;
            // (Newton keep fraction not needed below; the series form is the wired one.)
            k2sf = f[2] / 1e6;
        }
    }

    // Hot-loop costs on the 1e6 data at the true point.
    let big = make_belt(1_000_000, 1, None);
    let qm = make_body(2.5, 0.08, 1.7, 3.1);
    let lams: Vec<f64> = big.iter().map(|b| wrap(b.om + b.m0 + b.n * t0y)).collect();
    let tks: Vec<f64> = big.iter().map(|b| theta_keep(b, &qm, H_LONG_YR, NEAR_TRUE) + b.margin + qm.margin).collect();
    let lamq = wrap(qm.om + qm.m0 + qm.n * t0y);
    let (ns1, _) = timed(|| lams.iter().zip(&tks).filter(|(l, k)| wrap(*l - lamq).abs() <= **k).count(), 50);
    let c1 = ns1 / lams.len() as f64;

    let surv: Vec<Body> = big
        .iter()
        .copied()
        .filter(|j| wrap(wrap(j.om + j.m0 + j.n * t0y) - lamq).abs() <= theta_keep(j, &qm, H_LONG_YR, NEAR_TRUE) + j.margin + qm.margin)
        .collect();
    let thq = state(&qm, t0y).2;
    let pool: Vec<Body> = (0..40).flat_map(|_| surv.iter().copied()).collect();
    let tk2 = |j: &Body| theta_keep(j, &qm, H_LONG_YR, NEAR_TRUE);
    let (ns2n, keptn) = timed(|| pool.iter().filter(|j| { let m = j.m0 + j.n * t0y; wrap(wrap(j.om + m - thq) + wrap(nu_of(j.e, m) - m)).abs() <= tk2(j) }).count(), 5);
    let (ns2s, kepts) = timed(|| pool.iter().filter(|j| { let m = j.m0 + j.n * t0y; wrap(wrap(j.om + m - thq) + eoc_series(j.e, m)).abs() <= tk2(j) + tail_of(j.e) * 1.5 }).count(), 5);
    let c2n = ns2n / pool.len() as f64;
    let c2s = ns2s / pool.len() as f64;
    println!("{{\"cost_c1_ns\":{:.2},\"cost_c2_newton_ns\":{:.2},\"cost_c2_series_ns\":{:.2},\"timed_pool\":{},\"kept_newton\":{keptn},\"kept_series\":{kepts}}}", c1, c2n, c2s, pool.len());

    // Composed S from THIS run's measured costs and fractions (ms): wired = O(N) pass + series +
    // the shipped 4.2-us exact readout on series survivors; index = the standing lambda-bin index
    // (stage 1 free) + the 0.5-us closed-form readout. Bar: 6 ms.
    for (nn, k1n_, k2n_) in [
        (100_000f64, k1f * 100_000.0, k2sf * 100_000.0),
        (1_000_000.0, k1f * 1_000_000.0, k2sf * 1_000_000.0),
    ] {
        let wired = (c1 * nn + c2s * k1n_ + 4.2e3 * k2n_) / 1e6;
        let cheap = (c1 * nn + c2s * k1n_ + 0.5e3 * k2n_) / 1e6;
        let index = (c2s * k1n_ + 0.5e3 * k2n_) / 1e6;
        println!("{{\"N\":{nn:.0e},\"point\":\"true\",\"stage1_pass\":{:.0},\"stage2_series_pass\":{:.0},\"S_ms_wired\":{:.3},\"S_ms_cheap_readout\":{:.3},\"S_ms_lambda_index\":{:.3},\"bar_ms\":6.0}}", k1n_, k2n_, wired, cheap, index);
    }

    // Querent-e degradation of the wired S at 1e5 (the honest domain boundary of the bar).
    for (tag, fe) in [("e06", fe06), ("e095", fe095)] {
        let (k1n_, k2n_) = (fe[0], fe[2]);
        let wired = (c1 * n as f64 + c2s * k1n_ + 4.2e3 * k2n_) / 1e6;
        println!("{{\"N\":1e5,\"point\":\"true-querent-{tag}\",\"stage1_pass\":{:.0},\"stage2_series_pass\":{:.0},\"S_ms_wired\":{:.3},\"bar_ms\":6.0}}", k1n_, k2n_, wired);
    }
}
