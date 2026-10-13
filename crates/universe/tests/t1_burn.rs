//! Gate T1, a held burn converges (frozen 13 October 2026, before the burn's cadence changed): a burn is the player's verb,
//! and its kicks are a discretisation of a continuous thrust, so what a burn does must not depend on the cadence beyond a
//! bounded error that shrinks as the cadence refines.
//!
//! The scene: the plane (seed 5), the player on its starting orbit about Home; at 10 s it burns, forward at levels 0, 4, 8,
//! 12 and 15 for 2,000 s (from doubling the orbital speed to 0.64 c), and in reverse at levels 0, 4 and 8 for half the time
//! the burn takes to stop the ship (it slows, it does not fall); then it coasts 100 s. The reading: the root-frame position
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
        p.u.input(T0, word(keys, level)).map_err(|e| format!("{e:?}"))?;
        p.u.settle(end);
        p.u.input(end, word(0, level)).map_err(|e| format!("{e:?}"))?;
    }
    let read = end + (COAST_S / TICK_SECONDS) as i64;
    p.u.settle(read);
    let rec = p.u.rec(p.player);
    if !rec.alive || rec.refusals != 0 {
        return Err(format!("alive {} refusals {} fault {:?}", rec.alive, rec.refusals, rec.fault));
    }
    root_state(&p.u.ctx(), p.player, read).map_err(|e| format!("{e:?}"))
}

fn cadence(finer: i32) -> Config {
    let d = Config::default();
    Config { step_log2: d.step_log2 + finer, thrust_quantum_log2: d.thrust_quantum_log2 + finer, ..d }
}

fn dist(a: [f64; 2], b: [f64; 2]) -> f64 {
    ((a[0] - b[0]).powi(2) + (a[1] - b[1]).powi(2)).sqrt()
}

#[test]
#[ignore = "T1, frozen: its harness exceeds 60 s and loses a reverse coast (the burst job repairs both, criteria unchanged)"]
fn t1_a_held_burn_converges_with_its_cadence() {
    let d = Config::default();
    // The ship's speed about Home at the start, for the reverse burns' length.
    let v0 = {
        let mut p = plane(d, 5, Order::Sparse, 1, 8).unwrap();
        p.u.settle(T0);
        let (_, v) = p.u.rec(p.player).b.cartesian(T0).unwrap();
        let v = [emergent_universe::num::to_f64(v[0]), emergent_universe::num::to_f64(v[1])];
        (v[0] * v[0] + v[1] * v[1]).sqrt() * 299_792_458.0
    };
    let mut burns: Vec<(u8, u8, f64)> = [0u8, 4, 8, 12, 15].iter().map(|&l| (1u8, l, 2000.0)).collect();
    burns.extend([0u8, 4, 8].iter().map(|&l| (2u8, l, 0.5 * v0 / (g_of(&d, l) * 9.806_65))));
    let mut failures = Vec::new();
    let mut control_failed = false;
    for &(keys, level, seconds) in &burns {
        let coast = fly(d, 0, 0, seconds).unwrap();
        let reference = fly(cadence(6), keys, level, seconds).unwrap();
        let moved = (dist(reference.0, coast.0), dist(reference.1, coast.1));
        let err = |cfg: Config| -> Result<(f64, f64), String> {
            let r = fly(cfg, keys, level, seconds)?;
            Ok((dist(r.0, reference.0) / moved.0, dist(r.1, reference.1) / moved.1))
        };
        let name = format!("{} L{level} {seconds:.1} s", if keys == 1 { "forward" } else { "reverse" });
        let shipped = err(d);
        let finer = err(cadence(4));
        let coarse = err(cadence(-6));
        let show = |e: &Result<(f64, f64), String>| e.as_ref().map_or_else(|w| w.clone(), |e| format!("{:.2e}/{:.2e}", e.0, e.1));
        println!("{name:<24} moved {:.2e}/{:.2e}: shipped {}, 16x finer {}, 64x coarser {}", moved.0, moved.1, show(&shipped), show(&finer), show(&coarse));
        match (&shipped, &finer) {
            (Ok(s), Ok(f)) => {
                if s.0 > 3e-2 || s.1 > 3e-2 {
                    failures.push(format!("{name}: shipped error {:.3e}/{:.3e} over 3e-2", s.0, s.1));
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
    assert!(control_failed, "the control (64x coarser) must fail criterion 1 somewhere");
    assert!(failures.is_empty(), "T1 fails:\n{}", failures.join("\n"));
}
