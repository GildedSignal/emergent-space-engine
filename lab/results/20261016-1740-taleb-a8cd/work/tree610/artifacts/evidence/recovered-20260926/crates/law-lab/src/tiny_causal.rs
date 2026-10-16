//! Frozen tiny causal-evolution specification.
//!
//! Law id: `es-causal-retarded-gem-v0`. Piecewise retarded linearized-metric
//! (GEM) patches for two or three moving sources. Discrete-action / Fokker-AVI
//! was rejected incomplete. This module records the frozen falsifiers and
//! refuses a map: fixtures were frozen before any new integrator.
//!
//! Not `es-inertial-causal-v1`, not delayed-Newton-as-G2, not 2D log gravity,
//! not a Schwarzschild/Kerr patch, not wired into the engine. G2 stays FAIL.
//! `production_law` stays null.

use super::causal_kernel::{C, INERTIAL_LAB_LAW_ID, RESEARCH_LAW_ID};
use super::coupled::COUPLED_LAW_ID;
use super::schwarzschild::SCHWARZSCHILD_LAW_ID;
use super::{gate, CandidateReport};
use serde::Deserialize;

pub const GEM_LAW_ID: &str = "es-causal-retarded-gem-v0";
pub const MAP_NOT_IMPLEMENTED: &str = "map not implemented; fixtures frozen";
const POSITION_DENOM: i128 = 1 << 20;
const MAX_BODIES: usize = 3;
const CLOCK_FRACTIONAL_BITS: i128 = 32;
const PRESENT_ALIGNMENT_DOT_MIN: [i128; 2] = [2047, 2048];
const BETA_TRANSLATING: [i128; 2] = [1, 16];
const STATIC_KERNEL_RELATIVE_ERROR_MAX: f64 = 1e-12;
const ABERRATION_QUERY_TIME: [i128; 2] = [1, 8];
const ABERRATION_QUERY_POSITION: [[i128; 2]; 2] = [[0, 1], [4, 1]];
const MOMENTUM_DEFINITION: &str = "coordinate_mu_v";
const LEDGER_ROLE: &str = "audit-only";
const CAPTURED_MOMENTUM: &str = "zero_after_transfer";
const PAST_SEGMENT_MU: &str = "retained";
const MUTUAL_INTERIOR_TIE: &str = "worldtube-order";
const CONS_REMAINDER: &str = "interval_membership";
const KINK_RADIATION: &str = "omitted";
const ALIGNMENT_REFERENCE: &str = "present_coasting_newton";

pub const NAMED_EQUATIONS: [&str; 24] = [
    "C-CONE",
    "C-RET",
    "C-SEG",
    "GEM-PHI",
    "GEM-XI",
    "METRIC",
    "GEM-E",
    "GEM-B",
    "GEM-GRAD",
    "GEM-a",
    "GEM-STATIC",
    "GEM-ABERR",
    "CLK",
    "SIG",
    "INT",
    "ABS-CLASS",
    "ABS",
    "CONS",
    "EXT-INIT",
    "EXT-EVOL",
    "EXT-OBS",
    "MAP",
    "PROP",
    "COMPOSE",
];

pub const TINY_CAUSAL_FIXTURE_IDS: [&str; 19] = [
    "three_source_admitted_ivp",
    "translating_source_aberration",
    "short_binary_exchange",
    "accounted_burn_precone",
    "capture_transfers_momentum",
    "exterior_remainder_survives_step",
    "coherent_perturbation_eventually_matters",
    "grazing_cone_tie_visible",
    "unsupported_four_source_refuses",
    "budget_exhausted_not_a_sign",
    "propagation_returns_state",
    "composition_direct_vs_subdivided",
    "clock_inertial_limit",
    "signal_on_minkowski_cone",
    "observation_does_not_source",
    "retarded_newton_fails_aberration",
    "coupled_euler_zeros_capture_momentum",
    "schwarzschild_classifier_not_propagation",
    "static_kernel_matches_monopole",
];

const MANIFEST: &str = include_str!("../../../scenarios/law-gates.json");

#[derive(Clone, Deserialize)]
struct FileSlice {
    aggregate_gates: FrozenAggregates,
    required_production_gates: Vec<String>,
    tiny_causal_law_research: TinyCausalManifest,
}

