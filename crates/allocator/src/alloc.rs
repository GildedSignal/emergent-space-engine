//! Regions with clocks, window certificates, scoped rollback, finality, least-slack
//! scheduling, bounded units, core classes, snapshot publishing and monitoring. The
//! certificate and finality arguments are in the crate docs (lib.rs).
use crate::forecast::{kinetic, CostModel, Features, Sabotage};
use crate::geom::{coalesce, islands, separated, Aabb, Ent, Uf};
use crate::qos::{self, Class};
use crate::report::*;
use emergent_lattice::law::{Body, Consumed, Tick, World};
use emergent_lattice::worlds::Rng;
use emergent_lattice::{Log, Stepper};
use serde::Serialize;
use std::collections::{BTreeMap, HashMap, HashSet, VecDeque};
use std::sync::atomic::{AtomicU64, AtomicUsize, Ordering::Relaxed};
use std::sync::{Arc, Condvar, Mutex, MutexGuard};
use std::thread::{self, JoinHandle};
use std::time::{Duration, Instant};

/// Builds a region's stepper from its canonical world (any execution mode).
pub type Factory<S> = Arc<dyn Fn(World) -> S + Send + Sync>;

/// Chronons per second used to price slack when no frame clock runs (ordering only).
const BATCH_RATE: f64 = 1000.0;
/// Slack (s) under which efficiency workers leave a region to idle performance workers.
const URGENT: f64 = 0.005;

#[derive(Clone, Debug, Serialize)]
pub struct Config {
    /// Worker threads at user-interactive QoS (performance cores).
    pub p_workers: usize,
    /// Worker threads at utility QoS (efficiency cores).
    pub e_workers: usize,
    /// Certificate window in chronons: true boxes are measured and compared per window.
    pub window: Tick,
    /// Target wall time of one unit.
    pub unit_seconds: f64,
    /// Ops budget per unit instead of the calibrated one (invariance tests).
    pub fixed_budget: Option<u64>,
    /// Promise growth = tracked max |k_c| × margin: a forecast that plans merges; never trusted.
    pub speed_margin: f64,
    /// Seed: multiply every cost and speed forecast by a log-uniform factor in [0.1, 10].
    pub sabotage: Option<u64>,
    /// Windows ahead that two groups must stay apart before a region splits.
    pub split_lookahead: i64,
    /// Accepted windows between split checks of a region.
    pub split_every: u32,
    /// Smallest region a split may create: a tiny region costs more in per-window overhead
    /// (planning, measuring, scheduling) than it saves, so smaller groups join the nearest
    /// large one.
    pub min_region: usize,
    /// A per-axis speed bound (1/Q units per chronon) that the *law* guarantees for every body
    /// at every tick. It turns on light-cone finality (a region is published as soon as no
    /// unfinished history can reach it). None for es-lattice-elastic-v0: elastic exchanges
    /// push bodies past c without bound, so only the global all-verified tick is final.
    pub hard_speed: Option<i64>,
    /// The player's position (1/Q units): deadlines are distance / c from here.
    pub observer: [i64; 2],
    /// Radius of what the frame draws around the observer (1/Q units).
    pub view_radius: i64,
}

impl Default for Config {
    fn default() -> Self {
        Config {
            p_workers: 4,
            e_workers: 4,
            window: 32,
            unit_seconds: 0.5e-3,
            fixed_budget: None,
            speed_margin: 2.0,
            sabotage: None,
            split_lookahead: 2,
            split_every: 2,
            min_region: 32,
            hard_speed: None,
            observer: [0, 0],
            view_radius: 0,
        }
    }
}

#[derive(Clone, Debug)]
pub struct FrameConfig {
    pub hz: f64,
    pub seconds: f64,
    /// Target time acceleration: chronons of the player's present per wall second.
    pub rate: f64,
    /// Compute-ahead buffer target, in wall seconds at `rate`.
    pub ahead_seconds: f64,
    /// Keep every snapshot a frame drew (for audits: see [`Allocator::drawn`]).
    pub record: bool,
}

impl Default for FrameConfig {
    fn default() -> Self {
        FrameConfig { hz: 120.0, seconds: 1.0, rate: 400.0, ahead_seconds: 0.25, record: false }
    }
}

/// Accepted state of part of the world at `tick`, produced by region `owner`: what rollback
/// restores and, once final, what frames draw. `log` and `ops` are lineage totals.
pub struct Snap {
    pub tick: Tick,
    pub world: World,
    pub log: Log,
    pub ops: u64,
    pub owner: u64,
    pub bbox: Aabb,
    pub rmax: i64,
}

impl Snap {
    fn new(world: World, log: Log, ops: u64, owner: u64) -> Arc<Snap> {
        let bbox = Aabb::of(world.bodies.iter().map(|b| &b.x));
        let rmax = world.bodies.iter().map(|b| b.radius).max().unwrap_or(0);
        Arc::new(Snap { tick: world.tick, world, log, ops, owner, bbox, rmax })
    }
}

/// What the frame thread reads: one pointer, swapped whole by workers. Only final states:
/// every body appears once, in the snapshot of its region's final tick.
#[derive(Default)]
pub struct View {
    pub parts: Vec<Arc<Snap>>,
    /// The global all-verified tick (every part is at or after it).
    pub frontier: Tick,
}

/// Forecast box: centres at `tick` inside `bbox`, growing `v` per axis per chronon.
#[derive(Clone, Copy, Debug)]
struct Model {
    tick: Tick,
    bbox: Aabb,
    v: i64,
}

impl Model {
    fn at(&self, end: Tick) -> Aabb {
        self.bbox.grow(self.v.saturating_mul((end - self.tick).max(0)))
    }
}

type History = VecDeque<(Tick, Vec<Arc<Snap>>)>;

struct Region<S> {
    id: u64,
    stepper: Option<S>,
    busy: bool,
    /// Stepper tick; accepted only up to `verified`.
    tick: Tick,
    /// Last tick whose window ended with a true box clear of every true box recorded so far.
    verified: Tick,
    /// Last tick no rollback can ever reach (published to frames).
    fin: Tick,
    last: Arc<Snap>,
    /// Centres at `verified`: the start of the window being computed.
    bbox: Aabb,
    rmax: i64,
    model: Model,
    feat: Features,
    cost_factor: f64,
    /// Snapshots of this lineage at every accepted tick not older than the global frontier.
    /// Regions born from a regroup share their parents' entries.
    history: History,
    base_log: Log,
    base_ops: u64,
    since_split: u32,
    /// After a rollback the conflicting lineages recompute the window together, unsplit.
    no_split_until: Tick,
}

impl<S: Stepper> Region<S> {
    fn ops(&self) -> u64 {
        self.stepper.as_ref().map_or(self.last.ops, |s| self.base_ops + s.metrics().ops)
    }
    fn entry(&self, t: Tick) -> Option<&Vec<Arc<Snap>>> {
        self.history.iter().find(|(u, _)| *u == t).map(|(_, s)| s)
    }
}

/// One window of the plan: entities (sets of regions that are, or will by the window start
/// be, one region) with forecast boxes. Plans schedule merges before regions collide; they
/// carry no correctness.
struct Plan {
    ents: Vec<Ent<u64>>,
    of: HashMap<u64, usize>,
}

impl Plan {
    fn new(ents: Vec<Ent<u64>>) -> Self {
        let mut p = Plan { ents, of: HashMap::new() };
        p.reindex();
        p
    }
    fn reindex(&mut self) {
        self.of = self.ents.iter().enumerate().flat_map(|(i, e)| e.ids.iter().map(move |&id| (id, i))).collect();
    }
    fn ent(&self, id: u64) -> &Ent<u64> {
        &self.ents[self.of[&id]]
    }
}

/// A region's true box over one window (exact, from the extent argument).
struct Truth {
    id: u64,
    bbox: Aabb,
    r: i64,
}

#[derive(Clone, Copy)]
enum Goal {
    Batch(Tick),
    Frames { rate: f64, ahead: f64 },
}

