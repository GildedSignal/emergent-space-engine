//! Component bench: the event calendar ("one clock, one queue", docs/plane.md foundation 2).
//!
//! Shipped design: `Calendar` — a 4-ary indexed heap of (tick, slot) with a pos[] side table
//! (crates/space/src/events/calendar.rs, lifted from crates/lattice-event). Candidate: a
//! two-level intrusive bucket wheel (calendar queue, Brown 1988; hierarchical timing wheel,
//! Varghese–Lauck 1987) in lattice-event's own intrusive idiom ("moving a body allocates
//! nothing"). Keys are integer ticks; re-timings land in a bounded future window and pops are
//! monotone — the precondition for O(1) bucket queues.
//!
//! Exactness invariant (positive control): heap and wheel must produce IDENTICAL (tick, slot)
//! pop streams — rolling FNV hash compared. The engine pops by peek + cancel + re-set, with
//! per-frame requeue churn (0.5% of pops re-timed after each frame); both structures get the
//! identical op stream. Under-floor control: a FIFO ring on the uniform workload (equal
//! cadence, spread offsets), where round-robin IS the exact order.
//!
//! Wheel invariants: `base` never advances past the frame target (refill bounded), so every
//! insert is >= base-1; late inserts (t = target < base) sort into the ready buffer, which at
//! that point holds at most one tick's items; level-1 buckets spread into level-0 at window
//! boundaries. Within one tick, order is by slot: the frozen tie rule (law.md, 5 October).
//!
//! Run: rustc -O calbench.rs -o calbench && ./calbench [--n 100000] [--load belt] [--quick]

use std::env;
use std::time::Instant;

const NONE: u32 = u32::MAX;
const ARITY: usize = 4;
const W_LOG2: u32 = 12; // level-0: one bucket per tick, ring of 4096
const W: u64 = 1 << W_LOG2;
const H1: u64 = 1024; // level-1: one bucket per window of W ticks

