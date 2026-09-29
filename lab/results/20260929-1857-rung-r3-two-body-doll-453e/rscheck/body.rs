//! Additional independent GR oracle methods. No engine imports and no external numerical crates.
use super::*;

fn integrate_gl<F: Fn(f64) -> f64>(lo: f64, hi: f64, pieces: usize, n: usize, f: F) -> f64 {
    let nodes = gauss_legendre(n);
    let mut sum = 0.0;
    for j in 0..pieces {
        let a = lo + (hi - lo) * j as f64 / pieces as f64;
        let b = lo + (hi - lo) * (j + 1) as f64 / pieces as f64;
        for &(x, w) in &nodes {
            sum += (b - a) * 0.5 * w * f((a + b) * 0.5 + (b - a) * 0.5 * x);
        }
    }
    sum
}

pub(crate) fn null_turning_radius(b: f64) -> f64 {
    // The outer root of b²=r0²/(1-2/r0); b>3√3.
    let mut r = b - 1.0;
    for _ in 0..40 {
        let f = r * r / (1.0 - 2.0 / r) - b * b;
        let df = 2.0 * r * r * (r - 3.0) / (r - 2.0).powi(2);
        let step = f / df;
        r -= step;
        if step.abs() < 2e-15 * r {
            break;
        }
    }
    r
}

fn bound_constants(p: f64, e: f64) -> (f64, f64) {
    let energy = (((p - 2.0).powi(2) - 4.0 * e * e) / (p * (p - 3.0 - e * e))).sqrt();
    let angular = p / (p - 3.0 - e * e).sqrt();
    (energy, angular)
}

pub(crate) fn bound_period_quad(p: f64, e: f64) -> (f64, f64) {
    // Darwin's r=p/(1+e cos χ). From dφ/dχ=√[p/(p-6-2e cosχ)] and
    // dτ/dφ=r²/L, dt/dτ=E/(1-2/r); E,L are the exact Schwarzschild first integrals.
    // Pieces double until the value converges (H0193): near e = 1 the integrand peaks
    // sharply at apoapsis, which 16 fixed pieces under-resolve (1.8e-5 at e = 0.99996).
    let (energy, angular) = bound_constants(p, e);
    let refine = |f: &dyn Fn(f64) -> f64| {
        let mut pieces = 16;
        let mut v = integrate_gl(0.0, 2.0 * PI, pieces, 32, f);
        while pieces < 1 << 14 {
            pieces *= 2;
            let w = integrate_gl(0.0, 2.0 * PI, pieces, 32, f);
            let done = (w - v).abs() <= 1e-14 * w.abs();
            v = w;
            if done {
                break;
            }
        }
        v
    };
    let t = refine(&|chi: f64| {
        let r = p / (1.0 + e * chi.cos());
        let dphi = (p / (p - 6.0 - 2.0 * e * chi.cos())).sqrt();
        dphi * r * r / angular * energy / (1.0 - 2.0 / r)
    });
    let tau = refine(&|chi: f64| {
        let r = p / (1.0 + e * chi.cos());
        (p / (p - 6.0 - 2.0 * e * chi.cos())).sqrt() * r * r / angular
    });
    (t, tau)
}
fn eih_invariants(p: f64, e: f64, nu: f64) -> (f64, f64, f64, f64) {
    let rp = p / (1.0 + e);
    let ra = p / (1.0 - e);
    let j0 = p.sqrt();
    // Define p,e by the two harmonic radial turning radii. Solve the 1PN
    // energy equality at rp and ra for the angular-momentum correction, then
    // invert the 1PN angular-momentum integral for the periapsis speed.
    let correction = |r: f64| {
        -(1.0 - 3.0 * nu) * j0.powi(4) / (8.0 * r.powi(4))
            - (3.0 + nu) * j0 * j0 / (2.0 * r.powi(3))
            + 1.0 / (2.0 * r * r)
    };
    let dj = -(correction(rp) - correction(ra)) / (j0 * (1.0 / (rp * rp) - 1.0 / (ra * ra)));
    let vt =
        (j0 + dj) / rp * (1.0 - 0.5 * (1.0 - 3.0 * nu) * j0 * j0 / (rp * rp) - (3.0 + nu) / rp);
    let v2 = vt * vt;
    // Harmonic-CM 1PN reduced energy and angular momentum, G M=c=1.
    // Source: Battista & De Falco, Europhys. Lett. 141, 21002 (2023), eq. (2),
    // https://academic.oup.com/epl/article/141/2/acb07e/8765332;
    // also Damour & Deruelle, Ann. Inst. H. Poincare 43, 107 (1985).
    let energy = 0.5 * v2 - 1.0 / rp
        + 0.375 * (1.0 - 3.0 * nu) * v2 * v2
        + 0.5 / rp * ((3.0 + nu) * v2 + 1.0 / rp);
    let angular = rp * vt * (1.0 + 0.5 * (1.0 - 3.0 * nu) * v2 + (3.0 + nu) / rp);
    (rp, vt, energy, angular)
}

fn damour_deruelle(energy: f64, angular: f64, nu: f64) -> (f64, f64) {
    // Damour & Deruelle, Ann. Inst. H. Poincaré 43, 107 (1985), 1PN
    // quasi-Keplerian solution; original source:
    // https://numdam.org/item/AIHPA_1985__43_1_107_0/
    // Mean-motion formula is reproduced explicitly in Iyer's 1PN report:
    // https://luth2.obspm.fr/IHP06/workshops/gwdata/iyer.pdf
    // n=(-2E)^(3/2)[1+(-2E)(-15+ν)/8], K=1+k, k=3/J².
    // E and J are specific reduced conserved energy and angular momentum.
    let q = -2.0 * energy;
    let n = q.powf(1.5) * (1.0 + q * (-15.0 + nu) / 8.0);
    (6.0 * PI / (angular * angular), 2.0 * PI / n)
}
fn schwarzschild_from_invariants(binding_energy: f64, angular: f64, p_guess: f64) -> (f64, f64) {
    // Eliminate e² from the exact E,L formulas and solve the stable, outer
    // bound-orbit root for p. Matching invariants avoids equating harmonic and
    // Schwarzschild radial coordinates in the test-mass comparison.
    let l2 = angular * angular;
    let e2 = (1.0 + binding_energy).powi(2);
    let mut p = p_guess;
    for _ in 0..30 {
        let f = (l2 + 4.0) / p - 8.0 * l2 / (p * p) + 16.0 * l2 / p.powi(3) - e2;
        let df = -(l2 + 4.0) / (p * p) + 16.0 * l2 / p.powi(3) - 48.0 * l2 / p.powi(4);
        let step = f / df;
        p -= step;
        if step.abs() < 2e-14 * p {
            break;
        }
    }
    (p, (p - 3.0 - p * p / l2).sqrt())
}
