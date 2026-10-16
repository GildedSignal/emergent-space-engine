//! Integer primitives of the law. Each is an exact function of its integer inputs: its value is
//! defined by the formula in its comment, so any faster implementation must return the same bits.
use crate::tables::{ATAN, ODD, PI, SINE};
use crate::{Error, Result};

/// 1 in Q62.
pub const ONE: i128 = 1 << 62;

/// Exact 128/64 division with a word-sized quotient (`n >> 64 < d`).
/// In base 2^32, each trial digit comes from one native division. The low
/// divisor digit corrects the trial by at most two; no rounding is introduced.
#[inline]
pub(crate) fn div_word(n: u128, d: u64) -> u64 {
    debug_assert!(d != 0 && (n >> 64) < d as u128);
    if n <= u64::MAX as u128 {
        return n as u64 / d;
    }
    const B: u64 = 1 << 32;
    const MASK: u64 = B - 1;
    let shift = d.leading_zeros();
    let v = d << shift;
    let (v1, v0) = (v >> 32, v & MASK);
    // The quotient precondition also guarantees that this normalization fits.
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

/// floor(sqrt(x)).
pub fn isqrt(x: u128) -> u128 {
    if x < 2 {
        return x;
    }
    // Start at or above the root: the root of the top 64 bits (u64 Newton), plus one, rescaled.
    let shift = (128 - x.leading_zeros()).saturating_sub(64).div_ceil(2) * 2;
    let top = (x >> shift) as u64;
    let mut y = top.isqrt() as u128 + 1;
    y <<= shift / 2;
    // Newton from above decreases monotonically to floor(sqrt(x)).
    loop {
        let z = (y + x / y) >> 1;
        if z >= y {
            return y;
        }
        y = z;
    }
}

/// floor(a * b / 2^s) for a, b >= 0, from the exact 256-bit product; Range if it exceeds u128.
pub fn mul_shr(a: u128, b: u128, s: u32) -> Result<u128> {
    const M: u128 = u64::MAX as u128;
    let (a1, a0, b1, b0) = (a >> 64, a & M, b >> 64, b & M);
    let (p00, p01, p10, p11) = (a0 * b0, a0 * b1, a1 * b0, a1 * b1);
    let mid = (p00 >> 64) + (p01 & M) + (p10 & M);
    let lo = (p00 & M) | (mid << 64);
    let hi = p11 + (p01 >> 64) + (p10 >> 64) + (mid >> 64);
    let (hi, lo) = match s {
        0 => (hi, lo),
        1..=127 => (hi >> s, (lo >> s) | (hi << (128 - s))),
        128..=255 => (0, hi >> (s - 128)),
        _ => (0, 0),
    };
    if hi != 0 {
        return Err(Error::Range);
    }
    Ok(lo)
}

/// cos(psi) in Q62 for psi in [0, pi] in Q61. With x = psi - pi/2 in Q62 (|x| <= pi/2),
/// cos(psi) = -sin(x), and sin(x) = x(1 - x^2/(2*3)(1 - x^2/(4*5)(1 - ... x^2/(26*27)))):
/// thirteen nested factors, innermost first, each product floored (arithmetic shift).
pub fn cos(psi: i128) -> i128 {
    if psi == 0 {
        return ONE;
    }
    if psi == PI {
        return -ONE;
    }
    // |x|<=pi/2 in Q62 fits i64. x² and each x²*s shift fit u64 (<2.5*2^62).
    // Make those bounds visible to codegen: one 64×64 product, not a general 128×128.
    let x = (2 * psi - PI) as i64;
    let x2 = ((x as i128 * x as i128) >> 62) as u64;
    let mut s = ONE as u64;
    for r in SINE.iter().rev() {
        let y = ((x2 as u128 * s as u128) >> 62) as u64;
        s = ONE as u64 - ((y as u128 * *r as u64 as u128) >> 62) as u64;
    }
    -((x as i128 * s as i128) >> 62)
}

/// atan(s) in Q62 for s in [0, 1] in Q62. j = round(16 s) (ties up), a = j/16,
/// t = trunc((s - a) 2^62 / (1 + s a)) with |t| <= 1/32, and
/// atan(s) = atan(j/16) + t(1 - t^2/3 + t^4/5 - ... + t^12/13), nested, products floored.
pub fn atan(s: i128) -> i128 {
    let j = (s + (1 << 57)) >> 58;
    let a = j << 58;
    let t = ((s - a) << 62) / (ONE + ((s * a) >> 62));
    let t2 = (t * t) >> 62;
    let mut p = ODD[6];
    for c in ODD[..6].iter().rev() {
        p = c - ((t2 * p) >> 62);
    }
    ATAN[j as usize] + ((t * p) >> 62)
}

/// floor(floor(sqrt(num * den)) 2^62 / den): sqrt(num/den) in Q62, for 0 <= num <= den < 2^61.
pub fn ratio_sqrt(num: i128, den: i128) -> i128 {
    ((isqrt((num * den) as u128) as i128) << 62) / den
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn word_division_matches_wide_division_at_digit_corrections() {
        let mut x = 1u128;
        for i in 0..20000 {
            x = x.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            for d in [1, 3, u32::MAX as u64, 1 << 32, (1 << 32) + 1,
                (1 << 62) - 1, 1 << 62, (1 << 63) - 1, 1 << 63, u64::MAX,
                (x as u64).max(1)] {
                let n = ((x >> 64) % d as u128) << 64 | x as u64 as u128;
                assert_eq!(div_word(n, d) as u128, n / d as u128, "{i}: {n}/{d}");
                for n in [0, d as u128 - 1, d as u128, d as u128 * u64::MAX as u128] {
                    assert_eq!(div_word(n, d) as u128, n / d as u128);
                }
            }
        }
    }
    #[test]
    fn isqrt_is_the_exact_floor() {
        let mut x: u128 = 1;
        for i in 0..4000u128 {
            x = x.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407 + i);
            for v in [x, x >> (i % 127), i, (i * i).saturating_sub(1), i * i] {
                let r = isqrt(v);
                assert!(r * r <= v && (r + 1).checked_mul(r + 1).is_none_or(|s| s > v), "{v}");
            }
        }
        assert_eq!(isqrt(u128::MAX), u64::MAX as u128);
    }
    #[test]
    fn mul_shr_agrees_with_u128_where_it_fits_and_refuses_overflow() {
        for (a, b, s) in [
            (3u128 << 70, 5u128 << 40, 30u32),
            (u64::MAX as u128, u64::MAX as u128, 0),
            (7, 9, 1),
        ] {
            assert_eq!(mul_shr(a, b, s).unwrap(), (a * b) >> s);
        }
        assert_eq!(mul_shr(1 << 127, 1 << 127, 200).unwrap(), 1 << 54);
        assert_eq!(mul_shr(1 << 127, 1 << 127, 100), Err(Error::Range));
    }
    #[test]
    fn cos_and_atan_match_their_functions_to_a_few_units() {
        for i in 0..=1000 {
            let psi = PI * i / 1000;
            let want = (psi as f64 / 2f64.powi(61)).cos();
            assert!((cos(psi) as f64 / 2f64.powi(62) - want).abs() < 4e-16, "psi {psi}");
            let s = ONE * i / 1000;
            let want = (s as f64 / 2f64.powi(62)).atan();
            assert!((atan(s) as f64 / 2f64.powi(62) - want).abs() < 4e-16, "s {s}");
        }
        assert_eq!(atan(ONE), PI / 2);
        assert_eq!(atan(0), 0);
    }
}