// ---------- shipped design: 4-ary indexed heap (port of crates/space Calendar) ----------
struct Heap {
    heap: Vec<(u64, u32)>,
    pos: Vec<u32>,
}
impl Heap {
    fn new(n: usize) -> Self {
        Heap { heap: Vec::with_capacity(n), pos: vec![NONE; n] }
    }
    #[inline]
    fn place(&mut self, p: usize, x: (u64, u32)) {
        self.heap[p] = x;
        self.pos[x.1 as usize] = p as u32;
    }
    fn up(&mut self, mut p: usize) {
        let x = self.heap[p];
        while p > 0 {
            let q = (p - 1) / ARITY;
            if x >= self.heap[q] {
                break;
            }
            self.place(p, self.heap[q]);
            p = q;
        }
        self.place(p, x);
    }
    fn down(&mut self, mut p: usize) {
        let (x, n) = (self.heap[p], self.heap.len());
        loop {
            let first = ARITY * p + 1;
            if first >= n {
                break;
            }
            let mut c = first;
            for k in first + 1..(first + ARITY).min(n) {
                if self.heap[k] < self.heap[c] {
                    c = k;
                }
            }
            if self.heap[c] >= x {
                break;
            }
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
    fn set(&mut self, i: usize, t: u64) -> bool {
        let p = self.pos[i];
        if p == NONE {
            self.heap.push((t, i as u32));
            self.up(self.heap.len() - 1);
            return false;
        }
        let p = p as usize;
        let old = self.heap[p].0;
        self.heap[p].0 = t;
        if t < old {
            self.up(p);
        } else {
            self.down(p);
        }
        true
    }
    fn clear(&mut self, i: usize) {
        let p = self.pos[i];
        if p != NONE {
            self.remove_at(p as usize);
        }
    }
    fn peek(&self) -> Option<(u64, u32)> {
        self.heap.first().copied()
    }
    fn bytes(&self) -> usize {
        self.heap.capacity() * 12 + self.pos.capacity() * 4
    }
}

// ---------- candidate: two-level intrusive bucket wheel ----------
// Cancels (the engine's pop: peek, set(e, None), re-set later) must also drop the body's
// ready copy, so ready entries carry the body's generation; a peek skips stale generations.
struct Wheel {
    base: u64, // next tick to close; never advances past the frame target
    heads0: Vec<u32>,
    heads1: Vec<u32>,
    next: Vec<u32>,
    prev: Vec<u32>,
    key: Vec<u64>,
    lvl: Vec<u8>, // 0 = level-0 list, 1 = level-1, 2 = not linked
    gen: Vec<u32>, // bumped on every link; ready entries older than it are stale
    live: Vec<bool>,
    ready: Vec<(u64, u32, u32)>, // (tick, slot, gen); last element is the next exact pop
    late_sorts: u64,
}
impl Wheel {
    fn new(n: usize) -> Self {
        Wheel {
            base: 0,
            heads0: vec![NONE; W as usize],
            heads1: vec![NONE; H1 as usize],
            next: vec![NONE; n],
            prev: vec![NONE; n],
            key: vec![0; n],
            lvl: vec![2; n],
            gen: vec![0; n],
            live: vec![false; n],
            ready: Vec::with_capacity(1 << 12),
            late_sorts: 0,
        }
    }
    /// Unlink i from the list recorded at link time. Returns false if not live.
    fn unlink(&mut self, i: usize) -> bool {
        if !self.live[i] {
            return false;
        }
        if self.lvl[i] == 2 {
            // the body lives in `ready`; its copy is dropped by the generation check in `peek`
            self.live[i] = false;
            return true;
        }
        let lvl = self.lvl[i] as usize;
        let idx = if lvl == 0 {
            (self.key[i] & (W - 1)) as usize
        } else {
            ((self.key[i] >> W_LOG2) & (H1 - 1)) as usize
        };
        let (p, nx) = (self.prev[i], self.next[i]);
        if p != NONE {
            self.next[p as usize] = nx;
        }
        if nx != NONE {
            self.prev[nx as usize] = p;
        }
        let head = if lvl == 0 { &mut self.heads0 } else { &mut self.heads1 };
        if head[idx] == i as u32 {
            head[idx] = nx;
        }
        self.live[i] = false;
        self.lvl[i] = 2;
        true
    }
    /// Push live body i into the bucket holding tick t (t >= base, else the late path).
    #[inline]
    fn link(&mut self, i: usize, t: u64) {
        self.gen[i] = self.gen[i].wrapping_add(1);
        let g = self.gen[i];
        if t < self.base {
            // late insert into an already-drained tick: rare (a requeue at the frame tick).
            self.ready.push((t, i as u32, g));
            self.ready.sort_unstable();
            self.ready.reverse();
            self.late_sorts += 1;
        } else {
            let far = t >= self.base + W;
            let (h, idx) = if far {
                (&mut self.heads1, ((t >> W_LOG2) & (H1 - 1)) as usize)
            } else {
                (&mut self.heads0, (t & (W - 1)) as usize)
            };
            let old = h[idx];
            if old != NONE {
                self.prev[old as usize] = i as u32;
            }
            self.next[i] = old;
            self.prev[i] = NONE;
            h[idx] = i as u32;
            self.lvl[i] = far as u8;
        }
        self.key[i] = t;
        self.live[i] = true;
    }
    fn set(&mut self, i: usize, t: u64) -> bool {
        let was = self.unlink(i);
        self.link(i, t);
        was
    }
    fn clear(&mut self, i: usize) {
        self.unlink(i);
    }
    /// Close the level-0 bucket at tick t into ready, slot order within the tick.
    fn close0(&mut self, t: u64) {
        let idx = (t & (W - 1)) as usize;
        let mut list: Vec<u32> = Vec::new();
        let mut j = self.heads0[idx];
        while j != NONE {
            list.push(j);
            j = self.next[j as usize];
        }
        self.heads0[idx] = NONE;
        if list.is_empty() {
            return;
        }
        for &s in &list {
            self.lvl[s as usize] = 2; // in ready now
        }
        if list.len() > 1 {
            list.sort_unstable(); // same tick => slot order: the frozen tie rule
        }
        for &s in list.iter().rev() {
            self.ready.push((t, s, self.gen[s as usize]));
        }
    }
    /// Spread level-1 bucket of window w into level-0 buckets. Items keep their keys.
    fn spread1(&mut self, w: u64) {
        let idx = (w & (H1 - 1)) as usize;
        let mut j = self.heads1[idx];
        self.heads1[idx] = NONE;
        while j != NONE {
            let nx = self.next[j as usize];
            let t = self.key[j as usize];
            let slot = (t & (W - 1)) as usize;
            let old = self.heads0[slot];
            if old != NONE {
                self.prev[old as usize] = j;
            }
            self.next[j as usize] = old;
            self.prev[j as usize] = NONE;
            self.heads0[slot] = j;
            self.lvl[j as usize] = 0;
            j = nx;
        }
    }
    /// Advance until ready has a live entry, never past `upto` (the frame target).
    fn refill(&mut self, upto: u64) {
        while self.ready.is_empty() && self.base <= upto {
            if self.base & (W - 1) == 0 {
                self.spread1(self.base >> W_LOG2);
            }
            self.close0(self.base);
            self.base += 1;
        }
    }
    /// The next exact pop: skips ready entries whose body was cancelled or re-timed.
    fn peek(&mut self, upto: u64) -> Option<(u64, u32)> {
 loop {
            if self.ready.is_empty() {
                self.refill(upto);
                if self.ready.is_empty() {
                    return None;
                }
            }
            match self.ready.last() {
                Some(&(t, s, g)) if self.live[s as usize] && self.gen[s as usize] == g => {
                    return Some((t, s))
                }
                Some(_) => {
                    self.ready.pop();
                }
                None => return None,
            }
        }
    }
    fn bytes(&self) -> usize {
        (self.heads0.capacity() + self.heads1.capacity() + self.next.capacity() + self.prev.capacity()) * 4
            + self.key.capacity() * 8
            + self.live.capacity()
            + self.lvl.capacity()
            + self.gen.capacity() * 4
            + self.ready.capacity() * 16
    }
}
// ---------- FIFO floor instrument (uniform workload only: round-robin IS exact) ----------
struct Fifo {
    order: Vec<u32>,
    cursor: usize,
}
impl Fifo {
    fn new(offsets: &[u64]) -> Self {
        let mut idx: Vec<u32> = (0..offsets.len() as u32).collect();
        idx.sort_by_key(|&i| (offsets[i as usize], i));
        Fifo { order: idx, cursor: 0 }
    }
    #[inline]
    fn next_event(&mut self) -> Option<u32> {
        let i = *self.order.get(self.cursor)?;
        self.cursor += 1;
        Some(i)
    }
}

// ---------- floor design: the calendar as a counting scan over the generator ----------
// PRINCIPLES #6: store the generator (the per-body next-event time), not the generated (a
// second ordered container). Each frame is one sequential pass over key[] counting due
// ticks, then an exact (tick, id) merge of the collected batch with a small heap of
// same-frame re-due events (cadence < frame). No pos table, no intrusive lists.
const NEVER: u64 = u64::MAX;
struct ScanCal {
    key: Vec<u64>,
    buf: Vec<(u64, u32)>, // collected due events, scattered by tick bucket
    counts: Vec<u32>,     // one counter per tick offset in the frame window
    pend: Vec<(u64, u32)>,// small 4-ary heap of re-due events within the frame
}
impl ScanCal {
    fn new(n: usize) -> Self {
        ScanCal { key: vec![NEVER; n], buf: Vec::new(), counts: vec![0; 260], pend: Vec::new() }
    }
    fn set(&mut self, i: usize, t: u64) -> bool {
        let was = self.key[i] != NEVER;
        self.key[i] = t;
        was
    }
    fn clear(&mut self, i: usize) {
        self.key[i] = NEVER;
    }
    fn pend_push(&mut self, x: (u64, u32)) {
        self.pend.push(x);
        let mut p = self.pend.len() - 1;
        while p > 0 {
            let q = (p - 1) / ARITY;
            if self.pend[p] >= self.pend[q] { break; }
            self.pend.swap(p, q);
            p = q;
        }
    }
    fn pend_pop(&mut self) -> Option<(u64, u32)> {
        if self.pend.is_empty() { return None; }
        let last = self.pend.pop().unwrap();
        if self.pend.is_empty() {
            return Some(last);
        }
        let r = std::mem::replace(&mut self.pend[0], last);
        let mut p = 0usize;
        loop {
            let first = ARITY * p + 1;
            if first >= self.pend.len() { break; }
            let mut c = first;
            for k in first + 1..(first + ARITY).min(self.pend.len()) {
                if self.pend[k] < self.pend[c] { c = k; }
            }
            if self.pend[c] >= self.pend[p] { break; }
            self.pend.swap(p, c);
            p = c;
        }
        Some(r)
    }
    /// Drive the frame exactly: emit every event with tick in [base, target] in (tick, id)
    /// order, re-timing each popped body to t + cad, re-due ones merging back in.
    /// Returns (stream, ns-accounting handled by caller through `emit`).
    fn frame(&mut self, base: u64, target: u64, cad: &[u64], stream: &mut Vec<(u64, u64)>) {
        // The window starts one tick before base: a requeue at the previous frame's tick
        // (= base - 1, the engine's "now") fires first, exactly as the heap's pop loop does.
        let lo = base.saturating_sub(1);
        let span = (target - lo + 1) as usize;
        self.counts[..span].iter_mut().for_each(|c| *c = 0);
        // pass 1: count due ticks
        let mut total = 0u32;
        for i in 0..self.key.len() {
            let k = self.key[i];
            if k == NEVER || k < lo || k > target { continue; }
            let d = (k - lo) as usize;
            self.counts[d] += 1;
            total += 1;
        }
        if total == 0 { return; }
        // prefix offsets
        let mut off = 0u32;
        for d in 0..span {
            let c = self.counts[d];
            self.counts[d] = off;
            off += c;
        }
        self.buf.clear();
        self.buf.resize(total as usize, (0, 0));
        // pass 2: stable scatter by tick (id ascending within each tick: iterated in id order)
        for i in 0..self.key.len() {
            let k = self.key[i];
            if k == NEVER || k < lo || k > target { continue; }
            let d = (k - lo) as usize;
            let slot = self.counts[d] as usize;
            self.buf[slot] = (k, i as u32);
            self.counts[d] += 1;
        }
        // exact merge: batch (tick-major) with the pending re-due heap
        let mut bi = 0usize;
        loop {
            let b = self.buf.get(bi).copied();
            let pn = self.pend.first().copied();
            let nxt = match (b, pn) {
                (None, None) => break,
                (Some(x), None) => { bi += 1; x }
                (None, Some(x)) => { self.pend_pop(); x }
                (Some(x), Some(y)) => {
                    if x <= y { bi += 1; x } else { self.pend_pop(); y }
                }
            };
            let (t, e) = nxt;
            self.clear(e as usize);
            stream.push((t, e as u64));
            let nt = t + cad[e as usize];
            if nt <= target {
                self.pend_push((nt, e));
            } else {
                self.set(e as usize, nt);
            }
        }
        self.pend.clear();
    }
    fn bytes(&self) -> usize {
        self.key.capacity() * 8 + self.buf.capacity() * 12 + self.counts.capacity() * 4 + self.pend.capacity() * 12
    }
}

// ---------- RNG ----------
struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        let mut x = self.0;
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        self.0 = x;
        x
    }
    fn below(&mut self, m: u64) -> u64 {
        self.next() % m
    }
}

