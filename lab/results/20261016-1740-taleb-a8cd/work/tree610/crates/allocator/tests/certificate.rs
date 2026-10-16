//! Adversarial check of the fact the certificate rests on: in a containerless world, once a
//! centre passes the initial extent in some direction, that direction's extent never
//! shrinks again. Hence the extent over any interval is the hull of the extents at its ends.
use emergent_allocator::{geom::Aabb, scenes};
use emergent_lattice::{chronon::Chronon, law::{Law, Response, World}, worlds, Stepper};

fn extents(w: &World) -> [i64; 4] {
    let b = Aabb::of(w.bodies.iter().map(|b| &b.x));
    [b.hi[0], b.hi[1], -b.lo[0], -b.lo[1]]
}

fn check(w0: World, chronons: i64, name: &str) -> u64 {
    let mut c = Chronon::new(w0.clone(), false).unwrap();
    let mut seen: Vec<[i64; 4]> = vec![extents(&w0)];
    for t in 1..=chronons {
        c.advance(w0.tick + t, u64::MAX);
        seen.push(extents(&c.world()));
    }
    for d in 0..4 {
        let m0 = seen[0][d];
        let mut best = i64::MIN;
        for (s, e) in seen.iter().enumerate() {
            if best > m0 {
                assert!(e[d] >= best, "{name}: direction {d} shrank at chronon {s} after passing the start extent");
            }
            best = best.max(e[d]);
        }
        // The window certificate: max over the interval = max of its two ends.
        let (lo, hi) = (seen[0][d], seen[seen.len() - 1][d]);
        assert_eq!(best, lo.max(hi), "{name}: direction {d} interval extent");
    }
    c.log().contacts
}

#[test]
fn outward_extent_is_monotone_after_it_grows() {
    let mut contacts = 0;
    for seed in 0..12 {
        contacts += check(scenes::loose_mixed(60, 256, seed), 600, "loose mixed");
        contacts += check(worlds::random(80, 40, 256, 1, seed, Response::Bounce), 400, "dense bouncers");
        contacts += check(worlds::packed(64, 3, 1, 256, 1, seed), 300, "packed stops");
        // Unequal masses: light bodies are kicked past c, the case tracked speeds exist for.
        let mut w = scenes::loose_mixed(60, 1024, seed + 100);
        for b in w.bodies.iter_mut() {
            b.mass = if b.id % 2 == 0 { 64 } else { 1 };
        }
        contacts += check(w.clone(), 400, "mass ratio 64");
        // The relativistic bounce reflects 4-momenta across a normal whose spatial part lies
        // along the line of centres: the kick's sign argument is the same, magnitudes differ.
        contacts += check(w.with_law(Law::Relativistic).unwrap(), 400, "relativistic mass ratio 64");
        contacts += check(scenes::loose_gas(300, 256, 180, seed, 1, [0, 0]).with_law(Law::Relativistic).unwrap(), 300, "relativistic fast gas");
    }
    assert!(contacts > 2000, "the check must see many responses, saw {contacts}");
}
