//! Exact indexed families compiled as generators. Identities and parameter offsets survive any partition.
//! Affine families share velocity. Phase/departure families share a route generator and a
//! departure sequence; members need not share velocity at a given tick.
use crate::geometry::{self, Aabb, TickInterval};
use crate::math::{r, Rational, Vec2};
use crate::propagator::Inertial;
use num_bigint::BigInt;
use serde::{Deserialize, Serialize};

fn u64_is_zero(value: &u64) -> bool {
    *value == 0
}

/// Shared hold-then-cruise departure schedule. Member `index` departs at
/// `departure_epoch + index * departure_stride` and then follows `cruise`.
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct PhaseGenerator {
    pub departure_epoch: i128,
    pub departure_stride: i128,
    pub cruise: Vec2,
}

impl PhaseGenerator {
    pub fn new(departure_epoch: i128, departure_stride: i128, cruise: Vec2) -> Result<Self, String> {
        Inertial::new(0, Vec2::zero(), cruise.clone())?;
        Ok(Self {
            departure_epoch,
            departure_stride,
            cruise,
        })
    }
}

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
    /// Generator revision; bumped on in-place parametric burns.
    #[serde(default, skip_serializing_if = "u64_is_zero")]
    pub revision: u64,
    /// When set, members hold on the affine pad then cruise after a staggered departure.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub phase: Option<PhaseGenerator>,
}

impl Family {
    #[allow(clippy::too_many_arguments)]
    pub fn affine(
        name: impl Into<String>,
        first_id: u64,
        count: u64,
        offset: u64,
        trajectory: Inertial,
        stride: Vec2,
        radius: Rational,
        mass: Rational,
    ) -> Self {
        Self {
            name: name.into(),
            first_id,
            count,
            offset,
            trajectory,
            stride,
            radius,
            mass,
            revision: 0,
            phase: None,
        }
    }

    pub fn with_phase(mut self, phase: PhaseGenerator) -> Self {
        self.phase = Some(phase);
        self
    }

    pub fn contains(&self, id: u64) -> bool {
        id >= self.first_id && id - self.first_id < self.count
    }

    pub fn last_id(&self) -> u64 {
        self.first_id + (self.count - 1)
    }

    /// Isolate `[lo, hi]` as one partition; leftovers keep the original generator.
    /// Does not merge merely adjacent identities.
    pub fn split_off_range(&self, lo: u64, hi: u64) -> Result<(Vec<Self>, Self), String> {
        let last = self.last_id();
        let a = lo.max(self.first_id);
        let b = hi.min(last);
        if a > b || !self.contains(a) || !self.contains(b) {
            return Err("range does not intersect family".into());
        }
        let mut remainders = Vec::new();
        let mut mid = self.clone();
        if a > self.first_id {
            let (left, rest) = mid.split(a - self.first_id)?;
            remainders.push(left);
            mid = rest;
        }
        if b < mid.last_id() {
            let (kept, right) = mid.split(b - mid.first_id + 1)?;
            remainders.push(right);
            mid = kept;
        }
        Ok((remainders, mid))
    }

    pub fn shares_member_velocity(&self) -> bool {
        self.phase.is_none()
    }

    pub fn compatible_generator(&self, other: &Self) -> bool {
        self.name == other.name
            && self.trajectory == other.trajectory
            && self.stride == other.stride
            && self.radius == other.radius
            && self.mass == other.mass
            && self.revision == other.revision
            && self.phase == other.phase
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
        if let Some(phase) = &self.phase {
            Inertial::new(0, Vec2::zero(), phase.cruise.clone())?;
            for id in [self.first_id, self.first_id + (self.count - 1)] {
                self.departure_tick(id).ok_or("departure overflow")?;
                self.member_segments(id)
                    .ok_or("phase member decode failed")?;
            }
        }
        Ok(())
    }

    pub fn parameter_index(&self, id: u64) -> Option<i128> {
        if !self.contains(id) {
            return None;
        }
        Some(self.offset as i128 + (id - self.first_id) as i128)
    }

    /// Pad / hold inertial. Affine families have only this piece.
    pub fn member(&self, id: u64) -> Option<Inertial> {
        let index = self.parameter_index(id)?;
        Some(Inertial {
            epoch: self.trajectory.epoch,
            origin: self.trajectory.origin.clone() + self.stride.clone() * r(index),
            velocity: self.trajectory.velocity.clone(),
        })
    }

