//! The smoothness dashboard (docs/plane.md, "Measured on the whole"): smoothness as a service level,
//! not as FPS. A percentile alone can hide a 200 ms freeze once a minute, which is 0.028% of frames,
//! so the dashboard also counts hitches per gameplay hour and keeps the worst one.
use crate::view::TICK_SECONDS;

#[derive(Default, Clone)]
pub struct Dash {
    pub frame_ms: Vec<f64>,
    pub rtf: Vec<f64>,
    pub events: u64,
    /// Game seconds presented and wall seconds spent.
    pub game_seconds: f64,
    pub wall_seconds: f64,
    pub overflow_frames: u64,
    /// Where a frame's time went: the engine's advance, the view's gather, the JSON tree built from it, the
    /// wire (serialisation).
    pub engine_ms: Vec<f64>,
    pub view_ms: Vec<f64>,
    pub json_ms: Vec<f64>,
    pub wire_ms: Vec<f64>,
}

fn pct(sorted: &[f64], q: f64) -> f64 {
    if sorted.is_empty() {
        0.0
    } else {
        sorted[((sorted.len() - 1) as f64 * q).round() as usize]
    }
}

#[derive(Clone, Debug)]
pub struct Summary {
    pub frames: usize,
    pub p50: f64,
    pub p95: f64,
    pub p99: f64,
    pub p999: f64,
    /// Hitches per gameplay hour above 16.7, 33 and 50 ms.
    pub hitches_per_hour: [f64; 3],
    pub hitch_counts: [usize; 3],
    pub worst_ms: f64,
    pub worst_at_frame: usize,
    pub rtf_median: f64,
    pub rtf_low1: f64,
    pub events_per_second: f64,
    pub overflow_frames: u64,
    /// (p50, p99, share of the summed time, max) of the engine, the view's gather, the JSON tree and the wire.
    pub parts: [(f64, f64, f64, f64); 4],
}

impl Dash {
    pub fn record(&mut self, frame_ms: f64, game_ticks: i64, wall_dt: f64, events: u64, overflow: bool) {
        self.frame_ms.push(frame_ms);
        let game = game_ticks as f64 * TICK_SECONDS;
        self.rtf.push(game / wall_dt);
        self.game_seconds += game;
        self.wall_seconds += wall_dt;
        self.events += events;
        self.overflow_frames += overflow as u64;
    }

    pub fn parts(&mut self, engine: f64, view: f64, json: f64, wire: f64) {
        self.engine_ms.push(engine);
        self.view_ms.push(view);
        self.json_ms.push(json);
        self.wire_ms.push(wire);
    }

    pub fn summary(&self) -> Summary {
        let part = |v: &Vec<f64>, total: f64| {
            let mut s = v.clone();
            s.sort_by(f64::total_cmp);
            (pct(&s, 0.5), pct(&s, 0.99), if total > 0.0 { v.iter().sum::<f64>() / total } else { 0.0 }, s.last().copied().unwrap_or(0.0))
        };
        let total: f64 = [&self.engine_ms, &self.view_ms, &self.json_ms, &self.wire_ms].iter().map(|v| v.iter().sum::<f64>()).sum();
        let mut f = self.frame_ms.clone();
        f.sort_by(f64::total_cmp);
        let mut r = self.rtf.clone();
        r.sort_by(f64::total_cmp);
        let hours = self.wall_seconds / 3600.0;
        let counts = [16.7, 33.0, 50.0].map(|th| self.frame_ms.iter().filter(|&&x| x > th).count());
        let (worst_at, worst) = self.frame_ms.iter().cloned().enumerate().fold((0, 0.0), |a, (i, x)| if x > a.1 { (i, x) } else { a });
        Summary {
            frames: f.len(),
            p50: pct(&f, 0.5),
            p95: pct(&f, 0.95),
            p99: pct(&f, 0.99),
            p999: pct(&f, 0.999),
            hitches_per_hour: counts.map(|c| if hours > 0.0 { c as f64 / hours } else { 0.0 }),
            hitch_counts: counts,
            worst_ms: worst,
            worst_at_frame: worst_at,
            rtf_median: pct(&r, 0.5),
            rtf_low1: pct(&r, 0.01),
            events_per_second: if self.wall_seconds > 0.0 { self.events as f64 / self.wall_seconds } else { 0.0 },
            overflow_frames: self.overflow_frames,
            parts: [part(&self.engine_ms, total), part(&self.view_ms, total), part(&self.json_ms, total), part(&self.wire_ms, total)],
        }
    }
}
