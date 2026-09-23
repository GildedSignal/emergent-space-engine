//! Frozen finite-arc weak-field behavior bank; see docs/laws/two-body-bank-20260923.md.
//! The physical anchor is analytic Newtonian two-body motion. It is independent
//! of GEM implementation; the separate Euler refinement shares GEM equations.
use crate::coupled_source_response::{
    body_state, body_state_compiled, compile_source_response_opts, field_acceleration, BodyInit,
    Charge, CompileOpts, InitialCondition, Reference, ResponseError, C, COUPLED_RESPONSE_LAW_ID, G,
};
use serde::{Deserialize, Serialize};
use std::f64::consts::{PI, TAU};
use std::time::Instant;

pub const PHYSICAL_BAND: f64 = 0.05;
pub const COMPILED_REFERENCE_BAND: f64 = 0.02;
pub const REFERENCE_REFINEMENT_BAND: f64 = 0.01;
pub const CASE_COUNT: u64 = 12;

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Case {
    pub seed: u64,
    pub a: f64,
    pub eccentricity: f64,
    pub mass_ratio: f64,
    pub total_mass: f64,
    pub compactness: f64,
    pub orientation: f64,
    pub genesis: f64,
    pub horizon: f64,
}
impl Case {
    pub fn from_seed(seed: u64) -> Self {
        assert!(seed < CASE_COUNT);
        let base = seed / 2;
        let a = 4.0 + 2.0 * (base % 3) as f64;
        let compactness = if seed % 2 == 0 {
            1.0 / 512.0
        } else {
            1.0 / 2048.0
        };
        let total_mass = compactness * a * C * C / G;
        Self {
            seed,
            a,
            eccentricity: [0.0, 0.3, 0.6][(base / 2) as usize],
            mass_ratio: [0.01, 0.2, 1.0][(base % 3) as usize],
            total_mass,
            compactness,
            orientation: base as f64 * PI / 7.0,
            genesis: -4.0 * a / C,
            horizon: 0.75 * (a.powi(3) / (G * total_mass)).sqrt(),
        }
    }
    pub fn initial_condition(&self) -> InitialCondition {
        let (x, v) = kepler_relative(self, self.genesis);
        let secondary = self.total_mass * self.mass_ratio / (1.0 + self.mass_ratio);
        let primary = self.total_mass - secondary;
        InitialCondition {
            genesis_t: self.genesis,
            bodies: vec![
                BodyInit {
                    id: 0,
                    mu: primary,
                    x: scale(x, -secondary / self.total_mass),
                    v: scale(v, -secondary / self.total_mass),
                },
                BodyInit {
                    id: 1,
                    mu: secondary,
                    x: scale(x, primary / self.total_mass),
                    v: scale(v, primary / self.total_mass),
                },
            ],
        }
    }
}
fn sub(a: [f64; 2], b: [f64; 2]) -> [f64; 2] {
    [a[0] - b[0], a[1] - b[1]]
}
fn scale(a: [f64; 2], s: f64) -> [f64; 2] {
    [a[0] * s, a[1] * s]
}
fn norm(a: [f64; 2]) -> f64 {
    a[0].hypot(a[1])
}
fn rotate(a: [f64; 2], angle: f64) -> [f64; 2] {
    let (s, c) = angle.sin_cos();
    [c * a[0] - s * a[1], s * a[0] + c * a[1]]
}
fn energy(x: [f64; 2], v: [f64; 2], mu: f64) -> f64 {
    0.5 * (v[0] * v[0] + v[1] * v[1]) - mu / norm(x)
}
fn momentum(x: [f64; 2], v: [f64; 2]) -> f64 {
    x[0] * v[1] - x[1] * v[0]
}

