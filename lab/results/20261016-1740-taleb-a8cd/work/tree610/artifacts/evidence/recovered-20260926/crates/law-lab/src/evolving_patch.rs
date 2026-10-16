//! Evolving spacetime-patch laboratory map.
//!
//! Law id: `es-evolving-spacetime-patch-v0`. One compiled metric object in
//! `P`: two massive bodies, one test ship (`μ = 0`), one light ray, one clock.
//! Laboratory `P.ray` is the spec post-cone emit (`t = 1/8`, ship → receiver),
//! stored scheduled at genesis (`tick_delivery = None`). `U` does not fly it
//! until `live.time >= emit_time`; after emit it refreshes in-flight GEO-N
//! from the step's `g` and commits delivery only on the containing tick
//! (arrival ≈ `3/16`). `bind_observables` stamps `geometry_id` only; flown
//! `dt` is written solely by `U`. CONSIS reads two-sided stored `P.ray`.
//! Cached `U` certifies ship / in-flight emit / GEO-N path samples, not a
//! source's self-cone. GEM (METRIC)/(GEM-a)/(CLK) may fill `g`. GEM (SIG)
//! Minkowski is a named negative control. GEM (MAP) is not this object;
//! `advance_map` is not implemented here.
//!
//! Fixtures were frozen before this map. Do not retune. Do not freeze a
//! Shapiro magnitude. G2 stays FAIL. `production_law` stays null.

use super::causal_kernel::{
    compact_map, in_closed_past_cone, influence, q, qf, qf_pair, CompactClass, CompactMap,
    KernelEvent, OmittedTailBound, SourceSegment, C, GENESIS, INERTIAL_LAB_LAW_ID,
    POST_LIGHTCONE_INFLUENCE_MIN, RESEARCH_LAW_ID,
};
use super::coupled::COUPLED_LAW_ID;
use super::probe_counters;
use super::schwarzschild::SCHWARZSCHILD_LAW_ID;
use super::tiny_causal::{advance_map, GEM_LAW_ID};
use super::{gate, gravitational_acceleration, CandidateReport};
use num_rational::Ratio;
use num_traits::Zero;
use serde::Deserialize;

pub const PATCH_LAW_ID: &str = "es-evolving-spacetime-patch-v0";
const POSITION_DENOM: i128 = 1 << 20;
const MASSIVE_BODIES: usize = 2;
const TEST_BODIES: usize = 1;
const LIGHT_RAYS: usize = 1;
const CLOCKS: usize = 1;
const CLOCK_FRACTIONAL_BITS: i128 = 32;
const CLOCK_SCALE: i128 = 1 << 32;
const CONSIS_OBJECT: &str = "compiled_g_or_phi_xi";
const CONSIS_BINDING: &str = "geo-t-geo-n-clk-g-from-p";
const CONSIS_COMOVEMENT: &str = "necessary-not-sufficient";
const PRIVATE_PHI_TRIO: &str = "fails";
const GEO_N_DISCRIMINATOR: &str = "coordinate-affine-arrival";
const GEO_N_TICK_BINNING: &str = "commit-not-falsifier";
const SHAPIRO_MAGNITUDE: &str = "not-frozen";
const CERTIFICATE: &str = "source-digest-remainder-future-cone";
const CERTIFICATE_SCOPE: &str = "per-event";
const SHIP_OLD_G_DEADLINE: [i128; 2] = [1, 16];
const CACHE_KEY: &str = "source-history-digest";
const CACHE_AFTER_INV: &str = "fail";
const GEM_MAY_FILL: [&str; 3] = ["METRIC", "GEM-a", "CLK"];
const MINKOWSKI_FLIGHT: [i128; 2] = [1, 16];
const MAP_STATUS: &str = "implemented-research";
const ID_A: u64 = 1;
const ID_B: u64 = 2;
const ID_SHIP: u64 = 10;
const NULL_PATH_SAMPLES: u32 = 64;
const MINKOWSKI_GEOMETRY_ID: u64 = 0;
const UNFLOWN_COORDINATE_DT: f64 = 0.0;

pub const NAMED_EQUATIONS: [&str; 13] = [
    "PATCH-S",
    "PATCH-DOM",
    "PATCH-INV",
    "PATCH-PROP",
    "GEO-T",
    "GEO-N",
    "CLK-G",
    "EXT-P",
    "BR-P",
    "CONSIS",
    "BACKREACT",
    "COMPOSE",
    "CACHE",
];

pub const EVOLVING_PATCH_FIXTURE_IDS: [&str; 17] = [
    "two_source_one_ship_one_ray_one_clock",
    "source_change_moves_ship",
    "source_change_delays_light",
    "source_change_shifts_clock",
    "same_metric_consistency",
    "direct_vs_subdivided_patch",
    "cache_reuse_matches",
    "source_change_invalidates_certificate",
    "remainder_in_patch_state",
    "unsupported_third_massive_refuses",
    "budget_exhausted_not_a_geodesic",
    "inertial_clock_when_phi_zero",
    "observation_does_not_recompile",
    "minkowski_signal_not_metric_null",
    "delayed_newton_not_the_patch",
    "schwarzschild_classifier_not_evolving_patch",
    "gem_force_without_null_geodesic_fails_consistency",
];

const MANIFEST: &str = include_str!("../../../scenarios/law-gates.json");

type Q = super::causal_kernel::Q;

#[derive(Clone, Deserialize)]
struct FileSlice {
    aggregate_gates: FrozenAggregates,
    required_production_gates: Vec<String>,
    tiny_causal_law_research: GemSlice,
    evolving_spacetime_patch_research: PatchManifest,
}

#[derive(Clone, Deserialize)]
struct FrozenAggregates {
    pre_lightcone_response_max: f64,
    backreaction_relative_error_max: f64,
}

#[derive(Clone, Deserialize)]
struct GemSlice {
    present_alignment_dot_min: [i128; 2],
}

#[derive(Clone, Deserialize)]
struct PatchManifest {
    law_id: String,
    status: String,
    spec: String,
    map_status: String,
    shared_object: String,
    candidate_metric: String,
    parent_kernel: String,
    coupled_kernel: String,
    schwarzschild_kernel: String,
    gem_kernel: String,
    light_speed: i128,
    massive_bodies: usize,
    test_bodies: usize,
    light_rays: usize,
    clocks: usize,
    step: [i128; 2],
    position_denom: i128,
    clock_fractional_bits: i128,
    pre_lightcone_response_max: f64,
    post_lightcone_influence_min: f64,
    post_lightcone_influence_strict: bool,
    authored_futures: bool,
    consis_object: String,
    consis_binding: String,
    consis_comovement: String,
    private_phi_trio: String,
    geo_n_discriminator: String,
    geo_n_tick_binning: String,
    shapiro_magnitude: String,
    delay_strict_gt_minkowski: bool,
    delay_ne_baseline: bool,
    certificate: String,
    certificate_scope: String,
    ship_old_g_deadline: [i128; 2],
    cache_key: String,
    cache_after_inv: String,
    gem_map_is_this_object: bool,
    gem_may_fill: Vec<String>,
    named_equations: Vec<String>,
    fixtures: Vec<NamedFixture>,
}

#[derive(Clone, Deserialize)]
struct NamedFixture {
    id: String,
    #[serde(default)]
    kind: String,
    #[serde(default)]
    authored_futures: Option<bool>,
    #[serde(default)]
    consis_object: Option<String>,
    #[serde(default)]
    consis_binding: Option<String>,
    #[serde(default)]
    consis_comovement: Option<String>,
    #[serde(default)]
    private_phi_trio: Option<String>,
    #[serde(default)]
    discriminator: Option<String>,
    #[serde(default)]
    tick_binning: Option<String>,
    #[serde(default)]
    require_delay_gt_minkowski: Option<bool>,
    #[serde(default)]
    require_delay_ne_baseline: Option<bool>,
    #[serde(default)]
    shapiro_magnitude: Option<String>,
    #[serde(default)]
    minkowski_flight: Option<[i128; 2]>,
    #[serde(default)]
    certificate: Option<String>,
    #[serde(default)]
    certificate_scope: Option<String>,
    #[serde(default)]
    not_global_ttl: Option<bool>,
    #[serde(default)]
    ship_must_not_see_old_g_at: Option<[i128; 2]>,
    #[serde(default)]
    cache_key: Option<String>,
    #[serde(default)]
    cache_after_inv: Option<String>,
    #[serde(default)]
    gem_map_is_this_object: Option<bool>,
    #[serde(default)]
    gem_may_fill: Option<Vec<String>>,
}

/// GEM fill of the compiled patch metric: `g` from `(Φ, ξ)` at an event.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct PhiXi {
    pub phi: f64,
    pub xi: [f64; 2],
    pub e: [f64; 2],
    pub b: f64,
}

#[derive(Clone, Debug, PartialEq)]
pub struct PatchSegment {
    pub since: Q,
    pub position: [Q; 2],
    pub velocity: [f64; 2],
    pub mu: Q,
}

#[derive(Clone, Debug, PartialEq)]
pub struct PatchSource {
    pub id: u64,
    pub segments: Vec<PatchSegment>,
}

/// The one object in `P` that (GEO-T)/(GEO-N)/(CLK-G) read.
#[derive(Clone, Debug, PartialEq)]
pub struct CompiledGeometry {
    pub id: u64,
    sources: Vec<PatchSource>,
    remainder: OmittedTailBound,
    changes: Vec<KernelEvent>,
}

#[derive(Clone, Debug, PartialEq)]
pub struct Certificate {
    pub source_digest: u64,
    pub remainder: OmittedTailBound,
    pub changes: Vec<KernelEvent>,
}

#[derive(Clone, Debug, PartialEq)]
pub struct TestBody {
    pub id: u64,
    pub position: [Q; 2],
    pub velocity: [f64; 2],
    pub mu: Q,
    pub geometry_id: u64,
    pub captured: Option<(u64, CompactClass)>,
    pub worldtube: Vec<PatchSegment>,
}

