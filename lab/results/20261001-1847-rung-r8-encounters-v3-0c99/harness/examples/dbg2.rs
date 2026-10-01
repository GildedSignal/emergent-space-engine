fn main() {
    let dir = "data";
    for (name, rho, k, t_end) in [
        ("a13", 9.4585e-4, 3000, 100.0 * std::f64::consts::TAU),
        ("adv-equalperiod", 1e-3, 2500, 100.0 * std::f64::consts::TAU),
        ("adv-coorbital", 1e-3, 2500, 100.0 * std::f64::consts::TAU),
        ("adv-narrow", 1e-3, 2500, 100.0 * std::f64::consts::TAU),
    ] {
        let b = rung::load_belt(&format!("{dir}/{name}.bin"));
        let mut pairs = rung::radial_pairs(&b, rho);
        pairs.truncate(k);
        let t0 = std::time::Instant::now();
        let (truth, tst) = rung::truth_all(&b, &pairs, rho, t_end);
        let ts = t0.elapsed().as_secs_f64();
        let (meth, mst) = rung::dioph_all(&b, &pairs, rho, 0.0, t_end);
        let (missed, false_, n_t) = rung::matchup(&truth, &meth, t_end, 1e-3);
        println!("{name}: pairs={} truth={} meth={} missed={} false={} n_truth={} checks={} truth_s={:.1} steps={} fine={}",
            pairs.len(), truth.len(), meth.len(), missed, false_, n_t, mst.checks_total(), ts, tst.steps, tst.fine);
        for e in truth.iter().filter(|e| missed_in(e, &truth, &meth, t_end)) {}
        // print a few missed/false if any
        let inside = |t: f64| t > 0.05 && t < t_end - 0.05;
        use std::collections::HashMap;
        let mut byp: HashMap<(u32,u32), Vec<f64>> = HashMap::new();
        for e in &meth { byp.entry((e.0,e.1)).or_default().push(e.2); }
        for e in truth.iter().filter(|e| inside(e.2)) {
            if !byp.get(&(e.0,e.1)).map_or(false, |v| v.iter().any(|&t| (t-e.2).abs() < 1e-3)) {
                println!("  MISSED truth ({},{}) t={:.6} d={:.4e}", e.0, e.1, e.2, e.3);
            }
        }
        let mut tby: HashMap<(u32,u32), Vec<f64>> = HashMap::new();
        for e in &truth { tby.entry((e.0,e.1)).or_default().push(e.2); }
        for e in meth.iter().filter(|e| inside(e.2)) {
            if !tby.get(&(e.0,e.1)).map_or(false, |v| v.iter().any(|&t| (t-e.2).abs() < 1e-3)) {
                println!("  FALSE meth ({},{}) t={:.6} d={:.4e}", e.0, e.1, e.2, e.3);
            }
        }
    }
}
fn missed_in(_e: &(u32,u32,f64,f64), _t: &[(u32,u32,f64,f64)], _m: &[(u32,u32,f64,f64)], _te: f64) -> bool { false }
