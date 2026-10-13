//! The worlds: the restricted problem the behaviour checks use, and the star system the plane flies.
use crate::body::Kind;
use crate::ctx::Config;
use crate::num::{s, Res};
use crate::universe::{OrbitSpec, Universe};
use crate::world::Mass;
use emergent_space::orbit::Scalar;

/// The sun's `M` is 1.477 km: one root length unit. One astronomical unit in root units.
pub const AU: i64 = 101_300_000;
/// The star's radius (the sun's, 6.96e8 m) in root units.
pub const STAR_RADIUS: i64 = 471_000;

/// A star, one planet on a circle of radius `sep` with mass `mu` (a [`Mass`], in the star's: `Mass::ratio(1, 999)`
/// is the planet of a thousandth of the total; an `i32` is the old call, `2^mu_log2`), and test ships on circular
/// heliocentric orbits at `(sep + dr)` and angle `alpha` (turns, Q32): the restricted problem the Jacobi
/// checks use. `dr` and `alpha` come from the caller; nothing here is random. The planet's tube is the relative
/// orbit of the star and the planet (the Kepler problem of their total mass, so it turns at `√((1 + μ)/sep³)`).
pub struct Restricted {
    pub u: Universe,
    pub planet: usize,
    pub ships: Vec<usize>,
}

pub fn restricted(mu: impl Into<Mass>, sep: i64, planet_radius_root: i64, ships: &[(i64, u32)], clock_threads: usize) -> Res<Restricted> {
    restricted_with(mu, sep, planet_radius_root, ships, clock_threads, Config::default())
}

pub fn restricted_with(mu: impl Into<Mass>, sep: i64, planet_radius_root: i64, ships: &[(i64, u32)], clock_threads: usize, cfg: Config) -> Res<Restricted> {
    let mu = mu.into();
    let mut u = Universe::new(s(STAR_RADIUS), cfg);
    u.threads = clock_threads;
    let planet = u.add_body(
        Kind::Planet,
        OrbitSpec { doll: 0, periapsis: s(sep), e_q48: 0, clockwise: false, angle: 0, phase: 0 },
        Scalar::ZERO,
    )?;
    let surface = Scalar::raw(planet_radius_root as i128, -mu.octave)?; // root units → planet units: × 2^-octave
    u.add_doll("planet", planet, mu, surface)?;
    let mut ids = Vec::new();
    for &(r, alpha) in ships {
        ids.push(u.add_body(
            Kind::Ship,
            OrbitSpec { doll: 0, periapsis: s(r), e_q48: 0, clockwise: false, angle: alpha, phase: 0 },
            Scalar::ZERO,
        )?);
    }
    u.start()?;
    Ok(Restricted { u, planet, ships: ids })
}

// ---- relativistic content for the view ------------------------------------------------------------

/// How a stream's emitters move against the line of sight to the observer.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Stream {
    /// Perpendicular to the bearing they were made at.
    Across,
    /// Toward the observer.
    Toward,
    /// Away from it.
    Away,
}

/// A player in the star's doll that is at `(R, 0)` (`R = 10^8` root units) at tick `start`, circular about the star
/// when `beta_obs` is zero and otherwise moving at that speed along `+y`; and `n` emitters that are at `dist` root
/// units from it then, at evenly spaced bearings, each at speed `beta` in the direction `stream` says. Every one is a
/// bare tube (nothing pulls it, so nothing happens to it), made at tick 0 from its exact state (the straight line
/// back from `start`), so the view's cost on content at any speed is measurable on its own: the stream of B15's scene
/// at 0.9c is the content the game exists for. Tubes end at twice their radius: the scene is good while every
/// body is within `2·10^8` of the star (ticks of light). Returns the universe, the emitters' ids and the player's.
pub fn stream(beta_obs: f64, beta: f64, stream: Stream, n: usize, dist: f64, start: i64) -> Res<(Universe, Vec<usize>, usize)> {
    use crate::num::from_f64;
    let r = 1.0e8;
    let mut u = Universe::new(s(STAR_RADIUS), Config::default());
    let player = if beta_obs == 0.0 {
        u.add_body(Kind::Player, OrbitSpec { doll: 0, periapsis: from_f64(r), e_q48: 0, clockwise: false, angle: 0, phase: 0 }, Scalar::ZERO)?
    } else {
        u.add_body_state(Kind::Player, 0, [from_f64(r), from_f64(-beta_obs * start as f64)], [Scalar::ZERO, from_f64(beta_obs)], Scalar::ZERO)?
    };
    let mut ids = Vec::new();
    for j in 0..n {
        let th = (j as f64 + 0.5) / n as f64 * std::f64::consts::TAU;
        let bearing = [th.cos(), th.sin()]; // from the observer to the emitter
        let dir = match stream {
            Stream::Across => [-bearing[1], bearing[0]],
            Stream::Toward => [-bearing[0], -bearing[1]],
            Stream::Away => bearing,
        };
        // where it is at `start`, and the straight line back to tick 0
        let pos = [r + dist * bearing[0] - beta * dir[0] * start as f64, dist * bearing[1] - beta * dir[1] * start as f64];
        ids.push(u.add_body_state(Kind::Ship, 0, [from_f64(pos[0]), from_f64(pos[1])], [from_f64(beta * dir[0]), from_f64(beta * dir[1])], Scalar::ZERO)?);
    }
    u.start()?;
    Ok((u, ids, player))
}

