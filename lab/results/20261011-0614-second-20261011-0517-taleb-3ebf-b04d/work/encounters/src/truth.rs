//! The truth without the leak: every radially overlapping pair, dense in time, by rigorous
//! conservative advancement. A coarse step is taken only if a lower bound proves the distance stays
//! above 1.5ρ over the whole step:
//!   d(τ) ≥ min_[0,h] |Δr + Δv τ| − |R|,  |R| ≤ A h²/2  (A = |a_i|max + |a_j|max), or, while
//!   |Δr| ≤ d_cap, |R| ≤ U(h) − d₀ − v₀h with U = d₀ cosh ωh + (v₀/ω) sinh ωh, ω² = 2/r_seg³ (the tidal
//!   Lipschitz bound of the Kepler field along the segment joining the bodies; Gronwall comparison).
//! Within 2ρ the pair is sampled finely (Δ ≤ ρ/4 of relative motion per step) and every local minimum
//! of the distance is bracketed by a sign change of Δr·Δv and refined. States use Halley's iteration,
//! the method uses Newton's: no shared solver path.

use crate::kepler::{rel, Body};
use crate::pairs::{dot, norm, refine};

#[derive(Default, Clone, Copy, Debug)]
pub struct TruthStats {
    pub steps: u64,
    pub fine: u64,
    pub evals: u64,
}

impl TruthStats {
    pub fn add(&mut self, o: &TruthStats) {
        self.steps += o.steps;
        self.fine += o.fine;
        self.evals += o.evals;
    }
}

#[allow(clippy::too_many_arguments)]
fn safe_step(r: [f64; 2], v: [f64; 2], a_glob: f64, om: f64, dcap: f64, target: f64, hcap: f64) -> f64 {
    let d0 = norm(r);
    let v0 = norm(v);
    let rv = dot(r, v);
    let vv = dot(v, v);
    let lb = |h: f64| -> f64 {
        let tau = if vv > 0.0 { (-rv / vv).clamp(0.0, h) } else { 0.0 };
        let ml = norm([r[0] + v[0] * tau, r[1] + v[1] * tau]);
        let lb1 = ml - 0.5 * a_glob * h * h;
        let x = om * h;
        let u = d0 * x.cosh() + (v0 / om) * x.sinh();
        let lb2 = if u <= dcap { ml - (u - d0 - v0 * h) } else { f64::NEG_INFINITY };
        lb1.max(lb2)
    };
    let mut h = hcap;
    while lb(h) < target && h > 1e-13 {
        h *= 0.5;
    }
    let (mut lo, mut hi) = (h, (2.0 * h).min(hcap));
    if hi > lo {
        for _ in 0..4 {
            let mid = 0.5 * (lo + hi);
            if lb(mid) >= target {
                lo = mid;
            } else {
                hi = mid;
            }
        }
    }
    lo.max(1e-13)
}

/// Every local minimum of the pair's distance below ρ in (0, t_end).
pub fn truth_pair(bi: &Body, bj: &Body, rho: f64, t_end: f64, out: &mut Vec<(f64, f64)>, st: &mut TruthStats) {
    let rmin = bi.rmin().min(bj.rmin());
    let a_glob = 1.0 / (bi.rmin() * bi.rmin()) + 1.0 / (bj.rmin() * bj.rmin());
    let dcap = 0.5f64.min(rmin);
    let rseg = (rmin * rmin - 0.25 * dcap * dcap).sqrt();
    let om = (2.0 / (rseg * rseg * rseg)).sqrt();
    let mut t = 0.0;
    let (mut r, mut v, _) = rel(bi, bj, t, true);
    st.evals += 1;
    let mut g = dot(r, v);
    while t < t_end {
        let d = norm(r);
        let tn = if d > 2.0 * rho {
            st.steps += 1;
            t + safe_step(r, v, a_glob, om, dcap, 1.5 * rho, 1.0)
        } else {
            st.steps += 1;
            st.fine += 1;
            t + (0.25 * rho / norm(v).max(1e-12)).min(0.05)
        };
        let (rn, vn, _) = rel(bi, bj, tn, true);
        st.evals += 1;
        let gn = dot(rn, vn);
        if d <= 2.0 * rho && g < 0.0 && gn >= 0.0 {
            let (tm, dm) = refine(bi, bj, t, tn, true, &mut st.evals);
            if dm < rho && tm > 0.0 && tm < t_end {
                out.push((tm, dm));
            }
        }
        t = tn;
        r = rn;
        v = vn;
        g = gn;
    }
}
