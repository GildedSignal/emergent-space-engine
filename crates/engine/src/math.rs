//! Exact scalar arithmetic for the canonical inertial law.

use num_bigint::BigInt;
use num_rational::BigRational;
use serde::{Deserialize, Serialize};
use std::ops::{Add, Mul, Sub};

pub type Rational = BigRational;

pub fn r(value: i128) -> Rational {
    Rational::from_integer(BigInt::from(value))
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Vec2 {
    pub x: Rational,
    pub y: Rational,
}

impl Vec2 {
    pub fn new(x: i128, y: i128) -> Self {
        Self { x: r(x), y: r(y) }
    }

    pub fn zero() -> Self {
        Self::new(0, 0)
    }

    pub fn dot(&self, other: &Self) -> Rational {
        &self.x * &other.x + &self.y * &other.y
    }

    pub fn norm_squared(&self) -> Rational {
        self.dot(self)
    }
}

macro_rules! vector_binary {
    ($trait:ident, $method:ident, $op:tt) => {
        impl $trait for Vec2 {
            type Output = Vec2;
            fn $method(self, other: Vec2) -> Vec2 {
                Vec2 { x: self.x $op other.x, y: self.y $op other.y }
            }
        }
        impl $trait<&Vec2> for Vec2 {
            type Output = Vec2;
            fn $method(self, other: &Vec2) -> Vec2 {
                Vec2 { x: self.x $op &other.x, y: self.y $op &other.y }
            }
        }
        impl $trait<Vec2> for &Vec2 {
            type Output = Vec2;
            fn $method(self, other: Vec2) -> Vec2 {
                Vec2 { x: &self.x $op other.x, y: &self.y $op other.y }
            }
        }
        impl $trait<&Vec2> for &Vec2 {
            type Output = Vec2;
            fn $method(self, other: &Vec2) -> Vec2 {
                Vec2 { x: &self.x $op &other.x, y: &self.y $op &other.y }
            }
        }
    };
}

vector_binary!(Add, add, +);
vector_binary!(Sub, sub, -);

impl Mul<Rational> for Vec2 {
    type Output = Vec2;
    fn mul(self, scale: Rational) -> Vec2 {
        Vec2 {
            x: self.x * &scale,
            y: self.y * scale,
        }
    }
}

impl Mul<Rational> for &Vec2 {
    type Output = Vec2;
    fn mul(self, scale: Rational) -> Vec2 {
        Vec2 {
            x: &self.x * &scale,
            y: &self.y * scale,
        }
    }
}

impl Mul<&Rational> for Vec2 {
    type Output = Vec2;
    fn mul(self, scale: &Rational) -> Vec2 {
        Vec2 {
            x: self.x * scale,
            y: self.y * scale,
        }
    }
}

impl Mul<&Rational> for &Vec2 {
    type Output = Vec2;
    fn mul(self, scale: &Rational) -> Vec2 {
        Vec2 {
            x: &self.x * scale,
            y: &self.y * scale,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn vector_arithmetic_stays_exact_beyond_machine_integer_range() {
        let a = Vec2::new(i128::MAX, i128::MIN);
        let b = Vec2::new(i128::MIN, i128::MAX);
        assert_eq!(&a + &b, Vec2::new(-1, -1));
        assert_eq!((&a - &b) + b, a);
        assert_eq!((&a * (r(1) / r(3))) * r(3), a);
        assert!(a.norm_squared() > r(i128::MAX));
    }

    #[test]
    fn rational_normalization_and_serialization_preserve_identity() {
        assert_eq!(r(2) / r(6), r(1) / r(3));
        let value = Vec2 {
            x: r(1) / r(3),
            y: r(i128::MIN) * r(i128::MAX),
        };
        let encoded = serde_json::to_string(&value).unwrap();
        let decoded: Vec2 = serde_json::from_str(&encoded).unwrap();
        assert_eq!(decoded, value);
    }
}
