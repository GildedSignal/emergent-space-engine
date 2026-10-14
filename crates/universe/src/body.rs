//! Bodies: tubes in exactly one doll, behind one storage seam.
//!
//! [`BodyStore`] is the interface: a body is read out as a [`BodyRec`] and written back. Today
//! [`PlainBodies`] is plain struct-of-arrays; `crates/shipmem`'s population programs (a program
//! plus sparse scars, or packed blocks) implement the same four calls later, with no rewiring.
//! Every body is either a tube in one doll (here) or a member of one frame (the fleet's battle);
//! there is no third kind.
use crate::bind::Binding;
use crate::num::{Res, Tick};
use emergent_space::{orbit::Scalar, Tube};
use std::collections::VecDeque;
use std::mem::size_of;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Kind {
    Planet,
    Moon,
    Ship,
    Player,
}

/// What a plan item does at its tick.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum What {
    /// A kick of the symmetric split at `level` of the changeover (0 is the whole step).
    Kick(u8),
    /// The start of a level-`l` interval: engage level `l + 1` where a pair can reach its shell.
    Open(u8),
    /// A planned impact: the tube's periapsis is below the surface of the doll's centre. Re-checked
    /// at its tick (a kick may have changed the orbit since).
    Crash,
    /// The end of a step: the certificates (edge, impact, capture) and the next step's plan.
    Boundary,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Item {
    pub t: Tick,
    pub what: What,
}

/// The player's decision state: thrust grows the rapidity in proper time.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Thrust {
    pub keys: u8,
    /// The throttle: the burn is `2^level` times the base thrust (`Config::thrust_log2`). Part of the decision, like the keys.
    pub level: u8,
    /// Heading in turns, Q32.
    pub heading: u32,
    /// When the thrust now held started counting (the last flush), in ticks.
    pub since: Tick,
}

#[derive(Clone, Debug)]
pub struct BodyRec {
    pub kind: Kind,
    pub b: Binding,
    /// The sub-quantum velocity carry (sigma-delta), in `2^-16` of the velocity quantum.
    pub carry: [i64; 2],
    /// Proper time accumulated along the tubes, in root units (a clock reads its tube's length).
    pub proper: Scalar,
    /// The kick step `H`, in ticks (a power of two), and the origin of its grid.
    pub step: i64,
    /// The level-0 interval of the step now planned (the nominal step, or less when capped by an exit).
    pub interval: i64,
    pub anchor: Tick,
    pub plan: Vec<Item>,
    pub thrust: Option<Thrust>,
    /// The extended state of the motion law v2 (the energy register and the clock's constants), for a body of the root
    /// doll that anything can kick: its step is the fictitious clock's tick ([`crate::ext`]). None for the rest (the
    /// planets and the bodies of a planet's doll keep the split of docs/law.md until the dolls are coordinates).
    pub ext: Option<crate::ext::Ext>,
    pub alive: bool,
    pub events: u64,
    pub refusals: u64,
    /// Why the last refusal happened.
    pub fault: Option<(What, crate::num::Error)>,
}

/// A retired binding: readable at any `t` in `[b.event_time, until)`.
#[derive(Clone, Debug)]
pub struct Segment {
    pub b: Binding,
    pub until: Tick,
}

pub trait BodyStore: Send + Sync {
    fn len(&self) -> usize;
    fn is_empty(&self) -> bool {
        self.len() == 0
    }
    fn rec(&self, i: usize) -> BodyRec;
    fn put(&mut self, i: usize, r: BodyRec);
    fn push(&mut self, r: BodyRec) -> usize;
    /// Retire a binding into body `i`'s history (the view reads the past through it).
    fn retire(&mut self, i: usize, seg: Segment);
    /// Forget history that ended before `before`, keeping at least the last segment; how many segments went.
    fn prune(&mut self, i: usize, before: Tick) -> usize;
    /// The binding that holds at `t` (current, or a retired one), if still remembered.
    fn binding_at(&self, i: usize, t: Tick) -> Option<Binding>;
    /// The current binding's event time (the body's committed tick).
    fn event_time(&self, i: usize) -> Tick;
    fn next_time(&self, i: usize) -> Option<Tick>;
    fn alive(&self, i: usize) -> bool;
    /// The doll the body's current tube is in.
    fn doll(&self, i: usize) -> u16 {
        self.rec(i).b.doll
    }
    /// Bytes held per body (the arrays, the catalogue share of its compiled trajectory, history).
    fn bytes_of(&self, i: usize) -> usize;
    /// Retired bindings held for body `i`.
    fn history_len(&self, i: usize) -> usize;
    /// When the oldest retired binding of body `i` ended, if [`BodyStore::prune`] could forget it (more than one is held).
    fn droppable_until(&self, i: usize) -> Option<Tick>;
    /// Body `i`'s current binding and every retained one, oldest first (what a reader can still ask for).
    fn bindings_of(&self, i: usize) -> Vec<Binding>;
}

