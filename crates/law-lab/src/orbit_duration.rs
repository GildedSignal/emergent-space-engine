//! One-period diagnostic after initialization on the original short horizon.
//! Sampling cannot certify interval-wide behavior or permanent boundedness.
use crate::coupled_source_response::{
    body_state_compiled, compile_source_response_opts, CompileOpts, COUPLED_RESPONSE_LAW_ID, G,
};
use crate::orbit_initialization::{initialize_newton, InitializationReport};
use crate::two_body_bank::{kepler_relative, Case, PHYSICAL_BAND};
use serde::{Deserialize, Serialize};
use std::f64::consts::TAU;
use std::time::Instant;

pub const DURATION_VERSION: &str = "kepler-one-period-after-short-shoot-v1";
pub const DURATION_SAMPLES: usize = 1025;

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct OrbitDurationReport {
    pub version: String,
    pub law_id: String,
    /// Original calibration case: horizon is deliberately not extended here.
    pub case: Case,
    pub period: f64,
    pub compile_dt: f64,
    pub metadata_dt_divisor: usize,
    pub initialization: InitializationReport,
    pub status: String,
    pub reason: String,
    pub physical_band: f64,
    pub requested_samples: usize,
    pub completed_samples: usize,
    pub position_error_over_a: Option<f64>,
    pub newtonian_energy_drift: Option<f64>,
    pub angular_momentum_drift: Option<f64>,
    pub min_separation: Option<f64>,
    pub max_separation: Option<f64>,
    pub signed_angular_coverage: Option<f64>,
    pub radial_lower: f64,
    pub radial_upper: f64,
    pub minimum_angular_coverage: f64,
    pub initializer_compile_charge: u64,
    pub duration_compile_charge: u64,
    pub total_compile_charge: u64,
    pub complete_compile_charge: bool,
    /// Counts reconstruction queries; not arithmetic operations or a time proxy.
    pub sample_state_queries: u64,
    pub initialization_wall_ns: u128,
    pub duration_compile_wall_ns: u128,
    pub wall_ns: u128,
    pub accounting_scope: String,
}

pub fn measure_duration(case: Case) -> OrbitDurationReport {
    measure_duration_with_metadata_dt(case, 1)
}

