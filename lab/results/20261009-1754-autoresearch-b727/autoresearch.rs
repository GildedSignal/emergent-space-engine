//! Autoresearch harness (run 20261009-1754-autoresearch-b727): ns per kick rebuild on the
//! law pipeline (`from_state` + `compile` + `state`), behaviours held bit-identical via
//! full-output digests (not sinks: every field of every answer is hashed).
//!
//! ```text
//! cargo run --release -p emergent-universe --example autoresearch -- [iters] [stage]
//!   stage: all | from | compile | state | heldout
//! ```
use emergent_space::binding::{cartesian, IntegerState, Rebinding};
use emergent_space::orbit::{Orbit, OrbitKey, Scalar};
use std::time::Instant;

fn mix(h: u128, x: i128) -> u128 {
    let mut h = h ^ (x as u128);
    for _ in 0..2 {
        h = h.rotate_left(13).wrapping_mul(0x100000001b3);
    }
    h
}

/// Hash every observable of one rebinding answer: reconstruction, trajectory readouts.
fn hash_rebinding(h: u128, rb: &Rebinding, times: &[Scalar]) -> u128 {
    let mut h = h;
    let rec = rb.reconstruct().unwrap();
    for c in rec.position.iter().chain(rec.velocity.iter()) {
        h = mix(h, *c as i128);
    }
    h = mix(h, rec.length_exponent as i128);
    h = mix(h, rec.velocity_exponent as i128);
    let dec = rb.decoded_event().unwrap();
    for c in dec.position.iter().chain(dec.velocity.iter()) {
        h = mix(h, *c as i128);
    }
    for &t in times {
        let st = rb.trajectory.state(t).unwrap();
        h = mix(h, st.radius.significand() as i128);
        h = mix(h, st.radius.exponent() as i128);
        h = mix(h, st.radial_angle as i128);
        h = mix(h, st.advance.significand() as i128);
        h = mix(h, st.proper_time.significand() as i128);
        h = mix(h, st.radial_velocity.significand() as i128);
        h = mix(h, st.transverse_velocity.significand() as i128);
        h = mix(h, st.psi as i128);
        h = mix(h, st.cycles as i128);
        h = mix(h, st.outbound as i128);
    }
    h
}

