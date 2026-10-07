//! Capture the plane's own kick deltas in the tube's native columns.
//! Replays exactly the `--kick-bench` loop (same script, same dedup, same pure
//! resolver) and records, per distinct ship kick that resolves to a Kick with
//! both ends bound cycles in one doll:
//!   d_t_p : periapsis-time delta, doll clock ticks (i64)
//!   d_p   : periapsis delta in Q16 root units (i128 from Scalar::fixed, fits i64)
//!   d_k   : OrbitKey k delta, Q48 (i64)
//!   d_w   : periapsis-angle delta, u32 turns (i32)
//! plus the kick's dv and window. No darwin/invariant conversion: the belt
//! program's Key domain (p <= 8192 M, L <= 4096) cannot hold the plane's
//! orbits (p ~ 1e8 M), which this run measures directly.
use emergent_space::binding::Trajectory;
use emergent_universe::body::{Kind, What};
use emergent_universe::scenario::plane;
use emergent_universe::step::{self, Resolved};
use emergent_universe::{Budget, Config};
use serde_json::json;
use std::time::Instant;

fn script(frame: usize) -> u8 {
    let slot = frame / 240;
    if frame % 240 < 20 {
        [1, 9, 2, 4, 1, 1 | 4, 2, 8][slot % 8]
    } else {
        0
    }
}

fn tube_cols(t: &Trajectory) -> Option<(i64, u64)> {
    let Trajectory::Cycle(c) = t else { return None };
    let key = c.key();
    if key.null || !key.periodic() {
        return None;
    }
    let p_q16 = key.periapsis.fixed(16).ok()?;
    i64::try_from(p_q16).ok().map(|p| (p, key.k))
}

fn main() {
    let a: Vec<String> = std::env::args().collect();
    let seed: u64 = a.iter().nth(1).and_then(|s| s.parse().ok()).unwrap_or(1);
    let seconds: f64 = a.iter().nth(2).and_then(|s| s.parse().ok()).unwrap_or(10.0);
    let members: u64 = a.iter().nth(3).and_then(|s| s.parse().ok()).unwrap_or(48);
    let out = a.iter().nth(4).cloned().unwrap_or_else(|| "kicks.json".into());
    let rtf = 100.0f64;
    let wall = Instant::now();
    let mut p = plane(
        Config::default(),
        seed,
        emergent_universe::fleet::Order::Sparse,
        1,
        members,
    )
    .expect("the plane");
    let made_n = p.u.n_bodies();
    let mut last: Vec<Option<i64>> = vec![None; made_n];
    let mut keys = 0u8;
    let mut kicks: Vec<serde_json::Value> = Vec::new();
    let (mut refused, mut excluded, mut doll_change) = (0u64, 0u64, 0u64);
    let mut digest = blake3::Hasher::new();
    let mut frames = 0usize;
    for n in 1..=(seconds * 60.0) as usize {
        if wall.elapsed().as_secs_f64() >= 55.0 {
            eprintln!("capture exceeded 55 s; stopping at frame {n}");
            break;
        }
        let now = p.u.now;
        if keys != script(n) {
            keys = script(n);
            p.u.input(now, keys).expect("input");
        }
        last.resize(p.u.n_bodies(), None);
        for (i, seen) in last.iter_mut().enumerate() {
            let rec = p.u.rec(i);
            if rec.kind != Kind::Ship || !rec.alive {
                continue;
            }
            let Some(item) = rec.plan.first().copied() else { continue };
            if !matches!(item.what, What::Kick(_)) || *seen == Some(item.t) {
                continue;
            }
            *seen = Some(item.t);
            let upd = step::process(&p.u.ctx(), i, rec.clone());
            if upd.kind != Resolved::Kick {
                refused += 1;
                continue;
            }
            let (b0, b1) = (&rec.b, &upd.rec.b);
            if b0.doll != b1.doll {
                doll_change += 1;
                excluded += 1;
                continue;
            }
            let doll = b0.doll;
            let (c0, c1) = (
                tube_cols(&b0.entry.trajectory),
                tube_cols(&b1.entry.trajectory),
            );
            if c0.is_none() || c1.is_none() {
                excluded += 1;
                continue;
            }
            let ((p0, k0), (p1, k1)) = (c0.unwrap(), c1.unwrap());
            let dtp = b1.tube.periapsis_time.get() as i64 - b0.tube.periapsis_time.get() as i64;
            let dw = b1.tube.periapsis_angle.wrapping_sub(b0.tube.periapsis_angle) as u32 as i64;
            let dw = if dw >= 1 << 31 { dw - (1 << 32) } else { dw };
            let dp = p1 - p0;
            let dk = k1 as i64 - k0 as i64;
            digest.update(
                format!(
                    "{} {} {} {} {} {} {} {} {} {:?}",
                    i, item.t, doll, dp, dk, dtp, dw, b1.kick.len, b1.kick.level, b1.kick.dv
                )
                .as_bytes(),
            );
            kicks.push(json!({
                "body": i, "t": item.t, "doll": doll, "made": i < made_n,
                "dp": dp, "dk": dk, "dtp": dtp, "dw": dw,
                "kick_len": b1.kick.len, "kick_level": b1.kick.level,
                "dv": b1.kick.dv,
                "p0_q16": p0, "k0": k0,
            }));
        }
        p.u.frame(1.0 / 60.0, rtf, Budget::unlimited());
        p.u.settle(p.u.now);
        frames = n;
    }
    std::fs::write(&out, serde_json::to_string(&kicks).unwrap()).expect("write kicks");
    println!(
        "{}",
        serde_json::to_string_pretty(&json!({
            "seed": seed, "rtf": rtf, "seconds": seconds, "members": members, "frames": frames,
            "kicks": kicks.len(), "refused": refused, "excluded": excluded, "doll_change": doll_change,
            "digest": digest.finalize().to_hex().to_string(),
            "wall_seconds": wall.elapsed().as_secs_f64(),
        }))
        .unwrap()
    );
}
