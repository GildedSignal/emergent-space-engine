//! The belt bet's first wall: what one presented frame costs as the body count N grows, on the
//! shipped universe, with the events held at belt-like cadence (≈0 per frame). The restricted
//! scene (a star, a planet, N ships on circular orbits), built through the public API so ships
//! carry radii (the exact player-neighbourhood check skips zero-reach pairs). Measured, per N:
//! the whole frame, a scheduling-only advance (`Budget::events(0)`: the deadline rekey sweep
//! plus the defer/requeue of every far entity, no events), `rekey` alone, and
//! `PlayerNeighbourhood::find` alone (one player item's neighbourhood scan). Digest control:
//! frames at two budgets, settled to one horizon, must give one digest.
//!
//!     cargo run -p emergent-universe --release --offline --example nwall -- [ns] [rtf] [stride] [seconds]
//!     cargo run -p emergent-universe --release --offline --example nwall -- control
use emergent_space::orbit::Scalar;
use emergent_universe::encounter::{Encounters, PlayerNeighbourhood};
use emergent_universe::scenario::{AU, STAR_RADIUS};
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Budget, Kind, Mass, OrbitSpec, Universe};
use std::time::Instant;

fn pct(v: &mut [f64], p: f64) -> f64 {
    v.sort_by(|a, b| a.total_cmp(b));
    v[((p * v.len() as f64) as usize).min(v.len() - 1)]
}

fn sh(cmd: &str, args: &[&str]) -> String {
    std::process::Command::new(cmd)
        .args(args)
        .output()
        .map(|o| String::from_utf8_lossy(&o.stdout).trim().replace('\n', " | "))
        .unwrap_or_default()
}

/// The restricted scene built by hand: star, planet (2^-10 of the total), N ships on circular
/// orbits through a `stride`-spread annulus of ±0.48 sep, radius 1 root unit.
fn scene(n: u64, stride: u64) -> Universe {
    let mut u = Universe::new(Scalar::integer(STAR_RADIUS), Default::default());
    u.threads = 1;
    // The motion tests' own restricted problem: planet 2^-10 of the total, sep 527e6 root units,
    // planet radius 49_000 root units (the same numbers `crates/universe/tests/motion.rs` uses).
    let mu = Mass::from(-10i32);
    let sep = 527_000_000i64;
    let planet = u
        .add_body(
            Kind::Planet,
            OrbitSpec { doll: 0, periapsis: Scalar::integer(sep), e_q48: 0, clockwise: false, angle: 0, phase: 0 },
            Scalar::ZERO,
        )
        .expect("planet");
    let surface = Scalar::raw(49_000, -mu.octave).expect("surface");
    u.add_doll("planet", planet, mu, surface).expect("doll");
    let radius = Scalar::integer(1); // 1 root unit ≈ 1.5 km: the neighbourhood check sees every pair
    for i in 0..n {
        let r = sep + ((i as i64 % 256) - 128) * 2_000_000;
        u.add_body(
            Kind::Ship,
            OrbitSpec {
                doll: 0,
                periapsis: Scalar::integer(r),
                e_q48: 0,
                clockwise: false,
                angle: i.wrapping_mul(stride) as u32,
                phase: 0,
            },
            radius,
        )
        .expect("ship");
    }
    u.start().expect("start");
    u
}

fn main() {
    let a: Vec<String> = std::env::args().skip(1).collect();
    if a.first().map(|s| s.as_str()) == Some("control") {
        return control();
    }
    let ns: Vec<u64> = a
        .first()
        .map(|s| s.split(',').map(|x| x.parse().unwrap()).collect())
        .unwrap_or_else(|| vec![100, 1_000, 10_000, 100_000]);
    let rtf: f64 = a.get(1).map(|s| s.parse().unwrap()).unwrap_or(100.0);
    let stride: u64 = a.get(2).map(|s| s.parse().unwrap()).unwrap_or(2_654_435_761);
    let seconds: f64 = a.get(3).map(|s| s.parse().unwrap()).unwrap_or(3.0);
    println!(
        "nwall: {seconds} s of frames at 60 Hz, rtf {rtf}, stride {stride}, 1 thread; load before: {}",
        sh("uptime", &[])
    );
    println!("| n | frame us p50/p99/max | sched-only us p50 | rekey us p50 | events | find us p50 (hits) | build s |");
    println!("|---|---|---|---|---|---|---|");
    let want = (rtf / 60.0 / TICK_SECONDS) as i64;
    for n in ns {
        let t0 = Instant::now();
        let mut u = scene(n, stride);
        let build_s = t0.elapsed().as_secs_f64();
        let frames = (seconds * 60.0) as usize;
        let mut per = Vec::with_capacity(frames);
        let ev0 = u.stats.events();
        for _ in 0..frames {
            let target = u.now + want.max(1);
            let t = Instant::now();
            let adv = u.advance(target, Budget::unlimited());
            u.now = adv.horizon.max(u.now);
            per.push(t.elapsed().as_secs_f64() * 1e6);
        }
        let events = u.stats.events() - ev0;
        let mut sched = Vec::new();
        for _ in 0..10 {
            let t = Instant::now();
            u.advance(u.now + 1, Budget::events(0));
            sched.push(t.elapsed().as_secs_f64() * 1e6);
        }
        let mut rk = Vec::new();
        for _ in 0..10 {
            let t = Instant::now();
            u.rekey();
            rk.push(t.elapsed().as_secs_f64() * 1e6);
        }
        let ctx = u.ctx();
        let mut fnd = Vec::new();
        for _ in 0..3 {
            let t = Instant::now();
            let found = PlayerNeighbourhood.find(&ctx, 2, u.now, want.max(1));
            let us = t.elapsed().as_secs_f64() * 1e6;
            fnd.push((us, found.len() as u64));
        }
        drop(ctx);
        let hits = fnd.iter().map(|f| f.1).max().unwrap_or(0);
        println!(
            "| {n} | {:.0}/{:.0}/{:.0} | {:.0} | {:.0} | {events} | {:.0} ({hits}) | {build_s:.1} |",
            pct(&mut per, 0.5),
            pct(&mut per, 0.99),
            pct(&mut per, 1.0),
            pct(&mut sched, 0.5),
            pct(&mut rk, 0.5),
            fnd.iter().map(|f| f.0).sum::<f64>() / fnd.len() as f64,
        );
    }
    println!("load after: {}", sh("uptime", &[]));
}

/// Frames never change outcomes: one universe settled straight to a horizon, another run through
/// frames at two budgets first, both then settled to the same horizon — one digest or the
/// harness is void. Also prints the events the deep settle resolves (a vacuous control, with no
/// events between the budgets, is reported as such).
fn control() {
    let stride = 2_654_435_761u64;
    let horizon: i64 = 1 << 40;
    let mut a = scene(200, stride);
    a.settle(horizon);
    let da = a.digest();
    let eva = a.stats.events();
    let want = (100.0f64 / 60.0 / TICK_SECONDS) as i64;
    let mut b = scene(200, stride);
    for _ in 0..120 {
        // unlimited budget
        let target = b.now + want.max(1);
        let adv = b.advance(target, Budget::unlimited());
        b.now = adv.horizon.max(b.now);
    }
    for _ in 0..120 {
        // one event at a time, to the same target
        let target = b.now + want.max(1);
        loop {
            let adv = b.advance(target, Budget::events(1));
            if adv.events == 0 {
                break;
            }
        }
        b.now = target.max(b.now);
    }
    b.settle(horizon);
    let db = b.digest();
    println!("control: events settled {eva}, digests {} {} ({})", da, db, if da == db { "EQUAL" } else { "DIFFER" });
}
