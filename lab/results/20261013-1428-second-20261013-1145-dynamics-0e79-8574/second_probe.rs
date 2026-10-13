//! The pump probe, second author's build: the 20261013-1145 record made regenerable, plus the
//! checker's named unflown flights.
//!
//! Record rows (identical code path to the original probe): the fate of a HELD reverse key on
//! main's merged prograde nose over (level, initial γ, nose offset), with D levels [0,2,4,5,6,8,15]
//! committed so ONE run regenerates all 22 rows of grid.txt + grid-d.txt.
//!
//! New rows:
//! - E: raise to apoapsis ≈ 2R / 4R (forward L2, cut on the osculating apoapsis; nose tracked to
//!   v during the coast-out by bang-bang turn keys), then the same held fixed-nose reverse brake
//!   from apoapsis — the Λ*-vs-r flight. μ̃ is self-calibrated from the circular start orbit at
//!   the first check (μ̃ = β²·r), so no hardcoded gravity enters the phasing.
//! - F: the tracking brake — hold reverse while re-pointing the nose along v every check
//!   (band ±2.5°), the nose-sense / attitude-control flight. The turn tier runs at 2⁻³⁰ turns/tick
//!   ≈ 4.1°/min; v rotates ≈ 4–5°/min in the fall, so the tracker is marginal by construction.
//! - G: the two off-axis C rows re-flown with per-check refusal logging (phase, doll, γ), the
//!   refusal-storm decomposition. Physics and stdout row are unchanged.
//!
//! cargo run --release -p emergent-universe --example second_probe [-- <end tick log2, default 35>]
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
const BAND_DEG: f64 = 2.5;
/// Home's radius in metres (4,313 root units; a root unit is the sun's radius over 471,000).
/// Readout arithmetic only — no flight decision passes through it.
const HOME_R_M: f64 = 4313.0 * 6.96e8 / 471_000.0;

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

/// Λ = thrust / local weight at `rr` (radius in Home radii), from the self-calibrated μ̃.
/// Λ = 2^(L−44) · rr² · R_m / (TICK_SECONDS · c · μ̃). Prints 0.427·2^L at the start orbit.
fn lambda_of(level: u8, rr: f64, mu_tilde: f64) -> f64 {
    2f64.powi(-44 + level as i32) * rr * rr * HOME_R_M / (TICK_SECONDS * 299_792_458.0 * mu_tilde)
}

struct Flight {
    name: String,
    g0: f64,
    level: u8,
    off_deg: f64,
    cut: bool,
    /// E: target apoapsis in Home radii (0 = not an E flight).
    raise: f64,
    /// F: re-point the nose along v while braking.
    track: bool,
    /// G: per-check refusal logging (on the two off-axis C rows).
    reflog: bool,
}

