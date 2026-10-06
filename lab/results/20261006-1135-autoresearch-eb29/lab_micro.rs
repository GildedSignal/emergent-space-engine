//! TEMPORARY microbench for lab run 20261006-1135: cost of num::cos and the
//! 128/64 div_word pattern used per weak_quad node.
fn cos(psi: i128) -> i128 {
    // verbatim copy of crates/space/src/num.rs cos (module is private there)
    const ONE: i128 = 1 << 62;
    const PI: i128 = 7244019458077122842;
    const SINE: [i128; 13] = [768614336404564651, 230584300921369395, 109802048057794950, 64051194700380388, 41924418349339890, 29562089861714025, 21960409611558990, 16954728008924220, 13484462042185345, 10980204805779495, 9114003988986933, 7686143364045647, 6569353302603117];
    if psi == 0 {
        return ONE;
    }
    if psi == PI {
        return -ONE;
    }
    let x = (2 * psi - PI) as i64;
    let x2 = ((x as i128 * x as i128) >> 62) as u64;
    let mut s = ONE as u64;
    for r in SINE.iter().rev() {
        let y = ((x2 as u128 * s as u128) >> 62) as u64;
        s = ONE as u64 - ((y as u128 * *r as u64 as u128) >> 62) as u64;
    }
    -((x as i128 * s as i128) >> 62)
}
use std::time::Instant;

/// Copy of crates/space/src/num.rs div_word (pub(crate) there) for timing only.
fn div_word(n: u128, d: u64) -> u64 {
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

fn main() {
    // Representative inputs: psi in [0, PI] Q61 spread; x in [0.5, 1] Q62.
    let n = 2_000_000u64;
    let mut acc = 0i128;
    let t = Instant::now();
    for i in 0..n {
        let psi = (i as i128 * 3_622_009) % 7_244_019_458_077_122_842;
        acc ^= cos(psi);
    }
    let cos_ns = t.elapsed().as_nanos() as f64 / n as f64;
    let t = Instant::now();
    let mut acc2 = 0u64;
    for i in 0..n {
        let x = 2_305_843_009_213_693_952u64 + (i as u64 * 1_111_111_111) % 2_305_843_009_213_693_952;
        acc2 ^= div_word((2_251_799_813_685_248u128 << 62), x);
    }
    let div_ns = t.elapsed().as_nanos() as f64 / n as f64;
    println!("cos_ns={cos_ns:.1} div_word_ns={div_ns:.1} acc={acc}{acc2}");
}
