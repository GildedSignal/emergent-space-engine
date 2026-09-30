//! # Law `space-darwin16-v1`: the cycle compiler of one doll (one static mass)
//!
//! Units G = c = M = 1. u = 1/r. Q62 means an integer n standing for n/2^62; angles psi are Q61.
//! Every quantity below is an integer, and every operation is exact integer arithmetic: sums,
//! products floored by arithmetic right shifts, divisions of nonnegative integers floored (a
//! signed division truncates toward zero), and `isqrt` = floor of the square root. Floats never
//! decide anything; they appear only in the adapter and in tests. `num.rs` defines `cos`,
//! `atan`, `isqrt`, `mul_shr` and `ratio_sqrt`; `tables.rs` holds the constants, generated
//! with 90-digit Decimal arithmetic by `tests/tables.py`.
//!
//! ## What an orbit is
//! A tube stores its invariants: E (Q48) and L (Q32), an epoch and a phase. Its radial function
//! is GR's R(u) = (E² − 1)/L² + 2u/L² − u² + 2u³ = (u′)². A bound orbit has three roots
//! u_a < u_p < u_3, so R = 2(u − u_a)(u_p − u)(u_3 − u). With c = (u_a + u_p)/2 and
//! A = (u_p − u_a)/2, Darwin's phase ψ puts u = c + A cos ψ (ψ = 0 at periapsis, π at
//! apoapsis). Then the two turning-point roots cancel exactly, and along the orbit
//!   dφ/dψ = g = (2(u_3 − u))^(−1/2),  dτ/dψ = g/(L u²),  dt/dψ = E g/(L u² (1 − 2u)).
//! These are smooth, so the cycle is a quadrature. Circular orbits (A = 0) are the same
//! formula: nothing distinguishes them, and no regime is chosen.
//!
//! ## The roots (from the invariants only)
//! β = floor(2^127/L²) (2/L², Q62, with L² in Q64); α = (E² − 1)/L² in Q62, rounded toward zero.
//! A bound orbit needs E < 1 and 12/L² < 1. k₀ = isqrt((2^62 − 6β)·2^62), u_c = (2^62 − k₀)/6
//! (the circular orbit of this L), k = 2^62 − 6u_c. With y = L·u_c (Q62) and
//! V = (1 − 2u_c)(1 + y²), D = E² − V and R_c = trunc(D·2^64/L²) (R at u_c, without the
//! cancellation of evaluating α + βu_c − u_c² + 2u_c³ term by term). With R₁ = 6u_c² − 2u_c + β:
//!   f(x) = R_c + R₁x − k x² + 2x³ = R(u_c + x), every product floored to Q62.
//! If R_c ≤ 0: D ≥ −2^16 (one Q48 quantum of E, doubled) is a circular orbit (x₊ = x₋ = 0),
//! anything lower is `NoBoundOrbit`. Otherwise f(k/3) > 0 (above the barrier) is `NoBoundOrbit`,
//! and bisection to one unit gives x₊ in (0, k/3] (the last x with f(x) > 0) and x₋ in [−u_c, 0)
//! (the first x with f(x) > 0). u_p = u_c + x₊, u_a = u_c + x₋, u_3 = u_c + k/2 − x₊ − x₋ (the
//! roots of f sum to k/2). c = floor((u_a + u_p)/2), A = floor((u_p − u_a)/2), m₃ = u_3 − c.
//! Envelope: u_a ≥ 2^−28 and 2(u_3 − u_p) ≥ 2^−42, else `Range`.
//!
//! ## Cells and panels
//! Band k holds 2^(−(k+1)/16) < u ≤ 2^(−k/16); its edges are `EDGE[j] >> octave`. The outbound
//! half (ψ from 0 to π) crosses every edge u_e with u_a < u_e < u_p, at
//!   ψ_e = atan(ratio_sqrt(u_p − u_e, u_e − u_a))       if 2u_e ≥ u_a + u_p,
//!   ψ_e = π − atan(ratio_sqrt(u_e − u_a, u_p − u_e))    otherwise
//! (2·atan in Q61 is the Q62 atan's integer). These cuts are the crossing table. Each interval
//! between cuts splits into ceil(width/(π/4)) equal panels (endpoints floored). Near the
//! separatrix the first interval is refined first: if 2δ < 64A, with δ = m₃ − A, λ =
//! isqrt(floor(2δ·2^60/A)·2^60)/2 (a quarter of the peak's width sqrt(2δ/A)), and the panels
//! [0, λ], [λ, 2λ], [2λ, 4λ], … (each split by π/4 too) run while they end inside the interval.
//!
//! ## Quadrature (the time rule is the same rule)
//! Four-point Gauss–Legendre on each panel [a, b]: h = b − a, mid = a + h/2, nodes
//! mid ± floor(X_i·h/2^63), weights ω_i = floor(W_i·h/2^63). At a node: u = c + floor(A·cos ψ),
//! d = 2(m₃ − floor(A·cos ψ)) (≥ 2^20, else `Range`), g = isqrt(floor(2^126/d)·2^20) (Q42),
//! q = floor(u_a·2^62/u), r_τ = floor(q²/2^62), r_t = floor(r_τ·2^62/(2^62 − 2u)). The sums gain
//! S_φ += ω g (Q103), and with b = floor(ω g/2^63): S_τ += b r_τ, S_t += b r_t (Q102).
//! P = 1/(L u_a²) is p_m·2^(−p_e): the Q94 product L·u_a is cut to its top 64 bits, times u_a,
//! cut to its top 64 bits d₂, then p_m = floor(2^127/d₂). Over the half orbit (doubled for the
//! cycle, one shift less): Δφ = floor(S_φ/2^72) (Q30), Δτ = floor(p_m S_τ / 2^(p_e+81)) and
//! Δt = floor(floor(p_m S_t/2^64)·E / 2^(p_e+65)) (Q20). The crossing table stores the same
//! conversions of the partial sums at each cut (one more shift: half-orbit values).
//!
//! ## The cycle, the tube and a position
//! The cycle is compiled once per key and memoized by the exact key. It repeats by definition:
//! after n cycles φ, t and τ have gained n·Δ, and nothing is evolved from one cycle to the next.
//! The inbound half mirrors the outbound half (R depends on u only): at time T − t it is at the
//! same u, with angle Δφ − φ(t). A position at time t since periapsis is located by t mod T,
//! the mirror, a binary search of the crossing table, the same panels rebuilt inside that cell,
//! and a bracketed Newton solve of the panel's partial quadrature for ψ (the partial quadrature
//! is the four-point rule on [a, ψ]). It is a derivation, never a state.
//!
//! ## Light and unbound bodies
//! β = 0 and α = 1/L² for light (L = b, E = 1); α ≥ 0 for a body from infinity. If 6β ≥ 1 or R is
//! positive at its local minimum u = (1 + sqrt(1 − 6β))/6, nothing turns it: `Absorbed`. Else the
//! turning point u_t is the bisection root between the local maximum and minimum, the other
//! roots come from the quadratic R/(u − u_t) (u_0 ≤ 0 < u_t < u_3), and the same quadrature on
//! ψ from 0 to ψ_0 (where u = 0) gives the angle from the turning point to infinity.
//!
//! ## Error (what is exact, what is bounded)
//! Exact by construction: E, L, u_a, u_p, the crossing sequence and every cycle's constants;
//! hence r_min and r_max never drift, and the n-th cycle *is* the compiled one. The only
//! continuum error is systematic and identical every cycle: it enters Δφ, Δt and Δτ, so it is a
//! linear phase drift, never a compounding one. Its parts:
//! - quadrature: on a panel of half-width h whose integrand is analytic inside the Bernstein
//!   ellipse of parameter ρ, with |f| ≤ M there, four-point Gauss–Legendre errs by at most
//!   (64/15)·M·h·ρ^(−8)/(ρ² − 1). The singularities are at cos ψ = m₃/A (the branch point of g,
//!   imaginary distance acosh(m₃/A) ≥ sqrt(2δ/A)), cos ψ = −c/A (u = 0) and cos ψ = (1/2 − c)/A:
//!   the cap π/4, the band cuts (log-spaced in r, so the u = 0 pole is always many panels away)
//!   and the refinement keep ρ ≥ 2 on every panel. `tests/near_circular.rs` checks the measured
//!   error against GR over the envelope;
//! - rounding: each node's value is exact to a few units of 2^−42 relative (g) and 2^−62 (u, q,
//!   r), and each sum carries at most one unit per node: below 2^−30 relative per cycle;
//! - roots: bisection to one Q62 unit, so r_min and r_max are within 2^−62 of the invariants'.
//! The law differs from continuum GR by these and by the key's quantization of (E, L).
//!
//! The planted Newtonian variant (`compile_variant(key, true)`) drops the 2u³ term: g = 1, so
//! the advance is zero and the precession gate must kill it.

