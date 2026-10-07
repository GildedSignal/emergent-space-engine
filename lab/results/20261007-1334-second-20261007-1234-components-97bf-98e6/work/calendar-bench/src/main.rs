// Calendar bench: the sparse order's event calendar.
//   incumbent: lattice-event's Calendar (indexed 4-ary heap, verbatim structure)
//   candidate: bitmapped timing wheel on integer ticks, intrusive links + lazy overflow heap
//   control:   linear scan of the per-body time array (no structure)
// All three must deliver the identical (tick, body-id ascending) stream; digest equality is
// the positive control. Delays are always >= 1 (lattice-event's entry_time: "smallest s >= 1").

use std::time::Instant;

const NONE: u32 = u32::MAX;

// ---------------- RNG (deterministic, shared) ----------------
struct Rng(u64);
impl Rng {
    fn new(seed: u64) -> Self { Rng(seed.wrapping_mul(2685821657736338717)) }
    fn next(&mut self) -> u64 {
        let mut x = self.0;
        x ^= x << 13; x ^= x >> 7; x ^= x << 17;
        self.0 = x; x
    }
    fn below(&mut self, n: u64) -> u64 { self.next() % n }
}

// ---------------- case-shaped delay draw ----------------
#[derive(Clone, Copy)]
enum Case { A, B, C, D, E, F, S }

fn delay(rng: &mut Rng, c: Case, churn: bool) -> u64 {
    let u = rng.next() >> 11; // 53-bit uniform
    match c {
        // engine-shaped: mostly later, geometric-ish to 2^20, epochs of 64; 15% near-immediate
        Case::A => {
            if churn && (rng.next() >> 63) != 0 { 1 + rng.below(64) }
            else {
                let d = ((u as f64 / (1u64 << 53) as f64) + 1e-12).powf(-1.0 / 1.5); // Pareto tail
                let d = (d.min(1.0e6) as u64).max(1);
                (d / 64 + 1) * 64
            }
        }
        // decrease-key storm: everything wants to be early
        Case::B => 1 + rng.below(64),
        // clustered: all delays within a short window
        Case::C => 1 + rng.below(1024),
        // far horizon: most beyond the wheel window W (2^21)
        Case::D => {
            if (rng.next() >> 63) != 0 { 2u64.pow(21) + rng.below(64 * 2u64.pow(21)) }
            else { 1 + rng.below(1024) }
        }
        // mixed spread+storm: log-uniform over 30 octaves (≈30% beyond the wheel horizon),
        // seasoned with the engine-shaped storm draw (Pareto 1.5, 64-tick epochs) on 1/16 of draws
        Case::E => {
            if rng.next() & 15 == 0 {
                let d = ((u as f64 / (1u64 << 53) as f64) + 1e-12).powf(-1.0 / 1.5);
                ((d.min(1.0e6) as u64).max(1) / 64 + 1) * 64
            } else {
                1 + (u as f64 * 30.0 / (1u64 << 53) as f64).exp2() as u64
            }
        }
        // all-far: every delay beyond the wheel horizon (overflow-tier stress; the corner regime)
        Case::F => W as u64 + rng.below(2 * W as u64),
        // pure spread: log-uniform over 30 octaves, [1, 2^30) (checker's regime, now shipped)
        Case::S => 1 + (u as f64 * 30.0 / (1u64 << 53) as f64).exp2() as u64,
    }
}

