//! H_live: the live distinguishing information (docs/plane.md, "Distinctions created per game-second").
//!
//! **Definition.** A body's exact state is held as a *compiled description* — its 16-byte tube indexing a
//! shared compiled trajectory (the catalogue) — plus, only because dynamics has taken the state off that
//! compiled geodesic, a tuple of integer words the description cannot hold. That tuple is the body's live
//! distinguishing stock, measured in bits ([`bits`]: a magnitude's length and its sign; zero is free):
//!
//! - the **remainder** the fit discarded at the last binding ([`Binding::residual`], four words) and the
//!   sub-quantum **turn** ([`Binding::turn`], two words);
//! - the **sigma-delta carries**: the velocity's ([`BodyRec::carry`]) and, for a clock-stepped body, the
//!   energy register's and the clock's (`pt_carry`, `dt_carry`);
//! - the **energy register** `p_t` itself ([`crate::ext`]);
//! - the impulse of the **kick ramp** a binding keeps between kicks ([`crate::bind::Kick::dv`]).
//!
//! Excluded, on purpose: the tube (the compiled form's per-body floor, 128 bits — reported beside the
//! stock, not in it); the plan, step, anchor, heading and proper time (fixed-width scheduling state and
//! derived accumulators, functions of the event history); the catalogue (generators *shared* by tubes);
//! and a fleet battle's in-frame member state (`crates/engine`'s, below this instrument today — the seam
//! `crates/shipmem` fills; a leaver's stock is counted from the tick the doll binds it).
//!
//! **The ledger.** Every change of the live stock is one event ([`Ledger::note`]), and the ledger closes
//! exactly: `created + spill − reabsorbed = H_live(end) − H_live(start)` (tested):
//! - **created** — bits an event applies to a body from outside it: the velocity quanta a kick or a burn's
//!   flush applies (counted in [`crate::step`] where the integers are), the changed bits of a decision
//!   word, and a leaver's birth stock;
//! - **reabsorbed** — live bits an event removes: an old remainder folded into the new tube by a rebind
//!   (`created + h_old − h_new > 0`), and a lost body's whole stock;
//! - **spill** — a re-encoding that grew the stock beyond the payload (`h_new − h_old − created > 0`):
//!   a fit's discard widening, a handoff's re-expression, a register's projection.
//!
//! Sub-quantum kicks that fire nothing are counted ([`Ledger::carried_kicks`]): their energy stays in the
//! bounded carry — reabsorption by construction. A frame's origin kicks are reported apart
//! ([`Ledger::frame_kick_bits`]): their bits land in the battle's state, not in any body's stock.
//!
//! Observation only: nothing here writes a record, and no digest reads it.
use crate::bind::Binding;
use crate::body::BodyRec;

/// The bits it costs to name an integer exactly: the length of its magnitude and its sign. Zero is free.
#[inline]
pub fn bits(n: i128) -> u64 {
    if n == 0 {
        0
    } else {
        n.unsigned_abs().ilog2() as u64 + 2
    }
}

/// A live distinguishing stock, decomposed (bits; the components are the module's definition).
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct Stock {
    /// The fit's remainder (four words) and the sub-quantum turn (two).
    pub remainder: u64,
    /// The sigma-delta carries: the velocity's, and a clock-stepped body's register and clock carries.
    pub carries: u64,
    /// The energy register `p_t` of a clock-stepped body.
    pub register: u64,
    /// The kick ramp's stored impulse.
    pub ramp: u64,
}

impl Stock {
    #[inline]
    pub fn total(&self) -> u64 {
        self.remainder + self.carries + self.register + self.ramp
    }
    #[inline]
    pub(crate) fn plus(self, o: Stock) -> Stock {
        Stock {
            remainder: self.remainder + o.remainder,
            carries: self.carries + o.carries,
            register: self.register + o.register,
            ramp: self.ramp + o.ramp,
        }
    }
}

/// One binding's distinguishing stock: its remainder, turn and kick ramp.
pub fn stock_of_binding(b: &Binding) -> Stock {
    let mut s = Stock::default();
    for c in 0..2 {
        s.remainder += bits(b.residual.position[c]) + bits(b.residual.velocity[c]);
    }
    s.remainder += bits(b.turn.a as i128) + bits(b.turn.b as i128);
    if b.kick.len != 0 {
        s.ramp += bits(b.kick.dv[0] as i128) + bits(b.kick.dv[1] as i128);
    }
    s
}

/// One body's distinguishing stock: the binding's plus the carries and the energy register.
pub fn stock_of_rec(r: &BodyRec) -> Stock {
    let mut s = stock_of_binding(&r.b);
    s.carries += bits(r.carry[0] as i128) + bits(r.carry[1] as i128);
    if let Some(e) = r.ext {
        s.register += bits(e.pt);
        s.carries += bits(e.pt_carry as i128) + bits(e.dt_carry as i128);
    }
    s
}

/// The ledger of distinctions created and reabsorbed. Counters only; it observes and never writes.
#[derive(Clone, Copy, Debug, Default)]
pub struct Ledger {
    /// Bits events applied to bodies from outside them (kick impulses, decision words, births).
    pub created: u64,
    /// Live bits events removed (remainders folded into tubes, lost bodies' stock).
    pub reabsorbed: u64,
    /// Bits of re-encoding that grew the stock beyond the payload (a fit's discard widening, handoffs).
    pub spill: u64,
    /// Bindings rebound (a kick, a burn's flush, a handoff): the stock's encoding was replaced.
    pub rebinds: u64,
    /// Sub-quantum kicks that fired nothing: their energy stays in the bounded carry.
    pub carried_kicks: u64,
    /// Decisions taken.
    pub decisions: u64,
    /// Leavers bound into the doll (births).
    pub born: u64,
    /// Bodies lost (their stock left the live set).
    pub lost: u64,
    /// A fleet frame's origin kicks, and their bits (they land in the battle's state, not a body's).
    pub frame_kicks: u64,
    pub frame_kick_bits: u64,
}

