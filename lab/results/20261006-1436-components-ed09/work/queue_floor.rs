// Component bench: the event queue (one queue, root-clock deadlines).
// Heap = verbatim copy of crates/space/src/events/calendar.rs (indexed 4-ary heap,
// one slot per body, slot tie order) with Scalar ordering copied from
// crates/space/src/scaled.rs (normalized significand*2^(exp-62); same-sign order is
// (exponent, |significand|)). Wheel = lazy-deletion bucket wheel (hashed timing
// wheel / calendar queue): ring of B buckets of width w ticks, snapshot+sort on
// drain, frontier heap for the open bucket, overflow heap beyond the horizon.
// Keys: heap uses Scalar::integer(tick), wheel uses the raw i64 tick; the two
// orders are identical (integer() is monotone and injective; ties break on slot).
use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::time::Instant;

// ---------- Scalar (ordering + integer() copied from crates/space/src/scaled.rs) ----------
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct Scalar {
    significand: i64,
    exponent: i16,
}
impl Scalar {
    fn integer(n: i64) -> Self {
        if n == 0 {
            return Self { significand: 0, exponent: 0 };
        }
        let bits = 64 - n.unsigned_abs().leading_zeros();
        let shift = bits as i32 - 63;
        let mag = if shift >= 0 { n.unsigned_abs() >> shift } else { n.unsigned_abs() << -shift };
        Self {
            significand: if n < 0 { -(mag as i64) } else { mag as i64 },
            exponent: shift as i16,
        }
    }
}
impl Ord for Scalar {
    fn cmp(&self, rhs: &Self) -> std::cmp::Ordering {
        let signs = self.significand.signum().cmp(&rhs.significand.signum());
        if signs != std::cmp::Ordering::Equal {
            return signs;
        }
        if self.significand == 0 {
            return std::cmp::Ordering::Equal;
        }
        let cmp = (self.exponent, self.significand.abs()).cmp(&(rhs.exponent, rhs.significand.abs()));
        if self.significand < 0 {
            cmp.reverse()
        } else {
            cmp
        }
    }
}
impl PartialOrd for Scalar {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

// ---------- Calendar: verbatim copy of crates/space/src/events/calendar.rs ----------
const NONE: u32 = u32::MAX;
pub struct Calendar {
    heap: Vec<(Scalar, u32)>,
    pos: Vec<u32>,
}
const ARITY: usize = 4;
impl Calendar {
    pub fn new(n: usize) -> Self {
        Calendar { heap: Vec::with_capacity(n), pos: vec![NONE; n] }
    }
    #[inline]
    fn place(&mut self, p: usize, x: (Scalar, u32)) {
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
    fn set_unchecked(&mut self, i: usize, t: Option<Scalar>) -> bool {
        let p = self.pos[i];
        if p == NONE {
            if let Some(t) = t {
                self.heap.push((t, i as u32));
                self.up(self.heap.len() - 1);
            }
            return false;
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
        true
    }
    pub fn peek(&self) -> Option<(Scalar, usize)> {
        self.heap.first().map(|&(t, i)| (t, i as usize))
    }
    pub fn pop(&mut self) -> Option<(Scalar, usize)> {
        let event = self.peek()?;
        self.remove_at(0);
        Some(event)
    }
    pub fn set(&mut self, slot: usize, time: Option<Scalar>) {
        self.set_unchecked(slot, time);
    }
    fn tick_of(&self, j: usize) -> Option<i64> {
        let p = self.pos[j];
        if p == NONE {
            None
        } else {
            Some(reconstruct(self.heap[p as usize].0))
        }
    }
}

// reconstruct the integer tick from Scalar::integer(n): n = significand * 2^exponent,
// exponent = bits-63 <= 0 for bench magnitudes (< 2^40).
fn reconstruct(s: Scalar) -> i64 {
    if s.significand == 0 {
        return 0;
    }
    let shift = s.exponent as i32;
    if shift <= 0 {
        s.significand >> -shift
    } else {
        s.significand << shift
    }
}

// ---------- Wheel: bucket ring + frontier + overflow, lazy deletion by version ----------
const EMPTY: i64 = i64::MIN;
type Ent = (i64, u32, u32); // (tick, slot, version)
struct Wheel {
    buckets: Vec<Vec<Ent>>,        // ring of B buckets
    cur: Vec<i64>,                 // slot -> current tick, EMPTY = cancelled
    ver: Vec<u32>,                 // slot -> version; entry live iff version matches
    cur_a: i64,                    // absolute bucket index of the ring position
    w: i64,                        // bucket width in ticks
    b: i64,                        // number of ring buckets
    open: Vec<Ent>,                // snapshot of the current bucket, sorted
    open_idx: usize,
    frontier: BinaryHeap<Reverse<Ent>>, // entries inside the open window
    overflow: BinaryHeap<Reverse<Ent>>, // entries at/after the horizon
    stale: u64,                    // stale entries skipped (diagnostic)
    nosort: bool,                  // negative control: serve the snapshot unsorted
}
impl Wheel {
    fn new(n: usize, w: i64, b: i64, start_tick: i64, nosort: bool) -> Self {
        let mut buckets = Vec::with_capacity(b as usize);
        for _ in 0..b {
            buckets.push(Vec::new());
        }
        Wheel {
            buckets,
            cur: vec![EMPTY; n],
            ver: vec![0; n],
            cur_a: start_tick / w, // start_tick >= 0 in every bench
            w,
            b,
            open: Vec::new(),
            open_idx: 0,
            frontier: BinaryHeap::new(),
            overflow: BinaryHeap::new(),
            stale: 0,
            nosort,
        }
    }
    fn horizon(&self) -> i64 {
        (self.cur_a + self.b) * self.w
    }
    /// Route one entry (tick t) to frontier / bucket / overflow.
    fn route(&mut self, t: i64, i: u32, v: u32) {
        if t < self.horizon() {
            let a = t / self.w;
            if a < self.cur_a + 1 {
                self.frontier.push(Reverse((t, i, v)));
            } else {
                self.buckets[(a % self.b) as usize].push((t, i, v));
            }
        } else {
            self.overflow.push(Reverse((t, i, v)));
        }
    }
    fn set(&mut self, i: usize, t: Option<i64>) {
        self.ver[i] = self.ver[i].wrapping_add(1);
        match t {
            None => self.cur[i] = EMPTY,
            Some(t) => {
                self.cur[i] = t;
                let (i, v) = (i as u32, self.ver[i]);
                self.route(t, i, v);
            }
        }
    }
    #[inline]
    fn live(&self, e: &Ent) -> bool {
        self.ver[e.1 as usize] == e.2
    }
    /// Advance the ring until the open snapshot holds a live entry (or nothing remains).
    fn refill(&mut self) {
        let mut empty_run = 0i64;
        while self.open_idx >= self.open.len() {
            // migrate overflow entries that entered the horizon
            loop {
                let fits = match self.overflow.peek() {
                    Some(&Reverse((t, _, _))) if t < self.horizon() => true,
                    _ => false,
                };
                if !fits {
                    break;
                }
                let Reverse(e) = self.overflow.pop().unwrap();
                self.route(e.0, e.1, e.2);
            }
            if self.frontier.is_empty() && self.overflow.is_empty() && empty_run > self.b {
                return; // nothing anywhere; leave the queue empty
            }
            let slot = (self.cur_a % self.b) as usize;
            let entries = std::mem::take(&mut self.buckets[slot]);
            if entries.is_empty() {
                empty_run += 1;
                self.cur_a += 1;
                continue;
            }
            empty_run = 0;
            let ver = &self.ver;
            let mut open: Vec<Ent> = entries.into_iter().filter(|e| ver[e.1 as usize] == e.2).collect();
            self.stale += 0;
            if !self.nosort {
                open.sort_unstable();
            }
            self.open = open;
            self.open_idx = 0;
            self.cur_a += 1;
        }
    }
    fn pop(&mut self) -> Option<(i64, usize)> {
        loop {
            self.refill();
            // skip open entries invalidated after the snapshot
            while self.open_idx < self.open.len() && !self.live(&self.open[self.open_idx]) {
                self.stale += 1;
                self.open_idx += 1;
            }
            // the skip can exhaust the snapshot AFTER refill ran (refill is a no-op
            // while unexamined entries remain): drain the next bucket before deciding,
            // or a just-killed tail returns None with live entries still in buckets
            if self.open_idx >= self.open.len() {
                continue;
            }
            let wheel_next = (self.open_idx < self.open.len()).then(|| self.open[self.open_idx]);
            let front_next = self.frontier.peek().map(|&Reverse(e)| e);
            match (wheel_next, front_next) {
                (None, None) => return None,
                (Some(we), None) => {
                    self.open_idx += 1;
                    return Some((we.0, we.1 as usize));
                }
                (None, Some(fe)) => {
                    let Reverse(e) = self.frontier.pop().unwrap();
                    if self.live(&e) {
                        return Some((e.0, e.1 as usize));
                    }
                    self.stale += 1; // lazy deletion
                }
                (Some(we), Some(fe)) => {
                    if (fe.0, fe.1) <= (we.0, we.1) {
                        let Reverse(e) = self.frontier.pop().unwrap();
                        if self.live(&e) {
                            return Some((e.0, e.1 as usize));
                        }
                        self.stale += 1;
                    } else {
                        self.open_idx += 1;
                        return Some((we.0, we.1 as usize));
                    }
                }
            }
        }
    }
}

// ---------- deterministic RNG ----------
struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E3779B97F4A7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58476D1CE4E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D049BB133111EB);
        z ^ (z >> 31)
    }
    fn below(&mut self, n: u64) -> u64 {
        self.next() % n
    }
}

