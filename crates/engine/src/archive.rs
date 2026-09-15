//! Chunked history archive schema extracted from Packet 6 without old-law fields.
//!
//! `truncated_admission` from Packet 5/6 remainder JSON is refused. Seal,
//! restore and reconstruction against live `Engine` state are I1. Default
//! `Engine::advance` stays `es-inertial-causal-v1`.

use crate::{
    math::Vec2,
    policy::{Broadcast, BroadcastReception},
    population::Family,
    runtime::{Body, EventRecord, RecordedIntervention, ScheduledCourse, ScheduledRangeCourse, Signal},
};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

pub const ARCHIVE_SCHEMA: u32 = 1;

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ChunkListing {
    pub file: String,
    pub payload_hash: String,
    pub tick_lo: i128,
    pub tick_hi: i128,
    pub event_count: usize,
    pub bytes: u64,
}

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ArchiveManifest {
    pub schema: u32,
    pub law: String,
    pub seed: u64,
    pub sealed_through: i128,
    pub events_per_chunk: usize,
    pub history_hash: String,
    pub remainder_hash: String,
    pub chunks: Vec<ChunkListing>,
}

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct HistoryChunk {
    pub schema: u32,
    pub index: u32,
    pub tick_lo: i128,
    pub tick_hi: i128,
    pub payload_hash: String,
    pub events: Vec<EventRecord>,
}

/// Live frontier after the last sealed event. Incoming signals and outgoing
/// broadcasts/scheduled courses survive here when a chunk closes.
/// Packet 5/6 `truncated_admission` is intentionally absent.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct HistoryRemainder {
    pub schema: u32,
    pub law: String,
    pub seed: u64,
    pub branch: String,
    pub genesis_digest: String,
    pub genesis_bodies: BTreeMap<u64, Body>,
    pub genesis_families: Vec<Family>,
    pub interventions: Vec<RecordedIntervention>,
    pub clock: i128,
    pub bodies: BTreeMap<u64, Body>,
    pub families: Vec<Family>,
    pub signals: BTreeMap<String, Signal>,
    pub broadcasts: BTreeMap<String, Broadcast>,
    pub broadcast_receptions: BTreeMap<String, BTreeMap<u64, BroadcastReception>>,
    pub emitter_sequence: BTreeMap<u64, u64>,
    pub contacts: BTreeSet<(u64, u64, u64, u64)>,
    pub actuator_momentum: Vec2,
    pub scheduled_courses: BTreeMap<String, ScheduledCourse>,
    pub scheduled_range_courses: BTreeMap<String, ScheduledRangeCourse>,
    pub payload_hash: String,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::LAW_ID;

    #[test]
    fn remainder_schema_refuses_truncated_admission_field() {
        let remainder = HistoryRemainder {
            schema: ARCHIVE_SCHEMA,
            law: LAW_ID.into(),
            seed: 0,
            branch: "genesis".into(),
            genesis_digest: String::new(),
            genesis_bodies: BTreeMap::new(),
            genesis_families: vec![],
            interventions: vec![],
            clock: 0,
            bodies: BTreeMap::new(),
            families: vec![],
            signals: BTreeMap::new(),
            broadcasts: BTreeMap::new(),
            broadcast_receptions: BTreeMap::new(),
            emitter_sequence: BTreeMap::new(),
            contacts: BTreeSet::new(),
            actuator_momentum: Vec2::zero(),
            scheduled_courses: BTreeMap::new(),
            scheduled_range_courses: BTreeMap::new(),
            payload_hash: String::new(),
        };
        let json = serde_json::to_string(&remainder).unwrap();
        assert!(
            !json.contains("truncated_admission"),
            "Packet 5 truncated-law remainder field must not re-enter the selected schema"
        );
        assert_eq!(remainder.law, LAW_ID);
    }
}
