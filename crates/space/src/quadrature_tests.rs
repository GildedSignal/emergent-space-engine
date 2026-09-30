//! Numerical checks of the analytic proof in ../QUADRATURE.md, not runtime certificates.
use super::*;
use std::f64::consts::PI as P;
#[allow(dead_code)]
#[path = "../../../xtask/src/behave/sample.rs"]
mod sample;

fn gauss(n: usize) -> Vec<(f64, f64)> {
    (0..n)
        .map(|i| {
            let mut x = (P * (i as f64 + 0.75) / (n as f64 + 0.5)).cos();
            for _ in 0..16 {
                let (mut a, mut b) = (1.0, x);
                for j in 2..=n {
                    (a, b) = (b, ((2 * j - 1) as f64 * x * b - (j - 1) as f64 * a) / j as f64);
                }
                let dp = n as f64 * (x * b - a) / (x * x - 1.0);
                let next = x - b / dp;
                if next == x {
                    break;
                }
                x = next;
            }
            let (mut a, mut b) = (1.0, x);
            for j in 2..=n {
                (a, b) = (b, ((2 * j - 1) as f64 * x * b - (j - 1) as f64 * a) / j as f64);
            }
            let dp = n as f64 * (x * b - a) / (x * x - 1.0);
            (x, 2.0 / ((1.0 - x * x) * dp * dp))
        })
        .collect()
}
fn majorant(v0: f64, v: [f64; 9], alpha: f64) -> [f64; 9] {
    assert!(v0 > 0.0);
    let mut f = [0.0; 9];
    f[0] = v0.powf(-alpha);
    for n in 1..=8 {
        f[n] = (1..=n)
            .map(|j| (n as f64 + (alpha - 1.0) * j as f64) * v[j] * f[n - j])
            .sum::<f64>()
            / (n as f64 * v0);
    }
    f
}
fn product(a: [f64; 9], b: [f64; 9]) -> [f64; 9] {
    std::array::from_fn(|n| (0..=n).map(|i| a[i] * b[n - i]).sum())
}
struct Real {
    umin: f64,
    a: f64,
    gap: f64,
    ua: f64,
}
impl Real {
    fn new(s: &Shape) -> Self {
        let q = 2f64.powi(62);
        Self {
            umin: (s.c - s.a) as f64 / q,
            a: s.a as f64 / q,
            gap: 2.0 * (s.m3 - s.a) as f64 / q,
            ua: s.ua as f64 / q,
        }
    }
    fn u(&self, x: f64) -> f64 {
        self.umin + 2.0 * self.a * (x / 2.0).cos().powi(2)
    }
    fn d(&self, x: f64) -> f64 {
        self.gap + 4.0 * self.a * (x / 2.0).sin().powi(2)
    }
    fn value(&self, x: f64, clocks: bool) -> [f64; 3] {
        let g = self.d(x).sqrt().recip();
        if !clocks {
            return [g, 0.0, 0.0];
        }
        let u = self.u(x);
        let tau = g * (self.ua / u).powi(2);
        [g, tau, tau / (1.0 - 2.0 * u)]
    }
    fn bound(&self, lo: f64, hi: f64, clocks: bool) -> [f64; 3] {
        let sin = if lo <= P / 2.0 && hi >= P / 2.0 {
            1.0
        } else {
            lo.sin().max(hi.sin())
        };
        let cos = lo.cos().abs().max(hi.cos().abs());
        let mut v = [0.0; 9];
        let mut factorial = 1.0;
        for (j, x) in v.iter_mut().enumerate().skip(1) {
            factorial *= j as f64;
            *x = self.a * (if j % 2 == 0 { cos } else { sin }) / factorial;
        }
        let g = majorant(self.d(lo), v.map(|x| 2.0 * x), 0.5);
        let factor = (hi - lo).powi(9) / 44100.0;
        if !clocks {
            return [factor * g[8], 0.0, 0.0];
        }
        let q = majorant(self.u(hi), v, 2.0);
        let j = majorant(1.0 - 2.0 * self.u(lo), v.map(|x| 2.0 * x), 1.0);
        let tau = product(g, q).map(|x| x * self.ua * self.ua);
        [factor * g[8], factor * tau[8], factor * product(tau, j)[8]]
    }
    fn rounding(&self, lo: f64, hi: f64, clocks: bool, shift: u32) -> [f64; 3] {
        let q = 2f64.powi(-62);
        let eps = (64.0 * self.a + 1.0) * q;
        let d = self.d(lo);
        let u = self.u(hi);
        let horizon = 1.0 - 2.0 * self.u(lo);
        assert!(d > 2.0 * eps);
        let g = 1.0 / d.sqrt();
        let eg = eps / (d - 2.0 * eps).powf(1.5) + 2f64.powi(-41);
        let width = hi - lo;
        let weights = 8.0 * 2f64.powi(-61);
        let phi = width * eg + weights * (g + eg);
        if !clocks {
            return [phi, 0.0, 0.0];
        }
        assert!(u > eps && horizon > 2.0 * eps);
        let qr = self.ua / u;
        let eq = self.ua * eps / (u * (u - eps)) + q;
        let tau = qr * qr;
        let etau = 2.0 * qr * eq + eq * eq + q;
        let time = tau / horizon;
        let etime = etau / (horizon - 2.0 * eps) + tau * 2.0 * eps / (horizon * (horizon - 2.0 * eps)) + q;
        let clock = |r: f64, er: f64| {
            width * (eg * r + (g + eg) * er) + weights * (g + eg) * (r + er) + 4.0 * 2f64.powi(shift as i32 - 103) * (r + er)
        };
        [phi, clock(tau, etau), clock(time, etime)]
    }
    fn integrate(&self, lo: f64, width: f64, nodes: &[(f64, f64)], parts: usize, clocks: bool) -> [f64; 3] {
        let mut out = [0.0; 3];
        let width = width / parts as f64;
        for j in 0..parts {
            for &(x, w) in nodes {
                let f = self.value(lo + width * (j as f64 + 0.5 + 0.5 * x), clocks);
                for k in 0..3 {
                    out[k] += f[k] * w * width / 2.0;
                }
            }
        }
        out
    }
}
#[test]
fn degree_eight_witness_requires_the_proved_constant() {
    let approx = gauss(4).into_iter().map(|(x, w)| w / 2.0 * ((x + 1.0) / 2.0).powi(8)).sum::<f64>();
    let error = (1.0 / 9.0 - approx).abs();
    assert!((error - 1.0 / 44100.0).abs() < 1e-15);
    assert!(error > 1.0 / 88200.0, "a bound understated by a factor of two must fail");
}
#[test]
fn panel_bound_dominates_independent_refined_quadrature() {
    let gl4 = gauss(4);
    let gl8 = gauss(8);
    let mut cases = sample::bound_orbits(256);
    for p in [7.0, 8.0, 10.0, 30.0, 100.0, 1000.0, 8192.0] {
        for e in [0.0, 1e-6, 0.01, 0.03, 0.5, 0.9, 0.99, 0.9999] {
            if p > 6.0 + 2.0 * e {
                cases.push((p, e));
            }
        }
    }
    for e in [0.0, 0.01, 0.1, 0.5, 0.9] {
        for gap in [0.001, 0.01, 0.1] {
            cases.push((6.0 + 2.0 * e + gap, e));
        }
    }
    let mut panels = 0;
    let (mut ratio, mut max_relative_bound, mut max_relative_error) = (0f64, 0f64, 0f64);
    let mut worst = String::new();
    let mut check = |s: &Shape, lo: i128, hi: i128, clocks: bool| {
        let r = Real::new(s);
        let a = lo as f64 / 2f64.powi(61);
        let b = hi as f64 / 2f64.powi(61);
        // Subtract integers before converting: close f64 endpoints lose panel-width bits.
        let width = (hi - lo) as f64 / 2f64.powi(61);
        let f4 = r.integrate(a, width, &gl4, 1, clocks);
        let f8 = r.integrate(a, width, &gl8, 8, clocks);
        let f16 = r.integrate(a, width, &gl8, 16, clocks);
        let bound = r.bound(a, b, clocks);
        let arithmetic = r.rounding(a, b, clocks, s.clock_shift);
        let mut integer = [0i128; 3];
        s.quad(lo, hi, clocks, &mut integer).unwrap();
        let int = [
            integer[0] as f64 / 2f64.powi(103),
            integer[1] as f64 / 2f64.powi(165 - s.clock_shift as i32),
            integer[2] as f64 / 2f64.powi(165 - s.clock_shift as i32),
        ];
        for k in 0..if clocks { 3 } else { 1 } {
            let noise = 4e-13 * f16[k].abs();
            assert!((f8[k] - f16[k]).abs() <= noise, "oracle unconverged");
            let error = (f4[k] - f16[k]).abs();
            assert!(
                bound[k].is_finite() && error <= bound[k] + noise,
                "panel [{a},{b}], component {k}: error {error:e} bound {:e}",
                bound[k]
            );
            if error > noise && bound[k] > 0.0 {
                ratio = ratio.max(error / bound[k]);
            }
            // Floating evaluation of the conditional arithmetic bound, not a runtime certificate.
            let rounding = arithmetic[k] + noise;
            assert!(
                (int[k] - f4[k]).abs() <= rounding,
                "integer rounding exceeds diagnostic allowance: [{a},{b}] component {k}, error={:e} allowance={rounding:e} value={:e}",
                (int[k] - f4[k]).abs(),
                f4[k]
            );
            if bound[k] / f16[k].abs() > max_relative_bound {
                max_relative_bound = bound[k] / f16[k].abs();
                worst = format!("lo={a:.6} hi={b:.6} component={k} A={} Dmin={} Umin={}", r.a, r.d(a), r.u(b));
            }
            max_relative_error = max_relative_error.max(error / f16[k].abs());
        }
        panels += 1;
    };
    for &(p, e) in &cases {
        let key = Key::darwin((p * 65536.0).round() as u32, (e * 1073741824.0).round() as u32).unwrap();
        let s = Shape::bound(key, false).unwrap();
        let mut lo = 0;
        for hi in s.cuts().map(|(_, p)| p).chain(std::iter::once(PI)) {
            s.panels(lo, hi, |a, b| {
                check(&s, a, b, true);
                Ok(true)
            })
            .unwrap();
            lo = hi;
        }
    }
    // Unbound geometry with U=0 at infinity. Only the angle has a finite integral.
    let q = ONE as f64;
    let s = Shape {
        ua: (-0.125 * q) as i64,
        up: (0.2 * q) as i64,
        c: (0.0375 * q) as i64,
        a: (0.1625 * q) as i64,
        m3: (0.3875 * q) as i64,
        newton: false,
        pm: 0,
        pe: 0,
        e: 0,
        lambda: Shape::refinement_width((0.1625 * q) as i128, (0.3875 * q) as i128, false),
        clock_shift: 63,
    };
    s.panels(0, s.cut(0), |a, b| {
        check(&s, a, b, false);
        Ok(true)
    })
    .unwrap();
    println!("quadrature: {} bound shapes, {panels} panels; max error/bound={ratio:.3e}, max panel relative bound={max_relative_bound:.3e}, error={max_relative_error:.3e}",cases.len());
    println!("worst bound: {worst}");
}
