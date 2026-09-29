//! Tests of the gate harness. Each runs in well under 60 s. The built-in evaluators are the
//! proof that the harness can pass (echo) and fail (planted).
use super::eval::Replay;
use super::frozen::*;
use super::run::*;
use super::types::*;
use super::*;
use std::{
    path::Path,
    sync::{
        atomic::{AtomicBool, AtomicUsize, Ordering},
        OnceLock,
    },
    time::Duration,
};

fn fz() -> &'static Frozen {
    static F: OnceLock<Frozen> = OnceLock::new();
    F.get_or_init(|| Frozen::load(Path::new(DEFAULT_DIR), ALL_SETS).expect("frozen evidence loads"))
}
fn replay(name: &str) -> Replay {
    Replay::new(fz(), name).unwrap_or_else(|e| panic!("{name}: {e}"))
}
/// The context a run would have: the register's adjudications applied.
fn ctx() -> Ctx {
    Ctx { adjudicated: register().into_iter().map(|(e, _)| e).collect(), ..Ctx::quiet() }
}
fn literal() -> Ctx {
    Ctx::quiet()
}

// ---- parsers ----------------------------------------------------------------------------

#[test]
fn integers_and_decimals() {
    assert_eq!(parse_int("79228162514264337593543950335").unwrap(), (1i128 << 96) - 1);
    assert_eq!(parse_int("-1208925819614487527859418").unwrap(), -1208925819614487527859418);
    assert!(parse_int("12x").is_err());
    assert_eq!(int_of(&serde_json::json!("-7")).unwrap(), -7);
    assert_eq!(int_of(&serde_json::json!(25)).unwrap(), 25);
    assert_eq!(int_pair(&serde_json::json!(["3", "-4"])).unwrap(), [3, -4]);
    assert!(int_pair(&serde_json::json!(["3"])).is_err());
    // ceiling of a decimal string, without floats
    for (s, want) in [
        ("172.534452385", 173),
        ("172.000", 172),
        ("172", 172),
        ("-12.5", -12),
        ("-12", -12),
        ("0.000", 0),
        ("0.001", 1),
        ("-0.5", 0),
        ("238834950172.5344523858453695772993", 238834950173),
    ] {
        assert_eq!(ceil_decimal(s).unwrap(), want, "{s}");
    }
    assert!(ceil_decimal("1.2x").is_err());
}

#[test]
fn answers_parse() {
    use serde_json::json;
    let free = expect_of(&json!({"at": "Free", "x": ["-5", "7"], "T": "1"})).unwrap();
    assert_eq!(free, Expect::Known(At::Free([-5, 7])));
    assert_eq!(expect_of(&json!({"at": "Absorbed", "chronon": "9"})).unwrap(), Expect::Known(At::Absorbed { chronon: 9 }));
    assert_eq!(expect_of(&json!({"at": "OutOfRange", "chronon": "-9"})).unwrap(), Expect::Known(At::OutOfRange { chronon: -9 }));
    assert_eq!(expect_of(&json!({"at": "Before"})).unwrap(), Expect::Known(At::Before));
    assert!(matches!(expect_of(&json!({"at": "UNSETTLED", "why": "x"})).unwrap(), Expect::Unsettled(_)));
    assert!(expect_of(&json!({"x": [1, 2]})).is_err());
    assert_eq!(expect_of_r2(&json!([1, -2])).unwrap(), Expect::Known(At::Free([1, -2])));
    assert_eq!(expect_of_r2(&json!("A7")).unwrap(), Expect::Known(At::Absorbed { chronon: 7 }));
    assert_eq!(expect_of_r2(&json!("O12")).unwrap(), Expect::Known(At::OutOfRange { chronon: 12 }));
    assert!(matches!(expect_of_r2(&json!("UNSETTLED:why")).unwrap(), Expect::Unsettled(_)));
    // the JSON of an answer names the kind and the integers as strings
    assert_eq!(At::Free([1, 2]).to_json(), json!({"at": "Free", "x": ["1", "2"]}));
    assert_eq!(At::Absorbed { chronon: 3 }.to_json()["chronon"], "3");
}

