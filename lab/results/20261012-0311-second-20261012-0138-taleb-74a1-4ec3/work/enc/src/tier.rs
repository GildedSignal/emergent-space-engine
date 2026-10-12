//! The tiered candidate structure: envelopes above the pair, cheap exact arming below.
//!
//! Tier 1 (geometry, static between kicks): a balanced tree over the U-sorted order. Each node is an
//! envelope: a U-interval plus a disk in (V, W). Two orbits meet only if their Binet separation is
//! spacelike with |ΔU| − |Δ(V,W)| < ε, so a whole group pair is skipped when
//!   min|ΔU| − max|Δ(V,W)| ≥ ε_max
//! (a set-to-set causal-geometry test: the cone between envelopes). A kick walks one leaf-to-root
//! path: O(log N) envelope recomputations, and only node pairs on the path can lose a certificate.
//!
//! Tier 2 (time, once per horizon): a candidate pair is *armed* only if some passage lands in a
//! sound window superset within the horizon. Arming uses only closed forms (velocities at the
//! crossing longitude, exact passage ticks, the integer first-hit): no arc travel times, no numeric
//! windows, no state evaluations. Silent pairs store their slack (how far beyond the horizon the
//! first in-window passage sits, in units of the horizon). The exact float machinery runs on armed
//! pairs only; every reported event still comes from the crate's exact per-pair check.

use crate::dioph::first_hit;
use crate::kepler::{Body, TICKS};
use crate::method::{pair_events, Stats};
use crate::pairs::{eps_u, is_candidate, Kind};
use std::f64::consts::{PI, TAU};

// ---------------------------------------------------------------- envelope tree

#[derive(Clone, Copy)]
pub struct Node {
    pub lo: usize,
    pub hi: usize,
    pub ulo: f64,
    pub uhi: f64,
    pub cx: f64,
    pub cy: f64,
    pub rad: f64,
    pub rmin: f64,
    pub rmax: f64,
    pub emax: f64,
    pub pmin: f64,
    /// Children (internal only).
    pub ch: (usize, usize),
}

impl Node {
    fn eps_max(&self, o: &Node, rho: f64) -> f64 {
        let rmin = self.rmin.min(o.rmin);
        let rmax = self.rmax.max(o.rmax);
        let emax = self.emax.max(o.emax);
        let pmin = self.pmin.min(o.pmin);
        1.5 * rho * (1.0 + rmax * rmax * emax / (pmin * rmin)) / (rmin * rmin)
    }

    /// True: no member pair can be a candidate (sound prune of the whole group pair).
    fn sep(&self, o: &Node, rho: f64) -> bool {
        let du = (o.ulo - self.uhi).max(self.ulo - o.uhi).max(0.0);
        let rmax = ((self.cx - o.cx).hypot(self.cy - o.cy) + self.rad + o.rad).max(0.0);
        du - rmax >= self.eps_max(o, rho)
    }
}

pub struct Tree {
    pub order: Vec<(f64, u32)>,
    pub bucket: usize,
    pub nodes: Vec<Node>,
    pub nleaves: usize,
    pub parent: Vec<usize>,
    /// Position of each body in `order`.
    pub pos: Vec<u32>,
}

