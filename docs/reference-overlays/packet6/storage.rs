//! Atomic, checksummed checkpoints and chunked history archives.
//! Derived search state is intentionally rebuilt. Incoming and outgoing
//! influences live in the remainder so sealing a chunk does not drop them.
use crate::{
    runtime::{
        Broadcast, BroadcastReception, CanonicalState, Engine, EngineError, EventRecord, Signal,
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

const MAX_CHECKPOINT_BYTES: u64 = 256 * 1024 * 1024;
/// Individual history chunks stay far below the checkpoint blob limit.
const MAX_CHUNK_BYTES: u64 = 1024 * 1024;
const ARCHIVE_SCHEMA: u32 = 1;

#[derive(Serialize, Deserialize)]
struct Envelope {
    schema: u32,
    law: String,
    payload_hash: String,
    history_hash: String,
    payload: String,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ChunkListing {
    pub file: String,
    pub payload_hash: String,
    pub tick_lo: i128,
    pub tick_hi: i128,
    pub event_count: usize,
    pub bytes: u64,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
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

#[derive(Clone, Debug, Serialize, Deserialize)]
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
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct HistoryRemainder {
    pub schema: u32,
    pub law: String,
    pub seed: u64,
    pub branch: String,
    pub genesis_digest: String,
    pub genesis_bodies: BTreeMap<u64, crate::runtime::Body>,
    pub genesis_families: Vec<crate::population::Family>,
    pub interventions: Vec<crate::runtime::RecordedIntervention>,
    pub clock: i128,
    pub bodies: BTreeMap<u64, crate::runtime::Body>,
    pub families: Vec<crate::population::Family>,
    pub signals: BTreeMap<String, Signal>,
    pub broadcasts: BTreeMap<String, Broadcast>,
    pub broadcast_receptions: BTreeMap<String, BTreeMap<u64, BroadcastReception>>,
    pub emitter_sequence: BTreeMap<u64, u64>,
    pub contacts: BTreeSet<(u64, u64, u64, u64)>,
    pub actuator_momentum: crate::math::Vec2,
    pub scheduled_courses: BTreeMap<String, crate::runtime::ScheduledCourse>,
    pub scheduled_range_courses: BTreeMap<String, crate::runtime::ScheduledRangeCourse>,
    pub truncated_admission: Option<crate::truncated_gem::TruncatedAdmission>,
    pub payload_hash: String,
}

fn temporary(path: &Path) -> PathBuf {
    let mut s = path.as_os_str().to_os_string();
    s.push(format!(".{}.tmp", std::process::id()));
    PathBuf::from(s)
}

fn write_atomic(path: &Path, bytes: &[u8]) -> Result<(), EngineError> {
    let parent = path
        .parent()
        .filter(|p| !p.as_os_str().is_empty())
        .unwrap_or(Path::new("."));
    fs::create_dir_all(parent).map_err(err)?;
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
        File::open(parent).and_then(|f| f.sync_all()).map_err(err)?;
        Ok(())
    })();
    if result.is_err() && created {
        let _ = fs::remove_file(&temp);
    }
    result
}

fn read_capped(path: &Path, cap: u64) -> Result<Vec<u8>, EngineError> {
    let f = File::open(path).map_err(err)?;
    if f.metadata().map_err(err)?.len() > cap {
        return Err(EngineError::ResourceLimit(
            "archive file exceeds read budget".into(),
        ));
    }
    let mut bytes = Vec::new();
    f.take(cap + 1).read_to_end(&mut bytes).map_err(err)?;
    if bytes.len() as u64 > cap {
        return Err(EngineError::ResourceLimit(
            "archive file grew beyond read budget".into(),
        ));
    }
    Ok(bytes)
}

impl Engine {
    pub fn checkpoint(&self, path: impl AsRef<Path>) -> Result<(), EngineError> {
        let path = path.as_ref();
        let payload = serde_json::to_string(&self.state).map_err(err)?;
        let envelope = Envelope {
            schema: 1,
            law: self.state.law.clone(),
            payload_hash: blake3::hash(payload.as_bytes()).to_hex().to_string(),
            history_hash: self.history_digest(self.state.clock)?,
            payload,
        };
        let encoded = serde_json::to_vec(&envelope).map_err(err)?;
        if encoded.len() as u64 > MAX_CHECKPOINT_BYTES {
            return Err(EngineError::ResourceLimit(
                "checkpoint size exceeds 256 MiB; chunked archive required".into(),
            ));
        }
        write_atomic(path, &encoded)
    }
    pub fn restore(path: impl AsRef<Path>) -> Result<Self, EngineError> {
        let bytes = read_capped(path.as_ref(), MAX_CHECKPOINT_BYTES)?;
        let envelope: Envelope = serde_json::from_slice(&bytes).map_err(err)?;
        if envelope.schema != 1
            || (envelope.law != LAW_ID && envelope.law != crate::TRUNCATED_COUPLED_LAW_ID)
        {
            return Err(EngineError::Unsupported(
                "checkpoint schema/law migration required".into(),
            ));
        }
        if blake3::hash(envelope.payload.as_bytes()).to_hex().as_str() != envelope.payload_hash {
            return Err(EngineError::Checkpoint("payload checksum mismatch".into()));
        }
        let state: CanonicalState = serde_json::from_str(&envelope.payload).map_err(err)?;
        let engine = Self::from_state(state)?;
        if engine.history_digest(engine.state.clock)? != envelope.history_hash {
            return Err(EngineError::Checkpoint("history digest mismatch".into()));
        }
        Ok(engine)
    }
    pub fn verify_checkpoint(path: impl AsRef<Path>) -> Result<String, EngineError> {
        let e = Self::restore(path)?;
        e.history_digest(e.state.clock)
    }

    /// Seal committed history into checksummed chunks plus a remainder of
    /// incoming/outgoing influences. The manifest is replaced last.
    pub fn seal_archive(
        &self,
        dir: impl AsRef<Path>,
        events_per_chunk: usize,
    ) -> Result<ArchiveManifest, EngineError> {
        if events_per_chunk == 0 {
            return Err(EngineError::Invalid(
                "events_per_chunk must be positive".into(),
            ));
        }
        let dir = dir.as_ref();
        if dir.exists() {
            if dir.read_dir().map_err(err)?.next().is_some() {
                return Err(EngineError::Invalid(
                    "archive directory must be empty".into(),
                ));
            }
        } else {
            fs::create_dir_all(dir).map_err(err)?;
        }
        let mut events: Vec<EventRecord> = self.state.events.values().cloned().collect();
        events.sort_by(|a, b| (a.tick, &a.id).cmp(&(b.tick, &b.id)));
        let mut chunks = Vec::new();
        for (index, piece) in events.chunks(events_per_chunk).enumerate() {
            let tick_lo = piece.first().map(|e| e.tick).unwrap_or(self.state.clock);
            let tick_hi = piece.last().map(|e| e.tick).unwrap_or(self.state.clock);
            let mut chunk = HistoryChunk {
                schema: ARCHIVE_SCHEMA,
                index: index as u32,
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
                payload_hash: chunk.payload_hash.clone(),
                tick_lo,
                tick_hi,
                event_count: piece.len(),
                bytes: encoded.len() as u64,
            });
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
            truncated_admission: self.state.truncated_admission.clone(),
            payload_hash: String::new(),
        };
        let rem_payload = serde_json::to_vec(&RemainderHashView::from(&remainder)).map_err(err)?;
        remainder.payload_hash = blake3::hash(&rem_payload).to_hex().to_string();
        let rem_bytes = serde_json::to_vec(&remainder).map_err(err)?;
        if rem_bytes.len() as u64 > MAX_CHECKPOINT_BYTES {
            return Err(EngineError::ResourceLimit(
                "archive remainder exceeds 256 MiB".into(),
            ));
        }
        write_atomic(&dir.join("remainder.json"), &rem_bytes)?;
        let manifest = ArchiveManifest {
            schema: ARCHIVE_SCHEMA,
            law: self.state.law.clone(),
            seed: self.state.seed,
            sealed_through: self.state.clock,
            events_per_chunk,
            history_hash: self.history_digest(self.state.clock)?,
            remainder_hash: remainder.payload_hash,
            chunks,
        };
        let man_bytes = serde_json::to_vec_pretty(&manifest).map_err(err)?;
        write_atomic(&dir.join("manifest.json"), &man_bytes)?;
        Ok(manifest)
    }

    pub fn restore_archive(dir: impl AsRef<Path>) -> Result<Self, EngineError> {
        let dir = dir.as_ref();
        let man_bytes = read_capped(&dir.join("manifest.json"), MAX_CHUNK_BYTES)?;
        let manifest: ArchiveManifest = serde_json::from_slice(&man_bytes).map_err(err)?;
        if manifest.schema != ARCHIVE_SCHEMA
            || (manifest.law != LAW_ID && manifest.law != crate::TRUNCATED_COUPLED_LAW_ID)
        {
            return Err(EngineError::Unsupported(
                "archive schema/law migration required".into(),
            ));
        }
        let rem_bytes = read_capped(&dir.join("remainder.json"), MAX_CHECKPOINT_BYTES)?;
        let remainder: HistoryRemainder = serde_json::from_slice(&rem_bytes).map_err(err)?;
        let rem_view = serde_json::to_vec(&RemainderHashView::from(&remainder)).map_err(err)?;
        if blake3::hash(&rem_view).to_hex().as_str() != remainder.payload_hash
            || remainder.payload_hash != manifest.remainder_hash
        {
            return Err(EngineError::Checkpoint(
                "archive remainder checksum mismatch".into(),
            ));
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
            truncated_admission: remainder.truncated_admission,
            broadcasts: remainder.broadcasts,
            broadcast_receptions: remainder.broadcast_receptions,
        };
        let engine = Self::from_state(state)?;
        if engine.history_digest(engine.state.clock)? != manifest.history_hash {
            return Err(EngineError::Checkpoint("archive history digest mismatch".into()));
        }
        Ok(engine)
    }

    /// Reconstruct an old observation from a sealed archive. Uses restored
    /// worldtubes plus sealed event chunks; does not consult a live engine.
    pub fn reconstruct_observations(
        dir: impl AsRef<Path>,
        observer: u64,
        now: i128,
        targets: &[u64],
    ) -> Result<Vec<crate::runtime::Observation>, EngineError> {
        let restored = Self::restore_archive(dir)?;
        restored.observe(observer, now, targets)
    }

    pub fn read_archive_manifest(dir: impl AsRef<Path>) -> Result<ArchiveManifest, EngineError> {
        let bytes = read_capped(&dir.as_ref().join("manifest.json"), MAX_CHUNK_BYTES)?;
        serde_json::from_slice(&bytes).map_err(err)
    }

    pub fn read_archive_chunk(
        dir: impl AsRef<Path>,
        index: usize,
    ) -> Result<HistoryChunk, EngineError> {
        let manifest = Self::read_archive_manifest(&dir)?;
        let listing = manifest
            .chunks
            .get(index)
            .ok_or_else(|| EngineError::Invalid("archive chunk index".into()))?;
        Self::read_chunk(dir.as_ref(), listing)
    }

    fn read_chunk(dir: &Path, listing: &ChunkListing) -> Result<HistoryChunk, EngineError> {
        let bytes = read_capped(&dir.join(&listing.file), MAX_CHUNK_BYTES)?;
        let chunk: HistoryChunk = serde_json::from_slice(&bytes).map_err(err)?;
        let payload = serde_json::to_vec(&chunk.events).map_err(err)?;
        if blake3::hash(&payload).to_hex().as_str() != chunk.payload_hash
            || chunk.payload_hash != listing.payload_hash
        {
            return Err(EngineError::Checkpoint(
                "history chunk checksum mismatch".into(),
            ));
        }
        Ok(chunk)
    }
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
    scheduled_courses: &'a BTreeMap<String, crate::runtime::ScheduledCourse>,
    scheduled_range_courses: &'a BTreeMap<String, crate::runtime::ScheduledRangeCourse>,
    actuator_momentum: &'a crate::math::Vec2,
    contacts: &'a BTreeSet<(u64, u64, u64, u64)>,
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
            scheduled_courses: &r.scheduled_courses,
            scheduled_range_courses: &r.scheduled_range_courses,
            actuator_momentum: &r.actuator_momentum,
            contacts: &r.contacts,
        }
    }
}

