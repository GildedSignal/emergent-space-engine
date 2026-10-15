//! The view's per-frame floor, measured on the shipped light-cone gather (view.rs). Two instruments, one flight:
//!
//! (A) the price: the in-band gather — `gather_cached`, the pilot's instrument, called in the page's own loop
//!     order (view, then keys, then `frame_to`) — timed every frame beside the engine's own frame wall, with the
//!     cache's readouts an emitter. Across N and burn level this prices the crawl the nladder page found (a flight
//!     at ~rtf 0.7 with ~2 s frames) and answers, on the shipped instrument, whether a burn staleness the cache.
//!
//! (B) the floor: a row that is never re-read — the emission geometry frozen at one frame (the emitter's position
//!     when the light left, its Doppler denominator), the observer's state taken fresh each frame, aberration and
//!     shift recomputed observer-side, the one closed form the view owns — drifts against the freshly gathered row.
//!     The drift rate per row class sets how many frames a row can free-run before its drawn direction could cross
//!     half a pixel; the per-frame readout demand is the row count over that horizon, not the row count.
//!
//! cargo run --release -p emergent-universe --example view_floor -- [N] [coast|burn8|burn15] [frames] [rtf]
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane_extra;
use emergent_universe::thrust::word;
use emergent_universe::view::{aberration, gather_cached, Seen, ViewCache, TICK_SECONDS};
use emergent_universe::{Budget, Config};
use std::collections::HashMap;
use std::time::{Duration, Instant};

fn dot(a: [f64; 2], b: [f64; 2]) -> f64 {
    a[0] * b[0] + a[1] * b[1]
}

fn pct(sorted: &mut [f64], p: f64) -> f64 {
    if sorted.is_empty() {
        return 0.0;
    }
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap());
    sorted[(((sorted.len() - 1) as f64) * p).round() as usize]
}

