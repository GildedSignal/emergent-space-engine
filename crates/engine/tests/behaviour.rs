//! Behaviour of the free-fall frame, judged with floats inside the test (the law itself has
//! none): a body released in the frame follows the Clohessy–Wiltshire closed form, in both
//! evaluation orders; a reversed tide fails the same check; and the closed form itself is
//! checked against the full nonlinear two-body motion, which fixes the first-order limit.
//! The frame's axes do not rotate: Clohessy–Wiltshire is read in the axes that co-rotate with
//! the reference circle, so the body's offset is turned by −n·t (what a Hill-frame reading is).
//! A frame on an eccentric tube is checked against the full two-body motion (Tschauner–Hempel's
//! limit), and a frame's tube against Kepler's orbit.
//!
//! **Scale (stated).** Q = 2^20 (c = 2^20 lattice units per chronon, so one light-chronon is
//! 2^20 units and the lattice velocity quantum is 2^-20 c). Mean motion n = 2^-14 rad per
//! chronon (period P = 102,943 chronons); the epoch is E = 64 chronons (1,608 epochs per
//! period: the leapfrog's secular error in non-rotating axes grows as (n·t)²(n·E)²/24, which
//! at ten periods asks for n·E ≤ 2^-8). The body is released at rest at radial offset
//! dr = 2^22 units (4 light-chronons) from a parent orbit of radius R = 1000·dr = 4000
//! light-chronons: dr/R = 10^-3, and the orbit speed n·R = c/4.1 sits just under the weak-field
//! rule. The tide then moves the body by hundreds of units per chronon, so the velocity quantum
//! is a 0.1% effect.
use emergent_engine::{scenes, Battle, Frame};
use emergent_lattice::law::{Body, Law, Response, World};
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

/// A body's offset in the axes that co-rotate with the reference circle (radial, along-track):
/// the frame's non-rotating offset turned by −n·t.
fn hill(x: [i64; 2], n: f64, t: f64) -> [f64; 2] {
    let (c, s) = ((n * t).cos(), (n * t).sin());
    [c * x[0] as f64 + s * x[1] as f64, -s * x[0] as f64 + c * x[1] as f64]
}

struct Track {
    /// Largest |r − r_cw| / |r_cw| over every epoch of one period.
    max_rel: f64,
    epochs: i64,
    /// Final position, integer and closed form.
    end: ([f64; 2], [f64; 2]),
    /// Largest |x|² of the run, against the extent rule.
    extent_ok: bool,
}

