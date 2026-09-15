//! I2 started: family + in-flight signal on the I1 connected diagnostic scene.
//! This is not the I2 exit. Re-merge, selective history, indexed range
//! reception and unequal certified cuts remain missing.

use emergent_engine::{
    coupled_adapter::{CANONICAL_GRAVITY_ACCEPTANCE, BEACON_ID, EMITTER_ID, SHIP_ID},
    math::{r, Vec2},
    population::Family,
    propagator::Inertial,
    runtime::{Body, Command, Engine, Payload},
    WorkBudget,
};

fn body(id: u64, name: &str, x: i128, y: i128, radius: i128) -> Body {
    Body::new(
        id,
        name,
        Inertial::new(0, Vec2::new(x, y), Vec2::zero()).unwrap(),
        r(radius),
        r(1),
    )
}

#[test]
fn i2_started_family_perturbs_while_signal_in_flight_on_diagnostic_scene() {
    let emitter = body(EMITTER_ID, "emitter", 0, 0, 0);
    let mut ship = body(SHIP_ID, "test-ship", 8, 0, 1);
    ship.stop_on_contact = true;
    let mut beacon = body(BEACON_ID, "beacon", 14, 0, 1);
    beacon.stop_on_contact = true;
    let family = Family::affine(
        "i2-lane",
        10_000,
        8,
        0,
        Inertial::new(
            0,
            Vec2::new(0, 1000),
            Vec2 {
                x: r(1) / r(8),
                y: r(0),
            },
        )
        .unwrap(),
        Vec2::new(32, 0),
        r(1),
        r(1),
    );
    let mut engine = Engine::new(0x12C0_11EC, vec![emitter, ship, beacon], vec![family]).unwrap();
    engine.attach_connected_laboratory().unwrap();

    let _ = engine
        .intervene(
            EMITTER_ID,
            Command::SendSignal {
                target: SHIP_ID,
                payload: Payload::Ping,
            },
        )
        .unwrap();
    assert!(
        !engine.state.signals.is_empty(),
        "signal must be in flight before family extraction"
    );

    let neighbor = engine.decode(10_001).unwrap();
    engine
        .intervene(
            10_000,
            Command::SetVelocity {
                velocity: Vec2::zero(),
            },
        )
        .unwrap();
    assert!(engine.state.bodies.contains_key(&10_000));
    assert_eq!(engine.decode(10_001).unwrap(), neighbor);

    let mut pending = 0usize;
    loop {
        let _ = engine.advance(0, WorkBudget::new(1)).unwrap();
        if engine.coupled.as_ref().is_some_and(|d| d.is_ready()) {
            break;
        }
        pending += 1;
        assert!(pending < 50_000);
    }
    assert!(engine.coupled.as_ref().unwrap().is_ready());
    assert_eq!(CANONICAL_GRAVITY_ACCEPTANCE, "diagnostic-only");
}
