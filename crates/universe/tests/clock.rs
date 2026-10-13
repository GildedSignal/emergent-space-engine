//! Gate C1, the ship's clock (frozen by the integrator on 12 October, from the GLM probe of run
//! 20261011-1600-inversion-e128, which found the compiled clock off by about γ/2 from γ ≈ 3 and the ship lost at γ ≈ 1,761).
//!
//! A held burn from the plane's start at levels 8 and 15, at log-spaced checkpoints until the system's leave or γ = 10⁶:
//! (a) the tube's own dt/dτ (`orbit_state(t).proper_time`, which the view and the thrust flush read) against the exact u^t of
//!     the readout state (E = f·u^t, u^t = 1/√(f − v_r²/f − v_t²)): worst |ratio − 1| ≤ 1e-2;
//! (b) the readout's local γ against the closed form γ₀·cosh(ατ) + (u₀·n)·sinh(ατ), τ the ship's clock: worst relative
//!     error ≤ 1e-2;
//! (c) zero refusals, and the ship alive.
//! The oracle shares no code with the engine: the state is read out and the formulas are f64.
//!
//! The engine's cost bounds what a test may fly in 60 s: a held burn takes one kick per `2^-6/α` ticks at level 15, and the
//! motion law's clock shortens its step with the distance (the origin's fall grows the potential), so a full flight to the leave
//! (r = 2^40) is some 3×10⁵ events. The two tests below fly the first part of each burn; `…_to_the_leave` flies all of it
//! (run it with `--ignored`; minutes). The compiled clock is also checked to γ = 10⁶ by `crates/space/tests/clock.rs`.
use emergent_space::orbit::Scalar;
use emergent_universe::fleet::Order;
use emergent_universe::num::to_f64;
use emergent_universe::scenario::plane;
use emergent_universe::thrust::word;
use emergent_universe::Config;

struct Report {
    level: u8,
    /// |dt/dτ of the tube ÷ u^t − 1| and |γ readout ÷ closed form − 1|, per checkpoint.
    clock: Vec<f64>,
    gamma: Vec<f64>,
    /// The checkpoint (tick, γ) of each entry.
    at: Vec<(i64, f64)>,
    last_t: i64,
    last_gamma: f64,
    refusals: u64,
    alive: bool,
    left: bool,
    wall: f64,
}

fn local(x: [f64; 2], v: [f64; 2], mu: f64) -> (f64, [f64; 2]) {
    let r = (x[0] * x[0] + x[1] * x[1]).sqrt();
    let f = 1.0 - 2.0 * mu / r;
    let rh = [x[0] / r, x[1] / r];
    let th = [-rh[1], rh[0]];
    let (vr, vt) = (v[0] * rh[0] + v[1] * rh[1], v[0] * th[0] + v[1] * th[1]);
    let w = [vr / f, vt / f.sqrt()];
    // f, and the local velocity in the plane's axes (radial and tangential unit vectors).
    (f, [w[0] * rh[0] + w[1] * th[0], w[0] * rh[1] + w[1] * th[1]])
}

