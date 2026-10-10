//! Lifted boosts and rotations: integer shears (docs/law.md, "Handoffs are Lorentz, exactly invertible"; Paeth 1986,
//! Daubechies and Sweldens 1998; the Opus math memo, R3).
//!
//! A shear `x ← x + ⌊a·y⌋` rounds once, by an exact integer division, and `x ← x − ⌊a·y⌋` undoes it bit for bit, so a
//! product of shears is a bijection of the integer vectors it acts on, whatever the rounding. Three shears make a
//! rotation and three a boost:
//!
//! ```text
//!   R(φ)  = S_x(a)·S_y(b)·S_x(a),   a = −tan(φ/2),   b = sin φ                    (x ← x + ⌊a·y⌋, y ← y + ⌊b·x⌋)
//!   B(η)  = S_g(a)·S_u(b)·S_g(a),   a = −tanh(η/2),  b = −sinh η = 2a/(1 − a²)    (g ← g + ⌊a·u⌋, u ← u + ⌊b·g⌋)
//! ```
//!
//! whose unrounded products are exactly the rotation and the boost (equal diagonals, determinant one). A boost in any
//! direction in 2+1 is a rotation to the axis, the boost, and the rotation back: nine shears.
//!
//! **What they act on.** The vectors that transform linearly under a boost are events `(t, x)` and four-velocities
//! `(g, u) = (γ, γ·v)`; a coordinate velocity does not (it composes by a Möbius map, which is no bijection of integer
//! words). So a velocity is lifted to an integer four-velocity with extra fractional bits ([`lift`]), sheared, and
//! lowered again ([`lower`]); the round trip out and back is exact on the lifted vector, and on the words whenever the
//! child's grid is finer than the parent's by the map's Jacobian (a ship that moves with its centre: always).
//!
//! Positions are not boosted here: a boost also maps an event's time, and the plane's tick is the same physical time
//! in every doll (docs/plane.md, `world.rs`). That is the law's open question, and nothing here answers it.
use crate::num::{Error, Res, V2};
use emergent_space::orbit::Scalar;

/// Fractional bits of the shear coefficients of a [`Frame`].
pub const N: u32 = 100;
/// Fractional bits of a [`Turn`]'s coefficients: an absolute precision of 2^-64 in the angle, an eighth of a quantum on a 61-bit
/// word, whatever the angle (a hand-out's fit can be off by 10^-7).
pub const NT: u32 = 64;
/// Extra fractional bits a velocity is lifted with, below its word's quantum.
pub const EXTRA: i32 = 20;
/// The most fractional bits a lifted vector may carry (`g` is about `2^F`, and the shears' sums must stay in an `i128`).
const MAX_F: i32 = 122;

fn overflow() -> Error {
    Error::Refused("a shear left the integer word")
}

/// The 256-bit product of two unsigned words, as `(high, low)`.
fn mul_wide(a: u128, b: u128) -> (u128, u128) {
    let (a0, a1, b0, b1) = (a as u64 as u128, a >> 64, b as u64 as u128, b >> 64);
    let (p00, p01, p10, p11) = (a0 * b0, a0 * b1, a1 * b0, a1 * b1);
    let mid = (p00 >> 64) + (p01 as u64 as u128) + (p10 as u64 as u128);
    let lo = (p00 as u64 as u128) | ((mid as u64 as u128) << 64);
    let hi = p11 + (p01 >> 64) + (p10 >> 64) + (mid >> 64);
    (hi, lo)
}

/// `⌊p·y / 2^n⌋` for any two `i128`, through a 256-bit product (`n` below 128). The floor is the shear's rounding:
/// exact, and the same on every machine.
pub fn mulshr(p: i128, y: i128, n: u32) -> Res<i128> {
    debug_assert!(n > 0 && n < 128);
    let neg = (p < 0) != (y < 0);
    let (hi, lo) = mul_wide(p.unsigned_abs(), y.unsigned_abs());
    // The magnitude shifted, and whether a bit was shifted out.
    if hi >> n != 0 {
        return Err(overflow());
    }
    let mag = (lo >> n) | (hi << (128 - n));
    let inexact = lo & ((1u128 << n) - 1) != 0;
    let mag = i128::try_from(mag).map_err(|_| overflow())?;
    Ok(if neg { -mag - inexact as i128 } else { mag })
}

