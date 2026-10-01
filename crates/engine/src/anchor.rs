//! Re-anchoring: the frame keeps its members near its origin, its rounding honest and its tube
//! current by moving the origin to the members' centre of mass, as an event of the law
//! (docs/representation.md §1).
//!
//! # The event
//!
//! At a committed tick (an epoch tick, before its kick, or, for a planted law, later):
//!
//! 0. **Settle.** Each member's position is owed its dropped drift, `Σ c·Δt/2^48` since the
//!    last anchor (kept per body, exact). It is paid, rounded to the nearest lattice unit, so
//!    the position error restarts from at most half a unit: the guiding centre's random walk
//!    (0.003 dr after one period, 333 dr after a thousand) cannot outlive one anchor's age.
//! 1. **Members leave.** The centre of mass of the members in the frame is found (exact
//!    integer weighted means: position rounded to a lattice unit, velocity to `2^-48`). A member
//!    farther than `r_p/32` from it (the size rule, `r_p` the tube's periapsis distance) is
//!    handed out: flagged, no longer kicked or counted, its state recorded in a [`Handoff`]
//!    (relative to the origin, with the tube). The centre is then found again without it, until
//!    nobody is out of the rule. For now a handed-out body stays a plain lattice body (its
//!    rebinding into the parent doll is the events layer's job).
//! 2. **Recentre.** The origin moves to the centre of mass and takes its velocity: every
//!    position loses `X` and every velocity `V`, exactly in integers. A body's `k + c/2^48` is
//!    shifted as one number and split again by rounding to nearest, so the carries stay
//!    consistent and the members' total momentum becomes zero to half a `2^-48` per unit of
//!    mass: the momentum went, exactly, into the tube (`M·V`).
//! 3. **Rebind the tube.** The origin's new state is the tube's readout at the tick plus
//!    `(X, V)`: an exact integer state. The tube is refitted to it (`crates/space`: a new orbit
//!    key, orientation and periapsis time) and the difference between the state and the fit's
//!    readout is kept, exactly, as the remainder ([`crate::tube`]). There is no reference circle
//!    to move and no Coriolis term to rebuild, so the recentring is one exact Galilean shift and
//!    the tube's velocity gains exactly what the members lost: total momentum is conserved
//!    bit for bit.
//!
//! The rules bite: the frame is refused when it breaks the weak-field rule (`n·R ≤ c/4`) unless
//! the policy says stress; a rebinding that would break the rule at the new tube, the epoch
//! angle (the tide's axis turning by more than `2^-5` rad per epoch), or the tube's being bound,
//! is refused; a re-anchor whose new velocities would be illegal (past c) is refused whole.
//! Refusals are counted, deterministic and change nothing.
//!
//! # Certificates
//!
//! An anchor is due (`Battle` looks after each epoch's kick, and fires at the next epoch) when
//! a member is farther than `r_p/32` from the origin (the size rule: the anchor recentres it,
//! and whoever is still out of the rule then leaves), or when `AGE_DIV` anchors per period
//! have not happened (the lattice's owed drift, which the reading of positions carries until
//! it is paid, and the composition, are settled at least every `P/64`), and once at genesis.
//! The ladder scenes and the judge use a shorter age (a policy: the reading error of a body is
//! its dropped drift, up to half a unit per chronon since the last anchor).
//!
//! # What is still open (measured, not hidden)
//!
//! - The remainder is a constant offset between two bindings; it is exact at its event and
//!   small (a few lattice units of position, the quantisation of the fit's orientation), but
//!   its transport through later motion is not a proved law (`crates/space/ENVELOPE.md`).
//! - The recentre is Galilean and the lattice law is special-relativistic: a body already near c
//!   cannot take the velocity shift, and the whole anchor is refused. A Lorentz boost is not
//!   linear and not exact.
//! - A handed-out body stays in the stepper with the frame's coordinates and no tide, so it
//!   can meet the members it left. The hand-off records are what the events layer takes.
//! - The tube's fit loses its size and eccentricity to the double root of its cubic when the
//!   state is exactly circular (about 5e-10 of the size per fit, biased by 1e-11): 4,000 rebindings
//!   of an exact circle move the origin 10,000 lattice units along-track in ten orbits
//!   (`tube.rs` tests). An eccentric state (1e-3) moves 21.
//! - Sparse order: every anchor re-forms the grids (a rebuild, O(n)), about one epoch kick's
//!   worth of upkeep per body; an anchor per P/8 is 1/50 of the epochs.
use crate::frame::{round_shift, Battle, BattleStats, FrameError, KickStats, Weight, CARRY_BITS, EPOCH_ANGLE_LOG2, EXTENT_SHIFT};
use crate::tube::{Reference, Tube, Units};
use emergent_lattice::law::Tick;
use emergent_lattice::{Kickable, Motion};
use emergent_space::orbit::Scalar;
use std::time::Instant;

