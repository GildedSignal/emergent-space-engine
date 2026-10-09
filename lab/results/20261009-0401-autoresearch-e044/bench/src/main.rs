//! ns-per-compile bench for the geodesic compiler (Orbit::compile / OrbitShape::bound).
//! Deterministic banks; FNV-1a fingerprint of everything the public surface exposes
//! (knot psis, every knot sum, crossings, increments, crossing times).
use emergent_space::orbit::{Orbit, OrbitKey, Scalar};
use std::time::Instant;

fn fnv(state: &mut u64, bytes: &[u8]) {
    for b in bytes {
        *state ^= *b as u64;
        *state = state.wrapping_mul(0x100000001b3);
    }
}
fn u64b(x: u64) -> [u8; 8] {
    x.to_le_bytes()
}

/// Everything two compiled orbits can differ by, through the public surface.
fn fingerprint(o: &Orbit, state: &mut u64) {
    let shape = o.shape();
    fnv(state, &u64b(shape.knots().len() as u64));
    for k in shape.knots() {
        fnv(state, &u64b(k.psi));
        for s in k.sums() {
            fnv(state, &u64b(s.significand() as u64));
            fnv(state, &u64b(s.exponent() as u16 as u64));
        }
    }
    fnv(state, &u64b(shape.crossings().len() as u64));
    for c in shape.crossings() {
        fnv(state, &u64b(*c as u64));
    }
    for inc in [o.period(), o.proper_period(), o.advance()] {
        let s = inc.unwrap();
        fnv(state, &u64b(s.significand() as u64));
        fnv(state, &u64b(s.exponent() as u16 as u64));
    }
    for i in 0..shape.crossings().len() {
        let t = o.crossing_time(i).unwrap();
        fnv(state, &u64b(t.significand() as u64));
        fnv(state, &u64b(t.exponent() as u16 as u64));
    }
}

#[derive(Clone)]
struct Case {
    key: OrbitKey,
    ns_median: f64,
    ns_min: f64,
    knots: usize,
}

fn splitmix(seed: &mut u64) -> u64 {
    *seed = seed.wrapping_add(0x9E3779B97F4A7C15);
    let mut z = *seed;
    z = (z ^ (z >> 30)).wrapping_mul(0xBF58476D1CE4E5B9);
    z = (z ^ (z >> 27)).wrapping_mul(0x94D049BB133111EB);
    z ^ (z >> 31)
}

/// A grid over the bound envelope: periapsis exponents x k grid, plus jitter.
/// weak = q <= 2^-18 selects the Taylor branch; strong approaches q -> 1/3.
fn bank(seed: u64, n: usize) -> Vec<OrbitKey> {
    let mut s = seed;
    let mut out = Vec::new();
    for i in 0..n {
        // periapsis exponent from 2 (q~1/4, strong) to 41 (q~2^-41, deep weak)
        let exp = 2 + (i * 39 / n.max(1)) % 40;
        // k: from just above HALF (e->1) to UNIT (circle)
        let kf = if i % 7 == 0 {
            (1u64 << 47) + (splitmix(&mut s) % (1u64 << 46)) // near-separatrix eccentric
        } else {
            (1u64 << 47) + (splitmix(&mut s) % (1u64 << 48)) // anywhere in bound range
        };
        let mant = 0x8000_0000_0000_0000u64 + (splitmix(&mut s) >> 12); // top-aligned
        let periapsis = Scalar::raw((mant >> 2) as i128, exp as i32 - 62).unwrap();
        if let Ok(key) = OrbitKey::new(periapsis, kf) {
            out.push(key);
        }
    }
    out
}

