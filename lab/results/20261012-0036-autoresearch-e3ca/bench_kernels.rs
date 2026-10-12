//! Kernel micro-bench (run 20261012-0036): isqrt variants, wide division costs.
use std::time::Instant;

fn lcg(state: &mut u64) -> u64 {
    *state = state.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
    *state
}

/// Current num::isqrt (top-64 seed, u128 Newton from above).
fn isqrt_a(x: u128) -> u128 {
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

/// Candidate v2: f64 seed plus a provable at-or-above-root margin; identical descent.
fn isqrt_c(x: u128) -> u128 {
    if x < (1u128 << 40) {
        return (x as u64).isqrt() as u128;
    }
    let est = (x as f64).sqrt() as u128;
    let mut y = est + (est >> 40) + 16;
    loop {
        let z = (y + x / y) >> 1;
        if z >= y {
            return y;
        }
        y = z;
    }
}

fn main() {
    let n = 2_000_000u64;
    let mut s = 42u64;
    let mut xs: Vec<u128> = Vec::with_capacity(n as usize);
    for _ in 0..n {
        let bits = 30 + (lcg(&mut s) >> 59) as u32;
        let d = (1u128 << bits) + (lcg(&mut s) as u128 & ((1u128 << bits) - 1));
        xs.push(d.min((1u128 << 62) - 1) << 62);
    }
    // Edge corpus: adversarial widths (down to 2 and up to full 128 bits).
    for _ in 0..200_000 {
        let bits = (lcg(&mut s) >> 58) as u32;
        xs.push(((1u128 << bits) + (lcg(&mut s) as u128)) & ((1u128 << 126) - 1) | 1);
    }
    let mut agree = true;
    let mut bad = 0u128;
    for &x in &xs {
        if isqrt_a(x) != isqrt_c(x) {
            agree = false;
            bad = x;
            break;
        }
    }
    let m = xs.len() as u64;
    let t = Instant::now();
    let mut acc = 0u128;
    for &x in &xs {
        acc = acc.wrapping_add(isqrt_a(x));
    }
    let a_ns = t.elapsed().as_nanos() as f64 / m as f64;
    let t = Instant::now();
    for &x in &xs {
        acc = acc.wrapping_add(isqrt_c(x));
    }
    let c_ns = t.elapsed().as_nanos() as f64 / m as f64;
    println!(
        "agree={} bad={:x} isqrt_a={:.1}ns isqrt_c={:.1}ns acc={:x}",
        agree, bad, a_ns, c_ns, acc
    );
}
