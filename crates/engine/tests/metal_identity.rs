//! Bit-identity of the dense order on the GPU: the same battle in a free-fall frame, evaluated in
//! lockstep on the CPU (`Chronon`, the reference), sparse (`EventCore`) and lockstep on the M1's
//! GPU (`MetalChronon`), gives the same world digest, the same log digest and the same tide digest
//! (carries, epochs, counters, tube, hand-offs), and the same frame counters.
//!
//! Every scene of `identity.rs` (s0..s7: valid frames down to a storm that refuses kicks to c)
//! and of `reanchor.rs` (r0..r4: re-anchors, members handed out, anchors refused in a storm; the
//! genesis re-anchor; outliers; a frame that dissolves; a wide group that sheds members; five
//! particles over periods) runs on all three, with and without re-anchoring, at 1, 4 and 8 kick
//! threads. Planted laws (a kick or an anchor one chronon late) must break the equality and agree
//! again in every order when they are planted in every order. The GPU also matches the CPU
//! chronon's metrics (`ops`, `predicates`, `fired`, `batches`): it tests exactly the same pairs.
//!
//! Skips (prints) when the machine has no Metal device. Each test is one scene, under one minute.
#![cfg(target_os = "macos")]
use emergent_engine::{scenes, AnchorPolicy, Battle, BattleStats, Frame, Outcome};
use emergent_lattice::law::{Body, Law, Response, Tick, World};
use emergent_lattice::{chronon::Chronon, Kickable, Stepper};
use emergent_lattice_event::EventCore;
use emergent_lattice_metal::{MetalChronon, MetalError};
use std::time::Instant;

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
enum Order {
    Lockstep,
    Sparse,
    Gpu,
}

/// How a run is driven: the frame, the threads of the kick pass, planted shifts, and the anchoring.
#[derive(Clone)]
struct Drive {
    threads: usize,
    /// Every epoch kick applied this many chronons late (planted).
    kick_shift: Tick,
    /// `Some(policy)` turns re-anchoring on, with its planted lateness.
    anchor: Option<(AnchorPolicy, Tick)>,
    horizon: Tick,
}

impl Drive {
    fn new(horizon: Tick) -> Drive {
        Drive { threads: 1, kick_shift: 0, anchor: None, horizon }
    }
    fn threads(&self, threads: usize) -> Drive {
        Drive { threads, ..self.clone() }
    }
    fn late_kicks(&self) -> Drive {
        Drive { kick_shift: 1, ..self.clone() }
    }
    fn late_anchors(&self) -> Drive {
        Drive { anchor: self.anchor.map(|(p, _)| (p, 1)), ..self.clone() }
    }
}

struct Run {
    out: Outcome,
    /// The frame's counters (the timings of `BattleStats` are left out).
    counters: [i128; 7],
    contacts: u64,
    secs: f64,
    active: Vec<bool>,
    /// The stepper's `ops, predicates, fired, batches, max_batch`.
    metrics: [u64; 5],
    stats: BattleStats,
}

fn counters(s: &BattleStats) -> [i128; 7] {
    [s.epochs as i128, s.changed as i128, s.refused as i128, s.max_r2, s.anchors as i128, s.handed_out as i128, s.anchors_refused as i128]
}

fn battle<S: Kickable>(s: S, f: &Frame, d: &Drive) -> Run {
    let t = Instant::now();
    let mut b = Battle::new(s, f.clone(), d.threads).with_epoch_shift(d.kick_shift);
    if let Some((policy, shift)) = d.anchor {
        b = b.with_anchoring(policy).unwrap().with_anchor_shift(shift);
    }
    b.run_to(d.horizon).unwrap();
    let secs = t.elapsed().as_secs_f64();
    let m = b.stepper().metrics();
    Run {
        out: b.outcome(),
        counters: counters(b.stats()),
        contacts: b.stepper().log().contacts,
        secs,
        active: b.active().to_vec(),
        metrics: [m.ops, m.predicates, m.fired, m.batches, m.max_batch],
        stats: b.stats().clone(),
    }
}

