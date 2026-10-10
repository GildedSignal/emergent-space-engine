//! One clock, one queue, one digest.
//!
//! **The root clock is canonical.** A tick is the same physical time in every doll
//! ([`crate::world`]). Every entity (a body, a fleet) holds the time of its next certified event;
//! the queue is a min over entities, with deterministic ties (time, then entity id, ids running
//! star, planets, moon, ships, player, the members a fleet hands out (in the order it hands them
//! out), fleets).
//!
//! **The canonical key of an event is (tick, smallest body id, kind)** (docs/law.md, "Ties"). Events that
//! share no body commute (a body's event writes only that body). Events that share a body are ordered by the key:
//! an event reads another body at its own tick *after* every event of that body with a smaller key, and
//! before the rest, so a read at a tied tick is well defined (a segment of a body's history is readable
//! from its binding event up to, not including, the next); and the kinds of one body at one tick run
//! kick, impact, open, boundary, then the player's decision ([`crate::step`]'s `rank`, [`Universe::schedule`]). The
//! fleet's same-epoch contacts are one batch of the lattice law (bodies sorted by id, pairs sorted), inside the
//! battle. The queue's own order (the light-delayed deadline) is only a schedule: nothing it breaks a tie by
//! reaches an outcome.
//!
//! **Resolution is pull-driven, so the outcome cannot depend on the schedule.** An event reads other
//! bodies' tubes at its own tick and writes only its own body. Before an event at key `(t, id)` is
//! resolved, every event it reads from with a smaller key is resolved first (planets for
//! everyone, the moon for ships in a planet's doll, the ships for the player's neighbourhood
//! check). Any order that respects that gives the same bits; that is what the budget and the
//! threads are free to choose.
//!
//! **The budget.** A frame has a hard deadline. [`Universe::advance`] spends a budget in
//! *causal-deadline order*: an item's deadline is when its light reaches the player,
//! `t + distance` (c = 1, a root length unit is a tick of light). The presentable horizon is the
//! smallest deadline still unresolved: nothing the player could see by then is missing. Work whose
//! deadline is later than the frame is *idle-time* work, done only while the budget lasts.
//! When the mandatory work does not fit, the horizon stays behind the target: the real-time
//! factor dips for a frame, smoothly, and nothing hitches or degrades.
use crate::bind::{bind, bind_exact, Binding, Catalogue, Entry};
use crate::body::{BodyRec, BodyStore, Kind, PlainBodies, Segment, Thrust, What};
use crate::ctx::{BodyInfo, Config, Ctx};
use crate::encounter::{Encounter, Encounters, PlayerNeighbourhood};
use crate::fleet::{Fleet, Leaver};
use crate::num::{Error, Res, Tick};
use crate::step::{self, Resolved, Update};
use crate::world::{DollRec, Mass, Unit};
use emergent_space::{
    binding::Trajectory,
    events::Calendar,
    orbit::{Orbit, OrbitKey, Scalar},
    Tube,
};
use std::collections::VecDeque;
use std::sync::Arc;
use std::time::Instant;

#[cfg(test)]
#[path = "root_keys_test.rs"]
mod root_keys_test;

/// A frame's allowance: a number of events, and optionally a wall-clock instant.
#[derive(Clone, Copy, Debug)]
pub struct Budget {
    pub events: u64,
    pub until: Option<Instant>,
}
impl Budget {
    pub fn unlimited() -> Self {
        Self { events: u64::MAX, until: None }
    }
    pub fn events(n: u64) -> Self {
        Self { events: n, until: None }
    }
    pub fn wall(ms: f64) -> Self {
        Self { events: u64::MAX, until: Some(Instant::now() + std::time::Duration::from_secs_f64(ms / 1e3)) }
    }
    fn spent(&self, done: u64) -> bool {
        done >= self.events || self.until.is_some_and(|u| Instant::now() >= u)
    }
}

/// What one presented frame did.
#[derive(Clone, Copy, Debug)]
pub struct Frame {
    pub target: Tick,
    pub presented: Tick,
    /// Game ticks the frame advanced the presented time by.
    pub ticks: Tick,
    pub events: u64,
    pub overflow: bool,
}

/// What a call to [`Universe::advance`] did.
#[derive(Clone, Copy, Debug, Default)]
pub struct Advanced {
    pub events: u64,
    /// The presentable horizon: every item whose light could reach the player by it is resolved.
    pub horizon: Tick,
    /// Mandatory work (deadline within the target) was left because the budget ran out.
    pub overflow: bool,
}

#[derive(Clone, Copy, Debug, Default)]
pub struct Stats {
    pub kicks: u64,
    pub opens: u64,
    pub boundaries: u64,
    pub handoffs: u64,
    pub lost: u64,
    pub refused: u64,
    pub slices: u64,
    pub encounters: u64,
    pub decisions: u64,
    /// Members handed out of a frame into a doll, and frames dissolved.
    pub leavers: u64,
    pub dissolved: u64,
    /// Wall nanoseconds and items resolved, by kind: planet, moon, ship, player, fleet.
    pub cost_ns: [u64; 5],
    pub items: [u64; 5],
}
impl Stats {
    pub fn events(&self) -> u64 {
        self.kicks + self.opens + self.boundaries + self.handoffs + self.slices + self.decisions
    }
}

/// How a body is made: a tube of a doll from its orbit.
#[derive(Clone, Copy, Debug)]
pub struct OrbitSpec {
    pub doll: u16,
    /// Periapsis radius in the doll's units, and eccentricity in Q48.
    pub periapsis: Scalar,
    pub e_q48: u64,
    pub clockwise: bool,
    /// Where periapsis points, in turns (Q32).
    pub angle: u32,
    /// Where the body is on its orbit at tick 0: the fraction of the radial period since periapsis, in Q32.
    pub phase: u32,
}

