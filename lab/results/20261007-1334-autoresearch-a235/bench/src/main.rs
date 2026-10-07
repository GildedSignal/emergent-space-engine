//! Bench: ns per `Rebinding::from_state` (the plane's per-kick recompile) and per
//! `Orbit::compile`, plus a bit-identity digest over observable outputs.
//! Usage: bench [tuning|heldout] [iters]
use emergent_space::binding::{IntegerState, Rebinding};
use emergent_space::orbit::{Orbit, OrbitKey, Scalar};
use std::time::Instant;

fn scalar(n: i128, e: i32) -> Scalar {
    Scalar::raw(n, e).unwrap()
}

/// One integer state on a Newtonian-shaped bound orbit about M=1: distance `r` (M units),
/// eccentricity guide `e` (speed at apoapsis-like radius), tangential velocity.
fn state_at(r: i128, e: f64, frac: f64, len_exp: i32) -> IntegerState {
    // a from r taken as apoapsis: a = r/(1+e); speed at r: v^2 = (1-e)/(1+e) * 1/r
    let a = (r as f64) / (1.0 + e);
    let v = (((1.0 - e) / (1.0 + e) / r as f64).sqrt()) * (0.6 + 0.8 * frac);
    let x = (r as f64) * (1.0 - 0.5 * frac);
    let y = (r as f64) * 0.15 * frac;
    let scale = 1i128 << (-len_exp);
    IntegerState {
        position: [(x * scale as f64) as i64, (y * scale as f64) as i64],
        velocity: [
            (-v * (0.3 + frac) * (1i128 << 32) as f64) as i64,
            (v * (1i128 << 32) as f64) as i64,
        ],
        length_exponent: len_exp as i16,
        velocity_exponent: -32,
    }
}

fn corpus(kind: &'static str) -> Vec<(IntegerState, &'static str)> {
    let (radii, es): (&[i128], &[f64]) = if kind == "tuning" {
        (
            &[8, 16, 64, 512, 1 << 14, 1 << 18, 1 << 22, 1 << 26, 1 << 30],
            &[0.0, 0.1, 0.3, 0.7],
        )
    } else {
        (
            &[10, 24, 100, 1000, 1 << 15, 1 << 19, 1 << 23, 1 << 28],
            &[0.02, 0.2, 0.5, 0.85],
        )
    };
    let mut out = Vec::new();
    for &r in radii {
        for &e in es {
            for frac in [0.3f64, 0.7f64] {
                let len_exp = if r > (1 << 40) { -8 } else { 0 };
                out.push((state_at(r, e, frac, len_exp), kind));
            }
        }
    }
    out
}

fn fnv(data: &[u8], h: &mut u64) {
    for &b in data {
        *h ^= b as u64;
        *h = h.wrapping_mul(0x100000001b3);
    }
}
fn i128b(v: i128, out: &mut Vec<u8>) {
    out.extend_from_slice(&v.to_le_bytes());
}

/// Digest every observable the plane reads from a rebinding.
fn digest(fit: &Rebinding, out: &mut Vec<u8>) {
    i128b(fit.periapsis_time.significand() as i128, out);
    i128b(fit.periapsis_time.exponent() as i128, out);
    i128b(fit.periapsis_angle as i128, out);
    i128b(fit.clockwise as i128, out);
    i128b(fit.residual.position[0] as i128, out);
    i128b(fit.residual.position[1] as i128, out);
    i128b(fit.residual.velocity[0] as i128, out);
    i128b(fit.residual.velocity[1] as i128, out);
    if let emergent_space::binding::Trajectory::Cycle(orbit) = &fit.trajectory {
        i128b(orbit.period().unwrap().significand() as i128, out);
        i128b(orbit.period().unwrap().exponent() as i128, out);
        i128b(orbit.proper_period().unwrap().significand() as i128, out);
        i128b(orbit.proper_period().unwrap().exponent() as i128, out);
        i128b(orbit.advance().unwrap().significand() as i128, out);
        i128b(orbit.advance().unwrap().exponent() as i128, out);
        i128b(orbit.shape().crossings().len() as i128, out);
        i128b(orbit.shape().knots().len() as i128, out);
        let per = orbit.period().unwrap();
        for f in [scalar(1, 2), scalar(2, 2)] {
            let st = orbit.state(per.mul(f).unwrap()).unwrap();
            i128b(st.radius.significand() as i128, out);
            i128b(st.radius.exponent() as i128, out);
            i128b(st.radial_angle as i128, out);
            i128b(st.advance.significand() as i128, out);
            i128b(st.proper_time.significand() as i128, out);
            i128b(st.radial_velocity.significand() as i128, out);
            i128b(st.transverse_velocity.significand() as i128, out);
            i128b(st.psi as i128, out);
        }
    } else {
        i128b(-1, out);
    }
}

