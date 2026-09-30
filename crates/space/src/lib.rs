//! Integer Binet generator, `space-binet16-generator-v2`.
//! A cycle is the canonical object; its rounded return is not the next initial state.
//!
//! # Representation
//! G=c=M=1; another static mass uses M as its length and time unit. In band k,
//! r edges are 2^(k/16); the actual reciprocal edges are the immutable Q30 table
//! in `bands.rs`, shifted by the octave. Centres use k+1/2. Tables are generated
//! with 90-digit Decimal arithmetic in `tests/tables.py`. Leading-zero count
//! gives the octave; comparison with sixteen entries gives the band. m=16 only.
//! U,V are signed 32-bit words representing (u,u')=(U,V)*2^exponent. At entry,
//! the band's shared exponent puts max(u,|u'|,u_hi) in [2^27,2^28) words, leaving
//! headroom for the shears. Changing that exponent rounds both coordinates;
//! **this boundary conversion is not reversible**. Canonical E is unsigned Q48,
//! L is Q32, angle is Q30 and accumulated t,tau are Q20. Quantities needing more
//! than one word are explicit pairs of u32. Wide temporaries, roots and divisions
//! occur only during creation; Map::apply/inverse use i64 products of i32 words.
//! The supported input envelope is 0<E<=16, 1/4<=L<=4096, 2<r, with checked
//! range errors. Darwin input p is Q16, e Q30, 6+2e<p<=8192 and 0<=e<1.
//!
//! # Initialization and rounding
//! Darwin input gives L²=p²/(p-3-e²) and E²=((p-2)²-4e²)/(p*(p-3-e²)), evaluated
//! with sixteen guard bits for E² before its Q48 square root; integer square
//! roots floor their nonnegative radicands. The periapsis
//! is the upper bound root of R(u)=(E²-1)/L²+2u/L²-u²+2u³. Its bracket is between
//! (1-sqrt(1-12/L²))/6 and (1+sqrt(1-12/L²))/6, bisected to one Q48 unit. Invalid
//! brackets return NoBoundOrbit outside the local-cell rule below.
//! `rnd(x,d)` rounds to nearest with ties away from zero; shifts into a coarser
//! word use rnd. Ordinary signed integer divisions in initialization truncate
//! toward zero; interval bounds instead use floor/ceiling. A shift, coefficient
//! or state that cannot be represented returns Range; none wraps or saturates.
//! Float input/output conversion exists only in the adapter and diagnostics.
//!
//! # Small excursions and circular limit
//! First find C=(1-sqrt(1-12/L²))/6. If the upper energy-root amplitude A obeys
//! A/C<=1/32, use one orbit-centred cell: u=C+A*cos(w*phi), w²=1-6C. Physical
//! band edges inside this cell cause no change of generator. E² and the effective
//! potential (1-2u)(1+L²u²) are compared in Q64. A potential minimum within one
//! input E quantum plus eight Q64 arithmetic units uses A=0 (epicyclic limit).
//! This also defines a radial period for an exactly circular orbit. A smaller
//! energy returns NoBoundOrbit. The root and w are floored integer square roots.
//! Put D=sqrt(C²-A²), B=sqrt((1-2C)²-4A²). Round phi=2*pi/w to Q30, using
//! 2*pi=6746518852/2^30. Mean rates are tau=C/(L*D³) and
//! t=E*(C/(L*D³)+2/(L*D)+4/(L*B)); these follow by partial fractions and the
//! elementary cosine integrals. Round rates and final periods to Q20. The cell
//! stores C,A,w as word pairs and needs no band-crossing records. This explicitly
//! changes the band-centred law in the small-excursion regime; the old m16 float
//! regression still tests the band compiler, while a separate GR sweep tests it.
//!
//! # In-band map: the integer algorithm
//! Let w2=1-6*u_k and f=1/L²-3*u_k² (light drops 1/L²). Each full step is h=1/4
//! radian; an event can shorten it to an integer H in Q30, 1<=H<=2^28. Put
//! x=w2*H². In Q60, evaluate by Horner, rounding every multiply and rational
//! coefficient to nearest:
//!
//! ```text
//! a = H/2 * (1+x/12+x²/120+17x³/20160+31x⁴/362880+691x⁵/79833600)
//! b = H   * (1-x/6+x²/120-x³/5040+x⁴/362880-x⁵/39916800)
//! A = round(a*2^30); K = round(w2*b*2^30); J = round(f*b/2^exponent)
//! U1 = U + round(A*V / 2^30)
//! V1 = V - round(K*U1 / 2^30) + J
//! U2 = U1 + round(A*V1 / 2^30)
//! ```
//!
//! Reverse the three assignments, subtracting the increments, to recover all
//! input bits. Each shear is a permutation of integer lattice sites (exact
//! counting-area preservation). Its unrounded affine determinant is one.
//! a approximates tan(wH/2)/w and b sin(wH)/w. For w2<0 these same polynomials
//! approximate tanh(lambda H/2)/lambda and sinh(lambda H)/lambda. There is no
//! division by w2 at the transition. The affine map's angle is acos(1-A*K/2^60)
//! when 0<A*K/2^60<4; rounding state words introduces an additional ripple.
//! Area preservation does NOT imply exact energy conservation or radial closure.
//!
//! # Exact integer event search
//! Search H=1..2^28 for the FIRST outgoing edge or velocity-sign event. Outgoing
//! means U<=u_lo,V<0 or U>=u_hi,V>0. At entry reblocking may displace U by half a
//! new quantum; the edge behind the motion is not an exit. Velocity sign events
//! use V<0 to V>=0 (apo) or V>0 to V<=0 (peri). No state is snapped at an event.
//! Coefficients are monotone over H<=1/4, |w2|<=2. Interval endpoint arithmetic
//! encloses the three shears. A second enclosure retains the common b factor
//! in b*(f-w2*U1), with six outward word units covering coefficient/product
//! rounding; intersecting the enclosures tightens circular cases. Empty event
//! intervals are excluded; left intervals are searched first; singleton integer
//! predicates alone accept events. Thus earlier lattice hits cannot be skipped
//! even when rounded predicates are nonmonotone. 131072 search nodes or 300000
//! accepted steps exhaust the creation budget and return Budget, not an answer.
//!
//! # Time, light and records
//! For each accepted interval use eight-point Gauss-Legendre quadrature, with
//! nodes/weights in the same Decimal-generated Q30 table. Each node's integer H
//! is rounded once; u there is this same three-shear map from the interval start.
//! Round rates to Q20: dt/dphi=E/(L*u²*(1-2u)), dtau/dphi=1/(L*u²). Products for
//! u² and L*u² are truncated at Q48; accumulate weighted rates with i128 and
//! round the interval increments to Q20. Light tracing currently returns angle
//! only, with E=1 and L=b required. Its exterior tail uses 256 integer Simpson panels from u=0 to 1/10000
//! on 1/sqrt(1/b²-u²+2u³). Absorption is exactly u>=1/2. Horizon time is undefined.
//! The record contains crossings, integer increments, extrema, work and return
//! state. Memo keys are exactly (E,L), not nearby floats. The next cycle starts
//! at the same invariant-derived periapsis. The rounded return is diagnostic,
//! so the shape and increments repeat exactly. First differences in E,L
//! are stored as signed word pairs over explicit key steps, rejecting changed
//! crossing sequences. Their multiply-add is only a predictor: an exact kick
//! requires recompilation. A discrete, branching function has no global tangent.
//!
//! # Error bound and its limits
//! For one accepted fixed-band map let q=2^exponent, a=A/2^30, k=K/2^30. Against
//! the unrounded coefficient map, |delta u'|<=(1+|k|)*q/2 and
//! |delta u|<=[2+|a|(1+|k|)]*q/2. These follow by propagating the half-quantum
//! error of each shear. For |w2|<=2,H<=1/4, tan/tanh's first omitted term and
//! the geometric majorant of its tail bound a's truncation by 5e-13. The omitted
//! sin/sinh tail bounds b by 2e-16. Q60 Horner arithmetic adds less than 1e-17.
//! Hence each Q30 coefficient differs from exact oscillator flow by at most
//! 2^-31+5.1e-13; J adds q/2+|f|*3e-16. The centre table adds
//! delta<=2^(-31-octave) in u_k and force error <=6*|u-u_k|*delta+3*delta²;
//! initialization/Q48 truncation is separate. Reblocking adds <=q_new/2.
//! Conditional on a fixed event sequence, e_next<=|M|*e+d composes these local
//! bounds (M is the absolute shear matrix; d propagates the stated errors).
//! **No unconditional orbit, event-time or clock-quadrature bound is proved.**
//! The independent 262-case regression uses angle error<=2e-4 rad, relative
//! periods<=5e-4, relative turning radii<=2e-4 and equal crossing counts. Those
//! are measured checks, not a global error certificate. Global continuum bounds
//! and exact kick updates require separate qualification.

