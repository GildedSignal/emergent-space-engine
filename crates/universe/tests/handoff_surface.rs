//! Motion memo §5 step 3. These probes exercise the shipped universe, not a float replica.
use emergent_space::orbit::Scalar;
use emergent_universe::{num::from_f64 as sc, observe, Budget, Config, Kind, OrbitSpec, Universe};
use std::time::{Duration, Instant};

fn satellite(fraction: f64, retrograde: bool) -> (Universe, usize, usize, f64, f64) {
    let (sep, mu) = (527_000_000.0f64, 2f64.powi(-10));
    let hill = sep * (mu / 3.0).cbrt();
    let omega = (1.0 + mu).sqrt() / sep.powf(1.5);
    let mut u = Universe::new(sc(471_000.0), Config::default());
    let planet = u.add_body(Kind::Planet, OrbitSpec { doll: 0, periapsis: sc(sep), e_q48: 0, clockwise: false, angle: 0, phase: 0 }, Scalar::ZERO).unwrap();
    let doll = u.add_doll("planet", planet, -10, sc(49_000.0 / mu)).unwrap();
    let ship = u.add_body(Kind::Ship, OrbitSpec { doll, periapsis: sc(fraction * hill / mu), e_q48: 0, clockwise: retrograde, angle: 0, phase: 0 }, Scalar::ZERO).unwrap();
    u.start().unwrap();
    (u, planet, ship, omega, sep)
}

fn jacobi(u: &Universe, planet: usize, ship: usize, t: i64, omega: f64) -> f64 {
    let ((x, v), (p, _)) = (observe::root_state(&u.ctx(), ship, t).unwrap(), observe::root_state(&u.ctx(), planet, t).unwrap());
    let mu = 2f64.powi(-10);
    let r = x[0].hypot(x[1]);
    let d = (x[0] - p[0]).hypot(x[1] - p[1]);
    let e = 0.5 * (v[0]*v[0] + v[1]*v[1]) - 1.0/r - mu/d + mu*(x[0]*p[0]+x[1]*p[1])/p[0].hypot(p[1]).powi(3);
    -2.0 * (e - omega * (x[0]*v[1] - x[1]*v[0]))
}

fn median(xs: &mut [f64]) -> f64 {
    xs.sort_by(f64::total_cmp);
    xs[xs.len()/2]
}

fn p4(fraction: f64, retrograde: bool) {
    let start = Instant::now();
    let (mut u, planet, ship, omega, sep) = satellite(fraction, retrograde);
    let c0 = jacobi(&u, planet, ship, 0, omega);
    let period = std::f64::consts::TAU / omega;
    let mut errors = [Vec::new(), Vec::new(), Vec::new()];
    for sample in 1..=2000*8 {
        let t = (sample as f64 * period / 8.0).round() as i64;
        loop {
            assert!(start.elapsed() < Duration::from_secs(55), "P4 FAIL timeout before sample {sample}/16000; kicks={} handoffs={}", u.stats.kicks, u.stats.handoffs);
            if u.advance(t, Budget::events(128)).events == 0 { break; }
        }
        u.now = t;
        u.prune();
        let rec = u.rec(ship);
        assert!(rec.alive && rec.refusals == 0, "P4 FAIL f={fraction} retro={retrograde} sample={sample}: alive={} fault={:?}", rec.alive, rec.fault);
        let err = (jacobi(&u, planet, ship, t, omega) - c0).abs() * sep;
        let bin = if sample <= 20*8 { 0 } else if sample <= 200*8 { 1 } else { 2 };
        errors[bin].push(err);
        if sample == 20*8 || sample == 200*8 || sample == 2000*8 {
            let med = median(&mut errors[bin]);
            let previous = if bin > 0 { Some(median(&mut errors[bin-1])) } else { None };
            let ratio = previous.map(|p| med/p);
            println!("P4 f={fraction} retro={retrograde} periods={} median={med:e} decade_ratio={ratio:?} kicks={} handoffs={} seconds={:.3}", sample/8, u.stats.kicks, u.stats.handoffs, start.elapsed().as_secs_f64());
            assert!(ratio.is_none_or(|r| r.is_finite() && r <= 1.3), "P4 FAIL: decade ratio exceeds 1.3 at period {} of 2000", sample/8);
        }
    }
    let med = errors.each_mut().map(|xs| median(xs));
    let ratio = [med[1]/med[0], med[2]/med[1]];
    println!("P4 f={fraction} retro={retrograde} periods=2000 median={med:?} decade_ratio={ratio:?} kicks={} handoffs={} seconds={:.3}", u.stats.kicks, u.stats.handoffs, start.elapsed().as_secs_f64());
    assert!(ratio.into_iter().all(|r| r.is_finite() && r <= 1.3), "P4 FAIL: decade ratio exceeds 1.3");
}

