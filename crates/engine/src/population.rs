//! Exact indexed families. Identities and parameter offsets survive any partition.
use crate::math::{r, Rational, Vec2};
use crate::propagator::Inertial;
use num_bigint::BigInt;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct Family {
    pub name: String,
    pub first_id: u64,
    pub count: u64,
    /// Index of the first retained member in the original affine generator.
    pub offset: u64,
    pub trajectory: Inertial,
    pub stride: Vec2,
    pub radius: Rational,
    pub mass: Rational,
}

impl Family {
    pub fn contains(&self, id: u64) -> bool {
        id >= self.first_id && id - self.first_id < self.count
    }
    pub fn validate(&self) -> Result<(), String> {
        if self.count == 0 {
            return Err("empty family".into());
        }
        self.first_id
            .checked_add(self.count - 1)
            .ok_or("identity overflow")?;
        self.offset
            .checked_add(self.count - 1)
            .ok_or("parameter overflow")?;
        if self.radius < r(0) || self.mass <= r(0) {
            return Err("invalid family mass or radius".into());
        }
        Inertial::new(
            self.trajectory.epoch,
            self.trajectory.origin.clone(),
            self.trajectory.velocity.clone(),
        )?;
        Ok(())
    }
    pub fn member(&self, id: u64) -> Option<Inertial> {
        if !self.contains(id) {
            return None;
        }
        let index = self.offset as i128 + (id - self.first_id) as i128;
        Some(Inertial {
            epoch: self.trajectory.epoch,
            origin: self.trajectory.origin.clone() + self.stride.clone() * r(index),
            velocity: self.trajectory.velocity.clone(),
        })
    }
    pub fn split(&self, left_count: u64) -> Result<(Self, Self), String> {
        if left_count == 0 || left_count >= self.count {
            return Err("split must be interior".into());
        }
        let mut a = self.clone();
        let mut b = self.clone();
        a.count = left_count;
        b.first_id += left_count;
        b.offset += left_count;
        b.count -= left_count;
        Ok((a, b))
    }
    pub fn total_mass(&self) -> Rational {
        self.mass.clone() * r(self.count as i128)
    }
    /// Exact first moment of the affine family, including all unmaterialized members.
    pub fn first_moment(&self, tick: i128) -> Vec2 {
        let n = BigInt::from(self.count);
        let sum_index = &n * BigInt::from(self.offset) + &n * (&n - 1) / 2;
        (self.trajectory.state_at(tick) * Rational::from_integer(n)
            + self.stride.clone() * Rational::from_integer(sum_index))
            * self.mass.clone()
    }
    pub fn self_disjoint(&self) -> bool {
        let d2 = self.stride.x.clone() * self.stride.x.clone()
            + self.stride.y.clone() * self.stride.y.clone();
        self.count <= 1 || d2 > r(4) * self.radius.clone() * self.radius.clone()
    }
}

/// Semantic, stateless random access. Family partition IDs are intentionally absent.
pub fn semantic_random(seed: u64, entity: u64, event: &[u8], purpose: &str, lane: u64) -> u64 {
    let mut h = blake3::Hasher::new();
    h.update(b"emergent-space-random-v1\0");
    h.update(&seed.to_le_bytes());
    h.update(&entity.to_le_bytes());
    h.update(&(event.len() as u64).to_le_bytes());
    h.update(event);
    h.update(&(purpose.len() as u64).to_le_bytes());
    h.update(purpose.as_bytes());
    h.update(&lane.to_le_bytes());
    u64::from_le_bytes(h.finalize().as_bytes()[..8].try_into().unwrap())
}

#[cfg(test)]
mod tests {
    use super::*;
    fn family() -> Family {
        Family {
            name: "route".into(),
            first_id: 500,
            count: 1_000_000_000,
            offset: 0,
            trajectory: Inertial::new(
                0,
                Vec2::zero(),
                Vec2 {
                    x: r(1) / r(4),
                    y: r(0),
                },
            )
            .unwrap(),
            stride: Vec2::new(8, 3),
            radius: r(1),
            mass: r(2),
        }
    }
    #[test]
    fn billion_id_is_random_access_and_split_invariant() {
        let f = family();
        f.validate().unwrap();
        let (a, b) = f.split(123456).unwrap();
        for id in [500, 501, 123955, 123956, 999999999 + 500] {
            let decoded = a.member(id).or_else(|| b.member(id)).unwrap();
            assert_eq!(decoded, f.member(id).unwrap());
            assert_eq!(
                decoded.state_at(315576000000000000),
                f.member(id).unwrap().state_at(315576000000000000)
            );
        }
        assert_eq!(f.total_mass(), a.total_mass() + b.total_mass());
        assert_eq!(f.first_moment(71), a.first_moment(71) + b.first_moment(71));
    }
    #[test]
    fn rng_known_vector_and_purpose_separation() {
        let a = semantic_random(42, 99, b"arrival", "policy", 0);
        assert_eq!(a, semantic_random(42, 99, b"arrival", "policy", 0));
        assert_ne!(a, semantic_random(42, 99, b"arrival", "sensor", 0));
        assert_ne!(a, semantic_random(42, 100, b"arrival", "policy", 0));
    }
}
