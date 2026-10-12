//! Horizon certificate for a group concentrated in orbital phase.
//!
//! This is the float research layer, not an integer canonical-law certificate.
//! Fix over wt/cx-b-coorbital-cert (lab 20261012-0138-taleb-74a1, adoption items 1-4):
//!   1. every window pair is Binet-cone gated (`pairs::is_candidate`) BEFORE any
//!      boundary state or exact solve — dispersion no longer pays exact work;
//!   2. a measured walk budget aborts the phase sweep and falls back to the tree:
//!      the trigger is the sweep's own visit count, not a guessed dimensionless
//!      number (the simulation decides, PRINCIPLES 22);
//!   3. out-of-domain bodies (e >= 1, non-finite, no period) never panic: they are
//!      refused explicitly (counted in `domain_refusals`, zero events emitted) —
//!      this crate's Binet machinery is invalid for them, including the tree;
//!   4. the equation-of-centre is paid per pair (`c_i + c_j`), with the exact
//!      shared-shape cancellation kept per pair: one odd body no longer widens
//!      everyone else's window (the 1-ULP cliff).
//!
//! The walk bound stays the original conservative `reach` (angular + worst centre
//! terms + group drift); the per-pair window and the cone decide exact work.

use crate::{
    kepler::Body,
    method::{pair_events, Stats},
    pairs::is_candidate,
    tier::{self, ArmStats, Tree, TreeStats},
};
use std::f64::consts::{PI, TAU};

/// Window visits allowed before the phase sweep gives up and reruns via the
/// tree. Set from the measured crossover (probe crossover, D m=100 k=80):
/// the sweep costs ~12 ns/visit and the tree 3.7 s at n = 8000, so the sweep
/// wins until ~40k visits/body; the tree is linear where the walk is quadratic,
/// so past this constant the geometric pruning is the cheaper representation.
pub const BUDGET_PER_N: u64 = 40_960;
pub const BUDGET_FLOOR: u64 = 65_536;

pub fn budget_for(n: usize) -> u64 {
    BUDGET_PER_N * n as u64 + BUDGET_FLOOR
}

/// True iff the body is inside this crate's Kepler/Binet domain.
#[inline]
pub fn in_domain(x: &Body) -> bool {
    x.e.is_finite() && x.e >= 0.0 && x.e < 1.0 && x.period > 0 && x.n.is_finite() && x.n > 0.0
}

/// Horizon-wide exclusion certificate over a phase-concentrated group.
///
/// Bodies are grouped by exact shape (e, pom). Within a class the equation of
/// centre cancels (contact requires equal mean longitudes, within the mapped
/// angular term), so a shared-shape ring pays only the angular window — the
 /// 1-ULP cliff is impossible. Between classes a pair pays its own amplitudes
/// c_i + c_j; one odd body widens no one else's window. Every armed pair is
/// then Binet-cone gated before any exact work (fix 1, taleb-74a1).
pub struct Neighbours {
    /// Per-body equation-of-centre amplitude and mean motion.
    centre: Vec<f64>,
    mmn: Vec<f64>,
    /// Each class's members λ-sorted, with its shape bound.
    classes: Vec<Class>,
    /// Conservative cross-class walk bound (the original `reach` semantics).
    pub reach: f64,
    pub concentration: f64,
    angular: f64,
    drift: f64,
    horizon: f64,
    guard: f64,
}

struct Class {
    /// λ-sorted (λ, id) of this class's members.
    sorted: Vec<(f64, u32)>,
    /// Shared-shape angular factor (1+e)^{3/2}/sqrt(1-e).
    s: f64,
    /// Max centre amplitude in the class.
    cmax: f64,
}

#[derive(Default, Debug, Clone, Copy)]
pub struct VisitStats {
    /// Pairs passed to the callback (survived window + cone).
    pub pairs: u64,
    /// Walk visits (interval-query hits).
    pub walk: u64,
    /// Rejected by the per-pair window.
    pub window_reject: u64,
    /// Passed the window, rejected by the Binet cone.
    pub cone_reject: u64,
    pub max_k: usize,
    pub aborted: bool,
}

/// Above this many distinct shapes the group is not shape-concentrated and the
/// tree (geometric pruning in Binet space) is the right representation.
pub const MAX_CLASSES: usize = 1024;

