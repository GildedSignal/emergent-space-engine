//! Autoresearch bench (run 20261012-0036): ns per orbit compile, bit-identity hash.
//! Usage: cargo run --release -p emergent-space --example bench_compile -- [reps] [corpus]
//! corpus: main | heldout
use emergent_space::orbit::{Orbit, OrbitKey, Scalar};
use std::time::Instant;
fn lcg(state: &mut u64) -> u64 {
    *state = state.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
    *state
}
/// log-uniform p in [lo, hi] M units, e in [elo, ehi) Q48.
fn keys(n: usize, seed: u64, lo: f64, hi: f64, elo: f64, ehi: f64) -> Vec<OrbitKey> {
    let mut s = seed;
    let mut out = vec![];
    while out.len() < n {
        let t = (lcg(&mut s) >> 11) as f64 / (1u64 << 53) as f64;
        let p = (lo * (hi / lo).powf(t)) as i128;
        let e = elo + (ehi - elo) * (lcg(&mut s) >> 11) as f64 / (1u64 << 53) as f64;
        if let Ok(k) = OrbitKey::bound(
            Scalar::raw(p, 0).unwrap(),
            (e * (1u64 << 48) as f64) as u64,
        ) {
            out.push(k);
        }
    }
    out
}
fn fnv(data: &[u8]) -> u128 {
    let mut h: u128 = 0xcbf29ce484222325;
    for &b in data {
        h ^= b as u128;
        h = h.wrapping_mul(0x100000001b3);
    }
    h
}
fn main() {
    let reps: usize = std::env::args().nth(1).and_then(|a| a.parse().ok()).unwrap_or(30);
    let corpus = std::env::args().nth(2).unwrap_or_else(|| "main".into());
    let ks = match corpus.as_str() {
        "heldout" => [
            keys(120, 0x5eed_1234, 3.0, 50.0, 0.90, 0.99),
            keys(120, 0x5eed_5678, 30.0, 2000.0, 0.0, 0.3),
        ]
        .concat(),
        _ => keys(300, 0x1234_5678, 4.0, 512.0, 0.0, 0.95),
    };
    // Keep only keys this law compiles (separatrix refusals are dynamical, not bench noise).
    let ks: Vec<OrbitKey> = ks
        .into_iter()
        .filter(|k| Orbit::compile(*k).is_ok())
        .collect();
    let mut hash: u128 = 0xcbf29ce484222325;
    let mut knots: usize = 0;
    for k in &ks {
        let o = Orbit::compile(*k).expect("compile");
        knots += o.shape().knots().len();
        hash = fnv(&format!("{:?}", o).as_bytes()) ^ hash.wrapping_mul(3);
    }
    // Class timing: mirror of orbit.rs variant predicates (weak q==0, fast delta>=2^30, else generic).
    let mut class = vec![0u8; ks.len()];
    let mut tot = [0u128; 3];
    let mut cnt = [0u64; 3];
    for (i, k) in ks.iter().enumerate() {
        let sk = emergent_space::orbit::ShapeKey::for_orbit(*k).unwrap();
        let kk = (sk.k as i128) << 14;
        let eta = (1i128 << 62) - kk;
        let q = if !sk.null && sk.compactness <= Scalar::power_of_two(-18) { 0 } else { sk.compactness.fixed(62).unwrap() };
        let delta = (1i128 << 62) - ((q * (6 * kk + 2 * eta)) >> 62);
        class[i] = if q == 0 && !sk.null && kk >= 1 << 61 { 0 } else if delta >= 1 << 30 { 1 } else { 2 };
    }
    let t0 = Instant::now();
    let mut per = vec![0u128; ks.len()];
    for _ in 0..reps {
        for (i, k) in ks.iter().enumerate() {
            let s = Instant::now();
            let o = Orbit::compile(*k).expect("compile");
            per[i] += s.elapsed().as_nanos();
            std::hint::black_box(&o);
        }
    }
    let el = t0.elapsed().as_nanos();
    for (i, ns) in per.iter().enumerate() {
        tot[class[i] as usize] += ns;
        cnt[class[i] as usize] += 1;
    }
    per.sort();
    let n = per.len();
    let med = per[n / 2] / reps as u128;
    let p99 = per[(n * 99) / 100] / reps as u128;
    for (name, i) in [("weak", 0), ("fast", 1), ("generic", 2)] {
        if cnt[i] > 0 {
            println!("  {:8} n={:3} mean_ns={}", name, cnt[i], tot[i] / cnt[i] as u128 / reps as u128);
        }
    }
    println!(
        "corpus={} keys={} reps={} knots/key={:.1} ns/compile: mean={:.0} median={} p99={} hash={:032x}",
        corpus,
        ks.len(),
        reps,
        knots as f64 / ks.len() as f64,
        el / (ks.len() as u128 * reps as u128),
        med,
        p99,
        hash
    );
}
