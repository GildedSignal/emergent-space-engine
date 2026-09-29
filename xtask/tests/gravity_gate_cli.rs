//! End-to-end tests of `xtask gravity-gate`: exit codes, the last stdout line, and the output
//! files. Each runs in a few seconds.
use std::{path::PathBuf, process::Command};

fn out_dir(name: &str) -> PathBuf {
    let d = std::env::temp_dir().join(format!("gravity-gate-cli-{name}-{}", std::process::id()));
    let _ = std::fs::remove_dir_all(&d);
    d
}
fn gate(dir: &PathBuf, args: &[&str]) -> (i32, String) {
    let out = Command::new(env!("CARGO_BIN_EXE_xtask")).arg("gravity-gate").arg(dir).args(args).output().expect("xtask runs");
    (out.status.code().unwrap_or(-1), String::from_utf8_lossy(&out.stdout).to_string())
}
fn last(text: &str) -> &str {
    text.lines().last().unwrap_or("")
}

#[test]
fn echo_ends_gates_pass_with_exit_0_and_writes_every_verdict() {
    let d = out_dir("echo");
    let (code, text) = gate(&d, &["--evaluator", "echo"]);
    assert_eq!((code, last(&text)), (0, "GATES PASS"), "{text}");
    for f in ["rows.jsonl", "G2.1.verdict.json", "G2.2.verdict.json", "G2.3.verdict.json", "G2.4.verdict.json", "G2.5.verdict.json", "verdict.json"] {
        assert!(d.join(f).exists(), "{f}");
    }
    let v: serde_json::Value = serde_json::from_str(&std::fs::read_to_string(d.join("verdict.json")).unwrap()).unwrap();
    assert_eq!(v["result"], "GATES PASS");
    let g25: serde_json::Value = serde_json::from_str(&std::fs::read_to_string(d.join("G2.5.verdict.json")).unwrap()).unwrap();
    assert!(g25["machine_before"]["therm"].is_string() && g25["machine_after"]["power_source"].is_string());
    std::fs::remove_dir_all(&d).ok();
}

#[test]
fn literal_echo_fails_on_the_oracle_gap_and_says_so() {
    let d = out_dir("literal");
    let (code, text) = gate(&d, &["--evaluator", "echo", "--literal", "--gates", "2"]);
    assert_eq!((code, last(&text)), (1, "GATES FAIL"), "{text}");
    assert!(text.contains("radial_period_T"), "{text}");
    std::fs::remove_dir_all(&d).ok();
}

#[test]
fn planted_ends_gates_fail_with_exit_1() {
    let d = out_dir("planted");
    let (code, text) = gate(&d, &["--evaluator", "planted"]);
    assert_eq!((code, last(&text)), (1, "GATES FAIL"), "{text}");
    assert!(text.contains("G2.1 FAIL at R3"), "{text}");
    let rows = std::fs::read_to_string(d.join("rows.jsonl")).unwrap();
    assert!(rows.lines().any(|l| l.contains("\"kind\":\"disagreement\"") && l.contains("R3-00000")));
    std::fs::remove_dir_all(&d).ok();
}

#[test]
fn a_partial_run_is_not_a_gate_verdict() {
    let d = out_dir("partial");
    let (code, text) = gate(&d, &["--evaluator", "echo", "--rung", "R2", "--gates", "1"]);
    assert_eq!(code, 0, "{text}");
    assert!(last(&text).starts_with("PARTIAL PASS"), "{text}");
    std::fs::remove_dir_all(&d).ok();
}

#[test]
fn the_unwired_crate_adapter_fails_at_once() {
    let d = out_dir("unwired");
    let (code, text) = gate(&d, &[]);
    assert_eq!((code, last(&text)), (1, "GATES FAIL"), "{text}");
    assert!(text.contains("not wired"), "{text}");
    std::fs::remove_dir_all(&d).ok();
}

#[test]
fn a_chunk_past_the_hard_limit_is_killed() {
    let d = out_dir("hang");
    let t = std::time::Instant::now();
    let (code, text) = gate(&d, &["--evaluator", "hang", "--hard-secs", "1", "--rung", "R0", "--gates", "1"]);
    assert_eq!((code, last(&text)), (1, "GATES FAIL"), "{text}");
    assert!(text.contains("past the 1 s limit") && text.contains("G2.1 R0"), "{text}");
    assert!(t.elapsed().as_secs() < 30);
    let v: serde_json::Value = serde_json::from_str(&std::fs::read_to_string(d.join("verdict.json")).unwrap()).unwrap();
    assert_eq!(v["result"], "GATES FAIL");
    assert!(std::fs::read_to_string(d.join("rows.jsonl")).unwrap().contains("\"kind\":\"timeout\""));
    std::fs::remove_dir_all(&d).ok();
}

#[test]
fn evidence_that_differs_from_the_frozen_hashes_fails_the_gate() {
    let (d, ev) = (out_dir("evidence"), out_dir("evidence-copy"));
    std::fs::create_dir_all(&ev).unwrap();
    let src = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../artifacts/evidence/g2-reference-20260928");
    for f in ["R0.cases.jsonl.gz", "R0.answers.jsonl.gz"] {
        std::fs::copy(src.join(f), ev.join(f)).unwrap();
    }
    // The hashes of just these two files, so that only the changed byte can fail the check.
    let sums = std::fs::read_to_string(src.join("SHA256SUMS")).unwrap();
    let kept: Vec<&str> = sums.lines().filter(|l| l.ends_with("R0.cases.jsonl.gz") || l.ends_with("R0.answers.jsonl.gz")).collect();
    assert_eq!(kept.len(), 2);
    std::fs::write(ev.join("SHA256SUMS"), kept.join("\n") + "\n").unwrap();
    // A changed byte in a frozen file: the hash check must refuse the run before any comparison.
    let mut bytes = std::fs::read(ev.join("R0.answers.jsonl.gz")).unwrap();
    let n = bytes.len() - 20;
    bytes[n] ^= 1;
    std::fs::write(ev.join("R0.answers.jsonl.gz"), bytes).unwrap();
    let (code, text) = gate(&d, &["--evaluator", "echo", "--evidence", ev.to_str().unwrap()]);
    assert_eq!((code, last(&text)), (1, "GATES FAIL"), "{text}");
    assert!(text.contains("differs from SHA256SUMS") && text.contains("R0.answers.jsonl.gz") && !text.contains("R0.cases"), "{text}");
    std::fs::remove_dir_all(&d).ok();
    std::fs::remove_dir_all(&ev).ok();
}

#[test]
fn bad_arguments_are_refused() {
    let d = out_dir("args");
    for args in [&["--rung", "R9"][..], &["--gates", "7"], &["--nonsense"], &["--evaluator", "nope"]] {
        let (code, _) = gate(&d, args);
        assert_ne!(code, 0, "{args:?}");
    }
    std::fs::remove_dir_all(&d).ok();
}
