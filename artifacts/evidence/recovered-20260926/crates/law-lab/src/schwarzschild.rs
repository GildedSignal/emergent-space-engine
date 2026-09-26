//! Isolated Schwarzschild equatorial compact map.
//!
//! Law id: `es-schwarzschild-equatorial-v0`. Planar restriction of **3D
//! Schwarzschild** as a **stationary one-source compact patch**. This is never
//! `es-inertial-causal-v1`, not Kerr, not interacting GR, not 2D logarithmic
//! gravity, and not delayed Newton. It does not promote.
//!
//! # Candidate contract
//!
//! **Domain.** One static source, equatorial geodesics. From-infinity null
//! classification uses a conserved impact invariant `b²`. The geodesic IVP is
//! exact-or-fail-closed on a rational equatorial x-axis: symplectic identity
//! on circular null (photon sphere) and exact circular timelike, plus L=0
//! radial capture. Source μ is the latest segment in the closed past light
//! cone. A moving or two-source geodesic query fails closed. On/inside
//! `r_s=2μ/c²` the H0021 absorbing capture map remains the fallback.
//!
//! **Terminating oracles (one rational comparison, max_steps=1).**
//! - Photon sphere `r_ph=3μ/c²`: compare `r² c⁴ ≶ 9μ²`. Tie: OnPhotonSphere.
//! - Capture cross-section from infinity: compare `b² c⁴ ≶ 27μ²`. Tie:
//!   UnstablePhotonSphere. (Geometric `σ=π b_c²` is not required; `π` is not
//!   a laboratory rational.)
//! - Weak-field light deflection `4μ/(c²b)` on frozen `b≥4`. Exact elliptic
//!   deflection and the scatter turning-radius cubic `r³-b²r+b² r_s=0` fail
//!   closed. An iteration cap is a failed execution, never a guessed root.
//!
//! **Geodesic IVP (exact or fail closed).**
//! - Null capture / scatter / unstable photon orbit from finite-r data: the
//!   cubic *sign* `r³-b²r+b² r_s ≶ 0` plus `r ≶ r_ph` and `b² ≶ b_c²`.
//!   Solving for the turning *root* still fails closed.
//! - Circular identity: `(r, p_r)` stay put at the photon sphere (null) or
//!   when the exact timelike circular identity `L²(r-3M)=M r²` holds.
//! - Radial `L=0` rest/inward is capture. Generic scatter trajectory /
//!   elliptic deflection fail closed. Off-axis radius (laboratory square
//!   root) fails closed.
//!
//! **Causality.** A source-μ change is invisible inside the cone (Scatter /
//! vacuum for genesis μ=0) and visible after. Stationary Verlet/lapse still
//! fail that first gate; this patch must not.
//!
//! **Not claimed.** Interacting compact-body GR, Kerr, elliptic deflection,
//! FMM, clocks, or production compact-field / exact-branch certification.
//! `production_law` stays null. G2 still FAIL.
use super::causal_kernel::{
    compact_map, compact_radius, finite_root, genesis, in_closed_past_cone, mass_change_influence,
    origin, q, qf, r4, record_well_posed_exterior, tube, CausalKernel, CompactClass, CompactMap,
    KernelError, KernelEvent, SourceSegment, SourceWorldtube, C, INERTIAL_LAB_LAW_ID,
    POST_LIGHTCONE_INFLUENCE_MIN, Q, RESEARCH_LAW_ID,
};
use super::coupled::COUPLED_LAW_ID;
use super::exact_branch::{TerminatingDecision, MAX_PREDICATE_STEPS, STATIONARY_CROSSING_CAP};
use super::{gate, CandidateReport, Metric};
use num_traits::Zero;
use serde::Deserialize;
use std::fmt::Write as _;

pub const SCHWARZSCHILD_LAW_ID: &str = "es-schwarzschild-equatorial-v0";

const MANIFEST: &str = include_str!("../../../scenarios/law-gates.json");

const TIE_PHOTON: &str = "r²c⁴ = 9μ² is OnPhotonSphere";
const TIE_CAPTURE: &str = "b²c⁴ = 27μ² is UnstablePhotonSphere";
const TIE_HORIZON: &str = "r≤r_s uses absorbing capture (H0021); r=0 refuses Singular";
const TIE_DOMAIN: &str = "moving or multi-source geodesic queries refuse; they do not guess GR";
const TIE_TURNING: &str = "scatter turning radius is an unsupported cubic root; fail closed";
const TIE_CAP: &str = "exhausted budget is failed execution, not a guessed turning root";
const TIE_IVP: &str = "circular identity is exact; generic scatter elliptic/turning-root refuse; iteration cap is not a fate";
const TIE_RADIUS: &str =
    "geodesic IVP radius must be a rational equatorial x-axis value; no square root";

const CAPTURE_INVARIANT: i128 = 27;
const CRITICAL_B2: [i128; 2] = [27, 16_777_216];
const PHOTON_SPHERE: [i128; 2] = [3, 4096];
const ISCO_RADIUS: [i128; 2] = [3, 2048];
const WEAK_FIELD_B_MIN: [i128; 2] = [4, 1];
const WEAK_FIELD_DEFLECTION: [i128; 2] = [1, 4096];
const IVP_DOMAIN: &str = "equatorial-circular-radial-exact-or-fail-closed";

#[derive(Clone, Deserialize)]
struct FileSlice {
    schwarzschild_equatorial_research: SchwarzschildManifest,
    compact_field_research: CompactSlice,
    terminating_exact_branches_research: ExactSlice,
    required_production_gates: Vec<String>,
}

#[derive(Clone, Deserialize)]
struct CompactSlice {
    fixtures: Vec<NamedFixture>,
}

#[derive(Clone, Deserialize)]
struct ExactSlice {
    fixtures: Vec<NamedFixture>,
}

#[derive(Clone, Deserialize)]
struct SchwarzschildManifest {
    law_id: String,
    gate: String,
    parent_kernel: String,
    coupled_kernel: String,
    fallback: String,
    domain: String,
    ivp: String,
    light_speed: i128,
    mu: [i128; 2],
    compact_radius: [i128; 2],
    photon_sphere: [i128; 2],
    isco_radius: [i128; 2],
    capture_invariant: i128,
    critical_b2: [i128; 2],
    weak_field_impact_min: [i128; 2],
    weak_field_deflection: [i128; 2],
    max_predicate_steps: u32,
    stationary_crossing_cap: u32,
    fixtures: Vec<NamedFixture>,
}

#[derive(Clone, Deserialize)]
struct NamedFixture {
    id: String,
}

pub(crate) const SCHWARZSCHILD_FIXTURE_IDS: [&str; 18] = [
    "exact_photon_sphere",
    "null_capture_cross_section",
    "effective_potential_max_at_photon_sphere",
    "weak_field_deflection_is_4mu",
    "newton_flyby_not_4mu",
    "causal_schwarzschild_after_cone",
    "horizon_absorbing_fallback",
    "moving_source_geodesic_fails_closed",
    "two_source_geodesic_fails_closed",
    "turning_root_fails_closed",
    "iteration_cap_not_turning_sign",
    "null_geodesic_ivp_capture_scatter_photon",
    "circular_null_identity_step",
    "circular_timelike_isco_identity_step",
    "radial_timelike_rest_is_capture",
    "generic_scatter_trajectory_fails_closed",
    "causal_geodesic_ivp_after_cone",
    "irrational_radius_fails_closed",
];

/// Exact photon-sphere class for `r_ph = 3μ/c²`, compared as `r² c⁴ ≶ 9μ²`.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum PhotonSphereClass {
    Outside,
    OnPhotonSphere,
    Inside,
}

/// From-infinity equatorial null branch. Compared as `b² c⁴ ≶ 27μ²`.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum NullFromInfinity {
    Capture,
    UnstablePhotonSphere,
    Scatter,
}

/// Tiny exact-or-fail-closed stepper on the declared domain.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum EquatorialStep {
    Singular,
    HorizonCapture { class: CompactClass },
    Null(NullFromInfinity),
}

/// Null or timelike equatorial geodesic IVP.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum GeodesicKind {
    Null,
    Timelike,
}

