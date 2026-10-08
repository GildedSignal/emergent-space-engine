use emergent_space::orbit::{Orbit, OrbitKey};
use emergent_space::scaled::Scalar;
fn main() {
    for &e in &[0.07f64, 0.5, 0.99] {
        let t0 = std::time::Instant::now();
        let n = 20000;
        for i in 0..n {
            let p = Scalar::raw((2304.0 * (1u64 << 16) as f64) as i128 + i, -16).unwrap();
            let key = OrbitKey::bound(p, (e * (1u64 << 48) as f64) as u64).unwrap();
            std::hint::black_box(Orbit::compile(key).unwrap());
        }
        println!("e={e}: {:.1} us/compile", t0.elapsed().as_secs_f64() / n as f64 * 1e6);
    }
}
