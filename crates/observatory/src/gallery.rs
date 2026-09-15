//! Six-card host for the H0100/H0101 GEM-response slice.
//!
//! Frozen card ids and look-for cues come from
//! `docs/laws/litmus-gallery-contract-20260914.md`. Charged overlays sample
//! `es-linearized-retarded-gem-response-v0` in law-lab. This is not
//! `production_law`, not `Engine::advance`, and not the H0091 inertial
//! gallery relabelled as gravity. Native GUI/wgpu is not this module.

use emergent_law_lab::coupled_interval_enclosure::{
    enclose_compiled_interval, IntervalMethod,
};
use emergent_law_lab::coupled_source_response::{
    body_state, compile_source_response, complete_required_queries_compiled, fly_ray,
    laboratory_encounter, laboratory_kick, laboratory_two_body, recouple_compiled_pair,
    repair_from_committed, Charge, Intervention, SourceResponse, COUPLED_RESPONSE_LAW_ID,
};
use emergent_law_lab::coupled_interval_enclosure::laboratory_close_pair;

pub const RNG_VERSION: &str = "emergent-space-random-v1";
pub const COUPLED_TRANSITION_ID: &str = "coupled-fleet-hierarchy-inflight-ray-observer-boost";
pub const BANDS_STATUS: &str = "UNCONFIRMED";
pub const GEM_LAW_ID: &str = COUPLED_RESPONSE_LAW_ID;
pub const INERTIAL_LAW_ID: &str = "es-inertial-causal-v1";
pub const HOST_LABEL: &str = "gem-response-slice";

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum CardId {
    FastShipsLightTwins,
    SolarSystemHierarchy,
    ThreeBodies,
    GalaxyLikePopulation,
    BlackHoleNearMass,
    FleetAsteroidCausal,
}

impl CardId {
    pub const ALL: [CardId; 6] = [
        CardId::FastShipsLightTwins,
        CardId::SolarSystemHierarchy,
        CardId::ThreeBodies,
        CardId::GalaxyLikePopulation,
        CardId::BlackHoleNearMass,
        CardId::FleetAsteroidCausal,
    ];