/// Sign of `ṙ` without taking a laboratory square root.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum RadialSense {
    Inward,
    Rest,
    Outward,
}

/// Conserved invariant plus radial sense. Null uses `b²`; timelike uses `L²`.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct GeodesicSpec {
    pub kind: GeodesicKind,
    pub invariant: Q,
    pub radial: RadialSense,
}

/// Exact-or-fail-closed geodesic IVP outcome. Generic scatter is classified
/// here; integrating it is a separate unsupported predicate.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum GeodesicOutcome {
    Singular,
    HorizonCapture { class: CompactClass },
    CircularIdentity { kind: GeodesicKind, radius: Q },
    Capture,
    Scatter,
    UnstablePhotonOrbit,
}

fn one_step<T>(decision: Result<T, KernelError>, tie_rule: &'static str) -> TerminatingDecision<T> {
    TerminatingDecision {
        decision,
        steps: MAX_PREDICATE_STEPS,
        max_steps: MAX_PREDICATE_STEPS,
        tie_rule,
    }
}

pub fn schwarzschild_manifest() -> Result<(), String> {
    let slice: FileSlice = serde_json::from_str(MANIFEST).map_err(|e| e.to_string())?;
    let m = &slice.schwarzschild_equatorial_research;
    if m.law_id != SCHWARZSCHILD_LAW_ID {
        return Err("schwarzschild law id drifted".into());
    }
    if m.law_id == INERTIAL_LAB_LAW_ID || m.law_id == RESEARCH_LAW_ID || m.law_id == COUPLED_LAW_ID
    {
        return Err("schwarzschild kernel must keep a distinct research id".into());
    }
    if m.gate != "compact_field_certification" {
        return Err(
            "schwarzschild production compact gate must remain compact_field_certification".into(),
        );
    }
    if m.parent_kernel != RESEARCH_LAW_ID {
        return Err("schwarzschild parent must remain the retarded monopole kernel".into());
    }
    if m.coupled_kernel != COUPLED_LAW_ID {
        return Err("schwarzschild coupled kernel id drifted".into());
    }
    if m.fallback != "absorbing-capture-h0021"
        || m.domain != "equatorial-one-static-source-null-from-infinity"
        || m.ivp != IVP_DOMAIN
    {
        return Err("schwarzschild declared domain, IVP domain, or H0021 fallback drifted".into());
    }
    if m.light_speed != C
        || m.mu != [1, 1]
        || m.compact_radius != [1, 2048]
        || m.photon_sphere != PHOTON_SPHERE
        || m.isco_radius != ISCO_RADIUS
        || m.capture_invariant != CAPTURE_INVARIANT
        || m.critical_b2 != CRITICAL_B2
        || m.weak_field_impact_min != WEAK_FIELD_B_MIN
        || m.weak_field_deflection != WEAK_FIELD_DEFLECTION
        || m.max_predicate_steps != MAX_PREDICATE_STEPS
        || m.stationary_crossing_cap != STATIONARY_CROSSING_CAP
    {
        return Err("schwarzschild research thresholds were weakened or retuned".into());
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
    let ids: Vec<&str> = m.fixtures.iter().map(|f| f.id.as_str()).collect();
    if ids != SCHWARZSCHILD_FIXTURE_IDS {
        return Err("schwarzschild fixtures were renamed, dropped or reordered".into());
    }
    let compact_ids: Vec<&str> = slice
        .compact_field_research
        .fixtures
        .iter()
        .map(|f| f.id.as_str())
        .collect();
    if compact_ids != crate::compact::COMPACT_FIXTURE_IDS {
        return Err("existing compact-field fixtures were renamed, dropped or reordered".into());
    }
    let exact_ids: Vec<&str> = slice
        .terminating_exact_branches_research
        .fixtures
        .iter()
        .map(|f| f.id.as_str())
        .collect();
    if exact_ids != crate::exact_branch::EXACT_BRANCH_FIXTURE_IDS {
        return Err("existing exact-branch fixtures were renamed, dropped or reordered".into());
    }
    let rs = compact_radius(q(1, 1), C).ok_or("unit compact radius")?;
    if rs != q(1, 2048) || photon_sphere_radius(q(1, 1), C) != Some(q(3, 4096)) {
        return Err("unit photon sphere is not the exact rational 3μ/c² = 3/4096".into());
    }
    if isco_radius(q(1, 1), C) != Some(q(ISCO_RADIUS[0], ISCO_RADIUS[1])) {
        return Err("unit ISCO is not the exact rational 6μ/c² = 3/2048".into());
    }
    if critical_b2(q(1, 1), C) != q(CRITICAL_B2[0], CRITICAL_B2[1]) {
        return Err("unit critical b² is not the exact rational 27μ²/c⁴".into());
    }
    Ok(())
}

/// Photon sphere `r_ph = 3μ/c²`.
pub fn photon_sphere_radius(mu: Q, c: i128) -> Option<Q> {
    if mu <= Q::zero() {
        None
    } else {
        Some(Q::from_integer(3) * mu / Q::from_integer(c * c))
    }
}

/// Innermost stable circular orbit `r_isco = 6μ/c²`.
pub fn isco_radius(mu: Q, c: i128) -> Option<Q> {
    if mu <= Q::zero() {
        None
    } else {
        Some(Q::from_integer(6) * mu / Q::from_integer(c * c))
    }
}

/// Critical from-infinity impact invariant `b_c² = 27 μ² / c⁴`.
pub fn critical_b2(mu: Q, c: i128) -> Q {
    Q::from_integer(CAPTURE_INVARIANT) * mu * mu / Q::from_integer(c * c) / Q::from_integer(c * c)
}

fn displacement_r2(displacement: [Q; 2]) -> Q {
    displacement[0] * displacement[0] + displacement[1] * displacement[1]
}

fn c4(c: i128) -> Q {
    let c2 = Q::from_integer(c * c);
    c2 * c2
}

/// Exact photon-sphere class. Tie: OnPhotonSphere.
pub fn photon_sphere_class(displacement: [Q; 2], mu: Q, c: i128) -> PhotonSphereClass {
    if mu <= Q::zero() {
        return PhotonSphereClass::Outside;
    }
    let lhs = displacement_r2(displacement) * c4(c);
    let rhs = Q::from_integer(9) * mu * mu;
    if lhs > rhs {
        PhotonSphereClass::Outside
    } else if lhs == rhs {
        PhotonSphereClass::OnPhotonSphere
    } else {
        PhotonSphereClass::Inside
    }
}

/// Exact from-infinity null branch. Tie: UnstablePhotonSphere.
pub fn null_from_infinity(b2: Q, mu: Q, c: i128) -> NullFromInfinity {
    if mu <= Q::zero() {
        return NullFromInfinity::Scatter;
    }
    let lhs = b2 * c4(c);
    let rhs = Q::from_integer(CAPTURE_INVARIANT) * mu * mu;
    if lhs < rhs {
        NullFromInfinity::Capture
    } else if lhs == rhs {
        NullFromInfinity::UnstablePhotonSphere
    } else {
        NullFromInfinity::Scatter
    }
}

/// Weak-field GR light deflection `4μ/(c²b)` on frozen `b≥4`.
pub fn weak_field_light_deflection(mu: Q, c: i128, b: Q) -> Result<Q, KernelError> {
    if mu < Q::zero() || b <= Q::zero() {
        return Err(KernelError::Invalid(
            "weak-field deflection requires nonnegative μ and positive b",
        ));
    }
    if b < q(WEAK_FIELD_B_MIN[0], WEAK_FIELD_B_MIN[1]) {
        return Err(KernelError::UnsupportedPredicate(
            "weak-field deflection oracle requires b≥4; exact elliptic deflection is unsupported",
        ));
    }
    Ok(Q::from_integer(4) * mu / (Q::from_integer(c * c) * b))
}

fn newton_hyperbolic_deflection(mu: f64, c: f64, impact: f64) -> f64 {
    let eccentricity = (1.0 + (c * c * impact / mu).powi(2)).sqrt();
    2.0 * (1.0 / eccentricity).asin()
}

fn gr_weak_light_deflection_f64(mu: f64, c: f64, impact: f64) -> f64 {
    4.0 * mu / (c * c * impact)
}

/// Null effective potential `V=(r-r_s)/r³` compared without division.
fn null_potential_greater(left: Q, right: Q, rs: Q) -> bool {
    (left - rs) * right * right * right > (right - rs) * left * left * left
}

/// Scatter turning radius `r³ - b² r + b² r_s = 0` has no rational certificate.
pub fn decide_turning_radius(b2: Q, mu: Q, c: i128, max_steps: u32) -> TerminatingDecision<Q> {
    if max_steps < MAX_PREDICATE_STEPS {
        return TerminatingDecision {
            decision: Err(KernelError::BranchBudgetExhausted { max_steps }),
            steps: max_steps,
            max_steps,
            tie_rule: TIE_CAP,
        };
    }
    let _ = (b2, mu, c);
    one_step(
        Err(KernelError::UnsupportedPredicate(
            "Schwarzschild scatter turning radius is an unsupported cubic root; fail closed",
        )),
        TIE_TURNING,
    )
}

/// A guessed turning root after a cap hit is illegal.
pub fn turning_radius_iteration_cap(
    exhausted: bool,
    guessed: Q,
    cap: u32,
) -> Result<Q, KernelError> {
    if exhausted {
        let _ = guessed;
        Err(KernelError::BranchBudgetExhausted { max_steps: cap })
    } else {
        Ok(guessed)
    }
}

fn c2(c: i128) -> Q {
    Q::from_integer(c * c)
}

/// Exact timelike circular identity `L²(r − 3M) = M r²` with `M=μ/c²`.
/// Compared as `L²(r c² − 3μ) = μ r²` without division.
pub fn is_exact_timelike_circular(radius: Q, ang2: Q, mu: Q, c: i128) -> bool {
    if mu <= Q::zero() || radius <= Q::zero() || ang2 < Q::zero() {
        return false;
    }
    let r_c2 = radius * c2(c);
    let three_mu = Q::from_integer(3) * mu;
    r_c2 > three_mu && ang2 * (r_c2 - three_mu) == mu * radius * radius
}

/// Null radial cubic `r³ − b² r + b² r_s`. Sign classifies allowed motion;
/// a zero is a turning point or the photon sphere. The unknown root is not solved.
fn null_radial_cubic(radius: Q, b2: Q, rs: Q) -> Q {
    radius * radius * radius - b2 * radius + b2 * rs
}

fn rational_equatorial_radius(displacement: [Q; 2]) -> Result<Q, KernelError> {
    if displacement[1] != Q::zero() {
        return Err(KernelError::UnsupportedPredicate(
            "geodesic IVP requires a rational equatorial radius (y=0); a generic 2D radius is not a laboratory square root",
        ));
    }
    if displacement[0] < Q::zero() {
        return Err(KernelError::Invalid(
            "equatorial geodesic radius must be nonnegative",
        ));
    }
    Ok(displacement[0])
}

fn classify_null_ivp(
    radius: Q,
    b2: Q,
    radial: RadialSense,
    mu: Q,
    c: i128,
) -> Result<GeodesicOutcome, KernelError> {
    if b2 < Q::zero() || radius < Q::zero() {
        return Err(KernelError::Invalid(
            "null geodesic IVP requires nonnegative radius and b²",
        ));
    }
    if mu <= Q::zero() {
        return Ok(GeodesicOutcome::Scatter);
    }
    let rs = compact_radius(mu, c).ok_or(KernelError::Invalid("compact radius"))?;
    if radius == Q::zero() {
        return Ok(GeodesicOutcome::Singular);
    }
    if radius <= rs {
        let class = if radius * radius * c4(c) == Q::from_integer(4) * mu * mu {
            CompactClass::OnHorizon
        } else {
            CompactClass::Interior
        };
        return Ok(GeodesicOutcome::HorizonCapture { class });
    }
    let cubic = null_radial_cubic(radius, b2, rs);
    match radial {
        RadialSense::Rest if cubic != Q::zero() => {
            return Err(KernelError::Invalid(
                "null rest requires a turning or circular root (cubic = 0)",
            ));
        }
        RadialSense::Inward | RadialSense::Outward if cubic == Q::zero() => {
            return Err(KernelError::Invalid(
                "null turning/circular root requires rest (ṙ = 0)",
            ));
        }
        _ if cubic < Q::zero() => {
            return Err(KernelError::Invalid(
                "null geodesic IVP data is in the forbidden potential well",
            ));
        }
        _ => {}
    }
    let r_c2 = radius * c2(c);
    let three_mu = Q::from_integer(3) * mu;
    let vs_photon = r_c2.cmp(&three_mu);
    let vs_critical = (b2 * c4(c)).cmp(&(Q::from_integer(CAPTURE_INVARIANT) * mu * mu));
    match (vs_critical, vs_photon, radial) {
        (std::cmp::Ordering::Less, _, RadialSense::Inward) => Ok(GeodesicOutcome::Capture),
        (std::cmp::Ordering::Less, _, RadialSense::Outward) => Ok(GeodesicOutcome::Scatter),
        (std::cmp::Ordering::Equal, std::cmp::Ordering::Equal, RadialSense::Rest) => {
            Ok(GeodesicOutcome::CircularIdentity {
                kind: GeodesicKind::Null,
                radius,
            })
        }
        (std::cmp::Ordering::Equal, std::cmp::Ordering::Greater, RadialSense::Inward)
        | (std::cmp::Ordering::Equal, std::cmp::Ordering::Less, RadialSense::Outward) => {
            Ok(GeodesicOutcome::UnstablePhotonOrbit)
        }
        (std::cmp::Ordering::Equal, std::cmp::Ordering::Greater, RadialSense::Outward) => {
            Ok(GeodesicOutcome::Scatter)
        }
        (std::cmp::Ordering::Equal, std::cmp::Ordering::Less, RadialSense::Inward) => {
            Ok(GeodesicOutcome::Capture)
        }
        (std::cmp::Ordering::Greater, std::cmp::Ordering::Greater, _) => {
            Ok(GeodesicOutcome::Scatter)
        }
        (std::cmp::Ordering::Greater, std::cmp::Ordering::Less, _) => Ok(GeodesicOutcome::Capture),
        _ => Err(KernelError::Invalid(
            "null geodesic IVP combination is not a supported exact branch",
        )),
    }
}

fn classify_timelike_ivp(
    radius: Q,
    ang2: Q,
    radial: RadialSense,
    mu: Q,
    c: i128,
) -> Result<GeodesicOutcome, KernelError> {
    if ang2 < Q::zero() || radius < Q::zero() {
        return Err(KernelError::Invalid(
            "timelike geodesic IVP requires nonnegative radius and L²",
        ));
    }
    if mu <= Q::zero() {
        return Ok(GeodesicOutcome::Scatter);
    }
    let rs = compact_radius(mu, c).ok_or(KernelError::Invalid("compact radius"))?;
    if radius == Q::zero() {
        return Ok(GeodesicOutcome::Singular);
    }
    if radius <= rs {
        let class = if radius * radius * c4(c) == Q::from_integer(4) * mu * mu {
            CompactClass::OnHorizon
        } else {
            CompactClass::Interior
        };
        return Ok(GeodesicOutcome::HorizonCapture { class });
    }
    if ang2 == Q::zero() {
        return match radial {
            RadialSense::Outward => Err(KernelError::Invalid(
                "timelike L=0 rest energy cannot be outward",
            )),
            RadialSense::Rest | RadialSense::Inward => Ok(GeodesicOutcome::Capture),
        };
    }
    if radial == RadialSense::Rest && is_exact_timelike_circular(radius, ang2, mu, c) {
        return Ok(GeodesicOutcome::CircularIdentity {
            kind: GeodesicKind::Timelike,
            radius,
        });
    }
    Err(KernelError::UnsupportedPredicate(
        "generic timelike scatter/bound geodesic (turning cubic / elliptic) is unsupported; fail closed",
    ))
}

/// Exact-or-fail-closed equatorial geodesic IVP. One step classifies or
/// applies a circular identity; it does not iterate toward a turning point.
pub fn step_equatorial_geodesic(
    kernel: &CausalKernel,
    query: KernelEvent,
    spec: GeodesicSpec,
    max_steps: u32,
) -> TerminatingDecision<GeodesicOutcome> {
    if max_steps < MAX_PREDICATE_STEPS {
        return TerminatingDecision {
            decision: Err(KernelError::BranchBudgetExhausted { max_steps }),
            steps: max_steps,
            max_steps,
            tie_rule: TIE_CAP,
        };
    }
    if spec.invariant < Q::zero() {
        return one_step(
            Err(KernelError::Invalid(
                "geodesic invariant b²/L² must be nonnegative",
            )),
            TIE_IVP,
        );
    }
    let source = match equatorial_source(kernel) {
        Ok(source) => source,
        Err(error) => return one_step(Err(error), TIE_DOMAIN),
    };
    let Some(source) = source else {
        return one_step(Ok(GeodesicOutcome::Scatter), TIE_IVP);
    };
    let Some(seg) = visible_segment(kernel, source, query) else {
        return one_step(Ok(GeodesicOutcome::Scatter), TIE_IVP);
    };
    match compact_map(seg, query, kernel.light_speed) {
        CompactMap::Singular => return one_step(Ok(GeodesicOutcome::Singular), TIE_HORIZON),
        CompactMap::Captured { class } => {
            return one_step(Ok(GeodesicOutcome::HorizonCapture { class }), TIE_HORIZON);
        }
        CompactMap::Exterior => {}
    }
    let displacement = [
        query.position[0] - seg.position[0],
        query.position[1] - seg.position[1],
    ];
    let radius = match rational_equatorial_radius(displacement) {
        Ok(radius) => radius,
        Err(error) => {
            let tie = if matches!(error, KernelError::UnsupportedPredicate(_)) {
                TIE_RADIUS
            } else {
                TIE_IVP
            };
            return one_step(Err(error), tie);
        }
    };
    let decision = match spec.kind {
        GeodesicKind::Null => classify_null_ivp(
            radius,
            spec.invariant,
            spec.radial,
            seg.mu,
            kernel.light_speed,
        ),
        GeodesicKind::Timelike => classify_timelike_ivp(
            radius,
            spec.invariant,
            spec.radial,
            seg.mu,
            kernel.light_speed,
        ),
    };
    one_step(decision, TIE_IVP)
}

/// Generic scatter trajectory / elliptic deflection. Always fail closed.
pub fn integrate_equatorial_scatter(
    kernel: &CausalKernel,
    query: KernelEvent,
    spec: GeodesicSpec,
    max_steps: u32,
) -> TerminatingDecision<Q> {
    if max_steps < MAX_PREDICATE_STEPS {
        return TerminatingDecision {
            decision: Err(KernelError::BranchBudgetExhausted { max_steps }),
            steps: max_steps,
            max_steps,
            tie_rule: TIE_CAP,
        };
    }
    let _ = (query, spec);
    match equatorial_source(kernel) {
        Err(error) => one_step(Err(error), TIE_DOMAIN),
        Ok(_) => one_step(
            Err(KernelError::UnsupportedPredicate(
                "generic Schwarzschild scatter trajectory / elliptic deflection is unsupported; fail closed",
            )),
            TIE_IVP,
        ),
    }
}

fn static_source(tube: &SourceWorldtube) -> Result<[Q; 2], KernelError> {
    let position = tube.segments[0].position;
    if tube.segments.iter().any(|seg| seg.position != position) {
        Err(KernelError::UnsupportedPredicate(
            "schwarzschild equatorial domain requires one static source; moving source is not stationary-patch GR",
        ))
    } else {
        Ok(position)
    }
}

fn equatorial_source(kernel: &CausalKernel) -> Result<Option<&SourceWorldtube>, KernelError> {
    match kernel.sources.as_slice() {
        [] => Ok(None),
        [one] => {
            static_source(one)?;
            Ok(Some(one))
        }
        _ => Err(KernelError::UnsupportedPredicate(
            "schwarzschild equatorial domain is one static source; interacting compact-body GR is unsupported",
        )),
    }
}

fn visible_segment(
    kernel: &CausalKernel,
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
            kernel.light_speed,
        )
    })
}

