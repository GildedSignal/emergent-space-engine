//! The flight recorder: every flight the player makes is a test nobody scripted ("i just don't want it buggy").
//!
//! A flight is its inputs, never its states: `artifacts/flights/<UTC time>-seed<N>.json`, kilobytes. Replay is exact
//! (`Universe::schedule(t, word)` at the logged ticks reproduces a flight bit for bit), so the file plus the commit
//! that wrote it is the whole flight. [`super::replay`] plays it back and compares.
//!
//! **When it is written** (off the frame thread: the frame builds the text and a writer thread puts it on disk, atomically):
//! at the first frame, at every decision, every [`EVERY`] seconds of wall time, and at the end: exit, restart, loss, or a
//! panic in the engine.
//!
//! **The digest.** A live session cannot be settled to a cut without moving the player's present, so:
//! - at exit and restart the live universe is settled to the canonical cut ([`canonical_cut`]) and digested (`digest_source`
//!   "live": the flight as flown, observation and wall budget included);
//! - at a loss the flight is over but the page goes on showing the wreck, so the digest is taken by replaying the log on a
//!   shadow universe in a thread (`digest_source` "shadow"). The loss itself (reason, tick) is the live universe's, and the
//!   shadow's must agree with it: a difference is written in `note`.
//! A file written mid-flight (a crash, a kill) has no digest, and says so (`end` is null).
use super::replay::{replay, Replayed};
use super::session::Session;
use emergent_universe::num::Tick;
use emergent_universe::universe::Universe;
use emergent_universe::view::View;
use serde::{Deserialize, Serialize};
use std::path::{Path, PathBuf};
use std::sync::mpsc::{channel, Sender};
use std::sync::OnceLock;
use std::thread::JoinHandle;
use std::time::Instant;

pub const FORMAT: &str = "es-flight-v1";
/// The plane's log version (kept: `GET /log` has always said so).
pub const VERSION: &str = "es-plane-v0";
/// The law in force (docs/law.md). Its code's own identity is [`Meta::law_hash`].
pub const LAW: &str = "es-space-v2";
/// Wall seconds between two writes of a flight in progress.
pub const EVERY: f64 = 10.0;
/// Wall seconds a restart or an exit waits for a lost flight's shadow digest.
pub const SHADOW_WAIT: f64 = 10.0;

/// Why the ship was lost: the engine's own words, and the tick of its last state.
#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct Loss {
    pub reason: String,
    pub tick: Tick,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Flight {
    #[serde(default)]
    pub format: String,
    #[serde(default)]
    pub version: String,
    #[serde(default)]
    pub law: String,
    /// Identity of the law's code: a hash of the sources the universe is built from (not of the commit: a docs commit leaves it).
    #[serde(default)]
    pub law_hash: String,
    #[serde(default)]
    pub commit: String,
    #[serde(default)]
    pub dirty: bool,
    #[serde(default)]
    pub started_utc: String,
    pub seed: u64,
    #[serde(default)]
    pub rtf: f64,
    #[serde(default = "default_members")]
    pub members: u64,
    #[serde(default = "default_threads")]
    pub threads: usize,
    /// The decisions at their canonical ticks: the whole flight.
    pub inputs: Vec<(Tick, u8)>,
    pub presented_tick: Tick,
    /// The canonical cut the digest is taken at (never before the presented tick).
    #[serde(default)]
    pub cut_tick: Option<Tick>,
    /// How the flight ended: "exit", "restart", "loss" or "panic". Null: it was cut off (the file is the last write).
    #[serde(default)]
    pub end: Option<String>,
    #[serde(default)]
    pub loss: Option<Loss>,
    /// Refusals the player's body met, and those of every other body.
    #[serde(default)]
    pub refusals: u64,
    #[serde(default)]
    pub other_refusals: u64,
    #[serde(default)]
    pub digest: Option<String>,
    /// "live" (the universe as flown) or "shadow" (the log replayed while the page went on).
    #[serde(default)]
    pub digest_source: Option<String>,
    #[serde(default)]
    pub note: Option<String>,
}

fn default_members() -> u64 {
    48
}
fn default_threads() -> usize {
    1
}

