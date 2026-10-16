//! Re-anchoring (crates/engine/src/anchor.rs): the frame recentres on its members' centre of
//! mass, rebinds its tube to that state (with the exact remainder) and hands members out of the
//! size rule, as events of the law.
//!
//! - **Behaviour** (floats only inside the test): five particles released at rest near
//!   dr/R = 1e-3 stay within 1% of a float64 RK4 two-body reference for ten periods, in both
//!   orders; the same frame without re-anchoring is 20% off by then (the control).
//! - **Exactness**: the recentring is integer arithmetic; momentum and energy identities hold
//!   exactly (energy to the cross term of the half-quantum momentum residual), carries stay in
//!   range, and threads change nothing.
//! - **Identity**: lockstep and sparse give the same world, log and tide digests with
//!   re-anchors (and members leaving) in valid and stress scenes, across 1, 4 and 8 threads; a
//!   re-anchor planted one chronon late in one order breaks the equality.
//! - **Rules**: a frame outside the weak-field rule is refused; members outside the size rule
//!   leave at the anchor and are counted.
use emergent_engine::{recentre, scenes, AnchorPolicy, Battle, Frame, Outcome};
use emergent_lattice::law::{Body, Law, Response, Tick, World};
use emergent_lattice::{chronon::Chronon, Kickable, Motion, Stepper};
use emergent_lattice_event::EventCore;
use std::process::Command;
use std::time::Instant;

const Q: i64 = 1 << 20;
const DR: i64 = 1 << 22;
const R: i64 = 1000 * DR;
const N: u64 = 1 << 46;
/// n = 2^-14 rad per chronon, in radians per chronon (a float, for the reference only).
const N_RAD: f64 = N as f64 / (1u64 << 60) as f64;
const TWO32: f64 = 4294967296.0;

fn frame() -> Frame {
    Frame::new(Q, R, N).unwrap()
}

/// Five test particles near a radial offset `eps·R` from the reference orbit (dr = 2^22 at
/// eps = 1e-3): the group's spread is fixed (0.05 dr, in units of `REL`), so its shear over ten
/// periods, about 19 dr at most, stays inside the size rule's R/32 = 31 dr.
const REL: [(f64, f64); 5] = [(0.0, 0.0), (1.0, 0.6), (-0.8, -0.4), (0.4, 1.0), (-0.2, -0.8)];
const MASSES: [i64; 5] = [1, 2, 3, 1, 2];
const SPREAD: f64 = 0.05 * DR as f64;

/// Released at rest in the rotating axes, or (`epicycle`) with the drift-free epicycle's
/// velocity v_y = −2n·x (each on its own epicycle about the reference orbit).
fn particles_at(eps: f64, epicycle: bool) -> World {
    let bodies = REL
        .iter()
        .zip(MASSES)
        .enumerate()
        .map(|(i, (&(a, b), m))| {
            let x = [(eps * R as f64 + SPREAD * a) as i64, (SPREAD * b) as i64];
            let k = if epicycle { [0, (-2.0 * N_RAD * x[0] as f64).round() as i64] } else { [0, 0] };
            Body::new(i as u64 + 1, x, k, m, 1000, Response::Pass)
        })
        .collect();
    World::new(Q, None, bodies).unwrap().with_law(Law::RelativisticV1).unwrap()
}

fn particles() -> World {
    particles_at(1e-3, false)
}

// ---------------------------------------------------------------------------------------
// The float reference: full two-body motion (RK4), units n = 1, R = 1.
// ---------------------------------------------------------------------------------------