/// Tiny stepper: H0021 fallback on/inside `r_s`, else from-infinity null class.
pub fn step_equatorial_null(
    kernel: &CausalKernel,
    query: KernelEvent,
    b2: Q,
) -> TerminatingDecision<EquatorialStep> {
    if b2 < Q::zero() {
        return one_step(
            Err(KernelError::Invalid(
                "impact invariant b² must be nonnegative",
            )),
            TIE_CAPTURE,
        );
    }
    let source = match equatorial_source(kernel) {
        Ok(source) => source,
        Err(error) => return one_step(Err(error), TIE_DOMAIN),
    };
    let Some(source) = source else {
        return one_step(
            Ok(EquatorialStep::Null(NullFromInfinity::Scatter)),
            TIE_CAPTURE,
        );
    };
    let Some(seg) = visible_segment(kernel, source, query) else {
        return one_step(
            Ok(EquatorialStep::Null(NullFromInfinity::Scatter)),
            TIE_CAPTURE,
        );
    };
    match compact_map(seg, query, kernel.light_speed) {
        CompactMap::Singular => one_step(Ok(EquatorialStep::Singular), TIE_HORIZON),
        CompactMap::Captured { class } => {
            one_step(Ok(EquatorialStep::HorizonCapture { class }), TIE_HORIZON)
        }
        CompactMap::Exterior => one_step(
            Ok(EquatorialStep::Null(null_from_infinity(
                b2,
                seg.mu,
                kernel.light_speed,
            ))),
            TIE_CAPTURE,
        ),
    }
}

