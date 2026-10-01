//! Bit-identity of the dense order: the same battle in a free-fall frame, evaluated in
//! lockstep (`Chronon`, the reference) and sparse (`EventCore`), gives the same world digest,
//! the same log digest and the same tide digest (carries, epochs, counters), on eight seeded
//! scenes of 50 to 2000 bodies with contacts, run to 4096 chronons; the same across 1, 4 and 8
//! threads of the kick pass (the steppers themselves are single-threaded); and a kick applied
//! at a different epoch in one order breaks the equality.
//!
//! The scenes climb a ladder: the epoch shrinks from 256 chronons (a physically valid frame
//! for a small battle: the size rules of `frame.rs` hold) to 1 chronon (a kick and a
//! re-prediction of every body every chronon, far outside the physics: it exists to break the
//! sparse order). Scenes whose frame violates the size rules are stress scenes; the flags are
//! printed. Each test is one scene, under one minute.
use emergent_engine::{scenes, Battle, Frame, Outcome};
use emergent_lattice::law::{Tick, World};
use emergent_lattice::{chronon::Chronon, Stepper};
use emergent_lattice_event::EventCore;
use std::time::Instant;

const HORIZON: Tick = 4096;

struct Scene {
    name: &'static str,
    bodies: u64,
    q: i64,
    seed: u64,
    /// The fleets close at 2q/`div` per chronon.
    div: i64,
    /// Every body of a fleet shares one velocity (velocity classes in the event core).
    formation: bool,
    /// Mean motion 2^-k rad per chronon.
    k: u32,
    /// The tide is so strong that kicks to c are refused (a storm), instead of none.
    storm: bool,
}

/// A scene's frame: n = 2^-k. The orbit radius is the largest the weak-field rule allows
/// (n·R = c/4) when that also satisfies the extent rule for the battle's reach over the
/// horizon (32 × (genesis extent + 4 × the fleets' travel: a light body bouncing off a heavy one
/// leaves at up to 3v)): then the frame is valid.
/// Otherwise it is the extent rule's minimum and the orbit rule is violated: a stress scene.
fn build(s: &Scene) -> (World, Frame, bool) {
    let (w, extent) = scenes::battle(s.bodies, s.q, s.seed, s.div, s.formation);
    let r_orbit = (s.q << s.k) / 4;
    let r_extent = 32 * (extent + 4 * HORIZON * (s.q / s.div));
    let f = Frame::new(s.q, r_orbit.max(r_extent), 1u64 << (60 - s.k)).unwrap();
    let valid = f.orbit_speed_ok();
    (w, f, valid)
}

struct Run {
    out: Outcome,
    contacts: u64,
    secs: f64,
    battle_changed: u64,
    epochs: u64,
    refused: u64,
    extent_ok: bool,
    /// Some body holds a sub-quantum carry: the tide kicked it (a valid frame's tide is far below
    /// one velocity quantum over a battle, so its kicks live in the carries).
    carried: bool,
    /// Event core only: grids re-formed (genesis excluded).
    rebuilds: u64,
}

fn lockstep(w: &World, f: &Frame, threads: usize, shift: Tick) -> Run {
    let t = Instant::now();
    let mut b = Battle::new(Chronon::new(w.clone(), false).unwrap(), f.clone(), threads).with_epoch_shift(shift);
    b.run_to(HORIZON).unwrap();
    let secs = t.elapsed().as_secs_f64();
    let st = b.stats();
    Run { out: b.outcome(), contacts: b.stepper().log().contacts, secs, battle_changed: st.changed, epochs: st.epochs, refused: st.refused, extent_ok: f.extent_ok(st.max_r2), carried: b.carries().iter().any(|c| *c != [0, 0]), rebuilds: 0 }
}

fn sparse(w: &World, f: &Frame, threads: usize, shift: Tick) -> Run {
    let t = Instant::now();
    let mut b = Battle::new(EventCore::new(w.clone(), false).unwrap(), f.clone(), threads).with_epoch_shift(shift);
    b.run_to(HORIZON).unwrap();
    let secs = t.elapsed().as_secs_f64();
    let st = b.stats();
    Run { out: b.outcome(), contacts: b.stepper().log().contacts, secs, battle_changed: st.changed, epochs: st.epochs, refused: st.refused, extent_ok: f.extent_ok(st.max_r2), carried: b.carries().iter().any(|c| *c != [0, 0]), rebuilds: b.stepper().rebuilds() }
}