/// The age certificate: at least this many anchors per orbit period (the lattice's dropped sub-quantum
/// drift, which the tide shears, grows like t^1.5 between anchors).
pub const AGE_DIV: i64 = 64;
/// The largest reference radius the frame's tube arithmetic is validated for (2^40 lattice units).
pub const MAX_RADIUS: i64 = 1 << 40;

/// `round(num / den)` for `den > 0`, ties up.
pub(crate) fn div_round(num: i128, den: i128) -> i128 {
    (2 * num + den).div_euclid(2 * den)
}

/// A member handed out of the frame: its state as it leaves, relative to the origin in the
/// frame's axes, and the tube (so a parent can compose them). Exact integers.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Handoff {
    /// The body's index (id order).
    pub index: usize,
    pub tick: Tick,
    /// Position from the origin, lattice units.
    pub x: [i64; 2],
    /// Velocity in the frame's axes relative to the origin, `2^-48` lattice units per chronon.
    pub v: [i128; 2],
    /// The tube after the event.
    pub tube: Tube,
}

/// How a battle re-anchors.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct AnchorPolicy {
    /// Anchor when this many epochs have passed since the last one (0: a period / [`AGE_DIV`]).
    pub age_epochs: u64,
    /// Refuse a frame outside the weak-field rule (`n·R ≤ c/4`), and a rebinding that would
    /// leave it. False is a stress scene: the integer law is defined there, the physics is not.
    pub enforce_orbit_rule: bool,
}

impl Default for AnchorPolicy {
    fn default() -> Self {
        AnchorPolicy { age_epochs: 0, enforce_orbit_rule: true }
    }
}

/// What one re-anchor did.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct AnchorReport {
    pub tick: Tick,
    /// The centre of mass of the members that stayed: the shift of every position.
    pub centre: [i64; 2],
    /// Its velocity, `2^-48` lattice units per chronon.
    pub velocity: [i128; 2],
    /// Their mass.
    pub mass: i128,
    /// The bodies handed out (indices).
    pub handed_out: Vec<usize>,
    /// The reference circle's radius and mean motion (the readout convention; they never move).
    pub radius: i64,
    pub n: u64,
    /// The tube was rebound to a different orbit (record) by this event.
    pub moved: bool,
    /// The whole event was refused (a velocity past c, an unbound or too fast tube): nothing changed.
    pub refused: bool,
    /// `Σ m·Δv` over every body, `2^-48` units: `−M·V` plus the rounding of the carries.
    pub dp: [i128; 2],
}

/// The state of a battle's re-anchoring.
pub(crate) struct Anchoring {
    pub(crate) age_epochs: u64,
    pub(crate) enforce: bool,
    /// Expired at the last epoch: fires at the next.
    pub(crate) due: bool,
    /// Planted law: an anchor waiting for its (late) tick.
    pub(crate) pending: Option<Tick>,
    pub(crate) shift: Tick,
    pub(crate) since: u64,
    /// Epochs to wait after a refusal.
    pub(crate) hold: u64,
    pub(crate) handoffs: Vec<Handoff>,
    scratch: Vec<[i64; 2]>,
    pub(crate) last_refusal: Option<String>,
    flush: Vec<[i64; 2]>,
    /// A frame with fewer members than this hands the rest out too (0: never).
    pub(crate) min_members: usize,
    /// The frame ends when nobody is left in it (set by [`Battle::with_min_members`] and [`Battle::dissolve`]).
    pub(crate) ends: bool,
    /// [`Battle::dissolve`] is running its event: everyone leaves.
    force: bool,
}

