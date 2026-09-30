//! Candidates and sections.
//!
//! In Binet coordinates (U, V, W) = (1/p, e cos ϖ / p, e sin ϖ / p) an orbit is u(θ) = U + V cos θ +
//! W sin θ. Two orbits meet iff ΔU² ≤ ΔV² + ΔW² (spacelike), at θ = atan2(ΔW, ΔV) ± acos(−ΔU/R). A pair
//! can come within ρ only where |Δu(θ)| < ε(ρ): at most two short arcs (transversal crossings), one
//! arc (tangency), or the whole orbit (nearly identical orbits).
//!
//! A section samples the pair each time j passes the arc's reference longitude θ_c. At those passages
//! i passes θ_c offset by s_l = (t_i − t_j − l·T_j) mod T_i: an integer circle rotation. The window W
//! on s is a guide (a superset); an exact per-pair check decides each proposed passage.

use crate::kepler::{rel, Body, TICKS};
use std::f64::consts::{PI, TAU};

#[inline]
pub fn dot(a: [f64; 2], b: [f64; 2]) -> f64 {
    a[0] * b[0] + a[1] * b[1]
}

#[inline]
pub fn norm(a: [f64; 2]) -> f64 {
    a[0].hypot(a[1])
}

/// Radial-overlap pairs (r8 v2's candidate set, used by the truth): [rmin − ρ, rmax + ρ] overlap.
pub fn radial_pairs(b: &[Body], rho: f64) -> Vec<(u32, u32)> {
    let mut idx: Vec<u32> = (0..b.len() as u32).collect();
    idx.sort_by(|&x, &y| b[x as usize].rmin().total_cmp(&b[y as usize].rmin()));
    let mut out = Vec::new();
    for (k, &i) in idx.iter().enumerate() {
        let hi = b[i as usize].rmax() + 2.0 * rho;
        for &j in &idx[k + 1..] {
            if b[j as usize].rmin() > hi {
                break;
            }
            out.push((i.min(j), i.max(j)));
        }
    }
    out
}

/// A u-tolerance such that two orbits within ρ of each other must have |Δu(θ)| < ε at both bodies'
/// longitudes (radial gap plus the slope of the orbit across the angular offset, with a 1.5 margin).
#[inline]
pub fn eps_u(bi: &Body, bj: &Body, rho: f64) -> f64 {
    let rmin = bi.rmin().min(bj.rmin());
    let rmax = bi.rmax().max(bj.rmax());
    let emax = bi.e.max(bj.e);
    let pmin = bi.p.min(bj.p);
    let kappa = rmax * rmax * emax / (pmin * rmin);
    1.5 * rho * (1.0 + kappa) / (rmin * rmin)
}

/// |ΔU| − R: negative for crossing orbits, 0 for tangent ones.
#[inline]
pub fn cone_gap(bi: &Body, bj: &Body) -> f64 {
    let (a, b) = (bi.binet(), bj.binet());
    (a[0] - b[0]).abs() - (a[1] - b[1]).hypot(a[2] - b[2])
}

#[inline]
pub fn is_candidate(bi: &Body, bj: &Body, rho: f64) -> bool {
    cone_gap(bi, bj) < eps_u(bi, bj, rho)
}

/// The implicit candidate set: bodies sorted by U; a body's partners lie in a contiguous U-range.
pub struct Sorted {
    /// (U, body) ascending.
    pub order: Vec<(f64, u32)>,
    pub e_max: f64,
    pub eps_max: f64,
}

impl Sorted {
    pub fn new(b: &[Body], rho: f64) -> Self {
        let mut order: Vec<(f64, u32)> = b.iter().enumerate().map(|(k, x)| (x.binet()[0], k as u32)).collect();
        order.sort_by(|x, y| x.0.total_cmp(&y.0).then(x.1.cmp(&y.1)));
        let e_max = b.iter().map(|x| x.e / x.p).fold(0.0, f64::max);
        let rmin = b.iter().map(|x| x.rmin()).fold(f64::INFINITY, f64::min);
        let rmax = b.iter().map(|x| x.rmax()).fold(0.0, f64::max);
        let emax = b.iter().map(|x| x.e).fold(0.0, f64::max);
        let pmin = b.iter().map(|x| x.p).fold(f64::INFINITY, f64::min);
        let eps_max = 1.5 * rho * (1.0 + rmax * rmax * emax / (pmin * rmin)) / (rmin * rmin);
        Sorted { order, e_max, eps_max }
    }

    /// Half-width of body x's U-range.
    #[inline]
    pub fn reach(&self, x: &Body) -> f64 {
        x.e / x.p + self.e_max + self.eps_max
    }

