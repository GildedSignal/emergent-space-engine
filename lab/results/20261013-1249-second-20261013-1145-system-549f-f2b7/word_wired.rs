//! The wired a-word vs the shipped per-read field evaluation, on the same reads the shipped readout
//! completes (lab run 20261013-1249, the checker's named experiment for 20261013-1145-system-549f).
//!
//! Runs the census's three flights (coast, held forward L8, held reverse L15). Per gated read it
//! computes, by hand, the SHIPPED partial step (the tube decode at the mid, the secondaries' field
//! there, `Δv = a·τ`, `Δx = a·τ²/2`) and takes the READ the tree actually serves through
//! `observe::ramped_in`. On the shipped tree the two agree bit for bit (the control); on the wired
//! tree (`work/patch.diff`: the kick stores its `f.accel` as one word, `partial` reads it) their
//! difference is the wired word's true error — the word is `a(B − len/2)`, half a window staler
//! than the census's `a(B)`.
//!
//! Also censuses the multiplicity the prior run left unpriced: reads per window per body (how many
//! consumers share one stored word between a body's kicks), and prints the digest per flight (the
//! law must not move: identical across trees).
//!
//! cargo run --release -p emergent-universe --example word_wired [-- <flight>]
use emergent_universe::force;
use emergent_universe::num::{add2, scale2, time_of, to_f64};
use emergent_universe::observe::ramped_in;
use emergent_universe::scenario::plane;
use emergent_universe::{Budget, Config};
use std::collections::HashMap;
use std::time::Instant;

fn main() {
    let which = std::env::args().nth(1).unwrap_or_default();
    let flights: Vec<(&str, u8, u8)> = vec![
        ("coast", 0, 0),
        ("fwd", 1, 8),
        ("rev", 2, 15),
    ];
    for (name, keys, level) in flights {
        if !which.is_empty() && name != which { continue; }
        let mut p = plane(Config::default(), 1, emergent_universe::fleet::Order::Sparse, 1, 48).unwrap();
        let t0 = Instant::now();
        // per read: (tau_ticks, term, wired_pos_err, wired_dv_err)
        let mut reads: Vec<(f64, f64, f64, f64)> = Vec::new();
        let mut windows: HashMap<(usize, i64), u32> = HashMap::new(); // (body, window start) -> reads
        let frames = 480usize;
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
                let (base, start) = if t >= k.boundary {
                    (b.clone(), k.boundary)
                } else {
                    if k.lead <= 0 { continue; }
                    match ctx.bodies.binding_at(i, b.event_time - 1) {
                        Some(prev) => (prev, b.event_time - k.lead),
                        None => continue,
                    }
                };
                let tau = t - start;
                if tau <= 0 || tau > 2 * k.len.max(1) { continue; }
                // the shipped partial step, by hand
                let mid = start + tau / 2;
                let Ok((x_mid, _)) = base.cartesian(mid) else { continue };
                let Ok(secs) = ctx.secondaries(base.doll, mid, i) else { continue };
                let Ok(field) = force::field(&secs, x_mid) else { continue };
                let Ok(tau_s) = time_of(tau, base.clock_exp) else { continue };
                let Ok(dv) = scale2(field.accel, tau_s) else { continue };
                let Ok(dx) = scale2(dv, tau_s.scale(-1).unwrap()) else { continue };
                let Ok((px, pv)) = base.cartesian(t) else { continue };
                let Ok(sp) = add2(px, dx) else { continue };
                let Ok(sv) = add2(pv, dv) else { continue };
                // the read the tree serves (wired tree: from the stored word)
                let Ok((wp, wv)) = ramped_in(&ctx, i, t, &b) else { continue };
                let ts2 = to_f64(tau_s) * to_f64(tau_s) / 2.0;
                let am = to_f64(field.accel[0]).powi(2) + to_f64(field.accel[1]).powi(2);
                let term = am.sqrt() * ts2;
                let pe = ((to_f64(wp[0]) - to_f64(sp[0])).powi(2) + (to_f64(wp[1]) - to_f64(sp[1])).powi(2)).sqrt();
                let ve = ((to_f64(wv[0]) - to_f64(sv[0])).powi(2) + (to_f64(wv[1]) - to_f64(sv[1])).powi(2)).sqrt();
                let _ = &sv;
                reads.push((tau as f64, term, pe, ve));
                *windows.entry((i, start)).or_insert(0) += 1;
            }
        }
        let digest = p.u.digest();
        let pl = p.player;
        let _ = pl;
        let mut terms: Vec<f64> = reads.iter().map(|r| r.1).collect();
        let mut perrs: Vec<f64> = reads.iter().map(|r| r.2).collect();
        let mut verrs: Vec<f64> = reads.iter().map(|r| r.3).collect();
        terms.sort_by(|a, b| a.partial_cmp(b).unwrap());
        perrs.sort_by(|a, b| a.partial_cmp(b).unwrap());
        verrs.sort_by(|a, b| a.partial_cmp(b).unwrap());
        let q = |v: &Vec<f64>, f: f64| v[((f * (v.len() - 1) as f64) as usize).min(v.len() - 1)];
        let per_window: Vec<u32> = windows.values().copied().collect();
        let mut pw = per_window.clone();
        pw.sort();
        println!("== flight {name} (keys {keys} L{level}): {} frames, {} reads, {} windows, {:.1}s ==", frames, reads.len(), windows.len(), t0.elapsed().as_secs_f64());
        if reads.is_empty() { println!("digest {digest}"); continue; }
        println!("   term      (doll units): median {:.3e} p99 {:.3e} max {:.3e}", q(&terms, 0.5), q(&terms, 0.99), terms[terms.len() - 1]);
        println!("   wired err (doll units): median {:.3e} p99 {:.3e} max {:.3e}", q(&perrs, 0.5), q(&perrs, 0.99), perrs[perrs.len() - 1]);
        println!("   wired dv-err           : median {:.3e} p99 {:.3e} max {:.3e}", q(&verrs, 0.5), q(&verrs, 0.99), verrs[verrs.len() - 1]);
        println!("   reads per window per body: median {} p99 {} max {} ({} windows, {} bodies)", pw[pw.len() / 2], pw[((0.99 * (pw.len() - 1) as f64) as usize).min(pw.len() - 1)], pw[pw.len()-1], windows.len(), windows.keys().map(|(i, _)| i).collect::<std::collections::HashSet<_>>().len());
        println!("digest {digest}");
    }
}
