//! Re-anchoring: the frame keeps its members near its origin and its tide honest by moving
//! the origin, the reference circle and the members' rounding, as an event of the law
//! (docs/representation.md §1).
//!
//! # What the measurements said
//!
//! Members released at rest at dr/R = 1e-3, full two-body motion (RK4, float) as the truth, ten
//! periods (`tests/reanchor.rs`; the float model of the variants is a throwaway):
//!
//! - The frame's output today, (x, y) read as Cartesian offsets from the reference point, is
//!   2.1% off after one period and 19.8% after ten. Most of that is geometry, not tide: y is
//!   an arc, and the missing `x = −y²/2R` is 18% of the offset at the azimuth 0.37 rad. Read as
//!   (radial offset, arc length) the same fixed linear law is within 0.84% for all ten periods.
//!   So the tide is good to about 1%. What the fixed axes cannot do is turn with the group: the
//!   tide keeps pointing along x while it rotates with the azimuth, and the group's shape is off
//!   by 38% after ten periods.
//! - Re-expressing the members about a new point that drifts with the steady shear (`x' = x − X`,
//!   `k'_y = k_y + 3nX/2`, `n` unchanged, the first sketch here) is a change of variables of a
//!   linear system: it resets nothing physical (float model: the same 19.8%).
//! - Moving the circle, the reference point keeping its azimuth and `n` following Kepler's third
//!   law (`n' = n·(R/R')^{3/2}`), does it. The circle through the origin's position keeps its
//!   drift and gave 4.7% (1.8% anchored every P/32); the circle through the origin's guiding
//!   centre `x_c = 4x + 2v_y/n` gave 0.45% at any cadence, and is built: 0.44% worst position
//!   error over ten periods (0.24% after the first), group shape 0.97%. The floor is the linear
//!   epicycle's second-order shape (a Kepler ellipse against it), about 4·dr/R.
//! - The lattice's rounding is what broke the cadence. The lattice moves a body at the integer
//!   `k` while the law's velocity is `k + c/2^48`: every epoch drops `c·E/2^48` of position. The
//!   error feeds the tide and shears, and a scene that re-anchored at the wrong cadence was
//!   1.4% off at 1e-3 and 15% at 1e-4 (0.44% or 1.1% at the right one). Paying that drift into the
//!   positions at every anchor removes it: the same 0.44% at every cadence from 8 epochs to
//!   half a period, and 0.46% at 1e-4.
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
//!    farther than `R/32` from it (the size rule) is handed out: flagged, no longer kicked or
//!    counted, its state recorded in a [`Handoff`] (relative to the origin, with the tube).
//!    The centre is then found again without it, until nobody is out of the rule. For now a
//!    handed-out body stays a plain lattice body (tube handoffs belong to `crates/space`).
//! 2. **Recentre.** The origin moves to the centre of mass and takes its velocity: every
//!    position loses `X` and every velocity `V`, exactly in integers. A body's `k + c/2^48` is
//!    shifted as one number and split again by rounding to nearest, so the carries stay
//!    consistent and the members' total momentum becomes zero to half a `2^-48` per unit of
//!    mass: the momentum went, exactly, into the tube (`M·V`).
//! 3. **The tube.** The frame's own tube in its parent is the origin's state against the
//!    reference circle: `x`, `v`, in `2^-32` and `2^-48` lattice units, and the azimuth of the
//!    reference point against the parent's original axes (radians `2^-60`, exact). It absorbs
//!    `(X, V)`, and between events it is a member of the same law: kicked at every epoch with
//!    the frame's weights, drifting exactly. It is the stand-in for the parent's own law
//!    (`crates/space`): it is only as good as a linear epicycle about a circle.
//! 4. **Move the circle.** The tube's guiding centre (from the velocity at the tick: the
//!    half-kicked one, the staggered lattice velocity being half an epoch late) is where the
//!    reference circle goes: `R' = R + x_c`, `n' = n·(R/R')^{3/2}` (integer square root), the
//!    reference point keeping its azimuth. Members' velocities gain `δn·ẑ×r` and the tube's
//!    `δn·ẑ×P` (`δn = n − n'`, `P` its position from the parent: the steady shear), and the
//!    tube's `x` loses `x_c`. The tube then goes round the new circle in a pure epicycle, so
//!    the frame's axes turn with the tube and the linear error stays where it began. The epoch
//!    does not change (it is the frame's clock).
//!
//! The rules bite: the frame is refused when it breaks the weak-field rule (`n·R ≤ c/4`) unless
//! the policy says stress; a circle move that would break the rule, the epoch angle, or the
//! extent (`|x_c| ≤ R/32`) is refused and counted; a re-anchor whose new velocities would be
//! illegal (past c) is refused whole and counted. Refusals are deterministic.
//!
//! # Certificates
//!
//! An anchor is due (`Battle` looks after each epoch's kick, and fires at the next epoch) when
//! a member is farther than `R/32` from the origin (the size rule: the anchor recentres it,
//! and whoever is still out of the rule then leaves), or when `AGE_DIV` anchors per period
//! have not happened (the lattice's owed drift, and the composition, are settled at least every
//! `P/8`), and once at genesis. The ladder scenes use a shorter age (a policy).
//!
//! # What is still wrong (measured, not hidden)
//!
//! - Members' axes stay on the reference point, not on the tube: the tide direction is off by
//!   the tube's azimuth against it (an epicycle: 2A/R), and its strength uses the reference
//!   circle, not the tube's instantaneous radius (±3A/R): the group's shape is 1% off at 1e-3
//!   and 2.3% at 3e-3.
//! - The tube is a linear epicycle about a circle. Released on a drift-free epicycle
//!   (`v_y = −2n·x`) its guiding centre is exactly right in first order, and the true one is
//!   second order, `−(dr/R)²R`: the true drift is `94·(dr/R)²·R` in ten periods, 10% of the
//!   offset at 1e-3 (12% measured; 9% at 3e-4, where lattice rounding adds). Using the exact
//!   semi-major axis (vis-viva) moves the error, not removes it: the linear epicycle's own
//!   guiding centre is then off at the same order. That is the parent's exact Kepler tube.
//! - The recentre is Galilean and the lattice law is special-relativistic: a body already near c
//!   cannot take the velocity shift, and the whole anchor is refused (55 of 65 attempts in the
//!   storm scene, nT = 8), so a storm never re-anchors. A Lorentz boost is not linear and not
//!   exact.
//! - A handed-out body stays in the stepper with the frame's coordinates and no tide, so it
//!   can meet the members it left. The hand-off records are what `crates/space` will take.
//! - Sparse order: every anchor re-forms the grids (a rebuild, O(n)), about one epoch kick's
//!   worth of upkeep per body; an anchor per P/8 is 1/50 of the epochs.
use crate::frame::{round_shift, Battle, BattleStats, Frame, FrameError, KickStats, Weight, Weights, CARRY_BITS, EXTENT_SHIFT};
use emergent_lattice::law::Tick;
use emergent_lattice::{Kickable, Motion};
use std::time::Instant;

