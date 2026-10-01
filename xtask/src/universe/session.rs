//! A flight: the plane, the frame loop, the dashboard. Shared by the page and the benchmark.
use emergent_universe::dash::Dash;
use emergent_universe::fleet::Order;
use emergent_universe::scenario::{plane, Plane};
use emergent_universe::view::{gather, View};
use emergent_universe::{Budget, Config};
use serde_json::{json, Value};
use std::time::Instant;

/// The wall time the engine may spend in a frame (the frame is 16.7 ms at 60 Hz: the rest is the view,
/// the serialisation and the browser).
pub const ENGINE_BUDGET_MS: f64 = 5.0;

pub struct Session {
    pub p: Plane,
    pub seed: u64,
    pub rtf: f64,
    pub dash: Dash,
    keys: u8,
    names: Vec<String>,
}

impl Session {
    pub fn new(seed: u64, threads: usize, members: u64, rtf: f64) -> crate::Result<Self> {
        let p = plane(Config::default(), seed, Order::Sparse, threads, members).map_err(|e| format!("the plane: {e:?}"))?;
        let names = p.names.clone();
        Ok(Self { p, seed, rtf, dash: Dash::default(), keys: 0, names })
    }

    pub fn n_bodies(&self) -> usize {
        self.p.u.n_bodies()
    }
    pub fn catalogue_live(&self) -> usize {
        self.p.u.catalogue_live()
    }
    pub fn bytes_per_body(&self) -> usize {
        self.p.u.bytes_per_body()
    }
    pub fn player_alive(&self) -> bool {
        self.p.u.rec(self.p.player).alive
    }
    pub fn lost_bodies(&self) -> Vec<String> {
        (0..self.p.u.n_bodies()).filter(|&i| !self.p.u.rec(i).alive).map(|i| self.names[i].clone()).collect()
    }
    pub fn stats(&self) -> emergent_universe::universe::Stats {
        self.p.u.stats
    }

    /// One presented frame: the player's keys (a decision at the presented tick if they changed), the
    /// engine's budgeted advance, the view, its serialisation. Returns the view as JSON and the frame's wall time.
    pub fn step(&mut self, keys: u8, wall_dt: f64) -> crate::Result<(Value, f64)> {
        let start = Instant::now();
        if keys != self.keys {
            let now = self.p.u.now;
            self.p.u.input(now, keys).map_err(|e| format!("input: {e:?}"))?;
            self.keys = keys;
        }
        let f = self.p.u.frame(wall_dt, self.rtf, Budget::wall(ENGINE_BUDGET_MS));
        let t1 = Instant::now();
        let view = match gather(&self.p.u, &self.names) {
            Some(v) => v,
            None => {
                let r = self.p.u.rec(self.p.player);
                return Err(format!("no view: the player is {} (fault {:?}, doll {}, tick {})", if r.alive { "alive but unreadable" } else { "lost" }, r.fault, r.b.doll, self.p.u.now).into());
            }
        };
        let json = view_json(&view);
        let t2 = Instant::now();
        // The cost of putting it on the wire is part of the frame.
        let wire = serde_json::to_vec(&json)?;
        std::hint::black_box(&wire);
        let ms = start.elapsed().as_secs_f64() * 1e3;
        self.dash.parts((t1 - start).as_secs_f64() * 1e3, (t2 - t1).as_secs_f64() * 1e3, t2.elapsed().as_secs_f64() * 1e3);
        self.dash.record(ms, f.ticks, wall_dt, f.events, f.overflow);
        Ok((json, ms))
    }

    pub fn dash_json(&self) -> Value {
        let d = self.dash.summary();
        json!({"frames": d.frames, "p50": d.p50, "p95": d.p95, "p99": d.p99, "p999": d.p999, "worst": d.worst_ms, "rtf_median": d.rtf_median, "rtf_low1": d.rtf_low1,
               "hitches_per_hour": d.hitches_per_hour, "events_per_second": d.events_per_second, "overflow_frames": d.overflow_frames,
               "bytes_per_body": self.p.u.bytes_per_body()})
    }

    /// The digest at a canonical cut: everything up to the presented tick resolved.
    pub fn digest_at_cut(&mut self) -> String {
        let t = self.p.u.now;
        self.p.u.settle(t);
        self.p.u.digest()
    }

    pub fn log(&self) -> Value {
        json!({"version": "es-plane-v0", "seed": self.seed, "inputs": self.p.u.inputs, "presented_tick": self.p.u.now})
    }

    pub fn describe(&self) -> String {
        let u = &self.p.u;
        let mut out = String::new();
        out += &format!("{} dolls, {} bodies, {} fleet(s) of {} members\n", u.dolls.len(), u.n_bodies(), u.fleets.len(), u.fleets[0].n_members);
        for (i, d) in u.dolls.iter().enumerate() {
            out += &format!("  doll {i} {:<8} mass 2^{:<4} parent {:?} centre {:?}\n", d.name, d.mass_log2, d.parent, d.centre);
        }
        for i in 0..u.n_bodies() {
            let r = u.rec(i);
            out += &format!("  body {i:>2} {:<10} {:?} in doll {} tube {} bytes\n", self.names[i], r.kind, r.b.doll, std::mem::size_of::<emergent_space::Tube>());
        }
        out
    }
}

fn view_json(v: &View) -> Value {
    json!({
        "tick": v.tick, "coordinate": v.coordinate_seconds, "proper": v.proper_seconds, "rate": v.rate,
        "beta": v.beta, "position": v.position_light_seconds, "heading": v.heading, "doll": v.doll,
        "seen": v.seen.iter().map(|s| json!({
            "id": s.id, "name": s.name, "kind": s.kind, "direction": s.direction, "light_seconds": s.light_seconds,
            "color": s.color, "luminosity": s.luminosity, "shift": s.shift, "age": s.age, "lag": s.lag, "angular_radius": s.angular_radius,
        })).collect::<Vec<_>>(),
    })
}
