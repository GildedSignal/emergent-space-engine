//! Isolated terminating exact-branch research: every *supported* kernel
//! predicate has a finite authoritative decision. This is not a curved-null
//! geodesic solver and does not promote `terminating_exact_branches`.
//!
//! One comparison decides cone, compact class, capture, and certified-exterior
//! completeness. Equality invokes an explicit tie rule. Ambiguous `f64`
//! escalates to an exact dyadic or fails closed. Exceeding the documented
//! step budget is a failed execution, never a guessed sign. NaN is refuse.

use super::causal_kernel::{
    compact_class, compact_map, compact_radius, cone_relation, finite_root, genesis, origin, q, qf,
    r4, tube, BranchDecision, CausalKernel, CertifiedAcceleration, CompactClass, CompactMap,
    ExteriorModel, KernelError, KernelEvent, OmittedTailBound, SourceSegment, C, Q,
    RESEARCH_LAW_ID,
};
use super::coupled::COUPLED_LAW_ID;
use super::{circle_crossing, gate, CandidateReport, LAPSE_CROSSING_BUDGET_ERROR};
use num_rational::Ratio;
use num_traits::Zero;
use serde::Deserialize;

const MANIFEST: &str = include_str!("../../../scenarios/law-gates.json");

/// One sign comparison. Conversion of a finite `f64` is not an extra branch.
pub const MAX_PREDICATE_STEPS: u32 = 1;
/// Frozen stationary-lapse crossing budget. Exhaustion is execution failure.
pub const STATIONARY_CROSSING_CAP: u32 = 64;

const TIE_CONE: &str = "on-cone equality is visible (closed cone)";
const TIE_HORIZON: &str = "r²c⁴ = 4μ² is OnHorizon, which is capture";
const TIE_COINCIDENCE: &str = "r=0 refuses Singular; never NaN";
const TIE_EXTERIOR: &str = "incomplete or omitted-region queries refuse";
const TIE_CAP: &str = "exhausted budget is failed execution, not a guessed sign";
const TIE_UNSUPPORTED: &str = "unsupported predicates refuse; they do not guess a geodesic branch";

#[derive(Clone, Deserialize)]
struct ExactFileSlice {
    terminating_exact_branches_research: ExactResearchManifest,
    stationary_metric: CrossingCap,
}

#[derive(Clone, Deserialize)]
struct ExactResearchManifest {
    gate: String,
    parent_kernel: String,
    coupled_kernel: String,
    light_speed: i128,
    max_predicate_steps: u32,
    stationary_crossing_cap: u32,
    fixtures: Vec<NamedFixture>,
}

#[derive(Clone, Deserialize)]
struct CrossingCap {
    maximum_crossings_per_step: u32,
}

#[derive(Clone, Deserialize)]
struct NamedFixture {
    id: String,
}

pub(crate) const EXACT_BRANCH_FIXTURE_IDS: [&str; 9] = [
    "exact_cone_before_on_after",
    "on_cone_tie_is_visible",
    "on_horizon_tie_is_capture",
    "coincidence_tie_refuses_not_nan",
    "certified_exterior_refuses_incomplete",
    "f64_escalates_or_fails_closed",
    "iteration_cap_is_failed_execution",
    "floating_root_is_not_certificate",
    "curved_null_geodesic_unsupported",
];

/// Finite decision: a value or a closed failure, plus the step count.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct TerminatingDecision<T> {
    pub decision: Result<T, KernelError>,
    pub steps: u32,
    pub max_steps: u32,
    pub tie_rule: &'static str,
}

impl<T> TerminatingDecision<T> {
    fn one_step(decision: Result<T, KernelError>, tie_rule: &'static str) -> Self {
        Self {
            decision,
            steps: MAX_PREDICATE_STEPS,
            max_steps: MAX_PREDICATE_STEPS,
            tie_rule,
        }
    }

    fn exhausted(max_steps: u32) -> Self {
        Self {
            decision: Err(KernelError::BranchBudgetExhausted { max_steps }),
            steps: max_steps,
            max_steps,
            tie_rule: TIE_CAP,
        }
    }
}