impl Anchoring {
    pub(crate) fn digest_into(&self, h: &mut blake3::Hasher, st: &BattleStats, active: &[bool], _units: Option<&Units>) {
        let put = |h: &mut blake3::Hasher, v: i128| {
            h.update(&v.to_le_bytes());
        };
        for v in [st.anchors, st.handed_out, st.anchors_refused, self.since, self.hold, self.due as u64] {
            put(h, v as i128);
        }
        put(h, self.pending.map_or(-1, |t| t as i128));
        for a in active {
            h.update(&[*a as u8]);
        }
        for ho in &self.handoffs {
            for v in [ho.index as i128, ho.tick as i128, ho.x[0] as i128, ho.x[1] as i128, ho.v[0], ho.v[1]] {
                put(h, v);
            }
            let t = &ho.tube;
            for v in [t.x[0], t.x[1], t.v[0], t.v[1], t.azimuth, t.tick as i128, t.radius as i128, t.n as i128] {
                put(h, v);
            }
        }
    }
}

/// Sums over the members in the frame: mass, `Σ m·x`, `Σ m·v` (`v` in `2^-48`).
#[derive(Clone, Copy, Default)]
struct Sums {
    mass: i128,
    mx: [i128; 2],
    mv: [i128; 2],
}

impl Sums {
    fn add(&mut self, o: Sums) {
        self.mass += o.mass;
        for c in 0..2 {
            self.mx[c] += o.mx[c];
            self.mv[c] += o.mv[c];
        }
    }
}

fn sums_slice(masses: &[i64], active: &[bool], motions: &[Motion], carries: &[[i64; 2]]) -> Sums {
    let mut s = Sums::default();
    for i in 0..masses.len() {
        if !active.is_empty() && !active[i] {
            continue;
        }
        let m = masses[i] as i128;
        s.mass += m;
        for c in 0..2 {
            s.mx[c] += m * motions[i].x[c] as i128;
            s.mv[c] += m * (((motions[i].k[c] as i128) << CARRY_BITS) + carries[i][c] as i128);
        }
    }
    s
}

/// Integer sums are associative, so the chunking never changes the result.
fn par_sums(threads: usize, masses: &[i64], active: &[bool], motions: &[Motion], carries: &[[i64; 2]]) -> Sums {
    let n = masses.len();
    let t = threads.clamp(1, n.max(1));
    if t == 1 {
        return sums_slice(masses, active, motions, carries);
    }
    let chunk = n.div_ceil(t);
    let mut total = Sums::default();
    std::thread::scope(|s| {
        let jobs: Vec<_> = (0..n.div_ceil(chunk))
            .map(|j| {
                let r = j * chunk..((j + 1) * chunk).min(n);
                let a = if active.is_empty() { active } else { &active[r.clone()] };
                let (m, mo, c) = (&masses[r.clone()], &motions[r.clone()], &carries[r]);
                s.spawn(move || sums_slice(m, a, mo, c))
            })
            .collect();
        for j in jobs {
            total.add(j.join().expect("anchor sums thread"));
        }
    });
    total
}

/// The frame change applied to every body's velocity: the origin's velocity `vel` (`2^-48`) subtracted.
struct Change {
    vel: [i128; 2],
}

fn transform_slice(ch: &Change, motions: &[Motion], carries: &[[i64; 2]], dk: &mut [[i64; 2]], new_carry: &mut [[i64; 2]]) {
    let half = 1i128 << (CARRY_BITS - 1);
    for (((m, c), d), nc) in motions.iter().zip(carries).zip(dk.iter_mut()).zip(new_carry.iter_mut()) {
        // v' = v − V, one number in 2^-48, then split by rounding to nearest.
        let vx = ((m.k[0] as i128) << CARRY_BITS) + c[0] as i128 - ch.vel[0];
        let vy = ((m.k[1] as i128) << CARRY_BITS) + c[1] as i128 - ch.vel[1];
        let (kx, ky) = ((vx + half) >> CARRY_BITS, (vy + half) >> CARRY_BITS);
        *d = [(kx - m.k[0] as i128) as i64, (ky - m.k[1] as i128) as i64];
        *nc = [(vx - (kx << CARRY_BITS)) as i64, (vy - (ky << CARRY_BITS)) as i64];
    }
}

