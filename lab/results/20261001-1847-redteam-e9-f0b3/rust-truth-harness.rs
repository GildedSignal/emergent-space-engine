//! Independent Schwarzschild geodesic pairs, not the engine's tide or orbit compiler.
//! Coordinates (s=t sqrt(M/rp³), rho=r/rp, phi), lambda=tau sqrt(M/rp³).
//! Metric/rp² = diag(-f/alpha, 1/f, rho²), f=1-2alpha/rho, alpha=M/rp.
//! Affine radial ODE follows normalization and the two Killing constants:
//! rho''=-rho^-2 + Lbar² rho^-3 - 3alpha Lbar² rho^-4.
//! Pair differences use factored inverse-power differences to avoid subtracting
//! two galactic positions. They are finite geodesics, not a Jacobi/tide RHS.


pub const RADII: [f64; 7] = [1e6, 1e5, 1e4, 1e3, 100.0, 30.0, 10.0];
pub const ECCENTRICITIES: [f64; 3] = [0.0, 0.3, 0.6];
const R: i64 = 1 << 40;
const Q: i64 = 1 << 20;
const EPS: f64 = 1e-5;
const SAMPLES: usize = 400;
const SUBSTEPS: usize = 512;
const PAIR_SCALE: f64 = 1.0 / 16.0;
const ORACLE_TOL: f64 = 1e-5;
const BAND: f64 = 0.01; // E3's band at this initial extent. No new success fraction.
type V = [f64; 3];
type Offset = ([f64; 2], [f64; 2]);