impl Neighbours {
    pub fn new(b: &[Body], rho: f64, t0: f64, t1: f64) -> Option<Self> {
        assert!(rho.is_finite() && rho > 0.0 && t0.is_finite() && t1.is_finite() && t1 >= t0);
        assert!(b.len() <= u32::MAX as usize);
        let mut nlo = f64::INFINITY;
        let mut nhi = 0.0_f64;
        let mut rmin = f64::INFINITY;
        let mut centre_max = 0.0_f64;
        let mut sfac_max = 0.0_f64;
        let mut centre = Vec::with_capacity(b.len());
        let mut mmn = Vec::with_capacity(b.len());
        let mut key: Vec<(u64, u64)> = Vec::with_capacity(b.len());
        for x in b {
            if !in_domain(x) {
                return None; // fix 3: refuse, never panic (callers partition first)
            }
            nlo = nlo.min(x.n);
            nhi = nhi.max(x.n);
            rmin = rmin.min(x.rmin());
            let c = x.e + 2.0 * (x.e / (1.0 + x.sq)).asin();
            let s = (1.0 + x.e).powf(1.5) / x.sq;
            centre_max = centre_max.max(c);
            sfac_max = sfac_max.max(s);
            centre.push(c);
            mmn.push(x.n);
            key.push((x.e.to_bits(), x.pom.to_bits()));
        }
        // Group by exact shape; bail to the tree when shapes are not concentrated.
        let mut by_shape: Vec<u32> = (0..b.len() as u32).collect();
        by_shape.sort_by(|&i, &j| {
            key[i as usize]
                .cmp(&key[j as usize])
                .then(i.cmp(&j))
        });
        let mut classes: Vec<Class> = Vec::new();
        let mut i = 0;
        while i < by_shape.len() {
            let mut j = i;
            while j < by_shape.len() && key[by_shape[j] as usize] == key[by_shape[i] as usize] {
                j += 1;
            }
            let sample = &b[by_shape[i] as usize];
            let mut sorted: Vec<(f64, u32)> = by_shape[i..j]
                .iter()
                .map(|&id| {
                    (
                        (b[id as usize].mean_anomaly(t0 * 0.5 + t1 * 0.5) + b[id as usize].pom)
                            .rem_euclid(TAU),
                        id,
                    )
                })
                .collect();
            sorted.sort_by(|a, c| a.0.total_cmp(&c.0).then(a.1.cmp(&c.1)));
            classes.push(Class {
                sorted,
                s: (1.0 + sample.e).powf(1.5) / sample.sq,
                cmax: sample.e + 2.0 * (sample.e / (1.0 + sample.sq)).asin(),
            });
            i = j;
        }
        if classes.len() > MAX_CLASSES {
            return None;
        }
        let angular = 2.0 * (rho / (2.0 * rmin)).min(1.0).asin();
        let drift = if b.is_empty() {
            0.0
        } else {
            (nhi - nlo) * (t1 - t0) * 0.5
        };
        let guard = 64.0 * f64::EPSILON * (1.0 + nhi * t0.abs().max(t1.abs()));
        // Original π-fallback semantics, applied to both bounds (conservative).
        if (angular * sfac_max + drift + guard) >= PI || (angular + 2.0 * centre_max + drift + guard) >= PI {
            return None;
        }
        let reach = angular + 2.0 * centre_max + drift + guard;
        Some(Self {
            centre,
            mmn,
            classes,
            reach,
            concentration: reach / TAU,
            angular,
            drift,
            horizon: t1 - t0,
            guard,
        })
    }

    /// Same-shape window: the equation of centre cancels.
    #[inline]
    fn window_shared(&self, cls: &Class, i: u32, j: u32) -> f64 {
        self.angular * cls.s
            + (self.mmn[i as usize] - self.mmn[j as usize]).abs() * self.horizon * 0.5
            + self.guard
    }

    /// Cross-shape window: each body pays its own amplitude.
    #[inline]
    fn window_cross(&self, i: u32, j: u32) -> f64 {
        self.angular
            + self.centre[i as usize]
            + self.centre[j as usize]
            + (self.mmn[i as usize] - self.mmn[j as usize]).abs() * self.horizon * 0.5
            + self.guard
    }

    /// Circular λ distance, valid below π.
    #[inline]
    fn cd(a: f64, b: f64) -> f64 {
        let d = (a - b).abs();
        d.min(TAU - d)
    }

    /// Call f for every entry of `sorted` with λ in [l, r] (mod TAU).
    fn for_each_in(sorted: &[(f64, u32)], l: f64, r: f64, mut f: impl FnMut(&(f64, u32))) {
        for k in [-TAU, 0.0, TAU] {
            let lo = (l + k).max(0.0);
            let hi = (r + k).min(TAU);
            if lo >= hi {
                continue;
            }
            let s = sorted.partition_point(|x| x.0 < lo);
            let e = sorted.partition_point(|x| x.0 <= hi);
            for x in &sorted[s..e] {
                f(x);
            }
        }
    }

