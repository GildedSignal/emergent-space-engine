//! The compiled proper clock at every energy: a flyby's tube reads dt/dτ = E = f·u^t, from the first-order weak field
//! to γ = 10⁶ and beyond (the old weak branch's clock was first order in q and read 2E²/(E²+1): about 2 at any E ≫ 1, and
//! the Q48 `k` refused the key near E ≈ 1.75×10³). The oracle is the integer state itself, evaluated exactly (big integers):
//! E² = f²/(f − v_r²/f − v_t²), with f = 1 − 2/r. It shares no code with the crate.
use emergent_space::binding::{IntegerState, Rebinding, Trajectory};
use emergent_space::orbit::{OrbitKey, Passage, Scalar};
use num_bigint::BigInt;
use num_traits::ToPrimitive;

const LE: i32 = -34; // positions: n·2^-34 (M = 1)
const VE: i32 = -60; // velocities: n·2^-60 (c = 1)

/// An outbound flyby state at r₀ with impact parameter b at infinity and energy E (nominal: the quantized velocities set the
/// exact one): L = b·√(E²−1), so v_t = L/(r·u^t) = L·f/(r·E).
fn state(r0: f64, b: f64, e: f64) -> IntegerState {
    let f = 1.0 - 2.0 / r0;
    let vt = b * (e * e - 1.0).sqrt() * f / (r0 * e);
    let vr = (f * (f - vt * vt - f * f / (e * e))).sqrt();
    IntegerState {
        position: [(r0 * 2f64.powi(-LE)) as i64, 0],
        velocity: [(vr * 2f64.powi(-VE)) as i64, (vt * 2f64.powi(-VE)) as i64],
        length_exponent: LE as i16,
        velocity_exponent: VE as i16,
    }
}

/// E of the integer state, exactly: E² = f²/den, f = (P − 2^35)/P at r = P·2^-34, den = f − vr²/f − vt².
fn exact_e(st: &IntegerState) -> f64 {
    const S: usize = 300;
    let p = BigInt::from(st.position[0]);
    let pm = &p - (BigInt::from(1) << (1 - LE) as usize);
    let (vr, vt) = (BigInt::from(st.velocity[0]), BigInt::from(st.velocity[1]));
    let f = (&pm << S) / &p;
    let vr2_over_f = ((&vr * &vr * &p) << (S - 2 * (-VE) as usize)) / &pm;
    let vt2 = (&vt * &vt) << (S - 2 * (-VE) as usize);
    let den = &f - vr2_over_f - vt2;
    assert!(den > BigInt::from(0), "the state must be timelike");
    let e2: BigInt = ((&f * &f) << 64) / (den << S);
    (e2.to_f64().unwrap() / 2f64.powi(64)).sqrt()
}

fn d(x: Scalar) -> f64 {
    x.significand() as f64 * 2f64.powi(x.exponent() as i32 - 62)
}

/// The tube's own dt/dτ at the binding event (a window of Δt = 2^17 around it, inside the passage).
fn tube_rate(traj: &Trajectory, event: Scalar, peri_time: Scalar) -> f64 {
    let dt = Scalar::power_of_two(17);
    let at = |t: Scalar| traj.state(t.sub(peri_time).unwrap()).unwrap().proper_time;
    let (a, b) = (at(event), at(event.add(dt).unwrap()));
    d(dt) / d(b.sub(a).unwrap())
}

#[test]
fn the_tube_clock_is_e_at_every_energy_up_to_a_million() {
    let (r0, b) = (1.5e8, 9.0e7);
    let mut worst = 0.0f64;
    for nominal in [1.001, 1.01, 1.2, 1.5, 3.0, 10.0, 100.0, 1.0e3, 1.7e3, 3.0e3, 1.0e4, 1.0e5, 1.0e6] {
        let st = state(r0, b, nominal);
        let e = exact_e(&st);
        let rb = Rebinding::from_state(st, Scalar::ZERO, None).unwrap_or_else(|err| panic!("E {e}: {err:?}"));
        assert_eq!(rb.reconstruct().unwrap(), st, "E {e}: the binding must return the state it was made from, bit for bit");
        let rate = tube_rate(&rb.trajectory, rb.event_time, rb.periapsis_time);
        let err = (rate / e - 1.0).abs();
        println!("E {e:>14.6}: tube dt/dτ {rate:>14.6}, error {err:.2e}, gap carried: {}", rb.trajectory.key().gap.is_some());
        assert!(err < 1e-5, "E {e}: the tube's dt/dτ is {rate}");
        worst = worst.max(err);
    }
    println!("worst {worst:.2e}");
}

