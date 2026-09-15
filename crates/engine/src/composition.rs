//! I2 population composition: collective mass, restricted re-merge, range reception.
//! Isolated from `runtime.rs` scan internals. GEM stays diagnostic.

use crate::{
    geometry::{self, TickInterval},
    math::Rational,
    policy::{Broadcast, BroadcastReception},
    population::Family,
    runtime::{digest, event, Command, Engine, EngineError, Payload},
    LAW_ID,
};
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

#[derive(Clone, Debug, Default, Serialize, Deserialize, PartialEq)]
pub struct ReceptionIndex {
    pub logical_receptions: u64,
    pub stored_records: u64,
    pub by_tick: BTreeMap<i128, Vec<u64>>,
}

impl Engine {
    /// Family mass plus extracted identities that left every generator.
    pub fn collective_mass(&self) -> Rational {
        let mut mass = self
            .state
            .families
            .iter()
            .map(Family::total_mass)
            .fold(crate::math::r(0), |a, b| a + b);
        for (id, body) in &self.state.bodies {
            if self.family_for_id(*id).is_none() {
                mass += body.mass.clone();
            }
        }
        mass
    }

    pub fn family_first_moment(&self, tick: i128) -> crate::math::Vec2 {
        self.state
            .families
            .iter()
            .map(|f| f.first_moment(tick))
            .fold(crate::math::Vec2::zero(), |a, b| a + b)
    }

    fn family_for_id(&self, id: u64) -> Option<&Family> {
        let n = self.state.families.partition_point(|f| f.first_id <= id);
        n.checked_sub(1).and_then(|i| {
            self.state
                .families
                .get(i)
                .filter(|f| f.contains(id))
        })
    }

    /// Fold an extracted body back only when its future matches the generator.
    pub fn try_remerge_extracted(&mut self, id: u64) -> Result<bool, EngineError> {
        let Some(body) = self.state.bodies.get(&id).cloned() else {
            return Ok(false);
        };
        let Some(family) = self.family_for_id(id).cloned() else {
            return Ok(false);
        };
        if !family.matches_extracted_body(&body, self.state.clock) {
            return Ok(false);
        }
        self.state.bodies.remove(&id);
        Ok(true)
    }

    /// Join adjacent family partitions that share an affine future.
    pub fn try_remerge_adjacent_families(&mut self) -> Result<usize, EngineError> {
        let mut families = self.state.families.clone();
        families.sort_by_key(|f| f.first_id);
        let mut merged = 0usize;
        let mut out: Vec<Family> = Vec::new();
        for f in families {
            if let Some(prev) = out.last() {
                if let Some(joined) = Family::exact_remerge(prev, &f) {
                    *out.last_mut().unwrap() = joined;
                    merged += 1;
                    continue;
                }
            }
            out.push(f);
        }
        self.state.families = out;
        Ok(merged)
    }

    /// Two extracted identities swapping generator slots is not a merge.
    pub fn refuse_permutation_merge(&self, a: u64, b: u64) -> Result<bool, EngineError> {
        let ba = self.decode(a)?;
        let bb = self.decode(b)?;
        let Some(fa) = self.family_for_id(a) else {
            return Ok(true);
        };
        let Some(fb) = self.family_for_id(b) else {
            return Ok(true);
        };
        let a_fits_b = fb.matches_extracted_body(&ba, self.state.clock);
        let b_fits_a = fa.matches_extracted_body(&bb, self.state.clock);
        Ok(!(a_fits_b && b_fits_a) || a == b)
    }