#[derive(Default)]
struct Stats {
    units: u64,
    unit_ms: Vec<f64>,
    unit_ms_class: [Vec<f64>; 2],
    advance_ms: Vec<f64>,
    measure_ms: Vec<f64>,
    lock_ms: Vec<f64>,
    unit_ops: Vec<f64>,
    over_ops: Vec<f64>,
    over_ratio_max: f64,
    stepper_max_unit_ops: u64,
    queue: Vec<f64>,
    err: Vec<f64>,
    picks: u64,
    merges: u64,
    splits: u64,
    avoided: u64,
    exceeded: u64,
    rollbacks: u64,
    rolled_regions: u64,
    rollback_depth: Vec<f64>,
    accepted: u64,
    wasted: u64,
    chronons: u64,
    regions_initial: usize,
    regions_max: usize,
    hard_speed_violations: u64,
}

struct State<S> {
    cfg: Config,
    factory: Factory<S>,
    t0: Tick,
    q: i64,
    bodies: usize,
    /// A container world: one region, no boxes (walls break the extent argument).
    closed: bool,
    keep: bool,
    regions: BTreeMap<u64, Region<S>>,
    next_id: u64,
    plan_base: i64,
    plans: VecDeque<Plan>,
    truths: BTreeMap<i64, Vec<Truth>>,
    /// Region id → regions created from it (regroups, restores): lineage for scoped rollback.
    children: HashMap<u64, Vec<u64>>,
    /// Hard speed while light-cone finality is on (switched off for good by a violation).
    lightcone: Option<i64>,
    goal: Goal,
    escalation: f64,
    sabotage: Option<Sabotage>,
    cost: CostModel,
    /// Seconds per op, per core class.
    spo: [f64; 2],
    st: Stats,
    idle_p: usize,
    running: bool,
    dirty: bool,
}

struct Job<S> {
    id: u64,
    stepper: S,
    target: Tick,
    budget: u64,
    split_extra: Option<i64>,
    min_region: usize,
    feat: Features,
    predicted: f64,
    tick0: Tick,
}

struct Done<S> {
    id: u64,
    stepper: S,
    tick: Tick,
    tick0: Tick,
    ops: u64,
    budget: u64,
    advance_secs: f64,
    measure_secs: f64,
    feat: Features,
    predicted: f64,
    /// World, centre box and islands at the target, when reached.
    end: Option<(World, Aabb, Option<Vec<Vec<usize>>>)>,
}

enum Pick<S> {
    Run(Job<S>),
    Idle,
    Decline,
}

fn class_ix(c: Class) -> usize {
    match c {
        Class::Performance => 0,
        Class::Efficiency => 1,
    }
}

fn vmax<'a>(bs: impl Iterator<Item = &'a Body>) -> i64 {
    bs.map(|b| b.k[0].abs().max(b.k[1].abs())).max().unwrap_or(0)
}

fn speed(vmax: i64, factor: f64) -> i64 {
    if vmax == 0 {
        0
    } else {
        (vmax as f64 * factor).ceil().clamp(0.0, 1e15) as i64
    }
}

/// A copy of `w` without bodies or contacts: every other field, including any the contract
/// adds later, is carried through unchanged.
fn shell(w: &World) -> World {
    World { bodies: Vec::new(), consumed: Vec::new(), ..w.clone() }
}

/// Union of worlds at one tick: whole bodies by id, consumed contacts, summed ledgers.
fn union_of(ws: &[&World]) -> World {
    assert!(ws.windows(2).all(|p| p[0].tick == p[1].tick && p[0].q == p[1].q), "united worlds share tick and quantum");
    let mut bodies: Vec<Body> = ws.iter().flat_map(|w| w.bodies.iter().cloned()).collect();
    bodies.sort_unstable_by_key(|b| b.id);
    let mut consumed: Vec<Consumed> = ws.iter().flat_map(|w| w.consumed.iter().copied()).collect();
    consumed.sort_unstable();
    let wall = ws.iter().fold([0i64; 2], |a, w| [a[0] + w.wall_momentum[0], a[1] + w.wall_momentum[1]]);
    World { bodies, consumed, wall_momentum: wall, ..shell(ws[0]) }
}

fn push_unique(v: &mut Vec<Arc<Snap>>, s: &Arc<Snap>) {
    if !v.iter().any(|x| Arc::ptr_eq(x, s)) {
        v.push(s.clone());
    }
}

fn merged_history<'a>(hs: impl Iterator<Item = &'a History>, before: Tick) -> History {
    let mut m: BTreeMap<Tick, Vec<Arc<Snap>>> = BTreeMap::new();
    for h in hs {
        for (t, snaps) in h.iter().filter(|(t, _)| *t < before) {
            let e = m.entry(*t).or_default();
            snaps.iter().for_each(|s| push_unique(e, s));
        }
    }
    m.into_iter().collect()
}

