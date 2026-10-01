//! A fleet: a battle in a Fermi frame whose reference tube lives in a planet's doll, and its life.
//!
//! Every ship of the fleet is a member of exactly one frame (`crates/engine`'s [`Battle`]): a
//! lattice body of law `es-lattice-relativistic-v1`, in the freely falling frame of the fleet's
//! centre of mass, feeling only the tide of the planet as integer kicks at fixed epochs. The frame
//! falls along an exact tube of the planet's doll; contacts happen inside the frame, as the
//! engine does them. Lattice scale: `c = 2^20` lattice units per tick, so one lattice unit is
//! `2^-20` of the star's `M`, and a lattice chronon is one tick of the root clock. The planet's
//! pull in lattice units is `μ = 2^(mass_log2 + 60)`, which fixes the frame's mean motion from its
//! radius.
//!
//! **The frame's origin is a tube in its doll like any other**, so it takes the doll's kicks (the
//! parent's tide, the secondaries' pulls: [`crate::force::acceleration`], the same function ships use)
//! through the same split: a kick at the middle of a step of `1/2^step_log2` of the tube's radial
//! period, a power of two of ticks, the drift being the tube itself (zero work). The origin's tube is
//! the engine's (`Battle::kick_origin` rebinds it with the exact remainder, as an anchor does); its
//! plan (kick, boundary) is this fleet's, and an event of the queue like a ship's. The frame's
//! validity ends when its origin leaves the doll, meets the planet, or comes near a secondary's
//! shells (where the tide is no longer first order and the changeover belongs to ships).
//!
//! **The frame's life.** A member that leaves the frame's validity (the engine's size rule) is handed
//! into the doll as its own tube: the hand-off record (the member's exact state relative to the
//! origin, and the origin's) is composed into the doll's frame and bound as a ship's tube, with the
//! remainder carried ([`Leaver`]). A frame with fewer than [`MIN_MEMBERS`] members has nothing left to
//! touch, so it hands out the rest at that anchor and dissolves; a dissolved battle is dropped, costs
//! nothing and never wakes again. Every one of these is an event of the law at a canonical tick, so the
//! universe's digest does not depend on the budget, the threads or the slicing of the battle.
//!
//! The battle is an entity of the queue: it is advanced only as far as the player can see it (its
//! committed tick follows the retarded time of its light, `now − distance`), and in slices.
use crate::body::{Item, What};
use crate::ctx::Ctx;
use crate::force;
use crate::num::{norm2, scale2, sub2, time_of, Error, Res, Tick, V2};
use crate::step::{insert, to_word, MAX_STEP, MIN_STEP};
use emergent_engine::{AnchorPolicy, Battle, Frame, Handoff, Outcome};
use emergent_lattice::{chronon::Chronon, law::World, Kickable, Motion};
use emergent_lattice_event::EventCore;
use emergent_space::{binding::IntegerState, orbit::Scalar};

/// Lattice units per tick: the lattice's `Q`.
pub const Q: i64 = 1 << 20;
/// `log2 Q`: a lattice length is `2^-Q_LOG2` of a root length unit, and `c = 1` is `Q` lattice units per tick.
const Q_LOG2: i32 = 20;
/// A frame with fewer members than this has nothing to resolve: its members are tubes of the doll.
pub const MIN_MEMBERS: usize = 2;
/// A kick's `Δv` in `2^-48` lattice units per chronon: `c` units times `2^(48 + Q_LOG2)`.
const DV_BITS: i32 = 48 + Q_LOG2;