/// Inertial positions of a particle at `p0` from the parent with velocity `vr` in the
/// rotating axes, at t = s·`h_sample` for s in 0..=`samples`, `sub` RK4 steps per sample.
fn kepler(p0: [f64; 2], vr: [f64; 2], samples: usize, h_sample: f64, sub: usize) -> Vec<[f64; 2]> {
    let h = h_sample / sub as f64;
    let acc = |p: [f64; 2]| {
        let r3 = (p[0] * p[0] + p[1] * p[1]).powf(1.5);
        [-p[0] / r3, -p[1] / r3]
    };
    let (mut p, mut v) = (p0, [vr[0] - p0[1], vr[1] + p0[0]]);
    let mut out = vec![p];
    for _ in 0..samples {
        for _ in 0..sub {
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
        out.push(p);
    }
    out
}

/// A body's inertial position at `t` radians, in the parent's rotating axes from the reference point (lattice units).
fn rotating(p: [f64; 2], t: f64) -> [f64; 2] {
    let (c, s) = (t.cos(), t.sin());
    [(c * p[0] + s * p[1]) * R as f64 - R as f64, (-s * p[0] + c * p[1]) * R as f64]
}

fn initial(b: &Body) -> ([f64; 2], [f64; 2]) {
    let u = R as f64 * N_RAD;
    ([1.0 + b.x[0] as f64 / R as f64, b.x[1] as f64 / R as f64], [b.k[0] as f64 / u, b.k[1] as f64 / u])
}

struct Truth {
    stride: Tick,
    /// [member][sample]: position from the reference point in the parent's rotating axes, lattice units.
    pos: Vec<Vec<[f64; 2]>>,
}

fn truth(w: &World, periods: i64) -> Truth {
    let f = frame();
    let stride = 10 * f.epoch();
    let samples = (periods * f.period() / stride) as usize;
    let h = stride as f64 * N_RAD;
    let pos = w
        .bodies
        .iter()
        .map(|b| {
            let (p0, vr) = initial(b);
            kepler(p0, vr, samples, h, 256).iter().enumerate().map(|(s, p)| rotating(*p, s as f64 * h)).collect()
        })
        .collect();
    Truth { stride, pos }
}

/// One body's true position at an arbitrary tick.
fn truth_at(w: &World, i: usize, tick: Tick) -> [f64; 2] {
    let (p0, vr) = initial(&w.bodies[i]);
    let t = tick as f64 * N_RAD;
    rotating(kepler(p0, vr, 1, t, (t / 0.004).ceil() as usize + 1)[1], t)
}

/// A member's position from the reference point in the parent's rotating axes, as the frame
/// has it: the tube's position and azimuth (the readout convention) composed with the member's
/// offset from the origin.
fn frame_position<S: Kickable>(b: &Battle<S>, tick: Tick, x: [i64; 2]) -> [f64; 2] {
    let t = b.tube_at(tick).expect("a frame with a parent has a tube");
    let th = t.azimuth as f64 / (1u64 << 60) as f64;
    let p = [t.radius as f64 + t.x[0] as f64 / TWO32 + x[0] as f64, t.x[1] as f64 / TWO32 + x[1] as f64];
    let (c, s) = (th.cos(), th.sin());
    [c * p[0] - s * p[1] - R as f64, s * p[0] + c * p[1]]
}

fn norm(a: [f64; 2]) -> f64 {
    (a[0] * a[0] + a[1] * a[1]).sqrt()
}

struct Track {
    /// Largest |r − r_true| / |r_true| over members and samples (r from the reference orbit).
    max_rel: f64,
    /// The group's shape: members' offsets from their centre of mass against the two-body ones,
    /// the largest error over the group's largest offset at that sample.
    max_shape: f64,
    per_period: Vec<f64>,
    out: Outcome,
    stats: emergent_engine::BattleStats,
    end: Tick,
}

fn track<S: Kickable>(mut b: Battle<S>, tr: &Truth) -> Track {
    let mut m: Vec<Motion> = Vec::new();
    let (mut max_rel, mut max_shape, mut per_period) = (0f64, 0f64, Vec::new());
    let per = frame().period();
    let (mut worst_this_period, mut period_no) = (0f64, 1);
    let samples = tr.pos[0].len() - 1;
    let mass: f64 = MASSES.iter().map(|&m| m as f64).sum();
    for s in 1..=samples {
        let tick = s as i64 * tr.stride;
        b.run_to(tick).unwrap();
        b.stepper().motions(&mut m);
        let got: Vec<[f64; 2]> = m.iter().map(|mi| frame_position(&b, tick, mi.x)).collect();
        for i in 0..m.len() {
            let want = tr.pos[i][s];
            let rel = norm([got[i][0] - want[0], got[i][1] - want[1]]) / norm(want);
            max_rel = max_rel.max(rel);
            worst_this_period = worst_this_period.max(rel);
        }
        // The group's shape. Anchored, the members' offsets are in the frame's axes, which turn with
        // the tube: read in the parent's axes by the azimuth. Unanchored, the axes are the parent's.
        let th = b.tube_at(tick).map_or(0.0, |t| t.azimuth as f64 / (1u64 << 60) as f64);
        let (c, sn) = (th.cos(), th.sin());
        let cm = |v: &dyn Fn(usize) -> [f64; 2]| -> [f64; 2] { [(0..5).map(|i| MASSES[i] as f64 * v(i)[0]).sum::<f64>() / mass, (0..5).map(|i| MASSES[i] as f64 * v(i)[1]).sum::<f64>() / mass] };
        let cm_true = cm(&|i| tr.pos[i][s]);
        let cm_frame = cm(&|i| [m[i].x[0] as f64, m[i].x[1] as f64]);
        let want: Vec<[f64; 2]> = (0..5).map(|i| [tr.pos[i][s][0] - cm_true[0], tr.pos[i][s][1] - cm_true[1]]).collect();
        let size = want.iter().map(|w| norm(*w)).fold(0.0, f64::max);
        for i in 0..5 {
            let d = [m[i].x[0] as f64 - cm_frame[0], m[i].x[1] as f64 - cm_frame[1]];
            let got = [c * d[0] - sn * d[1], sn * d[0] + c * d[1]];
            max_shape = max_shape.max(norm([got[0] - want[i][0], got[1] - want[i][1]]) / size);
        }
        if tick >= period_no * per {
            per_period.push(worst_this_period);
            (worst_this_period, period_no) = (0.0, period_no + 1);
        }
    }
    Track { max_rel, max_shape, per_period, out: b.outcome(), stats: b.stats().clone(), end: samples as i64 * tr.stride }
}

fn anchored<S: Kickable>(s: S, threads: usize) -> Battle<S> {
    Battle::new(s, frame(), threads).with_anchoring(AnchorPolicy::default()).unwrap()
}

fn pct(v: f64) -> String {
    format!("{:.3}%", 100.0 * v)
}

#[test]
fn ten_periods_stay_within_one_percent_of_two_body_motion_and_unanchored_drifts_beyond() {
    let w = particles();
    let tr = truth(&w, 10);
    let lock = track(anchored(Chronon::new(w.clone(), false).unwrap(), 1), &tr);
    let sparse = track(anchored(EventCore::new(w.clone(), false).unwrap(), 1), &tr);
    let control = track(Battle::new(EventCore::new(w.clone(), false).unwrap(), frame(), 1), &tr);
    let fmt = |v: &[f64]| v.iter().map(|e| format!("{:.2}%", 100.0 * e)).collect::<Vec<_>>().join(" ");
    println!(
        "five particles released at rest at dr/R = 1e-3, {} chronons = 10 periods (P = {}, E = {}), truth: RK4 two-body\n  positions from the reference orbit, worst error over members and samples:\n    re-anchored, lockstep: {}  by period: {}\n    re-anchored, sparse:   {}\n    not re-anchored (the linear tide about the genesis circle): {}  by period: {}\n  the group's shape (offsets from its centre of mass, over the group's size): re-anchored {}, not re-anchored {}\n  {} anchors, {} refused, {} handed out",
        lock.end,
        frame().period(),
        frame().epoch(),
        pct(lock.max_rel),
        fmt(&lock.per_period),
        pct(sparse.max_rel),
        pct(control.max_rel),
        fmt(&control.per_period),
        pct(lock.max_shape),
        pct(control.max_shape),
        lock.stats.anchors,
        lock.stats.anchors_refused,
        lock.stats.handed_out
    );
    assert!(lock.max_rel < 0.01 && sparse.max_rel < 0.01, "within 1%: {} {}", lock.max_rel, sparse.max_rel);
    // The control: without re-anchoring the tide is the linear one about the genesis circle, while the
    // group's centre of mass drifts along the orbit by 12π·dr a period: the linearisation fails (20%).
    assert!(control.max_rel > 0.10, "the control must fail: without re-anchoring the members are far off: {}", control.max_rel);
    assert!(lock.max_shape < 0.02, "re-anchored, the group's shape is within 2%: {}", lock.max_shape);
    assert!(control.max_shape > 0.10, "unanchored, the group's shape is far off: {}", control.max_shape);
    assert_eq!(lock.out, sparse.out, "both orders, the same bits, re-anchors included");
    assert!(lock.stats.anchors >= 80, "at least eight a period: {}", lock.stats.anchors);
    assert!(lock.stats.handed_out == 0);
    assert_eq!(lock.stats.anchors_refused, 0);
    // The threaded kick and anchor passes are chunked over the five bodies.
    for t in [4, 8] {
        let s = track(anchored(EventCore::new(w.clone(), false).unwrap(), t), &tr);
        assert_eq!(s.out, lock.out, "sparse, {t} threads");
    }
}

#[test]
fn the_error_scales_with_the_release_and_never_with_time() {
    // Released at rest on either side of the reference orbit: the anchored error is the group's own
    // second-order shape (a few 1e-4 at every time), the unanchored one grows with time (2% a period
    // at 1e-3). The size rule keeps eps below about 3e-3. Released on drift-free epicycles
    // (v_y = −2n·x) the group never separates and the offsets stay at about dr: what is left is the
    // lattice's dropped sub-quantum drift, sheared by the tide, so the cadence of the anchors that pay
    // it matters (the rows below anchor every 8 epochs, 256 chronons).
    println!("release (dr/R)        anchored worst   not anchored worst   anchored shape");
    for (eps, epicycle) in [(1e-4, false), (3e-4, false), (-1e-3, false), (1e-3, false), (3e-3, false), (3e-4, true), (1e-3, true)] {
        let w = particles_at(eps, epicycle);
        let tr = truth(&w, 10);
        let policy = AnchorPolicy { age_epochs: if epicycle { 8 } else { 0 }, enforce_orbit_rule: true };
        let a = track(Battle::new(EventCore::new(w.clone(), false).unwrap(), frame(), 1).with_anchoring(policy).unwrap(), &tr);
        let c = track(Battle::new(EventCore::new(w.clone(), false).unwrap(), frame(), 1), &tr);
        println!(
            "{eps:>+8.0e} {:<9}      {:>9}          {:>9}        {:>9}   ({} anchors, {} handed out, {} refused)",
            if epicycle { "epicycle" } else { "at rest" },
            pct(a.max_rel),
            pct(c.max_rel),
            pct(a.max_shape),
            a.stats.anchors,
            a.stats.handed_out,
            a.stats.anchors_refused
        );
        assert_eq!(a.stats.handed_out, 0, "the group stays in the frame at eps = {eps}");
        if epicycle {
            assert!(a.max_rel < 0.02, "eps {eps}: {}", a.max_rel);
        } else {
            assert!(a.max_rel < 0.5 * c.max_rel, "re-anchoring must help at eps = {eps}");
            let limit = if eps.abs() <= 1e-3 { 0.01 } else { 0.03 };
            assert!(a.max_rel < limit, "eps {eps}: {}", a.max_rel);
        }
    }
}

#[test]
fn the_error_does_not_depend_on_how_often_the_frame_re_anchors() {
    // Every anchor pays each body's sub-quantum drift into its position, so the lattice's rounding
    // error cannot grow past one anchor's age: from an anchor every 8 epochs (about 400 a period)
    // to one every 4,000 epochs (two a period), the worst error stays inside the 1%. (The same
    // scene without the settling depended on the cadence, and was 10× worse at dr/R = 1e-4.)
    let w = particles();
    let tr = truth(&w, 10);
    let mut worst = Vec::new();
    for age in [8u64, 200, 800, 1600] {
        let b = Battle::new(EventCore::new(w.clone(), false).unwrap(), frame(), 1).with_anchoring(AnchorPolicy { age_epochs: age, enforce_orbit_rule: true }).unwrap();
        let a = track(b, &tr);
        println!("anchor every {age:>3} epochs ({:>3} anchors): worst {}, group shape {}", a.stats.anchors, pct(a.max_rel), pct(a.max_shape));
        assert!(a.max_rel < 0.01, "age {age}: {}", a.max_rel);
        worst.push(a.max_rel);
    }
    let (lo, hi) = (worst.iter().cloned().fold(f64::MAX, f64::min), worst.iter().cloned().fold(0.0, f64::max));
    assert!(hi < 1.1 * lo, "the same error at every cadence: {lo} to {hi}");
}

#[test]
fn a_group_on_epicycles_keeps_its_guiding_centres_for_hundreds_of_periods() {
    // Three particles on drift-free epicycles (v_y = −2n·x, exact in lattice units for x a multiple
    // of 2^13): in the linear law they never separate. The lattice drops c·E/2^48 of position every
    // epoch; the frame owes it and kicks each body at its true position, so the guiding centres do not
    // random-walk (the old frame's noise: the group flew past the size rule within a few hundred
    // periods unanchored). What is left is the leapfrog's own weak exponential mode in non-rotating
    // axes: the shear's double zero is split by the scheme (growth rate ≈ 0.5·n·E per radian, so the
    // group's 0.1 dr grows e-fold every 80 periods at n·E = 2^-8; the same scene in floats on Strang
    // with E = 256 blows up past 3,000 dr in 500 periods).
    // Three hundred periods stay far inside the size rule (31 dr), anchored or not.
    let offs = [1i64 << 22, (1 << 22) + (1 << 18), (1 << 22) - (1 << 19)];
    let bodies: Vec<Body> = offs.iter().enumerate().map(|(i, &x)| Body::new(i as u64 + 1, [x, 0], [0, -x / (1 << 13)], 1 + i as i64, 1000, Response::Pass)).collect();
    let w = World::new(Q, None, bodies).unwrap().with_law(Law::RelativisticV1).unwrap();
    let mut plain = Battle::new(EventCore::new(w.clone(), false).unwrap(), frame(), 1);
    let mut anch = anchored(EventCore::new(w, false).unwrap(), 1);
    let mut m = Vec::new();
    let mut trace = Vec::new();
    for p in [1i64, 10, 100, 300] {
        plain.run_to(p * frame().period()).unwrap();
        anch.run_to(p * frame().period()).unwrap();
        let far = |b: &Battle<EventCore>, m: &mut Vec<Motion>| {
            b.stepper().motions(m);
            m.iter().zip(b.active()).filter(|(_, a)| **a).map(|(mi, _)| norm([mi.x[0] as f64, mi.x[1] as f64])).fold(0.0, f64::max) / DR as f64
        };
        trace.push((p, far(&plain, &mut m), far(&anch, &mut m)));
    }
    println!("farthest member from the origin, in dr, after 1, 10, 100, 300 periods: not re-anchored {:?}, re-anchored {:?}", trace.iter().map(|t| (t.1 * 100.0).round() / 100.0).collect::<Vec<_>>(), trace.iter().map(|t| (t.2 * 100.0).round() / 100.0).collect::<Vec<_>>());
    println!("re-anchored: {} anchors, {} handed out, {} refused", anch.stats().anchors, anch.stats().handed_out, anch.stats().anchors_refused);
    assert_eq!(anch.stats().handed_out, 0, "nobody leaves in three hundred periods");
    assert!(plain.frame().extent_ok(plain.stats().max_r2) || trace[3].1 < 31.0);
    assert!(trace.iter().all(|t| t.1 < 8.0 && t.2 < 8.0), "the group stays inside its epicycles (2 dr) and the slow mode's growth: {trace:?}");
}

#[test]
fn a_re_anchor_planted_late_in_one_order_breaks_the_equality() {
    let w = particles();
    let tr = truth(&w, 2);
    let a = track(anchored(Chronon::new(w.clone(), false).unwrap(), 1), &tr);
    fn late<S: Kickable>(s: S) -> Battle<S> {
        Battle::new(s, frame(), 1).with_anchoring(AnchorPolicy::default()).unwrap().with_anchor_shift(1)
    }
    let b = track(late(EventCore::new(w.clone(), false).unwrap()), &tr);
    let c = track(late(Chronon::new(w.clone(), false).unwrap()), &tr);
    assert_ne!(b.out, a.out, "sparse one chronon late must differ from lockstep on time");
    assert_ne!(c.out, a.out, "lockstep one chronon late must differ from lockstep on time");
    assert_eq!(b.out, c.out, "shifted in both orders, the orders agree again");
}

// ---------------------------------------------------------------------------------------
// Exactness
// ---------------------------------------------------------------------------------------

/// Deterministic pseudo-random numbers for the exactness scenes.
struct Lcg(u64);
impl Lcg {
    fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        self.0 >> 20
    }
    fn range(&mut self, lo: i64, hi: i64) -> i64 {
        lo + (self.next() % (hi - lo + 1) as u64) as i64
    }
}

