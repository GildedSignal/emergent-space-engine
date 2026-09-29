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
    assert_eq!(gates(&lines).iter().map(|(_, v)| v.as_str()).collect::<Vec<_>>(), ["PASS"; 9]);
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

#[test]
fn each_new_planted_law_exits_1_and_fails_only_its_gate() {
    for (law, gate) in [("planted-clock", "B7"), ("planted-steps", "B9"), ("planted-quadratic", "B10")] {
        let (code, lines) = behave(&["--law", law]);
        assert_eq!(code, 1, "{lines:?}");
        let failed: Vec<String> = gates(&lines).into_iter().filter(|(_, v)| v == "FAIL").map(|(g, _)| g).collect();
        assert_eq!(failed, [gate], "{law}");
        assert_eq!(lines.last().unwrap(), &format!("behave {law}: FAIL {gate}"));
    }
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
