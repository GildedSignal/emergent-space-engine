//! Independent weak-field (and strong-field) GR oracle: what any gravity law of the lattice
//! will be judged against. Shares no code with crates/. Units G = c = M = 1 (lengths in GM/c²).
//!
//! Dimension: the game plane is the equatorial slice of 3+1 Schwarzschild, not 2+1 GR. In
//! 2+1 GR a point mass makes only a conical deficit (no Newtonian attraction), while orbits
//! and light rays of 3+1 GR around one mass are planar, so the slice loses nothing.
//!
//! Every quantity comes from two independent methods that must agree, plus its weak-field
//! series as a third check:
//! - periapsis advance per orbit: complete elliptic integral (AGM) vs RK4 on
//!   u'' + u = 1/L² + 3u² (u = 1/r, φ-parametrised), series 6π/p·(1 + (18+e²)/(4p));
//! - light deflection: Gauss–Legendre quadrature of 2∫du/√(1/b² − u² + 2u³) − π vs RK4 on
//!   u'' + u = 3u², series 4/b + 15π/(4b²);
//! - geodetic (de Sitter) precession per circular orbit: closed form 2π(1 − √(1 − 3/r)) vs
//!   RK4 parallel transport of a spin vector with the Schwarzschild Christoffel symbols,
//!   series 3π/r;
//! - clock rates: static √(1 − 2/r), circular orbit √(1 − 3/r) (closed forms; the lattice's
//!   region clocks will be compared with them).
use serde_json::{json, Value};
use std::f64::consts::PI;

// Frozen before the first extended-oracle run.  The strong-field series is diagnostic only:
// its omitted powers are not bounded by a weak-field truncation estimate there.
const SHAPIRO_METHOD_REL_BAND: f64 = 2e-5;
const SHAPIRO_SERIES_REL_COEFF: f64 = 100.0; // /r0², r0 >= 30
const PERIOD_METHOD_REL_BAND: f64 = 2e-7;
const PERIOD_SERIES_REL_COEFF: f64 = 300.0; // /p², p >= 100
const EIH_ADVANCE_REL_COEFF: f64 = 20.0; // /p, finite 2PN residual of 1PN dynamics
const EIH_PERIOD_REL_COEFF: f64 = 100.0; // /p², finite 2PN residual
const TEST_MASS_1PN_REL_COEFF: f64 = 20.0; // /p, 2PN residual relative to 1PN advance

const SHAPIRO_CASES: &[(f64, f64, f64)] = &[
    (4.71e5, 1.0e8, 8.0e8), // Cassini-like Earth/Saturn ranges, solar limb
    (10.0, 1000.0, 1200.0),
    (30.0, 3000.0, 3600.0),
    (100.0, 10000.0, 12000.0),
]; // first entry is r0; the other three are b, converted to r0 by the null turning root
const BOUND_PERIOD_CASES: &[(f64, f64)] = &[
    (20.0, 0.2), (30.0, 0.5), (100.0, 0.2), (1000.0, 0.5), (10000.0, 0.2),
];
const EIH_P: &[f64] = &[100.0, 300.0, 1000.0];
const EIH_E: &[f64] = &[0.2, 0.5];
const EIH_NU: &[f64] = &[0.0, 0.05, 0.1, 0.25];

/// K(m) = ∫₀^{π/2} dθ/√(1 − m sin²θ) by the arithmetic–geometric mean.
fn ellip_k(m: f64) -> f64 {
    let (mut a, mut g) = (1.0f64, (1.0 - m).sqrt());
    for _ in 0..40 {
        let (a1, g1) = ((a + g) / 2.0, (a * g).sqrt());
        if (a1 - g1).abs() <= 1e-17 * a1 {
            a = a1;
            break;
        }
        (a, g) = (a1, g1);
    }
    PI / (2.0 * a)
}

/// K(m) − π/2 without cancellation: the series (π/2)·Σ_{n≥1} ((2n−1)!!/(2n)!!)² mⁿ for small
/// m, the AGM value otherwise (then K − π/2 is not small).
fn ellip_k_minus_half_pi(m: f64) -> f64 {
    if m >= 0.25 {
        return ellip_k(m) - PI / 2.0;
    }
    let (mut c, mut mn, mut sum) = (1.0f64, 1.0f64, 0.0f64);
    for n in 1..200 {
        c *= (2 * n - 1) as f64 / (2 * n) as f64;
        mn *= m;
        let term = c * c * mn;
        sum += term;
        if term < 1e-19 * sum {
            break;
        }
    }
    PI / 2.0 * sum
}

