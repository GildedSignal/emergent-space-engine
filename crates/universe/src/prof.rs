//! Stage timers for the frame's cost (cargo feature `prof`). Off, every call is empty: the engine is what it was.
//! On, each stage keeps wall nanoseconds and calls in thread-local counters, taken (and reset) by [`take`].
//! Stages nest (a kick's rebind holds the fit), so a stage's share is read against its parent, not against the sum.

pub const REKEY: usize = 0;
pub const ROOT: usize = 1;
pub const APPLY: usize = 2;
pub const REQUEUE: usize = 3;
pub const PROCESS: usize = 4;
/// `bind_surface`: the exact fit of a tube to a state (a kick's, a hand-out's), the dearest thing an item does.
pub const FIT: usize = 5;
pub const TAKE_DUE: usize = 6;
pub const PRUNE: usize = 7;
/// The cheap half of the player's scan (who is there to be read), taken on the frame's critical path.
pub const ENCOUNTERS: usize = 8;
/// The held scans answered (in idle time, or at a settle or a digest).
pub const SCANS: usize = 9;
pub const P_KICK: usize = 10;
pub const P_KICK_CLOCK: usize = 11;
pub const P_KICK_SUB: usize = 12;
pub const P_BOUNDARY: usize = 13;
pub const P_OPEN: usize = 14;
pub const P_CRASH: usize = 15;
pub const P_DECIDE: usize = 16;
pub const F_RUN: usize = 17;
pub const F_ADV: usize = 18;
pub const HANDOUT: usize = 19;
pub const H_PULL: usize = 20;
pub const H_BIND: usize = 21;
pub const H_REPLAN: usize = 22;
/// The second `bind_in` of `bind_surface`: the word was too small for the new tube and the state is bound again, coarser.
pub const FIT2: usize = 23;
pub const N: usize = 24;

pub const NAMES: [&str; N] = [
    "rekey (all deadlines)",
    "  position walk (root_state_raw)",
    "apply (whole)",
    "requeue",
    "process (whole)",
    "  fit: bind_surface (kicks, hand-outs)",
    "take_due",
    "prune",
    "encounters: capture (cheap half)",
    "encounters: held scans answered",
    "item: kick (Wisdom-Holman)",
    "item: kick (clock)",
    "item: kick at a changeover level",
    "item: boundary",
    "item: open",
    "item: crash",
    "decision (player input)",
    "fleet: battle run_to",
    "fleet: advance (whole item)",
    "hand-out (a member made a body)",
    "  hand-out: pull planets and moons",
    "  hand-out: bind (the member as a tube)",
    "  hand-out: first plan (replan)",
    "  fit again: the coarser word (bind_surface)",
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
