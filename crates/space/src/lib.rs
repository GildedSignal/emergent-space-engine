//! # Law `space-darwin16-v2`: the cycle compiler of one doll (one static mass)
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
//! A shared cycle is keyed by E (Q48) and L (Q32); a 16-byte tube stores epoch and phase. Its radial function
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
//! Envelope: u_a ≥ 2^−28, u_p < 1/3 and 2(u_3 − u_p) ≥ 2^−42, else `Range`.
//!
//! ## Cells and panels
//! Band k holds 2^(−(k+1)/16) < u ≤ 2^(−k/16); its edges are `EDGE[j] >> octave`. The outbound
//! half (ψ from 0 to π) crosses every edge u_e with u_a < u_e < u_p, at
//!   ψ_e = atan(ratio_sqrt(u_p − u_e, u_e − u_a))       if 2u_e ≥ u_a + u_p,
//!   ψ_e = π − atan(ratio_sqrt(u_e − u_a, u_p − u_e))    otherwise
//! (2·atan in Q61 is the Q62 atan's integer). These cuts are the crossing table. Each interval
//! between cuts splits into ceil(width/(π/4)) equal panels (endpoints floored). Near the
//! separatrix every interval also intersects one global dyadic grid: if 2δ < 64A, δ = m₃ − A, λ =
//! isqrt(floor(2δ·2^60/A)·2^60)/2 (a quarter of the peak's width sqrt(2δ/A)), and the panels
//! [0, λ], [λ, 2λ], [2λ, 4λ], … (each split by π/4 too) are clipped at every band cut.
//! Refinement continues past the first band; a cut cannot erase the nearby singularity.
//!
//! ## Quadrature (the time rule is the same rule)
//! Four-point Gauss–Legendre on each panel [a, b]: h = b − a, mid = a + h/2, nodes
//! mid ± floor(X_i·h/2^63), weights ω_i = floor(W_i·h/2^63). At a node: u = c + floor(A·cos ψ),
//! d = 2(m₃ − floor(A·cos ψ)) (≥ 2^20, else `Range`), g = isqrt(floor(2^126/d)·2^20) (Q42),
//! q = floor(u_a·2^62/u), r_τ = floor(q²/2^62), r_t = floor(r_τ·2^62/(2^62 − 2u)). The sums gain
//! S_φ += ω g (Q103), and with b = floor(ω g/2^s): S_τ += b r_τ, S_t += b r_t (Q(165−s)).
//! s=max(55,1+bit_length(g_max)), with g_max bounded using d_min−64 Q62 units. Thus
//! ordinary panels retain Q48 weighted g, while conditioned panels shift enough to fit i128.
//! P = 1/(L u_a²) is p_m·2^(−p_e): the Q94 product L·u_a is cut to its top 64 bits, times u_a,
//! cut to its top 64 bits d₂, then p_m = floor(2^127/d₂). Over the half orbit (doubled for the
//! cycle, one shift less): Δφ = floor(S_φ/2^72) (Q30), Δτ = floor(p_m S_τ / 2^(p_e+144−s)) and
//! Δt = floor(floor(p_m S_t/2^64)·E / 2^(p_e+128−s)) (Q20). The crossing table stores the same
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
//! - quadrature: on a panel of FULL width h, error ≤ h^9 B₈/44100, where B₈ bounds
//!   |f⁽⁸⁾|/8!. `QUADRATURE.md` in this crate proves a positive recurrence for B₈ from
//!   the panel's real denominator minima. This replaces v1's unproved ellipse assertion;
//! - rounding: fixed-point arithmetic is the exact law, not exact real quadrature. Error
//!   depends on 1/u and 1/(u₃−u); there is no proven uniform 2^−30 relative bound;
//! - roots: the integer predicate is bisected to one Q62 unit. Its rounded residual is
//!   amplified by 1/|R′| at simple roots and by a square root near double roots, so this
//!   does NOT imply one-unit continuum root accuracy. Input E/L quantization is separate.
//! The law differs from continuum GR by these and by the key's quantization of (E, L).
//!
//! The planted Newtonian variant (`compile_variant(key, true)`) drops the 2u³ term: g = 1, so
//! the advance is zero and the precession gate must kill it.
//!
//! ## Consumer API
//! Coordinates are polar around a static mass: r=1/u, positive L is prograde, φ=0 at
//! periapsis. t is Schwarzschild coordinate time and τ is proper time. To restore a doll's
//! mass M, multiply r, t, τ and L by M; frames, orientation and retarded handoffs belong
//! to the caller. `Tube` describes bound massive bodies; use [`scatter`] for unbound/light.
//! Keys are exact Q48 E / Q32 L; [`Key::darwin`] accepts Q16 p / Q30 e. [`LAW_ID`] includes
//! the boundary conversion convention. `Range`, `NoBoundOrbit` and `Topology` are refusals,
//! never invitations to silently clamp a new key or apply an uncertified kick.
//!
//! ```
//! use emergent_space::{Cycle, Key, Tangent, Tube, Words};
//! let key = Key::darwin(20 << 16, 1 << 29)?; // p=20, e=0.5
//! let cycle = Cycle::compile(key)?;         // share this, or use Memo::get
//! let tube = Tube::new(Words::new(0), Words::new(0));
//! let state = tube.state(&cycle, cycle.half.t)?;
//! assert_eq!(state.velocity.radial, 0);     // at apoapsis
//! let response = Tangent::centered(&cycle, 1 << 25, key.angular.get() >> 11)?;
//! let prediction = response.predict(cycle.increments, 1 << 20, -(1 << 10))?;
//! // Prediction is for scheduling/refinement. Compile the kicked key before committing it.
//! # let _ = prediction;
//! # Ok::<(), emergent_space::Error>(())
//! ```

