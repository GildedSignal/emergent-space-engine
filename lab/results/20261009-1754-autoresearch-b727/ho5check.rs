use emergent_space::orbit::{Orbit, OrbitKey, Scalar};
use std::time::Instant;
fn main() {
    let key = OrbitKey::bound(Scalar::integer(64), (1u64 << 48) / 3).unwrap();
    let n = 300;
    for r in 0..5 {
        let t0 = Instant::now();
        for _ in 0..n { let _ = Orbit::compile(key).unwrap(); }
        println!("strong compile {:.0} ns", t0.elapsed().as_secs_f64()*1e9/n as f64);
    }
    let key2 = OrbitKey::bound(Scalar::integer(1<<44), 0).unwrap();
    for r in 0..3 {
        let t0 = Instant::now();
        for _ in 0..n { let _ = Orbit::compile(key2).unwrap(); }
        println!("circular compile {:.0} ns", t0.elapsed().as_secs_f64()*1e9/n as f64);
    }
}