/// Sweep threads only on the scenes small enough to repeat the runs inside the minute.
fn scene(s: Scene, sweep_threads: bool) {
    let (w, f, orbit_ok) = build(&s);
    let a = lockstep(&w, &f, 1, 0);
    let b = sparse(&w, &f, 1, 0);
    println!(
        "{:<3} {:>5} bodies q={:<5} nT={:<6.3} E={:<5} epochs {:<5} contacts {:<7} kicked {:<8} refused {:<8} | valid: orbit {} extent {} | lockstep {:.2}s sparse {:.2}s ({} rebuilds) | digest {}",
        s.name,
        s.bodies,
        s.q,
        f.n_f64() * HORIZON as f64,
        f.epoch(),
        a.epochs,
        a.contacts,
        a.battle_changed,
        a.refused,
        orbit_ok,
        a.extent_ok,
        a.secs,
        b.secs,
        b.rebuilds,
        &a.out.world[..12]
    );
    assert_eq!(a.out, b.out, "{}: lockstep and sparse digests", s.name);
    assert!(a.contacts > 0 && a.epochs > 0 && a.carried, "{}: contacts and kicks must happen", s.name);
    assert!(!s.storm || a.refused > 0, "{}: the storm must refuse kicks", s.name);
    assert_eq!((a.contacts, a.epochs), (b.contacts, b.epochs));

    // Control: without its kicks (pushed past the horizon) the same battle ends elsewhere, so
    // the equality above is about the tide, not a scene that ignores it. (The same frame about the
    // non-rotating axes: `Frame::new` also turns the world from the co-rotating axes at genesis,
    // which is a change of coordinates, not a kick of the tide.)
    let inertial = Frame::on_orbit(s.q, f.radius(), f.n(), 0, 0, 0).unwrap();
    let unkicked = lockstep(&w, &inertial, 1, HORIZON + 1);
    assert_eq!(unkicked.epochs, 0);
    assert_ne!(unkicked.out.world, a.out.world, "{}: the tide must change the outcome", s.name);

    // B0, flat reduction: with the kicks pushed past the horizon, and with no parent mass (a
    // flat frame), the outcome is the plain lattice's.
    let mut plain = Chronon::new(w.clone(), false).unwrap();
    plain.run_to(HORIZON);
    assert_eq!((unkicked.out.world.clone(), unkicked.out.log.clone()), plain.outcome(), "{}: no kicks, the lattice's digests", s.name);
    let mut b0 = Battle::new(EventCore::new(w.clone(), false).unwrap(), Frame::flat(s.q).unwrap(), 1);
    b0.run_to(HORIZON).unwrap();
    assert_eq!(b0.stats().epochs, 0, "{}: a flat frame never kicks", s.name);
    assert_eq!(b0.stepper().outcome(), plain.outcome(), "{}: no mass, the lattice's digests", s.name);

    // Planted: a kick at a different epoch in one order breaks the equality (both ways).
    let late_sparse = sparse(&w, &f, 1, 1);
    let late_lockstep = lockstep(&w, &f, 1, 1);
    assert_ne!(late_sparse.out, a.out, "{}: sparse kicks one chronon late must differ from lockstep", s.name);
    assert_ne!(late_lockstep.out, b.out, "{}: lockstep kicks one chronon late must differ from sparse", s.name);
    assert_eq!(late_sparse.out, late_lockstep.out, "{}: shifted in both orders, the orders agree again", s.name);

    if sweep_threads {
        for threads in [4, 8] {
            assert_eq!(lockstep(&w, &f, threads, 0).out, a.out, "{}: lockstep, {threads} threads", s.name);
            assert_eq!(sparse(&w, &f, threads, 0).out, a.out, "{}: sparse, {threads} threads", s.name);
        }
    }
}

macro_rules! scenes {
    ($($fn_name:ident: $name:literal, $n:expr, $q:expr, $seed:expr, $div:expr, $form:expr, $k:expr, $storm:expr, $sweep:expr;)*) => {
        $(#[test] fn $fn_name() {
            scene(Scene { name: $name, bodies: $n, q: $q, seed: $seed, div: $div, formation: $form, k: $k, storm: $storm }, $sweep);
        })*
    };
}

// The ladder: the tide over the battle, n·T with T = 4096 chronons, grows from 0.03 (a valid
// frame) to 16 (a storm). The radial tide grows like exp(√3·n·t), so from n·T of about 1 the
// battle flies apart and leaves the frame's size rule; from about 4, kicks reach c and are
// refused. Those rungs are stress scenes: the integer law is defined there, the physics is not.
scenes! {
    s0_valid_50_e256: "s0", 50, 1024, 1, 32, false, 16, false, true;
    s1_100_e128: "s1", 100, 1024, 2, 8, false, 15, false, true;
    s2_200_e64: "s2", 200, 512, 3, 8, false, 14, false, true;
    s3_formation_400_e32: "s3", 400, 1024, 4, 16, true, 13, false, true;
    s4_800_e16: "s4", 800, 2048, 5, 16, false, 12, false, true;
    s5_formation_1200_e8: "s5", 1200, 1024, 6, 32, true, 11, false, true;
    s6_1600_e4: "s6", 1600, 1024, 7, 32, false, 10, false, true;
    s7_storm_formation_2000_e1: "s7", 2000, 1024, 8, 8, true, 8, true, true;
}

/// Control: the formation scenes really form velocity classes in the event core (so the kicks
/// dissolve them, and re-home the kicked members, in the runs above).
#[test]
fn formation_scenes_form_velocity_classes() {
    for (n, seed) in [(400u64, 4u64), (1200, 6)] {
        let (w, _) = scenes::battle(n, 1024, seed, 16, true);
        let mut e = EventCore::new(w, false).unwrap();
        e.run_to(1);
        assert_eq!(e.classes(), 2, "{n} bodies: one class per fleet");
        let (w, _) = scenes::battle(n, 1024, seed, 16, false);
        let mut e = EventCore::new(w, false).unwrap();
        e.run_to(1);
        assert_eq!(e.classes(), 0, "{n} bodies scattered: no class");
    }
}