pub fn decide_photon_sphere(
    kernel: &CausalKernel,
    query: KernelEvent,
) -> TerminatingDecision<PhotonSphereClass> {
    let source = match equatorial_source(kernel) {
        Ok(source) => source,
        Err(error) => return one_step(Err(error), TIE_DOMAIN),
    };
    let Some(source) = source else {
        return one_step(Ok(PhotonSphereClass::Outside), TIE_PHOTON);
    };
    let Some(seg) = visible_segment(kernel, source, query) else {
        return one_step(Ok(PhotonSphereClass::Outside), TIE_PHOTON);
    };
    let displacement = [
        query.position[0] - seg.position[0],
        query.position[1] - seg.position[1],
    ];
    one_step(
        Ok(photon_sphere_class(
            displacement,
            seg.mu,
            kernel.light_speed,
        )),
        TIE_PHOTON,
    )
}

pub fn decide_null_from_infinity(
    kernel: &CausalKernel,
    query: KernelEvent,
    b2: Q,
) -> TerminatingDecision<NullFromInfinity> {
    match step_equatorial_null(kernel, query, b2).decision {
        Ok(EquatorialStep::Null(branch)) => one_step(Ok(branch), TIE_CAPTURE),
        Ok(EquatorialStep::HorizonCapture { .. } | EquatorialStep::Singular) => {
            one_step(Ok(NullFromInfinity::Capture), TIE_HORIZON)
        }
        Err(error) => one_step(Err(error), TIE_DOMAIN),
    }
}

fn static_unit() -> CausalKernel {
    CausalKernel::new(
        vec![tube(1, vec![genesis(origin(), q(1, 1))])],
        finite_root(),
    )
    .expect("static unit source")
}

fn event_at(time: Q, position: [Q; 2]) -> KernelEvent {
    KernelEvent { time, position }
}

fn capture_b2() -> Q {
    q(1, 2048) * q(1, 2048)
}

fn scatter_b2() -> Q {
    q(4, 1) * q(4, 1)
}

fn mass_change_static() -> CausalKernel {
    CausalKernel::new(
        vec![tube(
            1,
            vec![
                genesis(origin(), Q::zero()),
                SourceSegment {
                    since: Q::zero(),
                    position: origin(),
                    mu: q(1, 1),
                },
            ],
        )],
        finite_root(),
    )
    .expect("static mass change")
}

fn causal_null_two_sided() -> Result<(NullFromInfinity, NullFromInfinity), KernelError> {
    let changed = mass_change_static();
    let b2 = capture_b2();
    let pre = decide_null_from_infinity(&changed, event_at(q(1, 64), r4()), b2).decision?;
    let post = decide_null_from_infinity(&changed, event_at(q(1, 8), r4()), b2).decision?;
    Ok((pre, post))
}

