//! The flyable frame, second author: the row-set deletion built and measured on the shipped page path.
//!
//! Stage 1 (this file, pre-patch): `base` (the shipped frame the page pays: engine + `gather_cached` +
//! `view_json`-shaped wire, as the first author's flyframe) and `digest` (a rolling checksum of
//! `gather_cached`'s whole View per frame, to prove the view.rs refactor that follows is byte-identical).
//!
//! cargo run --release -p emergent-universe --example flyframe2 -- base <N> [frames] [rtf]
//! cargo run --release -p emergent-universe --example flyframe2 -- digest <N> [frames] [rtf]
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane_extra;
use emergent_universe::view::{gather_cached, ViewCache};
use emergent_universe::view::Seen;
use emergent_universe::{Budget, Config};
use serde_json::json;
use std::time::Instant;

fn pct(sorted: &[f64], p: f64) -> f64 {
    if sorted.is_empty() {
        return 0.0;
    }
    sorted[(((sorted.len() - 1) as f64) * p).round() as usize]
}

const W: f64 = 1920.0;
const H: f64 = 1080.0;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mode = args.get(1).cloned().unwrap_or_else(|| "base".into());
    let n: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(0);
    let frames: usize = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(240);
    let rtf: f64 = args.get(4).and_then(|s| s.parse().ok()).unwrap_or(100.0);
    let t0 = Instant::now();
    let mut p = plane_extra(Config::default(), 1, Order::Sparse, 1, 48, n).unwrap();
    let build = t0.elapsed().as_secs_f64();
    let bodies = p.u.n_bodies();
    let mut cache = ViewCache::default();

    match mode.as_str() {
        "digest" => {
            // A rolling checksum of the whole View: every Seen field, every frame, in order.
            let mut h = blake3::Hasher::new();
            for f in 0..frames {
                // Deterministic budget (the page's wall budget advances as much as fits in 5 ms, which is
                // machine timing): unlimited advances exactly wall_dt·rtf of game time every frame.
                let _ = p.u.frame_to(1.0 / 60.0, rtf, Budget::unlimited(), i64::MAX);
                let v = gather_cached(&p.u, &p.names, &mut cache).expect("view");
                h.update(&format!("{:?}|{}|{:?}|{:?}|", v.tick, v.proper_seconds, v.beta, v.heading).as_bytes());
                for s in &v.seen {
                    h.update(
                        &format!(
                            "{}|{}|{:?}|{:?}|{:?}|{}|{:?}|{:?}|{:?}|{}|{:?}|{}|",
                            s.id, s.name, s.kind, s.direction, s.offset, s.light_seconds, s.closing, s.color, s.shift, s.luminosity, s.age, s.angular_radius
                        )
                        .as_bytes(),
                    );
                }
                if f == frames / 2 {
                    println!("digest half {} bodies={} frames={}", h.finalize().to_hex(), bodies, frames);
                }
            }
            println!("digest final {} bodies={} frames={} build={:.1}s rtf={}", h.finalize().to_hex(), bodies, frames, build, rtf);
        }
        "base" => {
            let (cx, cy) = (W / 2.0, H / 2.0);
            let r_sky = 0.45 * W.min(H);
            let (lo, hi) = (-5.0f64, 3.6f64);
            for _ in 0..60 {
                let _ = p.u.frame_to(1.0 / 60.0, rtf, Budget::wall(5.0), i64::MAX);
                let _ = gather_cached(&p.u, &p.names, &mut cache);
            }
            let mut engine_ms: Vec<f64> = Vec::with_capacity(frames);
            let mut gather_ms: Vec<f64> = Vec::with_capacity(frames);
            let mut wire_ms: Vec<f64> = Vec::with_capacity(frames);
            let mut rows_seen = 0usize;
            let mut wire_bytes = 0usize;
            let mut static_sky_tot = 0usize;
            let mut census_frames = 0usize;
            let mut prev: Option<Vec<(i64, i64)>> = None;
            for f in 0..frames {
                let t1 = Instant::now();
                let _ = p.u.frame_to(1.0 / 60.0, rtf, Budget::wall(5.0), i64::MAX);
                let t2 = Instant::now();
                let view = gather_cached(&p.u, &p.names, &mut cache).expect("the player has a view");
                let t3 = Instant::now();
                let rows: Vec<_> = view
                    .seen
                    .iter()
                    .map(|s| {
                        json!({"name": s.name, "kind": s.kind, "direction": s.direction, "light_seconds": s.light_seconds,
                               "offset": s.offset, "closing": s.closing, "color": s.color, "shift": s.shift})
                    })
                    .collect();
                let wire = serde_json::to_vec(&json!({
                    "tick": view.tick, "coordinate": view.coordinate_seconds, "proper": view.proper_seconds, "rate": view.rate,
                    "beta": view.beta, "doll_rate": view.doll_rate, "doll_beta": view.doll_beta, "position": view.position_light_seconds,
                    "heading": view.heading, "doll": view.doll, "level": view.level, "burning": view.burning, "keys": view.keys,
                    "alive": view.alive, "loss": view.loss, "refusals": view.refusals, "impact": Option::<serde_json::Value>::None,
                    "seen": rows
                }))
                .unwrap();
                let t4 = Instant::now();
                std::hint::black_box(&wire);
                engine_ms.push((t2 - t1).as_secs_f64() * 1e3);
                gather_ms.push((t3 - t2).as_secs_f64() * 1e3);
                wire_ms.push((t4 - t3).as_secs_f64() * 1e3);
                rows_seen += view.seen.len();
                if f == 0 {
                    wire_bytes = wire.len();
                }
                let mut sky_px = Vec::with_capacity(view.seen.len());
                for s in &view.seen {
                    let x = ((s.light_seconds.max(1e-6).log10() - lo) / (hi - lo)).clamp(0.0, 1.0);
                    let r = r_sky * x;
                    let ang = s.direction[1].atan2(s.direction[0]);
                    sky_px.push(((cx + r * ang.sin()).round() as i64, (cy - r * ang.cos()).round() as i64));
                }
                if let Some(ps) = &prev {
                    static_sky_tot += sky_px.iter().zip(ps).filter(|(a, b)| a == b).count();
                    census_frames += 1;
                }
                prev = Some(sky_px);
            }
            let mut total: Vec<f64> = engine_ms.iter().zip(&gather_ms).zip(&wire_ms).map(|((e, g), w)| e + g + w).collect();
            total.sort_by(|a, b| a.partial_cmp(b).unwrap());
            let mut g = gather_ms.clone();
            g.sort_by(|a, b| a.partial_cmp(b).unwrap());
            let mut e = engine_ms.clone();
            e.sort_by(|a, b| a.partial_cmp(b).unwrap());
            let mut w = wire_ms.clone();
            w.sort_by(|a, b| a.partial_cmp(b).unwrap());
            let rows = rows_seen as f64 / frames as f64;
            println!(
                "base N={n}: {bodies} bodies, {frames} frames at rtf {rtf} (build {build:.1} s): total ms p50 {:.3} p99 {:.3} max {:.3} (engine {:.3} · gather {:.3}/{:.3} · wire {:.3}); wire {:.2} MB/frame; sky-static {:.2}%",
                pct(&total, 0.5), pct(&total, 0.99), pct(&total, 1.0), pct(&e, 0.5), pct(&g, 0.5), pct(&g, 0.99), pct(&w, 0.5), wire_bytes as f64 / 1e6, if census_frames > 0 { static_sky_tot as f64 / census_frames as f64 / rows * 100.0 } else { 0.0 }
            );
            println!(
                "base: n={n} bodies={bodies} frames={frames} rtf={rtf} total_p50={:.3} total_p99={:.3} total_max={:.3} engine_p50={:.3} gather_p50={:.3} wire_p50={:.3} wire_mb={:.2} rows={}",
                pct(&total, 0.5), pct(&total, 0.99), pct(&total, 1.0), pct(&e, 0.5), pct(&g, 0.5), pct(&w, 0.5), wire_bytes as f64 / 1e6, rows.round() as usize
            );
        }
        "disp" => {
            let display = args.get(5).cloned().unwrap_or_else(|| "map".into());
            let zoommode = args.get(6).cloned().unwrap_or_else(|| "fit".into());
            let events = args.get(7).cloned().unwrap_or_else(|| "coast".into());
            let audit_every: usize = args.get(8).and_then(|s| s.parse().ok()).unwrap_or(0);
            disp_mode(&mut p, bodies, frames, rtf, display != "sky", zoommode == "belt", &events, audit_every);
        }
        _ => {
            eprintln!("modes: base, digest, disp");
            std::process::exit(2);
        }
    }
    if let Some(kb) = hwm_kb() {
        println!("rss_hwm_mb {:.0}", kb as f64 / 1024.0);
    }
}

