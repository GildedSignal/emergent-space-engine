//! B13 assists (docs/law.md; principle 2: behaviours, not continuum fidelity). A ship flies by the
//! planet, and the planet changes its orbit about the star: an assist. The judge measures what the
//! flyby does to the orbit about the star, its energy and angular momentum, and not the raw
//! change of velocity, which mostly measures the star's pull during the flyby.
//!
//! - Seeds: 64 flybys: periapsis q log-uniform in [1.2, 50] planet radii, v∞ uniform in
//!   [1.67e-5, 6.7e-5] (5 to 20 km/s), the incoming asymptote's direction uniform. The ship starts
//!   at 1.5·R_SOI from the planet on the incoming two-body hyperbola (counter-clockwise about the
//!   planet), with the planet's velocity added.
//! - The reference gives t_exit: the first time after it has come within R_SOI that its distance
//!   from the planet exceeds 1.5·R_SOI, looked for within one planet period. A ship that never
//!   comes within R_SOI, or never leaves, is excluded and counted.
//! - The assist is ΔE = E_h(t_exit) − E_h(0) and ΔL likewise, with E_h = v²/2 − (1 − μ)/r and
//!   L_h = x·v_y − y·v_x taken relative to the star's own position and velocity.
//! - Excluded too: a reference that is not converged, meaning ΔE or ΔL differs by more than 1e-4
//!   relative between the tolerances 1e-12 and 1e-13. More than 10% of the 64 excluded, for any
//!   reason, fails the gate.
//! - Oracle domain (5 October, adjudicated): the reference is a point mass, so a seed whose
//!   reference passes within the planet's radius of its centre (closest approach over the span the
//!   reference is integrated, tracked to the periapsis itself) tests nothing a law with a surface can
//!   do. Such a seed is replaced by the next draw (the sampler's stream is prefix-stable, up to
//!   `DRAWS`), so the gate still judges `SEEDS` flybys; the replaced seeds are named in the detail
//!   line, and they count toward no exclusion cap (they are outside the domain, not failures of it).
//! - The law is asked for the ship's state at t_exit. PASS iff at least 99% of the judged flybys
//!   have both |ΔE_law − ΔE_ref| ≤ 0.01·|ΔE_ref| and |ΔL_law − ΔL_ref| ≤ 0.01·|ΔL_ref|.
use super::restricted::{Integrator, Model, Restricted, JUPITER, RTOL, RTOL_FINE};
use super::{sample, Gate, Law};

pub const SEEDS: usize = 64;
/// The most draws the stream is read to find `SEEDS` flybys inside the oracle's domain; fewer found fails the gate.
pub const DRAWS: usize = 256;
/// The ship starts and is followed out to this many sphere-of-influence radii.
pub const START_SOI: f64 = 1.5;
pub const ASSIST_TOL: f64 = 1e-2;
/// The reference's assist must agree between its two tolerances to this, relative.
pub const CONVERGED: f64 = 1e-4;
/// The share of the seeds that may be excluded.
pub const EXCLUDED_MAX: f64 = 0.1;

/// A ship at `START_SOI`·R_SOI from the planet on the incoming hyperbola of periapsis `q` (planet
/// radii), excess speed `v_inf` and incoming asymptote `psi`, with the planet's motion added.
pub fn ship(scene: &Restricted, q: f64, v_inf: f64, psi: f64) -> [f64; 4] {
    let (mu, q) = (scene.mu, q * scene.planet_radius);
    let e = 1.0 + q * v_inf * v_inf / mu;
    let p = q * (1.0 + e);
    let r = START_SOI * scene.soi();
    // The incoming branch: true anomaly −ν with cos ν = (p/r − 1)/e; the asymptote is at −ν∞, cos ν∞ = −1/e.
    let nu = -((p / r - 1.0) / e).acos();
    let angle = psi + (-1.0 / e).acos() + nu;
    let h = (mu * p).sqrt();
    let (radial, along) = (mu / h * e * nu.sin(), h / r);
    let (s, c) = angle.sin_cos();
    scene.barycentric(0.0, &[r * c, r * s, radial * c - along * s, radial * s + along * c])
}

