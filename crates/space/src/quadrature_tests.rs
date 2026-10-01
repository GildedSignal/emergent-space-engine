//! Independent real-node checks of the native panels, not a global certificate.
use super::*;
fn d(x: Scalar) -> f64 {
    x.significand() as f64 * 2f64.powi(x.exponent() as i32 - 62)
}
fn real_nodes(n: usize) -> Vec<(f64, f64)> {
    let pi = std::f64::consts::PI;
    (0..n)
        .map(|i| {
            let mut x = (pi * (i as f64 + 0.75) / (n as f64 + 0.5)).cos();
            let mut dp = 0.0;
            for _ in 0..20 {
                let (mut a, mut b) = (1.0, x);
                for j in 2..=n {
                    (a, b) = (
                        b,
                        ((2 * j - 1) as f64 * x * b - (j - 1) as f64 * a) / j as f64,
                    );
                }
                dp = n as f64 * (x * b - a) / (x * x - 1.0);
                let next = x - b / dp;
                if next == x {
                    break;
                }
                x = next;
            }
            (x, 2.0 / ((1.0 - x * x) * dp * dp))
        })
        .collect()
}
// Fourth-derivative majorants on the whole panel, not a fitted tolerance.
fn majorant(v0: f64, v: [f64; 5], alpha: f64) -> [f64; 5] {
    let mut f = [0.0; 5];
    f[0] = v0.powf(-alpha);
    for n in 1..5 {
        f[n] = (1..=n)
            .map(|j| (n as f64 + (alpha - 1.0) * j as f64) * v[j] * f[n - j])
            .sum::<f64>()
            / (n as f64 * v0);
    }
    f
}
fn product(a: [f64; 5], b: [f64; 5]) -> [f64; 5] {
    std::array::from_fn(|n| (0..=n).map(|j| a[j] * b[n - j]).sum())
}
fn panel_bound(k: f64, q: f64, tn: f64, taun: f64, lo: f64, hi: f64) -> [f64; 3] {
    let eta = 1.0 - k;
    let xmin = k + eta * hi.cos();
    let xmax = k + eta * lo.cos();
    let sn = if lo <= std::f64::consts::FRAC_PI_2 && hi >= std::f64::consts::FRAC_PI_2 {
        1.0
    } else {
        lo.sin().max(hi.sin())
    };
    let cs = lo.cos().abs().max(hi.cos().abs());
    let mut v = [0.0; 5];
    let mut fact = 1.0;
    for (j, a) in v.iter_mut().enumerate().skip(1) {
        fact *= j as f64;
        *a = eta * (if j % 2 == 0 { cs } else { sn }) / fact;
    }
    let gravitational = v.map(|a| a * 2.0 * q);
    let g = majorant(1.0 - q * (4.0 * k + 2.0 * xmax), gravitational, 0.5);
    let inv = majorant(xmin, v, 2.0);
    let horizon = majorant(1.0 - 2.0 * q * xmax, gravitational, 1.0);
    let clock = product(g, inv);
    // Two-point Gauss: h^5 sup of the fourth Taylor coefficient /180.
    let h5 = (hi - lo).powi(5) / 180.0;
    [
        g[4] * h5,
        tn * product(clock, horizon)[4] * h5,
        taun * clock[4] * h5,
    ]
}
#[test]
fn native_panels_obey_the_real_two_point_remainder_and_integer_rounding_allowance() {
    let nodes = real_nodes(16);
    let mut keys = vec![];
    for (p, e) in [
        (7, 0.0),
        (8, 0.9),
        (20, 0.3),
        (1000, 0.7),
        (1_000_000_000_000, 0.99),
    ] {
        keys.push((
            OrbitKey::bound(Scalar::integer(p), (e * 2f64.powi(48)).round() as u64).unwrap(),
            false,
        ));
    }
    for b in [6, 10, 1000] {
        keys.push((OrbitKey::photon(Scalar::integer(b)).unwrap().unwrap(), true));
    }
    for (key, null) in keys {
        let shape = if null {
            Passage::compile(key, key.periapsis.scale(5).unwrap())
                .unwrap()
                .orbit
                .shape
        } else {
            Orbit::compile(key).unwrap().shape
        };
        let k = key.k as f64 / 2f64.powi(48);
        let q = 1.0 / d(key.periapsis);
        let tn = if null {
            (1.0 - 2.0 * q).sqrt()
        } else {
            (k * (1.0 - 2.0 * q) * (1.0 + 2.0 * q * (1.0 - 2.0 * k))).sqrt()
        };
        let taun = if null {
            0.0
        } else {
            (k - q * (3.0 * k * k + (1.0 - k).powi(2))).sqrt()
        };
        for w in shape.knots.windows(2) {
            let (lo, hi) = (
                w[0].psi as f64 / 2f64.powi(61),
                w[1].psi as f64 / 2f64.powi(61),
            );
            let mut want = [0.0; 3];
            for &(node, weight) in &nodes {
                let psi = (lo + hi) / 2.0 + (hi - lo) * node / 2.0;
                let x = k + (1.0 - k) * psi.cos();
                let a = 4.0 * k + 2.0 * x;
                let root = (1.0 - q * a).sqrt();
                let values = [
                    1.0 / root,
                    tn / (root * x * x * (1.0 - 2.0 * q * x)),
                    taun / (root * x * x),
                ];
                for i in 0..3 {
                    want[i] += values[i] * weight * (hi - lo) / 2.0;
                }
            }
            let got = shape.quad(w[0].psi as i128, w[1].psi as i128).unwrap();
            let actual = [
                hi - lo + q * d(got.0[0]),
                d(got.0[1]
                    .add(got.0[3].mul(key.compactness().unwrap()).unwrap())
                    .unwrap()),
                d(got.0[2]
                    .add(got.0[4].mul(key.compactness().unwrap()).unwrap())
                    .unwrap()),
            ];
            let bound = panel_bound(k, q, tn, taun, lo, hi);
            for i in 0..3 {
                assert!(
                    (actual[i] - want[i]).abs() <= bound[i] + want[i].abs() * 1e-8 + 1e-12,
                    "{key:?} {lo}..{hi} component {i}: {} vs {}",
                    actual[i],
                    want[i]
                );
            }
        }
    }
}