impl<S: Stepper + Send + 'static> State<S> {
    fn boundary(&self, w: i64) -> Tick {
        self.t0 + w * self.cfg.window
    }
    fn window(&self, t: Tick) -> i64 {
        (t - self.t0).div_euclid(self.cfg.window)
    }
    fn plan_end(&self) -> i64 {
        self.plan_base + self.plans.len() as i64
    }
    fn has_plan(&self, w: i64) -> bool {
        w >= self.plan_base && w < self.plan_end()
    }
    fn plan(&self, w: i64) -> &Plan {
        &self.plans[(w - self.plan_base) as usize]
    }
    fn plan_mut(&mut self, w: i64) -> &mut Plan {
        let i = (w - self.plan_base) as usize;
        &mut self.plans[i]
    }
    fn frontier(&self) -> Tick {
        self.regions.values().map(|r| r.verified).min().unwrap_or(self.t0)
    }

    /// margin × sabotage, widened after every rollback ("bad forecasters get wider bands");
    /// the additive term keeps widening even from a zero margin.
    fn speed_factor(&mut self) -> f64 {
        let sab = self.sabotage.as_mut().map_or(1.0, |s| s.factor());
        (self.cfg.speed_margin * sab).max(0.0) * self.escalation + (self.escalation - 1.0)
    }
    fn cost_factor(&mut self) -> f64 {
        self.sabotage.as_mut().map_or(1.0, |s| s.factor())
    }
    fn rate(&self) -> f64 {
        match self.goal {
            Goal::Frames { rate, .. } => rate,
            Goal::Batch(_) => BATCH_RATE,
        }
    }
    /// Batch: the target. Frames: the compute-ahead cap, rounded up to a window boundary so
    /// every region idles on a boundary.
    fn goal_tick(&self, present: f64) -> Tick {
        match self.goal {
            Goal::Batch(t) => t,
            Goal::Frames { rate, ahead } => {
                let g = self.cfg.window;
                let w = ((present + ahead * rate - self.t0 as f64) / g as f64).ceil().max(0.0) as i64;
                self.t0 + w * g
            }
        }
    }
    /// Chronons for light from the nearest body of `bbox` to reach the observer.
    fn delay(&self, bbox: &Aabb, rmax: i64) -> f64 {
        (bbox.distance(self.cfg.observer) - rmax as f64).max(0.0) / self.q as f64
    }
    /// Deadline − now − forecast cost of the next window, in seconds. The deadline is when
    /// the region's frontier must be final for the frame: with light-cone finality, its light
    /// delay after the present; with global finality, the present itself (every region must
    /// be verified before any is shown).
    fn slack(&self, id: u64, present: f64) -> f64 {
        let r = &self.regions[&id];
        let delay = if self.lightcone.is_some() { self.delay(&r.bbox, r.rmax) } else { 0.0 };
        let cost = self.cost.predict(&r.feat) * self.cfg.window as f64 * self.spo[0] * r.cost_factor;
        (r.tick as f64 + delay - present) / self.rate() - cost
    }

    fn anchor(&mut self, id: u64, snap: Arc<Snap>) {
        let (f, cf, closed) = (self.speed_factor(), self.cost_factor(), self.closed);
        let r = self.regions.get_mut(&id).expect("anchored region exists");
        let b = &snap.world.bodies;
        r.bbox = snap.bbox;
        r.rmax = snap.rmax;
        r.feat = kinetic(b, &r.bbox);
        r.model = if closed {
            Model { tick: snap.tick, bbox: Aabb::EVERYWHERE, v: 0 }
        } else {
            Model { tick: snap.tick, bbox: r.bbox, v: speed(vmax(b.iter()), f) }
        };
        r.cost_factor = cf;
        r.last = snap;
    }

    fn make_region(&mut self, world: World, log: Log, ops: u64, mut history: History, fin: Tick) -> u64 {
        let id = self.next_id;
        self.next_id += 1;
        let tick = world.tick;
        let stepper = (self.factory)(world.clone());
        assert_eq!(stepper.tick(), tick, "a stepper starts at its world's tick");
        self.keep = stepper.log().keep;
        let mut log = log;
        log.keep |= self.keep;
        let snap = Snap::new(world, log.clone(), ops, id);
        history.push_back((tick, vec![snap.clone()]));
        let model = Model { tick, bbox: Aabb::EMPTY, v: 0 };
        self.regions.insert(
            id,
            Region {
                id,
                stepper: Some(stepper),
                busy: false,
                tick,
                verified: tick,
                fin: fin.min(tick),
                last: snap.clone(),
                bbox: Aabb::EMPTY,
                rmax: 0,
                model,
                feat: Features::default(),
                cost_factor: 1.0,
                history,
                base_log: log,
                base_ops: ops,
                since_split: 0,
                no_split_until: tick,
            },
        );
        self.anchor(id, snap);
        self.st.regions_max = self.st.regions_max.max(self.regions.len());
        id
    }

    fn ensure_plan(&mut self, w: i64) {
        assert!(w >= self.plan_base, "plans are kept for every region's current window");
        while self.plan_end() <= w {
            self.plan_next();
        }
    }

    /// Plan the next window: each entity of the previous window (a merge, once planned, stays)
    /// gets the hull of its regions' forecast boxes at the window end; conflicting entities
    /// unite and must merge at the window start.
    fn plan_next(&mut self) {
        let w = self.plan_end();
        let end = self.boundary(w + 1);
        let mut sets: Vec<Vec<u64>> = match self.plans.back() {
            Some(p) => p.ents.iter().map(|e| e.ids.iter().copied().filter(|id| self.regions.contains_key(id)).collect::<Vec<_>>()).filter(|s| !s.is_empty()).collect(),
            None => vec![],
        };
        let seen: HashSet<u64> = sets.iter().flatten().copied().collect();
        sets.extend(self.regions.keys().filter(|id| !seen.contains(id)).map(|&id| vec![id]));
        let ents = sets
            .into_iter()
            .map(|ids| {
                let (mut bbox, mut r) = (Aabb::EMPTY, 0);
                for id in &ids {
                    let g = &self.regions[id];
                    bbox = bbox.hull(&g.model.at(end));
                    r = r.max(g.rmax);
                }
                Ent { ids, bbox, r }
            })
            .collect();
        self.plans.push_back(Plan::new(coalesce(ents)));
    }

    fn pick(&mut self, class: Class, present: f64, depth: &AtomicUsize) -> Pick<S> {
        self.ready_merges();
        let goal = self.goal_tick(present);
        let ids: Vec<u64> = self.regions.keys().copied().collect();
        let mut run: Vec<(u64, Tick)> = Vec::new();
        let mut waits: Vec<(u64, i64)> = Vec::new();
        for id in ids {
            let (busy, tick) = (self.regions[&id].busy, self.regions[&id].tick);
            if busy || tick >= goal {
                continue;
            }
            let w = self.window(tick);
            self.ensure_plan(w);
            if self.plan(w).ent(id).ids.len() > 1 {
                waits.push((id, w));
            } else {
                run.push((id, self.boundary(w + 1).min(goal)));
            }
        }
        depth.store(run.len(), Relaxed);
        self.st.picks += 1;
        if self.st.picks % 4 == 0 {
            self.st.queue.push(run.len() as f64);
        }
        if run.is_empty() {
            return Pick::Idle;
        }
        let mut slack: HashMap<u64, f64> = run.iter().map(|&(id, _)| (id, self.slack(id, present))).collect();
        // Deadlines propagate through dependencies: a region others wait for (to merge) is due
        // when the earliest of them is.
        for &(wid, w) in &waits {
            let (s, b) = (self.slack(wid, present), self.boundary(w));
            for m in &self.plan(w).ent(wid).ids {
                if self.regions.get(m).is_some_and(|x| x.tick < b) {
                    if let Some(x) = slack.get_mut(m) {
                        *x = x.min(s);
                    }
                }
            }
        }
        let best = |all: bool| run.iter().filter(|(id, _)| all || slack[id] >= URGENT).min_by(|a, b| slack[&a.0].total_cmp(&slack[&b.0])).copied();
        let choice = match class {
            Class::Performance => best(true),
            Class::Efficiency => best(false).or_else(|| (self.idle_p == 0).then(|| best(true)).flatten()),
        };
        match choice {
            Some((id, target)) => Pick::Run(self.checkout(id, target, class)),
            None => Pick::Decline,
        }
    }

    fn checkout(&mut self, id: u64, target: Tick, class: Class) -> Job<S> {
        let (g, l, every) = (self.cfg.window, self.cfg.split_lookahead.max(0), self.cfg.split_every.max(1));
        let at_boundary = (target - self.t0).rem_euclid(g) == 0;
        let budget = self.cfg.fixed_budget.unwrap_or_else(|| (self.cfg.unit_seconds / self.spo[class_ix(class)]).max(1.0) as u64).max(1);
        let closed = self.closed;
        let r = self.regions.get_mut(&id).expect("picked region exists");
        r.busy = true;
        let due = r.since_split + 1 >= every && target > r.no_split_until;
        let split_extra = (!closed && at_boundary && due && r.last.world.bodies.len() > 1).then(|| r.model.v.saturating_mul((l + 1) * g).saturating_mul(2));
        let (feat, tick0) = (r.feat, r.tick);
        let stepper = r.stepper.take().expect("an idle region holds its stepper");
        Job { id, stepper, target, budget, split_extra, min_region: self.cfg.min_region.max(1), feat, predicted: self.cost.predict(&feat), tick0 }
    }

    fn commit(&mut self, d: Done<S>, secs: f64, class: Class) {
        let st = &mut self.st;
        st.units += 1;
        st.unit_ms.push(secs * 1e3);
        st.unit_ms_class[class_ix(class)].push(secs * 1e3);
        st.advance_ms.push(d.advance_secs * 1e3);
        st.measure_ms.push(d.measure_secs * 1e3);
        st.unit_ops.push(d.ops as f64);
        // Overshoot belongs to the stepper (its indivisible step); measuring belongs to us.
        if d.ops > d.budget {
            st.over_ops.push((d.ops - d.budget) as f64);
        }
        st.over_ratio_max = st.over_ratio_max.max(d.ops as f64 / d.budget as f64);
        st.stepper_max_unit_ops = st.stepper_max_unit_ops.max(d.stepper.metrics().max_unit_ops);
        if d.ops >= 256 {
            let c = class_ix(class);
            self.spo[c] = 0.9 * self.spo[c] + 0.1 * d.advance_secs / d.ops as f64;
        }
        let chronons = (d.tick - d.tick0) as u64;
        self.st.chronons += chronons;
        let measured = d.ops as f64 / chronons.max(1) as f64;
        self.st.err.push((measured.max(1.0) / d.predicted).log2().abs());
        self.cost.learn(&d.feat, measured);
        let Some(r) = self.regions.get_mut(&d.id) else {
            self.st.wasted += d.ops; // rolled back while it ran
            return;
        };
        r.stepper = Some(d.stepper);
        r.busy = false;
        r.tick = d.tick;
        let Some((world, end, comps)) = d.end else { return };
        if let Err(owners) = self.certify(d.id, d.tick0, &end) {
            self.rollback(self.window(d.tick0), owners);
            return;
        }
        self.accept(d.id, world);
        if let Some(c) = comps {
            self.regions.get_mut(&d.id).expect("accepted region exists").since_split = 0;
            if c.len() > 1 {
                self.regroup(vec![d.id], Some(c));
            }
        }
        self.prune();
        self.dirty = true;
    }

    /// The certificate. With no walls, the outermost body's outward velocity never decreases
    /// (bounce impulses push it outward, stops set it to zero), so the extent of an isolated
    /// region over a window is exactly the hull of its extents at the two ends. Two isolated
    /// regions of one window cannot have met if their true boxes stay out of reach; the one
    /// that finishes second checks the pair. On a conflict, returns the regions involved.
    fn certify(&mut self, id: u64, tick0: Tick, end: &Aabb) -> Result<(), Vec<u64>> {
        if self.closed {
            return Ok(());
        }
        let w = self.window(tick0);
        let (truth, r) = (self.regions[&id].bbox.hull(end), self.regions[&id].rmax);
        let list = self.truths.entry(w).or_default();
        let clash: Vec<u64> = list.iter().filter(|t| t.id != id && !separated(&truth, r, &t.bbox, t.r)).map(|t| t.id).collect();
        if !clash.is_empty() {
            return Err(std::iter::once(id).chain(clash).collect());
        }
        list.push(Truth { id, bbox: truth, r });
        let promised = self.has_plan(w) && self.plan(w).of.get(&id).is_some_and(|&e| self.plan(w).ents[e].bbox.contains(&truth));
        self.st.exceeded += !promised as u64;
        Ok(())
    }

    fn accept(&mut self, id: u64, world: World) {
        if let Some(v) = self.lightcone {
            // The bound must hold at every tick; a sample above it voids light-cone finality.
            if vmax(world.bodies.iter()) > v {
                self.st.hard_speed_violations += 1;
                self.lightcone = None;
            }
        }
        let r = self.regions.get_mut(&id).expect("accepted region exists");
        let s = r.stepper.as_ref().expect("stepper returned");
        let mut log = r.base_log.clone();
        log.merge(s.log());
        let snap = Snap::new(world, log, r.base_ops + s.metrics().ops, id);
        r.verified = r.tick;
        r.since_split += 1;
        r.history.push_back((r.tick, vec![snap.clone()]));
        self.st.accepted += 1;
        self.anchor(id, snap);
    }

    /// Snapshots, truths and plans older than the global frontier can never be read again.
    fn prune(&mut self) {
        let front = self.frontier();
        for r in self.regions.values_mut() {
            while r.history.len() > 1 && r.history[0].0 < front {
                r.history.pop_front();
            }
        }
        let wf = self.window(front);
        while self.truths.first_key_value().is_some_and(|(&w, _)| w < wf) {
            self.truths.pop_first();
        }
        let (t0, g) = (self.t0, self.cfg.window);
        let wmin = self.regions.values().map(|r| (r.tick - t0).div_euclid(g)).min().unwrap_or(0);
        while self.plans.len() > 1 && self.plan_base < wmin {
            self.plans.pop_front();
            self.plan_base += 1;
        }
    }

    fn ready_merges(&mut self) {
        loop {
            let mut found = None;
            for r in self.regions.values() {
                let w = self.window(r.tick);
                if r.busy || r.tick != r.verified || r.tick != self.boundary(w) || !self.has_plan(w) {
                    continue;
                }
                let e = self.plan(w).ent(r.id);
                if e.ids.len() > 1
                    && e.ids.iter().all(|m| {
                        let x = &self.regions[m];
                        !x.busy && x.tick == r.tick && x.verified == r.tick
                    })
                {
                    found = Some(e.ids.clone());
                    break;
                }
            }
            match found {
                Some(m) => self.regroup(m, None),
                None => return,
            }
        }
    }

    /// Merge and split are one operation. At a common accepted tick, unite the members'
    /// worlds, cut the union into islands, and group islands until the groups' forecast boxes
    /// (clipped to the members' planned box) stay apart through `split_lookahead` windows.
    /// Groups become regions (a member whose bodies form exactly one group keeps its stepper);
    /// later planned windows keep the groups apart or plan them to merge where they meet.
    fn regroup(&mut self, members: Vec<u64>, comps: Option<Vec<Vec<usize>>>) {
        let tick = self.regions[&members[0]].verified;
        debug_assert!(members.iter().all(|m| {
            let r = &self.regions[m];
            !r.busy && r.tick == tick && r.verified == tick
        }));
        let w = self.window(tick);
        let (g, l) = (self.cfg.window, self.cfg.split_lookahead.max(0));
        let union = union_of(&members.iter().map(|m| &self.regions[m].last.world).collect::<Vec<_>>());
        let f = self.speed_factor();
        let comps = comps.unwrap_or_else(|| islands(&union, speed(vmax(union.bodies.iter()), f).saturating_mul((l + 1) * g).saturating_mul(2), self.cfg.min_region.max(1)));
        let models: Vec<(Model, i64)> = comps
            .iter()
            .map(|c| {
                let bbox = Aabb::of(c.iter().map(|&i| &union.bodies[i].x));
                let v = speed(vmax(c.iter().map(|&i| &union.bodies[i])), f);
                (Model { tick, bbox, v }, c.iter().map(|&i| union.bodies[i].radius).max().unwrap_or(0))
            })
            .collect();
        let boxof = |grp: &[usize], end: Tick, outer: Option<Aabb>| {
            let (mut b, mut r) = (Aabb::EMPTY, 0);
            for &c in grp {
                b = b.hull(&models[c].0.at(end));
                r = r.max(models[c].1);
            }
            (outer.map_or(b, |o| b.meet(&o)), r)
        };
        let near = w + l;
        let outer = |s: &Self, win: i64| s.has_plan(win).then(|| s.plan(win).ent(members[0]).bbox);
        let stabilize = |s: &Self, mut groups: Vec<Vec<usize>>| loop {
            let before = groups.len();
            for win in w..=near {
                let (end, o) = (s.boundary(win + 1), outer(s, win));
                let ents = groups.into_iter().map(|ids| {
                    let (bbox, r) = boxof(&ids, end, o);
                    Ent { ids, bbox, r }
                });
                groups = coalesce(ents.collect()).into_iter().map(|e| e.ids).collect();
            }
            if groups.len() == before {
                return groups;
            }
        };
        let mut groups = stabilize(self, (0..comps.len()).map(|i| vec![i]).collect());
        let size = |g: &Vec<usize>| g.iter().map(|&c| comps[c].len()).sum::<usize>();
        let min = self.cfg.min_region.max(1);
        if groups.len() > 1 && groups.iter().any(|g| size(g) < min) {
            let (mut large, small): (Vec<_>, Vec<_>) = groups.into_iter().partition(|g| size(g) >= min);
            if large.is_empty() {
                large = vec![small.concat()];
            } else {
                let bb = |g: &[usize]| g.iter().fold(Aabb::EMPTY, |b, &c| b.hull(&models[c].0.bbox));
                let gap = |a: &Aabb, b: &Aabb| (0..2).map(|c| (b.lo[c] - a.hi[c]).max(a.lo[c] - b.hi[c]).max(0)).max().unwrap_or(0);
                for sm in small {
                    let sb = bb(&sm);
                    let j = (0..large.len()).min_by_key(|&j| gap(&bb(&large[j]), &sb)).expect("large groups exist");
                    large[j].extend(sm);
                }
            }
            groups = stabilize(self, large);
        }
        let flat = |set: &[usize]| set.iter().flat_map(|&gi| groups[gi].iter().copied()).collect::<Vec<usize>>();
        let mut later: HashMap<i64, Vec<Vec<usize>>> = HashMap::new();
        let mut sets: Vec<Vec<usize>> = (0..groups.len()).map(|gi| vec![gi]).collect();
        for win in near + 1..self.plan_end() {
            let (end, o) = (self.boundary(win + 1), outer(self, win));
            let ents = sets.into_iter().map(|ids| {
                let (bbox, r) = boxof(&flat(&ids), end, o);
                Ent { ids, bbox, r }
            });
            sets = coalesce(ents.collect()).into_iter().map(|e| e.ids).collect();
            later.insert(win, sets.clone());
        }

        let owner: HashMap<u64, usize> =
            members.iter().enumerate().flat_map(|(mi, m)| self.regions[m].last.world.bodies.iter().map(move |b| (b.id, mi))).collect();
        let gbodies: Vec<Vec<usize>> = groups
            .iter()
            .map(|grp| {
                let mut v: Vec<usize> = grp.iter().flat_map(|&c| comps[c].iter().copied()).collect();
                v.sort_unstable();
                v
            })
            .collect();
        let gmembers: Vec<Vec<usize>> = gbodies
            .iter()
            .map(|b| {
                let mut m: Vec<usize> = b.iter().map(|&i| owner[&union.bodies[i].id]).collect();
                m.sort_unstable();
                m.dedup();
                m
            })
            .collect();
        let sizes: Vec<usize> = members.iter().map(|m| self.regions[m].last.world.bodies.len()).collect();
        let reuse: Vec<Option<usize>> = gbodies.iter().zip(&gmembers).map(|(b, m)| (m.len() == 1 && b.len() == sizes[m[0]]).then(|| m[0])).collect();
        let merged = gmembers.iter().any(|m| m.len() > 1);
        self.st.merges += merged as u64;
        self.st.splits += (0..members.len()).any(|mi| gmembers.iter().filter(|m| m.contains(&mi)).count() > 1) as u64;
        self.st.avoided += (members.len() > 1 && !merged) as u64;

        // New regions: whole bodies copied; each member's log, ops and wall ledger go to the
        // first group that draws from it, so lineage totals stay sums. A group is final only
        // as far as every member it draws from.
        let blank = shell(&union);
        let mut taken = vec![false; members.len()];
        let mut specs: Vec<Result<u64, (World, Log, u64, History, Tick, Tick)>> = Vec::with_capacity(groups.len());
        for (gi, b) in gbodies.iter().enumerate() {
            if let Some(mi) = reuse[gi] {
                specs.push(Ok(members[mi]));
                continue;
            }
            let bodies: Vec<Body> = b.iter().map(|&i| union.bodies[i].clone()).collect();
            let ids: HashSet<u64> = bodies.iter().map(|b| b.id).collect();
            let consumed = union.consumed.iter().filter(|c| ids.contains(&c.a) && ids.contains(&c.b)).copied().collect();
            let (mut log, mut ops, mut wall) = (Log::new(self.keep), 0u64, [0i64; 2]);
            for &mi in &gmembers[gi] {
                if !std::mem::replace(&mut taken[mi], true) {
                    let s = &self.regions[&members[mi]].last;
                    log.merge(&s.log);
                    ops += s.ops;
                    wall = [wall[0] + s.world.wall_momentum[0], wall[1] + s.world.wall_momentum[1]];
                }
            }
            let src = || gmembers[gi].iter().map(|&mi| &self.regions[&members[mi]]);
            let history = merged_history(src().map(|r| &r.history), tick);
            let fin = src().map(|r| r.fin).min().unwrap_or(tick);
            let hold = src().map(|r| r.no_split_until).max().unwrap_or(tick);
            specs.push(Err((World { bodies, consumed, wall_momentum: wall, ..blank.clone() }, log, ops, history, fin, hold)));
        }
        for (mi, m) in members.iter().enumerate() {
            if !reuse.contains(&Some(mi)) {
                self.regions.remove(m);
            }
        }
        let ids: Vec<u64> = specs
            .into_iter()
            .map(|s| match s {
                Ok(id) => id,
                Err((wd, lg, ops, h, fin, hold)) => {
                    let id = self.make_region(wd, lg, ops, h, fin);
                    self.regions.get_mut(&id).expect("made").no_split_until = hold;
                    id
                }
            })
            .collect();
        for (gi, &id) in ids.iter().enumerate() {
            if reuse[gi].is_none() {
                for &mi in &gmembers[gi] {
                    self.children.entry(members[mi]).or_default().push(id);
                }
            }
        }

        let mset: HashSet<u64> = members.iter().copied().collect();
        for win in w.max(self.plan_base)..self.plan_end() {
            let end = self.boundary(win + 1);
            let p = self.plan_mut(win);
            let ei = p.of[&members[0]];
            if p.ents[ei].ids.len() == members.len() && p.ents[ei].ids.iter().all(|i| mset.contains(i)) {
                let outer = p.ents[ei].bbox;
                p.ents.swap_remove(ei);
                let singles: Vec<Vec<usize>> = (0..groups.len()).map(|gi| vec![gi]).collect();
                for set in later.get(&win).unwrap_or(&singles) {
                    let (bbox, r) = boxof(&flat(set), end, Some(outer));
                    p.ents.push(Ent { ids: set.iter().map(|&gi| ids[gi]).collect(), bbox, r });
                }
            } else {
                let e = &mut p.ents[ei];
                e.ids.retain(|i| !mset.contains(i));
                e.ids.extend(&ids);
            }
            p.reindex();
        }
        self.dirty = true;
    }

    /// Every region id created (transitively) from `roots`, roots included.
    fn descendants(&self, roots: &[u64]) -> HashSet<u64> {
        let mut out: HashSet<u64> = roots.iter().copied().collect();
        let mut stack: Vec<u64> = roots.to_vec();
        while let Some(id) = stack.pop() {
            for &c in self.children.get(&id).into_iter().flatten() {
                if out.insert(c) {
                    stack.push(c);
                }
            }
        }
        out
    }

    /// Two isolated histories of window `j` came within reach: their joint history may differ.
    /// Only they are rolled back, to the window start s: every current region descending from
    /// the conflicting computations, plus every region sharing a snapshot with those at s
    /// (the bodies travelled together there). They restart as one region that recomputes the
    /// window jointly. Everything else keeps running: any later truth of the new region is
    /// checked against theirs in turn, so a real knock-on conflict rolls back lazily, window
    /// by window, only where it happens. Nothing published can be touched (asserted).
    fn rollback(&mut self, j: i64, owners: Vec<u64>) {
        self.st.rollbacks += 1;
        self.escalation *= 2.0;
        let s = self.boundary(j);
        let desc = self.descendants(&owners);
        let with: Vec<u64> = self.regions.values().filter(|r| r.entry(s).is_some()).map(|r| r.id).collect();
        for id in self.regions.keys().filter(|id| desc.contains(id)) {
            assert!(with.contains(id), "a conflicting lineage keeps its snapshot at the window start");
        }
        let mut uf = Uf::new(with.len());
        let mut first: HashMap<*const Snap, usize> = HashMap::new();
        for (i, id) in with.iter().enumerate() {
            for sn in self.regions[id].entry(s).expect("filtered") {
                let k = *first.entry(Arc::as_ptr(sn)).or_insert(i);
                uf.union(i, k);
            }
        }
        let seeds: HashSet<usize> = (0..with.len()).filter(|&i| desc.contains(&with[i])).map(|i| uf.find(i)).collect();
        let affected: Vec<u64> = (0..with.len()).filter(|&i| seeds.contains(&uf.find(i))).map(|i| with[i]).collect();
        assert!(!affected.is_empty(), "a conflict names live lineages");
        for id in &affected {
            assert!(self.regions[id].fin <= s, "rollback of region {id} to {s} would revise its published tick {}", self.regions[id].fin);
        }
        let mut snaps: Vec<Arc<Snap>> = Vec::new();
        for id in &affected {
            self.regions[id].entry(s).expect("affected regions hold s").iter().for_each(|sn| push_unique(&mut snaps, sn));
        }
        let dead = self.descendants(&snaps.iter().map(|sn| sn.owner).chain(owners.iter().copied()).collect::<Vec<_>>());
        for list in self.truths.range_mut(j..).map(|(_, l)| l) {
            list.retain(|t| !dead.contains(&t.id));
        }
        let history = merged_history(affected.iter().map(|id| &self.regions[id].history), s);
        let fin = affected.iter().map(|id| self.regions[id].fin).min().expect("non-empty");
        let spent: u64 = affected.iter().map(|id| self.regions[id].ops()).sum();
        let ops: u64 = snaps.iter().map(|sn| sn.ops).sum();
        let world = union_of(&snaps.iter().map(|sn| &sn.world).collect::<Vec<_>>());
        let mut log = Log::new(self.keep);
        snaps.iter().for_each(|sn| log.merge(&sn.log));
        self.st.wasted += spent.saturating_sub(ops);
        self.st.rolled_regions += affected.len() as u64;
        let depth = affected.iter().map(|id| self.regions[id].tick - s).max().unwrap_or(0);
        self.st.rollback_depth.push(depth as f64);
        for id in &affected {
            self.regions.remove(id);
        }
        let rid = self.make_region(world, log, ops, history, fin);
        self.regions.get_mut(&rid).expect("made").no_split_until = self.boundary(j + 1 + self.cfg.split_lookahead.max(0));
        for &id in affected.iter().chain(owners.iter()) {
            self.children.entry(id).or_default().push(rid);
        }
        // Plans: forget regions that no longer exist; the restored region stands alone from j.
        for pw in self.plan_base..self.plan_end() {
            let end = self.boundary(pw + 1);
            let (bbox, r) = (self.regions[&rid].model.at(end), self.regions[&rid].rmax);
            let live = |id: &u64| self.regions.contains_key(id) && *id != rid;
            let mut ents: Vec<Ent<u64>> = self.plans[(pw - self.plan_base) as usize]
                .ents
                .iter()
                .map(|e| Ent { ids: e.ids.iter().copied().filter(live).collect(), bbox: e.bbox, r: e.r })
                .filter(|e| !e.ids.is_empty())
                .collect();
            if pw >= j {
                ents.push(Ent { ids: vec![rid], bbox, r });
            }
            self.plans[(pw - self.plan_base) as usize] = Plan::new(ents);
        }
        self.dirty = true;
    }

    /// Finality. The global all-verified tick is final: every pair of isolated histories up to
    /// it has been compared, and conflicts can only arise in later windows. With a law-given
    /// hard speed v, a region is final further, through t, if no unfinished history can reach
    /// it by t: every region whose final tick f is before t may still change anything within
    /// its bodies' box at f grown by v·(t − f) (all computations start from final states and
    /// no body outruns v); merges planned by t and certificate hulls are closed over by
    /// coalescing those boxes; the region is final if it stays alone.
    fn finalize(&mut self) {
        let front = self.frontier();
        for r in self.regions.values_mut() {
            r.fin = r.fin.max(front);
        }
        let Some(v) = self.lightcone else { return };
        for _round in 0..8 {
            let base: Vec<(u64, Tick, Aabb, i64)> = self
                .regions
                .values()
                .map(|r| {
                    let snaps = r.entry(r.fin).expect("a region keeps its final snapshot");
                    let x = snaps.iter().fold(Aabb::EMPTY, |b, s| b.hull(&s.bbox));
                    (r.id, r.fin, x, snaps.iter().map(|s| s.rmax).max().unwrap_or(0))
                })
                .collect();
            let mut changed = false;
            let ids: Vec<u64> = self.regions.keys().copied().collect();
            for id in ids {
                let r = &self.regions[&id];
                let cands: Vec<Tick> = r.history.iter().map(|(t, _)| *t).filter(|&t| t > r.fin && t <= r.verified).collect();
                let (mut lo, mut hi, mut best) = (0usize, cands.len(), None);
                while lo < hi {
                    let mid = (lo + hi) / 2;
                    if self.final_through(id, cands[mid], &base, v) {
                        best = Some(cands[mid]);
                        lo = mid + 1;
                    } else {
                        hi = mid;
                    }
                }
                if let Some(t) = best {
                    self.regions.get_mut(&id).expect("listed").fin = t;
                    changed = true;
                }
            }
            if !changed {
                return;
            }
        }
    }

    fn final_through(&self, id: u64, t: Tick, base: &[(u64, Tick, Aabb, i64)], v: i64) -> bool {
        let pw = self.window(t - 1);
        let plan = self.has_plan(pw).then(|| self.plan(pw));
        let mut groups: HashMap<(bool, u64), Ent<u64>> = HashMap::new();
        for &(rid, fin, x, r) in base {
            if fin >= t {
                continue;
            }
            let g = x.grow(v.saturating_mul(t - fin));
            let key = plan.and_then(|p| p.of.get(&rid)).map_or((false, rid), |&e| (true, e as u64));
            let e = groups.entry(key).or_insert(Ent { ids: vec![], bbox: Aabb::EMPTY, r: 0 });
            e.ids.push(rid);
            e.bbox = e.bbox.hull(&g);
            e.r = e.r.max(r);
        }
        coalesce(groups.into_values().collect()).iter().find(|e| e.ids.contains(&id)).is_none_or(|e| e.ids.len() == 1)
    }

    fn finished(&self) -> bool {
        match self.goal {
            Goal::Batch(t) => self.regions.values().all(|r| !r.busy && r.verified == t),
            Goal::Frames { .. } => false,
        }
    }

    /// Final snapshots only. Regions that share a snapshot share their final tick (their boxes
    /// at it overlap, so neither can be final past the other), so each body appears once.
    fn view(&self) -> View {
        let mut parts: Vec<Arc<Snap>> = Vec::new();
        for r in self.regions.values() {
            r.entry(r.fin).expect("a region keeps its final snapshot").iter().for_each(|s| push_unique(&mut parts, s));
        }
        assert_eq!(parts.iter().map(|p| p.world.bodies.len()).sum::<usize>(), self.bodies, "a view holds every body once");
        View { parts, frontier: self.frontier() }
    }

    fn reset_stats(&mut self) {
        self.st = Stats { regions_initial: self.regions.len(), regions_max: self.regions.len(), ..Stats::default() };
    }
}

