//! Verbatim subset of xtask/src/behave/plane.rs: the shipped plane as a B12 law (the adapter and
//! `restricted` are the gate's own code, byte for byte; only the `Law` trait is the local
//! `LawR`). `--plane-step`'s default is Config::default().step_log2 = 7 (ctx.rs).
use crate::handoff::LawR;
use crate::restricted::Restricted;
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
    pub fn new(step_log2: Option<i32>) -> Self {
        Self { step_log2: step_log2.unwrap_or(Config::default().step_log2) }
    }

    fn star_surface(scene: &Restricted, to_root: f64) -> Scalar {
        from_f64(STAR_RADIUS as f64 * (scene.sep * to_root / AU as f64).min(1.0))
    }
}

/// Verbatim `build_scene`.
pub fn build_scene(scene: &Restricted, ship: [f64; 4], step_log2: i32) -> Option<(Universe, usize)> {
    let mu = scene.mu;
    let to_root = 1.0 / (1.0 - mu);
    let mass = Mass::of(from_f64(mu / (1.0 - mu))).ok()?;
    let cfg = Config { step_log2, ..Config::default() };
    let mut u = Universe::new(Plane::star_surface(scene, to_root), cfg);
    u.threads = 1;
    let planet = u
        .add_body(
            Kind::Planet,
            OrbitSpec { doll: 0, periapsis: from_f64(scene.sep * to_root), e_q48: 0, clockwise: false, angle: 0, phase: 0 },
            Scalar::ZERO,
        )
        .ok()?;
    let surface = from_f64(scene.planet_radius * to_root).scale(-mass.octave).ok()?;
    u.add_doll("planet", planet, mass, surface).ok()?;
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
}

/// Verbatim `Plane::restricted`.
impl LawR for Plane {
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
        let mu = scene.mu;
        let to_root = 1.0 / (1.0 - mu);
        let trace = std::env::var_os("PLANE_TRACE").is_some();
        let build = || build_scene(scene, ship, self.step_log2);
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