fn hwm_kb() -> Option<u64> {
    std::fs::read_to_string("/proc/self/status").ok().and_then(|s| {
        s.lines().find(|l| l.starts_with("VmHWM")).and_then(|l| l.split_whitespace().nth(1).and_then(|v| v.parse::<u64>().ok()))
    })
}

// ---- the display side: the row-set deletion (canvas test + display quantum + a delta wire) ----
//
// The policy is all client-visible state, no physics of its own: `gather_rows` (the shipped crossings) reads
// exactly the bodies the policy lists, a body is listed only when its drawn pixel could have crossed the
// display quantum (a timing wheel of dues), and the wire carries only the rows that moved, plus the marker
// rows and the panel band the page always prints. The quantum lives in the row's own frame, not the
// display's: the map pixel at the current zoom, and the sky's heading-free polar (radius, angle) — a turn
// rotates the sky client-side from the header, so a turn costs the server nothing; a zoom change re-anchors
// every row (a cheap sweep over cached rows, no readouts) and re-derives the dues at the new scale.

const CX2: f64 = 960.0;
const CY2: f64 = 540.0;
const R_SKY: f64 = 0.45 * 960.0;
const LO_SKY: f64 = -5.0;
const HI_SKY: f64 = 3.6;
const WHEEL: usize = 1 << 15;
const DUE_CAP: u64 = 1 << 14;
const MARGIN: f64 = 20.0;

fn map_px_at(offset: [f64; 2], s: f64) -> (f64, f64) {
    (960.0 + s * offset[0], 540.0 + s * offset[1])
}

fn on_canvas(px: (f64, f64)) -> bool {
    px.0 > -MARGIN && px.0 < 1920.0 + MARGIN && px.1 > -MARGIN && px.1 < 1080.0 + MARGIN
}

/// The pixel gap from a point to the canvas's margin box.
fn gap_to_canvas(px: (f64, f64)) -> f64 {
    let gx = (-MARGIN - px.0).max(px.0 - (1920.0 + MARGIN));
    let gy = (-MARGIN - px.1).max(px.1 - (1080.0 + MARGIN));
    gx.max(gy).max(0.0)
}

fn sky_pol(direction: [f64; 2], light_seconds: f64) -> (f64, f64) {
    let x = ((light_seconds.max(1e-6).log10() - LO_SKY) / (HI_SKY - LO_SKY)).clamp(0.0, 1.0);
    (R_SKY * x, direction[1].atan2(direction[0]))
}

fn sky_px_of(pol: (f64, f64), heading: f64) -> (i64, i64) {
    let ang = pol.1 - heading;
    ((960.0 + pol.0 * ang.sin()).round() as i64, (540.0 - pol.0 * ang.cos()).round() as i64)
}

fn wire_id_of(seen_id: usize) -> u64 {
    if seen_id == usize::MAX {
        u64::MAX
    } else if seen_id >= 1_000_000 {
        (1u64 << 40) + seen_id as u64
    } else {
        seen_id as u64
    }
}

