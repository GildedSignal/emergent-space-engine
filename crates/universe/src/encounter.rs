//! Encounters sit behind one seam: [`Encounters`] answers "which pairs come close within this
//! interval". Today the answer is an exact check for the player's neighbourhood
//! ([`PlayerNeighbourhood`]); later the Binet cone of `crates/encounters` (orbits cross only inside a
//! 2+1 light cone, found with no work per orbit) implements the same trait, with no rewiring.
//!
//! The predicate is the lattice law's own bin predicate (`emergent_lattice::law::hit`): the pair's
//! linear relative motion over the interval comes within `reach`, exact in integers. A
//! *contact* is within the two bodies' radii; an *encounter* is within `2^ENCOUNTER_LOG2` of them
//! (the neighbourhood the player's own instruments would call close).
use crate::bind::Binding;
use crate::ctx::Ctx;
use crate::num::{sub2, time_of, to_f64, Res, Tick, V2};
use crate::radial::Window;
use emergent_lattice::law::hit;
use emergent_space::orbit::Scalar;
use std::sync::{Arc, Mutex, OnceLock};

pub const ENCOUNTER_LOG2: i32 = 10;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Encounter {
    pub a: usize,
    pub b: usize,
    pub t: Tick,
    /// Within the two radii (a contact), not only within the neighbourhood.
    pub contact: bool,
}

pub trait Encounters: Send + Sync {
    /// The pairs `(body, other)` that come close during `[t, t + interval]`, given every body's tube.
    fn find(&self, ctx: &Ctx, body: usize, t: Tick, interval: Tick) -> Vec<Encounter>;

    /// `find` in two halves: take now what the answer reads (the cheap half), and answer whenever the allocator has time.
    /// The universe answers a held scan in idle time, in the order the scans were taken, and always before it is asked for a
    /// digest or a count, so the encounters (and what is hashed of them) are the same as if each had been found at once.
    /// `None` (the default) means the finder does not split: the universe calls `find` where it is.
    fn capture(&self, _ctx: &Ctx, _body: usize, _t: Tick, _interval: Tick) -> Option<Arc<dyn Held>> {
        None
    }
}

/// A scan taken and not yet answered: everything its answer reads is held in it, so the answer is the same whenever it
/// is given (the bodies' histories may have moved on, been pruned, or the bodies died since).
pub trait Held: Send + Sync {
    fn answer(&self) -> Vec<Encounter>;
}

/// The exact check for the player's neighbourhood: every body in the player's doll, tested against the player over the
/// interval.
///
/// **Two things are not done on the frame's critical path, and one is not done twice.** The answer reads no live state, only
/// what the scan captured, and nothing the view shows reads it: it is found in idle time, in order ([`Encounters::capture`]).
/// And the finder reads the player at the tick of its binding, so the scan after a boundary or an opening (which rebind
/// nothing) is the scan after the kick before it again whenever nothing it reads has changed (the same player binding,
/// tick and interval, the same bodies in the same bindings): its encounters are logged again (that is the digest's
/// history), but their answer is found once.
///
/// **The predicate is exact** (13 October; it wrapped its `i128` products before, on 16–58% of the pairs a burn tests, and
/// answered garbage there: the probe `examples/hit_wrap.rs`, retired after 53165a9c). A cheap exact bound in front of it would now skip 70–86% of the pairs
/// (commit `ce694696` holds one, with its control); it is not carried, since the scans are already off the critical path.
pub struct PlayerNeighbourhood {
    /// The last scan taken.
    last: Mutex<Option<Arc<Scan>>>,
    /// The test's planted fault: reuse the last scan whatever the tick, the interval and the bodies.
    sloppy: bool,
}

/// Everything one scan reads.
struct Scan {
    body: usize,
    t: Tick,
    interval: Tick,
    me: Binding,
    /// Every body that passed the cheap tests (alive, born, in the player's doll, with a reach), with its binding.
    candidates: Vec<(usize, Binding, Scalar)>,
    found: OnceLock<Vec<Encounter>>,
}

impl Scan {
    fn same_inputs(&self, body: usize, t: Tick, interval: Tick, me: &Binding, candidates: &[(usize, Binding, Scalar)]) -> bool {
        self.body == body
            && self.t == t
            && self.interval == interval
            && same(&self.me, me)
            && self.candidates.len() == candidates.len()
            && self.candidates.iter().zip(candidates).all(|(a, b)| a.0 == b.0 && a.2 == b.2 && same(&a.1, &b.1))
    }
}

/// The same binding, in every part a reading of it depends on (the compiled trajectory by identity: an entry is
/// immutable, and the scan holds a reference, so its address cannot be another's).
fn same(a: &Binding, b: &Binding) -> bool {
    Arc::ptr_eq(&a.entry, &b.entry)
        && a.tube == b.tube
        && a.residual == b.residual
        && a.turn == b.turn
        && a.units == b.units
        && a.clock_exp == b.clock_exp
        && a.event_time == b.event_time
        && a.doll == b.doll
}

