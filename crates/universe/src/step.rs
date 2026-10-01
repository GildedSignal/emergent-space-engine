//! Motion: the compiled drift plus kicks (docs/law.md, "Perturbed motion").
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
use crate::bind::{bind, scalars, Binding, Bound, Entry};
use crate::body::{BodyRec, Item, Kind, Segment, What};
use crate::ctx::Ctx;
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
    let mut period = match &b.entry.trajectory {
        Trajectory::Cycle(c) => c.period()?,
        Trajectory::Passage(p) => p.duration()?,
    };
    if let (Some(edge), Some(tp)) = (edge, next_periapsis(b, b.event_time)?) {
        if b.entry.trajectory.key().periapsis < edge {
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

fn rank(w: What) -> u8 {
    match w {
        What::Kick(l) => 10 + l,
        What::Crash => 15,
        What::Open(l) => 20 + l,
        What::Boundary => 40,
    }
}
fn insert(plan: &mut Vec<Item>, it: Item) {
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
fn to_word(v: [i128; 2], exp: i32) -> Res<([i64; 2], i16)> {
    let bits = 128 - (v[0].unsigned_abs().max(v[1].unsigned_abs())).leading_zeros() as i32;
    let shift = (bits - 61).max(0);
    let word = |x: i128| i64::try_from(x / (1i128 << shift)).map_err(|_| Error::Refused("word"));
    Ok(([word(v[0])?, word(v[1])?], i16::try_from(exp + shift).map_err(|_| Error::Refused("exponent"))?))
}

fn lift(a: &IntegerState, c: usize, velocity: bool, el: i32, ev: i32) -> i128 {
    if velocity {
        (a.velocity[c] as i128) << (a.velocity_exponent as i32 - ev)
    } else {
        (a.position[c] as i128) << (a.length_exponent as i32 - el)
    }
}

/// Re-express `st` (a state in the doll whose clock exponent is `from`) relative to the doll's
/// child centre `centre` (a state in the same doll), in the child doll (`to`): subtract, then
/// relabel the length exponent (one doll unit is `2^(to − from)` of the other). Exact.
fn relative(st: &IntegerState, centre: &IntegerState, from: i16, to: i16) -> Res<IntegerState> {
    let (el, ev) = (st.length_exponent.min(centre.length_exponent) as i32, st.velocity_exponent.min(centre.velocity_exponent) as i32);
    let p = [0, 1].map(|c| lift(st, c, false, el, ev) - lift(centre, c, false, el, ev));
    let v = [0, 1].map(|c| lift(st, c, true, el, ev) - lift(centre, c, true, el, ev));
    let (pw, pe) = to_word(p, el + (to as i32 - from as i32))?;
    let (vw, ve) = to_word(v, ev)?;
    Ok(IntegerState { position: pw, velocity: vw, length_exponent: pe, velocity_exponent: ve })
}

/// The inverse: `rel` in the child doll (`from`) plus the child's centre in the parent (`to`).
/// The sum is rounded to the parent's word (toward zero): the one carry of a handoff, bounded by
/// one quantum of the parent's units.
fn absolute(rel: &IntegerState, centre: &IntegerState, from: i16, to: i16) -> Res<IntegerState> {
    let in_parent = IntegerState { length_exponent: rel.length_exponent - (from - to), ..*rel };
    let (el, ev) = (in_parent.length_exponent.min(centre.length_exponent) as i32, in_parent.velocity_exponent.min(centre.velocity_exponent) as i32);
    let p = [0, 1].map(|c| lift(&in_parent, c, false, el, ev) + lift(centre, c, false, el, ev));
    let v = [0, 1].map(|c| lift(&in_parent, c, true, el, ev) + lift(centre, c, true, el, ev));
    let (pw, pe) = to_word(p, el)?;
    let (vw, ve) = to_word(v, ev)?;
    Ok(IntegerState { position: pw, velocity: vw, length_exponent: pe, velocity_exponent: ve })
}

/// The first tick at or after `after` where the tube is at or beyond `edge` (outward), if any.
fn next_exit(b: &Binding, after: Tick, edge: Scalar) -> Res<Option<Tick>> {
    let outside = |t: Tick| -> Res<bool> { Ok(b.orbit_state(t)?.radius >= edge) };
    if outside(after)? {
        return Ok(Some(after));
    }
    let peri = time_of(b.tube.periapsis_time.get() as i64, b.clock_exp)?;
    let after_s = time_of(after, b.clock_exp)?;
    let apex = match &b.entry.trajectory {
        Trajectory::Cycle(c) => {
            let period = c.period()?;
            if edge > c.signed_state(period.scale(-1)?)?.radius {
                return Ok(None);
            }
            let n = after_s.sub(peri)?.div(period)?.fixed_floor(0)?;
            let mut apex = peri.add(period.mul(Scalar::raw(n, 0)?)?)?.add(period.scale(-1)?)?;
            if apex < after_s {
                apex = apex.add(period)?;
            }
            apex
        }
        Trajectory::Passage(p) => peri.add(p.duration()?.scale(-1)?)?,
    };
    // A passage's last readable tick is one before its window closes: round the end inward.
    let end = if matches!(b.entry.trajectory, Trajectory::Passage(_)) { apex.fixed_floor(-(b.clock_exp as i32))? - 1 } else { apex.fixed_ceil(-(b.clock_exp as i32))? };
    let (mut lo, mut hi) = (after, i64::try_from(end).map_err(|_| Error::Refused("exit"))?);
    if hi < lo || !outside(hi)? {
        return Ok(None);
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
            let period = c.period()?;
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

/// The proper time (root units) a binding's tube has run between `since` (or its binding event, if later)
/// and `t`: a clock reads its tube's length. `shift` is the doll's clock exponent.
pub fn proper_since(b: &Binding, shift: i16, since: Tick, t: Tick) -> Res<Scalar> {
    let tau = b.orbit_state(t)?.proper_time.sub(b.orbit_state(since.max(b.event_time))?.proper_time)?;
    Ok(tau.scale(-(shift as i32))?)
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

    /// Passage tubes are compiled out to four sphere-of-influence radii: past the edge the ship has
    /// been released long before the tube ends.
    fn passage_edge(&self, doll: u16) -> Option<Scalar> {
        (doll != 0).then(|| self.ctx.dolls[doll as usize].edge.scale(2).ok()).flatten()
    }

    /// Whether anything can kick this body: a secondary in its doll (other than itself) or a parent.
    fn has_forces(&self, doll: u16) -> bool {
        self.ctx.dolls[doll as usize].parent.is_some() || self.ctx.sources[doll as usize].iter().any(|&j| j != self.i)
    }

    /// Bind `exact` at `t` in `doll` and replace the body's binding, keeping the old one as history.
    fn rebind(&mut self, exact: IntegerState, t: Tick, doll: u16) -> Res<Bound> {
        let clock_exp = self.ctx.dolls[doll as usize].clock_exp();
        let bound = bind(exact, t, clock_exp, self.passage_edge(doll))?;
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
            delta: bound.delta,
            units: bound.units,
            clock_exp,
            event_time: t,
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
        let (heading, v2) = thrust::owed(self.ctx.cfg, th, dtau, x, v)?;
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
        let next = if thrusting {
            // The player's burn rides on the level-0 kick: velocity after the tide, then the boost.
            let v2 = self.burn(x, add2(v, dv)?, t)?;
            IntegerState { velocity: self.velocity_after(&st, v2)?, ..st }
        } else {
            let (dvq, carry) = quantize(dv, st.velocity_exponent, self.rec.carry)?;
            self.rec.carry = carry;
            if dvq == [0, 0] {
                // A sub-quantum kick fires nothing: it is carried.
                return Ok(());
            }
            IntegerState { velocity: [st.velocity[0] + dvq[0], st.velocity[1] + dvq[1]], ..st }
        };
        self.rebind(next, t, d)?;
        Ok(())
    }

    /// Deep inside a planet's shell the planet is the dominant body: the child doll of `centre`
    /// takes the ship. Returns whether it did.
    fn maybe_capture(&mut self, t: Tick, st: &IntegerState, x: V2) -> Res<bool> {
        let d = self.rec.b.doll;
        if !matches!(self.rec.kind, Kind::Ship | Kind::Player) {
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
        let mut h = self.rec.step;
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
            if key.periapsis < self.doll().surface {
                if let Some(tp) = next_periapsis(&self.rec.b, t)? {
                    if tp <= t + h {
                        insert(&mut self.rec.plan, Item { t: tp.max(t + 1), what: What::Crash });
                    }
                }
            }
        }
        self.open(t, 0, h)
    }

    fn thrust_step(&self, t: Tick) -> Res<i64> {
        let st = self.rec.b.readout(t)?;
        let (x, v) = scalars(&st)?;
        let speed = norm2(v)?.max(Scalar::ONE.div(norm2(x)?)?.sqrt()?);
        // α in rapidity per tick: 2^thrust_log2 per root unit, and a tick is 2^0 root units.
        let alpha = Scalar::power_of_two(self.ctx.cfg.thrust_log2 as i16);
        let ticks = speed.scale(-THRUST_FRACTION_LOG2)?.div(alpha)?;
        let exp = log2_floor(ticks).clamp(1, 50);
        Ok((1i64 << exp).clamp(MIN_STEP, MAX_STEP))
    }

    /// The end of a step: certificates, then the next step's plan.
    fn boundary(&mut self, t: Tick) -> Res<Resolved> {
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
pub fn decide(ctx: &Ctx, i: usize, rec: BodyRec, t: Tick, keys: u8) -> Update {
    let mut w = Work { ctx, i, rec, retired: Vec::new(), new_entry: None };
    let same = w.rec.thrust.is_some_and(|th| th.keys == keys);
    let res = (|| -> Res<()> {
        if let Some(th) = w.rec.thrust.filter(|th| th.keys != 0 && t > th.since) {
            let st = w.rec.b.readout(t)?;
            let (x, v) = scalars(&st)?;
            let v2 = w.burn(x, v, t)?;
            if th.keys & 3 != 0 {
                let next = IntegerState { velocity: w.velocity_after(&st, v2)?, ..st };
                w.rebind(next, t, w.rec.b.doll)?;
            }
        }
        if let Some(th) = w.rec.thrust.as_mut() {
            th.keys = keys;
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
}
