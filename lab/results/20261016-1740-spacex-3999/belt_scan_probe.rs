//! The belt-bin regime of the player's neighbourhood scan, measured on the shipped index
//! (scan-queue's named unmeasured case: the scan's window inside the belt's radial bins, root doll).
//! Print-only: no engine state is changed, no frame is stepped. Builds the plane with the N ladder's
//! population (`plane_with_extra`), then asks the shipped `Radial::candidates` for real bodies'
//! windows: the player's own (Home's doll, the control), the haulers' (root doll, in and out of the
//! belt band), and one belt body's own window (root doll, in the belt: "the player standing in the
//! belt"). For the belt window it prices the two halves the engine splits (`Encounters::capture`
//! here, `Scan::compute` in idle time): the capture walk (alive/born/binding_at/doll/reach) and the
//! answer (one cartesian readout + the exact lattice predicate per candidate), counts true
//! encounters, and measures the certificate slack (miss distance and angular separation, in reach
//! units). A radius sweep maps where the fallback trips. Output: `key=value` lines, `#` sections.
use emergent_lattice::law::hit;
use emergent_space::orbit::Scalar;
use emergent_universe::encounter::ENCOUNTER_LOG2;
use emergent_universe::fleet::Order;
use emergent_universe::num::{sub2, time_of, to_f64};
use emergent_universe::radial::Window;
use emergent_universe::scenario::{ladder_locals, plane_with_extra, AU};
use emergent_universe::{bind::Binding, ctx::Ctx, Config};
use std::time::Instant;

fn norm2(a: [Scalar; 2]) -> f64 {
    to_f64(a[0]).hypot(to_f64(a[1]))
}

fn integers(a: [Scalar; 2], q_exp: i32) -> Result<[i128; 2], emergent_space::Error> {
    Ok([a[0].fixed(-q_exp)?, a[1].fixed(-q_exp)?])
}

fn r1(x: f64) -> f64 {
    (x * 10.0).round() / 10.0
}
fn r3(x: f64) -> f64 {
    (x * 1000.0).round() / 1000.0
}

struct Asked {
    name: String,
    doll: u16,
    r_au: f64,
    h: f64,
    fallback: bool,
    kept: Option<usize>,
    walked: usize,
    pass: usize,
    capture_us: f64,
}

/// One window asked of the shipped index. `None` from `candidates` is the fallback (the caller then
/// walks and reads every body of the universe). The capture walk is timed over exactly the ids the
/// engine would walk, with the same tests `PlayerNeighbourhood::capture` applies, for the scanning
/// body `p` (its radius makes the reach).
fn ask(ctx: &Ctx, doll: u16, name: &str, p: usize, w: &Window, t: i64) -> Asked {
    let verdict = ctx.radial.candidates(doll, w);
    let kept = verdict.as_ref().map(|v| v.len());
    let ids: Vec<usize> = verdict.clone().unwrap_or_else(|| (0..ctx.bodies.len()).collect());
    let t0 = Instant::now();
    let mut pass = 0usize;
    for &j in &ids {
        if j == p || t <= ctx.info[j].born || !ctx.bodies.alive(j) {
            continue;
        }
        let Some(other) = ctx.bodies.binding_at(j, t) else { continue };
        if other.doll != doll {
            continue;
        }
        match ctx.info[p].radius.add(ctx.info[j].radius) {
            Ok(reach) if !reach.is_zero() => pass += 1,
            _ => {}
        }
    }
    let capture_us = t0.elapsed().as_secs_f64() * 1e6;
    Asked { name: name.into(), doll, r_au: w.r / AU as f64, h: w.h, fallback: kept.is_none(), kept, walked: ids.len(), pass, capture_us }
}