/// Independent ellipse solution; monotone Kepler equation is bracketed on [-pi,pi].
/// Bounded floating bisection is an offline approximate anchor, not canonical authority.
pub fn kepler_relative(case: &Case, t: f64) -> ([f64; 2], [f64; 2]) {
    let n = (G * case.total_mass / case.a.powi(3)).sqrt();
    let m = (n * t + PI).rem_euclid(TAU) - PI;
    let (mut lo, mut hi) = (-PI, PI);
    for _ in 0..64 {
        let mid = (lo + hi) * 0.5;
        if mid - case.eccentricity * mid.sin() < m {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    let e = (lo + hi) * 0.5;
    let q = (1.0 - case.eccentricity.powi(2)).sqrt();
    let de = n / (1.0 - case.eccentricity * e.cos());
    (
        rotate(
            [case.a * (e.cos() - case.eccentricity), case.a * q * e.sin()],
            case.orientation,
        ),
        rotate(
            [-case.a * e.sin() * de, case.a * q * e.cos() * de],
            case.orientation,
        ),
    )
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CaseReport {
    pub case: Case,
    pub initializer: String,
    pub initialization: Option<crate::orbit_initialization::InitializationReport>,
    pub status: String,
    pub reason: String,
    pub physical_position_error: Option<f64>,
    pub energy_drift: Option<f64>,
    pub angular_momentum_drift: Option<f64>,
    pub compiled_reference_error: Option<f64>,
    pub reference_refinement: Option<f64>,
    pub ballistic_position_error: Option<f64>,
    pub compile_charge: u64,
    pub reference_charge: u64,
    pub audit_sample_queries: u64,
    pub diagnostic_field_charge: u64,
    pub initial_position_offset: Option<f64>,
    pub initial_velocity_offset: Option<f64>,
    pub post_start_energy_drift: Option<f64>,
    pub post_start_angular_momentum_drift: Option<f64>,
    pub max_newtonian_force_difference: Option<f64>,
    pub physical_pass: Option<bool>,
    pub numerical_pass: Option<bool>,
    pub accounting_scope: String,
    pub wall_ns: u128,
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct BankReport {
    pub law_id: String,
    pub scope: String,
    pub cases: Vec<CaseReport>,
    pub all_pass: bool,
}

fn valid_residuals(values: &[f64]) -> bool {
    values.iter().all(|x| x.is_finite() && *x >= 0.0)
}

pub fn measure_case(case: Case) -> CaseReport {
    measure_case_mode(case, 0)
}
pub fn measure_initialized_case(case: Case) -> CaseReport {
    measure_case_mode(case, 1)
}
fn measure_case_mode(case: Case, mode: u8) -> CaseReport {
    let initialize = mode != 0;
    let start = Instant::now();
    let (xg, vg) = kepler_relative(&case, case.genesis);
    let mut ballistic = 0.0_f64;
    for i in 0..=32 {
        let t = case.horizon * i as f64 / 32.0;
        let expected = kepler_relative(&case, t).0;
        let drift = [
            xg[0] + vg[0] * (t - case.genesis),
            xg[1] + vg[1] * (t - case.genesis),
        ];
        ballistic = ballistic.max(norm(sub(drift, expected)) / case.a);
    }
    let mut out = CaseReport {
        case,
        initializer: if initialize {crate::orbit_initialization::INITIALIZER_VERSION}else{"kepler-genesis-v0"}.into(),
        initialization:None,
        status: "UNSUPPORTED".into(),
        reason: String::new(),
        physical_position_error: None,
        energy_drift: None,
        angular_momentum_drift: None,
        compiled_reference_error: None,
        reference_refinement: None,
        ballistic_position_error: if initialize {None}else{Some(ballistic)},
        compile_charge: 0,
        reference_charge: 0,
        audit_sample_queries: 0,
        diagnostic_field_charge: 0,
        initial_position_offset: None, initial_velocity_offset: None,
        post_start_energy_drift: None, post_start_angular_momentum_drift: None,
        max_newtonian_force_difference: None, physical_pass: None, numerical_pass: None,
        accounting_scope: "compile/reference counters are returned ledger units, not all arithmetic; sample_queries count requested states; failed calls lose partial counters; wall includes attempts".into(),
        wall_ns: 0,
    };
    let result = (|| -> Result<(), ResponseError> {
        let c = &out.case;
        let mut ic = c.initial_condition();
        let dt = (c.horizon - c.genesis) / 512.0;
        let compiled = if initialize {
            let (compiled, report) = if mode == 2 {
                crate::orbit_initialization::initialize_newton(c)
            } else {
                crate::orbit_initialization::initialize(c)
            };
            out.compile_charge = report.total_compile_charge;
            ic = report.resolved_genesis.clone();
            out.initialization = Some(report);
            compiled.ok_or(ResponseError::UnsupportedDomain {
                why: "versioned shooting initializer refused".into(),
            })?
        } else {
            let compiled = compile_source_response_opts(
                ic.clone(),
                vec![],
                c.horizon,
                dt,
                CompileOpts {
                    store_pair_inverse: false,
                },
            )?;
            out.compile_charge = compiled.charge.ledger_total();
            compiled
        };
        // Identical resolved genesis for this version's no-force control.
        let bx = sub(ic.bodies[1].x, ic.bodies[0].x);
        let bv = sub(ic.bodies[1].v, ic.bodies[0].v);
        let mut ballistic = 0.0_f64;
        for i in 0..=32 {
            let t = c.horizon * i as f64 / 32.0;
            let drift = [
                bx[0] + bv[0] * (t - c.genesis),
                bx[1] + bv[1] * (t - c.genesis),
            ];
            let error = norm(sub(drift, kepler_relative(c, t).0)) / c.a;
            if !error.is_finite() {
                out.status = "FAIL".into();
                return Err(ResponseError::UnsupportedDomain {
                    why: "nonfinite ballistic control".into(),
                });
            }
            ballistic = ballistic.max(error);
        }
        out.ballistic_position_error = Some(ballistic);
        let (coarse, coarse_charge) =
            Reference::from_genesis(ic.clone(), vec![], dt).evolve_to(c.horizon)?;
        out.reference_charge += coarse_charge.ledger_total();
        let (fine, fine_charge) =
            Reference::from_genesis(ic, vec![], dt / 2.0).evolve_to(c.horizon)?;
        out.reference_charge += fine_charge.ledger_total();
        let eg = energy(xg, vg, G * c.total_mass);
        let lg = momentum(xg, vg);
        let (mut physical, mut de, mut dl, mut numerical, mut refinement) =
            (0.0_f64, 0.0_f64, 0.0_f64, 0.0_f64, 0.0_f64);
        let (x0a, v0a) = body_state_compiled(&compiled, 0, 0.0)?;
        let (x0b, v0b) = body_state_compiled(&compiled, 1, 0.0)?;
        let (x0, v0) = (sub(x0b, x0a), sub(v0b, v0a));
        let e0 = energy(x0, v0, G * c.total_mass);
        let l0 = momentum(x0, v0);
        let anchor0 = kepler_relative(c, 0.0);
        out.initial_position_offset = Some(norm(sub(x0, anchor0.0)) / c.a);
        out.initial_velocity_offset =
            Some(norm(sub(v0, anchor0.1)) / (G * c.total_mass / c.a).sqrt());
        let (mut post_e, mut post_l, mut force) = (0.0_f64, 0.0_f64, 0.0_f64);
        let mut field_charge = Charge::default();
        for i in 0..=32 {
            let t = c.horizon * i as f64 / 32.0;
            let (xa, va) = body_state_compiled(&compiled, 0, t)?;
            let (xb, vb) = body_state_compiled(&compiled, 1, t)?;
            let x = sub(xb, xa);
            let v = sub(vb, va);
            let xf = sub(body_state(&fine, 1, t)?.0, body_state(&fine, 0, t)?.0);
            let xc = sub(body_state(&coarse, 1, t)?.0, body_state(&coarse, 0, t)?.0);
            let errors = [
                norm(sub(x, kepler_relative(c, t).0)) / c.a,
                (energy(x, v, G * c.total_mass) - eg).abs() / eg.abs(),
                (momentum(x, v) - lg).abs() / lg.abs(),
                norm(sub(x, xf)) / c.a,
                norm(sub(xf, xc)) / c.a,
            ];
            // f64::max ignores NaN, so validate before any aggregation.
            if !valid_residuals(&errors) {
                out.status = "FAIL".into();
                return Err(ResponseError::UnsupportedDomain {
                    why: format!("nonfinite residual at sample {i}"),
                });
            }
            physical = physical.max(errors[0]);
            de = de.max(errors[1]);
            dl = dl.max(errors[2]);
            numerical = numerical.max(errors[3]);
            refinement = refinement.max(errors[4]);
            let aa =
                field_acceleration(&compiled.worldtubes, t, xa, va, Some(0), &mut field_charge)?;
            let ab =
                field_acceleration(&compiled.worldtubes, t, xb, vb, Some(1), &mut field_charge)?;
            let newton = scale(x, -G * c.total_mass / norm(x).powi(3));
            let diagnostics = [
                (energy(x, v, G * c.total_mass) - e0).abs() / eg.abs(),
                (momentum(x, v) - l0).abs() / lg.abs(),
                norm(sub(sub(ab, aa), newton)) / norm(newton),
            ];
            if !valid_residuals(&diagnostics) {
                out.status = "FAIL".into();
                return Err(ResponseError::UnsupportedDomain {
                    why: format!("nonfinite diagnostic at sample {i}"),
                });
            }
            post_e = post_e.max(diagnostics[0]);
            post_l = post_l.max(diagnostics[1]);
            force = force.max(diagnostics[2]);
            out.audit_sample_queries += 6;
        }
        out.diagnostic_field_charge = field_charge.ledger_total();
        out.post_start_energy_drift = Some(post_e);
        out.post_start_angular_momentum_drift = Some(post_l);
        out.max_newtonian_force_difference = Some(force);
        out.physical_position_error = Some(physical);
        out.energy_drift = Some(de);
        out.angular_momentum_drift = Some(dl);
        out.compiled_reference_error = Some(numerical);
        out.reference_refinement = Some(refinement);
        let physical_pass = physical <= PHYSICAL_BAND && de <= PHYSICAL_BAND && dl <= PHYSICAL_BAND;
        let numerical_pass =
            numerical <= COMPILED_REFERENCE_BAND && refinement <= REFERENCE_REFINEMENT_BAND;
        out.physical_pass = Some(physical_pass);
        out.numerical_pass = Some(numerical_pass);
        let pass =
            physical_pass && numerical_pass && ballistic.is_finite() && ballistic > PHYSICAL_BAND;
        out.status = if pass { "PASS" } else { "FAIL" }.into();
        out.reason=format!("finite arc: Newtonian position/energy/angular bands={PHYSICAL_BAND}; shared-equation compiled/Euler band={COMPILED_REFERENCE_BAND}, Euler refinement band={REFERENCE_REFINEMENT_BAND}; ballistic must fail; not full-orbit stability");
        Ok(())
    })();
    if let Err(err) = result {
        out.reason = format!("candidate or reference refused: {err:?}; no case removed");
    }
    out.wall_ns = start.elapsed().as_nanos();
    out
}

pub fn measure_bank() -> BankReport {
    let cases: Vec<_> = (0..CASE_COUNT)
        .map(|seed| measure_case(Case::from_seed(seed)))
        .collect();
    let all_pass = cases.iter().all(|c| c.status == "PASS");
    BankReport{law_id:COUPLED_RESPONSE_LAW_ID.into(),scope:"12 varied weak-field finite arcs; independent Kepler anchor; no full orbit or canonical gravity qualification".into(),cases,all_pass}
}

pub fn measure_initialized_bank() -> BankReport {
    let cases: Vec<_> = (0..CASE_COUNT)
        .map(|seed| measure_initialized_case(Case::from_seed(seed)))
        .collect();
    let all_pass = cases.iter().all(|c| c.status == "PASS");
    BankReport{law_id:COUPLED_RESPONSE_LAW_ID.into(),scope:"versioned shooting: same 12 weak-field finite arcs; all initialization trials charged; original bank retained".into(),cases,all_pass}
}

pub fn measure_newton_bank() -> BankReport {
    let cases: Vec<_> = (0..CASE_COUNT)
        .map(|seed| measure_case_mode(Case::from_seed(seed), 2))
        .collect();
    let all_pass = cases.iter().all(|c| c.status == "PASS");
    BankReport{law_id:COUPLED_RESPONSE_LAW_ID.into(),scope:"versioned Newton shooting: same 12 finite arcs; all derivative/line-search compiles charged; prior banks retained".into(),cases,all_pass}
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn newton_bank_measures_every_case_and_charges_initialization() {
        let report = measure_newton_bank();
        assert_eq!(report.cases.len(), CASE_COUNT as usize);
        for case in &report.cases {
            let init = case.initialization.as_ref().unwrap();
            assert!(init.trials <= 100);
            assert_eq!(case.compile_charge, init.total_compile_charge);
            if case.status == "PASS" {
                assert!(init.residual.unwrap() <= crate::orbit_initialization::RESIDUAL_TOLERANCE);
                assert!(case
                    .ballistic_position_error
                    .is_some_and(|x| x > PHYSICAL_BAND));
            }
            eprintln!("NEWTON_TWO_BODY {}", serde_json::to_string(case).unwrap());
        }
        if let Some(path) = std::env::var_os("NEWTON_BANK_OUTPUT") {
            use std::io::Write;
            let mut f = std::fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(path)
                .unwrap();
            f.write_all(serde_json::to_string_pretty(&report).unwrap().as_bytes())
                .unwrap();
        }
    }
    #[test]
    fn initialized_bank_keeps_outcomes_without_reclassifying_genesis_bank() {
        let report = measure_initialized_bank();
        assert_eq!(report.cases.len(), CASE_COUNT as usize);
        for case in &report.cases {
            let init = case.initialization.as_ref().unwrap();
            assert!(init.trials <= crate::orbit_initialization::MAX_TRIALS);
            assert_eq!(case.compile_charge, init.total_compile_charge);
            if case.status == "PASS" {
                assert!(init.residual.unwrap() <= crate::orbit_initialization::RESIDUAL_TOLERANCE);
                assert!(case
                    .ballistic_position_error
                    .is_some_and(|e| e > PHYSICAL_BAND));
            }
            eprintln!(
                "INITIALIZED_TWO_BODY {}",
                serde_json::to_string(case).unwrap()
            );
        }
        if let Some(path) = std::env::var_os("INITIALIZED_BANK_OUTPUT") {
            use std::io::Write;
            let mut f = std::fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(path)
                .unwrap();
            f.write_all(serde_json::to_string_pretty(&report).unwrap().as_bytes())
                .unwrap();
        }
    }
    #[test]
    fn nonfinite_sample_cannot_disappear_in_maximum() {
        assert!(!valid_residuals(&[0.0, f64::NAN, 0.0]));
        assert!(!valid_residuals(&[f64::INFINITY]));
        assert!(valid_residuals(&[0.0, 0.01]));
    }
    #[test]
    fn analytic_anchor_preserves_invariants_and_period() {
        for seed in 0..CASE_COUNT {
            let c = Case::from_seed(seed);
            let period = TAU * (c.a.powi(3) / (G * c.total_mass)).sqrt();
            let (x0, v0) = kepler_relative(&c, 0.0);
            let (xp, vp) = kepler_relative(&c, period);
            assert!(norm(sub(x0, xp)) / c.a < 1e-12);
            assert!(norm(sub(v0, vp)) < 1e-12);
            for i in 0..=64 {
                let (x, v) = kepler_relative(&c, period * i as f64 / 64.0);
                let exact_e = -G * c.total_mass / (2.0 * c.a);
                let exact_l = (G * c.total_mass * c.a * (1.0 - c.eccentricity.powi(2))).sqrt();
                assert!((energy(x, v, G * c.total_mass) - exact_e).abs() / exact_e.abs() < 1e-12);
                assert!((momentum(x, v) - exact_l).abs() / exact_l < 1e-12);
            }
        }
    }
    #[test]
    fn bank_keeps_every_measured_outcome_and_rejects_ballistic_control() {
        let report = measure_bank();
        assert_eq!(report.cases.len(), CASE_COUNT as usize);
        for case in &report.cases {
            assert!(
                case.ballistic_position_error
                    .is_some_and(|e| e > PHYSICAL_BAND),
                "seed={} ineffective negative control",
                case.case.seed
            );
            eprintln!("TWO_BODY {}", serde_json::to_string(case).unwrap());
        }
        if let Some(path) = std::env::var_os("TWO_BODY_BANK_OUTPUT") {
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