fn par_transform(threads: usize, ch: &Change, motions: &[Motion], carries: &[[i64; 2]], dk: &mut [[i64; 2]], new_carry: &mut [[i64; 2]]) {
    let n = motions.len();
    let t = threads.clamp(1, n.max(1));
    if t == 1 {
        return transform_slice(ch, motions, carries, dk, new_carry);
    }
    let chunk = n.div_ceil(t);
    std::thread::scope(|s| {
        for (((m, c), d), nc) in motions.chunks(chunk).zip(carries.chunks(chunk)).zip(dk.chunks_mut(chunk)).zip(new_carry.chunks_mut(chunk)) {
            s.spawn(move || transform_slice(ch, m, c, d, nc));
        }
    });
}

/// The centre of mass of a set (`mx/M`, `mv/M`, each rounded: the position to a lattice unit,
/// the velocity to `2^-48`).
fn centre_of(s: &Sums) -> ([i64; 2], [i128; 2]) {
    let x = |c: usize| div_round(s.mx[c], s.mass) as i64;
    ([x(0), x(1)], [div_round(s.mv[0], s.mass), div_round(s.mv[1], s.mass)])
}

/// The exact recentring of a set of bodies on their centre of mass (the Galilean part of a
/// re-anchor, alone): positions lose `centre`, velocities lose `velocity`, and the result is
/// the new integer velocities' change and carries. `None` if the set is empty.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Recentred {
    pub centre: [i64; 2],
    /// `2^-48` lattice units per chronon.
    pub velocity: [i128; 2],
    pub mass: i128,
    pub dk: Vec<[i64; 2]>,
    pub carries: Vec<[i64; 2]>,
}

pub fn recentre(masses: &[i64], motions: &[Motion], carries: &[[i64; 2]], threads: usize) -> Option<Recentred> {
    let s = par_sums(threads, masses, &[], motions, carries);
    if s.mass == 0 {
        return None;
    }
    let (centre, velocity) = centre_of(&s);
    let n = motions.len();
    let (mut dk, mut nc) = (vec![[0i64; 2]; n], vec![[0i64; 2]; n]);
    par_transform(threads, &Change { vel: velocity }, motions, carries, &mut dk, &mut nc);
    Some(Recentred { centre, velocity, mass: s.mass, dk, carries: nc })
}

impl<S: Kickable> Battle<S> {
    /// Turn re-anchoring on, before the first epoch (the frame's genesis is anchored at it).
    /// Refused when the frame breaks the weak-field rule `n·R ≤ c/4`, unless the policy says
    /// stress. A flat frame has no tide and nothing to anchor: it is returned as it is.
    pub fn with_anchoring(mut self, policy: AnchorPolicy) -> Result<Self, FrameError> {
        assert!(self.next == 0, "re-anchoring is turned on before the first epoch");
        if self.frame.is_flat() {
            return Ok(self);
        }
        if policy.enforce_orbit_rule && !self.frame.orbit_speed_ok() {
            return Err(FrameError(format!(
                "orbit speed n·R = {:.3e} c exceeds c/4: outside the weak-field rule (a stress scene needs enforce_orbit_rule = false)",
                self.frame.n_f64() * self.frame.radius as f64 / self.frame.q as f64
            )));
        }
        if self.frame.radius > MAX_RADIUS {
            return Err(FrameError(format!("orbit radius {} beyond 2^40 lattice units: the tube's arithmetic is validated up to there", self.frame.radius)));
        }
        let age = if policy.age_epochs == 0 { ((self.frame.period() / self.frame.epoch()) / AGE_DIV).max(1) as u64 } else { policy.age_epochs };
        self.anchoring = Some(Anchoring {
            age_epochs: age,
            enforce: policy.enforce_orbit_rule,
            due: true,
            pending: None,
            shift: 0,
            since: 0,
            hold: 0,
            handoffs: Vec::new(),
            scratch: vec![[0; 2]; self.motions.len()],
            last_refusal: None,
            flush: Vec::new(),
            min_members: 0,
            ends: false,
            force: false,
        });
        Ok(self)
    }

