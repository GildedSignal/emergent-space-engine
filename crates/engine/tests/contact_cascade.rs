//! Stop-on-contact cascades (scale ladder C1, H0157): resting bodies must not re-collide, and a
//! body changed by one batch must have its new pairs searched before the next batch commits.
use emergent_engine::{
    math::{r, Rational, Vec2},
    propagator::Inertial,
    runtime::Body,
    Engine, WorkBudget,
};

fn stopper(id: u64, x: Rational, y: Rational, vx: Rational, vy: Rational) -> Body {
    let mut b = Body::new(id, "cascade", Inertial::new(0, Vec2 { x, y }, Vec2 { x: vx, y: vy }).unwrap(), r(1), r(1));
    b.stop_on_contact = true;
    b
}

fn contacts(e: &Engine) -> Vec<(i128, u64, u64)> {
    let mut v: Vec<_> = e
        .sorted_events()
        .into_iter()
        .filter(|ev| ev.kind == "contact")
        .map(|ev| (ev.tick, ev.subjects[0].min(ev.subjects[1]), ev.subjects[0].max(ev.subjects[1])))
        .collect();
    v.sort_unstable();
    v
}

fn run(mut e: Engine, target: i128, budget: usize) -> Engine {
    while !e.advance(target, WorkBudget::new(budget)).unwrap().complete {}
    e
}

#[test]
fn resting_overlapping_bodies_do_not_recollide_every_tick() {
    // 1 and 2 meet in tick 13 and stop slightly overlapping; 3 reaches the resting 1 in tick 14.
    let world = || {
        Engine::new(
            1,
            vec![
                stopper(1, r(0), r(0), r(7) / r(20), r(0)),
                stopper(2, r(11), r(0), -(r(7) / r(20)), r(0)),
                stopper(3, -(r(21) / r(5)), r(0), r(1) / r(2), r(0)),
            ],
            vec![],
        )
        .unwrap()
    };
    for budget in [1_000_000, 1] {
        let e = run(world(), 40, budget);
        assert_eq!(contacts(&e), vec![(13, 1, 2), (14, 1, 3)], "budget {budget}");
        assert_eq!(e.independent_inertial_facts(40).unwrap().contacts, contacts(&e));
        assert_eq!(e.state.bodies[&1].segments.len(), 2, "a stop at rest opens no new revision");
    }
}

struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
    fn range(&mut self, lo: i128, hi: i128) -> i128 {
        lo + (self.next() as u128 % (hi - lo + 1) as u128) as i128
    }
}

/// The scale-ladder C1 world at 64 bodies (seed and layout from scenarios/scale-ladder-v1.json).
fn packed64() -> Engine {
    let n = 64u64;
    let mut rng = Rng(2_718_281_828u64 ^ n ^ 0xC1);
    let mut bodies = Vec::new();
    for i in 0..n as i128 {
        let p = [(i % 8) * 8 + rng.range(-2, 2), (i / 8) * 8 + rng.range(-2, 2)];
        let v = [rng.range(-512, 512), rng.range(-512, 512)];
        bodies.push(stopper(i as u64 + 1, r(p[0]), r(p[1]), r(v[0]) / r(1024), r(v[1]) / r(1024)));
    }
    Engine::new(2_718_281_828, bodies, vec![]).unwrap()
}

#[test]
fn changed_bodies_are_repaired_before_the_next_commit() {
    // Body 55 stops in tick 15; body 47 reaches it in tick 17. Before the fix the next commit
    // overtook 55's repair: the contact came one tick late, or never at small budgets.
    let horizon = 40;
    let big = run(packed64(), horizon, 1_000_000);
    let audit = big.independent_inertial_facts(horizon).unwrap().contacts;
    assert_eq!(contacts(&big), audit);
    assert!(audit.contains(&(17, 47, 55)));
    for budget in [64, 8] {
        let small = run(packed64(), horizon, budget);
        assert_eq!(contacts(&small), audit, "budget {budget}");
        assert_eq!(small.history_digest(horizon).unwrap(), big.history_digest(horizon).unwrap());
    }
}
