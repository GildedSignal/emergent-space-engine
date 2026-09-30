//! `Kickable` for `MetalChronon` against `Chronon`, at the stepper level: every hook (`kick`,
//! `rebase`, `motions`, `masses`) between runs, with refusals, must leave the two in the same state
//! (world, events, digests, metrics), and the next dense batch must see what the hook did.
//!
//! - **Fuzz**: random schedules of run / kick / rebase (uniform and per-body shifts) / illegal
//!   kicks / wrong lengths, under every law, in worlds with and without walls.
//! - **Directed**, one per piece of GPU state the hooks must keep coherent: the speed
//!   precondition (`p1`: a boost past the GPU's range runs on the CPU, the un-boost returns to the
//!   GPU), the cell-coordinate bound (`xmax`: a shift out of i32 cells), the bins (`bincell`),
//!   and the reference's pruning (`prune_due`: owed at a multiple of 64, settled before a rebase).
use emergent_lattice::law::Response;
use emergent_lattice::worlds::{self, Rng};
use emergent_lattice::{chronon::Chronon, Body, Kickable, Law, Motion, Stepper, World};
use emergent_lattice_metal::{MetalChronon, MetalError, Options};

fn pair(w: World, opts: Options) -> Option<(Chronon, MetalChronon)> {
    let m = match MetalChronon::with_options(w.clone(), true, opts) {
        Ok(m) => m,
        Err(MetalError::NoDevice) => {
            eprintln!("skip: no Metal device");
            return None;
        }
        Err(e) => panic!("{e}"),
    };
    Some((Chronon::new(w, true).unwrap(), m))
}

/// The two are the same stepper in every way the contract can see.
fn agree(name: &str, c: &Chronon, m: &MetalChronon) {
    assert_eq!(m.tick(), c.tick(), "{name}: tick");
    assert_eq!(m.world(), c.world(), "{name}: world");
    assert_eq!(m.log().sorted(), c.log().sorted(), "{name}: events");
    assert_eq!(m.outcome(), c.outcome(), "{name}: digests");
    let (a, b) = (m.metrics(), c.metrics());
    assert_eq!((a.ops, a.predicates, a.fired, a.batches, a.max_batch), (b.ops, b.predicates, b.fired, b.batches, b.max_batch), "{name}: metrics");
    let (mut x, mut y): (Vec<Motion>, Vec<Motion>) = (vec![], vec![]);
    c.motions(&mut x);
    m.motions(&mut y);
    assert_eq!(x, y, "{name}: motions");
    let (mut p, mut q): (Vec<i64>, Vec<i64>) = (vec![], vec![]);
    c.masses(&mut p);
    m.masses(&mut q);
    assert_eq!(p, q, "{name}: masses");
}

fn both<T: PartialEq + std::fmt::Debug>(name: &str, what: &str, c: Result<T, emergent_lattice::law::LawError>, m: Result<T, emergent_lattice::law::LawError>) -> bool {
    assert_eq!(c.as_ref().map_err(|e| e.0.clone()), m.as_ref().map_err(|e| e.0.clone()), "{name}: {what}: the same answer, or the same refusal");
    c.is_ok()
}

struct Tally {
    kicks: u32,
    rebases: u32,
    refused: u32,
}

