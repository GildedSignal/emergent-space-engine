//! The checker's named experiment for run 20261009-0208-fermi-fe6b, on the SHIPPED
//! encounters crate (path dependency, unmodified): the kick->pair-certificate cascade
//! at N >= 1e6, plus the event-queue churn rate for program-level keys.
//!
//! Cases:
//!   global  <name> <n> <sigma_e> <rho> <a_lo> <a_hi> <kicks>          - one shipped Sorted, shipped kick path
//!   cells   <name> <n> <sigma_e> <rho> <a_lo> <a_hi> <blocks> <kicks> - geometric blocks, per-block Sorted
//!   heap    <depth> <ops>                                             - BinaryHeap churn, packed (t,id) keys
//!   rss                                                               - max RSS in MB
//!
//! One JSON object per line on stdout. Single-threaded timed loops (as shipped).

use emergent_encounters::belt::{make_belt, Spec};
use emergent_encounters::kepler::Body;
use emergent_encounters::method::{pair_events, Stats};
use emergent_encounters::pairs::{is_candidate, sections, Sorted};
use std::collections::BinaryHeap;
use std::time::Instant;

const SAFETY: f64 = 1.1; // shipped main.rs value
const TK: f64 = 10.0 * std::f64::consts::TAU;
const HORIZON: f64 = 1000.0 * std::f64::consts::TAU;
const EPS: f64 = 1e-9; // tidal kick, the steady-state regime

fn spec(name: &str, n: usize, sigma_e: f64, rho: f64, a_lo: f64, a_hi: f64, seed: u64) -> Spec {
    Spec { name: name.into(), n, sigma_e, rho, a_lo, a_hi, keys: 0, seed, orbits: 0.0 }
}

fn kicked_body(old: &Body) -> Body {
    let lam_k = old.mean_anomaly(TK) + old.pom;
    let a_new = old.a * (1.0 + EPS);
    let n_new = a_new.powf(-1.5);
    Body::new(a_new, old.e, old.pom, lam_k - n_new * TK)
}

fn kicked_idx(q: usize, nk: usize, n: usize) -> usize {
    (q * n / nk + 13) % n
}

fn rss_mb() -> f64 {
    let s = std::fs::read_to_string("/proc/self/statm").unwrap();
    let pages: f64 = s.split_whitespace().next().unwrap().parse().unwrap();
    pages * 4096.0 / 1e6
}

fn state_line(tag: &str) {
    let load = std::fs::read_to_string("/proc/loadavg").unwrap();
    println!(
        "{{\"exp\":\"state\",\"when\":\"{}\",\"load\":\"{}\",\"rss_mb\":{:.0}}}",
        tag,
        load.split_whitespace().take(3).collect::<Vec<_>>().join(" "),
        rss_mb()
    );
}

/// The shipped kick path verbatim: range scan + cone test + pair_events over the horizon.
fn recertify_global(b: &[Body], sorted: &Sorted, rho: f64, new: &Body, skip: usize) -> (u64, u64, f64, Stats) {
    let (mut pairs, mut scanned) = (0u64, 0u64);
    let mut st = Stats::default();
    let mut tmp = Vec::new();
    let t0 = Instant::now();
    let (lo, hi) = sorted.range(new.binet()[0], sorted.reach(new));
    for &(_, j) in &sorted.order[lo..hi] {
        if j as usize == skip {
            continue;
        }
        let bj = &b[j as usize];
        scanned += 1;
        if !is_candidate(new, bj, rho) {
            continue;
        }
        tmp.clear();
        pair_events(new, bj, rho, SAFETY, TK, TK + HORIZON, &mut st, &mut tmp);
        pairs += 1;
    }
    (pairs, scanned, t0.elapsed().as_secs_f64(), st)
}

