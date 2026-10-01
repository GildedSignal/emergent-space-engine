fn main() {
    let b = rung::load_belt("data/adv-coorbital.bin");
    let (i, j) = (539usize, 581usize);
    let rho = 1e-3_f64;
    // dense scan over the whole horizon with my solver
    let t_end = 100.0 * std::f64::consts::TAU;
    let mut best = (0.0f64, f64::INFINITY);
    let mut mins: Vec<(f64, f64)> = Vec::new();
    let k = 3_000_000usize;
    let h = t_end / k as f64;
    let mut prev = f64::INFINITY;
    for q in 0..=k {
        let t = q as f64 * h;
        let (r, _) = rung::mrel_pub(&b[i], &b[j], t);
        let d = (r[0]*r[0] + r[1]*r[1]).sqrt();
        if d < best.1 { best = (t, d); }
        mins.push((t, d));
        let _ = prev; prev = d;
    }
    println!("global min: t={:.6} d={:.6e}", best.0, best.1);
    // local minima of the dense scan
    for w in 1..mins.len()-1 {
        if mins[w].1 <= mins[w-1].1 && mins[w].1 < mins[w+1].1 && mins[w].1 < 5e-3 {
            println!("  local min t={:.6} d={:.6e}", mins[w].0, mins[w].1);
        }
    }
    // what the crate method reports
    let (meth, st) = rung::dioph_all(&b, &[(i as u32, j as u32)], rho, 0.0, t_end);
    for e in &meth { println!("meth: t={:.6} d={:.6e}", e.2, e.3); }
    println!("checks={} sections={:?}", st.checks_total(), st.sections);
    // my truth
    let mut out = Vec::new();
    let mut ts = rung::TStats::default();
    rung::truth_pair(&b[i], &b[j], rho, t_end, &mut out, &mut ts);
    for e in &out { println!("truth: t={:.6} d={:.6e}", e.2, e.3); }
    println!("steps={} fine={}", ts.steps, ts.fine);
}