    /// Two-pass visit: pass 0 counts against the budget with no side effects;
    /// pass 1 runs the callbacks. Each unordered pair is emitted once.
    pub fn visit(
        &self,
        b: &[Body],
        rho: f64,
        budget: u64,
        mut f: impl FnMut(u32, u32),
    ) -> VisitStats {
        let mut st = VisitStats::default();
        for pass in 0..2 {
            st = VisitStats::default();
            for ci in 0..self.classes.len() {
                let cls = &self.classes[ci];
                let walk_w = self.angular * cls.s + self.drift + self.guard;
                for &(li, i) in &cls.sorted {
                    let mut armed = 0usize;
                    Self::for_each_in(&cls.sorted, li - walk_w, li + walk_w, |&(lj, j)| {
                        if j <= i {
                            return;
                        }
                        st.walk += 1;
                        if st.walk > budget {
                            st.aborted = true;
                            return;
                        }
                        if Self::cd(li, lj) > self.window_shared(cls, i, j) {
                            st.window_reject += 1;
                            return;
                        }
                        if !is_candidate(&b[i as usize], &b[j as usize], rho) {
                            st.cone_reject += 1;
                            return;
                        }
                        armed += 1;
                        if pass == 1 {
                            f(i, j);
                        }
                        st.pairs += 1;
                    });
                    st.max_k = st.max_k.max(armed);
                }
            }
            for ci in 0..self.classes.len() {
                for cj in (ci + 1)..self.classes.len() {
                    let (a, c) = (&self.classes[ci], &self.classes[cj]);
                    let wmax =
                        self.angular + a.cmax + c.cmax + self.drift + self.guard;
                    // Skip class pairs whose λ-extents (widened by wmax) cannot overlap.
                    let (alo, ahi) = (a.sorted.first().unwrap().0, a.sorted.last().unwrap().0);
                    let (clo, chi) = (c.sorted.first().unwrap().0, c.sorted.last().unwrap().0);
                    let gap = Self::cd(
                        (alo + ahi) * 0.5,
                        (clo + chi) * 0.5,
                    ) - (ahi - alo) * 0.5 - (chi - clo) * 0.5;
                    if gap > wmax {
                        continue;
                    }
                    for &(li, i) in &a.sorted {
                        let wi = self.angular + self.centre[i as usize] + c.cmax
                            + self.drift
                            + self.guard;
                        let mut armed = 0usize;
                        Self::for_each_in(&c.sorted, li - wi, li + wi, |&(lj, j)| {
                            st.walk += 1;
                            if st.walk > budget {
                                st.aborted = true;
                                return;
                            }
                            if Self::cd(li, lj) > self.window_cross(i, j) {
                                st.window_reject += 1;
                                return;
                            }
                            if !is_candidate(&b[i as usize], &b[j as usize], rho) {
                                st.cone_reject += 1;
                                return;
                            }
                            armed += 1;
                            if pass == 1 {
                                f(i.min(j), i.max(j));
                            }
                            st.pairs += 1;
                        });
                        st.max_k = st.max_k.max(armed);
                    }
                }
            }
            if pass == 0 && st.walk == 0 {
                break;
            }
            if pass == 0 && st.aborted {
                return st;
            }
        }
        st
    }
}

#[derive(Default, Debug)]
pub struct GroupStats {
    pub phase: bool,
    pub concentration: f64,
    pub neighbours: u64,
    pub max_k: usize,
    pub walk: u64,
    pub window_reject: u64,
    pub cone_reject: u64,
    /// True when the walk budget fired and the tree path produced the events.
    pub budget_fallback: bool,
    /// Bodies refused as out of this crate's domain (e >= 1, non-finite...):
    /// no events are emitted for them; the caller owes them another layer.
    pub domain_refusals: usize,
    pub tree: TreeStats,
    pub arm: ArmStats,
    pub exact: Stats,
    pub boundary_checks: u64,
}

