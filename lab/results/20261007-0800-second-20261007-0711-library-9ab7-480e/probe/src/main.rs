//! The shipped plane's own event-size stream (the checker's named experiment for run
//! 20261007-0711-library-9ab7). No engine file is touched: the harness drives
//! `emergent_universe::scenario::plane` through its public API, exactly as the shipped
//! `tail` example does — resolve one item per call (`Budget::events(1)`), which moves
//! *when* work is done and never *what*, so the digest is the unlimited run's digest
//! (verified once per configuration against a `Budget::unlimited` run: same digest).
//!
//! Per frame it writes one fixed 48-byte little-endian record:
//!   0 u32 frame · 4 u32 items resolved · 8 u32 kicks · 12 u16 opens · 14 u16 boundaries
//!   16 u16 handoffs · 18 u16 slices · 20 u16 decisions · 22 u16 encounters
//!   24 u16 leavers · 26 u16 refused · 28 u16 lost
//!   32 f32 frame wall ms · 36 f32 items' summed µs · 40 f32 top item µs · 44 u8 kind
//! (kind 0..4 = planet, moon, ship, player, fleet, the engine's own `Stats::items` lanes;
//! 5 = unattributed). Top-1 per frame keeps the pooled top-N exact for N up to the number
//! of frames — all a Hill plot needs. Records rotate across part files of ≤ 72 000
//! frames (≤ 3.5 MB each).
//!
//! `plane_events FRAMES RTF SEED MEMBERS ORDER(sp|de) OUTPREFIX [flat]`
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Budget, Config};
use std::io::Write;
use std::time::Instant;

const REC: usize = 48;
const PART: usize = 72_000;

fn put(b: &mut [u8], off: usize, v: u32) {
    b[off..off + 4].copy_from_slice(&v.to_le_bytes());
}
fn put16(b: &mut [u8], off: usize, v: u64) {
    b[off..off + 2].copy_from_slice(&(v.min(u16::MAX as u64) as u16).to_le_bytes());
}
fn putf(b: &mut [u8], off: usize, v: f32) {
    b[off..off + 4].copy_from_slice(&v.to_le_bytes());
}

fn main() {
    let a: Vec<String> = std::env::args().skip(1).collect();
    let frames: usize = a.first().map(|s| s.parse().unwrap()).unwrap_or(2000);
    let rtf: f64 = a.get(1).map(|s| s.parse().unwrap()).unwrap_or(1.0);
    let seed: u64 = a.get(2).map(|s| s.parse().unwrap()).unwrap_or(1);
    let members: u64 = a.get(3).map(|s| s.parse().unwrap()).unwrap_or(48);
    let order = match a.get(4).map(|s| s.as_str()).unwrap_or("sp") {
        "de" => Order::Dense,
        _ => Order::Sparse,
    };
    let prefix = a.get(5).cloned().unwrap_or_else(|| format!("seed{seed}"));
    let flat = a.get(6).map(|s| s == "flat").unwrap_or(false);
    let mut p = plane(Config::default(), seed, order, 1, members).unwrap();
    let want = (rtf / 60.0 / TICK_SECONDS) as i64;
    let mut rec = [0u8; REC];
    let mut part: Vec<u8> = Vec::with_capacity(PART * REC);
    let mut files = 0usize;
    let wall = Instant::now();
    let mut tot_items = 0u64;
    let flush = |part: &Vec<u8>, prefix: &str, i: usize| {
        std::fs::write(format!("{prefix}.{i}"), part).unwrap();
    };
    for f in 0..frames {
        let target = p.u.now + want.max(1);
        let fr = Instant::now();
        let s0 = p.u.stats;
        let (mut ev, mut items_us, mut top_us, mut top_k) = (0u32, 0.0f32, 0.0f32, 5u8);
        if flat {
            p.u.advance(target, Budget::unlimited());
            let adv = p.u.advance(target, Budget::events(0));
            p.u.now = adv.horizon.max(p.u.now);
        } else {
            loop {
                let before = p.u.stats;
                let t0 = Instant::now();
                let adv = p.u.advance(target, Budget::events(1));
                let us = t0.elapsed().as_secs_f64() * 1e6;
                if adv.events == 0 {
                    break;
                }
                ev += 1;
                if ev > 500_000 {
                    eprintln!("frame {f}: runaway ({ev} items), stopping");
                    std::process::exit(2);
                }
                items_us += us as f32;
                if us as f32 > top_us {
                    let s = p.u.stats;
                    top_k = (0..5).find(|&k| s.items[k] > before.items[k]).map(|k| k as u8).unwrap_or(5);
                    top_us = us as f32;
                }
            }
            // The presented tick is the horizon of a final empty call (tail.rs semantics).
            let adv = p.u.advance(target, Budget::events(0));
            p.u.now = adv.horizon.max(p.u.now);
        }
        let s1 = p.u.stats;
        let fr_ms = fr.elapsed().as_secs_f64() * 1e3;
        tot_items += ev as u64;
        put(&mut rec, 0, f as u32);
        put(&mut rec, 4, ev);
        put(&mut rec, 8, (s1.kicks - s0.kicks) as u32);
        put16(&mut rec, 12, s1.opens - s0.opens);
        put16(&mut rec, 14, s1.boundaries - s0.boundaries);
        put16(&mut rec, 16, s1.handoffs - s0.handoffs);
        put16(&mut rec, 18, s1.slices - s0.slices);
        put16(&mut rec, 20, s1.decisions - s0.decisions);
        put16(&mut rec, 22, s1.encounters - s0.encounters);
        put16(&mut rec, 24, s1.leavers - s0.leavers);
        put16(&mut rec, 26, s1.refused - s0.refused);
        put16(&mut rec, 28, s1.lost - s0.lost);
        putf(&mut rec, 32, fr_ms as f32);
        putf(&mut rec, 36, items_us);
        putf(&mut rec, 40, top_us);
        rec[44] = top_k;
        part.extend_from_slice(&rec);
        if part.len() >= PART * REC {
            flush(&part, &prefix, files);
            files += 1;
            part.clear();
        }
    }
    if !part.is_empty() {
        flush(&part, &prefix, files);
    }
    let secs = wall.elapsed().as_secs_f64();
    p.u.settle(p.u.now);
    let digest = p.u.digest();
    let s = p.u.stats;
    let order_s = if matches!(order, Order::Dense) { "dense" } else { "sparse" };
    println!(
        "seed {seed} rtf {rtf} members {members} order {order_s} frames {frames} ticks {} items {tot_items} \
kicks {} opens {} boundaries {} handoffs {} slices {} decisions {} encounters {} leavers {} refused {} lost {} \
kinds {:?} wall_s {secs:.2} digest {digest}",
        p.u.now, s.kicks, s.opens, s.boundaries, s.handoffs, s.slices, s.decisions, s.encounters, s.leavers,
        s.refused, s.lost, s.items
    );
}