#[derive(Clone, Debug, PartialEq)]
pub struct NullRay {
    pub emit_time: Q,
    pub emit_position: [Q; 2],
    pub receiver: [Q; 2],
    pub coordinate_dt: f64,
    pub affine_arrival: f64,
    pub tick_delivery: Option<Q>,
    pub geometry_id: u64,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Clock {
    pub tau: Q,
    pub geometry_id: u64,
}

#[derive(Clone, Debug, PartialEq)]
pub struct PatchState {
    pub time: Q,
    pub sources: Vec<PatchSource>,
    pub geometry: CompiledGeometry,
    pub ship: TestBody,
    pub ray: Option<NullRay>,
    pub clock: Clock,
    pub remainder: OmittedTailBound,
    pub certificate: Certificate,
    pub ledger: Vec<(Q, u64, [f64; 2])>,
}

#[derive(Clone, Debug, PartialEq)]
pub struct PatchCache {
    pub digest: u64,
    pub remainder: OmittedTailBound,
    pub geometry: CompiledGeometry,
    pub changes: Vec<KernelEvent>,
}

/// Three Φ-responsive formulas that co-move without sharing `g` in `P`.
#[derive(Clone, Copy, Debug)]
pub struct PrivatePhiTrio {
    pub ship_accel: [f64; 2],
    pub light_dt: f64,
    pub clock_rate: f64,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum EvolvingPatchError {
    CastRefused(&'static str),
    AuthoredFutures,
    UnsupportedPredicate(&'static str),
    BranchBudgetExhausted { max_steps: u32 },
    CacheAfterInvalidation,
    Singular,
    Superluminal,
    UncertifiedExterior,
    ClockSpacelike,
    Nonfinite,
    Invalid(&'static str),
}

impl std::fmt::Display for EvolvingPatchError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::CastRefused(reason) => write!(f, "cast refused: {reason}"),
            Self::AuthoredFutures => f.write_str("authored future worldtubes are not state"),
            Self::UnsupportedPredicate(name) => write!(f, "unsupported predicate {name}"),
            Self::BranchBudgetExhausted { max_steps } => write!(
                f,
                "branch budget of {max_steps} steps exhausted; no guessed geodesic sign accepted"
            ),
            Self::CacheAfterInvalidation => {
                f.write_str("cache hit after PATCH-INV; per-event certificate is dead")
            }
            Self::Singular => f.write_str("coincidence r=0 is singular"),
            Self::Superluminal => f.write_str("superluminal worldtube refused"),
            Self::UncertifiedExterior => {
                f.write_str("incomplete omit without a remainder fails closed")
            }
            Self::ClockSpacelike => f.write_str("clock argument is spacelike/compact"),
            Self::Nonfinite => f.write_str("nonfinite field value cannot classify a branch"),
            Self::Invalid(reason) => f.write_str(reason),
        }
    }
}

/// Admitted laboratory tick. Equal to `1/c` with laboratory `c = 64`.
pub fn dt_q() -> Q {
    q(1, C)
}

fn dt_f() -> f64 {
    1.0 / C as f64
}

fn c_f() -> f64 {
    C as f64
}

fn is_tick(t: Q) -> bool {
    *(t * Q::from_integer(C)).denom() == 1
}

fn round_q(x: f64) -> Result<Q, EvolvingPatchError> {
    if !x.is_finite() {
        return Err(EvolvingPatchError::Nonfinite);
    }
    Ok(Ratio::new(
        (x * POSITION_DENOM as f64).round() as i128,
        POSITION_DENOM,
    ))
}

fn frozen_remainder() -> OmittedTailBound {
    OmittedTailBound {
        exterior_radius: q(16, 1),
        mu_bound: q(1, 1),
    }
}

fn ship_event(time: Q) -> KernelEvent {
    KernelEvent {
        time,
        position: [q(4, 1), Q::zero()],
    }
}

fn receiver_pos() -> [Q; 2] {
    [q(4, 1), q(4, 1)]
}

fn pre_emit() -> KernelEvent {
    KernelEvent {
        time: q(-1, 1),
        position: [q(4, 1), Q::zero()],
    }
}

fn post_emit() -> KernelEvent {
    KernelEvent {
        time: q(1, 8),
        position: [q(4, 1), Q::zero()],
    }
}

fn minkowski_flight() -> f64 {
    4.0 / c_f()
}

fn source_digest(sources: &[PatchSource], remainder: &OmittedTailBound) -> u64 {
    let mut hasher = blake3::Hasher::new();
    probe_counters::with(|c| {
        c.digest_calls += 1;
        // 8 B/source id + 144 B/segment + 64 B remainder, matching the
        // hasher.update sequence below.
        let entries: u64 = sources.iter().map(|s| s.segments.len() as u64).sum();
        c.digest_bytes += 8 * sources.len() as u64 + 144 * entries + 64;
    });
    for source in sources {
        hasher.update(&source.id.to_le_bytes());
        for seg in &source.segments {
            hasher.update(&seg.since.numer().to_le_bytes());
            hasher.update(&seg.since.denom().to_le_bytes());
            hasher.update(&seg.position[0].numer().to_le_bytes());
            hasher.update(&seg.position[0].denom().to_le_bytes());
            hasher.update(&seg.position[1].numer().to_le_bytes());
            hasher.update(&seg.position[1].denom().to_le_bytes());
            hasher.update(&seg.velocity[0].to_le_bytes());
            hasher.update(&seg.velocity[1].to_le_bytes());
            hasher.update(&seg.mu.numer().to_le_bytes());
            hasher.update(&seg.mu.denom().to_le_bytes());
        }
    }
    hasher.update(&remainder.exterior_radius.numer().to_le_bytes());
    hasher.update(&remainder.exterior_radius.denom().to_le_bytes());
    hasher.update(&remainder.mu_bound.numer().to_le_bytes());
    hasher.update(&remainder.mu_bound.denom().to_le_bytes());
    let hash = hasher.finalize();
    u64::from_le_bytes(hash.as_bytes()[..8].try_into().expect("blake3 is 32 bytes"))
}

fn last_segment(source: &PatchSource) -> Result<&PatchSegment, EvolvingPatchError> {
    source.segments.last().ok_or(EvolvingPatchError::Invalid(
        "source worldtube has no segments",
    ))
}

fn segment_visible(seg: &PatchSegment, query: KernelEvent) -> bool {
    probe_counters::with(|c| c.cone_checks += 1);
    in_closed_past_cone(
        KernelEvent {
            time: seg.since,
            position: seg.position,
        },
        query,
        C,
    )
}

fn gem_contrib(mu: f64, r_vec: [f64; 2], velocity: [f64; 2]) -> Result<PhiXi, EvolvingPatchError> {
    probe_counters::with(|c| c.gem_contrib_calls += 1);
    let c = c_f();
    let r2 = r_vec[0] * r_vec[0] + r_vec[1] * r_vec[1];
    if r2 == 0.0 {
        return Err(EvolvingPatchError::Singular);
    }
    if !r2.is_finite() || !mu.is_finite() {
        return Err(EvolvingPatchError::Nonfinite);
    }
    let r = r2.sqrt();
    let n = [r_vec[0] / r, r_vec[1] / r];
    let beta = [velocity[0] / c, velocity[1] / c];
    let beta2 = beta[0] * beta[0] + beta[1] * beta[1];
    if beta2 >= 1.0 {
        return Err(EvolvingPatchError::Superluminal);
    }
    let n_dot_b = n[0] * beta[0] + n[1] * beta[1];
    let kappa = 1.0 - n_dot_b;
    if kappa <= 0.0 || !kappa.is_finite() {
        return Err(EvolvingPatchError::Nonfinite);
    }
    let d = r * kappa;
    let phi = -mu / d;
    let xi = [phi * beta[0], phi * beta[1]];
    let coef = mu / (d * d);
    let fac = (1.0 - beta2) / kappa;
    let grad = [
        coef * (-beta[0] + n[0] * fac),
        coef * (-beta[1] + n[1] * fac),
    ];
    let dphi_dt = (mu * c / (d * d * kappa)) * (beta2 - n_dot_b);
    let dxi_dt = [beta[0] * dphi_dt, beta[1] * dphi_dt];
    let e = [
        -grad[0] - (4.0 / c) * dxi_dt[0],
        -grad[1] - (4.0 / c) * dxi_dt[1],
    ];
    let curl_z = coef * fac * (n[0] * beta[1] - n[1] * beta[0]);
    let b = (4.0 / c) * curl_z;
    if ![phi, xi[0], xi[1], e[0], e[1], b]
        .into_iter()
        .all(f64::is_finite)
    {
        return Err(EvolvingPatchError::Nonfinite);
    }
    Ok(PhiXi { phi, xi, e, b })
}

impl CompiledGeometry {
    fn compile(
        sources: Vec<PatchSource>,
        remainder: OmittedTailBound,
        changes: Vec<KernelEvent>,
    ) -> Self {
        let id = source_digest(&sources, &remainder);
        Self {
            id,
            sources,
            remainder,
            changes,
        }
    }

    /// GEM (METRIC) fill at `event`. Test bodies are excluded-self by not sourcing.
    pub fn phi_xi(
        &self,
        event: KernelEvent,
        exclude: Option<u64>,
    ) -> Result<PhiXi, EvolvingPatchError> {
        probe_counters::with(|c| c.phi_xi_calls += 1);
        let mut sum = PhiXi {
            phi: 0.0,
            xi: [0.0, 0.0],
            e: [0.0, 0.0],
            b: 0.0,
        };
        for source in &self.sources {
            probe_counters::with(|c| c.phi_xi_source_visits += 1);
            if exclude == Some(source.id) {
                continue;
            }
            let Some(seg) = source
                .segments
                .iter()
                .rev()
                .find(|seg| segment_visible(seg, event))
            else {
                continue;
            };
            let kernel_seg = SourceSegment {
                since: seg.since,
                position: seg.position,
                mu: seg.mu,
            };
            probe_counters::with(|c| c.compact_map_calls += 1);
            match compact_map(kernel_seg, event, C) {
                CompactMap::Singular => return Err(EvolvingPatchError::Singular),
                CompactMap::Captured { .. } => {
                    return Err(EvolvingPatchError::Invalid(
                        "compact capture is not a weak-field fill",
                    ));
                }
                CompactMap::Exterior => {}
            }
            if seg.mu.is_zero() {
                continue;
            }
            let tq = qf(event.time);
            let t0 = qf(seg.since);
            let x0 = qf_pair(seg.position);
            let dt = (tq - t0).max(0.0);
            let x_ret = [x0[0] + seg.velocity[0] * dt, x0[1] + seg.velocity[1] * dt];
            let query = qf_pair(event.position);
            let r_vec = [query[0] - x_ret[0], query[1] - x_ret[1]];
            let part = gem_contrib(qf(seg.mu), r_vec, seg.velocity)?;
            sum.phi += part.phi;
            sum.xi[0] += part.xi[0];
            sum.xi[1] += part.xi[1];
            sum.e[0] += part.e[0];
            sum.e[1] += part.e[1];
            sum.b += part.b;
        }
        Ok(sum)
    }

    /// Read access for the amortized evaluator's incremental frontiers.
    pub(crate) fn sources(&self) -> &[PatchSource] {
        &self.sources
    }

    /// Append one committed segment in lockstep with `PatchState::sources`
    /// without rebuilding the container or re-hashing history.
    pub(crate) fn push_segment(&mut self, id: u64, seg: PatchSegment) {
        if let Some(source) = self.sources.iter_mut().find(|s| s.id == id) {
            source.segments.push(seg);
        }
    }

