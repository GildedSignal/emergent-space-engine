//! Flight-v0: integer proper-time burn events over the unchanged lattice-v1 law.
//! A held engine supplies Δrapidity = 1/128 every 1/64 proper second (a = c/2 s).
//! Between these impulses the exact sparse lattice engine owns motion and contacts.
//! Q32 rest-frame four-velocity carries thrust rounding across impulses; contact resets
//! it to the law's outgoing velocity. Clock length uses an integer Q32 square root.
use emergent_lattice::{Body, Kickable, Law, Response, Stepper, World};
use emergent_lattice_event::EventCore;
use serde::{Deserialize, Serialize};

pub const Q: i64 = 65536;
pub const TPS: i64 = 4096;
const F: i128 = 1 << 32;
const BURN_TAU: i128 = (TPS as i128 / 64) * F;
pub const FORWARD: u8 = 1;
pub const REVERSE: u8 = 2;
pub const LEFT: u8 = 4;
pub const RIGHT: u8 = 8;

#[derive(Clone, Copy, Debug, Serialize, Deserialize, PartialEq, Eq)]
pub struct Input {
    pub tick: i64,
    pub keys: u8,
}

/// A generator, not a list of positions. The first segment has inertial prehistory;
/// every subsequent segment starts at the actual committed velocity change.
#[derive(Clone, Copy, Debug)]
pub struct Segment {
    pub tick: i64,
    pub x: [i64; 2],
    pub k: [i64; 2],
}

#[derive(Clone, Copy)]
pub struct Material {
    pub temperature: f64,
    pub luminosity: f64,
    pub radius: i64,
    pub kind: u8, // visual material only; all bodies obey the same contact law
}

pub struct Flight {
    pub core: EventCore,
    pub history: Vec<Vec<Segment>>,
    pub materials: Vec<Material>,
    pub inputs: Vec<Input>,
    pub heading: u8,
    pub keys: u8,
    pub seed: u64,
    proper: i128, // proper chronons, Q32; integer accumulation is partition invariant
    clock_tick: i64,
    clock_rate: i128, // derived once per player velocity event, never per scheduler step
    deadline: Option<i128>,
    drive: [i128; 2], // gamma beta, Q32
    contact_count: u64,
    pub burns: u64,
}

fn rate(k: [i64; 2]) -> i128 {
    let s = Q as i128 * Q as i128 - k[0] as i128 * k[0] as i128 - k[1] as i128 * k[1] as i128;
    ((s as u128 * (F * F) as u128).isqrt() / Q as u128) as i128
}

fn four(k: [i64; 2]) -> [i128; 2] {
    let r = rate(k);
    k.map(|v| v as i128 * F * F / (Q as i128 * r))
}

/// Integer CORDIC: heading 0 = +x; a full turn is 256. Constants are rounded
/// atan(2^-i) in binary turns (2^32 per revolution); no runtime float decides a turn.
fn direction(heading: u8) -> [i128; 2] {
    const ATAN: [i64; 24] = [
        536870912, 316933406, 167458907, 85004756, 42667331, 21354465, 10679838, 5340245, 2670163,
        1335087, 667544, 333772, 166886, 83443, 41722, 20861, 10430, 5215, 2608, 1304, 652, 326,
        163, 81,
    ];
    let mut z = (heading as i64) << 24;
    if z > 1 << 31 {
        z -= 1 << 32;
    }
    let mut sign = 1;
    if z > 1 << 30 {
        z -= 1 << 31;
        sign = -1;
    }
    if z < -(1 << 30) {
        z += 1 << 31;
        sign = -1;
    }
    let (mut x, mut y) = (2608131496i64, 0i64); // inverse CORDIC gain, Q32
    for (i, a) in ATAN.iter().enumerate() {
        let d = if z >= 0 { 1 } else { -1 };
        (x, y, z) = (x - d * (y >> i), y + d * (x >> i), z - d * a);
    }
    [sign * x as i128, sign * y as i128]
}