/// The tick every body and fleet is resolved up to, or the present if later: the cut a digest is taken at. A live frame may
/// resolve a body past the presented tick (when another reads it), and the digest of a universe settled only to the presented
/// tick would then differ from a replay's; settled to a cut no body is past, it cannot (docs/law.md, "Ties").
pub fn canonical_cut(u: &Universe) -> Tick {
    let mut cut = u.now;
    for i in 0..u.n_bodies() {
        cut = cut.max(u.bodies().event_time(i));
    }
    for f in &u.fleets {
        cut = cut.max(f.tick());
    }
    cut
}

/// What identifies the code and the tree a flight was recorded on.
#[derive(Clone, Debug)]
pub struct Meta {
    pub commit: String,
    pub dirty: bool,
    pub law_hash: String,
}

pub fn repo_root() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap_or(Path::new(".")).to_path_buf()
}

/// Where flights live: committed (inputs only), `artifacts/flights/`.
pub fn default_dir() -> PathBuf {
    repo_root().join("artifacts").join("flights")
}

pub fn meta() -> &'static Meta {
    static META: OnceLock<Meta> = OnceLock::new();
    META.get_or_init(|| {
        let root = repo_root();
        let git = |args: &[&str]| std::process::Command::new("git").args(args).current_dir(&root).output().ok().filter(|o| o.status.success()).map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string());
        // The flights directory is written by the sessions themselves: it must not make the tree dirty.
        let dirty = git(&["status", "--porcelain", "--", ".", ":!artifacts/flights"]).map_or(true, |s| !s.is_empty());
        Meta { commit: git(&["rev-parse", "HEAD"]).unwrap_or_else(|| "unknown".into()), dirty, law_hash: law_hash(&root) }
    })
}

/// A hash of the Rust sources and manifests of `emergent-universe` and of every crate it depends on, by path: the law's code.
fn law_hash(root: &Path) -> String {
    fn walk(dir: &Path, out: &mut Vec<PathBuf>) {
        let Ok(rd) = std::fs::read_dir(dir) else { return };
        let mut entries: Vec<_> = rd.filter_map(|e| e.ok().map(|e| e.path())).collect();
        entries.sort();
        for p in entries {
            if p.is_dir() {
                walk(&p, out);
            } else if p.extension().is_some_and(|e| e == "rs") {
                out.push(p);
            }
        }
    }
    let mut todo = vec!["universe".to_string()];
    let mut done: Vec<String> = Vec::new();
    while let Some(name) = todo.pop() {
        if done.contains(&name) {
            continue;
        }
        if let Ok(toml) = std::fs::read_to_string(root.join("crates").join(&name).join("Cargo.toml")) {
            for line in toml.lines() {
                if let Some(rest) = line.split("path = \"../").nth(1) {
                    if let Some(dep) = rest.split('"').next() {
                        todo.push(dep.to_string());
                    }
                }
            }
        }
        done.push(name);
    }
    done.sort();
    let mut h = blake3::Hasher::new();
    for name in &done {
        let base = root.join("crates").join(name);
        let mut files = vec![base.join("Cargo.toml")];
        walk(&base.join("src"), &mut files);
        for f in files {
            h.update(f.strip_prefix(root).unwrap_or(&f).to_string_lossy().as_bytes());
            h.update(&std::fs::read(&f).unwrap_or_default());
        }
    }
    h.finalize().to_hex()[..16].to_string()
}

/// `YYYYMMDDTHHMMSSZ`-style stamps from the wall clock: (file-name form, readable form).
pub fn utc_now() -> (String, String) {
    let secs = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).map_or(0, |d| d.as_secs()) as i64;
    let (days, rem) = (secs.div_euclid(86_400), secs.rem_euclid(86_400));
    // Howard Hinnant's civil-from-days.
    let z = days + 719_468;
    let era = z.div_euclid(146_097);
    let doe = z.rem_euclid(146_097);
    let yoe = (doe - doe / 1460 + doe / 36_524 - doe / 146_096) / 365;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let (d, m) = (doy - (153 * mp + 2) / 5 + 1, if mp < 10 { mp + 3 } else { mp - 9 });
    let y = yoe + era * 400 + (m <= 2) as i64;
    let (hh, mm, ss) = (rem / 3600, rem % 3600 / 60, rem % 60);
    (format!("{y:04}{m:02}{d:02}T{hh:02}{mm:02}{ss:02}Z"), format!("{y:04}-{m:02}-{d:02}T{hh:02}:{mm:02}:{ss:02}Z"))
}