// ---- the star system the plane flies -------------------------------------------------------------

/// A named planet of the system.
pub struct PlanetSpec {
    pub name: &'static str,
    /// Mass as an octave of the star's (a game's choice: a power of two).
    pub mass_log2: i32,
    /// Orbit: periapsis radius (root units), eccentricity (Q48), where periapsis points (turns, Q32)
    /// and the phase at tick 0 (fraction of the radial period since periapsis, Q32).
    pub periapsis: i64,
    pub e_q48: u64,
    pub angle: u32,
    pub phase: u32,
    /// The planet's radius in root units.
    pub radius: i64,
}

pub const PLANETS: [PlanetSpec; 3] = [
    // Cinder: a hot rock at 0.39 AU.
    PlanetSpec { name: "Cinder", mass_log2: -21, periapsis: 35_600_000, e_q48: (1u64 << 48) / 10, angle: 0x3000_0000, phase: 0x5000_0000, radius: 1_650 },
    // Home: an Earth at 1 AU, where the fleet and the player are.
    PlanetSpec { name: "Home", mass_log2: -18, periapsis: 99_300_000, e_q48: (1u64 << 48) / 50, angle: 0x9000_0000, phase: 0x2000_0000, radius: 4_313 },
    // Giant: a Jupiter at 5.2 AU.
    PlanetSpec { name: "Giant", mass_log2: -10, periapsis: 500_000_000, e_q48: (1u64 << 48) / 20, angle: 0xC000_0000, phase: 0xA000_0000, radius: 47_400 },
];

/// The ids of what the plane made.
pub struct Plane {
    pub u: Universe,
    pub planets: Vec<usize>,
    pub dolls: Vec<u16>,
    pub moon: usize,
    pub player: usize,
    pub ships: Vec<usize>,
    pub fleet: usize,
    /// Names by body id (for the view).
    pub names: Vec<String>,
}

fn lcg(seed: &mut u64) -> f64 {
    *seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
    (*seed >> 11) as f64 / (1u64 << 53) as f64
}

/// The first universe that flies: one star, three planets, a moon, ships on orbits (about the star,
/// about Home and about the Giant), one fleet battle in a Fermi frame about Home, and the player's
/// ship in low orbit near the fleet. Every number is a literal or comes from a fixed seeded
/// generator; nothing is engineered to produce an outcome.
pub fn plane(cfg: Config, seed: u64, order: crate::fleet::Order, threads: usize, members: u64) -> Res<Plane> {
    let (world, _) = emergent_engine::scenes::battle(members, crate::fleet::Q, seed, 1 << 15, false);
    plane_with(cfg, seed, order, threads, world)
}

/// [`plane`] with the fleet's world given (lattice bodies in the frame's axes, `crates/engine`'s scenes or
/// a test's own): the same star, planets, moon, ships and player.
pub fn plane_with(cfg: Config, seed: u64, order: crate::fleet::Order, threads: usize, world: emergent_lattice::law::World) -> Res<Plane> {
    plane_with_extra(cfg, seed, order, threads, world, 0)
}

