use std::time::Instant;
use std::hint::black_box;

#[inline]
fn div_word(n: u128, d: u64) -> u64 {
    if n <= u64::MAX as u128 { return n as u64 / d; }
    const B: u64 = 1 << 32; const MASK: u64 = B - 1;
    let shift = d.leading_zeros();
    let v = d << shift;
    let (v1, v0) = (v >> 32, v & MASK);
    let u = n << shift;
    let (u1, u0) = ((u >> 64) as u64, u as u64);
    let digit = |upper: u64, lower: u64| {
        let mut q = upper / v1;
        let mut r = upper % v1;
        while q >= B || q * v0 > (r << 32) + lower {
            q -= 1;
            r += v1;
            if r >= B { break; }
        }
        q
    };
    let q1 = digit(u1, u0 >> 32);
    let rem = (u1 << 32).wrapping_add(u0 >> 32).wrapping_sub(q1.wrapping_mul(v));
    let q0 = digit(rem, u0 & MASK);
    (q1 << 32) + q0
}

fn main() {
    // representative operands: numerator ~2^104..2^122, divisor ~2^46..2^62
    let cases: Vec<(u128, u64)> = vec![
        (1u128 << 104, 1u64 << 46),
        ((1u128 << 104) / 3 * 2, (1 << 47) + 12345),
        (0xC000_0000_0000_0000_0000_0000_0000u128 >> 6, (1 << 52) + 7),
        (0xA5A5_A5A5_A5A5_A5A5_A5A5_0000_0000u128, (1 << 58) + 99),
    ];
    let t0 = Instant::now();
    let mut acc = 0u64;
    for _ in 0..10_000_000u64 {
        for &(n, d) in &cases {
            let d = black_box(d);
            acc = acc.wrapping_add(((black_box(n) / d as u128) as u64) ^ 1);
        }
    }
    let wide = t0.elapsed();
    let t1 = Instant::now();
    for _ in 0..10_000_000u64 {
        for &(n, d) in &cases {
            let d = black_box(d);
            acc = acc.wrapping_add(div_word(black_box(n), d) ^ 1);
        }
    }
    let dw = t1.elapsed();
    println!("acc={acc} u128/u128: {wide:?}  div_word: {dw:?}  ratio {:.2}", wide.as_secs_f64() / dw.as_secs_f64());
    // correctness spot check
    for &(n, d) in &cases {
        assert_eq!(div_word(n, d), (n / d as u128) as u64);
    }
}
