//! Newtonian Kepler orbits in one doll (mu = 1, 2-D, prograde), with integer periods.
//!
//! Time unit: n = 1 at a = 1. The clock is integer: 2^32 ticks per time unit. A body's period and
//! periapsis time are integers (as in the law's tube), and its mean motion is derived from them.

use std::f64::consts::TAU;

pub const TICKS: f64 = 4_294_967_296.0;

#[derive(Clone, Copy, Debug)]
pub struct Body {
    pub a: f64,
    pub e: f64,
    pub pom: f64,
    pub n: f64,
    pub p: f64,
    pub sq: f64,
    pub cp: f64,
    pub sp: f64,
    /// Period in ticks.
    pub period: u64,
    /// Periapsis time in ticks, in [0, period).
    pub tp: u64,
}

impl Body {
    /// a0: nominal semi-major axis (the period is rounded to ticks), lam0: mean longitude at t = 0.
    pub fn new(a0: f64, e: f64, pom: f64, lam0: f64) -> Self {
        let period = (TAU * a0.powf(1.5) * TICKS).round() as u64;
        Self::with_period(period, e, pom, lam0)
    }

    pub fn with_period(period: u64, e: f64, pom: f64, lam0: f64) -> Self {
        let n = TAU * TICKS / period as f64;
        let a = n.powf(-2.0 / 3.0);
        let pom = pom.rem_euclid(TAU);
        let m0 = (lam0 - pom).rem_euclid(TAU);
        let tpf = (-(m0 / TAU) * period as f64).rem_euclid(period as f64);
        let tp = (tpf.round() as u64) % period;
        Body {
            a,
            e,
            pom,
            n,
            p: a * (1.0 - e * e),
            sq: (1.0 - e * e).sqrt(),
            cp: pom.cos(),
            sp: pom.sin(),
            period,
            tp,
        }
    }

    #[inline]
    pub fn rmin(&self) -> f64 {
        self.a * (1.0 - self.e)
    }

    #[inline]
    pub fn rmax(&self) -> f64 {
        self.a * (1.0 + self.e)
    }

    /// The orbit's Binet point: u(theta) = U + V cos(theta) + W sin(theta).
    #[inline]
    pub fn binet(&self) -> [f64; 3] {
        let u = 1.0 / self.p;
        [u, self.e * self.cp * u, self.e * self.sp * u]
    }

    /// Mean anomaly at time t (time units), from the integer period and periapsis time.
    #[inline]
    pub fn mean_anomaly(&self, t: f64) -> f64 {
        let x = (t * TICKS - self.tp as f64) / self.period as f64;
        TAU * (x - x.floor())
    }

    #[inline]
    fn ecc_newton(&self, m: f64) -> f64 {
        let e = self.e;
        let mut ea = m + e * m.sin() * (1.0 + e * m.cos());
        for _ in 0..12 {
            let d = (ea - e * ea.sin() - m) / (1.0 - e * ea.cos());
            ea -= d;
            if d.abs() < 1e-15 {
                break;
            }
        }
        ea
    }

    #[inline]
    fn ecc_halley(&self, m: f64) -> f64 {
        let e = self.e;
        let mut ea = m;
        for _ in 0..12 {
            let (s, c) = ea.sin_cos();
            let f = ea - e * s - m;
            let fp = 1.0 - e * c;
            let fpp = e * s;
            let d = f * fp / (fp * fp - 0.5 * f * fpp);
            ea -= d;
            if d.abs() < 1e-15 {
                break;
            }
        }
        ea
    }