// ---------- workloads ----------
fn make_load(n: usize, kind: &str, seed: u64) -> (Vec<u64>, Vec<u64>) {
    let mut rng = Rng(seed.wrapping_mul(0x9E3779B97F4A7C15) | 1);
    let belt = |rng: &mut Rng| {
        let lo = 64f64.ln();
        let hi = 64000f64.ln();
        let u = (rng.next() >> 11) as f64 / (1u64 << 53) as f64;
        (lo + u * (hi - lo)).exp() as u64
    };
    match kind {
        // cadence equal, offsets a spread permutation: FIFO round-robin is the exact order
        "uniform" => {
            let c = 4096u64;
            (vec![c; n], (0..n).map(|i| i as u64 * c / n as u64).collect())
        }
        // cadences log-uniform in [64, 64000]: a 0.4–40 AU belt at 32 kicks/orbit
        "belt" => {
            let cad: Vec<u64> = (0..n).map(|_| belt(&mut rng)).collect();
            let off: Vec<u64> = (0..n).map(|i| rng.below(cad[i].max(1))).collect();
            (cad, off)
        }
        // 10% of bodies on one orbit with 32 shared kick epochs (co-orbital formation), rest belt
        "formation" => {
            let cad: Vec<u64> = (0..n)
                .map(|i| if i % 10 == 0 { 4096 } else { belt(&mut rng) })
                .collect();
            let off: Vec<u64> = (0..n)
                .map(|i| {
                    if i % 10 == 0 {
                        (i as u64 / 10 % 32) * (cad[i] / 32) + rng.below(8)
                    } else {
                        rng.below(cad[i].max(1))
                    }
                })
                .collect();
            (cad, off)
        }
        _ => panic!("unknown load"),
    }
}

