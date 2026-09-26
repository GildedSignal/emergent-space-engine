//! MetalChronon against the CPU chronon reference: events, state, digests and metrics.
use emergent_lattice::{chronon::Chronon, law::Response, worlds, worlds::Rng, Law, Stepper, World};
use emergent_lattice_metal::{MetalChronon, MetalError, Options, Stats};

/// None (the test skips) only when there is no Metal device; any other error fails.
fn metal(w: World, opts: Options) -> Option<MetalChronon> {
    match MetalChronon::with_options(w, true, opts) {
        Ok(m) => Some(m),
        Err(MetalError::NoDevice) => {
            eprintln!("skip: no Metal device");
            None
        }
        Err(e) => panic!("{e}"),
    }
}

/// Run both to `horizon` and demand identical events, state, digests and accounting.
fn check(name: &str, w: World, horizon: i64, opts: Options) -> Option<Stats> {
    let mut m = metal(w.clone(), opts)?;
    let mut c = Chronon::new(w, true).unwrap();
    c.run_to(horizon);
    m.run_to(horizon);
    assert!(c.log().contacts > 0, "{name}: the case must exercise contacts");
    assert_eq!(m.tick(), horizon, "{name}: tick");
    assert_eq!(m.log().sorted(), c.log().sorted(), "{name}: events");
    assert_eq!(m.world(), c.world(), "{name}: state");
    assert_eq!(m.outcome(), c.outcome(), "{name}: digests");
    let (a, b) = (m.metrics(), c.metrics());
    assert_eq!(m.stats().table_overflows, 0, "{name}: GPU consumed table overflowed");
    assert_eq!(
        (a.ops, a.predicates, a.fired, a.batches, a.max_batch),
        (b.ops, b.predicates, b.fired, b.batches, b.max_batch),
        "{name}: metrics (the GPU must test exactly the reference's candidates)"
    );
    eprintln!("{name}: {} contacts, {} walls, {:?}", c.log().contacts, c.log().walls, m.stats());
    Some(m.stats().clone())
}

#[test]
fn gas_matches_reference() {
    for (n, horizon) in [(16, 800), (64, 1000), (256, 1024), (1024, 512), (2048, 256)] {
        check(&format!("gas {n}"), worlds::gas(n, 0.1, 1024, 256, 3), horizon, Options::default());
    }
    check("gas dense small Q", worlds::gas(40, 0.3, 64, 32, 4), 800, Options::default());
    check("gas fast", worlds::gas(300, 0.2, 1024, 700, 5), 600, Options::default());
}

#[test]
fn mixed_matches_reference() {
    for (n, q, seed, horizon) in [(48, 1024, 1, 600), (120, 256, 2, 600), (200, 512, 21, 1500), (700, 1024, 8, 400)] {
        check(&format!("mixed {n}"), worlds::mixed(n, q, seed), horizon, Options::default());
    }
}

#[test]
fn packed_matches_reference() {
    for (n, seed, horizon) in [(64, 5, 600), (400, 6, 400), (1500, 7, 200)] {
        check(&format!("packed {n}"), worlds::packed(n, 8, 2, 1024, 1, seed), horizon, Options::default());
    }
}

#[test]
fn random_matches_reference() {
    for (n, response) in [(64, Response::Pass), (500, Response::Pass), (300, Response::Bounce), (300, Response::Stop)] {
        let stats = check(&format!("random {n} {response:?}"), worlds::random(n, 400, 1024, 1, 6, response), 800, Options::default());
        if let Some(s) = stats.filter(|_| n == 64) {
            // Sparse: quiet chronons share command buffers.
            assert!(s.command_buffers < s.gpu_chronons / 2, "quiet chronons must be batched: {s:?}");
        }
    }
}

