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

pub(crate) fn shapiro_quad_leg(r0: f64, r: f64) -> f64 {
    // η=acosh(r/r0), u=(1/r0) sech η removes the square-root turning singularity.
    // Integrate dt/dη - d[sqrt(r²-r0²)]/dη directly, rationalizing the subtraction.
    let eps = 1.0 / r0;
    let end = (r / r0).acosh();
    integrate_gl(0.0, end, 16, 32, |eta| {
        let x = 1.0 / eta.cosh();
        let q = x + 1.0 / (1.0 + x);
        let root = (1.0 - 2.0 * eps).sqrt();
        let y = (1.0 - 2.0 * eps * x) * (1.0 - 2.0 * eps * q).sqrt();
        // (root²-y²)/(eps*x), factored exactly before evaluation.
        let numerator =
            2.0 * (2.0 + 3.0 * x) / (1.0 + x) - 4.0 * eps * (x + 2.0 * q) + 8.0 * eps * eps * x * q;
        numerator / (y * (root + y))
    })
}

fn shapiro_series_leg(r0: f64, r: f64) -> (f64, f64, f64) {
    // Fixed-turning-radius excess: 2 acosh(R/r0)+tanh[acosh(R/r0)/2] at 1PM.
    // Its distant-endpoint limit is 2 ln(2R/r0)+1, not just the logarithm.
    // The 2PM coefficient is the integral of the Taylor coefficient of dt/dη;
    // at R→∞ it tends to (15π/4-2)/r0 per leg.
    let end = (r / r0).acosh();
    let first = 2.0 * end + (0.5 * end).tanh();
    let second = integrate_gl(0.0, end, 8, 32, |eta| {
        let x = 1.0 / eta.cosh();
        1.5 * x * (4.0 + 8.0 * x + 5.0 * x * x) / (1.0 + x).powi(2)
    }) / r0;
    let log = 2.0 * (2.0 * r / r0).ln();
    (first + second, log, first - log + second)
}

fn rk4<const N: usize, F: Fn([f64; N]) -> [f64; N]>(y: [f64; N], h: f64, f: &F) -> [f64; N] {
    let k1 = f(y);
    let k2 = f(std::array::from_fn(|i| y[i] + 0.5 * h * k1[i]));
    let k3 = f(std::array::from_fn(|i| y[i] + 0.5 * h * k2[i]));
    let k4 = f(std::array::from_fn(|i| y[i] + h * k3[i]));
    std::array::from_fn(|i| y[i] + h * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) / 6.0)
}

fn shapiro_ode_time(eps: f64, target: f64) -> f64 {
    // Affine null geodesic with E=1, scaled λ and coordinates by r0:
    // y'=w, w'=(b/r0)²(y-3/r0)/y⁴, T'=1/(1-2/(r0 y)), φ'=(b/r0)/y².
    // The radial acceleration follows independently from the Schwarzschild geodesic equation.
    let beta = 1.0 / (1.0 - 2.0 * eps).sqrt();
    let deriv = |s: [f64; 4]| {
        let y = s[0];
        [
            s[1],
            beta * beta * (y - 3.0 * eps) / y.powi(4),
            1.0 / (1.0 - 2.0 * eps / y),
            beta / y.powi(2),
        ]
    };
    let mut s = [1.0, 0.0, 0.0, 0.0];
    for _ in 0..100_000 {
        let h = 0.01 * s[0];
        let next = rk4(s, h, &deriv);
        if next[0] >= target {
            let (mut lo, mut hi) = (0.0, h);
            for _ in 0..50 {
                let mid = (lo + hi) * 0.5;
                if rk4(s, mid, &deriv)[0] < target {
                    lo = mid;
                } else {
                    hi = mid;
                }
            }
            let finish = rk4(s, (lo + hi) * 0.5, &deriv);
            return finish[2];
        }
        s = next;
    }
    f64::NAN
}

fn shapiro_ode_leg(r0: f64, r: f64) -> f64 {
    // A separately integrated flat null ray cancels the finite-step geometric
    // error at very distant endpoints without sharing the quadrature method.
    let target = r / r0;
    r0 * (shapiro_ode_time(1.0 / r0, target) - shapiro_ode_time(0.0, target))
}