/// Random schedules. `q` sizes the kicks (at most q/32 per axis).
fn fuzz(name: &str, w: World, opts: Options, rounds: usize, seed: u64) -> Option<Tally> {
    let (mut c, mut m) = pair(w.clone(), opts)?;
    let (q, n, walls) = (w.q, w.bodies.len(), w.container.is_some());
    let mut rng = Rng(seed);
    let small = |rng: &mut Rng, span: i64| -> [i64; 2] { [rng.range(-span, span), rng.range(-span, span)] };
    let mut t = Tally { kicks: 0, rebases: 0, refused: 0 };
    let mut tick = 0;
    for round in 0..rounds {
        let label = format!("{name} round {round}");
        tick += rng.range(1, 70);
        c.run_to(tick);
        m.run_to(tick);
        agree(&format!("{label} run"), &c, &m);
        let sparse = |rng: &mut Rng, span: i64| -> Vec<[i64; 2]> { (0..n).map(|_| if rng.next() % 3 == 0 { small(rng, span) } else { [0, 0] }).collect() };
        match rng.next() % 8 {
            0..=3 => {
                let dk = sparse(&mut rng, q / 32);
                let ok = both(&label, "kick", c.kick(&dk), m.kick(&dk));
                (t.kicks, t.refused) = (t.kicks + ok as u32, t.refused + !ok as u32);
            }
            4 | 5 => {
                // A frame move: a uniform shift (no pair changes) plus, half the time, a per-body
                // settling (pairs move by the difference).
                let shift = small(&mut rng, 1 << 20);
                let per_body = rng.next() % 2 == 0;
                let dx: Vec<[i64; 2]> = (0..n)
                    .map(|_| {
                        if per_body && rng.next() % 2 == 0 {
                            let e = small(&mut rng, q / 4);
                            [shift[0] + e[0], shift[1] + e[1]]
                        } else {
                            shift
                        }
                    })
                    .collect();
                let dk = sparse(&mut rng, q / 64);
                let ok = both(&label, "rebase", c.rebase(&dx, &dk), m.rebase(&dx, &dk));
                (t.rebases, t.refused) = (t.rebases + ok as u32, t.refused + !ok as u32);
            }
            6 => {
                // Illegal: one body past the exactness range (2^22), or a wrong count. Nothing applied.
                let mut dk = vec![[0i64; 2]; n];
                dk[rng.range(0, n as i64 - 1) as usize] = [1 << 23, 0];
                assert!(!both(&label, "illegal kick", c.kick(&dk), m.kick(&dk)));
                assert!(!both(&label, "short kick", c.kick(&dk[1..]), m.kick(&dk[1..])));
                let dx = vec![[0i64; 2]; n];
                assert!(!both(&label, "illegal rebase", c.rebase(&dx, &dk), m.rebase(&dx, &dk)));
                assert!(!both(&label, "short rebase", c.rebase(&dx[1..], &dk), m.rebase(&dx[1..], &dk)));
                t.refused += 4;
            }
            _ => {
                let zero = vec![[0i64; 2]; n];
                assert!(both(&label, "zero kick", c.kick(&zero), m.kick(&zero)));
                assert_eq!(both(&label, "zero rebase", c.rebase(&zero, &zero), m.rebase(&zero, &zero)), !walls, "{label}: a world with walls refuses every rebase");
            }
        }
        agree(&format!("{label} after the hook"), &c, &m);
    }
    c.run_to(tick + 200);
    m.run_to(tick + 200);
    agree(&format!("{name} end"), &c, &m);
    assert!(c.log().contacts > 0, "{name}: the schedule must exercise contacts");
    assert!(m.stats().gpu_chronons > 0, "{name}: the GPU must run chronons");
    eprintln!("{name}: {} contacts, {} kicks, {} rebases, {} refusals | {:?}", c.log().contacts, t.kicks, t.rebases, t.refused, m.stats());
    Some(t)
}

fn free(n: u64, seed: u64, response: Response, law: Law) -> World {
    worlds::random(n, 400, 1024, 1, seed, response).with_law(law).unwrap()
}

#[test]
fn fuzz_free_worlds_under_every_law() {
    for (law, seed) in [(Law::Newtonian, 1u64), (Law::Relativistic, 2), (Law::RelativisticV1, 3)] {
        let t = fuzz(&format!("free {law:?}"), free(300, 6 + seed, Response::Bounce, law), Options::default(), 60, seed).unwrap_or(Tally { kicks: 1, rebases: 1, refused: 0 });
        assert!(t.kicks > 5 && t.rebases > 3, "the schedule must kick and rebase: {} {}", t.kicks, t.rebases);
    }
    fuzz("free Stop", free(300, 9, Response::Stop, Law::Newtonian), Options::default(), 40, 4);
    fuzz("packed", worlds::packed(400, 8, 2, 1024, 1, 6), Options::default(), 40, 5);
}