impl Tree {
    pub fn new(b: &[Body], bucket: usize) -> Self {
        let mut order: Vec<(f64, u32)> = b
            .iter()
            .enumerate()
            .map(|(k, x)| (x.binet()[0], k as u32))
            .collect();
        order.sort_by(|x, y| x.0.total_cmp(&y.0).then(x.1.cmp(&y.1)));
        let n = order.len();
        let bucket = bucket.max(1);
        let nleaves = n.div_ceil(bucket);
        let mut nodes: Vec<Node> = Vec::with_capacity(2 * nleaves);
        let mut parent: Vec<usize> = vec![usize::MAX; nleaves];
        for k in 0..nleaves {
            let lo = k * bucket;
            let hi = ((k + 1) * bucket).min(n);
            let mut nd = Node {
                lo,
                hi,
                ulo: f64::INFINITY,
                uhi: f64::NEG_INFINITY,
                cx: 0.0,
                cy: 0.0,
                rad: 0.0,
                rmin: f64::INFINITY,
                rmax: 0.0,
                emax: 0.0,
                pmin: f64::INFINITY,
                ch: (usize::MAX, usize::MAX),
            };
            let (mut sx, mut sy) = (0.0, 0.0);
            for &(_, i) in &order[lo..hi] {
                let x = &b[i as usize];
                let u = x.binet();
                nd.ulo = nd.ulo.min(u[0]);
                nd.uhi = nd.uhi.max(u[0]);
                nd.rmin = nd.rmin.min(x.rmin());
                nd.rmax = nd.rmax.max(x.rmax());
                nd.emax = nd.emax.max(x.e);
                nd.pmin = nd.pmin.min(x.p);
                sx += u[1];
                sy += u[2];
            }
            let m = (hi - lo) as f64;
            nd.cx = sx / m;
            nd.cy = sy / m;
            for &(_, i) in &order[lo..hi] {
                let u = b[i as usize].binet();
                nd.rad = nd.rad.max((u[1] - nd.cx).hypot(u[2] - nd.cy));
            }
            nodes.push(nd);
        }
        let mut level: Vec<usize> = (0..nleaves).collect();
        while level.len() > 1 {
            let mut next: Vec<usize> = Vec::new();
            for pair in level.chunks(2) {
                if pair.len() == 2 {
                    let (a, b) = (nodes[pair[0]], nodes[pair[1]]);
                    let cx = (a.cx + b.cx) * 0.5;
                    let cy = (a.cy + b.cy) * 0.5;
                    nodes.push(Node {
                        lo: a.lo,
                        hi: b.hi,
                        ulo: a.ulo.min(b.ulo),
                        uhi: a.uhi.max(b.uhi),
                        cx,
                        cy,
                        rad: 0.5 * (a.cx - b.cx).hypot(a.cy - b.cy) + a.rad.max(b.rad),
                        rmin: a.rmin.min(b.rmin),
                        rmax: a.rmax.max(b.rmax),
                        emax: a.emax.max(b.emax),
                        pmin: a.pmin.min(b.pmin),
                        ch: (pair[0], pair[1]),
                    });
                    parent.push(usize::MAX);
                    parent[pair[0]] = nodes.len() - 1;
                    parent[pair[1]] = nodes.len() - 1;
                    next.push(nodes.len() - 1);
                } else {
                    next.push(pair[0]);
                }
            }
            level = next;
        }
        let mut pos = vec![0u32; order.len()];
        for (k, &(_, i)) in order.iter().enumerate() {
            pos[i as usize] = k as u32;
        }
        Tree {
            order,
            bucket,
            nodes,
            nleaves,
            parent,
            pos,
        }
    }

    /// Recompute envelopes from leaf `lf` to the root after bodies changed; returns recomputations.
    pub fn refresh_path(&mut self, b: &[Body], lf: usize) -> usize {
        let mut count = 0;
        let mut k = lf;
        // Leaf envelope.
        self.recompute_leaf(b, k);
        count += 1;
        while self.parent[k] != usize::MAX {
            k = self.parent[k];
            self.recompute_node(k);
            count += 1;
        }
        count
    }

    fn recompute_leaf(&mut self, b: &[Body], k: usize) {
        let (lo, hi) = (self.nodes[k].lo, self.nodes[k].hi);
        let mut nd = self.nodes[k];
        nd.ulo = f64::INFINITY;
        nd.uhi = f64::NEG_INFINITY;
        nd.cx = 0.0;
        nd.cy = 0.0;
        nd.rad = 0.0;
        nd.rmin = f64::INFINITY;
        nd.rmax = 0.0;
        nd.emax = 0.0;
        nd.pmin = f64::INFINITY;
        let (mut sx, mut sy) = (0.0, 0.0);
        for &(_, i) in &self.order[lo..hi] {
            let x = &b[i as usize];
            let u = x.binet();
            nd.ulo = nd.ulo.min(u[0]);
            nd.uhi = nd.uhi.max(u[0]);
            nd.rmin = nd.rmin.min(x.rmin());
            nd.rmax = nd.rmax.max(x.rmax());
            nd.emax = nd.emax.max(x.e);
            nd.pmin = nd.pmin.min(x.p);
            sx += u[1];
            sy += u[2];
        }
        let m = (hi - lo) as f64;
        nd.cx = sx / m;
        nd.cy = sy / m;
        for &(_, i) in &self.order[lo..hi] {
            let u = b[i as usize].binet();
            nd.rad = nd.rad.max((u[1] - nd.cx).hypot(u[2] - nd.cy));
        }
        self.nodes[k] = nd;
    }