/// One run, or None when the order is the GPU and the machine has none.
fn run(order: Order, w: &World, f: &Frame, d: &Drive) -> Option<Run> {
    Some(match order {
        Order::Lockstep => battle(Chronon::new(w.clone(), false).unwrap(), f, d),
        Order::Sparse => battle(EventCore::new(w.clone(), false).unwrap(), f, d),
        Order::Gpu => match MetalChronon::new(w.clone(), false) {
            Ok(m) => battle(m, f, d),
            Err(MetalError::NoDevice) => {
                eprintln!("skip: no Metal device");
                return None;
            }
            Err(e) => panic!("{e}"),
        },
    })
}

/// The scene's three runs agree on everything the contract shows (the sparse core's metrics count
/// other work, so they are compared between the two lockstep orders only).
fn same(name: &str, what: &str, a: &Run, b: &Run, metrics: bool) {
    assert_eq!(a.out, b.out, "{name}: {what}: world, log and tide digests");
    assert_eq!(a.counters, b.counters, "{name}: {what}: the frame's counters");
    assert_eq!(a.contacts, b.contacts, "{name}: {what}: contacts");
    assert_eq!(a.active, b.active, "{name}: {what}: who is still in the frame");
    if metrics {
        assert_eq!(a.metrics, b.metrics, "{name}: {what}: ops, predicates, fired, batches, max_batch");
    }
}

/// The three orders on one scene, and what must hold around them. Returns the reference run.
fn three_orders(name: &str, w: &World, f: &Frame, d: &Drive, sweep_threads: bool) -> Option<Run> {
    let a = run(Order::Lockstep, w, f, d)?;
    let b = run(Order::Sparse, w, f, d)?;
    let g = run(Order::Gpu, w, f, d)?;
    println!(
        "{name:<4} {:>5} bodies E={:<5} | {} epochs, {} kicked, {} refused, {} anchors (refused {}), {} handed out | contacts {:<7} | lockstep {:.2}s sparse {:.2}s gpu {:.2}s | digest {}",
        w.bodies.len(),
        f.epoch(),
        a.stats.epochs,
        a.stats.changed,
        a.stats.refused,
        a.stats.anchors,
        a.stats.anchors_refused,
        a.stats.handed_out,
        a.contacts,
        a.secs,
        b.secs,
        g.secs,
        &a.out.world[..12]
    );
    same(name, "sparse against lockstep", &a, &b, false);
    same(name, "gpu against lockstep", &a, &g, true);
    same(name, "gpu against sparse", &b, &g, false);
    if sweep_threads {
        for threads in [4, 8] {
            let g = run(Order::Gpu, w, f, &d.threads(threads))?;
            same(name, &format!("gpu, {threads} kick threads"), &a, &g, true);
        }
    }
    Some(a)
}

/// A planted lateness breaks the equality with the on-time run and agrees again in every order.
fn planted(name: &str, w: &World, f: &Frame, d: &Drive, on_time: &Run, what: &str) {
    let late_lock = run(Order::Lockstep, w, f, d).unwrap();
    let Some(late_gpu) = run(Order::Gpu, w, f, d) else { return };
    assert_ne!(late_gpu.out, on_time.out, "{name}: {what} one chronon late on the GPU must differ from on time");
    assert_ne!(late_lock.out, on_time.out, "{name}: {what} one chronon late in lockstep must differ from on time");
    same(name, &format!("{what} late in both orders"), &late_lock, &late_gpu, true);
    let late_sparse = run(Order::Sparse, w, f, d).unwrap();
    same(name, &format!("{what} late in all three"), &late_sparse, &late_gpu, false);
}

// ---------------------------------------------------------------------------------------
// The scenes of identity.rs: the tide over the battle, no re-anchoring
// ---------------------------------------------------------------------------------------

const HORIZON: Tick = 4096;

