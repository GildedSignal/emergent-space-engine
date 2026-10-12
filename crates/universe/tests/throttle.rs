//! The throttle is part of the player's decision (docs/law.md, "Ties": a decision takes effect at its logged canonical
//! tick): one byte, the keys in bits 0-3 and the level in bits 4-7, the burn `2^level` times the base thrust (0.35 g at
//! level 0, about 11,500 g at 15). Physics is unchanged: the burn grows the rapidity in proper time, and the work is
//! what the energy gains.
//!
//! **Frozen before the first run.**
//! 1. A word with level 0 is the keys alone (every old log replays as before), and the levels' accelerations are
//!    `0.353 g · 2^level`, from 0.35 g to about 10^4 g.
//! 2. At every level the burn's work holds: the energy gained equals `∫ α·(v·n) dt` along the heading `n` (3%), the same criterion as
//!    `plane.rs`, with the burn long enough at each level to be well past the steps' own size.
//! 3. A log with throttle changes replays to one digest on any frames, budget and thread count; another level (a
//!    control) gives another digest.
//! 4. The time factor changes when, never what: a flight flown live with its time factor changed every few frames
//!    (decisions taken at the presented ticks and logged) replays from its log, at any other time factor, to the
//!    same digest. (Compared at a cut well past the flight: a live frame may resolve a body past the presented tick
//!    when another reads it, so the digest is canonical only once everything up to a cut beyond that is resolved.)
use emergent_space::orbit::Scalar;
use emergent_universe::fleet::Order;
use emergent_universe::num::to_f64;
use emergent_universe::observe::held_thrust;
use emergent_universe::scenario::{plane, Plane};
use emergent_universe::thrust::{g_of, split, word, MAX_LEVEL};
use emergent_universe::view::gather;
use emergent_universe::{Budget, Config};

#[test]
fn the_word_keeps_the_keys_and_the_levels_are_powers_of_two_of_a_third_of_a_g() {
    for keys in 0..16u8 {
        assert_eq!(word(keys, 0), keys, "level 0 is the keys alone");
        for level in 0..=MAX_LEVEL {
            assert_eq!(split(word(keys, level)), (keys, level));
        }
    }
    let cfg = Config::default();
    let g0 = g_of(&cfg, 0);
    assert!((g0 - 0.353).abs() < 0.002, "level 0 is about 0.35 g: {g0}");
    for l in 1..=MAX_LEVEL {
        assert!((g_of(&cfg, l) / g_of(&cfg, l - 1) - 2.0).abs() < 1e-12, "a power of two a level");
    }
    let top = g_of(&cfg, MAX_LEVEL);
    assert!((9_000.0..13_000.0).contains(&top), "the top is about 10^4 g: {top}");
}

/// The energy (Newtonian, in the Home doll's units) and the velocity of the player at `t`, the burn owed since the last
/// flush included (the engine takes it at its own kicks; the view reads it within the frame).
fn energy(p: &Plane, t: i64) -> (f64, [f64; 2]) {
    let rec = p.u.rec(p.player);
    let (x, v) = rec.b.cartesian(t).unwrap();
    let dv = held_thrust(&p.u.ctx(), &rec, t).unwrap().map_or([0.0; 2], |o| o.1);
    let f = |s: Scalar| to_f64(s);
    let (x, v) = ([f(x[0]), f(x[1])], [f(v[0]) + dv[0], f(v[1]) + dv[1]]);
    (0.5 * (v[0] * v[0] + v[1] * v[1]) - 1.0 / (x[0] * x[0] + x[1] * x[1]).sqrt(), v)
}

