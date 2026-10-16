//! Independent fixtures. No engine scenes or lattice world generators are imported.
use emergent_engine::{AnchorPolicy, Battle, Frame, Outcome};
use emergent_lattice::{chronon::Chronon, Body, Kickable, Law, Response, Stepper, World};
use emergent_lattice_event::EventCore;
#[cfg(target_os = "macos")]
use emergent_lattice_metal::MetalChronon;
use std::collections::BTreeMap;

pub const Q: i64 = 1 << 20;
pub const R: i64 = 1000 * (1 << 22);
pub const N: u64 = 1 << 46;
pub fn frame() -> Frame {
    Frame::new(Q, R, N).unwrap()
}
pub fn world(bodies: Vec<Body>, q: i64) -> World {
    World::new(q, None, bodies)
        .unwrap()
        .with_law(Law::RelativisticV1)
        .unwrap()
}
pub struct Rng(pub u64);
impl Rng {
    pub fn next(&mut self) -> u64 {
        self.0 ^= self.0 << 13;
        self.0 ^= self.0 >> 7;
        self.0 ^= self.0 << 17;
        self.0
    }
    pub fn range(&mut self, lo: i64, hi: i64) -> i64 {
        lo + (self.next() % (hi - lo + 1) as u64) as i64
    }
}

/// World requires sorted IDs (there is no insertion API). Different insertion sequences
/// into a BTreeMap are normalized to that public contract, with stable identities.
pub fn contact_scene(seed: u64, kind: usize, permutation: usize) -> World {
    let q = 1024;
    let mut rng = Rng(seed + 0x91e1);
    let mut bodies = Vec::new();
    for i in 0..32 {
        let (x, k, radius) = match kind {
            0 => (
                [(i % 8) * 130 - 450, (i / 8) * 130 - 180],
                [rng.range(-230, 230), rng.range(-230, 230)],
                50,
            ),
            1 => (
                [(i % 8) * 5000 - 18000, (i / 8) * 5000 - 7000],
                [if i % 2 == 0 { 1010 } else { -1010 }, rng.range(-32, 32)],
                150,
            ),
            // Pairs exactly grazing, and one unit inside/outside grazing, at high speed.
            _ => {
                let pair = i / 2;
                (
                    [
                        if i % 2 == 0 { -5000 } else { 5000 },
                        pair * 2500 + if i % 2 == 0 { 0 } else { 400 + pair % 3 - 1 },
                    ],
                    [if i % 2 == 0 { 700 } else { -700 }, 0],
                    200,
                )
            }
        };
        bodies.push(Body::new(
            i as u64 + 1,
            x,
            k,
            rng.range(1, 7),
            radius,
            Response::Bounce,
        ));
    }
    if permutation == 1 {
        bodies.reverse();
    }
    if permutation == 2 {
        for i in (1..bodies.len()).rev() {
            let j = (rng.next() as usize) % (i + 1);
            bodies.swap(i, j);
        }
    }
    let map: BTreeMap<_, _> = bodies.into_iter().map(|b| (b.id, b)).collect();
    world(map.into_values().collect(), q)
}

pub fn trace<S: Kickable>(
    s: S,
    f: Frame,
    threads: usize,
    anchored: bool,
    shift: i64,
) -> (Vec<Outcome>, u64, u64) {
    let mut b = Battle::new(s, f, threads).with_epoch_shift(shift);
    if anchored {
        b = b
            .with_anchoring(AnchorPolicy {
                age_epochs: 4,
                enforce_orbit_rule: false,
            })
            .unwrap();
    }
    let mut out = Vec::new();
    for t in [0, 1, 15, 16, 17, 31, 32, 33, 64, 128] {
        b.run_to(t).unwrap();
        out.push(b.outcome());
    }
    (out, b.stepper().log().contacts, b.stats().changed)
}