    /// A frame exists to resolve contacts between its members, so one with fewer than `n` of them has
    /// nothing left to resolve: at the anchor that leaves fewer, the rest are handed out too, the frame
    /// ends there ([`Battle::is_dissolved`], and [`Battle::run_to`] stops at that tick), and its parent
    /// (the events layer) takes every hand-off. With `n = 2`, a lone member is a tube of the parent.
    pub fn with_min_members(mut self, n: usize) -> Self {
        if let Some(a) = self.anchoring.as_mut() {
            a.min_members = n;
            a.ends = n > 0;
        }
        self
    }

    /// The frame ends now: every member still in it is handed out at the committed tick, exactly as it
    /// stands (an event of the law, like an anchor; nobody is recentred), and the frame is dissolved.
    pub fn dissolve(&mut self) -> Result<AnchorReport, FrameError> {
        let Some(a) = self.anchoring.as_mut() else { return Err(FrameError("re-anchoring is off (Battle::with_anchoring)".into())) };
        a.force = true;
        a.ends = true;
        let r = self.do_anchor(None);
        if let Some(a) = self.anchoring.as_mut() {
            a.force = false;
        }
        r
    }

    /// Whether the frame has ended: it was asked to end (`with_min_members`, `dissolve`) and nobody is in it.
    pub fn is_dissolved(&self) -> bool {
        self.anchoring.as_ref().is_some_and(|a| a.ends) && self.active.iter().all(|&a| !a)
    }

    /// What a handed-out member's position is still owed, `2^-48` lattice units: the sub-lattice-unit
    /// remainder of its dropped drift, which the hand-off record's integer position does not hold.
    pub fn owed(&self, index: usize) -> [i128; 2] {
        self.pcarry[index]
    }

    /// The parent's kick on the frame's origin (docs/law.md, "Perturbed motion": the origin is a tube in
    /// its doll like any other, and the parent's tide, the secondaries and the neighbours act on it as
    /// kicks): at the committed tick the origin's velocity gains `dv` (`2^-48` lattice units per chronon)
    /// and the tube is rebound to that state with the exact remainder. The members are *not* kicked: their
    /// frame is the origin's, in free fall, and feels what the origin does not (the tide, at epochs).
    /// Refused, and nothing changed, when the new tube is not one the frame can hold (see [`Battle::reanchor`]).
    pub fn kick_origin(&mut self, dv: [i128; 2]) -> Result<(), FrameError> {
        if self.frame.is_flat() {
            return Err(FrameError("a flat frame has no origin tube".into()));
        }
        let tick = self.stepper.tick();
        let enforce = self.anchoring.as_ref().is_some_and(|a| a.enforce);
        let new = self.rebind(tick, [0, 0], dv, enforce)?;
        self.reference = Some(new);
        Ok(())
    }

    /// `floor(log2)` of the origin tube's radial period, in chronons (the events layer's kick step is a
    /// fraction of it). `None` for a flat frame.
    pub fn origin_period_log2(&self) -> Option<i32> {
        let (p, r) = (self.frame.parent.as_ref()?, self.reference.as_ref()?);
        r.period_log2(&p.units).ok()
    }

    /// Planted law for tests: every re-anchor happens `shift` chronons after the epoch that
    /// found it due (0 ≤ shift < the epoch).
    pub fn with_anchor_shift(mut self, shift: Tick) -> Self {
        assert!((0..self.frame.epoch()).contains(&shift), "an anchor is late by less than an epoch");
        if let Some(a) = self.anchoring.as_mut() {
            a.shift = shift;
        }
        self
    }

    /// The frame's tube, as a record: the orbit's periapsis (lattice units) and its eccentricity
    /// (a float, for reporting only). `None` for a flat frame.
    pub fn orbit(&self) -> Option<(i64, f64)> {
        self.reference.as_ref().map(|r| (r.size(), 1.0 / (r.spec().key.k as f64 / (1u64 << 48) as f64) - 1.0))
    }

    /// Why the last refused re-anchor was refused (the stepper's or the tube's reason).
    pub fn last_refusal(&self) -> Option<&str> {
        self.anchoring.as_ref().and_then(|a| a.last_refusal.as_deref())
    }

