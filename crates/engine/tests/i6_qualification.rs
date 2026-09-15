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
        GateStatus::Pass
    );
    let moving = report
        .gates
        .iter()
        .find(|g| g.id == "moving-multi-mass-compact")
        .expect("moving gate");
    assert!(moving.evidence.contains("es-moving-schwarzschild-1pn-v0"));
    assert_eq!(status(&report, "sch-gem-accel-continuity-v0"), GateStatus::Fail);
    assert_eq!(status(&report, "family-moment-as-galaxy-skip"), GateStatus::Fail);
    assert_eq!(status(&report, "production-promotion"), GateStatus::Fail);
    assert_eq!(status(&report, "envelope-pressure"), GateStatus::Unsupported);
    assert_eq!(status(&report, "envelope-frozen-target"), GateStatus::Unsupported);
    assert_eq!(report.canonical_gravity_acceptance, "diagnostic-only");

    let bh = report
        .cards
        .iter()
        .find(|c| c.id == "black-hole-near-mass")
        .expect("bh card");
    assert_eq!(bh.status, GateStatus::Pass);
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
    assert!(report.held_out.len() >= 5);
    assert_eq!(report.daily_gallery.len(), 1);
    assert_eq!(report.envelope.len(), 4);
    assert!(
        report
            .held_out
            .iter()
            .any(|c| c.comparison.as_deref() == Some("compiler_exact"))
    );
    assert!(
        report
            .held_out
            .iter()
            .any(|c| c.comparison.as_deref() == Some("numerical_refinement"))
    );
    assert!(
        report
            .held_out
            .iter()
            .any(|c| c.comparison.as_deref() == Some("physical_law"))
    );
    assert!(
        report
            .held_out
            .iter()
            .all(|c| !c.evidence.contains("leftover==0"))
    );

    fn envelope<'a>(
        report: &'a emergent_engine::i6::I6Report,
        id: &str,
    ) -> &'a emergent_engine::i6::EnvelopeRung {
        report
            .envelope
            .iter()
            .find(|rung| rung.id == id)
            .unwrap_or_else(|| panic!("missing envelope rung {id}"))
    }
    let tiny = envelope(&report, "tiny-complete-loop");
    assert_eq!(tiny.status, GateStatus::Pass, "tiny {}", tiny.evidence);
    assert_eq!(tiny.identities, Some(4));
    assert_eq!(tiny.horizon_ticks, Some(80));
    assert!(tiny.digest.as_ref().is_some_and(|d| !d.is_empty()));
    assert!(tiny.wall_ns.is_some());
    assert_eq!(tiny.ledger_total, Some(0));
    assert!(!tiny.evidence.contains("leftover==0"));
    let connected_rung = envelope(&report, "connected-family-hierarchy");
    assert_eq!(
        connected_rung.status,
        GateStatus::Pass,
        "connected {}",
        connected_rung.evidence
    );
    assert_eq!(connected_rung.identities, Some(4));
    assert_eq!(connected_rung.families, Some(1));
    assert_eq!(connected_rung.family_members, Some(8));
    assert_eq!(connected_rung.horizon_ticks, Some(40));
    assert!(connected_rung.digest.as_ref().is_some_and(|d| !d.is_empty()));
    assert!(connected_rung.wall_ns.is_some());
    assert!(connected_rung.ledger_total.is_some_and(|n| n > 0));
    assert!(!connected_rung.evidence.contains("leftover==0"));
    let pressure = envelope(&report, "pressure-sweeps");
    assert_ne!(
        pressure.status,
        GateStatus::Unsupported,
        "pressure rung must be measured"
    );
    assert_eq!(pressure.identities, Some(64));
    assert_eq!(pressure.families, Some(10));
    assert_eq!(pressure.family_members, Some(48));
    assert_eq!(pressure.horizon_ticks, Some(80));
    assert!(pressure.digest.as_ref().is_some_and(|d| !d.is_empty()));
    assert!(pressure.wall_ns.is_some());
    assert!(pressure.ledger_total.is_some_and(|n| n > 0));
    assert!(pressure.limiting_resource.as_ref().is_some_and(|s| !s.is_empty()));
    assert!(pressure.evidence.contains("oracle="));
    assert!(!pressure.evidence.contains("leftover==0"));
    assert!(!pressure.evidence.contains("billion-identity hour"));
    assert_eq!(
        envelope(&report, "frozen-integrated-target").status,
        GateStatus::Unsupported
    );

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
        eprintln!("I6_CARD {} {:?} {}", c.id, c.status, c.evidence);
    }
    for rung in &report.envelope {
        eprintln!(
            "I6_ENVELOPE {} {:?} limiter={:?} rss_kb={:?} wall_ns={:?} ledger={:?} digest={:?}",
            rung.id,
            rung.status,
            rung.limiting_resource,
            rung.rss_kb,
            rung.wall_ns,
            rung.ledger_total,
            rung.digest.as_ref().map(|d| &d[..d.len().min(16)])
        );
    }

    let crossing = report
        .cards
        .iter()
        .find(|c| c.id == "coupled-fleet-hierarchy-inflight-ray-observer-boost")
        .expect("crossing");
    assert!(crossing.evidence.contains("hosted="));
    assert_eq!(
        crossing.status,
        GateStatus::Pass,
        "crossing evidence {}",
        crossing.evidence
    );
}