/// A writer thread: the frame hands it the text and goes on. It keeps the last text queued (the file is a snapshot), and a
/// file is never half written (a temporary, then a rename).
struct Writer {
    tx: Sender<String>,
    handle: JoinHandle<()>,
}

impl Writer {
    fn spawn(path: PathBuf) -> Self {
        let (tx, rx) = channel::<String>();
        let handle = std::thread::spawn(move || {
            let mut warned = false;
            while let Ok(mut text) = rx.recv() {
                while let Ok(newer) = rx.try_recv() {
                    text = newer;
                }
                let tmp = path.with_extension("json.tmp");
                let done = path.parent().map_or(Ok(()), std::fs::create_dir_all).and_then(|_| std::fs::write(&tmp, &text)).and_then(|_| std::fs::rename(&tmp, &path));
                if let (Err(e), false) = (done, warned) {
                    warned = true;
                    eprintln!("flight recorder: cannot write {}: {e} (the flight goes on, unrecorded)", path.display());
                }
            }
        });
        Self { tx, handle }
    }
}

pub struct Recorder {
    dir: PathBuf,
    path: PathBuf,
    flight: Flight,
    writer: Option<Writer>,
    last_write: Instant,
    seen_inputs: usize,
    /// Lost: the flight is over, and the file keeps the log as it was at the loss.
    frozen: bool,
    shadow: Option<JoinHandle<Result<Replayed, String>>>,
}

impl Recorder {
    pub fn new(dir: PathBuf, seed: u64, rtf: f64, members: u64, threads: usize) -> Self {
        let (stamp, readable) = utc_now();
        let m = meta();
        let mut path = dir.join(format!("{stamp}-seed{seed}.json"));
        let mut n = 2;
        while path.exists() {
            path = dir.join(format!("{stamp}-seed{seed}-{n}.json"));
            n += 1;
        }
        let flight = Flight {
            format: FORMAT.into(),
            version: VERSION.into(),
            law: LAW.into(),
            law_hash: m.law_hash.clone(),
            commit: m.commit.clone(),
            dirty: m.dirty,
            started_utc: readable,
            seed,
            rtf,
            members,
            threads,
            inputs: Vec::new(),
            presented_tick: 0,
            cut_tick: None,
            end: None,
            loss: None,
            refusals: 0,
            other_refusals: 0,
            digest: None,
            digest_source: None,
            note: None,
        };
        Self { dir, path, flight, writer: None, last_write: Instant::now(), seen_inputs: 0, frozen: false, shadow: None }
    }

    pub fn dir(&self) -> &Path {
        &self.dir
    }

    /// The flight as it stands: the recorded fields, brought up to date with the session. Once lost, the log is the one at the loss.
    pub fn current(&self, s: &Session) -> Flight {
        let mut f = self.flight.clone();
        f.rtf = s.rtf;
        if !self.frozen {
            let u = &s.p.u;
            f.inputs = u.inputs.clone();
            f.presented_tick = u.now;
            let (own, other) = refusals(u, s.p.player);
            (f.refusals, f.other_refusals) = (own, other);
        }
        f
    }

    fn write(&mut self, s: &Session) {
        let text = serde_json::to_string(&self.current(s)).unwrap_or_default() + "\n";
        self.queue(text);
    }

    fn queue(&mut self, text: String) {
        let path = self.path.clone();
        let w = self.writer.get_or_insert_with(|| Writer::spawn(path));
        let _ = w.tx.send(text);
        self.last_write = Instant::now();
    }

    /// Called after every presented frame. Writes at the first frame, at every new decision, and every [`EVERY`] seconds; at a
    /// loss, freezes the flight and starts the shadow that digests it.
    pub fn frame(&mut self, s: &Session, view: Option<&View>) {
        if self.frozen {
            self.poll_shadow(s);
            return;
        }
        let u = &s.p.u;
        let player = u.rec(s.p.player);
        if !player.alive {
            let reason = view.and_then(|v| v.loss.clone()).unwrap_or_else(|| format!("lost, with no view: {:?}", player.fault));
            self.flight = self.current(s);
            self.flight.loss = Some(Loss { reason, tick: player.b.event_time });
            self.flight.end = Some("loss".into());
            self.frozen = true;
            let f = self.flight.clone();
            self.shadow = Some(std::thread::spawn(move || replay(&f, None).map_err(|e| format!("{e:?}"))));
            self.write(s);
            return;
        }
        if self.writer.is_none() || u.inputs.len() != self.seen_inputs || self.last_write.elapsed().as_secs_f64() >= EVERY {
            self.seen_inputs = u.inputs.len();
            self.write(s);
        }
    }