mod num;
mod tables;

use std::collections::BTreeMap;
use std::sync::Arc;

use num::{atan, cos, isqrt, mul_shr, ratio_sqrt, ONE};
use tables::{EDGE, PI, W, X};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Error {
    Range,
    NoBoundOrbit,
    NotPeriodic,
    Topology,
}
pub type Result<T> = std::result::Result<T, Error>;

/// Two explicitly sized storage words; only arithmetic temporaries are wider.
#[derive(Clone, Copy, Default, Debug, Eq, PartialEq, Ord, PartialOrd, Hash)]
pub struct Words(pub [u32; 2]);
impl Words {
    pub const fn new(x: u64) -> Self {
        Self([x as u32, (x >> 32) as u32])
    }
    pub const fn get(self) -> u64 {
        self.0[0] as u64 | ((self.0[1] as u64) << 32)
    }
}
fn words(x: u128) -> Result<Words> {
    u64::try_from(x).map(Words::new).map_err(|_| Error::Range)
}

/// The invariants: E in Q48, L in Q32. The memo key.
#[derive(Clone, Copy, Debug, Eq, PartialEq, Ord, PartialOrd, Hash)]
pub struct Key {
    pub energy: Words,
    pub angular: Words,
}
impl Key {
    /// Boundary input: Darwin's p in Q16 and e in Q30. No float decisions.
    pub fn darwin(p: u32, eccentricity: u32) -> Result<Self> {
        const Q48: i128 = 1 << 48;
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
        // Sixteen guard bits before the square root: flooring E² at Q48 loses a quantum of E.
        let e2 = ((numerator / divisor) << 16) + ((numerator % divisor) << 16) / divisor;
        Ok(Self {
            energy: words(isqrt((e2 << 32) as u128))?,
            angular: words(isqrt((l2 << 16) as u128))?,
        })
    }
    /// 0 < E ≤ 16, 1/4 ≤ L ≤ 4096.
    pub fn new(energy_q48: u64, angular_q32: u64) -> Result<Self> {
        if energy_q48 == 0 || angular_q32 < 1 << 30 || energy_q48 > 16u64 << 48 || angular_q32 > 4096u64 << 32 {
            return Err(Error::Range);
        }
        Ok(Self {
            energy: Words::new(energy_q48),
            angular: Words::new(angular_q32),
        })
    }
    /// (L² in Q64, β = 2/L² in Q62, α = (E² − 1)/L² in Q62 rounded toward zero, E² in Q96).
    fn radial(self, light: bool) -> (u128, i128, i128, u128) {
        let l = self.angular.get() as u128;
        let l2 = l * l;
        let e = self.energy.get() as u128;
        let e2 = e * e;
        if light {
            return (l2, 0, ((1u128 << 126) / l2) as i128, e2);
        }
        let (negative, num) = if e2 >= 1 << 96 { (false, e2 - (1 << 96)) } else { (true, (1 << 96) - e2) };
        let mag = ((num / l2) << 30) + (((num % l2) << 30) / l2);
        (l2, ((1u128 << 127) / l2) as i128, if negative { -(mag as i128) } else { mag as i128 }, e2)
    }
}

