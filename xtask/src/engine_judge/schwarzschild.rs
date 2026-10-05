//! Independent Schwarzschild geodesic pairs, not the engine's tide or orbit compiler.
//! Coordinates (s=t sqrt(M/rp³), rho=r/rp, phi), lambda=tau sqrt(M/rp³).
//! Metric/rp² = diag(-f/alpha, 1/f, rho²), f=1-2alpha/rho, alpha=M/rp.
//! Affine radial ODE follows normalization and the two Killing constants:
//! rho''=-rho^-2 + Lbar² rho^-3 - 3alpha Lbar² rho^-4.
//! Pair differences use factored inverse-power differences to avoid subtracting
//! two galactic positions. They are finite geodesics, not a Jacobi/tide RHS.
use super::scene::world;
use emergent_engine::{AnchorPolicy, Battle, Frame};
use emergent_lattice::{Body, Kickable, Response};
use emergent_lattice_event::EventCore;
use serde_json::json;

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
fn fixtures(ratio: f64) -> (u64, f64, Vec<Offset>, Vec<Body>) {
    // Physical c=Q; mu=n²R³, so alpha=mu/(R c²). Quantisation is reported.
    let nword = ((1u64 << 60) as f64 * Q as f64 / R as f64 / ratio.sqrt()).round() as u64;
    let n = nword as f64 / (1u64 << 60) as f64;
    let a = (n * R as f64 / Q as f64).powi(2);
    let mut bodies = Vec::new();
    let mut offsets = Vec::new();
    for (i, p) in [[1.0, 0.0], [0.35, 0.8], [-0.7, 0.45]]
        .into_iter()
        .enumerate()
    {
        let x = p.map(|c| (c * EPS * R as f64).round() as i64);
        let k = [
            (-n * x[1] as f64).round() as i64,
            (-n * x[0] as f64).round() as i64,
        ];
        offsets.push((
            x.map(|c| c as f64 / R as f64),
            k.map(|c| c as f64 / (n * R as f64)),
        ));
        for sign in [1, -1] {
            bodies.push(Body::new(
                bodies.len() as u64 + 1,
                x.map(|c| c * sign),
                k.map(|c| c * sign),
                i as i64 + 1,
                1,
                Response::Pass,
            ));
        }
    }
    (nword, a, offsets, bodies)
}
fn engine(n: u64, e: f64, bodies: Vec<Body>, stride: i64) -> Result<Vec<Vec<[f64; 2]>>, String> {
    let f = Frame::on_orbit(Q, R, n, (e * (1u64 << 48) as f64).round() as u64, 0, 0)
        .map_err(|e| e.to_string())?;
    let mut b = Battle::new(
        EventCore::new(world(bodies, Q), false).map_err(|e| format!("{e:?}"))?,
        f,
        1,
    )
    .with_anchoring(AnchorPolicy {
        age_epochs: 8,
        enforce_orbit_rule: false,
    })
    .map_err(|e| e.to_string())?;
    let mut out = Vec::new();
    let mut m = Vec::new();
    for j in 0..=SAMPLES {
        b.run_to(j as i64 * stride).map_err(|e| e.to_string())?;
        // Every reading settles the integer position debt. Balanced +/- members
        // keep the origin fixed; any recentring invalidates this isolated tide test.
        let rep = b.reanchor().map_err(|e| e.to_string())?;
        if rep.refused
            || rep.centre != [0, 0]
            || rep.velocity != [0, 0]
            || b.stats().handed_out != 0
        {
            return Err(format!(
                "behaviour:frame_not_fixed centre={:?} velocity={:?} refused={} leavers={}",
                rep.centre,
                rep.velocity,
                rep.refused,
                b.stats().handed_out
            ));
        }
        b.stepper().motions(&mut m);
        out.push(m.iter().map(|m| m.x.map(|x| x as f64)).collect());
    }
    Ok(out)
}

