//! Replay a recorded flight, and compare it with what was recorded.
//!
//! universe --replay <file> [--seconds S]      one flight, in full
//! universe --replay-all [--flights DIR]       every saved flight within 60 s in all: the check run before every merge
//!
//! A replay rebuilds the session from the file (seed, members, threads), schedules the inputs at their canonical ticks, runs
//! to the recorded cut and reads the digest, the loss and the refusals. Exact replay is the law's property: the same digest
//! whenever the law is the same, on any machine, thread count or schedule. So a digest that differs under the same law
//! hash is a bug; under a changed law it is a change to review. A new loss or a new refusal is a regression either way.
use super::flight::{canonical_cut, default_dir, meta, refusals, Flight, Loss, LAW};
use super::session::Session;
use emergent_universe::num::Tick;
use std::path::{Path, PathBuf};
use std::time::{Duration, Instant};

/// Ticks between two looks at the clock while settling (82 s of game time): a deadline is kept to a fraction of a second.
const CHUNK: Tick = 1 << 24;
/// The whole of `--replay-all`.
pub const ALL_SECONDS: f64 = 55.0;

#[derive(Debug)]
pub enum Stop {
    /// The wall deadline came first: the replay got to `reached` of `cut`.
    Deadline { reached: Tick, cut: Tick },
    Failed(String),
}

#[derive(Debug, Clone)]
pub struct Replayed {
    pub cut: Tick,
    pub digest: String,
    pub loss: Option<Loss>,
    pub refusals: u64,
    pub other_refusals: u64,
    pub seconds: f64,
}

fn settle_to(s: &mut Session, target: Tick, deadline: Option<Instant>, cut: Tick) -> Result<(), Stop> {
    while s.p.u.now < target {
        if deadline.is_some_and(|d| Instant::now() >= d) {
            return Err(Stop::Deadline { reached: s.p.u.now, cut });
        }
        let next = (s.p.u.now + CHUNK).min(target);
        s.p.u.settle(next);
    }
    Ok(())
}

fn panic_text(p: &(dyn std::any::Any + Send)) -> String {
    p.downcast_ref::<&str>().map(|s| s.to_string()).or_else(|| p.downcast_ref::<String>().cloned()).unwrap_or_else(|| "(no message)".into())
}

/// Play the flight back. The cut is the recorded one; a flight with none (it was cut off, or this is a shadow replay that
/// digests a loss) is settled to its presented tick and then to the canonical cut of what it finds there, which is returned.
pub fn replay(f: &Flight, deadline: Option<Instant>) -> Result<Replayed, Stop> {
    let started = Instant::now();
    let run = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| -> Result<Replayed, Stop> {
        let mut s = Session::new(f.seed, f.threads.max(1), f.members, f.rtf.clamp(0.01, 1e7)).map_err(|e| Stop::Failed(format!("the plane: {e}")))?;
        for &(t, w) in &f.inputs {
            s.p.u.schedule(t, w).map_err(|e| Stop::Failed(format!("the input {w:#04x} at tick {t} was refused: {e:?}")))?;
        }
        let cut = match f.cut_tick {
            Some(c) => {
                settle_to(&mut s, c, deadline, c)?;
                c
            }
            None => {
                settle_to(&mut s, f.presented_tick, deadline, f.presented_tick)?;
                let c = canonical_cut(&s.p.u);
                settle_to(&mut s, c, deadline, c)?;
                c
            }
        };
        s.p.u.settle(cut);
        let player = s.p.u.rec(s.p.player);
        let loss = (!player.alive).then(|| Loss {
            reason: emergent_universe::view::gather(&s.p.u, &s.p.names).and_then(|v| v.loss).unwrap_or_else(|| format!("lost, with no view: {:?}", player.fault)),
            tick: player.b.event_time,
        });
        let (own, other) = refusals(&s.p.u, s.p.player);
        Ok(Replayed { cut, digest: s.p.u.digest(), loss, refusals: own, other_refusals: other, seconds: started.elapsed().as_secs_f64() })
    }));
    match run {
        Ok(r) => r,
        Err(p) => Err(Stop::Failed(format!("the engine panicked: {}", panic_text(&*p)))),
    }
}

#[derive(Debug, Default)]
pub struct Verdict {
    /// Every difference, named.
    pub notes: Vec<String>,
    /// A new loss, a new refusal, or a replay that is not exact under the same law.
    pub regression: bool,
    /// The file holds no digest to compare (the flight was cut off).
    pub unchecked: bool,
}