#[test] fn p4_satellite_03_prograde() { p4(0.3, false); }
#[test] fn p4_satellite_03_retrograde() { p4(0.3, true); }
#[test] fn p4_satellite_05_prograde() { p4(0.5, false); }
#[test] fn p4_satellite_05_retrograde() { p4(0.5, true); }
#[test] fn p4_satellite_09_prograde() { p4(0.9, false); }
#[test] fn p4_satellite_09_retrograde() { p4(0.9, true); }

/// P5 at the coordinate-map boundary. Energy and event time are nonzero independent integer
/// components, and survive 1000 captures/releases. This is deliberately distinct from a
/// universe-level handoff: rebinding and event scheduling must also keep these words.
#[test]
fn p5_extended_coordinates_return_identical_words() {
    use emergent_universe::lorentz::{Frame, Handoff, PhasePoint};
    for beta in [0.01, 0.3, 0.9] {
        for angle in [0.0f64, 0.7, 2.1, -2.8] {
            let chart = Handoff { frame: Frame::of([sc(beta*angle.cos()), sc(beta*angle.sin())]).unwrap(), origin: [7 << 65, -(3 << 63), 1 << 68], unit_shift: 10 };
            let initial = PhasePoint { event: [13 << 65, (5 << 63)+123, -(1 << 67)-317], momentum: [(1 << 90)+131, -(1 << 85)-17, (1 << 82)+27], event_exp: -40, momentum_exp: -90 };
            let mut point = initial;
            for _ in 0..1000 {
                let child = chart.capture(point).unwrap();
                assert_ne!(child.event[0], point.event[0]-chart.origin[0], "a moving chart must transform time");
                assert_ne!(child.momentum[0], point.momentum[0], "the energy register must transform");
                point = chart.release(child).unwrap();
                assert_eq!(point, initial, "beta={beta}, angle={angle}");
            }
        }
        println!("P5 coordinate map beta={beta}: 4000 exact extended-state round trips");
    }
}

#[test]
fn an_extended_handoff_refuses_overflow_without_mutating_the_input() {
    use emergent_universe::lorentz::{Handoff, PhasePoint};
    let chart = Handoff { frame: None, origin: [-1, 0, 0], unit_shift: 10 };
    let point = PhasePoint { event: [i128::MAX, 0, 0], momentum: [17, 3, -9], event_exp: 0, momentum_exp: -50 };
    assert!(chart.capture(point).is_err());
    let chart = Handoff { origin: [0; 3], unit_shift: 10, ..chart };
    assert!(chart.capture(PhasePoint { event_exp: i16::MAX, ..point }).is_err());
    let child = chart.capture(PhasePoint { event: [21, -31, 45], ..point }).unwrap();
    assert_eq!(chart.release(child).unwrap().event, [21, -31, 45]);
    let chart = Handoff { frame: emergent_universe::lorentz::Frame::of([sc(-0.3), Scalar::ZERO]).unwrap(), ..chart };
    assert!(chart.capture(PhasePoint { event: [0, i128::MIN, 0], ..point }).is_err());
}

