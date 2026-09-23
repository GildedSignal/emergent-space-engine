//! I6 same-model qualification matrix.
//!
//! One identified model (`es-inertial-causal-v1` plus diagnostic
//! `es-linearized-retarded-gem-response-v0`), one implementation, one
//! connected workload. Native observatory hosts this Engine — not the
//! GEM-response gallery and not a second laboratory world labelled as
//! qualification. Plan I6 exit is this matrix existing and run, not a
//! green promotion. `production_law` stays null. Canonical gravity stays
//! diagnostic-only. Frozen `1dac658` / H0052 / H0054 / H0124 unchanged.

use crate::{
    coupled_adapter::{
        course_change_program, CANONICAL_GRAVITY_ACCEPTANCE, BEACON_ID, EMITTER_ID,
        SHIP_ID, MovingCompactDiagnostic,
    },
    math::{r, Vec2},
    population::Family,
    propagator::Inertial,
    runtime::{Body, Command, Engine, EngineError, Payload},
    scenario::{
        self, packed_overlap_island, PACKED_FAR_NORTH, PACKED_ISLAND_BODIES,
        PACKED_ISLAND_HORIZON, PACKED_ISLAND_LANES, PACKED_ISLAND_LANE_SHIPS,
    },
    WorkBudget, LAW_ID,
};
use emergent_law_lab::{
    coupled_source_response::COUPLED_RESPONSE_LAW_ID,
    i4_family_gem::measure_family_sourced_gem,
    i4_galaxy::measure_galaxy_multipole,
    i4_gem_authority::enclose_gem_field_interval,
    i4_moving_compact::{measure_moving_compact, MOVING_SCHWARZSCHILD_1PN_LAW_ID},
    i4_moving_horizon::measure_moving_horizon,
    i4_near_mass::{measure_near_mass_1pn, measure_near_mass_interface, I4_IF_MATCH_BAND},
    i4_solar::{measure_solar_hierarchy, SolarHierarchy, solar_planet_ic_at, I4_COLLECTIVE_A_BAND, I4_HORIZON, I4_PREHISTORY},
};
use emergent_law_lab::two_body_bank::{measure_bank, measure_initialized_bank, measure_newton_bank, BankReport};
use serde::{Deserialize, Serialize};
use std::time::Instant;

const ASTEROID_ID: u64 = 13;
const BAND: f64 = 0.05;
const HELD_OUT_THREE_BODY: u64 = 0x16B0_1D01;
const HELD_OUT_FLEET: u64 = 0x16B0_1D02;
const HELD_OUT_COMPILER: u64 = 0x16B0_1D03;
const HELD_OUT_REFINEMENT: u64 = 0x16B0_1D04;
const DAILY_SEED: u64 = 0x14C0_55ED;
const PRESSURE_SEED: u64 = 0x15E1_A15D;
const PRESSURE_YIELD_BUDGET: usize = 128;

/// Frozen I6 envelope rungs. Declared before any Instant/RSS/digest.
/// Not the integrated target. Fixed ICs are many-seed capable, not the universe.
struct FrozenRung {
    id: &'static str,
    claim: &'static str,
    identities: u64,
    families: u64,
    family_members: u64,
    horizon_ticks: i128,
    independent_activity: &'static str,
    queries: &'static str,
    reconstruction: &'static str,
    seed: u64,
}

const TINY_RUNG: FrozenRung = FrozenRung {
    id: "tiny-complete-loop",
    claim: "Correctness and repair/authority semantics",
    identities: 4,
    families: 0,
    family_members: 0,
    horizon_ticks: 80,
    independent_activity: "one SendSignal Emitter->Courier; Independent witness far off-axis",
    queries: "history_digest(through) + signal_arrived presence",
    reconstruction: "replay digest equality",
    seed: 0x0E5C_A051,
};

const CONNECTED_RUNG: FrozenRung = FrozenRung {
    id: "connected-family-hierarchy",
    claim: "Composition and meaningful end-to-end optimization",
    identities: 4,
    families: 1,
    family_members: 8,
    horizon_ticks: 40,
    independent_activity: "SendSignal emitter->ship; in-flight beacon; policy Burn remaining>0; diagnostic compact sidecar",
    queries: "history_digest(through) + history_digest(cold) + decode(ship)",
    reconstruction: "checkpoint restore digest + replay digest",
    seed: DAILY_SEED,
};

