//! The extended state and the time-transformed step (docs/law.md, "Perturbed motion"; the Opus motion memo,
//! `lab/refs/opus-motion/memo.md` §2).
//!
//! A body of the root doll lives in extended phase space `(t, x; p_t, p)`: its event, its momentum and the **energy register**
//! `p_t` (an integer word, minus the body's energy in the doll's frame, perturbations included). One Hamiltonian per body,
//! in the doll's frame:
//!
//! ```text
//!   K = H_D(x, p) − U_P(x, t) + p_t ≡ 0          H_D: the drift's Hamiltonian (Kepler in the weak field)
//!   Γ = f(H_D + p_t + c) − f(U_P + c)             f'(y) = 1/y² + 1/(b·y)       (Γ ≡ 0 on K = 0)
//! ```
//!
//! `Γ` is `K` run on a **fictitious clock** `s`: on `K = 0`, `dt/ds = f'(U_P + c)`, so the physical time of one tick of `s` is a
//! fixed smooth function of the perturbing potential, and *the step is a property of the state, not a choice*. `Γ` is separable,
//! so both of its flows are exact: the **drift** `D(σ)` runs the tube for the physical time `σ·f'(H_D + p_t + c)` (`H_D` and
//! `p_t` do not change along it, so that time is known when the drift starts); the **kick** `Kc(σ)` adds `w·∇U_P` to the momentum
//! and `w·∂_tU_P` to `p_t`, `w = σ·f'(U_P + c)`. One step is `D(Δs/2)·Kc(Δs)·D(Δs/2)`, with `Δs` a power of two held by the body:
//! it is time-symmetric and symplectic, and its only error is the shadow offset of that map, a function of the current state
//! (it cannot compound). There is no step choice, no hysteresis, no level and no stub.
//!
//! **Constants, from dimensionless numbers, never fitted to a gate** (the memo, §2.2):
//! - `c_j = gm_j/R_H,j`, the secondary's potential at its Hill radius, where it stops being negligible; `c` is their sum, with a
//!   floor of `10·Σ gm_j/a_j` that keeps `U_P + c` positive for the origin's fall out to ten separations (past the doll's
//!   useful range `U_P + c` is held at `c/8`: a guard, a coarser step, not a branch of the law);
//! - `b = 30·c`: the refinement passes from `d²` to `d` (Sundman's `dt ∝ r`) at about `R_H/30`;
//! - `Δs = 2^−k·P_D/f'(c)`, rounded down to a power of two: `2^k` steps (`Config::step_log2`) per period `P_D` of the doll's
//!   shortest secondary, far from it.
//!
//! **The integers.** `p_t` is an `i128` word (a body under thrust takes its energy toward `c²/2`, far past an orbit's: the word
//! is wide enough for any speed the law allows) at the exponent `pt_exp` fixed when the body is born (`2·ve + 64`, `ve` its velocity
//! word's exponent: a quantum 16 times `v_max·δv`, with 2^7 of headroom over `v_max²`). A kick adds the energy its quantized
//! velocity kick brings: `Δp_t = w·∂_tU_P`, the sub-quantum part carried by sigma-delta like the velocity's, so `J = p_t + Ω·L`
//! (for a source on a circle) moves by the carries only and never trends. The fractional tick of every physical time is carried
//! the same way, so the next event's tick is a function of the integer state.
use crate::ctx::Ctx;
use crate::num::{log2_floor, Error, Res, Tick};
use emergent_space::{binding::Trajectory, orbit::Scalar};

/// `b = B_OVER_C·c`.
pub const B_OVER_C: i64 = 30;
/// The floor of `c`: this many times `Σ gm_j/a_j`.
pub const FLOOR_FACTOR: i64 = 10;
/// `U_P + c` is held at least at `c/2^GUARD_LOG2` (a guard beyond the useful range, see the module docs).
pub const GUARD_LOG2: i32 = 3;
/// Fractional bits of a carried physical time, in ticks.
const TICK_FRACTION: i32 = 16;

/// The extended state of one body (the root doll): the energy register and the constants of its clock.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Ext {
    /// Minus the body's energy in the doll's frame, perturbations included: `pt·2^pt_exp` (doll units).
    pub pt: i128,
    pub pt_exp: i16,
    /// The sub-quantum part of `p_t`, in `2^-16` of its quantum (sigma-delta).
    pub pt_carry: i64,
    /// The fractional tick of the physical time, in `2^-16` of a tick (sigma-delta).
    pub dt_carry: i64,
    /// The fictitious step `Δs`, a power of two.
    pub ds: Scalar,
    /// The floor of the time transformation and its break: `f'(y) = 1/y² + 1/(b·y)`.
    pub c: Scalar,
    pub b: Scalar,
}

impl Ext {
    /// `p_t` as a scalar.
    pub fn pt_value(&self) -> Res<Scalar> {
        Ok(Scalar::raw(self.pt, self.pt_exp as i32)?)
    }

    /// Set `p_t` to the scalar `v` (toward zero, at its quantum), the carry cleared: the projection onto `K = 0`.
    pub fn set_pt(&mut self, v: Scalar) -> Res<()> {
        self.pt = v.fixed(-(self.pt_exp as i32))?;
        self.pt_carry = 0;
        Ok(())
    }