// ---------------- incumbent: indexed 4-ary heap (lattice-event's Calendar) ----------------
const ARITY: usize = 4;
struct Cal { heap: Vec<(i64, u32)>, pos: Vec<u32> }
impl Cal {
    fn new(n: usize) -> Self { Cal { heap: Vec::with_capacity(n), pos: vec![NONE; n] } }
    #[inline]
    fn place(&mut self, p: usize, x: (i64, u32)) { self.heap[p] = x; self.pos[x.1 as usize] = p as u32; }
    fn up(&mut self, mut p: usize) {
        let x = self.heap[p];
        while p > 0 {
            let q = (p - 1) / ARITY;
            if x >= self.heap[q] { break; }
            self.place(p, self.heap[q]);
            p = q;
        }
        self.place(p, x);
    }
    fn down(&mut self, mut p: usize) {
        let (x, n) = (self.heap[p], self.heap.len());
        loop {
            let first = ARITY * p + 1;
            if first >= n { break; }
            let mut c = first;
            for k in first + 1..(first + ARITY).min(n) { if self.heap[k] < self.heap[c] { c = k; } }
            if self.heap[c] >= x { break; }
            self.place(p, self.heap[c]);
            p = c;
        }
        self.place(p, x);
    }
    fn remove_at(&mut self, p: usize) {
        self.pos[self.heap[p].1 as usize] = NONE;
        let last = self.heap.pop().expect("non-empty");
        if p < self.heap.len() {
            self.place(p, last);
            self.up(p);
            self.down(self.pos[last.1 as usize] as usize);
        }
    }
    fn set(&mut self, i: usize, t: i64) {
        let p = self.pos[i];
        if p == NONE { self.heap.push((t, i as u32)); self.up(self.heap.len() - 1); return; }
        let p = p as usize;
        let old = self.heap[p].0;
        self.heap[p].0 = t;
        if t < old { self.up(p); } else { self.down(p); }
    }
    fn peek(&self) -> Option<(i64, usize)> { self.heap.first().map(|&(t, i)| (t, i as usize)) }
    fn pop_min(&mut self) -> (i64, u32) { let x = self.heap[0]; self.remove_at(0); x }
}

struct HeapQ { cal: Cal, n: usize }
impl HeapQ {
    fn new(n: usize) -> Self { HeapQ { cal: Cal::new(n), n } }
    #[inline(always)]
    fn set(&mut self, i: usize, t: i64) { self.cal.set(i, t); }
    fn next_tick(&mut self) -> i64 { self.cal.peek().expect("empty").0 }
    fn deliver(&mut self, t: i64, out: &mut Vec<u32>) {
        while let Some((tt, _)) = self.cal.peek() {
            if tt != t { break; }
            let (_, i) = self.cal.pop_min();
            out.push(i);
        }
        debug_assert_eq!(out.len(), out.len()); // order is (t, id) ascending by heap key
    }
    fn pending(&self) -> usize { self.cal.heap.len() }
    fn touches_hint(&self) -> u64 { self.n as u64 }
}

// ---------------- candidate: bitmapped timing wheel + lazy overflow ----------------
const W_BITS: u32 = 21;
const W: usize = 1 << W_BITS;
const WMASK: usize = W - 1;
const NW0: usize = W / 64;      // 2^15 occupancy words
const NW1: usize = NW0 / 64;    // 8 summary words

