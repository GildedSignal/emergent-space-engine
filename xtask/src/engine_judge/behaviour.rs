//! Independent inverse-square float64 oracle: kick-drift-kick velocity Verlet.
//! Bands frozen before the first engine run. Numerical refinement is a separate gate
//! condition, not permission to silently widen a behaviour tolerance.
use super::scene::{frame, world, Rng, N, Q, R};
use emergent_engine::{AnchorPolicy, Battle, Frame};
use emergent_lattice::{chronon::Chronon, Body, Kickable, Response, World};
use emergent_lattice_event::EventCore;

const SHORT_TOL: f64 = 0.03;
const LONG_TOL: f64 = 0.01;
const ORACLE_TOL: f64 = 1e-5;
const SUBSTEPS: usize = 2048;
const SAMPLES_PER_PERIOD: i64 = 40;

fn norm(v: [f64; 2]) -> f64 {
    v[0].hypot(v[1])
}
fn sub(a: [f64; 2], b: [f64; 2]) -> [f64; 2] {
    [a[0] - b[0], a[1] - b[1]]
}
fn acceleration(p: [f64; 2]) -> [f64; 2] {
    let r = norm(p);
    [-p[0] / (r * r * r), -p[1] / (r * r * r)]
}
fn verlet(p: &mut [f64; 2], v: &mut [f64; 2], h: f64) {
    let a = acceleration(*p);
    for c in 0..2 {
        v[c] += 0.5 * h * a[c];
        p[c] += h * v[c];
    }
    let a = acceleration(*p);
    for c in 0..2 {
        v[c] += 0.5 * h * a[c];
    }
}
fn oracle(w: &World, stride: i64, samples: usize, substeps: usize) -> Vec<Vec<[f64; 2]>> {
    let n = N as f64 / (1u64 << 60) as f64;
    let h = stride as f64 * n / substeps as f64;
    w.bodies
        .iter()
        .map(|b| {
            let mut p = [1.0 + b.x[0] as f64 / R as f64, b.x[1] as f64 / R as f64];
            let mut v = [
                b.k[0] as f64 / (n * R as f64) - p[1],
                b.k[1] as f64 / (n * R as f64) + p[0],
            ];
            let mut out = Vec::new();
            for j in 0..=samples {
                let t = j as f64 * stride as f64 * n;
                let (s, c) = t.sin_cos();
                out.push([
                    (c * p[0] + s * p[1] - 1.0) * R as f64,
                    (-s * p[0] + c * p[1]) * R as f64,
                ]);
                for _ in 0..substeps {
                    verlet(&mut p, &mut v, h);
                }
            }
            out
        })
        .collect()
}

/// Same release regimes as the builder, with independently seeded group geometry,
/// masses and radial/along-track kicks. `mode`: rest, drift-free epicycle, steady shear,
/// radial impulse, off-axis release. Positions are Cartesian offsets at genesis.
fn release(eps: f64, mode: usize, seed: u64) -> World {
    let mut rng = Rng(seed + 781);
    let bodies = (0..7)
        .map(|i| {
            let x = [
                (eps * R as f64) as i64 + rng.range(-160000, 160000),
                rng.range(-100000, 100000),
            ];
            let k = match mode {
                1 => [0, -x[0] / 8192],
                2 => [0, -3 * x[0] / 32768],
                3 => [97, -33],
                4 => [-61, 43],
                _ => [0, 0],
            };
            Body::new(i + 1, x, k, rng.range(1, 5), 10, Response::Pass)
        })
        .collect();
    world(bodies, Q)
}
fn absolute<S: Kickable>(b: &Battle<S>, tick: i64, x: [i64; 2]) -> [f64; 2] {
    if let Some(t) = b.tube_at(tick) {
        let (s, c) = (t.azimuth as f64 / (1u64 << 60) as f64).sin_cos();
        let p = [
            t.radius as f64 + t.x[0] as f64 / (1u64 << 32) as f64 + x[0] as f64,
            t.x[1] as f64 / (1u64 << 32) as f64 + x[1] as f64,
        ];
        [c * p[0] - s * p[1] - R as f64, s * p[0] + c * p[1]]
    } else {
        [x[0] as f64, x[1] as f64]
    }
}
struct Errors {
    position: f64,
    shape: f64,
    sample: usize,
    member: usize,
    anchors: u64,
    leavers: u64,
}
fn follow<S: Kickable>(
    s: S,
    f: Frame,
    w: &World,
    truth: &[Vec<[f64; 2]>],
    stride: i64,
    anchored: bool,
) -> Errors {
    let mut b = Battle::new(s, f, 1);
    if anchored {
        b = b
            .with_anchoring(AnchorPolicy {
                age_epochs: 8,
                enforce_orbit_rule: true,
            })
            .unwrap();
    }
    let mut err = Errors {
        position: 0.0,
        shape: 0.0,
        sample: 0,
        member: 0,
        anchors: 0,
        leavers: 0,
    };
    let mut motions = Vec::new();
    let mass = w.bodies.iter().map(|b| b.mass as f64).sum::<f64>();
    for j in 0..truth[0].len() {
        let tick = j as i64 * stride;
        b.run_to(tick).unwrap();
        b.stepper().motions(&mut motions);
        let got: Vec<_> = motions.iter().map(|m| absolute(&b, tick, m.x)).collect();
        let mut cg = [0.0; 2];
        let mut ct = [0.0; 2];
        for i in 0..got.len() {
            for c in 0..2 {
                cg[c] += got[i][c] * w.bodies[i].mass as f64 / mass;
                ct[c] += truth[i][j][c] * w.bodies[i].mass as f64 / mass;
            }
        }
        let spread = (0..got.len())
            .map(|i| norm(sub(truth[i][j], ct)))
            .fold(1.0, f64::max);
        for i in 0..got.len() {
            let floor = norm([w.bodies[i].x[0] as f64, w.bodies[i].x[1] as f64]);
            let e = norm(sub(got[i], truth[i][j])) / norm(truth[i][j]).max(floor).max(1.0);
            if !e.is_finite() || e > err.position {
                err.position = e;
                err.sample = j;
                err.member = i;
            }
            let sh = norm(sub(sub(got[i], cg), sub(truth[i][j], ct))) / spread;
            if !sh.is_finite() || sh > err.shape {
                err.shape = sh;
            }
        }
    }
    err.anchors = b.stats().anchors;
    err.leavers = b.stats().handed_out;
    err
}

