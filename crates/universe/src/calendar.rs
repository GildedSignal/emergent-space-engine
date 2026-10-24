//! Who is due: the schedule's structures, with no slot reserved for every body (the calendar job, 24 October).
//!
//! **The ships are their own calendar.** A ship's record carries its next item's tick (each item plans the next: the causal
//! chain), so the schedule only has to find the ships a frame's target reaches. They are filed by **class**, a window of
//! `2^shift` ticks on a ring of them; a class's cursor ([`Wheel`]'s `heads`) is the first ship of a chain threaded through the
//! ships themselves (`link`, 4 bytes a ship), and a ship is filed in the class its own next tick puts it in. It moves only when it
//! is resolved (its tick moves, and it is filed again). Opening a class (the target reaches its window) puts its ships in tick
//! order in a small heap (`front`), and a ship is handed out when the target reaches its tick. A frame's work is the classes it
//! opens and the ships it hands out: nothing is walked for a ship that is not due.
//!
//! **What is explicit** (the hot set): the ships handed out and not yet resolved, the front, the deadline queue of what a frame
//! resolves (the planets, the moons, the player, the fleets and the due ships), and the bodies whose history can be shortened.
//! Each is a heap of the entries it holds, never a slot a body.
//!
//! **Why the class is not derived from the id** (the id-derived calendar, zero bytes a body: every ship of a class on one grid
//! `phase(id) + n·step`): a root ship's step is the time transform's `Δs·f'(U_P + c)` in ticks, carried (crate::ext), and it
//! moves at every kick: on the ladder's plane every root ship's kick after its first plans another step (0.01-6% of it, the
//! median about 0.3%), and a step or two later its kicks are hundreds of frames (at rtf 100) off the grid of its first
//! (`examples/grid.rs`).
//! The class a ship is in is a function of its state, not of its id, so the order of the ships has to be held, and the link is
//! that order's 32 bits a ship. A grid per class needs the law to hold the step in ticks (the integrator's choice).
//!
//! Nothing here reaches an outcome: the queue only schedules (crate::universe).
use crate::num::Tick;
use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashMap};
use std::hash::{BuildHasherDefault, Hasher};
use std::mem::size_of;

/// The last ship of a class's chain.
const END: u32 = u32::MAX - 2;
/// A ship in the front (its class is open, its tick not reached).
const FRONT: u32 = u32::MAX - 1;
/// Not in the calendar (handed out, never filed, or dead).
const FREE: u32 = u32::MAX;

/// A min-heap of `(tick, id)`, the smallest first.
pub type Ticks = BinaryHeap<Reverse<(Tick, u32)>>;

/// The bytes a heap holds (its capacity).
pub fn heap_bytes(h: &Ticks) -> usize {
    h.capacity() * size_of::<Reverse<(Tick, u32)>>()
}

/// The ships' calendar: classes by due window, each a chain threaded through the ships, and the front of the open ones.
pub struct Wheel {
    /// A class is `2^shift` ticks.
    shift: u32,
    /// The ring's size, less one (a power of two, less one).
    mask: i64,
    /// Each class's cursor: the first ship of its chain ([`END`]: none).
    heads: Vec<u32>,
    /// Each ship's next ship in its class's chain, or [`FRONT`] or [`FREE`].
    link: Vec<u32>,
    /// The ships of the open classes whose tick the target has not reached, in tick order.
    front: Ticks,
    /// Every tick up to this one is handed out: a ship in a chain or in the front has a later tick.
    drained: Tick,
    /// The first class not opened yet (an absolute index, `tick >> shift`).
    open: i64,
    /// Ships in chains.
    chained: usize,
}

impl Wheel {
    /// A calendar for ids below `slots`, every tick up to `drained` handed out, classes of `2^shift` ticks on a ring of `2^ring_log2`.
    pub fn new(slots: usize, drained: Tick, shift: u32, ring_log2: u32) -> Self {
        let r = 1usize << ring_log2;
        Self { shift, mask: r as i64 - 1, heads: vec![END; r], link: vec![FREE; slots], front: BinaryHeap::new(), drained, open: drained >> shift, chained: 0 }
    }

    /// The class width (log2 ticks) that puts a ring of `2^ring_log2` classes over `span` ticks (at least 1).
    pub fn shift_for(span: Tick, ring_log2: u32) -> u32 {
        let span = span.max(1) as u64;
        (64 - span.leading_zeros()).saturating_sub(ring_log2)
    }

    pub fn drained(&self) -> Tick {
        self.drained
    }

    /// Whether ship `i` is filed (in a chain or the front).
    pub fn holds(&self, i: usize) -> bool {
        self.link.get(i).is_some_and(|&l| l != FREE)
    }

    /// Ships filed (in chains and in the front).
    pub fn len(&self) -> usize {
        self.chained + self.front.len()
    }
    pub fn is_empty(&self) -> bool {
        self.len() == 0
    }
    /// Ships in the front now.
    pub fn front_len(&self) -> usize {
        self.front.len()
    }