struct RowState {
    wire_id: u64,
    kind: u8,
    name: String,
    direction: [f64; 2],
    light_seconds: f64,
    offset: [f64; 2],
    closing: f64,
    color: [f64; 3],
    shift: f64,
    served: bool,
    /// The pixel the client draws on the map from its held row (its quantum anchor).
    map_anchor: (i64, i64),
    /// The last exact readout's map pixel (drift is measured between reads).
    read_px: (f64, f64),
    /// The heading-free sky polar at the last read (the served anchor).
    sky_read: (f64, f64),
    due: u64,
    last_read: u64,
    map_drift: f64,
    sky_drift: f64,
    /// The due interval used at the last read (the zero-drift backoff grows it ×4).
    interval: u64,
    /// The panel band: read and served every frame (the page prints its numbers live).
    in_band: bool,
}

#[derive(Clone)]
struct Held {
    kind: u8,
    name: String,
    direction: [f64; 2],
    light_seconds: f64,
    offset: [f64; 2],
    closing: f64,
    color: [f64; 3],
    shift: f64,
    map_anchor: (i64, i64),
    /// The sky polar the client draws from (radius, angle), heading-free.
    sky_pol: (f64, f64),
}

fn held_of(r: &RowState) -> Held {
    Held { kind: r.kind, name: r.name.clone(), direction: r.direction, light_seconds: r.light_seconds, offset: r.offset, closing: r.closing, color: r.color, shift: r.shift, map_anchor: r.map_anchor, sky_pol: r.sky_read }
}

fn held_of_seen(s: &emergent_universe::view::Seen) -> Held {
    let pol = sky_pol(s.direction, s.light_seconds);
    let sky_anchor = sky_px_of(pol, 0.0);
    Held { kind: s.kind, name: s.name.clone(), direction: s.direction, light_seconds: s.light_seconds, offset: s.offset, closing: s.closing, color: s.color, shift: s.shift, map_anchor: (i64::MIN, i64::MIN), sky_pol: pol }
}

struct Disp {
    rows: Vec<Option<RowState>>,
    wheel: Vec<Vec<u32>>,
    always: Vec<usize>,
    band: Vec<usize>,
    held: std::collections::HashMap<u64, Held>,
    /// body index by wire id, for the rows `gather_rows` returns.
    view_log: f64,
    view_target: f64,
    near: f64,
    map_mode: bool,
}

impl Disp {
    fn new(map_mode: bool) -> Self {
        Disp { rows: Vec::new(), wheel: vec![Vec::new(); WHEEL], always: Vec::new(), band: Vec::new(), held: std::collections::HashMap::new(), view_log: f64::NAN, view_target: f64::NAN, near: 1e9, map_mode }
    }
    fn s(&self) -> f64 {
        10f64.powf(self.view_log)
    }
    /// The next due from observed drift and the gap to the canvas: when half a display pixel (or the
    /// margin) could have been crossed. The ×4 slack is acceleration and arrival-rate room.
    fn due_from(&mut self, i: usize, f: u64) -> u64 {
        let r = self.rows[i].as_ref().unwrap();
        let map_d = r.map_drift * 4.0;
        let sky_d = r.sky_drift * 4.0;
        let px = r.read_px;
        let gap = gap_to_canvas(px);
        // Zero observed drift can only be trusted as far as the last interval stretched: grow it ×4.
        let backoff = r.interval.saturating_mul(4).max(1) as f64;
        let mut q = backoff;
        let mut frozen = true;
        if map_d <= 0.0 && sky_d <= 0.0 {
            // Drift not yet measured (the fill, or a newborn): nothing reaches the canvas faster than
            // light, so the first due is the light-crossing time of the gap (in frames of game time).
            let gap_ls = if self.s() > 0.0 { gap / self.s() } else { f64::INFINITY };
            let dt_frame = 1.0 / 60.0 * 100.0; // game seconds per presented frame at rtf 100
            q = q.min((gap_ls / dt_frame).ceil().max(1.0));
        }
        if self.map_mode && gap > 0.0 && r.kind >= 3 {
            // Off the canvas in map mode: due when it could reach the margin.
            if map_d > 0.0 {
                q = q.min(gap / map_d);
                frozen = false;
            }
        } else if map_d > 0.0 {
            q = q.min(0.5 / map_d);
            frozen = false;
        }
        if !self.map_mode || r.kind <= 2 {
            if sky_d > 0.0 {
                q = q.min(0.5 / sky_d);
                frozen = false;
            }
        }
        // A moving row is read every frame its quantum could flip; only the frozen rows stretch, and
        // their stretch is jittered by body so the backoff does not bring them all due in one wave.
        let jitter = if frozen { 1 + (i.wrapping_mul(2654435761) % 7) as u64 } else { 0 };
        let q = (q.floor().max(1.0) as u64).saturating_add(jitter).min(DUE_CAP);
        self.rows[i].as_mut().unwrap().interval = q;
        f + q
    }
    /// Set a row's due and put it in the wheel whenever it moved (the old slot's entry, if any, is
    /// skipped lazily at pop time: a popped entry only counts when its row's due says now).
    fn reslot(&mut self, i: usize, due: u64) {
        if due != self.rows[i].as_ref().unwrap().due {
            self.rows[i].as_mut().unwrap().due = due;
            self.wheel[(due as usize) % WHEEL].push(i as u32);
        }
    }
    /// Re-anchor every row at a new map zoom (the client re-derives its pixels from held data; no
    /// readouts). A row that the NEXT eased step brings onto the canvas is due at once: entries during a
    /// zoom arrive on the zoom's geometric schedule, not by motion, so the drift bound cannot see them.
    fn sweep_zoom(&mut self, f: u64, s_next: f64) {
        let s = self.s();
        for (i, ro) in self.rows.iter_mut().enumerate() {
            let Some(r) = ro else { continue };
            let px = map_px_at(r.offset, s);
            r.read_px = px;
            r.last_read = f;
            r.map_anchor = (px.0.round() as i64, px.1.round() as i64);
            if let Some(h) = self.held.get_mut(&r.wire_id) {
                h.map_anchor = r.map_anchor;
            }
            let _ = i;
        }
        let n = self.rows.len();
        for i in 0..n {
            if self.rows[i].is_none() {
                continue;
            }
            let off = self.rows[i].as_ref().unwrap().offset;
            if on_canvas(map_px_at(off, s_next)) {
                self.reslot_early(i, f + 1);
            } else {
                let due = self.due_from(i, f);
                self.reslot_early(i, due);
            }
        }
    }
    fn reslot_early(&mut self, i: usize, due: u64) {
        self.reslot(i, due);
    }
    /// The panel band: the nearest bodies by cached distance (the page prints the nearest 8; the band
    /// keeps a slack of 2× and 16 rows so membership changes never miss a read).
    fn reband(&mut self) {
        let mut best: Vec<(f64, usize)> = Vec::new();
        for (i, ro) in self.rows.iter().enumerate() {
            let Some(r) = ro else { continue };
            if r.kind == 4 {
                continue;
            }
            if best.len() < 16 {
                best.push((r.light_seconds, i));
                best.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());
            } else if r.light_seconds < best[15].0 {
                best[15] = (r.light_seconds, i);
                best.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());
            }
        }
        let cut = if best.is_empty() { f64::INFINITY } else { best[best.len() - 1].0 * 2.0 + 1e-9 };
        self.band = self.rows.iter().enumerate().filter_map(|(i, ro)| {
            let r = ro.as_ref()?;
            (r.kind != 4 && r.light_seconds <= cut).then_some(i)
        }).collect();
        for ro in self.rows.iter_mut() {
            if let Some(r) = ro.as_mut() {
                r.in_band = false;
            }
        }
        for &i in &self.band {
            if let Some(r) = self.rows[i].as_mut() {
                r.in_band = true;
            }
        }
    }
}

