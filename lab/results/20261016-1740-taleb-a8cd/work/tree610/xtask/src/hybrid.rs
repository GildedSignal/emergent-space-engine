//! Hybrid mode (docs/archive/engine.md, rule 9): one region runs in event mode when it is
//! sparse and in Metal chronon mode when it is dense. The first choice comes from kinetic
//! theory (κ = predicted collisions per body per chronon); after that the measured wall time
//! per chronon decides, and the other mode is re-probed now and then. The modes are
//! bit-identical, so switching (a canonical snapshot handed from one to the other) changes
//! speed, never results; the ladder checks it like any other mode.
use emergent_lattice::{Log, Metrics, Stepper, Tick, World};
use emergent_lattice_event::EventCore;
use emergent_lattice_metal::MetalChronon;
use std::time::Instant;

/// A decision window ends after this many chronons or this much wall time, whichever comes
/// first, so probing the wrong mode on a huge region costs milliseconds, not seconds.
const WINDOW: Tick = 128;
const WINDOW_SECONDS: f64 = 0.05;
/// First re-probe interval in windows; doubles each time a probe loses (capped).
const PROBE_EVERY: u32 = 16;
const PROBE_CAP: u32 = 1024;
/// Kinetic prior: start on the GPU at or above this many bodies and collisions per body per chronon.
const DENSE_BODIES: usize = 4096;
const DENSE_KAPPA: f64 = 1e-3;
/// The GPU is never a candidate below this size or far below the dense κ: its round trip
/// and set-up cannot pay back (measured: slower than the CPU below about 2k ships).
const MIN_METAL_BODIES: usize = 2048;
const MIN_METAL_KAPPA: f64 = DENSE_KAPPA / 16.0;

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
enum Mode {
    Event,
    Metal,
}

pub struct Hybrid {
    cur: Box<dyn Stepper + Send>,
    mode: Mode,
    keep: bool,
    /// Log and metrics of the steppers already handed over.
    done_log: Log,
    done_metrics: Metrics,
    log: Log,
    metrics: Metrics,
    /// Measured seconds per chronon, per mode (exponential average).
    cost: [Option<f64>; 2],
    window_start: (Tick, Instant),
    windows: u32,
    probing: Option<Mode>,
    /// The first window after a switch is warm-up (GPU pipelines, cell set-up): not measured.
    warm: bool,
    metal_ok: bool,
    interval: u32,
    next_probe: u32,
    pub switches: u32,
}

/// Kinetic estimate of collisions per body per chronon: n·σ·v̄_rel with σ = 2·(2r̄), where n
/// is the density *where the bodies are*: the mean number of other bodies sharing a cell of
/// side 8r̄ (Σ c(c − 1) / N, unbiased for a Poisson scatter) over the cell's area. The box's
/// mean density was meaningless for clustered worlds (a galaxy's fleets: H0180, as for the
/// event core's cells in H0177); for a uniform gas both estimates agree.
pub fn kappa(w: &World) -> f64 {
    let n = w.bodies.len();
    if n < 2 {
        return 0.0;
    }
    let r = w.bodies.iter().map(|b| b.radius as f64).sum::<f64>() / n as f64;
    let v2 = w.bodies.iter().map(|b| (b.k[0] as f64).powi(2) + (b.k[1] as f64).powi(2)).sum::<f64>() / n as f64;
    let side = (8.0 * r).max(1.0) as i64;
    let mut cells: std::collections::HashMap<(i64, i64), u64> = std::collections::HashMap::with_capacity(n);
    for b in &w.bodies {
        *cells.entry((b.x[0].div_euclid(side), b.x[1].div_euclid(side))).or_default() += 1;
    }
    let mates = cells.values().map(|&c| (c * (c - 1)) as f64).sum::<f64>() / n as f64;
    mates / (side as f64).powi(2) * 4.0 * r * (2.0 * v2).sqrt()
}

