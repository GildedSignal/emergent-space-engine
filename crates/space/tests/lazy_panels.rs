//! An eager reader is the control: deferred reads must return the same integer states,
//! including reflected/inbound phases, large cycle counts, read reordering and eviction.
use emergent_space::orbit::{Orbit, OrbitKey, Scalar};

#[test]
fn deferred_prefix_matches_the_eager_cycle_in_any_read_order() {
    for radius in [19, 30, 100] {
        for eccentricity in [
            0,
            (1u64 << 48) / 5,
            (1u64 << 48) * 9 / 10,
            (1u64 << 48) * 99 / 100,
        ] {
            let key = OrbitKey::bound(Scalar::power_of_two(radius), eccentricity).unwrap();
            let eager = Orbit::compile(key).unwrap();
            let period = eager.period().unwrap(); // fills the control before any reads
            let lazy = Orbit::compile(key).unwrap();
            assert_eq!(lazy.shape().integrated_panels(), 0);
            let early = key
                .periapsis
                .mul(key.periapsis.sqrt().unwrap())
                .unwrap()
                .scale(-20)
                .unwrap();
            assert_eq!(lazy.state(early).unwrap(), eager.state(early).unwrap());
            assert!(lazy.shape().integrated_panels() < lazy.shape().knots().len() - 1);
            for numerator in [7, -1, 0, 1, 8, -39, 40001, 3, 2] {
                let time = period.mul(Scalar::raw(numerator, -2).unwrap()).unwrap();
                assert_eq!(
                    lazy.signed_state(time).unwrap(),
                    eager.signed_state(time).unwrap()
                );
            }
            let mut evictable = Orbit::compile(key).unwrap();
            evictable.make_evictable();
            let threaded = evictable.clone();
            let expected = eager.signed_state(early.negate()).unwrap();
            std::thread::spawn(move || {
                assert_eq!(threaded.signed_state(early.negate()).unwrap(), expected)
            })
            .join()
            .unwrap();
        }
    }
}

#[test]
fn passage_and_scaled_tail_match_eager_reads_without_minting_unused_panels() {
    use emergent_space::orbit::Passage;
    for radius in [5, 19, 60] {
        for word in [(1u64 << 48) / 3, 1 << 47] {
            let key = OrbitKey::new(Scalar::power_of_two(radius), word).unwrap();
            let edge = key.periapsis.scale(20).unwrap();
            let eager = Passage::compile(key, edge).unwrap();
            let duration = eager.duration().unwrap();
            let lazy = Passage::compile(key, edge).unwrap();
            assert_eq!(lazy.integrated_panels(), 0);
            let early = key.periapsis.mul(key.periapsis.sqrt().unwrap()).unwrap().scale(-20).unwrap();
            assert_eq!(lazy.state(early).unwrap(), eager.state(early).unwrap());
            assert!(lazy.integrated_panels() < eager.integrated_panels());
            for n in [15, -1, 0, 1, 16, -16, 3, 2] {
                let time = duration.mul(Scalar::raw(n, -5).unwrap()).unwrap();
                assert_eq!(lazy.state(time).unwrap(), eager.state(time).unwrap());
            }
            for shift in [20, 1, 10, 19, 0] {
                let r = key.periapsis.scale(shift).unwrap();
                assert_eq!(lazy.at_radius(r).unwrap(), eager.at_radius(r).unwrap());
            }
        }
    }
    let photon = Passage::photon(Scalar::integer(20), Scalar::power_of_two(20)).unwrap().unwrap();
    let fresh = Passage::photon(Scalar::integer(20), Scalar::power_of_two(20)).unwrap().unwrap();
    let duration = photon.duration().unwrap();
    assert_eq!(fresh.state(duration.scale(-2).unwrap()).unwrap(), photon.state(duration.scale(-2).unwrap()).unwrap());
}