#[test]
fn case_records_parse() {
    let line = r#"{"id":"R0-0000","rung":"R0","class":["T=T0"],"M":"819321666","Q":"2967","t0":"-576661854012586396","x":["-877837139003","1727073861284"],"k":["27","610"],"motion":"timelike","T":["-576661854012586396"],"note":1}"#;
    let c = case_of(&serde_json::from_str(line).unwrap()).unwrap();
    assert_eq!(
        (c.id.as_str(), c.m, c.q, c.t0, c.x, c.k, c.motion),
        ("R0-0000", 819321666, 2967, -576661854012586396, [-877837139003, 1727073861284], [27, 610], Motion::Timelike)
    );
    assert_eq!(c.times, vec![c.t0]);
    assert!(c.has_class("T=T0") && !c.has_class("bound"));
    assert_eq!(c.extra, serde_json::json!({"note": 1}));
    assert!(case_of(&serde_json::from_str(&line.replace("timelike", "spacelike")).unwrap()).is_err());
}

#[test]
fn statistics() {
    assert_eq!(median(&[1, 2, 9]), 2.0);
    assert_eq!(median(&[1, 2, 4, 9]), 3.0);
    assert!(median(&[]).is_nan());
    let v: Vec<u64> = (1..=100).collect();
    assert_eq!(percentile(&v, 99.0), 99.0);
    assert_eq!(percentile(&v, 100.0), 100.0);
    assert_eq!(percentile(&[5], 99.0), 5.0);
    assert_eq!(g22::rel(1.0 + 1e-10, 1.0), (1e-10f64 + 1.0 - 1.0).abs());
    assert_eq!(g22::rel(0.0, 0.0), 0.0);
    assert!(g22::rel(1e-30, 0.0).is_infinite());
    assert!(g22::rel(f64::NAN, 1.0).is_nan());
    assert_eq!(parse_gates("1,3,G2.5").unwrap(), [true, false, true, false, true]);
    assert!(parse_gates("6").is_err() && parse_gates("x").is_err());
}

#[test]
fn chunker_keeps_order_and_covers_everything() {
    let items: Vec<usize> = (0..5000).collect();
    let mut seen = Vec::new();
    let chunks = chunked(&Ctx::quiet(), "test", &items, |c| seen.extend_from_slice(c));
    assert_eq!(seen, items);
    assert_eq!(chunks.iter().map(|c| c.items).sum::<usize>(), items.len());
    assert!(chunks.len() > 1, "starts small, then grows");
    assert!(chunks[1].items > chunks[0].items);
}

#[test]
fn watchdog_fires_past_its_limit_and_stays_quiet_before() {
    let fired = std::sync::Arc::new(AtomicBool::new(false));
    let f2 = fired.clone();
    let w = Watch::spawn(Duration::from_millis(250), move |label, _| {
        assert!(label.starts_with("chunk"));
        f2.store(true, Ordering::SeqCst);
    });
    w.arm("chunk a");
    std::thread::sleep(Duration::from_millis(150));
    w.disarm();
    std::thread::sleep(Duration::from_millis(300));
    assert!(!fired.load(Ordering::SeqCst), "disarmed in time");
    w.arm("chunk b");
    w.detail("case X");
    std::thread::sleep(Duration::from_millis(600));
    assert!(fired.load(Ordering::SeqCst), "armed past the limit");
    w.disarm();
}

#[test]
fn machine_state_records_what_the_contract_asks() {
    let m = machine_state("test");
    for k in ["therm", "batt", "power_source", "swap", "loadavg", "time_utc", "hardware"] {
        assert!(m[k].as_str().is_some_and(|s| !s.is_empty()), "{k}: {m}");
    }
}

// ---- the frozen evidence ------------------------------------------------------------------

#[test]
fn frozen_evidence_is_intact_and_complete() {
    assert!(verify_hashes(Path::new(DEFAULT_DIR)).unwrap().contains("verified"));
    let counts = |n: &str| (fz().set(n).len(), fz().set(n).iter().map(|j| j.answers.len()).sum::<usize>());
    assert_eq!(counts("R0"), (600, 600));
    assert_eq!(counts("R1"), (560, 560));
    assert_eq!(counts("R2"), (22092, 176736));
    assert_eq!(counts("R3"), (1300, 1300));
    assert_eq!(counts("R4"), (1500, 1500));
    assert_eq!(counts("R5"), (22400, 22400));
    assert_eq!(counts("G22"), (510, 8160));
    assert_eq!(counts("G24"), (200, 716));
    assert_eq!(counts("G24edge"), (59, 136));
    assert_eq!(counts("FB"), (300, 300));
    let total: usize = ALL_SETS.iter().map(|n| counts(n).1).sum();
    assert_eq!(total, 212_408, "the queries the frozen provenance counts");
    let unsettled = ALL_SETS.iter().flat_map(|n| fz().set(n)).flat_map(|j| &j.answers).filter(|a| matches!(a.expect, Expect::Unsettled(_))).count();
    assert_eq!(unsettled, 0);
}

