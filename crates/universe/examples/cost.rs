use emergent_space::{binding::{cartesian, IntegerState, Rebinding}, orbit::{Orbit, OrbitKey, Scalar}};
use std::time::Instant;
fn main() {
    // A ship in a circular-ish orbit about a planet-like doll: p = 1.2e9 M, e = 0.01.
    let p = Scalar::integer(1_200_000_000);
    let key = OrbitKey::bound(p, (1u64 << 48) / 100).unwrap();
    let t0 = Instant::now();
    let n = 2000;
    for _ in 0..n { let _ = Orbit::compile(key).unwrap(); }
    println!("compile {:.1} us", t0.elapsed().as_secs_f64() * 1e6 / n as f64);
    let orbit = Orbit::compile(key).unwrap();
    let t0 = Instant::now();
    let mut st = None;
    for i in 0..n { st = Some(orbit.signed_state(Scalar::integer(1_000_000 + i as i64 * 1_000_003).scale(10).unwrap()).unwrap()); }
    println!("state {:.1} us", t0.elapsed().as_secs_f64() * 1e6 / n as f64);
    let st = st.unwrap();
    let units = (30 - 60, -15 - 60);
    let t0 = Instant::now();
    let mut s: Option<IntegerState> = None;
    for _ in 0..n { s = Some(cartesian(st, 0, false, units).unwrap()); }
    println!("cartesian {:.1} us", t0.elapsed().as_secs_f64() * 1e6 / n as f64);
    let s = s.unwrap();
    println!("{:?}", s);
    let t0 = Instant::now();
    for _ in 0..n { let _ = Rebinding::from_state(s, Scalar::integer(5), None).unwrap(); }
    println!("from_state {:.1} us", t0.elapsed().as_secs_f64() * 1e6 / n as f64);
}