/// Periapsis-to-periapsis angle minus 2π for a bound Schwarzschild orbit of semi-latus
/// rectum p and eccentricity e: Δφ = 4·√(p/d)·K(4e/d) − 2π with d = p − 6 + 2e, written as
/// 4·(√(p/d)·(K − π/2) + (π/2)·(√(p/d) − 1)) so the weak field loses no digits to the 2π.
fn periapsis_elliptic(p: f64, e: f64) -> f64 {
    let d = p - 6.0 + 2.0 * e;
    let s = (p / d).sqrt();
    let s_minus_1 = (6.0 - 2.0 * e) / d / (s + 1.0);
    4.0 * (s * ellip_k_minus_half_pi(4.0 * e / d) + PI / 2.0 * s_minus_1)
}

/// RK4 over φ from periapsis (u = (1+e)/p, u' = 0) to the next periapsis (u' from + to −).
fn periapsis_ode(p: f64, e: f64, steps_per_rad: f64) -> f64 {
    let inv_l2 = (p - 3.0 - e * e) / (p * p);
    let f = |u: f64| inv_l2 + 3.0 * u * u - u;
    let h = 1.0 / steps_per_rad;
    let (mut u, mut v, mut phi) = ((1.0 + e) / p, 0.0f64, 0.0f64);
    let step = |u: f64, v: f64, h: f64| {
        let (k1u, k1v) = (v, f(u));
        let (k2u, k2v) = (v + h / 2.0 * k1v, f(u + h / 2.0 * k1u));
        let (k3u, k3v) = (v + h / 2.0 * k2v, f(u + h / 2.0 * k2u));
        let (k4u, k4v) = (v + h * k3v, f(u + h * k3u));
        (u + h / 6.0 * (k1u + 2.0 * k2u + 2.0 * k3u + k4u), v + h / 6.0 * (k1v + 2.0 * k2v + 2.0 * k3v + k4v))
    };
    let mut seen_positive = false;
    for _ in 0..(20.0 * PI * steps_per_rad) as usize {
        let (u1, v1) = step(u, v, h);
        if v1 > 0.0 {
            seen_positive = true;
        }
        if seen_positive && v > 0.0 && v1 <= 0.0 {
            // Bisect the sub-step for u' = 0.
            let (mut lo, mut hi) = (0.0, h);
            for _ in 0..80 {
                let mid = (lo + hi) / 2.0;
                if step(u, v, mid).1 > 0.0 {
                    lo = mid;
                } else {
                    hi = mid;
                }
            }
            return phi + (lo + hi) / 2.0 - 2.0 * PI;
        }
        (u, v, phi) = (u1, v1, phi + h);
    }
    f64::NAN
}

/// Gauss–Legendre nodes and weights on [−1, 1] (Newton on the Legendre recurrence).
fn gauss_legendre(n: usize) -> Vec<(f64, f64)> {
    (1..=n)
        .map(|i| {
            let mut x = (PI * (i as f64 - 0.25) / (n as f64 + 0.5)).cos();
            let mut dp = 0.0;
            for _ in 0..100 {
                let (mut p0, mut p1) = (1.0, x);
                for k in 2..=n {
                    let p2 = ((2 * k - 1) as f64 * x * p1 - (k - 1) as f64 * p0) / k as f64;
                    (p0, p1) = (p1, p2);
                }
                dp = n as f64 * (x * p1 - p0) / (x * x - 1.0);
                let dx = p1 / dp;
                x -= dx;
                if dx.abs() < 1e-16 {
                    break;
                }
            }
            (x, 2.0 / ((1.0 - x * x) * dp * dp))
        })
        .collect()
}

/// Deflection by quadrature. g(u) = 1/b² − u² + 2u³ has its turning point u0 (Newton from the
/// flat value 1/b). Factoring the root out exactly, g(u) = (u0 − u)·q(u) with
/// q(u) = (u0 + u) − 2(u² + u·u0 + u0²), and u = u0(1 − s²) turn ∫₀^{u0} du/√g into the
/// smooth ∫₀¹ 2√(u0/q) ds, with no cancellation near the turning point. The flat integrand
/// with the same turning point (q_f = u0 + u) integrates to π/2 exactly, so the deflection
/// 2(I − π/2) is integrated directly as 4√u0 · r / (√(q·q_f)·(√q_f + √q)), r = q_f − q.
fn deflection_quadrature(b: f64) -> f64 {
    let mut u0 = 1.0 / b;
    for _ in 0..100 {
        let (h, dh) = (2.0 * u0 * u0 * u0 - u0 * u0 + 1.0 / (b * b), 6.0 * u0 * u0 - 2.0 * u0);
        let step = h / dh;
        u0 -= step;
        if step.abs() <= 1e-17 * u0 {
            break;
        }
    }
    let nodes = gauss_legendre(32);
    let pieces = 64;
    let mut total = 0.0;
    for j in 0..pieces {
        let (a, c) = (j as f64 / pieces as f64, (j + 1) as f64 / pieces as f64);
        for &(x, w) in &nodes {
            let s = (a + c) / 2.0 + (c - a) / 2.0 * x;
            let u = u0 * (1.0 - s * s);
            let (qf, r) = (u0 + u, 2.0 * (u * u + u * u0 + u0 * u0));
            let q = qf - r;
            total += w * (c - a) / 2.0 * 4.0 * u0.sqrt() * r / ((q * qf).sqrt() * (qf.sqrt() + q.sqrt()));
        }
    }
    total
}

