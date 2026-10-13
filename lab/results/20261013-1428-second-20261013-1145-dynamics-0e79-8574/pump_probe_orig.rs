//! The pump probe: the fate of a HELD reverse key, mapped over (level, initial γ, nose offset) on
//! main's merged prograde nose, with the dimensionless ruler Ψ = the radians the velocity turns
//! while the thrust cancels the rapidity (Δφ_v over the braking phase).
//!
//! A flight: coast 2^20, pump forward L15 to γ₀, optionally turn the nose θ off the velocity,
//! then hold reverse at L (or cut it at rest, the P1 control). Settles (canonical, schedule-free)
//! with the pilot checked every 2^22 ticks — the transition ticks are a function of the checked
//! state alone, so every run of this probe reproduces bit for bit.
//!
//! cargo run --release -p emergent-universe --example pump_probe [-- <end tick log2, default 36>]
use emergent_universe::fleet::Order;
use emergent_universe::num::to_f64;
use emergent_universe::scenario::plane;
use emergent_universe::thrust::word;
use emergent_universe::view::{gather_cached, ViewCache, TICK_SECONDS};
use emergent_universe::Config;
use std::f64::consts::TAU;
use std::time::Instant;

const CHECK: i64 = 1 << 24;
const TRACE: i64 = 1 << 26;

fn gamma_of(b: [f64; 2]) -> f64 {
    let b2 = b[0] * b[0] + b[1] * b[1];
    1.0 / (1.0 - b2).max(1e-18).sqrt()
}

fn along(b: [f64; 2], h: [f64; 2]) -> f64 {
    b[0] * h[0] + b[1] * h[1]
}

/// The signed angle from the velocity to the heading, in degrees (positive = the nose is left of v).
fn nose_off(b: [f64; 2], h: [f64; 2]) -> f64 {
    let (bm, hm) = (b[0].hypot(b[1]), h[0].hypot(h[1]));
    if bm < 1e-12 || hm < 1e-12 {
        return 0.0;
    }
    let dot = ((b[0] * h[0] + b[1] * h[1]) / (bm * hm)).clamp(-1.0, 1.0);
    let cross = (b[0] * h[1] - b[1] * h[0]) / (bm * hm);
    let a = dot.acos();
    if cross > 0.0 { a } else { -a }.to_degrees()
}

struct Flight {
    name: String,
    g0: f64,
    level: u8,
    off_deg: f64,
    cut: bool,
}

