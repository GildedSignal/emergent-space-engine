//! ns-per-compile bench for `crates/space`'s geodesic compiler, plus a bit-identical
//! behavioural digest of every corpus answer. One scalar headline: geomean ns/compile.
//!
//! Usage: bench [--heldout] [--reps N]
use emergent_space::orbit::{Orbit, OrbitKey, OrbitState};
use emergent_space::orbit::Scalar;
use std::hint::black_box;
use std::time::Instant;

/// Deterministic LCG (PCG-ish output mixing), independent of the corpus grids.
struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        self.0 = self
            .0
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        let x = self.0;
        (x ^ (x >> 33)) ^ (x >> 59)
    }
    fn unit(&mut self) -> f64 {
        (self.next() >> 11) as f64 / (1u64 << 53) as f64
    }
}

fn e_to_k48(e: f64) -> u64 {
    (e * (1u64 << 48) as f64) as u64
}

/// The tuning corpus: fixed grid covering the plane's population classes.
fn corpus_tuning() -> Vec<(&'static str, OrbitKey)> {
    let mut v = Vec::new();
    // weak eccentric (weak_quad): far periapsis, e sweep. AU-scale ships and comets.
    for (i, a) in [14i16, 18, 22, 26, 30, 34].iter().enumerate() {
        for (j, e) in [0.2f64, 0.5, 0.8, 0.95].iter().enumerate() {
            let p = Scalar::power_of_two(*a);
            if let Ok(k) = OrbitKey::bound(p, e_to_k48(*e)) {
                v.push((if j == 0 { "weak-ecc" } else { "" }, k));
                let _ = i;
            }
        }
    }
    // weak circular (symbolic fast path and near-circular Taylor shapes)
    for a in [12i16, 16, 20, 24, 28, 32, 36, 40] {
        let p = Scalar::power_of_two(a);
        if let Ok(k) = OrbitKey::new(p, 1 << 48) {
            v.push(("weak-circ", k));
        }
    }
    // strong fast path (fast_quad): compactness above 2^-18, far from separatrix
    for (p, e) in [(6.0, 0.0), (8.0, 0.3), (12.0, 0.6), (20.0, 0.0), (50.0, 0.3), (200.0, 0.6), (1000.0, 0.2), (1e4, 0.5)] {
        if let Ok(k) = OrbitKey::bound(Scalar::raw((p * 2f64.powi(30)) as i128, 30).unwrap(), e_to_k48(e)) {
            v.push(("strong-fast", k));
        }
    }
    // strong general path: near the separatrix (delta small)
    for (p, e) in [(8.0, 0.9), (10.0, 0.95), (20.0, 0.98), (12.0, 0.93)] {
        if let Ok(k) = OrbitKey::bound(Scalar::raw((p * 2f64.powi(30)) as i128, 30).unwrap(), e_to_k48(e)) {
            v.push(("strong-gen", k));
        }
    }
    v
}

/// The held-out corpus: randomized, no grid structure, different generator than tuning.
fn corpus_heldout(seed: u64) -> Vec<OrbitKey> {
    let mut r = Rng(seed);
    let mut v = Vec::new();
    for _ in 0..160 {
        // log-uniform periapsis in [4, 2^40]
        let a = 2.0 + 38.0 * r.unit();
        let mant = (1.0 + r.unit()) as i128;
        let p = Scalar::power_of_two((a as i16) - 1)
            .mul(Scalar::raw(mant, 0).unwrap())
            .unwrap();
        // e: mixture of uniform [0,0.995] and a near-separatrix band
        let e = if r.unit() < 0.3 {
            0.995 + 0.0049 * r.unit()
        } else {
            0.995 * r.unit()
        };
        if let Ok(k) = OrbitKey::bound(p, e_to_k48(e)) {
            v.push(k);
        }
    }
    v
}

fn digest_state(h: &mut blake3::Hasher, s: &OrbitState) {
    for x in [
        s.radius.significand(),
        s.radius.exponent() as i64,
        s.radial_angle as i64,
        s.advance.significand(),
        s.advance.exponent() as i64,
        s.proper_time.significand(),
        s.proper_time.exponent() as i64,
        s.radial_velocity.significand(),
        s.radial_velocity.exponent() as i64,
        s.transverse_velocity.significand(),
        s.transverse_velocity.exponent() as i64,
        s.psi as i64,
        s.cycles as i64,
    ] {
        h.update(&x.to_le_bytes());
    }
}

