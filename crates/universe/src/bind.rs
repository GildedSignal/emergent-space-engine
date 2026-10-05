//! A body's binding: the 16-byte tube of `crates/space` plus everything that makes its readout
//! exact. A tube is a key (an index into the catalogue of compiled trajectories), a periapsis
//! angle (32 bits) and a periapsis time (64 bits, in the doll's clock). A rounded fit is not
//! injective, so a binding also keeps what the fit discards (the law: "the remainder is carried
//! and never dropped"): the periapsis angle's 2^-32 turn as a **sub-quantum rotation** `delta`
//! (a constant Cartesian offset cannot carry it: it would send the body along a path whose
//! velocity is rotated by the quantum at every rebinding, and rebindings would accumulate, the
//! drift measured in `crates/engine/src/tube.rs`), and an integer **offset** (what is left after
//! the turn). The readout at any time is `turn(delta)·decode(tube, t) + offset`, and at the
//! binding event it is the bound state, bit for bit.
//!
//! The catalogue here is this crate's own: slots with a free list, so a body that rebinds gives
//! its old slot back (`crates/space`'s `Catalogue` only grows, which a body rebound a million
//! times cannot afford). A segment of history keeps its own `Arc` of the compiled trajectory, so
//! the past stays readable for the view after its slot is reused.
use crate::num::{cross2, dot2, time_of, Error, Res, Tick, V2};
use emergent_space::{
    binding::{cartesian, IntegerState, Rebinding, Residual, Trajectory},
    orbit::{OrbitState, Scalar},
    Tube,
};
use std::sync::Arc;

/// A compiled trajectory and its sense: the entry a tube's key indexes.
#[derive(Debug)]
pub struct Entry {
    pub trajectory: Trajectory,
    pub clockwise: bool,
}

/// The catalogue of compiled trajectories behind the tubes' key indexes.
#[derive(Default)]
pub struct Catalogue {
    slots: Vec<Option<Arc<Entry>>>,
    free: Vec<u32>,
}
impl Catalogue {
    pub fn insert(&mut self, e: Arc<Entry>) -> Res<u32> {
        if let Some(id) = self.free.pop() {
            self.slots[id as usize] = Some(e);
            return Ok(id);
        }
        let id = u32::try_from(self.slots.len()).map_err(|_| Error::Refused("catalogue full"))?;
        self.slots.push(Some(e));
        Ok(id)
    }
    pub fn release(&mut self, id: u32) {
        if let Some(slot) = self.slots.get_mut(id as usize) {
            if slot.take().is_some() {
                self.free.push(id);
            }
        }
    }
    pub fn get(&self, id: u32) -> Option<&Arc<Entry>> {
        self.slots.get(id as usize).and_then(|s| s.as_ref())
    }
    pub fn live(&self) -> usize {
        self.slots.len() - self.free.len()
    }
}

/// Everything needed to read one body's state at any time after its binding event.
#[derive(Clone, Debug)]
pub struct Binding {
    /// The doll whose frame the tube is in (units: that doll's `M = c = G = 1`).
    pub doll: u16,
    pub tube: Tube,
    pub entry: Arc<Entry>,
    /// What the fit discarded, exact at `event_time`: an integer offset and a sub-quantum turn.
    pub residual: Residual,
    pub delta: Scalar,
    /// Exponents of the integer state: positions `n·2^units.0`, velocities `n·2^units.1`.
    pub units: (i16, i16),
    /// The doll's clock quantum (`2^clock_exp` doll time units per tick).
    pub clock_exp: i16,
    pub event_time: Tick,
}

/// The tube's own readout (no remainder) at `t`, with the orbit state it came from.
fn decode(entry: &Entry, tube: &Tube, clock_exp: i16, units: (i16, i16), t: Tick) -> Res<(IntegerState, OrbitState)> {
    let peri = time_of(tube.periapsis_time.get() as i64, clock_exp)?;
    let elapsed = time_of(t, clock_exp)?.sub(peri)?;
    let state = entry.trajectory.state(elapsed)?;
    Ok((cartesian(state, tube.periapsis_angle, entry.clockwise, units)?, state))
}