/// `x + ⌊p·y / 2^n⌋`.
fn shear(x: i128, y: i128, p: i128, n: u32) -> Res<i128> {
    x.checked_add(mulshr(p, y, n)?).ok_or_else(overflow)
}
/// The inverse of [`shear`] (the same coefficient): `x − ⌊p·y / 2^n⌋`.
fn unshear(x: i128, y: i128, p: i128, n: u32) -> Res<i128> {
    x.checked_sub(mulshr(p, y, n)?).ok_or_else(overflow)
}

/// A rotation by `φ` as three shears with coefficients `(a, b)` over `2^n`: `a = −tan(φ/2)`, `b = sin φ`.
pub fn rotate(v: [i128; 2], a: i128, b: i128, n: u32) -> Res<[i128; 2]> {
    let x = shear(v[0], v[1], a, n)?;
    let y = shear(v[1], x, b, n)?;
    Ok([shear(x, y, a, n)?, y])
}
/// The exact inverse of [`rotate`]: the shears undone in the opposite order.
pub fn unrotate(v: [i128; 2], a: i128, b: i128, n: u32) -> Res<[i128; 2]> {
    let x = unshear(v[0], v[1], a, n)?;
    let y = unshear(v[1], x, b, n)?;
    Ok([unshear(x, y, a, n)?, y])
}

/// A boost on `(g, u)` as three shears with `a = −tanh(η/2)` and `b = −sinh η` over `2^n`: the new `u` is `cosh η·u −
/// sinh η·g`, the new `g` is `cosh η·g − sinh η·u` (a frame moving at `+tanh η` along the axis sees what moves at `v`
/// with `v` less that velocity).
pub fn boost(gu: [i128; 2], a: i128, b: i128, n: u32) -> Res<[i128; 2]> {
    let g1 = shear(gu[0], gu[1], a, n)?;
    let u1 = shear(gu[1], g1, b, n)?;
    Ok([shear(g1, u1, a, n)?, u1])
}
/// The exact inverse of [`boost`].
pub fn unboost(gu: [i128; 2], a: i128, b: i128, n: u32) -> Res<[i128; 2]> {
    let g1 = unshear(gu[0], gu[1], a, n)?;
    let u0 = unshear(gu[1], g1, b, n)?;
    Ok([unshear(g1, u0, a, n)?, u0])
}

/// A small rotation of integer words (the sub-quantum turn of a binding): the angle's shear coefficients over `2^NT`,
/// in an `i64` each (any angle under a radian). It replaces the second-order turn `x − δy − δ²x/2`, which
/// no map inverts; this one is a bijection of the integer plane, within two quanta of the exact rotation.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Default)]
pub struct Turn {
    pub a: i64,
    pub b: i64,
}
impl Turn {
    pub const NONE: Turn = Turn { a: 0, b: 0 };

    /// The rotation by the angle whose tangent is `t`: `a = −tan(φ/2) = −t/(1 + √(1 + t²))`, `b = sin φ = t/√(1 + t²)`.
    pub fn of_tangent(t: Scalar) -> Res<Turn> {
        if t.is_zero() {
            return Ok(Turn::NONE);
        }
        let s = Scalar::ONE.add(t.mul(t)?)?.sqrt()?;
        let a = t.negate().div(Scalar::ONE.add(s)?)?.fixed(NT as i32)?;
        let b = t.div(s)?.fixed(NT as i32)?;
        Ok(Turn { a: i64::try_from(a).map_err(|_| overflow())?, b: i64::try_from(b).map_err(|_| overflow())? })
    }

    pub fn is_none(self) -> bool {
        self.a == 0 && self.b == 0
    }

    /// The vector turned: three shears, each one multiplication and a floor (the coefficients are `i64` and the words
    /// `i64`, so the products fit an `i128`: no wide product here, it is on every readout).
    pub fn apply(self, v: [i64; 2]) -> Res<[i128; 2]> {
        if self.is_none() {
            return Ok([v[0] as i128, v[1] as i128]);
        }
        let (a, b) = (self.a as i128, self.b as i128);
        let x = v[0] as i128 + ((a * v[1] as i128) >> NT);
        let y = v[1] as i128 + ((b * x) >> NT);
        Ok([x + ((a * y) >> NT), y])
    }

    /// The exact inverse of [`Turn::apply`]'s result (an integer vector the shears produced).
    pub fn undo(self, v: [i128; 2]) -> Res<[i128; 2]> {
        let (a, b) = (self.a as i128, self.b as i128);
        let x = v[0] - ((a * v[1]) >> NT);
        let y = v[1] - ((b * x) >> NT);
        Ok([x - ((a * y) >> NT), y])
    }
}

