//! Seeded scenes for the frame's tests and cost probes. Deterministic integers only.
use emergent_lattice::law::{Body, Law, Response, World};
use emergent_lattice::worlds::Rng;

/// A battle in the frame of its centre of mass (no walls): two fleets, each a jittered grid
/// of `n/2` bodies (masses 1 to 4, radii q/2 to q, 80% bouncers, 10% pass, 10% stop), closing
/// at 2q/`speed_div` per chronon from a gap of 40 light-chronons, with a random sideways
/// offset so they meet off-axis. Genesis has no overlapping pair. With `formation` every
/// body of a fleet shares one velocity (the event core forms a velocity class per fleet);
/// otherwise velocities scatter by ±q/(4·`speed_div`) per axis. Law
/// `es-lattice-relativistic-v1`. Bodies are numbered from 1 in fleet order; the scene's
/// extent is returned with it (the largest |x| component at genesis, in lattice units).
pub fn battle(n: u64, q: i64, seed: u64, speed_div: i64, formation: bool) -> (World, i64) {
    assert!(n >= 4, "a battle needs two fleets");
    let mut rng = Rng(seed ^ (n << 16) ^ 0x00BA_771E);
    let spacing = 5 * q;
    let gap = 40 * q;
    let mut bodies: Vec<Body> = Vec::with_capacity(n as usize);
    let mut extent = 0i64;
    let sizes = [n / 2, n - n / 2];
    let per_row: Vec<i64> = sizes.iter().map(|&s| (s as f64).sqrt().ceil() as i64).collect();
    let offset = rng.range(-per_row[0] * spacing / 2, per_row[0] * spacing / 2);
    for (f, &size) in sizes.iter().enumerate() {
        let side = per_row[f] * spacing;
        // Fleet 0 left of the origin moving right; fleet 1 right of it moving left.
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
    let w = World::new(q, None, bodies).expect("battle within the law's ranges").with_law(Law::RelativisticV1).expect("subluminal");
    (w, extent)
}

/// One bouncer of radius q/2 and mass 1 at `x` with velocity `k`, under `es-lattice-relativistic-v1`.
pub fn lone(q: i64, x: [i64; 2], k: [i64; 2]) -> World {
    World::new(q, None, vec![Body::new(1, x, k, 1, q / 2, Response::Bounce)]).expect("one body").with_law(Law::RelativisticV1).expect("subluminal")
}