// ---------- workloads ----------
struct Wl {
    name: &'static str,
    interval: Vec<i64>, // per-slot re-prediction lead (ticks)
}
fn make_wl(name: &'static str, n: usize, seed: u64) -> Wl {
    let mut rng = Rng(seed);
    let interval = match name {
        // belt (TUNING): 16x period spread, cadence interval in [1024, 16384) ticks
        // churn: same belt plus lateral moves and cancels (driver)
        // tail: same belt plus far pareto re-sets (driver)
        "belt" | "churn" | "tail" => (0..n).map(|_| 1024 + (rng.below(16) * 1024) as i64).collect(),
        // formation: one shared interval (all in-flight times over one window)
        "burst" => vec![4096; n],
        _ => unreachable!(),
    };
    Wl { name, interval }
}

#[derive(Clone, Copy, PartialEq)]
enum St {
    Heap,
    Wheel,
    WheelNoSort, // negative control
}

struct Obs {
    hash: u64,
    idx: usize,
    ok: bool,
    mismatch_at: Option<usize>,
}
impl Obs {
    fn new() -> Self {
        Obs { hash: 0x243F6A8885A308D3, idx: 0, ok: true, mismatch_at: None }
    }
    fn see(&mut self, tick: i64, slot: u32, record: &mut Vec<(i64, u32)>, check: Option<&[u64]>) {
        record.push((tick, slot));
        self.hash = self
            .hash
            .rotate_left(17)
            ^ (tick as u64).wrapping_mul(0x9E3779B1)
            ^ (slot as u64).wrapping_mul(0x85EBCA77);
        if let Some(ch) = check {
            if ch.len() > self.idx && ch[self.idx] != self.hash {
                if self.mismatch_at.is_none() {
                    self.mismatch_at = Some(self.idx);
                }
                self.ok = false;
            }
        }
        self.idx += 1;
    }
    fn see_quiet(&mut self, tick: i64, slot: u32) {
        self.hash = self
            .hash
            .rotate_left(17)
            ^ (tick as u64).wrapping_mul(0x9E3779B1)
            ^ (slot as u64).wrapping_mul(0x85EBCA77);
        self.idx += 1;
    }
}
fn rolling(stream: &[(i64, u32)]) -> Vec<u64> {
    let mut hash: u64 = 0x243F6A8885A308D3;
    let mut out = Vec::with_capacity(stream.len());
    for &(tick, slot) in stream {
        hash = hash.rotate_left(17)
            ^ (tick as u64).wrapping_mul(0x9E3779B1)
            ^ (slot as u64).wrapping_mul(0x85EBCA77);
        out.push(hash);
    }
    out
}