    fn recompute_node(&mut self, k: usize) {
        let (l, r) = self.nodes[k].ch;
        let (a, c) = (self.nodes[l], self.nodes[r]);
        self.nodes[k].lo = a.lo;
        self.nodes[k].hi = c.hi;
        self.nodes[k].ulo = a.ulo.min(c.ulo);
        self.nodes[k].uhi = a.uhi.max(c.uhi);
        self.nodes[k].cx = (a.cx + c.cx) * 0.5;
        self.nodes[k].cy = (a.cy + c.cy) * 0.5;
        self.nodes[k].rad = 0.5 * (a.cx - c.cx).hypot(a.cy - c.cy) + a.rad.max(c.rad);
        self.nodes[k].rmin = a.rmin.min(c.rmin);
        self.nodes[k].rmax = a.rmax.max(c.rmax);
        self.nodes[k].emax = a.emax.max(c.emax);
        self.nodes[k].pmin = a.pmin.min(c.pmin);
    }
}

#[derive(Default, Debug, Clone, Copy)]
pub struct TreeStats {
    pub node_tests: u64,
    pub pruned: u64,
    pub leafpair_tests: u64,
    pub cand: u64,
}

fn go(
    t: &Tree,
    b: &[Body],
    rho: f64,
    x: usize,
    y: usize,
    bodies_too: bool,
    f: &mut dyn FnMut(u32, u32),
    st: &mut TreeStats,
) {
    st.node_tests += 1;
    if x != y && t.nodes[x].sep(&t.nodes[y], rho) {
        st.pruned += 1;
        return;
    }
    let leafx = t.nodes[x].ch == (usize::MAX, usize::MAX);
    let leafy = t.nodes[y].ch == (usize::MAX, usize::MAX);
    if x == y {
        if leafx {
            if bodies_too {
                let (lo, hi) = (t.nodes[x].lo, t.nodes[x].hi);
                for a in lo..hi {
                    for c in a + 1..hi {
                        let (i, j) = (t.order[a].1, t.order[c].1);
                        let (i, j) = (i.min(j), i.max(j));
                        if is_candidate(&b[i as usize], &b[j as usize], rho) {
                            st.cand += 1;
                            f(i, j);
                        }
                    }
                }
            }
            return;
        }
        let (l, r) = t.nodes[x].ch;
        go(t, b, rho, l, l, bodies_too, f, st);
        go(t, b, rho, l, r, bodies_too, f, st);
        go(t, b, rho, r, r, bodies_too, f, st);
        return;
    }
    if leafx && leafy {
        st.leafpair_tests += 1;
        if bodies_too {
            for a in t.nodes[x].lo..t.nodes[x].hi {
                for c in t.nodes[y].lo..t.nodes[y].hi {
                    let (i, j) = (t.order[a].1, t.order[c].1);
                    let (i, j) = if i < j { (i, j) } else { (j, i) };
                    if i == j {
                        continue;
                    }
                    if is_candidate(&b[i as usize], &b[j as usize], rho) {
                        st.cand += 1;
                        f(i, j);
                    }
                }
            }
        }
        return;
    }
    // Split the node with more bodies.
    let (nx, ny) = (t.nodes[x].hi - t.nodes[x].lo, t.nodes[y].hi - t.nodes[y].lo);
    if (nx >= ny && !leafx) || leafy {
        let (l, r) = t.nodes[x].ch;
        go(t, b, rho, l, y, bodies_too, f, st);
        go(t, b, rho, r, y, bodies_too, f, st);
    } else {
        let (l, r) = t.nodes[y].ch;
        go(t, b, rho, x, l, bodies_too, f, st);
        go(t, b, rho, x, r, bodies_too, f, st);
    }
}

/// Traverse every candidate pair through the tree. If `bodies_too`, call `f(i, j)` on each exact
/// candidate; otherwise stop at leaf-pair granularity (counting only).
pub fn traverse(
    t: &Tree,
    b: &[Body],
    rho: f64,
    bodies_too: bool,
    f: &mut dyn FnMut(u32, u32),
    st: &mut TreeStats,
) {
    if t.nodes.is_empty() {
        return;
    }
    let root = t.nodes.len() - 1;
    go(t, b, rho, root, root, bodies_too, f, st);
}

// ---------------------------------------------------------------- arming tier

fn ticks_up(x: f64) -> i64 {
    (x * TICKS).ceil() as i64
}