/// What the universe asks of a battle, whichever stepper runs it.
pub trait Battlefield: Send {
    fn tick(&self) -> Tick;
    fn run_to(&mut self, horizon: Tick) -> Result<(), String>;
    fn motions(&self, out: &mut Vec<Motion>);
    /// The frame origin's position at `tick` from the parent's centre, in lattice units.
    fn origin(&self, tick: Tick) -> Option<([f64; 2], [f64; 2])>;
    fn outcome(&self) -> Outcome;
    fn masses(&self) -> Vec<i64>;
    fn contacts(&self) -> u64;
    fn epochs(&self) -> u64;
    fn anchors(&self) -> u64;
    /// The origin's exact state from the planet's centre at `tick`: position `2^-32`, velocity `2^-48` lattice units.
    fn origin_exact(&self, tick: Tick) -> Option<([i128; 2], [i128; 2])>;
    /// `floor(log2)` of the origin tube's radial period, in ticks.
    fn period_log2(&self) -> Option<i32>;
    /// The parent's kick on the origin (`2^-48` lattice units per chronon).
    fn kick_origin(&mut self, dv: [i128; 2]) -> Result<(), String>;
    fn dissolve(&mut self) -> Result<(), String>;
    fn is_dissolved(&self) -> bool;
    /// One flag per member (index order): false once handed out.
    fn active(&self) -> &[bool];
    fn handoffs(&self) -> &[Handoff];
    /// A handed-out member's sub-lattice-unit position remainder (`2^-48`).
    fn owed(&self, index: usize) -> [i128; 2];
}

