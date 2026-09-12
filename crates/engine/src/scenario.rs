//! Reproducible laboratory fixtures; scenario identity participates in provenance.
use crate::{
    math::{r, Vec2},
    population::Family,
    propagator::Inertial,
    runtime::{Body, Command, Payload},
    Engine, EngineError,
};
pub const JULIAN_YEAR_TICKS: i128 = 31_557_600;
pub const TEN_BILLION_YEARS: i128 = 10_000_000_000 * JULIAN_YEAR_TICKS;

fn body(id: u64, name: &str, x: i128, y: i128, vx: i128, den: i128, radius: i128) -> Body {
    Body::new(
        id,
        name,
        Inertial::new(
            0,
            Vec2::new(x, y),
            Vec2 {
                x: r(vx) / r(den),
                y: r(0),
            },
        )
        .unwrap(),
        r(radius),
        r(1),
    )
}
/// Emitter -> moving courier -> contact -> outgoing signal, plus isolated witness.
pub fn causal_relay() -> Result<Engine, EngineError> {
    let emitter = body(1, "Emitter", 0, 0, 0, 1, 0);
    let mut courier = body(2, "Courier", 10, 0, 1, 4, 1);
    courier.stop_on_contact = true;
    courier.notify_on_contact = Some(1);
    let target = body(3, "Receiver", 30, 0, 0, 1, 1);
    let witness = body(4, "Independent witness", 0, 1000, 0, 1, 1);
    let mut e = Engine::new(0x0E5C_A051, vec![emitter, courier, target, witness], vec![])?;
    e.intervene(
        1,
        Command::SendSignal {
            target: 2,
            payload: Payload::Impulse {
                delta: Vec2 {
                    x: r(1) / r(4),
                    y: r(0),
                },
            },
        },
    )?;
    Ok(e)
}

/// Spatially separated, stable identity families. Physics scope is explicitly inertial.
pub fn population_fixture(count: u64, number_of_families: usize) -> Result<Engine, EngineError> {
    if count == 0 || number_of_families == 0 {
        return Err(EngineError::Invalid(
            "positive population and family count required".into(),
        ));
    }
    let n = (number_of_families as u64).min(count);
    let mut families = Vec::new();
    let mut first = 10_000;
    for lane in 0..n {
        let len = count / n + u64::from(lane < count % n);
        families.push(Family {
            name: format!("Transit {:03}", lane + 1),
            first_id: first,
            count: len,
            offset: 0,
            trajectory: Inertial::new(
                0,
                Vec2::new(0, 100_000 + lane as i128 * 1000),
                Vec2 {
                    x: r(1) / r(4),
                    y: r(0),
                },
            )?,
            stride: Vec2::new(64, 0),
            radius: r(1),
            mass: r(1),
        });
        first = first
            .checked_add(len)
            .ok_or_else(|| EngineError::Invalid("identity overflow".into()))?;
    }
    Engine::new(0x0E5C_A051, vec![], families)
}

pub fn observatory() -> Result<Engine, EngineError> {
    let mut e = population_fixture(1_000_000_000, 16)?;
    let mut entities = vec![
        body(1, "LUMINOR · Survey vessel", -170, -55, 1, 4, 3),
        body(2, "ARCHIMEDES · Listening station", 160, 35, 0, 1, 9),
        body(3, "PELAGIC · Laboratory occluder", 15, 110, 0, 1, 34),
        body(4, "ASTER · Navigation beacon", -70, -140, 0, 1, 5),
        body(5, "KESTREL · Courier", 210, -120, -1, 5, 2),
    ];
    entities[0].stop_on_contact = true;
    // Recreate with the initial entities included in the authoritative scenario root.
    e = Engine::new(e.state.seed, entities, e.state.families)?;
    e.intervene(
        2,
        Command::SendSignal {
            target: 1,
            payload: Payload::Ping,
        },
    )?;
    e.advance_fully(480)?;
    Ok(e)
}