/// A rotation by any angle, as three shears of coefficients over `2^N`: by the angle with cosine `c` and sine `s`
/// (a unit vector, as scalars). A half turn is exact (a negation), so a rotation of more than a quarter turn is the
/// half turn and one of less: `tan(φ/2)` never exceeds one, and the shears' rounding never blows up near `φ = π`
/// (where `a = −tan(φ/2)` runs to infinity).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Rotation {
    flip: bool,
    a: i128,
    b: i128,
}

impl Rotation {
    pub fn by(c: Scalar, s: Scalar) -> Res<Rotation> {
        let flip = c.significand() < 0;
        let (c, s) = if flip { (c.negate(), s.negate()) } else { (c, s) };
        let a = s.negate().div(Scalar::ONE.add(c)?)?.fixed(N as i32)?;
        let b = s.fixed(N as i32)?;
        Ok(Rotation { flip, a, b })
    }

    pub fn apply(&self, v: [i128; 2]) -> Res<[i128; 2]> {
        let v = if self.flip { [v[0].checked_neg().ok_or_else(overflow)?, v[1].checked_neg().ok_or_else(overflow)?] } else { v };
        rotate(v, self.a, self.b, N)
    }

    /// The exact inverse of [`Rotation::apply`].
    pub fn undo(&self, v: [i128; 2]) -> Res<[i128; 2]> {
        let v = unrotate(v, self.a, self.b, N)?;
        Ok(if self.flip { [v[0].checked_neg().ok_or_else(overflow)?, v[1].checked_neg().ok_or_else(overflow)?] } else { v })
    }
}

/// The frame of a centre moving with velocity `w` (`c = 1`): the rotation that brings `w` onto the first axis, the
/// boost along it by `w`'s rapidity, and the rotation back. Every coefficient is a dyadic rational computed by an
/// integer algorithm from the velocity (one square root): no float decides it.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Frame {
    to_axis: Rotation,
    back: Rotation,
    ba: i128,
    bb: i128,
}

impl Frame {
    /// The frame of velocity `w`; `None` for a centre at rest (nothing to do).
    pub fn of(w: V2) -> Res<Option<Frame>> {
        let beta = crate::num::norm2(w)?;
        if beta.is_zero() {
            return Ok(None);
        }
        let one = Scalar::ONE;
        if beta >= one {
            return Err(Error::Refused("a centre at or past the speed of light"));
        }
        let (cx, cy) = (w[0].div(beta)?, w[1].div(beta)?);
        let (to_axis, back) = (Rotation::by(cx, cy.negate())?, Rotation::by(cx, cy)?);
        // tanh(η/2) = β/(1 + √(1 − β²)); sinh η = 2a/(1 − a²) with a the dyadic that was kept.
        let s = one.sub(beta.mul(beta)?)?.sqrt()?;
        let a = beta.negate().div(one.add(s)?)?;
        let ba = a.fixed(N as i32)?;
        let a_kept = Scalar::raw(ba, -(N as i32))?;
        let bb = Scalar::integer(2).mul(a_kept)?.div(one.sub(a_kept.mul(a_kept)?)?)?.fixed(N as i32)?;
        Ok(Some(Frame { to_axis, back, ba, bb }))
    }

    /// A four-velocity `(g, u_x, u_y)` seen from the centre: nine shears.
    pub fn forward(&self, t: [i128; 3]) -> Res<[i128; 3]> {
        let u = self.to_axis.apply([t[1], t[2]])?;
        let gx = boost([t[0], u[0]], self.ba, self.bb, N)?;
        let u = self.back.apply([gx[1], u[1]])?;
        Ok([gx[0], u[0], u[1]])
    }

    /// The exact inverse of [`Frame::forward`]: a four-velocity seen from the centre, back in the parent's frame.
    pub fn inverse(&self, t: [i128; 3]) -> Res<[i128; 3]> {
        let u = self.back.undo([t[1], t[2]])?;
        let gx = unboost([t[0], u[0]], self.ba, self.bb, N)?;
        let u = self.to_axis.undo([gx[1], u[1]])?;
        Ok([gx[0], u[0], u[1]])
    }
}