fn case_global(name: &str, n: usize, sigma_e: f64, rho: f64, a_lo: f64, a_hi: f64, nk: usize) {
    let b = make_belt(&spec(name, n, sigma_e, rho, a_lo, a_hi, 20261050));
    let t0 = Instant::now();
    let sorted = Sorted::new(&b, rho);
    let sort_s = t0.elapsed().as_secs_f64();
    let (mut pairs, mut scanned, mut secs, mut stats) = (0u64, 0u64, 0.0, Stats::default());
    // Setup-only decomposition: sections + one first-hit per pair, no horizon run.
    let (mut su_pairs, mut su_secs, mut su_q) = (0u64, 0.0, 0u64);
    for q in 0..nk {
        let i = kicked_idx(q, nk, n);
        let new = kicked_body(&b[i]);
        let (p, s, sec, st) = recertify_global(&b, &sorted, rho, &new, i);
        pairs += p;
        scanned += s;
        secs += sec;
        stats.add(&st);
        let t1 = Instant::now();
        let (lo, hi) = sorted.range(new.binet()[0], sorted.reach(&new));
        for &(_, j) in &sorted.order[lo..hi] {
            if j as usize == i {
                continue;
            }
            let bj = &b[j as usize];
            if is_candidate(&new, bj, rho) {
                su_pairs += 1;
                for sec_ in sections(&new, bj, rho, SAFETY, &mut 0) {
                    let (pi, pj) = (new.period as u128, bj.period as u128);
                    let c = ((sec_.ti as i128 - sec_.tj as i128 + sec_.w1 as i128).rem_euclid(pi as i128)) as u128;
                    let d = (pi - pj % pi) % pi;
                    let w = ((sec_.w1 + sec_.w2).max(0) as u128).min(pi - 1);
                    std::hint::black_box(emergent_encounters::dioph::first_hit(c, d, pi, 0, w, &mut su_q));
                }
            }
        }
        su_secs += t1.elapsed().as_secs_f64();
    }
    let octaves = (a_hi / a_lo).ln();
    println!(
        "{{\"exp\":\"cascade\",\"mode\":\"global\",\"case\":\"{}\",\"n\":{},\"sigma_e\":{},\"rho\":{},\"a_lo\":{},\"a_hi\":{},\"octaves\":{:.2},\"bodies_per_octave\":{:.3e},\"kicks\":{},\"eps\":{:e},\"horizon_orbits\":1000,\
\"sort_s\":{:.2},\"pairs_per_kick\":{:.1},\"scanned_per_kick\":{:.1},\"us_per_kick\":{:.0},\"us_per_pair\":{:.2},\"us_setup_per_pair\":{:.2},\"checks_per_kick\":{:.1},\"hits_per_kick\":{:.1},\"rss_mb\":{:.0}}}",
        name, n, sigma_e, rho, a_lo, a_hi, octaves, n as f64 / octaves, nk, EPS,
        sort_s, pairs as f64 / nk as f64, scanned as f64 / nk as f64, secs * 1e6 / nk as f64,
        secs * 1e6 / pairs.max(1) as f64, su_secs * 1e6 / su_pairs.max(1) as f64,
        stats.checks_total() as f64 / nk as f64, stats.hits_total() as f64 / nk as f64, rss_mb()
    );
}

/// One geometric block (equal body count): its Sorted over its slice, its extrema.
struct Block {
    umin: f64,
    umax: f64,
    ep: f64, // max e/p in the block
    rmin: f64,
    rmax: f64,
    emax: f64,
    pmin: f64,
    sorted: Sorted,
    base: usize, // index offset into the a-sorted body array
}

/// Sound superset reach of x into blk (union extrema dominate every pair's own bounds).
fn block_reach(blk: &Block, x: &Body, rho: f64) -> f64 {
    let rmin = x.rmin().min(blk.rmin);
    let rmax = x.rmax().max(blk.rmax);
    let emax = x.e.max(blk.emax);
    let pmin = x.p.min(blk.pmin);
    let eps = 1.5 * rho * (1.0 + rmax * rmax * emax / (pmin * rmin)) / (rmin * rmin);
    x.e / x.p + blk.ep.max(x.e / x.p) + eps
}