/// Release a lone body at (dr, 0) with lattice velocity `v0`, run one period epoch by epoch,
/// and compare its position with the closed form after every epoch.
fn follow<S: Kickable>(mut battle: Battle<S>, v0: [i64; 2]) -> (Track, emergent_engine::Outcome) {
    let f = battle.frame().clone();
    let (n, e) = (f.n_f64(), f.epoch());
    let mut m: Vec<Motion> = Vec::new();
    let (mut max_rel, mut end) = (0f64, ([0.0, 0.0], [0.0, 0.0]));
    let epochs = f.period() / e;
    for j in 1..=epochs {
        battle.run_to(j * e).unwrap();
        battle.stepper().motions(&mut m);
        let want = cw(n, DR as f64, [v0[0] as f64, v0[1] as f64], (j * e) as f64);
        let got = hill(m[0].x, n, (j * e) as f64);
        let rel = ((got[0] - want[0]).powi(2) + (got[1] - want[1]).powi(2)).sqrt() / (want[0].powi(2) + want[1].powi(2)).sqrt();
        max_rel = max_rel.max(rel);
        end = (got, want);
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
    assert_eq!(f.epoch(), 64, "E is the largest power of two with n·E ≤ 2^-8");
    assert_eq!(f.period(), 102_943);
    assert!(f.orbit_speed_ok(), "n·R ≤ c/4");
    assert_eq!(R / DR, 1000, "dr/R = 10^-3");
}

#[test]
fn released_at_rest_follows_clohessy_wiltshire_within_one_percent_in_both_orders() {
    let (a, out_a) = lockstep(frame(), [0, 0]);
    let (b, out_b) = sparse(frame(), [0, 0]);
    println!(
        "CW behaviour, released at rest, dr/R = 1e-3, one period ({} epochs of {} chronons):\n  lockstep max relative position error {:.3e}\n  sparse   max relative position error {:.3e}\n  end of period: x = {:.0?}, closed form {:.0?}; extent rule (|x| ≤ R/32) held: {}",
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
    assert!(a.end.0[1] < -30.0 * DR as f64, "and so does the body");
}

#[test]
fn a_steady_shear_release_keeps_its_radius() {
    // v_y = −3n·dr/2 is the one solution that does not oscillate: n·dr = 256 units per
    // chronon here, so −384 is exact in lattice units. The radius must stay dr.
    let (a, _) = lockstep(frame(), [0, -384]);
    let (b, out_b) = sparse(frame(), [0, -384]);
    println!("steady shear: max relative error lockstep {:.3e}, sparse {:.3e}", a.max_rel, b.max_rel);
    assert!(a.max_rel < 1e-3 && b.max_rel < 1e-3);
    assert!((a.end.0[0] - DR as f64).abs() < DR as f64 / 1000.0, "radius {} against {DR}", a.end.0[0]);
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
fn an_epicycle_keeps_its_shape_and_its_guiding_centre_for_a_thousand_periods() {
    // v_y = −2n·dr = −512 (exact) is the drift-free epicycle: x = dr·cos nt, y = −2·dr·sin nt.
    // A thousand periods is 1.6×10^6 epochs of 64 chronons; the sparse order jumps between them
    // (lockstep would take a minute, and gives the same bits by the identity tests).
    //
    // Integer velocities carry a position error of up to E/2 units per epoch (the lattice drifts at
    // k; the true velocity is k + c/2^48). Were the tide to act at the lattice position, that error
    // would random-walk the guiding centre x_c = 4x + 2v_y/n (a constant of the linear motion), and
    // the shear would turn an error δ of x_c into an along-track drift of 3nδ/2 per chronon: the
    // tide's own amplification of a sub-quantum error, 1.7·n·√E·t^1.5 (150 dr after a thousand
    // periods here; it was the old frame's noise floor). The frame owes each body its dropped drift
    // and kicks it at its true position, lattice position plus the debt, so the error is only a
    // reading error, bounded by one epoch's drop, and the guiding centre does not move.
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
        let h = hill(m[0].x, f.n_f64(), (j * e) as f64);
        let (hx, hy) = (h[0].round() as i64, h[1].round() as i64);
        let s = &mut span[((j - 1) / per) as usize];
        *s = (s.0.min(hx), s.1.max(hx), s.2.min(hy), s.3.max(hy));
    }
    let dr = DR as f64;
    let first = span[0];
    let (xs, ys) = ((first.1 - first.0) as f64 / dr, (first.3 - first.2) as f64 / dr);
    let centre = |s: (i64, i64, i64, i64)| (s.2 + s.3) as f64 / 2.0 / dr;
    let drift = |p: i64| centre(span[p as usize - 1]);
    println!(
        "epicycle, first period: peak-to-peak x {xs:.5} dr (2 exact), y {ys:.5} dr (4 exact), centre y offset {:+.4} dr\ncentre y offset after 1, 10, 100, 1000 periods: {:+.4}, {:+.4}, {:+.4}, {:+.4} dr (the old frame's noise floor: 0.00, 0.1, 5, 149)",
        drift(1), drift(1), drift(10), drift(100), drift(1000)
    );
    assert!((xs / 2.0 - 1.0).abs() < 1e-3 && (ys / 4.0 - 1.0).abs() < 1e-3, "the epicycle's shape in its first period: {xs}, {ys}");
    for p in [1, 10, 100, 1000] {
        assert!(drift(p).abs() < 0.02, "after {p} periods the centre stays within 1% of the epicycle: {} dr", drift(p));
    }
    assert!(b.carries().iter().flatten().all(|&c| (-(1i64 << 47)..(1i64 << 47)).contains(&c)));
}

/// Two-body motion about a parent of GM = 1 (units: n = 1 at r = 1): the symplectic fourth-order
/// composition of velocity Verlet, small steps. Returns the position at each sample.
fn kepler_track(p0: [f64; 2], v0: [f64; 2], h_sample: f64, samples: usize, sub: usize) -> Vec<[f64; 2]> {
    let acc = |p: [f64; 2]| {
        let r3 = (p[0] * p[0] + p[1] * p[1]).powf(1.5);
        [-p[0] / r3, -p[1] / r3]
    };
    let verlet = |p: &mut [f64; 2], v: &mut [f64; 2], h: f64| {
        let a = acc(*p);
        for c in 0..2 {
            v[c] += 0.5 * h * a[c];
            p[c] += h * v[c];
        }
        let a = acc(*p);
        for c in 0..2 {
            v[c] += 0.5 * h * a[c];
        }
    };
    let c1 = 1.0 / (2.0 - 2.0_f64.cbrt());
    let c0 = 1.0 - 2.0 * c1;
    let (mut p, mut v) = (p0, v0);
    let h = h_sample / sub as f64;
    let mut out = vec![p];
    for _ in 0..samples {
        for _ in 0..sub {
            verlet(&mut p, &mut v, c1 * h);
            verlet(&mut p, &mut v, c0 * h);
            verlet(&mut p, &mut v, c1 * h);
        }
        out.push(p);
    }
    out
}

#[test]
fn a_frame_on_an_eccentric_tube_feels_the_tide_along_it() {
    // Tschauner–Hempel's limit: the frame's origin is on a Kepler orbit of eccentricity 0.3 (periapsis R,
    // so the tide swings by ((1+e)/(1−e))³ = 12 between periapsis and apoapsis and its axis turns
    // 2.2× faster at periapsis than a circle's), and members released at rest about it (small
    // offsets, so the linear tide is the whole story) must follow the full two-body motion. The
    // frame's tube is read from crates/space (the exact orbit), the tide from its r and r̂.
    let e = 0.3f64;
    let f = Frame::on_orbit(Q, R, N, (e * 2f64.powi(48)) as u64, 0, 0).unwrap();
    let n = f.n_f64();
    let period = 2.0 * std::f64::consts::PI / n * (1.0 - e).powf(-1.5);
    let stride = f.epoch() * 64;
    let samples = (2.0 * period / stride as f64) as usize;
    // Three members, 1e-4·R from the origin, at rest relative to it (same inertial velocity).
    let offs = [[4.2e5f64, 0.0], [-2.0e5, 3.0e5], [1.0e5, -4.0e5]];
    let bodies: Vec<Body> = offs.iter().enumerate().map(|(i, o)| Body::new(i as u64 + 1, [o[0] as i64, o[1] as i64], [0, 0], 1 + i as i64, 10, Response::Pass)).collect();
    let w = World::new(Q, None, bodies).unwrap().with_law(Law::RelativisticV1).unwrap();
    let h = stride as f64 * n;
    let v_peri = (1.0 + e).sqrt();
    let origin = kepler_track([1.0, 0.0], [0.0, v_peri], h, samples, 200);
    let truth: Vec<Vec<[f64; 2]>> = offs
        .iter()
        .map(|o| {
            let p = kepler_track([1.0 + o[0] / R as f64, o[1] / R as f64], [0.0, v_peri], h, samples, 200);
            p.iter().zip(&origin).map(|(a, b)| [(a[0] - b[0]) * R as f64, (a[1] - b[1]) * R as f64]).collect()
        })
        .collect();
    let mut worst = [0f64; 2];
    for (k, anchored) in [false, true].into_iter().enumerate() {
        let mut b = Battle::new(EventCore::new(w.clone(), false).unwrap(), f.clone(), 1);
        if anchored {
            b = b.with_anchoring(emergent_engine::AnchorPolicy { age_epochs: 64, enforce_orbit_rule: true }).unwrap();
        }
        let mut m: Vec<Motion> = Vec::new();
        for s in 1..=samples {
            let tick = s as i64 * stride;
            b.run_to(tick).unwrap();
            b.stepper().motions(&mut m);
            // The offsets from the origin are in the frame's own axes; anchored, the origin moves to the
            // members' centre of mass, so compare the members' offsets from their own centre of mass.
            let masses = [1.0, 2.0, 3.0];
            let mt: f64 = masses.iter().sum();
            let cm = |g: &dyn Fn(usize) -> [f64; 2]| [(0..3).map(|i| masses[i] * g(i)[0]).sum::<f64>() / mt, (0..3).map(|i| masses[i] * g(i)[1]).sum::<f64>() / mt];
            let (cg, ct) = (cm(&|i| [m[i].x[0] as f64, m[i].x[1] as f64]), cm(&|i| truth[i][s]));
            let spread = (0..3).map(|i| ((truth[i][s][0] - ct[0]).powi(2) + (truth[i][s][1] - ct[1]).powi(2)).sqrt()).fold(0.0, f64::max);
            for i in 0..3 {
                let d = [(m[i].x[0] as f64 - cg[0]) - (truth[i][s][0] - ct[0]), (m[i].x[1] as f64 - cg[1]) - (truth[i][s][1] - ct[1])];
                worst[k] = worst[k].max((d[0] * d[0] + d[1] * d[1]).sqrt() / spread);
            }
        }
        assert_eq!(b.stats().anchors_refused, 0, "{:?}", b.last_refusal());
    }
    println!(
        "eccentric tube (e = 0.3, period {:.0} chronons, E = {}), three members released at rest 1e-4·R from the origin, two periods:\n  group shape against the two-body motion: frame without anchors {:.3e}, with {:.3e}",
        period,
        f.epoch(),
        worst[0],
        worst[1]
    );
    assert!(worst[0] < 0.01 && worst[1] < 0.01, "within 1%: {worst:?}");
}