/// Extended coordinates at a handoff. The event is `(t, x, y)` at `event_exp`; the momentum is
/// `(-p_t, p_x, p_y)` at `momentum_exp`. Neither vector is lowered to velocity words or ticks:
/// doing so discards exactly the bits an inverse handoff needs. Units have c = 1.
/// This is scratch for a chart change, not an additional record per body. The energy component
/// must include rest energy: the current Kepler register in `Ext` is not a four-momentum.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct PhasePoint {
    pub event: [i128; 3],
    pub momentum: [i128; 3],
    pub event_exp: i16,
    pub momentum_exp: i16,
}

/// A local chart change at one surface event. `origin` uses the event vector's quantum in the
/// parent; `unit_shift` is child.shift - parent.shift. Length and time units change together,
/// by relabelling the exponent, never by discarding bits. Specific momentum is dimensionless.
/// The same chart, including the same origin and coefficients, must be used in reverse.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Handoff {
    pub frame: Option<Frame>,
    pub origin: [i128; 3],
    pub unit_shift: i16,
}

impl Handoff {
    pub fn capture(&self, point: PhasePoint) -> Res<PhasePoint> {
        let mut event = [0; 3];
        for c in 0..3 {
            event[c] = point.event[c].checked_sub(self.origin[c]).ok_or_else(overflow)?;
        }
        let (event, momentum) = match self.frame {
            Some(frame) => (frame.forward(event)?, frame.forward(point.momentum)?),
            None => (event, point.momentum),
        };
        Ok(PhasePoint { event, momentum, event_exp: point.event_exp.checked_add(self.unit_shift).ok_or_else(overflow)?, ..point })
    }

    pub fn release(&self, point: PhasePoint) -> Res<PhasePoint> {
        let (mut event, momentum) = match self.frame {
            Some(frame) => (frame.inverse(point.event)?, frame.inverse(point.momentum)?),
            None => (point.event, point.momentum),
        };
        for c in 0..3 {
            event[c] = event[c].checked_add(self.origin[c]).ok_or_else(overflow)?;
        }
        Ok(PhasePoint { event, momentum, event_exp: point.event_exp.checked_sub(self.unit_shift).ok_or_else(overflow)?, ..point })
    }
}

/// `round(num·2^shift / den)` (half away from zero) for `den > 0` and `shift ≥ 0`, by a 256-bit long division: the
/// velocity a four-velocity makes, to the last bit of a word (a scalar's 62 bits would leave none to round with).
fn div_shift_round(num: i128, den: i128, shift: u32) -> Res<i128> {
    debug_assert!(den > 0 && shift < 128);
    let n = num.unsigned_abs();
    let (hi, lo) = if shift == 0 { (0, n) } else { (n >> (128 - shift), n << shift) };
    let (mut q, mut rem) = (0u128, 0u128);
    let d = den as u128;
    for i in (0..256).rev() {
        let bit = if i >= 128 { (hi >> (i - 128)) & 1 } else { (lo >> i) & 1 };
        rem = (rem << 1) | bit;
        q = if q >> 127 != 0 { return Err(overflow()) } else { q << 1 };
        if rem >= d {
            rem -= d;
            q |= 1;
        }
    }
    if rem * 2 >= d {
        q += 1;
    }
    let q = i128::try_from(q).map_err(|_| overflow())?;
    Ok(if num < 0 { -q } else { q })
}

/// The fractional bits a velocity word at exponent `e` is lifted with: its own, and [`EXTRA`] more.
fn lift_bits(e: i32) -> Res<i32> {
    let f = EXTRA - e;
    if !(0..=MAX_F).contains(&f) {
        return Err(Error::Refused("a velocity word the lift cannot carry"));
    }
    Ok(f)
}

/// A velocity (integer words at exponent `e`, `c = 1`) as an integer four-velocity `(g, u_x, u_y) = 2^F·(γ, γv)` in
/// `2^-F` of `c`, `F = EXTRA − e`: `γ − 1 = v²/(√(1 − v²)·(1 + √(1 − v²)))` is computed apart (a scalar of 62 bits, so
/// the lift is exact to far below the word's quantum however small `v` is) and added to `2^F`.
pub fn lift(v: [i64; 2], e: i32) -> Res<[i128; 3]> {
    let f = lift_bits(e)?;
    let vs = [Scalar::raw(v[0] as i128, e)?, Scalar::raw(v[1] as i128, e)?];
    let v2 = vs[0].mul(vs[0])?.add(vs[1].mul(vs[1])?)?;
    if v2 >= Scalar::ONE {
        return Err(Error::Refused("a velocity at or past the speed of light"));
    }
    let s = Scalar::ONE.sub(v2)?.sqrt()?;
    let gm1 = v2.div(s.mul(Scalar::ONE.add(s)?)?)?;
    let g = (1i128 << f).checked_add(gm1.fixed(f)?).ok_or_else(overflow)?;
    let u = |c: usize| -> Res<i128> { ((v[c] as i128) << EXTRA).checked_add(gm1.mul(vs[c])?.fixed(f)?).ok_or_else(overflow) };
    Ok([g, u(0)?, u(1)?])
}