/// What the reference makes of a flyby.
#[derive(Debug, PartialEq)]
pub enum Flyby {
    /// The exit time and the assist (ΔE, ΔL).
    Exit(f64, f64, f64),
    /// It never came within R_SOI, or never left, within a period.
    Never,
    /// The integration gave up.
    Failed,
}

/// The reference on `ship` to tolerance `rtol`, and its closest approach to the planet's centre over
/// the span it was integrated (to the exit, or to wherever it stopped).
pub fn reference(scene: &Restricted, ship: [f64; 4], rtol: f64) -> (Flyby, f64) {
    let mut it = Integrator::new(scene, Model::Full, rtol, ship).tracking();
    let horizon = scene.period();
    let (soi, before) = (scene.soi(), scene.heliocentric(0.0, &ship));
    let exit = it.until_crossing(soi, false, horizon).and_then(|_| it.until_crossing(START_SOI * soi, true, horizon));
    let flyby = match exit {
        Some(t) => {
            let after = scene.heliocentric(t, &it.state());
            Flyby::Exit(t, after.0 - before.0, after.1 - before.1)
        }
        // The step size collapsing shows as a time short of the horizon; running out of time shows as the horizon.
        None if it.time() >= horizon => Flyby::Never,
        None => Flyby::Failed,
    };
    (flyby, it.closest())
}

/// |a − b|/|b|, and 0 when they are equal (also at 0). NaN in, NaN out.
fn rel_err(a: f64, b: f64) -> f64 {
    if a == b {
        0.0
    } else {
        (a - b).abs() / b.abs()
    }
}

pub fn b13(law: &dyn Law) -> Gate {
    let _quiet = super::scale::QUIET.read().unwrap_or_else(|e| e.into_inner());
    let scene = JUPITER;
    let (mut ok, mut judged, mut never, mut unconverged) = (0, 0, 0, 0);
    let (mut worst_e, mut worst_l) = (0.0f64, 0.0f64);
    // The seeds replaced because their reference passes inside the planet: (draw, closest approach in planet radii).
    let (mut inside, mut taken) = (Vec::new(), 0);
    for (i, (q, v_inf, psi)) in sample::flybys(DRAWS).into_iter().enumerate() {
        if taken == SEEDS {
            break;
        }
        let s = ship(&scene, q, v_inf, psi);
        let (flyby, closest) = reference(&scene, s, RTOL);
        if closest < scene.planet_radius {
            inside.push((i, closest / scene.planet_radius));
            continue;
        }
        taken += 1;
        let Flyby::Exit(t, de, dl) = flyby else {
            never += 1;
            continue;
        };
        let converged = matches!(reference(&scene, s, RTOL_FINE).0, Flyby::Exit(_, e, l) if rel_err(e, de) <= CONVERGED && rel_err(l, dl) <= CONVERGED);
        if !converged {
            unconverged += 1;
            continue;
        }
        judged += 1;
        let before = scene.heliocentric(0.0, &s);
        let answer = law.restricted(&scene, s, &[t]).and_then(|v| v.first().copied()).map(|state| scene.heliocentric(t, &state));
        let (ee, el) = answer.map_or((f64::INFINITY, f64::INFINITY), |a| (rel_err(a.0 - before.0, de), rel_err(a.1 - before.1, dl)));
        ok += (ee <= ASSIST_TOL && el <= ASSIST_TOL) as usize;
        (worst_e, worst_l) = (if worst_e.is_nan() || ee.is_nan() { f64::NAN } else { worst_e.max(ee) }, if worst_l.is_nan() || el.is_nan() { f64::NAN } else { worst_l.max(el) });
    }
    let excluded = never + unconverged;
    let pass = taken == SEEDS && judged > 0 && ok * 100 >= 99 * judged && excluded as f64 <= EXCLUDED_MAX * SEEDS as f64;
    let replaced = if inside.is_empty() { "none".to_string() } else { inside.iter().map(|(i, r)| format!("#{i} at {r:.2}")).collect::<Vec<_>>().join(", ") };
    let detail = format!(
        "assists: {ok}/{judged} judged flybys within {ASSIST_TOL:.0e} in both ΔE and ΔL, worst ΔE {worst_e:.2e} ΔL {worst_l:.2e}; {excluded} of {SEEDS} excluded ({never} never in or out, {unconverged} not converged); {} draws replaced, the reference passing inside the planet (draw at planet radii: {replaced})",
        inside.len()
    );
    Gate { id: "B13", pass, detail, secs: 0.0 }
}