/// Boost in the ship's instantaneous rest frame. e(n) = (u·n, n +
/// u(u·n)/(gamma+1)); U' = cosh(dη) U + sinh(dη) e(n).
fn boost(u: [i128; 2], heading: u8, sign: i128) -> [i128; 2] {
    let n = direction(heading);
    let g = ((F * F + u[0] * u[0] + u[1] * u[1]) as u128).isqrt() as i128;
    let dot = (u[0] * n[0] + u[1] * n[1]) / F;
    let eta = F / 128;
    let eta2 = eta * eta / F;
    let ch = F + eta2 / 2 + eta2 * eta2 / F / 24;
    let sh = sign * (eta + eta * eta2 / F / 6 + eta * eta2 / F * eta2 / F / 120);
    std::array::from_fn(|i| ch * u[i] / F + sh * (n[i] + u[i] * dot / (g + F)) / F)
}

fn lattice_velocity(u: [i128; 2]) -> [i64; 2] {
    let g = ((F * F + u[0] * u[0] + u[1] * u[1]) as u128).isqrt() as i128;
    u.map(|v| (v * Q as i128 / g) as i64) // truncation is strictly inside c
}

impl Flight {
    pub fn new(seed: u64) -> Self {
        let mut rng = seed;
        let mut rand = || {
            rng = rng.wrapping_add(0x9e3779b97f4a7c15);
            let mut z = rng;
            z = (z ^ (z >> 30)).wrapping_mul(0xbf58476d1ce4e5b9);
            z = (z ^ (z >> 27)).wrapping_mul(0x94d049bb133111eb);
            z ^ (z >> 31)
        };
        let unit = Q * TPS; // one light-second
        let mut bodies = vec![Body::new(
            1,
            [0, 0],
            [0, 0],
            8,
            unit / 200,
            Response::Bounce,
        )];
        let mut materials = vec![Material {
            temperature: 4000.,
            luminosity: 0.,
            radius: unit / 200,
            kind: 2,
        }];
        for i in 0..320 {
            let star = i < 48;
            let traffic = i >= 318;
            let spread = if star { 64 } else { 12 };
            let x = std::array::from_fn(|_| {
                ((rand() % (spread * 2 * unit as u64)) as i64) - spread as i64 * unit
            });
            let k = if star {
                [0, 0]
            } else {
                std::array::from_fn(|_| (rand() % (Q as u64 / 8)) as i64 - Q / 16)
            };
            let radius = if star {
                unit / 50
            } else if traffic {
                unit / 100
            } else {
                unit / 300 + (rand() % (unit as u64 / 300)) as i64
            };
            bodies.push(Body::new(
                i + 2,
                x,
                k,
                if star { 128 } else { 4 },
                radius,
                Response::Bounce,
            ));
            materials.push(Material {
                temperature: if star {
                    3000. + (rand() % 7000) as f64
                } else {
                    3500.
                },
                luminosity: if star {
                    0.7 + (rand() % 300) as f64 / 100.
                } else {
                    0.02
                },
                radius,
                kind: if star {
                    0
                } else if traffic {
                    2
                } else {
                    1
                },
            });
        }
        Self::from_world(
            seed,
            World::new(Q, None, bodies)
                .unwrap()
                .with_law(Law::RelativisticV1)
                .unwrap(),
            materials,
        )
    }

    fn from_world(seed: u64, world: World, materials: Vec<Material>) -> Self {
        let history = world
            .bodies
            .iter()
            .map(|b| {
                vec![Segment {
                    tick: world.tick,
                    x: b.x,
                    k: b.k,
                }]
            })
            .collect();
        let drive = four(world.bodies[0].k);
        let clock_rate = rate(world.bodies[0].k);
        Self {
            core: EventCore::new(world, false).unwrap(),
            history,
            materials,
            inputs: vec![],
            heading: 0,
            keys: 0,
            seed,
            proper: 0,
            clock_tick: 0,
            clock_rate,
            deadline: None,
            drive,
            contact_count: 0,
            burns: 0,
        }
    }

