//! MetalChronon against the CPU chronon reference: events, state, digests and metrics.
use emergent_lattice::{chronon::Chronon, law::Response, relativity, worlds, worlds::Rng, Body, Container, Law, Stepper, World};
use emergent_lattice_metal::{float_floors_probe, v1_momenta, FloorCase, MetalChronon, MetalError, Options, Stats};

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
    // es-lattice-relativistic-v1 on the GPU: its 32-bit-limb roots (Q ≤ 2^10) and its 128-bit
    // ones (the slow gas at Q = 2^12).
    let v1 = |w: World| w.with_law(Law::RelativisticV1).unwrap();
    for (name, w0, horizon) in [
        ("gas 2048 v1", v1(worlds::gas(2048, 0.1, 1024, 256, 4)), 200),
        ("hot mixed 256 v1", World { law: Law::RelativisticV1, ..hot_mixed(256, 256, 31) }, 1500),
        ("slow gas v1 (0.004c)", v1(worlds::gas(1024, 0.1, 4096, 16, 6)), 4000),
    ] {
        let s = check(name, w0, horizon, Options::default()).unwrap();
        assert!(s.gpu_contacts > s.cpu_contacts, "{name}: the GPU resolves v1 contacts: {s:?}");
    }
    // Near c under v1: the float estimates are far off and the exact Newton step runs; heavy
    // fast pairs leave the 128-bit ranges for the CPU.
    let Some(s) = check("near c, light and heavy v1", World { law: Law::RelativisticV1, ..near_c(400, 41, &[1, 1, 2, 3, 7, 1024, 65536]) }, 300, Options::default()) else { return };
    assert!(s.gpu_contacts > 0 && s.cpu_contacts > 0 && s.halts > 0, "both paths must run: {s:?}");
    let Some(s) = check("near c, light v1", World { law: Law::RelativisticV1, ..near_c(1500, 42, &[1, 2, 3, 7]) }, 200, Options::default()) else { return };
    assert!(s.gpu_contacts > 2 * s.cpu_contacts, "light pairs near c stay on the GPU: {s:?}");
    // v1 at Q = 2^16: the reflection's target products leave 128 bits, and the float filter
    // decides their floors exactly, so the GPU resolves these contacts too.
    let s = check("v1 Q = 2^16", v1(worlds::gas(256, 0.1, 1 << 16, 256, 5)), 400, Options::default()).unwrap();
    assert!(s.gpu_chronons == 400 && s.gpu_contacts > s.cpu_contacts, "{s:?}");
    // v1 at Q = 2^20: the Minkowski normal leaves 62 bits, so the CPU responds to every contact
    // (the GPU still detects; walls stay on the GPU).
    let s = check("v1 Q = 2^20 (CPU fallback)", v1(rows(64, 1 << 20, 43)), 400, Options::default()).unwrap();
    assert!(s.gpu_chronons == 400 && s.gpu_contacts == 0 && s.cpu_contacts > 0 && s.halts > 0, "{s:?}");
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

/// A crowded start: n bouncers of radius 50 on a grid of eight columns 130 apart (reach 100), at up
/// to 230 quanta per chronon in either axis, so that dozens of contacts fire in the very first
/// chronons. Law v1 at Q = 1024.
fn crowded(n: u64, seed: u64) -> World {
    let mut rng = Rng(seed);
    let bodies = (0..n as i64)
        .map(|i| {
            let (x, k) = ([(i % 8) * 130 - 450, (i / 8) * 130 - 180], [rng.range(-230, 230), rng.range(-230, 230)]);
            Body::new(i as u64 + 1, x, k, rng.range(1, 7), 50, Response::Bounce)
        })
        .collect();
    World::new(1024, None, bodies).unwrap().with_law(Law::RelativisticV1).unwrap()
}

