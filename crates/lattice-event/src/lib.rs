//! Event mode for `es-lattice-elastic-v0` (step 1 of docs/work-allocation-design.md §3, §7).
//!
//! [`EventCore`] reproduces [`emergent_lattice::chronon::Chronon`] bit for bit (world and log
//! digests, every budget slicing) while touching only bodies that have something to do.
//!
//! - **State.** A body is stored as (x0, k, t0): its position at t is x0 + k·(t − t0), exact,
//!   so quiet bodies are never advanced. What a neighbour visit reads (motion, radius,
//!   revision, cell link, consumed-list head) sits in one 64-byte line.
//! - **Frames.** Cells live in frames. Frame 0 is the rest frame. Velocities shared by at
//!   least [`CLASS_MIN`] bodies (up to [`MAX_CLASSES`], found by a bounded sketch at each
//!   rebuild) get a co-moving frame whose cells
//!   hold its members at y = x − u·(t − t_ref), which never changes while they keep velocity
//!   u. Two members never hit (zero relative velocity), so a class costs nothing inside
//!   itself; other bodies only cross its cells at their relative velocity, and only while
//!   their path is inside its bounding box. A member whose velocity changes moves to frame 0.
//! - **Cells.** Uniform grids (a dense array over the frame's formation box, a small hash map
//!   for cells bodies drift to) of side L ≥ reach_max + 2·kcap with every |k_c| ≤ kcap: a
//!   pair hitting in bin t has |d_c(t−1)| ≤ reach + |w_c| ≤ L in any frame, so it sits in
//!   adjacent cells. A response past kcap (the elastic tail past c) grows every grid; c is
//!   never assumed. Frame 0's L starts at sqrt(area per body) and follows density by cost
//!   feedback: over each window of n predictions it counts crossing- and event-triggered
//!   predictions and their neighbours, models 2L and L/2 (crossings ∝ 1/L, neighbours ∝ L²)
//!   and rescales when that saves 30%. A dispersing world grows its cells as it spreads, and
//!   frame 0 is re-formed around bodies that drifted out of its dense box.
//! - **Calendar.** An indexed heap, one slot per body at min(e_hit, e_cross): its earliest
//!   exact pair hit ([`law::first_hit`]) or wall ([`law::first_wall`]), and its next cell
//!   change or class-box entry. Replacing a slot is the invalidation; nothing goes stale.
//!
//! **Completeness (one-sided coverage).** Each pair that could hit has a covering body:
//! either one of two rest bodies (both scan frame 0), the rest body for (rest, member), the
//! lower class for two classes. The coverer's e_hit is ≤ the pair's next hit: it
//! re-predicts over all it covers whenever its velocity, revision, consumed set or cells
//! change, and a partner's change re-predicts the partner, which then covers the pair from
//! its side or leaves a stale slot that only costs a spurious wake-up. So every pair
//! hitting in bin t has a coverer with e_hit = t, and scanning those candidates with
//! [`law::hit`] finds exactly the set Chronon tests.
//!
//! **Batch rule.** All events at tick t form one batch: pairs sorted by index, bodies by id,
//! resolved per connected component (the contract's locality licence: same bits as the
//! whole batch), every pair consumed at the new revisions, then only touched bodies are
//! re-indexed and re-predicted.
//!
//! **Bounded units.** [`Stepper::advance`] runs resumable steps: one calendar pop, one
//! candidate scan, one component response, one body re-index or prediction, one body or
//! 4096 dense cells of a rebuild. The calendar is allocated once (n slots), cell arrays at
//! formation and filled in chunks, the sparse cell map and consumed arena are reserved and
//! a rebuild re-forms rather than rehash; batch buffers never outgrow the largest batch. So
//! no step reallocates or rehashes O(n) data (measured: the worst unit's own CPU time).
//! Overshoot: less than one step, at most max(one neighbourhood per frame + 8, 6 × batch)
//! ops: the batch terms are the component labelling and the publish, atomic so
//! [`Stepper::world`] and the log agree with [`Stepper::tick`], and one component's
//! response (the law's response is indivisible).
//!
//! **Metrics.** `ops` charges 1 per neighbourhood lookup, neighbour visited (a predicate or
//! a consumed-pair skip), wall predicate, crossing or entry time, calendar update and pop,
//! re-index check, cell unlink and link, rebuild sketch step (2) and box step, 64 dense
//! cells initialised, body in a response,
//! resolved pair, consumed entry kept or pruned, and published body, pair or wall.
//! `predicates` counts exact pair and wall predicates only.
use emergent_lattice::law::{self, Body, Consumed, Response, Tick, World};
use emergent_lattice::{Event, Kind, Log, Metrics, Stepper};
use std::collections::HashMap;
use std::hash::{BuildHasherDefault, Hasher};

const NEVER: Tick = Tick::MAX;
const NONE: u32 = u32::MAX;
const REST: usize = 0;
const UNHOMED: u8 = u8::MAX;
/// Initial cell side in units of sqrt(area per body), before feedback.
pub const DENSITY_FACTOR: f64 = 1.0;
/// Smallest velocity class that gets a co-moving frame.
pub const CLASS_MIN: u32 = 64;
pub const MAX_CLASSES: usize = 8;
/// Counters of the velocity sketch (Misra–Gries): every velocity shared by more than
/// n/(SKETCH + 1) bodies is found, in O(SKETCH) memory; a missed smaller class only costs
/// speed, never correctness. Each body costs one scan of the counters (charged 2 ops).
const SKETCH: usize = 64;
/// Dense cells initialised per rebuild step.
const FILL_CHUNK: usize = 4096;
/// Fixed ops of one prediction besides its neighbours (pop, re-index, lookup, crossing,
/// wall, calendar): the cost model of the density feedback.
const PREDICT_OPS: f64 = 8.0;
/// Rescale only for at least this saving, so the O(n) rebuild pays for itself.
const RESCALE_GAIN: f64 = 0.7;

/// Multiplicative hash (Fx) with a final fold: keys are small integer tuples, and the crate
/// takes no dependencies beyond the contract.
#[derive(Default)]
struct Fx(u64);

impl Fx {
    #[inline]
    fn add(&mut self, v: u64) {
        self.0 = (self.0.rotate_left(5) ^ v).wrapping_mul(0x51_7c_c1_b7_27_22_0a_95);
    }
}

impl Hasher for Fx {
    fn write(&mut self, bytes: &[u8]) {
        for &b in bytes {
            self.add(b as u64);
        }
    }
    fn write_u64(&mut self, v: u64) {
        self.add(v)
    }
    fn write_i64(&mut self, v: i64) {
        self.add(v as u64)
    }
    fn finish(&self) -> u64 {
        self.0 ^ (self.0 >> 29)
    }
}

type Map<K, V> = HashMap<K, V, BuildHasherDefault<Fx>>;

fn map_with<K, V>(n: usize) -> Map<K, V> {
    Map::with_capacity_and_hasher(n, Default::default())
}

fn kinf(k: [i64; 2]) -> i64 {
    k[0].abs().max(k[1].abs())
}

