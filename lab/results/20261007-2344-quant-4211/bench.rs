// Queue capacity bench: the plane's deadline calendar (4-ary indexed heap, copied
// from crates/space/src/events/calendar.rs; Scalar keys are integer ticks at every
// callsite, so i64 keys are order-faithful) driven by Universe::advance/rekey's
// frame mechanics (crates/universe/src/universe.rs).
// Variants: V0 ship; V2 triangle-inequality skin on the deadline; V3 = V2 + lazy
// reinsertion of deferred (idle) entities. Build: rustc -O bench.rs -o bench.
use std::time::Instant;

// ---- Calendar (verbatim sift logic; key (i64, u32) ~= (Scalar::integer, slot)) ----
const NONE: u32 = u32::MAX;
const ARITY: usize = 4;
struct Calendar {
    heap: Vec<(i64, u32)>,
    pos: Vec<u32>,
    sets: u64,
    pops: u64,
}
impl Calendar {
    fn new(n: usize) -> Self {
        Calendar { heap: Vec::with_capacity(n), pos: vec![NONE; n], sets: 0, pops: 0 }
    }
    #[inline]
    fn place(&mut self, p: usize, x: (i64, u32)) {
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
        let last = self.heap.pop().unwrap();
        if p < self.heap.len() {
            self.place(p, last);
            let np = self.pos[last.1 as usize] as usize;
            self.up(p);
            self.down(np);
        }
    }
    fn set(&mut self, i: usize, t: Option<i64>) {
        self.sets += 1;
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
    fn peek(&self) -> Option<(i64, usize)> {
        self.heap.first().map(|&(t, i)| (t, i as usize))
    }
    fn pop(&mut self) -> Option<(i64, usize)> {
        self.pops += 1;
        let e = self.peek()?;
        self.remove_at(0);
        Some(e)
    }
}

// ---- scene ----
struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        let mut z = self.0.wrapping_add(0x9E3779B97F4A7C15);
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58476D1CE4E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D049BB133111EB);
        self.0 = z;
        z ^ (z >> 31)
    }
}

struct Body {
    t: i64,        // next event tick (exact always)
    step: u32,     // power-of-two step in ticks
    px: f64,
    py: f64,
    dl: i64,       // cached deadline (V2/V3: lo of the skin interval)
    hi: i64,       // V2/V3: hi of the skin interval
}

const TICKS_PER_S: f64 = 1.0 / 4.925_490_947e-6; // ticks per second (view.rs)
const FPS: f64 = 60.0;
const R_TICKS: f64 = 3.0e9; // ~30 AU system radius
const BUDGET_EVENTS: u64 = 50_000;

struct Scene {
    n: usize,
    bodies: Vec<Body>,
    q: Calendar,
    // V4: dyadic wheel on event time t (exact, player-independent); buckets of
    // width q over absolute ticks, swept as `now` advances. Plus a skinned
    // dl-heap (the V2 rekey) for causal-deadline order and the horizon.
    wheel: Vec<Vec<u32>>,
    wheel_q: i64,
    wheel_next: usize, // next unswept bucket index
    inbox: Vec<u32>,   // V4: due entities the budget left over; drained by the next sweep and by settle
    // stats (per run)
    frames: usize,
}


fn deadline(b: &Body, ox: f64, oy: f64) -> i64 {
    let dx = b.px - ox;
    let dy = b.py - oy;
    b.t + ((dx * dx + dy * dy).sqrt().min(4e18) as i64)
}

#[derive(Default)]
struct FrameStat {
    rekey_ns: u64,
    drain_ns: u64,
    defreq_ns: u64,
    resolve_ns: u64,
    sets: u64,
    peeks: u64,
    sqrt: u64,
    events: u64,
    horizon: i64,
    deferred_out: u64, // deferred entities still parked at frame end (V3)
}