/// Held-out corners the tuning bank does not sample: branch boundaries and extremes.
fn corners() -> Vec<OrbitKey> {
    let mut out = Vec::new();
    // q exactly at the weak branch cut 2^-18, one and two quanta either side.
    for delta in [-2i128, -1, 0, 1, 2] {
        let q = Scalar::raw((1i128 << 62) + delta * (1i128 << 40), -80).unwrap();
        if let Ok(p) = q.reciprocal() {
            if let Ok(k) = OrbitKey::new(p, (3u64 << 47) + 12345) {
                out.push(k);
            }
        }
    }
    // extreme eccentricity: k = HALF + 1 (one quantum above separatrix), and HALF + 0x1234
    for exp in [3i32, 12, 25, 38] {
        if let Ok(k) = OrbitKey::new(Scalar::power_of_two(exp as i16), (1u64 << 47) + 1) {
            out.push(k);
        }
        if let Ok(k) = OrbitKey::new(Scalar::power_of_two(exp as i16), (1u64 << 47) + 0x1234) {
            out.push(k);
        }
    }
    // circle: k = UNIT
    for exp in [2i32, 6, 20, 40] {
        if let Ok(k) = OrbitKey::new(Scalar::power_of_two(exp as i16), 1u64 << 48) {
            out.push(k);
        }
    }
    // strong field (periapsis 2M), moderately eccentric
    for kf in [(2u64 << 47), (3 << 47), (1 << 48) - 7] {
        if let Ok(k) = OrbitKey::new(Scalar::power_of_two(1), kf) {
            out.push(k);
        }
    }
    out
}

fn time_bank(keys: &[OrbitKey], reps: usize, rounds: usize) -> (Vec<Case>, u64) {
    let mut cases = Vec::with_capacity(keys.len());
    let mut digest = 0xcbf29ce484222325u64;
    for key in keys {
        let mut samples: Vec<f64> = Vec::new();
        let mut knots = 0;
        let mut last = None;
        for r in 0..rounds {
            let t = Instant::now();
            for _ in 0..reps {
                last = Orbit::compile(*key).ok();
            }
            samples.push(t.elapsed().as_nanos() as f64 / reps as f64);
            if r == rounds - 1 {
                if let Some(o) = &last {
                    fingerprint(o, &mut digest);
                    knots = o.shape().knots().len();
                }
            }
        }
        samples.sort_by(|a, b| a.partial_cmp(b).unwrap());
        cases.push(Case {
            key: *key,
            ns_median: samples[samples.len() / 2],
            ns_min: samples[0],
            knots,
        });
    }
    (cases, digest)
}

fn stats(cases: &[Case]) -> (f64, f64, f64) {
    let mut v: Vec<f64> = cases.iter().map(|c| c.ns_median).collect();
    v.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let n = v.len();
    let idx = |p: usize| ((n * p) / 100).min(n - 1);
    (v[n / 2], v[idx(90)], v[idx(99)])
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mode = args.get(1).map(|s| s.as_str()).unwrap_or("tune");
    let reps: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(200);
    let rounds: usize = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(5);
    let (keys, label) = match mode {
        "tune" => (bank(0x5EED_0001, 210), "tune"),
        "heldout" => {
            let mut c = corners();
            c.extend(bank(0xC0FF_EE11, 60));
            (c, "heldout")
        }
        _ => panic!("modes: tune | heldout"),
    };
    let (cases, digest) = time_bank(&keys, reps, rounds);
    let (med, p90, p99) = stats(&cases);
    let total: f64 = cases.iter().map(|c| c.ns_median).sum();
    let total_min: f64 = cases.iter().map(|c| c.ns_min).sum();
    let total_knots: usize = cases.iter().map(|c| c.knots).sum();
    println!(
        "mode={} cases={} reps={} rounds={}",
        label,
        cases.len(),
        reps,
        rounds
    );
    println!(
        "ns_per_compile median={:.0} p90={:.0} p99={:.0} bank_total_ns={:.0} bank_total_min_ns={:.0} knots_total={} digest={:016x}",
        med, p90, p99, total, total_min, total_knots, digest
    );
    // Slowest five and the circles, for regime attribution.
    let mut by_ns = cases.clone();
    by_ns.sort_by(|a, b| b.ns_median.partial_cmp(&a.ns_median).unwrap());
    for c in by_ns.iter().take(5) {
        println!(
            "  slow: peri_exp={} k={:012x} knots={} ns={:.0}",
            c.key.periapsis.exponent(),
            c.key.k,
            c.knots,
            c.ns_median
        );
    }
    for c in cases.iter().filter(|c| c.key.k == 1u64 << 48).take(4) {
        println!(
            "  circle: peri_exp={} knots={} ns={:.0} (construction-dominated)",
            c.key.periapsis.exponent(),
            c.knots,
            c.ns_median
        );
    }
}
