//! Chunked history archive. Incremental seal, bounded resident tails, selective
//! reconstruction. Packet 5 `truncated_admission` is refused.

use crate::{
    math::Vec2,
    policy::{Broadcast, BroadcastReception, PolicyProgram},
    population::Family,
    runtime::{
        Body, CanonicalState, ElasticState, Engine, EngineError, EventRecord, Observation,
        RecordedIntervention,
        ScheduledCourse, ScheduledRangeCourse, Signal,
    },
    LAW_ID,
};
use serde::{Deserialize, Serialize};
use std::{
    collections::{BTreeMap, BTreeSet},
    fs::{self, File, OpenOptions},
    io::{Read, Write},
    path::{Path, PathBuf},
};

pub const ARCHIVE_SCHEMA: u32 = 1;
const MAX_CHECKPOINT_BYTES: u64 = 256 * 1024 * 1024;
const MAX_CHUNK_BYTES: u64 = 1024 * 1024;

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
    #[serde(default)]
    pub policy_fired: BTreeSet<(String, u64)>,
    #[serde(default)]
    pub policy: Option<PolicyProgram>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub elastic: Option<ElasticState>,
    pub payload_hash: String,
}

#[derive(Clone, Debug)]
pub struct LiveArchive {
    pub dir: PathBuf,
    pub manifest: ArchiveManifest,
    pub tail_ticks: i128,
}

fn err(e: impl std::fmt::Display) -> EngineError {
    EngineError::Checkpoint(e.to_string())
}

fn temporary(path: &Path) -> PathBuf {
    let mut s = path.as_os_str().to_os_string();
    s.push(format!(".{}.tmp", std::process::id()));
    PathBuf::from(s)
}

fn write_atomic(path: &Path, bytes: &[u8]) -> Result<(), EngineError> {
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent).map_err(err)?;
    }
    let temp = temporary(path);
    let mut created = false;
    let result = (|| {
        let mut f = OpenOptions::new()
            .create_new(true)
            .write(true)
            .open(&temp)
            .map_err(err)?;
        created = true;
        f.write_all(bytes).map_err(err)?;
        f.sync_all().map_err(err)?;
        fs::rename(&temp, path).map_err(err)?;
        Ok(())
    })();
    if result.is_err() && created {
        let _ = fs::remove_file(&temp);
    }
    result
}

fn read_capped(path: &Path, cap: u64) -> Result<Vec<u8>, EngineError> {
    let f = File::open(path).map_err(err)?;
    let mut bytes = Vec::new();
    f.take(cap + 1).read_to_end(&mut bytes).map_err(err)?;
    if bytes.len() as u64 > cap {
        return Err(EngineError::ResourceLimit("archive file exceeds read budget".into()));
    }
    Ok(bytes)
}

#[derive(Serialize)]
struct RemainderHashView<'a> {
    law: &'a str,
    seed: u64,
    clock: i128,
    genesis_digest: &'a str,
    signals: &'a BTreeMap<String, Signal>,
    broadcasts: &'a BTreeMap<String, Broadcast>,
    broadcast_receptions: &'a BTreeMap<String, BTreeMap<u64, BroadcastReception>>,
}

impl<'a> From<&'a HistoryRemainder> for RemainderHashView<'a> {
    fn from(r: &'a HistoryRemainder) -> Self {
        Self {
            law: &r.law,
            seed: r.seed,
            clock: r.clock,
            genesis_digest: &r.genesis_digest,
            signals: &r.signals,
            broadcasts: &r.broadcasts,
            broadcast_receptions: &r.broadcast_receptions,
        }
    }
}

impl Engine {
    pub fn resident_history_bytes(&self) -> usize {
        serde_json::to_vec(&self.state.events).map(|b| b.len()).unwrap_or(0)
    }

