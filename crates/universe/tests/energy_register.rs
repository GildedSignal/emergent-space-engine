//! Energy-register diagnostics. The P3' threshold is the memo's two quanta, unchanged.
use emergent_space::orbit::Scalar;
use emergent_universe::{bind::{scalars, Binding}, num::{cross2, dot2, norm2, s}, scenario};

// Schwarzschild angular momentum from the actual Cartesian readout, including C.
// Velocities here are dx/dt, not canonical momenta: L = (x cross v) / (dτ/dt).
fn angular(b: &Binding, t: i64) -> Scalar {
    let (x, v) = scalars(&b.readout(t).unwrap()).unwrap();
    let r = norm2(x).unwrap();
    let a = Scalar::ONE.sub(b.entry.unit.mu.div(r).unwrap().scale(1).unwrap()).unwrap();
    let vr = dot2(x, v).unwrap().div(r).unwrap();
    let vt = cross2(x, v).unwrap().div(r).unwrap();
    let rate = a.sub(vr.mul(vr).unwrap().div(a).unwrap()).unwrap().sub(vt.mul(vt).unwrap()).unwrap().sqrt().unwrap();
    cross2(x, v).unwrap().div(rate).unwrap()
}

#[test]
fn rebinding_is_exact_at_its_anchor_but_does_not_conserve_readout_invariants() {
    let w = scenario::restricted(-10, 527_000_000, 49_000, &[(600_000_000, 0)], 1).unwrap();
    let mut b = w.u.rec(w.ships[0]).b;
    let mut exact = b.readout(0).unwrap();
    exact.velocity[0] += 1 << 42;
    let bound = emergent_universe::bind::bind(exact, 0, b.clock_exp, None, b.entry.unit).unwrap();
    b.entry = bound.entry;
    b.tube = bound.tube;
    b.residual = bound.residual;
    b.turn = bound.turn;
    b.units = bound.units;
    assert_eq!(b.readout(0).unwrap(), exact, "C reconstructs the anchor exactly");
    let emergent_space::binding::Trajectory::Cycle(c) = &b.entry.trajectory else { panic!("bound orbit") };
    let t = c.period().unwrap().scale(-3).unwrap().fixed(0).unwrap() as i64;
    let l0 = angular(&b, 0);
    let l1 = angular(&b, t);
    let relative = emergent_universe::num::to_f64(l1.sub(l0).unwrap().div(l0).unwrap());
    println!("C exact at anchor; relative change in readout GR L after P/8: {relative:e}");
    assert_ne!(l1, l0, "an additive Cartesian offset is not an invariant remainder");
}

#[test]
#[ignore = "high-gamma inverse-fit diagnostic; distinct from the energy word"]
fn high_gamma_tubes_reach_the_energy_register() {
    use emergent_universe::{num::{from_f64, to_f64}, Config, Kind, Universe};
    let mut failures = 0;
    for gamma in [100.0f64, 2000.0, 10_000.0, 1_000_000.0] {
        let mut u = Universe::new(s(2), Config::default());
        let radius = 100_000_000.0;
        let lapse = 1.0 - 2.0 / radius;
        let speed = (lapse * (1.0 - 1.0 / (gamma * gamma))).sqrt();
        let result = u.add_body_state(Kind::Ship, 0, [from_f64(radius), Scalar::ZERO],
            [Scalar::ZERO, from_f64(speed)], Scalar::ZERO);
        match result {
            Ok(i) => println!("gamma={gamma} fit=PASS E-1={}", to_f64(emergent_universe::ext::drift_energy(&u.rec(i).b).unwrap())),
            Err(e) => { println!("gamma={gamma} fit=FAIL {e:?}"); failures += 1; }
        }
    }
    assert_eq!(failures, 0, "the inverse fit must deliver a tube before its energy can be registered");
}

/// P3': J=p_t+ΩL through actual kicks and intervening drifts. A failure is retained
/// explicitly; never redefine L as a ledger chosen to cancel p_t.
#[test]
#[ignore = "P3': measured failure; run explicitly with --ignored --nocapture"]
fn p3_prime_noether_two_quanta_per_kick() {
    let sep = 527_000_000i64;
    let hill = sep as f64 * (2f64.powi(-10) / 3.0).cbrt();
    let mut worst_kick = 0i128;
    let mut worst_drift = 0i128;
    let mut kicks = 0;
    for n in 0..4 {
        let radius = (sep as f64 + if n % 2 == 0 { 1.0 } else { -1.0 } * hill * (1.5 + 0.1 * n as f64)) as i64;
        let mut w = scenario::restricted(-10, sep, 49_000, &[(radius, (n as u32).wrapping_mul(0x9E37_79B9))], 1).unwrap();
        let sh = w.ships[0];
        let mu = w.u.rec(w.planet).b.entry.unit.mu;
        let omega = mu.div(s(sep).mul(s(sep)).unwrap().mul(s(sep)).unwrap()).unwrap().sqrt().unwrap();
        let end = (200.0 * std::f64::consts::TAU / emergent_universe::num::to_f64(omega)) as i64;
        let mut previous = 0;
        let mut seed_kicks = 0;
        let (mut wk, mut wd) = (0i128, 0i128);
        loop {
            let before = w.u.rec(sh);
            assert!(before.alive && before.refusals == 0, "P3' lost/refused ship {n}");
            let Some(t) = before.plan.iter().map(|p| p.t).min() else { panic!("P3' lost plan") };
            if t > end { break; }
            let ext = before.ext.unwrap();
            let q = -(ext.pt_exp as i32);
            let drift = angular(&before.b, t).sub(angular(&before.b, previous)).unwrap().mul(omega).unwrap().fixed(q).unwrap().abs();
            wd = wd.max(drift);
            w.u.settle(t);
            let after = w.u.rec(sh);
            assert!(after.alive && after.refusals == 0, "P3' lost/refused ship {n}");
            if after.b.event_time != before.b.event_time {
                let dl = angular(&after.b, t).sub(angular(&before.b, t)).unwrap();
                let dj = after.ext.unwrap().pt - ext.pt + dl.mul(omega).unwrap().fixed(q).unwrap();
                wk = wk.max(dj.abs());
                seed_kicks += 1;
            }
            previous = t;
            // The cheapest falsifying rung: a failed local bound already kills P3'.
            // A survivor continues to the full 200-period horizon.
            if seed_kicks >= 256 && wk > 2 { break; }
        }
        println!("P3' seed={n} kicks={seed_kicks} max_kick_quanta={wk} max_drift_quanta={wd}");
        worst_kick = worst_kick.max(wk);
        worst_drift = worst_drift.max(wd);
        kicks += seed_kicks;
    }
    println!("P3' kicks={kicks} max_kick_quanta={worst_kick} max_drift_quanta={worst_drift} limit=2");
    assert!(worst_kick <= 2 && worst_drift <= 2);
}
