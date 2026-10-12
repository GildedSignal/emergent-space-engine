//! The rung's truth, written independently of crates/encounters (no shared code path):
//! conservative advancement over every radially overlapping pair, dense in time, with no
//! conjunction logic anywhere. Kepler's equation is solved by bracketing bisection (the crate
//! uses Newton for the method and Halley for its own truth); minima are found by golden-section
//! search on the distance (the crate brackets sign changes of Δr·Δv and refines by Newton).
//!
//! Clock convention (the law's interface, shared with the code under test): a body's period is
//! an integer number of 2^32 ticks per time unit; mean motion, a, and periapsis time derive from it.

use std::f64::consts::TAU;

pub const TICKS: f64 = 4_294_967_296.0;

#[derive(Clone, Copy)]
pub struct Body {
    e: f64,
    cp: f64,
    sp: f64,
    pub n: f64,
    a: f64,
    sq: f64,
    pub period: u64,
    tp: f64,
    pub rmin: f64,
    pub rmax: f64,
}

impl Body {
    pub fn new(a0: f64, e: f64, pom: f64, lam0: f64) -> Self {
        let period = (TAU * a0.powf(1.5) * TICKS).round() as u64;
        let n = TAU * TICKS / period as f64;
        let a = n.powf(-2.0 / 3.0);
        let pom = pom.rem_euclid(TAU);
        let m0 = (lam0 - pom).rem_euclid(TAU);
        let tp = (-(m0 / TAU) * period as f64).rem_euclid(period as f64);
        Body {
            e,
            cp: pom.cos(),
            sp: pom.sin(),
            n,
            a,
            sq: (1.0 - e * e).sqrt(),
            period,
            tp,
            rmin: a * (1.0 - e),
            rmax: a * (1.0 + e),
        }
    }

    /// Position and velocity at time t (time units), full precision.
    #[inline]
    pub fn state(&self, t: f64) -> [f64; 4] {
        self.state_iters(t, 52)
    }

    /// Coarse state for certified stepping: 20 bisection halves leave |dE| <= 2e/2^21 <= 5e-7,
    /// a position error below a*1e-6, paid for by an explicit margin in the certification.
    #[inline]
    pub fn state_fast(&self, t: f64) -> [f64; 4] {
        self.state_iters(t, 20)
    }

    #[inline]
    fn state_iters(&self, t: f64, iters: u32) -> [f64; 4] {
        let x = (t * TICKS - self.tp) / self.period as f64;
        let m = TAU * (x - x.floor());
        let ea = self.solve_kepler(m, iters);
        let (se, ce) = ea.sin_cos();
        let xp = self.a * (ce - self.e);
        let yp = self.a * self.sq * se;
        let edot = self.n / (1.0 - self.e * ce);
        let vxp = -self.a * se * edot;
        let vyp = self.a * self.sq * ce * edot;
        [
            xp * self.cp - yp * self.sp,
            xp * self.sp + yp * self.cp,
            vxp * self.cp - vyp * self.sp,
            vxp * self.sp + vyp * self.cp,
        ]
    }

    /// Largest speed on the orbit (periapsis).
    #[inline]
    pub fn vmax(&self) -> f64 {
        (1.0 + self.e) / self.p_sq()
    }

    #[inline]
    fn p_sq(&self) -> f64 {
        (self.a * (1.0 - self.e * self.e)).sqrt()
    }

    /// Eccentric anomaly from mean anomaly by bisection on f(E) = E − e·sinE − m, which is
    /// strictly increasing; E lies in [m − e, m + e].
    #[inline]
    fn solve_kepler(&self, m: f64, iters: u32) -> f64 {
        let e = self.e;
        let f = |ea: f64| ea - e * ea.sin() - m;
        let (mut lo, mut hi) = (m - e, m + e);
        for _ in 0..iters {
            let mid = 0.5 * (lo + hi);
            if f(mid) < 0.0 {
                lo = mid;
            } else {
                hi = mid;
            }
        }
        0.5 * (lo + hi)
    }
}

#[inline]
fn rel(bi: &Body, bj: &Body, t: f64) -> [f64; 4] {
    let (si, sj) = (bi.state(t), bj.state(t));
    [si[0] - sj[0], si[1] - sj[1], si[2] - sj[2], si[3] - sj[3]]
}

#[inline]
fn rel_fast(bi: &Body, bj: &Body, t: f64) -> [f64; 4] {
    let (si, sj) = (bi.state_fast(t), bj.state_fast(t));
    [si[0] - sj[0], si[1] - sj[1], si[2] - sj[2], si[3] - sj[3]]
}

