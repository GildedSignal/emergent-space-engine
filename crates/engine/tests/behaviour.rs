//! Behaviour of the free-fall frame, judged with floats inside the test (the law itself has
//! none): a body released in the frame follows the Clohessy–Wiltshire closed form, in both
//! evaluation orders; a reversed tide fails the same check; and the closed form itself is
//! checked against the full nonlinear two-body motion, which fixes the first-order limit.
//!
//! **Scale (stated).** Q = 2^20 (c = 2^20 lattice units per chronon, so one light-chronon is
//! 2^20 units and the lattice velocity quantum is 2^-20 c). Mean motion n = 2^-14 rad per
//! chronon (period P = 102,943 chronons); the epoch is E = 256 chronons (402 epochs per
//! period). The body is released at rest at radial offset dr = 2^22 units (4 light-chronons)
//! from a parent orbit of radius R = 1000·dr = 4000 light-chronons: dr/R = 10^-3, and the
//! orbit speed n·R = c/4.1 sits just under the weak-field rule. The tide then moves the body
//! by hundreds of units per chronon, so the velocity quantum is a 0.1% effect.
use emergent_engine::{scenes, Battle, Frame};
use emergent_lattice::{chronon::Chronon, Kickable, Motion};
use emergent_lattice_event::EventCore;

const Q: i64 = 1 << 20;
const DR: i64 = 1 << 22;
const R: i64 = 1000 * DR;
const N: u64 = 1 << 46;

fn frame() -> Frame {
    Frame::new(Q, R, N).unwrap()
}

/// The Clohessy–Wiltshire solution (Hill's equations: x radial, y along-track) from rest
/// or from a given initial velocity, at time t.
fn cw(n: f64, x0: f64, v0: [f64; 2], t: f64) -> [f64; 2] {
    let (c, s) = ((n * t).cos(), (n * t).sin());
    [
        (4.0 - 3.0 * c) * x0 + s / n * v0[0] + 2.0 / n * (1.0 - c) * v0[1],
        6.0 * (s - n * t) * x0 + 2.0 / n * (c - 1.0) * v0[0] + (4.0 * s - 3.0 * n * t) / n * v0[1],
    ]
}

struct Track {
    /// Largest |r − r_cw| / |r_cw| over every epoch of one period.
    max_rel: f64,
    epochs: i64,
    /// Final position, integer and closed form.
    end: ([i64; 2], [f64; 2]),
    /// Largest |x|² of the run, against the extent rule.
    extent_ok: bool,
}

/// Release a lone body at (dr, 0) with lattice velocity `v0`, run one period epoch by epoch,
/// and compare its position with the closed form after every epoch.
fn follow<S: Kickable>(mut battle: Battle<S>, v0: [i64; 2]) -> (Track, emergent_engine::Outcome) {
    let f = battle.frame().clone();
    let (n, e) = (f.n_f64(), f.epoch());
    let mut m: Vec<Motion> = Vec::new();
    let (mut max_rel, mut end) = (0f64, ([0, 0], [0.0, 0.0]));
    let epochs = f.period() / e;
    for j in 1..=epochs {
        battle.run_to(j * e).unwrap();
        battle.stepper().motions(&mut m);
        let want = cw(n, DR as f64, [v0[0] as f64, v0[1] as f64], (j * e) as f64);
        let got = [m[0].x[0] as f64, m[0].x[1] as f64];
        let rel = ((got[0] - want[0]).powi(2) + (got[1] - want[1]).powi(2)).sqrt() / (want[0].powi(2) + want[1].powi(2)).sqrt();
        max_rel = max_rel.max(rel);
        end = (m[0].x, want);
    }
    let extent_ok = f.extent_ok(battle.stats().max_r2);
    (Track { max_rel, epochs, end, extent_ok }, battle.outcome())
}

fn lockstep(f: Frame, v0: [i64; 2]) -> (Track, emergent_engine::Outcome) {
    let w = scenes::lone(Q, [DR, 0], v0);
    follow(Battle::new(Chronon::new(w, false).unwrap(), f, 1), v0)
}

fn sparse(f: Frame, v0: [i64; 2]) -> (Track, emergent_engine::Outcome) {
    let w = scenes::lone(Q, [DR, 0], v0);
    follow(Battle::new(EventCore::new(w, false).unwrap(), f, 1), v0)
}

#[test]
fn the_frame_is_what_the_scale_says() {
    let f = frame();
    assert_eq!(f.epoch(), 256, "E is the largest power of two with n·E ≤ 2^-6");
    assert_eq!(f.period(), 102_943);
    assert!(f.orbit_speed_ok(), "n·R ≤ c/4");
    assert_eq!(R / DR, 1000, "dr/R = 10^-3");
}

