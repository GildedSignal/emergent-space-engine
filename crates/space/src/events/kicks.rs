//! Native E/L quantum accumulation and derivative prediction. Predictions never
//! decide dynamics: a changed memo key must compile successfully before commitment.
//! This module does not choose a tidal arc or silently average a resonance.
use super::handoff::Carry;
use super::CyclePool;
use crate::{Error, Increments, Key, Result, Tangent};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct KeyCarry {
    pub energy: Carry,
    pub angular: Carry,
}
impl KeyCarry {
    pub fn new(energy_quantum: u64, angular_quantum: u64) -> Result<Self> {
        Ok(Self {
            energy: Carry::new(energy_quantum)?,
            angular: Carry::new(angular_quantum)?,
        })
    }
    /// Atomic: a refused key leaves the accumulators unchanged. Returns a compiled
    /// key id only; the caller still needs a continuity-preserving phase/orientation
    /// fit before rebinding a tube. This is not a complete physical kick resolver.
    /// Carries' output is in the public encoded Q48 E / Q32 L units.
    pub fn apply(&mut self, pool: &mut CyclePool, old_id: u32, energy: i64, angular: i64) -> Result<u32> {
        let old = pool.get(old_id)?.key;
        let mut next = *self;
        let de = next.energy.add(energy)?;
        let dl = next.angular.add(angular)?;
        if de == 0 && dl == 0 {
            *self = next;
            return Ok(old_id);
        }
        let changed = |value: u64, d: i64| u64::try_from(value as i128 + d as i128).map_err(|_| Error::Range);
        let key = Key::new(changed(old.energy.get(), de)?, changed(old.angular.get(), dl)?)?;
        let id = pool.intern(key)?; // authoritative; Tangent::predict cannot replace this
        *self = next;
        Ok(id)
    }
}

pub fn predict(response: &Tangent, base: Increments, energy: i64, angular: i64) -> Result<Increments> {
    response.predict(base, energy, angular)
}

/// Linear parent's tide on offset x: M/R³ [3 n(n·x) - x], Q30 acceleration,
/// with M/R³ in Q30, unit n in Q30 and x in Q20. This is a pointwise kernel,
/// not an integrated flyby kick or a Hill/resonance-qualified generator.
pub fn linear_tide(strength_q30: u32, direction_q30: [i32; 2], offset_q20: [i64; 2]) -> Result<[i64; 2]> {
    let norm = direction_q30.iter().map(|&n| n as i128 * n as i128).sum::<i128>();
    if (norm - (1i128 << 60)).abs() > 1 << 32 {
        return Err(Error::Range);
    }
    let dot = (direction_q30[0] as i128 * offset_q20[0] as i128 + direction_q30[1] as i128 * offset_q20[1] as i128) >> 30;
    let mut a = [0; 2];
    for i in 0..2 {
        let radial = (3 * direction_q30[i] as i128 * dot) >> 30;
        let force = (radial - offset_q20[i] as i128) * strength_q30 as i128;
        a[i] = i64::try_from(force >> 20).map_err(|_| Error::Range)?;
    }
    Ok(a)
}