#[derive(Clone, Copy)]
struct Bod { at: i64, prev: u32, next: u32, loc: u8 } // 24 B: one cache line per op
struct Wheel {
    head: Vec<u32>, bod: Vec<Bod>,
    occ0: Vec<u64>, occ1: Vec<u64>,
    over: Vec<(i64, u32)>,      // lazy overflow min-heap (std is max: store (-t, id))
    cur: usize, now: i64,
}
impl Wheel {
    fn new(n: usize) -> Self {
        Wheel {
            head: vec![NONE; W], bod: vec![Bod { at: -1, prev: NONE, next: NONE, loc: 0 }; n],
            occ0: vec![0; NW0], occ1: vec![0; NW1],
            over: Vec::new(), cur: 0, now: 0,
        }
    }
    #[inline]
    fn bit_set(&mut self, b: usize) {
        let (w, m) = (b >> 6, 1u64 << (b & 63));
        if self.occ0[w] & m == 0 {
            self.occ0[w] |= m;
            self.occ1[w >> 6] |= 1u64 << (w & 63);
        }
    }
    #[inline]
    fn bit_clear(&mut self, b: usize) {
        let (w, m) = (b >> 6, 1u64 << (b & 63));
        self.occ0[w] &= !m;
        if self.occ0[w] == 0 { self.occ1[w >> 6] &= !(1u64 << (w & 63)); }
    }
    fn occ1_next(&self, from_bit: usize) -> Option<usize> {
        let (word, sh) = (from_bit >> 6, from_bit & 63);
        for j in word..NW1 {
            let v = if j == word { self.occ1[j] & (!0u64 << sh) } else { self.occ1[j] };
            if v != 0 { return Some((j << 6) + v.trailing_zeros() as usize); }
        }
        None
    }
    fn occ0_next(&self, from_bit: usize) -> Option<usize> {
        let (from_w, sh) = (from_bit >> 6, from_bit & 63);
        if sh != 0 {
            let v = self.occ0[from_w] & (!0u64 << sh);
            if v != 0 { return Some((from_w << 6) + v.trailing_zeros() as usize); }
            return self.occ1_next(from_w + 1).map(|w| (w << 6) + self.occ0[w].trailing_zeros() as usize);
        }
        self.occ1_next(from_w).map(|w| (w << 6) + self.occ0[w].trailing_zeros() as usize)
    }
    /// cyclic first set bit at or after `from`; caller guarantees non-empty
    fn next_set(&self, from: usize) -> usize {
        if let Some(x) = self.occ0_next(from) { return x; }
        self.occ0_next(0).expect("next_set on empty wheel")
    }
    fn any(&self) -> bool { self.occ1.iter().any(|&v| v != 0) }
    #[inline]
    fn unlink(&mut self, i: usize) {
        let b = self.bod[i].at as usize & WMASK;
        let (p, nx) = (self.bod[i].prev, self.bod[i].next);
        if p != NONE { self.bod[p as usize].next = nx; } else { self.head[b] = nx; }
        if nx != NONE { self.bod[nx as usize].prev = p; }
        if self.head[b] == NONE { self.bit_clear(b); }
        self.bod[i].at = -1; self.bod[i].loc = 0;
    }
    #[inline]
    fn link(&mut self, i: usize, t: i64) {
        let b = t as usize & WMASK;
        let h = self.head[b];
        self.bod[i].next = h; self.bod[i].prev = NONE;
        if h != NONE { self.bod[h as usize].prev = i as u32; }
        self.head[b] = i as u32;
        self.bod[i].at = t; self.bod[i].loc = 1;
        self.bit_set(b);
    }
    fn over_push(&mut self, i: usize, t: i64) {
        self.over.push((t, i as u32));
        let mut k = self.over.len() - 1;
        while k > 0 {
            let par = (k - 1) / 2;
            if self.over[par] <= self.over[k] { break; }
            self.over.swap(par, k); k = par;
        }
        self.bod[i].at = t; self.bod[i].loc = 2;
    }
    /// raw pop of the overflow top (sift-down, no liveness check)
    fn over_pop_raw(&mut self) -> Option<(i64, u32)> {
        if self.over.is_empty() { return None; }
        let x = self.over[0];
        let last = self.over.pop().unwrap();
        if !self.over.is_empty() {
            self.over[0] = last;
            let mut k = 0; let n = self.over.len();
            loop {
                let l = 2 * k + 1;
                if l >= n { break; }
                let mut m = l;
                let r = l + 1;
                if r < n && self.over[r] < self.over[l] { m = r; }
                if self.over[m] >= self.over[k] { break; }
                self.over.swap(m, k); k = m;
            }
        }
        Some(x)
    }
    /// pop until a LIVE entry is returned (lazy deletion); a stale top is discarded
    fn over_pop(&mut self) -> Option<(i64, usize)> {
        loop {
            let (t, id) = self.over_pop_raw()?;
            let id = id as usize;
            if self.bod[id].loc == 2 && self.bod[id].at == t { self.bod[id].at = -1; self.bod[id].loc = 0; return Some((t, id)); }
        }
    }
    /// discard stale tops until the top is live; its tick (None if the tier is empty).
    /// The 97bf bug: `over.first()` was read without this check, so a stale entry's tick
    /// leaked into `next_tick` and the deliver due-loop in every quiet region.
    fn over_top_live(&mut self) -> Option<i64> {
        while let Some(&(t, id)) = self.over.first() {
            if self.bod[id as usize].loc == 2 && self.bod[id as usize].at == t { return Some(t); }
            let _ = self.over_pop_raw(); // stale top: discard, keep looking
        }
        None
    }
    fn cascade(&mut self) {
        while self.over_top_live().map_or(false, |t| t - self.now < W as i64) {
            let (t, id) = self.over_pop().unwrap(); // pops exactly the live top verified above
            self.link(id, t);
        }
    }
    fn set(&mut self, i: usize, t: i64) {
        match self.bod[i].loc {
            1 => self.unlink(i),
            2 => { self.bod[i].loc = 0; self.bod[i].at = -1; } // old lazy entry goes stale
            _ => {}
        }
        if t - self.now >= W as i64 { self.over_push(i, t); } else { self.link(i, t); }
    }
    fn next_tick(&mut self) -> i64 {
        self.cascade();
        if self.any() {
            let b = self.next_set(self.cur);
            self.now + ((b + W - self.cur) % W) as i64
        } else {
            self.over_top_live().expect("empty queue")
        }
    }
    fn deliver(&mut self, t: i64, out: &mut Vec<u32>) {
        self.cascade();
        let b = t as usize & WMASK;
        if self.head[b] == NONE {
            // delivery straight from the overflow tier (wheel empty at this tick)
            loop {
                let due = self.over_top_live().map_or(false, |tt| tt == t);
                if !due { break; }
                let (pt, id) = self.over_pop().unwrap();
                debug_assert_eq!(pt, t); // the due check guarantees tick equality
                out.push(id as u32);
            }
            self.now = t; self.cur = (t as usize) & WMASK;
            out.sort_unstable();
            return;
        }
        debug_assert_eq!(self.cur, b); // driver calls next_tick first
        self.now = t; self.cur = (t as usize) & WMASK;
        while let Some(i) = { let h = self.head[b]; if h == NONE { None } else { Some(h as usize) } } {
            self.head[b] = self.bod[i].next;
            self.bod[i].at = -1; self.bod[i].loc = 0;
            out.push(i as u32);
        }
        self.bit_clear(b);
        out.sort_unstable(); // canonical tie order: ascending body id
    }
    fn pending(&self) -> usize { 0 }
}

