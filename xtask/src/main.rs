mod bench;
mod gas;
mod gas_rel;
mod history;
mod hybrid;
mod ladder;
mod ladder5;
mod lattice;
mod proxy;
mod tick_scale;
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
    if task == "history" {
        history::run(args.collect())?;
        return Ok(0);
    }
    if task == "gas-endurance" {
        // Law experiment on the independent reference (not a ladder rung): energy drift of the
        // 64-ship gas as collisions accumulate. Args: bodies, horizons...
        let rest: Vec<i128> = args.filter_map(|a| a.parse().ok()).collect();
        let n = rest.first().copied().unwrap_or(64) as u64;
        for &h in rest.iter().skip(1) {
            let g = gas::world(n, 0.1, 1024, 256, 2_718_281_828);
            let t = std::time::Instant::now();
            let reference = gas::reference(&g, h);
            let e0: i128 = g.bodies.iter().map(|(_, v)| v[0] * v[0] + v[1] * v[1]).sum();
            let drift: i128 = reference.finals.iter().map(|f| f.2).sum();
            let max_res = reference.finals.iter().map(|f| f.2.abs()).max().unwrap_or(0);
            let contacts = reference.events.iter().filter(|e| e.1 == "contact").count();
            println!("bodies {n} ticks {h:>8} contacts {contacts:>9} energy drift {:+.3e} (relative) max residual {:.2e} energy units ({:.1} s)",
                drift as f64 / e0 as f64, max_res as f64 / (2.0 * 1024.0 * 1024.0), t.elapsed().as_secs_f64());
        }
        return Ok(0);
    }
    if task == "lattice-check" {
        // The lattice contract's CPU chronon reference against the independent gas reference.
        // Args: bodies:horizon pairs (default 64:1024 256:1024 64:8192).
        let rest: Vec<String> = args.collect();
        let cases: Vec<(u64, i64)> = if rest.is_empty() {
            vec![(64, 1024), (256, 1024), (64, 8192)]
        } else {
            rest.iter().filter_map(|a| a.split_once(':')).filter_map(|(n, h)| Some((n.parse().ok()?, h.parse().ok()?))).collect()
        };
        let mut ok = true;
        for (n, h) in cases {
            let v = lattice::check_gas(n, h, 2_718_281_828);
            let pass = v["same_genesis"] == true && v["events_equal"] == true && v["finals_equal"] == true && v["wall_momentum_equal"] == true;
            ok &= pass;
            println!("{} {}", if pass { "EQUAL" } else { "DIFFERENT" }, v);
        }
        return Ok(if ok { 0 } else { 1 });
    }
    if task == "tick-scale" {
        // The same physical gas at chronons 1..32 times longer. Args: bodies (default 16384).
        let n = args.next().and_then(|v| v.parse().ok()).unwrap_or(16384);
        tick_scale::run_all(n, &["chronon", "event", "metal"]);
        return Ok(0);
    }
    if task == "hevc-proxy" {
        // Args: out-dir [frames] [ticks-per-frame]
        let rest: Vec<String> = args.collect();
        let out = PathBuf::from(rest.first().cloned().unwrap_or_else(|| "artifacts/runs/hevc-proxy".into()));
        let frames = rest.get(1).and_then(|v| v.parse().ok()).unwrap_or(60);
        let tpf = rest.get(2).and_then(|v| v.parse().ok()).unwrap_or(4);
        proxy::run(&out, frames, tpf)?;
        return Ok(0);
    }
    if task == "lattice-check-rel" {
        // The relativistic chronon reference against the independent relativistic gas reference.
        // v0 and v1 on the same gases (Q = 1024), then v1 slow (0.004c at Q = 4096), where v0's
        // energy is blind and v1's is the Newtonian one.
        use emergent_lattice::Law::{Relativistic, RelativisticV1};
        let mut cases: Vec<(u64, i64, i64, i64, emergent_lattice::Law)> = Vec::new();
        for law in [Relativistic, RelativisticV1] {
            cases.extend([(64, 1024, 256, 1024, law), (256, 1024, 256, 1024, law), (64, 8192, 256, 1024, law), (64, 2048, 600, 1024, law)]);
        }
        cases.push((64, 16384, 16, 4096, RelativisticV1));
        let mut ok = true;
        for (n, h, v, q, law) in cases {
            let r = lattice::check_gas_relativistic(n, h, v, 2_718_281_828, q, law);
            let pass = r["events_equal"] == true && r["finals_equal"] == true && r["wall_momentum_equal"] == true;
            ok &= pass;
            println!("{} {}", if pass { "EQUAL" } else { "DIFFERENT" }, r);
        }
        return Ok(if ok { 0 } else { 1 });
    }
    if task == "ladder5-rung" || task == "ladder6-rung" || task == "ladder7-rung" {
        ladder5::set_version(task[6..7].parse().unwrap_or(5));
        ladder5::rung(args.collect())?;
        return Ok(0);
    }
    if task == "ladder5" || task == "ladder6" || task == "ladder7" {
        ladder5::set_version(task[6..7].parse().unwrap_or(5));
        // Args: out-dir [track] [--full] [--modes=chronon,event,metal,regions]
        let rest: Vec<String> = args.collect();
        let out = PathBuf::from(rest.first().cloned().unwrap_or_else(|| "artifacts/runs/ladder5".into()));
        fs::create_dir_all(&out)?;
        let profile = if rest.iter().any(|a| a == "--full") { "full" } else { "quick" };
        let modes: Vec<String> = rest
            .iter()
            .find_map(|a| a.strip_prefix("--modes="))
            .unwrap_or("chronon,event,metal,regions,hybrid")
            .split(',')
            .map(String::from)
            .collect();
        let only = rest.iter().skip(1).find(|a| !a.starts_with("--")).cloned();
        let value = ladder5::run(&out, &modes, only.as_deref(), profile)?;
        write(&out.join("ladder.json"), &value)?;
        for row in value["rows"].as_array().into_iter().flatten() {
            println!(
                "{:<8} {:<24} {:>9} {:<13} {:>8.0} ms  unit max {:>8.2} ms {:<6} ops/event {:>8.1} pred/op {:.2} cores {:.2}  {}",
                row["mode"].as_str().unwrap_or("?"),
                row["track"].as_str().unwrap_or("?"),
                row["size"].as_f64().unwrap_or(0.0),
                row["status"].as_str().unwrap_or("?"),
                row["advance_ms"].as_f64().unwrap_or(0.0),
                row["unit_ms_max"].as_f64().unwrap_or(0.0),
                row["smoothness"].as_str().unwrap_or(""),
                row["ops_per_event"].as_f64().unwrap_or(0.0),
                row["predicates_per_op"].as_f64().unwrap_or(0.0),
                row["cores_used"].as_f64().unwrap_or(0.0),
                row["limiter"].as_str().unwrap_or("")
            );
        }
        println!("gates {}", value["gates"]);
        println!("ladder wall time {:.1} s", value["ladder_seconds"].as_f64().unwrap_or(0.0));
        return Ok(0);
    }
    if task == "ladder-rung" {
        ladder::rung(args.collect())?;
        return Ok(0);
    }
    let out = PathBuf::from(
        args.next()
            .unwrap_or_else(|| "artifacts/runs/latest".into()),
    );
    if task == "verify" {
        println!("{}", emergent_engine::Engine::verify_checkpoint(out)?);
        return Ok(0);
    }
    if task == "ladder" {
        fs::create_dir_all(&out)?;
        let rest: Vec<String> = args.collect();
        let profile = if rest.iter().any(|a| a == "--full") { "full" } else { "quick" };
        let only = rest.iter().find(|a| !a.starts_with("--")).cloned();
        let value = ladder::run(&out, only.as_deref(), profile)?;
        write(&out.join("ladder.json"), &value)?;
        for row in value["rows"].as_array().into_iter().flatten() {
            let s = &row["smoothness"];
            println!(
                "{:<24} {:>9} {:<13} {:>8.0} ms  p99 {:>8.2} ms {:<6} cores {:.2}  {}",
                row["track"].as_str().unwrap_or("?"),
                row["size"].as_f64().unwrap_or(0.0),
                row["status"].as_str().unwrap_or("?"),
                row["advance_ms"].as_f64().unwrap_or(0.0),
                s["p99_ms"].as_f64().unwrap_or(0.0),
                s["verdict"].as_str().unwrap_or(""),
                row["cores_used"].as_f64().unwrap_or(0.0),
                row["limiter"].as_str().unwrap_or("")
            );
        }
        println!("ladder wall time {:.1} s", value["ladder_seconds"].as_f64().unwrap_or(0.0));
        return Ok(0);
    }
    if ![
        "test",
        "reference",
        "law-lab",
        "bench",
        "fermi",
        "qualify",
        "exception-setup-advance",
    ]
    .contains(&task.as_str())
    {
        println!("Emergent Space tasks: test | reference | law-lab | bench | fermi | qualify | exception-setup-advance [output-dir]\nverify CHECKPOINT\nhistory [list | search TEXT | template | append FILE | check]\nUse cargo run --release -p xtask -- qualify for measured evidence.\nQualification exits 2 when a research gate fails; the failure remains in the report.");
        return Ok(0);
    }
    fs::create_dir_all(&out)?;
    if task == "test" || task == "qualify" {
        history::check()?;
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
    if task == "exception-setup-advance" {
        write(&out.join("metrics.json"), &bench::exception_setup_advance()?)?;
        println!("Measured: 1,000-exception setup vs advance (historical 18.478/27.768 ms remain labels only)");
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
