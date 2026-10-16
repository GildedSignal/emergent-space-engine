//! Isolated self-consistent retarded two-way backreaction.
//!
//! Law id: `es-causal-retarded-coupled-v0`. Continuation of the
//! `es-causal-retarded-monopole-v0` research track, not a production gravity
//! law, not FMM, not GR, and not delayed-Newton-as-G2. It is never
//! `es-inertial-causal-v1` and must not be wired into the canonical engine.
//!
//! # Candidate contract
//!
//! **State.** Tiny N (2..=64) massive bodies. Each is a source. History is a
//! growing piecewise-constant worldtube. There is no `is_planet` flag: a body
//! sources iff μ>0. Approximate state is a symplectic-Euler step of f64
//! retarded accelerations with dyadic position projection so cone tests stay
//! exact rationals.
//!
//! **Next segment.** Body i's next segment is computed from the excluded-self
//! retarded 3D-planar monopole of *already committed* history. Accelerations
//! for a tick are evaluated before any body in that tick commits. Authored
//! futures are not a valid next segment.
//!
//! **Causality.** Gravity changes propagate at c. A source-μ change at B has
//! zero influence on A's *trajectory* inside B's future cone, and nonzero
//! influence after. Instantaneous present-state two-body maps fail the pre-cone
//! side. Prescribed worldtubes fail the post-cone side.
//!
//! **Exterior.** The parent kernel's certified query contract applies:
//! incomplete omit of far mass fails closed; a sound omitted-tail bound must
//! enclose the frozen r=16 unit source at r=1. The tiny-N Euler stepper still
//! advances on listed retarded accelerations and does not integrate the
//! remainder.
//!
//! **Not claimed.** Orbits, clocks, FMM, compact-field certification
//! (absorbing capture is not Schwarzschild), a curved-null geodesic branch
//! solver, or instantaneous Newton third-law balance on retarded fields.
//! Kernel-supported predicates terminate or fail closed; the production
//! `terminating_exact_branches` gate stays failed. `production_law` stays null.

use super::causal_kernel::{
    authored_trajectory_two_sided, exterior_coupled_kernel, exterior_manifest, finite_root,
    genesis, influence, mass_change_influence, origin, q, qf, qf_pair, r4,
    record_well_posed_exterior, tube, two_sided_result, CausalKernel, CompactClass, FieldAt,
    KernelError, KernelEvent, SourceSegment, SourceWorldtube, TwoSidedResult, C,
    INERTIAL_LAB_LAW_ID, POST_LIGHTCONE_INFLUENCE_MIN, RESEARCH_LAW_ID,
};
use super::{gate, gravitational_acceleration, CandidateReport, Metric};
use num_rational::Ratio;
use num_traits::Zero;
use serde::Deserialize;
use std::fmt::Write as _;

pub const COUPLED_LAW_ID: &str = "es-causal-retarded-coupled-v0";
pub(crate) const MAX_BODIES: usize = 64;
pub(crate) const POSITION_DENOM: i128 = 1 << 20;

const MANIFEST: &str = include_str!("../../../scenarios/law-gates.json");

type Q = super::causal_kernel::Q;

#[derive(Clone, Deserialize)]
struct ManifestSlice {
    aggregate_gates: FrozenAggregates,
    required_production_gates: Vec<String>,
    causal_kernel_research: KernelFixtures,
    retarded_backreaction_research: CoupledManifest,
}

#[derive(Clone, Deserialize)]
struct FrozenAggregates {
    pre_lightcone_response_max: f64,
}

#[derive(Clone, Deserialize)]
struct KernelFixtures {
    fixtures: Vec<NamedFixture>,
}

#[derive(Clone, Deserialize)]
struct CoupledManifest {
    law_id: String,
    parent_kernel: String,
    gate: String,
    light_speed: i128,
    pre_lightcone_response_max: f64,
    post_lightcone_influence_min: f64,
    post_lightcone_influence_strict: bool,
    max_bodies: usize,
    step: [i128; 2],
    position_denom: i128,
    fixtures: Vec<NamedFixture>,
}

#[derive(Clone, Deserialize)]
struct NamedFixture {
    id: String,
}

