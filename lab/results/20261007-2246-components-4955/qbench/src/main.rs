//! Component bench: the event queue (plane.md foundation 2, "one clock, one queue").
//!
//! Question: how far is the shipped Calendar (a 4-ary indexed heap, crates/space events)
//! from the floor of its own workload, where re-predictions move monotonically later
//! (one slot per body) and same-tick events are resolved as one batch (law.md tie rule)?
//!
//! Structures (identical op stream: schedule all n, then pop_min + re-set the same body):
//!  - calendar_scalar : the real Calendar from crates/space, Scalar keys (the engine's interface)
//!  - calendar_u64    : the same algorithm verbatim with u64 keys (isolates the key cost)
//!  - binaryheap      : std BinaryHeap, lazy deletion (the naive control)
//!  - wheel           : monotone bucket queue: O(1) inserts, bucket-sorted drains, far list,
//!                      lazy deletion, side heap for out-of-order re-sets (handoffs)
//!  - floor           : sequential read of the exact verified event stream (memory floor)
//!
//! Every timed cell is preceded by an untimed verification pass asserting the structure
//! pops the identical (tick, body) sequence as the real Calendar.

use emergent_space::events::Calendar;
use emergent_space::orbit::Scalar;
use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::hint::black_box;
use std::time::Instant;

// ------------------------------------------------------------------ wheel ----

const CONSUMED: u64 = u64::MAX;

pub struct Wheel {
    b: usize,
    width: u64,
    base: u64,
    buckets: Vec<Vec<(u64, u32)>>,
    cur: usize, // bucket currently being drained; b == all drained (rebuild needed)
    far: Vec<(u64, u32)>,
    ready: Vec<(u64, u32)>, // sorted ascending, undelivered from ready_at
    ready_at: usize,
    side: BinaryHeap<Reverse<(u64, u32)>>, // re-sets earlier than the drain cursor
    live_t: Vec<u64>,                      // per body: scheduled tick, or CONSUMED
    dead: usize,
    live: usize,
    pub max_batch: usize,
    pub rebuilds: usize,
}

impl Wheel {
    pub fn new(n: usize) -> Self {
        let b = n.max(64).next_power_of_two().min(1 << 22);
        Wheel {
            b,
            width: 0,
            base: 0,
            buckets: vec![Vec::new(); b],
            cur: b,
            far: Vec::with_capacity(n),
            ready: Vec::new(),
            ready_at: 0,
            side: BinaryHeap::new(),
            live_t: vec![CONSUMED; n],
            dead: 0,
            live: 0,
            max_batch: 0,
            rebuilds: 0,
        }
    }

    #[inline]
    fn route(&mut self, t: u64, i: u32) {
        if self.width == 0 {
            self.far.push((t, i));
            return;
        }
        if self.width == 0 || self.base > t {
            self.far.push((t, i));
            return;
        }
        let k = ((t - self.base) / self.width) as usize;
        // At or behind the drain cursor (bucket `cur` is being drained via the sorted
        // ready buffer): exactness only via value order. Correctness never depends on
        // the workload; monotone re-predictions with width <= min delta always route ahead.
        if k <= self.cur {
            self.side.push(Reverse((t, i)));
        } else if k < self.b {
            self.buckets[k].push((t, i));
        } else {
            self.far.push((t, i));
        }
    }

    /// Schedule body i at tick t (or cancel with None).
    pub fn set(&mut self, i: usize, t: Option<u64>) {
        let old = self.live_t[i];
        match t {
            Some(t) => {
                if old == CONSUMED {
                    self.live += 1;
                } else {
                    self.dead += 1;
                }
                self.live_t[i] = t;
                self.route(t, i as u32);
            }
            None => {
                if old != CONSUMED {
                    self.dead += 1;
                    self.live -= 1;
                    self.live_t[i] = CONSUMED;
                }
            }
        }
    }

