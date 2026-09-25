//! Independent-evolution refinement diagnostic, sharing GEM force/root routines.
use crate::coupled_source_response::{
    body_state, body_state_compiled, compile_source_response_opts, CompileOpts, InitialCondition,
    Reference, ResponseError, G,
};
use crate::two_body_bank::{kepler_relative, Case};
use serde::{Deserialize, Serialize};
use std::f64::consts::TAU;
use std::time::Instant;

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Sample {
    pub x: [f64; 2],
    pub v: [f64; 2],
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Behavior {
    pub position_over_a: f64,
    pub energy_error: f64,
    pub momentum_error: f64,
    pub min_radius: f64,
    pub max_radius: f64,
    pub signed_angle: f64,
    pub pass: bool,
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Rung {
    pub steps: usize,
    pub dt: f64,
    pub status: String,
    pub reason: String,
    pub charge: u64,
    pub source_evolution_ops: u64,
    pub stored_history_segments: usize,
    pub complete_charge: bool,
    pub state_queries: u64,
    pub wall_ns: u128,
    pub behavior: Option<Behavior>,
    pub candidate_difference: Option<f64>,
    pub initial_candidate_difference: Option<f64>,
    pub initial_kepler_difference: Option<f64>,
    pub previous_difference: Option<f64>,
    pub samples: Vec<Sample>,
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Report {
    pub version: String,
    pub case: Case,
    pub genesis: InitialCondition,
    pub period: f64,
    pub candidate_charge: u64,
    pub candidate_state_queries: u64,
    pub candidate_wall_ns: u128,
    pub candidate_behavior: Behavior,
    pub rungs: Vec<Rung>,
    pub refinement_ratio: Option<f64>,
    /// Positional refinement only; does not qualify velocity-derived invariants.
    pub reference_screen_pass: bool,
    /// Positional agreement only, conditional on reference positional screening.
    pub candidate_agrees: bool,
    pub total_charge: u64,
    pub complete_charge: bool,
    pub wall_ns: u128,
    pub scope: String,
}
fn difference(a: &[Sample], b: &[Sample], scale: f64) -> f64 {
    assert_eq!(a.len(), b.len());
    a.iter()
        .zip(b)
        .map(|(a, b)| (a.x[0] - b.x[0]).hypot(a.x[1] - b.x[1]) / scale)
        .fold(0.0, f64::max)
}
fn sample(
    mut state: impl FnMut(u64, f64) -> Result<([f64; 2], [f64; 2]), ResponseError>,
    period: f64,
    queries: &mut u64,
) -> Result<Vec<Sample>, ResponseError> {
    let mut result = Vec::new();
    for i in 0..1025 {
        let t = period * i as f64 / 1024.0;
        *queries += 1;
        let (xa, va) = state(0, t)?;
        *queries += 1;
        let (xb, vb) = state(1, t)?;
        let x = [xb[0] - xa[0], xb[1] - xa[1]];
        let v = [vb[0] - va[0], vb[1] - va[1]];
        if !x.iter().chain(v.iter()).all(|v| v.is_finite()) || x[0].hypot(x[1]) <= 0.0 {
            return Err(ResponseError::UnsupportedDomain {
                why: format!("invalid sample {i}"),
            });
        }
        result.push(Sample { x, v });
    }
    Ok(result)
}
/// Physical classifier on the uniform 1025-point observation grid.
/// Invalid inputs are refused rather than hidden by floating maximum reductions.
pub fn behavior(c: &Case, period: f64, samples: &[Sample]) -> Behavior {
    assert!(period.is_finite() && period > 0.0 && samples.len() == 1025);
    assert!(samples.iter().all(|s| s.x.iter().chain(s.v.iter()).all(|v| v.is_finite())
        && s.x[0].hypot(s.x[1]) > 0.0));
    let e0 = -G * c.total_mass / (2.0 * c.a);
    let l0 = (G * c.total_mass * c.a * (1.0 - c.eccentricity.powi(2))).sqrt();
    let mut b = Behavior {
        position_over_a: 0.0,
        energy_error: 0.0,
        momentum_error: 0.0,
        min_radius: f64::INFINITY,
        max_radius: 0.0,
        signed_angle: 0.0,
        pass: false,
    };
    for (i, s) in samples.iter().enumerate() {
        let r = s.x[0].hypot(s.x[1]);
        let expected = kepler_relative(c, period * i as f64 / 1024.0).0;
        b.position_over_a = b
            .position_over_a
            .max((s.x[0] - expected[0]).hypot(s.x[1] - expected[1]) / c.a);
        b.energy_error = b.energy_error.max(
            (0.5 * (s.v[0] * s.v[0] + s.v[1] * s.v[1]) - G * c.total_mass / r - e0).abs()
                / e0.abs(),
        );
        b.momentum_error = b
            .momentum_error
            .max((s.x[0] * s.v[1] - s.x[1] * s.v[0] - l0).abs() / l0);
        b.min_radius = b.min_radius.min(r);
        b.max_radius = b.max_radius.max(r);
        if i > 0 {
            let a = &samples[i - 1].x;
            b.signed_angle += (a[0] * s.x[1] - a[1] * s.x[0]).atan2(a[0] * s.x[0] + a[1] * s.x[1]);
        }
    }
    b.pass = b.position_over_a <= 0.05
        && b.energy_error <= 0.05
        && b.momentum_error <= 0.05
        && b.min_radius >= c.a * (1.0 - c.eccentricity - 0.05)
        && b.max_radius <= c.a * (1.0 + c.eccentricity + 0.05)
        && b.signed_angle >= TAU - 0.05;
    b
}
pub fn measure(
    case: Case,
    genesis: InitialCondition,
    steps: &[usize],
) -> Result<Report, ResponseError> {
    measure_with_lookup(case, genesis, steps, false)
}
pub fn measure_indexed(
    case: Case,
    genesis: InitialCondition,
    steps: &[usize],
) -> Result<Report, ResponseError> {
    measure_with_lookup(case, genesis, steps, true)
}
fn measure_with_lookup(case: Case, genesis: InitialCondition, steps: &[usize], indexed: bool) -> Result<Report, ResponseError> {
    assert!(
        steps.len() >= 3
            && steps.iter().all(|n| *n > 0)
            && steps.windows(2).all(|w| w[1] == 2 * w[0])
    );
    let start = Instant::now();
    let period = TAU * (case.a.powi(3) / (G * case.total_mass)).sqrt();
    let compiled = compile_source_response_opts(
        genesis.clone(),
        vec![],
        period,
        (case.horizon - case.genesis) / 512.0,
        CompileOpts {
            store_pair_inverse: false,
        },
    )?;
    let mut queries = 0;
    let candidate = sample(
        |id, t| body_state_compiled(&compiled, id, t),
        period,
        &mut queries,
    )?;
    let mut report=Report{version:"same-genesis-euler-refinement-v1".into(),candidate_charge:compiled.charge.ledger_total(),candidate_state_queries:queries,candidate_wall_ns:start.elapsed().as_nanos(),candidate_behavior:behavior(&case,period,&candidate),case,genesis,period,rungs:vec![],refinement_ratio:None,reference_screen_pass:false,candidate_agrees:false,total_charge:compiled.charge.ledger_total(),complete_charge:true,wall_ns:0,scope:"Shared GEM equations/root routines; independent Euler evolution. Observed sampled refinement, not interval certification. Reused frozen genesis; historical initialization cost excluded explicitly. Charges are ledger units, not arithmetic; failed API partial counters unavailable.".into()};
    drop(compiled);
    if indexed { report.scope.push_str(" Opt-in indexed Euler history lookup; numerical recurrence unchanged; verification predicates charged."); }
    for &n in steps {
        let start = Instant::now();
        let dt = (period - report.genesis.genesis_t) / n as f64;
        let mut rung = Rung {
            steps: n,
            dt,
            status: "UNSUPPORTED".into(),
            reason: String::new(),
            charge: 0,
            source_evolution_ops: 0,
            stored_history_segments: 0,
            complete_charge: false,
            state_queries: 0,
            wall_ns: 0,
            behavior: None,
            candidate_difference: None,
            initial_candidate_difference: None,
            initial_kepler_difference: None,
            previous_difference: None,
            samples: vec![],
        };
        let reference = Reference::from_genesis(report.genesis.clone(), vec![], dt);
        let evolved = if indexed { reference.evolve_to_indexed(period) } else { reference.evolve_to(period) };
        match evolved {
            Err(e) => rung.reason = format!("reference refused: {e:?}"),
            Ok((bodies, charge)) => {
                rung.charge = charge.ledger_total();
                rung.source_evolution_ops = charge.source_evolution;
                rung.stored_history_segments = bodies.iter().map(|b| b.segments.len()).sum();
                rung.complete_charge = true;
                match sample(
                    |id, t| body_state(&bodies, id, t),
                    period,
                    &mut rung.state_queries,
                ) {
                    Err(e) => rung.reason = format!("sample refused: {e:?}"),
                    Ok(samples) => {
                        rung.behavior = Some(behavior(&report.case, period, &samples));
                        rung.candidate_difference =
                            Some(difference(&candidate, &samples, report.case.a));
                        if let Some(prev) = report.rungs.last() {
                            if prev.status == "MEASURED" {
                                rung.previous_difference =
                                    Some(difference(&prev.samples, &samples, report.case.a));
                            }
                        }
                        rung.initial_candidate_difference =
                            Some(difference(&candidate[..1], &samples[..1], report.case.a));
                        let expected = kepler_relative(&report.case, 0.0).0;
                        rung.initial_kepler_difference = Some(
                            (samples[0].x[0] - expected[0]).hypot(samples[0].x[1] - expected[1])
                                / report.case.a,
                        );
                        rung.samples = samples;
                        rung.status = "MEASURED".into();
                    }
                }
            }
        }
        rung.wall_ns = start.elapsed().as_nanos();
        report.total_charge += rung.charge;
        report.complete_charge &= rung.complete_charge;
        eprintln!(
            "seed={} N={} status={} diff={:?} elapsed={:.3}s",
            report.case.seed,
            n,
            rung.status,
            rung.previous_difference,
            rung.wall_ns as f64 / 1e9
        );
        report.rungs.push(rung);
    }
    let len = report.rungs.len();
    if let (Some(coarse), Some(fine)) = (
        report.rungs[len - 2].previous_difference,
        report.rungs[len - 1].previous_difference,
    ) {
        report.refinement_ratio = if coarse > 0.0 {
            Some(fine / coarse)
        } else {
            None
        };
        report.reference_screen_pass = fine <= 0.005
            && ((coarse <= 1e-10 && fine <= 1e-10)
                || report.refinement_ratio.is_some_and(|r| r <= 0.75));
        report.candidate_agrees = report.reference_screen_pass
            && report.rungs[len - 1]
                .candidate_difference
                .is_some_and(|d| d <= 0.02);
    }
    report.wall_ns = start.elapsed().as_nanos();
    Ok(report)
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn physical_classifier_accepts_kepler_and_rejects_ballistic_and_reversed_motion() {
        let c = Case::from_seed(10);
        let period = TAU * (c.a.powi(3) / (G * c.total_mass)).sqrt();
        let exact: Vec<_> = (0..1025)
            .map(|i| {
                let (x, v) = kepler_relative(&c, period * i as f64 / 1024.0);
                Sample { x, v }
            })
            .collect();
        assert!(behavior(&c, period, &exact).pass);
        let (x, v) = kepler_relative(&c, 0.0);
        let ballistic: Vec<_> = (0..1025)
            .map(|i| {
                let t = period * i as f64 / 1024.0;
                Sample {
                    x: [x[0] + t * v[0], x[1] + t * v[1]],
                    v,
                }
            })
            .collect();
        assert!(!behavior(&c, period, &ballistic).pass);
        let reversed: Vec<_> = exact
            .iter()
            .rev()
            .map(|s| Sample {
                x: s.x,
                v: [-s.v[0], -s.v[1]],
            })
            .collect();
        let b = behavior(&c, period, &reversed);
        assert!(!b.pass && b.signed_angle < 0.0);
    }

    #[test]
    fn invalid_states_cannot_disappear_in_aggregate() {
        let mut queries = 0;
        let result = sample(
            |id, _| Ok(([if id == 0 { f64::NAN } else { 1.0 }, 0.0], [0.0, 0.0])),
            1.0,
            &mut queries,
        );
        assert!(result.is_err());
        assert_eq!(queries, 2);
        let invalid = vec![Sample { x:[1.0,0.0], v:[f64::NAN,0.0] };1025];
        assert!(std::panic::catch_unwind(|| behavior(&Case::from_seed(0),1.0,&invalid)).is_err());
    }

    #[test]
    #[ignore = "explicit causal-block refinement against retained Euler samples"]
    fn causal_block_refinement_probe() {
        let input = std::env::var("ORBIT_REFERENCE_INPUT").unwrap();
        let saved: serde_json::Value =
            serde_json::from_str(&std::fs::read_to_string(input).unwrap()).unwrap();
        let case: Case = serde_json::from_value(saved["case"].clone()).unwrap();
        let genesis: InitialCondition = serde_json::from_value(saved["genesis"].clone()).unwrap();
        let rungs = saved["rungs"].as_array().unwrap();
        let reference: Vec<Sample> =
            serde_json::from_value(rungs.last().unwrap()["samples"].clone()).unwrap();
        assert_eq!(reference.len(), 1025);
        let period = saved["period"].as_f64().unwrap();
        let mut rows = vec![];
        let mut previous: Option<Vec<Sample>> = None;
        for factor in [1, 2, 4, 8] {
            let start = Instant::now();
            let result = crate::coupled_source_response::compile_source_response_refined(
                genesis.clone(),
                vec![],
                period,
                (case.horizon - case.genesis) / 512.0,
                CompileOpts {
                    store_pair_inverse: false,
                },
                factor,
            );
            let row = match result {
                Err(e) => {
                    serde_json::json!({"factor":factor,"status":"UNSUPPORTED","reason":format!("{e:?}"),"complete_charge":false,"wall_ns":start.elapsed().as_nanos()})
                }
                Ok(compiled) => {
                    let mut queries = 0;
                    match sample(
                        |id, t| body_state_compiled(&compiled, id, t),
                        period,
                        &mut queries,
                    ) {
                        Err(e) => {
                            serde_json::json!({"factor":factor,"status":"UNSUPPORTED","reason":format!("{e:?}"),"charge":compiled.charge.ledger_total(),"complete_charge":true,"state_queries":queries,"wall_ns":start.elapsed().as_nanos()})
                        }
                        Ok(samples) => {
                            let prior = previous.as_ref().map(|p| difference(p, &samples, case.a));
                            let row = serde_json::json!({"factor":factor,"status":"MEASURED","charge":compiled.charge.ledger_total(),"complete_charge":true,"state_queries":queries,"wall_ns":start.elapsed().as_nanos(),"interval_functions":compiled.interval_functions.len(),"effective_cadence":compiled.interval_tau,"reference_difference":difference(&reference,&samples,case.a),"previous_difference":prior,"behavior":behavior(&case,period,&samples),"samples":samples});
                            previous = Some(samples);
                            row
                        }
                    }
                }
            };
            eprintln!(
                "factor={factor} reference_diff={} intervals={}",
                row["reference_difference"], row["interval_functions"]
            );
            rows.push(row);
        }
        let output = serde_json::json!({"version":"same-genesis-causal-block-refinement-v1","case":case,"genesis":genesis,"reference_position_screen_pass":saved["reference_screen_pass"],"reference_steps":rungs.last().unwrap()["steps"],"rows":rows});
        if let Some(path) = std::env::var_os("ORBIT_BLOCK_OUTPUT") {
            use std::io::Write;
            let mut file = std::fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(path)
                .unwrap();
            file.write_all(serde_json::to_string_pretty(&output).unwrap().as_bytes())
                .unwrap();
        }
    }

    #[test]
    #[ignore = "explicit, charged full-orbit refinement experiment"]
    fn retained_genesis_reference_probe() {
        let saved: serde_json::Value = serde_json::from_str(include_str!(
            "../../../artifacts/evidence/orbit-duration-20260923/orbit-duration-bank.json"
        ))
        .unwrap();
        let seed: usize = std::env::var("ORBIT_REFERENCE_SEED")
            .unwrap_or("10".into())
            .parse()
            .unwrap();
        let case: Case = serde_json::from_value(saved[seed]["case"].clone()).unwrap();
        let genesis: InitialCondition =
            serde_json::from_value(saved[seed]["initialization"]["resolved_genesis"].clone())
                .unwrap();
        let steps: Vec<usize> = std::env::var("ORBIT_REFERENCE_STEPS")
            .unwrap_or("1024,2048,4096".into())
            .split(',')
            .map(|s| s.parse().unwrap())
            .collect();
        let measured = if std::env::var_os("ORBIT_REFERENCE_INDEXED").is_some() {
            measure_indexed(case, genesis, &steps)
        } else { measure(case, genesis, &steps) };
        let report = match measured {
            Ok(report) => report,
            Err(error) => {
                let refused = serde_json::json!({"status":"UNSUPPORTED", "seed":seed,
                    "reason": format!("candidate refused: {error:?}"), "complete_charge":false,
                    "accounting_scope":"candidate API failure lacks partial counters"});
                if let Some(path) = std::env::var_os("ORBIT_REFERENCE_OUTPUT") {
                    use std::io::Write;
                    let mut file = std::fs::OpenOptions::new()
                        .write(true)
                        .create_new(true)
                        .open(path)
                        .unwrap();
                    file.write_all(serde_json::to_string_pretty(&refused).unwrap().as_bytes())
                        .unwrap();
                }
                eprintln!("{refused}");
                return;
            }
        };
        assert_eq!(report.rungs.len(), steps.len());
        if let Some(path) = std::env::var_os("ORBIT_REFERENCE_OUTPUT") {
            use std::io::Write;
            let mut file = std::fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(path)
                .unwrap();
            file.write_all(serde_json::to_string_pretty(&report).unwrap().as_bytes())
                .unwrap();
        }
        eprintln!(
            "screen={} candidate_agrees={}",
            report.reference_screen_pass, report.candidate_agrees
        );
    }
}
