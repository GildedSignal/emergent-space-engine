//! First outgoing crossing in a native population clock. No display events.
use crate::{binding::Trajectory, orbit::Scalar, tube::Catalogue, Error, Result, Tube};

pub fn next_exit(
    trajectory: &Trajectory,
    tube: Tube,
    catalogue: &Catalogue,
    after: i64,
    clock_exponent: i16,
    edge: Scalar,
) -> Result<Option<i64>> {
    if !edge.is_positive() {
        return Err(Error::Range);
    }
    let outside =
        |t| -> Result<bool> { Ok(tube.state(catalogue, t, clock_exponent)?.radius >= edge) };
    if outside(after)? {
        return Ok(Some(after));
    }
    let peri = Scalar::raw(
        tube.periapsis_time.get() as i64 as i128,
        clock_exponent as i32,
    )?;
    let elapsed = Scalar::raw(after as i128, clock_exponent as i32)?.sub(peri)?;
    let apex = match trajectory {
        Trajectory::Cycle(c) => {
            if edge > c.signed_state(c.period()?.scale(-1)?)?.radius {
                return Ok(None);
            }
            let period = c.period()?;
            let n = elapsed.div(period)?.fixed_floor(0)?;
            let mut apex = peri
                .add(period.mul(Scalar::raw(n, 0)?)?)?
                .add(period.scale(-1)?)?;
            if apex < Scalar::raw(after as i128, clock_exponent as i32)? {
                apex = apex.add(period)?;
            }
            apex
        }
        Trajectory::Passage(p) => peri.add(p.duration()?.scale(-1)?)?,
    };
    let (mut lo, mut hi) = (
        after,
        i64::try_from(apex.fixed_ceil(-(clock_exponent as i32))?).map_err(|_| Error::Range)?,
    );
    if hi < lo || !outside(hi)? {
        return Ok(None);
    }
    while lo < hi {
        let mid = lo + ((hi as i128 - lo as i128) / 2) as i64;
        if outside(mid)? {
            hi = mid;
        } else {
            lo = mid.checked_add(1).ok_or(Error::Range)?;
        }
    }
    Ok(Some(lo))
}
