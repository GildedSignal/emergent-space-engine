//! Deterministic worlds. `gas`, `random` and `packed` reproduce the ladder's generators
//! (xtask/src/gas.rs, xtask/src/ladder.rs) exactly, with positions scaled by Q.
use crate::law::{Body, Container, Response, World};
use std::collections::HashMap;

/// SplitMix64, as in the ladder.
pub struct Rng(pub u64);

impl Rng {
    pub fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }

    /// Uniform integer in [lo, hi].
    pub fn range(&mut self, lo: i64, hi: i64) -> i64 {
        lo + (self.next() as u128 % (hi - lo + 1) as u128) as i64
    }
}

fn body(id: u64, x: [i64; 2], k: [i64; 2], mass: i64, radius: i64, response: Response) -> Body {
    Body::new(id, x, k, mass, radius, response)
}

/// Trapped gas (ladder C2/X5): n unit-mass bouncers of radius 1 on a jittered grid in a
/// square box at packing fraction `fill`, velocity components in [-vmax, vmax]/Q.
pub fn gas(n: u64, fill: f64, q: i64, vmax_units: i64, seed: u64) -> World {
    let radius = 1i64;
    let side = ((n as f64 * std::f64::consts::PI / fill).sqrt()).ceil() as i64;
    let per_row = (n as f64).sqrt().ceil() as i64;
    let cell = side / per_row;
    let mut rng = Rng(seed ^ n ^ 0x6A5);
    let jitter = ((cell - 2 * radius - 1) / 2).clamp(0, 1);
    let bodies = (0..n as i64)
        .map(|i| {
            let p = [
                (i % per_row) * cell + cell / 2 + rng.range(-jitter, jitter),
                (i / per_row) * cell + cell / 2 + rng.range(-jitter, jitter),
            ];
            let v = [rng.range(-vmax_units, vmax_units), rng.range(-vmax_units, vmax_units)];
            body(i as u64 + 1, [p[0] * q, p[1] * q], v, 1, radius * q, Response::Bounce)
        })
        .collect();
    let container = Container { min: [0, 0], max: [side * q, side * q] };
    World::new(q, Some(container), bodies).expect("gas world within the law's ranges")
}

/// Independent discs (ladder X1/X2): uniform positions in a square of `area_per_body`
/// per body, velocity components in [-Q/2, Q/2], genesis separations over 2·reach.
pub fn random(n: u64, area_per_body: i64, q: i64, radius: i64, seed: u64, response: Response) -> World {
    let reach = 2 * radius;
    let side = ((n as f64 * area_per_body as f64).sqrt()).ceil() as i64;
    let mut rng = Rng(seed ^ n);
    let mut out: Vec<([i64; 2], [i64; 2])> = Vec::with_capacity(n as usize);
    let cell = 4 * reach;
    let mut occupied: HashMap<(i64, i64), Vec<usize>> = HashMap::new();
    while out.len() < n as usize {
        let p = [rng.range(0, side), rng.range(0, side)];
        let v = [rng.range(-q / 2, q / 2), rng.range(-q / 2, q / 2)];
        let key = (p[0].div_euclid(cell), p[1].div_euclid(cell));
        let clash = (-1..=1).any(|dx| {
            (-1..=1).any(|dy| {
                occupied.get(&(key.0 + dx, key.1 + dy)).is_some_and(|v| {
                    v.iter().any(|&k| {
                        let o = out[k].0;
                        let (x, y) = (o[0] - p[0], o[1] - p[1]);
                        x * x + y * y <= (2 * reach) * (2 * reach)
                    })
                })
            })
        });
        if !clash {
            occupied.entry(key).or_default().push(out.len());
            out.push((p, v));
        }
    }
    let bodies = out
        .into_iter()
        .enumerate()
        .map(|(i, (p, v))| body(i as u64 + 1, [p[0] * q, p[1] * q], v, 1, radius * q, response))
        .collect();
    World::new(q, None, bodies).expect("random world within the law's ranges")
}

/// Packed grid (ladder C1): spacing `grid`, jitter ±`jitter`, velocity components in
/// [-Q/2, Q/2], every body stops on contact.
pub fn packed(n: u64, grid: i64, jitter: i64, q: i64, radius: i64, seed: u64) -> World {
    let side = (n as f64).sqrt().ceil() as i64;
    let mut rng = Rng(seed ^ n ^ 0xC1);
    let bodies = (0..n as i64)
        .map(|i| {
            let p = [(i % side) * grid + rng.range(-jitter, jitter), (i / side) * grid + rng.range(-jitter, jitter)];
            let v = [rng.range(-q / 2, q / 2), rng.range(-q / 2, q / 2)];
            body(i as u64 + 1, [p[0] * q, p[1] * q], v, 1, radius * q, Response::Stop)
        })
        .collect();
    World::new(q, None, bodies).expect("packed world within the law's ranges")
}

/// Adversarial mix for invariance tests: masses 1..=4, radii Q/2..=2Q, mostly bouncers
/// with some Pass and Stop bodies, dense, in a box; speeds up to Q/2 per component.
pub fn mixed(n: u64, q: i64, seed: u64) -> World {
    let mut rng = Rng(seed ^ n ^ 0x5EED);
    let side_units = ((n as f64) * 40.0).sqrt().ceil() as i64 + 8;
    let per_row = (n as f64).sqrt().ceil() as i64;
    let cell = side_units * q / per_row;
    let bodies = (0..n as i64)
        .map(|i| {
            let radius = rng.range(q / 2, (2 * q).min(cell / 2 - 1).max(q / 2));
            let slack = (cell / 2 - radius).max(0);
            let x = [
                (i % per_row) * cell + cell / 2 + rng.range(-slack, slack),
                (i / per_row) * cell + cell / 2 + rng.range(-slack, slack),
            ];
            let k = [rng.range(-q / 2, q / 2), rng.range(-q / 2, q / 2)];
            let response = match rng.next() % 10 {
                0 => Response::Pass,
                1 => Response::Stop,
                _ => Response::Bounce,
            };
            body(i as u64 + 1, x, k, rng.range(1, 4), radius, response)
        })
        .collect();
    let container = Container { min: [0, 0], max: [side_units * q, side_units * q] };
    World::new(q, Some(container), bodies).expect("mixed world within the law's ranges")
}