#[derive(Default)]
pub struct PlainBodies {
    recs: Vec<BodyRec>,
    history: Vec<VecDeque<Segment>>,
}

impl BodyStore for PlainBodies {
    fn len(&self) -> usize {
        self.recs.len()
    }
    fn rec(&self, i: usize) -> BodyRec {
        self.recs[i].clone()
    }
    fn put(&mut self, i: usize, r: BodyRec) {
        self.recs[i] = r;
    }
    fn push(&mut self, r: BodyRec) -> usize {
        self.recs.push(r);
        self.history.push(VecDeque::new());
        self.recs.len() - 1
    }
    fn retire(&mut self, i: usize, seg: Segment) {
        self.history[i].push_back(seg);
    }
    fn prune(&mut self, i: usize, before: Tick) -> usize {
        let h = &mut self.history[i];
        let mut gone = 0;
        while h.len() > 1 && h[0].until < before {
            h.pop_front();
            gone += 1;
        }
        gone
    }
    fn binding_at(&self, i: usize, t: Tick) -> Option<Binding> {
        let r = &self.recs[i];
        if t >= r.b.event_time {
            return Some(r.b.clone());
        }
        let h = &self.history[i];
        // Segments are contiguous and ascending in `until`: the first with `until > t`.
        let k = h.partition_point(|s| s.until <= t);
        h.get(k).filter(|s| s.b.event_time <= t).map(|s| s.b.clone())
    }
    fn event_time(&self, i: usize) -> Tick {
        self.recs[i].b.event_time
    }
    fn next_time(&self, i: usize) -> Option<Tick> {
        let r = &self.recs[i];
        if r.alive {
            r.plan.first().map(|p| p.t)
        } else {
            None
        }
    }
    fn alive(&self, i: usize) -> bool {
        self.recs[i].alive
    }
    fn doll(&self, i: usize) -> u16 {
        self.recs[i].b.doll
    }
    fn history_len(&self, i: usize) -> usize {
        self.history[i].len()
    }
    fn droppable_until(&self, i: usize) -> Option<Tick> {
        let h = &self.history[i];
        h.front().filter(|_| h.len() > 1).map(|s| s.until)
    }
    fn bindings_of(&self, i: usize) -> Vec<Binding> {
        self.history[i].iter().map(|s| s.b.clone()).chain(std::iter::once(self.recs[i].b.clone())).collect()
    }
    fn bytes_of(&self, i: usize) -> usize {
        let r = &self.recs[i];
        let shape = match &r.b.entry.trajectory {
            emergent_space::binding::Trajectory::Cycle(o) => o.shape().knots().len() * size_of::<emergent_space::orbit::Knot>() + o.shape().crossings().len() * size_of::<usize>(),
            emergent_space::binding::Trajectory::Passage(_) => 4096,
            emergent_space::binding::Trajectory::Plunge(p) => p.retained_bytes(),
        };
        size_of::<BodyRec>() + r.plan.capacity() * size_of::<Item>() + shape + self.history[i].len() * size_of::<Segment>()
    }
}

/// The body's tube record (the law's 16 bytes).
pub fn tube_bytes() -> usize {
    size_of::<Tube>()
}

/// Check the invariant of the world model: every body is a tube in one existing doll.
pub fn check_dolls(store: &dyn BodyStore, dolls: usize) -> Res<()> {
    for i in 0..store.len() {
        if store.rec(i).b.doll as usize >= dolls {
            return Err(crate::num::Error::Refused("a body in no doll"));
        }
    }
    Ok(())
}
