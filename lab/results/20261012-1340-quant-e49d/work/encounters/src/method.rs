//! The Diophantine method: per candidate pair, its sections; per section, jump straight to the next
//! passage whose offset lies in the window (exact integer first-hit), check it exactly, repeat.
//! Nothing is evaluated at passages outside the window.

use crate::dioph::first_hit;
use crate::kepler::{Body, TICKS};
use crate::pairs::{check, sections, Kind, Section};

#[derive(Default, Clone, Copy, Debug)]
pub struct Stats {
    pub pairs: u64,
    pub sections: [u64; 3],
    pub queries: u64,
    pub qsteps: u64,
    /// Exact checks (proposed passages) and minima below ρ found, by section kind.
    pub checks: [u64; 3],
    pub hits: [u64; 3],
    pub evals: u64,
    /// Largest |s| / window half-width among Cross passages that held an encounter (the margin the
    /// linear window keeps; 1/safety if the linear model were exact).
    pub max_util_cross: f64,
}

impl Stats {
    pub fn add(&mut self, o: &Stats) {
        self.pairs += o.pairs;
        self.queries += o.queries;
        self.qsteps += o.qsteps;
        self.evals += o.evals;
        self.max_util_cross = self.max_util_cross.max(o.max_util_cross);
        for k in 0..3 {
            self.sections[k] += o.sections[k];
            self.checks[k] += o.checks[k];
            self.hits[k] += o.hits[k];
        }
    }
    pub fn checks_total(&self) -> u64 {
        self.checks.iter().sum()
    }
    pub fn hits_total(&self) -> u64 {
        self.hits.iter().sum()
    }
}

/// All minima below ρ of pair (bi, bj) with time in [t0, t1] (time units), deduplicated.
#[allow(clippy::too_many_arguments)]
pub fn pair_events(bi: &Body, bj: &Body, rho: f64, safety: f64, t0: f64, t1: f64, st: &mut Stats, out: &mut Vec<(f64, f64)>) {
    st.pairs += 1;
    let start = out.len();
    for sec in sections(bi, bj, rho, safety, &mut st.evals) {
        st.sections[sec.kind as usize] += 1;
        run_section(bi, bj, &sec, rho, t0, t1, st, out);
    }
    let tail = &mut out[start..];
    tail.sort_by(|x, y| x.0.total_cmp(&y.0));
    let mut keep = start;
    for k in start..out.len() {
        if keep == start || (out[k].0 - out[keep - 1].0).abs() > 1e-7 {
            out[keep] = out[k];
            keep += 1;
        }
    }
    out.truncate(keep);
}

#[allow(clippy::too_many_arguments)]
pub fn run_section(bi: &Body, bj: &Body, sec: &Section, rho: f64, t0: f64, t1: f64, st: &mut Stats, out: &mut Vec<(f64, f64)>) {
    let ti = sec.ti as i128;
    let tj = sec.tj as i128;
    let pi = bi.period as i128;
    let pj = bj.period as i128;
    let ext = ((sec.dj.0.max(sec.dj.1) + sec.di.0.max(sec.di.1)) * TICKS) as i128 + pj;
    let t0t = (t0 * TICKS) as i128;
    let t1t = (t1 * TICKS) as i128;
    let base = tj + (t0t - ext - tj).div_euclid(pj) * pj;
    let lmax = (t1t + ext - base).div_euclid(pj);
    let w1 = sec.w1 as i128;
    let w = (w1 + sec.w2 as i128).clamp(0, pi - 1);
    let c0 = (ti - base + w1).rem_euclid(pi);
    let d = (pi - pj.rem_euclid(pi)).rem_euclid(pi);
    let kind = sec.kind as usize;
    let mut l: i128 = 0;
    let mut found = Vec::new();
    loop {
        let c = (c0 - l * pj).rem_euclid(pi);
        st.queries += 1;
        let k = match first_hit(c as u128, d as u128, pi as u128, 0, w as u128, &mut st.qsteps) {
            None => break,
            Some(k) => k as i128,
        };
        l += k;
        if l > lmax {
            break;
        }
        let s = ((c0 - l * pj).rem_euclid(pi) - w1) as f64 / TICKS;
        let tjc = (base + l * pj) as f64 / TICKS;
        st.checks[kind] += 1;
        found.clear();
        check(bi, bj, sec, tjc, s, rho, &mut found, &mut st.evals);
        for &(t, dm) in &found {
            if t >= t0 && t <= t1 {
                out.push((t, dm));
                st.hits[kind] += 1;
                if sec.kind == Kind::Cross {
                    let w = if s < 0.0 { sec.w1 } else { sec.w2 } as f64;
                    st.max_util_cross = st.max_util_cross.max((s * TICKS).abs() / w);
                }
            }
        }
        l += 1;
    }
}

/// Section kind names, for reports.
pub fn kind_name(k: Kind) -> &'static str {
    match k {
        Kind::Cross => "cross",
        Kind::Wide => "wide",
        Kind::Full => "full",
    }
}