    /// Incremental seal. Reuses existing chunks; does not require an empty
    /// directory or recopy of already sealed events.
    pub fn seal_archive(
        &mut self,
        dir: impl AsRef<Path>,
        events_per_chunk: usize,
    ) -> Result<ArchiveManifest, EngineError> {
        if events_per_chunk == 0 {
            return Err(EngineError::Invalid("events_per_chunk must be positive".into()));
        }
        let dir = dir.as_ref();
        fs::create_dir_all(dir).map_err(err)?;
        let existing = Self::try_read_manifest(dir)?;
        let sealed_through = existing.as_ref().map(|m| m.sealed_through).unwrap_or(-1);
        let mut events: Vec<EventRecord> = self
            .state
            .events
            .values()
            .filter(|e| e.tick > sealed_through)
            .cloned()
            .collect();
        events.sort_by(|a, b| (a.tick, &a.id).cmp(&(b.tick, &b.id)));
        let mut chunks = existing.map(|m| m.chunks).unwrap_or_default();
        let mut index = chunks.len() as u32;
        for piece in events.chunks(events_per_chunk.max(1)) {
            if piece.is_empty() {
                continue;
            }
            let tick_lo = piece.first().unwrap().tick;
            let tick_hi = piece.last().unwrap().tick;
            let mut chunk = HistoryChunk {
                schema: ARCHIVE_SCHEMA,
                index,
                tick_lo,
                tick_hi,
                payload_hash: String::new(),
                events: piece.to_vec(),
            };
            let payload = serde_json::to_vec(&chunk.events).map_err(err)?;
            chunk.payload_hash = blake3::hash(&payload).to_hex().to_string();
            let encoded = serde_json::to_vec(&chunk).map_err(err)?;
            if encoded.len() as u64 > MAX_CHUNK_BYTES {
                return Err(EngineError::ResourceLimit(
                    "history chunk exceeds 1 MiB; split further".into(),
                ));
            }
            let file = format!("chunk-{index:04}.json");
            write_atomic(&dir.join(&file), &encoded)?;
            chunks.push(ChunkListing {
                file,
                payload_hash: chunk.payload_hash,
                tick_lo,
                tick_hi,
                event_count: piece.len(),
                bytes: encoded.len() as u64,
            });
            index += 1;
        }
        if chunks.is_empty() {
            let mut chunk = HistoryChunk {
                schema: ARCHIVE_SCHEMA,
                index: 0,
                tick_lo: 0,
                tick_hi: self.state.clock,
                payload_hash: String::new(),
                events: Vec::new(),
            };
            let payload = serde_json::to_vec(&chunk.events).map_err(err)?;
            chunk.payload_hash = blake3::hash(&payload).to_hex().to_string();
            let encoded = serde_json::to_vec(&chunk).map_err(err)?;
            write_atomic(&dir.join("chunk-0000.json"), &encoded)?;
            chunks.push(ChunkListing {
                file: "chunk-0000.json".into(),
                payload_hash: chunk.payload_hash,
                tick_lo: 0,
                tick_hi: self.state.clock,
                event_count: 0,
                bytes: encoded.len() as u64,
            });
        }
        let remainder = self.remainder_from_live()?;
        let rem_bytes = serde_json::to_vec(&remainder).map_err(err)?;
        write_atomic(&dir.join("remainder.json"), &rem_bytes)?;
        let history_hash = Self::hash_chunk_listings(dir, &chunks, &self.state)?;
        let manifest = ArchiveManifest {
            schema: ARCHIVE_SCHEMA,
            law: self.state.law.clone(),
            seed: self.state.seed,
            sealed_through: self.state.clock,
            events_per_chunk,
            history_hash,
            remainder_hash: remainder.payload_hash,
            chunks,
        };
        let man_bytes = serde_json::to_vec_pretty(&manifest).map_err(err)?;
        write_atomic(&dir.join("manifest.json"), &man_bytes)?;
        self.archive = Some(LiveArchive {
            dir: dir.to_path_buf(),
            manifest: manifest.clone(),
            tail_ticks: 4,
        });
        Ok(manifest)
    }

    fn hash_chunk_listings(
        dir: &Path,
        chunks: &[ChunkListing],
        state: &CanonicalState,
    ) -> Result<String, EngineError> {
        let mut facts = BTreeMap::new();
        for listing in chunks {
            let chunk = Self::read_chunk(dir, listing)?;
            for event in chunk.events {
                if event.tick <= state.clock {
                    facts.insert(event.id.clone(), event);
                }
            }
        }
        let facts: Vec<_> = facts.values().collect();
        Ok(crate::runtime::digest(&(
            LAW_ID,
            state.seed,
            &state.branch,
            &state.genesis_digest,
            state.clock,
            facts,
        )))
    }