/// [`plane`] with `extra` more real bodies: ships made by [`ladder_ship`] (the N ladder's population: a few hundred about
/// Home and the Moon, the rest in a belt about the star), each on its own exact orbit, with the ids after the plane's own ships
/// and before the player's. `extra = 0` is the plane, bit for bit.
pub fn plane_extra(cfg: Config, seed: u64, order: crate::fleet::Order, threads: usize, members: u64, extra: usize) -> Res<Plane> {
    let (world, _) = emergent_engine::scenes::battle(members, crate::fleet::Q, seed, 1 << 15, false);
    plane_with_extra(cfg, seed, order, threads, world, extra)
}

/// [`plane_with`] with `extra` more real bodies (see [`plane_extra`]).
pub fn plane_with_extra(cfg: Config, seed: u64, order: crate::fleet::Order, threads: usize, world: emergent_lattice::law::World, extra: usize) -> Res<Plane> {
    use crate::fleet::{Fleet, Q};
    let mut u = Universe::new(s(STAR_RADIUS), cfg);
    u.threads = threads;
    let mut rng = seed ^ 0x5DEECE66D;
    let mut planets = Vec::new();
    let mut dolls = Vec::new();
    let mut names = Vec::new();
    for p in &PLANETS {
        let b = u.add_body(
            Kind::Planet,
            OrbitSpec { doll: 0, periapsis: s(p.periapsis), e_q48: p.e_q48, clockwise: false, angle: p.angle, phase: p.phase },
            Scalar::ZERO,
        )?;
        // The planet's radius in its own doll's units: root units × 2^(−mass_log2).
        let surface = Scalar::raw(p.radius as i128, -p.mass_log2)?;
        let d = u.add_doll(p.name, b, p.mass_log2, surface)?;
        planets.push(b);
        dolls.push(d);
        names.push(p.name.to_string());
    }
    let (home, home_doll) = (planets[1], dolls[1]);
    let giant_doll = dolls[2];
    // The moon: 2^-6 of Home's mass, at 60 Earth radii, in Home's doll. Its radius is 1,176 root units.
    let m = u.add_body(
        Kind::Moon,
        OrbitSpec { doll: home_doll, periapsis: Scalar::raw(260_000, 18)?, e_q48: (1u64 << 48) / 20, clockwise: false, angle: 0x1000_0000, phase: 0x7000_0000 },
        Scalar::raw(1_176, 18)?,
    )?;
    // Its sphere of influence from the mass ratio, in Home's units.
    let sep = u.rec(m).b.entry.trajectory.key().ok_or(crate::num::Error::Refused("moon without turning orbit"))?.periapsis;
    let proto = emergent_space::events::Doll::child(emergent_space::events::LogMass((-24) << 24), home_doll, u.rec(m).b.tube);
    let soi = proto.edge_radius(&u.dolls[home_doll as usize].record.clone(), sep)?;
    u.make_source(m, -6, soi)?;
    names.push("Moon".into());
    // Ships about the star: between 0.5 and 8 AU, e up to 0.25.
    let mut ships = Vec::new();
    for _ in 0..12 {
        let a = (0.5 + 7.5 * lcg(&mut rng)) * AU as f64;
        let e = 0.25 * lcg(&mut rng);
        let id = u.add_body(
            Kind::Ship,
            OrbitSpec {
                doll: 0,
                periapsis: s((a * (1.0 - e)) as i64),
                e_q48: (e * (1u64 << 48) as f64) as u64,
                clockwise: lcg(&mut rng) < 0.15,
                angle: (lcg(&mut rng) * 4294967296.0) as u32,
                phase: (lcg(&mut rng) * 4294967296.0) as u32,
            },
            Scalar::raw(34, -10)?,
        )?;
        ships.push(id);
        names.push(format!("Hauler {}", ships.len()));
    }
    // Ships about Home: low to medium orbits, near-circular.
    for k in 0..8 {
        let alt = 1.15 + 0.35 * k as f64 + 0.2 * lcg(&mut rng);
        let p = Scalar::raw((4_313.0 * alt * 1024.0) as i128, -10 + 18)?;
        let id = u.add_body(
            Kind::Ship,
            OrbitSpec {
                doll: home_doll,
                periapsis: p,
                e_q48: ((0.02 * lcg(&mut rng)) * (1u64 << 48) as f64) as u64,
                clockwise: k % 5 == 4,
                angle: (lcg(&mut rng) * 4294967296.0) as u32,
                phase: (lcg(&mut rng) * 4294967296.0) as u32,
            },
            Scalar::raw(34, -10 + 18)?,
        )?;
        ships.push(id);
        names.push(format!("Orbiter {}", k + 1));
    }
    // Ships about the Giant.
    for k in 0..3 {
        let alt = 1.6 + 1.1 * k as f64 + 0.3 * lcg(&mut rng);
        let p = Scalar::raw((47_400.0 * alt * 1024.0) as i128, -10 + 10)?;
        let id = u.add_body(
            Kind::Ship,
            OrbitSpec {
                doll: giant_doll,
                periapsis: p,
                e_q48: ((0.05 * lcg(&mut rng)) * (1u64 << 48) as f64) as u64,
                clockwise: false,
                angle: (lcg(&mut rng) * 4294967296.0) as u32,
                phase: (lcg(&mut rng) * 4294967296.0) as u32,
            },
            Scalar::raw(34, -10 + 10)?,
        )?;
        ships.push(id);
        names.push(format!("Skimmer {}", k + 1));
    }
    // The ladder's ships: real bodies, each on its own exact orbit, built from integers and the seed.
    for k in 0..extra {
        let (spec, radius) = ladder_ship(seed, k as u64, extra as u64, home_doll)?;
        ships.push(u.add_body(Kind::Ship, spec, radius)?);
        names.push(String::new());
    }
    // The fleet: lattice radius of Home's low orbit (7,000 km: 4,740 root units), starting at angle 0.
    let r_lat: i64 = 4_740 * Q;
    let (fleet_angle, player_offset) = (0x4000_0000u32, 2_100_000u32);
    let fleet = Fleet::new("Armada", home_doll, home, -18, world, r_lat, fleet_angle, order, threads.max(1))?;
    // The player: the same circle, a little ahead of the fleet (about 20 km along the orbit).
    let p_orbit = Scalar::raw(r_lat as i128, -20 + 18)?; // lattice units → root units → Home's units
    let player = u.add_body(
        Kind::Player,
        OrbitSpec { doll: home_doll, periapsis: p_orbit, e_q48: 0, clockwise: false, angle: fleet_angle.wrapping_add(player_offset), phase: 0 },
        Scalar::raw(34, -10 + 18)?,
    )?;
    names.push("You".into());
    let f = u.add_fleet(fleet);
    u.start()?;
    Ok(Plane { u, planets, dolls, moon: m, player, ships, fleet: f, names })
}

