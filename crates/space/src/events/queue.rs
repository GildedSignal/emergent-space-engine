//! One queue, root-clock deadlines. Only broken edge, key-quantum and horizon
//! certificates appear here. Resolving their physical payloads is a separate operation.
use super::{Calendar, Clock, CyclePool, Doll, TimeBasis};
use crate::{Error, Result, Words};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum EventKind {
    Edge { destination: u16 },
    Kick { energy: i64, angular: i64 },
    Horizon,
}
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Event {
    pub time: Words,
    pub slot: u32,
    pub kind: EventKind,
}
pub struct EventQueue {
    calendar: Calendar,
    payloads: Vec<Option<EventKind>>,
    now: u64,
}
impl EventQueue {
    pub fn new(slots: usize) -> Self {
        Self {
            calendar: Calendar::new(slots),
            payloads: vec![None; slots],
            now: 0,
        }
    }
    pub fn schedule(&mut self, event: Event) -> Result<()> {
        if event.time.get() < self.now || matches!(event.kind, EventKind::Kick { energy: 0, angular: 0 }) {
            return Err(Error::Range);
        }
        self.calendar.set(event.slot as usize, Some(event.time.get()))?;
        self.payloads[event.slot as usize] = Some(event.kind);
        Ok(())
    }
    pub fn cancel(&mut self, slot: u32) -> Result<()> {
        self.calendar.set(slot as usize, None)?;
        self.payloads[slot as usize] = None;
        Ok(())
    }
    /// Asking for a state never inserts a tick. Nothing is done if no certificate broke.
    pub fn pop_through(&mut self, deadline: Words) -> Result<Option<Event>> {
        if deadline.get() < self.now {
            return Err(Error::Range);
        }
        let Some((t, slot)) = self.calendar.peek().filter(|&(t, _)| t <= deadline.get()) else {
            self.now = deadline.get();
            return Ok(None);
        };
        self.calendar.pop();
        self.now = t;
        let kind = self.payloads[slot].take().ok_or(Error::Topology)?;
        Ok(Some(Event {
            time: Words::new(t),
            slot: slot as u32,
            kind,
        }))
    }
    pub fn len(&self) -> usize {
        self.calendar.len()
    }
    pub fn is_empty(&self) -> bool {
        self.calendar.is_empty()
    }
}

/// Parents are inserted first, so the clock graph is acyclic by construction.
/// Clock origins are explicit; epochs/bases and the key table are extra shared storage.
pub struct Hierarchy {
    dolls: Vec<Doll>,
    clocks: Vec<Option<Clock>>,
}
impl Hierarchy {
    pub fn new(root: Doll) -> Result<Self> {
        if root.parent.is_some() || root.centre.is_some() {
            return Err(Error::Topology);
        }
        Ok(Self {
            dolls: vec![root],
            clocks: vec![None],
        })
    }
    pub fn add(&mut self, doll: Doll, parent_basis: TimeBasis, proper_epoch: Words, pool: &CyclePool) -> Result<u16> {
        let parent = doll.parent.ok_or(Error::Topology)?;
        let p = self.dolls.get(parent as usize).ok_or(Error::Topology)?;
        let centre = doll.centre.ok_or(Error::Topology)?;
        if centre.doll != parent || doll.mass.0 >= p.mass.0 {
            return Err(Error::Topology);
        }
        pool.get(centre.key)?;
        let generator = centre.generator(parent_basis)?;
        let id = u16::try_from(self.dolls.len()).map_err(|_| Error::Range)?;
        self.clocks.push(Some(Clock {
            centre: generator,
            proper_epoch,
        }));
        self.dolls.push(doll);
        Ok(id)
    }
    pub fn root_time(&self, pool: &CyclePool, mut doll: u16, mut time: Words) -> Result<Words> {
        loop {
            let node = self.dolls.get(doll as usize).ok_or(Error::Topology)?;
            let Some(parent) = node.parent else {
                return Ok(time);
            };
            let clock = self.clocks[doll as usize].ok_or(Error::Topology)?;
            let centre = node.centre.ok_or(Error::Topology)?;
            let proper_parent = node.mass.relative(self.dolls[parent as usize].mass, time.get(), true)?;
            time = clock.parent_time(pool.get(centre.key)?, Words::new(proper_parent))?;
            doll = parent;
        }
    }
}
