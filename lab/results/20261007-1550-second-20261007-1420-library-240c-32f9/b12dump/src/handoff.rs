//! Verbatim subset of xtask/src/behave/handoff.rs (B12): the scene's frozen ships, the sample
//! times, and the law's err series. Only `Gate`/`Law` plumbing is adapted (a minimal `LawR`
//! trait here); every constant, every line of the search/assess/series code is the gate's own.
use crate::restricted::{Integrator, Model, Restricted, JUPITER, RTOL, RTOL_FINE};
use crate::sample;
use std::sync::OnceLock;

pub const PERIODS: usize = 200;
pub const COARSE: usize = 8;
pub const FINE: usize = 256;
pub const KEEP: usize = 16;
pub const CROSSINGS_MIN: usize = 20;
pub const ERR_MAX: f64 = 1e-4;
pub const FLOOR: f64 = 1e-12;
pub const CONVERGED: f64 = 1e-9;
pub const EXCLUDED_MAX: f64 = 0.1;
pub const GROWTH_MAX: f64 = 0.2;

/// The minimal slice of the gate's `Law` trait that B12 uses.
pub trait LawR {
    fn restricted(&self, scene: &Restricted, ship: [f64; 4], times: &[f64]) -> Option<Vec<[f64; 4]>>;
}

/// Verbatim from handoff.rs.
pub fn ship(scene: &Restricted, side: f64, k: f64, alpha: f64) -> [f64; 4] {
    let r = scene.sep * (1.0 + side * scene.hill() / scene.sep * k);
    let v = r.powf(-0.5);
    [r * alpha.cos(), r * alpha.sin(), -v * alpha.sin(), v * alpha.cos()]
}

/// Verbatim.
pub fn coarse_times(scene: &Restricted) -> Vec<f64> {
    (0..=PERIODS * COARSE).map(|j| j as f64 * scene.period() / COARSE as f64).collect()
}

pub struct Kept {
    pub ship: [f64; 4],
    pub crossings: usize,
    pub converged: bool,
    pub closest: f64,
}

impl Kept {
    fn judged(&self, scene: &Restricted) -> bool {
        self.converged && self.closest >= scene.planet_radius
    }
}

struct Assessed {
    crossings: usize,
    converged: bool,
    closest: f64,
}

/// Verbatim `watch`.
fn watch(scene: &Restricted, ship: [f64; 4], rtol: f64) -> Option<(usize, Vec<f64>, f64)> {
    let mut it = Integrator::new(scene, Model::Full, rtol, ship).tracking();
    let (mut inside, mut crossings, mut jacobi) = (None, 0, Vec::new());
    for j in 0..=PERIODS * FINE {
        let t = j as f64 * scene.period() / FINE as f64;
        let state = it.advance(t)?;
        let now = scene.planet_distance(t, &state) < scene.soi();
        crossings += inside.is_some_and(|before| before != now) as usize;
        inside = Some(now);
        if j % (FINE / COARSE) == 0 {
            jacobi.push(scene.jacobi(t, &state));
        }
    }
    Some((crossings, jacobi, it.closest()))
}

/// Verbatim `assess`.
fn assess(scene: &Restricted, ship: [f64; 4]) -> Option<Assessed> {
    let times = coarse_times(scene);
    let (crossings, reference, closest) = watch(scene, ship, RTOL)?;
    let c0 = scene.jacobi(0.0, &ship);
    let mut fine = Integrator::new(scene, Model::Full, RTOL_FINE, ship).tracking();
    let finer = times.iter().map(|&t| fine.advance(t)).collect::<Option<Vec<_>>>();
    let converged = finer.is_some_and(|f| f.iter().zip(&times).zip(&reference).all(|((s, &t), &c)| ((scene.jacobi(t, s) - c) / c0).abs() <= CONVERGED));
    Some(Assessed { crossings, converged, closest: closest.min(fine.closest()) })
}

/// Verbatim `kept`.
pub fn kept() -> &'static Vec<Kept> {
    static KEPT: OnceLock<Vec<Kept>> = OnceLock::new();
    KEPT.get_or_init(|| {
        let scene = JUPITER;
        let draws = sample::handoffs(sample::HANDOFF_KEPT.iter().max().map_or(0, |m| m + 1));
        sample::HANDOFF_KEPT
            .iter()
            .map(|&i| {
                let ship = ship(&scene, draws[i].0, draws[i].1, draws[i].2);
                let a = assess(&scene, ship).unwrap_or(Assessed { crossings: 0, converged: false, closest: 0.0 });
                Kept { ship, crossings: a.crossings, converged: a.converged, closest: a.closest }
            })
            .collect()
    })
}

/// The frozen ships the gate judges (kept ∧ converged ∧ outside the planet), in order.
pub fn judged_ships() -> Vec<&'static Kept> {
    let scene = JUPITER;
    kept().iter().filter(|k| k.judged(&scene)).collect()
}

/// Verbatim `err_series`.
pub fn err_series(scene: &Restricted, law: &dyn LawR, ship: [f64; 4], times: &[f64]) -> Vec<f64> {
    let c0 = scene.jacobi(0.0, &ship);
    match law.restricted(scene, ship, times) {
        Some(states) if states.len() == times.len() => states.iter().zip(times).map(|(s, &t)| ((scene.jacobi(t, s) - c0) / c0).abs()).collect(),
        _ => vec![f64::INFINITY; times.len()],
    }
}

/// Verbatim `median`.
pub fn median(mut xs: Vec<f64>) -> f64 {
    xs.iter_mut().for_each(|x| *x = if x.is_nan() { f64::INFINITY } else { *x });
    xs.sort_by(f64::total_cmp);
    match xs.len() {
        0 => f64::INFINITY,
        n if n % 2 == 1 => xs[n / 2],
        n => 0.5 * (xs[n / 2 - 1] + xs[n / 2]),
    }
}