fn execute<S: Stepper>(mut job: Job<S>) -> Done<S> {
    let ops0 = job.stepper.metrics().ops;
    let t = Instant::now();
    let tick = job.stepper.advance(job.target, job.budget);
    let advance_secs = t.elapsed().as_secs_f64();
    assert!(tick > job.tick0 && tick <= job.target, "a unit advances without passing its target ({} → {tick}, target {})", job.tick0, job.target);
    let t = Instant::now();
    let end = (tick == job.target).then(|| {
        let world = job.stepper.world();
        let bbox = Aabb::of(world.bodies.iter().map(|b| &b.x));
        let comps = job.split_extra.map(|x| islands(&world, x, job.min_region));
        (world, bbox, comps)
    });
    Done {
        id: job.id,
        tick,
        tick0: job.tick0,
        ops: job.stepper.metrics().ops - ops0,
        budget: job.budget,
        advance_secs,
        measure_secs: t.elapsed().as_secs_f64(),
        feat: job.feat,
        predicted: job.predicted,
        end,
        stepper: job.stepper,
    }
}

struct Shared<S> {
    state: Mutex<State<S>>,
    work: Condvar,
    done: Condvar,
    view: Mutex<Arc<View>>,
    present: AtomicU64,
    queue_depth: AtomicUsize,
}