/// Bit-identical behavioural digest of everything the compiler produces for one key.
/// Read failures hash an error tag, so the digest always carries per-key information.
fn digest(key: OrbitKey) -> Option<[u8; 32]> {
    let o = match Orbit::compile(key) {
        Ok(o) => o,
        Err(e) => {
            let mut h = blake3::Hasher::new();
            h.update(&[0xFF]);
            h.update(format!("{e:?}").as_bytes());
            return Some(*h.finalize().as_bytes());
        }
    };
    let mut h = blake3::Hasher::new();
    h.update(&[0x01]);
    h.update(&key.k.to_le_bytes());
    h.update(&key.periapsis.significand().to_le_bytes());
    h.update(&key.periapsis.exponent().to_le_bytes());
    let sh = o.shape();
    for k in sh.knots() {
        h.update(&k.psi.to_le_bytes());
    }
    for c in sh.crossings() {
        h.update(&(*c as u64).to_le_bytes());
    }
    macro_rules! feed { ($e:expr) => { match $e { Ok(v) => v, Err(e) => { h.update(format!("E{e:?}").as_bytes()); return Some(*h.finalize().as_bytes()); } } } }
    for s in [feed!(o.period()), feed!(o.advance()), feed!(o.proper_period())] {
        h.update(&s.significand().to_le_bytes());
        h.update(&(s.exponent() as i64).to_le_bytes());
    }
    let per = feed!(o.period());
    for i in 0..sh.crossings().len().max(1) {
        if let Ok(t) = o.crossing_time(i.min(sh.crossings().len().saturating_sub(1))) {
            h.update(&t.significand().to_le_bytes());
            h.update(&(t.exponent() as i64).to_le_bytes());
        }
    }
    for f in 1..10u64 {
        if let Some(t) = per
            .mul(Scalar::raw(f as i128, 1).unwrap())
            .ok()
            .and_then(|t| t.div(Scalar::raw(10, 0).unwrap()).ok())
        {
            match o.at_phase(0, t) {
                Ok(s) => { digest_state(&mut h, &s); }
                Err(e) => { h.update(format!("P{e:?}").as_bytes()); }
            }
        }
    }
    match o.crossing_state(0, 3, false) {
        Ok(s) => { digest_state(&mut h, &s); }
        Err(e) => { h.update(format!("C{e:?}").as_bytes()); }
    }
    match o.signed_state(per.mul(Scalar::raw(3, 0).unwrap()).unwrap()) {
        Ok(s) => { digest_state(&mut h, &s); }
        Err(e) => { h.update(format!("S{e:?}").as_bytes()); }
    }
    Some(*h.finalize().as_bytes())
}

