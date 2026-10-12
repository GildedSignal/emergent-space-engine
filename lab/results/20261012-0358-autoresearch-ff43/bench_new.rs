//! TEMPORARY (20261012-0358-autoresearch-ff43): microbench of OrbitShape::new and bound.
use emergent_space::orbit::{OrbitKey, Scalar};

fn main() {
    // A weak-field eccentric orbit like the plane's ships: q below 2^-18, e around 0.6.
    let mut seed = 0x243F6A8885A308D3u64;
    let mut next = || {
        seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1);
        seed
    };
    let keys: Vec<OrbitKey> = (0..512)
        .map(|_| {
            let k = (1u64 << 47) + 1 + (next() % ((1 << 47) - 2));
            OrbitKey::new(Scalar::integer(1 << 30).add(Scalar::integer((next() % 4096) as i64)).unwrap(), k).unwrap()
        })
        .collect();
    // warm
    for k in &keys[..8] {
        let _ = emergent_space::orbit::debug_bound(k);
    }
    let t = std::time::Instant::now();
    let mut acc = 0u128;
    for k in &keys {
        acc = acc.wrapping_add(emergent_space::orbit::debug_new_ns(k) as u128);
    }
    let dt = t.elapsed();
    println!(
        "512 builds: {:?} total, new-ns sum {} (avg {} ns/build)",
        dt,
        acc,
        acc / 512
    );
    let t = std::time::Instant::now();
    for k in &keys {
        let _ = emergent_space::orbit::debug_bound(k);
    }
    println!("bound full: {:?} for 512 (avg {} ns)", t.elapsed(), t.elapsed().as_nanos() / 512);
    let _ = acc;
}