/// Sound window half-widths around a transversal crossing, closed forms only: the same linear
/// model the exact machinery uses (Δ(τ) = −v_i s + a_P s²/2 + (v_i − v_j − a_P s)τ), with the
/// distance-to-line D(s) evaluated directly. None: model degenerate (|Δv| ≈ 0) — caller falls
/// back to a full-width window.
fn fast_window(bi: &Body, bj: &Body, th: f64, rho: f64) -> Option<(f64, f64)> {
    let (st, ct) = th.sin_cos();
    // Closed-form state of a Kepler orbit at true longitude th.
    let state = |o: &Body| -> ([f64; 2], [f64; 2]) {
        let f = th - o.pom;
        let (sf, cf) = f.sin_cos();
        let r = o.p / (1.0 + o.e * cf);
        let k = 1.0 / o.p.sqrt();
        let vr = k * o.e * sf;
        let vt = k * (1.0 + o.e * cf);
        ([r * ct, r * st], [vr * ct - vt * st, vr * st + vt * ct])
    };
    let (ri, vi) = state(bi);
    let (_rj, vj) = state(bj);
    let r3 = (ri[0] * ri[0] + ri[1] * ri[1]).powf(1.5);
    let ap = [-ri[0] / r3, -ri[1] / r3];
    let dv = [vi[0] - vj[0], vi[1] - vj[1]];
    let ndv = dv[0].hypot(dv[1]);
    if !(ndv > 1e-12) {
        return None;
    }
    // D(s) = |Δ₀(s) × û(s)|, Δ₀ = −v_i s + a_P s²/2, u = Δv − a_P s.
    let d_of = |s: f64| -> f64 {
        let d0 = [
            -vi[0] * s + 0.5 * ap[0] * s * s,
            -vi[1] * s + 0.5 * ap[1] * s * s,
        ];
        let u = [dv[0] - ap[0] * s, dv[1] - ap[1] * s];
        (d0[0] * u[1] - d0[1] * u[0]).abs() / u[0].hypot(u[1])
    };
    // Start from the linear width and walk out until D ≥ ρ (D ≈ linear near 0).
    let c0 = (vi[0] * dv[1] - vi[1] * dv[0]).abs() / ndv;
    if !(c0 > 1e-14) {
        return None;
    }
    let w0 = rho / c0;
    let grow = 1.3;
    let side = |sign: f64| -> f64 {
        let mut w = w0;
        // First a coarse geometric walk, then a few secant refinements — soundness only needs
        // D(±w) ≥ ρ at the end (walked outward with margin).
        let mut k = 0;
        while d_of(sign * w) < rho && k < 64 {
            w *= grow;
            k += 1;
        }
        w * 1.05
    };
    Some((side(-1.0), side(1.0)))
}

pub struct ArmSection {
    pub kind: Kind,
    pub ti: u64,
    pub tj: u64,
    pub w1: i64,
    pub w2: i64,
}

struct Arc {
    c: f64,
    dm: f64,
    dp: f64,
    cross: bool,
}

fn full_section_arm(bi: &Body, bj: &Body, rho: f64) -> Vec<ArmSection> {
    // pairs::full_section (analytic): window from the time-offset spread of the two orbits.
    let th = bj.pom;
    let k = 64;
    let (mut dmin, mut dmax, mut jump, mut prev) = (0.0f64, 0.0f64, 0.0f64, 0.0f64);
    let mut push = |d: f64| {
        dmin = dmin.min(d);
        dmax = dmax.max(d);
        jump = jump.max((d - prev).abs());
        prev = d;
    };
    for q in 1..k {
        let thq = th + TAU * q as f64 / k as f64;
        push(bj.travel(th, thq) - bi.travel(th, thq));
    }
    push((bj.period as f64 - bi.period as f64) / TICKS);
    let rmin = bi.rmin().min(bj.rmin());
    let rmax = bi.rmax().max(bj.rmax());
    let thdot_min = bi.p.min(bj.p).sqrt() / (rmax * rmax);
    let pad = 1.3 * rho / (rmin * thdot_min) + jump;
    vec![ArmSection {
        kind: Kind::Full,
        ti: bi.passage_tick(th),
        tj: bj.passage_tick(th),
        w1: ticks_up(pad - dmin),
        w2: ticks_up(dmax + pad),
    }]
}