impl<S: Stepper + Send + 'static> Shared<S> {
    /// O(1) for the reader: the frame clones one Arc; workers settle finality, build the view
    /// and swap it.
    fn publish(&self, g: &mut MutexGuard<State<S>>) {
        if g.dirty {
            g.dirty = false;
            g.finalize();
            let v = Arc::new(g.view());
            let old = std::mem::replace(&mut *self.view.lock().unwrap(), v);
            drop(old);
        }
    }
}

fn worker<S: Stepper + Send + 'static>(sh: Arc<Shared<S>>, class: Class) -> WorkerReport {
    let qos_accepted = qos::set_current(class);
    let start = Instant::now();
    let (mut busy, mut units, mut ops) = (0.0, 0u64, 0u64);
    let mut g = sh.state.lock().unwrap();
    while g.running {
        let present = f64::from_bits(sh.present.load(Relaxed));
        let pick = g.pick(class, present, &sh.queue_depth);
        sh.publish(&mut g);
        let declined = match pick {
            Pick::Run(job) => {
                drop(g);
                let t = Instant::now();
                let done = execute(job);
                let secs = t.elapsed().as_secs_f64();
                busy += secs;
                units += 1;
                ops += done.ops;
                let t = Instant::now();
                g = sh.state.lock().unwrap();
                g.st.lock_ms.push(t.elapsed().as_secs_f64() * 1e3);
                g.commit(done, secs, class);
                sh.publish(&mut g);
                sh.work.notify_all();
                continue;
            }
            Pick::Idle => false,
            Pick::Decline => true,
        };
        if g.finished() {
            sh.done.notify_all();
        }
        if declined {
            sh.work.notify_all();
        }
        let p = class == Class::Performance;
        g.idle_p += p as usize;
        g = sh.work.wait_timeout(g, Duration::from_millis(2)).unwrap().0;
        g.idle_p -= p as usize;
    }
    let wall = start.elapsed().as_secs_f64().max(1e-9);
    WorkerReport { class, qos_accepted, units, ops, busy_seconds: busy, utilisation: busy / wall }
}

