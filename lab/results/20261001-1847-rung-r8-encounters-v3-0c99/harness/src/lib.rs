//! r8 v3 harness. The `diophantine` configuration is the crate `crates/encounters` exactly as on
//! main (cone_pairs + pair_events, SAFETY = 1.1 = its main.rs constant). Everything else is ours:
//! the truth (conservative advancement, dense in time, no conjunction logic), r8 v2's conjunction
//! machinery for the two negatives, and the case drivers.

use emergent_encounters::kepler::{Body, TICKS};
use emergent_encounters::method::{pair_events, Stats};
use std::f64::consts::{PI, TAU};
use std::time::Instant;

const THREADS: usize = 2;
const SAFETY: f64 = 1.1;
pub type Enc = (u32, u32, f64, f64);

fn par_map<T, R, F>(items: Vec<T>, f: F) -> Vec<R>
where
    T: Send + Sync,
    R: Send,
    F: Fn(&[T]) -> R + Sync,
{
    emergent_encounters::par_chunks(items.len(), (items.len() / THREADS).max(1), THREADS, |r| f(&items[r]))
}

// ---------------------------------------------------------------- my Kepler (truth's solver)

#[inline]
fn kepler_state(b: &Body, t: f64) -> [f64; 4] {
    let x = (t * TICKS - b.tp as f64) / b.period as f64;
    let m = TAU * (x - x.floor());
    let e = b.e;
    // Newton from M + e sin M, residual-guarded; a different solver path from the method's.
    let mut ea = m + e * m.sin();
    for _ in 0..12 {
        let (s, c) = ea.sin_cos();
        let d = (ea - e * s - m) / (1.0 - e * c);
        ea -= d;
        if d.abs() < 1e-15 {
            break;
        }
    }
    if false && (ea - e * ea.sin() - m).abs() > 1e-13 {
        let (mut lo, mut hi) = (m - e - 1e-12, m + e + 1e-12);
        for _ in 0..80 {
            ea = 0.5 * (lo + hi);
            if ea - e * ea.sin() < m {
                lo = ea;
            } else {
                hi = ea;
            }
        }
    }
    state_from_ecc(b, ea)
}

#[inline]
fn state_from_ecc(b: &Body, ea: f64) -> [f64; 4] {
    let (se, ce) = ea.sin_cos();
    let xp = b.a * (ce - b.e);
    let yp = b.a * b.sq * se;
    let edot = b.n / (1.0 - b.e * ce);
    let vxp = -b.a * se * edot;
    let vyp = b.a * b.sq * ce * edot;
    [
        xp * b.cp - yp * b.sp,
        xp * b.sp + yp * b.cp,
        vxp * b.cp - vyp * b.sp,
        vxp * b.sp + vyp * b.cp,
    ]
}

/// (dr, dv) at t with our solver.
#[inline]
pub fn mrel_pub(bi: &Body, bj: &Body, t: f64) -> ([f64; 2], [f64; 2]) {
    mrel(bi, bj, t)
}

fn mrel(bi: &Body, bj: &Body, t: f64) -> ([f64; 2], [f64; 2]) {
    let si = kepler_state(bi, t);
    let sj = kepler_state(bj, t);
    ([si[0] - sj[0], si[1] - sj[1]], [si[2] - sj[2], si[3] - sj[3]])
}

// ---------------------------------------------------------------- the truth

#[derive(Default, Clone, Copy)]
pub struct TStats {
    pub steps: u64,
    pub fine: u64,
    pub evals: u64,
}

impl TStats {
    fn add(&mut self, o: &TStats) {
        self.steps += o.steps;
        self.fine += o.fine;
        self.evals += o.evals;
    }
}

