fn main() {
    let b = rung::load_belt("data/a13.bin");
    let rho = 9.4585e-4_f64;
    let mut rp = rung::radial_pairs(&b, rho);
    println!("radial pairs: {}", rp.len());
    let t0 = std::time::Instant::now();
    let (truth, st) = rung::truth_all(&b, &rp, rho, 100.0 * std::f64::consts::TAU);
    println!("truth all: {} enc, {} steps, {} evals, {:.1}s", truth.len(), st.steps, st.evals, t0.elapsed().as_secs_f64());
    let t0 = std::time::Instant::now();
    let (conj, cst) = rung::conj_all(&b, &rp, rho, 100.0 * std::f64::consts::TAU);
    println!("conj all: {} enc, {} events, {:.1}s", conj.len(), cst.conjunctions, t0.elapsed().as_secs_f64());
    let (m, f, n) = rung::matchup(&truth, &conj, 100.0 * std::f64::consts::TAU, 1e-3);
    println!("conj vs truth: missed={} false={} n={}", m, f, n);
    let cs = emergent_encounters::pairs::cone_pairs(&b, rho);
    let t0 = std::time::Instant::now();
    let (meth, mst) = rung::dioph_all(&b, &cs.pairs, rho, 0.0, 100.0 * std::f64::consts::TAU);
    println!("dioph all: {} enc, checks {}, {:.1}s", meth.len(), mst.checks_total(), t0.elapsed().as_secs_f64());
    let (m2, f2, _) = rung::matchup(&truth, &meth, 100.0 * std::f64::consts::TAU, 1e-3);
    println!("dioph vs truth: missed={} false={}", m2, f2);
    let _ = rp.len(); rp.clear();
}
