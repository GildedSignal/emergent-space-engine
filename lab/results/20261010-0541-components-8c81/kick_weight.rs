// P4 completion: the compiled weight one rebind materializes, across eccentricity.
use emergent_space::orbit::{Orbit, OrbitKey};
use std::time::Instant;

fn main() {
    let p = 1_200_000_000u64;
    for e100 in [1, 30, 70, 95] {
        let e_q48 = ((1u64 << 48) as u128 * e100 as u128 / 100) as u64;
        let key = OrbitKey::bound(emergent_space::orbit::Scalar::integer(p as i64), e_q48).unwrap();
        let t0 = Instant::now();
        let orbit = Orbit::compile(key).unwrap();
        let compile_us = t0.elapsed().as_secs_f64() * 1e6;
        let mut knots = 0usize;
        while orbit.crossing_state(knots, 0, true).is_ok() {
            knots += 1;
        }
        println!(
            "e=0.{e100:02}: compile {compile_us:6.1} us, knots {knots:4}, shallow orbit {} B",
            std::mem::size_of::<Orbit>()
        );
    }
    println!(
        "Binding {} B, Tube {} B, Entry {} B (a retired Segment per kick holds a Binding)",
        std::mem::size_of::<emergent_universe::bind::Binding>(),
        std::mem::size_of::<emergent_space::Tube>(),
        std::mem::size_of::<emergent_space::binding::Trajectory>(),
    );
}
