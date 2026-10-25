//! A body's binding: the 16-byte tube of `crates/space` plus everything that makes its readout
//! exact. A tube is a key (an index into the catalogue of compiled trajectories), a periapsis
//! angle (32 bits) and a periapsis time (64 bits, in the doll's clock). A rounded fit is not
//! injective, so a binding also keeps what the fit discards (the law: "the remainder is carried
//! and never dropped"): the periapsis angle's 2^-32 turn as a **sub-quantum rotation** `turn`
//! (a constant Cartesian offset cannot carry it: it would send the body along a path whose
//! velocity is rotated by the quantum at every rebinding, and rebindings would accumulate, the
//! drift measured in `crates/engine/src/tube.rs`), and an integer **offset** (what is left after
//! the turn). The readout at any time is `turn·decode(tube, t) + offset`, and at the
//! binding event it is the bound state, bit for bit. The turn is three integer shears
//! ([`crate::lorentz`]): a bijection of the integer plane, exactly invertible, within two quanta of the rotation.
//!
//! The catalogue here is this crate's own: slots with a free list, so a body that rebinds gives
//! its old slot back (`crates/space`'s `Catalogue` only grows, which a body rebound a million
//! times cannot afford). A segment of history keeps its own `Arc` of the compiled trajectory, so
//! the past stays readable for the view after its slot is reused.
use crate::lorentz::Turn;
use crate::num::{cross2, dot2, time_of, Error, Res, Tick, V2};
use crate::world::Unit;
use emergent_space::{
    binding::{cartesian, IntegerState, FittedOrbit, Residual, Trajectory},
    orbit::{OrbitState, Scalar},
    Tube,
};
use std::sync::Arc;

/// A compiled trajectory and its sense: the entry a tube's key indexes. The trajectory is compiled
/// about a mass of one, in units of the doll's mass; `unit` converts it to the doll's own units (the
/// mantissa of the doll's mass; the identity when the mass is a power of two).
#[derive(Debug)]
pub struct Entry {
    pub trajectory: Trajectory,
    pub clockwise: bool,
    pub unit: Unit,
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

/// The kick that made a binding (docs/law.md, "A body's state between kicks"): the split's impulse stands for a
/// force spread over its window `[M − len/2, M + len/2)` around the tick `M` it fires at (the binding's
/// `event_time`). The tube holds the post-kick velocity from `M` on, so it is first order wrong inside the
/// window; a reader completes it by a linear ramp ([`crate::observe::credit`]). A binding that is not a kick
/// (a body's creation, a handoff, a burn's flush) has `len == 0`.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Kick {
    /// The window's length in ticks (the step of its level), or zero for a binding that is not a kick.
    pub len: i64,
    /// The level of the changeover (0 is the whole step, `len = H >> 2·level`).
    pub level: u8,
    /// The velocity the kick added, in quanta of the binding's velocity exponent.
    pub dv: [i64; 2],
    /// The motion law v2's kick or start ([`crate::ext`]): `len` is the physical length of the step it planned, `boundary` the tick
    /// of the synchronised state the next step starts from, `lead` how long before this binding's tick the step it closes started.
    /// A reader between kicks reads the partial step ([`crate::observe`]) and not the ramp.
    pub clock: bool,
    pub boundary: i64,
    pub lead: i64,
}
impl Kick {
    pub const NONE: Kick = Kick { len: 0, level: 0, dv: [0; 2], clock: false, boundary: 0, lead: 0 };
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
    pub turn: Turn,
    /// Exponents of the integer state: positions `n·2^units.0`, velocities `n·2^units.1`.
    pub units: (i16, i16),
    /// The doll's clock quantum (`2^clock_exp` doll time units per tick).
    pub clock_exp: i16,
    pub event_time: Tick,
    /// The kick that made this binding (zero length if none): what the state between kicks is completed with.
    pub kick: Kick,
    /// The impact this tube is on, as [`crate::step::next_impact`] found it after tick `.0` (`.1`: none, or the tick): a function
    /// of the binding alone, so the boundary after a kick reads what the kick found instead of bisecting again. Not state.
    pub impact: Option<(Tick, Option<Tick>)>,
}

