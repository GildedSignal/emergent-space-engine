//! Normalized dyadic arithmetic: a virtual binary point, not an absolute-value cap.
//! Products, quotients and boundary conversions truncate toward zero. Addition ignores
//! a nonoverlapping operand more than 64 binary places below the larger one; otherwise
//! it retains cancellation before truncating. Exponent exhaustion is an explicit error.
use crate::{num::isqrt, Error, Result};
use std::cmp::Ordering;

/// `significand * 2^(exponent-62)`. Private fields enforce normalization, including zero.
#[derive(Clone, Copy, Debug, Default, Eq, PartialEq, Hash)]
pub struct Scalar {
    significand: i64,
    exponent: i16,
}
// These named operations return Result so exponent exhaustion cannot be hidden by operators.
#[allow(clippy::should_implement_trait)]
impl Scalar {
    pub const ZERO: Self = Self { significand: 0, exponent: 0 };
    pub const ONE: Self = Self {
        significand: 1 << 62,
        exponent: 0,
    };
    pub fn raw(n: i128, binary_point: i32) -> Result<Self> {
        if n == 0 {
            return Ok(Self::ZERO);
        }
        let bits = 128 - n.unsigned_abs().leading_zeros();
        let shift = bits as i32 - 63;
        let mag = if shift >= 0 {
            n.unsigned_abs() >> shift
        } else {
            n.unsigned_abs() << -shift
        };
        let exponent =
            i16::try_from(binary_point.checked_add(shift).and_then(|x| x.checked_add(62)).ok_or(Error::Range)?).map_err(|_| Error::Range)?;
        Ok(Self {
            significand: if n < 0 { -(mag as i64) } else { mag as i64 },
            exponent,
        })
    }
    pub fn integer(n: i64) -> Self {
        Self::raw(n as i128, 0).expect("i64 exponent fits")
    }
    pub fn power_of_two(exponent: i16) -> Self {
        Self {
            significand: 1 << 62,
            exponent,
        }
    }
    pub const fn significand(self) -> i64 {
        self.significand
    }
    pub const fn exponent(self) -> i16 {
        self.exponent
    }
    pub fn is_zero(self) -> bool {
        self.significand == 0
    }
    pub fn is_positive(self) -> bool {
        self.significand > 0
    }
    pub fn abs(self) -> Self {
        Self {
            significand: self.significand.abs(),
            ..self
        }
    }
    pub fn negate(self) -> Self {
        Self {
            significand: -self.significand,
            ..self
        }
    }
    pub fn scale(self, shift: i32) -> Result<Self> {
        if self.is_zero() {
            return Ok(self);
        }
        Ok(Self {
            exponent: i16::try_from((self.exponent as i32).checked_add(shift).ok_or(Error::Range)?).map_err(|_| Error::Range)?,
            ..self
        })
    }
    pub fn add(self, rhs: Self) -> Result<Self> {
        if self.is_zero() {
            return Ok(rhs);
        }
        if rhs.is_zero() {
            return Ok(self);
        }
        let (hi, lo) = if self.exponent >= rhs.exponent { (self, rhs) } else { (rhs, self) };
        let gap = hi.exponent as i32 - lo.exponent as i32;
        // Preserve all cancellation bits when the operands overlap. A non-overlapping
        // operand is below the retained quantum; it never wraps a machine shift.
        if gap > 64 {
            return Ok(hi);
        }
        Self::raw(((hi.significand as i128) << gap) + lo.significand as i128, lo.exponent as i32 - 62)
    }
    pub fn sub(self, rhs: Self) -> Result<Self> {
        self.add(rhs.negate())
    }
    pub fn mul(self, rhs: Self) -> Result<Self> {
        let product = self.significand as i128 * rhs.significand as i128;
        if product == 0 {
            return Ok(Self::ZERO);
        }
        // Two normalized 63-bit magnitudes produce 125 or 126 bits. The
        // binary point moves by exactly zero or one, never a general shift.
        let carry = i32::from(product.unsigned_abs() >= 1u128 << 125);
        let magnitude = (product.unsigned_abs() >> (62 + carry)) as i64;
        Ok(Self {
            significand: if product < 0 { -magnitude } else { magnitude },
            exponent: i16::try_from(self.exponent as i32 + rhs.exponent as i32 + carry).map_err(|_| Error::Range)?,
        })
    }
    pub fn div(self, rhs: Self) -> Result<Self> {
        if rhs.is_zero() {
            return Err(Error::Range);
        }
        if self.is_zero() {
            return Ok(Self::ZERO);
        }
        // Normalized magnitudes are in [2^62, 2^63), so the exact quotient
        // has 63 or 64 bits. Its correction and normalization both fit words.
        let q = crate::num::div_word(
            (self.significand.unsigned_abs() as u128) << 63,
            rhs.significand.unsigned_abs(),
        );
        let carry = i32::from(q >= 1u64 << 63);
        let magnitude = (q >> carry) as i64;
        Ok(Self {
            significand: if (self.significand < 0) != (rhs.significand < 0) { -magnitude } else { magnitude },
            exponent: i16::try_from(self.exponent as i32 - rhs.exponent as i32 - 1 + carry).map_err(|_| Error::Range)?,
        })
    }
    pub fn sqrt(self) -> Result<Self> {
        if self.significand < 0 {
            return Err(Error::Range);
        }
        if self.is_zero() {
            return Ok(self);
        }
        let odd = self.exponent.rem_euclid(2) as u32;
        Self::raw(
            isqrt((self.significand as u128) << (62 + odd)) as i128,
            self.exponent.div_euclid(2) as i32 - 62,
        )
    }
    pub fn reciprocal(self) -> Result<Self> {
        Self::ONE.div(self)
    }
    /// Checked boundary conversion, truncating toward zero; never a saturating cast.
    pub fn fixed(self, fractional_bits: i32) -> Result<i128> {
        let shift = (self.exponent as i32 - 62).checked_add(fractional_bits).ok_or(Error::Range)?;
        if self.is_zero() {
            return Ok(0);
        }
        if shift >= 0 {
            if shift >= 127 {
                return Err(Error::Range);
            }
            (self.significand as i128).checked_mul(1i128 << shift).ok_or(Error::Range)
        } else if shift <= -127 {
            Ok(0)
        } else {
            Ok(self.significand as i128 / (1i128 << -shift))
        }
    }
    /// Outward boundary conversion for event deadlines: never return an earlier tick.
    pub fn fixed_ceil(self, fractional_bits: i32) -> Result<i128> {
        let trunc = self.fixed(fractional_bits)?;
        if self.is_positive() && self.has_fraction(fractional_bits)? {
            trunc.checked_add(1).ok_or(Error::Range)
        } else {
            Ok(trunc)
        }
    }
    pub fn fixed_floor(self, fractional_bits: i32) -> Result<i128> {
        let trunc = self.fixed(fractional_bits)?;
        if self.significand < 0 && self.has_fraction(fractional_bits)? {
            trunc.checked_sub(1).ok_or(Error::Range)
        } else {
            Ok(trunc)
        }
    }
    fn has_fraction(self, fractional_bits: i32) -> Result<bool> {
        let shift = (self.exponent as i32 - 62).checked_add(fractional_bits).ok_or(Error::Range)?;
        Ok(!self.is_zero() && shift < 0 && (shift <= -63 || self.significand.unsigned_abs() & ((1u64 << -shift) - 1) != 0))
    }
    /// Round toward zero to a chosen number of significant bits. Boundary operation only.
    pub fn quantize(self, bits: u32) -> Result<Self> {
        if !(1..=63).contains(&bits) {
            return Err(Error::Range);
        }
        let shift = 63 - bits;
        Self::raw((self.significand / (1i64 << shift)) as i128, self.exponent as i32 - 62 + shift as i32)
    }
}
impl Ord for Scalar {
    fn cmp(&self, rhs: &Self) -> Ordering {
        let signs = self.significand.signum().cmp(&rhs.significand.signum());
        if signs != Ordering::Equal {
            return signs;
        }
        if self.is_zero() {
            return Ordering::Equal;
        }
        let cmp = (self.exponent, self.significand.abs()).cmp(&(rhs.exponent, rhs.significand.abs()));
        if self.significand < 0 {
            cmp.reverse()
        } else {
            cmp
        }
    }
}
impl PartialOrd for Scalar {
    fn partial_cmp(&self, rhs: &Self) -> Option<Ordering> {
        Some(self.cmp(rhs))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn native_products_and_quotients_keep_signed_normalized_words() {
        let mut n = 3u64;
        for _ in 0..10000 {
            n = n.wrapping_mul(6364136223846793005).wrapping_add(1);
            let a = (n >> 1) | (1 << 62);
            let b = (n.rotate_left(17) >> 1) | (1 << 62);
            for sa in [-1i128, 1] {
                for sb in [-1i128, 1] {
                    let a = Scalar::raw(sa * a as i128, -75).unwrap();
                    let b = Scalar::raw(sb * b as i128, 17).unwrap();
                    let reference = Scalar::raw(((a.significand as i128) << 63) / b.significand as i128,
                        a.exponent as i32 - b.exponent as i32 - 63).unwrap();
                    assert_eq!(a.div(b).unwrap(), reference);
                    let reference = Scalar::raw(a.significand as i128 * b.significand as i128,
                        a.exponent as i32 + b.exponent as i32 - 124).unwrap();
                    assert_eq!(a.mul(b).unwrap(), reference);
                }
            }
        }
        assert_eq!(Scalar::ZERO.div(Scalar::ONE).unwrap(), Scalar::ZERO);
        for ea in [i16::MIN, -32000, -1, 0, 1, 32000, i16::MAX] {
            for eb in [i16::MIN, -32000, -1, 0, 1, 32000, i16::MAX] {
                for n in [0, 1 << 62, (1 << 63) - 1, -((1 << 63) - 1)] {
                    let a = Scalar::raw(n, ea as i32 - 62).unwrap();
                    let b = Scalar::raw((1 << 63) - 1, eb as i32 - 62).unwrap();
                    assert_eq!(a.mul(b), Scalar::raw(a.significand as i128 * b.significand as i128,
                        a.exponent as i32 + b.exponent as i32 - 124));
                    assert_eq!(a.div(b), Scalar::raw(((a.significand as i128) << 63) / b.significand as i128,
                        a.exponent as i32 - b.exponent as i32 - 63));
                }
            }
        }
    }
    #[test]
    fn exponents_change_range_without_changing_relative_information() {
        for e in [-20000, -100, 0, 100, 20000] {
            let a = Scalar::integer(3).scale(e).unwrap();
            let b = Scalar::integer(2).scale(e).unwrap();
            assert_eq!(a.sub(b).unwrap(), Scalar::ONE.scale(e).unwrap());
            assert_eq!(a.div(b).unwrap().fixed(30).unwrap(), 3 << 29);
            let root = a.sqrt().unwrap();
            assert!(root.mul(root).unwrap() <= a);
        }
        assert!(Scalar::power_of_two(i16::MAX).scale(1).is_err());
        assert!(Scalar::ONE.div(Scalar::ZERO).is_err());
        assert_eq!(Scalar::integer(-3).fixed(-1).unwrap(), -1);
        assert_eq!(Scalar::integer(3).sub(Scalar::integer(3)).unwrap(), Scalar::ZERO);
    }
    #[test]
    fn outward_clock_rounding_contains_the_exact_dyadic_for_both_signs() {
        for exponent in [-1000, -64, -63, -30, -1, 0, 1, 30] {
            for integer in [-12345, -3, -1, 0, 1, 3, 12345] {
                let x = Scalar::integer(integer).scale(exponent).unwrap();
                for bits in [-10, 0, 20] {
                    let floor = x.fixed_floor(bits).unwrap();
                    let ceil = x.fixed_ceil(bits).unwrap();
                    assert!(Scalar::raw(floor, -bits).unwrap() <= x);
                    assert!(Scalar::raw(ceil, -bits).unwrap() >= x);
                    assert!(ceil - floor <= 1);
                }
            }
        }
    }
}