/// Everything a neighbour visit reads, in one cache line: the motion (position `x` at `t0`,
/// velocity `k`), radius, revision, the cell-list link, the consumed-list head and the
/// candidate epoch. Canonical x, k and rev live here; [`Body`] keeps the rest.
#[derive(Clone, Copy)]
#[repr(C, align(64))]
struct Hot {
    x: [i64; 2],
    k: [i64; 2],
    t0: Tick,
    radius: i64,
    rev: u32,
    /// Next body in the same cell.
    next: u32,
    /// First consumed entry stored at this body (the lower index of its pairs).
    cons: u32,
    /// Epoch of the batch in which it is a candidate (or, after labelling, involved).
    cand: u32,
}

impl Hot {
    #[inline]
    fn at(&self, t: Tick) -> [i64; 2] {
        let dt = t - self.t0;
        [self.x[0] + self.k[0] * dt, self.x[1] + self.k[1] * dt]
    }
}

/// A consumed contact (a, b) stored in a's list: b and both revisions at consumption.
#[derive(Clone, Copy)]
struct Cons {
    b: u32,
    ra: u32,
    rb: u32,
    next: u32,
}

/// Ticks until floor(y/side) changes for y moving at v (y inside `cell`), from t.
fn cross_time(y: [i64; 2], v: [i64; 2], cell: [i64; 2], side: i64, t: Tick) -> Tick {
    let mut e = NEVER;
    for c in 0..2 {
        if v[c] != 0 {
            // floor(y/L) changes when y reaches lo + L moving up, lo − 1 moving down. The gap
            // is at most L and |v| ≤ 2^23: i64 (a software i128 division was a hot spot).
            let lo = cell[c] * side;
            let gap = if v[c] > 0 { lo + side - y[c] } else { y[c] - lo + 1 };
            let w = v[c].abs();
            e = e.min(t.saturating_add((gap + w - 1) / w));
        }
    }
    e
}

/// Smallest s ≥ 1 with y + v·s inside [lo, hi] (inclusive), if any.
fn entry_time(y: [i64; 2], v: [i64; 2], lo: [i64; 2], hi: [i64; 2]) -> Option<i64> {
    let (mut a, mut b) = (1i128, i128::MAX);
    for c in 0..2 {
        let (y, v, lo, hi) = (y[c] as i128, v[c] as i128, lo[c] as i128, hi[c] as i128);
        if v == 0 {
            if y < lo || y > hi {
                return None;
            }
            continue;
        }
        let (d0, d1, w) = if v > 0 { (lo - y, hi - y, v) } else { (y - hi, y - lo, -v) };
        a = a.max(-(-d0).div_euclid(w));
        b = b.min(d1.div_euclid(w));
    }
    (a <= b).then(|| i64::try_from(a).unwrap_or(NEVER))
}

/// Indexed 4-ary heap of (time, body) with one slot per body: the calendar never holds
/// stale entries and never grows past n, so it is allocated once. Keys are inline and the
/// four children of a node share a cache line: re-predictions mostly move a slot later, and
/// that sift-down dominated the calendar's cost at a million bodies.
struct Calendar {
    heap: Vec<(Tick, u32)>,
    pos: Vec<u32>,
}

const ARITY: usize = 4;

impl Calendar {
    fn new(n: usize) -> Self {
        Calendar { heap: Vec::with_capacity(n), pos: vec![NONE; n] }
    }

    #[inline]
    fn place(&mut self, p: usize, x: (Tick, u32)) {
        self.heap[p] = x;
        self.pos[x.1 as usize] = p as u32;
    }

    fn up(&mut self, mut p: usize) {
        let x = self.heap[p];
        while p > 0 {
            let q = (p - 1) / ARITY;
            if x >= self.heap[q] {
                break;
            }
            self.place(p, self.heap[q]);
            p = q;
        }
        self.place(p, x);
    }

    fn down(&mut self, mut p: usize) {
        let (x, n) = (self.heap[p], self.heap.len());
        loop {
            let first = ARITY * p + 1;
            if first >= n {
                break;
            }
            let mut c = first;
            for k in first + 1..(first + ARITY).min(n) {
                if self.heap[k] < self.heap[c] {
                    c = k;
                }
            }
            if self.heap[c] >= x {
                break;
            }
            self.place(p, self.heap[c]);
            p = c;
        }
        self.place(p, x);
    }

    fn remove_at(&mut self, p: usize) {
        self.pos[self.heap[p].1 as usize] = NONE;
        let last = self.heap.pop().expect("non-empty");
        if p < self.heap.len() {
            self.place(p, last);
            self.up(p);
            self.down(self.pos[last.1 as usize] as usize);
        }
    }

    /// Set body i's slot; returns whether a live prediction was replaced.
    fn set(&mut self, i: usize, t: Tick) -> bool {
        let p = self.pos[i];
        if p == NONE {
            if t != NEVER {
                self.heap.push((t, i as u32));
                self.up(self.heap.len() - 1);
            }
            return false;
        }
        let p = p as usize;
        if t == NEVER {
            self.remove_at(p);
        } else {
            let old = self.heap[p].0;
            self.heap[p].0 = t;
            if t < old {
                self.up(p);
            } else {
                self.down(p);
            }
        }
        true
    }

    fn peek(&self) -> Option<(Tick, usize)> {
        self.heap.first().map(|&(t, i)| (t, i as usize))
    }

    fn pop(&mut self) {
        self.remove_at(0);
    }
}

/// Cell → head of an intrusive list through [`Hot::next`]/[`Sched::prev`], so moving a body
/// allocates nothing. Cells of the frame's formation box are a dense array (one load, 4
/// bytes a cell, allocated once); cells outside it, where bodies drift, a small hash map.
struct Grid {
    lo: [i64; 2],
    dim: [i64; 2],
    dense: Vec<u32>,
    sparse: Map<[i64; 2], u32>,
    /// Sparse cells it can hold without rehashing.
    reserve: usize,
    occupied: usize,
}

impl Grid {
    /// Dense over cells [lo, hi] unless that exceeds `max_cells`; the sparse map reserves
    /// `drift` cells, or all `bodies` when there is no dense part.
    fn new(lo: [i64; 2], hi: [i64; 2], max_cells: usize, drift: usize, bodies: usize) -> Self {
        let dim = [hi[0] - lo[0] + 1, hi[1] - lo[1] + 1];
        let fits = dim[0] > 0 && dim[1] > 0 && (dim[0] as u128 * dim[1] as u128) <= max_cells as u128;
        let (dim, cells, reserve) = if fits { (dim, (dim[0] * dim[1]) as usize, drift) } else { ([0, 0], 0, bodies + 64) };
        // The dense cells are initialised by the rebuild's Fill phase, in bounded chunks.
        Grid { lo, dim, dense: Vec::with_capacity(cells), sparse: map_with(reserve), reserve, occupied: 0 }
    }

    #[inline]
    fn slot(&self, c: [i64; 2]) -> Option<usize> {
        let (x, y) = (c[0].wrapping_sub(self.lo[0]), c[1].wrapping_sub(self.lo[1]));
        ((x as u64) < self.dim[0] as u64 && (y as u64) < self.dim[1] as u64).then(|| (y * self.dim[0] + x) as usize)
    }

    #[inline]
    fn head(&self, c: [i64; 2]) -> u32 {
        match self.slot(c) {
            Some(s) => self.dense[s],
            None => self.sparse.get(&c).copied().unwrap_or(NONE),
        }
    }