#[test]
fn recentring_is_exact_in_integers() {
    let mut rng = Lcg(7);
    for (n, max_mass, span) in [(1usize, 4, 1 << 30), (2, 4, 1 << 30), (50, 4, 1 << 32), (1001, 65536, 1 << 38)] {
        let masses: Vec<i64> = (0..n).map(|_| rng.range(1, max_mass)).collect();
        let motions: Vec<Motion> = (0..n).map(|_| Motion { x: [rng.range(-span, span), rng.range(-span, span)], k: [rng.range(-3000, 3000), rng.range(-3000, 3000)] }).collect();
        let carries: Vec<[i64; 2]> = (0..n).map(|_| [rng.range(-(1 << 47), (1 << 47) - 1), rng.range(-(1 << 47), (1 << 47) - 1)]).collect();
        let r = recentre(&masses, &motions, &carries, 1).unwrap();
        let mass: i128 = masses.iter().map(|&m| m as i128).sum();
        assert_eq!(r.mass, mass);
        let vv = |m: &Motion, c: &[i64; 2], d: [i64; 2]| [(((m.k[0] + d[0]) as i128) << 48) + c[0] as i128, (((m.k[1] + d[1]) as i128) << 48) + c[1] as i128];
        let (mut p0, mut p1, mut x1, mut k0, mut k1) = ([0i128; 2], [0i128; 2], [0i128; 2], 0i128, 0i128);
        for i in 0..n {
            let (v0, v1) = (vv(&motions[i], &carries[i], [0, 0]), vv(&motions[i], &r.carries[i], r.dk[i]));
            let m = masses[i] as i128;
            for c in 0..2 {
                p0[c] += m * v0[c];
                p1[c] += m * v1[c];
                x1[c] += m * (motions[i].x[c] - r.centre[c]) as i128;
                assert!((-(1i64 << 47)..(1i64 << 47)).contains(&r.carries[i][c]), "carry in range");
            }
            k0 += m * (v0[0] * v0[0] + v0[1] * v0[1]);
            k1 += m * (v1[0] * v1[0] + v1[1] * v1[1]);
        }
        for c in 0..2 {
            // Momentum: exactly P − M·V, which is at most half a quantum (2^-49 c/Q) per unit of mass.
            assert_eq!(p1[c], p0[c] - mass * r.velocity[c], "n = {n}: P' = P − M·V exactly");
            assert!(p1[c].abs() * 2 <= mass, "n = {n}: the members' momentum is within half a quantum per unit mass: {}", p1[c]);
            assert!(x1[c].abs() * 2 <= mass, "n = {n}: the centre of mass is within half a lattice unit of the origin");
        }
        // Energy: Σ m|v|² = Σ m|v'|² + M|V|² + 2V·P' exactly (König), so it is preserved to the
        // cross term of the residual momentum: at most M·(|V_x| + |V_y|) in 2^-96 units.
        let (v, cross) = (r.velocity, 2 * (r.velocity[0] * p1[0] + r.velocity[1] * p1[1]));
        assert_eq!(k0, k1 + mass * (v[0] * v[0] + v[1] * v[1]) + cross, "n = {n}: energy, exactly with its cross term");
        assert!(cross.abs() <= mass * (v[0].abs() + v[1].abs()), "n = {n}: the cross term is one quantum of the tube's momentum");
        // Threads change nothing.
        for t in [4, 8, 64] {
            assert_eq!(recentre(&masses, &motions, &carries, t).unwrap(), r, "n = {n}, {t} threads");
        }
        println!("recentre n = {n:>4}: |ΣmΔx| ≤ M/2 ({} of {mass}), |P'| ≤ M/2 ({} of {mass}); energy identity exact; threads 1, 4, 8, 64 equal", x1[0].abs(), p1[0].abs());
    }
    assert!(recentre(&[], &[], &[], 1).is_none());
}