mod num;
#[cfg(feature = "profile")]
pub mod profile;
#[cfg(test)]
mod quadrature_tests;
mod tables;

macro_rules! stage {
    ($i:expr, $e:expr) => {{
        #[cfg(feature = "profile")]
        {
            crate::profile::stage($i, || $e)
        }
        #[cfg(not(feature = "profile"))]
        {
            $e
        }
    }};
}

use std::collections::BTreeMap;
use std::sync::Arc;

use num::{atan, cos, isqrt, mul_shr, ratio_sqrt, ONE};
use tables::{EDGE, PI, W, X};

/// Integer law and boundary-quantization version. Never reuse a memo across law versions.
pub const LAW_ID: &str = "space-darwin16-v2";

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
#[repr(transparent)]
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
    pub const ENERGY_FRACTION_BITS: u32 = 48;
    pub const ANGULAR_FRACTION_BITS: u32 = 32;
    pub const DARWIN_P_FRACTION_BITS: u32 = 16;
    pub const ECCENTRICITY_FRACTION_BITS: u32 = 30;
    /// Boundary input: Darwin's p in Q16 and e in Q30. No float decisions.
    /// L is floored first; E is then floored from V(u_p, L), so the rounded L does not
    /// lift a near-circular orbit above its barrier. At e=0 use that L's stable minimum.
    /// This input conversion is version 2; `new` preserves already quantized invariants.
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
        let angular = isqrt((l2 << 16) as u128);
        let u = if eccentricity == 0 {
            let beta = ((1u128 << 127) / (angular * angular)) as i128;
            if 6 * beta >= ONE {
                return Err(Error::NoBoundOrbit);
            }
            (ONE - isqrt(((ONE - 6 * beta) as u128) << 62) as i128) / 6
        } else {
            ((Q48 + e) << 62) / p
        };
        let y = (angular as i128 * u) >> 32;
        let v = ((ONE - 2 * u) * (ONE + ((y * y) >> 62))) >> 62;
        Ok(Self {
            energy: words(isqrt((v as u128) << 34))?,
            angular: words(angular)?,
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
        let (negative, num) = if e2 >= 1 << 96 {
            (false, e2 - (1 << 96))
        } else {
            (true, (1 << 96) - e2)
        };
        let mag = ((num / l2) << 30) + (((num % l2) << 30) / l2);
        (
            l2,
            ((1u128 << 127) / l2) as i128,
            if negative { -(mag as i128) } else { mag as i128 },
            e2,
        )
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
    /// First global dyadic phase cut, Q61, or zero when refinement is unnecessary.
    lambda: Words,
    /// Shift the weighted node before multiplying the clock ratios; see the law's bound.
    clock_shift: u32,
}

const CAP: i128 = PI / 4;

impl Shape {
    fn refinement_width(a: i128, m3: i128, newton: bool) -> Words {
        let d = 2 * (m3 - a);
        let w = if !newton && a > 0 && d < 64 * a {
            (isqrt((((d << 60) / a) as u128) << 60) >> 1).max(1) as u64
        } else {
            0
        };
        Words::new(w)
    }
    fn bound(key: Key, newton: bool) -> Result<Self> {
        let (l2, beta, alpha, e2) = key.radial(false);
        if alpha >= 0 {
            return Err(Error::NoBoundOrbit);
        }
        let (ua, up, m3);
        if newton {
            // A Newtonian control outside the exterior envelope is not a GR doll;
            // reject it before beta² could overflow on small-L keys.
            if beta >= 2 * ONE / 3 {
                return Err(Error::Range);
            }
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
        if ua < 1 << 34 || up >= ONE / 3 || 2 * (m3 - a) < 1 << 20 {
            return Err(Error::Range);
        }
        // P = 1/(L u_a²): L·u_a (Q94) cut to 64 bits, times u_a, cut to 64 bits, reciprocal.
        let den = key.angular.get() as u128 * ua as u128;
        let sd = (128 - den.leading_zeros()).saturating_sub(64);
        let den2 = (den >> sd) * ua as u128;
        let s2 = (128 - den2.leading_zeros()).saturating_sub(64);
        let pm = (1u128 << 127) / (den2 >> s2);
        let pe = (s2 + sd).checked_sub(29).ok_or(Error::Range)?;
        // cos's error cannot reduce d by 64 Q62 units. Σ weights <2^63 and each
        // clock ratio <2^64; s>bit_length(g_max) keeps each half sum below 2^126.
        let gmax = if newton {
            1u128 << 42
        } else {
            isqrt(((1u128 << 126) / (2 * (m3 - a) - 64) as u128) << 20)
        };
        let clock_shift = 55.max(129 - gmax.leading_zeros());
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
            lambda: Self::refinement_width(a, m3, newton),
            clock_shift,
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
    fn node(&self, psi: i128, clocks: bool) -> Result<(u64, u64, u64)> {
        let cs = cos(psi) as i64;
        let acs = (self.a as i128 * cs as i128) >> 62;
        let g = if self.newton {
            1 << 42
        } else {
            let d = 2 * (self.m3 as i128 - acs);
            if d < 1 << 20 {
                return Err(Error::Range);
            }
            isqrt(((1u128 << 126) / d as u128) << 20) as u64
        };
        if !clocks {
            return Ok((g, 0, 0));
        }
        let u = self.c as i128 + acs;
        let q = (((self.ua as i128) << 62) / u) as u64;
        let rtau = ((q as u128 * q as u128) >> 62) as u64;
        Ok((g, rtau, (((rtau as u128) << 62) / (ONE - 2 * u) as u128) as u64))
    }
    /// Four-point GL on [lo, hi]: S_φ Q103, clocks Q(165-clock_shift).
    fn quad(&self, lo: i128, hi: i128, clocks: bool, sums: &mut [i128; 3]) -> Result<()> {
        let h = hi - lo;
        let mid = lo + (h >> 1);
        for i in 0..2 {
            let (dx, w) = ((X[i] * h) >> 63, (W[i] * h) >> 63);
            for psi in [mid - dx, mid + dx] {
                let (g, rtau, rt) = self.node(psi, clocks)?;
                let a = w as u64 as u128 * g as u128;
                sums[0] += a as i128;
                let b = (a >> self.clock_shift) as u64;
                sums[1] += (b as u128 * rtau as u128) as i128;
                sums[2] += (b as u128 * rt as u128) as i128;
            }
        }
        Ok(())
    }
    /// The panels of the interval [lo, hi] between two cuts, in order.
    fn panels(&self, lo: i128, hi: i128, mut each: impl FnMut(i128, i128) -> Result<bool>) -> Result<()> {
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
        let mut cut = self.lambda.get() as i128;
        if cut > 0 {
            while cut <= lo {
                cut *= 2;
            }
            while cut < hi {
                if !split(a, cut)? {
                    return Ok(());
                }
                a = cut;
                cut *= 2;
            }
        }
        split(a, hi).map(|_| ())
    }
    fn integrate(&self, lo: i128, hi: i128, clocks: bool, sums: &mut [i128; 3]) -> Result<()> {
        self.panels(lo, hi, |a, b| self.quad(a, b, clocks, sums).map(|_| true))
    }
    /// Sums to (φ Q30, t Q20, τ Q20); `half` adds one shift (half-orbit values).
    fn convert(&self, sums: &[i128; 3], half: u32) -> Result<Increments> {
        let [phi, t, tau] = self.convert_guarded(sums, half, 0)?;
        Ok(Increments {
            phi: words(phi)?,
            t: words(t)?,
            tau: words(tau)?,
        })
    }
    /// Retain guard bits for response differences before final output rounding.
    fn convert_guarded(&self, sums: &[i128; 3], half: u32, guard: u32) -> Result<[u128; 3]> {
        let pos = |x: i128| u128::try_from(x).map_err(|_| Error::Range);
        let t = mul_shr(
            mul_shr(pos(sums[2])?, self.pm, 64)?,
            self.e as u128,
            self.pe + 128 + half - self.clock_shift - guard,
        )?;
        Ok([
            pos(sums[0])? >> (72 + half - guard),
            t,
            mul_shr(pos(sums[1])?, self.pm, self.pe + 144 + half - self.clock_shift - guard)?,
        ])
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
        Ok(Self {
            phi: f(self.phi, o.phi)?,
            t: f(self.t, o.t)?,
            tau: f(self.tau, o.tau)?,
        })
    }
    fn sub(self, o: Self) -> Result<Self> {
        let f = |a: Words, b: Words| a.get().checked_sub(b.get()).map(Words::new).ok_or(Error::Range);
        Ok(Self {
            phi: f(self.phi, o.phi)?,
            t: f(self.t, o.t)?,
            tau: f(self.tau, o.tau)?,
        })
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

/// Polar coordinate velocity in Schwarzschild coordinate time, in units c=1.
/// Both components are signed Q30: dr/dt and r*dφ/dt. These are NOT local orthonormal
/// frame components. The positive-L cycle is prograde; outbound radial velocity is positive.
/// This is the smooth generator's tangent at the integer readout, rounded toward zero,
/// not a derivative of a staircase of quantized positions.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Velocity {
    pub radial: i32,
    pub transverse: i32,
}

/// A readout and its tangent. Neither is stored per entity.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct State {
    pub position: Position,
    pub velocity: Velocity,
}

impl Cycle {
    /// Compile the exact key; equivalent to [`compile`].
    pub fn compile(key: Key) -> Result<Self> {
        compile(key)
    }

    /// Read position and coordinate velocity without evolving any prior state.
    pub fn state(&self, elapsed: Words) -> Result<State> {
        let position = self.position(elapsed)?;
        let s = &self.shape;
        let psi = position.psi as i128;
        let u = position.u as i128;
        let lapse = ONE - 2 * u;
        let l = self.key.angular.get() as i128;
        let e = self.key.energy.get() as i128;
        // Wide temporaries preserve Q62 shape conditioning (see QUADRATURE.md).
        let transverse = (((l * u) >> 32) * lapse) >> 62;
        let sin = cos((psi - PI / 2).abs());
        let radial = (((((s.a as i128 * sin) >> 62) * l) >> 32) * lapse) >> 62;
        let (g, _, _) = s.node(psi, false)?;
        let radial = (radial << 58) / (e * g as i128);
        let sign = if position.outbound { 1 } else { -1 };
        let velocity = Velocity {
            radial: i32::try_from(sign * radial).map_err(|_| Error::Range)?,
            transverse: i32::try_from((transverse << 16) / e).map_err(|_| Error::Range)?,
        };
        Ok(State { position, velocity })
    }
    /// Coordinate time t since periapsis (Q20) → where the tube is. Quotient and remainder, the
    /// mirror, a table search and one cell's panels: no previous cycle is evaluated.
    pub fn position(&self, elapsed: Words) -> Result<Position> {
        let period = self.increments.t.get();
        if period == 0 {
            return Err(Error::NotPeriodic);
        }
        let (n, r) = (elapsed.get() / period, elapsed.get() % period);
        let outbound = r <= period / 2;
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
        if target == 0 {
            return Ok((0, Increments::default()));
        }
        if target >= self.half.t.get() {
            return Ok((PI, self.half));
        }
        let s = &self.shape;
        let i = self.crossings.partition_point(|c| c.at.t.get() <= target);
        let (lo, base) = match i {
            0 => (0, Increments::default()),
            _ => (self.crossings[i - 1].psi.get() as i128, self.crossings[i - 1].at),
        };
        if target == base.t.get() {
            return Ok((lo, base));
        }
        let hi = self.crossings.get(i).map_or(PI, |c| c.psi.get() as i128);
        let time = |sums: &[i128; 3]| -> Result<u64> { Ok(base.t.get() + s.convert(sums, 1)?.t.get()) };
        let mut sums = [0i128; 3];
        let mut found = None;
        s.panels(lo, hi, |a, b| {
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
            let rate = s
                .convert(&[0, 0, (((g as i128) << 61) >> s.clock_shift) * rt as i128], 1)?
                .t
                .get()
                .max(1) as i128;
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

/// Sixteen-byte phase/epoch record for a bound body in a doll. Epoch and phase are Q20
/// coordinate times. The owning population holds the shared Cycle/key, not each Tube.
/// Pass that same cycle to every read; this record deliberately contains no cycle handle.
/// A doll handoff must bind a new cycle and rebase the phase/epoch explicitly.
/// Times before epoch and overflowing accumulated phases return `Range`; no wrapping.
#[repr(C)]
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Tube {
    pub epoch: Words,
    pub phase: Words,
}
impl Tube {
    pub const fn new(epoch: Words, phase: Words) -> Self {
        Self { epoch, phase }
    }
    fn elapsed(&self, t: Words) -> Result<Words> {
        let since = t.get().checked_sub(self.epoch.get()).ok_or(Error::Range)?;
        since.checked_add(self.phase.get()).map(Words::new).ok_or(Error::Range)
    }
    pub fn position(&self, cycle: &Cycle, t: Words) -> Result<Position> {
        cycle.position(self.elapsed(t)?)
    }
    pub fn state(&self, cycle: &Cycle, t: Words) -> Result<State> {
        cycle.state(self.elapsed(t)?)
    }
}

pub fn compile(key: Key) -> Result<Cycle> {
    compile_variant(key, false)
}
/// `newton = true` is the planted Newtonian law: the same machinery without the 2u³ term.
pub fn compile_variant(key: Key, newton: bool) -> Result<Cycle> {
    compile_sums(key, newton).map(|(cycle, _)| cycle)
}
fn compile_sums(key: Key, newton: bool) -> Result<(Cycle, [i128; 3])> {
    Key::new(key.energy.get(), key.angular.get())?;
    let shape = stage!(0, Shape::bound(key, newton))?;
    let mut sums = [0i128; 3];
    let mut crossings = Vec::new();
    let mut lo = 0;
    let mut cuts = shape.cuts();
    while let Some((band, psi)) = stage!(1, cuts.next()) {
        stage!(2, shape.integrate(lo, psi, true, &mut sums))?;
        crossings.push(Crossing {
            band,
            psi: Words::new(psi as u64),
            at: stage!(3, shape.convert(&sums, 1))?,
        });
        lo = psi;
    }
    stage!(2, shape.integrate(lo, PI, true, &mut sums))?;
    Ok((
        Cycle {
            key,
            shape,
            increments: shape.convert(&sums, 0)?,
            half: shape.convert(&sums, 1)?,
            crossings,
        },
        sums,
    ))
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
    let shape = Shape {
        ua: u0 as i64,
        up: ut as i64,
        c: c as i64,
        a: a as i64,
        m3: (u3 - c) as i64,
        newton: false,
        pm: 0,
        pe: 0,
        e: 0,
        lambda: Shape::refinement_width(a, u3 - c, false),
        clock_shift: 63,
    };
    if 2 * (u3 - ut) < 1 << 20 {
        return Err(Error::Range);
    }
    let psi0 = match u0 {
        0 => PI,
        _ if ut <= -u0 => atan(ratio_sqrt(ut, -u0)),
        _ => PI - atan(ratio_sqrt(-u0, ut)),
    };
    let mut sums = [0i128; 3];
    shape.integrate(0, psi0, false, &mut sums)?;
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
    /// Extra numerator fraction bits: 0 for forward output secants, 16 for central responses.
    pub guard_bits: u32,
}

/// A signed rational derivative in encoded output units per encoded key unit.
/// `difference` is two's-complement i64 in two storage words; `step` is positive.
/// For physical units multiply by 2^(input_fraction_bits - output_fraction_bits - guard_bits).
/// Output order is (Δφ Q30, Δt Q20, Δτ Q20); inputs are E Q48 and L Q32.
/// A quantized law has no infinitesimal derivative: these are explicit finite differences.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Derivative {
    pub difference: Words,
    pub step: Words,
    pub guard_bits: u32,
}
impl Derivative {
    pub const fn numerator(self) -> i64 {
        self.difference.get() as i64
    }
    /// Multiply by a signed key kick and truncate toward zero. 64×64 can require
    /// 126 signed product bits; this is the reason for the i128 temporary here.
    pub fn apply(self, kick: i64) -> Result<i128> {
        if self.guard_bits > 32 || self.step.get() == 0 {
            return Err(Error::Range);
        }
        Ok(self.numerator() as i128 * kick as i128 / ((self.step.get() as i128) << self.guard_bits))
    }
}
fn values(i: Increments) -> [u64; 3] {
    [i.phi.get(), i.t.get(), i.tau.get()]
}
fn differences(a: Increments, b: Increments) -> Result<[Words; 3]> {
    wide_differences(values(a).map(u128::from), values(b).map(u128::from))
}
fn wide_differences(a: [u128; 3], b: [u128; 3]) -> Result<[Words; 3]> {
    let mut out = [Words::default(); 3];
    for i in 0..3 {
        let x = i128::try_from(a[i]).map_err(|_| Error::Range)?;
        let y = i128::try_from(b[i]).map_err(|_| Error::Range)?;
        let d = i64::try_from(y - x).map_err(|_| Error::Range)?;
        out[i] = Words::new(d as u64);
    }
    Ok(out)
}
impl Tangent {
    /// Forward secants. A boundary key may have no finite admissible two-sided derivative.
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
            guard_bits: 0,
        })
    }
    /// Central derivatives over ± the supplied Q48/Q32 steps. Sixteen extra output
    /// fraction bits prevent subtraction of Q20 clocks from drowning small derivatives.
    /// All four probes must
    /// remain bound and have the base crossing topology, else an explicit error.
    /// Compile once per response tile, not once per Tube. No Hessian/remainder is certified.
    /// Probe size is part of the derivative: very small steps amplify rounded-root noise.
    /// The independent oracle checks E steps 2^25 and L steps key.angular/2048 on p=8.2..1000;
    /// these are not universal safe steps, and a topology refusal requires refinement.
    pub fn centered(c: &Cycle, energy_step: u64, angular_step: u64) -> Result<Self> {
        let es = energy_step.checked_mul(2).filter(|&s| s != 0).ok_or(Error::Range)?;
        let ls = angular_step.checked_mul(2).filter(|&s| s != 0).ok_or(Error::Range)?;
        let probe = |de: i128, dl: i128| -> Result<[u128; 3]> {
            let e = u64::try_from(c.key.energy.get() as i128 + de).map_err(|_| Error::Range)?;
            let l = u64::try_from(c.key.angular.get() as i128 + dl).map_err(|_| Error::Range)?;
            let (x, sums) = compile_sums(Key::new(e, l)?, false)?;
            if !x.crossings.iter().map(|a| a.band).eq(c.crossings.iter().map(|a| a.band)) {
                return Err(Error::Topology);
            }
            x.shape.convert_guarded(&sums, 0, 16)
        };
        Ok(Self {
            energy_step: Words::new(es),
            angular_step: Words::new(ls),
            energy_diff: wide_differences(probe(-(energy_step as i128), 0)?, probe(energy_step as i128, 0)?)?,
            angular_diff: wide_differences(probe(0, -(angular_step as i128))?, probe(0, angular_step as i128)?)?,
            guard_bits: 16,
        })
    }
    pub fn d_energy(&self) -> [Derivative; 3] {
        self.energy_diff.map(|difference| Derivative {
            difference,
            step: self.energy_step,
            guard_bits: self.guard_bits,
        })
    }
    pub fn d_angular(&self) -> [Derivative; 3] {
        self.angular_diff.map(|difference| Derivative {
            difference,
            step: self.angular_step,
            guard_bits: self.guard_bits,
        })
    }
    /// Prediction only. Recompile before any canonical decision.
    pub fn predict(&self, base: Increments, de: i64, dl: i64) -> Result<Increments> {
        let mut v = values(base);
        if self.energy_step.get() == 0 || self.angular_step.get() == 0 {
            return Err(Error::Range);
        }
        for (i, x) in v.iter_mut().enumerate() {
            let e = self.d_energy()[i].apply(de)?;
            let l = self.d_angular()[i].apply(dl)?;
            let sum = (*x as i128).checked_add(e).and_then(|s| s.checked_add(l)).ok_or(Error::Range)?;
            *x = u64::try_from(sum).map_err(|_| Error::Range)?;
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
        assert_eq!(
            compile_variant(Key::new((1 << 48) - 1, 1 << 30).unwrap(), true).map(|_| ()),
            Err(Error::Range)
        );
        assert_eq!(
            compile(Key {
                energy: Words::new(0),
                angular: Words::new(0)
            }),
            Err(Error::Range)
        );
        // Unbound and plunging keys are not cycles.
        assert_eq!(compile(Key::new(1 << 48, 5 << 32).unwrap()).map(|_| ()), Err(Error::NoBoundOrbit));
        assert_eq!(
            compile(Key::new((1 << 48) - (1 << 40), 3 << 32).unwrap()).map(|_| ()),
            Err(Error::NoBoundOrbit)
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
            let key = Key::new(1 << 48, (3.0 * 3f64.sqrt() * factor * 4294967296.0).round() as u64).unwrap();
            let (out, _) = scatter(key, true).unwrap();
            assert_eq!(out == Outcome::Absorbed, factor < 1.0);
        }
    }
}