fn bench(keys: &[(&'static str, OrbitKey)], reps: usize) -> (f64, Vec<(String, f64, usize)>) {
    // warm
    let mut sink = 0u64;
    for (_, k) in keys.iter() {
        if let Ok(o) = Orbit::compile(*k) {
            sink += o.shape().knots().len() as u64;
        }
    }
    black_box(sink);
    let mut per_key = Vec::new();
    let mut all = Vec::new();
    for (tag, k) in keys.iter() {
        let mut times = Vec::with_capacity(reps);
        for _ in 0..reps {
            let t0 = Instant::now();
            let o = Orbit::compile(*k).unwrap();
            times.push(t0.elapsed().as_nanos() as f64);
            black_box(o.shape().knots().len());
        }
        times.sort_by(|a, b| a.partial_cmp(b).unwrap());
        let med = times[times.len() / 2];
        all.push(med);
        let knots = Orbit::compile(*k).map(|o| o.shape().knots().len()).unwrap_or(0);
        per_key.push((tag.to_string(), med, knots));
    }
    let geo = all.iter().product::<f64>().powf(1.0 / all.len() as f64);
    (geo, per_key)
}

mod ops;

fn main() {
    ops::run();
    let args: Vec<String> = std::env::args().collect();
    let heldout = args.iter().any(|a| a == "--heldout");
    let reps: usize = args
        .iter()
        .position(|a| a == "--reps")
        .and_then(|i| args.get(i + 1))
        .and_then(|s| s.parse().ok())
        .unwrap_or(31);

    if heldout {
        let keys = corpus_heldout(0x5eed_1234_5678_9abc);
        let mut h = blake3::Hasher::new();
        let mut n = 0usize;
        let mut nk = 0usize;
        for k in keys.iter() {
            nk += Orbit::compile(*k).map(|o| o.shape().knots().len()).unwrap_or(0);
            if let Some(d) = digest(*k) {
                h.update(&d);
                n += 1;
            }
        }
        eprintln!("heldout: {n}/{} digested, knots {nk}, digest {}", keys.len(), h.finalize().to_hex());
        for k in keys.iter().take(3) {
            let o = Orbit::compile(*k).unwrap();
            let per = o.period().unwrap();
            eprintln!("  dbg k={:x} peri_exp={} knots={} period_exp={} at_phase(1/10)={:?} cross_state={:?} signed={:?}", k.k, k.periapsis.exponent(), o.shape().knots().len(), per.exponent(), o.at_phase(0, per.mul(Scalar::raw(1,1).unwrap()).unwrap().div(Scalar::raw(10,0).unwrap()).unwrap()).map(|s| s.psi), o.crossing_state(0, 3, false).map(|s| s.psi), o.signed_state(per.mul(Scalar::raw(3,0).unwrap()).unwrap()).map(|s| s.psi));
        }
        let mut ts = Vec::new();
        for _ in 0..5 {
            let t0 = std::time::Instant::now();
            for k in keys.iter() { black_box(Orbit::compile(*k)); }
            ts.push(t0.elapsed().as_nanos() as f64 / keys.len() as f64);
        }
        ts.sort_by(|a, b| a.partial_cmp(b).unwrap());
        println!("heldout_ns_per_compile_min {:.1}", ts[0]);
        return;
    }

    
let keys = corpus_tuning(); eprintln!("corpus: {} keys", keys.len());
    let mut dh = blake3::Hasher::new();
    for (_, k) in keys.iter() {
        dh.update(&digest(*k).unwrap_or([0; 32]));
    }
    println!("digest {}", dh.finalize().to_hex());
    let (geo, per_key) = bench(&keys, reps);
    let mut by_tag: std::collections::BTreeMap<String, (f64, usize, usize)> = Default::default();
    for (tag, med, knots) in per_key.iter() {
        let t = tag.split('/').next().unwrap_or("").to_string();
        let e = by_tag.entry(if t.is_empty() { "weak-ecc".into() } else { t }).or_default();
        e.0 += med;
        e.1 += 1;
        e.2 += knots;
    }
    #[cfg(feature = "profile")]
    {
        let t = emergent_space::profile::take8();
        let names = ["quad-total", "weak.cos", "weak.div_word", "fast.cos", "fast.div+isqrt", "(unused)", "general.node", "(unused)"];
        for (i, n) in names.iter().enumerate() {
            eprintln!("  stage8 {:2} {:14} {:12.3} ms", i, n, t[i] as f64 / 1e6);
        }
        let c = emergent_space::profile::counts();
        let names2 = ["quad calls", "weak.cos", "weak.div_word", "fast.cos", "fast.node-block", "fast.nodes", "general.nodes", "shape.bound"];
        for (i, n) in names2.iter().enumerate() {
            eprintln!("  count {:2} {:18} {}", i, n, c[i]);
        }
        let _ = &t;
    }

    println!("geomean_ns_per_compile {:.1}", geo);
    for (t2, m2, k2) in per_key.iter() { eprintln!("    per-key {:10} {:9.1} ns {:5} knots", t2, m2, k2); }
    for (tag, (sum, n, knots)) in by_tag {
        println!("  {:10} mean_ms {:9.3}  mean_knots {:7.1}", tag, sum / n as f64 / 1e6, knots as f64 / n as f64);
    }
}