    fn capture_at(
        &self,
        event: KernelEvent,
        exclude: Option<u64>,
    ) -> Result<Option<(u64, CompactClass)>, EvolvingPatchError> {
        probe_counters::with(|c| c.capture_calls += 1);
        for source in &self.sources {
            if exclude == Some(source.id) {
                continue;
            }
            let Some(seg) = source
                .segments
                .iter()
                .rev()
                .find(|seg| segment_visible(seg, event))
            else {
                continue;
            };
            let kernel_seg = SourceSegment {
                since: seg.since,
                position: seg.position,
                mu: seg.mu,
            };
            probe_counters::with(|c| c.compact_map_calls += 1);
            match compact_map(kernel_seg, event, C) {
                CompactMap::Singular => return Err(EvolvingPatchError::Singular),
                CompactMap::Captured { class } => return Ok(Some((source.id, class))),
                CompactMap::Exterior => {}
            }
        }
        Ok(None)
    }
}

fn vacuum_geometry() -> CompiledGeometry {
    CompiledGeometry {
        id: MINKOWSKI_GEOMETRY_ID,
        sources: Vec::new(),
        remainder: frozen_remainder(),
        changes: Vec::new(),
    }
}

/// (GEO-T) linearized geodesic acceleration from the compiled fill.
pub fn geo_t_accel(
    g: &CompiledGeometry,
    event: KernelEvent,
    velocity: [f64; 2],
    max_steps: u32,
) -> Result<[f64; 2], EvolvingPatchError> {
    if max_steps == 0 {
        return Err(EvolvingPatchError::BranchBudgetExhausted { max_steps: 0 });
    }
    if g.capture_at(event, None)?.is_some() {
        return Ok([0.0, 0.0]);
    }
    let field = g.phi_xi(event, None)?;
    Ok([
        field.e[0] + velocity[1] * field.b,
        field.e[1] - velocity[0] * field.b,
    ])
}

/// Path samples `geo_n_arrival` integrates. Cached `U` certifies these events,
/// not a source's own change event.
fn null_path_samples(
    emit: KernelEvent,
    receiver: [Q; 2],
    max_steps: u32,
) -> Result<Vec<(KernelEvent, f64, [f64; 2])>, EvolvingPatchError> {
    if max_steps == 0 {
        return Err(EvolvingPatchError::BranchBudgetExhausted { max_steps: 0 });
    }
    let x0 = qf_pair(emit.position);
    let x1 = qf_pair(receiver);
    let dx = [x1[0] - x0[0], x1[1] - x0[1]];
    let length = dx[0].hypot(dx[1]);
    if length == 0.0 {
        return Ok(Vec::new());
    }
    let samples = max_steps.clamp(1, NULL_PATH_SAMPLES);
    let c = c_f();
    let n_hat = [dx[0] / length, dx[1] / length];
    let dl = length / samples as f64;
    let mut out = Vec::with_capacity(samples as usize);
    for i in 0..samples {
        let mid = (i as f64 + 0.5) / samples as f64;
        let x = [x0[0] + dx[0] * mid, x0[1] + dx[1] * mid];
        let t = qf(emit.time) + mid * length / c;
        out.push((
            KernelEvent {
                time: round_q(t)?,
                position: [round_q(x[0])?, round_q(x[1])?],
            },
            dl,
            n_hat,
        ));
    }
    Ok(out)
}

/// (GEO-N) coordinate travel time of a metric null along the Euclidean path.
/// Tick binning is commit, not this discriminator. No Shapiro magnitude.
pub fn geo_n_arrival(
    g: &CompiledGeometry,
    emit: KernelEvent,
    receiver: [Q; 2],
    max_steps: u32,
) -> Result<f64, EvolvingPatchError> {
    probe_counters::with(|c| c.geo_n_refreshes += 1);
    let samples = null_path_samples(emit, receiver, max_steps)?;
    if samples.is_empty() {
        return Ok(0.0);
    }
    let c = c_f();
    let mut dt = 0.0;
    for (event, dl, n_hat) in samples {
        let field = g.phi_xi(event, None)?;
        let shapiro = (1.0 - 2.0 * field.phi / (c * c)) / c * dl;
        let xi_term = 4.0 * (field.xi[0] * n_hat[0] + field.xi[1] * n_hat[1]) / (c * c * c) * dl;
        dt += shapiro + xi_term;
    }
    if !dt.is_finite() {
        return Err(EvolvingPatchError::Nonfinite);
    }
    Ok(dt)
}

/// (CLK-G) laboratory quantum from the same `Φ` that enters `g_00`.
pub fn clk_g_rate(
    g: &CompiledGeometry,
    event: KernelEvent,
    velocity: [f64; 2],
    max_steps: u32,
) -> Result<Q, EvolvingPatchError> {
    probe_counters::with(|c| c.clock_rate_calls += 1);
    if max_steps == 0 {
        return Err(EvolvingPatchError::BranchBudgetExhausted { max_steps: 0 });
    }
    let field = g.phi_xi(event, None)?;
    clock_rate_from_phi(field.phi, velocity)
}

fn clock_rate_from_phi(phi: f64, velocity: [f64; 2]) -> Result<Q, EvolvingPatchError> {
    let c2 = c_f() * c_f();
    let v2 = velocity[0] * velocity[0] + velocity[1] * velocity[1];
    let arg = 1.0 + 2.0 * phi / c2 - v2 / c2;
    if arg < 0.0 {
        return Err(EvolvingPatchError::ClockSpacelike);
    }
    if !arg.is_finite() {
        return Err(EvolvingPatchError::Nonfinite);
    }
    let scaled = CLOCK_SCALE as f64 * arg.sqrt();
    if !scaled.is_finite() {
        return Err(EvolvingPatchError::Nonfinite);
    }
    Ok(Ratio::new(scaled.floor() as i128, CLOCK_SCALE))
}

fn tick_containing(t: f64) -> Q {
    let k = (t * c_f()).ceil() as i128;
    q(k, C)
}

fn stored_emit(ray: &NullRay) -> KernelEvent {
    KernelEvent {
        time: ray.emit_time,
        position: ray.emit_position,
    }
}

fn scheduled_post_cone_ray(geometry_id: u64) -> NullRay {
    let emit = post_emit();
    NullRay {
        emit_time: emit.time,
        emit_position: emit.position,
        receiver: receiver_pos(),
        coordinate_dt: UNFLOWN_COORDINATE_DT,
        affine_arrival: qf(emit.time),
        tick_delivery: None,
        geometry_id,
    }
}

fn rays_scheduled_identically(a: &NullRay, b: &NullRay) -> bool {
    a.emit_time == b.emit_time
        && a.emit_position == b.emit_position
        && a.receiver == b.receiver
        && a.tick_delivery.is_none()
        && b.tick_delivery.is_none()
        && a.coordinate_dt.to_bits() == b.coordinate_dt.to_bits()
}

fn refresh_ray_from_geometry(
    ray: &mut NullRay,
    g: &CompiledGeometry,
) -> Result<(), EvolvingPatchError> {
    let refreshed = geo_n_arrival(g, stored_emit(ray), ray.receiver, NULL_PATH_SAMPLES)?;
    ray.coordinate_dt = refreshed;
    ray.affine_arrival = qf(ray.emit_time) + refreshed;
    ray.geometry_id = g.id;
    Ok(())
}

fn commit_ray_on_containing_tick(ray: &mut NullRay, t_start: Q, t_end: Q) {
    if ray.tick_delivery.is_some() {
        return;
    }
    let start = qf(t_start);
    let end = qf(t_end);
    if ray.affine_arrival > start && ray.affine_arrival <= end {
        ray.tick_delivery = Some(t_end);
    }
}

/// `U` is the only writer of flown `dt`. Scheduled rays stay untouched until emit.
fn fly_pending_ray(
    ray: &mut NullRay,
    g: &CompiledGeometry,
    t_start: Q,
    t_end: Q,
) -> Result<(), EvolvingPatchError> {
    if ray.tick_delivery.is_some() || t_end < ray.emit_time {
        return Ok(());
    }
    refresh_ray_from_geometry(ray, g)?;
    let start = if t_start >= ray.emit_time {
        t_start
    } else {
        ray.emit_time
    };
    commit_ray_on_containing_tick(ray, start, t_end);
    Ok(())
}

fn clk_g_along_worldtube(
    g: &CompiledGeometry,
    worldtube: &[PatchSegment],
    t_end: Q,
) -> Result<Q, EvolvingPatchError> {
    if worldtube.is_empty() {
        return Err(EvolvingPatchError::Invalid(
            "CONSIS requires the ship's stepped worldtube",
        ));
    }
    let mut tau = Q::zero();
    for i in 0..worldtube.len() {
        let seg = &worldtube[i];
        let until = if i + 1 < worldtube.len() {
            worldtube[i + 1].since
        } else {
            t_end
        };
        if until <= seg.since {
            continue;
        }
        let event = KernelEvent {
            time: seg.since,
            position: seg.position,
        };
        let rate = clk_g_rate(g, event, seg.velocity, NULL_PATH_SAMPLES)?;
        tau += (until - seg.since) * rate;
    }
    Ok(tau)
}

fn bind_observables(p: &mut PatchState) -> Result<(), EvolvingPatchError> {
    let id = p.geometry.id;
    p.ship.geometry_id = id;
    p.clock.geometry_id = id;
    if let Some(ray) = p.ray.as_mut() {
        ray.geometry_id = id;
    }
    Ok(())
}

fn recompile(p: &mut PatchState) -> Result<(), EvolvingPatchError> {
    probe_counters::with(|c| {
        c.recompile_calls += 1;
        c.recompile_segments_copied += p
            .sources
            .iter()
            .map(|s| s.segments.len() as u64)
            .sum::<u64>()
    });
    p.geometry = CompiledGeometry::compile(
        p.sources.clone(),
        p.remainder,
        p.certificate.changes.clone(),
    );
    p.certificate.source_digest = p.geometry.id;
    p.certificate.remainder = p.remainder;
    bind_observables(p)
}

fn validate_cast(p: &PatchState) -> Result<(), EvolvingPatchError> {
    probe_counters::with(|c| c.validate_calls += 1);
    if p.sources.len() != MASSIVE_BODIES {
        return Err(EvolvingPatchError::UnsupportedPredicate(
            "cast requires N_mass=2",
        ));
    }
    if p.ship.mu != Q::zero() {
        return Err(EvolvingPatchError::CastRefused("test ship must have μ=0"));
    }
    for source in &p.sources {
        if source.segments.is_empty() {
            return Err(EvolvingPatchError::Invalid(
                "source worldtube has no segments",
            ));
        }
        if source.segments.iter().any(|seg| seg.since > p.time) {
            return Err(EvolvingPatchError::AuthoredFutures);
        }
        let last = last_segment(source)?;
        if last.mu <= Q::zero() {
            return Err(EvolvingPatchError::CastRefused(
                "massive source μ must be positive",
            ));
        }
        let speed = last.velocity[0].hypot(last.velocity[1]);
        if speed >= c_f() {
            return Err(EvolvingPatchError::Superluminal);
        }
    }
    Ok(())
}

fn canonical_eq(a: &PatchState, b: &PatchState) -> bool {
    a.time == b.time
        && a.sources == b.sources
        && a.geometry == b.geometry
        && a.ship == b.ship
        && a.ray == b.ray
        && a.clock == b.clock
        && a.remainder == b.remainder
        && a.certificate == b.certificate
}

/// Frozen laboratory cast at the admitted cut `t = 0`.
pub fn laboratory(change_a_mu_at_zero: bool) -> Result<PatchState, EvolvingPatchError> {
    laboratory_n(
        vec![
            (ID_A, [q(0, 1), Q::zero()], q(1, 1)),
            (ID_B, [q(8, 1), Q::zero()], q(1, 1)),
        ],
        change_a_mu_at_zero,
        Some(frozen_remainder()),
    )
}

pub fn laboratory_n(
    masses: Vec<(u64, [Q; 2], Q)>,
    change_a_mu_at_zero: bool,
    remainder: Option<OmittedTailBound>,
) -> Result<PatchState, EvolvingPatchError> {
    if masses.len() != MASSIVE_BODIES {
        return Err(EvolvingPatchError::UnsupportedPredicate(
            "cast requires N_mass=2",
        ));
    }
    let remainder = remainder.ok_or(EvolvingPatchError::UncertifiedExterior)?;
    let mut sources = Vec::new();
    let mut changes = Vec::new();
    for (id, position, mu) in masses {
        let mut segments = vec![PatchSegment {
            since: Q::from_integer(GENESIS),
            position,
            velocity: [0.0, 0.0],
            mu,
        }];
        if change_a_mu_at_zero && id == ID_A {
            segments.push(PatchSegment {
                since: Q::zero(),
                position,
                velocity: [0.0, 0.0],
                mu: q(2, 1),
            });
            changes.push(KernelEvent {
                time: Q::zero(),
                position,
            });
        }
        sources.push(PatchSource { id, segments });
    }
    let geometry = CompiledGeometry::compile(sources.clone(), remainder, changes.clone());
    let mut p = PatchState {
        time: Q::zero(),
        sources,
        geometry: geometry.clone(),
        ship: TestBody {
            id: ID_SHIP,
            position: [q(4, 1), Q::zero()],
            velocity: [0.0, 0.0],
            mu: Q::zero(),
            geometry_id: geometry.id,
            captured: None,
            worldtube: vec![PatchSegment {
                since: Q::zero(),
                position: [q(4, 1), Q::zero()],
                velocity: [0.0, 0.0],
                mu: Q::zero(),
            }],
        },
        ray: None,
        clock: Clock {
            tau: Q::zero(),
            geometry_id: geometry.id,
        },
        remainder,
        certificate: Certificate {
            source_digest: geometry.id,
            remainder,
            changes,
        },
        ledger: Vec::new(),
    };
    validate_cast(&p)?;
    p.ray = Some(scheduled_post_cone_ray(geometry.id));
    bind_observables(&mut p)?;
    Ok(p)
}

pub fn shares_compiled_object(p: &PatchState) -> bool {
    let id = p.geometry.id;
    id != MINKOWSKI_GEOMETRY_ID
        && p.ship.geometry_id == id
        && p.clock.geometry_id == id
        && p.ray.as_ref().is_some_and(|ray| ray.geometry_id == id)
}

/// A private trio co-moves after μ changes but does not share `g` in `P`.
pub fn private_phi_trio(mu_a: f64) -> PrivatePhiTrio {
    let ship = [4.0, 0.0];
    let a = gravitational_acceleration(ship, mu_a).unwrap_or([0.0, 0.0]);
    let b = gravitational_acceleration([-4.0, 0.0], 1.0).unwrap_or([0.0, 0.0]);
    let phi = -mu_a / 4.0 - 1.0 / 4.0;
    let c = c_f();
    PrivatePhiTrio {
        ship_accel: [a[0] + b[0], a[1] + b[1]],
        light_dt: minkowski_flight() * (1.0 - 2.0 * phi / (c * c)),
        clock_rate: (1.0 + 2.0 * phi / (c * c)).max(0.0).sqrt(),
    }
}

/// CONSIS sufficiency: stored ship / `P.ray` / `τ` are GEO-T / GEO-N / CLK-G
/// of the object in `P`. ID stamps are not a substitute.
fn bound_geo_readings(p: &PatchState) -> Result<([f64; 2], f64, Q), EvolvingPatchError> {
    let ray = p.ray.as_ref().ok_or(EvolvingPatchError::Invalid(
        "CONSIS requires a live ray in P",
    ))?;
    let last = p.ship.worldtube.last().ok_or(EvolvingPatchError::Invalid(
        "CONSIS requires the ship's stepped worldtube",
    ))?;
    if last.position != p.ship.position {
        return Err(EvolvingPatchError::Invalid(
            "stored ship worldtube does not end at the stored ship event",
        ));
    }
    let light = geo_n_arrival(
        &p.geometry,
        stored_emit(ray),
        ray.receiver,
        NULL_PATH_SAMPLES,
    )?;
    if ray.coordinate_dt.to_bits() != light.to_bits() {
        return Err(EvolvingPatchError::Invalid(
            "stored P.ray.coordinate_dt is not the GEO-N evaluation of the stored emit",
        ));
    }
    let event = KernelEvent {
        time: p.time,
        position: p.ship.position,
    };
    let ship = geo_t_accel(&p.geometry, event, p.ship.velocity, NULL_PATH_SAMPLES)?;
    let tau = clk_g_along_worldtube(&p.geometry, &p.ship.worldtube, p.time)?;
    if p.clock.tau != tau {
        return Err(EvolvingPatchError::Invalid(
            "stored τ is not CLK-G along the stepped worldtube",
        ));
    }
    Ok((ship, ray.coordinate_dt, p.clock.tau))
}

/// CONSIS rejects a private Φ-trio used as a substitute for the object in `P`.
pub fn consis_rejects_private_trio(trio: &PrivatePhiTrio, p: &PatchState) -> bool {
    let Ok((ship, light, _tau)) = bound_geo_readings(p) else {
        return true;
    };
    let event = KernelEvent {
        time: p.time,
        position: p.ship.position,
    };
    let Ok(rate) = clk_g_rate(&p.geometry, event, p.ship.velocity, NULL_PATH_SAMPLES) else {
        return true;
    };
    let ship_sub = trio.ship_accel[0].to_bits() != ship[0].to_bits()
        || trio.ship_accel[1].to_bits() != ship[1].to_bits();
    let light_sub = trio.light_dt.to_bits() != light.to_bits();
    let clock_sub = trio.clock_rate.to_bits() != qf(rate).to_bits();
    (ship_sub || light_sub || clock_sub) && shares_compiled_object(p)
}

/// Delayed Newton of both rest sources at `ship` (A at the origin, B at `(8,0)`).
fn delayed_newton_both_rest(
    ship: [f64; 2],
    mu_a: f64,
    mu_b: f64,
) -> Result<[f64; 2], EvolvingPatchError> {
    let a = gravitational_acceleration(ship, mu_a).map_err(|_| EvolvingPatchError::Nonfinite)?;
    let b = gravitational_acceleration([ship[0] - 8.0, ship[1]], mu_b)
        .map_err(|_| EvolvingPatchError::Nonfinite)?;
    Ok([a[0] + b[0], a[1] + b[1]])
}

fn evaluate_ray(
    p: &PatchState,
    emit: KernelEvent,
    receiver: [Q; 2],
    max_steps: u32,
) -> Result<NullRay, EvolvingPatchError> {
    let coordinate_dt = geo_n_arrival(&p.geometry, emit, receiver, max_steps)?;
    let affine_arrival = qf(emit.time) + coordinate_dt;
    Ok(NullRay {
        emit_time: emit.time,
        emit_position: emit.position,
        receiver,
        coordinate_dt,
        affine_arrival,
        tick_delivery: None,
        geometry_id: p.geometry.id,
    })
}

/// Minkowski negative-control probe. May pre-bin: these rays never go through `U`.
fn minkowski_ray(emit: KernelEvent, receiver: [Q; 2]) -> NullRay {
    let x0 = qf_pair(emit.position);
    let x1 = qf_pair(receiver);
    let length = (x1[0] - x0[0]).hypot(x1[1] - x0[1]);
    let coordinate_dt = length / c_f();
    let affine_arrival = qf(emit.time) + coordinate_dt;
    NullRay {
        emit_time: emit.time,
        emit_position: emit.position,
        receiver,
        coordinate_dt,
        affine_arrival,
        tick_delivery: Some(tick_containing(affine_arrival)),
        geometry_id: MINKOWSKI_GEOMETRY_ID,
    }
}

/// Observation / inspect: does not mutate `P` or any digest.
pub fn inspect(p: &PatchState, event: KernelEvent) -> Result<PhiXi, EvolvingPatchError> {
    p.geometry.phi_xi(event, None)
}

pub fn compile_cache(p: &PatchState) -> PatchCache {
    PatchCache {
        digest: p.geometry.id,
        remainder: p.remainder,
        geometry: p.geometry.clone(),
        changes: p.certificate.changes.clone(),
    }
}

/// Per-event certificate: a cache hit after (PATCH-INV) fails. `1/16` is
/// when the ship must not see old `g`, not a global TTL.
pub fn cached_geometry<'a>(
    cache: &'a PatchCache,
    live: &PatchState,
    event: KernelEvent,
) -> Result<&'a CompiledGeometry, EvolvingPatchError> {
    if cache.digest == live.geometry.id && cache.remainder == live.remainder {
        return Ok(&cache.geometry);
    }
    let visible_change =
        live.certificate.changes.iter().any(|change| {
            !cache.changes.contains(change) && in_closed_past_cone(*change, event, C)
        });
    if visible_change {
        return Err(EvolvingPatchError::CacheAfterInvalidation);
    }
    Ok(&cache.geometry)
}

