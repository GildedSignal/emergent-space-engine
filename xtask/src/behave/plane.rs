//! The plane itself as a law: `behave --law plane` answers the restricted problem with the shipped
//! plane (crates/universe), through its public API only, so the frozen gates B12-B14 and B17 judge
//! the engine the game flies, not the `space` crate's dense stepper. The scene is the judge's (a
//! star and a planet of mass ratio μ on a circle, in units of their total mass); the plane's root
//! unit is the star's mass, so every length and time crosses as `/(1 − μ)` and velocities (β,
//! c = 1) cross unchanged. Floats appear only at this boundary; everything inside is the plane's
//! integer law. The star's surface is the shipped plane's (STAR_RADIUS) at the plane's own scale,
//! scaled down with a scene shrunk below one AU (B17's miniature, sep = 100: the judge's star is a
//! point, and a surface that could swallow the whole system would decide an outcome nobody asked
//! for). The kick cadence is `Config::step_log2` (`--plane-step`): a power of two of ticks near
//! 2^step_log2 kicks per radial period of each tube. With `PLANE_TRACE` set, every answer leaves
//! one line on stderr: the event counts of the run that produced it, or where a ship the law lost
//! was lost (a law that kills a ship the judge keeps is a finding, not a gap in the adapter).
use super::restricted::Restricted;
use super::Law;
use emergent_space::orbit::Scalar;
use emergent_universe::num::{from_f64, to_f64};
use emergent_universe::observe;
use emergent_universe::scenario::{AU, STAR_RADIUS};
use emergent_universe::world::Mass;
use emergent_universe::{Config, Kind, OrbitSpec, Universe};

pub struct Plane {
    pub step_log2: i32,
}

impl Plane {
    /// From the CLI's `--plane-step`, the plane's own default when absent.
    pub fn new(step_log2: Option<i32>) -> Self {
        Self { step_log2: step_log2.unwrap_or(Config::default().step_log2) }
    }

    /// The star's surface in root units: the shipped plane's at its own scale, scaled down with a
    /// scene whose planet orbits within one AU of its star.
    fn star_surface(scene: &Restricted, to_root: f64) -> Scalar {
        from_f64(STAR_RADIUS as f64 * (scene.sep * to_root / AU as f64).min(1.0))
    }
}

// The single-mass questions the plane does not answer through this boundary: it says so, which
// fails those gates honestly (`space` answers them through the crates the plane shares).
impl Law for Plane {
    fn advance_per_cycle(&self, _: f64, _: f64) -> Option<(f64, f64, f64)> {
        None
    }
    fn deflection(&self, _: f64) -> Option<f64> {
        None
    }
    fn captured(&self, _: f64, _: f64) -> bool {
        false
    }
    fn photon_captured(&self, _: f64) -> bool {
        false
    }
    fn long_run(&self, _: f64, _: f64, _: usize) -> Vec<(f64, f64, f64, f64)> {
        Vec::new()
    }

