//! Motion: the compiled drift plus kicks (docs/law.md, "Perturbed motion").
//!
//! **Two clocks, until the dolls are coordinates.** A ship or the player of the *root* doll that anything can kick is stepped
//! by the motion law v2 ([`crate::ext`]): one fixed tick of its fictitious clock, a physical time set by the perturbing
//! potential, exact tube drifts, kicks that also update the integer energy register `p_t`; nothing in it chooses a step, and
//! it is never captured by a planet's doll (a passage is resolved by the time transformation, in the root doll). The
//! planets and the bodies of a planet's doll keep the split described below (step `H`, changeover levels, handoffs) until the
//! single-surface handoff on extended coordinates (the memo's step 3) and the secular kicks for stable bodies (step 5) replace it.
//!
//! A body's motion is a symmetric, symplectic split (Wisdom–Holman). The drift is exact along
//! the tube of the doll it sits in (zero work: a tube is read, never stepped); the kicks carry
//! everything else (the parent's tide, the secondaries' pulls) at a fixed step `H` in the
//! drift's own phase: `1/64` of the tube's radial period (of a passage's duration), a power of
//! two of ticks. An interval `[T, T+H]` is drift `H/2`, a kick of weight `H` at its midpoint,
//! drift `H/2`, so the state at every `T` is the map's synchronised output and a kick is an
//! event at `T + H/2`. A step in *phase* (mean anomaly) and not in time at periapsis: the
//! perturbations here are tides and distant pulls, which grow with the distance, so the
//! orbit's slow part carries them and a quasi-parabolic orbit costs no more kicks than a circle.
//! The step is anchored (block time steps, [`aligned`]): every interval starts on a multiple of its own length, so a body
//! of a longer step has its boundaries on those of a shorter one's. Between boundaries a reader completes the tube by a
//! ramp ([`crate::observe::credit`]); each kick leaves in its binding the window it stands for and what it added
//! ([`crate::bind::Kick`]), and nothing here reads the ramp: kicks, handoffs and certificates read the canonical tubes.
//! Near a secondary the kick is split across levels (SyMBA, [`crate::force`]): the pair is engaged
//! on finer sub-intervals, recursively, while it can be inside a shell, by a certificate that
//! depends on separation and speed only.
//!
//! Every kick reads the exact integer state (`turn·decode + offset`), adds `Δv` (sub-quantum
//! parts carried by sigma-delta), and **rebinds**: a new tube for the new state, with the
//! remainder kept. When the dominant body changes (a ship deep in a planet's well, or leaving
//! it) the state is re-expressed in the other doll (a translation and a boost, at this event
//! only) and rebound there: the changeover levels make the approach smooth, and the handoff
//! happens deep inside the shells (`R_edge/4`, the deepest shell), where the other doll's drift is
//! accurate, and at the edge (`R_edge`) on the way out, with a four-to-one hysteresis so no ship
//! chatters. A body
//! that has nothing to be kicked by (no secondary, no parent) has no events at all.
use crate::bind::{bind, scalars, Binding, Bound, Entry, Kick};
use crate::body::{BodyRec, Item, Kind, Segment, What};
use crate::ctx::Ctx;
use crate::ext::Ext;
use crate::force::{self, LEVELS, RATIO};
use crate::num::{add2, dot2, log2_floor, norm2, scale2, sub2, time_of, Error, Res, Tick, V2};
use crate::thrust;
use emergent_space::{
    binding::{IntegerState, Trajectory},
    orbit::Scalar,
};
use std::sync::Arc;

pub const MIN_STEP: i64 = 2 * 64;
pub const MAX_STEP: i64 = 1 << 50;
/// A thrust step moves the velocity by at most `1/2^THRUST_FRACTION_LOG2` of the local speed.
pub const THRUST_FRACTION_LOG2: i32 = 6;

