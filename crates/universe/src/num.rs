//! Exact arithmetic helpers over `crates/space`'s normalized dyadic [`Scalar`]: two-vectors,
//! tick conversions and the error type. Everything that decides an outcome in this crate is
//! built from these (integers); floats appear only in the view and in the tests' oracles.
use emergent_space::orbit::Scalar;

/// Root-clock tick: one tick is `2^TICK_EXP` of the star's `M/c` (the root doll's time unit).
pub type Tick = i64;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Error {
    /// A refusal of `crates/space` (range, no bound orbit, topology).
    Space(emergent_space::Error),
    /// The universe's own refusal, with its reason.
    Refused(&'static str),
}
impl From<emergent_space::Error> for Error {
    fn from(e: emergent_space::Error) -> Self {
        Error::Space(e)
    }
}
pub type Res<T> = Result<T, Error>;

pub type V2 = [Scalar; 2];

pub fn s(n: i64) -> Scalar {
    Scalar::integer(n)
}

/// `ticks · 2^exp`: a time in a doll's units.
pub fn time_of(ticks: Tick, exp: i16) -> Res<Scalar> {
    Ok(Scalar::raw(ticks as i128, exp as i32)?)
}

pub fn add2(a: V2, b: V2) -> Res<V2> {
    Ok([a[0].add(b[0])?, a[1].add(b[1])?])
}
pub fn sub2(a: V2, b: V2) -> Res<V2> {
    Ok([a[0].sub(b[0])?, a[1].sub(b[1])?])
}
pub fn scale2(a: V2, k: Scalar) -> Res<V2> {
    Ok([a[0].mul(k)?, a[1].mul(k)?])
}
pub fn dot2(a: V2, b: V2) -> Res<Scalar> {
    Ok(a[0].mul(b[0])?.add(a[1].mul(b[1])?)?)
}
pub fn cross2(a: V2, b: V2) -> Res<Scalar> {
    Ok(a[0].mul(b[1])?.sub(a[1].mul(b[0])?)?)
}
/// |a|, scaled by the larger component first so the square cannot lose range.
pub fn norm2(a: V2) -> Res<Scalar> {
    let hi = a[0].abs().max(a[1].abs());
    if hi.is_zero() {
        return Ok(hi);
    }
    let r = a[0].abs().min(a[1].abs()).div(hi)?;
    Ok(hi.mul(Scalar::ONE.add(r.mul(r)?)?.sqrt()?)?)
}

/// floor(log2 |x|) for x ≠ 0 (a `Scalar` is `significand · 2^(exponent − 62)` with the
/// significand in `[2^62, 2^63)`, so its exponent is the floor).
pub fn log2_floor(x: Scalar) -> i32 {
    x.exponent() as i32
}

/// A float view of a scalar, for observation and tests only (never for an outcome).
pub fn to_f64(x: Scalar) -> f64 {
    x.significand() as f64 * 2f64.powi(x.exponent() as i32 - 62)
}

/// A scalar from a float, all 53 bits of it: for scenes made from floats (a state a float oracle gives). The
/// scalar is then the exact value; no outcome is decided by the float.
pub fn from_f64(v: f64) -> Scalar {
    if v == 0.0 || !v.is_finite() {
        return Scalar::ZERO;
    }
    let e = v.abs().log2().floor() as i32;
    Scalar::raw((v * 2f64.powi(52 - e)) as i128, e - 52).expect("a finite float is in range")
}