fn metric(a: f64, r: f64, x: V, y: V) -> f64 {
    let f = 1.0 - 2.0 * a / r;
    -f / a * x[0] * y[0] + x[1] * y[1] / f + r * r * x[2] * y[2]
}
// Gamma(u,v), derived directly from the diagonal Schwarzschild metric.
fn connection(a: f64, r: f64, u: V, v: V) -> V {
    let f = 1.0 - 2.0 * a / r;
    let g = a / (r * r * f);
    [
        g * (u[0] * v[1] + u[1] * v[0]),
        f / (r * r) * u[0] * v[0] - g * u[1] * v[1] - f * r * u[2] * v[2],
        (u[1] * v[2] + u[2] * v[1]) / r,
    ]
}
fn rk4(y: &mut [f64], h: f64, rhs: impl Fn(&[f64], &mut [f64])) {
    // Fixed stack storage: reference, two axes, six nearby geodesics = 34 words.
    let mut k1 = [0.0; 34];
    let mut k2 = k1;
    let mut k3 = k1;
    let mut k4 = k1;
    let mut z = k1;
    let len = y.len();
    rhs(y, &mut k1[..len]);
    for i in 0..len {
        z[i] = y[i] + h * k1[i] / 2.0;
    }
    rhs(&z[..len], &mut k2[..len]);
    for i in 0..len {
        z[i] = y[i] + h * k2[i] / 2.0;
    }
    rhs(&z[..len], &mut k3[..len]);
    for i in 0..len {
        z[i] = y[i] + h * k3[i];
    }
    rhs(&z[..len], &mut k4[..len]);
    for i in 0..len {
        y[i] += h / 6.0 * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]);
    }
}
fn vector(y: &[f64], i: usize) -> V {
    [y[i], y[i + 1], y[i + 2]]
}
fn inv_diff(r: f64, d: f64, power: i32) -> f64 {
    let b = r + d;
    let sum = (0..power)
        .map(|j| r.powi(j) * b.powi(power - 1 - j))
        .sum::<f64>();
    -d * sum / (r.powi(power) * b.powi(power))
}
#[derive(Clone)]
struct Pair {
    de: f64,
    dl: f64,
}
struct System {
    a: f64,
    energy: f64,
    angular: f64,
    pairs: Vec<Pair>,
}
impl System {
    fn tangent(&self, y: &[f64]) -> V {
        [
            self.energy / (1.0 - 2.0 * self.a / y[0]),
            y[1],
            self.angular / y[0].powi(2),
        ]
    }
    fn rhs(&self, y: &[f64], dy: &mut [f64]) {
        let (r, w, a, l) = (y[0], y[1], self.a, self.angular);
        let f = 1.0 - 2.0 * a / r;
        dy[0] = w;
        dy[1] = -1.0 / r.powi(2) + l * l / r.powi(3) - 3.0 * a * l * l / r.powi(4);
        let u = self.tangent(y);
        dy[2] = u[0];
        dy[3] = u[2];
        for start in [4, 7] {
            let g = connection(a, r, u, vector(y, start));
            for c in 0..3 {
                dy[start + c] = -g[c];
            }
        }
        for (i, p) in self.pairs.iter().enumerate() {
            let j = 10 + 4 * i;
            let (d, b) = (y[j], r + y[j]);
            let fb = 1.0 - 2.0 * a / b;
            let dl2 = p.dl * (2.0 * l + p.dl);
            dy[j] = y[j + 1];
            dy[j + 1] = -inv_diff(r, d, 2) + dl2 / b.powi(3) + l * l * inv_diff(r, d, 3)
                - 3.0 * a * (dl2 / b.powi(4) + l * l * inv_diff(r, d, 4));
            dy[j + 2] = p.de / fb - self.energy * 2.0 * a * d / (r * b * f * fb);
            dy[j + 3] = p.dl / b.powi(2) + l * inv_diff(r, d, 2);
        }
    }
}
// Exponential-map initial separation, and parallel transport of the initial 4-velocity
// along that spacelike geodesic. No coordinate-distance initialisation shortcut.
fn displaced(a: f64, u: V, axes: [V; 2], x: [f64; 2], v: [f64; 2]) -> (V, V) {
    let mut y = [0.0; 9];
    y[1] = 1.0;
    for c in 0..3 {
        y[3 + c] = x[0] * axes[0][c] + x[1] * axes[1][c];
        y[6 + c] = u[c] + v[0] * axes[0][c] + v[1] * axes[1][c];
    }
    // Enforce unit timelike norm before transporting the added local velocity.
    let rescale = (-1.0 / (a * metric(a, 1.0, vector(&y, 6), vector(&y, 6)))).sqrt();
    for c in 0..3 {
        y[6 + c] *= rescale;
    }
    for _ in 0..16 {
        rk4(&mut y, 1.0 / 16.0, |z, dz| {
            dz[..3].copy_from_slice(&z[3..6]);
            let eta = vector(z, 3);
            let gg = connection(a, z[1], eta, eta);
            let gu = connection(a, z[1], eta, vector(z, 6));
            for c in 0..3 {
                dz[3 + c] = -gg[c];
                dz[6 + c] = -gu[c];
            }
        });
    }
    (vector(&y, 0), vector(&y, 6))
}
fn initial(a: f64, e: f64, offsets: &[Offset], scale: f64) -> (System, Vec<f64>) {
    let p = (1.0 + e) / a;
    let energy = (((p - 2.0).powi(2) - 4.0 * e * e) / (p * (p - 3.0 - e * e))).sqrt();
    let angular = ((1.0 + e) / (1.0 - (3.0 + e * e) * a / (1.0 + e))).sqrt();
    let f = 1.0 - 2.0 * a;
    let u = [energy / f, 0.0, angular];
    let axes = [
        [0.0, f.sqrt(), 0.0],
        [a * angular / f.sqrt(), 0.0, energy / f.sqrt()],
    ];
    let mut y = vec![1.0, 0.0, 0.0, 0.0];
    y.extend(axes[0]);
    y.extend(axes[1]);
    let mut pairs = Vec::new();
    for &(x, v) in offsets {
        for sign in [scale, -scale] {
            let (z, vel) = displaced(a, u, axes, x.map(|c| c * sign), v.map(|c| c * sign));
            let r = z[1];
            pairs.push(Pair {
                de: (1.0 - 2.0 * a / r) * vel[0] - energy,
                dl: r * r * vel[2] - angular,
            });
            y.extend([r - 1.0, vel[1], z[0], z[2]]);
        }
    }
    (
        System {
            a,
            energy,
            angular,
            pairs,
        },
        y,
    )
}
fn period(a: f64, e: f64) -> f64 {
    if e == 0.0 {
        return std::f64::consts::TAU * (1.0 - 3.0 * a).sqrt();
    }
    // Darwin anomaly quadrature of proper radial period, independent of crates/space.
    let p = (1.0 + e) / a;
    let points = 4096;
    let h = std::f64::consts::TAU / points as f64;
    (0..=points)
        .map(|i| {
            let c = (i as f64 * h).cos();
            let weight = if i == 0 || i == points {
                1.0
            } else if i % 2 == 0 {
                2.0
            } else {
                4.0
            };
            weight * (1.0 + e).powf(1.5) * ((p - 3.0 - e * e) / (p - 6.0 - 2.0 * e * c)).sqrt()
                / (1.0 + e * c).powi(2)
        })
        .sum::<f64>()
        * h
        / 3.0
}
struct Truth {
    samples: Vec<Vec<[f64; 2]>>,
    invariant: f64,
}
fn oracle(a: f64, e: f64, offsets: &[Offset], stride: f64, steps: usize, scale: f64) -> Truth {
    let (sys, mut y) = initial(a, e, offsets, scale);
    let mut out = Vec::with_capacity(SAMPLES + 1);
    let mut invariant = 0.0f64;
    for j in 0..=SAMPLES {
        let axes = [vector(&y, 4), vector(&y, 7)];
        let u = sys.tangent(&y);
        for k in 0..2 {
            invariant = invariant.max((metric(a, y[0], axes[k], axes[k]) - 1.0).abs());
            invariant = invariant.max((a.sqrt() * metric(a, y[0], u, axes[k])).abs());
        }
        invariant = invariant.max(metric(a, y[0], axes[0], axes[1]).abs());
        invariant = invariant.max((a * metric(a, y[0], u, u) + 1.0).abs());
        for (i, pair) in sys.pairs.iter().enumerate() {
            let j = 10 + 4 * i;
            let r = y[0] + y[j];
            let v = [
                (sys.energy + pair.de) / (1.0 - 2.0 * a / r),
                y[1] + y[j + 1],
                (sys.angular + pair.dl) / (r * r),
            ];
            invariant = invariant.max((a * metric(a, r, v, v) + 1.0).abs());
        }
        let mut members = Vec::new();
        for i in 0..offsets.len() {
            let plus = 10 + 8 * i;
            let minus = plus + 4;
            // Odd finite difference rejects quadratic coordinate/simultaneity error.
            // Projection removes separation along u; refining scale checks higher orders.
            let delta = [
                (y[plus + 2] - y[minus + 2]) / (2.0 * scale),
                (y[plus] - y[minus]) / (2.0 * scale),
                (y[plus + 3] - y[minus + 3]) / (2.0 * scale),
            ];
            let pos = axes.map(|axis| metric(a, y[0], delta, axis) * R as f64);
            members.push(pos);
            members.push(pos.map(|c| -c));
        }
        out.push(members);
        if j < SAMPLES {
            for _ in 0..steps {
                rk4(&mut y, stride / steps as f64, |z, dz| sys.rhs(z, dz));
            }
        }
    }
    Truth {
        samples: out,
        invariant,
    }
}
fn norm(x: [f64; 2]) -> f64 {
    x[0].hypot(x[1])
}
fn sub(x: [f64; 2], y: [f64; 2]) -> [f64; 2] {
    [x[0] - y[0], x[1] - y[1]]
}
fn errors(got: &[Vec<[f64; 2]>], truth: &[Vec<[f64; 2]>], offsets: &[Offset]) -> (f64, f64) {
    let mut pe = 0.0f64;
    let mut se = pe;
    for (g, t) in got.iter().zip(truth) {
        let mass: f64 = (0..t.len()).map(|i| (1 + i / 2) as f64).sum();
        let centre = |v: &[[f64; 2]]| -> [f64; 2] {
            std::array::from_fn(|c| {
                v.iter()
                    .enumerate()
                    .map(|(i, p)| p[c] * (1 + i / 2) as f64 / mass)
                    .sum()
            })
        };
        let cg = centre(g);
        let ct = centre(t);
        let spread = t.iter().map(|&p| norm(sub(p, ct))).fold(1.0, f64::max);
        for i in 0..t.len() {
            let d = norm(t[i]).max(norm(offsets[i / 2].0) * R as f64).max(1.0);
            let p = norm(sub(g[i], t[i])) / d;
            let s = norm(sub(sub(g[i], cg), sub(t[i], ct))) / spread;
            if !p.is_finite() || !s.is_finite() {
                return (f64::INFINITY, f64::INFINITY);
            }
            pe = pe.max(p);
            se = se.max(s);
        }
    }
    (pe, se)
}
fn fixtures_pub(ratio: f64) -> (u64, f64, Vec<Offset>, ()) {
    let nword = ((1u64 << 60) as f64 * Q as f64 / R as f64 / ratio.sqrt()).round() as u64;
    let n = nword as f64 / (1u64 << 60) as f64;
    let a = (n * R as f64 / Q as f64).powi(2);
    let mut offsets = Vec::new();
    for p in [[1.0, 0.0], [0.35, 0.8], [-0.7, 0.45]] {
        let x = p.map(|c| (c * EPS * R as f64).round() as i64);
        let k = [(-n * x[1] as f64).round() as i64, (-n * x[0] as f64).round() as i64];
        offsets.push((x.map(|c| c as f64 / R as f64), k.map(|c| c as f64 / (n * R as f64))));
    }
    (nword, a, offsets, ())
}