struct Scene {
    name: &'static str,
    bodies: u64,
    q: i64,
    seed: u64,
    div: i64,
    formation: bool,
    /// Mean motion 2^-k rad per chronon.
    k: u32,
    /// The tide is so strong that kicks to c are refused.
    storm: bool,
}

/// As in `identity.rs`: n = 2^-k; the orbit radius is the largest the weak-field rule allows when
/// that also satisfies the extent rule over the horizon, else the extent rule's minimum.
fn build(s: &Scene) -> (World, Frame) {
    let (w, extent) = scenes::battle(s.bodies, s.q, s.seed, s.div, s.formation);
    let r_orbit = (s.q << s.k) / 4;
    let r_extent = 32 * (extent + 4 * HORIZON * (s.q / s.div));
    (w, Frame::new(s.q, r_orbit.max(r_extent), 1u64 << (60 - s.k)).unwrap())
}

fn tide_scene(s: Scene) {
    let (w, f) = build(&s);
    let d = Drive::new(HORIZON);
    let Some(a) = three_orders(s.name, &w, &f, &d, true) else { return };
    assert!(a.contacts > 0 && a.stats.epochs > 0, "{}: contacts and kicks must happen", s.name);
    assert!(!s.storm || a.stats.refused > 0, "{}: the storm must refuse kicks", s.name);

    // Control: without its kicks the same battle ends elsewhere, so the equality is about the tide.
    // (The frame about the non-rotating axes: `Frame::new` also turns the world from the co-rotating
    // axes at genesis, a change of coordinates and not a kick.)
    let inertial = Frame::on_orbit(s.q, f.radius(), f.n(), 0, 0, 0).unwrap();
    let unkicked = run(Order::Gpu, &w, &inertial, &Drive { kick_shift: HORIZON + 1, ..d.clone() }).unwrap();
    assert_eq!(unkicked.stats.epochs, 0);
    assert_ne!(unkicked.out.world, a.out.world, "{}: the tide must change the outcome", s.name);
    // B0, flat reduction: with the kicks pushed past the horizon, and with no parent mass (a flat
    // frame), the GPU's outcome is the plain lattice's.
    let mut plain = Chronon::new(w.clone(), false).unwrap();
    plain.run_to(HORIZON);
    assert_eq!((unkicked.out.world.clone(), unkicked.out.log.clone()), plain.outcome(), "{}: no kicks, the lattice's digests", s.name);
    let flat = run(Order::Gpu, &w, &Frame::flat(s.q).unwrap(), &d).unwrap();
    assert_eq!(flat.stats.epochs, 0, "{}: a flat frame never kicks", s.name);
    assert_eq!((flat.out.world.clone(), flat.out.log.clone()), plain.outcome(), "{}: no mass, the lattice's digests", s.name);

    planted(s.name, &w, &f, &d.late_kicks(), &a, "kicks");
}

macro_rules! tide_scenes {
    ($($fn_name:ident: $name:literal, $n:expr, $q:expr, $seed:expr, $div:expr, $form:expr, $k:expr, $storm:expr;)*) => {
        $(#[test] fn $fn_name() {
            tide_scene(Scene { name: $name, bodies: $n, q: $q, seed: $seed, div: $div, formation: $form, k: $k, storm: $storm });
        })*
    };
}

tide_scenes! {
    s0_valid_50_e256: "s0", 50, 1024, 1, 32, false, 16, false;
    s1_100_e128: "s1", 100, 1024, 2, 8, false, 15, false;
    s2_200_e64: "s2", 200, 512, 3, 8, false, 14, false;
    s3_formation_400_e32: "s3", 400, 1024, 4, 16, true, 13, false;
    s4_800_e16: "s4", 800, 2048, 5, 16, false, 12, false;
    s5_formation_1200_e8: "s5", 1200, 1024, 6, 32, true, 11, false;
    s6_1600_e4: "s6", 1600, 1024, 7, 32, false, 10, false;
    s7_storm_formation_2000_e1: "s7", 2000, 1024, 8, 8, true, 8, true;
}