#[test]
fn slicing_and_restore_do_not_change_the_outcome() {
    for w0 in [worlds::mixed(200, 512, 21), worlds::gas(256, 0.1, 1024, 256, 9), worlds::random(64, 400, 1024, 1, 6, Response::Pass)] {
        let horizon = 1100;
        let mut reference = Chronon::new(w0.clone(), false).unwrap();
        reference.run_to(horizon);
        let expected = reference.outcome();
        for budget in [1u64, 97, 5000, 200_000] {
            let Some(mut s) = metal(w0.clone(), Options::default()) else { return };
            while s.tick() < horizon {
                s.advance(horizon, budget);
            }
            assert_eq!(s.outcome(), expected, "budget {budget}");
            assert_eq!(s.metrics().ops, reference.metrics().ops, "budget {budget}: ops");
        }
        let Some(mut first) = metal(w0.clone(), Options::default()) else { return };
        first.run_to(517);
        let Some(mut second) = metal(first.world(), Options::default()) else { return };
        second.run_to(horizon);
        let mut log = first.log().clone();
        log.merge(second.log());
        assert_eq!((second.world().digest(), log.digest()), expected, "restore");
    }
}

#[test]
fn every_path_gives_the_same_bits() {
    let hand_over = Options { cpu_every: 7, ..Options::default() };
    let s = check("mixed, CPU every 7th chronon", worlds::mixed(200, 512, 21), 900, hand_over.clone());
    if let Some(s) = s {
        assert!(s.cpu_chronons > 100 && s.gpu_chronons > 600, "{s:?}");
    }
    check("packed, CPU every 7th chronon", worlds::packed(400, 8, 2, 1024, 1, 6), 400, hand_over);
    let tiny = Options { pair_capacity: 1, ..Options::default() };
    if let Some(s) = check("gas, pair buffer overflow", worlds::gas(512, 0.1, 1024, 256, 3), 300, tiny) {
        assert!(s.pair_overflows > 0, "{s:?}");
    }
    check("mixed, one chronon per buffer", worlds::mixed(120, 256, 2), 600, Options { max_batch: 1, ..Options::default() });
    // Components resolved concurrently on threads, every batch.
    let threads = Options { par_min: 1, threads: 4, ..Options::default() };
    check("mixed, threaded response", worlds::mixed(700, 1024, 8), 400, threads.clone());
    check("packed, threaded response", worlds::packed(1500, 8, 2, 1024, 1, 7), 200, threads.clone());
    check("gas, threaded response", worlds::gas(4096, 0.1, 1024, 256, 2), 200, threads);
    // Every contact resolved on the CPU.
    let cpu = Options { gpu_response: false, ..Options::default() };
    check("gas, CPU responds to all", worlds::gas(1024, 0.1, 1024, 256, 3), 300, cpu.clone());
    check("mixed, CPU responds to all", worlds::mixed(200, 512, 21), 600, cpu);
    // Q = 2^20 with speeds near c: C·(K + 1) is about 2^39, so every chronon takes the CPU path.
    let big = worlds::gas(64, 0.1, 1 << 20, 1 << 18, 3);
    if let Some(s) = check("gas Q = 2^20 (precondition fails)", big, 400, Options::default()) {
        assert_eq!((s.gpu_chronons, s.cpu_chronons), (0, 400), "{s:?}");
    }
}

/// Mixed bouncers at up to 0.88c at genesis (as the event core's relativistic test).
fn hot_mixed(n: u64, q: i64, seed: u64) -> World {
    let mut w = worlds::mixed(n, q, seed);
    for b in &mut w.bodies {
        b.response = Response::Bounce;
        b.k = [b.k[0] * 5 / 4, b.k[1] * 5 / 4];
    }
    w.with_law(Law::Relativistic).unwrap()
}

