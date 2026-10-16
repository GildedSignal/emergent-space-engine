//! Exact event-frame conversion. Rebinding retains every Cartesian difference.
use crate::{
    binding::{IntegerState, Rebinding},
    orbit::Scalar,
    tube::{Catalogue, TubeEvent},
    Error, Result,
};
pub type Cartesian = IntegerState;

pub fn slow(state: Cartesian) -> Result<bool> {
    let square = state
        .velocity
        .iter()
        .map(|&v| (v.unsigned_abs() as u128).pow(2))
        .sum::<u128>();
    if square == 0 {
        return Ok(true);
    }
    let bits = -4 - 2 * state.velocity_exponent as i32;
    Ok(if bits < 0 {
        false
    } else if bits >= 128 {
        true
    } else {
        square <= 1u128 << bits
    })
}

/// Same axes, common integer exponents. Intermediate sums use i128; overflow
/// or a nonmatching unit is refused before any state is changed. c/4 is inclusive.
pub fn translate(body: Cartesian, old: Cartesian, new: Cartesian) -> Result<Cartesian> {
    if (body.length_exponent, body.velocity_exponent)
        != (old.length_exponent, old.velocity_exponent)
        || (body.length_exponent, body.velocity_exponent)
            != (new.length_exponent, new.velocity_exponent)
        || !slow(body)?
        || !slow(old)?
        || !slow(new)?
    {
        return Err(Error::Range);
    }
    let mut out = body;
    for i in 0..2 {
        out.position[i] = i64::try_from(
            body.position[i] as i128 + old.position[i] as i128 - new.position[i] as i128,
        )
        .map_err(|_| Error::Range)?;
        out.velocity[i] = i64::try_from(
            body.velocity[i] as i128 + old.velocity[i] as i128 - new.velocity[i] as i128,
        )
        .map_err(|_| Error::Range)?;
    }
    if !slow(out)? {
        return Err(Error::Range);
    }
    Ok(out)
}

/// Reconstruct before converting. The destination fit and its clock quantization
/// both contribute to the newly retained remainder. The source is never mutated.
pub fn rebind(
    source: &TubeEvent,
    catalogue: &mut Catalogue,
    old: Cartesian,
    new: Cartesian,
    passage_edge: Option<Scalar>,
) -> Result<TubeEvent> {
    let exact = translate(source.reconstruct(catalogue)?, old, new)?;
    bind(
        exact,
        source.event_time,
        source.clock_exponent,
        passage_edge,
        catalogue,
    )
}

pub fn bind(
    exact: Cartesian,
    time: i64,
    clock_exponent: i16,
    passage_edge: Option<Scalar>,
    catalogue: &mut Catalogue,
) -> Result<TubeEvent> {
    if !slow(exact)? {
        return Err(Error::Range);
    }
    let fit = Rebinding::from_state(
        exact,
        Scalar::raw(time as i128, clock_exponent as i32)?,
        passage_edge,
    )?;
    TubeEvent::bind(fit, catalogue, clock_exponent)
}

/// The dense order consumes this exact state, evolves it including the remainder,
/// then calls bind at the next event. Never advance the lossy sample instead.
pub fn event_state(event: &TubeEvent, catalogue: &Catalogue) -> Result<Cartesian> {
    event.reconstruct(catalogue)
}

/// Transport the remainder by consuming the reconstructed state before physical
/// evolution. The evolution operation owns the force law and returns its exact
/// integer result; rebinding never evolves or erases a correction separately.
pub fn advance(
    source: &TubeEvent,
    catalogue: &mut Catalogue,
    next_time: i64,
    passage_edge: Option<Scalar>,
    evolve: impl FnOnce(Cartesian) -> Result<Cartesian>,
) -> Result<TubeEvent> {
    if next_time < source.event_time {
        return Err(Error::Range);
    }
    let exact = evolve(source.reconstruct(catalogue)?)?;
    bind(
        exact,
        next_time,
        source.clock_exponent,
        passage_edge,
        catalogue,
    )
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
        Ok(Self {
            quantum,
            remainder: 0,
        })
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
