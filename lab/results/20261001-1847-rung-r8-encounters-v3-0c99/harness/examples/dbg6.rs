fn main() {
    let b = rung::load_belt("data/adv-narrow.bin");
    let (i, j) = (86usize, 605usize);
    let rho = 1e-3_f64;
    let t_end = 100.0 * std::f64::consts::TAU;
    let (lo, hi) = (495.60f64, 495.70f64);
    let k = 20000usize;
    let mut prev_d = 0.0; let mut prev_g = 0.0;
    let mut dmin = (0.0, f64::INFINITY);
    for q in 0..=k {
        let t = lo + (hi - lo) * q as f64 / k as f64;
        let (r, v) = rung::mrel_pub(&b[i], &b[j], t);
        let d = (r[0]*r[0] + r[1]*r[1]).sqrt();
        let g = r[0]*v[0] + r[1]*v[1];
        if d < dmin.1 { dmin = (t, d); }
        if q > 0 {
            let dc = (prev_d < rho && d >= rho) || (prev_d >= rho && d < rho);
            let gc = (prev_g < 0.0 && g >= 0.0) || (prev_g >= 0.0 && g < 0.0);
            if dc || gc { println!("t={:.6} d={:.8e} g={:.3e} dc={} gc={}", t, d, g, dc, gc); }
        }
        prev_d = d; prev_g = g;
    }
    println!("dense min in window: t={:.6} d={:.8e} (rho={})", dmin.0, dmin.1, rho);
    let mut out = Vec::new();
    let mut ts = rung::TStats::default();
    rung::truth_pair(&b[i], &b[j], rho, t_end, &mut out, &mut ts);
    for e in &out { if (e.2 - 495.6).abs() < 0.2 { println!("truth: t={:.6} d={:.8e}", e.2, e.3); } }
    let (meth, st) = rung::dioph_all(&b, &[(i as u32, j as u32)], rho, 0.0, t_end);
    for e in &meth { if (e.2 - 495.6).abs() < 0.2 { println!("meth: t={:.6} d={:.8e} checks={} sections={:?}", e.2, e.3, st.checks_total(), st.sections); } }
}
