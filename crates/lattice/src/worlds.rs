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

/// sin and cos from IEEE +, ×, ÷ only (Taylor to x^25 after reduction to [−π, π]), so
/// genesis is bit-identical on every IEEE machine; platform `sin`/`cos` are not.
fn sin_cos(x: f64) -> (f64, f64) {
    const PI: f64 = std::f64::consts::PI;
    let x = x - (2.0 * PI) * ((x + PI) / (2.0 * PI)).floor();
    let (mut s, mut c, mut ts, mut tc) = (0.0, 0.0, x, 1.0);
    for n in 0..13 {
        s += ts;
        c += tc;
        let (a, b) = ((2 * n + 2) as f64, (2 * n + 3) as f64);
        ts *= -x * x / (a * b);
        tc *= -x * x / ((2 * n + 1) as f64 * a);
    }
    (s, c)
}

/// Galaxy-shaped scene (ladder v7 G1/G2): `clusters` fleets on two spiral arms over a disc of
/// radius 2^`span_bits` light-chronons, plus a stream of 256 ships at 0.9c aimed at the
/// largest fleet (when n ≥ 4096). No gravity: fleets coast. Cluster sizes follow Zipf (the
/// r-th largest holds a share ∝ 1/r, at least 16 ships); each fleet is a jittered grid of
/// unit-mass bouncers of radius one light-chronon at about 10% fill, with a bulk drift up
/// to Q/4 per axis and a dispersion up to Q/16. Fleets never overlap at genesis. Positions
/// must fit the law's range: Err when the disc does not (wide origins are future work).
pub fn galaxy(n: u64, clusters: u64, span_bits: u32, q: i64, seed: u64) -> Result<World, crate::law::LawError> {
    let mut rng = Rng(seed ^ n ^ (clusters << 20) ^ ((span_bits as u64) << 40) ^ 0x6A1A);
    let u = |r: &mut Rng| (r.next() >> 11) as f64 / (1u64 << 53) as f64;
    let stream = if n >= 4096 { 256 } else { 0 };
    let fleet = n - stream;
    let c = clusters.clamp(1, fleet / 16) as usize;
    let h: f64 = (1..=c).map(|r| 1.0 / r as f64).sum();
    let mut sizes: Vec<u64> = (1..=c).map(|r| ((fleet as f64 / (r as f64 * h)) as u64).max(16)).collect();
    let rest = fleet as i64 - sizes.iter().sum::<u64>() as i64;
    sizes[0] = (sizes[0] as i64 + rest).max(16) as u64;
    let (spacing, radius) = (6 * q, q);
    let disc = (1u64 << span_bits) as f64;
    let mut boxes: Vec<([i64; 2], i64)> = Vec::with_capacity(c);
    let mut bodies: Vec<Body> = Vec::with_capacity(n as usize);
    let mut id = 1u64;
    for (i, &size) in sizes.iter().enumerate() {
        let per_row = (size as f64).sqrt().ceil() as i64;
        let half = per_row * spacing / 2 + 2 * spacing;
        let mut centre = None;
        for _ in 0..10_000 {
            let f = 0.05 + 0.9 * u(&mut rng);
            let th = (i % 2) as f64 * std::f64::consts::PI + 3.0 * std::f64::consts::PI * f.sqrt() + 0.3 * (u(&mut rng) - 0.5);
            let (s, co) = sin_cos(th);
            let p = [(disc * f * co) as i64 * q, (disc * f * s) as i64 * q];
            if boxes.iter().all(|(b, bh)| (p[0] - b[0]).abs() > half + bh || (p[1] - b[1]).abs() > half + bh) {
                centre = Some(p);
                break;
            }
        }
        let p = centre.ok_or_else(|| crate::law::LawError(format!("{c} fleets do not fit a disc of 2^{span_bits} light-chronons")))?;
        boxes.push((p, half));
        let drift = [rng.range(-q / 4, q / 4), rng.range(-q / 4, q / 4)];
        let origin = [p[0] - per_row * spacing / 2, p[1] - per_row * spacing / 2];
        for j in 0..size as i64 {
            let x = [origin[0] + (j % per_row) * spacing + rng.range(-q, q), origin[1] + (j / per_row) * spacing + rng.range(-q, q)];
            let k = [drift[0] + rng.range(-q / 16, q / 16), drift[1] + rng.range(-q / 16, q / 16)];
            bodies.push(body(id, x, k, 1, radius, Response::Bounce));
            id += 1;
        }
    }
    if stream > 0 {
        let (p, half) = boxes[0];
        let start = [p[0] - half - 600 * q - 16 * spacing, p[1] - 8 * spacing];
        for j in 0..stream as i64 {
            let x = [start[0] + (j % 16) * spacing, start[1] + (j / 16) * spacing];
            bodies.push(body(id, x, [9 * q / 10, 0], 1, radius, Response::Bounce));
            id += 1;
        }
    }
    World::new(q, None, bodies)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sin_cos_matches_the_platform_to_rounding() {
        for i in -2000..=2000 {
            let x = i as f64 * 0.01;
            let (s, c) = sin_cos(x);
            assert!((s - x.sin()).abs() < 1e-13 && (c - x.cos()).abs() < 1e-13, "x {x}");
        }
    }

    #[test]
    fn galaxy_is_deterministic_exact_in_size_and_overlap_free() {
        for (n, c, span) in [(4096u64, 16u64, 12u32), (20000, 64, 30), (1000, 8, 20)] {
            let w = galaxy(n, c, span, 256, 7).unwrap();
            assert_eq!(w.bodies.len() as u64, n);
            assert_eq!(w, galaxy(n, c, span, 256, 7).unwrap(), "deterministic");
            assert!(w.bodies.iter().all(|b| (b.k[0] as i128).pow(2) + (b.k[1] as i128).pow(2) < 256 * 256));
            // No two bodies within contact reach (2 radii) at genesis.
            let cell = 4 * 256;
            let mut grid: HashMap<(i64, i64), Vec<[i64; 2]>> = HashMap::new();
            for b in &w.bodies {
                let key = (b.x[0].div_euclid(cell), b.x[1].div_euclid(cell));
                for dx in -1..=1 {
                    for dy in -1..=1 {
                        for p in grid.get(&(key.0 + dx, key.1 + dy)).into_iter().flatten() {
                            let d = [(p[0] - b.x[0]) as i128, (p[1] - b.x[1]) as i128];
                            assert!(d[0] * d[0] + d[1] * d[1] > (2 * 256i128).pow(2), "genesis overlap");
                        }
                    }
                }
                grid.entry(key).or_default().push(b.x);
            }
        }
        assert!(galaxy(65536, 64, 45, 256, 7).is_err(), "past the coordinate range");
    }
}