fn main() {
    for (ratio, e) in [(10.0f64, 0.6), (10.0, 0.0), (1e6, 0.0)] {
        let (nword, a, offsets, _) = fixtures_pub(ratio);
        let dt = period(a, e) / 40.0;
        for (scale, tag) in [(1.0/16.0, "s16"), (1.0, "s1"), (1.0/32.0, "s32")] {
            let t0 = std::time::Instant::now();
            let truth = oracle(a, e, &offsets, dt, SUBSTEPS, scale);
            let mut s = format!("{{\"ratio\":{ratio},\"e\":{e},\"tag\":\"{tag}\",\"invariant\":{},\"samples\":[", truth.invariant);
            for (j, members) in truth.samples.iter().enumerate() {
                if j > 0 { s.push(','); }
                s.push('[');
                for (i, m) in members.iter().enumerate() {
                    if i > 0 { s.push(','); }
                    s.push_str(&format!("[{:.17e},{:.17e}]", m[0], m[1]));
                }
                s.push(']');
            }
            s.push_str("]}\n");
            use std::io::Write;
            std::io::stdout().write_all(s.as_bytes()).unwrap();
            eprintln!("done ratio={ratio} e={e} {tag} dt={dt} invariant={} wall={:?} n_epoch_rate={}", truth.invariant, t0.elapsed(), nword);
        }
    }
}