fn disp_mode(p: &mut emergent_universe::scenario::Plane, bodies: usize, frames: usize, rtf: f64, map_mode: bool, belt: bool, events: &str, audit_every: usize) {
    use emergent_universe::view::gather_rows;
    let mut vcache = ViewCache::default();
    let mut acache = ViewCache::default();
    let mut d = Disp::new(map_mode);
    let mut keys = 0u8;
    let mut newborns: Vec<usize> = Vec::new();
    let turn_at = frames / 4;
    let zoom_at = frames * 3 / 5;
    let mut stats = Stats::default();

    // Warm-up: the fill (every body read once) and the fitted zoom happen here, untimed, like the page's
    // first second; both audit and display memos warm.
    let warm = 30;
    for _ in 0..warm {
        let _ = p.u.frame_to(1.0 / 60.0, rtf, Budget::wall(5.0), i64::MAX);
        let _ = emergent_universe::view::gather_cached(&p.u, &p.names, &mut acache);
    }
    let all: Vec<usize> = (0..p.u.n_bodies()).collect();
    let _ = p.u.frame_to(1.0 / 60.0, rtf, Budget::wall(5.0), i64::MAX);
    let t_fill = Instant::now();
    let (head, seen) = gather_rows(&p.u, &p.names, &mut vcache, &all).expect("view");
    let fill_rows = seen.len();
    // The page's fitLog: the nearest kind≤3 row holds 0.33·R pixels.
    d.near = seen.iter().filter(|(_, s)| s.kind <= 3).map(|(_, s)| s.light_seconds).fold(f64::INFINITY, f64::min);
    let fit = (0.33 * 432.0 / d.near.max(1e-6)).log10();
    d.view_log = if belt { fit - 2.6 } else { fit };
    d.view_target = d.view_log;
    d.rows = Vec::with_capacity(p.u.n_bodies());
    for _ in 0..p.u.n_bodies() {
        d.rows.push(None);
    }
    let mut nearest_fleet: Option<u64> = None;
    let mut best_ls = f64::INFINITY;
    for (_, s) in &seen {
        if s.kind == 4 && s.light_seconds < best_ls {
            best_ls = s.light_seconds;
            nearest_fleet = Some(wire_id_of(s.id));
        }
    }
    let mut fill_served: Vec<&Seen> = Vec::new();
    let mut fill_gone: Vec<u64> = Vec::new();
    for (bi, s) in &seen {
        match bi {
            Some(i) => absorb(&mut d, *i, s, 0),
            None => serve_side(&mut d, s, nearest_fleet, &mut fill_gone, &mut fill_served),
        }
    }
    for i in 0..d.rows.len() {
        let (wid, kind, due) = match d.rows[i].as_ref() {
            Some(r) => (r.wire_id, r.kind, d.due_from(i, 0)),
            None => continue,
        };
        if kind <= 2 {
            d.always.push(i);
        }
        d.rows[i].as_mut().unwrap().due = due;
        d.wheel[(due as usize) % WHEEL].push(i as u32);
    }
    d.reband();
    let fill_ms = t_fill.elapsed().as_secs_f64() * 1e3;
    let mut served_fill = 0usize;
    for f in 0..frames {
        // The keys: one turn held for 30 frames.
        let want = if events == "turn" && f >= turn_at && f < turn_at + 30 { 4u8 } else { 0u8 };
        if want != keys {
            let now = p.u.now;
            p.u.input(now, want).unwrap();
            keys = want;
        }
        let in_turn = events == "turn" && f >= turn_at && f < turn_at + 30;
        let t1 = Instant::now();
        let fr = p.u.frame_to(1.0 / 60.0, rtf, Budget::wall(5.0), i64::MAX);
        let t2 = Instant::now();
        // The zoom ease (the page's own): viewLog += (target − viewLog)·0.3.
        if events == "zoomout" && f == zoom_at {
            // The belt's own scale: the 3 AU of it across the canvas (an absolute zoom, not relative to
            // the fitted one, whose `near` changes with N).
            d.view_target = (432.0 / 1500.0_f64).log10();
        }
        let mut swept = false;
        if (d.view_target - d.view_log).abs() > 1e-4 {
            let next = d.view_log + (d.view_target - d.view_log) * 0.3;
            d.view_log = if (d.view_target - next).abs() < 1e-4 { d.view_target } else { next };
            d.sweep_zoom(f as u64, 10f64.powf(next));
            swept = true;
        }
        let easing = events == "zoomout" && f >= zoom_at && (d.view_target - d.view_log).abs() > 1e-4;
        // Births and deaths, once a second of frames: a fleet member handed out to a doll is born as a
        // body mid-flight (the engine's own event feed would say so; a scan stands in for it here), and a
        // lost body's row leaves the client.
        let mut pending_gone: Vec<u64> = Vec::new();
        // The engine said something changed, or the periodic stand-in for its event feed: a fleet member
        // handed out to a doll is born as a body (the engine's own feed would say so at once; a scan every
        // 10 frames stands in for it here, and costs one alive-check per body per scan).
        let nb_now = p.u.n_bodies();
        let grew = nb_now > d.rows.len();
        while d.rows.len() < nb_now {
            d.rows.push(None);
        }
        // The full sweep only when bodies were born (the count grew) or on a slow death sweep: `rec(i)`
        // is not free, and the scan must not become the Θ(N) it replaces (the engine's event counter
        // fires on every kick, so it says nothing about births at belt scale).
        if grew || f % 240 == 0 {
            let nb = nb_now;
            for i in 0..nb {
                let alive = p.u.rec(i).alive;
                match (d.rows[i].is_some(), alive) {
                    (false, true) => newborns.push(i),
                    (true, false) => {
                        if let Some(r) = d.rows[i].as_ref() {
                            if r.served {
                                pending_gone.push(r.wire_id);
                            }
                        }
                        d.rows[i] = None;
                    }
                    _ => {}
                }
            }
        }
        if std::env::var("DISP_DEBUG").is_ok() && events == "zoomout" && f >= zoom_at && f <= zoom_at + 24 && f % 4 == 0 {
            let sc = d.s();
            let mut oc = 0;
            for ro in d.rows.iter().flatten() {
                if on_canvas(map_px_at(ro.offset, sc)) { oc += 1; }
            }
            eprintln!("ZOOM f {} log {:.3} target {:.3} fit {:.3} S {:.3} rows_oncanvas(cached) {} held {}", f, d.view_log, d.view_target, fit, sc, oc, d.held.len());
        }
        // Who is due: the wheel's slot, the marker rows, the panel band, the newborns.
        let slot = std::mem::take(&mut d.wheel[f % WHEEL]);
        let mut due: Vec<usize> = Vec::with_capacity(64);
        for i in slot {
            let i = i as usize;
            if d.rows[i].as_ref().is_some_and(|r| r.due <= f as u64) {
                due.push(i);
            }
        }
        for &i in d.always.iter().chain(d.band.iter()) {
            due.push(i);
        }
        // A zoom step that brought rows onto the canvas reads them now: entries arrive on the zoom's
        // schedule, not by motion, so the wheel cannot see them (the sweep already re-anchored everyone).
        if swept {
            for i in 0..d.rows.len() {
                if let Some(r) = d.rows[i].as_ref() {
                    if !d.held.contains_key(&r.wire_id) && on_canvas(map_px_at(r.offset, d.s())) && r.kind > 2 {
                        due.push(i);
                    }
                }
            }
        }
        due.extend(newborns.drain(..));
        due.sort_unstable();
        due.dedup();
        let (head, seen) = gather_rows(&p.u, &p.names, &mut vcache, &due).expect("view");
        let readouts = vcache.readouts;
        if std::env::var("DISP_DEBUG").is_ok() && (f >= 4 && f <= 8) {
            let in_due = due.contains(&28);
            let in_seen = seen.iter().any(|(b, _)| *b == Some(28));
            let r28 = d.rows[28].as_ref().map(|r| (r.due, r.last_read, r.map_drift, r.interval));
            eprintln!("T28 f {} in_due {} in_seen {} row {:?} slot_len {}", f, in_due, in_seen, r28, d.wheel[f % WHEEL].len());
        }
        if std::env::var("DISP_DEBUG").is_ok() && (f < 2 || f == 70) {
            eprintln!("SEEN f {} len {} k4 {} due {} always {} band {}", f, seen.len(), seen.iter().filter(|(_, s)| s.kind == 4).count(), due.len(), d.always.len(), d.band.len());
            if f == 70 {
                let m = seen.iter().find(|(_, s)| s.id == 1000021);
                eprintln!("M21 in seen: {:?} bi={:?}", m.map(|(_, s)| s.offset), m.map(|(b, _)| b));
                {
                    let key = (1u64 << 40) + 1000021;
                    let mut found = None;
                    for (i, ro) in d.rows.iter().enumerate() {
                        if let Some(r) = ro { if r.wire_id == key { found = Some((i, r.due, r.last_read, r.served, r.map_anchor, r.map_drift)); } }
                    }
                    eprintln!("M21 row: {:?} held_anchor {:?}", found, d.held.get(&key).map(|h| h.map_anchor));
                }
                let mut k4rows = 0; let mut overdue = 0;
                for (i, ro) in d.rows.iter().enumerate() {
                    if let Some(r) = ro {
                        if r.kind == 4 { k4rows += 1; if r.due <= f as u64 { overdue += 1; } }
                    }
                }
                eprintln!("ROWS k4 bodies {} of {} rows, k4 due<=f {}", k4rows, d.rows.len(), overdue);
                for (i, ro) in d.rows.iter().enumerate() {
                    if let Some(r) = ro {
                        if r.kind == 4 && i % 7 == 0 { eprintln!("  k4row {} due {} served {} drift {}", i, r.due, r.served, r.map_drift); }
                    }
                }
            }
        }
        // The nearest fleet row is printed even off-canvas.
        let mut nearest_fleet: Option<u64> = None;
        let mut best_ls = f64::INFINITY;
        for (_, s) in &seen {
            if s.kind == 4 && s.light_seconds < best_ls {
                best_ls = s.light_seconds;
                nearest_fleet = Some(wire_id_of(s.id));
            }
        }
        let mut gone: Vec<u64> = Vec::new();
        let mut served_rows: Vec<&Seen> = Vec::new();
        for (bi, s) in &seen {
            match bi {
                Some(i) => {
                    if d.rows[*i].is_none() {
                        absorb(&mut d, *i, s, f as u64);
                        if d.rows[*i].as_ref().is_some_and(|r| r.served) {
                            served_rows.push(s);
                        }
                    } else {
                        absorb_row(&mut d, *i, s, f as u64, nearest_fleet == Some(wire_id_of(s.id)), &mut gone, &mut served_rows);
                    }
                }
                None => serve_side(&mut d, s, nearest_fleet, &mut gone, &mut served_rows),
            }
        }
        gone.extend(pending_gone.iter().copied());
        for &g in &pending_gone {
            d.held.remove(&g);
        }
        // Rows that were due but produced nothing are gone (unreadable or lost).
        for &i in &due {
            if let Some(r) = d.rows[i].as_ref() {
                if r.last_read < f as u64 && r.served {
                    gone.push(r.wire_id);
                    d.held.remove(&r.wire_id);
                    d.rows[i].as_mut().unwrap().served = false;
                }
            }
        }
        if f % 60 == 59 {
            d.reband();
        }
        // The delta wire: the header every frame, the rows that moved, the ids that left.
        let rows_json: Vec<_> = served_rows.iter().map(|s| {
            json!({"id": wire_id_of(s.id), "name": s.name, "kind": s.kind, "direction": s.direction, "light_seconds": s.light_seconds,
                   "offset": s.offset, "closing": s.closing, "color": s.color, "shift": s.shift})
        }).collect();
        let wire = serde_json::to_vec(&json!({
            "tick": head.t_now, "coordinate": head.t_now as f64 * emergent_universe::view::TICK_SECONDS, "proper": head.proper, "rate": head.rate_obs,
            "beta": head.vo, "doll_rate": head.doll_rate, "doll_beta": head.doll_beta, "position": [head.xo[0] * emergent_universe::view::TICK_SECONDS, head.xo[1] * emergent_universe::view::TICK_SECONDS],
            "heading": [head.heading.cos(), head.heading.sin()], "level": 0, "burning": false, "keys": keys, "alive": true, "loss": Option::<String>::None, "refusals": 0,
            "rows": rows_json, "gone": gone
        })).unwrap();
        let t3 = Instant::now();
        std::hint::black_box(&wire);
        let engine_ms = (t2 - t1).as_secs_f64() * 1e3;
        let gather_ms = (t3 - t2).as_secs_f64() * 1e3;
        let total_ms = engine_ms + gather_ms;
        stats.push(f, total_ms, engine_ms, gather_ms, wire.len(), served_rows.len(), readouts as f64, in_turn, swept, 0);
        if f == 0 {
            served_fill = served_rows.len();
        }
        // The audit: the shipped gather on the same frame, compared against what the client would draw.
        if audit_every > 0 && f % audit_every == 0 {
            let exact = emergent_universe::view::gather_cached(&p.u, &p.names, &mut acache).expect("view");
            if std::env::var("DISP_DEBUG").is_ok() && f == 70 {
                let mine: std::collections::HashSet<usize> = seen.iter().map(|(_, s)| s.id).collect();
                let theirs: std::collections::HashSet<usize> = exact.seen.iter().map(|s| s.id).collect();
                eprintln!("DIFF missing: {:?}", theirs.difference(&mine).take(10).collect::<Vec<_>>());
                eprintln!("DIFF extra: {:?}", mine.difference(&theirs).take(10).collect::<Vec<_>>());
                let m21 = exact.seen.iter().find(|s| s.id == 1000021);
                eprintln!("M21 exact row: {:?}", m21.map(|s| (s.offset, s.kind)));
                for (i, ro) in d.rows.iter().enumerate() {
                    if let Some(r) = ro {
                        if r.wire_id == 1000021 {
                            eprintln!("M21 rowstate idx {} due {} last_read {} served {} drift {}", i, r.due, r.last_read, r.served, r.map_drift);
                        }
                    }
                }
                eprintln!("M21 due list len {}", due.len());
            }
            stats.audit(&exact, &d.held, d.s(), head.heading, map_mode);
        }
    }
    stats.report(bodies, frames, rtf, map_mode, belt, events, audit_every, fill_ms, fill_rows, served_fill);
}