/// A row as last read: where the emitter was when the light left (root frame, light-seconds), the Doppler
/// denominator `(1 − n·β_obs)/rate` of that frame, and the row's shift then.
#[derive(Clone, Copy)]
struct FrozenRow {
    emit: [f64; 2],
    denom_scale: f64, // num_then / shift_then = the emitter-side denominator
    kind: u8,
    /// far at freeze: beyond 250 light-seconds (half an AU) — the belt rows, the O(N) set at scale.
    far: bool,
    /// running max of the direction error since the freeze (a staircase quantizes: the envelope, not the last frame, is the drift)
    max_err: f64,
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let n: usize = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(10_000);
    let mode = args.get(2).cloned().unwrap_or_else(|| "coast".into());
    let frames: usize = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(300);
    let rtf: f64 = args.get(4).and_then(|s| s.parse().ok()).unwrap_or(100.0);
    let freeze_at: usize = args.get(5).and_then(|s| s.parse().ok()).unwrap_or(0);
    let level: u8 = match mode.as_str() {
        "burn8" => 8,
        "burn15" => 15,
        _ => 0,
    };
    let t0 = Instant::now();
    let mut p = plane_extra(Config::default(), 1, Order::Sparse, 1, 48, n).unwrap();
    let bodies = p.u.n_bodies();
    let build = t0.elapsed().as_secs_f64();
    let mut cache = ViewCache::default();
    let freeze = if freeze_at > 0 { freeze_at.min(frames.saturating_sub(2)) } else { frames.saturating_sub(40).max(70) };
    let (mut g_ms, mut e_ms, mut rps) = (Vec::new(), Vec::new(), Vec::new());
    let mut frozen: Option<HashMap<usize, FrozenRow>> = None;
    // per class at the last curve frame: slope of direction error (rad/frame); shift rel error; curve maxima
    let mut far_slope = Vec::new();
    let mut near_slope = Vec::new();
    let mut local_slope = Vec::new();
    let mut belt_curve: Vec<(usize, f64, f64, f64, f64)> = Vec::new(); // k, belt dir, near-ship dir, local dir, shift rel
    let mut set_changes = 0usize;
    let mut seen_last = 0usize;
    let now0 = p.u.now;
    let mut alive = true;
    for f in 0..frames {
        let tg = Instant::now();
        let view = gather_cached(&p.u, &p.names, &mut cache);
        let g = tg.elapsed().as_secs_f64() * 1e3;
        let Some(v) = view else { continue };
        seen_last = v.seen.len();
        if f == 60 && level > 0 {
            let t = p.u.now;
            let _ = p.u.input(t, word(1, level));
        }
        if f == freeze {
            let m: HashMap<usize, FrozenRow> = v
                .seen
                .iter()
                .filter(|s| s.kind != 4)
                .map(|s| {
                    let l = (dot(s.offset, s.offset)).sqrt();
                    let toward = if l > 0.0 { [s.offset[0] / l, s.offset[1] / l] } else { [1.0, 0.0] };
                    let n_prop = [-toward[0], -toward[1]];
                    let num_then = (1.0 - dot(n_prop, v.beta)) / v.rate;
                    (
                        s.id,
                        FrozenRow {
                            emit: [v.position_light_seconds[0] + s.offset[0], v.position_light_seconds[1] + s.offset[1]],
                            denom_scale: num_then / s.shift,
                            kind: s.kind,
                            far: s.light_seconds > 250.0,
                            max_err: 0.0,
                        },
                    )
                })
                .collect();
            frozen = Some(m);
        } else if f > freeze {
            let (Some(fz), k) = (frozen.as_mut(), f - freeze) else { unreachable!() };
            let fresh: HashMap<usize, &Seen> = v.seen.iter().map(|s| (s.id, s)).collect();
            let (mut bmax, mut lmax, mut nmax, mut smax) = (0.0f64, 0.0f64, 0.0f64, 0.0f64);
            for (id, row) in fz.iter_mut() {
                let Some(fr) = fresh.get(id) else { set_changes += 1; continue };
                let d = [row.emit[0] - v.position_light_seconds[0], row.emit[1] - v.position_light_seconds[1]];
                let dist = dot(d, d).sqrt();
                if dist <= 0.0 {
                    continue;
                }
                let toward = [d[0] / dist, d[1] / dist];
                let (dir_p, _) = aberration(toward, v.beta);
                let dir_t = fr.direction;
                let err = ((dir_p[0] * dir_t[1] - dir_p[1] * dir_t[0]).abs()).atan2(dot(dir_p, dir_t));
                row.max_err = row.max_err.max(err);
                let n_prop = [-toward[0], -toward[1]];
                let num_now = (1.0 - dot(n_prop, v.beta)) / v.rate;
                let shift_p = num_now / row.denom_scale;
                let serr = ((shift_p - fr.shift) / fr.shift).abs();
                if row.kind >= 3 {
                    if row.far {
                        bmax = bmax.max(err);
                        if f == frames - 1 {
                            far_slope.push(row.max_err / k as f64);
                        }
                    } else {
                        nmax = nmax.max(err);
                        if f == frames - 1 {
                            near_slope.push(row.max_err / k as f64);
                        }
                    }
                } else {
                    lmax = lmax.max(err);
                    if f == frames - 1 {
                        local_slope.push(row.max_err / k as f64);
                    }
                }
                smax = smax.max(serr);
            }
            if k % 50 == 1 {
                if let Some((pid, _)) = fz.iter().find(|(_, r)| r.far) {
                    if let Some(fr) = fresh.get(pid) {
                        eprintln!("probe id={pid} k={k} age={:.6} ls={:.6} off=({:.4},{:.4})", fr.age, fr.light_seconds, fr.offset[0], fr.offset[1]);
                    }
                }
            }
            belt_curve.push((f, bmax, nmax, lmax, smax));
        }
        let te = Instant::now();
        let _ = p.u.frame_to(1.0 / 60.0, rtf, Budget { events: u64::MAX, until: Some(te + Duration::from_millis(12)) }, i64::MAX);
        let e = te.elapsed().as_secs_f64() * 1e3;
        if f >= 60 {
            g_ms.push(g);
            e_ms.push(e);
            rps.push(cache.readouts as f64 / v.seen.len().max(1) as f64);
        }
        if !p.u.rec(p.player).alive {
            alive = false;
            break;
        }
    }
    let wall = t0.elapsed().as_secs_f64();
    let game_s = (p.u.now - now0) as f64 * TICK_SECONDS;
    let us_body = pct(&mut g_ms.clone(), 0.5) * 1e3 / bodies as f64;
    let k_last = belt_curve.last().map(|c| c.0).unwrap_or(0);
    let (half_map, half_sky) = (std::f64::consts::PI / 1920.0, (std::f64::consts::PI / 3.0) / 1920.0 / 2.0);
    let belt_p99 = pct(&mut far_slope, 0.99);
    let belt_max = far_slope.iter().cloned().fold(0.0, f64::max);
    let near_p99 = pct(&mut near_slope, 0.99);
    let local_p99 = pct(&mut local_slope, 0.99);
    println!(
        "N={n} ({bodies} bodies) {mode} rtf={rtf} frames={} build {build:.2}s wall {wall:.1}s alive={alive}; seen {seen_last}, set changes over the curve {set_changes}",
        g_ms.len() + 60
    );
    println!(
        "price: gather ms p50 {:.2} p99 {:.2} | {:.2} us/body | readouts/emitter p50 {:.2} p99 {:.2}; engine ms p50 {:.3} p99 {:.3}; rtf achieved {:.2}",
        pct(&mut g_ms.clone(), 0.5),
        pct(&mut g_ms.clone(), 0.99),
        us_body,
        pct(&mut rps.clone(), 0.5),
        pct(&mut rps.clone(), 0.99),
        pct(&mut e_ms.clone(), 0.5),
        pct(&mut e_ms.clone(), 0.99),
        game_s / wall
    );
    for (k, dir, ndir, ldir, sh) in belt_curve.iter().step_by((belt_curve.len() / 8).max(1)) {
        println!("  free-run k={k:>4}: belt max dir err {dir:.3e}, near-ship max {ndir:.3e}, local max {ldir:.3e} rad, max shift rel err {sh:.3e}");
    }
    println!(
        "floor: belt drift p99 {belt_p99:.3e} max {belt_max:.3e} rad/frame (n={}), near-ship p99 {near_p99:.3e} (n={}), locals p99 {local_p99:.3e} (n={}), k_last {k_last}; horizon at half-pixel map ({half_map:.1e}) {:.3e} frames (p99), sky ({half_sky:.1e}) {:.3e}; readout demand at N: {:.3e}/frame",
        far_slope.len(),
        near_slope.len(),
        local_slope.len(),
        half_map / belt_p99.max(1e-18),
        half_sky / belt_p99.max(1e-18),
        bodies as f64 * belt_p99 / half_map
    );
}
