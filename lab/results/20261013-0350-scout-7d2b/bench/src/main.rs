// Division primitives for the kick's compile path, priced and fuzzed.
// Standalone: no dependency on the crate, so the shipped div_word is copied verbatim
// (from crates/space/src/num.rs) and cross-checked only against hardware `/`.
use std::time::Instant;

/// Verbatim copy of the shipped div_word (debug_assert stripped).
#[inline(never)]
fn div_word_sb(n: u128, d: u64) -> u64 {
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

/// Precomputed reciprocal: v = d << s (normalized to [2^63, 2^64)), m = floor(2^127 / v).
struct Recip {
    v: u64,
    m: u64,
    s: u32,
}

/// The reciprocal itself costs one schoolbook division (the cold case).
fn recip_new(d: u64) -> Recip {
    let s = d.leading_zeros();
    let v = d << s;
    Recip { v, m: div_word_sb(1u128 << 127, v), s }
}
#[inline(never)]
fn div_recip(n: u128, r: &Recip) -> u64 {
    let u = n << r.s;
    debug_assert!(u >= n); // precondition guarantees the shift fits (same as div_word)
    let (u1, u0) = ((u >> 64) as u64, u as u64);
    // q̂ = floor(m·u/2^127), computed as two u128 products (no 192-bit intermediate).
    let mut q = ((r.m as u128 * u1 as u128) >> 63) + ((r.m as u128 * u0 as u128) >> 127);
    let v = r.v as u128;
    let mut rem = u.wrapping_sub(q * v);
    while rem >= v {
        q += 1;
        rem -= v;
    }
    q as u64
}

/// The compiler's default: full 128/128 software division.
#[inline(never)]
fn div_libcall(n: u128, d: u64) -> u64 {
    (n / d as u128) as u64
}

fn pcg(state: &mut u64) -> u64 {
    *state = state.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
    let x = state.wrapping_mul(2685821657736338717);
    x ^ (x >> 32)
}

/// Precondition-satisfying pair: (n >> 64) < d.
fn pair(state: &mut u64, adversarial: bool) -> (u128, u64) {
    if adversarial {
        let d = match pcg(state) % 4 {
            0 => (1u64 << 63) - 1 + (pcg(state) % 2) as u64, // 2^63-1 or 2^63
            1 => u64::MAX - pcg(state) % 8,
            2 => (1u64 << 62) | (pcg(state) as u64 & ((1 << 62) - 1)), // high bit at 62
            _ => 1 + pcg(state) % (1 << 20), // small divisors, early path of div_word
        };
        let qmax = if d >= 1 { (u128::MAX >> 64) / d as u128 } else { 0 };
        if qmax == 0 {
            return (pcg(state) as u128, 1);
        }
        let q = pcg(state) as u128 % (qmax + 1);
        let r = (pcg(state) as u128).wrapping_rem(d as u128); // near-multiples
        ((q * d as u128 + r).min(d as u128 * (1u128 << 64) - 1), d)
    } else {
        let d = 1 + pcg(state) % u64::MAX;
        let hi = (pcg(state) as u128) % d as u128; // n >> 64 < d
        let lo = ((pcg(state) as u128) << 64) | (pcg(state) as u128);
        ((hi << 64) | (lo & u64::MAX as u128), d)
    }
}

fn main() {
    let mut state = 0x853c49e6748fea9b;
    // ---- Fuzz: bit identity of every implementation vs hardware `/`.
    let n_cases = 10_000_000u64;
    let mut mism_sb = 0u64;
    let mut mism_recip = 0u64;
    let mut max_corr = 0i64;
    let mut sum = 0u128; // checksum, also defeats elision later
    for i in 0..n_cases {
        let (n, d) = pair(&mut state, i % 4 == 0);
        let truth = div_libcall(n, d);
        let sb = div_word_sb(n, d);
        let r = recip_new(d);
        let rq = div_recip(n, &r);
        if sb != truth {
            mism_sb += 1;
        }
        if rq != truth {
            mism_recip += 1;
        }
        // correction-loop length census (curiosity: bound the loop)
        let u = n << r.s;
        let q0 = ((r.m as u128 * ((u >> 64) as u64 as u128)) >> 63)
            + ((r.m as u128 * (u as u64 as u128)) >> 127);
        max_corr = max_corr.max(truth as i64 - q0 as i64);
        sum = sum.wrapping_add(truth as u128);
    }
    println!("fuzz cases            : {n_cases}");
    println!("mismatches schoolbook : {mism_sb}");
    println!("mismatches reciprocal : {mism_recip}");
    println!("max correction steps  : {max_corr}");
    println!("checksum              : {sum:x}");

    // ---- Timing.
    const M: usize = 1 << 20;
    let mut ns = Vec::with_capacity(M);
    let mut ds = Vec::with_capacity(M);
    for _ in 0..M {
        let (n, d) = pair(&mut state, false);
        ns.push(n);
        ds.push(d);
    }
    let mut time_it = |name: &str, f: &mut dyn FnMut() -> u128| {
        // warmup
        for _ in 0..3 {
            f();
        }
        let mut best = f64::INFINITY;
        for _ in 0..5 {
            let t = Instant::now();
            let s = f();
            let dt = t.elapsed().as_secs_f64();
            best = best.min(dt);
            if s == 42_424_242 {
                println!("."); // never
            }
        }
        println!("{name:24}: {:6.2} ns/op  ({:6.1} ms/M)", best / M as f64 * 1e9, best * 1e3);
    };

    // Native u64/u64 control (same dividend class: hi part only).
    time_it("u64/u64 native (control)", &mut || {
        let mut a = 0u128;
        for i in 0..M {
            let hi = (ns[i] >> 64) as u64;
            a = a.wrapping_add((hi / ds[i]) as u128);
        }
        a
    });
    // The compiler's default on the fast_quad sites.
    time_it("u128/u128 `/` (libcall)", &mut || {
        let mut a = 0u128;
        for i in 0..M {
            a = a.wrapping_add(div_libcall(ns[i], ds[i]) as u128);
        }
        a
    });
    // The shipped primitive.
    time_it("div_word (shipped)", &mut || {
        let mut a = 0u128;
        for i in 0..M {
            a = a.wrapping_add(div_word_sb(ns[i], ds[i]) as u128);
        }
        a
    });
    // Reciprocal, cold: reciprocal rebuilt per division (worst case, no repetition).
    time_it("reciprocal, cold", &mut || {
        let mut a = 0u128;
        for i in 0..M {
            let r = recip_new(ds[i]);
            a = a.wrapping_add(div_recip(ns[i], &r) as u128);
        }
        a
    });
    // Reciprocal, amortized: one divisor repeated M times (the repetition ceiling).
    time_it("reciprocal, amortized", &mut || {
        let mut a = 0u128;
        let r = recip_new(ds[0]);
        for i in 0..M {
            a = a.wrapping_add(div_recip(ns[i], &r) as u128);
        }
        a
    });
    // Mixed reality check: divisor changes every 8 divisions.
    time_it("reciprocal, 8x repeat", &mut || {
        let mut a = 0u128;
        for c in 0..M / 8 {
            let r = recip_new(ds[c]);
            for j in 0..8 {
                let i = c * 8 + j;
                a = a.wrapping_add(div_recip(ns[i], &r) as u128);
            }
        }
        a
    });
}