/// Deflection by RK4 on u'' + u = 3u² from u = 0, u' = 1/b until u returns to 0.
fn deflection_ode(b: f64, steps_per_rad: f64) -> f64 {
    let f = |u: f64| 3.0 * u * u - u;
    let h = 1.0 / steps_per_rad;
    let step = |u: f64, v: f64, h: f64| {
        let (k1u, k1v) = (v, f(u));
        let (k2u, k2v) = (v + h / 2.0 * k1v, f(u + h / 2.0 * k1u));
        let (k3u, k3v) = (v + h / 2.0 * k2v, f(u + h / 2.0 * k2u));
        let (k4u, k4v) = (v + h * k3v, f(u + h * k3u));
        (u + h / 6.0 * (k1u + 2.0 * k2u + 2.0 * k3u + k4u), v + h / 6.0 * (k1v + 2.0 * k2v + 2.0 * k3v + k4v))
    };
    let (mut u, mut v, mut phi) = (0.0f64, 1.0 / b, 0.0f64);
    for _ in 0..(4.0 * PI * steps_per_rad) as usize {
        let (u1, v1) = step(u, v, h);
        if phi > 1.0 && u1 <= 0.0 {
            let (mut lo, mut hi) = (0.0, h);
            for _ in 0..80 {
                let mid = (lo + hi) / 2.0;
                if step(u, v, mid).0 > 0.0 {
                    lo = mid;
                } else {
                    hi = mid;
                }
            }
            return phi + (lo + hi) / 2.0 - PI;
        }
        (u, v, phi) = (u1, v1, phi + h);
    }
    f64::NAN
}

/// Geodetic precession by parallel transport: RK4 on dS^μ/dτ = −Γ^μ_αβ u^α S^β along the
/// circular equatorial geodesic of radius r; the spin's angle to the radial axis is tracked
/// continuously in the orbiter's rest frame. After one orbit it is −2π√(1 − 3/r) (mod the
/// frame's own turn), so the precession against distant stars is 2π + angle.
fn geodetic_ode(r: f64, steps: usize) -> f64 {
    let omega = r.powf(-1.5);
    let ut = 1.0 / (1.0 - 3.0 / r).sqrt();
    let uphi = omega * ut;
    let (g_tt, g_rr, g_pp) = (-(1.0 - 2.0 / r), 1.0 / (1.0 - 2.0 / r), r * r);
    let (c_ttr, c_rtt, c_rpp, c_prp) = (1.0 / (r * (r - 2.0)), (r - 2.0) / (r * r * r), -(r - 2.0), 1.0 / r);
    let deriv = |s: [f64; 3]| -> [f64; 3] {
        // s = (S^t, S^r, S^φ)
        [-c_ttr * ut * s[1], -c_rtt * ut * s[0] - c_rpp * uphi * s[2], -c_prp * uphi * s[1]]
    };
    let tau = 2.0 * PI / omega / ut;
    let h = tau / steps as f64;
    let mut s = [0.0, 1.0 / g_rr.sqrt(), 0.0];
    // Rest-frame tangential axis: unit, orthogonal to u and to ∂r: e = (A, 0, B) with
    // g_tt A u^t + g_pp B u^φ = 0 and g_tt A² + g_pp B² = 1.
    let (a, bb) = {
        let ratio = -g_pp * uphi / (g_tt * ut); // A = ratio·B
        let bb = 1.0 / (g_tt * ratio * ratio + g_pp).sqrt();
        (ratio * bb, bb)
    };
    let angle = |s: [f64; 3]| {
        let radial = g_rr.sqrt() * s[1];
        let tangential = g_tt * a * s[0] + g_pp * bb * s[2];
        tangential.atan2(radial)
    };
    let (mut prev, mut unwrapped) = (angle(s), 0.0);
    for _ in 0..steps {
        let k1 = deriv(s);
        let k2 = deriv([s[0] + h / 2.0 * k1[0], s[1] + h / 2.0 * k1[1], s[2] + h / 2.0 * k1[2]]);
        let k3 = deriv([s[0] + h / 2.0 * k2[0], s[1] + h / 2.0 * k2[1], s[2] + h / 2.0 * k2[2]]);
        let k4 = deriv([s[0] + h * k3[0], s[1] + h * k3[1], s[2] + h * k3[2]]);
        for i in 0..3 {
            s[i] += h / 6.0 * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]);
        }
        let now = angle(s);
        let mut d = now - prev;
        if d > PI {
            d -= 2.0 * PI;
        } else if d < -PI {
            d += 2.0 * PI;
        }
        unwrapped += d;
        prev = now;
    }
    2.0 * PI + unwrapped
}

