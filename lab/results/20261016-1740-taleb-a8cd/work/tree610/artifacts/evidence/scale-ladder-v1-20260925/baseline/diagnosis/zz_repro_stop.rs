//! TEMPORARY repro (delete after use): contact with a body that stopped in the previous bin.
use emergent_engine::{math::{r, Vec2}, propagator::Inertial, runtime::Body, Engine, WorkBudget};
fn b(id: u64, x: emergent_engine::math::Rational, v: emergent_engine::math::Rational) -> Body {
    let mut b = Body::new(id, "t", Inertial::new(0, Vec2 { x, y: r(0) }, Vec2 { x: v, y: r(0) }).unwrap(), r(1), r(1));
    b.stop_on_contact = true;
    b
}
fn main() {
    for budget in [1_000_000usize, 64, 8, 1] {
        let bodies = vec![
            b(1, r(0), r(7) / r(20)),
            b(2, r(11), -(r(7) / r(20))),
            b(3, -(r(21) / r(5)), r(1) / r(2)),
        ];
        let mut e = Engine::new(1, bodies, vec![]).unwrap();
        while !e.advance(40, WorkBudget::new(budget)).unwrap().complete {}
        let ev: Vec<_> = e.sorted_events().into_iter().map(|x| (x.tick, x.kind.clone(), x.subjects.clone())).collect();
        let audit = e.independent_inertial_facts(40).unwrap().contacts;
        println!("budget {budget}: events {ev:?}\n   audit {audit:?}");
        for id in 1..=3 { println!("   body {id} segments {:?}", e.state.bodies[&id].segments.iter().map(|s| (s.epoch, s.origin.x.to_string(), s.velocity.x.to_string())).collect::<Vec<_>>()); }
    }
}