// ---------------- control: linear scan ----------------
struct LinQ { at: Vec<i64>, n: usize }
impl LinQ {
    fn new(n: usize) -> Self { LinQ { at: vec![-1; n], n } }
    fn set(&mut self, i: usize, t: i64) { self.at[i] = t; }
    fn next_tick(&mut self) -> i64 {
        let mut m = i64::MAX;
        for i in 0..self.n { if self.at[i] >= 0 && self.at[i] < m { m = self.at[i]; } }
        m
    }
    fn deliver(&mut self, t: i64, out: &mut Vec<u32>) {
        for i in 0..self.n { if self.at[i] == t { out.push(i as u32); self.at[i] = -1; } } // ascending id
    }
    fn pending(&self) -> usize { 0 }
}

// ---------------- driver ----------------
trait Queue { fn set(&mut self, i: usize, t: i64); fn next_tick(&mut self) -> i64; fn deliver(&mut self, t: i64, out: &mut Vec<u32>); }
impl Queue for HeapQ { fn set(&mut self, i: usize, t: i64) { HeapQ::set(self, i, t) } fn next_tick(&mut self) -> i64 { HeapQ::next_tick(self) } fn deliver(&mut self, t: i64, o: &mut Vec<u32>) { HeapQ::deliver(self, t, o) } }
impl Queue for Wheel { fn set(&mut self, i: usize, t: i64) { Wheel::set(self, i, t) } fn next_tick(&mut self) -> i64 { Wheel::next_tick(self) } fn deliver(&mut self, t: i64, o: &mut Vec<u32>) { Wheel::deliver(self, t, o) } }
impl Queue for LinQ { fn set(&mut self, i: usize, t: i64) { LinQ::set(self, i, t) } fn next_tick(&mut self) -> i64 { LinQ::next_tick(self) } fn deliver(&mut self, t: i64, o: &mut Vec<u32>) { LinQ::deliver(self, t, o) } }

#[inline(always)]
fn digest_mix(h: u64, x: u64) -> u64 { (h ^ x).wrapping_mul(0x100000001b3) }

struct Rung { ns_per_op: f64, digest: u64, delivered: u64, sets: u64, p50: f64, p99: f64, p999: f64, steps: u64, burst_mean: f64, burst_max: u64, steady_delivered: u64 }