fn run(
    wl: &Wl,
    n: usize,
    which: St,
    pops: usize,
    seed: u64,
    record: Option<&mut Vec<(i64, u32)>>,
    check: Option<&[u64]>,
) -> (f64, bool, u64) {
    let mut rng = Rng(seed ^ 0xABCD);
    let mut obs = Obs::new();
    let mut rec: Vec<(i64, u32)> = Vec::new();
    let start = 1_000_000i64;
    let (w, b) = (1i64, 32768i64);
    let mut lateral = Rng(seed ^ 0x7777);
    let churn = wl.name == "churn";
    let tail = wl.name == "tail";
    let mut far_rng = Rng(seed ^ 0xBEEF);
    let t0;
    let dt;
    let stale;
    match which {
        St::Heap => {
            let mut cal = Calendar::new(n);
            for i in 0..n {
                let t = start + rng.below(wl.interval[i] as u64) as i64;
                cal.set(i, Some(Scalar::integer(t)));
            }
            t0 = Instant::now();
            for p in 0..pops {
                let Some((ts, i)) = cal.pop() else { break };
                let tick = reconstruct(ts);
                if record.is_some() || check.is_some() {
                    obs.see(tick, i as u32, &mut rec, check);
                } else {
                    obs.see_quiet(tick, i as u32);
                }
                cal.set(i, Some(Scalar::integer(tick + wl.interval[i])));
                if churn {
                    for _ in 0..2 {
                        let j = lateral.below(n as u64) as usize;
                        if let Some(old) = cal.tick_of(j) {
                            let delta = (lateral.below(257) as i64) - 128;
                            let nt = (old + delta).max(tick + 1);
                            cal.set(j, Some(Scalar::integer(nt)));
                        }
                    }
                    if p % 10 == 0 {
                        let j = lateral.below(n as u64) as usize;
                        if let Some(old) = cal.tick_of(j) {
                            cal.set(j, None);
                            cal.set(j, Some(Scalar::integer(old + 1)));
                        }
                    }
                }
                if tail && p % 20 == 0 {
                    let j = far_rng.below(n as u64) as usize;
                    let far = tick + wl.interval[j] * (16 + (far_rng.below(48)) as i64);
                    cal.set(j, Some(Scalar::integer(far)));
                }
            }
            dt = t0.elapsed().as_secs_f64();
            stale = 0;
        }
        St::Wheel | St::WheelNoSort => {
            let mut wh = Wheel::new(n, w, b, start, which == St::WheelNoSort);
            for i in 0..n {
                let t = start + rng.below(wl.interval[i] as u64) as i64;
                wh.set(i, Some(t));
            }
            t0 = Instant::now();
            for p in 0..pops {
                let Some((tick, i)) = wh.pop() else { break };
                if record.is_some() || check.is_some() {
                    obs.see(tick, i as u32, &mut rec, check);
                } else {
                    obs.see_quiet(tick, i as u32);
                }
                wh.set(i, Some(tick + wl.interval[i]));
                if churn {
                    for _ in 0..2 {
                        let j = lateral.below(n as u64) as usize;
                        if wh.cur[j] != EMPTY {
                            let old = wh.cur[j];
                            let delta = (lateral.below(257) as i64) - 128;
                            let nt = (old + delta).max(tick + 1);
                            wh.set(j, Some(nt));
                        }
                    }
                    if p % 10 == 0 {
                        let j = lateral.below(n as u64) as usize;
                        if wh.cur[j] != EMPTY {
                            let old = wh.cur[j];
                            wh.set(j, None);
                            wh.set(j, Some(old + 1));
                        }
                    }
                }
                if tail && p % 20 == 0 {
                    let j = far_rng.below(n as u64) as usize;
                    let far = tick + wl.interval[j] * (16 + (far_rng.below(48)) as i64);
                    wh.set(j, Some(far));
                }
            }
            dt = t0.elapsed().as_secs_f64();
            stale = wh.stale;
        }
    }
    if let Some(r) = record {
        r.extend_from_slice(&rec);
    }
    (dt / pops as f64 * 1e9, obs.ok && obs.mismatch_at.is_none(), stale)
}

