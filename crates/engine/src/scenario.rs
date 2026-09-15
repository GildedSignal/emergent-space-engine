//! Reproducible laboratory fixtures; scenario identity participates in provenance.
//! Interaction fixtures are compiled scripted IR, not a physical law.
use crate::{
    math::{r, Vec2},
    population::{Family, PhaseGenerator},
    propagator::Inertial,
    runtime::{Body, Command, Payload},
    Engine, EngineError,
};
/// Scripted ship interactions compiled as external certificates. Not a gravity law.
pub const SCRIPTED_INTERACTION: &str = "scripted-interaction-v1";
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
        families.push(Family::affine(
            format!("Transit {:03}", lane + 1),
            first,
            len,
            0,
            Inertial::new(
                0,
                Vec2::new(0, 100_000 + lane as i128 * 1000),
                Vec2 {
                    x: r(1) / r(4),
                    y: r(0),
                },
            )?,
            Vec2::new(64, 0),
            r(1),
            r(1),
        ));
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

/// Mixed-velocity explicit bodies for cooperative scan / stutter fixtures.
pub fn mixed_velocity_bodies(count: u64) -> Result<Engine, EngineError> {
    if count == 0 {
        return Err(EngineError::Invalid("positive body count required".into()));
    }
    let bodies = (0..count)
        .map(|i| {
            let i = i as i128;
            Body::new(
                i as u64,
                format!("mixed {i}"),
                Inertial::new(
                    0,
                    Vec2::new(i * 11, (i % 9) * 7),
                    Vec2 {
                        x: r((i % 7) - 3) / r(8),
                        y: r((i % 5) - 2) / r(8),
                    },
                )
                .unwrap(),
                r(1) / r(8),
                r(1),
            )
        })
        .collect();
    Engine::new(0xC0FF_EE11, bodies, vec![])
}

/// Frozen scripted IR: scheduled course, addressed SetCourse, contact-stop/notify.
pub fn scripted_interactions() -> Result<Engine, EngineError> {
    let emitter = body(1, "Scripted A", 0, 0, 0, 1, 1);
    let mut courier = body(2, "Scripted B", 12, 0, 0, 1, 1);
    courier.stop_on_contact = true;
    courier.notify_on_contact = Some(1);
    let receiver = body(3, "Scripted C", 40, 0, 0, 1, 1);
    let family = Family::affine(
        "scripted-lane",
        100,
        8,
        0,
        Inertial::new(0, Vec2::new(0, 400), Vec2::zero())?,
        Vec2::new(16, 0),
        r(1),
        r(1),
    );
    let mut e = Engine::new(0x5C12_17ED, vec![emitter, courier, receiver], vec![family])?;
    e.intervene(
        1,
        Command::SetCourse {
            at: 5,
            velocity: Vec2 {
                x: r(1) / r(2),
                y: r(0),
            },
        },
    )?;
    e.intervene(
        1,
        Command::SendSignal {
            target: 2,
            payload: Payload::SetCourse {
                velocity: Vec2 {
                    x: r(1) / r(4),
                    y: r(0),
                },
            },
        },
    )?;
    Ok(e)
}

/// N ships on one pad polyline with staggered hold-then-cruise departures.
/// Members do not share velocity while some are still holding.
/// Interaction IR is scripted; this is not a gravity law.
pub fn phase_departure_lane(count: u64) -> Result<Engine, EngineError> {
    if count == 0 {
        return Err(EngineError::Invalid("positive family count required".into()));
    }
    let family = Family::affine(
        "phase-lane",
        100,
        count,
        0,
        Inertial::new(0, Vec2::zero(), Vec2::zero())?,
        Vec2::new(8, 0),
        r(1) / r(8),
        r(1),
    )
    .with_phase(PhaseGenerator::new(
        4,
        3,
        Vec2 {
            x: r(-1) / r(4),
            y: r(0),
        },
    )?);
    let probe = Body::new(
        1,
        "probe",
        Inertial::new(
            0,
            Vec2::new(-20, 0),
            Vec2 {
                x: r(1) / r(8),
                y: r(0),
            },
        )?,
        r(1) / r(8),
        r(1),
    );
    let mut e = Engine::new(0x9A5E_F41E, vec![probe], vec![family])?;
    e.intervene(
        1,
        Command::SendSignal {
            target: 100,
            payload: Payload::Ping,
        },
    )?;
    Ok(e)
}