impl Default for PlayerNeighbourhood {
    fn default() -> Self {
        Self { last: Mutex::new(None), sloppy: false }
    }
}

impl PlayerNeighbourhood {
    /// A planted fault for the tests' control: a finder that reuses the last scan whatever the tick, the interval and the
    /// bodies. It must give another digest.
    #[doc(hidden)]
    pub fn planted_sloppy_reuse() -> Self {
        Self { sloppy: true, ..Self::default() }
    }
}

fn integers(a: V2, q_exp: i32) -> Res<[i128; 2]> {
    Ok([a[0].fixed(-q_exp)?, a[1].fixed(-q_exp)?])
}

impl Held for Scan {
    fn answer(&self) -> Vec<Encounter> {
        self.found.get_or_init(|| self.compute()).clone()
    }
}

impl Scan {
    /// The expensive half: read the player and each candidate at `t` and apply the predicate.
    fn compute(&self) -> Vec<Encounter> {
        let mut out = Vec::new();
        let (t, body) = (self.t, self.body);
        let Ok((x, v)) = self.me.cartesian(t) else { return out };
        let Ok(h) = time_of(self.interval, self.me.clock_exp) else { return out };
        for (j, other, reach) in &self.candidates {
            let found = (|| -> Res<Option<bool>> {
                let (xj, vj) = other.cartesian(t)?;
                let d = sub2(xj, x)?;
                let w = [vj[0].sub(v[0])?.mul(h)?, vj[1].sub(v[1])?.mul(h)?];
                // Integers in units of reach/2^20: the lattice predicate is exact on i128 (until it wraps: see above).
                let q_exp = reach.exponent() as i32 - 20;
                let (di, wi) = (integers(d, q_exp)?, integers(w, q_exp)?);
                let near = reach.scale(ENCOUNTER_LOG2)?.fixed(-q_exp)?;
                if !hit(di, wi, near) {
                    return Ok(None);
                }
                Ok(Some(hit(di, wi, reach.fixed(-q_exp)?)))
            })();
            if let Ok(Some(contact)) = found {
                out.push(Encounter { a: body, b: *j, t, contact });
            }
        }
        out
    }
}

impl Encounters for PlayerNeighbourhood {
    fn find(&self, ctx: &Ctx, body: usize, t: Tick, interval: Tick) -> Vec<Encounter> {
        self.capture(ctx, body, t, interval).map_or_else(Vec::new, |held| held.answer())
    }

    fn capture(&self, ctx: &Ctx, body: usize, t: Tick, interval: Tick) -> Option<Arc<dyn Held>> {
        let me = ctx.bodies.binding_at(body, t)?;
        // The cheap tests, in body order: who is there to be read.
        // Only the bodies whose radial range can meet the player's window are read (`crate::radial`: the apsidal filter, a certificate
        // that the rest cannot be a hit); when that is most of the doll, every body is read, as it always was.
        let near = (|| -> Option<Vec<usize>> {
            let (x, v) = me.cartesian(t).ok()?;
            let h = time_of(interval, me.clock_exp).ok()?;
            let norm = |a: V2| to_f64(a[0]).hypot(to_f64(a[1]));
            let w = Window { r: norm(x), v: norm(v), reach_p: to_f64(ctx.info[body].radius), near_log2: ENCOUNTER_LOG2, h: to_f64(h) };
            ctx.radial.candidates(me.doll, &w)
        })();
        let mut candidates = Vec::new();
        for j in near.map_or_else(|| Box::new(0..ctx.bodies.len()) as Box<dyn Iterator<Item = usize>>, |ids| Box::new(ids.into_iter())) {
            // A member handed out of a frame is there for the ticks after its hand-out.
            if j == body || !ctx.bodies.alive(j) || t <= ctx.info[j].born {
                continue;
            }
            let Some(other) = ctx.bodies.binding_at(j, t) else { continue };
            if other.doll != me.doll {
                continue;
            }
            let reach = ctx.info[body].radius.add(ctx.info[j].radius).unwrap_or(Scalar::ZERO);
            if reach.is_zero() {
                continue;
            }
            candidates.push((j, other, reach));
        }
        let mut last = self.last.lock().expect("the finder's last scan");
        let reusable = |l: &&Arc<Scan>| if self.sloppy { l.body == body } else { l.same_inputs(body, t, interval, &me, &candidates) };
        if let Some(l) = last.as_ref().filter(reusable) {
            return Some(l.clone() as Arc<dyn Held>);
        }
        let scan = Arc::new(Scan { body, t, interval, me, candidates, found: OnceLock::new() });
        *last = Some(scan.clone());
        Some(scan)
    }
}
