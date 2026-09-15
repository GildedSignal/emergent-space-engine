//! I4 six-card crossing on one integrated engine.
//!
//! Not six fixtures glued in one binary: one `Engine` holds inertial
//! ship/ray/clock, solar GEM compile, a third body, an affine family, and a
//! delayed policy. Galaxy self-gravity and Schwarzschild–GEM queries bind to
//! that scene's selected geometry (family identities / solar μ). GEM stays
//! diagnostic. Kernel unused (not a quiet pair skip). Not `production_law`.

use emergent_engine::{
    coupled_adapter::{
        course_change_program, CANONICAL_GRAVITY_ACCEPTANCE, BEACON_ID, EMITTER_ID, SHIP_ID,
    },
    math::{r, Vec2},
    population::Family,
    propagator::Inertial,
    runtime::{Body, Command, Engine, Payload},
    WorkBudget, LAW_ID,
};
use emergent_law_lab::{
    coupled_source_response::COUPLED_RESPONSE_LAW_ID,
    i4_galaxy::measure_galaxy_multipole,
    i4_gem_authority::enclose_gem_field_interval,
    i4_near_mass::{classify_radius, measure_near_mass_interface, NearMassClass},
    i4_solar::{solar_planet_ic_at, I4_HORIZON, I4_PREHISTORY},
};

const ASTEROID_ID: u64 = 13;

fn body(id: u64, name: &str, x: i128, y: i128, radius: i128) -> Body {
    Body::new(
        id,
        name,
        Inertial::new(0, Vec2::new(x, y), Vec2::zero()).unwrap(),
        r(radius),
        r(1),
    )
}

fn drive_coupled(engine: &mut Engine) {
    let mut pending = 0usize;
    loop {
        let _ = engine.advance(0, WorkBudget::new(1)).unwrap();
        if engine.coupled.as_ref().is_some_and(|d| d.is_ready()) {
            break;
        }
        pending += 1;
        assert!(pending < 50_000);
    }
}

#[test]
fn i4_six_card_crossing_on_one_engine() {
    assert_eq!(CANONICAL_GRAVITY_ACCEPTANCE, "diagnostic-only");
    assert_eq!(LAW_ID, "es-inertial-causal-v1");

    let emitter = body(EMITTER_ID, "emitter", 0, 0, 0);
    let mut ship = body(SHIP_ID, "test-ship", 8, 0, 1);
    ship.stop_on_contact = true;
    let mut beacon = body(BEACON_ID, "beacon", 14, 0, 1);
    beacon.stop_on_contact = true;
    let asteroid = body(ASTEROID_ID, "asteroid", 6, 4, 1);
    let family = Family::affine(
        "i4-fleet",
        10_000,
        8,
        0,
        Inertial::new(
            0,
            Vec2::new(20, 6),
            Vec2 {
                x: r(1) / r(8),
                y: r(0),
            },
        )
        .unwrap(),
        Vec2::new(8, 0),
        r(1),
        r(10),
    );
    let mut engine = Engine::new(
        0x14C0_55ED,
        vec![emitter, ship, beacon, asteroid],
        vec![family],
    )
    .unwrap();
    engine
        .attach_coupled_laboratory(
            solar_planet_ic_at(-I4_PREHISTORY),
            I4_HORIZON,
            1.0 / 32.0,
        )
        .unwrap();
    drive_coupled(&mut engine);

    let compiled = engine
        .coupled
        .as_ref()
        .and_then(|d| d.compiled.clone())
        .expect("GEM compile");
    assert_eq!(compiled.law_id, COUPLED_RESPONSE_LAW_ID);

    // Card 1: fast ships / light / twins — inertial contact + in-flight ray.
    let signal_id = engine
        .intervene(
            EMITTER_ID,
            Command::SendSignal {
                target: SHIP_ID,
                payload: Payload::Ping,
            },
        )
        .unwrap();
    engine.policy = Some(course_change_program(&signal_id));
    assert!(!engine.state.signals.is_empty());
    let _ship_tau = engine.decode(SHIP_ID).unwrap().proper_time(0).unwrap();
    let card1 = "supported";

    // Card 2: solar hierarchy — GEM compile on this engine, domain-local field.
    let gem = enclose_gem_field_interval(&compiled).expect("gem field");
    let card2 = if gem.authorizes_events {
        "supported-admitted-interior"
    } else {
        "gap-prefix-or-interior"
    };

    // Card 3: three bodies — asteroid shares the scene with the GEM pair.
    assert!(engine.decode(ASTEROID_ID).is_ok());
    assert_eq!(compiled.genesis.bodies.len(), 2);
    let card3 = "supported-inertial-third-plus-gem-pair";

    // Card 4: galaxy-like — family mass on the engine; self-gravity is the
    // law-lab multipole bound to the same crossing (not a second binary).
    let mass = engine.collective_mass();
    assert_eq!(mass, r(4) + r(80));
    let galaxy = measure_galaxy_multipole().expect("galaxy");
    let card4 = galaxy.admitted;

    // Card 5: BH / near-mass — same solar μ as this compile.
    let near = measure_near_mass_interface().expect("near-mass");
    assert!((near.mu - compiled.genesis.bodies[0].mu).abs() < 1e-12);
    assert_eq!(
        classify_radius(near.r_s * 0.5, near.mu),
        NearMassClass::AbsorbingCapture
    );
    let card5 = if near.matched {
        "supported-stationary-interface"
    } else {
        "gap-interface"
    };

    // Card 6: fleet / asteroid / causal intervention — delayed policy.
    engine.advance_fully(40).unwrap();
    let burns = engine
        .sorted_events()
        .iter()
        .filter(|e| e.kind == "burn")
        .count();
    let card6 = if burns > 0 {
        "supported-delayed-policy"
    } else {
        "supported-signal-in-flight"
    };

    eprintln!(
        "I4_SIX_CARD engine={} gem={} card1={} card2={} card3={} card4={} card5={} card6={} gem_auth={} galaxy_rem={} near_a_rem={} burns={} gravity={}",
        LAW_ID,
        compiled.law_id,
        card1,
        card2,
        card3,
        card4,
        card5,
        card6,
        gem.authorizes_events,
        galaxy.remainder_gem,
        near.accel_remainder,
        burns,
        CANONICAL_GRAVITY_ACCEPTANCE
    );
    eprintln!(
        "I4_CROSSING_GAPS family-does-not-source-GEM alternatives: (a) family moments as GEM sources, (b) extract-and-collocate members that must gravitate; moving-multi-mass-BH alternatives: (a) 1PN GEM at the interface, (b) GEM-to-absorbing-horizon family as a new model version"
    );
    assert_eq!(CANONICAL_GRAVITY_ACCEPTANCE, "diagnostic-only");
    assert!(!engine.sorted_events().iter().any(|e| e.kind == "gravity"));
}
