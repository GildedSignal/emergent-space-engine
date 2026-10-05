//! End-to-end tests of `xtask behave`: exit codes and the shape of the output.
use std::process::Command;

fn behave(args: &[&str]) -> (i32, Vec<String>) {
    let out = Command::new(env!("CARGO_BIN_EXE_xtask")).arg("behave").args(args).output().expect("xtask runs");
    (out.status.code().unwrap_or(-1), String::from_utf8_lossy(&out.stdout).lines().map(String::from).collect())
}
/// The gate lines, `G<n>` or `B<n> PASS|FAIL ...`, as (id, verdict).
fn gates(lines: &[String]) -> Vec<(String, String)> {
    lines.iter().filter(|l| l.starts_with(['G', 'B']) && l[1..].starts_with(|c: char| c.is_ascii_digit())).map(|l| {
        let mut w = l.split(' ');
        (w.next().unwrap().to_string(), w.next().unwrap().to_string())
    }).collect()
}

#[test]
fn echo_passes_every_gate_between_two_machine_states() {
    let (code, lines) = behave(&["--law", "echo"]);
    assert_eq!(code, 0, "{lines:?}");
    assert_eq!(gates(&lines).iter().map(|(_, v)| v.as_str()).collect::<Vec<_>>(), ["PASS"; 16]);
    let states: Vec<usize> = (0..lines.len()).filter(|&i| lines[i].starts_with("machine_state {")).collect();
    assert_eq!((states.first(), states.last()), (Some(&0), Some(&(lines.len() - 2))), "{lines:?}");
    assert!(lines[0].contains("\"when\":\"start\"") && lines[lines.len() - 2].contains("\"when\":\"end\""));
    assert_eq!(lines.last().unwrap(), "behave echo: PASS");
}

#[test]
fn a_planted_law_exits_1_and_fails_only_its_gate() {
    let (code, lines) = behave(&["--law=planted-walk"]);
    assert_eq!(code, 1, "{lines:?}");
    let failed: Vec<String> = gates(&lines).into_iter().filter(|(_, v)| v == "FAIL").map(|(g, _)| g).collect();
    assert_eq!(failed, ["G5"]);
    assert_eq!(lines.last().unwrap(), "behave planted-walk: FAIL G5");
}

/// A planted law of the single-mass core fails only its gate. The nine core gates are named: the
/// default run is all sixteen (45 s or so, and B10 is a timing gate), and three of those at once
/// would make B10 flaky. `a_planted_law_exits_1_and_fails_only_its_gate` runs a planted law by default.
fn planted_fails_only(law: &str, gate: &str) {
    let core = ["G1", "G2", "G3", "G4", "G5", "G6", "B7", "B9", "B10"];
    let (code, lines) = behave(&["--law", law, "--gates", &core.join(",")]);
    assert_eq!(code, 1, "{lines:?}");
    let failed: Vec<String> = gates(&lines).into_iter().filter(|(_, v)| v == "FAIL").map(|(g, _)| g).collect();
    assert_eq!(failed, [gate], "{law}");
    assert_eq!(lines.last().unwrap(), &format!("behave {law} ({}): FAIL {gate}", core.join(" ")));
}

#[test]
fn planted_clock_exits_1_and_fails_only_b7() {
    planted_fails_only("planted-clock", "B7");
}

#[test]
fn planted_steps_exits_1_and_fails_only_b9() {
    planted_fails_only("planted-steps", "B9");
}

#[test]
fn planted_quadratic_exits_1_and_fails_only_b10() {
    planted_fails_only("planted-quadratic", "B10");
}

#[test]
fn gates_can_be_picked_and_only_those_run() {
    let (code, lines) = behave(&["--gates", "b10,B7"]);
    assert_eq!(code, 0, "{lines:?}");
    assert_eq!(gates(&lines).iter().map(|(g, v)| format!("{g} {v}")).collect::<Vec<_>>(), ["B7 PASS", "B10 PASS"]);
    assert_eq!(lines.last().unwrap(), "behave echo (B7 B10): PASS");
    // A picked gate that a law fails still exits 1; a gate the law does not fail passes even on a planted law.
    assert_eq!(behave(&["--law", "planted-clock", "--gates=B7"]).0, 1);
    assert_eq!(behave(&["--law", "planted-clock", "--gates=B9"]).0, 0);
}

#[test]
fn unknown_laws_and_arguments_are_refused() {
    for args in [&["--law", "newton"][..], &["--law"], &["--fast"], &["--gates", "B8"], &["--gates", "G7"], &["--gates"]] {
        let (code, lines) = behave(args);
        assert_ne!(code, 0);
        assert!(gates(&lines).is_empty(), "{lines:?}");
    }
}

/// The amendments' planted laws that plant their flaw in a cheap gate, through the CLI: the exit code and the last line say
/// which gate failed. planted-apsides and planted-average plant theirs in the slow gates (B14 and B17, seconds of four
/// threads each), which would tilt the timing gate B10 of the runs beside them: the unit tests in `behave::amendment_tests` judge them.
fn amended_fails_only(law: &str, gates_run: &str, gate: &str) {
    let (code, lines) = behave(&["--law", law, "--gates", gates_run]);
    assert_eq!(code, 1, "{law}: {lines:?}");
    let failed: Vec<String> = gates(&lines).into_iter().filter(|(_, v)| v == "FAIL").map(|(g, _)| g).collect();
    assert_eq!(failed, [gate], "{law}");
    assert_eq!(lines.last().unwrap(), &format!("behave {law} ({}): FAIL {gate}", gates_run.replace(',', " ")));
}

#[test]
fn the_cheap_planted_laws_of_the_amendments_exit_1_and_fail_only_their_gate() {
    for (law, gate) in [("planted-linear", "B9"), ("planted-static", "B16"), ("planted-flipped", "B16"), ("planted-fat", "B18")] {
        amended_fails_only(law, "B9,B16,B18", gate);
    }
}

/// The belt case of B18 is not frozen, so it runs only when named; the reference passes it and a planted belt fails only it.
/// Release only: the debug build is far slower than the gate's 60 s.
#[test]
#[cfg_attr(debug_assertions, ignore = "release only")]
fn the_belt_gate_runs_only_when_named_and_a_planted_belt_fails_only_it() {
    let (code, lines) = behave(&["--law", "echo", "--gates", "b18b"]);
    assert_eq!(code, 0, "{lines:?}");
    assert_eq!(gates(&lines), [("B18b".to_string(), "PASS".to_string())]);
    assert_eq!(lines.last().unwrap(), "behave echo (B18b): PASS");
    let (code, lines) = behave(&["--law", "planted-belt-fat", "--gates", "B18b"]);
    assert_eq!(code, 1, "{lines:?}");
    assert_eq!(gates(&lines), [("B18b".to_string(), "FAIL".to_string())]);
    assert_eq!(lines.last().unwrap(), "behave planted-belt-fat (B18b): FAIL B18b");
}
