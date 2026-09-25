//! The lattice contract shared by every execution mode (docs/work-allocation-design.md).
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

pub use law::{Body, Consumed, Container, Response, Tick, World};
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
