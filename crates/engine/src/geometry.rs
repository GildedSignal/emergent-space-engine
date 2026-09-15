//! Exact broad-phase bounds and canonical tick-binned contact/light predicates.

use crate::math::{r, Rational, Vec2};
use crate::propagator::Inertial;
use serde::{Deserialize, Serialize};

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct TickInterval {
    pub start: i128,
    pub end: i128,
}

impl TickInterval {
    pub fn new(start: i128, end: i128) -> Result<Self, String> {
        if start > end {
            return Err("tick interval must satisfy start <= end".into());
        }
        Ok(Self { start, end })
    }

    pub fn contains(&self, tick: i128) -> bool {
        self.start <= tick && tick <= self.end
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Aabb {
    pub min: Vec2,
    pub max: Vec2,
}

impl Aabb {
    pub fn from_points(a: &Vec2, b: &Vec2) -> Self {
        Self {
            min: Vec2 {
                x: a.x.clone().min(b.x.clone()),
                y: a.y.clone().min(b.y.clone()),
            },
            max: Vec2 {
                x: a.x.clone().max(b.x.clone()),
                y: a.y.clone().max(b.y.clone()),
            },
        }
    }

    pub fn contains(&self, point: &Vec2) -> bool {
        self.min.x <= point.x
            && point.x <= self.max.x
            && self.min.y <= point.y
            && point.y <= self.max.y
    }

    pub fn intersects(&self, other: &Self) -> bool {
        self.min.x <= other.max.x
            && other.min.x <= self.max.x
            && self.min.y <= other.max.y
            && other.min.y <= self.max.y
    }
}

/// Future causal reachability in the flat c=1 law; all products use BigInt-backed rationals.
pub fn causal_reachable(
    emission_tick: i128,
    emission: &Vec2,
    reception_tick: i128,
    reception: &Vec2,
) -> bool {
    if reception_tick < emission_tick {
        return false;
    }
    let duration = r(reception_tick) - r(emission_tick);
    (reception - emission).norm_squared() <= &duration * &duration
}

/// Earliest integer tick inside the emission's future light cone.
/// Inertial subluminal motion makes cone membership monotone after emission.
pub fn first_signal_arrival(
    emission_tick: i128,
    emission: &Vec2,
    receiver: &Inertial,
    domain: TickInterval,
) -> Option<i128> {
    let start = domain.start.max(emission_tick);
    if start > domain.end || !receiver.is_subluminal() {
        return None;
    }
    first_true(start, domain.end, |tick| {
        causal_reachable(emission_tick, emission, tick, &receiver.state_at(tick))
    })
}

/// First tick k in domain whose half-open bin (k-1,k] contains continuous contact.
/// Contact means distance <= radius, and radius is the combined contact radius.
/// Tangencies and contacts entirely between samples are included. A tangent exactly
/// at k belongs to bin k only. Existing extended overlap can occupy several bins.
/// This bin ownership is invariant under splitting a search into adjacent tick ranges.
pub fn first_contact(
    a: &Inertial,
    b: &Inertial,
    radius: &Rational,
    domain: TickInterval,
) -> Option<i128> {
    if domain.start > domain.end
        || radius < &r(0)
        || a.velocity.norm_squared() > r(1)
        || b.velocity.norm_squared() > r(1)
    {
        return None;
    }
    let velocity = &a.velocity - &b.velocity;
    // Work relative to the left edge of the first bin. Rational subtraction avoids
    // underflow when domain.start == i128::MIN; worldlines extend analytically there.
    let relative_at_left = (a.state_at(domain.start) - b.state_at(domain.start)) - &velocity;
    let quadratic = velocity.norm_squared();
    let linear = r(2) * relative_at_left.dot(&velocity);
    let constant = relative_at_left.norm_squared() - radius * radius;

    first_true(domain.start, domain.end, |tick| {
        let duration = r(tick) - r(domain.start) + r(1);
        prefix_has_contact(&quadratic, &linear, &constant, &duration)
    })
}

/// Contact ticks owned by `segments[index]`: the first segment covers the full
/// incoming domain; a later segment starts at epoch+1 so the switch tick stays
/// on the previous piece (matching `Body::at` continuity at the join).
pub fn segment_query_domain(
    segments: &[Inertial],
    index: usize,
    domain: TickInterval,
) -> Option<TickInterval> {
    if index >= segments.len() || domain.start > domain.end {
        return None;
    }
    let start = if index == 0 {
        domain.start
    } else {
        domain.start.max(segments[index].epoch.saturating_add(1))
    };
    let end = match segments.get(index + 1) {
        Some(next) => domain.end.min(next.epoch),
        None => domain.end,
    };
    if start <= end {
        Some(TickInterval { start, end })
    } else {
        None
    }
}

/// Earliest contact between piecewise inertial generators. Each piece is clipped
/// to the ticks it owns; the result is the minimum certified tick.
pub fn first_contact_piecewise(
    a: &[Inertial],
    b: &[Inertial],
    radius: &Rational,
    domain: TickInterval,
) -> Option<i128> {
    let mut best = None;
    for i in 0..a.len() {
        let Some(da) = segment_query_domain(a, i, domain) else {
            continue;
        };
        for j in 0..b.len() {
            let Some(db) = segment_query_domain(b, j, domain) else {
                continue;
            };
            let start = da.start.max(db.start);
            let end = da.end.min(db.end);
            if start > end {
                continue;
            }
            if let Some(tick) = first_contact(
                &a[i],
                &b[j],
                radius,
                TickInterval { start, end },
            ) {
                best = Some(best.map_or(tick, |t: i128| t.min(tick)));
            }
        }
    }
    best
}

/// Earliest light-cone arrival onto a piecewise receiver.
pub fn first_signal_arrival_piecewise(
    emission_tick: i128,
    emission: &Vec2,
    receiver: &[Inertial],
    domain: TickInterval,
) -> Option<i128> {
    let mut best = None;
    for i in 0..receiver.len() {
        let Some(d) = segment_query_domain(receiver, i, domain) else {
            continue;
        };
        if let Some(tick) = first_signal_arrival(emission_tick, emission, &receiver[i], d) {
            best = Some(best.map_or(tick, |t: i128| t.min(tick)));
        }
    }
    best
}

/// Does A u^2+B u+C <= 0 anywhere in (0,duration]? Here A is nonnegative.
/// The closed right endpoint and open left endpoint need separate treatment when
/// the only zero is a tangent at the left edge.
fn prefix_has_contact(a: &Rational, b: &Rational, c: &Rational, duration: &Rational) -> bool {
    if c < &r(0) {
        return true; // Continuity gives an overlap immediately after the open edge.
    }
    if a == &r(0) {
        // A is relative speed squared, so its zero implies B == 0 as well.
        return c <= &r(0);
    }
    if b >= &r(0) {
        return false; // The quadratic increases strictly after the open edge.
    }
    let minimum_at = (-b / (r(2) * a)).min(duration.clone());
    a * &minimum_at * &minimum_at + b * minimum_at + c <= r(0)
}

/// Binary search without signed subtraction overflow, valid across all i128 ticks.
fn first_true(mut start: i128, mut end: i128, predicate: impl Fn(i128) -> bool) -> Option<i128> {
    if !predicate(end) {
        return None;
    }
    while start < end {
        // Flipping the sign bit maps signed ordering bijectively to unsigned ordering.
        const SIGN: u128 = 1_u128 << 127;
        let low = (start as u128) ^ SIGN;
        let high = (end as u128) ^ SIGN;
        let middle = ((low + (high - low) / 2) ^ SIGN) as i128;
        if predicate(middle) {
            end = middle;
        } else {
            // middle < end while start < end, so the successor exists.
            start = middle + 1;
        }
    }
    Some(start)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn stationary(x: i128, y: i128) -> Inertial {
        Inertial::new(0, Vec2::new(x, y), Vec2::zero()).unwrap()
    }

    fn moving(x: i128, y: i128, vx: Rational, vy: Rational) -> Inertial {
        Inertial::new(0, Vec2::new(x, y), Vec2 { x: vx, y: vy }).unwrap()
    }

    #[test]
    fn inclusive_intervals_validate_and_include_single_ticks() {
        assert!(TickInterval::new(2, 1).is_err());
        assert!(TickInterval::new(1, 1).unwrap().contains(1));
        assert!(!TickInterval::new(1, 1).unwrap().contains(0));
    }

    #[test]
    fn tangent_and_point_crossing_between_tick_samples_are_not_missed() {
        let a = stationary(0, 0);
        let tangent = moving(-1, 1, r(2) / r(3), r(0));
        let crossing = moving(-1, 0, r(2) / r(3), r(0));
        let domain = TickInterval::new(0, 3).unwrap();
        assert!(tangent.state_at(1).norm_squared() > r(1));
        assert!(tangent.state_at(2).norm_squared() > r(1));
        assert_eq!(first_contact(&a, &tangent, &r(1), domain), Some(2));
        assert_eq!(first_contact(&a, &crossing, &r(0), domain), Some(2));
    }

    #[test]
    fn tangent_at_integer_boundary_belongs_only_to_ending_bin() {
        let a = stationary(0, 0);
        let tangent = moving(-1, 1, r(1) / r(2), r(0));
        assert_eq!(
            first_contact(&a, &tangent, &r(1), TickInterval::new(2, 2).unwrap()),
            Some(2)
        );
        assert_eq!(
            first_contact(&a, &tangent, &r(1), TickInterval::new(3, 10).unwrap()),
            None
        );
        assert_eq!(
            first_contact(&a, &tangent, &r(1), TickInterval::new(-10, 1).unwrap()),
            None
        );
    }

    #[test]
    fn continuous_contact_matches_independent_linear_interval_oracle_grid() {
        let a = stationary(0, 0);
        for position_twice in -8..=8 {
            for velocity_fifths in -4..=4 {
                for radius_twice in 0..=3 {
                    let position = r(position_twice) / r(2);
                    let speed = r(velocity_fifths) / r(5);
                    let radius = r(radius_twice) / r(2);
                    let b = Inertial::new(
                        0,
                        Vec2 {
                            x: position.clone(),
                            y: r(0),
                        },
                        Vec2 {
                            x: speed.clone(),
                            y: r(0),
                        },
                    )
                    .unwrap();
                    let expected = (-4..=6).find(|tick| {
                        if speed == r(0) {
                            return position >= -&radius && position <= radius;
                        }
                        // Independently solve the two LINEAR contact boundaries.
                        let one = (-&radius - &position) / &speed;
                        let two = (&radius - &position) / &speed;
                        let entry = one.clone().min(two.clone());
                        let exit = one.max(two);
                        entry <= r(*tick) && exit > r(*tick - 1)
                    });
                    let domain = TickInterval::new(-4, 6).unwrap();
                    assert_eq!(
                        first_contact(&a, &b, &radius, domain),
                        expected,
                        "x={position}, v={speed}, radius={radius}"
                    );
                    for split in -4..6 {
                        let left =
                            first_contact(&a, &b, &radius, TickInterval::new(-4, split).unwrap());
                        let right = first_contact(
                            &a,
                            &b,
                            &radius,
                            TickInterval::new(split + 1, 6).unwrap(),
                        );
                        assert_eq!(left.or(right), expected);
                    }
                }
            }
        }
    }

    #[test]
    fn receding_contact_invalid_radius_and_stationary_overlap() {
        let a = stationary(0, 0);
        let b = moving(2, 0, r(1) / r(2), r(0));
        let domain = TickInterval::new(1, 1_000_000_000).unwrap();
        assert_eq!(first_contact(&a, &b, &r(1), domain), None);
        assert_eq!(first_contact(&a, &a, &r(-1), domain), None);
        assert_eq!(first_contact(&a, &a, &r(0), domain), Some(1));
    }

    #[test]
    fn signal_arrival_matches_exhaustive_tick_oracle() {
        let emission = Vec2::new(1, -2);
        for vx in -3..=3 {
            for vy in -3..=3 {
                let receiver = moving(-2, 3, r(vx) / r(5), r(vy) / r(5));
                for emission_tick in -3..=3 {
                    let expected = (-5..=45).find(|tick| {
                        causal_reachable(emission_tick, &emission, *tick, &receiver.state_at(*tick))
                    });
                    assert_eq!(
                        first_signal_arrival(
                            emission_tick,
                            &emission,
                            &receiver,
                            TickInterval::new(-5, 45).unwrap()
                        ),
                        expected
                    );
                    if let Some(arrival) = expected {
                        assert_eq!(
                            first_signal_arrival(
                                emission_tick,
                                &emission,
                                &receiver,
                                TickInterval::new(-5, arrival - 1).unwrap()
                            ),
                            None
                        );
                    }
                }
            }
        }
    }

    #[test]
    fn lightcone_and_binary_search_handle_full_i128_range_without_overflow() {
        let origin = Vec2::zero();
        let far = Vec2 {
            x: r(i128::MAX) - r(i128::MIN),
            y: r(0),
        };
        assert!(causal_reachable(i128::MIN, &origin, i128::MAX, &far));
        assert!(!causal_reachable(i128::MAX, &far, i128::MIN, &origin));
        assert!(!causal_reachable(
            i128::MIN,
            &origin,
            i128::MAX,
            &(&far + Vec2::new(1, 0))
        ));
        let receiver = Inertial::new(i128::MIN, far, Vec2::zero()).unwrap();
        assert_eq!(
            first_signal_arrival(
                i128::MIN,
                &origin,
                &receiver,
                TickInterval::new(i128::MIN, i128::MAX).unwrap()
            ),
            Some(i128::MAX)
        );
        let a = stationary(0, 0);
        assert_eq!(
            first_contact(
                &a,
                &a,
                &r(0),
                TickInterval::new(i128::MIN, i128::MIN).unwrap()
            ),
            Some(i128::MIN)
        );
        for target in [i128::MIN, -1, 0, 1, i128::MAX] {
            assert_eq!(
                first_true(i128::MIN, i128::MAX, |tick| tick >= target),
                Some(target)
            );
        }
    }

    #[test]
    fn aabb_touch_counts_as_intersection() {
        let left = Aabb::from_points(&Vec2::new(0, 0), &Vec2::new(1, 1));
        let right = Aabb::from_points(&Vec2::new(1, 1), &Vec2::new(2, 2));
        assert!(left.intersects(&right));
        assert!(!left.intersects(&Aabb::from_points(&Vec2::new(2, 2), &Vec2::new(3, 3))));
    }
}