#[test]
fn a_re_anchor_conserves_momentum_in_both_orders() {
    // The particles at genesis: one anchor moves the origin to their centre of mass (1.0 dr) and rebinds
    // the tube to that state. The members' momentum, in the frame's non-rotating axes, goes into the
    // tube exactly (M·V), and what stays is within half a quantum (2^-49) per unit of mass.
    fn one<S: Kickable>(s: S) -> (emergent_engine::AnchorReport, [i128; 2], [i128; 2], Vec<Motion>) {
        let mut b = anchored(s, 1);
        let mut m = Vec::new();
        b.stepper().motions(&mut m);
        let p = |m: &[Motion], c: &[[i64; 2]]| {
            let mut p = [0i128; 2];
            for (i, mi) in m.iter().enumerate() {
                for k in 0..2 {
                    p[k] += MASSES[i] as i128 * (((mi.k[k] as i128) << 48) + c[i][k] as i128);
                }
            }
            p
        };
        let before = p(&m, b.carries());
        let rep = b.reanchor().unwrap();
        b.stepper().motions(&mut m);
        let after = p(&m, b.carries());
        (rep, before, after, m)
    }
    let (ra, ba, aa, ma) = one(Chronon::new(particles(), false).unwrap());
    let (rb, bb, ab, mb) = one(EventCore::new(particles(), false).unwrap());
    assert_eq!((&ra, ba, aa), (&rb, bb, ab), "the same report and momentum in both orders");
    assert_eq!(ma, mb);
    assert!(ra.moved && !ra.refused && ra.handed_out.is_empty());
    let mass = ra.mass;
    for c in 0..2 {
        assert_eq!(aa[c], ba[c] + ra.dp[c], "the stepper received exactly the planned change");
        assert!(aa[c].abs() * 2 <= mass, "the members' momentum is within half a quantum per unit mass: {} of {mass}", aa[c]);
        // And the tube took it, exactly: every member's velocity lost V as one number, so P' = P − M·V.
        assert_eq!(aa[c], ba[c] - mass * ra.velocity[c], "P' = P − M·V exactly");
    }
    println!(
        "genesis re-anchor of the five particles: centre {:?} lattice units ({:.3} dr), tube takes v = {:?}·2^-48; momentum before {:?}, after {:?} (M = {mass}, 2^-48 units)",
        ra.centre,
        ra.centre[0] as f64 / DR as f64,
        ra.velocity,
        ba,
        aa
    );
}