/// Analytic-only sections with sound superset windows. Cross: fast_window × margin. Wide/tangency:
/// the crate's arc-overlap cap window (travel bounds, closed forms; no state evaluations).
pub fn arm_sections(bi: &Body, bj: &Body, rho: f64, safety: f64) -> Vec<ArmSection> {
    let (a, b) = (bi.binet(), bj.binet());
    let du = a[0] - b[0];
    let dv = a[1] - b[1];
    let dw = a[2] - b[2];
    let r = dv.hypot(dw);
    let eps = eps_u(bi, bj, rho);
    if du.abs() - r >= eps {
        return Vec::new();
    }
    if r < 1e-300 {
        return full_section_arm(bi, bj, rho);
    }
    let th0 = dw.atan2(dv);
    let c_lo = (-eps - du) / r;
    let c_hi = (eps - du) / r;
    let merged0 = c_hi >= 1.0;
    let merged_pi = c_lo <= -1.0;
    let phi1 = c_hi.min(1.0).acos();
    let phi2 = c_lo.max(-1.0).acos();
    let arcs = if merged0 && merged_pi {
        return full_section_arm(bi, bj, rho);
    } else if merged0 {
        vec![Arc {
            c: th0,
            dm: phi2,
            dp: phi2,
            cross: false,
        }]
    } else if merged_pi {
        vec![Arc {
            c: th0 + PI,
            dm: PI - phi1,
            dp: PI - phi1,
            cross: false,
        }]
    } else {
        let phx = (-du / r).clamp(-1.0, 1.0).acos();
        vec![
            Arc {
                c: th0 + phx,
                dm: phx - phi1,
                dp: phi2 - phx,
                cross: true,
            },
            Arc {
                c: th0 - phx,
                dm: phi2 - phx,
                dp: phx - phi1,
                cross: true,
            },
        ]
    };
    arcs.into_iter()
        .filter_map(|arc| {
            let th = arc.c.rem_euclid(TAU);
            let (w1, w2, kind) = if arc.cross {
                match fast_window(bi, bj, th, rho) {
                    Some((sm, sp)) => (safety * sm, safety * sp, Kind::Cross),
                    // Degenerate crossing (|Δv| ≈ 0): the crate's cap window (computed lazily).
                    None => {
                        let di = (bi.travel(th - arc.dm, th), bi.travel(th, th + arc.dp));
                        let dj = (bj.travel(th - arc.dm, th), bj.travel(th, th + arc.dp));
                        (dj.0 + di.1, dj.1 + di.0, Kind::Wide)
                    }
                }
            } else {
                // Keep the passage-overlap cap. The lab's linear tightening
                // dropped contacts at e=0.7..0.9; no model window may narrow it.
                let di = (bi.travel(th - arc.dm, th), bi.travel(th, th + arc.dp));
                let dj = (bj.travel(th - arc.dm, th), bj.travel(th, th + arc.dp));
                (dj.0 + di.1, dj.1 + di.0, Kind::Wide)
            };
            if !(w1.is_finite() && w2.is_finite() && w1 >= 0.0 && w2 >= 0.0) {
                return None;
            }
            Some(ArmSection {
                kind,
                ti: bi.passage_tick(th),
                tj: bj.passage_tick(th),
                w1: ticks_up(w1),
                w2: ticks_up(w2),
            })
        })
        .collect()
}

#[derive(Default, Debug, Clone, Copy)]
pub struct ArmStats {
    pub tests: u64,
    pub armed: u64,
    pub silent: u64,
    pub qsteps: u64,
    /// First in-window passage time (time units) — may exceed the horizon (slack).
    pub due: f64,
    pub sections: [u64; 3],
}

/// Does some passage of j over the section land in the (superset) window within [t0, t1]?
/// Sound superset of "the exact machinery reports an event in [t0, t1]". Returns (armed, due).
pub fn arm_pair(
    bi: &Body,
    bj: &Body,
    rho: f64,
    safety: f64,
    t0: f64,
    t1: f64,
    st: &mut ArmStats,
) -> (bool, f64) {
    st.tests += 1;
    let mut due = f64::INFINITY;
    let mut any = false;
    for sec in arm_sections(bi, bj, rho, safety) {
        st.sections[sec.kind as usize] += 1;
        let ti = sec.ti as i128;
        let tj = sec.tj as i128;
        let pi = bi.period as i128;
        let pj = bj.period as i128;
        // Sound superset of the crate's `ext` (arc traversals are sub-period).
        let ext = pi + 2 * pj;
        let t0t = (t0 * TICKS) as i128;
        let t1t = (t1 * TICKS) as i128;
        let base = tj + (t0t - ext - tj).div_euclid(pj) * pj;
        let lmax = (t1t + ext - base).div_euclid(pj);
        let w1 = sec.w1 as i128;
        let w = (w1 + sec.w2 as i128).clamp(0, pi - 1);
        let c0 = (ti - base + w1).rem_euclid(pi);
        let d = (pi - pj.rem_euclid(pi)).rem_euclid(pi);
        if let Some(k) = first_hit(
            c0 as u128,
            d as u128,
            pi as u128,
            0,
            w as u128,
            &mut st.qsteps,
        ) {
            let l = k as i128;
            due = due.min((base + l * pj) as f64 / TICKS);
            if l <= lmax {
                any = true;
            }
        }
    }
    st.due = st.due.min(due);
    if any {
        st.armed += 1;
    } else {
        st.silent += 1;
    }
    (any, due)
}