mod bands;
mod local;
#[cfg(feature = "profile")]
pub mod profile;
pub use local::LocalOscillator;
use std::collections::BTreeMap;
use std::sync::Arc;

const Q30: i64 = 1 << 30;
const Q48: i128 = 1 << 48;
pub const STEP: u32 = 1 << 28;
pub const MAX_STEPS: usize = 300_000;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Error {
    Range,
    NoBoundOrbit,
    Budget,
    Horizon,
    NotPeriodic,
    Topology,
}
pub type Result<T> = std::result::Result<T, Error>;

/// Two explicitly sized storage words; only arithmetic temporaries are u64.
#[derive(Clone, Copy, Default, Debug, Eq, PartialEq, Ord, PartialOrd, Hash)]
pub struct Words(pub [u32; 2]);
impl Words {
    pub const fn new(x: u64) -> Self {
        Self([x as u32, (x >> 32) as u32])
    }
    pub const fn get(self) -> u64 {
        self.0[0] as u64 | ((self.0[1] as u64) << 32)
    }
    fn add(&mut self, x: u64) -> Result<()> {
        *self = Self::new(self.get().checked_add(x).ok_or(Error::Range)?);
        Ok(())
    }
}
#[inline]
fn round_shift(x: i64, bits: u32) -> i64 {
    if x < 0 {
        -((-x + (1i64 << (bits - 1))) >> bits)
    } else {
        (x + (1i64 << (bits - 1))) >> bits
    }
}
fn rnd(x: i128, d: i128) -> i128 {
    debug_assert!(d > 0);
    if x < 0 {
        -((-x + d / 2) / d)
    } else {
        (x + d / 2) / d
    }
}
fn shift(x: i128, n: i32) -> Result<i128> {
    if n >= 0 {
        x.checked_mul(1i128.checked_shl(n as u32).ok_or(Error::Range)?)
            .ok_or(Error::Range)
    } else {
        Ok(rnd(x, 1i128.checked_shl((-n) as u32).ok_or(Error::Range)?))
    }
}
fn i32c(x: i128) -> Result<i32> {
    i32::try_from(x).map_err(|_| Error::Range)
}
fn u64c(x: i128) -> Result<u64> {
    u64::try_from(x).map_err(|_| Error::Range)
}
fn sqrt(x: u128) -> u128 {
    if x == 0 {
        return 0;
    }
    let mut a = 1u128 << (128 - x.leading_zeros()).div_ceil(2);
    loop {
        let b = (a + x / a) / 2;
        if b >= a {
            return a;
        }
        a = b;
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, Ord, PartialOrd, Hash)]
pub struct Key {
    pub energy: Words,
    pub angular: Words,
}
impl Key {
    /// Boundary inputs are p in Q16 and eccentricity in Q30. No float decisions.
    pub fn darwin(p: u32, eccentricity: u32) -> Result<Self> {
        let p = (p as i128) << 32;
        let e = (eccentricity as i128) << 18;
        if e >= Q48 || p <= 6 * Q48 + 2 * e || p > 8192 * Q48 {
            return Err(Error::NoBoundOrbit);
        }
        let e2 = e * e / Q48;
        let den = p - 3 * Q48 - e2;
        let l2 = p * p / den;
        let numerator = (p - 2 * Q48) * (p - 2 * Q48) - 4 * e * e;
        let divisor = p * den / Q48;
        // Retain sixteen guard bits before the square root. Truncating E²
        // directly to Q48 can lose more than one output quantum of E.
        let e2 = ((numerator / divisor) << 16) + ((numerator % divisor) << 16) / divisor;
        Ok(Self {
            energy: Words::new(u64c(sqrt((e2 << 32) as u128) as i128)?),
            angular: Words::new(u64c(sqrt((l2 << 16) as u128) as i128)?),
        })
    }
    pub fn new(energy_q48: u64, angular_q32: u64) -> Result<Self> {
        if energy_q48 == 0
            || angular_q32 < 1 << 30
            || energy_q48 > 16u64 << 48
            || angular_q32 > 4096u64 << 32
        {
            return Err(Error::Range);
        }
        Ok(Self {
            energy: Words::new(energy_q48),
            angular: Words::new(angular_q32),
        })
    }
    fn inverse_l2(self) -> i128 {
        let l = self.angular.get() as i128;
        Q48 * Q48 / ((l * l) >> 16)
    }
    fn radial(self, u: i128, light: bool) -> i128 {
        let inv = self.inverse_l2();
        let e = self.energy.get() as i128;
        let u2 = u * u / Q48;
        if light {
            inv - u2 + 2 * u2 * u / Q48
        } else {
            (e * e / Q48 - Q48) * inv / Q48 + 2 * inv * u / Q48 - u2 + 2 * u2 * u / Q48
        }
    }
    fn periapsis(self) -> Result<i128> {
        let inv = self.inverse_l2();
        if 12 * inv >= Q48 {
            return Err(Error::NoBoundOrbit);
        }
        let d = sqrt(((Q48 - 12 * inv) * Q48) as u128) as i128;
        let mut lo = (Q48 - d) / 6;
        let mut hi = (Q48 + d) / 6;
        if self.radial(lo, false) <= 0 || self.radial(hi, false) >= 0 {
            return Err(Error::NoBoundOrbit);
        }
        while hi - lo > 1 {
            let mid = (hi + lo) / 2;
            if self.radial(mid, false) > 0 {
                lo = mid;
            } else {
                hi = mid;
            }
        }
        Ok((lo + hi) / 2)
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct State {
    pub u: i32,
    pub v: i32,
    pub exponent: i32,
}
impl State {
    pub fn from_q48(u: i128, v: i128) -> Result<Self> {
        if u <= 0 || u >= Q48 / 2 {
            return Err(Error::Range);
        }
        let max = u.max(v.abs()) as u128;
        let exponent = 127 - max.leading_zeros() as i32 - 48 - 27;
        Ok(Self {
            u: i32c(shift(u, -48 - exponent)?)?,
            v: i32c(shift(v, -48 - exponent)?)?,
            exponent,
        })
    }
    pub fn u_q48(self) -> i128 {
        shift(self.u as i128, self.exponent + 48).expect("validated exponent")
    }
    pub fn v_q48(self) -> i128 {
        shift(self.v as i128, self.exponent + 48).expect("validated exponent")
    }
    fn reblock(self, exponent: i32) -> Result<Self> {
        Ok(Self {
            u: i32c(shift(self.u as i128, self.exponent - exponent)?)?,
            v: i32c(shift(self.v as i128, self.exponent - exponent)?)?,
            exponent,
        })
    }
}

/// Three lattice permutations. Their inverse is exact even for hyperbolic K<0.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Map {
    pub a: i32,
    pub k: i32,
    pub j: i32,
}
impl Map {
    fn product(a: i32, b: i32) -> i64 {
        let p = a as i64 * b as i64;
        if p < 0 {
            -((-p + (1 << 29)) >> 30)
        } else {
            (p + (1 << 29)) >> 30
        }
    }
    pub fn apply(self, s: State) -> Result<State> {
        let u = i32::try_from(s.u as i64 + Self::product(self.a, s.v)).map_err(|_| Error::Range)?;
        let v = i32::try_from(s.v as i64 - Self::product(self.k, u) + self.j as i64)
            .map_err(|_| Error::Range)?;
        let u = i32::try_from(u as i64 + Self::product(self.a, v)).map_err(|_| Error::Range)?;
        Ok(State { u, v, ..s })
    }
    pub fn inverse(self, s: State) -> Result<State> {
        let u = i32::try_from(s.u as i64 - Self::product(self.a, s.v)).map_err(|_| Error::Range)?;
        let v = i32::try_from(s.v as i64 + Self::product(self.k, u) - self.j as i64)
            .map_err(|_| Error::Range)?;
        let u = i32::try_from(u as i64 - Self::product(self.a, v)).map_err(|_| Error::Range)?;
        Ok(State { u, v, ..s })
    }
}

pub fn band_index(s: State) -> Result<i32> {
    if s.u <= 0 {
        return Err(Error::Range);
    }
    let top = 31 - (s.u as u32).leading_zeros() as i32;
    let power = top + s.exponent;
    let norm = shift(s.u as i128, 30 - top)? as i64; // [1,2) Q30
    if norm == Q30 {
        return Ok(-16 * power);
    }
    let half = norm / 2; // (.5,1) Q30
    let j = (0..16)
        .find(|&j| half >= bands::EDGES[j + 1])
        .ok_or(Error::Range)?;
    Ok(-16 * (power + 1) + j as i32)
}
fn edge_q48(k: i32, center: bool) -> Result<i128> {
    let oct = k.div_euclid(16);
    let j = k.rem_euclid(16) as usize;
    let word = if center {
        bands::CENTERS[j]
    } else {
        bands::EDGES[j]
    };
    shift(word as i128, 18 - oct)
}

#[derive(Clone, Debug)]
struct Band {
    k: i32,
    exponent: i32,
    lo: i32,
    hi: i32,
    w2: i128,
    rhs: i128,
    full: Map,
    full_b: i64,
    force_q30: i64,
    w2_q30: i32,
}
impl Band {
    fn new(k: i32, s: State, key: Key, light: bool, newton: bool) -> Result<(Self, State)> {
        let hi = edge_q48(k, false)?;
        let max = hi.max(s.v_q48().abs());
        let exponent = 127 - (max as u128).leading_zeros() as i32 - 48 - 27;
        let s = s.reblock(exponent)?;
        let uk = edge_q48(k, true)?;
        let w2 = if newton { Q48 } else { Q48 - 6 * uk };
        let rhs =
            if light { 0 } else { key.inverse_l2() } - if newton { 0 } else { 3 * uk * uk / Q48 };
        let mut b = Self {
            k,
            exponent,
            lo: i32c(shift(edge_q48(k + 1, false)?, -48 - exponent)?)?,
            hi: i32c(shift(hi, -48 - exponent)?)?,
            w2,
            rhs,
            full: Map { a: 0, k: 0, j: 0 },
            full_b: 0,
            force_q30: i64::try_from(shift(rhs, -18 - exponent)?).map_err(|_| Error::Range)?,
            w2_q30: i32c(rnd(w2, 1 << 18))?,
        };
        let full = b.evaluate(STEP)?;
        b.full = full.0;
        b.full_b = full.1;
        Ok((b, s))
    }
    fn coefficients(&self, h: u32) -> (i64, i64) {
        #[cfg(feature = "profile")]
        profile::add(|s| s.coefficients += 1);
        // x is Q30, polynomial values Q32. |x|<=1/8, so every
        // product is below 2^62. The constants are nearest Q32.
        let h = h as i64;
        let h2 = round_shift(h * h, 30);
        let x = round_shift(self.w2_q30 as i64 * h2, 30);
        let poly = |terms: &[i64]| {
            let mut p = 0;
            for &c in terms.iter().rev() {
                p = round_shift(p * x, 30) + c;
            }
            p
        };
        let a = round_shift(
            h * poly(&[4294967296, 357913941, 35791394, 3621760, 366920, 37168]),
            31,
        );
        let b = round_shift(
            h * poly(&[4294967296, -715827883, 35791394, -852176, 11836, -108]),
            30,
        );
        (a, b)
    }
    fn evaluate(&self, h: u32) -> Result<(Map, i64)> {
        let (a, b) = self.coefficients(h);
        Ok((
            Map {
                a: i32::try_from(round_shift(a, 2)).map_err(|_| Error::Range)?,
                k: i32::try_from(round_shift(self.w2_q30 as i64 * b, 32))
                    .map_err(|_| Error::Range)?,
                // Q48*Q32 needs up to 80 bits. Creation-only, power-of-two shift.
                j: i32c(shift(self.rhs * b as i128, -80 - self.exponent)?)?,
            },
            b,
        ))
    }
    fn map(&self, h: u32) -> Result<Map> {
        Ok(self.evaluate(h)?.0)
    }
    fn outside(&self, s: State) -> bool {
        (s.u <= self.lo && s.v < 0) || (s.u >= self.hi && s.v > 0)
    }
}

#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
pub struct Increments {
    pub phi: Words,
    pub t: Words,
    pub tau: Words,
}
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Crossing {
    pub band: i32,
    pub state: State,
    pub at: Increments,
}
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Cycle {
    pub key: Key,
    pub start: State,
    pub end: State,
    pub start_band: i32,
    pub end_band: i32,
    pub apo: State,
    pub increments: Increments,
    pub crossings: Vec<Crossing>,
    pub steps: u32,
    pub local: Option<LocalOscillator>,
}
/// Address within the repeated generator. `crossing` is the last completed
/// crossing, or None before its first crossing (also for a local cell).
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Location {
    pub cycle: u64,
    pub time_in_cycle: Words,
    pub crossing: Option<usize>,
}
impl Cycle {
    /// The generator repeats by definition; end is a diagnostic first-return value.
    pub fn periodic(&self) -> bool {
        self.increments.t.get() > 0 && self.increments.phi.get() > 0
    }
    pub fn raw_return_closes(&self) -> bool {
        self.start == self.end && self.start_band == self.end_band
    }
    /// Coordinate time since the tube's epoch, Q20. Quotient/remainder, then
    /// an integer table search; no previous cycle is evaluated or evolved.
    pub fn locate(&self, elapsed: Words) -> Result<Location> {
        let period = self.increments.t.get();
        if period == 0 {
            return Err(Error::NotPeriodic);
        }
        let time = elapsed.get() % period;
        let next = self.crossings.partition_point(|c| c.at.t.get() <= time);
        Ok(Location {
            cycle: elapsed.get() / period,
            time_in_cycle: Words::new(time),
            crossing: next.checked_sub(1),
        })
    }
    /// Repeat the compiled constants; never evolve a previous cycle's rounded end.
    pub fn repeat(&self, n: u32) -> Result<Increments> {
        if !self.periodic() {
            return Err(Error::NotPeriodic);
        }
        let mul = |w: Words| {
            w.get()
                .checked_mul(n as u64)
                .map(Words::new)
                .ok_or(Error::Range)
        };
        Ok(Increments {
            phi: mul(self.increments.phi)?,
            t: mul(self.increments.t)?,
            tau: mul(self.increments.tau)?,
        })
    }
}

fn rates(s: State, key: Key) -> Result<(u64, u64)> {
    let u = s.u_q48();
    if u <= 0 || u >= Q48 / 2 {
        return Err(Error::Horizon);
    }
    let u2 = u * u / Q48;
    let den = (key.angular.get() as i128 * u2) >> 32;
    if den == 0 {
        return Err(Error::Range);
    }
    let tau = rnd(1i128 << 68, den);
    let t = rnd(tau * key.energy.get() as i128, Q48 - 2 * u);
    Ok((u64c(t)?, u64c(tau)?))
}
fn clock(s: State, _end: State, band: &Band, h: u32, key: Key) -> Result<(u64, u64)> {
    let (mut t, mut tau) = (0i128, 0i128);
    for (&node, &weight) in bands::NODES.iter().zip(bands::WEIGHTS.iter()) {
        let hh = rnd(h as i128 * (Q30 + node) as i128, 2 * Q30 as i128) as u32;
        let sample = band.map(hh)?.apply(s)?;
        let (a, b) = rates(sample, key)?;
        t += a as i128 * weight as i128;
        tau += b as i128 * weight as i128;
    }
    Ok((
        u64c(rnd(t * h as i128, 2 * (1i128 << 60)))?,
        u64c(rnd(tau * h as i128, 2 * (1i128 << 60)))?,
    ))
}
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Outcome {
    Absorbed,
    Escaped,
    AngleReached,
}

struct Walker {
    s: State,
    band: Band,
    key: Key,
    light: bool,
    newton: bool,
    at: Increments,
    steps: u32,
    crossings: Vec<Crossing>,
}
impl Walker {
    fn new(s: State, key: Key, light: bool, newton: bool) -> Result<Self> {
        let (band, s) = Band::new(band_index(s)?, s, key, light, newton)?;
        Ok(Self {
            s,
            band,
            key,
            light,
            newton,
            at: Increments::default(),
            steps: 0,
            crossings: vec![],
        })
    }
    // +1 apo (V - to +), -1 peri (V + to -), 0 no turn.
    fn step(&mut self, times: bool, escape: Option<i128>) -> Result<i32> {
        let before = self.s;
        let trial = self.band.full.apply(before)?;
        let turn = |s: State| (before.v < 0 && s.v >= 0) || (before.v > 0 && s.v <= 0);
        #[cfg(feature = "profile")]
        let exit_start = std::time::Instant::now();
        let found = self.band.first_event(before, 1, STEP, escape, &mut 0)?;
        #[cfg(feature = "profile")]
        profile::add(|s| s.exits_ns += exit_start.elapsed().as_nanos());
        let (h, end) = found.unwrap_or((STEP, trial));
        if h == 0 {
            return Err(Error::Range);
        }
        self.at.phi.add(h as u64)?;
        if times {
            #[cfg(feature = "profile")]
            let clock_start = std::time::Instant::now();
            let (t, tau) = clock(before, end, &self.band, h, self.key)?;
            #[cfg(feature = "profile")]
            profile::add(|s| s.clocks_ns += clock_start.elapsed().as_nanos());
            self.at.t.add(t)?;
            self.at.tau.add(tau)?;
        }
        self.steps += 1;
        let turned = if turn(end) {
            if before.v < 0 {
                1
            } else {
                -1
            }
        } else {
            0
        };
        self.s = end;
        if self.s.u_q48() >= Q48 / 2 {
            return Err(Error::Horizon);
        }
        if self.band.outside(end) {
            let next = if end.v > 0 {
                self.band.k - 1
            } else {
                self.band.k + 1
            };
            let (band, s) = Band::new(next, end, self.key, self.light, self.newton)?;
            self.s = s;
            self.band = band;
            self.crossings.push(Crossing {
                band: next,
                state: s,
                at: self.at,
            });
        }
        Ok(turned)
    }
}

pub fn compile(key: Key) -> Result<Cycle> {
    Key::new(key.energy.get(), key.angular.get())?;
    if let Some(c) = local::compile_local(key)? {
        return Ok(c);
    }
    compile_variant(key, false)
}
/// The planted Newtonian variant shares all integer arithmetic and event rules.
pub fn compile_variant(key: Key, newton: bool) -> Result<Cycle> {
    Key::new(key.energy.get(), key.angular.get())?;
    let u = key.periapsis()?;
    let mut w = Walker::new(State::from_q48(u, 0)?, key, false, newton)?;
    let start = w.s;
    let start_band = w.band.k;
    let mut apo = None;
    for _ in 0..MAX_STEPS {
        match w.step(true, None)? {
            1 => apo = Some(w.s),
            -1 if apo.is_some() => {
                return Ok(Cycle {
                    key,
                    start,
                    end: w.s,
                    start_band,
                    end_band: w.band.k,
                    apo: apo.unwrap(),
                    increments: w.at,
                    crossings: w.crossings,
                    steps: w.steps,
                    local: None,
                });
            }
            _ => {}
        }
    }
    Err(Error::Budget)
}

/// Trace an incoming ray or particle from u=1/10000 (light), u=1/100 (matter).
/// Stop at absorption or the first outgoing return. No GR capture threshold.
pub fn scatter(key: Key, light: bool) -> Result<(Outcome, Words)> {
    Key::new(key.energy.get(), key.angular.get())?;
    if light && key.energy.get() != 1 << 48 {
        return Err(Error::Range);
    }
    let u = Q48 / if light { 10000 } else { 100 };
    let radial = key.radial(u, light);
    if radial < 0 {
        return Err(Error::Range);
    }
    let v = sqrt((radial * Q48) as u128) as i128;
    let mut w = Walker::new(State::from_q48(u, v)?, key, light, false)?;
    for _ in 0..MAX_STEPS {
        match w.step(false, Some(u)) {
            Err(Error::Horizon) => return Ok((Outcome::Absorbed, w.at.phi)),
            Err(e) => return Err(e),
            _ => {}
        }
        if w.s.v < 0 && w.s.u_q48() <= u {
            return Ok((Outcome::Escaped, w.at.phi));
        }
    }
    Err(Error::Budget)
}

/// The exterior light tail: integer composite Simpson on u in [0,1/10000].
/// 256 fixed panels; only used at ray creation. Returns its angle in Q30.
pub fn light_tail(key: Key) -> Result<u64> {
    Key::new(key.energy.get(), key.angular.get())?;
    if key.energy.get() != 1 << 48 {
        return Err(Error::Range);
    }
    let n = 256;
    let end = Q48 / 10000;
    let mut sum = 0i128;
    for i in 0..=n {
        let u = end * i / n;
        let r = key.radial(u, true);
        if r <= 0 {
            return Err(Error::Range);
        }
        let v = sqrt((r * Q48) as u128) as i128;
        let f = (1i128 << 78) / v;
        sum += f * if i == 0 || i == n {
            1
        } else if i % 2 == 0 {
            2
        } else {
            4
        };
    }
    u64c(rnd(sum * end, 3 * n * Q48))
}

#[derive(Default)]
pub struct Memo {
    cycles: BTreeMap<Key, Arc<Cycle>>,
}
impl Memo {
    pub fn get(&mut self, key: Key) -> Result<Arc<Cycle>> {
        if let Some(c) = self.cycles.get(&key) {
            return Ok(c.clone());
        }
        let c = Arc::new(compile(key)?);
        self.cycles.insert(key, c.clone());
        Ok(c)
    }
    pub fn len(&self) -> usize {
        self.cycles.len()
    }
    pub fn is_empty(&self) -> bool {
        self.cycles.is_empty()
    }
}

/// Signed first differences of increments, encoded as two's-complement word pairs.
/// A quotient diff / key_step is a discrete sensitivity, not a real derivative.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Tangent {
    pub energy_step: Words,
    pub angular_step: Words,
    pub energy_diff: [Words; 3],
    pub angular_diff: [Words; 3],
}
fn values(i: Increments) -> [u64; 3] {
    [i.phi.get(), i.t.get(), i.tau.get()]
}
fn differences(a: Increments, b: Increments) -> Result<[Words; 3]> {
    let (a, b) = (values(a), values(b));
    let mut out = [Words::default(); 3];
    for i in 0..3 {
        let d = i64::try_from(b[i] as i128 - a[i] as i128).map_err(|_| Error::Range)?;
        out[i] = Words::new(d as u64);
    }
    Ok(out)
}
impl Tangent {
    pub fn create(c: &Cycle, energy_step: u64, angular_step: u64) -> Result<Self> {
        if energy_step == 0 || angular_step == 0 {
            return Err(Error::Range);
        }
        let e = Key::new(
            c.key
                .energy
                .get()
                .checked_add(energy_step)
                .ok_or(Error::Range)?,
            c.key.angular.get(),
        )?;
        let l = Key::new(
            c.key.energy.get(),
            c.key
                .angular
                .get()
                .checked_add(angular_step)
                .ok_or(Error::Range)?,
        )?;
        let ce = compile(e)?;
        let cl = compile(l)?;
        let topology = |x: &Cycle| {
            x.crossings
                .iter()
                .map(|a| a.band)
                .eq(c.crossings.iter().map(|a| a.band))
        };
        if !topology(&ce) || !topology(&cl) {
            return Err(Error::Topology);
        }
        Ok(Self {
            energy_step: Words::new(energy_step),
            angular_step: Words::new(angular_step),
            energy_diff: differences(c.increments, ce.increments)?,
            angular_diff: differences(c.increments, cl.increments)?,
        })
    }
    /// Prediction only. Recompile and compare before making any canonical decision.
    pub fn predict(&self, base: Increments, de: i64, dl: i64) -> Result<Increments> {
        let mut v = values(base);
        for (i, x) in v.iter_mut().enumerate() {
            let e = rnd(
                self.energy_diff[i].get() as i64 as i128 * de as i128,
                self.energy_step.get() as i128,
            );
            let l = rnd(
                self.angular_diff[i].get() as i64 as i128 * dl as i128,
                self.angular_step.get() as i128,
            );
            *x = u64c(*x as i128 + e + l)?;
        }
        Ok(Increments {
            phi: Words::new(v[0]),
            t: Words::new(v[1]),
            tau: Words::new(v[2]),
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn key() -> Key {
        Key::darwin(20 << 16, 1 << 29).unwrap()
    }
    #[test]
    fn shears_reverse_bit_for_bit_in_both_regimes() {
        for k in [17, 30, 41, 100, 200] {
            let u = edge_q48(k, true).unwrap();
            let s = State::from_q48(u, u / 3).unwrap();
            let (b, s) = Band::new(k, s, key(), true, false).unwrap();
            for h in [1, 13, 1024, STEP / 2, STEP] {
                let m = b.map(h).unwrap();
                for (du, dv) in [(0, 0), (123, -33), (-876, 435), (-20000, -100000)] {
                    let s = State {
                        u: s.u + du,
                        v: s.v + dv,
                        ..s
                    };
                    assert_eq!(m.inverse(m.apply(s).unwrap()).unwrap(), s);
                    assert_eq!(m.apply(m.inverse(s).unwrap()).unwrap(), s);
                }
            }
        }
    }
    #[test]
    fn bit_identical_compilation_and_memo_hits() {
        let a = compile(key()).unwrap();
        let b = compile(key()).unwrap();
        assert_eq!(a, b);
        let mut memo = Memo::default();
        let c = memo.get(key()).unwrap();
        let d = memo.get(key()).unwrap();
        assert!(Arc::ptr_eq(&c, &d));
        assert_eq!(memo.len(), 1);
        assert!(a.periodic());
        assert_eq!(
            a.repeat(10000).unwrap().phi.get(),
            a.increments.phi.get() * 10000
        );
    }
    #[test]
    fn bit_band_lookup_agrees_at_every_centre() {
        for k in 16..320 {
            let s = State::from_q48(edge_q48(k, true).unwrap(), 0).unwrap();
            assert_eq!(band_index(s).unwrap(), k);
        }
    }
    #[test]
    fn zero_kick_is_identity_and_probe_step_is_its_first_difference() {
        let c = compile(key()).unwrap();
        let t = Tangent::create(&c, 1 << 24, 1 << 16).unwrap();
        assert_eq!(t.predict(c.increments, 0, 0).unwrap(), c.increments);
        let perturbed = Key::new(c.key.energy.get() + (1 << 24), c.key.angular.get()).unwrap();
        assert_eq!(
            t.predict(c.increments, 1 << 24, 0).unwrap(),
            compile(perturbed).unwrap().increments
        );
    }
    #[test]
    fn oscillator_coefficient_and_rounding_bounds() {
        for k in [17, 30, 41, 70, 140, 220] {
            let uk = edge_q48(k, true).unwrap();
            let s = State::from_q48(uk, uk / 5).unwrap();
            let (b, s) = Band::new(k, s, key(), true, false).unwrap();
            let w2 = b.w2 as f64 / Q48 as f64;
            let f = b.rhs as f64 / Q48 as f64;
            let h = STEP as f64 / Q30 as f64;
            let (a, bb) = if w2 > 0.0 {
                let w = w2.sqrt();
                ((w * h / 2.0).tan() / w, (w * h).sin() / w)
            } else {
                let w = (-w2).sqrt();
                ((w * h / 2.0).tanh() / w, (w * h).sinh() / w)
            };
            let m = b.full;
            let coef_bound = 0.5 / Q30 as f64 + 5e-13;
            assert!((m.a as f64 / Q30 as f64 - a).abs() <= coef_bound);
            assert!((m.k as f64 / Q30 as f64 - w2 * bb).abs() <= coef_bound);
            let q = 2f64.powi(b.exponent);
            assert!((m.j as f64 * q - f * bb).abs() <= q / 2.0 + f.abs() * 5e-16);
            let got = m.apply(s).unwrap();
            let a = m.a as f64 / Q30 as f64;
            let k = m.k as f64 / Q30 as f64;
            let u1 = s.u as f64 + a * s.v as f64;
            let v1 = s.v as f64 - k * u1 + m.j as f64;
            let u2 = u1 + a * v1;
            assert!((got.v as f64 - v1).abs() <= 0.5 * (1.0 + k.abs()) + 1e-6);
            assert!((got.u as f64 - u2).abs() <= 0.5 * (2.0 + a.abs() * (1.0 + k.abs())) + 1e-6);
        }
    }
}

/// Outward enclosures use integer endpoint extrema; no floating padding.
#[derive(Clone, Copy)]
struct Interval {
    lo: i64,
    hi: i64,
}
impl Interval {
    fn point(x: i32) -> Self {
        Self {
            lo: x as i64,
            hi: x as i64,
        }
    }
    fn ends(a: i32, b: i32) -> Self {
        Self {
            lo: a.min(b) as i64,
            hi: a.max(b) as i64,
        }
    }
    fn add(self, b: Self) -> Self {
        Self {
            lo: self.lo + b.lo,
            hi: self.hi + b.hi,
        }
    }
    fn sub(self, b: Self) -> Self {
        Self {
            lo: self.lo - b.hi,
            hi: self.hi - b.lo,
        }
    }
    fn product(self, b: Self) -> Result<Self> {
        let mut lo = i64::MAX;
        let mut hi = i64::MIN;
        for a in [self.lo, self.hi] {
            for b in [b.lo, b.hi] {
                let x = round_shift(a.checked_mul(b).ok_or(Error::Range)?, 30);
                lo = lo.min(x);
                hi = hi.max(x);
            }
        }
        Ok(Self { lo, hi })
    }
}
impl Band {
    fn event_possible(
        &self,
        s: State,
        a: Map,
        b: Map,
        blo: i64,
        bhi: i64,
        escape: Option<i128>,
    ) -> Result<bool> {
        let aa = Interval::ends(a.a, b.a);
        let kk = Interval::ends(a.k, b.k);
        let jj = Interval::ends(a.j, b.j);
        let u1 = Interval::point(s.u).add(aa.product(Interval::point(s.v))?);
        let mut v1 = Interval::point(s.v).sub(kk.product(u1)?).add(jj);
        // Keep the common H factor: J and K*U nearly cancel on circular orbits.
        let fl = self.force_q30 - self.w2_q30 as i64 * u1.lo;
        let fh = self.force_q30 - self.w2_q30 as i64 * u1.hi;
        let force = Interval {
            lo: fl.min(fh).div_euclid(Q30),
            hi: -(-fl.max(fh)).div_euclid(Q30),
        };
        let hh = Interval {
            lo: blo.div_euclid(4),
            hi: -(-bhi).div_euclid(4),
        };
        let acc = hh.product(force)?;
        let slack = 6; // includes coefficient, force and product rounding (U<2^31).
        v1.lo = v1.lo.max(s.v as i64 + acc.lo - slack);
        v1.hi = v1.hi.min(s.v as i64 + acc.hi + slack);
        let u2 = u1.add(aa.product(v1)?);
        let turn = (s.v < 0 && v1.hi >= 0) || (s.v > 0 && v1.lo <= 0);
        let edge = (u2.lo <= self.lo as i64 && v1.lo < 0) || (u2.hi >= self.hi as i64 && v1.hi > 0);
        let escape = if let Some(u) = escape {
            v1.lo < 0 && shift(u2.lo as i128, self.exponent + 48)? <= u
        } else {
            false
        };
        Ok(turn || edge || escape)
    }
    fn first_event(
        &self,
        s: State,
        lo: u32,
        hi: u32,
        escape: Option<i128>,
        visits: &mut u32,
    ) -> Result<Option<(u32, State)>> {
        let a = self.evaluate(lo)?;
        let b = if hi == STEP {
            (self.full, self.full_b)
        } else {
            self.evaluate(hi)?
        };
        self.search(s, lo, hi, a, b, escape, visits)
    }
    #[allow(clippy::too_many_arguments)]
    fn search(
        &self,
        s: State,
        lo: u32,
        hi: u32,
        a: (Map, i64),
        b: (Map, i64),
        escape: Option<i128>,
        visits: &mut u32,
    ) -> Result<Option<(u32, State)>> {
        *visits += 1;
        #[cfg(feature = "profile")]
        profile::add(|s| s.nodes += 1);
        if *visits > 131072 {
            return Err(Error::Budget);
        }
        if !self.event_possible(s, a.0, b.0, a.1, b.1, escape)? {
            return Ok(None);
        }
        if lo == hi {
            let t = a.0.apply(s)?;
            let event = (s.v < 0 && t.v >= 0)
                || (s.v > 0 && t.v <= 0)
                || self.outside(t)
                || escape.is_some_and(|u| t.v < 0 && t.u_q48() <= u);
            return Ok(event.then_some((lo, t)));
        }
        let mid = (lo + hi) / 2;
        let m = if mid == lo { a } else { self.evaluate(mid)? };
        if let Some(hit) = self.search(s, lo, mid, a, m, escape, visits)? {
            return Ok(Some(hit));
        }
        let m = if mid + 1 == hi {
            b
        } else {
            self.evaluate(mid + 1)?
        };
        self.search(s, mid + 1, hi, m, b, escape, visits)
    }
}

#[cfg(test)]
mod exit_tests {
    use super::*;
    #[test]
    fn first_integer_exit_agrees_with_exhaustive_search() {
        let key = Key::darwin(20 << 16, 1 << 29).unwrap();
        let mut hits = 0;
        for k in [17, 30, 70, 150] {
            let s = State::from_q48(edge_q48(k, true).unwrap(), 0).unwrap();
            let (b, s) = Band::new(k, s, key, false, false).unwrap();
            for (u, v) in [
                (b.lo + 1, -5000000),
                (b.hi - 1, 5000000),
                (s.u, -1),
                (s.u, 1),
                (s.u, 0),
            ] {
                let s = State { u, v, ..s };
                let predicate =
                    |t: State| b.outside(t) || (s.v < 0 && t.v >= 0) || (s.v > 0 && t.v <= 0);
                let brute = (1..=4096).find_map(|h| {
                    let t = b.map(h).unwrap().apply(s).unwrap();
                    predicate(t).then_some((h, t))
                });
                let got = b.first_event(s, 1, 4096, None, &mut 0).unwrap();
                assert_eq!(got, brute, "k={k} state={s:?}");
                hits += usize::from(got.is_some());
            }
        }
        assert!(hits >= 8, "only {hits} positive exit cases");
    }
}

/// Nonperiodic diagnostic evolution; used to test the two ISCO cases without a
/// GR stability classifier. Return Budget if the requested angle was not reached.
pub fn trace_until(key: Key, u_q48: u64, v_q48: i64, phi_q30: u64) -> Result<Outcome> {
    Key::new(key.energy.get(), key.angular.get())?;
    let mut w = Walker::new(
        State::from_q48(u_q48 as i128, v_q48 as i128)?,
        key,
        false,
        false,
    )?;
    for _ in 0..1_000_000 {
        match w.step(false, None) {
            Err(Error::Horizon) => return Ok(Outcome::Absorbed),
            Err(e) => return Err(e),
            _ => {}
        }
        if w.at.phi.get() >= phi_q30 {
            return Ok(Outcome::AngleReached);
        }
    }
    Err(Error::Budget)
}

#[cfg(test)]
mod domain_tests {
    use super::*;
    #[test]
    fn invalid_inputs_are_explicit_errors() {
        assert_eq!(Key::new(1 << 48, 1), Err(Error::Range));
        assert_eq!(Key::new(0, 4 << 32), Err(Error::Range));
        assert_eq!(
            scatter(Key::new(2 << 48, 4 << 32).unwrap(), true),
            Err(Error::Range)
        );
        assert_eq!(Key::darwin(u32::MAX, 1 << 29), Err(Error::NoBoundOrbit));
        assert_eq!(Key::darwin(5 << 16, 0), Err(Error::NoBoundOrbit));
        assert_eq!(
            compile(Key {
                energy: Words::new(0),
                angular: Words::new(0)
            }),
            Err(Error::Range)
        );
    }
    #[test]
    fn capture_cases_are_answered_not_errors_disguised_as_escape() {
        for factor in [0.5f64, 0.9, 0.97, 1.03, 1.1, 1.5] {
            let key = Key::new(1 << 48, (4.0 * factor * 4294967296.0).round() as u64).unwrap();
            let (out, _) = scatter(key, false).unwrap();
            assert_eq!(out == Outcome::Absorbed, factor < 1.0);
        }
        for factor in [0.9f64, 0.97, 1.03, 1.1] {
            let key = Key::new(
                1 << 48,
                (3.0 * 3f64.sqrt() * factor * 4294967296.0).round() as u64,
            )
            .unwrap();
            let (out, _) = scatter(key, true).unwrap();
            assert_eq!(out == Outcome::Absorbed, factor < 1.0);
        }
    }
}
