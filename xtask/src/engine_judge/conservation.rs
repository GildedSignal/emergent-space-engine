//! Check conserved quantities by reconstructing every body's velocity in the SAME
//! pre-event rotating frame. Never trust AnchorReport.dp as a conservation oracle.
use super::scene::{frame, world, Rng, Q, R};
use emergent_engine::{AnchorPolicy, Battle, Tube};
use emergent_lattice::{chronon::Chronon, Body, Kickable, Response};
use emergent_lattice_event::EventCore;
use std::collections::BTreeSet;

const SCALE: i128 = 1 << 48;
const ENERGY_SCALE: i128 = 1 << 96; // one quantum is one m*k² unit, same as lattice energy
fn rounded(x: i128, bits: u32) -> i128 {
    (x + (1i128 << (bits - 1))) >> bits
}
fn velocities<S: Kickable>(b: &Battle<S>) -> Vec<[i128; 2]> {
    let mut m = Vec::new();
    b.stepper().motions(&mut m);
    m.iter()
        .zip(b.carries())
        .map(|(m, c)| {
            [
                m.k[0] as i128 * SCALE + c[0] as i128,
                m.k[1] as i128 * SCALE + c[1] as i128,
            ]
        })
        .collect()
}
fn totals(masses: &[i64], v: &[[i128; 2]]) -> ([i128; 2], i128) {
    let mut p = [0; 2];
    let mut e = 0;
    for (&mass, v) in masses.iter().zip(v) {
        for c in 0..2 {
            p[c] += mass as i128 * v[c];
            e += mass as i128 * v[c] * v[c];
        }
    }
    (p, e)
}
/// Invert the change in the axes' angular velocity in one operation on the composed
/// parent position. Per-component integer roundings are exactly what this gate audits.
fn common_velocity(v: [i128; 2], t: &Tube, x: [i64; 2], old_n: u64) -> [i128; 2] {
    let dn = old_n as i128 - t.n as i128;
    let px = ((t.radius as i128) << 32) + t.x[0] + ((x[0] as i128) << 32);
    let py = t.x[1] + ((x[1] as i128) << 32);
    [
        v[0] + t.v[0] + rounded(dn * py, 44),
        v[1] + t.v[1] - rounded(dn * px, 44),
    ]
}
fn check<S: Kickable>(s: S) -> (i128, i128, u64, String) {
    let masses: Vec<_> = s.world().bodies.iter().map(|b| b.mass).collect();
    let mut b = Battle::new(s, frame(), 1)
        .with_anchoring(AnchorPolicy {
            age_epochs: 100000,
            enforce_orbit_rule: true,
        })
        .unwrap();
    let mut worst_p = 0;
    let mut worst_e = 0;
    let mut moves = 0;
    let mut first = String::new();
    for tick in [0, 1, 17, 123, 257, 999] {
        b.run_to(tick).unwrap();
        let t0 = b.tube_at(tick).unwrap();
        let before: Vec<_> = velocities(&b)
            .into_iter()
            .map(|v| [v[0] + t0.v[0], v[1] + t0.v[1]])
            .collect();
        let (p0, e0) = totals(&masses, &before);
        let rep = b.reanchor().unwrap();
        if rep.refused {
            continue;
        }
        moves += rep.moved as u64;
        let t1 = b.tube_at(tick).unwrap();
        let mut motions = Vec::new();
        b.stepper().motions(&mut motions);
        let after: Vec<_> = velocities(&b)
            .iter()
            .zip(&motions)
            .map(|(&v, m)| common_velocity(v, &t1, m.x, t0.n))
            .collect();
        let (p1, e1) = totals(&masses, &after);
        let pe = (p1[0] - p0[0]).abs().max((p1[1] - p0[1]).abs());
        // Subtract before rounding; bounding a difference to one energy quantum.
        let ee = (e1 - e0).abs();
        worst_p = worst_p.max(pe);
        worst_e = worst_e.max(ee);
        if pe != 0 && first.is_empty() {
            first = format!(
                "tick={tick} dn={} dp={:?} centre={:?}",
                t0.n as i128 - t1.n as i128,
                [p1[0] - p0[0], p1[1] - p0[1]],
                rep.centre
            );
        }
    }
    (worst_p, worst_e, moves, first)
}
pub fn conservation() -> (bool, String) {
    let mut worst_p = 0;
    let mut worst_e = 0;
    let mut moves = 0;
    let mut first = String::new();
    for seed in [5, 17, 81, 191] {
        let mut rng = Rng(seed);
        let bodies = (0..7)
            .map(|i| {
                Body::new(
                    i + 1,
                    [rng.range(-80000, 160000), rng.range(-50000, 50000)],
                    [rng.range(-25, 25), rng.range(-25, 25)],
                    rng.range(1, 7),
                    1,
                    Response::Pass,
                )
            })
            .collect();
        let w = world(bodies, Q);
        for row in [
            check(Chronon::new(w.clone(), false).unwrap()),
            check(EventCore::new(w, false).unwrap()),
        ] {
            worst_p = worst_p.max(row.0);
            worst_e = worst_e.max(row.1);
            moves += row.2;
            if !row.3.is_empty() && first.is_empty() {
                first = format!("seed={seed} {}", row.3);
            }
        }
    }
    (worst_p==0 && worst_e<=ENERGY_SCALE && moves>0,format!("anchors=48 circle_moves={moves} momentum_delta={worst_p} unit=2^-48 required=0 energy_delta_quanta={:.3e} allowed=1 first={first:?}",worst_e as f64/ENERGY_SCALE as f64))
}