pub fn exact_branch_manifest() -> Result<(), String> {
    let slice: ExactFileSlice = serde_json::from_str(MANIFEST).map_err(|e| e.to_string())?;
    if slice.terminating_exact_branches_research.gate != "terminating_exact_branches" {
        return Err("exact-branch gate must remain terminating_exact_branches".into());
    }
    if slice.terminating_exact_branches_research.parent_kernel != RESEARCH_LAW_ID {
        return Err("exact-branch parent must remain the retarded monopole kernel".into());
    }
    if slice.terminating_exact_branches_research.coupled_kernel != COUPLED_LAW_ID {
        return Err("exact-branch coupled kernel id drifted".into());
    }
    if slice.terminating_exact_branches_research.light_speed != C
        || slice
            .terminating_exact_branches_research
            .max_predicate_steps
            != MAX_PREDICATE_STEPS
        || slice
            .terminating_exact_branches_research
            .stationary_crossing_cap
            != STATIONARY_CROSSING_CAP
        || slice.stationary_metric.maximum_crossings_per_step != STATIONARY_CROSSING_CAP
    {
        return Err("exact-branch research thresholds were weakened or retuned".into());
    }
    let ids: Vec<&str> = slice
        .terminating_exact_branches_research
        .fixtures
        .iter()
        .map(|f| f.id.as_str())
        .collect();
    if ids != EXACT_BRANCH_FIXTURE_IDS {
        return Err("exact-branch fixtures were renamed, dropped or reordered".into());
    }
    Ok(())
}

/// Exact IEEE-754 → laboratory `Ratio<i128>`. Never continued fractions.
/// Overflow or nonfinite input fails closed; there is no precision loop.
pub fn q_from_f64(x: f64) -> Result<Q, KernelError> {
    if !x.is_finite() {
        return Err(KernelError::NonfiniteBranch);
    }
    if x == 0.0 {
        return Ok(Q::zero());
    }
    let bits = x.to_bits();
    let negative = bits >> 63 != 0;
    let exp_bits = ((bits >> 52) & 0x7ff) as i32;
    let frac = bits & ((1u64 << 52) - 1);
    let (mut mantissa, mut exp) = if exp_bits == 0 {
        (frac as i128, -1022i32 - 52)
    } else {
        ((frac as i128) | (1i128 << 52), exp_bits - 1023 - 52)
    };
    if negative {
        mantissa = -mantissa;
    }
    while mantissa != 0 && mantissa % 2 == 0 {
        mantissa /= 2;
        exp += 1;
    }
    if exp >= 0 {
        let shift = exp as u32;
        if shift >= 75 {
            return Err(KernelError::ExactConversionOverflow);
        }
        let numer = mantissa
            .checked_shl(shift)
            .ok_or(KernelError::ExactConversionOverflow)?;
        Ok(Q::from_integer(numer))
    } else {
        let shift = (-exp) as u32;
        if shift >= 127 {
            return Err(KernelError::ExactConversionOverflow);
        }
        let denom = 1i128
            .checked_shl(shift)
            .ok_or(KernelError::ExactConversionOverflow)?;
        Ok(Ratio::new(mantissa, denom))
    }
}

fn pair_from_f64(value: [f64; 2]) -> Result<[Q; 2], KernelError> {
    Ok([q_from_f64(value[0])?, q_from_f64(value[1])?])
}

/// Cone membership. Future events refuse. Tie: On (visible / simultaneous).
pub fn decide_cone(
    source: KernelEvent,
    query: KernelEvent,
    c: i128,
) -> TerminatingDecision<BranchDecision> {
    match cone_relation(source, query, c) {
        Some(branch) => TerminatingDecision::one_step(Ok(branch), TIE_CONE),
        None => TerminatingDecision::one_step(
            Err(KernelError::Invalid(
                "query is in the causal future of the source; cone membership refuses",
            )),
            "future events refuse",
        ),
    }
}

/// Compact class `r²c⁴ ≶ 4μ²`. Tie: OnHorizon.
pub fn decide_compact_class(
    displacement: [Q; 2],
    mu: Q,
    c: i128,
) -> TerminatingDecision<CompactClass> {
    TerminatingDecision::one_step(Ok(compact_class(displacement, mu, c)), TIE_HORIZON)
}

/// Capture map. Tie: OnHorizon captures. Coincidence refuses Singular.
pub fn decide_capture(
    seg: SourceSegment,
    query: KernelEvent,
    c: i128,
) -> TerminatingDecision<CompactMap> {
    TerminatingDecision::one_step(Ok(compact_map(seg, query, c)), TIE_COINCIDENCE)
}

