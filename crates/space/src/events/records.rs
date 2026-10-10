//! Doll records and native-scale catalogue. Doll/type belong to the population.
pub use crate::Tube;
use crate::{
    binding::Trajectory,
    orbit::{OrbitKey, Scalar, ShapeMemo},
    tube::Catalogue,
    Error, Result,
};
use std::collections::HashMap;

/// log2(M), signed Q24. Exponent range is independent of significand width.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct LogMass(pub i32);
impl LogMass {
    pub fn factor(log: i64) -> Result<Scalar> {
        let octave = log.div_euclid(1 << 24);
        let fraction = log.rem_euclid(1 << 24) as u32;
        let mut factor = Scalar::ONE;
        let mut root = Scalar::integer(2).sqrt()?;
        for bit in (0..24).rev() {
            if fraction & (1 << bit) != 0 {
                factor = factor.mul(root)?;
            }
            root = root.sqrt()?;
        }
        factor.scale(i32::try_from(octave).map_err(|_| Error::Range)?)
    }
    pub fn relative(self, parent: Self, value: Scalar) -> Result<Scalar> {
        value.mul(Self::factor(self.0 as i64 - parent.0 as i64)?)
    }
}

#[derive(Default)]
pub struct CyclePool {
    pub catalogue: Catalogue,
    shapes: ShapeMemo,
    trajectories: Vec<Trajectory>,
    ids: HashMap<OrbitKey, u32>,
}
impl CyclePool {
    pub fn intern(&mut self, key: OrbitKey) -> Result<u32> {
        if let Some(&id) = self.ids.get(&key) {
            return Ok(id);
        }
        let trajectory = Trajectory::Cycle(self.shapes.get(key)?);
        let id = self.catalogue.insert(trajectory.clone(), false)?;
        if id as usize != self.trajectories.len() {
            return Err(Error::Topology);
        }
        self.trajectories.push(trajectory);
        self.ids.insert(key, id);
        Ok(id)
    }
    pub fn get(&self, id: u32) -> Result<&Trajectory> {
        self.trajectories.get(id as usize).ok_or(Error::Range)
    }
    pub fn len(&self) -> usize {
        self.trajectories.len()
    }
    pub fn is_empty(&self) -> bool {
        self.trajectories.is_empty()
    }
}

/// Shared binary clock quantum. The population rebases its origin before i64 exhaustion.
#[derive(Clone, Copy, Default, Debug, Eq, PartialEq)]
pub struct TimeBasis {
    pub exponent: i16,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Doll {
    pub mass: LogMass,
    pub spin: crate::kerr::Spin,
    pub parent: Option<u16>,
    pub centre: Option<Tube>,
}
impl Doll {
    /// Spin is shared by every tube in the doll. The native Kerr catalogue is
    /// separate from the legacy events pool until its resolver supports spin.
    pub fn with_spin(mut self, spin: crate::kerr::Spin) -> Self {
        self.spin = spin;
        self
    }
    pub fn compile_cycle(
        &self,
        memo: &mut crate::kerr::Memo,
        p: Scalar,
        eccentricity_q48: u64,
        retrograde: bool,
    ) -> Result<std::sync::Arc<crate::kerr::Cycle>> {
        memo.bound(self.spin, p, eccentricity_q48, retrograde)
    }
    pub fn root(mass: LogMass) -> Self {
        Self {
            mass,
            spin: crate::kerr::Spin::ZERO,
            parent: None,
            centre: None,
        }
    }
    pub fn child(mass: LogMass, parent: u16, centre: Tube) -> Self {
        Self {
            mass,
            spin: crate::kerr::Spin::ZERO,
            parent: Some(parent),
            centre: Some(centre),
        }
    }
    pub fn edge_radius(&self, parent: &Self, separation: Scalar) -> Result<Scalar> {
        let ratio = self.mass.0 as i64 - parent.mass.0 as i64;
        if self.parent.is_none() || ratio >= 0 || !separation.is_positive() {
            return Err(Error::Topology);
        }
        separation.mul(LogMass::factor((2 * ratio).div_euclid(5))?)
    }
}
