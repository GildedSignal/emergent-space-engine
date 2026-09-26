//! Isolated causal physical-kernel research track.
//!
//! Law id: `es-causal-retarded-monopole-v0`. This is never
//! `es-inertial-causal-v1` and is not a production gravity law. It exists so
//! future gravity cannot be fake-Newtonian: source *changes* have retarded
//! support, compact queries use a finite absorbing capture map rather than
//! 1/r² through r=0, and missing G2 semantics stay failed instead of being
//! hidden behind a pretty orbit.
//!
//! # Candidate contract
//!
//! **State.** A kernel state is a finite list of source worldtubes plus a query
//! event `(t, x, y)`. Each worldtube is a piecewise-constant history of
//! `(since, position, μ)` segments. This prescribed-worldtube evaluator does
//! not couple the field back onto source motion. Self-consistent two-way
//! retarded backreaction is a sibling candidate (`es-causal-retarded-coupled-v0`).
//!
//! **Causal field / source history.** The acceleration at a query is the
//! 3D-planar monopole sum using, for each source, the latest segment in the
//! *closed* past light cone:
//! `c²(t − t_s)² ≥ |x − x_s|²` and `t ≥ t_s`, decided in rationals with
//! integer `c`. Segments still outside that cone contribute nothing. This is a
//! retarded source evaluator, not an ad-hoc delay bolted onto a Verlet orbit
//! and called G2. A change that has not arrived must have zero influence; a
//! change that has arrived must have nonzero influence. Always-zero and
//! instantaneous maps both fail that two-sided gate.
//!
//! **Exterior.** `ExteriorModel::FiniteAuthoritativeRoot` is the allowed next
//! model. `acceleration_at` evaluates listed worldtubes only (retarded kernel).
//! `certified_acceleration_at` requires `declared_complete=true` and returns
//! the listed field plus a sound omitted-tail enclosure, or fails closed
//! (uncertified / resource). Incomplete roots cannot silently omit the frozen
//! unit source at r=16. A claimed bound that does not contain that influence
//! fails `well_posed_exterior`. This is a tiny-N 3D-planar remainder, not a
//! cosmological or procedural unresolved-matter certificate.
//!
//! **Exact / finite branch decisions.** Light-cone membership, compact-radius
//! class (`r ≶ 2μ/c²`: Interior / OnHorizon / Exterior / Singular), capture
//! versus not, and certified-exterior completeness are terminating rational
//! or fail-closed predicates (one comparison; documented max steps). On-cone
//! equality is visible (closed cone). On-horizon equality is capture. `r=0`
//! refuses (`Singular`), never NaN. Ambiguous `f64` escalates to an exact
//! dyadic or fails closed; an iteration cap is a failed execution, not a
//! guessed sign. Field *values* stay `f64` Newton. There is no curved-null
//! geodesic branch solver, so `terminating_exact_branches` remains failed.
//!
//! **Compact map.** `r_s = 2μ/c²`. Coincidence is `Singular` (finite error,
//! never NaN). On or inside `r_s` of a retarded-visible source the specified
//! map is absorbing **capture**, not Newton 1/r². Capture of a mass change is
//! causal: a source still outside the closed past cone cannot capture.
//! `acceleration_at` still refuses compact queries (`CompactForbidden`);
//! `field_at` returns the capture branch. This is not Schwarzschild/Kerr,
//! photon-sphere capture, or light deflection, so
//! `compact_field_certification` remains failed.
//!
//! **Domains.** Weak-field exterior of a finite root, subluminal source
//! histories, piecewise-constant segments. The frozen orbit/quantum ladder
//! stays on the stationary maps; this kernel does not run or retune those
//! thresholds.

use super::{gate, gravitational_acceleration, norm, CandidateReport, Metric};
use num_rational::Ratio;
use num_traits::Zero;
use serde::Deserialize;
use std::fmt::Write as _;

pub const RESEARCH_LAW_ID: &str = "es-causal-retarded-monopole-v0";
pub const INERTIAL_LAB_LAW_ID: &str = "es-inertial-causal-v1";
pub const POST_LIGHTCONE_INFLUENCE_MIN: f64 = 0.0;

const MANIFEST: &str = include_str!("../../../scenarios/law-gates.json");
pub(crate) const C: i128 = 64;
pub(crate) const GENESIS: i128 = -65_536;