#[test]
fn released_at_rest_follows_clohessy_wiltshire_within_one_percent_in_both_orders() {
    let (a, out_a) = lockstep(frame(), [0, 0]);
    let (b, out_b) = sparse(frame(), [0, 0]);
    println!(
        "CW behaviour, released at rest, dr/R = 1e-3, one period ({} epochs of {} chronons):\n  lockstep max relative position error {:.3e}\n  sparse   max relative position error {:.3e}\n  end of period: x = {:?}, closed form {:?}; extent rule (|x| ≤ R/32) held: {}",
        a.epochs,
        frame().epoch(),
        a.max_rel,
        b.max_rel,
        a.end.0,
        a.end.1,
        a.extent_ok
    );
    assert!(a.max_rel < 0.01, "lockstep {:.3e}", a.max_rel);
    assert!(b.max_rel < 0.01, "sparse {:.3e}", b.max_rel);
    assert_eq!(out_a, out_b, "one body, both orders, the same bits");
    // The drift is real: 12π·dr along the orbit, so the check is not passed by standing still.
    assert!(a.end.1[1] < -30.0 * DR as f64, "the closed form drifts by 12π·dr per period");
    assert!((a.end.0[1] as f64) < -30.0 * DR as f64, "and so does the body");
}

#[test]
fn a_steady_shear_release_keeps_its_radius() {
    // v_y = −3n·dr/2 is the one solution that does not oscillate: n·dr = 256 units per
    // chronon here, so −384 is exact in lattice units. The radius must stay dr.
    let (a, _) = lockstep(frame(), [0, -384]);
    let (b, out_b) = sparse(frame(), [0, -384]);
    println!("steady shear: max relative error lockstep {:.3e}, sparse {:.3e}", a.max_rel, b.max_rel);
    assert!(a.max_rel < 1e-3 && b.max_rel < 1e-3);
    assert!((a.end.0[0] - DR).abs() < DR / 1000, "radius {} against {DR}", a.end.0[0]);
    assert_eq!(out_b, lockstep(frame(), [0, -384]).1);
}

#[test]
fn a_reversed_tide_fails_the_behaviour_check() {
    let planted = frame().planted_tide_sign(-1);
    let (a, _) = lockstep(planted.clone(), [0, 0]);
    let (b, _) = sparse(planted, [0, 0]);
    println!("planted wrong-sign tide: max relative error lockstep {:.3e}, sparse {:.3e}", a.max_rel, b.max_rel);
    assert!(a.max_rel > 0.01 && b.max_rel > 0.01, "the check must fail: {:.3e}, {:.3e}", a.max_rel, b.max_rel);
}

/// The full two-body motion in float (RK4), for a test particle released at rest in the
/// rotating frame at dr/R = `eps`, sampled against the closed form at `frac` of a period:
/// the relative position error, and the absolute one in units of dr.
/// Units: n = 1, R = 1.
fn nonlinear_error(eps: f64, frac: f64) -> (f64, f64) {
    let steps = 20_000usize;
    let h = 2.0 * std::f64::consts::PI / steps as f64;
    let acc = |p: [f64; 2]| {
        let r3 = (p[0] * p[0] + p[1] * p[1]).powf(1.5);
        [-p[0] / r3, -p[1] / r3]
    };
    let (mut p, mut v) = ([1.0 + eps, 0.0], [0.0, 1.0 + eps]);
    let end = (steps as f64 * frac) as usize;
    for _ in 0..end {
        let a1 = acc(p);
        let (p2, v2) = ([p[0] + 0.5 * h * v[0], p[1] + 0.5 * h * v[1]], [v[0] + 0.5 * h * a1[0], v[1] + 0.5 * h * a1[1]]);
        let a2 = acc(p2);
        let (p3, v3) = ([p[0] + 0.5 * h * v2[0], p[1] + 0.5 * h * v2[1]], [v[0] + 0.5 * h * a2[0], v[1] + 0.5 * h * a2[1]]);
        let a3 = acc(p3);
        let (p4, v4) = ([p[0] + h * v3[0], p[1] + h * v3[1]], [v[0] + h * a3[0], v[1] + h * a3[1]]);
        let a4 = acc(p4);
        p = [p[0] + h / 6.0 * (v[0] + 2.0 * v2[0] + 2.0 * v3[0] + v4[0]), p[1] + h / 6.0 * (v[1] + 2.0 * v2[1] + 2.0 * v3[1] + v4[1])];
        v = [v[0] + h / 6.0 * (a1[0] + 2.0 * a2[0] + 2.0 * a3[0] + a4[0]), v[1] + h / 6.0 * (a1[1] + 2.0 * a2[1] + 2.0 * a3[1] + a4[1])];
    }
    let t = end as f64 * h;
    let (c, s) = (t.cos(), t.sin());
    let d = [p[0] - c, p[1] - s];
    let got = [d[0] * c + d[1] * s, -d[0] * s + d[1] * c];
    let want = cw(1.0, eps, [0.0, 0.0], t);
    let abs = ((got[0] - want[0]).powi(2) + (got[1] - want[1]).powi(2)).sqrt();
    (abs / (want[0].powi(2) + want[1].powi(2)).sqrt(), abs / eps)
}