    fn rebuild(&mut self) {
        debug_assert!(self.ready_at >= self.ready.len());
        debug_assert!(self.side.is_empty());
        let min = self.far.iter().map(|e| e.0).min().expect("far nonempty at rebuild");
        let max = self.far.iter().map(|e| e.0).max().unwrap_or(min);
        self.base = min;
        self.width = ((max - min) / self.b as u64).max(1);
        self.cur = 0;
        let far = std::mem::take(&mut self.far);
        for (t, i) in far {
            let k = (((t - self.base) / self.width) as usize).min(self.b - 1);
            self.buckets[k].push((t, i));
        }
        self.far = Vec::new();
        self.rebuilds += 1;
    }

    pub fn pop_min(&mut self) -> Option<(u64, u32)> {
        loop {
            // 1. deliver from the sorted ready buffer
            while self.ready_at < self.ready.len() {
                let e = self.ready[self.ready_at];
                if let Some(&Reverse(s)) = self.side.peek() {
                    if s < e {
                        break; // side holds an earlier event
                    }
                }
                self.ready_at += 1;
                if self.live_t[e.1 as usize] == e.0 {
                    self.live_t[e.1 as usize] = CONSUMED;
                    self.live -= 1;
                    return Some(e);
                }
                self.dead -= 1;
            }
            // 2. side (out-of-order re-sets)
            if let Some(Reverse(s)) = self.side.pop() {
                if self.live_t[s.1 as usize] == s.0 {
                    self.live_t[s.1 as usize] = CONSUMED;
                    self.live -= 1;
                    return Some(s);
                }
                self.dead -= 1;
                continue;
            }
            // 3. refill ready from the current bucket
            if self.cur == self.b {
                if self.far.is_empty() {
                    debug_assert_eq!(self.live, 0, "live entries must be in some container");
                    return None;
                }
                self.rebuild();
            }
            if self.buckets[self.cur].is_empty() {
                self.cur += 1;
                continue;
            }
            let mut v = std::mem::take(&mut self.buckets[self.cur]);
            self.max_batch = self.max_batch.max(v.len());
            v.sort_unstable();
            self.ready = v;
            self.ready_at = 0;
        }
    }
}

// ---------------------------------------------------- calendar, u64 keys ----
// The shipped algorithm (crates/space/src/events/calendar.rs), keys changed to u64.

const NONE: u32 = u32::MAX;
const ARITY: usize = 4;

pub struct CalendarU64 {
    heap: Vec<(u64, u32)>,
    pos: Vec<u32>,
}

impl CalendarU64 {
    pub fn new(n: usize) -> Self {
        CalendarU64 { heap: Vec::with_capacity(n), pos: vec![NONE; n] }
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
    pub fn set(&mut self, i: usize, t: Option<u64>) {
        let p = self.pos[i];
        if p == NONE {
            if let Some(t) = t {
                self.heap.push((t, i as u32));
                self.up(self.heap.len() - 1);
            }
            return;
        }
        let p = p as usize;
        if let Some(t) = t {
            let old = self.heap[p].0;
            self.heap[p].0 = t;
            if t < old {
                self.up(p);
            } else {
                self.down(p);
            }
        } else {
            self.remove_at(p);
        }
    }
    pub fn pop(&mut self) -> Option<(u64, u32)> {
        let event = *self.heap.first()?;
        self.remove_at(0);
        Some(event)
    }
}

// ------------------------------------------------------------ binaryheap ----

struct BhQueue {
    heap: BinaryHeap<Reverse<(u64, u32)>>,
    live_t: Vec<u64>,
}

impl BhQueue {
    fn new(n: usize) -> Self {
        BhQueue { heap: BinaryHeap::with_capacity(n), live_t: vec![CONSUMED; n] }
    }
    fn set(&mut self, i: usize, t: Option<u64>) {
        if let Some(t) = t {
            self.live_t[i] = t;
            self.heap.push(Reverse((t, i as u32)));
        } else {
            self.live_t[i] = CONSUMED;
        }
    }
    fn pop_min(&mut self) -> Option<(u64, u32)> {
        while let Some(Reverse(e)) = self.heap.pop() {
            if self.live_t[e.1 as usize] == e.0 {
                self.live_t[e.1 as usize] = CONSUMED;
                return Some(e);
            }
        }
        None
    }
}

// -------------------------------------------------- one interface for all ----

trait Q {
    fn set(&mut self, i: usize, t: Option<u64>);
    fn pop_min(&mut self) -> Option<(u64, u32)>;
    fn name(&self) -> &'static str;
}

impl Q for Wheel {
    fn set(&mut self, i: usize, t: Option<u64>) {
        Wheel::set(self, i, t)
    }
    fn pop_min(&mut self) -> Option<(u64, u32)> {
        Wheel::pop_min(self)
    }
    fn name(&self) -> &'static str {
        "wheel"
    }
}