#[test]
fn a_changed_evidence_file_is_refused() {
    let dir = std::env::temp_dir().join(format!("gate-hash-test-{}", std::process::id()));
    std::fs::create_dir_all(&dir).unwrap();
    std::fs::write(dir.join("a.txt"), "hello\n").unwrap();
    let ok = std::process::Command::new("shasum").args(["-a", "256", "a.txt"]).current_dir(&dir).output().unwrap();
    std::fs::write(dir.join("SHA256SUMS"), &ok.stdout).unwrap();
    assert!(verify_hashes(&dir).is_ok());
    std::fs::write(dir.join("a.txt"), "hello!\n").unwrap();
    let e = verify_hashes(&dir).unwrap_err().to_string();
    assert!(e.contains("differs from SHA256SUMS") && e.contains("a.txt"), "{e}");
    std::fs::remove_dir_all(&dir).ok();
}

#[test]
fn r2_regenerates_from_its_spec() {
    let n = g21::r2_spec_check(fz());
    assert_eq!(n["spec_anchors"], 22092);
    assert_eq!(n["identical"], true, "{n}");
    assert_eq!(n["f64_decision_safe"], true, "{n}");
}

#[test]
fn g23_intermediates_are_distinct_in_domain_with_repeats() {
    for (t0, tf) in [(0i128, 100i128), (-500, 100_000), (7, 1 << 80), (-(1 << 90), -(1 << 90) + 12_345)] {
        let q = g23::intermediates(t0, tf, &mut g23::Rng::new(42));
        assert_eq!(q.len(), 100);
        let distinct: std::collections::BTreeSet<_> = q.iter().copied().collect();
        assert_eq!(distinct.len(), 80, "{t0}..{tf}");
        assert!(q.iter().all(|t| (t0..tf).contains(t)), "in the working domain, T_final excluded");
        assert_eq!(q, g23::intermediates(t0, tf, &mut g23::Rng::new(42)), "deterministic");
        assert!(q.windows(2).any(|w| w[0] > w[1]) && q.windows(2).any(|w| w[0] < w[1]), "not sorted");
    }
    let sel = g23::select(fz());
    assert_eq!(sel.len(), 1000);
    assert!(sel.iter().all(|(j, tf)| tf - j.case.t0 >= 100));
    assert_eq!(sel.iter().map(|(j, _)| j.case.id.as_str()).collect::<std::collections::BTreeSet<_>>().len(), 1000);
}

// ---- echo: the harness passes a perfect evaluator, every gate that needs no timing ----------------

fn rung_passes(rung: &str, cases: usize, queries: usize) {
    let echo = replay("echo");
    let r = g21::run_rung(&echo, fz(), &ctx(), rung);
    assert!(r.pass, "{rung}: {:?} {:?}", r.first, r.notes);
    assert_eq!((r.cases, r.queries, r.agree, r.disagree, r.unsettled, r.anchor_errors), (cases, queries, queries, 0, 0, 0), "{rung}");
    assert!(max_secs(&r.chunks) < 60.0);
}
#[test]
fn echo_passes_r0() {
    rung_passes("R0", 600, 600);
}
#[test]
fn echo_passes_r1() {
    rung_passes("R1", 560, 560);
}
#[test]
fn echo_passes_r2() {
    rung_passes("R2", 22092, 176736);
}
#[test]
fn echo_passes_r3() {
    rung_passes("R3", 1300, 1300);
}
#[test]
fn echo_passes_r4() {
    rung_passes("R4", 1500, 1500);
}
#[test]
fn echo_passes_r5_with_the_fallback_cases() {
    rung_passes("R5", 22400 + 200 + 59, 22400 + 716 + 136);
    let echo = replay("echo");
    let fb = g21::run_fallback(&echo, fz(), &ctx());
    assert_eq!(fb["pass"], true, "{fb}");
    // 146 circular cases can straddle a boundary at 64 bits; two of them (FB-0016, FB-0098) are not eligible.
    assert_eq!((fb["eligible"].clone(), fb["may_force_midpoint_at_64"].clone()), (298.into(), 144.into()), "{fb}");
    assert_eq!(fb["skipped_ineligible"], serde_json::json!(["FB-0016", "FB-0098"]));
}

