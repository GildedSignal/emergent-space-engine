//! Isolated compact-field research: exact `r_s = 2μ/c²` membership and a
//! finite absorbing capture map. This is not Schwarzschild/Kerr, not a
//! geodesic integrator, and does not promote `compact_field_certification`.
//!
//! The production gate stays failed. These fixtures measure that Newton has
//! no horizon or GR deflection, that the shell-lapse domain misses `r_s`,
//! and that the retarded kernels never continue 1/r² through r=0.

use super::causal_kernel::{
    compact_class, compact_map, compact_radius, finite_root, genesis, origin, q, qf, r4, tube,
    CausalKernel, CompactClass, CompactMap, FieldAt, KernelError, KernelEvent, SourceSegment, C, Q,
    RESEARCH_LAW_ID,
};
use super::coupled::COUPLED_LAW_ID;
use super::{gate, gravitational_acceleration, norm, CandidateReport, Metric};
use num_traits::Zero;
use serde::Deserialize;

const MANIFEST: &str = include_str!("../../../scenarios/law-gates.json");

#[derive(Clone, Deserialize)]
struct CompactFileSlice {
    compact_field_research: CompactResearchManifest,
    stationary_metric: LapseDomain,
    units: FrozenUnits,
}

#[derive(Clone, Deserialize)]
struct CompactResearchManifest {
    gate: String,
    parent_kernel: String,
    coupled_kernel: String,
    light_speed: i128,
    compact_radius: [i128; 2],
    mu: [i128; 2],
    lapse_minimum_radius: [i128; 2],
    fixtures: Vec<NamedFixture>,
}

#[derive(Clone, Deserialize)]
struct LapseDomain {
    minimum_radius: f64,
}

#[derive(Clone, Deserialize)]
struct FrozenUnits {
    gravitational_parameter: f64,
    light_speed: f64,
}

#[derive(Clone, Deserialize)]
struct NamedFixture {
    id: String,
}

pub(crate) const COMPACT_FIXTURE_IDS: [&str; 8] = [
    "exact_compact_membership",
    "interior_capture_not_newton",
    "on_horizon_capture",
    "coincidence_singular_not_nan",
    "causal_compact_after_cone",
    "newton_continues_through_horizon",
    "lapse_domain_misses_compact",
    "newton_deflection_not_gr",
];