#[test]
fn the_burn_does_the_work_at_every_level() {
    let cfg = Config::default();
    for level in 0..=MAX_LEVEL {
        let mut p = plane(cfg, 5, Order::Sparse, 1, 8).unwrap();
        let alpha = 2f64.powi(cfg.thrust_log2 + level as i32); // rapidity per tick
        let t0 = 2_000_000;
        p.u.settle(t0);
        // Forward: along the heading, which starts along the orbit's own direction of motion (prograde, so the burn raises
        // the orbit: a burn against it that stopped the ship dead above the planet would be a radial plunge).
        let n = emergent_universe::thrust::direction(p.u.rec(p.player).thrust.unwrap().heading).unwrap().map(to_f64);
        let along = |v: [f64; 2]| v[0] * n[0] + v[1] * n[1];
        p.u.input(t0, word(1, level)).unwrap();
        // A burn of at most 4e6 ticks, and no more than 2e-4 c of velocity: the ship stays in Home's doll.
        let span = ((2e-4 / alpha) as i64).clamp(100_000, 4_000_000);
        let (e0, mut last_v) = energy(&p, t0);
        let (mut work, mut t, mut last_t) = (0.0f64, t0, t0);
        let dt = span / 200;
        while t < t0 + span {
            t += dt;
            p.u.settle(t);
            let (_, v) = energy(&p, t);
            work += alpha * 0.5 * (along(last_v) + along(v)) * (t - last_t) as f64;
            last_v = v;
            last_t = t;
        }
        let (e1, _) = energy(&p, t);
        let d = e1 - e0;
        let rec = p.u.rec(p.player);
        println!("level {level:>2}: {} ticks, energy changed by {d:.4e}, the work done {work:.4e} ({} refusals)", t - t0, rec.refusals);
        assert!(rec.alive && rec.refusals == 0, "level {level}: the engine refused");
        assert!(work.abs() > 1e-12, "level {level}: the burn must do work");
        assert!(((d - work) / work).abs() < 0.03, "level {level}: ΔE {d:e} against work {work:e}");
        assert_eq!(p.u.rec(p.player).thrust.unwrap().level, level);
    }
}

const CUT: i64 = 200_000_000;
/// Decisions at canonical ticks: burn at level 8, up to 15, coast at 15, burn and reverse at 3, coast.
const LOG: [(i64, u8); 6] = [(10_000_000, 0x81), (14_000_000, 0xF1), (18_000_000, 0xF0), (100_000_000, 0x39), (102_000_000, 0x32), (104_000_000, 0x30)];

fn run(log: &[(i64, u8)], dts: &[f64], budget: Budget, threads: usize, rtfs: &[f64]) -> (String, Vec<(i64, u8)>) {
    let mut p = plane(Config::default(), 3, Order::Sparse, threads, 16).unwrap();
    for &(t, k) in log {
        p.u.schedule(t, k).unwrap();
    }
    let mut f = 0;
    while p.u.now < CUT && f < 200_000 {
        p.u.frame_to(dts[f % dts.len()], rtfs[f % rtfs.len()], budget, CUT);
        f += 1;
    }
    p.u.settle(CUT);
    (p.u.digest(), p.u.inputs.clone())
}

#[test]
fn a_log_with_throttle_changes_replays_to_one_digest() {
    let (reference, taken) = run(&LOG, &[1.0 / 60.0], Budget::unlimited(), 1, &[100.0]);
    assert_eq!(taken, LOG.to_vec(), "the decisions as taken are the decisions as logged");
    for (dts, budget, threads, rtfs) in [
        (&[1.0 / 60.0, 0.0171, 0.033, 0.0042][..], Budget::unlimited(), 4, &[100.0][..]),
        (&[1.0 / 37.0, 1.0 / 144.0][..], Budget::events(40), 2, &[100.0][..]),
        (&[1.0 / 60.0][..], Budget::events(5), 1, &[100.0][..]),
    ] {
        let (d, taken) = run(&LOG, dts, budget, threads, rtfs);
        assert_eq!(taken, LOG.to_vec(), "{budget:?}: a decision moved or was dropped");
        assert_eq!(d, reference, "{budget:?}, {threads} threads");
    }
    // Controls: the digest must be able to fail. Another level for the same keys, and the same log without its throttle.
    let mut other = LOG;
    other[1].1 = 0xE1;
    assert_ne!(run(&other, &[1.0 / 60.0], Budget::unlimited(), 1, &[100.0]).0, reference, "a lower level must give another universe");
    let plain: Vec<_> = LOG.iter().map(|&(t, w)| (t, w & 15)).collect();
    assert_ne!(run(&plain, &[1.0 / 60.0], Budget::unlimited(), 1, &[100.0]).0, reference, "the level must matter");
}

