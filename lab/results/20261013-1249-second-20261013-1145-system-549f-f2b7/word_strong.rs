//! The acceleration word at strong field (r ≲ 20 M): the plane cannot express the scene (its star's
//! r = 20 M is inside its surface), but the engine can — a compact doll of 2^12 solar masses has
//! GM = 1 in its own units with a surface at 1 M, so a ship at periapsis 20 orbits at r = 20 M,
//! beta_circ = sqrt(1/20) = 0.224 (7ab4's strong-field consumer), and a moon at 800 (1/16 the mass)
//! gives the perturbing field a real gradient to age against.
//!
//! The question (549f's checker, the gold experiment's second half): does the kick cadence — the
//! word's refresh — shorten with the field enough that the stored word still tracks `a(mid)`, or
//! does strong field force one word per read? Measures, per gated read of the ship: the shipped
//! term |a(mid)|·tau²/2, the wired word's true error (the tree's readout vs the by-hand shipped
//! readout), the longest window against the ship's orbital period, and events per orbit.
//! Control flight: the same ship at r = 4000 (weak field, beta = 0.016).
//!
//! cargo run --release -p emergent-universe --example word_strong [-- <r: 20|4000>]
use emergent_universe::force;
use emergent_universe::num::{add2, scale2, time_of, to_f64};
use emergent_universe::observe::ramped_in;
use emergent_universe::scenario::STAR_RADIUS;
use emergent_space::orbit::Scalar;
use emergent_universe::num::s;
use emergent_universe::{Budget, Config, Kind, OrbitSpec, Universe};
use std::collections::HashMap;
use std::time::Instant;