/// The velocity words of an integer four-velocity: `v = u/g` (to the nearest word) at the exponent `e` asked, or, when it
/// does not fit 62 bits there (or none is asked), at the finest exponent where the larger component does. A lifted
/// vector's own `F` (`f`) is the one [`lift`] used, `EXTRA − e` of the words it was lifted from.
pub fn lower(t: [i128; 3], f: i32, want: Option<i32>) -> Res<([i64; 2], i32)> {
    let q = |c: usize| -> Res<Scalar> { Ok(Scalar::raw(t[1 + c], 0)?.div(Scalar::raw(t[0], 0)?)?) };
    let r = [q(0)?, q(1)?];
    // The finest exponent at which the larger component has at most 62 bits (an `i64` has 63).
    let top = r.iter().filter(|x| !x.is_zero()).map(|x| x.exponent() as i32).max();
    let fit = top.map(|t| t - 61);
    // Never finer than the lift could carry: its quantum is `2^-f`, and three bits above it keep its noise an eighth of a word.
    let floor = 3 - f;
    let e = match (want, fit) {
        (Some(w), Some(x)) => w.max(x),
        (Some(w), None) => w,
        (None, Some(x)) => x,
        (None, None) => floor,
    }
    .max(floor);
    // To the nearest word (half away from zero), by an exact long division: a vector that was a word's, plus the lift's
    // noise far below its quantum, comes back as that word.
    let word = |c: usize| -> Res<i64> { i64::try_from(div_shift_round(t[1 + c], t[0], u32::try_from(-e).map_err(|_| overflow())?)?).map_err(|_| overflow()) };
    Ok(([word(0)?, word(1)?], e))
}

/// A ship's velocity `v` (words at an exponent) seen from a centre moving with `w` (words at an exponent): the
/// relativistic composition, by nine integer shears on the lifted four-velocity, at the finest exponent that holds it
/// (or `want`, if it fits). A centre at rest leaves it as it is.
pub fn seen_from(v: ([i64; 2], i32), w: ([i64; 2], i32), want: Option<i32>) -> Res<([i64; 2], i32)> {
    let ws = [Scalar::raw(w.0[0] as i128, w.1)?, Scalar::raw(w.0[1] as i128, w.1)?];
    let Some(frame) = Frame::of(ws)? else { return Ok(v) };
    let t = frame.forward(lift(v.0, v.1)?)?;
    lower(t, lift_bits(v.1)?, want)
}

/// The inverse of [`seen_from`]: a velocity seen from the centre, in the parent's frame (`want` is the exponent the
/// parent's words are asked in: the centre's own, when the body leaves the centre's doll).
pub fn seen_by_parent(v: ([i64; 2], i32), w: ([i64; 2], i32), want: Option<i32>) -> Res<([i64; 2], i32)> {
    let ws = [Scalar::raw(w.0[0] as i128, w.1)?, Scalar::raw(w.0[1] as i128, w.1)?];
    let Some(frame) = Frame::of(ws)? else { return Ok(v) };
    let t = frame.inverse(lift(v.0, v.1)?)?;
    lower(t, lift_bits(v.1)?, want)
}

#[cfg(test)]
mod tests {
    use super::*;

    struct Rng(u64);
    impl Rng {
        fn next(&mut self) -> u64 {
            self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            self.0 >> 11
        }
        fn unit(&mut self) -> f64 {
            self.next() as f64 / (1u64 << 53) as f64
        }
        fn word(&mut self, bits: u32) -> i128 {
            let m = (((self.next() as u128) << 40) ^ self.next() as u128) & ((1u128 << bits) - 1);
            if self.next() & 1 == 0 { m as i128 } else { -(m as i128) }
        }
    }

    fn sc(v: f64) -> Scalar {
        crate::num::from_f64(v)
    }

