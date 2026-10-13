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
    /// The universe resolves a held scan in idle time, in the order the scans were taken, and always before it is
    /// asked for a digest or a count, so the encounters (and what is hashed of them) are the same as if each had been
    /// found at once. `None` (the default) means the finder does not split: the universe calls `find` where it is.
    fn capture(&self, _ctx: &Ctx, _body: usize, _t: Tick, _interval: Tick) -> Option<Arc<dyn Held>> {
        None
    }
}

/// A scan taken and not yet answered: everything its answer reads is held in it, so the answer is the same whenever it
/// is given (the bodies' histories may have moved on, been pruned, or the bodies died since).
pub trait Held: Send + Sync {
    fn answer(&self) -> Vec<Encounter>;
}

/// The exact check for the player's neighbourhood: every body in the player's doll, tested against
/// the player over the interval.
///
/// **A filter in front of the exact test, never in place of it.** The test reads the other body's tube at `t` (a root solve
/// for a passage, tens of microseconds) and applies the lattice predicate to the pair's separation `d` and relative
/// displacement `w`. A pair can hit only if `|d| − |w| ≤ near` (the predicate asks that some point of the segment `d + s·w`
/// be within `near`), and the finder remembers where each body was when it last paid for a reading: `x_a` at `t_a`. A
/// tube's speed is bounded by its integer word (`units.1`: the velocity components are `i64` words of `2^units.1`, sized
/// to the tube's periapsis speed with margin, and a state outside the word is refused) and by `c = 1`, so the body is
/// within `V·|t − t_a|` of `x_a`, the player is read exactly now, and `|d| ≥ |x_a − x_p| − V·|t − t_a|`, `|w| ≤ (V + |v_p|)·h`.
/// When that lower bound clears `near` by a wide margin (1% and a few units of the predicate's resolution), the exact test
/// would answer no and is not run: the same encounters, in the same order, with the same digest. The bound is evaluated in
/// floats with a margin eight orders of magnitude above their rounding (a filter that can only skip a test that fails, as
/// in exact geometric predicates), and `verify` runs the exact test on what it skips and panics if it ever finds a hit.
///
/// **The predicate wraps.** `hit` multiplies `i128`s; for a pair thousands of kilometres apart over a long interval
/// (|d|·|w| beyond 2^63 in its units) the products wrap and it answers yes or no on garbage, and that answer is hashed
/// into the digest. The filter therefore skips only where no product can wrap; every other pair is read and tested
/// exactly, wrapped bits and all (a finding for the law's owner: the fix changes digests).
pub struct PlayerNeighbourhood {
    state: Arc<Mutex<State>>,
    /// Run the exact test on every body the filter skips and panic if one hits (the tests' control; off in the game).
    pub verify: bool,
    /// The tests' planted fault ([`PlayerNeighbourhood::planted_always_skip`]).
    always_skip: bool,
}

#[derive(Default)]
struct State {
    memo: Vec<Option<Memo>>,
    /// The last scan taken: a scan after a boundary or an opening, which rebind nothing, reads the player at the tick of
    /// the kick before it (the finder reads the player at its binding's tick), and with the same inputs it is that
    /// scan again; the encounters are logged again, and the answer is not found twice.
    last: Option<Arc<Scan>>,
}

/// Everything one scan reads.
struct Scan {
    state: Arc<Mutex<State>>,
    verify: bool,
    always_skip: bool,
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

/// Where a body was when the finder last read it, and which binding that reading belongs to.
#[derive(Clone, Copy)]
struct Memo {
    print: Print,
    t: Tick,
    x: [f64; 2],
}

/// A binding's identity: the tube, its angle and time, its units and the event that made it. The bound on the body's
/// speed is the binding's, so a memo is used only while the body has not been rebound since.
#[derive(Clone, Copy, PartialEq, Eq)]
struct Print {
    event_time: Tick,
    key: u32,
    angle: u32,
    peri: i64,
    units: (i16, i16),
    doll: u16,
}

impl Print {
    fn of(b: &Binding) -> Self {
        Self { event_time: b.event_time, key: b.tube.key, angle: b.tube.periapsis_angle, peri: b.tube.periapsis_time.get() as i64, units: b.units, doll: b.doll }
    }
}

impl Default for PlayerNeighbourhood {
    fn default() -> Self {
        Self { state: Arc::new(Mutex::new(State::default())), verify: false, always_skip: false }
    }
}

impl PlayerNeighbourhood {
    /// The control: every body the filter skips is tested exactly, and a hit among them panics.
    pub fn verifying() -> Self {
        Self { verify: true, ..Self::default() }
    }