#[test]
fn fuzz_worlds_with_walls_kick_and_refuse_to_rebase() {
    // A container does not move with the frame: every rebase is refused (by both), kicks work.
    for (law, seed) in [(Law::Newtonian, 6u64), (Law::Relativistic, 7), (Law::RelativisticV1, 8)] {
        let w = worlds::mixed(200, 512, 21).with_law(law);
        let Ok(w) = w else { continue };
        if let Some(t) = fuzz(&format!("walls {law:?}"), w, Options::default(), 50, seed) {
            assert_eq!(t.rebases, 0, "a world with walls cannot be re-expressed in a moved frame");
            assert!(t.kicks > 5);
        }
    }
    fuzz("gas", worlds::gas(256, 0.1, 1024, 256, 9), Options::default(), 40, 10);
}

#[test]
fn fuzz_with_the_cpu_and_the_small_batches_interleaved() {
    // GPU/CPU hand-over every 7th chronon and short command buffers: a hook may land after a
    // CPU chronon, a halted one, or the middle of a batch's bookkeeping.
    let opts = Options { cpu_every: 7, max_batch: 5, ..Options::default() };
    fuzz("interleaved", free(200, 11, Response::Bounce, Law::RelativisticV1), opts, 40, 11);
    let opts = Options { gpu_response: false, ..Options::default() };
    fuzz("cpu response", free(200, 12, Response::Bounce, Law::Newtonian), opts, 30, 12);
}

/// Two bouncers collide head-on at t = 10 and part (no walls, Newtonian).
fn two_bodies(q: i64) -> World {
    let r = q / 2;
    let a = Body::new(1, [0, 0], [q / 8, 0], 1, r, Response::Bounce);
    let b = Body::new(2, [7 * q / 2, 0], [-q / 8, 0], 1, r, Response::Bounce);
    World::new(q, None, vec![a, b]).unwrap()
}

#[test]
fn a_boost_past_the_gpu_range_runs_on_the_cpu_and_the_unboost_returns() {
    let q = 1024;
    let mut bodies: Vec<Body> = free(300, 13, Response::Bounce, Law::Newtonian).bodies;
    bodies.truncate(300);
    let w = World::new(q, None, bodies).unwrap();
    let Some((mut c, mut m)) = pair(w, Options::default()) else { return };
    c.run_to(40);
    m.run_to(40);
    agree("before the boost", &c, &m);
    let gpu0 = m.stats().gpu_chronons;
    // One body at 2^17 units per chronon (128 c): K ≥ 2^14, so the GPU's precondition fails.
    let mut dk = vec![[0i64; 2]; 300];
    dk[17] = [1 << 17, -(1 << 16)];
    assert!(both("boost", "kick", c.kick(&dk), m.kick(&dk)));
    agree("boosted", &c, &m);
    c.run_to(60);
    m.run_to(60);
    agree("running boosted", &c, &m);
    assert_eq!(m.stats().gpu_chronons, gpu0, "the boosted chronons run on the CPU path");
    assert!(m.stats().cpu_chronons >= 20, "{:?}", m.stats());
    let back: Vec<[i64; 2]> = dk.iter().map(|d| [-d[0], -d[1]]).collect();
    assert!(both("unboost", "kick", c.kick(&back), m.kick(&back)));
    c.run_to(200);
    m.run_to(200);
    agree("unboosted", &c, &m);
    assert!(m.stats().gpu_chronons > gpu0 + 100, "the GPU takes the chronons back at once: {:?}", m.stats());
    assert!(m.stats().cpu_chronons < 40, "no CPU chronon after the unboost: {:?}", m.stats());
}

/// Bodies of radius 40 units (reach 80) on a jittered grid, speeds up to Q/4: small enough that,
/// near the exactness range (2^39), cell coordinates leave i32 (2^38 / 80 > 2^31).
fn tiny_bodies(n: usize, seed: u64) -> World {
    let (q, spacing, per_row) = (1024, 1600i64, 18usize);
    let mut rng = Rng(seed);
    let bodies = (0..n)
        .map(|i| {
            let x = [(i % per_row) as i64 * spacing + rng.range(-200, 200), (i / per_row) as i64 * spacing + rng.range(-200, 200)];
            Body::new(i as u64 + 1, x, [rng.range(-q / 4, q / 4), rng.range(-q / 4, q / 4)], 1, 40, Response::Bounce)
        })
        .collect();
    World::new(q, None, bodies).unwrap()
}

