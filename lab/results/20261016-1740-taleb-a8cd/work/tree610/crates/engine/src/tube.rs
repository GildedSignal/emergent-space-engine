//! The frame's reference: an exact tube in the parent doll (docs/law.md, dense order).
//!
//! The frame's origin falls freely: it follows the members' centre-of-mass worldline, which is
//! a tube of the parent (`crates/space`: an orbit key, an orientation, a periapsis time). This
//! module reads that tube in lattice integers and gives the frame what it needs from it: the
//! origin's position and velocity at any tick, and the tidal tensor there.
//!
//! # Units
//!
//! `crates/space` speaks in the parent's units: lengths in `M`, speeds in `c`, times in `M/c`.
//! Phase 1 is Newtonian (the tide is `(GM/r³)(I − 3 r̂r̂ᵀ)`), so the tube is read at the
//! Newtonian scale: the parent's length unit is the power of two `ℓ` with `R/ℓ` in
//! `[2^40, 2^41)` and its speed unit is `√(μ/ℓ)`, so that `c²ℓ = μ` (`μ = GM` in lattice units).
//! The orbit's compactness is then `2^-40` and `crates/space`'s weak-field branch gives Kepler's
//! orbit, with relativistic terms of order `2^-40`. [`Units`] is the one place where the
//! parent's unit system is chosen. Phase 2 (Schwarzschild tide and geodetic precession) gives
//! it the true `M = μ/c²` and `c`, and adds the tide's relativistic terms beside [`Reference::tide`].
//!
//! # The exact remainder
//!
//! A rounded orbit fit is not injective, so a binding keeps what the fit discards, in two parts
//! (positions in `2^-32` lattice units, velocities in `2^-48`):
//!
//! - **A rotation.** The orientation is stored in 32 bits (`crates/space`'s tube), so the fit's
//!   orbit is turned by up to `2^-32` turn against the exact one, and always the same way (the
//!   fit truncates). A constant Cartesian offset cannot carry that: it would send the origin
//!   along a path whose velocity is rotated by the quantum, every binding, and rebindings
//!   accumulate (measured: a lone body, rebound every 256 chronons for ten periods, 36,000
//!   lattice units off in the along-track direction by the shear). The sub-quantum angle `δ` is kept and the
//!   readout is the fit turned by it: `(I + δJ)·decode`, `J` the quarter turn.
//! - **An offset.** What is left is the rounding of the turned fit, an integer constant: the
//!   readout at the binding tick is the exact state that was bound. Nothing is lost, and
//!   repetition telescopes.
//!
//! So `readout = (I + δJ)·decode + remainder`, with `δ` and the offset replaced at every binding.
use crate::frame::FrameError;
use emergent_lattice::law::Tick;
use emergent_space::binding::{cartesian, IntegerState, Rebinding, Trajectory};
use emergent_space::orbit::{Orbit, OrbitKey, Scalar};
use emergent_space::Error as SpaceError;

/// The parent's length unit is `R / 2^SCALE_BITS`: the orbit's compactness (Newtonian scale).
pub(crate) const SCALE_BITS: i32 = 40;
/// Exponents of the integer readout from `crates/space`: positions to 2^62 · 2^-17 ℓ (16 R),
/// velocities to 64 circular speeds, both with 56 bits at the circular orbit.
const POS_EXP: i16 = (SCALE_BITS + 4 - 61) as i16;
const VEL_EXP: i16 = (-(SCALE_BITS / 2) + 6 - 62) as i16;
/// Fraction bits of the tide matrix.
pub(crate) const TIDE_BITS: i32 = 60;

fn sp(e: SpaceError) -> FrameError {
    FrameError(format!("crates/space: {e:?}"))
}

/// The position fixed point (`2^-32` lattice units) and the velocity one (`2^-48`).
pub(crate) type State = ([i128; 2], [i128; 2]);

/// How the parent's `(M, c)` map onto the lattice.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) struct Units {
    /// `GM` in lattice units³ per chronon².
    pub(crate) mu: Scalar,
    /// The parent's length unit, in lattice units (a power of two).
    pub(crate) length: Scalar,
    /// Its speed unit, in lattice units per chronon.
    speed: Scalar,
    /// Its time unit's inverse: geometric time per chronon.
    pub(crate) rate: Scalar,
}