fn make(mode: Mode, w: World, keep: bool) -> Result<Box<dyn Stepper + Send>, String> {
    match mode {
        Mode::Event => EventCore::new(w, keep).map(|s| Box::new(s) as Box<dyn Stepper + Send>).map_err(|e| e.to_string()),
        Mode::Metal => MetalChronon::new(w, keep).map(|s| Box::new(s) as Box<dyn Stepper + Send>).map_err(|e| e.to_string()),
    }
}

impl Hybrid {
    pub fn new(w: World, keep: bool) -> Result<Self, String> {
        let k = kappa(&w);
        let dense = w.bodies.len() >= DENSE_BODIES && k >= DENSE_KAPPA;
        let metal_ok = w.bodies.len() >= MIN_METAL_BODIES && k >= MIN_METAL_KAPPA;
        let mode = if dense { Mode::Metal } else { Mode::Event };
        let tick = w.tick;
        let cur = make(mode, w, keep)?;
        Ok(Hybrid {
            cur,
            mode,
            keep,
            done_log: Log::new(keep),
            done_metrics: Metrics::default(),
            log: Log::new(keep),
            metrics: Metrics::default(),
            cost: [None, None],
            window_start: (tick, Instant::now()),
            windows: 0,
            probing: None,
            warm: true,
            metal_ok,
            interval: PROBE_EVERY,
            next_probe: 2,
            switches: 0,
        })
    }

    fn switch(&mut self, to: Mode) {
        let w = self.cur.world();
        // Metal may be unavailable; staying put is always correct.
        let Ok(next) = make(to, w, self.keep) else { return };
        self.done_log.merge(self.cur.log());
        self.done_metrics.merge(self.cur.metrics());
        self.cur = next;
        self.mode = to;
        self.switches += 1;
        self.warm = true;
    }

    /// At a window boundary: record the cost of the window and choose the next mode.
    fn decide(&mut self) {
        let (t0, start) = self.window_start;
        self.windows += 1;
        if std::mem::take(&mut self.warm) {
            // Warm-up window: measure the next one instead.
            self.window_start = (self.cur.tick(), Instant::now());
            return;
        }
        let chronons = (self.cur.tick() - t0).max(1) as f64;
        let per = start.elapsed().as_secs_f64() / chronons;
        let slot = &mut self.cost[self.mode as usize];
        *slot = Some(slot.map_or(per, |c| 0.7 * c + 0.3 * per));
        let other = if self.mode == Mode::Event { Mode::Metal } else { Mode::Event };
        let next = if let Some(probed) = self.probing.take() {
            // A probe just finished: go with the cheaper measured mode; a losing probe backs off.
            let (e, m) = (self.cost[0].unwrap_or(f64::MAX), self.cost[1].unwrap_or(f64::MAX));
            let best = if m < e { Mode::Metal } else { Mode::Event };
            if best != probed {
                self.interval = (self.interval * 2).min(PROBE_CAP);
            }
            self.next_probe = self.windows + self.interval;
            best
        } else if self.metal_ok && self.windows >= self.next_probe {
            self.probing = Some(other);
            other
        } else {
            self.mode
        };
        if next != self.mode {
            self.switch(next);
        }
        self.window_start = (self.cur.tick(), Instant::now());
    }

    fn refresh(&mut self) {
        let mut log = self.done_log.clone();
        log.merge(self.cur.log());
        self.log = log;
        let mut m = self.done_metrics.clone();
        m.merge(self.cur.metrics());
        self.metrics = m;
    }
}

impl Stepper for Hybrid {
    fn tick(&self) -> Tick {
        self.cur.tick()
    }

    /// One call stays inside one decision window; the overshoot bound is the current mode's.
    fn advance(&mut self, target: Tick, budget: u64) -> Tick {
        let window_end = self.window_start.0 + WINDOW;
        self.cur.advance(target.min(window_end), budget);
        if self.cur.tick() >= window_end || (self.cur.tick() > self.window_start.0 && self.window_start.1.elapsed().as_secs_f64() > WINDOW_SECONDS) {
            self.decide();
        }
        self.refresh();
        self.cur.tick()
    }

    fn world(&self) -> World {
        self.cur.world()
    }

    fn log(&self) -> &Log {
        &self.log
    }

    fn metrics(&self) -> &Metrics {
        &self.metrics
    }
}
