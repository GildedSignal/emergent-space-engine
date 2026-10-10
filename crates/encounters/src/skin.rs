//! A slack skin for one Binet-cone pair. This is the floating-point research tier, not an integer
//! canonical certificate. The existing section/window construction and minimum bracketing remain
//! its regime; a skin does not repair that construction's concentrated/high-eccentricity limits.
//!
//! Store sections for two *unchanged anchor tubes* at rho + slack. Before every query prove a
//! uniform displacement bound d_i + d_j < slack over its horizon. Then triangle inequality gives
//! |x_i(t)-x_j(t)| < rho => |anchor_i(t)-anchor_j(t)| < rho+slack. Thus every current encounter is
//! inside an anchor section's passage window. Its integer rotation is unchanged; check the current
//! tubes inside that interval, at rho, so padding cannot itself report a false encounter.
//!
//! This covers longitude/width drift, period drift and phase-only kicks together. Empty sections
//! also carry slack: their exclusion was made at rho+slack. A long query exhausts phase slack and
//! forces setup before querying. No wake calendar, time stepping, or age-dependent heuristic.

use crate::kepler::Body;
use crate::method::{run_section_on, Stats};
use crate::pairs::{sections, Section};
use std::f64::consts::{PI, TAU};

#[derive(Default, Clone, Copy, Debug)]
pub struct SkinStats {
    /// Includes the first setup. Callers can subtract it to measure kick maintenance alone.
    pub setups: u64,
    pub reused: u64,
    pub setup_evals: u64,
    pub query: Stats,
}

/// Caller owns the pair identity and supplies constructor-produced current tubes after each kick. The radius,
/// safety and slack are immutable; changing any of them requires a new cache. No global state.
pub struct SlackSkin {
    rho: f64,
    slack: f64,
    safety: f64,
    anchor: Option<(Body, Body, Vec<Section>, f64)>,
    last: Option<(Body, Body)>,
}

impl SlackSkin {
    /// A local default: spend one contact radius of positional uncertainty, rather than a
    /// scene-specific Binet width. `new` also permits an explicit nonnegative slack, including
    /// zero for the always-setup control. Wider skins exchange setup cost for query checks.
    pub fn contact_scale(rho: f64, safety: f64) -> Self {
        Self::new(rho, rho, safety)
    }

    pub fn new(rho: f64, slack: f64, safety: f64) -> Self {
        assert!(rho.is_finite() && rho > 0.0);
        assert!(slack.is_finite() && slack >= 0.0 && (rho + slack).is_finite());
        assert!(safety.is_finite() && safety >= 1.0);
        Self {
            rho,
            slack,
            safety,
            anchor: None,
            last: None,
        }
    }

    /// Minima below the physical radius in [t0,t1], deduplicated exactly as `pair_events`.
    /// Setup is lazy, including for newly discovered partners. Candidate discovery is still
    /// `cone_pairs` on the current tubes; this cache never authorizes skipping a partner scan.
    #[allow(clippy::too_many_arguments)]
    pub fn events(&mut self, bi: &Body, bj: &Body, t0: f64, t1: f64, st: &mut SkinStats, out: &mut Vec<(f64, f64)>) {
        assert!(t0.is_finite() && t1.is_finite() && t1 >= t0);
        assert!(valid(bi) && valid(bj), "skin requires finite bound Kepler tubes");
        let reuse = self.anchor.as_ref().is_some_and(|(ai, aj, _, slack)| {
            let bound = displacement_bound(ai, bi, t0, t1) + displacement_bound(aj, bj, t0, t1);
            // Identity is reusable even with slack zero. All nonzero bounds need strict slack.
            bound == 0.0 || bound < *slack
        });
        if reuse {
            st.reused += 1;
        } else {
            // When even one observed change spends the whole budget, padding buys no reuse.
            // Use the unchanged baseline construction at rho in that regime. This is a cost
            // choice only: a zero-slack anchor must be rebuilt on the next nonzero change.
            let step = self.last.as_ref().map_or(0.0, |(li, lj)| {
                displacement_bound(li, bi, t0, t1) + displacement_bound(lj, bj, t0, t1)
            });
            let slack = if step < self.slack { self.slack } else { 0.0 };
            let secs = sections(bi, bj, self.rho + slack, self.safety, &mut st.setup_evals);
            self.anchor = Some((*bi, *bj, secs, slack));
            st.setups += 1;
        }
        self.last = Some((*bi, *bj));
        let start = out.len();
        let (ai, aj, secs, _) = self.anchor.as_ref().unwrap();
        st.query.pairs += 1;
        for sec in secs {
            st.query.sections[sec.kind as usize] += 1;
            run_section_on(ai, aj, bi, bj, sec, self.rho, t0, t1, &mut st.query, out);
        }
        out[start..].sort_by(|x, y| x.0.total_cmp(&y.0));
        let mut keep = start;
        for k in start..out.len() {
            if keep == start || (out[k].0 - out[keep - 1].0).abs() > 1e-7 {
                out[keep] = out[k];
                keep += 1;
            }
        }
        out.truncate(keep);
    }
}