    /// The members handed out so far, in order.
    pub fn handoffs(&self) -> &[Handoff] {
        self.anchoring.as_ref().map_or(&[], |a| &a.handoffs)
    }

    pub(crate) fn pending_anchor(&self) -> Option<Tick> {
        self.anchoring.as_ref().and_then(|a| a.pending)
    }

    /// Re-anchor now, at the stepper's committed tick (an event of the law that nothing
    /// scheduled: the caller's own, as in the tests).
    pub fn reanchor(&mut self) -> Result<AnchorReport, FrameError> {
        if self.anchoring.is_none() {
            return Err(FrameError("re-anchoring is off (Battle::with_anchoring)".into()));
        }
        self.do_anchor(None)
    }

    /// Before an epoch's kick: settle the positions, and re-anchor if one is due.
    pub(crate) fn anchor_epoch(&mut self, weight: Weight) -> Result<(), FrameError> {
        let tick = self.stepper.tick();
        let go = match self.anchoring.as_mut() {
            None => return Ok(()),
            Some(a) => {
                if a.due && a.hold == 0 {
                    a.due = false;
                    if a.shift == 0 {
                        true
                    } else {
                        a.pending = Some(tick + a.shift);
                        false
                    }
                } else {
                    false
                }
            }
        };
        if go {
            self.do_anchor(Some(weight))?;
        }
        Ok(())
    }

    /// After an epoch's kick: count the age, and look at the certificates (the extent from this
    /// epoch's pass over the members).
    pub(crate) fn anchor_certificate(&mut self, k: &KickStats) {
        let r = self.reference.as_ref().map_or(self.frame.radius, |r| r.size()) as i128;
        let Some(a) = self.anchoring.as_mut() else { return };
        a.since += 1;
        a.hold = a.hold.saturating_sub(1);
        if a.due || a.pending.is_some() || a.hold > 0 {
            return;
        }
        if a.since >= a.age_epochs || (k.max_r2 << (2 * EXTENT_SHIFT)) > r * r {
            a.due = true;
        }
    }

    /// Add the sub-quantum drift each body's lattice motion dropped since the last update: the
    /// lattice moves at the integer `k`, the law's velocity is `k + c/2^48`, so `c·Δt` (in `2^-48`
    /// units) is owed to the position. Exact integers; only for bodies still in the frame.
    pub(crate) fn settle_position_carries(&mut self, tick: Tick) {
        let dt = (tick - self.ptick) as i128;
        self.ptick = tick;
        if dt == 0 {
            return;
        }
        for i in 0..self.pcarry.len() {
            if self.active[i] {
                for c in 0..2 {
                    self.pcarry[i][c] += self.carries[i][c] as i128 * dt;
                }
            }
        }
    }

    /// The tube rebound to the origin's new state: the readout at `tick` plus the recentring
    /// `(centre, vel)`. Refused (and nothing changes) when the new tube is not a bound orbit,
    /// turns the tide's axis by more than `2^-5` rad per epoch, or, under the weak-field rule,
    /// has a circular speed above `c/4` at its periapsis.
    fn rebind(&self, tick: Tick, centre: [i64; 2], vel: [i128; 2], enforce: bool) -> Result<Reference, FrameError> {
        let (p, old) = (self.frame.parent.as_ref().expect("a frame with a tube has a parent"), self.reference.as_ref().expect("a frame with a parent has a tube"));
        let (x, v) = old.readout(&p.units, tick)?;
        let new = Reference::bind(
            &p.units,
            ([x[0] + ((centre[0] as i128) << 32), x[1] + ((centre[1] as i128) << 32)], [v[0] + vel[0], v[1] + vel[1]]),
            tick,
        )?;
        let sp = |e: emergent_space::Error| FrameError(format!("crates/space: {e:?}"));
        // The tide's axis turns by at most twice the epoch angle per epoch (an epoch of one chronon: by up to 2^-5).
        let turn = new.peak_rate(&p.units)?.mul(Scalar::integer(self.frame.epoch())).map_err(sp)?;
        let limit = if self.frame.epoch() == 1 { 5 } else { EPOCH_ANGLE_LOG2 as i16 - 1 };
        if turn > Scalar::power_of_two(-limit) {
            return Err(FrameError("the new tube turns the tide's axis by too much per epoch".into()));
        }
        if enforce && new.circular_speed(&p.units)?.scale(2).map_err(sp)? > Scalar::integer(self.frame.q) {
            return Err(FrameError("the new tube's circular speed exceeds c/4: outside the weak-field rule".into()));
        }
        Ok(new)
    }