#[test]
fn the_closed_form_is_first_order_and_the_size_rule_says_how_first() {
    // Independent of the frame's algebra: Newton's two-body problem, RK4, transformed to the
    // rotating frame. It confirms the tide, its sign and the Coriolis coupling (the linear
    // model is off by the neglected quadratic term only), and it measures the first-order limit.
    let (half, one, tenth) = (nonlinear_error(1e-3, 0.5).0, nonlinear_error(1e-3, 1.0).0, nonlinear_error(1e-4, 1.0).0);
    let (hundredth, in_dr) = nonlinear_error(1e-2, 1.0);
    println!("linear model against the two-body motion: dr/R = 1e-3: {half:.4} at half a period, {one:.4} at one; dr/R = 1e-4: {tenth:.5} at one; dr/R = 1e-2: {hundredth:.4} at one");
    assert!(half < 0.01, "within 1% for half a period at dr/R = 1e-3: {half}");
    assert!(one > 0.01 && one < 0.03, "about 2% after one period: {one}");
    assert!((7.0..14.0).contains(&(one / tenth)), "the error scales with dr/R: ratio {}", one / tenth);
    // The red-team (H0203): about 7.7 dr off after one period at dr/R = 0.01.
    println!("dr/R = 1e-2: {in_dr:.2} dr off after one period (red-team: 7.7)");
    assert!((7.0..8.4).contains(&in_dr), "the red-team's 7.7 dr: {in_dr}");
}

#[test]
fn an_epicycle_keeps_its_shape_for_a_period_and_drifts_by_the_quantum_noise_after() {
    // v_y = −2n·dr = −512 (exact) is the drift-free epicycle: x = dr·cos nt, y = −2·dr·sin nt.
    // A thousand periods is 4×10^5 epochs of 256 chronons; the sparse order jumps between them
    // (lockstep would take a minute, and gives the same bits by the identity tests).
    //
    // Within the first period (the frame's whole life: see the size rule) the shape holds.
    // After that the guiding centre moves, and it is a finding. Integer velocities carry a
    // position error of up to E/2 units per epoch (the lattice drifts at k; the true velocity
    // is k + c/2^48). That error random-walks the guiding centre x_c = 4x + 2v_y/n, and the
    // shear turns an error δ of x_c into an along-track drift of 3nδ/2 per chronon: the tide's
    // own amplification of a sub-quantum error, growing like t^1.5, not exponentially. The
    // check below is that it stays within the random-walk estimate of the noise.
    let f = frame();
    let e = f.epoch();
    let per = f.period() / e;
    let periods = 1000;
    let mut b = Battle::new(EventCore::new(scenes::lone(Q, [DR, 0], [0, -512]), false).unwrap(), f.clone(), 1);
    let mut m: Vec<Motion> = Vec::new();
    // Per period: (min x, max x, min y, max y).
    let mut span = vec![(i64::MAX, i64::MIN, i64::MAX, i64::MIN); periods as usize];
    for j in 1..=periods * per {
        b.run_to(j * e).unwrap();
        b.stepper().motions(&mut m);
        let s = &mut span[((j - 1) / per) as usize];
        *s = (s.0.min(m[0].x[0]), s.1.max(m[0].x[0]), s.2.min(m[0].x[1]), s.3.max(m[0].x[1]));
    }
    let dr = DR as f64;
    let first = span[0];
    let (xs, ys) = ((first.1 - first.0) as f64 / dr, (first.3 - first.2) as f64 / dr);
    let centre = |s: (i64, i64, i64, i64)| (s.2 + s.3) as f64 / 2.0 / dr;
    // Random-walk estimate of the along-track drift after t chronons: 3n/2 · (4E/√12)·√(t/E) · t.
    let estimate = |periods: i64| {
        let t = (periods * per * e) as f64;
        1.5 * f.n_f64() * (4.0 * e as f64 / 12f64.sqrt()) * (t / e as f64).sqrt() * t / dr
    };
    let drift = |p: i64| centre(span[p as usize - 1]);
    println!(
        "epicycle, first period: peak-to-peak x {xs:.5} dr (2 exact), y {ys:.5} dr (4 exact), centre y offset {:+.4} dr\ncentre y offset after 1, 10, 100, 1000 periods: {:+.3}, {:+.3}, {:+.2}, {:+.1} dr; random-walk estimate of the quantum noise: {:.2}, {:.1}, {:.0}, {:.0} dr",
        drift(1), drift(1), drift(10), drift(100), drift(1000), estimate(1), estimate(10), estimate(100), estimate(1000)
    );
    assert!((xs / 2.0 - 1.0).abs() < 3e-3 && (ys / 4.0 - 1.0).abs() < 3e-3, "the epicycle's shape in its first period: {xs}, {ys}");
    assert!(drift(1).abs() < 0.02, "within the first period the centre stays within 1% of the epicycle: {} dr", drift(1));
    for p in [10, 100, 1000] {
        assert!(drift(p).abs() < 3.0 * estimate(p), "after {p} periods the drift is the quantum noise's: {} dr against {}", drift(p), estimate(p));
    }
    assert!(b.carries().iter().flatten().all(|&c| (-(1i64 << 47)..(1i64 << 47)).contains(&c)));
}
