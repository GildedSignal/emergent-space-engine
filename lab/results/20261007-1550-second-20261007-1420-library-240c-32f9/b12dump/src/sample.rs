//! Verbatim subset of xtask/src/behave/sample.rs (the gate's own sampler): SplitMix64, the
//! handoff draws and the frozen candidate lists. Nothing changed but visibility.
//! Source: xtask@HEAD, lines 5-28 (Rng) and 35,112-135 (handoffs, HANDOFF_KEPT, HANDOFF_INSIDE).

pub struct Rng(pub u64);
impl Rng {
    pub fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
    pub fn unit(&mut self) -> f64 {
        (self.next() >> 11) as f64 / (1u64 << 53) as f64
    }
}

pub const HANDOFF_SEED: u64 = 20261002;

/// `n` handoff candidates (side, k, α). Verbatim.
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

pub const HANDOFF_KEPT: [usize; 16] = [32, 39, 53, 57, 70, 72, 78, 83, 85, 88, 101, 106, 138, 142, 148, 159];

pub const HANDOFF_INSIDE: &[(usize, f64)] = &[(1, 0.91), (2, 0.20), (7, 0.38), (12, 0.03), (14, 0.55), (15, 0.36), (19, 0.56), (22, 0.90), (23, 0.67), (25, 0.60), (30, 0.33), (31, 0.06), (35, 0.25), (44, 0.21), (45, 0.14), (46, 0.01), (49, 0.10), (52, 0.88), (54, 0.28), (56, 0.25), (60, 0.05), (62, 0.13), (65, 0.24), (68, 0.16), (69, 0.40), (79, 0.12), (91, 0.02), (92, 0.70), (93, 0.10), (98, 0.20), (103, 0.32), (110, 0.07), (111, 0.05), (112, 0.35), (118, 0.39), (134, 0.43), (137, 0.89), (140, 0.64), (143, 0.07), (147, 0.85), (150, 0.01), (151, 0.04), (154, 0.12), (158, 0.18)];
