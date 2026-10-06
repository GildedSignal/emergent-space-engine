//! Designed-kick arithmetic floor (P2): one orbit-averaged kick as the law defines it —
//! integer ΔE/ΔL from the doll's shared moments (fixed point, i64 inputs, i128 products),
//! a quantized-key cycle-memo probe, tube advance by additions. No rebind, no compile.
//! Two access patterns: SHARED (a fleet on one orbit: hot memo) and STREAM (16 B tubes
//! streamed from an array far beyond cache: the bandwidth-bound floor at population scale).
use std::collections::HashMap;
use std::time::Instant;

#[derive(Clone, Copy)]
struct Tube { key: u32, peri: u32, t_peri: i64 } // 16 bytes, the law's tube

struct Cycle { dphi: i64, dt: i64, dtau: i64, slope_e: i64, slope_l: i64 }

/// The doll's moments at this kick epoch: shared by every member (read-only, hot in cache).
struct Moments { qxx: i64, qyy: i64, qzz: i64, qxy: i64, sx: i64, sy: i64, n: u32 }

#[inline(always)]
fn kick(t: &mut Tube, mom: &Moments, memo: &HashMap<u64, Cycle>, carry: &mut i64) -> i64 {
    let k = ((t.key as u64) << 32) | (t.key as u64).rotate_left(17); // quantized (E,L) probe
    let c = match memo.get(&k) { Some(c) => c, None => { return 0 } };
    // fixed point: E,L 32-bit signed fractions; moments 48-bit; products in i128
    let e = (t.key as i32 >> 8) as i64;
    let l = ((t.key as i16) as i32) as i64;
    let q_form = (mom.qxx * e * e + mom.qyy * l * l + 2 * mom.qxy * e * l) as i128;
    let d_e = (q_form * c.slope_e as i128 >> 48) as i64;
    let d_l = ((mom.sx * e + mom.sy * l) as i128 * c.slope_l as i128 >> 48) as i64;
    let j2 = (mom.qzz * (e * e + l * l + 41)) >> 17; // J2 must be in the formula (H0190)
    let t2 = d_e.wrapping_mul(l >> 3) as i128 + (d_l as i128) * (e as i128) + j2 as i128;
    *carry = carry.wrapping_add(t2 as i64);
    // tube advance: additions only (the cycle memo); periapsis angle and time move
    t.peri = t.peri.wrapping_add(c.dphi as u32);
    t.t_peri = t.t_peri.wrapping_add(c.dt + (t2 as i64 >> 20) + mom.n as i64);
    d_e ^ d_l // return something so nothing is optimized out
}

fn main() {
    let n = 1usize << 22; // 4.2 M tubes
    let mom = Moments { qxx: 1 << 40, qyy: 3 << 39, qzz: -(1 << 38), qxy: 1 << 36, sx: 1 << 30, sy: -(3 << 29), n: 7 };
    // memo sized like one fleet's shared cycles + neighbours: small and hot
    let mut memo = HashMap::with_capacity(1 << 14);
    for i in 0..(1u64 << 14) {
        let k = (i << 32) | i.rotate_left(17) ^ (i << 3);
        memo.insert(k, Cycle { dphi: (i as i64) << 3, dt: (i as i64) << 9, dtau: i as i64, slope_e: 1 + (i as i64 & 0xff), slope_l: 1 + ((i >> 8) as i64 & 0x7f) });
    }
    let mut tubes: Vec<Tube> = (0..n).map(|i| Tube { key: ((i as u32 >> 3) & 0x3fff) << 8 | 0x37, peri: i as u32, t_peri: (i as i64) << 4 }).collect();
    // give every tube a memo hit
    for t in tubes.iter_mut() {
        let k = ((t.key as u64) << 32) | (t.key as u64).rotate_left(17);
        memo.get(&k).map(|c| c.dphi); // touch
        let _ = k;
    }
    // keys must probe existing entries: rewrite keys into the memo's key space
    for (i, t) in tubes.iter_mut().enumerate() {
        let base = ((i as u64 >> 6) & 0x3fff) as u32; // ~262k distinct keys over 16k slots? keep dense:
        let idx = (i % (1 << 13)) as u32;
        t.key = idx << 8 | 0x37;
    }
    for i in 0..(1u64 << 14) {
        let key = ((i as u32) << 8 | 0x37) as u64;
        let k = (key << 32) | key.rotate_left(17);
        memo.insert(k, Cycle { dphi: (i as i64) << 3, dt: (i as i64) << 9, dtau: i as i64, slope_e: 1 + (i as i64 & 0xff), slope_l: 1 + ((i >> 8) as i64 & 0x7f) });
    }
    let mut sink: i64 = 0;
    // SHARED/HOT: repeat kicks over a working set that fits L2 (one fleet's slice)
    let hot = &mut tubes[..1 << 15];
    for _ in 0..0 { let _ = hot.len(); }
    let t0 = Instant::now();
    let reps = 2000;
    let mut carry = 0i64;
    for _ in 0..reps {
        for t in hot.iter_mut() { sink ^= kick(t, &mom, &memo, &mut carry); }
    }
    let hot_ns = t0.elapsed().as_nanos() as f64 / (reps as f64 * hot.len() as f64);
    // STREAM: one kick per tube over 4.2 M tubes = 67 MB (> L3 on most cloud nodes)
    let t1 = Instant::now();
    for t in tubes.iter_mut() { sink ^= kick(t, &mom, &memo, &mut carry); }
    let stream_ns = t1.elapsed().as_nanos() as f64 / n as f64;
    println!("{{\"hot_ns_per_kick\": {hot_ns:.1}, \"stream_ns_per_kick\": {stream_ns:.1}, \"tubes\": {n}, \"bytes_streamed\": {}, \"sink\": {sink}, \"carry\": {carry}}}", n * 16);
}