pub fn behaviour(anchored: bool) -> (bool, String) {
    let cases: Vec<_> = if anchored {
        vec![
            (1e-4, 0, 11),
            (3e-4, 0, 23),
            (-1e-3, 0, 71),
            (1e-3, 0, 7),
            (3e-3, 0, 13),
            (3e-4, 1, 11),
            (1e-3, 1, 7),
            (1e-3, 3, 19),
            (1e-3, 4, 31),
        ]
    } else {
        vec![
            (1e-3, 0, 7),
            (1e-3, 1, 7),
            (1e-3, 2, 7),
            (1e-3, 3, 19),
            (-1e-3, 4, 31),
        ]
    };
    let periods = if anchored { 10 } else { 1 };
    let stride = frame().period() / SAMPLES_PER_PERIOD;
    let samples = (periods * SAMPLES_PER_PERIOD) as usize;
    let mut good = 0;
    let mut total = 0;
    let mut worst = 0.0f64;
    let mut shape = 0.0f64;
    let mut refinement = 0.0f64;
    let mut first = String::new();
    let mut release_worst = 0.0f64;
    let mut anchors = 0;
    for (eps, mode, seed) in cases {
        let w = release(eps, mode, seed);
        let coarse = oracle(&w, stride, samples, SUBSTEPS / 2);
        let truth = oracle(&w, stride, samples, SUBSTEPS);
        for i in 0..w.bodies.len() {
            for j in 0..=samples {
                let scale = norm([w.bodies[i].x[0] as f64, w.bodies[i].x[1] as f64]).max(1.0);
                refinement = refinement.max(norm(sub(coarse[i][j], truth[i][j])) / scale);
            }
        }
        let results = [
            follow(
                Chronon::new(w.clone(), false).unwrap(),
                frame(),
                &w,
                &truth,
                stride,
                anchored,
            ),
            follow(
                EventCore::new(w.clone(), false).unwrap(),
                frame(),
                &w,
                &truth,
                stride,
                anchored,
            ),
        ];
        // First-order band is 1% at eps<=1e-3; 3% at eps=3e-3. Same band
        // for both orders, all samples, all members; no aggregate success threshold.
        let tol = if anchored {
            LONG_TOL.max(10.0 * eps.abs())
        } else {
            SHORT_TOL
        };
        for (order, e) in results.iter().enumerate() {
            total += 1;
            anchors += e.anchors;
            worst = worst.max(e.position);
            shape = shape.max(e.shape);
            if mode == 0 && eps.abs() <= 1e-3 {
                release_worst = release_worst.max(e.position);
            }
            let pass = e.position <= tol
                && (!anchored || e.shape <= tol)
                && e.position.is_finite()
                && e.shape.is_finite()
                && e.leavers == 0;
            good += pass as usize;
            if !pass && first.is_empty() {
                first=format!("eps={eps} mode={mode} seed={seed} order={order} sample={} member={} pos={:.6} shape={:.6} tol={tol}",e.sample,e.member,e.position,e.shape);
            }
        }
    }
    (good==total && refinement<ORACLE_TOL,format!("cases={good}/{total} periods={periods} position={worst:.6} shape={shape:.6} rest={release_worst:.6} tol={} oracle_delta={refinement:.2e} oracle_tol={ORACLE_TOL} anchors={anchors} first={first:?}",if anchored {"0.01(0.03_at_eps0.003)"} else {"0.03"}))
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::f64::consts::TAU;
    #[test]
    fn verlet_circular_orbit_converges_and_is_reversible() {
        fn run(steps: usize) -> [f64; 2] {
            let mut p = [1.0, 0.0];
            let mut v = [0.0, 1.0];
            for _ in 0..steps {
                verlet(&mut p, &mut v, TAU / steps as f64);
            }
            p
        }
        let a = norm(sub(run(2048), [1.0, 0.0]));
        let b = norm(sub(run(4096), [1.0, 0.0]));
        assert!(a / b > 3.9 && a / b < 4.1);
        let mut p = [1.01, 0.03];
        let mut v = [-0.04, 0.97];
        let (p0, v0) = (p, v);
        for _ in 0..1000 {
            verlet(&mut p, &mut v, 0.001);
        }
        for _ in 0..1000 {
            verlet(&mut p, &mut v, -0.001);
        }
        assert!(norm(sub(p, p0)) < 1e-12 && norm(sub(v, v0)) < 1e-12);
    }
}