pub fn compact_manifest() -> Result<(), String> {
    let slice: CompactFileSlice = serde_json::from_str(MANIFEST).map_err(|e| e.to_string())?;
    if slice.compact_field_research.gate != "compact_field_certification" {
        return Err("compact-field gate must remain compact_field_certification".into());
    }
    if slice.compact_field_research.parent_kernel != RESEARCH_LAW_ID {
        return Err("compact-field parent must remain the retarded monopole kernel".into());
    }
    if slice.compact_field_research.coupled_kernel != COUPLED_LAW_ID {
        return Err("compact-field coupled kernel id drifted".into());
    }
    if slice.compact_field_research.light_speed != C
        || slice.units.light_speed != C as f64
        || slice.compact_field_research.mu != [1, 1]
        || slice.compact_field_research.compact_radius != [1, 2048]
        || slice.compact_field_research.lapse_minimum_radius != [1, 16]
        || slice.stationary_metric.minimum_radius != 0.0625
        || slice.units.gravitational_parameter != 1.0
    {
        return Err("compact-field research thresholds were weakened or retuned".into());
    }
    let ids: Vec<&str> = slice
        .compact_field_research
        .fixtures
        .iter()
        .map(|f| f.id.as_str())
        .collect();
    if ids != COMPACT_FIXTURE_IDS {
        return Err("compact-field fixtures were renamed, dropped or reordered".into());
    }
    let expected = compact_radius(q(1, 1), C).ok_or("compact radius of unit μ")?;
    if expected != q(1, 2048) {
        return Err("unit compact radius is not the exact rational 2μ/c² = 1/2048".into());
    }
    Ok(())
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

fn static_unit() -> CausalKernel {
    CausalKernel::new(
        vec![tube(1, vec![genesis(origin(), q(1, 1))])],
        finite_root(),
    )
    .expect("static unit source")
}

fn event_at(position: [Q; 2]) -> KernelEvent {
    KernelEvent {
        time: q(1, 1),
        position,
    }
}

fn interior_query() -> [Q; 2] {
    [q(1, 4096), Q::zero()]
}

fn horizon_query() -> [Q; 2] {
    [q(1, 2048), Q::zero()]
}

fn newton_hyperbolic_deflection(mu: f64, c: f64, impact: f64) -> f64 {
    // Unbound Newton particle from infinity at speed c: e = √(1 + (c² b/μ)²),
    // turning angle 2 arcsin(1/e). Weak-field limit is 2μ/(c²b), half of GR.
    let eccentricity = (1.0 + (c * c * impact / mu).powi(2)).sqrt();
    2.0 * (1.0 / eccentricity).asin()
}

fn gr_weak_light_deflection(mu: f64, c: f64, impact: f64) -> f64 {
    4.0 * mu / (c * c * impact)
}

pub(crate) fn record_compact_field(report: &mut CandidateReport) {
    match compact_manifest() {
        Ok(()) => gate(
            report,
            "compact_manifest_isolated",
            true,
            "New compact-field fixtures did not edit frozen production-gate identities or old numeric thresholds.",
        ),
        Err(error) => gate(report, "compact_manifest_isolated", false, error),
    }

    let rs = compact_radius(q(1, 1), C).expect("unit μ compact radius");
    let interior = compact_class(interior_query(), q(1, 1), C);
    let on = compact_class(horizon_query(), q(1, 1), C);
    let far = compact_class(r4(), q(1, 1), C);
    let membership_ok = rs == q(1, 2048)
        && interior == CompactClass::Interior
        && on == CompactClass::OnHorizon
        && far == CompactClass::Exterior;
    gate(
        report,
        "exact_compact_membership",
        membership_ok,
        "Exact rational class: r_s=2μ/c²=1/2048; r=1/4096 Interior; r=1/2048 OnHorizon; r=4 Exterior. Compared as r²c⁴ ≶ 4μ².",
    );

    let kernel = static_unit();
    let interior_event = event_at(interior_query());
    let interior_field = kernel.field_at(interior_event);
    let interior_accel = kernel.acceleration_at(interior_event);
    let newton_interior = gravitational_acceleration([qf(q(1, 4096)), 0.0], 1.0);
    let interior_ok = matches!(
        interior_field,
        Ok(FieldAt::Captured {
            id: 1,
            class: CompactClass::Interior
        })
    ) && matches!(interior_accel, Err(KernelError::CompactForbidden { id: 1 }))
        && newton_interior
            .as_ref()
            .is_ok_and(|a| a.iter().all(|x| x.is_finite()) && norm(*a) > 0.0);
    if let Ok(a) = newton_interior {
        push_metric(
            report,
            "interior_capture_not_newton",
            "newton_acceleration",
            norm(a),
            "acceleration",
            0.0,
            false,
        );
    }
    gate(
        report,
        "interior_capture_not_newton",
        interior_ok,
        "Interior r=1/4096: kernel field_at is Captured, acceleration_at refuses. Newton 1/r² is still finite there — that is the measured missing horizon, not a certified GR interior.",
    );

    let horizon_event = event_at(horizon_query());
    let horizon_field = kernel.field_at(horizon_event);
    let horizon_accel = kernel.acceleration_at(horizon_event);
    let newton_horizon = gravitational_acceleration([qf(rs), 0.0], 1.0);
    let horizon_ok = matches!(
        horizon_field,
        Ok(FieldAt::Captured {
            id: 1,
            class: CompactClass::OnHorizon
        })
    ) && matches!(horizon_accel, Err(KernelError::CompactForbidden { id: 1 }))
        && newton_horizon
            .as_ref()
            .is_ok_and(|a| a.iter().all(|x| x.is_finite()) && norm(*a) > 0.0);
    gate(
        report,
        "on_horizon_capture",
        horizon_ok,
        "On-horizon r=1/2048 is an exact branch: Captured(OnHorizon), not Newton 1/r² and not a floating root.",
    );

    let coincidence = event_at(origin());
    let singular = kernel.field_at(coincidence);
    let newton_r0 = gravitational_acceleration([0.0, 0.0], 1.0);
    let singular_ok = matches!(singular, Err(KernelError::Singular { id: 1 }))
        && newton_r0.is_err()
        && !matches!(
            compact_map(genesis(origin(), q(1, 1)), coincidence, C,),
            CompactMap::Exterior
        );
    gate(
        report,
        "coincidence_singular_not_nan",
        singular_ok,
        "r=0 is Singular (finite error). Neither the kernel nor Newton returns NaN or a 1/r² continuation through the origin.",
    );

    let causal_ok = match causal_compact_two_sided() {
        Ok((pre, post)) => {
            let pre_ok = matches!(pre, FieldAt::Acceleration(a) if a == [0.0, 0.0]);
            let post_ok = matches!(
                post,
                FieldAt::Captured {
                    id: 1,
                    class: CompactClass::Interior
                }
            );
            pre_ok && post_ok
        }
        Err(_) => false,
    };
    gate(
        report,
        "causal_compact_after_cone",
        causal_ok,
        "μ 0→1 at t=0, query r=1/4096. Pre-cone t=1/524288 sees genesis μ=0 (no capture). Post-cone t=1/131072 captures. Compact of a mass change is retarded.",
    );

    let newton_through = newton_horizon
        .as_ref()
        .is_ok_and(|a| a.iter().all(|x| x.is_finite()) && norm(*a) > 0.0);
    if let Ok(a) = newton_horizon {
        push_metric(
            report,
            "newton_continues_through_horizon",
            "newton_acceleration_at_rs",
            norm(a),
            "acceleration",
            0.0,
            false,
        );
    }
    gate(
        report,
        "newton_continues_through_horizon",
        newton_through,
        "NEGATIVE CONTROL. Stationary 1/r² at r_s is finite. Newtonian gravity has no horizon; this is the frozen G2 compact failure of Verlet, measured rather than asserted.",
    );

    let lapse_min = 1.0 / 16.0;
    let rs_f = qf(rs);
    let lapse_miss = lapse_min > rs_f;
    push_metric(
        report,
        "lapse_domain_misses_compact",
        "lapse_min_over_rs",
        lapse_min / rs_f,
        "ratio",
        1.0,
        false,
    );
    gate(
        report,
        "lapse_domain_misses_compact",
        lapse_miss,
        "NEGATIVE CONTROL. Frozen shell-lapse domain starts at r=1/16; r_s=1/2048 is 128× closer. The lapse laboratory never reaches compact radius and is not Schwarzschild.",
    );

    let mu_f = 1.0;
    let c_f = C as f64;
    let impact = 4.0;
    let newton_delta = newton_hyperbolic_deflection(mu_f, c_f, impact);
    let gr_delta = gr_weak_light_deflection(mu_f, c_f, impact);
    let deflection_gap = (newton_delta - gr_delta).abs();
    let deflection_ok = newton_delta.is_finite()
        && gr_delta.is_finite()
        && deflection_gap > 0.0
        && newton_delta < gr_delta;
    push_metric(
        report,
        "newton_deflection_not_gr",
        "newton_minus_gr",
        deflection_gap,
        "radian",
        0.0,
        false,
    );
    gate(
        report,
        "newton_deflection_not_gr",
        deflection_ok,
        format!(
            "NEGATIVE CONTROL. Unbound Newton flyby at b=4, v=c turns by {newton_delta:.12e} rad; GR weak-field light deflection 4μ/(c²b) is {gr_delta:.12e}. The kernel has no geodesic map. Factor-of-two (and missing photon-sphere capture) is the frozen G2 deflection hole."
        ),
    );

    let certified = membership_ok
        && interior_ok
        && horizon_ok
        && singular_ok
        && causal_ok
        && newton_through
        && lapse_miss
        && deflection_ok;
    gate(
        report,
        "compact_field_certification",
        false,
        format!(
            "Exact membership and absorbing capture are implemented (fixtures passed={certified}). Capture/refuse is not Schwarzschild/Kerr: Newton remains finite at r_s, lapse min r=1/16 misses r_s=1/2048, and Newton flyby deflection {newton_delta:.12e} ≠ GR {gr_delta:.12e}. No photon sphere, no light-bending geodesic, no terminating curved-null branch."
        ),
    );
}

fn causal_compact_two_sided() -> Result<(FieldAt, FieldAt), KernelError> {
    let query = interior_query();
    let changed = CausalKernel::new(
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
    )?;
    let pre = changed.field_at(KernelEvent {
        time: q(1, 524_288),
        position: query,
    })?;
    let post = changed.field_at(KernelEvent {
        time: q(1, 131_072),
        position: query,
    })?;
    Ok((pre, post))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn compact_radius_is_exact_two_mu_over_c2() {
        compact_manifest().unwrap();
        assert_eq!(compact_radius(q(1, 1), C).unwrap(), q(1, 2048));
        assert_eq!(compact_radius(q(2, 1), C).unwrap(), q(1, 1024));
        assert!(compact_radius(Q::zero(), C).is_none());
    }

    #[test]
    fn compact_class_is_exact_on_interior_horizon_and_far() {
        assert_eq!(
            compact_class(interior_query(), q(1, 1), C),
            CompactClass::Interior
        );
        assert_eq!(
            compact_class(horizon_query(), q(1, 1), C),
            CompactClass::OnHorizon
        );
        assert_eq!(compact_class(r4(), q(1, 1), C), CompactClass::Exterior);
        assert_eq!(compact_class(origin(), q(1, 1), C), CompactClass::Interior);
    }

    #[test]
    fn interior_is_captured_and_newton_is_not() {
        let kernel = static_unit();
        let query = event_at(interior_query());
        assert_eq!(
            kernel.field_at(query).unwrap(),
            FieldAt::Captured {
                id: 1,
                class: CompactClass::Interior
            }
        );
        assert!(matches!(
            kernel.acceleration_at(query),
            Err(KernelError::CompactForbidden { id: 1 })
        ));
        let newton = gravitational_acceleration([1.0 / 4096.0, 0.0], 1.0).unwrap();
        assert!(newton.iter().all(|x| x.is_finite()));
        assert!(norm(newton) > 1.0);
        match kernel.field_at(event_at(r4())).unwrap() {
            FieldAt::Acceleration(a) => {
                assert_eq!(a, gravitational_acceleration([4.0, 0.0], 1.0).unwrap())
            }
            FieldAt::Captured { .. } => panic!("far query must remain exterior Newton"),
        }
    }

    #[test]
    fn coincidence_is_singular_not_nan() {
        let kernel = static_unit();
        assert!(matches!(
            kernel.field_at(event_at(origin())),
            Err(KernelError::Singular { id: 1 })
        ));
        assert!(gravitational_acceleration([0.0, 0.0], 1.0).is_err());
        assert!(matches!(
            compact_map(genesis(origin(), q(1, 1)), event_at(origin()), C),
            CompactMap::Singular
        ));
    }

    #[test]
    fn compact_of_a_mass_change_is_retarded() {
        let (pre, post) = causal_compact_two_sided().unwrap();
        assert_eq!(pre, FieldAt::Acceleration([0.0, 0.0]));
        assert_eq!(
            post,
            FieldAt::Captured {
                id: 1,
                class: CompactClass::Interior
            }
        );
    }

    #[test]
    fn newton_deflection_is_half_of_gr_weak_field() {
        let newton = newton_hyperbolic_deflection(1.0, 64.0, 4.0);
        let gr = gr_weak_light_deflection(1.0, 64.0, 4.0);
        assert!((gr - 1.0 / 4096.0).abs() < 1e-18);
        assert!(newton < gr);
        assert!((newton * 2.0 - gr).abs() / gr < 1e-8);
    }

    #[test]
    fn compact_field_does_not_promote() {
        let mut report = CandidateReport {
            id: RESEARCH_LAW_ID.into(),
            version: 0,
            status: "FAIL".into(),
            metrics: Vec::new(),
            gates: Vec::new(),
            evidence: Vec::new(),
        };
        record_compact_field(&mut report);
        assert!(
            !report
                .gates
                .iter()
                .find(|g| g.id == "compact_field_certification")
                .unwrap()
                .passed
        );
        for id in COMPACT_FIXTURE_IDS {
            assert!(
                report.gates.iter().find(|g| g.id == id).unwrap().passed,
                "{id} must pass as an honest compact capability or negative control"
            );
        }
    }
}