fn case_cells(name: &str, n: usize, sigma_e: f64, rho: f64, a_lo: f64, a_hi: f64, nblocks: usize, nk: usize) {
    let b0 = make_belt(&spec(name, n, sigma_e, rho, a_lo, a_hi, 20261050));
    // Sort by a so blocks are geometric with equal body count.
    let mut idx: Vec<u32> = (0..n as u32).collect();
    idx.sort_by(|&x, &y| b0[x as usize].a.total_cmp(&b0[y as usize].a));
    let b: Vec<Body> = idx.iter().map(|&x| b0[x as usize]).collect();
    let per = n.div_ceil(nblocks);
    let t0 = Instant::now();
    let mut blocks: Vec<Block> = Vec::new();
    let mut start = 0usize;
    while start < n {
        let end = (start + per).min(n);
        let slice = &b[start..end];
        let sorted = Sorted::new(slice, rho);
        let (umin, umax, ep): (f64, f64, f64) = slice.iter().fold((f64::INFINITY, 0.0f64, 0.0f64), |acc, x| {
            (acc.0.min(x.binet()[0]), acc.1.max(x.binet()[0]), acc.2.max(x.e / x.p))
        });
        blocks.push(Block {
            umin,
            umax,
            ep,
            rmin: slice.iter().map(|x| x.rmin()).fold(f64::INFINITY, f64::min),
            rmax: slice.iter().map(|x| x.rmax()).fold(0.0, f64::max),
            emax: slice.iter().map(|x| x.e).fold(0.0, f64::max),
            pmin: slice.iter().map(|x| x.p).fold(f64::INFINITY, f64::min),
            sorted,
            base: start,
        });
        start = end;
    }
    let build_s = t0.elapsed().as_secs_f64();
    let (mut pairs, mut scanned, mut secs, mut stats, mut blocks_hit) = (0u64, 0u64, 0.0, Stats::default(), 0u64);
    let mut tmp = Vec::new();
    for q in 0..nk {
        let i = kicked_idx(q, nk, n); // uniform in the a-sorted array = a-uniform
        let new = kicked_body(&b[i]);
        let un = new.binet()[0];
        let t1 = Instant::now();
        for blk in blocks.iter() {
            let reach = block_reach(blk, &new, rho);
            if un + reach < blk.umin || un - reach > blk.umax {
                continue;
            }
            blocks_hit += 1;
            let (lo, hi) = blk.sorted.range(un, reach);
            for &(_, j) in &blk.sorted.order[lo..hi] {
                let jg = blk.base + j as usize;
                if jg == i {
                    continue;
                }
                let bj = &b[jg];
                scanned += 1;
                if !is_candidate(&new, bj, rho) {
                    continue;
                }
                tmp.clear();
                pair_events(&new, bj, rho, SAFETY, TK, TK + HORIZON, &mut stats, &mut tmp);
                pairs += 1;
            }
        }
        secs += t1.elapsed().as_secs_f64();
    }
    let octaves = (a_hi / a_lo).ln();
    println!(
        "{{\"exp\":\"cascade\",\"mode\":\"cells\",\"case\":\"{}\",\"n\":{},\"blocks\":{},\"per_block\":{},\"sigma_e\":{},\"rho\":{},\"a_lo\":{},\"a_hi\":{},\"octaves\":{:.2},\"kicks\":{},\"eps\":{:e},\
\"build_s\":{:.2},\"blocks_per_kick\":{:.1},\"pairs_per_kick\":{:.1},\"scanned_per_kick\":{:.1},\"us_per_kick\":{:.0},\"us_per_pair\":{:.2},\"checks_per_kick\":{:.1},\"hits_per_kick\":{:.1},\"rss_mb\":{:.0}}}",
        name, n, blocks.len(), per, sigma_e, rho, a_lo, a_hi, octaves, nk, EPS,
        build_s, blocks_hit as f64 / nk as f64, pairs as f64 / nk as f64, scanned as f64 / nk as f64,
        secs * 1e6 / nk as f64, secs * 1e6 / pairs.max(1) as f64,
        stats.checks_total() as f64 / nk as f64, stats.hits_total() as f64 / nk as f64, rss_mb()
    );
}

