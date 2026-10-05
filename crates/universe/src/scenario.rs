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
    let sep = u.rec(m).b.entry.trajectory.key().periapsis;
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