/// The tube's own readout (no remainder) at `t`, with the orbit state it came from, in the doll's units
/// (the compiled trajectory is read in units of the doll's mass: elapsed time is converted in, and
/// the radius and the proper time out; angles and velocities are the same in both).
fn decode(entry: &Entry, tube: &Tube, clock_exp: i16, units: (i16, i16), t: Tick) -> Res<(IntegerState, OrbitState)> {
    let peri = time_of(tube.periapsis_time.get() as i64, clock_exp)?;
    let mut elapsed = entry.unit.to_tube(time_of(t, clock_exp)?.sub(peri)?)?;
    if let Trajectory::Plunge(p) = &entry.trajectory {
        let end = p.arrival().coordinate_time.ok_or(Error::Refused("horizon needs a falling clock"))?;
        let deadline = peri.add(entry.unit.to_doll(end)?)?.fixed_ceil(-(clock_exp as i32))?;
        // The terminal event is rounded outward to the population clock. Its
        // sole endpoint read returns the exact surface, never motion beyond it.
        if t as i128 == deadline && elapsed > end { elapsed = end; }
    }
    let mut state = entry.trajectory.state(elapsed)?;
    if !entry.unit.unity {
        state.radius = entry.unit.to_doll(state.radius)?;
        state.proper_time = entry.unit.to_doll(state.proper_time)?;
    }
    Ok((cartesian(state, tube.periapsis_angle, entry.clockwise, units)?, state))
}

impl Binding {
    pub fn terminal_tick(&self) -> Res<Option<Tick>> {
        let Trajectory::Plunge(p) = &self.entry.trajectory else { return Ok(None) };
        // An arc whose anchor has inward speed and is still ahead of the state is a leg the ship leaves its doll by: it
        // never reaches the surface.
        if !p.rests_at_anchor() && self.event_time < self.tube.periapsis_time.get() as i64 {
            return Ok(None);
        }
        let end = p.arrival().coordinate_time.ok_or(Error::Refused("horizon needs a falling clock"))?;
        let peri = time_of(self.tube.periapsis_time.get() as i64, self.clock_exp)?;
        let tick = peri.add(self.to_doll(end)?)?.fixed_ceil(-(self.clock_exp as i32))?;
        Ok(Some(i64::try_from(tick).map_err(|_| Error::Refused("terminal clock"))?))
    }
    /// A length or time of the compiled trajectory (in units of the doll's mass) in the doll's own units.
    pub fn to_doll(&self, x: Scalar) -> Res<Scalar> {
        self.entry.unit.to_doll(x)
    }

    /// The orbit state at `t` (proper time, radius, velocities of the tube).
    pub fn orbit_state(&self, t: Tick) -> Res<OrbitState> {
        Ok(decode(&self.entry, &self.tube, self.clock_exp, self.units, t)?.1)
    }

