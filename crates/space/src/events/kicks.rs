//! Dimensionless tide selector and E/L work along compiled geodesic arcs.
use crate::{
    binding::{cartesian, Trajectory},
    orbit::{Orbit, Scalar},
    Error, Result,
};
/// One threshold, shared by all callers: 0.08 exactly in the law's dyadic arithmetic.
pub fn tau0() -> Result<Scalar> {
    Scalar::integer(2).div(Scalar::integer(25))
}
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Regime {
    Averaged,
    Arc,
    Dense,
}

pub fn tidal_ratio(
    parent_mass: Scalar,
    own_mass: Scalar,
    apoapsis: Scalar,
    separation: Scalar,
) -> Result<Scalar> {
    if !parent_mass.is_positive()
        || !own_mass.is_positive()
        || !apoapsis.is_positive()
        || !separation.is_positive()
    {
        return Err(Error::Range);
    }
    let ratio = apoapsis.div(separation)?;
    parent_mass
        .scale(1)?
        .div(own_mass)?
        .mul(ratio.mul(ratio)?.mul(ratio)?)
}
/// Compiled mean azimuthal frequencies, including GR advance; near a low-order
/// commensurability do not average.
pub fn resonant(inner: &Orbit, outer: &Orbit) -> Result<bool> {
    let turn = Scalar::raw(2 * crate::tables::PI, -61)?;
    let ratio = outer.period()?.div(inner.period()?)?.mul(
        turn.add(inner.advance()?)?
            .div(turn.add(outer.advance()?)?)?,
    )?;
    for p in 1..=8 {
        for q in 1..=8 {
            let a = ratio.mul(Scalar::integer(p))?;
            let b = Scalar::integer(q);
            if a.sub(b)?.abs() <= a.max(b).scale(-10)? {
                return Ok(true);
            }
        }
    }
    Ok(false)
}
pub fn regime(tau: Scalar, stable: bool, resonance: bool) -> Result<Regime> {
    if tau < Scalar::ZERO {
        return Err(Error::Range);
    }
    Ok(if tau >= tau0()? || resonance {
        Regime::Dense
    } else if stable {
        Regime::Averaged
    } else {
        Regime::Arc
    })
}

/// Full differential parent force, not its linear truncation. Inputs are in the
/// same doll units: acceleration of origin is subtracted from acceleration of body.
pub fn parent_tide(mass: Scalar, centre: [Scalar; 2], offset: [Scalar; 2]) -> Result<[Scalar; 2]> {
    fn pull(mass: Scalar, x: [Scalar; 2]) -> Result<[Scalar; 2]> {
        let r2 = x[0].mul(x[0])?.add(x[1].mul(x[1])?)?;
        let k = mass.div(r2.mul(r2.sqrt()?)?)?;
        Ok([x[0].mul(k)?.negate(), x[1].mul(k)?.negate()])
    }
    let absolute = [centre[0].add(offset[0])?, centre[1].add(offset[1])?];
    let a = pull(mass, absolute)?;
    let origin = pull(mass, centre)?;
    Ok([a[0].sub(origin[0])?, a[1].sub(origin[1])?])
}
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Kick {
    pub energy: Scalar,
    pub angular: Scalar,
}
/// Fixed midpoint panels integrate v·a and x×a in time. A stable orbit is
/// averaged only by integrating its complete period; a passage uses its actual arc.
/// This first-order kernel is never used for a resonant orbit.
pub fn integrate_arc(
    trajectory: &Trajectory,
    orientation: u32,
    clockwise: bool,
    start: Scalar,
    end: Scalar,
    panels: u32,
    units: (i16, i16),
    tide: impl Fn(Scalar, [Scalar; 2]) -> Result<[Scalar; 2]>,
) -> Result<Kick> {
    if end <= start || panels == 0 {
        return Err(Error::Range);
    }
    let dt = end.sub(start)?.div(Scalar::integer(panels as i64))?;
    let mut sum = Kick {
        energy: Scalar::ZERO,
        angular: Scalar::ZERO,
    };
    for i in 0..panels {
        let time = start.add(dt.mul(Scalar::raw(2 * i as i128 + 1, -1)?)?)?;
        let state = cartesian(trajectory.state(time)?, orientation, clockwise, units)?;
        let x = state
            .position
            .map(|n| Scalar::raw(n as i128, units.0 as i32));
        let v = state
            .velocity
            .map(|n| Scalar::raw(n as i128, units.1 as i32));
        let (x, v) = ([x[0]?, x[1]?], [v[0]?, v[1]?]);
        let a = tide(time, x)?;
        sum.energy = sum
            .energy
            .add(v[0].mul(a[0])?.add(v[1].mul(a[1])?)?.mul(dt)?)?;
        sum.angular = sum
            .angular
            .add(x[0].mul(a[1])?.sub(x[1].mul(a[0])?)?.mul(dt)?)?;
    }
    Ok(sum)
}