#[test]
fn the_time_factor_changes_when_and_never_what() {
    // Flown live: keys and throttle taken at the presented ticks, the time factor changed every few frames.
    let mut p = plane(Config::default(), 4, Order::Sparse, 1, 8).unwrap();
    let live = [1.0, 100.0, 3000.0, 10.0, 0.5, 250.0];
    for f in 0..90 {
        match f {
            4 => p.u.input(p.u.now, word(1, 8)).unwrap(),
            20 => p.u.input(p.u.now, word(1, 15)).unwrap(),
            40 => p.u.input(p.u.now, word(5, 15)).unwrap(),
            55 => p.u.input(p.u.now, word(0, 15)).unwrap(),
            70 => p.u.input(p.u.now, word(2, 4)).unwrap(),
            _ => {}
        }
        p.u.frame(1.0 / 60.0, live[(f / 5) % live.len()], Budget::events(50));
        let _ = gather(&p.u, &p.names);
    }
    let log = p.u.inputs.clone();
    assert_eq!(log.len(), 5, "five decisions, none per frame: {log:?}");
    let h = p.u.now;
    let cut = h + 300_000_000;
    p.u.settle(cut);
    let want = p.u.digest();
    for rtfs in [&[7.0][..], &[1e4, 1.0, 300.0][..]] {
        let mut q = plane(Config::default(), 4, Order::Sparse, 1, 8).unwrap();
        for &(t, w) in &log {
            q.u.schedule(t, w).unwrap();
        }
        let mut f = 0;
        while q.u.now < h && f < 2_000_000 {
            q.u.frame_to(1.0 / 41.0, rtfs[f % rtfs.len()], Budget::events(9), h);
            f += 1;
        }
        q.u.settle(cut);
        assert_eq!(q.u.inputs, log, "a decision moved or was dropped at {rtfs:?}");
        assert_eq!(q.u.digest(), want, "the time factor changed the universe ({rtfs:?})");
    }
}

#[test]
fn the_view_shows_the_throttle_and_the_two_frames() {
    let mut p = plane(Config::default(), 2, Order::Sparse, 1, 8).unwrap();
    p.u.input(0, word(1, 12)).unwrap();
    for _ in 0..40 {
        p.u.frame(1.0 / 60.0, 100.0, Budget::unlimited());
    }
    let v = gather(&p.u, &p.names).unwrap();
    assert_eq!((v.level, v.burning, v.refusals), (12, true, 0));
    // In Home's doll, the velocity against the doll's centre differs from the one against the star by the planet's own (1e-4 c).
    let (b, bd) = ((v.beta[0].powi(2) + v.beta[1].powi(2)).sqrt(), (v.doll_beta[0].powi(2) + v.doll_beta[1].powi(2)).sqrt());
    println!("doll {}: star frame β {b:.6} rate {:.9}; doll frame β {bd:.6} rate {:.9}", v.doll, v.rate, v.doll_rate);
    assert_eq!(v.doll, "Home");
    assert!((b - bd).abs() > 1e-5 && bd > 0.0 && (v.rate - v.doll_rate).abs() < 1e-3 && v.rate < 1.0 && v.doll_rate < 1.0);
    // The rate is the clock's: close to 1/γ in the star's frame, once the burn is large.
    let g = 1.0 / (1.0 - b * b).sqrt();
    assert!((v.rate * g - 1.0).abs() < 1e-4, "rate {} against 1/γ {}", v.rate, 1.0 / g);
}