fn main() {
    let kind: &'static str = match std::env::args().nth(1).as_deref() {
        Some("heldout") => "heldout",
        _ => "tuning",
    };
    let iters: u32 = std::env::args()
        .nth(2)
        .and_then(|s| s.parse().ok())
        .unwrap_or(50);
    let corpus = corpus(&kind);
    let t0 = scalar(1_000_000, 0);

    // Correctness digest first (bit identity across builds).
    let mut buf = Vec::new();
    let mut ok = 0usize;
    let mut err = 0usize;
    for (st, _) in &corpus {
        match Rebinding::from_state(*st, t0, None) {
            Ok(fit) => {
                digest(&fit, &mut buf);
                ok += 1;
            }
            Err(_) => {
                err += 1;
                i128b(-2, &mut buf);
            }
        }
    }
    let mut h = 0xcbf29ce484222325u64;
    fnv(&buf, &mut h);

    // Timing: median-of-runs per corpus, then total.
    let mut per_state = Vec::new();
    let mut labels = Vec::new();
    for (i, (st, _)) in corpus.iter().enumerate() {
        let mut best = u128::MAX;
        for _ in 0..5 {
            let start = Instant::now();
            for _ in 0..iters {
                let r = Rebinding::from_state(*st, t0, None);
                std::hint::black_box(&r);
            }
            let d = start.elapsed().as_nanos() / iters as u128;
            best = best.min(d);
        }
        per_state.push(best);
        let extra = match Rebinding::from_state(*st, t0, None) {
            Ok(f) => match &f.trajectory {
                emergent_space::binding::Trajectory::Cycle(o) =>
                    format!("knots={} cross={}", o.shape().knots().len(), o.shape().crossings().len()),
                _ => "passage".into(),
            },
            Err(_) => "err".into(),
        };
        labels.push(format!("{:2} ns={:>7} {}", i, best, extra));
    }
    if std::env::var("VERBOSE").is_ok() {
        for l in &labels { eprintln!("{}", l); }
    }
    per_state.sort();
    let total: u128 = per_state.iter().sum();
    let n = per_state.len();
    println!(
        "kind={} states={} ok={} err={} digest={:016x}",
        kind, n, ok, err, h
    );
    println!(
        "from_state ns: median={} p90={} max={} mean={:.0}",
        per_state[n / 2],
        per_state[(n * 9) / 10],
        per_state[n - 1],
        total as f64 / n as f64
    );

    // Orbit::compile alone on the same fitted keys (attribution).
    let mut keys = Vec::new();
    for (st, _) in &corpus {
        if let Ok(fit) = Rebinding::from_state(*st, t0, None) {
            if let emergent_space::binding::Trajectory::Cycle(o) = &fit.trajectory {
                keys.push(o.key());
            }
        }
    }
    if !keys.is_empty() {
        let mut best = u128::MAX;
        for _ in 0..5 {
            let start = Instant::now();
            for _ in 0..iters {
                for &k in &keys {
                    let r = Orbit::compile(k);
                    std::hint::black_box(&r);
                }
            }
            let d = start.elapsed().as_nanos() / (iters as u128 * keys.len() as u128);
            best = best.min(d);
        }
        println!("orbit compile ns (mean over {} keys): {}", keys.len(), best);
    }
}