fn ledger_one<S: Kickable>(s: S) -> (bool, usize, String) {
    let w0 = s.world();
    let masses: Vec<_> = w0.bodies.iter().map(|b| b.mass).collect();
    let total: i64 = masses.iter().sum();
    let mut b = Battle::new(s, frame(), 1)
        .with_anchoring(AnchorPolicy {
            age_epochs: 4,
            enforce_orbit_rule: true,
        })
        .unwrap();
    b.run_to(0).unwrap();
    let mut ok = true;
    let mut first = String::new();
    for tick in [0, 1, 256, 1024, 4096] {
        b.run_to(tick).unwrap();
        let ledger = b.handoffs();
        let ids: BTreeSet<_> = ledger.iter().map(|h| h.index).collect();
        let out_mass: i64 = ids.iter().map(|&i| masses[i]).sum();
        let live_mass: i64 = b
            .active()
            .iter()
            .enumerate()
            .filter(|(_, a)| **a)
            .map(|(i, _)| masses[i])
            .sum();
        let valid = ids.len() == ledger.len()
            && ledger.len() as u64 == b.stats().handed_out
            && out_mass + live_mass == total
            && b.active()
                .iter()
                .enumerate()
                .all(|(i, &a)| a != ids.contains(&i))
            && b.stepper().world().bodies.len() == masses.len();
        ok &= valid;
        if !valid && first.is_empty() {
            first = format!("tick={tick} total={total} live={live_mass} out={out_mass}");
        }
        if tick == 0 {
            // Handoff snapshot composes with its tube to the original parent position,
            // including the correction from any move of the reference circle.
            for h in ledger {
                let px = ((h.x[0] as i128 + h.tube.radius as i128 - R as i128) << 32) + h.tube.x[0];
                let py = ((h.x[1] as i128) << 32) + h.tube.x[1];
                ok &= [px, py]
                    == [
                        (w0.bodies[h.index].x[0] as i128) << 32,
                        (w0.bodies[h.index].x[1] as i128) << 32,
                    ];
            }
        }
    }
    (ok, b.handoffs().len(), first)
}
pub fn ledger() -> (bool, String) {
    let bodies = vec![
        Body::new(1, [100000, 0], [0, 0], 50, 1, Response::Pass),
        Body::new(2, [120000, 1000], [3, -1], 3, 1, Response::Pass),
        Body::new(3, [R / 8, 0], [10, 0], 1, 1, Response::Pass),
        Body::new(4, [-R / 8, 0], [-10, 0], 1, 1, Response::Pass),
    ];
    let w = world(bodies, Q);
    let a = ledger_one(Chronon::new(w.clone(), false).unwrap());
    let b = ledger_one(EventCore::new(w, false).unwrap());
    (
        a.0 && b.0 && a.1 == 2 && b.1 == 2,
        format!(
            "handed_out_lockstep={} sparse={} mass=55 unique_and_balanced={} first={:?}",
            a.1,
            b.1,
            a.0 && b.0,
            if a.2.is_empty() { b.2 } else { a.2 }
        ),
    )
}

/// A narrow exact Galilean control, independent of circle moves and unrelated to E4's
/// inverse-rotation check. Used in the judge's self-test, not as a substitute for E4.
#[cfg(test)]
mod tests {
    use super::*;
    use emergent_lattice::Motion;
    #[test]
    fn exact_recentre_composes_velocities_without_a_report_ledger() {
        let masses = [2, 5, 3];
        let motions = [
            Motion {
                x: [1, 2],
                k: [3, -7],
            },
            Motion {
                x: [4, 5],
                k: [-2, 9],
            },
            Motion {
                x: [-4, 2],
                k: [6, -1],
            },
        ];
        let carries = [[31, -19], [8, 4], [-51, 71]];
        let r = emergent_engine::recentre(&masses, &motions, &carries, 1).unwrap();
        for i in 0..3 {
            for c in 0..2 {
                assert_eq!(
                    (motions[i].k[c] + r.dk[i][c]) as i128 * SCALE
                        + r.carries[i][c] as i128
                        + r.velocity[c],
                    motions[i].k[c] as i128 * SCALE + carries[i][c] as i128
                );
            }
        }
    }
}