#[derive(Clone, Deserialize)]
struct FrozenAggregates {
    pre_lightcone_response_max: f64,
    backreaction_relative_error_max: f64,
}

#[derive(Clone, Deserialize)]
struct TinyCausalManifest {
    law_id: String,
    status: String,
    spec: String,
    competition_winner: String,
    discrete_action: String,
    piecewise_metric: String,
    map_status: String,
    parent_kernel: String,
    coupled_kernel: String,
    schwarzschild_kernel: String,
    light_speed: i128,
    max_bodies: usize,
    step: [i128; 2],
    position_denom: i128,
    beta_translating: [i128; 2],
    present_alignment_dot_min: [i128; 2],
    static_kernel_relative_error_max: f64,
    pre_lightcone_response_max: f64,
    post_lightcone_influence_min: f64,
    post_lightcone_influence_strict: bool,
    clock_fractional_bits: i128,
    momentum_definition: String,
    ledger_role: String,
    captured_momentum: String,
    past_segment_mu: String,
    mutual_interior_tie: String,
    cons_remainder: String,
    kink_radiation: String,
    alignment_reference: String,
    aberration_query_event: EventPin,
    named_equations: Vec<String>,
    fixtures: Vec<NamedFixture>,
}

#[derive(Clone, Deserialize, PartialEq, Eq)]
struct EventPin {
    time: [i128; 2],
    position: [[i128; 2]; 2],
}

#[derive(Clone, Deserialize)]
struct NamedFixture {
    id: String,
    #[serde(default)]
    kind: String,
    #[serde(default)]
    query_event: Option<EventPin>,
    #[serde(default)]
    query_position: Option<[[i128; 2]; 2]>,
    #[serde(default)]
    post_cone_time: Option<[i128; 2]>,
    #[serde(default)]
    present_alignment_dot_min: Option<[i128; 2]>,
    #[serde(default)]
    alignment_reference: Option<String>,
    #[serde(default)]
    accounting: Option<String>,
    #[serde(default)]
    not_newton_third_law: Option<bool>,
    #[serde(default)]
    remainder_update: Option<String>,
    #[serde(default)]
    cons_remainder: Option<String>,
    #[serde(default)]
    captured_momentum: Option<String>,
    #[serde(default)]
    past_segment_mu: Option<String>,
    #[serde(default)]
    ledger_role: Option<String>,
    #[serde(default)]
    momentum_definition: Option<String>,
    #[serde(default)]
    mutual_interior_tie: Option<String>,
    #[serde(default)]
    pre_cone_influence_max: Option<f64>,
    #[serde(default)]
    post_cone_influence_strict: Option<bool>,
}

/// Finite map of the specified law. Intentionally unimplemented: falsifiers
/// were frozen first. Authored worldtubes are not a valid substitute.
pub fn advance_map() -> Result<NeverState, TinyCausalError> {
    Err(TinyCausalError::MapNotImplemented)
}

/// Marker: no laboratory state is produced until a later map lands against
/// the frozen fixtures.
#[derive(Clone, Debug)]
pub struct NeverState;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum TinyCausalError {
    MapNotImplemented,
}

impl std::fmt::Display for TinyCausalError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(MAP_NOT_IMPLEMENTED)
    }
}

