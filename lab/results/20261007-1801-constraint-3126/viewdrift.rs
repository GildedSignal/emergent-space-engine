//! View-drift probe (run 20261007-1801-constraint-3126): what fraction of the gather's
//! per-frame per-body work changes the *displayed* output by more than a display quantum?
//!
//! Steps the plane exactly as `xtask universe --bench` does (rtf 100, 60 Hz nominal frames,
//! 5 ms engine budget, the same burn script at canonical ticks, members 400, Order::Sparse)
//! and per frame compares each emitter's View entry against the previous frame's:
//! direction (angle between unit vectors), colour (max channel diff), angular radius,
//! Doppler shift (relative). Reports the fraction of emitters below quanta, split by the
//! Newton path (bodies) and the already-carried path (fleet members), the gather's readout
//! count and wall ms, and the length of sub-quantum streaks. Plain stdout (no extra deps).
use emergent_universe::scenario::plane;
use emergent_universe::view::{gather_cached, Seen, ViewCache, TICK_SECONDS};
use emergent_universe::{fleet::Order, Budget, Config};
use std::collections::HashMap;
use std::time::Instant;

type Err = Box<dyn std::error::Error>;

/// The bench's scripted player (xtask/src/universe/mod.rs `script`), verbatim.
fn script(frame: usize) -> u8 {
    let slot = frame / 240;
    if frame % 240 < 20 {
        [1, 9, 2, 4, 1, 1 | 4, 2, 8][slot % 8]
    } else {
        0
    }
}

fn ang(a: [f64; 2], b: [f64; 2]) -> f64 {
    (a[0] * b[0] + a[1] * b[1]).clamp(-1.0, 1.0).acos()
}

fn quantile(mut v: Vec<f64>, q: f64) -> f64 {
    if v.is_empty() {
        return f64::NAN;
    }
    v.sort_by(|x, y| x.partial_cmp(y).unwrap());
    v[((v.len() - 1) as f64 * q) as usize]
}