pub fn coupled_manifest() -> Result<(), String> {
    let slice: ManifestSlice = serde_json::from_str(MANIFEST).map_err(|e| e.to_string())?;
    if slice.retarded_backreaction_research.law_id != COUPLED_LAW_ID {
        return Err("coupled law id drifted".into());
    }
    if slice.retarded_backreaction_research.law_id == INERTIAL_LAB_LAW_ID
        || slice.retarded_backreaction_research.law_id == RESEARCH_LAW_ID
    {
        return Err("coupled kernel must keep a distinct research id".into());
    }
    if slice.retarded_backreaction_research.parent_kernel != RESEARCH_LAW_ID {
        return Err("coupled kernel must continue the retarded monopole track".into());
    }
    if slice.retarded_backreaction_research.gate != "retarded_two_way_backreaction" {
        return Err("coupled first coupling gate must remain retarded_two_way_backreaction".into());
    }
    if slice.aggregate_gates.pre_lightcone_response_max != 0.0
        || slice
            .retarded_backreaction_research
            .pre_lightcone_response_max
            != 0.0
        || slice
            .retarded_backreaction_research
            .post_lightcone_influence_min
            != POST_LIGHTCONE_INFLUENCE_MIN
        || !slice
            .retarded_backreaction_research
            .post_lightcone_influence_strict
        || slice.retarded_backreaction_research.light_speed != C
        || slice.retarded_backreaction_research.max_bodies != MAX_BODIES
        || slice.retarded_backreaction_research.step != [1, C]
        || slice.retarded_backreaction_research.position_denom != POSITION_DENOM
    {
        return Err("coupled-research thresholds were weakened or retuned".into());
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
    let kernel_ids: Vec<&str> = slice
        .causal_kernel_research
        .fixtures
        .iter()
        .map(|f| f.id.as_str())
        .collect();
    let kernel_expected = [
        "mass_change_r4",
        "compact_vs_far",
        "huge_mass_ratio",
        "moving_source",
        "exterior_source_r16",
        "simultaneous_source_changes",
    ];
    if kernel_ids != kernel_expected {
        return Err("causal-kernel fixtures were renamed, dropped or reordered".into());
    }
    exterior_manifest()?;
    if exterior_coupled_kernel()? != COUPLED_LAW_ID {
        return Err("finite-exterior coupled kernel id drifted".into());
    }
    crate::compact::compact_manifest()?;
    crate::exact_branch::exact_branch_manifest()?;
    let ids: Vec<&str> = slice
        .retarded_backreaction_research
        .fixtures
        .iter()
        .map(|f| f.id.as_str())
        .collect();
    let expected = [
        "authored_worldtube_no_coupling",
        "instantaneous_two_body_precone",
        "coupled_mass_change_r4",
        "every_mass_sources",
        "mutual_two_way",
        "fleet_collective_n64",
    ];
    if ids != expected {
        return Err("coupled fixtures were renamed, dropped or reordered".into());
    }
    Ok(())
}

fn dt_q() -> Q {
    q(1, C)
}

fn dt_f() -> f64 {
    1.0 / C as f64
}

fn round_q(x: f64) -> Result<Q, KernelError> {
    if !x.is_finite() {
        return Err(KernelError::Invalid("nonfinite coupled position"));
    }
    Ok(Ratio::new(
        (x * POSITION_DENOM as f64).round() as i128,
        POSITION_DENOM,
    ))
}

/// Tiny-N retarded coupled stepper. Next worldtube segment = finite-map
/// update from the excluded-self retarded field of committed history.
pub struct CoupledSystem {
    pub kernel: CausalKernel,
    momenta: Vec<[f64; 2]>,
    pub time: Q,
    last_predicted: Vec<[Q; 2]>,
    captured: Vec<Option<(u64, CompactClass)>>,
}

impl CoupledSystem {
    pub fn at_rest(bodies: Vec<(u64, [Q; 2], Q)>) -> Result<Self, KernelError> {
        if bodies.is_empty() {
            return Err(KernelError::Invalid("coupled system has no bodies"));
        }
        if bodies.len() > MAX_BODIES {
            return Err(KernelError::Invalid(
                "coupled system exceeds tiny-N laboratory bound",
            ));
        }
        let mut seen = Vec::new();
        for (id, _, _) in &bodies {
            if seen.contains(id) {
                return Err(KernelError::Invalid("duplicate coupled body id"));
            }
            seen.push(*id);
        }
        let sources: Vec<SourceWorldtube> = bodies
            .iter()
            .map(|&(id, position, mu)| tube(id, vec![genesis(position, mu)]))
            .collect();
        Ok(Self {
            kernel: CausalKernel::new(sources, finite_root())?,
            momenta: vec![[0.0, 0.0]; bodies.len()],
            time: Q::zero(),
            last_predicted: bodies.iter().map(|&(_, position, _)| position).collect(),
            captured: vec![None; bodies.len()],
        })
    }

    pub fn insert_body(&mut self, id: u64, position: [Q; 2], mu: Q) -> Result<(), KernelError> {
        if self.kernel.sources.len() >= MAX_BODIES {
            return Err(KernelError::Invalid(
                "coupled system exceeds tiny-N laboratory bound",
            ));
        }
        if self.kernel.sources.iter().any(|source| source.id == id) {
            return Err(KernelError::Invalid("duplicate coupled body id"));
        }
        let mut sources = self.kernel.sources.clone();
        sources.push(tube(
            id,
            vec![SourceSegment {
                since: self.time,
                position,
                mu,
            }],
        ));
        self.kernel = CausalKernel::new(sources, self.kernel.exterior.clone())?;
        self.momenta.push([0.0, 0.0]);
        self.last_predicted.push(position);
        self.captured.push(None);
        Ok(())
    }

    pub fn set_mu(&mut self, id: u64, mu: Q) -> Result<(), KernelError> {
        let mut sources = self.kernel.sources.clone();
        let source = sources
            .iter_mut()
            .find(|source| source.id == id)
            .ok_or(KernelError::Invalid("unknown coupled body id"))?;
        let last = *source
            .segments
            .last()
            .ok_or(KernelError::Invalid("source worldtube has no segments"))?;
        if last.since == self.time {
            source.segments.last_mut().expect("last segment").mu = mu;
        } else {
            source.segments.push(SourceSegment {
                since: self.time,
                position: last.position,
                mu,
            });
        }
        self.kernel = CausalKernel::new(sources, self.kernel.exterior.clone())?;
        Ok(())
    }

    pub fn position(&self, id: u64) -> Result<[Q; 2], KernelError> {
        self.kernel
            .source_position_at(id, self.time)
            .ok_or(KernelError::Invalid("unknown coupled body id"))
    }

    pub fn captured_by(&self, id: u64) -> Option<(u64, CompactClass)> {
        let index = self
            .kernel
            .sources
            .iter()
            .position(|source| source.id == id)?;
        self.captured[index]
    }

    /// One tick: evaluate every retarded field on committed history, then
    /// commit every next segment. A body at or inside another visible source's
    /// compact radius is absorbed (finite capture), not Newton-stepped through
    /// r=0. Same-tick bodies cannot see each other's update.
    pub fn step(&mut self) -> Result<(), KernelError> {
        let dt = dt_f();
        let next_time = self.time + dt_q();
        let mut sources = self.kernel.sources.clone();
        let mut predicted = Vec::with_capacity(sources.len());
        let mut next_captured = self.captured.clone();
        let mut next_momenta = self.momenta.clone();
        for (i, source) in sources.iter_mut().enumerate() {
            let last = *source
                .segments
                .last()
                .ok_or(KernelError::Invalid("source worldtube has no segments"))?;
            if next_captured[i].is_some() {
                source.segments.push(SourceSegment {
                    since: next_time,
                    position: last.position,
                    mu: last.mu,
                });
                next_momenta[i] = [0.0, 0.0];
                predicted.push(last.position);
                continue;
            }
            let event = KernelEvent {
                time: self.time,
                position: last.position,
            };
            match self.kernel.field_at_excluding(event, Some(source.id))? {
                FieldAt::Captured { id, class } => {
                    source.segments.push(SourceSegment {
                        since: next_time,
                        position: last.position,
                        mu: last.mu,
                    });
                    next_momenta[i] = [0.0, 0.0];
                    next_captured[i] = Some((id, class));
                    predicted.push(last.position);
                }
                FieldAt::Acceleration(accel) => {
                    let momentum = [
                        self.momenta[i][0] + accel[0] * dt,
                        self.momenta[i][1] + accel[1] * dt,
                    ];
                    if !momentum[0].is_finite() || !momentum[1].is_finite() {
                        return Err(KernelError::Invalid("nonfinite coupled momentum"));
                    }
                    if momentum[0].hypot(momentum[1]) >= C as f64 {
                        return Err(KernelError::SuperluminalHistory { id: source.id });
                    }
                    let xf = [
                        qf(last.position[0]) + momentum[0] * dt,
                        qf(last.position[1]) + momentum[1] * dt,
                    ];
                    let position = [round_q(xf[0])?, round_q(xf[1])?];
                    source.segments.push(SourceSegment {
                        since: next_time,
                        position,
                        mu: last.mu,
                    });
                    next_momenta[i] = momentum;
                    predicted.push(position);
                }
            }
        }
        self.kernel = CausalKernel::new(sources, self.kernel.exterior.clone())?;
        self.time = next_time;
        self.last_predicted = predicted;
        self.momenta = next_momenta;
        self.captured = next_captured;
        self.check_commit_matches_prediction()?;
        Ok(())
    }

    fn check_commit_matches_prediction(&self) -> Result<(), KernelError> {
        for (source, predicted) in self.kernel.sources.iter().zip(&self.last_predicted) {
            let last = source
                .segments
                .last()
                .ok_or(KernelError::Invalid("source worldtube has no segments"))?;
            if last.position != *predicted {
                return Err(KernelError::Invalid(
                    "committed segment was not the retarded finite-map update",
                ));
            }
        }
        Ok(())
    }

    pub fn advance_to(&mut self, time: Q) -> Result<(), KernelError> {
        if time < self.time {
            return Err(KernelError::Invalid("coupled system cannot step backward"));
        }
        while self.time < time {
            self.step()?;
        }
        Ok(())
    }
}

fn pair_at_rest(mu_a: Q, mu_b: Q) -> Result<CoupledSystem, KernelError> {
    CoupledSystem::at_rest(vec![(1, origin(), mu_a), (2, r4(), mu_b)])
}

fn trajectory_influence(
    changed: &CoupledSystem,
    baseline: &CoupledSystem,
    id: u64,
) -> Result<f64, KernelError> {
    Ok(influence(
        qf_pair(changed.position(id)?),
        qf_pair(baseline.position(id)?),
    ))
}

pub fn instantaneous_two_body_two_sided() -> TwoSidedResult {
    let dt = dt_f();
    let step = |mu_b: f64| -> [f64; 2] {
        let accel = gravitational_acceleration([-4.0, 0.0], mu_b).expect("nonsingular two-body");
        let momentum = [accel[0] * dt, accel[1] * dt];
        [momentum[0] * dt, momentum[1] * dt]
    };
    let delta = influence(step(2.0), step(1.0));
    two_sided_result(delta, delta, 0.0, POST_LIGHTCONE_INFLUENCE_MIN)
}

fn coupled_mass_change_two_sided() -> Result<TwoSidedResult, KernelError> {
    let mut pre_base = pair_at_rest(q(1, 1), q(1, 1))?;
    let mut pre_changed = pair_at_rest(q(1, 1), q(1, 1))?;
    pre_changed.set_mu(2, q(2, 1))?;
    pre_base.advance_to(q(1, 64))?;
    pre_changed.advance_to(q(1, 64))?;
    let pre = trajectory_influence(&pre_changed, &pre_base, 1)?;
    let mut post_base = pair_at_rest(q(1, 1), q(1, 1))?;
    let mut post_changed = pair_at_rest(q(1, 1), q(1, 1))?;
    post_changed.set_mu(2, q(2, 1))?;
    post_base.advance_to(q(1, 8))?;
    post_changed.advance_to(q(1, 8))?;
    let post = trajectory_influence(&post_changed, &post_base, 1)?;
    Ok(two_sided_result(
        pre,
        post,
        0.0,
        POST_LIGHTCONE_INFLUENCE_MIN,
    ))
}

fn every_mass_sources_passed() -> Result<bool, KernelError> {
    let mut sourced = pair_at_rest(q(1, 1), q(1, 64))?;
    let mut vacuum = pair_at_rest(q(1, 1), Q::zero())?;
    sourced.advance_to(q(1, 2))?;
    vacuum.advance_to(q(1, 2))?;
    let moved = sourced.position(1)? != origin();
    let unmoved = vacuum.position(1)? == origin();
    Ok(moved && unmoved)
}

fn mutual_two_way_passed() -> Result<bool, KernelError> {
    let mut sys = pair_at_rest(q(1, 1), q(1, 1))?;
    sys.advance_to(q(1, 8))?;
    Ok(sys.position(1)? != origin() && sys.position(2)? != r4())
}

fn no_self_force_passed() -> Result<bool, KernelError> {
    let mut sys = CoupledSystem::at_rest(vec![(1, origin(), q(1, 1))])?;
    sys.advance_to(q(1, 8))?;
    Ok(sys.position(1)? == origin() && sys.momenta[0] == [0.0, 0.0])
}

fn coupled_capture_halt_passed() -> Result<bool, KernelError> {
    // μ_B is small enough that A's exterior Newton kick stays subluminal,
    // so the fixture measures B's capture rather than A's 1/r² blow-up.
    let start = [q(1, 4096), Q::zero()];
    let mut sys = CoupledSystem::at_rest(vec![(1, origin(), q(1, 1)), (2, start, q(1, 8192))])?;
    sys.step()?;
    Ok(sys.captured_by(2) == Some((1, CompactClass::Interior))
        && sys.captured_by(1).is_none()
        && sys.position(2)? == start
        && sys.momenta[1] == [0.0, 0.0]
        && sys.position(1).is_ok())
}

fn ship_cluster(n: usize) -> Vec<(u64, [Q; 2], Q)> {
    (0..n)
        .map(|i| {
            let y = q(i as i128, 16) - q(n as i128 - 1, 32);
            (i as u64 + 2, [q(4, 1), y], q(1, 64))
        })
        .collect()
}

fn fleet_star(n_ships: usize) -> Result<CoupledSystem, KernelError> {
    let mut sys = CoupledSystem::at_rest(vec![(1, origin(), q(1, 1))])?;
    for (id, position, mu) in ship_cluster(n_ships) {
        sys.insert_body(id, position, mu)?;
    }
    Ok(sys)
}

fn fleet_collective_two_sided() -> Result<(TwoSidedResult, bool), KernelError> {
    let mut one = fleet_star(1)?;
    let mut many = fleet_star(63)?;
    let mut one_pre = fleet_star(1)?;
    let mut many_pre = fleet_star(63)?;
    one_pre.advance_to(q(1, 64))?;
    many_pre.advance_to(q(1, 64))?;
    let pre = influence(
        qf_pair(many_pre.position(1)?),
        qf_pair(one_pre.position(1)?),
    );
    one.advance_to(q(1, 8))?;
    many.advance_to(q(1, 8))?;
    let post = influence(qf_pair(many.position(1)?), qf_pair(one.position(1)?));
    let two_sided = two_sided_result(pre, post, 0.0, POST_LIGHTCONE_INFLUENCE_MIN);
    let collective = qf_pair(many.position(1)?)[0].abs() > qf_pair(one.position(1)?)[0].abs();
    Ok((two_sided, collective && two_sided.passed))
}

fn push_metric(
    report: &mut CandidateReport,
    scenario: &str,
    name: &str,
    value: f64,
    unit: &str,
    threshold: f64,
    passed: bool,
) {
    report.metrics.push(Metric {
        scenario: scenario.into(),
        name: name.into(),
        value,
        unit: unit.into(),
        threshold,
        passed,
    });
}

fn fail_missing(report: &mut CandidateReport, id: &str, reason: &str) {
    gate(report, id, false, reason);
}

fn record_two_sided(
    report: &mut CandidateReport,
    scenario: &str,
    gate_id: &str,
    result: TwoSidedResult,
    reason: String,
) {
    push_metric(
        report,
        scenario,
        "pre_lightcone_response",
        result.pre_influence,
        "length",
        0.0,
        result.pre_passed,
    );
    push_metric(
        report,
        scenario,
        "post_lightcone_influence",
        result.post_influence,
        "length",
        POST_LIGHTCONE_INFLUENCE_MIN,
        result.post_passed,
    );
    gate(report, gate_id, result.passed, reason);
}

pub fn qualify_coupled_kernel() -> CandidateReport {
    let mut report = CandidateReport {
        id: COUPLED_LAW_ID.into(),
        version: 0,
        status: "FAIL".into(),
        metrics: Vec::new(),
        gates: Vec::new(),
        evidence: vec![
            "Research kernel es-causal-retarded-coupled-v0 is isolated from es-inertial-causal-v1.".into(),
            "Next source segment is the retarded excluded-self finite-map update of committed history; no authored future, no is_planet.".into(),
            "Tiny-N (≤64) 3D-planar retarded monopole stepper is not G2, GR, FMM, or delayed-Newton promotion.".into(),
            "Certified queries require a declared-complete finite root plus a sound omitted-tail enclosure, or fail closed. The Euler stepper still uses listed retarded accelerations.".into(),
            "Compact radius r_s=2μ/c² is exact. A coupled body at or inside another visible source's r_s is captured (finite halt), not Newton-stepped through r=0. That is not Schwarzschild certification.".into(),
            "Kernel predicates terminate in one rational comparison or fail closed. An iteration cap is a failed execution, not a guessed sign. Curved-null geodesic branches are unsupported; terminating_exact_branches stays failed.".into(),
            format!(
                "Default coupled exterior is {:?}; certified remainder uses declared_complete with an omitted-tail bound.",
                finite_root()
            ),
        ],
    };

    match coupled_manifest() {
        Ok(()) => gate(
            &mut report,
            "coupled_manifest_isolated",
            true,
            "New coupled fixtures did not edit frozen production-gate identities, old kernel fixtures, or numeric thresholds.",
        ),
        Err(error) => gate(&mut report, "coupled_manifest_isolated", false, error),
    }

    let field_pre = mass_change_influence(origin(), r4(), q(1, 1), q(2, 1), q(1, 64));
    let field_post = mass_change_influence(origin(), r4(), q(1, 1), q(2, 1), q(1, 8));
    let field_two_sided = match (field_pre, field_post) {
        (Ok(pre_influence), Ok(post_influence)) => two_sided_result(
            pre_influence,
            post_influence,
            0.0,
            POST_LIGHTCONE_INFLUENCE_MIN,
        ),
        (Err(error), _) | (_, Err(error)) => {
            gate(
                &mut report,
                "source_change_light_cone_execution",
                false,
                error.to_string(),
            );
            TwoSidedResult {
                passed: false,
                pre_passed: false,
                post_passed: false,
                pre_influence: f64::NAN,
                post_influence: f64::NAN,
            }
        }
    };
    record_two_sided(
        &mut report,
        "mass_change_r4",
        "source_change_light_cone",
        field_two_sided,
        format!(
            "Shared retarded field evaluator. Source μ 1→2 at t=0, query r=4. Pre t=1/64 influence {:.12e}; post t=1/8 influence {:.12e}.",
            field_two_sided.pre_influence, field_two_sided.post_influence
        ),
    );
    gate(
        &mut report,
        "causal_dynamic_sources",
        field_two_sided.passed,
        "Same two-sided retarded-source field measurement as the parent kernel. Passing it is not production gravity.",
    );

    match authored_trajectory_two_sided() {
        Ok(result) => record_two_sided(
            &mut report,
            "authored_worldtube_no_coupling",
            "authored_worldtube_is_not_coupling",
            result,
            format!(
                "NEGATIVE CONTROL. Prescribed A's worldtube ignores B's μ change. Pre {:.12e}; post {:.12e} (must fail post).",
                result.pre_influence, result.post_influence
            ),
        ),
        Err(error) => gate(
            &mut report,
            "authored_worldtube_is_not_coupling",
            false,
            error.to_string(),
        ),
    }

    let inst = instantaneous_two_body_two_sided();
    record_two_sided(
        &mut report,
        "instantaneous_two_body_precone",
        "instantaneous_two_body_is_not_retarded",
        inst,
        format!(
            "NEGATIVE CONTROL. Present-state two-body Euler responds immediately. Pre {:.12e}; post {:.12e} (must fail pre).",
            inst.pre_influence, inst.post_influence
        ),
    );

    let coupled = match coupled_mass_change_two_sided() {
        Ok(result) => {
            record_two_sided(
                &mut report,
                "coupled_mass_change_r4",
                "retarded_two_way_backreaction",
                result,
                format!(
                    "A's next segments come from B's retarded field. B μ 1→2 at t=0. A's trajectory pre t=1/64 influence {:.12e}; post t=1/8 influence {:.12e}.",
                    result.pre_influence, result.post_influence
                ),
            );
            result
        }
        Err(error) => {
            gate(
                &mut report,
                "retarded_two_way_backreaction",
                false,
                error.to_string(),
            );
            TwoSidedResult {
                passed: false,
                pre_passed: false,
                post_passed: false,
                pre_influence: f64::NAN,
                post_influence: f64::NAN,
            }
        }
    };

    match every_mass_sources_passed() {
        Ok(passed) => gate(
            &mut report,
            "every_mass_sources",
            passed,
            "μ_B=1/64 still moves A; μ_B=0 does not. Backreaction is by influence, not an is_planet flag.",
        ),
        Err(error) => gate(&mut report, "every_mass_sources", false, error.to_string()),
    }

    match mutual_two_way_passed() {
        Ok(passed) => gate(
            &mut report,
            "mutual_two_way",
            passed,
            "Equal μ pair: both worldtubes leave their genesis positions. One-way test-particle maps cannot pass.",
        ),
        Err(error) => gate(&mut report, "mutual_two_way", false, error.to_string()),
    }

    match no_self_force_passed() {
        Ok(passed) => gate(
            &mut report,
            "no_self_force",
            passed,
            "An isolated rest mass does not accelerate itself. Coupled steps exclude the querier's own monopole.",
        ),
        Err(error) => gate(&mut report, "no_self_force", false, error.to_string()),
    }

    match fleet_collective_two_sided() {
        Ok((two_sided, passed)) => {
            push_metric(
                &mut report,
                "fleet_collective_n64",
                "pre_lightcone_response",
                two_sided.pre_influence,
                "length",
                0.0,
                two_sided.pre_passed,
            );
            push_metric(
                &mut report,
                "fleet_collective_n64",
                "post_lightcone_influence",
                two_sided.post_influence,
                "length",
                POST_LIGHTCONE_INFLUENCE_MIN,
                two_sided.post_passed,
            );
            gate(
                &mut report,
                "fleet_collective_n64",
                passed,
                format!(
                    "Star plus 1 vs 63 ships appearing at t=0 near r=4. Pre-cone star influence {:.12e}; post-cone {:.12e}; 63-ship displacement is larger. Direct tiny-N reference, not FMM.",
                    two_sided.pre_influence, two_sided.post_influence
                ),
            );
        }
        Err(error) => gate(
            &mut report,
            "fleet_collective_n64",
            false,
            error.to_string(),
        ),
    }

    record_well_posed_exterior(&mut report);
    crate::compact::record_compact_field(&mut report);
    crate::exact_branch::record_terminating_exact_branches(&mut report);

    match coupled_capture_halt_passed() {
        Ok(passed) => gate(
            &mut report,
            "coupled_capture_halt",
            passed,
            "Body B starts at r=1/4096 of A (Interior) with tiny μ_B so A's exterior Newton stays subluminal. The next segment is a finite capture halt: B stays put, momenta vanish, no NaN and no Newton through r=0. Absorbing capture is not a Schwarzschild geodesic.",
        ),
        Err(error) => gate(&mut report, "coupled_capture_halt", false, error.to_string()),
    }

    fail_missing(
        &mut report,
        "orbit_stability",
        "No orbit map and no Kepler tuning. Causality plus backreaction are required before any orbit integrator.",
    );
    fail_missing(
        &mut report,
        "angular_isotropy",
        "No rotation suite. Frozen quantum/rotation ladder remains on the rejected stationary experiments.",
    );
    fail_missing(
        &mut report,
        "quantum_refinement",
        "Coupled position projection 2^-20 is a research finite map, not the frozen 2^-22..2^-24 orbit ladder.",
    );
    fail_missing(
        &mut report,
        "stationary_clock",
        "Retarded coupled steps do not define dτ/dt or a piecewise lapse.",
    );
    fail_missing(
        &mut report,
        "source_tree_bound",
        "No monopole quadtree/FMM. Direct retarded evaluation is the tiny-N reference only.",
    );
    fail_missing(
        &mut report,
        "source_backreaction",
        "Frozen source_backreaction is instantaneous Newton fleet scaling and pair-force residual. Retarded coupling does not claim simultaneous action-reaction, and this is not a production orbit map.",
    );
    // Production gate is recorded by record_terminating_exact_branches.

    let mut notes = String::from("retarded_two_way_backreaction ");
    let _ = write!(
        notes,
        "{}; authored and instantaneous negative controls kept.",
        if coupled.passed { "passed" } else { "failed" }
    );
    report.evidence.push(notes);
    if let Ok(sys) = pair_at_rest(q(1, 1), q(1, 1)) {
        report.evidence.push(sys.kernel.contract_identity());
    }
    report
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn coupled_law_is_isolated() {
        assert_ne!(COUPLED_LAW_ID, RESEARCH_LAW_ID);
        assert_ne!(COUPLED_LAW_ID, INERTIAL_LAB_LAW_ID);
        coupled_manifest().unwrap();
    }

    #[test]
    fn instantaneous_two_body_fails_pre_cone() {
        let result = instantaneous_two_body_two_sided();
        assert!(!result.pre_passed);
        assert!(result.post_passed);
        assert!(!result.passed);
        assert!(result.pre_influence > 0.0);
    }

    #[test]
    fn coupled_mass_change_is_two_sided() {
        let result = coupled_mass_change_two_sided().unwrap();
        assert_eq!(result.pre_influence, 0.0);
        assert!(result.post_influence > 0.0);
        assert!(result.passed);
    }

    #[test]
    fn every_positive_mass_sources() {
        assert!(every_mass_sources_passed().unwrap());
    }

    #[test]
    fn both_bodies_move() {
        assert!(mutual_two_way_passed().unwrap());
    }

    #[test]
    fn isolated_mass_has_no_self_force() {
        assert!(no_self_force_passed().unwrap());
    }

    #[test]
    fn fleet_collective_is_retarded_and_larger() {
        let (two_sided, passed) = fleet_collective_two_sided().unwrap();
        assert_eq!(two_sided.pre_influence, 0.0);
        assert!(two_sided.post_influence > 0.0);
        assert!(passed);
    }

    #[test]
    fn next_segment_is_the_retarded_update() {
        let mut sys = pair_at_rest(q(1, 1), q(1, 1)).unwrap();
        sys.step().unwrap();
        assert_eq!(sys.position(1).unwrap(), sys.last_predicted[0]);
        assert_eq!(sys.position(2).unwrap(), sys.last_predicted[1]);
        assert_ne!(sys.position(1).unwrap(), origin());
    }

    #[test]
    fn rejects_more_than_tiny_n() {
        let bodies: Vec<_> = (0..=MAX_BODIES)
            .map(|i| (i as u64 + 1, [q(i as i128 + 8, 1), Q::zero()], q(1, 1)))
            .collect();
        assert!(matches!(
            CoupledSystem::at_rest(bodies),
            Err(KernelError::Invalid(_))
        ));
    }

    #[test]
    fn incomplete_coupled_certified_query_fails_closed() {
        let sys = pair_at_rest(q(1, 1), q(1, 1)).unwrap();
        let query = KernelEvent {
            time: q(1, 1),
            position: [q(1, 1), Q::zero()],
        };
        assert!(sys.kernel.acceleration_at(query).is_ok());
        assert_eq!(
            sys.kernel.certified_acceleration_at(query).unwrap_err(),
            KernelError::UncertifiedExterior
        );
    }

    #[test]
    fn coupled_capture_halt_is_finite() {
        assert!(coupled_capture_halt_passed().unwrap());
    }

    #[test]
    fn coupled_kernel_does_not_promote() {
        let report = qualify_coupled_kernel();
        assert_eq!(report.id, COUPLED_LAW_ID);
        assert_eq!(report.status, "FAIL");
        assert!(
            report
                .gates
                .iter()
                .find(|g| g.id == "retarded_two_way_backreaction")
                .unwrap()
                .passed
        );
        assert!(
            report
                .gates
                .iter()
                .find(|g| g.id == "source_change_light_cone")
                .unwrap()
                .passed
        );
        assert!(
            report
                .gates
                .iter()
                .find(|g| g.id == "well_posed_exterior")
                .unwrap()
                .passed
        );
        assert!(
            !report
                .gates
                .iter()
                .find(|g| g.id == "authored_worldtube_is_not_coupling")
                .unwrap()
                .passed
        );
        assert!(
            !report
                .gates
                .iter()
                .find(|g| g.id == "instantaneous_two_body_is_not_retarded")
                .unwrap()
                .passed
        );
        assert!(
            report
                .gates
                .iter()
                .find(|g| g.id == "coupled_capture_halt")
                .unwrap()
                .passed
        );
        for id in [
            "exact_cone_before_on_after",
            "on_cone_tie_is_visible",
            "on_horizon_tie_is_capture",
            "coincidence_tie_refuses_not_nan",
            "certified_exterior_refuses_incomplete",
            "f64_escalates_or_fails_closed",
            "iteration_cap_is_failed_execution",
            "floating_root_is_not_certificate",
            "curved_null_geodesic_unsupported",
        ] {
            assert!(
                report.gates.iter().find(|g| g.id == id).unwrap().passed,
                "{id} must pass as a terminating-branch capability or negative control"
            );
        }
        for id in [
            "orbit_stability",
            "source_backreaction",
            "compact_field_certification",
            "terminating_exact_branches",
        ] {
            assert!(
                !report.gates.iter().find(|g| g.id == id).unwrap().passed,
                "{id} must remain failed"
            );
        }
    }
}
