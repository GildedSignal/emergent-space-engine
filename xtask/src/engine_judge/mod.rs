//! Independent judge of the dense frame and sparse kick hooks (Claude's implementation).
//! E1 order/thread/input equivalence; E2 one-period nonlinear behaviour; E3 anchored
//! ten-period behaviour/shape; E4 exact common-frame momentum and one-quantum energy;
//! E5 handoff mass ledger; E6 scratch planted defects; E7 public state contracts.
//! Frozen before running: see behaviour.rs constants and conservation.rs quantum.
mod api;
mod behaviour;
mod conservation;
mod drift;
mod scene;
use crate::measure::{machine_state, Watch};
use crate::Result;
use std::{
    path::PathBuf,
    process::Command,
    time::{Duration, Instant},
};

const LIMIT: Duration = Duration::from_secs(55);
fn gate(id: &str) -> (bool, String) {
    match id {
        "E1" => scene::determinism(),
        "E2" => behaviour::behaviour(false),
        "E3" => behaviour::behaviour(true),
        "E4" => conservation::conservation(),
        "E5" => conservation::ledger(),
        "E7" => api::api(),
        "E8" => drift::drift(),
        _ => unreachable!(),
    }
}
fn mutants(path: PathBuf) -> (bool, String) {
    let plans = [
        ("late", "E1"),
        ("coriolis", "E2"),
        ("drift", "E8"),
        ("rev", "E1"),
    ];
    let control = Command::new(&path)
        .args(["engine-judge", "--gates", "E1,E2,E8"])
        .env_remove("ENGINE_JUDGE_MUTANT")
        .output();
    let controls = control.is_ok_and(|o| {
        o.status.success()
            && String::from_utf8_lossy(&o.stdout)
                .lines()
                .filter(|l| {
                    l.starts_with("E1 PASS ")
                        || l.starts_with("E2 PASS ")
                        || l.starts_with("E8 PASS ")
                })
                .count()
                == 3
    });
    let mut caught = 0;
    let mut results = Vec::new();
    for (name, id) in plans {
        let run = Command::new(&path)
            .args(["engine-judge", "--gates", id])
            .env("ENGINE_JUDGE_MUTANT", name)
            .output();
        match run {
            Ok(o) => {
                let stdout = String::from_utf8_lossy(&o.stdout);
                let line = stdout
                    .lines()
                    .find(|l| l.starts_with(&format!("{id} ")))
                    .unwrap_or("missing_gate");
                let killed = !o.status.success() && line.starts_with(&format!("{id} FAIL "));
                // Timeout, panic, missing binary or error is NOT an observed gate kill.
                let killed = killed && !line.contains("timeout") && !line.contains("panic");
                caught += killed as usize;
                results.push(format!(
                    "{name}:{id}:{}",
                    if killed { "caught" } else { "SURVIVED" }
                ));
                // Full child gate lines are retained in the run evidence by the CLI user;
                // the ordinary summary remains one line per parent gate.
                let dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                    .join("../artifacts/runs/engine-judge");
                let _ = std::fs::create_dir_all(&dir);
                let _ = std::fs::write(
                    dir.join(format!("mutant-{name}.txt")),
                    format!("{}\n{}", stdout, String::from_utf8_lossy(&o.stderr)),
                );
            }
            Err(e) => results.push(format!("{name}:unavailable:{e}")),
        }
    }
    (
        caught == 4 && controls,
        format!(
            "caught={caught}/4 baseline_controls={controls} {}",
            results.join(" ")
        ),
    )
}
pub fn run(args: Vec<String>) -> Result<u8> {
    let mut only: Option<Vec<String>> = None;
    let mut binary = None;
    let mut prepare = false;
    let mut i = 0;
    while i < args.len() {
        match args[i].as_str() {
        "--gates"=>{i+=1;only=Some(args.get(i).ok_or("missing --gates value")?.split(',').map(str::to_string).collect());},
        "--mutant-binary"=>{i+=1;binary=Some(PathBuf::from(args.get(i).ok_or("missing --mutant-binary path")?));},
        "--prepare-mutants"=>prepare=true,
        _=>return Err("usage: engine-judge [--gates E1,E2,E3,E4,E5,E6,E7,E8] [--prepare-mutants] [--mutant-binary PATH]".into())
    }
        i += 1;
    }
    let ids = ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"];
    if only
        .as_ref()
        .is_some_and(|o| o.is_empty() || o.iter().any(|id| !ids.contains(&id.as_str())))
    {
        return Err("unknown/empty engine gate selection".into());
    }
    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("..");
    if prepare {
        let status = Command::new("python3")
            .arg(root.join("xtask/src/engine_judge/prepare_mutants.py"))
            .status()?;
        if !status.success() {
            return Err("scratch mutant preparation failed".into());
        }
    }
    let binary = binary.unwrap_or_else(|| root.join("artifacts/runs/engine-judge/mutant-xtask"));
    println!("machine_state {}", machine_state("start"));
    let uptime = Command::new("uptime")
        .output()
        .map(|o| String::from_utf8_lossy(&o.stdout).trim().to_owned())
        .unwrap_or_else(|e| format!("unavailable:{e}"));
    println!("machine_state uptime={uptime:?}");
    let watch = Watch::spawn(LIMIT, |id, secs| {
        println!("{id} FAIL timeout seconds={secs:.2} limit=55");
        std::process::exit(1);
    });
    let mut passed = true;
    for id in ids {
        if only.as_ref().is_some_and(|o| !o.iter().any(|x| x == id)) {
            continue;
        }
        watch.arm(id);
        let start = Instant::now();
        let (ok, detail) = if id == "E6" {
            mutants(binary.clone())
        } else {
            std::panic::catch_unwind(|| gate(id))
                .unwrap_or_else(|_| (false, "panic public_engine_contract".into()))
        };
        watch.disarm();
        passed &= ok;
        println!(
            "{id} {} {detail} seconds={:.3}",
            if ok { "PASS" } else { "FAIL" },
            start.elapsed().as_secs_f64()
        );
    }
    println!("machine_state {}", machine_state("end"));
    Ok(if passed { 0 } else { 1 })
}
