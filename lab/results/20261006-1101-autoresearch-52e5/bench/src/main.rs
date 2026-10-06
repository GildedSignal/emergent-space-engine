//! Chronon CPU reference bench: ns per body-chronon, digest-checked.
//! Usage: chronon-bench N HORIZON FILL VMAX SEED RUNS [law]
//! law: "newton" (default) | "relv1"
use emergent_lattice::{chronon::Chronon, worlds, Law, Stepper};
use std::time::Instant;

fn main() {
    let a: Vec<String> = std::env::args().collect();
    let n: u64 = a[1].parse().unwrap();
    let horizon: i64 = a[2].parse().unwrap();
    let fill: f64 = a[3].parse().unwrap();
    let vmax: i64 = a[4].parse().unwrap();
    let seed: u64 = a[5].parse().unwrap();
    let runs: usize = a[6].parse().unwrap();
    let law = match a.get(7).map(|s| s.as_str()) {
        Some("relv1") => Law::RelativisticV1,
        _ => Law::Newtonian,
    };
    let q = 1024i64;

    let mut digests: Vec<String> = Vec::new();
    let mut ns: Vec<f64> = Vec::new();
    let mut metrics_json = serde_json::Value::Null;
    for r in 0..runs {
        let mut w = worlds::gas(n, fill, q, vmax, seed);
        if law != Law::Newtonian {
            w = w.with_law(law).expect("subluminal gas");
        }
        let mut c = Chronon::new(w, true).expect("gas world");
        let t = Instant::now();
        c.run_to(horizon);
        let el = t.elapsed().as_secs_f64();
        let world = c.world();
        digests.push(format!("{}|{}", world.digest(), c.log().digest()));
        if r == 0 {
            metrics_json = serde_json::to_value(c.metrics()).unwrap_or(serde_json::Value::Null);
        }
        ns.push(el * 1e9 / (n as f64 * horizon as f64));
    }
    ns.sort_by(|x, y| x.partial_cmp(y).unwrap());
    let same = digests.windows(2).all(|w| w[0] == w[1]);
    let out = serde_json::json!({
        "n": n, "horizon": horizon, "fill": fill, "vmax": vmax, "seed": seed, "law": format!("{:?}", law),
        "runs": runs,
        "ns_per_body_chronon_median": ns[ns.len() / 2],
        "ns_per_body_chronon_min": ns[0],
        "digest_stable_across_runs": same,
        "digest": digests[0],
        "metrics": metrics_json,
    });
    println!("{}", out.to_string());
}