#[test]
fn the_same_surface_rejects_an_unbound_passage_and_keeps_a_bound_body() {
    use emergent_universe::step::retained_by_child;
    let (x, radius, mu) = ([sc(100.0), Scalar::ZERO], sc(200.0), Scalar::ONE);
    assert!(retained_by_child(x, [Scalar::ZERO, sc(0.01)], mu, radius).unwrap());
    assert!(!retained_by_child(x, [Scalar::ZERO, sc(0.2)], mu, radius).unwrap());
    assert!(!retained_by_child([radius, Scalar::ZERO], [Scalar::ZERO; 2], mu, radius).unwrap());
    // E_p = 0 belongs to the parent side, as does r = r_c (one strict predicate).
    assert!(!retained_by_child([sc(2.0), Scalar::ZERO], [Scalar::ZERO, Scalar::ONE], mu, radius).unwrap());
}

#[test]
fn the_surface_is_half_the_hill_radius_in_child_units() {
    use emergent_universe::{step::capture_radius, num::to_f64};
    let (u, _, _, _, sep) = satellite(0.3, false);
    let r = to_f64(capture_radius(&u.ctx(), 1, 0).unwrap());
    let expected = 0.5 * sep * (2f64.powi(-10) / 3.0).cbrt() * 1024.0;
    assert!((r/expected-1.0).abs() < 1e-8, "half-Hill surface: {r}, expected {expected}");
    assert!(r < 0.6*to_f64(u.dolls[1].edge), "the Laplace edge is a different surface");
}

#[test]
fn the_extended_map_matches_an_independent_axis_boost() {
    use emergent_universe::{lorentz::{Frame, Handoff, PhasePoint}, num::to_f64};
    let q = 1i128 << 70;
    for beta in [0.01f64, 0.3, 0.9] {
        let chart = Handoff { frame: Frame::of([sc(beta), Scalar::ZERO]).unwrap(), origin: [0; 3], unit_shift: 10 };
        let point = PhasePoint { event: [3*q, 2*q, -q], momentum: [5*q, -q, 2*q], event_exp: -70, momentum_exp: -70 };
        let got = chart.capture(point).unwrap();
        let gamma = (1.0-beta*beta).sqrt().recip();
        for (input, output, exponent) in [(point.event, got.event, got.event_exp-10), (point.momentum, got.momentum, got.momentum_exp)] {
            let f = |n: i128, e: i16| to_f64(Scalar::raw(n, e as i32).unwrap());
            let a = input.map(|n| f(n,-70));
            let want = [gamma*(a[0]-beta*a[1]), gamma*(a[1]-beta*a[0]), a[2]];
            for c in 0..3 { assert!((f(output[c],exponent)-want[c]).abs() < 1e-13); }
        }
    }
}

/// A falsifying control for wiring Ext directly into the Lorentz map: its current register
/// is minus the Kepler energy, whereas a boost needs total relativistic energy (rest energy
/// included) and momentum, not coordinate velocity. A comoving body must be at rest after a
/// boost. The literal `(-p_t, v)` vector fails this even without a handoff or a drift.
#[test]
fn the_kepler_register_is_not_a_lorentz_four_momentum() {
    use emergent_universe::{force, lorentz::Frame, num::to_f64};
    let mut wrong = 0;
    for beta in [0.01, 0.3, 0.9] {
        let v = [sc(beta), Scalar::ZERO];
        let hd = force::kepler([sc(1e15), Scalar::ZERO], v, Scalar::ONE).unwrap();
        let frame = Frame::of(v).unwrap().unwrap();
        let q = 80;
        let literal = [hd.fixed(q).unwrap(), v[0].fixed(q).unwrap(), 0];
        let child = frame.forward(literal).unwrap();
        let p = to_f64(Scalar::raw(child[1], -q).unwrap());
        println!("Kepler-register control beta={beta}: comoving child's momentum={p:e} (must be zero)");
        wrong += (p.abs() > 0.5*beta) as usize;
        // The control with actual four-momentum does come to rest under the same shears.
        let gamma = Scalar::ONE.sub(v[0].mul(v[0]).unwrap()).unwrap().sqrt().unwrap().reciprocal().unwrap();
        let physical = [gamma.fixed(q).unwrap(), gamma.mul(v[0]).unwrap().fixed(q).unwrap(), 0];
        let child = frame.forward(physical).unwrap();
        assert!(to_f64(Scalar::raw(child[1], -q).unwrap()).abs() < 1e-15);
    }
    assert_eq!(wrong, 3, "this control must expose the current register convention at all speeds");
}