// ---------------------------------------------------------------------------------------
// The two orders, with re-anchors in the scene
// ---------------------------------------------------------------------------------------

const HORIZON: Tick = 4096;

struct Scene {
    name: &'static str,
    bodies: u64,
    q: i64,
    seed: u64,
    div: i64,
    formation: bool,
    /// Mean motion 2^-k.
    k: u32,
    /// The frame's radius is the extent rule's (32 × the battle's reach) divided by this, so members leave.
    squeeze: i64,
    /// Anchor every this many epochs.
    age: u64,
}

fn build(s: &Scene) -> (World, Frame) {
    let (w, extent) = scenes::battle(s.bodies, s.q, s.seed, s.div, s.formation);
    let r_orbit = (s.q << s.k) / 4;
    let r_extent = 32 * (extent + 4 * HORIZON * (s.q / s.div));
    let radius = if s.squeeze == 1 { r_orbit.max(r_extent) } else { (r_extent / s.squeeze).max(64) };
    (w, Frame::new(s.q, radius, 1u64 << (60 - s.k)).unwrap())
}

fn policy(s: &Scene) -> AnchorPolicy {
    AnchorPolicy { age_epochs: s.age, enforce_orbit_rule: false }
}

struct Run {
    out: Outcome,
    stats: emergent_engine::BattleStats,
    contacts: u64,
    secs: f64,
    active: usize,
}

fn lockstep(s: &Scene, w: &World, f: &Frame, threads: usize, shift: Tick) -> Run {
    let t = Instant::now();
    let mut b = Battle::new(Chronon::new(w.clone(), false).unwrap(), f.clone(), threads).with_anchoring(policy(s)).unwrap().with_anchor_shift(shift);
    b.run_to(HORIZON).unwrap();
    Run { out: b.outcome(), stats: b.stats().clone(), contacts: b.stepper().log().contacts, secs: t.elapsed().as_secs_f64(), active: b.active().iter().filter(|&&a| a).count() }
}

fn sparse(s: &Scene, w: &World, f: &Frame, threads: usize, shift: Tick) -> Run {
    let t = Instant::now();
    let mut b = Battle::new(EventCore::new(w.clone(), false).unwrap(), f.clone(), threads).with_anchoring(policy(s)).unwrap().with_anchor_shift(shift);
    b.run_to(HORIZON).unwrap();
    Run { out: b.outcome(), stats: b.stats().clone(), contacts: b.stepper().log().contacts, secs: t.elapsed().as_secs_f64(), active: b.active().iter().filter(|&&a| a).count() }
}

fn scene(s: Scene, sweep_threads: bool, expect_leavers: Option<bool>, expect_refused: bool) {
    let (w, f) = build(&s);
    let a = lockstep(&s, &w, &f, 1, 0);
    let b = sparse(&s, &w, &f, 1, 0);
    let st = &a.stats;
    println!(
        "{:<3} {:>5} bodies nT={:<6.3} E={:<5} R={:<12} | {} epochs, {} anchors (refused {}), {} handed out, {} still in | contacts {:<6} | lockstep {:.2}s sparse {:.2}s | digest {}",
        s.name,
        s.bodies,
        f.n_f64() * HORIZON as f64,
        f.epoch(),
        f.radius(),
        st.epochs,
        st.anchors,
        st.anchors_refused,
        st.handed_out,
        a.active,
        a.contacts,
        a.secs,
        b.secs,
        &a.out.world[..12]
    );
    assert_eq!(a.out, b.out, "{}: lockstep and sparse digests, re-anchors included", s.name);
    assert_eq!(a.stats.anchors, b.stats.anchors);
    assert!(a.stats.anchors >= 3, "{}: re-anchors must happen: {}", s.name, a.stats.anchors);
    assert_eq!(a.stats.anchors, b.stats.anchors);
    assert!(a.contacts > 0, "{}: contacts must happen", s.name);
    if let Some(leavers) = expect_leavers {
        assert_eq!(leavers, a.stats.handed_out > 0, "{}: members leave the frame iff the size rule breaks: {}", s.name, a.stats.handed_out);
    }
    assert_eq!(expect_refused, a.stats.anchors_refused > 0, "{}: anchors are refused (a velocity past c) only in a storm: {}", s.name, a.stats.anchors_refused);
    assert_eq!(a.stats.handed_out as usize + a.active, s.bodies as usize, "{}: the count is reported", s.name);

    // Control: the same battle in the same frame without re-anchoring ends elsewhere.
    let mut plain = Battle::new(Chronon::new(w.clone(), false).unwrap(), f.clone(), 1);
    plain.run_to(HORIZON).unwrap();
    assert_ne!(plain.outcome().world, a.out.world, "{}: re-anchoring must change the outcome", s.name);

    // Planted: a re-anchor one chronon late in one order breaks the equality (both ways).
    let late_sparse = sparse(&s, &w, &f, 1, 1);
    let late_lockstep = lockstep(&s, &w, &f, 1, 1);
    assert_ne!(late_sparse.out, a.out, "{}: sparse anchors one chronon late must differ from lockstep", s.name);
    assert_ne!(late_lockstep.out, b.out, "{}: lockstep anchors one chronon late must differ from sparse", s.name);
    assert_eq!(late_sparse.out, late_lockstep.out, "{}: shifted in both orders, the orders agree again", s.name);

    if sweep_threads {
        for threads in [4, 8] {
            assert_eq!(lockstep(&s, &w, &f, threads, 0).out, a.out, "{}: lockstep, {threads} threads", s.name);
            assert_eq!(sparse(&s, &w, &f, threads, 0).out, a.out, "{}: sparse, {threads} threads", s.name);
        }
    }
}

