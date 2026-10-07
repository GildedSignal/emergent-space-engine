//! Standalone copies of the law's integer primitives (exact same source) timed on the
//! operand distributions quad actually sees. `mod tables_copy` holds the copied constants.
#[path = "tables_copy.rs"]
mod tables_copy;
use tables_copy::{PI, SINE, X, W};

const ONE: i128 = 1 << 62;

/// Exact copy of num.rs cos (psi in [0, pi], Q61).
pub fn cos(psi: i128) -> i128 {
    if psi == 0 {
        return ONE;
    }
    if psi == PI {
        return -ONE;
    }
    let x = (2 * psi - PI) as i64;
    let x2 = ((x as i128 * x as i128) >> 62) as u64;
    let mut s = ONE as u64;
    for r in SINE.iter().rev() {
        let y = ((x2 as u128 * s as u128) >> 62) as u64;
        s = ONE as u64 - ((y as u128 * *r as u64 as u128) >> 62) as u64;
    }
    -((x as i128 * s as i128) >> 62)
}

/// Exact copy of num.rs div_word (128/64 -> 64).
pub fn div_word(n: u128, d: u64) -> u64 {
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

pub fn isqrt_u128(x: u128) -> u128 {
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

fn median(mut v: Vec<f64>) -> f64 {
    v.sort_by(|a, b| a.partial_cmp(b).unwrap());
    v[v.len() / 2]
}

pub fn run() {
    use std::hint::black_box;
    use std::time::Instant;
    let reps = 3000;

    // ---- operand distributions from real panels -------------------------------
    // psi nodes: panels of width pi/4 between cuts across [0, pi], four GL nodes each.
    let mut psis: Vec<i128> = Vec::new();
    let mut n_panels = 0;
    for seg in 0..64 {
        let a = PI * seg / 64;
        let b = PI * (seg + 1) / 64;
        let mid = a + (b - a) / 2;
        for j in 0..2 {
            let dx = (X[j] * (b - a)) >> 63;
            for psi in [mid - dx, mid + dx] {
                psis.push(psi);
            }
        }
        n_panels += 1;
    }

    // x = k + (1-k) cos psi for a weak eccentric orbit: k ~ 0.55
    let k: i128 = (0.55 * (1u64 << 62) as f64) as i128;
    let xs: Vec<i128> = psis.iter().map(|&p| k + (((ONE - k) * cos(p)) >> 62)).collect();
    let floors: Vec<u128> = vec![(2 * k - 1).max(1) as u128; psis.len()];

    // fast-path divisors: root in [2^31, 2^62], horizon in (0, 2^62], a in (0, 6*2^62)
    let mut roots: Vec<u128> = Vec::new();
    for i in 0..psis.len() {
        let d = (ONE - (psis[i] % (ONE / 4))) as u128;
        roots.push(isqrt_u128(d << 62));
    }

    // ---- timings ---------------------------------------------------------------
    let t = Instant::now();
    let mut acc = 0i128;
    for _ in 0..reps {
        for &p in psis.iter() {
            acc = acc.wrapping_add(cos(p));
        }
    }
    black_box(acc);
    let ns_cos = t.elapsed().as_nanos() as f64 / (reps * psis.len()) as f64;

    let t = Instant::now();
    let mut acc2 = 0u64;
    for _ in 0..reps {
        for (i, &x) in xs.iter().enumerate() {
            acc2 = acc2.wrapping_add(div_word(floors[i] << 62, x as u64));
        }
    }
    black_box(acc2);
    let ns_divword = t.elapsed().as_nanos() as f64 / (reps * xs.len()) as f64;

    let t = Instant::now();
    let mut acc3 = 0u64;
    for _ in 0..reps {
        for (i, &x) in xs.iter().enumerate() {
            acc3 = acc3.wrapping_add((((floors[i]) << 62) / x as u128) as u64);
        }
    }
    black_box(acc3);
    let ns_u128div = t.elapsed().as_nanos() as f64 / (reps * xs.len()) as f64;

    let t = Instant::now();
    let mut acc4 = 0u128;
    for _ in 0..reps {
        for &r in roots.iter() {
            acc4 += (1u128 << 104) / r;
        }
    }
    black_box(acc4);
    let ns_fast_g = t.elapsed().as_nanos() as f64 / (reps * roots.len()) as f64;

    let t = Instant::now();
    let mut acc5 = 0u128;
    for _ in 0..reps {
        for &r in roots.iter() {
            acc5 += isqrt_u128(r << 62);
        }
    }
    black_box(acc5);
    let ns_isqrt = t.elapsed().as_nanos() as f64 / (reps * roots.len()) as f64;

    // one whole weak panel, exactly as weak_quad computes it (minus counters)
    let term = 0i128;
    let t = Instant::now();
    let mut acc6 = 0i128;
    for _ in 0..reps {
        for seg in 0..64 {
            let a = PI * seg / 64;
            let b = PI * (seg + 1) / 64;
            let mid = a + (b - a) / 2;
            let h = b - a;
            let mut sum = [0i128; 4];
            for j in 0..2 {
                let dx = (X[j] * h) >> 63;
                let w = (W[j] * h) >> 63;
                for psi in [mid - dx, mid + dx] {
                    let ac = ((ONE - k) * cos(psi)) >> 62;
                    let x = k + ac;
                    let excess = 3 * k + ac;
                    let ratio = div_word(((2 * k - 1).max(1) as u128) << 62, x as u64) as i128;
                    let rtau = (ratio * ratio) >> 62;
                    sum[0] += w * excess;
                    sum[1] += w * rtau;
                    sum[2] += w * ((rtau * (3 * x)) >> 62);
                    sum[3] += w * ((rtau * (excess - term)) >> 62);
                }
            }
            acc6 = acc6.wrapping_add(sum[0] + sum[3]);
        }
    }
    black_box(acc6);
    let ns_weak_panel = t.elapsed().as_nanos() as f64 / (reps * 64) as f64;

    println!(
        "ops: cos {ns_cos:.1}  div_word {ns_divword:.1}  u128/ {ns_u128div:.1}  fast(1<<104)/root {ns_fast_g:.1}  isqrt {ns_isqrt:.1}  weak_panel_total {ns_weak_panel:.1} ns (panels {n_panels})"
    );
}
