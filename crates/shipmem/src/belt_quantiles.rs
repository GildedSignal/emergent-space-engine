//! Derived Rayleigh quantiles. All arithmetic, including table creation, is integer.
//! Each probability octave has 2048 midpoint cells, at BOTH ends of the CDF.
const BITS: u32 = 11;
const CELLS: usize = 1 << BITS;
const Q: u32 = 62;
const ONE: u128 = 1 << Q;
const LN2: u128 = 0x2c5c_85fd_f473_de6a; // floor(ln(2) * 2^62)

pub(super) struct Quantiles {
    values: Vec<u32>,
    sigma_milli: u16,
    e_bits: u8,
    cap: u32,
}
impl Quantiles {
    pub(super) fn new(sigma_milli: u16, e_bits: u8, cap: u32) -> Self {
        let mut values = Vec::with_capacity(2 * 64 * CELLS);
        for side in 0..2 {
            for z in 0..64u32 {
                for j in 0..CELLS {
                    if z == 0 {
                        values.push(0);
                        continue;
                    }
                    let d = if z <= 63 - BITS {
                        (1u64 << (63 - z)) + ((((2 * j + 1) as u64) << (63 - z - BITS)) >> 1)
                    } else {
                        // These octaves contain fewer than CELLS integer draws.
                        (1u64 << (63 - z)) + ((j as u64) >> (z + BITS - 63))
                    };
                    let u = if side == 0 { d } else { !d };
                    values.push(quantile(u, sigma_milli, e_bits).min(cap));
                }
            }
        }
        Self {
            values,
            sigma_milli,
            e_bits,
            cap,
        }
    }
    #[inline]
    pub(super) fn at(&self, u: u64) -> u32 {
        let (side, d) = if u < 1 << 63 { (0, u) } else { (1, !u) };
        if d < CELLS as u64 {
            return quantile(u, self.sigma_milli, self.e_bits).min(self.cap);
        }
        let z = d.leading_zeros();
        let j = if z <= 63 - BITS {
            ((d >> (63 - z - BITS)) as usize) & (CELLS - 1)
        } else {
            ((d << (z + BITS - 63)) as usize) & (CELLS - 1)
        };
        self.values[(side * 64 + z as usize) * CELLS + j]
    }
    pub(super) const fn bytes() -> usize {
        2 * 64 * CELLS * 4
    }
}

/// -ln((2 * survival + 1) / 2^65), Q62. Normalize, then use
/// ln(m) = 2 atanh((m-1)/(m+1)); |(m-1)/(m+1)| <= 1/3.
fn neg_ln(survival: u64) -> u128 {
    let n = 2 * survival as u128 + 1;
    let exponent = 127 - n.leading_zeros();
    let m = if exponent <= Q {
        n << (Q - exponent)
    } else {
        n >> (exponent - Q)
    };
    let x = ((m - ONE) << Q) / (m + ONE);
    let x2 = (x * x) >> Q;
    let (mut term, mut sum) = (x, x);
    for k in 1..32u128 {
        term = (term * x2) >> Q;
        sum += term / (2 * k + 1);
    }
    ((65 - exponent) as u128 * LN2).saturating_sub(2 * sum)
}
fn sqrt(n: u128) -> u128 {
    if n == 0 {
        return 0;
    }
    let mut x = 1u128 << (128 - n.leading_zeros()).div_ceil(2);
    loop {
        let y = (x + n / x) / 2;
        if y >= x {
            return x;
        }
        x = y;
    }
}
pub(super) fn quantile(u: u64, sigma_milli: u16, e_bits: u8) -> u32 {
    let square_q62 = neg_ln(!u) * 2 * (sigma_milli as u128).pow(2) / 1_000_000;
    (sqrt(square_q62) >> (31 - e_bits)).min(u32::MAX as u128) as u32
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn integer_quantiles_match_an_independent_float_oracle_across_octaves() {
        for sigma in [1, 70, 110, 1000] {
            for z in 0..64 {
                for d in [0, 1, 3, 17, 255] {
                    let u = ((1u64 << z) - 1).saturating_add(d);
                    for u in [u, !u] {
                        let survival = (!u as f64 + 0.5) / 18446744073709551616.0;
                        let expected =
                            (sigma as f64 / 1000.0 * (-2.0 * survival.ln()).sqrt() * 1073741824.0)
                                .min(u32::MAX as f64) as u32;
                        assert!(
                            quantile(u, sigma, 30).abs_diff(expected) <= 24,
                            "sigma={sigma} u={u} got={} expected={expected}",
                            quantile(u, sigma, 30)
                        );
                    }
                }
            }
        }
    }
    #[test]
    fn both_cdf_tails_are_resolved_and_tables_are_monotone() {
        let t = Quantiles::new(70, 30, 644_245_094);
        let mut prev = 0;
        for k in 0..=100000u64 {
            let u = ((u64::MAX as u128 * k as u128) / 100000) as u64;
            let e = t.at(u);
            assert!(e >= prev);
            prev = e;
        }
        assert_eq!(t.at(0), 0);
        assert_eq!(t.at(u64::MAX), 644_245_094);
        assert_ne!(t.at(1 << 44), t.at(1 << 45));
        assert_ne!(t.at(!(1 << 44)), t.at(!(1 << 45)));
    }
}