/// Certified exterior: listed field plus enclosure, or fail closed.
pub fn decide_certified_exterior(
    kernel: &CausalKernel,
    query: KernelEvent,
) -> TerminatingDecision<CertifiedAcceleration> {
    TerminatingDecision::one_step(kernel.certified_acceleration_at(query), TIE_EXTERIOR)
}

/// Escalate finite `f64` to the exact compact-class predicate, or refuse.
pub fn decide_compact_class_f64(
    displacement: [f64; 2],
    mu: f64,
    c: i128,
) -> TerminatingDecision<CompactClass> {
    match (pair_from_f64(displacement), q_from_f64(mu)) {
        (Ok(disp), Ok(mu_q)) => decide_compact_class(disp, mu_q, c),
        (Err(error), _) | (_, Err(error)) => TerminatingDecision::one_step(Err(error), TIE_HORIZON),
    }
}

/// Escalate finite `f64` events to the exact cone predicate, or refuse.
pub fn decide_cone_f64(
    source_time: f64,
    source_position: [f64; 2],
    query_time: f64,
    query_position: [f64; 2],
    c: i128,
) -> TerminatingDecision<BranchDecision> {
    let source = match (q_from_f64(source_time), pair_from_f64(source_position)) {
        (Ok(time), Ok(position)) => KernelEvent { time, position },
        (Err(error), _) | (_, Err(error)) => {
            return TerminatingDecision::one_step(Err(error), TIE_CONE);
        }
    };
    let query = match (q_from_f64(query_time), pair_from_f64(query_position)) {
        (Ok(time), Ok(position)) => KernelEvent { time, position },
        (Err(error), _) | (_, Err(error)) => {
            return TerminatingDecision::one_step(Err(error), TIE_CONE);
        }
    };
    decide_cone(source, query, c)
}

/// A budget of zero comparisons cannot guess a sign. "Keep increasing
/// precision" that hits the cap is a failed execution.
pub fn decide_with_iteration_budget(
    lhs: f64,
    rhs: f64,
    max_steps: u32,
) -> TerminatingDecision<CompactClass> {
    if max_steps < MAX_PREDICATE_STEPS {
        return TerminatingDecision::exhausted(max_steps);
    }
    match (q_from_f64(lhs), q_from_f64(rhs)) {
        (Ok(left), Ok(right)) => {
            let class = if left > right {
                CompactClass::Exterior
            } else if left == right {
                CompactClass::OnHorizon
            } else {
                CompactClass::Interior
            };
            TerminatingDecision::one_step(Ok(class), TIE_HORIZON)
        }
        (Err(error), _) | (_, Err(error)) => TerminatingDecision::one_step(Err(error), TIE_CAP),
    }
}

/// Negative control: a guessed Interior/Exterior after a cap hit is illegal.
pub fn iteration_cap_guess(
    exhausted: bool,
    guessed: CompactClass,
    cap: u32,
) -> Result<CompactClass, KernelError> {
    if exhausted {
        let _ = guessed;
        Err(KernelError::BranchBudgetExhausted { max_steps: cap })
    } else {
        Ok(guessed)
    }
}

/// Curved-null / geodesic branch: unsupported. Refuse, do not guess capture.
pub fn decide_curved_null_geodesic(_impact: Q, _mu: Q) -> TerminatingDecision<CompactClass> {
    TerminatingDecision::one_step(
        Err(KernelError::UnsupportedPredicate(
            "curved-null / geodesic branch solver is not implemented",
        )),
        TIE_UNSUPPORTED,
    )
}

fn event_at(time: Q, position: [Q; 2]) -> KernelEvent {
    KernelEvent { time, position }
}

fn origin_event(time: Q) -> KernelEvent {
    event_at(time, origin())
}

fn static_unit() -> CausalKernel {
    CausalKernel::new(
        vec![tube(1, vec![genesis(origin(), q(1, 1))])],
        finite_root(),
    )
    .expect("static unit source")
}