fn null_spec(b2: Q, radial: RadialSense) -> GeodesicSpec {
    GeodesicSpec {
        kind: GeodesicKind::Null,
        invariant: b2,
        radial,
    }
}

fn timelike_spec(ang2: Q, radial: RadialSense) -> GeodesicSpec {
    GeodesicSpec {
        kind: GeodesicKind::Timelike,
        invariant: ang2,
        radial,
    }
}

fn isco_ang2() -> Q {
    q(12, 16_777_216)
}

fn causal_geodesic_two_sided() -> Result<(GeodesicOutcome, GeodesicOutcome), KernelError> {
    let changed = mass_change_static();
    let spec = null_spec(capture_b2(), RadialSense::Inward);
    let pre = step_equatorial_geodesic(
        &changed,
        event_at(q(1, 64), r4()),
        spec,
        MAX_PREDICATE_STEPS,
    )
    .decision?;
    let post =
        step_equatorial_geodesic(&changed, event_at(q(1, 8), r4()), spec, MAX_PREDICATE_STEPS)
            .decision?;
    Ok((pre, post))
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

pub fn qualify_schwarzschild() -> CandidateReport {
    let mut report = CandidateReport {
        id: SCHWARZSCHILD_LAW_ID.into(),
        version: 0,
        status: "FAIL".into(),
        metrics: Vec::new(),
        gates: Vec::new(),
        evidence: vec![
            "Research kernel es-schwarzschild-equatorial-v0 is isolated from es-inertial-causal-v1.".into(),
            "Planar restriction of 3D Schwarzschild: stationary one-source equatorial patch, not Kerr, not interacting GR, not 2D log gravity, not delayed Newton.".into(),
            "Photon sphere r_ph=3μ/c² and from-infinity null capture b²c⁴ ≶ 27μ² terminate in one rational comparison. Weak-field deflection oracle is 4μ/(c²b) on frozen b≥4.".into(),
            "Geodesic IVP is exact-or-fail-closed on the rational equatorial x-axis: circular identity (photon sphere / exact timelike circular), L=0 radial capture, and cubic-sign capture/scatter/unstable-photon classification. Exact elliptic deflection, scatter turning-radius *roots*, and generic scatter trajectories fail closed. An iteration cap is not a guessed root.".into(),
            "On/inside r_s the H0021 absorbing capture map remains the fallback. Moving and two-source geodesic queries refuse.".into(),
            "compact_field_certification and terminating_exact_branches stay failed. production_law stays null.".into(),
        ],
    };

    match schwarzschild_manifest() {
        Ok(()) => gate(
            &mut report,
            "schwarzschild_manifest_isolated",
            true,
            "New Schwarzschild fixtures did not edit frozen production-gate identities, old compact/exact fixtures, or numeric thresholds.",
        ),
        Err(error) => gate(&mut report, "schwarzschild_manifest_isolated", false, error),
    }

    let pre = mass_change_influence(origin(), r4(), q(1, 1), q(2, 1), q(1, 64));
    let post = mass_change_influence(origin(), r4(), q(1, 1), q(2, 1), q(1, 8));
    let field_ok = match (pre, post) {
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
            pre_influence <= 0.0 && post_influence > POST_LIGHTCONE_INFLUENCE_MIN
        }
        _ => false,
    };
    gate(
        &mut report,
        "source_change_light_cone",
        field_ok,
        "FIRST GATE. Parent retarded monopole: source μ 1→2 at t=0, query r=4. Pre-cone influence must stay zero; post-cone must be nonzero. Verlet/lapse still fail this gate.",
    );
    gate(
        &mut report,
        "causal_dynamic_sources",
        field_ok,
        "Same two-sided retarded-source field measurement as the parent kernel. Passing it is not production gravity.",
    );

    let kernel = static_unit();
    let r_ph = photon_sphere_radius(q(1, 1), C).expect("unit photon sphere");
    let rs = compact_radius(q(1, 1), C).expect("unit compact radius");
    let on_ph = decide_photon_sphere(&kernel, event_at(q(1, 1), [r_ph, Q::zero()]));
    let inside_ph = decide_photon_sphere(&kernel, event_at(q(1, 1), [rs, Q::zero()]));
    let outside_ph = decide_photon_sphere(&kernel, event_at(q(1, 1), r4()));
    let photon_ok = r_ph == q(3, 4096)
        && rs == q(1, 2048)
        && on_ph.decision == Ok(PhotonSphereClass::OnPhotonSphere)
        && inside_ph.decision == Ok(PhotonSphereClass::Inside)
        && outside_ph.decision == Ok(PhotonSphereClass::Outside)
        && on_ph.steps <= MAX_PREDICATE_STEPS;
    gate(
        &mut report,
        "exact_photon_sphere",
        photon_ok,
        "Exact rational photon sphere: r_ph=3μ/c²=3/4096. r_s=1/2048 Inside; r_ph OnPhotonSphere; r=4 Outside. Compared as r²c⁴ ≶ 9μ².",
    );

    let capture = null_from_infinity(capture_b2(), q(1, 1), C);
    let scatter = null_from_infinity(scatter_b2(), q(1, 1), C);
    let critical = null_from_infinity(critical_b2(q(1, 1), C), q(1, 1), C);
    let capture_ok = capture == NullFromInfinity::Capture
        && scatter == NullFromInfinity::Scatter
        && critical == NullFromInfinity::UnstablePhotonSphere
        && capture_b2() * c4(C) == q(4, 1)
        && critical_b2(q(1, 1), C) == q(CRITICAL_B2[0], CRITICAL_B2[1]);
    gate(
        &mut report,
        "null_capture_cross_section",
        capture_ok,
        "From-infinity null capture: b=1/2048 (b²c⁴=4<27) Capture; b²=27μ²/c⁴ UnstablePhotonSphere; b=4 Scatter. One comparison, no √3, no loop.",
    );

    let potential_ok = null_potential_greater(r_ph, rs + rs, rs)
        && null_potential_greater(r_ph, Q::from_integer(3) * rs, rs)
        && r_ph > rs;
    gate(
        &mut report,
        "effective_potential_max_at_photon_sphere",
        potential_ok,
        "Equatorial null V=(r-r_s)/r³ is greater at r_ph than at 2 r_s and 3 r_s (cross-multiply, no square root). Diagnostic maximum, not a geodesic IVP.",
    );

    let deflection = weak_field_light_deflection(q(1, 1), C, q(4, 1));
    let compact_b = weak_field_light_deflection(q(1, 1), C, q(1, 2048));
    let deflection_ok = deflection == Ok(q(WEAK_FIELD_DEFLECTION[0], WEAK_FIELD_DEFLECTION[1]))
        && matches!(compact_b, Err(KernelError::UnsupportedPredicate(_)));
    if let Ok(delta) = deflection {
        push_metric(
            &mut report,
            "weak_field_deflection_is_4mu",
            "gr_weak_field",
            qf(delta),
            "radian",
            qf(q(WEAK_FIELD_DEFLECTION[0], WEAK_FIELD_DEFLECTION[1])),
            true,
        );
    }
    gate(
        &mut report,
        "weak_field_deflection_is_4mu",
        deflection_ok,
        "Weak-field oracle at frozen b=4 is exactly 4μ/(c²b)=1/4096. b=1/2048 (inside the frozen weak-field floor) refuses; exact elliptic deflection is unsupported.",
    );

    let newton_delta = newton_hyperbolic_deflection(1.0, C as f64, 4.0);
    let gr_delta = gr_weak_light_deflection_f64(1.0, C as f64, 4.0);
    let deflection_gap = (newton_delta - gr_delta).abs();
    let newton_hole = newton_delta.is_finite()
        && gr_delta.is_finite()
        && deflection_gap > 0.0
        && newton_delta < gr_delta;
    push_metric(
        &mut report,
        "newton_flyby_not_4mu",
        "newton_minus_gr",
        deflection_gap,
        "radian",
        0.0,
        false,
    );
    gate(
        &mut report,
        "newton_flyby_not_4mu",
        newton_hole,
        format!(
            "NEGATIVE CONTROL. Unbound Newton flyby at b=4, v=c turns by {newton_delta:.12e} rad; GR weak-field 4μ/(c²b) is {gr_delta:.12e}. Newton flyby ≠ 4μ/(c²b)."
        ),
    );

    let causal_ok = match causal_null_two_sided() {
        Ok((pre_branch, post_branch)) => {
            pre_branch == NullFromInfinity::Scatter && post_branch == NullFromInfinity::Capture
        }
        Err(_) => false,
    };
    gate(
        &mut report,
        "causal_schwarzschild_after_cone",
        causal_ok,
        "μ 0→1 at t=0, capture b=1/2048, query r=4. Pre-cone t=1/64 is Scatter (genesis μ=0). Post-cone t=1/8 is Capture. The stationary patch is retarded.",
    );

    let interior = event_at(q(1, 1), [q(1, 4096), Q::zero()]);
    let horizon = event_at(q(1, 1), [rs, Q::zero()]);
    let coincidence = event_at(q(1, 1), origin());
    let interior_step = step_equatorial_null(&kernel, interior, scatter_b2());
    let horizon_step = step_equatorial_null(&kernel, horizon, scatter_b2());
    let singular_step = step_equatorial_null(&kernel, coincidence, scatter_b2());
    let fallback_ok = interior_step.decision
        == Ok(EquatorialStep::HorizonCapture {
            class: CompactClass::Interior,
        })
        && horizon_step.decision
            == Ok(EquatorialStep::HorizonCapture {
                class: CompactClass::OnHorizon,
            })
        && singular_step.decision == Ok(EquatorialStep::Singular);
    gate(
        &mut report,
        "horizon_absorbing_fallback",
        fallback_ok,
        "H0021 fallback: even a scatter impact b=4 is HorizonCapture at r=1/4096 and r_s, and Singular at r=0. Absorbing capture remains when the geodesic domain does not apply.",
    );

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
    .expect("subluminal move");
    let moving_step = step_equatorial_null(&moving, event_at(q(1, 8), r4()), scatter_b2());
    let moving_ok = matches!(
        moving_step.decision,
        Err(KernelError::UnsupportedPredicate(_))
    );
    gate(
        &mut report,
        "moving_source_geodesic_fails_closed",
        moving_ok,
        "A moving source is outside the stationary-patch domain. The geodesic stepper refuses rather than guessing a dynamical GR map.",
    );

    let two = CausalKernel::new(
        vec![
            tube(1, vec![genesis(origin(), q(1, 1))]),
            tube(2, vec![genesis([q(8, 1), Q::zero()], q(1, 1))]),
        ],
        finite_root(),
    )
    .expect("two static sources");
    let two_step = step_equatorial_null(&two, event_at(q(1, 1), r4()), scatter_b2());
    let two_ok = matches!(two_step.decision, Err(KernelError::UnsupportedPredicate(_)));
    gate(
        &mut report,
        "two_source_geodesic_fails_closed",
        two_ok,
        "Two sources are interacting compact-body GR, which this patch does not claim. The geodesic stepper fails closed.",
    );

    let turning = decide_turning_radius(scatter_b2(), q(1, 1), C, MAX_PREDICATE_STEPS);
    let turning_ok = matches!(turning.decision, Err(KernelError::UnsupportedPredicate(_)))
        && turning.steps <= MAX_PREDICATE_STEPS;
    gate(
        &mut report,
        "turning_root_fails_closed",
        turning_ok,
        "Scatter turning radius solves r³-b²r+b² r_s=0. There is no laboratory rational root; the stepper fails closed rather than iterating for a sign.",
    );

    let cap_zero = decide_turning_radius(scatter_b2(), q(1, 1), C, 0);
    let cap_guess = turning_radius_iteration_cap(true, q(1, 1), STATIONARY_CROSSING_CAP);
    let cap_ok = cap_zero.decision == Err(KernelError::BranchBudgetExhausted { max_steps: 0 })
        && cap_guess
            == Err(KernelError::BranchBudgetExhausted {
                max_steps: STATIONARY_CROSSING_CAP,
            });
    gate(
        &mut report,
        "iteration_cap_not_turning_sign",
        cap_ok,
        "Iteration cap is a failed execution. A guessed turning radius after budget exhaustion is illegal. Stationary lapse cap stays 64.",
    );

    let r_isco = isco_radius(q(1, 1), C).expect("unit ISCO");
    let capture_ivp = step_equatorial_geodesic(
        &kernel,
        event_at(q(1, 1), r4()),
        null_spec(capture_b2(), RadialSense::Inward),
        MAX_PREDICATE_STEPS,
    );
    let scatter_ivp = step_equatorial_geodesic(
        &kernel,
        event_at(q(1, 1), r4()),
        null_spec(scatter_b2(), RadialSense::Inward),
        MAX_PREDICATE_STEPS,
    );
    let photon_ivp = step_equatorial_geodesic(
        &kernel,
        event_at(q(1, 1), [r_ph, Q::zero()]),
        null_spec(critical_b2(q(1, 1), C), RadialSense::Rest),
        MAX_PREDICATE_STEPS,
    );
    let escape_ivp = step_equatorial_geodesic(
        &kernel,
        event_at(q(1, 1), r4()),
        null_spec(capture_b2(), RadialSense::Outward),
        MAX_PREDICATE_STEPS,
    );
    let ivp_class_ok = capture_ivp.decision == Ok(GeodesicOutcome::Capture)
        && scatter_ivp.decision == Ok(GeodesicOutcome::Scatter)
        && escape_ivp.decision == Ok(GeodesicOutcome::Scatter)
        && photon_ivp.decision
            == Ok(GeodesicOutcome::CircularIdentity {
                kind: GeodesicKind::Null,
                radius: r_ph,
            })
        && capture_ivp.steps <= MAX_PREDICATE_STEPS;
    gate(
        &mut report,
        "null_geodesic_ivp_capture_scatter_photon",
        ivp_class_ok,
        "Null geodesic IVP at finite r: capture b inward at r=4 is Capture; the same b outward is Scatter; scatter b inward at r=4 is Scatter; critical b at rest on r_ph is CircularIdentity. Cubic sign plus r ≶ r_ph, not a turning-root solver.",
    );

    let photon_step_ok = photon_ivp.decision
        == Ok(GeodesicOutcome::CircularIdentity {
            kind: GeodesicKind::Null,
            radius: r_ph,
        });
    gate(
        &mut report,
        "circular_null_identity_step",
        photon_step_ok,
        "Exact symplectic identity on the unstable photon orbit: r stays r_ph=3μ/c², p_r stays 0. One step, no iteration.",
    );

    let isco_ivp = step_equatorial_geodesic(
        &kernel,
        event_at(q(1, 1), [r_isco, Q::zero()]),
        timelike_spec(isco_ang2(), RadialSense::Rest),
        MAX_PREDICATE_STEPS,
    );
    let isco_ok = r_isco == q(ISCO_RADIUS[0], ISCO_RADIUS[1])
        && is_exact_timelike_circular(r_isco, isco_ang2(), q(1, 1), C)
        && isco_ivp.decision
            == Ok(GeodesicOutcome::CircularIdentity {
                kind: GeodesicKind::Timelike,
                radius: r_isco,
            });
    gate(
        &mut report,
        "circular_timelike_isco_identity_step",
        isco_ok,
        "Exact timelike circular identity L²(r-3M)=M r² at r_isco=6μ/c²=3/2048. (r, p_r) stay put. Not an orbit-tuned production map.",
    );

    let radial_ivp = step_equatorial_geodesic(
        &kernel,
        event_at(q(1, 1), r4()),
        timelike_spec(Q::zero(), RadialSense::Rest),
        MAX_PREDICATE_STEPS,
    );
    let radial_ok = radial_ivp.decision == Ok(GeodesicOutcome::Capture);
    gate(
        &mut report,
        "radial_timelike_rest_is_capture",
        radial_ok,
        "Frozen radial domain: timelike L=0 from rest at r=4 is Capture. Finite proper-time plunge; no turning cubic and no guessed time-of-flight.",
    );

    let scatter_int = integrate_equatorial_scatter(
        &kernel,
        event_at(q(1, 1), r4()),
        null_spec(scatter_b2(), RadialSense::Inward),
        MAX_PREDICATE_STEPS,
    );
    let scatter_int_cap = integrate_equatorial_scatter(
        &kernel,
        event_at(q(1, 1), r4()),
        null_spec(scatter_b2(), RadialSense::Inward),
        0,
    );
    let scatter_traj_ok = matches!(
        scatter_int.decision,
        Err(KernelError::UnsupportedPredicate(_))
    ) && scatter_int_cap.decision
        == Err(KernelError::BranchBudgetExhausted { max_steps: 0 });
    gate(
        &mut report,
        "generic_scatter_trajectory_fails_closed",
        scatter_traj_ok,
        "Generic scatter trajectory / elliptic deflection is unsupported. Classification may return Scatter; integrating it fails closed. Budget 0 is BranchBudgetExhausted, not a guessed deflection.",
    );

    let causal_ivp_ok = match causal_geodesic_two_sided() {
        Ok((pre_branch, post_branch)) => {
            pre_branch == GeodesicOutcome::Scatter && post_branch == GeodesicOutcome::Capture
        }
        Err(_) => false,
    };
    gate(
        &mut report,
        "causal_geodesic_ivp_after_cone",
        causal_ivp_ok,
        "Geodesic IVP is retarded. μ 0→1 at t=0, capture b inward, query r=4. Pre-cone t=1/64 is Scatter (genesis μ=0). Post-cone t=1/8 is Capture.",
    );

    let off_axis = step_equatorial_geodesic(
        &kernel,
        event_at(q(1, 1), [q(4, 1), q(1, 1)]),
        null_spec(scatter_b2(), RadialSense::Inward),
        MAX_PREDICATE_STEPS,
    );
    let off_axis_ok = matches!(off_axis.decision, Err(KernelError::UnsupportedPredicate(_)));
    gate(
        &mut report,
        "irrational_radius_fails_closed",
        off_axis_ok,
        "Off-axis query (y≠0) is not a laboratory square root. The geodesic IVP fails closed rather than extracting r.",
    );

    record_well_posed_exterior(&mut report);

    let certified = photon_ok
        && capture_ok
        && potential_ok
        && deflection_ok
        && newton_hole
        && causal_ok
        && fallback_ok
        && moving_ok
        && two_ok
        && turning_ok
        && cap_ok
        && ivp_class_ok
        && photon_step_ok
        && isco_ok
        && radial_ok
        && scatter_traj_ok
        && causal_ivp_ok
        && off_axis_ok;
    gate(
        &mut report,
        "compact_field_certification",
        false,
        format!(
            "Schwarzschild equatorial oracles plus a restricted geodesic IVP are implemented (fixtures passed={certified}): photon sphere, from-infinity capture b²c⁴ ≶ 27μ², weak-field 4μ/(c²b), circular identity, L=0 radial capture, cubic-sign capture/scatter. This is a stationary one-source patch, not interacting GR, not Kerr, not elliptic deflection. Newton flyby {newton_delta:.12e} ≠ GR {gr_delta:.12e}. compact_field_certification stays failed."
        ),
    );
    gate(
        &mut report,
        "terminating_exact_branches",
        false,
        format!(
            "From-infinity null Capture/PhotonSphere/Scatter, photon-sphere class, circular identity, and cubic-sign IVP classification terminate in one comparison (max_steps={MAX_PREDICATE_STEPS}). Horizon uses H0021. Turning-point *root*, elliptic deflection, and generic scatter/timelike bound trajectories fail closed. Field values remain f64. Stationary maps still use floating roots and a {STATIONARY_CROSSING_CAP}-crossing cap. Production terminating_exact_branches stays failed."
        ),
    );

    fail_missing(
        &mut report,
        "orbit_stability",
        "No orbit map and no Kepler tuning. A photon-sphere oracle is not an orbit integrator.",
    );
    fail_missing(
        &mut report,
        "angular_isotropy",
        "No rotation suite. Frozen quantum/rotation ladder remains on the rejected stationary experiments.",
    );
    fail_missing(
        &mut report,
        "quantum_refinement",
        "This patch is not a quantized finite map. Existing quanta 2^-22,2^-23,2^-24 stay frozen on the stationary suite and were not retuned.",
    );
    fail_missing(
        &mut report,
        "stationary_clock",
        "A null-from-infinity oracle does not define dτ/dt. Matching Schwarzschild lapse is not claimed as a production clock.",
    );
    fail_missing(
        &mut report,
        "source_tree_bound",
        "No monopole quadtree/FMM. Direct retarded evaluation remains the small-system reference only.",
    );
    fail_missing(
        &mut report,
        "source_backreaction",
        "Stationary one-source patch. Frozen source_backreaction is instantaneous Newton fleet/force-balance, not retarded coupling and not GR.",
    );
    fail_missing(
        &mut report,
        "retarded_two_way_backreaction",
        "This candidate is a stationary Schwarzschild patch, not the coupled two-way stepper. See es-causal-retarded-coupled-v0.",
    );

    let mut notes = String::from("schwarzschild equatorial oracles ");
    let _ = write!(
        notes,
        "{}; compact_field_certification and terminating_exact_branches kept failed.",
        if certified { "passed" } else { "failed" }
    );
    report.evidence.push(notes);
    report.evidence.push(format!(
        "law={} parent={} c={}",
        SCHWARZSCHILD_LAW_ID, RESEARCH_LAW_ID, C
    ));
    report
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn schwarzschild_law_is_isolated() {
        assert_ne!(SCHWARZSCHILD_LAW_ID, RESEARCH_LAW_ID);
        assert_ne!(SCHWARZSCHILD_LAW_ID, COUPLED_LAW_ID);
        assert_ne!(SCHWARZSCHILD_LAW_ID, INERTIAL_LAB_LAW_ID);
        schwarzschild_manifest().unwrap();
    }

    #[test]
    fn photon_sphere_is_exact_three_mu_over_c2() {
        assert_eq!(photon_sphere_radius(q(1, 1), C).unwrap(), q(3, 4096));
        assert_eq!(
            photon_sphere_class([q(3, 4096), Q::zero()], q(1, 1), C),
            PhotonSphereClass::OnPhotonSphere
        );
        assert_eq!(
            photon_sphere_class([q(1, 2048), Q::zero()], q(1, 1), C),
            PhotonSphereClass::Inside
        );
        assert_eq!(
            photon_sphere_class(r4(), q(1, 1), C),
            PhotonSphereClass::Outside
        );
    }

    #[test]
    fn null_capture_is_exact_without_sqrt3() {
        assert_eq!(
            null_from_infinity(capture_b2(), q(1, 1), C),
            NullFromInfinity::Capture
        );
        assert_eq!(
            null_from_infinity(critical_b2(q(1, 1), C), q(1, 1), C),
            NullFromInfinity::UnstablePhotonSphere
        );
        assert_eq!(
            null_from_infinity(scatter_b2(), q(1, 1), C),
            NullFromInfinity::Scatter
        );
        assert_eq!(
            null_from_infinity(capture_b2(), Q::zero(), C),
            NullFromInfinity::Scatter
        );
    }

    #[test]
    fn weak_field_deflection_is_exactly_4mu_and_newton_is_not() {
        assert_eq!(
            weak_field_light_deflection(q(1, 1), C, q(4, 1)).unwrap(),
            q(1, 4096)
        );
        assert!(matches!(
            weak_field_light_deflection(q(1, 1), C, q(1, 2048)),
            Err(KernelError::UnsupportedPredicate(_))
        ));
        let newton = newton_hyperbolic_deflection(1.0, 64.0, 4.0);
        let gr = gr_weak_light_deflection_f64(1.0, 64.0, 4.0);
        assert!((gr - 1.0 / 4096.0).abs() < 1e-18);
        assert!(newton < gr);
        assert!((newton * 2.0 - gr).abs() / gr < 1e-8);
    }

    #[test]
    fn schwarzschild_of_a_mass_change_is_retarded() {
        let (pre, post) = causal_null_two_sided().unwrap();
        assert_eq!(pre, NullFromInfinity::Scatter);
        assert_eq!(post, NullFromInfinity::Capture);
    }

    #[test]
    fn horizon_fallback_beats_scatter_impact() {
        let kernel = static_unit();
        let rs = compact_radius(q(1, 1), C).unwrap();
        assert_eq!(
            step_equatorial_null(
                &kernel,
                event_at(q(1, 1), [q(1, 4096), Q::zero()]),
                scatter_b2()
            )
            .decision,
            Ok(EquatorialStep::HorizonCapture {
                class: CompactClass::Interior
            })
        );
        assert_eq!(
            step_equatorial_null(&kernel, event_at(q(1, 1), [rs, Q::zero()]), scatter_b2())
                .decision,
            Ok(EquatorialStep::HorizonCapture {
                class: CompactClass::OnHorizon
            })
        );
        assert_eq!(
            step_equatorial_null(&kernel, event_at(q(1, 1), origin()), scatter_b2()).decision,
            Ok(EquatorialStep::Singular)
        );
        assert_eq!(
            step_equatorial_null(&kernel, event_at(q(1, 1), r4()), scatter_b2()).decision,
            Ok(EquatorialStep::Null(NullFromInfinity::Scatter))
        );
    }

    #[test]
    fn domain_misses_fail_closed() {
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
        assert!(matches!(
            step_equatorial_null(&moving, event_at(q(1, 8), r4()), scatter_b2()).decision,
            Err(KernelError::UnsupportedPredicate(_))
        ));
        let two = CausalKernel::new(
            vec![
                tube(1, vec![genesis(origin(), q(1, 1))]),
                tube(2, vec![genesis([q(8, 1), Q::zero()], q(1, 1))]),
            ],
            finite_root(),
        )
        .unwrap();
        assert!(matches!(
            step_equatorial_null(&two, event_at(q(1, 1), r4()), scatter_b2()).decision,
            Err(KernelError::UnsupportedPredicate(_))
        ));
    }

    #[test]
    fn turning_root_is_fail_closed_and_cap_is_not_a_sign() {
        let hit = decide_turning_radius(scatter_b2(), q(1, 1), C, MAX_PREDICATE_STEPS);
        assert!(matches!(
            hit.decision,
            Err(KernelError::UnsupportedPredicate(_))
        ));
        assert_eq!(
            decide_turning_radius(scatter_b2(), q(1, 1), C, 0).decision,
            Err(KernelError::BranchBudgetExhausted { max_steps: 0 })
        );
        assert!(turning_radius_iteration_cap(true, q(4, 1), 64).is_err());
    }

    #[test]
    fn null_geodesic_ivp_distinguishes_capture_scatter_and_photon() {
        let kernel = static_unit();
        let r_ph = photon_sphere_radius(q(1, 1), C).unwrap();
        assert_eq!(
            step_equatorial_geodesic(
                &kernel,
                event_at(q(1, 1), r4()),
                null_spec(capture_b2(), RadialSense::Inward),
                MAX_PREDICATE_STEPS
            )
            .decision,
            Ok(GeodesicOutcome::Capture)
        );
        assert_eq!(
            step_equatorial_geodesic(
                &kernel,
                event_at(q(1, 1), r4()),
                null_spec(capture_b2(), RadialSense::Outward),
                MAX_PREDICATE_STEPS
            )
            .decision,
            Ok(GeodesicOutcome::Scatter)
        );
        assert_eq!(
            step_equatorial_geodesic(
                &kernel,
                event_at(q(1, 1), r4()),
                null_spec(scatter_b2(), RadialSense::Inward),
                MAX_PREDICATE_STEPS
            )
            .decision,
            Ok(GeodesicOutcome::Scatter)
        );
        assert_eq!(
            step_equatorial_geodesic(
                &kernel,
                event_at(q(1, 1), [r_ph, Q::zero()]),
                null_spec(critical_b2(q(1, 1), C), RadialSense::Rest),
                MAX_PREDICATE_STEPS
            )
            .decision,
            Ok(GeodesicOutcome::CircularIdentity {
                kind: GeodesicKind::Null,
                radius: r_ph
            })
        );
        assert_eq!(
            step_equatorial_geodesic(
                &kernel,
                event_at(q(1, 1), r4()),
                null_spec(critical_b2(q(1, 1), C), RadialSense::Inward),
                MAX_PREDICATE_STEPS
            )
            .decision,
            Ok(GeodesicOutcome::UnstablePhotonOrbit)
        );
    }

    #[test]
    fn circular_and_radial_domains_are_exact() {
        let kernel = static_unit();
        let r_isco = isco_radius(q(1, 1), C).unwrap();
        assert_eq!(r_isco, q(3, 2048));
        assert!(is_exact_timelike_circular(r_isco, isco_ang2(), q(1, 1), C));
        assert_eq!(
            step_equatorial_geodesic(
                &kernel,
                event_at(q(1, 1), [r_isco, Q::zero()]),
                timelike_spec(isco_ang2(), RadialSense::Rest),
                MAX_PREDICATE_STEPS
            )
            .decision,
            Ok(GeodesicOutcome::CircularIdentity {
                kind: GeodesicKind::Timelike,
                radius: r_isco
            })
        );
        assert_eq!(
            step_equatorial_geodesic(
                &kernel,
                event_at(q(1, 1), r4()),
                timelike_spec(Q::zero(), RadialSense::Rest),
                MAX_PREDICATE_STEPS
            )
            .decision,
            Ok(GeodesicOutcome::Capture)
        );
        assert!(matches!(
            step_equatorial_geodesic(
                &kernel,
                event_at(q(1, 1), r4()),
                timelike_spec(q(1, 1), RadialSense::Inward),
                MAX_PREDICATE_STEPS
            )
            .decision,
            Err(KernelError::UnsupportedPredicate(_))
        ));
    }

    #[test]
    fn scatter_trajectory_and_off_axis_fail_closed() {
        let kernel = static_unit();
        assert!(matches!(
            integrate_equatorial_scatter(
                &kernel,
                event_at(q(1, 1), r4()),
                null_spec(scatter_b2(), RadialSense::Inward),
                MAX_PREDICATE_STEPS
            )
            .decision,
            Err(KernelError::UnsupportedPredicate(_))
        ));
        assert_eq!(
            integrate_equatorial_scatter(
                &kernel,
                event_at(q(1, 1), r4()),
                null_spec(scatter_b2(), RadialSense::Inward),
                0
            )
            .decision,
            Err(KernelError::BranchBudgetExhausted { max_steps: 0 })
        );
        assert!(matches!(
            step_equatorial_geodesic(
                &kernel,
                event_at(q(1, 1), [q(4, 1), q(1, 1)]),
                null_spec(scatter_b2(), RadialSense::Inward),
                MAX_PREDICATE_STEPS
            )
            .decision,
            Err(KernelError::UnsupportedPredicate(_))
        ));
        assert_eq!(
            step_equatorial_geodesic(
                &kernel,
                event_at(q(1, 1), r4()),
                null_spec(scatter_b2(), RadialSense::Inward),
                0
            )
            .decision,
            Err(KernelError::BranchBudgetExhausted { max_steps: 0 })
        );
    }

    #[test]
    fn geodesic_ivp_of_a_mass_change_is_retarded() {
        let (pre, post) = causal_geodesic_two_sided().unwrap();
        assert_eq!(pre, GeodesicOutcome::Scatter);
        assert_eq!(post, GeodesicOutcome::Capture);
    }

    #[test]
    fn schwarzschild_does_not_promote() {
        let report = qualify_schwarzschild();
        assert_eq!(report.id, SCHWARZSCHILD_LAW_ID);
        assert_eq!(report.status, "FAIL");
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
        for id in SCHWARZSCHILD_FIXTURE_IDS {
            assert!(
                report.gates.iter().find(|g| g.id == id).unwrap().passed,
                "{id} must pass as a Schwarzschild capability or negative control"
            );
        }
        for id in [
            "orbit_stability",
            "compact_field_certification",
            "terminating_exact_branches",
            "source_backreaction",
            "retarded_two_way_backreaction",
            "stationary_clock",
            "source_tree_bound",
        ] {
            assert!(
                !report.gates.iter().find(|g| g.id == id).unwrap().passed,
                "{id} must remain failed"
            );
        }
    }
}
