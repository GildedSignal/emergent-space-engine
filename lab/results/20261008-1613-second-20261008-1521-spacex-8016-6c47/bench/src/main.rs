// Second author on 20261008-1521-spacex-8016. The checker's named gold experiment:
// wire the re-anchored jet into the plane's rebind and measure a digest-identical
// speedup. This bench runs its cheapest decisive parts without touching a crate:
//   kick/frame  — the prior run's modes, verbatim (the record regenerates).
//   jet <seed>  — on the plane's real fired-kick stream: key recurrence under every
//                 shipped reuse hook (exact ShapeMemo, coarsening QuantizedMemo),
//                 per-kick key drift (the jet's re-anchor cadence), bit divergence
//                 between consecutive compiled orbits (can reuse be bit-identical?),
//                 and the per-use cost of each reuse path against the fresh compile.
//   sweep       — compile cost and knot count across eccentricity and radius extremes.
use emergent_space::binding::Rebinding;
use emergent_space::orbit::{MemoCode, Orbit, OrbitKey, OrbitState, QuantizedMemo, ShapeMemo, Scalar};
use emergent_universe::body::What;
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::{step, Budget, Config, Kind};
use std::collections::HashMap;
use std::time::Instant;

type Acc = HashMap<&'static str, (u64, f64)>;

fn add(m: &mut Acc, name: &'static str, us: f64) {
    let e = m.entry(name).or_insert((0, 0.0));
    e.0 += 1;
    e.1 += us;
}

fn f64_of(s: Scalar) -> f64 {
    s.significand() as f64 * 2f64.powi(s.exponent() as i32 - 62)
}

fn main() {
    let a: Vec<String> = std::env::args().skip(1).collect();
    let mode = a.first().map(|s| s.as_str()).unwrap_or("frame");
    let seed: u64 = a.get(1).map(|s| s.parse().unwrap()).unwrap_or(1);
    match mode {
        "frame" => frame(seed),
        "kick" => kick(seed),
        "jet" => jet(seed),
        "sweep" => sweep(),
        _ => unreachable!(),
    }
}

fn pct(v: &mut Vec<f64>, q: f64) -> f64 {
    v.sort_by(|a, b| a.total_cmp(b));
    v[((q * v.len() as f64) as usize).min(v.len() - 1)]
}

/// Player-like run: per-frame advance with an unlimited budget; the per-kind cost split.
fn frame(seed: u64) {
    let mut p = plane(Config::default(), seed, Order::Sparse, 1, 48).unwrap();
    let frames = 600usize;
    let rtf = 100.0f64; // the way Julien flies it
    let t0 = Instant::now();
    let mut frame_us: Vec<f64> = Vec::new();
    for _ in 0..frames {
        let fr = Instant::now();
        p.u.frame(1.0 / 60.0, rtf, Budget::unlimited());
        frame_us.push(fr.elapsed().as_secs_f64() * 1e6);
    }
    let wall = t0.elapsed().as_secs_f64();
    let s = &p.u.stats;
    let names = ["planet", "moon", "ship", "player", "fleet"];
    let total_ns: u64 = s.cost_ns.iter().sum();
    let p95 = pct(&mut frame_us, 0.95);
    let p50 = frame_us[frame_us.len() / 2];
    let mx = frame_us.iter().cloned().fold(0.0f64, f64::max);
    println!("seed {seed} rtf {rtf} wall {wall:.2}s frames {frames} (p50 {p50:.0}us p95 {p95:.0}us max {mx:.0}us) contacts {}",
        p.u.contacts);
    for k in 0..5 {
        println!("  {:>7}: {:>7} items {:>9.3}s {:>6.2}% of event cost, {:>6.2} us/item",
            names[k], s.items[k], s.cost_ns[k] as f64 / 1e9, 100.0 * s.cost_ns[k] as f64 / total_ns as f64,
            s.cost_ns[k] as f64 / 1e3 / s.items[k].max(1) as f64);
    }
    println!("  event cost total {:.3}s of wall {wall:.2}s ({:.1}% of one core); items {}",
        total_ns as f64 / 1e9, 100.0 * total_ns as f64 / 1e9 / wall, s.items.iter().sum::<u64>());
    println!("  kinds: kicks {} opens {} bounds {} handoffs {} slices {} leavers {} dissolved {} lost {} refused {}",
        s.kicks, s.opens, s.boundaries, s.handoffs, s.slices, s.leavers, s.dissolved, s.lost, s.refused);
    println!("  digest {}", p.u.digest());
}