    pub fn as_str(self) -> &'static str {
        match self {
            CardId::FastShipsLightTwins => "fast-ships-light-twins",
            CardId::SolarSystemHierarchy => "solar-system-hierarchy",
            CardId::ThreeBodies => "three-bodies",
            CardId::GalaxyLikePopulation => "galaxy-like-population",
            CardId::BlackHoleNearMass => "black-hole-near-mass",
            CardId::FleetAsteroidCausal => "fleet-asteroid-causal",
        }
    }

    pub fn title(self) -> &'static str {
        match self {
            CardId::FastShipsLightTwins => "Fast ships, light and twins",
            CardId::SolarSystemHierarchy => "Solar system and hierarchy",
            CardId::ThreeBodies => "Three bodies",
            CardId::GalaxyLikePopulation => "Galaxy-like self-gravitating population",
            CardId::BlackHoleNearMass => "Black hole, near-mass rays and clocks",
            CardId::FleetAsteroidCausal => "Fleet, asteroid and causal intervention",
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum CardSupport {
    /// Implemented weak-field coupled loop on this slice.
    GemSlice,
    /// Outside the admitted GEM band or not a solved product on this id.
    Unsupported,
}

impl CardSupport {
    pub fn as_str(self) -> &'static str {
        match self {
            CardSupport::GemSlice => "gem-slice",
            CardSupport::Unsupported => "unsupported",
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum WorkOverlayKind {
    Reuse,
    NewlyCompiled,
    Refinement,
    RepairedPrediction,
}

impl WorkOverlayKind {
    pub const ALL: [WorkOverlayKind; 4] = [
        WorkOverlayKind::Reuse,
        WorkOverlayKind::NewlyCompiled,
        WorkOverlayKind::Refinement,
        WorkOverlayKind::RepairedPrediction,
    ];

    pub fn as_str(self) -> &'static str {
        match self {
            WorkOverlayKind::Reuse => "reuse",
            WorkOverlayKind::NewlyCompiled => "newly_compiled",
            WorkOverlayKind::Refinement => "refinement",
            WorkOverlayKind::RepairedPrediction => "repaired_prediction",
        }
    }
}

#[derive(Clone, Debug)]
pub struct CardView {
    pub id: CardId,
    pub title: String,
    pub glance: String,
    pub look_for: String,
    pub looks_wrong: Vec<String>,
    pub do_not_force: String,
    pub allowed_classes: Vec<String>,
    pub support: CardSupport,
    pub support_note: String,
    /// Host that actually draws this card. Never "this law" when inertial.
    pub host_law_id: String,
}

#[derive(Clone, Debug)]
pub struct OverlayCell {
    pub identity: String,
    pub kind: WorkOverlayKind,
    pub chart_position: [f64; 2],
}

#[derive(Clone, Debug)]
pub struct GemWorkSample {
    pub kind: WorkOverlayKind,
    pub charged: bool,
    pub mutates_world: bool,
    pub law_id: String,
    pub host_label: String,
    pub source_ops_before: u64,
    pub source_ops_after: u64,
    pub consumer_ops: u64,
    /// Consumers charged by `complete_required_queries_compiled`. Extra-ray
    /// overlay work is a different counter; this field is 0 when those
    /// compiled queries did not run.
    pub required_query_consumers: u64,
    pub required_queries_compiled: bool,
    /// Source-compile API that produced `cells`. Fast-ships must be
    /// `complete_required_queries_compiled`; three-bodies must be
    /// `recouple_compiled_pair`. Extra-ray Reuse overlay is not this field.
    pub overlay_api: String,
    pub genesis_body_ids: Vec<u64>,
    pub enclosure_certified: Option<bool>,
    pub enclosure_q: Option<f64>,
    pub enclosure_method: Option<String>,
    pub production_law: Option<String>,
    pub cells: Vec<OverlayCell>,
}

impl GemWorkSample {
    pub fn source_ops_unchanged(&self) -> bool {
        self.source_ops_before == self.source_ops_after
    }
}

#[derive(Clone, Debug)]
pub struct GemGalleryHost {
    pub cards: Vec<CardView>,
    pub selected: CardId,
    pub intended_class: String,
    pub seed: u64,
    pub seed_bank: String,
    pub comparison_class: String,
    pub coupled_transition_id: Option<String>,
    pub work: Option<GemWorkSample>,
    pub bands_status: String,
    pub playback_law_id: String,
    pub playback_cached: bool,
    pub production_law: Option<String>,
    pub default_engine_law: String,
}

fn card_view(id: CardId) -> CardView {
    match id {
        CardId::FastShipsLightTwins => CardView {
            id,
            title: id.title().into(),
            glance: "Light always leaves at c; clocks and sky fit the motion.".into(),
            look_for: "Held-out ship + ray + clock on the same GEM worldtubes; ray emit after motion; kick while the ray flies; Φ=0 clock matches inertial. Pulses reach moving receivers in an order that matches emission events and finite c.".into(),
            looks_wrong: vec![
                "Emitter speed is added to light".into(),
                "UnsupportedPredicate on required ray/clock".into(),
                "Rotating or boosting the camera changes when pulses meet".into(),
                "Inertial host motion sold as this GEM law".into(),
            ],
            do_not_force: "Not every seed is a closed twin circuit. A one-way pulse on this weak-field slice is enough if arrivals and clocks fit the motion.".into(),
            allowed_classes: vec![
                "one_way_pulse".into(),
                "moving_receiver".into(),
                "twin_reunion".into(),
                "aberration_only".into(),
            ],
            support: CardSupport::GemSlice,
            support_note: "partial on the implemented weak-field coupled loop".into(),
            host_law_id: GEM_LAW_ID.into(),
        },
        CardId::SolarSystemHierarchy => CardView {
            id,
            title: id.title().into(),
            glance: "A supported hierarchy stays organized; a kick breathes, it does not snap to a circle.".into(),
            look_for: "Not claimed on this slice.".into(),
            looks_wrong: vec![
                "Reading the two-ball laboratory as a solar system".into(),
                "Inertial overlay labelled as this GEM law".into(),
                "Every orbit forced perfect".into(),
                "A small kick instantly circularizes the hierarchy".into(),
            ],
            do_not_force: "Do not force a miniature Solar System out of the two-body GEM laboratory.".into(),
            allowed_classes: vec![
                "supported_hierarchy".into(),
                "binary_plus_companion".into(),
                "perturbed_precessing".into(),
                "compact_pair".into(),
            ],
            support: CardSupport::Unsupported,
            support_note: "unsupported: two-body laboratory is not a solar-system product".into(),
            host_law_id: GEM_LAW_ID.into(),
        },
        CardId::ThreeBodies => CardView {
            id,
            title: id.title().into(),
            glance: "Nested seeds can stay bound; encounter seeds can swap, eject, or go messy.".into(),
            look_for: "Recoupled encounter compile-once/reuse of certified interval functions vs an independent kicked same-IC; pair share still refuses at 1.519. Encounter only; not a solved three-body product.".into(),
            looks_wrong: vec![
                "Treating the encounter as a solved three-body product".into(),
                "Bodies jump through encounters".into(),
                "Every seed must remain stable to pass".into(),
                "Inertial host sold as gravitational three-body behavior".into(),
            ],
            do_not_force: "Stability is one class, not a universal pass. This slice reports an encounter diagnostic only.".into(),
            allowed_classes: vec![
                "hierarchical_bound".into(),
                "partner_exchange".into(),
                "ejection".into(),
                "chaotic_close_pass".into(),
            ],
            support: CardSupport::GemSlice,
            support_note: "partial (encounter only) on the implemented weak-field loop".into(),
            host_law_id: GEM_LAW_ID.into(),
        },
        CardId::GalaxyLikePopulation => CardView {
            id,
            title: id.title().into(),
            glance: "The crowd shears together; mass, not sprites, moves it.".into(),
            look_for: "Not claimed on this slice.".into(),
            looks_wrong: vec![
                "Family of extra masses sold as a galaxy".into(),
                "Decorative test particles as collective gravity".into(),
                "Inertial overlay labelled as this GEM law".into(),
                "A reduced scene sold as cosmological formation".into(),
            ],
            do_not_force: "Aggregate backreaction of a few extra masses is not a galaxy.".into(),
            allowed_classes: vec![
                "sheared_disk".into(),
                "clumpy_collection".into(),
                "triaxial_blob".into(),
                "perturber_response".into(),
            ],
            support: CardSupport::Unsupported,
            support_note: "unsupported: not a galaxy-like self-gravitating population".into(),
            host_law_id: GEM_LAW_ID.into(),
        },
        CardId::BlackHoleNearMass => CardView {
            id,
            title: id.title().into(),
            glance: "Closer pass: more bend, more delay; too close, no return; clocks agree with that story.".into(),
            look_for: "Not claimed on this slice.".into(),
            looks_wrong: vec![
                "Grafting Schwarzschild oracles onto this id".into(),
                "Compact / photon-sphere inside ‖Φ‖/c² < 0.05".into(),
                "Inertial overlay labelled as this GEM law".into(),
                "Bend, delay and clocks disagree".into(),
            ],
            do_not_force: "Compact remnants stay outside the admitted weak-field band.".into(),
            allowed_classes: vec![
                "weak_flyby".into(),
                "strong_bending_delay".into(),
                "absorbing_capture".into(),
                "near_mass_clock".into(),
            ],
            support: CardSupport::Unsupported,
            support_note: "unsupported: compact / photon-sphere remain outside ‖Φ‖/c² < 0.05".into(),
            host_law_id: GEM_LAW_ID.into(),
        },
        CardId::FleetAsteroidCausal => CardView {
            id,
            title: id.title().into(),
            glance: "Many specks matter together; news arrives at different times; later motion feels the change.".into(),
            look_for: "Accounted kick at A changes B only after the cone, then A; recoupled three-body compile-once/reuse/repair of certified interval functions vs independent same-IC; extra-ray is not equivalent completed source histories. Independent enclosure: failed q≥1 rejects the certificate, not the solution.".into(),
            looks_wrong: vec![
                "Remote bodies react before possible influence".into(),
                "Visibility flags as feedback".into(),
                "Hardcoded f=1 or authored worldtubes as the loop".into(),
                "Inertial overlay labelled as this GEM law".into(),
            ],
            do_not_force: "Cumulative effect may be tiny — if magnified, label it. Extra-ray reuse ~0.19 is not 99.9%.".into(),
            allowed_classes: vec![
                "collective_nudge".into(),
                "slow_backreaction".into(),
                "staggered_arrival".into(),
                "capture_keeps_history".into(),
            ],
            support: CardSupport::GemSlice,
            support_note: "partial on the implemented A→B→A loop plus laboratory enclosure".into(),
            host_law_id: GEM_LAW_ID.into(),
        },
    }
}

fn source_ops(compiled: &SourceResponse) -> u64 {
    compiled.charge.source_evolution + compiled.charge.retarded_solves
}

fn extra_ray_consumers(compiled: &SourceResponse, n: u64) -> Result<u64, String> {
    let mut rec = Charge::default();
    let sources = compiled
        .decode_sources(&mut rec)
        .map_err(|e| format!("{e:?}"))?;
    let mut charge = Charge::default();
    for k in 0..n {
        let y = 2.5 + 0.04 * k as f64;
        fly_ray(
            &sources,
            1.1,
            [0.0, y],
            [1.0, 0.0],
            8.0,
            0.05,
            &mut charge,
        )
        .map_err(|e| format!("{e:?}"))?;
    }
    Ok(charge.consumers)
}

fn chart_cells(compiled: &SourceResponse) -> Result<Vec<OverlayCell>, String> {
    let t = compiled.domain.horizon;
    let mut rec = Charge::default();
    let sources = compiled
        .decode_sources(&mut rec)
        .map_err(|e| format!("{e:?}"))?;
    let (a, _) = body_state(&sources, 0, t).map_err(|e| format!("{e:?}"))?;
    let (b, _) = body_state(&sources, 1, t).map_err(|e| format!("{e:?}"))?;
    Ok(vec![
        OverlayCell {
            identity: "A".into(),
            kind: WorkOverlayKind::Reuse,
            chart_position: a,
        },
        OverlayCell {
            identity: "compile".into(),
            kind: WorkOverlayKind::NewlyCompiled,
            chart_position: a,
        },
        OverlayCell {
            identity: "enclosure".into(),
            kind: WorkOverlayKind::Refinement,
            chart_position: b,
        },
        OverlayCell {
            identity: "B".into(),
            kind: WorkOverlayKind::RepairedPrediction,
            chart_position: b,
        },
    ])
}

fn required_queries_or_fail(compiled: &SourceResponse, horizon: f64) -> Result<u64, String> {
    let mut charge = Charge::default();
    let (ship, ray, clock, contact) =
        complete_required_queries_compiled(compiled, horizon, &mut charge)
            .map_err(|e| format!("{e:?}"))?;
    if !ship || !ray || !clock || !contact {
        return Err(
            "required ship/ray/clock/contact did not return values on this GEM slice".into(),
        );
    }
    Ok(charge.consumers)
}

fn overlay_kind_work(
    compiled: &SourceResponse,
    ic: emergent_law_lab::coupled_source_response::InitialCondition,
    kicks: Vec<Intervention>,
    kind: WorkOverlayKind,
    horizon: f64,
    dt: f64,
) -> Result<(u64, Option<bool>, Option<f64>, Option<String>), String> {
    let mut enclosure_certified = None;
    let mut enclosure_q = None;
    let mut enclosure_method = None;
    let consumer_ops = match kind {
        WorkOverlayKind::Reuse => extra_ray_consumers(compiled, 8)?,
        WorkOverlayKind::NewlyCompiled => {
            let _again =
                compile_source_response(ic, kicks, horizon, dt).map_err(|e| format!("{e:?}"))?;
            extra_ray_consumers(compiled, 1)?
        }
        WorkOverlayKind::Refinement => {
            let enc = enclose_compiled_interval(compiled, ic, kicks, IntervalMethod::IntegralOperator)
                .map_err(|e| format!("{e:?}"))?;
            enclosure_certified = Some(enc.certified);
            enclosure_q = Some(enc.q);
            enclosure_method = Some(format!("{:?}", enc.method));
            extra_ray_consumers(compiled, 1)?
        }
        WorkOverlayKind::RepairedPrediction => {
            let late = [Intervention {
                t: (horizon * 0.625).min(horizon),
                body_id: 0,
                delta_v: [0.0, 0.02],
            }];
            let _repaired = repair_from_committed(compiled, &late, horizon, dt)
                .map_err(|e| format!("{e:?}"))?;
            extra_ray_consumers(compiled, 1)?
        }
    };
    Ok((
        consumer_ops,
        enclosure_certified,
        enclosure_q,
        enclosure_method,
    ))
}

fn genesis_ids(compiled: &SourceResponse) -> Vec<u64> {
    compiled.genesis.bodies.iter().map(|b| b.id).collect()
}

fn finish_sample(
    kind: WorkOverlayKind,
    compiled: &SourceResponse,
    before: u64,
    consumer_ops: u64,
    required_query_consumers: u64,
    overlay_api: &'static str,
    enclosure_certified: Option<bool>,
    enclosure_q: Option<f64>,
    enclosure_method: Option<String>,
    cells: Vec<OverlayCell>,
) -> GemWorkSample {
    let after = source_ops(compiled);
    GemWorkSample {
        kind,
        charged: true,
        mutates_world: false,
        law_id: GEM_LAW_ID.into(),
        host_label: HOST_LABEL.into(),
        source_ops_before: before,
        source_ops_after: after,
        consumer_ops,
        required_query_consumers,
        required_queries_compiled: required_query_consumers > 0,
        overlay_api: overlay_api.into(),
        genesis_body_ids: genesis_ids(compiled),
        enclosure_certified,
        enclosure_q,
        enclosure_method,
        production_law: None,
        cells,
    }
}

fn sample_fast_ships_overlay(kind: WorkOverlayKind) -> Result<GemWorkSample, String> {
    let ic = laboratory_two_body();
    let kicks = laboratory_kick();
    let horizon = 4.0;
    let dt = 1.0 / 32.0;
    let compiled = compile_source_response(ic.clone(), kicks.clone(), horizon, dt)
        .map_err(|e| format!("{e:?}"))?;
    let before = source_ops(&compiled);
    let held_out = required_queries_or_fail(&compiled, horizon)?;
    let (mut consumer_ops, enclosure_certified, enclosure_q, enclosure_method) =
        overlay_kind_work(&compiled, ic, kicks, kind, horizon, dt)?;
    consumer_ops = consumer_ops.saturating_add(held_out);
    Ok(finish_sample(
        kind,
        &compiled,
        before,
        consumer_ops,
        held_out,
        "complete_required_queries_compiled",
        enclosure_certified,
        enclosure_q,
        enclosure_method,
        chart_cells(&compiled)?,
    ))
}

fn recoupled_chart_cells(compiled: &SourceResponse) -> Result<Vec<OverlayCell>, String> {
    let t = compiled.domain.horizon;
    let mut rec = Charge::default();
    let sources = compiled
        .decode_sources(&mut rec)
        .map_err(|e| format!("{e:?}"))?;
    if compiled.genesis.bodies.len() != 3 {
        return Err("three-body overlay must be the recoupled slice, not two-body paint".into());
    }
    let (a, _) = body_state(&sources, 0, t).map_err(|e| format!("{e:?}"))?;
    let (b, _) = body_state(&sources, 1, t).map_err(|e| format!("{e:?}"))?;
    let (c, _) = body_state(&sources, 99, t).map_err(|e| format!("{e:?}"))?;
    Ok(vec![
        OverlayCell {
            identity: "A".into(),
            kind: WorkOverlayKind::Reuse,
            chart_position: a,
        },
        OverlayCell {
            identity: "B".into(),
            kind: WorkOverlayKind::NewlyCompiled,
            chart_position: b,
        },
        OverlayCell {
            identity: "C".into(),
            kind: WorkOverlayKind::Refinement,
            chart_position: c,
        },
        OverlayCell {
            identity: "recouple".into(),
            kind: WorkOverlayKind::RepairedPrediction,
            chart_position: c,
        },
    ])
}

fn sample_three_body_overlay(kind: WorkOverlayKind) -> Result<GemWorkSample, String> {
    let horizon = 4.0;
    let dt = 1.0 / 32.0;
    let pair = compile_source_response(laboratory_two_body(), Vec::new(), horizon, dt)
        .map_err(|e| format!("{e:?}"))?;
    let (enc_ic, _) = laboratory_encounter();
    let entrant = enc_ic
        .bodies
        .iter()
        .find(|b| b.id == 99)
        .cloned()
        .ok_or_else(|| "encounter third mass".to_string())?;
    let recoupled = recouple_compiled_pair(&pair, &entrant, horizon, dt)
        .map_err(|e| format!("{e:?}"))?;
    if recoupled.genesis.bodies.len() != 3 || recoupled.pair_inverse.is_some() {
        return Err(
            "three-body overlay must be recouple_compiled_pair, not the two-body laboratory".into(),
        );
    }
    let before = source_ops(&recoupled);
    let held_out = required_queries_or_fail(&recoupled, horizon)?;
    let (mut consumer_ops, enclosure_certified, enclosure_q, enclosure_method) = overlay_kind_work(
        &recoupled,
        recoupled.genesis.clone(),
        recoupled.incoming.clone(),
        kind,
        horizon,
        dt,
    )?;
    consumer_ops = consumer_ops.saturating_add(held_out);
    Ok(finish_sample(
        kind,
        &recoupled,
        before,
        consumer_ops,
        held_out,
        "recouple_compiled_pair",
        enclosure_certified,
        enclosure_q,
        enclosure_method,
        recoupled_chart_cells(&recoupled)?,
    ))
}

fn sample_fleet_overlay(kind: WorkOverlayKind) -> Result<GemWorkSample, String> {
    let ic = laboratory_two_body();
    let kicks = laboratory_kick();
    let horizon = 4.0;
    let dt = 1.0 / 32.0;
    let compiled = compile_source_response(ic.clone(), kicks.clone(), horizon, dt)
        .map_err(|e| format!("{e:?}"))?;
    let before = source_ops(&compiled);
    let (consumer_ops, enclosure_certified, enclosure_q, enclosure_method) =
        overlay_kind_work(&compiled, ic, kicks, kind, horizon, dt)?;
    Ok(finish_sample(
        kind,
        &compiled,
        before,
        consumer_ops,
        0,
        "compile_source_response",
        enclosure_certified,
        enclosure_q,
        enclosure_method,
        chart_cells(&compiled)?,
    ))
}

/// Charged work overlay on this GEM slice. Fast-ships uses compiled
/// ship/ray/clock/contact. Three-bodies uses `recouple_compiled_pair`,
/// not two-body paint. Fleet stays the A→B→A kick overlay. Must not be
/// read as inertial-host gravity.
pub fn sample_gem_overlay(kind: WorkOverlayKind, card: CardId) -> Result<GemWorkSample, String> {
    match card {
        CardId::SolarSystemHierarchy
        | CardId::GalaxyLikePopulation
        | CardId::BlackHoleNearMass => Err(format!(
            "card {} is unsupported on this GEM slice; refusing to paint inertial motion as this law",
            card.as_str()
        )),
        CardId::FastShipsLightTwins => sample_fast_ships_overlay(kind),
        CardId::ThreeBodies => sample_three_body_overlay(kind),
        CardId::FleetAsteroidCausal => sample_fleet_overlay(kind),
    }
}

impl GemGalleryHost {
    pub fn mount() -> Result<Self, String> {
        let selected = CardId::FleetAsteroidCausal;
        let mut host = Self {
            cards: CardId::ALL.into_iter().map(card_view).collect(),
            selected,
            intended_class: "staggered_arrival".into(),
            seed: 0,
            seed_bank: "diagnostic".into(),
            comparison_class: "physical_law".into(),
            coupled_transition_id: None,
            work: None,
            bands_status: BANDS_STATUS.into(),
            playback_law_id: GEM_LAW_ID.into(),
            playback_cached: false,
            production_law: None,
            default_engine_law: INERTIAL_LAW_ID.into(),
        };
        host.work = Some(sample_gem_overlay(WorkOverlayKind::Reuse, selected)?);
        Ok(host)
    }

    pub fn select(&mut self, card: CardId) {
        self.selected = card;
        let view = self
            .cards
            .iter()
            .find(|c| c.id == card)
            .expect("catalog covers every CardId");
        self.intended_class = view.allowed_classes[0].clone();
        if view.support == CardSupport::Unsupported {
            self.work = None;
        }
    }

    pub fn selected_view(&self) -> &CardView {
        self.cards
            .iter()
            .find(|c| c.id == self.selected)
            .expect("selected card is in the catalog")
    }

    pub fn sample_work(&mut self, kind: WorkOverlayKind) -> Result<(), String> {
        if self.selected_view().support == CardSupport::Unsupported {
            return Err(format!(
                "card {} is unsupported on this GEM slice; refusing to paint inertial motion as this law",
                self.selected.as_str()
            ));
        }
        self.work = Some(sample_gem_overlay(kind, self.selected)?);
        Ok(())
    }

    pub fn set_coupled_exercise(&mut self, on: bool) {
        self.coupled_transition_id = on.then_some(COUPLED_TRANSITION_ID.into());
    }

    pub fn run_record(&self) -> serde_json::Value {
        let selected = self.selected_view();
        let work = self.work.as_ref().map(|sample| {
            serde_json::json!({
                "kind": sample.kind.as_str(),
                "charged": sample.charged,
                "mutates_world": sample.mutates_world,
                "law_id": sample.law_id,
                "host_label": sample.host_label,
                "source_ops_before": sample.source_ops_before,
                "source_ops_after": sample.source_ops_after,
                "source_ops_unchanged": sample.source_ops_unchanged(),
                "consumer_ops": sample.consumer_ops,
                "required_query_consumers": sample.required_query_consumers,
                "required_queries_compiled": sample.required_queries_compiled,
                "overlay_api": sample.overlay_api,
                "genesis_body_ids": sample.genesis_body_ids,
                "enclosure_certified": sample.enclosure_certified,
                "enclosure_q": sample.enclosure_q,
                "enclosure_method": sample.enclosure_method,
                "production_law": sample.production_law,
                "cells": sample.cells.iter().map(|cell| serde_json::json!({
                    "identity": cell.identity,
                    "kind": cell.kind.as_str()
                })).collect::<Vec<_>>()
            })
        });
        serde_json::json!({
            "card_id": selected.id.as_str(),
            "card_support": selected.support.as_str(),
            "support_note": selected.support_note,
            "look_for": selected.look_for,
            "coupled_transition_id": self.coupled_transition_id,
            "law_id": GEM_LAW_ID,
            "host_label": HOST_LABEL,
            "not_inertial_overlay_as_this_law": true,
            "default_engine_advance": self.default_engine_law,
            "rng_version": RNG_VERSION,
            "seed": self.seed.to_string(),
            "intended_outcome_class": self.intended_class,
            "seed_bank": self.seed_bank,
            "comparison_class": self.comparison_class,
            "numeric_bands": self.bands_status,
            "playback": {
                "cached": self.playback_cached,
                "law_id": self.playback_law_id,
                "label": if self.playback_cached {
                    format!(
                        "Cached playback · {} — not a fresh validation run",
                        self.playback_law_id
                    )
                } else {
                    String::new()
                }
            },
            "work_overlay_sample": work,
            "production_law": serde_json::Value::Null,
            "native_gui_compiled": false
        })
    }
}

/// Named close-pair enclosure used as a host cue: q≥1 refuses the
/// certificate while compile still succeeds. Not a KA proof.
pub fn close_pair_integral_operator_refuses_certificate() -> Result<(bool, f64, bool), String> {
    let ic = laboratory_close_pair();
    let compiled = compile_source_response(ic.clone(), Vec::new(), 1.0, 1.0 / 32.0)
        .map_err(|e| format!("{e:?}"))?;
    let enc = enclose_compiled_interval(&compiled, ic, Vec::new(), IntervalMethod::IntegralOperator)
        .map_err(|e| format!("{e:?}"))?;
    Ok((enc.certified, enc.q, true))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn frozen_catalog_has_six_cards_and_no_seventh_physics() {
        let host = GemGalleryHost::mount().expect("mount GEM gallery");
        assert_eq!(host.cards.len(), 6);
        let ids: Vec<_> = host.cards.iter().map(|c| c.id.as_str()).collect();
        assert_eq!(
            ids,
            vec![
                "fast-ships-light-twins",
                "solar-system-hierarchy",
                "three-bodies",
                "galaxy-like-population",
                "black-hole-near-mass",
                "fleet-asteroid-causal"
            ]
        );
        assert!(!CardId::ALL.iter().any(|c| c.as_str() == COUPLED_TRANSITION_ID));
        for card in &host.cards {
            assert!(!card.glance.is_empty());
            assert!(!card.look_for.is_empty());
            assert_eq!(card.looks_wrong.len(), 4);
            assert_eq!(card.allowed_classes.len(), 4);
        }
        let mut host = host;
        host.set_coupled_exercise(true);
        assert_eq!(host.cards.len(), 6, "coupled transition is not a seventh card");
        assert_eq!(
            host.coupled_transition_id.as_deref(),
            Some(COUPLED_TRANSITION_ID)
        );
    }

    #[test]
    fn solar_galaxy_black_hole_are_unsupported() {
        let host = GemGalleryHost::mount().unwrap();
        let unsupported: Vec<_> = host
            .cards
            .iter()
            .filter(|c| c.support == CardSupport::Unsupported)
            .map(|c| c.id)
            .collect();
        assert_eq!(
            unsupported,
            vec![
                CardId::SolarSystemHierarchy,
                CardId::GalaxyLikePopulation,
                CardId::BlackHoleNearMass
            ]
        );
        for card in &host.cards {
            if card.support == CardSupport::Unsupported {
                assert!(
                    card.support_note.contains("unsupported"),
                    "{}",
                    card.support_note
                );
            }
        }
    }

    #[test]
    fn gem_cards_show_look_for_and_are_not_inertial_relabelled() {
        let host = GemGalleryHost::mount().unwrap();
        for id in [
            CardId::FastShipsLightTwins,
            CardId::ThreeBodies,
            CardId::FleetAsteroidCausal,
        ] {
            let card = host.cards.iter().find(|c| c.id == id).unwrap();
            assert_eq!(card.support, CardSupport::GemSlice);
            assert_eq!(card.host_law_id, GEM_LAW_ID);
            assert_ne!(card.host_law_id, INERTIAL_LAW_ID);
            assert!(card.looks_wrong.iter().any(|w| w.contains("Inertial")));
        }
        assert_eq!(host.default_engine_law, INERTIAL_LAW_ID);
        assert!(host.production_law.is_none());
        assert_eq!(host.playback_law_id, GEM_LAW_ID);
        assert!(!host.playback_cached);
    }

    #[test]
    fn charged_reuse_overlay_does_not_re_evolve_sources() {
        let host = GemGalleryHost::mount().unwrap();
        let work = host.work.as_ref().expect("gallery opens with a charged sample");
        assert!(work.charged);
        assert!(!work.mutates_world);
        assert_eq!(work.law_id, GEM_LAW_ID);
        assert_eq!(work.host_label, HOST_LABEL);
        assert_ne!(work.host_label, "inertial-host");
        assert!(work.source_ops_unchanged());
        assert!(work.consumer_ops > 0);
        assert!(work.production_law.is_none());
        assert_eq!(work.cells.len(), 4);
        let kinds: Vec<_> = work.cells.iter().map(|c| c.kind.as_str()).collect();
        assert_eq!(
            kinds,
            vec![
                "reuse",
                "newly_compiled",
                "refinement",
                "repaired_prediction"
            ]
        );
    }

    #[test]
    fn unsupported_cards_refuse_inertial_paint_as_this_law() {
        let mut host = GemGalleryHost::mount().unwrap();
        for card in [
            CardId::SolarSystemHierarchy,
            CardId::GalaxyLikePopulation,
            CardId::BlackHoleNearMass,
        ] {
            host.select(card);
            assert_eq!(host.selected_view().support, CardSupport::Unsupported);
            assert!(
                host.work.is_none(),
                "{} must not keep a painted overlay",
                card.as_str()
            );
            let err = host
                .sample_work(WorkOverlayKind::Reuse)
                .expect_err("must not paint inertial as GEM");
            assert!(err.contains("unsupported"), "{err}");
            assert!(err.contains("inertial"), "{err}");
        }
    }

    #[test]
    fn overlay_kinds_match_the_gallery_contract() {
        let kinds: Vec<_> = WorkOverlayKind::ALL.iter().map(|k| k.as_str()).collect();
        assert_eq!(
            kinds,
            vec![
                "reuse",
                "newly_compiled",
                "refinement",
                "repaired_prediction"
            ]
        );
    }

    #[test]
    fn refinement_overlay_records_independent_enclosure_not_ka() {
        let mut host = GemGalleryHost::mount().unwrap();
        host.select(CardId::FleetAsteroidCausal);
        host.sample_work(WorkOverlayKind::Refinement).unwrap();
        let work = host.work.as_ref().unwrap();
        assert_eq!(work.kind, WorkOverlayKind::Refinement);
        assert_eq!(work.enclosure_method.as_deref(), Some("IntegralOperator"));
        let q = work.enclosure_q.expect("q recorded");
        assert!(q.is_finite() && q >= 0.0);
        let certified = work.enclosure_certified.expect("verdict recorded");
        if certified {
            assert!(q < 1.0);
        }
        let (close_certified, close_q, compile_ok) =
            close_pair_integral_operator_refuses_certificate().unwrap();
        assert!(compile_ok);
        assert!(!close_certified);
        assert!(close_q >= 1.0);
    }

    #[test]
    fn fast_ships_overlay_returns_compiled_ship_ray_clock() {
        let mut host = GemGalleryHost::mount().unwrap();
        host.select(CardId::FastShipsLightTwins);
        host.sample_work(WorkOverlayKind::Reuse).unwrap();
        let work = host.work.as_ref().unwrap();
        assert_eq!(work.law_id, GEM_LAW_ID);
        assert_eq!(work.law_id, "es-linearized-retarded-gem-response-v0");
        assert_ne!(work.law_id, INERTIAL_LAW_ID);
        assert_eq!(work.overlay_api, "complete_required_queries_compiled");
        assert!(
            work.required_queries_compiled && work.required_query_consumers > 0,
            "fast-ships must run complete_required_queries_compiled; extra-ray-only would leave required_query_consumers=0"
        );
        assert!(
            work.consumer_ops >= work.required_query_consumers,
            "compiled query consumers must be in the overlay charge"
        );
        assert!(work.source_ops_unchanged());
        assert_eq!(host.selected_view().support, CardSupport::GemSlice);
        let ids: Vec<_> = work.cells.iter().map(|c| c.identity.as_str()).collect();
        assert_ne!(ids, vec!["A", "B", "C", "recouple"]);
    }

    #[test]
    fn three_bodies_overlay_is_recoupled_slice_not_two_body() {
        let mut host = GemGalleryHost::mount().unwrap();
        host.select(CardId::ThreeBodies);
        host.sample_work(WorkOverlayKind::Reuse).unwrap();
        let work = host.work.as_ref().unwrap();
        assert_eq!(work.law_id, GEM_LAW_ID);
        assert_eq!(work.law_id, "es-linearized-retarded-gem-response-v0");
        assert_ne!(work.host_label, "inertial-host");
        assert_eq!(work.overlay_api, "recouple_compiled_pair");
        assert_eq!(work.genesis_body_ids, vec![0, 1, 99]);
        let ids: Vec<_> = work.cells.iter().map(|c| c.identity.as_str()).collect();
        assert_eq!(ids, vec!["A", "B", "C", "recouple"]);
        assert!(
            work.required_queries_compiled && work.required_query_consumers > 0,
            "three-bodies recouple overlay must still complete compiled ship/ray/clock/contact"
        );
        assert!(work.source_ops_unchanged());
        assert!(work.production_law.is_none());
    }

    #[test]
    fn run_record_keeps_production_law_null_and_engine_inertial() {
        let host = GemGalleryHost::mount().unwrap();
        let record = host.run_record();
        assert!(record["production_law"].is_null());
        assert_eq!(record["default_engine_advance"], INERTIAL_LAW_ID);
        assert_eq!(record["law_id"], GEM_LAW_ID);
        assert_eq!(record["not_inertial_overlay_as_this_law"], true);
        assert_eq!(record["native_gui_compiled"], false);
        assert_eq!(record["numeric_bands"], BANDS_STATUS);
        if let Ok(dir) = std::env::var("COUPLED_GALLERY_ARTIFACTS") {
            std::fs::create_dir_all(&dir).unwrap();
            std::fs::write(
                std::path::Path::new(&dir).join("gallery-run.json"),
                serde_json::to_string_pretty(&record).unwrap(),
            )
            .unwrap();
        }
    }
}
