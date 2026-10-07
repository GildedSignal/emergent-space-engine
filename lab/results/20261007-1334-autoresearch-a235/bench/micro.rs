#[allow(dead_code)]
fn micro() {
    use emergent_space::num;
    let args: Vec<String> = std::env::args().collect();
    if !args.iter().any(|a| a == "micro") { return; }
    let n = 2_000_000u32;
    let psis: Vec<i128> = (0..n)
        .map(|i| ((i as i128 * 7244019458077122842) / n as i128).abs())
        .collect();
    let mut acc = 0i128;
    let t = Instant::now();
    for &p in &psis {
        acc = acc.wrapping_add(num::cos(p));
    }
    println!("cos: {:.1} ns/call (acc {})", t.elapsed().as_nanos() as f64 / n as f64, acc & 1);
    let mut x: u128 = 0x123456789abcdef;
    let mut acc2 = 0u64;
    let t = Instant::now();
    for _ in 0..n {
        x = x.wrapping_mul(6364136223846793005).wrapping_add(1);
        let den = (x >> 64) as u64 | 1;
        acc2 = acc2.wrapping_add(num::div_word(x, den));
    }
    println!("div_word: {:.1} ns/call (acc {})", t.elapsed().as_nanos() as f64 / n as f64, acc2 & 1);
    let t = Instant::now();
    let mut acc3 = 0u128;
    for _ in 0..n {
        x = x.wrapping_mul(6364136223846793005).wrapping_add(1);
        acc3 = acc3.wrapping_add(num::isqrt(x >> 2));
    }
    println!("isqrt126: {:.1} ns/call (acc {})", t.elapsed().as_nanos() as f64 / n as f64, acc3 & 1);
    let ys: Vec<u64> = (0..n).map(|i| ((i as u128 * 0x9E3779B97F4A7C15u128) >> 64) as u64).collect();
    let t = Instant::now();
    let mut a4 = 0u64;
    for &v in &ys { a4 = a4.wrapping_add(v.isqrt()); }
    println!("u64::isqrt(std): {:.1} ns/call", t.elapsed().as_nanos() as f64 / n as f64);
    #[inline(never)]
    fn isf(v: u64) -> u64 {
        let mut r = (v as f64).sqrt() as u64;
        while r > 0 && (r as u128) * (r as u128) > v as u128 { r -= 1; }
        while ((r + 1) as u128) * ((r + 1) as u128) <= v as u128 { r += 1; }
        r
    }
    let t = Instant::now();
    let mut a5 = 0u64;
    for &v in &ys { a5 = a5.wrapping_add(isf(v)); }
    println!("u64 f64-seeded: {:.1} ns/call  (match: {})", t.elapsed().as_nanos() as f64 / n as f64, a4 == a5);
}
