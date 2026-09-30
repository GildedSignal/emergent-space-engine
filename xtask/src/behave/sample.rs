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
    pub(crate) fn unit(&mut self) -> f64 {
        (self.next() >> 11) as f64 / (1u64 << 53) as f64
    }
    /// Log-uniform in [lo, hi].
    pub(crate) fn log_uniform(&mut self, lo: f64, hi: f64) -> f64 {
        lo * (hi / lo).powf(self.unit())
    }
}

/// Seed of the bound-orbit set (G1, G2, G5, G6) and of the light set (G3).
pub const BOUND_SEED: u64 = 20260930;
pub const LIGHT_SEED: u64 = 20260931;
/// Seed of the clock radii (B7).
pub const CLOCK_SEED: u64 = 20260932;
/// Seeds of the events layer: binaries (B11), handoffs (B12), assists (B13), Hill moons (B14).
pub const BINARY_SEED: u64 = 20261001;
pub const HANDOFF_SEED: u64 = 20261002;
pub const ASSIST_SEED: u64 = 20261003;
pub const HILL_SEED: u64 = 20261004;

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

/// `n` radii r, log-uniform in [3, 10^4] and strictly above 3 (a circular orbit needs r > 3M).
pub fn clock_radii(n: usize) -> Vec<f64> {
    let mut rng = Rng(CLOCK_SEED);
    let mut out = Vec::with_capacity(n);
    while out.len() < n {
        let r = rng.log_uniform(3.0, 1e4);
        if r > 3.0 {
            out.push(r);
        }
    }
    out
}

/// `n` binaries (p, e, ν): p log-uniform in [20, 1000], e uniform in [0, 0.6], ν uniform in [0.01, 0.25].
pub fn binaries(n: usize) -> Vec<(f64, f64, f64)> {
    let mut rng = Rng(BINARY_SEED);
    (0..n)
        .map(|_| {
            let p = rng.log_uniform(20.0, 1000.0);
            (p, 0.6 * rng.unit(), 0.01 + 0.24 * rng.unit())
        })
        .collect()
}

/// `n` handoff candidates (side, k, α): side ±1 (outside or inside the planet's orbit), k uniform
/// in [1.5, 3] (the orbit's distance from the planet's, in Hill radii), and the starting angle from
/// the planet α uniform in [30°, 330°], radians. The first `k` of `n` are those of any longer draw.
pub fn handoffs(n: usize) -> Vec<(f64, f64, f64)> {
    let mut rng = Rng(HANDOFF_SEED);
    (0..n)
        .map(|_| {
            let side = if rng.next() >> 63 == 1 { 1.0 } else { -1.0 };
            let k = 1.5 + 1.5 * rng.unit();
            (side, k, (30.0 + 300.0 * rng.unit()).to_radians())
        })
        .collect()
}

/// The 16 handoff candidates the search of `handoff::search` keeps (indices into `handoffs`), frozen
/// before the first gate run on a law: candidates 0 to 46 were drawn (47), and 2 of them crossed
/// R_SOI 20 times but had a reference that was not converged. The search is chaotic, so it can be
/// re-run only on the same arithmetic; the ignored test in `handoff.rs` re-derives this list.
pub const HANDOFF_KEPT: [usize; 16] = [1, 2, 12, 14, 15, 19, 22, 23, 25, 30, 31, 32, 35, 39, 45, 46];

/// `n` flybys (q, v∞, ψ): periapsis q log-uniform in [1.2, 50] planet radii, v∞ uniform in
/// [1.67e-5, 6.7e-5] (5 to 20 km/s in units of c), the asymptote's direction ψ uniform in [0, 2π).
pub fn flybys(n: usize) -> Vec<(f64, f64, f64)> {
    let mut rng = Rng(ASSIST_SEED);
    (0..n)
        .map(|_| {
            let q = rng.log_uniform(1.2, 50.0);
            (q, 1.67e-5 + (6.7e-5 - 1.67e-5) * rng.unit(), std::f64::consts::TAU * rng.unit())
        })
        .collect()
}

/// `n` moons (a, phase): a uniform in [0.2, 0.9] Hill radii, phase uniform in [0, 2π). Even seeds
/// are prograde, odd seeds retrograde (the caller reads the parity of the index).
pub fn moons(n: usize) -> Vec<(f64, f64)> {
    let mut rng = Rng(HILL_SEED);
    (0..n).map(|_| (0.2 + 0.7 * rng.unit(), std::f64::consts::TAU * rng.unit())).collect()
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
        let radii = clock_radii(64);
        assert_eq!(radii.len(), 64);
        assert!(radii.iter().all(|&r| r > 3.0 && r <= 1e4));
        assert_eq!(clock_radii(8)[..], radii[..8]);
        // Log-uniform on [3, 10^4]: about half fall below the geometric middle, sqrt(3 * 10^4) = 173.
        let low = clock_radii(1024).iter().filter(|&&r| r < 173.2).count();
        assert!((440..584).contains(&low), "{low} of 1024 below r = 173");
        // Log-uniform: about half the draws fall below the geometric middle, sqrt(10 * 1000) = 100.
        let low = a.iter().filter(|&&(p, _)| p < 100.0).count();
        assert!((100..156).contains(&low), "{low} of 256 below p = 100");
    }

    #[test]
    fn the_events_draws_are_deterministic_prefix_stable_and_in_range() {
        let b = binaries(1024);
        assert_eq!(b[..64], binaries(64)[..]);
        assert!(b.iter().all(|&(p, e, nu)| (20.0..=1000.0).contains(&p) && (0.0..0.6).contains(&e) && (0.01..0.25).contains(&nu)));
        let low = b.iter().filter(|&&(p, _, _)| p < 141.5).count(); // sqrt(20 * 1000)
        assert!((440..584).contains(&low), "{low} of 1024 below p = 141");
        let h = handoffs(256);
        assert_eq!(h[..16], handoffs(16)[..]);
        assert!(h.iter().all(|&(side, k, a)| side.abs() == 1.0 && (1.5..=3.0).contains(&k) && (30f64.to_radians()..=330f64.to_radians()).contains(&a)));
        let outside = h.iter().filter(|x| x.0 > 0.0).count();
        assert!((90..166).contains(&outside), "{outside} of 256 outside");
        let f = flybys(64);
        assert!(f.iter().all(|&(q, v, psi)| (1.2..=50.0).contains(&q) && (1.67e-5..=6.7e-5).contains(&v) && (0.0..std::f64::consts::TAU).contains(&psi)));
        let m = moons(128);
        assert!(m.iter().all(|&(a, phase)| (0.2..=0.9).contains(&a) && (0.0..std::f64::consts::TAU).contains(&phase)));
        // The four sets come from four different seeds.
        assert!(b[0].0 != h[0].1 && f[0].2 != m[0].1 && HANDOFF_SEED == BINARY_SEED + 1 && HILL_SEED == ASSIST_SEED + 1);
    }
}