// ---- the N ladder's population -------------------------------------------------------------------

/// How many of `extra` ladder ships are about Home and the Moon (the rest are the belt): a few hundred, at most half.
pub fn ladder_locals(extra: u64) -> u64 {
    (extra / 2).min(300)
}

/// splitmix64's finalizer: the ladder's only source of randomness, with the seed (integers all the way).
fn mix64(mut z: u64) -> u64 {
    z = z.wrapping_add(0x9E37_79B9_7F4A_7C15);
    z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
    z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
    z ^ (z >> 31)
}

/// Draw `lane` of ship `k`: independent of every other ship's draws (a counter, not a stream).
fn draw(seed: u64, k: u64, lane: u64) -> u64 {
    mix64(mix64(seed ^ 0x5DEE_CE66_D1CE_4E5B) ^ k.wrapping_mul(0x9E37_79B9_7F4A_7C15) ^ (lane << 56))
}

/// `e · 2^48` of a Rayleigh draw of scale `sigma_milli / 1000` from a uniform 32-bit `u`: `σ √(−2 ln(1 − u))`, in integers
/// (`log2` by squaring, `ln = ln2 · log2`, an integer root): the same bits on every machine.
pub fn rayleigh_q48(u: u32, sigma_milli: u64) -> u64 {
    let d = (1u64 << 32) - u as u64; // the survival probability, d / 2^32, in (0, 1]
    let k = 63 - d.leading_zeros() as u64;
    let mut x = (d as u128) << (62 - k); // the mantissa in [1, 2), Q62
    let mut frac = 0u64;
    for _ in 0..32 {
        x = (x * x) >> 62;
        frac <<= 1;
        if x >= 2u128 << 62 {
            x >>= 1;
            frac |= 1;
        }
    }
    let l2 = (32u64 << 32) - ((k << 32) | frac); // log2(2^32 / d), Q32
    let ln = (l2 as u128 * 2_977_044_472u128) >> 32; // ln 2 = 2977044472 / 2^32; ln(2^32 / d), Q32
    let e2 = ln * 2 * (sigma_milli as u128).pow(2) / 1_000_000; // e², Q32
    (e2 << 64).isqrt() as u64 // e · 2^48
}