fn run<S: Queue>(mut q: S, n: usize, c: Case, seed: u64, max_deliver: u64, tail_mode: bool, warmup: u64) -> Rung {
    let mut rng_churn = Rng::new(seed ^ 0xC0FFEE);
    let mut rng_live = Rng::new(seed ^ 0xABCD);
    // pre-generate churn stream (identical across structures)
    let churn_len = 2 * max_deliver as usize + 4096;
    let mut churn: Vec<(u32, i64)> = Vec::with_capacity(churn_len);
    for _ in 0..churn_len {
        let i = rng_churn.below(n as u64) as usize;
        let d = delay(&mut rng_churn, c, true) as i64;
        churn.push((i as u32, d));
    }
    // initial fill: every body pending
    let mut now: i64 = 0;
    let mut t0 = Instant::now();
    for i in 0..n {
        let d = delay(&mut rng_live, c, false) as i64;
        q.set(i, now + d.max(1));
    }
    let fill_ms = t0.elapsed().as_secs_f64() * 1e3;
    let mut h: u64 = 0xcbf29ce484222325;
    let mut delivered: u64 = 0;
    let mut churn_used = 0usize;
    let mut out: Vec<u32> = Vec::new();
    // latency sampling on churn sets
    let sample_start = churn_len / 4;
    let mut samples: Vec<u32> = Vec::new();
    let mut sample_on = tail_mode;
    // steady-state clock: starts after `warmup` deliveries (default 0: whole window, old behaviour)
    let (mut steps, mut burst_sum, mut burst_max) = (0u64, 0u64, 0u64);
    let mut steady_on = warmup == 0;
    let (mut delivered0, mut churn0, mut steps0) = (0u64, 0usize, 0u64);
    if steady_on { delivered0 = 0; churn0 = 0; }
    t0 = Instant::now();
    let mut last_k = 1usize;
    loop {
        if delivered >= max_deliver { break; }
        // churn: one re-prediction per delivered event of the previous step
        for _ in 0..last_k.min(churn.len() - churn_used) {
            let (ci, cd) = churn[churn_used]; churn_used += 1;
            if sample_on && churn_used > sample_start {
                let a = unsafe { std::arch::x86_64::_rdtsc() };
                q.set(ci as usize, now + cd.max(1));
                let b = unsafe { std::arch::x86_64::_rdtsc() };
                samples.push((b - a) as u32);
            } else {
                q.set(ci as usize, now + cd.max(1));
            }
        }
        let t = q.next_tick();
        out.clear();
        q.deliver(t, &mut out);
        now = t;
        last_k = out.len();
        steps += 1; burst_sum += out.len() as u64; if (out.len() as u64) > burst_max { burst_max = out.len() as u64; }
        for &i in out.iter() {
            h = digest_mix(h, t as u64); h = digest_mix(h, i as u64);
            let d = delay(&mut rng_live, c, false) as i64;
            if sample_on && samples.len() < 200_000 {
                let a = unsafe { std::arch::x86_64::_rdtsc() };
                q.set(i as usize, now + d.max(1));
                let b = unsafe { std::arch::x86_64::_rdtsc() };
                samples.push((b - a) as u32);
            } else {
                q.set(i as usize, now + d.max(1));
            }
            delivered += 1;
            if delivered >= max_deliver { break; }
        }
        if !steady_on && delivered >= warmup {
            steady_on = true; t0 = Instant::now();
            delivered0 = delivered; churn0 = churn_used; steps0 = steps;
        }
        if out.is_empty() { panic!("step with no delivery"); }
    }
    let wall = t0.elapsed().as_secs_f64();
    let total_ops = delivered as f64 + churn_used as f64;
    let steady_ops = (delivered - delivered0) as f64 + (churn_used - churn0) as f64;
    let ns_per_op = if steady_on && steady_ops > 0.0 { wall * 1e9 / steady_ops } else { wall * 1e9 / total_ops };
    let (p50, p99, p999) = if tail_mode { percentiles(&mut samples) } else { (0.0, 0.0, 0.0) };
    Rung {
        ns_per_op, digest: h, delivered, sets: churn_used as u64,
        steps: steps - steps0, burst_mean: if steps > steps0 { burst_sum as f64 / (steps - steps0) as f64 } else { 0.0 },
        burst_max, steady_delivered: delivered - delivered0,
        p50, p99, p999,
    }
}

fn percentiles(v: &mut Vec<u32>) -> (f64, f64, f64) {
    if v.is_empty() { return (0.0, 0.0, 0.0); }
    v.sort_unstable();
    let pick = |q: f64| -> f64 { let i = ((v.len() as f64 - 1.0) * q).round() as usize; v[i] as f64 };
    (pick(0.5), pick(0.99), pick(0.999))
}

fn tsc_ghz() -> f64 {
    let a = unsafe { std::arch::x86_64::_rdtsc() };
    let t = Instant::now();
    let mut x = 0u64;
    while t.elapsed().as_secs_f64() < 0.25 { x = x.wrapping_add(1); }
    let b = unsafe { std::arch::x86_64::_rdtsc() };
    (b - a) as f64 / 0.25 / 1e9
}

