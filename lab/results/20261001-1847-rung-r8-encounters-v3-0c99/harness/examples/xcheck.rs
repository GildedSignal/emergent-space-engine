// checker: where do the "false" events live, and are they real encounters?
// For each belt: rebuild the author's PAIRSAMP=1500 sample, run the method on cone-filtered
// sampled pairs, run the timed truth with the author's 3 s budget, match, then classify every
// false event (on a skipped pair?) and dense-verify it independently (2001-point scan).
fn main() {
    let belts = [
        ("a13", 0.0009459812542956238_f64),
        ("adv-narrow", 1e-3_f64),
    ];
    for (name, rho) in belts {
        let b = rung::load_belt(&format!("data/{name}.bin"));
        let t_end = 100.0 * std::f64::consts::TAU;
        let mut rp = rung::radial_pairs(&b, rho);
        let full = rp.len();
        // the author's PAIRSAMP=1500 draw (main.rs lines 114-120)
        let mut xr = emergent_encounters::belt::Rng(424242);
        let mut samp: Vec<(u32, u32)> = (0..1500).map(|_| rp[(xr.next_u64() as usize) % rp.len()]).collect();
        samp.sort_unstable();
        samp.dedup();
        rp = samp;
        println!("{name}: full radial pairs = {full}, sampled = {}", rp.len());
        // method on cone-filtered sampled pairs (as casea does)
        let meth_pairs: Vec<(u32, u32)> = rp.iter().filter(|&&(i, j)| emergent_encounters::pairs::is_candidate(&b[i as usize], &b[j as usize], rho)).copied().collect();
        let (meth, mst) = rung::dioph_all(&b, &meth_pairs, rho, 0.0, t_end);
        // timed truth per pair, 3 s budget, skip set recorded
        let mut truth: Vec<rung::Enc> = Vec::new();
        let mut skipped: Vec<(u32, u32)> = Vec::new();
        for &(i, j) in &rp {
            if let Some((mut v, _)) = rung::timed_truth_pair(b[i as usize], b[j as usize], rho, t_end, 3.0) {
                for e in &mut v { e.0 = i; e.1 = j; }
                truth.append(&mut v);
            } else {
                skipped.push((i, j));
            }
        }
        let (missed, false_, n_t) = rung::matchup(&truth, &meth, t_end, 1e-3);
        println!("{name}: truth={} (skipped {} pairs), meth={} checks={}, missed={} false={} n_truth={}",
            truth.len(), skipped.len(), meth.len(), mst.checks_total(), missed, false_, n_t);
        // events on skipped pairs
        let mut on_skip = 0usize;
        let mut off_skip = 0usize;
        for e in &meth {
            if skipped.contains(&(e.0, e.1)) { on_skip += 1; } else { off_skip += 1; }
        }
        println!("{name}: meth events on skipped pairs = {on_skip}, on processed pairs = {off_skip}");
        // dense-verify every meth event: min distance in [t-0.05, t+0.05] over 2001 samples
        let mut real = 0usize;
        let mut unreal: Vec<(u32, u32, f64, f64)> = Vec::new();
        for e in &meth {
            let (mut bt, mut bd) = (e.2, f64::INFINITY);
            for q in 0..=2000 {
                let t = e.2 - 0.05 + 0.1 * q as f64 / 2000.0;
                let (r, _) = rung::mrel_pub(&b[e.0 as usize], &b[e.1 as usize], t);
                let d = (r[0] * r[0] + r[1] * r[1]).sqrt();
                if d < bd { bd = d; bt = t; }
            }
            if bd < rho { real += 1; } else { unreal.push((e.0, e.1, bt, bd)); }
        }
        println!("{name}: meth events dense-verified real (d<rho within +-0.05) = {real}/{}", meth.len());
        for (i, j, t, d) in unreal.iter().take(10) {
            println!("{name}:   UNREAL ({i},{j}) t={t:.6} dmin={d:.4e} rho={rho:.4e}");
        }
        // missed truth events (should be 0): print any
        use std::collections::HashMap;
        let mut byp: HashMap<(u32, u32), Vec<f64>> = HashMap::new();
        for e in &meth { byp.entry((e.0, e.1)).or_default().push(e.2); }
        let inside = |t: f64| t > 0.05 && t < t_end - 0.05;
        for e in truth.iter().filter(|e| inside(e.2)) {
            if !byp.get(&(e.0, e.1)).map_or(false, |v| v.iter().any(|&t| (t - e.2).abs() < 1e-3)) {
                println!("{name}:   MISSED truth ({},{}) t={:.6} d={:.4e}", e.0, e.1, e.2, e.3);
            }
        }
    }
}
