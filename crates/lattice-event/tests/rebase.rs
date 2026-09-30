//! The rebase hook ([`Kickable::rebase`]): re-expressing the world in a moved frame (every
//! position shifted, by the same or by its own amount, some velocities changed) at arbitrary
//! committed ticks gives the same
//! world and log digests in the event core as in the chronon reference, at every rebase and at
//! the end. Worlds without walls (a wall does not move with the frame): random discs (bounce,
//! pass, stop mixed), a battle with velocity classes, the crowded axes; under the Newtonian
//! and the relativistic laws. A rebase that would leave the exactness range, or break c, is
//! refused by both and applies nothing; so is any rebase of a world with walls.
use emergent_lattice::{
    chronon::Chronon,
    law::{Tick, World},
    worlds::{self, Rng},
    Kickable, Law, Response, Stepper,
};
use emergent_lattice_event::{crowded_axes, EventCore};

/// (tick, one shift per body, one kick per body): every body shifted by the same up to ±`reach` (a
/// frame move) or, one time in three, by its own (a caller settling positions), and kicks on about a
/// quarter of the bodies.
type Plan = Vec<(Tick, Vec<[i64; 2]>, Vec<[i64; 2]>)>;

fn plan(n: usize, horizon: Tick, seed: u64, reach: i64, mag: i64) -> Plan {
    let mut rng = Rng(seed);
    let (mut t, mut out) = (0, Vec::new());
    loop {
        t += rng.range(1, 60);
        if t > horizon {
            return out;
        }
        let shift = [rng.range(-reach, reach), rng.range(-reach, reach)];
        let own = rng.next().is_multiple_of(3);
        let shifts = (0..n).map(|_| if own { [rng.range(-reach / 8, reach / 8), rng.range(-reach / 8, reach / 8)] } else { shift }).collect();
        let all = rng.next().is_multiple_of(4);
        let dk = (0..n).map(|_| if all || rng.next() % 4 == 0 { [rng.range(-mag, mag), rng.range(-mag, mag)] } else { [0, 0] }).collect();
        out.push((t, shifts, dk));
    }
}

fn drive<S: Kickable>(s: &mut S, plan: &Plan, horizon: Tick) -> Vec<(String, String, bool)> {
    let mut seen = Vec::new();
    for (t, shifts, dk) in plan {
        s.run_to(*t);
        let ok = s.rebase(shifts, dk).is_ok();
        let (w, l) = s.outcome();
        seen.push((w, l, ok));
    }
    s.run_to(horizon);
    let (w, l) = s.outcome();
    seen.push((w, l, true));
    seen
}

fn equal(name: &str, w0: &World, horizon: Tick, reach: i64, mag: i64, seed: u64) {
    let p = plan(w0.bodies.len(), horizon, seed, reach, mag);
    let mut c = Chronon::new(w0.clone(), false).unwrap();
    let mut e = EventCore::new(w0.clone(), false).unwrap();
    let (a, b) = (drive(&mut c, &p, horizon), drive(&mut e, &p, horizon));
    for (i, (x, y)) in a.iter().zip(&b).enumerate() {
        assert_eq!(x, y, "{name}: rebase {i} of {} (tick {:?})", p.len(), p.get(i).map(|k| k.0));
    }
    let refused = a.iter().filter(|x| !x.2).count();
    let mut plain = Chronon::new(w0.clone(), false).unwrap();
    plain.run_to(horizon);
    assert_ne!(plain.outcome(), c.outcome(), "{name}: the rebases must change the outcome");
    println!("{name}: {} rebases ({refused} refused), {} contacts, digests equal at every rebase", p.len(), c.log().contacts);
}

#[test]
fn rebases_equal_the_chronon_reference_newtonian() {
    equal("random256", &worlds::random(256, 4096, 512, 4, 21, Response::Bounce), 1200, 300, 3, 1);
    equal("packed256", &worlds::packed(256, 8, 2, 1024, 1, 22), 800, 2000, 2, 2);
    equal("random128-stop", &worlds::random(128, 900, 256, 4, 23, Response::Stop), 800, 50, 1, 3);
}

#[test]
fn rebases_equal_the_chronon_reference_relativistic() {
    let v1 = |w: World| w.with_law(Law::RelativisticV1).unwrap();
    equal("random256-v1", &v1(worlds::random(256, 4096, 512, 4, 24, Response::Bounce)), 1000, 300, 3, 4);
    let mut hot = worlds::random(200, 4096, 256, 4, 25, Response::Bounce);
    for b in &mut hot.bodies {
        b.k = [b.k[0] * 5 / 4, b.k[1] * 5 / 4];
    }
    equal("hot-v1", &hot.with_law(Law::Relativistic).unwrap(), 800, 100, 6, 5);
}

#[test]
fn rebases_equal_the_chronon_reference_with_velocity_classes() {
    let (w, _) = crowded_axes(512, 1024, 3);
    equal("axes512", &w, 1200, 4000, 2, 6);
    let (w, _) = crowded_axes(1024, 256, 4);
    equal("axes1024", &w, 1000, 800, 1, 7);
}

#[test]
fn illegal_rebases_are_refused_by_both_and_apply_nothing() {
    let q = 1024;
    let mut w = worlds::random(64, 4096, q, 4, 9, Response::Bounce);
    w.bodies[10].k = [1000, 0]; // 0.977c
    let w = w.with_law(Law::RelativisticV1).unwrap();
    let n = w.bodies.len();
    let mut c = Chronon::new(w.clone(), false).unwrap();
    let mut e = EventCore::new(w, false).unwrap();
    c.run_to(5);
    e.run_to(5);
    let before = (c.outcome(), e.outcome());
    let mut dk = vec![[0, 0]; n];
    let shift = |s: [i64; 2]| vec![s; n];
    dk[10] = [30, 0]; // 1030 ≥ c
    assert!(c.rebase(&shift([1, 1]), &dk).is_err() && e.rebase(&shift([1, 1]), &dk).is_err(), "past c is refused");
    assert_eq!((c.outcome(), e.outcome()), before, "and nothing of it is applied, the shift included");
    dk[10] = [0, 0];
    let far = 1i64 << 39;
    assert!(c.rebase(&shift([far, 0]), &dk).is_err() && e.rebase(&shift([far, 0]), &dk).is_err(), "outside 2^39 is refused");
    assert_eq!((c.outcome(), e.outcome()), before);
    assert!(c.rebase(&shift([0, 0])[..3], &dk[..3]).is_err() && e.rebase(&shift([0, 0])[..3], &dk[..3]).is_err(), "one shift and one kick per body");
    // A pure shift changes positions only: no revision, and the digests still agree.
    assert!(c.rebase(&shift([7, -3]), &dk).is_ok() && e.rebase(&shift([7, -3]), &dk).is_ok());
    c.run_to(200);
    e.run_to(200);
    assert_ne!(c.outcome(), before.0);
    assert_eq!(c.outcome(), e.outcome());
    // Walls do not move with the frame: refused.
    let boxed = worlds::mixed(32, 256, 3);
    let (mut c, mut e) = (Chronon::new(boxed.clone(), false).unwrap(), EventCore::new(boxed.clone(), false).unwrap());
    let dk = vec![[0, 0]; boxed.bodies.len()];
    assert!(c.rebase(&vec![[1, 0]; dk.len()], &dk).is_err() && e.rebase(&vec![[1, 0]; dk.len()], &dk).is_err());
}
