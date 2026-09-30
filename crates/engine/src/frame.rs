//! The free-fall frame: a battle as a doll with no central mass (docs/representation.md §1, §3).
//!
//! A [`Frame`] is the freely falling frame of a battle's centre of mass. It orbits a parent
//! mass on a circle of radius `R` with mean motion `n` (radians per chronon). Its members are
//! ordinary `emergent-lattice` bodies (law `es-lattice-relativistic-v1`, contacts unchanged)
//! in frame coordinates: lattice units, origin at the reference point. The parent's own pull
//! is absent, because the frame falls with the bodies (the equivalence principle). What is
//! left is the tide, and this module is the tide as an integer law.
//!
//! # The choice: rotating axes, Clohessy–Wiltshire (Hill) to first order
//!
//! Axes co-rotate with the parent: `x` radial (away from the parent), `y` along the orbit
//! (prograde). With `k` the velocity in these axes, the in-plane equations are
//!
//! ```text
//! dk_x/dt = 3n²·x + 2n·k_y        dk_y/dt = -2n·k_x
//! ```
//!
//! The tide proper is `(3n²·x, 0)`; the rest is the Coriolis term, a rotation of `k` by
//! `-2n` per unit time. This is the system whose closed form Clohessy and Wiltshire gave
//! (1960), which the behaviour test checks. The brief's `(3n²x, -n²y)` is not the planar
//! tide in rotating axes: `-n²·z` belongs to the out-of-plane axis of the 3D problem, which
//! a 2D lattice does not have, and in non-rotating axes the planar tide is `n²·(2x, -y)`
//! turned with the parent's direction (a time-dependent tensor). Rotating axes give
//! constant coefficients, so the whole law is a handful of integers.
//!
//! # The kick: integers at fixed epochs
//!
//! Every `E = 2^e` chronons the frame gives every body a velocity kick, and between kicks
//! the lattice law moves bodies exactly (`x += k` each chronon, contacts included). `E` is
//! fixed by the frame from `n`: the largest power of two with `n·E ≤ 2^-6` (an epoch turns
//! the rotating axes by at most 1/64 rad), so a period is 400 to 800 epochs.
//!
//! The kick is the **exact** solution of the velocity subsystem over the interval `h` with
//! `x` held fixed: `k' = R(φ)·k + (3n/2)·x_r·(sin φ, cos φ − 1)`, `φ = 2n·h`, `R` the
//! rotation `[[cos φ, sin φ], [-sin φ, cos φ]]`. Alternating it with the lattice's exact
//! drift is Strang splitting, second order in `n·E`: the frame starts with a **half kick**
//! (`h = E/2`, at tick 0) and gives a **full kick** (`h = E`) at every later epoch. The
//! lattice velocity `k` is then the velocity at the middle of its interval: it runs E/2
//! chronons ahead of the position, so in a frame whose epoch is comparable to the battle the
//! opening half kick front-loads up to E/2 chronons of tide (a rotation of up to 1/64 rad).
//! That staggering is the scheme's second-order price, not noise. A frame with no parent mass
//! is [`Frame::flat`]: no tide, no kicks, the lattice's own digests (gate B0). `cos φ`, `sin φ`
//! come from an integer Taylor series (no floating point anywhere in the law), so every
//! coefficient is the same on every machine.
//!
//! **Carries.** A body's velocity is `v = k + c/2^48`, with the carry `c ∈ [-2^47, 2^47)`
//! the sub-quantum part (principle 6: influences below one quantum accumulate). A kick maps
//! `v` exactly (48-bit coefficients, no intermediate rounding but one shift) and splits the
//! result again by rounding to nearest. This is error feedback in the pattern of the
//! lattice's `carry` fields (a sigma-delta or Bresenham error term): the velocity error is
//! at most half a quantum at every epoch and never accumulates. The carries live in the
//! frame (`Battle`), not in `Body`: they are frame state, and the tide digest covers them.
//! Rounding to nearest matters: a floor would bias every epoch the same way (a coherent
//! `E/2` lattice units of position error per epoch); rounding makes the error zero-mean
//! (see the noise floor below).
//!
//! A kick that would take a body to `|k| ≥ c` is **refused** for that epoch (velocity and
//! carry stay as they were, and the refusal is counted): the tide is Newtonian and knows
//! nothing of the light cone. Refusals are deterministic, so both orders agree.
//!
//! # Validity: the size rule (first order, and why)
//!
//! The exact radial tide of an inverse-square parent is `3n²x·(1 − x/R + …)`: linearising
//! it drops a relative `x/R`. Two rules follow, and the frame reports them (the integer law is
//! defined for any parameters; a stress scene may leave the physics); a battle with re-anchoring
//! enforces them, refusing a frame outside rule 2 and handing out members outside rule 1:
//!
//! 1. **Extent:** every member stays within `R/32` of the reference (`EXTENT_SHIFT = 5`),
//!    so the tide is off by at most about 3%. See [`Frame::extent_ok`].
//! 2. **Weak field:** the orbit speed `n·R` is at most `c/4`, so the Newtonian tide is not
//!    contradicted by the parent's own field (1PN terms are `O((nR/c)²)`).
//!    See [`Frame::orbit_speed_ok`].
//!
//! Free drift is what breaks rule 1 in time. A body released at rest at radial offset `dr`
//! drifts along the orbit by `12π·dr` per period (the tide shears the frame), so it leaves
//! the `R/32` bound after about `P·(R/dr)/1200`: 0.8 P at `dr/R = 10⁻³`, 0.08 P at `10⁻²`.
//! Measured against the full two-body motion (`tests/behaviour.rs`, RK4 in float), reading (x, y)
//! as Cartesian offsets: the linear model is off by 0.7% after half a period and 2.0% after one
//! at `dr/R = 10⁻³`, by 0.20% after one period at `10⁻⁴`, and by `7.7·dr` (20% of the drift,
//! the red-team's H0203 figure) at `10⁻²`: about `20·dr/R` after one period. Nearly all of it is
//! the reading (see re-anchoring below); `tests/reanchor.rs` measures both.
//!
//! **A valid frame has few epochs.** The radial tide grows like `exp(√3·n·t)`, so a battle
//! that lasts `T` chronons needs `n·T` of about 1 at most, and there are only
//! `T/E ∈ [64·nT, 128·nT)` epochs in it (33 for `nT = 0.5`). The frame is cheap because the
//! physics is slow; a scene with hundreds of epochs is a stress scene.
//!
//! **Noise floor (measured).** The lattice drifts at the integer `k`; the true velocity is
//! `k + c/2^48`, so each epoch leaves a position error of up to `E/2` units. That error
//! random-walks the guiding centre `x_c = 4x + 2v_y/n` (a constant of the linear motion), and
//! the shear turns an error `δ` of `x_c` into an along-track drift of `3nδ/2` per chronon:
//! after `t` chronons about `1.7·n·√E·t^1.5` units (`tests/behaviour.rs`: 0.003 dr after one
//! period, 333 dr after a thousand, at the estimate). It is the tide amplifying a
//! sub-quantum error, not a compounding of the law's, and it is far below the linear model's
//! own error inside a frame's life; it is also what re-anchoring resets. Dithering the
//! velocity inside an epoch (two kick events per epoch instead of one) would cut the
//! position error per epoch from `E/2` units to one, at twice the kick events.
//!
//! **Re-anchoring** is built in [`crate::anchor`] (opt in with [`Battle::with_anchoring`]). The
//! obvious sketch (`x' = x − X`, `k'_y = k_y + 3nX/2`, `n` unchanged) would change nothing physical
//! in a linear system, and the 2% above is mostly the Cartesian reading of the along-track arc
//! (the orbit's curvature, `x ≈ −y²/2R`), not the tide: read as an arc, this fixed linear law is
//! within 0.84% of the two-body motion for ten periods, and what it lacks is axes that turn with
//! the group. Re-anchoring moves the origin to the members' centre of mass, the reference circle
//! to the tube's guiding centre (`R' = R + x_c`, `n' = n·(R/R')^{3/2}`), pays each body's dropped
//! sub-quantum drift into its position (the noise floor above restarts at every anchor), and hands
//! out members beyond the size rule. It is also where the two rules are enforced.
//!
//! # The two orders
//!
//! [`Battle`] runs any [`Kickable`] stepper: lockstep (`Chronon`) or sparse (`EventCore`).
//! The epoch kicks are the frame's own events, at ticks `j·E`: the stepper commits its tick,
//! the frame reads every body's motion, computes the kicks (pure per body; the pass may be
//! chunked over threads and gives the same bits), and hands them back through the hook. Bodies
//! whose velocity changes revise (`rev + 1`), so the lattice's consumed-contact rule applies
//! unchanged. The sparse order treats an epoch as a scheduled event: the core advances to it
//! (`advance(target = epoch tick)`), then re-homes and re-predicts the kicked bodies. Both
//! orders produce identical world, log and tide digests ([`Outcome`]).
use emergent_lattice::law::{Tick, MAX_Q};
use emergent_lattice::{Kickable, Motion};
use std::time::Instant;