impl<S: Kickable + Send> Battlefield for Battle<S> {
    fn tick(&self) -> Tick {
        self.stepper().tick()
    }
    fn run_to(&mut self, horizon: Tick) -> Result<(), String> {
        Battle::run_to(self, horizon).map_err(|e| e.0)
    }
    fn motions(&self, out: &mut Vec<Motion>) {
        self.stepper().motions(out)
    }
    fn origin(&self, tick: Tick) -> Option<([f64; 2], [f64; 2])> {
        let t = self.tube_at(tick)?;
        let k = 1.0 / (1u64 << 32) as f64;
        let kv = 1.0 / (1u64 << 48) as f64;
        Some(([t.x[0] as f64 * k + t.radius as f64, t.x[1] as f64 * k], [t.v[0] as f64 * kv, t.v[1] as f64 * kv]))
    }
    fn outcome(&self) -> Outcome {
        Battle::outcome(self)
    }
    fn masses(&self) -> Vec<i64> {
        let mut m = Vec::new();
        self.stepper().masses(&mut m);
        m
    }
    fn contacts(&self) -> u64 {
        self.stepper().log().contacts
    }
    fn epochs(&self) -> u64 {
        self.stats().epochs
    }
    fn anchors(&self) -> u64 {
        self.stats().anchors
    }
    fn origin_exact(&self, tick: Tick) -> Option<([i128; 2], [i128; 2])> {
        let t = self.tube_at(tick)?;
        Some(([t.x[0] + ((t.radius as i128) << 32), t.x[1]], t.v))
    }
    fn period_log2(&self) -> Option<i32> {
        self.origin_period_log2()
    }
    fn kick_origin(&mut self, dv: [i128; 2]) -> Result<(), String> {
        Battle::kick_origin(self, dv).map_err(|e| e.0)
    }
    fn dissolve(&mut self) -> Result<(), String> {
        Battle::dissolve(self).map(|_| ()).map_err(|e| e.0)
    }
    fn is_dissolved(&self) -> bool {
        Battle::is_dissolved(self)
    }
    fn active(&self) -> &[bool] {
        Battle::active(self)
    }
    fn handoffs(&self) -> &[Handoff] {
        Battle::handoffs(self)
    }
    fn owed(&self, index: usize) -> [i128; 2] {
        Battle::owed(self, index)
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Order {
    /// Lockstep: the reference stepper (`Chronon`).
    Dense,
    /// Sparse: the event core (`EventCore`).
    Sparse,
}

/// What a dissolved battle leaves behind: its last outcome and counters (the battle itself is dropped).
struct Frozen {
    tick: Tick,
    outcome: Outcome,
    contacts: u64,
    epochs: u64,
    anchors: u64,
}

pub struct Fleet {
    pub name: &'static str,
    /// The doll the frame's tube lives in (a planet's).
    pub doll: u16,
    /// The body that is the centre of that doll.
    pub centre: usize,
    /// The battle in its frame; `None` once dissolved.
    battle: Option<Box<dyn Battlefield>>,
    done: Option<Frozen>,
    pub radius: i64,
    pub n_members: usize,
    /// The origin's position in root units (a cache for deadlines and the view).
    pub pos: [f64; 2],
    /// Member radii in lattice units (for the view).
    pub radii: Vec<i64>,
    /// The origin's plan: the kick at the middle of a step and the boundary at its end (as a ship's).
    plan: Vec<Item>,
    /// The kick step `H` in ticks (a power of two) and the interval now planned.
    step: i64,
    interval: i64,
    /// The sub-quantum part of the parent's kicks (sigma-delta), in `2^-16` of the velocity quantum.
    carry: [i128; 2],
    /// Hand-off records already turned into bodies.
    taken: usize,
    /// Kicks of the origin applied, and refused.
    pub kicks: u64,
    pub refused: u64,
}

/// A member that left the frame, as the doll takes it: its exact state at the hand-off tick, in the
/// doll's integer word (one carry: the rounding to the word, bounded by its quantum), ready to bind.
#[derive(Clone, Debug)]
pub struct Leaver {
    pub member: usize,
    pub tick: Tick,
    pub state: IntegerState,
    /// The member's radius in lattice units.
    pub radius: i64,
}

/// What one call to [`Fleet::advance`] did.
#[derive(Default)]
pub struct Step {
    /// Slices of the battle run (0 or 1), kicks of the origin applied and refused.
    pub slices: u64,
    pub kicks: u64,
    pub refused: u64,
    /// Members handed out of the frame, in the order the frame handed them out.
    pub leavers: Vec<Leaver>,
    /// The frame dissolved in this call.
    pub dissolved: bool,
}

/// The frame's mean motion `n/2^60` rad per tick for a planet of mass `2^mass_log2` (octave of the
/// root's) at lattice radius `radius`: `n = √(μ/R³)`, `μ = 2^(mass_log2 + 60)` in lattice units.
pub fn mean_motion(mass_log2: i32, radius: i64) -> Res<u64> {
    let mu = Scalar::power_of_two((mass_log2 + 60) as i16);
    let r = Scalar::integer(radius);
    let n = mu.div(r.mul(r)?.mul(r)?)?.sqrt()?;
    u64::try_from(n.fixed(60)?).map_err(|_| Error::Refused("mean motion"))
}

/// The origin's state in the doll's units (`M = c = 1`), as scalars, from the engine's lattice integers.
fn origin_state(ctx: &Ctx, doll: u16, b: &dyn Battlefield, t: Tick) -> Res<(V2, V2)> {
    let (x, v) = b.origin_exact(t).ok_or(Error::Refused("a frame with no origin"))?;
    let shift = ctx.dolls[doll as usize].shift as i32;
    // 2^-32 lattice units → root units (× 2^-Q_LOG2) → doll units (× 2^shift); velocities are in c.
    let p = |c: usize| Scalar::raw(x[c], -32 - Q_LOG2 + shift);
    let w = |c: usize| Scalar::raw(v[c], -48 - Q_LOG2);
    Ok(([p(0)?, p(1)?], [w(0)?, w(1)?]))
}

impl Fleet {
    /// A fleet of the world `w` (lattice bodies in the frame's axes), on a circular tube of lattice
    /// radius `radius` about the centre of `doll` (mass `2^mass_log2`), starting at `phase` (turns, Q32)
    /// of the circle at tick 0.
    #[allow(clippy::too_many_arguments)]
    pub fn new(name: &'static str, doll: u16, centre: usize, mass_log2: i32, w: World, radius: i64, phase: u32, order: Order, threads: usize) -> Res<Self> {
        let n = mean_motion(mass_log2, radius)?;
        // Periapsis at the orientation `phase`, at tick 0: the body starts there on a circle.
        let frame = Frame::on_orbit(Q, radius, n, 0, phase, 0).map_err(|_| Error::Refused("frame"))?;
        let policy = AnchorPolicy::default();
        let radii = w.bodies.iter().map(|b| b.radius).collect();
        let n_members = w.bodies.len();
        let battle: Box<dyn Battlefield> = match order {
            Order::Dense => Box::new(
                Battle::new(Chronon::new(w, false).map_err(|_| Error::Refused("chronon"))?, frame, threads)
                    .with_anchoring(policy)
                    .map_err(|_| Error::Refused("anchoring"))?
                    .with_min_members(MIN_MEMBERS),
            ),
            Order::Sparse => Box::new(
                Battle::new(EventCore::new(w, false).map_err(|_| Error::Refused("event core"))?, frame, threads)
                    .with_anchoring(policy)
                    .map_err(|_| Error::Refused("anchoring"))?
                    .with_min_members(MIN_MEMBERS),
            ),
        };
        Ok(Self { name, doll, centre, battle: Some(battle), done: None, radius, n_members, pos: [0.0; 2], radii, plan: Vec::new(), step: 0, interval: 0, carry: [0; 2], taken: 0, kicks: 0, refused: 0 })
    }

    /// The committed tick of the battle (the tick it dissolved at, once dissolved).
    pub fn tick(&self) -> Tick {
        match (&self.battle, &self.done) {
            (Some(b), _) => b.tick(),
            (None, Some(d)) => d.tick,
            _ => 0,
        }
    }
    /// Whether the frame is still there: a dissolved battle has no next event and costs nothing.
    pub fn live(&self) -> bool {
        self.battle.is_some()
    }
    /// Whether member `m` is still in the frame.
    pub fn is_member(&self, m: usize) -> bool {
        self.battle.as_ref().is_some_and(|b| b.active().get(m).copied().unwrap_or(false))
    }
    /// The hand-off records so far (the engine's: the member's exact state against the origin's), for the
    /// universe's tests and measures; empty once the frame is dissolved and its battle dropped.
    pub fn handoffs(&self) -> &[Handoff] {
        self.battle.as_ref().map_or(&[], |b| b.handoffs())
    }
    /// What a handed-out member's position still owes (`2^-48` lattice units): the remainder the record's integer
    /// position does not hold, carried into the doll's tube.
    pub fn owed(&self, index: usize) -> [i128; 2] {
        self.battle.as_ref().map_or([0; 2], |b| b.owed(index))
    }
    pub fn members(&self) -> usize {
        self.battle.as_ref().map_or(0, |b| b.active().iter().filter(|&&a| a).count())
    }
    /// The tick of the next event the fleet could resolve: the next chronon (the battle is advanced in
    /// slices to whatever the frame asks), or the origin's next kick or boundary, if sooner. Never, once
    /// dissolved.
    pub fn next_time(&self) -> Option<Tick> {
        let t = self.battle.as_ref()?.tick() + 1;
        Some(self.plan.first().map_or(t, |i| i.t.min(t)))
    }
    pub fn root_position(&self) -> [f64; 2] {
        self.pos
    }

    /// The tick the next [`Fleet::advance`] runs the battle to: no further than a slice, the limit, or
    /// the origin's next planned event.
    pub fn horizon(&self, slice: Tick, limit: Tick) -> Option<Tick> {
        let t = self.battle.as_ref()?.tick();
        Some((t + slice).min(limit).min(self.plan.first().map_or(Tick::MAX, |i| i.t)))
    }

    /// Plan the origin's first step (the universe has started: every body's tube is there to read).
    pub fn start(&mut self, ctx: &Ctx) {
        if self.plan_origin(ctx, 0).is_err() {
            self.dissolve();
        }
    }

    /// Run the battle to `min(tick + slice, limit)` or the origin's next planned event, whichever is first,
    /// and resolve the origin's events due at the tick it reached; take the members that left the frame.
    pub fn advance(&mut self, ctx: &Ctx, slice: Tick, limit: Tick) -> Step {
        let mut out = Step::default();
        let Some(to) = self.horizon(slice, limit) else { return out };
        let b = self.battle.as_mut().expect("a live fleet");
        if to > b.tick() {
            b.run_to(to).expect("a fleet's frame is valid");
            out.slices = 1;
        }
        // The origin's events: the same kicks and boundaries a ship has, at their ticks.
        while self.battle.as_ref().is_some_and(|b| !b.is_dissolved()) {
            let Some(it) = self.plan.first().copied() else { break };
            if it.t > self.tick() {
                break;
            }
            self.plan.remove(0);
            let t = it.t;
            match it.what {
                What::Kick(_) => match self.kick(ctx, t) {
                    Ok(true) => out.kicks += 1,
                    Ok(false) => {}
                    Err(_) => out.refused += 1,
                },
                What::Boundary => {
                    if self.boundary(ctx, t).is_err() {
                        self.dissolve();
                    }
                }
                _ => {}
            }
        }
        self.kicks += out.kicks;
        self.refused += out.refused;
        // Whoever left the frame, in the order the frame handed them out.
        let b = self.battle.as_ref().expect("a live fleet");
        for h in &b.handoffs()[self.taken..] {
            if let Ok(l) = Self::leaver(ctx, self.doll, h, b.owed(h.index), self.radii[h.index]) {
                out.leavers.push(l);
            }
        }
        self.taken = b.handoffs().len();
        if b.is_dissolved() {
            self.freeze();
            out.dissolved = true;
        }
        out
    }

    /// End the frame now: everyone in it is handed out as they stand (picked up by the next `advance`).
    fn dissolve(&mut self) {
        if let Some(b) = self.battle.as_mut() {
            b.dissolve().expect("a frame with anchoring can end");
        }
        self.plan.clear();
    }

    /// Drop the battle, keeping what its outcome says.
    fn freeze(&mut self) {
        if let Some(b) = self.battle.take() {
            self.done = Some(Frozen { tick: b.tick(), outcome: b.outcome(), contacts: b.contacts(), epochs: b.epochs(), anchors: b.anchors() });
        }
        self.plan.clear();
    }

    /// A hand-off record in the doll's integer word. The member's state is the origin's (the tube at the
    /// hand-off tick, from the planet's centre) plus its own relative to it (position settled to a lattice
    /// unit and the sub-unit remainder the engine still owes it; velocity with its sub-quantum carry), the
    /// sum Galilean as the engine's own recentring is. The word keeps 61 bits, so the lattice's 2^-32 is
    /// rounded to the doll's quantum, once, toward zero.
    fn leaver(ctx: &Ctx, doll: u16, h: &Handoff, owed: [i128; 2], radius: i64) -> Res<Leaver> {
        let x = [0, 1].map(|c| ((h.tube.radius as i128 * (c == 0) as i128) << 32) + h.tube.x[c] + ((h.x[c] as i128) << 32) + (owed[c] >> 16));
        let v = [0, 1].map(|c| h.tube.v[c] + h.v[c]);
        let shift = ctx.dolls[doll as usize].shift as i32;
        let (pw, pe) = to_word(x, -32 - Q_LOG2 + shift)?;
        let (vw, ve) = to_word(v, -48 - Q_LOG2)?;
        Ok(Leaver { member: h.index, tick: h.tick, state: IntegerState { position: pw, velocity: vw, length_exponent: pe, velocity_exponent: ve }, radius })
    }

    // ---- the origin's split ---------------------------------------------------------------------

    /// Plan the interval starting at `t`: the step (a power of two of ticks, `1/2^step_log2` of the tube's
    /// radial period, with hysteresis so it does not chatter), its kick at the middle and its boundary.
    fn plan_origin(&mut self, ctx: &Ctx, t: Tick) -> Res<()> {
        let Some(per) = self.battle.as_ref().and_then(|b| b.period_log2()) else {
            self.plan.clear();
            return Ok(());
        };
        let want = (1i64 << (per - ctx.cfg.step_log2).clamp(1, 50)).clamp(MIN_STEP, MAX_STEP);
        let cur = self.step;
        if cur == 0 || want >= cur.saturating_mul(2) || want.saturating_mul(2) <= cur {
            self.step = want;
        }
        let h = self.step;
        self.interval = h;
        insert(&mut self.plan, Item { t: t + h / 2, what: What::Kick(0) });
        insert(&mut self.plan, Item { t: t + h, what: What::Boundary });
        Ok(())
    }

    /// The parent's kick at the middle of a step: `Δv = h·a` from the doll's kick sources at the origin's
    /// position (the secondaries' pulls and the parent's tide, as for a ship), whole `2^-48` quanta
    /// applied to the origin's tube (the rest carried). Whether a kick was applied.
    fn kick(&mut self, ctx: &Ctx, t: Tick) -> Res<bool> {
        let b = self.battle.as_mut().expect("a live fleet");
        let (x, _) = origin_state(ctx, self.doll, &**b, t)?;
        let secs = ctx.secondaries(self.doll, t, usize::MAX)?;
        let tide = ctx.tide(self.doll, t)?;
        let a = force::acceleration(0, x, &secs, tide)?;
        let dv = scale2(a, time_of(self.interval, ctx.dolls[self.doll as usize].clock_exp())?)?;
        let mut whole = [0i128; 2];
        let mut carry = self.carry;
        for c in 0..2 {
            let total = carry[c] + dv[c].fixed(DV_BITS + 16)?;
            whole[c] = total.div_euclid(65536);
            carry[c] = total.rem_euclid(65536);
        }
        if whole == [0, 0] {
            self.carry = carry;
            return Ok(false);
        }
        b.kick_origin(whole).map_err(|_| Error::Refused("the frame cannot hold the kicked tube"))?;
        self.carry = carry;
        Ok(true)
    }

    /// The end of a step: the frame's validity (its origin is in the doll, off the planet and clear of
    /// every secondary's shells), then the next step.
    fn boundary(&mut self, ctx: &Ctx, t: Tick) -> Res<()> {
        let b = self.battle.as_ref().expect("a live fleet");
        let (x, v) = origin_state(ctx, self.doll, &**b, t)?;
        let doll = &ctx.dolls[self.doll as usize];
        let r = norm2(x)?;
        let mut valid = r <= doll.edge && r >= doll.surface;
        if valid {
            let h = time_of(self.interval, doll.clock_exp())?;
            for s in ctx.secondaries(self.doll, t, usize::MAX)? {
                if force::engaged(0, norm2(sub2(s.pos, x)?)?, force::relative_speed(v, s.vel)?, h, s.edge)? {
                    valid = false;
                    break;
                }
            }
        }
        if !valid {
            self.dissolve();
            return Ok(());
        }
        self.plan_origin(ctx, t)
    }

    // ---- what it says ---------------------------------------------------------------------------

    pub fn outcome_digest(&self) -> String {
        let o = self.outcome();
        format!("{}{}{}", o.world, o.log, o.tide)
    }
    /// The frame's whole state for the universe's digest: the battle's outcome, the origin's plan and
    /// carry, and how many hand-offs have been taken.
    pub fn digest_into(&self, h: &mut blake3::Hasher) {
        h.update(self.outcome_digest().as_bytes());
        for v in [self.step as i128, self.interval as i128, self.taken as i128, self.battle.is_none() as i128, self.carry[0], self.carry[1], self.kicks as i128, self.refused as i128] {
            h.update(&v.to_le_bytes());
        }
        for it in &self.plan {
            h.update(&(it.t as i128).to_le_bytes());
            h.update(&[if it.what == What::Boundary { 1 } else { 0 }]);
        }
    }
    pub fn outcome(&self) -> Outcome {
        match (&self.battle, &self.done) {
            (Some(b), _) => b.outcome(),
            (None, Some(d)) => d.outcome.clone(),
            _ => unreachable!("a fleet is live or dissolved"),
        }
    }
    pub fn contacts(&self) -> u64 {
        self.battle.as_ref().map_or_else(|| self.done.as_ref().map_or(0, |d| d.contacts), |b| b.contacts())
    }
    pub fn epochs(&self) -> u64 {
        self.battle.as_ref().map_or_else(|| self.done.as_ref().map_or(0, |d| d.epochs), |b| b.epochs())
    }
    pub fn anchors(&self) -> u64 {
        self.battle.as_ref().map_or_else(|| self.done.as_ref().map_or(0, |d| d.anchors), |b| b.anchors())
    }
    pub fn motions(&self, out: &mut Vec<Motion>) {
        match &self.battle {
            Some(b) => b.motions(out),
            None => out.clear(),
        }
    }
    /// The frame origin in lattice units from the planet's centre, and its velocity (lattice units per tick).
    pub fn origin(&self, tick: Tick) -> Option<([f64; 2], [f64; 2])> {
        self.battle.as_ref()?.origin(tick)
    }
}
