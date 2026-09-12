//! Atomic, checksummed checkpoints. Derived search state is intentionally rebuilt.
use crate::{
    runtime::{CanonicalState, Engine, EngineError},
    LAW_ID,
};
use serde::{Deserialize, Serialize};
use std::{
    fs::{self, File, OpenOptions},
    io::{Read, Write},
    path::{Path, PathBuf},
};

const MAX_CHECKPOINT_BYTES: u64 = 256 * 1024 * 1024;
#[derive(Serialize, Deserialize)]
struct Envelope {
    schema: u32,
    law: String,
    payload_hash: String,
    history_hash: String,
    payload: String,
}
fn temporary(path: &Path) -> PathBuf {
    let mut s = path.as_os_str().to_os_string();
    s.push(format!(".{}.tmp", std::process::id()));
    PathBuf::from(s)
}
impl Engine {
    pub fn checkpoint(&self, path: impl AsRef<Path>) -> Result<(), EngineError> {
        let path = path.as_ref();
        let payload = serde_json::to_string(&self.state).map_err(err)?;
        let envelope = Envelope {
            schema: 1,
            law: LAW_ID.into(),
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
            f.write_all(&encoded).map_err(err)?;
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
    pub fn restore(path: impl AsRef<Path>) -> Result<Self, EngineError> {
        let f = File::open(path).map_err(err)?;
        if f.metadata().map_err(err)?.len() > MAX_CHECKPOINT_BYTES {
            return Err(EngineError::ResourceLimit(
                "checkpoint exceeds read budget".into(),
            ));
        }
        let mut bytes = Vec::new();
        f.take(MAX_CHECKPOINT_BYTES + 1)
            .read_to_end(&mut bytes)
            .map_err(err)?;
        if bytes.len() as u64 > MAX_CHECKPOINT_BYTES {
            return Err(EngineError::ResourceLimit(
                "checkpoint grew beyond read budget".into(),
            ));
        }
        let envelope: Envelope = serde_json::from_slice(&bytes).map_err(err)?;
        if envelope.schema != 1 || envelope.law != LAW_ID {
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
