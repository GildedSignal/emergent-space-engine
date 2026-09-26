//! MetalChronon against the CPU chronon reference: events, state, digests and metrics.
use emergent_lattice::{chronon::Chronon, law::Response, worlds, Stepper, World};
use emergent_lattice_metal::{MetalChronon, Options, Stats};

fn metal(w: World, opts: Options) -> Option<MetalChronon> {
    match MetalChronon::with_options(w, true, opts) {
        Ok(m) => Some(m),
        Err(e) => {
            eprintln!("skip: {e}");
            None
        }
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
    // Every contact resolved on the CPU, none settled on the GPU.
    let cpu = Options { gpu_settle: false, ..Options::default() };
    check("gas, CPU responds to all", worlds::gas(1024, 0.1, 1024, 256, 3), 300, cpu.clone());
    check("mixed, CPU responds to all", worlds::mixed(200, 512, 21), 600, cpu);
    // Q = 2^20 with speeds near c: C·(K + 1) is about 2^39, so every chronon takes the CPU path.
    let big = worlds::gas(64, 0.1, 1 << 20, 1 << 18, 3);
    if let Some(s) = check("gas Q = 2^20 (precondition fails)", big, 400, Options::default()) {
        assert_eq!((s.gpu_chronons, s.cpu_chronons), (0, 400), "{s:?}");
    }
}
