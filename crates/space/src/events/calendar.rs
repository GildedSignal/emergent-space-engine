//! Lifted from lattice-event Calendar; same 4-ary indexed heap and slot tie order.
use crate::{orbit::Scalar, Error, Result};
const NONE: u32 = u32::MAX;
/// Indexed 4-ary heap of (time, body) with one slot per body: the calendar never holds
/// stale entries and never grows past n, so it is allocated once. Keys are inline and the
/// four children of a node share a cache line: re-predictions mostly move a slot later, and
/// that sift-down dominated the calendar's cost at a million bodies.
pub struct Calendar {
    heap: Vec<(Scalar, u32)>,
    pos: Vec<u32>,
}

const ARITY: usize = 4;

impl Calendar {
    pub fn new(n: usize) -> Self {
        Calendar {
            heap: Vec::with_capacity(n),
            pos: vec![NONE; n],
        }
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

    /// Set body i's slot; returns whether a live prediction was replaced.
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
}

impl Calendar {
    /// Times are in the root doll clock. None cancels a slot; scale is carried in the exponent.
    pub fn set(&mut self, slot: usize, time: Option<Scalar>) -> Result<bool> {
        if slot >= self.pos.len() || slot >= u32::MAX as usize {
            return Err(Error::Range);
        }
        Ok(self.set_unchecked(slot, time))
    }
    pub fn len(&self) -> usize {
        self.heap.len()
    }
    pub fn is_empty(&self) -> bool {
        self.heap.is_empty()
    }
}
