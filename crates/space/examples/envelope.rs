//! Scaled compiler timings and reproducible key-width/population experiment.
use emergent_space::orbit::{Orbit, OrbitKey, Scalar, ShapeKey};
use std::{collections::HashSet, hint::black_box, time::Instant};
#[allow(dead_code)]
#[path = "../../../xtask/src/behave/sample.rs"]
mod sample;
fn encode(x: f64) -> Scalar {
    let e = x.log2().floor() as i32;
    Scalar::raw((x * 2f64.powi(60 - e)).round() as i128, e - 60).unwrap()
}
fn decode(x: Scalar) -> f64 {
    x.significand() as f64 * 2f64.powi(x.exponent() as i32 - 62)
}
fn key(p: f64, e: f64) -> OrbitKey {
    OrbitKey::bound(encode(p), (e * 2f64.powi(48)).round() as u64).unwrap()
}
fn report(label: &str, mut v: Vec<u128>) {
    v.sort_unstable();
    println!(
        "{label}: n={} median_ns={} p99_ns={} max_ns={}",
        v.len(),
        v[v.len() / 2],
        v[(v.len() * 99).div_ceil(100) - 1],
        v[v.len() - 1]
    );
}
fn reference(p: f64, e: f64) -> [f64; 3] {
    let mut out = [0.0; 3];
    let pi = std::f64::consts::PI;
    let l = p / (p - 3.0 - e * e).sqrt();
    let en = (((p - 2.0).powi(2) - 4.0 * e * e) / (p * (p - 3.0 - e * e))).sqrt();
    for i in 0..8192 {
        let x = pi * (i as f64 + 0.5) / 8192.0;
        let u = (1.0 + e * x.cos()) / p;
        let g = (p / (p - 6.0 - 2.0 * e * x.cos())).sqrt();
        out[0] += g - 1.0;
        out[1] += en * g / (l * u * u * (1.0 - 2.0 * u));
        out[2] += g / (l * u * u);
    }
    out.map(|x| x * 2.0 * pi / 8192.0)
}
fn main() {
    let mut keys: Vec<_> = sample::bound_orbits(256).into_iter().map(|(p, e)| key(p, e)).collect();
    if std::env::args().any(|x| x == "--keys") {
        let want: Vec<_> = sample::bound_orbits(256).into_iter().map(|(p, e)| reference(p, e)).collect();
        let mut best = None;
        for kbits in 7..=15 {
            for pbits in 7..=15 {
                let mut count = [0; 3];
                let mut worst = [0.0f64; 2];
                for (&k, w) in keys.iter().zip(&want) {
                    let c = Orbit::compile(k.quantized(kbits, pbits).unwrap()).unwrap();
                    let a = (decode(c.advance().unwrap()) / w[0] - 1.0).abs();
                    let t = (decode(c.period().unwrap()) / w[1] - 1.0)
                        .abs()
                        .max((decode(c.proper_period().unwrap()) / w[2] - 1.0).abs());
                    count[0] += (a <= 0.01) as usize;
                    count[1] += (t <= 0.001) as usize;
                    count[2] += c.advance().unwrap().is_positive() as usize;
                    worst[0] = worst[0].max(a);
                    worst[1] = worst[1].max(t);
                }
                let pass = count[0] >= 254 && count[1] >= 254 && count[2] == 256;
                println!(
                    "key k_bits={kbits} scale_bits={pbits} G1={} G2={} G6={} worst={worst:?} pass={pass}",
                    count[0], count[1], count[2]
                );
                if pass && best.is_none_or(|(a, b)| kbits + pbits < a + b) {
                    best = Some((kbits, pbits));
                }
            }
        }
        let (kb, pb) = best.expect("a measured width passes");
        println!(
            "coarsest_in_tested_grid k_bits={kb} scale_bits={pb} total={} (exponent separate)",
            kb + pb
        );
        // This is a lookup hit rate, not a million compiles or a physical galaxy claim.
        for (kb, pb) in [(kb, pb), (12, 12)] {
            for (label, lo, hi) in [("frozen-range", 10.0, 1000.0), ("galactic-envelope", 10.0, 1e12), ("weak", 1e6, 1e12)] {
                let mut rng = sample::Rng(0x454e56454c4f5045);
                let mut shapes = HashSet::new();
                let mut bindings = HashSet::new();
                for _ in 0..1_000_000 {
                    let k = key(rng.log_uniform(lo, hi), 0.9 * rng.unit()).quantized(kb, pb).unwrap();
                    bindings.insert(k);
                    shapes.insert(ShapeKey::for_orbit(k).unwrap());
                }
                println!("population={label} shape_bits={kb} scale_bits={pb} seed=0x454e56454c4f5045 n=1000000 e=uniform[0,.9] p=loguniform[{lo},{hi}] shapes={} shape_hits={} bindings={} binding_hits={}",shapes.len(),1_000_000-shapes.len(),bindings.len(),1_000_000-bindings.len());
            }
        }
        return;
    }
    if std::env::args().any(|x| x == "--weak") {
        let mut rng = sample::Rng(0x454e56454c4f5045);
        keys = (0..256).map(|_| key(rng.log_uniform(1e4, 1e12), 0.9 * rng.unit())).collect();
        println!("sampler=weak seed=0x454e56454c4f5045 p=loguniform[1e4,1e12] e=uniform[0,.9]");
    } else {
        println!("sampler=behave bound seed={} p=loguniform[10,1000] e=uniform[0,.7]", sample::BOUND_SEED);
    }
    let cycles: Vec<_> = keys.iter().map(|&k| Orbit::compile(k).unwrap()).collect();
    let (mut compile, mut cross, mut inside) = (vec![], vec![], vec![]);
    for round in 0..16 {
        for (&key, c) in keys.iter().zip(&cycles) {
            let t = Instant::now();
            black_box(Orbit::compile(black_box(key)).unwrap());
            compile.push(t.elapsed().as_nanos());
            let index = c.shape.crossings.get(round % c.shape.crossings.len().max(1)).copied().unwrap_or(0);
            let t = Instant::now();
            black_box(c.crossing_state(black_box(index), 0, true).unwrap());
            cross.push(t.elapsed().as_nanos());
            let time = c.period().unwrap().mul(Scalar::integer(13)).unwrap().div(Scalar::integer(31)).unwrap();
            let t = Instant::now();
            black_box(c.state(black_box(time)).unwrap());
            inside.push(t.elapsed().as_nanos());
        }
    }
    report("scaled_compile", compile);
    report("scaled_crossing_state", cross);
    report("scaled_interior_state", inside);
}
