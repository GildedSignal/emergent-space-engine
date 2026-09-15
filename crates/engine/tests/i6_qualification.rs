//! I6 same-model qualification matrix. Plan exit is the matrix run, not promotion.
//!
//! Behavior tests: independent inertial oracle, remainder bands that can become
//! a many-seed bank. Does not `assert_eq` leftover==0.0, freeze 1188/1675, or
//! pin 1.519…. Does not select `production_law`. Does not mint
//! `CANONICAL_GRAVITY_ACCEPTANCE`. Frozen 1dac658 / H0052 / H0054 / H0124
//! untouched.

use emergent_engine::{
    coupled_adapter::CANONICAL_GRAVITY_ACCEPTANCE,
    i6::{run_matrix, GateStatus},
    LAW_ID,
};

#[test]
fn i6_same_model_matrix_runs_without_promotion() {
    let report = run_matrix().expect("i6 matrix");
    assert_eq!(report.canonical_law, LAW_ID);
    assert_eq!(report.canonical_gravity_acceptance, CANONICAL_GRAVITY_ACCEPTANCE);
    assert!(report.production_law.is_none());
    assert!(!report.promotion);
    assert!(!report.full_engine);
    assert_eq!(report.plan_i6_exit, "matrix-run");
    assert_eq!(report.observatory.law, LAW_ID);
    assert_eq!(report.observatory.host, "EngineBridge");

    fn status(report: &emergent_engine::i6::I6Report, id: &str) -> GateStatus {
        report
            .gates
            .iter()
            .find(|g| g.id == id)
            .unwrap_or_else(|| panic!("missing gate {id}"))
            .status
            .clone()
    }

    assert_eq!(status(&report, "observatory-same-engine"), GateStatus::Pass);
    assert_eq!(status(&report, "compiler-inertial-facts"), GateStatus::Pass);
    assert_eq!(status(&report, "persist-replay"), GateStatus::Pass);
    assert_eq!(status(&report, "cold-history-query"), GateStatus::Pass);
    assert_eq!(status(&report, "galaxy-quadrupole-skip"), GateStatus::Fail);
    assert_eq!(
        status(&report, "moving-multi-mass-compact"),
        GateStatus::Unsupported
    );
    let moving = report
        .gates
        .iter()
        .find(|g| g.id == "moving-multi-mass-compact")
        .expect("moving gate");
    assert!(moving.evidence.contains("Shopping stopped"));
    let crossing = report
        .cards
        .iter()
        .find(|c| c.id == "coupled-fleet-hierarchy-inflight-ray-observer-boost")
        .expect("crossing");
    assert_eq!(crossing.status, GateStatus::Fail);
    assert_eq!(status(&report, "sch-gem-accel-continuity-v0"), GateStatus::Fail);
    assert_eq!(status(&report, "family-moment-as-galaxy-skip"), GateStatus::Fail);
    assert_eq!(status(&report, "production-promotion"), GateStatus::Fail);
    assert_eq!(status(&report, "envelope-frozen-target"), GateStatus::Unsupported);
    assert_eq!(report.canonical_gravity_acceptance, "diagnostic-only");

    let bh = report
        .cards
        .iter()
        .find(|c| c.id == "black-hole-near-mass")
        .expect("bh card");
    assert_eq!(bh.status, GateStatus::Unsupported);
    assert!(bh.failing_input_visible);
    assert!(bh.unconfirmed_magnitudes_visible);

    let galaxy = report
        .cards
        .iter()
        .find(|c| c.id == "galaxy-like-population")
        .expect("galaxy card");
    assert!(galaxy.evidence.contains("quadrupole remainder"));
    assert!(galaxy.evidence.contains("FAIL as skip"));

    assert!(!report.held_out.is_empty());
    assert_eq!(report.daily_gallery.len(), 1);
    assert_eq!(report.envelope.len(), 4);

    let json = serde_json::to_string_pretty(&report).expect("json");
    assert!(json.contains("\"production_law\": null"));
    let dest = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../docs/laws/i6-qualification-matrix-20260915.json");
    std::fs::write(&dest, json).expect("write matrix");
    eprintln!(
        "I6_MATRIX path={} promotion=false full_engine=false production_law=null plan_exit={}",
        dest.display(),
        report.plan_i6_exit
    );
    for g in &report.gates {
        eprintln!("I6_GATE {} {:?}", g.id, g.status);
    }
    for c in &report.cards {
        eprintln!("I6_CARD {} {:?}", c.id, c.status);
    }
}