fn fnv(pairs: &[(u64, u64)]) -> u64 {
    let mut h: u64 = 0xcbf29ce484222325;
    for &(a, b) in pairs {
        h ^= a;
        h = h.wrapping_mul(0x100000001b3);
        h ^= b;
        h = h.wrapping_mul(0x100000001b3);
    }
    h
}

/// Drive one structure through the engine's op pattern. Returns per-frame per-event ns,
/// the pop-stream hash, pops, and late_sorts (wheel only; 0 for heap).
fn drive_heap(cad: &[u64], off: &[u64], target_pops: u64, frame: u64, seed: u64) -> (Vec<f64>, u64, u64) {
    let n = cad.len();
    let mut h = Heap::new(n);
    let mut rng = Rng(seed.wrapping_mul(0x2545F4914F6CDD1D) | 1);
    for i in 0..n {
        h.set(i, off[i]);
    }
    let mut per_event: Vec<f64> = Vec::new();
    let mut stream: Vec<(u64, u64)> = Vec::new();
    let mut pops = 0u64;
    let mut target = 0u64;
    while pops < target_pops {
        target += frame;
        let tf = Instant::now();
        let mut in_frame = 0u64;
        while let Some((t, e)) = h.peek() {
            if t > target {
                break;
            }
            h.clear(e as usize);
            stream.push((t, e as u64));
            h.set(e as usize, t + cad[e as usize]);
            pops += 1;
            in_frame += 1;
        }
        let churn = (in_frame / 200).max(1);
        for _ in 0..churn {
            let i = rng.below(n as u64) as usize;
            h.set(i, target + rng.below(cad[i].max(1)));
        }
        let dt = tf.elapsed().as_nanos() as f64;
        if in_frame > 0 {
            per_event.push(dt / in_frame as f64);
        }
    }
    (per_event, fnv(&stream), pops)
}

