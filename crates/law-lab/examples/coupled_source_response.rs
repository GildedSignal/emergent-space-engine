//! Charged coupled-source-response measurements and a six-card scope drawing.
//! Not production gravity. Not Engine::advance.
use std::fs;
use std::path::PathBuf;

fn main() {
    match run() {
        Ok(()) => {}
        Err(err) => {
            eprintln!("{err}");
            std::process::exit(1);
        }
    }
}

fn run() -> Result<(), String> {
    let report = emergent_law_lab::coupled_source_response::run_charged_workload()
        .map_err(|e| e.to_string())?;
    assert!(report.production_law.is_none());
    let svg = emergent_law_lab::coupled_source_response::laboratory_scene_svg()
        .map_err(|e| e.to_string())?;
    let dir = PathBuf::from("artifacts/runs/distinct-histories-20260914");
    fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
    fs::write(dir.join("charged.json"), serde_json::to_string_pretty(&report).unwrap())
        .map_err(|e| e.to_string())?;
    fs::write(dir.join("scene.svg"), svg).map_err(|e| e.to_string())?;
    println!("{}", serde_json::to_string_pretty(&report).unwrap());
    println!("wrote {}/charged.json and scene.svg", dir.display());
    Ok(())
}
