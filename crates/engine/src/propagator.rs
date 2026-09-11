//! Exact inertial worldlines; no gravity or force approximation is implied.

use crate::geometry::{Aabb, TickInterval};
use crate::math::{r, Rational, Vec2};
use num_bigint::BigInt;
use serde::{Deserialize, Serialize};

pub const PROPER_TIME_FRACTION_BITS: usize = 32;

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Inertial {
    pub epoch: i128,
    pub origin: Vec2,
    pub velocity: Vec2,
}

impl Inertial {
    pub fn new(epoch: i128, origin: Vec2, velocity: Vec2) -> Result<Self, String> {
        if velocity.norm_squared() >= r(1) {
            return Err("inertial velocity must satisfy |v| < c = 1".into());
        }
        Ok(Self {
            epoch,
            origin,
            velocity,
        })
    }

    /// Validates public fields after deserialization or direct mutation.
    pub fn is_subluminal(&self) -> bool {
        self.velocity.norm_squared() < r(1)
    }

    /// Exact affine evaluation, including across the complete signed tick range.
    pub fn state_at(&self, tick: i128) -> Vec2 {
        &self.origin + &self.velocity * (r(tick) - r(self.epoch))
    }

    pub fn rebase(&self, tick: i128) -> Self {
        Self {
            epoch: tick,
            origin: self.state_at(tick),
            velocity: self.velocity.clone(),
        }
    }

    /// The law's velocity-dependent rate is floor(2^32 sqrt(1-|v|^2))/2^32.
    /// It is rounded once as a segment property, not after multiplying a duration.
    /// Recomputing this pure scalar on a query gives the same canonical rate.
    pub fn proper_time_rate(&self) -> Result<Rational, String> {
        let radicand = r(1) - self.velocity.norm_squared();
        if radicand <= r(0) {
            return Err("proper time requires |v| < c = 1".into());
        }
        let scaled = (radicand.numer() << (2 * PROPER_TIME_FRACTION_BITS)) / radicand.denom();
        // floor(sqrt(floor(x))) == floor(sqrt(x)) for nonnegative x.
        let root = scaled
            .to_biguint()
            .expect("validated positive radicand")
            .sqrt();
        Ok(Rational::new(
            BigInt::from(root),
            BigInt::from(1) << PROPER_TIME_FRACTION_BITS,
        ))
    }

    pub fn proper_time_ticks(&self, from: i128, to: i128) -> Result<Rational, String> {
        if from > to {
            return Err("proper-time interval must satisfy from <= to".into());
        }
        Ok((r(to) - r(from)) * self.proper_time_rate()?)
    }

    /// Exact spatial envelope of this affine worldline at every time in [start,end].
    pub fn worldtube(&self, interval: TickInterval) -> Aabb {
        assert!(interval.start <= interval.end, "invalid worldtube interval");
        Aabb::from_points(&self.state_at(interval.start), &self.state_at(interval.end))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn moving() -> Inertial {
        Inertial::new(
            7,
            Vec2::new(5, -9),
            Vec2 {
                x: r(1) / r(3),
                y: r(-1) / r(4),
            },
        )
        .unwrap()
    }

    #[test]
    fn rejects_lightlike_and_superluminal_worldlines() {
        assert!(Inertial::new(0, Vec2::zero(), Vec2::new(1, 0)).is_err());
        assert!(Inertial::new(0, Vec2::zero(), Vec2::new(1, 1)).is_err());
        assert!(Inertial::new(0, Vec2::zero(), Vec2::zero()).is_ok());
    }

    #[test]
    fn rebasing_preserves_the_entire_worldline() {
        let line = moving();
        for epoch in [i128::MIN, -100, 0, 7, 1_000_000_000, i128::MAX] {
            let rebased = line.rebase(epoch);
            for tick in [i128::MIN, -1, 0, 7, 19, i128::MAX] {
                assert_eq!(line.state_at(tick), rebased.state_at(tick));
            }
        }
    }

    #[test]
    fn proper_time_is_subdivision_and_rebase_invariant() {
        let line = moving();
        let full = line.proper_time_ticks(i128::MIN, i128::MAX).unwrap();
        for middle in [i128::MIN, -1, 0, 41, i128::MAX] {
            let left = line.proper_time_ticks(i128::MIN, middle).unwrap();
            let right = line
                .rebase(middle)
                .proper_time_ticks(middle, i128::MAX)
                .unwrap();
            assert_eq!(full, left + right);
        }
        assert_eq!(line.proper_time_ticks(9, 9).unwrap(), r(0));
        assert!(line.proper_time_ticks(9, 8).is_err());
    }

    #[test]
    fn proper_rate_is_an_exact_dyadic_lower_bound() {
        let quantum = r(1) / Rational::from_integer(BigInt::from(1) << PROPER_TIME_FRACTION_BITS);
        for vx in -9..=9 {
            for vy in -9..=9 {
                let velocity = Vec2 {
                    x: r(vx) / r(10),
                    y: r(vy) / r(10),
                };
                let Ok(line) = Inertial::new(0, Vec2::zero(), velocity) else {
                    continue;
                };
                let rate = line.proper_time_rate().unwrap();
                let radicand = r(1) - line.velocity.norm_squared();
                assert!(&rate * &rate <= radicand);
                let next = rate + &quantum;
                assert!(&next * &next > radicand);
            }
        }
        let stationary = Inertial::new(0, Vec2::zero(), Vec2::zero()).unwrap();
        assert_eq!(stationary.proper_time_rate().unwrap(), r(1));
    }

    #[test]
    fn nearly_lightlike_quantization_is_explicit_not_a_float_accident() {
        let denominator = BigInt::from(1) << 100;
        let velocity = Vec2 {
            x: Rational::new(&denominator - 1, denominator),
            y: r(0),
        };
        let line = Inertial::new(0, Vec2::zero(), velocity).unwrap();
        assert_eq!(line.proper_time_rate().unwrap(), r(0));
        assert!(line.is_subluminal());
    }

    #[test]
    fn worldtube_bounds_negative_motion_and_fractional_samples() {
        let line = moving();
        let tube = line.worldtube(TickInterval::new(-10, 30).unwrap());
        for tick in -10..=30 {
            assert!(tube.contains(&line.state_at(tick)));
        }
        assert_eq!(tube.min.x, line.state_at(-10).x);
        assert_eq!(tube.min.y, line.state_at(30).y);
    }

    #[test]
    fn serialization_contains_only_canonical_worldline_state() {
        let line = moving();
        let encoded = serde_json::to_string(&line).unwrap();
        let decoded: Inertial = serde_json::from_str(&encoded).unwrap();
        assert_eq!(decoded, line);
        assert_eq!(decoded.proper_time_rate(), line.proper_time_rate());
        assert_eq!(
            serde_json::to_value(line)
                .unwrap()
                .as_object()
                .unwrap()
                .len(),
            3
        );
    }
}
