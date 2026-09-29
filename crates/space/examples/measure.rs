//! Complete cold first-return cost (including tables, roots, clocks and exits).
//! ns/crossing divides that whole cost by crossings; it is not a shear microbench.
use emergent_space::*;
use std::{hint::black_box, time::Instant};
#[allow(dead_code)]
mod fixtures {
    include!("../tests/fixtures/reference.rs");
}
fn median(v: &mut [u128]) -> u128 {
    v.sort_unstable();
    v[v.len() / 2]
}
fn percentile(v: &[u128], p: usize) -> u128 {
    v[(v.len() - 1) * p / 100]
}
fn main() {
    let all = Instant::now();
    let keys: Vec<_> = fixtures::REFERENCE[..256]
        .iter()
        .map(|&(p, e, _, _, _, _, _, _)| {
            Key::darwin(
                (p * 65536.0).round() as u32,
                (e * 1073741824.0).round() as u32,
            )
            .unwrap()
        })
        .collect();
    let (mut ns, mut cross_ns, mut crosses, mut steps) = (vec![], vec![], vec![], vec![]);
    let mut closes = 0;
    let mut failures = 0;
    let mut max_return_defect = 0i128;
    let mut memo = Memo::default();
    for &key in &keys {
        let start = Instant::now();
        let result = compile(black_box(key));
        let elapsed = start.elapsed().as_nanos();
        match result {
            Ok(c) => {
                ns.push(elapsed);
                crosses.push(c.crossings.len() as u128);
                steps.push(c.steps as u128);
                if !c.crossings.is_empty() {
                    cross_ns.push(elapsed / c.crossings.len() as u128);
                }
                closes += usize::from(c.periodic());
                max_return_defect = max_return_defect.max((c.end.u_q48() - c.start.u_q48()).abs());
                black_box(c);
            }
            Err(e) => {
                eprintln!("compile failure {key:?}: {e:?}");
                failures += 1;
            }
        }
        if all.elapsed().as_secs() > 45 {
            panic!("measurement budget");
        }
    }
    println!("cold_first_return samples={} failures={failures} closed={closes} median_crossings={} median_steps={} median_ns_per_cycle={} p95_ns={} p99_ns={} max_ns={} charged_median_ns_per_crossing={} crossing_denominator={}",
        ns.len(),median(&mut crosses),median(&mut steps),median(&mut ns),percentile(&ns,95),percentile(&ns,99),ns.last().unwrap(),median(&mut cross_ns),cross_ns.len());
    println!("max_return_u_defect_q48={max_return_defect}");
    for &k in &keys {
        black_box(memo.get(k).unwrap());
    }
    let mut hits = vec![];
    for &k in &keys {
        let t = Instant::now();
        black_box(memo.get(k).unwrap());
        hits.push(t.elapsed().as_nanos());
    }
    println!(
        "memo_hit samples={} entries={} median_ns={}",
        hits.len(),
        memo.len(),
        median(&mut hits)
    );
    let mut tangent_ns = vec![];
    let mut rejected = 0;
    for &k in &keys[..32] {
        let t = Instant::now();
        let c = compile(k).unwrap();
        let d = Tangent::create(&c, 1 << 24, 1 << 16);
        let elapsed = t.elapsed().as_nanos();
        match d {
            Ok(d) => {
                black_box(d);
                tangent_ns.push(elapsed);
            }
            Err(_) => rejected += 1,
        }
    }
    if !tangent_ns.is_empty() {
        println!(
            "cold_with_first_differences samples={} rejected={} median_ns={}",
            tangent_ns.len(),
            rejected,
            median(&mut tangent_ns)
        );
    }
    for (r, f, turns) in [(7.0f64, 1.01f64, 100), (5.5, 0.99, 50)] {
        // Only the diagnostic input adapter has floats. trace_until has no classifier.
        let e = (1.0 - 2.0 / r) / (1.0 - 3.0 / r).sqrt();
        let l = f * r / (r - 3.0).sqrt();
        let k = Key::new(
            (e * 281474976710656.0).round() as u64,
            (l * 4294967296.0).round() as u64,
        )
        .unwrap();
        let start = Instant::now();
        let result = trace_until(
            k,
            (281474976710656.0 / r).round() as u64,
            0,
            (turns as f64 * std::f64::consts::TAU * 1073741824.0).round() as u64,
        );
        println!(
            "isco r={r} L_factor={f} requested_orbits={turns} result={result:?} elapsed_ms={}",
            start.elapsed().as_millis()
        );
    }
    println!("total_ms={}", all.elapsed().as_millis());
}