#[test]
fn echo_passes_g22_literally() {
    // The oracle's period quadrature now converges (H0193), so no adjudication is needed:
    // at G22-0047 (e = 0.99996) its fixed 16x32 rule had been 1.79e-5 off the judge.
    let r = g22::run(&replay("echo"), fz(), &literal());
    assert!(r.pass, "{}", r.to_json());
    assert_eq!(r.cases, 510);
    assert_eq!(r.tau_queries, 8138);
    assert_eq!(r.tau_skipped_no_reference, 22, "the OutOfRange queries carry no judge tau");
    for (name, n) in [
        ("periapsis_advance", 415),
        ("radial_period_T", 415),
        ("radial_period_tau", 415),
        ("light_deflection", 95),
        ("shapiro_delay", 95),
        ("static_clock", 510),
        ("circular_clock", 510),
        ("proper_time", 510),
        ("absorbed_clock", 418),
    ] {
        assert_eq!(r.checks[name].n, n, "{name}");
        assert_eq!(r.checks[name].fail, 0, "{name}");
    }
}

#[test]
fn echo_passes_g23_with_a_pure_memo() {
    let r = g23::run(&replay("echo"), fz(), &ctx());
    assert!(r.pass, "{}", r.to_json());
    assert_eq!((r.cases, r.failed, r.domain_violations, r.repeat_inconsistent), (1000, 0, 0, 0));
}

#[test]
fn echo_passes_g24() {
    let r = g24::run(&replay("echo"), fz(), &ctx());
    assert!(r.pass, "{}", r.to_json());
    assert_eq!((r.cases, r.infall, r.absorbed_side, r.escape_side, r.edge), (259, 80, 60 + 14 + 15, 60 + 15 + 15, 59));
    assert_eq!(r.reference_inconsistent, 0, "the frozen files agree with the closed form and the band");
    assert!(r.absorbed_at_first_chronon >= 11, "the band-edge cases with no free query before absorption");
}

#[test]
fn g25_times_every_frozen_query_and_reports_the_state() {
    let r = g25::run(&replay("echo"), fz(), &ctx());
    assert_eq!(r.natural_ns.len(), 20_000);
    assert_eq!(r.all_calls, 212_408);
    assert_eq!(r.untimed_cases, 0);
    assert_eq!(r.by_class.len(), 5);
    assert!(r.timer_overhead_ns > 0.0 && r.timer_overhead_ns < 1000.0);
    assert!(r.machine_before["therm"].is_string() && r.machine_after["swap"].is_string());
    // The verdict is taken as measured. Only its shape is asserted here: echo is a table lookup.
    let j = r.to_json();
    assert!(j["G2.5a"]["median_us"].is_number() && j["G2.5b"]["max_us"].is_number());
}

#[test]
fn g25_fails_a_slow_evaluator_and_an_evaluator_that_refuses_cases() {
    // A body that spends 6 ms in position fails G2.5b (max <= 5 ms) and, spending 60 us per
    // call on natural anchors, fails G2.5a's median. It is exercised on a tiny frozen set.
    struct Slow(std::time::Duration);
    struct SlowBody(std::time::Duration);
    impl Body for SlowBody {
        fn position(&self, _t: i128) -> At {
            let s = std::time::Instant::now();
            while s.elapsed() < self.0 {}
            At::Before
        }
        fn orbit(&self) -> Orbit {
            Orbit::nothing()
        }
        fn proper_time(&self, _t: i128) -> f64 {
            0.0
        }
    }
    impl Evaluator for Slow {
        fn name(&self) -> String {
            "slow".into()
        }
        fn new_body(&self, _: Field, _: i128, _: Anchor, _: Motion) -> Built {
            Ok(Box::new(SlowBody(self.0)))
        }
    }
    let tiny = tiny_frozen(60);
    let slow = g25::run(&Slow(Duration::from_micros(6000)), &tiny, &ctx());
    assert!(!slow.pass_a && !slow.pass_b && slow.max_ns > 5_000_000, "{}", slow.to_json());
    let ok = g25::run(&Slow(Duration::from_micros(2)), &tiny, &ctx());
    assert!(ok.pass_a && ok.pass_b, "{}", ok.to_json());
    struct Refuses;
    impl Evaluator for Refuses {
        fn name(&self) -> String {
            "refuses".into()
        }
        fn new_body(&self, _: Field, _: i128, _: Anchor, _: Motion) -> Built {
            Err(AnchorError("no".into()))
        }
    }
    let r = g25::run(&Refuses, &tiny, &ctx());
    assert!(!r.pass() && r.untimed_cases > 0, "an evaluator cannot pass cost by refusing cases");
}