/// quantize, reimplemented exactly from step.rs (private there), to classify fired vs carried.
fn quantize(dv: [Scalar; 2], exp: i16, carry: [i64; 2]) -> Result<([i64; 2], [i64; 2]), String> {
    let mut out = [0i64; 2];
    let mut rem = carry;
    for c in 0..2 {
        let inc = dv[c].fixed(16 - exp as i32).map_err(|e| format!("{e:?}"))?;
        let total = carry[c] as i128 + inc;
        out[c] = i64::try_from(total / 65536).map_err(|_| "word".to_string())?;
        rem[c] = (total % 65536) as i64;
    }
    Ok((out, rem))
}

/// The kick dissection: distinct ship kicks, fired vs carried, pieces, rebind share, context dedup.
fn kick(seed: u64) {
    let mut p = plane(Config::default(), seed, Order::Sparse, 1, 48).unwrap();
    let mut acc: Acc = HashMap::new();
    let mut last: Vec<Option<i64>> = Vec::new();
    let mut ctx_keys: HashMap<(u16, i64), u64> = HashMap::new();
    let mut dv_quanta: Vec<f64> = Vec::new();
    let mut mismatches = 0u64;
    let mut thrust_kicks = 0u64;
    for _ in 0..900 {
        last.resize(p.u.n_bodies(), None);
        for i in 0..p.u.n_bodies() {
            let rec = p.u.rec(i);
            if rec.kind != Kind::Ship || !rec.alive {
                continue;
            }
            let Some(item) = rec.plan.first().copied() else { continue };
            if !matches!(item.what, What::Kick(_)) || last[i] == Some(item.t) {
                continue;
            }
            last[i] = Some(item.t);
            let t0 = Instant::now();
            let upd = step::process(&p.u.ctx(), i, rec.clone());
            let us = t0.elapsed().as_secs_f64() * 1e6;
            let fired_entry = upd.new_entry.is_some();
            let mut cls: &'static str = "ext";
            if rec.ext.is_none() {
                if let What::Kick(level) = item.what {
                    cls = "entry-only";
                    let ctx = p.u.ctx();
                    let t = item.t;
                    let t0 = Instant::now();
                    let st = rec.b.readout(t).unwrap();
                    let t_read = t0.elapsed().as_secs_f64() * 1e6;
                    let (x, _v) = emergent_universe::bind::scalars(&st).unwrap();
                    let d = rec.b.doll;
                    let t0 = Instant::now();
                    let secs = ctx.secondaries(d, t, i).unwrap();
                    let t_secs = t0.elapsed().as_secs_f64() * 1e6;
                    let t0 = Instant::now();
                    let tide = ctx.tide(d, t).unwrap();
                    let t_tide = t0.elapsed().as_secs_f64() * 1e6;
                    let a = emergent_universe::force::acceleration(level, x, &secs, tide).unwrap();
                    let h = emergent_universe::num::time_of(rec.interval >> (2 * level as i64), rec.b.clock_exp).unwrap();
                    let dv = emergent_universe::num::scale2(a, h).unwrap();
                    let (dvq, _c2) = quantize(dv, st.velocity_exponent, rec.carry).unwrap();
                    let fired = dvq != [0, 0];
                    cls = match (fired, fired_entry) {
                        (true, true) => "fired",
                        (false, false) => "carried",
                        _ => { mismatches += 1; "mismatch" }
                    };
                    add(&mut acc, "piece readout", t_read);
                    add(&mut acc, "piece secondaries", t_secs);
                    add(&mut acc, "piece tide", t_tide);
                    *ctx_keys.entry((d, item.t)).or_insert(0) += 1;
                    let q0 = dv[0].fixed(-st.velocity_exponent as i32).unwrap().abs();
                    let q1 = dv[1].fixed(-st.velocity_exponent as i32).unwrap().abs();
                    dv_quanta.push((q0.max(q1) as f64 + 1.0).log2());
                    if level == 0 && rec.thrust.is_some_and(|th| th.keys != 0) {
                        thrust_kicks += 1;
                    }
                    // The rebind, isolated: the kicked state bound from Cartesian, and the shape compile alone.
                    if fired {
                        let next = emergent_space::binding::IntegerState {
                            velocity: [st.velocity[0] + dvq[0], st.velocity[1] + dvq[1]],
                            ..st
                        };
                        let t0 = Instant::now();
                        if let Ok(_rb) = Rebinding::from_state(next, Scalar::integer(5), None) {
                            add(&mut acc, "rebind from_state", t0.elapsed().as_secs_f64() * 1e6);
                        }
                        if let Some(e) = upd.new_entry.as_ref() {
                            let t0 = Instant::now();
                            if let Ok(_o) = Orbit::compile(e.trajectory.key()) {
                                add(&mut acc, "rebind compile-only", t0.elapsed().as_secs_f64() * 1e6);
                            }
                        }
                    }
                }
            }
            add(&mut acc, cls, us);
        }
        p.u.frame(1.0 / 60.0, 100.0, Budget::unlimited());
        p.u.settle(p.u.now);
    }
    let total: u64 = ["fired", "carried", "ext", "mismatch", "entry-only"].iter().map(|n| acc.get(*n).map(|e| e.0).unwrap_or(0)).sum();
    let sum_us = |ns: &[&str]| ns.iter().map(|n| acc.get(*n).map(|e| e.1).unwrap_or(0.0)).sum::<f64>();
    let proc_us = sum_us(&["fired", "carried", "ext", "mismatch", "entry-only"]);
    println!("seed {seed}: {total} distinct ship kicks ({thrust_kicks} thrusting, {} ext/clock-stepped), entry-heuristic mismatches {mismatches}",
        acc.get("ext").map(|e| e.0).unwrap_or(0));
    for n in ["fired", "carried", "ext", "mismatch", "entry-only"] {
        if let Some((c, us)) = acc.get(n) {
            println!("  {:>10}: {:>6} kicks, {:>7.2} us/kick, {:>6.2}% of kick time", n, c, us / *c as f64, 100.0 * us / proc_us);
        }
    }
    for n in ["piece readout", "piece secondaries", "piece tide", "rebind from_state", "rebind compile-only"] {
        if let Some((c, us)) = acc.get(n) {
            println!("  {:>20}: {:>7.2} us/call over {c} calls ({:>6.2}% of process time)", n, us / *c as f64, 100.0 * us / proc_us);
        }
    }
    let ctx_us = sum_us(&["piece secondaries", "piece tide"]);
    println!("  shareable context (secondaries+tide): {:.2} us/kick = {:.1}% of kick time", ctx_us / total as f64, 100.0 * ctx_us / proc_us);
    let distinct = ctx_keys.len() as u64;
    let covered: u64 = ctx_keys.values().sum();
    if distinct > 0 {
        let mut hist: Vec<u64> = ctx_keys.values().copied().collect();
        hist.sort_unstable();
        hist.reverse();
        println!("  context dedup: {covered} kicks over {distinct} distinct (doll,tick): {:.1} kicks/context; top {:?}",
            covered as f64 / distinct as f64, &hist[..hist.len().min(8)]);
    }
    dv_quanta.sort_by(|a, b| a.total_cmp(b));
    if !dv_quanta.is_empty() {
        println!("  |dv| in velocity quanta (log2): p50 {:.1} p05 {:.1} p95 {:.1} (<=0 is sub-quantum)",
            dv_quanta[dv_quanta.len() / 2],
            dv_quanta[(0.05 * dv_quanta.len() as f64) as usize],
            dv_quanta[(0.95 * dv_quanta.len() as f64) as usize]);
    }
    println!("  digest {}", p.u.digest());
}