    /// A planted fault for the tests' controls: a filter that skips every body it has read once (it believes nothing
    /// moves), with or without the verification that catches it.
    #[doc(hidden)]
    pub fn planted_always_skip(verify: bool) -> Self {
        Self { verify, always_skip: true, ..Self::default() }
    }
}

/// A speed no body of this binding exceeds, in units of `c` (the doll's `c = 1`): the integer word's capacity, at most `c`.
fn speed_cap(b: &Binding) -> f64 {
    (1.5 * 2f64.powi(63 + b.units.1 as i32)).min(1.0)
}

fn floats(a: V2) -> [f64; 2] {
    [to_f64(a[0]), to_f64(a[1])]
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
    /// The expensive half: read the player and each candidate at `t` and apply the predicate, past the filter where it applies.
    fn compute(&self) -> Vec<Encounter> {
        let mut out = Vec::new();
        let (me, t, body) = (&self.me, self.t, self.body);
        let Ok((x, v)) = me.cartesian(t) else { return out };
        let h = match time_of(self.interval, me.clock_exp) {
            Ok(h) => h,
            Err(_) => return out,
        };
        let (xf, vf, hf) = (floats(x), floats(v), to_f64(h));
        let speed = (vf[0] * vf[0] + vf[1] * vf[1]).sqrt();
        let mut state = self.state.lock().expect("the finder's state");
        if let Some(last) = self.candidates.last() {
            if state.memo.len() <= last.0 {
                state.memo.resize(last.0 + 1, None);
            }
        }
        for (j, other, reach) in &self.candidates {
            let (j, reach) = (*j, *reach);
            // The exact test, given the other body's state at `t`.
            let exact = |xj: V2, vj: V2| -> Res<Option<bool>> {
                let d = sub2(xj, x)?;
                let w = [vj[0].sub(v[0])?.mul(h)?, vj[1].sub(v[1])?.mul(h)?];
                // Integers in units of reach/2^20: the lattice predicate is exact on i128.
                let q_exp = reach.exponent() as i32 - 20;
                let (di, wi) = (integers(d, q_exp)?, integers(w, q_exp)?);
                let near = reach.scale(ENCOUNTER_LOG2)?.fixed(-q_exp)?;
                if !hit(di, wi, near) {
                    return Ok(None);
                }
                Ok(Some(hit(di, wi, reach.fixed(-q_exp)?)))
            };
            // The filter: where the body was when it was last read, and how far it can have gone since.
            let print = Print::of(other);
            if let Some(m) = state.memo[j].filter(|m| m.print == print) {
                let cap = speed_cap(other);
                let dt = t.abs_diff(m.t) as f64 * 2f64.powi(other.clock_exp as i32);
                let gap = ((m.x[0] - xf[0]).powi(2) + (m.x[1] - xf[1]).powi(2)).sqrt();
                let near = to_f64(reach) * (1u64 << ENCOUNTER_LOG2) as f64;
                // |d| ≥ gap − cap·dt and |w| ≤ (cap + |v_p|)·h: the closest the pair gets over the interval.
                let closest = gap - cap * dt - (cap + speed) * hf;
                // The predicate's products are `i128`s that wrap: far beyond its design it answers yes on garbage, and that
                // answer is part of the digest. The filter skips a pair only where the predicate cannot have wrapped:
                // every product below 2^124 in its units.
                let unit = 2f64.powi(reach.exponent() as i32 - 20);
                let (d_max, w_max, near_int) = ((gap + cap * dt) / unit + 4.0, (cap + speed) * hf / unit + 4.0, near / unit + 4.0);
                let no_wrap = d_max < 2f64.powi(60) && w_max < 2f64.powi(60) && d_max * w_max < 2f64.powi(60) && w_max * w_max * near_int * near_int < 2f64.powi(122);
                if self.always_skip || (no_wrap && closest > near * 1.01) {
                    if self.verify {
                        if let Ok((xj, vj)) = other.cartesian(t) {
                            assert!(!matches!(exact(xj, vj), Ok(Some(_))), "the filter skipped body {j} at tick {t}, which hits (closest bound {closest:e}, near {near:e})");
                        }
                    }
                    continue;
                }
            }
            let found = match other.cartesian(t) {
                Ok((xj, vj)) => {
                    state.memo[j] = Some(Memo { print, t, x: floats(xj) });
                    exact(xj, vj)
                }
                Err(e) => {
                    state.memo[j] = None;
                    Err(e)
                }
            };
            if let Ok(Some(contact)) = found {
                out.push(Encounter { a: body, b: j, t, contact });
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
        let mut candidates = Vec::new();
        for j in 0..ctx.bodies.len() {
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
        let last = {
            let state = self.state.lock().expect("the finder's state");
            state.last.clone().filter(|l| l.same_inputs(body, t, interval, &me, &candidates))
        };
        if let Some(last) = last {
            if self.verify && last.found.get().is_some() {
                // The repeated scan is the earlier answer; recompute it from nothing (no filter) and compare.
                let fresh = Scan { state: Arc::new(Mutex::new(State::default())), verify: false, always_skip: false, body, t, interval, me: me.clone(), candidates: candidates.clone(), found: OnceLock::new() };
                assert_eq!(fresh.answer(), last.answer(), "a repeated scan at tick {t} found something else");
            }
            return Some(last as Arc<dyn Held>);
        }
        let scan = Arc::new(Scan { state: self.state.clone(), verify: self.verify, always_skip: self.always_skip, body, t, interval, me, candidates, found: OnceLock::new() });
        self.state.lock().expect("the finder's state").last = Some(scan.clone());
        Some(scan)
    }
}