    /// File ship `i`, whose next tick is `t` (after [`Wheel::drained`]). A ship already filed stays where it is: its tick has
    /// not moved (a ship is filed again only after it is resolved, and it is resolved only after it is handed out).
    pub fn file(&mut self, i: usize, t: Tick) {
        debug_assert!(t > self.drained);
        if self.link[i] != FREE {
            return;
        }
        let k = t >> self.shift;
        if k < self.open {
            self.front.push(Reverse((t, i as u32)));
            self.link[i] = FRONT;
        } else {
            self.chain(i as u32, k);
        }
    }

    fn chain(&mut self, i: u32, k: i64) {
        let slot = (k & self.mask) as usize;
        self.link[i as usize] = self.heads[slot];
        self.heads[slot] = i;
        self.chained += 1;
    }

    /// Hand out every filed ship whose tick is at or before `to` (each once, into `out`, in tick order), reading a ship's tick from
    /// its own record (`next`; none: it died and leaves the calendar). The classes `to` reaches are opened: their ships go to the
    /// front, or back into the chain of a later lap of the ring.
    pub fn drain(&mut self, to: Tick, next: impl Fn(usize) -> Option<Tick>, out: &mut Vec<usize>) {
        if to <= self.drained {
            return;
        }
        let last = to >> self.shift;
        if last - self.open >= self.heads.len() as i64 {
            // A jump past a whole lap of the ring: open every class at once.
            let mut ships = Vec::with_capacity(self.chained);
            for slot in 0..self.heads.len() {
                let mut c = std::mem::replace(&mut self.heads[slot], END);
                while c != END {
                    ships.push(c);
                    c = self.link[c as usize];
                }
            }
            self.chained = 0;
            self.open = last + 1;
            for c in ships {
                self.place(c, &next);
            }
        } else {
            while self.open <= last {
                let slot = (self.open & self.mask) as usize;
                let mut c = std::mem::replace(&mut self.heads[slot], END);
                self.open += 1;
                while c != END {
                    let following = self.link[c as usize];
                    self.chained -= 1;
                    self.place(c, &next);
                    c = following;
                }
            }
        }
        while let Some(&Reverse((t, c))) = self.front.peek() {
            if t > to {
                break;
            }
            self.front.pop();
            self.link[c as usize] = FREE;
            out.push(c as usize);
        }
        self.drained = to;
    }

    /// A ship taken out of a chain: to the front if its class is open, else into its class's chain (a later lap).
    fn place(&mut self, c: u32, next: &impl Fn(usize) -> Option<Tick>) {
        match next(c as usize) {
            None => self.link[c as usize] = FREE,
            Some(t) => {
                let k = t >> self.shift;
                if k < self.open {
                    self.front.push(Reverse((t, c)));
                    self.link[c as usize] = FRONT;
                } else {
                    self.chain(c, k);
                }
            }
        }
    }

    /// Bytes held: the links, the cursors and the front.
    pub fn bytes(&self) -> usize {
        self.link.capacity() * size_of::<u32>() + self.heads.capacity() * size_of::<u32>() + heap_bytes(&self.front)
    }
}

/// A hasher for small integer ids (a multiply: the ids are dense, a map holds only the queued few).
#[derive(Default)]
pub struct IdHasher(u64);
impl Hasher for IdHasher {
    fn finish(&self) -> u64 {
        self.0
    }
    fn write(&mut self, bytes: &[u8]) {
        for &b in bytes {
            self.0 = (self.0.rotate_left(8) ^ b as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15);
        }
    }
    fn write_u32(&mut self, x: u32) {
        self.0 = (x as u64 ^ 0x5851_F42D_4C95_7F2D).wrapping_mul(0x9E37_79B9_7F4A_7C15);
    }
}

/// The deadline queue: what a frame may resolve, in the order `(key, id)` (the light-delayed deadline, then the id), holding only
/// what is queued. A heap with lazy removal: an entry is current while the map gives its entity that key.
#[derive(Default)]
pub struct Queue {
    heap: Ticks,
    key: HashMap<u32, Tick, BuildHasherDefault<IdHasher>>,
}

impl Queue {
    /// Queue `e` at `key`, or take it out (None).
    pub fn set(&mut self, e: usize, key: Option<Tick>) {
        let id = e as u32;
        match key {
            Some(k) => {
                if self.key.insert(id, k) != Some(k) {
                    self.heap.push(Reverse((k, id)));
                }
            }
            None => {
                self.key.remove(&id);
            }
        }
        if self.heap.len() > 2 * self.key.len() + 64 {
            self.heap = self.key.iter().map(|(&e, &k)| Reverse((k, e))).collect();
        }
    }

    /// The first `(key, entity)`.
    pub fn peek(&mut self) -> Option<(Tick, usize)> {
        while let Some(&Reverse((k, e))) = self.heap.peek() {
            if self.key.get(&e) == Some(&k) {
                return Some((k, e as usize));
            }
            self.heap.pop();
        }
        None
    }

    pub fn len(&self) -> usize {
        self.key.len()
    }
    pub fn is_empty(&self) -> bool {
        self.key.is_empty()
    }