/// Fraction bits of the carry and of every kick coefficient.
pub const CARRY_BITS: u32 = 48;
/// Mean motion is stored as `n = N / 2^60` radians per chronon.
pub const N_BITS: u32 = 60;
/// 2π·2^60, rounded: the mean motion of a period of `P` chronons is `TWO_PI_N / P`.
pub const TWO_PI_N: u64 = 7_244_019_458_077_122_842;
/// An epoch turns the axes by at most `2^-EPOCH_ANGLE_LOG2` radians.
pub const EPOCH_ANGLE_LOG2: u32 = 6;
/// Extent rule: members within `R / 2^EXTENT_SHIFT` of the reference.
pub const EXTENT_SHIFT: u32 = 5;
/// Weak-field rule: the orbit speed `n·R` is at most `c / ORBIT_SPEED_DIV`.
pub const ORBIT_SPEED_DIV: u128 = 4;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FrameError(pub String);

impl std::fmt::Display for FrameError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.0)
    }
}
impl std::error::Error for FrameError {}

/// The 2×2 rotation and the tide vector of one kick, scaled by 2^48.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) struct Weights {
    /// cos φ and sin φ.
    pub(crate) c: i64,
    pub(crate) s: i64,
    /// (3n/2)·(sin φ, cos φ − 1): the velocity per unit of radial offset.
    pub(crate) gx: i64,
    pub(crate) gy: i64,
}

