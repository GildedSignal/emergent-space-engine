//! 16-byte tube, with scale in the indexed binding and clock units in the population.
use crate::{
    binding::{self, IntegerState, Rebinding, Residual, Trajectory},
    orbit::{OrbitKey, OrbitState, Scalar},
    Error, Result, Words,
};
use std::collections::HashMap;

/// Complete per-body generator handle. Doll/type come from the owning population.
/// All 32 index bits remain available; chirality and scale live in the indexed binding.
#[repr(C)]
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Tube {
    pub key: u32,
    pub periapsis_angle: u32,
    /// Signed i64 in two storage words, using the population's binary clock quantum.
    pub periapsis_time: Words,
}
impl Tube {
    pub const fn new(key: u32, periapsis_angle: u32, periapsis_time: i64) -> Self {
        Self {
            key,
            periapsis_angle,
            periapsis_time: Words::new(periapsis_time as u64),
        }
    }
    pub fn state(self, catalogue: &Catalogue, time: i64, clock_exponent: i16) -> Result<OrbitState> {
        let entry = catalogue.entries.get(self.key as usize).ok_or(Error::Range)?;
        let elapsed = Scalar::raw(time as i128 - self.periapsis_time.get() as i64 as i128, clock_exponent as i32)?;
        let mut state = entry.trajectory.state(elapsed)?;
        let tau = 2 * crate::tables::PI;
        let base = state.radial_angle as i128;
        state.radial_angle = (((self.periapsis_angle as i128 * tau) >> 32) + if entry.clockwise { -base } else { base }).rem_euclid(tau) as u64;
        if entry.clockwise {
            state.advance = state.advance.negate();
            state.transverse_velocity = state.transverse_velocity.negate();
        }
        Ok(state)
    }
    pub fn cartesian(self, catalogue: &Catalogue, time: i64, clock_exponent: i16, units: (i16, i16)) -> Result<IntegerState> {
        binding::cartesian(self.state(catalogue, time, clock_exponent)?, 0, false, units)
    }
}
#[derive(Clone, Debug)]
struct Entry {
    trajectory: Trajectory,
    clockwise: bool,
}
#[derive(Default)]
pub struct Catalogue {
    entries: Vec<Entry>,
    ids: HashMap<(OrbitKey, bool, Option<Scalar>), u32>,
}
impl Catalogue {
    pub fn insert(&mut self, trajectory: Trajectory, clockwise: bool) -> Result<u32> {
        let edge = match &trajectory {
            Trajectory::Cycle(_) => None,
            Trajectory::Passage(p) => Some(p.outer_radius),
        };
        let key = (trajectory.key(), clockwise, edge);
        if let Some(&id) = self.ids.get(&key) {
            return Ok(id);
        }
        let id = u32::try_from(self.entries.len()).map_err(|_| Error::Range)?;
        self.entries.push(Entry { trajectory, clockwise });
        self.ids.insert(key, id);
        Ok(id)
    }
    pub fn len(&self) -> usize {
        self.entries.len()
    }
    pub fn is_empty(&self) -> bool {
        self.entries.is_empty()
    }
}

/// Tube plus its exact event residue. This storage is additional and cannot be
/// erased until the consumer has accounted for it in its authoritative event state.
#[derive(Clone, Debug)]
pub struct TubeEvent {
    pub tube: Tube,
    pub residual: Residual,
    pub event_time: i64,
    pub clock_exponent: i16,
    units: (i16, i16),
}
impl TubeEvent {
    pub fn bind(fit: Rebinding, catalogue: &mut Catalogue, clock_exponent: i16) -> Result<Self> {
        let exact = fit.reconstruct()?;
        let event_time = i64::try_from(fit.event_time.fixed(-(clock_exponent as i32))?).map_err(|_| Error::Range)?;
        // The event must be representable in this population clock. Its origin can
        // be rebased by the caller, without changing the event or losing its residue.
        if Scalar::raw(event_time as i128, clock_exponent as i32)? != fit.event_time {
            return Err(Error::Range);
        }
        let peri = i64::try_from(fit.periapsis_time.fixed(-(clock_exponent as i32))?).map_err(|_| Error::Range)?;
        let id = catalogue.insert(fit.trajectory, fit.clockwise)?;
        let tube = Tube::new(id, fit.periapsis_angle, peri);
        let units = (exact.length_exponent, exact.velocity_exponent);
        let decoded = tube.cartesian(catalogue, event_time, clock_exponent, units)?;
        let residual = Residual {
            position: std::array::from_fn(|i| exact.position[i] as i128 - decoded.position[i] as i128),
            velocity: std::array::from_fn(|i| exact.velocity[i] as i128 - decoded.velocity[i] as i128),
        };
        Ok(Self {
            tube,
            residual,
            event_time,
            clock_exponent,
            units,
        })
    }
    pub fn reconstruct(&self, catalogue: &Catalogue) -> Result<IntegerState> {
        self.residual
            .reconstruct(self.tube.cartesian(catalogue, self.event_time, self.clock_exponent, self.units)?)
    }
}