    #[test]
    fn mulshr_is_a_floor_of_the_exact_product() {
        let mut r = Rng(1);
        for _ in 0..20_000 {
            let (p, y, n) = (r.word(100), r.word(110), 100);
            let got = mulshr(p, y, n).unwrap();
            // The exact floor by a different road: split y.
            let (yh, yl) = (y >> 55, y & ((1i128 << 55) - 1));
            let exact = (mulshr(p, yh, n - 55).unwrap() << 0) + mulshr(p, yl, n).unwrap();
            assert!((got - exact).abs() <= 2, "{p} {y}: {got} vs {exact}");
        }
        assert_eq!(mulshr(-3, 1 << 99, 100).unwrap(), -2, "floor, not truncation: −3/2 is −2");
        assert_eq!(mulshr(3, 1 << 99, 100).unwrap(), 1);
        assert_eq!(mulshr(i128::MAX, i128::MAX, 100).unwrap_err(), Error::Refused("a shear left the integer word"));
    }

    fn exact_boost(v: [f64; 2], w: [f64; 2]) -> [f64; 2] {
        // The velocity of a body at `v` seen from a frame moving at `w`: (1/(1 − v·w))·[v/γ_w − w + (γ_w/(γ_w + 1))(v·w)·w]
        let (ww, vw) = (w[0] * w[0] + w[1] * w[1], v[0] * w[0] + v[1] * w[1]);
        let g = 1.0 / (1.0 - ww).sqrt();
        let k = 1.0 / (1.0 - vw);
        [k * (v[0] / g - w[0] + g / (g + 1.0) * vw * w[0]), k * (v[1] / g - w[1] + g / (g + 1.0) * vw * w[1])]
    }

    fn words(x: [f64; 2], e: i32) -> [i64; 2] {
        [(x[0] * 2f64.powi(-e)).round() as i64, (x[1] * 2f64.powi(-e)).round() as i64]
    }
    fn value(v: [i64; 2], e: i32) -> [f64; 2] {
        [v[0] as f64 * 2f64.powi(e), v[1] as f64 * 2f64.powi(e)]
    }
    /// The centre velocity words at the exponent that gives them 62 bits, for speed `beta` at angle `ang`.
    fn centre(beta: f64, ang: f64) -> ([i64; 2], i32) {
        let e = beta.log2().floor() as i32 - 61;
        (words([beta * ang.cos(), beta * ang.sin()], e), e)
    }

    /// Frozen before the first run (Opus memo, R3): rotations through any angle round-trip bit for bit, and are the rotation
    /// to the precision of their coefficients; the control is the plain shear form, whose coefficient `−tan(φ/2)` does not
    /// even fit a word near a half turn, where the rotation by π first keeps it under one.
    #[test]
    fn rotations_round_trip_exactly_through_every_angle() {
        let mut r = Rng(7);
        let mut angles: Vec<f64> = (0..3000).map(|_| (r.unit() * 2.0 - 1.0) * std::f64::consts::PI).collect();
        for d in [0.0, 1e-3, 1e-6, 1e-9, 1e-12] {
            for base in [0.0, std::f64::consts::PI, -std::f64::consts::PI, std::f64::consts::FRAC_PI_2, -std::f64::consts::FRAC_PI_2] {
                angles.push(base + d);
                angles.push(base - d);
            }
        }
        let mut worst = 0.0f64;
        for phi in angles {
            let rot = Rotation::by(sc(phi.cos()), sc(phi.sin())).unwrap();
            for _ in 0..8 {
                let v = [r.word(90), r.word(90)];
                let out = rot.apply(v).unwrap();
                assert_eq!(rot.undo(out).unwrap(), v, "angle {phi}: out and back");
                let (x, y) = (v[0] as f64, v[1] as f64);
                let want = [x * phi.cos() - y * phi.sin(), x * phi.sin() + y * phi.cos()];
                let scale = x.abs().max(y.abs());
                worst = worst.max(((out[0] as f64 - want[0]).abs().max((out[1] as f64 - want[1]).abs())) / scale);
            }
        }
        println!("worst distance to the exact rotation: {worst:.2e} of the vector's size (the coefficients' 62 bits)");
        assert!(worst < 1e-14);
        // The control: near a half turn the plain form's coefficient is out of the word.
        let phi = std::f64::consts::PI - 1e-9;
        let plain = -(phi / 2.0).tan() * 2f64.powi(N as i32);
        assert!(plain.abs() > 2f64.powi(126), "the plain shear coefficient at π − 1e-9 is {plain:e}");
    }

