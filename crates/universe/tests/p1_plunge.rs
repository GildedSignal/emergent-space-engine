//! **Gate P1, the plunge** (Julien, 12 October: "i just don't want it buggy, fly like the sr 71"). Braking to rest above a
//! planet gave `NoBoundOrbit`: a radial plunge has no periapsis, so no tube, so a refused kick after another and a ship frozen
//! alive. A ship at rest is the plain case of a fall, and the compiler owes it a tube.
//!
//! **Frozen before the first run.** A lone central mass `M = 1` (the root unit) of radius `R`, and a ship at rest at `r0`
//! (an exact integer state with zero velocity) at `r0/R` = 2, 5, 20, 100 and 1000. Over every case, against the exact
//! Schwarzschild radial infall from rest (closed forms in `η`, checked here against a quadrature of the geodesic):
//! 1. the time to the surface in coordinate time (the tick the engine loses the ship at, found by bisection on fresh
//!    universes) and in proper time (the ship's clock at the loss, as the view reads it) is within 1e-2 of the oracle's: worst
//!    relative error ≤ 1e-2, and at every case at once;
//! 2. zero refusals and no fault, and the ship is alive at every tick before the surface (the tick before the loss) and lost
//!    at it (one event);
//! 3. the HUD has the impact from the first frame, and its tick is the loss's.
//! Families: the star's own radius (471,000 M: the plane's central body), an Earth-sized radius at a star's mass (4,313 M),
//! and a compact star (6 M, where the fall is strongly relativistic: the control that the oracle can tell GR from Newton:
//! there Newton's time is off by more than 1e-2 and the engine must not be).
//! The gate is the worst case of each family, printed one line per case.
use emergent_space::orbit::Scalar;
use emergent_universe::num::{s, Tick};
use emergent_universe::view::{gather, TICK_SECONDS};
use emergent_universe::{Config, Kind, Universe};

/// Exact Schwarzschild radial infall from rest at `r0` (`M = 1`) to radius `rs`: (coordinate time, proper time).
fn exact(r0: f64, rs: f64) -> (f64, f64) {
    let eta = (2.0 * rs / r0 - 1.0).acos();
    let a = (r0 / 2.0 - 1.0).sqrt();
    let tau = (r0.powi(3) / 8.0).sqrt() * (eta + eta.sin());
    let t = 2.0 * ((a + (eta / 2.0).tan()) / (a - (eta / 2.0).tan())).abs().ln() + 2.0 * a * (eta + r0 / 4.0 * (eta + eta.sin()));
    (t, tau)
}

/// The same by quadrature of `dt/dη` (Gauss-Legendre, 24 nodes on 64 panels): the oracle's own check.
fn quadrature(r0: f64, rs: f64) -> f64 {
    let eta_end = (2.0 * rs / r0 - 1.0).acos();
    let e = (1.0 - 2.0 / r0).sqrt();
    let f = |eta: f64| {
        let r = r0 / 2.0 * (1.0 + eta.cos());
        let lapse = 1.0 - 2.0 / r;
        // dr = -(r0/2) sin η dη; sqrt(2/r - 2/r0) = sqrt((1 - cos η)/r)
        e * (r0 / 2.0) * eta.sin() / (lapse * ((1.0 - eta.cos()) / r).sqrt())
    };
    // 24-point Gauss-Legendre by Newton on the Legendre polynomial
    let n = 24;
    let mut nodes = Vec::new();
    for i in 0..n {
        let mut x = (std::f64::consts::PI * (i as f64 + 0.75) / (n as f64 + 0.5)).cos();
        let mut dp = 1.0;
        for _ in 0..60 {
            let (mut p0, mut p1) = (1.0, x);
            for k in 2..=n {
                let p2 = ((2 * k - 1) as f64 * x * p1 - (k - 1) as f64 * p0) / k as f64;
                p0 = p1;
                p1 = p2;
            }
            dp = n as f64 * (x * p1 - p0) / (x * x - 1.0);
            let dx = p1 / dp;
            x -= dx;
            if dx.abs() < 1e-15 {
                break;
            }
        }
        nodes.push((x, 2.0 / ((1.0 - x * x) * dp * dp)));
    }
    let panels = 64;
    let mut total = 0.0;
    for p in 0..panels {
        let (lo, hi) = (eta_end * p as f64 / panels as f64, eta_end * (p + 1) as f64 / panels as f64);
        for &(x, w) in &nodes {
            total += w * (hi - lo) / 2.0 * f((hi + lo) / 2.0 + (hi - lo) / 2.0 * x);
        }
    }
    total
}