    pub fn departure_tick(&self, id: u64) -> Option<i128> {
        let phase = self.phase.as_ref()?;
        let index = self.parameter_index(id)?;
        let delta = index.checked_mul(phase.departure_stride)?;
        phase.departure_epoch.checked_add(delta)
    }

    /// Full generator worldline: hold, then optional cruise.
    pub fn member_segments(&self, id: u64) -> Option<Vec<Inertial>> {
        let hold = self.member(id)?;
        let Some(phase) = &self.phase else {
            return Some(vec![hold]);
        };
        let departure = self.departure_tick(id)?;
        if departure <= hold.epoch {
            let cruise = Inertial::new(hold.epoch, hold.origin, phase.cruise.clone()).ok()?;
            return Some(vec![cruise]);
        }
        let cruise = Inertial::new(departure, hold.state_at(departure), phase.cruise.clone()).ok()?;
        Some(vec![hold, cruise])
    }

    pub fn member_state(&self, id: u64, tick: i128) -> Option<Vec2> {
        let segments = self.member_segments(id)?;
        Some(
            segments
                .iter()
                .rev()
                .find(|s| s.epoch <= tick)
                .unwrap_or(&segments[0])
                .state_at(tick),
        )
    }

    pub fn member_velocity(&self, id: u64, tick: i128) -> Option<Vec2> {
        let segments = self.member_segments(id)?;
        Some(
            segments
                .iter()
                .rev()
                .find(|s| s.epoch <= tick)
                .unwrap_or(&segments[0])
                .velocity
                .clone(),
        )
    }

    /// Sample points for a sound range enclosure, tagged with the evaluation tick.
    pub fn range_samples(
        &self,
        lo: u64,
        hi: u64,
        t0: i128,
        t1: i128,
    ) -> Option<Vec<(i128, Vec2)>> {
        if lo > hi || !self.contains(lo) || !self.contains(hi) {
            return None;
        }
        let mut points = Vec::new();
        for id in [lo, hi] {
            for t in [t0, t1] {
                points.push((t, self.member_state(id, t)?));
                if self.phase.is_some() {
                    points.push((t, self.member(id)?.state_at(t)));
                    if let Some(cruise) = self.cruise_inertial(id) {
                        points.push((t, cruise.state_at(t)));
                    }
                }
            }
        }
        Some(points)
    }

    /// Sound AABB of identities `[lo, hi]` over `[start, end]`, including both
    /// hold and cruise images when the family is phased.
    pub fn range_enclosure(&self, lo: u64, hi: u64, interval: TickInterval) -> Option<Aabb> {
        let points = self.range_samples(lo, hi, interval.start, interval.end)?;
        let first = &points[0].1;
        let mut aabb = Aabb::from_points(first, first);
        for (_, p) in &points {
            aabb.min.x = aabb.min.x.clone().min(p.x.clone());
            aabb.min.y = aabb.min.y.clone().min(p.y.clone());
            aabb.max.x = aabb.max.x.clone().max(p.x.clone());
            aabb.max.y = aabb.max.y.clone().max(p.y.clone());
        }
        aabb.min.x -= &self.radius;
        aabb.min.y -= &self.radius;
        aabb.max.x += &self.radius;
        aabb.max.y += &self.radius;
        Some(aabb)
    }

    fn cruise_inertial(&self, id: u64) -> Option<Inertial> {
        let phase = self.phase.as_ref()?;
        let hold = self.member(id)?;
        let departure = self.departure_tick(id)?;
        let epoch = departure.max(hold.epoch);
        Inertial::new(epoch, hold.state_at(epoch), phase.cruise.clone()).ok()
    }