/// What resolving one item did, for the universe to apply and count.
pub struct Update {
    pub rec: BodyRec,
    /// The binding replaced by a rebinding: it goes to the body's history.
    pub retired: Vec<Segment>,
    /// A compiled entry to put in the catalogue (the rec's tube key is then set by the owner).
    pub new_entry: Option<Arc<Entry>>,
    pub kind: Resolved,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Resolved {
    Kick,
    Open,
    Boundary,
    Handoff,
    Lost,
    Refused,
}

/// The kick step of a tube: `1/64` of its radial period (a passage: of its duration), a power of
/// two of ticks. Inside a planet's doll the orbit that leaves the doll (a flyby, a quasi-parabolic
/// capture) is resolved over what it spends in the doll: twice the leg from periapsis to the edge.
pub fn step_for(b: &Binding, per_period_log2: i32, edge: Option<Scalar>) -> Res<i64> {
    let mut period = b.to_doll(match &b.entry.trajectory {
        Trajectory::Cycle(c) => c.period()?,
        Trajectory::Passage(p) => p.duration()?,
    })?;
    if let (Some(edge), Some(tp)) = (edge, next_periapsis(b, b.event_time)?) {
        if b.to_doll(b.entry.trajectory.key().periapsis)? < edge {
            if let Some(out) = next_exit(b, tp, edge)? {
                let inside = time_of(out - tp, b.clock_exp)?.scale(1)?;
                if inside < period {
                    period = inside;
                }
            }
        }
    }
    let exp = log2_floor(period) - per_period_log2 - b.clock_exp as i32;
    Ok((1i64 << exp.clamp(1, 50)).clamp(MIN_STEP, MAX_STEP))
}

/// **Block time steps** (Aarseth and Makino; docs/law.md, "A body's state between kicks"): the interval of a body
/// whose step is `step` (a power of two of ticks) and which is at tick `t`. On the grid (a multiple of `step`) it is
/// `step`; off it (after a handoff or a decision) it is one **stub** to the next multiple of `step` (shorter than a step,
/// so no less accurate), and every interval after it starts on the grid: every interval of a power of two starts on a
/// multiple of its own length, a body of a longer step has its boundaries on those of a shorter one's, and every pair
/// shares boundaries. (The way back by doublings from the tick's own lowest set bit would take a dozen intervals, each
/// an event, inside one frame: a stub is one.) A stub under `MIN_STEP` ticks is joined to the next interval.
pub fn aligned(step: i64, t: Tick) -> i64 {
    let off = t.rem_euclid(step);
    if off == 0 {
        return step;
    }
    let stub = step - off;
    if stub < MIN_STEP {
        stub + step
    } else {
        stub
    }
}

/// The kind of an item, the third part of its canonical key (tick, body, kind): a kick before an impact before
/// an open before the boundary, and a scheduled decision after all of them at its tick.
fn rank(w: What) -> u8 {
    match w {
        What::Kick(l) => 10 + l,
        What::Crash => 15,
        What::Open(l) => 20 + l,
        What::Boundary => 40,
    }
}
pub(crate) fn insert(plan: &mut Vec<Item>, it: Item) {
    let k = (it.t, rank(it.what));
    let at = plan.partition_point(|p| (p.t, rank(p.what)) <= k);
    plan.insert(at, it);
}

/// Sigma-delta: add `dv` (scalars, velocity units) to the carry in `2^-16` of the quantum `2^exp`,
/// return the whole quanta to apply and the new carry.
fn quantize(dv: V2, exp: i16, carry: [i64; 2]) -> Res<([i64; 2], [i64; 2])> {
    let mut out = [0i64; 2];
    let mut rem = carry;
    for c in 0..2 {
        let inc = dv[c].fixed(16 - exp as i32)?;
        let total = carry[c] as i128 + inc;
        out[c] = i64::try_from(total / 65536).map_err(|_| Error::Refused("kick outside the word"))?;
        rem[c] = (total % 65536) as i64;
    }
    Ok((out, rem))
}

/// An exact two-vector of i128 at an exponent, fit back into an i64 word (dropping the lowest
/// bits, toward zero, when it does not fit in 61 bits).
pub(crate) fn to_word(v: [i128; 2], exp: i32) -> Res<([i64; 2], i16)> {
    let bits = 128 - (v[0].unsigned_abs().max(v[1].unsigned_abs())).leading_zeros() as i32;
    let shift = (bits - 61).max(0);
    let word = |x: i128| i64::try_from(x / (1i128 << shift)).map_err(|_| Error::Refused("word"));
    Ok(([word(v[0])?, word(v[1])?], i16::try_from(exp + shift).map_err(|_| Error::Refused("exponent"))?))
}

/// A position component of `a` as an integer at the length exponent `el` (not above its own).
fn lift(a: &IntegerState, c: usize, el: i32) -> i128 {
    (a.position[c] as i128) << (a.length_exponent as i32 - el)
}

/// Re-express `st` (a state in the doll whose clock exponent is `from`) relative to the doll's
/// child centre `centre` (a state in the same doll), in the child doll (`to`). The position is subtracted and its
/// length exponent relabelled (one doll unit is `2^(to − from)` of the other): exact. The velocity is the ship's seen
/// from the centre, the Lorentz composition by nine integer shears on its lifted four-velocity ([`crate::lorentz`]; the
/// Galilean `v − v_c` was the low-speed approximation), at the finest exponent that holds it. The tick is the same in
/// both dolls: the position is not boosted (the law's open question: a boost also maps an event's time).
fn relative(st: &IntegerState, centre: &IntegerState, from: i16, to: i16) -> Res<IntegerState> {
    let el = st.length_exponent.min(centre.length_exponent) as i32;
    let p = [0, 1].map(|c| lift(st, c, el) - lift(centre, c, el));
    let (pw, pe) = to_word(p, el + (to as i32 - from as i32))?;
    let (vw, ve) = crate::lorentz::seen_from((st.velocity, st.velocity_exponent as i32), (centre.velocity, centre.velocity_exponent as i32), None)?;
    Ok(IntegerState { position: pw, velocity: vw, length_exponent: pe, velocity_exponent: i16::try_from(ve).map_err(|_| Error::Refused("exponent"))? })
}

/// The inverse: `rel` in the child doll (`from`) seen from the child's centre in the parent (`to`). The positions add
/// (rounded to the parent's word, toward zero: the one carry of a handoff, bounded by one quantum of the parent's
/// units); the velocity is the child's, composed with the centre's by the inverse shears, at the exponent of the
/// centre's own words when it fits there (the parent's convention for what leaves a centre) and at the finest that
/// holds it otherwise.
fn absolute(rel: &IntegerState, centre: &IntegerState, from: i16, to: i16) -> Res<IntegerState> {
    let in_parent = IntegerState { length_exponent: rel.length_exponent - (from - to), ..*rel };
    let el = in_parent.length_exponent.min(centre.length_exponent) as i32;
    let p = [0, 1].map(|c| lift(&in_parent, c, el) + lift(centre, c, el));
    let (pw, pe) = to_word(p, el)?;
    let (vw, ve) = crate::lorentz::seen_by_parent(
        (rel.velocity, rel.velocity_exponent as i32),
        (centre.velocity, centre.velocity_exponent as i32),
        Some(centre.velocity_exponent as i32),
    )?;
    Ok(IntegerState { position: pw, velocity: vw, length_exponent: pe, velocity_exponent: i16::try_from(ve).map_err(|_| Error::Refused("exponent"))? })
}

/// The first tick at or after `after` where the tube is at or beyond `edge` (outward), if any.
fn next_exit(b: &Binding, after: Tick, edge: Scalar) -> Res<Option<Tick>> {
    next_exit_with(b, after, edge, true)
}

/// [`next_exit`], with or without the passage's analytic guess (the bisection alone is the reference the guess must equal).
fn next_exit_with(b: &Binding, after: Tick, edge: Scalar, guess: bool) -> Res<Option<Tick>> {
    let outside = |t: Tick| -> Res<bool> { Ok(b.orbit_state(t)?.radius >= edge) };
    if outside(after)? {
        return Ok(Some(after));
    }
    let peri = time_of(b.tube.periapsis_time.get() as i64, b.clock_exp)?;
    let after_s = time_of(after, b.clock_exp)?;
    let apex = match &b.entry.trajectory {
        Trajectory::Cycle(c) => {
            let tube_period = c.period()?;
            if edge > b.to_doll(c.signed_state(tube_period.scale(-1)?)?.radius)? {
                return Ok(None);
            }
            let period = b.to_doll(tube_period)?;
            let n = after_s.sub(peri)?.div(period)?.fixed_floor(0)?;
            let mut apex = peri.add(period.mul(Scalar::raw(n, 0)?)?)?.add(period.scale(-1)?)?;
            if apex < after_s {
                apex = apex.add(period)?;
            }
            apex
        }
        Trajectory::Passage(p) => peri.add(b.to_doll(p.duration()?)?.scale(-1)?)?,
    };
    // A passage's last readable tick is one before its window closes: round the end inward.
    let end = if matches!(b.entry.trajectory, Trajectory::Passage(_)) { apex.fixed_floor(-(b.clock_exp as i32))? - 1 } else { apex.fixed_ceil(-(b.clock_exp as i32))? };
    let (mut lo, mut hi) = (after, i64::try_from(end).map_err(|_| Error::Refused("exit"))?);
    if hi < lo || !outside(hi)? {
        return Ok(None);
    }
    // A passage knows when it reaches a radius (its inverse, one solve): the tick it names is verified against
    // the predicate itself (inside one tick before, outside on it), and the bisection below, which finds the same
    // tick (the predicate is monotone from `after`), is the fallback. A hand-out plans each leaver's passage, and
    // fifty readouts a bisection took most of the time.
    if let (true, Trajectory::Passage(p)) = (guess, &b.entry.trajectory) {
        let guess = b.entry.unit.to_tube(edge).ok().and_then(|e| p.at_radius(e).ok()).and_then(|(off, _)| b.to_doll(off).ok()).and_then(|off| peri.add(off).ok()).and_then(|t| t.fixed_ceil(-(b.clock_exp as i32)).ok()).and_then(|t| i64::try_from(t).ok());
        if let Some(g) = guess.filter(|&g| g > lo && g <= hi) {
            if outside(g)? && !outside(g - 1)? {
                return Ok(Some(g));
            }
        }
    }
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if outside(mid)? {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    Ok(Some(lo))
}

/// The tick of the tube's next periapsis passage at or after `after`, if it has one.
fn next_periapsis(b: &Binding, after: Tick) -> Res<Option<Tick>> {
    let peri = time_of(b.tube.periapsis_time.get() as i64, b.clock_exp)?;
    let after_s = time_of(after, b.clock_exp)?;
    let at = match &b.entry.trajectory {
        Trajectory::Cycle(c) => {
            let period = b.to_doll(c.period()?)?;
            let ahead = after_s.sub(peri)?;
            let n = if ahead <= Scalar::ZERO { 0 } else { ahead.div(period)?.fixed_ceil(0)? };
            peri.add(period.mul(Scalar::raw(n, 0)?)?)?
        }
        Trajectory::Passage(_) => {
            if peri < after_s {
                return Ok(None);
            }
            peri
        }
    };
    Ok(Some(i64::try_from(at.fixed_ceil(-(b.clock_exp as i32))?).map_err(|_| Error::Refused("periapsis"))?))
}

/// The impact the tube holds: the first tick at or after `after` where it is below `surface` (the doll's units). That is
/// `after` itself if it is already below; else, if the periapsis dips under the surface and is still ahead (the certificate
/// `plan_interval` plans a [`What::Crash`] from), the tick the radius falls through it. The radius falls monotonically on the
/// way in, from the apoapsis before a periapsis (from the first readable tick of a passage), so the first tick below is
/// found by bisection on that branch: the answer is the same however far ahead it is. None when the periapsis is above the
/// surface (the course no longer crosses it), when it has passed (the way out is clear), or when the tube dips by less than a
/// tick of its fall.
pub fn next_impact(b: &Binding, surface: Scalar, after: Tick) -> Res<Option<Tick>> {
    // The engine's own reading (the turned tube plus its remainder), the one a kick or a crash checks the surface with.
    let inside = |t: Tick| -> Res<bool> { Ok(norm2(scalars(&b.readout(t)?)?.0)? < surface) };
    if inside(after)? {
        return Ok(Some(after));
    }
    if b.to_doll(b.entry.trajectory.key().periapsis)? >= surface {
        return Ok(None);
    }
    let Some(tp) = next_periapsis(b, after)? else { return Ok(None) };
    let whole = match &b.entry.trajectory {
        Trajectory::Cycle(c) => c.period()?,
        Trajectory::Passage(p) => p.duration()?,
    };
    let half = i64::try_from(b.to_doll(whole.scale(-1)?)?.fixed_ceil(-(b.clock_exp as i32))?).map_err(|_| Error::Refused("half period"))?;
    let (mut lo, mut hi) = (after.max(tp.saturating_sub(half)), tp);
    if !inside(hi)? {
        return Ok(None);
    }
    while hi - lo > 1 {
        let mid = lo + (hi - lo) / 2;
        if inside(mid)? {
            hi = mid;
        } else {
            lo = mid;
        }
    }
    Ok(Some(hi))
}

/// The proper time (root units) a binding's tube has run between `since` (or its binding event, if later)
/// and `t`: a clock reads its tube's length. `shift` is the doll's clock exponent.
pub fn proper_since(b: &Binding, shift: i16, since: Tick, t: Tick) -> Res<Scalar> {
    let tau = b.orbit_state(t)?.proper_time.sub(b.orbit_state(since.max(b.event_time))?.proper_time)?;
    Ok(tau.scale(-(shift as i32))?)
}

/// Passage tubes are compiled out to four sphere-of-influence radii: past the edge the ship has
/// been released long before the tube ends.
pub(crate) fn passage_edge(ctx: &Ctx, doll: u16) -> Option<Scalar> {
    (doll != 0).then(|| ctx.dolls[doll as usize].edge.scale(2).ok()).flatten()
}

struct Work<'a, 'c> {
    ctx: &'a Ctx<'c>,
    i: usize,
    rec: BodyRec,
    retired: Vec<Segment>,
    new_entry: Option<Arc<Entry>>,
}

impl Work<'_, '_> {
    fn doll(&self) -> &crate::world::DollRec {
        &self.ctx.dolls[self.rec.b.doll as usize]
    }

    fn passage_edge(&self, doll: u16) -> Option<Scalar> {
        passage_edge(self.ctx, doll)
    }

    /// Whether anything can kick this body: a secondary in its doll (other than itself) or a parent.
    fn has_forces(&self, doll: u16) -> bool {
        self.ctx.dolls[doll as usize].parent.is_some() || self.ctx.sources[doll as usize].iter().any(|&j| j != self.i)
    }

    /// Bind `exact` at `t` in `doll` and replace the body's binding, keeping the old one as history.
    fn rebind(&mut self, exact: IntegerState, t: Tick, doll: u16) -> Res<Bound> {
        let clock_exp = self.ctx.dolls[doll as usize].clock_exp();
        let bound = bind(exact, t, clock_exp, self.passage_edge(doll), self.ctx.tube_unit(self.i, doll)?)?;
        let old = &self.rec.b;
        // The tube's length since the last binding is the body's clock reading (root units).
        let tau = old.orbit_state(t)?.proper_time.sub(old.orbit_state(old.event_time)?.proper_time)?;
        let root_tau = tau.scale(-(self.ctx.dolls[old.doll as usize].shift as i32))?;
        self.rec.proper = self.rec.proper.add(root_tau)?;
        self.retired.push(Segment { b: old.clone(), until: t });
        self.rec.b = Binding {
            doll,
            tube: bound.tube,
            entry: bound.entry.clone(),
            residual: bound.residual,
            turn: bound.turn,
            units: bound.units,
            clock_exp,
            event_time: t,
            kick: Kick::NONE,
        };
        self.new_entry = Some(bound.entry.clone());
        Ok(bound)
    }

    /// The proper time (root units) the ship's tube has run since `since`, at tick `t`.
    fn proper_since(&self, since: Tick, t: Tick) -> Res<Scalar> {
        proper_since(&self.rec.b, self.ctx.dolls[self.rec.b.doll as usize].shift, since, t)
    }

    /// The thrust burn owed since the last flush: new velocity (scalars); the heading changes too.
    fn burn(&mut self, x: V2, v: V2, t: Tick) -> Res<V2> {
        let Some(th) = self.rec.thrust else { return Ok(v) };
        if th.keys == 0 || t <= th.since {
            return Ok(v);
        }
        let dtau = self.proper_since(th.since, t)?;
        let (heading, v2) = thrust::owed(self.ctx.cfg, th, dtau, x, v, self.ctx.dolls[self.rec.b.doll as usize].unit.mu)?;
        self.rec.thrust = Some(crate::body::Thrust { heading, since: t, ..th });
        Ok(v2)
    }

    fn velocity_after(&self, st: &IntegerState, v_new: V2) -> Res<[i64; 2]> {
        let q = |c: usize| -> Res<i64> { i64::try_from(v_new[c].fixed(-(st.velocity_exponent as i32))?).map_err(|_| Error::Refused("velocity outside the word")) };
        Ok([q(0)?, q(1)?])
    }

    /// A kick at `level`: read the exact state, add `Δv = h·a`, rebind.
    fn kick(&mut self, t: Tick, level: u8) -> Res<()> {
        let st = self.rec.b.readout(t)?;
        let (x, v) = scalars(&st)?;
        let d = self.rec.b.doll;
        let secs = self.ctx.secondaries(d, t, self.i)?;
        let tide = self.ctx.tide(d, t)?;
        let a = force::acceleration(level, x, &secs, tide)?;
        let h = time_of(self.rec.interval >> (2 * level as i64), self.rec.b.clock_exp)?;
        let dv = scale2(a, h)?;
        let thrusting = level == 0 && self.rec.thrust.is_some_and(|t| t.keys != 0);
        // What the split's impulse added, as scalars (the burn is owed up to this tick, not pending: only the tide's part is).
        let added;
        let next = if thrusting {
            // The player's burn rides on the level-0 kick: velocity after the tide, then the boost.
            let v2 = self.burn(x, add2(v, dv)?, t)?;
            added = dv;
            IntegerState { velocity: self.velocity_after(&st, v2)?, ..st }
        } else {
            let (dvq, carry) = quantize(dv, st.velocity_exponent, self.rec.carry)?;
            self.rec.carry = carry;
            if dvq == [0, 0] {
                // A sub-quantum kick fires nothing: it is carried.
                return Ok(());
            }
            added = [Scalar::raw(dvq[0] as i128, st.velocity_exponent as i32)?, Scalar::raw(dvq[1] as i128, st.velocity_exponent as i32)?];
            IntegerState { velocity: [st.velocity[0] + dvq[0], st.velocity[1] + dvq[1]], ..st }
        };
        self.rebind(next, t, d)?;
        // The binding remembers the kick it is: the window it stands for and the velocity it added, so a reader between
        // kicks completes the tube by the ramp (docs/law.md, "A body's state between kicks").
        let ve = self.rec.b.units.1 as i32;
        let q = |s: Scalar| -> Res<i64> { i64::try_from(s.fixed(-ve)?).map_err(|_| Error::Refused("kick outside the word")) };
        // (A kick that does not fit the word's quanta leaves no ramp: the rebinding stands either way.)
        if let (Ok(a), Ok(b)) = (q(added[0]), q(added[1])) {
            self.rec.b.kick = Kick { len: self.rec.interval >> (2 * level as i64), level, dv: [a, b], ..Kick::NONE };
        }
        Ok(())
    }

    /// Deep inside a planet's shell the planet is the dominant body: the child doll of `centre`
    /// takes the ship. Returns whether it did.
    fn maybe_capture(&mut self, t: Tick, st: &IntegerState, x: V2) -> Res<bool> {
        let d = self.rec.b.doll;
        // The motion law v2: every ship of the root doll stays in it (a passage needs no handoff, the time transformation
        // resolves it); the handoff of a bound body is the single surface of the memo's step 3.
        if !matches!(self.rec.kind, Kind::Ship | Kind::Player) || d == 0 {
            return Ok(false);
        }
        for (c, doll) in self.ctx.dolls.iter().enumerate().skip(1) {
            if doll.parent != Some(d) {
                continue;
            }
            let centre = doll.centre.expect("a child doll has a centre");
            let (cx, _) = self.ctx.state_of(centre, t)?;
            if norm2(sub2(x, cx)?)? < self.ctx.info[centre].soi.scale(1 - LEVELS as i32)? {
                if let Err(e) = self.capture(t, *st, c as u16) {
                    eprintln!("capture refused: {e:?} at t={t} state {st:?} centre {:?}", cx.map(crate::num::to_f64));
                    return Err(e);
                }
                return Ok(true);
            }
        }
        Ok(false)
    }

    /// The start of a level-`l` interval at `t` (`h0` is the level-0 interval of this step): engage
    /// level `l+1` where a pair can reach the support of its weight within the interval, and take a
    /// ship that is already deep in a planet's well.
    fn open(&mut self, t: Tick, l: u8, h0: i64) -> Res<()> {
        if l >= LEVELS {
            return Ok(());
        }
        let st = self.rec.b.readout(t)?;
        let (x, v) = scalars(&st)?;
        if l > 0 && self.maybe_capture(t, &st, x)? {
            return Ok(());
        }
        let d = self.rec.b.doll;
        let h_ticks = h0 >> (2 * l as i64);
        let h = time_of(h_ticks, self.rec.b.clock_exp)?;
        let mut hot = false;
        for s in self.ctx.secondaries(d, t, self.i)? {
            let r = norm2(sub2(s.pos, x)?)?;
            if force::engaged(l, r, force::relative_speed(v, s.vel)?, h, s.edge)? {
                hot = true;
                break;
            }
        }
        if !hot {
            return Ok(());
        }
        let sub = h_ticks / RATIO;
        for m in 0..RATIO {
            let start = t + m * sub;
            insert(&mut self.rec.plan, Item { t: start + sub / 2, what: What::Kick(l + 1) });
            if l + 1 < LEVELS && m > 0 {
                insert(&mut self.rec.plan, Item { t: start, what: What::Open(l + 1) });
            }
        }
        if l + 1 < LEVELS {
            // The first sub-interval opens now: the state is this one.
            self.open(t, l + 1, h0)?;
        }
        Ok(())
    }

    /// Plan the interval starting at `t`: the step (with hysteresis), its midpoint kick and boundary,
    /// capped so that it ends no later than the tube's exit from its doll, and the planned impact.
    fn plan_interval(&mut self, t: Tick) -> Res<()> {
        let d = self.rec.b.doll;
        if !self.has_forces(d) {
            // Nothing can kick this body: it is a pure tube, and costs nothing until observed.
            self.rec.plan.clear();
            return Ok(());
        }
        if self.on_clock() {
            return self.plan_clock(t);
        }
        let edge = (d != 0 && matches!(self.rec.kind, Kind::Ship | Kind::Player)).then(|| self.doll().edge);
        let want = step_for(&self.rec.b, self.ctx.cfg.step_log2, edge)?;
        // Thrust steps: the burn moves the velocity by a small fraction of the local speed.
        let want = match self.rec.thrust {
            Some(th) if th.keys & 3 != 0 => want.min(self.thrust_step(t)?),
            _ => want,
        };
        let cur = self.rec.step;
        if cur == 0 || want >= cur.saturating_mul(2) || want.saturating_mul(2) <= cur || self.rec.thrust.is_some_and(|th| th.keys != 0) {
            self.rec.step = want;
        }
        self.rec.anchor = t;
        let mut h = aligned(self.rec.step, t);
        self.rec.interval = h;
        let movable = matches!(self.rec.kind, Kind::Ship | Kind::Player);
        if movable && d != 0 {
            if let Some(exit) = next_exit(&self.rec.b, t, self.doll().edge)? {
                // The interval must end at or before the exit, so the release is checked there.
                let room = exit - t;
                while h > room && h > MIN_STEP {
                    h >>= 1;
                }
                if h > room {
                    insert(&mut self.rec.plan, Item { t: t + room.max(1), what: What::Boundary });
                    self.rec.interval = 0;
                    return Ok(());
                }
                self.rec.interval = h;
            }
        }
        insert(&mut self.rec.plan, Item { t: t + h / 2, what: What::Kick(0) });
        insert(&mut self.rec.plan, Item { t: t + h, what: What::Boundary });
        if self.rec.kind != Kind::Planet {
            let key = self.rec.b.entry.trajectory.key();
            if self.rec.b.to_doll(key.periapsis)? < self.doll().surface {
                // The ship is lost where the course meets the surface, not at the periapsis behind it.
                if let Some(tc) = next_impact(&self.rec.b, self.doll().surface, t)?.filter(|&tc| tc <= t + h) {
                    insert(&mut self.rec.plan, Item { t: tc.max(t + 1), what: What::Crash });
                }
            }
        }
        // A stub is split into quarters like any interval (the levels' lengths are `h >> 2l`, floored: a few ticks of the
        // deepest level's weight are left out of a stub), unless it is too short to split.
        if h < MIN_STEP {
            return Ok(());
        }
        self.open(t, 0, h)
    }

    // ---- the motion law v2: the root doll's ships ---------------------------------------------------

    /// Whether the motion law v2 steps this body: a ship or the player of the root doll (it is planned when something can
    /// kick it; a body that nothing kicks is a tube and has no plan).
    fn on_clock(&self) -> bool {
        self.rec.b.doll == 0 && matches!(self.rec.kind, Kind::Ship | Kind::Player)
    }

    /// The mass of the body's drift in the doll's units: its tube's host.
    fn tube_mu(&self) -> Res<Scalar> {
        Ok(self.ctx.tube_unit(self.i, self.rec.b.doll)?.mu)
    }

    /// Project the energy register onto the constraint `K = 0` at the state read at `t`: `p_t = U_P − H_D`.
    fn project(&mut self, t: Tick) -> Res<()> {
        let st = self.rec.b.readout(t)?;
        let (x, v) = scalars(&st)?;
        let secs = self.ctx.secondaries(self.rec.b.doll, t, self.i)?;
        let u = force::field(&secs, x)?.potential;
        let hd = force::kepler(x, v, self.tube_mu()?)?;
        let mut ext = self.rec.ext.expect("a clock-stepped body");
        ext.set_pt(u.sub(hd)?)?;
        self.rec.ext = Some(ext);
        Ok(())
    }

    /// Begin (or begin again, after a decision or a handoff) the clock at tick `t`, where the state is synchronised: the
    /// constants of the clock are derived if the body has none, the register is projected onto `K = 0`, and the first kick
    /// is planned at the middle of the first step.
    fn plan_clock(&mut self, t: Tick) -> Res<()> {
        let d = self.rec.b.doll;
        if self.rec.ext.is_none() {
            let st = self.rec.b.readout(t)?;
            let (ds, c, b) = crate::ext::constants(self.ctx, d, t, self.i, self.ctx.cfg.step_log2)?;
            let pt_exp = i16::try_from(2 * st.velocity_exponent as i32 + 64).map_err(|_| Error::Refused("exponent"))?;
            self.rec.ext = Some(Ext { pt: 0, pt_exp, pt_carry: 0, dt_carry: 0, ds, c, b });
        }
        self.project(t)?;
        let st = self.rec.b.readout(t)?;
        let (x, v) = scalars(&st)?;
        let mut ext = self.rec.ext.expect("a clock-stepped body");
        let y = ext.y(force::kepler(x, v, self.tube_mu()?)?.add(ext.pt_value()?)?)?;
        let mut half = ext.ticks(ext.time(y, ext.ds.scale(-1)?)?, self.ctx.dolls[d as usize].clock_exp())?;
        // A held burn limits the step as it does at every kick (the clock's own step is far longer in the far field: the burn
        // would be one lump, and the velocity leaves its word): the velocity moves by a small fraction of itself per step.
        if matches!(self.rec.thrust, Some(th) if th.keys & 3 != 0) {
            half = half.min((self.thrust_step(t)? / 2).max(1));
        }
        self.rec.ext = Some(ext);
        self.rec.plan.clear();
        self.rec.anchor = t;
        self.rec.interval = 2 * half;
        self.rec.step = 2 * half;
        // The synchronised state a reader's partial step starts from, until the first kick: this one.
        self.rec.b.kick = Kick { len: 2 * half, level: 0, dv: [0; 2], clock: true, boundary: t, lead: 0 };
        insert(&mut self.rec.plan, Item { t: t + half, what: What::Kick(0) });
        Ok(())
    }

    /// A kick of the clock: `Kc(Δs)` at the middle of a step, then the next boundary and kick, planned from the state it leaves.
    /// The weight is `w = Δs·f'(U_P + c)`: the velocity gets `w·∇U_P`, the register `w·∂_tU_P`, and the two flows are one.
    fn kick_clock(&mut self, t: Tick, _level: u8) -> Res<Resolved> {
        let d = self.rec.b.doll;
        let st = self.rec.b.readout(t)?;
        let (x, v) = scalars(&st)?;
        let secs = self.ctx.secondaries(d, t, self.i)?;
        // A surface is a crash, wherever the kick finds it: the star's, and the planets' (a ship is never in a planet's doll here).
        let sources = self.ctx.sources[d as usize].iter().filter(|&&j| j != self.i);
        for (s, &j) in secs.iter().zip(sources) {
            if let Some(radius) = self.ctx.surface_in(j, d)? {
                if norm2(sub2(s.pos, x)?)? < radius {
                    self.rec.alive = false;
                    return Ok(Resolved::Lost);
                }
            }
        }
        if self.rec.kind != Kind::Planet && norm2(x)? < self.doll().surface {
            self.rec.alive = false;
            return Ok(Resolved::Lost);
        }
        let mut ext = self.rec.ext.expect("a clock-stepped body");
        let f = force::field(&secs, x)?;
        let w = ext.time(ext.y(f.potential)?, ext.ds)?;
        let dv = scale2(f.accel, w)?;
        let thrusting = self.rec.thrust.is_some_and(|t| t.keys != 0);
        let (next, carry) = if thrusting {
            // The player's burn rides on the kick; it is not a flow of the Hamiltonian, so the register is projected after.
            let v2 = self.burn(x, add2(v, dv)?, t)?;
            (IntegerState { velocity: self.velocity_after(&st, v2)?, ..st }, self.rec.carry)
        } else {
            let (dvq, carry) = quantize(dv, st.velocity_exponent, self.rec.carry)?;
            ext.add_pt(w.mul(f.rate)?)?;
            (IntegerState { velocity: [st.velocity[0] + dvq[0], st.velocity[1] + dvq[1]], ..st }, carry)
        };
        let fired = next.velocity != st.velocity;
        if fired {
            self.rebind(next, t, d)?;
        }
        self.rec.carry = carry;
        self.rec.ext = Some(ext);
        if thrusting {
            self.project(t)?;
        }
        // The drift to come: `D(Δs)` at `y = H_D + p_t + c` of the state the kick leaves (the two half drifts around the next
        // kick share it), and its boundary in the middle.
        let (x, v) = scalars(&next)?;
        let mut ext = self.rec.ext.expect("a clock-stepped body");
        let y = ext.y(force::kepler(x, v, self.tube_mu()?)?.add(ext.pt_value()?)?)?;
        let mut full = ext.ticks(ext.time(y, ext.ds)?, self.ctx.dolls[d as usize].clock_exp())?;
        if matches!(self.rec.thrust, Some(th) if th.keys & 3 != 0) {
            full = full.min(self.thrust_step(t)?);
        }
        self.rec.ext = Some(ext);
        if fired {
            // The step the next reader completes by a partial step: from the boundary in the middle, and how long the step this kick
            // closes had been running.
            self.rec.b.kick = Kick { len: full, level: 0, dv: [0; 2], clock: true, boundary: t + full / 2, lead: t - self.rec.anchor };
        }
        self.rec.interval = full;
        self.rec.step = full;
        insert(&mut self.rec.plan, Item { t: t + full / 2, what: What::Boundary });
        insert(&mut self.rec.plan, Item { t: t + full, what: What::Kick(0) });
        if self.rec.kind != Kind::Planet {
            let key = self.rec.b.entry.trajectory.key();
            if self.rec.b.to_doll(key.periapsis)? < self.doll().surface {
                if let Some(tc) = next_impact(&self.rec.b, self.doll().surface, t)?.filter(|&tc| tc <= t + full) {
                    insert(&mut self.rec.plan, Item { t: tc.max(t + 1), what: What::Crash });
                }
            }
        }
        Ok(Resolved::Kick)
    }

    /// The synchronised output of the split, in the middle between two kicks: the certificates (surface, the system's edge),
    /// and the tick the map's state is read at ([`BodyRec::anchor`]). The next kick is already planned.
    fn boundary_clock(&mut self, t: Tick) -> Res<Resolved> {
        let st = self.rec.b.readout(t)?;
        let (x, _) = scalars(&st)?;
        let r = norm2(x)?;
        if self.rec.kind != Kind::Planet && r < self.doll().surface {
            self.rec.alive = false;
            return Ok(Resolved::Lost);
        }
        if r > Scalar::power_of_two(self.ctx.cfg.leave_log2 as i16) {
            self.rec.alive = false;
            return Ok(Resolved::Lost);
        }
        self.rec.anchor = t;
        Ok(Resolved::Boundary)
    }

    fn thrust_step(&self, t: Tick) -> Res<i64> {
        let st = self.rec.b.readout(t)?;
        let (x, v) = scalars(&st)?;
        let speed = norm2(v)?.max(Scalar::ONE.div(norm2(x)?)?.sqrt()?);
        // α in rapidity per tick: 2^thrust_log2 per root unit at the throttle's level, and a tick is 2^0 root units.
        let alpha = Scalar::power_of_two(thrust::alpha_log2(self.ctx.cfg, self.rec.thrust.map_or(0, |t| t.level)));
        let ticks = speed.scale(-THRUST_FRACTION_LOG2)?.div(alpha)?;
        let exp = log2_floor(ticks).clamp(1, 50);
        Ok((1i64 << exp).clamp(MIN_STEP, MAX_STEP))
    }

    /// The end of a step: certificates, then the next step's plan.
    fn boundary(&mut self, t: Tick) -> Res<Resolved> {
        if self.rec.ext.is_some() {
            return self.boundary_clock(t);
        }
        let d = self.rec.b.doll;
        let movable = matches!(self.rec.kind, Kind::Ship | Kind::Player);
        let st = self.rec.b.readout(t)?;
        let (x, _) = scalars(&st)?;
        let r = norm2(x)?;
        if self.rec.kind != Kind::Planet && r < self.doll().surface {
            self.rec.alive = false;
            return Ok(Resolved::Lost);
        }
        if movable {
            if d == 0 {
                if r > Scalar::power_of_two(self.ctx.cfg.leave_log2 as i16) {
                    self.rec.alive = false;
                    return Ok(Resolved::Lost);
                }
                if self.maybe_capture(t, &st, x)? {
                    return Ok(Resolved::Handoff);
                }
            } else if r > self.doll().edge {
                self.release(t, st)?;
                return Ok(Resolved::Handoff);
            }
        }
        self.plan_interval(t)?;
        Ok(Resolved::Boundary)
    }

    fn handoff_to(&mut self, t: Tick, exact: IntegerState, doll: u16) -> Res<()> {
        self.rebind(exact, t, doll)?;
        self.rec.carry = [0, 0];
        self.rec.plan.clear();
        self.rec.step = 0;
        self.plan_interval(t)
    }

    fn capture(&mut self, t: Tick, st: IntegerState, child: u16) -> Res<()> {
        let from = self.rec.b.doll;
        let centre = self.ctx.dolls[child as usize].centre.expect("centre");
        let cs = self.ctx.bodies.binding_at(centre, t).ok_or(Error::Refused("history pruned"))?.readout(t)?;
        let rel = relative(&st, &cs, self.ctx.dolls[from as usize].shift, self.ctx.dolls[child as usize].shift)?;
        self.handoff_to(t, rel, child)
    }

    fn release(&mut self, t: Tick, st: IntegerState) -> Res<()> {
        let from = self.rec.b.doll;
        let to = self.ctx.dolls[from as usize].parent.expect("a child doll has a parent");
        let centre = self.ctx.dolls[from as usize].centre.expect("centre");
        let cs = self.ctx.bodies.binding_at(centre, t).ok_or(Error::Refused("history pruned"))?.readout(t)?;
        let abs = absolute(&st, &cs, self.ctx.dolls[from as usize].shift, self.ctx.dolls[to as usize].shift)?;
        self.handoff_to(t, abs, to)
    }

    /// A planned impact: the ship is at or below the surface at the periapsis passage.
    fn crash(&mut self, t: Tick) -> Res<Resolved> {
        let st = self.rec.b.readout(t)?;
        let (x, _) = scalars(&st)?;
        if norm2(x)? <= self.doll().surface {
            self.rec.alive = false;
            return Ok(Resolved::Lost);
        }
        Ok(Resolved::Open)
    }
}

/// Resolve body `i`'s next item against the context. Pure: it reads other bodies' tubes at the
/// item's tick and returns the new record; the universe applies it.
pub fn process(ctx: &Ctx, i: usize, rec: BodyRec) -> Update {
    let mut w = Work { ctx, i, rec, retired: Vec::new(), new_entry: None };
    let item = w.rec.plan.remove(0);
    w.rec.events += 1;
    let t = item.t;
    let h0 = w.rec.interval;
    let result = match item.what {
        What::Kick(l) if w.rec.ext.is_some() => w.kick_clock(t, l),
        What::Kick(l) => w.kick(t, l).map(|_| Resolved::Kick),
        What::Open(l) => w.open(t, l, h0).map(|_| Resolved::Open),
        What::Crash => w.crash(t),
        What::Boundary => w.boundary(t),
    };
    let kind = match result {
        Ok(k) => k,
        Err(e) => {
            w.rec.fault = Some((item.what, e));
            // A refusal never corrupts a body: the old binding stands, the kick is dropped and
            // counted. A boundary that cannot plan its next step ends the body: it is lost.
            w.rec.refusals += 1;
            if item.what == What::Boundary {
                w.rec.alive = false;
                Resolved::Lost
            } else if w.rec.ext.is_some() && w.rec.alive && !w.rec.plan.iter().any(|p| matches!(p.what, What::Kick(_))) {
                // A clock-stepped body plans its next kick when it kicks: a refused kick must not leave it without one.
                if w.plan_clock(t).is_err() {
                    w.rec.alive = false;
                    Resolved::Lost
                } else {
                    Resolved::Refused
                }
            } else {
                Resolved::Refused
            }
        }
    };
    Update { rec: w.rec, retired: w.retired, new_entry: w.new_entry, kind }
}

/// Plan a body's first interval at its creation.
pub fn replan(ctx: &Ctx, i: usize, rec: BodyRec, t: Tick) -> Update {
    let mut w = Work { ctx, i, rec, retired: Vec::new(), new_entry: None };
    w.rec.plan.clear();
    if w.plan_interval(t).is_err() {
        w.rec.alive = false;
    }
    Update { rec: w.rec, retired: w.retired, new_entry: w.new_entry, kind: Resolved::Open }
}

/// A decision: flush the thrust owed so far at `t` (a rebinding when a burn is owed; a turn alone only
/// updates the heading), set the keys. New keys replan from `t`; the same keys held (the player re-asserting
/// them each frame) only flush, so the kicks keep their cadence.
pub fn decide(ctx: &Ctx, i: usize, rec: BodyRec, t: Tick, word: u8) -> Update {
    let mut w = Work { ctx, i, rec, retired: Vec::new(), new_entry: None };
    let (keys, level) = thrust::split(word);
    let same = w.rec.thrust.is_some_and(|th| th.keys == keys && th.level == level);
    let res = (|| -> Res<()> {
        if let Some(th) = w.rec.thrust.filter(|th| th.keys != 0 && t > th.since) {
            let st = w.rec.b.readout(t)?;
            let (x, v) = scalars(&st)?;
            let v2 = w.burn(x, v, t)?;
            if th.keys & 3 != 0 {
                let next = IntegerState { velocity: w.velocity_after(&st, v2)?, ..st };
                w.rebind(next, t, w.rec.b.doll)?;
                if w.rec.ext.is_some() {
                    // A burn is not a flow of the Hamiltonian: the register is projected back onto K = 0.
                    w.project(t)?;
                }
            }
        }
        if let Some(th) = w.rec.thrust.as_mut() {
            th.keys = keys;
            th.level = level;
            th.since = t;
        }
        if same {
            return Ok(());
        }
        w.rec.plan.clear();
        w.rec.step = 0;
        w.plan_interval(t)
    })();
    if res.is_err() {
        w.rec.refusals += 1;
    }
    Update { rec: w.rec, retired: w.retired, new_entry: w.new_entry, kind: Resolved::Open }
}

pub fn dot(a: V2, b: V2) -> Res<Scalar> {
    dot2(a, b)
}

#[cfg(test)]
mod tests {
    use super::*;

    /// The passage's analytic guess finds the tick the bisection finds: for every member the plane hands out
    /// (passages and cycles, from every state the frame hands over), from periapsis and from the binding event.
    #[test]
    fn a_passages_exit_by_its_inverse_is_the_exit_by_bisection() {
        use crate::fleet::Order;
        let mut p = crate::scenario::plane(crate::ctx::Config::default(), 1, Order::Sparse, 1, 48).unwrap();
        let n0 = p.u.n_bodies();
        p.u.settle(30_000_000);
        let (mut passages, mut exits) = (0, 0);
        for i in n0..p.u.n_bodies() {
            let born = p.u.info[i].born;
            let b = p.u.bodies().binding_at(i, born).unwrap();
            let doll = &p.u.dolls[b.doll as usize];
            let is_passage = matches!(b.entry.trajectory, Trajectory::Passage(_));
            let starts = [Some(born), next_periapsis(&b, born).unwrap()];
            for after in starts.into_iter().flatten() {
                for edge in [doll.edge, doll.edge.scale(-1).unwrap(), doll.edge.scale(-3).unwrap()] {
                    let (fast, slow) = (next_exit_with(&b, after, edge, true).unwrap(), next_exit_with(&b, after, edge, false).unwrap());
                    assert_eq!(fast, slow, "body {i}, from {after}, edge {edge:?}");
                    exits += fast.is_some() as usize;
                }
            }
            passages += is_passage as usize;
        }
        println!("{passages} passages of {} handed out; {exits} exits found, each the same by both ways", p.u.n_bodies() - n0);
        assert!(passages >= 10 && exits >= 20, "the test must look at passages that exit: {passages} {exits}");
    }

    /// A handoff is a translation and a boost, exact in integers, with one bounded carry (the sum is
    /// rounded to the parent's word): a thousand capture and release round trips return the state to
    /// within one quantum of the parent's word, and never drift away from it.
    #[test]
    fn a_thousand_handoff_round_trips_do_not_drift() {
        let planet = IntegerState { position: [1i64 << 59, 1i64 << 58], velocity: [-(1i64 << 40), 1i64 << 41], length_exponent: -30, velocity_exponent: -75 };
        let ship = IntegerState {
            position: [(1i64 << 59) + 123_456_789_012_345, (1i64 << 58) - 98_765_432_109_876],
            velocity: [-(1i64 << 40) + 77_777_777, (1i64 << 41) + 33_333_333],
            length_exponent: -30,
            velocity_exponent: -75,
        };
        let (host, child) = (0i16, 10i16);
        let mut s = ship;
        let first = absolute(&relative(&s, &planet, host, child).unwrap(), &planet, child, host).unwrap();
        for _ in 0..1000 {
            let rel = relative(&s, &planet, host, child).unwrap();
            s = absolute(&rel, &planet, child, host).unwrap();
        }
        // Compare at the host's exponent: positions and velocities within one quantum of the word.
        let q = |a: &IntegerState, b: &IntegerState| -> (i128, i128) {
            let lift = |st: &IntegerState, c: usize, v: bool| if v { (st.velocity[c] as i128) << (st.velocity_exponent as i32 + 200) } else { (st.position[c] as i128) << (st.length_exponent as i32 + 200) };
            ((lift(a, 0, false) - lift(b, 0, false)).abs().max((lift(a, 1, false) - lift(b, 1, false)).abs()), (lift(a, 0, true) - lift(b, 0, true)).abs().max((lift(a, 1, true) - lift(b, 1, true)).abs()))
        };
        let (dp, dv) = q(&s, &first);
        assert_eq!((dp, dv), (0, 0), "the second round trip onward is a fixed point");
        let (dp, dv) = q(&first, &ship);
        let quantum = 1i128 << (200 - 30 + 0).max(0);
        assert!(dp <= quantum && dv <= (1i128 << (200 - 75)), "one round trip loses at most a quantum: {dp} {dv}");
    }

    /// A ship captured and released at a centre speed of 0.01, 0.3 and 0.9 returns the identical integer state (the
    /// memo's R3 test; frozen before the first run): a ship that moves with its centre, at any distance in the doll, in the
    /// state's words and exponents (compared as values). 4000 states each, every direction of the centre's motion.
    #[test]
    fn a_ship_captured_and_released_returns_the_identical_integer_state_at_every_speed() {
        let mut seed = 0x1234_5678_9ABC_DEF1u64;
        let mut rnd = move || {
            seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            (seed >> 11) as f64 / (1u64 << 53) as f64
        };
        let (host, child) = (0i16, 10i16);
        let value = |st: &IntegerState| -> [i128; 4] {
            let sh = |x: i64, e: i16| (x as i128) << (e as i32 + 200);
            [sh(st.position[0], st.length_exponent), sh(st.position[1], st.length_exponent), sh(st.velocity[0], st.velocity_exponent), sh(st.velocity[1], st.velocity_exponent)]
        };
        for beta in [0.01f64, 0.3, 0.9] {
            let ve = beta.log2().floor() as i16 - 61;
            let mut exact = 0;
            for _ in 0..4000 {
                let ang = (rnd() * 2.0 - 1.0) * std::f64::consts::PI;
                let w = [(beta * ang.cos() / 2f64.powi(ve as i32)).round() as i64, (beta * ang.sin() / 2f64.powi(ve as i32)).round() as i64];
                let centre = IntegerState { position: [(rnd() * 2e18 - 1e18) as i64, (rnd() * 2e18 - 1e18) as i64], velocity: w, length_exponent: -30, velocity_exponent: ve };
                // Within the doll: a few million units of the centre's, moving with it at up to a thousandth of its speed.
                let rel = (rnd() * 0.001 * beta) / 2f64.powi(ve as i32);
                let a2 = (rnd() * 2.0 - 1.0) * std::f64::consts::PI;
                let ship = IntegerState {
                    position: [centre.position[0] + (rnd() * 4e15 - 2e15) as i64, centre.position[1] + (rnd() * 4e15 - 2e15) as i64],
                    velocity: [w[0] + (rel * a2.cos()).round() as i64, w[1] + (rel * a2.sin()).round() as i64],
                    length_exponent: -30,
                    velocity_exponent: ve,
                };
                let back = absolute(&relative(&ship, &centre, host, child).unwrap(), &centre, child, host).unwrap();
                exact += (value(&back) == value(&ship)) as usize;
            }
            println!("centre at {beta}c: {exact} of 4000 captured-then-released ships come back as the identical state");
            assert_eq!(exact, 4000, "centre at {beta}c");
        }
    }

    /// The handoff is Lorentz: a ship captured is seen with the relativistic composition of velocities (to the float
    /// oracle's own precision), where the Galilean difference of the old handoff is off by the order of `β²`.
    #[test]
    fn a_captured_ship_is_seen_with_the_relativistic_velocity() {
        let ve = -62i16;
        let w = [(0.6f64 * 2f64.powi(62)) as i64, (0.3f64 * 2f64.powi(62)) as i64];
        let centre = IntegerState { position: [0, 0], velocity: w, length_exponent: -30, velocity_exponent: ve };
        let v = [(0.1f64 * 2f64.powi(62)) as i64, (-0.2f64 * 2f64.powi(62)) as i64];
        let ship = IntegerState { position: [1 << 40, 1 << 41], velocity: v, length_exponent: -30, velocity_exponent: ve };
        let rel = relative(&ship, &centre, 0, 10).unwrap();
        let f = |x: i64, e: i16| x as f64 * 2f64.powi(e as i32);
        let (vf, wf) = ([f(v[0], ve), f(v[1], ve)], [f(w[0], ve), f(w[1], ve)]);
        let (ww, vw) = (wf[0] * wf[0] + wf[1] * wf[1], vf[0] * wf[0] + vf[1] * wf[1]);
        let g = 1.0 / (1.0 - ww).sqrt();
        let k = 1.0 / (1.0 - vw);
        let want = [k * (vf[0] / g - wf[0] + g / (g + 1.0) * vw * wf[0]), k * (vf[1] / g - wf[1] + g / (g + 1.0) * vw * wf[1])];
        let got = [f(rel.velocity[0], rel.velocity_exponent), f(rel.velocity[1], rel.velocity_exponent)];
        let miss = (got[0] - want[0]).abs().max((got[1] - want[1]).abs());
        let galilean = (vf[0] - wf[0] - want[0]).abs().max((vf[1] - wf[1] - want[1]).abs());
        println!("relativistic composition: miss {miss:.1e}; the Galilean difference misses by {galilean:.1e}");
        assert!(miss < 1e-15 && galilean > 1e-2);
    }
}
