//! Native-scale events. Only changes insert work; the compiler owns geodesic readout.
/// Experimental number/record conventions; not an integrated es-space-v2 qualification.
pub const EVENTS_ID: &str = "space-events-scaled-v3";
pub mod binary;
pub mod calendar;
pub mod clock;
pub mod dense;
pub mod edge;
pub mod handoff;
pub mod kicks;
pub mod queue;
pub mod records;

pub use calendar::Calendar;
pub use clock::Clock;
pub use queue::{Event, EventKind, EventQueue, Hierarchy};
pub use records::{CyclePool, Doll, LogMass, TimeBasis, Tube};

/// Closed-form lapse: sqrt(1 - k*u), Q48; k=2 static, k=3 circular.
/// This is a readout, not a stored/evolved clock rate.
pub fn clock_rate(u_q62: u64, k: u32) -> crate::Result<crate::Words> {
    if k != 2 && k != 3 {
        return Err(crate::Error::Range);
    }
    let lapse = (1u128 << 62)
        .checked_sub(k as u128 * u_q62 as u128)
        .ok_or(crate::Error::Range)?;
    if lapse == 0 {
        return Err(crate::Error::Range);
    }
    Ok(crate::Words::new(crate::num::isqrt(lapse << 34) as u64))
}