pub(crate) fn record_terminating_exact_branches(report: &mut CandidateReport) {
    match exact_branch_manifest() {
        Ok(()) => gate(
            report,
            "exact_branch_manifest_isolated",
            true,
            "New terminating-branch fixtures did not edit frozen production-gate identities or old numeric thresholds.",
        ),
        Err(error) => gate(report, "exact_branch_manifest_isolated", false, error),
    }

    let source = origin_event(Q::zero());
    let before = decide_cone(source, event_at(q(1, 64), r4()), C);
    let on = decide_cone(source, event_at(q(1, 16), r4()), C);
    let after = decide_cone(source, event_at(q(1, 8), r4()), C);
    let cone_ok = before.decision == Ok(BranchDecision::Before)
        && on.decision == Ok(BranchDecision::On)
        && after.decision == Ok(BranchDecision::After)
        && before.steps <= MAX_PREDICATE_STEPS
        && on.steps <= MAX_PREDICATE_STEPS
        && after.steps <= MAX_PREDICATE_STEPS;
    gate(
        report,
        "exact_cone_before_on_after",
        cone_ok,
        "Exact rational cone: c²(t−t_s)² ≶ r². Query r=4, c=64: t=1/64 Before, t=1/16 On, t=1/8 After. One comparison, no loop.",
    );

    let future = decide_cone(source, event_at(q(-1, 1), r4()), C);
    let tie_ok = on.decision == Ok(BranchDecision::On)
        && on.tie_rule == TIE_CONE
        && future.decision.is_err();
    gate(
        report,
        "on_cone_tie_is_visible",
        tie_ok,
        "Tie rule: on-cone equality is visible (closed cone). A query in the source's future refuses rather than iterating.",
    );

    let rs = compact_radius(q(1, 1), C).expect("unit μ compact radius");
    let horizon = decide_capture(
        genesis(origin(), q(1, 1)),
        event_at(q(1, 1), [rs, Q::zero()]),
        C,
    );
    let horizon_ok = horizon.decision
        == Ok(CompactMap::Captured {
            class: CompactClass::OnHorizon,
        })
        && horizon.steps <= MAX_PREDICATE_STEPS;
    gate(
        report,
        "on_horizon_tie_is_capture",
        horizon_ok,
        "Tie rule: r²c⁴ = 4μ² is OnHorizon and the specified map captures. Equality is not deferred to more precision.",
    );

    let singular = decide_capture(genesis(origin(), q(1, 1)), event_at(q(1, 1), origin()), C);
    let nan_class = decide_compact_class_f64([f64::NAN, 0.0], 1.0, C);
    let singular_ok = singular.decision == Ok(CompactMap::Singular)
        && nan_class.decision == Err(KernelError::NonfiniteBranch)
        && !matches!(singular.decision, Ok(CompactMap::Exterior));
    gate(
        report,
        "coincidence_tie_refuses_not_nan",
        singular_ok,
        "Tie rule: r=0 refuses Singular. NaN is NonfiniteBranch. Neither is a 1/r² continuation.",
    );

    let incomplete = decide_certified_exterior(
        &CausalKernel::new(vec![], finite_root()).expect("empty incomplete root"),
        event_at(q(1, 1), [q(1, 1), Q::zero()]),
    );
    let omitted = decide_certified_exterior(
        &CausalKernel::new(
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
        .expect("complete tail root"),
        event_at(q(1, 1), [q(16, 1), Q::zero()]),
    );
    let exterior_ok = incomplete.decision == Err(KernelError::UncertifiedExterior)
        && omitted.decision == Err(KernelError::ExteriorResourceLimit)
        && incomplete.steps <= MAX_PREDICATE_STEPS;
    gate(
        report,
        "certified_exterior_refuses_incomplete",
        exterior_ok,
        "Certified exterior is a terminating decision: incomplete omit and omitted-region queries fail closed in one step.",
    );

    let exact_rs = decide_compact_class_f64([qf(rs), 0.0], 1.0, C);
    let exact_cone = decide_cone_f64(0.0, [0.0, 0.0], 1.0 / 16.0, [4.0, 0.0], C);
    let overflow = q_from_f64(1e300);
    let listed = static_unit();
    let listed_far = listed.acceleration_at(event_at(q(1, 1), r4()));
    let f64_ok = exact_rs.decision == Ok(CompactClass::OnHorizon)
        && exact_cone.decision == Ok(BranchDecision::On)
        && overflow == Err(KernelError::ExactConversionOverflow)
        && decide_compact_class_f64([f64::INFINITY, 0.0], 1.0, C).decision
            == Err(KernelError::NonfiniteBranch)
        && listed_far.is_ok();
    gate(
        report,
        "f64_escalates_or_fails_closed",
        f64_ok,
        "Finite f64 escalates to an exact dyadic (1/2048 is OnHorizon). Inf/NaN refuse. Overflow of Ratio<i128> refuses. No epsilon guess.",
    );

    let cap_zero = decide_with_iteration_budget(1.0, 1.0, 0);
    let cap_guess = iteration_cap_guess(true, CompactClass::Exterior, STATIONARY_CROSSING_CAP);
    let cap_ok = cap_zero.decision == Err(KernelError::BranchBudgetExhausted { max_steps: 0 })
        && cap_guess
            == Err(KernelError::BranchBudgetExhausted {
                max_steps: STATIONARY_CROSSING_CAP,
            })
        && LAPSE_CROSSING_BUDGET_ERROR.contains("exhausted");
    gate(
        report,
        "iteration_cap_is_failed_execution",
        cap_ok,
        "Iteration cap is a failed execution gate. A guessed Exterior/Interior after budget exhaustion is illegal. Stationary lapse cap stays 64.",
    );

    let well_conditioned = circle_crossing([-2.0, 0.0], [4.0, 0.0], 1.0, false);
    let floating_ok = well_conditioned.is_some_and(f64::is_finite);
    gate(
        report,
        "floating_root_is_not_certificate",
        floating_ok,
        "NEGATIVE CONTROL. f64 circle roots can return a finite t (here 0.25) and still are not exact certificates. Frozen fail: floating roots are not production branch truth.",
    );

    let geodesic = decide_curved_null_geodesic(q(4, 1), q(1, 1));
    let geodesic_ok = geodesic.decision
        == Err(KernelError::UnsupportedPredicate(
            "curved-null / geodesic branch solver is not implemented",
        ))
        && geodesic.steps <= MAX_PREDICATE_STEPS;
    gate(
        report,
        "curved_null_geodesic_unsupported",
        geodesic_ok,
        "NEGATIVE CONTROL. Curved-null / geodesic branch solver is not implemented. The kernel refuses rather than guessing photon-sphere capture or light deflection.",
    );

    let kernel_predicates = cone_ok
        && tie_ok
        && horizon_ok
        && singular_ok
        && exterior_ok
        && f64_ok
        && cap_ok
        && floating_ok
        && geodesic_ok;
    gate(
        report,
        "terminating_exact_branches",
        false,
        format!(
            "Kernel-supported predicates terminate or fail closed (fixtures passed={kernel_predicates}): cone, compact class, capture, certified exterior; max_steps={MAX_PREDICATE_STEPS}; ties are visible/capture/refuse. Field values remain f64. Stationary maps still use f64 circle roots and a {STATIONARY_CROSSING_CAP}-crossing cap that is not a certificate. Curved-null/geodesic branch solver is missing. Production terminating_exact_branches stays failed."
        ),
    );
}

#[cfg(test)]
mod tests {
    use super::super::causal_kernel::{in_closed_past_cone, FieldAt};
    use super::*;

    #[test]
    fn exact_branch_manifest_is_additive() {
        exact_branch_manifest().unwrap();
        assert_eq!(MAX_PREDICATE_STEPS, 1);
        assert_eq!(STATIONARY_CROSSING_CAP, 64);
    }

    #[test]
    fn cone_is_before_on_after_in_one_step() {
        let source = origin_event(Q::zero());
        let before = decide_cone(source, event_at(q(1, 64), r4()), C);
        let on = decide_cone(source, event_at(q(1, 16), r4()), C);
        let after = decide_cone(source, event_at(q(1, 8), r4()), C);
        assert_eq!(before.decision, Ok(BranchDecision::Before));
        assert_eq!(on.decision, Ok(BranchDecision::On));
        assert_eq!(after.decision, Ok(BranchDecision::After));
        assert!(in_closed_past_cone(source, event_at(q(1, 16), r4()), C));
        assert!(!in_closed_past_cone(source, event_at(q(1, 64), r4()), C));
        assert!(before.steps <= MAX_PREDICATE_STEPS);
        assert!(decide_cone(source, event_at(q(-1, 1), r4()), C)
            .decision
            .is_err());
    }

    #[test]
    fn compact_ties_are_capture_or_refuse() {
        let rs = compact_radius(q(1, 1), C).unwrap();
        assert_eq!(
            decide_compact_class([rs, Q::zero()], q(1, 1), C).decision,
            Ok(CompactClass::OnHorizon)
        );
        assert_eq!(
            decide_capture(
                genesis(origin(), q(1, 1)),
                event_at(q(1, 1), [rs, Q::zero()]),
                C
            )
            .decision,
            Ok(CompactMap::Captured {
                class: CompactClass::OnHorizon
            })
        );
        assert_eq!(
            decide_capture(genesis(origin(), q(1, 1)), event_at(q(1, 1), origin()), C).decision,
            Ok(CompactMap::Singular)
        );
        assert_eq!(
            decide_compact_class(r4(), q(1, 1), C).decision,
            Ok(CompactClass::Exterior)
        );
    }

    #[test]
    fn f64_escalates_and_nonfinite_refuses() {
        let rs = compact_radius(q(1, 1), C).unwrap();
        assert_eq!(q_from_f64(1.0 / 2048.0).unwrap(), rs);
        assert_eq!(
            decide_compact_class_f64([1.0 / 2048.0, 0.0], 1.0, C).decision,
            Ok(CompactClass::OnHorizon)
        );
        assert_eq!(
            decide_compact_class_f64([f64::NAN, 0.0], 1.0, C).decision,
            Err(KernelError::NonfiniteBranch)
        );
        assert_eq!(
            decide_cone_f64(0.0, [0.0, 0.0], f64::INFINITY, [4.0, 0.0], C).decision,
            Err(KernelError::NonfiniteBranch)
        );
        assert_eq!(q_from_f64(1e300), Err(KernelError::ExactConversionOverflow));
    }

    #[test]
    fn iteration_cap_is_not_a_sign() {
        let hit = decide_with_iteration_budget(4.0, 1.0 / 2048.0 / 2048.0, 0);
        assert_eq!(
            hit.decision,
            Err(KernelError::BranchBudgetExhausted { max_steps: 0 })
        );
        assert!(iteration_cap_guess(true, CompactClass::Interior, 64).is_err());
        let exact = decide_with_iteration_budget(1.0, 1.0, MAX_PREDICATE_STEPS);
        assert_eq!(exact.decision, Ok(CompactClass::OnHorizon));
        assert_eq!(exact.steps, MAX_PREDICATE_STEPS);
    }

    #[test]
    fn floating_root_is_diagnostic_only() {
        let t = circle_crossing([-2.0, 0.0], [4.0, 0.0], 1.0, false).unwrap();
        assert!((t - 0.25).abs() < 1e-15);
        assert!(LAPSE_CROSSING_BUDGET_ERROR.contains("exhausted"));
    }

    #[test]
    fn curved_null_is_unsupported() {
        assert_eq!(
            decide_curved_null_geodesic(q(4, 1), q(1, 1)).decision,
            Err(KernelError::UnsupportedPredicate(
                "curved-null / geodesic branch solver is not implemented"
            ))
        );
    }

    #[test]
    fn certified_exterior_decision_fails_closed() {
        let kernel = CausalKernel::new(vec![], finite_root()).unwrap();
        let query = event_at(q(1, 1), [q(1, 1), Q::zero()]);
        assert_eq!(
            decide_certified_exterior(&kernel, query).decision,
            Err(KernelError::UncertifiedExterior)
        );
        let listed = static_unit();
        assert!(listed.acceleration_at(event_at(q(1, 1), r4())).is_ok());
        assert_eq!(
            decide_certified_exterior(&listed, query).decision,
            Err(KernelError::UncertifiedExterior)
        );
    }

    #[test]
    fn simultaneous_capture_is_first_worldtube() {
        let kernel = CausalKernel::new(
            vec![
                tube(2, vec![genesis([q(1, 8192), Q::zero()], q(1, 1))]),
                tube(1, vec![genesis(origin(), q(1, 1))]),
            ],
            finite_root(),
        )
        .unwrap();
        match kernel.field_at(event_at(q(1, 1), [q(1, 4096), Q::zero()])) {
            Ok(FieldAt::Captured { id, .. }) => {
                assert_eq!(
                    id, 2,
                    "simultaneous capture uses worldtube order, not lowest id"
                );
            }
            other => panic!("expected capture, got {other:?}"),
        }
    }

    #[test]
    fn terminating_exact_branches_does_not_promote() {
        let mut report = CandidateReport {
            id: RESEARCH_LAW_ID.into(),
            version: 0,
            status: "FAIL".into(),
            metrics: Vec::new(),
            gates: Vec::new(),
            evidence: Vec::new(),
        };
        record_terminating_exact_branches(&mut report);
        assert!(
            !report
                .gates
                .iter()
                .find(|g| g.id == "terminating_exact_branches")
                .unwrap()
                .passed
        );
        for id in EXACT_BRANCH_FIXTURE_IDS {
            assert!(
                report.gates.iter().find(|g| g.id == id).unwrap().passed,
                "{id} must pass as a terminating capability or negative control"
            );
        }
    }
}