/// One pair: every local minimum of the distance below rho in (0, t_end), as (t, d).
///
/// Coarse steps (taken while the pair is farther than 6 rho) are certified: over [t, t+h] the
/// distance stays above 2 rho, using the exact straight-line lower bound minus half the worst
/// local curvature (each body's radius is bounded below by r(t) − vmax·h, floored at its
/// periapsis) minus the coarse-state position error. So no sub-rho minimum can hide inside a
/// coarse step. Within 6 rho the pair is stepped finely (at most 0.2 rho of relative motion per
/// step, full precision) and every sign flip of Δr·Δv with both ends under 4 rho is refined by
/// golden section; a fine step moves the pair by at most 0.2 rho, so it cannot bridge a sub-rho
/// dip. Evaluations within 12 rho of each other use the full-precision solver, so every bracket
/// that can hold a minimum is exact.
pub fn truth_pair(bi: &Body, bj: &Body, rho: f64, t_end: f64, out: &mut Vec<(f64, f64)>, evals: &mut u64) {
    let fine_zone = 6.0 * rho;
    let near_zone = 12.0 * rho;
    let h_cap = 1.2;
    let poserr = 1e-5; // bound on the coarse state's position error (see state_fast)
    let (vmax_i, vmax_j) = (bi.vmax(), bj.vmax());
    let mut t = 0.0f64;
    let mut st = rel(bi, bj, t); // full precision: golden brackets must be exact
    let (mut d, mut g) = (st[0].hypot(st[1]), st[0] * st[2] + st[1] * st[3]);
    let mut v = st[2].hypot(st[3]);
    *evals += 1;
    while t < t_end {
        let h = if d < fine_zone {
            (0.2 * rho / v.max(1e-12)).min(0.02)
        } else {
            let (rx, ry, vx, vy) = (st[0], st[1], st[2], st[3]);
            let vv = vx * vx + vy * vy;
            let (sfi, sfj) = (bi.state_fast(t), bj.state_fast(t));
            let (r_i, r_j) = (sfi[0].hypot(sfi[1]), sfj[0].hypot(sfj[1]));
            let mut h = h_cap;
            loop {
                let fl_i = (r_i - vmax_i * h).max(bi.rmin);
                let fl_j = (r_j - vmax_j * h).max(bj.rmin);
                let accel = 1.0 / (fl_i * fl_i) + 1.0 / (fl_j * fl_j);
                let mut lin = rx.hypot(ry).min((rx + vx * h).hypot(ry + vy * h));
                if vv > 0.0 {
                    let tca = -(rx * vx + ry * vy) / vv;
                    if tca > 0.0 && tca < h {
                        lin = lin.min((rx + vx * tca).hypot(ry + vy * tca));
                    }
                }
                if lin - 0.5 * accel * h * h - poserr > 2.0 * rho || h <= 1e-12 {
                    break;
                }
                h *= 0.5;
            }
            h
        };
        let tn = (t + h).min(t_end);
        let stn = if d < near_zone || (t + h) > t_end - 1.0 {
            rel(bi, bj, tn)
        } else {
            rel_fast(bi, bj, tn)
        };
        *evals += 1;
        let (dn, gn) = (stn[0].hypot(stn[1]), stn[0] * stn[2] + stn[1] * stn[3]);
        v = stn[2].hypot(stn[3]);
        if g < 0.0 && gn >= 0.0 && dn.min(d) < 4.0 * rho {
            let (tm, dm) = golden(bi, bj, t, tn, evals);
            if dm < rho && tm > 0.0 && tm < t_end {
                out.push((tm, dm));
            }
        }
        t = tn;
        st = stn;
        d = dn;
        g = gn;
    }
    let _ = poserr;
}

/// Golden-section minimum of the distance over [a, b] (the bracket before a sign flip).
fn golden(bi: &Body, bj: &Body, a: f64, b: f64, evals: &mut u64) -> (f64, f64) {
    let phi = 0.618_033_988_749_894_9;
    let dd = |t: f64| {
        let s = rel(bi, bj, t);
        s[0].hypot(s[1])
    };
    let (mut lo, mut hi) = (a, b);
    let mut x1 = hi - phi * (hi - lo);
    let mut x2 = lo + phi * (hi - lo);
    let mut f1 = dd(x1);
    let mut f2 = dd(x2);
    *evals += 2;
    for _ in 0..80 {
        if hi - lo < 1e-14 * (1.0 + a.abs()) {
            break;
        }
        if f1 < f2 {
            hi = x2;
            x2 = x1;
            f2 = f1;
            x1 = hi - phi * (hi - lo);
            f1 = dd(x1);
        } else {
            lo = x1;
            x1 = x2;
            f1 = f2;
            x2 = lo + phi * (hi - lo);
            f2 = dd(x2);
        }
        *evals += 1;
    }
    let tm = 0.5 * (lo + hi);
    (tm, dd(tm))
}