    /// Range of sorted positions whose U lies within reach of u.
    pub fn range(&self, u: f64, reach: f64) -> (usize, usize) {
        let lo = self.order.partition_point(|z| z.0 < u - reach);
        let hi = self.order.partition_point(|z| z.0 <= u + reach);
        (lo, hi)
    }
}

pub struct ConeScan {
    pub pairs: Vec<(u32, u32)>,
    pub scanned: u64,
}

/// Every candidate pair once, by scanning each body's upper U-range and testing the cone exactly.
pub fn cone_pairs(b: &[Body], rho: f64) -> ConeScan {
    let s = Sorted::new(b, rho);
    let mut pairs = Vec::new();
    let mut scanned = 0u64;
    for (k, &(u, i)) in s.order.iter().enumerate() {
        let bi = &b[i as usize];
        let reach = s.reach(bi);
        for &(uj, j) in &s.order[k + 1..] {
            if uj - u > reach {
                break;
            }
            scanned += 1;
            if is_candidate(bi, &b[j as usize], rho) {
                pairs.push((i.min(j), i.max(j)));
            }
        }
    }
    ConeScan { pairs, scanned }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Kind {
    /// A transversal crossing: linear window around the exact crossing point.
    Cross = 0,
    /// A tangency, a merged arc, or a crossing whose arc is long: the passage-overlap window.
    Wide = 1,
    /// Nearly identical orbits: section at j's periapsis, window from the time-offset spread.
    Full = 2,
}

#[derive(Clone, Debug)]
pub struct Section {
    pub kind: Kind,
    pub theta: f64,
    /// Ticks (mod period) at which i and j pass θ_c.
    pub ti: u64,
    pub tj: u64,
    /// Window: s ∈ [−w1, w2] ticks.
    pub w1: i64,
    pub w2: i64,
    /// Time from arc entry to θ_c and from θ_c to arc exit, for i and j.
    pub di: (f64, f64),
    pub dj: (f64, f64),
}

struct Arc {
    c: f64,
    dm: f64,
    dp: f64,
    cross: bool,
}

/// The pair's sections (0, 1 or 2). `safety` scales the linear window; `evals` counts the exact
/// state evaluations spent on numeric windows (setup cost).
pub fn sections(bi: &Body, bj: &Body, rho: f64, safety: f64, evals: &mut u64) -> Vec<Section> {
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
        return vec![full_section(bi, bj, rho)];
    }
    let th0 = dw.atan2(dv);
    let c_lo = (-eps - du) / r;
    let c_hi = (eps - du) / r;
    let merged0 = c_hi >= 1.0;
    let merged_pi = c_lo <= -1.0;
    let phi1 = c_hi.min(1.0).acos();
    let phi2 = c_lo.max(-1.0).acos();
    let arcs = if merged0 && merged_pi {
        return vec![full_section(bi, bj, rho)];
    } else if merged0 {
        vec![Arc { c: th0, dm: phi2, dp: phi2, cross: false }]
    } else if merged_pi {
        vec![Arc { c: th0 + PI, dm: PI - phi1, dp: PI - phi1, cross: false }]
    } else {
        let phx = (-du / r).clamp(-1.0, 1.0).acos();
        vec![
            Arc { c: th0 + phx, dm: phx - phi1, dp: phi2 - phx, cross: true },
            Arc { c: th0 - phx, dm: phi2 - phx, dp: phx - phi1, cross: true },
        ]
    };
    arcs.into_iter().filter_map(|arc| arc_section(bi, bj, rho, safety, &arc, evals)).collect()
}

fn ticks_up(x: f64) -> i64 {
    (x * TICKS).ceil() as i64
}

fn arc_section(bi: &Body, bj: &Body, rho: f64, safety: f64, arc: &Arc, evals: &mut u64) -> Option<Section> {
    let th = arc.c.rem_euclid(TAU);
    let di = (bi.travel(th - arc.dm, th), bi.travel(th, th + arc.dp));
    let dj = (bj.travel(th - arc.dm, th), bj.travel(th, th + arc.dp));
    let cap = (dj.0 + di.1, dj.1 + di.0);
    let mut kind = Kind::Wide;
    let mut w = cap;
    if arc.cross && arc.dm.max(arc.dp) < 0.2 {
        if let Some((sm, sp)) = cross_window(bi, bj, th, rho) {
            let (wm, wp) = (safety * sm, safety * sp);
            if wm <= 0.5 * cap.0 && wp <= 0.5 * cap.1 {
                kind = Kind::Cross;
                w = (wm, wp);
            }
        }
    }
    if kind == Kind::Wide {
        // Tangency, merged or long arc: the window is computed once, numerically and rigorously.
        let (l, r) = numeric_window(bi, bj, th, dj, (-cap.0, cap.1), rho, evals)?;
        w = (-l, r);
    }
    Some(Section { kind, theta: th, ti: bi.passage_tick(th), tj: bj.passage_tick(th), w1: ticks_up(w.0), w2: ticks_up(w.1), di, dj })
}