pub(crate) fn bound_constants(p: f64, e: f64) -> (f64, f64) {
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

fn bound_period_ode(p: f64, e: f64) -> (f64, f64) {
    // Independently integrate Binet's timelike equation in φ, plus t and τ.
    let (energy, angular) = bound_constants(p, e);
    let deriv = |s: [f64; 4]| {
        let u = s[0];
        [
            s[1],
            1.0 / (angular * angular) + 3.0 * u * u - u,
            energy / (angular * u * u * (1.0 - 2.0 * u)),
            1.0 / (angular * u * u),
        ]
    };
    let h = 0.001;
    let mut s = [(1.0 + e) / p, 0.0, 0.0, 0.0];
    let mut phi = 0.0;
    let mut seen_negative = false;
    for _ in 0..40_000 {
        let next = rk4(s, h, &deriv);
        if next[1] < 0.0 {
            seen_negative = true;
        }
        if seen_negative && s[1] > 0.0 && next[1] <= 0.0 && phi > PI {
            let (mut lo, mut hi) = (0.0, h);
            for _ in 0..50 {
                let mid = 0.5 * (lo + hi);
                if rk4(s, mid, &deriv)[1] > 0.0 {
                    lo = mid;
                } else {
                    hi = mid;
                }
            }
            let end = rk4(s, 0.5 * (lo + hi), &deriv);
            return (end[2], end[3]);
        }
        s = next;
        phi += h;
    }
    (f64::NAN, f64::NAN)
}

fn bound_series(p: f64, e: f64) -> (f64, f64, f64) {
    // Fixed Darwin p,e: a=p/(1-e²); T_N=2πa^(3/2).
    // Expansion of exact dt/dχ and dτ/dχ gives T_t/T_N=1+3/a and
    // T_τ/T_N=1+3/(2a), with O(a^-2) relative remainders.
    let a = p / (1.0 - e * e);
    let newton = 2.0 * PI * a.powf(1.5);
    (newton, newton * (1.0 + 3.0 / a), newton * (1.0 + 1.5 / a))
}

pub(crate) fn eih_invariants(p: f64, e: f64, nu: f64) -> (f64, f64, f64, f64) {
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

pub(crate) fn damour_deruelle(energy: f64, angular: f64, nu: f64) -> (f64, f64) {
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

fn eih_weak_series(p: f64, e: f64, nu: f64) -> (f64, f64, f64) {
    // Expand the 1PN invariants and n about the Newtonian orbit with the same
    // harmonic turning radii, retaining only O(1/p) relative to Kepler's law.
    let rp = p / (1.0 + e);
    let ra = p / (1.0 - e);
    let j0 = p.sqrt();
    let v0 = p.sqrt() / rp;
    let correction = |r: f64| {
        -(1.0 - 3.0 * nu) * j0.powi(4) / (8.0 * r.powi(4))
            - (3.0 + nu) * j0 * j0 / (2.0 * r.powi(3))
            + 1.0 / (2.0 * r * r)
    };
    let dj = -(correction(rp) - correction(ra)) / (j0 * (1.0 / (rp * rp) - 1.0 / (ra * ra)));
    let dv = dj / rp - v0 * (0.5 * (1.0 - 3.0 * nu) * j0 * j0 / (rp * rp) + (3.0 + nu) / rp);
    let e0 = 0.5 * v0 * v0 - 1.0 / rp;
    let e1 = v0 * dv
        + 0.375 * (1.0 - 3.0 * nu) * v0.powi(4)
        + 0.5 / rp * ((3.0 + nu) * v0 * v0 + 1.0 / rp);
    let q0 = -2.0 * e0;
    let q1 = -2.0 * e1;
    let newton = 2.0 * PI / (q0.powf(1.5));
    let period = newton * (1.0 - 1.5 * q1 / q0 + q0 * (15.0 - nu) / 8.0);
    (6.0 * PI / p, newton, period)
}

fn eih_ode(p: f64, e: f64, nu: f64) -> (f64, f64) {
    let (rp, vt, _, _) = eih_invariants(p, e, nu);
    // Relative EIH equation in the harmonic centre-of-mass frame, 1PN:
    // a = -n/r² + [n((4+2ν)/r-(1+3ν)v²+3ν rdot²/2)
    //                +(4-2ν)rdot v]/r².
    // Source: Blanchet, Living Rev. Relativity 17, 2 (2014),
    // https://www.kurims.kyoto-u.ac.jp/EMIS/journals/LRG/Articles/lrr-2014-2/
    let deriv = |s: [f64; 5]| {
        let (x, y, vx, vy) = (s[0], s[1], s[2], s[3]);
        let r = (x * x + y * y).sqrt();
        let rd = (x * vx + y * vy) / r;
        let v2 = vx * vx + vy * vy;
        let radial = -1.0 + (4.0 + 2.0 * nu) / r - (1.0 + 3.0 * nu) * v2 + 1.5 * nu * rd * rd;
        let tangent = (4.0 - 2.0 * nu) * rd;
        [
            vx,
            vy,
            (radial * x / r + tangent * vx) / (r * r),
            (radial * y / r + tangent * vy) / (r * r),
            (x * vy - y * vx) / (r * r),
        ]
    };
    let a = p / (1.0 - e * e);
    let h = 2.0 * PI * a.powf(1.5) / 20_000.0;
    let mut s = [rp, 0.0, 0.0, vt, 0.0];
    let mut t = 0.0;
    let mut seen_negative = false;
    for _ in 0..60_000 {
        let next = rk4(s, h, &deriv);
        let rd0 = s[0] * s[2] + s[1] * s[3];
        let rd1 = next[0] * next[2] + next[1] * next[3];
        if rd1 < 0.0 {
            seen_negative = true;
        }
        if seen_negative && rd0 < 0.0 && rd1 >= 0.0 {
            let (mut lo, mut hi) = (0.0, h);
            for _ in 0..48 {
                let mid = 0.5 * (lo + hi);
                let z = rk4(s, mid, &deriv);
                if z[0] * z[2] + z[1] * z[3] < 0.0 {
                    lo = mid;
                } else {
                    hi = mid;
                }
            }
            let end = rk4(s, 0.5 * (lo + hi), &deriv);
            return (end[4] - 2.0 * PI, t + 0.5 * (lo + hi));
        }
        s = next;
        t += h;
    }
    (f64::NAN, f64::NAN)
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

pub(super) fn run(rows: &mut Vec<Value>, ok: &mut bool) {
    for (index, &(first, r1, r2)) in SHAPIRO_CASES.iter().enumerate() {
        let r0 = if index == 0 {
            first
        } else {
            null_turning_radius(first)
        };
        let b = r0 / (1.0 - 2.0 / r0).sqrt();
        let quad = shapiro_quad_leg(r0, r1) + shapiro_quad_leg(r0, r2);
        let ode = shapiro_ode_leg(r0, r1) + shapiro_ode_leg(r0, r2);
        let (s1, l1, c1) = shapiro_series_leg(r0, r1);
        let (s2, l2, c2) = shapiro_series_leg(r0, r2);
        let series = s1 + s2;
        let methods = rel(ode, quad);
        let series_diff = rel(series, quad);
        let pass = methods < SHAPIRO_METHOD_REL_BAND
            && (r0 < 30.0 || series_diff < SHAPIRO_SERIES_REL_COEFF / (r0 * r0));
        *ok &= pass;
        rows.push(json!({"case":"shapiro_delay","r0":r0,"b":b,"r1":r1,"r2":r2,
            "quadrature_one_way":quad,"ode_one_way":ode,"series_one_way":series,
            "quadrature_round_trip":2.0*quad,"ode_round_trip":2.0*ode,"series_round_trip":2.0*series,
            "leading_log":l1+l2,"finite_endpoint_and_2pm_correction":c1+c2,
            "methods_rel_diff":methods,"quadrature_series_rel_diff":series_diff,
            "ode_series_rel_diff":rel(series,ode),"pass":pass}));
    }
    for &(p, e) in BOUND_PERIOD_CASES {
        let (qt, qtau) = bound_period_quad(p, e);
        let (ot, otau) = bound_period_ode(p, e);
        let (newton, st, stau) = bound_series(p, e);
        let mt = rel(ot, qt);
        let mta = rel(otau, qtau);
        let st_diff = rel(st, qt);
        let sta_diff = rel(stau, qtau);
        let pass = mt < PERIOD_METHOD_REL_BAND
            && mta < PERIOD_METHOD_REL_BAND
            && (p < 100.0
                || (st_diff < PERIOD_SERIES_REL_COEFF / (p * p)
                    && sta_diff < PERIOD_SERIES_REL_COEFF / (p * p)));
        *ok &= pass;
        rows.push(json!({"case":"bound_period","p":p,"e":e,"newtonian":newton,
            "quadrature_coordinate":qt,"ode_coordinate":ot,"series_coordinate":st,
            "quadrature_proper":qtau,"ode_proper":otau,"series_proper":stau,
            "coordinate_methods_rel_diff":mt,"proper_methods_rel_diff":mta,
            "coordinate_series_rel_diff":st_diff,"proper_series_rel_diff":sta_diff,
            "ode_coordinate_series_rel_diff":rel(st,ot),"ode_proper_series_rel_diff":rel(stau,otau),"pass":pass}));
    }
    for &p in EIH_P {
        for &e in EIH_E {
            for &nu in EIH_NU {
                let (_, _, energy, angular) = eih_invariants(p, e, nu);
                let (dd_advance, dd_period) = damour_deruelle(energy, angular, nu);
                let (ode_advance, ode_period) = eih_ode(p, e, nu);
                let (series_advance, newton, series_period) = eih_weak_series(p, e, nu);
                let advance_diff = rel(ode_advance, dd_advance);
                let period_diff = rel(ode_period, dd_period);
                let pass = advance_diff < EIH_ADVANCE_REL_COEFF / p
                    && period_diff < EIH_PERIOD_REL_COEFF / (p * p);
                *ok &= pass;
                rows.push(json!({"case":"eih_1pn","p":p,"e":e,"nu":nu,
            "dd_advance":dd_advance,"ode_advance":ode_advance,"series_advance":series_advance,
            "dd_radial_period":dd_period,"ode_radial_period":ode_period,"newtonian_period":newton,
            "series_radial_period":series_period,
            "advance_methods_rel_diff":advance_diff,"period_methods_rel_diff":period_diff,
            "dd_advance_series_rel_diff":rel(series_advance,dd_advance),
            "ode_advance_series_rel_diff":rel(series_advance,ode_advance),
            "dd_period_series_rel_diff":rel(series_period,dd_period),
                    "ode_period_series_rel_diff":rel(series_period,ode_period),"pass":pass}));
                if nu == 0.0 {
                    let (sp, se) = schwarzschild_from_invariants(energy, angular, p);
                    let sch_advance = periapsis_elliptic(sp, se);
                    let (sch_period, _) = bound_period_quad(sp, se);
                    let ad = rel(ode_advance, sch_advance);
                    let td = rel(ode_period, sch_period);
                    let cross_pass =
                        ad < TEST_MASS_1PN_REL_COEFF / p && td < PERIOD_SERIES_REL_COEFF / (p * p);
                    *ok &= cross_pass;
                    rows.push(json!({"case":"eih_test_mass_limit","p":p,"e":e,
                        "matched_schwarzschild_p":sp,"matched_schwarzschild_e":se,
                        "eih_advance":ode_advance,"schwarzschild_advance":sch_advance,
                        "eih_period":ode_period,"schwarzschild_period":sch_period,
                        "advance_rel_diff":ad,"period_rel_diff":td,"pass":cross_pass}));
                }
            }
        }
    }
    // Match invariant E in the ν=0 quasi-Keplerian period to the exact test-mass
    // Schwarzschild E-1, and compare the gauge-invariant advance at the same p,e.
    for &(p, e) in BOUND_PERIOD_CASES {
        if p < 100.0 {
            continue;
        }
        let (es, l) = bound_constants(p, e);
        let (advance, period) = damour_deruelle(es - 1.0, l, 0.0);
        let (exact_period, _) = bound_period_quad(p, e);
        let exact_advance = periapsis_elliptic(p, e);
        let ad = rel(advance, exact_advance);
        let td = rel(period, exact_period);
        let pass = ad < TEST_MASS_1PN_REL_COEFF / p && td < PERIOD_SERIES_REL_COEFF / (p * p);
        *ok &= pass;
        rows.push(json!({"case":"test_mass_1pn_limit","p":p,"e":e,
            "dd_advance":advance,"schwarzschild_advance":exact_advance,
            "dd_period":period,"schwarzschild_period":exact_period,
            "advance_rel_diff":ad,"period_rel_diff":td,"pass":pass}));
    }
}