/// A lost ship says why and keeps its readings (proper time, β, rate) instead of zeros: here an impact, the body and the speed
/// in words. (The edge and the engine's own refusal are worded by the same function; the page's loss report is flown in the
/// browser.)
#[test]
fn a_lost_ship_says_why_and_keeps_its_readings() {
    let mut p = plane(Config::default(), 1, Order::Sparse, 1, 48).unwrap();
    p.u.frame(0.1, 800.0, Budget::unlimited());
    // Reverse: against the orbit's motion, the burn that brings a ship down into the planet (forward is prograde).
    p.u.input(p.u.now, word(2, 4)).unwrap();
    let mut last_b = 0.0;
    for _ in 0..3000 {
        p.u.frame(0.1, 800.0, Budget::unlimited());
        let v = gather(&p.u, &p.names).expect("a lost or stuck ship is still a view");
        let b = (v.beta[0].powi(2) + v.beta[1].powi(2)).sqrt();
        if !v.alive {
            let loss = v.loss.clone().expect("a wreck says why");
            println!("lost: {loss}; β {b:.9}, proper {:.1} s, rate {:.9}", v.proper_seconds, v.rate);
            assert!(loss.starts_with("hit Home at ") && loss.contains("km/s"), "{loss}");
            assert!(v.proper_seconds > 0.0 && b > 0.0 && v.rate < 1.0, "the readings are frozen at the last state, not zero");
            assert!(last_b > 0.0);
            return;
        }
        last_b = b;
    }
    panic!("the ship should have crashed");
}

/// A ship the engine could not carry on (a refused kick: stopping dead above a planet is a radial plunge, which the compile
/// refuses, kick after kick) stays viewable, alive: the view reads its last state when the presented tick cannot be read.
#[test]
fn a_stuck_ship_keeps_a_view() {
    let mut p = plane(Config::default(), 5, Order::Sparse, 1, 8).unwrap();
    p.u.settle(2_000_000);
    p.u.input(2_000_000, word(2, 14)).unwrap(); // reverse: brake against the orbit's motion
    p.u.settle(2_300_000);
    p.u.now = 2_300_000;
    let v = gather(&p.u, &p.names).expect("a stuck ship is still a view");
    let rec = p.u.rec(p.player);
    println!("stuck: {} refusals, alive {}, β {:?}, loss {:?}", rec.refusals, rec.alive, v.beta, v.loss);
    assert!(rec.refusals > 0, "the scene must refuse (the engine's radial-fall limit)");
    assert!(v.refusals > 0 && v.proper_seconds > 0.0);
}

/// Julien's goal is to feel high c: a ship burning at the top level from the plane's start reaches β 0.999 (γ ≈ 22) with
/// no refusal and no loss, whatever step law carries it. (The motion law v2 refused at β ≈ 0.05: its energy register was a
/// 64-bit word sized for orbital energies, and the first step after a handoff into the root doll ignored a held burn, so the
/// burn came in one lump and the velocity left its word.) Frozen before the run; the engine's own events keep up with the
/// presented tick all along (no wall budget: the outcome is the engine's, not the clock's).
#[test]
fn a_ship_burning_at_the_top_level_reaches_beta_0_999_without_a_refusal() {
    let mut p = plane(Config::default(), 1, Order::Sparse, 1, 48).unwrap();
    p.u.input(0, word(1, 15)).unwrap();
    let mut best = 0.0f64;
    for _ in 0..3000 {
        p.u.frame(0.1, 800.0, Budget::unlimited());
        let v = gather(&p.u, &p.names).unwrap();
        let b = (v.beta[0].powi(2) + v.beta[1].powi(2)).sqrt();
        assert!(v.alive && v.refusals == 0, "refused or lost at β {b}: {:?} ({} refusals)", v.loss, v.refusals);
        let last_event = p.u.rec(p.player).b.event_time;
        assert!(p.u.now - last_event < 1 << 24, "the engine's last event ({last_event}) lags the presented tick {}: a burn held in one lump", p.u.now);
        best = best.max(b);
        if b >= 0.999 {
            return;
        }
    }
    panic!("the ship only reached β {best}");
}
