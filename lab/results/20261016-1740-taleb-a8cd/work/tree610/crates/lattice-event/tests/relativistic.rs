//! The event core under the relativistic law: bit-identical to the chronon reference,
//! including slicing, and nothing massive reaches c.
use emergent_lattice::{chronon::Chronon, worlds, Law, Response, Stepper, World};
use emergent_lattice_event::EventCore;

fn hot_mixed(n: u64, q: i64, seed: u64) -> World {
    let mut w = worlds::mixed(n, q, seed);
    for b in &mut w.bodies {
        b.response = Response::Bounce;
        b.k = [b.k[0] * 5 / 4, b.k[1] * 5 / 4]; // up to 0.88c at genesis
    }
    w.with_law(Law::Relativistic).unwrap()
}

#[test]
fn relativistic_worlds_equal_the_chronon_reference() {
    let v1 = |w: World| World { law: Law::RelativisticV1, ..w };
    let cases = [
        (worlds::gas(256, 0.1, 1024, 256, 3).with_law(Law::Relativistic).unwrap(), 2048),
        (hot_mixed(256, 256, 31), 3000),
        (hot_mixed(1024, 512, 32), 1500),
        (worlds::gas(256, 0.1, 1024, 256, 3).with_law(Law::RelativisticV1).unwrap(), 2048),
        (v1(hot_mixed(256, 256, 31)), 3000),
        (worlds::gas(256, 0.1, 4096, 16, 3).with_law(Law::RelativisticV1).unwrap(), 20000),
    ];
    for (i, (w0, horizon)) in cases.into_iter().enumerate() {
        let mut r = Chronon::new(w0.clone(), false).unwrap();
        r.run_to(horizon);
        assert!(r.log().contacts > if i == 5 { 100 } else { 500 }, "case {i} must collide ({})", r.log().contacts);
        for budget in [u64::MAX, 97] {
            let mut e = EventCore::new(w0.clone(), false).unwrap();
            while e.tick() < horizon {
                e.advance(horizon, budget);
            }
            assert_eq!(e.outcome(), r.outcome(), "case {i} budget {budget}");
            let w = e.world();
            assert!(w.bodies.iter().all(|b| (b.k[0] as i128).pow(2) + (b.k[1] as i128).pow(2) < (w.q as i128).pow(2)), "case {i}: c");
        }
    }
}