/// Every local minimum of the pair distance below rho in (0, t_end), by conservative advancement.
///
/// Rigorous coarse step: over [t, t+h], dr(t+s) = dr + dv s + R(s) with
///   |R(h)| <= U(h) - d0 - v0 h,  U = d0 cosh(w h) + (v0/w) sinh(w h),  w^2 = 4/rc^3,
/// rc = min(rmin_i, rmin_j): both bodies stay outside the disk of radius rc forever, the disk's
/// complement is convex, and the gravity Jacobian there has norm <= 2/rc^3, so |dr''| <= w^2 |dr|
/// and Gronwall gives the separation bound U. Coarse steps keep
///   d(t+s) >= min_s |dr + dv s| - (U - d0 - v0 h)  >= 1.5 rho,
/// so nothing below 1.5 rho is ever jumped over. No conjunction logic anywhere.
///
/// Fine zone (d <= 2 rho): steps whose relative displacement is bounded (<= 0.25 rho, with the
/// acceleration accounted), so |d(t) - d(sample)| <= 0.25 rho/2 and a sub-rho dip cannot hide
/// between two samples both >= rho (it would need >= 0.25 rho of path). Encounters live in the
/// connected components of {d < rho}, entered/exited where d crosses rho; inside a component every
/// local minimum is a sign change - to + of g = dr.dv, sampled finely (displacement <= 0.1 rho,
/// capped) and refined by bisection. A near-tangency can hold several minima; all are reported.
#[allow(clippy::too_many_arguments)]
fn fine_step(rho: f64, v0: f64, w: f64, frac: f64, cap: f64) -> f64 {
    // solve v0*h + a_f h^2/2 = frac*rho with a_f = 3 rho w^2 (fine-zone acceleration bound)
    let a_f = 3.0 * rho * w * w;
    let target = frac * rho;
    let h = if a_f > 0.0 {
        (-v0 + (v0 * v0 + 2.0 * a_f * target).sqrt()) / a_f
    } else {
        target / v0.max(1e-300)
    };
    h.clamp(1e-12, cap)
}


fn dist_at(bi: &Body, bj: &Body, t: f64, st: &mut TStats) -> f64 {
    let (rr, _) = mrel(bi, bj, t);
    st.evals += 1;
    (rr[0] * rr[0] + rr[1] * rr[1]).sqrt()
}

/// Crossing of d through rho in [a, b], by bisection. entry: d(a) >= rho > d(b); exit: d(a) < rho <= d(b).
fn bisect_rho(bi: &Body, bj: &Body, rho: f64, a: f64, b: f64, st: &mut TStats, entry: bool) -> f64 {
    let (mut a, mut b) = (a, b);
    for _ in 0..40 {
        let mid = 0.5 * (a + b);
        let below = dist_at(bi, bj, mid, st) < rho;
        if below == entry {
            b = mid;
        } else {
            a = mid;
        }
    }
    0.5 * (a + b)
}