/// The star's and the fleets' rows (read every frame by `gather_rows`): the same canvas and quantum
/// tests decide whether the wire carries them.
fn serve_side<'a>(d: &mut Disp, s: &'a Seen, nearest_fleet: Option<u64>, gone: &mut Vec<u64>, served_rows: &mut Vec<&'a Seen>) {
    let wid = wire_id_of(s.id);
    let pol = sky_pol(s.direction, s.light_seconds);
    let sky_px = sky_px_of(pol, 0.0);
    let map_px = map_px_at(s.offset, d.s());
    let on = on_canvas(map_px);
    let held = d.held.get(&wid);
    let do_serve = if s.kind <= 2 || nearest_fleet == Some(wid) {
        true
    } else if d.map_mode {
        match held {
            None => on,
            Some(h) => on && (map_px.0.round() as i64, map_px.1.round() as i64) != h.map_anchor,
        }
    } else {
        // The sky's quantum is polar (radius, angle), heading-free: half a pixel.
        held.is_none_or(|h| (pol.0 - h.sky_pol.0).abs() >= 0.5 || (pol.1 - h.sky_pol.1).abs().min(std::f64::consts::TAU - (pol.1 - h.sky_pol.1).abs()) * pol.0 >= 0.5)
    };
    let was_served = held.is_some();
    if std::env::var("DISP_TRACE").map(|v| v == "1000021").unwrap_or(false) && s.id == 1000021 {
        eprintln!("TRACE f? id {} px ({},{}) anchor {:?} on {} serve {} off {:?}", s.id, map_px.0.round(), map_px.1.round(), held.map(|h| h.map_anchor), on, do_serve, s.offset);
    }
    if do_serve {
        let mut h = held_of_seen(s);
        h.map_anchor = (map_px.0.round() as i64, map_px.1.round() as i64);
        d.held.insert(wid, h);
        served_rows.push(s);
    } else if d.map_mode && was_served && !on {
        gone.push(wid);
        d.held.remove(&wid);
    }
}

