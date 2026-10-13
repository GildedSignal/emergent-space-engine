//! The Λ* map: does the from-orbit crash-basin boundary Λ* = thrust/local-weight (0e79's
//! Λ* ∈ (6.8, 13.6), one scene, one nose sense) move with r/R, orbit sense, or eccentricity?
//!
//! One flight: the player starts on a circular (or eccentric, retro) orbit about Home at radius
//! `alt` × Home's low orbit, and at the first check (tick 2^24) holds the reverse key at `level`
//! — 0e79's "from orbit" D row, never re-asserted. Fate classes: CRASH (dead near the surface),
//! ESCAPE (pumped out past 1.5 R with γ > 1.0002 and r rising), or LINGER at the horizon
//! (2^33 ticks = 42,211 game-s ≈ 11.7 game-hours; D-row deaths all land inside 800 s).
//! Bisection on `alt` at a fixed level localizes the boundary: with the point-mass g ∝ 1/r²,
//! Λ(alt, L) = Λ(1, L)·alt², so if Λ* is a constant of the mechanism every level returns the
//! same Λ*, and if the true ruler is the surface gravity the summary shows Λ* ∝ 1/alt².
//!
//! Λ is computed from first principles per flight: GM(Home) is measured once from the default
//! circular start (GM = β²r²), and Λ = (2^(L−44)·2^18)·r²/GM in Home units, c = 2^18 Home/tick.
//! Sanity: Λ(L0, alt 1) must print ≈ 0.43 (0e79's independent number).
//!
//! cargo run --release -p emergent-universe --example lam_star [-- one <alt> <0|1> <e> <L> [end_log2] | bisect <L> <0|1> <e> <lo> <hi> [end_log2] | grid [end_log2]]
use emergent_universe::fleet::Order;
use emergent_universe::num::to_f64;
use emergent_universe::scenario::plane_player;
use emergent_universe::thrust::word;
use emergent_universe::view::{gather_cached, ViewCache, TICK_SECONDS};
use emergent_universe::Config;
use std::time::Instant;

const CHECK: i64 = 1 << 24;
const BRAKE_AT: i64 = 1 << 24; // the first check: brake input lands here (0e79's D row)
const ALT_RR: f64 = 1.0990; // r/R of the default start (7,000 km over Home's 6,371 km surface)

fn gamma_of(b: [f64; 2]) -> f64 {
    let b2 = b[0] * b[0] + b[1] * b[1];
    1.0 / (1.0 - b2).max(1e-18).sqrt()
}

#[derive(Clone, Copy, PartialEq, Debug)]
enum Fate {
    Crash,
    Escape,
    Linger,
}

struct Row {
    fate: Fate,
    lam: f64,
}

fn build(alt: f64, retro: bool, e: f64) -> emergent_universe::scenario::Plane {
    let (world, _) = emergent_engine::scenes::battle(48, emergent_universe::fleet::Q, 1, 1 << 15, false);
    plane_player(Config::default(), 1, Order::Sparse, 1, world, alt, retro, e).unwrap()
}

fn r_over_r(p: &emergent_universe::scenario::Plane, tick: i64) -> f64 {
    let rec = p.u.rec(p.player);
    rec.b
        .cartesian(tick.max(rec.b.event_time))
        .map(|(x, _)| {
            let doll = &p.u.dolls[rec.b.doll as usize];
            (to_f64(x[0]).powi(2) + to_f64(x[1]).powi(2)).sqrt() / to_f64(doll.surface)
        })
        .unwrap_or(f64::INFINITY)
}

/// Λ at the brake start: proper thrust 2^(L−44) root/tick² (c = 1 root/tick) over GM/r² (root³/tick²).
fn lam_of(level: u8, r: f64, gm: f64) -> f64 {
    2f64.powi(level as i32 - 44) * r * r / gm
}