    fn set_head(&mut self, c: [i64; 2], h: u32) {
        let old = match self.slot(c) {
            Some(s) => std::mem::replace(&mut self.dense[s], h),
            None if h == NONE => self.sparse.remove(&c).unwrap_or(NONE),
            None => self.sparse.insert(c, h).unwrap_or(NONE),
        };
        self.occupied = self.occupied + (h != NONE) as usize - (old != NONE) as usize;
    }
}

/// A cell grid in the frame moving at `u`: y = x − u·(t − t_ref).
struct Frame {
    u: [i64; 2],
    t_ref: Tick,
    side: i64,
    grid: Grid,
    /// Class frames: bounding box of the members' co-moving positions at formation. Members
    /// only ever leave, so it stays a valid bound.
    lo: [i64; 2],
    hi: [i64; 2],
    /// Side to use when the frame is formed again (feedback or elastic tail).
    next_side: i64,
}

impl Frame {
    #[inline]
    fn y(&self, x: [i64; 2], t: Tick) -> [i64; 2] {
        let dt = t - self.t_ref;
        [x[0] - self.u[0] * dt, x[1] - self.u[1] * dt]
    }

    #[inline]
    fn cell(&self, y: [i64; 2]) -> [i64; 2] {
        [y[0].div_euclid(self.side), y[1].div_euclid(self.side)]
    }

    /// Where a tracker must be for a pair with a member to be able to hit next bin: the box
    /// grown by one side (≥ reach + |w_c|).
    fn region(&self) -> ([i64; 2], [i64; 2]) {
        ([self.lo[0] - self.side, self.lo[1] - self.side], [self.hi[0] + self.side, self.hi[1] + self.side])
    }
}

fn inside(y: [i64; 2], (lo, hi): ([i64; 2], [i64; 2])) -> bool {
    (0..2).all(|c| lo[c] <= y[c] && y[c] <= hi[c])
}

/// Calls `f` for every body listed in the 3×3 cells of `frame` around `cell`.
#[inline]
fn around(frame: &Frame, hot: &[Hot], cell: [i64; 2], mut f: impl FnMut(usize)) {
    for dx in -1..=1 {
        for dy in -1..=1 {
            let mut j = frame.grid.head([cell[0] + dx, cell[1] + dy]);
            while j != NONE {
                f(j as usize);
                j = hot[j as usize].next;
            }
        }
    }
}

/// Per-body index and calendar data (not part of the canonical state).
#[derive(Clone, Copy)]
struct Sched {
    home: u8,
    cell: [i64; 2],
    prev: u32,
    e_hit: Tick,
    e_cross: Tick,
    /// Tick at which the body joined the upkeep set (dedup).
    touched: Tick,
}

fn link(f: &mut Frame, hot: &mut [Hot], s: &mut [Sched], i: usize, cell: [i64; 2]) {
    let old = f.grid.head(cell);
    f.grid.set_head(cell, i as u32);
    s[i].cell = cell;
    s[i].prev = NONE;
    hot[i].next = old;
    if old != NONE {
        s[old as usize].prev = i as u32;
    }
}

fn unlink(f: &mut Frame, hot: &mut [Hot], s: &mut [Sched], i: usize) {
    let (p, nx, cell) = (s[i].prev, hot[i].next, s[i].cell);
    if nx != NONE {
        s[nx as usize].prev = p;
    }
    if p != NONE {
        hot[p as usize].next = nx;
    } else {
        f.grid.set_head(cell, nx);
    }
}

/// Contact (a, b), a < b by index, consumed at both bodies' current revisions. Entries live
/// in a's list; lists are pruned on insertion.
fn consumed(hot: &[Hot], cons: &[Cons], a: usize, b: usize) -> bool {
    let (ra, rb) = (hot[a].rev, hot[b].rev);
    let mut e = hot[a].cons;
    while e != NONE {
        let c = &cons[e as usize];
        if c.b as usize == b && c.ra == ra && c.rb == rb {
            return true;
        }
        e = c.next;
    }
    false
}

/// Free every entry of the list at `head` matching `dead` onto the free list; returns
/// entries walked.
fn unlist(head: &mut u32, cons: &mut [Cons], free: &mut u32, len: &mut usize, mut dead: impl FnMut(&Cons) -> bool) -> u64 {
    let (mut prev, mut e, mut walked) = (NONE, *head, 0);
    while e != NONE {
        walked += 1;
        let c = cons[e as usize];
        if dead(&c) {
            if prev == NONE {
                *head = c.next;
            } else {
                cons[prev as usize].next = c.next;
            }
            cons[e as usize].next = *free;
            *free = e;
            *len -= 1;
        } else {
            prev = e;
        }
        e = c.next;
    }
    walked
}

/// Working sets of the pending tick; invisible until published. Buffers keep their capacity.
#[derive(Default)]
struct Batch {
    cand: Vec<u32>,
    pairs: Vec<(u32, u32)>,
    walls: Vec<u32>,
    touched: Vec<u32>,
    /// Component labelling: involved bodies, union-find, component of each, offsets.
    inv: Vec<u32>,
    parent: Vec<u32>,
    comp_of: Vec<u32>,
    at: Vec<u32>,
    body_start: Vec<u32>,
    pair_start: Vec<u32>,
    fill: Vec<u32>,
    comp_bodies: Vec<u32>,
    comp_walls: Vec<bool>,
    comp_pairs: Vec<(usize, usize)>,
    work: Vec<Body>,
    resolved: Vec<(u32, Body)>,
    wall_momentum: [i64; 2],
    /// Largest |k_c| among changed velocities (elastic tail check).
    kmax: i64,
}

