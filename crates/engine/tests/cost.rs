//! Cost of the dense order, measured the way the player runs it (a busy fanless M1: heat and
//! load are part of the number, so the machine's state is printed before and after).
//!
//! Reported: (1) ns per body per epoch-kick, split into reading the bodies, computing the kick
//! (the frame's integer law) and applying it (the stepper's hook), for both orders; the sparse
//! order's real cost of an epoch also includes re-predicting every kicked body, so the end-to-end
//! marginal cost (a run with the tide against the same run without it) and the event core's
//! ops per body-epoch are reported too; (2) events per second of the sparse order, and the
//! lockstep time for the same battle; (3) the kick pass alone across 1, 4 and 8 threads.
//! Asserts only that the runs are equal in both orders and finish inside the minute.
use emergent_engine::{scenes, Battle, Frame, Weight};
use emergent_lattice::law::Tick;
use emergent_lattice::{chronon::Chronon, Kickable, Motion, Stepper};
use emergent_lattice_event::EventCore;
use std::process::Command;
use std::time::Instant;

const HORIZON: Tick = 4096;

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

/// One order's epoch kicks, driven by hand so that each phase can be timed: reading the bodies,
/// computing the kicks, applying them (the stepper's hook), and, for the sparse order, the
/// upkeep the hook leaves pending (re-homing and re-predicting every kicked body), which runs
/// inside the next chronon. The genesis epoch (the event core's first indexing) is left out.
#[derive(Default)]
struct Phases {
    read: u64,
    frame: u64,
    apply: u64,
    upkeep: u64,
    epochs: u64,
}

fn drive<S: Kickable>(s: &mut S, f: &Frame, n: usize, upkeep: bool) -> (Phases, f64) {
    let (mut m, mut c, mut d) = (Vec::new(), vec![[0i64; 2]; n], vec![[0i64; 2]; n]);
    // The drift each body's lattice motion has dropped (the frame kicks it at its true position).
    let mut owed = vec![[0i128; 2]; n];
    let mut last = 0;
    let mut p = Phases::default();
    let wall = Instant::now();
    for j in 0..=HORIZON / f.epoch() {
        let at = j * f.epoch();
        s.run_to(at);
        let t0 = Instant::now();
        s.motions(&mut m);
        for (o, c) in owed.iter_mut().zip(&c) {
            o[0] += c[0] as i128 * (at - last) as i128;
            o[1] += c[1] as i128 * (at - last) as i128;
        }
        last = at;
        let t1 = Instant::now();
        let w = f.weights_at(at, if j == 0 { Weight::Half } else { Weight::Full }).unwrap();
        f.kick_all_masked(&w, &[], &owed, &m, &mut c, &mut d, 1);
        let t2 = Instant::now();
        s.kick(&d).unwrap();
        let t3 = Instant::now();
        if upkeep && at < HORIZON {
            s.run_to(at + 1);
        }
        let t4 = Instant::now();
        if j > 0 {
            p.epochs += 1;
            p.read += (t1 - t0).as_nanos() as u64;
            p.frame += (t2 - t1).as_nanos() as u64;
            p.apply += (t3 - t2).as_nanos() as u64;
            p.upkeep += (t4 - t3).as_nanos() as u64;
        }
    }
    s.run_to(HORIZON);
    (p, wall.elapsed().as_secs_f64())
}