/// Fly a held burn at `level` from the plane's start, checking at log-spaced ticks up to 2^`log2_end`.
fn fly(level: u8, log2_end: f64, checkpoints: usize, gamma_max: f64) -> Report {
    let started = std::time::Instant::now();
    let cfg = Config::default();
    let alpha = 2f64.powi(cfg.thrust_log2 + level as i32); // rapidity per proper tick
    let mut p = plane(cfg, 1, Order::Sparse, 1, 48).unwrap();
    let me = p.player;
    p.u.input(0, word(1, level)).unwrap();
    let f2 = |v: [Scalar; 2]| [to_f64(v[0]), to_f64(v[1])];
    // The start state: γ₀ and u₀·n (the heading is 0: n = (1, 0), and no turn key is held).
    let (g0, u0n) = {
        let rec = p.u.rec(me);
        let ctx = p.u.ctx();
        let (x, v) = rec.b.cartesian(0).unwrap();
        let mu = to_f64(ctx.tube_unit(me, rec.b.doll).unwrap().mu);
        let (_, w) = local(f2(x), f2(v), mu);
        let g = 1.0 / (1.0 - w[0] * w[0] - w[1] * w[1]).sqrt();
        (g, g * w[0])
    };
    let mut rep = Report { level, clock: vec![], gamma: vec![], at: vec![], last_t: 0, last_gamma: 1.0, refusals: 0, alive: true, left: false, wall: 0.0 };
    let mut t_prev = 0i64;
    for j in 1..=checkpoints {
        let t = (2f64.powf(24.0 + (log2_end - 24.0) * j as f64 / checkpoints as f64)) as i64;
        if t <= t_prev {
            continue;
        }
        p.u.settle(t);
        let rec = p.u.rec(me);
        rep.refusals = rec.refusals;
        if !rec.alive {
            rep.alive = false;
            rep.left = rec.refusals == 0 && rec.fault.is_none();
            break;
        }
        let ctx = p.u.ctx();
        let (x, v) = rec.b.cartesian(t).unwrap_or_else(|e| panic!("level {level}: the readout at {t} is refused: {e:?}"));
        let (x, v) = (f2(x), f2(v));
        let mu = to_f64(ctx.tube_unit(me, rec.b.doll).unwrap().mu);
        let (f, w) = local(x, v, mu);
        let r = (x[0] * x[0] + x[1] * x[1]).sqrt();
        let rh = [x[0] / r, x[1] / r];
        let (vr, vt) = (v[0] * rh[0] + v[1] * rh[1], -v[0] * rh[1] + v[1] * rh[0]);
        let den = f - vr * vr / f - vt * vt;
        let ut = 1.0 / den.sqrt();
        let gamma = 1.0 / (1.0 - w[0] * w[0] - w[1] * w[1]).sqrt();
        // (a) the tube's own dt/dτ at t, over a window of 2^16 ticks.
        let shift = ctx.dolls[rec.b.doll as usize].shift as i32;
        let win = 1i64 << 16;
        let tau_at = |at: i64| to_f64(rec.b.orbit_state(at).unwrap().proper_time) * 2f64.powi(-shift);
        let rate = win as f64 / (tau_at(t + win) - tau_at(t));
        // (b) the closed form at the ship's clock: the proper time summed over its bindings, plus the tube's since the last.
        let tau = to_f64(rec.proper) + tau_at(t) - tau_at(rec.b.event_time);
        let closed = g0 * (alpha * tau).cosh() + u0n * (alpha * tau).sinh();
        rep.clock.push((rate / ut - 1.0).abs());
        rep.gamma.push((gamma / closed - 1.0).abs());
        rep.at.push((t, gamma));
        rep.last_t = t;
        rep.last_gamma = gamma;
        t_prev = t;
        if gamma >= gamma_max {
            break;
        }
    }
    rep.wall = started.elapsed().as_secs_f64();
    rep
}

fn median(v: &[f64]) -> f64 {
    let mut s = v.to_vec();
    s.sort_by(|a, b| a.partial_cmp(b).unwrap());
    s[s.len() / 2]
}

fn judge(r: &Report) {
    let worst = |v: &[f64]| v.iter().cloned().fold(0.0, f64::max);
    println!(
        "level {:>2}: {} checkpoints to t = {:.3e}, γ = {:.1}, {:.1} s; (a) dt/dτ over u^t: worst {:.2e}, median {:.2e}; (b) γ over its closed form: worst {:.2e}, median {:.2e}; refusals {}, alive {}, left the system {}",
        r.level, r.clock.len(), r.last_t as f64, r.last_gamma, r.wall, worst(&r.clock), median(&r.clock), worst(&r.gamma), median(&r.gamma), r.refusals, r.alive, r.left
    );
    let argmax = |v: &[f64]| v.iter().enumerate().fold((0, 0.0), |m, (i, &x)| if x > m.1 { (i, x) } else { m }).0;
    println!("  worst (a) at t = {:.3e}, γ = {:.3}; worst (b) at t = {:.3e}, γ = {:.3}", r.at[argmax(&r.clock)].0 as f64, r.at[argmax(&r.clock)].1, r.at[argmax(&r.gamma)].0 as f64, r.at[argmax(&r.gamma)].1);
    assert!(r.clock.len() >= 20, "level {}: the flight ended after {} checkpoints", r.level, r.clock.len());
    assert_eq!(r.refusals, 0, "level {}: the engine refused {} kicks (alive {})", r.level, r.refusals, r.alive);
    assert!(r.alive || r.left, "level {}: the ship was lost, not out of the system", r.level);
    assert!(worst(&r.clock) <= 1e-2, "level {}: (a) the tube's clock is off by {:.3e}", r.level, worst(&r.clock));
    assert!(worst(&r.gamma) <= 1e-2, "level {}: (b) γ is off its closed form by {:.3e}", r.level, worst(&r.gamma));
}

#[test]
fn c1_level_8_the_tubes_clock_is_the_ships_to_gamma_4() {
    judge(&fly(8, 38.0, 100, 1e6));
}

#[test]
fn c1_level_15_the_tubes_clock_is_the_ships_to_gamma_130() {
    judge(&fly(15, 36.0, 100, 1e6));
}

/// The whole gate: until the system's leave or γ = 10⁶ (minutes on the M1: run with `--ignored`).
#[test]
#[ignore]
fn c1_to_the_leave_at_levels_8_and_15() {
    for level in [8, 15] {
        judge(&fly(level, 41.7, 140, 1e6));
    }
}