#[test]
fn the_gap_is_carried_only_where_the_first_order_clock_is_not_good_enough() {
    let (r0, b) = (1.5e8, 9.0e7);
    // A slow flyby (v∞ ≈ 10⁻⁴ c) and a bound-looking near-parabolic one keep their keys as before: no gap, the same bits.
    for nominal in [1.000000001, 1.0000001] {
        let rb = Rebinding::from_state(state(r0, b, nominal), Scalar::ZERO, None).unwrap();
        assert!(rb.trajectory.key().gap.is_none(), "E {nominal}: a gap where the first-order clock holds");
    }
    // A flyby at 0.1 c or more carries one.
    for nominal in [1.01, 1.5, 1.0e3, 1.0e6] {
        let rb = Rebinding::from_state(state(r0, b, nominal), Scalar::ZERO, None).unwrap();
        assert!(rb.trajectory.key().gap.is_some_and(|g| g.is_positive()), "E {nominal}: no gap");
    }
}

/// A control: the same keys without their gap are the old weak-branch clock, which must fail this gate.
#[test]
fn without_the_gap_the_old_clock_fails() {
    let (r0, b) = (1.5e8, 9.0e7);
    for nominal in [3.0, 10.0, 100.0] {
        let st = state(r0, b, nominal);
        let e = exact_e(&st);
        let rb = Rebinding::from_state(st, Scalar::ZERO, None).unwrap();
        let Trajectory::Passage(p) = &rb.trajectory else { panic!("a flyby is a passage") };
        let old = Passage::compile(OrbitKey { gap: None, ..p.key() }, p.outer_radius).unwrap();
        let rate = tube_rate(&Trajectory::Passage(old), rb.event_time, rb.periapsis_time);
        println!("E {e:>10.4}: old dt/dτ {rate:.4} (2E²/(E²+1) = {:.4})", 2.0 * e * e / (e * e + 1.0));
        assert!((rate / e - 1.0).abs() > 0.1, "E {e}: the planted old clock is right ({rate}): the control cannot fail");
    }
    // And the old key could not be compiled at all where the gap is under a quantum of the Q48 k (E ≳ 1.75×10³ = √(q·2^48): the more of them the more erratic, then none).
    for nominal in [1.0e5, 1.0e6] {
        let rb = Rebinding::from_state(state(r0, b, nominal), Scalar::ZERO, None).unwrap();
        let Trajectory::Passage(p) = &rb.trajectory else { panic!("a flyby is a passage") };
        assert!(Passage::compile(OrbitKey { gap: None, ..p.key() }, p.outer_radius).is_err(), "E {nominal}: the old key compiles");
    }
}

/// The gap moves the proper clock and nothing else: the same key with and without its gap reads out the same radius, angle,
/// advance and velocities at every time, bit for bit (positions and velocities read `k` alone; the coordinate clock is unchanged).
#[test]
fn the_gap_moves_the_proper_clock_and_nothing_else() {
    let (r0, b) = (1.5e8, 9.0e7);
    for nominal in [1.01, 3.0, 100.0, 1.0e3] {
        let rb = Rebinding::from_state(state(r0, b, nominal), Scalar::ZERO, None).unwrap();
        let Trajectory::Passage(with) = &rb.trajectory else { panic!("a flyby is a passage") };
        assert!(with.key().gap.is_some());
        let without = Passage::compile(OrbitKey { gap: None, ..with.key() }, with.outer_radius).unwrap();
        let mut moved = 0;
        for i in -8..=20i64 {
            let t = Scalar::integer(i * 150_000_000).add(rb.event_time).unwrap().sub(rb.periapsis_time).unwrap();
            let (Ok(a), Ok(c)) = (with.state(t), without.state(t)) else { continue };
            assert_eq!((a.radius, a.radial_angle, a.advance, a.radial_velocity, a.transverse_velocity, a.outbound),
                       (c.radius, c.radial_angle, c.advance, c.radial_velocity, c.transverse_velocity, c.outbound),
                       "E {nominal}, t = {i}e8: the gap moved a position or a velocity");
            moved += (a.proper_time != c.proper_time) as i32;
        }
        assert!(moved > 0, "E {nominal}: the gap must move the proper time somewhere");
    }
}