/// `(I + δJ − δ²/2)·a`, truncated: the sub-quantum turn applied to an integer vector.
fn turn(a: [i64; 2], delta: Scalar) -> Res<[i128; 2]> {
    if delta.is_zero() {
        return Ok([a[0] as i128, a[1] as i128]);
    }
    let half = delta.mul(delta)?.scale(-1)?;
    let (x, y) = (Scalar::raw(a[0] as i128, 0)?, Scalar::raw(a[1] as i128, 0)?);
    let nx = x.sub(delta.mul(y)?)?.sub(half.mul(x)?)?;
    let ny = y.add(delta.mul(x)?)?.sub(half.mul(y)?)?;
    Ok([nx.fixed(0)?, ny.fixed(0)?])
}

impl Binding {
    /// The orbit state at `t` (proper time, radius, velocities of the tube).
    pub fn orbit_state(&self, t: Tick) -> Res<OrbitState> {
        Ok(decode(&self.entry, &self.tube, self.clock_exp, self.units, t)?.1)
    }

    /// The body's exact integer state at `t ≥ event_time`: the turned tube plus the offset. At the
    /// binding event it equals the bound state.
    pub fn readout(&self, t: Tick) -> Res<IntegerState> {
        let (d, _) = decode(&self.entry, &self.tube, self.clock_exp, self.units, t)?;
        let (p, v) = (turn(d.position, self.delta)?, turn(d.velocity, self.delta)?);
        let fit = |c: i128, r: i128| -> Res<i64> { i64::try_from(c + r).map_err(|_| Error::Refused("state outside the integer word")) };
        Ok(IntegerState {
            position: [fit(p[0], self.residual.position[0])?, fit(p[1], self.residual.position[1])?],
            velocity: [fit(v[0], self.residual.velocity[0])?, fit(v[1], self.residual.velocity[1])?],
            length_exponent: self.units.0,
            velocity_exponent: self.units.1,
        })
    }

    /// Position and velocity as scalars in the doll's units.
    pub fn cartesian(&self, t: Tick) -> Res<(V2, V2)> {
        scalars(&self.readout(t)?)
    }
}

/// An integer state as scalars (units of the doll, c = 1).
pub fn scalars(st: &IntegerState) -> Res<(V2, V2)> {
    let p = |i: usize| Scalar::raw(st.position[i] as i128, st.length_exponent as i32);
    let v = |i: usize| Scalar::raw(st.velocity[i] as i128, st.velocity_exponent as i32);
    Ok(([p(0)?, p(1)?], [v(0)?, v(1)?]))
}

/// Choose the integer word's exponents so the largest position (`r_max`) and speed (`v_max`) use
/// 60 bits: the width follows the information, not a largest test radius.
pub fn choose_units(r_max: Scalar, v_max: Scalar) -> (i16, i16) {
    ((r_max.exponent() as i32 - 60) as i16, (v_max.exponent() as i32 - 60) as i16)
}

/// The word a tube needs: the smallest exponents (coarsest units) at which its largest radius and its
/// periapsis speed (with a factor of two of margin) still fit in 60 bits.
pub fn word_for(entry: &Entry) -> Res<(i32, i32)> {
    let key = entry.trajectory.key();
    let k = Scalar::raw(key.k as i128, -48)?;
    let r_max = match &entry.trajectory {
        Trajectory::Cycle(_) => key.periapsis.div(k.scale(1)?.sub(Scalar::ONE)?)?,
        Trajectory::Passage(p) => p.outer_radius,
    };
    let v_max = Scalar::ONE.div(key.periapsis.mul(k)?)?.sqrt()?.scale(1)?;
    Ok((r_max.exponent() as i32 - 60, v_max.exponent() as i32 - 60))
}

