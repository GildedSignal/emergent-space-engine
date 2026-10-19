//! Gate T1, a held burn converges (frozen 13 October 2026, before the burn's cadence changed): a burn is the player's verb,
//! and its kicks are a discretisation of a continuous thrust, so what a burn does must not depend on the cadence beyond a
//! bounded error that shrinks as the cadence refines.
//!
//! The scene: the plane (seed 5), the player on its starting orbit about Home; at 10 s it burns, forward at levels 0, 4, 8,
//! 12 and 15 for 2,000 s (from doubling the orbital speed to 0.64 c), and in reverse at levels 0, 4 and 8.
//! Amendment (the integrator, 14 October): the reverse L0 burn lasts 0.02·v₀/a (it loses 2% of its speed and stays up past the reading); reverse L4 and L8 keep 0.5·v₀/a.
//! Then it coasts 100 s. The reading: the root-frame position
//! and velocity at the end of the coast. The reference is the same flight at a cadence 64 times finer (2^6 more kicks per
//! radial period and a thrust quantum 2^6 smaller); the error is the distance to the reference over what the burn itself
//! moved the ship (its distance to the flight that never burned), in position and in velocity.
//!
//! PASS iff, in every burn:
//! 1. at the shipped cadence (`Config::default()`), both errors are at most 3e-2 (the work test's tolerance, `throttle.rs`);
//! 2. the error converges: at a cadence 16 times finer than shipped it is at most a quarter of the shipped one's (or both are
//!    below 1e-9);
//! 3. no run refuses, and the ship is alive at the reading.
//! Control: the cadence 64 times coarser than shipped must fail criterion 1 in at least one burn.
//!
//! First run, on the shipped cadence of 13 October (a kick moves the velocity by 1/64 of the local speed): the forward burns
//! pass (shipped 3.4e-3..1.8e-2 in position, 16x finer 1.6e-4..9.0e-4: first order; 64x coarser 7.6e-2..4.8e-1); the
//! harness then lost the reverse L0 coast (the ship not alive at the reading, no refusal) and the run took 137 s. The harness
//! is repaired and split to fit 60 s by the job that changes the cadence (`artifacts/runs/burst/prompt.md`); the criteria
//! above do not change.
//! First pass, centred payment + capped geometric cadence (13 October): forward shipped position errors are
//! 2.66e-4, 2.23e-4, 5.67e-4, 1.36e-4, 1.29e-5 at L0/4/8/12/15; velocity errors are
//! 3.12e-4, 6.86e-5, 2.09e-5, 3.82e-6, 5.42e-6. Reverse L4/L8 position errors are 7.55e-4/2.03e-4,
//! velocity 2.61e-5/3.16e-6. All readable shipped burns pass the 3e-2 accuracy limit, but T1 is FAIL:
//! forward L4 fails convergence in both readings; L8 fails position convergence. The reverse L0 reference
//! hits Home during the burn (~700 s world time, 7.51 km/s), before its 1,239 s cut. The old harness cut
//! the already lost ship and rebound its wreck, hiding the real loss time; it now reports loss before cutting.
//! That first pass kept the original scene and durations. Its nine split tests took 48.50 s in total in
//! artifacts/runs/burst/t1-after.txt (therefore each is below 60 s); the coarse control fails at forward L0.
//!
//! Continuation (20 October): only the authorised L0 duration amendment above changes the scene.
//! Refinement now subdivides the geometric ramp: previously 16x finer regrew the shipped 20.659 s
//! interval at 100 s. Root-doll gravity pays the shortened burn interval, not the full fictitious tick
//! (the previous weight reached 518 times the interval). No numerical criterion changed.
//! Final shipped position/velocity errors, forward L0/4/8/12/15:
//! 3.86e-4/3.60e-4, 2.26e-4/7.39e-5, 5.81e-4/1.85e-6, 1.34e-4/2.29e-6, 1.24e-5/5.25e-6.
//! Reverse L0/4/8: 6.92e-4/3.69e-5, 7.55e-4/2.61e-5, 2.04e-4/3.19e-6.
//! T1 PASS, 9/9; 44.69 s total, longest individual 10.51 s. The coarse control still fails at L0.
//! Full measurements: artifacts/runs/burst2/suite-final.txt and test-times-final.json.
use emergent_universe::fleet::Order;
use emergent_universe::observe::root_state;
use emergent_universe::scenario::plane;
use emergent_universe::thrust::{g_of, word};
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::Config;