fn loadavg() -> String {
    std::fs::read_to_string("/proc/loadavg").unwrap_or_default().trim().to_string()
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mode = args.get(1).map(|s| s.as_str()).unwrap_or("all");
    if mode == "debug2" {
        let n = 1_000_000usize;
        let seed = 0xFEED ^ (n as u64) ^ (4 * 31);
        let wl = make_wl("belt", n, seed);
        let pops = 200_000usize;
        let mut a: Vec<(i64, u32)> = Vec::new();
        let mut c: Vec<(i64, u32)> = Vec::new();
        run(&wl, n, St::Heap, pops, seed, Some(&mut a), None);
        run(&wl, n, St::WheelNoSort, pops, seed, Some(&mut c), None);
        let mut d = None;
        for k in 0..a.len().min(c.len()) { if a[k] != c[k] { d = Some(k); break; } }
        println!("heap vs nosort n=1e6 first diff {d:?} lens {} {}", a.len(), c.len());
        // same-tick group stats and where group slot order breaks
        let mut groups = 0usize; let mut maxg = 0usize; let mut inversions = 0usize;
        let mut k = 0usize;
        while k < a.len() {
            let mut j = k;
            while j < a.len() && a[j].0 == a[k].0 { j += 1; }
            let g = j - k;
            if g > 1 { groups += 1; maxg = maxg.max(g); }
            for x in k..j { for y in x+1..j { if c[x].1 > c[y].1 { inversions += 1; } } }
            k = j;
        }
        println!("same-tick groups={groups} max_size={maxg} nosort_inversions={inversions}");
        if let Some(k) = d {
            for j in k.saturating_sub(2)..(k+3).min(a.len()) { println!("  heap[{j}]={:?} nosort[{j}]={:?}", a[j], c[j]); }
        }
        return;
    }
    if mode == "debug4" {
        // wheel vs brute-force min over cur[], churn, from pop `start_check` on
        let n = 100_000usize;
        let seed = 0xFEED ^ (n as u64) ^ (5 * 31);
        let wl = make_wl("churn", n, seed);
        let pops = 2_000_000usize;
        let start_check = 60_000usize;
        let mut rng = Rng(seed ^ 0xABCD);
        let mut wh = Wheel::new(n, 1, 32768, 1_000_000, false);
        for i in 0..n {
            let t = 1_000_000 + rng.below(wl.interval[i] as u64) as i64;
            wh.set(i, Some(t));
        }
        let mut lateral = Rng(seed ^ 0x7777);
        let mut far_rng = Rng(seed ^ 0xBEEF);
        for p in 0..pops {
            let got = wh.pop();
            let Some((tick, i)) = got else {
                let mut best: Option<(i64, usize)> = None;
                for j in 0..n {
                    if wh.cur[j] != EMPTY {
                        let e = (wh.cur[j], j);
                        if best.is_none() || e < best.unwrap() { best = Some(e); }
                    }
                }
                println!("drained at pop {p}; brute min over cur: {best:?}");
                if let Some((bt, bj)) = best {
                    println!("  slot {bj}: cur={bt} ver={}", wh.ver[bj]);
                    for (bi, bk) in wh.buckets.iter().enumerate() {
                        for e in bk.iter() { if e.1 as usize == bj { println!("  bucket[{bi}] entry {:?} (cur_a%b={})", e, (wh.cur_a % 32768)); } }
                    }
                    for f in wh.frontier.iter() { let Reverse(e) = f; if e.1 as usize == bj { println!("  frontier entry {:?}", e); } }
                    for f in wh.overflow.iter() { let Reverse(e) = f; if e.1 as usize == bj { println!("  overflow entry {:?}", e); } }
                    println!("  cur_a={} horizon={}", wh.cur_a, wh.horizon());
                }
                break;
            };
            if p >= start_check {
                // brute force: smallest (cur[j], j) over live slots
                let mut best: Option<(i64, usize)> = None;
                for j in 0..n {
                    if wh.cur[j] != EMPTY {
                        let e = (wh.cur[j], j);
                        if best.is_none() || e < best.unwrap() { best = Some(e); }
                    }
                }
                if best != Some((tick, i)) {
                    println!("pop {p}: wheel served {:?} but brute min is {:?}", (tick, i), best);
                    println!("  slot {i}: cur={} ver={}", wh.cur[i], wh.ver[i]);
                    if let Some((bt, bj)) = best {
                        println!("  slot {bj}: cur={} ver={}", wh.cur[bj], wh.ver[bj]);
                        // find all ring/frontier/overflow entries for slot bj
                        for (bi, bk) in wh.buckets.iter().enumerate() {
                            for e in bk.iter() {
                                if e.1 as usize == bj || e.1 as usize == i {
                                    println!("  bucket[{bi}] entry {:?}", e);
                                }
                            }
                        }
                        for f in wh.frontier.iter() { let Reverse(e) = f; if e.1 as usize == bj || e.1 as usize == i { println!("  frontier entry {:?}", e); } }
                        for f in wh.overflow.iter() { let Reverse(e) = f; if e.1 as usize == bj || e.1 as usize == i { println!("  overflow entry {:?}", e); } }
                        println!("  open (len {} idx {}) entries for the two slots:", wh.open.len(), wh.open_idx);
                        for (oi, e) in wh.open.iter().enumerate() { if e.1 as usize == bj || e.1 as usize == i { println!("    open[{oi}] = {:?} live={}", e, wh.live(e)); } }
                        println!("  cur_a={} horizon={}", wh.cur_a, wh.horizon());
                        return;
                    }
                }
            }
            wh.set(i, Some(tick + wl.interval[i]));
            for _ in 0..2 {
                let j = lateral.below(n as u64) as usize;
                if wh.cur[j] != EMPTY {
                    let old = wh.cur[j];
                    let delta = (lateral.below(257) as i64) - 128;
                    let nt = (old + delta).max(tick + 1);
                    wh.set(j, Some(nt));
                }
            }
            if p % 10 == 0 {
                let j = lateral.below(n as u64) as usize;
                if wh.cur[j] != EMPTY {
                    let old = wh.cur[j];
                    wh.set(j, None);
                    wh.set(j, Some(old + 1));
                }
            }
            let _ = far_rng;
        }
        println!("all checked pops consistent");
        return;
    }
    if mode == "debug3" {
        let n = 100_000usize;
        let seed = 0xFEED ^ (n as u64) ^ (5 * 31);
        let wl = make_wl("churn", n, seed);
        let pops = 2_000_000usize;
        let mut a: Vec<(i64, u32)> = Vec::new();
        let mut b: Vec<(i64, u32)> = Vec::new();
        run(&wl, n, St::Heap, pops, seed, Some(&mut a), None);
        run(&wl, n, St::Wheel, pops, seed, Some(&mut b), None);
        println!("lens {} {}", a.len(), b.len());
        for k in 0..a.len().min(b.len()) {
            if a[k] != b[k] {
                println!("first mismatch at {k}");
                let lo = k.saturating_sub(5);
                for j in lo..(k + 5).min(a.len().min(b.len())) {
                    let mark = if a[j] == b[j] { "   " } else { "XX " };
                    println!("  {mark}heap[{j}]={:?}  wheel[{j}]={:?}", a[j], b[j]);
                }
                return;
            }
        }
        println!("no mismatch in {} entries", a.len().min(b.len()));
        return;
    }
    if mode == "debug" {
        let n = 500usize;
        let seed = 0xFEED ^ (n as u64) ^ (4 * 31);
        let wl = make_wl("belt", n, seed);
        let pops = 3000usize;
        let mut a: Vec<(i64, u32)> = Vec::new();
        let mut b: Vec<(i64, u32)> = Vec::new();
        run(&wl, n, St::Heap, pops, seed, Some(&mut a), None);
        run(&wl, n, St::Wheel, pops, seed, Some(&mut b), None);
        let mut c: Vec<(i64, u32)> = Vec::new();
        run(&wl, n, St::WheelNoSort, pops, seed, Some(&mut c), None);
        let mut nosort_diff = None;
        for k in 0..b.len().min(c.len()) {
            if b[k] != c[k] { nosort_diff = Some(k); break; }
        }
        println!("wheel vs wheel-nosort first diff at {nosort_diff:?} (len {} vs {})", b.len(), c.len());
        for k in 0..a.len().min(b.len()) {
            if a[k] != b[k] {
                println!("first mismatch at {k}");
                let lo = k.saturating_sub(3);
                for j in lo..(k + 4).min(a.len()) {
                    println!("  heap[{j}] = {:?}   wheel[{j}] = {:?}", a[j], b.get(j));
                }
                return;
            }
        }
        println!("no mismatch in {} entries", a.len().min(b.len()));
        return;
    }
    let pops: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(2_000_000);
    println!("# loadavg_start {}", loadavg());
    let sizes: Vec<usize> = if mode == "quick" {
        vec![1_000_000]
    } else {
        vec![100_000, 1_000_000, 3_000_000]
    };
    let workloads: &[&str] = if mode == "quick" { &["belt"] } else { &["belt", "churn", "burst", "tail"] };
    for &n in &sizes {
        for &wl_name in workloads {
            let seed = 0xFEED ^ (n as u64) ^ (wl_name.len() as u64 * 31);
            let wl = make_wl(wl_name, n, seed);
            // reference stream from the heap, then its rolling-hash chain
            let mut stream: Vec<(i64, u32)> = Vec::with_capacity(pops);
            let _ = run(&wl, n, St::Heap, pops, seed, Some(&mut stream), None);
            let chain = rolling(&stream);
            drop(stream);
            // timings: 2 reps each, min; wheel reps verified against the chain
            let (h1, _, _) = run(&wl, n, St::Heap, pops, seed, None, None);
            let (h2, _, _) = run(&wl, n, St::Heap, pops, seed, None, None);
            let (q1, ok1, stale) = run(&wl, n, St::Wheel, pops, seed, None, Some(&chain));
            let (q2, ok2, _) = run(&wl, n, St::Wheel, pops, seed, None, Some(&chain));
            let order = if ok1 && ok2 { "ORDER-MATCH" } else { "ORDER-MISMATCH" };
            let ratio = h1.min(h2) / q1.min(q2).max(1e-9);
            println!(
                "{wl_name:6} n={n:>8} heap={h1:8.1}/{h2:8.1}ns wheel={q1:8.1}/{q2:8.1}ns ratio={ratio:6.2}x {order} stale_skips={stale}"
            );
            if wl_name == "belt" || wl_name == "churn" {
                let (_, nosort_ok, _) = run(&wl, n, St::WheelNoSort, pops, seed, None, Some(&chain));
                println!(
                    "       negative(wheel-nosort): {}",
                    if nosort_ok { "BAD: still matches" } else { "fails as expected" }
                );
            }
        }
    }
    println!("# loadavg_end {}", loadavg());
}
