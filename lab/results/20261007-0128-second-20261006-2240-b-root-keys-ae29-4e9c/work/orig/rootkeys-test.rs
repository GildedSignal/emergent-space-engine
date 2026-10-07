//! The root image of every event (the Opus memo §5 step 4; docs/law.md, "Handoffs are Lorentz" and
//! "Ties"): a body's events are held in its doll's clock, and the queue's key is the event's image on
//! the root clock through the doll chain's simultaneity shears — never "one tick is the same physical
//! time in every doll".
//!
//! **Frozen before the first run** (the memo's P6, plus the tie it implies):
//! 1. *P6.* A relativistic doll — a planet crossing the system at 0.5 c — with 1,000 members: at a
//!    settled state, every member's next event has its queue key equal to the shear image of its doll
//!    event (recomputed here, independently, in floats from the member's position and the planet's
//!    velocity: the agreement is the map's rounding, half a tick), and the queue's whole order is the
//!    same under 1, 4 and 8 threads and two orders of making the members (each member's whole history
//!    is the same record, as in `ties`).
//! 2. *The order follows the root clock, not the doll's.* Two members of the same doll, one ahead of
//!    the planet's motion and one behind it, their plans on the same doll ticks: at a cut between
//!    their root keys the behind one's item has resolved and the ahead one's has not, though their
//!    doll ticks are equal. Under the old key (the doll tick) both resolve or neither does; the
//!    control — a cut below both root keys — resolves neither.
use emergent_space::orbit::Scalar;
use emergent_universe::num::{from_f64, s, to_f64};
use emergent_universe::scenario::STAR_RADIUS;
use emergent_universe::universe::Universe;
use emergent_universe::{Config, Kind, OrbitSpec};

/// The planet crosses the system on a hyperbolic passage (a state-made tube): in at 5×10^5 root units
/// moving at 0.5 c along `+y`, so `sinh η = 0.577` for the whole run (the star's pull changes its
/// speed by 10^-6 over the cut).
const BETA: f64 = 0.5;
/// The doll's mass octave: its unit is `2^-10` root units and its edge (the Hill sphere at the
/// passage's periapsis separation) is `3.2 × 10^7` doll units wide.
const MASS_LOG2: i32 = -10;
const MEMBERS: usize = 1000;

/// The star, the planet at 0.5 c (the doll's centre), and `specs` (angle, phase, periapsis in doll
/// units), made in `make_order` (the k-th body made has the k-th spec; the ids follow the make
/// order). Returns the universe and the ids in `specs` order.
fn scene(specs: &[(u32, u32, i64)], make_order: &[usize]) -> (Universe, usize, Vec<usize>) {
    let mut u = Universe::new(s(STAR_RADIUS), Config::default());
    let planet = u
        .add_body_state(Kind::Planet, 0, [s(500_000), s(0)], [Scalar::ZERO, from_f64(BETA)], Scalar::ZERO)
        .unwrap();
    let doll = u.add_doll("fast", planet, MASS_LOG2, Scalar::raw(10, 10).unwrap()).unwrap();
    let mut ids = vec![0usize; specs.len()];
    for &k in make_order {
        let (angle, phase, r) = specs[k];
        ids[k] = u
            .add_body(
                Kind::Ship,
                OrbitSpec { doll, periapsis: Scalar::raw(r as i128, 0).unwrap(), e_q48: 0, clockwise: false, angle, phase },
                Scalar::ZERO,
            )
            .unwrap();
    }
    u.start().unwrap();
    (u, planet, ids)
}

/// The shear image of a member's next doll event, recomputed independently: the member's position `x`
/// at the event's tick (its committed tube) and the planet's velocity `w` then (its committed tube),
/// both in floats, give `γ·(w·x)` in root ticks — what the queue's integer shear rounds.
fn image(u: &Universe, planet: usize, i: usize) -> Option<(i64, f64)> {
    let rec = u.rec(i);
    let t = rec.plan.first()?.t;
    let b = u.bodies().binding_at(i, t)?;
    let (x, _) = b.cartesian(t).ok()?;
    let to_root = 2f64.powi(-(u.dolls[b.doll as usize].shift as i32));
    let xr = [to_f64(x[0]) * to_root, to_f64(x[1]) * to_root];
    let pb = u.bodies().binding_at(planet, t)?;
    let (_, w) = pb.cartesian(t).ok()?;
    let w2 = to_f64(w[0]) * to_f64(w[0]) + to_f64(w[1]) * to_f64(w[1]);
    let g = 1.0 / (1.0 - w2).sqrt();
    Some((t, g * (to_f64(w[0]) * xr[0] + to_f64(w[1]) * xr[1])))
}

