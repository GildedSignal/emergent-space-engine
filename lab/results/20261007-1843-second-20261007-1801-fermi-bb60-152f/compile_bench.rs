// Compile-cost micro-bench: the recompile half of the plane's kick, isolated.
use emergent_space::scaled::Scalar;
use emergent_space::orbit::OrbitKey;
use std::time::Instant;

fn main() {
    let exps: [i16; 8] = [4, 6, 8, 10, 12, 16, 20, 24]; // p = 2^exp M units (16 M .. 1.7e7 M)
    let es: [f64; 6] = [0.0, 0.2, 0.5, 0.8, 0.95, 0.99];
    let unit: u64 = 1 << 48;
    let mut rows: Vec<(u32, u32, f64)> = Vec::new(); // (exp, e_index, ns median)
    let mut all: Vec<f64> = Vec::new();
    let mut skipped = 0;
    for &ex in exps.iter() {
        for (ei, &e) in es.iter().enumerate() {
            let eq = (e * unit as f64) as u64;
            let key = match OrbitKey::bound(Scalar::power_of_two(ex), eq) {
                Ok(k) => k,
                Err(_) => { skipped += 1; continue; }
            };
            // warm
            for _ in 0..3 {
                if emergent_space::orbit::Orbit::compile(key).is_err() { skipped += 1; continue; }
            }
            let mut samples: Vec<f64> = Vec::new();
            for _ in 0..200 {
                let t0 = Instant::now();
                let r = emergent_space::orbit::Orbit::compile(key);
                samples.push(t0.elapsed().as_secs_f64() * 1e9);
                assert!(r.is_ok(), "compile failed after warmup");
            }
            samples.sort_by(f64::total_cmp);
            let med = samples[samples.len() / 2];
            rows.push((ex as u32, ei as u32, med));
            all.push(med);
        }
    }
    all.sort_by(f64::total_cmp);
    let at = |p: f64| all[(((all.len() as f64 - 1.0) * p).ceil()) as usize];
    println!("compile_ns: median {:.0} p90 {:.0} p99 {:.0} max {:.0} cells {} skipped {}",
             at(0.5), at(0.9), at(0.99), all[all.len() - 1], all.len(), skipped);
    println!("ns by e (rows: p=2^exp, cols e=0,0.2,0.5,0.8,0.95,0.99):");
    for &ex in exps.iter() {
        let mut line = format!("  2^{:<2}", ex);
        for (ei, _) in es.iter().enumerate() {
            if let Some(&(_, _, ns)) = rows.iter().find(|r| r.0 == ex as u32 && r.1 == ei as u32) {
                line += &format!("{:>9.0}", ns);
            } else { line += "        -"; }
        }
        println!("{line}");
    }
    // The quantized memo key: compile cost on the law's 12+12-bit cells (the reuse tier).
    let mut qs: Vec<f64> = Vec::new();
    for &ex in exps.iter() {
        for &e in es.iter() {
            let eq = (e * unit as f64) as u64;
            let key = match OrbitKey::bound(Scalar::power_of_two(ex), eq) { Ok(k) => k, Err(_) => continue };
            let mk = match key.memo_key() { Ok(m) => m, Err(_) => continue };
            for _ in 0..3 { let _ = emergent_space::orbit::Orbit::compile(mk); }
            let mut samples: Vec<f64> = Vec::new();
            for _ in 0..200 {
                let t0 = Instant::now();
                let _ = emergent_space::orbit::Orbit::compile(mk);
                samples.push(t0.elapsed().as_secs_f64() * 1e9);
            }
            samples.sort_by(f64::total_cmp);
            qs.push(samples[samples.len() / 2]);
        }
    }
    qs.sort_by(f64::total_cmp);
    println!("quantized-key compile_ns: median {:.0} p99 {:.0} cells {}", qs[qs.len() / 2], qs[qs.len() - 1], qs.len());
}
