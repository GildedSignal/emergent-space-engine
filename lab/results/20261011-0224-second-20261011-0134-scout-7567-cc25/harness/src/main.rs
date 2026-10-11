//! Driver: `harness <horizon_periods> <grid_n> <threads> [amplitude:variant ...]`
//! Writes composite-out.json. Defaults: 2000 (10×), grid 1600, 6 threads, leaks
//! 1e-8:v0 3e-8:v0 1e-7:v0 and the at-floor seed panel 4e-8:v0..v7.
mod behave;
mod composite;
mod gr_oracle;
mod measure;
pub type Result<T, E = Box<dyn std::error::Error>> = std::result::Result<T, E>;

fn main() {
    let mut args = std::env::args().skip(1);
    let horizon = args.next().and_then(|a| a.parse().ok()).unwrap_or(2000);
    let grid = args.next().and_then(|a| a.parse().ok()).unwrap_or(1600);
    let threads = args.next().and_then(|a| a.parse().ok()).unwrap_or(6);
    let mut leaks: Vec<composite::Leak> = [(1e-8, 0u64), (3e-8, 0), (1e-7, 0)]
        .into_iter()
        .chain((0..8u64).map(|v| (4e-8, v)))
        .collect();
    for a in args {
        if let Some((e, v)) = a.split_once(':') {
            if let (Ok(e), Ok(v)) = (e.parse::<f64>(), v.parse::<u64>()) {
                leaks.push((e, v));
            }
        }
    }
    eprintln!("horizon={horizon}p grid={grid} threads={threads} leaks={leaks:?}");
    let out = composite::main_run(horizon, grid, leaks, threads);
    std::fs::write("composite-out.json", serde_json::to_string_pretty(&out).unwrap()).unwrap();
    eprintln!("verdicts: {}", out["verdicts"]);
}
