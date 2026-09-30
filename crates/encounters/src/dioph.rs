//! The next close conjunction as an exact integer Diophantine problem.
//!
//! A pair's section is an integer circle rotation: s_l = (c + l*d) mod m. The first return into a
//! window [lo, hi] is found by a Euclid-like recursion (continued fractions in disguise): each level
//! swaps (d, m) for (m mod d, d), so the depth is O(log m). Exact, no floats.

/// Smallest k >= 0 with lo <= (c + d*k) mod m <= hi, for 0 <= lo <= hi < m and c < m.
/// `steps` counts recursion levels.
pub fn first_hit(c: u128, d: u128, m: u128, lo: u128, hi: u128, steps: &mut u64) -> Option<u128> {
    debug_assert!(lo <= hi && hi < m && c < m);
    if lo <= c && c <= hi {
        return Some(0);
    }
    // d*k mod m must lie in [lo - c, hi - c] (mod m); c is outside [lo, hi], so this interval
    // excludes 0 and does not wrap.
    let l2 = (lo + m - c) % m;
    let h2 = (hi + m - c) % m;
    debug_assert!(1 <= l2 && l2 <= h2);
    min_k(d % m, m, l2, h2, steps)
}

/// Smallest k >= 0 with l <= (a*k mod m) <= r, for 0 <= l <= r < m.
fn min_k(a: u128, m: u128, l: u128, r: u128, steps: &mut u64) -> Option<u128> {
    *steps += 1;
    if l == 0 {
        return Some(0);
    }
    if a == 0 {
        return None;
    }
    let k = (l + a - 1) / a;
    if a * k <= r {
        return Some(k);
    }
    // No multiple of a lies in [l, r], so l mod a <= r mod a, both nonzero. We need the smallest
    // y >= 1 with m*y mod a in [a - r mod a, a - l mod a]; then k = ceil((l + m*y) / a).
    let y = min_k(m % a, a, a - r % a, a - l % a, steps)?;
    Some((l + m * y + a - 1) / a)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn brute(c: u128, d: u128, m: u128, lo: u128, hi: u128) -> Option<u128> {
        let mut x = c;
        for k in 0..(2 * m + 2) {
            if lo <= x && x <= hi {
                return Some(k);
            }
            x = (x + d) % m;
        }
        None
    }

    #[test]
    fn matches_brute_force() {
        let mut s: u64 = 12345;
        let mut next = || {
            s = s.wrapping_add(0x9E3779B97F4A7C15);
            let mut z = s;
            z = (z ^ (z >> 30)).wrapping_mul(0xBF58476D1CE4E5B9);
            z = (z ^ (z >> 27)).wrapping_mul(0x94D049BB133111EB);
            z ^ (z >> 31)
        };
        let mut steps = 0;
        for _ in 0..200_000 {
            let m = 1 + (next() % 3000) as u128;
            let c = (next() as u128) % m;
            let d = (next() as u128) % m;
            let a = (next() as u128) % m;
            let b = (next() as u128) % m;
            let (lo, hi) = if a <= b { (a, b) } else { (b, a) };
            let hi = if next() % 3 == 0 { lo + (hi - lo) / 50 } else { hi };
            assert_eq!(first_hit(c, d, m, lo, hi, &mut steps), brute(c, d, m, lo, hi), "{c} {d} {m} {lo} {hi}");
        }
    }

    #[test]
    fn large_moduli_are_exact() {
        // m ~ 2^44 (a period in ticks), window ~ 2^20: check the answer is a hit and that no
        // earlier k is (brute force up to the answer when it is small enough).
        let mut steps = 0;
        let m: u128 = 27_000_000_000_017;
        for t in 0..200u128 {
            let d = (m / 997) * (t + 1) + 12345 * t;
            let d = d % m;
            let c = (t * 7_919_000_000_001) % m;
            let (lo, hi) = (1u128 << 40, (1u128 << 40) + (1 << 20));
            if let Some(k) = first_hit(c, d, m, lo, hi, &mut steps) {
                let x = (c + d * k) % m;
                assert!(lo <= x && x <= hi);
                if k < 2_000_000 {
                    let mut y = c;
                    for _ in 0..k {
                        assert!(!(lo <= y && y <= hi));
                        y = (y + d) % m;
                    }
                }
            }
        }
    }
}