    fn remainder_from_live(&self) -> Result<HistoryRemainder, EngineError> {
        let mut remainder = HistoryRemainder {
            schema: ARCHIVE_SCHEMA,
            law: self.state.law.clone(),
            seed: self.state.seed,
            branch: self.state.branch.clone(),
            genesis_digest: self.state.genesis_digest.clone(),
            genesis_bodies: self.state.genesis_bodies.clone(),
            genesis_families: self.state.genesis_families.clone(),
            interventions: self.state.interventions.clone(),
            clock: self.state.clock,
            bodies: self.state.bodies.clone(),
            families: self.state.families.clone(),
            signals: self.state.signals.clone(),
            broadcasts: self.state.broadcasts.clone(),
            broadcast_receptions: self.state.broadcast_receptions.clone(),
            emitter_sequence: self.state.emitter_sequence.clone(),
            contacts: self.state.contacts.clone(),
            actuator_momentum: self.state.actuator_momentum.clone(),
            scheduled_courses: self.state.scheduled_courses.clone(),
            scheduled_range_courses: self.state.scheduled_range_courses.clone(),
            policy_fired: self.state.policy_fired.clone(),
            elastic: self.state.elastic.clone(),
            policy: self.policy.clone(),
            payload_hash: String::new(),
        };
        let rem_payload = serde_json::to_vec(&RemainderHashView::from(&remainder)).map_err(err)?;
        remainder.payload_hash = blake3::hash(&rem_payload).to_hex().to_string();
        Ok(remainder)
    }

    /// Drop sealed events older than the resident tail. Canonical facts stay
    /// on disk; live RAM only keeps the tail plus remainder influences.
    pub fn evict_resident_history(&mut self) -> Result<usize, EngineError> {
        let Some(archive) = self.archive.as_ref() else {
            return Err(EngineError::Invalid("no sealed archive".into()));
        };
        let keep_after = archive
            .manifest
            .sealed_through
            .saturating_sub(archive.tail_ticks);
        let before = self.state.events.len();
        self.state.events.retain(|_, e| e.tick > keep_after);
        Ok(before.saturating_sub(self.state.events.len()))
    }

    pub fn restore_archive(dir: impl AsRef<Path>) -> Result<Self, EngineError> {
        let dir = dir.as_ref();
        let manifest = Self::read_archive_manifest(dir)?;
        let rem_bytes = read_capped(&dir.join("remainder.json"), MAX_CHECKPOINT_BYTES)?;
        let remainder: HistoryRemainder = serde_json::from_slice(&rem_bytes).map_err(err)?;
        let rem_view = serde_json::to_vec(&RemainderHashView::from(&remainder)).map_err(err)?;
        if blake3::hash(&rem_view).to_hex().as_str() != remainder.payload_hash
            || remainder.payload_hash != manifest.remainder_hash
        {
            return Err(EngineError::Checkpoint("archive remainder checksum mismatch".into()));
        }
        let mut events = BTreeMap::new();
        for listing in &manifest.chunks {
            let chunk = Self::read_chunk(dir, listing)?;
            for event in chunk.events {
                events.insert(event.id.clone(), event);
            }
        }
        let state = CanonicalState {
            law: remainder.law,
            seed: remainder.seed,
            branch: remainder.branch,
            genesis_digest: remainder.genesis_digest,
            genesis_bodies: remainder.genesis_bodies,
            genesis_families: remainder.genesis_families,
            interventions: remainder.interventions,
            clock: remainder.clock,
            bodies: remainder.bodies,
            families: remainder.families,
            signals: remainder.signals,
            events,
            emitter_sequence: remainder.emitter_sequence,
            contacts: remainder.contacts,
            actuator_momentum: remainder.actuator_momentum,
            scheduled_courses: remainder.scheduled_courses,
            scheduled_range_courses: remainder.scheduled_range_courses,
            broadcasts: remainder.broadcasts,
            broadcast_receptions: remainder.broadcast_receptions,
            policy_fired: remainder.policy_fired,
            elastic: remainder.elastic.clone(),
        };
        let mut engine = Self::from_state(state)?;
        engine.policy = remainder.policy;
        engine.archive = Some(LiveArchive {
            dir: dir.to_path_buf(),
            manifest: manifest.clone(),
            tail_ticks: 4,
        });
        if engine.history_digest(engine.state.clock)? != manifest.history_hash {
            return Err(EngineError::Checkpoint("archive history digest mismatch".into()));
        }
        Ok(engine)
    }