fn drive_wheel(cad: &[u64], off: &[u64], target_pops: u64, frame: u64, seed: u64) -> (Vec<f64>, u64, u64, u64, usize) {
    let n = cad.len();
    let mut w = Wheel::new(n);
    let mut rng = Rng(seed.wrapping_mul(0x2545F4914F6CDD1D) | 1);
    for i in 0..n {
        w.set(i, off[i]);
    }
    let mut per_event: Vec<f64> = Vec::new();
    let mut stream: Vec<(u64, u64)> = Vec::new();
    let mut pops = 0u64;
    let mut target = 0u64;
    while pops < target_pops {
        target += frame;
        let tf = Instant::now();
        let mut in_frame = 0u64;
        while let Some((t, e)) = w.peek(target) {
            if t > target {
                break;
            }
            w.clear(e as usize);
            stream.push((t, e as u64));
            w.set(e as usize, t + cad[e as usize]);
            pops += 1;
            in_frame += 1;
        }
        let churn = (in_frame / 200).max(1);
        for _ in 0..churn {
            let i = rng.below(n as u64) as usize;
            w.set(i, target + rng.below(cad[i].max(1)));
        }
        let dt = tf.elapsed().as_nanos() as f64;
        if in_frame > 0 {
            per_event.push(dt / in_frame as f64);
        }
    }
    let bytes = w.bytes();
    let late = w.late_sorts;
    (per_event, fnv(&stream), pops, late, bytes)
}

