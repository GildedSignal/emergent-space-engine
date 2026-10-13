//! The acceleration-word census: is the second-order term the shipped readout re-derives per
//! read (`observe::partial`, one `force::field` at the window's mid) the SAME quantity the kick
//! already computes and discards (`step.rs:669`, `f.accel`), and how stale is one stored word
//! across each consumer's window?
//!
//! Per frame, per body whose binding the shipped readout would complete with a partial step
//! (a clock kick, 0 < τ ≤ 2·len — `partial`'s own gate), it samples:
//!   term = |a(mid)|·τ²/2          the per-read term the shipped readout pays to compute;
//!   err  = |a(mid) − a(B)|·τ²/2   the error if the term came from a word stored at the
//!                                 window's synchronised boundary B (where the tube read is
//!                                 exact, and the engine's own machinery runs);
//!   Δa/a, and Δa across the light window to the dominant secondary (the news consumer's T).
//! All in the body's own doll units (c = 1), f64 for measurement only.
//!
//! cargo run --release -p emergent-universe --example a_word [-- <flight: coast|fwd|rev>]
use emergent_universe::force;
use emergent_universe::num::{time_of, to_f64};
use emergent_universe::scenario::plane;
use emergent_universe::{Budget, Config};
use std::time::Instant;

fn main() {
    let which = std::env::args().nth(1).unwrap_or_default();
    let flights: Vec<(&str, u8, u8)> = vec![
        ("coast", 0, 0),
        ("fwd", 1, 8),   // held forward burn, level 8 (the waterfall scene, 174d)
        ("rev", 2, 15),  // held reverse burn, level 15 (the dive approach, 174d checker2)
    ];
    for (name, keys, level) in flights {
        if !which.is_empty() && name != which { continue; }
        let mut p = plane(Config::default(), 1, emergent_universe::fleet::Order::Sparse, 1, 48).unwrap();
        let mut t0 = Instant::now();
        let mut reads: Vec<(usize, String, f64, f64, f64, f64, f64, f64)> = Vec::new(); // (i, name, tau, term, err, da_rel, |a|, r)
        let mut light_rel: Vec<f64> = Vec::new();
        let frames = 480usize; // 8 s at 60 Hz
        for f in 0..frames {
            if level > 0 && f == 60 {
                let _ = p.u.input(p.u.now, emergent_universe::thrust::word(keys, level));
            }
            let frame = p.u.frame_to(1.0 / 60.0, 100.0, Budget::unlimited(), i64::MAX);
            let t = frame.presented;
            let ctx = p.u.ctx();
            for i in 0..ctx.info.len() {
                let rec = p.u.rec(i);
                if !rec.alive { continue; }
                let b = rec.b;
                let k = b.kick;
                if !k.clock { continue; }
                let (start, doll) = if t >= k.boundary {
                    (k.boundary, b.doll)
                } else {
                    if k.lead <= 0 { continue; }
                    match ctx.bodies.binding_at(i, b.event_time - 1) {
                        Some(prev) => (b.event_time - k.lead, prev.doll),
                        None => continue,
                    }
                };
                let tau = t - start;
                if tau <= 0 || tau > 2 * k.len.max(1) { continue; }
                let mid = start + tau / 2;
                let base = if t >= k.boundary { b } else { ctx.bodies.binding_at(i, b.event_time - 1).unwrap() };
                let a_at = |tick| -> Option<(f64, f64, f64, f64)> {
                    let (x, v) = base.cartesian(tick).ok()?;
                    let secs = ctx.secondaries(base.doll, tick, i).ok()?;
                    let f = force::field(&secs, x).ok()?;
                    Some((to_f64(f.accel[0]), to_f64(f.accel[1]), (to_f64(x[0]).powi(2) + to_f64(x[1]).powi(2)).sqrt(), (to_f64(v[0]).powi(2) + to_f64(v[1]).powi(2)).sqrt()))
                };
                let Some((amx, amy, _, _)) = a_at(mid) else { continue };
                let Some((abx, aby, r, beta)) = a_at(start) else { continue };
                let tau_s = match time_of(tau, base.clock_exp) { Ok(v) => to_f64(v), Err(_) => continue };
                let ts2 = tau_s * tau_s / 2.0;
                let term = (amx.powi(2) + amy.powi(2)).sqrt() * ts2;
                let err = ((amx - abx).powi(2) + (amy - aby).powi(2)).sqrt() * ts2;
                let a_mag = (abx.powi(2) + aby.powi(2)).sqrt();
                let da_rel = if a_mag > 0.0 { ((amx - abx).powi(2) + (amy - aby).powi(2)).sqrt() / a_mag } else { 0.0 };
                let name = p.names.get(i).cloned().unwrap_or_else(|| format!("body {i}"));
                reads.push((i, name, tau as f64, term, err, da_rel, a_mag, r));
                let _ = beta;
                // the light window to the dominant secondary: the news consumer's T (weak-field plane bound)
                if let Some((ax, ay, _, _)) = a_at(start) {
                    let Ok(secs) = ctx.secondaries(base.doll, start, i) else { continue };
                    let Ok((x, _)) = base.cartesian(start) else { continue };
                    let mut best: Option<(f64, f64)> = None; // (pull, r)
                    for s in &secs {
                        let (dx, dy) = (to_f64(s.pos[0]) - to_f64(x[0]), to_f64(s.pos[1]) - to_f64(x[1]));
                        let rr = (dx.powi(2) + dy.powi(2)).sqrt();
                        let gm = to_f64(s.gm);
                        if gm > 0.0 {
                            let pull = gm / rr / rr;
                            if best.map(|(p0, _)| pull > p0).unwrap_or(true) { best = Some((pull, rr)); }
                        }
                    }
                    if let Some((_, t_light)) = best {
                        if let Some((ax2, ay2, _, _)) = a_at(start + (t_light as i64).max(1)) {
                            let m = (ax.powi(2) + ay.powi(2)).sqrt();
                            if m > 0.0 {
                                light_rel.push((((ax2 - ax).powi(2) + (ay2 - ay).powi(2)).sqrt()) / m);
                            }
                        }
                    }
                }
            }
        }
        // report
        let pl = p.player;
        {
            let prec = p.u.rec(pl);
            let doll = prec.b.doll;
            let (r, beta) = prec.b.cartesian(p.u.now.max(prec.b.event_time))
                .map(|(x, v)| ((to_f64(x[0]).powi(2) + to_f64(x[1]).powi(2)).sqrt(), (to_f64(v[0]).powi(2) + to_f64(v[1]).powi(2)).sqrt()))
                .unwrap_or((f64::NAN, f64::NAN));
            let mut names: Vec<String> = reads.iter().map(|r| r.1.clone()).collect();
            names.sort(); names.dedup();
            println!("   player end: alive {} refusals {} doll {} r {:.3e} beta {:.3e} | census bodies: {}", prec.alive, prec.refusals, doll, r, beta, names.join(", "));
        }
        let (mut pt, mut pe, mut pd): (Vec<f64>, Vec<f64>, Vec<f64>) = Default::default();
        for r in reads.iter().filter(|r| r.0 == pl) { pt.push(r.3); pe.push(r.4); pd.push(r.5); }
        if !pt.is_empty() {
            pt.sort_by(|a, b| a.partial_cmp(b).unwrap()); pe.sort_by(|a, b| a.partial_cmp(b).unwrap()); pd.sort_by(|a, b| a.partial_cmp(b).unwrap());
            let med = |v: &Vec<f64>| v[(0.5 * (v.len() - 1) as f64) as usize];
            println!("   player-only ({} reads): term med {:.3e} max {:.3e} | err med {:.3e} max {:.3e} | da/a med {:.3e} max {:.3e}", pt.len(), med(&pt), pt[pt.len()-1], med(&pe), pe[pe.len()-1], med(&pd), pd[pd.len()-1]);
        }
        let mut terms: Vec<f64> = reads.iter().map(|r| r.3).collect();
        let mut errs: Vec<f64> = reads.iter().map(|r| r.4).collect();
        let mut das: Vec<f64> = reads.iter().map(|r| r.5).collect();
        terms.sort_by(|a, b| a.partial_cmp(b).unwrap());
        errs.sort_by(|a, b| a.partial_cmp(b).unwrap());
        das.sort_by(|a, b| a.partial_cmp(b).unwrap());
        let q = |v: &Vec<f64>, f: f64| v[((f * (v.len() - 1) as f64) as usize).min(v.len() - 1)];
        let gt1 = das.iter().filter(|d| **d > 1.0).count();
        println!("== flight {name} (keys {keys} L{level}): {} frames, {} census reads, {:.1}s wall ==", frames, reads.len(), t0.elapsed().as_secs_f64());
        if reads.is_empty() { continue; }
        println!("   term (doll units): median {:.3e} p99 {:.3e} max {:.3e}", q(&terms, 0.5), q(&terms, 0.99), terms[terms.len() - 1]);
        println!("   err  (doll units): median {:.3e} p99 {:.3e} max {:.3e}", q(&errs, 0.5), q(&errs, 0.99), errs[errs.len() - 1]);
        println!("   da/a : median {:.3e} p99 {:.3e} max {:.3e}  reads with da/a>1: {} ({:.3}%)", q(&das, 0.5), q(&das, 0.99), das[das.len() - 1], gt1, 100.0 * gt1 as f64 / das.len() as f64);
        if !light_rel.is_empty() {
            let mut l = light_rel.clone();
            l.sort_by(|a, b| a.partial_cmp(b).unwrap());
            println!("   light-window da/a (news T): median {:.3e} max {:.3e}", q(&l, 0.5), l[l.len() - 1]);
        }
        let mut worst = reads.clone();
        worst.sort_by(|a, b| b.4.partial_cmp(&a.4).unwrap());
        println!("   worst 8 reads by err (i, name, tau_ticks, term, err, da/a, |a|, r):");
        for w in worst.iter().take(8) {
            println!("     {:>3} {:<12} tau {:>9} term {:.3e} err {:.3e} da/a {:.2} |a| {:.3e} r {:.3e}", w.0, w.1, w.2 as i64, w.3, w.4, w.5, w.6, w.7);
        }
        let _ = t0; t0 = Instant::now();
    }
}
