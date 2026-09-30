//! Child proper clock -> parent's coordinate clock. The inverse is the first
//! integer coordinate time whose derived proper time is at least the deadline.
//! Whole cycles skip by Δt/Δτ; the crossing table brackets the remaining search.
use crate::{Cycle, Error, Result, Tube, Words};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Clock {
    pub centre: Tube,
    pub proper_epoch: Words,
}
impl Clock {
    /// Both clocks are normalized to the parent's mass. Convert child units once
    /// at the boundary using LogMass::relative with upward rounding for deadlines.
    pub fn parent_time(self, cycle: &Cycle, child_time: Words) -> Result<Words> {
        let delta = child_time.get().checked_sub(self.proper_epoch.get()).ok_or(Error::Range)?;
        if delta == 0 {
            return Ok(self.centre.epoch);
        }
        let start_tau = cycle.position(self.centre.phase)?.tau.get();
        let target = start_tau.checked_add(delta).ok_or(Error::Range)?;
        let t = inverse_tau(cycle, target)?.checked_sub(self.centre.phase.get()).ok_or(Error::Range)?;
        Ok(Words::new(self.centre.epoch.get().checked_add(t).ok_or(Error::Range)?))
    }
    pub fn proper_time(self, cycle: &Cycle, parent_time: Words) -> Result<Words> {
        let now = self.centre.position(cycle, parent_time)?.tau.get();
        let start = cycle.position(self.centre.phase)?.tau.get();
        Ok(Words::new(
            now.checked_sub(start)
                .and_then(|d| self.proper_epoch.get().checked_add(d))
                .ok_or(Error::Range)?,
        ))
    }
}

fn inverse_tau(cycle: &Cycle, target: u64) -> Result<u64> {
    let (period, proper) = (cycle.increments.t.get(), cycle.increments.tau.get());
    if proper == 0 || period == 0 {
        return Err(Error::NotPeriodic);
    }
    // Keep exact multiples at the end of the preceding cycle: quantized plateaux
    // may already reach the target before the nominal cycle endpoint.
    let n = target.saturating_sub(1) / proper;
    let base_t = n.checked_mul(period).ok_or(Error::Range)?;
    let base_tau = n.checked_mul(proper).ok_or(Error::Range)?;
    let rem = target - base_tau;
    let mut cuts = Vec::with_capacity(2 * cycle.crossings.len() + 3);
    cuts.push((0, 0));
    cuts.extend(cycle.crossings.iter().map(|c| (c.at.t.get(), c.at.tau.get())));
    cuts.push((cycle.half.t.get(), cycle.half.tau.get()));
    cuts.extend(cycle.crossings.iter().rev().map(|c| (period - c.at.t.get(), proper - c.at.tau.get())));
    cuts.push((period, proper));
    let hi_index = cuts.partition_point(|c| c.1 < rem);
    let (mut lo, mut hi) = (cuts[hi_index.saturating_sub(1)].0, cuts[hi_index].0);
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if cycle.position(Words::new(mid))?.tau.get() < rem {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    base_t.checked_add(lo).ok_or(Error::Range)
}