    /// Earliest contact between two decoded members in `domain`.
    pub fn earliest_member_contact(
        &self,
        a: u64,
        b: u64,
        domain: TickInterval,
    ) -> Option<i128> {
        let sa = self.member_segments(a)?;
        let sb = self.member_segments(b)?;
        geometry::first_contact_piecewise(&sa, &sb, &(r(2) * &self.radius), domain)
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

    fn departed(&self, j: u64, tick: i128) -> bool {
        self.departure_tick(self.first_id + j)
            .is_some_and(|d| tick >= d)
    }

    fn run_end(&self, start: u64, tick: i128) -> u64 {
        if start >= self.count {
            return self.count;
        }
        let flag = self.departed(start, tick);
        let mut lo = start + 1;
        let mut hi = self.count;
        while lo < hi {
            let mid = lo + (hi - lo) / 2;
            if self.departed(mid, tick) == flag {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        lo
    }

    fn sum_positions(&self, j0: u64, j1: u64, tick: i128, departed: bool) -> Vec2 {
        if j0 >= j1 {
            return Vec2::zero();
        }
        let n = BigInt::from(j1 - j0);
        let idx0 = BigInt::from(self.offset) + BigInt::from(j0);
        let idx1 = BigInt::from(self.offset) + BigInt::from(j1 - 1);
        let sum_index: BigInt = &n * (&idx0 + &idx1) / 2;
        let pad_sum = self.trajectory.origin.clone() * Rational::from_integer(n.clone())
            + self.stride.clone() * Rational::from_integer(sum_index.clone());
        if !departed {
            let hold = self.trajectory.velocity.clone() * (r(tick) - r(self.trajectory.epoch));
            return (pad_sum + hold * Rational::from_integer(n)) * self.mass.clone();
        }
        let Some(phase) = &self.phase else {
            let hold = self.trajectory.velocity.clone() * (r(tick) - r(self.trajectory.epoch));
            return (pad_sum + hold * Rational::from_integer(n)) * self.mass.clone();
        };
        let hold_v = &self.trajectory.velocity;
        let epoch = self.trajectory.epoch;
        // cruise_pos(j) = pad(j) + hold_v*(D(j)-epoch) + cruise*(tick-D(j))
        let d0 = phase.departure_epoch;
        let ds = phase.departure_stride;
        let sum_d = r(d0) * Rational::from_integer(n.clone())
            + r(ds) * Rational::from_integer(sum_index);
        let hold_part = hold_v.clone() * (sum_d.clone() - r(epoch) * Rational::from_integer(n.clone()));
        let cruise_part = phase.cruise.clone()
            * (r(tick) * Rational::from_integer(n) - sum_d);
        (pad_sum + hold_part + cruise_part) * self.mass.clone()
    }

    /// Exact first moment, including unmaterialized members. Phase families split
    /// into holding and cruising arithmetic runs.
    pub fn first_moment(&self, tick: i128) -> Vec2 {
        if self.phase.is_none() {
            let n = BigInt::from(self.count);
            let sum_index = &n * BigInt::from(self.offset) + &n * (&n - 1) / 2;
            return (self.trajectory.state_at(tick) * Rational::from_integer(n)
                + self.stride.clone() * Rational::from_integer(sum_index))
                * self.mass.clone();
        }
        let mut sum = Vec2::zero();
        let mut j = 0u64;
        while j < self.count {
            let flag = self.departed(j, tick);
            let end = self.run_end(j, tick);
            sum = sum + self.sum_positions(j, end, tick, flag);
            j = end;
        }
        sum
    }

    /// Affine pads must be disjoint. Phase families additionally prove adjacent
    /// members never contact; otherwise the family must be materialized so
    /// interior interactions are not skipped.
    pub fn self_disjoint(&self) -> bool {
        let d2 = self.stride.x.clone() * self.stride.x.clone()
            + self.stride.y.clone() * self.stride.y.clone();
        if self.count <= 1 {
            return true;
        }
        if d2 <= r(4) * self.radius.clone() * self.radius.clone() {
            return false;
        }
        if self.phase.is_none() {
            return true;
        }
        let a = self.first_id;
        let b = self.first_id + 1;
        let Some(sa) = self.member_segments(a) else {
            return false;
        };
        let Some(sb) = self.member_segments(b) else {
            return false;
        };
        let da = self.departure_tick(a).unwrap_or(self.trajectory.epoch);
        let db = self.departure_tick(b).unwrap_or(self.trajectory.epoch);
        let end = da.max(db).saturating_add(1).max(1);
        let domain = TickInterval { start: 1, end };
        if geometry::first_contact_piecewise(&sa, &sb, &(r(2) * &self.radius), domain).is_some() {
            return false;
        }
        let Some(pa) = self.member_state(a, end) else {
            return false;
        };
        let Some(pb) = self.member_state(b, end) else {
            return false;
        };
        let delta = pb - pa;
        delta.norm_squared() > r(4) * self.radius.clone() * self.radius.clone()
    }

    /// Rebase every current member position onto a shared inertial velocity.
    pub fn rebase_as_affine(&self, at: i128, velocity: Vec2) -> Result<Self, String> {
        let origin = self
            .member_state(self.first_id, at)
            .ok_or("member decode failed")?;
        let stride = if self.count > 1 {
            self.member_state(self.first_id + 1, at)
                .ok_or("member decode failed")?
                - origin.clone()
        } else {
            self.stride.clone()
        };
        let mut next = self.clone();
        next.trajectory = Inertial::new(at, origin, velocity)?;
        next.stride = stride;
        next.phase = None;
        next.revision = self.revision.saturating_add(1);
        next.validate()?;
        if !next.self_disjoint() {
            return Err("parametric burn would overlap family members".into());
        }
        Ok(next)
    }

    /// Split holding vs already-departed runs at `at` (at most one cut when
    /// departure is monotone in identity).
    pub fn phase_aligned_parts(&self, at: i128) -> Result<Vec<Self>, String> {
        if self.phase.is_none() || self.count <= 1 {
            return Ok(vec![self.clone()]);
        }
        let first = self.departed(0, at);
        let mut cut = None;
        let mut lo = 1u64;
        let mut hi = self.count;
        while lo < hi {
            let mid = lo + (hi - lo) / 2;
            if self.departed(mid, at) == first {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        if lo < self.count {
            cut = Some(lo);
        }
        match cut {
            Some(left) => {
                let (a, b) = self.split(left)?;
                Ok(vec![a, b])
            }
            None => Ok(vec![self.clone()]),
        }
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
        Family::affine(
            "route",
            500,
            1_000_000_000,
            0,
            Inertial::new(
                0,
                Vec2::zero(),
                Vec2 {
                    x: r(1) / r(4),
                    y: r(0),
                },
            )
            .unwrap(),
            Vec2::new(8, 3),
            r(1),
            r(2),
        )
    }
    fn phase_family() -> Family {
        Family::affine(
            "phase",
            100,
            16,
            0,
            Inertial::new(0, Vec2::zero(), Vec2::zero()).unwrap(),
            Vec2::new(8, 0),
            r(1),
            r(1),
        )
        .with_phase(
            PhaseGenerator::new(
                4,
                3,
                Vec2 {
                    x: r(-1) / r(4),
                    y: r(0),
                },
            )
            .unwrap(),
        )
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
    fn phase_decode_split_and_moment_match_materialized() {
        let f = phase_family();
        f.validate().unwrap();
        assert!(f.self_disjoint());
        assert!(!f.shares_member_velocity());
        let (a, b) = f.split(5).unwrap();
        for id in [100, 104, 105, 107, 115] {
            let segs = a
                .member_segments(id)
                .or_else(|| b.member_segments(id))
                .unwrap();
            assert_eq!(segs, f.member_segments(id).unwrap());
            for t in [0, 4, 20, 49, 80] {
                assert_eq!(
                    a.member_state(id, t)
                        .or_else(|| b.member_state(id, t))
                        .unwrap(),
                    f.member_state(id, t).unwrap()
                );
            }
        }
        let sum = (100..116).fold(Vec2::zero(), |sum, id| {
            sum + f.member_state(id, 20).unwrap() * r(1)
        });
        assert_eq!(sum, f.first_moment(20));
        assert_eq!(f.first_moment(20), a.first_moment(20) + b.first_moment(20));
        let first = f.member_velocity(100, 10).unwrap();
        let last = f.member_velocity(115, 10).unwrap();
        assert_ne!(first, last);
        let (left, mid) = f.split_off_range(104, 110).unwrap();
        assert_eq!(mid.first_id, 104);
        assert_eq!(mid.count, 7);
        assert_eq!(left.len(), 2);
        assert_eq!(left[0].count + mid.count + left[1].count, 16);
    }
    #[test]
    fn closing_phase_family_is_not_self_disjoint() {
        let f = Family::affine(
            "closing",
            1,
            4,
            0,
            Inertial::new(0, Vec2::zero(), Vec2::zero()).unwrap(),
            Vec2::new(8, 0),
            r(1),
            r(1),
        )
        .with_phase(
            PhaseGenerator::new(
                0,
                20,
                Vec2 {
                    x: r(1) / r(2),
                    y: r(0),
                },
            )
            .unwrap(),
        );
        assert!(!f.self_disjoint());
    }
    #[test]
    fn rng_known_vector_and_purpose_separation() {
        let a = semantic_random(42, 99, b"arrival", "policy", 0);
        assert_eq!(a, semantic_random(42, 99, b"arrival", "policy", 0));
        assert_ne!(a, semantic_random(42, 99, b"arrival", "sensor", 0));
        assert_ne!(a, semantic_random(42, 100, b"arrival", "policy", 0));
    }
}