pub fn tiny_causal_manifest() -> Result<(), String> {
    let slice: FileSlice = serde_json::from_str(MANIFEST).map_err(|e| e.to_string())?;
    let m = &slice.tiny_causal_law_research;
    if m.law_id != GEM_LAW_ID {
        return Err("tiny causal law id drifted".into());
    }
    if m.law_id == INERTIAL_LAB_LAW_ID
        || m.law_id == RESEARCH_LAW_ID
        || m.law_id == COUPLED_LAW_ID
        || m.law_id == SCHWARZSCHILD_LAW_ID
    {
        return Err("tiny causal law must keep a distinct research id".into());
    }
    if m.status != "research-not-production"
        || m.spec != "docs/laws/causal-retarded-gem-v0.md"
        || m.competition_winner != "piecewise-retarded-linearized-metric"
        || m.discrete_action != "rejected-incomplete"
        || m.piecewise_metric != "accepted-tiny-domain"
        || m.map_status != "not-implemented"
    {
        return Err("tiny causal spec competition verdict drifted".into());
    }
    if m.parent_kernel != RESEARCH_LAW_ID {
        return Err("tiny causal parent must remain the retarded monopole kernel".into());
    }
    if m.coupled_kernel != COUPLED_LAW_ID {
        return Err("tiny causal coupled kernel id drifted".into());
    }
    if m.schwarzschild_kernel != SCHWARZSCHILD_LAW_ID {
        return Err("tiny causal Schwarzschild kernel id drifted".into());
    }
    if m.light_speed != C
        || m.max_bodies != MAX_BODIES
        || m.step != [1, C]
        || m.position_denom != POSITION_DENOM
        || m.beta_translating != BETA_TRANSLATING
        || m.present_alignment_dot_min != PRESENT_ALIGNMENT_DOT_MIN
        || m.static_kernel_relative_error_max != STATIC_KERNEL_RELATIVE_ERROR_MAX
        || m.pre_lightcone_response_max != 0.0
        || m.post_lightcone_influence_min != 0.0
        || !m.post_lightcone_influence_strict
        || m.clock_fractional_bits != CLOCK_FRACTIONAL_BITS
    {
        return Err("tiny-causal research thresholds were weakened or retuned".into());
    }
    if slice.aggregate_gates.pre_lightcone_response_max != 0.0
        || slice.aggregate_gates.backreaction_relative_error_max != 1e-12
    {
        return Err("frozen aggregate thresholds were edited".into());
    }
    let required = [
        "orbit_stability",
        "angular_isotropy",
        "quantum_refinement",
        "stationary_clock",
        "source_tree_bound",
        "source_backreaction",
        "causal_dynamic_sources",
        "well_posed_exterior",
        "compact_field_certification",
        "terminating_exact_branches",
    ];
    if slice.required_production_gates != required {
        return Err("required production gates were edited".into());
    }
    let equations: Vec<&str> = m.named_equations.iter().map(String::as_str).collect();
    if equations != NAMED_EQUATIONS {
        return Err("tiny causal named equations were renamed, dropped or reordered".into());
    }
    let ids: Vec<&str> = m.fixtures.iter().map(|f| f.id.as_str()).collect();
    if ids != TINY_CAUSAL_FIXTURE_IDS {
        return Err("tiny causal fixtures were renamed, dropped or reordered".into());
    }
    pin_spec_patch(m)?;
    Ok(())
}

fn fixture<'a>(m: &'a TinyCausalManifest, id: &str) -> Result<&'a NamedFixture, String> {
    m.fixtures
        .iter()
        .find(|f| f.id == id)
        .ok_or_else(|| format!("missing tiny-causal fixture {id}"))
}