/// A small synthetic frozen set: `n` natural R5 cases with Free answers, in R5.
fn tiny_frozen(n: usize) -> Frozen {
    let js: Vec<Judged> = (0..n)
        .map(|i| Judged {
            case: Case {
                id: format!("S{i}"),
                class: vec!["bound".into()],
                m: 1,
                q: 25,
                t0: 0,
                x: [30, 40],
                k: [i as i128, 0],
                motion: Motion::Timelike,
                times: vec![5],
                extra: serde_json::Value::Null,
            },
            answers: vec![Answer { t: 5, expect: Expect::Known(At::Free([1, 2])), tau: None, dist: [None, None] }],
            diag: None,
        })
        .collect();
    Frozen::synthetic("R5", js)
}

// ---- planted: the harness fails a wrong evaluator, at the right place --------------------------------

#[test]
fn planted_floor_stops_the_climb_at_r3_with_exactly_one_disagreement() {
    let p = replay("planted");
    let (id, t) = p.planted_target.clone().unwrap();
    assert!(id.starts_with("R3-"), "the first rung with a three-root case is R3: {id}");
    let rep = g21::climb(&p, fz(), &ctx(), 5);
    assert_eq!(rep.failed_at.as_deref(), Some("R3"));
    assert!(!rep.pass() && !rep.complete);
    assert_eq!(
        rep.rungs.iter().map(|r| (r.rung.as_str(), r.pass)).collect::<Vec<_>>(),
        [("R0", true), ("R1", true), ("R2", true), ("R3", false)],
        "R4 and R5 are not run"
    );
    let r3 = &rep.rungs[3];
    assert_eq!((r3.queries, r3.agree, r3.disagree), (1300, 1299, 1));
    let row = &r3.first[0];
    assert_eq!((row["id"].as_str().unwrap(), row["T"].as_str().unwrap().to_string()), (id.as_str(), t.to_string()));
    let (want, got) = (&row["expected"]["x"], &row["got"]["x"]);
    assert_eq!(got[1], want[1]);
    let d = parse_int(got[0].as_str().unwrap()).unwrap() - parse_int(want[0].as_str().unwrap()).unwrap();
    assert_eq!(d, 1, "one floor flipped by one");
}

#[test]
fn planted_radial_and_circular_fail_at_r1() {
    for chart in ["planted:radial", "planted:circular"] {
        let rep = g21::climb(&replay(chart), fz(), &ctx(), 5);
        assert_eq!(rep.failed_at.as_deref(), Some("R1"), "{chart}");
        assert_eq!(rep.rungs.len(), 2, "R2..R5 are not run");
        assert_eq!(rep.rungs[1].disagree, 1);
    }
}

#[test]
fn a_partial_climb_never_says_gates_pass() {
    let echo = replay("echo");
    let sel = Selection { upto: 1, gates: [true, false, false, false, false] };
    let out = execute(&echo, fz(), &ctx(), &sel);
    assert!(out.g21.as_ref().unwrap().pass() && !out.failed() && !out.complete());
    assert!(out.label().starts_with("PARTIAL PASS"));
    assert_eq!(out.g21.as_ref().unwrap().rungs.len(), 2);
    let planted = execute(&replay("planted"), fz(), &ctx(), &Selection { upto: 5, gates: [true, false, false, false, false] });
    assert_eq!(planted.label(), "GATES FAIL");
}

#[test]
fn planted_clock_fails_g22_and_only_g22() {
    let p = replay("planted-g22");
    assert!(g21::climb(&p, fz(), &ctx(), 5).pass(), "positions are untouched");
    let r = g22::run(&p, fz(), &ctx());
    assert!(!r.pass);
    assert_eq!((r.checks["proper_time"].fail, r.checks["absorbed_clock"].fail), (415, 418), "every timelike case, every absorbed query; light has tau = 0");
    assert_eq!(r.checks["periapsis_advance"].fail, 0);
    assert!(g23::run(&p, fz(), &ctx()).pass && g24::run(&p, fz(), &ctx()).pass);
}