/// One ship of the N ladder: the orbit it is made on and its radius. Ship `k` of `extra`: the first [`ladder_locals`] are about
/// Home (a quarter of them on the Moon's orbit, 60 degrees ahead of or behind it, where a ship stays; the rest from just above
/// the surface out to two thirds of the Moon's distance, Rayleigh eccentricities); the rest are a belt about the star between 2
/// and 3 AU (Rayleigh eccentricities of scale 0.07, periapsis above 1.2 AU: no crossing of Home's orbit), uniform angles. Each is
/// a real body on its own exact orbit; nothing is averaged, and every number is an integer from the seed and `k`.
pub fn ladder_ship(seed: u64, k: u64, extra: u64, home_doll: u16) -> Res<(OrbitSpec, Scalar)> {
    let d = |lane: u64| draw(seed, k, lane);
    let (angle, phase) = (d(3) as u32, (d(3) >> 32) as u32);
    let locals = ladder_locals(extra);
    if k >= locals {
        // The belt: a uniform in [2, 3) AU at 2^-8 of a root unit, e Rayleigh (re-drawn above 0.4), p = a (1 - e).
        let a_q8 = ((2 * AU as u128) << 8) + (d(1) as u128 % ((AU as u128) << 8));
        let mut e = rayleigh_q48((d(2) >> 32) as u32, 70);
        for lane in 16.. {
            if e <= (2u64 << 48) / 5 {
                break;
            }
            e = rayleigh_q48((d(lane) >> 32) as u32, 70);
        }
        let p_q8 = a_q8 - ((a_q8 * e as u128) >> 48);
        let spec = OrbitSpec { doll: 0, periapsis: Scalar::raw(p_q8 as i128, -8)?, e_q48: e, clockwise: false, angle, phase };
        return Ok((spec, Scalar::raw(34, -10)?));
    }
    let radius = Scalar::raw(34, -10 + 18)?;
    if k < locals / 4 {
        // About the Moon: its orbit (periapsis 260,000 root units, e = 1/20, the Moon's angle), 3 % off in size at most, e within a
        // tenth of its own, 60 degrees ahead of it or behind (L4 and L5) within 5 degrees.
        let jit = |lane: u64| (d(lane) >> 32) as i128 - (1i128 << 31); // [-2^31, 2^31): [-1/2, 1/2) turn of 2^32
        let base = 260_000i128 << 16;
        let peri_q16 = base + base * 6 * jit(4) / (100 * (1i128 << 32));
        let e = ((1i128 << 48) / 20 + ((1i128 << 48) / 100) * jit(5) / (1i128 << 32)) as u64;
        let sixth = (1i128 << 32) / 6;
        let phase = 0x7000_0000i128 + if d(6) & 1 == 0 { sixth } else { -sixth } + jit(7) / 36;
        let spec = OrbitSpec {
            doll: home_doll,
            periapsis: Scalar::raw(peri_q16, 18 - 16)?,
            e_q48: e,
            clockwise: false,
            angle: 0x1000_0000,
            phase: phase.rem_euclid(1 << 32) as u32,
        };
        return Ok((spec, radius));
    }
    // About Home: a in [5,200 root units, 2^5 times that): an octave uniform and the place in it uniform; e Rayleigh of scale 0.03
    // (re-drawn above 0.1: the periapsis clears the surface); 1 in 8 against the planet's turn.
    let lo_q16 = 5_200u128 << 16;
    let oct = d(1) % 5;
    let a_q16 = (lo_q16 << oct) + (((lo_q16 << oct) * (d(2) >> 32) as u128) >> 32);
    let mut e = rayleigh_q48((d(2) & 0xFFFF_FFFF) as u32, 30);
    for lane in 16.. {
        if e <= (1u64 << 48) / 10 {
            break;
        }
        e = rayleigh_q48((d(lane) >> 32) as u32, 30);
    }
    let p_q16 = a_q16 - ((a_q16 * e as u128) >> 48);
    let spec = OrbitSpec { doll: home_doll, periapsis: Scalar::raw(p_q16 as i128, 18 - 16)?, e_q48: e, clockwise: d(5) & 7 == 0, angle, phase };
    Ok((spec, radius))
}
