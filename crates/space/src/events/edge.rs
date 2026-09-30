//! A radial doll-edge certificate for a member of that doll. The integer
//! outbound cycle is monotone in radius, so one bisection finds the next exit.
//! Entering another moving doll needs a separate relative-trajectory certificate.
use crate::{Cycle, Error, Result, Tube, Words};

/// First coordinate time >= after at which r >= edge. No band-crossing or
/// display events are inserted. Radius is in this doll's own Q20 length units.
pub fn next_exit(cycle: &Cycle, tube: Tube, after: Words, edge: Words) -> Result<Option<Words>> {
    if edge.get() == 0 {
        return Err(Error::Range);
    }
    let since = after.get().checked_sub(tube.epoch.get()).ok_or(Error::Range)?;
    let elapsed = since.checked_add(tube.phase.get()).ok_or(Error::Range)?;
    let outside = |t: u64| -> Result<bool> {
        let u = cycle.position(Words::new(t))?.u;
        if u <= 0 {
            return Err(Error::Range);
        }
        Ok(u as u128 * edge.get() as u128 <= 1u128 << 82)
    };
    if outside(elapsed)? {
        return Ok(Some(after));
    }
    if !outside(cycle.half.t.get())? {
        return Ok(None);
    }
    let (mut lo, mut hi) = (0, cycle.half.t.get());
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if outside(mid)? {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    let period = cycle.increments.t.get();
    if period == 0 {
        return Err(Error::NotPeriodic);
    }
    let mut crossing = (elapsed / period)
        .checked_mul(period)
        .and_then(|base| base.checked_add(lo))
        .ok_or(Error::Range)?;
    if crossing < elapsed {
        crossing = crossing.checked_add(period).ok_or(Error::Range)?;
    }
    Ok(Some(Words::new(
        crossing
            .checked_sub(tube.phase.get())
            .and_then(|t| t.checked_add(tube.epoch.get()))
            .ok_or(Error::Range)?,
    )))
}
