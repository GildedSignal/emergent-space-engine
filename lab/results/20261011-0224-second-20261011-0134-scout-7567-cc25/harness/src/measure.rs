//! Measurement shared by the judges (`ladder7`, `behave`): process resources, percentiles, the
//! unit-timed stepper driver, the 60 s watchdog and the machine state (AGENTS.md: heat and load
//! are part of reality, so every run records them).
use emergent_lattice::Stepper;
use serde_json::{json, Value};
use std::{
    process::Command,
    sync::{Arc, Mutex},
    time::{Duration, Instant},
};

pub(crate) fn peak_rss() -> u64 {
    let mut usage = std::mem::MaybeUninit::<libc::rusage>::uninit();
    // SAFETY: getrusage initializes the out pointer on success.
    unsafe {
        if libc::getrusage(libc::RUSAGE_SELF, usage.as_mut_ptr()) == 0 {
            let n = usage.assume_init().ru_maxrss as u64;
            if cfg!(target_os = "macos") {
                n
            } else {
                n * 1024
            }
        } else {
            0
        }
    }
}

/// Process CPU time (user + system) in seconds; cores used = CPU time / wall time.
pub(crate) fn cpu_seconds() -> f64 {
    let mut usage = std::mem::MaybeUninit::<libc::rusage>::uninit();
    // SAFETY: getrusage initializes the out pointer on success.
    unsafe {
        if libc::getrusage(libc::RUSAGE_SELF, usage.as_mut_ptr()) == 0 {
            let u = usage.assume_init();
            let tv = |t: libc::timeval| t.tv_sec as f64 + t.tv_usec as f64 / 1e6;
            tv(u.ru_utime) + tv(u.ru_stime)
        } else {
            0.0
        }
    }
}

/// Nearest-index percentile of sorted data, `q` in [0, 1].
pub(crate) fn percentile(sorted: &[f64], q: f64) -> f64 {
    if sorted.is_empty() {
        return 0.0;
    }
    sorted[((sorted.len() - 1) as f64 * q).round() as usize]
}

pub(crate) struct Drive {
    pub(crate) complete: bool,
    pub(crate) limiter: Option<String>,
    pub(crate) advance_ms: f64,
    pub(crate) cpu_s: f64,
    pub(crate) units_ms: Vec<f64>,
}

/// Advances `s` to `horizon` in units of `unit_ops` charged operations, timing every unit, and
/// stops at the wall or peak-RSS cap.
pub(crate) fn drive(s: &mut dyn Stepper, horizon: i64, unit_ops: u64, wall_s: f64, rss_cap: u64) -> Drive {
    let (start, cpu0) = (Instant::now(), cpu_seconds());
    let mut units_ms = Vec::new();
    let mut limiter = None;
    while s.tick() < horizon {
        let t = Instant::now();
        s.advance(horizon, unit_ops);
        units_ms.push(t.elapsed().as_secs_f64() * 1e3);
        if units_ms.len() % 256 == 0 {
            if start.elapsed().as_secs_f64() > wall_s {
                limiter = Some(format!("wall cap {wall_s} s at tick {} of {horizon}", s.tick()));
                break;
            }
            if peak_rss() > rss_cap {
                limiter = Some("peak RSS cap".into());
                break;
            }
        }
    }
    // The cap binds whether or not a check boundary fell inside it ("complete within caps").
    if limiter.is_none() && start.elapsed().as_secs_f64() > wall_s {
        limiter = Some(format!("wall cap {wall_s} s (reached tick {} of {horizon} in {:.1} s)", s.tick(), start.elapsed().as_secs_f64()));
    }
    Drive { complete: limiter.is_none(), limiter, advance_ms: start.elapsed().as_secs_f64() * 1e3, cpu_s: cpu_seconds() - cpu0, units_ms }
}

/// Hard limit per phase: if a phase runs past it, `on_timeout(label, secs)` is called from a
/// separate thread (it writes the failure down and exits the process).
pub(crate) struct Watch {
    slot: Mutex<Option<(Instant, String)>>,
}
impl Watch {
    pub(crate) fn spawn(limit: Duration, on_timeout: impl Fn(&str, f64) + Send + 'static) -> Arc<Watch> {
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
    pub(crate) fn arm(&self, label: &str) {
        *self.slot.lock().unwrap() = Some((Instant::now(), label.to_string()));
    }
    pub(crate) fn disarm(&self) {
        *self.slot.lock().unwrap() = None;
    }
}

fn shell(prog: &str, args: &[&str]) -> String {
    match Command::new(prog).args(args).output() {
        Ok(o) if o.status.success() => String::from_utf8_lossy(&o.stdout).trim().to_string(),
        Ok(o) => format!("unavailable: exit {} {}", o.status, String::from_utf8_lossy(&o.stderr).trim()),
        Err(e) => format!("unavailable: {e}"),
    }
}
/// The machine state to record with a run: thermal, power, swap and load.
pub(crate) fn machine_state(when: &str) -> Value {
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

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::{AtomicBool, Ordering};

    #[test]
    fn percentile_takes_the_nearest_index() {
        let v = [1.0, 2.0, 3.0, 4.0, 5.0];
        assert_eq!([percentile(&v, 0.0), percentile(&v, 0.5), percentile(&v, 0.99), percentile(&v, 1.0)], [1.0, 3.0, 5.0, 5.0]);
        assert_eq!(percentile(&[], 0.5), 0.0);
    }

    #[test]
    fn the_watch_fires_on_a_phase_past_its_limit_and_not_on_one_that_ends() {
        let fired = Arc::new(AtomicBool::new(false));
        let f = fired.clone();
        let w = Watch::spawn(Duration::from_millis(150), move |label, _| {
            assert_eq!(label, "slow");
            f.store(true, Ordering::SeqCst);
        });
        w.arm("quick");
        w.disarm();
        std::thread::sleep(Duration::from_millis(400));
        assert!(!fired.load(Ordering::SeqCst));
        w.arm("slow");
        std::thread::sleep(Duration::from_millis(600));
        assert!(fired.load(Ordering::SeqCst));
        w.disarm();
    }

    #[test]
    fn the_machine_state_records_the_load() {
        let m = machine_state("test");
        assert_eq!(m["when"], "test");
        assert!(m["loadavg"].is_string() && m["swap"].is_string());
    }
}
