//! Deterministic multi-island scenes (containerless) for invariance tests and the frame
//! harness. Each scene is a list of worlds with disjoint ids: a scene may start as several
//! worlds, and [`union`] is the single world the reference stepper runs.
use emergent_lattice::law::{Body, Law, Response, World};
use emergent_lattice::worlds;

/// Bodies of `w` shifted by `offset` units (× Q), velocities scaled by num/den then offset by
/// `drift` (1/Q per chronon), ids renumbered from `first_id`. Whole bodies are copied, so
/// fields the contract adds later ride along.
pub fn place(w: &World, first_id: u64, offset: [i64; 2], num: i64, den: i64, drift: [i64; 2]) -> Vec<Body> {
    w.bodies
        .iter()
        .enumerate()
        .map(|(i, b)| Body {
            id: first_id + i as u64,
            x: [b.x[0] + offset[0] * w.q, b.x[1] + offset[1] * w.q],
            k: [b.k[0] * num / den + drift[0], b.k[1] * num / den + drift[1]],
            ..b.clone()
        })
        .collect()
}

/// A genesis world from placed bodies (ranges and c = 1 checked).
pub fn world(template: &World, bodies: Vec<Body>) -> World {
    let mut w = World { bodies, container: None, consumed: vec![], wall_momentum: [0, 0], ..template.clone() };
    w.bodies.sort_unstable_by_key(|b| b.id);
    w.validate().expect("placed bodies within the law's ranges");
    w.check_speed_limit().expect("placed bodies respect c at genesis");
    w
}

/// Union of worlds at one tick: bodies by id, consumed contacts, summed ledgers.
pub fn union(ws: &[World]) -> World {
    let mut bodies: Vec<Body> = ws.iter().flat_map(|w| w.bodies.iter().cloned()).collect();
    bodies.sort_unstable_by_key(|b| b.id);
    let mut consumed: Vec<_> = ws.iter().flat_map(|w| w.consumed.iter().copied()).collect();
    consumed.sort_unstable();
    let wall = ws.iter().fold([0i64; 2], |a, w| [a[0] + w.wall_momentum[0], a[1] + w.wall_momentum[1]]);
    World { bodies, consumed, wall_momentum: wall, ..ws[0].clone() }
}

/// [`worlds::mixed`] without its container: masses 1–4, radii Q/2–2Q, Pass/Stop/Bounce.
pub fn loose_mixed(n: u64, q: i64, seed: u64) -> World {
    World { container: None, ..worlds::mixed(n, q, seed) }
}

/// Four islands: two Pass-disc clusters approaching head-on (they must merge), a loose mixed
/// cluster and a bouncing-disc cluster.
pub fn islands(q: i64, seed: u64) -> Vec<World> {
    let a = worlds::random(60, 300, q, 1, seed, Response::Pass);
    let b = worlds::random(60, 300, q, 1, seed + 1, Response::Pass);
    let c = loose_mixed(40, q, seed + 2);
    let d = worlds::random(50, 300, q, 1, seed + 3, Response::Bounce);
    vec![
        world(&a, place(&a, 1, [0, 0], 1, 1, [q / 8, 0])),
        world(&b, place(&b, 1001, [500, 0], 1, 1, [-q / 8, 0])),
        world(&c, place(&c, 2001, [0, 700], 1, 1, [0, 0])),
        world(&d, place(&d, 3001, [700, 700], 1, 1, [0, 0])),
    ]
}

/// A bouncing cluster and a Pass cluster that start interpenetrated and fly apart: one
/// region that must split once they separate.
pub fn diverging(q: i64, seed: u64) -> Vec<World> {
    let a = worlds::random(80, 300, q, 1, seed, Response::Bounce);
    let b = worlds::random(80, 300, q, 1, seed + 1, Response::Pass);
    vec![world(&a, place(&a, 1, [0, 0], 1, 4, [-q / 2, 0])), world(&b, place(&b, 1001, [0, 0], 1, 4, [q / 2, 0]))]
}

/// A grid of `rows × cols` clusters `spacing` units apart, `per` bodies each, cycling through
/// Pass discs, bouncing discs and loose mixed clusters, internal velocities divided by `den`;
/// the first two drift toward each other at Q/8 each.
pub fn galaxy(q: i64, rows: i64, cols: i64, per: u64, spacing: i64, den: i64, seed: u64) -> Vec<World> {
    let mut out = Vec::new();
    for i in 0..rows * cols {
        let s = seed + 7 * i as u64;
        let w = match i % 3 {
            0 => worlds::random(per, 300, q, 1, s, Response::Pass),
            1 => worlds::random(per, 300, q, 1, s, Response::Bounce),
            _ => loose_mixed(per, q, s),
        };
        let drift = match i {
            0 => [q / 8, 0],
            1 => [-q / 8, 0],
            _ => [0, 0],
        };
        let off = [(i % cols) * spacing, (i / cols) * spacing];
        out.push(world(&w, place(&w, 1 + 100_000 * i as u64, off, 1, den, drift)));
    }
    out
}

/// The same scene under another law (genesis rules re-checked: relativistic needs |k| < c).
pub fn with_law(ws: Vec<World>, law: Law) -> Vec<World> {
    ws.into_iter().map(|w| w.with_law(law).expect("scene valid under the law")).collect()
}

/// A dense gas cluster without its container ([`worlds::gas`] bodies), offset by `offset` units.
pub fn loose_gas(n: u64, q: i64, vmax_units: i64, seed: u64, first_id: u64, offset: [i64; 2]) -> World {
    let g = World { container: None, ..worlds::gas(n, 0.3, q, vmax_units, seed) };
    world(&g, place(&g, first_id, offset, 1, 1, [0, 0]))
}

/// Heavy-tailed scene: one dense gas region of `gas_n` bodies at the origin and a
/// `rows × cols` grid of small sparse islands (`per` bodies, alternating bouncing and Pass
/// discs) `spacing` units apart, starting `gap` units to the east. Returns the worlds and a
/// point in the middle of the islands (where the player looks).
pub fn heavy_tail(q: i64, gas_n: u64, rows: i64, cols: i64, per: u64, spacing: i64, gap: i64, seed: u64) -> (Vec<World>, [i64; 2]) {
    let mut out = vec![loose_gas(gas_n, q, q / 4, seed, 1, [0, 0])];
    for i in 0..rows * cols {
        let response = if i % 2 == 0 { Response::Bounce } else { Response::Pass };
        let w = worlds::random(per, 300, q, 1, seed + 1 + i as u64, response);
        let off = [gap + (i % cols) * spacing, (i / cols) * spacing];
        out.push(world(&w, place(&w, 1_000_000 + 1000 * i as u64, off, 1, 1, [0, 0])));
    }
    let observer = [(gap + (cols - 1) * spacing / 2) * q, ((rows - 1) * spacing / 2) * q];
    (out, observer)
}