/// Apply work/torque to the reconstructed event state. Position and the incoming
/// radial branch are retained; the new E/L determine the velocity. The binding
/// remainder includes every rounded Cartesian component, including clock fitting.
pub fn apply(
    event: &crate::tube::TubeEvent,
    catalogue: &mut crate::tube::Catalogue,
    kick: Kick,
    passage_edge: Option<Scalar>,
) -> Result<crate::tube::TubeEvent> {
    if kick.energy.is_zero() && kick.angular.is_zero() {
        return Ok(event.clone());
    }
    let mut exact = event.reconstruct(catalogue)?;
    let units = (exact.length_exponent, exact.velocity_exponent);
    let x = exact
        .position
        .map(|n| Scalar::raw(n as i128, units.0 as i32));
    let v = exact
        .velocity
        .map(|n| Scalar::raw(n as i128, units.1 as i32));
    let (x, v) = ([x[0]?, x[1]?], [v[0]?, v[1]?]);
    let r = x[0].mul(x[0])?.add(x[1].mul(x[1])?)?.sqrt()?;
    let u = r.reciprocal()?;
    let lapse = Scalar::ONE.sub(u.scale(1)?)?;
    let vr = x[0].mul(v[0])?.add(x[1].mul(v[1])?)?.div(r)?;
    let vt = x[0].mul(v[1])?.sub(x[1].mul(v[0])?)?.div(r)?;
    let kinetic = vr.mul(vr)?.div(lapse)?.add(vt.mul(vt)?)?;
    let den = lapse.sub(kinetic)?;
    if !den.is_positive() {
        return Err(Error::NoBoundOrbit);
    }
    // Compute E-1 without subtracting two near-unit numbers.
    let delta2 = kinetic.sub(u.scale(1)?.mul(lapse)?)?.div(den)?;
    let energy = delta2
        .div(Scalar::ONE.add(delta2)?.sqrt()?.add(Scalar::ONE)?)?
        .add(kick.energy)?;
    let angular = r.mul(vt)?.div(den.sqrt()?)?.add(kick.angular)?;
    let next_delta2 = energy.mul(Scalar::integer(2).add(energy)?)?;
    let e2 = Scalar::ONE.add(next_delta2)?;
    if !e2.is_positive() || angular.is_zero() {
        return Err(Error::NoBoundOrbit);
    }
    let next_den = lapse.mul(lapse)?.div(e2)?;
    let transverse = angular.mul(next_den.sqrt()?)?.div(r)?;
    let next_kinetic = lapse.mul(next_delta2.add(u.scale(1)?)?)?.div(e2)?;
    let radial2 = lapse.mul(next_kinetic.sub(transverse.mul(transverse)?)?)?;
    if radial2 < Scalar::ZERO {
        return Err(Error::NoBoundOrbit);
    }
    let radial = if vr < Scalar::ZERO {
        radial2.sqrt()?.negate()
    } else {
        radial2.sqrt()?
    };
    let n = [x[0].div(r)?, x[1].div(r)?];
    let out = [
        radial.mul(n[0])?.sub(transverse.mul(n[1])?)?,
        radial.mul(n[1])?.add(transverse.mul(n[0])?)?,
    ];
    for i in 0..2 {
        exact.velocity[i] =
            i64::try_from(out[i].fixed(-(units.1 as i32))?).map_err(|_| Error::Range)?;
    }
    super::handoff::bind(
        exact,
        event.event_time,
        event.clock_exponent,
        passage_edge,
        catalogue,
    )
}