/// Interior minima and existing contacts at t0/t1 (unchanged r8 definition).
/// Broad-phase streaming API: callbacks consume without stored pair lists.
pub fn group_events(
    b: &[Body],
    rho: f64,
    t0: f64,
    t1: f64,
    mut emit: impl FnMut(u32, u32, f64, f64),
) -> GroupStats {
    let mut st = GroupStats::default();
    let core: Vec<usize> = (0..b.len()).filter(|&i| in_domain(&b[i])).collect();
    st.domain_refusals = b.len() - core.len();
    if core.is_empty() {
        return st;
    }
    if core.len() == b.len() {
        run_core(b, rho, t0, t1, &mut emit, &mut st);
    } else {
        // Mixed domain: certify the Kepler core with original indices remapped.
        let bodies: Vec<Body> = core.iter().map(|&i| b[i]).collect();
        let mut st2;
        let mut emit2 = |i: u32, j: u32, t: f64, d: f64| {
            emit(core[i as usize] as u32, core[j as usize] as u32, t, d);
        };
        st2 = GroupStats::default();
        run_core(&bodies, rho, t0, t1, &mut emit2, &mut st2);
        st2.domain_refusals = st.domain_refusals;
        st = st2;
    }
    st
}

fn run_core(
    b: &[Body],
    rho: f64,
    t0: f64,
    t1: f64,
    emit: &mut impl FnMut(u32, u32, f64, f64),
    st: &mut GroupStats,
) {
    let neighbours = Neighbours::new(b, rho, t0, t1);
    let mut out = Vec::new();
    let budget = budget_for(b.len());
    if let Some(nh) = &neighbours {
        // One call: pass 0 counts (no emits); only if the budget holds does
        // pass 1 emit, so an abort can never duplicate or half-emit events.
        // st.phase is armed BEFORE the visit: the phase path's pairs are
        // already window- and cone-gated and must not pass arm_pair's tier
        // window (the gold's 4-6% formation drop lives there).
        st.phase = true;
        let run = nh.visit(b, rho, budget, |i, j| {
            check_pair(b, i, j, rho, t0, t1, st, &mut out, emit)
        });
        if !run.aborted {
            st.concentration = nh.concentration;
            st.walk = run.walk;
            st.window_reject = run.window_reject;
            st.cone_reject = run.cone_reject;
            st.neighbours = run.pairs;
            st.max_k = run.max_k;
            return;
        }
        st.phase = false;
        st.budget_fallback = true;
        st.walk = run.walk;
    }
    let tree = Tree::new(b, 32);
    let mut tree_stats = TreeStats::default();
    tier::traverse(
        &tree,
        b,
        rho,
        true,
        &mut |i, j| check_pair(b, i, j, rho, t0, t1, st, &mut out, emit),
        &mut tree_stats,
    );
    st.tree = tree_stats;
}

