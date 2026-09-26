//! Forecasts: kinetic-theory cost per chronon, an online fit to measured ops, the ops→time
//! calibration and the sabotage switch. Forecasts only order and size work; the invariance
//! tests run them multiplied by random factors in [0.1, 10] and demand identical digests.
use crate::geom::Aabb;
use emergent_lattice::law::Body;
use emergent_lattice::worlds::Rng;
use serde::Serialize;

/// A region's aggregate state for the cost forecast (Asimov: forecast masses, not individuals).
#[derive(Clone, Copy, Debug, Default, Serialize)]
pub struct Features {
    pub n: f64,
    /// Expected contacts per chronon, ½·n²·σ·v̄_rel / area.
    pub lambda: f64,
}

/// Kinetic theory in 2D: σ is the diameter of the reach disc (2·(r_a + r_b) ≈ 4·r̄), v̄_rel ≈
/// √2·v_rms for isotropic velocities, area the region's box (never below the bodies' own
/// footprint). Positions and speeds share the 1/Q unit, so λ is per chronon.
pub fn kinetic(bodies: &[Body], bbox: &Aabb) -> Features {
    let n = bodies.len() as f64;
    if bodies.len() < 2 || bbox.is_empty() {
        return Features { n, lambda: 0.0 };
    }
    let r = bodies.iter().map(|b| b.radius as f64).sum::<f64>() / n;
    let v2 = bodies.iter().map(|b| (b.k[0] as f64).powi(2) + (b.k[1] as f64).powi(2)).sum::<f64>() / n;
    let side = |c: usize| (bbox.hi[c] - bbox.lo[c]) as f64 + 2.0 * r;
    let area = (side(0) * side(1)).max(n * (2.0 * r).powi(2));
    Features { n, lambda: 0.5 * n * n * 4.0 * r * (2.0 * v2).sqrt() / area }
}

/// ops per chronon ≈ k0·n + k1·λ, fitted online by recursive least squares with forgetting,
/// so the forecast tracks whichever stepper (chronon grid, event core, Metal) is plugged in.
/// The fit runs per body (y/n on [1, λ/n]): raw features span n² ~ 10^7 and made RLS lose
/// positive definiteness to cancellation (measured: k diverged to 10^26 on a 4,000-body region).
#[derive(Clone, Debug, Serialize)]
pub struct CostModel {
    pub k: [f64; 2],
    p: [[f64; 2]; 2],
}

impl Default for CostModel {
    fn default() -> Self {
        // Prior: the chronon grid touches each body about three times per chronon.
        CostModel { k: [3.0, 8.0], p: [[1.0, 0.0], [0.0, 1.0]] }
    }
}

impl CostModel {
    const FORGET: f64 = 0.995;

    pub fn predict(&self, f: &Features) -> f64 {
        (self.k[0] * f.n + self.k[1] * f.lambda).max(1.0)
    }

    pub fn learn(&mut self, f: &Features, ops_per_chronon: f64) {
        let n = f.n.max(1.0);
        let (x, y) = ([1.0, f.lambda / n], ops_per_chronon / n);
        let px = [self.p[0][0] * x[0] + self.p[0][1] * x[1], self.p[1][0] * x[0] + self.p[1][1] * x[1]];
        let den = Self::FORGET + x[0] * px[0] + x[1] * px[1];
        if !(den.is_finite() && den > 0.0 && y.is_finite()) {
            return;
        }
        let g = [px[0] / den, px[1] / den];
        let e = y - (self.k[0] * x[0] + self.k[1] * x[1]);
        for i in 0..2 {
            self.k[i] = (self.k[i] + g[i] * e).max(0.0);
            for j in 0..2 {
                self.p[i][j] = (self.p[i][j] - g[i] * px[j]) / Self::FORGET;
            }
        }
        // Keep P symmetric positive definite and bounded (no excitation makes it grow as 1/forget^t).
        let off = 0.5 * (self.p[0][1] + self.p[1][0]);
        self.p[0][1] = off;
        self.p[1][0] = off;
        let (tr, det) = (self.p[0][0] + self.p[1][1], self.p[0][0] * self.p[1][1] - off * off);
        if !(tr.is_finite() && tr < 1e6 && det > 0.0 && self.p[0][0] > 0.0) {
            self.p = [[1.0, 0.0], [0.0, 1.0]];
        }
    }
}

/// Log-uniform factor in [0.1, 10] per forecast.
pub struct Sabotage(pub Rng);

impl Sabotage {
    pub fn factor(&mut self) -> f64 {
        let u = (self.0.next() >> 11) as f64 / (1u64 << 53) as f64;
        10f64.powf(2.0 * u - 1.0)
    }
}