impl Units {
    /// The Newtonian scale for a parent of strength `mu` and an orbit near `radius`.
    pub(crate) fn newtonian(mu: Scalar, radius: i64) -> Result<Units, FrameError> {
        let m = 63 - radius.max(1).leading_zeros() as i32 - SCALE_BITS;
        let length = Scalar::power_of_two(i16::try_from(m).map_err(|_| FrameError("orbit radius outside the tube's scale".into()))?);
        let speed = mu.div(length).map_err(sp)?.sqrt().map_err(sp)?;
        let rate = speed.div(length).map_err(sp)?;
        Ok(Units { mu, length, speed, rate })
    }

    /// Geometric time of a tick.
    pub(crate) fn time(&self, tick: Tick) -> Result<Scalar, FrameError> {
        Scalar::integer(tick).mul(self.rate).map_err(sp)
    }

    fn encode(&self, (x, v): State) -> Result<IntegerState, FrameError> {
        let int = |c: i128, bits: i32, unit: Scalar, exp: i16| -> Result<i64, FrameError> {
            let s = Scalar::raw(c, -bits).map_err(sp)?.div(unit).map_err(sp)?.scale(-(exp as i32)).map_err(sp)?;
            i64::try_from(s.fixed(0).map_err(sp)?).map_err(|_| FrameError("state outside the tube's integer range".into()))
        };
        Ok(IntegerState {
            position: [int(x[0], 32, self.length, POS_EXP)?, int(x[1], 32, self.length, POS_EXP)?],
            velocity: [int(v[0], 48, self.speed, VEL_EXP)?, int(v[1], 48, self.speed, VEL_EXP)?],
            length_exponent: POS_EXP,
            velocity_exponent: VEL_EXP,
        })
    }

    fn decode(&self, s: &IntegerState) -> Result<State, FrameError> {
        let fix = |n: i64, exp: i16, unit: Scalar, bits: i32| -> Result<i128, FrameError> {
            Scalar::raw(n as i128, exp as i32).map_err(sp)?.mul(unit).map_err(sp)?.fixed(bits).map_err(sp)
        };
        Ok((
            [fix(s.position[0], POS_EXP, self.length, 32)?, fix(s.position[1], POS_EXP, self.length, 32)?],
            [fix(s.velocity[0], VEL_EXP, self.speed, 48)?, fix(s.velocity[1], VEL_EXP, self.speed, 48)?],
        ))
    }
}

/// The tube's stored record: the orbit key, its orientation (turns, Q32), its periapsis time
/// (geometric) and its sense (what `crates/space`'s `Tube` holds, without the population's clock).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) struct Spec {
    pub(crate) key: OrbitKey,
    pub(crate) angle: u32,
    pub(crate) clockwise: bool,
    pub(crate) peri_time: Scalar,
}

/// The frame's tube, bound at an event: the compiled orbit, its record and the exact remainder.
#[derive(Clone, Debug)]
pub(crate) struct Reference {
    orbit: Orbit,
    spec: Spec,
    /// The orientation the 32-bit angle could not hold: radians, about `2^-29` at most.
    delta: Scalar,
    dx: [i128; 2],
    dv: [i128; 2],
    /// The periapsis distance in lattice units: what the size rule measures the members against.
    size: i64,
}

