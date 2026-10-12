//! Red-team 20261012-0138: premise 4 (both orders, identical bits) at relativistic speed
//! heterogeneity — the identity ladder's scenes all move at fleet speed (β ≤ ~0.18, one
//! speed class). The player's headline action is a relativistic body crossing a battle.
//! Scene: the shipped s1 battle (100 bodies, q = 1024, seed 2, div 8, same rng draw order)
//! plus interceptors appended after the fleet draws. Controls: the epoch-shift plant (the
//! instrument detects differences), asserted per variant.
use emergent_engine::{Battle, Frame, Outcome};
use emergent_lattice::chronon::Chronon;
use emergent_lattice::law::{Body, Law, Response, Tick, World};
use emergent_lattice::worlds::Rng;
use emergent_lattice_event::EventCore;
use emergent_lattice::Stepper;
use std::time::Instant;

const HORIZON: Tick = 4096;

/// scenes::battle with the fleet draws identical (n = 100, q = 1024, seed 2, div 8), then
/// interceptors appended after the fleet draws, so the fleet layout is the ladder's s1.
fn battle_with(interceptors: Vec<([i64; 2], [i64; 2])>) -> (World, i64) {
    let (n, q, seed, speed_div, formation) = (100u64, 1024i64, 2u64, 8i64, false);
    let mut rng = Rng(seed ^ (n << 16) ^ 0x00BA_771E);
    let spacing = 5 * q;
    let gap = 40 * q;
    let mut bodies: Vec<Body> = Vec::with_capacity(n as usize + interceptors.len());
    let mut extent = 0i64;
    let sizes = [n / 2, n - n / 2];
    let per_row: Vec<i64> = sizes.iter().map(|&s| (s as f64).sqrt().ceil() as i64).collect();
    let offset = rng.range(-per_row[0] * spacing / 2, per_row[0] * spacing / 2);
    for (f, &size) in sizes.iter().enumerate() {
        let side = per_row[f] * spacing;
        let v = q / speed_div;
        let (x0, vx, y_off) = if f == 0 { (-(gap / 2) - side, v, 0) } else { (gap / 2, -v, offset) };
        let scatter = if formation { 0 } else { (v / 4).max(1) };
        let y0 = y_off - side / 2;
        for j in 0..size as i64 {
            let radius = rng.range(q / 2, q);
            let x = [x0 + (j % per_row[f]) * spacing + rng.range(-q / 2, q / 2), y0 + (j / per_row[f]) * spacing + rng.range(-q / 2, q / 2)];
            let k = [vx + rng.range(-scatter, scatter), rng.range(-scatter, scatter)];
            let response = match rng.next() % 10 {
                0 => Response::Pass,
                1 => Response::Stop,
                _ => Response::Bounce,
            };
            extent = extent.max(x[0].abs()).max(x[1].abs());
            bodies.push(Body::new(bodies.len() as u64 + 1, x, k, rng.range(1, 4), radius, response));
        }
    }
    // Interceptors: mass 1, radius q/2, bouncers. A +900-speed body from x = -432000
    // arrives at the engagement zone (x = 0) at t = 480, mid-battle.
    for (x, k) in interceptors {
        extent = extent.max(x[0].abs()).max(x[1].abs());
        bodies.push(Body::new(bodies.len() as u64 + 1, x, k, 1, q / 2, Response::Bounce));
    }
    let w = World::new(q, None, bodies).expect("battle within the law's ranges").with_law(Law::RelativisticV1).expect("subluminal");
    (w, extent)
}

/// The battle's random row offset, recomputed with the same first rng draw as `battle_with`.
fn row_offset() -> i64 {
    let (n, q, seed) = (100u64, 1024i64, 2u64);
    let mut rng = Rng(seed ^ (n << 16) ^ 0x00BA_771E);
    let spacing = 5 * q;
    let per_row: Vec<i64> = [n / 2, n - n / 2].iter().map(|&s| (s as f64).sqrt().ceil() as i64).collect();
    rng.range(-per_row[0] * spacing / 2, per_row[0] * spacing / 2)
}

fn frame(q: i64, extent: i64, k: u32) -> Frame {
    let r_orbit = (q << k) / 4;
    let r_extent = 32 * (extent + 4 * HORIZON * (q / 8));
    Frame::new(q, r_orbit.max(r_extent), 1u64 << (60 - k)).unwrap()
}

struct Run {
    out: Outcome,
    contacts: u64,
    secs: f64,
    rebuilds: u64,
    epochs: u64,
}

fn lockstep(w: &World, f: &Frame, shift: Tick) -> Run {
    let t = Instant::now();
    let mut b = Battle::new(Chronon::new(w.clone(), false).unwrap(), f.clone(), 1).with_epoch_shift(shift);
    b.run_to(HORIZON).unwrap();
    Run { out: b.outcome(), contacts: b.stepper().log().contacts, secs: t.elapsed().as_secs_f64(), rebuilds: 0, epochs: b.stats().epochs }
}

fn sparse(w: &World, f: &Frame, shift: Tick) -> Run {
    let t = Instant::now();
    let mut b = Battle::new(EventCore::new(w.clone(), false).unwrap(), f.clone(), 1).with_epoch_shift(shift);
    b.run_to(HORIZON).unwrap();
    Run { out: b.outcome(), contacts: b.stepper().log().contacts, secs: t.elapsed().as_secs_f64(), rebuilds: b.stepper().rebuilds(), epochs: b.stats().epochs }
}

fn variant(name: &str, interceptors: Vec<([i64; 2], [i64; 2])>) {
    let (w, extent) = battle_with(interceptors);
    let f = frame(1024, extent, 15);
    let a = lockstep(&w, &f, 0);
    let b = sparse(&w, &f, 0);

    let (lk_secs, sp_secs) = (a.secs, b.secs);
    println!(
        "{name:<26} contacts {} epochs {} | lk {lk_secs:.2}s sp {sp_secs:.2}s ({} rebuilds) | digest {}",
        a.contacts, a.epochs, b.rebuilds, &a.out.world[..12]
    );
    assert!(a.contacts > 0, "{name}: the battle must happen");
    assert_eq!(a.contacts, b.contacts, "{name}: contact counts");
    assert_eq!(a.out, b.out, "{name}: lockstep and sparse digests");

    // Negative control (the instrument can see a difference): one chronon of epoch shift.
    let late_sparse = sparse(&w, &f, 1);
    let late_lockstep = lockstep(&w, &f, 1);
    assert_ne!(late_sparse.out, b.out, "{name}: shifted sparse must differ");
    assert_eq!(late_sparse.out, late_lockstep.out, "{name}: shifted in both orders, they agree");
}

#[test]
fn relativistic_flyby_through_a_battle() {
    let offset = row_offset();
    println!("row offset (y of a fleet row): {offset}");
    // v0 control: the plain s1 battle (must agree, as the ladder shows).
    variant("v0 no interceptor", vec![]);
    // v1: one interceptor at β = 0.88 (k = [900, 0]) along a fleet row.
    variant("v1 one at 0.88c", vec!(([-432000, offset], [900, 0])));
    // v2: diagonal at β = 0.74 (k = [720, 240]), aimed to cross the row at t = 480.
    variant("v2 one at 0.74c diagonal", vec!(([-432000, offset - 240 * 480], [720, 240])));
    // v3: two opposing interceptors on the same row: a guaranteed near-c pair contact at
    // x = 0, t = 480, each having crossed half the battle.
    variant("v3 two opposing 0.88c", vec!(([-432000, offset], [900, 0]), ([432000, offset], [-900, 0])));
}