/// Home's GM in root³/tick², measured from the default circular start: two settled positions one
/// 2^20-tick window apart give ω, and GM = ω²r³ (Kepler, the engine's own truth — no unit guessing).
fn measure_gm() -> (f64, f64) {
    let p = build(1.0, false, 0.0);
    let mut u = p.u;
    let mut pos = |t: i64| -> (f64, f64) {
        u.settle(t);
        let rec = u.rec(p.player);
        rec.b.cartesian(t.max(rec.b.event_time)).map(|(x, _)| {
            let doll = &u.dolls[rec.b.doll as usize];
            let f = 2f64.powi(doll.mass_log2); // doll units → root units
            (to_f64(x[0]) * f, to_f64(x[1]) * f)
        }).unwrap()
    };
    let (x1, y1) = pos(BRAKE_AT);
    let (x2, y2) = pos(BRAKE_AT + (1 << 20));
    let r = (x1 * x1 + y1 * y1).sqrt();
    let dtheta = (y2.atan2(x2) - y1.atan2(x1)).abs();
    let omega = dtheta / (1 << 20) as f64; // rad per tick
    (omega * omega * r * r * r, r)
}
fn flight(gm: f64, alt: f64, retro: bool, e: f64, level: u8, end_log2: i64, burn: bool) -> Row {
    let t0 = Instant::now();
    let mut p = build(alt, retro, e);
    let mut cache = ViewCache::default();
    let end = 1i64 << end_log2;
    let (mut lam, mut min_rr, mut end_rr, mut g_max) = (0.0f64, f64::INFINITY, 0.0f64, 0.0f64);
    let mut rr_hist: Vec<f64> = Vec::new();
    let mut fate = Fate::Linger;
    let (mut t_s, mut refusals) = (0.0f64, 0u64);
    let mut t = CHECK;
    while t <= end {
        p.u.settle(t);
        let Some(v) = gather_cached(&p.u, &p.names, &mut cache) else { break };
        let rr = r_over_r(&p, v.tick);
        let g_d = gamma_of(v.doll_beta);
        if t == BRAKE_AT && burn {
            let rec = p.u.rec(p.player);
            let r_root = rec.b.cartesian(v.tick.max(rec.b.event_time)).map(|(x, _)| {
                let f = 2f64.powi(p.u.dolls[rec.b.doll as usize].mass_log2);
                (to_f64(x[0]).powi(2) + to_f64(x[1]).powi(2)).sqrt() * f
            }).unwrap();
            lam = lam_of(level, r_root, gm);
            let _ = p.u.input(v.tick, word(2, level)); // held reverse: one assertion, never re-asserted
        }
        min_rr = min_rr.min(rr);
        end_rr = rr;
        g_max = g_max.max(g_d);
        t_s = v.tick as f64 * TICK_SECONDS;
        refusals = p.u.rec(p.player).refusals;
        if !v.alive {
            fate = Fate::Crash;
            break;
        }
        if burn && t > BRAKE_AT {
            rr_hist.push(rr);
            if rr_hist.len() >= 3 {
                let rising = rr_hist.iter().zip(rr_hist.iter().skip(1)).all(|(a, b)| b > a);
                if (rr > 1.5 && g_d > 1.0002 && rising) || rr > 40.0 {
                    fate = Fate::Escape;
                    break;
                }
            }
            if rr_hist.len() > 4 {
                rr_hist.remove(0);
            }
        }
        t += CHECK;
    }
    println!(
        "{:>6.3} {} e={:<4} L{:<2} Λ={:<9.3} {:<7} t={:<9.1}s minR/R={:<8.4} endR/R={:<9.3} γmax={:<9.4} refus={:<6} [{:.1}s wall]",
        alt, if retro { "retro" } else { "pro  " }, e, level, lam,
        format!("{:?}", fate).to_uppercase(), t_s, min_rr, end_rr, g_max, refusals,
        t0.elapsed().as_secs_f32()
    );
    Row { fate, lam }
}

