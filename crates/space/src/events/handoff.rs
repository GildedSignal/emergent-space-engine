//! Event-only frame translation. This does not certify a newly fitted orbital key:
//! an authoritative key/phase resolver is still required before committing a tube.
use crate::{Error, Result};

/// Cartesian position in a common Q20 length unit, velocity in c Q30.
/// Different doll mass units must be converted explicitly before translating.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Cartesian {
    pub position: [i64; 2],
    pub velocity: [i32; 2],
}
impl Cartesian {
    pub const ZERO: Self = Self {
        position: [0; 2],
        velocity: [0; 2],
    };
    pub fn slow(self) -> bool {
        self.velocity.iter().map(|&v| v as i128 * v as i128).sum::<i128>() <= 1i128 << 56
    }
}

/// Same axes, two origins at the same event. The low-v approximation is refused
/// if either centre or the input/output body exceeds c/4 (including diagonal speeds).
pub fn translate(body: Cartesian, old: Cartesian, new: Cartesian) -> Result<Cartesian> {
    if !body.slow() || !old.slow() || !new.slow() {
        return Err(Error::Range);
    }
    let mut out = Cartesian::ZERO;
    for i in 0..2 {
        out.position[i] = body.position[i]
            .checked_add(old.position[i])
            .and_then(|x| x.checked_sub(new.position[i]))
            .ok_or(Error::Range)?;
        out.velocity[i] = i32::try_from(body.velocity[i] as i64 + old.velocity[i] as i64 - new.velocity[i] as i64).map_err(|_| Error::Range)?;
    }
    if !out.slow() {
        return Err(Error::Range);
    }
    Ok(out)
}

/// Native sigma-delta remainder. Exact integer increments may accumulate below
/// a key quantum; |remainder| < quantum. Quantum cannot change. Truncation
/// toward zero makes both signs wait until a full quantum has accumulated.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Carry {
    quantum: u64,
    remainder: i64,
}
impl Carry {
    pub fn new(quantum: u64) -> Result<Self> {
        if quantum == 0 || quantum > i64::MAX as u64 {
            return Err(Error::Range);
        }
        Ok(Self { quantum, remainder: 0 })
    }
    pub fn remainder(self) -> i64 {
        self.remainder
    }
    pub fn quantum(self) -> u64 {
        self.quantum
    }
    pub fn add(&mut self, native_increment: i64) -> Result<i64> {
        let total = self.remainder as i128 + native_increment as i128;
        let out = i64::try_from(total / self.quantum as i128).map_err(|_| Error::Range)?;
        self.remainder = (total % self.quantum as i128) as i64;
        Ok(out)
    }
}

/// Derive a same-doll Cartesian readout from the cycle's polar state. No state
/// is advanced. This accessor relies on the public u/phi and velocity units.
pub fn cartesian(state: crate::State, clockwise: bool, orientation_q30: i64) -> Result<Cartesian> {
    use crate::num::{cos, ONE};
    use crate::tables::PI;
    // Public states can be constructed by callers; enforce the compiler's u envelope
    // before a polar-to-Cartesian product, rather than relying on its provenance.
    if state.position.u < 1 << 34 {
        return Err(Error::Range);
    }
    let direction = if clockwise { -1i128 } else { 1 };
    let angle = direction * state.position.phi.get() as i128 + orientation_q30 as i128;
    // Full-turn Q61 representation; reduction happens before trig evaluation.
    let angle = (angle << 31).rem_euclid(2 * PI);
    let c = cos(if angle <= PI { angle } else { 2 * PI - angle });
    let s = if angle <= PI {
        cos((angle - PI / 2).abs())
    } else {
        -cos((angle - 3 * PI / 2).abs())
    };
    let r = (1i128 << 82).checked_div(state.position.u as i128).filter(|&r| r > 0).ok_or(Error::Range)?;
    let (vr, vt) = (state.velocity.radial as i128, direction * state.velocity.transverse as i128);
    Ok(Cartesian {
        position: [
            i64::try_from(r * c / ONE).map_err(|_| Error::Range)?,
            i64::try_from(r * s / ONE).map_err(|_| Error::Range)?,
        ],
        velocity: [
            i32::try_from((vr * c - vt * s) / ONE).map_err(|_| Error::Range)?,
            i32::try_from((vr * s + vt * c) / ONE).map_err(|_| Error::Range)?,
        ],
    })
}