// ---------------------------------------------------------------------------------------
// The scenes of reanchor.rs: re-anchors, hand-outs, refusals
// ---------------------------------------------------------------------------------------

struct AScene {
    name: &'static str,
    bodies: u64,
    q: i64,
    seed: u64,
    div: i64,
    formation: bool,
    k: u32,
    /// The frame's radius is the extent rule's divided by this, so members leave.
    squeeze: i64,
    /// Anchor every this many epochs.
    age: u64,
}

fn abuild(s: &AScene) -> (World, Frame) {
    let (w, extent) = scenes::battle(s.bodies, s.q, s.seed, s.div, s.formation);
    let r_orbit = (s.q << s.k) / 4;
    let r_extent = 32 * (extent + 4 * HORIZON * (s.q / s.div));
    let radius = if s.squeeze == 1 { r_orbit.max(r_extent) } else { (r_extent / s.squeeze).max(64) };
    (w, Frame::new(s.q, radius, 1u64 << (60 - s.k)).unwrap())
}

fn anchor_scene(s: AScene, expect_leavers: Option<bool>, expect_refused: bool) {
    let (w, f) = abuild(&s);
    let d = Drive { anchor: Some((AnchorPolicy { age_epochs: s.age, enforce_orbit_rule: false }, 0)), ..Drive::new(HORIZON) };
    let Some(a) = three_orders(s.name, &w, &f, &d, true) else { return };
    assert!(a.stats.anchors >= 3, "{}: re-anchors must happen: {}", s.name, a.stats.anchors);
    assert!(a.contacts > 0, "{}: contacts must happen", s.name);
    if let Some(leavers) = expect_leavers {
        assert_eq!(leavers, a.stats.handed_out > 0, "{}: members leave the frame iff the size rule breaks: {}", s.name, a.stats.handed_out);
    }
    assert_eq!(expect_refused, a.stats.anchors_refused > 0, "{}: anchors are refused (a velocity past c) only in a storm: {}", s.name, a.stats.anchors_refused);
    assert_eq!(a.stats.handed_out as usize + a.active.iter().filter(|&&x| x).count(), s.bodies as usize, "{}: the count is reported", s.name);
    // Control: the same battle in the same frame without re-anchoring ends elsewhere.
    let plain = run(Order::Gpu, &w, &f, &Drive::new(HORIZON)).unwrap();
    assert_ne!(plain.out.world, a.out.world, "{}: re-anchoring must change the outcome", s.name);
    planted(s.name, &w, &f, &d.late_anchors(), &a, "anchors");
}

macro_rules! anchor_scenes {
    ($($fn_name:ident: $name:literal, $n:expr, $q:expr, $seed:expr, $div:expr, $form:expr, $k:expr, $squeeze:expr, $age:expr, $leavers:expr, $refused:expr;)*) => {
        $(#[test] fn $fn_name() {
            anchor_scene(AScene { name: $name, bodies: $n, q: $q, seed: $seed, div: $div, formation: $form, k: $k, squeeze: $squeeze, age: $age }, $leavers, $refused);
        })*
    };
}

anchor_scenes! {
    r0_valid_200_e512: "r0", 200, 1024, 11, 32, false, 17, 1, 4, Some(false), false;
    r1_stress_400_e16: "r1", 400, 1024, 12, 16, true, 13, 1, 24, Some(false), false;
    r2_squeezed_400_e16: "r2", 400, 1024, 13, 16, false, 13, 8, 24, Some(true), false;
    r3_squeezed_formation_800_e8: "r3", 800, 2048, 14, 16, true, 12, 16, 32, Some(true), false;
    r4_storm_1200_e2: "r4", 1200, 1024, 15, 8, false, 10, 4, 64, None, true;
    r5_anchor_every_epoch_200_e512: "r5", 200, 1024, 11, 32, false, 17, 1, 1, Some(false), false;
}

