//! Cost of a battle on the three steppers, measured the way the player runs it: a busy fanless
//! M1 where heat and load are part of the number, so the machine's state is printed before and
//! after each block. Lockstep on the CPU (`Chronon`), sparse (`EventCore`), lockstep on the GPU
//! (`MetalChronon`): the same battle in the same frame, the same digests (asserted), and three costs.
//!
//! Reported per scene and stepper: wall time of the whole battle (median and p99 over the repeats:
//! with fewer than 100 repeats the p99 is the worst one), the same per 1,000 chronons, and the
//! latency of one epoch segment (`run_to` the next epoch: the frame's unit of work, the nearest thing
//! to a frame time) with its p50 and p99 over all segments of all repeats. Construction (`setup`) is
//! timed apart: a `MetalChronon` compiles its shaders when built. A game-second is 1.2·10^10
//! chronons (docs/universe-quanta.md: δt = 83 ps), so these scenes, whose ships are one light-chronon
//! wide, are stress scales and every real-time factor is tiny: the comparison is between steppers.
//!
//! Scenes: the engine's cost scenes (`cost.rs`: 2000 bodies, three epochs), the same battle with
//! re-anchoring (`reanchor.rs` cost scene), a sweep of body counts over `scenes::battle` (dense
//! battles: where the GPU should win), and sparse ones (formations that barely meet, or never: where
//! the event core should win), and the range where the GPU path lets go (large Q). Each test stays under
//! one minute; run them one at a time (`-- --test-threads=1`), since they measure each other's load.
#![cfg(target_os = "macos")]
use emergent_engine::{scenes, AnchorPolicy, Battle, Frame, Outcome};
use emergent_lattice::law::{Tick, World};
use emergent_lattice::{chronon::Chronon, Kickable, Stepper};
use emergent_lattice_event::EventCore;
use emergent_lattice_metal::{MetalChronon, MetalError};
use std::process::Command;
use std::time::Instant;

fn sh(cmd: &str, args: &[&str]) -> String {
    Command::new(cmd).args(args).output().map(|o| String::from_utf8_lossy(&o.stdout).trim().replace('\n', "; ")).unwrap_or_default()
}

fn machine_state(when: &str) {
    println!(
        "machine {when}: {} | {} | {} | {} | {}",
        sh("uptime", &[]).split("load averages:").last().map(|l| format!("load{}", l.trim_end())).unwrap_or_default(),
        sh("sysctl", &["-n", "vm.swapusage"]),
        sh("pmset", &["-g", "therm"]).lines().next().unwrap_or(""),
        sh("pmset", &["-g", "batt"]).lines().next().unwrap_or(""),
        sh("sysctl", &["-n", "machdep.cpu.brand_string"]),
    );
}

/// How long to repeat a battle: until `budget` seconds have passed and `min` repeats are done, or `max`.
#[derive(Clone, Copy)]
struct Reps {
    budget: f64,
    min: usize,
    max: usize,
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum Order {
    Lockstep,
    Sparse,
    Gpu,
}

impl Order {
    fn name(self) -> &'static str {
        match self {
            Order::Lockstep => "lockstep",
            Order::Sparse => "sparse",
            Order::Gpu => "gpu",
        }
    }
}

struct Cell {
    setup: Vec<f64>,
    wall: Vec<f64>,
    /// Every epoch segment but the first (steady state).
    seg: Vec<f64>,
    /// The first epoch segment of each battle: the stepper's cold start (the GPU's first command
    /// buffers, the event core's genesis indexing).
    first: Vec<f64>,
    out: Outcome,
    contacts: u64,
    reps: usize,
    /// The epoch kicks' hooks of the last repeat, ns per body-epoch: reading the motions, and applying the kicks.
    read_ns: f64,
    apply_ns: f64,
}

fn quantile(v: &[f64], p: f64) -> f64 {
    let mut s = v.to_vec();
    s.sort_by(|a, b| a.partial_cmp(b).unwrap());
    s[((p * s.len() as f64).ceil() as usize).clamp(1, s.len()) - 1]
}

/// Repeat one battle as `reps` says.
fn measure<S: Kickable>(mk: &dyn Fn() -> S, f: &Frame, horizon: Tick, anchor: Option<AnchorPolicy>, reps: Reps) -> Cell {
    let e = f.epoch();
    let started = Instant::now();
    let mut c = Cell { setup: vec![], wall: vec![], seg: vec![], first: vec![], out: Outcome { world: String::new(), log: String::new(), tide: String::new() }, contacts: 0, reps: 0, read_ns: 0.0, apply_ns: 0.0 };
    loop {
        let t0 = Instant::now();
        let mut b = Battle::new(mk(), f.clone(), 1);
        if let Some(p) = anchor {
            b = b.with_anchoring(p).unwrap();
        }
        c.setup.push(t0.elapsed().as_secs_f64());
        let run = Instant::now();
        let mut at = 0;
        while at < horizon {
            at = (at + e).min(horizon);
            let t = Instant::now();
            b.run_to(at).unwrap();
            let dt = t.elapsed().as_secs_f64();
            if at <= e {
                c.first.push(dt);
            } else {
                c.seg.push(dt);
            }
        }
        c.wall.push(run.elapsed().as_secs_f64());
        let out = b.outcome();
        let (st, n) = (b.stats(), b.carries().len() as f64);
        (c.read_ns, c.apply_ns) = (st.read_ns as f64 / (st.epochs as f64 * n), st.apply_ns as f64 / (st.epochs as f64 * n));
        if c.reps > 0 {
            assert_eq!(out, c.out, "a repeat must give the same bits");
        }
        (c.out, c.contacts, c.reps) = (out, b.stepper().log().contacts, c.reps + 1);
        if c.reps >= reps.max || (c.reps >= reps.min && started.elapsed().as_secs_f64() >= reps.budget) {
            return c;
        }
    }
}