/// truth_pair under a wall-clock budget (the shared box can starve a pathological graze pair for
/// minutes): None if the budget is exceeded (the pair is then skipped and reported as such).
pub fn timed_truth_pair(bi: Body, bj: Body, rho: f64, t_end: f64, budget_s: f64) -> Option<(Vec<Enc>, TStats)> {
    let (tx, rx) = std::sync::mpsc::channel();
    std::thread::spawn(move || {
        let mut out = Vec::new();
        let mut st = TStats::default();
        truth_pair(&bi, &bj, rho, t_end, &mut out, &mut st);
        let _ = tx.send((out, st));
    });
    match rx.recv_timeout(std::time::Duration::from_secs_f64(budget_s)) {
        Ok(v) => Some(v),
        Err(_) => None,
    }
}
pub fn truth_pair(bi: &Body, bj: &Body, rho: f64, t_end: f64, out: &mut Vec<Enc>, st: &mut TStats) {
    let rc = bi.rmin().min(bj.rmin());
    let w = (4.0 / (rc * rc * rc)).sqrt();
    let target = 1.5 * rho;
    let mut t = 0.0f64;
    let (mut r, mut v) = mrel(bi, bj, t);
    st.evals += 1;
    let mut since_dip: u32 = 16;
    let d_start = (r[0] * r[0] + r[1] * r[1]).sqrt();
    let mut walk_component = |t_in: f64, t: &mut f64, r: &mut [f64; 2], v: &mut [f64; 2], out: &mut Vec<Enc>, st: &mut TStats| -> bool {
        let (t_out, r_out, v_out) = component_minima(bi, bj, rho, t_in, t_end, w, out, st);
        *t = t_out;
        *r = r_out;
        *v = v_out;
        t_out < t_end
    };
    if d_start < rho && !walk_component(0.0, &mut t, &mut r, &mut v, out, st) {
        return;
    }
    while t < t_end {
        let d0 = (r[0] * r[0] + r[1] * r[1]).sqrt();
        let v0 = (v[0] * v[0] + v[1] * v[1]).sqrt();
        let fine = d0 <= 2.0 * rho;
        let h = if fine {
            st.fine += 1;
            fine_step(rho, v0, w, 0.25, 0.5)
        } else {
            let mut h = 1.0f64;
            let mut bad = 0.0f64;
            let bound = |h: f64| -> f64 {
                // min_s |dr + dv s| over [0, h] (point-to-segment), minus the tidal excess
                let vv = v0 * v0;
                let tau = if vv > 0.0 { (-(r[0] * v[0] + r[1] * v[1]) / vv).clamp(0.0, h) } else { 0.0 };
                let ml = (r[0] + v[0] * tau).hypot(r[1] + v[1] * tau);
                let x = w * h;
                let excess = d0 * (x.cosh() - 1.0) + (v0 / w) * x.sinh() - v0 * h;
                ml - excess
            };
            let mut it = 0;
            while bound(h) < target && h > 1e-12 {
                bad = h;
                h *= 0.5;
                it += 1;
                if it > 80 {
                    break;
                }
            }
            if bad > 0.0 && h < 1.0 {
                let g0 = bound(h);
                let gb = bound(bad);
                if gb < target && g0 > gb {
                    let h2 = h + (target - g0) * (bad - h) / (gb - g0);
                    if h2 > h && h2 < bad && bound(h2) >= target {
                        h = h2;
                    }
                }
            }
            h
        };
        let tn = (t + h).min(t_end);
        let (rn, vn) = mrel(bi, bj, tn);
        st.evals += 1;
        st.steps += 1;
        let dn = (rn[0] * rn[0] + rn[1] * rn[1]).sqrt();
        if fine && d0 >= rho {
            let entry = if dn < rho {
                Some(bisect_rho(bi, bj, rho, t, tn, st, true))
            } else {
                // both ends >= rho: a dip could hide only if the step's whole displacement P
                // covers the down-and-back traverse, which needs |d0 - dn| <= P and
                // min(d0, dn) < rho + P. Slow flat grazes then re-searched at most every 16th
                // step: their dips are long and caught by the crossing detection above.
                let path = 0.25 * rho;
                let entry = if (d0 - dn).abs() <= path && d0.min(dn) < rho + path && since_dip >= 16 {
                    since_dip = 0;
                    find_dip(bi, bj, rho, t, d0, tn, dn, path, w, st)
                } else {
                    since_dip += 1;
                    None
                };
                entry
            };
            if let Some(entry) = entry {
                if !walk_component(entry, &mut t, &mut r, &mut v, out, st) {
                    return;
                }
                continue;
            }
        }
        t = tn;
        r = rn;
        v = vn;
    }
}

/// Recursive dip search on a fine interval whose ends are both >= rho. Returns the entry time of a
/// hidden {d < rho} component, or None once min(d0, dn) - path >= rho (no dip possible) or the
/// displacement bound reaches float resolution.
fn find_dip(bi: &Body, bj: &Body, rho: f64, a: f64, da: f64, b: f64, db: f64, path: f64, w: f64, st: &mut TStats) -> Option<f64> {
    find_dip_d(bi, bj, rho, a, da, b, db, path, w, st, 5)
}

