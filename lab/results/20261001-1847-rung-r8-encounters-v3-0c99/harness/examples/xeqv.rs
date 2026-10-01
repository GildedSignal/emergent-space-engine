fn main() {
    let b = rung::load_belt("data/adv-equalperiod.bin");
    let (rho, t_end) = (1e-3_f64, 100.0 * std::f64::consts::TAU);
    let mut rp = rung::radial_pairs(&b, rho);
    let mut xr = emergent_encounters::belt::Rng(424242);
    let mut samp: Vec<(u32, u32)> = (0..250).map(|_| rp[(xr.next_u64() as usize) % rp.len()]).collect();
    samp.sort_unstable(); samp.dedup();
    rp = samp;
    let meth_pairs: Vec<(u32, u32)> = rp.iter().filter(|&&(i, j)| emergent_encounters::pairs::is_candidate(&b[i as usize], &b[j as usize], rho)).copied().collect();
    let (meth, _) = rung::dioph_all(&b, &meth_pairs, rho, 0.0, t_end);
    let mut real = 0;
    for e in &meth {
        let mut bd = f64::INFINITY;
        for q in 0..=2000 {
            let t = e.2 - 0.05 + 0.1 * q as f64 / 2000.0;
            let (r, _) = rung::mrel_pub(&b[e.0 as usize], &b[e.1 as usize], t);
            bd = bd.min((r[0] * r[0] + r[1] * r[1]).sqrt());
        }
        if bd < rho { real += 1; } else { println!("UNREAL ({},{}) t={:.6} dmin={:.4e}", e.0, e.1, e.2, bd); }
    }
    println!("adv-equalperiod: {} of {} meth events dense-verified real", real, meth.len());
}