/// The allocator over one scene. Generic over the stepper: every region runs the same mode.
pub struct Allocator<S> {
    sh: Arc<Shared<S>>,
    drawn: Vec<Arc<Snap>>,
}

impl<S: Stepper + Send + 'static> Allocator<S> {
    /// A scene from one or more worlds at one tick with disjoint ids. Containerless scenes are
    /// cut into islands; a world with a container stays one region (and must be alone).
    pub fn new(worlds: Vec<World>, factory: Factory<S>, cfg: Config) -> Result<Self, String> {
        let first = worlds.first().ok_or("a scene needs a world")?;
        if worlds.iter().any(|w| w.container.is_some()) && worlds.len() > 1 {
            return Err("a world with a container cannot share a scene: its walls would not bound the others".into());
        }
        if cfg.window < 1 || cfg.p_workers + cfg.e_workers == 0 {
            return Err("window ≥ 1 and at least one worker".into());
        }
        let union = union_of(&worlds.iter().collect::<Vec<_>>());
        union.validate().map_err(|e| format!("scene: {e} (ids must be disjoint across worlds)"))?;
        if let Some(v) = cfg.hard_speed {
            let m = vmax(union.bodies.iter());
            if m > v {
                return Err(format!("hard speed {v} below a genesis speed {m}"));
            }
        }
        let (t0, q, bodies, closed) = (first.tick, first.q, union.bodies.len(), first.container.is_some());
        let st = State {
            sabotage: cfg.sabotage.map(|s| Sabotage(Rng(s))),
            lightcone: cfg.hard_speed,
            cfg,
            factory,
            t0,
            q,
            bodies,
            closed,
            keep: false,
            regions: BTreeMap::new(),
            next_id: 1,
            plan_base: 0,
            plans: VecDeque::new(),
            truths: BTreeMap::new(),
            children: HashMap::new(),
            goal: Goal::Batch(t0),
            escalation: 1.0,
            cost: CostModel::default(),
            spo: [30e-9, 60e-9],
            st: Stats::default(),
            idle_p: 0,
            running: false,
            dirty: true,
        };
        let sh = Arc::new(Shared {
            state: Mutex::new(st),
            work: Condvar::new(),
            done: Condvar::new(),
            view: Mutex::new(Arc::new(View::default())),
            present: AtomicU64::new((t0 as f64).to_bits()),
            queue_depth: AtomicUsize::new(0),
        });
        {
            let mut g = sh.state.lock().unwrap();
            let id = g.make_region(union, Log::new(false), 0, History::new(), t0);
            if !closed {
                g.regroup(vec![id], None);
            }
            sh.publish(&mut g);
        }
        Ok(Allocator { sh, drawn: Vec::new() })
    }

    fn spawn(&self) -> Vec<JoinHandle<WorkerReport>> {
        let (p, e) = {
            let g = self.sh.state.lock().unwrap();
            (g.cfg.p_workers, g.cfg.e_workers)
        };
        (0..p + e)
            .map(|i| {
                let sh = self.sh.clone();
                let class = if i < p { Class::Performance } else { Class::Efficiency };
                thread::Builder::new().name(format!("alloc-{i}")).spawn(move || worker(sh, class)).expect("spawn worker")
            })
            .collect()
    }

    fn stop(&self, hs: Vec<JoinHandle<WorkerReport>>) -> Vec<WorkerReport> {
        self.sh.state.lock().unwrap().running = false;
        self.sh.work.notify_all();
        hs.into_iter().map(|h| h.join().expect("worker panicked")).collect()
    }

    /// Batch: advance every region to `target`, certified, then stop the workers.
    pub fn run_to(&mut self, target: Tick) -> Report {
        let p0 = {
            let mut g = self.sh.state.lock().unwrap();
            assert!(g.regions.values().all(|r| r.verified <= target), "target behind the scene");
            g.goal = Goal::Batch(target);
            g.running = true;
            g.reset_stats();
            g.frontier() as f64
        };
        let t = Instant::now();
        let hs = self.spawn();
        {
            let mut g = self.sh.state.lock().unwrap();
            while !g.finished() {
                // A worker that panicked outside the lock leaves its region busy forever.
                assert!(!hs.iter().any(|h| h.is_finished()), "a worker stopped early");
                g = self.sh.done.wait_timeout(g, Duration::from_millis(20)).unwrap().0;
            }
            g.dirty = true;
            self.sh.publish(&mut g);
        }
        let workers = self.stop(hs);
        self.report("batch", t.elapsed().as_secs_f64(), workers, None, p0, target as f64)
    }

    /// Frame harness: this thread is the frame thread. It never simulates and never waits:
    /// each frame reads the published view (one pointer; if a worker is mid-swap, the previous
    /// frame's), which holds only final states. The player's present advances by `rate`·dt
    /// unless some part's final tick plus its light delay is behind (then time acceleration
    /// drops, never the frame rate). Workers compute ahead up to `ahead_seconds` of present
    /// in least-slack order; that work stays invisible until final.
    pub fn run_frames(&mut self, fc: &FrameConfig) -> Report {
        let (p0, obs, q, view_r) = {
            let mut g = self.sh.state.lock().unwrap();
            g.goal = Goal::Frames { rate: fc.rate, ahead: fc.ahead_seconds };
            g.running = true;
            g.reset_stats();
            (g.frontier() as f64, g.cfg.observer, g.q as f64, g.cfg.view_radius as f64)
        };
        self.sh.present.store(p0.to_bits(), Relaxed);
        qos::set_current(Class::Performance);
        let hs = self.spawn();
        let period = Duration::from_secs_f64(1.0 / fc.hz);
        let start = Instant::now();
        let (mut last, mut next, mut p) = (start, start + period, p0);
        let mut fr = FrameReport { hz: fc.hz, target_rate: fc.rate, ..Default::default() };
        let (mut work, mut interval, mut buffer, mut queue, mut lead) = (vec![], vec![], vec![], vec![], vec![]);
        let mut view = self.sh.view.lock().unwrap().clone();
        let mut seen: HashSet<*const Snap> = HashSet::new();
        while start.elapsed().as_secs_f64() < fc.seconds {
            let now = Instant::now();
            let dt = (now - last).as_secs_f64().min(4.0 / fc.hz);
            if fr.frames > 0 {
                interval.push((now - last).as_secs_f64() * 1e3);
            }
            last = now;
            if let Ok(v) = self.sh.view.try_lock() {
                view = v.clone();
            }
            let want = p + fc.rate * dt;
            let (mut bound, mut visible, mut ahead) = (f64::INFINITY, 0usize, 0.0f64);
            for part in &view.parts {
                let dist = (part.bbox.distance(obs) - part.rmax as f64).max(0.0);
                let b = part.tick as f64 + dist / q;
                fr.deadline_misses += (b < want) as u64;
                bound = bound.min(b);
                ahead = ahead.max((part.tick - view.frontier) as f64);
                if dist <= view_r {
                    let r2 = view_r * view_r;
                    visible += part.world.bodies.iter().filter(|b| ((b.x[0] - obs[0]) as f64).powi(2) + ((b.x[1] - obs[1]) as f64).powi(2) <= r2).count();
                }
                if fc.record && seen.insert(Arc::as_ptr(part)) {
                    self.drawn.push(part.clone());
                }
            }
            let np = want.min(bound).max(p);
            fr.acceleration_drops += (np < want) as u64;
            p = np;
            buffer.push(bound - p);
            lead.push(ahead);
            fr.visible_bodies_last = visible;
            self.sh.present.store(p.to_bits(), Relaxed);
            self.sh.work.notify_all();
            queue.push(self.sh.queue_depth.load(Relaxed) as f64);
            fr.frames += 1;
            work.push(now.elapsed().as_secs_f64() * 1e3);
            let after = Instant::now();
            if next > after {
                thread::sleep(next - after);
            }
            next += period;
            if next < Instant::now() {
                next = Instant::now() + period;
            }
        }
        let wall = start.elapsed().as_secs_f64();
        let workers = self.stop(hs);
        fr.work_ms = pcts(&work);
        fr.interval_ms = pcts(&interval);
        fr.buffer_chronons = pcts(&buffer);
        fr.final_lead_chronons = pcts(&lead);
        fr.queue_depth = pcts(&queue);
        self.report("frames", wall, workers, Some(fr), p0, p)
    }

    /// Every distinct snapshot frames drew while recording (see [`FrameConfig::record`]).
    pub fn drawn(&mut self) -> Vec<Arc<Snap>> {
        std::mem::take(&mut self.drawn)
    }

    fn report(&self, mode: &str, wall: f64, workers: Vec<WorkerReport>, frames: Option<FrameReport>, p0: f64, p1: f64) -> Report {
        let g = self.sh.state.lock().unwrap();
        let s = &g.st;
        let v_inf = g.regions.values().map(|r| r.model.v).max().unwrap_or(0).max(g.q) as f64;
        let region_list = g
            .regions
            .values()
            .map(|r| RegionReport {
                id: r.id,
                bodies: r.last.world.bodies.len(),
                verified: r.verified,
                final_tick: r.fin,
                light_delay: g.delay(&r.bbox, r.rmax),
                speed_bound_c: r.model.v as f64 / g.q as f64,
                speculation_horizon: speculation_horizon(&r.bbox, r.rmax, r.model.v, r.model.tick, g.cfg.observer, p1, v_inf),
            })
            .collect();
        Report {
            mode: mode.into(),
            stepper: std::any::type_name::<S>().into(),
            wall_seconds: wall,
            bodies: g.bodies,
            window: g.cfg.window,
            finality: FinalityReport {
                light_cone: g.cfg.hard_speed.is_some() && g.lightcone.is_some(),
                hard_speed: g.cfg.hard_speed,
                hard_speed_violations: s.hard_speed_violations,
                frontier: g.frontier(),
            },
            regions: RegionsReport {
                initial: s.regions_initial,
                last: g.regions.len(),
                max: s.regions_max,
                merges: s.merges,
                splits: s.splits,
                merges_avoided: s.avoided,
                promises_exceeded: s.exceeded,
                rollbacks: s.rollbacks,
                rolled_back_regions: s.rolled_regions,
                rollback_depth_chronons: pcts(&s.rollback_depth),
                accepted_windows: s.accepted,
                wasted_ops: s.wasted,
                speed_escalation: g.escalation,
            },
            workers,
            units: UnitsReport {
                count: s.units,
                ms: pcts(&s.unit_ms),
                ms_performance: pcts(&s.unit_ms_class[0]),
                ms_efficiency: pcts(&s.unit_ms_class[1]),
                stepper_advance_ms: pcts(&s.advance_ms),
                allocator_measure_ms: pcts(&s.measure_ms),
                lock_wait_ms: pcts(&s.lock_ms),
                ops: pcts(&s.unit_ops),
                over_budget_units: s.over_ops.len() as u64,
                over_budget_ops: pcts(&s.over_ops),
                max_ops_over_budget_ratio: s.over_ratio_max,
                stepper_max_unit_ops: s.stepper_max_unit_ops,
                budget_performance: g.cfg.fixed_budget.unwrap_or((g.cfg.unit_seconds / g.spo[0]) as u64),
                budget_efficiency: g.cfg.fixed_budget.unwrap_or((g.cfg.unit_seconds / g.spo[1]) as u64),
            },
            queue_depth: pcts(&s.queue),
            sim: SimReport {
                region_chronons: s.chronons,
                region_chronons_per_wall_second: s.chronons as f64 / wall,
                present_start: p0,
                present_end: p1,
                present_chronons_per_wall_second: (p1 - p0) / wall,
            },
            forecast: ForecastReport {
                sabotage: g.sabotage.is_some(),
                k_bodies: g.cost.k[0],
                k_contacts: g.cost.k[1],
                ns_per_op_performance: g.spo[0] * 1e9,
                ns_per_op_efficiency: g.spo[1] * 1e9,
                abs_log2_error: pcts(&s.err),
            },
            frames,
            region_list,
        }
    }

    /// Union of every region's accepted world. Canonical only when all regions share a tick
    /// (after [`Allocator::run_to`]).
    pub fn world(&self) -> World {
        let g = self.sh.state.lock().unwrap();
        union_of(&g.regions.values().map(|r| &r.last.world).collect::<Vec<_>>())
    }

    /// Merged event log of every lineage (logs merge by addition in any order).
    pub fn log(&self) -> Log {
        let g = self.sh.state.lock().unwrap();
        let mut log = Log::new(g.keep);
        g.regions.values().for_each(|r| log.merge(&r.last.log));
        log
    }

    /// World digest of the union and merged log digest: must equal one stepper over the scene.
    pub fn outcome(&self) -> (String, String) {
        (self.world().digest(), self.log().digest())
    }

    pub fn regions(&self) -> usize {
        self.sh.state.lock().unwrap().regions.len()
    }

    /// The latest published view (what a frame would draw).
    pub fn view(&self) -> Arc<View> {
        self.sh.view.lock().unwrap().clone()
    }
}

/// Step-6 safety primitive. The player's influence spreads from `observer` at `v_inf` (1/Q
/// units per chronon: c, or the tracked maximum speed when evolved speeds exceed it); the
/// region's box grows at `v` per axis from its anchor, so its distance to a point shrinks at
/// most √2·v per chronon. Up to the returned tick the region cannot feel anything the player
/// does from `present` on, so computing it that far ahead carries no rollback risk from the
/// player (its own speed forecast is still measured by the certificate).
pub fn speculation_horizon(bbox: &Aabb, rmax: i64, v: i64, anchor: Tick, observer: [i64; 2], present: f64, v_inf: f64) -> f64 {
    let d0 = bbox.distance(observer) - rmax as f64;
    if d0 <= 0.0 {
        return present;
    }
    let vr = std::f64::consts::SQRT_2 * v as f64;
    ((d0 + vr * anchor as f64 + v_inf * present) / (vr + v_inf)).max(present)
}