/// Fraction bits of the tube's position (its velocity has [`CARRY_BITS`]).
pub const TUBE_BITS: u32 = 32;
/// The age certificate: at least this many anchors per orbit period.
pub const AGE_DIV: i64 = 8;
/// The largest reference radius the anchor arithmetic is exact for (2^40 lattice units).
pub const MAX_RADIUS: i64 = 1 << 40;

/// `round(num / den)` for `den > 0`, ties up.
pub(crate) fn div_round(num: i128, den: i128) -> i128 {
    (2 * num + den).div_euclid(2 * den)
}

/// `floor(sqrt(n))`.
pub(crate) fn isqrt(n: u128) -> u128 {
    if n < 2 {
        return n;
    }
    let mut x = 1u128 << (128 - n.leading_zeros()).div_ceil(2);
    loop {
        let y = (x + n / x) >> 1;
        if y >= x {
            return x;
        }
        x = y;
    }
}

/// Kepler's third law in integers: `n·(R/R')^{3/2}` for `R' = radius2` (both at most 2^40,
/// `R'` within a factor 2 of `R`), in 2^-62 fixed point. No floats.
pub(crate) fn kepler_n(n: u64, radius: i64, radius2: i64) -> u64 {
    let r = ((radius as u128) << 62) / radius2 as u128;
    let r2 = (r * r) >> 62;
    let r3 = (r2 * r) >> 62;
    let s = isqrt(r3 << 62);
    ((n as u128 * s + (1 << 61)) >> 62) as u64
}