    #[inline]
    fn from_ecc(&self, ea: f64) -> [f64; 4] {
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

    /// Position and velocity at time t (Newton on Kepler's equation). Used by the method.
    #[inline]
    pub fn state(&self, t: f64) -> [f64; 4] {
        self.from_ecc(self.ecc_newton(self.mean_anomaly(t)))
    }

    /// Position and velocity at mean anomaly m.
    #[inline]
    pub fn state_at_mean(&self, m: f64) -> [f64; 4] {
        self.from_ecc(self.ecc_newton(m.rem_euclid(TAU)))
    }

    /// Largest speed on the orbit (at periapsis).
    #[inline]
    pub fn vmax(&self) -> f64 {
        (1.0 + self.e) / self.p.sqrt()
    }

    /// The same state by Halley's iteration from a different start. Used by the truth only.
    #[inline]
    pub fn state_halley(&self, t: f64) -> [f64; 4] {
        self.from_ecc(self.ecc_halley(self.mean_anomaly(t)))
    }

    /// Mean anomaly at true anomaly f (closed form, no iteration).
    #[inline]
    pub fn true_to_mean(&self, f: f64) -> f64 {
        let (s, c) = (0.5 * f).sin_cos();
        let ea = 2.0 * ((1.0 - self.e).sqrt() * s).atan2((1.0 + self.e).sqrt() * c);
        (ea - self.e * ea.sin()).rem_euclid(TAU)
    }

    /// Position and velocity where the body's true longitude is theta (closed form).
    pub fn at_longitude(&self, theta: f64) -> [f64; 4] {
        let f = theta - self.pom;
        let (sf, cf) = f.sin_cos();
        let r = self.p / (1.0 + self.e * cf);
        let (st, ct) = theta.sin_cos();
        let k = (1.0 / self.p).sqrt();
        let vr = k * self.e * sf;
        let vt = k * (1.0 + self.e * cf);
        [r * ct, r * st, vr * ct - vt * st, vr * st + vt * ct]
    }

    /// Mean anomaly at true longitude theta.
    #[inline]
    pub fn mean_at_longitude(&self, theta: f64) -> f64 {
        self.true_to_mean(theta - self.pom)
    }

    /// Tick (mod period) at which the body passes true longitude theta.
    pub fn passage_tick(&self, theta: f64) -> u64 {
        let m = self.mean_at_longitude(theta);
        let off = ((m / TAU) * self.period as f64).round() as u64 % self.period;
        (self.tp + off) % self.period
    }

    /// Time (time units) to go from longitude th0 forward to th1 (in [0, period)).
    #[inline]
    pub fn travel(&self, th0: f64, th1: f64) -> f64 {
        (self.mean_at_longitude(th1) - self.mean_at_longitude(th0)).rem_euclid(TAU) / self.n
    }
}

/// Relative state (dr, dv) and the relative accelerations' difference at time t.
#[inline]
pub fn rel(bi: &Body, bj: &Body, t: f64, halley: bool) -> ([f64; 2], [f64; 2], [f64; 2]) {
    let (si, sj) = if halley {
        (bi.state_halley(t), bj.state_halley(t))
    } else {
        (bi.state(t), bj.state(t))
    };
    let ri3 = (si[0] * si[0] + si[1] * si[1]).powf(1.5);
    let rj3 = (sj[0] * sj[0] + sj[1] * sj[1]).powf(1.5);
    (
        [si[0] - sj[0], si[1] - sj[1]],
        [si[2] - sj[2], si[3] - sj[3]],
        [-si[0] / ri3 + sj[0] / rj3, -si[1] / ri3 + sj[1] / rj3],
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn closed_forms_match_kepler() {
        let b = Body::new(1.23, 0.07, 1.1, 2.9);
        for k in 0..64 {
            let theta = k as f64 * TAU / 64.0 + 0.013;
            let s1 = b.at_longitude(theta);
            let tick = b.passage_tick(theta);
            let s2 = b.state(tick as f64 / TICKS);
            for q in 0..4 {
                assert!((s1[q] - s2[q]).abs() < 1e-8, "{k} {q} {} {}", s1[q], s2[q]);
            }
            let s3 = b.state_halley(tick as f64 / TICKS + 3.0 * b.period as f64 / TICKS);
            for q in 0..4 {
                assert!((s1[q] - s3[q]).abs() < 1e-8);
            }
        }
    }
}