const PRESSURE_RUNG: FrozenRung = FrozenRung {
    id: "pressure-sweeps",
    claim: "Break-even domains, fragmentation/rank/history/latency limits",
    identities: 64,
    families: 10,
    family_members: 48,
    horizon_ticks: 80,
    independent_activity: "SetCourseRange lane burn at t=10; SendSignal 0->7; hot packed island plus quiet far-north/south families; diagnostic GEM collocation H=2",
    queries: "history_digest(through) + decode(far-north) + observe_with_budget yield",
    reconstruction: "replay digest equality; residual bytes = owned CanonicalState JSON",
    seed: PRESSURE_SEED,
};

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "UPPERCASE")]
pub enum GateStatus {
    Pass,
    Fail,
    Unsupported,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Gate {
    pub id: String,
    pub status: GateStatus,
    pub evidence: String,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Card {
    pub id: String,
    pub look_for: String,
    pub allowed_outcome_class: String,
    pub model_regime: String,
    pub comparison: String,
    pub status: GateStatus,
    pub failing_input_visible: bool,
    pub unconfirmed_magnitudes_visible: bool,
    pub evidence: String,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SeedCase {
    pub role: String,
    pub seed: u64,
    pub intended_outcome_class: String,
    pub observed_class: String,
    pub status: GateStatus,
    pub evidence: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub comparison: Option<String>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct EnvelopeRung {
    pub id: String,
    pub claim: String,
    pub status: GateStatus,
    pub evidence: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub identities: Option<u64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub families: Option<u64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub family_members: Option<u64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub horizon_ticks: Option<i64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub independent_activity: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub queries: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub reconstruction: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub seed: Option<u64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub rss_kb: Option<u64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub wall_ns: Option<u64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub digest: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub ledger_total: Option<u64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub owned_bytes: Option<usize>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub residual_bytes: Option<usize>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub limiting_resource: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub yield_pauses: Option<u64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub collocation_ns: Option<u64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub reconstruction_ns: Option<u64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub advance_ns: Option<u64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub oracle_ns: Option<u64>,
}

impl EnvelopeRung {
    fn unsupported(id: &str, claim: &str, evidence: &str) -> Self {
        Self {
            id: id.into(),
            claim: claim.into(),
            status: GateStatus::Unsupported,
            evidence: evidence.into(),
            identities: None,
            families: None,
            family_members: None,
            horizon_ticks: None,
            independent_activity: None,
            queries: None,
            reconstruction: None,
            seed: None,
            rss_kb: None,
            wall_ns: None,
            digest: None,
            ledger_total: None,
            owned_bytes: None,
            residual_bytes: None,
            limiting_resource: None,
            yield_pauses: None,
            collocation_ns: None,
            reconstruction_ns: None,
            advance_ns: None,
            oracle_ns: None,
        }
    }

    fn measured(
        spec: &FrozenRung,
        status: GateStatus,
        evidence: String,
        rss_kb: Option<u64>,
        wall_ns: u64,
        digest: String,
        ledger_total: u64,
        owned_bytes: Option<usize>,
    ) -> Self {
        Self {
            id: spec.id.into(),
            claim: spec.claim.into(),
            status,
            evidence,
            identities: Some(spec.identities),
            families: Some(spec.families),
            family_members: Some(spec.family_members),
            horizon_ticks: Some(spec.horizon_ticks as i64),
            independent_activity: Some(spec.independent_activity.into()),
            queries: Some(spec.queries.into()),
            reconstruction: Some(spec.reconstruction.into()),
            seed: Some(spec.seed),
            rss_kb,
            wall_ns: Some(wall_ns),
            digest: Some(digest),
            ledger_total: Some(ledger_total),
            owned_bytes,
            residual_bytes: owned_bytes,
            limiting_resource: None,
            yield_pauses: None,
            collocation_ns: None,
            reconstruction_ns: None,
            advance_ns: None,
            oracle_ns: None,
        }
    }

    fn with_pressure(
        mut self,
        limiter: &str,
        yield_pauses: u64,
        collocation_ns: u64,
        reconstruction_ns: u64,
        advance_ns: u64,
        oracle_ns: u64,
    ) -> Self {
        self.limiting_resource = Some(limiter.into());
        self.yield_pauses = Some(yield_pauses);
        self.collocation_ns = Some(collocation_ns);
        self.reconstruction_ns = Some(reconstruction_ns);
        self.advance_ns = Some(advance_ns);
        self.oracle_ns = Some(oracle_ns);
        self
    }
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ObservatoryBind {
    pub host: String,
    pub engine: String,
    pub law: String,
    pub native_world: String,
    pub connected_world: String,
    pub not_qualification_world: String,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct I6Report {
    pub schema: u32,
    pub id: String,
    pub canonical_law: String,
    pub diagnostic_response: String,
    pub implementation: String,
    pub workload: String,
    pub production_law: Option<String>,
    pub canonical_gravity_acceptance: String,
    pub promotion: bool,
    pub plan_i6_exit: String,
    pub full_engine: bool,
    pub observatory: ObservatoryBind,
    pub gates: Vec<Gate>,
    pub cards: Vec<Card>,
    pub daily_gallery: Vec<SeedCase>,
    pub held_out: Vec<SeedCase>,
    pub two_body_behavior: BankReport,
    pub initialized_two_body_behavior: BankReport,
    pub newton_two_body_behavior: BankReport,
    pub solar_window: SolarHierarchy,
    pub envelope: Vec<EnvelopeRung>,
}

fn body(id: u64, name: &str, x: i128, y: i128, radius: i128) -> Body {
    Body::new(
        id,
        name,
        Inertial::new(0, Vec2::new(x, y), Vec2::zero()).unwrap(),
        r(radius),
        r(1),
    )
}

fn drive_coupled(engine: &mut Engine) -> Result<(), EngineError> {
    let mut pending = 0usize;
    loop {
        let _ = engine.advance(0, WorkBudget::new(1))?;
        if engine.coupled.as_ref().is_some_and(|d| d.is_ready()) {
            return Ok(());
        }
        pending += 1;
        if pending >= 50_000 {
            return Err(EngineError::Unsupported(
                "coupled compile did not become ready".into(),
            ));
        }
    }
}

fn gate(id: &str, status: GateStatus, evidence: impl Into<String>) -> Gate {
    Gate {
        id: id.into(),
        status,
        evidence: evidence.into(),
    }
}

fn unsupported(e: impl std::fmt::Display) -> EngineError {
    EngineError::Unsupported(e.to_string())
}

fn process_rss_kb() -> Option<u64> {
    let pid = std::process::id().to_string();
    let out = std::process::Command::new("ps")
        .args(["-o", "rss=", "-p", &pid])
        .output()
        .ok()?;
    String::from_utf8(out.stdout).ok()?.trim().parse().ok()
}

fn owned_state_bytes(engine: &Engine) -> Option<usize> {
    serde_json::to_vec(&engine.state)
        .ok()
        .map(|bytes| bytes.len())
}

fn nested_ledger_total(engine: &Engine) -> u64 {
    engine
        .coupled
        .as_ref()
        .and_then(|d| d.compiled.as_ref())
        .map(|compiled| compiled.charge.ledger_total())
        .unwrap_or(0)
}

fn wall_ns(start: Instant) -> u64 {
    start.elapsed().as_nanos().min(u128::from(u64::MAX)) as u64
}

struct TinyRungMeasure {
    received: bool,
    replay_ok: bool,
    rss_kb: Option<u64>,
    wall_ns: u64,
    digest: String,
    ledger_total: u64,
    owned_bytes: Option<usize>,
}

/// Freeze TINY_RUNG is already a const. Measurement starts after that declaration.
fn measure_tiny_rung() -> Result<TinyRungMeasure, EngineError> {
    let spec = &TINY_RUNG;
    let start = Instant::now();
    let mut engine = scenario::causal_relay()?;
    if engine.state.seed != spec.seed {
        return Err(EngineError::Invalid("tiny seed drifted from freeze".into()));
    }
    if engine.state.bodies.len() as u64 != spec.identities {
        return Err(EngineError::Invalid(
            "tiny identity count drifted from freeze".into(),
        ));
    }
    if !engine.state.families.is_empty() {
        return Err(EngineError::Invalid(
            "tiny family count drifted from freeze".into(),
        ));
    }
    engine.advance_fully(spec.horizon_ticks)?;
    let through = engine.state.clock;
    let digest = engine.history_digest(through)?;
    let received = engine
        .sorted_events()
        .iter()
        .any(|event| event.kind == "signal_arrived");
    let replayed = engine.replay()?;
    let replay_ok = replayed.history_digest(replayed.state.clock)? == digest;
    Ok(TinyRungMeasure {
        received,
        replay_ok,
        rss_kb: process_rss_kb(),
        wall_ns: wall_ns(start),
        digest,
        ledger_total: nested_ledger_total(&engine),
        owned_bytes: owned_state_bytes(&engine),
    })
}

struct PressureRungMeasure {
    ok: bool,
    rss_kb: Option<u64>,
    wall_ns: u64,
    digest: String,
    ledger_total: u64,
    owned_bytes: Option<usize>,
    limiter: &'static str,
    yield_pauses: u64,
    collocation_ns: u64,
    reconstruction_ns: u64,
    advance_ns: u64,
    oracle_ns: u64,
    far_ok: bool,
    replay_ok: bool,
    oracle_ok: bool,
}

fn name_limiter(
    collocation_ns: u64,
    advance_ns: u64,
    reconstruction_ns: u64,
    oracle_ns: u64,
    yield_pauses: u64,
) -> &'static str {
    let max_t = collocation_ns
        .max(advance_ns)
        .max(reconstruction_ns)
        .max(oracle_ns);
    if max_t == 0 {
        return "unmeasured";
    }
    if oracle_ns == max_t {
        "sequential-query"
    } else if collocation_ns == max_t {
        "sequential-collocation"
    } else if reconstruction_ns == max_t {
        "reconstruction"
    } else if yield_pauses > 0 {
        "yield"
    } else {
        "sequential-advance"
    }
}

/// Freeze PRESSURE_RUNG is already a const. Mixed quiet/hot, not the billion-identity target.
fn measure_pressure_rung() -> Result<PressureRungMeasure, EngineError> {
    let spec = &PRESSURE_RUNG;
    assert_eq!(spec.identities, PACKED_ISLAND_BODIES);
    assert_eq!(spec.families, PACKED_ISLAND_LANES + 2);
    assert_eq!(
        spec.family_members,
        PACKED_ISLAND_LANES * PACKED_ISLAND_LANE_SHIPS + 16
    );
    assert_eq!(spec.horizon_ticks, PACKED_ISLAND_HORIZON);
    assert_eq!(spec.seed, PRESSURE_SEED);

    let total = Instant::now();
    let colloc_started = Instant::now();
    let mut engine = packed_overlap_island()?;
    if engine.state.seed != spec.seed {
        return Err(EngineError::Invalid(
            "pressure seed drifted from freeze".into(),
        ));
    }
    if engine.state.bodies.len() as u64 != spec.identities {
        return Err(EngineError::Invalid(
            "pressure identity count drifted from freeze".into(),
        ));
    }
    if engine.state.families.len() as u64 != spec.families
        || engine
            .state
            .families
            .iter()
            .map(|family| family.count)
            .sum::<u64>()
            != spec.family_members
    {
        return Err(EngineError::Invalid(
            "pressure family freeze drifted".into(),
        ));
    }
    engine.attach_coupled_laboratory(
        solar_planet_ic_at(-I4_PREHISTORY),
        I4_HORIZON.min(2.0),
        1.0 / 32.0,
    )?;
    drive_coupled(&mut engine)?;
    let collocation_ns = wall_ns(colloc_started);

    let adv_started = Instant::now();
    let mut yield_pauses = 0u64;
    loop {
        let result = engine.advance(spec.horizon_ticks, WorkBudget::new(PRESSURE_YIELD_BUDGET))?;
        if result.complete {
            break;
        }
        yield_pauses += 1;
        if yield_pauses > 100_000 {
            return Err(EngineError::ResourceLimit(
                "pressure yield loop did not complete".into(),
            ));
        }
    }
    let through = engine.state.clock;
    let digest = engine.history_digest(through)?;
    let far_ok = engine.decode(PACKED_FAR_NORTH).is_ok();
    let _ = engine.observe_with_budget(
        0,
        through,
        &[7, PACKED_FAR_NORTH],
        WorkBudget::new(16),
    );
    let advance_ns = wall_ns(adv_started);

    let recon_started = Instant::now();
    let replayed = engine.replay()?;
    let replay_ok = replayed.history_digest(replayed.state.clock)? == digest;
    let reconstruction_ns = wall_ns(recon_started);
    let oracle_started = Instant::now();
    let oracle_ok = engine.canonical_facts_agree(through)?;
    let oracle_ns = wall_ns(oracle_started);

    let limiter = name_limiter(
        collocation_ns,
        advance_ns,
        reconstruction_ns,
        oracle_ns,
        yield_pauses,
    );
    Ok(PressureRungMeasure {
        ok: replay_ok && far_ok && oracle_ok,
        rss_kb: process_rss_kb(),
        wall_ns: wall_ns(total),
        digest,
        ledger_total: nested_ledger_total(&engine),
        owned_bytes: owned_state_bytes(&engine),
        limiter,
        yield_pauses,
        collocation_ns,
        reconstruction_ns,
        advance_ns,
        oracle_ns,
        far_ok,
        replay_ok,
        oracle_ok,
    })
}

/// Same `Engine` type and law as the native observatory host.
pub fn connected_qualification_engine() -> Result<Engine, EngineError> {
    let emitter = body(EMITTER_ID, "emitter", 0, 0, 0);
    let mut ship = body(SHIP_ID, "test-ship", 8, 0, 1);
    ship.stop_on_contact = true;
    let mut beacon = body(BEACON_ID, "beacon", 14, 0, 1);
    beacon.stop_on_contact = true;
    let asteroid = body(ASTEROID_ID, "asteroid", 6, 4, 1);
    let family = Family::affine(
        "i6-fleet",
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
        )?,
        Vec2::new(8, 0),
        r(1),
        r(10),
    );
    let mut engine = Engine::new(
        DAILY_SEED,
        vec![emitter, ship, beacon, asteroid],
        vec![family],
    )?;
    engine.attach_coupled_laboratory(
        solar_planet_ic_at(-I4_PREHISTORY),
        I4_HORIZON,
        1.0 / 32.0,
    )?;
    engine.attach_moving_compact(DAILY_SEED)?;
    Ok(engine)
}

/// Run the I6 matrix. Never selects `production_law`.
pub fn run_matrix() -> Result<I6Report, EngineError> {
    assert_eq!(I4_COLLECTIVE_A_BAND, BAND);
    assert_eq!(I4_IF_MATCH_BAND, BAND);
    assert_eq!(TINY_RUNG.horizon_ticks, 80);
    assert_eq!(CONNECTED_RUNG.horizon_ticks, 40);
    assert_eq!(CONNECTED_RUNG.seed, DAILY_SEED);
    assert_eq!(PRESSURE_RUNG.horizon_ticks, PACKED_ISLAND_HORIZON);
    assert_eq!(PRESSURE_RUNG.seed, PRESSURE_SEED);

    let tiny_m = measure_tiny_rung()?;
    let pressure_m = measure_pressure_rung()?;

    let native = scenario::observatory()?;
    let connected_started = Instant::now();
    let mut connected = connected_qualification_engine()?;
    if connected.state.seed != CONNECTED_RUNG.seed {
        return Err(EngineError::Invalid(
            "connected seed drifted from freeze".into(),
        ));
    }
    if connected.state.bodies.len() as u64 != CONNECTED_RUNG.identities {
        return Err(EngineError::Invalid(
            "connected identity count drifted from freeze".into(),
        ));
    }
    if connected.state.families.len() as u64 != CONNECTED_RUNG.families
        || connected
            .state
            .families
            .first()
            .map(|family| family.count)
            != Some(CONNECTED_RUNG.family_members)
    {
        return Err(EngineError::Invalid(
            "connected family freeze drifted".into(),
        ));
    }
    drive_coupled(&mut connected)?;

    let observatory = ObservatoryBind {
        host: "EngineBridge".into(),
        engine: "emergent_engine::Engine".into(),
        law: LAW_ID.into(),
        native_world: "scenario::observatory".into(),
        connected_world: "i6::connected_qualification_engine".into(),
        not_qualification_world: "observatory::gallery GEM-response-slice".into(),
    };
    let same_engine = native.state.law == LAW_ID && connected.state.law == LAW_ID;

    let signal_id = connected.intervene(
        EMITTER_ID,
        Command::SendSignal {
            target: SHIP_ID,
            payload: Payload::Ping,
        },
    )?;
    connected.policy = Some(course_change_program(&signal_id));
    let in_flight = !connected.state.signals.is_empty();
    connected.advance_fully(CONNECTED_RUNG.horizon_ticks)?;

    let through = connected.state.clock;
    let cold_cut = (through / 2).max(0);
    let digest_full = connected.history_digest(through)?;
    let digest_cold = connected.history_digest(cold_cut)?;
    let cold_ok = connected.state.clock == through && digest_cold != digest_full;

    let tmp = std::env::temp_dir().join(format!("es-i6-{}.checkpoint", std::process::id()));
    connected.checkpoint(&tmp)?;
    let restored = Engine::restore(&tmp)?;
    let replayed = connected.replay()?;
    let persist_ok = restored.history_digest(restored.state.clock)? == digest_full
        && replayed.history_digest(replayed.state.clock)? == digest_full;
    let _ = std::fs::remove_file(&tmp);
    let ship_query_ok = connected.decode(SHIP_ID)?.proper_time(0).is_ok();
    let connected_wall_ns = wall_ns(connected_started);
    let connected_rss_kb = process_rss_kb();
    let connected_owned_bytes = owned_state_bytes(&connected);
    let connected_ledger_total = nested_ledger_total(&connected);
    let connected_digest = digest_full.clone();
    let inertial_match = connected.canonical_facts_agree(through)?;

    let compiled = connected
        .coupled
        .as_ref()
        .and_then(|d| d.compiled.clone())
        .ok_or_else(|| unsupported("GEM compile missing on connected engine"))?;
    let gem = enclose_gem_field_interval(&compiled).map_err(unsupported)?;
    let galaxy = measure_galaxy_multipole().map_err(unsupported)?;
    let near_v0 = measure_near_mass_interface().map_err(unsupported)?;
    let near = measure_near_mass_1pn().map_err(unsupported)?;
    let horizon = measure_moving_horizon().map_err(unsupported)?;
    let compact = measure_moving_compact();
    let family = measure_family_sourced_gem().map_err(unsupported)?;
    let two_body_behavior = measure_bank();
    let initialized_two_body_behavior=measure_initialized_bank();
    let newton_two_body_behavior=measure_newton_bank();
    let solar_window = measure_solar_hierarchy().map_err(unsupported)?;
    let domain_auth = connected.authorizes_gem_events_on_admitted_field();

    let burns = connected
        .sorted_events()
        .iter()
        .filter(|e| e.kind == "burn")
        .count();
    let ship_tau_ok = ship_query_ok;
    let asteroid_ok = connected.decode(ASTEROID_ID).is_ok();

    let quadrupole_fail = galaxy.remainder_gem > BAND;
    let family_keep = family.remainder <= BAND && family.admitted == "family-moment-gem-source";
    let hosted = connected.hosts_moving_compact_law();
    let engine_captured = connected
        .moving_compact
        .as_ref()
        .is_some_and(|m| m.captured());
    let engine_rem = connected
        .moving_compact
        .as_ref()
        .map(|m| m.remainder_vs_slow())
        .unwrap_or(1.0);
    let engine_moved = connected
        .moving_compact
        .as_ref()
        .is_some_and(|m| m.map.host_displaced());
    let remnant_mu = connected
        .moving_compact
        .as_ref()
        .map(|m| m.map.remnant_mu())
        .unwrap_or(0.0);
    let crossing_ok = hosted
        && engine_captured
        && engine_rem <= BAND
        && engine_moved
        && in_flight
        && ship_tau_ok
        && burns > 0
        && persist_ok
        && inertial_match
        && asteroid_ok
        && family_keep;

    let tiny_ok = tiny_m.received && tiny_m.replay_ok;
    let connected_rung_ok = persist_ok && in_flight && ship_query_ok && asteroid_ok;

    let gates = vec![
        gate("newton-initialized-two-body-finite-arcs",
            if newton_two_body_behavior.all_pass {GateStatus::Pass}
            else if newton_two_body_behavior.cases.iter().any(|c|c.status=="FAIL"){GateStatus::Fail}else{GateStatus::Unsupported},
            "separate observation-start Newton initializer; all derivative/line-search solves charged; retained original bank; not full-orbit or production qualification"),
        gate("two-body-finite-arc-behavior",
            if two_body_behavior.all_pass { GateStatus::Pass }
            else if two_body_behavior.cases.iter().any(|c|c.status=="FAIL") { GateStatus::Fail }
            else { GateStatus::Unsupported },
            &format!("{}; {} / {} pass; numerical agreement cannot replace independent physical anchors; frozen failures retained",two_body_behavior.scope,two_body_behavior.cases.iter().filter(|c|c.status=="PASS").count(),two_body_behavior.cases.len())),
        gate(
            "observatory-same-engine",
            if same_engine {
                GateStatus::Pass
            } else {
                GateStatus::Fail
            },
            format!(
                "native law={} connected law={}; host EngineBridge; gallery GEM slice is not this matrix",
                native.state.law, connected.state.law
            ),
        ),
        gate(
            "compiler-inertial-facts",
            if inertial_match {
                GateStatus::Pass
            } else {
                GateStatus::Fail
            },
            "independent contact/arrival oracle vs engine events; comparison_type=compiler_only",
        ),
        gate(
            "persist-replay",
            if persist_ok {
                GateStatus::Pass
            } else {
                GateStatus::Fail
            },
            "checkpoint restore and replay match history_digest at the committed cut",
        ),
        gate(
            "cold-history-query",
            if cold_ok {
                GateStatus::Pass
            } else {
                GateStatus::Fail
            },
            format!("history_digest({cold_cut}) without moving clock {through}"),
        ),
        gate(
            "galaxy-quadrupole-skip",
            if quadrupole_fail {
                GateStatus::Fail
            } else {
                GateStatus::Pass
            },
            format!(
                "remainder_gem={:.6} vs band {BAND}; admitted={}; not hidden",
                galaxy.remainder_gem, galaxy.admitted
            ),
        ),
        gate(
            "moving-multi-mass-compact",
            if compact.covers_compact {
                GateStatus::Pass
            } else {
                GateStatus::Unsupported
            },
            compact.gate_evidence(),
        ),
        gate(
            "sch-gem-accel-continuity-v0",
            if near_v0.accel_remainder > BAND {
                GateStatus::Fail
            } else {
                GateStatus::Pass
            },
            format!(
                "v0 Newton GEM remainder {:.6} vs band {BAND}; row kept; not deleted",
                near_v0.accel_remainder
            ),
        ),
        gate(
            "sch-gem-accel-continuity",
            if near.accel_remainder > BAND {
                GateStatus::Fail
            } else {
                GateStatus::Pass
            },
            format!(
                "1PN GEM {} remainder {:.6} vs Sch Γ^r_tt band {BAND}; clocks {:.6}",
                near.law_id, near.accel_remainder, near.clock_remainder
            ),
        ),
        gate(
            "engine-canonical-gravity",
            if domain_auth && CANONICAL_GRAVITY_ACCEPTANCE == "diagnostic-only" {
                GateStatus::Pass
            } else {
                GateStatus::Fail
            },
            format!(
                "admitted-interior authorizes_gem_events={domain_auth}; global {CANONICAL_GRAVITY_ACCEPTANCE} (not minted)"
            ),
        ),
        gate(
            "family-moment-as-galaxy-skip",
            GateStatus::Fail,
            format!(
                "family KEEP remainder {:.6} ≤ {BAND} on affine N={} rest fixture only; not an all-galaxy skip",
                family.remainder, family.n_members
            ),
        ),
        gate(
            "production-promotion",
            GateStatus::Fail,
            "required cards include FAIL/UNSUPPORTED; production_law stays null",
        ),
        gate(
            "envelope-pressure",
            GateStatus::Unsupported,
            "pressure-sweeps rung is measured on packed quiet/hot; this gate stays UNSUPPORTED because no frozen large break-even workload was declared; not ≤4 GiB / 30 FPS",
        ),
        gate(
            "envelope-frozen-target",
            GateStatus::Unsupported,
            "no frozen large workload; tiny/connected RSS/time/digest are not ≤4 GiB / 30 FPS / billion-identity hour",
        ),
    ];

    let cards = vec![
        Card {
            id: "fast-ships-light-twins".into(),
            look_for: "Pulses reach moving receivers in an order that matches emission events and finite c; accumulated proper time fits the worldline.".into(),
            allowed_outcome_class: "one_way_pulse".into(),
            model_regime: format!("{LAW_ID} exact inertial; GEM diagnostic"),
            comparison: "compiler_only independent inertial oracle".into(),
            status: if in_flight && ship_tau_ok && inertial_match {
                GateStatus::Pass
            } else {
                GateStatus::Fail
            },
            failing_input_visible: true,
            unconfirmed_magnitudes_visible: true,
            evidence: format!("in_flight={in_flight} proper_time_ok={ship_tau_ok} oracle_match={inertial_match}"),
        },
        Card {
            id: "solar-system-hierarchy".into(),
            look_for: "A supported hierarchy stays organized; a kick breathes, it does not snap to a circle.".into(),
            allowed_outcome_class: "supported_hierarchy".into(),
            model_regime: "solar two-body GEM with prehistory; admitted interior field bound".into(),
            comparison: "physical_law remainder band 0.05".into(),
            status: GateStatus::Unsupported,
            failing_input_visible: true,
            unconfirmed_magnitudes_visible: true,
            evidence: format!(
                "sustained_orbit={}; finite-window radius=[{:.6},{:.6}] angular_coverage={:.6} radians negative_sampled_energy={}; field authorization={} is not orbital behavior; global gravity diagnostic-only",
                solar_window.sustained_bound_status,solar_window.min_r,solar_window.max_r,
                solar_window.sampled_orbit.sampled_angular_coverage_radians,
                solar_window.sampled_orbit.all_sampled_newtonian_energies_negative,gem.authorizes_events
            ),
        },
        Card {
            id: "three-bodies".into(),
            look_for: "Nested seeds can stay bound; encounter seeds can swap, eject, or go messy.".into(),
            allowed_outcome_class: "hierarchical_bound".into(),
            model_regime: "inertial third body plus GEM pair; close-entrant collocation fallback".into(),
            comparison: "physical_law; chaos does not excuse compiler change of inertial facts".into(),
            status: GateStatus::Unsupported,
            failing_input_visible: true,
            unconfirmed_magnitudes_visible: true,
            evidence: "asteroid shares the connected engine; decode success does not validate a gravitational three-body encounter; actual outcome bank still unsupported".into(),
        },
        Card {
            id: "galaxy-like-population".into(),
            look_for: "The crowd shears together; mass, not sprites, moves it.".into(),
            allowed_outcome_class: "clumpy_collection".into(),
            model_regime: "direct small-world GEM sums; quadrupole rejected".into(),
            comparison: "physical_law remainder vs direct sums; band 0.05".into(),
            status: GateStatus::Unsupported,
            failing_input_visible: true,
            unconfirmed_magnitudes_visible: true,
            evidence: format!(
                "admitted={}; quadrupole remainder {:.6} FAIL as skip (visible, not hidden); direct field sums do not establish evolved clumpy collection behavior",
                galaxy.admitted, galaxy.remainder_gem
            ),
        },
        Card {
            id: "black-hole-near-mass".into(),
            look_for: "Closer pass: more bend, more delay; too close, no return; clocks agree with that story.".into(),
            allowed_outcome_class: "near_mass_clock".into(),
            model_regime: format!(
                "{} moving 1PN until r_if then Sch geodesic; GEM-to-horizon wrappers stopped",
                compact.law_id
            ),
            comparison: "physical_law remainder band 0.05; RK2 vs RK4 dt/4".into(),
            status: if compact.covers_compact {
                GateStatus::Pass
            } else {
                GateStatus::Unsupported
            },
            failing_input_visible: true,
            unconfirmed_magnitudes_visible: true,
            evidence: format!(
                "1PN clocks remainder {:.6}; moving compact covers={}; captured={}; clock {:.3e} null {:.3e}; GEM-to-horizon covers={}",
                near.clock_remainder,
                compact.covers_compact,
                compact.captured,
                compact.clock_remainder,
                compact.null_remainder,
                horizon.covers_compact
            ),
        },
        Card {
            id: "fleet-asteroid-causal".into(),
            look_for: "Many small masses jointly affect a larger body; news arrives at different times; later motion feels the change.".into(),
            allowed_outcome_class: "staggered_arrival".into(),
            model_regime: format!(
                "affine family + delayed policy; family-moment GEM KEEP remainder {:.6} on N=4 rest fixture",
                family.remainder
            ),
            comparison: "compiler_only policy burn; physical_law family remainder ≤ 0.05".into(),
            status: if burns > 0 && family_keep {
                GateStatus::Pass
            } else {
                GateStatus::Fail
            },
            failing_input_visible: true,
            unconfirmed_magnitudes_visible: true,
            evidence: format!("burns={burns} family_admitted={}", family.admitted),
        },
        Card {
            id: "coupled-fleet-hierarchy-inflight-ray-observer-boost".into(),
            look_for: "Conjunction of hierarchy, in-flight light, and delayed fleet feedback on one Engine.".into(),
            allowed_outcome_class: "crossing".into(),
            model_regime: format!(
                "one Engine; GEM diagnostic; {} hosted sidecar; kernel unused",
                MOVING_SCHWARZSCHILD_1PN_LAW_ID
            ),
            comparison: "compiler_only inertial facts; moving compact RK2 vs RK4 dt/4 band 0.05".into(),
            status: if crossing_ok {
                GateStatus::Pass
            } else {
                GateStatus::Fail
            },
            failing_input_visible: true,
            unconfirmed_magnitudes_visible: true,
            evidence: format!(
                "hosted={hosted} captured={engine_captured} remainder={engine_rem:.3e} remnant={remnant_mu} host_moved={engine_moved} in_flight={in_flight} burns={burns} persist={persist_ok}; not a second lab world"
            ),
        },
    ];

    let daily_gallery = vec![SeedCase {
        role: "daily-diagnostic".into(),
        seed: DAILY_SEED,
        intended_outcome_class: "one_way_pulse".into(),
        observed_class: "one_way_pulse".into(),
        status: if in_flight {
            GateStatus::Pass
        } else {
            GateStatus::Fail
        },
        evidence: "fixed lab IC; not the universe; re-seeding cannot erase galaxy/BH FAILs".into(),
        comparison: Some("compiler_exact".into()),
    }];

    let mut held_out = vec![
        held_out_three_body()?,
        held_out_fleet_count()?,
        held_out_compiler_exact()?,
        held_out_numerical_refinement()?,
    ];

    held_out.extend(two_body_behavior.cases.iter().map(|case| SeedCase {
        role: "held-out".into(), seed: case.case.seed,
        intended_outcome_class: "weak-field-finite-orbital-arc".into(),
        observed_class: format!("finite_arc_{}",case.status.to_lowercase()),
        status: match case.status.as_str() { "PASS"=>GateStatus::Pass,"FAIL"=>GateStatus::Fail,_=>GateStatus::Unsupported },
        comparison: Some("physical_law".into()),
        evidence: serde_json::to_string(case).expect("finite bank report"),
    }));

    held_out.extend(newton_two_body_behavior.cases.iter().map(|case| SeedCase {
        role: "held-out-newton-initialized".into(), seed: case.case.seed,
        intended_outcome_class: "weak-field-finite-orbital-arc".into(),
        observed_class: format!("finite_arc_{}",case.status.to_lowercase()),
        status: match case.status.as_str(){"PASS"=>GateStatus::Pass,"FAIL"=>GateStatus::Fail,_=>GateStatus::Unsupported},
        comparison: Some("physical_law".into()),
        evidence: serde_json::to_string(case).expect("finite initialized bank report"),
    }));

    let envelope = vec![
        EnvelopeRung::measured(
            &TINY_RUNG,
            if tiny_ok {
                GateStatus::Pass
            } else {
                GateStatus::Fail
            },
            format!(
                "freeze identities={} families={} members={} horizon={} seed={:#x} activity='{}' queries='{}' reconstruction='{}'; received={} replay={} rss_kb={:?} wall_ns={} digest={} ledger_total={} owned_bytes={:?}; process RSS not isolated heap; fixed IC not the universe; not a ≤4 GiB / 30 FPS claim; does not pin historical 14/43/71 ticks",
                TINY_RUNG.identities,
                TINY_RUNG.families,
                TINY_RUNG.family_members,
                TINY_RUNG.horizon_ticks,
                TINY_RUNG.seed,
                TINY_RUNG.independent_activity,
                TINY_RUNG.queries,
                TINY_RUNG.reconstruction,
                tiny_m.received,
                tiny_m.replay_ok,
                tiny_m.rss_kb,
                tiny_m.wall_ns,
                tiny_m.digest,
                tiny_m.ledger_total,
                tiny_m.owned_bytes
            ),
            tiny_m.rss_kb,
            tiny_m.wall_ns,
            tiny_m.digest.clone(),
            tiny_m.ledger_total,
            tiny_m.owned_bytes,
        ),
        EnvelopeRung::measured(
            &CONNECTED_RUNG,
            if connected_rung_ok {
                GateStatus::Pass
            } else {
                GateStatus::Fail
            },
            format!(
                "freeze identities={} families={} members={} horizon={} seed={:#x} activity='{}' queries='{}' reconstruction='{}'; persist={} in_flight={} ship_decode={} asteroid={} rss_kb={:?} wall_ns={} digest={} ledger_total={} owned_bytes={:?}; nested Charge from GEM compile children; process RSS not isolated heap; fixed IC not the universe; not a ≤4 GiB / 30 FPS / billion-identity claim",
                CONNECTED_RUNG.identities,
                CONNECTED_RUNG.families,
                CONNECTED_RUNG.family_members,
                CONNECTED_RUNG.horizon_ticks,
                CONNECTED_RUNG.seed,
                CONNECTED_RUNG.independent_activity,
                CONNECTED_RUNG.queries,
                CONNECTED_RUNG.reconstruction,
                persist_ok,
                in_flight,
                ship_query_ok,
                asteroid_ok,
                connected_rss_kb,
                connected_wall_ns,
                connected_digest,
                connected_ledger_total,
                connected_owned_bytes
            ),
            connected_rss_kb,
            connected_wall_ns,
            connected_digest,
            connected_ledger_total,
            connected_owned_bytes,
        ),
        EnvelopeRung::measured(
            &PRESSURE_RUNG,
            if pressure_m.ok {
                GateStatus::Pass
            } else {
                GateStatus::Fail
            },
            format!(
                "freeze identities={} families={} members={} horizon={} seed={:#x} activity='{}' queries='{}' reconstruction='{}'; limiter={} yield_pauses={} colloc_ns={} adv_ns={} recon_ns={} oracle_ns={} far={} replay={} oracle={} rss_kb={:?} wall_ns={} digest={} ledger_total={} residual_bytes={:?}; mixed quiet/hot packed island; process RSS not isolated heap; not a ≤4 GiB / 30 FPS / billion-identity claim",
                PRESSURE_RUNG.identities,
                PRESSURE_RUNG.families,
                PRESSURE_RUNG.family_members,
                PRESSURE_RUNG.horizon_ticks,
                PRESSURE_RUNG.seed,
                PRESSURE_RUNG.independent_activity,
                PRESSURE_RUNG.queries,
                PRESSURE_RUNG.reconstruction,
                pressure_m.limiter,
                pressure_m.yield_pauses,
                pressure_m.collocation_ns,
                pressure_m.advance_ns,
                pressure_m.reconstruction_ns,
                pressure_m.oracle_ns,
                pressure_m.far_ok,
                pressure_m.replay_ok,
                pressure_m.oracle_ok,
                pressure_m.rss_kb,
                pressure_m.wall_ns,
                pressure_m.digest,
                pressure_m.ledger_total,
                pressure_m.owned_bytes
            ),
            pressure_m.rss_kb,
            pressure_m.wall_ns,
            pressure_m.digest.clone(),
            pressure_m.ledger_total,
            pressure_m.owned_bytes,
        )
        .with_pressure(
            pressure_m.limiter,
            pressure_m.yield_pauses,
            pressure_m.collocation_ns,
            pressure_m.reconstruction_ns,
            pressure_m.advance_ns,
            pressure_m.oracle_ns,
        ),
        EnvelopeRung::unsupported(
            "frozen-integrated-target",
            "≤4 GiB / 30 FPS / ≤5 ms yield / billion-identity hour",
            "no frozen large workload exists; tiny/connected/pressure RSS/time/digest do not promote this target",
        ),
    ];

    Ok(I6Report {
        schema: 2,
        id: "i6-same-model-matrix-20260915".into(),
        canonical_law: LAW_ID.into(),
        diagnostic_response: COUPLED_RESPONSE_LAW_ID.into(),
        implementation: "emergent-full-engine-integration".into(),
        workload: "connected-family-hierarchy-inflight-ray-observer-policy-archive".into(),
        production_law: None,
        canonical_gravity_acceptance: CANONICAL_GRAVITY_ACCEPTANCE.into(),
        promotion: false,
        plan_i6_exit: "matrix-run".into(),
        full_engine: false,
        observatory,
        gates,
        cards,
        daily_gallery,
        held_out,
        two_body_behavior,
        initialized_two_body_behavior,
        newton_two_body_behavior,
        solar_window,
        envelope,
    })
}

fn held_out_three_body() -> Result<SeedCase, EngineError> {
    let a = body(1, "a", 0, 0, 1);
    let b = body(2, "b", 8, 0, 1);
    let c = body(3, "c", 4, 6, 1);
    let mut e = Engine::new(HELD_OUT_THREE_BODY, vec![a, b, c], vec![])?;
    e.advance_fully(20)?;
    let contacts = e
        .sorted_events()
        .iter()
        .filter(|ev| ev.kind == "contact")
        .count();
    let class = if contacts > 0 {
        "inertial_contacts"
    } else {
        "stationary_noninteracting_bodies"
    };
    Ok(SeedCase {
        role: "held-out".into(),
        seed: HELD_OUT_THREE_BODY,
        intended_outcome_class: "chaotic_close_pass".into(),
        observed_class: class.into(),
        status: GateStatus::Unsupported,
        evidence: format!(
            "fixed stationary inertial IC; seed is engine metadata, not an IC generator; contacts={contacts}; no gravitational three-body evolution or chaotic-close-pass classifier is implemented for this row"
        ),
        comparison: Some("compiler_exact".into()),
    })
}

fn held_out_fleet_count() -> Result<SeedCase, EngineError> {
    let family = Family::affine(
        "held-out-lane",
        10_000,
        3,
        0,
        Inertial::new(0, Vec2::new(40, 0), Vec2::zero())?,
        Vec2::new(8, 0),
        r(1),
        r(10),
    );
    let e = Engine::new(HELD_OUT_FLEET, vec![], vec![family])?;
    Ok(SeedCase {
        role: "held-out".into(),
        seed: HELD_OUT_FLEET,
        intended_outcome_class: "clumpy_collection".into(),
        observed_class: "stationary_affine_family".into(),
        status: GateStatus::Unsupported,
        evidence: format!(
            "fixed stationary affine IC; seed is engine metadata, not an IC generator; measured family count={}; population count does not validate clumpy collection dynamics or gravitational aggregation",
            e.logical_count()
        ),
        comparison: Some("compiler_exact".into()),
    })
}

fn held_out_compiler_exact() -> Result<SeedCase, EngineError> {
    let emitter = body(1, "held-emitter", 0, 0, 0);
    let mut receiver = body(2, "held-receiver", 12, 0, 1);
    receiver.stop_on_contact = true;
    let mut engine = Engine::new(HELD_OUT_COMPILER, vec![emitter, receiver], vec![])?;
    engine.intervene(
        1,
        Command::SendSignal {
            target: 2,
            payload: Payload::Ping,
        },
    )?;
    engine.advance_fully(24)?;
    let digest = engine.history_digest(engine.state.clock)?;
    let replayed = engine.replay()?;
    let replay_ok = replayed.history_digest(replayed.state.clock)? == digest;
    let oracle_ok = engine.canonical_facts_agree(engine.state.clock)?;
    let pass = replay_ok && oracle_ok;
    Ok(SeedCase {
        role: "held-out".into(),
        seed: HELD_OUT_COMPILER,
        intended_outcome_class: "compiler_exact_digest".into(),
        observed_class: if pass {
            "compiler_exact_digest".into()
        } else {
            "compiler_mismatch".into()
        },
        status: if pass {
            GateStatus::Pass
        } else {
            GateStatus::Fail
        },
        evidence: format!(
            "comparison=compiler_exact replay={replay_ok} oracle={oracle_ok}; fixed inertial IC with engine seed metadata, not a generated many-seed physical workload; re-seeding cannot erase galaxy quadrupole FAIL"
        ),
        comparison: Some("compiler_exact".into()),
    })
}

fn held_out_numerical_refinement() -> Result<SeedCase, EngineError> {
    let mut host = MovingCompactDiagnostic::new(HELD_OUT_REFINEMENT);
    host.poll_steps(64);
    let remainder = host.remainder_vs_slow();
    let pass = remainder <= BAND;
    Ok(SeedCase {
        role: "held-out".into(),
        seed: HELD_OUT_REFINEMENT,
        intended_outcome_class: "numerical_refinement_band".into(),
        observed_class: if pass {
            "numerical_refinement_band".into()
        } else {
            "refinement_remainder_outside_band".into()
        },
        status: if pass {
            GateStatus::Pass
        } else {
            GateStatus::Fail
        },
        evidence: format!(
            "comparison=numerical_refinement RK2 vs RK4 dt/4 remainder={remainder:.3e} band={BAND}; seed changes only one of seven rotations (seed % 7) of the same radial capture IC; both integrators share the law derivatives, so this is numerical refinement, not independent physical-law validation; does not re-seed galaxy quadrupole FAIL"
        ),
        comparison: Some("numerical_refinement".into()),
    })
}
