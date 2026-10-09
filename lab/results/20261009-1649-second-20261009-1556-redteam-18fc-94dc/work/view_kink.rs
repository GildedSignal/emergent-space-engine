// The checker's named gold experiment for 20261009-1556-redteam-18fc: the view-gather premise
// ("each tube crosses the observer's past light cone once; Newton from the previous frame's
// crossing finds it") on **kinked tubes** — emitters whose worldlines are kicked by the engine's
// own stepper, at closing speeds up to β→1. The straight-tube run's linearity argument (one Newton
// step lands on the root from any guess) fails on a kicked chain: `g` gains concave kinks at every
// rebind, and the memo's slope goes stale across them.
//
// Kinks are made with the shipped machinery only: a secondary (a source in the root doll) at the
// emitters' convergence point makes `has_forces` true, so `settle` steps the emitters and the
// changeover's `What::Kick` items rebind their tubes (each rebind is a kink). No crate code is
// edited; this example builds the `stream` geometry itself (scenario::stream cannot take a source).
//
// `view_kink probe`     — verify the construction: source placement, kicks per emitter, refusals.
// `view_kink run [rtf frames]` — the full record (tables in the run folder).
use emergent_universe::observe::state_rate;

use emergent_universe::universe::OrbitSpec;
use emergent_universe::view::{gather, gather_cached, ViewCache, TICK_SECONDS};
use emergent_universe::{Config, Kind as UKind, Mass, Universe};
use emergent_universe::num::from_f64 as ff;
use emergent_space::orbit::Scalar;

fn from_f64(v: f64) -> Scalar {
    ff(v)
}
fn s(v: i64) -> Scalar {
    Scalar::raw(v as i128, 0).unwrap()
}

const START: i64 = 1_200_000_000;
const R_OBS: f64 = 1.0e8;
const DIST: f64 = 1.0e6;
/// The source's offset from the convergence point, root units. Between bearings (0°), so the
/// closest approach any emitter gets is `OFF·sin(π/n)` > 0: no dead-centre flyby.
const OFF: f64 = 2.0e4;

/// The universe of `scenario::stream`, plus a secondary of mass ratio 1/999 (a Jupiter) on a
/// circular orbit that passes through `P + [0, OFF]` at `t_fly`, where P is the point the
/// `Toward` emitters converge on (the observer's position at `START`). All emitters fly through
/// the convergence point, so every one gets a flyby of the source at approach in
/// `[OFF·sin(π/n), OFF]`.
fn kinked(beta_obs: f64, beta: f64, n: usize, t_fly: i64, gm_num: u64, gm_den: u64, step_log2: i32) -> (Universe, Vec<usize>, usize, usize) {
    // Phase calibration: place the source, measure where it actually is at `t_fly`, nudge the
    // phase by the response a probe build measures (conventions absorbed, not assumed).
    let target = [R_OBS, OFF];
    let at = |phase: f64| -> [f64; 2] {
        let (u, (src, _), _) = build(beta_obs, beta, n, phase, gm_num, gm_den, step_log2);
        state_rate(&u.ctx(), src, t_fly).expect("the source's tube reads at t_fly").0
    };
    let mut phase = 0.0f64;
    let mut best = f64::MAX;
    for k in 0..64 {
        let p = k as f64 / 64.0;
        let pos = at(p);
        let e = (pos[0] - target[0]).powi(2) + (pos[1] - target[1]).powi(2);
        if e < best {
            best = e;
            phase = p;
        }
    }
    for _ in 0..6 {
        let pos0 = at(phase);
        let pos1 = at(phase + 1e-6);
        let dpos = [pos1[0] - pos0[0], pos1[1] - pos0[1]];
        let dd = dpos[0] * dpos[0] + dpos[1] * dpos[1];
        let err = [target[0] - pos0[0], target[1] - pos0[1]];
        phase += (err[0] * dpos[0] + err[1] * dpos[1]) / dd * 1e-6;
    }
    let (mut u, (src, ids), player) = build(beta_obs, beta, n, phase, gm_num, gm_den, step_log2);
    let st = state_rate(&u.ctx(), src, t_fly).unwrap();
    let err2 = ((st.0[0] - target[0]).powi(2) + (st.0[1] - target[1]).powi(2)).sqrt();
    println!(
        "source at t_fly: ({:.1},{:.1}) target ({:.1},{:.1}) err {:.1} root units, |v|={:.2e}",
        st.0[0], st.0[1], target[0], target[1], err2, (st.1[0] * st.1[0] + st.1[1] * st.1[1]).sqrt()
    );
    (u, ids, player, src)
}

