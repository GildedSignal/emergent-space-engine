//! Inverse at an event. The residual is part of the answer, not optional accuracy metadata.
//! `reconstruct` is an exact left inverse; this is not a three-body conservation proof.
use crate::{
    num::{atan, cos},
    orbit::{Orbit, OrbitKey, OrbitState, Passage, Scalar},
    tables::PI,
    Error, Result,
};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct IntegerState {
    pub position: [i64; 2],
    pub velocity: [i64; 2],
    /// Values are integer * 2^exponent, in M and c respectively.
    pub length_exponent: i16,
    pub velocity_exponent: i16,
}
impl IntegerState {
    fn components(self) -> Result<([Scalar; 2], [Scalar; 2])> {
        let p = [
            Scalar::raw(self.position[0] as i128, self.length_exponent as i32)?,
            Scalar::raw(self.position[1] as i128, self.length_exponent as i32)?,
        ];
        let v = [
            Scalar::raw(self.velocity[0] as i128, self.velocity_exponent as i32)?,
            Scalar::raw(self.velocity[1] as i128, self.velocity_exponent as i32)?,
        ];
        Ok((p, v))
    }
    /// Same axes and integer units. Exact, atomic translation/boost for the existing
    /// low-speed event approximation. Relativistic boosts belong to the event resolver.
    pub fn translate(self, position: [i64; 2], velocity: [i64; 2]) -> Result<Self> {
        let mut next = self;
        for i in 0..2 {
            next.position[i] = self.position[i].checked_sub(position[i]).ok_or(Error::Range)?;
            next.velocity[i] = self.velocity[i].checked_sub(velocity[i]).ok_or(Error::Range)?;
        }
        Ok(next)
    }
}

#[derive(Clone, Debug)]
pub enum Trajectory {
    Cycle(Orbit),
    Passage(Passage),
}
impl Trajectory {
    pub fn key(&self) -> OrbitKey {
        match self {
            Self::Cycle(c) => c.key(),
            Self::Passage(p) => p.key(),
        }
    }
    pub fn state(&self, time: Scalar) -> Result<OrbitState> {
        match self {
            Self::Cycle(c) => c.signed_state(time),
            Self::Passage(p) => p.state(time),
        }
    }
    fn at_radius(&self, r: Scalar) -> Result<(Scalar, OrbitState)> {
        match self {
            Self::Cycle(c) => c.at_radius(r),
            Self::Passage(p) => p.at_radius(r),
        }
    }
}

/// Additional event storage, charged separately from a tube. Each component can require
/// 65 bits: the difference of two i64 readouts. It is not falsely called a one-ulp bound.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Residual {
    pub position: [i128; 2],
    pub velocity: [i128; 2],
}
impl Residual {
    fn between(exact: IntegerState, decoded: IntegerState) -> Self {
        Self {
            position: std::array::from_fn(|i| exact.position[i] as i128 - decoded.position[i] as i128),
            velocity: std::array::from_fn(|i| exact.velocity[i] as i128 - decoded.velocity[i] as i128),
        }
    }
    pub fn reconstruct(self, decoded: IntegerState) -> Result<IntegerState> {
        let mut out = decoded;
        for i in 0..2 {
            out.position[i] =
                i64::try_from((decoded.position[i] as i128).checked_add(self.position[i]).ok_or(Error::Range)?).map_err(|_| Error::Range)?;
            out.velocity[i] =
                i64::try_from((decoded.velocity[i] as i128).checked_add(self.velocity[i]).ok_or(Error::Range)?).map_err(|_| Error::Range)?;
        }
        Ok(out)
    }
}

/// Fit plus all discarded information at the named event. New dynamics must act on
/// `reconstruct()`, never on the lossy geodesic sample alone.
#[derive(Clone, Debug)]
pub struct Rebinding {
    pub trajectory: Trajectory,
    pub periapsis_time: Scalar,
    /// Turns, Q32, modulo one turn.
    pub periapsis_angle: u32,
    pub clockwise: bool,
    pub residual: Residual,
    pub event_time: Scalar,
    units: (i16, i16),
}