#[test]
fn cost_of_the_epoch_kick_and_of_the_sparse_order() {
    machine_state("before");
    let (n, q) = (2000u64, 1024i64);
    let (w, extent) = scenes::battle(n, q, 8, 8, false);
    println!("scene: {n} bodies, q = {q}, genesis extent {} light-chronons, horizon {HORIZON} chronons", extent / q);
    println!("ns per body per epoch-kick (epochs after the first), by phase; sparse upkeep = re-home and re-predict every kicked body (run inside the next chronon):");
    for k in [13u32, 11, 9] {
        let radius = 32 * (extent + 4 * HORIZON * (q / 8));
        // About the non-rotating axes (the genesis rotation of `Frame::new` is the Battle's, not the driver's).
        let f = Frame::on_orbit(q, radius, 1u64 << (60 - k), 0, 0, 0).unwrap();
        let per = |ns: u64, p: &Phases| ns as f64 / (p.epochs * n) as f64;

        let mut lock = Chronon::new(w.clone(), false).unwrap();
        let (lp, lock_wall) = drive(&mut lock, &f, n as usize, false);
        let mut sp = EventCore::new(w.clone(), false).unwrap();
        let ops0 = sp.metrics().ops;
        let (sp_phases, sp_wall) = drive(&mut sp, &f, n as usize, true);
        // The hand-driven runs are the same runs as Battle's.
        let mut b = Battle::new(EventCore::new(w.clone(), false).unwrap(), f.clone(), 1);
        b.run_to(HORIZON).unwrap();
        assert_eq!((lock.world().digest(), lock.log().digest()), (sp.world().digest(), sp.log().digest()), "both orders, the same bits");
        assert_eq!((sp.world().digest(), sp.log().digest()), (b.stepper().world().digest(), b.stepper().log().digest()), "hand-driven = Battle");

        let events = sp.log().contacts + sp.log().walls;
        println!(
            "E = {:>3} (nT {:>4.2}, {:>3} epochs): lockstep read {:.1} + frame {:.1} + apply {:.1} = {:.1} ns; wall {:.2} s ({:.0} ns per body-chronon)\n                         sparse   read {:.1} + frame {:.1} + apply {:.1} + upkeep {:.1} = {:.1} ns; wall {:.2} s; {} contacts = {:.0} events/s, {:.1}M ops/s, {:.0} ops per body-epoch",
            f.epoch(),
            f.n_f64() * HORIZON as f64,
            lp.epochs,
            per(lp.read, &lp),
            per(lp.frame, &lp),
            per(lp.apply, &lp),
            per(lp.read + lp.frame + lp.apply, &lp),
            lock_wall,
            lock_wall * 1e9 / (n as i64 * HORIZON) as f64,
            per(sp_phases.read, &sp_phases),
            per(sp_phases.frame, &sp_phases),
            per(sp_phases.apply, &sp_phases),
            per(sp_phases.upkeep, &sp_phases),
            per(sp_phases.read + sp_phases.frame + sp_phases.apply + sp_phases.upkeep, &sp_phases),
            sp_wall,
            events,
            events as f64 / sp_wall,
            (sp.metrics().ops - ops0) as f64 / sp_wall / 1e6,
            (sp.metrics().ops - ops0) as f64 / (n * (HORIZON / f.epoch() + 1) as u64) as f64
        );
    }

    // The kick pass alone, across threads (the steppers are single-threaded; this is the only
    // threaded part). Chunked scoped threads pay a spawn per call, so small n does not gain.
    let f = Frame::new(q, 1 << 36, 1u64 << 47).unwrap();
    let mut motions: Vec<Motion> = Vec::new();
    Chronon::new(w.clone(), false).unwrap().motions(&mut motions);
    for threads in [1usize, 4, 8] {
        let (mut c, mut d) = (vec![[0i64; 2]; motions.len()], vec![[0i64; 2]; motions.len()]);
        let iters = 3000;
        // The weights are one tube readout per kick, outside the per-body pass; the pass alone is timed.
        let (half, full) = (f.weights_at(0, Weight::Half).unwrap(), f.weights_at(f.epoch(), Weight::Full).unwrap());
        let t = Instant::now();
        for i in 0..iters {
            f.kick_all(if i == 0 { &half } else { &full }, &motions, &mut c, &mut d, threads);
        }
        println!("kick pass alone, {n} bodies, {threads} threads: {:.1} ns per body-kick", t.elapsed().as_nanos() as f64 / (iters * n) as f64);
    }
    machine_state("after");
}