impl Reference {
    /// The tube `spec`, with the exact state `exact` at `tick`: the remainder makes the readout
    /// equal it there.
    pub(crate) fn new(units: &Units, spec: Spec, orbit: Orbit, exact: State, tick: Tick) -> Result<Reference, FrameError> {
        let size = i64::try_from(spec.key.periapsis.mul(units.length).map_err(sp)?.fixed(0).map_err(sp)?).map_err(|_| FrameError("periapsis outside the lattice".into()))?;
        let mut r = Reference { orbit, spec, delta: Scalar::ZERO, dx: [0; 2], dv: [0; 2], size: size.max(1) };
        let (x, _) = r.geodesic(units, tick)?;
        // The turn the fit lacks: the small angle from its position to the exact one.
        let q = |c: i128| Scalar::raw(c, -32).map_err(sp);
        let (dx0, dx1, ex0, ex1) = (q(x[0])?, q(x[1])?, q(exact.0[0])?, q(exact.0[1])?);
        let cross = dx0.mul(ex1).map_err(sp)?.sub(dx1.mul(ex0).map_err(sp)?).map_err(sp)?;
        let dot = dx0.mul(ex0).map_err(sp)?.add(dx1.mul(ex1).map_err(sp)?).map_err(sp)?;
        if dot.is_positive() {
            r.delta = cross.div(dot).map_err(sp)?;
        }
        let (x, v) = r.turned(units, tick)?;
        r.dx = [exact.0[0] - x[0], exact.0[1] - x[1]];
        r.dv = [exact.1[0] - v[0], exact.1[1] - v[1]];
        Ok(r)
    }

    /// Bind the tube to the exact state `exact` at `tick` (rebinding: fit, then the remainder).
    /// Only bound (periodic) orbits are tubes of a frame.
    pub(crate) fn bind(units: &Units, exact: State, tick: Tick) -> Result<Reference, FrameError> {
        let state = units.encode(exact)?;
        let fit = Rebinding::from_state(state, units.time(tick)?, None).map_err(sp)?;
        let Trajectory::Cycle(orbit) = fit.trajectory else {
            return Err(FrameError("the origin's state is not on a bound orbit".into()));
        };
        let spec = Spec { key: orbit.key(), angle: fit.periapsis_angle, clockwise: fit.clockwise, peri_time: fit.periapsis_time };
        Reference::new(units, spec, orbit, exact, tick)
    }

    pub(crate) fn spec(&self) -> &Spec {
        &self.spec
    }

    pub(crate) fn size(&self) -> i64 {
        self.size
    }

    /// The same orbit (record) as another binding: the remainders may differ.
    pub(crate) fn same_orbit(&self, o: &Reference) -> bool {
        self.spec == o.spec
    }

    /// The tube's own readout at a tick: position and velocity of the geodesic, without the remainder.
    pub(crate) fn geodesic(&self, units: &Units, tick: Tick) -> Result<State, FrameError> {
        let t = units.time(tick)?.sub(self.spec.peri_time).map_err(sp)?;
        let state = self.orbit.signed_state(t).map_err(sp)?;
        let s = cartesian(state, self.spec.angle, self.spec.clockwise, (POS_EXP, VEL_EXP)).map_err(sp)?;
        units.decode(&s)
    }

    /// The geodesic turned by the remainder's rotation: `(I + δJ)` applied to position and velocity.
    fn turned(&self, units: &Units, tick: Tick) -> Result<State, FrameError> {
        let (x, v) = self.geodesic(units, tick)?;
        let turn = |a: [i128; 2], bits: i32| -> Result<[i128; 2], FrameError> {
            let d = |c: i128| -> Result<i128, FrameError> { self.delta.mul(Scalar::raw(c, -bits).map_err(sp)?).map_err(sp)?.fixed(bits).map_err(sp) };
            // J·(a0, a1) = (−a1, a0)
            Ok([a[0] - d(a[1])?, a[1] + d(a[0])?])
        };
        Ok((turn(x, 32)?, turn(v, 48)?))
    }

    /// The origin's position (`2^-32`) and velocity (`2^-48`) at a tick, from the parent's centre:
    /// the geodesic turned by the remainder's rotation, plus the remainder's offset.
    pub(crate) fn readout(&self, units: &Units, tick: Tick) -> Result<State, FrameError> {
        let (x, v) = self.turned(units, tick)?;
        Ok(([x[0] + self.dx[0], x[1] + self.dx[1]], [v[0] + self.dv[0], v[1] + self.dv[1]]))
    }

    /// The peak angular rate of the tube (at periapsis), radians per chronon:
    /// `√(μ(1+e)/r_p³)`. The tide's axis turns by at most this much per chronon.
    pub(crate) fn peak_rate(&self, units: &Units) -> Result<Scalar, FrameError> {
        let p = self.spec.key.periapsis;
        let p32 = p.mul(p.sqrt().map_err(sp)?).map_err(sp)?;
        let k = Scalar::raw(self.spec.key.k as i128, -48).map_err(sp)?;
        units.rate.div(p32).map_err(sp)?.div(k.sqrt().map_err(sp)?).map_err(sp)
    }