fn pin_spec_patch(m: &TinyCausalManifest) -> Result<(), String> {
    if m.momentum_definition != MOMENTUM_DEFINITION
        || m.ledger_role != LEDGER_ROLE
        || m.captured_momentum != CAPTURED_MOMENTUM
        || m.past_segment_mu != PAST_SEGMENT_MU
        || m.mutual_interior_tie != MUTUAL_INTERIOR_TIE
        || m.cons_remainder != CONS_REMAINDER
        || m.kink_radiation != KINK_RADIATION
        || m.alignment_reference != ALIGNMENT_REFERENCE
    {
        return Err("tiny-causal CONS/ABS/C-RET spec-patch identities drifted".into());
    }
    if m.aberration_query_event.time != ABERRATION_QUERY_TIME
        || m.aberration_query_event.position != ABERRATION_QUERY_POSITION
    {
        return Err("aberration query event drifted from (t,x)=(1/8,(0,4))".into());
    }

    let translating = fixture(m, "translating_source_aberration")?;
    if translating.query_event.as_ref() != Some(&m.aberration_query_event)
        || translating.post_cone_time != Some(ABERRATION_QUERY_TIME)
        || translating.query_position != Some(ABERRATION_QUERY_POSITION)
        || translating.present_alignment_dot_min != Some(PRESENT_ALIGNMENT_DOT_MIN)
        || translating.alignment_reference.as_deref() != Some(ALIGNMENT_REFERENCE)
    {
        return Err(
            "translating_source_aberration is not pinned to present-coasting Newton at (1/8,(0,4)) with 2047/2048"
                .into(),
        );
    }

    let newton = fixture(m, "retarded_newton_fails_aberration")?;
    if newton.query_event.as_ref() != Some(&m.aberration_query_event)
        || newton.present_alignment_dot_min != Some(PRESENT_ALIGNMENT_DOT_MIN)
        || newton.alignment_reference.as_deref() != Some(ALIGNMENT_REFERENCE)
    {
        return Err(
            "monopole negative control must use the same aberration event and 2047/2048 bound"
                .into(),
        );
    }

    let binary = fixture(m, "short_binary_exchange")?;
    if binary.kind != "causal_accounted_exchange"
        || binary.accounting.as_deref() != Some("cons-membership-not-third-law")
        || binary.not_newton_third_law != Some(true)
        || binary.pre_cone_influence_max.map(f64::to_bits) != Some(0.0f64.to_bits())
        || binary.post_cone_influence_strict != Some(true)
    {
        return Err(
            "short_binary_exchange must stay pre-cone zero / post-cone nonzero CONS accounting, not a 3rd-law Σp test"
                .into(),
        );
    }

    let capture = fixture(m, "capture_transfers_momentum")?;
    if capture.momentum_definition.as_deref() != Some(MOMENTUM_DEFINITION)
        || capture.captured_momentum.as_deref() != Some(CAPTURED_MOMENTUM)
        || capture.past_segment_mu.as_deref() != Some(PAST_SEGMENT_MU)
        || capture.ledger_role.as_deref() != Some(LEDGER_ROLE)
        || capture.mutual_interior_tie.as_deref() != Some(MUTUAL_INTERIOR_TIE)
    {
        return Err(
            "capture_transfers_momentum must keep p:=μv, p_i←0, past μ, audit-only ledger, worldtube-order tie"
                .into(),
        );
    }

    let exterior = fixture(m, "exterior_remainder_survives_step")?;
    if exterior.remainder_update.as_deref() != Some("keep_enclosure_or_promote_before_cone")
        || exterior.cons_remainder.as_deref() != Some(CONS_REMAINDER)
    {
        return Err(
            "exterior remainder must keep enclosure or promote before the omitted cone, with CONS membership"
                .into(),
        );
    }
    Ok(())
}