macro_rules! scenes {
    ($($fn_name:ident: $name:literal, $n:expr, $q:expr, $seed:expr, $div:expr, $form:expr, $k:expr, $squeeze:expr, $age:expr, $leavers:expr, $refused:expr;)*) => {
        $(#[test] fn $fn_name() {
            scene(Scene { name: $name, bodies: $n, q: $q, seed: $seed, div: $div, formation: $form, k: $k, squeeze: $squeeze, age: $age }, true, $leavers, $refused);
        })*
    };
}

// The ladder: valid frames keep everyone (a slow frame has few epochs, so a short age); stress
// frames have the tide of a battle that lasts several radians (nT up to 16) and a frame
// smaller than the battle (members leave, in numbers). The epoch is 2^-8 rad of the orbit
// (4× shorter than before the frame stopped rotating), so the ages are about 4× the
// earlier ones for the same anchors per orbit (more, smaller anchors).
scenes! {
    r0_valid_200_e512: "r0", 200, 1024, 11, 32, false, 17, 1, 4, Some(false), false;
    r1_stress_400_e16: "r1", 400, 1024, 12, 16, true, 13, 1, 24, Some(false), false;
    r2_squeezed_400_e16: "r2", 400, 1024, 13, 16, false, 13, 8, 24, Some(true), false;
    r3_squeezed_formation_800_e8: "r3", 800, 2048, 14, 16, true, 12, 16, 32, Some(true), false;
    r4_storm_1200_e2: "r4", 1200, 1024, 15, 8, false, 10, 4, 64, None, true;
    // The scene of r0 with an anchor at every epoch: the settle moves bodies by up to E/2 units each,
    // and without `revise_settled` the orders disagreed here (816 contacts in lockstep, 813 sparse).
    r5_anchor_every_epoch_200_e512: "r5", 200, 1024, 11, 32, false, 17, 1, 1, Some(false), false;
}

// ---------------------------------------------------------------------------------------
// The size rules
// ---------------------------------------------------------------------------------------

#[test]
fn the_weak_field_rule_is_enforced_and_a_stress_frame_must_say_so() {
    // n·R = c/4 exactly is legal; a hair more is not a frame.
    let ok = Frame::new(Q, (Q << 14) / 4, N).unwrap();
    assert!(ok.orbit_speed_ok());
    let bad = Frame::new(Q, (Q << 14) / 4 + 1, N).unwrap();
    assert!(!bad.orbit_speed_ok());
    let w = || scenes::lone(Q, [0, 0], [0, 0]);
    assert!(Battle::new(EventCore::new(w(), false).unwrap(), ok.clone(), 1).with_anchoring(AnchorPolicy::default()).is_ok());
    let e = Battle::new(EventCore::new(w(), false).unwrap(), bad.clone(), 1).with_anchoring(AnchorPolicy::default()).err().expect("refused");
    println!("refused: {e}");
    assert!(e.0.contains("weak-field"));
    assert!(Battle::new(EventCore::new(w(), false).unwrap(), bad, 1).with_anchoring(AnchorPolicy { age_epochs: 0, enforce_orbit_rule: false }).is_ok(), "stress is allowed when said");
    // A flat frame has nothing to anchor and is left alone.
    let flat = Battle::new(EventCore::new(w(), false).unwrap(), Frame::flat(Q).unwrap(), 1).with_anchoring(AnchorPolicy::default()).unwrap();
    assert!(flat.tube_at(0).is_none());
}

/// Eight members at rest: five within a few dr of each other (mass 4), three 50 to 80 dr out (mass 1): R/32 is 31 dr.
fn outliers() -> World {
    let mut bodies = Vec::new();
    for (i, (x, y)) in [(1.0, 0.0), (2.0, 1.0), (0.5, -1.0), (1.5, 0.5), (0.0, 0.0)].iter().enumerate() {
        bodies.push(Body::new(i as u64 + 1, [(x * DR as f64) as i64, (y * DR as f64) as i64], [0, 0], 4, 1000, Response::Pass));
    }
    for (j, (x, y)) in [(60.0, 0.0), (-50.0, 20.0), (10.0, 80.0)].iter().enumerate() {
        bodies.push(Body::new(6 + j as u64, [(x * DR as f64) as i64, (y * DR as f64) as i64], [0, 0], 1, 1000, Response::Pass));
    }
    World::new(Q, None, bodies).unwrap().with_law(Law::RelativisticV1).unwrap()
}

#[test]
fn members_outside_the_size_rule_leave_and_are_counted() {
    fn go<S: Kickable>(s: S, name: &str) -> Outcome {
        let mut b = Battle::new(s, frame(), 1).with_anchoring(AnchorPolicy::default()).unwrap();
        let rep = b.reanchor().unwrap();
        assert_eq!(rep.handed_out, vec![5, 6, 7], "{name}: the three far bodies leave, the cluster stays");
        assert_eq!(rep.mass, 20);
        assert_eq!(b.stats().handed_out, 3);
        assert_eq!(b.active(), &[true, true, true, true, true, false, false, false]);
        // The frame's own tube takes the cluster's centre of mass (x: 5 dr·4/20 = 1 dr; y: 0.5 dr·4/20 = dr/10 rounded);
        // the leavers' hand-off records name their state relative to it.
        assert_eq!(rep.centre, [DR, 419_430], "{name}");
        let h = b.handoffs();
        assert_eq!(h.iter().map(|h| h.index).collect::<Vec<_>>(), vec![5, 6, 7]);
        assert_eq!(h[0].x[0], 60 * DR - rep.centre[0], "{name}: position relative to the new origin");
        // Everyone left in the frame is within R/32 of the origin, exactly.
        let mut m = Vec::new();
        b.stepper().motions(&mut m);
        let (radius, tube) = (b.orbit().unwrap().0 as i128, b.tube_at(0).unwrap());
        for (i, mi) in m.iter().enumerate().take(5) {
            let r2 = mi.x[0] as i128 * mi.x[0] as i128 + mi.x[1] as i128 * mi.x[1] as i128;
            assert!(r2 << 10 <= radius * radius, "{name}: member {i} is within R/32: {:?}", mi.x);
        }
        // And it goes on: the tide keeps the leavers out and the rest in.
        b.run_to(50_000).unwrap();
        assert!(b.active().iter().take(5).all(|&a| a));
        println!("{name}: 3 of 8 members left at genesis (indices {:?}); tube after: radius {} → {}, x = ({:.3}, {:.3}) dr", rep.handed_out, R, tube.radius, tube.x[0] as f64 / TWO32 / DR as f64, tube.x[1] as f64 / TWO32 / DR as f64);
        b.outcome()
    }
    let a = go(Chronon::new(outliers(), false).unwrap(), "lockstep");
    let b = go(EventCore::new(outliers(), false).unwrap(), "sparse");
    assert_eq!(a, b, "both orders");
}