// Independent circular Jacobi control. In a parallel frame the radial direction
// turns by lambda, not by the Schwarzschild azimuth. The radial stretching is
// 3 gamma^2 - 1 (minus the curvature eigenvalue); tangential compression is -1.
// This path shares no geodesic-pair RHS/connection with the oracle above.
fn circular_tide_trace(
    offsets: &[Offset],
    dt: f64,
    stretch: f64,
    sign: f64,
    frozen: bool,
) -> Vec<Vec<[f64; 2]>> {
    let mut traces = vec![Vec::new(); SAMPLES + 1];
    for &(x, v) in offsets {
        let mut y = [x[0], x[1], v[0], v[1], 0.0];
        for (j, trace) in traces.iter_mut().enumerate() {
            let p = [y[0] * R as f64, y[1] * R as f64];
            trace.push(p);
            trace.push(p.map(|c| -c));
            if j == SAMPLES {
                break;
            }
            for _ in 0..SUBSTEPS {
                rk4(&mut y, dt / SUBSTEPS as f64, |z, dz| {
                    let (s, c) = if frozen { (0.0, 1.0) } else { z[4].sin_cos() };
                    dz[0] = z[2];
                    dz[1] = z[3];
                    dz[2] = sign
                        * (((stretch + 1.0) * c * c - 1.0) * z[0] + (stretch + 1.0) * c * s * z[1]);
                    dz[3] = sign
                        * ((stretch + 1.0) * c * s * z[0] + ((stretch + 1.0) * s * s - 1.0) * z[1]);
                    dz[4] = 1.0;
                });
            }
        }
    }
    traces
}

fn gr_discrimination() -> (bool, String) {
    let mut rows = Vec::new();
    let mut valid = true;
    let mut positive = true;
    let mut killed = 0;
    // Existing spectrum radii; circle is stable at both. Hold the correct GR
    // origin, proper clock and parallel axes fixed while replacing only the tide.
    for ratio in [100.0, 10.0] {
        let (nword, a, offsets, _) = fixtures(ratio);
        let n = nword as f64 / (1u64 << 60) as f64;
        let dt = (period(a, 0.0) / 40.0 / n).round() * n;
        let coarse = oracle(a, 0.0, &offsets, dt, SUBSTEPS / 2, PAIR_SCALE);
        let truth = oracle(a, 0.0, &offsets, dt, SUBSTEPS, PAIR_SCALE);
        let half = oracle(a, 0.0, &offsets, dt, SUBSTEPS, PAIR_SCALE / 2.0);
        let refine = errors(&coarse.samples, &truth.samples, &offsets);
        let separation = errors(&half.samples, &truth.samples, &offsets);
        let invariant = coarse.invariant.max(truth.invariant).max(half.invariant);
        let oracle_ok = [refine.0, refine.1, separation.0, separation.1, invariant]
            .into_iter()
            .all(|v| v.is_finite() && v < ORACLE_TOL);
        valid &= oracle_ok;
        let gamma2 = (1.0 - 2.0 * a) / (1.0 - 3.0 * a);
        for (name, stretch) in [
            ("GR", 3.0 * gamma2 - 1.0),
            ("Newtonian-tide", 2.0),
            ("wrong-Riemann-sign", gamma2 + 1.0),
        ] {
            let got = circular_tide_trace(&offsets, dt, stretch, 1.0, false);
            let (pe, se) = errors(&got, &truth.samples, &offsets);
            let finite = pe.is_finite() && se.is_finite();
            let pass = finite && pe <= BAND && se <= BAND;
            if name == "GR" {
                positive &= oracle_ok && pass;
            } else {
                killed += (oracle_ok && finite && !pass) as usize;
            }
            rows.push(
                json!({"control":name,"scope":"oracle-only circular Jacobi tide",
                "r_per_M_requested":ratio,"r_per_M_actual":1.0/a,"e":0.0,
                "periods":10,"samples":401,"members":6,"band":BAND,
                "position":pe,"shape":se,"pass":pass,"oracle_ok":oracle_ok,
                "oracle_position":refine.0,"oracle_shape":refine.1,
                "finite_separation_position":separation.0,"finite_separation_shape":separation.1,
                "invariant":invariant}),
            );
        }
    }
    let dir =
        std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../artifacts/runs/engine-judge");
    let saved = std::fs::create_dir_all(&dir)
        .and_then(|_| {
            std::fs::write(
                dir.join("schwarzschild-gr-controls.jsonl"),
                rows.iter().map(|v| format!("{v}\n")).collect::<String>(),
            )
        })
        .is_ok();
    (valid && positive && killed == 4 && saved,
        format!("gr_oracle_valid={valid} gr_positive={positive} gr_mutants={killed}/4 gr_evidence_saved={saved}"))
}