/// Which interval a kick integrates: the opening half kick or a full epoch.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Weight {
    Half,
    Full,
}

/// Bodies kicked and kicks refused (a kick to `|k| ≥ c`), and the largest `|x|²` seen.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct KickStats {
    pub changed: u64,
    pub refused: u64,
    pub max_r2: i128,
}

impl KickStats {
    fn merge(&mut self, o: KickStats) {
        self.changed += o.changed;
        self.refused += o.refused;
        self.max_r2 = self.max_r2.max(o.max_r2);
    }
}

/// The frame's law: mean motion, its epoch and the integer kick coefficients.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Frame {
    pub(crate) q: i64,
    pub(crate) radius: i64,
    pub(crate) n: u64,
    pub(crate) e: u32,
    pub(crate) full: Weights,
    pub(crate) half: Weights,
}

/// sin φ and cos φ − 1 for φ = `phi` / 2^64 (φ < 2^-4), in 2^64 fixed point, by Taylor series
/// in integers: no floating point, so the same bits on every machine.
fn sin_cosm1(phi: u128) -> (i128, i128) {
    let p2 = (phi * phi) >> 64;
    let (mut s, mut term, mut k) = (0i128, phi, 0u128);
    while term > 0 {
        s += if k % 2 == 0 { term as i128 } else { -(term as i128) };
        term = ((term * p2) >> 64) / ((2 * k + 2) * (2 * k + 3));
        k += 1;
    }
    let (mut cm1, mut term, mut k) = (0i128, p2 / 2, 1u128);
    while term > 0 {
        cm1 += if k % 2 == 1 { -(term as i128) } else { term as i128 };
        term = ((term * p2) >> 64) / ((2 * k + 1) * (2 * k + 2));
        k += 1;
    }
    (s, cm1)
}

/// Round `v / 2^sh` to nearest (ties up).
pub(crate) fn round_shift(v: i128, sh: u32) -> i128 {
    (v + (1i128 << (sh - 1))) >> sh
}

