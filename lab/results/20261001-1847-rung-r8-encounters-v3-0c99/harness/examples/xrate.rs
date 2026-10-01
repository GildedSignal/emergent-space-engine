// checker: b-steady truth encounter rate from a fresh 24-pair sample, NO budget, per-pair results.
fn main() {
    let b = rung::load_belt("data/b-steady.bin");
    let (n, rho, orbits) = (b.len(), 1e-4_f64, 1e5_f64);
    let rp = rung::radial_pairs(&b, rho);
    println!("n={n} radial={} cone={}", rp.len(), emergent_encounters::pairs::cone_pairs(&b, rho).pairs.len());
    let mut xr = emergent_encounters::belt::Rng(13579113);
    let mut samp: Vec<(u32, u32)> = Vec::new();
    while samp.len() < 24 {
        let p = rp[(xr.next_u64() as usize) % rp.len()];
        if !samp.contains(&p) { samp.push(p); }
    }
    let t_end = orbits * std::f64::consts::TAU;
    let t0 = std::time::Instant::now();
    let mut tot = 0usize;
    for (k, &(i, j)) in samp.iter().enumerate() {
        let t1 = std::time::Instant::now();
        let mut out = Vec::new();
        let mut st = rung::TStats::default();
        rung::truth_pair(&b[i as usize], &b[j as usize], rho, t_end, &mut out, &mut st);
        tot += out.len();
        println!("pair {k:2} ({i},{j}): {} enc, {} steps, {:.1}s [{} total, {:.0}s elapsed]", out.len(), st.steps, t1.elapsed().as_secs_f64(), tot, t0.elapsed().as_secs_f64());
    }
    let rate = tot as f64 / 24.0 * rp.len() as f64 / (n as f64 * orbits);
    println!("FAIR truth rate over 24 complete pairs: {:.6e}/body/orbit ({} encounters)", rate, tot);
}