impl Ledger {
    /// One resolved item of an existing body: the stock it replaced (`h0`) and left (`h1`), whether it
    /// rebound, and the payload bits it applied. Keeps `created + spill − reabsorbed = ΔH_live` exactly.
    pub fn note(&mut self, was_alive: bool, is_alive: bool, rebound: bool, payload: u64, h0: u64, h1: u64) {
        if !was_alive {
            return; // a lost body's record no longer changes
        }
        self.rebinds += rebound as u64;
        if !is_alive {
            self.reabsorbed += h0; // the whole stock leaves the live set
            self.lost += 1;
            return;
        }
        self.created += payload;
        let delta = h1 as i64 - h0 as i64;
        if delta >= payload as i64 {
            self.spill += (delta - payload as i64) as u64;
        } else {
            self.reabsorbed += (payload as i64 - delta) as u64;
        }
    }

    /// A sub-quantum kick that fired nothing.
    pub fn note_carried_kick(&mut self) {
        self.carried_kicks += 1;
    }

    /// A decision word: the bits that changed.
    pub fn note_decision(&mut self, changed: u32) {
        self.decisions += 1;
        self.created += changed as u64;
    }

    /// A leaver bound into the doll, arriving with stock `h` (the frame's copy is not counted).
    pub fn note_birth(&mut self, h: u64) {
        self.born += 1;
        self.created += h;
    }

    /// A fleet frame's origin kicks (reported apart: their bits land in the battle, not a body stock).
    pub fn note_frame_kicks(&mut self, kicks: u64, bits: u64) {
        self.frame_kicks += kicks;
        self.frame_kick_bits += bits;
    }
}

/// The universe's H_live at one moment: the live stock, the history the view still holds, and context.
#[derive(Clone, Copy, Debug, Default)]
pub struct Snapshot {
    pub live: Stock,
    /// The same stock over the retained history segments: dead-but-stored distinctions the view costs.
    pub history: u64,
    pub alive: usize,
    pub bodies: usize,
    /// Live compiled trajectories: the generators the tubes share (context, not per-body stock).
    pub catalogue: usize,
    /// The tube form's per-body floor, in bits (128 per body, live or not): the compiled description.
    pub tube_floor_bits: u64,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn bits_name_an_integer_exactly() {
        assert_eq!(bits(0), 0);
        assert_eq!(bits(1), 2); // one magnitude bit and the sign
        assert_eq!(bits(-1), 2);
        assert_eq!(bits(2), 3);
        assert_eq!(bits(-3), 3);
        assert_eq!(bits(i64::MAX as i128), 65);
        assert_eq!(bits(i64::MIN as i128), 65);
        assert_eq!(bits(i128::MAX), 128);
    }

    #[test]
    fn the_ledger_closes_over_a_scripted_flight() {
        use crate::scenario::plane;
        let (seed, members) = (7u64, 12u64);
        let mut p = plane(crate::Config::default(), seed, crate::fleet::Order::Sparse, 1, members).expect("the plane");
        // The ledger and the stock are read at the same moments; both count from `start`, which itself
        // derives the clock registers (spill), so the compared quantities are their deltas.
        let (before, l0) = (p.u.h_live(), p.u.h);
        // A scripted flight: the benchmark's canonical decisions, then a settle to a cut.
        let cut = 1 << 24;
        for k in 0..8 {
            let t = cut / 8 * k + 1000;
            let word = [1u8, 9, 2, 4, 0, 1 | 4, 2, 0][k as usize];
            p.u.schedule(t, word).expect("schedule");
        }
        p.u.settle(cut);
        let (after, h) = (p.u.h_live(), p.u.h);
        let ledger_delta = (h.created + h.spill).saturating_sub(h.reabsorbed) as i64 - (l0.created + l0.spill).saturating_sub(l0.reabsorbed) as i64;
        let stock_delta = after.live.total() as i64 - before.live.total() as i64;
        assert_eq!(
            ledger_delta, stock_delta,
            "Δ(created + spill − reabsorbed) must equal ΔH_live: ledger {} vs stock {} (created {}, spill {}, reabsorbed {}, born {}, lost {})",
            ledger_delta, stock_delta, h.created, h.spill, h.reabsorbed, h.born, h.lost
        );
        // The run actually distinguished things: kicks fired and decisions were taken.
        assert!(h.rebinds > l0.rebinds && h.decisions == l0.decisions + 8, "{:?}", h);
        assert!(after.live.total() > 0, "a kicked universe holds live distinctions");
    }

    #[test]
    fn a_body_made_from_its_orbit_holds_no_live_distinction() {
        use crate::{Config, Kind, OrbitSpec, Universe};
        use emergent_space::orbit::Scalar;
        // Before the universe starts, a body made from its orbit is exactly its tube: no remainder, no
        // carry, no register. The clock's energy register appears when the body is planned (derived from
        // the exact state, held at exact width): that is a live distinction from then on.
        let mut u = Universe::new(Scalar::power_of_two(10), Config::default());
        let spec = OrbitSpec { doll: 0, periapsis: Scalar::integer(1 << 20), e_q48: 0, clockwise: false, angle: 0, phase: 0 };
        let i = u.add_body(Kind::Ship, spec, Scalar::ZERO).expect("body");
        assert_eq!(stock_of_rec(&u.rec(i)).total(), 0);
    }
}