pub struct Universe {
    pub dolls: Vec<DollRec>,
    pub info: Vec<BodyInfo>,
    /// How each body made by `add_body` was specified (a secondary's tube is compiled again when its mass is set).
    specs: Vec<Option<OrbitSpec>>,
    pub sources: Vec<Vec<usize>>,
    pub cfg: Config,
    bodies: Box<dyn BodyStore>,
    cat: Catalogue,
    pub fleets: Vec<Fleet>,
    queue: Option<Calendar>,
    /// The presented time of the last frame, and the position of the player used for deadlines.
    pub now: Tick,
    player: Option<usize>,
    observer: [f64; 2],
    /// Cached positions in root units (for deadlines only; never an outcome).
    pos: Vec<[f64; 2]>,
    pub stats: Stats,
    pub inputs: Vec<(Tick, u8)>,
    /// Members the frame handed out whose tubes are not made yet, in hand-out order ([`Universe::resolve_handout`]):
    /// each is an item of the queue (the front one has the next body id), made when the budget gets to it.
    handouts: VecDeque<(usize, Leaver)>,
    /// Decisions scheduled at canonical ticks and not yet taken, in order ([`Universe::schedule`]).
    pending: VecDeque<(Tick, u8)>,
    /// The tick of the last decision scheduled or taken: the log is written in order.
    last_decision: Tick,
    /// Threads the resolver may use for independent ships.
    pub threads: usize,
    /// The frame's slice of a fleet's battle, in ticks.
    pub slice: Tick,
    lanes: Lanes,
    target: Tick,
    encounters: Box<dyn Encounters>,
    pub enc_log: Vec<Encounter>,
    enc_digest: [u8; 32],
    pub contacts: u64,
    /// Every item resolved (a refusal or a loss counts: it was work).
    resolved: u64,
    frames: u64,
    /// Entity ids below this are bodies (those made, and the room for every member a fleet can hand out);
    /// a fleet's entity id is `body_cap + its index`.
    body_cap: usize,
}

#[derive(Default)]
struct Lanes {
    planets: Vec<usize>,
    moons: Vec<usize>,
    ships: Vec<usize>,
}

impl Universe {
    pub fn new(star_surface: Scalar, cfg: Config) -> Self {
        Self {
            dolls: vec![DollRec::root("star", star_surface)],
            info: Vec::new(),
            specs: Vec::new(),
            sources: vec![Vec::new()],
            cfg,
            bodies: Box::<PlainBodies>::default(),
            cat: Catalogue::default(),
            fleets: Vec::new(),
            queue: None,
            now: 0,
            player: None,
            observer: [0.0; 2],
            pos: Vec::new(),
            stats: Stats::default(),
            inputs: Vec::new(),
            handouts: VecDeque::new(),
            pending: VecDeque::new(),
            last_decision: 0,
            threads: 1,
            slice: 1 << 18,
            lanes: Lanes::default(),
            target: 0,
            encounters: Box::new(PlayerNeighbourhood),
            enc_log: Vec::new(),
            enc_digest: [0; 32],
            contacts: 0,
            resolved: 0,
            frames: 0,
            body_cap: 0,
        }
    }

