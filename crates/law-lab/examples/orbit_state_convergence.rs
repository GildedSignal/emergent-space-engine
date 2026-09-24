//! Usage: orbit_state_convergence reference.json blocks.json output.json
use emergent_law_lab::orbit_reference::Sample;
use emergent_law_lab::orbit_state_convergence::{ReferenceRun, assess};
use std::io::Write;
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<_> = std::env::args().collect();
    if args.len() != 4 {
        return Err("expected reference.json blocks.json output.json".into());
    }
    let raw: serde_json::Value = serde_json::from_slice(&std::fs::read(&args[1])?)?;
    let blocks: serde_json::Value = serde_json::from_slice(&std::fs::read(&args[2])?)?;
    if blocks["version"] != "same-genesis-causal-block-refinement-v1"
        || raw["case"] != blocks["case"]
        || raw["genesis"] != blocks["genesis"]
    {
        return Err("reference and compiler must have identical case and genesis".into());
    }
    let reference: ReferenceRun = serde_json::from_value(raw)?;
    if blocks["reference_steps"].as_u64() != reference.rungs.last().map(|r| r.steps as u64) {
        return Err("compiler comparison names a different reference rung".into());
    }
    let rows = blocks["rows"].as_array().ok_or("missing compiler rows")?;
    let selected: Vec<_> = rows.iter().filter(|r| r["factor"] == 8).collect();
    if selected.len() != 1
        || selected[0]["status"] != "MEASURED"
        || selected[0]["complete_charge"] != true
    {
        return Err("expected one successful charged compiler subdivision8".into());
    }
    let samples: Vec<Sample> = serde_json::from_value(selected[0]["samples"].clone())?;
    let report = assess(&reference, &samples)?;
    let output = serde_json::json!({"audit":report,"compiler_charge":selected[0]["charge"],
        "compiler_state_queries":selected[0]["state_queries"],"production_law":null});
    let mut file = std::fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(&args[3])?;
    file.write_all(serde_json::to_string_pretty(&output)?.as_bytes())?;
    println!(
        "seed={} reference={:?} agreement={:?}",
        report.seed, report.reference_pass, report.agreement_pass
    );
    // A numerical FAIL is saved as evidence and also yields a failing process status.
    if !report.all_pass {
        std::process::exit(2);
    }
    Ok(())
}