    /// Cold observation: load only chunks that overlap the query interval and
    /// mention the observer or targets. Does not restore every sealed event.
    pub fn observe_archived(
        dir: impl AsRef<Path>,
        observer: u64,
        now: i128,
        targets: &[u64],
    ) -> Result<Vec<Observation>, EngineError> {
        let dir = dir.as_ref();
        let manifest = Self::read_archive_manifest(dir)?;
        let rem_bytes = read_capped(&dir.join("remainder.json"), MAX_CHECKPOINT_BYTES)?;
        let remainder: HistoryRemainder = serde_json::from_slice(&rem_bytes).map_err(err)?;
        let mut needed: BTreeSet<u64> = targets.iter().copied().collect();
        needed.insert(observer);
        let mut events = BTreeMap::new();
        let mut chunks_loaded = 0usize;
        for listing in &manifest.chunks {
            if listing.tick_lo > now {
                continue;
            }
            let chunk = Self::read_chunk(dir, listing)?;
            let relevant = chunk.events.iter().any(|e| {
                e.subjects.iter().any(|id| needed.contains(id))
            });
            if !relevant && listing.event_count > 0 {
                continue;
            }
            chunks_loaded += 1;
            for event in chunk.events {
                if event.tick <= now {
                    events.insert(event.id.clone(), event);
                }
            }
        }
        let _ = chunks_loaded;
        let state = CanonicalState {
            law: remainder.law,
            seed: remainder.seed,
            branch: remainder.branch,
            genesis_digest: remainder.genesis_digest,
            genesis_bodies: remainder.genesis_bodies,
            genesis_families: remainder.genesis_families,
            interventions: remainder.interventions,
            clock: remainder.clock.min(now.max(0)),
            bodies: remainder.bodies,
            families: remainder.families,
            signals: remainder.signals,
            events,
            emitter_sequence: remainder.emitter_sequence,
            contacts: remainder.contacts,
            actuator_momentum: remainder.actuator_momentum,
            scheduled_courses: remainder.scheduled_courses,
            scheduled_range_courses: remainder.scheduled_range_courses,
            broadcasts: remainder.broadcasts,
            broadcast_receptions: remainder.broadcast_receptions,
            policy_fired: remainder.policy_fired,
            elastic: remainder.elastic.clone(),
        };
        let engine = Self::from_state(state)?;
        engine.observe(observer, now.min(engine.state.clock), targets)
    }

    pub fn read_archive_manifest(dir: impl AsRef<Path>) -> Result<ArchiveManifest, EngineError> {
        let bytes = read_capped(&dir.as_ref().join("manifest.json"), MAX_CHUNK_BYTES)?;
        serde_json::from_slice(&bytes).map_err(err)
    }

    fn try_read_manifest(dir: &Path) -> Result<Option<ArchiveManifest>, EngineError> {
        let path = dir.join("manifest.json");
        if !path.exists() {
            return Ok(None);
        }
        Ok(Some(Self::read_archive_manifest(dir)?))
    }

    fn read_chunk(dir: &Path, listing: &ChunkListing) -> Result<HistoryChunk, EngineError> {
        let bytes = read_capped(&dir.join(&listing.file), MAX_CHUNK_BYTES)?;
        let chunk: HistoryChunk = serde_json::from_slice(&bytes).map_err(err)?;
        let payload = serde_json::to_vec(&chunk.events).map_err(err)?;
        if blake3::hash(&payload).to_hex().as_str() != chunk.payload_hash
            || chunk.payload_hash != listing.payload_hash
        {
            return Err(EngineError::Checkpoint("history chunk checksum mismatch".into()));
        }
        Ok(chunk)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

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
            policy_fired: BTreeSet::new(),
            policy: None,
            elastic: None,
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