impl Q for CalendarU64 {
    fn set(&mut self, i: usize, t: Option<u64>) {
        CalendarU64::set(self, i, t)
    }
    fn pop_min(&mut self) -> Option<(u64, u32)> {
        CalendarU64::pop(self)
    }
    fn name(&self) -> &'static str {
        "calendar_u64"
    }
}

impl Q for BhQueue {
    fn set(&mut self, i: usize, t: Option<u64>) {
        BhQueue::set(self, i, t)
    }
    fn pop_min(&mut self) -> Option<(u64, u32)> {
        BhQueue::pop_min(self)
    }
    fn name(&self) -> &'static str {
        "binaryheap"
    }
}

struct CalScalar(Calendar);

impl CalScalar {
    fn new(n: usize) -> Self {
        CalScalar(Calendar::new(n))
    }
}

fn scalar_of(t: u64) -> Scalar {
    Scalar::integer(t as i64)
}

fn tick_of(s: Scalar) -> u64 {
    let e = s.exponent();
    let sig = s.significand() as i128;
    if e >= 62 {
        (sig << (e - 62)) as u64
    } else {
        (sig >> (62 - e)) as u64
    }
}

impl Q for CalScalar {
    fn set(&mut self, i: usize, t: Option<u64>) {
        self.0.set(i, t.map(scalar_of)).expect("calendar range");
    }
    fn pop_min(&mut self) -> Option<(u64, u32)> {
        self.0.pop().map(|(s, i)| (tick_of(s), i as u32))
    }
    fn name(&self) -> &'static str {
        "calendar_scalar"
    }
}

// -------------------------------------------------------------- driver ----

fn splitmix(seed: u64) -> impl FnMut() -> u64 {
    let mut s = seed.wrapping_mul(0x9E3779B97F4A7C15).max(1);
    move || {
        s = s.wrapping_add(0x9E3779B97F4A7C15);
        let mut z = s;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58476D1CE4E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D049BB133111EB);
        z ^ (z >> 31)
    }
}

#[derive(Clone, Copy, PartialEq)]
enum W {
    Belt,      // log-uniform periods over ~325x, 32 kicks per orbit (law.md default cadence)
    Formation, // one period, phase band of 64 ticks: same-tick batches (co-orbital fleet)
    Averaged,  // ~1 kick per orbit (H0190 averaged cadence): huge lookahead
    Perturbed, // belt + a cancel and an earlier re-set every 64 pops (handoffs)
}

fn parse_w(s: &str) -> W {
    match s {
        "belt" => W::Belt,
        "formation" => W::Formation,
        "averaged" => W::Averaged,
        "perturbed" => W::Perturbed,
        _ => panic!("workload"),
    }
}

struct Spec {
    delta: Vec<u64>,
    first: Vec<u64>,
}