pub fn qualify_tiny_causal_spec() -> CandidateReport {
    let mut report = CandidateReport {
        id: GEM_LAW_ID.into(),
        version: 0,
        status: "FAIL".into(),
        metrics: Vec::new(),
        gates: Vec::new(),
        evidence: vec![
            "Research spec es-causal-retarded-gem-v0 is isolated from es-inertial-causal-v1.".into(),
            "Specification competition: discrete-action/Fokker-AVI rejected incomplete; piecewise retarded linearized-metric (GEM) accepted on the N∈{2,3} domain.".into(),
            "Named transition rules cover matter, field/history, remainder, clocks, Minkowski signals, accounted interventions, and capture with coordinate p:=μv transfer (ledger audit-only; past μ retained). Fixtures frozen; map still refused.".into(),
            "Not delayed-Newton-as-G2, not 2D log gravity, not a Schwarzschild/Kerr patch. Aberration cosine 2047/2048 on β=1/16 is frozen at (t,x)=(1/8,(0,4)) vs present coasting Newton.".into(),
            "G2 stays FAIL. compact_field_certification stays FAIL. terminating_exact_branches stays FAIL. production_law stays null.".into(),
        ],
    };

    match tiny_causal_manifest() {
        Ok(()) => gate(
            &mut report,
            "tiny_causal_manifest_isolated",
            true,
            "New tiny-causal fixtures did not edit frozen production-gate identities or old numeric thresholds.",
        ),
        Err(error) => gate(&mut report, "tiny_causal_manifest_isolated", false, error),
    }

    match advance_map() {
        Err(TinyCausalError::MapNotImplemented) => gate(
            &mut report,
            "map_frozen_unimplemented",
            true,
            MAP_NOT_IMPLEMENTED,
        ),
        Ok(NeverState) => gate(
            &mut report,
            "map_frozen_unimplemented",
            false,
            "A map returned state before frozen falsifiers were allowed to fail closed.",
        ),
    }

    for (id, reason) in [
        (
            "complete_dynamic_transition",
            MAP_NOT_IMPLEMENTED,
        ),
        (
            "causal_moving_source_exchange",
            MAP_NOT_IMPLEMENTED,
        ),
        (
            "exterior_through_evolution",
            MAP_NOT_IMPLEMENTED,
        ),
        (
            "useful_finite_branch_decisions",
            MAP_NOT_IMPLEMENTED,
        ),
        (
            "actual_propagation_and_reuse",
            MAP_NOT_IMPLEMENTED,
        ),
        (
            "causal_dynamic_sources",
            "Spec frozen; no GEM map. Delayed Newton is not this law and is not G2.",
        ),
        (
            "well_posed_exterior",
            "Remainder-through-evolution is specified; the map that must retain it is not implemented.",
        ),
        (
            "source_backreaction",
            "GEM excluded-self coupling is specified; instantaneous Newton third-law is not a rule of this law.",
        ),
        (
            "compact_field_certification",
            "Capture-with-transfer is specified; that is not Schwarzschild/Kerr certification.",
        ),
        (
            "terminating_exact_branches",
            "Cone/compact/N-domain predicates are specified; GEM field values remain f64 until enclosed.",
        ),
    ] {
        gate(&mut report, id, false, reason);
    }

    report
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn tiny_causal_manifest_is_frozen_and_additive() {
        tiny_causal_manifest().unwrap();
        crate::causal_kernel::research_manifest().unwrap();
        crate::coupled::coupled_manifest().unwrap();
        crate::compact::compact_manifest().unwrap();
        crate::exact_branch::exact_branch_manifest().unwrap();
        crate::schwarzschild::schwarzschild_manifest().unwrap();
    }

    #[test]
    fn gem_law_is_not_an_existing_identity() {
        assert_ne!(GEM_LAW_ID, INERTIAL_LAB_LAW_ID);
        assert_ne!(GEM_LAW_ID, RESEARCH_LAW_ID);
        assert_ne!(GEM_LAW_ID, COUPLED_LAW_ID);
        assert_ne!(GEM_LAW_ID, SCHWARZSCHILD_LAW_ID);
        assert_eq!(TINY_CAUSAL_FIXTURE_IDS.len(), 19);
        assert_eq!(NAMED_EQUATIONS.len(), 24);
        assert_eq!(PRESENT_ALIGNMENT_DOT_MIN, [2047, 2048]);
        assert!(NAMED_EQUATIONS.contains(&"GEM-GRAD"));
    }

    #[test]
    fn spec_patch_pins_aberration_event_without_retuning() {
        tiny_causal_manifest().unwrap();
        assert_eq!(PRESENT_ALIGNMENT_DOT_MIN, [2047, 2048]);
        assert_eq!(ABERRATION_QUERY_TIME, [1, 8]);
        assert_eq!(ABERRATION_QUERY_POSITION, [[0, 1], [4, 1]]);
        assert_eq!(ALIGNMENT_REFERENCE, "present_coasting_newton");
        assert_eq!(LEDGER_ROLE, "audit-only");
        assert_eq!(CAPTURED_MOMENTUM, "zero_after_transfer");
        assert_eq!(KINK_RADIATION, "omitted");
        assert_eq!(CONS_REMAINDER, "interval_membership");
    }

    #[test]
    fn advance_map_is_refused_until_fixtures_are_frozen() {
        assert_eq!(
            advance_map().unwrap_err(),
            TinyCausalError::MapNotImplemented
        );
    }

    #[test]
    fn spec_qualify_does_not_promote() {
        let report = qualify_tiny_causal_spec();
        assert_eq!(report.id, GEM_LAW_ID);
        assert_eq!(report.status, "FAIL");
        assert!(report
            .gates
            .iter()
            .any(|g| g.id == "tiny_causal_manifest_isolated" && g.passed));
        assert!(report
            .gates
            .iter()
            .any(|g| g.id == "map_frozen_unimplemented" && g.passed));
        for id in [
            "complete_dynamic_transition",
            "causal_moving_source_exchange",
            "exterior_through_evolution",
            "useful_finite_branch_decisions",
            "actual_propagation_and_reuse",
            "causal_dynamic_sources",
            "compact_field_certification",
            "terminating_exact_branches",
        ] {
            let gate = report.gates.iter().find(|g| g.id == id).unwrap();
            assert!(!gate.passed, "{id} must remain failed until a map lands");
        }
    }
}
