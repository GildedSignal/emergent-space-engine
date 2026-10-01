//! The lattice contract shared by every execution mode (docs/engine.md).
//!
//! - [`law`]: `es-lattice-elastic-v0`, state and the exact per-chronon rule.
//! - [`relativity`]: the relativistic bounce (`es-lattice-relativistic-v0`): exact 4-momentum,
//!   nothing massive reaches c.
//! - [`chronon`]: the CPU chronon-mode reference stepper (grid per chronon). Every other
//!   mode (event core, Metal, regions on many cores) must reproduce its digests.
//! - [`worlds`]: deterministic generators shared by tests and the ladder.
//!
//! Canonical outcome = [`law::World::digest`] (state, live consumed contacts, wall ledger)
//! plus [`Log::digest`] (the multiset of contact and wall events). The log digest is a
//! lane-wise wrapping sum of per-event hashes, so logs from regions, cores or GPU chunks
//! merge by addition in any order.
pub mod chronon;
pub mod law;
pub mod relativity;
pub mod worlds;

pub use law::{Body, Consumed, Container, Law, Response, Tick, World};
use serde::{Deserialize, Serialize};

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum Kind {
    Contact,
    Wall,
}

/// A committed event. Contacts: ids a < b. Walls: b = 0.
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub struct Event {
    pub tick: Tick,
    pub kind: Kind,
    pub a: u64,
    pub b: u64,
}

impl Event {
    fn lanes(&self) -> [u64; 4] {
        let mut buf = [0u8; 25];
        buf[..8].copy_from_slice(&self.tick.to_le_bytes());
        buf[8] = self.kind as u8;
        buf[9..17].copy_from_slice(&self.a.to_le_bytes());
        buf[17..25].copy_from_slice(&self.b.to_le_bytes());
        let h = blake3::hash(&buf);
        let b = h.as_bytes();
        std::array::from_fn(|i| u64::from_le_bytes(b[i * 8..i * 8 + 8].try_into().unwrap()))
    }
}

/// Order-independent event record: counts, a mergeable digest, and optionally the events.
#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Log {
    pub keep: bool,
    pub events: Vec<Event>,
    pub contacts: u64,
    pub walls: u64,
    pub sum: [u64; 4],
}

impl Log {
    pub fn new(keep: bool) -> Self {
        Log { keep, ..Default::default() }
    }

    pub fn record(&mut self, e: Event) {
        match e.kind {
            Kind::Contact => self.contacts += 1,
            Kind::Wall => self.walls += 1,
        }
        for (s, l) in self.sum.iter_mut().zip(e.lanes()) {
            *s = s.wrapping_add(l);
        }
        if self.keep {
            self.events.push(e);
        }
    }

    /// Add another log's events (regions, cores, GPU chunks). Order does not matter.
    pub fn merge(&mut self, other: &Log) {
        self.contacts += other.contacts;
        self.walls += other.walls;
        for (s, l) in self.sum.iter_mut().zip(other.sum) {
            *s = s.wrapping_add(l);
        }
        if self.keep {
            self.events.extend_from_slice(&other.events);
        }
    }

    /// Kept events in canonical order (tick, kind, a, b).
    pub fn sorted(&self) -> Vec<Event> {
        let mut v = self.events.clone();
        v.sort_unstable();
        v
    }

    pub fn digest(&self) -> String {
        let mut buf = Vec::with_capacity(48);
        buf.extend_from_slice(&self.contacts.to_le_bytes());
        buf.extend_from_slice(&self.walls.to_le_bytes());
        for s in self.sum {
            buf.extend_from_slice(&s.to_le_bytes());
        }
        blake3::hash(&buf).to_hex().to_string()
    }
}

/// Resource accounting shared by every mode, so the ladder compares like with like.
///
/// `ops` counts every charged operation: exact predicate evaluations, calendar pushes and
/// pops, cell insertions and removals, body advances, invalidation checks, response work.
/// `predicates` counts exact pair and wall predicate evaluations only. The ladder reports
/// `predicates / ops` (useful-work ratio: step 1 wants > 0.5; the H0158 engine is about
/// 0.003) and `ops / fired` (cost per event: must not grow with world size).
#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Metrics {
    pub ops: u64,
    pub predicates: u64,
    /// Event predictions made (event mode).
    pub scheduled: u64,
    /// Predictions superseded before they fired.
    pub invalidated: u64,
    /// Committed contact and wall events.
    pub fired: u64,
    pub cell_moves: u64,
    pub batches: u64,
    pub max_batch: u64,
    /// Work units (advance calls that did work).
    pub units: u64,
    /// Largest ops spent in one unit.
    pub max_unit_ops: u64,
}

impl Metrics {
    pub fn merge(&mut self, o: &Metrics) {
        self.ops += o.ops;
        self.predicates += o.predicates;
        self.scheduled += o.scheduled;
        self.invalidated += o.invalidated;
        self.fired += o.fired;
        self.cell_moves += o.cell_moves;
        self.batches += o.batches;
        self.max_batch = self.max_batch.max(o.max_batch);
        self.units += o.units;
        self.max_unit_ops = self.max_unit_ops.max(o.max_unit_ops);
    }
}

/// One body's motion at the committed tick: position (1/Q units) and the velocity that
/// holds for the next chronon (1/Q units per chronon).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Motion {
    pub x: [i64; 2],
    pub k: [i64; 2],
}