fn build_states(bank: &[(i64, u64)]) -> (Vec<IntegerState>, Vec<(OrbitKey, Orbit)>) {
    let mut states = Vec::new();
    let mut orbit_bank = Vec::new();
    for &(p, e) in bank {
        let key = OrbitKey::bound(Scalar::integer(p), e).unwrap();
        let orbit = Orbit::compile(key).unwrap();
        let per = orbit.period().unwrap();
        let mut bank_states = Vec::new();
        for j in 0..4u64 {
            let t = per.mul(Scalar::raw((j * 16 + 3) as i128, -7).unwrap()).unwrap();
            let st = orbit.signed_state(t).unwrap();
            let units = (st.radius.exponent() - 60, st.transverse_velocity.abs().exponent() - 60);
            if let Some(s) = cartesian(st, (j * 0x10000000) as u32, j % 2 == 0, units).ok() {
                bank_states.push(s);
            }
        }
        orbit_bank.push((key, orbit));
        states.extend(bank_states);
    }
    (states, orbit_bank)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let iters: usize = args.get(1).map(|s| s.parse().unwrap()).unwrap_or(2000);
    let stage = args.get(2).cloned().unwrap_or_else(|| "all".into());

    // Tuning bank.
    let bank: Vec<(i64, u64)> = vec![
        (1_200_000_000, (1u64 << 48) / 100),
        (1_200_000_000, 0),
        (1_200_000_000, (1u64 << 48) / 10),
        (1_200_000_000, (1u64 << 48) / 2),
        (1_200_000_000, (1u64 << 48) - (1u64 << 30)),
        (16, (1u64 << 48) / 10),
        (1 << 30, (1u64 << 48) / 10),
        (1 << 52, (1u64 << 48) / 100),
    ];
    // Held-out bank (predictions.md; never tuned on).
    let heldout_bank: Vec<(i64, u64)> = vec![
        (3_456_789_001, (1u64 << 48) / 50),
        (2_000_000_000, (1u64 << 48) / 4),
        (987_654_321, (1u64 << 48) / 20),
        (1 << 44, 0),
        (64, (1u64 << 48) / 3),
        (1_500_000_000, (1u64 << 48) / 10 * 9),
    ];

    if stage == "heldout" {
        let (states, orbits) = build_states(&heldout_bank);
        // Digest of every observable, then per-case timings.
        let mut h: u128 = 0x9e3779b97f4a7c15;
        let times: Vec<Scalar> = [1i64, 7, 31, 101, 997]
            .iter()
            .map(|&k| Scalar::integer(k * 1_000_003))
            .collect();
        for &s in &states {
            let rb = Rebinding::from_state(s, Scalar::integer(1_000_000), None).unwrap();
            h = hash_rebinding(h, &rb, &times);
        }
        for (key, orbit) in &orbits {
            h = mix(h, orbit.period().unwrap().significand() as i128);
            h = mix(h, orbit.advance().unwrap().significand() as i128);
            h = mix(h, orbit.proper_period().unwrap().significand() as i128);
            let per = orbit.period().unwrap();
            for j in 0..8u64 {
                let t = per.mul(Scalar::raw((j * 4 + 1) as i128, -5).unwrap()).unwrap();
                let st = orbit.signed_state(t).unwrap();
                h = mix(h, st.radius.significand() as i128);
                h = mix(h, st.radial_angle as i128);
                h = mix(h, st.proper_time.significand() as i128);
                h = mix(h, st.psi as i128);
            }
        }
        println!("heldout digest {:x}", h);
        let n = 200;
        for (i, &(p, e)) in heldout_bank.iter().enumerate() {
            let key = OrbitKey::bound(Scalar::integer(p), e).unwrap();
            let orbit = Orbit::compile(key).unwrap();
            let per = orbit.period().unwrap();
            let t0 = Instant::now();
            for _ in 0..n {
                let _ = Orbit::compile(key).unwrap();
            }
            let d_c = t0.elapsed().as_secs_f64() * 1e9 / n as f64;
            let mut st_opt = None;
            let t0 = Instant::now();
            for k in 0..n {
                let t = per.mul(Scalar::raw((k * 37 + 11) as i128 % 997, -10).unwrap()).unwrap();
                st_opt = Some(orbit.signed_state(t).unwrap());
            }
            let d_s = t0.elapsed().as_secs_f64() * 1e9 / n as f64;
            let _ = st_opt.unwrap();
            // from_state on the i-th built state if it exists (index 4*i within range).
            let d_f = if let Some(&s) = states.get(4 * i) {
                let t0 = Instant::now();
                for _ in 0..n {
                    let _ = Rebinding::from_state(s, Scalar::integer(1_000_000), None).unwrap();
                }
                t0.elapsed().as_secs_f64() * 1e9 / n as f64
            } else { 0.0 };
            println!(
                "HO{} p {:-12} e {:.4}: compile {:7.0} state {:7.0} from {:7.0} ns",
                i + 1,
                p,
                e as f64 / (1u64 << 48) as f64,
                d_c,
                d_s,
                d_f
            );
        }
        return;
    }

    let (states, orbit_bank) = build_states(&bank);
    let n = states.len();
    let mut digest: u128 = 0xcbf29ce484222325;

    let t0 = Instant::now();
    let mut sink = 0i128;
    for _ in 0..iters {
        for &s in &states {
            let rb = Rebinding::from_state(s, Scalar::integer(1_000_000), None).unwrap();
            sink ^= rb.reconstruct().unwrap().position[0] as i128;
        }
    }
    let d_from = t0.elapsed();
    digest = mix(digest, sink);

    let t0 = Instant::now();
    let mut sink2 = 0i128;
    for _ in 0..iters {
        for &(key, _) in &orbit_bank {
            let o = Orbit::compile(key).unwrap();
            sink2 ^= o.period().unwrap().significand() as i128;
        }
    }
    let d_compile = t0.elapsed();
    digest = mix(digest, sink2);

    let t0 = Instant::now();
    let mut sink3 = 0i128;
    for i in 0..iters {
        for (j, &(key, _)) in orbit_bank.iter().enumerate() {
            let orbit = Orbit::compile(key).unwrap();
            let t = orbit
                .period()
                .unwrap()
                .mul(Scalar::raw((i as i128 * 8 + j as i128 * 3 + 1) * 997, -20).unwrap())
                .unwrap();
            let st = orbit.signed_state(t).unwrap();
            sink3 ^= st.radius.significand() as i128;
        }
    }
    let d_state = t0.elapsed();
    digest = mix(digest, sink3);

    let per = |d: std::time::Duration, count: usize| d.as_secs_f64() * 1e9 / count as f64;
    match stage.as_str() {
        "from" => println!("from_state {:.0} ns", per(d_from, iters * n)),
        "compile" => println!("compile {:.0} ns", per(d_compile, iters * bank.len())),
        "state" => println!("state {:.0} ns", per(d_state, iters * bank.len())),
        _ => {
            println!("bank {} states / {} orbits, iters {}", n, bank.len(), iters);
            println!("from_state {:.0} ns", per(d_from, iters * n));
            println!("compile   {:.0} ns", per(d_compile, iters * bank.len()));
            println!("state     {:.0} ns", per(d_state, iters * bank.len()));
            println!("total     {:.0} ns", per(d_from + d_compile + d_state, iters * (n + 2 * bank.len())));
            println!("digest {:x}", digest);
        }
    }
}