/// The fill's absorption of a body row: it becomes a RowState (the served decision applies at once).
fn absorb(d: &mut Disp, idx: usize, s: &Seen, f: u64) {
    let wid = wire_id_of(s.id);
    let pol = sky_pol(s.direction, s.light_seconds);
    let map_px = map_px_at(s.offset, d.s());
    let on = on_canvas(map_px);
    let serve = if s.kind <= 2 { true } else if d.map_mode { on } else { true };
    let r = RowState {
        wire_id: wid,
        kind: s.kind,
        name: s.name.clone(),
        direction: s.direction,
        light_seconds: s.light_seconds,
        offset: s.offset,
        closing: s.closing,
        color: s.color,
        shift: s.shift,
        served: serve,
        map_anchor: (map_px.0.round() as i64, map_px.1.round() as i64),
        read_px: map_px,
        sky_read: pol,
        due: f + 1 + (idx.wrapping_mul(2654435761) % 7) as u64,
        last_read: f,
        map_drift: 0.0,
        sky_drift: 0.0,
        interval: 1,
        in_band: false,
    };
    if serve {
        d.held.insert(wid, held_of(&r));
    }
    let due = r.due;
    d.rows[idx] = Some(r);
    d.wheel[(due as usize) % WHEEL].push(idx as u32);
}