#[cfg(test)]
mod tests {
    use super::super::laws::{Echo, Events, Fault, Planted, Silent};
    use super::*;

    fn events(restricted: impl Fn(&Restricted, [f64; 4], &[f64]) -> Option<Vec<[f64; 4]>> + 'static) -> Events {
        Events { binary: Box::new(Some), restricted: Box::new(restricted) }
    }

    #[test]
    fn the_flyby_starts_on_the_incoming_hyperbola() {
        let s = JUPITER;
        for (q, v_inf, psi) in sample::flybys(8) {
            let w = s.relative(0.0, &ship(&s, q, v_inf, psi));
            let (r, v2) = (w[0].hypot(w[1]), w[2] * w[2] + w[3] * w[3]);
            assert!((r / (START_SOI * s.soi()) - 1.0).abs() < 1e-12);
            // Energy v∞²/2 and angular momentum √(μ·q·(1 + e)), counter-clockwise, arriving.
            assert!(((0.5 * v2 - s.mu / r) / (0.5 * v_inf * v_inf) - 1.0).abs() < 1e-9);
            let (e, h) = (1.0 + q * s.planet_radius * v_inf * v_inf / s.mu, w[0] * w[3] - w[1] * w[2]);
            assert!((h / (s.mu * q * s.planet_radius * (1.0 + e)).sqrt() - 1.0).abs() < 1e-9 && w[0] * w[2] + w[1] * w[3] < 0.0);
            // The periapsis of that orbit, from the eccentricity vector, is q.
            let (vr, mu) = ((w[0] * w[2] + w[1] * w[3]) / r, s.mu);
            let evec = [(v2 - mu / r) * w[0] / mu - r * vr * w[2] / mu, (v2 - mu / r) * w[1] / mu - r * vr * w[3] / mu];
            let ecc = evec[0].hypot(evec[1]);
            assert!((ecc / e - 1.0).abs() < 1e-9 && (h * h / mu / (1.0 + ecc) / (q * s.planet_radius) - 1.0).abs() < 1e-9);
            // The asymptote it came in on points at ψ: the position turned back to infinity, at −ν∞ from periapsis.
            let (omega, nu_inf) = (evec[1].atan2(evec[0]), (-1.0 / ecc).acos());
            assert!((((omega - nu_inf) - psi).rem_euclid(std::f64::consts::TAU)).min(std::f64::consts::TAU - ((omega - nu_inf) - psi).rem_euclid(std::f64::consts::TAU)) < 1e-9);
        }
    }

    #[test]
    fn echo_passes_and_the_reference_finds_every_flyby_in_and_out_within_a_period() {
        let g = b13(&Echo);
        assert!(g.pass && g.detail.contains("64/64 judged") && g.detail.contains("0 of 64 excluded"), "{}", g.detail);
        let s = JUPITER;
        let (q, v_inf, psi) = sample::flybys(1)[0];
        let (Flyby::Exit(t, de, dl), _) = reference(&s, ship(&s, q, v_inf, psi), RTOL) else { panic!("no exit") };
        assert!(t > 0.0 && t < s.period() && de != 0.0 && dl != 0.0);
    }

    #[test]
    fn the_planted_kick_and_the_dropped_tide_fail() {
        for fault in [Fault::Kick, Fault::NoTide] {
            let g = b13(&Planted(fault));
            assert!(!g.pass, "{}", g.detail);
        }
    }

    #[test]
    fn a_law_that_cannot_answer_fails_and_so_does_one_that_is_off_by_2_permille_in_speed() {
        assert!(!b13(&Silent).pass);
        // Every speed 0.2% high: the heliocentric energy moves by 0.4% of v², which is a large share of an assist.
        let fast = events(|scene, ship, times| Some(Echo.restricted(scene, ship, times)?.into_iter().map(|st| [st[0], st[1], st[2] * 1.002, st[3] * 1.002]).collect()));
        assert!(!b13(&fast).pass);
        assert!(!b13(&events(|_, _, _| Some(vec![]))).pass);
    }