// ---------------------------------------------------------------------------------------
// The hand-built scenes of reanchor.rs
// ---------------------------------------------------------------------------------------

const Q: i64 = 1 << 20;
const DR: i64 = 1 << 22;
const R: i64 = 1000 * DR;
const N: u64 = 1 << 46;

fn frame() -> Frame {
    Frame::new(Q, R, N).unwrap()
}

const REL: [(f64, f64); 5] = [(0.0, 0.0), (1.0, 0.6), (-0.8, -0.4), (0.4, 1.0), (-0.2, -0.8)];
const MASSES: [i64; 5] = [1, 2, 3, 1, 2];
const SPREAD: f64 = 0.05 * DR as f64;

/// Five test particles near a radial offset 1e-3·R, released at rest (no contacts: radius 1000, Pass).
fn particles() -> World {
    let bodies = REL
        .iter()
        .zip(MASSES)
        .enumerate()
        .map(|(i, (&(a, b), m))| Body::new(i as u64 + 1, [(1e-3 * R as f64 + SPREAD * a) as i64, (SPREAD * b) as i64], [0, 0], m, 1000, Response::Pass))
        .collect();
    World::new(Q, None, bodies).unwrap().with_law(Law::RelativisticV1).unwrap()
}

#[test]
fn five_particles_over_a_period_anchored_and_not() {
    // reanchor.rs runs ten periods (1.03 million chronons) on the event core. On the GPU a chronon
    // of five bodies costs a command buffer's dispatches (about 85 µs, measured), so this runs half a
    // period with an anchor every 8 epochs: anchors and the tube's rebindings are all exercised.
    let (w, f) = (particles(), frame());
    // The genesis re-anchor by hand (reanchor.rs: a_re_anchor_conserves_momentum_in_both_orders): the same report,
    // carries and motions in all three orders.
    let (a, b) = (genesis(Chronon::new(w.clone(), false).unwrap()), genesis(EventCore::new(w.clone(), false).unwrap()));
    assert_eq!(a, b, "sparse: the genesis re-anchor");
    let Ok(m) = MetalChronon::new(w.clone(), false) else { return };
    assert_eq!(a, genesis(m), "gpu: the genesis re-anchor");
    assert!(a.0.moved && !a.0.refused && a.0.handed_out.is_empty());
    let horizon = f.period() / 2;
    let policy = AnchorPolicy { age_epochs: 8, enforce_orbit_rule: true };
    for (label, d) in [("anchored", Drive { anchor: Some((policy, 0)), ..Drive::new(horizon) }), ("not anchored", Drive::new(horizon))] {
        let Some(a) = three_orders(&format!("5p {label}"), &w, &f, &d, label == "anchored") else { return };
        if label == "anchored" {
            assert!(a.stats.anchors >= 10, "anchors happen: {}", a.stats.anchors);
        }
    }
}

/// Eight members at rest: five within a few dr of each other (mass 4), three 50 to 80 dr out (mass 1).
fn outliers() -> World {
    let mut bodies = Vec::new();
    for (i, (x, y)) in [(1.0, 0.0), (2.0, 1.0), (0.5, -1.0), (1.5, 0.5), (0.0, 0.0)].iter().enumerate() {
        bodies.push(Body::new(i as u64 + 1, [(x * DR as f64) as i64, (y * DR as f64) as i64], [0, 0], 4, 1000, Response::Pass));
    }
    for (j, (x, y)) in [(60.0, 0.0), (-50.0, 20.0), (10.0, 80.0)].iter().enumerate() {
        bodies.push(Body::new(6 + j as u64, [(x * DR as f64) as i64, (y * DR as f64) as i64], [0, 0], 1, 1000, Response::Pass));
    }
    World::new(Q, None, bodies).unwrap().with_law(Law::RelativisticV1).unwrap()
}

type Genesis = (emergent_engine::AnchorReport, Vec<emergent_lattice::Motion>, Vec<[i64; 2]>, Vec<bool>, Outcome);