#[test]
fn planted_cache_fails_g23_and_only_g23() {
    let p = replay("planted-g23");
    // A direct query is right; the corruption needs 10 distinct earlier queries, which G2.1 never makes.
    assert!(g21::climb(&p, fz(), &ctx(), 5).pass());
    assert!(g22::run(&p, fz(), &ctx()).pass && g24::run(&p, fz(), &ctx()).pass);
    let r = g23::run(&p, fz(), &ctx());
    assert!(!r.pass);
    assert_eq!(r.failed, 1000);
}

#[test]
fn planted_absorption_off_by_one_fails_g24_and_r1() {
    let p = replay("planted-g24");
    let r = g24::run(&p, fz(), &ctx());
    assert!(!r.pass && r.failed_cases > 0 && r.reference_inconsistent == 0);
    let rep = g21::climb(&p, fz(), &ctx(), 5);
    assert_eq!(rep.failed_at.as_deref(), Some("R1"), "R1 holds the first absorbed answers");
    assert!(g23::run(&p, fz(), &ctx()).pass);
}

#[test]
fn planted_range_exit_off_by_one_fails_at_r1_and_g24() {
    let p = replay("planted-range");
    let rep = g21::climb(&p, fz(), &ctx(), 5);
    assert_eq!(rep.failed_at.as_deref(), Some("R1"), "R1 holds the first OutOfRange answers");
    assert_eq!(rep.rungs[1].disagree, 2, "R1's two OutOfRange answers");
    assert!(!g24::run(&p, fz(), &ctx()).pass, "the G2.4 files hold OutOfRange answers too");
    assert!(g22::run(&p, fz(), &ctx()).pass && g23::run(&p, fz(), &ctx()).pass);
}

/// The straight line x0 + k0 (T - T0): no gravity at all.
struct Straight;
struct StraightBody(Anchor);
impl Body for StraightBody {
    fn position(&self, t: i128) -> At {
        let (a, dt) = (self.0, t - self.0.t);
        match dt {
            d if d < 0 => At::Before,
            0 => At::Free(a.x),
            d => At::Free([a.x[0] + a.k[0] * d, a.x[1] + a.k[1] * d]),
        }
    }
    fn orbit(&self) -> Orbit {
        Orbit::nothing()
    }
    fn proper_time(&self, _: i128) -> f64 {
        f64::NAN
    }
}
impl Evaluator for Straight {
    fn name(&self) -> String {
        "straight".into()
    }
    fn new_body(&self, _: Field, _: i128, a: Anchor, _: Motion) -> Built {
        Ok(Box::new(StraightBody(a)))
    }
}

#[test]
fn a_straight_line_passes_the_control_rung_r0_and_fails_r1() {
    let rep = g21::climb(&Straight, fz(), &ctx(), 5);
    assert_eq!(rep.failed_at.as_deref(), Some("R1"), "R0 is a control (the contract says so); R1 has real gravity");
    assert!(rep.rungs[0].pass, "{:?}", rep.rungs[0].first);
    assert_eq!(rep.rungs.len(), 2);
    assert!(rep.rungs[1].disagree > 300, "{}", rep.rungs[1].disagree);
}

// ---- other ways an evaluator can fail -----------------------------------------------------------------

