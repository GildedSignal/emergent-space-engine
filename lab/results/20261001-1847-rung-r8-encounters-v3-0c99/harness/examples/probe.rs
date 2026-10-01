fn main() {
    let b = rung::load_belt("data/b-steady.bin");
    let rho = 1e-4_f64;
    // one truth pair over 200 orbits: calibrate steps/second right now
    let mut out = Vec::new();
    let mut st = rung::TStats::default();
    let t0 = std::time::Instant::now();
    rung::truth_pair(&b[3], &b[700], rho, 200.0 * std::f64::consts::TAU, &mut out, &mut st);
    let s = t0.elapsed().as_secs_f64();
    println!("200 orbits: {} steps {} evals in {:.2}s -> {:.2} us/eval, enc={}", st.steps, st.evals, s, s * 1e6 / st.evals as f64, out.len());
    let t0 = std::time::Instant::now();
    rung::truth_pair(&b[3], &b[700], rho, 2000.0 * std::f64::consts::TAU, &mut out, &mut st);
    println!("2000 orbits: {} steps {} evals in {:.2}s", st.steps, st.evals, t0.elapsed().as_secs_f64());
}
