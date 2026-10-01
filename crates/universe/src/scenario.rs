//! The worlds: the restricted problem the behaviour checks use, and the star system the plane flies.
use crate::body::Kind;
use crate::ctx::Config;
use crate::num::{s, Res};
use crate::universe::{OrbitSpec, Universe};
use emergent_space::orbit::Scalar;

/// The sun's `M` is 1.477 km: one root length unit. One astronomical unit in root units.
pub const AU: i64 = 101_300_000;
/// The star's radius (the sun's, 6.96e8 m) in root units.
pub const STAR_RADIUS: i64 = 471_000;

/// A star, one planet on a circle of radius `sep` with mass `2^mu_log2`, and test ships on circular
/// heliocentric orbits at `(sep + dr)` and angle `alpha` (turns, Q32): the restricted problem the
/// Jacobi checks use. `dr` and `alpha` come from the caller; nothing here is random.
pub struct Restricted {
    pub u: Universe,
    pub planet: usize,
    pub ships: Vec<usize>,
}

pub fn restricted(mu_log2: i32, sep: i64, planet_radius_root: i64, ships: &[(i64, u32)], clock_threads: usize) -> Res<Restricted> {
    restricted_with(mu_log2, sep, planet_radius_root, ships, clock_threads, Config::default())
}

pub fn restricted_with(mu_log2: i32, sep: i64, planet_radius_root: i64, ships: &[(i64, u32)], clock_threads: usize, cfg: Config) -> Res<Restricted> {
    let mut u = Universe::new(s(STAR_RADIUS), cfg);
    u.threads = clock_threads;
    let planet = u.add_body(
        Kind::Planet,
        OrbitSpec { doll: 0, periapsis: s(sep), e_q48: 0, clockwise: false, angle: 0, phase: 0 },
        Scalar::ZERO,
    )?;
    let surface = Scalar::raw(planet_radius_root as i128, -mu_log2 as i32)?.scale(0)?; // root units → planet units: × 2^-mu_log2
    u.add_doll("planet", planet, mu_log2, surface)?;
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