    pub fn emit_broadcast(
        &mut self,
        observer: u64,
        lo: u64,
        hi: u64,
        payload: Payload,
        t: i128,
    ) -> Result<String, EngineError> {
        if lo > hi {
            return Err(EngineError::Invalid(
                "broadcast identity range must satisfy lo <= hi".into(),
            ));
        }
        if hi.saturating_sub(lo) >= self.max_pending_jobs as u64 {
            return Err(EngineError::ResourceLimit(
                "broadcast identity range exceeds job capacity".into(),
            ));
        }
        let body = self.decode(observer)?;
        for id in lo..=hi {
            self.decode(id)?;
        }
        if self.state.signals.len() + self.state.broadcasts.len() >= self.max_pending_jobs {
            return Err(EngineError::ResourceLimit("pending signal capacity reached".into()));
        }
        let seq = *self.state.emitter_sequence.get(&observer).unwrap_or(&0);
        let id = digest(&(LAW_ID, self.state.seed, t, observer, lo, hi, seq, &payload));
        let next = seq
            .checked_add(1)
            .ok_or_else(|| EngineError::ResourceLimit("emitter sequence exhausted".into()))?;
        self.state.emitter_sequence.insert(observer, next);
        self.state.broadcasts.insert(
            id.clone(),
            Broadcast {
                id: id.clone(),
                source: observer,
                lo,
                hi,
                tick: t,
                position: body.at(t),
                payload,
            },
        );
        self.state
            .broadcast_receptions
            .entry(id.clone())
            .or_default();
        let e = event(
            t,
            "broadcast_emitted",
            vec![observer, lo, hi],
            vec![id.clone()],
            format!("broadcast {id}"),
        );
        self.state.events.insert(e.id.clone(), e);
        Ok(id)
    }

    /// Index committed receptions. Logical count is the identity range; stored
    /// records group equal arrival ticks. Each heterogeneous recipient keeps
    /// its actual reception time.
    pub fn index_broadcast_receptions(&mut self) -> Result<(), EngineError> {
        let through = self.state.clock;
        let broadcasts: Vec<_> = self.state.broadcasts.values().cloned().collect();
        for b in broadcasts {
            let domain = TickInterval::new(b.tick, through)?;
            let mut map = self
                .state
                .broadcast_receptions
                .remove(&b.id)
                .unwrap_or_default();
            let mut id = b.lo;
            while id <= b.hi {
                if map.contains_key(&id) || !self.in_scan_filter(id) {
                    id = id.saturating_add(1);
                    continue;
                }
                let receiver = self.decode(id)?;
                if let Some(tick) = geometry::first_signal_arrival_piecewise(
                    b.tick,
                    &b.position,
                    &receiver.segments,
                    domain,
                ) {
                    if tick <= through {
                        map.insert(id, BroadcastReception::Received { tick });
                        let e = event(
                            tick,
                            "broadcast_received",
                            vec![b.source, id],
                            vec![b.id.clone()],
                            format!("broadcast {} -> {id}", b.id),
                        );
                        self.state.events.insert(e.id.clone(), e);
                    }
                }
                id = id.saturating_add(1);
            }
            self.state.broadcast_receptions.insert(b.id.clone(), map);
        }
        Ok(())
    }

    pub fn reception_index(&self, broadcast_id: &str) -> ReceptionIndex {
        let mut index = ReceptionIndex::default();
        let Some(map) = self.state.broadcast_receptions.get(broadcast_id) else {
            return index;
        };
        let Some(b) = self.state.broadcasts.get(broadcast_id) else {
            index.logical_receptions = map.len() as u64;
            index.stored_records = map.len() as u64;
            for (id, rec) in map {
                if let BroadcastReception::Received { tick } = rec {
                    index.by_tick.entry(*tick).or_default().push(*id);
                }
            }
            index.stored_records = index.by_tick.len() as u64;
            return index;
        };
        index.logical_receptions = b.hi.saturating_sub(b.lo).saturating_add(1);
        for (id, rec) in map {
            if let BroadcastReception::Received { tick } = rec {
                index.by_tick.entry(*tick).or_default().push(*id);
            }
        }
        index.stored_records = index.by_tick.len() as u64;
        index
    }
}

pub fn command_broadcast(lo: u64, hi: u64, payload: Payload) -> Command {
    Command::Broadcast { lo, hi, payload }
}