pub fn determinism() -> (bool, String) {
    #[cfg(target_os = "macos")]
    let metal_error = MetalChronon::new(contact_scene(1, 0, 0), false)
        .err()
        .map(|e| format!("{e:?}"));
    #[cfg(not(target_os = "macos"))]
    let metal_error: Option<String> = None;
    let metal_available = cfg!(target_os = "macos") && metal_error.is_none();
    let mut comparisons = 0;
    let mut wrong = 0;
    let mut contacts = 0;
    let mut kicks = 0;
    let mut first = String::new();
    for seed in [1, 17, 901, 0xdead] {
        for kind in 0..3 {
            for anchored in [false, true] {
                // Stress law: epoch 16, nT=1/8. Near-c scenes stress refusal as well as contacts.
                let f = Frame::new(1024, 1 << 24, 1 << 50).unwrap();
                let w = contact_scene(seed, kind, 0);
                let base = trace(Chronon::new(w, false).unwrap(), f.clone(), 1, anchored, 0);
                contacts += base.1;
                kicks += base.2;
                for permutation in 0..3 {
                    for threads in [1, 4, 8] {
                        let w = contact_scene(seed, kind, permutation);
                        let c = trace(
                            Chronon::new(w.clone(), false).unwrap(),
                            f.clone(),
                            threads,
                            anchored,
                            0,
                        );
                        let e = trace(
                            EventCore::new(w.clone(), false).unwrap(),
                            f.clone(),
                            threads,
                            anchored,
                            0,
                        );
                        #[allow(unused_mut)]
                        let mut orders = vec![("lockstep", c.0), ("sparse", e.0)];
                        #[cfg(target_os = "macos")]
                        if metal_available {
                            let m = trace(
                                MetalChronon::new(w, false).unwrap(),
                                f.clone(),
                                threads,
                                anchored,
                                0,
                            );
                            orders.push(("metal", m.0));
                        }
                        for (order, out) in orders {
                            for (i, (got, want)) in out.iter().zip(&base.0).enumerate() {
                                comparisons += 1;
                                if got != want {
                                    wrong += 1;
                                    if first.is_empty() {
                                        first=format!("seed={seed} kind={kind} anchor={anchored} insertion={permutation} threads={threads} order={order} sample={i}");
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    // Flat reduction against the bare steppers, rather than merely equality of two Battles.
    let w = contact_scene(41, 0, 0);
    let mut c = Chronon::new(w.clone(), false).unwrap();
    c.run_to(128);
    let mut e = EventCore::new(w.clone(), false).unwrap();
    e.run_to(128);
    let mut b = Battle::new(
        Chronon::new(w.clone(), false).unwrap(),
        Frame::flat(1024).unwrap(),
        1,
    );
    b.run_to(128).unwrap();
    let o = b.outcome();
    #[allow(unused_mut)]
    let mut flat = (o.world, o.log) == c.outcome() && c.outcome() == e.outcome();
    #[cfg(target_os = "macos")]
    if metal_available {
        let mut m = MetalChronon::new(w.clone(), false).unwrap();
        m.run_to(128);
        let mut b = Battle::new(
            MetalChronon::new(w, false).unwrap(),
            Frame::flat(1024).unwrap(),
            1,
        );
        b.run_to(128).unwrap();
        let o = b.outcome();
        flat &= (o.world, o.log) == m.outcome() && m.outcome() == c.outcome();
    }
    let expected = if cfg!(target_os = "macos") {
        6480
    } else {
        4320
    };
    let unsupported = if metal_error.is_some() {
        "UNSUPPORTED "
    } else {
        ""
    };
    (wrong==0 && comparisons==expected && contacts>0 && kicks>0 && flat,
     format!("{unsupported}equal={}/{comparisons} checked={comparisons}/{expected} scenes=24 seeds=4 insertion=3 threads=1,4,8 metal={metal_available} metal_unavailable={metal_error:?} contacts={contacts} kicks={kicks} flat={flat} first={first:?}",comparisons-wrong))
}