fn step_one(p: &PatchState) -> Result<PatchState, EvolvingPatchError> {
    step_one_with(p, &p.geometry)
}

fn step_one_with(p: &PatchState, g: &CompiledGeometry) -> Result<PatchState, EvolvingPatchError> {
    validate_cast(p)?;
    let dt = dt_f();
    let next_time = p.time + dt_q();
    let mut next = p.clone();
    probe_counters::with(|c| c.state_clones += 1);

    if let Some(ray) = next.ray.as_mut() {
        if ray.tick_delivery.is_none() && p.time >= ray.emit_time {
            fly_pending_ray(ray, g, p.time, next_time)?;
        }
    }

    let start_event = KernelEvent {
        time: p.time,
        position: p.ship.position,
    };
    let start_velocity = p.ship.velocity;
    if let Some((id, class)) = g.capture_at(start_event, None)? {
        next.ship.captured = Some((id, class));
        next.ship.velocity = [0.0, 0.0];
    } else {
        let accel = geo_t_accel(g, start_event, start_velocity, NULL_PATH_SAMPLES)?;
        let velocity = [
            start_velocity[0] + accel[0] * dt,
            start_velocity[1] + accel[1] * dt,
        ];
        if !velocity[0].is_finite() || !velocity[1].is_finite() {
            return Err(EvolvingPatchError::Nonfinite);
        }
        if velocity[0].hypot(velocity[1]) >= c_f() {
            return Err(EvolvingPatchError::Superluminal);
        }
        let xf = [
            qf(p.ship.position[0]) + velocity[0] * dt,
            qf(p.ship.position[1]) + velocity[1] * dt,
        ];
        next.ship.position = [round_q(xf[0])?, round_q(xf[1])?];
        next.ship.velocity = velocity;
    }

    next.ship.worldtube.push(PatchSegment {
        since: next_time,
        position: next.ship.position,
        velocity: next.ship.velocity,
        mu: Q::zero(),
    });

    let rate = clk_g_rate(g, start_event, start_velocity, NULL_PATH_SAMPLES)?;
    next.clock.tau += dt_q() * rate;

    let mut committed = Vec::with_capacity(p.sources.len());
    for source in &p.sources {
        let last = last_segment(source)?.clone();
        let event = KernelEvent {
            time: p.time,
            position: last.position,
        };
        let mut next_seg = last.clone();
        next_seg.since = next_time;
        if g.capture_at(event, Some(source.id))?.is_some() {
            next_seg.velocity = [0.0, 0.0];
        } else {
            let field = g.phi_xi(event, Some(source.id))?;
            let accel = [
                field.e[0] + last.velocity[1] * field.b,
                field.e[1] - last.velocity[0] * field.b,
            ];
            let velocity = [
                last.velocity[0] + accel[0] * dt,
                last.velocity[1] + accel[1] * dt,
            ];
            if !velocity[0].is_finite() || !velocity[1].is_finite() {
                return Err(EvolvingPatchError::Nonfinite);
            }
            if velocity[0].hypot(velocity[1]) >= c_f() {
                return Err(EvolvingPatchError::Superluminal);
            }
            let xf = [
                qf(last.position[0]) + velocity[0] * dt,
                qf(last.position[1]) + velocity[1] * dt,
            ];
            next_seg.position = [round_q(xf[0])?, round_q(xf[1])?];
            next_seg.velocity = velocity;
        }
        let mut source = source.clone();
        let change = KernelEvent {
            time: next_time,
            position: next_seg.position,
        };
        source.segments.push(next_seg);
        next.certificate.changes.push(change);
        committed.push(source);
    }
    next.sources = committed;
    next.time = next_time;
    recompile(&mut next)?;
    let emit_now = next.ray.as_ref().is_some_and(|ray| {
        ray.tick_delivery.is_none() && p.time < ray.emit_time && next.time >= ray.emit_time
    });
    if emit_now {
        let g_now = next.geometry.clone();
        if let Some(ray) = next.ray.as_mut() {
            fly_pending_ray(ray, &g_now, ray.emit_time, next.time)?;
        }
    }
    validate_cast(&next)?;
    Ok(next)
}

fn cache_key_matches(cache: &PatchCache, live: &PatchState) -> bool {
    cache.digest == live.geometry.id && cache.remainder == live.remainder
}

fn certify_cached_step(cache: &PatchCache, live: &PatchState) -> Result<(), EvolvingPatchError> {
    cached_geometry(
        cache,
        live,
        KernelEvent {
            time: live.time,
            position: live.ship.position,
        },
    )?;
    if let Some(ray) = &live.ray {
        if ray.tick_delivery.is_none() && live.time + dt_q() >= ray.emit_time {
            cached_geometry(cache, live, stored_emit(ray))?;
            for (event, _, _) in
                null_path_samples(stored_emit(ray), ray.receiver, NULL_PATH_SAMPLES)?
            {
                cached_geometry(cache, live, event)?;
            }
        }
    }
    Ok(())
}

/// Finite map `U(t_out, t_in, P)` on admitted integer-tick cuts.
/// Source-history path: `phi_xi` picks the latest cone-visible segment.
pub fn advance_patch(state: &PatchState, t_out: Q) -> Result<PatchState, EvolvingPatchError> {
    validate_cast(state)?;
    if t_out < state.time {
        return Err(EvolvingPatchError::Invalid("cannot step backward"));
    }
    if !is_tick(state.time) || !is_tick(t_out) {
        return Err(EvolvingPatchError::UnsupportedPredicate(
            "admitted cuts are integer ticks",
        ));
    }
    let mut p = state.clone();
    while p.time < t_out {
        p = step_one(&p)?;
        probe_counters::with(|c| c.ticks += 1);
    }
    Ok(p)
}

/// Evaluating `U` from compiled cache `C`. Cache key is source-history digest
/// plus remainder. A cache hit after (PATCH-INV) fails this `U`.
pub fn advance_from_cache(
    state: &PatchState,
    t_out: Q,
    cache: &PatchCache,
) -> Result<PatchState, EvolvingPatchError> {
    validate_cast(state)?;
    if t_out < state.time {
        return Err(EvolvingPatchError::Invalid("cannot step backward"));
    }
    if !is_tick(state.time) || !is_tick(t_out) {
        return Err(EvolvingPatchError::UnsupportedPredicate(
            "admitted cuts are integer ticks",
        ));
    }
    let refresh = cache_key_matches(cache, state);
    let mut p = state.clone();
    let mut c = cache.clone();
    while p.time < t_out {
        certify_cached_step(&c, &p)?;
        let start = KernelEvent {
            time: p.time,
            position: p.ship.position,
        };
        let g = cached_geometry(&c, &p, start)?.clone();
        p = step_one_with(&p, &g)?;
        probe_counters::with(|c| c.ticks += 1);
        if refresh {
            c = compile_cache(&p);
        }
    }
    Ok(p)
}