const T0: i64 = 2_000_000;
const COAST_S: f64 = 100.0;

/// The root-frame (position, velocity) at the reading, or why there is none.
fn fly(cfg: Config, keys: u8, level: u8, seconds: f64) -> Result<([f64; 2], [f64; 2]), String> {
    let mut p = plane(cfg, 5, Order::Sparse, 1, 8).unwrap();
    p.u.settle(T0);
    let end = T0 + (seconds / TICK_SECONDS) as i64;
    if keys != 0 {
        p.u.input(T0, word(keys, level))
            .map_err(|e| format!("{e:?}"))?;
        p.u.settle(end);
        // Never send a cut to an already lost ship: it would rebind the wreck at
        // the cut tick and erase the location/time of the loss from this diagnostic.
        live(&p, end)?;
        p.u.input(end, word(0, level))
            .map_err(|e| format!("{e:?}"))?;
    }
    let read = end + (COAST_S / TICK_SECONDS) as i64;
    p.u.settle(read);
    live(&p, read)?;
    root_state(&p.u.ctx(), p.player, read).map_err(|e| format!("{e:?}"))
}

fn live(p: &emergent_universe::scenario::Plane, read: i64) -> Result<(), String> {
    let rec = p.u.rec(p.player);
    if !rec.alive || rec.refusals != 0 {
        return Err(format!(
            "alive {} refusals {} fault {:?}, last binding {}, read {}, loss {:?}",
            rec.alive,
            rec.refusals,
            rec.fault,
            rec.b.event_time,
            read,
            emergent_universe::view::gather(&p.u, &p.names).and_then(|v| v.loss)
        ));
    }
    Ok(())
}

fn cadence(finer: i32) -> Config {
    let d = Config::default();
    Config {
        step_log2: d.step_log2 + finer,
        thrust_quantum_log2: d.thrust_quantum_log2 + finer,
        ..d
    }
}

fn dist(a: [f64; 2], b: [f64; 2]) -> f64 {
    ((a[0] - b[0]).powi(2) + (a[1] - b[1]).powi(2)).sqrt()
}