    /// The body's exact integer state at `t ≥ event_time`: the turned tube plus the offset. At the
    /// binding event it equals the bound state.
    pub fn readout(&self, t: Tick) -> Res<IntegerState> {
        let (d, _) = decode(&self.entry, &self.tube, self.clock_exp, self.units, t)?;
        let (p, v) = (self.turn.apply(d.position)?, self.turn.apply(d.velocity)?);
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
    if let Trajectory::Plunge(p) = &entry.trajectory {
        return Ok((entry.unit.to_doll(p.initial_radius())?.exponent() as i32 - 60, p.speed_bound()?.scale(1)?.exponent() as i32 - 60));
    }
    let key = entry.trajectory.key().ok_or(Error::Refused("turning key"))?;
    let k = key.shape()?;
    let r_max = match &entry.trajectory {
        Trajectory::Cycle(_) => key.periapsis.div(k.scale(1)?.sub(Scalar::ONE)?)?,
        Trajectory::Passage(p) => p.outer_radius,
        Trajectory::Plunge(_) => unreachable!(),
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
    pub turn: Turn,
    pub orbit: OrbitState,
}

/// Fit a tube to the exact state `exact` at tick `t` (in a doll whose clock exponent is `clock_exp`),
/// and keep everything the fit discards. `edge` is the radius a passage is compiled out to.
pub fn bind(exact: IntegerState, t: Tick, clock_exp: i16, edge: Option<Scalar>, unit: Unit) -> Res<Bound> {
    bind_surface(exact, t, clock_exp, edge, unit, None)
}

pub fn bind_surface(exact: IntegerState, t: Tick, clock_exp: i16, edge: Option<Scalar>, unit: Unit, surface: Option<Scalar>) -> Res<Bound> {
    let t_fit = crate::prof::t();
    let bound = bind_in(exact, t, clock_exp, edge, unit, surface)?;
    crate::prof::add(crate::prof::FIT, t_fit);
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
    let t_again = crate::prof::t();
    let again = bind_in(coarser, t, clock_exp, edge, unit, surface);
    crate::prof::add(crate::prof::FIT2, t_again);
    again
}

/// The state in the tube's units (`M_D`): positions divided by `μ`, rounded toward zero at the word (a fit is
/// not injective, and the remainder taken against the doll's own readout below carries what it discards).
fn in_tube_units(st: IntegerState, unit: Unit) -> Res<IntegerState> {
    if unit.unity {
        return Ok(st);
    }
    let q = |p: i64| -> Res<i64> { i64::try_from(unit.to_tube(Scalar::raw(p as i128, 0)?)?.fixed(0)?).map_err(|_| Error::Refused("state outside the integer word")) };
    Ok(IntegerState { position: [q(st.position[0])?, q(st.position[1])?], ..st })
}

fn bind_in(exact: IntegerState, t: Tick, clock_exp: i16, edge: Option<Scalar>, unit: Unit, surface: Option<Scalar>) -> Res<Bound> {
    let input = in_tube_units(exact, unit)?;
    let time = unit.to_tube(time_of(t, clock_exp)?)?;
    let edge = edge.map(|e| unit.to_tube(e)).transpose()?;
    let mut fit = if let Some(surface) = surface {
        FittedOrbit::ending_at_grid(input, time, edge, unit.to_tube(surface)?, emergent_space::orbit::READOUT_GRID)?
    } else { FittedOrbit::from_state_grid(input, time, edge, emergent_space::orbit::READOUT_GRID)? };
    let peri = i64::try_from(unit.to_doll(fit.periapsis_time)?.fixed(-(clock_exp as i32))?).map_err(|_| Error::Refused("periapsis time outside the clock"))?;
    let tube = Tube::new(0, fit.periapsis_angle, peri);
    if let Trajectory::Cycle(orbit) = &mut fit.trajectory { orbit.make_evictable(); }
    let entry = Arc::new(Entry { trajectory: fit.trajectory, clockwise: fit.clockwise, unit });
    if let Trajectory::Plunge(p) = &entry.trajectory {
        let end = p.arrival().coordinate_time.ok_or(Error::Refused("horizon needs a falling clock"))?;
        let at = time_of(peri, clock_exp)?.add(unit.to_doll(end)?)?.fixed_ceil(-(clock_exp as i32))?;
        i64::try_from(at).map_err(|_| Error::Refused("terminal clock"))?;
    }
    let units = (exact.length_exponent, exact.velocity_exponent);
    let (decoded, orbit) = decode(&entry, &tube, clock_exp, units, t)?;
    // The turn the 32-bit angle could not hold: the small angle from the decoded position to the exact one.
    let q = |a: [i64; 2]| -> Res<V2> { Ok([Scalar::raw(a[0] as i128, 0)?, Scalar::raw(a[1] as i128, 0)?]) };
    let (dp, ep) = (q(decoded.position)?, q(exact.position)?);
    let dot = dot2(dp, ep)?;
    let turn = if dot.is_positive() { Turn::of_tangent(cross2(dp, ep)?.div(dot)?)? } else { Turn::NONE };
    let (tp, tv) = (turn.apply(decoded.position)?, turn.apply(decoded.velocity)?);
    let residual = Residual {
        position: [exact.position[0] as i128 - tp[0], exact.position[1] as i128 - tp[1]],
        velocity: [exact.velocity[0] as i128 - tv[0], exact.velocity[1] as i128 - tv[1]],
    };
    Ok(Bound { units, entry, tube, residual, turn, orbit })
}

/// A binding with an exactly known tube and nothing to carry (a body made from its orbit).
pub fn bind_exact(entry: Arc<Entry>, tube: Tube, clock_exp: i16, units: (i16, i16), t: Tick, doll: u16) -> Binding {
    Binding {
        doll,
        tube,
        entry,
        residual: Residual { position: [0; 2], velocity: [0; 2] },
        turn: Turn::NONE,
        units,
        clock_exp,
        event_time: t,
        kick: Kick::NONE,
        impact: None,
    }
}