    fn restricted(&self, scene: &Restricted, ship: [f64; 4], times: &[f64]) -> Option<Vec<[f64; 4]>> {
        if !(0.0..0.5).contains(&scene.mu)
            || !scene.sep.is_finite()
            || scene.sep <= 0.0
            || ship.iter().chain(times.iter()).any(|x| !x.is_finite())
            || times.iter().any(|&t| t < 0.0)
            || times.windows(2).any(|w| w[0] > w[1])
        {
            return None;
        }
        // Judge units (M_total = 1) → root units (M_star = 1): lengths and times × 1/(1 − μ).
        let mu = scene.mu;
        let to_root = 1.0 / (1.0 - mu);
        // The planet's mass in units of the star's: q = μ/(1 − μ), exact for the f64 given
        // (`Mass::ratio(1, 999)` is the case μ = 1e-3; B17's μ are not).
        let mass = Mass::of(from_f64(mu / (1.0 - mu))).ok()?;
        let cfg = Config { step_log2: self.step_log2, ..Config::default() };
        let trace = std::env::var_os("PLANE_TRACE").is_some();
        let build = || -> Option<(Universe, usize)> {
            let mut u = Universe::new(Self::star_surface(scene, to_root), cfg);
            u.threads = 1;
            // The planet: a circular tube of the judge's separation about the star (the Kepler
            // problem of the pair's total mass, as the plane compiles it), at (sep, 0), ccw.
            let planet = u
                .add_body(
                    Kind::Planet,
                    OrbitSpec { doll: 0, periapsis: from_f64(scene.sep * to_root), e_q48: 0, clockwise: false, angle: 0, phase: 0 },
                    Scalar::ZERO,
                )
                .ok()?;
            // The doll's surface is the planet's radius in the doll's units (root × 2^−octave).
            let surface = from_f64(scene.planet_radius * to_root).scale(-mass.octave).ok()?;
            u.add_doll("planet", planet, mass, surface).ok()?;
            // The ship: an exact heliocentric start (the star's own barycentric state at t = 0).
            let (sp, sv) = scene.star(0.0);
            let id = u
                .add_body_state(
                    Kind::Ship,
                    0,
                    [from_f64((ship[0] - sp[0]) * to_root), from_f64((ship[1] - sp[1]) * to_root)],
                    [from_f64(ship[2] - sv[0]), from_f64(ship[3] - sv[1])],
                    Scalar::ZERO,
                )
                .ok()?;
            u.start().ok()?;
            Some((u, id))
        };
        let (mut u, id) = build().or_else(|| {
            if trace {
                eprintln!("plane_trace step_log2={} refused: the scene would not build", self.step_log2);
            }
            None
        })?;
        let mut states = Vec::with_capacity(times.len());
        for &t in times {
            let tick = (t * to_root).round() as i64;
            u.settle(tick);
            // A ship the plane lost (a surface, the system's edge, a state no tube can hold) has
            // no answer; extrapolating its last tube would invent one.
            if !u.bodies().alive(id) {
                if trace {
                    eprintln!(
                        "plane_trace step_log2={} lost at sample {} of {} (kicks={} handoffs={} refused={} lost={})",
                        self.step_log2,
                        states.len() + 1,
                        times.len(),
                        u.stats.kicks,
                        u.stats.handoffs,
                        u.stats.refused,
                        u.stats.lost
                    );
                }
                return None;
            }
            let (pos, vel) = observe::root_state(&u.ctx(), id, tick).ok()?;
            // Heliocentric root units → barycentric judge units: × (1 − μ), plus the star's own.
            let (sp, sv) = scene.star(t);

            states.push([
                pos[0] / to_root + sp[0],
                pos[1] / to_root + sp[1],
                vel[0] + sv[0],
                vel[1] + sv[1],
            ]);
        }
        if trace {
            eprintln!(
                "plane_trace step_log2={} samples={} spans={:.4} planet-periods kicks={} handoffs={} boundaries={} opens={} refused={} lost={} events={}",
                self.step_log2,
                times.len(),
                times.last().copied().unwrap_or(0.0) / scene.period(),
                u.stats.kicks,
                u.stats.handoffs,
                u.stats.boundaries,
                u.stats.opens,
                u.stats.refused,
                u.stats.lost,
                u.stats.events(),
            );
        }
        let _ = to_f64; // observation only; never an outcome
        Some(states)
    }
}

#[cfg(test)]
mod tests {
    use super::super::restricted::{self, JUPITER, RTOL};
    use super::*;

    /// A ship at 4.1 sep, far outside the planet's sphere of influence, on a circular orbit.
    fn far_ship() -> [f64; 4] {
        let scene = JUPITER;
        let r = 4.1 * scene.sep;
        let v = (1.0 - scene.mu).sqrt() * r.powf(-0.5); // circular about the star's mass
        let (x, y) = (r * 0.6, r * 0.8);
        let (vx, vy) = (-v * 0.8, v * 0.6);
        let (p, w) = scene.star(0.0);
        [p[0] + x, p[1] + y, w[0] + vx, w[1] + vy]
    }

    fn times() -> Vec<f64> {
        (1..=40).map(|k| k as f64 * JUPITER.period() / 4.0).collect()
    }

    /// The worst of the law's states against the reference's, positions against `sep` and
    /// velocities against the planet's speed `sep·Ω`.
    fn worst(step: i32, truth: &[[f64; 4]]) -> f64 {
        let scene = JUPITER;
        let law = Plane { step_log2: step }.restricted(&scene, far_ship(), &times()).unwrap();
        let vscale = scene.sep * scene.omega();
        law.iter()
            .zip(truth)
            .flat_map(|(a, b)| (0..4).map(move |k| (a[k] - b[k]).abs() / if k < 2 { scene.sep } else { vscale }))
            .fold(0.0f64, f64::max)
    }

