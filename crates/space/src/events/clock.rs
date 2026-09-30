//! Derived proper clocks, in a population's explicit binary quantum.
use super::{CyclePool, TimeBasis, Tube};
use crate::{orbit::Scalar, Error, Result};
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Clock {
    pub centre: Tube,
    pub basis: TimeBasis,
    pub coordinate_epoch: i64,
    pub proper_epoch: Scalar,
}
impl Clock {
    pub fn proper_time(self, pool: &CyclePool, parent_time: i64) -> Result<Scalar> {
        let tau = self
            .centre
            .state(&pool.catalogue, parent_time, self.basis.exponent)?
            .proper_time;
        let start = self
            .centre
            .state(&pool.catalogue, self.coordinate_epoch, self.basis.exponent)?
            .proper_time;
        self.proper_epoch.add(tau.sub(start)?)
    }
    /// First tick whose derived proper time reaches the deadline. No undershoot.
    pub fn parent_time(self, pool: &CyclePool, child_time: Scalar) -> Result<Scalar> {
        if child_time < self.proper_epoch {
            return Err(Error::Range);
        }
        let mut lo = self.coordinate_epoch;
        let mut hi = lo;
        let mut span = 1i64;
        while self.proper_time(pool, hi)? < child_time {
            hi = self
                .coordinate_epoch
                .checked_add(span)
                .ok_or(Error::Range)?;
            if self.proper_time(pool, hi)? < child_time {
                span = span.checked_mul(2).ok_or(Error::Range)?;
            }
        }
        while lo < hi {
            let mid = lo + ((hi as i128 - lo as i128) / 2) as i64;
            if self.proper_time(pool, mid)? < child_time {
                lo = mid.checked_add(1).ok_or(Error::Range)?;
            } else {
                hi = mid;
            }
        }
        Scalar::raw(lo as i128, self.basis.exponent as i32)
    }
}