fn spec(w: W, n: usize, seed: u64) -> Spec {
    let mut rng = splitmix(seed);
    let mut delta = Vec::with_capacity(n);
    let mut first = Vec::with_capacity(n);
    for _ in 0..n {
        match w {
            W::Belt | W::Perturbed => {
                let u = (rng() & 0xFFFF_FFFF) as f64 / 4294967296.0;
                let p = (2.0f64.powf(21.0 + u * 8.35) * 32.0) as u64; // multiple of 32
                let d = p / 32;
                delta.push(d);
                first.push(rng() % p);
            }
            W::Formation => {
                let d = 1u64 << 23; // P = 2^28, 32 kicks per orbit
                delta.push(d);
                first.push(rng() % 64);
            }
            W::Averaged => {
                let u = (rng() & 0xFFFF_FFFF) as f64 / 4294967296.0;
                let p = (2.0f64.powf(21.0 + u * 8.35)) as u64;
                delta.push(p);
                first.push(rng() % p);
            }
        }
    }
    Spec { delta, first }
}

struct RunStats {
    build_s: f64,
    drive_s: f64,
    pops: usize,
    samples: Vec<u32>,
    max_batch: usize,
    rebuilds: usize,
    seq: Vec<(u64, u32)>,
}

/// Drive one structure over the shared op stream. `record` captures the pop sequence.
fn drive(q: &mut dyn Q, sp: &Spec, pops: usize, w: W, record: bool) -> RunStats {
    let n = sp.delta.len();
    let t0 = Instant::now();
    for i in 0..n {
        q.set(i, Some(sp.first[i]));
    }
    let build_s = t0.elapsed().as_secs_f64();

    let mut seq = if record { Vec::with_capacity(pops) } else { Vec::new() };
    let mut samples = Vec::with_capacity(pops / 64 + 16);
    let t1 = Instant::now();
    let mut done = 0usize;
    let mut k = 0u64;
    while done < pops {
        let sample = done & 63 == 0;
        let a = if sample { Some(Instant::now()) } else { None };
        let Some((t, i)) = q.pop_min() else { break };
        if record {
            seq.push((t, i));
        }
        if w == W::Perturbed && k % 64 == 0 {
            let j = ((k as usize).wrapping_mul(2654435761) % n) | 1;
            q.set(j, None);
            q.set(j, Some(t + sp.delta[j] / 8));
        }
        q.set(i as usize, Some(t + sp.delta[i as usize]));
        if let Some(a) = a {
            let ns = a.elapsed().as_nanos();
            samples.push(ns.min(u32::MAX as u128) as u32);
        }
        k += 1;
        done += 1;
    }
    let drive_s = t1.elapsed().as_secs_f64();
    RunStats { build_s, drive_s, pops: done, samples, max_batch: 0, rebuilds: 0, seq }
}

fn pct(sorted: &[u32], q: f64) -> u32 {
    if sorted.is_empty() {
        return 0;
    }
    let idx = ((q * sorted.len() as f64) as usize).min(sorted.len() - 1);
    sorted[idx]
}

fn json_cell(w: W, n: usize, seed: u64, name: &str, st: &RunStats) -> String {
    let mut s = st.samples.clone();
    s.sort_unstable();
    format!(
        "{{\"workload\":\"{}\",\"n\":{},\"seed\":{},\"structure\":\"{}\",\"pops\":{},\"build_s\":{:.4},\"drive_s\":{:.4},\"ns_per_event\":{:.1},\"p50_ns\":{},\"p99_ns\":{},\"p999_ns\":{},\"max_sample_ns\":{},\"max_batch\":{},\"rebuilds\":{}}}",
        match w { W::Belt => "belt", W::Formation => "formation", W::Averaged => "averaged", W::Perturbed => "perturbed" },
        n, seed, name, st.pops, st.build_s, st.drive_s,
        st.drive_s * 1e9 / st.pops as f64,
        pct(&s, 0.50), pct(&s, 0.99), pct(&s, 0.999), s.last().copied().unwrap_or(0),
        st.max_batch, st.rebuilds,
    )
}