/// More hits in one chronon than the threads of the last, partial threadgroup of `pairs`
/// (dispatched over n threads in groups of 256: the last group holds n mod 256; below 256 bodies
/// that is the only group). The hits a group buffers must be appended by every thread of that
/// group, whatever its size: a loop that strides by 256 left the rest of the buffer unwritten
/// (found by the engine judge's E1: battle frames on Metal differed from the CPU at the first
/// chronon of a crowded 32-body scene, whose 43 hits met 32 threads).
#[test]
fn hits_beyond_the_last_threadgroup_size_are_all_reported() {
    for n in [8, 16, 32, 40, 64, 100, 128] {
        for seed in [1, 2, 3] {
            let Some(s) = check(&format!("crowded {n} seed {seed}"), crowded(n, seed), 6, Options::default()) else { return };
            assert!(s.gpu_chronons == 6, "crowded {n}: every chronon is detected on the GPU: {s:?}");
        }
    }
    // Far more hits than threads in the first chronon, past the 256 a threadgroup buffers (the
    // rest go to the global list); the crowd's consumed contacts overflow the GPU table, which
    // only the predicate count shows (check() would refuse it), so compare the outcome alone.
    for (n, side) in [(100u64, 10), (200, 14)] {
        let bodies = (0..n as i64)
            .map(|i| Body::new(i as u64 + 1, [(i % side) * 30, (i / side) * 30], [(i * 7) % 61 - 30, (i * 13) % 59 - 29], 1 + i % 5, 50, Response::Bounce))
            .collect();
        let w = World::new(1024, None, bodies).unwrap().with_law(Law::RelativisticV1).unwrap();
        let Some(mut m) = metal(w.clone(), Options::default()) else { return };
        let mut c = Chronon::new(w, true).unwrap();
        for t in 1..=4 {
            c.run_to(t);
            m.run_to(t);
            assert_eq!(m.outcome(), c.outcome(), "overlapping crowd of {n}: digests at {t}");
        }
        assert!(c.log().contacts > 256, "overlapping crowd of {n}: {} contacts", c.log().contacts);
    }
}

