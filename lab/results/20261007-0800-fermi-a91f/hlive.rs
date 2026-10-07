//! H_live under repeated kicks (lab run 20261007-0800-fermi-a91f).
//!
//! `cargo run --release -p emergent-shipmem --example hlive -- state [m]`
//!   The state floor: every ship of a program convoy (the frozen ladder's Rate(0.0) rung)
//!   kicked K times, K in {1,2,4,16,64,256,1024}. Per-ship bits = empirical entropy of the
//!   deviation of the four kicked columns (t, E, L, w) from the program, per ordinal — what a
//!   lossless store of current states must pay on top of the shared program — against the draw
//!   account 44*K bits (a store that never re-encodes, or a logged history).
//!
//! `cargo run --release -p emergent-shipmem --example hlive -- shelf [m] [epochs] [x]`
//!   The shipped store: the same convoy in a Shelf; each epoch kicks a fraction x of the ships
//!   through the hot tier, then compacts (the idle-time reabsorption). Records bytes per live
//!   ship after each compact, the state floor of the same states, hot-update ns per kick,
//!   compact ns, and checks the decode against the oracle bit for bit, by birth ordinal.
//!   Output goes to $HLIVE_OUT (default stdout), one JSON per line.
use emergent_shipmem::codec::{Buf, MAXC};
use emergent_shipmem::pop::{ladder, Pop, Rng, Rung};
use emergent_shipmem::shelf::{Kind, Shelf, Ship};
use std::collections::HashMap;
use std::io::Write;
use std::time::Instant;

/// The Rate(0.0) convoy: members in birth order, plus each ordinal's program values.
fn convoy(m: usize, g: u64) -> (Vec<Ship>, Vec<[u64; MAXC]>) {
    let (members, _, prog) = ladder(Rung::Rate(0.0), m, g);
    let pr = prog.expect("rate rung has a program");
    let pv = (0..m as u64)
        .map(|i| {
            let mut v = [0u64; MAXC];
            for f in 0..5 {
                v[f] = pr[f].at(i);
            }
            v
        })
        .collect();
    (members, pv)
}

fn entropy(cols: &[HashMap<i64, u64>], n: u64) -> f64 {
    let mut h = 0.0;
    for m in cols {
        for &c in m.values() {
            let p = c as f64 / n as f64;
            h -= p * p.log2();
        }
    }
    h
}

/// Deviation entropy of the kicked columns against the program, per ordinal.
fn state_bits(members: &[Ship], pv: &[[u64; MAXC]], cols: &[usize]) -> f64 {
    let n = members.len() as u64;
    let maps: Vec<HashMap<i64, u64>> = cols
        .iter()
        .map(|&c| {
            let mut m: HashMap<i64, u64> = HashMap::with_capacity(1 << 12);
            for (i, s) in members.iter().enumerate() {
                *m.entry(s[c] as i64 - pv[i][c] as i64).or_insert(0) += 1;
            }
            m
        })
        .collect();
    entropy(&maps, n)
}


fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mode = args.get(1).cloned().unwrap_or_default();
    let out = std::env::var("HLIVE_OUT").unwrap_or_else(|_| "/dev/stdout".into());
    let mut w = std::fs::File::create(&out).expect("out");
    let cols = [0usize, 2, 3, 4];
    match mode.as_str() {
        "state" => {
            let m: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(1 << 20);
            for k in [1u32, 2, 4, 16, 64, 256, 1024] {
                let (mut members, pv) = convoy(m, 7);
                let mut r = Rng::new(0xBADC0DE + k as u64);
                let t = Instant::now();
                for s in members.iter_mut() {
                    for _ in 0..k {
                        *s = Pop::Convoy.kick(s, &mut r);
                    }
                }
                let kick_ns = t.elapsed().as_nanos() as f64 / (m as f64 * k as f64);
                let sb = state_bits(&members, &pv, &cols);
                let model = 4.0 * (11.0 + 0.5 * (k as f64).log2());
                writeln!(
                    w,
                    "{{\"mode\":\"state\",\"m\":{},\"k\":{},\"state_bits\":{:.3},\"model_bits\":{:.3},\"draw_bits\":{:.1},\"kick_ns\":{:.1}}}",
                    m, k, sb, model, 44.0 * k as f64, kick_ns
                )
                .unwrap();
            }
        }
        "shelf" => {
            let m: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(1 << 20);
            let epochs: usize = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(8);
            let x: f64 = args.get(4).and_then(|s| s.parse().ok()).unwrap_or(0.25);
            let (members, pv) = convoy(m, 7);
            let mut shelf = Shelf::new(5, 128, Pop::Convoy.orders(), true);
            let mut src = members.clone();
            let t = Instant::now();
            shelf.add_group(&mut src, Kind::Slot { grid: 0 });
            let enc_ms = t.elapsed().as_nanos() as f64 / 1e6;
            shelf.shrink();
            // Birth-ordinal -> handle. add_group splits into groups of at most MAXG slots;
            // a block's `start` is its slot within its group's own domain.
            let mut handles = vec![0u32; m];
            let mut off = 0usize;
            for g in 0..shelf.groups.len() {
                let gr = shelf.groups[g];
                for bi in gr.first as usize..(gr.first + gr.nb) as usize {
                    let b = shelf.blocks[bi];
                    if b.n == 0 {
                        continue;
                    }
                    for slot in 0..b.n as u32 {
                        handles[off + (b.start + slot) as usize] = (bi as u32) << 8 | slot;
                    }
                }
                off += gr.n as usize;
            }
            let mut oracle = members.clone();
            let mut krng = Rng::new(0xE7E47);
            let mut hot_ns: Vec<u64> = Vec::with_capacity(1 << 17);
            for ep in 1..=epochs {
                let victims: Vec<usize> = (0..m).filter(|_| krng.bernoulli_p(x)).collect();
                let mut out = [0u64; MAXC];
                for &i in &victims {
                    let h = handles[i];
                    shelf.get(h, &mut out);
                    let new = Pop::Convoy.kick(&out, &mut krng);
                    let t = Instant::now();
                    shelf.update(h, new);
                    hot_ns.push(t.elapsed().as_nanos() as u64);
                    oracle[i] = new;
                }
                let t = Instant::now();
                shelf.compact();
                let compact_ms = t.elapsed().as_nanos() as f64 / 1e6;
                shelf.shrink();
                // Decode every ship by birth ordinal and check bit for bit.
                let mut buf = Buf::default();
                let mut dec: Vec<Ship> = vec![[0u64; MAXC]; m];
                let mut mism = 0usize;
                let mut off = 0usize;
                for g in 0..shelf.groups.len() {
                    let gr = shelf.groups[g];
                    for bi in gr.first as usize..(gr.first + gr.nb) as usize {
                        let b = shelf.blocks[bi];
                        if b.n == 0 {
                            continue;
                        }
                        shelf.decode_into(bi, &mut buf);
                        for (slot, i) in (0..buf.n).zip(off + b.start as usize..) {
                            for c in 0..5 {
                                dec[i][c] = buf.col[c][slot];
                            }
                            mism += (dec[i] != oracle[i]) as usize;
                        }
                    }
                    off += gr.n as usize;
                }
                let sb = state_bits(&dec, &pv, &cols);
                hot_ns.sort_unstable();
                let med = hot_ns[hot_ns.len() / 2] as f64;
                let p99 = hot_ns[(hot_ns.len() as f64 * 0.99) as usize] as f64;
                writeln!(
                    w,
                    "{{\"mode\":\"shelf\",\"m\":{},\"epoch\":{},\"x\":{:.3},\"kbar\":{:.2},\"bytes_per_ship\":{:.4},\"bits_per_ship\":{:.3},\"state_bits\":{:.3},\"floor_gap_bits\":{:.3},\"hot_ns_med\":{:.0},\"hot_ns_p99\":{:.0},\"compact_ms\":{:.1},\"enc_ms\":{:.1},\"mismatches\":{}}}",
                    m, ep, x, x * ep as f64,
                    shelf.bytes() as f64 / shelf.n as f64,
                    shelf.bytes() as f64 * 8.0 / shelf.n as f64,
                    sb,
                    shelf.bytes() as f64 * 8.0 / shelf.n as f64 - sb,
                    med, p99, compact_ms, enc_ms, mism
                )
                .unwrap();
            }
        }
        _ => eprintln!("usage: hlive state [m] | shelf [m] [epochs] [x]   (env HLIVE_OUT=path)"),
    }
}