    /// Add `dv` (a scalar, doll units) to `p_t` through the sigma-delta carry; the whole quanta are applied, the rest carried.
    pub fn add_pt(&mut self, dv: Scalar) -> Res<()> {
        let total = self.pt_carry as i128 + dv.fixed(-(self.pt_exp as i32) + 16)?;
        let whole = total.div_euclid(65536);
        self.pt_carry = total.rem_euclid(65536) as i64;
        self.pt = self.pt.checked_add(whole).ok_or(Error::Refused("the energy register is outside its word"))?;
        Ok(())
    }

    /// `y = max(level + c, c/2^GUARD_LOG2)`, `level` being `U_P` or `H_D + p_t`.
    pub fn y(&self, level: Scalar) -> Res<Scalar> {
        Ok(level.add(self.c)?.max(self.c.scale(-GUARD_LOG2)?))
    }

    /// The physical time of `sigma` ticks of the fictitious clock at `y`: `σ·f'(y)`, in the doll's time units.
    pub fn time(&self, y: Scalar, sigma: Scalar) -> Res<Scalar> {
        Ok(sigma.mul(fprime(y, self.b)?)?)
    }

    /// Whole ticks of the doll's clock for the time `dt` (doll time units), the fraction carried; at least one tick.
    pub fn ticks(&mut self, dt: Scalar, clock_exp: i16) -> Res<Tick> {
        let total = self.dt_carry as i128 + dt.fixed(-(clock_exp as i32) + TICK_FRACTION)?;
        let whole = total.div_euclid(1 << TICK_FRACTION).max(1);
        self.dt_carry = (total - (whole << TICK_FRACTION)) as i64;
        Tick::try_from(whole).map_err(|_| Error::Refused("a step outside the clock"))
    }
}

/// `f'(y) = 1/y² + 1/(b·y)`.
pub fn fprime(y: Scalar, b: Scalar) -> Res<Scalar> {
    let r = y.reciprocal()?;
    Ok(r.mul(r)?.add(r.div(b)?)?)
}

/// The cube root of a positive scalar: Newton's iteration from a power of two within a factor two of it, a fixed count
/// (an integer algorithm, the same bits everywhere).
pub fn cbrt(x: Scalar) -> Res<Scalar> {
    if !x.is_positive() {
        return Err(Error::Refused("the cube root of a non-positive number"));
    }
    let mut y = Scalar::power_of_two(i16::try_from((x.exponent() as i32).div_euclid(3)).map_err(|_| Error::Refused("range"))?);
    let three = Scalar::integer(3);
    for _ in 0..24 {
        y = y.scale(1)?.add(x.div(y.mul(y)?)?)?.div(three)?;
    }
    Ok(y)
}

/// What a source of the doll gives the clock: its semi-major axis and period, in the doll's units.
struct Source {
    gm: Scalar,
    axis: Scalar,
    period: Scalar,
}

fn source(ctx: &Ctx, j: usize, t: Tick) -> Res<Source> {
    let b = ctx.bodies.binding_at(j, t).ok_or(Error::Refused("history pruned"))?;
    let Trajectory::Cycle(c) = &b.entry.trajectory else { return Err(Error::Refused("a source without a period")) };
    let key = c.key();
    let k = key.shape()?;
    let den = k.scale(1)?.sub(Scalar::ONE)?;
    if !den.is_positive() {
        return Err(Error::Refused("a source on an unbound orbit"));
    }
    Ok(Source { gm: ctx.info[j].gm, axis: b.to_doll(key.periapsis.mul(k)?.div(den)?)?, period: b.to_doll(c.period()?)? })
}

/// The constants of the clock of a body of doll `d` (its secondaries other than `except`), read at `t`: `(Δs, c, b)`.
pub fn constants(ctx: &Ctx, d: u16, t: Tick, except: usize, kicks_log2: i32) -> Res<(Scalar, Scalar, Scalar)> {
    let host = ctx.dolls[d as usize].unit.mu;
    let (mut c, mut floor, mut period) = (Scalar::ZERO, Scalar::ZERO, None::<Scalar>);
    for &j in &ctx.sources[d as usize] {
        if j == except {
            continue;
        }
        let s = source(ctx, j, t)?;
        // The Hill radius a·(gm/3μ)^(1/3), and the potential there.
        let hill = s.axis.mul(cbrt(s.gm.div(host.mul(Scalar::integer(3))?)?)?)?;
        c = c.add(s.gm.div(hill)?)?;
        floor = floor.add(s.gm.div(s.axis)?)?;
        period = Some(period.map_or(s.period, |p| p.min(s.period)));
    }
    let Some(period) = period else { return Err(Error::Refused("a doll without a source has no clock")) };
    let c = c.max(floor.mul(Scalar::integer(FLOOR_FACTOR))?);
    let b = c.mul(Scalar::integer(B_OVER_C))?;
    // Δs = 2^-k·P_D/f'(c), rounded down to a power of two.
    let ds = period.scale(-kicks_log2)?.div(fprime(c, b)?)?;
    Ok((Scalar::power_of_two(log2_floor(ds) as i16), c, b))
}
