//! Executable physical-law experiments. Nothing in this crate is a production
//! exact-gravity implementation: each finite map has its own version, the
//! numerical gates are frozen in `scenarios/law-gates.json`, and promotion also
//! requires capabilities these stationary candidates do not have.

use serde::{Deserialize, Serialize};
use std::f64::consts::{PI, TAU};

const MANIFEST: &str = include_str!("../../../scenarios/law-gates.json");

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct QualificationReport {
    pub schema_version: u32,
    pub gate_manifest_digest: String,
    pub status: String,
    pub production_law: Option<String>,
    pub candidates: Vec<CandidateReport>,
    pub scope_notes: Vec<String>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CandidateReport {
    pub id: String,
    pub version: u32,
    pub status: String,
    pub metrics: Vec<Metric>,
    pub gates: Vec<GateResult>,
    pub evidence: Vec<String>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Metric {
    pub scenario: String,
    pub name: String,
    pub value: f64,
    pub unit: String,
    pub threshold: f64,
    pub passed: bool,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct GateResult {
    pub id: String,
    pub passed: bool,
    pub reason: String,
}

#[derive(Clone, Deserialize)]
struct Config {
    units: Units,
    quanta: Vec<f64>,
    rotations_radians: Vec<f64>,
    orbit_scenarios: Vec<OrbitScenario>,
    stationary_metric: MetricConfig,
    aggregate_gates: AggregateGates,
    required_production_gates: Vec<String>,
}

#[derive(Clone, Deserialize)]
struct Units {
    gravitational_parameter: f64,
    semimajor_axis: f64,
    light_speed: f64,
}

#[derive(Clone, Deserialize)]
struct OrbitScenario {
    id: String,
    eccentricity: f64,
    periods: u32,
    dt: f64,
    energy_drift_max: f64,
    angular_momentum_drift_max: f64,
    radial_envelope_error_max: f64,
    period_relative_error_max: f64,
}

#[derive(Clone, Deserialize)]
struct MetricConfig {
    shell_width: f64,
    minimum_radius: f64,
    maximum_radius: f64,
    maximum_crossings_per_step: usize,
}

#[derive(Clone, Deserialize)]
struct AggregateGates {
    angular_radial_spread_max: f64,
    angular_energy_spread_max: f64,
    quantum_envelope_change_max: f64,
    quantum_energy_growth_factor_max: f64,
    quantum_energy_growth_floor: f64,
    stationary_clock_absolute_error_max: f64,
    source_tree_bound_ratio_max: f64,
    backreaction_relative_error_max: f64,
    momentum_balance_absolute_error_max: f64,
    pre_lightcone_response_max: f64,
}

#[derive(Clone, Copy, Debug, Serialize, Deserialize)]
pub struct PhasePoint {
    pub position: [f64; 2],
    /// Unit-mass Newtonian momentum for VV; local spatial momentum for lapse.
    pub momentum: [f64; 2],
}

fn add(a: [f64; 2], b: [f64; 2]) -> [f64; 2] {
    [a[0] + b[0], a[1] + b[1]]
}
fn sub(a: [f64; 2], b: [f64; 2]) -> [f64; 2] {
    [a[0] - b[0], a[1] - b[1]]
}
fn scale(a: [f64; 2], s: f64) -> [f64; 2] {
    [a[0] * s, a[1] * s]
}
fn dot(a: [f64; 2], b: [f64; 2]) -> f64 {
    a[0] * b[0] + a[1] * b[1]
}
fn norm(a: [f64; 2]) -> f64 {
    dot(a, a).sqrt()
}
fn cross(a: [f64; 2], b: [f64; 2]) -> f64 {
    a[0] * b[1] - a[1] * b[0]
}
fn quantize(x: f64, q: f64) -> f64 {
    (x / q).round_ties_even() * q
}
fn quantize_state(mut s: PhasePoint, q: f64) -> PhasePoint {
    for i in 0..2 {
        s.position[i] = quantize(s.position[i], q);
        s.momentum[i] = quantize(s.momentum[i], q);
    }
    s
}
fn finite(s: PhasePoint) -> bool {
    s.position.into_iter().chain(s.momentum).all(f64::is_finite)
}

/// Newtonian inverse-square acceleration: the *three-dimensional* 1/r
/// potential restricted to a plane, not the logarithmic 2D gravity kernel.
pub fn gravitational_acceleration(position: [f64; 2], mu: f64) -> Result<[f64; 2], String> {
    let r2 = dot(position, position);
    if !r2.is_finite() || r2 <= 0.0 || !mu.is_finite() || mu < 0.0 {
        return Err("invalid or singular stationary source query".into());
    }
    Ok(scale(position, -mu / (r2 * r2.sqrt())))
}

/// `stationary-verlet-q-v1`: one velocity-Verlet map followed by one specified
/// nearest-even projection of position and momentum. The unprojected map is a
/// discrete variational integrator; projection generally destroys its exact
/// symplectic and reversal properties. Quantization happens at this law-defined
/// step boundary, never at diagnostic queries.
pub fn stationary_verlet_step(
    s: PhasePoint,
    dt: f64,
    q: f64,
    mu: f64,
) -> Result<PhasePoint, String> {
    if !(dt > 0.0 && q > 0.0 && dt.is_finite() && q.is_finite() && finite(s)) {
        return Err("invalid stationary Verlet input".into());
    }
    let half = add(
        s.momentum,
        scale(gravitational_acceleration(s.position, mu)?, 0.5 * dt),
    );
    let position = add(s.position, scale(half, dt));
    let momentum = add(
        half,
        scale(gravitational_acceleration(position, mu)?, 0.5 * dt),
    );
    let result = quantize_state(PhasePoint { position, momentum }, q);
    if finite(result) {
        Ok(result)
    } else {
        Err("nonfinite stationary Verlet result".into())
    }
}

#[derive(Clone, Copy)]
enum Candidate {
    Verlet,
    Lapse,
}

impl Candidate {
    fn id(self) -> &'static str {
        match self {
            Self::Verlet => "stationary-verlet-q-v1",
            Self::Lapse => "stationary-shell-lapse-q-v1",
        }
    }
}

fn config() -> Config {
    serde_json::from_str(MANIFEST).expect("checked-in frozen law manifest")
}

fn shell_index(r: f64, cfg: &Config) -> Result<i64, String> {
    if !r.is_finite()
        || r < cfg.stationary_metric.minimum_radius
        || r >= cfg.stationary_metric.maximum_radius
    {
        return Err(format!(
            "stationary lapse radius {r} outside finite laboratory domain"
        ));
    }
    Ok((r / cfg.stationary_metric.shell_width).floor() as i64)
}

fn lapse_at_shell(index: i64, mu: f64, cfg: &Config) -> Result<f64, String> {
    let radius = (index as f64 + 0.5) * cfg.stationary_metric.shell_width;
    if radius < cfg.stationary_metric.minimum_radius
        || radius >= cfg.stationary_metric.maximum_radius
    {
        return Err("stationary lapse crossing outside finite laboratory domain".into());
    }
    let square = 1.0 - 2.0 * mu / (cfg.units.light_speed.powi(2) * radius);
    if square <= 0.0 || !square.is_finite() {
        return Err("stationary lapse has no supported real timelike Hamiltonian here".into());
    }
    Ok(square.sqrt())
}

fn lapse_hamiltonian(s: PhasePoint, cfg: &Config) -> Result<f64, String> {
    let alpha = lapse_at_shell(
        shell_index(norm(s.position), cfg)?,
        cfg.units.gravitational_parameter,
        cfg,
    )?;
    let c2 = cfg.units.light_speed.powi(2);
    Ok(alpha * c2 * (1.0 + dot(s.momentum, s.momentum) / c2).sqrt())
}

/// Earliest future intersection with a circle in the requested radial direction.
/// This is an analytic floating diagnostic, not an exact root certificate.
fn circle_crossing(x: [f64; 2], v: [f64; 2], radius: f64, outward: bool) -> Option<f64> {
    let a = dot(v, v);
    if a <= 0.0 {
        return None;
    }
    let b = dot(x, v);
    let discriminant = b * b - a * (dot(x, x) - radius * radius);
    if discriminant < 0.0 {
        return None;
    }
    let d = discriminant.sqrt();
    let mut result = None;
    // q-form avoids cancellation for the small root near a boundary.
    let qr = -b - d.copysign(b);
    let roots = if qr == 0.0 {
        [-b / a, -b / a]
    } else {
        [qr / a, (dot(x, x) - radius * radius) / qr]
    };
    for t in roots {
        if t <= 1e-12 || !t.is_finite() {
            continue;
        }
        let radial = dot(add(x, scale(v, t)), v);
        if ((outward && radial > 0.0) || (!outward && radial < 0.0))
            && result.is_none_or(|old| t < old)
        {
            result = Some(t);
        }
    }
    result
}

/// `stationary-shell-lapse-q-v1`: ds²=-alpha_k² c²dt²+dx²+dy²,
/// alpha_k²=1-2mu/(c²(k+1/2)h). Inside each annulus the Hamiltonian
/// H=alpha_k c² sqrt(1+p²/c²) gives straight propagation. At a shell boundary
/// preserve H and tangential momentum; refract the radial momentum, or reflect
/// if the next shell is inaccessible. Reproject x,p once at each fixed dt.
/// Shell lookup after that projection is part of this experimental finite map.
fn lapse_step(mut s: PhasePoint, dt: f64, q: f64, cfg: &Config) -> Result<PhasePoint, String> {
    let mut band = shell_index(norm(s.position), cfg)?;
    let mut remaining = dt;
    let c2 = cfg.units.light_speed.powi(2);
    let h = cfg.stationary_metric.shell_width;
    for _ in 0..cfg.stationary_metric.maximum_crossings_per_step {
        let alpha = lapse_at_shell(band, cfg.units.gravitational_parameter, cfg)?;
        let gamma = (1.0 + dot(s.momentum, s.momentum) / c2).sqrt();
        let velocity = scale(s.momentum, alpha / gamma);
        let outer = circle_crossing(s.position, velocity, (band as f64 + 1.0) * h, true);
        let inner = circle_crossing(s.position, velocity, band as f64 * h, false);
        let next = match (outer, inner) {
            (Some(a), Some(b)) => Some(if a < b { (a, 1) } else { (b, -1) }),
            (Some(a), None) => Some((a, 1)),
            (None, Some(b)) => Some((b, -1)),
            _ => None,
        };
        if next.is_none_or(|(time, _)| time > remaining) {
            s.position = add(s.position, scale(velocity, remaining));
            let result = quantize_state(s, q);
            shell_index(norm(result.position), cfg)?;
            return if finite(result) {
                Ok(result)
            } else {
                Err("nonfinite lapse map result".into())
            };
        }
        let (time, direction) = next.expect("crossing selected");
        s.position = add(s.position, scale(velocity, time));
        remaining -= time;
        let normal = scale(s.position, 1.0 / norm(s.position));
        let radial = dot(s.momentum, normal);
        let tangent = sub(s.momentum, scale(normal, radial));
        let next_alpha = lapse_at_shell(band + direction, cfg.units.gravitational_parameter, cfg)?;
        let energy_over_next = alpha * gamma / next_alpha;
        let next_radial_square =
            c2 * (energy_over_next * energy_over_next - 1.0) - dot(tangent, tangent);
        if next_radial_square >= 0.0 {
            s.momentum = add(
                tangent,
                scale(normal, next_radial_square.sqrt().copysign(radial)),
            );
            band += direction;
        } else {
            s.momentum = sub(s.momentum, scale(normal, 2.0 * radial));
        }
        if remaining <= 0.0 {
            return Ok(quantize_state(s, q));
        }
    }
    Err("stationary lapse finite crossing budget exhausted; no result accepted".into())
}

fn energy(candidate: Candidate, s: PhasePoint, cfg: &Config) -> Result<f64, String> {
    match candidate {
        Candidate::Verlet => Ok(0.5 * dot(s.momentum, s.momentum)
            - cfg.units.gravitational_parameter / norm(s.position)),
        Candidate::Lapse => Ok(lapse_hamiltonian(s, cfg)? - cfg.units.light_speed.powi(2)),
    }
}

#[derive(Clone, Debug)]
struct OrbitResult {
    energy_drift: f64,
    angular_drift: f64,
    radial_error: f64,
    period_error: f64,
    min_radius: f64,
    max_radius: f64,
    final_radius: f64,
    steps: usize,
}

fn orbit(
    candidate: Candidate,
    scenario: &OrbitScenario,
    q: f64,
    angle: f64,
    cfg: &Config,
) -> Result<OrbitResult, String> {
    let mu = cfg.units.gravitational_parameter;
    let a = cfg.units.semimajor_axis;
    let periapsis = a * (1.0 - scenario.eccentricity);
    let apoapsis = a * (1.0 + scenario.eccentricity);
    // Independent Kepler initial condition and period formula (vis-viva).
    let speed = (mu * (2.0 / periapsis - 1.0 / a)).sqrt();
    let period = TAU * (a.powi(3) / mu).sqrt();
    let mut s = PhasePoint {
        position: [periapsis * angle.cos(), periapsis * angle.sin()],
        momentum: [-speed * angle.sin(), speed * angle.cos()],
    };
    if matches!(candidate, Candidate::Lapse) {
        let alpha = lapse_at_shell(shell_index(periapsis, cfg)?, mu, cfg)?;
        // v=alpha p/sqrt(1+p²/c²), inverted for the same initial coordinate v.
        s.momentum = scale(
            s.momentum,
            1.0 / (alpha * alpha - speed * speed / cfg.units.light_speed.powi(2)).sqrt(),
        );
    }
    s = quantize_state(s, q);
    let initial_energy = energy(candidate, s, cfg)?;
    let initial_angular = cross(s.position, s.momentum);
    let steps = (period * scenario.periods as f64 / scenario.dt).ceil() as usize;
    let mut result = OrbitResult {
        energy_drift: 0.0,
        angular_drift: 0.0,
        radial_error: 0.0,
        period_error: 0.0,
        min_radius: norm(s.position),
        max_radius: norm(s.position),
        final_radius: 0.0,
        steps,
    };
    let mut unwrapped_angle = 0.0;
    let mut previous_angle = s.position[1].atan2(s.position[0]);
    let mut crossings = Vec::new();
    for step in 1..=steps {
        s = match candidate {
            Candidate::Verlet => stationary_verlet_step(s, scenario.dt, q, mu)?,
            Candidate::Lapse => lapse_step(s, scenario.dt, q, cfg)?,
        };
        if !finite(s) {
            return Err("orbit produced nonfinite state".into());
        }
        let r = norm(s.position);
        result.min_radius = result.min_radius.min(r);
        result.max_radius = result.max_radius.max(r);
        result.energy_drift = result
            .energy_drift
            .max((energy(candidate, s, cfg)? - initial_energy).abs() / initial_energy.abs());
        result.angular_drift = result
            .angular_drift
            .max((cross(s.position, s.momentum) - initial_angular).abs() / initial_angular.abs());
        let current_angle = s.position[1].atan2(s.position[0]);
        let delta = (current_angle - previous_angle + PI).rem_euclid(TAU) - PI;
        let old = unwrapped_angle;
        unwrapped_angle += delta;
        let target = TAU * (crossings.len() + 1) as f64;
        if old < target && unwrapped_angle >= target {
            crossings.push(((step - 1) as f64 + (target - old) / delta) * scenario.dt);
        }
        previous_angle = current_angle;
    }
    result.radial_error = ((result.min_radius - periapsis)
        .abs()
        .max((result.max_radius - apoapsis).abs()))
        / a;
    result.final_radius = norm(s.position);
    // Use every completed revolution; no selection of a favorable crossing.
    if crossings.is_empty() {
        return Err("orbit did not complete one revolution".into());
    }
    for (i, arrival) in crossings.iter().enumerate() {
        result.period_error = result
            .period_error
            .max((arrival / (i + 1) as f64 / period - 1.0).abs());
    }
    Ok(result)
}

fn metric(
    report: &mut CandidateReport,
    scenario: impl Into<String>,
    name: &str,
    value: f64,
    unit: &str,
    threshold: f64,
) -> bool {
    let passed = value.is_finite() && value <= threshold;
    // Nonfinite outputs become explicit failed gates rather than invalid JSON.
    if value.is_finite() {
        report.metrics.push(Metric {
            scenario: scenario.into(),
            name: name.into(),
            value,
            unit: unit.into(),
            threshold,
            passed,
        });
    } else {
        gate(
            report,
            name,
            false,
            "nonfinite diagnostic value; no numeric result accepted",
        );
    }
    passed
}

fn gate(report: &mut CandidateReport, id: &str, passed: bool, reason: impl Into<String>) {
    report.gates.push(GateResult {
        id: id.into(),
        passed,
        reason: reason.into(),
    });
}

#[derive(Clone, Copy, Debug)]
pub struct PointSource {
    pub mass: f64,
    pub position: [f64; 2],
}

/// Floating direct-source oracle, including every positive source mass.
pub fn direct_acceleration(sources: &[PointSource], target: [f64; 2]) -> Result<[f64; 2], String> {
    let mut sum = [0.0, 0.0];
    for source in sources {
        sum = sub(
            sum,
            gravitational_acceleration(sub(source.position, target), source.mass)?,
        );
    }
    Ok(sum)
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct TreeEvaluation {
    pub acceleration: [f64; 2],
    pub absolute_error_bound: f64,
    pub accepted_nodes: usize,
    pub direct_sources: usize,
}

/// A bounded monopole quadtree diagnostic, explicitly NOT FMM.
/// For source support radius a, target-COM distance d>a, the 1/r field
/// Jacobian has norm <=2/(d-a)^3. Thus replacing a node by its monopole
/// has error <=2 M a/(d-a)^3. The analytic truncation bound is sound in
/// real arithmetic; the floating padding here is diagnostic, not a formal
/// directed-rounding proof for a production certificate.
pub fn bounded_monopole_tree(
    sources: &[PointSource],
    target: [f64; 2],
) -> Result<TreeEvaluation, String> {
    fn recurse(
        sources: &[PointSource],
        target: [f64; 2],
        depth: usize,
    ) -> Result<TreeEvaluation, String> {
        if sources.is_empty() {
            return Ok(TreeEvaluation {
                acceleration: [0.0, 0.0],
                absolute_error_bound: 0.0,
                accepted_nodes: 0,
                direct_sources: 0,
            });
        }
        let mass: f64 = sources.iter().map(|s| s.mass).sum();
        if mass <= 0.0 || sources.iter().any(|s| s.mass <= 0.0 || !s.mass.is_finite()) {
            return Err("tree requires finite positive masses".into());
        }
        let center = scale(
            sources
                .iter()
                .fold([0.0, 0.0], |sum, s| add(sum, scale(s.position, s.mass))),
            1.0 / mass,
        );
        let radius = sources
            .iter()
            .map(|s| norm(sub(s.position, center)))
            .fold(0.0, f64::max);
        let distance = norm(sub(target, center));
        if sources.len() > 1 && distance > radius && radius / distance < 0.2 {
            let acceleration = direct_acceleration(
                &[PointSource {
                    mass,
                    position: center,
                }],
                target,
            )?;
            let truncation = 2.0 * mass * radius / (distance - radius).powi(3);
            let pad = 128.0 * f64::EPSILON * (1.0 + norm(acceleration) + truncation);
            return Ok(TreeEvaluation {
                acceleration,
                absolute_error_bound: truncation + pad,
                accepted_nodes: 1,
                direct_sources: 0,
            });
        }
        if sources.len() <= 4 || depth >= 24 || radius == 0.0 {
            let acceleration = direct_acceleration(sources, target)?;
            return Ok(TreeEvaluation {
                acceleration,
                absolute_error_bound: 128.0
                    * sources.len() as f64
                    * f64::EPSILON
                    * (1.0 + norm(acceleration)),
                accepted_nodes: 0,
                direct_sources: sources.len(),
            });
        }
        let mut children = [Vec::new(), Vec::new(), Vec::new(), Vec::new()];
        for s in sources {
            let index = usize::from(s.position[0] >= center[0])
                + 2 * usize::from(s.position[1] >= center[1]);
            children[index].push(*s);
        }
        let mut result = TreeEvaluation {
            acceleration: [0.0, 0.0],
            absolute_error_bound: 0.0,
            accepted_nodes: 0,
            direct_sources: 0,
        };
        for child in children {
            let part = recurse(&child, target, depth + 1)?;
            result.acceleration = add(result.acceleration, part.acceleration);
            result.absolute_error_bound += part.absolute_error_bound;
            result.accepted_nodes += part.accepted_nodes;
            result.direct_sources += part.direct_sources;
        }
        Ok(result)
    }
    recurse(sources, target, 0)
}

fn qualify_sources(report: &mut CandidateReport, cfg: &Config) {
    let mut worst_ratio: f64 = 0.0;
    let mut tested = 0;
    let mut accepted = 0;
    let fixtures = [
        (0..64)
            .map(|i| PointSource {
                mass: 1.0 / 64.0,
                position: [
                    0.01 * (i as f64 * TAU / 64.0).cos(),
                    0.01 * (i as f64 * TAU / 64.0).sin(),
                ],
            })
            .collect::<Vec<_>>(),
        (0..65)
            .map(|i| PointSource {
                mass: if i == 0 { 1e9 } else { 1e-6 },
                position: [0.03 * i as f64, 0.001 * ((i * 17) % 23) as f64],
            })
            .collect(),
        (0..128)
            .map(|i| PointSource {
                mass: 0.1 + (i % 7) as f64,
                position: [
                    ((i * 37) % 101) as f64 / 20.0 - 2.5,
                    ((i * 61) % 103) as f64 / 20.0 - 2.5,
                ],
            })
            .collect(),
    ];
    for (i, sources) in fixtures.iter().enumerate() {
        for target in [[0.123, 0.789], [3.0, 2.0], [10.0, -1.0], [-80.0, 50.0]] {
            match (
                direct_acceleration(sources, target),
                bounded_monopole_tree(sources, target),
            ) {
                (Ok(direct), Ok(tree)) => {
                    let ratio = norm(sub(direct, tree.acceleration))
                        / tree.absolute_error_bound.max(f64::MIN_POSITIVE);
                    worst_ratio = worst_ratio.max(ratio);
                    accepted += tree.accepted_nodes;
                    tested += 1;
                    metric(
                        report,
                        format!("source_fixture_{i}_target_{target:?}"),
                        "tree_error_to_bound",
                        ratio,
                        "ratio",
                        cfg.aggregate_gates.source_tree_bound_ratio_max,
                    );
                }
                _ => gate(
                    report,
                    "source_fixture_execution",
                    false,
                    "source fixture failed to evaluate",
                ),
            }
        }
    }
    gate(report, "source_tree_bound", tested == 12 && accepted > 0 && worst_ratio <= cfg.aggregate_gates.source_tree_bound_ratio_max,
        format!("{tested} direct/tree queries; {accepted} accepted monopole nodes; worst observed error/bound={worst_ratio:.6e}. Analytic truncation plus floating diagnostic padding; not a certified FMM."));

    let ship = PointSource {
        mass: 1.0,
        position: [2.0, 0.0],
    };
    let single = direct_acceleration(&[ship], [-2.0, 0.0]).expect("nonsingular fixture");
    let fleet = direct_acceleration(&vec![ship; 64], [-2.0, 0.0]).expect("nonsingular fixture");
    let ratio_error = (norm(fleet) / norm(single) / 64.0 - 1.0).abs();
    let star_mass = 1000.0;
    let ship_acceleration = direct_acceleration(
        &[PointSource {
            mass: star_mass,
            position: [-2.0, 0.0],
        }],
        ship.position,
    )
    .expect("nonsingular fixture");
    let force_residual = norm(add(
        scale(fleet, star_mass),
        scale(ship_acceleration, 64.0 * ship.mass),
    ));
    let passed = metric(
        report,
        "backreaction",
        "fleet_acceleration_scaling_error",
        ratio_error,
        "relative",
        cfg.aggregate_gates.backreaction_relative_error_max,
    ) & metric(
        report,
        "backreaction",
        "total_force_residual",
        force_residual,
        "force",
        cfg.aggregate_gates.momentum_balance_absolute_error_max,
    );
    gate(report, "source_backreaction", passed,
        format!("Direct two-way source experiment: star acceleration {} for one ship and {} for 64; total pair-force residual {force_residual}. This source evaluator is not dynamically coupled into either stationary orbit map.", norm(single), norm(fleet)));
}

fn qualify_candidate(candidate: Candidate, cfg: &Config) -> CandidateReport {
    let mut report = CandidateReport {
        id: candidate.id().into(),
        version: 1,
        status: "FAIL".into(),
        metrics: Vec::new(),
        gates: Vec::new(),
        evidence: Vec::new(),
    };
    let mut all_orbits = true;
    let mut isotropy = true;
    let mut quantum = true;
    let mut total_steps = 0;
    for scenario in &cfg.orbit_scenarios {
        let mut by_quantum = Vec::new();
        for (qi, q) in cfg.quanta.iter().copied().enumerate() {
            let mut by_angle = Vec::new();
            for (ai, angle) in cfg.rotations_radians.iter().copied().enumerate() {
                let label = format!("{}_q{qi}_rotation{ai}", scenario.id);
                match orbit(candidate, scenario, q, angle, cfg) {
                    Ok(result) => {
                        total_steps += result.steps;
                        all_orbits &= metric(
                            &mut report,
                            &label,
                            "maximum_energy_drift",
                            result.energy_drift,
                            "relative",
                            scenario.energy_drift_max,
                        );
                        all_orbits &= metric(
                            &mut report,
                            &label,
                            "maximum_angular_momentum_drift",
                            result.angular_drift,
                            "relative",
                            scenario.angular_momentum_drift_max,
                        );
                        all_orbits &= metric(
                            &mut report,
                            &label,
                            "radial_envelope_error",
                            result.radial_error,
                            "semimajor_axis",
                            scenario.radial_envelope_error_max,
                        );
                        all_orbits &= metric(
                            &mut report,
                            &label,
                            "revolution_period_error",
                            result.period_error,
                            "relative",
                            scenario.period_relative_error_max,
                        );
                        by_angle.push(result);
                    }
                    Err(error) => {
                        all_orbits = false;
                        isotropy = false;
                        quantum = false;
                        gate(&mut report, &format!("{label}_execution"), false, error);
                    }
                }
            }
            if by_angle.len() == cfg.rotations_radians.len() {
                let spread = |extract: fn(&OrbitResult) -> f64| -> f64 {
                    let min = by_angle.iter().map(extract).fold(f64::INFINITY, f64::min);
                    let max = by_angle
                        .iter()
                        .map(extract)
                        .fold(f64::NEG_INFINITY, f64::max);
                    max - min
                };
                isotropy &= metric(
                    &mut report,
                    format!("{}_q{qi}", scenario.id),
                    "rotated_final_radius_spread",
                    spread(|r| r.final_radius),
                    "length",
                    cfg.aggregate_gates.angular_radial_spread_max,
                );
                isotropy &= metric(
                    &mut report,
                    format!("{}_q{qi}", scenario.id),
                    "rotated_energy_drift_spread",
                    spread(|r| r.energy_drift),
                    "relative",
                    cfg.aggregate_gates.angular_energy_spread_max,
                );
                by_quantum.push(by_angle);
            }
        }
        if by_quantum.len() == cfg.quanta.len() {
            for qi in 1..by_quantum.len() {
                for ai in 0..cfg.rotations_radians.len() {
                    let coarse = &by_quantum[qi - 1][ai];
                    let fine = &by_quantum[qi][ai];
                    let change = (fine.min_radius - coarse.min_radius)
                        .abs()
                        .max((fine.max_radius - coarse.max_radius).abs());
                    quantum &= metric(
                        &mut report,
                        format!("{}_q{}-q{}_rotation{ai}", scenario.id, qi - 1, qi),
                        "quantum_radial_envelope_change",
                        change,
                        "length",
                        cfg.aggregate_gates.quantum_envelope_change_max,
                    );
                    quantum &= metric(
                        &mut report,
                        format!("{}_q{}-q{}_rotation{ai}", scenario.id, qi - 1, qi),
                        "refined_energy_drift",
                        fine.energy_drift,
                        "relative",
                        coarse.energy_drift * cfg.aggregate_gates.quantum_energy_growth_factor_max
                            + cfg.aggregate_gates.quantum_energy_growth_floor,
                    );
                }
            }
        } else {
            quantum = false;
        }
    }
    gate(&mut report, "orbit_stability", all_orbits, "All frozen regular/eccentric orbit, period, energy, angular momentum and radial envelope gates must pass; analytic Kepler formulas are independent diagnostics, not the canonical law.");
    gate(
        &mut report,
        "angular_isotropy",
        isotropy,
        "Same initial orbit rotated by 0, pi/8 and pi/4, with every frozen quantum included.",
    );
    gate(
        &mut report,
        "quantum_refinement",
        quantum,
        "Compare q,q/2,q/4 radial envelopes and drift; no chaotic coordinate-equality requirement.",
    );
    report.evidence.push(format!(
        "Executed {total_steps} finite-map steps across {} orbit/quantum/orientation scenarios.",
        cfg.orbit_scenarios.len() * cfg.quanta.len() * cfg.rotations_radians.len()
    ));

    let mut clock_passed = true;
    for radius in [0.4, 1.0, 1.6, 4.0] {
        let reference = (1.0
            - 2.0 * cfg.units.gravitational_parameter / (cfg.units.light_speed.powi(2) * radius))
            .sqrt();
        let candidate_rate = match candidate {
            Candidate::Verlet => 1.0,
            Candidate::Lapse => lapse_at_shell(
                shell_index(radius, cfg).expect("clock fixture in domain"),
                cfg.units.gravitational_parameter,
                cfg,
            )
            .expect("clock fixture real"),
        };
        clock_passed &= metric(
            &mut report,
            format!("stationary_clock_r{radius}"),
            "proper_time_rate_error",
            (candidate_rate - reference).abs(),
            "d_tau/d_t",
            cfg.aggregate_gates.stationary_clock_absolute_error_max,
        );
    }
    gate(&mut report, "stationary_clock", clock_passed, match candidate {
        Candidate::Verlet => "Newtonian time has d_tau/d_t=1 and fails the stationary relativistic-clock gate.",
        Candidate::Lapse => "Compare piecewise lapse against sqrt(1-2mu/(c²r)); this tests the chosen stationary lapse, not full Schwarzschild spatial geometry or dynamic GR.",
    });
    qualify_sources(&mut report, cfg);

    // A concrete counterexample: mutate mu at t=0, query r=4 at one
    // quarter of its light-travel time. These stationary query formulas
    // respond immediately; neither implements retarded source histories.
    let radius = 4.0;
    let before = match candidate {
        Candidate::Verlet => norm(gravitational_acceleration([radius, 0.0], 1.0).unwrap()),
        Candidate::Lapse => lapse_at_shell(shell_index(radius, cfg).unwrap(), 1.0, cfg).unwrap(),
    };
    let after = match candidate {
        Candidate::Verlet => norm(gravitational_acceleration([radius, 0.0], 2.0).unwrap()),
        Candidate::Lapse => lapse_at_shell(shell_index(radius, cfg).unwrap(), 2.0, cfg).unwrap(),
    };
    let response = (after - before).abs();
    let causality = metric(
        &mut report,
        "mass_change_before_lightcone",
        "pre_lightcone_response",
        response,
        "acceleration_or_clock_rate",
        cfg.aggregate_gates.pre_lightcone_response_max,
    );
    gate(&mut report, "causal_dynamic_sources", causality, format!("Counterexample: source mu 1->2 at t=0; radius={radius}; query t={} < arrival {} responds by {response:.12e}. Static formulas lack retarded source histories and coupled field evolution.", radius / cfg.units.light_speed / 4.0, radius / cfg.units.light_speed));
    let exterior_effect = norm(
        direct_acceleration(
            &[PointSource {
                mass: 1.0,
                position: [16.0, 0.0],
            }],
            [1.0, 0.0],
        )
        .unwrap(),
    );
    gate(&mut report, "well_posed_exterior", false, format!("No infinite-universe source measure, initial field or certified tail is specified. Adding a unit source outside the finite r<8 laboratory changes acceleration at r=1 by {exterior_effect:.12e}; omitting it cannot be certified. A finite authoritative massive root is the next allowed model, not an implicit infinity."));
    gate(&mut report, "compact_field_certification", false, match candidate {
        Candidate::Verlet => "The 1/r Newtonian map has a singular r=0 force and no light deflection, horizon or stationary compact-field branch evaluator.",
        Candidate::Lapse => "The finite r>=1/16 lapse laboratory does not reach the compact radius 2mu/c², and its Euclidean spatial metric is not Schwarzschild/Kerr. No compact-field certification is inferred from clock agreement.",
    });
    gate(&mut report, "terminating_exact_branches", false, "Both maps and root calculations use f64 candidates. The crossing cap terminates with an error, not a certified result; no exact arithmetic/enclosure verifier exists for these physical laws. They cannot define production branch truth.");
    report.evidence.push("The source tree is a monopole quadtree with an explicit analytic truncation bound. It is not FMM; floating arithmetic error is not formally certified.".into());
    report.evidence.push("The stationary source is an external fixed field in both orbit experiments. The separate direct backreaction experiment does not grant either map dynamic coupled-source support.".into());
    report.evidence.push("Neither orbital step count nor elapsed simulated time is an integrated billion-year/billion-ship qualification.".into());
    let complete = cfg
        .required_production_gates
        .iter()
        .all(|id| report.gates.iter().any(|g| &g.id == id && g.passed))
        && report.gates.iter().all(|g| g.passed)
        && report.metrics.iter().all(|m| m.passed);
    if complete {
        report.status = "PASS".into();
    }
    report
}

/// Execute the frozen G2 laboratory suite. This is intentionally real numerical
/// work (hundreds of thousands of steps per candidate), not a capability stub.
/// No filesystem mutation, clocks or scheduler-dependent random state is used.
pub fn qualify() -> QualificationReport {
    let cfg = config();
    let candidates = [Candidate::Verlet, Candidate::Lapse]
        .into_iter()
        .map(|candidate| qualify_candidate(candidate, &cfg))
        .collect::<Vec<_>>();
    let production_law = candidates
        .iter()
        .find(|c| c.status == "PASS")
        .map(|c| c.id.clone());
    QualificationReport {
        schema_version: 1,
        gate_manifest_digest: blake3::hash(MANIFEST.as_bytes()).to_hex().to_string(),
        status: if production_law.is_some() { "PASS" } else { "FAIL" }.into(),
        production_law,
        candidates,
        scope_notes: vec![
            "Gate manifest was frozen before these two candidate implementations; law versions never change with optimizer selection.".into(),
            "The suite is a bounded CPU physical-law experiment, suitable for the M1/8GB development target; it is not a performance qualification.".into(),
            "Quantization is a projected finite-map experiment. f64/libm results are not claimed bitwise portable or production exact.".into(),
            "Production promotion requires every frozen numerical and capability gate; physical failures and missing proofs remain visible.".into(),
        ],
    }
}

pub fn gate_manifest() -> &'static str {
    MANIFEST
}

/// Isolated coupled source-response experiment. Not selected as `production_law`.
/// Diagnostic `Engine::advance` may poll its jobs; that is not canonical gravity.
pub mod coupled_source_response;
pub use coupled_source_response::COUPLED_RESPONSE_LAW_ID;
/// Independent interval contraction/enclosure. Does not share the compile residual.
pub mod coupled_interval_enclosure;
/// Compact phase/residual stored response and navigation inversion on the GEM slice.
/// Not `production_law`. Diagnostic advance may skip this sidecar.
pub mod coupled_phase_nav;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn inverse_square_kernel_is_three_dimensional_restricted_to_plane() {
        let acceleration = gravitational_acceleration([3.0, 4.0], 10.0).unwrap();
        assert!((acceleration[0] + 0.24).abs() < 1e-15);
        assert!((acceleration[1] + 0.32).abs() < 1e-15);
        assert!(
            (norm(gravitational_acceleration([6.0, 8.0], 10.0).unwrap()) / norm(acceleration)
                - 0.25)
                .abs()
                < 1e-15
        );
    }

    #[test]
    fn zero_mass_verlet_is_exact_ballistic_at_binary_boundaries() {
        let state = PhasePoint {
            position: [1.0, -2.0],
            momentum: [0.5, 0.25],
        };
        let next = stationary_verlet_step(state, 0.125, 1.0 / 1024.0, 0.0).unwrap();
        assert_eq!(next.position, [1.0625, -1.96875]);
        assert_eq!(next.momentum, state.momentum);
    }

    #[test]
    fn circular_orbit_is_checked_against_analytic_period_and_radius() {
        let cfg = config();
        let result = orbit(
            Candidate::Verlet,
            &cfg.orbit_scenarios[0],
            cfg.quanta[2],
            0.0,
            &cfg,
        )
        .unwrap();
        assert!(result.period_error < 0.01, "period {}", result.period_error);
        assert!(result.radial_error < 0.02, "radial {}", result.radial_error);
    }

    #[test]
    fn shell_free_flight_matches_its_hamiltonian_velocity() {
        let cfg = config();
        let s = PhasePoint {
            position: [1.003, 0.0],
            momentum: [0.0, 0.5],
        };
        let q = 2.0_f64.powi(-40);
        let dt = 2.0_f64.powi(-16);
        let alpha = (1.0 - 2.0 / (64.0_f64.powi(2) * (128.5 / 128.0))).sqrt();
        let expected_y = dt * alpha * 0.5 / (1.0 + 0.25 / 64.0_f64.powi(2)).sqrt();
        let next = lapse_step(s, dt, q, &cfg).unwrap();
        assert!((next.position[1] - expected_y).abs() <= q);
        assert_eq!(next.momentum, s.momentum);
    }

    #[test]
    fn analytic_circle_solver_finds_two_crossings_without_sampling() {
        let x = [-2.0, 0.0];
        let v = [4.0, 0.0];
        assert!((circle_crossing(x, v, 1.0, false).unwrap() - 0.25).abs() < 1e-15);
        assert!((circle_crossing(x, v, 1.0, true).unwrap() - 0.75).abs() < 1e-15);
    }

    #[test]
    fn monopole_bound_contains_independently_summed_asymmetric_sources() {
        let sources = [
            PointSource {
                mass: 2.0,
                position: [-0.2, 0.1],
            },
            PointSource {
                mass: 7.0,
                position: [0.4, -0.1],
            },
        ];
        let target = [10.0, 3.0];
        let tree = bounded_monopole_tree(&sources, target).unwrap();
        let direct = direct_acceleration(&sources, target).unwrap();
        assert_eq!(tree.accepted_nodes, 1);
        assert!(norm(sub(direct, tree.acceleration)) <= tree.absolute_error_bound);
    }

    #[test]
    fn frozen_manifest_has_all_three_quanta_and_both_regimes() {
        let cfg = config();
        assert_eq!(cfg.quanta.len(), 3);
        assert_eq!(cfg.quanta[0], cfg.quanta[1] * 2.0);
        assert_eq!(cfg.quanta[1], cfg.quanta[2] * 2.0);
        assert_eq!(cfg.orbit_scenarios.len(), 2);
        assert_eq!(cfg.aggregate_gates.pre_lightcone_response_max, 0.0);
    }

    #[test]
    fn stationary_source_counterexample_really_changes_before_signal_arrival() {
        let initial = gravitational_acceleration([4.0, 0.0], 1.0).unwrap();
        let changed = gravitational_acceleration([4.0, 0.0], 2.0).unwrap();
        assert_eq!(norm(sub(changed, initial)), 1.0 / 16.0);
    }
}