fn fixture_two_source_cast() -> Result<(), EvolvingPatchError> {
    let p = laboratory(false)?;
    validate_cast(&p)?;
    let ray = p.ray.as_ref().ok_or(EvolvingPatchError::Invalid(
        "laboratory P is missing the live ray",
    ))?;
    if p.geometry.id == MINKOWSKI_GEOMETRY_ID || !shares_compiled_object(&p) {
        return Err(EvolvingPatchError::Invalid("missing compiled g"));
    }
    if ray.emit_time != post_emit().time || ray.emit_position != post_emit().position {
        return Err(EvolvingPatchError::Invalid(
            "laboratory P.ray must be the spec post-cone emit",
        ));
    }
    if ray.tick_delivery.is_some() || ray.coordinate_dt != UNFLOWN_COORDINATE_DT {
        return Err(EvolvingPatchError::Invalid(
            "scheduled laboratory ray must stay unflown until U emits it",
        ));
    }
    let mut authored = p.clone();
    let authored_position = authored.sources[0].segments[0].position;
    authored.sources[0].segments.push(PatchSegment {
        since: q(1, 1),
        position: authored_position,
        velocity: [0.0, 0.0],
        mu: q(1, 1),
    });
    match validate_cast(&authored) {
        Err(EvolvingPatchError::AuthoredFutures) => Ok(()),
        Ok(()) => Err(EvolvingPatchError::Invalid(
            "authored futures were accepted",
        )),
        Err(other) => Err(other),
    }
}

fn fixture_source_change_moves_ship() -> Result<(f64, f64), EvolvingPatchError> {
    let p0 = laboratory(false)?;
    let pd = laboratory(true)?;
    let pre0 = advance_patch(&p0, q(1, 64))?;
    let pred = advance_patch(&pd, q(1, 64))?;
    let post0 = advance_patch(&p0, q(1, 8))?;
    let postd = advance_patch(&pd, q(1, 8))?;
    let pre = influence(qf_pair(pred.ship.position), qf_pair(pre0.ship.position));
    let post = influence(qf_pair(postd.ship.position), qf_pair(post0.ship.position));
    Ok((pre, post))
}

fn fixture_source_change_delays_light() -> Result<(f64, f64, f64), EvolvingPatchError> {
    let p0 = laboratory(false)?;
    let pd = laboratory(true)?;
    // Spec pre_emit remains a geometry probe. It does not substitute for P.ray.
    let pre0 = evaluate_ray(&p0, pre_emit(), receiver_pos(), NULL_PATH_SAMPLES)?;
    let pred = evaluate_ray(&pd, pre_emit(), receiver_pos(), NULL_PATH_SAMPLES)?;
    if pred.coordinate_dt.to_bits() != pre0.coordinate_dt.to_bits() {
        return Err(EvolvingPatchError::Invalid(
            "pre-cone light arrival changed",
        ));
    }
    let post0_state = advance_patch(&p0, q(1, 8))?;
    let postd_state = advance_patch(&pd, q(1, 8))?;
    let post0 = post0_state.ray.as_ref().ok_or(EvolvingPatchError::Invalid(
        "post-cone P_0 dropped the live ray",
    ))?;
    let postd = postd_state.ray.as_ref().ok_or(EvolvingPatchError::Invalid(
        "post-cone P_Δ dropped the live ray",
    ))?;
    if post0.emit_time != post_emit().time || postd.emit_time != post_emit().time {
        return Err(EvolvingPatchError::Invalid(
            "laboratory P.ray must be the spec post-cone emit",
        ));
    }
    Ok((postd.coordinate_dt, minkowski_flight(), post0.coordinate_dt))
}

fn fixture_source_change_shifts_clock() -> Result<(Q, Q, Q, Q), EvolvingPatchError> {
    let p0 = laboratory(false)?;
    let pd = laboratory(true)?;
    let pre0 = advance_patch(&p0, q(1, 64))?;
    let pred = advance_patch(&pd, q(1, 64))?;
    let post0 = advance_patch(&p0, q(1, 8))?;
    let postd = advance_patch(&pd, q(1, 8))?;
    Ok((
        pre0.clock.tau,
        pred.clock.tau,
        post0.clock.tau,
        postd.clock.tau,
    ))
}

fn fixture_same_metric_consistency() -> Result<bool, EvolvingPatchError> {
    let p0 = laboratory(false)?;
    let pd = laboratory(true)?;
    let pre0 = advance_patch(&p0, q(1, 64))?;
    let pred = advance_patch(&pd, q(1, 64))?;
    let post0 = advance_patch(&p0, q(1, 8))?;
    let postd = advance_patch(&pd, q(1, 8))?;
    let ship_pre = influence(qf_pair(pred.ship.position), qf_pair(pre0.ship.position));
    let ship_post = influence(qf_pair(postd.ship.position), qf_pair(post0.ship.position));
    let clock_pre = pred.clock.tau == pre0.clock.tau;
    let clock_post = postd.clock.tau != post0.clock.tau;
    // Spec pre_emit probes remain extra geometry probes; they do not substitute
    // for composing the post-cone ray in P.
    let light0_pre_probe = evaluate_ray(&pre0, pre_emit(), receiver_pos(), NULL_PATH_SAMPLES)?;
    let lightd_pre_probe = evaluate_ray(&pred, pre_emit(), receiver_pos(), NULL_PATH_SAMPLES)?;
    let probe_pre =
        lightd_pre_probe.coordinate_dt.to_bits() == light0_pre_probe.coordinate_dt.to_bits();
    let r_pre0 = pre0.ray.as_ref().ok_or(EvolvingPatchError::Invalid(
        "pre-cone P_0 dropped the live ray",
    ))?;
    let r_pred = pred.ray.as_ref().ok_or(EvolvingPatchError::Invalid(
        "pre-cone P_Δ dropped the live ray",
    ))?;
    let light_pre = rays_scheduled_identically(r_pre0, r_pred);
    let r_post0 = post0.ray.as_ref().ok_or(EvolvingPatchError::Invalid(
        "post-cone P_0 dropped the live ray",
    ))?;
    let r_postd = postd.ray.as_ref().ok_or(EvolvingPatchError::Invalid(
        "post-cone P_Δ dropped the live ray",
    ))?;
    if r_post0.emit_time != post_emit().time || r_postd.emit_time != post_emit().time {
        return Err(EvolvingPatchError::Invalid(
            "CONSIS of light requires the stored post-cone emit in P.ray",
        ));
    }
    let Ok((_, stored0, _)) = bound_geo_readings(&post0) else {
        return Ok(false);
    };
    let Ok((from_g_ship, stored_light, stored_tau)) = bound_geo_readings(&postd) else {
        return Ok(false);
    };
    let light_post = stored_light.to_bits() != stored0.to_bits()
        && stored_light.to_bits() == r_postd.coordinate_dt.to_bits()
        && stored0.to_bits() == r_post0.coordinate_dt.to_bits();
    if ship_pre != 0.0 || !clock_pre || !light_pre || !probe_pre {
        return Ok(false);
    }
    if ship_post <= 0.0 || !clock_post || !light_post {
        return Ok(false);
    }
    let bound = shares_compiled_object(&postd)
        && from_g_ship.iter().all(|x| x.is_finite())
        && stored_tau == postd.clock.tau;
    let trio = private_phi_trio(2.0);
    let trio_comoves = (trio.light_dt - private_phi_trio(1.0).light_dt).abs() > 0.0;
    let mut stamped = postd.clone();
    if let Some(stamped_ray) = stamped.ray.as_mut() {
        stamped_ray.coordinate_dt = trio.light_dt;
        stamped_ray.affine_arrival = qf(stamped_ray.emit_time) + trio.light_dt;
        stamped_ray.geometry_id = postd.geometry.id;
    }
    stamped.ship.geometry_id = postd.geometry.id;
    stamped.clock.geometry_id = postd.geometry.id;
    let stamped_is_object = bound_geo_readings(&stamped).is_ok();
    Ok(bound
        && trio_comoves
        && !stamped_is_object
        && consis_rejects_private_trio(&trio, &postd)
        && consis_rejects_private_trio(&trio, &stamped))
}

fn fixture_direct_vs_subdivided() -> Result<bool, EvolvingPatchError> {
    let p = laboratory(true)?;
    let direct = advance_patch(&p, q(1, 8))?;
    let mid = advance_patch(&p, q(1, 64))?;
    let subdivided = advance_patch(&mid, q(1, 8))?;
    Ok(canonical_eq(&direct, &subdivided))
}

fn fixture_cache_reuse() -> Result<bool, EvolvingPatchError> {
    let p = laboratory(false)?;
    let cache = compile_cache(&p);
    if !cache_key_matches(&cache, &p) {
        return Ok(false);
    }
    let event = ship_event(Q::zero());
    let cached = cached_geometry(&cache, &p, event)?;
    let field_c = cached.phi_xi(event, None)?;
    let field_p = p.geometry.phi_xi(event, None)?;
    if field_c.phi.to_bits() != field_p.phi.to_bits()
        || field_c.e[0].to_bits() != field_p.e[0].to_bits()
        || cached.id != p.geometry.id
    {
        return Ok(false);
    }
    let from_history = advance_patch(&p, q(1, 8))?;
    let from_cache = advance_from_cache(&p, q(1, 8), &cache)?;
    Ok(canonical_eq(&from_history, &from_cache) && cache.digest == p.geometry.id)
}

fn fixture_invalidates_certificate() -> Result<bool, EvolvingPatchError> {
    let p0 = laboratory(false)?;
    let pd = laboratory(true)?;
    let cache = compile_cache(&p0);
    let ship_on = ship_event(q(1, 16));
    let far = KernelEvent {
        time: q(1, 16),
        position: [q(16, 1), Q::zero()],
    };
    let interior = KernelEvent {
        time: q(1, 32),
        position: [q(1, 1), Q::zero()],
    };
    let post_path = KernelEvent {
        time: q(1, 8) + q(1, 32),
        position: [q(4, 1), q(2, 1)],
    };
    let hit = cached_geometry(&cache, &pd, ship_on);
    let far_ok = cached_geometry(&cache, &pd, far);
    let interior_hit = cached_geometry(&cache, &pd, interior);
    let path_hit = cached_geometry(&cache, &pd, post_path);
    let history_pre = advance_patch(&pd, q(1, 64))?;
    let u_precone = advance_from_cache(&pd, q(1, 64), &cache);
    let precone_ok = u_precone
        .as_ref()
        .ok()
        .is_some_and(|cached| canonical_eq(cached, &history_pre));
    let u_stale = advance_from_cache(&pd, q(1, 8), &cache);
    Ok(
        matches!(hit, Err(EvolvingPatchError::CacheAfterInvalidation))
            && matches!(
                interior_hit,
                Err(EvolvingPatchError::CacheAfterInvalidation)
            )
            && matches!(path_hit, Err(EvolvingPatchError::CacheAfterInvalidation))
            && far_ok.is_ok()
            && precone_ok
            && matches!(u_stale, Err(EvolvingPatchError::CacheAfterInvalidation)),
    )
}

fn fixture_remainder_survives() -> Result<bool, EvolvingPatchError> {
    match laboratory_n(
        vec![
            (ID_A, [q(0, 1), Q::zero()], q(1, 1)),
            (ID_B, [q(8, 1), Q::zero()], q(1, 1)),
        ],
        false,
        None,
    ) {
        Err(EvolvingPatchError::UncertifiedExterior) => {}
        _ => return Ok(false),
    }
    let p = laboratory(false)?;
    let next = advance_patch(&p, dt_q())?;
    Ok(next.remainder == p.remainder && next.remainder.mu_bound == q(1, 1))
}

