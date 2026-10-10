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
//! **The integers.** `p_t` is an `i128` word (under thrust the GR energy grows without bound as the speed approaches c)
//! at the exponent `pt_exp` fixed when the body is born (`2·ve + 64`, `ve` its velocity
//! word's exponent: a quantum 16 times `v_max·δv`). A kick adds `Δp_t = w·∂_tU_P`, the sub-quantum part carried by
//! sigma-delta like the velocity's. This does NOT yet
//! conserve the GR `J = p_t + Ω·L`: coordinate velocity is not canonical momentum, and the Cartesian rebinding offset does
//! not preserve the tube's invariants away from its anchor (see the P3' diagnostic). The fractional tick of every physical time is carried
//! the same way, so the next event's tick is a function of the integer state.
use crate::ctx::Ctx;
use crate::bind::Binding;
use crate::num::{log2_floor, Error, Res, Tick};
use emergent_space::{binding::Trajectory, orbit::{OrbitKey, Scalar}};

/// The massive tube's conserved Schwarzschild energy per rest mass, with the
/// constant rest energy removed. No Cartesian readout (or rebinding offset)
/// enters this value: it is constant throughout a compiled drift.
pub fn drift_energy(binding: &Binding) -> Res<Scalar> {
    key_energy(binding.entry.trajectory.key())
}

fn key_energy(key: OrbitKey) -> Res<Scalar> {
    if key.null {
        return Err(Error::Refused("a null tube has no energy per rest mass"));
    }
    let q = key.periapsis.reciprocal()?;
    let k = Scalar::raw(key.k as i128, -48)?;
    let eta = Scalar::ONE.sub(k)?;
    let d = k.sub(q.mul(k.mul(k)?.mul(Scalar::integer(3))?.add(eta.mul(eta)?)?)?)?;
    if !d.is_positive() {
        return Err(Error::Refused("a tube without timelike invariants"));
    }
    // L²/r_p² = q/d and E² = (1-2q)(1+q/d). Factor E²-1
    // BEFORE evaluating: subtracting 1 from E loses the weak-field energy.
    // E²-1 = q(1-2k)(1-4qk)/d; E-1 = (E²-1)/(E+1).
    let delta = q.mul(Scalar::ONE.sub(k.scale(1)?)?)?
        .mul(Scalar::ONE.sub(q.mul(k)?.scale(2)?)?)?.div(d)?;
    Ok(delta.div(Scalar::ONE.add(delta)?.sqrt()?.add(Scalar::ONE)?)?)
}

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
    let k = Scalar::raw(key.k as i128, -48)?;
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

#[cfg(test)]
mod tests {
    use super::*;
    use crate::num::{from_f64, to_f64};

    #[test]
    fn tube_energy_matches_the_independent_schwarzschild_formula() {
        for p in [10.0, 20.0, 100.0, 1000.0] {
            for e in [0.0, 0.2, 0.6] {
                let key = OrbitKey::bound(from_f64(p), (e * (1u64 << 48) as f64) as u64).unwrap();
                let expected = (((p - 2.0).powi(2) - 4.0 * e * e) / (p * (p - 3.0 - e * e))).sqrt() - 1.0;
                assert!((to_f64(key_energy(key).unwrap()) - expected).abs() < 5e-15);
            }
        }
    }

    #[test]
    fn weak_and_parabolic_energies_do_not_subtract_nearly_equal_words() {
        for exponent in [30, 80, 300] {
            for k in [1u64 << 48, 3u64 << 46, 1u64 << 47] {
                let key = OrbitKey::new(Scalar::power_of_two(exponent), k).unwrap();
                let got = key_energy(key).unwrap();
                if k == 1 << 47 {
                    assert_eq!(got, Scalar::ZERO);
                } else {
                    let k = Scalar::raw(k as i128, -48).unwrap();
                    let weak = Scalar::ONE.sub(k.scale(1).unwrap()).unwrap()
                        .div(k.scale(1).unwrap()).unwrap().scale(-(exponent as i32)).unwrap();
                    assert!(to_f64(got.div(weak).unwrap().sub(Scalar::ONE).unwrap()).abs() < 1e-8);
                }
            }
        }
    }

    #[test]
    fn the_energy_word_holds_a_tube_with_energy_beyond_one_million() {
        let k = Scalar::power_of_two(-10);
        let eta = Scalar::ONE.sub(k).unwrap();
        let a = k.mul(k).unwrap().mul(Scalar::integer(3)).unwrap().add(eta.mul(eta).unwrap()).unwrap();
        let periapsis = a.div(k).unwrap().mul(Scalar::ONE.add(Scalar::power_of_two(-40)).unwrap()).unwrap();
        let energy = key_energy(OrbitKey::new(periapsis, 1 << 38).unwrap()).unwrap();
        assert!(energy > Scalar::integer(1_000_000));
        let mut ext = Ext { pt: 0, pt_exp: -80, pt_carry: 0, dt_carry: 0,
            ds: Scalar::ONE, c: Scalar::ONE, b: Scalar::integer(B_OVER_C) };
        ext.set_pt(energy.negate()).unwrap();
        assert!(ext.pt < 0);
        assert_eq!(ext.pt_value().unwrap(), energy.negate());
        // This tests the register, not inverse fitting or a thrusting flight at γ=10^6.
    }
}
