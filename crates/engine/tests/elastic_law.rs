//! Elastic law (H0159): bounces, walls, sequential multi-contact impulses, the momentum
//! payload, and the exact momentum and energy ledgers.
use emergent_engine::{
    math::{r, Rational, Vec2},
    propagator::Inertial,
    runtime::{Body, Container, Payload},
    Command, Engine, WorkBudget,
};

fn ball(id: u64, x: i128, y: i128, vx: Rational, vy: Rational, mass: i128) -> Body {
    let mut b = Body::new(id, "ball", Inertial::new(0, Vec2::new(x, y), Vec2 { x: vx, y: vy }).unwrap(), r(1), r(mass));
    b.bounce = true;
    b
}

fn run(mut e: Engine, target: i128) -> Engine {
    while !e.advance(target, WorkBudget::new(1000)).unwrap().complete {}
    e
}

fn kinetic(e: &Engine, t: i128) -> Rational {
    e.state.bodies.values().map(|b| &b.mass * b.velocity_at(t).norm_squared() / r(2)).sum()
}

#[test]
fn equal_masses_exchange_velocities_head_on() {
    for quantum in [None, Some(1024)] {
        let e = Engine::new(1, vec![ball(1, 0, 0, r(1) / r(4), r(0), 1), ball(2, 10, 0, -(r(1) / r(4)), r(0), 1)], vec![])
            .unwrap()
            .with_elastic(None, quantum)
            .unwrap();
        let e = run(e, 40);
        assert_eq!(e.state.bodies[&1].velocity_at(40), Vec2 { x: -(r(1) / r(4)), y: r(0) }, "{quantum:?}");
        assert_eq!(e.state.bodies[&2].velocity_at(40), Vec2 { x: r(1) / r(4), y: r(0) }, "{quantum:?}");
        let contacts = e.sorted_events().iter().filter(|x| x.kind == "contact").count();
        assert_eq!(contacts, 1, "separating overlappers must not re-collide");
    }
}

#[test]
fn walls_reflect_and_record_momentum() {
    let container = Container { min: Vec2::new(0, 0), max: Vec2::new(20, 20) };
    let e = Engine::new(1, vec![ball(1, 10, 10, r(1) / r(2), r(1) / r(4), 3)], vec![])
        .unwrap()
        .with_elastic(Some(container), Some(1024))
        .unwrap();
    let e = run(e, 200);
    let b = &e.state.bodies[&1];
    let p = b.at(200);
    assert!(p.x >= r(0) && p.x <= r(20) && p.y >= r(0) && p.y <= r(20));
    let walls = e.sorted_events().iter().filter(|x| x.kind == "wall").count();
    assert!(walls >= 4);
    let dp = (b.velocity_at(200) - e.state.genesis_bodies[&1].velocity_at(0)) * b.mass.clone();
    let wm = e.state.elastic.as_ref().unwrap().wall_momentum.clone();
    assert_eq!(dp + wm, Vec2::zero(), "body momentum change must equal minus the wall momentum");
    assert_eq!(kinetic(&e, 200), r(3) * (r(1) / r(4) + r(1) / r(16)) / r(2), "walls conserve energy");
}

#[test]
fn simultaneous_contacts_stay_exactly_elastic() {
    // Ball 2 is struck from both sides in the same tick.
    let e = Engine::new(
        1,
        vec![
            ball(1, 0, 0, r(1) / r(4), r(0), 1),
            ball(2, 6, 0, r(0), r(0), 1),
            ball(3, 12, 0, -(r(1) / r(4)), r(0), 1),
        ],
        vec![],
    )
    .unwrap()
    .with_elastic(None, None)
    .unwrap();
    let before = kinetic(&e, 0);
    let e = run(e, 60);
    assert_eq!(kinetic(&e, 60), before, "exact fractions: sequential impulses conserve energy exactly");
    let residual: Rational = e.state.bodies.values().map(|b| b.energy_residual.clone()).sum();
    assert_eq!(residual, r(0));
}

#[test]
fn momentum_payload_divides_by_mass() {
    let mut e = Engine::new(
        1,
        vec![
            Body::new(1, "sender", Inertial::new(0, Vec2::new(0, 0), Vec2::zero()).unwrap(), r(1), r(1)),
            Body::new(2, "heavy", Inertial::new(0, Vec2::new(0, 50), Vec2::zero()).unwrap(), r(1), r(4)),
        ],
        vec![],
    )
    .unwrap();
    e.intervene(1, Command::SendSignal { target: 2, payload: Payload::Momentum { impulse: Vec2 { x: r(1), y: r(0) } } })
        .unwrap();
    let e = run(e, 100);
    assert_eq!(e.state.bodies[&2].velocity_at(100), Vec2 { x: r(1) / r(4), y: r(0) });
}