fn show(a: &Asked) {
    println!("window.{}: doll={} r_au={} h={:e} fallback={} kept={} walked={} pass={} capture_us={} capture_us_per_walked={}",
        a.name.replace(' ', "_"), a.doll, r3(a.r_au), a.h, a.fallback,
        a.kept.map(|k| k.to_string()).unwrap_or_else(|| "none".into()), a.walked, a.pass,
        r1(a.capture_us), r3(a.capture_us / a.walked.max(1) as f64));
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let extra: usize = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(100_000);
    let seed: u64 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(1);
    let (world, _) = emergent_engine::scenes::battle(48, emergent_universe::fleet::Q, seed, 1 << 15, false);
    let t_build = Instant::now();
    let plane = plane_with_extra(Config::default(), seed, Order::Sparse, 1, world, extra).expect("the plane");
    let build_s = t_build.elapsed().as_secs_f64();
    let u = &plane.u;
    let ctx = u.ctx();
    let n = ctx.bodies.len();
    let player = plane.player;
    let prec = ctx.bodies.rec(player);
    // One tick after birth (at rest every body's event is tick 0; a scan in flight reads t > born).
    let t = ctx.bodies.event_time(player).max(1);
    let (px, pv) = prec.b.cartesian(t).expect("the player's readout");
    let h_p = to_f64(time_of(prec.step.max(2), prec.b.clock_exp).expect("h"));
    println!("extra={} seed={} bodies={} radial_bodies={} scan_t={} build_s={}", extra, seed, n, ctx.radial.bodies, t, r1(build_s));

    // P4a: the player's own window, Home's doll (the flown control).
    let home = Window { r: norm2(px), v: norm2(pv), reach_p: to_f64(ctx.info[player].radius), near_log2: ENCOUNTER_LOG2, h: h_p };
    show(&ask(&ctx, prec.b.doll, "player_home", player, &home, t));

    // P4b: the haulers' windows, root doll (0.5–8 AU: in and out of the belt band).
    for (k, &j) in plane.ships.iter().take(12).enumerate() {
        let r = ctx.bodies.rec(j);
        let (x, v) = r.b.cartesian(t).expect("hauler");
        let h = to_f64(time_of(r.step.max(2), r.b.clock_exp).expect("h"));
        let w = Window { r: norm2(x), v: norm2(v), reach_p: to_f64(ctx.info[j].radius), near_log2: ENCOUNTER_LOG2, h };
        show(&ask(&ctx, r.b.doll, &format!("hauler_{k}"), j, &w, t));
    }

    // The belt stand-in: the ladder's belt body nearest 2.5 AU (the first `ladder_locals(extra)`
    // ladder ships are locals about Home and the Moon; the rest are the belt, root doll). With no
    // belt, the hauler nearest 2.5 AU stands in (same band, empty bins).
    let locals = ladder_locals(extra as u64) as usize;
    let belt_ids: Vec<usize> = plane.ships.iter().skip(12 + locals).copied().collect();
    let pool: Vec<usize> = if belt_ids.is_empty() { plane.ships.iter().take(12).copied().collect() } else { belt_ids };
    let mut standin = pool[0];
    let mut best = f64::MAX;
    for &j in &pool {
        let Ok((x, _)) = ctx.bodies.rec(j).b.cartesian(t) else { continue };
        let d = (norm2(x) / AU as f64 - 2.5).abs();
        if d < best {
            best = d;
            standin = j;
        }
    }
    let srec = ctx.bodies.rec(standin);
    let (sx, sv) = srec.b.cartesian(t).expect("the stand-in's readout");
    let h_s = time_of(srec.step.max(2), srec.b.clock_exp).expect("h");
    let (r_s, v_s) = (norm2(sx), norm2(sv));
    let belt = Window { r: r_s, v: v_s, reach_p: to_f64(ctx.info[standin].radius), near_log2: ENCOUNTER_LOG2, h: to_f64(h_s) };
    let belt_asked = ask(&ctx, srec.b.doll, "belt_standin_root", standin, &belt, t);
    show(&belt_asked);

    // C-: the same window with h → ∞ must fall back (the negative control: the rule fires when it should).
    let inf = Window { r: r_s, v: v_s, reach_p: to_f64(ctx.info[standin].radius), near_log2: ENCOUNTER_LOG2, h: 1e9 };
    show(&ask(&ctx, srec.b.doll, "huge_h_root", standin, &inf, t));

    // Where does the fallback trip? The stand-in's window swept over radius (v, h, reach held).
    println!("# fallback sweep (the stand-in's v, h and reach, r swept)");
    for k in 0..=14 {
        let r = (1.0 + 0.25 * k as f64) * AU as f64;
        let w = Window { r, v: v_s, reach_p: to_f64(ctx.info[standin].radius), near_log2: ENCOUNTER_LOG2, h: to_f64(h_s) };
        let a = ask(&ctx, srec.b.doll, &format!("sweep_{k}"), standin, &w, t);
        println!("sweep: r_au={} fallback={} kept={}", r3(a.r_au), a.fallback, a.kept.map(|k| k.to_string()).unwrap_or_else(|| "none".into()));
    }

    // The answer half on the belt window's candidates: `Scan::compute`'s loop, timed (on fallback
    // the engine reads every body: the ids are all of them, the candidate list is the doll's).
    let ids: Vec<usize> = ctx.radial.candidates(srec.b.doll, &belt).unwrap_or_else(|| (0..n).collect());
    let mut cands: Vec<(usize, Binding, Scalar)> = Vec::new();
    for &j in &ids {
        if j == standin || t <= ctx.info[j].born || !ctx.bodies.alive(j) {
            continue;
        }
        let Some(other) = ctx.bodies.binding_at(j, t) else { continue };
        if other.doll != srec.b.doll {
            continue;
        }
        let Ok(reach) = ctx.info[standin].radius.add(ctx.info[j].radius) else { continue };
        if reach.is_zero() {
            continue;
        }
        cands.push((j, other, reach));
    }
    let t0 = Instant::now();
    let mut encounters = 0usize;
    let mut misses: Vec<f64> = Vec::new();
    let mut arcs: Vec<f64> = Vec::new();
    let hf = to_f64(h_s);
    let (sxf, syf) = (to_f64(sx[0]), to_f64(sx[1]));
    let (svxf, svyf) = (to_f64(sv[0]), to_f64(sv[1]));
    let lam_s = syf.atan2(sxf);
    for (_j, other, reach) in &cands {
        let (xj, vj) = match other.cartesian(t) {
            Ok(v) => v,
            Err(_) => continue,
        };
        let w = match (|| -> Result<_, emergent_space::Error> {
            Ok([vj[0].sub(sv[0])?.mul(h_s)?, vj[1].sub(sv[1])?.mul(h_s)?])
        })() {
            Ok(w) => w,
            Err(_) => continue,
        };
        let d = match sub2(xj, sx) {
            Ok(d) => d,
            Err(_) => continue,
        };
        let q_exp = reach.exponent() as i32 - 20;
        let (di, wi) = match (integers(d, q_exp), integers(w, q_exp)) {
            (Ok(a), Ok(b)) => (a, b),
            _ => continue,
        };
        let near = match reach.scale(ENCOUNTER_LOG2).and_then(|n| n.fixed(-q_exp)) {
            Ok(n) => n,
            Err(_) => continue,
        };
        if hit(di, wi, near) {
            encounters += 1;
        }
        // Float replica of the predicate's linear model, for the slack metrics only.
        let (dx, dy) = (to_f64(xj[0]) - sxf, to_f64(xj[1]) - syf);
        let (wx, wy) = ((to_f64(vj[0]) - svxf) * hf, (to_f64(vj[1]) - svyf) * hf);
        let s_star = (-(dx * wx + dy * wy) / (wx * wx + wy * wy)).clamp(0.0, 1.0);
        misses.push((dx + s_star * wx).hypot(dy + s_star * wy) / to_f64(*reach));
        let (xjf, yjf) = (to_f64(xj[0]), to_f64(xj[1]));
        let rj = xjf.hypot(yjf);
        let mut ang = (yjf.atan2(xjf) - lam_s).rem_euclid(std::f64::consts::TAU);
        ang = ang.min(std::f64::consts::TAU - ang);
        arcs.push(ang * rj / to_f64(*reach));
    }
    let answer_us = t0.elapsed().as_secs_f64() * 1e6;
    misses.sort_by(|a, b| a.total_cmp(b));
    arcs.sort_by(|a, b| a.total_cmp(b));
    let at = |v: &Vec<f64>, f: f64| v.get(((v.len() as f64 * f) as usize).min(v.len().saturating_sub(1))).copied().unwrap_or(f64::NAN);
    println!("# belt answer half (Scan::compute's loop, timed)");
    println!("belt_answer: candidates={} encounters={} answer_us={} answer_us_per_read={} reads_per_hit={} miss_over_reach_min={} miss_over_reach_p50={} arc_over_reach_min={} arc_over_reach_p50={} standin_r_au={} standin_step={}",
        cands.len(), encounters, r1(answer_us), r3(answer_us / cands.len().max(1) as f64),
        if encounters > 0 { r1(cands.len() as f64 / encounters as f64).to_string() } else { "inf".into() },
        r3(at(&misses, 0.0)), (at(&misses, 0.5) * 10.0).round() / 10.0,
        r3(at(&arcs, 0.0)), (at(&arcs, 0.5) * 10.0).round() / 10.0,
        r3(r_s / AU as f64), srec.step);
    println!("# latch arithmetic (b = 5 ms, drain bar S >= b/2 = 2.5 ms)");
    let per_read = answer_us / cands.len().max(1) as f64;
    println!("latch: S_answer_us={} S_capture_us={} bar_us=2500 latch_answer={} latch_capture={}",
        r1(belt_asked.pass as f64 * per_read), r1(belt_asked.capture_us),
        belt_asked.pass as f64 * per_read >= 2500.0, belt_asked.capture_us >= 2500.0);
}