    /// The adapter is faithful at the boundary: the state it returns at t = 0 is the state it was
    /// given (the plane binds the exact integer state), through the whole unit and frame conversion.
    #[test]
    fn the_start_comes_back_through_the_conversion() {
        let ship = far_ship();
        let back = Plane { step_log2: 7 }.restricted(&JUPITER, ship, &[0.0]).unwrap();
        for (a, b) in back[0].iter().zip(ship) {
            assert!((a - b).abs() / b.abs().max(1e-30) < 1e-12, "{back:?} vs {ship:?}");
        }
    }

    /// A far ship keeps its orbit: against the judge's own reference (the planet present, float64
    /// at 1e-12), within the kicks' own error. A conversion bug errs at ~μ·sep per synodic period
    /// and grows linearly (past 1e-2·sep over this span); the cadence's own error is the 5e-4·sep
    /// measured here at 2^7, and the next test tells the two apart.
    #[test]
    fn a_far_ship_keeps_its_orbit_against_the_reference() {
        let truth = restricted::reference(&JUPITER, far_ship(), &times(), RTOL).unwrap();
        let w = worst(7, &truth);
        assert!(w < 3e-3, "worst {w:.3e}");
    }

    /// The far ship's error is the kick cadence's, not the conversion's: it falls like H² when the
    /// cadence doubles twice (a conversion bug would not move).
    #[test]
    fn a_far_ships_error_falls_like_the_cadence() {
        let truth = restricted::reference(&JUPITER, far_ship(), &times(), RTOL).unwrap();
        let (coarse, fine) = (worst(7, &truth), worst(9, &truth));
        assert!(coarse > 0.0 && fine < coarse / 8.0, "step 7: {coarse:.3e}, step 9: {fine:.3e}");
    }

    /// Not the B14 gate (its 768 reference runs cannot fit this machine's 60 s phase limit —
    /// `echo` itself times out): a probe of the same physics through the public pieces only —
    /// the gate's own first `N` circular births, one reference run each (no convergence nudge),
    /// the class from the gate's rule (beyond 1.5 R_H at any sample) and the gate's own
    /// `apsidal_rate`. `cargo test --release -p xtask moon_probe -- --ignored --nocapture`.
    #[test]
    #[ignore]
    fn moon_probe_b14_physics_not_the_gate() {
        use super::super::hill;
        let scene = JUPITER;
        let times = hill::times(&scene);
        let escape = |states: &[[f64; 4]]| times.iter().zip(states).any(|(&t, s)| scene.planet_distance(t, s) > 1.5 * scene.hill());
        for step in [7i32, 3] {
            let (mut agree, mut answered) = (0, 0);
            for (i, (a_hill, phase)) in super::super::sample::moons(12).into_iter().enumerate() {
                let ship = hill::birth(&scene, a_hill * scene.hill(), phase, 0.0, i % 2 == 0);
                let Some(truth_states) = restricted::reference(&scene, ship, &times, RTOL) else { continue };
                let truth = escape(&truth_states);
                answered += 1;
                match (Plane { step_log2: step }).restricted(&scene, ship, &times) {
                    None => println!("step {step} moon {i} a={a_hill:.3}R_H retro={}: LOST (reference {})", i % 2 == 1, if truth { "escape" } else { "bound" }),
                    Some(s) => {
                        let mine = escape(&s);
                        agree += (mine == truth) as usize;
                        let rate = |x: &[[f64; 4]]| hill::apsidal_rate(&scene, &times, x).map(|r| format!("{r:9.4}")).unwrap_or_else(|| "    none".into());
                        println!(
                            "step {step} moon {i} a={a_hill:.3}R_H retro={}: class {} (reference {}), apsidal rate law {} reference {}",
                            i % 2 == 1,
                            if mine { "escape" } else { "bound" },
                            if truth { "escape" } else { "bound" },
                            rate(&s),
                            rate(&truth_states)
                        );
                    }
                }
            }
            println!("step {step}: classes {agree}/{answered} agree");
        }
    }
}
