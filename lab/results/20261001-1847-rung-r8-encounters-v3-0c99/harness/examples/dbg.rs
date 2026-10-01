// debug: compare crate method vs my truth on the smoke pairs
fn main() {
    let dir = "data";
    let b = rung::load_belt(&format!("{dir}/a00.bin"));
    let rho = 2.7528056140595e-4_f64;
    let mut pairs = rung::radial_pairs(&b, rho);
    pairs.truncate(400);
    let t_end = 40.0;
    for &(i, j) in &pairs {
        let (meth, st) = rung::dioph_all(&b, &[(i, j)], rho, 0.0, t_end);
        let (truth, tst) = rung::truth_all(&b, &[(i, j)], rho, t_end);
        if !meth.is_empty() || !truth.is_empty() {
            println!("pair ({i},{j}) meth={:?}", meth.iter().map(|e| (e.2, e.3)).collect::<Vec<_>>());
            println!("           truth={:?}", truth.iter().map(|e| (e.2, e.3)).collect::<Vec<_>>());
            // dense scan around the method's time with my solver
            if let Some(m) = meth.first() {
                let t = m.2;
                let mut best = (t, f64::INFINITY);
                for q in -20000..20000 {
                    let tt = t + q as f64 * 1e-6;
                    let (r, _) = rung::mrel_pub(&b[i as usize], &b[j as usize], tt);
                    let d = (r[0]*r[0] + r[1]*r[1]).sqrt();
                    if d < best.1 { best = (tt, d); }
                }
                println!("           my dense scan min: t={:.9} d={:.6e} (rho={:.6e}) steps={} fine={}", best.0, best.1, rho, tst.steps, tst.fine);
                let (r, _) = rung::mrel_pub(&b[i as usize], &b[j as usize], t);
                println!("           my d at method t: {:.6e}", (r[0]*r[0]+r[1]*r[1]).sqrt());
            }
        }
    }
}