pub type Q = Ratio<i128>;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct KernelEvent {
    pub time: Q,
    pub position: [Q; 2],
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct SourceSegment {
    pub since: Q,
    pub position: [Q; 2],
    pub mu: Q,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct SourceWorldtube {
    pub id: u64,
    pub segments: Vec<SourceSegment>,
}

/// Conservative remainder for unlisted mass at coordinate radius ≥
/// `exterior_radius`. The certified acceleration enclosure is
/// `|a_omitted| ≤ μ / (R − ||x||₁)²` when `||x||₁ < R`.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct OmittedTailBound {
    pub exterior_radius: Q,
    pub mu_bound: Q,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ExteriorModel {
    Unspecified,
    FiniteAuthoritativeRoot {
        support_radius: Q,
        declared_complete: bool,
        omitted_tail: Option<OmittedTailBound>,
    },
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct CertifiedAcceleration {
    pub listed: [f64; 2],
    /// Sound 3D-planar bound on omitted-tail acceleration magnitude.
    pub omitted_tail_bound: f64,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum BranchDecision {
    Before,
    On,
    After,
}

/// Exact compact-radius class for `r_s = 2μ/c²`.
/// Compared as `r² c⁴ ≶ 4μ²` so membership does not take a square root.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum CompactClass {
    Exterior,
    OnHorizon,
    Interior,
}

/// Specified finite compact rule. Never NaN, never silent Newton through r=0.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum CompactMap {
    Exterior,
    Captured { class: CompactClass },
    Singular,
}

/// Retarded field query: weak-field monopole or the absorbing compact branch.
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum FieldAt {
    Acceleration([f64; 2]),
    Captured { id: u64, class: CompactClass },
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum KernelError {
    SuperluminalHistory {
        id: u64,
    },
    CompactForbidden {
        id: u64,
    },
    Singular {
        id: u64,
    },
    Invalid(&'static str),
    /// Incomplete root or unspecified exterior: the query is not certified.
    UncertifiedExterior,
    /// Query is not in the certified interior (on/inside the omitted tail).
    ExteriorResourceLimit,
    /// NaN or Inf cannot classify a branch.
    NonfiniteBranch,
    /// Comparison/iteration budget exhausted: failed execution, not a guessed sign.
    BranchBudgetExhausted {
        max_steps: u32,
    },
    /// Finite float could not be converted to a laboratory rational.
    ExactConversionOverflow,
    /// Predicate is not implemented by this kernel (curved-null geodesic).
    UnsupportedPredicate(&'static str),
}

impl std::fmt::Display for KernelError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::SuperluminalHistory { id } => {
                write!(f, "source {id} history is superluminal")
            }
            Self::CompactForbidden { id } => {
                write!(f, "source {id} query is at or inside compact radius 2μ/c²")
            }
            Self::Singular { id } => write!(f, "source {id} query is singular"),
            Self::Invalid(reason) => write!(f, "{reason}"),
            Self::UncertifiedExterior => write!(
                f,
                "finite root is not declared complete and has no certified omitted-tail bound"
            ),
            Self::ExteriorResourceLimit => write!(
                f,
                "query is not in the certified interior of the finite exterior"
            ),
            Self::NonfiniteBranch => write!(f, "nonfinite value cannot classify a branch"),
            Self::BranchBudgetExhausted { max_steps } => write!(
                f,
                "branch budget of {max_steps} steps exhausted; no guessed sign accepted"
            ),
            Self::ExactConversionOverflow => {
                write!(f, "f64 exact conversion overflowed laboratory rationals")
            }
            Self::UnsupportedPredicate(name) => {
                write!(f, "unsupported predicate {name}")
            }
        }
    }
}

#[derive(Clone, Debug)]
pub struct CausalKernel {
    pub law_id: &'static str,
    pub light_speed: i128,
    pub sources: Vec<SourceWorldtube>,
    pub exterior: ExteriorModel,
}

#[derive(Clone, Copy, Debug)]
pub struct TwoSidedResult {
    pub passed: bool,
    pub pre_passed: bool,
    pub post_passed: bool,
    pub pre_influence: f64,
    pub post_influence: f64,
}

#[derive(Clone, Deserialize)]
struct ManifestSlice {
    aggregate_gates: FrozenAggregates,
    required_production_gates: Vec<String>,
    causal_kernel_research: ResearchManifest,
}

#[derive(Clone, Deserialize)]
struct FrozenAggregates {
    pre_lightcone_response_max: f64,
}

#[derive(Clone, Deserialize)]
struct ResearchManifest {
    law_id: String,
    first_gate: String,
    light_speed: i128,
    pre_lightcone_response_max: f64,
    post_lightcone_influence_min: f64,
    post_lightcone_influence_strict: bool,
    fixtures: Vec<NamedFixture>,
}

#[derive(Clone, Deserialize)]
struct NamedFixture {
    id: String,
}

pub fn research_manifest() -> Result<(), String> {
    let slice: ManifestSlice = serde_json::from_str(MANIFEST).map_err(|e| e.to_string())?;
    if slice.causal_kernel_research.law_id != RESEARCH_LAW_ID {
        return Err("research law id drifted".into());
    }
    if slice.causal_kernel_research.law_id == INERTIAL_LAB_LAW_ID {
        return Err("research kernel must not reuse the inertial laboratory id".into());
    }
    if slice.causal_kernel_research.first_gate != "source_change_light_cone" {
        return Err("first gate must remain source_change_light_cone".into());
    }
    if slice.aggregate_gates.pre_lightcone_response_max != 0.0
        || slice.causal_kernel_research.pre_lightcone_response_max != 0.0
        || slice.causal_kernel_research.post_lightcone_influence_min != POST_LIGHTCONE_INFLUENCE_MIN
        || !slice.causal_kernel_research.post_lightcone_influence_strict
        || slice.causal_kernel_research.light_speed != C
    {
        return Err("causal-kernel research thresholds were weakened or retuned".into());
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
    let ids: Vec<&str> = slice
        .causal_kernel_research
        .fixtures
        .iter()
        .map(|f| f.id.as_str())
        .collect();
    let expected = [
        "mass_change_r4",
        "compact_vs_far",
        "huge_mass_ratio",
        "moving_source",
        "exterior_source_r16",
        "simultaneous_source_changes",
    ];
    if ids != expected {
        return Err("causal-kernel fixtures were renamed, dropped or reordered".into());
    }
    exterior_manifest()?;
    crate::compact::compact_manifest()?;
    crate::exact_branch::exact_branch_manifest()?;
    Ok(())
}

#[derive(Clone, Deserialize)]
struct ExteriorFileSlice {
    finite_exterior_research: ExteriorResearchManifest,
}

#[derive(Clone, Deserialize)]
struct ExteriorResearchManifest {
    gate: String,
    parent_kernel: String,
    coupled_kernel: String,
    light_speed: i128,
    fixtures: Vec<NamedFixture>,
}

pub(crate) const EXTERIOR_FIXTURE_IDS: [&str; 6] = [
    "incomplete_omit_r16",
    "false_complete_omit_r16",
    "unsound_tail_bound_r16",
    "certified_tail_bound_r16",
    "query_in_omitted_tail",
    "listed_r16_complete",
];

pub fn exterior_manifest() -> Result<(), String> {
    let slice: ExteriorFileSlice = serde_json::from_str(MANIFEST).map_err(|e| e.to_string())?;
    if slice.finite_exterior_research.gate != "well_posed_exterior" {
        return Err("finite-exterior gate must remain well_posed_exterior".into());
    }
    if slice.finite_exterior_research.parent_kernel != RESEARCH_LAW_ID {
        return Err("finite-exterior parent must remain the retarded monopole kernel".into());
    }
    if slice.finite_exterior_research.coupled_kernel.is_empty() {
        return Err("finite-exterior coupled kernel id is missing".into());
    }
    if slice.finite_exterior_research.light_speed != C {
        return Err("finite-exterior light speed was retuned".into());
    }
    let ids: Vec<&str> = slice
        .finite_exterior_research
        .fixtures
        .iter()
        .map(|f| f.id.as_str())
        .collect();
    if ids != EXTERIOR_FIXTURE_IDS {
        return Err("finite-exterior fixtures were renamed, dropped or reordered".into());
    }
    Ok(())
}

pub fn exterior_coupled_kernel() -> Result<String, String> {
    let slice: ExteriorFileSlice = serde_json::from_str(MANIFEST).map_err(|e| e.to_string())?;
    Ok(slice.finite_exterior_research.coupled_kernel)
}

pub fn q(n: i128, d: i128) -> Q {
    Ratio::new(n, d)
}

pub fn cone_relation(source: KernelEvent, query: KernelEvent, c: i128) -> Option<BranchDecision> {
    if query.time < source.time {
        return None;
    }
    let dt = query.time - source.time;
    let dx = query.position[0] - source.position[0];
    let dy = query.position[1] - source.position[1];
    let cdt = Q::from_integer(c) * dt;
    let lhs = cdt * cdt;
    let rhs = dx * dx + dy * dy;
    Some(if lhs > rhs {
        BranchDecision::After
    } else if lhs == rhs {
        BranchDecision::On
    } else {
        BranchDecision::Before
    })
}

pub fn in_closed_past_cone(source: KernelEvent, query: KernelEvent, c: i128) -> bool {
    matches!(
        cone_relation(source, query, c),
        Some(BranchDecision::On | BranchDecision::After)
    )
}

fn subluminal_step(prev: SourceSegment, next: SourceSegment, c: i128) -> bool {
    if next.since <= prev.since {
        return false;
    }
    if prev.position == next.position {
        return true;
    }
    matches!(
        cone_relation(
            KernelEvent {
                time: prev.since,
                position: prev.position,
            },
            KernelEvent {
                time: next.since,
                position: next.position,
            },
            c,
        ),
        Some(BranchDecision::After)
    )
}

/// Compact radius `r_s = 2μ/c²`. Exact rational for integer `c` and rational μ.
pub fn compact_radius(mu: Q, c: i128) -> Option<Q> {
    if mu <= Q::zero() {
        None
    } else {
        Some(Q::from_integer(2) * mu / Q::from_integer(c * c))
    }
}

fn displacement_r2(displacement: [Q; 2]) -> Q {
    displacement[0] * displacement[0] + displacement[1] * displacement[1]
}

/// Exact compact class: compare `r² c⁴` with `4μ²` (no square root).
pub fn compact_class(displacement: [Q; 2], mu: Q, c: i128) -> CompactClass {
    if mu <= Q::zero() {
        return CompactClass::Exterior;
    }
    let c2 = Q::from_integer(c * c);
    let lhs = displacement_r2(displacement) * c2 * c2;
    let rhs = Q::from_integer(4) * mu * mu;
    if lhs > rhs {
        CompactClass::Exterior
    } else if lhs == rhs {
        CompactClass::OnHorizon
    } else {
        CompactClass::Interior
    }
}

/// Smallest non-divergent compact rule: coincidence is singular; on or inside
/// `r_s` is absorbing capture; outside is the retarded 3D-planar monopole.
pub fn compact_map(seg: SourceSegment, query: KernelEvent, c: i128) -> CompactMap {
    let displacement = [
        query.position[0] - seg.position[0],
        query.position[1] - seg.position[1],
    ];
    if displacement_r2(displacement).is_zero() {
        return CompactMap::Singular;
    }
    match compact_class(displacement, seg.mu, c) {
        CompactClass::Exterior => CompactMap::Exterior,
        class => CompactMap::Captured { class },
    }
}

impl CausalKernel {
    pub fn new(
        sources: Vec<SourceWorldtube>,
        exterior: ExteriorModel,
    ) -> Result<Self, KernelError> {
        for source in &sources {
            if source.segments.is_empty() {
                return Err(KernelError::Invalid("source worldtube has no segments"));
            }
            for pair in source.segments.windows(2) {
                if !subluminal_step(pair[0], pair[1], C) {
                    return Err(KernelError::SuperluminalHistory { id: source.id });
                }
            }
        }
        match &exterior {
            ExteriorModel::FiniteAuthoritativeRoot {
                omitted_tail: Some(tail),
                support_radius,
                ..
            } => {
                if tail.mu_bound < Q::zero() {
                    return Err(KernelError::Invalid("omitted-tail μ bound is negative"));
                }
                if tail.exterior_radius <= Q::zero() {
                    return Err(KernelError::Invalid(
                        "omitted-tail exterior radius must be positive",
                    ));
                }
                if tail.exterior_radius < *support_radius {
                    return Err(KernelError::Invalid(
                        "omitted-tail radius is inside the declared support",
                    ));
                }
            }
            ExteriorModel::Unspecified | ExteriorModel::FiniteAuthoritativeRoot { .. } => {}
        }
        Ok(Self {
            law_id: RESEARCH_LAW_ID,
            light_speed: C,
            sources,
            exterior,
        })
    }

    pub fn contract_identity(&self) -> String {
        let exterior = match &self.exterior {
            ExteriorModel::Unspecified => "unspecified",
            ExteriorModel::FiniteAuthoritativeRoot {
                declared_complete: false,
                omitted_tail: None,
                ..
            } => "finite-root-incomplete",
            ExteriorModel::FiniteAuthoritativeRoot {
                declared_complete: false,
                omitted_tail: Some(_),
                ..
            } => "finite-root-incomplete-tail",
            ExteriorModel::FiniteAuthoritativeRoot {
                declared_complete: true,
                omitted_tail: None,
                ..
            } => "finite-root-complete-vacuum",
            ExteriorModel::FiniteAuthoritativeRoot {
                declared_complete: true,
                omitted_tail: Some(_),
                ..
            } => "finite-root-complete-tail",
        };
        format!(
            "law={} c={} exterior={exterior}",
            self.law_id, self.light_speed
        )
    }

    fn visible_segment(
        &self,
        source: &SourceWorldtube,
        query: KernelEvent,
    ) -> Option<SourceSegment> {
        source.segments.iter().rev().copied().find(|seg| {
            in_closed_past_cone(
                KernelEvent {
                    time: seg.since,
                    position: seg.position,
                },
                query,
                self.light_speed,
            )
        })
    }

    pub fn acceleration_at(&self, query: KernelEvent) -> Result<[f64; 2], KernelError> {
        self.acceleration_at_excluding(query, None)
    }

    pub fn field_at(&self, query: KernelEvent) -> Result<FieldAt, KernelError> {
        self.field_at_excluding(query, None)
    }

    /// Retarded 3D-planar monopole excluding one source id. Compact queries
    /// remain `CompactForbidden` so existing refuse fixtures stay exact.
    pub fn acceleration_at_excluding(
        &self,
        query: KernelEvent,
        exclude_id: Option<u64>,
    ) -> Result<[f64; 2], KernelError> {
        match self.field_at_excluding(query, exclude_id)? {
            FieldAt::Acceleration(acceleration) => Ok(acceleration),
            FieldAt::Captured { id, .. } => Err(KernelError::CompactForbidden { id }),
        }
    }

    /// Specified compact map: absorbing capture on/inside `r_s` of a retarded
    /// visible source; exterior Newton otherwise. Never NaN.
    pub fn field_at_excluding(
        &self,
        query: KernelEvent,
        exclude_id: Option<u64>,
    ) -> Result<FieldAt, KernelError> {
        let mut sum = [0.0, 0.0];
        for source in &self.sources {
            if exclude_id == Some(source.id) {
                continue;
            }
            let Some(seg) = self.visible_segment(source, query) else {
                continue;
            };
            match compact_map(seg, query, self.light_speed) {
                CompactMap::Singular => {
                    return Err(KernelError::Singular { id: source.id });
                }
                CompactMap::Captured { class } => {
                    return Ok(FieldAt::Captured {
                        id: source.id,
                        class,
                    });
                }
                CompactMap::Exterior => {
                    if seg.mu.is_zero() {
                        continue;
                    }
                    let displacement = [
                        qf(query.position[0] - seg.position[0]),
                        qf(query.position[1] - seg.position[1]),
                    ];
                    let part = gravitational_acceleration(displacement, qf(seg.mu))
                        .map_err(|_| KernelError::Singular { id: source.id })?;
                    if !part[0].is_finite() || !part[1].is_finite() {
                        return Err(KernelError::NonfiniteBranch);
                    }
                    sum = [sum[0] + part[0], sum[1] + part[1]];
                }
            }
        }
        if !sum[0].is_finite() || !sum[1].is_finite() {
            return Err(KernelError::NonfiniteBranch);
        }
        Ok(FieldAt::Acceleration(sum))
    }

    /// Listed retarded field plus a certified omitted-tail enclosure, or a
    /// closed failure. Incomplete roots never return a silent listed-only
    /// field as if it were the exterior.
    pub fn certified_acceleration_at(
        &self,
        query: KernelEvent,
    ) -> Result<CertifiedAcceleration, KernelError> {
        match &self.exterior {
            ExteriorModel::Unspecified
            | ExteriorModel::FiniteAuthoritativeRoot {
                declared_complete: false,
                ..
            } => Err(KernelError::UncertifiedExterior),
            ExteriorModel::FiniteAuthoritativeRoot {
                declared_complete: true,
                omitted_tail,
                ..
            } => {
                let listed = self.acceleration_at(query)?;
                let omitted_tail_bound = match omitted_tail {
                    None => 0.0,
                    Some(tail) => {
                        let raw = qf(omitted_tail_acceleration_bound(query.position, tail)?);
                        raw + 128.0 * f64::EPSILON * (1.0 + raw)
                    }
                };
                Ok(CertifiedAcceleration {
                    listed,
                    omitted_tail_bound,
                })
            }
        }
    }

    /// Present worldtube coordinate at lab time `t`: the last authored or
    /// committed segment with `since <= t`. This is the source's own history,
    /// not a retarded query seen by someone else.
    pub fn source_position_at(&self, id: u64, time: Q) -> Option<[Q; 2]> {
        let source = self.sources.iter().find(|source| source.id == id)?;
        source
            .segments
            .iter()
            .rev()
            .find(|seg| seg.since <= time)
            .map(|seg| seg.position)
    }
}

pub(crate) fn qf(value: Q) -> f64 {
    *value.numer() as f64 / *value.denom() as f64
}

pub(crate) fn qf_pair(value: [Q; 2]) -> [f64; 2] {
    [qf(value[0]), qf(value[1])]
}

pub(crate) fn genesis(position: [Q; 2], mu: Q) -> SourceSegment {
    SourceSegment {
        since: Q::from_integer(GENESIS),
        position,
        mu,
    }
}

pub(crate) fn tube(id: u64, segments: Vec<SourceSegment>) -> SourceWorldtube {
    SourceWorldtube { id, segments }
}

pub(crate) fn finite_root() -> ExteriorModel {
    ExteriorModel::FiniteAuthoritativeRoot {
        support_radius: q(16, 1),
        declared_complete: false,
        omitted_tail: None,
    }
}

fn abs_q(value: Q) -> Q {
    if value < Q::zero() {
        -value
    } else {
        value
    }
}

/// Sound conservative remainder: Euclidean distance to omitted mass is at
/// least `R − ||x||₁`, so `|a| ≤ μ / (R − ||x||₁)²`.
pub fn omitted_tail_acceleration_bound(
    query: [Q; 2],
    tail: &OmittedTailBound,
) -> Result<Q, KernelError> {
    if tail.mu_bound < Q::zero() {
        return Err(KernelError::Invalid("omitted-tail μ bound is negative"));
    }
    if tail.exterior_radius <= Q::zero() {
        return Err(KernelError::Invalid(
            "omitted-tail exterior radius must be positive",
        ));
    }
    let r_upper = abs_q(query[0]) + abs_q(query[1]);
    if r_upper >= tail.exterior_radius {
        return Err(KernelError::ExteriorResourceLimit);
    }
    let min_dist = tail.exterior_radius - r_upper;
    Ok(tail.mu_bound / (min_dist * min_dist))
}

fn interior_query() -> KernelEvent {
    KernelEvent {
        time: q(1, 1),
        position: [q(1, 1), Q::zero()],
    }
}

fn omitted_r16() -> [Q; 2] {
    [q(16, 1), Q::zero()]
}

fn sound_tail() -> OmittedTailBound {
    OmittedTailBound {
        exterior_radius: q(16, 1),
        mu_bound: q(1, 1),
    }
}

fn unsound_tail() -> OmittedTailBound {
    OmittedTailBound {
        exterior_radius: q(32, 1),
        mu_bound: q(1, 1),
    }
}

fn exterior_root(complete: bool, tail: Option<OmittedTailBound>) -> ExteriorModel {
    ExteriorModel::FiniteAuthoritativeRoot {
        support_radius: q(8, 1),
        declared_complete: complete,
        omitted_tail: tail,
    }
}

fn actual_omitted_r16() -> f64 {
    gravitational_acceleration([-15.0, 0.0], 1.0)
        .map(norm)
        .expect("nonsingular r=16 exterior fixture")
}

fn certified_empty(
    complete: bool,
    tail: Option<OmittedTailBound>,
    query: KernelEvent,
) -> Result<CertifiedAcceleration, KernelError> {
    CausalKernel::new(vec![], exterior_root(complete, tail))?.certified_acceleration_at(query)
}

pub(crate) fn record_well_posed_exterior(report: &mut CandidateReport) {
    match exterior_manifest() {
        Ok(()) => gate(
            report,
            "exterior_manifest_isolated",
            true,
            "New finite-exterior fixtures did not edit frozen production-gate identities or old numeric thresholds.",
        ),
        Err(error) => gate(report, "exterior_manifest_isolated", false, error),
    }

    let actual = actual_omitted_r16();
    let query = interior_query();
    let tail_query = KernelEvent {
        time: q(1, 1),
        position: omitted_r16(),
    };

    let incomplete = certified_empty(false, None, query);
    let incomplete_ok = matches!(incomplete, Err(KernelError::UncertifiedExterior));
    gate(
        report,
        "incomplete_omit_r16",
        incomplete_ok,
        "declared_complete=false with no omitted-tail bound: certified query at r=1 fails closed. Listed-only evaluation would silently omit the unit source at r=16.",
    );

    let false_complete = certified_empty(true, None, query);
    let false_ok = match false_complete {
        Ok(certified) => actual > certified.omitted_tail_bound,
        Err(_) => false,
    };
    gate(
        report,
        "false_complete_omit_r16",
        false_ok,
        format!(
            "declared_complete=true with vacuum remainder (bound 0) omits r=16. Actual influence {actual:.12e} exceeds the claimed enclosure."
        ),
    );

    let mut unsound_ok = false;
    let mut unsound_bound = 0.0;
    if let Ok(certified) = certified_empty(true, Some(unsound_tail()), query) {
        unsound_bound = certified.omitted_tail_bound;
        unsound_ok = actual > certified.omitted_tail_bound;
        push_metric(
            report,
            "unsound_tail_bound_r16",
            "omitted_influence",
            actual,
            "acceleration",
            unsound_bound,
            actual <= unsound_bound,
        );
    }
    gate(
        report,
        "unsound_tail_bound_r16",
        unsound_ok,
        format!(
            "Claimed tail R=32, μ≤1 at query r=1 has bound {unsound_bound:.12e}; actual r=16 unit source {actual:.12e} violates it."
        ),
    );

    let mut sound_ok = false;
    let mut sound_bound = 0.0;
    if let Ok(certified) = certified_empty(true, Some(sound_tail()), query) {
        sound_bound = certified.omitted_tail_bound;
        sound_ok = actual <= certified.omitted_tail_bound && certified.listed == [0.0, 0.0];
        push_metric(
            report,
            "certified_tail_bound_r16",
            "omitted_influence",
            actual,
            "acceleration",
            sound_bound,
            sound_ok,
        );
    }
    gate(
        report,
        "certified_tail_bound_r16",
        sound_ok,
        format!(
            "Sound tail R=16, μ≤1: bound {sound_bound:.12e} contains actual omitted influence {actual:.12e}. Conservative 3D-planar closest-approach remainder, tiny N."
        ),
    );

    let resource = certified_empty(true, Some(sound_tail()), tail_query);
    let resource_ok = matches!(resource, Err(KernelError::ExteriorResourceLimit));
    gate(
        report,
        "query_in_omitted_tail",
        resource_ok,
        "Query at r=16 lies on the omitted-tail radius and fails closed (resource/capability), not a silent listed field.",
    );

    let listed = match CausalKernel::new(
        vec![tube(7, vec![genesis(omitted_r16(), q(1, 1))])],
        ExteriorModel::FiniteAuthoritativeRoot {
            support_radius: q(16, 1),
            declared_complete: true,
            omitted_tail: None,
        },
    ) {
        Ok(kernel) => match kernel.certified_acceleration_at(query) {
            Ok(certified) => {
                let newton = gravitational_acceleration([-15.0, 0.0], 1.0).expect("newton r16");
                influence(certified.listed, newton) <= 0.0 && certified.omitted_tail_bound == 0.0
            }
            Err(_) => false,
        },
        Err(_) => false,
    };
    gate(
        report,
        "listed_r16_complete",
        listed,
        "Listing the r=16 source on a declared-complete root includes its influence; it is not omitted.",
    );

    let passed = incomplete_ok && false_ok && unsound_ok && sound_ok && resource_ok && listed;
    gate(
        report,
        "well_posed_exterior",
        passed,
        format!(
            "Two-sided finite exterior: incomplete omit fails closed; false-complete and unsound tails are detected against the unit source at r=16 (actual {actual:.12e}); sound remainder encloses it; query in the omitted region fails closed; listing the source is certified. Tiny-N 3D-planar remainder, not a cosmological/procedural certificate."
        ),
    );
}

pub fn two_sided_result(
    pre_influence: f64,
    post_influence: f64,
    pre_max: f64,
    post_min: f64,
) -> TwoSidedResult {
    let pre_passed = pre_influence.is_finite() && pre_influence <= pre_max;
    let post_passed = post_influence.is_finite() && post_influence > post_min;
    TwoSidedResult {
        passed: pre_passed && post_passed,
        pre_passed,
        post_passed,
        pre_influence,
        post_influence,
    }
}

pub(crate) fn influence(changed: [f64; 2], baseline: [f64; 2]) -> f64 {
    norm([changed[0] - baseline[0], changed[1] - baseline[1]])
}

fn mass_change_pair(
    position: [Q; 2],
    mu_before: Q,
    mu_after: Q,
    change_time: Q,
) -> Result<(CausalKernel, CausalKernel), KernelError> {
    let baseline = CausalKernel::new(
        vec![tube(1, vec![genesis(position, mu_before)])],
        finite_root(),
    )?;
    let changed = CausalKernel::new(
        vec![tube(
            1,
            vec![
                genesis(position, mu_before),
                SourceSegment {
                    since: change_time,
                    position,
                    mu: mu_after,
                },
            ],
        )],
        finite_root(),
    )?;
    Ok((changed, baseline))
}

pub(crate) fn mass_change_influence(
    source: [Q; 2],
    query: [Q; 2],
    mu_before: Q,
    mu_after: Q,
    time: Q,
) -> Result<f64, KernelError> {
    let (changed, baseline) = mass_change_pair(source, mu_before, mu_after, Q::zero())?;
    let event = KernelEvent {
        time,
        position: query,
    };
    Ok(influence(
        changed.acceleration_at(event)?,
        baseline.acceleration_at(event)?,
    ))
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

/// Cheap first-gate probe used by stationary maps (instantaneous adapters).
pub fn instantaneous_two_sided(pre_and_post: f64, pre_max: f64) -> TwoSidedResult {
    two_sided_result(
        pre_and_post,
        pre_and_post,
        pre_max,
        POST_LIGHTCONE_INFLUENCE_MIN,
    )
}

pub fn qualify_research_kernel() -> CandidateReport {
    let mut report = CandidateReport {
        id: RESEARCH_LAW_ID.into(),
        version: 0,
        status: "FAIL".into(),
        metrics: Vec::new(),
        gates: Vec::new(),
        evidence: vec![
            "Research kernel es-causal-retarded-monopole-v0 is isolated from es-inertial-causal-v1.".into(),
            "First gate is the two-sided source-change light-cone falsifier; no orbit map is tuned.".into(),
            "Retarded 3D-planar monopole with exact rational cones is not G2, GR, FMM, or delayed-Newton promotion.".into(),
            "Certified queries require a declared-complete finite root plus a sound omitted-tail enclosure, or fail closed.".into(),
            "Compact radius r_s=2μ/c² has exact Interior/OnHorizon/Exterior membership. On/inside r_s is absorbing capture, never NaN or Newton through r=0. That is not Schwarzschild/Kerr certification.".into(),
            "Kernel predicates (cone, compact class, capture, certified exterior) terminate in one rational comparison or fail closed. Curved-null geodesic branches are unsupported; terminating_exact_branches stays failed.".into(),
            format!(
                "Exterior contract variants include {:?}; default research root is {:?}.",
                ExteriorModel::Unspecified,
                finite_root()
            ),
        ],
    };

    let mut first = true;
    match research_manifest() {
        Ok(()) => gate(
            &mut report,
            "research_manifest_isolated",
            true,
            "New fixtures did not edit frozen production-gate identities or old numeric thresholds.",
        ),
        Err(error) => {
            first = false;
            gate(&mut report, "research_manifest_isolated", false, error);
        }
    }

    let pre = mass_change_influence(origin(), r4(), q(1, 1), q(2, 1), q(1, 64));
    let post = mass_change_influence(origin(), r4(), q(1, 1), q(2, 1), q(1, 8));
    let on = mass_change_influence(origin(), r4(), q(1, 1), q(2, 1), q(1, 16));
    let two_sided = match (pre, post) {
        (Ok(pre_influence), Ok(post_influence)) => {
            push_metric(
                &mut report,
                "mass_change_r4",
                "pre_lightcone_response",
                pre_influence,
                "acceleration",
                0.0,
                pre_influence <= 0.0,
            );
            push_metric(
                &mut report,
                "mass_change_r4",
                "post_lightcone_influence",
                post_influence,
                "acceleration",
                POST_LIGHTCONE_INFLUENCE_MIN,
                post_influence > POST_LIGHTCONE_INFLUENCE_MIN,
            );
            two_sided_result(
                pre_influence,
                post_influence,
                0.0,
                POST_LIGHTCONE_INFLUENCE_MIN,
            )
        }
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
    first &= two_sided.passed;
    gate(
        &mut report,
        "source_change_light_cone",
        two_sided.passed,
        format!(
            "FIRST GATE. Source μ 1→2 at t=0, query r=4. Pre t=1/64 influence {:.12e}; post t=1/8 influence {:.12e}. Instantaneous maps fail pre-cone; a null kernel fails post-cone.",
            two_sided.pre_influence, two_sided.post_influence
        ),
    );
    gate(
        &mut report,
        "causal_dynamic_sources",
        two_sided.passed,
        "Same two-sided retarded-source measurement as source_change_light_cone. Passing this kernel gate is not production gravity.",
    );
    match on {
        Ok(value) if value > POST_LIGHTCONE_INFLUENCE_MIN => {
            push_metric(
                &mut report,
                "mass_change_r4",
                "on_cone_influence",
                value,
                "acceleration",
                POST_LIGHTCONE_INFLUENCE_MIN,
                true,
            );
            gate(
                &mut report,
                "closed_light_cone_equality",
                true,
                "On-cone t=r/c is a finite exact branch: the change is visible.",
            );
        }
        Ok(value) => gate(
            &mut report,
            "closed_light_cone_equality",
            false,
            format!("on-cone influence {value} was not visible"),
        ),
        Err(error) => gate(
            &mut report,
            "closed_light_cone_equality",
            false,
            error.to_string(),
        ),
    }

    record_compact(&mut report);
    record_huge_mass(&mut report);
    record_moving(&mut report);
    record_exterior(&mut report);
    record_well_posed_exterior(&mut report);
    crate::compact::record_compact_field(&mut report);
    crate::exact_branch::record_terminating_exact_branches(&mut report);
    record_simultaneous(&mut report);
    record_static_newton_limit(&mut report);
    record_superluminal_rejection(&mut report);
    record_authored_backreaction(&mut report);

    fail_missing(
        &mut report,
        "orbit_stability",
        "No coupled retarded orbit map. A floating orbit is not accepted as G2; source-change causality is required first.",
    );
    fail_missing(
        &mut report,
        "angular_isotropy",
        "No orbit map, so no rotation suite. The frozen quantum/rotation ladder remains on the rejected stationary experiments.",
    );
    fail_missing(
        &mut report,
        "quantum_refinement",
        "This kernel is not a quantized finite map. Existing quanta 2^-22,2^-23,2^-24 stay frozen on the stationary suite and were not retuned.",
    );
    fail_missing(
        &mut report,
        "stationary_clock",
        "Retarded monopole queries do not define dτ/dt or a piecewise lapse.",
    );
    fail_missing(
        &mut report,
        "source_tree_bound",
        "No monopole quadtree/FMM in this kernel. Direct retarded evaluation is the small-system reference only.",
    );
    fail_missing(
        &mut report,
        "source_backreaction",
        "Prescribed worldtubes do not update from the field. Frozen source_backreaction is the stationary-map Newton fleet/force-balance diagnostic, not retarded coupling. See retarded_two_way_backreaction.",
    );
    // Production gate is recorded by record_terminating_exact_branches: kernel
    // predicates terminate, but curved-null/geodesic and f64 field values keep it failed.

    let mut notes = String::from("source_change_light_cone is the first gate; ");
    let _ = write!(
        notes,
        "it {} before any orbit work was attempted.",
        if first { "passed" } else { "failed" }
    );
    report.evidence.push(notes);
    if let Ok((changed, _)) = mass_change_pair(origin(), q(1, 1), q(2, 1), Q::zero()) {
        report.evidence.push(changed.contract_identity());
    }
    report
}

pub(crate) fn origin() -> [Q; 2] {
    [Q::zero(), Q::zero()]
}

pub(crate) fn r4() -> [Q; 2] {
    [q(4, 1), Q::zero()]
}

pub(crate) fn authored_trajectory_two_sided() -> Result<TwoSidedResult, KernelError> {
    let a = origin();
    let b = r4();
    let baseline = CausalKernel::new(
        vec![
            tube(1, vec![genesis(a, q(1, 1))]),
            tube(2, vec![genesis(b, q(1, 1))]),
        ],
        finite_root(),
    )?;
    let changed = CausalKernel::new(
        vec![
            tube(1, vec![genesis(a, q(1, 1))]),
            tube(
                2,
                vec![
                    genesis(b, q(1, 1)),
                    SourceSegment {
                        since: Q::zero(),
                        position: b,
                        mu: q(2, 1),
                    },
                ],
            ),
        ],
        finite_root(),
    )?;
    let pos = |kernel: &CausalKernel, time: Q| -> Result<[f64; 2], KernelError> {
        kernel
            .source_position_at(1, time)
            .map(qf_pair)
            .ok_or(KernelError::Invalid("missing source 1"))
    };
    let pre = influence(pos(&changed, q(1, 64))?, pos(&baseline, q(1, 64))?);
    let post = influence(pos(&changed, q(1, 8))?, pos(&baseline, q(1, 8))?);
    Ok(two_sided_result(
        pre,
        post,
        0.0,
        POST_LIGHTCONE_INFLUENCE_MIN,
    ))
}

fn record_authored_backreaction(report: &mut CandidateReport) {
    match authored_trajectory_two_sided() {
        Ok(result) => {
            push_metric(
                report,
                "authored_worldtube_no_coupling",
                "pre_lightcone_response",
                result.pre_influence,
                "length",
                0.0,
                result.pre_passed,
            );
            push_metric(
                report,
                "authored_worldtube_no_coupling",
                "post_lightcone_influence",
                result.post_influence,
                "length",
                POST_LIGHTCONE_INFLUENCE_MIN,
                result.post_passed,
            );
            gate(
                report,
                "retarded_two_way_backreaction",
                result.passed,
                format!(
                    "Prescribed worldtubes: A's present position is authored, not integrated from B's retarded field. Pre-cone influence {:.12e}; post-cone {:.12e}. This fails post (no coupling). Instantaneous two-body maps fail pre. A self-consistent retarded stepper is required.",
                    result.pre_influence, result.post_influence
                ),
            );
        }
        Err(error) => gate(
            report,
            "retarded_two_way_backreaction",
            false,
            error.to_string(),
        ),
    }
}

fn record_compact(report: &mut CandidateReport) {
    let kernel = CausalKernel::new(
        vec![tube(1, vec![genesis(origin(), q(1, 1))])],
        finite_root(),
    )
    .expect("static source");
    let compact = kernel.acceleration_at(KernelEvent {
        time: q(1, 1),
        position: [q(1, 2048), Q::zero()],
    });
    let far = kernel.acceleration_at(KernelEvent {
        time: q(1, 1),
        position: r4(),
    });
    let refused = matches!(compact, Err(KernelError::CompactForbidden { id: 1 }));
    let far_ok = far.map(norm).ok().is_some_and(|a| a > 0.0);
    gate(
        report,
        "compact_vs_far_domain",
        refused && far_ok,
        "Compact r=2μ/c²=1/2048 is refused; far r=4 remains evaluable. This does not certify compact gravity.",
    );
}

fn record_huge_mass(report: &mut CandidateReport) {
    let far = [q(1_000_000, 1), Q::zero()];
    let compact_near = CausalKernel::new(
        vec![tube(1, vec![genesis(origin(), q(1_000_000_000, 1))])],
        finite_root(),
    )
    .expect("huge static");
    let near_refused = matches!(
        compact_near.acceleration_at(KernelEvent {
            time: q(1, 1),
            position: r4(),
        }),
        Err(KernelError::CompactForbidden { id: 1 })
    );
    let pre = mass_change_influence(
        origin(),
        far,
        q(1_000_000_000, 1),
        q(2_000_000_000, 1),
        q(15_625, 4),
    );
    let post = mass_change_influence(
        origin(),
        far,
        q(1_000_000_000, 1),
        q(2_000_000_000, 1),
        q(31_250, 1),
    );
    let passed =
        near_refused && matches!((pre, post), (Ok(pre), Ok(post)) if pre <= 0.0 && post > 0.0);
    gate(
        report,
        "huge_mass_ratio_causality",
        passed,
        "μ 1e9→2e9: r=4 is compact and refused; far r=1e6 still has zero pre-cone influence and nonzero post-cone influence.",
    );
}

fn record_moving(report: &mut CandidateReport) {
    let baseline = CausalKernel::new(
        vec![tube(1, vec![genesis(origin(), q(1, 1))])],
        finite_root(),
    )
    .expect("static");
    let moving = CausalKernel::new(
        vec![tube(
            1,
            vec![
                genesis(origin(), q(1, 1)),
                SourceSegment {
                    since: Q::zero(),
                    position: [q(1, 1), Q::zero()],
                    mu: q(1, 1),
                },
            ],
        )],
        finite_root(),
    );
    let Ok(moving) = moving else {
        gate(
            report,
            "moving_source_retarded_position",
            false,
            "moving history rejected",
        );
        return;
    };
    let pre_event = KernelEvent {
        time: q(1, 64),
        position: r4(),
    };
    let post_event = KernelEvent {
        time: q(1, 8),
        position: r4(),
    };
    let passed = match (
        moving.acceleration_at(pre_event),
        baseline.acceleration_at(pre_event),
        moving.acceleration_at(post_event),
        baseline.acceleration_at(post_event),
    ) {
        (Ok(pre_m), Ok(pre_b), Ok(post_m), Ok(post_b)) => {
            influence(pre_m, pre_b) <= 0.0 && influence(post_m, post_b) > 0.0
        }
        _ => false,
    };
    gate(
        report,
        "moving_source_retarded_position",
        passed,
        "Source jumps (0,0)→(1,0) at t=0 with subluminal separation from genesis. Query (4,0) uses retarded position, not present position, until the new cone arrives.",
    );
}

fn record_exterior(report: &mut CandidateReport) {
    let baseline = CausalKernel::new(vec![], finite_root()).expect("empty root");
    let appearing = CausalKernel::new(
        vec![tube(
            7,
            vec![SourceSegment {
                since: Q::zero(),
                position: [q(16, 1), Q::zero()],
                mu: q(1, 1),
            }],
        )],
        finite_root(),
    )
    .expect("exterior source");
    let query = [q(1, 1), Q::zero()];
    let pre = KernelEvent {
        time: q(15, 256),
        position: query,
    };
    let post = KernelEvent {
        time: q(15, 32),
        position: query,
    };
    let passed = match (
        appearing.acceleration_at(pre),
        baseline.acceleration_at(pre),
        appearing.acceleration_at(post),
        baseline.acceleration_at(post),
    ) {
        (Ok(a), Ok(b), Ok(c), Ok(d)) => influence(a, b) <= 0.0 && influence(c, d) > 0.0,
        _ => false,
    };
    gate(
        report,
        "exterior_source_light_cone",
        passed,
        "Unit source at r=16, query r=1: pre t=15/256 no influence, post t=15/32 influence. Listing it is still not a certified infinite exterior.",
    );
}

fn record_simultaneous(report: &mut CandidateReport) {
    let a = [Q::zero(), Q::zero()];
    let b = [q(8, 1), Q::zero()];
    let query = [q(1, 1), Q::zero()];
    let baseline = CausalKernel::new(
        vec![
            tube(1, vec![genesis(a, q(1, 1))]),
            tube(2, vec![genesis(b, q(1, 1))]),
        ],
        finite_root(),
    )
    .expect("two sources");
    let changed = CausalKernel::new(
        vec![
            tube(
                1,
                vec![
                    genesis(a, q(1, 1)),
                    SourceSegment {
                        since: Q::zero(),
                        position: a,
                        mu: q(2, 1),
                    },
                ],
            ),
            tube(
                2,
                vec![
                    genesis(b, q(1, 1)),
                    SourceSegment {
                        since: Q::zero(),
                        position: b,
                        mu: q(2, 1),
                    },
                ],
            ),
        ],
        finite_root(),
    )
    .expect("simultaneous changes");
    let only_a = CausalKernel::new(
        vec![
            tube(
                1,
                vec![
                    genesis(a, q(1, 1)),
                    SourceSegment {
                        since: Q::zero(),
                        position: a,
                        mu: q(2, 1),
                    },
                ],
            ),
            tube(2, vec![genesis(b, q(1, 1))]),
        ],
        finite_root(),
    )
    .expect("only A");
    let infl = |k: &CausalKernel, t: Q| {
        let event = KernelEvent {
            time: t,
            position: query,
        };
        influence(
            k.acceleration_at(event).unwrap(),
            baseline.acceleration_at(event).unwrap(),
        )
    };
    let neither = infl(&changed, q(1, 256));
    let mid = infl(&changed, q(1, 32));
    let only = infl(&only_a, q(1, 32));
    let both = infl(&changed, q(1, 4));
    let both_only_a = infl(&only_a, q(1, 4));
    let passed = neither <= 0.0
        && (mid - only).abs() <= 1e-15
        && only > 0.0
        && both > 0.0
        && (both - both_only_a).abs() > 0.0;
    gate(
        report,
        "simultaneous_source_cones",
        passed,
        "Two sources change at the same t=0. Query (1,0) sees neither, then only the nearer change, then both. Simultaneous emission is not simultaneous reception.",
    );
}

fn record_static_newton_limit(report: &mut CandidateReport) {
    let kernel = CausalKernel::new(
        vec![tube(1, vec![genesis(origin(), q(1, 1))])],
        finite_root(),
    )
    .expect("static");
    let query = KernelEvent {
        time: q(1, 1),
        position: r4(),
    };
    let retarded = kernel.acceleration_at(query).expect("far static");
    let newton = gravitational_acceleration([4.0, 0.0], 1.0).expect("newton");
    let error = influence(retarded, newton);
    push_metric(
        report,
        "static_limit",
        "retarded_vs_newton",
        error,
        "acceleration",
        0.0,
        error <= 0.0,
    );
    gate(
        report,
        "static_limit_matches_newton",
        error <= 0.0,
        "Eternal static sources must reproduce the 3D-planar Newton query. Causality is about changes, not a different static kernel.",
    );
}

fn record_superluminal_rejection(report: &mut CandidateReport) {
    let result = CausalKernel::new(
        vec![tube(
            1,
            vec![
                SourceSegment {
                    since: Q::zero(),
                    position: origin(),
                    mu: q(1, 1),
                },
                SourceSegment {
                    since: q(1, 64),
                    position: r4(),
                    mu: q(1, 1),
                },
            ],
        )],
        finite_root(),
    );
    gate(
        report,
        "superluminal_history_rejected",
        matches!(result, Err(KernelError::SuperluminalHistory { id: 1 })),
        "A source that moves Δr=4 in Δt=1/64 is superluminal and is not a valid worldtube.",
    );
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn research_law_is_not_the_inertial_laboratory() {
        assert_ne!(RESEARCH_LAW_ID, INERTIAL_LAB_LAW_ID);
        research_manifest().unwrap();
    }

    #[test]
    fn instantaneous_newton_fails_the_first_gate() {
        let before = gravitational_acceleration([4.0, 0.0], 1.0).unwrap();
        let after = gravitational_acceleration([4.0, 0.0], 2.0).unwrap();
        let response = crate::norm(crate::sub(after, before));
        let result = instantaneous_two_sided(response, 0.0);
        assert!(!result.pre_passed);
        assert!(result.post_passed);
        assert!(!result.passed);
        assert_eq!(response, 0.0625);
    }

    #[test]
    fn retarded_mass_change_is_two_sided() {
        let pre = mass_change_influence(origin(), r4(), q(1, 1), q(2, 1), q(1, 64)).unwrap();
        let post = mass_change_influence(origin(), r4(), q(1, 1), q(2, 1), q(1, 8)).unwrap();
        let on = mass_change_influence(origin(), r4(), q(1, 1), q(2, 1), q(1, 16)).unwrap();
        assert_eq!(pre, 0.0);
        assert!(post > 0.0);
        assert!(on > 0.0);
        assert!(two_sided_result(pre, post, 0.0, 0.0).passed);
    }

    #[test]
    fn always_zero_kernel_fails_post_cone() {
        assert!(!two_sided_result(0.0, 0.0, 0.0, 0.0).passed);
    }

    #[test]
    fn compact_is_refused_and_far_is_not() {
        let kernel = CausalKernel::new(
            vec![tube(1, vec![genesis(origin(), q(1, 1))])],
            finite_root(),
        )
        .unwrap();
        assert!(matches!(
            kernel.acceleration_at(KernelEvent {
                time: q(1, 1),
                position: [q(1, 2048), Q::zero()],
            }),
            Err(KernelError::CompactForbidden { id: 1 })
        ));
        assert!(kernel
            .acceleration_at(KernelEvent {
                time: q(1, 1),
                position: r4(),
            })
            .is_ok());
    }

    #[test]
    fn moving_source_ignores_present_position_before_cone() {
        let moving = CausalKernel::new(
            vec![tube(
                1,
                vec![
                    genesis(origin(), q(1, 1)),
                    SourceSegment {
                        since: Q::zero(),
                        position: [q(1, 1), Q::zero()],
                        mu: q(1, 1),
                    },
                ],
            )],
            finite_root(),
        )
        .unwrap();
        let query = KernelEvent {
            time: q(1, 64),
            position: r4(),
        };
        let retarded = moving.acceleration_at(query).unwrap();
        let present = gravitational_acceleration([3.0, 0.0], 1.0).unwrap();
        let old = gravitational_acceleration([4.0, 0.0], 1.0).unwrap();
        assert_eq!(retarded, old);
        assert_ne!(retarded, present);
    }

    #[test]
    fn superluminal_history_is_rejected() {
        let err = CausalKernel::new(
            vec![tube(
                1,
                vec![
                    SourceSegment {
                        since: Q::zero(),
                        position: origin(),
                        mu: q(1, 1),
                    },
                    SourceSegment {
                        since: q(1, 64),
                        position: r4(),
                        mu: q(1, 1),
                    },
                ],
            )],
            finite_root(),
        )
        .unwrap_err();
        assert_eq!(err, KernelError::SuperluminalHistory { id: 1 });
    }

    #[test]
    fn simultaneous_changes_arrive_on_their_own_cones() {
        let report = qualify_research_kernel();
        assert!(
            report
                .gates
                .iter()
                .find(|g| g.id == "simultaneous_source_cones")
                .unwrap()
                .passed
        );
        assert!(
            report
                .gates
                .iter()
                .find(|g| g.id == "moving_source_retarded_position")
                .unwrap()
                .passed
        );
        assert!(
            report
                .gates
                .iter()
                .find(|g| g.id == "huge_mass_ratio_causality")
                .unwrap()
                .passed
        );
        assert!(
            report
                .gates
                .iter()
                .find(|g| g.id == "exterior_source_light_cone")
                .unwrap()
                .passed
        );
        assert!(
            report
                .gates
                .iter()
                .find(|g| g.id == "compact_vs_far_domain")
                .unwrap()
                .passed
        );
    }

    #[test]
    fn research_kernel_does_not_promote() {
        let report = qualify_research_kernel();
        assert_eq!(report.id, RESEARCH_LAW_ID);
        assert_eq!(report.status, "FAIL");
        let first = report
            .gates
            .iter()
            .find(|g| g.id == "source_change_light_cone")
            .unwrap();
        assert!(first.passed);
        assert!(
            report
                .gates
                .iter()
                .find(|g| g.id == "well_posed_exterior")
                .unwrap()
                .passed
        );
        for id in [
            "incomplete_omit_r16",
            "false_complete_omit_r16",
            "unsound_tail_bound_r16",
            "certified_tail_bound_r16",
            "query_in_omitted_tail",
            "listed_r16_complete",
            "exact_compact_membership",
            "interior_capture_not_newton",
            "on_horizon_capture",
            "coincidence_singular_not_nan",
            "causal_compact_after_cone",
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
                "{id} must pass the two-sided exterior, compact, or terminating-branch contract"
            );
        }
        for id in [
            "orbit_stability",
            "compact_field_certification",
            "terminating_exact_branches",
            "source_backreaction",
            "retarded_two_way_backreaction",
        ] {
            assert!(
                !report.gates.iter().find(|g| g.id == id).unwrap().passed,
                "{id} must remain failed"
            );
        }
        assert!(
            report
                .gates
                .iter()
                .find(|g| g.id == "causal_dynamic_sources")
                .unwrap()
                .passed
        );
    }

    #[test]
    fn authored_worldtubes_fail_two_way_backreaction() {
        let result = authored_trajectory_two_sided().unwrap();
        assert!(result.pre_passed);
        assert!(!result.post_passed);
        assert!(!result.passed);
        assert_eq!(result.post_influence, 0.0);
    }

    #[test]
    fn self_query_without_exclude_is_singular() {
        let kernel = CausalKernel::new(
            vec![tube(1, vec![genesis(origin(), q(1, 1))])],
            finite_root(),
        )
        .unwrap();
        let at_self = KernelEvent {
            time: q(1, 1),
            position: origin(),
        };
        assert!(matches!(
            kernel.acceleration_at(at_self),
            Err(KernelError::Singular { id: 1 })
        ));
        assert_eq!(
            kernel.acceleration_at_excluding(at_self, Some(1)).unwrap(),
            [0.0, 0.0]
        );
    }

    #[test]
    fn incomplete_root_fails_certified_query_closed() {
        let kernel = CausalKernel::new(vec![], finite_root()).unwrap();
        let query = KernelEvent {
            time: q(1, 1),
            position: [q(1, 1), Q::zero()],
        };
        assert_eq!(kernel.acceleration_at(query).unwrap(), [0.0, 0.0]);
        assert_eq!(
            kernel.certified_acceleration_at(query).unwrap_err(),
            KernelError::UncertifiedExterior
        );
        let unspecified = CausalKernel::new(vec![], ExteriorModel::Unspecified).unwrap();
        assert_eq!(
            unspecified.certified_acceleration_at(query).unwrap_err(),
            KernelError::UncertifiedExterior
        );
    }

    #[test]
    fn sound_tail_bound_encloses_omitted_r16() {
        let kernel = CausalKernel::new(
            vec![],
            ExteriorModel::FiniteAuthoritativeRoot {
                support_radius: q(8, 1),
                declared_complete: true,
                omitted_tail: Some(OmittedTailBound {
                    exterior_radius: q(16, 1),
                    mu_bound: q(1, 1),
                }),
            },
        )
        .unwrap();
        let query = KernelEvent {
            time: q(1, 1),
            position: [q(1, 1), Q::zero()],
        };
        let certified = kernel.certified_acceleration_at(query).unwrap();
        let actual = gravitational_acceleration([-15.0, 0.0], 1.0)
            .map(norm)
            .unwrap();
        assert_eq!(certified.listed, [0.0, 0.0]);
        assert!(actual <= certified.omitted_tail_bound);
        assert!(certified.omitted_tail_bound >= 1.0 / 225.0);
        assert!((actual - 1.0 / 225.0).abs() <= 1e-15);
    }

    #[test]
    fn unsound_tail_bound_is_violated_by_omitted_r16() {
        let kernel = CausalKernel::new(
            vec![],
            ExteriorModel::FiniteAuthoritativeRoot {
                support_radius: q(8, 1),
                declared_complete: true,
                omitted_tail: Some(OmittedTailBound {
                    exterior_radius: q(32, 1),
                    mu_bound: q(1, 1),
                }),
            },
        )
        .unwrap();
        let query = KernelEvent {
            time: q(1, 1),
            position: [q(1, 1), Q::zero()],
        };
        let certified = kernel.certified_acceleration_at(query).unwrap();
        let actual = gravitational_acceleration([-15.0, 0.0], 1.0)
            .map(norm)
            .unwrap();
        assert!(actual > certified.omitted_tail_bound);
    }

    #[test]
    fn query_in_omitted_region_fails_closed() {
        let kernel = CausalKernel::new(
            vec![],
            ExteriorModel::FiniteAuthoritativeRoot {
                support_radius: q(8, 1),
                declared_complete: true,
                omitted_tail: Some(OmittedTailBound {
                    exterior_radius: q(16, 1),
                    mu_bound: q(1, 1),
                }),
            },
        )
        .unwrap();
        let query = KernelEvent {
            time: q(1, 1),
            position: [q(16, 1), Q::zero()],
        };
        assert_eq!(
            kernel.certified_acceleration_at(query).unwrap_err(),
            KernelError::ExteriorResourceLimit
        );
    }
}