    /// Bytes held: the heap and the map (a bucket holds an entry and a control byte).
    pub fn bytes(&self) -> usize {
        heap_bytes(&self.heap) + self.key.capacity() * (size_of::<(u32, Tick)>() + 1)
    }
}

/// The bodies whose history holds more than one retired binding, by the earliest tick it could be shortened: a heap of those
/// bodies and one bit a body (whether it has an entry).
#[derive(Default)]
pub struct Prunable {
    heap: Ticks,
    marks: Vec<u64>,
}

impl Prunable {
    pub fn new(slots: usize) -> Self {
        Self { heap: BinaryHeap::new(), marks: vec![0; slots.div_ceil(64)] }
    }

    fn marked(&self, i: usize) -> bool {
        self.marks.get(i / 64).is_some_and(|w| w & (1 << (i % 64)) != 0)
    }
    fn mark(&mut self, i: usize, on: bool) {
        if self.marks.len() <= i / 64 {
            self.marks.resize(i / 64 + 1, 0);
        }
        if on {
            self.marks[i / 64] |= 1 << (i % 64);
        } else {
            self.marks[i / 64] &= !(1 << (i % 64));
        }
    }

    /// Key body `i` at `at`, or take it out (None). A body already keyed keeps its key: it is visited then, and keyed again.
    pub fn set(&mut self, i: usize, at: Option<Tick>) {
        match at {
            Some(at) => {
                if !self.marked(i) {
                    self.mark(i, true);
                    self.heap.push(Reverse((at, i as u32)));
                }
            }
            None => self.mark(i, false),
        }
    }

    /// The next body keyed at or before `now`, taken out.
    pub fn pop_due(&mut self, now: Tick) -> Option<usize> {
        while let Some(&Reverse((at, i))) = self.heap.peek() {
            if at > now {
                return None;
            }
            self.heap.pop();
            if self.marked(i as usize) {
                self.mark(i as usize, false);
                return Some(i as usize);
            }
        }
        None
    }

    pub fn bytes(&self) -> usize {
        heap_bytes(&self.heap) + self.marks.capacity() * size_of::<u64>()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// The wheel hands out exactly the ships whose tick a target reaches, each once, in tick order, across laps of the ring and
    /// jumps past it, against a brute-force scan of the same ticks.
    #[test]
    fn the_wheel_hands_out_what_is_due_and_nothing_else() {
        let n = 2_000usize;
        let mut z = 0x1234_5678_9ABC_DEF0u64;
        let mut rnd = move || {
            z ^= z << 13;
            z ^= z >> 7;
            z ^= z << 17;
            z
        };
        let mut tick: Vec<Option<Tick>> = (0..n).map(|_| Some((rnd() % 5_000_000) as Tick + 1)).collect();
        let mut w = Wheel::new(n, 0, 10, 6);
        for (i, t) in tick.iter().enumerate() {
            w.file(i, t.unwrap());
        }
        let mut to = 0;
        for step in 0..400 {
            // Mostly short targets; now and then a jump past the whole ring (64 classes of 1,024 ticks).
            to += if step % 37 == 0 { 200_000 } else { (rnd() % 30_000) as Tick };
            let mut out = Vec::new();
            {
                let tk = tick.clone();
                w.drain(to, |i| tk[i], &mut out);
            }
            let mut want: Vec<usize> = (0..n).filter(|&i| tick[i].is_some_and(|t| t <= to)).collect();
            let mut got = out.clone();
            got.sort();
            want.sort();
            assert_eq!(got, want, "at {to}");
            let ticks: Vec<Tick> = out.iter().map(|&i| tick[i].unwrap()).collect();
            assert!(ticks.windows(2).all(|p| p[0] <= p[1]), "in tick order");
            // Each handed-out ship is resolved: a later tick (or it dies), and filed again.
            for i in out {
                if rnd() % 50 == 0 {
                    tick[i] = None;
                } else {
                    let t = to + 1 + (rnd() % 3_000_000) as Tick;
                    tick[i] = Some(t);
                    w.file(i, t);
                }
            }
            assert_eq!(w.len(), tick.iter().filter(|t| t.is_some_and(|t| t > to)).count());
        }
    }

    #[test]
    fn the_queue_orders_by_key_then_id_and_forgets_what_is_taken_out() {
        let mut q = Queue::default();
        q.set(5, Some(10));
        q.set(3, Some(10));
        q.set(7, Some(4));
        q.set(7, Some(12));
        assert_eq!(q.peek(), Some((10, 3)));
        q.set(3, None);
        assert_eq!(q.peek(), Some((10, 5)));
        q.set(5, None);
        assert_eq!(q.peek(), Some((12, 7)));
        q.set(3, Some(10));
        assert_eq!(q.peek(), Some((10, 3)));
        for k in 0..1_000 {
            q.set(9, Some(k));
        }
        assert_eq!(q.len(), 3);
        assert!(q.heap.len() <= 2 * 3 + 65);
        assert_eq!(q.peek(), Some((10, 3)));
    }
}