/// Depth-capped: 5 levels resolve dips wider than h/32 (~2e-3 of a 0.05 fine step), finer than the
/// method's own grids (Full: T/256 ~ 0.025; Cross/Wide windows are proportionally finer where the
/// relative motion is fast, and there the displacement step is small too), so parity holds.
fn find_dip_d(bi: &Body, bj: &Body, rho: f64, a: f64, da: f64, b: f64, db: f64, path: f64, w: f64, st: &mut TStats, depth: u32) -> Option<f64> {
    if depth == 0 || da.min(db) - path >= rho {
        return None;
    }
    let mid = 0.5 * (a + b);
    let (rm, _) = mrel(bi, bj, mid);
    st.evals += 1;
    let dm = (rm[0] * rm[0] + rm[1] * rm[1]).sqrt();
    if dm < rho {
        // entry is on the side whose end is >= rho
        return Some(if da >= rho { bisect_rho(bi, bj, rho, a, mid, st, true) } else { bisect_rho(bi, bj, rho, mid, b, st, true) });
    }
    let _ = w;
    find_dip_d(bi, bj, rho, a, da, mid, dm, path / 2.0, w, st, depth - 1)
        .or_else(|| find_dip_d(bi, bj, rho, mid, dm, b, db, path / 2.0, w, st, depth - 1))
}

/// Walk one component of {d < rho} from t (d(t) < rho assumed) until d >= rho or t_end; report
/// every local minimum below rho (sign changes - to + of g = dr.dv, refined by bisection).
/// Returns (t_after, r, v) at the exit sample.
fn component_minima(bi: &Body, bj: &Body, rho: f64, t_start: f64, t_end: f64, w: f64, out: &mut Vec<Enc>, st: &mut TStats) -> (f64, [f64; 2], [f64; 2]) {
    let mut t = t_start;
    let (mut r, mut v) = mrel(bi, bj, t);
    st.evals += 1;
    let mut g = r[0] * v[0] + r[1] * v[1];
    let mut any = false;
    let mut best = (t, (r[0] * r[0] + r[1] * r[1]).sqrt());
    loop {
        let d = (r[0] * r[0] + r[1] * r[1]).sqrt();
        if d >= rho || t >= t_end {
            if !any && best.1 < rho && best.0 > 0.0 && best.0 < t_end {
                // numeric edge (component entered exactly at a minimum): report its best sample
                out.push((0, 0, best.0, best.1));
            }
            return (t, r, v);
        }
        let v0 = (v[0] * v[0] + v[1] * v[1]).sqrt();
        let h = fine_step(rho, v0, w, 0.1, 2e-3);
        let tn = (t + h).min(t_end);
        let (rn, vn) = mrel(bi, bj, tn);
        st.evals += 1;
        let gn = rn[0] * vn[0] + rn[1] * vn[1];
        let dcur = (rn[0] * rn[0] + rn[1] * rn[1]).sqrt();
        if dcur < best.1 {
            best = (tn, dcur);
        }
        if g < 0.0 && gn >= 0.0 {
            let (mut a, mut b) = (t, tn);
            for _ in 0..44 {
                let mid = 0.5 * (a + b);
                let (rm, vm) = mrel(bi, bj, mid);
                st.evals += 1;
                if rm[0] * vm[0] + rm[1] * vm[1] < 0.0 {
                    a = mid;
                } else {
                    b = mid;
                }
            }
            let tm = 0.5 * (a + b);
            let (rm, _) = mrel(bi, bj, tm);
            st.evals += 1;
            let dm = (rm[0] * rm[0] + rm[1] * rm[1]).sqrt();
            if dm < rho && tm > 0.0 && tm < t_end {
                out.push((0, 0, tm, dm));
                any = true;
            }
        }
        t = tn;
        r = rn;
        v = vn;
        g = gn;
    }
}

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

