fn main() {
    let b = rung::load_belt("data/a13.bin");
    let (i, j) = (28usize, 891usize);
    let rho = 9.4585e-4_f64;
    let t_end = 100.0 * std::f64::consts::TAU;
    // dense scan around 292.3-292.5
    let (lo, hi) = (292.30f64, 292.45f64);
    let k = 30000usize;
    let mut prev_d = 0.0; let mut prev_g = 0.0;
    for q in 0..=k {
        let t = lo + (hi - lo) * q as f64 / k as f64;
        let (r, v) = rung::mrel_pub(&b[i], &b[j], t);
        let d = (r[0]*r[0] + r[1]*r[1]).sqrt();
        let g = r[0]*v[0] + r[1]*v[1];
        if q > 0 {
            let crossed = (prev_d < rho && d >= rho) || (prev_d >= rho && d < rho);
            let gcross = (prev_g < 0.0 && g >= 0.0) || (prev_g >= 0.0 && g < 0.0);
            if crossed || gcross {
                println!("t={:.6} d={:.6e} g={:.3e} d_cross={} g_cross={}", t, d, g, crossed, gcross);
            }
        }
        prev_d = d; prev_g = g;
    }
    let (mut out) = Vec::new();
    let mut ts = rung::TStats::default();
    rung::truth_pair(&b[i], &b[j], rho, t_end, &mut out, &mut ts);
    for e in &out { if (e.2 - 292.4).abs() < 0.2 { println!("truth: t={:.6} d={:.6e}", e.2, e.3); } }
    let (meth, _) = rung::dioph_all(&b, &[(i as u32, j as u32)], rho, 0.0, t_end);
    for e in &meth { if (e.2 - 292.4).abs() < 0.2 { println!("meth: t={:.6} d={:.6e}", e.2, e.3); } }
}