// V: 0 = ship, 2 = skin, 3 = skin + lazy reinsertion
fn run_frame(s: &mut Scene, variant: u8, now: i64, target: i64, dpl: f64, ox: f64, oy: f64, skin: i64, lookahead: i64, unlimited: bool) -> FrameStat {
    let mut st = FrameStat::default();
    let mut deferred: Vec<usize> = Vec::new();
    // ---- rekey (Universe::rekey: every entity's deadline is recomputed and set) ----
    let t0 = Instant::now();
    match variant {
        0 => {
            for e in 0..s.n {
                let dl = deadline(&s.bodies[e], ox, oy);
                s.bodies[e].dl = dl;
                st.sqrt += 1;
                s.q.set(e, Some(dl));
            }
        }
        2 | 4 => {
            let widen = (2.0 * dpl) as i64; // |d_new - d_old| <= player displacement (triangle ineq)
            for e in 0..s.n {
                let b = &mut s.bodies[e];
                b.dl -= widen;
                b.hi += widen;
                if b.hi - b.dl > skin {
                    let dl = deadline(b, ox, oy);
                    b.dl = dl;
                    b.hi = dl;
                    st.sqrt += 1;
                    drop(b);
                    s.q.set(e, Some(dl));
                }
            }
        }
        3 => {
            // Parked entities (pos == NONE, idle) carry no key: reinsert by
            // proximity only, with an exact recompute. Heap members keep the skin.
            let widen = (2.0 * dpl) as i64;
            for e in 0..s.n {
                if s.q.pos[e] == NONE {
                    if s.bodies[e].t <= target + lookahead {
                        let dl = deadline(&s.bodies[e], ox, oy);
                        s.bodies[e].dl = dl;
                        s.bodies[e].hi = dl;
                        st.sqrt += 1;
                        s.q.set(e, Some(dl));
                    }
                } else {
                    let b = &mut s.bodies[e];
                    b.dl -= widen;
                    b.hi += widen;
                    if b.hi - b.dl > skin {
                        let dl = deadline(b, ox, oy);
                        b.dl = dl;
                        b.hi = dl;
                        st.sqrt += 1;
                        drop(b);
                        s.q.set(e, Some(dl));
                    }
                }
            }
        }
        _ => unreachable!(),
    }
    st.rekey_ns = t0.elapsed().as_nanos() as u64;
    st.sets = s.q.sets;
    st.peeks = 0;
    if variant == 4 {
        // ---- V4: sweep the dyadic wheel on t (no drain; due events are found by
        // position, not by search), resolve in skinned dl order under the budget,
        // re-stash leftovers. The dl-heap keeps the horizon (conservative: lo). ----
        let t0 = Instant::now();
        let q = s.wheel_q;
        let mut due: Vec<u32> = s.inbox.drain(..).collect();
        let last = (target / q) as usize;
        if s.wheel.len() <= last + 1 {
            s.wheel.resize(last + 2, Vec::new());
        }
        while s.wheel_next <= last {
            let bkt = std::mem::take(&mut s.wheel[s.wheel_next]);
            for e in bkt {
                if s.bodies[e as usize].t <= target {
                    due.push(e);
                } else {
                    // bucket edge: not yet due, re-stash by exact t
                    let idx = ((s.bodies[e as usize].t / q) as usize).max(s.wheel_next + 1);
                    if idx >= s.wheel.len() {
                        s.wheel.resize(idx + 1, Vec::new());
                    }
                    s.wheel[idx].push(e);
                }
            }
            s.wheel_next += 1;
        }
        st.drain_ns = t0.elapsed().as_nanos() as u64;
        st.peeks = due.len() as u64;
        // causal-deadline order is a spend heuristic only (the budget's
        // preference on overflow); bucket order resolves earliest events first.
        let mut done: u64 = 0;
        for &eu in &due {
            let e = eu as usize;
            if !unlimited && done >= BUDGET_EVENTS {
                // leftover: due but not resolved; the next sweep (and settle) drains the inbox
                s.inbox.push(eu);
                st.deferred_out += 1;
                continue;
            }
            let b = &mut s.bodies[e];
            while b.t <= target {
                b.t += b.step as i64;
                done += 1;
            }
            let dl = deadline(b, ox, oy);
            b.dl = dl;
            b.hi = dl;
            st.sqrt += 1;
            let nt = b.t;
            drop(b);
            s.q.set(e, Some(dl));
            let mut idx = (nt / q) as usize;
            if idx < s.wheel_next {
                idx = s.wheel_next; // due sooner than the sweep front: next frame sees it
            }
            if idx >= s.wheel.len() {
                s.wheel.resize(idx + 1, Vec::new());
            }
            s.wheel[idx].push(e as u32);
        }
        st.resolve_ns = t0.elapsed().as_nanos() as u64;
        st.events = done;
        let mut horizon = target;
        if let Some((lo, _)) = s.q.peek() {
            horizon = horizon.min(lo - 1);
        }
        st.horizon = horizon.max(now);
        st.sets = s.q.sets - st.sets;
        return st;
    }
    // ---- the advance drain (Universe::advance) ----
    let t0 = Instant::now();
    let mut done: u64 = 0;
    loop {
        let Some((_, e)) = s.q.peek() else { break };
        st.peeks += 1;
        let t = s.bodies[e].t;
        if t > target {
            s.q.set(e, None);
            deferred.push(e);
            continue;
        }
        if !unlimited && done >= BUDGET_EVENTS {
            break;
        }
        // resolve_entity: consume all due items, then requeue with a fresh deadline
        let tr = Instant::now();
        let b = &mut s.bodies[e];
        while b.t <= target {
            b.t += b.step as i64;
            done += 1;
        }
        let dl = deadline(b, ox, oy);
        b.dl = dl;
        b.hi = dl;
        st.sqrt += 1;
        drop(b);
        s.q.set(e, Some(dl));
        st.resolve_ns += tr.elapsed().as_nanos() as u64;
    }
    st.drain_ns = t0.elapsed().as_nanos() as u64;
    // ---- deferred requeue (ship: immediate; V3: only if due within lookahead) ----
    let t0 = Instant::now();
    let mut horizon = target;
    if let Some((dl, _)) = s.q.peek() {
        horizon = horizon.min(dl - 1);
    }
    for &e in &deferred {
        if variant < 3 {
            let dl = deadline(&s.bodies[e], ox, oy);
            let b = &mut s.bodies[e];
            b.dl = dl;
            b.hi = dl;
            st.sqrt += 1;
            s.q.set(e, Some(dl));
            horizon = horizon.min(dl - 1);
        } else {
            // V3: stay parked; rekey reinserts when due within the lookahead
            st.deferred_out += 1;
        }
    }
    st.defreq_ns = t0.elapsed().as_nanos() as u64;
    st.events = done;
    st.horizon = horizon.max(now);
    st.sets = s.q.sets - st.sets;
    st
}

