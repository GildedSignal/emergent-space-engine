//! Kernel-level cost attribution, copied verbatim from crates/space/src/num.rs (exact pure fns).
fn div_word(n: u128, d: u64) -> u64 {
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
    let digit = |upper: u64, lower: u64| -> u64 {
        let mut q = (upper << 6) / (v1 + 1);
        let mut r = ((upper << 32) | (lower >> 32)) - q * v1 - (q * v0 >> 32);
        if r > i64::MAX as u64 {
            q -= 1;
            r += v;
        }
        while r >= v {
            q += 1;
            r -= v;
        }
        q
    };
    let q1 = digit(u1, u0 >> 32);
    let rem = (u1 << 32).wrapping_add(u0 >> 32).wrapping_sub(q1.wrapping_mul(v));
    let q0 = digit(rem, u0 & MASK);
    (q1 << 32) + q0
}
fn isqrt(x: u128) -> u128 {
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
const PI: i128 = 3575845210336147; // from tables (approx; cos only needs shape)
const SINE_N: usize = 13;
fn cos(psi: i128) -> i128 {
    let one: i128 = 1 << 62;
    if psi == 0 {
        return one;
    }
    let x = (2 * psi - PI) as i64;
    let x2 = ((x as i128 * x as i128) >> 62) as u64;
    // stand-in constants with the right magnitudes: 1/(r(r+1)) Q62
    let sine: [u64; SINE_N] = std::array::from_fn(|i| (one as u64 / ((i as u64 + 2) * (i as u64 + 3))));
    let mut s = one as u64;
    for r in sine.iter().rev() {
        let y = ((x2 as u128 * s as u128) >> 62) as u64;
        s = one as u64 - ((y as u128 * *r as u64 as u128) >> 62) as u64;
    }
    -((x as i128 * s as i128) >> 62)
}
fn bench(name: &str, mut f: impl FnMut(u64) -> u64) {
    // two passes: warm, then time ~0.4 s
    for i in 0..1000u64 {
        std::hint::black_box(f(i));
    }
    let t = std::time::Instant::now();
    let mut n = 0u64;
    let mut acc = 0u64;
    while t.elapsed().as_secs_f64() < 0.4 {
        for i in 0..2000u64 {
            acc ^= f(i);
        }
        n += 2000;
    }
    let ns = t.elapsed().as_secs_f64() * 1e9 / n as f64;
    println!("{name:24} {ns:7.1} ns   (acc {acc:x})");
}
fn main() {
    bench("u128/u64 div (soft)", |i| {
        let root = (1u128 << 61) + (i as u128 % 1000) * 7;
        ((1u128 << 104) / root) as u64
    });
    bench("div_word 128/64", |i| {
        let root = (1u128 << 61) + (i as u128 % 1000) * 7;
        div_word(1u128 << 104, root as u64)
    });
    bench("isqrt(u128)<<62", |i| {
        let d = (1u128 << 60) + (i as u128 % 1000) * 13;
        isqrt(d << 62) as u64
    });
    bench("u64 isqrt", |i| {
        let d = (1u64 << 60) + (i % 1000) * 13;
        d.isqrt()
    });
    bench("cos Q61->Q62", |i| {
        let psi = ((i % 3217) as i128 * PI) / 3217;
        cos(psi) as u64
    });
    bench("i128*i128 >>62", |i| {
        let a = (1i128 << 61) + i as i128;
        let b = (1i128 << 60) + (i as i128 % 97) * 3;
        ((a * b) >> 62) as u64
    });
}