/// Phase A: arm every candidate of body i's U-range; collect armed partner ids and dues.
#[allow(clippy::too_many_arguments)]
pub fn tiered_arm(
    b: &[Body],
    order: &[(f64, u32)],
    i: u32,
    rho: f64,
    safety_arm: f64,
    t0: f64,
    t1: f64,
    reach: impl Fn(&Body) -> f64,
    ast: &mut ArmStats,
    armed: &mut Vec<(u32, f64)>,
) {
    let bi = &b[i as usize];
    let u = bi.binet()[0];
    let lo = order.partition_point(|z| z.0 < u - reach(bi));
    let hi = order.partition_point(|z| z.0 <= u + reach(bi));
    for &(_, j) in &order[lo..hi] {
        if j <= i {
            continue;
        }
        let bj = &b[j as usize];
        if !is_candidate(bi, bj, rho) {
            continue;
        }
        let (on, due) = arm_pair(bi, bj, rho, safety_arm, t0, t1, ast);
        if on {
            armed.push((j, due));
        }
    }
}

/// Phase B: the exact machinery on armed pairs only.
pub fn tiered_exact(
    b: &[Body],
    i: u32,
    armed: &[(u32, f64)],
    rho: f64,
    t0: f64,
    t1: f64,
    xst: &mut Stats,
    out: &mut Vec<(u32, u32, f64, f64)>,
) {
    let bi = &b[i as usize];
    for &(j, _) in armed {
        let mut tmp = Vec::new();
        pair_events(bi, &b[j as usize], rho, 1.1, t0, t1, xst, &mut tmp);
        out.extend(tmp.iter().map(|&(t, d)| (i, j, t, d)));
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{
        belt::{make_belt, Spec},
        pairs::cone_pairs,
    };
    use std::collections::BTreeSet;

    #[test]
    fn envelope_tree_equals_brute_cone_with_unbalanced_radii_and_id_order() {
        let spec = Spec {
            name: "tree".into(),
            n: 193,
            sigma_e: 0.15,
            rho: 0.001,
            a_lo: 0.5,
            a_hi: 3.0,
            keys: 0,
            seed: 89,
            orbits: 1.0,
        };
        let mut b = make_belt(&spec);
        b[71] = Body::new(1.0, 0.9, 0.7, 1.1);
        let expected: BTreeSet<_> = cone_pairs(&b, spec.rho).pairs.into_iter().collect();
        for bucket in [1, 7, 32, 1000] {
            let tree = Tree::new(&b, bucket);
            let mut found = BTreeSet::new();
            traverse(
                &tree,
                &b,
                spec.rho,
                true,
                &mut |i, j| {
                    assert!(found.insert((i, j)));
                },
                &mut TreeStats::default(),
            );
            assert_eq!(found, expected, "bucket {bucket}");
        }
    }

    #[test]
    fn wide_arming_keeps_the_full_passage_overlap_cap_at_high_e() {
        let mut wide = 0;
        for e in [0.7, 0.8, 0.9] {
            let a = Body::new(1.0, e, 0.0, 0.0);
            let b = Body::new(0.9, 1.0 - (1.0 - e) / 0.9, 0.0, 0.02);
            for sec in arm_sections(&a, &b, 1e-5, 1.1) {
                if sec.kind != Kind::Wide {
                    continue;
                }
                wide += 1;
                // Vary safety to catch accidental model-dependent tightening:
                // overlap bounds depend solely on arc transit times.
                let other = arm_sections(&a, &b, 1e-5, 0.0);
                let same = other
                    .iter()
                    .find(|s| s.ti == sec.ti && s.tj == sec.tj)
                    .unwrap();
                assert_eq!((sec.w1, sec.w2), (same.w1, same.w2));
            }
        }
        assert!(wide > 0, "probe must exercise Wide");
    }
}
