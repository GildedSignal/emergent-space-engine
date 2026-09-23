//! Versioned offline shooting initialization. Never edits state at observation start.
use crate::coupled_source_response::{
    body_state_compiled, compile_source_response_opts, CompileOpts, InitialCondition,
    SourceResponse,
};
use crate::two_body_bank::{kepler_relative, Case};
use serde::{Deserialize, Serialize};

pub const INITIALIZER_VERSION: &str = "kepler-observation-shoot-v1";
pub const MAX_TRIALS: usize = 8;
pub const RESIDUAL_TOLERANCE: f64 = 1e-8;

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct InitializationReport {
    pub version: String,
    pub trials: usize,
    pub residual: Option<f64>,
    /// Includes every returned compile ledger, including the accepted trial once.
    pub total_compile_charge: u64,
    pub complete_charge: bool,
    pub resolved_genesis: InitialCondition,
    pub reason: String,
}

pub fn initialize(case: &Case) -> (Option<SourceResponse>, InitializationReport) {
    let mut ic = case.initial_condition();
    let (target_x, target_v) = kepler_relative(case, 0.0);
    let velocity_scale = (crate::coupled_source_response::G * case.total_mass / case.a).sqrt();
    let elapsed = -case.genesis;
    let mut report = InitializationReport {
        version: INITIALIZER_VERSION.into(),
        trials: 0,
        residual: None,
        total_compile_charge: 0,
        complete_charge: true,
        resolved_genesis: ic.clone(),
        reason: String::new(),
    };
    for _ in 0..MAX_TRIALS {
        report.trials += 1;
        report.resolved_genesis = ic.clone();
        let compiled = match compile_source_response_opts(
            ic.clone(),
            vec![],
            case.horizon,
            (case.horizon - case.genesis) / 512.0,
            CompileOpts {
                store_pair_inverse: false,
            },
        ) {
            Ok(c) => c,
            Err(e) => {
                report.complete_charge = false;
                report.reason =
                    format!("compile refused; failed-call partial charge unavailable: {e:?}");
                return (None, report);
            }
        };
        report.total_compile_charge += compiled.charge.ledger_total();
        let mut residual = 0.0_f64;
        let mut corrections = Vec::new();
        for b in &ic.bodies {
            let fraction = if b.id == 0 {
                -ic.bodies[1].mu / case.total_mass
            } else {
                ic.bodies[0].mu / case.total_mass
            };
            let (x, v) = match body_state_compiled(&compiled, b.id, 0.0) {
                Ok(s) => s,
                Err(e) => {
                    report.reason = format!("observation refused: {e:?}");
                    return (None, report);
                }
            };
            let dx = [x[0] - fraction * target_x[0], x[1] - fraction * target_x[1]];
            let dv = [v[0] - fraction * target_v[0], v[1] - fraction * target_v[1]];
            let rp = dx[0].hypot(dx[1]) / case.a;
            let rv = dv[0].hypot(dv[1]) / velocity_scale;
            if !rp.is_finite() || !rv.is_finite() {
                report.reason = "nonfinite shooting residual".into();
                return (None, report);
            }
            residual = residual.max(rp).max(rv);
            corrections.push((dx, dv));
        }
        report.residual = Some(residual);
        if residual <= RESIDUAL_TOLERANCE {
            report.reason =
                "converged by evolving genesis; returned compiled history is accepted trial".into();
            return (Some(compiled), report);
        }
        for (b, (dx, dv)) in ic.bodies.iter_mut().zip(corrections) {
            for axis in 0..2 {
                b.v[axis] -= dv[axis];
                b.x[axis] += -dx[axis] + elapsed * dv[axis];
            }
        }
    }
    report.reason =
        "frozen shooting trial budget exhausted; no state patched or tolerance widened".into();
    (None, report)
}

pub const NEWTON_INITIALIZER_VERSION: &str = "kepler-observation-newton-v1";
pub const NEWTON_MAX_UPDATES: usize = 8;
pub const NEWTON_MAX_EVALUATIONS: usize = 100;
const JACOBIAN_STEP: f64 = 1e-6;
const MIN_PIVOT: f64 = 1e-10;

fn velocity_scale(case: &Case) -> f64 {
    (crate::coupled_source_response::G * case.total_mass / case.a).sqrt()
}

fn normalized_genesis(ic: &InitialCondition, case: &Case) -> [f64; 8] {
    let mut y = [0.0; 8];
    for (i, body) in ic.bodies.iter().enumerate() {
        for axis in 0..2 {
            y[4 * i + axis] = body.x[axis] / case.a;
            y[4 * i + 2 + axis] = body.v[axis] / velocity_scale(case);
        }
    }
    y
}

