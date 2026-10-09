//! Compile-stage split via the crate's profile feature.
use emergent_space::orbit::{Orbit, OrbitKey, Scalar};
use emergent_space::profile;
fn main() {
    let bank: Vec<(i64, u64)> = vec![
        (1_200_000_000, (1u64 << 48) / 100),
        (1_200_000_000, 0),
        (1_200_000_000, (1u64 << 48) / 10),
        (1_200_000_000, (1u64 << 48) / 2),
        (1_200_000_000, (1u64 << 48) - (1u64 << 30)),
        (16, (1u64 << 48) / 10),
        (1 << 30, (1u64 << 48) / 10),
        (1 << 52, (1u64 << 48) / 100),
    ];
    let n = 300;
    let mut names = ["roots", "cuts", "integration", "conversion"];
    for &(p, e) in &bank {
        let key = OrbitKey::bound(Scalar::integer(p), e).unwrap();
        let t0 = std::time::Instant::now();
        for _ in 0..n { let _ = Orbit::compile(key).unwrap(); }
        let total = t0.elapsed().as_secs_f64() * 1e9 / n as f64;
        let ns = profile::take();
        let parts: Vec<String> = names.iter().zip(ns.iter())
            .map(|(nm, v)| format!("{} {:.0}", nm, v as f64 / n as f64)).collect();
        println!("p {:-12} e {:.6}: total {:6.0} ns | {}", p, e as f64 / (1u64 << 48) as f64, total, parts.join(", "));
    }
}