/// `reanchor()` at genesis, by hand, in any order: the report, the carries, the motions.
fn genesis<S: Kickable>(s: S) -> Genesis {
    let mut b = Battle::new(s, frame(), 1).with_anchoring(AnchorPolicy::default()).unwrap();
    let rep = b.reanchor().unwrap();
    let mut m = Vec::new();
    b.stepper().motions(&mut m);
    (rep, m, b.carries().to_vec(), b.active().to_vec(), b.outcome())
}

#[test]
fn members_outside_the_size_rule_leave_at_genesis_and_the_rest_goes_on() {
    let w = outliers();
    let a = genesis(Chronon::new(w.clone(), false).unwrap());
    let b = genesis(EventCore::new(w.clone(), false).unwrap());
    let Ok(m) = MetalChronon::new(w.clone(), false) else { return };
    let g = genesis(m);
    assert_eq!(a.0.handed_out, vec![5, 6, 7], "the three far bodies leave, the cluster stays");
    assert_eq!(a.0, b.0, "sparse: the same report");
    assert_eq!(a.0, g.0, "gpu: the same report, momentum and hand-outs included");
    assert_eq!((&a.1, &a.2, &a.3, &a.4), (&g.1, &g.2, &g.3, &g.4), "gpu: motions, carries, who leaves, digests after the re-anchor");
    assert_eq!(a.3, [true, true, true, true, true, false, false, false]);
    // And it goes on: the tide keeps the leavers out and the rest in (as reanchor.rs: 50 000 chronons).
    let d = Drive { threads: 1, anchor: Some((AnchorPolicy::default(), 0)), ..Drive::new(50_000) };
    let Some(x) = three_orders("outl", &w, &frame(), &d, true) else { return };
    assert!(x.stats.handed_out == 3 && x.active.iter().take(5).all(|&a| a));
}

#[test]
fn a_frame_whose_members_all_leave_dissolves_and_keeps_running() {
    // Two pairs 40 dr either side of their centre of mass: R/32 is 31 dr, so nobody is inside the
    // rule, nobody is left to recentre on, and all four are handed out where they stand.
    let bodies: Vec<Body> = [(40.0, 1.0), (40.0, -1.0), (-40.0, 0.5), (-40.0, -0.5)]
        .iter()
        .enumerate()
        .map(|(i, (x, y))| Body::new(i as u64 + 1, [(x * DR as f64) as i64, (y * DR as f64) as i64], [0, 0], 1, 1000, Response::Pass))
        .collect();
    let w = World::new(Q, None, bodies).unwrap().with_law(Law::RelativisticV1).unwrap();
    let a = genesis(Chronon::new(w.clone(), false).unwrap());
    let Ok(m) = MetalChronon::new(w.clone(), false) else { return };
    let g = genesis(m);
    assert_eq!(a.0.handed_out, vec![0, 1, 2, 3]);
    assert!(!a.0.moved && !a.0.refused);
    assert_eq!(a.0, g.0);
    assert_eq!((&a.1, &a.2, &a.3, &a.4), (&g.1, &g.2, &g.3, &g.4), "nothing moved, in either order");
    let horizon = frame().period() / 2;
    let d = Drive { anchor: Some((AnchorPolicy::default(), 0)), ..Drive::new(horizon) };
    let Some(x) = three_orders("dissolve", &w, &frame(), &d, false) else { return };
    assert!(x.stats.handed_out == 4 && x.active.iter().all(|&a| !a), "nothing is kicked once handed out");
}