fn build(beta_obs: f64, beta: f64, n: usize, phase: f64, gm_num: u64, gm_den: u64, step_log2: i32) -> (Universe, (usize, Vec<usize>), usize) {
    let mut u = Universe::new(s(471_000), Config { step_log2, ..Default::default() });
    let player = if beta_obs == 0.0 {
        u.add_body(
            UKind::Player,
            OrbitSpec { doll: 0, periapsis: from_f64(R_OBS), e_q48: 0, clockwise: false, angle: 0, phase: 0 },
            Scalar::ZERO,
        )
        .unwrap()
    } else {
        u.add_body_state(
            UKind::Player,
            0,
            [from_f64(R_OBS), from_f64(-beta_obs * START as f64)],
            [Scalar::ZERO, from_f64(beta_obs)],
            Scalar::ZERO,
        )
        .unwrap()
    };
    // The secondary: circular at the target radius, `angle` at the target direction, `phase`
    // timed so it is there at `t_fly`.
    let target = [R_OBS, OFF];
    let r_src = (target[0] * target[0] + target[1] * target[1]).sqrt();
    let th_src = target[1].atan2(target[0]);
    let t_fly = START + (DIST / beta.max(1e-9)) as i64;
    let period = 2.0 * std::f64::consts::PI * r_src / (1.0 / r_src).sqrt();
    let phase_q32 = ((phase - t_fly as f64 / period).fract().rem_euclid(1.0) * 4294967296.0) as u32;
    let src = u
        .add_body(
            UKind::Planet,
            OrbitSpec {
                doll: 0,
                periapsis: from_f64(r_src),
                e_q48: 0,
                clockwise: false,
                angle: (th_src / std::f64::consts::TAU * 4294967296.0) as u32,
                phase: phase_q32,
            },
            Scalar::ZERO,
        )
        .unwrap();
    u.make_source(src, Mass::ratio(gm_num, gm_den).unwrap(), s(300_000)).unwrap();
    // The emitters, exactly as scenario::stream makes them (Toward: they converge on P).
    let mut ids = Vec::new();
    for j in 0..n {
        let th = (j as f64 + 0.5) / n as f64 * std::f64::consts::TAU;
        let bearing = [th.cos(), th.sin()];
        let dir = [-bearing[0], -bearing[1]];
        let pos = [R_OBS + DIST * bearing[0] - beta * dir[0] * START as f64, DIST * bearing[1] - beta * dir[1] * START as f64];
        ids.push(
            u.add_body_state(
                UKind::Ship,
                0,
                [from_f64(pos[0]), from_f64(pos[1])],
                [from_f64(beta * dir[0]), from_f64(beta * dir[1])],
                Scalar::ZERO,
            )
            .unwrap(),
        );
    }
    u.start().unwrap();
    (u, (src, ids), player)
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let mode = args.first().map(|s| s.as_str()).unwrap_or("probe");
    let beta = 0.9999f64;
    let n = 12usize;
    if mode == "run20" {
        let rtf: f64 = args.get(1).map(|s| s.parse().unwrap()).unwrap_or(1.0);
        let frames: usize = args.get(2).map(|s| s.parse().unwrap()).unwrap_or(600);
        let frame = (rtf / 60.0 / TICK_SECONDS) as i64;
        let b = 0.9999f64;
        let t_fly = START + (DIST / b) as i64;
        let (mut u, ids, _p, _s) = kinked(0.0, b, 12, t_fly, 1, 999, 20);
        let mut cache = ViewCache::default();
        let (mut reads, mut worst, mut drops, mut dis, mut mismatch, mut worst_dte) = (0u64, 0u64, 0u64, 0u64, 0u64, 0i64);
        let (mut n_frames, mut unalive) = (0u64, 0u64);
        for f in 0..frames {
            let t = START + f as i64 * frame;
            u.settle(t);
            u.now = t;
            let cold = gather(&u, &[]);
            let warm = gather_cached(&u, &[], &mut cache);
            let (Some(cold), Some(warm)) = (cold, warm) else { continue };
            n_frames += 1;
            if f >= 1 {
                reads += cache.readouts;
                worst = worst.max(cache.readouts);
                let ctx = u.ctx();
                let xo = [warm.position_light_seconds[0] / TICK_SECONDS, warm.position_light_seconds[1] / TICK_SECONDS];
                for &id in &ids {
                    if !u.bodies().alive(id) { unalive += 1; continue; }
                    let c = cold.seen.iter().find(|s| s.id == id);
                    let w = warm.seen.iter().find(|s| s.id == id);
                    match (c, w) {
                        (None, None) => drops += 1,
                        (Some(c), Some(w)) => {
                            if c.offset != w.offset || c.light_seconds != w.light_seconds { dis += 1; }
                        }
                        _ => dis += 1,
                    }
                    if let Some(w) = w {
                        let te_gather = (t as f64 - w.age / TICK_SECONDS).round() as i64;
                        match bisect(&ctx, id, t, xo) {
                            Ok(te_true) => {
                                let d = te_gather - te_true;
                                if d != 0 { mismatch += 1; worst_dte = worst_dte.max(d.abs()); }
                            }
                            Err(()) => mismatch += 1,
                        }
                    }
                }
            }
        }
        let kinked = ids.iter().filter(|&&i| u.bodies().event_time(i) > 0).count();
        println!("run20 (log2 20, kinked 0.9999 toward, rtf {rtf}): reads/em={:.2} max/fr={worst} drops={drops} disagr={dis} oracle={mismatch} dte={worst_dte} [kicks={} refused={} kinked {kinked}/12 unalive={unalive}] ({n_frames} frames)",
            reads as f64 / n_frames.max(1) as f64 / 12.0, u.stats.kicks, u.stats.refused);
        return;
    }
    if mode == "slow" {
        let t_fly = START + (DIST / beta) as i64;
        let t0 = std::time::Instant::now();
        let (mut u, ids, _p, _s) = kinked(0.0, beta, n, t_fly, 1, 999, 20);
        println!("log2 20: build {:.1}s", t0.elapsed().as_secs_f64());
        let t0 = std::time::Instant::now();
        u.settle(t_fly + 200_000);
        println!("log2 20: settle {:.1}s kicks={} refused={} kinked={}/12", t0.elapsed().as_secs_f64(), u.stats.kicks, u.stats.refused, ids.iter().filter(|&&i| u.bodies().event_time(i) > 0).count());
        return;
    }
    if mode == "sweep" {
        let t_fly = START + (DIST / beta) as i64;
        for (num, den, log2) in [(1u64, 999u64, 7), (1, 99, 7), (1, 9, 7), (1, 3, 7), (1, 1, 7), (1, 999, 14), (1, 99, 14), (1, 9, 14), (1, 3, 14), (1, 999, 20), (1, 99, 20)] {
            let t0 = std::time::Instant::now();
            let (mut u, ids, _player, _src) = kinked(0.0, beta, n, t_fly, num, den, log2);
            let tb = t0.elapsed().as_secs_f64();
            let t0 = std::time::Instant::now();
            u.settle(t_fly + 200_000);
            let ts = t0.elapsed().as_secs_f64();
            let rebinding = ids.iter().filter(|&&i| u.bodies().event_time(i) > 0).count();
            // deflection of emitter 0: actual vs the constructed straight line at t_fly+2e5
            let j = 0.5 / n as f64 * std::f64::consts::TAU;
            let bearing = [j.cos(), j.sin()];
            let dir = [-bearing[0], -bearing[1]];
            let pos0 = [R_OBS + DIST * bearing[0] - beta * dir[0] * START as f64, DIST * bearing[1] - beta * dir[1] * START as f64];
            let v0 = [beta * dir[0], beta * dir[1]];
            let tch = t_fly + 200_000;
            let lin = [pos0[0] + v0[0] * tch as f64, pos0[1] + v0[1] * tch as f64];
            let act = state_rate(&u.ctx(), ids[0], tch).map(|s| s.0).unwrap_or([f64::NAN; 2]);
            let deflect = ((act[0] - lin[0]).powi(2) + (act[1] - lin[1]).powi(2)).sqrt();
            println!("gm {num}/{den} log2 {log2}: kicks={} refused={} lost={} rebinding_emitters={rebinding}/12 deflect_em0={deflect:.3e} root units (build {tb:.1}s settle {ts:.1}s)", u.stats.kicks, u.stats.refused, u.stats.lost);
        }
        return;
    }

    let t_fly = START + (DIST / beta) as i64;
    let (mut u, ids, player, src) = kinked(0.0, beta, n, t_fly, 1, 999, 14);
    match mode {
        "run" => {
            let rtf: f64 = args.get(1).map(|s| s.parse().unwrap()).unwrap_or(1.0);
            let frames: usize = args.get(2).map(|s| s.parse().unwrap()).unwrap_or(600);
            let frame = (rtf / 60.0 / TICK_SECONDS) as i64;
            println!("rtf {rtf}: {frame} ticks/frame, {frames} frames, 12 emitters at 1e6, source 1/999 at P+[0,2e4]");
            println!("{:<26} {:>8} {:>7} {:>6} {:>6} {:>7} {:>6} {:>7}", "case", "reads/em", "max/fr", "drops", "disagr", "oracle", "dte", "kinked");
            let cases: [(&str, f64, f64, u64, u64, i32, bool); 5] = [
                ("control straight 0.9999", 0.0, 0.9999, 1, 999, 7, false),
                ("kinked 0.9 toward", 0.0, 0.9, 1, 999, 14, false),
                ("kinked 0.9999 toward", 0.0, 0.9999, 1, 999, 14, false),
                ("kinked obs 0.9 x 0.9999", 0.9, 0.9999, 1, 999, 14, false),
                ("kinked 0.9999 stalejump", 0.0, 0.9999, 1, 999, 14, true),
            ];
            for (name, bo, b, gn, gd, log2, jumps) in cases {
                let t_fly = START + (DIST / b) as i64;
                let (mut u, ids, _player, _src) = kinked(bo, b, 12, t_fly, gn, gd, log2);
                let mut cache = ViewCache::default();
                let (mut reads, mut worst, mut drops, mut dis, mut mismatch, mut worst_dte) = (0u64, 0u64, 0u64, 0u64, 0u64, 0i64);
                let (mut n_frames, mut seen_ok, mut unalive) = (0u64, 0u64, 0u64);
                let mut te_range = vec![(i64::MAX, i64::MIN); ids.len()];
                let start = START;
                let mut f = 0usize;
                while f < frames {
                    let mut t = start + f as i64 * frame;
                    if jumps && f > 0 && f % 120 == 0 { t += 40 * frame; }
                    u.settle(t);
                    u.now = t;
                    let ctx = u.ctx();
                    let cold = gather(&u, &[]);
                    let warm = gather_cached(&u, &[], &mut cache);
                    let (Some(cold), Some(warm)) = (cold, warm) else { continue };
                    n_frames += 1;
                    if f >= 1 {
                        reads += cache.readouts;
                        worst = worst.max(cache.readouts);
                        let xo = [warm.position_light_seconds[0] / TICK_SECONDS, warm.position_light_seconds[1] / TICK_SECONDS];
                        for &id in &ids {
                            if !u.bodies().alive(id) { unalive += 1; continue; }
                            let c = cold.seen.iter().find(|s| s.id == id);
                            let w = warm.seen.iter().find(|s| s.id == id);
                            match (c, w) {
                                (None, None) => drops += 1,
                                (Some(c), Some(w)) => {
                                    seen_ok += 1;
                                    if c.offset != w.offset || c.light_seconds != w.light_seconds { dis += 1; }
                                }
                                _ => dis += 1,
                            }
                            // The oracle: bisection on g(t)=t+|x(t)-xo|-t_now (monotone: a tube is
                            // timelike), an independent search sharing only the worldline reads.
                            if let Some(w) = w {
                                let te_gather = t as f64 - w.age / TICK_SECONDS;
                                let k = ids.iter().position(|&x| x == id).unwrap();
                                let teg = te_gather.round() as i64;
                                te_range[k].0 = te_range[k].0.min(teg);
                                te_range[k].1 = te_range[k].1.max(teg);
                                match bisect(&ctx, id, t, xo) {
                                    Ok(te_true) => {
                                        let d = te_gather.round() as i64 - te_true;
                                        if d != 0 { mismatch += 1; worst_dte = worst_dte.max(d.abs()); }
                                    }
                                    Err(()) => mismatch += 1,
                                }
                            }
                        }
                    }
                    f += 1;
                }
                let kinked = ids.iter().filter(|&&i| u.bodies().event_time(i) > 0).count();
                // Where each emitter's kinks (rebind ticks) lie against the swept emission ticks.
                let mut in_sweep = 0usize;
                let mut total_kinks = 0usize;
                for (k, &id) in ids.iter().enumerate() {
                    let mut kinks = Vec::new();
                    let end = u.bodies().event_time(id);
                    let ev = |tt: i64| u.bodies().binding_at(id, tt).map(|b| b.event_time).unwrap_or(0);
                    // The next rebind after `e`: the least `t` whose holding binding starts later
                    // than `e` (monotone once past the kink: binary search).
                    let mut e = ev(0);
                    while e < end {
                        let (mut lo, mut hi) = (e + 1, end);
                        while lo < hi {
                            let mid = lo + (hi - lo) / 2;
                            if ev(mid) > e { hi = mid } else { lo = mid + 1 }
                        }
                        if lo >= end || ev(lo) <= e { break; }
                        e = ev(lo);
                        kinks.push(e);
                    }
                    // The current binding's own start (when it is not the original) is a rebind too.
                    if end > 0 && ev(end - 1) < end {
                        kinks.push(end);
                    }
                    if kinks.is_empty() && end > 0 {
                        let r = u.rec(id);
                        eprintln!("dbg em {id}: end={end} events={} refusals={} alive={} ev(end/2)={} ev(end-1)={}", r.events, r.refusals, u.bodies().alive(id), u.bodies().binding_at(id, end / 2).map(|b| b.event_time).unwrap_or(-1), u.bodies().binding_at(id, end - 1).map(|b| b.event_time).unwrap_or(-1));
                    }
                    total_kinks += kinks.len();
                    if te_range[k].0 <= te_range[k].1 {
                        in_sweep += kinks.iter().filter(|&&kt| kt >= te_range[k].0 && kt <= te_range[k].1).count();
                    }
                }
                println!("{:<26} {:>8.2} {:>7} {:>6} {:>6} {:>7} {:>6}   [engine: kicks={} refused={} lost={}; kinked emitters {kinked}/12; unalive-frame-counts {unalive}; kinks {total_kinks} total, {in_sweep} inside the swept emission range]",
                    name,
                    reads as f64 / n_frames.max(1) as f64 / 12.0,
                    worst, drops, dis, mismatch, worst_dte,
                    u.stats.kicks, u.stats.refused, u.stats.lost);
            }
        }
        _ => {
            println!("settle to {t_fly} (the flyby) ...");
            u.settle(t_fly + 100_000);
            println!("stats: kicks={} opens={} boundaries={} refused={} lost={}", u.stats.kicks, u.stats.opens, u.stats.boundaries, u.stats.refused, u.stats.lost);
            for &id in ids.iter().take(4) {
                println!("emitter {id}: alive={} event_time={} (kinked: {})", u.bodies().alive(id), u.bodies().event_time(id), u.bodies().event_time(id) > 0);
            }
            println!("player event_time={} alive={}", u.bodies().event_time(player), u.bodies().alive(player));
            for &id in ids.iter().take(3) {
                println!("emitter {id}: next item at {:?} step={} interval={}", u.bodies().next_time(id), u.rec(id).step, u.rec(id).interval);
            }
            println!("source event_time={} (a pure tube: {})", u.bodies().event_time(src), u.bodies().event_time(src) == 0);
        }
    }
}