/// Frozen packed-overlap / war-island fixture.
/// Many explicit bodies and distinct families share certified AABB overlaps on a
/// finite horizon so one large causal component appears. Independent far families
/// stay outside that island. Overlap is not an equivalence merge. Scripted IR
/// only (`SetCourseRange`, signal, contacts); not a gravity law or battle mode.
pub const PACKED_ISLAND_BODIES: u64 = 64;
pub const PACKED_ISLAND_LANES: u64 = 8;
pub const PACKED_ISLAND_LANE_SHIPS: u64 = 4;
pub const PACKED_ISLAND_LANE_FIRST: u64 = 100;
pub const PACKED_ISLAND_LANE_STRIDE: u64 = 10;
pub const PACKED_FAR_NORTH: u64 = 10_000;
pub const PACKED_FAR_SOUTH: u64 = 20_000;
pub const PACKED_ISLAND_BURN_AT: i128 = 10;
pub const PACKED_ISLAND_HORIZON: i128 = 80;

pub fn packed_overlap_island() -> Result<Engine, EngineError> {
    let side = 8i128;
    let spacing = 2i128;
    let mut bodies = Vec::with_capacity(PACKED_ISLAND_BODIES as usize);
    for i in 0..PACKED_ISLAND_BODIES {
        let col = (i as i128) % side;
        let row = (i as i128) / side;
        bodies.push(Body::new(
            i,
            format!("war {i}"),
            Inertial::new(
                0,
                Vec2::new(col * spacing, row * spacing),
                Vec2 {
                    x: r((i as i128 % 3) - 1) / r(8),
                    y: r((i as i128 % 5) - 2) / r(8),
                },
            )?,
            r(1),
            r(1),
        ));
    }
    let mut families = Vec::new();
    for lane in 0..PACKED_ISLAND_LANES {
        families.push(Family::affine(
            format!("war-lane-{lane:02}"),
            PACKED_ISLAND_LANE_FIRST + lane * PACKED_ISLAND_LANE_STRIDE,
            PACKED_ISLAND_LANE_SHIPS,
            0,
            Inertial::new(0, Vec2::new(1, lane as i128 * spacing), Vec2::zero())?,
            Vec2::new(8, 0),
            r(1),
            r(1),
        ));
    }
    families.push(Family::affine(
        "far-north",
        PACKED_FAR_NORTH,
        8,
        0,
        Inertial::new(
            0,
            Vec2::new(0, 100_000),
            Vec2 {
                x: r(1) / r(4),
                y: r(0),
            },
        )?,
        Vec2::new(64, 0),
        r(1),
        r(1),
    ));
    families.push(Family::affine(
        "far-south",
        PACKED_FAR_SOUTH,
        8,
        0,
        Inertial::new(
            0,
            Vec2::new(0, 200_000),
            Vec2 {
                x: r(1) / r(4),
                y: r(0),
            },
        )?,
        Vec2::new(64, 0),
        r(1),
        r(1),
    ));
    let mut e = Engine::new(0x15E1_A15D, bodies, families)?;
    e.intervene(
        PACKED_ISLAND_LANE_FIRST,
        Command::SetCourseRange {
            lo: PACKED_ISLAND_LANE_FIRST,
            hi: PACKED_ISLAND_LANE_FIRST + PACKED_ISLAND_LANE_SHIPS - 1,
            at: PACKED_ISLAND_BURN_AT,
            velocity: Vec2 {
                x: r(1) / r(8),
                y: r(0),
            },
        },
    )?;
    e.intervene(
        0,
        Command::SendSignal {
            target: 7,
            payload: Payload::Ping,
        },
    )?;
    Ok(e)
}

pub fn materialize_family(family: &Family) -> Vec<Body> {
    (family.first_id..family.first_id + family.count)
        .map(|id| {
            Body::from_segments(
                id,
                family.name.clone(),
                family.member_segments(id).unwrap(),
                family.radius.clone(),
                family.mass.clone(),
                family.revision,
            )
            .unwrap()
        })
        .collect()
}
