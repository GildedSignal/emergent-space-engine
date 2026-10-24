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
use crate::bind::{bind_surface, bind_exact, Binding, Catalogue, Entry};
use crate::body::{BodyRec, BodyStore, Kind, PlainBodies, Segment, Thrust, What};
use crate::ctx::{BodyInfo, Config, Ctx};
use crate::encounter::{Encounter, Encounters, Held, PlayerNeighbourhood};
use crate::fleet::{Fleet, Leaver};
use crate::num::{Error, Res, Tick};
use crate::step::{self, Resolved, Update};
use crate::world::{DollRec, Mass, Unit};
use crate::calendar::{heap_bytes, Prunable, Queue, Ticks, Wheel};
use emergent_space::{
    binding::Trajectory,
    orbit::{Orbit, OrbitKey, Scalar},
    Tube,
};
use std::cmp::Reverse;
use std::collections::VecDeque;
use std::sync::Arc;
use std::time::Instant;

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
    /// Spent, or the wall left is less than `margin_ns` (what the next item may cost).
    fn spent_before(&self, done: u64, margin_ns: u64) -> bool {
        done >= self.events || self.until.is_some_and(|u| Instant::now() + std::time::Duration::from_nanos(margin_ns) >= u)
    }
}

/// Idle time is spent on a scan only if at least twice the longest recent one (and this, ns) is left: a scan costs 30 us to
/// 1.5 ms (the finder reads each of up to a hundred bodies, a passage in tens of microseconds), and the frame must not overrun.
const SCAN_MARGIN_NS: u64 = 750_000;

/// The scans held for idle time (about 10 KB each: the bindings they read) are answered, inside the frame's budget, before the
/// frame resolves anything else once this many are waiting, the oldest first, so the memory they hold is bounded.
const SCAN_BACKLOG: usize = 2048;

/// What a frame does after its last item (the horizon, what was set aside, the check for idle time), ns: kept free of items.
const FRAME_TAIL_NS: u64 = 50_000;

