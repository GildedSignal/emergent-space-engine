//! Plumbing shared by the gates: rows.jsonl, the 60 s chunk driver and watchdog, machine state.
use crate::Result;
use serde_json::{json, Value};
use std::{
    fs::File,
    io::{BufWriter, Write},
    path::Path,
    process::Command,
    sync::{Arc, Mutex},
    time::{Duration, Instant},
};

/// rows.jsonl, shared with the watchdog thread. `sink()` discards (unit tests).
#[derive(Clone)]
pub struct Rows(Arc<Mutex<Option<BufWriter<File>>>>);
impl Rows {
    pub fn create(path: &Path) -> Result<Rows> {
        Ok(Rows(Arc::new(Mutex::new(Some(BufWriter::new(File::create(path)?))))))
    }
    #[cfg(test)]
    pub fn sink() -> Rows {
        Rows(Arc::new(Mutex::new(None)))
    }
    pub fn write(&self, v: &Value) {
        if let Some(w) = self.0.lock().unwrap().as_mut() {
            let _ = writeln!(w, "{v}");
        }
    }
    pub fn flush(&self) {
        if let Some(w) = self.0.lock().unwrap().as_mut() {
            let _ = w.flush();
        }
    }
}

/// Hard limit per chunk: if a chunk runs past it, `on_timeout(label, secs)` is called from a
/// separate thread (it writes the failure down and exits the process).
pub struct Watch {
    slot: Mutex<Option<(Instant, String)>>,
}
impl Watch {
    pub fn spawn(limit: Duration, on_timeout: impl Fn(&str, f64) + Send + 'static) -> Arc<Watch> {
        let w = Arc::new(Watch { slot: Mutex::new(None) });
        let w2 = w.clone();
        std::thread::spawn(move || loop {
            std::thread::sleep(Duration::from_millis(100));
            let over = w2.slot.lock().unwrap().as_ref().filter(|(t, _)| t.elapsed() > limit).map(|(t, l)| (t.elapsed().as_secs_f64(), l.clone()));
            if let Some((secs, label)) = over {
                on_timeout(&label, secs);
            }
        });
        w
    }
    pub fn arm(&self, label: &str) {
        *self.slot.lock().unwrap() = Some((Instant::now(), label.to_string()));
    }
    /// What the current chunk is working on (for the timeout message).
    pub fn detail(&self, what: &str) {
        if let Some((_, l)) = self.slot.lock().unwrap().as_mut() {
            if let Some(i) = l.find(" @ ") {
                l.truncate(i);
            }
            l.push_str(" @ ");
            l.push_str(what);
        }
    }
    pub fn disarm(&self) {
        *self.slot.lock().unwrap() = None;
    }
}

#[derive(Clone)]
pub struct Ctx {
    pub rows: Rows,
    /// Target wall time of one chunk, seconds. Every chunk must stay under `hard_secs`.
    pub chunk_secs: f64,
    pub hard_secs: f64,
    pub watch: Option<Arc<Watch>>,
    /// Print progress lines to stdout.
    pub console: bool,
    /// G2.2 oracle-versus-judge gaps the integrator has adjudicated: "ID" (every check) or
    /// "ID:check". Empty by default: an unadjudicated gap fails the gate.
    pub adjudicated: Vec<String>,
}
impl Ctx {
    #[cfg(test)]
    pub fn quiet() -> Ctx {
        Ctx { rows: Rows::sink(), chunk_secs: 30.0, hard_secs: 60.0, watch: None, console: false, adjudicated: Vec::new() }
    }
    pub fn say(&self, line: &str) {
        if self.console {
            println!("{line}");
        }
    }
    pub fn note(&self, what: &str) {
        if let Some(w) = &self.watch {
            w.detail(what);
        }
    }
}

#[derive(Clone, Debug)]
pub struct Chunk {
    pub items: usize,
    pub secs: f64,
}
impl Chunk {
    pub fn to_json(&self) -> Value {
        json!({"items": self.items, "secs": (self.secs * 1e3).round() / 1e3})
    }
}
pub fn max_secs(chunks: &[Chunk]) -> f64 {
    chunks.iter().map(|c| c.secs).fold(0.0, f64::max)
}

/// Runs `work` over `items` in chunks sized to take about `ctx.chunk_secs` each: it starts small
/// and scales the next chunk by (target / measured), at most 4x up and down to 1/4. The chunking
/// never changes a result. Each chunk is armed on the watchdog.
pub fn chunked<T>(ctx: &Ctx, label: &str, items: &[T], mut work: impl FnMut(&[T])) -> Vec<Chunk> {
    let mut chunks = Vec::new();
    let (mut at, mut size) = (0usize, 16usize);
    while at < items.len() {
        let end = (at + size).min(items.len());
        if let Some(w) = &ctx.watch {
            w.arm(&format!("{label} chunk {}", chunks.len() + 1));
        }
        let t = Instant::now();
        work(&items[at..end]);
        let secs = t.elapsed().as_secs_f64();
        chunks.push(Chunk { items: end - at, secs });
        ctx.rows.write(&json!({"kind": "chunk", "what": label, "n": chunks.len(), "items": end - at, "secs": (secs * 1e3).round() / 1e3}));
        ctx.rows.flush();
        let scale = (ctx.chunk_secs / secs.max(1e-6)).clamp(0.25, 4.0);
        size = ((end - at) as f64 * scale).ceil().max(1.0) as usize;
        at = end;
    }
    if let Some(w) = &ctx.watch {
        w.disarm();
    }
    chunks
}

fn shell(prog: &str, args: &[&str]) -> String {
    match Command::new(prog).args(args).output() {
        Ok(o) if o.status.success() => String::from_utf8_lossy(&o.stdout).trim().to_string(),
        Ok(o) => format!("unavailable: exit {} {}", o.status, String::from_utf8_lossy(&o.stderr).trim()),
        Err(e) => format!("unavailable: {e}"),
    }
}
/// The machine state to record with a run (AGENTS.md: heat and load are part of reality).
pub fn machine_state(when: &str) -> Value {
    let batt = shell("pmset", &["-g", "batt"]);
    let power = batt.lines().next().unwrap_or("").to_string();
    json!({
        "kind": "machine", "when": when,
        "time_utc": shell("date", &["-u", "+%Y-%m-%dT%H:%M:%SZ"]),
        "unix": std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).map(|d| d.as_secs()).unwrap_or(0),
        "therm": shell("pmset", &["-g", "therm"]),
        "power_source": power, "batt": batt,
        "swap": shell("sysctl", &["-n", "vm.swapusage"]),
        "loadavg": shell("sysctl", &["-n", "vm.loadavg"]),
        "hardware": shell("sysctl", &["-n", "machdep.cpu.brand_string"]),
    })
}

/// Median (mean of the two middle values when even) and nearest-rank percentile of sorted data.
pub fn median(sorted: &[u64]) -> f64 {
    match sorted.len() {
        0 => f64::NAN,
        n if n % 2 == 1 => sorted[n / 2] as f64,
        n => (sorted[n / 2 - 1] + sorted[n / 2]) as f64 / 2.0,
    }
}
pub fn percentile(sorted: &[u64], p: f64) -> f64 {
    if sorted.is_empty() {
        return f64::NAN;
    }
    let rank = ((p / 100.0) * sorted.len() as f64).ceil().max(1.0) as usize;
    sorted[rank - 1] as f64
}
