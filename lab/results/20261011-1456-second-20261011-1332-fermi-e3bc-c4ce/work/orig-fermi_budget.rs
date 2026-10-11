//! Fermi-lens bench for run 20261011-1332-fermi-e3bc: the per-event cost ladder of the
//! geodesic compiler at 10^9-body budget scale. Orders of magnitude only (Linux/x86 here;
//! the integrator re-measures on the M1). Everything is deterministic: one fixed seed.
//!
//! Measures: (1) Orbit::compile on belt/planet-range keys, split by eccentricity;
//! (2) ShapeMemo hit cost; (3) Orbit::state readout cost; (4) the integer kick floor;
//! (5) bytes per compiled cycle; (6) memo-key collapse for belt-like samples.
use emergent_space::orbit::{Knot, Orbit, OrbitKey, ShapeMemo};
use emergent_space::scaled::Scalar;
use std::collections::HashSet;
use std::time::Instant;

/// Deterministic xorshift64*.
struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        let mut x = self.0;
        x ^= x >> 12;
        x ^= x << 25;
        x ^= x >> 27;
        self.0 = x;
        x.wrapping_mul(0x2545F4914F6CDD1D)
    }
    fn unit(&mut self) -> f64 {
        (self.next() >> 11) as f64 / (1u64 << 53) as f64
    }
}

/// p in M units as an exact dyadic Scalar on a 2^-30 grid.
fn periapsis(r: &mut Rng, lo: f64, hi: f64) -> Scalar {
    let p = lo + r.unit() * (hi - lo);
    let bits = (p * (1u64 << 30) as f64) as i128;
    Scalar::raw(bits, -30).expect("periapsis in range")
}

/// Belt/planet-range key (B11: p 20-1000 M, e <= 0.6). e given explicitly.
fn key_in(r: &mut Rng, lo: f64, hi: f64, e: f64) -> OrbitKey {
    let e_q48 = (e * (1u64 << 48) as f64) as u64;
    OrbitKey::bound(periapsis(r, lo, hi), e_q48).expect("bound key")
}

fn ns_per(total: std::time::Duration, n: u64) -> f64 {
    total.as_secs_f64() * 1e9 / n as f64
}