    /// The boost's nine shears round-trip bit for bit at every speed and direction, on the four-velocities of the words
    /// they are given, and the result is the relativistic composition of velocities (the exact formula, to the lift's
    /// precision); the Galilean `v − w` is the control and misses it by the order of `β²` (and more).
    #[test]
    fn the_boost_is_exactly_invertible_and_is_lorentz() {
        let mut r = Rng(11);
        for beta in [0.01, 0.3, 0.9, 0.99] {
            let (mut galilean_miss, mut lorentz_miss) = (0.0f64, 0.0f64);
            for k in 0..400 {
                let ang = if k < 8 { [0.0, std::f64::consts::PI, -std::f64::consts::PI, 1e-9, std::f64::consts::PI - 1e-9, std::f64::consts::FRAC_PI_2, -std::f64::consts::FRAC_PI_2, 3.0][k] } else { (r.unit() * 2.0 - 1.0) * std::f64::consts::PI };
                let (w, ew) = centre(beta, ang);
                let frame = Frame::of([Scalar::raw(w[0] as i128, ew).unwrap(), Scalar::raw(w[1] as i128, ew).unwrap()]).unwrap().unwrap();
                // A ship: anywhere in the disc of speed up to 0.6 (the centre's own speed, for the slow, is the interesting case).
                let speed = if k % 2 == 0 { beta * 0.5 * r.unit() } else { 0.6 * r.unit() };
                let a2 = (r.unit() * 2.0 - 1.0) * std::f64::consts::PI;
                let ev = ew;
                let v = words([speed * a2.cos(), speed * a2.sin()], ev);
                let t = lift(v, ev).unwrap();
                let out = frame.forward(t).unwrap();
                assert_eq!(frame.inverse(out).unwrap(), t, "beta {beta} k {k}: out and back");
                // And as velocities: the exact composition.
                let (got, eg) = seen_from((v, ev), (w, ew), None).unwrap();
                let (vf, wf) = (value(v, ev), value(w, ew));
                let want = exact_boost(vf, wf);
                let gv = value(got, eg);
                let scale = (vf[0].hypot(vf[1]) + wf[0].hypot(wf[1])).max(1e-300);
                lorentz_miss = lorentz_miss.max(((gv[0] - want[0]).abs().max((gv[1] - want[1]).abs())) / scale);
                galilean_miss = galilean_miss.max(((vf[0] - wf[0] - want[0]).abs().max((vf[1] - wf[1] - want[1]).abs())) / scale);
            }
            println!("beta {beta}: distance to the exact composition {lorentz_miss:.1e} (of |v|+|w|); the Galilean difference {galilean_miss:.1e}");
            assert!(lorentz_miss < 1e-14, "beta {beta}: {lorentz_miss:e}");
            assert!(galilean_miss > 1e3 * lorentz_miss, "the control must fail: {galilean_miss:e}");
        }
    }

    /// A centre is at rest in its own frame (to a quantum of its words), at every speed and direction.
    #[test]
    fn a_centre_is_at_rest_in_its_own_frame() {
        for beta in [0.01, 0.3, 0.9] {
            for ang in [0.0, 1.0, 2.5, -3.0, std::f64::consts::PI] {
                let (w, ew) = centre(beta, ang);
                let (v, ev) = seen_from((w, ew), (w, ew), None).unwrap();
                let mag = value(v, ev)[0].hypot(value(v, ev)[1]);
                assert!(mag <= 8.0 * 2f64.powi(ew), "beta {beta} angle {ang}: the centre moves at {mag:e} in its own frame (word {:e})", 2f64.powi(ew));
            }
        }
    }

