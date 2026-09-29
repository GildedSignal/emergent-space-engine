//! The kick hook ([`Kickable`]): external integer velocity kicks at arbitrary committed ticks
//! give the same world and log digests in the event core as in the chronon reference, at every
//! kick and at the end. Kicks land on random subsets at random ticks (consecutive ticks, ticks
//! that also hold contacts, every body at once), in worlds with contacts, walls and velocity
//! classes, under the Newtonian and the relativistic laws; an illegal kick (past c) is refused
//! by both, and applies nothing.
use emergent_lattice::{
    chronon::Chronon,
    law::{Tick, World},
    worlds::{self, Rng},
    Kickable, Law, Response, Stepper,
};
use emergent_lattice_event::{crowded_axes, EventCore};

/// A random kick plan: (tick, one kick per body), ticks strictly increasing.
fn plan(n: usize, horizon: Tick, seed: u64, mag: i64) -> Vec<(Tick, Vec<[i64; 2]>)> {
    let mut rng = Rng(seed);
    let (mut t, mut out) = (0, Vec::new());
    loop {
        t += rng.range(1, 40);
        if t > horizon {
            return out;
        }
        // Every so often kick everyone; otherwise a random subset of about 1% to 30%.
        let density = if rng.next().is_multiple_of(8) { 100 } else { rng.range(1, 30) as u64 };
        let dk = (0..n)
            .map(|_| if rng.next() % 100 < density { [rng.range(-mag, mag), rng.range(-mag, mag)] } else { [0, 0] })
            .collect();
        out.push((t, dk));
    }
}

fn drive<S: Kickable>(s: &mut S, plan: &[(Tick, Vec<[i64; 2]>)], horizon: Tick) -> Vec<(String, String, bool)> {
    let mut seen = Vec::new();
    for (t, dk) in plan {
        s.run_to(*t);
        let ok = s.kick(dk).is_ok();
        let (w, l) = s.outcome();
        seen.push((w, l, ok));
    }
    s.run_to(horizon);
    let (w, l) = s.outcome();
    seen.push((w, l, true));
    seen
}

fn equal(name: &str, w0: &World, horizon: Tick, mag: i64, seed: u64) {
    let p = plan(w0.bodies.len(), horizon, seed, mag);
    let mut c = Chronon::new(w0.clone(), false).unwrap();
    let mut e = EventCore::new(w0.clone(), false).unwrap();
    let (a, b) = (drive(&mut c, &p, horizon), drive(&mut e, &p, horizon));
    for (i, (x, y)) in a.iter().zip(&b).enumerate() {
        assert_eq!(x, y, "{name}: kick {i} of {} (tick {:?})", p.len(), p.get(i).map(|k| k.0));
    }
    let refused = a.iter().filter(|x| !x.2).count();
    let mut plain = Chronon::new(w0.clone(), false).unwrap();
    plain.run_to(horizon);
    assert_ne!(plain.outcome(), c.outcome(), "{name}: the kicks must change the outcome");
    assert!(c.log().contacts > 0 || name.contains("axes"), "{name}: contacts expected");
    println!("{name}: {} kicks ({refused} refused), {} contacts, digests equal at every kick", p.len(), c.log().contacts);
}

#[test]
fn kicks_equal_the_chronon_reference_newtonian() {
    equal("mixed200", &worlds::mixed(200, 512, 21), 1500, 3, 1);
    equal("gas256", &worlds::gas(256, 0.1, 1024, 256, 3), 1200, 4, 2);
    equal("packed256", &worlds::packed(256, 8, 2, 1024, 1, 22), 800, 2, 3);
    equal("gas64-dense", &worlds::gas(64, 0.3, 64, 32, 4), 1500, 1, 4);
}

#[test]
fn kicks_equal_the_chronon_reference_relativistic() {
    let v1 = |w: World| w.with_law(Law::RelativisticV1).unwrap();
    equal("gas256-v1", &v1(worlds::gas(256, 0.1, 1024, 256, 3)), 1500, 3, 5);
    // Near c: most kicks past c are refused by both, and refuse everything (nothing applied).
    let mut hot = worlds::mixed(256, 256, 31);
    for b in &mut hot.bodies {
        b.response = Response::Bounce;
        b.k = [b.k[0] * 5 / 4, b.k[1] * 5 / 4];
    }
    equal("hot-mixed-v1", &hot.with_law(Law::Relativistic).unwrap(), 1200, 6, 6);
}

#[test]
fn kicks_equal_the_chronon_reference_with_velocity_classes() {
    // Columns and rows share velocities (classes of 64 or more); the kicks pull members out.
    let (w, _) = crowded_axes(512, 1024, 3);
    equal("axes512", &w, 1500, 2, 7);
    let (w, _) = crowded_axes(2048, 256, 4);
    equal("axes2048", &w, 1500, 1, 8);
}

#[test]
fn illegal_kicks_are_refused_by_both_and_apply_nothing() {
    let q = 1024;
    let mut w = worlds::mixed(64, q, 9);
    w.bodies[10].k = [1000, 0]; // 0.977c
    let w = w.with_law(Law::RelativisticV1).unwrap();
    let n = w.bodies.len();
    let mut c = Chronon::new(w.clone(), false).unwrap();
    let mut e = EventCore::new(w, false).unwrap();
    // At genesis (tick 0), where the event core still has its first indexing pending.
    let before = (c.outcome(), e.outcome());
    let mut dk = vec![[0, 0]; n];
    dk[3] = [1, 1];
    dk[10] = [30, 0]; // 1030 ≥ c
    assert!(c.kick(&dk).is_err() && e.kick(&dk).is_err(), "past c is refused");
    assert_eq!((c.outcome(), e.outcome()), before, "and nothing of it is applied, the legal part included");
    dk[10] = [10, 0];
    assert!(c.kick(&dk).is_ok() && e.kick(&dk).is_ok());
    c.run_to(300);
    e.run_to(300);
    assert_ne!(c.outcome(), before.0);
    assert_eq!(c.outcome(), e.outcome());
    assert!(c.kick(&dk[..3]).is_err() && e.kick(&dk[..3]).is_err(), "one kick per body");
}