/// Rows of eight unit-mass bouncers of radius Q a few hundred quanta apart, at up to 50 quanta
/// per chronon (slow enough for the GPU's detection at any Q), boxed: contacts from the start.
fn rows(n: u64, q: i64, seed: u64) -> World {
    let mut rng = Rng(seed);
    let (step, row) = (2 * q + 400, 4 * q);
    let bodies = (0..n as i64)
        .map(|i| {
            let x = [q + 1000 + (i % 8) * step + rng.range(0, 300), q + 1000 + (i / 8) * row];
            let k = [rng.range(-50, 50), rng.range(-3, 3)];
            Body::new(i as u64 + 1, x, k, 1, q, Response::Bounce)
        })
        .collect();
    let side = 2 * q + 2000 + 8 * step.max(row);
    World::new(q, Some(Container { min: [0, 0], max: [side, side] }), bodies).unwrap()
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

/// The GPU kernel's v1 4-momentum against `relativity::four_momentum_v1` (u128 square roots,
/// independent code): Q from 3 to 2^20 on both sides of the 32-bit-limb bound (2Q³ ≤ 2^31),
/// velocities from rest to the light cone's edge (s = Q² − |k|² down to 1, γ up to Q), on and
/// off the axes, masses 1 to 2^16. Equal wherever the kernel answers, and it answers whenever
/// m·E < 2^58.
#[test]
fn v1_momentum_is_exact_on_the_gpu() {
    let mut rng = Rng(77);
    for q in [3i64, 5, 64, 1000, 1024, 1025, 1291, 4096, 1 << 15, 99_991, (1 << 20) - 1, 1 << 20] {
        let edge = |kx: i64| ((q * q - 1 - kx * kx) as u64).isqrt() as i64;
        let mut ks: Vec<[i64; 2]> = vec![[0, 0], [q - 1, 0], [0, 1 - q], [1, 0], [-1, 1], [edge(q / 2), -(q / 2)]];
        for _ in 0..1500 {
            let kx = rng.range(1 - q, q - 1);
            ks.push([kx, rng.range(-edge(kx), edge(kx))]);
            let kx = rng.range(1 - q, q - 1);
            let sign = if rng.next().is_multiple_of(2) { 1 } else { -1 };
            ks.push([kx, sign * edge(kx)]);
            let v = (q / 64).max(1);
            ks.push([rng.range(-v, v), rng.range(-v, v)]);
        }
        let cases: Vec<(i64, [i64; 2])> = ks.iter().flat_map(|&k| [1, 3, 1024, 65536].map(|m| (m, k))).collect();
        let got = match v1_momenta(q, &cases) {
            Ok(g) => g,
            Err(MetalError::NoDevice) => return,
            Err(e) => panic!("{e}"),
        };
        let mut answered = 0;
        for (&(m, k), g) in cases.iter().zip(&got) {
            let r = relativity::four_momentum_v1(m, k, q);
            match g {
                Some(g) => {
                    assert_eq!(g.map(|x| x as i128), r, "Q {q}, m {m}, k {k:?}");
                    answered += 1;
                }
                None => assert!(r[0] >= 1 << 58, "Q {q}, m {m}, k {k:?}: in range but left to the CPU"),
            }
        }
        eprintln!("Q {q}: {answered} of {} answered on the GPU, all exact", cases.len());
    }
}

/// The reflection's float filter against exact i128 floors: it may defer to the exact path,
/// but a floor it decides must be exact and its target must not be an integer. Adversarial
/// cases: targets exactly at integers and within one part in 2^40 of them, heavy cancellation
/// (T·p ≈ 2S·n, so x or e nearly vanishes), e = 0, both signs, Q from 3 to 2^20.
#[test]
fn float_filter_decides_only_exact_floors() {
    let (mut rng, mut uniform) = (Rng(91), Rng(92));
    let mut big = |bits: u32| -> i64 {
        let b = rng.range(0, bits as i64) as u32;
        let v = (rng.next() >> (64 - b.max(1))) as i64;
        if rng.next().is_multiple_of(2) { v } else { -v }
    };
    let mut cases: Vec<FloorCase> = vec![];
    for i in 0..60_000 {
        let q = [3i64, 1024, 4096, 1 << 16, 1 << 20][i % 5];
        let (t, s2) = (big(60) as i128, big(60) as i128);
        let (pv, nv) = ([big(40).abs().max(1), big(40), big(40)], [big(40), big(40), big(40)]);
        match i % 6 {
            // Random.
            0 => cases.push((q, t, s2, pv, nv)),
            // S = 0: target q·p_c/p_E, placed on, just below and just above integers.
            1 => {
                let m = big(20).abs().max(1);
                let k = big(10) % q.max(2);
                let pe = q * m;
                let px = k * m + [0, -1, 1][i % 3];
                cases.push((q, t.max(1), 0, [pe, px, pv[2] % pe], nv));
            }
            // Cancellation in x: 2S = T and n_x = p_x + δ, so x = −T·δ.
            2 => {
                let d = big(3);
                cases.push((q, t, t, pv, [nv[0], pv[1] + d, pv[2] - d]));
            }
            // e = 0 and e tiny: 2S = T, n_E = p_E (+ 1).
            3 => cases.push((q, t, t, pv, [pv[0] + (i as i64 / 6) % 2, nv[1], nv[2]])),
            // Near-integer targets with S ≠ 0: n = 0 except n_E, so x = T·p_x, e = T·p_E − 2S·n_E.
            4 => {
                let pe = big(38).abs().max(1) * q;
                let k = big(10) % q.max(2);
                cases.push((q, t, s2, [pe, k * (pe / q) + [0, -1, 1][i % 3], pv[2] % pe], [0, 0, 0]));
            }
            // Realistic magnitudes: T ≫ 2S·n, small velocities.
            _ => {
                let pe = (1i64 << 39) + big(38).abs();
                let mut half = || (uniform.next() % pe as u64) as i64 - pe / 2;
                cases.push((q, t, s2 >> 30, [pe, half(), half()], nv.map(|v| v >> 20)))
            }
        }
    }
    let got = match float_floors_probe(&cases) {
        Ok(g) => g,
        Err(MetalError::NoDevice) => return,
        Err(e) => panic!("{e}"),
    };
    let floor = |n: i128, d: i128| n.div_euclid(d);
    let (mut decided, mut small_q) = ([0usize; 6], [0usize; 2]);
    for (i, (&(q, t, s2, pv, nv), g)) in cases.iter().zip(&got).enumerate() {
        if i % 6 == 5 && q <= 4096 {
            small_q[1] += 1;
        }
        let Some(f) = g else { continue };
        decided[i % 6] += 1;
        if i % 6 == 5 && q <= 4096 {
            small_q[0] += 1;
        }
        let (mut e, mut x, mut y) =
            (t * pv[0] as i128 - s2 * nv[0] as i128, t * pv[1] as i128 - s2 * nv[1] as i128, t * pv[2] as i128 - s2 * nv[2] as i128);
        assert!(e != 0, "decided with e = 0: {:?}", (q, t, s2, pv, nv));
        if e < 0 {
            (e, x, y) = (-e, -x, -y);
        }
        let (nx, ny) = (q as i128 * x, q as i128 * y);
        assert_eq!([floor(nx, e) as i64, floor(ny, e) as i64], *f, "{:?}", (q, t, s2, pv, nv));
        assert!(nx % e != 0 && ny % e != 0, "an integer target was decided: {:?}", (q, t, s2, pv, nv));
    }
    eprintln!("float filter: decided per kind (random, on/near integers, cancelling x, e ≈ 0, near integers, realistic) {decided:?} of {} each; all exact", cases.len() / 6);
    // Floats carry 24 bits: at Q ≤ 2^12 nearly every realistic floor is decided, at Q = 2^20
    // few are.
    assert!(small_q[0] > small_q[1] * 9 / 10, "the filter decides most realistic cases at Q ≤ 2^12: {small_q:?}");
}
