//! H_live (docs/plane.md, "Distinctions created per game-second"): the live distinguishing bits
//! the universe holds against its generators. Two contracts: sampling the measure is read-only
//! (no digest moves — the brief's hard line), and the bits a body carries stay far under the
//! 64-bit line that 8 GB draws for 10⁹ bodies. Each test finishes within 60 s.
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::{Budget, Config};

/// A short flight (about 5 minutes of game time, no player input): the fleet fights, bodies get
/// kicked, bindings rebind.
fn flown(sample: bool) -> (String, emergent_universe::universe::LiveBits, usize) {
    let mut p = plane(Config::default(), 7, Order::Sparse, 1, 8).unwrap();
    let mut bits = 0u64;
    let mut t = 0i64;
    while t < 60_000_000 {
        t += 500_000;
        p.u.advance(t, Budget::events(2000));
        if sample {
            bits += p.u.live_bits().bits();
        }
    }
    p.u.settle(t);
    (p.u.digest(), p.u.live_bits(), p.u.n_bodies())
}

#[test]
fn sampling_moves_no_digest() {
    let (quiet, _, _) = flown(false);
    let (sampled, _, _) = flown(true);
    assert_eq!(quiet, sampled, "sampling live bits moved the digest");
}

#[test]
fn a_kicked_scene_stays_under_the_billion_body_line() {
    let (_, lb, n) = flown(true);
    // 8 GB / 10⁹ bodies = 64 bits per body: the whole scene's live distinctions must sit under
    // that line, or the memory question is not about distinctions at all.
    assert!(
        lb.bits() < 64 * n as u64,
        "live bits {} over {} bodies exceed 64 per body",
        lb.bits(),
        n
    );
    assert!(lb.decisions == 0, "no player flew, but decision bits appeared");
}