/// R(u) = 2u³ − u² + βu + α in Q62, products floored.
fn radial_at(u: i128, beta: i128, alpha: i128) -> i128 {
    let u2 = (u * u) >> 62;
    2 * ((u2 * u) >> 62) - u2 + ((beta * u) >> 62) + alpha
}

/// The last x in [lo, hi] with pred(x), given pred(lo) and !pred(hi): bisection to one unit.
fn bisect(mut lo: i128, mut hi: i128, pred: impl Fn(i128) -> bool) -> i128 {
    while hi - lo > 1 {
        let mid = (lo + hi) >> 1;
        if pred(mid) {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    lo
}

/// 2^(−k/16) in Q62, k ≥ 0.
fn edge(k: i32) -> i128 {
    EDGE[k.rem_euclid(16) as usize] >> k.div_euclid(16)
}
/// The band k with edge(k+1) < u ≤ edge(k), for 0 < u ≤ 1 (Q62).
pub fn band(u: i128) -> i32 {
    let octave = 62 - (128 - (u - 1).leading_zeros() as i32);
    let j = (1..16).take_while(|&j| u <= EDGE[j] >> octave).count() as i32;
    16 * octave + j
}

/// The compiled shape of one orbit: everything a position needs besides the crossing table.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Shape {
    /// Turning points (apoapsis, periapsis), centre, amplitude, u_3 − c: Q62.
    pub ua: i64,
    pub up: i64,
    pub c: i64,
    pub a: i64,
    pub m3: i64,
    newton: bool,
    /// P = 1/(L u_a²) = pm·2^−pe; E in Q48.
    pm: u128,
    pe: u32,
    e: u64,
}

const CAP: i128 = PI / 4;

impl Shape {
    fn bound(key: Key, newton: bool) -> Result<Self> {
        let (l2, beta, alpha, e2) = key.radial(false);
        if alpha >= 0 {
            return Err(Error::NoBoundOrbit);
        }
        let (ua, up, m3);
        if newton {
            // R = −u² + βu + α: roots β/2 ± sqrt(β²/4 + α); no third root (g = 1).
            let disc = ((beta * beta) >> 64) + alpha;
            if disc < -(1 << 16) {
                return Err(Error::NoBoundOrbit);
            }
            let s = isqrt((disc.max(0) as u128) << 62) as i128;
            (ua, up, m3) = (beta / 2 - s, beta / 2 + s, ONE);
        } else {
            if 6 * beta >= ONE {
                return Err(Error::NoBoundOrbit);
            }
            let k0 = isqrt(((ONE - 6 * beta) as u128) << 62) as i128;
            let uc = (ONE - k0) / 6;
            let k = ONE - 6 * uc;
            let l = key.angular.get() as i128;
            let y = (l * uc) >> 32;
            let v = ((ONE - 2 * uc) * (ONE + ((y * y) >> 62))) >> 62;
            let d = (e2 >> 34) as i128 - v;
            let rc = (d << 64) / l2 as i128;
            let r1 = 6 * ((uc * uc) >> 62) - 2 * uc + beta;
            let f = |x: i128| {
                let x2 = (x * x) >> 62;
                rc + ((r1 * x) >> 62) - ((k * x2) >> 62) + 2 * ((x2 * x) >> 62)
            };
            let (xp, xm) = if rc <= 0 {
                if d < -(1 << 16) {
                    return Err(Error::NoBoundOrbit);
                }
                (0, 0)
            } else {
                if f(k / 3) > 0 {
                    return Err(Error::NoBoundOrbit);
                }
                (bisect(0, k / 3, |x| f(x) > 0), bisect(-uc, 0, |x| f(x) <= 0) + 1)
            };
            ua = uc + xm;
            up = uc + xp;
            m3 = uc + k / 2 - xp - xm - ((ua + up) >> 1);
        }
        let (c, a) = ((ua + up) >> 1, (up - ua) >> 1);
        if ua < 1 << 34 || 2 * (m3 - a) < 1 << 20 {
            return Err(Error::Range);
        }
        // P = 1/(L u_a²): L·u_a (Q94) cut to 64 bits, times u_a, cut to 64 bits, reciprocal.
        let den = key.angular.get() as u128 * ua as u128;
        let sd = (128 - den.leading_zeros()).saturating_sub(64);
        let den2 = (den >> sd) * ua as u128;
        let s2 = (128 - den2.leading_zeros()).saturating_sub(64);
        let pm = (1u128 << 127) / (den2 >> s2);
        let pe = (s2 + sd).checked_sub(29).ok_or(Error::Range)?;
        Ok(Self {
            ua: ua as i64,
            up: up as i64,
            c: c as i64,
            a: a as i64,
            m3: m3 as i64,
            newton,
            pm,
            pe,
            e: key.energy.get(),
        })
    }

    /// ψ of the edge u_e, u_a < u_e < u_p (Q61).
    fn cut(&self, ue: i128) -> i128 {
        let (ua, up) = (self.ua as i128, self.up as i128);
        if 2 * ue >= ua + up {
            atan(ratio_sqrt(up - ue, ue - ua))
        } else {
            PI - atan(ratio_sqrt(ue - ua, up - ue))
        }
    }
    /// The outbound half's cuts: (band entered, ψ), in order.
    fn cuts(&self) -> impl Iterator<Item = (i32, i128)> + '_ {
        let (ua, up) = (self.ua as i128, self.up as i128);
        (band(up) + 1..)
            .take_while(move |&k| edge(k) > ua)
            .filter(move |&k| edge(k) < up)
            .map(move |k| (k, self.cut(edge(k))))
    }

    /// The node's integrands: (g in Q42, r_τ, r_t in Q62).
    fn node(&self, psi: i128, clocks: bool) -> Result<(i128, i128, i128)> {
        let acs = (self.a as i128 * cos(psi)) >> 62;
        let g = if self.newton {
            1 << 42
        } else {
            let d = 2 * (self.m3 as i128 - acs);
            if d < 1 << 20 {
                return Err(Error::Range);
            }
            isqrt(((1u128 << 126) / d as u128) << 20) as i128
        };
        if !clocks {
            return Ok((g, 0, 0));
        }
        let u = self.c as i128 + acs;
        let q = ((self.ua as i128) << 62) / u;
        let rtau = (q * q) >> 62;
        Ok((g, rtau, (rtau << 62) / (ONE - 2 * u)))
    }
    /// Four-point Gauss–Legendre on [lo, hi] into the sums (S_φ Q103, S_τ and S_t Q102).
    fn quad(&self, lo: i128, hi: i128, clocks: bool, sums: &mut [i128; 3]) -> Result<()> {
        let h = hi - lo;
        let mid = lo + (h >> 1);
        for i in 0..2 {
            let (dx, w) = ((X[i] * h) >> 63, (W[i] * h) >> 63);
            for psi in [mid - dx, mid + dx] {
                let (g, rtau, rt) = self.node(psi, clocks)?;
                let a = w * g;
                sums[0] += a;
                let b = a >> 63;
                sums[1] += b * rtau;
                sums[2] += b * rt;
            }
        }
        Ok(())
    }
    /// The panels of the interval [lo, hi] between two cuts, in order.
    fn panels(&self, lo: i128, hi: i128, first: bool, mut each: impl FnMut(i128, i128) -> Result<bool>) -> Result<()> {
        let mut a = lo;
        let mut split = |a: i128, b: i128| -> Result<bool> {
            let n = (b - a + CAP - 1) / CAP;
            for i in 0..n {
                if !each(a + (b - a) * i / n, a + (b - a) * (i + 1) / n)? {
                    return Ok(false);
                }
            }
            Ok(true)
        };
        let delta2 = 2 * (self.m3 as i128 - self.a as i128);
        if first && !self.newton && self.a > 0 && delta2 < 64 * self.a as i128 {
            let ratio = (delta2 << 60) / self.a as i128;
            let mut w = ((isqrt((ratio as u128) << 60) >> 1) as i128).max(1);
            while a + w < hi {
                if !split(a, a + w)? {
                    return Ok(());
                }
                a += w;
                w = a;
            }
        }
        split(a, hi).map(|_| ())
    }
    fn integrate(&self, lo: i128, hi: i128, first: bool, clocks: bool, sums: &mut [i128; 3]) -> Result<()> {
        self.panels(lo, hi, first, |a, b| self.quad(a, b, clocks, sums).map(|_| true))
    }
    /// Sums to (φ Q30, t Q20, τ Q20); `half` adds one shift (half-orbit values).
    fn convert(&self, sums: &[i128; 3], half: u32) -> Result<Increments> {
        let pos = |x: i128| u128::try_from(x).map_err(|_| Error::Range);
        let t = mul_shr(mul_shr(pos(sums[2])?, self.pm, 64)?, self.e as u128, self.pe + 65 + half)?;
        Ok(Increments {
            phi: words(pos(sums[0])? >> (72 + half))?,
            t: words(t)?,
            tau: words(mul_shr(pos(sums[1])?, self.pm, self.pe + 81 + half)?)?,
        })
    }
    /// u at ψ (Q62).
    pub fn u(&self, psi: i128) -> i128 {
        self.c as i128 + ((self.a as i128 * cos(psi)) >> 62)
    }
}