/// The coefficients of a kick over `h` chronons, φ = 2n·h, for `n = n/2^60`, `E = 2^e`.
fn weights(n: u64, e: u32, half: bool) -> Weights {
    // n·E·2^64 = n·2^(e+4); φ = 2nE for a full kick, nE for a half kick.
    let th = (n as u128) << (e + 4);
    let phi = if half { th } else { 2 * th };
    let (s, cm1) = sin_cosm1(phi);
    let n64 = (n as i128) << 4; // n·2^64
    Weights {
        c: ((1i128 << CARRY_BITS) + round_shift(cm1, 64 - CARRY_BITS)) as i64,
        s: round_shift(s, 64 - CARRY_BITS) as i64,
        gx: round_shift(3 * n64 * s / 2, 128 - CARRY_BITS) as i64,
        gy: round_shift(3 * n64 * cm1 / 2, 128 - CARRY_BITS) as i64,
    }
}

/// One slice of bodies: kick each and update its carry. `active` is empty (every body is in
/// the frame) or one flag per body; a body handed out of the frame is left alone.
fn kick_slice(w: &Weights, q2: i128, motions: &[Motion], carries: &mut [[i64; 2]], dk: &mut [[i64; 2]], active: &[bool]) -> KickStats {
    let half = 1i128 << (CARRY_BITS - 1);
    let (cc, ss, gx, gy) = (w.c as i128, w.s as i128, w.gx as i128, w.gy as i128);
    let mut st = KickStats::default();
    for (i, ((m, c), d)) in motions.iter().zip(carries.iter_mut()).zip(dk.iter_mut()).enumerate() {
        if !active.is_empty() && !active[i] {
            *d = [0, 0];
            continue;
        }
        let (x, k) = (m.x, m.k);
        st.max_r2 = st.max_r2.max(x[0] as i128 * x[0] as i128 + x[1] as i128 * x[1] as i128);
        let (kx, ky, cx, cy, xr) = (k[0] as i128, k[1] as i128, c[0] as i128, c[1] as i128, x[0] as i128);
        // v' = R·v + G·x_r, in 2^48 fixed point, with v = k + c/2^48.
        let rx = cc * kx + ss * ky + ((cc * cx + ss * cy + half) >> CARRY_BITS) + gx * xr;
        let ry = -ss * kx + cc * ky + ((-ss * cx + cc * cy + half) >> CARRY_BITS) + gy * xr;
        let (nx, ny) = ((rx + half) >> CARRY_BITS, (ry + half) >> CARRY_BITS);
        if nx * nx + ny * ny >= q2 {
            st.refused += 1;
            *d = [0, 0];
            continue;
        }
        *d = [(nx - kx) as i64, (ny - ky) as i64];
        *c = [(rx - (nx << CARRY_BITS)) as i64, (ry - (ny << CARRY_BITS)) as i64];
        st.changed += (*d != [0, 0]) as u64;
    }
    st
}

impl Frame {
    /// A frame of mean motion `n / 2^60` radians per chronon at orbit radius `radius` (lattice
    /// units), for a lattice of quantum `q`. Fails when the epoch would be shorter than one
    /// chronon (`n > 2^-6`).
    pub fn new(q: i64, radius: i64, n: u64) -> Result<Frame, FrameError> {
        if !(1..=MAX_Q).contains(&q) {
            return Err(FrameError(format!("quantum {q} outside [1, 2^20]")));
        }
        if radius < 1 {
            return Err(FrameError(format!("orbit radius {radius} below one lattice unit")));
        }
        let cap = 1u64 << (N_BITS - EPOCH_ANGLE_LOG2);
        if n == 0 || n > cap {
            return Err(FrameError(format!("mean motion {n}/2^60 outside [1, 2^54]: the epoch would be shorter than a chronon")));
        }
        let mut e = 0;
        while (n << (e + 1)) <= cap {
            e += 1;
        }
        Ok(Frame { q, radius, n, e, full: weights(n, e, false), half: weights(n, e, true) })
    }

    /// No parent mass, so no tide: a flat frame never kicks, and the lattice runs as it is
    /// (gate B0: the digests are the lattice's own).
    pub fn flat(q: i64) -> Result<Frame, FrameError> {
        if !(1..=MAX_Q).contains(&q) {
            return Err(FrameError(format!("quantum {q} outside [1, 2^20]")));
        }
        let zero = Weights { c: 1 << CARRY_BITS, s: 0, gx: 0, gy: 0 };
        Ok(Frame { q, radius: i64::MAX, n: 0, e: 0, full: zero, half: zero })
    }