fn flights() -> Vec<Flight> {
    let f = |name: &str, g0: f64, level: u8, off_deg: f64, cut: bool| Flight {
        name: name.into(),
        g0,
        level,
        off_deg,
        cut,
        raise: 0.0,
        track: false,
        reflog: false,
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
    // The record's D row, all seven levels committed (the second checker's one-line fix).
    for level in [0u8, 2, 4, 5, 6, 8, 15] {
        v.push(f(&format!("D: from orbit L{level}"), -1.0, level, 0.0, false));
    }
    // E: the apoapsis brake at raised r (levels chosen to straddle Λ* at each radius).
    for (target, levels) in [(1.3f64, &[1u8, 4][..]), (1.6, &[1u8, 4][..]), (2.0, &[1u8, 2, 3, 4][..]), (4.0, &[0u8, 1, 2, 4][..])] {
        for &level in levels {
            v.push(Flight {
                name: format!("E{target:.1}R: apo brake L{level}"),
                g0: -2.0,
                level,
                off_deg: 0.0,
                cut: false,
                raise: target,
                track: false,
                reflog: false,
            });
        }
    }
    // F: the tracking brake from the start orbit (fixed-nose fates: L0/L2/L4 crash, L5 grazes).
    for level in [0u8, 2, 4, 5] {
        v.push(Flight {
            name: format!("F: track brake L{level}"),
            g0: -3.0,
            level,
            off_deg: 0.0,
            cut: false,
            raise: 0.0,
            track: true,
            reflog: false,
        });
    }
    // G: refusal decomposition on the two storm rows themselves (physics unchanged).
    for fl in v.iter_mut() {
        if fl.name.contains("off45") || fl.name.contains("off90") {
            fl.reflog = true;
        }
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
        // phase: 0 coast, 1 pump, 2 turn, 3 hold, 4 post (cut), 5 raise, 6 coast-out — 9 done
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
        // E/F/G bookkeeping
        let mut mu_tilde = 0.0f64; // μ̃ in Home radii × (c=1), from the circular start orbit
        let mut rr_hold = 0.0f64;
        let mut rr_prev = 0.0f64; // coast-out apoapsis detector
        let mut rapo = 0.0f64;
        let mut last_word: Option<u8> = None; // tracker inputs only on change
        let mut lag_max = 0.0f64;
        let mut lambda0 = 0.0f64;
        let mut min_rr_hold = f64::INFINITY;
        let mut ref_prev: u64 = 0;
        let mut phase_at_ref: Vec<(u8, u64)> = Vec::new(); // (phase, refusals) at each change
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
            // G: refusal change → log with the phase that accrued it (before any transition below).
            if fl.reflog && rec.refusals != ref_prev {
                phase_at_ref.push((phase, rec.refusals - ref_prev));
                eprintln!(
                    "G t={}s phase={} dref={} tot={} doll={} g_d={:.4}",
                    v.tick as f64 * TICK_SECONDS, phase, rec.refusals - ref_prev, rec.refusals, v.doll, g_d
                );
                ref_prev = rec.refusals;
            }
            let _ = v.loss;
            if !v.alive {
                last = v.loss.unwrap_or_else(|| format!("lost@{}", v.tick));
                break;
            }
            // E: self-calibrate μ̃ on the circular start orbit, once, before any input.
            if (fl.raise > 0.0 || fl.track) && mu_tilde == 0.0 && rr.is_finite() {
                let b2 = v.doll_beta[0] * v.doll_beta[0] + v.doll_beta[1] * v.doll_beta[1];
                mu_tilde = b2 * rr;
            }
            match phase {
                0 if v.tick >= 1 << 20 => {
                    if fl.g0 > 0.0 {
                        phase = 1;
                        let _ = p.u.input(v.tick, word(1, 15));
                    } else if fl.raise > 0.0 {
                        phase = 5; // raise: forward L0, cut on the osculating apoapsis
                        let _ = p.u.input(v.tick, word(1, 0));
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
                // E raise: cut when the osculating apoapsis reaches the target (or the orbit unbinds).
                5 => {
                    let (br, bt) = if rr.is_finite() && rr > 0.0 {
                        let (x, _) = rec.b.cartesian(v.tick.max(rec.b.event_time)).unwrap();
                        let (xn, yn) = (to_f64(x[0]), to_f64(x[1]));
                        let rn = (xn * xn + yn * yn).sqrt();
                        let rhat = [xn / rn, yn / rn];
                        let b = v.doll_beta;
                        (b[0] * rhat[0] + b[1] * rhat[1], (b[0] * rhat[1] - b[1] * rhat[0]).abs())
                    } else { (f64::INFINITY, 0.0) };
                    let eps = (br * br + bt * bt) / 2.0 - mu_tilde / rr;
                    let h = rr * bt;
                    let rapo_now = if eps < 0.0 && mu_tilde > 0.0 {
                        let aa = -mu_tilde / (2.0 * eps);
                        let e = (1.0 + 2.0 * eps * h * h / (mu_tilde * mu_tilde)).sqrt();
                        aa * (1.0 + e)
                    } else { f64::INFINITY };
                    if rapo_now >= fl.raise || eps >= 0.0 {
                        phase = 6;
                        let _ = p.u.input(v.tick, word(0, 2)); // release; track the nose on the way out
                        rr_prev = rr;
                    }
                }
                // E coast-out: track the nose to v; apoapsis = first check where rr declines.
                6 => {
                    let no = nose_off(v.doll_beta, v.heading);
                    let b2 = v.doll_beta[0] * v.doll_beta[0] + v.doll_beta[1] * v.doll_beta[1];
                    let want = if b2 < 1e-14 {
                        word(0, 0)
                    } else if no > BAND_DEG {
                        word(4, 0)
                    } else if no < -BAND_DEG {
                        word(8, 0)
                    } else {
                        word(0, 0)
                    };
                    if last_word != Some(want) {
                        let _ = p.u.input(v.tick, want);
                        last_word = Some(want);
                    }
                    if rr_prev > 0.0 && rr < rr_prev - 1e-6 {
                        rapo = rr_prev;
                        phase = 3;
                        let _ = p.u.input(v.tick, word(2, fl.level)); // hold reverse, nose frozen ~on v
                        last_word = None;
                    } else {
                        rr_prev = rr_prev.max(rr);
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
                min_rr_hold = rr;
                rr_hold = rr;
                if fl.raise > 0.0 || fl.track {
                    lambda0 = lambda_of(fl.level, rr.max(1e-9), mu_tilde);
                }
                // The a-priori ruler: radians the velocity would turn (about the star, at its
                // hold-start angular rate) while the burn cancels the hold-start rapidity.
                let eta0 = gamma_of(v.beta).acosh();
                let (rx, ry) = (v.position_light_seconds[0], v.position_light_seconds[1]);
                let r_ticks = (rx * rx + ry * ry).sqrt() / TICK_SECONDS;
                let vt = (v.beta[0] * ry - v.beta[1] * rx) / (rx * rx + ry * ry).sqrt(); // |v x rhat| = v_t
                let alpha = 2f64.powi(-44 + fl.level as i32); // rapidity per proper tick
                psi0 = eta0 / alpha * (vt / r_ticks);
            }
            // F: the tracking brake — re-point the nose along v, inputs only on change.
            if fl.track && phase == 3 && v.tick > hold_tick {
                let no = nose_off(v.doll_beta, v.heading);
                lag_max = lag_max.max(no.abs());
                let b2 = v.doll_beta[0] * v.doll_beta[0] + v.doll_beta[1] * v.doll_beta[1];
                let key = if b2 < 1e-14 { 0 } else if no > BAND_DEG { 4 } else if no < -BAND_DEG { 8 } else { 0 };
                let want = word(2 | key, fl.level);
                if last_word != Some(want) {
                    let _ = p.u.input(v.tick, want);
                    last_word = Some(want);
                }
            }
            if phase >= 3 {
                if rr.is_finite() {
                    min_rr_hold = min_rr_hold.min(rr);
                }
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
        // E/F rows carry their extra readouts in the bracket; record rows keep the original bracket.
        let extra = if fl.raise > 0.0 {
            format!(", rapo={:.4}R, mu={:.3e}, Lam0={:.2}, thold={:.0}s, minRpost={:.4}", rapo, mu_tilde, lambda0, hold_tick as f64 * TICK_SECONDS, min_rr_hold)
        } else if fl.track {
            format!(", lagmax={:.1}deg, Lam0={:.2}, thold={:.0}s, minRpost={:.4}", lag_max, lambda0, hold_tick as f64 * TICK_SECONDS, min_rr_hold)
        } else {
            String::new()
        };
        println!(
            "{:<26} {:>7} {:>6} {:>8} {:>11} {:>9} {:>9} {:>9} {:>9} {:>8} {:>8} {:>7} {} [{:.1}s wall, cos0={:.3}, doll0={}, samedoll={}{}]",
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
            same_doll,
            extra
        );
    }
}