#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
pub struct Increments {
    pub phi: Words,
    pub t: Words,
    pub tau: Words,
}
impl Increments {
    fn add(self, o: Self) -> Result<Self> {
        let f = |a: Words, b: Words| a.get().checked_add(b.get()).map(Words::new).ok_or(Error::Range);
        Ok(Self { phi: f(self.phi, o.phi)?, t: f(self.t, o.t)?, tau: f(self.tau, o.tau)? })
    }
    fn sub(self, o: Self) -> Result<Self> {
        let f = |a: Words, b: Words| a.get().checked_sub(b.get()).map(Words::new).ok_or(Error::Range);
        Ok(Self { phi: f(self.phi, o.phi)?, t: f(self.t, o.t)?, tau: f(self.tau, o.tau)? })
    }
}
/// One band-edge crossing of the outbound half (periapsis to apoapsis).
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Crossing {
    /// The band entered, moving outward.
    pub band: i32,
    /// Darwin's phase at the crossing, Q61.
    pub psi: Words,
    /// Half-orbit values since periapsis: φ Q30, t and τ Q20.
    pub at: Increments,
}
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Cycle {
    pub key: Key,
    pub shape: Shape,
    /// Per radial cycle: φ Q30 (2π plus the advance), t and τ Q20.
    pub increments: Increments,
    /// The outbound half at apoapsis.
    pub half: Increments,
    pub crossings: Vec<Crossing>,
}
/// Where a tube is: derived from the compiled cycle, never evolved.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Position {
    /// Completed radial cycles since the epoch's periapsis.
    pub cycle: u64,
    /// Darwin's phase within the outbound half (Q61; the inbound half is mirrored).
    pub psi: i64,
    pub outbound: bool,
    /// u = 1/r, Q62.
    pub u: i64,
    pub band: i32,
    /// Since the epoch's periapsis: φ Q30 and τ Q20.
    pub phi: Words,
    pub tau: Words,
}