/// Echo with one deliberate defect.
#[derive(Clone, Copy)]
enum Defect {
    NoHook,
    NoDiagnostics,
    AlwaysFree,
    FbOffByTwo,
    FbFlaky,
}
struct Broken<'a>(&'a Replay, Defect, AtomicUsize);
struct BrokenBody(Box<dyn Body>, Defect);
impl Evaluator for Broken<'_> {
    fn name(&self) -> String {
        "broken".into()
    }
    fn new_body(&self, f: Field, q: i128, a: Anchor, m: Motion) -> Built {
        Ok(Box::new(BrokenBody(self.0.new_body(f, q, a, m)?, self.1)))
    }
    fn new_body_reduced(&self, f: Field, q: i128, a: Anchor, m: Motion, s: &[u32]) -> Option<Built> {
        match self.1 {
            Defect::NoHook => None,
            Defect::FbOffByTwo => Some(self.0.new_body(f, q, a, m).map(|b| Box::new(BrokenBody(b, Defect::FbOffByTwo)) as Box<dyn Body>)),
            Defect::FbFlaky => {
                let n = self.2.fetch_add(1, Ordering::SeqCst);
                Some(
                    self.0
                        .new_body(f, q, a, m)
                        .map(|b| Box::new(BrokenBody(b, if n.is_multiple_of(5) { Defect::FbOffByTwo } else { Defect::FbFlaky })) as Box<dyn Body>),
                )
            }
            _ => self.0.new_body_reduced(f, q, a, m, s),
        }
    }
}
impl Body for BrokenBody {
    fn position(&self, t: i128) -> At {
        match (self.1, self.0.position(t)) {
            (Defect::AlwaysFree, At::Absorbed { .. }) => At::Free([0, 0]),
            (Defect::FbOffByTwo, At::Free(x)) => At::Free([x[0] + 2, x[1]]),
            (_, at) => at,
        }
    }
    fn orbit(&self) -> Orbit {
        if matches!(self.1, Defect::NoDiagnostics) {
            Orbit::nothing()
        } else {
            self.0.orbit()
        }
    }
    fn proper_time(&self, t: i128) -> f64 {
        self.0.proper_time(t)
    }
    fn shapiro_delay(&self, r1: f64, r2: f64) -> Option<f64> {
        (!matches!(self.1, Defect::NoDiagnostics)).then(|| self.0.shapiro_delay(r1, r2)).flatten()
    }
}

#[test]
fn an_evaluator_without_the_reduced_schedule_hook_fails_the_fallback_cases() {
    let echo = replay("echo");
    let fb = g21::run_fallback(&Broken(&echo, Defect::NoHook, AtomicUsize::new(0)), fz(), &ctx());
    assert_eq!((fb["pass"].clone(), fb["hook_implemented"].clone()), (false.into(), false.into()), "{fb}");
    let r = g21::run_rung(&Broken(&echo, Defect::NoHook, AtomicUsize::new(0)), fz(), &ctx(), "R5");
    assert!(!r.pass && r.disagree == 0, "R5's own cases pass; the missing hook fails the rung");
}

#[test]
fn fallback_floors_outside_the_admissible_pair_or_unstable_between_runs_fail() {
    let echo = replay("echo");
    let bad = g21::run_fallback(&Broken(&echo, Defect::FbOffByTwo, AtomicUsize::new(0)), fz(), &ctx());
    assert_eq!(bad["pass"], false);
    assert!(bad["inadmissible"].as_u64().unwrap() > 250, "{bad}");
    let flaky = g21::run_fallback(&Broken(&echo, Defect::FbFlaky, AtomicUsize::new(0)), fz(), &ctx());
    assert_eq!(flaky["pass"], false);
    assert!(flaky["not_identical_across_runs_or_threads"].as_u64().unwrap() > 0, "{flaky}");
}

#[test]
fn diagnostics_the_evaluator_does_not_provide_fail_g22() {
    let echo = replay("echo");
    let r = g22::run(&Broken(&echo, Defect::NoDiagnostics, AtomicUsize::new(0)), fz(), &ctx());
    assert!(!r.pass);
    for name in ["periapsis_advance", "radial_period_T", "radial_period_tau", "light_deflection", "shapiro_delay", "static_clock", "circular_clock"] {
        assert_eq!(r.checks[name].fail, r.checks[name].n, "{name}: missing counts as failing");
        assert_eq!(r.checks[name].missing, r.checks[name].n, "{name}");
    }
}

#[test]
fn an_evaluator_that_never_absorbs_fails_g24() {
    let echo = replay("echo");
    let r = g24::run(&Broken(&echo, Defect::AlwaysFree, AtomicUsize::new(0)), fz(), &ctx());
    assert!(!r.pass);
    assert!(r.failed_cases >= 60 + 14 + 40 + 40 - 1, "{}", r.to_json());
}