    pub fn ctx(&self) -> Ctx<'_> {
        Ctx { dolls: &self.dolls, bodies: &*self.bodies, info: &self.info, sources: &self.sources, cfg: &self.cfg }
    }
    pub fn bodies(&self) -> &dyn BodyStore {
        &*self.bodies
    }
    pub fn catalogue_live(&self) -> usize {
        self.cat.live()
    }
    pub fn player(&self) -> Option<usize> {
        self.player
    }
    pub fn n_bodies(&self) -> usize {
        self.bodies.len()
    }
    /// Members the frame has handed out whose tubes are not made yet (each is an item of the queue).
    pub fn pending_handouts(&self) -> usize {
        self.handouts.len()
    }

    /// Add a child doll centred on an existing body (a tube in the parent doll). `mass` is the doll's
    /// mass as a mantissa with the doll's exponent ([`Mass`], in units of the root's mass; an `i32` is the
    /// old call, a power of two); `surface` the centre's radius in the doll's units. The centre becomes a
    /// secondary of its host doll with `G·m` in the host's units, and its sphere of influence (Laplace,
    /// from the mass ratio) the doll's edge.
    pub fn add_doll(&mut self, name: &'static str, centre: usize, mass: impl Into<Mass>, surface: Scalar) -> Res<u16> {
        let mass = mass.into();
        let host = self.bodies.rec(centre).b.doll;
        let tube = self.bodies.rec(centre).b.tube;
        // The separation in the host's own units (the tube is compiled in units of the host's mass).
        let sep = self.bodies.rec(centre).b.to_doll(self.bodies.rec(centre).b.entry.trajectory.key().periapsis)?;
        let parent_rec = self.dolls[host as usize].record.clone();
        let rec = DollRec::child(name, host, mass, centre, tube, surface, Scalar::ZERO)?;
        // The sphere of influence from the mass ratio (Laplace): separation · (m/M)^(2/5), in the parent's units.
        let soi_parent = rec.record.edge_radius(&parent_rec, sep)?;
        let id = u16::try_from(self.dolls.len()).map_err(|_| Error::Refused("too many dolls"))?;
        let shift_h = self.dolls[host as usize].shift;
        let edge = soi_parent.scale((-mass.octave) - shift_h as i32)?;
        self.dolls.push(DollRec { edge, ..rec });
        self.sources.push(Vec::new());
        self.info[centre].doll = Some(id);
        self.info[centre].soi = soi_parent;
        // `G·m` in the host's units: the mass over the host's length unit, `μ·2^(e − e_host)`.
        self.info[centre].gm = mass.mantissa.scale(mass.octave - self.dolls[host as usize].mass_log2)?;
        self.sources[host as usize].push(centre);
        self.retune(centre)?;
        Ok(id)
    }

    /// The exact binding of an orbit spec in `spec.doll`, its trajectory compiled about a central mass of `unit.mu`
    /// (in the doll's units): the orbit is given in the doll's units, so in the tube's its periapsis is `p/μ`.
    /// Returns the entry and the tube without a catalogue key.
    fn spec_binding(&self, spec: &OrbitSpec, unit: Unit) -> Res<(Arc<Entry>, Tube, (i16, i16))> {
        let doll = &self.dolls[spec.doll as usize];
        let key = OrbitKey::bound(unit.to_tube(spec.periapsis)?, spec.e_q48)?;
        let orbit = Orbit::compile(key)?;
        let period = unit.to_doll(orbit.period()?)?;
        let entry = Arc::new(Entry { trajectory: Trajectory::Cycle(orbit), clockwise: spec.clockwise, unit });
        // Periapsis `phase` of a period before tick 0.
        let behind = period.mul(Scalar::raw(spec.phase as i128, -32)?)?;
        let peri = -i64::try_from(behind.fixed(-(doll.clock_exp() as i32))?).map_err(|_| Error::Refused("period outside the clock"))?;
        let k = Scalar::raw(key.k as i128, -48)?;
        let r_max = unit.to_doll(key.periapsis.div(k.scale(1)?.sub(Scalar::ONE)?)?)?; // apoapsis: p/(2k − 1)
        let v_max = Scalar::integer(2).mul(Scalar::ONE.div(key.periapsis)?)?.sqrt()?.scale(1)?;
        Ok((entry, Tube::new(0, spec.angle, peri), crate::bind::choose_units(r_max, v_max)))
    }

    /// Make a body from an orbit: a tube of `spec.doll`, exactly (no remainder to carry).
    pub fn add_body(&mut self, kind: Kind, spec: OrbitSpec, radius: Scalar) -> Res<usize> {
        let (entry, mut tube, units) = self.spec_binding(&spec, self.dolls[spec.doll as usize].unit)?;
        tube.key = self.cat.insert(entry.clone())?;
        let b = bind_exact(entry, tube, self.dolls[spec.doll as usize].clock_exp(), units, 0, spec.doll);
        let rec = BodyRec {
            kind,
            b,
            carry: [0; 2],
            proper: Scalar::ZERO,
            step: 0,
            interval: 0,
            anchor: 0,
            plan: Vec::new(),
            thrust: (kind == Kind::Player).then_some(Thrust { keys: 0, level: 0, heading: 0, since: 0 }),
            ext: None,
            alive: true,
            events: 0,
            refusals: 0,
            fault: None,
        };
        let i = self.bodies.push(rec);
        self.info.push(BodyInfo { kind, gm: Scalar::ZERO, soi: Scalar::ZERO, doll: None, radius, from: None, born: 0 });
        self.specs.push(Some(spec));
        if kind == Kind::Player {
            self.player = Some(i);
        }
        Ok(i)
    }

    /// Make a body from an exact state at tick 0: `position` and `velocity` (scalars, in the doll's units, `c = 1`),
    /// rounded once to the integer word the state needs (that integer state is the body's, exactly), then bound
    /// as any rebinding is: a tube with its remainder carried. For a test particle in `doll` (about the doll's
    /// centre alone). The way to start a body from a state a float oracle gives (a circular barycentric orbit).
    pub fn add_body_state(&mut self, kind: Kind, doll: u16, position: [Scalar; 2], velocity: [Scalar; 2], radius: Scalar) -> Res<usize> {
        let d = &self.dolls[doll as usize];
        let (x, v) = (crate::num::norm2(position)?, crate::num::norm2(velocity)?);
        if x.is_zero() || v.is_zero() {
            return Err(Error::Refused("a state at rest or at the centre has no orbit"));
        }
        let (le, ve) = crate::bind::choose_units(x.scale(2)?, v.scale(2)?);
        let word = |a: Scalar, e: i16| -> Res<i64> { i64::try_from(a.fixed(-(e as i32))?).map_err(|_| Error::Refused("state outside the integer word")) };
        let exact = emergent_space::binding::IntegerState {
            position: [word(position[0], le)?, word(position[1], le)?],
            velocity: [word(velocity[0], ve)?, word(velocity[1], ve)?],
            length_exponent: le,
            velocity_exponent: ve,
        };
        let edge = (doll != 0).then(|| d.edge.scale(2)).transpose()?;
        let bound = bind(exact, 0, d.clock_exp(), edge, d.unit)?;
        let mut tube = bound.tube;
        tube.key = self.cat.insert(bound.entry.clone())?;
        let b = Binding { doll, tube, entry: bound.entry, residual: bound.residual, turn: bound.turn, units: bound.units, clock_exp: d.clock_exp(), event_time: 0, kick: crate::bind::Kick::NONE };
        let rec = BodyRec {
            kind,
            b,
            carry: [0; 2],
            proper: Scalar::ZERO,
            step: 0,
            interval: 0,
            anchor: 0,
            plan: Vec::new(),
            thrust: (kind == Kind::Player).then_some(Thrust { keys: 0, level: 0, heading: 0, since: 0 }),
            ext: None,
            alive: true,
            events: 0,
            refusals: 0,
            fault: None,
        };
        let i = self.bodies.push(rec);
        self.info.push(BodyInfo { kind, gm: Scalar::ZERO, soi: Scalar::ZERO, doll: None, radius, from: None, born: 0 });
        self.specs.push(None);
        if kind == Kind::Player {
            self.player = Some(i);
        }
        Ok(i)
    }

    /// The body `i` became a secondary with `G·m = gm`: its own tube is now the relative orbit of two bodies,
    /// the Kepler problem of their total mass (the origin falls toward the secondary as the secondary falls
    /// toward the origin), so it is compiled again, as specified, about the host's centre plus `gm`. Before
    /// the universe starts: a body that has run has no spec to rebuild from.
    fn retune(&mut self, i: usize) -> Res<()> {
        let Some(spec) = self.specs.get(i).copied().flatten().filter(|_| self.queue.is_none()) else {
            return Err(Error::Refused("a body's mass is set before the universe starts, on a body made by add_body"));
        };
        let unit = Ctx { dolls: &self.dolls, bodies: &*self.bodies, info: &self.info, sources: &self.sources, cfg: &self.cfg }.tube_unit(i, spec.doll)?;
        let (entry, mut tube, units) = self.spec_binding(&spec, unit)?;
        let mut rec = self.bodies.rec(i);
        self.cat.release(rec.b.tube.key);
        tube.key = self.cat.insert(entry.clone())?;
        rec.b = bind_exact(entry, tube, self.dolls[spec.doll as usize].clock_exp(), units, 0, spec.doll);
        self.bodies.put(i, rec);
        Ok(())
    }

    /// Give a body a pull as a secondary (the moon): `gm` is its mass as a mantissa with an exponent in units
    /// of its host doll's mass (an `i32` is the old call, a power of two), so `G·m` in the host's units is
    /// `gm · μ`, the mass of the host's centre in the host's own length unit.
    pub fn make_source(&mut self, i: usize, gm: impl Into<Mass>, soi: Scalar) -> Res<()> {
        let d = self.bodies.rec(i).b.doll as usize;
        self.info[i].gm = self.dolls[d].unit.to_doll(gm.into().value()?)?;
        self.info[i].soi = soi;
        if !self.sources[d].contains(&i) {
            self.sources[d].push(i);
        }
        self.retune(i)
    }

    /// Replace the encounter finder (the seam): the Binet cone later.
    pub fn set_encounters(&mut self, e: Box<dyn Encounters>) {
        self.encounters = e;
    }

    /// Everything is made: plan every body's first interval and build the queue.
    pub fn start(&mut self) -> Res<()> {
        let n = self.bodies.len();
        self.lanes = Lanes {
            planets: self.kinds(Kind::Planet),
            moons: self.kinds(Kind::Moon),
            ships: self.kinds(Kind::Ship),
        };
        self.pos = vec![[0.0; 2]; n];
        for i in 0..n {
            let rec = self.bodies.rec(i);
            let upd = step::replan(&self.ctx(), i, rec, 0);
            self.apply(i, upd);
        }
        self.body_cap = n + self.fleets.iter().map(|f| f.n_members).sum::<usize>();
        self.queue = Some(Calendar::new(self.body_cap + self.fleets.len()));
        let (ctx, fleets) = self.split();
        for f in fleets.iter_mut() {
            f.start(&ctx);
        }
        // Where each frame is, for the deadlines: a frame that starts at the star's centre (its unset position) would
        // look a hundred million ticks away and be resolved after the player's items that read it.
        for f in 0..self.fleets.len() {
            self.update_fleet_position(f);
        }
        self.rekey();
        Ok(())
    }

    /// Add a fleet. One per universe: a member handed out becomes a body with the next id, and ids issued
    /// in handoff order are canonical only for one fleet (a second would need a range of ids of its own).
    pub fn add_fleet(&mut self, f: Fleet) -> usize {
        assert!(self.fleets.is_empty(), "one fleet per universe: hand-out ids are issued in hand-out order");
        self.fleets.push(f);
        self.fleets.len() - 1
    }

    /// The read-only context and the fleets, borrowed apart (a fleet's step reads the bodies it kicks against).
    fn split(&mut self) -> (Ctx<'_>, &mut Vec<Fleet>) {
        (Ctx { dolls: &self.dolls, bodies: &*self.bodies, info: &self.info, sources: &self.sources, cfg: &self.cfg }, &mut self.fleets)
    }

    /// The entity id of fleet `f`, and the fleet an entity id names (none for a body).
    fn fleet_entity(&self, f: usize) -> usize {
        self.body_cap + f
    }
    fn entity_fleet(&self, e: usize) -> Option<usize> {
        e.checked_sub(self.body_cap)
    }

    // ---- the keys -------------------------------------------------------------------------------

    /// The `(tick, id)` of an entity's next item.
    pub fn key_of(&self, e: usize) -> Option<(Tick, usize)> {
        if e < self.bodies.len() {
            self.bodies.next_time(e).map(|t| (t, e))
        } else if e == self.bodies.len() && e < self.body_cap {
            // The member at the front of the hand-outs is the body that will have this id.
            self.handouts.front().map(|(_, l)| (l.tick, e))
        } else {
            let f = self.entity_fleet(e)?;
            self.fleets.get(f)?.next_time().map(|t| (t, e))
        }
    }

    fn light_distance(&self, e: usize) -> Tick {
        if Some(e) == self.player {
            return 0;
        }
        let p = if e >= self.bodies.len() && e < self.body_cap {
            // A member not made yet is where its frame is.
            self.fleets[self.handouts.front().map_or(0, |h| h.0)].root_position()
        } else {
            match self.entity_fleet(e) {
                Some(f) if e >= self.bodies.len() => self.fleets[f].root_position(),
                _ => self.pos[e],
            }
        };
        let (dx, dy) = (p[0] - self.observer[0], p[1] - self.observer[1]);
        (dx * dx + dy * dy).sqrt().min(4e18) as Tick
    }

    /// The deadline of an entity's next item: when its light reaches the player.
    fn deadline_of(&self, e: usize) -> Option<Tick> {
        self.key_of(e).map(|(t, _)| t.saturating_add(self.light_distance(e)))
    }

    fn requeue(&mut self, e: usize) {
        let d = self.deadline_of(e);
        if let Some(q) = self.queue.as_mut() {
            let _ = q.set(e, d.map(Scalar::integer));
        }
    }

    /// Recompute every deadline from the player's present position (a scheduling heuristic only).
    pub fn rekey(&mut self) {
        if let Some(p) = self.player {
            if let Ok((pos, _)) = crate::observe::root_state_raw(&self.ctx(), p, self.bodies.event_time(p).max(self.now)) {
                self.observer = pos;
            }
        }
        for e in 0..self.bodies.len() {
            self.requeue(e);
        }
        for f in 0..self.fleets.len() {
            self.requeue(self.fleet_entity(f));
        }
        self.requeue(self.bodies.len());
    }

    // ---- resolving ------------------------------------------------------------------------------

    fn apply(&mut self, i: usize, mut upd: Update) {
        for seg in upd.retired.drain(..) {
            self.cat.release(seg.b.tube.key);
            self.bodies.retire(i, Segment { b: seg.b, until: seg.until });
        }
        if let Some(entry) = upd.new_entry.take() {
            if let Ok(id) = self.cat.insert(entry) {
                upd.rec.b.tube.key = id;
            }
        }
        match upd.kind {
            Resolved::Kick => self.stats.kicks += 1,
            Resolved::Open => self.stats.opens += 1,
            Resolved::Boundary => self.stats.boundaries += 1,
            Resolved::Handoff => self.stats.handoffs += 1,
            Resolved::Lost => self.stats.lost += 1,
            Resolved::Refused => self.stats.refused += 1,
        }
        self.resolved += 1;
        let t = upd.rec.b.event_time;
        self.bodies.put(i, upd.rec);
        if let Ok((p, _)) = crate::observe::root_state_raw(&self.ctx(), i, t) {
            self.pos[i] = p;
        }
    }

    fn lane(&self, ids: &[usize]) -> Option<(Tick, usize)> {
        ids.iter().filter_map(|&i| self.key_of(i)).min()
    }

    /// Resolve every item of `ids` with a key below `key`, in key order.
    fn pull(&mut self, ids: &[usize], key: (Tick, usize)) {
        while let Some(k) = self.lane(ids) {
            if k >= key {
                break;
            }
            self.resolve_body(k.1);
        }
    }

    fn kinds(&self, kind: Kind) -> Vec<usize> {
        (0..self.bodies.len()).filter(|&i| self.info[i].kind == kind).collect()
    }

    /// Resolve body `i`'s next item (after the items it reads from).
    fn resolve_body(&mut self, i: usize) {
        let Some(key) = self.key_of(i) else { return };
        let kind = self.info[i].kind;
        let planets = std::mem::take(&mut self.lanes.planets);
        self.pull(&planets, key);
        self.lanes.planets = planets;
        if matches!(kind, Kind::Ship | Kind::Player) {
            let moons = std::mem::take(&mut self.lanes.moons);
            self.pull(&moons, key);
            self.lanes.moons = moons;
        }
        if kind == Kind::Player {
            // The player's neighbourhood check reads every body of its doll: the members a frame hands out
            // before the player's tick must exist, so the fleets run to the tick before it (never to it:
            // a hand-out at the player's own tick comes after the player in the order of ids, and a
            // frame never runs past the presented time, which the digest's cut relies on).
            for f in 0..self.fleets.len() {
                while self.fleets[f].live() && self.fleets[f].tick() < key.0 - 1 {
                    self.resolve_fleet(f, key.0 - 1);
                }
            }
            // ...and so must the members already handed out, each made before the player reads the doll.
            while self.handouts.front().is_some_and(|(_, l)| l.tick < key.0) {
                self.resolve_handout();
            }
            let ships = std::mem::take(&mut self.lanes.ships);
            self.pull(&ships, key);
            self.lanes.ships = ships;
        }
        let rec = self.bodies.rec(i);
        let upd = step::process(&self.ctx(), i, rec);
        self.apply(i, upd);
        if kind == Kind::Player {
            self.encounters_for_player();
        }
    }

    fn resolve_entity(&mut self, e: usize) {
        if e == self.bodies.len() && self.handouts.front().is_some() {
            let t0 = Instant::now();
            self.resolve_handout();
            // The fleet's cost (a hand-out was inside its item): time, not an item.
            self.stats.cost_ns[4] += t0.elapsed().as_nanos() as u64;
            return;
        }
        match self.entity_fleet(e).filter(|_| e >= self.bodies.len()) {
            Some(f) => {
                // The battle may run only as far as the light-delayed deadline of the next entity in
                // line: its committed tick never passes the presented time (the horizon is at least
                // that deadline, less one), so a canonical cut finds every frame at the cut.
                let dist = self.light_distance(e);
                let second = self.queue.as_mut().and_then(|q| {
                    let _ = q.set(e, None);
                    q.peek()
                });
                let cap = second.map_or(Tick::MAX, |(d, _)| (d.fixed(0).unwrap_or(i128::MAX) as Tick).saturating_sub(dist));
                self.resolve_fleet(f, cap);
            }
            None => {
                let t0 = Instant::now();
                let class = self.info[e].kind as usize;
                self.resolve_body(e);
                self.stats.cost_ns[class] += t0.elapsed().as_nanos() as u64;
                self.stats.items[class] += 1;
                self.requeue(e);
            }
        }
    }

    /// One step of fleet `f`: the battle runs to its next slice end or planned event (but not past `cap`),
    /// the origin's kick or boundary due there is resolved, and the members that left the frame become
    /// bodies of the doll.
    fn resolve_fleet(&mut self, f: usize, cap: Tick) {
        let t0 = Instant::now();
        let e = self.fleet_entity(f);
        let (slice, limit) = (self.slice, self.target.min(cap));
        let Some(to) = self.fleets[f].horizon(slice, limit) else { return };
        // What the origin's kick and a leaver's first plan read: the planets and the moon, up to the tick
        // the battle runs to.
        let key = (to + 1, 0);
        let planets = std::mem::take(&mut self.lanes.planets);
        self.pull(&planets, key);
        self.lanes.planets = planets;
        let moons = std::mem::take(&mut self.lanes.moons);
        self.pull(&moons, key);
        self.lanes.moons = moons;
        let step = {
            let (ctx, fleets) = self.split();
            fleets[f].advance(&ctx, slice, limit)
        };
        self.resolved += 1;
        self.stats.slices += step.slices;
        self.stats.kicks += step.kicks;
        self.stats.refused += step.refused;
        // Whoever left is made a body later, one item each, when the budget gets to it (docs/plane.md, foundation 7:
        // a hand-out of nine members used to be one event of thirteen milliseconds).
        self.handouts.extend(step.leavers.into_iter().map(|l| (f, l)));
        self.requeue(self.bodies.len());
        self.stats.dissolved += step.dissolved as u64;
        if self.fleets[f].live() {
            self.update_fleet_position(f);
        }
        self.stats.cost_ns[4] += t0.elapsed().as_nanos() as u64;
        self.stats.items[4] += 1;
        self.requeue(e);
    }

    /// The member at the front of the hand-outs becomes a ship of the doll: its exact state at the hand-off tick is
    /// bound as a tube (the fit's remainder carried), and its first interval is planned. A refusal (a state no tube
    /// can hold) loses the member, counted. An item like any other of the queue, key `(hand-off tick, the id it
    /// will have)`: it reads the planets and the moon up to its tick (pulled first) and writes only the new body, so
    /// when it is made changes no outcome; whoever reads the doll at a later tick (the player's check) makes the
    /// members handed out before it first.
    fn resolve_handout(&mut self) {
        let Some((f, l)) = self.handouts.pop_front() else { return };
        let key = (l.tick + 1, 0);
        let planets = std::mem::take(&mut self.lanes.planets);
        self.pull(&planets, key);
        self.lanes.planets = planets;
        let moons = std::mem::take(&mut self.lanes.moons);
        self.pull(&moons, key);
        self.lanes.moons = moons;
        let doll = self.fleets[f].doll;
        let made = (|| -> Res<usize> {
            let clock_exp = self.dolls[doll as usize].clock_exp();
            let bound = bind(l.state, l.tick, clock_exp, crate::step::passage_edge(&self.ctx(), doll), self.dolls[doll as usize].unit)?;
            let key = self.cat.insert(bound.entry.clone())?;
            let mut tube = bound.tube;
            tube.key = key;
            let b = Binding { doll, tube, entry: bound.entry, residual: bound.residual, turn: bound.turn, units: bound.units, clock_exp, event_time: l.tick, kick: crate::bind::Kick::NONE };
            let rec = BodyRec {
                kind: Kind::Ship,
                b,
                carry: [0; 2],
                proper: Scalar::ZERO,
                step: 0,
                interval: 0,
                anchor: l.tick,
                plan: Vec::new(),
                thrust: None,
                ext: None,
                alive: true,
                events: 0,
                refusals: 0,
                fault: None,
            };
            let radius = Scalar::raw(l.radius as i128, -20 + self.dolls[doll as usize].shift as i32)?;
            let i = self.bodies.push(rec);
            self.info.push(BodyInfo { kind: Kind::Ship, gm: Scalar::ZERO, soi: Scalar::ZERO, doll: None, radius, from: Some((f as u16, l.member as u16)), born: l.tick });
            self.pos.push([0.0; 2]);
            self.lanes.ships.push(i);
            Ok(i)
        })();
        match made {
            Ok(i) => {
                let upd = step::replan(&self.ctx(), i, self.bodies.rec(i), l.tick);
                self.apply(i, upd);
                self.requeue(i);
                self.stats.leavers += 1;
            }
            Err(_) => {
                self.stats.lost += 1;
                self.resolved += 1;
            }
        }
        // The next member in line has the next id.
        self.requeue(self.bodies.len());
    }

    fn update_fleet_position(&mut self, f: usize) {
        let t = self.fleets[f].tick();
        let centre = self.fleets[f].centre;
        if let (Ok((cp, _)), Some((o, _))) = (crate::observe::root_state_raw(&self.ctx(), centre, t.max(self.bodies.event_time(centre))), self.fleets[f].origin(t)) {
            let k = 2f64.powi(-20);
            self.fleets[f].pos = [cp[0] + o[0] * k, cp[1] + o[1] * k];
        }
    }

    /// Independent ships whose next items are due: resolve them together. Ships read the planets and
    /// the moon and write only themselves, so once those are resolved up to the latest key of the wave
    /// the ships' items are pure functions of their own records, and any number of threads gives the
    /// same bits; the updates are applied in key order.
    fn resolve_wave(&mut self, first: usize, target: Tick) {
        let t0 = Instant::now();
        let cap = self.threads * 4;
        let mut wave = vec![first];
        let _ = self.queue.as_mut().map(|q| q.set(first, None));
        while wave.len() < cap {
            let Some((_, e)) = self.queue.as_ref().and_then(|q| q.peek()) else { break };
            let ok = self.info.get(e).is_some_and(|i| i.kind == Kind::Ship) && self.key_of(e).is_some_and(|k| k.0 <= target);
            if !ok {
                break;
            }
            let _ = self.queue.as_mut().map(|q| q.set(e, None));
            wave.push(e);
        }
        let mut keyed: Vec<((Tick, usize), usize)> = wave.iter().filter_map(|&e| self.key_of(e).map(|k| (k, e))).collect();
        keyed.sort();
        let max = keyed.last().map(|k| k.0).unwrap_or((0, 0));
        let planets = std::mem::take(&mut self.lanes.planets);
        self.pull(&planets, max);
        self.lanes.planets = planets;
        let moons = std::mem::take(&mut self.lanes.moons);
        self.pull(&moons, max);
        self.lanes.moons = moons;
        let recs: Vec<(usize, BodyRec)> = keyed.iter().map(|&(_, e)| (e, self.bodies.rec(e))).collect();
        let threads = self.threads.min(recs.len()).max(1);
        let updates: Vec<(usize, Update)> = {
            let ctx = self.ctx();
            let per = recs.len().div_ceil(threads);
            let mut chunks: Vec<Vec<(usize, BodyRec)>> = Vec::new();
            let mut it = recs.into_iter().peekable();
            while it.peek().is_some() {
                chunks.push(it.by_ref().take(per).collect());
            }
            std::thread::scope(|sc| {
                let handles: Vec<_> = chunks
                    .into_iter()
                    .map(|chunk| {
                        let ctx = &ctx;
                        sc.spawn(move || chunk.into_iter().map(|(i, rec)| (i, step::process(ctx, i, rec))).collect::<Vec<_>>())
                    })
                    .collect();
                handles.into_iter().flat_map(|h| h.join().expect("a ship's item")).collect()
            })
        };
        self.stats.items[2] += updates.len() as u64;
        for (e, upd) in updates {
            self.apply(e, upd);
            self.requeue(e);
        }
        self.stats.cost_ns[2] += t0.elapsed().as_nanos() as u64;
    }

    /// Spend `budget` resolving items with a tick up to `target`, in causal-deadline order.
    pub fn advance(&mut self, target: Tick, budget: Budget) -> Advanced {
        self.target = target;
        self.rekey();
        let start = self.resolved;
        let mut done = 0u64;
        let mut deferred: Vec<usize> = Vec::new();
        let mut overflow = false;
        loop {
            self.take_due(target);
            let Some((dl, e)) = self.queue.as_ref().and_then(|q| q.peek()) else { break };
            let dl = dl.fixed(0).unwrap_or(i128::MAX) as Tick;
            let Some((t, _)) = self.key_of(e) else {
                let _ = self.queue.as_mut().map(|q| q.set(e, None));
                continue;
            };
            if t > target {
                // Beyond this frame: set aside until the frame is done.
                let _ = self.queue.as_mut().map(|q| q.set(e, None));
                deferred.push(e);
                continue;
            }
            if budget.spent(done) {
                overflow = dl <= target;
                break;
            }
            if self.threads > 1 && self.info.get(e).is_some_and(|i| i.kind == Kind::Ship) {
                self.resolve_wave(e, target);
            } else {
                self.resolve_entity(e);
            }
            done = self.resolved - start;
        }
        // The horizon: the smallest deadline still unresolved (the heap's min, and what was set aside).
        let mut horizon = target;
        if let Some((dl, _)) = self.queue.as_ref().and_then(|q| q.peek()) {
            horizon = horizon.min(dl.fixed(0).unwrap_or(i128::MAX) as Tick - 1);
        }
        for e in deferred {
            if let Some(d) = self.deadline_of(e) {
                horizon = horizon.min(d - 1);
            }
            self.requeue(e);
        }
        Advanced { events: done, horizon: horizon.max(self.now), overflow }
    }

    /// Resolve every item up to `horizon` (the canonical cut): the state a digest is taken at.
    pub fn settle(&mut self, horizon: Tick) {
        loop {
            let a = self.advance(horizon, Budget::unlimited());
            if a.events == 0 {
                break;
            }
        }
        self.now = self.now.max(horizon);
    }

    /// One presented frame: advance toward `rtf` game seconds per wall second over `wall_dt` seconds,
    /// spending `budget`; the presented time is the horizon (every item whose light could reach the
    /// player by it is resolved), so an overflow shows only as a lower real-time factor.
    pub fn frame(&mut self, wall_dt: f64, rtf: f64, budget: Budget) -> Frame {
        self.frame_to(wall_dt, rtf, budget, Tick::MAX)
    }

    /// [`Universe::frame`] that never advances the target past `limit`: a canonical cut (a digest taken after
    /// [`Universe::settle`]`(limit)` is the same whatever the frames were). Nothing is resolved past `limit`.
    ///
    /// No decision is taken here: the keys' changes are decisions at the ticks written in the log
    /// ([`Universe::schedule`], [`Universe::input`]), and a key held is *not* a decision per frame (that
    /// would bind the history to the wall's frames). The burn and the turn owed since the last decision or
    /// kick are what the view derives ([`crate::observe::held_thrust`]), and the player's own kicks, at the
    /// thrust's canonical step, flush them into the state.
    pub fn frame_to(&mut self, wall_dt: f64, rtf: f64, budget: Budget, limit: Tick) -> Frame {
        let want = (rtf * wall_dt / crate::view::TICK_SECONDS) as Tick;
        let target = self.now.saturating_add(want.max(1)).min(limit.max(self.now));
        let a = self.advance(target, budget);
        let before = self.now;
        self.now = a.horizon.max(self.now);
        // Histories older than every light cone the view can need are forgotten.
        self.frames += 1;
        if self.frames % 64 == 0 {
            self.prune();
        }
        Frame { target, presented: self.now, ticks: self.now - before, events: a.events, overflow: a.overflow }
    }

    // ---- decisions ------------------------------------------------------------------------------

    /// The player's decision word (bits 0–3 the keys: forward, reverse, left, right; bits 4–7 the throttle level, a
    /// power of two of the base thrust: [`crate::thrust::word`]) changes at tick `t`: a decision, taken
    /// **at that tick** whenever the engine gets there (docs/law.md, "Ties": a decision takes effect at its
    /// logged canonical tick, never at a wall-derived one). The decision waits until the player's own
    /// items up to `t` are resolved (the frame's presented time cannot pass them), so a budget that
    /// bites delays it without moving or dropping it. Decisions are written in order: `t` is not before
    /// the last one, nor before the player's committed tick.
    pub fn schedule(&mut self, t: Tick, keys: u8) -> Res<()> {
        let p = self.player.ok_or(Error::Refused("no player"))?;
        if t < self.last_decision || t < self.now.min(self.bodies.event_time(p)) {
            return Err(Error::Refused("input in the past"));
        }
        self.last_decision = t;
        self.pending.push_back((t, keys));
        Ok(())
    }

    /// Take every scheduled decision whose tick is within `target` and whose past is resolved: the player's next
    /// item is after it. (An item at the decision's own tick is resolved first.)
    fn take_due(&mut self, target: Tick) {
        let Some(p) = self.player else { return };
        while let Some(&(t, keys)) = self.pending.front() {
            if t > target || self.key_of(p).is_some_and(|k| k.0 <= t) {
                break;
            }
            self.pending.pop_front();
            self.take(p, t, keys);
        }
    }

    fn take(&mut self, p: usize, t: Tick, keys: u8) {
        let rec = self.bodies.rec(p);
        let upd = step::decide(&self.ctx(), p, rec, t, keys);
        self.apply(p, upd);
        self.stats.decisions += 1;
        self.inputs.push((t, keys));
        self.requeue(p);
    }

    /// The player's keys change at tick `t`, which must be `now` or later and not before the player's committed
    /// tick, taken now: the scheduled decisions before it are taken first, then the player's own past is
    /// resolved (and what it reads, by pulling). The change is a decision event, logged at `t`.
    pub fn input(&mut self, t: Tick, keys: u8) -> Res<()> {
        let p = self.player.ok_or(Error::Refused("no player"))?;
        if t < self.last_decision || t < self.now.min(self.bodies.event_time(p)) {
            return Err(Error::Refused("input in the past"));
        }
        while let Some(&(pt, pk)) = self.pending.front().filter(|d| d.0 <= t) {
            while self.key_of(p).is_some_and(|k| k.0 <= pt) {
                self.resolve_body(p);
            }
            self.pending.pop_front();
            self.take(p, pt, pk);
        }
        while self.key_of(p).is_some_and(|k| k.0 <= t) {
            self.resolve_body(p);
        }
        self.last_decision = t;
        self.take(p, t, keys);
        Ok(())
    }

    fn encounters_for_player(&mut self) {
        let Some(p) = self.player else { return };
        let t = self.bodies.event_time(p);
        let interval = self.bodies.rec(p).step.max(2);
        for e in self.encounters.find(&self.ctx(), p, t, interval) {
            self.stats.encounters += 1;
            self.contacts += e.contact as u64;
            let mut h = blake3::Hasher::new();
            h.update(&self.enc_digest);
            for v in [e.a as i128, e.b as i128, e.t as i128, e.contact as i128] {
                h.update(&v.to_le_bytes());
            }
            self.enc_digest = *h.finalize().as_bytes();
            if self.enc_log.len() < 4096 {
                self.enc_log.push(e);
            }
        }
    }

    // ---- observation ----------------------------------------------------------------------------

    pub fn rec(&self, i: usize) -> BodyRec {
        self.bodies.rec(i)
    }

    /// Forget history the view can no longer need: older than twice the body's light distance (plus a
    /// margin) behind the present, and older than the oldest item any body still has to resolve.
    pub fn prune(&mut self) {
        let oldest = (0..self.bodies.len()).filter_map(|i| self.bodies.next_time(i)).min().unwrap_or(self.now).min(self.now);
        for i in 0..self.bodies.len() {
            let keep = 2 * self.light_distance(i) + (1 << 26);
            self.bodies.prune(i, (self.now - keep).min(oldest - (1 << 26)));
        }
    }

    /// Bytes per body (arrays, compiled trajectory share, history), averaged.
    pub fn bytes_per_body(&self) -> usize {
        let n = self.bodies.len().max(1);
        (0..self.bodies.len()).map(|i| self.bodies.bytes_of(i)).sum::<usize>() / n
    }

    // ---- the digest -----------------------------------------------------------------------------

    /// One digest of the whole universe: the dolls, every body's exact record, the fleets' battles and
    /// the player's decisions. Taken after [`Universe::settle`]; independent of schedule, budget,
    /// threads and observation.
    pub fn digest(&self) -> String {
        let mut h = blake3::Hasher::new();
        h.update(b"es-universe-plane-v0");
        let put = |h: &mut blake3::Hasher, v: i128| {
            h.update(&v.to_le_bytes());
        };
        let put_s = |h: &mut blake3::Hasher, s: Scalar| {
            h.update(&(s.significand() as i128).to_le_bytes());
            h.update(&(s.exponent() as i128).to_le_bytes());
        };
        for d in &self.dolls {
            put(&mut h, d.mass_log2 as i128);
            put_s(&mut h, d.unit.mu);
            put(&mut h, d.parent.map_or(-1, |p| p as i128));
            put_s(&mut h, d.edge);
            put_s(&mut h, d.surface);
        }
        for i in 0..self.bodies.len() {
            let r = self.bodies.rec(i);
            put(&mut h, r.kind as i128);
            put(&mut h, r.alive as i128);
            put(&mut h, r.b.doll as i128);
            put(&mut h, r.b.event_time as i128);
            put(&mut h, r.b.tube.periapsis_angle as i128);
            put(&mut h, r.b.tube.periapsis_time.get() as i64 as i128);
            let key = r.b.entry.trajectory.key();
            put_s(&mut h, key.periapsis);
            put(&mut h, key.k as i128);
            put(&mut h, r.b.entry.clockwise as i128);
            put(&mut h, r.b.turn.a as i128);
            put(&mut h, r.b.turn.b as i128);
            for c in 0..2 {
                put(&mut h, r.b.residual.position[c]);
                put(&mut h, r.b.residual.velocity[c]);
                put(&mut h, r.carry[c] as i128);
            }
            put(&mut h, r.b.units.0 as i128);
            put(&mut h, r.b.units.1 as i128);
            put_s(&mut h, r.proper);
            if let Some(e) = r.ext {
                // the extended state of the motion law v2: the register, its carries and the clock's constants
                for v in [e.pt, e.pt_exp as i128, e.pt_carry as i128, e.dt_carry as i128] {
                    put(&mut h, v);
                }
                for c in [e.ds, e.c, e.b] {
                    put_s(&mut h, c);
                }
            }
            put(&mut h, r.step as i128);
            put(&mut h, r.interval as i128);
            put(&mut h, r.anchor as i128);
            for it in &r.plan {
                put(&mut h, it.t as i128);
                put(&mut h, match it.what {
                    What::Kick(l) => 100 + l as i128,
                    What::Open(l) => 200 + l as i128,
                    What::Crash => 250,
                    What::Boundary => 300,
                });
            }
            if let Some(t) = r.thrust {
                put(&mut h, t.keys as i128);
                if t.level != 0 {
                    put(&mut h, 1000 + t.level as i128);
                }
                put(&mut h, t.heading as i128);
                put(&mut h, t.since as i128);
            }
            put(&mut h, r.events as i128);
            put(&mut h, r.refusals as i128);
            h.update(format!("{:?}", r.fault).as_bytes());
        }
        for f in &self.fleets {
            f.digest_into(&mut h);
        }
        for (t, k) in &self.inputs {
            put(&mut h, *t as i128);
            put(&mut h, *k as i128);
        }
        // Members handed out and not made yet (none at a canonical cut: every hand-out is at or before it).
        if !self.handouts.is_empty() {
            put(&mut h, self.handouts.len() as i128);
        }
        h.update(&self.enc_digest);
        h.finalize().to_hex().to_string()
    }

    /// The canonical time at which a body's next item is, for tests.
    pub fn horizon_of(&self, i: usize) -> Option<Tick> {
        self.key_of(i).map(|k| k.0)
    }
}