/// The velocity `k + dk` an external kick may give a body under `which`, or the reason it may
/// not: the law's exactness ranges and, for the relativistic laws, |k|² < Q². Both steppers'
/// kick hooks call this, so they refuse the same kicks.
pub fn kicked(which: Law, q: i64, k: [i64; 2], dk: [i64; 2]) -> Result<[i64; 2], law::LawError> {
    let nk = [k[0] + dk[0], k[1] + dk[1]];
    let kk = nk[0] as i128 * nk[0] as i128 + nk[1] as i128 * nk[1] as i128;
    if nk.iter().any(|c| c.abs() > law::MAX_SPEED) || (which.subluminal() && kk >= q as i128 * q as i128) {
        return Err(law::LawError(format!("kick {dk:?} takes velocity {k:?} to {nk:?}, outside the law")));
    }
    Ok(nk)
}

/// A stepper that accepts external velocity kicks at its committed tick: the hook the
/// free-fall frame (`crates/engine`) uses to apply its tide. A kick is an event of the frame,
/// not of the lattice law: the caller runs the stepper to the kick's tick (`run_to`, never
/// lowering the target afterwards), reads [`Kickable::motions`], and calls [`Kickable::kick`].
/// Bodies whose velocity changes revise (`rev + 1`), exactly as a contact would; a
/// consumed contact is therefore live again if the pair is still approaching.
pub trait Kickable: Stepper {
    /// Position and velocity of every body (id order) at [`Stepper::tick`].
    fn motions(&self, out: &mut Vec<Motion>);

    /// Add `dk[i]` to body i's velocity (id order, one entry per body; zero leaves it alone).
    /// Nothing is applied unless every kicked velocity is legal ([`kicked`]).
    fn kick(&mut self, dk: &[[i64; 2]]) -> Result<(), law::LawError>;

    /// Every body's mass (id order): the weights of a centre of mass.
    fn masses(&self, out: &mut Vec<i64>);

    /// Re-express the world at [`Stepper::tick`] in a moved frame: body i's position gains `dx[i]`
    /// and its velocity `dk[i]` (a body whose velocity changes revises, as in [`Kickable::kick`]).
    /// A frame move is a uniform `dx`, which keeps every pair's separation, so no contact is
    /// created or lost by the translation itself; a per-body `dx` (a caller settling sub-quantum
    /// positions) moves pairs by the difference. Refused, and nothing applied, when a velocity
    /// would be illegal ([`kicked`]), a position would leave the exactness range (|x_c| ≤ 2^39), or
    /// the world has a container (its walls do not move with the frame).
    fn rebase(&mut self, dx: &[[i64; 2]], dk: &[[i64; 2]]) -> Result<(), law::LawError>;
}

/// Whether every shift of a [`Kickable::rebase`] is the same (a frame move, which changes no pair).
pub fn uniform_shift(dx: &[[i64; 2]]) -> bool {
    dx.iter().all(|s| *s == dx[0])
}

/// Whether [`Kickable::rebase`] revises a body: when its velocity changes, or when it is moved by a
/// shift that is not uniform (its pairs then change, so a consumed contact may come back). A frame
/// move revises nobody. Every stepper applies this same rule, so the orders agree.
pub fn rebase_revises(uniform: bool, s: [i64; 2], d: [i64; 2]) -> bool {
    d != [0, 0] || (!uniform && s != [0, 0])
}

/// The legality checks of [`Kickable::rebase`], shared by both steppers so they refuse alike.
pub fn rebased_ok(which: Law, q: i64, has_container: bool, bodies: impl Iterator<Item = Motion>, dx: &[[i64; 2]], dk: &[[i64; 2]]) -> Result<(), law::LawError> {
    if has_container {
        return Err(law::LawError("a world with walls cannot be re-expressed in a moved frame".into()));
    }
    for ((m, s), d) in bodies.zip(dx).zip(dk) {
        if (0..2).any(|c| (m.x[c] as i128 + s[c] as i128).abs() > law::MAX_COORD as i128) {
            return Err(law::LawError(format!("shift {s:?} takes position {:?} outside 2^39", m.x)));
        }
        kicked(which, q, m.k, *d)?;
    }
    Ok(())
}

/// An execution mode for one region of the lattice law.
pub trait Stepper {
    /// Last fully committed tick: every event at or before it is final and [`Stepper::world`]
    /// is the state at this tick.
    fn tick(&self) -> Tick;

    /// Do at most about `budget` ops of work toward `target` and return the committed
    /// tick. Implementations document their overshoot bound (the largest indivisible
    /// step); results must not depend on how the work was sliced.
    fn advance(&mut self, target: Tick, budget: u64) -> Tick;

    /// Canonical state at [`Stepper::tick`].
    fn world(&self) -> World;

    fn log(&self) -> &Log;

    fn metrics(&self) -> &Metrics;

    /// Advance to `target` with unbounded budget.
    fn run_to(&mut self, target: Tick) -> Tick {
        while self.tick() < target {
            self.advance(target, u64::MAX);
        }
        self.tick()
    }

    /// World digest and log digest together.
    fn outcome(&self) -> (String, String) {
        (self.world().digest(), self.log().digest())
    }
}