fn flights() -> Vec<Flight> {
    let f = |name: &str, g0: f64, level: u8, off_deg: f64, cut: bool| Flight {
        name: name.into(),
        g0,
        level,
        off_deg,
        cut,
    };
    let mut v: Vec<Flight> = vec![
        f("control: coast", 0.0, 0, 0.0, false),
        f("control: cut-brake L8 g30", 30.0, 8, 0.0, true),
        f("A: held L15 g30", 30.0, 15, 0.0, false),
        f("A: held L12 g30", 30.0, 12, 0.0, false),
        f("A: held L8 g30", 30.0, 8, 0.0, false),
        f("A: held L4 g30", 30.0, 4, 0.0, false),
        f("A: held L2 g30", 30.0, 2, 0.0, false),
        f("B: held L15 g10", 10.0, 15, 0.0, false),
        f("B: held L15 g3", 3.0, 15, 0.0, false),
        f("B: held L15 g1.5", 1.5, 15, 0.0, false),
        f("B: held L15 g1.1", 1.1, 15, 0.0, false),
        f("C: held L15 g3 off45", 3.0, 15, 45.0, false),
        f("C: held L15 g3 off90", 3.0, 15, 90.0, false),
        f("C: held L15 g3 off135", 3.0, 15, 135.0, false),
        f("C: held L15 g3 off180", 3.0, 15, 180.0, false),
    ];
    for level in [5u8, 6, 8] {
        v.push(f(&format!("D: from orbit L{level}"), -1.0, level, 0.0, false));
    }
    let only = std::env::var("ONLY").unwrap_or_default();
    v.retain(|fl| only.is_empty() || fl.name.contains(&only));
    v
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let end_log2: i64 = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(35);
    let end: i64 = 1 << end_log2;
    println!(
        "pump probe: settle flights to 2^{end_log2} ({} game-s), checks every 2^24 ticks",
        end as f64 * TICK_SECONDS
    );
    println!(
        "{:<26} {:>7} {:>6} {:>8} {:>11} {:>9} {:>9} {:>9} {:>9} {:>8} {:>8} {:>7} {}",
        "flight", "g0 seen", "cross", "Psi0", "t_cross(s)", "g_cross", "g_min", "g_max_post", "Psi(rad)", "dphi(v)", "minR/R", "refus", "end"
    );
    for fl in flights() {
        // phase: 0 coast, 1 pump, 2 turn, 3 hold, 4 post (cut) — 9 done
        let (mut phase, mut armed) = (0u8, 0i32);
        let (mut hold_tick, mut cross_tick, mut arm_tick) = (0i64, 0i64, 0i64);
        let (mut g_cross, mut g_min, mut g_max_post) = (0.0f64, f64::INFINITY, 0.0f64);
        let (mut phi0, mut dphi_v) = (0.0f64, 0.0f64);
        let mut phi_prev: Option<f64> = None;
        let mut same_doll = true;
        let mut doll0 = String::new();
        let mut cos0 = 0.0f64;
        let mut g0_seen = 0.0f64;
        let mut psi0 = 0.0f64;
        let mut min_rr = f64::INFINITY;
        let mut last = String::new();
        let t0 = Instant::now();
        let mut p = plane(Config::default(), 1, Order::Sparse, 1, 48).unwrap();
        let mut t = CHECK;
        let mut cache = ViewCache::default();
        while t <= end {
            p.u.settle(t);
            let Some(v) = gather_cached(&p.u, &p.names, &mut cache) else { break };
            let rec = p.u.rec(p.player);
            let g_d = gamma_of(v.doll_beta);
            let g_s = gamma_of(v.beta);
            let rr = if rec.b.doll != 0 {
                rec.b.cartesian(v.tick.max(rec.b.event_time)).map(|(x, _)| {
                    (to_f64(x[0]).powi(2) + to_f64(x[1]).powi(2)).sqrt() / to_f64(p.u.dolls[rec.b.doll as usize].surface)
                }).unwrap_or(f64::INFINITY)
            } else {
                f64::INFINITY
            };
            if rr.is_finite() {
                min_rr = min_rr.min(rr);
            }
            let _ = v.loss;
            if !v.alive {
                last = v.loss.unwrap_or_else(|| format!("lost@{}", v.tick));
                break;
            }
            match phase {
                0 if v.tick >= 1 << 20 => {
                    if fl.g0 > 0.0 {
                        phase = 1;
                        let _ = p.u.input(v.tick, word(1, 15));
                    } else if fl.g0 < 0.0 {
                        phase = 3;
                        let _ = p.u.input(v.tick, word(2, fl.level));
                    } else {
                        phase = 4;
                    }
                }
                1 => {
                    if g_d >= fl.g0 || g_s >= fl.g0 {
                        g0_seen = g_d.max(g_s);
                        phase = if fl.off_deg > 0.0 { 2 } else { 3 };
                        let _ = p.u.input(v.tick, word(if fl.off_deg > 0.0 { 4 } else { 2 }, if fl.off_deg > 0.0 { 0 } else { fl.level }));
                    }
                }
                2 => {
                    if nose_off(v.doll_beta, v.heading) <= -fl.off_deg {
                        phase = 3;
                        let _ = p.u.input(v.tick, word(2, fl.level));
                    }
                }
                _ => {}
            }
            if phase == 3 && hold_tick == 0 {
                hold_tick = v.tick;
                phi0 = v.doll_beta[1].atan2(v.doll_beta[0]);
                doll0 = v.doll.to_string();
                cos0 = along(v.doll_beta, v.heading) / v.doll_beta.iter().map(|b| b * b).sum::<f64>().sqrt().max(1e-12);
                g_min = g_d;
                // The a-priori ruler: radians the velocity would turn (about the star, at its
                // hold-start angular rate) while the burn cancels the hold-start rapidity.
                let eta0 = gamma_of(v.beta).acosh();
                let (rx, ry) = (v.position_light_seconds[0], v.position_light_seconds[1]);
                let r_ticks = (rx * rx + ry * ry).sqrt() / TICK_SECONDS;
                let vt = (v.beta[0] * ry - v.beta[1] * rx) / (rx * rx + ry * ry).sqrt(); // |v x rhat| = v_t
                let alpha = 2f64.powi(-44 + fl.level as i32); // rapidity per proper tick
                psi0 = eta0 / alpha * (vt / r_ticks);
            }
            if phase >= 3 {
                if v.doll != doll0.as_str() {
                    same_doll = false;
                }
                let phi = v.doll_beta[1].atan2(v.doll_beta[0]);
                if let Some(pp) = phi_prev {
                    let mut d = phi - pp;
                    if d > std::f64::consts::PI {
                        d -= TAU;
                    }
                    if d < -std::f64::consts::PI {
                        d += TAU;
                    }
                    dphi_v += d;
                }
                phi_prev = Some(phi);
                let a = along(v.doll_beta, v.heading);
                if cross_tick == 0 {
                    if a > 1e-9 {
                        armed += 1;
                        if armed >= 3 {
                            arm_tick = v.tick;
                        }
                    } else if armed >= 3 {
                        cross_tick = v.tick;
                        g_cross = g_d;
                    }
                    if cross_tick == 0 {
                        g_min = g_min.min(g_d);
                    }
                } else {
                    g_max_post = g_max_post.max(g_d);
                }
                if fl.cut && cross_tick > 0 && phase == 3 {
                    phase = 4;
                    let _ = p.u.input(v.tick, word(0, fl.level));
                }
                if v.tick % TRACE == 0 {
                    eprintln!(
                        "  t={}s g_d={:.4} along={:.3e} rr={:.4} doll={} dphi={:.3}",
                        v.tick as f64 * TICK_SECONDS,
                        g_d,
                        a,
                        rr,
                        v.doll,
                        dphi_v
                    );
                }
            }
            last = format!("alive@{} g={:.4}", v.tick, g_d);
            t += CHECK;
        }
        let rec = p.u.rec(p.player);
        let psi = if cross_tick > 0 { dphi_v.abs() } else { f64::NAN };
        let print = |x: f64| if x.is_finite() { format!("{x:.4}") } else { "-".into() };
        println!(
            "{:<26} {:>7} {:>6} {:>8} {:>11} {:>9} {:>9} {:>9} {:>9} {:>8} {:>8} {:>7} {} [{:.1}s wall, cos0={:.3}, doll0={}, samedoll={}]",
            fl.name,
            if fl.g0 > 0.0 { print(if g0_seen > 0.0 { g0_seen } else { f64::NAN }) } else { "start".into() },
            if cross_tick > 0 { "yes" } else { "no" },
            print(psi0),
            if cross_tick > 0 { format!("{:.1}", cross_tick as f64 * TICK_SECONDS) } else { "-".into() },
            print(g_cross),
            print(if g_min.is_finite() { g_min } else { f64::NAN }),
            print(if g_max_post > 0.0 { g_max_post } else { f64::NAN }),
            print(psi),
            print(dphi_v),
            if min_rr.is_finite() { format!("{min_rr:.4}") } else { "-".into() },
            rec.refusals,
            last,
            t0.elapsed().as_secs_f64(),
            cos0,
            doll0,
            same_doll
        );
    }
}