fn valid(b: &Body) -> bool {
    b.a.is_finite()
        && b.a > 0.0
        && b.e.is_finite()
        && (0.0..1.0).contains(&b.e)
        && b.pom.is_finite()
        && b.period > 0
        && b.n.is_finite()
}

fn angle(x: f64) -> f64 {
    (x + PI).rem_euclid(TAU) - PI
}

/// Uniform Euclidean separation bound between two tubes on [t0,t1], not a sampled estimate.
/// With x = Rot(pom) a (cos E-e, sqrt(1-e²) sin E):
/// - |dx/da| <= 1+e_max; |dx/dpom| <= a_max(1+e_max).
/// - At fixed E, |dx/de| <= a_max(1+e_max/sqrt(1-e_max²)).
/// - Kepler's M=E-e sin E has derivative >= 1-e_max, so
///   |delta E| <= (|delta M|+|delta e|)/(1-e_max), and |dx/dE| <= a_max.
/// The unwrapped mean-phase difference is affine in time: the wrapped difference at t0 plus
/// |delta n|*(t1-t0) bounds it everywhere. This includes epoch changes even at identical Binet
/// points. The bound uses endpoints of *parameters*, never trajectory sampling. Triangle
/// inequality combines the terms. Roundoff padding is a research guard, not a directed-rounding
/// proof; integration into the integer law would need authoritative integer/interval bounds.
pub fn displacement_bound(a: &Body, b: &Body, t0: f64, t1: f64) -> f64 {
    assert!(t0.is_finite() && t1.is_finite() && t1 >= t0);
    assert!(valid(a) && valid(b));
    if a.period == b.period && a.tp == b.tp && a.e == b.e && a.pom == b.pom && a.a == b.a && a.n == b.n {
        return 0.0;
    }
    let e = a.e.max(b.e);
    let am = a.a.max(b.a);
    let de = (a.e - b.e).abs();
    // Compute the epoch difference before reducing modulo a period: subtracting large absolute
    // mean anomalies would lose small phase kicks. Integer epoch differences are exact here.
    let phase = angle(
        (a.n - b.n) * t0 - a.n * (a.tp as f64 / crate::kepler::TICKS) + b.n * (b.tp as f64 / crate::kepler::TICKS),
    )
    .abs()
        + (a.n - b.n).abs() * (t1 - t0);
    let bound = (a.a - b.a).abs() * (1.0 + e)
        + am * (1.0 + e) * angle(a.pom - b.pom).abs()
        + am * de * (1.0 + e / (1.0 - e * e).sqrt())
        + am * (phase + de) / (1.0 - e);
    bound * (1.0 + 64.0 * f64::EPSILON) + 64.0 * f64::EPSILON * am * (1.0 + t0.abs() + t1.abs())
}