fn fixture_third_massive_refuses() -> bool {
    matches!(
        laboratory_n(
            vec![
                (ID_A, [q(0, 1), Q::zero()], q(1, 1)),
                (ID_B, [q(8, 1), Q::zero()], q(1, 1)),
                (3, [q(2, 1), Q::zero()], q(1, 1)),
            ],
            false,
            Some(frozen_remainder()),
        ),
        Err(EvolvingPatchError::UnsupportedPredicate(_))
    )
}

fn fixture_budget_exhausted() -> bool {
    let p = laboratory(false).expect("frozen cast");
    let emit = post_emit();
    matches!(
        geo_n_arrival(&p.geometry, emit, receiver_pos(), 0),
        Err(EvolvingPatchError::BranchBudgetExhausted { max_steps: 0 })
    ) && matches!(
        geo_t_accel(&p.geometry, ship_event(Q::zero()), [0.0, 0.0], 0),
        Err(EvolvingPatchError::BranchBudgetExhausted { max_steps: 0 })
    ) && matches!(
        clk_g_rate(&p.geometry, ship_event(Q::zero()), [0.0, 0.0], 0),
        Err(EvolvingPatchError::BranchBudgetExhausted { max_steps: 0 })
    )
}

fn fixture_inertial_clock_phi_zero() -> Result<bool, EvolvingPatchError> {
    let vac = vacuum_geometry();
    let rate = clk_g_rate(
        &vac,
        KernelEvent {
            time: Q::zero(),
            position: [Q::zero(), Q::zero()],
        },
        [0.0, 0.0],
        NULL_PATH_SAMPLES,
    )?;
    Ok(rate == Q::from_integer(1))
}

fn fixture_observation_does_not_recompile() -> Result<bool, EvolvingPatchError> {
    let p = laboratory(false)?;
    let before = p.geometry.id;
    let _ = inspect(&p, ship_event(q(1, 8)))?;
    Ok(p.geometry.id == before && p.certificate.source_digest == before && p.time == Q::zero())
}

fn fixture_minkowski_negative() -> Result<bool, EvolvingPatchError> {
    let p = advance_patch(&laboratory(true)?, q(1, 8))?;
    let metric = evaluate_ray(&p, post_emit(), receiver_pos(), NULL_PATH_SAMPLES)?;
    let mink = minkowski_ray(post_emit(), receiver_pos());
    Ok(mink.coordinate_dt.to_bits() == minkowski_flight().to_bits()
        && metric.coordinate_dt > minkowski_flight()
        && mink.geometry_id != p.geometry.id
        && metric.geometry_id == p.geometry.id)
}

fn fixture_delayed_newton_negative() -> Result<bool, EvolvingPatchError> {
    let p = advance_patch(&laboratory(true)?, q(1, 8))?;
    let ship = qf_pair(p.ship.position);
    let newton = delayed_newton_both_rest(ship, 2.0, 1.0)?;
    let mink = minkowski_ray(post_emit(), receiver_pos());
    let geodesic = geo_t_accel(
        &p.geometry,
        ship_event(p.time),
        [0.0, 0.0],
        NULL_PATH_SAMPLES,
    )?;
    let metric = evaluate_ray(&p, post_emit(), receiver_pos(), NULL_PATH_SAMPLES)?;
    let inertial_rate = Q::from_integer(1);
    let _rest_geo_t_may_equal_delayed_newton = newton[0].to_bits() == geodesic[0].to_bits()
        && newton[1].to_bits() == geodesic[1].to_bits();
    let light_split = mink.geometry_id != p.geometry.id
        && metric.coordinate_dt.to_bits() != mink.coordinate_dt.to_bits()
        && metric.geometry_id == p.geometry.id;
    let clock_split = clk_g_rate(
        &p.geometry,
        ship_event(p.time),
        p.ship.velocity,
        NULL_PATH_SAMPLES,
    )? != inertial_rate;
    Ok(light_split && clock_split && shares_compiled_object(&p) && advance_map().is_err())
}

fn fixture_schwarzschild_negative() -> bool {
    SCHWARZSCHILD_LAW_ID != PATCH_LAW_ID
        && matches!(
            laboratory_n(
                vec![(ID_A, [Q::zero(), Q::zero()], q(1, 1))],
                false,
                Some(frozen_remainder()),
            ),
            Err(EvolvingPatchError::UnsupportedPredicate(_))
        )
}

fn fixture_gem_force_without_null() -> Result<bool, EvolvingPatchError> {
    let p = advance_patch(&laboratory(true)?, q(1, 8))?;
    let gem_ship = geo_t_accel(
        &p.geometry,
        KernelEvent {
            time: p.time,
            position: p.ship.position,
        },
        p.ship.velocity,
        NULL_PATH_SAMPLES,
    )?;
    let mink = minkowski_ray(post_emit(), receiver_pos());
    let metric = evaluate_ray(&p, post_emit(), receiver_pos(), NULL_PATH_SAMPLES)?;
    let gem_map_still_refused = advance_map().is_err();
    Ok(gem_ship.iter().all(|x| x.is_finite())
        && mink.geometry_id == MINKOWSKI_GEOMETRY_ID
        && metric.geometry_id == p.geometry.id
        && mink.coordinate_dt.to_bits() != metric.coordinate_dt.to_bits()
        && gem_map_still_refused
        && !shares_compiled_object(&PatchState {
            ray: Some(mink),
            ..p.clone()
        }))
}

pub fn evolving_patch_manifest() -> Result<(), String> {
    let slice: FileSlice = serde_json::from_str(MANIFEST).map_err(|e| e.to_string())?;
    let m = &slice.evolving_spacetime_patch_research;
    if m.law_id != PATCH_LAW_ID {
        return Err("evolving patch law id drifted".into());
    }
    if m.law_id == INERTIAL_LAB_LAW_ID
        || m.law_id == RESEARCH_LAW_ID
        || m.law_id == COUPLED_LAW_ID
        || m.law_id == SCHWARZSCHILD_LAW_ID
        || m.law_id == GEM_LAW_ID
    {
        return Err("evolving patch must keep a distinct research id".into());
    }
    if m.status != "research-not-production"
        || m.spec != "docs/laws/evolving-spacetime-patch-v0.md"
        || m.map_status != MAP_STATUS
        || m.shared_object != "patch-metric-geometry"
        || m.candidate_metric != GEM_LAW_ID
    {
        return Err("evolving patch spec verdict drifted".into());
    }
    if m.parent_kernel != RESEARCH_LAW_ID {
        return Err("evolving patch parent must remain the retarded monopole kernel".into());
    }
    if m.coupled_kernel != COUPLED_LAW_ID {
        return Err("evolving patch coupled kernel id drifted".into());
    }
    if m.schwarzschild_kernel != SCHWARZSCHILD_LAW_ID {
        return Err("evolving patch Schwarzschild kernel id drifted".into());
    }
    if m.gem_kernel != GEM_LAW_ID {
        return Err("evolving patch GEM candidate id drifted".into());
    }
    if m.light_speed != C
        || m.massive_bodies != MASSIVE_BODIES
        || m.test_bodies != TEST_BODIES
        || m.light_rays != LIGHT_RAYS
        || m.clocks != CLOCKS
        || m.step != [1, C]
        || m.position_denom != POSITION_DENOM
        || m.clock_fractional_bits != CLOCK_FRACTIONAL_BITS
        || m.pre_lightcone_response_max != 0.0
        || m.post_lightcone_influence_min != 0.0
        || !m.post_lightcone_influence_strict
    {
        return Err("evolving-patch research thresholds were weakened or retuned".into());
    }
    if slice.aggregate_gates.pre_lightcone_response_max != 0.0
        || slice.aggregate_gates.backreaction_relative_error_max != 1e-12
    {
        return Err("frozen aggregate thresholds were edited".into());
    }
    if slice.tiny_causal_law_research.present_alignment_dot_min != [2047, 2048] {
        return Err("GEM frozen cosine 2047/2048 was retuned".into());
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
        return Err("evolving patch named equations were renamed, dropped or reordered".into());
    }
    let ids: Vec<&str> = m.fixtures.iter().map(|f| f.id.as_str()).collect();
    if ids != EVOLVING_PATCH_FIXTURE_IDS {
        return Err("evolving patch fixtures were renamed, dropped or reordered".into());
    }
    pin_spec_patch(m)?;
    Ok(())
}

fn fixture<'a>(m: &'a PatchManifest, id: &str) -> Result<&'a NamedFixture, String> {
    m.fixtures
        .iter()
        .find(|f| f.id == id)
        .ok_or_else(|| format!("missing evolving-patch fixture {id}"))
}

fn fills_g(got: &[String]) -> bool {
    got.iter()
        .map(String::as_str)
        .eq(GEM_MAY_FILL.iter().copied())
}

fn pin_spec_patch(m: &PatchManifest) -> Result<(), String> {
    if m.consis_object != CONSIS_OBJECT
        || m.consis_binding != CONSIS_BINDING
        || m.consis_comovement != CONSIS_COMOVEMENT
        || m.private_phi_trio != PRIVATE_PHI_TRIO
    {
        return Err("CONSIS must bind GEO-T/GEO-N/CLK-G to one object in P; co-movement is necessary not sufficient; a private Φ-trio fails".into());
    }
    if m.geo_n_discriminator != GEO_N_DISCRIMINATOR
        || m.geo_n_tick_binning != GEO_N_TICK_BINNING
        || m.shapiro_magnitude != SHAPIRO_MAGNITUDE
        || !m.delay_strict_gt_minkowski
        || !m.delay_ne_baseline
    {
        return Err("GEO-N must discriminate by coordinate/affine arrival with Δt>L/c and Δt≠baseline and no Shapiro freeze".into());
    }
    if m.certificate != CERTIFICATE
        || m.certificate_scope != CERTIFICATE_SCOPE
        || m.ship_old_g_deadline != SHIP_OLD_G_DEADLINE
        || m.cache_key != CACHE_KEY
        || m.cache_after_inv != CACHE_AFTER_INV
    {
        return Err("PATCH-INV/CACHE certificate must be source digest + remainder + per-event future cone; 1/16 is ship-local; cache after INV fails".into());
    }
    if m.authored_futures {
        return Err("authored_futures must stay false".into());
    }
    if m.gem_map_is_this_object || !fills_g(&m.gem_may_fill) {
        return Err("GEM MAP is not this object; GEM METRIC/GEM-a/CLK may fill g".into());
    }

    let cast = fixture(m, "two_source_one_ship_one_ray_one_clock")?;
    if cast.authored_futures != Some(false) {
        return Err(
            "two_source_one_ship_one_ray_one_clock must record authored_futures: false as claimed by the spec table"
                .into(),
        );
    }

    let consis = fixture(m, "same_metric_consistency")?;
    if consis.consis_object.as_deref() != Some(CONSIS_OBJECT)
        || consis.consis_binding.as_deref() != Some(CONSIS_BINDING)
        || consis.consis_comovement.as_deref() != Some(CONSIS_COMOVEMENT)
        || consis.private_phi_trio.as_deref() != Some(PRIVATE_PHI_TRIO)
    {
        return Err(
            "same_metric_consistency must pin one object in P; co-movement necessary not sufficient; private Φ-trio fails"
                .into(),
        );
    }

    let light = fixture(m, "source_change_delays_light")?;
    if light.discriminator.as_deref() != Some(GEO_N_DISCRIMINATOR)
        || light.tick_binning.as_deref() != Some(GEO_N_TICK_BINNING)
        || light.require_delay_gt_minkowski != Some(true)
        || light.require_delay_ne_baseline != Some(true)
        || light.shapiro_magnitude.as_deref() != Some(SHAPIRO_MAGNITUDE)
        || light.minkowski_flight != Some(MINKOWSKI_FLIGHT)
    {
        return Err(
            "source_change_delays_light must discriminate by coordinate/affine arrival, keep L/c as Minkowski flight, and freeze no Shapiro magnitude"
                .into(),
        );
    }

    let inv = fixture(m, "source_change_invalidates_certificate")?;
    if inv.certificate.as_deref() != Some(CERTIFICATE)
        || inv.certificate_scope.as_deref() != Some(CERTIFICATE_SCOPE)
        || inv.not_global_ttl != Some(true)
        || inv.ship_must_not_see_old_g_at != Some(SHIP_OLD_G_DEADLINE)
        || inv.cache_key.as_deref() != Some(CACHE_KEY)
        || inv.cache_after_inv.as_deref() != Some(CACHE_AFTER_INV)
    {
        return Err(
            "source_change_invalidates_certificate must be per-event future-cone, not a global TTL; 1/16 is when the ship must not see old g"
                .into(),
        );
    }

    let cache = fixture(m, "cache_reuse_matches")?;
    if cache.cache_key.as_deref() != Some(CACHE_KEY)
        || cache.cache_after_inv.as_deref() != Some(CACHE_AFTER_INV)
    {
        return Err(
            "cache_reuse_matches must key on source-history digest and fail after INV".into(),
        );
    }

    let gem = fixture(m, "gem_force_without_null_geodesic_fails_consistency")?;
    if gem.gem_map_is_this_object != Some(false)
        || !gem.gem_may_fill.as_ref().is_some_and(|fill| fills_g(fill))
    {
        return Err(
            "GEM negative control must keep MAP as not this object and METRIC/GEM-a/CLK as fills"
                .into(),
        );
    }

    for id in [
        "minkowski_signal_not_metric_null",
        "delayed_newton_not_the_patch",
        "schwarzschild_classifier_not_evolving_patch",
        "gem_force_without_null_geodesic_fails_consistency",
    ] {
        let named = fixture(m, id)?;
        if named.kind != "negative_control" {
            return Err(format!("{id} must remain a named negative control"));
        }
    }
    Ok(())
}