#[test]
fn the_oracle_is_the_geodesic_and_not_newton() {
    for (r0, rs) in [(12.0, 6.0), (30.0, 6.0), (9.4e5, 4.71e5), (4.71e8, 4.71e5), (8_626.0, 4_313.0)] {
        let (t, tau) = exact(r0, rs);
        let q = quadrature(r0, rs);
        assert!(((t - q) / t).abs() < 1e-9, "r0 {r0}, R {rs}: closed form {t}, quadrature {q}");
        // Newton: t = τ = sqrt(r0³/8) (η + sin η) (no lapse, no time dilation)
        println!("r0 {r0:e}, R {rs:e}: t {t:.6e}, τ {tau:.6e}, t/τ {:.6}", t / tau);
    }
    // the compact star: the Newtonian fall time (the proper time, in this weak-field-free form `sqrt(r0³/8)(η + sin η)` is Newton's
    // too) is more than 1e-2 off the coordinate time: the control that the gate can tell GR from Newton
    let (t, tau) = exact(12.0, 6.0);
    assert!(((t - tau) / tau).abs() > 0.1, "the strong field must matter: t {t}, τ {tau}");
}

fn world(surface: i64, r0: i64) -> Universe {
    let mut u = Universe::new(s(surface), Config::default());
    u.add_body_state(Kind::Player, 0, [s(r0), Scalar::ZERO], [Scalar::ZERO; 2], Scalar::ZERO).expect("a ship at rest above a surface has a tube");
    u.start().expect("the universe starts");
    u
}

/// Whether the ship is alive after everything up to tick `t` is resolved (a fresh universe: a probe never disturbs another).
fn alive_at(surface: i64, r0: i64, t: Tick) -> bool {
    let mut u = world(surface, r0);
    u.settle(t);
    u.rec(0).alive
}

#[test]
fn a_ship_at_rest_falls_to_the_surface_by_the_exact_infall() {
    let mut families = Vec::new();
    for (name, surface) in [("star", 471_000i64), ("earth-sized", 4_313), ("compact", 6)] {
        let (mut worst_t, mut worst_tau) = (0f64, 0f64);
        for ratio in [2i64, 5, 20, 100, 1000] {
            let r0 = surface * ratio;
            let (t_exact, tau_exact) = exact(r0 as f64, surface as f64);
            let mut u = world(surface, r0);
            // 3. the impact, from the first frame
            u.now = 0;
            let view = gather(&u, &[]).expect("a view");
            let impact = view.impact.clone().unwrap_or_else(|| panic!("{name} {ratio}R: no impact warning at the start"));
            assert!(view.alive && impact.body == "star");
            // 1. the coordinate time: the loss tick by bisection (alive before, lost at)
            let (mut lo, mut hi) = (0i64, (t_exact * 1.5) as i64 + 10);
            assert!(!alive_at(surface, r0, hi), "{name} {ratio}R: still alive at 1.5x the exact time ({hi})");
            assert!(alive_at(surface, r0, lo));
            while hi - lo > 1 {
                let mid = lo + (hi - lo) / 2;
                if alive_at(surface, r0, mid) {
                    lo = mid;
                } else {
                    hi = mid;
                }
            }
            let lost = hi;
            let err_t = (lost as f64 - t_exact) / t_exact;
            assert_eq!(impact.tick, lost, "{name} {ratio}R: the HUD says tick {}, the ship is lost at {lost}", impact.tick);
            // 2. alive at every tick before, lost at the tick (one event, no refusal)
            u.settle(lost - 1);
            assert!(u.rec(0).alive);
            u.settle(lost);
            let rec = u.rec(0);
            assert!(!rec.alive && rec.refusals == 0 && rec.fault.is_none(), "{name} {ratio}R: alive {}, refusals {}, fault {:?}", rec.alive, rec.refusals, rec.fault);
            assert_eq!(rec.events, 1, "{name} {ratio}R: the fall is one event, the impact");
            // the ship's clock at the loss, as the HUD reads it
            u.now = lost;
            let wreck = gather(&u, &[]).expect("a wreck has a view");
            let tau = wreck.proper_seconds / TICK_SECONDS;
            let err_tau = (tau - tau_exact) / tau_exact;
            println!("{name:<11} r0 = {ratio:>4} R: coordinate {lost:.6e} (exact {t_exact:.6e}, {err_t:+.2e}), proper {tau:.6e} (exact {tau_exact:.6e}, {err_tau:+.2e}); {}", wreck.loss.clone().unwrap_or_default());
            worst_t = worst_t.max(err_t.abs());
            worst_tau = worst_tau.max(err_tau.abs());
            assert!(err_t.abs() <= 1e-2 && err_tau.abs() <= 1e-2, "{name} {ratio}R: coordinate {err_t:+.3e}, proper {err_tau:+.3e}");
        }
        families.push((name, worst_t, worst_tau));
    }
    for (name, wt, wtau) in &families {
        println!("P1 {name}: worst relative error {wt:.2e} (coordinate), {wtau:.2e} (proper)");
    }
}