fn flight(r: i64, frames: usize, name: &str) {
    let mut u = Universe::new(s(STAR_RADIUS), Config::default());
    u.threads = 1;
    // the compact: 2^-4 of the star (a red dwarf) with a surface at 1 M of its own mass: a doll's
    // units normalise GM = 1 and c = 1, so periapsis 20 is r = 20 M regardless of the star; deeper dolls must be lighter
    let compact = u.add_body(Kind::Planet, OrbitSpec { doll: 0, periapsis: s(101_300_000), e_q48: 0, clockwise: false, angle: 0, phase: 0 }, Scalar::ZERO).unwrap();
    let cd = u.add_doll("compact", compact, -4, s(1)).unwrap();
    // the moon: 1/16 of the compact at 800 (its sphere of influence there is ~205; the ship at r never enters)
    let moon = u.add_body(Kind::Planet, OrbitSpec { doll: cd, periapsis: s(800), e_q48: 0, clockwise: false, angle: 0, phase: 0 }, Scalar::ZERO).unwrap();
    let _md = u.add_doll("moon", moon, -12, s(1)).unwrap();
    // the ship: r gravitational radii of the compact
    let ship = u.add_body(Kind::Ship, OrbitSpec { doll: cd, periapsis: s(r), e_q48: 0, clockwise: false, angle: 0, phase: 0 }, Scalar::ZERO).unwrap();
    u.start().unwrap();
    let t0 = Instant::now();
    let events0 = u.rec(ship).events;
    let mut windows: HashMap<i64, u32> = HashMap::new();
    let mut reads: Vec<(f64, f64, f64)> = Vec::new(); // (term, wired pos err, wired dv err)
    let mut max_len = 0.0f64; // window length in doll time units
    for f in 0..frames {
        let frame = u.frame_to(1.0 / 60.0, 100.0, Budget::unlimited(), i64::MAX);
        let t = frame.presented;
        let ctx = u.ctx();
        let rec = u.rec(ship);
        if !rec.alive {
            println!("== {name}: ship lost at frame {f} ({:?}) ==", rec.fault);
            return;
        }
        let b = rec.b;
        let k = b.kick;
        let mut sample = || -> Option<()> {
            if !k.clock {
                return None;
            }
            let (base, start) = if t >= k.boundary {
                (b.clone(), k.boundary)
            } else {
                if k.lead <= 0 {
                    return None;
                }
                let prev = ctx.bodies.binding_at(ship, b.event_time - 1)?;
                (prev, b.event_time - k.lead)
            };
            let tau = t - start;
            if tau <= 0 || tau > 2 * k.len.max(1) {
                return None;
            }
            // the shipped partial step, by hand
            let mid = start + tau / 2;
            let (x_mid, _) = base.cartesian(mid).ok()?;
            let secs = ctx.secondaries(base.doll, mid, ship).ok()?;
            let field = force::field(&secs, x_mid).ok()?;
            let tau_s = time_of(tau, base.clock_exp).ok()?;
            let dv = scale2(field.accel, tau_s).ok()?;
            let dx = scale2(dv, tau_s.scale(-1).ok()?).ok()?;
            let (px, pv) = base.cartesian(t).ok()?;
            let sp = add2(px, dx).ok()?;
            let sv = add2(pv, dv).ok()?;
            // the read the tree serves (wired tree: from the stored word)
            let (wp, wv) = ramped_in(&ctx, ship, t, &b).ok()?;
            let ts2 = to_f64(tau_s) * to_f64(tau_s) / 2.0;
            let am = to_f64(field.accel[0]).powi(2) + to_f64(field.accel[1]).powi(2);
            let term = am.sqrt() * ts2;
            let pe = ((to_f64(wp[0]) - to_f64(sp[0])).powi(2) + (to_f64(wp[1]) - to_f64(sp[1])).powi(2)).sqrt();
            let ve = ((to_f64(wv[0]) - to_f64(sv[0])).powi(2) + (to_f64(wv[1]) - to_f64(sv[1])).powi(2)).sqrt();
            reads.push((term, pe, ve));
            if let Ok(len_s) = time_of(k.len, base.clock_exp) {
                max_len = max_len.max(to_f64(len_s));
            }
            *windows.entry(start).or_insert(0) += 1;
            Some(())
        };
        let _ = sample();
        drop(ctx);
    }
    let digest = u.digest();
    let mut terms: Vec<f64> = reads.iter().map(|x| x.0).collect();
    let mut perrs: Vec<f64> = reads.iter().map(|x| x.1).collect();
    let mut verrs: Vec<f64> = reads.iter().map(|x| x.2).collect();
    for v in [&mut terms, &mut perrs, &mut verrs] {
        v.sort_by(|a, b| a.partial_cmp(b).unwrap());
    }
    let q = |v: &Vec<f64>, f: f64| v[((f * (v.len() - 1) as f64) as usize).min(v.len() - 1)];
    let rec = u.rec(ship);
    let beta = (1.0 / r as f64).sqrt();
    let period = 2.0 * std::f64::consts::PI * (r as f64).powf(1.5); // GM = 1, c = 1
    let game_time = frames as f64 / 60.0 * 100.0; // rtf 100
    println!("== {name}: r = {r} M (beta_circ {beta:.3}), period {period:.0} GM/c^3, {frames} frames = {game_time:.0} t doll-units, {:.1}s wall ==", t0.elapsed().as_secs_f64());
    println!("   ship alive {} events {} windows {} reads {}", rec.alive, rec.events - events0, windows.len(), reads.len());
    if !reads.is_empty() {
        println!("   term      (doll units): median {:.3e} p99 {:.3e} max {:.3e}", q(&terms, 0.5), q(&terms, 0.99), terms[terms.len() - 1]);
        println!("   wired err (doll units): median {:.3e} p99 {:.3e} max {:.3e}", q(&perrs, 0.5), q(&perrs, 0.99), perrs[perrs.len() - 1]);
        println!("   wired dv-err           : median {:.3e} p99 {:.3e} max {:.3e}", q(&verrs, 0.5), q(&verrs, 0.99), verrs[verrs.len() - 1]);
        println!("   longest window seen {:.1} doll t-units = {:.2} ship periods; events per orbit {:.1}", max_len, max_len / period, (rec.events - events0) as f64 * period / game_time);
    }
    println!("digest {digest}");
}

fn main() {
    let which = std::env::args().nth(1).unwrap_or_default();
    if which.is_empty() || which == "20" {
        flight(20, 480, "strong r=20M");
    }
    if which.is_empty() || which == "4000" {
        flight(4000, 480, "weak control r=4000M");
    }
}