impl Cycle {
    /// Coordinate time t since periapsis (Q20) → where the tube is. Quotient and remainder, the
    /// mirror, a table search and one cell's panels: no previous cycle is evaluated.
    pub fn position(&self, elapsed: Words) -> Result<Position> {
        let period = self.increments.t.get();
        if period == 0 {
            return Err(Error::NotPeriodic);
        }
        let (n, r) = (elapsed.get() / period, elapsed.get() % period);
        let outbound = 2 * r <= period;
        let (psi, at) = self.outbound_at(if outbound { r } else { period - r })?;
        let at = if outbound { at } else { self.increments.sub(at)? };
        let base = self.repeat(n)?;
        let u = self.shape.u(psi);
        Ok(Position {
            cycle: n,
            psi: psi as i64,
            outbound,
            u: u as i64,
            band: band(u),
            phi: words(base.phi.get() as u128 + at.phi.get() as u128)?,
            tau: words(base.tau.get() as u128 + at.tau.get() as u128)?,
        })
    }
    /// ψ and the half-orbit values at time `target` (Q20) along the outbound half.
    fn outbound_at(&self, target: u64) -> Result<(i128, Increments)> {
        if target >= self.half.t.get() {
            return Ok((PI, self.half));
        }
        let s = &self.shape;
        let i = self.crossings.partition_point(|c| c.at.t.get() <= target);
        let (lo, base) = match i {
            0 => (0, Increments::default()),
            _ => (self.crossings[i - 1].psi.get() as i128, self.crossings[i - 1].at),
        };
        let hi = self.crossings.get(i).map_or(PI, |c| c.psi.get() as i128);
        let time = |sums: &[i128; 3]| -> Result<u64> { Ok(base.t.get() + s.convert(sums, 1)?.t.get()) };
        let mut sums = [0i128; 3];
        let mut found = None;
        s.panels(lo, hi, lo == 0, |a, b| {
            let mut next = sums;
            s.quad(a, b, true, &mut next)?;
            if time(&next)? > target {
                found = Some((a, b));
                return Ok(false);
            }
            sums = next;
            Ok(true)
        })?;
        let Some((a, b)) = found else {
            return Ok((hi, base.add(s.convert(&sums, 1)?)?));
        };
        // Bracketed Newton for ψ in [a, b] with time(sums + partial(a, ψ)) == target.
        let partial = |psi: i128| -> Result<[i128; 3]> {
            let mut p = sums;
            s.quad(a, psi, true, &mut p)?;
            Ok(p)
        };
        let (mut lo, mut hi, mut psi) = (a, b, a);
        for _ in 0..200 {
            let t = time(&partial(psi)?)?;
            if t == target || hi - lo <= 1 {
                break;
            }
            if t < target {
                lo = psi;
            } else {
                hi = psi;
            }
            // dt/dψ per radian in Q20: the node's integrand with a weight of one radian.
            let (g, _, rt) = s.node(psi, true)?;
            let rate = s.convert(&[0, 0, (g >> 2) * rt], 1)?.t.get().max(1) as i128;
            let step = (target as i128 - t as i128) * (1 << 61) / rate;
            let next = psi + step;
            psi = if next > lo && next < hi { next } else { lo + ((hi - lo) >> 1) };
        }
        Ok((psi, base.add(s.convert(&partial(psi)?, 1)?)?))
    }
    /// Repeat the compiled constants; never evolve a previous cycle's end.
    pub fn repeat(&self, n: u64) -> Result<Increments> {
        let mul = |w: Words| w.get().checked_mul(n).map(Words::new).ok_or(Error::Range);
        Ok(Increments {
            phi: mul(self.increments.phi)?,
            t: mul(self.increments.t)?,
            tau: mul(self.increments.tau)?,
        })
    }
}