fn build(n: usize, seed: u64) -> Scene {
    let mut rng = Rng(seed);
    let mut bodies = Vec::with_capacity(n);
    for _ in 0..n {
        let r = R_TICKS * (rng.next() as f64 / u64::MAX as f64).sqrt();
        let a = 2.0 * std::f64::consts::PI * (rng.next() as f64 / u64::MAX as f64);
        let step_log = 19 + (rng.next() % 6) as u32; // 2^19..2^24 ticks
        let t = (rng.next() % (1 << step_log)) as i64 + 1;
        bodies.push(Body { t, step: 1 << step_log, px: r * a.cos(), py: r * a.sin(), dl: 0, hi: 0 });
    }
    Scene { n, bodies, q: Calendar::new(n), wheel: Vec::new(), wheel_q: 1 << 18, wheel_next: 0, inbox: Vec::new(), frames: 0 }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    // bench <n> <variant> <beta×1000> <rtf> <frames> <skin_log2> <lookahead_log2> <fleet: 0/1> [label]
    let n: usize = args[1].parse().unwrap();
    let variant: u8 = args[2].parse().unwrap();
    let beta = args[3].parse::<u64>().unwrap() as f64 / 1000.0;
    let rtf: f64 = args[4].parse().unwrap();
    let frames: usize = args[5].parse().unwrap();
    let skin: i64 = 1i64 << args[6].parse::<u32>().unwrap();
    let lookahead: i64 = 1i64 << args[7].parse::<u32>().unwrap();
    let fleet: u8 = args[8].parse().unwrap();
    let label = args.get(9).cloned().unwrap_or_default();

    let mut s = build(n, if fleet == 1 { 0xC0FFEE } else { 42 });
    if fleet == 1 {
        // concentration: every body on one ring at R/30 (the co-orbital case)
        for (i, b) in s.bodies.iter_mut().enumerate() {
            let a = 2.0 * std::f64::consts::PI * (i as f64 / n as f64);
            b.px = (R_TICKS / 30.0) * a.cos();
            b.py = (R_TICKS / 30.0) * a.sin();
        }
    }
    let dt_frame = (rtf / FPS * TICKS_PER_S) as i64; // game ticks per frame
    let dpl = beta * dt_frame as f64; // player displacement per frame (c = 1)
    let mut now: i64 = 0;
    let mut px = -2.0 * R_TICKS;
    let mut py = 0.0f64;
    // prime: initial requeue so the heap is full (Universe::rekey at line 423)
    for e in 0..n {
        let dl = deadline(&s.bodies[e], px, py);
        s.bodies[e].dl = dl;
        s.bodies[e].hi = dl;
        s.q.set(e, Some(dl));
        // V4: stash each entity in its event-time bucket
        let idx = (s.bodies[e].t / s.wheel_q) as usize;
        if idx >= s.wheel.len() {
            s.wheel.resize(idx + 1, Vec::new());
        }
        s.wheel[idx].push(e as u32);
    }
    let mut tot_ns: Vec<f64> = Vec::new();
    let (mut s_rekey, mut s_drain, mut s_defreq, mut s_resolve, mut s_sets, mut s_peeks, mut s_sqrt, mut s_events, mut s_parked) =
        (0u64, 0u64, 0u64, 0u64, 0u64, 0u64, 0u64, 0u64, 0u64);
    // prime: initial requeue so the heap is full (Universe::rekey at line 423)
    for e in 0..n {
        let dl = deadline(&s.bodies[e], px, py);
        s.bodies[e].dl = dl;
        s.bodies[e].hi = dl;
        s.q.set(e, Some(dl));
    }
    for f in 0..frames {
        let target = now + dt_frame;
        let t0 = Instant::now();
        let st = run_frame(&mut s, variant, now, target, dpl, px, py, skin, lookahead, false);
        let el = t0.elapsed().as_nanos() as f64;
        if f >= 5 {
            tot_ns.push(el);
            s_rekey += st.rekey_ns;
            s_drain += st.drain_ns;
            s_defreq += st.defreq_ns;
            s_resolve += st.resolve_ns;
            s_sets += st.sets;
            s_peeks += st.peeks;
            s_sqrt += st.sqrt;
            s_events += st.events;
            s_parked += st.deferred_out;
        }
        now = target;
        px += dpl; // player crosses at beta
        let _ = py;
    }
    tot_ns.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let p = |q: f64| tot_ns[((tot_ns.len() as f64 - 1.0) * q) as usize];
    let nf = (tot_ns.len() as u64).max(1);
    // final state checksum: settle to the same target with unlimited budget
    let mut sum_t: i128 = 0;
    {
        let target = now;
        loop {
            let st = run_frame(&mut s, variant, now, target, 0.0, px, py, skin, lookahead, true);
            if st.events == 0 {
                break;
            }
        }
        for b in &s.bodies {
            sum_t += b.t as i128;
        }
    }
    println!(
        "{label}\tn={n}\tv={variant}\tbeta={beta}\trtf={rtf}\tfleet={fleet}\tp50_ns={:.0}\tp99_ns={:.0}\trekey_ns/fr={:.0}\tdrain_ns/fr={:.0}\tdefreq_ns/fr={:.0}\tresolve_ns/fr={:.0}\tsets/fr={:.0}\tpeeks/fr={:.0}\tsqrt/fr={:.0}\tevents/fr={}\tparked/fr={:.0}\tsum_t={sum_t}",
        p(0.5), p(0.99),
        s_rekey as f64 / nf as f64, s_drain as f64 / nf as f64, s_defreq as f64 / nf as f64,
        s_resolve as f64 / nf as f64, s_sets as f64 / nf as f64, s_peeks as f64 / nf as f64,
        s_sqrt as f64 / nf as f64, s_events / nf, s_parked as f64 / nf as f64
    );
}