/// Bisect alt in [lo, hi] (lo crashes, hi does not) at a fixed level; returns (alt*, Λ*).
fn bisect(gm: f64, r0: f64, level: u8, retro: bool, e: f64, lo: f64, hi: f64, end_log2: i64) -> Option<(f64, f64)> {
    println!("-- bisect L{level} retro={retro} e={e} in [{lo}, {hi}]");
    let f_lo = flight(gm, lo, retro, e, level, end_log2, true).fate;
    let f_hi = flight(gm, hi, retro, e, level, end_log2, true).fate;
    if f_lo != Fate::Crash || f_hi == Fate::Crash {
        println!("   !! bracket failed: lo → {f_lo:?}, hi → {f_hi:?}\n");
        return None;
    }
    let (mut lo, mut hi) = (lo, hi);
    for _ in 0..9 {
        let mid = (lo * hi).sqrt();
        match flight(gm, mid, retro, e, level, end_log2, true).fate {
            Fate::Crash => lo = mid,
            _ => hi = mid,
        }
    }
    let alt_star = (lo * hi).sqrt();
    let lam_star = lam_of(level, r0, gm) * alt_star * alt_star; // Λ ∝ alt² at fixed L (g ∝ 1/r²)
    println!("   => alt* = {alt_star:.4}, Λ* = {lam_star:.2}   [r*/R = {:.3}]\n", ALT_RR * alt_star);
    Some((alt_star, lam_star))
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mode = args.get(1).cloned().unwrap_or("grid".into());
    let (gm, r0) = measure_gm();
    println!("GM(Home) = {gm:.4e} root³/tick² from the default start (r₀ = {r0:.4e} root units);");
    println!("sanity Λ(L0, alt 1) = {:.3} (0e79 measured 0.43); default start r/R = {ALT_RR}\n", lam_of(0, r0, gm));
    match mode.as_str() {
        "one" => {
            let alt: f64 = args[2].parse().unwrap();
            let retro = args[3] == "1";
            let e: f64 = args[4].parse().unwrap();
            let level: u8 = args[5].parse().unwrap();
            let end: i64 = args.get(6).and_then(|s| s.parse().ok()).unwrap_or(33);
            flight(gm, alt, retro, e, level, end, true);
        }
        "bisect" => {
            let level: u8 = args[2].parse().unwrap();
            let retro = args[3] == "1";
            let e: f64 = args[4].parse().unwrap();
            let lo: f64 = args[5].parse().unwrap();
            let hi: f64 = args[6].parse().unwrap();
            let end: i64 = args.get(7).and_then(|s| s.parse().ok()).unwrap_or(33);
            bisect(gm, r0, level, retro, e, lo, hi, end);
        }
        _ => {
            let end_log2: i64 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(33);
            println!("== controls: 0e79's D row reproduced at alt 1.0 (L0/L2/L4 crash, L5/L6/L8 escape), horizon 2^{end_log2}");
            for level in [0u8, 2, 4, 5, 6, 8] {
                flight(gm, 1.0, false, 0.0, level, end_log2, true);
            }
            println!("\n== the r/R axis: bisect alt at L0–L4 (each returns Λ* if the mechanism is r-independent)");
            let mut stars = Vec::new();
            for (level, lo, hi) in [(0u8, 2.0f64, 8.0), (1, 1.5, 6.0), (2, 1.2, 5.0), (3, 1.05, 3.0), (4, 1.0, 1.9)] {
                if let Some(s) = bisect(gm, r0, level, false, 0.0, lo, hi, end_log2) {
                    stars.push((level, s));
                }
            }
            println!("== Λ* vs level (r*/R = 1.099·alt*):");
            for (level, (alt, lam)) in &stars {
                println!("   L{level}: alt* = {alt:.4}, r*/R = {:.3}, Λ* = {lam:.2}", ALT_RR * alt);
            }
            println!("\n== sense: retro at L2");
            bisect(gm, r0, 2, true, 0.0, 1.2, 5.0, end_log2);
            println!("\n== eccentricity: e ∈ {{0.3, 0.6, 0.9}} at L2 (brake from periapsis)");
            for e in [0.3f64, 0.6, 0.9] {
                bisect(gm, r0, 2, false, e, 1.2, 5.0, end_log2);
            }
        }
    }
}