fn err(e: impl std::fmt::Display) -> EngineError {
    EngineError::Checkpoint(e.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn checkpoint_roundtrip_corruption_and_law_rejection() {
        let mut e = crate::scenario::causal_relay().unwrap();
        e.advance_fully(40).unwrap();
        let p = std::env::temp_dir().join(format!("es-storage-{}.checkpoint", std::process::id()));
        e.checkpoint(&p).unwrap();
        let restored = Engine::restore(&p).unwrap();
        assert_eq!(
            e.history_digest(40).unwrap(),
            restored.history_digest(40).unwrap()
        );
        let mut v: serde_json::Value = serde_json::from_slice(&fs::read(&p).unwrap()).unwrap();
        v["payload"] = serde_json::Value::String("{}".into());
        fs::write(&p, serde_json::to_vec(&v).unwrap()).unwrap();
        assert!(Engine::restore(&p).is_err());
        e.checkpoint(&p).unwrap();
        v = serde_json::from_slice(&fs::read(&p).unwrap()).unwrap();
        v["law"] = "other-law".into();
        fs::write(&p, serde_json::to_vec(&v).unwrap()).unwrap();
        assert!(matches!(
            Engine::restore(&p),
            Err(EngineError::Unsupported(_))
        ));
        let _ = fs::remove_file(p);
    }
}