fn main() -> Result<(), Err> {
    let args: Vec<String> = std::env::args().collect();
    let get = |i: usize, d: &str| args.get(i).cloned().unwrap_or_else(|| d.to_string());
    let rtf: f64 = get(1, "100").parse()?;
    let seconds: f64 = get(2, "10").parse()?;
    let members: u64 = get(3, "400").parse()?;
    let frames = (seconds * 60.0) as usize;
    let level = 0u8;

    let p = plane(Config::default(), 1, Order::Sparse, 1, members).map_err(|e| format!("plane: {e:?}"))?;
    let names = p.names.clone();
    let mut u = p.u;
    // The bench's canonical decision log, at the same ticks it uses.
    let per_frame = rtf / 60.0 / TICK_SECONDS;
    let mut word = 0u8;
    for n in 1..=frames {
        let w = emergent_universe::thrust::word(script(n), level);
        if w != word {
            word = w;
            u.schedule(((n - 1) as f64 * per_frame).round() as i64, w).map_err(|e| format!("schedule: {e:?}"))?;
        }
    }
    let cut = (frames as f64 * rtf / 60.0 / TICK_SECONDS).round() as i64;

    let mut cache = ViewCache::default();
    let mut prev: HashMap<usize, Seen> = HashMap::new();
    // streak[id] = consecutive frames (including current) the emitter stayed sub-quantum.
    let mut streak: HashMap<usize, u32> = HashMap::new();
    let mut streak_done: Vec<u32> = Vec::new(); // streak lengths when broken (plus closings)
    let mut frac_px: Vec<f64> = Vec::new(); // fraction of bodies below 1 px (all channels)
    let mut frac_px10: Vec<f64> = Vec::new();
    let mut frac_col: Vec<f64> = Vec::new();
    let mut frac_fleet_px: Vec<f64> = Vec::new();
    let mut readouts: Vec<u64> = Vec::new();
    let mut gms: Vec<f64> = Vec::new();
    let mut nseen: Vec<usize> = Vec::new();
    let mut nseen_bodies: Vec<usize> = Vec::new();
    let mut nalive: Vec<usize> = Vec::new();

    for _n in 1..=frames {
        u.frame_to(1.0 / 60.0, rtf, Budget::wall(5.0), cut);
        let t = Instant::now();
        let v = gather_cached(&u, &names, &mut cache).ok_or("no view: the player is unreadable")?;
        gms.push(t.elapsed().as_secs_f64() * 1e3);
        readouts.push(cache.readouts);
        nseen.push(v.seen.len());
        nseen_bodies.push(v.seen.iter().filter(|s| s.kind != 4).count());
        nalive.push((0..u.n_bodies()).filter(|&i| u.bodies().alive(i)).count());
        let px = 1.636e-3_f64; // one 1080p pixel across a 90° FOV
        let (mut sub_px, mut sub_px10, mut sub_col, mut tot, mut fleet, mut fleet_sub) =
            (0usize, 0usize, 0usize, 0usize, 0usize, 0usize);
        let mut cur: HashMap<usize, Seen> = HashMap::with_capacity(v.seen.len());
        for s in &v.seen {
            cur.insert(s.id, s.clone());
            let Some(o) = prev.get(&s.id) else { continue };
            let d_ang = ang(s.direction, o.direction);
            let d_col = s.color.iter().zip(o.color.iter()).map(|(a, b)| (a - b).abs()).fold(0.0_f64, f64::max);
            let d_rad = (s.angular_radius - o.angular_radius).abs();
            let d_shift = ((s.shift - o.shift) / o.shift).abs();
            let is_fleet = s.kind == 4;
            if is_fleet {
                fleet += 1;
            } else {
                tot += 1;
            }
            let under = |q: f64| d_ang < q && d_rad < q;
            if under(px) && d_col < 1.0 / 255.0 && d_shift < 0.01 {
                sub_px += !is_fleet as usize;
                fleet_sub += is_fleet as usize;
                *streak.entry(s.id).or_insert(0) += 1;
            } else if let Some(e) = streak.get_mut(&s.id) {
                if *e > 0 {
                    streak_done.push(*e);
                }
                *e = 0;
            }
            if under(10.0 * px) {
                sub_px10 += !is_fleet as usize;
            }
            if d_col < 1.0 / 255.0 {
                sub_col += !is_fleet as usize;
            }
        }
        if tot > 0 {
            frac_px.push(sub_px as f64 / tot as f64);
            frac_px10.push(sub_px10 as f64 / tot as f64);
            frac_col.push(sub_col as f64 / tot as f64);
        }
        if fleet > 0 {
            frac_fleet_px.push(fleet_sub as f64 / fleet as f64);
        }
        prev = cur;
    }
    // Closing streaks are still observed (bounded below by their length so far).
    for e in streak.values() {
        if *e > 0 {
            streak_done.push(*e);
        }
    }
    let med = |v: &[f64]| quantile(v.to_vec(), 0.5);
    let f64s = |v: &Vec<u64>| v.iter().map(|&r| r as f64).collect::<Vec<_>>();
    let u32s = |v: &Vec<u32>| v.iter().map(|&s| s as f64).collect::<Vec<_>>();
    println!(
        "rtf {} frames {} members {}\nbodies {} seen_median {:.0} seen_bodies_median {:.0} alive_median {:.0}\ngather_ms p50 {:.3} p99 {:.3}\nreadouts_per_frame p50 {:.1} max {}\nbodies_subquantum_frac p50_all_channels {:.3} p10 {:.3} p50_10px {:.3} p50_colour_only {:.3}\nfleet_members_subquantum_frac_p50 {:.3}\nsubquantum_streak_frames median {:.1} p90 {:.1} count {}\nquanta pixel_rad 1.636e-3 colour_step {:.5} shift_rel 0.01",
        rtf, frames, members,
        u.n_bodies(), quantile(nseen.iter().map(|&n| n as f64).collect(), 0.5), quantile(nseen_bodies.iter().map(|&n| n as f64).collect(), 0.5), quantile(nalive.iter().map(|&n| n as f64).collect(), 0.5),
        med(&gms), quantile(gms.clone(), 0.99),
        med(&f64s(&readouts)), *readouts.iter().max().unwrap_or(&0),
        med(&frac_px), quantile(frac_px.clone(), 0.1), med(&frac_px10), med(&frac_col),
        med(&frac_fleet_px),
        med(&u32s(&streak_done)), quantile(u32s(&streak_done), 0.9),
        streak_done.len(),
        1.0 / 255.0
    );
    Ok(())
}