/// Rebuild scratch: velocity sketch, classes found, new home per body, new frames' boxes.
#[derive(Default)]
struct Rebuild {
    /// (velocity, count + base): live while above `base`; decrement-all is base += 1.
    sketch: Vec<([i64; 2], u32)>,
    base: u32,
    classes: Vec<[i64; 2]>,
    home: Vec<u8>,
    count: Vec<usize>,
    lo: Vec<[i64; 2]>,
    hi: Vec<[i64; 2]>,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Phase {
    /// Sketch the velocities; up to MAX_CLASSES nonzero ones with at least CLASS_MIN
    /// bodies (sketch counts only underestimate) form classes.
    Count,
    /// Assign homes and measure each new frame's box.
    Box,
    /// Create the new frames (one step, O(frames)).
    Setup,
    /// Initialise frame `.1 / 2^32`'s dense cells, FILL_CHUNK per step.
    Fill,
    /// Move each body from its old frame to its new one.
    Register,
    Predict,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Stage {
    /// Index and calendar current at `tick`: find the next event tick.
    Idle,
    /// Re-form every frame at `tick` (genesis, elastic tail, density feedback).
    Rebuild(Phase, usize),
    /// Pop the calendar slots at t.
    Gather(Tick),
    /// Scan candidate `.1` for pairs hitting in bin t and walls at t.
    Scan(Tick, usize),
    /// Sort pairs and label connected components.
    Build(Tick),
    /// Respond to component `.1`.
    Resolve(Tick, usize),
    /// Commit tick t: bodies, consumed pairs, log, wall ledger.
    Publish(Tick),
    /// Re-home/re-register, then re-predict, the touched bodies at `tick`.
    Upkeep(bool, usize),
}

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct Footprint {
    pub calendar: usize,
    pub calendar_cap: usize,
    pub cells: usize,
    pub cells_cap: usize,
    pub consumed: usize,
    pub frames: usize,
}

pub struct EventCore {
    /// The genesis world without bodies or consumed pairs: carries q, the container and any
    /// field the contract adds (a law selector) into every [`Stepper::world`] snapshot.
    meta: World,
    /// Canonical bodies; their x, k and rev are stale: those live in `hot`.
    bodies: Vec<Body>,
    hot: Vec<Hot>,
    s: Vec<Sched>,
    /// Consumed-entry arena, its free list and live count.
    cons: Vec<Cons>,
    cons_free: u32,
    cons_len: usize,
    /// Batch epoch (one per event tick processed).
    epoch: u32,
    frames: Vec<Frame>,
    old: Vec<Frame>,
    cal: Calendar,
    reach_max: i64,
    kcap: i64,
    /// Largest |k_c| seen (genesis or published): grids are formed for twice it.
    kseen: i64,
    /// Requested genesis side (test hook), no margin.
    fixed_side: Option<i64>,
    tick: Tick,
    wall_momentum: [i64; 2],
    log: Log,
    metrics: Metrics,
    stage: Stage,
    b: Batch,
    rb: Rebuild,
    rebuilds: u64,
    /// Density feedback window on frame 0: crossing-triggered predictions and their
    /// neighbours, event-triggered predictions and their neighbours.
    fb: [u64; 4],
}

impl EventCore {
    pub fn new(world: World, keep_events: bool) -> Result<Self, law::LawError> {
        Self::build(world, keep_events, None)
    }

    /// Like [`EventCore::new`] with a requested genesis cell side, raised to the validity
    /// bound reach_max + 2·max|k_c| (no margin, so the elastic tail forces rebuilds: a test hook).
    pub fn with_cell_side(world: World, keep_events: bool, side: i64) -> Result<Self, law::LawError> {
        Self::build(world, keep_events, Some(side))
    }

    fn build(mut world: World, keep_events: bool, fixed_side: Option<i64>) -> Result<Self, law::LawError> {
        world.validate()?;
        let n = world.bodies.len();
        if n >= NONE as usize {
            return Err(law::LawError(format!("{n} bodies exceed the u32 index")));
        }
        let hot: Vec<Hot> = world
            .bodies
            .iter()
            .map(|b| Hot { x: b.x, k: b.k, t0: world.tick, radius: b.radius, rev: b.rev, next: NONE, cons: NONE, cand: 0 })
            .collect();
        let blank = Sched { home: UNHOMED, cell: [0, 0], prev: NONE, e_hit: NEVER, e_cross: NEVER, touched: Tick::MIN };
        let bodies = std::mem::take(&mut world.bodies);
        let consumed_in = std::mem::take(&mut world.consumed);
        let mut core = EventCore {
            reach_max: 2 * bodies.iter().map(|b| b.radius).max().unwrap_or(1),
            kseen: bodies.iter().map(|b| kinf(b.k)).max().unwrap_or(0),
            hot,
            s: vec![blank; n],
            cons: Vec::with_capacity(n / 2 + 64),
            cons_free: NONE,
            cons_len: 0,
            epoch: 0,
            frames: Vec::new(),
            old: Vec::new(),
            cal: Calendar::new(n),
            kcap: 0,
            fixed_side,
            tick: world.tick,
            wall_momentum: world.wall_momentum,
            log: Log::new(keep_events),
            metrics: Metrics::default(),
            stage: Stage::Idle,
            b: Batch::default(),
            rb: Rebuild { home: vec![0; n], ..Rebuild::default() },
            rebuilds: 0,
            fb: [0; 4],
            bodies,
            meta: world,
        };
        for c in &consumed_in {
            let (Ok(i), Ok(j)) = (core.bodies.binary_search_by_key(&c.a, |b| b.id), core.bodies.binary_search_by_key(&c.b, |b| b.id)) else {
                return Err(law::LawError(format!("consumed pair ({}, {}) names a missing body", c.a, c.b)));
            };
            if i >= j {
                return Err(law::LawError(format!("consumed pair ({}, {}) not in id order", c.a, c.b)));
            }
            // Later entries overwrite earlier ones, as a map insert would.
            core.unlist(i, |e| e.b as usize == j);
            core.enlist(i, Cons { b: j as u32, ra: c.rev_a, rb: c.rev_b, next: NONE });
        }
        core.begin_rebuild();
        core.rebuilds = 0;
        Ok(core)
    }

    /// Frame 0's cell side (1/Q units).
    pub fn cell_side(&self) -> i64 {
        self.frames.first().map_or(0, |f| f.side)
    }

    /// Rebuilds after genesis (elastic tail or density feedback).
    pub fn rebuilds(&self) -> u64 {
        self.rebuilds
    }

    /// Co-moving class frames currently formed.
    pub fn classes(&self) -> usize {
        self.frames.len().saturating_sub(1)
    }

    pub fn footprint(&self) -> Footprint {
        Footprint {
            calendar: self.cal.heap.len(),
            calendar_cap: self.cal.heap.capacity(),
            cells: self.frames.iter().map(|f| f.grid.occupied).sum(),
            cells_cap: self.frames.iter().map(|f| f.grid.dense.len() + f.grid.sparse.capacity()).sum(),
            consumed: self.cons_len,
            frames: self.frames.len(),
        }
    }

    fn at(&self, i: usize, t: Tick) -> [i64; 2] {
        self.hot[i].at(t)
    }

    /// Push an entry at the head of a's consumed list (reusing a freed slot).
    fn enlist(&mut self, a: usize, mut c: Cons) {
        c.next = self.hot[a].cons;
        let slot = if self.cons_free != NONE {
            let f = self.cons_free;
            self.cons_free = self.cons[f as usize].next;
            self.cons[f as usize] = c;
            f
        } else {
            self.cons.push(c);
            (self.cons.len() - 1) as u32
        };
        self.hot[a].cons = slot;
        self.cons_len += 1;
    }

    /// Free every entry of a's list matching `dead`; returns entries walked.
    fn unlist(&mut self, a: usize, dead: impl FnMut(&Cons) -> bool) -> u64 {
        let mut head = self.hot[a].cons;
        let walked = unlist(&mut head, &mut self.cons, &mut self.cons_free, &mut self.cons_len, dead);
        self.hot[a].cons = head;
        walked
    }

    fn touch(&mut self, i: u32, t: Tick) {
        let s = &mut self.s[i as usize];
        if s.touched != t {
            s.touched = t;
            self.b.touched.push(i);
        }
    }

    /// Frames body i covers besides its home: every class frame for a rest body, the
    /// higher class frames for a member.
    fn tracked(&self, i: usize) -> std::ops::Range<usize> {
        let h = self.s[i].home as usize;
        (if h == REST { 1 } else { h + 1 })..self.frames.len()
    }

    /// Earliest hit (covered pairs, walls) and next cell change or class-box entry of body
    /// i from its state at t; replaces its calendar slot.
    /// `feedback`: count it in the density window (not for rebuild sweeps).
    fn predict(&mut self, i: usize, t: Tick, feedback: bool) {
        let hi = self.hot[i];
        let xi = hi.at(t);
        let bi = &self.bodies[i];
        let (mut ops, mut preds, mut e_hit, mut e_cross) = (0u64, 0u64, NEVER, NEVER);
        let (hot, cons) = (&self.hot, &self.cons);
        let mut visits = [0u64; MAX_CLASSES + 1];
        let mut visit = |j: usize, n: &mut u64| {
            if j == i {
                return;
            }
            *n += 1;
            let (a, b) = (i.min(j), i.max(j));
            if consumed(hot, cons, a, b) {
                return;
            }
            preds += 1;
            let xj = hot[j].at(t);
            let (xa, xb) = if a == i { (xi, xj) } else { (xj, xi) };
            let (ha, hb) = (&hot[a], &hot[b]);
            if let Some(u) = law::first_hit(law::sub(xb, xa), law::sub(hb.k, ha.k), (ha.radius + hb.radius) as i128) {
                e_hit = e_hit.min(t.saturating_add(u).saturating_add(1));
            }
        };
        if self.s[i].home as usize == REST {
            let (f, cell) = (&self.frames[REST], self.s[i].cell);
            around(f, hot, cell, |j| visit(j, &mut visits[REST]));
            e_cross = e_cross.min(cross_time(xi, hi.k, cell, f.side, t));
            ops += 2;
        }
        for g in self.tracked(i) {
            let f = &self.frames[g];
            let (y, v) = (f.y(xi, t), [hi.k[0] - f.u[0], hi.k[1] - f.u[1]]);
            let region = f.region();
            ops += 1;
            if inside(y, region) {
                let cell = f.cell(y);
                around(f, hot, cell, |j| visit(j, &mut visits[g]));
                e_cross = e_cross.min(cross_time(y, v, cell, f.side, t));
                ops += 1;
            } else if let Some(s) = entry_time(y, v, region.0, region.1) {
                e_cross = e_cross.min(t.saturating_add(s));
            }
        }
        if let (Some(c), Response::Bounce) = (&self.meta.container, bi.response) {
            ops += 1;
            preds += 1;
            let (lo, up) = c.inset(hi.radius);
            if let Some(s) = law::first_wall(xi, hi.k, lo, up) {
                e_hit = e_hit.min(t.saturating_add(s));
            }
        }
        ops += visits.iter().sum::<u64>();
        if feedback && self.s[i].home as usize == REST {
            // Candidates and involved bodies carry this batch's epoch; the rest only crossed.
            let slot = if hi.cand == self.epoch { 2 } else { 0 };
            self.fb[slot] += 1;
            self.fb[slot + 1] += visits[REST];
        }
        let s = &mut self.s[i];
        s.e_hit = e_hit;
        s.e_cross = e_cross;
        let e = e_hit.min(e_cross);
        if self.cal.set(i, e) {
            self.metrics.invalidated += 1;
        }
        self.metrics.scheduled += (e != NEVER) as u64;
        self.metrics.ops += ops + 1;
        self.metrics.predicates += preds;
    }

    /// One resumable step toward `target`.
    fn step(&mut self, target: Tick) {
        match self.stage {
            Stage::Rebuild(phase, cursor) => self.rebuild(phase, cursor),
            Stage::Upkeep(predict, cursor) => self.upkeep(predict, cursor),
            Stage::Idle => self.idle(target),
            // No event before the pending tick: commit up to the target, keep the work.
            Stage::Gather(t) | Stage::Scan(t, _) | Stage::Build(t) | Stage::Resolve(t, _) | Stage::Publish(t) if t > target => {
                self.tick = target;
            }
            Stage::Gather(t) => self.gather(t),
            Stage::Scan(t, c) => self.scan(t, c),
            Stage::Build(t) => self.label(t),
            Stage::Resolve(t, c) => self.resolve(t, c),
            Stage::Publish(t) => self.publish(t),
        }
    }

    fn begin_rebuild(&mut self) {
        self.rb.classes.clear();
        self.rb.sketch.clear();
        self.rb.base = 0;
        self.rebuilds += 1;
        self.stage = Stage::Rebuild(Phase::Count, 0);
    }

    fn rebuild(&mut self, phase: Phase, i: usize) {
        let n = self.bodies.len();
        let (t, rb) = (self.tick, &mut self.rb);
        let next = |p| Stage::Rebuild(p, 0);
        self.stage = match phase {
            Phase::Count if i == n || n < CLASS_MIN as usize => {
                // Sketch counts never exceed the true counts, so each class has CLASS_MIN members.
                let base = rb.base;
                let mut found: Vec<_> = rb.sketch.iter().filter(|e| e.1 >= base + CLASS_MIN).copied().collect();
                found.sort_unstable_by_key(|&(k, c)| (std::cmp::Reverse(c), k));
                rb.classes.extend(found.iter().take(MAX_CLASSES).map(|e| e.0));
                self.metrics.ops += rb.sketch.len() as u64;
                let f = rb.classes.len() + 1;
                rb.count.clear();
                rb.lo.clear();
                rb.hi.clear();
                rb.count.resize(f, 0);
                rb.lo.resize(f, [i64::MAX; 2]);
                rb.hi.resize(f, [i64::MIN; 2]);
                next(Phase::Box)
            }
            Phase::Count => {
                let (k, base) = (self.hot[i].k, rb.base);
                if k != [0, 0] {
                    let (mut hit, mut free) = (None, None);
                    for (j, e) in rb.sketch.iter().enumerate() {
                        if e.1 <= base {
                            free = free.or(Some(j));
                        } else if e.0 == k {
                            hit = Some(j);
                            break;
                        }
                    }
                    match (hit, free) {
                        (Some(j), _) => rb.sketch[j].1 += 1,
                        (None, Some(j)) => rb.sketch[j] = (k, base + 1),
                        (None, None) if rb.sketch.len() < SKETCH => rb.sketch.push((k, base + 1)),
                        (None, None) => rb.base += 1,
                    }
                }
                self.metrics.ops += 2;
                Stage::Rebuild(phase, i + 1)
            }
            Phase::Box if i == n => next(Phase::Setup),
            Phase::Box => {
                let k = self.hot[i].k;
                let h = rb.classes.iter().position(|&u| u == k).map_or(REST, |p| p + 1);
                rb.home[i] = h as u8;
                rb.count[h] += 1;
                // New frames are referenced at t, so y = x(t).
                let x = self.hot[i].at(t);
                for (c, &v) in x.iter().enumerate() {
                    rb.lo[h][c] = rb.lo[h][c].min(v);
                    rb.hi[h][c] = rb.hi[h][c].max(v);
                }
                self.metrics.ops += 1;
                Stage::Rebuild(phase, i + 1)
            }
            Phase::Setup => {
                self.setup_frames();
                next(Phase::Fill)
            }
            Phase::Fill => {
                // Allocation reserved the dense arrays; initialise them in bounded chunks.
                let (f, done) = (i >> 32, i & 0xFFFF_FFFF);
                match self.frames.get_mut(f) {
                    None => next(Phase::Register),
                    Some(fr) => {
                        let cells = (fr.grid.dim[0] * fr.grid.dim[1]) as usize;
                        let take = FILL_CHUNK.min(cells - done);
                        fr.grid.dense.extend(std::iter::repeat_n(NONE, take));
                        self.metrics.ops += (take / 64 + 1) as u64;
                        let next_i = if done + take == cells { (f + 1) << 32 } else { (f << 32) | (done + take) };
                        Stage::Rebuild(Phase::Fill, next_i)
                    }
                }
            }
            Phase::Register if i == n => next(Phase::Predict),
            Phase::Register => {
                let old = self.s[i].home;
                if old != UNHOMED {
                    unlink(&mut self.old[old as usize], &mut self.hot, &mut self.s, i);
                }
                let h = self.rb.home[i] as usize;
                let f = &mut self.frames[h];
                let cell = f.cell(f.y(self.hot[i].at(t), t));
                link(f, &mut self.hot, &mut self.s, i, cell);
                self.s[i].home = h as u8;
                self.metrics.ops += 2;
                Stage::Rebuild(phase, i + 1)
            }
            Phase::Predict if i == n => {
                // Every old list is empty now: dropping the maps frees without touching entries.
                self.old.clear();
                Stage::Idle
            }
            Phase::Predict => {
                self.predict(i, t, false);
                Stage::Rebuild(phase, i + 1)
            }
        };
    }

    /// Form the new frames: sides from feedback (a frame of the same velocity existed) or
    /// from density, never below the validity bound with a 2× margin for the elastic tail.
    fn setup_frames(&mut self) {
        let n = self.bodies.len();
        let valid = (self.reach_max + 4 * self.kseen).max(1);
        self.old = std::mem::take(&mut self.frames);
        let genesis = self.old.is_empty();
        let rb = &self.rb;
        for h in 0..rb.count.len() {
            let u = if h == REST { [0, 0] } else { rb.classes[h - 1] };
            let (mut lo, mut hi) = (rb.lo[h], rb.hi[h]);
            if let (Some(c), REST) = (&self.meta.container, h) {
                (lo, hi) = ([lo[0].min(c.min[0]), lo[1].min(c.min[1])], [hi[0].max(c.max[0]), hi[1].max(c.max[1])]);
            }
            let side = match (self.old.iter().find(|f| f.u == u), self.fixed_side) {
                (Some(f), _) => f.next_side.max(valid),
                (None, Some(s)) if genesis => s.max(self.reach_max + 2 * self.kseen).max(1),
                (None, _) => {
                    let area = if rb.count[h] == 0 { 0.0 } else { (hi[0] - lo[0]) as f64 * (hi[1] - lo[1]) as f64 };
                    ((DENSITY_FACTOR * (area / rb.count[h].max(1) as f64).sqrt()).ceil() as i64).max(valid)
                }
            };
            // Dense over the box plus one cell (at most 4 cells a body); drifters go sparse.
            // Frame 0 can come to hold every body; a class frame only its members.
            let (m, cap) = (rb.count[h], if h == REST { n } else { rb.count[h] });
            let grid = if m == 0 {
                Grid::new([0, 0], [-1, -1], 0, 0, cap)
            } else {
                let cell = |v: i64| v.div_euclid(side);
                let (clo, chi) = ([cell(lo[0]) - 1, cell(lo[1]) - 1], [cell(hi[0]) + 1, cell(hi[1]) + 1]);
                Grid::new(clo, chi, 4 * n + 1024, cap / 8 + 64, cap)
            };
            self.frames.push(Frame { u, t_ref: self.tick, side, grid, lo, hi, next_side: side });
        }
        self.kcap = self.frames.iter().map(|f| (f.side - self.reach_max) / 2).min().unwrap_or(0);
        self.fb = [0; 4];
        self.metrics.ops += self.frames.len() as u64;
    }

    /// Density feedback on frame 0, once per window of max(n, 1024) predictions so a rebuild
    /// (O(n), incremental) is amortised: model the window's ops at 2L and L/2 and pick the
    /// cheaper if it saves 30%. Class frames keep the side of their formation density.
    fn retune(&mut self) -> bool {
        let [pc, vc, pe, ve] = self.fb.map(|v| v as f64);
        self.fb = [0; 4];
        let valid = (self.reach_max + 4 * self.kseen).max(1);
        let Some(f) = self.frames.first_mut() else { return false };
        let now = PREDICT_OPS * (pc + pe) + vc + ve;
        let up = PREDICT_OPS * (pc / 2.0 + pe) + 2.0 * vc + 4.0 * ve;
        let down = PREDICT_OPS * (2.0 * pc + pe) + vc / 2.0 + ve / 4.0;
        let side = if up < RESCALE_GAIN * now && up <= down {
            f.side.saturating_mul(2)
        } else if down < RESCALE_GAIN * now && f.side / 2 >= valid {
            f.side / 2
        } else {
            return false;
        };
        f.next_side = side;
        true
    }

    fn upkeep(&mut self, predict: bool, cursor: usize) {
        let Some(&i) = self.b.touched.get(cursor) else {
            self.stage = if predict { Stage::Idle } else { Stage::Upkeep(true, 0) };
            return;
        };
        let i = i as usize;
        if predict {
            self.predict(i, self.tick, true);
        } else {
            let h = self.s[i].home as usize;
            let x = self.at(i, self.tick);
            self.metrics.ops += 1;
            if h != REST && self.hot[i].k != self.frames[h].u {
                // Left its class: re-home to the rest frame.
                unlink(&mut self.frames[h], &mut self.hot, &mut self.s, i);
                let cell = self.frames[REST].cell(x);
                link(&mut self.frames[REST], &mut self.hot, &mut self.s, i, cell);
                self.s[i].home = REST as u8;
                self.metrics.cell_moves += 1;
                self.metrics.ops += 2;
            } else if h == REST {
                let cell = self.frames[REST].cell(x);
                if cell != self.s[i].cell {
                    unlink(&mut self.frames[REST], &mut self.hot, &mut self.s, i);
                    link(&mut self.frames[REST], &mut self.hot, &mut self.s, i, cell);
                    self.metrics.cell_moves += 1;
                    self.metrics.ops += 2;
                }
            }
        }
        self.stage = Stage::Upkeep(predict, cursor + 1);
    }

    fn idle(&mut self, target: Tick) {
        // Bodies that drifted out of frame 0's dense box outgrew its sparse reserve: re-form
        // it around them rather than let the hash map rehash in one step.
        if self.frames.first().is_some_and(|f| f.grid.sparse.len() > f.grid.reserve) {
            self.begin_rebuild();
            return;
        }
        if self.fb[0] + self.fb[2] >= (self.bodies.len() as u64).max(1024) && self.retune() {
            self.begin_rebuild();
            return;
        }
        let Some((t, _)) = self.cal.peek() else {
            self.tick = target;
            return;
        };
        if t > target {
            self.tick = target;
            return;
        }
        debug_assert!(t > self.tick, "calendar slot {t} not after the committed tick {}", self.tick);
        self.tick = t - 1;
        self.epoch = self.epoch.wrapping_add(1);
        let b = &mut self.b;
        b.cand.clear();
        b.pairs.clear();
        b.walls.clear();
        b.touched.clear();
        b.resolved.clear();
        (b.wall_momentum, b.kmax) = ([0, 0], 0);
        self.stage = Stage::Gather(t);
    }

    fn gather(&mut self, t: Tick) {
        match self.cal.peek() {
            Some((tt, i)) if tt == t => {
                self.cal.pop();
                self.metrics.ops += 1;
                if self.s[i].e_hit == t {
                    self.hot[i].cand = self.epoch;
                    self.b.cand.push(i as u32);
                }
                // A crossing or box entry (e_cross == t) needs no batch work: upkeep re-predicts it.
                self.touch(i as u32, t);
            }
            _ => self.stage = Stage::Scan(t, 0),
        }
    }

    /// Candidate c: every covered, non-consumed pair hitting in bin t (positions at t − 1,
    /// where the registered cells are exact), and the wall set at t.
    fn scan(&mut self, t: Tick, c: usize) {
        let Some(&i) = self.b.cand.get(c) else {
            self.stage = Stage::Build(t);
            return;
        };
        let i = i as usize;
        let xi = self.at(i, t - 1);
        let (hot, cons, s, epoch) = (&self.hot, &self.cons, &self.s, self.epoch);
        let mut pairs = std::mem::take(&mut self.b.pairs);
        let (mut ops, mut visits, mut preds) = (0u64, 0u64, 0u64);
        let mut visit = |j: usize, symmetric: bool| {
            // Rest pairs of two candidates are scanned once, by the lower index.
            if j == i || (symmetric && hot[j].cand == epoch && j < i) {
                return;
            }
            visits += 1;
            let (a, b) = (i.min(j), i.max(j));
            if consumed(hot, cons, a, b) {
                return;
            }
            preds += 1;
            let xj = hot[j].at(t - 1);
            let (xa, xb) = if a == i { (xi, xj) } else { (xj, xi) };
            let (ha, hb) = (&hot[a], &hot[b]);
            if law::hit(law::sub(xb, xa), law::sub(hb.k, ha.k), (ha.radius + hb.radius) as i128) {
                pairs.push((a as u32, b as u32));
            }
        };
        if s[i].home as usize == REST {
            around(&self.frames[REST], hot, s[i].cell, |j| visit(j, true));
            ops += 1;
        }
        for g in self.tracked(i) {
            let f = &self.frames[g];
            let y = f.y(xi, t - 1);
            ops += 1;
            if inside(y, f.region()) {
                around(f, hot, f.cell(y), |j| visit(j, false));
            }
        }
        self.b.pairs = pairs;
        ops += visits;
        if let (Some(ct), Response::Bounce) = (&self.meta.container, self.bodies[i].response) {
            ops += 1;
            preds += 1;
            let (lo, hi) = ct.inset(self.hot[i].radius);
            if law::at_wall(self.at(i, t), self.hot[i].k, lo, hi) {
                self.b.walls.push(i as u32);
            }
        }
        self.metrics.ops += ops;
        self.metrics.predicates += preds;
        self.stage = Stage::Scan(t, c + 1);
    }

    /// Sort the pairs as Chronon does and group the batch into connected components (counting
    /// sort into flat buffers): each component's bodies ascend by id and its pairs keep the
    /// global order.
    fn label(&mut self, t: Tick) {
        let b = &mut self.b;
        b.pairs.sort_unstable();
        b.inv.clear();
        b.inv.extend(b.pairs.iter().flat_map(|&(x, y)| [x, y]).chain(b.walls.iter().copied()));
        b.inv.sort_unstable();
        b.inv.dedup();
        let m = b.inv.len();
        let inv = &b.inv;
        let loc = |g: u32| inv.binary_search(&g).expect("involved body");
        fn find(p: &mut [u32], mut x: usize) -> usize {
            while p[x] as usize != x {
                p[x] = p[p[x] as usize];
                x = p[x] as usize;
            }
            x
        }
        b.parent.clear();
        b.parent.extend(0..m as u32);
        for &(x, y) in &b.pairs {
            let (rx, ry) = (find(&mut b.parent, loc(x)), find(&mut b.parent, loc(y)));
            if rx != ry {
                b.parent[rx.max(ry)] = rx.min(ry) as u32;
            }
        }
        // Roots are the smallest member, so components are numbered in order of first body.
        b.comp_of.clear();
        b.body_start.clear();
        for l in 0..m {
            let r = find(&mut b.parent, l);
            let c = if r == l {
                b.body_start.push(0);
                (b.body_start.len() - 1) as u32
            } else {
                b.comp_of[r]
            };
            b.comp_of.push(c);
            b.body_start[c as usize] += 1;
        }
        let nc = b.body_start.len();
        let prefix = |v: &mut Vec<u32>| {
            let mut acc = 0;
            for x in v.iter_mut() {
                (acc, *x) = (acc + *x, acc);
            }
            v.push(acc);
        };
        prefix(&mut b.body_start);
        b.fill.clear();
        b.fill.extend_from_slice(&b.body_start[..nc]);
        b.comp_bodies.clear();
        b.comp_bodies.resize(m, 0);
        b.at.clear();
        b.at.resize(m, 0);
        for (l, &g) in inv.iter().enumerate() {
            let c = b.comp_of[l] as usize;
            let p = b.fill[c] as usize;
            b.fill[c] += 1;
            b.comp_bodies[p] = g;
            b.at[l] = p as u32 - b.body_start[c];
        }
        b.comp_walls.clear();
        b.comp_walls.resize(m, false);
        for &w in &b.walls {
            let l = loc(w);
            b.comp_walls[(b.body_start[b.comp_of[l] as usize] + b.at[l]) as usize] = true;
        }
        b.pair_start.clear();
        b.pair_start.resize(nc, 0);
        for &(x, _) in &b.pairs {
            b.pair_start[b.comp_of[loc(x)] as usize] += 1;
        }
        prefix(&mut b.pair_start);
        b.fill.clear();
        b.fill.extend_from_slice(&b.pair_start[..nc]);
        b.comp_pairs.clear();
        b.comp_pairs.resize(b.pairs.len(), (0, 0));
        for &(x, y) in &b.pairs {
            let (lx, ly) = (loc(x), loc(y));
            let c = b.comp_of[lx] as usize;
            b.comp_pairs[b.fill[c] as usize] = (b.at[lx] as usize, b.at[ly] as usize);
            b.fill[c] += 1;
        }
        self.metrics.ops += (m + self.b.pairs.len()) as u64;
        for l in 0..m {
            let g = self.b.inv[l];
            // Scans are over: the epoch now also marks involved partners as event-triggered.
            self.hot[g as usize].cand = self.epoch;
            self.touch(g, t);
        }
        self.stage = Stage::Resolve(t, 0);
    }

    fn resolve(&mut self, t: Tick, c: usize) {
        let b = &mut self.b;
        if c + 1 >= b.body_start.len() {
            self.stage = Stage::Publish(t);
            return;
        }
        let (bs, be) = (b.body_start[c] as usize, b.body_start[c + 1] as usize);
        let (ps, pe) = (b.pair_start[c] as usize, b.pair_start[c + 1] as usize);
        b.work.clear();
        let hot = &self.hot;
        b.work.extend(b.comp_bodies[bs..be].iter().map(|&g| {
            let (g, h) = (g as usize, &hot[g as usize]);
            Body { x: h.at(t), k: h.k, rev: h.rev, ..self.bodies[g].clone() }
        }));
        respond(&mut b.work, &b.comp_pairs[ps..pe], &b.comp_walls[bs..be], &self.meta, &mut b.wall_momentum);
        b.resolved.extend(b.comp_bodies[bs..be].iter().copied().zip(b.work.drain(..)));
        self.metrics.ops += (be - bs + pe - ps) as u64;
        self.stage = Stage::Resolve(t, c + 1);
    }

    /// Atomic commit of tick t (see the crate docs for why it is not split).
    fn publish(&mut self, t: Tick) {
        let mut ops = 0u64;
        for (g, nb) in self.b.resolved.drain(..) {
            let (g, h) = (g as usize, &mut self.hot[g as usize]);
            if nb.k != h.k {
                self.b.kmax = self.b.kmax.max(kinf(nb.k));
            }
            (h.x, h.k, h.rev, h.t0) = (nb.x, nb.k, nb.rev, t);
            self.bodies[g] = nb;
            ops += 1;
        }
        self.tick = t;
        let pairs = std::mem::take(&mut self.b.pairs);
        for &(a, b) in &pairs {
            let (a, b) = (a as usize, b as usize);
            ops += self.consume(a, b, t);
            self.log.record(Event { tick: t, kind: Kind::Contact, a: self.bodies[a].id, b: self.bodies[b].id });
        }
        for &w in &self.b.walls {
            self.log.record(Event { tick: t, kind: Kind::Wall, a: self.bodies[w as usize].id, b: 0 });
            ops += 1;
        }
        for ax in 0..2 {
            self.wall_momentum[ax] += self.b.wall_momentum[ax];
        }
        let size = (pairs.len() + self.b.walls.len()) as u64;
        self.b.pairs = pairs;
        if size > 0 {
            self.metrics.batches += 1;
            self.metrics.max_batch = self.metrics.max_batch.max(size);
            self.metrics.fired += size;
        }
        self.metrics.ops += ops;
        if self.b.kmax > self.kcap {
            // The elastic tail outgrew the cells: grow every frame (2× margin) and re-form.
            self.kseen = self.kseen.max(self.b.kmax);
            let valid = self.reach_max + 4 * self.kseen;
            for f in &mut self.frames {
                f.next_side = f.next_side.max(valid);
            }
            self.begin_rebuild();
        } else {
            self.kseen = self.kseen.max(self.b.kmax);
            self.stage = Stage::Upkeep(false, 0);
        }
    }

    /// Consume (a, b) at the current revisions, pruning a's dead entries (a revision
    /// changed, or the pair no longer approaches) and any older entry for b. Returns ops spent.
    fn consume(&mut self, a: usize, b: usize, t: Tick) -> u64 {
        let (hot, ha) = (&self.hot, self.hot[a]);
        let xa = ha.at(t);
        let mut head = ha.cons;
        let walked = unlist(&mut head, &mut self.cons, &mut self.cons_free, &mut self.cons_len, |c| {
            let x = &hot[c.b as usize];
            c.b as usize == b || c.ra != ha.rev || c.rb != x.rev || law::dot(law::sub(x.at(t), xa), law::sub(x.k, ha.k)) >= 0
        });
        self.hot[a].cons = head;
        self.enlist(a, Cons { b: b as u32, ra: self.hot[a].rev, rb: self.hot[b].rev, next: NONE });
        walked + 1
    }
}

/// The law's response for one component: the one call to change when the contract gains
/// its law selector.
fn respond(bodies: &mut [Body], pairs: &[(usize, usize)], walls: &[bool], meta: &World, wall_momentum: &mut [i64; 2]) {
    law::resolve(bodies, pairs, walls, meta.container.as_ref(), wall_momentum);
}

impl Stepper for EventCore {
    fn tick(&self) -> Tick {
        self.tick
    }

    /// Resumable steps; overshoot below one step (crate docs). Genesis indexing is itself
    /// done here, in steps, so construction is O(n) copies only.
    fn advance(&mut self, target: Tick, budget: u64) -> Tick {
        let start = self.metrics.ops;
        let mut did = false;
        while self.tick < target && (!did || self.metrics.ops - start < budget) {
            self.step(target);
            did = true;
        }
        if did {
            let spent = self.metrics.ops - start;
            self.metrics.units += 1;
            self.metrics.max_unit_ops = self.metrics.max_unit_ops.max(spent);
        }
        self.tick
    }

    fn world(&self) -> World {
        let t = self.tick;
        let bodies = self.bodies.iter().zip(&self.hot).map(|(b, h)| Body { x: h.at(t), k: h.k, rev: h.rev, ..b.clone() }).collect();
        let mut consumed = Vec::with_capacity(self.cons_len);
        for (a, h) in self.hot.iter().enumerate() {
            let mut e = h.cons;
            while e != NONE {
                let c = &self.cons[e as usize];
                consumed.push(Consumed { a: self.bodies[a].id, b: self.bodies[c.b as usize].id, rev_a: c.ra, rev_b: c.rb });
                e = c.next;
            }
        }
        World { tick: t, bodies, consumed, wall_momentum: self.wall_momentum, ..self.meta.clone() }.canonical()
    }

    fn log(&self) -> &Log {
        &self.log
    }

    fn metrics(&self) -> &Metrics {
        &self.metrics
    }
}

/// The ladder's crowded-axes world (xtask/src/ladder.rs `x_crowded`: spacing 16, radius 1,
/// speed Q/4, Pass): half the bodies in columns moving down, half in rows above them moving
/// sideways across the whole width; every box overlaps on one projection and no pair ever
/// touches. Returns the world and the ladder's horizon (4 × width). Kept here until the
/// contract's `worlds` module adopts it.
pub fn crowded_axes(n: u64, q: i64, seed: u64) -> (World, Tick) {
    let (s, radius) = (16i64, 1i64);
    let half = (n / 2) as i64;
    let (width, speed) = (half * s, q / 4);
    let height = width;
    let mut rng = emergent_lattice::worlds::Rng(seed ^ n ^ 0xC0);
    let mut bodies: Vec<Body> = Vec::with_capacity(2 * half as usize);
    let mut push = |p: [i64; 2], k: [i64; 2]| {
        let id = bodies.len() as u64 + 1;
        bodies.push(genesis(id, [p[0] * q, p[1] * q], k, 1, radius * q, Response::Pass));
    };
    for i in 0..half {
        let y = rng.range(0, height);
        push([i * s, y], [0, -speed]);
    }
    for j in 0..half {
        let dir = if rng.next().is_multiple_of(2) { 1 } else { -1 };
        let x = rng.range(0, width);
        push([x, 2 * height + j * s], [dir * speed, 0]);
    }
    (World::new(q, None, bodies).expect("crowded world within the law's ranges"), 4 * width)
}

/// A genesis body: the one place this crate spells out every [`Body`] field.
pub fn genesis(id: u64, x: [i64; 2], k: [i64; 2], mass: i64, radius: i64, response: Response) -> Body {
    Body { id, x, k, mass, radius, response, residual: 0, rev: 0 }
}