impl Verdict {
    pub fn same(&self) -> bool {
        self.notes.is_empty() && !self.unchecked
    }
}

fn short(s: &str) -> &str {
    &s[..s.len().min(12)]
}

fn loss_text(l: &Option<Loss>) -> String {
    l.as_ref().map_or("none".into(), |l| format!("{} (tick {})", l.reason, l.tick))
}

pub fn compare(f: &Flight, r: &Replayed) -> Verdict {
    let now = meta();
    let law_same = f.law == LAW && f.law_hash == now.law_hash;
    let mut v = Verdict::default();
    match (&f.loss, &r.loss) {
        (None, Some(l)) => {
            v.notes.push(format!("a loss appeared: {}", loss_text(&Some(l.clone()))));
            v.regression = true;
        }
        (Some(_), None) => v.notes.push(format!("the loss vanished: it was {}", loss_text(&f.loss))),
        (Some(a), Some(b)) if a != b => {
            v.notes.push(format!("the loss changed: {} -> {}", loss_text(&f.loss), loss_text(&r.loss)));
            // The engine giving up is a bug whatever the physics did.
            v.regression |= b.reason.starts_with("the engine lost it") && !a.reason.starts_with("the engine lost it");
        }
        _ => {}
    }
    for (what, was, is) in [("refusals", f.refusals, r.refusals), ("other bodies' refusals", f.other_refusals, r.other_refusals)] {
        if is > was {
            v.notes.push(format!("{what}: {was} -> {is}"));
            v.regression = true;
        } else if is < was {
            v.notes.push(format!("{what}: {was} -> {is} (fewer)"));
        }
    }
    match &f.digest {
        Some(d) if *d != r.digest => {
            if law_same {
                v.notes.push(format!("the digest differs under the SAME law ({}): the replay is not exact, or the file was altered (recorded {} by {}, now {})", f.law_hash, short(d), short(&f.commit), short(&r.digest)));
                v.regression = true;
            } else {
                v.notes.push(format!("the digest differs, the law changed since {}{} (law {} #{} -> {} #{}): {} -> {}", short(&f.commit), if f.dirty { " (dirty)" } else { "" }, f.law, f.law_hash, LAW, now.law_hash, short(d), short(&r.digest)));
            }
        }
        Some(_) => {}
        None => v.unchecked = true,
    }
    if let Some(c) = f.cut_tick {
        if c != r.cut {
            v.notes.push(format!("the cut moved: {c} -> {}", r.cut));
        }
    }
    v
}

fn load(path: &Path) -> Result<Flight, String> {
    let text = std::fs::read_to_string(path).map_err(|e| format!("cannot read: {e}"))?;
    serde_json::from_str(&text).map_err(|e| format!("not a flight: {e}"))
}

fn name_of(path: &Path) -> String {
    path.file_name().map_or_else(|| path.display().to_string(), |n| n.to_string_lossy().into_owned())
}

/// `--replay`: one flight in full. Exit 1 on a regression, 2 when the deadline came first.
pub fn replay_file(path: &Path, seconds: f64) -> crate::Result<u8> {
    let f = load(path).map_err(|e| format!("{}: {e}", path.display()))?;
    println!("flight {}", name_of(path));
    println!("  recorded {} at {}{}, law {} #{}, seed {}, rtf {}, {} members, {} thread(s)", f.started_utc, short(&f.commit), if f.dirty { " (dirty)" } else { "" }, f.law, f.law_hash, f.seed, f.rtf, f.members, f.threads);
    println!("  now      {}{}, law {LAW} #{}", short(&meta().commit), if meta().dirty { " (dirty)" } else { "" }, meta().law_hash);
    println!("  {} inputs, presented tick {}, cut {}, end {}", f.inputs.len(), f.presented_tick, f.cut_tick.map_or("none".into(), |c| c.to_string()), f.end.as_deref().unwrap_or("none (cut off)"));
    let r = match replay(&f, Some(Instant::now() + Duration::from_secs_f64(seconds))) {
        Ok(r) => r,
        Err(Stop::Deadline { reached, cut }) => {
            println!("stopped at the {seconds:.0} s deadline: reached tick {reached} of {cut} (not a result)");
            return Ok(2);
        }
        Err(Stop::Failed(e)) => {
            println!("REGRESSION: the replay failed: {e}");
            return Ok(1);
        }
    };
    let v = compare(&f, &r);
    println!("digest     {}", r.digest);
    println!("cut        tick {}", r.cut);
    println!("loss       {}", loss_text(&r.loss));
    println!("refusals   {} (other bodies {})", r.refusals, r.other_refusals);
    match (&f.digest, v.same()) {
        (None, _) => println!("recorded   no digest (the flight was cut off): nothing to match"),
        (Some(d), _) => println!("recorded   {d} ({})", f.digest_source.as_deref().unwrap_or("?")),
    }
    if let Some(n) = &f.note {
        println!("note       {n}");
    }
    if v.same() {
        println!("match: SAME as recorded ({:.1} s)", r.seconds);
    } else if v.notes.is_empty() {
        println!("match: unchecked ({:.1} s)", r.seconds);
    } else {
        println!("match: DIFFERENT ({:.1} s)", r.seconds);
        for n in &v.notes {
            println!("  - {n}");
        }
    }
    Ok(v.regression as u8)
}