/// The frame's own tube in its parent (exact integers): where the origin (the members'
/// centre of mass) is against the reference circle, and where the circle is against the
/// parent's original rotating axes.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Tube {
    /// The origin's position from the reference point, in the frame's axes: `2^-32` lattice units.
    pub x: [i128; 2],
    /// Its velocity in those axes: `2^-48` lattice units per chronon.
    pub v: [i128; 2],
    /// The reference point's azimuth from the parent's original axes (which turn at `n0`):
    /// radians · `2^60`, the exact sum of `(n − n0)·Δt`.
    pub azimuth: i128,
    /// The tick `x`, `v` and the azimuth are advanced to.
    pub tick: Tick,
    /// The reference circle: radius (lattice units) and mean motion (`n/2^60` rad per chronon).
    pub radius: i64,
    pub n: u64,
    /// The parent's original circle: the frame's genesis.
    pub radius0: i64,
    pub n0: u64,
}

impl Tube {
    fn new(radius: i64, n: u64) -> Tube {
        Tube { x: [0; 2], v: [0; 2], azimuth: 0, tick: 0, radius, n, radius0: radius, n0: n }
    }

    /// Drift to `tick` (exact: `x += v·Δt`, rounded once to `2^-32`) and turn the azimuth.
    pub fn advance_to(&mut self, tick: Tick) {
        let dt = (tick - self.tick) as i128;
        assert!(dt >= 0, "a tube only advances");
        if dt > 0 {
            for c in 0..2 {
                self.x[c] += round_shift(self.v[c] * dt, CARRY_BITS - TUBE_BITS);
            }
            self.azimuth += (self.n as i128 - self.n0 as i128) * dt;
            self.tick = tick;
        }
    }

    /// The tube at a later tick (nothing changes in the frame).
    pub fn at(&self, tick: Tick) -> Tube {
        let mut t = self.clone();
        t.advance_to(tick);
        t
    }

    /// The velocity after one epoch kick (the same law as a member's, in the tube's precision).
    pub(crate) fn kicked_v(&self, w: &Weights) -> [i128; 2] {
        let (cc, ss, gx, gy) = (w.c as i128, w.s as i128, w.gx as i128, w.gy as i128);
        [
            round_shift(cc * self.v[0] + ss * self.v[1], CARRY_BITS) + round_shift(gx * self.x[0], TUBE_BITS),
            round_shift(-ss * self.v[0] + cc * self.v[1], CARRY_BITS) + round_shift(gy * self.x[0], TUBE_BITS),
        ]
    }

    fn absorb(&mut self, centre: [i64; 2], v: [i128; 2]) {
        for c in 0..2 {
            self.x[c] += (centre[c] as i128) << TUBE_BITS;
            self.v[c] += v[c];
        }
    }

    /// `x_c = 4x + 2v_y/n` in `2^-32` lattice units, from the velocity at the tick.
    fn guiding_centre(&self, v_y_at_tick: i128) -> i128 {
        4 * self.x[0] + div_round((2 * v_y_at_tick) << (TUBE_BITS + 12), self.n as i128)
    }

    /// Move the reference circle to `radius2`, `n2` (same azimuth): the origin's `x` loses the
    /// step, and its velocity gains `δn·ẑ×P` with `P` its position from the parent, the steady
    /// shear of the new circle against the old.
    fn rebase(&mut self, radius2: i64, n2: u64) {
        let dn = self.n as i128 - n2 as i128;
        let (px, py) = (((self.radius as i128) << TUBE_BITS) + self.x[0], self.x[1]);
        self.v[0] += round_shift(-dn * py, 60 + TUBE_BITS - CARRY_BITS);
        self.v[1] += round_shift(dn * px, 60 + TUBE_BITS - CARRY_BITS);
        self.x[0] -= ((radius2 - self.radius) as i128) << TUBE_BITS;
        self.radius = radius2;
        self.n = n2;
    }
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
    /// Refuse a frame outside the weak-field rule (`n·R ≤ c/4`), and a circle move that would
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
    /// The reference circle after the event, and whether it moved.
    pub radius: i64,
    pub n: u64,
    pub moved: bool,
    /// The whole event was refused (a velocity past c): nothing changed.
    pub refused: bool,
    /// `Σ m·Δv` over every body, `2^-48` units: `−M·V` plus the (small) frame-change term.
    pub dp: [i128; 2],
}

/// The state of a battle's re-anchoring.
pub(crate) struct Anchoring {
    pub(crate) age_epochs: u64,
    pub(crate) enforce: bool,
    pub(crate) tube: Tube,
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
}