    /// A frame whose orbit takes `period` chronons (`n = 2π/period`).
    pub fn from_period(q: i64, radius: i64, period: Tick) -> Result<Frame, FrameError> {
        if period < 1 {
            return Err(FrameError(format!("period {period} below one chronon")));
        }
        Frame::new(q, radius, TWO_PI_N / period as u64)
    }

    /// Planted law for tests: the tide's sign multiplied by `sign` (−1 reverses it), the
    /// Coriolis rotation untouched.
    pub fn planted_tide_sign(mut self, sign: i64) -> Frame {
        for w in [&mut self.full, &mut self.half] {
            w.gx *= sign;
            w.gy *= sign;
        }
        self
    }

    /// The epoch: chronons between kicks, a power of two (never, for a flat frame).
    pub fn epoch(&self) -> Tick {
        if self.n == 0 {
            Tick::MAX
        } else {
            1 << self.e
        }
    }

    pub fn epoch_log2(&self) -> u32 {
        self.e
    }

    /// The mean motion as stored: `n / 2^60` radians per chronon.
    pub fn n(&self) -> u64 {
        self.n
    }

    /// The mean motion in radians per chronon (a float, for reporting and float checks only).
    pub fn n_f64(&self) -> f64 {
        self.n as f64 / (1u64 << N_BITS) as f64
    }

    /// The orbit period, in chronons (rounded down; never, for a flat frame).
    pub fn period(&self) -> Tick {
        (TWO_PI_N.checked_div(self.n).unwrap_or(i64::MAX as u64)) as Tick
    }

    pub fn radius(&self) -> i64 {
        self.radius
    }

    pub fn q(&self) -> i64 {
        self.q
    }

    /// Weak-field rule: `n·R ≤ c/4`, exactly (`c = Q` lattice units per chronon).
    pub fn orbit_speed_ok(&self) -> bool {
        self.n as u128 * self.radius as u128 * ORBIT_SPEED_DIV <= (self.q as u128) << N_BITS
    }

    /// Extent rule: `|x|² ≤ (R/2^5)²` for the largest `|x|²` a run saw (`BattleStats::max_r2`).
    pub fn extent_ok(&self, max_r2: i128) -> bool {
        max_r2 << (2 * EXTENT_SHIFT) <= self.radius as i128 * self.radius as i128
    }

    pub(crate) fn weights(&self, w: Weight) -> &Weights {
        match w {
            Weight::Half => &self.half,
            Weight::Full => &self.full,
        }
    }

    /// The kick of every body at one epoch: `dk[i]` for body i, its carry updated. Pure per
    /// body, so the result does not depend on `threads` (chunks are contiguous slices).
    pub fn kick_all(&self, weight: Weight, motions: &[Motion], carries: &mut [[i64; 2]], dk: &mut [[i64; 2]], threads: usize) -> KickStats {
        self.kick_all_masked(weight, &[], motions, carries, dk, threads)
    }

    /// [`Frame::kick_all`] for the members still in the frame: `active` is empty (all of them)
    /// or one flag per body, and a body handed out (false) is neither kicked nor counted.
    pub fn kick_all_masked(&self, weight: Weight, active: &[bool], motions: &[Motion], carries: &mut [[i64; 2]], dk: &mut [[i64; 2]], threads: usize) -> KickStats {
        let (w, q2, n) = (*self.weights(weight), self.q as i128 * self.q as i128, motions.len());
        assert!(carries.len() == n && dk.len() == n, "one carry and one kick per body");
        assert!(active.is_empty() || active.len() == n, "one flag per body");
        let t = threads.clamp(1, n.max(1));
        if t == 1 {
            return kick_slice(&w, q2, motions, carries, dk, active);
        }
        let chunk = n.div_ceil(t);
        let mut total = KickStats::default();
        std::thread::scope(|s| {
            let jobs: Vec<_> = motions
                .chunks(chunk)
                .zip(carries.chunks_mut(chunk))
                .zip(dk.chunks_mut(chunk))
                .enumerate()
                .map(|(j, ((m, c), d))| {
                    let a = if active.is_empty() { active } else { &active[j * chunk..(j * chunk + m.len())] };
                    s.spawn(move || kick_slice(&w, q2, m, c, d, a))
                })
                .collect();
            for j in jobs {
                total.merge(j.join().expect("kick thread"));
            }
        });
        total
    }

