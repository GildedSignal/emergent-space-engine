//! One clock, one queue, one digest.
//!
//! **The root clock is canonical.** A tick is the same physical time in every doll
//! ([`crate::world`]). Every entity (a body, a fleet) holds the time of its next certified event;
//! the queue is a min over entities, with deterministic ties (time, then entity id, ids running
//! star, planets, moon, ships, player, fleets).
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
use crate::bind::{bind_exact, Catalogue, Entry};
use crate::body::{BodyRec, BodyStore, Kind, PlainBodies, Segment, Thrust, What};
use crate::ctx::{BodyInfo, Config, Ctx};
use crate::encounter::{Encounter, Encounters, PlayerNeighbourhood};
use crate::fleet::Fleet;
use crate::num::{Error, Res, Tick};
use crate::step::{self, Resolved, Update};
use crate::world::{pow2, DollRec};
use emergent_space::{
    binding::Trajectory,
    events::Calendar,
    orbit::{Orbit, OrbitKey, Scalar},
    Tube,
};
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
    fn spent(&self, done: u64) -> bool {
        done >= self.events || self.until.is_some_and(|u| Instant::now() >= u)
    }
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
            threads: 1,
            slice: 1 << 18,
            lanes: Lanes::default(),
            target: 0,
            encounters: Box::new(PlayerNeighbourhood),
            enc_log: Vec::new(),
            enc_digest: [0; 32],
            contacts: 0,
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

    /// Add a child doll centred on an existing body (a tube in the parent doll). `mass_log2` is
    /// the doll's mass as an octave of the root's; `surface` the centre's radius in the doll's units.
    pub fn add_doll(&mut self, name: &'static str, centre: usize, mass_log2: i32, surface: Scalar) -> Res<u16> {
        let host = self.bodies.rec(centre).b.doll;
        let tube = self.bodies.rec(centre).b.tube;
        let sep = self.bodies.rec(centre).b.entry.trajectory.key().periapsis;
        let parent_rec = self.dolls[host as usize].record.clone();
        let proto = emergent_space::events::Doll::child(emergent_space::events::LogMass(mass_log2 << 24), host, tube);
        // The sphere of influence from the mass ratio (Laplace): separation · (m/M)^(2/5), in the parent's units.
        let soi_parent = proto.edge_radius(&parent_rec, sep)?;
        let id = u16::try_from(self.dolls.len()).map_err(|_| Error::Refused("too many dolls"))?;
        let shift_h = self.dolls[host as usize].shift;
        let edge = soi_parent.scale((-mass_log2) as i32 - shift_h as i32)?;
        self.dolls.push(DollRec::child(name, host, mass_log2, centre, tube, surface, edge));
        self.sources.push(Vec::new());
        self.info[centre].doll = Some(id);
        self.info[centre].soi = soi_parent;
        self.info[centre].gm = pow2(mass_log2 - self.dolls[host as usize].mass_log2);
        self.sources[host as usize].push(centre);
        Ok(id)
    }

    /// Make a body from an orbit: a tube of `spec.doll`, exactly (no remainder to carry).
    pub fn add_body(&mut self, kind: Kind, spec: OrbitSpec, radius: Scalar) -> Res<usize> {
        let doll = &self.dolls[spec.doll as usize];
        let key = OrbitKey::bound(spec.periapsis, spec.e_q48)?;
        let orbit = Orbit::compile(key)?;
        let period = orbit.period()?;
        let entry = Arc::new(Entry { trajectory: Trajectory::Cycle(orbit), clockwise: spec.clockwise });
        let clock_exp = doll.clock_exp();
        // Periapsis `phase` of a period before tick 0.
        let behind = period.mul(Scalar::raw(spec.phase as i128, -32)?)?;
        let peri = -i64::try_from(behind.fixed(-(clock_exp as i32))?).map_err(|_| Error::Refused("period outside the clock"))?;
        let k = Scalar::raw(key.k as i128, -48)?;
        let r_max = key.periapsis.div(k.scale(1)?.sub(Scalar::ONE)?)?; // apoapsis: p/(2k − 1)
        let v_max = Scalar::integer(2).mul(Scalar::ONE.div(key.periapsis)?)?.sqrt()?.scale(1)?;
        let units = crate::bind::choose_units(r_max, v_max);
        let id = self.cat.insert(entry.clone())?;
        let tube = Tube::new(id, spec.angle, peri);
        let b = bind_exact(entry, tube, clock_exp, units, 0, spec.doll);
        let rec = BodyRec {
            kind,
            b,
            carry: [0; 2],
            proper: Scalar::ZERO,
            step: 0,
            interval: 0,
            anchor: 0,
            plan: Vec::new(),
            thrust: (kind == Kind::Player).then_some(Thrust { keys: 0, heading: 0, since: 0 }),
            alive: true,
            events: 0,
            refusals: 0,
            fault: None,
        };
        let i = self.bodies.push(rec);
        self.info.push(BodyInfo { kind, gm: Scalar::ZERO, soi: Scalar::ZERO, doll: None, radius });
        if kind == Kind::Player {
            self.player = Some(i);
        }
        Ok(i)
    }

    /// Give a body a pull as a secondary (a planet, the moon): `mass_log2` is its mass as an octave of
    /// its doll's.
    pub fn make_source(&mut self, i: usize, gm_log2: i32, soi: Scalar) {
        self.info[i].gm = pow2(gm_log2);
        self.info[i].soi = soi;
        let d = self.bodies.rec(i).b.doll as usize;
        if !self.sources[d].contains(&i) {
            self.sources[d].push(i);
        }
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
        self.queue = Some(Calendar::new(n + self.fleets.len()));
        self.rekey();
        Ok(())
    }

    pub fn add_fleet(&mut self, f: Fleet) -> usize {
        self.fleets.push(f);
        self.fleets.len() - 1
    }

    fn entities(&self) -> usize {
        self.bodies.len() + self.fleets.len()
    }

    // ---- the keys -------------------------------------------------------------------------------

    /// The `(tick, id)` of an entity's next item.
    pub fn key_of(&self, e: usize) -> Option<(Tick, usize)> {
        let n = self.bodies.len();
        if e < n {
            self.bodies.next_time(e).map(|t| (t, e))
        } else {
            let f = &self.fleets[e - n];
            f.next_time().map(|t| (t, e))
        }
    }

    fn light_distance(&self, e: usize) -> Tick {
        let n = self.bodies.len();
        if Some(e) == self.player {
            return 0;
        }
        let p = if e < n { self.pos[e] } else { self.fleets[e - n].root_position() };
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
            if let Ok((pos, _)) = crate::observe::root_state(&self.ctx(), p, self.bodies.event_time(p).max(self.now)) {
                self.observer = pos;
            }
        }
        for e in 0..self.entities() {
            self.requeue(e);
        }
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
        let t = upd.rec.b.event_time;
        self.bodies.put(i, upd.rec);
        if let Ok((p, _)) = crate::observe::root_state(&self.ctx(), i, t) {
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
        let n = self.bodies.len();
        if e < n {
            self.resolve_body(e);
        } else {
            let f = e - n;
            self.stats.slices += self.fleets[f].advance(self.slice, self.target);
            self.update_fleet_position(f);
        }
        self.requeue(e);
    }

    fn update_fleet_position(&mut self, f: usize) {
        let t = self.fleets[f].tick();
        let centre = self.fleets[f].centre;
        if let (Ok((cp, _)), Some((o, _))) = (crate::observe::root_state(&self.ctx(), centre, t.max(self.bodies.event_time(centre))), self.fleets[f].origin(t)) {
            let k = 2f64.powi(-20);
            self.fleets[f].pos = [cp[0] + o[0] * k, cp[1] + o[1] * k];
        }
    }

    /// Spend `budget` resolving items with a tick up to `target`, in causal-deadline order.
    pub fn advance(&mut self, target: Tick, budget: Budget) -> Advanced {
        self.target = target;
        self.rekey();
        let start = self.stats.events();
        let mut done = 0u64;
        let mut deferred: Vec<usize> = Vec::new();
        let mut overflow = false;
        loop {
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
            self.resolve_entity(e);
            done = self.stats.events() - start;
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

    // ---- decisions ------------------------------------------------------------------------------

    /// The player's keys (bit 0 forward, 1 reverse, 2 left, 3 right) change at tick `t`, which must be
    /// `now` or later and not before the player's committed tick. The change is a decision event.
    pub fn input(&mut self, t: Tick, keys: u8) -> Res<()> {
        let p = self.player.ok_or(Error::Refused("no player"))?;
        if keys > 15 || t < self.now.min(self.bodies.event_time(p)) {
            return Err(Error::Refused("input in the past"));
        }
        // The player's own past is resolved first (and what it reads, by pulling).
        while self.key_of(p).is_some_and(|k| k.0 <= t) {
            self.resolve_body(p);
        }
        let rec = self.bodies.rec(p);
        let upd = step::decide(&self.ctx(), p, rec, t, keys);
        self.apply(p, upd);
        self.stats.decisions += 1;
        self.inputs.push((t, keys));
        self.requeue(p);
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

    /// Prune histories the view can no longer need (older than the light-time to the farthest thing
    /// plus a margin, and older than every body that still reads them).
    pub fn prune(&mut self, keep: Tick) {
        let watermark = (0..self.bodies.len()).filter_map(|i| self.bodies.next_time(i)).min().unwrap_or(self.now).min(self.now);
        for i in 0..self.bodies.len() {
            self.bodies.prune(i, watermark - keep);
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
            put_s(&mut h, r.b.delta);
            for c in 0..2 {
                put(&mut h, r.b.residual.position[c]);
                put(&mut h, r.b.residual.velocity[c]);
                put(&mut h, r.carry[c] as i128);
            }
            put(&mut h, r.b.units.0 as i128);
            put(&mut h, r.b.units.1 as i128);
            put_s(&mut h, r.proper);
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
                put(&mut h, t.heading as i128);
                put(&mut h, t.since as i128);
            }
            put(&mut h, r.events as i128);
            put(&mut h, r.refusals as i128);
            h.update(format!("{:?}", r.fault).as_bytes());
        }
        for f in &self.fleets {
            h.update(f.outcome_digest().as_bytes());
        }
        for (t, k) in &self.inputs {
            put(&mut h, *t as i128);
            put(&mut h, *k as i128);
        }
        h.update(&self.enc_digest);
        h.finalize().to_hex().to_string()
    }

    /// The canonical time at which a body's next item is, for tests.
    pub fn horizon_of(&self, i: usize) -> Option<Tick> {
        self.key_of(i).map(|k| k.0)
    }
}