fn absorb_row<'a>(d: &mut Disp, i: usize, s: &'a Seen, f: u64, force_serve: bool, gone: &mut Vec<u64>, served_rows: &mut Vec<&'a Seen>) {
    let wid = wire_id_of(s.id);
    let pol = sky_pol(s.direction, s.light_seconds);
    let sky_px = sky_px_of(pol, 0.0);
    let map_px = map_px_at(s.offset, d.s());
    let on = on_canvas(map_px);
    let r = d.rows[i].as_mut().unwrap();
    let df = (f - r.last_read).max(1) as f64;
    let map_drift = (((map_px.0 - r.read_px.0).powi(2) + (map_px.1 - r.read_px.1).powi(2)).sqrt() / df).max(r.map_drift * 0.5);
    let dr = (pol.0 - r.sky_read.0).abs();
    let dth = (pol.1 - r.sky_read.1).abs().min(std::f64::consts::TAU - (pol.1 - r.sky_read.1).abs()) * pol.0;
    let sky_drift = (dr.max(dth) / df).max(r.sky_drift * 0.5);
    r.direction = s.direction;
    r.light_seconds = s.light_seconds;
    r.offset = s.offset;
    r.closing = s.closing;
    r.color = s.color;
    r.shift = s.shift;
    r.read_px = map_px;
    r.sky_read = pol;
    r.last_read = f;
    r.map_drift = map_drift;
    r.sky_drift = sky_drift;
    let was = r.served;
    let do_serve = if r.kind <= 2 || force_serve || r.in_band {
        true
    } else if d.map_mode {
        if on {
            !was || (map_px.0.round() as i64, map_px.1.round() as i64) != d.held.get(&wid).map(|h| h.map_anchor).unwrap_or((i64::MIN, i64::MIN))
        } else {
            false
        }
    } else {
        !was || d.held.get(&wid).map(|h| (pol.0 - h.sky_pol.0).abs() >= 0.5 || (pol.1 - h.sky_pol.1).abs().min(std::f64::consts::TAU - (pol.1 - h.sky_pol.1).abs()) * pol.0 >= 0.5).unwrap_or(true)
    };
    if do_serve {
        r.served = true;
        r.map_anchor = (map_px.0.round() as i64, map_px.1.round() as i64);
        let rr = d.rows[i].as_ref().unwrap();
        d.held.insert(wid, held_of(rr));
        served_rows.push(s);
    } else if d.map_mode && was && !on {
        r.served = false;
        gone.push(wid);
        d.held.remove(&wid);
    }
    let due = d.due_from(i, f);
    d.reslot_early(i, due);
}

#[derive(Default)]
struct Stats {
    total: Vec<f64>,
    engine: Vec<f64>,
    gather: Vec<f64>,
    wire_bytes: Vec<usize>,
    served: Vec<usize>,
    readouts: Vec<f64>,
    steady_total: Vec<f64>,
    steady_gather: Vec<f64>,
    turn_max_ms: f64,
    turn_served_max: usize,
    turn_frames: usize,
    zoom_max_ms: f64,
    zoom_served_max: usize,
    zoom_frames: usize,
    zoom_readouts: f64,
    viol_px: u64,
    viol_miss: u64,
    viol_ghost: u64,
    viol_panel: u64,
    audit_frames: u64,
    audit_drawn: u64,
}