    /// `floor(log2)` of the radial period in chronons.
    pub(crate) fn period_log2(&self, units: &Units) -> Result<i32, FrameError> {
        Ok(self.orbit.period().map_err(sp)?.div(units.rate).map_err(sp)?.exponent() as i32)
    }

    /// `√(μ/r_p)`: the circular speed at the periapsis distance, lattice units per chronon.
    pub(crate) fn circular_speed(&self, units: &Units) -> Result<Scalar, FrameError> {
        let rp = self.spec.key.periapsis.mul(units.length).map_err(sp)?;
        units.mu.div(rp).map_err(sp)?.sqrt().map_err(sp)
    }

    /// The tide over an interval `h` (chronons) at `tick`: `h·(GM/r³)(3 r̂r̂ᵀ − I)`, the velocity
    /// the tide gives per unit of offset, in `2^-TIDE_BITS`. The Newtonian tidal tensor along the
    /// tube, frozen at the tick (Strang: the kick at the centre of its interval).
    pub(crate) fn tide(&self, units: &Units, tick: Tick, h: Scalar) -> Result<[[i128; 2]; 2], FrameError> {
        let (x, _) = self.readout(units, tick)?;
        let (px, py) = (Scalar::raw(x[0], -32).map_err(sp)?, Scalar::raw(x[1], -32).map_err(sp)?);
        let r2 = px.mul(px).map_err(sp)?.add(py.mul(py).map_err(sp)?).map_err(sp)?;
        let r = r2.sqrt().map_err(sp)?;
        let (c, s) = (px.div(r).map_err(sp)?, py.div(r).map_err(sp)?);
        let g = units.mu.div(r2.mul(r).map_err(sp)?).map_err(sp)?.mul(h).map_err(sp)?;
        let three = Scalar::integer(3);
        let diag = |u: Scalar| -> Result<i128, FrameError> {
            g.mul(three.mul(u.mul(u).map_err(sp)?).map_err(sp)?.sub(Scalar::ONE).map_err(sp)?).map_err(sp)?.fixed(TIDE_BITS).map_err(sp)
        };
        let off = g.mul(three).map_err(sp)?.mul(c.mul(s).map_err(sp)?).map_err(sp)?.fixed(TIDE_BITS).map_err(sp)?;
        Ok([[diag(c)?, off], [off, diag(s)?]])
    }

    pub(crate) fn digest_into(&self, h: &mut blake3::Hasher) {
        for v in [self.delta.significand() as i128, self.delta.exponent() as i128] {
            h.update(&v.to_le_bytes());
        }
        let put = |h: &mut blake3::Hasher, v: i128| {
            h.update(&v.to_le_bytes());
        };
        let s = &self.spec;
        for v in [s.key.periapsis.significand() as i128, s.key.periapsis.exponent() as i128, s.key.k as i128, s.angle as i128, s.clockwise as i128, s.peri_time.significand() as i128, s.peri_time.exponent() as i128, self.dx[0], self.dx[1], self.dv[0], self.dv[1]] {
            put(h, v);
        }
    }
}

/// The origin's state as a consumer of the battle reads it: from the parent's centre, in the
/// frame's axes, which do not rotate. The offsets are measured from the point `(radius, 0)`, and
/// `azimuth` says how the parent's original axes (which turn at `n`, the reference circle's mean
/// motion) sit against the frame's: `−n·tick`, so that turning a position by it gives the position
/// in the axes that co-rotate with the reference circle (the coordinates of a Hill-frame reading).
/// A readout convention only; the dynamics know nothing of those axes.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Tube {
    /// The origin's position from `(radius, 0)`: `2^-32` lattice units.
    pub x: [i128; 2],
    /// Its velocity: `2^-48` lattice units per chronon.
    pub v: [i128; 2],
    /// The frame's axes against the parent's original axes: radians · `2^60`, exactly `−n·tick`.
    pub azimuth: i128,
    /// The tick of the readout.
    pub tick: Tick,
    /// The readout's reference point `(radius, 0)`, and the original axes' mean motion (`n/2^60`).
    pub radius: i64,
    pub n: u64,
}

