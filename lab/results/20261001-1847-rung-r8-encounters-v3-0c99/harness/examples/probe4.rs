fn main() {
    let b = rung::load_belt("data/b-steady.bin");
    let rho = 1e-4_f64;
    let mut best: Vec<(f64, usize, usize)> = Vec::new();
    for i in 0..b.len().min(400) {
        for j in i + 1..b.len().min(400) {
            let ov = (b[i].rmax() - b[j].rmin()).min(b[j].rmax() - b[i].rmin());
            best.push((ov, i, j));
        }
    }
    best.sort_by(|x, y| y.0.total_cmp(&x.0));
    let (_, i, j) = best[2];
    println!("bad pair ({i},{j}): a=({:.6},{:.6}) e=({:.2e},{:.2e}) dn={:.3e}", b[i].a, b[j].a, b[i].e, b[j].e, b[i].n - b[j].n);
    // trace the first 3000 steps
    let t_end = 1e5 * std::f64::consts::TAU;
    let _ = t_end;
    let mut st = rung::TStats::default();
    let mut out = Vec::new();
    let h = std::time::Instant::now();
    let th = std::thread::spawn(move || {
        rung::truth_pair(&b[i], &b[j], rho, 2000.0 * std::f64::consts::TAU, &mut out, &mut st);
        println!("2000 orbits done: steps={} evals={} enc={}", st.steps, st.evals, out.len());
    });
    th.join().unwrap();
    println!("{:.2}s", h.elapsed().as_secs_f64());
}