/// Bitwise comparison of two orbit states at identical arguments.
fn states_equal(a: &OrbitState, b: &OrbitState) -> bool {
    a.radius == b.radius && a.radial_angle == b.radial_angle && a.advance == b.advance
        && a.proper_time == b.proper_time && a.radial_velocity == b.radial_velocity
        && a.transverse_velocity == b.transverse_velocity && a.cycles == b.cycles
        && a.outbound == b.outbound && a.psi == b.psi
}

/// The decisive mode: on the plane's real fired-kick stream, can any reuse of a
/// compiled cycle across kicks be bit-identical, what would the jet re-anchor on,
/// and what does each shipped reuse path cost per use?
fn jet(seed: u64) {
    let mut p = plane(Config::default(), seed, Order::Sparse, 1, 48).unwrap();
    let mut acc: Acc = HashMap::new();
    let mut last_t: Vec<Option<i64>> = Vec::new();
    let mut last_key: Vec<Option<OrbitKey>> = Vec::new();
    let mut last_orbit: Vec<Option<Orbit>> = Vec::new();
    // Reuse accounting, end-to-end over every fired kick's exact key.
    let mut shape_memo = ShapeMemo::default();
    let mut quant_memo = QuantizedMemo::with_capacity(256);
    let mut shape_feed_hits = 0u64;
    let mut quant_feed_hits = 0u64;
    let mut code_global: HashMap<u64, u64> = HashMap::new();
    // Pair statistics between a body's consecutive fired kicks.
    let mut pairs = 0u64;
    let mut exact_rep = 0u64;
    let mut shape_rep = 0u64;
    let mut code_rep = 0u64;
    let mut weak_shapes = 0u64;
    let mut reads_equal = 0u64;
    let mut incr_equal = 0u64;
    let mut drift: Vec<f64> = Vec::new();
    let mut incr_rel: Vec<f64> = Vec::new();
    // Re-anchor cadence on the real stream: reset when |accumulated signed drift|
    // crosses sqrt(floor/C), floor = 1e-6, C = 1.9 (red-team 20261006-0346).
    let thresh = (1e-6f64 / 1.9).sqrt();
    let (mut acc_k, mut acc_p, mut anchors) = (0.0f64, 0.0f64, 0u64);
    let mut fired = 0u64;
    let mut carried = 0u64;
    let mut mismatches = 0u64;
    let mut player_items = 0u64;
    let mut player_fired = 0u64;
    for _ in 0..900 {
        let n = p.u.n_bodies();
        last_t.resize(n, None);
        last_key.resize_with(n, || None);
        last_orbit.resize_with(n, || None);
        for i in 0..n {
            let rec = p.u.rec(i);
            if !matches!(rec.kind, Kind::Ship | Kind::Player) || !rec.alive {
                continue;
            }
            let Some(item) = rec.plan.first().copied() else { continue };
            if !matches!(item.what, What::Kick(_)) || last_t[i] == Some(item.t) {
                continue;
            }
            last_t[i] = Some(item.t);
            let t0 = Instant::now();
            let upd = step::process(&p.u.ctx(), i, rec.clone());
            let us = t0.elapsed().as_secs_f64() * 1e6;
            let fired_entry = upd.new_entry.is_some();
            if rec.kind == Kind::Player {
                player_items += 1;
            }
            if rec.ext.is_some() {
                add(&mut acc, "ext", us);
                continue;
            }
            let What::Kick(level) = item.what else { continue };
            let ctx = p.u.ctx();
            let st = rec.b.readout(item.t).unwrap();
            // A player's kick also rides its burn, so the tide-only classifier does not
            // apply: the universe's own new_entry is the fired decision there.
            let mut dvq = [0i64; 2];
            let is_fired = if rec.kind == Kind::Player {
                fired_entry
            } else {
                let (x, _v) = emergent_universe::bind::scalars(&st).unwrap();
                let d = rec.b.doll;
                let secs = ctx.secondaries(d, item.t, i).unwrap();
                let tide = ctx.tide(d, item.t).unwrap();
                let a = emergent_universe::force::acceleration(level, x, &secs, tide).unwrap();
                let h = emergent_universe::num::time_of(rec.interval >> (2 * level as i64), rec.b.clock_exp).unwrap();
                let dv = emergent_universe::num::scale2(a, h).unwrap();
                let (q, _c2) = quantize(dv, st.velocity_exponent, rec.carry).unwrap();
                dvq = q;
                q != [0, 0]
            };
            match (is_fired, fired_entry) {
                (true, true) => fired += 1,
                (false, false) => carried += 1,
                _ => mismatches += 1,
            }
            if !is_fired {
                add(&mut acc, "carried", us);
                continue;
            }
            add(&mut acc, if rec.kind == Kind::Ship { "fired" } else { "fired-player" }, us);
            if rec.kind == Kind::Player {
                player_fired += 1;
            }
            let Some(e) = upd.new_entry.as_ref() else { continue };
            let key = e.trajectory.key();
            // --- recurrence under every reuse identity -------------------------------
            if let Ok(sk) = emergent_space::orbit::ShapeKey::for_orbit(key) {
                if sk.compactness.is_zero() {
                    weak_shapes += 1;
                }
            }
            let sh0 = shape_memo.hits;
            let _ = shape_memo.get(key);
            shape_feed_hits += shape_memo.hits - sh0;
            let q0h = quant_memo.hits;
            let _ = quant_memo.get(key);
            quant_feed_hits += quant_memo.hits - q0h;
            if let Ok(code) = MemoCode::encode(key) {
                *code_global.entry(code.bits()).or_insert(0) += 1;
            }
            let t0 = Instant::now();
            let _ = shape_memo.get(key); // guaranteed hit now (or the same refusal)
            add(&mut acc, "reuse shape-hit", t0.elapsed().as_secs_f64() * 1e6);
            let t0 = Instant::now();
            let _ = quant_memo.get(key); // guaranteed hit now (or the same refusal)
            add(&mut acc, "reuse quant-hit", t0.elapsed().as_secs_f64() * 1e6);
            let t0 = Instant::now();
            if let Ok(_o) = Orbit::compile(key) {
                add(&mut acc, "rebind compile-only", t0.elapsed().as_secs_f64() * 1e6);
            }
            // The rebind in isolation, as the plane does it (the plane's ships never
            // thrust in these runs: the tide kick is the whole velocity change).
            if rec.kind == Kind::Ship {
                let next = emergent_space::binding::IntegerState {
                    velocity: [st.velocity[0] + dvq[0], st.velocity[1] + dvq[1]],
                    ..st
                };
                let t0 = Instant::now();
                if let Ok(_rb) = Rebinding::from_state(next, Scalar::integer(5), None) {
                    add(&mut acc, "rebind from_state", t0.elapsed().as_secs_f64() * 1e6);
                }
            }
            // --- consecutive-kick pairs: drift, recurrence, bit divergence ----------
            if let Some(prev) = last_key[i] {
                pairs += 1;
                if prev == key {
                    exact_rep += 1;
                }
                let sk_now = emergent_space::orbit::ShapeKey::for_orbit(key).ok();
                let sk_prev = emergent_space::orbit::ShapeKey::for_orbit(prev).ok();
                if sk_now.is_some() && sk_now == sk_prev {
                    shape_rep += 1;
                }
                if let (Ok(c1), Ok(c2)) = (MemoCode::encode(prev), MemoCode::encode(key)) {
                    if c1 == c2 {
                        code_rep += 1;
                    }
                }
                let dk = ((key.k as f64) / (prev.k as f64)).ln();
                let dp = (f64_of(key.periapsis) / f64_of(prev.periapsis)).ln();
                drift.push(dk.abs().max(dp.abs()));
                acc_k += dk;
                acc_p += dp;
                if acc_k.abs().max(acc_p.abs()) > thresh {
                    anchors += 1;
                    acc_k = 0.0;
                    acc_p = 0.0;
                }
                // Would the previous compiled orbit serve this kick bit-identically?
                if let (Some(old), Ok(new)) = (&last_orbit[i], Orbit::compile(key)) {
                    let incr_eq = old.period() == new.period()
                        && old.advance() == new.advance()
                        && old.proper_period() == new.proper_period();
                    if incr_eq {
                        incr_equal += 1;
                    }
                    let t_q = new.period().unwrap().mul(Scalar::raw(1, -2).unwrap()).unwrap();
                    let so = old.at_phase(0, t_q);
                    let sn = new.at_phase(0, t_q);
                    if let (Ok(so), Ok(sn)) = (so, sn) {
                        if states_equal(&so, &sn) {
                            reads_equal += 1;
                        }
                    }
                    let rel = |a: Scalar, b: Scalar| {
                        (f64_of(a) - f64_of(b)).abs() / f64_of(b).abs().max(1e-300)
                    };
                    if let (Ok(po), Ok(pn)) = (old.period(), new.period()) {
                        incr_rel.push(rel(po, pn));
                    }
                }
            }
            last_key[i] = Some(key);
            last_orbit[i] = Orbit::compile(key).ok();
        }
        p.u.frame(1.0 / 60.0, 100.0, Budget::unlimited());
        p.u.settle(p.u.now);
    }
    let proc_us: f64 = ["fired", "fired-player", "carried", "ext"].iter()
        .map(|n| acc.get(*n).map(|e| e.1).unwrap_or(0.0)).sum();
    println!("seed {seed}: fired {fired} (player {player_fired} of {player_items} items), carried {carried}, mismatches {mismatches}");
    for n in ["fired", "fired-player", "carried", "ext", "rebind from_state", "rebind compile-only", "reuse shape-hit", "reuse quant-hit"] {
        if let Some((c, us)) = acc.get(n) {
            println!("  {:>20}: {:>7} calls, {:>8.2} us/call", n, c, us / *c as f64);
        }
    }
    let nf = acc.get("fired").map(|e| e.0).unwrap_or(1) as f64;
    let t_compile = acc.get("rebind compile-only").map(|e| e.1).unwrap_or(0.0) / nf;
    let t_state = acc.get("rebind from_state").map(|e| e.1).unwrap_or(0.0) / nf;
    let t_hit = acc.get("reuse shape-hit").map(|e| e.1).unwrap_or(0.0) / nf;
    println!("  per fired ship kick: from_state {t_state:.1} us, compile {t_compile:.1} us ({:.0}% of from_state), shape-hit reuse {t_hit:.1} us",
        100.0 * t_compile / t_state.max(1e-9));
    println!("  recurrence over {pairs} consecutive-kick pairs: exact key {exact_rep}, exact ShapeKey {shape_rep}, MemoCode {code_rep}; weak-branch shapes {weak_shapes}/{fired}");
    println!("  end-to-end memo feeds (first encounter only): ShapeMemo hits {shape_feed_hits} of {fired}, QuantizedMemo hits {quant_feed_hits} of {fired} (stored {})",
        quant_memo.len());
    let mut code_hist: Vec<u64> = code_global.values().copied().collect();
    code_hist.sort_unstable();
    let collisions: u64 = code_hist.iter().map(|c| c.saturating_sub(1)).sum();
    println!("  MemoCode collisions across all fired kicks: {collisions} extra kicks sharing a code ({} distinct)", code_hist.len());
    if !drift.is_empty() {
        println!("  per-kick key drift |dln|: p50 {:.2e} p95 {:.2e} max {:.2e}; re-anchors at sqrt(floor/C)={thresh:.1e}: {anchors}",
            pct(&mut drift.clone(), 0.5), pct(&mut drift.clone(), 0.95), drift.iter().cloned().fold(0.0f64, f64::max));
        let e50 = pct(&mut drift.clone(), 0.5);
        println!("  implied jet cadence (correlated worst case): n* = sqrt(floor/C)/eps = {:.0} kicks -> {:.3} compiles/kick", thresh / e50.max(1e-12), e50.max(1e-12) / thresh);
    }
    if pairs > 0 {
        println!("  bit identity across a key step: increments equal {incr_equal}/{pairs}, quarter-period state reads equal {reads_equal}/{pairs}");
        if !incr_rel.is_empty() {
            println!("  relative period change between consecutive keys: p50 {:.2e} p95 {:.2e} (vs Scalar ulp 2^-62 = 2.2e-19)",
                pct(&mut incr_rel.clone(), 0.5), pct(&mut incr_rel.clone(), 0.95));
        }
    }
    println!("  digest {}", p.u.digest());
}

/// Compile cost against the eccentricity and radius extremes the plane never visits.
fn sweep() {
    println!("p(M)      e      us/compile  knots  note");
    for log_p in [4i32, 12, 18, 24, 30] {
        for e in [0.0f64, 0.3, 0.5, 0.7, 0.9, 0.99, 0.995] {
            let p = Scalar::power_of_two(log_p as i16);
            let eq = (e * (1u64 << 48) as f64) as u64;
            let Ok(key) = OrbitKey::bound(p, eq) else {
                println!("2^{log_p:<8} {e:<6} refused");
                continue;
            };
            // Warm one compile outside the timed loop, then time fresh compiles.
            let warm = Orbit::compile(key).ok();
            let t0 = Instant::now();
            let n = 30u64;
            let mut ok = 0u64;
            for _ in 0..n {
                if Orbit::compile(key).is_ok() {
                    ok += 1;
                }
            }
            let us = t0.elapsed().as_secs_f64() * 1e6 / n as f64;
            let knots = warm.map(|o| o.shape().knots().len()).unwrap_or(0);
            println!("2^{log_p:<8} {e:<6} {us:>8.1}  {knots:>5}  ({} ok)", ok);
        }
    }
}