fn main() {
    println!("fermi_budget: one fixed seed, orders of magnitude only");
    let mut rng = Rng(0x2026_1011_1332_e3bc);

    // ---- (1) compile cost, split by eccentricity -----------------------------
    for (name, elo, ehi) in [("circular-ish e<0.2", 0.0, 0.2), ("eccentric 0.2-0.6", 0.2, 0.6)] {
        let n = 1_000u64;
        let mut errors = 0u64;
        let mut knots = 0usize;
        let t = Instant::now();
        let mut max_state = None;
        for _ in 0..n {
            let e = elo + rng.unit() * (ehi - elo);
            let key = key_in(&mut rng, 20.0, 1000.0, e);
            match Orbit::compile(key) {
                Ok(orbit) => {
                    knots += orbit.shape().knots().len();
                    if max_state.is_none() {
                        max_state = Some(orbit);
                    }
                }
                Err(_) => errors += 1,
            }
        }
        let d = t.elapsed();
        println!(
            "compile[{name}]: {:.1} ns each ({} compiles, {} errors, ~{:.0} knots/orbit)",
            ns_per(d, n - errors),
            n,
            errors,
            knots as f64 / (n - errors.max(1)) as f64
        );
    }

    // ---- (2) ShapeMemo hit cost ----------------------------------------------
    let key = key_in(&mut rng, 100.0, 200.0, 0.3);
    let mut memo = ShapeMemo::default();
    let _ = memo.get(key).expect("first compile");
    let n = 200_000u64;
    let t = Instant::now();
    let mut sink = 0u64;
    for i in 0..n {
        let orbit = memo.get(key).expect("memo hit");
        sink = sink.wrapping_add(orbit.shape().knots().len() as u64 + i % 1);
    }
    let d = t.elapsed();
    println!("shape_memo_hit: {:.1} ns each (sink {sink})", ns_per(d, n));

    // ---- (3) Orbit::state readout --------------------------------------------
    let orbit = Orbit::compile(key_in(&mut rng, 100.0, 200.0, 0.3)).expect("compile");
    let period = orbit.period().expect("period");
    let n = 200_000u64;
    let mut sink = 0i128;
    let t = Instant::now();
    for i in 0..n {
        let frac = Scalar::raw(rng.next() as i128 >> 12, -52).expect("fraction");
        let elapsed = period.mul(frac).expect("elapsed");
        let st = orbit.state(elapsed).expect("state");
        sink = sink.wrapping_add(st.radius.significand() as i128 + (i % 1) as i128);
    }
    let d = t.elapsed();
    println!("orbit_state_eval: {:.1} ns each (sink {sink})", ns_per(d, n));


    // Overhead control for the eval loop above: same RNG + Scalar raw + mul, no state().
    let n = 200_000u64;
    let mut sink2 = 0i128;
    let t = Instant::now();
    for i in 0..n {
        let frac = Scalar::raw(rng.next() as i128 >> 12, -52).expect("fraction");
        let elapsed = period.mul(frac).expect("elapsed");
        sink2 = sink2.wrapping_add(elapsed.significand() as i128 + (i % 1) as i128);
    }
    let d = t.elapsed();
    println!("eval_overhead_control: {:.1} ns each (sink {sink2})", ns_per(d, n));
    // ---- (4) integer kick floor: (E, L) += (dE, dL) on a packed array ---------
    let n = 10_000_000u64;
    let mut el = vec![[0i64; 2]; 4096];
    let t = Instant::now();
    let mut r2 = Rng(0xfeed_face_cafe_1234);
    for i in 0..n as usize {
        let b = &mut el[i & 4095];
        b[0] = b[0].wrapping_add((r2.next() >> 48) as i64 as i64);
        b[1] = b[1].wrapping_add((r2.next() >> 48) as i64);
    }
    let d = t.elapsed();
    let sink: i64 = el.iter().map(|b| b[0] ^ b[1]).sum();
    println!("integer_kick_floor: {:.2} ns each (sink {sink})", ns_per(d, n));

    // ---- (5) bytes per compiled cycle ----------------------------------------
    for e in [0.01, 0.3, 0.6] {
        let key = key_in(&mut rng, 100.0, 200.0, e);
        if let Ok(orbit) = Orbit::compile(key) {
            let shape = orbit.shape();
            let knots_b = shape.knots().len() * std::mem::size_of::<Knot>();
            let cross_b = shape.crossings().len() * std::mem::size_of::<usize>();
            let base = std::mem::size_of::<emergent_space::orbit::OrbitShape>();
            println!(
                "cycle_bytes[e={e}]: {} knots + {} crossings = ~{} B per cycle (Knot = {} B)",
                shape.knots().len(),
                shape.crossings().len(),
                knots_b + cross_b + base,
                std::mem::size_of::<Knot>()
            );
        }
    }

    // ---- (6) memo-key collapse for belt-like samples --------------------------
    for (name, plo, phi, elo, ehi, n) in [
        ("narrow belt (p 1 octave, e 0-0.6)", 100.0, 200.0, 0.0, 0.6, 100_000usize),
        ("wide field (p 20-1000, e 0-0.6)", 20.0, 1000.0, 0.0, 0.6, 100_000usize),
        ("fleet clump (p 1%, e 0.01)", 100.0, 101.0, 0.0, 0.01, 100_000usize),
    ] {
        let mut raw = HashSet::new();
        let mut memoed = HashSet::new();
        let mut errors = 0usize;
        for _ in 0..n {
            let e = elo + rng.unit() * (ehi - elo);
            let key = key_in(&mut rng, plo, phi, e);
            raw.insert(key);
            match key.memo_key() {
                Ok(m) => {
                    memoed.insert(m);
                }
                Err(_) => errors += 1,
            }
        }
        println!(
            "memo_collapse[{name}]: {n} keys -> {} raw distinct, {} memo distinct (collapse {:.1}x, {} errors)",
            raw.len(),
            memoed.len(),
            n as f64 / memoed.len() as f64,
            errors
        );
    }
}
