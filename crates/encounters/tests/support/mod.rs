#![allow(dead_code)]
use emergent_encounters::belt::{make_belt, Rng, Spec};
use emergent_encounters::kepler::{Body, TICKS};
use std::f64::consts::TAU;

pub const EPS: [f64; 5] = [1e-8, 1e-7, 1e-6, 1e-5, 1e-4];
pub const RHO: f64 = 0.003;

pub fn scene(name: &str, seed: u64) -> Vec<Body> {
    let (lo, hi, sigma, keys) = match name {
        "belt" => (1.0, 1.5, 0.025, 0),
        "ring" => (1.0, 1.0025, 0.025, 0),
        "equal" => (1.0, 1.001, 0.01, 3),
        "hot" => (1.0, 1.5, 0.1, 0),
        "fleet" => (1.0, 1.0001, 0.0003, 0),
        _ => panic!("unknown scene"),
    };
    let mut b = make_belt(&Spec {
        name: name.into(),
        n: 16,
        sigma_e: sigma,
        rho: RHO,
        a_lo: lo,
        a_hi: hi,
        keys,
        seed,
        orbits: 4.0,
    });
    if name == "fleet" {
        // A formation with unequal elements and clustered phases, not identical trajectories.
        for (i, x) in b.iter_mut().enumerate() {
            *x = Body::new(x.a, x.e, 0.01 * i as f64, 0.001 * i as f64);
        }
    }
    b
}

pub fn kick(b: Body, t: f64, eps: f64, mode: usize) -> Body {
    let m = b.mean_anomaly(t);
    let (a, e, pom, phase) = match mode % 4 {
        0 => (b.a * (1.0 + eps), b.e, b.pom, 0.0),
        1 => (b.a, (b.e + eps).clamp(0.0, 0.8), b.pom, 0.0),
        2 => (b.a, b.e, b.pom + eps, 0.0),
        _ => (b.a, b.e, b.pom, eps),
    };
    let period = Body::new(a, e, pom, 0.0).period;
    let n = TAU * TICKS / period as f64;
    Body::with_period(period, e, pom, m + pom + phase - n * t)
}

fn rv(bi: &Body, bj: &Body, t: f64) -> (f64, f64, f64) {
    // Halley solver, independent of Newton used by the candidate method. No cone or sections.
    let x = bi.state_halley(t);
    let y = bj.state_halley(t);
    let (dx, dy, vx, vy) = (x[0] - y[0], x[1] - y[1], x[2] - y[2], x[3] - y[3]);
    (dx.hypot(dy), dx * vx + dy * vy, vx.hypot(vy))
}

/// r8 v4's truth construction: conservative advancement on radial overlap, cap 0.002,
/// independent bisection of each derivative sign change, and the 1e-6*rho dip quantum.
/// No candidate filter, integer first-hit query, section, or method refinement is used.
pub fn truth(bi: &Body, bj: &Body, t0: f64, t1: f64) -> Vec<(f64, f64)> {
    if bi.rmin() > bj.rmax() + RHO || bj.rmin() > bi.rmax() + RHO {
        return vec![];
    }
    let vmax = bi.vmax() + bj.vmax();
    let mut t = t0;
    let mut old = rv(bi, bj, t);
    let mut out = Vec::new();
    while t < t1 {
        // Distance is vmax-Lipschitz. Outside 2rho skip only a provably empty interval.
        let h = if old.0 > 2.0 * RHO {
            ((old.0 - 1.5 * RHO) / vmax).min(0.002)
        } else {
            (0.25 * RHO / old.2.max(1e-12)).min(0.002)
        };
        let tn = (t + h).min(t1);
        let new = rv(bi, bj, tn);
        if old.1 < 0.0 && new.1 >= 0.0 {
            let (mut lo, mut hi) = (t, tn);
            for _ in 0..48 {
                let mid = (lo + hi) * 0.5;
                if rv(bi, bj, mid).1 < 0.0 {
                    lo = mid;
                } else {
                    hi = mid;
                }
            }
            let tm = (lo + hi) * 0.5;
            let dm = rv(bi, bj, tm).0;
            if dm < RHO && tm > t0 && tm < t1 {
                let mut h = 0.002;
                let mut dip = false;
                for _ in 0..16 {
                    let l = rv(bi, bj, tm - h);
                    let r = rv(bi, bj, tm + h);
                    if l.0 - dm >= 1e-6 * RHO && r.0 - dm >= 1e-6 * RHO {
                        dip = true;
                        break;
                    }
                    if l.1 > 0.0 || r.1 < 0.0 {
                        break;
                    }
                    h *= 2.0;
                }
                if dip {
                    out.push((tm, dm));
                }
            }
        }
        t = tn;
        old = new;
    }
    out
}

pub fn run<F: FnMut(usize, usize, &Body, &Body, f64, f64, &mut Vec<(f64, f64)>)>(
    name: &str,
    eps: f64,
    mut events: F,
) -> (u64, u64, u64) {
    let mut bodies = scene(name, 20261008);
    let mut rng = Rng(20261009);
    let (mut total, mut misses, mut false_) = (0, 0, 0);
    for seg in 0..4 {
        let t0 = seg as f64 * TAU;
        let t1 = t0 + TAU;
        for (i, b) in bodies.iter_mut().enumerate() {
            if rng.f64() < 0.5 {
                *b = kick(*b, t0, eps, i + seg);
            }
        }
        for i in 0..bodies.len() {
            for j in i + 1..bodies.len() {
                let tr = truth(&bodies[i], &bodies[j], t0, t1);
                let mut got = vec![];
                events(i, j, &bodies[i], &bodies[j], t0, t1, &mut got);
                // Same segment-edge margin in both paths. A kick can replace a minimum at the edge.
                let inside = |t: f64| t > t0 + 0.002 && t < t1 - 0.002;
                for &(t, _) in tr.iter().filter(|x| inside(x.0)) {
                    total += 1;
                    misses += (!got.iter().any(|x| (x.0 - t).abs() < 1e-6)) as u64;
                }
                for &(t, d) in got.iter().filter(|x| inside(x.0)) {
                    // Apply the frozen dip definition to the method as well.
                    if rv(&bodies[i], &bodies[j], t - 0.002).0 - d < 1e-6 * RHO
                        || rv(&bodies[i], &bodies[j], t + 0.002).0 - d < 1e-6 * RHO
                    {
                        continue;
                    }
                    false_ += (!tr.iter().any(|x| (x.0 - t).abs() < 1e-6)) as u64;
                }
            }
        }
    }
    (total, misses, false_)
}