/// `--replay-all`: every flight in `dir`, longest first, within `budget` seconds in all. One line a flight. A new loss, a new
/// refusal or a replay that is not exact under the same law exits 1; flights the time did not reach are counted, not failed.
pub fn replay_all(dir: &Path, budget: f64) -> crate::Result<u8> {
    let started = Instant::now();
    let mut flights: Vec<(PathBuf, Result<Flight, String>)> = match std::fs::read_dir(dir) {
        Ok(rd) => rd.filter_map(|e| e.ok().map(|e| e.path())).filter(|p| p.extension().is_some_and(|e| e == "json")).map(|p| (p.clone(), load(&p))).collect(),
        Err(e) => return Err(format!("cannot read {}: {e}", dir.display()).into()),
    };
    let size = |f: &Result<Flight, String>| f.as_ref().map_or(Tick::MAX, |f| f.cut_tick.unwrap_or(f.presented_tick).max(f.presented_tick));
    flights.sort_by(|a, b| size(&b.1).cmp(&size(&a.1)).then(a.0.cmp(&b.0)));
    println!("replay-all: {} flight(s) in {}, longest first, {budget:.0} s in all; now {}{}, law {LAW} #{}", flights.len(), dir.display(), short(&meta().commit), if meta().dirty { " (dirty)" } else { "" }, meta().law_hash);
    let (mut same, mut changed, mut unchecked, mut skipped, mut bad) = (0, 0, 0, 0, 0);
    for (path, f) in &flights {
        let name = name_of(path);
        let f = match f {
            Ok(f) => f,
            Err(e) => {
                println!("REGRESSION {name}  {e}");
                bad += 1;
                continue;
            }
        };
        let left = budget - started.elapsed().as_secs_f64();
        // One flight may take at most half of the whole: the longest first must not starve the rest.
        let limit = left.min(budget / 2.0);
        if left < 0.5 {
            skipped += 1;
            continue;
        }
        match replay(f, Some(Instant::now() + Duration::from_secs_f64(limit))) {
            Ok(r) => {
                let v = compare(f, &r);
                if v.regression {
                    bad += 1;
                    println!("REGRESSION {name}  {}", v.notes.join("; "));
                } else if !v.notes.is_empty() {
                    changed += 1;
                    println!("changed    {name}  {}", v.notes.join("; "));
                } else if v.unchecked {
                    unchecked += 1;
                    println!("unchecked  {name}  no recorded digest (cut off); loss {}; refusals {}; digest {}", loss_text(&r.loss), r.refusals, short(&r.digest));
                } else {
                    same += 1;
                    println!("same       {name}  digest {}  cut {}  loss {}  {:.1} s", short(&r.digest), r.cut, r.loss.as_ref().map_or("none", |_| "yes (as recorded)"), r.seconds);
                }
            }
            Err(Stop::Deadline { reached, cut }) => {
                skipped += 1;
                println!("skipped    {name}  not replayed within {limit:.0} s (reached tick {reached} of {cut})");
            }
            Err(Stop::Failed(e)) => {
                bad += 1;
                println!("REGRESSION {name}  the replay failed: {e}");
            }
        }
    }
    println!("replay-all: {same} same, {changed} changed, {unchecked} unchecked, {skipped} skipped (time), {bad} regression(s), {:.1} s", started.elapsed().as_secs_f64());
    Ok((bad > 0) as u8)
}

/// Where `--replay-all` looks unless told: the committed flights.
pub fn default_flights() -> PathBuf {
    default_dir()
}