#[test]
fn relativistic_worlds_match_reference() {
    let rel = |w: World| w.with_law(Law::Relativistic).unwrap();
    let cases = [
        ("gas 256 relativistic", rel(worlds::gas(256, 0.1, 1024, 256, 3)), 1024),
        ("gas 2048 relativistic", rel(worlds::gas(2048, 0.1, 1024, 256, 4)), 200),
        ("mixed relativistic", rel(worlds::mixed(200, 512, 21)), 800),
        ("hot mixed 256", hot_mixed(256, 256, 31), 1500),
        ("hot mixed 1024", hot_mixed(1024, 512, 32), 500),
    ];
    for (name, w0, horizon) in cases {
        let Some(s) = check(name, w0.clone(), horizon, Options::default()) else { return };
        assert!(s.gpu_contacts > s.cpu_contacts, "{name}: the GPU resolves relativistic contacts: {s:?}");
        let Some(mut m) = metal(w0, Options::default()) else { return };
        m.run_to(horizon);
        let w = m.world();
        assert!(w.bodies.iter().all(|b| (b.k[0] as i128).pow(2) + (b.k[1] as i128).pow(2) < (w.q as i128).pow(2)), "{name}: below c");
    }
    // Near c, light and heavy: γ up to ~22, masses 1 to 2^16. Heavy fast pairs leave the
    // GPU's 128-bit ranges and go to the CPU (big integers there); the rest stay on the GPU.
    let Some(s) = check("near c, light and heavy", near_c(400, 41, &[1, 1, 2, 3, 7, 1024, 65536]), 300, Options::default()) else { return };
    assert!(s.gpu_contacts > 0 && s.cpu_contacts > 0 && s.halts > 0, "both paths must run: {s:?}");
    let Some(s) = check("near c, light", near_c(1500, 42, &[1, 2, 3, 7]), 200, Options::default()) else { return };
    assert!(s.gpu_contacts > 2 * s.cpu_contacts, "light pairs near c stay on the GPU: {s:?}");
    // Q > 2^15: the GPU still detects, the CPU responds.
    let s = check("relativistic Q = 2^16", rel(worlds::gas(256, 0.1, 1 << 16, 256, 5)), 400, Options::default()).unwrap();
    assert!(s.gpu_chronons == 400 && s.gpu_contacts == 0, "{s:?}");
    // es-lattice-relativistic-v1: the GPU detects, the CPU responds (the kernel is v0's).
    let v1 = |w: World| w.with_law(Law::RelativisticV1).unwrap();
    for (name, w0, horizon) in [
        ("gas 2048 v1", v1(worlds::gas(2048, 0.1, 1024, 256, 4)), 200),
        ("hot mixed 256 v1", World { law: Law::RelativisticV1, ..hot_mixed(256, 256, 31) }, 1500),
        ("slow gas v1 (0.004c)", v1(worlds::gas(1024, 0.1, 4096, 16, 6)), 4000),
    ] {
        let s = check(name, w0, horizon, Options::default()).unwrap();
        assert!(s.gpu_contacts == 0 && s.cpu_contacts > 0, "{name}: v1 responds on the CPU: {s:?}");
    }
    // Slicing under the relativistic law.
    let w0 = hot_mixed(256, 256, 31);
    let mut r = Chronon::new(w0.clone(), false).unwrap();
    r.run_to(900);
    for budget in [97u64, 5000] {
        let Some(mut m) = metal(w0.clone(), Options::default()) else { return };
        while m.tick() < 900 {
            m.advance(900, budget);
        }
        assert_eq!(m.outcome(), r.outcome(), "relativistic budget {budget}");
    }
}

/// Bouncers of the given masses at |k| from 0.9c to 1023/1024 c (γ up to ~22), boxed.
fn near_c(n: u64, seed: u64, masses: &[i64]) -> World {
    let mut w = worlds::mixed(n, 1024, seed);
    let mut rng = Rng(seed);
    for b in &mut w.bodies {
        b.response = Response::Bounce;
        b.mass = masses[(rng.next() % masses.len() as u64) as usize];
        let speed = rng.range(922, 1023);
        let kx = rng.range(-speed, speed);
        let ky = ((speed * speed - kx * kx) as f64).sqrt() as i64 * if rng.next() % 2 == 0 { 1 } else { -1 };
        b.k = [kx, ky];
    }
    w.with_law(Law::Relativistic).unwrap()
}