#[test]
fn a_shift_out_of_the_cell_range_is_seen_and_so_is_the_shift_back() {
    // Cell coordinates leave i32 at about 2^37 here, so the GPU may not run there; the hook must
    // refresh the bound (a stale one would let the kernels narrow cells).
    let Some((mut c, mut m)) = pair(tiny_bodies(300, 14), Options::default()) else { return };
    c.run_to(30);
    m.run_to(30);
    let gpu0 = m.stats().gpu_chronons;
    assert!(gpu0 > 0);
    let far = vec![[1i64 << 38, -(1 << 38)]; 300];
    let zero = vec![[0i64; 2]; 300];
    assert!(both("far", "rebase", c.rebase(&far, &zero), m.rebase(&far, &zero)));
    c.run_to(90);
    m.run_to(90);
    agree("far", &c, &m);
    assert_eq!(m.stats().gpu_chronons, gpu0, "out of range: the CPU path");
    let back: Vec<[i64; 2]> = far.iter().map(|d| [-d[0], -d[1]]).collect();
    assert!(both("back", "rebase", c.rebase(&back, &zero), m.rebase(&back, &zero)));
    c.run_to(250);
    m.run_to(250);
    agree("back", &c, &m);
    assert!(m.stats().gpu_chronons > gpu0 + 100, "back in range: the GPU again {:?}", m.stats());
    assert!(c.log().contacts > 10, "contacts must happen: {}", c.log().contacts);
    // Past the exactness range (2^39): refused by both, nothing applied.
    let wall = vec![[1i64 << 39, 0]; 300];
    assert!(!both("past 2^39", "rebase", c.rebase(&wall, &zero), m.rebase(&wall, &zero)));
    agree("refused", &c, &m);
}

#[test]
fn per_body_shifts_rebin_the_next_chronon() {
    // The bins of the previous chronon are reused when the cell side is unchanged: a rebase that
    // moves positions must invalidate them. Every body nudged by a different few units, at many ticks.
    let Some((mut c, mut m)) = pair(free(400, 15, Response::Bounce, Law::RelativisticV1), Options::default()) else { return };
    let mut rng = Rng(77);
    for tick in (1..=120).map(|i| i * 3) {
        c.run_to(tick);
        m.run_to(tick);
        let dx: Vec<[i64; 2]> = (0..400).map(|_| [rng.range(-700, 700), rng.range(-700, 700)]).collect();
        let zero = vec![[0i64; 2]; 400];
        assert!(both("nudge", "rebase", c.rebase(&dx, &zero), m.rebase(&dx, &zero)));
        agree(&format!("nudged at {tick}"), &c, &m);
    }
    assert!(c.log().contacts > 0);
    eprintln!("nudges: {} contacts, {:?}", c.log().contacts, m.stats());
}

#[test]
fn the_pruning_owed_at_a_multiple_of_64_is_settled_before_a_rebase() {
    // The reference prunes consumed contacts at the end of chronon 64: the pair that collided at
    // t ≈ 10 and parted is forgotten. A per-body rebase at tick 64 that puts them back in contact
    // must find it forgotten (the contact fires again), even though the GPU order prunes lazily
    // (a CPU chronon at 64, `cpu_every`, leaves the prune owed).
    let q = 1024;
    let opts = Options { cpu_every: 64, ..Options::default() };
    let Some((mut c, mut m)) = pair(two_bodies(q), opts) else { return };
    c.run_to(64);
    m.run_to(64);
    agree("at 64", &c, &m);
    assert_eq!(c.log().contacts, 1, "they collided once and parted");
    let (mut mo, zero) = (vec![], vec![[0i64; 2]; 2]);
    c.motions(&mut mo);
    // Body 1 (moving left after the exchange) jumps to just right of body 2 (moving right):
    // approaching again, in contact at the next chronon.
    let dx = vec![[mo[1].x[0] - mo[0].x[0] + q - 1, 0], [0, 0]];
    assert!(both("swap", "rebase", c.rebase(&dx, &zero), m.rebase(&dx, &zero)));
    agree("rebased", &c, &m);
    c.run_to(70);
    m.run_to(70);
    agree("after", &c, &m);
    assert_eq!(c.log().contacts, 2, "the forgotten contact fires again");
}