/// Steady-state heap churn: pop the min, push a later key (every event consumption + reschedule).
fn heap_churn(depth: usize, ops: usize) {
    // BinaryHeap is a max-heap: reverse the comparison for a min-heap.
    #[derive(Eq, PartialEq)]
    struct MinKey { t: u64, id: u32 }
    impl Ord for MinKey {
        fn cmp(&self, o: &Self) -> std::cmp::Ordering {
            o.t.cmp(&self.t).then(o.id.cmp(&self.id))
        }
    }
    impl PartialOrd for MinKey {
        fn partial_cmp(&self, o: &Self) -> Option<std::cmp::Ordering> {
            Some(self.cmp(o))
        }
    }
    let mut hh: BinaryHeap<MinKey> = BinaryHeap::new();
    let mut x: u64 = 0x9E37_79B9_7F4A_7C15;
    let next = |x: &mut u64| -> u64 {
        *x = x.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = *x;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    };
    let t0 = Instant::now();
    for k in 0..depth {
        let t = next(&mut x) % (1u64 << 48);
        hh.push(MinKey { t, id: k as u32 });
    }
    let fill_s = t0.elapsed().as_secs_f64();
    let mut id = depth as u32;
    let t1 = Instant::now();
    for _ in 0..ops {
        let m = hh.pop().unwrap();
        let dt = 1 + next(&mut x) % (1u64 << 20);
        hh.push(MinKey { t: m.t.saturating_add(dt), id });
        id = id.wrapping_add(1);
    }
    let churn_s = t1.elapsed().as_secs_f64();
    println!(
        "{{\"exp\":\"heap\",\"depth\":{},\"ops\":{},\"fill_s\":{:.3},\"churn_s\":{:.3},\"ns_per_pop_push\":{:.0},\"entry_bytes\":{},\"heap_mb\":{:.0},\"rss_mb\":{:.0}}}",
        depth, ops, fill_s, churn_s, churn_s * 1e9 / ops as f64, std::mem::size_of::<MinKey>(),
        depth as f64 * std::mem::size_of::<MinKey>() as f64 / 1e6, rss_mb()
    );
}