    /// The event. `weight` is `Some` when it runs before an epoch's kick (the motions are then
    /// the epoch's, and are updated in place for the kick that follows), `None` between epochs.
    pub(crate) fn do_anchor(&mut self, weight: Option<Weight>) -> Result<AnchorReport, FrameError> {
        let t_start = Instant::now();
        let tick = self.stepper.tick();
        let n_all = self.motions.len();
        if weight.is_none() {
            self.stepper.motions(&mut self.motions);
            self.anchoring.as_mut().expect("anchoring is on").pending = None;
        }
        let (radius, n_frame) = (self.frame.radius, self.frame.n);
        let size = self.reference.as_ref().map_or(radius, |r| r.size());

        // 0. Settle the positions. Each body's sub-quantum drift since the last anchor is owed to
        // its position (the lattice moved it at the integer k): pay it, to the nearest lattice
        // unit, so the position error restarts from at most half a unit at every anchor. This is
        // what stops the guiding centre's random walk: it cannot grow past one anchor's age.
        self.settle_position_carries(tick);
        let mut flush = std::mem::take(&mut self.anchoring.as_mut().expect("anchoring is on").flush);
        flush.clear();
        flush.resize(n_all, [0, 0]);
        for i in 0..n_all {
            if self.active[i] {
                for c in 0..2 {
                    flush[i][c] = round_shift(self.pcarry[i][c], CARRY_BITS) as i64;
                    self.motions[i].x[c] += flush[i][c];
                }
            }
        }

        // 1. Who stays: the centre of mass of the members, without whoever is out of the size rule.
        let mut active = self.active.clone();
        let mut handed: Vec<usize> = Vec::new();
        let (force, min_members) = self.anchoring.as_ref().map_or((false, 0), |a| (a.force, a.min_members));
        let (mut sums, centre, vel) = loop {
            if force {
                // The frame ends: everyone still in it goes, as they stand.
                for i in 0..n_all {
                    if active[i] {
                        active[i] = false;
                        handed.push(i);
                    }
                }
                break (Sums::default(), [0, 0], [0, 0]);
            }
            let s = par_sums(self.threads, &self.masses, &active, &self.motions, &self.carries);
            if s.mass == 0 {
                break (s, [0, 0], [0, 0]);
            }
            let (x, v) = centre_of(&s);
            let mut any = false;
            for i in 0..n_all {
                if active[i] {
                    let (dx, dy) = ((self.motions[i].x[0] - x[0]) as i128, (self.motions[i].x[1] - x[1]) as i128);
                    if (dx * dx + dy * dy) << (2 * EXTENT_SHIFT) > size as i128 * size as i128 {
                        active[i] = false;
                        handed.push(i);
                        any = true;
                    }
                }
            }
            if !any {
                break (s, x, v);
            }
        };
        // Too few members left to touch one another: the rest leave with them, and the frame ends.
        let left = active.iter().filter(|&&a| a).count();
        if min_members > 0 && left > 0 && left < min_members {
            for i in 0..n_all {
                if active[i] {
                    active[i] = false;
                    handed.push(i);
                }
            }
            sums = Sums::default();
        }
        let dissolved = sums.mass == 0;
        if dissolved {
            // Everyone is out of the rule: nobody is left to recentre on, so nothing moves. The
            // members are handed out as they stand (the settled positions are not applied).
            for i in 0..n_all {
                for c in 0..2 {
                    self.motions[i].x[c] -= flush[i][c];
                }
            }
            flush.iter_mut().for_each(|f| *f = [0, 0]);
        }

        // 2. The origin takes the members' centre of mass and its velocity (the momentum the
        // recentring takes from the members goes, exactly, into the tube).
        // 3. The tube is rebound to that state, with the exact remainder.
        let enforce = self.anchoring.as_ref().expect("anchoring is on").enforce;
        let mut rebound: Option<Reference> = None;
        let mut refusal = None;
        if !dissolved {
            match self.rebind(tick, centre, vel, enforce) {
                Ok(r) => rebound = Some(r),
                Err(e) => refusal = Some(e.0),
            }
        }

        // 4. New velocities, then the stepper.
        let change = Change { vel };
        let mut scratch = std::mem::take(&mut self.anchoring.as_mut().expect("anchoring is on").scratch);
        scratch.resize(n_all, [0, 0]);
        let mut applied = dissolved;
        let t_plan = Instant::now();
        if !dissolved && refusal.is_none() {
            par_transform(self.threads, &change, &self.motions, &self.carries, &mut self.dk, &mut scratch);
            let dx: Vec<[i64; 2]> = flush.iter().map(|f| [f[0] - centre[0], f[1] - centre[1]]).collect();
            let t_apply = Instant::now();
            match self.stepper.rebase(&dx, &self.dk) {
                Ok(()) => applied = true,
                Err(e) => refusal = Some(e.0),
            }
            self.stats.anchor_apply_ns += t_apply.elapsed().as_nanos() as u64;
        }
        self.stats.anchor_plan_ns += (t_plan - t_start).as_nanos() as u64;
        if !applied {
            let a = self.anchoring.as_mut().expect("anchoring is on");
            // Refused whole (a velocity past c, out of range, or a tube that is not the frame's):
            // nothing changed anywhere.
            for i in 0..n_all {
                for c in 0..2 {
                    self.motions[i].x[c] -= flush[i][c];
                }
            }
            a.scratch = scratch;
            a.flush = flush;
            a.since = 0;
            a.hold = a.age_epochs;
            self.stats.anchors_refused += 1;
            a.last_refusal = refusal;
            return Ok(AnchorReport { tick, centre, velocity: vel, mass: sums.mass, handed_out: Vec::new(), radius, n: n_frame, moved: false, refused: true, dp: [0; 2] });
        }

        // 5. Commit.
        let mut dp = [0i128; 2];
        if !dissolved {
            for i in 0..n_all {
                let m = self.masses[i] as i128;
                for c in 0..2 {
                    dp[c] += m * (((self.dk[i][c] as i128) << CARRY_BITS) + scratch[i][c] as i128 - self.carries[i][c] as i128);
                    self.motions[i].x[c] -= centre[c];
                    self.motions[i].k[c] += self.dk[i][c];
                    self.pcarry[i][c] -= (flush[i][c] as i128) << CARRY_BITS;
                }
                self.carries[i] = scratch[i];
            }
        }
        let a = self.anchoring.as_mut().expect("anchoring is on");
        let mut moved = false;
        if let Some(new) = rebound {
            moved = !self.reference.as_ref().is_some_and(|old| old.same_orbit(&new));
            self.reference = Some(new);
        }
        if let (Some(p), Some(r)) = (self.frame.parent.as_ref(), self.reference.as_ref()) {
            for &i in &handed {
                let v = [((self.motions[i].k[0] as i128) << CARRY_BITS) + self.carries[i][0] as i128, ((self.motions[i].k[1] as i128) << CARRY_BITS) + self.carries[i][1] as i128];
                let tube = Tube::read(&p.units, r, tick, radius, n_frame).expect("the tube reads at its own binding");
                a.handoffs.push(Handoff { index: i, tick, x: self.motions[i].x, v, tube });
            }
        }
        a.scratch = scratch;
        a.flush = flush;
        a.since = 0;
        a.due = false;
        self.stats.anchors += 1;
        self.stats.handed_out += handed.len() as u64;
        self.gone += handed.len();
        self.active = active;
        Ok(AnchorReport { tick, centre, velocity: vel, mass: sums.mass, handed_out: handed, radius, n: n_frame, moved, refused: false, dp })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn division_rounds_to_nearest_with_ties_up() {
        assert_eq!((div_round(7, 2), div_round(5, 2), div_round(-5, 2), div_round(-7, 2), div_round(-6, 4), div_round(6, 4)), (4, 3, -2, -3, -1, 2));
    }
}