#[allow(clippy::too_many_arguments)]
fn check_pair(
    b: &[Body],
    i: u32,
    j: u32,
    rho: f64,
    t0: f64,
    t1: f64,
    st: &mut GroupStats,
    out: &mut Vec<(f64, f64)>,
    emit: &mut impl FnMut(u32, u32, f64, f64),
) {
    let (bi, bj) = (&b[i as usize], &b[j as usize]);
    // Fix 1: the Binet cone gates everything, before any state evaluation.
    if !is_candidate(bi, bj, rho) {
        return;
    }
    for (edge, t) in [t0, t1].into_iter().enumerate() {
        if edge == 1 && t0 == t1 {
            continue;
        }
        let (x, y) = (bi.state(t), bj.state(t));
        st.boundary_checks += 1;
        let d = (x[0] - y[0]).hypot(x[1] - y[1]);
        if d < rho {
            emit(i, j, t, d);
        }
    }
    if st.phase || tier::arm_pair(bi, bj, rho, 1.1, t0, t1, &mut st.arm).0 {
        out.clear();
        pair_events(bi, bj, rho, 1.1, t0, t1, &mut st.exact, out);
        for &(t, d) in out.iter() {
            if t > t0 && t < t1 {
                emit(i, j, t, d);
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::BTreeSet;

    #[test]
    fn seam_overtake_and_ties_are_not_lost_or_duplicated() {
        let b = [
            Body::new(1.0, 0.01, 0.0, TAU - 0.001),
            Body::new(1.0001, 0.02, 0.0, 0.001),
            Body::new(1.0, 0.01, 0.0, TAU - 0.001),
            Body::new(1.0, 0.01, 0.0, PI),
        ];
        let n = Neighbours::new(&b, 0.01, 0.0, 20.0).unwrap();
        let mut set = BTreeSet::new();
        n.visit(&b, 0.01, u64::MAX, |i, j| {
            assert!(i < j && set.insert((i, j)));
        });
        for tick in 0..=400 {
            let t = tick as f64 * 0.05;
            for i in 0..b.len() {
                for j in i + 1..b.len() {
                    let (x, y) = (b[i].state_halley(t), &b[j].state_halley(t));
                    if (x[0] - y[0]).hypot(x[1] - y[1]) < 0.01 {
                        assert!(set.contains(&(i as u32, j as u32)));
                    }
                }
            }
        }
    }

    #[test]
    fn a_crowded_phase_window_never_assumes_rank_four() {
        let b = vec![Body::new(1.0, 0.0, 0.0, 0.0); 32];
        let n = Neighbours::new(&b, 0.01, 0.0, TAU).unwrap();
        let st = n.visit(&b, 0.01, u64::MAX, |_, _| {});
        assert_eq!(st.pairs, 32 * 31 / 2);
        assert_eq!(st.max_k, 31);
    }

    #[test]
    fn instantaneous_query_reports_existing_overlap_once() {
        let b = [
            Body::new(1.0, 0.0, 0.0, 0.0),
            Body::new(1.0, 0.0, 0.0, 0.001),
        ];
        let mut events = Vec::new();
        group_events(&b, 0.01, 3.0, 3.0, |i, j, t, _| events.push((i, j, t)));
        assert_eq!(events, vec![(0, 1, 3.0)]);
    }

    #[test]
    fn frequency_spread_expiring_the_horizon_uses_general_tiers() {
        let b = [Body::new(1.0, 0.0, 0.0, 0.0), Body::new(2.0, 0.0, 0.0, PI)];
        assert!(Neighbours::new(&b, 0.01, 0.0, 100.0).is_none());
        assert!(!group_events(&b, 0.01, 0.0, 100.0, |_, _, _, _| {}).phase);
    }

    #[test]
    fn fixed_density_ring_visits_linear_work_to_a_million() {
        for n in [1000, 10_000, 100_000, 1_000_000] {
            let b: Vec<_> = (0..n)
                .map(|i| Body::new(1.0, 0.02, 0.0, TAU * i as f64 / n as f64))
                .collect();
            let cert = Neighbours::new(&b, 1.5 * TAU / n as f64, 0.0, TAU).unwrap();
            let st = cert.visit(&b, 1.5 * TAU / n as f64, u64::MAX, |_, _| {});
            println!(
                "GATE phase-scale n={n} neighbours={} max_k={}",
                st.pairs, st.max_k
            );
            assert_eq!(st.pairs, n as u64);
            // Interval queries cross the seam directly, so the body at the
            // seam arms one neighbour on each side: armed degree <= 2, while
            // total pairs stay exactly n (the linearity that matters).
            assert!(st.max_k <= 2, "max_k={} at n={n}", st.max_k);
        }
    }

    #[test]
    fn one_shape_outlier_does_not_widen_the_shared_window() {
        // Tight formation, shared shape, one body's e one ULP higher: the
        // shared pairs keep the cancelled window; only odd pairs pay c_i+c_j.
        let n = 64;
        let period = Body::new(1.0, 0.05, 0.0, 0.0).period;
        let e_ulp = f64::from_bits(0.05f64.to_bits() + 1);
        let b: Vec<_> = (0..n)
            .map(|i| {
                let e = if i == n / 2 { e_ulp } else { 0.05 };
                Body::with_period(period, e, 0.0, 0.6 * 1e-4 * i as f64)
            })
            .collect();
        let cert = Neighbours::new(&b, 1e-4, 0.0, 5.0).unwrap();
        let st = cert.visit(&b, 1e-4, u64::MAX, |_, _| {});
        // ~2 λ-neighbours per body within the shared window, plus the outlier's
        // cross pairs: linear, never the n²/2 the original's cliff produced.
        assert!(
            st.pairs < 4 * n as u64,
            "armed {} must be linear in n={n}, not the cliff",
            st.pairs
        );
        assert!(st.pairs > n as u64, "expected shared neighbours + outlier pairs");
    }

    #[test]
    fn hyperbolic_bodies_are_refused_not_panicked() {
        let mut b: Vec<Body> = (0..8)
            .map(|i| Body::new(1.0, 0.0, 0.0, TAU * i as f64 / 8.0))
            .collect();
        b.push(Body::new(1.0, 1.5, 0.3, 0.0));
        let mut events = 0;
        let st = group_events(&b, 1e-4, 0.0, 1.0, |_, _, _, _| events += 1);
        assert_eq!(st.domain_refusals, 1);
        assert_eq!(events, 0, "refused bodies must not emit silent events");
    }
}