fn run_order(order: Order, w: &World, f: &Frame, horizon: Tick, anchor: Option<AnchorPolicy>, reps: Reps) -> Option<Cell> {
    Some(match order {
        Order::Lockstep => measure(&|| Chronon::new(w.clone(), false).unwrap(), f, horizon, anchor, reps),
        Order::Sparse => measure(&|| EventCore::new(w.clone(), false).unwrap(), f, horizon, anchor, reps),
        Order::Gpu => {
            if matches!(MetalChronon::new(w.clone(), false), Err(MetalError::NoDevice)) {
                eprintln!("skip: no Metal device");
                return None;
            }
            measure(&|| MetalChronon::new(w.clone(), false).expect("metal"), f, horizon, anchor, reps)
        }
    })
}

/// One scene on the three steppers: prints a row each, asserts the same bits, returns the median walls.
fn scene(label: &str, w: &World, f: &Frame, horizon: Tick, anchor: Option<AnchorPolicy>, reps: Reps) -> Option<[f64; 3]> {
    let mut med = [0.0; 3];
    let mut hooks = String::new();
    let mut first: Option<Cell> = None;
    for (i, order) in [Order::Lockstep, Order::Sparse, Order::Gpu].into_iter().enumerate() {
        let c = run_order(order, w, f, horizon, anchor, reps)?;
        med[i] = quantile(&c.wall, 0.5);
        println!(
            "{label:<24} {:<8} x{:<2} setup {:>3.0} ms | battle {:>8.1} ms med {:>8.1} p99 | {:>8.1} ms/1000 chronons | epoch segment {:>7.0} us p50 {:>7.0} us p99, first {:>7.0} us | {} contacts",
            order.name(),
            c.reps,
            quantile(&c.setup, 0.5) * 1e3,
            med[i] * 1e3,
            quantile(&c.wall, 0.99) * 1e3,
            med[i] * 1e6 / horizon as f64,
            quantile(&c.seg, 0.5) * 1e6,
            quantile(&c.seg, 0.99) * 1e6,
            quantile(&c.first, 0.5) * 1e6,
            c.contacts
        );
        hooks += &format!(" {} {:.1}+{:.1}", order.name(), c.read_ns, c.apply_ns);
        match &first {
            None => first = Some(c),
            Some(a) => assert_eq!(a.out, c.out, "{label}: {} and lockstep give the same bits", order.name()),
        }
    }
    println!("{label:<24} kick hooks, ns per body-epoch (read + apply):{hooks}");
    Some(med)
}

/// A battle in a frame of mean motion 2^-k whose radius satisfies the extent rule over the horizon
/// (as the tests of this crate do).
fn frame_for(w_extent: i64, q: i64, div: i64, horizon: Tick, k: u32) -> Frame {
    let r_orbit = (q << k) / 4;
    let r_extent = 32 * (w_extent + 4 * horizon * (q / div));
    Frame::new(q, r_orbit.max(r_extent), 1u64 << (60 - k)).unwrap()
}

fn warm_up() {
    // The GPU wakes at its own pace: one short battle first, as a player's second battle would.
    let (w, _) = scenes::battle(400, 1024, 3, 8, false);
    if let Ok(mut m) = MetalChronon::new(w, false) {
        m.run_to(300);
    }
}

#[test]
fn cost_scenes_2000_bodies_three_epochs() {
    machine_state("before");
    warm_up();
    const H: Tick = 4096;
    let (n, q) = (2000u64, 1024i64);
    let (w, extent) = scenes::battle(n, q, 8, 8, false);
    println!("cost.rs scene: {n} bodies, q = {q}, horizon {H} chronons, non-formation, closing at q/4 per chronon");
    for k in [13u32, 11, 9] {
        let f = frame_for(extent, q, 8, H, k);
        scene(&format!("E = {} (nT {:.2})", f.epoch(), f.n_f64() * H as f64), &w, &f, H, None, Reps { budget: 3.5, min: 3, max: 9 });
    }
    machine_state("after");
}

