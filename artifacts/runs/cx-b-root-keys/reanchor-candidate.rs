//! Step 4's cheapest falsifier: the first simultaneous slice, before any evolution.
//! This deliberately exercises Universe::key_of and its actual Calendar. It does not
//! claim to test the later sparse/dense physical histories: a wrong first key already
//! fails P6. All positions and the boost are exact integers; no float is an oracle.
use super::*;
use crate::body::Item;
use crate::lorentz::Frame;
use crate::num::s;

const MEMBERS: usize = 1_000;

fn scene() -> (Universe, Vec<usize>) {
    let mut u = Universe::new(Scalar::ZERO, Config::default());
    // A passage with exactly w = (0, 1/2), at its binding event. Building the
    // coordinate doll directly avoids add_doll's unrelated bound-orbit retune.
    let centre = u.add_body_state(
        Kind::Planet, 0, [s(1 << 24), Scalar::ZERO],
        [Scalar::ZERO, Scalar::raw(1, -1).unwrap()], Scalar::ZERO,
    ).unwrap();
    let doll = DollRec::child("P6", 0, Mass::pow2(-10), centre,
        u.rec(centre).b.tube, Scalar::ZERO, s(1 << 30)).unwrap();
    u.dolls.push(doll);
    u.sources.push(Vec::new());
    let template = u.add_body(Kind::Ship, OrbitSpec {
        doll: 1, periapsis: s(1 << 24), e_q48: 0,
        clockwise: false, angle: 0, phase: 0,
    }, Scalar::ZERO).unwrap();
    let rec = u.rec(template);
    let info = u.info[template];
    let mut ids = vec![template];
    for _ in 1..MEMBERS {
        ids.push(u.bodies.push(rec.clone()));
        u.info.push(info);
    }
    // Identical local ticks, distinct places. Pairs share a place to test id ties.
    // IDs visit the upper semicircle in reverse spatial order, so sorting by the
    // unchanged local tick cannot accidentally give the Lorentz order.
    for (n, &i) in ids.iter().enumerate() {
        let mut r = u.rec(i);
        r.b.tube.periapsis_angle = ((n / 2) as u64 * (1u64 << 32) / (MEMBERS / 2) as u64) as u32;
        r.plan = vec![Item { t: 0, what: What::Boundary }];
        u.bodies.put(i, r);
    }
    u.body_cap = u.bodies.len();
    // Equal light distances isolate canonical event keys from the deadline heuristic.
    u.pos = vec![[0.0; 2]; u.bodies.len()];
    u.queue = Some(Calendar::new(u.body_cap));
    (u, ids)
}

fn images(u: &Universe, ids: &[usize], threads: usize) -> Vec<(Tick, usize)> {
    let (_, velocity) = u.ctx().centre(1, 0).unwrap();
    assert_eq!(velocity, [Scalar::ZERO, Scalar::raw(1, -1).unwrap()]);
    let boost = Frame::of(velocity).unwrap().unwrap();
    let ctx = u.ctx();
    std::thread::scope(|scope| {
        let handles: Vec<_> = ids.chunks(ids.len().div_ceil(threads)).map(|chunk| {
            let ctx = &ctx;
            scope.spawn(move || chunk.iter().map(|&i| {
                let b = ctx.bodies.rec(i).b;
                let (position, _) = b.cartesian(0).unwrap();
                // The common integer event lattice is one root light tick.
                // At the coincident clock origins no time-translation or clock
                // integration convention is needed. A spatial translation does
                // not affect the root time at this first slice.
                let x = position[0].fixed(-(b.clock_exp as i32)).unwrap();
                let y = position[1].fixed(-(b.clock_exp as i32)).unwrap();
                let image = boost.inverse([0, x, y]).unwrap();
                assert_eq!(boost.forward(image).unwrap(), [0, x, y]);
                (Tick::try_from(image[0]).unwrap(), i)
            }).collect::<Vec<_>>())
        }).collect();
        handles.into_iter().flat_map(|h| h.join().unwrap()).collect()
    })
}

#[test]
fn p6_first_slice_root_keys_are_the_shear_images() {
    let (mut u, ids) = scene();
    let mut reference = images(&u, &ids, 1);
    reference.sort();
    assert!(reference.first().unwrap().0 < 0 && reference.last().unwrap().0 > 0,
        "a simultaneity test must put events on both sides of the root epoch");
    assert!(reference.windows(2).any(|p| p[0].0 == p[1].0), "actual root-time ties");
    let mut failures = 0;
    for threads in [1, 4, 8] {
        u.threads = threads;
        let expected = images(&u, &ids, threads);
        let wrong = expected.iter().filter(|&&(t, i)| u.key_of(i) != Some((t, i))).count();
        for reverse in [false, true] {
            let mut order = ids.clone();
            if reverse { order.reverse(); }
            for i in order { u.requeue(i); }
            let mut actual = Vec::new();
            while let Some((t, i)) = u.queue.as_ref().unwrap().peek() {
                actual.push((Tick::try_from(t.fixed(0).unwrap()).unwrap(), i));
                u.queue.as_mut().unwrap().set(i, None).unwrap();
            }
            let mut sorted = expected.clone();
            sorted.sort();
            assert_eq!(sorted, reference, "the independent shear images depend on threads");
            let wrong_order = actual.iter().zip(&reference).filter(|(a, b)| a.1 != b.1).count();
            println!("P6 threads={threads} insertion_reverse={reverse} keys_wrong={wrong}/{MEMBERS} order_wrong={wrong_order}/{MEMBERS}");
            failures += wrong + wrong_order;
        }
    }
    assert_eq!(failures, 0, "P6: local ticks are not root-clock images (both insertion orders are only the first-slice probe, not sparse/dense evolution)");
}

#[test]
fn a_centres_exact_rebind_does_not_change_an_events_root_image() {
    let (mut u, _) = scene();
    let at = 1_000_000;
    let centre = u.dolls[1].centre.unwrap();
    let mut rec = u.rec(centre);
    let exact = rec.b.readout(at).unwrap();
    let before = u.ctx().root_tick(1, at, [Scalar::ZERO; 2]).unwrap();
    let fitted = bind(exact, at, rec.b.clock_exp, None, rec.b.entry.unit).unwrap();
    let old = rec.b.clone();
    rec.b = Binding {
        doll: 0, tube: fitted.tube, entry: fitted.entry, residual: fitted.residual,
        turn: fitted.turn, units: fitted.units, clock_exp: old.clock_exp,
        event_time: at, kick: crate::bind::Kick::NONE,
    };
    assert_eq!(rec.b.readout(at).unwrap(), exact, "the physical state did not change");
    u.bodies.retire(centre, Segment { b: old, until: at });
    u.bodies.put(centre, rec);
    let after = u.ctx().root_tick(1, at, [Scalar::ZERO; 2]).unwrap();
    println!("root image before exact centre rebind={before}, after={after}, jump={}", after-before);
    assert_eq!(after, before, "queue keys must not depend on the centre's binding allocation");
}
