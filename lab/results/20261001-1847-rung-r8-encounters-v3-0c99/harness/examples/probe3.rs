fn main() {
    let args: Vec<String> = std::env::args().collect();
    let (belt, rho, orbits): (&str, f64, f64) = match args.get(1).map(|s| s.as_str()) {
        Some("b") => ("b-steady", 1e-4, 1e5),
        Some("a13") => ("a13", 9.4585e-4, 100.0),
        _ => ("adv-coorbital", 1e-3, 100.0),
    };
    let b = rung::load_belt(&format!("data/{belt}.bin"));
    let t_end = orbits * std::f64::consts::TAU;
    // worst-case-ish pairs: closest radial overlap first
    let mut best: Vec<(f64, usize, usize)> = Vec::new();
    for i in 0..b.len().min(400) {
        for j in i + 1..b.len().min(400) {
            let ov = (b[i].rmax() - b[j].rmin()).min(b[j].rmax() - b[i].rmin());
            best.push((ov, i, j));
        }
    }
    best.sort_by(|x, y| y.0.total_cmp(&x.0));
    for &(_, i, j) in best.iter().take(3) {
        let mut out = Vec::new();
        let mut st = rung::TStats::default();
        let t0 = std::time::Instant::now();
        rung::truth_pair(&b[i], &b[j], rho, t_end, &mut out, &mut st);
        println!("{belt} pair ({i},{j}): {} enc, {} steps, {} evals, {:.2}s", out.len(), st.steps, st.evals, t0.elapsed().as_secs_f64());
    }
}
