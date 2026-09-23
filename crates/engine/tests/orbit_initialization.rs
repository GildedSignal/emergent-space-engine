//! Offline initial-state solve followed by the real WorkBudget-driven compiler.
//! Sources are diagnostic; this does not assert canonical gravitational events.
use emergent_engine::{coupled_adapter::connected_laboratory_engine, WorkBudget};
use emergent_law_lab::{
    coupled_source_response::{body_state_compiled, G},
    orbit_initialization::{initialize_newton, RESIDUAL_TOLERANCE},
    two_body_bank::{kepler_relative, Case},
};

#[test]
fn initialized_orbit_survives_budgeted_engine_compilation() {
    for seed in [0, 8, 10] {
        let case = Case::from_seed(seed);
        let (accepted, report) = initialize_newton(&case);
        let accepted = accepted.unwrap_or_else(|| panic!("seed={seed} {}", report.reason));
        assert!(report.residual.unwrap() <= RESIDUAL_TOLERANCE);
        assert_eq!(
            serde_json::to_value(&accepted.genesis).unwrap(),
            serde_json::to_value(&report.resolved_genesis).unwrap()
        );
        for budget in [1, 256] {
            let mut engine = connected_laboratory_engine().unwrap();
            engine
                .attach_coupled_laboratory(
                    report.resolved_genesis.clone(),
                    case.horizon,
                    (case.horizon - case.genesis) / 512.0,
                )
                .unwrap();
            let mut polls = 0;
            while !engine.coupled.as_ref().unwrap().is_ready() {
                engine.advance(0, WorkBudget::new(budget)).unwrap();
                polls += 1;
                assert!(
                    polls < 1_000_000,
                    "compiler did not complete seed={seed} budget={budget}"
                );
            }
            assert!(polls > 1);
            let compiled = engine.coupled.as_ref().unwrap().compiled.as_ref().unwrap();
            assert_eq!(
                compiled.interval_functions, accepted.interval_functions,
                "budget subdivision changed source response"
            );
            let (xa, va) = body_state_compiled(compiled, 0, 0.0).unwrap();
            let (xb, vb) = body_state_compiled(compiled, 1, 0.0).unwrap();
            let (tx, tv) = kepler_relative(&case, 0.0);
            let dx = (xb[0] - xa[0] - tx[0]).hypot(xb[1] - xa[1] - tx[1]) / case.a;
            let dv = (vb[0] - va[0] - tv[0]).hypot(vb[1] - va[1] - tv[1])
                / (G * case.total_mass / case.a).sqrt();
            // Initializer bounds each body; relative error is at most their sum.
            assert!(dx <= 2.0 * RESIDUAL_TOLERANCE && dv <= 2.0 * RESIDUAL_TOLERANCE);
            eprintln!("ENGINE_INITIALIZED seed={seed} budget={budget} polls={polls} dx={dx:e} dv={dv:e} initialization_compiles={}",report.trials);
        }
    }
}