fn norm(a: [Scalar; 2]) -> Result<Scalar> {
    let hi = a[0].abs().max(a[1].abs());
    if hi.is_zero() {
        return Ok(hi);
    }
    let ratio = a[0].abs().min(a[1].abs()).div(hi)?;
    hi.mul(Scalar::ONE.add(ratio.mul(ratio)?)?.sqrt()?)
}
fn dot(a: [Scalar; 2], b: [Scalar; 2]) -> Result<Scalar> {
    a[0].mul(b[0])?.add(a[1].mul(b[1])?)
}
fn angle(x: Scalar, y: Scalar) -> Result<i128> {
    if x.is_zero() && y.is_zero() {
        return Err(Error::Range);
    }
    let (a, b) = (x.abs(), y.abs());
    let z = if a >= b {
        atan(b.div(a)?.fixed(62)?) / 2
    } else {
        PI / 2 - atan(a.div(b)?.fixed(62)?) / 2
    };
    Ok(match (x >= Scalar::ZERO, y >= Scalar::ZERO) {
        (true, true) => z,
        (false, true) => PI - z,
        (false, false) => PI + z,
        (true, false) => 2 * PI - z,
    })
}
fn phase(state: OrbitState) -> Result<i128> {
    // Reduce the azimuthal excess in turns before trig; large phases never overflow a shift.
    let turns = state.advance.div(Scalar::raw(2 * PI, -61)?)?;
    let fractional = if turns.exponent() < 0 {
        turns.fixed(61)?
    } else if turns.exponent() >= 62 {
        0
    } else {
        let bits = 62 - turns.exponent() as u32;
        (turns.significand() as i128 % (1i128 << bits)) * (1i128 << 61) / (1i128 << bits)
    };
    Ok((state.radial_angle as i128 + (((2 * PI) * fractional) >> 61)).rem_euclid(2 * PI))
}
pub fn cartesian(state: OrbitState, orientation: u32, clockwise: bool, units: (i16, i16)) -> Result<IntegerState> {
    let orientation = (orientation as i128 * (2 * PI)) >> 32;
    let phi = (orientation + if clockwise { -phase(state)? } else { phase(state)? }).rem_euclid(2 * PI);
    let c = Scalar::raw(cos(if phi <= PI { phi } else { 2 * PI - phi }), -62)?;
    let s = Scalar::raw(
        if phi <= PI {
            cos((phi - PI / 2).abs())
        } else {
            -cos((phi - 3 * PI / 2).abs())
        },
        -62,
    )?;
    let vr = state.radial_velocity;
    let vt = if clockwise {
        state.transverse_velocity.negate()
    } else {
        state.transverse_velocity
    };
    let to_int = |v: Scalar, e: i16| -> Result<i64> { i64::try_from(v.fixed(-(e as i32))?).map_err(|_| Error::Range) };
    Ok(IntegerState {
        position: [to_int(state.radius.mul(c)?, units.0)?, to_int(state.radius.mul(s)?, units.0)?],
        velocity: [
            to_int(vr.mul(c)?.sub(vt.mul(s)?)?, units.1)?,
            to_int(vr.mul(s)?.add(vt.mul(c)?)?, units.1)?,
        ],
        length_exponent: units.0,
        velocity_exponent: units.1,
    })
}