    pub fn input(&mut self, input: Input) -> Result<(), String> {
        if input.tick < self.core.tick() || input.keys > 15 {
            return Err("input is in the past or has unknown keys".into());
        }
        self.advance(input.tick)?;
        if self.keys == 0 && input.keys != 0 {
            self.deadline = Some(self.proper + BURN_TAU);
        }
        if input.keys == 0 {
            self.deadline = None;
        }
        self.keys = input.keys;
        self.inputs.push(input);
        Ok(())
    }

    fn capture(&mut self) {
        let w = self.core.world();
        for (i, b) in w.bodies.iter().enumerate() {
            if self.history[i].last().unwrap().k != b.k {
                self.history[i].push(Segment {
                    tick: w.tick,
                    x: b.x,
                    k: b.k,
                });
                if i == 0 {
                    self.clock_rate = rate(b.k);
                    self.drive = four(b.k);
                }
            }
        }
    }

    pub fn advance(&mut self, target: i64) -> Result<(), String> {
        if target < self.core.tick() || target > TPS * 1024 {
            return Err("flight horizon outside [now, 1024 seconds]".into());
        }
        while self.core.tick() < target {
            let r = self.clock_rate;
            let next = self
                .deadline
                .map(|d| self.core.tick() + ((d - self.proper).max(1) + r - 1) as i64 / r as i64)
                .unwrap_or(target);
            let stop = target.min(next);
            // A one-operation budget exposes each atomic contact publication, so a
            // generator is anchored at its true event, never at the frame boundary.
            self.core.advance(stop, 1);
            let t = self.core.tick();
            self.proper += (t - self.clock_tick) as i128 * r;
            self.clock_tick = t;
            if self.core.log().contacts != self.contact_count {
                self.contact_count = self.core.log().contacts;
                self.capture();
            }
            if self.deadline.is_some_and(|d| self.proper >= d) {
                self.burn()?;
                self.deadline = Some(self.deadline.unwrap() + BURN_TAU);
            }
        }
        Ok(())
    }

    fn burn(&mut self) -> Result<(), String> {
        self.heading = self
            .heading
            .wrapping_add(if self.keys & RIGHT != 0 { 2 } else { 0 })
            .wrapping_sub(if self.keys & LEFT != 0 { 2 } else { 0 });
        let sign = ((self.keys & FORWARD != 0) as i128) - ((self.keys & REVERSE != 0) as i128);
        if sign == 0 {
            return Ok(());
        }
        let u = boost(self.drive, self.heading, sign);
        // Stop explicitly before the fixed-point interface can overflow. This is an
        // unsupported rapidity envelope, not a new speed law or a silent clamp.
        if u.iter().any(|v| v.abs() > 4096 * F) {
            return Err("thrust exceeds flight-v0's rapidity envelope; cut thrust".into());
        }
        let k = lattice_velocity(u);
        let old = self.history[0].last().unwrap().k;
        let mut kicks = vec![[0, 0]; self.history.len()];
        kicks[0] = [k[0] - old[0], k[1] - old[1]];
        self.core.kick(&kicks).map_err(|e| e.to_string())?;
        self.capture();
        self.drive = u;
        self.burns += 1;
        Ok(())
    }

    pub fn proper_seconds(&self) -> f64 {
        self.proper as f64 / F as f64 / TPS as f64
    }
    pub fn heading_direction(&self) -> [f64; 2] {
        direction(self.heading).map(|v| v as f64 / F as f64)
    }