fn rdtsc_overhead_cycles() -> f64 {
    let mut ds = Vec::with_capacity(100_000);
    for _ in 0..100_000 {
        let a = unsafe { std::arch::x86_64::_rdtsc() };
        let b = unsafe { std::arch::x86_64::_rdtsc() };
        ds.push((b - a) as u32);
    }
    ds.sort_unstable();
    ds[ds.len() / 2] as f64
}

/// floor references: sequential bandwidth and an L1 dependent-chain per op
fn floors() -> (f64, f64) {
    let n = 16 << 20; // 16M u64 = 128 MB per buffer
    let mut a = vec![1u64; n]; let mut b = vec![2u64; n];
    let t = Instant::now();
    for i in 0..n { b[i] = a[i].wrapping_add(b[i]); }
    let w = t.elapsed().as_secs_f64();
    let bw = (2.0 * 8.0 * n as f64) / w; // bytes/s moved (read+write)
    let seq_floor_ns = 16.0 / bw * 1e9; // 16 B per event (write (tick,id), read it back)
    // dependent chain on a tiny array (L1): 4 dependent loads+stores, the minimum a queue op needs
    let mut k = [0u64; 8];
    let t = Instant::now();
    let iters = 20_000_000u64;
    for i in 0..iters {
        let j = ((i >> 7) & 7) as usize;
        k[j] = k[j].wrapping_add(k[(j + 1) & 7]);
        k[(j + 2) & 7] = k[j] ^ k[(j + 3) & 7];
    }
    let w = t.elapsed().as_secs_f64();
    std::hint::black_box(&k);
    let chain_floor_ns = w * 1e9 / iters as f64;
    (seq_floor_ns, chain_floor_ns)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let case = args[1].clone();
    let c = match case.as_str() { "A" => Case::A, "B" => Case::B, "C" => Case::C, "D" => Case::D, "E" => Case::E, "F" => Case::F, "S" => Case::S, _ => panic!("case") };
    let n: usize = args[2].parse().unwrap();
    let seed: u64 = args[3].parse().unwrap();
    let max_deliver: u64 = args[4].parse().unwrap();
    let mode = args[5].clone();
    let which = args[6].clone();
    // args[7]: warmup deliveries before the steady-state clock starts (default 0 = old behaviour)
    let warmup: u64 = args.get(7).map_or(0, |s| s.parse().unwrap());

    if mode == "floors" {
        let (seq, chain) = floors();
        let ghz = tsc_ghz();
        println!("{{\"floors\": true, \"seq_floor_ns\": {seq:.3}, \"chain_floor_ns\": {chain:.3}, \"tsc_ghz\": {ghz:.3}, \"rdtsc_overhead_cycles\": {:.1}}}", rdtsc_overhead_cycles());
        return;
    }

    if mode == "corner" {
        // the checker's corner: every body beyond the horizon, body 0 re-timed far-later.
        // Heap reference: next tick 2W = 4194304. A stale overflow top reads 1.5W = 3145728.
        let n: usize = 8;
        let mut hq = HeapQ::new(n);
        let mut wq = Wheel::new(n);
        for i in 0..n { let t = 2 * W as i64; hq.set(i, t); wq.set(i, t); }
        let stale = (3 * W as i64) / 2;
        hq.set(0, stale); wq.set(0, stale);           // body 0 enters overflow at 1.5W
        hq.set(0, 2 * W as i64); wq.set(0, 2 * W as i64); // re-timed far-later: 1.5W entry goes stale
        let (th, tw) = (hq.next_tick(), wq.next_tick());
        let (mut oh, mut ow) = (Vec::new(), Vec::new());
        if th == tw { hq.deliver(th, &mut oh); wq.deliver(tw, &mut ow); }
        if th != tw || oh != ow {
            println!("{{\"corner\": \"FAIL\", \"heap_next\": {th}, \"wheel_next\": {tw}, \"heap_ids\": {:?}, \"wheel_ids\": {:?}}}", &oh, &ow);
        } else {
            println!("{{\"corner\": \"OK\", \"tick\": {th}, \"ids\": {:?}}}", &oh);
        }
        return;
    }

    if mode == "diff" {
        // differential debug: heap vs wheel, step by step, first divergence printed
        let mut rng_churn = Rng::new(seed ^ 0xC0FFEE);
        let mut rng_live_h = Rng::new(seed ^ 0xABCD);
        let mut rng_live_w = Rng::new(seed ^ 0xABCD);
        let mut churn: Vec<(u32, i64)> = Vec::new();
        for _ in 0..(2 * max_deliver as usize + 4096) {
            let i = rng_churn.below(n as u64) as usize;
            let d = delay(&mut rng_churn, c, true) as i64;
            churn.push((i as u32, d));
        }
        let mut hq = HeapQ::new(n);
        let mut wq = Wheel::new(n);
        let (mut now_h, mut now_w) = (0i64, 0i64);
        for i in 0..n {
            let d = delay(&mut rng_live_h, c, false) as i64;
            hq.set(i, d.max(1));
            let d2 = delay(&mut rng_live_w, c, false) as i64;
            assert_eq!(d, d2);
            wq.set(i, d2.max(1));
        }
        let (mut delivered, mut churn_used, mut last_k) = (0u64, 0usize, 1usize);
        let (mut oh, mut ow) = (Vec::new(), Vec::new());
        for step in 0.. {
            if delivered >= max_deliver { break; }
            for _ in 0..last_k.min(churn.len() - churn_used) {
                let (ci, cd) = churn[churn_used]; churn_used += 1;
                hq.set(ci as usize, now_h + cd.max(1));
                wq.set(ci as usize, now_w + cd.max(1));
            }
            let th = hq.next_tick();
            let tw = wq.next_tick();
            if th != tw {
                let b = if wq.any() { wq.next_set(wq.cur) } else { usize::MAX };
                let mut pend = 0; for i in 0..n { if wq.bod[i].loc == 1 { pend += 1; } }
                println!("DIVERGE step {step}: next_tick heap {th} wheel {tw} (now {now_h}/{now_w}, cur {}, any {}, b_next {}, over_min {:?}, pend {pend}, occ0[0] {:x}, occ1[0] {:x}, head1 {:?} head2 {:?})",
                    wq.cur, wq.any(), b, wq.over.first().map(|&(nt, _)| -nt), wq.occ0[0], wq.occ1[0], wq.head[1] as i64, wq.head[2] as i64);
                return;
            }
            oh.clear(); ow.clear();
            hq.deliver(th, &mut oh);
            wq.deliver(tw, &mut ow);
            if oh != ow {
                println!("DIVERGE step {step} tick {th}: heap {} ids {:?} | wheel {} ids {:?} (cur {}, over_min {:?})",
                    oh.len(), &oh[..oh.len().min(8)], ow.len(), &ow[..ow.len().min(8)], wq.cur, wq.over.first().map(|&(nt, _)| -nt));
                return;
            }
            now_h = th; now_w = tw; last_k = oh.len();
            for &i in oh.iter() {
                let d = delay(&mut rng_live_h, c, false) as i64;
                hq.set(i as usize, now_h + d.max(1));
                let d2 = delay(&mut rng_live_w, c, false) as i64;
                assert_eq!(d, d2);
                wq.set(i as usize, now_w + d2.max(1));
                delivered += 1;
                if delivered >= max_deliver { break; }
            }
        }
        println!("OK: no divergence in {delivered} deliveries");
        return;
    }
    let tail = mode == "tail";

    let r = match which.as_str() {
        "heap" => { let q = HeapQ::new(n); run(q, n, c, seed, max_deliver, tail, warmup) }
        "wheel" => { let q = Wheel::new(n); run(q, n, c, seed, max_deliver, tail, warmup) }
        "linear" => { let q = LinQ::new(n); run(q, n, c, seed, max_deliver, tail, warmup) }
        _ => panic!("struct"),
    };
    println!(
        "{{\"case\": \"{case}\", \"n\": {n}, \"seed\": {seed}, \"struct\": \"{which}\", \"ns_per_op\": {:.2}, \"delivered\": {}, \"sets\": {}, \"digest\": {}, \"steps\": {}, \"burst_mean\": {:.1}, \"burst_max\": {}, \"steady_delivered\": {}, \"p50_cycles\": {:.1}, \"p99_cycles\": {:.1}, \"p999_cycles\": {:.1}, \"tail_mode\": {tail}}}",
        r.ns_per_op, r.delivered, r.sets, r.digest, r.steps, r.burst_mean, r.burst_max, r.steady_delivered, r.p50, r.p99, r.p999
    );
}