/// Varies stored domain dt only. Collocation does not use this as resolution.
pub fn measure_duration_with_metadata_dt(case: Case, refinement: usize) -> OrbitDurationReport {
    assert!(refinement > 0);
    let start = Instant::now();
    let period = TAU * (case.a.powi(3) / (G * case.total_mass)).sqrt();
    // Preserve calibration metadata. This dt does not control causal-block
    // collocation resolution; varying it is not a convergence experiment.
    let dt = (case.horizon - case.genesis) / (512.0 * refinement as f64);
    let (calibrated, initialization) = initialize_newton(&case);
    let initialization_wall_ns = start.elapsed().as_nanos();
    let mut report = OrbitDurationReport {
        version: DURATION_VERSION.into(),
        law_id: COUPLED_RESPONSE_LAW_ID.into(),
        period,
        compile_dt: dt,
        metadata_dt_divisor: refinement,
        status: "UNSUPPORTED".into(),
        reason: String::new(),
        physical_band: PHYSICAL_BAND,
        requested_samples: DURATION_SAMPLES,
        completed_samples: 0,
        position_error_over_a: None,
        newtonian_energy_drift: None,
        angular_momentum_drift: None,
        min_separation: None,
        max_separation: None,
        signed_angular_coverage: None,
        radial_lower: case.a * (1.0 - case.eccentricity - PHYSICAL_BAND),
        radial_upper: case.a * (1.0 + case.eccentricity + PHYSICAL_BAND),
        minimum_angular_coverage: TAU - PHYSICAL_BAND,
        initializer_compile_charge: initialization.total_compile_charge,
        duration_compile_charge: 0,
        total_compile_charge: initialization.total_compile_charge,
        complete_compile_charge: initialization.complete_charge,
        sample_state_queries: 0,
        initialization_wall_ns,
        duration_compile_wall_ns: 0,
        wall_ns: 0,
        accounting_scope: "All returned initialization and duration compile ledgers; a failed compile lacks partial counters and is flagged. State-query counts exclude analytic arithmetic; total wall includes it. Offline sampled diagnostic, not an engine WorkBudget or interval certificate.".into(),
        initialization,
        case,
    };
    if calibrated.is_none() {
        report.reason = format!(
            "short-horizon initializer refused: {}",
            report.initialization.reason
        );
        report.wall_ns = start.elapsed().as_nanos();
        return report;
    }
    // Release the short history before allocating the one-period compilation.
    drop(calibrated);
    let compile_start = Instant::now();
    let compiled = compile_source_response_opts(
        report.initialization.resolved_genesis.clone(),
        vec![],
        period,
        dt,
        CompileOpts {
            store_pair_inverse: false,
        },
    );
    report.duration_compile_wall_ns = compile_start.elapsed().as_nanos();
    let compiled = match compiled {
        Ok(compiled) => compiled,
        Err(error) => {
            report.complete_compile_charge = false;
            report.reason =
                format!("duration compile refused; failed partial ledger unavailable: {error:?}");
            report.wall_ns = start.elapsed().as_nanos();
            return report;
        }
    };
    report.duration_compile_charge = compiled.charge.ledger_total();
    report.total_compile_charge += report.duration_compile_charge;
    let c = &report.case;
    let exact_energy = -G * c.total_mass / (2.0 * c.a);
    let exact_momentum = (G * c.total_mass * c.a * (1.0 - c.eccentricity.powi(2))).sqrt();
    let (mut position_error, mut energy_error, mut momentum_error) = (0.0_f64, 0.0_f64, 0.0_f64);
    let (mut min_r, mut max_r) = (f64::INFINITY, 0.0_f64);
    let mut angle = 0.0_f64;
    let mut previous_unit: Option<[f64; 2]> = None;
    for i in 0..DURATION_SAMPLES {
        let t = period * i as f64 / (DURATION_SAMPLES - 1) as f64;
        report.sample_state_queries += 1;
        let first = body_state_compiled(&compiled, 0, t);
        report.sample_state_queries += 1;
        let second = body_state_compiled(&compiled, 1, t);
        let ((xa, va), (xb, vb)) = match (first, second) {
            (Ok(a), Ok(b)) => (a, b),
            (a, b) => {
                report.reason = format!("duration state query refused at sample {i}: {a:?}; {b:?}");
                report.wall_ns = start.elapsed().as_nanos();
                return report;
            }
        };
        let x = [xb[0] - xa[0], xb[1] - xa[1]];
        let v = [vb[0] - va[0], vb[1] - va[1]];
        let radius = x[0].hypot(x[1]);
        let expected = kepler_relative(c, t).0;
        let energy = 0.5 * (v[0] * v[0] + v[1] * v[1]) - G * c.total_mass / radius;
        let momentum = x[0] * v[1] - x[1] * v[0];
        let errors = [
            (x[0] - expected[0]).hypot(x[1] - expected[1]) / c.a,
            (energy - exact_energy).abs() / exact_energy.abs(),
            (momentum - exact_momentum).abs() / exact_momentum.abs(),
        ];
        if !radius.is_finite() || radius <= 0.0 || !errors.iter().all(|x| x.is_finite()) {
            report.status = "FAIL".into();
            report.reason = format!("nonfinite/coincident duration state at sample {i}");
            report.wall_ns = start.elapsed().as_nanos();
            return report;
        }
        position_error = position_error.max(errors[0]);
        energy_error = energy_error.max(errors[1]);
        momentum_error = momentum_error.max(errors[2]);
        min_r = min_r.min(radius);
        max_r = max_r.max(radius);
        let unit = [x[0] / radius, x[1] / radius];
        if let Some(previous) = previous_unit {
            angle += (previous[0] * unit[1] - previous[1] * unit[0])
                .atan2(previous[0] * unit[0] + previous[1] * unit[1]);
        }
        previous_unit = Some(unit);
        report.completed_samples += 1;
        // Keep measured prefixes available if a later query fails.
        report.position_error_over_a = Some(position_error);
        report.newtonian_energy_drift = Some(energy_error);
        report.angular_momentum_drift = Some(momentum_error);
        report.min_separation = Some(min_r);
        report.max_separation = Some(max_r);
        report.signed_angular_coverage = Some(angle);
        // A later unavailable sample must not erase an already observed failure.
        // Angular coverage is only a terminal gate, so exclude it here.
        if position_error > PHYSICAL_BAND
            || energy_error > PHYSICAL_BAND
            || momentum_error > PHYSICAL_BAND
            || min_r < report.radial_lower
            || max_r > report.radial_upper
        {
            report.status = "FAIL".into();
        }
    }
    let pass = position_error <= PHYSICAL_BAND
        && energy_error <= PHYSICAL_BAND
        && momentum_error <= PHYSICAL_BAND
        && min_r >= report.radial_lower
        && max_r <= report.radial_upper
        && angle.is_finite()
        && angle >= report.minimum_angular_coverage;
    report.status = if pass { "PASS" } else { "FAIL" }.into();
    report.reason = "One nominal period with fixed short-horizon initialized genesis; sampled position/energy/angular-momentum bands, padded radial envelope and signed angular coverage. No interval-wide or permanent-boundedness claim; no physical-law promotion.".into();
    report.wall_ns = start.elapsed().as_nanos();
    report
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn failed_case_metadata_dt_control_retains_outcomes() {
        let reports: Vec<_> = [4, 8, 9, 10, 11]
            .into_iter()
            .map(|seed| measure_duration_with_metadata_dt(Case::from_seed(seed), 2))
            .collect();
        for report in &reports {
            assert_eq!(report.metadata_dt_divisor, 2);
            assert_eq!(
                report.case.horizon,
                Case::from_seed(report.case.seed).horizon
            );
            assert_eq!(
                report.total_compile_charge,
                report.initializer_compile_charge + report.duration_compile_charge
            );
        }
        if let Some(path) = std::env::var_os("ORBIT_DURATION_REFINEMENT_OUTPUT") {
            use std::io::Write;
            let mut file = std::fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(path)
                .unwrap();
            file.write_all(serde_json::to_string_pretty(&reports).unwrap().as_bytes())
                .unwrap();
        }
    }

    #[test]
    fn twelve_case_one_period_bank_retains_each_outcome() {
        let reports: Vec<_> = (0..12)
            .map(|seed| measure_duration(Case::from_seed(seed)))
            .collect();
        for (seed, report) in reports.iter().enumerate() {
            assert_eq!(report.case.seed as usize, seed);
            assert_eq!(report.case.horizon, Case::from_seed(seed as u64).horizon);
            assert_eq!(
                report.total_compile_charge,
                report.initializer_compile_charge + report.duration_compile_charge
            );
            assert!(matches!(
                report.status.as_str(),
                "PASS" | "FAIL" | "UNSUPPORTED"
            ));
            if report.status == "PASS" {
                assert_eq!(report.completed_samples, DURATION_SAMPLES);
                assert!(report.complete_compile_charge);
            }
        }
        if let Some(path) = std::env::var_os("ORBIT_DURATION_BANK_OUTPUT") {
            use std::io::Write;
            let mut file = std::fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(path)
                .unwrap();
            file.write_all(serde_json::to_string_pretty(&reports).unwrap().as_bytes())
                .unwrap();
        }
        eprintln!(
            "ORBIT_DURATION_BANK {}",
            serde_json::to_string(&reports).unwrap()
        );
    }

    #[test]
    fn circular_seed0_one_period_probe_retains_outcome() {
        // First discriminating rung only. Do not turn this into a bank until
        // reviewing its retained outcome and fully charged cost.
        let report = measure_duration(Case::from_seed(0));
        assert_eq!(report.case.seed, 0);
        assert_eq!(report.case.horizon, Case::from_seed(0).horizon);
        assert_eq!(report.requested_samples, 1025);
        assert_eq!(
            report.total_compile_charge,
            report.initializer_compile_charge + report.duration_compile_charge
        );
        assert!(matches!(
            report.status.as_str(),
            "PASS" | "FAIL" | "UNSUPPORTED"
        ));
        if report.status == "PASS" {
            assert_eq!(report.completed_samples, DURATION_SAMPLES);
            assert!(report.complete_compile_charge);
        }
        eprintln!("ORBIT_DURATION {}", serde_json::to_string(&report).unwrap());
        if let Some(path) = std::env::var_os("ORBIT_DURATION_OUTPUT") {
            use std::io::Write;
            let mut file = std::fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(path)
                .unwrap();
            file.write_all(serde_json::to_string_pretty(&report).unwrap().as_bytes())
                .unwrap();
        }
    }
}