const E9_FROZEN: bool = true;
pub fn run(binary: &std::path::Path, weak_control: bool) -> (bool, String) {
    // A candidate gate must never silently qualify before the required red-team.
    // The freeze digest, when admitted, lives in docs/engine-judge.md.
    if !E9_FROZEN {
        return (false,"UNSUPPORTED E9_not_frozen cloud_GLM_redteam_required; oracle checks available via cargo test -p xtask schwarzschild".into());
    }
    let (ok, detail) = frozen_run(weak_control);
    if weak_control {
        return (ok, detail);
    }
    let (gr_ok, gr_detail) = gr_discrimination();
    let mut caught = 0;
    let mut control = false;
    let mut results = Vec::new();
    for name in ["control", "sign-tide", "static-tide"] {
        let mut cmd = std::process::Command::new(binary);
        cmd.args(["engine-judge", "--gates", "E9", "--e9-weak-control"]);
        if name == "control" {
            cmd.env_remove("ENGINE_JUDGE_MUTANT");
        } else {
            cmd.env("ENGINE_JUDGE_MUTANT", name);
        }
        match cmd.output() {
            Ok(o) => {
                let stdout = String::from_utf8_lossy(&o.stdout);
                let line = stdout
                    .lines()
                    .find(|l| l.starts_with("E9 "))
                    .unwrap_or("missing_gate");
                let valid = line.contains("oracle_valid=true")
                    && line.contains("engine_valid=true")
                    && !line.contains("timeout")
                    && !line.contains("panic")
                    && !line.contains("UNSUPPORTED");
                if name == "control" {
                    control = o.status.success() && valid && line.starts_with("E9 PASS ");
                } else {
                    caught +=
                        (control && !o.status.success() && valid && line.starts_with("E9 FAIL "))
                            as usize;
                }
                results.push(format!(
                    "{name}:{line}\n{}\n{}",
                    stdout,
                    String::from_utf8_lossy(&o.stderr)
                ));
            }
            Err(e) => results.push(format!("{name}:unavailable:{e}")),
        }
    }
    let dir =
        std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../artifacts/runs/engine-judge");
    let saved = std::fs::write(dir.join("schwarzschild-mutants.txt"), results.join("\n")).is_ok();
    (
        ok && gr_ok && control && caught == 2 && saved,
        format!("{detail} {gr_detail} weak_control={control} mutants={caught}/2 mutant_evidence_saved={saved}"),
    )
}