impl Stats {
    fn push(&mut self, _f: usize, total: f64, engine: f64, gather: f64, wire: usize, served: usize, readouts: f64, in_turn: bool, in_zoom: bool, _ticks: i64) {
        self.total.push(total);
        self.engine.push(engine);
        self.gather.push(gather);
        self.wire_bytes.push(wire);
        self.served.push(served);
        self.readouts.push(readouts);
        if in_turn {
            self.turn_max_ms = self.turn_max_ms.max(total);
            self.turn_served_max = self.turn_served_max.max(served);
            self.turn_frames += 1;
        } else if in_zoom {
            self.zoom_max_ms = self.zoom_max_ms.max(total);
            self.zoom_served_max = self.zoom_served_max.max(served);
            self.zoom_frames += 1;
            self.zoom_readouts += readouts;
        } else {
            self.steady_total.push(total);
            self.steady_gather.push(gather);
        }
    }
    fn audit(&mut self, exact: &emergent_universe::view::View, held: &std::collections::HashMap<u64, Held>, s: f64, heading: f64, map_mode: bool) {
        let before = self.viol_px + self.viol_miss + self.viol_ghost;
        self.audit_frames += 1;
        for e in &exact.seen {
            let wid = wire_id_of(e.id);
            let map_px = map_px_at(e.offset, s);
            let draws = if map_mode { e.kind <= 2 || on_canvas(map_px) } else { true };
            let h = held.get(&wid);
            if draws {
                self.audit_drawn += 1;
                match h {
                    None => { if std::env::var("DISP_DEBUG").is_ok() && self.viol_miss < 4 { eprintln!("VIOL miss id {} kind {} name {}", e.id, e.kind, e.name); } self.viol_miss += 1; }
                    Some(h) => {
                        if map_mode {
                            let ex = (map_px.0.round() as i64, map_px.1.round() as i64);
                            if ex != h.map_anchor {
                                self.viol_px += 1;
                                if std::env::var("DISP_DEBUG").is_ok() && self.audit_frames == 100 && self.viol_px < 4200 {
                                    eprintln!("VIOL px id {} kind {} name {} ex {:?} held {:?} held_off {:?} ex_off {:?}", e.id, e.kind, e.name, ex, h.map_anchor, h.offset, e.offset);
                                }
                            }
                        } else {
                            // The polars, heading-free: the client rotates both by the same heading. The
                            // served threshold is half a pixel, so a held row never reaches a whole one.
                            let ep = sky_pol(e.direction, e.light_seconds);
                            let hp = sky_pol(h.direction, h.light_seconds);
                            let dth = (ep.1 - hp.1).abs().min(std::f64::consts::TAU - (ep.1 - hp.1).abs());
                            if (ep.0 - hp.0).abs() >= 1.0 || dth * ep.0 >= 1.0 {
                                self.viol_px += 1;
                            }
                        }
                    }
                }
            } else if let Some(h) = h {
                let hp = map_px_at(h.offset, s);
                if on_canvas(hp) && e.kind > 2 {
                    self.viol_ghost += 1;
                }
            }
        }
        if std::env::var("DISP_DEBUG").is_ok() && self.audit_frames % 20 == 0 {
            eprintln!("VIOLOLS f~{} added {} total px {} miss {} ghost {}", self.audit_frames, self.viol_px + self.viol_miss + self.viol_ghost - before, self.viol_px, self.viol_miss, self.viol_ghost);
        }
        // The panel: the nearest 8 by distance (kind ≠ 4) and the nearest fleet row, as the page prints them.
        let mut panel: Vec<&emergent_universe::view::Seen> = exact.seen.iter().filter(|e| e.kind != 4).collect();
        panel.sort_by(|a, b| a.light_seconds.partial_cmp(&b.light_seconds).unwrap());
        for e in panel.iter().take(8) {
            match held.get(&wire_id_of(e.id)) {
                None => { if std::env::var("DISP_DEBUG").is_ok() && self.viol_panel < 4 { eprintln!("VIOL panel MISS id {} name {}", e.id, e.name); } self.viol_panel += 1; }
                Some(h) => {
                    let bad = (h.light_seconds - e.light_seconds).abs() > 1e-4 * e.light_seconds.abs() + 1e-12
                        || (h.closing - e.closing).abs() > 1e-4 * e.closing.abs() + 1e-12
                        || (h.shift - e.shift).abs() > 1e-4 * e.shift.abs() + 1e-12
                        || h.name != e.name;
                    if bad {
                        self.viol_panel += 1;
                    }
                }
            }
        }
    }
    fn report(&self, bodies: usize, frames: usize, rtf: f64, map_mode: bool, belt: bool, events: &str, audit_every: usize, fill_ms: f64, fill_rows: usize, served_fill: usize) {
        let mut st = self.steady_total.clone();
        st.sort_by(|a, b| a.partial_cmp(b).unwrap());
        let mut sg = self.steady_gather.clone();
        sg.sort_by(|a, b| a.partial_cmp(b).unwrap());
        let served_med = median_usize(&self.served);
        let read_med = median_f(&self.readouts);
        let wire_med = median_usize(&self.wire_bytes);
        println!(
            "disp N={bodies} mode={} zoom={} events={} frames={} rtf={} (fill {:.1} ms, {} rows read, {} served): steady total ms p50 {:.3} p99 {:.3} max {:.3} · gather p50 {:.3} · wire {:.2} KB · served {} · readouts {}/{:.0} | turn: {} frames max {:.3} ms served {} | zoom: {} frames max {:.3} ms served {} readouts {:.0} | audit {} frames: px {} miss {} ghost {} panel {}",
            if map_mode { "map" } else { "sky" }, if belt { "belt" } else { "fit" }, events, frames, rtf, fill_ms, fill_rows, served_fill,
            pct(&st, 0.5), pct(&st, 0.99), pct(&st, 1.0), pct(&sg, 0.5), wire_med as f64 / 1e3, served_med, read_med, frames,
            self.turn_frames, self.turn_max_ms, self.turn_served_max,
            self.zoom_frames, self.zoom_max_ms, self.zoom_served_max, self.zoom_readouts,
            self.audit_frames, self.viol_px, self.viol_miss, self.viol_ghost, self.viol_panel,
        );
        println!(
            "disp: bodies={} frames={} steady_total_p50={:.3} steady_total_p99={:.3} steady_gather_p50={:.3} fill_ms={:.1} wire_kb={:.2} served={} readouts={:.0} turn_max_ms={:.3} zoom_max_ms={:.3} audit_viol={} audit_panel={} audit_frames={}",
            bodies, frames, pct(&st, 0.5), pct(&st, 0.99), pct(&sg, 0.5), fill_ms, wire_med as f64 / 1e3, served_med, read_med, self.turn_max_ms, self.zoom_max_ms, self.viol_px + self.viol_miss + self.viol_ghost, self.viol_panel, self.audit_frames,
        );
    }
}

fn median_usize(v: &[usize]) -> usize {
    if v.is_empty() {
        return 0;
    }
    let mut s = v.to_vec();
    s.sort_unstable();
    s[s.len() / 2]
}

fn median_f(v: &[f64]) -> f64 {
    if v.is_empty() {
        return 0.0;
    }
    let mut s = v.to_vec();
    s.sort_by(|a, b| a.partial_cmp(b).unwrap());
    s[s.len() / 2]
}