fn rel(a: f64, b: f64) -> f64 {
    ((a - b) / b).abs()
}

/// Runs every case; each row carries both methods, their relative disagreement, the series
/// value and whether the row meets its frozen agreement band.
pub fn run() -> (bool, Value) {
    let mut rows = Vec::new();
    let mut ok = true;
    // Periapsis advance. Mercury: p ≈ 3.75e7 (a = 3.92e7 GM☉/c², e = 0.2056).
    for (p, e) in [(20.0, 0.0), (20.0, 0.5), (100.0, 0.2), (1e3, 0.2), (1e3, 0.9), (1e4, 0.5), (1e6, 0.2), (3.75e7, 0.2056)] {
        let ell = periapsis_elliptic(p, e);
        let series = 6.0 * PI / p * (1.0 + (18.0 + e * e) / (4.0 * p));
        // A circular orbit has no periapsis to find: the elliptic form covers it alone.
        let ode = (p <= 1e4 && e > 0.0).then(|| periapsis_ode(p, e, 4000.0));
        // Bands frozen with the oracle: methods agree to 1e-8; the two-term series is
        // O(1/p²) off, so it must be within 60/p² relative (checked only for p ≥ 100).
        let agree = ode.is_none_or(|o| rel(o, ell) < 1e-8);
        let series_ok = p < 100.0 || rel(series, ell) < 60.0 / (p * p);
        ok &= agree && series_ok;
        rows.push(json!({"case": "periapsis_advance", "p": p, "e": e, "elliptic_rad": ell, "ode_rad": ode, "series_rad": series,
            "methods_rel_diff": ode.map(|o| rel(o, ell)), "series_rel_diff": rel(series, ell), "pass": agree && series_ok,
            "arcsec_per_orbit": ell.to_degrees() * 3600.0}));
    }
    // Light deflection. Sun's limb: b ≈ 4.71e5 GM☉/c² (1.75").
    for b in [10.0, 30.0, 100.0, 1e3, 1e4, 4.71e5] {
        let quad = deflection_quadrature(b);
        let series = 4.0 / b + 15.0 * PI / (4.0 * b * b);
        let ode = (b <= 1e4).then(|| deflection_ode(b, 20000.0));
        let agree = ode.is_none_or(|o| rel(o, quad) < 1e-8);
        let series_ok = b < 100.0 || rel(series, quad) < 40.0 / (b * b);
        ok &= agree && series_ok;
        rows.push(json!({"case": "light_deflection", "b": b, "quadrature_rad": quad, "ode_rad": ode, "series_rad": series,
            "methods_rel_diff": ode.map(|o| rel(o, quad)), "series_rel_diff": rel(series, quad), "pass": agree && series_ok,
            "arcsec": quad.to_degrees() * 3600.0}));
    }
    // Geodetic precession per circular orbit. Gravity Probe B: r ≈ 1.58e9 GM⊕/c² (6.6"/yr).
    for r in [8.0f64, 20.0, 100.0, 1e4, 1.58e9] {
        let exact = 2.0 * PI * (1.0 - (1.0 - 3.0 / r).sqrt());
        let exact = if r > 1e6 { 2.0 * PI * (3.0 / r) / (1.0 + (1.0 - 3.0 / r).sqrt()) } else { exact };
        let ode = (r <= 1e4).then(|| geodetic_ode(r, 200_000));
        let series = 3.0 * PI / r;
        let agree = ode.is_none_or(|o| rel(o, exact) < 1e-7);
        let series_ok = r < 100.0 || rel(series, exact) < 3.0 / r;
        ok &= agree && series_ok;
        rows.push(json!({"case": "geodetic_precession", "r": r, "closed_form_rad": exact, "ode_rad": ode, "series_rad": series,
            "methods_rel_diff": ode.map(|o| rel(o, exact)), "series_rel_diff": rel(series, exact), "pass": agree && series_ok}));
    }
    // Clock rates (closed forms: the lattice's region clocks must reproduce them).
    for r in [3.5f64, 6.0, 20.0, 1e3, 1e6] {
        rows.push(json!({"case": "clock_rate", "r": r, "static_dtau_dt": (1.0 - 2.0 / r).sqrt(),
            "circular_orbit_dtau_dt": if r > 3.0 { Some((1.0 - 3.0 / r).sqrt()) } else { None }}));
    }
    (ok, json!(rows))
}