fn check_burn(keys: u8, level: u8) {
    let d = Config::default();
    // The ship's speed about Home at the start, for the reverse burns' length.
    let v0 = {
        let mut p = plane(d, 5, Order::Sparse, 1, 8).unwrap();
        p.u.settle(T0);
        let (_, v) = p.u.rec(p.player).b.cartesian(T0).unwrap();
        let v = [
            emergent_universe::num::to_f64(v[0]),
            emergent_universe::num::to_f64(v[1]),
        ];
        (v[0] * v[0] + v[1] * v[1]).sqrt() * 299_792_458.0
    };
    let seconds = if keys == 1 {
        2000.0
    } else {
        (if level == 0 { 0.02 } else { 0.5 }) * v0 / (g_of(&d, level) * 9.806_65)
    };
    let burns = [(keys, level, seconds)];
    let mut failures = Vec::new();
    let mut control_failed = false;
    for &(keys, level, seconds) in &burns {
        let coast = fly(d, 0, 0, seconds).unwrap();
        let reference = match fly(cadence(6), keys, level, seconds) {
            Ok(r) => r,
            Err(why) => {
                // A lost reference cannot judge convergence. Report every cadence rather
                // than dropping the burn or changing its duration/reading/criterion.
                println!("reference {keys} L{level} {seconds:.1}s: {why}");
                for q in [0, 4, -6] {
                    println!("cadence {q}: {:?}", fly(cadence(q), keys, level, seconds));
                }
                panic!("T1 reference is not alive at the frozen reading: {why}");
            }
        };
        let moved = (dist(reference.0, coast.0), dist(reference.1, coast.1));
        let err = |cfg: Config| -> Result<(f64, f64), String> {
            let r = fly(cfg, keys, level, seconds)?;
            Ok((
                dist(r.0, reference.0) / moved.0,
                dist(r.1, reference.1) / moved.1,
            ))
        };
        let name = format!(
            "{} L{level} {seconds:.1} s",
            if keys == 1 { "forward" } else { "reverse" }
        );
        let shipped = err(d);
        let finer = err(cadence(4));
        let coarse = err(cadence(-6));
        let show = |e: &Result<(f64, f64), String>| {
            e.as_ref()
                .map_or_else(|w| w.clone(), |e| format!("{:.2e}/{:.2e}", e.0, e.1))
        };
        println!(
            "{name:<24} moved {:.2e}/{:.2e}: shipped {}, 16x finer {}, 64x coarser {}",
            moved.0,
            moved.1,
            show(&shipped),
            show(&finer),
            show(&coarse)
        );
        match (&shipped, &finer) {
            (Ok(s), Ok(f)) => {
                if s.0 > 3e-2 || s.1 > 3e-2 {
                    failures.push(format!(
                        "{name}: shipped error {:.3e}/{:.3e} over 3e-2",
                        s.0, s.1
                    ));
                }
                for (a, b, what) in [(s.0, f.0, "position"), (s.1, f.1, "velocity")] {
                    if !(b <= a / 4.0 || (a < 1e-9 && b < 1e-9)) {
                        failures.push(format!("{name}: the {what} error does not converge ({a:.3e} shipped, {b:.3e} 16x finer)"));
                    }
                }
            }
            _ => failures.push(format!("{name}: refused or lost ({shipped:?}, {finer:?})")),
        }
        control_failed |= coarse.map_or(true, |c| c.0 > 3e-2 || c.1 > 3e-2);
    }
    // The separate control test checks the frozen existential criterion.
    let _ = control_failed;
    assert!(failures.is_empty(), "T1 fails:\n{}", failures.join("\n"));
}

macro_rules! burn_test {
    ($name:ident, $keys:expr, $level:expr) => {
        #[test]
        fn $name() {
            check_burn($keys, $level);
        }
    };
}
burn_test!(t1_forward_l0, 1, 0);
burn_test!(t1_forward_l4, 1, 4);
burn_test!(t1_forward_l8, 1, 8);
burn_test!(t1_forward_l12, 1, 12);
burn_test!(t1_forward_l15, 1, 15);
burn_test!(t1_reverse_l0, 2, 0);
burn_test!(t1_reverse_l4, 2, 4);
burn_test!(t1_reverse_l8, 2, 8);
#[test]
fn t1_coarse_control() {
    // The frozen existential control: stop at a witness, otherwise try every burn.
    let d = Config::default();
    let mut p = plane(d, 5, Order::Sparse, 1, 8).unwrap();
    p.u.settle(T0);
    let (_, v) = p.u.rec(p.player).b.cartesian(T0).unwrap();
    let v0 = (emergent_universe::num::to_f64(v[0]).powi(2)
        + emergent_universe::num::to_f64(v[1]).powi(2))
    .sqrt()
        * 299_792_458.0;
    let burns = [0u8, 4, 8, 12, 15]
        .map(|l| (1, l, 2000.0))
        .into_iter()
        .chain([0u8, 4, 8].map(|l| (2, l, (if l == 0 { 0.02 } else { 0.5 }) * v0 / (g_of(&d, l) * 9.806_65))));
    for (keys, level, seconds) in burns {
        let coast = fly(d, 0, 0, seconds).unwrap();
        let reference = fly(cadence(6), keys, level, seconds).unwrap();
        let coarse = fly(cadence(-6), keys, level, seconds);
        if coarse.map_or(true, |c| {
            dist(c.0, reference.0) / dist(reference.0, coast.0) > 3e-2
                || dist(c.1, reference.1) / dist(reference.1, coast.1) > 3e-2
        }) {
            println!("coarse control witness: keys {keys}, L{level}");
            return;
        }
    }
    panic!("the control (64x coarser) must fail criterion 1 somewhere");
}