#[test]
fn p6_every_events_root_key_is_the_shear_image_of_its_doll_event() {
    // Members spread over the doll: radii from 2^18 to 2^24 doll units (256 to 16,384 root units, all
    // well inside the edge), every angle, so the shear's key offsets spread over ±9,000 ticks.
    let specs: Vec<(u32, u32, i64)> = (0..MEMBERS)
        .map(|k| {
            let f = k as f64 / MEMBERS as f64;
            let r = (1u64 << 18) as f64 * (1.0 + 63.0 * f);
            ((f * 4294967296.0) as u32, (f * 4294967296.0) as u32, r as i64)
        })
        .collect();
    let straight: Vec<usize> = (0..MEMBERS).collect();
    let mut reversed = straight.clone();
    reversed.reverse();
    let cut = 300_000i64;
    let mut reference: Option<Vec<String>> = None;
    for (threads, order) in [(1usize, &straight[..]), (4, &reversed[..]), (8, &straight[..])] {
        let (mut u, planet, ids) = scene(&specs, order);
        u.threads = threads;
        u.settle(cut);
        assert!(u.stats.events() > MEMBERS as u64, "the members were stepped: {}", u.stats.events());
        // (a) every member's next event: the key is the doll tick plus the shear image, to the rounding.
        let (mut worst, mut moved) = (0f64, 0i64);
        let mut spread = (i64::MAX, i64::MIN);
        for &i in &ids {
            let (t, image_ticks) = image(&u, planet, i).expect("a live member with a next item");
            let key = u.horizon_of(i).expect("a next item");
            let off = (key - t) as f64 - image_ticks;
            assert!(off.abs() <= 0.5 + 1e-9, "member {i}: key {key} tick {t} image {image_ticks:.9} (off {off:.6})");
            worst = worst.max(off.abs());
            moved += (key != t) as i64;
            spread = (spread.0.min(key - t), spread.1.max(key - t));
        }
        assert!(worst <= 0.5, "the key is the rounded shear image: {worst}");
        assert!(moved > MEMBERS as i64 / 2, "the shear moves most keys: {moved}");
        assert!(spread.1 - spread.0 > 100, "the doll's spread is visible: {spread:?}");
        // (b) the order is one: each member's whole history is the same record under every schedule
        // and both make orders (the catalogue slot is an allocation, not a history).
        let records: Vec<String> = ids
            .iter()
            .map(|&i| {
                let rec = u.rec(i);
                format!("{:?}", rec).replace(&format!("Tube {{ key: {},", rec.b.tube.key), "Tube { key: _,")
            })
            .collect();
        match &reference {
            None => reference = Some(records),
            Some(r) => assert_eq!(records, *r, "threads {threads}: a member's history depends on the schedule"),
        }
        println!("threads {threads}: {} events, worst image miss {worst:.2e}, key offsets {spread:?}", u.stats.events());
    }
}

#[test]
fn the_order_follows_the_root_clock_not_the_dolls() {
    // Two members on one circle (2^20 doll units), at periapsis ahead of the planet's motion (angle a
    // quarter turn: the planet moves along +y) and behind it (three quarters). Their plans share
    // doll ticks; the ahead one's root key is the later by 2·sinh(η)·r. The old key (the doll tick)
    // orders them together, so a cut between their root keys resolves both or neither.
    let specs = [(1u32 << 30, 0u32, 1i64 << 20), (3u32 << 30, 0, 1 << 20)];
    let (mut u, _planet, ids) = scene(&specs, &[0, 1]);
    let (ahead, behind) = (ids[0], ids[1]);
    let first = |u: &Universe, i: usize| u.rec(i).plan.first().map(|p| p.t);
    let t0 = first(&u, ahead).expect("a planned member");
    assert_eq!(first(&u, behind), Some(t0), "the two share the doll's ticks");
    let (ka, kb) = (u.horizon_of(ahead).unwrap(), u.horizon_of(behind).unwrap());
    assert!(ka > kb && ka - kb > 16, "the shear separates the two keys: {ka} {kb}");
    u.settle((ka + kb) / 2);
    // The behind member's first item has resolved; the ahead one's has not, at equal doll ticks.
    assert!(u.rec(behind).b.event_time >= t0, "behind resolved past its first item: {}", u.rec(behind).b.event_time);
    assert!(u.rec(ahead).b.event_time < t0, "ahead resolved early: {}", u.rec(ahead).b.event_time);
    // The control: a cut below both root keys resolves neither member's first item.
    let (mut v, _, ids2) = scene(&specs, &[0, 1]);
    let (ka, kb) = (v.horizon_of(ids2[0]).unwrap(), v.horizon_of(ids2[1]).unwrap());
    v.settle(kb.min(ka) - 1);
    assert!(v.rec(ids2[0]).b.event_time < t0 && v.rec(ids2[1]).b.event_time < t0, "the control cut resolves neither");
}