fn record_probe(report: &mut CandidateReport, id: &str, result: Result<bool, EvolvingPatchError>) {
    match result {
        Ok(true) => gate(report, id, true, "frozen fixture holds on the patch map"),
        Ok(false) => gate(report, id, false, "frozen fixture failed on the patch map"),
        Err(error) => gate(report, id, false, error.to_string()),
    }
}

pub fn qualify_evolving_patch_spec() -> CandidateReport {
    let mut report = CandidateReport {
        id: PATCH_LAW_ID.into(),
        version: 0,
        status: "FAIL".into(),
        metrics: Vec::new(),
        gates: Vec::new(),
        evidence: vec![
            "Research map es-evolving-spacetime-patch-v0 is isolated from es-inertial-causal-v1 and from es-causal-retarded-gem-v0.".into(),
            "Shared object is the compiled patch metric / (Φ,ξ) in P. Cast: two massive bodies, one test ship μ=0, one light ray, one clock.".into(),
            "GEO-T, GEO-N, and CLK-G are stored ship / P.ray / τ evaluations of that one object in P. Laboratory P.ray is the spec post-cone emit (t=1/8), scheduled at genesis; U flies it after emit_time with pending tick_delivery. bind_observables stamps geometry_id only. Co-movement is necessary, not sufficient. A private Φ-trio, including a stamped light_dt on P.ray, fails CONSIS.".into(),
            "GEO-N discriminates by coordinate/affine arrival before tick binning; Δt>L/c and Δt≠baseline; no Shapiro freeze. GEM (SIG) Minkowski is a negative control.".into(),
            "Certificate is source digest + remainder + per-event future cone; 1/16 is ship-local, not a global TTL. Cached U certifies the ship, in-flight or just-emitted ray emit, and GEO-N path samples — not a source's self-cone. Cache after INV fails U. authored_futures is false.".into(),
            "GEM (METRIC)/(GEM-a)/(CLK) may fill g. GEM (MAP) is not this object; advance_map still refuses. Not delayed-Newton-as-G2, not 2D log gravity.".into(),
            "G2 stays FAIL. compact_field_certification stays FAIL. terminating_exact_branches stays FAIL. production_law stays null.".into(),
        ],
    };

    match evolving_patch_manifest() {
        Ok(()) => gate(
            &mut report,
            "evolving_patch_manifest_isolated",
            true,
            "New evolving-patch fixtures did not edit frozen production-gate identities, old numeric thresholds, or GEM cosine 2047/2048.",
        ),
        Err(error) => gate(
            &mut report,
            "evolving_patch_manifest_isolated",
            false,
            error,
        ),
    }

    record_probe(
        &mut report,
        "two_source_one_ship_one_ray_one_clock",
        fixture_two_source_cast().map(|()| true),
    );
    match fixture_source_change_moves_ship() {
        Ok((pre, post)) => {
            report.metrics.push(super::Metric {
                scenario: "source_change_moves_ship".into(),
                name: "pre_lightcone_response".into(),
                value: pre,
                unit: "length".into(),
                threshold: 0.0,
                passed: pre == 0.0,
            });
            report.metrics.push(super::Metric {
                scenario: "source_change_moves_ship".into(),
                name: "post_lightcone_influence".into(),
                value: post,
                unit: "length".into(),
                threshold: POST_LIGHTCONE_INFLUENCE_MIN,
                passed: post > 0.0,
            });
            gate(
                &mut report,
                "source_change_moves_ship",
                pre == 0.0 && post > 0.0,
                format!("Ship vs μ:1→2. Pre t=1/64 influence {pre:.12e}; post t=1/8 {post:.12e}."),
            );
        }
        Err(error) => gate(
            &mut report,
            "source_change_moves_ship",
            false,
            error.to_string(),
        ),
    }
    match fixture_source_change_delays_light() {
        Ok((dt_delta, mink, dt_base)) => {
            let passed = dt_delta > mink && dt_delta.to_bits() != dt_base.to_bits();
            gate(
                &mut report,
                "source_change_delays_light",
                passed,
                "Coordinate/affine arrival: Δt_PΔ > L/c and Δt_PΔ ≠ Δt_P0. No Shapiro magnitude frozen. Tick binning is commit.",
            );
        }
        Err(error) => gate(
            &mut report,
            "source_change_delays_light",
            false,
            error.to_string(),
        ),
    }
    match fixture_source_change_shifts_clock() {
        Ok((pre0, pred, post0, postd)) => gate(
            &mut report,
            "source_change_shifts_clock",
            pre0 == pred && post0 != postd,
            "Clock τ matches pre-cone and differs post-cone from the same g.",
        ),
        Err(error) => gate(
            &mut report,
            "source_change_shifts_clock",
            false,
            error.to_string(),
        ),
    }
    record_probe(
        &mut report,
        "same_metric_consistency",
        fixture_same_metric_consistency(),
    );
    record_probe(
        &mut report,
        "direct_vs_subdivided_patch",
        fixture_direct_vs_subdivided(),
    );
    record_probe(&mut report, "cache_reuse_matches", fixture_cache_reuse());
    record_probe(
        &mut report,
        "source_change_invalidates_certificate",
        fixture_invalidates_certificate(),
    );
    record_probe(
        &mut report,
        "remainder_in_patch_state",
        fixture_remainder_survives(),
    );
    gate(
        &mut report,
        "unsupported_third_massive_refuses",
        fixture_third_massive_refuses(),
        "N_mass=3 is UnsupportedPredicate.",
    );
    gate(
        &mut report,
        "budget_exhausted_not_a_geodesic",
        fixture_budget_exhausted(),
        "max_steps=0 is BranchBudgetExhausted, not a geodesic/Shapiro/clock sign.",
    );
    record_probe(
        &mut report,
        "inertial_clock_when_phi_zero",
        fixture_inertial_clock_phi_zero(),
    );
    record_probe(
        &mut report,
        "observation_does_not_recompile",
        fixture_observation_does_not_recompile(),
    );
    record_probe(
        &mut report,
        "minkowski_signal_not_metric_null",
        fixture_minkowski_negative(),
    );
    record_probe(
        &mut report,
        "delayed_newton_not_the_patch",
        fixture_delayed_newton_negative(),
    );
    gate(
        &mut report,
        "schwarzschild_classifier_not_evolving_patch",
        fixture_schwarzschild_negative(),
        "Schwarzschild fate classifiers are not this propagator.",
    );
    record_probe(
        &mut report,
        "gem_force_without_null_geodesic_fails_consistency",
        fixture_gem_force_without_null(),
    );

    let ship = report
        .gates
        .iter()
        .find(|g| g.id == "source_change_moves_ship")
        .map(|g| g.passed)
        .unwrap_or(false);
    let light = report
        .gates
        .iter()
        .find(|g| g.id == "source_change_delays_light")
        .map(|g| g.passed)
        .unwrap_or(false);
    let clock = report
        .gates
        .iter()
        .find(|g| g.id == "source_change_shifts_clock")
        .map(|g| g.passed)
        .unwrap_or(false);
    let cast_ok = report
        .gates
        .iter()
        .any(|g| g.id == "two_source_one_ship_one_ray_one_clock" && g.passed);
    let remainder_ok = report
        .gates
        .iter()
        .any(|g| g.id == "remainder_in_patch_state" && g.passed);
    let compose_ok = report
        .gates
        .iter()
        .any(|g| g.id == "direct_vs_subdivided_patch" && g.passed);
    let cache_ok = report
        .gates
        .iter()
        .any(|g| g.id == "cache_reuse_matches" && g.passed);
    let inv_ok = report
        .gates
        .iter()
        .any(|g| g.id == "source_change_invalidates_certificate" && g.passed);
    gate(
        &mut report,
        "complete_patch_cast",
        cast_ok,
        "Two masses, test ship μ=0, ray, clock, compiled g; authored futures refuse.",
    );
    gate(
        &mut report,
        "source_change_consistency",
        ship && light && clock,
        "μ:1→2 is two-sided for motion, coordinate light arrival, and τ from the same g.",
    );
    gate(
        &mut report,
        "causal_dynamic_sources",
        ship,
        "Pre-cone zero influence of μ:1→2 on the ship; post-cone nonzero. This is not G2.",
    );
    gate(
        &mut report,
        "well_posed_exterior",
        remainder_ok,
        "Remainder stays in P after a step. Incomplete omit fails closed. Observation does not create geometry.",
    );
    gate(
        &mut report,
        "direct_vs_subdivided",
        compose_ok,
        "U(t2,t0,P)=U(t2,t1,U(t1,t0,P)) on the full patch state.",
    );
    gate(
        &mut report,
        "cache_reuse",
        cache_ok && inv_ok,
        "Cache key is source-history digest. Cache after INV fails. 1/16 is not a global TTL.",
    );
    gate(
        &mut report,
        "source_backreaction",
        false,
        "Sources recompile g by excluded-self GEM-a; instantaneous Newton third-law is not a rule of this law.",
    );
    gate(
        &mut report,
        "compact_field_certification",
        false,
        "H0021 absorbing fallback is specified; that is not Schwarzschild/Kerr certification.",
    );
    gate(
        &mut report,
        "terminating_exact_branches",
        false,
        "Cone/cast/remainder predicates terminate; patch metric values remain f64 until enclosed.",
    );

    report.status = "FAIL".into();
    report
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn evolving_patch_manifest_is_frozen_and_additive() {
        evolving_patch_manifest().unwrap();
        crate::causal_kernel::research_manifest().unwrap();
        crate::coupled::coupled_manifest().unwrap();
        crate::compact::compact_manifest().unwrap();
        crate::exact_branch::exact_branch_manifest().unwrap();
        crate::schwarzschild::schwarzschild_manifest().unwrap();
        crate::tiny_causal::tiny_causal_manifest().unwrap();
    }

    #[test]
    fn patch_law_is_not_an_existing_identity() {
        assert_ne!(PATCH_LAW_ID, INERTIAL_LAB_LAW_ID);
        assert_ne!(PATCH_LAW_ID, RESEARCH_LAW_ID);
        assert_ne!(PATCH_LAW_ID, COUPLED_LAW_ID);
        assert_ne!(PATCH_LAW_ID, SCHWARZSCHILD_LAW_ID);
        assert_ne!(PATCH_LAW_ID, GEM_LAW_ID);
        assert_eq!(EVOLVING_PATCH_FIXTURE_IDS.len(), 17);
        assert_eq!(NAMED_EQUATIONS.len(), 13);
    }

    #[test]
    fn spec_patch_pins_consis_geo_n_cache_without_shapiro() {
        evolving_patch_manifest().unwrap();
        assert_eq!(CONSIS_OBJECT, "compiled_g_or_phi_xi");
        assert_eq!(CONSIS_BINDING, "geo-t-geo-n-clk-g-from-p");
        assert_eq!(CONSIS_COMOVEMENT, "necessary-not-sufficient");
        assert_eq!(PRIVATE_PHI_TRIO, "fails");
        assert_eq!(GEO_N_DISCRIMINATOR, "coordinate-affine-arrival");
        assert_eq!(GEO_N_TICK_BINNING, "commit-not-falsifier");
        assert_eq!(SHAPIRO_MAGNITUDE, "not-frozen");
        assert_eq!(CERTIFICATE, "source-digest-remainder-future-cone");
        assert_eq!(CERTIFICATE_SCOPE, "per-event");
        assert_eq!(SHIP_OLD_G_DEADLINE, [1, 16]);
        assert_eq!(CACHE_KEY, "source-history-digest");
        assert_eq!(CACHE_AFTER_INV, "fail");
        assert_eq!(GEM_MAY_FILL, ["METRIC", "GEM-a", "CLK"]);
        assert_eq!(MINKOWSKI_FLIGHT, [1, 16]);
    }

    #[test]
    fn two_source_cast_has_compiled_g_and_refuses_authored_futures() {
        fixture_two_source_cast().unwrap();
        let p = laboratory(false).unwrap();
        assert_eq!(p.ship.mu, Q::zero());
        assert!(p.ray.is_some(), "laboratory P must carry a live ray");
        let ray = p.ray.as_ref().unwrap();
        assert_eq!(ray.emit_time, q(1, 8));
        assert_eq!(ray.emit_position, post_emit().position);
        assert!(
            ray.tick_delivery.is_none(),
            "laboratory ray must stay scheduled until U emits it"
        );
        assert_eq!(ray.coordinate_dt, UNFLOWN_COORDINATE_DT);
        assert!(!p.ship.worldtube.is_empty());
        assert!(shares_compiled_object(&p));
        assert_eq!(p.sources.len(), 2);
        let mut missing_ray = p.clone();
        missing_ray.ray = None;
        assert!(
            !shares_compiled_object(&missing_ray),
            "a missing ray is not bound to the object in P"
        );
    }

    #[test]
    fn u_flies_pending_laboratory_ray() {
        let p = laboratory(false).unwrap();
        let ray0 = p.ray.as_ref().unwrap();
        assert_eq!(ray0.emit_time, q(1, 8));
        assert!(ray0.tick_delivery.is_none());
        assert_eq!(ray0.coordinate_dt, UNFLOWN_COORDINATE_DT);

        let early = advance_patch(&p, q(1, 64)).unwrap();
        let early_ray = early.ray.as_ref().unwrap();
        assert_eq!(early_ray.emit_time, q(1, 8));
        assert!(
            early_ray.tick_delivery.is_none(),
            "scheduled post-cone emit must not fly before emit_time"
        );
        assert_eq!(early_ray.coordinate_dt, UNFLOWN_COORDINATE_DT);

        let at_emit = advance_patch(&p, q(1, 8)).unwrap();
        let emitted = at_emit.ray.as_ref().unwrap();
        assert_eq!(emitted.emit_time, q(1, 8));
        assert!(
            emitted.tick_delivery.is_none(),
            "arrival ≈ 1/8+1/16=3/16; emit tick must not pre-bin delivery"
        );
        let from_g = geo_n_arrival(
            &at_emit.geometry,
            stored_emit(emitted),
            emitted.receiver,
            NULL_PATH_SAMPLES,
        )
        .unwrap();
        assert_eq!(emitted.coordinate_dt.to_bits(), from_g.to_bits());
        assert!(emitted.coordinate_dt > minkowski_flight());
        bound_geo_readings(&at_emit).unwrap();

        let deliver_at = tick_containing(emitted.affine_arrival);
        assert!(deliver_at > q(1, 8));
        let done = advance_patch(&p, deliver_at).unwrap();
        let ray = done.ray.as_ref().unwrap();
        assert_eq!(ray.tick_delivery, Some(deliver_at));
        let frozen = ray.coordinate_dt;
        let later = advance_patch(&done, done.time + dt_q()).unwrap();
        assert_eq!(
            later.ray.as_ref().unwrap().coordinate_dt.to_bits(),
            frozen.to_bits(),
            "bind_observables must not overwrite flown dt after delivery"
        );

        let pd = laboratory(true).unwrap();
        let postd = advance_patch(&pd, q(1, 8)).unwrap();
        let rd = postd.ray.as_ref().unwrap();
        assert_ne!(
            rd.coordinate_dt.to_bits(),
            emitted.coordinate_dt.to_bits(),
            "flown P_Δ.ray must see μ:1→2"
        );
        let from_gd = geo_n_arrival(
            &postd.geometry,
            stored_emit(rd),
            rd.receiver,
            NULL_PATH_SAMPLES,
        )
        .unwrap();
        assert_eq!(rd.coordinate_dt.to_bits(), from_gd.to_bits());
        bound_geo_readings(&postd).unwrap();
    }

    #[test]
    fn source_change_is_two_sided_for_ship_light_and_clock() {
        let (pre, post) = fixture_source_change_moves_ship().unwrap();
        assert_eq!(pre, 0.0);
        assert!(post > 0.0, "post-cone ship influence {post}");
        let (dt_delta, mink, dt_base) = fixture_source_change_delays_light().unwrap();
        assert!(dt_delta > mink, "Δt={dt_delta} mink={mink}");
        assert_ne!(dt_delta.to_bits(), dt_base.to_bits());
        let (pre0, pred, post0, postd) = fixture_source_change_shifts_clock().unwrap();
        assert_eq!(pre0, pred);
        assert_ne!(post0, postd);
    }

    #[test]
    fn same_metric_object_and_private_trio_fails() {
        assert!(fixture_same_metric_consistency().unwrap());
    }

    #[test]
    fn direct_equals_subdivided_and_cache_matches() {
        assert!(fixture_direct_vs_subdivided().unwrap());
        assert!(fixture_cache_reuse().unwrap());
        assert!(fixture_invalidates_certificate().unwrap());
    }

    #[test]
    fn remainder_cast_budget_clock_observation() {
        assert!(fixture_remainder_survives().unwrap());
        assert!(fixture_third_massive_refuses());
        assert!(fixture_budget_exhausted());
        assert!(fixture_inertial_clock_phi_zero().unwrap());
        assert!(fixture_observation_does_not_recompile().unwrap());
    }

    #[test]
    fn named_negatives_stay_negative() {
        assert!(fixture_minkowski_negative().unwrap());
        assert!(fixture_delayed_newton_negative().unwrap());
        assert!(fixture_schwarzschild_negative());
        assert!(fixture_gem_force_without_null().unwrap());
        assert!(advance_map().is_err());
    }

    #[test]
    fn spec_qualify_does_not_promote() {
        let report = qualify_evolving_patch_spec();
        assert_eq!(report.id, PATCH_LAW_ID);
        assert_eq!(report.status, "FAIL");
        assert!(report
            .gates
            .iter()
            .any(|g| g.id == "evolving_patch_manifest_isolated" && g.passed));
        for id in [
            "compact_field_certification",
            "terminating_exact_branches",
            "source_backreaction",
        ] {
            let gate = report.gates.iter().find(|g| g.id == id).unwrap();
            assert!(!gate.passed, "{id} must remain failed");
        }
        for id in [
            "two_source_one_ship_one_ray_one_clock",
            "source_change_moves_ship",
            "source_change_delays_light",
            "source_change_shifts_clock",
            "same_metric_consistency",
            "direct_vs_subdivided_patch",
            "cache_reuse_matches",
            "source_change_invalidates_certificate",
            "remainder_in_patch_state",
            "unsupported_third_massive_refuses",
            "budget_exhausted_not_a_geodesic",
            "inertial_clock_when_phi_zero",
            "observation_does_not_recompile",
            "minkowski_signal_not_metric_null",
            "delayed_newton_not_the_patch",
            "schwarzschild_classifier_not_evolving_patch",
            "gem_force_without_null_geodesic_fails_consistency",
            "complete_patch_cast",
            "source_change_consistency",
            "causal_dynamic_sources",
            "well_posed_exterior",
            "direct_vs_subdivided",
            "cache_reuse",
        ] {
            let gate = report.gates.iter().find(|g| g.id == id).unwrap();
            assert!(
                gate.passed,
                "{id} should pass on the patch map: {}",
                gate.reason
            );
        }
    }

    #[test]
    fn static_fill_is_three_dimensional_planar() {
        let p = laboratory(false).unwrap();
        let field = p.geometry.phi_xi(ship_event(Q::zero()), None).unwrap();
        let newton_a = gravitational_acceleration([4.0, 0.0], 1.0).unwrap();
        let newton_b = gravitational_acceleration([-4.0, 0.0], 1.0).unwrap();
        assert!((field.e[0] - (newton_a[0] + newton_b[0])).abs() < 1e-12);
        assert!((field.e[1] - (newton_a[1] + newton_b[1])).abs() < 1e-12);
        assert!((field.phi - (-0.5)).abs() < 1e-12);
        assert_eq!(field.xi, [0.0, 0.0]);
    }
}