#[test]
fn a_frame_whose_members_all_leave_dissolves_and_keeps_running() {
    // Two pairs 40 dr either side of their centre of mass: R/32 is 31 dr, so nobody is inside the
    // rule, nobody is left to recentre on, and all four are handed out where they stand.
    let bodies: Vec<Body> = [(40.0, 1.0), (40.0, -1.0), (-40.0, 0.5), (-40.0, -0.5)]
        .iter()
        .enumerate()
        .map(|(i, (x, y))| Body::new(i as u64 + 1, [(x * DR as f64) as i64, (y * DR as f64) as i64], [0, 0], 1, 1000, Response::Pass))
        .collect();
    let w = World::new(Q, None, bodies).unwrap().with_law(Law::RelativisticV1).unwrap();
    fn go<S: Kickable>(s: S) -> (Outcome, Vec<Motion>) {
        let mut b = anchored(s, 1);
        let before = {
            let mut m = Vec::new();
            b.stepper().motions(&mut m);
            m
        };
        let rep = b.reanchor().unwrap();
        assert_eq!(rep.handed_out, vec![0, 1, 2, 3]);
        assert_eq!(rep.mass, 0, "nobody is left in the frame");
        assert!(!rep.moved && !rep.refused);
        assert_eq!(b.stats().handed_out, 4);
        assert!(b.active().iter().all(|&a| !a));
        let mut m = Vec::new();
        b.stepper().motions(&mut m);
        assert_eq!(m, before, "nothing moved");
        assert_eq!(b.handoffs().len(), 4);
        b.run_to(3 * frame().period()).unwrap();
        assert!(b.stats().anchors > 1, "later anchors of an empty frame are harmless: {}", b.stats().anchors);
        assert!(b.stats().handed_out == 4 && b.carries().iter().all(|c| *c == [0, 0]), "nothing is kicked once handed out");
        b.stepper().motions(&mut m);
        (b.outcome(), m)
    }
    let a = go(Chronon::new(w.clone(), false).unwrap());
    let b = go(EventCore::new(w, false).unwrap());
    assert_eq!(a, b, "both orders");
}

#[test]
fn a_wide_group_sheds_members_as_the_tide_shears_it() {
    // Radial offsets spread over ±25% of dr shear the group by up to 17 dr a period between its
    // extremes: members reach R/32 (31 dr) from the centre of mass and leave one by one, at the
    // anchors, while the rest keep going. Each hand-off record, composed with its tube, is where
    // the two-body motion has the member at that tick.
    let bodies: Vec<Body> = (0..12)
        .map(|i| Body::new(i as u64 + 1, [DR + (i as i64 - 6) * DR / 24, (i as i64 % 3 - 1) * DR / 50], [0, 0], 1 + i as i64 % 3, 1000, Response::Pass))
        .collect();
    let w = World::new(Q, None, bodies).unwrap().with_law(Law::RelativisticV1).unwrap();
    let mut s = anchored(EventCore::new(w.clone(), false).unwrap(), 1);
    let mut trace = Vec::new();
    for p in 1..=6 {
        s.run_to(p * frame().period()).unwrap();
        trace.push(s.stats().handed_out);
    }
    println!("a wide group (±25% dr): members handed out by the end of periods 1..6: {trace:?}");
    assert!(trace.windows(2).all(|p| p[0] <= p[1]) && *trace.last().unwrap() > 0, "members leave: {trace:?}");
    assert!(s.active().iter().any(|&a| a) && s.active().iter().any(|&a| !a));
    let mut worst = 0f64;
    for h in s.handoffs() {
        let th = h.tube.azimuth as f64 / (1u64 << 60) as f64;
        let p = [h.tube.radius as f64 + h.tube.x[0] as f64 / TWO32 + h.x[0] as f64, h.tube.x[1] as f64 / TWO32 + h.x[1] as f64];
        let (c, sn) = (th.cos(), th.sin());
        let got = [c * p[0] - sn * p[1] - R as f64, sn * p[0] + c * p[1]];
        let want = truth_at(&w, h.index, h.tick);
        let rel = norm([got[0] - want[0], got[1] - want[1]]) / norm(want);
        worst = worst.max(rel);
        // A member leaves at the edge of the size rule (r/32), measured from the centre of mass of those who
        // stay (so up to half as far again from the origin): the linear tide is off there by about 3 to 5%.
        assert!(rel < 0.06, "hand-off of body {} at tick {}: {:.3}% from the two-body motion", h.index, h.tick, 100.0 * rel);
    }
    println!("{} hand-off records, each within {} of the two-body position at its tick (the linear tide's limit at the size rule: 3 to 5%)", s.handoffs().len(), pct(worst));
    // The same in lockstep, members leaving included.
    let mut l = anchored(Chronon::new(w, false).unwrap(), 1);
    l.run_to(6 * frame().period()).unwrap();
    assert_eq!(l.outcome(), s.outcome());
}

// ---------------------------------------------------------------------------------------
// Cost
// ---------------------------------------------------------------------------------------

fn sh(cmd: &str, args: &[&str]) -> String {
    Command::new(cmd).args(args).output().map(|o| String::from_utf8_lossy(&o.stdout).trim().replace('\n', "; ")).unwrap_or_default()
}

fn machine_state(when: &str) {
    println!(
        "machine {when}: {} | {} | {} | {} | {}",
        sh("uptime", &[]).split("load averages:").last().map(|l| format!("load{}", l.trim_end())).unwrap_or_default(),
        sh("sysctl", &["-n", "vm.swapusage"]),
        sh("pmset", &["-g", "therm"]).lines().next().unwrap_or(""),
        sh("pmset", &["-g", "batt"]).lines().next().unwrap_or(""),
        sh("sysctl", &["-n", "machdep.cpu.brand_string"]),
    );
}