#[test]
fn cost_of_the_same_battle_with_re_anchoring() {
    machine_state("before");
    warm_up();
    const H: Tick = 4096;
    let (n, q) = (2000u64, 1024i64);
    let (w, extent) = scenes::battle(n, q, 8, 8, false);
    let f = frame_for(extent, q, 8, H, 11);
    let policy = AnchorPolicy { age_epochs: 16, enforce_orbit_rule: false };
    println!("reanchor.rs cost scene: {n} bodies, E = {}, an anchor every 16 epochs (a re-anchor is a rebase of every body)", f.epoch());
    scene("with re-anchors", &w, &f, H, Some(policy), Reps { budget: 6.0, min: 3, max: 9 });
    scene("without", &w, &f, H, None, Reps { budget: 6.0, min: 3, max: 9 });
    machine_state("after");
}

/// n bodies closing at 2q/`div` per chronon, tide epoch 32. Contacts start at about chronon 40·div/2.
fn sweep(what: &str, ns: &[u64], div: i64, horizon: Tick, budget: f64, min: usize) {
    machine_state("before");
    warm_up();
    let q = 1024i64;
    println!("{what}: scenes::battle(n, q = {q}, seed 8, div {div}), horizon {horizon} chronons, E = 32");
    for &n in ns {
        let (w, extent) = scenes::battle(n, q, 8, div, false);
        let f = frame_for(extent, q, div, horizon, 11);
        if scene(&format!("{n} bodies"), &w, &f, horizon, None, Reps { budget, min, max: 15 }).is_none() {
            return;
        }
    }
    machine_state("after");
}

#[test]
fn sweep_small_battles() {
    sweep("dense sweep, small", &[50, 200, 800], 8, 1024, 2.5, 3);
}

#[test]
fn sweep_large_battles() {
    sweep("dense sweep, large", &[4_000, 8_000, 16_000, 64_000], 8, 512, 2.0, 1);
}

/// Faster fleets (closing at q per chronon, half the light speed each): every body meets many
/// others and bounces again and again.
#[test]
fn sweep_dense_fast_battles() {
    sweep("dense and fast", &[2_000, 16_000, 64_000], 2, 256, 2.0, 1);
}

/// Sparse battles: formations closing slowly (div 32) over 4096 chronons meet for a short while
/// (the tail of `s5`); at div 64 they do not meet in 1024 chronons at all.
#[test]
fn sparse_battles() {
    machine_state("before");
    warm_up();
    let q = 1024i64;
    for (n, div, horizon, what) in [(2000u64, 32i64, 4096 as Tick, "formations meeting late"), (2000, 64, 1024, "formations that never meet"), (16_000, 64, 1024, "formations that never meet")] {
        let (w, extent) = scenes::battle(n, q, 6, div, true);
        let f = frame_for(extent, q, div, horizon, 11);
        println!("sparse: {n} bodies, {what}, closing at q/{} per chronon, horizon {horizon}", div / 2);
        scene(&format!("{n} bodies, div {div}"), &w, &f, horizon, None, Reps { budget: 3.0, min: 3, max: 9 });
    }
    machine_state("after");
}

/// Where the GPU path lets go: its exactness ranges need C·(K + 1) ≤ 2^28 (cell side C, fastest
/// body K, in velocity quanta per chronon), so at a large Q any body near a fraction of c sends the
/// whole battle to the CPU path of `MetalChronon` (exact, tested, and not fast). The same battle
/// (closing at q/4 per chronon) at growing Q: the chronons the GPU ran, those it handed to the CPU,
/// and the wall time against the CPU lockstep.
#[test]
fn the_gpu_path_needs_small_velocities() {
    machine_state("before");
    warm_up();
    const H: Tick = 192;
    println!("400 bodies closing at q/4 per chronon, {H} chronons: the GPU path needs C*(K+1) <= 2^28");
    for lg in [10u32, 13, 14, 15, 16, 18, 20] {
        let q = 1i64 << lg;
        let (w, extent) = scenes::battle(400, q, 8, 8, false);
        let f = frame_for(extent, q, 8, H, 11);
        let reps = Reps { budget: 1.5, min: 2, max: 5 };
        let a = measure(&|| Chronon::new(w.clone(), false).unwrap(), &f, H, None, reps);
        let g = measure(
            &|| match MetalChronon::new(w.clone(), false) {
                Ok(m) => m,
                Err(e) => panic!("{e}"),
            },
            &f,
            H,
            None,
            reps,
        );
        // One more run to read the stepper's own count of where its chronons went.
        let mut b = Battle::new(MetalChronon::new(w.clone(), false).unwrap(), f.clone(), 1);
        b.run_to(H).unwrap();
        let s = b.stepper().stats().clone();
        assert_eq!(a.out, g.out, "Q = 2^{lg}: the CPU path and the GPU path give the same bits");
        println!(
            "Q = 2^{lg:<2}: GPU ran {:>4} chronons, CPU path {:>4} | lockstep {:>8.1} ms, metal {:>8.1} ms ({:.2}x)",
            s.gpu_chronons,
            s.cpu_chronons,
            quantile(&a.wall, 0.5) * 1e3,
            quantile(&g.wall, 0.5) * 1e3,
            quantile(&a.wall, 0.5) / quantile(&g.wall, 0.5)
        );
    }
    machine_state("after");
}