// This runner is kept separate from run() so pre-freeze oracle tests cannot touch
// the engine. Once admitted, run() calls this function without changing its bands.
fn frozen_run(weak_control: bool) -> (bool, String) {
    let mut rows = Vec::new();
    let mut passed = 0;
    let mut valid = true;
    let mut frontier = Vec::new();
    let mut engine_valid = true;
    let radii = if weak_control {
        &RADII[..1]
    } else {
        &RADII[..]
    };
    for e in ECCENTRICITIES {
        let mut radii_passed = Vec::new();
        let mut radii_failed = Vec::new();
        for &ratio in radii {
            let (nword, a, offsets, bodies) = fixtures(ratio);
            let n = nword as f64 / (1u64 << 60) as f64;
            let stride = (period(a, e) / 40.0 / n).round() as i64;
            let dt = stride as f64 * n;
            let coarse = oracle(a, e, &offsets, dt, SUBSTEPS / 2, PAIR_SCALE);
            let truth = oracle(a, e, &offsets, dt, SUBSTEPS, PAIR_SCALE);
            let half = oracle(a, e, &offsets, dt, SUBSTEPS, PAIR_SCALE / 2.0);
            let refine = errors(&coarse.samples, &truth.samples, &offsets);
            let separation = errors(&half.samples, &truth.samples, &offsets);
            let invariant = coarse.invariant.max(truth.invariant).max(half.invariant);
            let oracle_ok = [refine.0, refine.1, separation.0, separation.1, invariant]
                .into_iter()
                .all(|x| x.is_finite() && x < ORACLE_TOL);
            valid &= oracle_ok;
            let result = if oracle_ok {
                engine(nword, e, bodies, stride)
            } else {
                Err("oracle_unconverged".into())
            };
            let (pe, se, reason) = match result {
                Ok(got) => {
                    let (pe, se) = errors(&got, &truth.samples, &offsets);
                    (pe, se, String::new())
                }
                Err(e) => {
                    engine_valid &= e.starts_with("behaviour:");
                    (f64::INFINITY, f64::INFINITY, e)
                }
            };
            let ok = oracle_ok && pe <= BAND && se <= BAND && reason.is_empty();
            passed += ok as usize;
            if ok {
                radii_passed.push(ratio);
            } else {
                radii_failed.push(ratio);
            }
            rows.push(json!({"r_per_M_requested":ratio,"r_per_M_actual":1.0/a,"e":e,"periods":10,"samples":401,"members":6,"order":"sparse","band":BAND,"position":pe,"shape":se,"oracle_position":refine.0,"oracle_shape":refine.1,"finite_separation_position":separation.0,"finite_separation_shape":separation.1,"invariant":invariant,"oracle_ok":oracle_ok,"pass":ok,"reason":reason}));
        }
        frontier.push(format!(
            "e={e}:passed={radii_passed:?}:failed={radii_failed:?}"
        ));
    }
    let dir =
        std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../artifacts/runs/engine-judge");
    let filename = if weak_control {
        match std::env::var("ENGINE_JUDGE_MUTANT").as_deref() {
            Ok("sign-tide") => "schwarzschild-weak-sign-tide.jsonl",
            Ok("static-tide") => "schwarzschild-weak-static-tide.jsonl",
            _ => "schwarzschild-weak.jsonl",
        }
    } else {
        "schwarzschild.jsonl"
    };
    let saved = std::fs::create_dir_all(&dir)
        .and_then(|_| {
            std::fs::write(
                dir.join(filename),
                rows.iter().map(|v| format!("{v}\n")).collect::<String>(),
            )
        })
        .is_ok();
    let total = radii.len() * ECCENTRICITIES.len();
    (valid && engine_valid && passed==total && saved,format!("cases={passed}/{total} oracle_valid={valid} engine_valid={engine_valid} evidence_saved={saved} periods=10 band={BAND} {}",frontier.join(" ")))
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn eccentric_radial_period_and_apsidal_angle_match_anomaly_quadrature() {
        for a in [1e-6, 0.1] {
            for e in [0.3, 0.6] {
                let (sys, mut y) = initial(a, e, &[], 1.0);
                let steps = 20000;
                let h = period(a, e) / steps as f64;
                for i in 0..steps {
                    rk4(&mut y, h, |z, dz| sys.rhs(z, dz));
                    if i + 1 == steps / 2 {
                        assert!((y[0] - (1.0 + e) / (1.0 - e)).abs() < 1e-8);
                    }
                }
                assert!((y[0] - 1.0).abs() < 1e-8 && y[1].abs() < 1e-8);
                let p = (1.0 + e) / a;
                let h = std::f64::consts::TAU / 4096.0;
                let angle = (0..=4096)
                    .map(|i| {
                        let weight = if i == 0 || i == 4096 {
                            1.0
                        } else if i % 2 == 0 {
                            2.0
                        } else {
                            4.0
                        };
                        weight * (p / (p - 6.0 - 2.0 * e * (i as f64 * h).cos())).sqrt()
                    })
                    .sum::<f64>()
                    * h
                    / 3.0;
                assert!((y[3] - angle).abs() < 1e-8);
            }
        }
    }
    #[test]
    fn weak_field_positive_and_sign_static_falsifiers_without_engine() {
        let (_, a, offsets, _) = fixtures(1e6);
        let dt = period(a, 0.0) / 40.0;
        let truth = oracle(a, 0.0, &offsets, dt, SUBSTEPS, PAIR_SCALE);
        for (name, sign, frozen) in [
            ("Newtonian", 1.0, false),
            ("sign", -1.0, false),
            ("static", 1.0, true),
        ] {
            let traces = circular_tide_trace(&offsets, dt, 2.0, sign, frozen);
            let err = errors(&traces, &truth.samples, &offsets);
            println!("oracle-only {name} position={} shape={}", err.0, err.1);
            if name == "Newtonian" {
                assert!(err.0 <= BAND && err.1 <= BAND);
            } else {
                assert!(err.0 > BAND || err.1 > BAND);
            }
        }
    }
    #[test]
    fn strong_field_gr_positive_and_planted_wrong_tides() {
        let (ok, detail) = gr_discrimination();
        println!("{detail}");
        assert!(ok, "{detail}");
    }
    #[test]
    fn circular_killing_constants_tetrad_and_radial_epicycle() {
        let a = 0.1;
        let (mut sys, mut y) = initial(a, 0.0, &[], 1.0);
        let delta = 1e-6;
        sys.pairs.push(Pair { de: 0.0, dl: 0.0 });
        y.extend([delta, 0.0, 0.0, 0.0]);
        let kappa = ((1.0 - 6.0 * a) / (1.0 - 3.0 * a)).sqrt();
        for i in 0..=10000 {
            let t = i as f64 * 0.001;
            assert!((y[0] - 1.0).abs() < 1e-12);
            assert!((y[10] / delta - (kappa * t).cos()).abs() < 2e-5);
            let axis = vector(&y, 4);
            assert!((metric(a, y[0], axis, axis) - 1.0).abs() < 1e-10);
            // Parallel axes rotate relative to the radial tetrad by lambda,
            // rather than the azimuth (the geodetic precession control).
            assert!((axis[1] / (1.0 - 2.0 * a).sqrt() - t.cos()).abs() < 1e-10);
            rk4(&mut y, 0.001, |z, dz| sys.rhs(z, dz));
        }
    }
    #[test]
    fn genesis_exponential_map_and_velocity_transport() {
        for ratio in RADII {
            let (_, a, offsets, _) = fixtures(ratio);
            let (sys, y) = initial(a, 0.6, &offsets, 1.0);
            assert!((a * metric(a, 1.0, sys.tangent(&y), sys.tangent(&y)) + 1.0).abs() < 1e-12);
            for i in 0..offsets.len() {
                let j = 10 + 8 * i;
                let d = [
                    (y[j + 2] - y[j + 6]) / 2.0,
                    (y[j] - y[j + 4]) / 2.0,
                    (y[j + 3] - y[j + 7]) / 2.0,
                ];
                for c in 0..2 {
                    let got = metric(a, 1.0, d, vector(&y, 4 + 3 * c));
                    assert!((got - offsets[i].0[c]).abs() < 1e-12);
                }
            }
        }
    }
    #[test]
    fn oracle_refinement_and_finite_separation_controls() {
        for ratio in RADII {
            for e in ECCENTRICITIES {
                let (_, a, offsets, _) = fixtures(ratio);
                let dt = period(a, e) / 40.0;
                let coarse = oracle(a, e, &offsets, dt, SUBSTEPS / 2, PAIR_SCALE);
                let fine = oracle(a, e, &offsets, dt, SUBSTEPS, PAIR_SCALE);
                let half = oracle(a, e, &offsets, dt, SUBSTEPS, PAIR_SCALE / 2.0);
                for (name, other) in [("steps", coarse), ("separation", half)] {
                    let err = errors(&other.samples, &fine.samples, &offsets);
                    println!(
                        "r={ratio} e={e} control={name} position={} shape={} invariant={}",
                        err.0, err.1, other.invariant
                    );
                    assert!(
                        err.0 < ORACLE_TOL && err.1 < ORACLE_TOL && other.invariant < ORACLE_TOL
                    );
                }
            }
        }
    }
}
