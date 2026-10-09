//! ns/event bench + bit-identity fingerprint for `Orbit::compile`.
//! Usage: compile-bench [tune|heldout] [--secs N]
use emergent_space::orbit::{Orbit, OrbitKey, Scalar};
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use std::time::Instant;

/// (periapsis exponent (p = 2^exp), e in Q48 units of 2^-48)
fn keys(mode: &str) -> Vec<(i16, u64)> {
    let e = |x: f64| (x * 2f64.powi(48)) as u64;
    let mut out = Vec::new();
    let (exps, ecs): (&[i16], &[f64]) = if mode == "heldout" {
        (
            &[3, 5, 9, 13, 17, 21],
            &[0.0, 0.003, 0.05, 0.2, 0.35, 0.65, 0.8, 0.95, 0.99],
        )
    } else {
        (
            &[2, 4, 7, 11, 15, 19, 24],
            &[0.0, 0.001, 0.02, 0.1, 0.5, 0.9, 0.97],
        )
    };
    for &p in exps {
        for &x in ecs {
            out.push((p, e(x)));
        }
    }
    out
}

fn fingerprint(key: OrbitKey, orbit: &Orbit) -> u64 {
    let mut h = DefaultHasher::new();
    key.hash(&mut h);
    for acc in [orbit.period().ok(), orbit.proper_period().ok(), orbit.advance().ok()] {
        match acc {
            Some(s) => s.hash(&mut h),
            None => 0u8.hash(&mut h),
        }
    }
    let shape = orbit.shape();
    shape.crossings().hash(&mut h);
    for k in shape.knots() {
        k.psi.hash(&mut h);
    }
    // Readouts exercise every internal sum: quarter-phase states over one cycle.
    let period = orbit.period().unwrap();
    for i in 0..16u64 {
        let t = period.mul(Scalar::raw((i as i128) << 40, -40).unwrap()).unwrap();
        match orbit.signed_state(t) {
            Ok(st) => {
                st.radius.hash(&mut h);
                st.advance.hash(&mut h);
                st.proper_time.hash(&mut h);
                st.radial_velocity.hash(&mut h);
                st.transverse_velocity.hash(&mut h);
                st.psi.hash(&mut h);
                st.cycles.hash(&mut h);
                st.outbound.hash(&mut h);
            }
            Err(_) => 1u8.hash(&mut h),
        }
    }
    h.finish()
}

#[cfg(feature = "profile")]
fn dump_prof(tag: &str) {
    let p = emergent_space::orbit::prof::take();
    eprintln!(
        "prof {}: cuts={} ns_cut={} panels={} weak={} fast={} gen={} ns_quad={}",
        tag, p[0], p[5], p[1], p[2], p[3], p[4], p[6]
    );
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mode = args.get(1).map(String::as_str).unwrap_or("tune");
    let secs: f64 = args
        .get(2)
        .and_then(|s| s.parse().ok())
        .unwrap_or(3.0);
    let pop = keys(mode);
    let mut results = Vec::new();
    let mut hash = DefaultHasher::new();
    let mut refused = 0usize;
    for &(p, e) in &pop {
        let key = OrbitKey::bound(Scalar::power_of_two(p), e).unwrap();
        let orbit = match Orbit::compile(key) {
            Ok(o) => o,
            Err(_) => {
                refused += 1;
                continue;
            }
        };
        #[cfg(feature = "profile")]
        if p == 4 && e > 200000000000000 {
            let _ = emergent_space::orbit::prof::take();
            let key2 = OrbitKey::bound(Scalar::power_of_two(p), e).unwrap();
            let _ = std::hint::black_box(Orbit::compile(key2));
            dump_prof(&format!("isolated p={} e={}", p, e));
        }
        fingerprint(key, &orbit).hash(&mut hash);
        // Calibrate iterations, then time.
        let mut n = 1usize;
        loop {
            let t = Instant::now();
            for _ in 0..n {
                std::hint::black_box(Orbit::compile(std::hint::black_box(key)));
            }
            if t.elapsed().as_secs_f64() >= secs || n >= 1 << 22 {
                results.push((p, e, t.elapsed().as_nanos() as f64 / n as f64));
                break;
            }
            n *= 4;
        }
    }
    let mut ns: Vec<f64> = results.iter().map(|r| r.2).collect();
    ns.sort_by(f64::total_cmp);
    let at = |p: f64| ns.get(((ns.len().saturating_sub(1)) as f64 * p).ceil() as usize).copied();
    println!(
        "mode={} n={} refused={} median_ns={:.0} p90_ns={:.0} max_ns={:.0} total_ns={:.0} fp={:016x}",
        mode,
        ns.len(),
        refused,
        at(0.5).unwrap_or(0.0),
        at(0.9).unwrap_or(0.0),
        at(1.0).unwrap_or(0.0),
        ns.iter().sum::<f64>(),
        hash.finish()
    );
    for (p, e, v) in &results {
        println!("  p_exp={} e_q48={} ns={:.0}", p, e, v);
    }
}
