//! Separately versioned initializer experiment. Never overwrites frozen genesis.
use emergent_law_lab::{
    orbit_initialization::initialize_newton_refined, orbit_reference::measure_indexed,
    two_body_bank::Case,
};
use std::io::Write;
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let a: Vec<_> = std::env::args().collect();
    if a.len() != 4 {
        return Err("expected seed new-initialization.json new-reference.json".into());
    }
    let case = Case::from_seed(a[1].parse()?);
    // Reserve paths before performing expensive work; never overwrite evidence.
    let mut init_file = std::fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(&a[2])?;
    let mut ref_file = std::fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(&a[3])?;
    let (compiled, init) = initialize_newton_refined(&case);
    init_file.write_all(serde_json::to_string_pretty(&init)?.as_bytes())?;
    if compiled.is_none() {
        return Err("refined initializer refused; report retained".into());
    }
    drop(compiled);
    let reference = measure_indexed(case, init.resolved_genesis, &[1048576, 2097152, 4194304])
        .map_err(|e| format!("reference refused: {e:?}"))?;
    ref_file.write_all(serde_json::to_string_pretty(&reference)?.as_bytes())?;
    Ok(())
}
