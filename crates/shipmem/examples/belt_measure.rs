//! Measurements for the integrated belt, not the independently owned B18 gate.
//! cargo run --release -p emergent-shipmem --example belt_measure -- <n> <birth|tails|churn>
use emergent_shipmem::belt::Belt;
use emergent_shipmem::belt::Columns;
use emergent_shipmem::codec::Enc;
use emergent_shipmem::pop::{Pop, Rng};
use std::hint::black_box;
use std::time::Instant;

fn main() {
    let args: Vec<_> = std::env::args().collect();
    let n: u64 = args.get(1).expect("n").parse().unwrap();
    let mode = args.get(2).map(String::as_str).unwrap_or("birth");
    let b = Belt::new(Belt::LAB_KEYS, Columns::Independent).unwrap();
    let mut enc = Enc::new(true);
    let mut p = b.population(n, &mut enc);
    match mode {
        "birth" => {
            let mut timings = Vec::new();
            let mut out = [0; 8];
            let start = Instant::now();
            for s in (0..n).step_by(1024) {
                let end = (s + 1024).min(n);
                let t = Instant::now();
                for i in s..end {
                    p.eval(i, &mut out);
                    black_box(out);
                }
                timings.push(t.elapsed().as_nanos() as f64 / (end - s) as f64);
            }
            let ns = start.elapsed().as_nanos() as f64 / n as f64;
            timings.sort_by(f64::total_cmp);
            let q = |f: f64| timings[(f * (timings.len() - 1) as f64) as usize];
            println!("{{\"mode\":\"birth\",\"n\":{n},\"bytes\":{},\"table_bytes\":{},\"bits_per_body\":{},\"ns_per_body\":{ns},\"batch_p50_ns\":{},\"batch_p95_ns\":{},\"batch_p99_ns\":{},\"billion_bits_extrapolated\":{}}}", p.bytes(), p.table_bytes(), p.bytes() as f64 * 8.0 / n as f64, q(0.5), q(0.95), q(0.99), p.bytes() as f64 * 8.0 / 1e9);
        }
        "tails" => {
            // Independent continuous inverse-CDF iid control, not the program table.
            let ecut = 0.07 * (-2.0 * 1e-4f64.ln()).sqrt();
            let pcut = 2048.0 + 512.0 * (1.0 - 1e-4);
            for seed in [0, 17, 91, 1234, 99991] {
                let keys = if seed == 0 {
                    Belt::LAB_KEYS
                } else {
                    std::array::from_fn(|f| {
                        let mut r = Rng::new(seed + f as u64 * 98179);
                        r.next() | 1
                    })
                };
                let belt = Belt::new(keys, Columns::Independent).unwrap();
                let mut iid = Rng::new(seed ^ 0x123456789abcdef);
                let mut count = [[0u64; 2]; 2];
                let mut lo = [[f64::INFINITY; 2]; 2];
                let mut hi = [[0f64; 2]; 2];
                for i in 0..n {
                    let (p, e, _, _, _) = belt.draws(i);
                    let rp = 2048.0 + iid.below(1 << 25) as f64 / 65536.0;
                    let survival = (!iid.next() as f64 + 0.5) / 2f64.powi(64);
                    let re = 0.07 * (-2.0 * survival.ln()).sqrt();
                    for (arm, v) in [[p as f64 / 65536.0, e as f64 / 2f64.powi(30)], [rp, re]]
                        .iter()
                        .enumerate()
                    {
                        for col in 0..2 {
                            if v[col] >= [pcut, ecut][col] {
                                count[arm][col] += 1;
                                lo[arm][col] = lo[arm][col].min(v[col]);
                                hi[arm][col] = hi[arm][col].max(v[col]);
                            }
                        }
                    }
                }
                println!("{{\"mode\":\"tails\",\"n\":{n},\"seed\":{seed},\"expected_count\":{},\"count_program_p_e\":{:?},\"count_iid_p_e\":{:?},\"min_program_p_e\":{:?},\"max_program_p_e\":{:?},\"min_iid_p_e\":{:?},\"max_iid_p_e\":{:?}}}", n as f64 * 1e-4, count[0], count[1], lo[0], hi[0], lo[1], hi[1]);
            }
        }
        "churn" => {
            let birth_bytes = p.bytes();
            let mut r = Rng::new(9091);
            for epoch in 1..=12 {
                let mut changed = Vec::new();
                for i in 0..n {
                    if r.bernoulli_p(0.01) {
                        let mut s = [0; 8];
                        p.eval(i, &mut s);
                        let s = Pop::Convoy.kick(&s, &mut r);
                        p.update(i, s);
                        changed.push((i, s));
                    }
                }
                p.seal(&mut enc);
                for (i, expected) in changed {
                    let mut s = [0; 8];
                    p.eval(i, &mut s);
                    assert_eq!(s, expected);
                }
                let bytes = p.bytes();
                println!("{{\"mode\":\"churn\",\"n\":{n},\"epoch\":{epoch},\"rate\":0.01,\"scars\":{},\"bytes\":{bytes},\"bits_per_body\":{},\"incremental_bits_per_scar\":{},\"billion_bytes_extrapolated\":{}}}", p.scars(), bytes as f64 * 8.0 / n as f64, (bytes-birth_bytes) as f64 * 8.0 / p.scars() as f64, (bytes-birth_bytes) as f64 / n as f64 * 1e9 + birth_bytes as f64);
            }
        }
        _ => panic!("unknown measurement"),
    }
}
