//! Scout 20261013-0350: the kick's compile path, censused and timed.
//! Sweeps exact `Orbit::compile` over a (periapsis, eccentricity) grid, in both
//! division arms (schoolbook vs libcall), checking structural bit-identity of
//! every produced shape (derived Eq over all knots) and reporting wall time
//! plus the division census (div_word and the raw u128 `/` sites).
use emergent_space::num::census;
use emergent_space::orbit::{Orbit, OrbitKey};
use emergent_space::scaled::Scalar;
use std::time::Instant;

fn keys() -> Vec<OrbitKey> {
    let mut out = Vec::new();
    // p from just outside the separatrix to the far field (M units), e across the band.
    for p in [8u32, 12, 20, 40, 100, 400, 1500, 8192] {
        for e48 in [
            0u64,
            (0.2 * (1u64 << 48) as f64) as u64,
            (0.5 * (1u64 << 48) as f64) as u64,
            (0.7 * (1u64 << 48) as f64) as u64,
            (0.9 * (1u64 << 48) as f64) as u64,
            (0.97 * (1u64 << 48) as f64) as u64,
        ] {
            let p_scalar = Scalar::raw(p as i128, 0).unwrap();
            if let Ok(key) = OrbitKey::bound(p_scalar, e48) {
                if Orbit::compile(key).is_ok() {
                    out.push(key);
                }
            }
        }
    }
    out
}

fn main() {
    let keys = keys();
    println!("keys compiled          : {}", keys.len());

    // Census on the schoolbook arm: calls and distinct divisors per compile.
    census::configure(false, true);
    let mut per_key = Vec::new();
    for k in &keys {
        census::reset();
        let _ = Orbit::compile(*k).unwrap();
        per_key.push(census::take());
    }
    let total_divs: u64 = per_key.iter().map(|d| d.0).sum();
    let distinct_all: usize = per_key.iter().map(|d| d.1).sum();
    let total_w128: u64 = per_key.iter().map(|d| d.2).sum();
    let distinct_w128: usize = per_key.iter().map(|d| d.3).sum();
    let max_divs = per_key.iter().map(|d| d.0 + d.2).max().unwrap();
    let min_divs = per_key.iter().map(|d| d.0 + d.2).min().unwrap();
    println!(
        "div_word calls         : {total_divs} total, {} avg/compile (distinct {}, repeat frac {:.3})",
        total_divs / keys.len() as u64,
        distinct_all,
        1.0 - distinct_all as f64 / total_divs as f64
    );
    println!(
        "u128 `/` sites         : {total_w128} total, {} avg/compile (distinct {}, repeat frac {:.3})",
        total_w128 / keys.len() as u64,
        distinct_w128,
        1.0 - distinct_w128 as f64 / total_w128.max(1) as f64
    );
    println!("divisions per compile  : min {min_divs}, max {max_divs}");
    // Aggregate top divisors over the whole sweep (identifies the repeating site).
    census::reset();
    for k in &keys {
        let _ = Orbit::compile(*k).unwrap();
    }
    let (top64, top128) = census::top(4);
    for (d, c) in top64 {
        println!("  top u64 divisor   {d:>20} x{c}");
    }
    for (d, c) in top128 {
        println!("  top u128 divisor  {d:>38} x{c}");
    }

    // Bit-identity across arms via derived Eq over the whole shape.
    census::configure(false, false);
    let sb: Vec<_> = keys.iter().map(|k| Orbit::compile(*k).unwrap()).collect();
    census::configure(true, false);
    let lc: Vec<_> = keys.iter().map(|k| Orbit::compile(*k).unwrap()).collect();
    let mism = sb
        .iter()
        .zip(&lc)
        .filter(|(a, b)| a.shape() != b.shape())
        .count();
    println!("libcall mismatches     : {mism} of {}", keys.len());

    // Timing both arms (census off, HashSet cold-path absent).
    let run = || {
        let t = Instant::now();
        let mut acc = 0u128;
        for k in &keys {
            let o = Orbit::compile(*k).unwrap();
            acc = acc.wrapping_add(o.shape().knots().len() as u128);
            for kn in o.shape().knots().iter().step_by(16) {
                acc = acc.wrapping_mul(31).wrapping_add(kn.psi as u128);
            }
            std::hint::black_box(&o);
        }
        (t.elapsed(), acc)
    };
    for (name, libcall) in [("schoolbook", false), ("libcall", true)] {
        census::configure(libcall, false);
        let _ = run(); // warm
        let mut best = f64::INFINITY;
        let mut acc = 0;
        for _ in 0..7 {
            let (d, a) = run();
            best = best.min(d.as_secs_f64());
            acc = a;
        }
        println!(
            "{name:10} arm        : {:8.1} us/compile ({:>6.2} ms/sweep, {} keys) [acc {acc:x}]",
            best / keys.len() as f64 * 1e6,
            best * 1e3,
            keys.len()
        );
    }
}
