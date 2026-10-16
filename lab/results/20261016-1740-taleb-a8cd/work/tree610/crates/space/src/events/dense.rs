//! Integer dense-order fallback in separation/orbital-time units. The full parent
//! differential force is retained. This is the weak-field restricted problem,
//! not a strong-field multi-source GR solver. Sampling never changes the step sequence.
use crate::{num::isqrt, orbit::Scalar, Error, Result};
const BITS: u32 = 48;
pub const ONE: i64 = 1 << BITS;
const MAX_STEPS: u64 = 2_000_000;
fn narrow(n: i128) -> Result<i64> {
    i64::try_from(n).map_err(|_| Error::Range)
}
fn add(a: i64, b: i64) -> Result<i64> {
    a.checked_add(b).ok_or(Error::Range)
}
pub fn norm(x: [i64; 2]) -> Result<i64> {
    let sum = (x[0] as i128 * x[0] as i128)
        .checked_add(x[1] as i128 * x[1] as i128)
        .ok_or(Error::Range)?;
    narrow(isqrt(sum as u128) as i128)
}
#[derive(Clone, Copy, Debug)]
pub struct Scene {
    pub mu: i64,
    /// Planet radius and doll edge, in units of separation.
    pub radius: i64,
    pub edge: i64,
    /// Physical c-units per normalized velocity unit.
    pub speed_unit: Scalar,
}
impl Scene {
    fn force(self, q: [i64; 2]) -> Result<[i128; 2]> {
        let r = norm(q)?.max(self.radius);
        if r == 0 {
            return Err(Error::Range);
        }
        let d = [add(ONE, q[0])?, q[1]];
        let rd = norm(d)?;
        let pull = |m: i64, x: i64, r: i64| -> Result<i128> {
            if r == 0 {
                return Err(Error::Range);
            }
            let mut a = m as i128 * x as i128 / r as i128;
            for _ in 0..2 {
                a = a.checked_mul(ONE as i128).ok_or(Error::Range)? / r as i128;
            }
            Ok(a)
        };
        let star = ONE - self.mu;
        Ok([
            -pull(self.mu, q[0], r)? - pull(star, d[0], rd)? + star as i128,
            -pull(self.mu, q[1], r)? - pull(star, d[1], rd)?,
        ])
    }
    fn slow(self, v: [i64; 2]) -> Result<bool> {
        let square = v
            .iter()
            .map(|&n| (n.unsigned_abs() as u128).pow(2))
            .sum::<u128>();
        if square == 0 {
            return Ok(true);
        }
        let sig2 = (self.speed_unit.significand() as u128).pow(2);
        // speed^2 = square * sig2 * 2^(2*exponent - 220).
        // Compare the exact 256-bit product to c^2/16 without a rounded root.
        let bits = 216 - 2 * self.speed_unit.exponent() as i32;
        if bits < 0 {
            return Ok(false);
        }
        if bits >= 256 {
            return Ok(true);
        }
        let high = match crate::num::mul_shr(square, sig2, bits as u32) {
            Ok(value) => value,
            Err(Error::Range) => return Ok(false),
            Err(error) => return Err(error),
        };
        Ok(high == 0
            || (high == 1
                && square.is_power_of_two()
                && sig2.is_power_of_two()
                && square.trailing_zeros() + sig2.trailing_zeros() == bits as u32))
    }
    fn deriv(self, y: [i64; 4]) -> Result<[i128; 4]> {
        if !self.slow([y[2], y[3]])? || !self.slow([y[2], add(y[3], ONE - self.mu)?])? {
            return Err(Error::Range);
        }
        let a = self.force([y[0], y[1]])?;
        Ok([
            y[2] as i128 + y[1] as i128,
            y[3] as i128 - y[0] as i128,
            a[0] + y[3] as i128,
            a[1] - y[2] as i128,
        ])
    }
    fn rk4(self, y: [i64; 4], h: i64) -> Result<[i64; 4]> {
        let k1 = self.deriv(y)?;
        let stage = |k: [i128; 4], dt| -> Result<[i64; 4]> {
            let mut out = y;
            for i in 0..4 {
                out[i] = add(
                    y[i],
                    narrow(k[i].checked_mul(dt as i128).ok_or(Error::Range)? / ONE as i128)?,
                )?;
            }
            Ok(out)
        };
        let k2 = self.deriv(stage(k1, h / 2)?)?;
        let k3 = self.deriv(stage(k2, h / 2)?)?;
        let k4 = self.deriv(stage(k3, h)?)?;
        let mut out = y;
        for i in 0..4 {
            let sum = k1[i]
                .checked_add(k2[i].checked_mul(2).ok_or(Error::Range)?)
                .and_then(|n| n.checked_add(k3[i].checked_mul(2)?))
                .and_then(|n| n.checked_add(k4[i]))
                .ok_or(Error::Range)?;
            out[i] = add(
                y[i],
                narrow(sum.checked_mul(h as i128).ok_or(Error::Range)? / (6 * ONE as i128))?,
            )?;
        }
        Ok(out)
    }
}
#[derive(Clone, Copy, Default, Debug)]
pub struct Counts {
    pub steps: u64,
    pub force_evaluations: u64,
    pub edge_crossings: u64,
    pub readouts: u64,
}
#[derive(Clone, Debug)]
pub struct Stepper {
    pub scene: Scene,
    pub time: i64,
    pub state: [i64; 4],
    pub counts: Counts,
    step: i64,
}
impl Stepper {
    pub fn new(scene: Scene, state: [i64; 4]) -> Result<Self> {
        if scene.mu <= 0
            || scene.mu >= ONE / 2
            || scene.radius <= 0
            || scene.edge <= scene.radius
            || !scene.speed_unit.is_positive()
        {
            return Err(Error::Range);
        }
        scene.deriv(state)?;
        Ok(Self {
            scene,
            time: 0,
            state,
            step: ONE / 1024,
            counts: Counts::default(),
        })
    }
    /// An accepted physical step. Dyadic step changes use only integer local errors.
    /// No Jacobi projection, oracle or float-dependent branches.
    fn step(&mut self) -> Result<()> {
        loop {
            if self.counts.steps >= MAX_STEPS || self.step < 16 {
                return Err(Error::Range);
            }
            let full = self.scene.rk4(self.state, self.step)?;
            let half = self.scene.rk4(self.state, self.step / 2)?;
            let fine = self.scene.rk4(half, self.step / 2)?;
            self.counts.force_evaluations += 12;
            let lp = norm([self.state[0], self.state[1]])?.max(self.scene.radius);
            let lv = norm([self.state[2], self.state[3]])?.max(1);
            let acceptable = (0..4).all(|i| {
                (fine[i] as i128 - full[i] as i128).abs()
                    <= (if i < 2 { lp } else { lv }) as i128 / (1 << 30) + 4
            });
            if !acceptable {
                self.step /= 2;
                continue;
            }
            let before = norm([self.state[0], self.state[1]])? >= self.scene.edge;
            let after = norm([fine[0], fine[1]])? >= self.scene.edge;
            self.counts.edge_crossings += (before != after) as u64;
            self.state = fine;
            self.time = self.time.checked_add(self.step).ok_or(Error::Range)?;
            self.counts.steps += 1;
            let tiny = (0..4).all(|i| {
                (fine[i] as i128 - full[i] as i128).abs()
                    <= (if i < 2 { lp } else { lv }) as i128 / (1 << 36) + 1
            });
            if tiny && self.step < ONE / 128 {
                self.step *= 2;
            }
            return Ok(());
        }
    }
    /// Readout uses a temporary shortened step. The canonical state always follows
    /// its own accepted sequence, so inserting/removing observations cannot change it.
    pub fn at(&mut self, time: i64) -> Result<[i64; 4]> {
        if time < self.time {
            return Err(Error::Range);
        }
        loop {
            let mut next = self.clone();
            next.step()?;
            if next.time > time {
                // Charge the speculative step and both readout half-steps.
                self.counts.force_evaluations = next.counts.force_evaluations + 8;
                self.counts.readouts += 1;
                let left = time - self.time;
                let half = self.scene.rk4(self.state, left / 2)?;
                return self.scene.rk4(half, left - left / 2);
            }
            *self = next;
            if self.time == time {
                return Ok(self.state);
            }
        }
    }
}

/// Nonrotating Cartesian readout on the same normalized integer lattice. The
/// phase is reduced before any products; an unbounded absolute angle is never built.
pub fn inertial(state: [i64; 4], time: i64) -> Result<[i64; 4]> {
    use crate::{num::cos, tables::PI};
    let phase = ((time as i128) << 13).rem_euclid(2 * PI);
    let c = cos(if phase <= PI { phase } else { 2 * PI - phase });
    let sn = if phase <= PI {
        cos((phase - PI / 2).abs())
    } else {
        -cos((phase - 3 * PI / 2).abs())
    };
    let mut out = state;
    for i in [0, 2] {
        out[i] = narrow((state[i] as i128 * c - state[i + 1] as i128 * sn) / (1i128 << 62))?;
        out[i + 1] = narrow((state[i] as i128 * sn + state[i + 1] as i128 * c) / (1i128 << 62))?;
    }
    Ok(out)
}
