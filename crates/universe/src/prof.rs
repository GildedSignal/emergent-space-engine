//! Stage timers for the frame's cost (cargo feature `prof`). Off, every call is empty: the engine is what it was.
//! On, each stage keeps wall nanoseconds and calls in thread-local counters, taken (and reset) by [`take`].
//! Stages nest (a kick's rebind holds the fit), so a stage's share is read against its parent, not against the sum.

pub const REKEY: usize = 0;
pub const ROOT: usize = 1;
pub const APPLY: usize = 2;
pub const REQUEUE: usize = 3;
pub const PROCESS: usize = 4;
pub const K_READOUT: usize = 5;
pub const K_SOURCES: usize = 6;
pub const K_FIELD: usize = 7;
pub const K_QUANT: usize = 8;
pub const K_REBIND: usize = 9;
pub const R_FIT: usize = 10;
pub const R_TAU: usize = 11;
pub const R_REST: usize = 12;
pub const K_POST: usize = 13;
pub const B_FROM_STATE: usize = 14;
pub const B_DECODE: usize = 15;
pub const B_REST: usize = 16;
pub const TAKE_DUE: usize = 17;
pub const PRUNE: usize = 18;
pub const ENCOUNTERS: usize = 19;
pub const WALK: usize = 20;
pub const P_KICK: usize = 21;
pub const P_KICK_CLOCK: usize = 22;
pub const P_BOUNDARY: usize = 23;
pub const P_OPEN: usize = 24;
pub const P_CRASH: usize = 25;
pub const P_DECIDE: usize = 26;
pub const P_KICK_SUB: usize = 27;
pub const F_RUN: usize = 28;
pub const F_ADV: usize = 29;
pub const HANDOUT: usize = 30;
pub const H_PULL: usize = 31;
pub const H_BIND: usize = 32;
pub const H_REPLAN: usize = 33;
pub const N: usize = 34;

pub const NAMES: [&str; N] = [
    "rekey (all deadlines)",
    "  position walk (root_state_raw)",
    "apply (whole)",
    "requeue",
    "process (whole)",
    "  kick: readout",
    "  kick: sources",
    "  kick: field",
    "  kick: quantize",
    "  kick: rebind (whole)",
    "    rebind: bind() fit",
    "    rebind: proper-time reads",
    "    rebind: rest",
    "  kick: replan",
    "      bind: Rebinding::from_state",
    "      bind: decode",
    "      bind: rest (incl. decode)",
    "take_due",
    "prune",
    "encounters (player)",
    "deadline anchor walks",
    "item: kick (Wisdom-Holman)",
    "item: kick (clock)",
    "item: boundary",
    "item: open",
    "item: crash",
    "decision (player input)",
    "item: kick at a changeover level",
    "fleet: battle run_to",
    "fleet: advance (whole item)",
    "hand-out (a member made a body)",
    "  hand-out: pull planets and moons",
    "  hand-out: bind (the member as a tube)",
    "  hand-out: first plan (replan)",
];

#[cfg(feature = "prof")]
mod on {
    use super::N;
    use std::cell::RefCell;
    pub type T = std::time::Instant;
    thread_local! {
        static P: RefCell<([u64; N], [u64; N])> = const { RefCell::new(([0; N], [0; N])) };
    }
    #[inline(always)]
    pub fn t() -> T {
        std::time::Instant::now()
    }
    #[inline(always)]
    pub fn add(stage: usize, since: T) {
        let ns = since.elapsed().as_nanos() as u64;
        P.with(|p| {
            let mut p = p.borrow_mut();
            p.0[stage] += ns;
            p.1[stage] += 1;
        });
    }
    /// Count a call that took no time of its own (a walk skipped, say).
    #[inline(always)]
    pub fn count(stage: usize) {
        P.with(|p| p.borrow_mut().1[stage] += 1);
    }
    pub fn take() -> ([u64; N], [u64; N]) {
        P.with(|p| std::mem::replace(&mut *p.borrow_mut(), ([0; N], [0; N])))
    }
}

#[cfg(not(feature = "prof"))]
mod on {
    use super::N;
    pub type T = ();
    #[inline(always)]
    pub fn t() -> T {}
    #[inline(always)]
    pub fn add(_stage: usize, _since: T) {}
    #[inline(always)]
    pub fn count(_stage: usize) {}
    pub fn take() -> ([u64; N], [u64; N]) {
        ([0; N], [0; N])
    }
}

pub use on::{add, count, t, take, T};
pub const ENABLED: bool = cfg!(feature = "prof");
