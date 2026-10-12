//! ns/compile and ns/readout of the orbit compiler, with a bit-identity hash.
//! Usage: compile-bench <tuning|heldout> [reps]
use emergent_space::orbit::{Orbit, OrbitKey, Scalar};
use std::time::Instant;

/// Deterministic LCG (u64): reproducible corpora, no external deps.
struct Lcg(u64);
impl Lcg {
    fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        self.0 >> 11
    }
    fn frac(&mut self) -> f64 {
        (self.next() as f64) / (1u64 << 53) as f64
    }
}

fn scalar_from_f64(x: f64) -> Scalar {
    // x in [1, 2^20): exact enough for corpus generation (inputs only need determinism).
    Scalar::raw((x * (1u64 << 40) as f64) as i128, -40).unwrap()
}

fn keep(k: OrbitKey) -> Option<OrbitKey> {
    // p/(1+e) must clear the strong-field boundness predicate; skip what refuses.
    Orbit::compile(k).ok()?;
    Some(k)
}
/// `which` = tuning (seed 1) or heldout (seed 2, different span: tight + extreme keys).
fn corpus(which: &str) -> Vec<OrbitKey> {
    let seed: u64 = if which == "heldout" { 2 } else { 1 };
    let mut rng = Lcg(seed.wrapping_mul(0x9E3779B97F4A7C15));
    let mut keys = Vec::new();
    if which == "heldout" {
        // Extremes first: near-circular at many scales, near-parabolic, compact.
        for j in 0..24u32 {
            let p = 2.2f64 * (1u64 << (j / 2)) as f64 * (1.0 + rng.frac());
            for &e in &[0.0f64, 0.02, 0.9, 0.99, 0.999] {
                if let Some(k) = OrbitKey::bound(scalar_from_f64(p), (e * (1u64 << 48) as f64) as u64).ok().and_then(keep) {
                    keys.push(k);
                }
            }
        }
    }
    while keys.len() < 480 {
        let j = (rng.next() % 20) as f64;
        let p = 2.5f64 * (2f64.powf(j)) * (1.0 + rng.frac());
        let e = rng.frac() * rng.frac() * 0.97; // eccentricity-biased mix
        if let Some(k) = OrbitKey::bound(scalar_from_f64(p), (e * (1u64 << 48) as f64) as u64).ok().and_then(keep) {
            keys.push(k);
        }
    }
    keys
}

fn fnv(hash: u64, bytes: &[u8]) -> u64 {
    bytes.iter().fold(hash, |h, &b| {
        (h ^ b as u64).wrapping_mul(1099511628211)
    })
}
fn hs(hash: &mut u64, s: Scalar) {
    *hash = fnv(*hash, &s.significand().to_le_bytes());
    *hash = fnv(*hash, &s.exponent().to_le_bytes());
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let which = args.get(1).map(String::as_str).unwrap_or("tuning");
    let reps: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(0);

    let keys = corpus(which);
    // Correctness first: every key compiles, hash every output bit.
    let mut orbits = Vec::new();
    let mut hash = 0xcbf29ce484222325u64;
    let mut knots = 0usize;
    for k in &keys {
        let o = Orbit::compile(*k).expect("compile");
        knots += o.shape().knots().len() + o.shape().crossings().len();
        for knot in o.shape().knots() {
            hash = fnv(hash, &knot.psi.to_le_bytes());
        }
        hs(&mut hash, o.period().unwrap());
        hs(&mut hash, o.proper_period().unwrap());
        hs(&mut hash, o.advance().unwrap());
        for i in 0..o.shape().crossings().len() {
            hs(&mut hash, o.crossing_time(i).unwrap());
        }
        orbits.push(o);
    }
    // Readout corpus: 4 fractions of the first period per orbit.
    let reads: Vec<Vec<Scalar>> = orbits
        .iter()
        .map(|o| {
            let scale = o.key().periapsis.mul(o.key().periapsis.sqrt().unwrap()).unwrap();
            (1..=4u64)
                .map(|i| scale.mul(Scalar::integer((i as i64) * 1000)).unwrap())
                .collect()
        })
        .collect();

    // Time compile: fresh compiles, no memo (the memo is the caller's business).
    let mut compile_ns = 0u128;
    let mut n_compile = 0usize;
    let creps = if reps > 0 { reps } else { 12 };
    let t0 = Instant::now();
    let mut rep = 0;
    while rep < creps || t0.elapsed().as_secs_f64() < 1.2 {
        for k in &keys {
            let s = Instant::now();
            let o = Orbit::compile(*k).expect("compile");
            compile_ns += s.elapsed().as_nanos();
            std::hint::black_box(&o);
            n_compile += 1;
        }
        rep += 1;
    }

    // Time readout.
    let mut read_ns = 0u128;
    let mut n_read = 0usize;
    let t1 = Instant::now();
    let mut rrep = 0;
    while rrep < creps.max(30) || t1.elapsed().as_secs_f64() < 1.0 {
        for (o, ts) in orbits.iter().zip(&reads) {
            for t in ts {
                let s = Instant::now();
                let st = o.state(*t).expect("state");
                read_ns += s.elapsed().as_nanos();
                std::hint::black_box(&st);
                n_read += 1;
            }
        }
        rrep += 1;
    }

    // Hash readout outputs too (bit identity includes the read path).
    for (o, ts) in orbits.iter().zip(&reads) {
        for t in ts {
            if let Ok(st) = o.state(*t) {
                hs(&mut hash, st.radius);
                hash = fnv(hash, &st.radial_angle.to_le_bytes());
                hs(&mut hash, st.advance);
                hs(&mut hash, st.proper_time);
                hs(&mut hash, st.radial_velocity);
                hs(&mut hash, st.transverse_velocity);
            }
        }
    }

    println!(
        "which={} keys={} knots/orbit={:.1} compile={:.1} ns readout={:.1} ns hash={:016x}",
        which,
        keys.len(),
        knots as f64 / keys.len() as f64,
        compile_ns as f64 / n_compile as f64,
        read_ns as f64 / n_read as f64,
        hash
    );
}