/// The encounter hash chain's next link.
fn chain(prev: [u8; 32], e: &Encounter) -> [u8; 32] {
    let mut h = blake3::Hasher::new();
    h.update(&prev);
    for v in [e.a as i128, e.b as i128, e.t as i128, e.contact as i128] {
        h.update(&v.to_le_bytes());
    }
    *h.finalize().as_bytes()
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

/// A measurement of how far the ships' items stay on their own grid (next = last + its step): off unless
/// [`Universe::watch_grid`] turns it on. A ship's item is **off its grid** when the step it plans differs from the step it had
/// (the next item is not where the previous step put it); a body's first item (a root ship's stub) is not counted.
#[derive(Clone, Debug)]
pub struct GridWatch {
    /// Items of ships watched at which the step is chosen (a root ship's kick on its own clock; the boundary of a ship of a
    /// planet's doll on the split), by clock (0 and 1).
    pub items: [u64; 2],
    /// Of them, those after which the step changed.
    pub off: [u64; 2],
    /// `|ΔS|/S` of the off items: bucket `k` counts `2^-(k+1) < r ≤ 2^-k` (63: smaller).
    pub rel_log2: [u64; 64],
    /// `|ΔS|` of the off items in ticks: bucket `k` counts `2^k ≤ |ΔS| < 2^(k+1)`.
    pub abs_log2: [u64; 64],
    /// Bodies with at least one off item, and bodies with at least one item, while watched (bitsets).
    off_bodies: Vec<u64>,
    seen: Vec<u64>,
    /// A root ship's own grid, fixed at its first watched kick: (that kick's tick, the step it planned).
    first: Vec<(i64, i64)>,
    /// How far a root ship's kick is from that grid (`|t − (t0 + n·S0)|`, ticks): bucket `k` counts `2^k ≤ d < 2^(k+1)`; 0 counts `d ≤ 1`.
    pub drift_log2: [u64; 64],
}

impl Default for GridWatch {
    fn default() -> Self {
        Self { items: [0; 2], off: [0; 2], rel_log2: [0; 64], abs_log2: [0; 64], off_bodies: Vec::new(), seen: Vec::new(), first: Vec::new(), drift_log2: [0; 64] }
    }
}

impl GridWatch {
    fn mark(set: &mut Vec<u64>, i: usize) {
        if set.len() <= i / 64 {
            set.resize(i / 64 + 1, 0);
        }
        set[i / 64] |= 1 << (i % 64);
    }
    /// Bodies with at least one off item while watched (the hot set over the window).
    pub fn off_bodies(&self) -> usize {
        self.off_bodies.iter().map(|w| w.count_ones() as usize).sum()
    }
    /// Bodies with at least one item while watched.
    pub fn seen_bodies(&self) -> usize {
        self.seen.iter().map(|w| w.count_ones() as usize).sum()
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
    /// What a frame may resolve, by deadline ([`crate::calendar::Queue`]): the planets, the moons, the player, the fleets, the next
    /// hand-out, and the ships the target reaches. None until the universe starts.
    queue: Option<Queue>,
    /// The ships' calendar ([`crate::calendar::Wheel`]): every ship whose next tick is after what it has handed out
    /// (`wheel.drained()`), filed by the class its own next tick puts it in. [`Universe::rekey`] hands out the ones the target reaches.
    wheel: Wheel,
    /// The ships the calendar handed out and not resolved yet, by `(tick, id)`: those of the root doll (0) and those of a planet's
    /// doll (1). The minimum is the ship the player's scan must wait for ([`Universe::pull_ships`]). Lazy: an entry holds while the
    /// ship's next tick is its tick.
    due: [Ticks; 2],
    /// Of them, those whose tick is after the target (the player's own pull can hand out past it): queued when the target reaches them.
    parked: Ticks,
    /// What the calendar handed out last (reused).
    out: Vec<usize>,
    /// How far the observer has moved since the start (root units, rounded up at each frame): the queue's keys are a deadline plus the
    /// `moved` of when it was computed, so `key - moved` is never later than the deadline the present observer gives (a light distance
    /// changes by at most the observer's displacement), and an entry need not be re-keyed when the observer moves.
    moved: Tick,
    observed: bool,
    /// Where each doll's bodies can be, by radius ([`crate::radial`]): kept by [`Universe::apply`] and [`Universe::prune`].
    radial: crate::radial::Radial,
    /// The bodies whose history holds more than one retired binding (the only ones [`Universe::prune`] can shorten), keyed by the
    /// earliest tick it could: the end of the oldest one plus what is kept behind the present (twice the light distance, and a margin).
    prunable: Prunable,
    /// The presented time of the last frame, and the position of the player used for deadlines.
    pub now: Tick,
    player: Option<usize>,
    observer: [f64; 2],
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
    /// Scans the player's items took and the allocator has not answered yet, in the order taken
    /// ([`Universe::drain_scans`]); the log, the count and the hash below are as if each had been answered at once once
    /// this is empty, and [`Universe::digest`] answers what is held.
    scans: VecDeque<Arc<dyn Held>>,
    /// The longest a scan took to answer recently, in ns: idle time is spent on one only when it fits.
    scan_ns: u64,
    /// The longest recent item of each class (a planet, a moon, a ship, the player; a fleet or a hand-out), ns: a running maximum that
    /// forgets (1/64 an item of the class). A frame with a wall to keep starts an item only if that much is left, once it has resolved one.
    item_ns: [u64; 5],
    pub enc_log: Vec<Encounter>,
    enc_digest: [u8; 32],
    pub contacts: u64,
    /// Every item resolved (a refusal or a loss counts: it was work).
    resolved: u64,
    frames: u64,
    /// Entity ids below this are bodies (those made, and the room for every member a fleet can hand out);
    /// a fleet's entity id is `body_cap + its index`.
    body_cap: usize,
    /// The hot-set measurement ([`GridWatch`]), when on.
    grid: Option<Box<GridWatch>>,
}

#[derive(Default)]
struct Lanes {
    planets: Vec<usize>,
    moons: Vec<usize>,
}

/// The heading a player's nose starts at: along its velocity at tick 0 in its doll's axes (prograde, so that "forward" burns
/// the orbit up and not down into the planet).
fn prograde(b: &Binding) -> Res<u32> {
    crate::thrust::heading_of(b.cartesian(0)?.1)
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
            wheel: Wheel::new(0, 0, 0, 0),
            due: Default::default(),
            parked: Ticks::new(),
            out: Vec::new(),
            moved: 0,
            observed: false,
            radial: crate::radial::Radial::default(),
            prunable: Prunable::default(),
            now: 0,
            player: None,
            observer: [0.0; 2],
            stats: Stats::default(),
            inputs: Vec::new(),
            handouts: VecDeque::new(),
            pending: VecDeque::new(),
            last_decision: 0,
            threads: 1,
            slice: 1 << 18,
            lanes: Lanes::default(),
            target: 0,
            encounters: Box::<PlayerNeighbourhood>::default(),
            scans: VecDeque::new(),
            scan_ns: 0,
            item_ns: [0; 5],
            enc_log: Vec::new(),
            enc_digest: [0; 32],
            contacts: 0,
            resolved: 0,
            frames: 0,
            body_cap: 0,
            grid: None,
        }
    }

    /// Start (or restart) measuring the ships' items against their own grid ([`GridWatch`]).
    pub fn watch_grid(&mut self) {
        self.grid = Some(Box::default());
    }
    pub fn grid_watch(&self) -> Option<&GridWatch> {
        self.grid.as_deref()
    }

    /// Bytes the schedule holds, by allocation: the calendar (a link a ship, the classes' cursors, the front), the hot set's heaps
    /// (the due ships, the parked ones, the deadline queue, the bodies whose history can be shortened) and one bit a body.
    pub fn schedule_bytes(&self) -> usize {
        self.wheel.bytes()
            + self.due.iter().map(heap_bytes).sum::<usize>()
            + heap_bytes(&self.parked)
            + self.out.capacity() * std::mem::size_of::<usize>()
            + self.queue.as_ref().map_or(0, Queue::bytes)
            + self.prunable.bytes()
    }

    /// The hot set now: ships handed out and not resolved, in the calendar's front, and entities queued.
    pub fn hot(&self) -> (usize, usize, usize) {
        (self.due.iter().map(|h| h.len()).sum(), self.wheel.front_len(), self.queue.as_ref().map_or(0, Queue::len))
    }


    pub fn ctx(&self) -> Ctx<'_> {
        Ctx { dolls: &self.dolls, bodies: &*self.bodies, info: &self.info, sources: &self.sources, cfg: &self.cfg, radial: &self.radial }
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
    /// Scans the player's items took that idle time has not answered yet ([`Universe::digest`] counts them as answered).
    pub fn held_scans(&self) -> usize {
        self.scans.len()
    }
    /// The bindings the held scans keep (a scan reused by the next one is counted once), and their bytes.
    pub fn held_scan_bindings(&self) -> (usize, usize) {
        let mut seen: Vec<*const ()> = Vec::new();
        let mut n = 0;
        for s in &self.scans {
            let p = Arc::as_ptr(s) as *const ();
            if !seen.contains(&p) {
                seen.push(p);
                n += s.held();
            }
        }
        (n, n * std::mem::size_of::<(usize, Binding, Scalar)>())
    }
    /// Answer every held scan now (what the count, the log and the hash read once nothing is held; `settle` does it too).
    pub fn flush_scans(&mut self) {
        self.drain_scans(None);
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
        let sep = self.bodies.rec(centre).b.to_doll(self.bodies.rec(centre).b.entry.trajectory.key().ok_or(Error::Refused("a doll centre needs a turning orbit"))?.periapsis)?;
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
        let k = key.shape()?;
        let r_max = unit.to_doll(key.periapsis.div(k.scale(1)?.sub(Scalar::ONE)?)?)?; // apoapsis: p/(2k − 1)
        let v_max = Scalar::integer(2).mul(Scalar::ONE.div(key.periapsis)?)?.sqrt()?.scale(1)?;
        Ok((entry, Tube::new(0, spec.angle, peri), crate::bind::choose_units(r_max, v_max)))
    }

    /// Make a body from an orbit: a tube of `spec.doll`, exactly (no remainder to carry).
    pub fn add_body(&mut self, kind: Kind, spec: OrbitSpec, radius: Scalar) -> Res<usize> {
        let (entry, mut tube, units) = self.spec_binding(&spec, self.dolls[spec.doll as usize].unit)?;
        tube.key = self.cat.insert(entry.clone())?;
        let b = bind_exact(entry, tube, self.dolls[spec.doll as usize].clock_exp(), units, 0, spec.doll);
        let heading = prograde(&b)?;
        let rec = BodyRec {
            kind,
            b,
            carry: [0; 2],
            proper: Scalar::ZERO,
            step: 0,
            interval: 0,
            anchor: 0,
            plan: Vec::new(),
            thrust: (kind == Kind::Player).then_some(Thrust { keys: 0, level: 0, heading, since: 0 }),
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
        if x.is_zero() {
            return Err(Error::Refused("a state at the centre has no exterior orbit"));
        }
        let (le, ve) = crate::bind::choose_units(x.scale(2)?, if v.is_zero() { Scalar::ONE } else { v.scale(2)? });
        let word = |a: Scalar, e: i16| -> Res<i64> { i64::try_from(a.fixed(-(e as i32))?).map_err(|_| Error::Refused("state outside the integer word")) };
        let exact = emergent_space::binding::IntegerState {
            position: [word(position[0], le)?, word(position[1], le)?],
            velocity: [word(velocity[0], ve)?, word(velocity[1], ve)?],
            length_exponent: le,
            velocity_exponent: ve,
        };
        let edge = (doll != 0).then(|| d.edge.scale(2)).transpose()?;
        let bound = bind_surface(exact, 0, d.clock_exp(), edge, d.unit, Some(d.surface))?;
        let mut tube = bound.tube;
        tube.key = self.cat.insert(bound.entry.clone())?;
        let b = Binding { doll, tube, entry: bound.entry, residual: bound.residual, turn: bound.turn, units: bound.units, clock_exp: d.clock_exp(), event_time: 0, kick: crate::bind::Kick::NONE, impact: None };
        let heading = prograde(&b)?;
        let rec = BodyRec {
            kind,
            b,
            carry: [0; 2],
            proper: Scalar::ZERO,
            step: 0,
            interval: 0,
            anchor: 0,
            plan: Vec::new(),
            thrust: (kind == Kind::Player).then_some(Thrust { keys: 0, level: 0, heading, since: 0 }),
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
        let unit = Ctx { dolls: &self.dolls, bodies: &*self.bodies, info: &self.info, sources: &self.sources, cfg: &self.cfg, radial: &self.radial }.tube_unit(i, spec.doll)?;
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
        self.drain_scans(None);
        self.encounters = e;
    }

    /// Everything is made: plan every body's first interval and build the queue.
    pub fn start(&mut self) -> Res<()> {
        let n = self.bodies.len();
        self.lanes = Lanes { planets: self.kinds(Kind::Planet), moons: self.kinds(Kind::Moon) };
        self.body_cap = n + self.fleets.iter().map(|f| f.n_members).sum::<usize>();
        let slots = self.body_cap + self.fleets.len();
        self.prunable = Prunable::new(slots);
        for i in 0..n {
            let rec = self.bodies.rec(i);
            let upd = step::replan(&self.ctx(), i, rec, 0);
            self.apply(i, upd);
        }
        // The calendar's classes: a ring of them (one class for every four ships or so, at most 2^16) over the ships' median step, so
        // that a ship's next item is mostly within one lap. A schedule only: no choice here reaches an outcome.
        let mut steps: Vec<i64> = (0..n).filter(|&i| self.info[i].kind == Kind::Ship).map(|i| self.bodies.step(i)).filter(|&s| s > 0).collect();
        let ring_log2 = (usize::BITS - steps.len().max(1).leading_zeros()).saturating_sub(2).clamp(6, 16);
        let span = if steps.is_empty() {
            1 << 24
        } else {
            let m = steps.len() / 2;
            *steps.select_nth_unstable(m).1
        };
        self.wheel = Wheel::new(slots, 0, Wheel::shift_for(span, ring_log2), ring_log2);
        self.queue = Some(Queue::default());
        // Every ship waits in the calendar for the target to reach its tick.
        for i in 0..n {
            if self.info[i].kind == Kind::Ship {
                self.requeue(i);
            }
        }
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
        (Ctx { dolls: &self.dolls, bodies: &*self.bodies, info: &self.info, sources: &self.sources, cfg: &self.cfg, radial: &self.radial }, &mut self.fleets)
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
                _ => self.position(e),
            }
        };
        let (dx, dy) = (p[0] - self.observer[0], p[1] - self.observer[1]);
        (dx * dx + dy * dy).sqrt().min(4e18) as Tick
    }

    /// Where body `i` is in root units at its binding's event, for its deadline (a scheduling heuristic only, never an outcome):
    /// the walk of its doll chain at that tick, or, if a centre's history no longer reaches back to it, where its doll's centre is.
    fn position(&self, i: usize) -> [f64; 2] {
        let t0 = crate::prof::t();
        let p = match crate::observe::root_state_raw(&self.ctx(), i, self.bodies.event_time(i)) {
            Ok((p, _)) => p,
            Err(_) => self.dolls[self.bodies.doll(i) as usize].centre.map_or([0.0; 2], |c| self.position(c)),
        };
        crate::prof::add(crate::prof::ROOT, t0);
        p
    }

    /// The deadline of an entity's next item: when its light reaches the player.
    fn deadline_of(&self, e: usize) -> Option<Tick> {
        self.key_of(e).map(|(t, _)| t.saturating_add(self.light_distance(e)))
    }

    /// Put entity `e` in the queue at its deadline (its key is the deadline plus `moved`: see [`Universe::moved`]). **A ship whose next
    /// item is after the frame's target is not in the queue** but in the calendar ([`crate::calendar::Wheel`]), by its tick: the queue
    /// holds what can be resolved now, in the order of its deadlines (when its light reaches the player), and a ship that nothing is due
    /// for costs nothing a frame. The presentable horizon cannot depend on it: its deadline is its tick plus its distance, after the
    /// target. It enters the queue when the target reaches its tick ([`Universe::rekey`]) or when its own item gives it a tick the
    /// calendar has already handed out.
    fn requeue(&mut self, e: usize) {
        let t0 = crate::prof::t();
        if e < self.bodies.len() && self.info[e].kind == Kind::Ship {
            match self.bodies.next_time(e) {
                Some(t) if t > self.wheel.drained() => {
                    if let Some(q) = self.queue.as_mut() {
                        q.set(e, None);
                    }
                    self.wheel.file(e, t);
                }
                Some(t) => self.hand_out(e, t),
                None => {
                    if let Some(q) = self.queue.as_mut() {
                        q.set(e, None);
                    }
                }
            }
        } else {
            let key = self.deadline_of(e).map(|d| d.saturating_add(self.moved));
            if let Some(q) = self.queue.as_mut() {
                q.set(e, key);
            }
        }
        crate::prof::add(crate::prof::REQUEUE, t0);
    }

    /// Ship `i`, due at `t` (a tick the calendar has handed out): among the due ships, and queued if the target reaches it (parked
    /// until it does if not).
    fn hand_out(&mut self, i: usize, t: Tick) {
        self.due[(self.bodies.doll(i) != 0) as usize].push(Reverse((t, i as u32)));
        let key = if t <= self.target {
            self.deadline_of(i).map(|d| d.saturating_add(self.moved))
        } else {
            self.parked.push(Reverse((t, i as u32)));
            None
        };
        if let Some(q) = self.queue.as_mut() {
            q.set(i, key);
        }
    }

    /// Hand out every ship of the calendar whose tick is at or before `to`.
    fn drain_ships(&mut self, to: Tick) {
        let mut out = std::mem::take(&mut self.out);
        {
            let bodies = &*self.bodies;
            self.wheel.drain(to, |i| bodies.next_time(i), &mut out);
        }
        for &i in &out {
            if let Some(t) = self.bodies.next_time(i) {
                self.hand_out(i, t);
            }
        }
        out.clear();
        self.out = out;
    }

    /// The first current entry among the due ships of the root doll (0) or of a planet's doll (1); stale entries are dropped.
    fn due_top(&mut self, c: usize) -> Option<(Tick, usize)> {
        while let Some(&Reverse((t, i))) = self.due[c].peek() {
            let i = i as usize;
            if self.bodies.next_time(i) == Some(t) && (self.bodies.doll(i) != 0) as usize == c && !self.wheel.holds(i) {
                return Some((t, i));
            }
            self.due[c].pop();
        }
        None
    }

    /// The deadline a queue key stands for: never later than the one the present observer gives.
    fn deadline_of_key(&self, key: Tick) -> Tick {
        key.saturating_sub(self.moved)
    }

    /// Recompute the deadline of the few that are always queued from the player's present position (a scheduling heuristic only): the
    /// planets, the moons, the player, the fleets and the next hand-out; and move the ships the target now reaches into the queue. A ship
    /// already queued keeps its key (it is sound however the observer moved: [`Universe::moved`]): a backlog of due ships costs nothing a
    /// frame (every due ship was re-keyed every frame before: a wave of kicks larger than a frame's budget was re-keyed whole each frame,
    /// and the re-keying alone could eat the budget).
    pub fn rekey(&mut self) {
        let t0 = crate::prof::t();
        if let Some(p) = self.player {
            if let Ok((pos, _)) = crate::observe::root_state_raw(&self.ctx(), p, self.bodies.event_time(p).max(self.now)) {
                if self.observed {
                    let step = (pos[0] - self.observer[0]).hypot(pos[1] - self.observer[1]);
                    self.moved = self.moved.saturating_add(step.ceil().min(4e18) as Tick);
                }
                self.observed = true;
                self.observer = pos;
            }
        }
        for k in 0..self.lanes.planets.len() {
            self.requeue(self.lanes.planets[k]);
        }
        for k in 0..self.lanes.moons.len() {
            self.requeue(self.lanes.moons[k]);
        }
        if let Some(p) = self.player {
            self.requeue(p);
        }
        // The ships the target reaches: handed out by the calendar, and the parked ones.
        self.drain_ships(self.target);
        while let Some(&Reverse((t, i))) = self.parked.peek() {
            if t > self.target {
                break;
            }
            self.parked.pop();
            let i = i as usize;
            if self.bodies.next_time(i) == Some(t) && !self.wheel.holds(i) {
                let key = self.deadline_of(i).map(|d| d.saturating_add(self.moved));
                if let Some(q) = self.queue.as_mut() {
                    q.set(i, key);
                }
            }
        }
        for f in 0..self.fleets.len() {
            self.requeue(self.fleet_entity(f));
        }
        self.requeue(self.bodies.len());
        crate::prof::add(crate::prof::REKEY, t0);
    }

    // ---- resolving ------------------------------------------------------------------------------

    fn apply(&mut self, i: usize, mut upd: Update) {
        let t_apply = crate::prof::t();
        let retired = !upd.retired.is_empty();
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
        self.radial.note(i, self.info[i].kind, crate::num::to_f64(self.info[i].radius), &upd.rec.b);
        // The step is chosen at a root ship's kick and at the boundary of a ship of a planet's doll.
        let chosen = if upd.rec.ext.is_some() { upd.kind == Resolved::Kick } else { upd.kind == Resolved::Boundary };
        if let Some(g) = self.grid.as_deref_mut().filter(|_| self.info[i].kind == Kind::Ship && upd.rec.events > 1 && chosen) {
            let (old, new) = (self.bodies.step(i), upd.rec.step);
            let c = (upd.rec.ext.is_none()) as usize;
            g.items[c] += 1;
            GridWatch::mark(&mut g.seen, i);
            if let (0, Some(t_item)) = (c, self.bodies.next_time(i)) {
                if g.first.len() <= i {
                    g.first.resize(i + 1, (0, 0));
                }
                let (t0, s0) = g.first[i];
                if s0 == 0 {
                    g.first[i] = (t_item, new);
                } else {
                    let n = ((t_item - t0) as f64 / s0 as f64).round() as i64;
                    let d = (t_item - t0 - n * s0).unsigned_abs();
                    g.drift_log2[if d <= 1 { 0 } else { 63 - d.leading_zeros() as usize }] += 1;
                }
            }
            if old != 0 && new != old {
                g.off[c] += 1;
                GridWatch::mark(&mut g.off_bodies, i);
                let d = (new - old).unsigned_abs();
                g.abs_log2[63 - d.leading_zeros() as usize] += 1;
                let r = d as f64 / old.unsigned_abs().max(1) as f64;
                g.rel_log2[((-r.log2()).floor().max(0.0) as usize).min(63)] += 1;
            }
        }
        self.bodies.put(i, upd.rec);
        if retired {
            self.key_prune(i, Tick::MIN);
        }
        crate::prof::add(crate::prof::APPLY, t_apply);
    }

    fn lane(&self, ids: &[usize]) -> Option<(Tick, usize)> {
        ids.iter().filter_map(|&i| self.key_of(i)).min()
    }

    /// Resolve every ship item with a key below `key`, in key order (the calendar hands out every ship up to the key's tick first; the
    /// due ships' minimum is the first entry of their heaps: no walk over the ships); with `children_only`, the items of the ships of
    /// a planet's doll only.
    fn pull_ships(&mut self, key: (Tick, usize), children_only: bool) {
        self.drain_ships(key.0);
        loop {
            let root = if children_only { None } else { self.due_top(0) };
            let first = match (root, self.due_top(1)) {
                (Some(a), Some(b)) => a.min(b),
                (a, b) => match a.or(b) {
                    Some(k) => k,
                    None => break,
                },
            };
            if first >= key {
                break;
            }
            self.resolve_body(first.1);
            self.requeue(first.1);
        }
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
            // ...and the ships with an item before the player's: after the player's own item (below), which reads none of them.
        }
        let rec = self.bodies.rec(i);
        let t_process = crate::prof::t();
        let item = if crate::prof::ENABLED { rec.plan.first().map(|it| (it.what, rec.ext.is_some())) } else { None };
        let upd = step::process(&self.ctx(), i, rec);
        crate::prof::add(crate::prof::PROCESS, t_process);
        if let Some((what, clock)) = item {
            use crate::prof::*;
            let stage = match what {
                What::Kick(_) if clock => P_KICK_CLOCK,
                What::Kick(l) if l > 0 => P_KICK_SUB,
                What::Kick(_) => P_KICK,
                What::Open(_) => P_OPEN,
                What::Crash => P_CRASH,
                What::Boundary => P_BOUNDARY,
            };
            add(stage, t_process);
        }
        self.apply(i, upd);
        if kind == Kind::Player {
            // The scan reads the ships of the player's doll at its tick, so the ships with an item before it are resolved first. A ship of
            // the root doll never leaves it (the motion law v2 has no capture from the root: `step::Work::maybe_capture`), so when the
            // player is in a planet's doll after its item, the root's ships cannot be read by the scan: they are left to the queue, in the
            // order of their deadlines and inside the frame's budget (the player's item pulled every due ship of every doll before, a burst
            // the size of the root's whole wave of kicks, inside one item and outside the budget). Ships read only the sources, and the
            // player reads no ship: resolving the player's item before theirs changes no bit.
            let in_root = self.bodies.doll(i) == 0;
            self.pull_ships(key, !in_root);
            let t_enc = crate::prof::t();
            self.encounters_for_player();
            crate::prof::add(crate::prof::ENCOUNTERS, t_enc);
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
                    q.set(e, None);
                    q.peek()
                });
                let cap = second.map_or(Tick::MAX, |(d, _)| self.deadline_of_key(d).saturating_sub(dist));
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
        let t_adv = crate::prof::t();
        let step = {
            let (ctx, fleets) = self.split();
            fleets[f].advance(&ctx, slice, limit)
        };
        crate::prof::add(crate::prof::F_ADV, t_adv);
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
        let t_ho = crate::prof::t();
        let Some((f, l)) = self.handouts.pop_front() else { return };
        let key = (l.tick + 1, 0);
        let t_pull = crate::prof::t();
        let planets = std::mem::take(&mut self.lanes.planets);
        self.pull(&planets, key);
        self.lanes.planets = planets;
        let moons = std::mem::take(&mut self.lanes.moons);
        self.pull(&moons, key);
        self.lanes.moons = moons;
        crate::prof::add(crate::prof::H_PULL, t_pull);
        let doll = self.fleets[f].doll;
        let made = (|| -> Res<usize> {
            let clock_exp = self.dolls[doll as usize].clock_exp();
            let t_bind = crate::prof::t();
            let bound = bind_surface(l.state, l.tick, clock_exp, crate::step::passage_edge(&self.ctx(), doll), self.dolls[doll as usize].unit, Some(self.dolls[doll as usize].surface))?;
            crate::prof::add(crate::prof::H_BIND, t_bind);
            let key = self.cat.insert(bound.entry.clone())?;
            let mut tube = bound.tube;
            tube.key = key;
            let b = Binding { doll, tube, entry: bound.entry, residual: bound.residual, turn: bound.turn, units: bound.units, clock_exp, event_time: l.tick, kick: crate::bind::Kick::NONE, impact: None };
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
            Ok(i)
        })();
        match made {
            Ok(i) => {
                let t_replan = crate::prof::t();
                let upd = step::replan(&self.ctx(), i, self.bodies.rec(i), l.tick);
                crate::prof::add(crate::prof::H_REPLAN, t_replan);
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
        crate::prof::add(crate::prof::HANDOUT, t_ho);
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
        if let Some(q) = self.queue.as_mut() {
            q.set(first, None);
        }
        while wave.len() < cap {
            let Some((_, e)) = self.queue.as_mut().and_then(|q| q.peek()) else { break };
            let ok = self.info.get(e).is_some_and(|i| i.kind == Kind::Ship) && self.key_of(e).is_some_and(|k| k.0 <= target);
            if !ok {
                break;
            }
            if let Some(q) = self.queue.as_mut() {
                q.set(e, None);
            }
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
            let t_due = crate::prof::t();
            self.take_due(target);
            crate::prof::add(crate::prof::TAKE_DUE, t_due);
            let Some((dl, e)) = self.queue.as_mut().and_then(|q| q.peek()) else { break };
            let dl = self.deadline_of_key(dl);
            let Some((t, _)) = self.key_of(e) else {
                if let Some(q) = self.queue.as_mut() {
                    q.set(e, None);
                }
                continue;
            };
            if t > target {
                // Beyond this frame: set aside until the frame is done.
                if let Some(q) = self.queue.as_mut() {
                    q.set(e, None);
                }
                deferred.push(e);
                continue;
            }
            // The next item is started only if what such an item has cost lately is left (a frame overran by the one item it started
            // with a few microseconds to spare: up to 1.4 ms through the root's wave of kicks); the first item of a frame always runs.
            let class = if e < self.bodies.len() { self.info[e].kind as usize } else { 4 };
            if budget.spent_before(done, if done == 0 { 0 } else { self.item_ns[class] + FRAME_TAIL_NS }) {
                overflow = dl <= target;
                break;
            }
            // Held scans are work like any other once they pile up (the memory they hold is bounded): at the backlog's cap
            // the player's next item waits for the oldest scan, inside the budget, so a frame stays within it and the
            // presented time lags (as it did before scans were held), instead of the frame overrunning.
            if self.scans.len() >= SCAN_BACKLOG {
                self.answer_front();
                continue;
            }
            let t_item = Instant::now();
            if self.threads > 1 && self.info.get(e).is_some_and(|i| i.kind == Kind::Ship) {
                self.resolve_wave(e, target);
            } else {
                self.resolve_entity(e);
            }
            let ns = t_item.elapsed().as_nanos() as u64;
            let m = &mut self.item_ns[class];
            *m = if ns >= *m { ns } else { *m - *m / 64 };
            done = self.resolved - start;
        }
        // The horizon: the smallest deadline still unresolved (the heap's min, and what was set aside).
        let mut horizon = target;
        if let Some((dl, _)) = self.queue.as_mut().and_then(|q| q.peek()) {
            horizon = horizon.min(self.deadline_of_key(dl) - 1);
        }
        for e in deferred {
            if let Some(d) = self.deadline_of(e) {
                horizon = horizon.min(d - 1);
            }
            self.requeue(e);
        }
        // Idle time: what the frame's budget has left goes to the scans the player's items held (all of them when there
        // is no wall to keep).
        self.drain_scans(budget.until);
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
        // Histories older than every light cone the view can need are forgotten, every frame and inside its budget (before the
        // items): a call visits only the bodies that can be shortened now (it ran every 64th frame, after the items, and that frame
        // paid for 64 frames' worth).
        let t_prune = crate::prof::t();
        self.prune();
        crate::prof::add(crate::prof::PRUNE, t_prune);
        let a = self.advance(target, budget);
        let before = self.now;
        self.now = a.horizon.max(self.now);
        self.frames += 1;
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
        let t_decide = crate::prof::t();
        let upd = step::decide(&self.ctx(), p, rec, t, keys);
        crate::prof::add(crate::prof::P_DECIDE, t_decide);
        self.apply(p, upd);
        self.stats.decisions += 1;
        self.inputs.push((t, keys));
        self.requeue(p);
    }

    /// The player's keys change at tick `t` (`now` or later), taken now: the scheduled decisions before it are taken
    /// first, then the player's own past is resolved (and what it reads, by pulling). The change is a decision event,
    /// logged at the tick it takes effect: `t`, or the player's committed tick when a frame has resolved the player past
    /// `t` (a kick at now + 1), or a replay, which takes it at its logged tick, would take it earlier than the flight did.
    pub fn input(&mut self, t: Tick, keys: u8) -> Res<()> {
        let p = self.player.ok_or(Error::Refused("no player"))?;
        if t < self.last_decision || t < self.now.min(self.bodies.event_time(p)) {
            return Err(Error::Refused("input in the past"));
        }
        let t = t.max(self.bodies.event_time(p));
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
        match self.encounters.capture(&self.ctx(), p, t, interval) {
            // The answer is not on the frame's critical path (nothing the view shows reads it): hold the scan.
            Some(held) => self.scans.push_back(held),
            None => {
                for e in self.encounters.find(&self.ctx(), p, t, interval) {
                    self.log_encounter(e);
                }
            }
        }
    }

    /// One encounter into the count, the hash chain and the log.
    fn log_encounter(&mut self, e: Encounter) {
        self.stats.encounters += 1;
        self.contacts += e.contact as u64;
        self.enc_digest = chain(self.enc_digest, &e);
        if self.enc_log.len() < 4096 {
            self.enc_log.push(e);
        }
    }

    /// Answer the held scans, oldest first, while `until` allows (all of them if `None`): scans are idle-time work as far
    /// as the frame's budget goes, and they keep their order.
    fn drain_scans(&mut self, until: Option<Instant>) {
        while !self.scans.is_empty() {
            if let Some(u) = until {
                let room = u.checked_duration_since(Instant::now()).map_or(0, |d| d.as_nanos() as u64);
                if room < 2 * self.scan_ns.max(SCAN_MARGIN_NS) {
                    break;
                }
            }
            self.answer_front();
        }
    }

    /// Answer the oldest held scan: into the count, the log and the hash.
    fn answer_front(&mut self) {
        let (t0, t_scan) = (Instant::now(), crate::prof::t());
        let found = self.scans.front().map(|held| held.answer()).unwrap_or_default();
        let ns = t0.elapsed().as_nanos() as u64;
        crate::prof::add(crate::prof::SCANS, t_scan);
        // The longest recently: a running maximum that forgets (a scan that repeats another costs nothing).
        self.scan_ns = if ns >= self.scan_ns { ns } else { self.scan_ns - self.scan_ns / 64 };
        self.scans.pop_front();
        for e in found {
            self.log_encounter(e);
        }
    }

    // ---- observation ----------------------------------------------------------------------------

    pub fn rec(&self, i: usize) -> BodyRec {
        self.bodies.rec(i)
    }

    /// Key body `i` in `prunable` at the earliest tick its oldest retired binding could be forgotten (never before `after`), or take it
    /// out when it holds one or none.
    fn key_prune(&mut self, i: usize, after: Tick) {
        let at = self.bodies.droppable_until(i).map(|u| u.saturating_add(2 * self.light_distance(i) + (1 << 26)).max(after));
        self.prunable.set(i, at);
    }

    /// Forget history the view can no longer need: older than twice the body's light distance (plus a
    /// margin) behind the present, and older than the oldest item any body still has to resolve. Only the bodies whose oldest
    /// binding could go by now are visited (`prunable`, by that tick: a body is visited once when it can be shortened, not every
    /// call while it has history: the bodies kicked since the last call were each visited, a spike the size of a wave of kicks);
    /// one the oldest item holds back, or whose light distance grew, is visited again at the next call. When a binding is forgotten
    /// changes no outcome (only what may be forgotten is): nothing at or after the oldest item reads what ended before it.
    pub fn prune(&mut self) {
        // The oldest item any body still has to resolve (the planets, the moons and the player by a walk of those few, the ships by the
        // first of the due ones: a ship in the calendar has a tick after what it handed out, which is not before the present).
        let mut oldest = self.now;
        let few = self.lanes.planets.iter().chain(&self.lanes.moons).copied().chain(self.player);
        for i in few {
            if let Some(t) = self.bodies.next_time(i) {
                oldest = oldest.min(t);
            }
        }
        for c in 0..2 {
            if let Some((t, _)) = self.due_top(c) {
                oldest = oldest.min(t);
            }
        }
        while let Some(i) = self.prunable.pop_due(self.now) {
            let keep = 2 * self.light_distance(i) + (1 << 26);
            if self.bodies.prune(i, (self.now - keep).min(oldest - (1 << 26))) > 0 {
                // what a reader can still ask for shrank: so does where the body is registered
                self.radial.rebuild(i, self.info[i].kind, crate::num::to_f64(self.info[i].radius), self.bodies.bindings_of(i).iter());
            }
            self.key_prune(i, self.now + 1);
        }
    }

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
            if let Some(key) = r.b.entry.trajectory.key() {
                put_s(&mut h, key.periapsis);
                put(&mut h, key.k as i128);
                if key.k_exponent != 0 {
                    put(&mut h, key.k_exponent as i128);
                }
                if let Some(gap) = key.gap {
                    put_s(&mut h, gap);
                }
            } else if let Trajectory::Plunge(p) = &r.b.entry.trajectory {
                put(&mut h, -1);
                for coefficient in p.coefficients() { put_s(&mut h, coefficient); }
                put_s(&mut h, p.arrival().end.radius());
            }
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
        // The scans still held count as answered: the chain, extended by them in their order.
        let mut enc = self.enc_digest;
        for held in &self.scans {
            for e in held.answer() {
                enc = chain(enc, &e);
            }
        }
        h.update(&enc);
        h.finalize().to_hex().to_string()
    }

    /// The canonical time at which a body's next item is, for tests.
    pub fn horizon_of(&self, i: usize) -> Option<Tick> {
        self.key_of(i).map(|k| k.0)
    }
}
