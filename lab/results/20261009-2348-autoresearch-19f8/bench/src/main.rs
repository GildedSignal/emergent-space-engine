//! Latency of `Rebinding::from_state` — the plane's per-kick compile — on a fixed
//! deterministic corpus of kicked states. Behaviours are held fixed by a digest of
//! every output; only speed may change.
//!
//! Usage: rebind-bench <tune|heldout> [passes]
use emergent_space::binding::{cartesian, IntegerState, Rebinding};
use emergent_space::orbit::{Orbit, OrbitKey};
use emergent_space::scaled::Scalar;
use std::time::Instant;

struct Corpus {
    states: Vec<IntegerState>,
    times: Vec<Scalar>,
}

fn lcg(state: &mut u64) -> u64 {
    *state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
    *state
}

/// A kicked population: bound orbits sampled around their cycle, then velocity
/// perturbations of a given quantum (the test's recipe, extended).
fn corpus(radius_exps: &[i32], es: &[u64], kicks: i64, perturb: i64, seed: u64) -> Corpus {
    let mut states = Vec::new();
    let mut times = Vec::new();
    let mut seed = seed;
    for &re in radius_exps {
        for &e in es {
            let Ok(key) = OrbitKey::bound(Scalar::integer(16).scale(re).unwrap(), e) else { continue };
            let Ok(orbit) = Orbit::compile(key) else { continue };
            for j in 0..16u64 {
                let time = orbit.period().unwrap().mul(Scalar::raw((j * 2 + 1) as i128, -5).unwrap()).unwrap();
                let st = orbit.state(time).unwrap();
                let units = (st.radius.exponent() - 60, st.transverse_velocity.abs().exponent() - 60);
                let Ok(mut state) = cartesian(st, j as u32 * 0x10000000, j % 2 == 0, units) else { continue };
                let t = time;
                for _ in 0..kicks {
                    lcg(&mut seed);
                    for c in &mut state.velocity {
                        *c = c.saturating_add(((seed >> 32) as i32 as i64) * perturb);
                    }
                    states.push(state);
                    times.push(t);
                }
            }
        }
    }
    Corpus { states, times }
}

fn digest(fit: &Result<Rebinding, emergent_space::Error>) -> u64 {
    // FNV-1a over a stable rendering of the exact output.
    let mut h: u64 = 0xcbf29ce484222325;
    let mut eat = |s: String| {
        for b in s.bytes() {
            h ^= b as u64;
            h = h.wrapping_mul(0x100000001b3);
        }
    };
    match fit {
        Ok(f) => {
            eat(format!("{:?}", std::mem::discriminant(&f.trajectory)));
            eat(format!("{:?}", f.periapsis_time));
            eat(format!("{}", f.periapsis_angle));
            eat(format!("{}", f.clockwise));
            eat(format!("{:?}", f.residual));
            eat(format!("{:?}", f.event_time));
        }
        Err(e) => eat(format!("E{:?}", e)),
    }
    h
}

fn run(name: &str, c: &Corpus, passes: usize, with_profile: bool) {
    // Warmup + correctness digest.
    let mut reference: u64 = 0;
    let mut oks = 0usize;
    for (s, t) in c.states.iter().zip(&c.times) {
        let r = Rebinding::from_state(*s, *t, None);
        if r.is_ok() { oks += 1; }
        reference ^= digest(&r).wrapping_mul(0x9E3779B97F4A7C15).rotate_add(reference / 3);
    }
    let mut per_call: Vec<u64> = Vec::with_capacity(c.states.len() * passes);
    let start = Instant::now();
    for _ in 0..passes {
        for (s, t) in c.states.iter().zip(&c.times) {
            let t0 = Instant::now();
            let r = Rebinding::from_state(*s, *t, None);
            let dt = t0.elapsed().as_nanos() as u64;
            std::hint::black_box(&r);
            per_call.push(dt);
        }
    }
    let wall = start.elapsed().as_nanos() as f64;
    #[cfg(feature = "profile")]
    let profile = {
        let p = emergent_space::profile::take();
        let c = emergent_space::profile::take_counts();
        let n = per_call.len() as f64;
        format!(
            " phases[fit,compile,orient,residual]={:.0},{:.0},{:.0},{:.0}ns counts[poly,iter,skip,wit,newton,brack|mul,div,add,sqrt,isqrt,divw]/call={:.1},{:.1},{:.1},{:.1},{:.1},{:.1}|{:.0},{:.0},{:.0},{:.1},{:.1},{:.1}",
            p[4] as f64 / n, p[5] as f64 / n, p[6] as f64 / n, p[7] as f64 / n,
            c[0] as f64 / n, c[1] as f64 / n, c[2] as f64 / n, c[3] as f64 / n, c[4] as f64 / n, c[5] as f64 / n, c[8] as f64 / n, c[9] as f64 / n, c[10] as f64 / n, c[11] as f64 / n, c[12] as f64 / n, c[13] as f64 / n
        )
    };
    #[cfg(not(feature = "profile"))]
    let profile = String::new();
    per_call.sort_unstable();
    let q = |f: f64| per_call[((per_call.len() as f64 - 1.0) * f) as usize];
    println!(
        "{name}: n={} ok={} mean={:.0}ns p50={:.0}ns p99={:.0}ns max={:.0}ns wall/call={:.0}ns digest={:016x}{}",
        c.states.len(), oks,
        per_call.iter().sum::<u64>() as f64 / per_call.len() as f64,
        q(0.50), q(0.99), *per_call.last().unwrap(), wall / (c.states.len() * passes) as f64,
        reference, profile
    );
}

trait RotAdd { fn rotate_add(self, o: u64) -> u64; }
impl RotAdd for u64 { fn rotate_add(self, o: u64) -> u64 { self.rotate_left(17).wrapping_add(o) } }

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let which = args.get(1).map(String::as_str).unwrap_or("tune");
    let passes: usize = args.get(2).map(|s| s.parse().unwrap()).unwrap_or(3);
    let with_profile = cfg!(feature = "profile");
    // Tune set: the plane's bulk (bound orbits, kick-sized perturbations).
    let tune = corpus(
        &[-1, 8, 17, 18, 19, 30],
        &[0, 1, 1 << 20, (1 << 48) / 100, (1 << 48) / 10, (1 << 48) / 2],
        8, 256, 0x5DEECE66D,
    );
    // Held-out: unseen radius scales (deep weak field, relativistic), extreme e,
    // heavier kicks and a different seed. Never touched while tuning.
    let held = corpus(
        &[4, 12, 45, 60, 120],
        &[1 << 32, (1 << 48) / 5, (1 << 48) - (1 << 28), (1 << 48) / 1000],
        6, 1024, 0xCAFEF00DBEEF,
    );
    match which {
        "tune" => run("tune", &tune, passes, with_profile),
        "heldout" => run("heldout", &held, passes, with_profile),
        "all" => { run("tune", &tune, passes, with_profile); run("heldout", &held, passes, with_profile); }
        _ => eprintln!("unknown set {which}"),
    }
}
