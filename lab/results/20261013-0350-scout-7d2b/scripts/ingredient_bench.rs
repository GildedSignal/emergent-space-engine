//! Scout 20261013-0350: per-node ingredient costs (isqrt, cos, the 4-div block).
use emergent_space::num::{cos, isqrt};
use std::time::Instant;

fn main() {
    let mut state = 0x243f6a8885a308d3u64;
    let mut next = || {
        state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
        state ^= state >> 33;
        state
    };
    const M: usize = 1 << 22;
    let args: Vec<u128> = (0..M).map(|_| ((next() as u128) << 64) | next() as u128).collect();
    let bench = |name: &str, f: &dyn Fn(&[u128]) -> u128| {
        f(&args); // warm
        let mut best = f64::INFINITY;
        for _ in 0..5 {
            let t = Instant::now();
            let a = f(&args);
            let d = t.elapsed().as_secs_f64();
            best = best.min(d);
            if a == 42_424_2 {
                println!();
            }
        }
        println!("{name:28}: {:6.2} ns/op", best / M as f64 * 1e9);
    };
    bench("u128 isqrt", &|a: &[u128]| {
        let mut acc = 0u128;
        for &x in a {
            acc = acc.wrapping_add(isqrt(x));
        }
        acc
    });
    // cos takes Q61 psi in [0, pi]; keep in range.
    bench("cos(psi) Q62", &|a: &[u128]| {
        let mut acc = 0u128;
        for &x in a {
            acc = acc.wrapping_add(cos((x % 7244019458077122842u128) as i128) as u128);
        }
        acc
    });
    bench("u128 mul (control)", &|a: &[u128]| {
        let mut acc = 0u128;
        for i in 1..a.len() {
            acc ^= a[i].wrapping_mul(a[i - 1]);
        }
        acc
    });
    bench("u128 >>62 (control)", &|a: &[u128]| {
        let mut acc = 0u128;
        for &x in a {
            acc ^= x >> 62;
        }
        acc
    });
}