/// The window around a transversal crossing point P, to second order. Both bodies at P feel the same
/// gravity a_P, so with i passing P s later than j (τ from j's passage):
///   Δ(τ) = −v_i s + a_P s²/2 + (v_i − v_j − a_P s) τ + O(3),
/// a straight line in τ. Its distance from the origin is D(s) = |Δ₀(s) × û(s)|; the window edges are
/// the roots of D(s) = ρ on each side (from the linear estimate, a few secant steps). Returns the
/// (negative-side, positive-side) half-widths in time units.
fn cross_window(bi: &Body, bj: &Body, th: f64, rho: f64) -> Option<(f64, f64)> {
    let si = bi.at_longitude(th);
    let sj = bj.at_longitude(th);
    let r3 = (si[0] * si[0] + si[1] * si[1]).powf(1.5);
    let ap = [-si[0] / r3, -si[1] / r3];
    let vi = [si[2], si[3]];
    let vr = [si[2] - sj[2], si[3] - sj[3]];
    let d2 = |s: f64| -> f64 {
        let d0 = [-vi[0] * s + 0.5 * ap[0] * s * s, -vi[1] * s + 0.5 * ap[1] * s * s];
        let u = [vr[0] - ap[0] * s, vr[1] - ap[1] * s];
        (d0[0] * u[1] - d0[1] * u[0]).abs() / norm(u)
    };
    let c = (vi[0] * vr[1] - vi[1] * vr[0]).abs() / norm(vr);
    if !(c > 0.0) {
        return None;
    }
    let w0 = rho / c;
    let side = |sign: f64| -> Option<f64> {
        // Bracket D(s) = ρ between 0 and a growing multiple of the linear estimate, then bisect.
        let mut hi = w0;
        let mut k = 0;
        while d2(sign * hi) < rho {
            hi *= 1.5;
            k += 1;
            if k > 40 {
                return None;
            }
        }
        let mut lo = 0.0;
        for _ in 0..40 {
            let mid = 0.5 * (lo + hi);
            if d2(sign * mid) < rho {
                lo = mid;
            } else {
                hi = mid;
            }
        }
        Some(hi)
    };
    Some((side(-1.0)?, side(1.0)?))
}

type RelState = ([f64; 2], [f64; 2], [f64; 2]);

#[inline]
fn rel_of(a: [f64; 4], b: [f64; 4]) -> RelState {
    let ra3 = (a[0] * a[0] + a[1] * a[1]).powf(1.5);
    let rb3 = (b[0] * b[0] + b[1] * b[1]).powf(1.5);
    ([a[0] - b[0], a[1] - b[1]], [a[2] - b[2], a[3] - b[3]], [-a[0] / ra3 + b[0] / rb3, -a[1] / ra3 + b[1] / rb3])
}

/// D(s): the pair's minimum distance while j crosses the arc, with i passing θ_c s later than j.
/// Changing s by δ moves i by at most vmax_i·δ, so D is Lipschitz in s with that constant.
fn d_of_s(bi: &Body, bj: &Body, th: f64, dj: (f64, f64), s: f64, evals: &mut u64) -> f64 {
    let mi = bi.mean_at_longitude(th);
    let mj = bj.mean_at_longitude(th);
    let f = |tau: f64| rel_of(bi.state_at_mean(mi + bi.n * (tau - s)), bj.state_at_mean(mj + bj.n * tau));
    let (lo, hi) = (-dj.0, dj.1);
    let k = 32;
    let h = (hi - lo) / k as f64;
    let (r0, v0, _) = f(lo);
    *evals += 1;
    let mut best = norm(r0);
    let mut gp = dot(r0, v0);
    for q in 1..=k {
        let t = lo + h * q as f64;
        let (r, v, _) = f(t);
        *evals += 1;
        best = best.min(norm(r));
        let g = dot(r, v);
        if gp < 0.0 && g >= 0.0 {
            best = best.min(refine_fn(&f, t - h, t, evals).1);
        }
        gp = g;
    }
    best
}