    /// The same law about another circle of the parent: radius `radius` and mean motion `n`,
    /// with the epoch kept (the epoch grid is the frame's clock: it does not move when the
    /// reference circle does). Fails when the epoch would turn the axes by more than 2^-5 rad.
    pub fn rebased(&self, radius: i64, n: u64) -> Result<Frame, FrameError> {
        if self.n == 0 {
            return Err(FrameError("a flat frame has no circle to move".into()));
        }
        if radius < 1 {
            return Err(FrameError(format!("orbit radius {radius} below one lattice unit")));
        }
        if n == 0 || (n as u128) << self.e > 1u128 << (N_BITS - EPOCH_ANGLE_LOG2 + 1) {
            return Err(FrameError(format!("mean motion {n}/2^60 turns the axes by more than 2^-5 rad in an epoch of 2^{}", self.e)));
        }
        Ok(Frame { radius, n, full: weights(n, self.e, false), half: weights(n, self.e, true), ..self.clone() })
    }

    /// No parent mass: never kicks (see [`Frame::flat`]).
    pub fn is_flat(&self) -> bool {
        self.n == 0
    }
}

/// Counters and timings of a [`Battle`]. Timings are wall time inside the epoch kicks only
/// (the re-anchors have their own).
#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct BattleStats {
    pub epochs: u64,
    /// Body-kicks that changed a lattice velocity.
    pub changed: u64,
    pub refused: u64,
    /// Largest |x|² any member had at an epoch (for [`Frame::extent_ok`]).
    pub max_r2: i128,
    /// Reading the bodies' motions, computing the kicks (and the extent), and applying them.
    pub read_ns: u64,
    pub frame_ns: u64,
    pub apply_ns: u64,
    /// Re-anchors done, members handed out of the frame (the size rule), reference circles
    /// moved, and anchors or circle moves refused (see [`crate::anchor`]).
    pub anchors: u64,
    pub handed_out: u64,
    pub rebases: u64,
    pub anchors_refused: u64,
    pub rebases_refused: u64,
    /// Wall time in re-anchors: planning (centre of mass, leavers, new velocities), and the
    /// stepper's `rebase`.
    pub anchor_plan_ns: u64,
    pub anchor_apply_ns: u64,
}

/// The canonical outcome of a run: the world and log digests of the lattice law, and the
/// tide digest (the frame's law, carries, epochs, counters; with re-anchoring also the tube, the circle, who
/// left and the hand-off records).
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Outcome {
    pub world: String,
    pub log: String,
    pub tide: String,
}

/// A stepper (lockstep `Chronon` or sparse `EventCore`, through [`Kickable`]) inside a frame:
/// the epoch kicks are the frame's events, run at ticks `j·E` (`j = 0` half weight). With
/// [`Battle::with_anchoring`] the frame also re-anchors (see [`crate::anchor`]).
pub struct Battle<S: Kickable> {
    pub(crate) stepper: S,
    pub(crate) frame: Frame,
    pub(crate) carries: Vec<[i64; 2]>,
    pub(crate) next: u64,
    pub(crate) shift: Tick,
    pub(crate) threads: usize,
    pub(crate) motions: Vec<Motion>,
    pub(crate) dk: Vec<[i64; 2]>,
    pub(crate) stats: BattleStats,
    /// Masses (the weights of the centre of mass), read once: bodies are a fixed set.
    pub(crate) masses: Vec<i64>,
    /// One flag per body: false once handed out of the frame (never true again).
    pub(crate) active: Vec<bool>,
    pub(crate) gone: usize,
    pub(crate) anchoring: Option<crate::anchor::Anchoring>,
    /// The sub-quantum drift owed to each position (`2^-48` lattice units), and the tick it is settled to (re-anchoring only).
    pub(crate) pcarry: Vec<[i128; 2]>,
    pub(crate) ptick: Tick,
}