/// Exact soundness control: for each kicked body, the candidate id SET from the global
/// Sorted vs from the block decomposition (with per-block sound union bounds). No sampling:
/// set equality per kick, or the missing ids are printed.
fn verify_cells(n: usize, sigma_e: f64, rho: f64, a_lo: f64, a_hi: f64, nblocks: usize, nk: usize) {
    let b0 = make_belt(&spec("verify", n, sigma_e, rho, a_lo, a_hi, 20261050));
    let gsorted = Sorted::new(&b0, rho);
    let mut idx: Vec<u32> = (0..n as u32).collect();
    idx.sort_by(|&x, &y| b0[x as usize].a.total_cmp(&b0[y as usize].a));
    let b: Vec<Body> = idx.iter().map(|&x| b0[x as usize]).collect();
    let per = n.div_ceil(nblocks);
    let mut blocks: Vec<Block> = Vec::new();
    let mut start = 0usize;
    while start < n {
        let end = (start + per).min(n);
        let slice = &b[start..end];
        let sorted = Sorted::new(slice, rho);
        let (umin, umax, ep): (f64, f64, f64) = slice.iter().fold((f64::INFINITY, 0.0f64, 0.0f64), |acc, x| {
            (acc.0.min(x.binet()[0]), acc.1.max(x.binet()[0]), acc.2.max(x.e / x.p))
        });
        blocks.push(Block {
            umin, umax, ep,
            rmin: slice.iter().map(|x| x.rmin()).fold(f64::INFINITY, f64::min),
            rmax: slice.iter().map(|x| x.rmax()).fold(0.0, f64::max),
            emax: slice.iter().map(|x| x.e).fold(0.0, f64::max),
            pmin: slice.iter().map(|x| x.p).fold(f64::INFINITY, f64::min),
            sorted, base: start,
        });
        start = end;
    }
    let position: Vec<u32> = {
        let mut p = vec![0u32; n];
        for (k, &o) in idx.iter().enumerate() {
            p[o as usize] = k as u32;
        }
        p
    };
    let (mut kicks, mut mismatches, mut g_total, mut c_total) = (0u64, 0u64, 0u64, 0u64);
    for q in 0..nk {
        let i_orig = kicked_idx(q, nk, n); // original-array index, same as the global cases
        let new = kicked_body(&b0[i_orig]);
        let un = new.binet()[0];
        // global set
        let mut gs: Vec<u32> = Vec::new();
        let (lo, hi) = gsorted.range(un, gsorted.reach(&new));
        for &(_, j) in &gsorted.order[lo..hi] {
            let j = j as usize;
            if j != i_orig && is_candidate(&new, &b0[j], rho) {
                gs.push(j as u32);
            }
        }
        // cells set (original ids)
        let mut cs: Vec<u32> = Vec::new();
        for blk in blocks.iter() {
            let reach = block_reach(blk, &new, rho);
            if un + reach < blk.umin || un - reach > blk.umax {
                continue;
            }
            let (lo, hi) = blk.sorted.range(un, reach);
            for &(_, j) in &blk.sorted.order[lo..hi] {
                let jp = blk.base + j as usize;
                if jp != position[i_orig] as usize && is_candidate(&new, &b[jp], rho) {
                    cs.push(idx[jp]);
                }
            }
        }
        gs.sort_unstable();
        cs.sort_unstable();
        kicks += 1;
        g_total += gs.len() as u64;
        c_total += cs.len() as u64;
        if gs != cs {
            mismatches += 1;
            let miss: Vec<u32> = gs.iter().filter(|x| !cs.contains(x)).cloned().collect();
            let extra: Vec<u32> = cs.iter().filter(|x| !gs.contains(x)).cloned().collect();
            if mismatches <= 3 {
                println!("{{\"exp\":\"verify-mismatch\",\"kick\":{},\"global_n\":{},\"cells_n\":{},\"missing\":{:?},\"extra\":{:?}}}", q, gs.len(), cs.len(), &miss[..miss.len().min(8)], &extra[..extra.len().min(8)]);
            }
        }
    }
    println!(
        "{{\"exp\":\"verify\",\"n\":{},\"blocks\":{},\"a_hi\":{},\"kicks\":{},\"mismatches\":{},\"global_pairs_per_kick\":{:.1},\"cells_pairs_per_kick\":{:.1}}}",
        n, blocks.len(), a_hi, kicks, mismatches, g_total as f64 / nk as f64, c_total as f64 / nk as f64
    );
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    state_line("before");
    match args[1].as_str() {
        "global" => case_global(
            &args[2], args[3].parse().unwrap(), args[4].parse().unwrap(), args[5].parse().unwrap(),
            args[6].parse().unwrap(), args[7].parse().unwrap(), args[8].parse().unwrap(),
        ),
        "cells" => case_cells(
            &args[2], args[3].parse().unwrap(), args[4].parse().unwrap(), args[5].parse().unwrap(),
            args[6].parse().unwrap(), args[7].parse().unwrap(), args[8].parse().unwrap(),
            args[9].parse().unwrap(),
        ),
        "verify" => verify_cells(
            args[2].parse().unwrap(), args[3].parse().unwrap(), args[4].parse().unwrap(),
            args[5].parse().unwrap(), args[6].parse().unwrap(), args[7].parse().unwrap(),
            args[8].parse().unwrap(),
        ),
        "heap" => heap_churn(args[2].parse().unwrap(), args[3].parse().unwrap()),
        "rss" => println!("{{\"rss_mb\":{:.0}}}", rss_mb()),
        _ => eprintln!("usage: cascade-bench global|cells|heap|rss ..."),
    }
    state_line("after");
}
