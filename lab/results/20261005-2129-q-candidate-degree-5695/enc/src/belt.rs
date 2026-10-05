//! Belts: N bodies in one doll, a uniform in [a_lo, a_hi] (or on `keys` discrete values, so that
//! bodies of one key share an exactly equal integer period), Rayleigh eccentricities, random angles.

use crate::kepler::Body;
use std::f64::consts::TAU;

pub struct Rng(pub u64);

impl Rng {
    pub fn next_u64(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }

    pub fn f64(&mut self) -> f64 {
        (self.next_u64() >> 11) as f64 / 9_007_199_254_740_992.0
    }
}

#[derive(Clone, Debug)]
pub struct Spec {
    pub name: String,
    pub n: usize,
    pub sigma_e: f64,
    pub rho: f64,
    pub a_lo: f64,
    pub a_hi: f64,
    /// 0: continuous a. k > 1: a on k equally spaced values (equal integer periods per key).
    pub keys: usize,
    pub seed: u64,
    /// Horizon in orbits of a = 1 (2 pi time units each).
    pub orbits: f64,
}

pub fn make_belt(s: &Spec) -> Vec<Body> {
    let mut rng = Rng(s.seed);
    (0..s.n)
        .map(|_| {
            let a = if s.keys > 1 {
                let k = (rng.next_u64() % s.keys as u64) as f64;
                s.a_lo + (s.a_hi - s.a_lo) * k / (s.keys - 1) as f64
            } else {
                s.a_lo + (s.a_hi - s.a_lo) * rng.f64()
            };
            let u = rng.f64();
            let e = (s.sigma_e * (-2.0 * (1.0 - u).ln()).sqrt()).min(0.5);
            let pom = TAU * rng.f64();
            let lam = TAU * rng.f64();
            Body::new(a, e, pom, lam)
        })
        .collect()
}