impl<S: Kickable> Battle<S> {
    /// `threads` only chunks the kick pass; the steppers themselves are single-threaded.
    pub fn new(stepper: S, frame: Frame, threads: usize) -> Self {
        let mut motions = Vec::new();
        stepper.motions(&mut motions);
        let mut masses = Vec::new();
        stepper.masses(&mut masses);
        let n = motions.len();
        Battle {
            stepper,
            frame,
            carries: vec![[0, 0]; n],
            next: 0,
            shift: 0,
            threads,
            motions,
            dk: vec![[0, 0]; n],
            stats: BattleStats::default(),
            masses,
            active: vec![true; n],
            gone: 0,
            anchoring: None,
            pcarry: vec![[0; 2]; n],
            ptick: 0,
        }
    }

    /// Planted law for tests: every epoch kick is applied `shift` chronons late.
    pub fn with_epoch_shift(mut self, shift: Tick) -> Self {
        assert!(shift >= 0, "kicks cannot be early");
        self.shift = shift;
        self
    }

    pub fn stepper(&self) -> &S {
        &self.stepper
    }

    pub fn frame(&self) -> &Frame {
        &self.frame
    }

    pub fn stats(&self) -> &BattleStats {
        &self.stats
    }

    /// Every body's carry, in id order: `|c| ≤ 2^47` always.
    pub fn carries(&self) -> &[[i64; 2]] {
        &self.carries
    }

    /// One flag per body (id order): false for a member handed out of the frame.
    pub fn active(&self) -> &[bool] {
        &self.active
    }

    /// The tick of the next epoch kick.
    pub fn next_epoch_tick(&self) -> Option<Tick> {
        if self.frame.n == 0 {
            return None;
        }
        let e = self.frame.epoch();
        i64::try_from(self.next).ok()?.checked_mul(e)?.checked_add(self.shift)
    }

    /// Run to `horizon`: every event at a tick ≤ `horizon`, in order (epoch kicks, and a
    /// re-anchor pending past its epoch), each after the stepper has committed its tick.
    /// Horizons may only grow.
    pub fn run_to(&mut self, horizon: Tick) -> Result<(), FrameError> {
        loop {
            let epoch = self.next_epoch_tick().filter(|&t| t <= horizon);
            let anchor = self.pending_anchor().filter(|&t| t <= horizon);
            if let Some(a) = anchor.filter(|&a| epoch.is_none_or(|e| a < e)) {
                self.stepper.run_to(a);
                self.do_anchor(None)?;
                continue;
            }
            let Some(at) = epoch else { break };
            self.stepper.run_to(at);
            self.epoch_kick(if self.next == 0 { Weight::Half } else { Weight::Full })?;
            self.next += 1;
        }
        self.stepper.run_to(horizon);
        Ok(())
    }

    fn epoch_kick(&mut self, weight: Weight) -> Result<(), FrameError> {
        let t0 = Instant::now();
        self.stepper.motions(&mut self.motions);
        let t1 = Instant::now();
        self.anchor_epoch(weight)?;
        let t2 = Instant::now();
        let mask: &[bool] = if self.gone > 0 { &self.active } else { &[] };
        let k = self.frame.kick_all_masked(weight, mask, &self.motions, &mut self.carries, &mut self.dk, self.threads);
        let t3 = Instant::now();
        self.stepper.kick(&self.dk).map_err(|e| FrameError(e.0))?;
        let t4 = Instant::now();
        let s = &mut self.stats;
        s.epochs += 1;
        s.changed += k.changed;
        s.refused += k.refused;
        s.max_r2 = s.max_r2.max(k.max_r2);
        s.read_ns += (t1 - t0).as_nanos() as u64;
        s.frame_ns += (t3 - t2).as_nanos() as u64;
        s.apply_ns += (t4 - t3).as_nanos() as u64;
        self.anchor_certificate(weight, &k);
        Ok(())
    }

