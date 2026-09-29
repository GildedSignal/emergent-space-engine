mod behave;
mod gas;
mod gas_rel;
mod gr_oracle;
mod history;
mod hybrid;
mod ladder;
mod lattice;
mod measure;
mod regions;
use serde_json::Value;
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
    if task == "gr-oracle" {
        // Independent weak/strong-field GR oracle (G = c = M = 1): two methods per quantity.
        let out_dir = args.next().map(PathBuf::from);
        if args.next().is_some() {
            return Err("usage: gr-oracle [out-dir]".into());
        }
        let (ok, rows) = gr_oracle::run();
        let mut jsonl = String::new();
        for r in rows.as_array().into_iter().flatten() {
            println!("{r}");
            jsonl.push_str(&format!("{r}\n"));
        }
        if let Some(dir) = out_dir {
            fs::create_dir_all(&dir)?;
            fs::write(dir.join("rows.jsonl"), jsonl)?;
        }
        println!("{}", if ok { "ORACLE AGREES" } else { "ORACLE DISAGREES" });
        return Ok(if ok { 0 } else { 1 });
    }
    if task == "behave" {
        // The behaviour judge: gates G1-G6, B7, B9, B10 against the GR oracle (xtask/src/behave/mod.rs).
        return behave::run(args.collect());
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
    if task == "ladder7-rung" {
        ladder::rung(args.collect())?;
        return Ok(0);
    }
    if task == "ladder7" {
        // Args: out-dir [track] [--full] [--modes=chronon,event,metal,regions]
        let rest: Vec<String> = args.collect();
        let out = PathBuf::from(rest.first().cloned().unwrap_or_else(|| "artifacts/runs/ladder7".into()));
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
        let value = ladder::run(&out, &modes, only.as_deref(), profile)?;
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
    if task == "test" {
        history::check()?;
        let out = PathBuf::from(args.next().unwrap_or_else(|| "artifacts/runs/latest".into()));
        fs::create_dir_all(&out)?;
        let tests = Command::new("cargo").args(["test", "--workspace", "--release", "--locked", "--offline"]).output()?;
        fs::write(out.join("test-output.txt"), [tests.stdout, tests.stderr].concat())?;
        if !tests.status.success() {
            return Err(format!("tests failed; see {}", out.join("test-output.txt").display()).into());
        }
        println!("PASS: history check and workspace tests ({})", out.join("test-output.txt").display());
        return Ok(0);
    }
    println!("Emergent Space tasks:\n  test [out-dir]                      history check + workspace tests\n  history [list | search TEXT | template | append FILE | check]\n  gr-oracle [out-dir]                 independent GR oracle\n  behave [--law echo|planted-*] [--gates G1,..,B10]  behaviour judge, gates G1-G6, B7, B9, B10\n  lattice-check [n:h ...]             chronon reference vs the independent gas reference\n  lattice-check-rel                   relativistic reference checks (v0, v1)\n  ladder7 OUT [track] [--full] [--modes=...]\n  ladder7-rung MODE TRACK RUNG PROFILE");
    Ok(0)
}