    /// The shadow's digest, once it is done.
    fn poll_shadow(&mut self, s: &Session) {
        if self.shadow.as_ref().is_some_and(|h| h.is_finished()) {
            self.land_shadow(s);
        }
    }

    fn land_shadow(&mut self, s: &Session) {
        let Some(h) = self.shadow.take() else { return };
        let out = h.join().map_err(|_| "the shadow replay panicked".to_string()).and_then(|r| r);
        match out {
            Ok(r) => {
                self.flight.cut_tick = Some(r.cut);
                self.flight.digest = Some(r.digest);
                self.flight.digest_source = Some("shadow".into());
                self.flight.refusals = r.refusals;
                self.flight.other_refusals = r.other_refusals;
                if r.loss != self.flight.loss {
                    self.flight.note = Some(format!("the shadow replay disagrees with the live loss: {:?}", r.loss));
                }
            }
            Err(e) => self.flight.note = Some(format!("no digest: the shadow replay failed: {e}")),
        }
        self.write(s);
    }

    /// The end of the flight (exit or restart): the live universe is settled to the canonical cut and digested. A flight already
    /// lost waits for its shadow. Waits for the writer: when this returns, the file is on disk.
    pub fn finish(&mut self, s: &mut Session, why: &str) -> Option<PathBuf> {
        self.writer.as_ref()?;
        if self.frozen {
            let until = Instant::now() + std::time::Duration::from_secs_f64(SHADOW_WAIT);
            while self.shadow.as_ref().is_some_and(|h| !h.is_finished()) && Instant::now() < until {
                std::thread::sleep(std::time::Duration::from_millis(20));
            }
            if self.shadow.as_ref().is_some_and(|h| h.is_finished()) {
                self.land_shadow(s);
            } else if self.shadow.is_some() {
                self.flight.note = Some(format!("no digest: the shadow replay had not finished in {SHADOW_WAIT} s; the log is complete (replay it)"));
                self.write(s);
            }
        } else {
            self.flight = self.current(s);
            let cut = canonical_cut(&s.p.u);
            s.p.u.settle(cut);
            let player = s.p.u.rec(s.p.player);
            if !player.alive {
                // Doomed before the cut: the course held an impact, and the cut is past it.
                let reason = emergent_universe::view::gather(&s.p.u, &s.p.names).and_then(|v| v.loss).unwrap_or_else(|| format!("lost, with no view: {:?}", player.fault));
                self.flight.loss = Some(Loss { reason, tick: player.b.event_time });
            }
            let (own, other) = refusals(&s.p.u, s.p.player);
            (self.flight.refusals, self.flight.other_refusals) = (own, other);
            self.flight.cut_tick = Some(cut);
            self.flight.digest = Some(s.p.u.digest());
            self.flight.digest_source = Some("live".into());
            self.flight.end = Some(why.into());
            self.frozen = true;
            self.write(s);
        }
        self.close()
    }

    /// The engine panicked: the inputs so far are the reproduction. No settle, no digest (the universe cannot be trusted).
    pub fn panicked(&mut self, s: &Session, message: &str) -> Option<PathBuf> {
        self.writer.as_ref()?;
        if !self.frozen {
            self.flight = self.current(s);
            self.flight.end = Some("panic".into());
            self.flight.note = Some(format!("the engine panicked: {message}"));
            self.frozen = true;
        }
        self.write(s);
        self.close()
    }

    fn close(&mut self) -> Option<PathBuf> {
        let w = self.writer.take()?;
        drop(w.tx);
        let _ = w.handle.join();
        Some(self.path.clone())
    }
}

/// The player's refusals, and everyone else's.
pub fn refusals(u: &Universe, player: usize) -> (u64, u64) {
    let (mut own, mut other) = (0, 0);
    for i in 0..u.n_bodies() {
        let r = u.rec(i).refusals;
        if i == player {
            own = r;
        } else {
            other += r;
        }
    }
    (own, other)
}
