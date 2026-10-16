//! A purely integer witness for the drift mutant, independent of a physics tolerance.
//! Between epochs, capture the public carries; at a manual anchor compose positions
//! with the tube and compare with the independently accumulated owed displacement.
use super::scene::{frame, world, Q};
use emergent_engine::{AnchorPolicy, Battle};
use emergent_lattice::{chronon::Chronon, Body, Kickable, Response};
use emergent_lattice_event::EventCore;

fn witness<S: Kickable>(s: S) -> (usize, usize, i128) {
    let mut b = Battle::new(s, frame(), 1)
        .with_anchoring(AnchorPolicy {
            age_epochs: 100000,
            enforce_orbit_rule: true,
        })
        .unwrap();
    b.run_to(0).unwrap();
    let mut owed = vec![[0i128; 2]; b.carries().len()];
    let mut last = 0;
    let mut good = 0;
    let mut count = 0;
    let mut worst = 0;
    // Each interval is split at every kick boundary BEFORE integrating its new carry.
    for target in [7, 113, 255, 257, 511, 513, 997] {
        while last < target {
            let next = b.next_epoch_tick().unwrap().min(target);
            let carries = b.carries().to_vec();
            for i in 0..owed.len() {
                for c in 0..2 {
                    owed[i][c] += carries[i][c] as i128 * (next - last) as i128;
                }
            }
            b.run_to(next).unwrap();
            last = next;
        }
        let before = b.stepper().world();
        let old = b.tube_at(target).unwrap();
        let flush: Vec<[i128; 2]> = owed
            .iter()
            .map(|p| [(p[0] + (1 << 47)) >> 48, (p[1] + (1 << 47)) >> 48])
            .collect();
        let rep = b.reanchor().unwrap();
        assert!(!rep.refused && rep.handed_out.is_empty());
        let after = b.stepper().world();
        let new = b.tube_at(target).unwrap();
        for i in 0..owed.len() {
            for c in 0..2 {
                let old_origin = old.x[c]
                    + if c == 0 {
                        (old.radius as i128) << 32
                    } else {
                        0
                    };
                let new_origin = new.x[c]
                    + if c == 0 {
                        (new.radius as i128) << 32
                    } else {
                        0
                    };
                let expected = old_origin + ((before.bodies[i].x[c] as i128 + flush[i][c]) << 32);
                let got = new_origin + ((after.bodies[i].x[c] as i128) << 32);
                let delta = (got - expected).abs();
                worst = worst.max(delta);
                count += 1;
                good += (delta == 0) as usize;
                owed[i][c] -= flush[i][c] << 48;
            }
        }
    }
    (good, count, worst)
}
pub fn drift() -> (bool, String) {
    let bodies = vec![
        Body::new(1, [4100000, 11000], [13, -519], 2, 1, Response::Pass),
        Body::new(2, [4320000, -17000], [-7, -511], 5, 1, Response::Pass),
        Body::new(3, [3910000, 31000], [17, -491], 3, 1, Response::Pass),
    ];
    let w = world(bodies, Q);
    let a = witness(Chronon::new(w.clone(), false).unwrap());
    let b = witness(EventCore::new(w, false).unwrap());
    let good = a.0 + b.0;
    let total = a.1 + b.1;
    (
        good == total,
        format!(
            "settled={good}/{total} position_delta={} unit=2^-32 required=0",
            a.2.max(b.2)
        ),
    )
}