    /// Out and back: a ship that moves with its centre (the planets' captures) comes back as the same words, at the
    /// speeds the memo names; and a ship that does not (a heavy loss of resolution: the child's grid is coarser than the
    /// parent's) comes back within a quantum and is then a fixed point: no drift in a thousand round trips.
    #[test]
    fn a_handoff_out_and_back_is_the_identity() {
        let mut r = Rng(5);
        for beta in [0.01, 0.3, 0.9] {
            let (mut exact, mut total) = (0, 0);
            for k in 0..2000 {
                let ang = (r.unit() * 2.0 - 1.0) * std::f64::consts::PI;
                let (w, ew) = centre(beta, ang);
                // A comoving ship: the centre's velocity plus a relative speed under 1e-3·β, in the words' exponent.
                let rel = (0.001 * beta * r.unit()) * 2f64.powi(0);
                let a2 = (r.unit() * 2.0 - 1.0) * std::f64::consts::PI;
                let v = [w[0] + (rel * a2.cos() * 2f64.powi(-ew)).round() as i64, w[1] + (rel * a2.sin() * 2f64.powi(-ew)).round() as i64];
                let (child, ec) = seen_from((v, ew), (w, ew), None).unwrap();
                let (back, eb) = seen_by_parent((child, ec), (w, ew), Some(ew)).unwrap();
                total += 1;
                exact += (eb == ew && back == v) as usize;
                if k < 200 {
                    assert!(ec < ew, "the child's grid is finer than the parent's: {ec} against {ew}");
                }
            }
            println!("beta {beta}: {exact} of {total} comoving ships come back as the same words");
            assert_eq!(exact, total, "beta {beta}");
            // Not comoving: a ship slow in the parent, which the centre's frame sees at about −w. The map contracts there (by
            // 1 − β² at rest), so up to 1/(1 − β²) words of the parent's share a word of the child's: the loss is the map's,
            // not the shears', and it is bounded: five hundred more round trips never leave the first one's neighbourhood.
            let bound = (2.0 / (1.0 - beta * beta)).ceil() as i64;
            let (mut worst, mut drift) = (0i64, 0i64);
            for _ in 0..300 {
                let ang = (r.unit() * 2.0 - 1.0) * std::f64::consts::PI;
                let (w, ew) = centre(beta, ang);
                let a2 = (r.unit() * 2.0 - 1.0) * std::f64::consts::PI;
                let v = words([0.2 * beta * a2.cos() * r.unit(), 0.2 * beta * a2.sin() * r.unit()], ew);
                let mut s = (v, ew);
                for k in 0..500 {
                    let (c, ec) = seen_from(s, (w, ew), None).unwrap();
                    s = seen_by_parent((c, ec), (w, ew), Some(ew)).unwrap();
                    assert_eq!(s.1, ew);
                    let off = (s.0[0] - v[0]).abs().max((s.0[1] - v[1]).abs());
                    if k == 0 {
                        worst = worst.max(off);
                    }
                    drift = drift.max(off);
                }
            }
            println!("beta {beta}: slow ships come back within {worst} words of the parent's on the first round trip, and never more than {drift} in 500 (the contraction's bound: {bound})");
            assert!(worst <= bound && drift <= bound, "beta {beta}: first loss {worst}, worst over 500 trips {drift}, bound {bound}");
        }
    }

    /// The sub-quantum turn of a binding: a bijection of the integer plane, exactly invertible, within two quanta of the
    /// rotation by the angle (tangent `t`), for the angles a 32-bit periapsis angle leaves out.
    #[test]
    fn the_turn_is_exactly_invertible_and_within_two_quanta_of_the_rotation() {
        let mut r = Rng(3);
        let mut worst = 0.0f64;
        for _ in 0..4000 {
            let t = (r.unit() * 2.0 - 1.0) * 2f64.powi(if r.next() & 1 == 0 { -30 } else { -22 });
            let turn = Turn::of_tangent(sc(t)).unwrap();
            let v = [r.word(61) as i64, r.word(61) as i64];
            let out = turn.apply(v).unwrap();
            assert_eq!(turn.undo(out).unwrap(), [v[0] as i128, v[1] as i128]);
            // The exact rotation, by scalars (62 bits: the oracle's own floor is a quantum or two).
            let (one, tt) = (Scalar::ONE, sc(t));
            let c = one.div(one.add(tt.mul(tt).unwrap()).unwrap().sqrt().unwrap()).unwrap();
            let sn = tt.mul(c).unwrap();
            let (x, y) = (Scalar::raw(v[0] as i128, 0).unwrap(), Scalar::raw(v[1] as i128, 0).unwrap());
            let want = [x.mul(c).unwrap().sub(y.mul(sn).unwrap()).unwrap().fixed(0).unwrap(), x.mul(sn).unwrap().add(y.mul(c).unwrap()).unwrap().fixed(0).unwrap()];
            worst = worst.max(((out[0] - want[0]).abs().max((out[1] - want[1]).abs())) as f64);
        }
        println!("worst distance of the turn to the rotation: {worst:.0} quanta");
        assert!(worst <= 4.0, "{worst}");
        assert_eq!(Turn::NONE.apply([5, -7]).unwrap(), [5, -7]);
    }
}