impl Tube {
    pub(crate) fn read(units: &Units, r: &Reference, tick: Tick, radius: i64, n: u64) -> Result<Tube, FrameError> {
        let (x, v) = r.readout(units, tick)?;
        Ok(Tube { x: [x[0] - ((radius as i128) << 32), x[1]], v, azimuth: -(n as i128) * tick as i128, tick, radius, n })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const R: i64 = 1000 << 22;
    const N: i128 = 1 << 46;

    fn units() -> Units {
        let n = Scalar::raw(N, -60).unwrap();
        let r = Scalar::integer(R);
        Units::newtonian(n.mul(n).unwrap().mul(r).unwrap().mul(r).unwrap().mul(r).unwrap(), R).unwrap()
    }

    /// The exact circular state at tick 0: (R, 0) and (0, n·R).
    fn circle() -> State {
        ([(R as i128) << 32, 0], [0, (N * R as i128 + (1 << 11)) >> 12])
    }

    /// Binding keeps what the fit discards: at its tick the readout is the exact state, bit for bit,
    /// for circular, eccentric, retrograde and off-axis states.
    #[test]
    fn a_binding_reads_back_the_state_it_was_given() {
        let u = units();
        let (x0, v0) = circle();
        let cases: Vec<(State, Tick)> = vec![
            ((x0, v0), 0),
            (([x0[0] + (123_456_789 << 32), 987_654_321 << 20], [v0[0] + (1 << 40) + 12345, v0[1] - (1 << 42) + 777]), 4096),
            (([-(R as i128) << 32, 1 << 31], [0, -v0[1]]), 1_000_003),
            (([(R as i128 * 3 / 5) << 32, (R as i128 * 4 / 5) << 32], [-v0[1] * 4 / 5, v0[1] * 3 / 5 + 31]), 77),
        ];
        for (exact, tick) in cases {
            let r = Reference::bind(&u, exact, tick).unwrap();
            assert_eq!(r.readout(&u, tick).unwrap(), exact, "tick {tick}");
        }
    }

    /// Rebinding every few hundred chronons for ten orbits leaves the origin where it was: the part of
    /// the state a 32-bit orientation cannot hold is carried as a rotation, not as a constant
    /// offset (which, measured, sent the origin 36,000 lattice units off along-track). The state is
    /// released at rest 3e-4·R outside the circle, so its orbit has e = 9e-4: for an exactly circular one
    /// (e < 1e-8) `crates/space`'s fit loses its eccentricity and size to the double root of its cubic
    /// (about 5e-10 of the size per fit, with a bias of 1e-11), and 4000 rebindings move the origin
    /// 10,000 units: the cost of rebinding a circle, bounded by rebinding less often.
    #[test]
    fn rebinding_every_epoch_for_ten_orbits_does_not_move_the_origin() {
        let u = units();
        let eps = 3e-4;
        let (x0, v0) = circle();
        let x = [(R as f64 * (1.0 + eps)) as i128, 0];
        let state: State = ([x[0] << 32, 0], [0, (v0[1] as f64 * (1.0 + eps)) as i128]);
        let _ = x0;
        let mut reference = Reference::bind(&u, state, 0).unwrap();
        let fixed = reference.clone();
        let (mut worst, step) = (0i128, 256);
        for j in 1..=4000i64 {
            let tick = j * step;
            let state = reference.readout(&u, tick).unwrap();
            reference = Reference::bind(&u, state, tick).unwrap();
            if j % 400 == 0 {
                let (a, b) = (reference.readout(&u, tick).unwrap().0, fixed.readout(&u, tick).unwrap().0);
                worst = worst.max((a[0] - b[0]).abs().max((a[1] - b[1]).abs()) >> 32);
            }
        }
        assert!(worst < 100, "after 4000 rebindings the origin is {worst} lattice units from the orbit it was bound to (R = {R})");
    }
}
