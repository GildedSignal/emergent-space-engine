//! Lab bench 20261010-2220: ns per orbit-compile / rebind event in `crates/space`.
//! Deterministic: fixed LCG seeds, checksum over outputs.
//! cargo run --release -p emergent-space --example lab_bench -- [mode] [rounds]
use emergent_space::{
    binding::{IntegerState, Rebinding},
    orbit::{Orbit, OrbitKey},
    scaled::Scalar,
};
use std::time::Instant;

fn lcg(state: &mut u64) -> u64 {
    *state = state
        .wrapping_mul(6364136223846793005)
        .wrapping_add(1442695040888963407);
    *state >> 11
}

fn keys_r(n: u64, seed: u64, rlo: f64, rspan: f64, elo: f64, espan: f64) -> Vec<OrbitKey> {
    let mut s = seed;
    let mut out = Vec::new();
    for _ in 0..n {
        let log_r = rlo + (lcg(&mut s) as f64 / (1u64 << 53) as f64) * rspan;
        let e = elo + (lcg(&mut s) as f64 / (1u64 << 53) as f64) * espan;
        let rp = Scalar::integer(1 << 20)
            .mul(Scalar::power_of_two((log_r - 20.0) as i16))
            .unwrap();
        let k = ((1u128 << 96) / ((1u128 << 48) + (e * (1u64 << 48) as f64) as u128)) as u64;
        out.push(OrbitKey::new(rp, k).unwrap());
    }
    out
}

fn keys(n: u64) -> Vec<OrbitKey> {
    keys_r(n, 0x853c49e6748fea9b, 4.0, 10.0, 0.0, 0.9)
}

/// Integer states near bound orbits: r in 2^5..2^13 M, near-circular with radial kick.
fn states(n: u64) -> Vec<IntegerState> {
    let mut s = 0x9e3779b97f4a7c15;
    let mut out = Vec::new();
    for _ in 0..n {
        let log_r = 5.0 + (lcg(&mut s) as f64 / (1u64 << 53) as f64) * 8.0;
        let r = 2f64.powf(log_r);
        let vc = (1.0f64 / r).sqrt(); // circular coordinate speed, G=c=M=1, weak field
        let vr = (lcg(&mut s) as f64 / (1u64 << 53) as f64 - 0.5) * 0.6 * vc;
        let theta = (lcg(&mut s) as f64 / (1u64 << 53) as f64) * std::f64::consts::TAU;
        let (ct, st) = (theta.cos(), theta.sin());
        let (vx, vy) = (vc * ct - vr * st, vc * st + vr * ct);
        let vexp = -24i16;
        let pexp = -12i16;
        out.push(IntegerState {
            position: [
                (r * ct * (1u64 << (-pexp) as u32) as f64) as i64,
                (r * st * (1u64 << (-pexp) as u32) as f64) as i64,
            ],
            velocity: [
                (vx * (1u64 << (-vexp) as u32) as f64) as i64,
                (vy * (1u64 << (-vexp) as u32) as f64) as i64,
            ],
            length_exponent: pexp,
            velocity_exponent: vexp,
        });
    }
    out
}

fn fold(h: u64, x: u64) -> u64 {
    (h ^ x).wrapping_mul(0x100000001b3)
}

fn run_compile(ks: Vec<OrbitKey>, n: u64, rounds: u64, tag: &str) {
    let n = ks.len() as u64;
            let mut h = 0xcbf29ce484222325;
            let mut knots = 0u64;
            for &key in &ks {
                let o = Orbit::compile(key).unwrap();
                for inc in [
                    o.advance().unwrap(),
                    o.period().unwrap(),
                    o.proper_period().unwrap(),
                ] {
                    h = fold(h, inc.significand() as u64);
                    h = fold(h, inc.exponent() as u16 as u64);
                }
                knots += o.shape().knots().len() as u64;
            }
            let mut best = u128::MAX;
            let mut times = Vec::new();
            for _ in 0..rounds {
                let t = Instant::now();
                for &key in &ks {
                    std::hint::black_box(Orbit::compile(key).unwrap());
                }
                let d = t.elapsed().as_nanos();
                times.push(d);
                best = best.min(d);
            }
            times.sort();
            let med = times[times.len() / 2];
            println!(
                "compile-{} n={} med={}ns best={}ns/event med={:.1}ns best={:.1}ns knots/orbit={:.1} ck=0x{:016x}",
                tag, n, med, best, med as f64 / n as f64, best as f64 / n as f64, knots as f64 / n as f64, h
            );
}

fn main() {
    let mode = std::env::args().nth(1).unwrap_or_else(|| "compile".into());
    let rounds: u64 = std::env::args()
        .nth(2)
        .and_then(|a| a.parse().ok())
        .unwrap_or(7);
    let n = 512u64;
    match mode.as_str() {
        "compile-deep" => run_compile(keys_r(n, 0xdeadbeefcafe1234, 2.0, 2.0, 0.7, 0.25), n, rounds, "deep"),
        "compile-circ" => run_compile(keys_r(n, 0x0badc0ffee123456, 4.0, 10.0, 0.0, 0.05), n, rounds, "circ"),
        "compile" => run_compile(keys(n), n, rounds, "main"),
        "rebind" => {
            let sts = states(n);
            let mut h = 0xcbf29ce484222325;
            let mut ok = 0u64;
            for st in &sts {
                if let Ok(rb) = Rebinding::from_state(*st, Scalar::ZERO, None) {
                    ok += 1;
                    h = fold(h, rb.periapsis_angle as u64);
                    h = fold(h, rb.periapsis_time.significand() as u64);
                    h = fold(h, rb.residual.position[0] as u64);
                    h = fold(h, rb.residual.position[1] as u64);
                    h = fold(h, rb.residual.velocity[0] as u64);
                    h = fold(h, rb.residual.velocity[1] as u64);
                }
            }
            let mut best = u128::MAX;
            let mut times = Vec::new();
            for _ in 0..rounds {
                let t = Instant::now();
                for st in &sts {
                    std::hint::black_box(Rebinding::from_state(*st, Scalar::ZERO, None));
                }
                let d = t.elapsed().as_nanos();
                times.push(d);
                best = best.min(d);
            }
            times.sort();
            let med = times[times.len() / 2];
            println!(
                "rebind n={} ok={} med={}ns best={}ns/event med={:.1}ns best={:.1}ns ck=0x{:016x}",
                n,
                ok,
                med,
                best,
                med as f64 / n as f64,
                best as f64 / n as f64,
                h
            );
        }
        _ => eprintln!("modes: compile rebind"),
    }
}
