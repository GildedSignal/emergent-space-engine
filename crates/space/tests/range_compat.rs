//! Before/after fingerprints for the retained Q48 domain. The key's derived
//! Hash implementation is deliberately excluded: only canonical readouts count.
use emergent_space::binding::{IntegerState, Rebinding};
use emergent_space::orbit::{Orbit, OrbitKey, Passage, Scalar};
fn feed(hash: &mut u64, value: impl std::fmt::Debug) {
    for b in format!("{value:?}").bytes() {
        *hash = (*hash ^ b as u64).wrapping_mul(1099511628211);
    }
}
#[test]
fn retained_domain_fingerprint() {
    let mut hash = 14695981039346656037u64;
    let mut count = 0;
    for re in [4, 8, 19, 28, 40, 80] {
        for word in [
            1 << 20,
            (1 << 20) + 1,
            1 << 24,
            1 << 36,
            (1 << 47) - 1,
            1 << 47,
            (1 << 47) + 1,
            3 << 46,
            1 << 48,
        ] {
            let key = OrbitKey::new(Scalar::power_of_two(re), word).unwrap();
            if key.periodic() {
                match Orbit::compile(key) {
                    Ok(o) => {
                        for j in -10..=10 {
                            let t = o
                                .period()
                                .unwrap()
                                .mul(Scalar::integer(j))
                                .unwrap()
                                .scale(-3)
                                .unwrap();
                            feed(&mut hash, o.signed_state(t));
                            count += 1;
                        }
                    }
                    Err(e) => feed(&mut hash, e),
                }
            } else {
                match Passage::compile(key, key.periapsis.scale(14).unwrap()) {
                    Ok(p) => {
                        for j in -10..=10 {
                            let t = p
                                .duration()
                                .unwrap()
                                .mul(Scalar::integer(j))
                                .unwrap()
                                .scale(-5)
                                .unwrap();
                            feed(&mut hash, p.state(t));
                            count += 1;
                        }
                    }
                    Err(e) => feed(&mut hash, e),
                }
            }
        }
    }
    // Inverse compilation, including the carried clock gap, near the old cutoff.
    for r in [1000, 1000000, 100000000, 268000000] {
        for speed in [1i64 << 50, 1 << 55, 1 << 58, 1 << 59, (1 << 60) - (1 << 42)] {
            let st = IntegerState {
                position: [r, 0],
                velocity: [speed / 5, speed],
                length_exponent: 0,
                velocity_exponent: -60,
            };
            match Rebinding::from_state(st, Scalar::ZERO, None) {
                Ok(b) => {
                    let k = b.trajectory.key();
                    feed(
                        &mut hash,
                        (
                            k.periapsis,
                            k.k,
                            k.gap,
                            b.periapsis_time,
                            b.periapsis_angle,
                            b.residual,
                        ),
                    );
                    for t in [-r, 0, r] {
                        feed(&mut hash, b.trajectory.state(Scalar::integer(t)));
                        count += 1;
                    }
                }
                Err(e) => feed(&mut hash, e),
            }
        }
    }
    println!("retained_domain count={count} digest={hash:016x}");
    // Recorded on ac1a0a4a, before changing the representation.
    assert_eq!((count, hash), (948, 0xc0e57acda1dfa0ce));
}