#[test]
fn a_wide_group_sheds_members_as_the_tide_shears_it() {
    // Radial offsets spread over ±1 dr shear the group by about 70 dr a period between its extremes
    // (reanchor.rs spreads ±0.25 dr over 6 periods): members reach R/32 (31 dr) from the centre of
    // mass and leave one by one, at the anchors, while the rest keep going.
    let bodies: Vec<Body> = (0..12)
        .map(|i| Body::new(i as u64 + 1, [DR + (i as i64 - 6) * DR / 6, (i as i64 % 3 - 1) * DR / 50], [0, 0], 1 + i as i64 % 3, 1000, Response::Pass))
        .collect();
    let w = World::new(Q, None, bodies).unwrap().with_law(Law::RelativisticV1).unwrap();
    let d = Drive { anchor: Some((AnchorPolicy::default(), 0)), ..Drive::new(frame().period()) };
    let Some(x) = three_orders("wide", &w, &frame(), &d, false) else { return };
    assert!(x.stats.handed_out > 0 && x.active.iter().any(|&a| a) && x.active.iter().any(|&a| !a), "members leave one by one: {} handed out", x.stats.handed_out);
    println!("wide group after a period: {} of 12 handed out, {} anchors", x.stats.handed_out, x.stats.anchors);
}

// ---------------------------------------------------------------------------------------
// The independent judge's crowded scene (engine-judge E1), reproduced here and not imported
// ---------------------------------------------------------------------------------------

/// The judge's xorshift (xtask/src/engine_judge/scene.rs).
struct Xor(u64);

impl Xor {
    fn next(&mut self) -> u64 {
        self.0 ^= self.0 << 13;
        self.0 ^= self.0 >> 7;
        self.0 ^= self.0 << 17;
        self.0
    }
    fn range(&mut self, lo: i64, hi: i64) -> i64 {
        lo + (self.next() % (hi - lo + 1) as u64) as i64
    }
}

/// The judge's kind 0: 32 bouncers of radius 50 on a grid 130 apart, up to 230 quanta per chronon
/// in each axis, Q = 1024: 43 contacts fire in the first chronon, more than the 32 threads of the
/// one threadgroup that detects them. The GPU's detection once reported only the first 32 of them
/// (a kernel appending a threadgroup's hits strode by 256 whatever the group's size), so the
/// battle's first frame differed from the CPU's: E1 failed at "seed=1 kind=0 anchor=false
/// insertion=0 threads=1 order=metal sample=1" (6156/6480). Also the judge's seed 901, which failed too.
#[test]
fn the_judges_crowded_scene_gives_the_cpu_frames_on_the_gpu() {
    for seed in [1u64, 901] {
        let mut rng = Xor(seed + 0x91e1);
        let bodies: Vec<Body> = (0..32i64)
            .map(|i| {
                let (x, k) = ([(i % 8) * 130 - 450, (i / 8) * 130 - 180], [rng.range(-230, 230), rng.range(-230, 230)]);
                Body::new(i as u64 + 1, x, k, rng.range(1, 7), 50, Response::Bounce)
            })
            .collect();
        let w = World::new(1024, None, bodies).unwrap().with_law(Law::RelativisticV1).unwrap();
        // The judge's stress frame: epoch 16 chronons, nT = 1/8 (the world is first turned out of the
        // co-rotating axes, and kicked at tick 0, before the first chronon).
        let f = Frame::new(1024, 1 << 24, 1 << 50).unwrap();
        for anchored in [false, true] {
            let policy = anchored.then_some((AnchorPolicy { age_epochs: 4, enforce_orbit_rule: false }, 0));
            // The judge's checkpoints, each a battle of its own that stops there.
            for t in [0, 1, 15, 16, 17, 31, 32, 33, 64, 128] {
                let d = Drive { anchor: policy, ..Drive::new(t) };
                let a = run(Order::Lockstep, &w, &f, &d).unwrap();
                let Some(g) = run(Order::Gpu, &w, &f, &d) else { return };
                same(&format!("judge seed {seed} anchored {anchored}"), &format!("gpu at tick {t}"), &a, &g, true);
                if t == 1 && seed == 1 {
                    assert_eq!(a.contacts, 43, "the first chronon's contacts outnumber the 32 threads that detect them");
                }
            }
        }
    }
}