    pub fn outcome(&self) -> Outcome {
        let (world, log) = self.stepper.outcome();
        let mut h = blake3::Hasher::new();
        h.update(if self.anchoring.is_some() { b"es-frame-tide-v1" } else { b"es-frame-tide-v0" });
        // The frame's own law decides the future (the next kick's tick and weights), so it is
        // part of the state: two frames that differ only in it must not share a digest (E7).
        let f = &self.frame;
        for v in [f.q as i128, f.radius as i128, f.n as i128, f.e as i128, self.shift as i128] {
            h.update(&v.to_le_bytes());
        }
        for v in [self.next, self.stats.changed, self.stats.refused] {
            h.update(&v.to_le_bytes());
        }
        for c in &self.carries {
            h.update(&c[0].to_le_bytes());
            h.update(&c[1].to_le_bytes());
        }
        if let Some(a) = &self.anchoring {
            a.digest_into(&mut h, &self.stats, &self.frame, &self.active);
            for p in &self.pcarry {
                h.update(&p[0].to_le_bytes());
                h.update(&p[1].to_le_bytes());
            }
            h.update(&self.ptick.to_le_bytes());
        }
        Outcome { world, log, tide: h.finalize().to_hex().to_string() }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn integer_trig_matches_the_platform() {
        for phi in [1e-9, 1e-4, 0.01, 1.0 / 64.0, 1.0 / 32.0, 0.0624] {
            let p = (phi * 2f64.powi(64)) as u128;
            let phi = p as f64 / 2f64.powi(64);
            let (s, cm1) = sin_cosm1(p);
            let (s, cm1) = (s as f64 / 2f64.powi(64), cm1 as f64 / 2f64.powi(64));
            assert!((s - phi.sin()).abs() < 2e-18 + 4e-16 * phi, "sin {phi}: {s} vs {}", phi.sin());
            // cos φ − 1 = −2 sin²(φ/2): the platform's cos φ − 1 cancels.
            let want = -2.0 * (phi / 2.0).sin().powi(2);
            assert!((cm1 - want).abs() < 2e-18 + 4e-16 * phi * phi, "cos-1 {phi}: {cm1} vs {want}");
        }
    }

    #[test]
    fn epoch_is_the_largest_power_of_two_under_the_angle() {
        for n in [1u64, 3, 1 << 20, 1 << 46, (1 << 46) + 1, (1 << 54) - 1, 1 << 54] {
            let f = Frame::new(1024, 1 << 30, n).unwrap();
            let cap = 1u64 << 54;
            assert!((n as u128) << f.epoch_log2() <= cap as u128, "n {n}: E too long");
            assert!((n as u128) << (f.epoch_log2() + 1) > cap as u128, "n {n}: E could be doubled");
        }
        assert!(Frame::new(1024, 1 << 30, (1 << 54) + 1).is_err());
        assert!(Frame::new(1024, 1 << 30, 0).is_err());
    }

    #[test]
    fn coefficients_follow_the_closed_form() {
        let f = Frame::new(1 << 20, 1 << 40, 1 << 46).unwrap();
        let n = f.n_f64();
        let e = f.epoch() as f64;
        for (w, phi) in [(&f.full, 2.0 * n * e), (&f.half, n * e)] {
            let sc = (1u64 << CARRY_BITS) as f64;
            assert!((w.c as f64 / sc - phi.cos()).abs() < 1e-14);
            assert!((w.s as f64 / sc - phi.sin()).abs() < 1e-14);
            assert!(((w.gx as f64 / sc) / (1.5 * n * phi.sin()) - 1.0).abs() < 1e-6);
            assert!(((w.gy as f64 / sc) / (1.5 * n * (phi.cos() - 1.0)) - 1.0).abs() < 1e-4);
        }
    }

    #[test]
    fn kicks_do_not_depend_on_threads_and_the_carry_stays_in_range() {
        let f = Frame::new(1 << 10, 1 << 34, 1 << 40).unwrap();
        let motions: Vec<Motion> = (0..1001i64)
            .map(|i| Motion { x: [(i - 500) * 40_009, (i * 7919) % 100_003 - 50_000], k: [(i % 61) - 30, (i % 43) - 21] })
            .collect();
        let run = |threads: usize| {
            let (mut c, mut d) = (vec![[0i64; 2]; motions.len()], vec![[0i64; 2]; motions.len()]);
            let mut st = KickStats::default();
            for w in [Weight::Half, Weight::Full, Weight::Full] {
                st = f.kick_all(w, &motions, &mut c, &mut d, threads);
            }
            (c, d, st)
        };
        let base = run(1);
        assert!(base.2.changed > 0);
        for t in [2, 4, 8, 64] {
            assert_eq!(run(t), base, "threads {t}");
        }
        assert!(base.0.iter().flatten().all(|&c| (-(1i64 << 47)..(1i64 << 47)).contains(&c)));
    }
}