fn genesis_from_normalized(y: [f64; 8], case: &Case) -> InitialCondition {
    let mut ic = case.initial_condition();
    for (i, body) in ic.bodies.iter_mut().enumerate() {
        for axis in 0..2 {
            body.x[axis] = y[4 * i + axis] * case.a;
            body.v[axis] = y[4 * i + 2 + axis] * velocity_scale(case);
        }
    }
    ic
}

fn residual_norm(values: &[f64; 8]) -> f64 {
    values
        .chunks_exact(2)
        .map(|v| v[0].hypot(v[1]))
        .fold(0.0, f64::max)
}

/// Each invocation is one complete compile evaluation, including Jacobian and
/// rejected line-search proposals. Failed API calls mark incomplete accounting.
fn evaluate_newton(
    y: [f64; 8],
    case: &Case,
    report: &mut InitializationReport,
) -> Result<(SourceResponse, [f64; 8]), String> {
    if report.trials >= NEWTON_MAX_EVALUATIONS {
        return Err("frozen total compile evaluation budget exhausted".into());
    }
    if !y.iter().all(|value| value.is_finite()) {
        return Err("nonfinite normalized genesis".into());
    }
    let ic = genesis_from_normalized(y, case);
    report.resolved_genesis = ic.clone();
    report.residual = None;
    report.trials += 1;
    let compiled = compile_source_response_opts(
        ic.clone(),
        vec![],
        case.horizon,
        (case.horizon - case.genesis) / 512.0,
        CompileOpts {
            store_pair_inverse: false,
        },
    )
    .map_err(|e| {
        report.complete_charge = false;
        format!("compile refused; failed-call partial charge unavailable: {e:?}")
    })?;
    report.total_compile_charge += compiled.charge.ledger_total();
    let (tx, tv) = kepler_relative(case, 0.0);
    let mut residual = [0.0; 8];
    for (i, body) in ic.bodies.iter().enumerate() {
        let fraction = if i == 0 {
            -ic.bodies[1].mu
        } else {
            ic.bodies[0].mu
        } / case.total_mass;
        let (x, v) = body_state_compiled(&compiled, body.id, 0.0)
            .map_err(|e| format!("observation refused: {e:?}"))?;
        for axis in 0..2 {
            residual[4 * i + axis] = (x[axis] - fraction * tx[axis]) / case.a;
            residual[4 * i + 2 + axis] = (v[axis] - fraction * tv[axis]) / velocity_scale(case);
        }
    }
    if !residual.iter().all(|r| r.is_finite()) {
        return Err("nonfinite Newton shooting residual".into());
    }
    report.residual = Some(residual_norm(&residual));
    Ok((compiled, residual))
}

/// Partial-pivot Gaussian elimination on the dimensionless shooting Jacobian.
fn solve_newton(mut matrix: [[f64; 8]; 8], mut rhs: [f64; 8]) -> Result<[f64; 8], String> {
    if !matrix
        .iter()
        .flatten()
        .chain(rhs.iter())
        .all(|x| x.is_finite())
    {
        return Err("nonfinite Newton linear system".into());
    }
    for col in 0..8 {
        let pivot = (col..8)
            .max_by(|&a, &b| matrix[a][col].abs().total_cmp(&matrix[b][col].abs()))
            .unwrap();
        if matrix[pivot][col].abs() < MIN_PIVOT {
            return Err("Newton Jacobian pivot below frozen minimum".into());
        }
        matrix.swap(col, pivot);
        rhs.swap(col, pivot);
        for row in col + 1..8 {
            let factor = matrix[row][col] / matrix[col][col];
            for j in col..8 {
                matrix[row][j] -= factor * matrix[col][j];
            }
            rhs[row] -= factor * rhs[col];
        }
    }
    let mut step = [0.0; 8];
    for row in (0..8).rev() {
        let tail: f64 = (row + 1..8).map(|j| matrix[row][j] * step[j]).sum();
        step[row] = (rhs[row] - tail) / matrix[row][row];
    }
    if !step.iter().all(|x| x.is_finite()) {
        return Err("nonfinite Newton correction".into());
    }
    Ok(step)
}