/// The window {s : D(s) < ρ(1 + 0.05)} within [a, b], as a hull, by conservative advancement in s:
/// from a sample with D = d, every s' within (d − ρ)/L has D(s') ≥ ρ, so it is skipped rigorously.
/// None: the section can never hold an encounter (a certificate valid until a kick).
fn numeric_window(bi: &Body, bj: &Body, th: f64, dj: (f64, f64), ab: (f64, f64), rho: f64, evals: &mut u64) -> Option<(f64, f64)> {
    let lip = bi.vmax() * 1.001;
    let stop = rho * 1.05;
    let (a, b) = ab;
    let mut s = a;
    let left = loop {
        if s > b {
            return None;
        }
        let d = d_of_s(bi, bj, th, dj, s, evals);
        if d < stop {
            break s;
        }
        s += (d - rho) / lip;
    };
    let mut s = b;
    let right = loop {
        let d = d_of_s(bi, bj, th, dj, s, evals);
        if d < stop || s <= left {
            break s.max(left);
        }
        s -= (d - rho) / lip;
    };
    Some((left, right))
}

fn full_section(bi: &Body, bj: &Body, rho: f64) -> Section {
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
    Section {
        kind: Kind::Full,
        theta: th,
        ti: bi.passage_tick(th),
        tj: bj.passage_tick(th),
        w1: ticks_up(pad - dmin),
        w2: ticks_up(dmax + pad),
        di: (0.0, 0.0),
        dj: (0.0, 0.0),
    }
}

/// The exact per-pair check of one proposed passage: every local minimum of the pair's distance below
/// ρ while both bodies are in the arc (or over j's whole return, for a Full section).
pub fn check(bi: &Body, bj: &Body, sec: &Section, tjc: f64, s: f64, rho: f64, out: &mut Vec<(f64, f64)>, evals: &mut u64) {
    let (lo, hi, k) = match sec.kind {
        Kind::Cross | Kind::Wide => {
            let lo = tjc + (-sec.dj.0).max(s - sec.di.0);
            let hi = tjc + sec.dj.1.min(s + sec.di.1);
            if !(hi > lo) {
                return;
            }
            (lo, hi, if sec.kind == Kind::Cross { 24 } else { 64 })
        }
        Kind::Full => (tjc - 0.02, tjc + bj.period as f64 / TICKS + 0.02, 256),
    };
    scan_minima(bi, bj, lo, hi, k, rho, false, out, evals);
}

/// Local minima of the distance below ρ on [lo, hi], bracketed by sign changes of Δr·Δv on k steps.
#[allow(clippy::too_many_arguments)]
pub fn scan_minima(bi: &Body, bj: &Body, lo: f64, hi: f64, k: usize, rho: f64, halley: bool, out: &mut Vec<(f64, f64)>, evals: &mut u64) {
    let h = (hi - lo) / k as f64;
    let (r0, v0, _) = rel(bi, bj, lo, halley);
    let mut tp = lo;
    let mut gp = dot(r0, v0);
    *evals += 1;
    for q in 1..=k {
        let t = lo + h * q as f64;
        let (r, v, _) = rel(bi, bj, t, halley);
        *evals += 1;
        let g = dot(r, v);
        if gp < 0.0 && g >= 0.0 {
            let (tm, dm) = refine(bi, bj, tp, t, halley, evals);
            if dm < rho {
                out.push((tm, dm));
            }
        }
        tp = t;
        gp = g;
    }
}

/// The minimum of the distance in [a, b] where Δr·Δv goes from negative to non-negative.
pub fn refine(bi: &Body, bj: &Body, a: f64, b: f64, halley: bool, evals: &mut u64) -> (f64, f64) {
    refine_fn(&|t| rel(bi, bj, t, halley), a, b, evals)
}

/// Safeguarded Newton on g = Δr·Δv, for any relative-state function.
pub fn refine_fn<F: Fn(f64) -> RelState>(f: &F, mut a: f64, mut b: f64, evals: &mut u64) -> (f64, f64) {
    let mut t = 0.5 * (a + b);
    for _ in 0..80 {
        let (r, v, acc) = f(t);
        *evals += 1;
        let g = dot(r, v);
        let gp = dot(v, v) + dot(r, acc);
        if g < 0.0 {
            a = t;
        } else {
            b = t;
        }
        let mut tn = if gp > 0.0 { t - g / gp } else { f64::NAN };
        if !(tn > a && tn < b) {
            tn = 0.5 * (a + b);
        }
        let done = (tn - t).abs() < 1e-14 * (1.0 + t.abs()) || (b - a) < 1e-14 * (1.0 + t.abs());
        t = tn;
        if done {
            break;
        }
    }
    let (r, _, _) = f(t);
    *evals += 1;
    (t, norm(r))
}