pub fn truth_all(b: &[Body], pairs: &[(u32, u32)], rho: f64, t_end: f64) -> (Vec<Enc>, TStats) {
    let parts = par_map(pairs.to_vec(), |chunk| {
        let mut out = Vec::new();
        let mut st = TStats::default();
        for &(i, j) in chunk {
            let n = out.len();
            truth_pair(&b[i as usize], &b[j as usize], rho, t_end, &mut out, &mut st);
            for e in &mut out[n..] {
                e.0 = i;
                e.1 = j;
            }
        }
        (out, st)
    });
    let (mut all, mut st) = (Vec::new(), TStats::default());
    for (o, s) in parts {
        all.extend(o);
        st.add(&s);
    }
    (all, st)
}

// ---------------------------------------------------------------- r8 v2's conjunction machinery

#[derive(Default)]
pub struct CStats {
    pub conjunctions: u64,
    pub evals: u64,
}

/// One exact distance check per synodic conjunction, over v2's window (v2's reference method;
/// element-sort runs the same exact checks, one per swap). Events = conjunctions for both.
fn conj_pair(bi: &Body, bj: &Body, rho: f64, t_end: f64, out: &mut Vec<Enc>, st: &mut CStats) {
    let dn = bi.n - bj.n;
    if dn == 0.0 {
        return;
    }
    let dlam = (bi.mean_anomaly(0.0) + bi.pom - (bj.mean_anomaly(0.0) + bj.pom)).rem_euclid(TAU);
    let adn = dn.abs();
    let abar = 0.5 * (bi.a + bj.a);
    let w = ((2.0 * abar * (bi.e + bj.e) + 3.0 * rho) / (abar * adn)).min(PI / adn).min(t_end);
    let off = if dn < 0.0 { dlam } else { TAU - dlam };
    let mut m = 0i64;
    loop {
        let tc = (off + TAU * m as f64) / adn;
        if tc > t_end {
            break;
        }
        st.conjunctions += 1;
        if tc >= 0.0 {
            // v2's grid: 8 samples per radial beat, 3..257
            let nbar = bi.n.max(bj.n);
            let ms = ((1.0 + 8.0 * w * nbar / TAU).ceil() as usize).clamp(3, 257);
            let mut best_t = tc;
            let mut best_d2 = f64::INFINITY;
            for q in 0..ms {
                let t = tc + (2.0 * q as f64 / (ms - 1) as f64 - 1.0) * w;
                let (r, _) = mrel(bi, bj, t);
                st.evals += 1;
                let d2 = r[0] * r[0] + r[1] * r[1];
                if d2 < best_d2 {
                    best_d2 = d2;
                    best_t = t;
                }
            }
            // Newton refine, clamped to the window and [0, T] (v2's reference)
            let (lo, hi) = ((tc - w).max(0.0), (tc + w).min(t_end));
            let mut t = best_t.clamp(lo, hi);
            for _ in 0..4 {
                let si = kepler_state(bi, t);
                let sj = kepler_state(bj, t);
                st.evals += 2;
                let (dx, dy) = (si[0] - sj[0], si[1] - sj[1]);
                let (vx, vy) = (si[2] - sj[2], si[3] - sj[3]);
                let r1 = (si[0] * si[0] + si[1] * si[1]).powf(1.5);
                let r2 = (sj[0] * sj[0] + sj[1] * sj[1]).powf(1.5);
                let (ax, ay) = (-si[0] / r1 + sj[0] / r2, -si[1] / r1 + sj[1] / r2);
                let g = dx * vx + dy * vy;
                let gp = vx * vx + vy * vy + dx * ax + dy * ay;
                let step = if gp.abs() > 1e-300 { g / gp } else { 0.0 };
                t = (t - step).clamp(lo, hi);
            }
            let (r, _) = mrel(bi, bj, t);
            st.evals += 1;
            let d2 = r[0] * r[0] + r[1] * r[1];
            if d2 < best_d2 {
                best_d2 = d2;
                best_t = t;
            }
            if best_d2.sqrt() < rho {
                out.push((0, 0, best_t, best_d2.sqrt()));
            }
        }
        m += 1;
        if m > 4_000_000 {
            break;
        }
    }
}