impl Anchoring {
    pub(crate) fn digest_into(&self, h: &mut blake3::Hasher, st: &BattleStats, frame: &Frame, active: &[bool]) {
        let put = |h: &mut blake3::Hasher, v: i128| {
            h.update(&v.to_le_bytes());
        };
        for v in [st.anchors, st.handed_out, st.rebases, st.anchors_refused, st.rebases_refused, self.since, self.hold, self.due as u64] {
            put(h, v as i128);
        }
        put(h, self.pending.map_or(-1, |t| t as i128));
        put(h, frame.radius as i128);
        put(h, frame.n as i128);
        let tube = |h: &mut blake3::Hasher, t: &Tube| {
            for v in [t.x[0], t.x[1], t.v[0], t.v[1], t.azimuth, t.tick as i128, t.radius as i128, t.n as i128] {
                put(h, v);
            }
        };
        tube(h, &self.tube);
        for a in active {
            h.update(&[*a as u8]);
        }
        for ho in &self.handoffs {
            for v in [ho.index as i128, ho.tick as i128, ho.x[0] as i128, ho.x[1] as i128, ho.v[0], ho.v[1]] {
                put(h, v);
            }
            tube(h, &ho.tube);
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

/// The frame change applied to every body: origin `centre` and velocity `vel` (`2^-48`) subtracted, and
/// the change of the axes' rotation `dn` (`2^-60` rad per chronon) as `δn·ẑ×r`.
struct Change {
    centre: [i64; 2],
    vel: [i128; 2],
    dn: i128,
}

fn transform_slice(ch: &Change, motions: &[Motion], carries: &[[i64; 2]], dk: &mut [[i64; 2]], new_carry: &mut [[i64; 2]]) {
    let half = 1i128 << (CARRY_BITS - 1);
    for (((m, c), d), nc) in motions.iter().zip(carries).zip(dk.iter_mut()).zip(new_carry.iter_mut()) {
        let (rx, ry) = ((m.x[0] - ch.centre[0]) as i128, (m.x[1] - ch.centre[1]) as i128);
        // v' = v − V + δn·ẑ×r, one number in 2^-48, then split by rounding to nearest.
        let vx = ((m.k[0] as i128) << CARRY_BITS) + c[0] as i128 - ch.vel[0] - round_shift(ch.dn * ry, 60 - CARRY_BITS);
        let vy = ((m.k[1] as i128) << CARRY_BITS) + c[1] as i128 - ch.vel[1] + round_shift(ch.dn * rx, 60 - CARRY_BITS);
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

/// `Σ m·δv` of the frame change's rotation term over the members in the frame (`2^-48` units):
/// the momentum the change adds, which the tube's velocity absorbs so the members' total stays
/// within half a quantum of zero (the centre is rounded to a lattice unit, so `Σ m·r ≠ 0`).
fn dv_sum_slice(centre: [i64; 2], dn: i128, masses: &[i64], active: &[bool], motions: &[Motion]) -> [i128; 2] {
    let mut s = [0i128; 2];
    for i in 0..masses.len() {
        if !active[i] {
            continue;
        }
        let (rx, ry) = ((motions[i].x[0] - centre[0]) as i128, (motions[i].x[1] - centre[1]) as i128);
        s[0] -= masses[i] as i128 * round_shift(dn * ry, 60 - CARRY_BITS);
        s[1] += masses[i] as i128 * round_shift(dn * rx, 60 - CARRY_BITS);
    }
    s
}

fn par_dv_sum(threads: usize, centre: [i64; 2], dn: i128, masses: &[i64], active: &[bool], motions: &[Motion]) -> [i128; 2] {
    let n = masses.len();
    let t = threads.clamp(1, n.max(1));
    if t == 1 {
        return dv_sum_slice(centre, dn, masses, active, motions);
    }
    let chunk = n.div_ceil(t);
    let mut total = [0i128; 2];
    std::thread::scope(|s| {
        let jobs: Vec<_> = (0..n.div_ceil(chunk))
            .map(|j| {
                let r = j * chunk..((j + 1) * chunk).min(n);
                let (m, a, mo) = (&masses[r.clone()], &active[r.clone()], &motions[r]);
                s.spawn(move || dv_sum_slice(centre, dn, m, a, mo))
            })
            .collect();
        for j in jobs {
            let d = j.join().expect("anchor dv thread");
            total[0] += d[0];
            total[1] += d[1];
        }
    });
    total
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
    par_transform(threads, &Change { centre, vel: velocity, dn: 0 }, motions, carries, &mut dk, &mut nc);
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
            return Err(FrameError(format!("orbit radius {} beyond 2^40 lattice units: the anchor arithmetic is exact up to there", self.frame.radius)));
        }
        let age = if policy.age_epochs == 0 { ((self.frame.period() / self.frame.epoch()) / AGE_DIV).max(1) as u64 } else { policy.age_epochs };
        self.anchoring = Some(Anchoring {
            age_epochs: age,
            enforce: policy.enforce_orbit_rule,
            tube: Tube::new(self.frame.radius, self.frame.n),
            due: true,
            pending: None,
            shift: 0,
            since: 0,
            hold: 0,
            handoffs: Vec::new(),
            scratch: vec![[0; 2]; self.motions.len()],
            last_refusal: None,
            flush: Vec::new(),
        });
        Ok(self)
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

    /// The frame's own tube in its parent, as of its last update (an epoch or an anchor).
    pub fn tube(&self) -> Option<&Tube> {
        self.anchoring.as_ref().map(|a| &a.tube)
    }

    /// The tube advanced to `tick` (nothing changes in the frame).
    pub fn tube_at(&self, tick: Tick) -> Option<Tube> {
        self.tube().map(|t| t.at(tick))
    }

    /// Why the last refused re-anchor was refused (the stepper's reason).
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
    /// scheduled: the caller's own, as in the tests). The tube's guiding centre uses the
    /// staggered lattice velocity as it is there.
    pub fn reanchor(&mut self) -> Result<AnchorReport, FrameError> {
        if self.anchoring.is_none() {
            return Err(FrameError("re-anchoring is off (Battle::with_anchoring)".into()));
        }
        self.do_anchor(None)
    }

    /// Before an epoch's kick: bring the tube to the tick, and re-anchor if one is due.
    pub(crate) fn anchor_epoch(&mut self, weight: Weight) -> Result<(), FrameError> {
        let tick = self.stepper.tick();
        if self.anchoring.is_some() {
            self.settle_position_carries(tick);
        }
        let go = match self.anchoring.as_mut() {
            None => return Ok(()),
            Some(a) => {
                a.tube.advance_to(tick);
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

    /// After an epoch's kick: kick the tube with the same law, count the age, and look at the
    /// certificates (the extent from this epoch's pass over the members).
    pub(crate) fn anchor_certificate(&mut self, weight: Weight, k: &KickStats) {
        let Some(a) = self.anchoring.as_mut() else { return };
        a.tube.v = a.tube.kicked_v(self.frame.weights(weight));
        a.since += 1;
        a.hold = a.hold.saturating_sub(1);
        if a.due || a.pending.is_some() || a.hold > 0 {
            return;
        }
        let r = self.frame.radius as i128;
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

    /// The event. `weight` is `Some` when it runs before an epoch's kick (the motions are then
    /// the epoch's, and are updated in place for the kick that follows), `None` between epochs.
    pub(crate) fn do_anchor(&mut self, weight: Option<Weight>) -> Result<AnchorReport, FrameError> {
        let t_start = Instant::now();
        let tick = self.stepper.tick();
        let n_all = self.motions.len();
        if weight.is_none() {
            self.stepper.motions(&mut self.motions);
            let a = self.anchoring.as_mut().expect("anchoring is on");
            a.tube.advance_to(tick);
            a.pending = None;
        }
        let (radius, n_frame) = (self.frame.radius, self.frame.n);

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
        let (sums, centre, vel) = loop {
            let s = par_sums(self.threads, &self.masses, &active, &self.motions, &self.carries);
            if s.mass == 0 {
                break (s, [0, 0], [0, 0]);
            }
            let (x, v) = centre_of(&s);
            let mut any = false;
            for i in 0..n_all {
                if active[i] {
                    let (dx, dy) = ((self.motions[i].x[0] - x[0]) as i128, (self.motions[i].x[1] - x[1]) as i128);
                    if (dx * dx + dy * dy) << (2 * EXTENT_SHIFT) > radius as i128 * radius as i128 {
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

        // 2. The tube takes the origin's motion: the members' centre of mass, and its velocity (the
        // momentum the recentring took from the members goes, exactly, into it).
        // 3. The circle goes to the tube's guiding centre.
        let a = self.anchoring.as_ref().expect("anchoring is on");
        let mut tube = a.tube.clone();
        let mut circle: Option<(i64, u64, Frame)> = None;
        let mut circle_refused = false;
        if !dissolved {
            tube.absorb(centre, vel);
            let v_y = match weight {
                Some(Weight::Full) => tube.kicked_v(self.frame.weights(Weight::Half))[1],
                _ => tube.v[1],
            };
            let dr = div_round(tube.guiding_centre(v_y), 1i128 << TUBE_BITS);
            if dr != 0 {
                let radius2 = radius as i128 + dr;
                if radius > MAX_RADIUS || radius2 < 1 || radius2 > MAX_RADIUS as i128 || dr.abs() * 32 > radius as i128 {
                    circle_refused = true;
                } else {
                    let n2 = kepler_n(n_frame, radius, radius2 as i64);
                    match self.frame.rebased(radius2 as i64, n2) {
                        Ok(f) if !a.enforce || f.orbit_speed_ok() => circle = Some((radius2 as i64, n2, f)),
                        _ => circle_refused = true,
                    }
                }
            }
        }
        // The rotation term of the frame change adds momentum Σ m·δv; the velocity the tube takes
        // includes it, so the members' total is within half a quantum of zero either way.
        let dn = circle.as_ref().map_or(0, |c| n_frame as i128 - c.1 as i128);
        let mut vel = vel;
        if dn != 0 {
            let dv = par_dv_sum(self.threads, centre, dn, &self.masses, &active, &self.motions);
            vel = [div_round(sums.mv[0] + dv[0], sums.mass), div_round(sums.mv[1] + dv[1], sums.mass)];
            tube = a.tube.clone();
            tube.absorb(centre, vel);
        }

        // 4. New velocities, then the stepper.
        let change = Change { centre, vel, dn };
        let mut scratch = std::mem::take(&mut self.anchoring.as_mut().expect("anchoring is on").scratch);
        scratch.resize(n_all, [0, 0]);
        let mut applied = dissolved;
        let mut refusal = None;
        let t_plan = Instant::now();
        if !dissolved {
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
        let a = self.anchoring.as_mut().expect("anchoring is on");
        if !applied {
            // Refused whole (a velocity past c, or out of range): nothing changed anywhere.
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
        let moved = circle.is_some();
        if let Some((radius2, n2, frame)) = circle {
            tube.rebase(radius2, n2);
            self.frame = frame;
            self.stats.rebases += 1;
        }
        self.stats.rebases_refused += circle_refused as u64;
        for &i in &handed {
            let v = [((self.motions[i].k[0] as i128) << CARRY_BITS) + self.carries[i][0] as i128, ((self.motions[i].k[1] as i128) << CARRY_BITS) + self.carries[i][1] as i128];
            a.handoffs.push(Handoff { index: i, tick, x: self.motions[i].x, v, tube: tube.clone() });
        }
        a.tube = tube;
        a.scratch = scratch;
        a.flush = flush;
        a.since = 0;
        a.due = false;
        self.stats.anchors += 1;
        self.stats.handed_out += handed.len() as u64;
        self.gone += handed.len();
        self.active = active;
        Ok(AnchorReport { tick, centre, velocity: vel, mass: sums.mass, handed_out: handed, radius: self.frame.radius, n: self.frame.n, moved, refused: false, dp })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn integer_square_root() {
        for n in [0u128, 1, 2, 3, 4, 15, 16, 17, 1 << 64, (1 << 64) - 1, (1 << 126) + 12345, u128::MAX] {
            let r = isqrt(n);
            assert!(r * r <= n && (r + 1).checked_mul(r + 1).is_none_or(|s| s > n), "isqrt({n}) = {r}");
        }
    }

    #[test]
    fn keplers_third_law_in_integers() {
        for (n, r, r2) in [(1u64 << 46, 1i64 << 32, (1i64 << 32) + (1 << 24)), (1 << 46, 1 << 32, (1 << 32) - (1 << 26)), (1 << 40, 1 << 40, (1 << 40) + 1), (12345678901, 999_999_937, 1_030_000_003)] {
            let want = n as f64 * (r as f64 / r2 as f64).powf(1.5);
            let got = kepler_n(n, r, r2) as f64;
            assert!((got - want).abs() <= 0.5 + 1e-14 * want, "n {n}: {got} vs {want}");
        }
        assert_eq!(kepler_n(1 << 46, 1 << 32, 1 << 32), 1 << 46);
    }

    #[test]
    fn division_rounds_to_nearest_with_ties_up() {
        assert_eq!((div_round(7, 2), div_round(5, 2), div_round(-5, 2), div_round(-7, 2), div_round(-6, 4), div_round(6, 4)), (4, 3, -2, -3, -1, 2));
    }
}
