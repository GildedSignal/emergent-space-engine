//! Exact cache eviction: a history-sized clone survives eviction without pinning its table.
use emergent_space::orbit::{shape_cache_stats, Orbit, OrbitKey, Scalar};
use std::sync::Arc;

#[test]
fn evicted_history_rebuilds_bit_for_bit() {
    let key = OrbitKey::bound(Scalar::power_of_two(27), (1u64 << 48) / 5).unwrap();
    let pinned = Orbit::compile(key).unwrap();
    let mut cached = pinned.clone();
    cached.make_evictable();
    let history = cached.clone();
    assert_eq!(cached.retained_shape_bytes(), 0);
    let old_table = Arc::downgrade(&cached.shape());
    let expected: Vec<_> = [-7, -1, 0, 1, 3, 10].into_iter().map(|t| {
        let time = pinned.period().unwrap().mul(Scalar::raw(t, -2).unwrap()).unwrap();
        (time, pinned.signed_state(time).unwrap())
    }).collect();
    let expected_shape = (*pinned.shape()).clone();
    drop(pinned);
    for i in 0..5000 {
        let key = OrbitKey::bound(Scalar::power_of_two(27), (1u64 << 48) / 6 + i * 1234567).unwrap();
        let mut orbit = Orbit::compile(key).unwrap();
        orbit.make_evictable();
    }
    assert!(old_table.upgrade().is_none(), "history must not pin the old table");
    let (n, bytes, _, misses, evictions) = shape_cache_stats();
    assert!(n <= 4096 && bytes <= 8 * 1024 * 1024 && evictions > 0);
    assert_eq!(*history.shape(), expected_shape);
    assert!(shape_cache_stats().3 > misses, "read must really take the cold rebuild");
    let elsewhere = history.clone();
    let threaded = expected.clone();
    std::thread::spawn(move || {
        for (time, state) in threaded {
            assert_eq!(elsewhere.signed_state(time).unwrap(), state);
        }
        assert!(shape_cache_stats().3 > 0, "a new reader thread must rebuild independently");
    }).join().unwrap();
    for (time, state) in expected {
        assert_eq!(history.signed_state(time).unwrap(), state);
        assert_eq!(cached.signed_state(time).unwrap(), state);
    }
}

#[test]
fn scale_shares_only_the_exact_shape_and_strong_cycles_stay_pinned() {
    let a = OrbitKey::bound(Scalar::power_of_two(26), (1u64 << 48) / 8).unwrap();
    let b = OrbitKey::bound(Scalar::power_of_two(29), (1u64 << 48) / 8).unwrap();
    let mut a = Orbit::compile(a).unwrap();
    let mut b = Orbit::compile(b).unwrap();
    a.make_evictable(); b.make_evictable();
    assert!(Arc::ptr_eq(&a.shape(), &b.shape()));
    assert_ne!(a.period(), b.period());
    // Includes the symbolic-circle exception at/below the ISCO.
    for radius in [4, 6, 20] {
        let mut strong = Orbit::compile(OrbitKey::new(Scalar::integer(radius), 1 << 48).unwrap()).unwrap();
        let before = strong.state(Scalar::ONE).unwrap();
        strong.make_evictable();
        assert!(strong.retained_shape_bytes() > 0);
        assert_eq!(strong.state(Scalar::ONE).unwrap(), before);
    }
}
