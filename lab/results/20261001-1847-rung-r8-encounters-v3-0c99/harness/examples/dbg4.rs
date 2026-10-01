fn main() {
    let b = rung::load_belt("data/adv-coorbital.bin");
    let (i, j) = (539usize, 581usize);
    // dense g(t) scan around the double minimum
    let mut prev_g = 0.0f64;
    let mut prev_d = 0.0f64;
    let (lo, hi) = (556.8f64, 558.5f64);
    let k = 34000usize; // h = 5e-5
    for q in 0..=k {
        let t = lo + (hi - lo) * q as f64 / k as f64;
        let (r, v) = rung::mrel_pub(&b[i], &b[j], t);
        let d = (r[0]*r[0] + r[1]*r[1]).sqrt();
        let g = r[0]*v[0] + r[1]*v[1];
        if q > 0 && ((prev_g < 0.0 && g >= 0.0) || (prev_g >= 0.0 && g < 0.0)) {
            println!("g sign change at t={:.6}: d={:.6e} g={:.3e} (prev g={:.3e} d={:.6e})", t, d, g, prev_g, prev_d);
        }
        prev_g = g; prev_d = d;
    }
}