/// A body or photon in a doll: its invariants, its epoch (Q20 coordinate time) and the time
/// since periapsis at that epoch (Q20). Position and clocks are derived when asked.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Tube {
    pub key: Key,
    pub epoch: Words,
    pub phase: Words,
}
impl Tube {
    pub fn position(&self, cycle: &Cycle, t: Words) -> Result<Position> {
        if cycle.key != self.key {
            return Err(Error::Range);
        }
        let since = t.get().checked_sub(self.epoch.get()).ok_or(Error::Range)?;
        cycle.position(words(since as u128 + self.phase.get() as u128)?)
    }
}

pub fn compile(key: Key) -> Result<Cycle> {
    compile_variant(key, false)
}
/// `newton = true` is the planted Newtonian law: the same machinery without the 2u³ term.
pub fn compile_variant(key: Key, newton: bool) -> Result<Cycle> {
    Key::new(key.energy.get(), key.angular.get())?;
    let shape = Shape::bound(key, newton)?;
    let mut sums = [0i128; 3];
    let mut crossings = Vec::new();
    let mut lo = 0;
    for (band, psi) in shape.cuts() {
        shape.integrate(lo, psi, lo == 0, true, &mut sums)?;
        crossings.push(Crossing { band, psi: Words::new(psi as u64), at: shape.convert(&sums, 1)? });
        lo = psi;
    }
    shape.integrate(lo, PI, lo == 0, true, &mut sums)?;
    Ok(Cycle {
        key,
        shape,
        increments: shape.convert(&sums, 0)?,
        half: shape.convert(&sums, 1)?,
        crossings,
    })
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Outcome {
    Absorbed,
    Escaped,
}
/// A body (`light = false`, E ≥ 1) or photon (`light = true`, E = 1, L = b) from infinity:
/// absorbed, or escaped with the angle from its turning point to infinity (Q30).
pub fn scatter(key: Key, light: bool) -> Result<(Outcome, Words)> {
    Key::new(key.energy.get(), key.angular.get())?;
    if light && key.energy.get() != 1 << 48 {
        return Err(Error::Range);
    }
    let (_, beta, alpha, _) = key.radial(light);
    if alpha < 0 {
        return Err(Error::Range);
    }
    if 6 * beta >= ONE {
        return Ok((Outcome::Absorbed, Words::default()));
    }
    let k0 = isqrt(((ONE - 6 * beta) as u128) << 62) as i128;
    let (umax, umin) = ((ONE - k0) / 6, (ONE + k0) / 6);
    if radial_at(umin, beta, alpha) > 0 {
        return Ok((Outcome::Absorbed, Words::default()));
    }
    let ut = bisect(umax, umin, |u| radial_at(u, beta, alpha) > 0);
    // The other roots: z² − Sz + P = 0 with S = 1/2 − u_t, P = β/2 − u_t S.
    let sum = (ONE >> 1) - ut;
    let prod = (beta >> 1) - ((ut * sum) >> 62);
    let disc = (((sum * sum) >> 62) - 4 * prod).max(0);
    let sq = isqrt((disc as u128) << 62) as i128;
    let (u0, u3) = (((sum - sq) >> 1).min(0), (sum + sq) >> 1);
    let (c, a) = ((ut + u0) >> 1, (ut - u0) >> 1);
    let shape = Shape { ua: u0 as i64, up: ut as i64, c: c as i64, a: a as i64, m3: (u3 - c) as i64, newton: false, pm: 0, pe: 0, e: 0 };
    if 2 * (u3 - ut) < 1 << 20 {
        return Err(Error::Range);
    }
    let psi0 = match u0 {
        0 => PI,
        _ if ut <= -u0 => atan(ratio_sqrt(ut, -u0)),
        _ => PI - atan(ratio_sqrt(-u0, ut)),
    };
    let mut sums = [0i128; 3];
    shape.integrate(0, psi0, true, false, &mut sums)?;
    Ok((Outcome::Escaped, words(sums[0] as u128 >> 73)?))
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

/// Signed first differences of the increments over explicit key steps. A kick's multiply-add
/// through them is a predictor; the recompiled key is the authority.
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
        let step = |de: u64, dl: u64| {
            let e = c.key.energy.get().checked_add(de).ok_or(Error::Range)?;
            let l = c.key.angular.get().checked_add(dl).ok_or(Error::Range)?;
            compile(Key::new(e, l)?)
        };
        let (ce, cl) = (step(energy_step, 0)?, step(0, angular_step)?);
        let topology = |x: &Cycle| x.crossings.iter().map(|a| a.band).eq(c.crossings.iter().map(|a| a.band));
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
    /// Prediction only. Recompile before any canonical decision.
    pub fn predict(&self, base: Increments, de: i64, dl: i64) -> Result<Increments> {
        let mut v = values(base);
        for (i, x) in v.iter_mut().enumerate() {
            let e = self.energy_diff[i].get() as i64 as i128 * de as i128 / self.energy_step.get() as i128;
            let l = self.angular_diff[i].get() as i64 as i128 * dl as i128 / self.angular_step.get() as i128;
            *x = u64::try_from(*x as i128 + e + l).map_err(|_| Error::Range)?;
        }
        Ok(Increments { phi: Words::new(v[0]), t: Words::new(v[1]), tau: Words::new(v[2]) })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn key() -> Key {
        Key::darwin(20 << 16, 1 << 29).unwrap()
    }
    #[test]
    fn bands_from_bits_agree_with_the_edges() {
        for k in 16..400 {
            assert_eq!(band(edge(k)), k, "at edge {k}");
            assert_eq!(band(edge(k) - 1), k, "inside {k}");
            assert_eq!(band(edge(k) + 1), k - 1, "outside {k}");
        }
    }
    #[test]
    fn bit_identical_compilation_and_memo_hits() {
        let a = compile(key()).unwrap();
        assert_eq!(a, compile(key()).unwrap());
        let mut memo = Memo::default();
        let (c, d) = (memo.get(key()).unwrap(), memo.get(key()).unwrap());
        assert!(Arc::ptr_eq(&c, &d));
        assert_eq!(memo.len(), 1);
        assert_eq!(a.repeat(10000).unwrap().phi.get(), a.increments.phi.get() * 10000);
    }
    #[test]
    fn the_crossing_table_is_ordered_and_mirrors() {
        let c = compile(key()).unwrap();
        assert!(!c.crossings.is_empty());
        for w in c.crossings.windows(2) {
            assert_eq!(w[1].band, w[0].band + 1);
            let g = |x: &Crossing| [x.psi.get(), x.at.phi.get(), x.at.t.get(), x.at.tau.get()];
            assert!(g(&w[1]).iter().zip(g(&w[0])).all(|(b, a)| *b > a), "{w:?}");
        }
        let period = c.increments.t.get();
        for f in [1u64, 3, 5, 7, 11] {
            let t = period * f / 23;
            let (a, b) = (c.position(Words::new(t)).unwrap(), c.position(Words::new(period - t)).unwrap());
            assert!(a.outbound && !b.outbound);
            assert_eq!((a.u, a.band), (b.u, b.band));
            assert_eq!(a.phi.get() + b.phi.get(), c.increments.phi.get());
        }
    }
    #[test]
    fn a_position_at_a_crossing_time_is_on_its_edge() {
        let c = compile(key()).unwrap();
        for x in &c.crossings {
            let p = c.position(x.at.t).unwrap();
            let e = edge(x.band);
            assert!((p.u as i128 - e).abs() < e >> 20, "u {} edge {e}", p.u);
        }
    }
    #[test]
    fn zero_kick_is_identity_and_probe_step_is_its_first_difference() {
        let c = compile(key()).unwrap();
        let t = Tangent::create(&c, 1 << 24, 1 << 16).unwrap();
        assert_eq!(t.predict(c.increments, 0, 0).unwrap(), c.increments);
        let perturbed = Key::new(c.key.energy.get() + (1 << 24), c.key.angular.get()).unwrap();
        assert_eq!(t.predict(c.increments, 1 << 24, 0).unwrap(), compile(perturbed).unwrap().increments);
    }
    #[test]
    fn the_planted_newtonian_law_closes() {
        let c = compile_variant(key(), true).unwrap();
        let tau = 6746518852u64; // 2π in Q30
        assert!(c.increments.phi.get().abs_diff(tau) < 8, "{:?}", c.increments);
    }
    #[test]
    fn invalid_inputs_are_explicit_errors() {
        assert_eq!(Key::new(1 << 48, 1), Err(Error::Range));
        assert_eq!(Key::new(0, 4 << 32), Err(Error::Range));
        assert_eq!(scatter(Key::new(2 << 48, 4 << 32).unwrap(), true), Err(Error::Range));
        assert_eq!(Key::darwin(u32::MAX, 1 << 29), Err(Error::NoBoundOrbit));
        assert_eq!(Key::darwin(5 << 16, 0), Err(Error::NoBoundOrbit));
        assert_eq!(compile(Key { energy: Words::new(0), angular: Words::new(0) }), Err(Error::Range));
        // Unbound and plunging keys are not cycles.
        assert_eq!(compile(Key::new(1 << 48, 5 << 32).unwrap()).map(|_| ()), Err(Error::NoBoundOrbit));
        assert_eq!(compile(Key::new((1 << 48) - (1 << 40), 3 << 32).unwrap()).map(|_| ()), Err(Error::NoBoundOrbit));
    }
    #[test]
    fn capture_cases_are_answered_not_errors_disguised_as_escape() {
        for factor in [0.5f64, 0.9, 0.97, 1.03, 1.1, 1.5] {
            let key = Key::new(1 << 48, (4.0 * factor * 4294967296.0).round() as u64).unwrap();
            let (out, _) = scatter(key, false).unwrap();
            assert_eq!(out == Outcome::Absorbed, factor < 1.0);
        }
        for factor in [0.9f64, 0.97, 1.03, 1.1] {
            let key = Key::new(1 << 48, (3.0 * 3f64.sqrt() * factor * 4294967296.0).round() as u64).unwrap();
            let (out, _) = scatter(key, true).unwrap();
            assert_eq!(out == Outcome::Absorbed, factor < 1.0);
        }
    }
}
