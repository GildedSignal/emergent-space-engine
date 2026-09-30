//! 1PN effective-one-body energy map. The relative doll uses total mass M;
//! ν appears only in the map from real binding energy to the Schwarzschild key
//! and the corresponding Hamiltonian clock conversion. No orbit fit to a judge.
use crate::{Cycle, Error, Key, Result, Words};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Binary {
    /// Reduced real binding energy, signed Q48, -1 < energy < 0.
    pub energy: i64,
    /// Reduced angular momentum in units of total M, Q32.
    pub angular: Words,
    /// Symmetric mass ratio in Q30, 0 <= ν <= 1/4.
    pub nu: u32,
}
impl Binary {
    /// E_eff = 1 + ε + (ν/2) ε². The map is the 1PN truncation;
    /// the central generator remains the exact integer Schwarzschild cycle.
    pub fn key(self) -> Result<Key> {
        if self.energy >= 0 || self.energy <= -(1 << 48) || self.nu > 1 << 28 {
            return Err(Error::Range);
        }
        let e = self.energy as i128;
        let effective = (1i128 << 48) + e + ((e * e * self.nu as i128) >> 79);
        Key::new(u64::try_from(effective).map_err(|_| Error::Range)?, self.angular.get())
    }
    /// dt_real/dt_eff = H_real/M = 1 + ν ε, from the same energy map.
    /// A derivative prediction never replaces an authoritative cycle here.
    pub fn period(self, cycle: &Cycle) -> Result<Words> {
        if cycle.key != self.key()? {
            return Err(Error::Topology);
        }
        let clock = (1i128 << 48) + ((self.energy as i128 * self.nu as i128) >> 30);
        let t = (cycle.increments.t.get() as i128 * clock) >> 48;
        Ok(Words::new(u64::try_from(t).map_err(|_| Error::Range)?))
    }
}
