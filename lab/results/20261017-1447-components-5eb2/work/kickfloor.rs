//! Lab run 20261017-1447-components-5eb2 (lens: first principles, one component).
//! Component: the kick's refit — `Orbit::compile`, the quadrature that recompiles a body's
//! tube after every fired kick. Measures ns/compile and knots/compile on belt-class keys
//! (weak field, q = 1/2^p, near-circular to e = 0.4) and strong-field keys, and prints a
//! bit checksum of every compiled shape. Run before and after the `fast_quad` division
//! patch: identical checksums prove the patch is bit-identical, the timings price it.
use emergent_space::orbit::{Orbit, OrbitKey};
use emergent_space::scaled::Scalar;
use std::fmt::Write as _;
use std::hint::black_box;
use std::time::Instant;

fn fnv(bytes: &[u8]) -> u64 {
    let mut h = 0xcbf29ce484222325u64;
    for b in bytes {
        h ^= *b as u64;
        h = h.wrapping_mul(0x100000001b3);
    }
    h
}

/// One bench row: label, key.
fn keys() -> Vec<(String, OrbitKey)> {
    let mut out = Vec::new();
    // Belt class: periapsis 2^20..2^30 M (an AU-scale belt about a star sits around 2^24-2^28),
    // eccentricity 0..0.4 (k = 1/(1+e) in Q48).
    for p in [20i16, 24, 27, 30] {
        for e in [0u64, 1 << 43, 1 << 45, (1 << 47) / 5, (1 << 47) / 3] {
            let key = OrbitKey::bound(Scalar::power_of_two(p), e).unwrap();
            out.push((format!("belt_p{p}_e{e}"), key));
        }
    }
    // Strong field: periapsis 8..64 M.
    for p in [3i16, 4, 6] {
        for e in [0u64, 1 << 45, (1 << 47) / 3, (1 << 47) / 2] {
            let key = OrbitKey::bound(Scalar::power_of_two(p), e).unwrap();
            out.push((format!("strong_p{p}_e{e}"), key));
        }
    }
    out
}

/// div_word copied from crates/space/src/num.rs (pub(crate) there): exact 128/64 division
/// with a word-sized quotient, base 2^32, one native division per trial digit.
fn div_word(n: u128, d: u64) -> u64 {
    debug_assert!(d != 0 && (n >> 64) < d as u128);
    if n <= u64::MAX as u128 {
        return n as u64 / d;
    }
    const B: u64 = 1 << 32;
    const MASK: u64 = B - 1;
    let shift = d.leading_zeros();
    let v = d << shift;
    let (v1, v0) = (v >> 32, v & MASK);
    let u = n << shift;
    let (u1, u0) = ((u >> 64) as u64, u as u64);
    let digit = |upper: u64, lower: u64| {
        let mut q = upper / v1;
        let mut r = upper % v1;
        while q >= B || q * v0 > (r << 32) + lower {
            q -= 1;
            r += v1;
            if r >= B {
                break;
            }
        }
        q
    };
    let q1 = digit(u1, u0 >> 32);
    let rem = (u1 << 32).wrapping_add(u0 >> 32).wrapping_sub(q1.wrapping_mul(v));
    let q0 = digit(rem, u0 & MASK);
    (q1 << 32) + q0
}

fn micro() {
    // Representative fast_quad operands (Q62/Q48 scales from orbit.rs).
    let root = 1u128 << 61;
    let n1 = 1u128 << 104;
    let a = 6u128 << 48;
    let g = (n1 / root) as u64;
    let d2 = (1u128 << 62) + root;
    let n2 = a * g as u128;
    let floor = 1u128 << 46;
    let x = 1u128 << 48;
    let rtau = 1u128 << 58;
    let horizon = (1u128 << 62) - (1u128 << 40);
    const N: u32 = 2_000_000;
    let mut sink = 0u64;
    let t = Instant::now();
    for _ in 0..N {
        sink = sink.wrapping_add(((black_box(n1)) / black_box(root)) as u64);
        sink = sink.wrapping_add(((black_box(n2)) / black_box(d2)) as u64);
        sink = sink.wrapping_add(((black_box(floor << 62)) / black_box(x)) as u64);
        sink = sink.wrapping_add(((black_box(rtau << 62)) / black_box(horizon)) as u64);
    }
    let wide = t.elapsed().as_nanos() as f64 / N as f64 / 4.0;
    let t = Instant::now();
    for _ in 0..N {
        sink = sink.wrapping_add(div_word(black_box(n1), root as u64));
        sink = sink.wrapping_add(div_word(black_box(n2), d2 as u64));
        sink = sink.wrapping_add(div_word(black_box(floor << 62), x as u64));
        sink = sink.wrapping_add(div_word(black_box(rtau << 62), horizon as u64));
    }
    let word = t.elapsed().as_nanos() as f64 / N as f64 / 4.0;
    // u64 isqrt (the word_root path's square root) for the per-node budget.
    let t = Instant::now();
    for i in 0..N {
        sink = sink.wrapping_add(((1u64 << 61) + i as u64).isqrt());
    }
    let isqrt_ns = t.elapsed().as_nanos() as f64 / N as f64;
    println!("micro: wide_div={wide:.1}ns div_word={word:.1}ns isqrt64={isqrt_ns:.1}ns sink={sink}");
}

fn main() {
    micro();
    let mut rows = Vec::new();
    for (label, key) in keys() {
        let orbit = Orbit::compile(key).expect("compile");
        let knots = orbit.shape().knots().len();
        let mut text = String::new();
        write!(text, "{:?}", orbit.shape()).unwrap();
        let checksum = fnv(text.as_bytes());
        // Warm, then time a fixed number of recompiles (the rebind does exactly this).
        let reps = 30u32;
        let mut ns = Vec::with_capacity(5);
        for _ in 0..5 {
            let t = Instant::now();
            for _ in 0..reps {
                black_box(Orbit::compile(black_box(key)).unwrap());
            }
            ns.push(t.elapsed().as_nanos() as f64 / reps as f64);
        }
        ns.sort_by(|a, b| a.partial_cmp(b).unwrap());
        rows.push((label.clone(), ns[2], knots, checksum));
        println!("{label}: ns={:.0} knots={knots} sumhash={checksum:016x}", ns[2]);
    }
    let belt: Vec<&(String, f64, usize, u64)> = rows.iter().filter(|r| r.0.starts_with("belt")).collect();
    let strong: Vec<&(String, f64, usize, u64)> = rows.iter().filter(|r| r.0.starts_with("strong")).collect();
    for (name, set) in [("belt", &belt), ("strong", &strong)] {
        let mut s: Vec<f64> = set.iter().map(|r| r.1).collect();
        s.sort_by(|a, b| a.partial_cmp(b).unwrap());
        let k: Vec<usize> = set.iter().map(|r| r.2).collect();
        println!("class {name}: n={} ns median={:.0} min={:.0} max={:.0} knots {}-{}", set.len(), s[s.len() / 2], s[0], s[s.len() - 1], k.iter().min().unwrap(), k.iter().max().unwrap());
    }
}
