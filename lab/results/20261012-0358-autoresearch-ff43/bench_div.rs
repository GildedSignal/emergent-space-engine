//! TEMPORARY (20261012-0358-autoresearch-ff43): div_word and isqrt implementation shootout.
//! Every candidate must return the same integer as the reference for all inputs tried.
use std::time::Instant;

/// Reference: current shipped base-2^32 Knuth D.
fn div_word_ref(n: u128, d: u64) -> u64 {
    debug_assert!(d != 0 && (n >> 64) < d as u128);
    if n <= u64::MAX as u128 {
        return n as u64 / d;
    }
    const B: u64 = 1 << 32;
    const MASK: u64 = B - 1;
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
            if r >= B {
                break;
            }
        }
        q
    };
    let q1 = digit(u1, u0 >> 32);
    let rem = (u1 << 32).wrapping_add(u0 >> 32).wrapping_sub(q1.wrapping_mul(v));
    let q0 = digit(rem, u0 & MASK);
    (q1 << 32) + q0
}

/// Candidate A: one 64-bit hardware divide via the n>>64<d precondition (128/64 fits).
#[cfg(target_arch = "x86_64")]
fn div_word_asm(n: u128, d: u64) -> u64 {
    debug_assert!(d != 0 && (n >> 64) < d as u128);
    let lo = n as u64;
    let hi = (n >> 64) as u64;
    let q: u64;
    unsafe {
        std::arch::asm!(
            "div {d}",
            inlateout("rax") lo => q,
            inlateout("rdx") hi => _,
            d = in(reg) d,
            options(nomem, nostack)
        );
    }
    q
}

fn isqrt_ref(x: u128) -> u128 {
    if x < 2 {
        return x;
    }
    let shift = (128 - x.leading_zeros()).saturating_sub(64).div_ceil(2) * 2;
    let top = (x >> shift) as u64;
    let mut y = top.isqrt() as u128 + 1;
    y <<= shift / 2;
    loop {
        let z = (y + x / y) >> 1;
        if z >= y {
            return y;
        }
        y = z;
    }
}

/// Candidate: Newton with div_word_ref instead of u128/u128.
fn isqrt_dw(x: u128) -> u128 {
    if x < 2 {
        return x;
    }
    let shift = (128 - x.leading_zeros()).saturating_sub(64).div_ceil(2) * 2;
    let top = (x >> shift) as u64;
    let mut y = top.isqrt() as u128 + 1;
    y <<= shift / 2;
    loop {
        let q = if y <= u64::MAX as u128 && x >> 64 < y {
            div_word_ref(x, y as u64) as u128
        } else if y <= u64::MAX as u128 {
            // x/y >= 2^64: quotient wider than a word only in the first step; fall back.
            x / y
        } else {
            x / y
        };
        let z = (y + q) >> 1;
        if z >= y {
            return y;
        }
        y = z;
    }
}

fn main() {
    // Correctness sweep: n>>64 < d, wide magnitudes.
    let mut seed = 0xB5026A5B0F1E89A3u64;
    let mut next = || {
        seed ^= seed << 13;
        seed ^= seed >> 7;
        seed ^= seed << 17;
        seed
    };
    let mut cases = Vec::new();
    for _ in 0..200_000 {
        let d = (next() as u128 | (1u128 << 63) | ((next() % (1 << 20)) as u128)) as u64;
        let nhi = next() as u128 % d as u128;
        let n = (nhi << 64) | next() as u128;
        cases.push((n, d));
    }
    let mut bad = 0;
    for &(n, d) in &cases {
        let a = div_word_ref(n, d);
        let b = isqrt_correctness_placeholder(n, d);
        if a != b {
            bad += 1;
        }
    }
    println!("asm mismatches: {bad}");

    // isqrt equivalence
    let mut bad2 = 0;
    for _ in 0..100_000 {
        let bits = 60 + (next() as u32 % 68) as u32;
        let x = (next() as u128) | ((next() as u128) << 64) >> (128 - bits) | 1;
        if isqrt_ref(x) != isqrt_dw(x) {
            bad2 += 1;
        }
    }
    println!("isqrt mismatches: {bad2}");

    // u128/u128 with 64-bit divisor (LLVM __udivti3 fast path) + correctness
    let mut bad3 = 0;
    for &(n, d) in &cases {
        if div_word_ref(n, d) != ((n / d as u128) as u64) {
            bad3 += 1;
        }
    }
    println!("u128/u128 mismatches: {bad3}");

    // Timing
    let t = Instant::now();
    let mut acc2 = 0u128;
    for &(n, d) in &cases {
        acc2 = acc2.wrapping_add(n / d as u128);
    }
    println!("u128_by_u64: {:?} ({:.2} ns/call)", t.elapsed(), t.elapsed().as_secs_f64() / cases.len() as f64 * 1e9);
    std::hint::black_box(acc2);
    let t = Instant::now();
    let mut acc = 0u64;
    for &(n, d) in &cases {
        acc = acc.wrapping_add(div_word_ref(n, d));
    }
    println!("div_word_ref: {:?} ({:.2} ns/call)", t.elapsed(), t.elapsed().as_secs_f64() / cases.len() as f64 * 1e9);
    let t = Instant::now();
    for &(n, d) in &cases {
        acc = acc.wrapping_add(div_word_asm(n, d));
    }
    println!("div_word_asm: {:?} ({:.2} ns/call)", t.elapsed(), t.elapsed().as_secs_f64() / cases.len() as f64 * 1e9);

    let sqrt_cases: Vec<u128> = (0..100_000)
        .map(|_| {
            let bits = 100 + (next() as u32 % 28);
            (((next() as u128) << 64) | next() as u128) >> (128 - bits) | 1
        })
        .collect();
    let t = Instant::now();
    for &x in &sqrt_cases {
        acc = acc.wrapping_add(isqrt_ref(x) as u64);
    }
    println!("isqrt_ref: {:?} ({:.2} ns/call)", t.elapsed(), t.elapsed().as_secs_f64() / sqrt_cases.len() as f64 * 1e9);
    let t = Instant::now();
    for &x in &sqrt_cases {
        acc = acc.wrapping_add(isqrt_dw(x) as u64);
    }
    println!("isqrt_dw: {:?} ({:.2} ns/call)", t.elapsed(), t.elapsed().as_secs_f64() / sqrt_cases.len() as f64 * 1e9);
    std::hint::black_box(acc);
}

fn isqrt_correctness_placeholder(n: u128, d: u64) -> u64 {
    div_word_asm(n, d)
}
