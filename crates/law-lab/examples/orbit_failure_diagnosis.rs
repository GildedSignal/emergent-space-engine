use emergent_law_lab::{
    orbit_newtonian_control,
    orbit_reference::{Sample, behavior},
    orbit_state_convergence::{ReferenceRun, assess, differences},
};
use std::io::Write;
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<_> = std::env::args().collect();
    if args.len() != 4 {
        return Err("expected reference.json retained-blocks.json new-output.json".into());
    }
    let raw: serde_json::Value = serde_json::from_slice(&std::fs::read(&args[1])?)?;
    let blocks: serde_json::Value = serde_json::from_slice(&std::fs::read(&args[2])?)?;
    if raw["case"] != blocks["case"]
        || raw["genesis"] != blocks["genesis"]
        || blocks["version"] != "same-genesis-causal-block-refinement-v1"
    {
        return Err("case/genesis/schema mismatch".into());
    }
    let reference: ReferenceRun = serde_json::from_value(raw)?;
    let selected: Vec<_> = blocks["rows"]
        .as_array()
        .ok_or("missing rows")?
        .iter()
        .filter(|r| r["factor"] == 8)
        .collect();
    if selected.len() != 1
        || selected[0]["status"] != "MEASURED"
        || selected[0]["complete_charge"] != true
    {
        return Err("expected successful charged subdivision8".into());
    }
    let candidate: Vec<Sample> = serde_json::from_value(selected[0]["samples"].clone())?;
    let state = assess(&reference, &candidate)?;
    let samples = &reference.rungs.last().ok_or("no rungs")?.samples;
    let coarse = orbit_newtonian_control::evolve(&reference.case, &samples[0], 4096)?;
    let fine = orbit_newtonian_control::evolve(&reference.case, &samples[0], 8192)?;
    let refinement = differences(&reference.case, &coarse, &fine)?;
    let control_resolved = refinement.position <= 1e-6
        && refinement.velocity <= 1e-6
        && refinement.energy <= 1e-6
        && refinement.angular_momentum <= 1e-6;
    let output = serde_json::json!({"version":"same-observed-state-newtonian-attribution-v1",
        "seed":reference.case.seed,"numerical_state_audit":state,
        "gem_behavior":behavior(&reference.case,reference.period,samples),
        "newtonian_control_behavior":behavior(&reference.case,reference.period,&fine),
        "control_refinement":refinement,"control_resolved":control_resolved,
        "gem_minus_same_state_newtonian":differences(&reference.case,samples,&fine)?,
        "initial_observed_state":samples[0],"newtonian_force_evaluations":4*(4096+8192),
        "control_pair_comparisons":2*1025,"compiler_charge":selected[0]["charge"],
        "compiler_original_reference_steps":blocks["reference_steps"],
        "current_reference_steps":reference.rungs.last().unwrap().steps,
        "scope":"Different-law Newtonian diagnostic begins at the identical observed t=0 state; no genesis reshooting. RK4 shares no GEM force/root routines. Not a replacement gravity law or GR reference. Retained compiler samples paired with the new reference explicitly.",
        "production_law":null});
    let mut f = std::fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(&args[3])?;
    f.write_all(serde_json::to_string_pretty(&output)?.as_bytes())?;
    println!(
        "seed={} numerical={} Newtonian={} GEM={}",
        reference.case.seed,
        state.all_pass,
        output["newtonian_control_behavior"]["pass"],
        output["gem_behavior"]["pass"]
    );
    if !state.all_pass || !control_resolved {
        std::process::exit(2);
    }
    Ok(())
}
