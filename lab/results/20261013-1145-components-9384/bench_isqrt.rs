// Standalone A/B of the law's exact isqrt(u128) primitive (crates/space/src/num.rs).
// The shipped algorithm is copied verbatim (it is self-contained); candidates must return
// the same bits everywhere (isqrt = floor(sqrt(x)) is a unique integer).
// rustc -O bench_isqrt.rs -o bench_isqrt && ./bench_isqrt
use std::time::Instant;

fn div_word(n: u128, d: u64) -> u64 {
    // verbatim from crates/space/src/num.rs (exact 128/64, quotient fits u64)
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

/// SHIPPED: verbatim crates/space/src/num.rs:45.
fn isqrt_shipped(x: u128) -> u128 {
    if x < 2 {
        return x;
    }
    let shift = (128 - x.leading_zeros()).saturating_sub(64).div_ceil(2) * 2;
    let top = (x >> shift) as u64;
    let mut y = top.isqrt() as u128 + 1;
    y <<= shift / 2;
    loop {
        let z = (y + x / y) >> 1;
        if z >= y {
            return y;
        }
        y = z;
    }
}

/// CANDIDATE B: f64 seed (correctly rounded sqrt, relative error < 2^-51), one integer
/// Newton step by the exact 128/64 word division, then exact square fix-up loops.
fn isqrt_b(x: u128) -> u128 {
    if x < 2 || x >= 1u128 << 126 {
        return isqrt_shipped(x); // no call site reaches 2^126; keep exact regardless
    }
    let mut y = ((x as f64).sqrt() as u128).max(1);
    let q = div_word(x, y as u64) as u128;
    y = (y + q) >> 1;
    while y.checked_mul(y).map_or(false, |s| s > x) {
        y -= 1;
    }
    let mut s = y + 1;
    while s.checked_mul(s).map_or(false, |t| t <= x) {
        y = s;
        s += 1;
    }
    y
}

/// CANDIDATE C: f64 seed + one Newton step by the soft u128 division, then fix-up.
fn isqrt_c(x: u128) -> u128 {
    if x < 2 {
        return x;
    }
    let mut y = ((x as f64).sqrt() as u128).max(1);
    if y > 1 {
        y = (y + x / y) >> 1;
    }
    while y.checked_mul(y).map_or(false, |s| s > x) {
        y -= 1;
    }
    let mut s = y + 1;
    while s.checked_mul(s).map_or(false, |t| t <= x) {
        y = s;
        s += 1;
    }
    y
}

fn reference(x: u128) -> u128 {
    // slow but certainly exact: Newton from x itself in u256-ish via u128 (start wide)
    if x < 2 {
        return x;
    }
    let mut y = (x >> 1) + 1;
    loop {
        let z = (y + x / y) >> 1;
        if z >= y {
            break;
        }
        y = z;
    }
    while y.checked_mul(y).map_or(false, |s| s > x) {
        y -= 1;
    }
    let mut s = y + 1;
    while s.checked_mul(s).map_or(false, |t| t <= x) {
        y = s;
        s += 1;
    }
    y
}

struct Lcg(u128);
impl Lcg {
    fn next(&mut self) -> u128 {
        self.0 = self
            .0
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        self.0 ^ (self.0 >> 64)
    }
}

fn fuzz() {
    let cases: Vec<(&str, Box<dyn Fn(u128, u64, u128) -> u128>)> = vec![
        ("uniform", Box::new(|r, _i, _j| r)),
        ("fastquad: (d<<62), d<2^62", Box::new(|r, _i, _j| (r % (1u128 << 62)) << 62 | (r >> 100))),
        ("ratio_sqrt: num*den, <=2^61", Box::new(|r, _i, _j| {
            let a = r % (1u128 << 61);
            let b = (r >> 64) % (1u128 << 61);
            a * b
        })),
        ("squares", Box::new(|r, _i, _j| {
            let s = (r % (1u128 << 63)) as u128;
            s.wrapping_mul(s)
        })),
        ("squares-1", Box::new(|r, _i, _j| {
            let s = (r % (1u128 << 63)) as u128;
            s.wrapping_mul(s).wrapping_sub(1)
        })),
        ("squares+1", Box::new(|r, _i, _j| {
            let s = (r % (1u128 << 63)) as u128;
            s.wrapping_mul(s).wrapping_add(1)
        })),
        ("small", Box::new(|r, i, _j| r % (1 + i as u128 % 4096))),
        ("pow2 +-1", Box::new(|r, i, _j| {
            let s = 1u128 << (1 + (r % 127) as u32);
            s.wrapping_add((i % 3) as u128).wrapping_sub(1)
        })),
    ];
    let mut lcg = Lcg(0x853c49e6748fea9b);
    let n = 3_000_000u64;
    let mut mismatches = 0u64;
    for (name, gen) in &cases {
        let mut acc = 0u128;
        for i in 0..n {
            let r = lcg.next();
            let x = gen(r, i, 0);
            let want = isqrt_shipped(x);
            let refd = reference(x);
            debug_assert_eq!(want, refd, "reference vs shipped disagree on {x}");
            let (b, c) = (isqrt_b(x), isqrt_c(x));
            if b != want || c != want {
                mismatches += 1;
                if mismatches < 10 {
                    eprintln!("MISMATCH {name} x={x}: want {want} b {b} c {c}");
                }
            }
            acc ^= want;
        }
        println!("fuzz {name}: {n} cases ok (acc {acc:x})");
    }
    // edge corners
    for x in [
        0u128,
        1,
        2,
        3,
        4,
        u128::MAX,
        u128::MAX - 1,
        (1u128 << 126),
        (1u128 << 126) - 1,
        (1u128 << 126) + 1,
        (1u128 << 127) - 1,
        (1u128 << 64) - 1,
        (1u128 << 64),
        (1u128 << 63),
        (1u128 << 62),
    ] {
        let want = isqrt_shipped(x);
        assert_eq!(reference(x), want, "edge {x}");
        assert_eq!(isqrt_b(x), want, "edge b {x}");
        assert_eq!(isqrt_c(x), want, "edge c {x}");
    }
    println!("edges ok; total mismatches: {mismatches}");
}

fn bench(name: &str, f: fn(u128) -> u128, xs: &[u128]) {
    // ~5M evaluations, checksummed so nothing is deleted
    let reps = 5_000_000u64;
    let t = Instant::now();
    let mut acc = 0u128;
    let n = xs.len() as u64;
    for r in 0..reps {
        let x = xs[(r % n) as usize];
        acc = acc.wrapping_add(f(x));
    }
    let d = t.elapsed().as_secs_f64();
    println!(
        "{name:34} {:8.1} ns/op  (acc {:x}, {:.2} M ops)",
        d / reps as f64 * 1e9,
        acc,
        reps as f64 / d / 1e6
    );
}

fn main() {
    let mode = std::env::args().nth(1).unwrap_or_default();
    if mode == "fuzz" {
        fuzz();
        return;
    }
    // operand distributions straight from the compile's call sites:
    // fast_quad: isqrt((denominator as u128) << 62), denominator in (0, 2^62)
    // ratio_sqrt: isqrt(num * den), num, den in [0, 2^61)
    // lib.rs fit: isqrt(((ONE - 6*beta) as u128) << 62), isqrt((v as u128) << 34), ...
    let mut lcg = Lcg(0x9e3779b97f4a7c15);
    let mut quad: Vec<u128> = (0..4096).map(|_| (lcg.next() % (1u128 << 62)) << 62 | (lcg.next() >> 120)).collect();
    let mut ratio: Vec<u128> = (0..4096)
        .map(|_| {
            let a = lcg.next() % (1u128 << 61);
            let b = lcg.next() % (1u128 << 61);
            a * b
        })
        .collect();
    // one distribution: mix both (the compile hits fast_quad per node, ratio_sqrt per cut)
    let mut mix: Vec<u128> = Vec::new();
    for i in 0..4096 {
        mix.push(quad[i]);
        mix.push(ratio[i]);
    }
    for (name, xs) in [("fastquad-domain", &quad), ("ratio-domain", &ratio), ("mixed", &mix)] {
        println!("-- {name} ({} operands)", xs.len());
        bench("shipped (u64seed + soft u128 divs)", isqrt_shipped, xs);
        bench("B: f64 seed + div_word + fixup", isqrt_b, xs);
        bench("C: f64 seed + soft div + fixup", isqrt_c, xs);
    }
    // fixup-length census on the mixed domain (how far the seed lands)
    let mut hist = [0u64; 16];
    for &x in &mix {
        if x < 2 {
            continue;
        }
        let seed = ((x as f64).sqrt() as u128).max(1);
        let y = isqrt_b(x);
        let d = (seed as i128 - y as i128).unsigned_abs() as usize;
        hist[d.min(15)] += 1;
    }
    println!("seed error histogram |f64seed - isqrt| (0..=15+): {hist:?}");
}
