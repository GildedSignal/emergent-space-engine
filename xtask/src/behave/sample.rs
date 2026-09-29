//! The seed sampler: SplitMix64, one fixed seed per gate set, so every run and every law meets
//! the same cases. Units are G = c = M = 1.

/// SplitMix64 (Steele, Lea and Flood, 2014).
pub(crate) struct Rng(pub(crate) u64);
impl Rng {
    pub(crate) fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
    /// Uniform integer in [lo, hi].
    pub(crate) fn range(&mut self, lo: i128, hi: i128) -> i128 {
        lo + (self.next() as u128 % (hi - lo + 1) as u128) as i128
    }
    /// Uniform in [0, 1) with 53 bits.
    fn unit(&mut self) -> f64 {
        (self.next() >> 11) as f64 / (1u64 << 53) as f64
    }
    /// Log-uniform in [lo, hi].
    fn log_uniform(&mut self, lo: f64, hi: f64) -> f64 {
        lo * (hi / lo).powf(self.unit())
    }
}

/// Seed of the bound-orbit set (G1, G2, G5, G6) and of the light set (G3).
pub const BOUND_SEED: u64 = 20260930;
pub const LIGHT_SEED: u64 = 20260931;

/// `n` bound orbits (p, e): p log-uniform in [10, 1000], e uniform in [0, 0.7], redrawn unless
/// p >= 6.5 + 2e (it never binds for p >= 10; it keeps a wider range safe). The first `k` of `n`
/// are the same orbits as the first `k` of any longer draw.
pub fn bound_orbits(n: usize) -> Vec<(f64, f64)> {
    let mut rng = Rng(BOUND_SEED);
    let mut out = Vec::with_capacity(n);
    while out.len() < n {
        let (p, e) = (rng.log_uniform(10.0, 1000.0), 0.7 * rng.unit());
        if p >= 6.5 + 2.0 * e {
            out.push((p, e));
        }
    }
    out
}

/// `n` light impact parameters b, log-uniform in [10, 1000].
pub fn light_impacts(n: usize) -> Vec<f64> {
    let mut rng = Rng(LIGHT_SEED);
    (0..n).map(|_| rng.log_uniform(10.0, 1000.0)).collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn splitmix64_matches_the_reference_vector() {
        // The published first outputs of SplitMix64 seeded with 0.
        let mut r = Rng(0);
        assert_eq!([r.next(), r.next()], [0xE220_A839_7B1D_CDAF, 0x6E78_9E6A_A1B9_65F4]);
    }

    #[test]
    fn draws_are_deterministic_prefix_stable_and_in_range() {
        let (a, b) = (bound_orbits(256), bound_orbits(32));
        assert_eq!(a[..32], b[..]);
        assert!(a.iter().all(|&(p, e)| (10.0..=1000.0).contains(&p) && (0.0..0.7).contains(&e) && p >= 6.5 + 2.0 * e));
        assert!(light_impacts(64).iter().all(|b| (10.0..=1000.0).contains(b)));
        // Log-uniform: about half the draws fall below the geometric middle, sqrt(10 * 1000) = 100.
        let low = a.iter().filter(|&&(p, _)| p < 100.0).count();
        assert!((100..156).contains(&low), "{low} of 256 below p = 100");
    }
}