/// Crate-private reuse shims for the amortized-evaluator probe. Zero new
/// behavior: every item forwards to the exact canonical helper in this file,
/// so a same-law accelerated driver can share its update semantics without
/// widening the law's public API.
pub(crate) mod internal {
    use super::super::causal_kernel::{CompactClass, KernelEvent};
    use super::{
        CompiledGeometry, EvolvingPatchError, NullRay, PatchSegment, PatchSource, PatchState,
    };

    pub(crate) type Q = super::Q;

    pub(crate) const NULL_PATH_SAMPLES: u32 = super::NULL_PATH_SAMPLES;

    pub(crate) fn dt_f() -> f64 {
        super::dt_f()
    }

    pub(crate) fn c_f() -> f64 {
        super::c_f()
    }

    pub(crate) fn is_tick(t: Q) -> bool {
        super::is_tick(t)
    }

    pub(crate) fn round_q(x: f64) -> Result<Q, EvolvingPatchError> {
        super::round_q(x)
    }

    pub(crate) fn last_segment(
        source: &PatchSource,
    ) -> Result<&PatchSegment, EvolvingPatchError> {
        super::last_segment(source)
    }

    pub(crate) fn segment_visible(seg: &PatchSegment, query: KernelEvent) -> bool {
        super::segment_visible(seg, query)
    }

    pub(crate) fn null_path_samples(
        emit: KernelEvent,
        receiver: [Q; 2],
        max_steps: u32,
    ) -> Result<Vec<(KernelEvent, f64, [f64; 2])>, EvolvingPatchError> {
        super::null_path_samples(emit, receiver, max_steps)
    }

    pub(crate) fn clock_rate_from_phi(
        phi: f64,
        velocity: [f64; 2],
    ) -> Result<Q, EvolvingPatchError> {
        super::clock_rate_from_phi(phi, velocity)
    }

    pub(crate) fn commit_ray_on_containing_tick(ray: &mut NullRay, t_start: Q, t_end: Q) {
        super::commit_ray_on_containing_tick(ray, t_start, t_end)
    }

    pub(crate) fn recompile(p: &mut PatchState) -> Result<(), EvolvingPatchError> {
        super::recompile(p)
    }

    pub(crate) fn validate_cast(p: &PatchState) -> Result<(), EvolvingPatchError> {
        super::validate_cast(p)
    }

    /// Used by the parity tests and probe harness, not the live driver.
    #[allow(dead_code)]
    pub(crate) fn canonical_eq(a: &PatchState, b: &PatchState) -> bool {
        super::canonical_eq(a, b)
    }

    /// Exact canonical step retained for differential checks.
    #[allow(dead_code)]
    pub(crate) fn step_one_with(
        p: &PatchState,
        g: &CompiledGeometry,
    ) -> Result<PatchState, EvolvingPatchError> {
        super::step_one_with(p, g)
    }

    pub(crate) fn compile(
        sources: Vec<PatchSource>,
        remainder: super::OmittedTailBound,
        changes: Vec<KernelEvent>,
    ) -> CompiledGeometry {
        CompiledGeometry::compile(sources, remainder, changes)
    }

    pub(crate) fn capture_at(
        g: &CompiledGeometry,
        event: KernelEvent,
        exclude: Option<u64>,
    ) -> Result<Option<(u64, CompactClass)>, EvolvingPatchError> {
        g.capture_at(event, exclude)
    }
}
