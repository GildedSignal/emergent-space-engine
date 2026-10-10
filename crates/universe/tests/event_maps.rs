//! The event-chart primitive only. P6's production-queue acceptance test is
//! `universe::root_keys_test::p6_first_slice_root_keys_are_the_shear_images`.
use emergent_space::orbit::Scalar;
use emergent_universe::lorentz::{EventMap, Frame};

fn map(local_anchor: [i128; 3], parent_anchor: [i128; 3], velocity: [Scalar; 2]) -> EventMap {
    EventMap { local_anchor, parent_anchor, frame: Frame::of(velocity).unwrap() }
}

#[test]
fn affine_events_round_trip_through_three_dolls() {
    let half = Scalar::raw(1, -1).unwrap();
    let zero = Scalar::ZERO;
    let maps = [
        map([99, -13, 56], [1 << 60, 991, -77], [half, zero]),
        map([-234, 51, 100], [675, -815, 700], [zero, half.negate()]),
        map([346, -11, 23], [-17, 551, -66], [half, half]),
    ];
    for n in -500i128..500 {
        let event = [n << 32, (n * 7 - 39) << 24, (n * n - 500) << 12];
        let mut image = event;
        for m in &maps { image = m.to_parent(image).unwrap(); }
        for m in maps.iter().rev() { image = m.to_local(image).unwrap(); }
        assert_eq!(image, event);
    }
    for m in maps {
        assert_eq!(m.to_parent(m.local_anchor).unwrap(), m.parent_anchor);
        assert_eq!(m.to_local(m.parent_anchor).unwrap(), m.local_anchor);
    }
}

#[test]
fn changing_boosts_needs_both_clock_anchors() {
    let zero = Scalar::ZERO;
    let old = map([0; 3], [0; 3], [Scalar::raw(1, -1).unwrap(), zero]);
    let at = [1_000_000, 0, 0];
    let parent = old.to_parent(at).unwrap();
    let new = map(at, parent, [zero; 2]);
    assert_eq!(new.to_parent(at).unwrap(), parent);
    assert!(new.to_parent([at[0] + 1, 0, 0]).unwrap()[0] > parent[0]);
    // Resetting the shear at tick zero sends the next event into the past.
    let reset = map([0; 3], [0; 3], [zero; 2]);
    assert!(reset.to_parent([at[0] + 1, 0, 0]).unwrap()[0] < parent[0]);
}

#[test]
fn a_stationary_chart_is_an_exact_translation_and_overflow_is_refused() {
    let m = map([10, 20, 30], [-30, -20, -10], [Scalar::ZERO; 2]);
    assert_eq!(m.to_parent([11, 22, 33]).unwrap(), [-29, -18, -7]);
    assert_eq!(m.to_local([-29, -18, -7]).unwrap(), [11, 22, 33]);
    assert!(m.to_parent([i128::MIN, 0, 0]).is_err());
    assert!(m.to_local([i128::MAX, 0, 0]).is_err());
}
