//! One queue, root-clock deadlines. Only broken edge, key-quantum and horizon
//! certificates appear here. Resolving their physical payloads is a separate operation.
use super::{Calendar, Clock, CyclePool, Doll, TimeBasis};
use crate::{orbit::Scalar, Error, Result};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum EventKind {
    Edge { destination: u16 },
    Kick { energy: i64, angular: i64 },
    Horizon,
}
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Event {
    pub time: Scalar,
    pub slot: u32,
    pub kind: EventKind,
}
pub struct EventQueue {
    calendar: Calendar,
    payloads: Vec<Option<EventKind>>,
    now: Scalar,
}
impl EventQueue {
    pub fn new(slots: usize) -> Self {
        Self {
            calendar: Calendar::new(slots),
            payloads: vec![None; slots],
            now: Scalar::ZERO,
        }
    }
    pub fn schedule(&mut self, event: Event) -> Result<()> {
        if event.time < self.now
            || matches!(
                event.kind,
                EventKind::Kick {
                    energy: 0,
                    angular: 0
                }
            )
        {
            return Err(Error::Range);
        }
        self.calendar.set(event.slot as usize, Some(event.time))?;
        self.payloads[event.slot as usize] = Some(event.kind);
        Ok(())
    }
    pub fn cancel(&mut self, slot: u32) -> Result<()> {
        self.calendar.set(slot as usize, None)?;
        self.payloads[slot as usize] = None;
        Ok(())
    }
    /// Asking for a state never inserts a tick. Nothing is done if no certificate broke.
    pub fn pop_through(&mut self, deadline: Scalar) -> Result<Option<Event>> {
        if deadline < self.now {
            return Err(Error::Range);
        }
        let Some((t, slot)) = self.calendar.peek().filter(|&(t, _)| t <= deadline) else {
            self.now = deadline;
            return Ok(None);
        };
        self.calendar.pop();
        self.now = t;
        let kind = self.payloads[slot].take().ok_or(Error::Topology)?;
        Ok(Some(Event {
            time: t,
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
    pub fn add(
        &mut self,
        doll: Doll,
        parent_basis: TimeBasis,
        proper_epoch: Scalar,
        pool: &CyclePool,
    ) -> Result<u16> {
        let parent = doll.parent.ok_or(Error::Topology)?;
        let p = self.dolls.get(parent as usize).ok_or(Error::Topology)?;
        let centre = doll.centre.ok_or(Error::Topology)?;
        if doll.mass.0 >= p.mass.0 {
            return Err(Error::Topology);
        }
        pool.get(centre.key)?;
        let id = u16::try_from(self.dolls.len()).map_err(|_| Error::Range)?;
        self.clocks.push(Some(Clock {
            centre,
            basis: parent_basis,
            coordinate_epoch: 0,
            proper_epoch,
        }));
        self.dolls.push(doll);
        Ok(id)
    }
    pub fn root_time(&self, pool: &CyclePool, mut doll: u16, mut time: Scalar) -> Result<Scalar> {
        loop {
            let node = self.dolls.get(doll as usize).ok_or(Error::Topology)?;
            let Some(parent) = node.parent else {
                return Ok(time);
            };
            let clock = self.clocks[doll as usize].ok_or(Error::Topology)?;
            let proper_parent = node.mass.relative(self.dolls[parent as usize].mass, time)?;
            time = clock.parent_time(pool, proper_parent)?;
            doll = parent;
        }
    }
}