#[test]
fn an_unsettled_expected_answer_counts_as_a_failure() {
    let mut js = tiny_frozen(3).set("R5").to_vec();
    js[1].answers[0].expect = Expect::Unsettled("undecided at 2048 bits".into());
    let fz = Frozen::synthetic("R0", js);
    // An evaluator that says Free([1, 2]) agrees on two queries and cannot agree with UNSETTLED.
    struct Says;
    struct SaysBody;
    impl Body for SaysBody {
        fn position(&self, _: i128) -> At {
            At::Free([1, 2])
        }
        fn orbit(&self) -> Orbit {
            Orbit::nothing()
        }
        fn proper_time(&self, _: i128) -> f64 {
            0.0
        }
    }
    impl Evaluator for Says {
        fn name(&self) -> String {
            "says".into()
        }
        fn new_body(&self, _: Field, _: i128, _: Anchor, _: Motion) -> Built {
            Ok(Box::new(SaysBody))
        }
    }
    let r = g21::run_rung(&Says, &fz, &ctx(), "R0");
    assert_eq!((r.queries, r.agree, r.disagree, r.unsettled, r.pass), (3, 2, 1, 1, false));
    assert_eq!(r.first[0]["expected"]["at"], "UNSETTLED");
}

#[test]
fn a_refused_valid_anchor_is_a_disagreement_on_every_query_of_the_case() {
    let echo = replay("echo");
    let mut js = fz().set("R2")[..3].to_vec();
    js[0].case.q = 26; // an anchor the replay does not know, as a real evaluator refusing a valid one
    let fz = Frozen::synthetic("R2", js);
    let r = g21::run_rung(&echo, &fz, &ctx(), "R2");
    assert_eq!((r.anchor_errors, r.disagree, r.agree, r.pass), (1, 8, 16, false));
    assert!(r.first[0]["got"]["message"].as_str().unwrap().contains("not in the frozen files"));
}

#[test]
fn the_crate_adapter_is_a_stub_until_wired() {
    let a = adapter::CrateEvaluator;
    assert!(!a.wired());
    assert!(a.new_body(Field { m: 1 }, 25, Anchor { t: 0, x: [30, 40], k: [-3, -4] }, Motion::Timelike).is_err());
    assert!(a.new_body_reduced(Field { m: 1 }, 25, Anchor { t: 0, x: [30, 40], k: [-3, -4] }, Motion::Timelike, &[16, 32, 64]).is_none());
}

#[test]
fn the_register_names_only_real_gaps() {
    for (entry, reason) in register() {
        assert!(entry.starts_with("G22-") && !reason.is_empty(), "{entry}");
    }
}

#[test]
fn verdict_files_are_machine_readable() {
    let dir = std::env::temp_dir().join(format!("gate-verdict-test-{}", std::process::id()));
    std::fs::create_dir_all(&dir).unwrap();
    let rows = Rows::create(&dir.join("rows.jsonl")).unwrap();
    let ctx = Ctx { rows: rows.clone(), ..ctx() };
    let out = execute(&replay("planted"), fz(), &ctx, &Selection { upto: 5, gates: [true, false, true, true, false] });
    write_verdicts(&dir, &out, &serde_json::json!({"test": true})).unwrap();
    rows.flush();
    for f in ["G2.1.verdict.json", "G2.3.verdict.json", "G2.4.verdict.json", "verdict.json"] {
        let v: serde_json::Value = serde_json::from_str(&std::fs::read_to_string(dir.join(f)).unwrap()).unwrap();
        assert!(v["pass"].is_boolean() || f == "verdict.json", "{f}");
    }
    assert!(!dir.join("G2.2.verdict.json").exists(), "gates that did not run write no verdict");
    let v: serde_json::Value = serde_json::from_str(&std::fs::read_to_string(dir.join("verdict.json")).unwrap()).unwrap();
    assert_eq!((v["result"].as_str(), v["gates"]["G2.1"].clone(), v["gates"]["G2.2"].clone()), (Some("GATES FAIL"), false.into(), serde_json::Value::Null));
    let g21: serde_json::Value = serde_json::from_str(&std::fs::read_to_string(dir.join("G2.1.verdict.json")).unwrap()).unwrap();
    assert_eq!(g21["failed_at"], "R3");
    let kinds: Vec<String> = std::fs::read_to_string(dir.join("rows.jsonl"))
        .unwrap()
        .lines()
        .map(|l| serde_json::from_str::<serde_json::Value>(l).unwrap()["kind"].as_str().unwrap_or("summary").to_string())
        .collect();
    assert!(kinds.iter().any(|k| k == "disagreement") && kinds.iter().any(|k| k == "rung") && kinds.iter().any(|k| k == "chunk"));
    std::fs::remove_dir_all(&dir).ok();
}
