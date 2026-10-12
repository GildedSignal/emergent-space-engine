//! Horizon certificate for a group concentrated in orbital frequency and phase.
//!
//! This is the float research layer, not an integer canonical-law certificate.
//! k is the actual occupancy of a conservative phase window, NEVER an assumed
//! rank of four. Gold measured distance rank at the contact, not phase rank at
//! setup; radial scatter and overtakes can make those different.

use crate::{
    kepler::Body,
    method::{pair_events, Stats},
    tier::{self, ArmStats, Tree, TreeStats},
};
use std::f64::consts::{PI, TAU};

/// Sorted phase plus a horizon-wide exclusion certificate. O(n) storage;
/// sorting costs O(n log n), traversal O(n k), where k is window occupancy.
/// Valid only for these unmodified tubes in [t0,t1]; any kick rebuilds it.
pub struct Neighbours {
    order: Vec<(f64, u32)>,
    pub reach: f64,
    /// Dimensionless swept phase spread / circumference. Below 1/2 the
    /// neighbourhood fits in a semicircle; otherwise use the general tiers.
    pub concentration: f64,
}

impl Neighbours {
    pub fn new(b: &[Body], rho: f64, t0: f64, t1: f64) -> Option<Self> {
        assert!(rho.is_finite() && rho > 0.0 && t0.is_finite() && t1.is_finite() && t1 >= t0);
        assert!(b.len() <= u32::MAX as usize);
        let mut nlo = f64::INFINITY;
        let mut nhi = 0.0_f64;
        let mut centre = 0.0_f64;
        let mut rmin = f64::INFINITY;
        for x in b {
            assert!(x.e >= 0.0 && x.e < 1.0 && x.period > 0);
            nlo = nlo.min(x.n);
            nhi = nhi.max(x.n);
            rmin = rmin.min(x.rmin());
            // |E-M| <= e. tan(f/2) = sqrt((1+e)/(1-e)) tan(E/2)
            // implies max |f-E| = 2 asin(e/(1+sqrt(1-e^2))).
            centre = centre.max(x.e + 2.0 * (x.e / (1.0 + x.sq)).asin());
        }
        // At distance <= rho, radii >= rmin imply angular separation <=
        // 2 asin(rho/(2 rmin)). At a contact, each true longitude differs
        // from its mean longitude by <= centre. Between midpoint and contact,
        // pair mean-longitude separation changes by <= (nhi-nlo)*H/2.
        // Hence every contact's pair is in this midpoint phase window, even
        // across the seam, an overtake, or either horizon edge. No sampling.
        let mut angular = 2.0 * (rho / (2.0 * rmin)).min(1.0).asin();
        // A shared orbit shape has a shared monotone theta -> mean-longitude
        // map. Its equation of centre cancels; paying its amplitude per body
        // would turn an eccentric dense ring quadratic under dilution.
        if let Some(ref_shape) = b.first() {
            if b.iter()
                .all(|x| x.e == ref_shape.e && x.pom == ref_shape.pom)
            {
                // max dM/df = (1+e)^(3/2) / sqrt(1-e), at apoapsis.
                angular *= (1.0 + ref_shape.e).powf(1.5) / (1.0 - ref_shape.e).sqrt();
                centre = 0.0;
            }
        }
        let reach = if b.is_empty() {
            0.0
        } else {
            angular + 2.0 * centre + (nhi - nlo) * (t1 - t0) * 0.5
        };
        // Numerical guard for this research implementation's clock/phase conversion.
        let reach = reach + 64.0 * f64::EPSILON * (1.0 + nhi * t0.abs().max(t1.abs()));
        if !reach.is_finite() || reach >= PI {
            return None;
        }
        let mid = t0 * 0.5 + t1 * 0.5;
        let mut order: Vec<_> = b
            .iter()
            .enumerate()
            .map(|(i, x)| ((x.mean_anomaly(mid) + x.pom).rem_euclid(TAU), i as u32))
            .collect();
        order.sort_by(|a, b| a.0.total_cmp(&b.0).then(a.1.cmp(&b.1)));
        Some(Self {
            order,
            reach,
            concentration: reach / TAU,
        })
    }

    /// Every neighbour once; no quadratic pair list is ever materialized.
    pub fn visit(&self, mut f: impl FnMut(u32, u32)) -> (u64, usize) {
        let n = self.order.len();
        let mut count = 0;
        let mut max_k = 0;
        let mut end = 1;
        for start in 0..n {
            end = end.max(start + 1);
            let phase = self.order[start].0;
            while end < start + n {
                let next = self.order[end % n].0 + if end >= n { TAU } else { 0.0 };
                if next - phase > self.reach {
                    break;
                }
                end += 1;
            }
            max_k = max_k.max(end - start - 1);
            for pos in start + 1..end {
                let (i, j) = (self.order[start].1, self.order[pos % n].1);
                f(i.min(j), i.max(j));
                count += 1;
            }
        }
        (count, max_k)
    }
}

#[derive(Default, Debug)]
pub struct GroupStats {
    pub phase: bool,
    pub concentration: f64,
    pub neighbours: u64,
    pub max_k: usize,
    pub tree: TreeStats,
    pub arm: ArmStats,
    pub exact: Stats,
    pub boundary_checks: u64,
}

/// Interior minima and existing contacts at t0/t1. Boundary contacts have
/// exactly the boundary timestamp, distinct from r8's interior-minimum events.
/// This API is a streaming broad phase: callbacks can consume results without
/// storing the generated pairs/events. No changes to the frozen r8 definition.
pub fn group_events(
    b: &[Body],
    rho: f64,
    t0: f64,
    t1: f64,
    mut emit: impl FnMut(u32, u32, f64, f64),
) -> GroupStats {
    let neighbours = Neighbours::new(b, rho, t0, t1);
    let mut st = GroupStats::default();
    let mut out = Vec::new();
    if let Some(n) = neighbours {
        st.concentration = n.concentration;
        st.phase = true;
        let (count, k) =
            n.visit(|i, j| check_pair(b, i, j, rho, t0, t1, &mut st, &mut out, &mut emit));
        st.neighbours = count;
        st.max_k = k;
    } else {
        let tree = Tree::new(b, 32);
        let mut tree_stats = TreeStats::default();
        tier::traverse(
            &tree,
            b,
            rho,
            true,
            &mut |i, j| check_pair(b, i, j, rho, t0, t1, &mut st, &mut out, &mut emit),
            &mut tree_stats,
        );
        st.tree = tree_stats;
    }
    st
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
        n.visit(|i, j| {
            assert!(i < j && set.insert((i, j)));
        });
        for tick in 0..=400 {
            let t = tick as f64 * 0.05;
            for i in 0..b.len() {
                for j in i + 1..b.len() {
                    let (x, y) = (b[i].state_halley(t), b[j].state_halley(t));
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
        assert_eq!(n.visit(|_, _| {}), (32 * 31 / 2, 31));
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
            let (pairs, k) = cert.visit(|_, _| {});
            println!("GATE phase-scale n={n} neighbours={pairs} max_k={k}");
            assert_eq!(pairs, n as u64);
            assert_eq!(k, 1);
        }
    }
}