/// The cost of one re-anchor of a battle, hand-driven: the anchor call (centre of mass,
/// leavers, new velocities, the stepper's rebase) and, right after, the next chronon (which
/// for the sparse order pays the deferred rebuild of its grids and predictions).
fn cost_of<S: Kickable>(mut b: Battle<S>, n: usize, label: &str) -> (f64, f64, f64) {
    let e = b.frame().epoch();
    let (mut anchor, mut next, mut base, mut count) = (0u128, 0u128, 0u128, 0u128);
    for j in 1..=24i64 {
        let t = j * e + e / 2;
        b.run_to(t).unwrap();
        // Control: a plain chronon in the same state (the anchor's cost is what it adds).
        if j % 2 == 0 {
            let t0 = Instant::now();
            b.run_to(t + 1).unwrap();
            base += t0.elapsed().as_nanos();
            continue;
        }
        let t0 = Instant::now();
        let rep = b.reanchor().unwrap();
        let t1 = Instant::now();
        b.run_to(t + 1).unwrap();
        let t2 = Instant::now();
        assert!(!rep.refused);
        anchor += (t1 - t0).as_nanos();
        next += (t2 - t1).as_nanos();
        count += 1;
    }
    let per = |ns: u128, k: u128| ns as f64 / k as f64;
    let ctrl = per(base, 12);
    println!(
        "{label:<8}: re-anchor of {n} bodies: {:.0} µs in the call ({:.1} ns/body), then the next chronon {:.0} µs (a plain chronon there: {:.0} µs): {:.1} ns/body all in",
        per(anchor, count) / 1e3,
        per(anchor, count) / n as f64,
        per(next, count) / 1e3,
        ctrl / 1e3,
        (per(anchor, count) + per(next, count) - ctrl) / n as f64
    );
    (per(anchor, count), per(next, count), ctrl)
}

#[test]
fn cost_of_a_re_anchor_and_events_per_second() {
    machine_state("before");
    let (n, q) = (2000u64, 1024i64);
    let s = Scene { name: "cost", bodies: n, q, seed: 8, div: 8, formation: false, k: 11, squeeze: 1, age: 128 };
    let (w, f) = build(&s);
    println!("scene: {n} bodies, q = {q}, E = {} chronons, frame R = {} light-chronons, anchor every {} epochs", f.epoch(), f.radius() / q, s.age);
    let new_l = || Battle::new(Chronon::new(w.clone(), false).unwrap(), f.clone(), 1).with_anchoring(policy(&s)).unwrap();
    let new_s = || Battle::new(EventCore::new(w.clone(), false).unwrap(), f.clone(), 1).with_anchoring(policy(&s)).unwrap();
    cost_of(new_l(), n as usize, "lockstep");
    cost_of(new_s(), n as usize, "sparse");

    // A whole run: events per second, with and without re-anchoring, both orders.
    for (name, anchoring) in [("with re-anchors", true), ("without", false)] {
        let mut lock = Battle::new(Chronon::new(w.clone(), false).unwrap(), f.clone(), 1);
        let mut sp = Battle::new(EventCore::new(w.clone(), false).unwrap(), f.clone(), 1);
        if anchoring {
            lock = lock.with_anchoring(policy(&s)).unwrap();
            sp = sp.with_anchoring(policy(&s)).unwrap();
        }
        let t = Instant::now();
        lock.run_to(HORIZON).unwrap();
        let tl = t.elapsed().as_secs_f64();
        let t = Instant::now();
        sp.run_to(HORIZON).unwrap();
        let ts = t.elapsed().as_secs_f64();
        assert_eq!(lock.outcome(), sp.outcome(), "{name}: both orders");
        let st = sp.stats();
        let events = sp.stepper().log().contacts + sp.stepper().log().walls + st.anchors;
        println!(
            "{name:<16}: {} epochs, {} anchors ({} handed out), {} contacts | lockstep {tl:.2} s | sparse {ts:.2} s = {:.0} events/s ({} contacts + {} anchors), {:.0} anchors/s if they were the only work; kick pass {:.1} ms, anchors {:.1} ms (plan {:.1}, rebase {:.1}), {} rebuilds",
            st.epochs,
            st.anchors,
            st.handed_out,
            sp.stepper().log().contacts,
            events as f64 / ts,
            sp.stepper().log().contacts,
            st.anchors,
            st.anchors as f64 / ((st.anchor_plan_ns + st.anchor_apply_ns) as f64 / 1e9).max(1e-9),
            (st.read_ns + st.frame_ns + st.apply_ns) as f64 / 1e6,
            (st.anchor_plan_ns + st.anchor_apply_ns) as f64 / 1e6,
            st.anchor_plan_ns as f64 / 1e6,
            st.anchor_apply_ns as f64 / 1e6,
            sp.stepper().rebuilds()
        );
    }
    machine_state("after");
}



/// The lattice finding behind `Battle::revise_settled`: a `rebase` that shifts bodies by different
/// amounts and changes no velocity does not revise them, so a consumed contact survives a shift that
/// makes its pair approach again, and lockstep and sparse prune consumed contacts at different
/// times (every 64 chronons against when the list is walked): the pair fires in one order only.
/// Two Pass bodies cross and separate; body 2 is then moved 150 units from body 1 on the approaching
/// side (dk = 0), after 64 chronons. Both orders must log the second contact. Today lockstep logs it
/// and sparse does not (2 against 1); `lattice`/`lattice-event` should revise a body whose shift
/// differs from the others', after which `revise_settled` is deleted.
#[test]
fn a_rebase_with_per_body_shifts_and_no_kick_splits_the_orders() {
    let bodies = vec![Body::new(1, [-150, 0], [3, 0], 1, 100, Response::Pass), Body::new(2, [150, 0], [-3, 0], 1, 100, Response::Pass)];
    let w = World::new(1024, None, bodies).unwrap().with_law(Law::RelativisticV1).unwrap();
    let (mut c, mut e) = (Chronon::new(w.clone(), true).unwrap(), EventCore::new(w, true).unwrap());
    c.run_to(100);
    e.run_to(100);
    let mut m = Vec::new();
    c.motions(&mut m);
    let dx = [[0, 0], [m[0].x[0] + 150 - m[1].x[0], 0]];
    c.rebase(&dx, &[[0, 0], [0, 0]]).unwrap();
    e.rebase(&dx, &[[0, 0], [0, 0]]).unwrap();
    c.run_to(120);
    e.run_to(120);
    assert_eq!(c.log().contacts, e.log().contacts, "lockstep and sparse log the same contacts");
}
