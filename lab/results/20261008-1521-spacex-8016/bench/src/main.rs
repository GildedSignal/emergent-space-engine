// The kick's idiot index: where the plane's kick money goes, and what a bit-identical
// deletion (sharing the per-(doll, tick) context) would buy. No crate is edited.
use emergent_space::binding::Rebinding;
use emergent_space::orbit::{Orbit, Scalar};
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

fn main() {
    let a: Vec<String> = std::env::args().skip(1).collect();
    let mode = a.first().map(|s| s.as_str()).unwrap_or("frame");
    let seed: u64 = a.get(1).map(|s| s.parse().unwrap()).unwrap_or(1);
    match mode {
        "frame" => frame(seed),
        "kick" => kick(seed),
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
