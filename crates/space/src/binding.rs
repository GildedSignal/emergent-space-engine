//! Inverse at an event. The residual is part of the answer, not optional accuracy metadata.
//! `reconstruct` is an exact left inverse; this is not a three-body conservation proof.
use crate::{
    num::{atan, cos},
    orbit::{Orbit, OrbitKey, OrbitState, Passage, Scalar},
    tables::PI,
    Error, Result,
};

macro_rules! fit_stage {
    ($i:expr, $e:expr) => {{
        #[cfg(feature = "profile")]
        { crate::profile::stage($i, || $e) }
        #[cfg(not(feature = "profile"))]
        { $e }
    }};
}
/// Optional fit timings: inverse key, shape, locate event, reconstruct event.
/// Disabled builds carry no timers; this diagnostic resets the reading thread.
pub fn take_fit_profile() -> [u128; 4] {
    #[cfg(feature = "profile")]
    { crate::profile::take() }
    #[cfg(not(feature = "profile"))]
    { [0; 4] }
}

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
    Plunge(crate::plunge::Plunge),
}
impl Trajectory {
    /// A plunge has no periapsis or Darwin shape key.
    pub fn key(&self) -> Option<OrbitKey> {
        match self {
            Self::Cycle(c) => Some(c.key()),
            Self::Passage(p) => Some(p.key()),
            Self::Plunge(_) => None,
        }
    }
    pub fn state(&self, time: Scalar) -> Result<OrbitState> {
        match self {
            Self::Cycle(c) => c.signed_state(time),
            Self::Passage(p) => p.state(time),
            Self::Plunge(p) => p.orbit_state(time),
        }
    }
    fn at_radius(&self, r: Scalar) -> Result<(Scalar, OrbitState)> {
        match self {
            Self::Cycle(c) => c.at_radius(r),
            Self::Passage(p) => p.at_radius(r),
            Self::Plunge(_) => Err(Error::Topology),
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
fn fit_key(state: IntegerState, accelerate: bool) -> Result<(OrbitKey, Scalar, bool, bool)> {
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
        let witness = if accelerate { root_witness(alpha, q, lo, hi, &poly)? } else { None };
        for _ in 0..128 {
            let mid = lo.add(hi)?.scale(-1)?;
            if mid == lo || mid == hi {
                break;
            }
            let positive = match witness {
                Some((a, _)) if mid < a => true,
                Some((_, b)) if mid > b => false,
                _ => poly(mid)?.is_positive(),
            };
            if positive {
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
    if k >= Scalar::power_of_two(-28) && k.sub(Scalar::raw(word as i128, -48)?)?.abs() > k.scale(-20)? {
        return Err(Error::Range);
    }
    let scaled = k < Scalar::power_of_two(-28);
    let full_k = k;
    let mut k = word;
    // Classification follows the conserved binding energy, including a parabolic tie.
    if alpha.is_zero() {
        k = 1 << 47;
    } else if alpha.is_positive() {
        k = k.min((1 << 47) - 1);
    } else {
        k = k.max((1 << 47) + 1);
    }
    let key = if scaled { OrbitKey::scaled(rp, full_k)? } else { OrbitKey::new(rp, k)? };
    // The clock's gap, from the state and not from the key: E² = f²/den exactly (E = f·u^t), and E² = tn/d, so d = tn·den/f².
    // No cancellation, so E has no ceiling short of what the state's own words hold (k keeps the shape, which does not
    // need E: positions and velocities read k alone).
    if alpha.is_positive() && key.needs_gap()? {
        let (q, k) = (key.compactness()?, key.shape()?);
        let one_minus_2q = Scalar::ONE.sub(q.scale(1)?)?;
        let tn = k.mul(one_minus_2q)?.mul(Scalar::ONE.add(q.scale(1)?.mul(Scalar::ONE.sub(k.scale(1)?)?)?)?)?;
        let gap = tn.mul(den)?.div(lapse.mul(lapse)?)?;
        return Ok((key.with_gap(gap)?, r, vt < Scalar::ZERO, vr < Scalar::ZERO));
    }
    Ok((key, r, vt < Scalar::ZERO, vr < Scalar::ZERO))
}

/// A narrow sign witness, never a replacement root. Replay the original midpoint
/// sequence, including its final rounding, but omit polynomial evaluations outside
/// this interval. For 1 <= z <= 4, |alpha| <= 4 and 0 <= q <= 2^-18,
/// P=alpha+2z-z²+2qz³ is strictly concave (P''=-2+12qz<0).
/// The specified 63-bit operations differ from this exact dyadic polynomial by
/// less than 2^-55: z² and the two final sums each lose <2^-58; the first sum
/// loses <2^-59; rounding the cubic term contributes <2^-72. Use 2^-50 as
/// the outward witness margin, including the derivative's arithmetic error.
/// Positive endpoints certify every point to their left by concavity; a negative
/// right endpoint with negative slope certifies every point to its right.
/// Newton only proposes endpoints. Failure to certify takes the old full search.
fn root_witness(
    alpha: Scalar, q: Scalar, lo: Scalar, hi: Scalar,
    poly: &impl Fn(Scalar) -> Result<Scalar>,
) -> Result<Option<(Scalar, Scalar)>> {
    let margin = Scalar::power_of_two(-50);
    if q > Scalar::power_of_two(-18) || alpha.abs() > Scalar::integer(4)
        || lo < Scalar::ONE || hi > Scalar::integer(4) || poly(lo)? <= margin {
        return Ok(None);
    }
    let slope = |z: Scalar| -> Result<Scalar> {
        Scalar::integer(2).sub(z.scale(1)?)?.add(q.mul(Scalar::integer(6))?.mul(z.mul(z)?)?)
    };
    let mut z = lo.add(hi)?.scale(-1)?;
    // Around the critical point the cubic is a quadratic plus 2q·(z-lo)^3.
    // This seed resolves the root gap even for an almost circular weak orbit;
    // starting halfway across the whole bracket wastes Newton iterations there.
    if slope(lo)?.abs() <= margin {
        let curvature = Scalar::ONE.sub(q.mul(Scalar::integer(6))?.mul(lo)?)?;
        let seed = lo.add(poly(lo)?.div(curvature)?.sqrt()?)?;
        if seed > lo && seed < hi {
            z = seed;
        }
    }
    for _ in 0..8 {
        let d = slope(z)?;
        if d >= margin.negate() {
            return Ok(None);
        }
        let f = poly(z)?;
        if f.abs() <= margin.scale(1)? {
            break;
        }
        let next = z.sub(f.div(d)?)?;
        if next <= lo || next >= hi {
            return Ok(None);
        }
        z = next;
    }
    let d = slope(z)?;
    if d >= margin.negate() {
        return Ok(None);
    }
    let width = margin.scale(3)?.div(d.abs())?;
    let a = z.sub(width)?.max(lo);
    let b = z.add(width)?.min(hi);
    Ok(if a < b && poly(a)? > margin && poly(b)? < margin.negate()
        && slope(b)? < margin.negate() {
        Some((a, b))
    } else { None })
}
impl Rebinding {
    /// Extend the turning-orbit inverse with the arcs a state that has no periapsis to turn at needs, ending at a body's
    /// surface. A state the turning inverse takes keeps its turning orbit, whatever its periapsis: one that dips under the
    /// surface is ended where its tube meets it (the engine's `next_impact`), and the exact interval predicate of the arcs
    /// (a Bernstein certificate over rationals, milliseconds) is paid only by the states that cannot do without it: a fall
    /// toward the surface (`Plunge::from_state`, inbound or at rest) or a rise (`Plunge::outbound`). Horizon arcs use
    /// `Plunge`'s explicit falling-clock API instead.
    pub fn ending_at(state: IntegerState, event_time: Scalar, passage_edge: Option<Scalar>, surface: Scalar) -> Result<Self> {
        match Self::from_state(state, event_time, passage_edge) {
            Ok(fit) => return Ok(fit),
            Err(Error::NoBoundOrbit) => {}
            Err(e) => return Err(e),
        }
        let (p, v) = state.components()?;
        if dot(p, v)? > Scalar::ZERO {
            // Going up with no periapsis to turn at (a near-radial state): the leg up and the fall back, one arc.
            return Self::outbound_arc(state, event_time, passage_edge, surface);
        }
        let plunge = crate::plunge::Plunge::from_state(state, crate::plunge::End::Surface(surface))?;
        let periapsis_angle = ((angle(p[0], p[1])? << 32) / (2 * PI)) as u32;
        let mut fit = Self { trajectory: Trajectory::Plunge(plunge), periapsis_time: event_time,
            periapsis_angle, clockwise: false, residual: Residual { position: [0; 2], velocity: [0; 2] },
            event_time, units: (state.length_exponent, state.velocity_exponent) };
        fit.residual = Residual::between(state, fit_stage!(3, fit.decoded_event())?);
        Ok(fit)
    }
    /// An outbound near-radial state as the arc [`crate::plunge::Plunge::outbound`] compiles from its anchor (the radius it
    /// turns at, or the one past the edge it is released by): the binding's anchor is the arc's, ahead of the event by the
    /// lead, and the state is read before it, in reflection.
    fn outbound_arc(state: IntegerState, event_time: Scalar, passage_edge: Option<Scalar>, surface: Scalar) -> Result<Self> {
        // Past the doll's edge, or (the root doll has none) far past the radius a ship is lost at (2^40 root units).
        let outer = passage_edge.unwrap_or(Scalar::power_of_two(42));
        let (arc, lead) = crate::plunge::Plunge::outbound(state, crate::plunge::End::Surface(surface), outer)?;
        let trajectory = Trajectory::Plunge(arc);
        let sample = trajectory.state(lead.negate())?;
        let (p, _) = state.components()?;
        let orientation = (angle(p[0], p[1])? - phase(sample)?).rem_euclid(2 * PI);
        let mut fit = Self {
            trajectory,
            periapsis_time: event_time.add(lead)?,
            periapsis_angle: ((orientation << 32) / (2 * PI)) as u32,
            clockwise: false,
            residual: Residual { position: [0; 2], velocity: [0; 2] },
            event_time,
            units: (state.length_exponent, state.velocity_exponent),
        };
        fit.residual = Residual::between(state, fit_stage!(3, fit.decoded_event())?);
        Ok(fit)
    }
    pub fn from_state(state: IntegerState, event_time: Scalar, passage_edge: Option<Scalar>) -> Result<Self> {
        let (key, r, clockwise, incoming) = fit_stage!(0, fit_key(state, true))?;
        let trajectory = if key.periodic() {
            Trajectory::Cycle(fit_stage!(1, Orbit::compile(key))?)
        } else {
            Trajectory::Passage(fit_stage!(1, Passage::compile(key, passage_edge.unwrap_or(r.scale(1)?)))?)
        };
        let (mut offset, mut sample) = fit_stage!(2, trajectory.at_radius(r))?;
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
        fit.residual = Residual::between(state, fit_stage!(3, fit.decoded_event())?);
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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn root_witness_certifies_skipped_signs_including_small_root_gaps() {
        for qe in [18, 20, 40, 100, 1000] {
            let q = Scalar::power_of_two(-qe);
            let critical = Scalar::integer(2).div(Scalar::ONE.add(
                Scalar::ONE.sub(q.mul(Scalar::integer(12)).unwrap()).unwrap().sqrt().unwrap()
            ).unwrap()).unwrap();
            for ee in [1, 4, 10, 20] {
                let gap = Scalar::power_of_two(-ee);
                let alpha = gap.mul(gap).unwrap().sub(critical.scale(1).unwrap()).unwrap()
                    .add(critical.mul(critical).unwrap()).unwrap()
                    .sub(q.scale(1).unwrap().mul(critical.mul(critical).unwrap().mul(critical).unwrap()).unwrap()).unwrap();
                let poly = |z: Scalar| -> Result<Scalar> {
                    alpha.add(z.scale(1)?)?.sub(z.mul(z)?)?.add(q.scale(1)?.mul(z.mul(z)?.mul(z)?)?)
                };
                let mut lo = critical;
                let mut hi = critical.scale(1).unwrap();
                let (a, b) = root_witness(alpha, q, lo, hi, &poly).unwrap().expect("weak root witness");
                let mut skipped = 0;
                for _ in 0..128 {
                    let mid = lo.add(hi).unwrap().scale(-1).unwrap();
                    if mid == lo || mid == hi { break; }
                    let actual = poly(mid).unwrap().is_positive();
                    if mid < a { assert!(actual); skipped += 1; }
                    if mid > b { assert!(!actual); skipped += 1; }
                    if actual { lo = mid; } else { hi = mid; }
                }
                assert!(skipped >= 20);
            }
        }
    }

    #[test]
    fn witnessed_fit_keeps_the_full_search_key_at_kicks_and_boundaries() {
        let mut seed = 1u64;
        for radius_exp in [-1, 8, 17, 18, 19, 30, 60, 120] {
            for e in [0, 1, 1 << 20, 1 << 32, (1 << 48) / 100,
                (1 << 48) / 10, (1 << 48) / 2, (1 << 48) - (1 << 28)] {
                let key = OrbitKey::bound(Scalar::integer(16).scale(radius_exp).unwrap(), e).unwrap();
                let Ok(orbit) = Orbit::compile(key) else { continue };
                for j in 0..16 {
                    let time = orbit.period().unwrap().mul(Scalar::raw(j * 2 + 1, -5).unwrap()).unwrap();
                    let st = orbit.state(time).unwrap();
                    let units = (st.radius.exponent() - 60, st.transverse_velocity.abs().exponent() - 60);
                    let Ok(mut state) = cartesian(st, j as u32 * 0x10000000, j % 2 == 0, units) else { continue };
                    for _ in 0..8 {
                        seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1);
                        for c in &mut state.velocity {
                            *c = c.saturating_add(((seed >> 32) as i32 as i64) * 256);
                        }
                        assert_eq!(fit_key(state, true), fit_key(state, false), "{state:?}");
                    }
                }
            }
        }
    }
}