    #[test]
    fn a_law_that_only_gets_the_position_wrong_by_a_planet_radius_still_passes() {
        // An assist is a change of orbit, not of place: a shift of 4.84e4 is 1e-4 of the orbit's radius.
        let shifted = events(|scene, ship, times| Some(Echo.restricted(scene, ship, times)?.into_iter().map(|st| [st[0] + scene.planet_radius, st[1], st[2], st[3]]).collect()));
        let g = b13(&shifted);
        assert!(g.pass, "{}", g.detail);
    }

    /// The first `SEEDS` draws in the oracle's domain, as the gate takes them, and how many it replaced; each with its closest approach.
    fn domain() -> (Vec<(f64, f64, f64, f64)>, usize) {
        let s = JUPITER;
        let (mut taken, mut replaced) = (Vec::new(), 0);
        for (q, v_inf, psi) in sample::flybys(DRAWS) {
            let (_, closest) = reference(&s, ship(&s, q, v_inf, psi), RTOL);
            if closest < s.planet_radius {
                replaced += 1;
            } else if taken.len() < SEEDS {
                taken.push((q, v_inf, psi, closest / s.planet_radius));
            }
        }
        (taken, replaced)
    }

    #[test]
    fn a_seed_whose_reference_passes_inside_the_planet_is_replaced_and_named_and_the_count_is_kept() {
        let s = JUPITER;
        let g = b13(&Echo);
        let (mut replaced, mut taken) = (0, Vec::new());
        for (i, (q, v_inf, psi)) in sample::flybys(DRAWS).into_iter().enumerate() {
            if taken.len() == SEEDS {
                break;
            }
            let (_, closest) = reference(&s, ship(&s, q, v_inf, psi), RTOL);
            if closest < s.planet_radius {
                replaced += 1;
                // The draw is named with its closest approach in the detail line.
                let named = format!("#{i} at {:.2}", closest / s.planet_radius);
                assert!(g.detail.contains(&named), "{named} not in {}", g.detail);
            } else {
                taken.push(closest / s.planet_radius);
            }
        }
        // The rule is exercised (the plane's lost flybys are among them), the 64 are kept, and every one judged is outside the planet.
        assert!(replaced >= 7 && taken.len() == SEEDS && taken.iter().all(|&r| r >= 1.0));
        assert!(g.pass && g.detail.contains("64/64 judged") && g.detail.contains(&format!("; {replaced} draws replaced")), "{}", g.detail);
    }

    #[test]
    fn the_closest_approach_agrees_between_the_two_tolerances_on_every_flyby() {
        // Unlike B12's chaos, one flyby's closest approach is converged: the replacement does not depend on the tolerance.
        let s = JUPITER;
        for (q, v_inf, psi) in sample::flybys(DRAWS).into_iter().take(96) {
            let (a, b) = (reference(&s, ship(&s, q, v_inf, psi), RTOL).1, reference(&s, ship(&s, q, v_inf, psi), RTOL_FINE).1);
            assert!((a / b - 1.0).abs() < 1e-6, "{a} against {b}");
        }
    }

    #[test]
    fn a_law_that_destroys_ships_passing_above_the_surface_fails() {
        // planted-swollen has a surface at 1.5 planet radii; the reference passes the planet at 1.0 to 1.5 radii on some of the 64.
        let (taken, _) = domain();
        let thin = taken.iter().filter(|x| x.3 < 1.5).count();
        assert!(thin >= 1, "no judged flyby passes between 1.0 and 1.5 radii");
        let g = b13(&Planted(Fault::Swollen));
        assert!(!g.pass && g.detail.contains(&format!("{}/64 judged", 64 - thin)), "{thin} thin: {}", g.detail);
        // A law with the true surface (echo) keeps them all.
        assert!(b13(&Echo).pass);
    }

    #[test]
    fn relative_error_is_zero_for_equal_values_and_nan_stays_nan() {
        assert_eq!(rel_err(0.0, 0.0), 0.0);
        assert_eq!(rel_err(1.5, 1.5), 0.0);
        assert!((rel_err(1.01, 1.0) - 0.01).abs() < 1e-15);
        assert!(rel_err(f64::NAN, 1.0).is_nan() && rel_err(1.0, 0.0).is_infinite());
    }
}
