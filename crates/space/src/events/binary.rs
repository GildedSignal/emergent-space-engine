//! 1PN effective-one-body map in the compiler's normalized native units.
//! Both real binding energy and angular momentum retain their own exponents.
use crate::{
    Error, Result,
    orbit::{Orbit, OrbitKey, Scalar},
};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Binary {
    /// Reduced real binding energy, -1 < energy < 0, without a fixed absolute quantum.
    pub energy: Scalar,
    /// Reduced angular momentum in units of the total mass M.
    pub angular: Scalar,
    /// Symmetric mass ratio in Q30, 0 <= ν <= 1/4.
    pub nu: u32,
}
impl Binary {
    pub fn effective_binding(self) -> Result<Scalar> {
        if self.energy >= Scalar::ZERO || self.energy <= Scalar::integer(-1) || self.nu > 1 << 28 {
            return Err(Error::Range);
        }
        self.energy.add(
            self.energy
                .mul(self.energy)?
                .mul(Scalar::raw(self.nu as i128, -31)?)?,
        )
    }
    /// E_eff-1 = ε + ν ε²/2. Never form a rounded nearly-unit E.
    pub fn key(self) -> Result<OrbitKey> {
        OrbitKey::from_invariants(self.effective_binding()?, self.angular)
    }
    /// dt_real/dt_eff = 1 + ν ε, the same Hamiltonian energy map.
    pub fn period(self, cycle: &Orbit) -> Result<Scalar> {
        if cycle.key() != self.key()? {
            return Err(Error::Topology);
        }
        let clock = Scalar::ONE.add(self.energy.mul(Scalar::raw(self.nu as i128, -30)?)?)?;
        cycle.period()?.mul(clock)
    }
}