/// The crossing tick by bisection: the last integer `t` with `g(t) <= 0`, `g` monotone (a tube is
/// timelike). An independent search: no slope, no memo, no convexity argument — only the same
/// worldline reads the gather sees. `Err` when the worldline does not read.
fn bisect(ctx: &emergent_universe::ctx::Ctx, id: usize, t_now: i64, xo: [f64; 2]) -> Result<i64, ()> {
    let g = |t: i64| -> Option<f64> {
        let st = state_rate(ctx, id, t).ok()?;
        Some((t - t_now) as f64 + ((st.0[0] - xo[0]) * (st.0[0] - xo[0]) + (st.0[1] - xo[1]) * (st.0[1] - xo[1])).sqrt())
    };
    let (mut lo, mut hi) = (0i64, t_now);
    if g(0).ok_or(())? > 0.0 {
        return Ok(0); // before the first light: the gather shows the state at tick 0
    }
    match g(hi) {
        Some(v) if v <= 0.0 => return Ok(hi), // co-located now: the crossing is the present
        Some(_) => {}
        None => return Err(()),
    }
    while hi - lo > 1 {
        let mid = lo + (hi - lo) / 2;
        match g(mid) {
            Some(v) if v <= 0.0 => lo = mid,
            Some(_) => hi = mid,
            None => return Err(()),
        }
    }
    Ok(lo)
}