pub fn conj_all(b: &[Body], pairs: &[(u32, u32)], rho: f64, t_end: f64) -> (Vec<Enc>, CStats) {
    let parts = par_map(pairs.to_vec(), |chunk| {
        let mut out = Vec::new();
        let mut st = CStats::default();
        for &(i, j) in chunk {
            let n = out.len();
            conj_pair(&b[i as usize], &b[j as usize], rho, t_end, &mut out, &mut st);
            for e in &mut out[n..] {
                e.0 = i;
                e.1 = j;
            }
        }
        (out, st)
    });
    let (mut all, mut st) = (Vec::new(), CStats::default());
    for (o, s) in parts {
        all.extend(o);
        st.conjunctions += s.conjunctions;
        st.evals += s.evals;
    }
    (all, st)
}

/// Closed-form conjunction count of one pair over [0, H] (the negatives' event count).
pub fn conj_count(bi: &Body, bj: &Body, t_end: f64) -> u64 {
    let dn = bi.n - bj.n;
    if dn == 0.0 {
        return 0;
    }
    let dlam = (bi.mean_anomaly(0.0) + bi.pom - (bj.mean_anomaly(0.0) + bj.pom)).rem_euclid(TAU);
    let first = if dn < 0.0 { dlam / (-dn) } else { (TAU - dlam) / dn };
    if first > t_end {
        return 0;
    }
    1 + ((t_end - first) / (TAU / dn.abs())) as u64
}

// ---------------------------------------------------------------- matchup (crate-style)

pub fn matchup(truth: &[Enc], meth: &[Enc], t_end: f64, tol: f64) -> (u64, u64, u64) {
    let inside = |t: f64| t > 0.05 && t < t_end - 0.05;
    use std::collections::HashMap;
    let mut by_pair: HashMap<(u32, u32), Vec<f64>> = HashMap::new();
    for e in meth {
        by_pair.entry((e.0, e.1)).or_default().push(e.2);
    }
    let mut tby: HashMap<(u32, u32), Vec<f64>> = HashMap::new();
    for e in truth {
        tby.entry((e.0, e.1)).or_default().push(e.2);
    }
    let n_truth = truth.iter().filter(|e| inside(e.2)).count() as u64;
    let mut missed = 0u64;
    for e in truth.iter().filter(|e| inside(e.2)) {
        if !by_pair.get(&(e.0, e.1)).is_some_and(|v| v.iter().any(|&t| (t - e.2).abs() < tol)) {
            missed += 1;
        }
    }
    let mut false_ = 0u64;
    for e in meth.iter().filter(|e| inside(e.2)) {
        if !tby.get(&(e.0, e.1)).is_some_and(|v| v.iter().any(|&t| (t - e.2).abs() < tol)) {
            false_ += 1;
        }
    }
    (missed, false_, n_truth)
}

pub fn load_belt(path: &str) -> Vec<Body> {
    let raw = std::fs::read(path).unwrap();
    let n = raw.len() / 32;
    (0..n)
        .map(|k| {
            let f = |q: usize| f64::from_le_bytes(raw[k * 32 + q * 8..k * 32 + q * 8 + 8].try_into().unwrap());
            Body::new(f(0), f(1), f(2), f(3))
        })
        .collect()
}

pub fn dioph_all(b: &[Body], pairs: &[(u32, u32)], rho: f64, t0: f64, t1: f64) -> (Vec<Enc>, Stats) {
    let parts = par_map(pairs.to_vec(), |chunk| {
        let mut out = Vec::new();
        let mut st = Stats::default();
        let mut tmp = Vec::new();
        for &(i, j) in chunk {
            tmp.clear();
            pair_events(&b[i as usize], &b[j as usize], rho, SAFETY, t0, t1, &mut st, &mut tmp);
            out.extend(tmp.iter().map(|&(t, d)| (i, j, t, d)));
        }
        (out, st)
    });
    let (mut all, mut st) = (Vec::new(), Stats::default());
    for (o, s) in parts {
        all.extend(o);
        st.add(&s);
    }
    (all, st)
}