    pub fn digest(&self) -> String {
        let mut h = blake3::Hasher::new();
        h.update(b"es-flight-v0");
        h.update(&self.seed.to_le_bytes());
        for s in [self.core.outcome().0, self.core.outcome().1] {
            h.update(s.as_bytes());
        }
        h.update(&self.proper.to_le_bytes());
        h.update(&self.deadline.unwrap_or(-1).to_le_bytes());
        for u in self.drive {
            h.update(&u.to_le_bytes());
        }
        h.update(&[self.heading, self.keys]);
        h.update(&self.burns.to_le_bytes());
        for i in &self.inputs {
            h.update(&i.tick.to_le_bytes());
            h.update(&[i.keys]);
        }
        h.finalize().to_hex().to_string()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn replay_is_independent_of_frame_partition_and_seed_matters() {
        for seed in [0, 1, 17, u64::MAX] {
            let log = [
                Input {
                    tick: 0,
                    keys: FORWARD,
                },
                Input {
                    tick: TPS * 2,
                    keys: FORWARD | RIGHT,
                },
                Input {
                    tick: TPS * 3,
                    keys: 0,
                },
                Input {
                    tick: TPS * 4,
                    keys: REVERSE,
                },
                Input {
                    tick: TPS * 5,
                    keys: 0,
                },
            ];
            let (mut a, mut b) = (Flight::new(seed), Flight::new(seed));
            for i in log {
                a.input(i).unwrap();
                while b.core.tick() < i.tick {
                    b.advance((b.core.tick() + 137).min(i.tick)).unwrap();
                }
                b.input(i).unwrap();
            }
            a.advance(TPS * 6).unwrap();
            b.advance(TPS * 6).unwrap();
            assert_eq!(a.digest(), b.digest(), "seed {seed}");
            assert_ne!(a.digest(), Flight::new(seed.wrapping_add(1)).digest());
            a.core.world().check_speed_limit().unwrap();
        }
    }

    #[test]
    fn proper_acceleration_matches_closed_form_rapidity() {
        for sign in [FORWARD, REVERSE] {
            let w = World::new(
                Q,
                None,
                vec![Body::new(1, [0, 0], [0, 0], 8, 1, Response::Bounce)],
            )
            .unwrap()
            .with_law(Law::RelativisticV1)
            .unwrap();
            let mut f = Flight::from_world(0, w, vec![]);
            f.input(Input {
                tick: 0,
                keys: sign,
            })
            .unwrap();
            f.advance(TPS * 12).unwrap();
            let beta = f.core.world().bodies[0].k[0] as f64 / Q as f64;
            let expected_eta = f.burns as f64 / 128. * if sign == FORWARD { 1. } else { -1. };
            assert!((beta.atanh() - expected_eta).abs() < 0.001);
            assert!((f.burns as f64 / 64. - f.proper_seconds()).abs() <= 1. / 64.);
            // Endpoint proper velocity follows sinh(a τ), independently of the clock.
            assert!((f.drive[0] as f64 / F as f64 - expected_eta.sinh()).abs() < 0.00002);
        }
    }

    #[test]
    fn contacts_keep_the_lattice_outcome_and_true_kink_tick() {
        use emergent_lattice::chronon::Chronon;
        let w = World::new(
            Q,
            None,
            vec![
                Body::new(1, [-Q * 10, 0], [Q / 2, 0], 8, Q, Response::Bounce),
                Body::new(2, [Q * 10, 0], [-Q / 2, 0], 8, Q, Response::Bounce),
            ],
        )
        .unwrap()
        .with_law(Law::RelativisticV1)
        .unwrap();
        let mut oracle = Chronon::new(w.clone(), true).unwrap();
        let mut f = Flight::from_world(0, w, vec![]);
        f.advance(60).unwrap();
        oracle.run_to(60);
        assert_eq!(f.core.outcome(), oracle.outcome());
        assert_eq!(f.history[0].len(), 2);
        assert_eq!(f.history[0][1].tick, oracle.log().events[0].tick);
    }
}
