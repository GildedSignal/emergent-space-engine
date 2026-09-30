//! Compact records. E/L live in the shared key table, never in a per-body decoded state.
//! Epoch and phase are exact Q20 offsets in a population's shared epoch; out-of-range
//! offsets are refused, never truncated. The table and time basis must be charged too.
use crate::num::isqrt;
use crate::{Cycle, Error, Key, Result, State, Words};
use std::collections::HashMap;
use std::sync::Arc;

/// log2(M) in signed Q24. Quantization is a boundary conversion, not a float decision.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct LogMass(pub i32);
impl LogMass {
    /// Scale by 2^log, log in Q24. Fractional powers are defined by 24 integer
    /// square roots in Q48. This rounded exponential is the law, not real exp2.
    pub fn scale(value: u64, log: i64, ceil: bool) -> Result<u64> {
        let octave = log.div_euclid(1 << 24);
        if !(-63..=63).contains(&octave) {
            return Err(Error::Range);
        }
        let fraction = log.rem_euclid(1 << 24) as u32;
        let (mut factor, mut root) = (1u128 << 48, isqrt(2u128 << 96));
        for bit in (0..24).rev() {
            if fraction & (1 << bit) != 0 {
                factor = (factor * root) >> 48;
            }
            root = isqrt(root << 48);
        }
        let shift = 48 - octave;
        let product = value as u128 * factor;
        let scaled = if shift >= 0 {
            let shift = shift as u32;
            let add = if ceil { (1u128 << shift) - 1 } else { 0 };
            product.checked_add(add).ok_or(Error::Range)? >> shift
        } else {
            product.checked_mul(1u128 << -shift).ok_or(Error::Range)?
        };
        u64::try_from(scaled).map_err(|_| Error::Range)
    }
    pub fn relative(self, parent: Self, value: u64, ceil: bool) -> Result<u64> {
        Self::scale(value, self.0 as i64 - parent.0 as i64, ceil)
    }
}

#[derive(Default)]
pub struct CyclePool {
    // Hash iteration is never used: ids follow insertion, outcomes follow exact keys.
    ids: HashMap<Key, u32>,
    cycles: Vec<Arc<Cycle>>,
}
impl CyclePool {
    pub fn with_capacity(n: usize) -> Self {
        Self {
            ids: HashMap::with_capacity(n),
            cycles: Vec::with_capacity(n),
        }
    }
    pub fn intern(&mut self, key: Key) -> Result<u32> {
        if let Some(&id) = self.ids.get(&key) {
            return Ok(id);
        }
        let id = u32::try_from(self.cycles.len()).map_err(|_| Error::Range)?;
        let cycle = Arc::new(Cycle::compile(key)?);
        self.ids.insert(key, id);
        self.cycles.push(cycle);
        Ok(id)
    }
    pub fn get(&self, id: u32) -> Result<&Cycle> {
        self.cycles.get(id as usize).map(AsRef::as_ref).ok_or(Error::Range)
    }
    pub fn len(&self) -> usize {
        self.cycles.len()
    }
    pub fn is_empty(&self) -> bool {
        self.cycles.is_empty()
    }
}

/// Shared population epoch in the doll's coordinate clock. No hidden precision loss.
#[derive(Clone, Copy, Default, Debug, Eq, PartialEq)]
pub struct TimeBasis(pub Words);

/// A compact E/L handle, doll, type, and rebased Q20 epoch/phase. 16 bytes per
/// individual; the E/L table is additional shared storage. Phase must fit u32.
#[repr(C)]
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Tube {
    pub doll: u16,
    pub kind: u16,
    pub key: u32,
    pub epoch: u32,
    pub phase: u32,
}
impl Tube {
    pub fn new(doll: u16, kind: u16, key: u32, epoch: u64, phase: u64, basis: TimeBasis) -> Result<Self> {
        Ok(Self {
            doll,
            kind,
            key,
            epoch: u32::try_from(epoch.checked_sub(basis.0.get()).ok_or(Error::Range)?).map_err(|_| Error::Range)?,
            phase: u32::try_from(phase).map_err(|_| Error::Range)?,
        })
    }
    pub fn generator(self, basis: TimeBasis) -> Result<crate::LegacyTube> {
        Ok(crate::LegacyTube::new(
            Words::new(basis.0.get().checked_add(self.epoch as u64).ok_or(Error::Range)?),
            Words::new(self.phase as u64),
        ))
    }
    pub fn state(self, pool: &CyclePool, basis: TimeBasis, t: Words) -> Result<State> {
        self.generator(basis)?.state(pool.get(self.key)?, t)
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Doll {
    pub mass: LogMass,
    pub parent: Option<u16>,
    /// None only for a root doll; a child's centre is a tube in its parent.
    pub centre: Option<Tube>,
}
impl Doll {
    pub fn root(mass: LogMass) -> Self {
        Self {
            mass,
            parent: None,
            centre: None,
        }
    }
    pub fn child(mass: LogMass, parent: u16, centre: Tube) -> Result<Self> {
        if centre.doll != parent {
            return Err(Error::Topology);
        }
        Ok(Self {
            mass,
            parent: Some(parent),
            centre: Some(centre),
        })
    }
    /// Laplace SOI: separation * (child/parent)^(2/5), at the event's separation.
    /// It is derived rather than stored; only smaller children belong in this hierarchy.
    pub fn edge_radius(&self, parent: &Self, separation: Words) -> Result<Words> {
        let log_ratio = self.mass.0 as i64 - parent.mass.0 as i64;
        if self.parent.is_none() || log_ratio >= 0 {
            return Err(Error::Topology);
        }
        let log_edge = (2 * log_ratio).div_euclid(5);
        let edge = LogMass::scale(separation.get(), log_edge, false)?;
        if edge == 0 {
            Err(Error::Range)
        } else {
            Ok(Words::new(edge))
        }
    }
}
