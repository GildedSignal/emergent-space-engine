mod bench;
use serde_json::{json, Value};
use std::{
    fs,
    path::{Path, PathBuf},
    process::{Command, ExitCode},
};
type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;
fn main() -> ExitCode {
    match run() {
        Ok(code) => ExitCode::from(code),
        Err(e) => {
            eprintln!("error: {e}");
            ExitCode::FAILURE
        }
    }
}
fn write(path: &Path, value: &Value) -> Result<()> {
    fs::write(path, serde_json::to_vec_pretty(value)?)?;
    Ok(())
}
fn run() -> Result<u8> {
    let mut args = std::env::args().skip(1);
    let task = args.next().unwrap_or_else(|| "help".into());
    let out = PathBuf::from(
        args.next()
            .unwrap_or_else(|| "artifacts/runs/latest".into()),
    );
    if task == "verify" {
        println!("{}", emergent_engine::Engine::verify_checkpoint(out)?);
        return Ok(0);
    }
    if !["test", "reference", "law-lab", "bench", "fermi", "qualify"].contains(&task.as_str()) {
        println!("Emergent Space tasks: test | reference | law-lab | bench | fermi | qualify [output-dir]\nverify CHECKPOINT\nUse cargo run --release -p xtask -- qualify for measured evidence.\nQualification exits 2 when a research gate fails; the failure remains in the report.");
        return Ok(0);
    }
    fs::create_dir_all(&out)?;
    if task == "test" || task == "qualify" {
        let tests = Command::new("cargo")
            .args(["test", "--workspace", "--locked", "--offline"])
            .output()?;
        fs::write(
            out.join("test-output.txt"),
            [tests.stdout, tests.stderr].concat(),
        )?;
        if !tests.status.success() {
            return Err("correctness tests failed; see test-output.txt".into());
        }
        println!("PASS: canonical and law-laboratory test suites");
    }
    if task == "reference" || task == "qualify" {
        write(&out.join("reference.json"), &bench::reference()?)?;
        println!("PASS: reception 14 → contact 43 → notification 71");
    }
    if task == "bench" || task == "qualify" {
        write(&out.join("benchmarks.json"), &bench::run(&out)?)?;
    }
    if task == "fermi" || task == "qualify" {
        write(&out.join("fermi-estimates.json"), &bench::fermi())?;
    }
    if task == "law-lab" || task == "qualify" {
        let law = emergent_law_lab::qualify();
        write(
            &out.join("law-qualification.json"),
            &serde_json::to_value(&law)?,
        )?;
        if task == "qualify" {
            write(
                &out.join("qualification.json"),
                &json!({"schema":1,"provenance":bench::provenance(),"release_qualified":false,"gates":[
                 {"id":"G0","status":"PASS","evidence":"workspace contracts, test runner and frozen manifests"},
                 {"id":"G1","status":"PASS","evidence":"test-output.txt and reference.json; exact inertial causal law only"},
                 {"id":"G2","status":law.status,"evidence":"law-qualification.json"},
                 {"id":"G3","status":"BLOCKED","reason":"no qualified causal gravity law"},
                 {"id":"G4","status":"PARTIAL","evidence":"indexed families and source moments; production FMM absent"},
                 {"id":"G5","status":"PARTIAL","evidence":"bounded responses, checkpoints/replay; arbitrary block elimination absent"},
                 {"id":"G6","status":"PARTIAL","evidence":"native observatory and causal sensors; production propulsion absent"},
                 {"id":"G7","status":"PARTIAL","evidence":"worker execution and wgpu rendering; parallel causal commit/GPU physics unqualified"},
                 {"id":"G8","status":"BLOCKED","reason":"inertial mechanisms measured; integrated gravitational workload unqualified"}
                ]}),
            )?;
        }
        println!(
            "G2 {}. Production gravity law: {}",
            law.status,
            law.production_law.as_deref().unwrap_or("none qualified")
        );
        if law.production_law.is_none() {
            println!("Evidence: {}", out.display());
            return Ok(2);
        }
    }
    println!("Evidence: {}", out.display());
    Ok(0)
}