/// Inverse invariants without subtracting E from one. The cubic is in z=L²/r,
/// whose outer turning root is O(1) in the weak field, not in absolute 1/r.
fn fit_key(state: IntegerState) -> Result<(OrbitKey, Scalar, bool, bool)> {
    let (p, v) = state.components()?;
    let r = norm(p)?;
    let u = r.reciprocal()?;
    let lapse = Scalar::ONE.sub(u.scale(1)?)?;
    if !lapse.is_positive() {
        return Err(Error::NoBoundOrbit);
    }
    let vr = dot(p, v)?.div(r)?;
    let vt = p[0].mul(v[1])?.sub(p[1].mul(v[0])?)?.div(r)?;
    if crate::inverse::circular(state) {
        return Ok((OrbitKey::new(r, 1 << 48)?, r, vt < Scalar::ZERO, false));
    }
    let kinetic = vr.mul(vr)?.div(lapse)?.add(vt.mul(vt)?)?;
    let den = lapse.sub(kinetic)?;
    if !den.is_positive() || vt.is_zero() {
        return Err(Error::NoBoundOrbit);
    }
    let angular = r.mul(vt)?;
    let l2 = angular.mul(angular)?.div(den)?;
    let q = l2.reciprocal()?;
    let alpha = kinetic.sub(u.scale(1)?.mul(lapse)?)?.div(den)?.mul(l2)?;
    // The exact algebraic energy predicate preserves symbolic E=1. It also
    // defines the boundary quantization when an adapter perturbs E by less
    // than the retained shape quantum; do not manufacture a radial cycle.
    if alpha.abs() < Scalar::power_of_two(-48) {
        return Ok((crate::inverse::fit(state)?, r, vt < Scalar::ZERO, vr < Scalar::ZERO));
    }
    let disc = Scalar::ONE.sub(q.mul(Scalar::integer(12))?)?;
    if !disc.is_positive() {
        return Err(Error::NoBoundOrbit);
    }
    let root = disc.sqrt()?;
    let uc = Scalar::integer(2).div(Scalar::ONE.add(root)?)?;
    let minimum = Scalar::ONE.add(root)?.div(q.mul(Scalar::integer(6))?)?;
    let poly = |z: Scalar| -> Result<Scalar> { alpha.add(z.scale(1)?)?.sub(z.mul(z)?)?.add(q.scale(1)?.mul(z.mul(z)?.mul(z)?)?) };
    // Divide the barrier predicate by z² before evaluating: its sign is all
    // that is requested, and its absolute magnitude need not be representable.
    let inverse = minimum.reciprocal()?;
    let barrier = alpha
        .mul(inverse)?
        .mul(inverse)?
        .add(inverse.scale(1)?)?
        .sub(Scalar::ONE)?
        .add(q.scale(1)?.mul(minimum)?)?;
    if q > Scalar::power_of_two(-10) && barrier.abs() < Scalar::power_of_two(-24) {
        return Ok((crate::inverse::fit(state)?, r, vt < Scalar::ZERO, vr < Scalar::ZERO));
    }
    if barrier.is_positive() {
        return Err(Error::NoBoundOrbit);
    }
    let at_c = poly(uc)?;
    let zp = if at_c <= Scalar::ZERO {
        // Cancellation uncertainty: a handful of the 63-bit arithmetic quanta, not
        // a bound on physical eccentricity. The residual retains the input exactly.
        if at_c.abs() > Scalar::power_of_two(-56) {
            return Err(Error::NoBoundOrbit);
        }
        uc
    } else {
        let mut lo = uc;
        let mut hi = uc.scale(1)?.min(minimum);
        while poly(hi)?.is_positive() {
            lo = hi;
            hi = hi.scale(1)?.min(minimum);
            if hi == lo {
                return Err(Error::NoBoundOrbit);
            }
        }
        for _ in 0..128 {
            let mid = lo.add(hi)?.scale(-1)?;
            if mid == lo || mid == hi {
                break;
            }
            if poly(mid)?.is_positive() {
                lo = mid;
            } else {
                hi = mid;
            }
        }
        lo.add(hi)?.scale(-1)?
    };
    let rp = l2.div(zp)?;
    let compact = rp.reciprocal()?;
    let d = zp.reciprocal()?;
    let b = Scalar::ONE.add(compact.scale(1)?)?;
    let discriminant = b.mul(b)?.sub(compact.mul(Scalar::integer(16))?.mul(compact.add(d)?)?)?;
    let k = compact.add(d)?.scale(1)?.div(b.add(discriminant.sqrt()?)?)?;
    let word = u64::try_from(k.fixed(48)?).map_err(|_| Error::Range)?.min(1 << 48);
    if k.sub(Scalar::raw(word as i128, -48)?)?.abs() > k.scale(-20)? {
        return Err(Error::Range);
    }
    let mut k = word;
    // Classification follows the conserved binding energy, including a parabolic tie.
    if alpha.is_zero() {
        k = 1 << 47;
    } else if alpha.is_positive() {
        k = k.min((1 << 47) - 1);
    } else {
        k = k.max((1 << 47) + 1);
    }
    Ok((OrbitKey::new(rp, k)?, r, vt < Scalar::ZERO, vr < Scalar::ZERO))
}
impl Rebinding {
    pub fn from_state(state: IntegerState, event_time: Scalar, passage_edge: Option<Scalar>) -> Result<Self> {
        let (key, r, clockwise, incoming) = fit_key(state)?;
        let trajectory = if key.periodic() {
            Trajectory::Cycle(Orbit::compile(key)?)
        } else {
            Trajectory::Passage(Passage::compile(key, passage_edge.unwrap_or(r.scale(1)?))?)
        };
        let (mut offset, mut sample) = trajectory.at_radius(r)?;
        if incoming {
            offset = offset.negate();
            sample.reflect();
        }
        let (p, _) = state.components()?;
        let at = angle(p[0], p[1])?;
        let orientation = (at - if clockwise { -phase(sample)? } else { phase(sample)? }).rem_euclid(2 * PI);
        let periapsis_angle = ((orientation << 32) / (2 * PI)) as u32;
        let mut fit = Self {
            trajectory,
            periapsis_time: event_time.sub(offset)?,
            periapsis_angle,
            clockwise,
            residual: Residual {
                position: [0; 2],
                velocity: [0; 2],
            },
            event_time,
            units: (state.length_exponent, state.velocity_exponent),
        };
        fit.residual = Residual::between(state, fit.decoded_event()?);
        Ok(fit)
    }
    pub fn decoded_event(&self) -> Result<IntegerState> {
        cartesian(
            self.trajectory.state(self.event_time.sub(self.periapsis_time)?)?,
            self.periapsis_angle,
            self.clockwise,
            self.units,
        )
    }
    pub fn reconstruct(&self) -> Result<IntegerState> {
        self.residual.reconstruct(self.decoded_event()?)
    }
}