fn drive_scan(cad: &[u64], off: &[u64], target_pops: u64, frame: u64, seed: u64) -> (Vec<f64>, u64, u64) {
    let n = cad.len();
    let mut c = ScanCal::new(n);
    let mut rng = Rng(seed.wrapping_mul(0x2545F4914F6CDD1D) | 1);
    for i in 0..n {
        c.set(i, off[i]);
    }
    let mut per_event: Vec<f64> = Vec::new();
    let mut stream: Vec<(u64, u64)> = Vec::new();
    let mut pops = 0u64;
    let mut base = 0u64;
    let mut target = 0u64;
    while pops < target_pops {
        target += frame;
        let tf = Instant::now();
        let before = stream.len();
        c.frame(base, target, cad, &mut stream);
        let in_frame = (stream.len() - before) as u64;
        pops += in_frame;
        let churn = (in_frame / 200).max(1);
        for _ in 0..churn {
            let i = rng.below(n as u64) as usize;
            c.set(i, target + rng.below(cad[i].max(1)));
        }
        let dt = tf.elapsed().as_nanos() as f64;
        if in_frame > 0 {
            per_event.push(dt / in_frame as f64);
        }
        base = target + 1;
    }
    (per_event, fnv(&stream), pops)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let quick = args.iter().any(|a| a == "--quick");
    let mut n_filter: Option<usize> = None;
    let mut load_filter: Option<String> = None;
    let mut i = 1;
    while i < args.len() {
        if args[i] == "--n" {
            n_filter = Some(args[i + 1].parse().unwrap());
            i += 2;
        } else if args[i] == "--load" {
            load_filter = Some(args[i + 1].clone());
            i += 2;
        } else {
            i += 1;
        }
    }
    let sizes: Vec<usize> = if quick {
        vec![100_000]
    } else {
        vec![100_000, 1_000_000, 4_000_000]
    };
    let loads = ["belt", "formation", "uniform"];
    let frame = 256u64;
    println!("[");
    let mut first = true;
    for &n in &sizes {
        if let Some(f) = n_filter {
            if f != n {
                continue;
            }
        }
        for lname in loads {
            if let Some(f) = &load_filter {
                if f != lname {
                    continue;
                }
            }
            for seed in 1..=3u64 {
                let t_start = Instant::now();
                let (cad, off) = make_load(n, lname, seed);
                let target_pops: u64 = if quick { 200_000 } else { (6 * n as u64).min(12_000_000) };

                let (h_ev, h_hash, h_pops) = drive_heap(&cad, &off, target_pops, frame, seed);
                let (w_ev, w_hash, w_pops, late, w_bytes) = drive_wheel(&cad, &off, target_pops, frame, seed);
                let (s_ev, s_hash, s_pops) = drive_scan(&cad, &off, target_pops, frame, seed);
                assert_eq!(h_pops, s_pops, "scan pop count differs");
                let scan_identical = h_hash == s_hash;
                assert_eq!(h_pops, w_pops, "pop count differs");
                let identical = h_hash == w_hash;

                let stat = |v: &Vec<f64>, q: f64| -> f64 {
                    let mut s = v.clone();
                    s.sort_by(|a, b| a.partial_cmp(b).unwrap());
                    s[((q * s.len() as f64) as usize).min(s.len() - 1)]
                };
                let heap_med = stat(&h_ev, 0.5);
                let heap_p99 = stat(&h_ev, 0.99);
                let wheel_med = stat(&w_ev, 0.5);
                let wheel_p99 = stat(&w_ev, 0.99);
                let scan_med = stat(&s_ev, 0.5);
                let scan_p99 = stat(&s_ev, 0.99);

                // FIFO floor: uniform workload only (round-robin exact there)
                let fifo_ns = if lname == "uniform" {
                    let mut f = Fifo::new(&off);
                    let t0 = Instant::now();
                    let mut pops = 0u64;
                    let per_frame = (frame * n as u64 / 4096).max(1);
                    while pops < target_pops {
                        for _ in 0..per_frame {
                            if f.next_event().is_none() {
                                f.cursor = 0;
                            }
                            pops += 1;
                            if pops >= target_pops {
                                break;
                            }
                        }
                    }
                    t0.elapsed().as_nanos() as f64 / pops as f64
                } else {
                    f64::NAN
                };

                let line = format!(
                    "{{\"n\": {}, \"load\": \"{}\", \"seed\": {}, \"heap_ns\": {:.1}, \"heap_p99\": {:.1}, \"wheel_ns\": {:.1}, \"wheel_p99\": {:.1}, \"scan_ns\": {:.1}, \"scan_p99\": {:.1}, \"fifo_floor_ns\": {}, \"speedup\": {:.2}, \"pop_streams_identical\": {}, \"scan_identical\": {}, \"late_sorts\": {}, \"pops\": {}}}",
                    n, lname, seed, heap_med, heap_p99, wheel_med, wheel_p99, scan_med, scan_p99,
                    if fifo_ns.is_nan() { "null".into() } else { format!("{:.1}", fifo_ns) },
                    heap_med / wheel_med, identical, scan_identical, late, h_pops,
                );
                if !first {
                    println!(",");
                }
                print!("{}", line);
                first = false;
                eprintln!(
                    "n={} {} seed={} heap {:.0}ns wheel {:.0}ns scan {:.0}ns identical={} scan_identical={} late={} ({:.1}s)",
                    n, lname, seed, heap_med, wheel_med, scan_med, identical, scan_identical, late,
                    t_start.elapsed().as_secs_f32()
                );
            }
        }
    }
    println!("\n]");
}