/// Distinct initializer version; does not replace fixed-point results or gates.
/// `trials` counts compile evaluations, not Newton iterations.
pub fn initialize_newton(case: &Case) -> (Option<SourceResponse>, InitializationReport) {
    let mut report = InitializationReport {
        version: NEWTON_INITIALIZER_VERSION.into(),
        trials: 0,
        residual: None,
        total_compile_charge: 0,
        complete_charge: true,
        resolved_genesis: case.initial_condition(),
        reason: String::new(),
    };
    let result = (|| -> Result<SourceResponse, String> {
        let mut y = normalized_genesis(&report.resolved_genesis, case);
        let (mut compiled, mut residual) = evaluate_newton(y, case, &mut report)?;
        for _ in 0..NEWTON_MAX_UPDATES {
            if residual_norm(&residual) <= RESIDUAL_TOLERANCE {
                return Ok(compiled);
            }
            let mut jacobian = [[0.0; 8]; 8];
            for column in 0..8 {
                let mut perturbed = y;
                perturbed[column] += JACOBIAN_STEP;
                let (_, perturbed_residual) = evaluate_newton(perturbed, case, &mut report)?;
                for row in 0..8 {
                    jacobian[row][column] =
                        (perturbed_residual[row] - residual[row]) / JACOBIAN_STEP;
                }
            }
            let delta = solve_newton(jacobian, residual.map(|v| -v))?;
            let previous_norm = residual_norm(&residual);
            let mut accepted = None;
            for alpha in [1.0, 0.5, 0.25, 0.125] {
                let proposal = std::array::from_fn(|i| y[i] + alpha * delta[i]);
                let (candidate, candidate_residual) = evaluate_newton(proposal, case, &mut report)?;
                if residual_norm(&candidate_residual) < previous_norm {
                    accepted = Some((proposal, candidate, candidate_residual));
                    break;
                }
            }
            let Some((next_y, next_compiled, next_residual)) = accepted else {
                return Err(
                    "all four frozen Newton line-search proposals failed to reduce residual".into(),
                );
            };
            y = next_y;
            compiled = next_compiled;
            residual = next_residual;
        }
        if residual_norm(&residual) <= RESIDUAL_TOLERANCE {
            Ok(compiled)
        } else {
            Err("frozen Newton update budget exhausted; tolerance unchanged".into())
        }
    })();
    match result {
        Ok(compiled) => {
            report.reason = "Newton converged by evolving genesis; accepted compiled history returned without state patch".into();
            (Some(compiled), report)
        }
        Err(reason) => {
            report.reason = reason;
            (None, report)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn assert_accepted_history(
        case: &Case,
        compiled: &SourceResponse,
        report: &InitializationReport,
    ) {
        assert_eq!(
            serde_json::to_value(&compiled.genesis).unwrap(),
            serde_json::to_value(&report.resolved_genesis).unwrap()
        );
        assert_eq!(compiled.genesis.genesis_t, case.genesis);
        let (target_x, target_v) = kepler_relative(case, 0.0);
        let primary = case.total_mass / (1.0 + case.mass_ratio);
        let secondary = case.total_mass - primary;
        for (id, fraction) in [
            (0, -secondary / case.total_mass),
            (1, primary / case.total_mass),
        ] {
            let (x, v) = body_state_compiled(compiled, id, 0.0).unwrap();
            let dx = (x[0] - fraction * target_x[0]).hypot(x[1] - fraction * target_x[1]) / case.a;
            let dv = (v[0] - fraction * target_v[0]).hypot(v[1] - fraction * target_v[1])
                / velocity_scale(case);
            assert!(dx.is_finite() && dv.is_finite());
            assert!(dx <= RESIDUAL_TOLERANCE && dv <= RESIDUAL_TOLERANCE);
        }
        assert!(
            report.complete_charge && report.total_compile_charge >= compiled.charge.ledger_total()
        );
    }

    #[test]
    fn shooting_returns_evolved_genesis_without_observation_patch() {
        let case = Case::from_seed(0);
        let (compiled, report) = initialize(&case);
        assert_accepted_history(&case, &compiled.expect("fixed-point control"), &report);
        let case = Case::from_seed(8);
        let (compiled, report) = initialize_newton(&case);
        assert!(report.trials <= NEWTON_MAX_EVALUATIONS);
        assert_accepted_history(&case, &compiled.expect("Newton eccentric case"), &report);
    }

    #[test]
    fn newton_linear_solve_pivots_and_refuses_singular_system() {
        let mut matrix = [[0.0; 8]; 8];
        for i in 0..8 {
            matrix[i][(i + 1) % 8] = 1.0;
        }
        let rhs = std::array::from_fn(|i| ((i + 1) % 8) as f64);
        let solved = solve_newton(matrix, rhs).unwrap();
        for i in 0..8 {
            assert!((solved[i] - i as f64).abs() < 1e-12);
        }
        assert!(solve_newton([[0.0; 8]; 8], [1.0; 8]).is_err());
    }
}
