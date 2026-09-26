//! es-lattice-relativistic-v1: the fixed-point 4-momentum is the exact floor of its
//! definition, reduces exactly to the Newtonian momentum and energy at low speed, and the
//! ledgers see kinetic energy where v0 is blind (H0173).
use emergent_lattice::{
    chronon::Chronon,
    law::{Body, Container, Response},
    relativity::{self, carried, four_momentum_v1, total},
    worlds::{self, Rng},
    Law, Stepper, World,
};
use num_bigint::BigInt;

/// E = ⌊2Q³/√s⌋ and |p_c| = ⌊2Q²|k_c|/√s⌋ (s = Q² − |k|²), checked by the defining
/// inequalities v²·s ≤ N² < (v + 1)²·s in big integers.
#[test]
fn the_momentum_is_the_exact_floor_of_its_definition() {
    let mut rng = Rng(7);
    for q in [3i64, 256, 1024, 1 << 15, 1 << 20] {
        for i in 0..2000 {
            let k = if i < 8 {
                [[0, 0], [q - 1, 0], [0, 1 - q], [1, 1], [-1, 0], [q / 2, q / 2], [q - 1, 1.min(q - 1)], [-(q / 3), q / 3]][i]
            } else {
                [rng.range(1 - q, q - 1), rng.range(1 - q, q - 1)]
            };
            let (kk, q2) = (k[0] as i128 * k[0] as i128 + k[1] as i128 * k[1] as i128, q as i128 * q as i128);
            if kk >= q2 {
                continue;
            }
            let s = BigInt::from(q2 - kk);
            let p = four_momentum_v1(1, k, q);
            let big = |v: i128| BigInt::from(v);
            let check = |v: i128, num: BigInt| {
                let v = big(v.abs());
                assert!(&v * &v * &s <= &num * &num && &num * &num < (&v + 1) * (&v + 1) * &s, "q {q} k {k:?}");
            };
            check(p[0], big(2) * big(q as i128).pow(3));
            for c in 0..2 {
                check(p[1 + c], big(2) * big(q2) * big(k[c].abs() as i128));
                assert_eq!(p[1 + c].signum(), (k[c] as i128).signum(), "antisymmetric");
            }
            assert_eq!(four_momentum_v1(3, k, q), p.map(|v| 3 * v), "linear in mass");
        }
    }
}

#[test]
fn the_newtonian_limit_is_exact() {
    for q in [1024i64, 1 << 15, 1 << 20] {
        for k in [[0i64, 0], [1, 0], [0, -1], [3, 4], [-7, 2], [30, -30]] {
            let kk = (k[0] * k[0] + k[1] * k[1]) as i128;
            let q = q as i128;
            if 3 * kk * kk >= 4 * q * q || k.iter().any(|&c| (c.abs() as i128) * kk >= q) {
                continue;
            }
            let p = four_momentum_v1(5, k, q as i64);
            assert_eq!(p, [5 * (2 * q * q + kk), 5 * 2 * q * k[0] as i128, 5 * 2 * q * k[1] as i128], "q {q} k {k:?}");
        }
    }
}

/// A slow boxed gas (|k_c| ≤ 16 at Q = 2^14, 0.001c): v1's energy is the Newtonian energy
/// above rest there, so Σm|k|² must change by exactly the energy carried. v0 is blind: Γ = F
/// for every body, its energy carry never moves.
#[test]
fn v1_ledgers_see_slow_kinetic_energy() {
    let (q, r, n) = (1i64 << 14, 64i64, 1024usize);
    let mut rng = Rng(11);
    let bodies: Vec<Body> = (0..n as i64)
        .map(|i| {
            let x = [(i % 32) * 256 + 128, (i / 32) * 256 + 128];
            let k = [rng.range(-16, 16), rng.range(-16, 16)];
            Body::new(i as u64 + 1, x, k, 1 + (i % 3), r, Response::Bounce)
        })
        .collect();
    let base = World::new(q, Some(Container { min: [0, 0], max: [8192, 8192] }), bodies).unwrap();
    let ke = |w: &World| w.bodies.iter().map(|b| b.mass as i128 * (b.k[0] as i128 * b.k[0] as i128 + b.k[1] as i128 * b.k[1] as i128)).sum::<i128>();
    let mut out = Vec::new();
    for law in [Law::Relativistic, Law::RelativisticV1] {
        let w0 = base.clone().with_law(law).unwrap();
        let mut c = Chronon::new(w0.clone(), false).unwrap();
        c.run_to(600);
        let w = c.world();
        assert!(c.log().contacts > 5000, "{law:?}: the gas must collide ({})", c.log().contacts);
        let (t0, t1, cr) = (total(&w0), total(&w), carried(&w));
        assert_eq!(t1[0] - t0[0], cr[0], "{law:?}: energy ledger");
        for a in 0..2 {
            assert_eq!(t1[1 + a] - t0[1 + a] + w.wall_momentum[a] as i128, cr[1 + a], "{law:?}: momentum ledger {a}");
        }
        out.push((ke(&w0), ke(&w), cr[0]));
    }
    let (v0, v1) = (out[0], out[1]);
    assert_eq!(v0.2, 0, "v0's energy carry is blind below 0.0055c");
    assert_eq!(v1.1 - v1.0, v1.2, "v1: the kinetic energy changes by exactly the energy carried");
    assert!(v1.2 != 0, "v1's energy ledger is live at 0.001c");
}

/// The hot mixed gas of the v0 test under v1: nothing reaches c, ledgers exact, slicing
/// invariant.
#[test]
fn v1_hot_gas_keeps_c_and_exact_ledgers() {
    let mut w0 = worlds::mixed(256, 256, 31);
    for b in &mut w0.bodies {
        b.response = Response::Bounce;
        b.k = [b.k[0] * 5 / 4, b.k[1] * 5 / 4];
    }
    let w0 = w0.with_law(Law::RelativisticV1).unwrap();
    let mut c = Chronon::new(w0.clone(), false).unwrap();
    c.run_to(4000);
    let w = c.world();
    assert!(c.log().contacts > 1000);
    assert!(w.bodies.iter().all(|b| (b.k[0] as i128).pow(2) + (b.k[1] as i128).pow(2) < (w.q as i128).pow(2)));
    let (t0, t1, cr) = (relativity::total(&w0), relativity::total(&w), relativity::carried(&w));
    assert_eq!(t1[0] - t0[0], cr[0], "energy ledger");
    for a in 0..2 {
        assert_eq!(t1[1 + a] - t0[1 + a] + w.wall_momentum[a] as i128, cr[1 + a], "momentum ledger {a}");
    }
    let mut s = Chronon::new(w0.clone(), false).unwrap();
    while s.tick() < 4000 {
        s.advance(4000, 777);
    }
    assert_eq!(s.outcome(), c.outcome());
    let mut v0 = Chronon::new(World { law: Law::Relativistic, ..w0 }, false).unwrap();
    v0.run_to(4000);
    assert_ne!(v0.outcome(), c.outcome(), "v1 is a different law version");
}