/// The result of binding an exact state: the compiled entry and the record to store.
pub struct Bound {
    pub units: (i16, i16),
    pub entry: Arc<Entry>,
    pub tube: Tube,
    pub residual: Residual,
    pub delta: Scalar,
    pub orbit: OrbitState,
}

/// Fit a tube to the exact state `exact` at tick `t` (in a doll whose clock exponent is `clock_exp`),
/// and keep everything the fit discards. `edge` is the radius a passage is compiled out to.
pub fn bind(exact: IntegerState, t: Tick, clock_exp: i16, edge: Option<Scalar>) -> Res<Bound> {
    let bound = bind_in(exact, t, clock_exp, edge)?;
    // The integer word was chosen for an earlier orbit: when the new tube reaches farther, or is
    // faster at periapsis, than the word holds, re-express the state in coarser units (a rounding of
    // at most one quantum of the new word) and bind again.
    let (len, vel) = word_for(&bound.entry)?;
    let (cur_len, cur_vel) = (exact.length_exponent as i32, exact.velocity_exponent as i32);
    if len <= cur_len && vel <= cur_vel {
        return Ok(bound);
    }
    let (nl, nv) = (len.max(cur_len), vel.max(cur_vel));
    let shift = |v: i64, by: i32| -> i64 { if by <= 0 { v } else { v / (1i64 << by.min(62)) } };
    let coarser = IntegerState {
        position: [shift(exact.position[0], nl - cur_len), shift(exact.position[1], nl - cur_len)],
        velocity: [shift(exact.velocity[0], nv - cur_vel), shift(exact.velocity[1], nv - cur_vel)],
        length_exponent: nl as i16,
        velocity_exponent: nv as i16,
    };
    bind_in(coarser, t, clock_exp, edge)
}

fn bind_in(exact: IntegerState, t: Tick, clock_exp: i16, edge: Option<Scalar>) -> Res<Bound> {
    let fit = Rebinding::from_state(exact, time_of(t, clock_exp)?, edge)?;
    let peri = i64::try_from(fit.periapsis_time.fixed(-(clock_exp as i32))?).map_err(|_| Error::Refused("periapsis time outside the clock"))?;
    let tube = Tube::new(0, fit.periapsis_angle, peri);
    let entry = Arc::new(Entry { trajectory: fit.trajectory, clockwise: fit.clockwise });
    let units = (exact.length_exponent, exact.velocity_exponent);
    let (decoded, orbit) = decode(&entry, &tube, clock_exp, units, t)?;
    // The turn the 32-bit angle could not hold: the small angle from the decoded position to the exact one.
    let q = |a: [i64; 2]| -> Res<V2> { Ok([Scalar::raw(a[0] as i128, 0)?, Scalar::raw(a[1] as i128, 0)?]) };
    let (dp, ep) = (q(decoded.position)?, q(exact.position)?);
    let dot = dot2(dp, ep)?;
    let delta = if dot.is_positive() { cross2(dp, ep)?.div(dot)? } else { Scalar::ZERO };
    let (tp, tv) = (turn(decoded.position, delta)?, turn(decoded.velocity, delta)?);
    let residual = Residual {
        position: [exact.position[0] as i128 - tp[0], exact.position[1] as i128 - tp[1]],
        velocity: [exact.velocity[0] as i128 - tv[0], exact.velocity[1] as i128 - tv[1]],
    };
    Ok(Bound { units, entry, tube, residual, delta, orbit })
}

/// A binding with an exactly known tube and nothing to carry (a body made from its orbit).
pub fn bind_exact(entry: Arc<Entry>, tube: Tube, clock_exp: i16, units: (i16, i16), t: Tick, doll: u16) -> Binding {
    Binding {
        doll,
        tube,
        entry,
        residual: Residual { position: [0; 2], velocity: [0; 2] },
        delta: Scalar::ZERO,
        units,
        clock_exp,
        event_time: t,
    }
}
