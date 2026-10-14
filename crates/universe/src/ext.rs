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
//! - `Δs = T/f'(c)`, rounded down to a power of two, `T` the step far from every secondary (**each body's own clock**,
//!   14 October; [`constants`]): the longest that resolves the three timescales that force the body,
//!   `T = min(2^−k_s·P, 2^−k_f·P_D, 2^−k·P_j over the secondaries j it can meet)`:
//!   - its own orbit: `P` its radial period, `k_s = Config::smooth_log2` (the lab's smooth frontier: 16 a period);
//!   - the frame's fall: the origin falls toward every secondary (the indirect term, a uniform field, the same at every body of
//!     the doll), so every body is forced at the period `P_D` of the doll's shortest secondary; `k_f = Config::forcing_log2` = 2
//!     is the cheapest measured to keep a belt's error an offset (`examples/cadence.rs`: at `k_f` = 1, or with no such term, a
//!     belt about Cinder, Home and the Giant aliases Cinder's 88 days and its eccentricity walks, growth exponent 1.0-1.1);
//!   - a passage: `P_j` the period of a secondary its orbit can meet (`k = Config::step_log2`, the price B13 is measured at).
//!     Which secondaries a body can meet is one dimensionless number per secondary: the gap between the radial ranges of the two
//!     orbits in the secondary's Hill radii, against `2√3` (Gladman's bound: orbits further apart never meet).
//!
//!   A body whose tube has no period (a passage through the system) can meet them all; the player, whose orbit is a decision,
//!   keeps the doll's clock (`2^−k·P_D`), as every body did before.
//! - **No lockstep:** a body's first step is a stub `φ·Δs`, `φ ∈ (0, 1)` a function of its id ([`phase`]), a symmetric step
//!   like the others (`D(φΔs/2)·Kc(φΔs)·D(φΔs/2)`), so that bodies born at one tick with one `Δs` never kick at one tick.
//!
//! **The integers.** `p_t` is an `i128` word (a body under thrust takes its energy toward `c²/2`, far past an orbit's: the word
//! is wide enough for any speed the law allows) at the exponent `pt_exp` fixed when the body is born (`2·ve + 64`, `ve` its velocity
//! word's exponent: a quantum 16 times `v_max·δv`, with 2^7 of headroom over `v_max²`). A kick adds the energy its quantized
//! velocity kick brings: `Δp_t = w·∂_tU_P`, the sub-quantum part carried by sigma-delta like the velocity's, so `J = p_t + Ω·L`
//! (for a source on a circle) moves by the carries only and never trends. The fractional tick of every physical time is carried
//! the same way, so the next event's tick is a function of the integer state.
use crate::bind::Binding;
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
    /// The step now running is a stub of `stub/2^16` of `Δs` (the body's first: [`phase`]); zero: a whole step.
    pub stub: u16,
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

    /// The fictitious length of the step now running: `Δs`, or the stub's `(stub/2^16)·Δs` (exact: `Δs` is a power of two).
    pub fn step(&self) -> Res<Scalar> {
        if self.stub == 0 {
            return Ok(self.ds);
        }
        Ok(Scalar::raw(self.stub as i128, -16)?.mul(self.ds)?)
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

/// The radial range and period of a bound tube, in the doll's units: `(periapsis, apoapsis, semi-major axis, radial period)`,
/// or None for a tube without a period (a passage, a plunge).
fn span(b: &Binding) -> Res<Option<(Scalar, Scalar, Scalar, Scalar)>> {
    let Trajectory::Cycle(c) = &b.entry.trajectory else { return Ok(None) };
    let key = c.key();
    let k = key.shape()?;
    let den = k.scale(1)?.sub(Scalar::ONE)?;
    if !den.is_positive() {
        return Ok(None);
    }
    // r = p/(1 + e·cos χ) with k = 1/(1 + e): periapsis `key.periapsis`, apoapsis `periapsis/(2k − 1)`, axis `periapsis·k/(2k − 1)`.
    let q = key.periapsis;
    Ok(Some((b.to_doll(q)?, b.to_doll(q.div(den)?)?, b.to_doll(q.mul(k)?.div(den)?)?, b.to_doll(c.period()?)?)))
}

/// What a source of the doll gives the clock: its strength, radial range, semi-major axis and period, in the doll's units.
struct Source {
    gm: Scalar,
    peri: Scalar,
    apo: Scalar,
    axis: Scalar,
    period: Scalar,
}

fn source(ctx: &Ctx, j: usize, t: Tick) -> Res<Source> {
    let b = ctx.bodies.binding_at(j, t).ok_or(Error::Refused("history pruned"))?;
    let Some((peri, apo, axis, period)) = span(&b)? else { return Err(Error::Refused("a source without a period")) };
    Ok(Source { gm: ctx.info[j].gm, peri, apo, axis, period })
}

/// The phase of a body's first step: the stub's share of `Δs`, in `2^-16` (1 to 65,535), from the body's id alone (splitmix64's
/// finalizer), so bodies born at one tick with one step never kick at one tick, and a body's clock is a function of what it is.
pub fn phase(id: usize) -> u16 {
    let mut z = (id as u64).wrapping_add(0x9E37_79B9_7F4A_7C15);
    z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
    z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
    z ^= z >> 31;
    (z % 65_535) as u16 + 1
}

/// The constants of the clock of a body of doll `d` (its secondaries other than `except`), read at `t`: `(Δs, c, b)`.
///
/// `own` is the body's tube when it has its own clock (a ship), None for the doll's clock (the player, and every body under
/// `Config::own_clock = false`). The step far from every secondary is `T = min(2^-k_s·P, 2^-k_f·P_D, 2^-k·P_j)` over the
/// secondaries `j` the tube can meet (module docs): the gap between the tube's radial range `[q, Q]` and the secondary's
/// `[q_j, Q_j]` is under `2√3·R_H,j`. A tube without a period can meet every secondary.
pub fn constants(ctx: &Ctx, d: u16, t: Tick, except: usize, own: Option<&Binding>) -> Res<(Scalar, Scalar, Scalar)> {
    let host = ctx.dolls[d as usize].unit.mu;
    let (k, k_s) = (ctx.cfg.step_log2, ctx.cfg.smooth_log2);
    let mine = own.map(span).transpose()?.flatten();
    let reach = Scalar::integer(12).sqrt()?; // 2√3
    let (mut c, mut floor, mut shortest, mut met) = (Scalar::ZERO, Scalar::ZERO, None::<Scalar>, None::<Scalar>);
    for &j in &ctx.sources[d as usize] {
        if j == except {
            continue;
        }
        let s = source(ctx, j, t)?;
        // The Hill radius a·(gm/3μ)^(1/3), and the potential there.
        let hill = s.axis.mul(cbrt(s.gm.div(host.mul(Scalar::integer(3))?)?)?)?;
        c = c.add(s.gm.div(hill)?)?;
        floor = floor.add(s.gm.div(s.axis)?)?;
        shortest = Some(shortest.map_or(s.period, |p| p.min(s.period)));
        let meets = match (own, mine) {
            (None, _) => false,
            (Some(_), None) => true,
            (Some(_), Some((q, apo, _, _))) => q.sub(s.apo)?.max(s.peri.sub(apo)?) < reach.mul(hill)?,
        };
        if meets {
            met = Some(met.map_or(s.period, |p| p.min(s.period)));
        }
    }
    let Some(shortest) = shortest else { return Err(Error::Refused("a doll without a source has no clock")) };
    let step = match (own, mine) {
        (None, _) => shortest.scale(-k)?,
        (Some(_), None) => met.unwrap_or(shortest).scale(-k)?,
        (Some(_), Some((_, _, _, p))) => {
            let mine = p.scale(-k_s)?.min(shortest.scale(-ctx.cfg.forcing_log2)?);
            match met {
                Some(m) => mine.min(m.scale(-k)?),
                None => mine,
            }
        }
    };
    let c = c.max(floor.mul(Scalar::integer(FLOOR_FACTOR))?);
    let b = c.mul(Scalar::integer(B_OVER_C))?;
    // Δs = T/f'(c), rounded down to a power of two.
    let ds = step.div(fprime(c, b)?)?;
    Ok((Scalar::power_of_two(log2_floor(ds) as i16), c, b))
}
