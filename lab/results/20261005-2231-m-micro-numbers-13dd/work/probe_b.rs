// Probe B: order-independence from rounding structure. One body kicked by 96 secondaries.
// (i) exact integer accumulation (per-term floor onto a 2^-62 common grid, then ONE quantize)
// vs (ii) a truncating software-float accumulation (crates/space/src/scaled.rs semantics), one
// quantize at the end. 20 shuffled orders x 200 configurations; count distinct final digests.
use std::time::Instant;

fn fdiv(a: i128, b: i128) -> i128 { let q = a / b; if a % b < 0 { q - 1 } else { q } }

#[derive(Clone, Copy)]
struct F { sig: i64, e: i16 }
impl F {
    fn zero(self) -> bool { self.sig == 0 }
    fn mk(mut sig: i128, mut e: i32) -> F {
        if sig == 0 { return F { sig: 0, e: 0 }; }
        let neg = sig < 0;
        let mut a = sig.unsigned_abs();
        let mut bits = 128 - a.leading_zeros() as i32;
        if bits > 63 { let sh = bits - 63; a >>= sh; e += sh; bits = 63; }
        while bits < 63 { a <<= 1; e -= 1; bits += 1; }
        F { sig: if neg { -(a as i64) } else { a as i64 }, e: e as i16 }
    }
    fn from_i(v: i64) -> F { F::mk(v as i128, 62) }
    fn to_f64(self) -> f64 { (self.sig as f64) * 2f64.powi(self.e as i32 - 62) }
    fn mul(self, o: F) -> F { if self.zero() || o.zero() { return F { sig: 0, e: 0 }; }
        F::mk((self.sig as i128) * (o.sig as i128), self.e as i32 + o.e as i32 - 62) }
    fn div(self, o: F) -> F { if self.zero() { return F { sig: 0, e: 0 }; }
        let n = (self.sig as i128) << 62; let d = o.sig as i128;
        let q = if (n >= 0) == (d >= 0) { n / d } else { -((-n) / d) };
        F::mk(q, self.e as i32 - o.e as i32) }
    fn add(self, o: F) -> F {
        if self.zero() { return o; } if o.zero() { return self; }
        let (hi, lo) = if self.e >= o.e { (self, o) } else { (o, self) };
        let d = (hi.e - lo.e) as i32;
        if d > 100 { return hi; }
        F::mk((hi.sig as i128) + ((lo.sig as i128) / (1i128 << d)), hi.e as i32)
    }
}

struct R(u64);
impl R { fn next(&mut self) -> u64 { let mut x = self.0; x ^= x >> 12; x ^= x << 25; x ^= x >> 27; self.0 = x; x.wrapping_mul(0x2545F4914F6CDD1D) }
         fn range(&mut self, m: u64) -> u64 { self.next() % m } }

fn digest(v: [i128; 2]) -> u64 {
    let mut h: u64 = 0xcbf29ce484222325;
    for w in v { for b in w.to_le_bytes() { h ^= b as u64; h = h.wrapping_mul(0x100000001b3); } }
    h
}

fn main() {
    let mut rng = R(0x123456789abcdef);
    let mut exact_multi = 0u32;
    let mut trunc_single = 0u32;
    let mut counts = Vec::new();
    let (mut t_exact, mut t_trunc) = (0u128, 0u128);
    let cfgs = 200u32;
    for _ in 0..cfgs {
        let (bx, by) = ((rng.range(1 << 21) as i64) - (1 << 20), (rng.range(1 << 21) as i64) - (1 << 20));
        let mut srcs = Vec::new();
        for _ in 0..96 {
            let (x, y) = ((rng.range(1 << 22) as i64) - (1 << 21), (rng.range(1 << 22) as i64) - (1 << 21));
            // keep the body out of collisions (the plane refuses those too)
            let (x, y) = if (x - bx).abs() < 64 && (y - by).abs() < 64 { (x + 128, y + 128) } else { (x, y) };
            srcs.push(((1 + rng.range(1 << 26)) as i64, x, y));
        }
        let mut nums: Vec<[i128; 2]> = Vec::new();
        let mut dens: Vec<i128> = Vec::new();
        for &(gm, x, y) in &srcs {
            let dx = (x - bx) as i128; let dy = (y - by) as i128;
            let d2 = dx * dx + dy * dy;
            let d3 = d2 * ((d2 as f64).sqrt() as i128);
            nums.push([gm as i128 * dx, gm as i128 * dy]);
            dens.push(d3.max(1));
        }
        let mut de = std::collections::HashSet::new();
        let te = Instant::now();
        for _ in 0..20 {
            let mut perm: Vec<usize> = (0..96).collect();
            for i in (1..96).rev() { let j = rng.range((i + 1) as u64) as usize; perm.swap(i, j); }
            // (i) exact: per-term floor onto the 2^-62 grid (fixed per source), i128 sums
            let mut sum = [0i128; 2];
            for &i in &perm {
                for c in 0..2 {
                    sum[c] += fdiv(nums[i][c] << 62, dens[i]);
                }
            }
            // ONE quantize to the 2^-10 velocity lattice (round to nearest)
            let v = [fdiv(sum[0] + (1i128 << 61), 1i128 << 52), fdiv(sum[1] + (1i128 << 61), 1i128 << 52)];
            de.insert(digest(v));
        }
        t_exact += te.elapsed().as_nanos();
        if de.len() > 1 { exact_multi += 1; }

        let mut dt = std::collections::HashSet::new();
        let tt = Instant::now();
        for _ in 0..20 {
            let mut perm: Vec<usize> = (0..96).collect();
            for i in (1..96).rev() { let j = rng.range((i + 1) as u64) as usize; perm.swap(i, j); }
            // (ii) the plane's today-path shape: truncating float accumulation, one quantize at the end
            let mut sum = [F { sig: 0, e: 0 }; 2];
            for &i in &perm {
                for c in 0..2 {
                    let (gm, x, y) = srcs[i];
                    let dc = if c == 0 { x - bx } else { y - by };
                    let d3 = dens[i] as i64;
                    sum[c] = sum[c].add(F::from_i(gm).mul(F::from_i(dc)).div(F::from_i(d3)));
                }
            }
            let v = [ (sum[0].to_f64() * 1024.0).round() as i128, (sum[1].to_f64() * 1024.0).round() as i128 ];
            dt.insert(digest(v));
        }
        t_trunc += tt.elapsed().as_nanos();
        if dt.len() == 1 { trunc_single += 1; }
        counts.push(dt.len());
    }
    counts.sort();
    println!("configs={} orders=20", cfgs);
    println!("exact accumulate + one quantize : configs with >1 distinct digest : {}  (prediction: 0)", exact_multi);
    println!("truncating float accumulate    : configs with exactly 1 digest    : {}/{}  (prediction: <200)", trunc_single, cfgs);
    println!("truncating distinct-digest count: median={} max={}", counts[cfgs as usize / 2], *counts.last().unwrap());
    println!("ns per source term: exact-grid {:.0}  trunc-float {:.0}  ratio {:.2}",
        t_exact as f64 / (cfgs as f64 * 20.0 * 96.0), t_trunc as f64 / (cfgs as f64 * 20.0 * 96.0),
        t_exact as f64 / t_trunc as f64);
}