/// The floor: deliver the exact verified stream by sequential read.
fn floor(stream: &[(u64, u32)]) -> f64 {
    let mut h: u64 = 0;
    let t = Instant::now();
    for &(tick, i) in stream {
        h = h.rotate_left(13) ^ tick ^ (i as u64).wrapping_mul(0x9E3779B97F4A7C15);
    }
    let d = t.elapsed().as_secs_f64();
    black_box(h);
    d
}

fn verify_or_die(name: &str, got: &[(u64, u32)], want: &[(u64, u32)]) {
    if got == want {
        return;
    }
    let at = got.iter().zip(want).position(|(a, b)| a != b).unwrap_or(got.len().min(want.len()));
    eprintln!(
        "SEQUENCE MISMATCH {} at {}: got {:?} want {:?} (lens {}/{})",
        name, at,
        got.get(at), want.get(at), got.len(), want.len()
    );
    std::process::exit(2);
}

fn main() {
    // args: <workload> <n> <pops> <seed> <mode: verify|time>
    let a: Vec<String> = std::env::args().collect();
    if a.len() < 6 {
        eprintln!("usage: qbench <belt|formation|averaged|perturbed> <n> <pops> <seed> <verify|time>");
        std::process::exit(1);
    }
    let w = parse_w(&a[1]);
    let n: usize = a[2].parse().unwrap();
    let pops: usize = a[3].parse().unwrap();
    let seed: u64 = a[4].parse().unwrap();
    let mode = a[5].clone();
    let sp = spec(w, n, seed);

    // Reference sequence from the shipped Calendar, always verified first.
    let mut cal = CalScalar::new(n);
    let ref_run = drive(&mut cal, &sp, pops, w, true);
    let want = &ref_run.seq;

    if mode == "verify" {
        let mut wheel = Wheel::new(n);
        let r = drive(&mut wheel, &sp, pops, w, true);
        verify_or_die("wheel", &r.seq, want);
        let mut cu = CalendarU64::new(n);
        let r = drive(&mut cu, &sp, pops, w, true);
        verify_or_die("calendar_u64", &r.seq, want);
        let mut bh = BhQueue::new(n);
        let r = drive(&mut bh, &sp, pops, w, true);
        verify_or_die("binaryheap", &r.seq, want);
        println!("verify ok {} n={} pops={} seed={}", a[1], n, pops, seed);
        return;
    }

    // Timed cells (no recording).
    let mut cal = CalScalar::new(n);
    let r = drive(&mut cal, &sp, pops, w, false);
    println!("{}", json_cell(w, n, seed, "calendar_scalar", &r));
    let mut cu = CalendarU64::new(n);
    let r = drive(&mut cu, &sp, pops, w, false);
    println!("{}", json_cell(w, n, seed, "calendar_u64", &r));
    let mut bh = BhQueue::new(n);
    let r = drive(&mut bh, &sp, pops, w, false);
    println!("{}", json_cell(w, n, seed, "binaryheap", &r));
    let mut wheel = Wheel::new(n);
    let r = drive(&mut wheel, &sp, pops, w, false);
    let mut rw = RunStats { max_batch: wheel.max_batch, rebuilds: wheel.rebuilds, ..r };
    println!("{}", json_cell(w, n, seed, "wheel", &rw));

    // Floor: materialize the exact stream with the (verified) wheel, then stream-read it.
    let mut wheel2 = Wheel::new(n);
    let r2 = drive(&mut wheel2, &sp, pops, w, true);
    verify_or_die("wheel-floor", &r2.seq, want);
    let d = floor(&r2.seq);
    rw = RunStats { pops: r2.pops, ..rw };
    println!(
        "{{\"workload\":\"{}\",\"n\":{},\"seed\":{},\"structure\":\"floor\",\"pops\":{},\"build_s\":0,\"drive_s\":{:.4},\"ns_per_event\":{:.1}}}",
        a[1], n, seed, r2.pops, d, d * 1e9 / r2.pops as f64
    );
}
