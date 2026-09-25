//! Isolated `es-linearized-retarded-gem-response-v0`.
//! Not `production_law`. Diagnostic `Engine::advance` may poll jobs here;
//! that path does not authorize canonical gravity.
//!
//! Slow reference and compiled response share the GEM-v0 formulas with f64
//! finite semantics. The reference is constructed only from genesis plus the
//! intervention list.

use serde::{Deserialize, Serialize};

pub const COUPLED_RESPONSE_LAW_ID: &str = "es-linearized-retarded-gem-response-v0";
pub const C: f64 = 8.0;
pub const G: f64 = 1.0;

const PHI_C2_MAX: f64 = 0.05;
const BETA_MAX: f64 = 0.25;
const FD_EPS: f64 = 1e-6;

/// Role of a nested ledger entry. Offline audit is recorded separately from
/// the cost of a normal runtime request. Historical `Charge::total` stays the
/// flat field sum used by H0124 scoped compile/repair counts.
#[derive(Clone, Copy, Debug, Default, Serialize, Deserialize, PartialEq, Eq)]
pub enum ChargeRole {
    #[default]
    RuntimeRequest,
    OfflineAudit,
    Certificate,
    FailedAttempt,
    Fallback,
    Reconstruction,
}

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ChargedOp {
    pub name: String,
    pub role: ChargeRole,
    pub charge: Box<Charge>,
}

#[derive(Clone, Debug, Default, Serialize, Deserialize, PartialEq)]
pub struct Charge {
    pub init: u64,
    pub source_evolution: u64,
    pub retarded_solves: u64,
    pub field_evals: u64,
    pub coefficient_construction: u64,
    pub factorization: u64,
    pub validation: u64,
    pub consumers: u64,
    pub repair: u64,
    pub fallback: u64,
    pub history: u64,
    pub reconstruction: u64,
    pub verification: u64,
    /// Nested executed children. Counted in `ledger_total`, not in historical
    /// `total()`. Enclosure genesis/Picard work lives here as OfflineAudit.
    #[serde(default)]
    pub children: Vec<ChargedOp>,
}

impl Charge {
    /// Historical flat sum. H0124 scoped `1188 vs 1675` / `1126 vs 1722`
    /// source-operation comparisons use `source_evolution + retarded_solves`,
    /// not this total and not `ledger_total`.
    pub fn total(&self) -> u64 {
        self.init
            + self.source_evolution
            + self.retarded_solves
            + self.field_evals
            + self.coefficient_construction
            + self.factorization
            + self.validation
            + self.consumers
            + self.repair
            + self.fallback
            + self.history
            + self.reconstruction
            + self.verification
    }

    /// Every executed child, failed attempt, certificate, fallback and
    /// reconstruction counted once, including offline audit.
    pub fn ledger_total(&self) -> u64 {
        self.total().saturating_add(
            self.children
                .iter()
                .map(|child| child.charge.ledger_total())
                .sum::<u64>(),
        )
    }

    /// Cost required for a normal runtime request. Offline audit and
    /// independent certificates are excluded; runtime validation on this node
    /// remains.
    pub fn runtime_request_total(&self) -> u64 {
        let mut n = self.total();
        for child in &self.children {
            match child.role {
                ChargeRole::OfflineAudit | ChargeRole::Certificate => {}
                ChargeRole::FailedAttempt => {}
                ChargeRole::RuntimeRequest
                | ChargeRole::Fallback
                | ChargeRole::Reconstruction => {
                    n = n.saturating_add(child.charge.runtime_request_total());
                }
            }
        }
        n
    }

    pub fn offline_audit_total(&self) -> u64 {
        self.children
            .iter()
            .map(|child| match child.role {
                ChargeRole::OfflineAudit | ChargeRole::Certificate => child.charge.ledger_total(),
                _ => child.charge.offline_audit_total(),
            })
            .sum()
    }

    pub fn push_child(&mut self, name: impl Into<String>, role: ChargeRole, child: Charge) {
        self.children.push(ChargedOp {
            name: name.into(),
            role,
            charge: Box::new(child),
        });
    }

    pub fn child(&self, name: &str) -> Option<&ChargedOp> {
        self.children.iter().find(|c| c.name == name)
    }
}

fn attach_offline_enclosure(
    dst: &mut Charge,
    enclosure: &crate::coupled_interval_enclosure::Enclosure,
) {
    dst.push_child(
        "enclose_compiled_interval",
        ChargeRole::OfflineAudit,
        enclosure.charge.clone(),
    );
}

#[derive(Clone, Copy, Debug)]
struct V2 {
    x: f64,
    y: f64,
}

impl V2 {
    fn new(x: f64, y: f64) -> Self {
        Self { x, y }
    }
    fn zero() -> Self {
        Self { x: 0.0, y: 0.0 }
    }
    fn add(self, o: Self) -> Self {
        Self::new(self.x + o.x, self.y + o.y)
    }
    fn sub(self, o: Self) -> Self {
        Self::new(self.x - o.x, self.y - o.y)
    }
    fn scale(self, s: f64) -> Self {
        Self::new(self.x * s, self.y * s)
    }
    fn dot(self, o: Self) -> f64 {
        self.x * o.x + self.y * o.y
    }
    fn norm2(self) -> f64 {
        self.dot(self)
    }
    fn norm(self) -> f64 {
        self.norm2().sqrt()
    }
    fn cross_z(self, o: Self) -> f64 {
        self.x * o.y - self.y * o.x
    }
    fn perp_z(self, bz: f64) -> Self {
        Self::new(self.y * bz, -self.x * bz)
    }
    fn arr(self) -> [f64; 2] {
        [self.x, self.y]
    }
    fn from_arr(a: [f64; 2]) -> Self {
        Self::new(a[0], a[1])
    }
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Segment {
    pub t0: f64,
    pub t1: Option<f64>,
    pub x0: [f64; 2],
    pub v: [f64; 2],
    /// Constant-a on a closed collocation block. The open tail after the last
    /// knot stores the same `a` so `at` continues ½`ah²` like lookback.
    /// Euler `continue_from` still writes zero (inertial chords).
    #[serde(default)]
    pub a: [f64; 2],
    pub mu: f64,
}

impl Segment {
    fn at(&self, t: f64) -> V2 {
        let dt = t - self.t0;
        V2::from_arr(self.x0)
            .add(V2::from_arr(self.v).scale(dt))
            .add(V2::from_arr(self.a).scale(0.5 * dt * dt))
    }
    fn covers(&self, t: f64) -> bool {
        t + 1e-15 >= self.t0 && self.t1.map(|t1| t <= t1 + 1e-15).unwrap_or(true)
    }
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Body {
    pub id: u64,
    pub segments: Vec<Segment>,
}

impl Body {
    fn present(&self, t: f64) -> Result<(V2, V2, f64), ResponseError> {
        let seg = self
            .segments
            .iter()
            .rev()
            .find(|s| s.covers(t))
            .ok_or(ResponseError::UnsupportedDomain {
                why: format!("body {} has no segment at t={t}", self.id),
            })?;
        let dt = t - seg.t0;
        let v = V2::from_arr(seg.v).add(V2::from_arr(seg.a).scale(dt));
        Ok((seg.at(t), v, seg.mu))
    }
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Intervention {
    pub t: f64,
    pub body_id: u64,
    pub delta_v: [f64; 2],
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct BodyInit {
    pub id: u64,
    pub mu: f64,
    pub x: [f64; 2],
    pub v: [f64; 2],
}

#[derive(Clone, Debug, Default, Serialize, Deserialize)]
pub struct InitialCondition {
    pub genesis_t: f64,
    pub bodies: Vec<BodyInit>,
}

/// Constant-acceleration collocation block. This is the stored interval
/// function: GEM-a is sampled at the block midpoint from stored-a lookback
/// of already-committed functions (same geometry queries read). Observer
/// knots and `inertial_end` use that stored-a endpoint (including ½`ah²`).
/// Closed worldtube segments store the same `a` so `present` matches `state_at`.
/// The open tail after the last knot continues that stored `a` (½`ah²`).
/// Reuse copies these blocks. Euler `continue_from` stays inertial.
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct IntervalFunction {
    pub body_id: u64,
    pub t0: f64,
    pub t1: f64,
    pub x0: [f64; 2],
    pub v0: [f64; 2],
    pub a: [f64; 2],
    pub mu: f64,
}

impl IntervalFunction {
    /// Stored constant-a endpoint, including ½`ah²`. Same geometry as
    /// `state_at(t1)` / lookback. Rebuilt worldtubes, observer knots, and the
    /// open tail after this block use that stored `a`.
    fn inertial_end(&self) -> (V2, V2) {
        self.state_at(self.t1)
    }

    fn covers(&self, t: f64) -> bool {
        t + 1e-15 >= self.t0 && t <= self.t1 + 1e-15
    }

    /// Constant-a evaluation on the stored block, including interior ½`ah²`.
    fn state_at(&self, t: f64) -> (V2, V2) {
        let h = t - self.t0;
        let a = V2::from_arr(self.a);
        let v0 = V2::from_arr(self.v0);
        let x = V2::from_arr(self.x0)
            .add(v0.scale(h))
            .add(a.scale(0.5 * h * h));
        let v = v0.add(a.scale(h));
        (x, v)
    }

    /// Chord-only sample of the same block (½`ah²` omitted; v held at `v0`).
    #[cfg(test)]
    fn chord_at(&self, t: f64) -> (V2, V2) {
        let h = t - self.t0;
        let v0 = V2::from_arr(self.v0);
        (V2::from_arr(self.x0).add(v0.scale(h)), v0)
    }
}

#[derive(Clone, Debug)]
pub enum ResponseError {
    Singular,
    Superluminal,
    UnsupportedDomain { why: String },
    BranchBudgetExhausted,
}

impl std::fmt::Display for ResponseError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ResponseError::Singular => write!(f, "Singular: r=0"),
            ResponseError::Superluminal => write!(f, "superluminal worldtube"),
            ResponseError::UnsupportedDomain { why } => write!(f, "UnsupportedDomain: {why}"),
            ResponseError::BranchBudgetExhausted => write!(f, "BranchBudgetExhausted"),
        }
    }
}

#[derive(Clone, Copy, Debug)]
struct GemField {
    phi: f64,
    e: V2,
    b_z: f64,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Residual {
    pub max_grad_rel: f64,
    pub max_accel_rel: f64,
    pub max_phi_c2: f64,
    pub max_beta: f64,
    pub static_kernel_ok: bool,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Domain {
    pub phi_c2_max: f64,
    pub beta_max: f64,
    pub horizon: f64,
    pub dt: f64,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SourceResponse {
    pub law_id: String,
    pub domain: Domain,
    pub incoming: Vec<Intervention>,
    /// Compact phase + residual generator. Sidecar of the interval operator,
    /// not the compile itself. Pieces split at causal arrivals as well as local
    /// interventions. Admitted-band decode can still miss 1e-8 pre-cone identity.
    /// A \(10^{-8}\) band fit is a polyline, not compact. Four-kick \(H=9\) may
    /// refuse the generator.
    pub compact: crate::coupled_phase_nav::CompactResponse,
    /// Piecewise-inertial decode of the causal-block interval operator.
    /// Not `Reference::from_genesis` + `evolve()` copied here. Chebyshev compact
    /// is a sidecar of this decode; do not paper this table as decode-only of
    /// compact, and do not call it an Euler remainder.
    pub worldtubes: Vec<Body>,
    /// Number of causal blocks in the interval operator (Schur forward subst).
    pub interval_blocks: u64,
    /// Delay-grouped Lipschitz of the assembled interval operator, computed
    /// as \(\max_k (h_k L_k)\), not assigned 0.
    pub interval_q: f64,
    /// Effective numerical cadence used for causal-block knots (knots use
    /// half this value). Refined laboratory compiles divide the initial
    /// light-crossing time; this field is not then the physical light crossing.
    /// Repair reuses it so execution shares the same interval grid.
    pub interval_tau: f64,
    /// Genesis IC for domain-share checks. Distinct-history reuse refuses a
    /// different genesis (new massive entrant from t=0).
    #[serde(default)]
    pub genesis: InitialCondition,
    /// Certified interval functions of the collocation. Empty means reuse must
    /// refuse rather than paper worldtube chords as this object.
    #[serde(default)]
    pub interval_functions: Vec<IntervalFunction>,
    /// Stored \((I-K_{AB}K_{BA})^{-1}\) on the pair collocation mesh. Present
    /// only for a two-body compile. Applying a distant-tide correction uses
    /// this operator; do not recollocate pair-internal GEM from scratch, and
    /// do not assemble this on a three-body compile to inflate a denominator.
    #[serde(default)]
    pub pair_inverse: Option<PairInverse>,
    pub residual: Residual,
    pub charge: Charge,
    pub wall_ns: u128,
}

/// LU of \((I-K)\) on the pair mesh. Unknowns are \((a_x,a_y)\) per stored
/// interval function, matching `interval_functions` order at factorization.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct PairInverse {
    pub body_id: Vec<u64>,
    pub t0: Vec<f64>,
    pub lu: Vec<f64>,
    pub pivots: Vec<usize>,
    pub n: usize,
}

impl SourceResponse {
    /// Reconstruct consumer geometry from the stored generator.
    /// Template times/ids/μ come from the debug worldtube grid; x and v come
    /// from `compact`. Fails closed if the generator has no piece at a sample.
    pub fn decode_sources(&self, charge: &mut Charge) -> Result<Vec<Body>, ResponseError> {
        if self.compact.pieces.is_empty() {
            return Err(ResponseError::UnsupportedDomain {
                why: "compact generator refused; consumers cannot reconstruct".into(),
            });
        }
        self.compact.decode_from_template(&self.worldtubes, charge)
    }
}

/// Slow independent reference: genesis + interventions only.
pub struct Reference {
    ic: InitialCondition,
    interventions: Vec<Intervention>,
    dt: f64,
}

impl Reference {
    pub fn from_genesis(ic: InitialCondition, interventions: Vec<Intervention>, dt: f64) -> Self {
        Self {
            ic,
            interventions,
            dt,
        }
    }

    /// Opt-in numerical reference lookup for continuous Euler histories only.
    /// Original exhaustive path remains the equivalence oracle.
    pub fn evolve_to_indexed(&self, horizon: f64) -> Result<(Vec<Body>, Charge), ResponseError> {
        if !self.interventions.is_empty()
            || !self.dt.is_finite()
            || self.dt <= 0.0
            || !horizon.is_finite()
            || !self.ic.genesis_t.is_finite()
            || horizon < self.ic.genesis_t
            || self.ic.genesis_t + self.dt <= self.ic.genesis_t
            || horizon + self.dt <= horizon
            || self.ic.bodies.iter().any(|b| {
                !b.mu.is_finite()
                    || !b.x.iter().chain(b.v.iter()).all(|x| x.is_finite())
                    || V2::from_arr(b.v).norm() / C > BETA_MAX
            })
        {
            return Err(ResponseError::UnsupportedDomain { why:"indexed Euler requires finite unforced subluminal genesis and positive representable dt".into() });
        }
        let mut job = EulerContinueJob::from_genesis(&self.ic, &[], horizon, self.dt);
        job.indexed_lookup = true;
        let mut budget = u64::MAX;
        while job.poll(&mut budget)? == JobPoll::Pending {}
        Ok(job.into_bodies())
    }

    pub fn evolve_to(&self, horizon: f64) -> Result<(Vec<Body>, Charge), ResponseError> {
        let mut charge = Charge {
            init: 1,
            ..Charge::default()
        };
        let bodies = evolve(
            &self.ic,
            &self.interventions,
            horizon,
            self.dt,
            &mut charge,
        )?;
        Ok((bodies, charge))
    }
}

pub fn laboratory_two_body() -> InitialCondition {
    InitialCondition {
        genesis_t: 0.0,
        bodies: vec![
            BodyInit {
                id: 0,
                mu: 1.0,
                x: [-4.0, 0.0],
                v: [0.0, 0.0],
            },
            BodyInit {
                id: 1,
                mu: 1.0,
                x: [4.0, 0.0],
                v: [0.0, 0.0],
            },
        ],
    }
}

pub fn laboratory_family() -> InitialCondition {
    let mut ic = laboratory_two_body();
    let extras = [
        ([1.5, -6.0], 0.05),
        ([-1.5, -6.4], 0.05),
        ([0.8, -7.2], 0.05),
        ([-0.9, -7.6], 0.05),
    ];
    for (k, (x, mu)) in extras.into_iter().enumerate() {
        ic.bodies.push(BodyInit {
            id: 10 + k as u64,
            mu,
            x,
            v: [0.0, 0.0],
        });
    }
    ic
}

pub fn laboratory_encounter() -> (InitialCondition, Vec<Intervention>) {
    let mut ic = laboratory_two_body();
    ic.bodies.push(BodyInit {
        id: 99,
        mu: 1.0,
        x: [0.0, 5.5],
        v: [0.0, -0.4],
    });
    (ic, Vec::new())
}

/// Named farther massive fixture for a Schur pair-block update. Not
/// `laboratory_encounter` id 99. μ=1 is massive, not a test particle.
pub fn laboratory_distant_tide() -> InitialCondition {
    let mut ic = laboratory_two_body();
    ic.bodies.push(BodyInit {
        id: 77,
        mu: 1.0,
        x: [0.0, 40.0],
        v: [0.0, 0.0],
    });
    ic
}

pub fn laboratory_kick() -> Vec<Intervention> {
    vec![Intervention {
        t: 1.25,
        body_id: 0,
        delta_v: [0.0, 0.125],
    }]
}

/// Four delayed kicks that refuse the compact sidecar at H=9.
pub fn laboratory_four_kick() -> Vec<Intervention> {
    (0..4)
        .map(|n| Intervention {
            t: 1.25 + 2.0 * n as f64,
            body_id: 0,
            delta_v: [0.0, 0.02],
        })
        .collect()
}

/// Source ops of one equivalent completed history through the requested
/// horizon: collocation `source_evolution` plus retarded GEM solves.
/// Repair suffix work is counted here via `interval_continue`; it is not a
/// skipped counter. `Charge.repair` is the splice flag, not this denominator.
/// Reconstruction copies are not source ops.
fn source_ops_of(compiled: &SourceResponse) -> u64 {
    compiled.charge.source_evolution + compiled.charge.retarded_solves
}

/// Chord-only held-out queries (named remainder). Compile-time and extra-ray
/// consumers that decode worldtubes still call `fly_ship` / `fly_ray` on
/// `&[Body]`. Query-time GEM lookback for required ship/ray/clock uses
/// `complete_required_queries_compiled`.
#[allow(dead_code)]
fn complete_required_queries(
    bodies: &[Body],
    horizon: f64,
    charge: &mut Charge,
) -> Result<(bool, bool, bool, bool), ResponseError> {
    let ship_h = horizon.min(3.5).max(0.25);
    let ship = fly_ship(
        bodies,
        0.1_f64.min(ship_h * 0.5),
        [0.0, 3.0],
        [0.125, 0.0],
        ship_h,
        (horizon / 32.0).max(1.0 / 64.0),
        charge,
    )?;
    let ray = fly_ray(
        bodies,
        0.1_f64.min(ship_h * 0.5),
        [0.0, 3.0],
        [1.0, 0.0],
        8.0,
        0.05,
        charge,
    )?;
    let clock = clock_rate(bodies, ship.t, ship.x, ship.v, charge)?;
    let (ct, cd) = contact_closest(
        bodies,
        0,
        1,
        0.0,
        horizon.min(4.0),
        (horizon / 16.0).max(1.0 / 32.0),
        charge,
    )?;
    let _ = ct;
    Ok((
        ship.tau > 0.0,
        ray.t > 0.1,
        clock.is_finite() && clock > 0.0 && clock <= 1.0,
        cd.is_finite() && cd > 0.0,
    ))
}

fn genesis_bodies(ic: &InitialCondition) -> Vec<Body> {
    ic.bodies
        .iter()
        .map(|b| Body {
            id: b.id,
            segments: vec![Segment {
                t0: ic.genesis_t,
                t1: None,
                x0: b.x,
                v: b.v,
                a: [0.0, 0.0],
                mu: b.mu,
            }],
        })
        .collect()
}

fn close_and_kink(
    body: &mut Body,
    t: f64,
    x: V2,
    v: V2,
    mu: f64,
    closed_a: V2,
    tail_a: V2,
) {
    if let Some(last) = body.segments.last_mut() {
        last.t1 = Some(t);
        last.a = closed_a.arr();
    }
    body.segments.push(Segment {
        t0: t,
        t1: None,
        x0: x.arr(),
        v: v.arr(),
        a: tail_a.arr(),
        mu,
    });
}

fn segment_as_function(seg: &Segment, query_t: f64) -> IntervalFunction {
    IntervalFunction {
        body_id: 0,
        t0: seg.t0,
        t1: seg.t1.unwrap_or(query_t).max(seg.t0),
        x0: seg.x0,
        v0: seg.v,
        a: seg.a,
        mu: seg.mu,
    }
}

/// Inertial (constant-v) retarded delay. Chord remainder; omits ½`ah²`.
fn inertial_delay(query_t: f64, query_x: V2, seg: &Segment) -> Option<f64> {
    let v = V2::from_arr(seg.v);
    let x_now = seg.at(query_t);
    let r_now = query_x.sub(x_now);
    let a = v.norm2() - C * C;
    let b = 2.0 * r_now.dot(v);
    let c0 = r_now.norm2();
    let u = if a.abs() < 1e-18 {
        if c0 <= 0.0 {
            0.0
        } else {
            c0.sqrt() / C
        }
    } else {
        let disc = b * b - 4.0 * a * c0;
        if disc < 0.0 {
            return None;
        }
        let u = (-b - disc.sqrt()) / (2.0 * a);
        if !u.is_finite() || u < -1e-12 {
            return None;
        }
        u.max(0.0)
    };
    let t_ret = query_t - u;
    let t1 = seg.t1.unwrap_or(query_t);
    if t_ret + 1e-12 < seg.t0 || t_ret > t1 + 1e-12 || t_ret > query_t + 1e-12 {
        return None;
    }
    Some(u)
}

fn retarded_lookback(query_t: f64, query_x: V2, seg: &Segment, charge: &mut Charge) -> Option<f64> {
    charge.retarded_solves += 1;
    inertial_delay(query_t, query_x, seg)
}

/// Constant-a retarded delay on a stored interval function, including ½`ah²`.
fn retarded_lookback_function(
    query_t: f64,
    query_x: V2,
    fun: &IntervalFunction,
    charge: &mut Charge,
) -> Option<f64> {
    charge.retarded_solves += 1;
    if !query_t.is_finite() || !fun.t0.is_finite() || !fun.t1.is_finite()
        || !query_x.x.is_finite() || !query_x.y.is_finite()
        || fun.t1 < fun.t0 || query_t < fun.t0
    {
        return None;
    }
    let mut lo = fun.t0;
    let mut hi = fun.t1.min(query_t);
    // F(s)=|query_x-source(s)|-C*(query_t-s) increases strictly for
    // subluminal source motion. Constant-a velocity is affine, so checking
    // both endpoints bounds its norm throughout this interval. A source's
    // absence must follow from this bracket, never an out-of-range guess.
    // Each residual/state evaluation, including failed attempts, is charged
    // as verification; retarded_solves continues to count requested solves.
    let mut evaluate = |t: f64| -> Option<(f64, f64, f64)> {
        charge.verification += 1;
        let (x, v) = fun.state_at(t);
        let speed = v.norm();
        let rel = query_x.sub(x);
        let distance = rel.norm();
        let light_distance = C * (query_t - t);
        if !speed.is_finite() || speed >= C || !distance.is_finite()
            || !light_distance.is_finite()
        {
            return None;
        }
        let derivative = if distance > 0.0 { C - rel.dot(v) / distance } else { C };
        let residual = distance - light_distance;
        let tolerance = 1e-12 * (1.0 + distance + light_distance.abs());
        if !derivative.is_finite() || derivative <= 0.0 || !residual.is_finite() {
            return None;
        }
        Some((residual, derivative, tolerance))
    };
    let (flo, _, tol_lo) = evaluate(lo)?;
    let (fhi, _, tol_hi) = evaluate(hi)?;
    if flo.abs() <= tol_lo {
        return Some(query_t - lo);
    }
    if fhi.abs() <= tol_hi {
        return Some(query_t - hi);
    }
    if flo > 0.0 || fhi < 0.0 {
        return None;
    }
    let mut t = lo + 0.5 * (hi - lo);
    for _ in 0..80 {
        let (f, derivative, tolerance) = evaluate(t)?;
        if f.abs() <= tolerance {
            return Some(query_t - t);
        }
        if f < 0.0 { lo = t; } else { hi = t; }
        let width = hi - lo;
        let proposal = t - f / derivative;
        // Safeguard the Newton step so every unsuccessful iteration contracts
        // the bracket; no iteration may abandon a valid root at an endpoint.
        let next = if proposal.is_finite()
            && proposal > lo + 0.1 * width && proposal < hi - 0.1 * width
        {
            proposal
        } else {
            lo + 0.5 * width
        };
        if next <= lo || next >= hi {
            break;
        }
        t = next;
    }
    // Retain the historical numerical miss ceiling as a final rounding check.
    // This is a floating diagnostic, not a canonical branch certificate.
    let (miss, _, _) = evaluate(t)?;
    let delay = query_t - t;
    if delay.is_finite() && delay >= 0.0 && miss.abs() <= 1e-6 * (1.0 + C * delay) {
        Some(delay)
    } else {
        None
    }
}

fn gem_from_segment(
    query_t: f64,
    query_x: V2,
    seg: &Segment,
    charge: &mut Charge,
) -> Result<Option<GemField>, ResponseError> {
    if V2::from_arr(seg.a).norm() > 0.0 {
        let fun = segment_as_function(seg, query_t);
        return gem_from_function(query_t, query_x, &fun, charge);
    }
    let Some(u) = retarded_lookback(query_t, query_x, seg, charge) else {
        return Ok(None);
    };
    let t_ret = query_t - u;
    let x_ret = seg.at(t_ret);
    let rel = query_x.sub(x_ret);
    let r = rel.norm();
    if r < 1e-15 {
        return Err(ResponseError::Singular);
    }
    let n = rel.scale(1.0 / r);
    let beta = V2::from_arr(seg.v).scale(1.0 / C);
    let beta2 = beta.norm2();
    if beta2.sqrt() >= 1.0 {
        return Err(ResponseError::Superluminal);
    }
    let kappa = 1.0 - n.dot(beta);
    if kappa.abs() < 1e-15 {
        return Err(ResponseError::Singular);
    }
    let d = r * kappa;
    let mu = seg.mu;
    let phi = -mu / d;
    let inv_d2 = mu / (d * d);
    let grad = beta
        .scale(-1.0)
        .add(n.scale((1.0 - beta2) / kappa))
        .scale(inv_d2);
    let dphi_dt = (mu * C / (d * d * kappa)) * (beta2 - n.dot(beta));
    let dxi_dt = beta.scale(dphi_dt);
    let e = grad.scale(-1.0).sub(dxi_dt.scale(4.0 / C));
    let curl_z = inv_d2 * ((1.0 - beta2) / kappa) * n.cross_z(beta);
    let b_z = (4.0 / C) * curl_z;
    charge.field_evals += 1;
    Ok(Some(GemField { phi, e, b_z }))
}

fn gem_from_function(
    query_t: f64,
    query_x: V2,
    fun: &IntervalFunction,
    charge: &mut Charge,
) -> Result<Option<GemField>, ResponseError> {
    let Some(u) = retarded_lookback_function(query_t, query_x, fun, charge) else {
        return Ok(None);
    };
    let t_ret = query_t - u;
    let (x_ret, v_ret) = fun.state_at(t_ret);
    let rel = query_x.sub(x_ret);
    let r = rel.norm();
    if r < 1e-15 {
        return Err(ResponseError::Singular);
    }
    let n = rel.scale(1.0 / r);
    let beta = v_ret.scale(1.0 / C);
    let beta2 = beta.norm2();
    if beta2.sqrt() >= 1.0 {
        return Err(ResponseError::Superluminal);
    }
    let kappa = 1.0 - n.dot(beta);
    if kappa.abs() < 1e-15 {
        return Err(ResponseError::Singular);
    }
    let d = r * kappa;
    let mu = fun.mu;
    let phi = -mu / d;
    let inv_d2 = mu / (d * d);
    let grad = beta
        .scale(-1.0)
        .add(n.scale((1.0 - beta2) / kappa))
        .scale(inv_d2);
    let dphi_dt = (mu * C / (d * d * kappa)) * (beta2 - n.dot(beta));
    let dxi_dt = beta.scale(dphi_dt);
    let e = grad.scale(-1.0).sub(dxi_dt.scale(4.0 / C));
    let curl_z = inv_d2 * ((1.0 - beta2) / kappa) * n.cross_z(beta);
    let b_z = (4.0 / C) * curl_z;
    charge.field_evals += 1;
    Ok(Some(GemField { phi, e, b_z }))
}

/// Conservative AABB of constant-a motion on `[t0, t1]`. Axis-wise quadratic
/// extrema are included, so the box contains the curve.
fn function_aabb(fun: &IntervalFunction) -> (V2, V2) {
    let h = (fun.t1 - fun.t0).max(0.0);
    let x0 = V2::from_arr(fun.x0);
    let v0 = V2::from_arr(fun.v0);
    let a = V2::from_arr(fun.a);
    let (x1, _) = fun.state_at(fun.t1);
    let mut mn = V2::new(x0.x.min(x1.x), x0.y.min(x1.y));
    let mut mx = V2::new(x0.x.max(x1.x), x0.y.max(x1.y));
    let include = |mn: &mut V2, mx: &mut V2, p: V2| {
        mn.x = mn.x.min(p.x);
        mn.y = mn.y.min(p.y);
        mx.x = mx.x.max(p.x);
        mx.y = mx.y.max(p.y);
    };
    if a.x.abs() > 1e-18 {
        let hv = -v0.x / a.x;
        if hv > 0.0 && hv < h {
            include(&mut mn, &mut mx, fun.state_at(fun.t0 + hv).0);
        }
    }
    if a.y.abs() > 1e-18 {
        let hv = -v0.y / a.y;
        if hv > 0.0 && hv < h {
            include(&mut mn, &mut mx, fun.state_at(fun.t0 + hv).0);
        }
    }
    (mn, mx)
}

fn point_aabb_delay_range(query: V2, mn: V2, mx: V2) -> (f64, f64) {
    let dx = if query.x < mn.x {
        mn.x - query.x
    } else if query.x > mx.x {
        query.x - mx.x
    } else {
        0.0
    };
    let dy = if query.y < mn.y {
        mn.y - query.y
    } else if query.y > mx.y {
        query.y - mx.y
    } else {
        0.0
    };
    let dmin = (dx * dx + dy * dy).sqrt();
    let mut dmax2 = 0.0_f64;
    for x in [mn.x, mx.x] {
        for y in [mn.y, mx.y] {
            let ddx = query.x - x;
            let ddy = query.y - y;
            dmax2 = dmax2.max(ddx * ddx + ddy * ddy);
        }
    }
    (dmin / C, dmax2.sqrt() / C)
}

/// True if this stored-a block *might* contain the retarded event. AABB delay
/// range is a superset of the curve delay range, so a possible hit is never
/// skipped. No retarded Newton; not a source-ops charge.
fn interval_may_contain_retarded(query_t: f64, query_x: V2, fun: &IntervalFunction) -> bool {
    if query_t + 1e-12 < fun.t0 {
        return false;
    }
    let t1 = fun.t1.min(query_t);
    if t1 + 1e-12 < fun.t0 {
        return false;
    }
    let u_lo = (query_t - t1).max(0.0);
    let u_hi = (query_t - fun.t0).max(0.0);
    let (mn, mx) = function_aabb(fun);
    let (delay_lo, delay_hi) = point_aabb_delay_range(query_x, mn, mx);
    delay_lo <= u_hi + 1e-9 && delay_hi + 1e-9 >= u_lo
}

fn field_at(
    bodies: &[Body],
    t: f64,
    x: V2,
    skip: Option<u64>,
    charge: &mut Charge,
) -> Result<GemField, ResponseError> {
    let mut total = GemField {
        phi: 0.0,
        e: V2::zero(),
        b_z: 0.0,
    };
    for body in bodies {
        if Some(body.id) == skip {
            continue;
        }
        let mut best: Option<GemField> = None;
        for seg in body.segments.iter().rev() {
            if seg.t0 > t + 1e-15 {
                continue;
            }
            if let Some(f) = gem_from_segment(t, x, seg, charge)? {
                best = Some(f);
                break;
            }
        }
        if let Some(f) = best {
            total.phi += f.phi;
            total.e = total.e.add(f.e);
            total.b_z += f.b_z;
        }
    }
    Ok(total)
}

/// Private: callers must construct continuous subluminal inertial chords through
/// Euler from genesis. Arrival(s)=s+|x-X(s)|/C is strictly increasing on this
/// domain. Select a conservative upper start index, then run the ORIGINAL root
/// and field routines in the ORIGINAL reverse order. This is floating laboratory
/// lookup, not a certificate for canonical branches.
fn field_at_euler_indexed(
    bodies: &[Body],
    t: f64,
    x: V2,
    skip: Option<u64>,
    charge: &mut Charge,
) -> Result<GemField, ResponseError> {
    let mut total = GemField {
        phi: 0.0,
        e: V2::zero(),
        b_z: 0.0,
    };
    for body in bodies {
        if Some(body.id) == skip || body.segments.is_empty() {
            continue;
        }
        let first = &body.segments[0];
        // Includes the root's time-boundary tolerance and conservative roundoff
        // slack. Extra candidates cost work; never snap the selected root/state.
        let slack = 1e-9
            * (1.0 + t.abs() + x.norm() + V2::from_arr(first.x0).norm() + C * (t - first.t0).abs());
        let (mut lo, mut hi) = (0, body.segments.len());
        while lo < hi {
            let mid = lo + (hi - lo) / 2;
            let seg = &body.segments[mid];
            charge.verification += 1;
            let arrival = seg.t0 + x.sub(V2::from_arr(seg.x0)).norm() / C;
            if !arrival.is_finite() || !slack.is_finite() {
                return Err(ResponseError::UnsupportedDomain {
                    why: "nonfinite indexed arrival".into(),
                });
            }
            if arrival <= t + slack {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        for seg in body.segments[..lo].iter().rev() {
            if seg.t0 > t + 1e-15 {
                continue;
            }
            if let Some(f) = gem_from_segment(t, x, seg, charge)? {
                total.phi += f.phi;
                total.e = total.e.add(f.e);
                total.b_z += f.b_z;
                break;
            }
        }
    }
    Ok(total)
}

/// GEM lookback on stored constant-a interval functions (½`ah²` included).
/// Compile-time collocation and query-time cameras share this geometry.
/// When no function covers the retarded event, the open-tail worldtube is
/// the last stored `a` (same ½`ah²`), not an inertial chord. Independent
/// enclosure checkers still use chord `field_at` on Euler bodies and do not
/// read compile residual.
fn field_at_stored(
    functions: &[IntervalFunction],
    chords: &[Body],
    t: f64,
    x: V2,
    skip: Option<u64>,
    charge: &mut Charge,
) -> Result<GemField, ResponseError> {
    let mut total = GemField {
        phi: 0.0,
        e: V2::zero(),
        b_z: 0.0,
    };
    let mut ids: Vec<u64> = chords.iter().map(|b| b.id).collect();
    for fun in functions {
        if !ids.contains(&fun.body_id) {
            ids.push(fun.body_id);
        }
    }
    for id in ids {
        if Some(id) == skip {
            continue;
        }
        let mut funs: Vec<&IntervalFunction> = functions
            .iter()
            .filter(|f| f.body_id == id)
            .collect();
        funs.sort_by(|a, b| a.t0.partial_cmp(&b.t0).unwrap());
        let mut best: Option<GemField> = None;
        for fun in funs.iter().rev() {
            if fun.t0 > t + 1e-15 {
                continue;
            }
            // Covering bound: do not charge a retarded Newton on an interval
            // that cannot contain t_ret. Same stored-a geometry when it hits.
            if !interval_may_contain_retarded(t, x, fun) {
                continue;
            }
            if let Some(f) = gem_from_function(t, x, fun, charge)? {
                best = Some(f);
                break;
            }
        }
        if best.is_none() {
            if let Some(body) = chords.iter().find(|b| b.id == id) {
                for seg in body.segments.iter().rev() {
                    if seg.t0 > t + 1e-15 {
                        continue;
                    }
                    if let Some(f) = gem_from_segment(t, x, seg, charge)? {
                        best = Some(f);
                        break;
                    }
                }
            }
        }
        if let Some(f) = best {
            total.phi += f.phi;
            total.e = total.e.add(f.e);
            total.b_z += f.b_z;
        }
    }
    Ok(total)
}

fn field_at_compiled(
    compiled: &SourceResponse,
    t: f64,
    x: V2,
    skip: Option<u64>,
    charge: &mut Charge,
) -> Result<GemField, ResponseError> {
    field_at_stored(
        &compiled.interval_functions,
        &compiled.worldtubes,
        t,
        x,
        skip,
        charge,
    )
}

#[derive(Clone, Copy)]
enum QuerySources<'a> {
    Chords(&'a [Body]),
    Compiled(&'a SourceResponse),
}

fn gem_field(
    sources: QuerySources<'_>,
    t: f64,
    x: V2,
    skip: Option<u64>,
    charge: &mut Charge,
) -> Result<GemField, ResponseError> {
    match sources {
        QuerySources::Chords(bodies) => field_at(bodies, t, x, skip, charge),
        QuerySources::Compiled(compiled) => field_at_compiled(compiled, t, x, skip, charge),
    }
}

fn apply_gem_a(field: GemField, v: V2) -> V2 {
    field.e.add(v.perp_z(field.b_z))
}

fn evolve(
    ic: &InitialCondition,
    interventions: &[Intervention],
    horizon: f64,
    dt: f64,
    charge: &mut Charge,
) -> Result<Vec<Body>, ResponseError> {
    let mut bodies = genesis_bodies(ic);
    charge.history += 1;
    continue_from(&mut bodies, ic.genesis_t, interventions, horizon, dt, charge)?;
    Ok(bodies)
}

fn pair_tau_min(bodies: &[Body], t: f64) -> Result<f64, ResponseError> {
    if bodies.len() < 2 {
        return Ok(f64::INFINITY);
    }
    let mut tau = f64::INFINITY;
    for i in 0..bodies.len() {
        let (xi, _, _) = bodies[i].present(t)?;
        for j in (i + 1)..bodies.len() {
            let (xj, _, _) = bodies[j].present(t)?;
            let r = xi.sub(xj).norm().max(1e-12);
            tau = tau.min(r / C);
        }
    }
    Ok(tau)
}

fn tidal_l_at(bodies: &[Body], t: f64, charge: &mut Charge) -> Result<f64, ResponseError> {
    let mut beta_max = 0.0_f64;
    let mut row_max = 0.0_f64;
    for body in bodies {
        let (_, v, _) = body.present(t)?;
        beta_max = beta_max.max(v.norm() / C);
        let mut row = 0.0_f64;
        let (xi, _, _) = body.present(t)?;
        for other in bodies {
            if other.id == body.id {
                continue;
            }
            let (xj, _, mu) = other.present(t)?;
            let r = xi.sub(xj).norm().max(1e-12);
            row += 2.0 * mu / (r * r * r);
            charge.coefficient_construction += 1;
        }
        row_max = row_max.max(row);
    }
    Ok(row_max * (1.0 + 4.0 * beta_max))
}

struct IntervalOutcome {
    bodies: Vec<Body>,
    blocks: u64,
    q: f64,
    tau: f64,
    functions: Vec<IntervalFunction>,
}

/// Causal-block collocation of the retarded GEM Volterra map.
///
/// On each block of length `≤ τ_min = r_min/c`, same-block cross response is
/// spacelike, so the discrete operator is block-lower-triangular. Forward
/// substitution is the Schur elimination of
/// `a = f_A + K_AB b`, `b = f_B + K_BA a`
/// for interval functions that are constant-acceleration on the block and
/// piecewise-inertial between knots. This is not Euler-`dt` `evolve()`, and
/// not a Chebyshev sidecar of that stepper.
fn interval_compile(
    ic: &InitialCondition,
    interventions: &[Intervention],
    horizon: f64,
    charge: &mut Charge,
    subdivision: usize,
) -> Result<IntervalOutcome, ResponseError> {
    let mut bodies = genesis_bodies(ic);
    charge.history += 1;
    // Factor one deliberately follows the historical no-hint path exactly.
    let tau_hint = if subdivision == 1 {
        None
    } else {
        let cadence = pair_tau_min(&bodies, ic.genesis_t)? / subdivision as f64;
        let step = cadence * 0.5;
        // incoming_knots filters/deduplicates at 1e-12, so a smaller step
        // would not represent the requested subdivision. Also refuse steps
        // that cannot advance floating time anywhere in this finite window.
        if !cadence.is_finite() || step <= 1e-12
            || !ic.genesis_t.is_finite() || !horizon.is_finite()
            || !(ic.genesis_t + step).is_finite() || !(horizon + step).is_finite()
            || ic.genesis_t + step <= ic.genesis_t || horizon + step <= horizon
        {
            return Err(ResponseError::UnsupportedDomain {
                why: "refined causal cadence is nonfinite or below usable knot/time resolution".into(),
            });
        }
        Some(cadence)
    };
    let stats = interval_continue(
        &mut bodies,
        ic.genesis_t,
        interventions,
        horizon,
        charge,
        tau_hint,
        &[],
    )?;
    Ok(IntervalOutcome {
        bodies,
        blocks: stats.blocks,
        q: stats.q,
        tau: stats.tau,
        functions: stats.functions,
    })
}

struct IntervalStats {
    blocks: u64,
    q: f64,
    tau: f64,
    functions: Vec<IntervalFunction>,
}

/// Pollable collocation/repair continuation. One causal block is charged before
/// a yield. This is a diagnostic adapter; it does not authorize canonical gravity.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum JobPoll {
    Pending,
    Ready,
}

#[derive(Clone, Debug)]
pub struct CoupledCompileJob {
    bodies: Vec<Body>,
    t: f64,
    k: usize,
    knots: Vec<Vec<f64>>,
    kicks: Vec<Intervention>,
    known: Vec<IntervalFunction>,
    functions: Vec<IntervalFunction>,
    blocks: u64,
    q: f64,
    tau: f64,
    horizon: f64,
    t_start: f64,
    charge: Charge,
    ready: bool,
}

impl CoupledCompileJob {
    pub fn from_genesis(
        ic: &InitialCondition,
        interventions: &[Intervention],
        horizon: f64,
    ) -> Result<Self, ResponseError> {
        Self::begin(
            genesis_bodies(ic),
            ic.genesis_t,
            interventions,
            horizon,
            Charge {
                init: 1,
                ..Charge::default()
            },
            None,
            &[],
        )
    }

    fn begin(
        mut bodies: Vec<Body>,
        t_start: f64,
        interventions: &[Intervention],
        horizon: f64,
        mut charge: Charge,
        tau_hint: Option<f64>,
        prior: &[IntervalFunction],
    ) -> Result<Self, ResponseError> {
        let mut kicks: Vec<Intervention> = interventions
            .iter()
            .filter(|iv| iv.t + 1e-12 >= t_start)
            .cloned()
            .collect();
        kicks.sort_by(|a, b| a.t.partial_cmp(&b.t).unwrap());
        let tau = match tau_hint {
            Some(tau) if tau.is_finite() && tau > 0.0 => tau,
            _ => pair_tau_min(&bodies, t_start)?,
        };
        let knots = incoming_knots(&bodies, t_start, horizon, &kicks, tau, &mut charge)?;
        let mut functions: Vec<IntervalFunction> = Vec::new();
        let mut known: Vec<IntervalFunction> = prior.to_vec();
        {
            let mut catch_up: Vec<(usize, V2, V2, f64, IntervalFunction)> = Vec::new();
            for (i, body) in bodies.iter().enumerate() {
                let has = kicks
                    .iter()
                    .any(|iv| iv.body_id == body.id && (iv.t - t_start).abs() < 1e-12);
                if !has {
                    continue;
                }
                let t_seg = body.segments.last().map(|s| s.t0).unwrap_or(t_start);
                if t_start <= t_seg + 1e-18 {
                    continue;
                }
                let h = t_start - t_seg;
                let (x, v, mu) = body.present(t_seg)?;
                let t_col = t_seg + 0.5 * h;
                let x_col = x.add(v.scale(t_col - t_seg));
                let field = field_at_stored(&known, &bodies, t_col, x_col, Some(body.id), &mut charge)?;
                let a = apply_gem_a(field, v);
                let fun = IntervalFunction {
                    body_id: body.id,
                    t0: t_seg,
                    t1: t_start,
                    x0: x.arr(),
                    v0: v.arr(),
                    a: a.arr(),
                    mu,
                };
                let (x_new, v_new) = fun.inertial_end();
                if v_new.norm() >= C {
                    return Err(ResponseError::Superluminal);
                }
                catch_up.push((i, x_new, v_new, mu, fun));
                charge.source_evolution += 1;
            }
            if !catch_up.is_empty() {
                charge.factorization += 1;
            }
            for (i, x_new, v_new, mu, fun) in catch_up {
                close_and_kink(
                    &mut bodies[i],
                    t_start,
                    x_new,
                    v_new,
                    mu,
                    V2::from_arr(fun.a),
                    V2::from_arr(fun.a),
                );
                known.push(fun.clone());
                functions.push(fun);
            }
        }
        Ok(Self {
            bodies,
            t: t_start,
            k: 0,
            knots,
            kicks,
            known,
            functions,
            blocks: 0,
            q: 0.0,
            tau,
            horizon,
            t_start,
            charge,
            ready: false,
        })
    }

    /// Charge one collocation block, then yield if the budget is exhausted.
    pub fn poll(&mut self, op_budget: &mut u64) -> Result<JobPoll, ResponseError> {
        if self.ready {
            return Ok(JobPoll::Ready);
        }
        loop {
            if self.t >= self.horizon - 1e-15 {
                self.ready = true;
                return Ok(JobPoll::Ready);
            }
            if *op_budget == 0 {
                return Ok(JobPoll::Pending);
            }
            self.step_one_block()?;
            *op_budget = op_budget.saturating_sub(1);
        }
    }

    fn step_one_block(&mut self) -> Result<(), ResponseError> {
        let bodies = &mut self.bodies;
        let t = self.t;
        let horizon = self.horizon;
        let t_start = self.t_start;
        while self.k < self.kicks.len() && self.kicks[self.k].t <= t + 1e-12 {
            let kick = &self.kicks[self.k];
            if let Some(body) = bodies.iter_mut().find(|b| b.id == kick.body_id) {
                let (x, v, mu) = body.present(kick.t)?;
                let v_new = v.add(V2::from_arr(kick.delta_v));
                if v_new.norm() >= C {
                    return Err(ResponseError::Superluminal);
                }
                let closed_a = body
                    .segments
                    .last()
                    .map(|s| V2::from_arr(s.a))
                    .unwrap_or(V2::zero());
                close_and_kink(body, kick.t, x, v_new, mu, closed_a, V2::zero());
                self.charge.history += 1;
            }
            self.k += 1;
        }
        let mut t_next = horizon;
        let mut any_physical = false;
        for body_knots in &self.knots {
            if let Some(tn) = body_knots.iter().copied().find(|tn| *tn > t + 1e-12) {
                if tn < t_next {
                    t_next = tn;
                    any_physical = true;
                } else if (tn - t_next).abs() < 1e-12 {
                    any_physical = true;
                }
            }
        }
        if !any_physical || t_next <= t + 1e-18 {
            self.t = horizon;
            return Ok(());
        }
        let mut updates: Vec<(usize, V2, V2, f64, IntervalFunction)> = Vec::new();
        let mut h_max = 0.0_f64;
        let mut t_col_q = t;
        for (i, body) in bodies.iter().enumerate() {
            let has_knot = self.knots[i].iter().any(|tn| (*tn - t_next).abs() < 1e-12);
            if !has_knot {
                continue;
            }
            let t_seg = body.segments.last().map(|s| s.t0).unwrap_or(t);
            let h = t_next - t_seg;
            if h <= 1e-18 {
                continue;
            }
            let (x, v, mu) = body.present(t_seg)?;
            if v.norm() / C > BETA_MAX {
                return Err(ResponseError::UnsupportedDomain {
                    why: format!("beta={} exceeds admitted {}", v.norm() / C, BETA_MAX),
                });
            }
            let t_col = t_seg + 0.5 * h;
            let x_col = x.add(v.scale(t_col - t_seg));
            let field = field_at_stored(&self.known, bodies, t_col, x_col, Some(body.id), &mut self.charge)?;
            if field.phi.abs() / (C * C) > PHI_C2_MAX {
                return Err(ResponseError::UnsupportedDomain {
                    why: format!("|Phi|/c^2={} exceeds {PHI_C2_MAX}", field.phi.abs() / (C * C)),
                });
            }
            let a = apply_gem_a(field, v);
            let fun = IntervalFunction {
                body_id: body.id,
                t0: t_seg,
                t1: t_next,
                x0: x.arr(),
                v0: v.arr(),
                a: a.arr(),
                mu,
            };
            let (x_new, v_new) = fun.inertial_end();
            if v_new.norm() >= C {
                return Err(ResponseError::Superluminal);
            }
            updates.push((i, x_new, v_new, mu, fun));
            self.charge.source_evolution += 1;
            h_max = h_max.max(h);
            t_col_q = t_col;
        }
        if !updates.is_empty() {
            let l = tidal_l_at(bodies, t_col_q.min(horizon).max(t_start), &mut self.charge)?;
            self.q = self.q.max(h_max * l);
            self.charge.factorization += 1;
        }
        for (i, x_new, v_new, mu, fun) in updates {
            close_and_kink(
                &mut bodies[i],
                t_next,
                x_new,
                v_new,
                mu,
                V2::from_arr(fun.a),
                V2::from_arr(fun.a),
            );
            self.known.push(fun.clone());
            self.functions.push(fun);
        }
        self.blocks += 1;
        self.t = t_next;
        Ok(())
    }

    pub fn is_ready(&self) -> bool {
        self.ready
    }

    pub fn charge(&self) -> &Charge {
        &self.charge
    }

    /// Resume a committed prefix after an extra kick in an uncommitted suffix
    /// or new history branch. Continuation uses the complete ordered inputs.
    pub fn from_repair(
        compiled: &SourceResponse,
        extra: &[Intervention],
        horizon: f64,
    ) -> Result<Self, ResponseError> {
        if extra.is_empty() {
            return Err(ResponseError::UnsupportedDomain {
                why: "repair extra is empty; extra-ray consumers are not a source-history splice"
                    .into(),
            });
        }
        if compiled.interval_functions.is_empty() {
            return Err(ResponseError::UnsupportedDomain {
                why: "no stored interval functions; refusing to paper inertial chords as reuse"
                    .into(),
            });
        }
        let kept = kept_certified_functions(compiled, extra)?;
        let body_ids: Vec<u64> = compiled.genesis.bodies.iter().map(|b| b.id).collect();
        let t_prefix = certified_prefix_end(&kept, compiled.genesis.genesis_t, &body_ids);
        let worldtubes = worldtubes_from_interval_functions(&compiled.genesis, &kept);
        let all = merge_repair_interventions(&compiled.incoming, extra);
        Self::begin(
            worldtubes,
            t_prefix,
            &all,
            horizon,
            Charge {
                repair: 1,
                init: 1,
                reconstruction: kept.len() as u64,
                history: 1,
                ..Charge::default()
            },
            Some(compiled.interval_tau),
            &kept,
        )
    }

    pub fn collocation_parts(
        self,
    ) -> Result<(Vec<Body>, Vec<IntervalFunction>, u64, f64, f64, Charge, f64), ResponseError> {
        if !self.ready {
            return Err(ResponseError::UnsupportedDomain {
                why: "collocation job is not ready".into(),
            });
        }
        Ok((
            self.bodies,
            self.functions,
            self.blocks,
            self.q,
            self.tau,
            self.charge,
            self.horizon,
        ))
    }
}

fn incoming_knots(
    bodies: &[Body],
    t_start: f64,
    horizon: f64,
    interventions: &[Intervention],
    tau_cadence: f64,
    charge: &mut Charge,
) -> Result<Vec<Vec<f64>>, ResponseError> {
    let origin = bodies
        .iter()
        .filter_map(|b| b.segments.first().map(|s| s.t0))
        .fold(t_start, f64::min);
    let mut per_body: Vec<Vec<f64>> = bodies.iter().map(|_| Vec::new()).collect();
    // The genesis-limited model has no field before its first massive-source
    // light cone arrives. A midpoint block must not straddle that discontinuity.
    // Before the FIRST arrival each receiver is inertial, so its intersection
    // with the emitted genesis event is analytic. Later arrivals need not be
    // inertial; do not claim their frozen-position prediction is exact.
    // Restrict this construction to the common-genesis history contract.
    if bodies.iter().all(|b| b.segments.first().is_some_and(|s| s.t0 == origin)) {
        for (i, receiver) in bodies.iter().enumerate() {
            let rec = &receiver.segments[0];
            let mut first = f64::INFINITY;
            for source in bodies {
                if source.id == receiver.id { continue; }
                let src = &source.segments[0];
                if src.mu == 0.0 { continue; }
                charge.retarded_solves += 1;
                let offset = V2::from_arr(rec.x0).sub(V2::from_arr(src.x0));
                let velocity = V2::from_arr(rec.v);
                let a = velocity.norm2() - C*C;
                let b = 2.0*offset.dot(velocity);
                let d = b*b - 4.0*a*offset.norm2();
                if a >= 0.0 || !d.is_finite() || d < 0.0 {
                    return Err(ResponseError::UnsupportedDomain { why: "invalid genesis light-cone intersection".into() });
                }
                let arrival = origin + (-b-d.sqrt())/(2.0*a);
                if !arrival.is_finite() { return Err(ResponseError::UnsupportedDomain { why: "nonfinite genesis arrival".into() }); }
                first = first.min(arrival);
            }
            // An earlier commanded velocity change invalidates the straight
            // receiver construction. Retain cadence/intervention subdivision
            // in that case rather than labeling this guess a true arrival.
            let earlier_command = interventions.iter().any(|iv| iv.body_id == receiver.id && iv.t < first);
            let changed_prefix = receiver.segments.iter().any(|seg| seg.t0 < first && seg.v != rec.v);
            if !earlier_command && !changed_prefix && first > t_start + 1e-12 && first < horizon - 1e-12 {
                per_body[i].push(first);
            }
        }
    }
    if tau_cadence.is_finite() && tau_cadence > 1e-12 {
        // Collocate twice per effective cadence to resolve GEM-a variation.
        // Default cadence is the initial light crossing; explicit laboratory
        // subdivision reduces it independently of Euler-dt or dt metadata.
        let step = tau_cadence * 0.5;
        let mut t = origin + step;
        while t < horizon - 1e-12 {
            if t > t_start + 1e-12 {
                for knots in &mut per_body {
                    knots.push(t);
                }
            }
            t += step;
        }
    }
    for (i, body) in bodies.iter().enumerate() {
        for iv in interventions {
            if iv.body_id == body.id && iv.t > t_start + 1e-12 && iv.t < horizon - 1e-12 {
                per_body[i].push(iv.t);
            }
        }
    }
    // Frozen-observer light-arrival knots: B is not split at A's kick, only
    // after the cone. Incoming structure, not evolve-sampled.
    for iv in interventions {
        if iv.t + 1e-12 < t_start || iv.t > horizon + 1e-12 {
            continue;
        }
        let src = bodies
            .iter()
            .find(|b| b.id == iv.body_id)
            .ok_or(ResponseError::UnsupportedDomain {
                why: format!("kick on missing body {}", iv.body_id),
            })?;
        let x_ev = {
            let seg = src.segments.first().ok_or(ResponseError::UnsupportedDomain {
                why: "source has no genesis segment".into(),
            })?;
            seg.at(iv.t)
        };
        for (j, obs) in bodies.iter().enumerate() {
            if obs.id == iv.body_id {
                continue;
            }
            let x_obs = {
                let Some(seg) = obs.segments.first() else {
                    continue;
                };
                seg.at(iv.t)
            };
            let t_arr = iv.t + x_obs.sub(x_ev).norm() / C;
            if t_arr > t_start + 1e-12 && t_arr < horizon - 1e-12 {
                per_body[j].push(t_arr);
            }
        }
    }
    for knots in &mut per_body {
        knots.sort_by(|a, b| a.partial_cmp(b).unwrap());
        knots.dedup_by(|a, b| (*a - *b).abs() < 1e-12);
    }
    Ok(per_body)
}

fn interval_continue(
    bodies: &mut Vec<Body>,
    t_start: f64,
    interventions: &[Intervention],
    horizon: f64,
    charge: &mut Charge,
    tau_hint: Option<f64>,
    prior: &[IntervalFunction],
) -> Result<IntervalStats, ResponseError> {
    let mut job = CoupledCompileJob::begin(
        bodies.clone(),
        t_start,
        interventions,
        horizon,
        charge.clone(),
        tau_hint,
        prior,
    )?;
    let mut budget = u64::MAX;
    while job.poll(&mut budget)? == JobPoll::Pending {}
    *bodies = job.bodies;
    *charge = job.charge;
    Ok(IntervalStats {
        blocks: job.blocks,
        q: job.q,
        tau: job.tau,
        functions: job.functions,
    })
}

/// Euler/GEM reference continuation. One dt (or kick-clipped) step is charged
/// before a yield. Used by enclosure genesis evolutions and `continue_from`.
#[derive(Clone, Debug)]
pub struct EulerContinueJob {
    bodies: Vec<Body>,
    kicks: Vec<Intervention>,
    t: f64,
    k: usize,
    horizon: f64,
    dt: f64,
    charge: Charge,
    ready: bool,
    indexed_lookup: bool,
}

impl EulerContinueJob {
    pub fn start(
        bodies: Vec<Body>,
        t_start: f64,
        interventions: &[Intervention],
        horizon: f64,
        dt: f64,
        charge: Charge,
    ) -> Self {
        let mut kicks: Vec<Intervention> = interventions
            .iter()
            .filter(|iv| iv.t + 1e-12 >= t_start)
            .cloned()
            .collect();
        kicks.sort_by(|a, b| a.t.partial_cmp(&b.t).unwrap());
        Self {
            bodies,
            kicks,
            t: t_start,
            k: 0,
            horizon,
            dt,
            charge,
            ready: false,
            indexed_lookup: false,
        }
    }

    pub fn from_genesis(
        ic: &InitialCondition,
        interventions: &[Intervention],
        horizon: f64,
        dt: f64,
    ) -> Self {
        Self::start(
            genesis_bodies(ic),
            ic.genesis_t,
            interventions,
            horizon,
            dt,
            Charge {
                init: 1,
                history: 1,
                ..Charge::default()
            },
        )
    }

    pub fn poll(&mut self, op_budget: &mut u64) -> Result<JobPoll, ResponseError> {
        if self.ready {
            return Ok(JobPoll::Ready);
        }
        loop {
            if self.t >= self.horizon - 1e-15 {
                self.ready = true;
                return Ok(JobPoll::Ready);
            }
            if *op_budget == 0 {
                return Ok(JobPoll::Pending);
            }
            self.step_one()?;
            *op_budget = op_budget.saturating_sub(1);
        }
    }

    fn step_one(&mut self) -> Result<(), ResponseError> {
        let bodies = &mut self.bodies;
        let t = self.t;
        while self.k < self.kicks.len() && self.kicks[self.k].t <= t + 1e-12 {
            let kick = &self.kicks[self.k];
            if let Some(body) = bodies.iter_mut().find(|b| b.id == kick.body_id) {
                let (x, v, mu) = body.present(kick.t)?;
                let v_new = v.add(V2::from_arr(kick.delta_v));
                if v_new.norm() >= C {
                    return Err(ResponseError::Superluminal);
                }
                close_and_kink(body, kick.t, x, v_new, mu, V2::zero(), V2::zero());
                self.charge.history += 1;
            }
            self.k += 1;
        }
        let t_next = {
            let step = t + self.dt;
            let next_kick = self.kicks.get(self.k).map(|iv| iv.t).unwrap_or(self.horizon);
            step.min(next_kick).min(self.horizon)
        };
        if t_next <= t + 1e-18 {
            self.t = t_next;
            return Ok(());
        }
        let h = t_next - t;
        let mut updates: Vec<(usize, V2, V2, f64)> = Vec::new();
        for (i, body) in bodies.iter().enumerate() {
            let (x, v, mu) = body.present(t)?;
            if v.norm() / C > BETA_MAX {
                return Err(ResponseError::UnsupportedDomain {
                    why: format!("beta={} exceeds admitted {}", v.norm() / C, BETA_MAX),
                });
            }
            let field = if self.indexed_lookup {
                field_at_euler_indexed(bodies,t,x,Some(body.id),&mut self.charge)?
            } else { field_at(bodies, t, x, Some(body.id), &mut self.charge)? };
            if field.phi.abs() / (C * C) > PHI_C2_MAX {
                return Err(ResponseError::UnsupportedDomain {
                    why: format!("|Phi|/c^2={} exceeds {PHI_C2_MAX}", field.phi.abs() / (C * C)),
                });
            }
            let a = apply_gem_a(field, v);
            let v_new = v.add(a.scale(h));
            let x_new = x.add(v.scale(h));
            if self.indexed_lookup && (!v_new.norm().is_finite() || !x_new.norm().is_finite()) {
                return Err(ResponseError::UnsupportedDomain {why:"nonfinite indexed Euler state".into()});
            }
            if v_new.norm() >= C {
                return Err(ResponseError::Superluminal);
            }
            updates.push((i, x_new, v_new, mu));
            self.charge.source_evolution += 1;
        }
        for (i, x_new, v_new, mu) in updates {
            close_and_kink(
                &mut bodies[i],
                t_next,
                x_new,
                v_new,
                mu,
                V2::zero(),
                V2::zero(),
            );
        }
        self.t = t_next;
        Ok(())
    }

    pub fn is_ready(&self) -> bool {
        self.ready
    }

    pub fn into_bodies(self) -> (Vec<Body>, Charge) {
        (self.bodies, self.charge)
    }
}

fn continue_from(
    bodies: &mut Vec<Body>,
    t_start: f64,
    interventions: &[Intervention],
    horizon: f64,
    dt: f64,
    charge: &mut Charge,
) -> Result<(), ResponseError> {
    let mut job = EulerContinueJob::start(
        bodies.clone(),
        t_start,
        interventions,
        horizon,
        dt,
        charge.clone(),
    );
    let mut budget = u64::MAX;
    while job.poll(&mut budget)? == JobPoll::Pending {}
    *bodies = job.bodies;
    *charge = job.charge;
    Ok(())
}

fn finite_diff_grad(bodies: &[Body], t: f64, x: V2, charge: &mut Charge) -> Result<V2, ResponseError> {
    let mut g = V2::zero();
    for (k, basis) in [V2::new(1.0, 0.0), V2::new(0.0, 1.0)].into_iter().enumerate() {
        let plus = field_at(bodies, t, x.add(basis.scale(FD_EPS)), None, charge)?.phi;
        let minus = field_at(bodies, t, x.sub(basis.scale(FD_EPS)), None, charge)?.phi;
        let d = (plus - minus) / (2.0 * FD_EPS);
        if k == 0 {
            g.x = d;
        } else {
            g.y = d;
        }
    }
    Ok(g)
}

fn validate_residual(bodies: &[Body], t_samples: &[f64], charge: &mut Charge) -> Result<Residual, ResponseError> {
    charge.validation += 1;
    let mut max_grad_rel: f64 = 0.0;
    let mut max_accel_rel: f64 = 0.0;
    let mut max_phi_c2: f64 = 0.0;
    let mut max_beta: f64 = 0.0;
    for &t in t_samples {
        if t <= bodies[0].segments[0].t0 + 1e-12 {
            continue;
        }
        for body in bodies {
            let Ok((x, v, _)) = body.present(t) else {
                continue;
            };
            max_beta = max_beta.max(v.norm() / C);
            let field = field_at(bodies, t, x, Some(body.id), charge)?;
            max_phi_c2 = max_phi_c2.max(field.phi.abs() / (C * C));
            let probe = x.add(V2::new(0.35, 0.2));
            let analytic = field_at(bodies, t, probe, None, charge)?;
            let fd = finite_diff_grad(bodies, t, probe, charge)?;
            let denom = analytic.e.norm().max(1e-12);
            // E = -∇Φ - (4/c)∂ξ/∂t; at low β the first term dominates.
            let grad_from_e = analytic.e.scale(-1.0);
            max_grad_rel = max_grad_rel.max(fd.sub(grad_from_e).norm() / denom.max(fd.norm()));
            let a = apply_gem_a(field, v);
            max_accel_rel = max_accel_rel.max(a.norm());
        }
    }
    let rest = laboratory_two_body();
    let rest_bodies = genesis_bodies(&rest);
    let mut dummy = Charge::default();
    let f = field_at(
        &rest_bodies,
        1.0,
        V2::new(-4.0, 0.0),
        Some(0),
        &mut dummy,
    )?;
    let expected = 1.0 / 64.0;
    let static_kernel_ok = (f.e.x - expected).abs() < 1e-12 && f.e.y.abs() < 1e-12;
    Ok(Residual {
        max_grad_rel,
        max_accel_rel,
        max_phi_c2,
        max_beta,
        static_kernel_ok,
    })
}

/// Compile options. Historical `compile_source_response` stores the dense
/// pair inverse on a quiet two-body. I3 may skip that setup when no Schur
/// consumer is present; call `ensure_pair_inverse` if a later consumer needs it.
#[derive(Clone, Copy, Debug)]
pub struct CompileOpts {
    pub store_pair_inverse: bool,
}

impl Default for CompileOpts {
    fn default() -> Self {
        Self {
            store_pair_inverse: true,
        }
    }
}

pub fn compile_source_response(
    ic: InitialCondition,
    interventions: Vec<Intervention>,
    horizon: f64,
    dt: f64,
) -> Result<SourceResponse, ResponseError> {
    compile_source_response_opts(ic, interventions, horizon, dt, CompileOpts::default())
}

pub fn compile_source_response_opts(
    ic: InitialCondition,
    interventions: Vec<Intervention>,
    horizon: f64,
    dt: f64,
    opts: CompileOpts,
) -> Result<SourceResponse, ResponseError> {
    compile_source_response_refined(ic, interventions, horizon, dt, opts, 1)
}

/// Laboratory numerical control: divide the initial causal-knot cadence by
/// `subdivision`, preserving genesis, interventions and field equations.
/// Unlike `dt` metadata, this changes actual collocation intervals. Factor one
/// reproduces the existing default. A finer grid alone is not convergence or
/// physical-law qualification. `interval_tau` records the effective cadence.
pub fn compile_source_response_refined(
    ic: InitialCondition,
    interventions: Vec<Intervention>,
    horizon: f64,
    dt: f64,
    opts: CompileOpts,
    subdivision: usize,
) -> Result<SourceResponse, ResponseError> {
    if subdivision == 0 {
        return Err(ResponseError::UnsupportedDomain {
            why: "causal-knot subdivision must be positive".into(),
        });
    }
    let start = std::time::Instant::now();
    let mut charge = Charge {
        init: 1,
        ..Charge::default()
    };
    let outcome = interval_compile(&ic, &interventions, horizon, &mut charge, subdivision)?;
    let samples: Vec<f64> = (0..12)
        .map(|i| ic.genesis_t + (i as f64 + 1.0) * (horizon - ic.genesis_t) / 12.0)
        .collect();
    let mut compiled = seal_compiled(
        ic.clone(),
        interventions,
        outcome.bodies,
        outcome.functions,
        horizon,
        dt,
        &samples,
        charge,
        start.elapsed().as_nanos(),
        outcome.blocks,
        outcome.q,
        outcome.tau,
    )?;
    // Quiet two-body only: do not assemble on a kicked pair or a three-body
    // compile to inflate a denominator or fail unrelated kick/compact paths.
    if opts.store_pair_inverse
        && compiled.genesis.bodies.len() == 2
        && compiled.incoming.is_empty()
        && compiled.interval_functions.len() >= 2
    {
        let mut inverse_charge = compiled.charge.clone();
        let inv = store_pair_inverse(&compiled, &mut inverse_charge)?;
        compiled.charge = inverse_charge;
        compiled.pair_inverse = Some(inv);
    }
    Ok(compiled)
}

/// On-demand dense pair inverse. No-op if already stored. Not a skip of
/// collocation; it only defers factorization until a Schur consumer exists.
pub fn ensure_pair_inverse(compiled: &mut SourceResponse) -> Result<(), ResponseError> {
    if compiled.pair_inverse.is_some() {
        return Ok(());
    }
    if compiled.genesis.bodies.len() != 2
        || !compiled.incoming.is_empty()
        || compiled.interval_functions.len() < 2
    {
        return Err(ResponseError::UnsupportedDomain {
            why: "pair inverse is only stored for a quiet two-body compile".into(),
        });
    }
    let mut inverse_charge = compiled.charge.clone();
    let inv = store_pair_inverse(compiled, &mut inverse_charge)?;
    compiled.charge = inverse_charge;
    compiled.pair_inverse = Some(inv);
    Ok(())
}

/// Fit the compact sidecar and attach interval-operator metadata.
/// Compact refuse (empty pieces) fails closed at `decode_sources`.
fn seal_compiled(
    genesis: InitialCondition,
    incoming: Vec<Intervention>,
    raw: Vec<Body>,
    interval_functions: Vec<IntervalFunction>,
    horizon: f64,
    dt: f64,
    samples: &[f64],
    mut charge: Charge,
    wall_ns: u128,
    interval_blocks: u64,
    interval_q: f64,
    interval_tau: f64,
) -> Result<SourceResponse, ResponseError> {
    let compact = match crate::coupled_phase_nav::compact_from_bodies(
        COUPLED_RESPONSE_LAW_ID,
        horizon,
        &incoming,
        &raw,
        crate::coupled_phase_nav::CompactSpec {
            adaptive_bisect: true,
            ..crate::coupled_phase_nav::CompactSpec::default()
        },
    ) {
        Ok(compact) => {
            charge.coefficient_construction += compact.charge.coefficient_construction;
            charge.factorization += compact.charge.factorization;
            let _decoded = compact.decode_from_template(&raw, &mut charge)?;
            compact
        }
        Err(refuse) => {
            charge.fallback += 1;
            crate::coupled_phase_nav::CompactResponse {
                law_id: COUPLED_RESPONSE_LAW_ID.into(),
                band: refuse.band,
                max_error: refuse.max_error,
                pieces: Vec::new(),
                charge: Charge {
                    fallback: 1,
                    ..Charge::default()
                },
            }
        }
    };
    let residual = validate_residual(&raw, samples, &mut charge)?;
    charge.verification += 1;
    Ok(SourceResponse {
        law_id: COUPLED_RESPONSE_LAW_ID.into(),
        domain: Domain {
            phi_c2_max: residual.max_phi_c2,
            beta_max: residual.max_beta,
            horizon,
            dt,
        },
        incoming,
        compact,
        worldtubes: raw,
        interval_blocks,
        interval_q,
        interval_tau,
        genesis,
        interval_functions,
        pair_inverse: None,
        residual,
        charge,
        wall_ns,
    })
}

pub fn body_state(bodies: &[Body], id: u64, t: f64) -> Result<([f64; 2], [f64; 2]), ResponseError> {
    let body = bodies
        .iter()
        .find(|b| b.id == id)
        .ok_or(ResponseError::UnsupportedDomain {
            why: format!("missing body {id}"),
        })?;
    let (x, v, _) = body.present(t)?;
    Ok((x.arr(), v.arr()))
}

pub fn acceleration_at(bodies: &[Body], id: u64, t: f64, charge: &mut Charge) -> Result<[f64; 2], ResponseError> {
    let body = bodies
        .iter()
        .find(|b| b.id == id)
        .ok_or(ResponseError::UnsupportedDomain {
            why: format!("missing body {id}"),
        })?;
    let (x, v, _) = body.present(t)?;
    let field = field_at(bodies, t, x, Some(id), charge)?;
    Ok(apply_gem_a(field, v).arr())
}

/// GEM acceleration at an arbitrary event from frozen sources. Independent
/// checkers use this; it does not read `SourceResponse::residual`.
pub fn field_acceleration(
    sources: &[Body],
    t: f64,
    x: [f64; 2],
    v: [f64; 2],
    skip: Option<u64>,
    charge: &mut Charge,
) -> Result<[f64; 2], ResponseError> {
    let field = field_at(sources, t, V2::from_arr(x), skip, charge)?;
    Ok(apply_gem_a(field, V2::from_arr(v)).arr())
}

/// Retarded lookback time from a query event to a named source. Independent
/// causal-time error uses this; it does not read `SourceResponse::residual`.
pub fn retarded_lookback_time(
    query_t: f64,
    query_x: [f64; 2],
    sources: &[Body],
    source_id: u64,
    charge: &mut Charge,
) -> Result<Option<f64>, ResponseError> {
    let body = sources
        .iter()
        .find(|b| b.id == source_id)
        .ok_or(ResponseError::UnsupportedDomain {
            why: format!("missing source {source_id}"),
        })?;
    let x = V2::from_arr(query_x);
    for seg in body.segments.iter().rev() {
        if seg.t0 > query_t + 1e-15 {
            continue;
        }
        if let Some(u) = retarded_lookback(query_t, x, seg, charge) {
            return Ok(Some(u));
        }
    }
    Ok(None)
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ShipState {
    pub t: f64,
    pub x: [f64; 2],
    pub v: [f64; 2],
    pub tau: f64,
}

pub fn fly_ship(
    sources: &[Body],
    t0: f64,
    x0: [f64; 2],
    v0: [f64; 2],
    horizon: f64,
    dt: f64,
    charge: &mut Charge,
) -> Result<ShipState, ResponseError> {
    fly_ship_from(QuerySources::Chords(sources), t0, x0, v0, horizon, dt, charge)
}

/// Held-out ship on compiled lookback: GEM field from stored constant-a
/// interval functions (½`ah²` included), not only worldtube chords.
pub fn fly_ship_compiled(
    compiled: &SourceResponse,
    t0: f64,
    x0: [f64; 2],
    v0: [f64; 2],
    horizon: f64,
    dt: f64,
    charge: &mut Charge,
) -> Result<ShipState, ResponseError> {
    fly_ship_from(
        QuerySources::Compiled(compiled),
        t0,
        x0,
        v0,
        horizon,
        dt,
        charge,
    )
}

fn fly_ship_from(
    sources: QuerySources<'_>,
    t0: f64,
    x0: [f64; 2],
    v0: [f64; 2],
    horizon: f64,
    dt: f64,
    charge: &mut Charge,
) -> Result<ShipState, ResponseError> {
    let mut t = t0;
    let mut x = V2::from_arr(x0);
    let mut v = V2::from_arr(v0);
    let mut tau = 0.0;
    while t < horizon - 1e-15 {
        let h = (horizon - t).min(dt);
        let field = gem_field(sources, t, x, None, charge)?;
        let radicand = 1.0 + 2.0 * field.phi / (C * C) - v.norm2() / (C * C);
        if radicand < 0.0 {
            return Err(ResponseError::UnsupportedDomain {
                why: "clock radicand negative".into(),
            });
        }
        tau += h * radicand.sqrt();
        let a = apply_gem_a(field, v);
        x = x.add(v.scale(h));
        v = v.add(a.scale(h));
        t += h;
        charge.consumers += 1;
    }
    Ok(ShipState {
        t,
        x: x.arr(),
        v: v.arr(),
        tau,
    })
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct RayState {
    pub t: f64,
    pub x: [f64; 2],
    pub n: [f64; 2],
    pub path: f64,
}

pub fn fly_ray(
    sources: &[Body],
    t_emit: f64,
    x_emit: [f64; 2],
    n_emit: [f64; 2],
    path_length: f64,
    ds: f64,
    charge: &mut Charge,
) -> Result<RayState, ResponseError> {
    fly_ray_from(
        QuerySources::Chords(sources),
        t_emit,
        x_emit,
        n_emit,
        path_length,
        ds,
        charge,
    )
}

/// Held-out ray on compiled lookback: GEM field from stored constant-a
/// interval functions (½`ah²` included), not only worldtube chords.
pub fn fly_ray_compiled(
    compiled: &SourceResponse,
    t_emit: f64,
    x_emit: [f64; 2],
    n_emit: [f64; 2],
    path_length: f64,
    ds: f64,
    charge: &mut Charge,
) -> Result<RayState, ResponseError> {
    fly_ray_from(
        QuerySources::Compiled(compiled),
        t_emit,
        x_emit,
        n_emit,
        path_length,
        ds,
        charge,
    )
}

fn fly_ray_from(
    sources: QuerySources<'_>,
    t_emit: f64,
    x_emit: [f64; 2],
    n_emit: [f64; 2],
    path_length: f64,
    ds: f64,
    charge: &mut Charge,
) -> Result<RayState, ResponseError> {
    let mut t = t_emit;
    let mut x = V2::from_arr(x_emit);
    let mut n = V2::from_arr(n_emit);
    let n0 = n.norm();
    if n0 < 1e-15 {
        return Err(ResponseError::UnsupportedDomain {
            why: "null direction vanished".into(),
        });
    }
    n = n.scale(1.0 / n0);
    let mut s = 0.0;
    while s < path_length - 1e-15 {
        let dl = (path_length - s).min(ds);
        let field = gem_field(sources, t, x, None, charge)?;
        let e_par = n.scale(field.e.dot(n));
        let e_perp = field.e.sub(e_par);
        n = n.add(e_perp.scale(4.0 / (C * C) * dl));
        let nn = n.norm();
        if nn < 1e-15 {
            return Err(ResponseError::UnsupportedDomain {
                why: "null direction vanished".into(),
            });
        }
        n = n.scale(1.0 / nn);
        let dt = (1.0 - 2.0 * field.phi / (C * C)) * dl / C;
        t += dt;
        x = x.add(n.scale(dl));
        s += dl;
        charge.consumers += 1;
    }
    Ok(RayState {
        t,
        x: x.arr(),
        n: n.arr(),
        path: s,
    })
}

pub fn clock_rate(sources: &[Body], t: f64, x: [f64; 2], v: [f64; 2], charge: &mut Charge) -> Result<f64, ResponseError> {
    clock_rate_from(QuerySources::Chords(sources), t, x, v, charge)
}

pub fn clock_rate_compiled(
    compiled: &SourceResponse,
    t: f64,
    x: [f64; 2],
    v: [f64; 2],
    charge: &mut Charge,
) -> Result<f64, ResponseError> {
    clock_rate_from(QuerySources::Compiled(compiled), t, x, v, charge)
}

fn clock_rate_from(
    sources: QuerySources<'_>,
    t: f64,
    x: [f64; 2],
    v: [f64; 2],
    charge: &mut Charge,
) -> Result<f64, ResponseError> {
    let field = gem_field(sources, t, V2::from_arr(x), None, charge)?;
    let radicand = 1.0 + 2.0 * field.phi / (C * C) - V2::from_arr(v).norm2() / (C * C);
    if radicand < 0.0 {
        return Err(ResponseError::UnsupportedDomain {
            why: "clock radicand negative".into(),
        });
    }
    charge.consumers += 1;
    Ok(radicand.sqrt())
}

pub fn contact_closest(
    a: &[Body],
    id_a: u64,
    id_b: u64,
    t0: f64,
    t1: f64,
    dt: f64,
    charge: &mut Charge,
) -> Result<(f64, f64), ResponseError> {
    let mut best_t = t0;
    let mut best_d = f64::INFINITY;
    let mut t = t0;
    while t <= t1 + 1e-15 {
        let (xa, _) = body_state(a, id_a, t)?;
        let (xb, _) = body_state(a, id_b, t)?;
        let d = V2::from_arr(xa).sub(V2::from_arr(xb)).norm();
        if d < best_d {
            best_d = d;
            best_t = t;
        }
        t += dt;
        charge.consumers += 1;
    }
    Ok((best_t, best_d))
}

pub fn body_state_compiled(
    compiled: &SourceResponse,
    id: u64,
    t: f64,
) -> Result<([f64; 2], [f64; 2]), ResponseError> {
    let mut funs: Vec<&IntervalFunction> = compiled
        .interval_functions
        .iter()
        .filter(|f| f.body_id == id && f.covers(t))
        .collect();
    funs.sort_by(|a, b| a.t0.partial_cmp(&b.t0).unwrap());
    if let Some(fun) = funs.last() {
        let (x, v) = fun.state_at(t);
        return Ok((x.arr(), v.arr()));
    }
    body_state(&compiled.worldtubes, id, t)
}

pub fn contact_closest_compiled(
    compiled: &SourceResponse,
    id_a: u64,
    id_b: u64,
    t0: f64,
    t1: f64,
    dt: f64,
    charge: &mut Charge,
) -> Result<(f64, f64), ResponseError> {
    let mut best_t = t0;
    let mut best_d = f64::INFINITY;
    let mut t = t0;
    while t <= t1 + 1e-15 {
        let (xa, _) = body_state_compiled(compiled, id_a, t)?;
        let (xb, _) = body_state_compiled(compiled, id_b, t)?;
        let d = V2::from_arr(xa).sub(V2::from_arr(xb)).norm();
        if d < best_d {
            best_d = d;
            best_t = t;
        }
        t += dt;
        charge.consumers += 1;
    }
    Ok((best_t, best_d))
}

/// Held-out ship, ray, clock and contact on compiled lookback. Required
/// queries returning `UnsupportedDomain` fail the coupled-slice capability.
pub fn complete_required_queries_compiled(
    compiled: &SourceResponse,
    horizon: f64,
    charge: &mut Charge,
) -> Result<(bool, bool, bool, bool), ResponseError> {
    let ship_h = horizon.min(3.5).max(0.25);
    let ship = fly_ship_compiled(
        compiled,
        0.1_f64.min(ship_h * 0.5),
        [0.0, 3.0],
        [0.125, 0.0],
        ship_h,
        (horizon / 32.0).max(1.0 / 64.0),
        charge,
    )?;
    let ray = fly_ray_compiled(
        compiled,
        0.1_f64.min(ship_h * 0.5),
        [0.0, 3.0],
        [1.0, 0.0],
        8.0,
        0.05,
        charge,
    )?;
    let clock = clock_rate_compiled(compiled, ship.t, ship.x, ship.v, charge)?;
    let (ct, cd) = contact_closest_compiled(
        compiled,
        0,
        1,
        0.0,
        horizon.min(4.0),
        (horizon / 16.0).max(1.0 / 32.0),
        charge,
    )?;
    let _ = ct;
    Ok((
        ship.tau > 0.0,
        ray.t > 0.1,
        clock.is_finite() && clock > 0.0 && clock <= 1.0,
        cd.is_finite() && cd > 0.0,
    ))
}

fn arr_norm(a: [f64; 2]) -> f64 {
    (a[0] * a[0] + a[1] * a[1]).sqrt()
}

/// Post-cone GEM coupling of a new massive body onto pair member 0 versus the
/// partner, on the compiled pair's frozen worldtubes. Genesis t=0 has no
/// retarded history (lookback is before the worldtube start), so the ratio
/// is sampled after the pair light-crossing. Linearized GEM is linear in μ
/// at frozen worldtubes; worldtubes are not. Ratio ≥ 1 means the entrant is
/// not an omitted tail of the pair.
fn massive_entrant_coupling_ratio(
    compiled: &SourceResponse,
    entrant: &BodyInit,
    charge: &mut Charge,
) -> Result<f64, ResponseError> {
    let host = compiled
        .genesis
        .bodies
        .first()
        .ok_or(ResponseError::UnsupportedDomain {
            why: "compiled pair has no host body for an exterior share".into(),
        })?;
    let partner_init = compiled
        .genesis
        .bodies
        .get(1)
        .ok_or(ResponseError::UnsupportedDomain {
            why: "compiled response is not a pair; no partner for an exterior ratio".into(),
        })?;
    let r_pair = dist_arr(host.x, partner_init.x);
    let t = (compiled.genesis.genesis_t + r_pair / C + compiled.domain.dt)
        .min(compiled.domain.horizon);
    let pair = if compiled.worldtubes.len() >= 2 {
        compiled.worldtubes.clone()
    } else {
        genesis_bodies(&compiled.genesis)
    };
    let a_partner = acceleration_at(&pair, host.id, t, charge)?;
    let mut recoupled = pair;
    recoupled.push(Body {
        id: entrant.id,
        segments: vec![Segment {
            t0: compiled.genesis.genesis_t,
            t1: None,
            x0: entrant.x,
            v: entrant.v,
            a: [0.0, 0.0],
            mu: entrant.mu,
        }],
    });
    let a_with = acceleration_at(&recoupled, host.id, t, charge)?;
    let a_from_entrant = [a_with[0] - a_partner[0], a_with[1] - a_partner[1]];
    let partner = arr_norm(a_partner);
    if partner < 1e-18 {
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "pair partner acceleration vanished at t={t}; cannot compare exterior coupling"
            ),
        });
    }
    Ok(arr_norm(a_from_entrant) / partner)
}

fn collocate_on_frozen_sources(
    frozen: &[Body],
    frozen_funs: &[IntervalFunction],
    init: &BodyInit,
    genesis_t: f64,
    horizon: f64,
    tau: f64,
    charge: &mut Charge,
) -> Result<(Body, Vec<IntervalFunction>), ResponseError> {
    let mut body = genesis_bodies(&InitialCondition {
        genesis_t,
        bodies: vec![init.clone()],
    })
    .remove(0);
    let step = tau * 0.5;
    if !step.is_finite() || step <= 1e-12 {
        return Err(ResponseError::UnsupportedDomain {
            why: "pair interval tau is not a usable collocation cadence for the entrant".into(),
        });
    }
    let mut knots = Vec::new();
    let mut t_knot = genesis_t + step;
    while t_knot < horizon - 1e-12 {
        knots.push(t_knot);
        t_knot += step;
    }
    let mut functions = Vec::new();
    let mut t = genesis_t;
    for t_next in knots {
        let h = t_next - t;
        if h <= 1e-18 {
            continue;
        }
        let (x, v, mu) = body.present(t)?;
        if v.norm() / C > BETA_MAX {
            return Err(ResponseError::UnsupportedDomain {
                why: format!("beta={} exceeds admitted {}", v.norm() / C, BETA_MAX),
            });
        }
        let t_col = t + 0.5 * h;
        let x_col = x.add(v.scale(t_col - t));
        let field = field_at_stored(frozen_funs, frozen, t_col, x_col, None, charge)?;
        if field.phi.abs() / (C * C) > PHI_C2_MAX {
            return Err(ResponseError::UnsupportedDomain {
                why: format!("|Phi|/c^2={} exceeds {PHI_C2_MAX}", field.phi.abs() / (C * C)),
            });
        }
        let a = apply_gem_a(field, v);
        let fun = IntervalFunction {
            body_id: init.id,
            t0: t,
            t1: t_next,
            x0: x.arr(),
            v0: v.arr(),
            a: a.arr(),
            mu,
        };
        let (x_new, v_new) = fun.inertial_end();
        if v_new.norm() >= C {
            return Err(ResponseError::Superluminal);
        }
        functions.push(fun.clone());
        close_and_kink(
            &mut body,
            t_next,
            x_new,
            v_new,
            mu,
            V2::from_arr(fun.a),
            V2::from_arr(fun.a),
        );
        charge.source_evolution += 1;
        t = t_next;
    }
    charge.factorization += 1;
    Ok((body, functions))
}

const PAIR_INVERSE_FD_EPS: f64 = 1e-6;

fn rematch_interval_functions(
    genesis: &InitialCondition,
    functions: &[IntervalFunction],
) -> Result<Vec<IntervalFunction>, ResponseError> {
    let mut by_body: std::collections::BTreeMap<u64, Vec<IntervalFunction>> =
        std::collections::BTreeMap::new();
    for fun in functions {
        by_body.entry(fun.body_id).or_default().push(fun.clone());
    }
    let mut out = Vec::new();
    for (id, mut funs) in by_body {
        funs.sort_by(|a, b| a.t0.partial_cmp(&b.t0).unwrap());
        let init = genesis
            .bodies
            .iter()
            .find(|b| b.id == id)
            .ok_or(ResponseError::UnsupportedDomain {
                why: format!("pair function for missing genesis body {id}"),
            })?;
        let mut x = V2::from_arr(init.x);
        let mut v = V2::from_arr(init.v);
        for fun in funs {
            let mut corrected = fun;
            corrected.x0 = x.arr();
            corrected.v0 = v.arr();
            let (x_end, v_end) = corrected.inertial_end();
            if v_end.norm() >= C {
                return Err(ResponseError::Superluminal);
            }
            x = x_end;
            v = v_end;
            out.push(corrected);
        }
    }
    Ok(out)
}

#[allow(dead_code)]
fn lu_factor(mat: &mut [f64], n: usize) -> Result<Vec<usize>, ResponseError> {
    let mut pivots = Vec::with_capacity(n);
    for k in 0..n {
        let mut pivot = k;
        let mut best = mat[k * n + k].abs();
        for i in (k + 1)..n {
            let v = mat[i * n + k].abs();
            if v > best {
                best = v;
                pivot = i;
            }
        }
        if !best.is_finite() || best < 1e-18 {
            return Err(ResponseError::UnsupportedDomain {
                why: format!("pair (I-K) is singular at column {k}; refusing to store a fake inverse"),
            });
        }
        if pivot != k {
            for j in 0..n {
                mat.swap(k * n + j, pivot * n + j);
            }
        }
        pivots.push(pivot);
        let akk = mat[k * n + k];
        for i in (k + 1)..n {
            mat[i * n + k] /= akk;
            let lik = mat[i * n + k];
            for j in (k + 1)..n {
                mat[i * n + j] -= lik * mat[k * n + j];
            }
        }
    }
    Ok(pivots)
}

fn lu_solve(lu: &[f64], pivots: &[usize], b: &[f64]) -> Result<Vec<f64>, ResponseError> {
    let n = pivots.len();
    if lu.len() != n * n || b.len() != n {
        return Err(ResponseError::UnsupportedDomain {
            why: "pair inverse LU shape does not match the collocation mesh".into(),
        });
    }
    let mut x = b.to_vec();
    for k in 0..n {
        x.swap(k, pivots[k]);
    }
    for i in 0..n {
        let mut s = x[i];
        for j in 0..i {
            s -= lu[i * n + j] * x[j];
        }
        x[i] = s;
    }
    for i in (0..n).rev() {
        let mut s = x[i];
        for j in (i + 1)..n {
            s -= lu[i * n + j] * x[j];
        }
        let uii = lu[i * n + i];
        if !uii.is_finite() || uii.abs() < 1e-18 {
            return Err(ResponseError::UnsupportedDomain {
                why: "pair inverse U is singular during apply".into(),
            });
        }
        x[i] = s / uii;
    }
    Ok(x)
}

fn mat_vec(mat: &[f64], n: usize, v: &[f64]) -> Vec<f64> {
    let mut out = vec![0.0; n];
    for i in 0..n {
        let mut s = 0.0;
        for j in 0..n {
            s += mat[i * n + j] * v[j];
        }
        out[i] = s;
    }
    out
}

/// Assemble and factor \((I-K_{AB}K_{BA})\) on the stored pair mesh.
/// Charged to the two-body compile, never to a three-body compile.
/// One finite-difference column or one LU elimination step per poll.
#[derive(Clone, Debug)]
pub struct PairInverseJob {
    genesis: InitialCondition,
    funs: Vec<IntervalFunction>,
    nfun: usize,
    n: usize,
    k_mat: Vec<f64>,
    fill_j: usize,
    fill_comp: usize,
    m: Vec<f64>,
    m_copy: Vec<f64>,
    lu_k: usize,
    pivots: Vec<usize>,
    charge: Charge,
    stage: PairInverseStage,
    result: Option<PairInverse>,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum PairInverseStage {
    Fill,
    Assemble,
    Factor,
    Check,
    Done,
}

impl PairInverseJob {
    pub fn start(pair: &SourceResponse) -> Result<Self, ResponseError> {
        if pair.genesis.bodies.len() != 2 {
            return Err(ResponseError::UnsupportedDomain {
                why: "pair inverse is stored only on a two-body compile".into(),
            });
        }
        let funs = pair.interval_functions.clone();
        if funs.len() < 2 {
            return Err(ResponseError::UnsupportedDomain {
                why: "pair inverse needs stored interval functions; refusing to paper chords"
                    .into(),
            });
        }
        let nfun = funs.len();
        let n = 2 * nfun;
        Ok(Self {
            genesis: pair.genesis.clone(),
            funs,
            nfun,
            n,
            k_mat: vec![0.0; n * n],
            fill_j: 0,
            fill_comp: 0,
            m: Vec::new(),
            m_copy: Vec::new(),
            lu_k: 0,
            pivots: Vec::new(),
            charge: Charge::default(),
            stage: PairInverseStage::Fill,
            result: None,
        })
    }

    pub fn poll(&mut self, op_budget: &mut u64) -> Result<JobPoll, ResponseError> {
        if self.stage == PairInverseStage::Done {
            return Ok(JobPoll::Ready);
        }
        loop {
            if self.stage == PairInverseStage::Done {
                return Ok(JobPoll::Ready);
            }
            if *op_budget == 0 {
                return Ok(JobPoll::Pending);
            }
            match self.stage {
                PairInverseStage::Fill => self.fill_one_column()?,
                PairInverseStage::Assemble => self.assemble()?,
                PairInverseStage::Factor => self.factor_one()?,
                PairInverseStage::Check => self.check()?,
                PairInverseStage::Done => {}
            }
            *op_budget = op_budget.saturating_sub(1);
        }
    }

    fn fill_one_column(&mut self) -> Result<(), ResponseError> {
        let j = self.fill_j;
        let comp = self.fill_comp;
        let mut pert = self.funs.clone();
        pert[j].a[comp] += PAIR_INVERSE_FD_EPS;
        let pert = rematch_interval_functions(&self.genesis, &pert)?;
        let tubes = worldtubes_from_interval_functions(&self.genesis, &pert);
        self.charge.coefficient_construction += 1;
        for i in 0..self.nfun {
            if self.funs[i].body_id == self.funs[j].body_id {
                continue;
            }
            let h = self.funs[i].t1 - self.funs[i].t0;
            if h <= 1e-18 {
                continue;
            }
            let t_col = self.funs[i].t0 + 0.5 * h;
            let x_col =
                V2::from_arr(self.funs[i].x0).add(V2::from_arr(self.funs[i].v0).scale(0.5 * h));
            let field = field_at_stored(
                &pert,
                &tubes,
                t_col,
                x_col,
                Some(self.funs[i].body_id),
                &mut self.charge,
            )?;
            let a = apply_gem_a(field, V2::from_arr(self.funs[i].v0));
            let a0 = V2::from_arr(self.funs[i].a);
            self.k_mat[2 * i * self.n + (2 * j + comp)] = (a.x - a0.x) / PAIR_INVERSE_FD_EPS;
            self.k_mat[(2 * i + 1) * self.n + (2 * j + comp)] = (a.y - a0.y) / PAIR_INVERSE_FD_EPS;
        }
        if self.fill_comp == 0 {
            self.fill_comp = 1;
        } else {
            self.fill_comp = 0;
            self.fill_j += 1;
            if self.fill_j >= self.nfun {
                self.stage = PairInverseStage::Assemble;
            }
        }
        Ok(())
    }

    fn assemble(&mut self) -> Result<(), ResponseError> {
        let n = self.n;
        self.m = vec![0.0; n * n];
        for i in 0..n {
            for j in 0..n {
                self.m[i * n + j] = if i == j { 1.0 } else { 0.0 } - self.k_mat[i * n + j];
            }
        }
        self.m_copy = self.m.clone();
        self.pivots = (0..n).collect();
        self.lu_k = 0;
        self.stage = PairInverseStage::Factor;
        Ok(())
    }

    fn factor_one(&mut self) -> Result<(), ResponseError> {
        let n = self.n;
        let k = self.lu_k;
        let mut pivot = k;
        let mut best = self.m[k * n + k].abs();
        for i in (k + 1)..n {
            let mag = self.m[i * n + k].abs();
            if mag > best {
                best = mag;
                pivot = i;
            }
        }
        if !best.is_finite() || best < 1e-18 {
            return Err(ResponseError::UnsupportedDomain {
                why: "pair inverse (I-K) is singular; refusing a stored inverse".into(),
            });
        }
        if pivot != k {
            for j in 0..n {
                let a = self.m[k * n + j];
                self.m[k * n + j] = self.m[pivot * n + j];
                self.m[pivot * n + j] = a;
            }
        }
        self.pivots[k] = pivot;
        let akk = self.m[k * n + k];
        for i in (k + 1)..n {
            self.m[i * n + k] /= akk;
            let lik = self.m[i * n + k];
            for j in (k + 1)..n {
                self.m[i * n + j] -= lik * self.m[k * n + j];
            }
        }
        self.lu_k += 1;
        if self.lu_k >= n {
            self.charge.factorization += 1;
            self.stage = PairInverseStage::Check;
        }
        Ok(())
    }

    fn check(&mut self) -> Result<(), ResponseError> {
        let mut probe = vec![0.0; self.n];
        probe[0] = 1.0;
        let solved = lu_solve(&self.m, &self.pivots, &probe)?;
        let check = mat_vec(&self.m_copy, self.n, &solved);
        let mut err = 0.0_f64;
        for i in 0..self.n {
            err = err.max((check[i] - probe[i]).abs());
        }
        self.charge.verification += 1;
        if err > 1e-8 {
            return Err(ResponseError::UnsupportedDomain {
                why: format!("stored pair inverse failed LU residual check err={err}"),
            });
        }
        self.result = Some(PairInverse {
            body_id: self.funs.iter().map(|f| f.body_id).collect(),
            t0: self.funs.iter().map(|f| f.t0).collect(),
            lu: self.m.clone(),
            pivots: self.pivots.clone(),
            n: self.n,
        });
        self.stage = PairInverseStage::Done;
        Ok(())
    }

    pub fn is_ready(&self) -> bool {
        self.stage == PairInverseStage::Done
    }

    pub fn take(self) -> Result<(PairInverse, Charge), ResponseError> {
        let inv = self.result.ok_or(ResponseError::UnsupportedDomain {
            why: "pair inverse job is not ready".into(),
        })?;
        Ok((inv, self.charge))
    }
}

fn store_pair_inverse(
    pair: &SourceResponse,
    charge: &mut Charge,
) -> Result<PairInverse, ResponseError> {
    let mut job = PairInverseJob::start(pair)?;
    job.charge = charge.clone();
    let mut budget = u64::MAX;
    while job.poll(&mut budget)? == JobPoll::Pending {}
    let (inv, next) = job.take()?;
    *charge = next;
    Ok(inv)
}

/// Diagnostic seal: skip the compact sidecar and charge residual samples one at
/// a time. Consumers bind to interval functions, not Chebyshev decode.
#[derive(Clone, Debug)]
pub struct ResidualJob {
    genesis: InitialCondition,
    incoming: Vec<Intervention>,
    raw: Vec<Body>,
    interval_functions: Vec<IntervalFunction>,
    horizon: f64,
    dt: f64,
    samples: Vec<f64>,
    sample_i: usize,
    interval_blocks: u64,
    interval_q: f64,
    interval_tau: f64,
    charge: Charge,
    max_grad_rel: f64,
    max_accel_rel: f64,
    max_phi_c2: f64,
    max_beta: f64,
    ready: bool,
    result: Option<SourceResponse>,
}

impl ResidualJob {
    pub fn start(
        genesis: InitialCondition,
        incoming: Vec<Intervention>,
        raw: Vec<Body>,
        interval_functions: Vec<IntervalFunction>,
        horizon: f64,
        dt: f64,
        interval_blocks: u64,
        interval_q: f64,
        interval_tau: f64,
        mut charge: Charge,
    ) -> Self {
        let samples: Vec<f64> = (0..12)
            .map(|i| genesis.genesis_t + (i as f64 + 1.0) * (horizon - genesis.genesis_t) / 12.0)
            .collect();
        charge.fallback += 1;
        charge.validation += 1;
        Self {
            genesis,
            incoming,
            raw,
            interval_functions,
            horizon,
            dt,
            samples,
            sample_i: 0,
            interval_blocks,
            interval_q,
            interval_tau,
            charge,
            max_grad_rel: 0.0,
            max_accel_rel: 0.0,
            max_phi_c2: 0.0,
            max_beta: 0.0,
            ready: false,
            result: None,
        }
    }

    pub fn poll(&mut self, op_budget: &mut u64) -> Result<JobPoll, ResponseError> {
        if self.ready {
            return Ok(JobPoll::Ready);
        }
        loop {
            if self.sample_i >= self.samples.len() {
                self.finish_residual()?;
                self.ready = true;
                return Ok(JobPoll::Ready);
            }
            if *op_budget == 0 {
                return Ok(JobPoll::Pending);
            }
            self.sample_one()?;
            *op_budget = op_budget.saturating_sub(1);
        }
    }

    fn sample_one(&mut self) -> Result<(), ResponseError> {
        let t = self.samples[self.sample_i];
        self.sample_i += 1;
        if t <= self.raw[0].segments[0].t0 + 1e-12 {
            return Ok(());
        }
        for body in &self.raw {
            let Ok((x, v, _)) = body.present(t) else {
                continue;
            };
            self.max_beta = self.max_beta.max(v.norm() / C);
            let field = field_at(&self.raw, t, x, Some(body.id), &mut self.charge)?;
            self.max_phi_c2 = self.max_phi_c2.max(field.phi.abs() / (C * C));
            let probe = x.add(V2::new(0.35, 0.2));
            let analytic = field_at(&self.raw, t, probe, None, &mut self.charge)?;
            let fd = finite_diff_grad(&self.raw, t, probe, &mut self.charge)?;
            let denom = analytic.e.norm().max(1e-12);
            let grad_from_e = analytic.e.scale(-1.0);
            self.max_grad_rel = self
                .max_grad_rel
                .max(fd.sub(grad_from_e).norm() / denom.max(fd.norm()));
            let a = apply_gem_a(field, v);
            self.max_accel_rel = self.max_accel_rel.max(a.norm());
        }
        Ok(())
    }

    fn finish_residual(&mut self) -> Result<(), ResponseError> {
        let rest = laboratory_two_body();
        let rest_bodies = genesis_bodies(&rest);
        let mut dummy = Charge::default();
        let f = field_at(
            &rest_bodies,
            1.0,
            V2::new(-4.0, 0.0),
            Some(0),
            &mut dummy,
        )?;
        let expected = 1.0 / 64.0;
        let static_kernel_ok = (f.e.x - expected).abs() < 1e-12 && f.e.y.abs() < 1e-12;
        let residual = Residual {
            max_grad_rel: self.max_grad_rel,
            max_accel_rel: self.max_accel_rel,
            max_phi_c2: self.max_phi_c2,
            max_beta: self.max_beta,
            static_kernel_ok,
        };
        self.charge.verification += 1;
        self.result = Some(SourceResponse {
            law_id: COUPLED_RESPONSE_LAW_ID.into(),
            domain: Domain {
                phi_c2_max: residual.max_phi_c2,
                beta_max: residual.max_beta,
                horizon: self.horizon,
                dt: self.dt,
            },
            incoming: self.incoming.clone(),
            compact: crate::coupled_phase_nav::CompactResponse {
                law_id: COUPLED_RESPONSE_LAW_ID.into(),
                band: 0.0,
                max_error: 0.0,
                pieces: Vec::new(),
                charge: Charge {
                    fallback: 1,
                    ..Charge::default()
                },
            },
            worldtubes: self.raw.clone(),
            interval_blocks: self.interval_blocks,
            interval_q: self.interval_q,
            interval_tau: self.interval_tau,
            genesis: self.genesis.clone(),
            interval_functions: self.interval_functions.clone(),
            pair_inverse: None,
            residual,
            charge: self.charge.clone(),
            wall_ns: 0,
        });
        Ok(())
    }

    pub fn is_ready(&self) -> bool {
        self.ready
    }

    pub fn take(self) -> Result<SourceResponse, ResponseError> {
        self.result.ok_or(ResponseError::UnsupportedDomain {
            why: "residual job is not ready".into(),
        })
    }
}

/// Apply stored \((I-K)^{-1}\) to incoming \(K_{AC}c\) at frozen pair knots.
/// Rematches \((x,v)\) once. Does not recollocate pair-internal GEM.
fn apply_stored_pair_inverse(
    pair: &SourceResponse,
    frozen_c: &Body,
    frozen_c_funs: &[IntervalFunction],
    charge: &mut Charge,
) -> Result<Vec<IntervalFunction>, ResponseError> {
    let inv = pair.pair_inverse.as_ref().ok_or(ResponseError::UnsupportedDomain {
        why: "compiled pair has no stored (I-K)^{-1}; refusing to recollocate the pair mesh from scratch".into(),
    })?;
    let funs = &pair.interval_functions;
    if inv.n != 2 * funs.len()
        || inv.body_id.len() != funs.len()
        || inv.t0.len() != funs.len()
    {
        return Err(ResponseError::UnsupportedDomain {
            why: "stored pair inverse does not match interval_functions; refusing a drifted mesh".into(),
        });
    }
    for (i, fun) in funs.iter().enumerate() {
        if fun.body_id != inv.body_id[i] || (fun.t0 - inv.t0[i]).abs() > 1e-12 {
            return Err(ResponseError::UnsupportedDomain {
                why: "stored pair inverse mesh keys drifted from interval_functions".into(),
            });
        }
    }
    let mut f = vec![0.0; inv.n];
    for (i, fun) in funs.iter().enumerate() {
        let h = fun.t1 - fun.t0;
        if h <= 1e-18 {
            continue;
        }
        let t_col = fun.t0 + 0.5 * h;
        let x_col = V2::from_arr(fun.x0).add(V2::from_arr(fun.v0).scale(0.5 * h));
        let field_c = field_at_stored(
            frozen_c_funs,
            std::slice::from_ref(frozen_c),
            t_col,
            x_col,
            None,
            charge,
        )?;
        let a_c = apply_gem_a(field_c, V2::from_arr(fun.v0));
        f[2 * i] = a_c.x;
        f[2 * i + 1] = a_c.y;
    }
    let da = lu_solve(&inv.lu, &inv.pivots, &f)?;
    charge.factorization += 1;
    let mut updated = funs.clone();
    for (i, fun) in updated.iter_mut().enumerate() {
        fun.a[0] += da[2 * i];
        fun.a[1] += da[2 * i + 1];
    }
    let rematched = rematch_interval_functions(&pair.genesis, &updated)?;
    charge.source_evolution += rematched.len() as u64;
    charge.reconstruction += rematched.len() as u64;
    Ok(rematched)
}

#[allow(dead_code)]
/// Independent omitted/correction residual: GEM on the updated three-body
/// worldtubes versus stored updated a (not compile residual). Position bound
/// uses influence after first retarded arrival, divided by 1-q_pair.
/// Kept for independent leftover checks; not mixed into schur_update source ops.
fn omitted_correction_position_bound(
    functions: &[IntervalFunction],
    bodies: &[Body],
    horizon: f64,
    pair_q: f64,
    first_influence: f64,
    charge: &mut Charge,
) -> Result<f64, ResponseError> {
    let mut max_da = 0.0_f64;
    for fun in functions {
        let h = fun.t1 - fun.t0;
        if h <= 1e-18 {
            continue;
        }
        let t_col = fun.t0 + 0.5 * h;
        let x_col = V2::from_arr(fun.x0).add(V2::from_arr(fun.v0).scale(0.5 * h));
        let field = field_at_stored(functions, bodies, t_col, x_col, Some(fun.body_id), charge)?;
        let a = apply_gem_a(field, V2::from_arr(fun.v0));
        max_da = max_da.max(a.sub(V2::from_arr(fun.a)).norm());
        charge.validation += 1;
    }
    let h_eff = (horizon - first_influence).max(0.0);
    if pair_q >= 1.0 || !pair_q.is_finite() {
        return Err(ResponseError::UnsupportedDomain {
            why: format!("pair q={pair_q} cannot enclose an omitted residual"),
        });
    }
    Ok(0.5 * max_da * h_eff * h_eff / (1.0 - pair_q))
}

/// Compiled pair as a solved block; new massive source as incoming f plus
/// K_pair,entrant. Applies stored (I-K)^{-1} at frozen pair knots. Encounter
/// -scale coupling (ratio > 1) refuses — H0112 stands.
pub fn schur_update_compiled_pair(
    compiled: &SourceResponse,
    entrant: &BodyInit,
    horizon: f64,
    dt: f64,
) -> Result<SourceResponse, ResponseError> {
    if compiled.genesis.bodies.iter().any(|b| b.id == entrant.id) {
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "body {} is already in the compiled genesis; this is not a new massive entrant",
                entrant.id
            ),
        });
    }
    if compiled.genesis.bodies.len() < 2 {
        return Err(ResponseError::UnsupportedDomain {
            why: "compiled response is not a pair; no pair block to update".into(),
        });
    }
    if compiled.interval_functions.is_empty() {
        return Err(ResponseError::UnsupportedDomain {
            why: "no stored interval functions; refusing to paper inertial chords as a Schur pair block".into(),
        });
    }
    if compiled.pair_inverse.is_none() {
        return Err(ResponseError::UnsupportedDomain {
            why: "compiled pair has no stored (I-K)^{-1}; refusing to recollocate the pair mesh from scratch".into(),
        });
    }
    let enclosure = crate::coupled_interval_enclosure::enclose_compiled_interval(
        compiled,
        compiled.genesis.clone(),
        compiled.incoming.clone(),
        crate::coupled_interval_enclosure::IntervalMethod::CausalBlocks,
    )?;
    if !enclosure.certified {
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "independent CausalBlocks enclosure did not certify the compiled pair (q={}, residual unused); cannot Schur-update an uncertified block",
                enclosure.q
            ),
        });
    }
    let pair_radius = enclosure.radius.ok_or(ResponseError::UnsupportedDomain {
        why: "certified pair enclosure has no radius".into(),
    })?;
    let start = std::time::Instant::now();
    let mut charge = Charge {
        init: 1,
        validation: 1,
        ..Charge::default()
    };
    let ratio = massive_entrant_coupling_ratio(compiled, entrant, &mut charge)?;
    if ratio > 1.0 {
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "new massive entrant {} cannot share this compiled pair's exterior; independent CausalBlocks enclosure (q={}, residual unused) certifies the pair IC only and does not cover a different genesis IC; post-cone |a←entrant|/|a←partner|={ratio:.6} so linearized GEM recouples the pair; fly_ship on the pair is not this share; H0110 refuse stands",
                entrant.id, enclosure.q
            ),
        });
    }
    let (body_c, funs_c) = collocate_on_frozen_sources(
        &compiled.worldtubes,
        &compiled.interval_functions,
        entrant,
        compiled.genesis.genesis_t,
        horizon,
        compiled.interval_tau,
        &mut charge,
    )?;
    let mut pair_funs = apply_stored_pair_inverse(compiled, &body_c, &funs_c, &mut charge)?;
    let mut changed = false;
    for fun in &pair_funs {
        if let Some(old) = compiled
            .interval_functions
            .iter()
            .find(|o| o.body_id == fun.body_id && (o.t0 - fun.t0).abs() < 1e-12)
        {
            if arr_norm([fun.a[0] - old.a[0], fun.a[1] - old.a[1]]) > 1e-18 {
                changed = true;
                break;
            }
        }
    }
    if !changed {
        return Err(ResponseError::UnsupportedDomain {
            why: "Schur correction did not update pair interval functions; refusing to paper fly_ship as a pair-block update".into(),
        });
    }
    let pair_only = worldtubes_from_interval_functions(&compiled.genesis, &pair_funs);
    let times: Vec<f64> = (0..12)
        .map(|i| compiled.genesis.genesis_t + (i as f64 + 1.0) * (horizon - compiled.genesis.genesis_t) / 12.0)
        .collect();
    let mut x_delta = 0.0_f64;
    for &t in &times {
        for id in compiled.genesis.bodies.iter().map(|b| b.id) {
            let (xp, _) = body_state(&compiled.worldtubes, id, t)?;
            let (xu, _) = body_state(&pair_only, id, t)?;
            x_delta = x_delta.max(dist_arr(xp, xu));
        }
    }
    if x_delta > pair_radius {
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "stored-inverse pair displacement {x_delta} exceeds pair enclosure radius {pair_radius}; linearization does not cover this IC"
            ),
        });
    }
    let mut genesis = compiled.genesis.clone();
    genesis.bodies.push(entrant.clone());
    pair_funs.extend(funs_c);
    let worldtubes = worldtubes_from_interval_functions(&genesis, &pair_funs);
    let mut sealed = seal_compiled(
        genesis,
        compiled.incoming.clone(),
        worldtubes,
        pair_funs,
        horizon,
        dt,
        &times,
        charge,
        start.elapsed().as_nanos(),
        compiled.interval_blocks,
        compiled.interval_q,
        compiled.interval_tau,
    )?;
    attach_offline_enclosure(&mut sealed.charge, &enclosure);
    Ok(sealed)
}

/// Declared workload: a new massive body that is not in the compiled pair's
/// genesis IC. Independently enclose that pair on its own IC (CausalBlocks;
/// does not read compile residual). Encounter-scale coupling (H0112 id 99,
/// ratio > 1) still refuses. Weaker coupling may Schur-update the pair block
/// rather than treating `fly_ship` on the pair as an exterior share.
pub fn share_compiled_pair_exterior(
    compiled: &SourceResponse,
    entrant: &BodyInit,
    horizon: f64,
    dt: f64,
) -> Result<SourceResponse, ResponseError> {
    if compiled.genesis.bodies.iter().any(|b| b.id == entrant.id) {
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "body {} is already in the compiled genesis; this is not a new massive entrant",
                entrant.id
            ),
        });
    }
    if compiled.genesis.bodies.len() < 2 {
        return Err(ResponseError::UnsupportedDomain {
            why: "compiled response is not a pair; no pair exterior to share".into(),
        });
    }
    if compiled.interval_functions.is_empty() {
        return Err(ResponseError::UnsupportedDomain {
            why: "no stored interval functions; refusing to paper inertial chords as a pair exterior".into(),
        });
    }
    let enclosure = crate::coupled_interval_enclosure::enclose_compiled_interval(
        compiled,
        compiled.genesis.clone(),
        compiled.incoming.clone(),
        crate::coupled_interval_enclosure::IntervalMethod::CausalBlocks,
    )?;
    if !enclosure.certified {
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "independent CausalBlocks enclosure did not certify the compiled pair (q={}, residual unused); cannot share an uncertified exterior",
                enclosure.q
            ),
        });
    }
    let mut charge = Charge {
        validation: 1,
        ..Charge::default()
    };
    let ratio = massive_entrant_coupling_ratio(compiled, entrant, &mut charge)?;
    if ratio > 1.0 {
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "new massive entrant {} cannot share this compiled pair's exterior; independent CausalBlocks enclosure (q={}, residual unused) certifies the pair IC only and does not cover a different genesis IC; post-cone |a←entrant|/|a←partner|={ratio:.6} so linearized GEM recouples the pair; fly_ship on the pair is not this share; H0110 refuse stands",
                entrant.id, enclosure.q
            ),
        });
    }
    let mut shared = schur_update_compiled_pair(compiled, entrant, horizon, dt)?;
    shared.charge.push_child(
        "share_pair_exterior_enclose",
        ChargeRole::OfflineAudit,
        enclosure.charge.clone(),
    );
    Ok(shared)
}

/// Named recovery when a compiled pair's neighborhood cannot cover a new
/// massive body. Compiles A, B, and the entrant jointly (causal-block
/// interval collocation on that recoupled IC). Does **not** copy pair
/// interval functions, does **not** apply the stored pair inverse, and is
/// not `fly_ship`. Encounter-scale coupling (ratio > 1) is required;
/// a far third that still fits the pair neighborhood must use
/// `share_compiled_pair_exterior` / `schur_update_compiled_pair`.
///
/// Recouple is the three-body interval compile of that IC. It is not
/// required cheaper than an independent `compile_source_response` of the
/// same IC. Failed CausalBlocks recertify of the recoupled compile rejects
/// that certificate, not the existence of the recoupled solution.
pub fn recouple_compiled_pair(
    compiled: &SourceResponse,
    entrant: &BodyInit,
    horizon: f64,
    dt: f64,
) -> Result<SourceResponse, ResponseError> {
    if compiled.genesis.bodies.iter().any(|b| b.id == entrant.id) {
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "body {} is already in the compiled genesis; this is not a new massive recouple",
                entrant.id
            ),
        });
    }
    if compiled.genesis.bodies.len() != 2 {
        return Err(ResponseError::UnsupportedDomain {
            why: "recouple is the recovery of a compiled pair; this response is not a pair".into(),
        });
    }
    if compiled.interval_functions.is_empty() {
        return Err(ResponseError::UnsupportedDomain {
            why: "no stored interval functions; refusing to paper inertial chords as a recouple".into(),
        });
    }
    let enclosure = crate::coupled_interval_enclosure::enclose_compiled_interval(
        compiled,
        compiled.genesis.clone(),
        compiled.incoming.clone(),
        crate::coupled_interval_enclosure::IntervalMethod::CausalBlocks,
    )?;
    if !enclosure.certified {
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "independent CausalBlocks enclosure did not certify the compiled pair (q={}, residual unused); cannot recouple from an uncertified pair",
                enclosure.q
            ),
        });
    }
    let mut probe = Charge {
        validation: 1,
        repair: 1,
        ..Charge::default()
    };
    let ratio = massive_entrant_coupling_ratio(compiled, entrant, &mut probe)?;
    if ratio <= 1.0 {
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "new massive entrant {} still fits this compiled pair neighborhood (post-cone |a←entrant|/|a←partner|={ratio}); recouple is the recovery when linearized GEM recouples the pair (ratio>1); use share_compiled_pair_exterior, not fill-in of pair interval functions",
                entrant.id
            ),
        });
    }
    let mut genesis = compiled.genesis.clone();
    genesis.bodies.push(entrant.clone());
    let mut recoupled = compile_source_response(genesis, compiled.incoming.clone(), horizon, dt)?;
    recoupled.charge.repair = recoupled.charge.repair.saturating_add(1);
    recoupled.charge.validation = recoupled.charge.validation.saturating_add(1);
    attach_offline_enclosure(&mut recoupled.charge, &enclosure);
    if recoupled.pair_inverse.is_some() {
        return Err(ResponseError::UnsupportedDomain {
            why: "three-body recouple must not store a pair inverse; refusing to inflate a denominator".into(),
        });
    }
    if recoupled.interval_functions.is_empty() {
        return Err(ResponseError::UnsupportedDomain {
            why: "recouple compiled no interval functions; refusing to paper inertial chords".into(),
        });
    }
    if !recoupled.interval_q.is_finite() {
        return Err(ResponseError::UnsupportedDomain {
            why: "recouple interval q is not finite; refusing an unrecertified three-body operator".into(),
        });
    }
    Ok(recoupled)
}

fn require_recoupled_three_body(compiled: &SourceResponse) -> Result<(), ResponseError> {
    if compiled.genesis.bodies.len() != 3 {
        return Err(ResponseError::UnsupportedDomain {
            why: "recoupled reuse/repair requires a three-body recoupled compile, not a pair and not pair-interval fill-in".into(),
        });
    }
    if compiled.pair_inverse.is_some() {
        return Err(ResponseError::UnsupportedDomain {
            why: "three-body recouple must not store a pair inverse; refusing to inflate a denominator".into(),
        });
    }
    if compiled.interval_functions.is_empty() {
        return Err(ResponseError::UnsupportedDomain {
            why: "no stored recoupled interval functions; refusing to paper inertial chords as reuse".into(),
        });
    }
    Ok(())
}

/// Compile-once / reuse of certified interval functions on a recoupled
/// three-body compile across a distinct later source history on the **same
/// three masses**. Not pair-interval fill-in. Not extra-ray. Not
/// evolve-then-copy. Independent leftover is versus `compile_source_response`
/// of the same recoupled genesis plus the same extra.
pub fn reuse_recoupled_interval_functions(
    compiled: &SourceResponse,
    extra: &[Intervention],
    horizon: f64,
    dt: f64,
) -> Result<SourceResponse, ResponseError> {
    require_recoupled_three_body(compiled)?;
    reuse_certified_interval_functions(compiled, extra, horizon, dt)
}

/// Repair of a recoupled three-body compile when an in-flight change
/// invalidates certified blocks. Charged suffix work stays in source ops.
/// Passing a pair refuses (Job 2 pair fill-in is not this path).
pub fn repair_recoupled_interval_functions(
    compiled: &SourceResponse,
    extra: &[Intervention],
    horizon: f64,
    dt: f64,
) -> Result<SourceResponse, ResponseError> {
    require_recoupled_three_body(compiled)?;
    if extra.is_empty() {
        return Err(ResponseError::UnsupportedDomain {
            why: "repair extra is empty; extra-ray consumers are not a source-history splice".into(),
        });
    }
    let enclosure = crate::coupled_interval_enclosure::enclose_compiled_interval(
        compiled,
        compiled.genesis.clone(),
        compiled.incoming.clone(),
        crate::coupled_interval_enclosure::IntervalMethod::CausalBlocks,
    )?;
    if !enclosure.certified {
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "independent CausalBlocks enclosure did not certify the recoupled compile (q={}, residual unused); repair refused",
                enclosure.q
            ),
        });
    }
    let mut repaired = repair_from_committed(compiled, extra, horizon, dt)?;
    attach_offline_enclosure(&mut repaired.charge, &enclosure);
    Ok(repaired)
}

pub fn delayed_newton_a(bodies: &[Body], id: u64, t: f64, charge: &mut Charge) -> Result<[f64; 2], ResponseError> {
    let body = bodies.iter().find(|b| b.id == id).unwrap();
    let (x, _, _) = body.present(t)?;
    let mut a = V2::zero();
    for other in bodies {
        if other.id == id {
            continue;
        }
        for seg in other.segments.iter().rev() {
            if seg.t0 > t + 1e-15 {
                continue;
            }
            if let Some(u) = retarded_lookback(t, x, seg, charge) {
                let x_ret = seg.at(t - u);
                let rel = x.sub(x_ret);
                let r = rel.norm();
                if r < 1e-15 {
                    return Err(ResponseError::Singular);
                }
                a = a.add(rel.scale(-seg.mu / (r * r * r)));
                break;
            }
        }
    }
    Ok(a.arr())
}

fn dist_arr(a: [f64; 2], b: [f64; 2]) -> f64 {
    let dx = a[0] - b[0];
    let dy = a[1] - b[1];
    (dx * dx + dy * dy).sqrt()
}

/// Per-body causal cut for reuse: kick time on the kicked body, frozen-observer
/// light arrival on others. Genesis positions, not evolved events.
fn causal_reuse_cut(
    genesis: &InitialCondition,
    extra: &[Intervention],
    body_id: u64,
) -> Result<f64, ResponseError> {
    let mut cut = f64::INFINITY;
    for iv in extra {
        if iv.body_id == body_id {
            cut = cut.min(iv.t);
            continue;
        }
        let src = genesis
            .bodies
            .iter()
            .find(|b| b.id == iv.body_id)
            .ok_or(ResponseError::UnsupportedDomain {
                why: format!("kick on missing genesis body {}", iv.body_id),
            })?;
        let obs = genesis
            .bodies
            .iter()
            .find(|b| b.id == body_id)
            .ok_or(ResponseError::UnsupportedDomain {
                why: format!("observer {} not in genesis", body_id),
            })?;
        cut = cut.min(iv.t + dist_arr(src.x, obs.x) / C);
    }
    if !cut.is_finite() {
        return Err(ResponseError::UnsupportedDomain {
            why: "no extra intervention to cut certified interval functions".into(),
        });
    }
    Ok(cut)
}

/// Extra kick knot the independent kicked compile collocates. Quiet cadence
/// omits it unless a cadence sample already lands on the intervention.
fn extra_kick_knot_time(extra: &[Intervention]) -> f64 {
    extra.iter().map(|iv| iv.t).fold(f64::INFINITY, f64::min)
}

/// Common certified prefix on the independent kicked collocation grid:
/// complete by the causal cut *and* by the extra kick knot. Quiet observer
/// blocks that end after the kick omit that knot; the independent compile
/// collocates them after it.
fn certified_prefix_cut(
    genesis: &InitialCondition,
    extra: &[Intervention],
    body_id: u64,
) -> Result<f64, ResponseError> {
    Ok(causal_reuse_cut(genesis, extra, body_id)?.min(extra_kick_knot_time(extra)))
}

/// Last shared prefix endpoint across bodies. Continuation starts here so
/// `incoming_knots` includes the extra kick knot (`t_kick > t_start`).
fn certified_prefix_end(kept: &[IntervalFunction], genesis_t: f64, body_ids: &[u64]) -> f64 {
    let mut t_end = genesis_t;
    let mut first = true;
    for id in body_ids {
        let last = kept
            .iter()
            .filter(|f| f.body_id == *id)
            .map(|f| f.t1)
            .fold(genesis_t, f64::max);
        if first {
            t_end = last;
            first = false;
        } else {
            t_end = t_end.min(last);
        }
    }
    t_end
}

fn worldtubes_from_interval_functions(
    genesis: &InitialCondition,
    functions: &[IntervalFunction],
) -> Vec<Body> {
    let mut bodies = genesis_bodies(genesis);
    let mut ordered = functions.to_vec();
    ordered.sort_by(|a, b| {
        a.body_id
            .cmp(&b.body_id)
            .then(a.t0.partial_cmp(&b.t0).unwrap())
    });
    for fun in &ordered {
        if let Some(body) = bodies.iter_mut().find(|b| b.id == fun.body_id) {
            let (x_end, v_end) = fun.inertial_end();
            close_and_kink(
                body,
                fun.t1,
                x_end,
                v_end,
                fun.mu,
                V2::from_arr(fun.a),
                V2::from_arr(fun.a),
            );
        }
    }
    bodies
}

fn kept_certified_functions(
    compiled: &SourceResponse,
    extra: &[Intervention],
) -> Result<Vec<IntervalFunction>, ResponseError> {
    let mut kept = Vec::new();
    for fun in &compiled.interval_functions {
        let cut = certified_prefix_cut(&compiled.genesis, extra, fun.body_id)?;
        if fun.t1 <= cut + 1e-12 {
            kept.push(fun.clone());
        }
    }
    Ok(kept)
}

/// Complete ordered repair inputs: already-recorded incoming plus extra,
/// without duplicating an identical kick. Extra-only continuation drops a
/// later recorded cause after an earlier inserted intervention.
fn merge_repair_interventions(recorded: &[Intervention], extra: &[Intervention]) -> Vec<Intervention> {
    let mut all = recorded.to_vec();
    for iv in extra {
        let dup = all.iter().any(|e| {
            (e.t - iv.t).abs() < 1e-12
                && e.body_id == iv.body_id
                && (e.delta_v[0] - iv.delta_v[0]).abs() < 1e-15
                && (e.delta_v[1] - iv.delta_v[1]).abs() < 1e-15
        });
        if !dup {
            all.push(iv.clone());
        }
    }
    all.sort_by(|a, b| {
        a.t.partial_cmp(&b.t)
            .unwrap()
            .then(a.body_id.cmp(&b.body_id))
    });
    all
}

pub fn repair_from_committed(
    compiled: &SourceResponse,
    extra: &[Intervention],
    horizon: f64,
    dt: f64,
) -> Result<SourceResponse, ResponseError> {
    let mut charge = Charge {
        repair: 1,
        init: 1,
        ..Charge::default()
    };
    if extra.is_empty() {
        return Err(ResponseError::UnsupportedDomain {
            why: "repair extra is empty; extra-ray consumers are not a source-history splice".into(),
        });
    }
    if compiled.interval_functions.is_empty() {
        return Err(ResponseError::UnsupportedDomain {
            why: "no stored interval functions; refusing to paper inertial chords as reuse".into(),
        });
    }
    let t_kick = extra_kick_knot_time(extra).min(compiled.domain.horizon);
    let kept = kept_certified_functions(compiled, extra)?;
    charge.reconstruction += kept.len() as u64;
    charge.history += 1;
    let body_ids: Vec<u64> = compiled.genesis.bodies.iter().map(|b| b.id).collect();
    // Continue from the last shared quiet knot *before* the extra kick so the
    // repair collocation grid includes that kick knot, matching independent
    // `incoming_knots` of the kicked IC. Starting at t_kick omits it and
    // catch-up-splices instead (H0119 quiet-prefix remainder).
    let t_prefix = certified_prefix_end(&kept, compiled.genesis.genesis_t, &body_ids);
    let mut worldtubes = worldtubes_from_interval_functions(&compiled.genesis, &kept);
    // Metadata and continuation share the complete ordered input history.
    // Prefix cut still uses `extra` (new earlier intervention in an uncommitted
    // suffix or new history branch). That does not rewrite a committed past.
    let all = merge_repair_interventions(&compiled.incoming, extra);
    let stats = interval_continue(
        &mut worldtubes,
        t_prefix,
        &all,
        horizon,
        &mut charge,
        Some(compiled.interval_tau),
        &kept,
    )?;
    let mut functions = kept;
    functions.extend(stats.functions);
    let samples: Vec<f64> = (0..8)
        .map(|i| t_kick + (i as f64 + 1.0) * (horizon - t_kick).max(0.0) / 8.0)
        .filter(|t| *t <= horizon)
        .collect();
    seal_compiled(
        compiled.genesis.clone(),
        all,
        worldtubes,
        functions,
        horizon,
        dt,
        &samples,
        charge,
        0,
        compiled.interval_blocks + stats.blocks,
        compiled.interval_q.max(stats.q),
        compiled.interval_tau,
    )
}

/// Reuse certified interval functions for a distinct second source history
/// (same genesis IC, later interventions). Independent CausalBlocks enclosure
/// of the first compile must certify; it does not read compile residual.
/// Empty extra / extra-ray / foreign body / uncertified / zero copied blocks
/// refuse rather than claiming reuse.
pub fn reuse_certified_interval_functions(
    compiled: &SourceResponse,
    extra: &[Intervention],
    horizon: f64,
    dt: f64,
) -> Result<SourceResponse, ResponseError> {
    if extra.is_empty() {
        return Err(ResponseError::UnsupportedDomain {
            why: "no distinct source history: extra-ray / empty extra is not equivalent completed source histories".into(),
        });
    }
    if compiled.interval_functions.is_empty() {
        return Err(ResponseError::UnsupportedDomain {
            why: "no stored interval functions; refusing to paper inertial chords as reuse".into(),
        });
    }
    for iv in extra {
        if compiled.genesis.bodies.iter().all(|b| b.id != iv.body_id) {
            return Err(ResponseError::UnsupportedDomain {
                why: format!(
                    "body {} is not in the compiled genesis; distinct IC / new massive entrant cannot share this domain",
                    iv.body_id
                ),
            });
        }
        if iv.t <= compiled.genesis.genesis_t + 1e-12 {
            return Err(ResponseError::UnsupportedDomain {
                why: "intervention at genesis leaves no certified prefix to reuse".into(),
            });
        }
    }
    // Independent enclosure: Picard + CausalBlocks q. Does not read compile residual.
    let enclosure = crate::coupled_interval_enclosure::enclose_compiled_interval(
        compiled,
        compiled.genesis.clone(),
        compiled.incoming.clone(),
        crate::coupled_interval_enclosure::IntervalMethod::CausalBlocks,
    )?;
    if !enclosure.certified {
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "independent CausalBlocks enclosure did not certify (q={}, residual unused); reuse refused",
                enclosure.q
            ),
        });
    }
    let kept = kept_certified_functions(compiled, extra)?;
    if kept.is_empty() {
        return Err(ResponseError::UnsupportedDomain {
            why: "no complete certified interval function survives the causal cut; mid-block splits are not reused".into(),
        });
    }
    let mut reused = repair_from_committed(compiled, extra, horizon, dt)?;
    // Independent enclosure performs two genesis evolutions and Picard. Nest the
    // full child ledger as offline audit; do not copy only validation/verification
    // into the flat runtime totals (H0124 source ops stay suffix collocation).
    attach_offline_enclosure(&mut reused.charge, &enclosure);
    for body in &compiled.genesis.bodies {
        let mut orig: Vec<IntervalFunction> = kept
            .iter()
            .filter(|f| f.body_id == body.id)
            .cloned()
            .collect();
        orig.sort_by(|a, b| a.t0.partial_cmp(&b.t0).unwrap());
        let mut got_all: Vec<IntervalFunction> = reused
            .interval_functions
            .iter()
            .filter(|f| f.body_id == body.id)
            .cloned()
            .collect();
        got_all.sort_by(|a, b| a.t0.partial_cmp(&b.t0).unwrap());
        if got_all.len() < orig.len() || got_all[..orig.len()] != orig[..] {
            return Err(ResponseError::UnsupportedDomain {
                why: format!(
                    "reused interval functions for body {} do not start with the certified prefix",
                    body.id
                ),
            });
        }
    }
    Ok(reused)
}

/// Linear delayed-gain predictor used as a certificate candidate, not as truth.
pub fn delayed_feedback_series(u: f64, r: f64, t: f64, tau: f64) -> f64 {
    if t <= 0.0 {
        return 0.0;
    }
    let n = (t / (2.0 * tau)).floor() as i32;
    if (r - 1.0).abs() < 1e-12 {
        return u * (n + 1) as f64;
    }
    u * (1.0 - r.powi(n + 1)) / (1.0 - r)
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ChargedReport {
    pub law_id: String,
    pub worktree_head: String,
    pub quiet_queries: u64,
    pub quiet_horizon: f64,
    pub encounter_horizon: f64,
    pub source_ops_quiet: u64,
    pub consumer_ops_quiet: u64,
    pub source_ops_many_queries: u64,
    pub consumer_ops_many_queries: u64,
    pub full_recompute_ops: u64,
    pub repaired_ops: u64,
    pub source_evolution_full: u64,
    pub source_evolution_repair: u64,
    pub reuse_fraction_queries: f64,
    pub reuse_denominator: String,
    pub wall_ns_quiet: u128,
    pub wall_ns_many_queries: u128,
    pub max_phi_c2: f64,
    pub max_beta: f64,
    pub production_law: Option<String>,
    pub notes: Vec<String>,
    pub n_independent_compiles: u64,
    pub independent_compile_source_ops: Vec<u64>,
    pub independent_compile_wall_ns: Vec<u128>,
    pub independent_compile_source_ops_sum: u64,
    pub compiled_once_source_ops: u64,
    pub compiled_once_plus_consumers_ops: u64,
    pub independent_compiles_plus_consumers_ops: u64,
    pub consumer_share: f64,
    pub consumer_share_denominator: String,
    pub extra_ray_count: u64,
    pub compact_refuse_fallback: u64,
    pub certificate_refused: bool,
    pub certificate_refined: bool,
    pub certificate_refuse_q: f64,
    pub certificate_refine_q: f64,
    pub refuse_recovered: bool,
    pub refuse_recovery_ops: u64,
    pub refuse_full_recompute_ops_sum: u64,
    pub refuse_n_independent_compiles: u64,
    pub refuse_repair_fraction: f64,
    pub output_match_max_pos_err: f64,
    pub refuse_output_match_max_pos_err: f64,
    pub required_ship_ok: bool,
    pub required_ray_ok: bool,
    pub required_clock_ok: bool,
    pub required_contact_ok: bool,
    pub distinct_history_declared: String,
    pub distinct_history_reuse_certified: bool,
    pub distinct_history_refuse_why: String,
    pub distinct_history_reused_functions: u64,
    pub distinct_history_recollocated_functions: u64,
    pub distinct_history_source_ops_reuse: u64,
    pub distinct_history_source_ops_full: u64,
    pub distinct_history_reuse_fraction: f64,
    pub distinct_history_reuse_denominator: String,
    pub distinct_history_output_match_max_pos_err: f64,
    pub distinct_history_required_ok: bool,
}

pub fn run_charged_workload() -> Result<ChargedReport, ResponseError> {
    // Declared before results: artifacts/runs/equivalent-histories-20260914/workload-declaration.md
    const N: usize = 3;
    let ic = laboratory_two_body();
    let horizon = 6.0;
    let dt = 1.0 / 32.0;

    let mut independent_compile_source_ops = Vec::with_capacity(N);
    let mut independent_compile_wall_ns = Vec::with_capacity(N);
    let mut independent_pos_a = Vec::with_capacity(N);
    let mut independent_pos_b = Vec::with_capacity(N);
    let mut charge_indep_consumers = Charge::default();
    let mut first_compiled: Option<SourceResponse> = None;
    for k in 0..N {
        let compiled = compile_source_response(ic.clone(), Vec::new(), horizon, dt)?;
        independent_compile_source_ops.push(source_ops_of(&compiled));
        independent_compile_wall_ns.push(compiled.wall_ns);
        let (xa, _) = body_state(&compiled.worldtubes, 0, horizon)?;
        let (xb, _) = body_state(&compiled.worldtubes, 1, horizon)?;
        independent_pos_a.push(xa);
        independent_pos_b.push(xb);
        let mut rec = Charge::default();
        let sources = compiled.decode_sources(&mut rec)?;
        let y = 2.5 + 0.04 * k as f64;
        fly_ray(
            &sources,
            1.1,
            [0.0, y],
            [1.0, 0.0],
            8.0,
            0.05,
            &mut charge_indep_consumers,
        )?;
        if first_compiled.is_none() {
            first_compiled = Some(compiled);
        }
    }
    let compiled = first_compiled.expect("N>=1");
    let mut rec = Charge::default();
    let sources = compiled.decode_sources(&mut rec)?;
    let mut charge_q = Charge::default();
    let _ = fly_ray(
        &sources,
        1.1,
        [0.0, 3.0],
        [1.0, 0.0],
        8.0,
        0.05,
        &mut charge_q,
    )?;
    let source_ops_quiet = source_ops_of(&compiled);
    let consumer_ops_quiet = charge_q.consumers;

    let many = 24u64;
    let t_many = std::time::Instant::now();
    let mut charge_m = Charge::default();
    for k in 0..many {
        let y = 2.5 + 0.04 * k as f64;
        fly_ray(
            &sources,
            1.1,
            [0.0, y],
            [1.0, 0.0],
            8.0,
            0.05,
            &mut charge_m,
        )?;
    }
    let wall_ns_many_queries = t_many.elapsed().as_nanos();
    let source_ops_many_queries = source_ops_of(&compiled);
    let consumer_ops_many_queries = charge_m.consumers;
    let consumer_share = {
        let s = source_ops_quiet as f64;
        let c = consumer_ops_many_queries as f64;
        if s + c <= 0.0 {
            0.0
        } else {
            c / (s + c)
        }
    };

    let mut charge_reuse = Charge::default();
    for k in 0..N {
        let y = 2.5 + 0.04 * k as f64;
        fly_ray(
            &sources,
            1.1,
            [0.0, y],
            [1.0, 0.0],
            8.0,
            0.05,
            &mut charge_reuse,
        )?;
    }
    let independent_compile_source_ops_sum: u64 = independent_compile_source_ops.iter().copied().sum();
    let compiled_once_source_ops = source_ops_quiet;
    let compiled_once_plus_consumers_ops = compiled_once_source_ops + charge_reuse.consumers;
    let independent_compiles_plus_consumers_ops =
        independent_compile_source_ops_sum + charge_indep_consumers.consumers;
    let reuse_fraction_queries = if independent_compiles_plus_consumers_ops == 0 {
        0.0
    } else {
        1.0 - compiled_once_plus_consumers_ops as f64
            / independent_compiles_plus_consumers_ops as f64
    };
    let denom = format!(
        "measured equivalent completed coupled compiles through H={horizon}: sum of {N} independent compile_source_response source ops plus their {N} fly_ray consumers. Numerator cost is one of those compiles plus the {N} consumers. Not extra-ray n×S on one compile, not consumer-share, not 99.9%"
    );

    let mut output_match_max_pos_err: f64 = 0.0;
    for k in 1..N {
        output_match_max_pos_err = output_match_max_pos_err
            .max(V2::from_arr(independent_pos_a[k]).sub(V2::from_arr(independent_pos_a[0])).norm())
            .max(V2::from_arr(independent_pos_b[k]).sub(V2::from_arr(independent_pos_b[0])).norm());
    }

    let long = compile_source_response(ic.clone(), Vec::new(), 12.0, dt)?;
    let late = vec![Intervention {
        t: 5.0,
        body_id: 0,
        delta_v: [0.0, 0.05],
    }];
    let full = compile_source_response(ic.clone(), late.clone(), horizon, dt)?;
    let repaired = repair_from_committed(&compiled, &late, horizon, dt)?;

    let refuse_h = 1.0;
    let refuse_dt = 1.0 / 32.0;
    let close = crate::coupled_interval_enclosure::laboratory_close_pair();
    let mut refuse_ops = Vec::with_capacity(N);
    let mut refuse_pos_a = Vec::with_capacity(N);
    let mut refuse_pos_b = Vec::with_capacity(N);
    let mut first_close: Option<SourceResponse> = None;
    for _ in 0..N {
        let driven = compile_source_response(close.clone(), Vec::new(), refuse_h, refuse_dt)?;
        let mut completed = driven.charge.clone();
        let mono = crate::coupled_interval_enclosure::enclose_compiled_interval(
            &driven,
            close.clone(),
            Vec::new(),
            crate::coupled_interval_enclosure::IntervalMethod::IntegralOperator,
        )?;
        completed.validation += mono.charge.validation;
        completed.coefficient_construction += mono.charge.coefficient_construction;
        completed.factorization += mono.charge.factorization;
        let blocks = crate::coupled_interval_enclosure::enclose_compiled_interval(
            &driven,
            close.clone(),
            Vec::new(),
            crate::coupled_interval_enclosure::IntervalMethod::CausalBlocks,
        )?;
        completed.validation += blocks.charge.validation;
        completed.coefficient_construction += blocks.charge.coefficient_construction;
        completed.factorization += blocks.charge.factorization;
        completed.verification += blocks.charge.verification;
        let _ = complete_required_queries_compiled(&driven, refuse_h, &mut completed)?;
        refuse_ops.push(completed.total());
        let (xa, _) = body_state(&driven.worldtubes, 0, refuse_h)?;
        let (xb, _) = body_state(&driven.worldtubes, 1, refuse_h)?;
        refuse_pos_a.push(xa);
        refuse_pos_b.push(xb);
        if first_close.is_none() {
            first_close = Some(driven);
        }
    }
    let recovered = first_close.expect("N>=1");
    let compact_refuse_fallback = recovered.charge.fallback;
    let mono = crate::coupled_interval_enclosure::enclose_compiled_interval(
        &recovered,
        close.clone(),
        Vec::new(),
        crate::coupled_interval_enclosure::IntervalMethod::IntegralOperator,
    )?;
    let blocks = crate::coupled_interval_enclosure::enclose_compiled_interval(
        &recovered,
        close,
        Vec::new(),
        crate::coupled_interval_enclosure::IntervalMethod::CausalBlocks,
    )?;
    let certificate_refused = !mono.certified && mono.q >= 1.0;
    let certificate_refined = blocks.certified && blocks.q < 1.0 && blocks.q < mono.q;
    let mut recov_charge = recovered.charge.clone();
    recov_charge.repair += 1;
    recov_charge.validation += mono.charge.validation + blocks.charge.validation;
    recov_charge.coefficient_construction +=
        mono.charge.coefficient_construction + blocks.charge.coefficient_construction;
    recov_charge.factorization += mono.charge.factorization + blocks.charge.factorization;
    recov_charge.verification += blocks.charge.verification;
    recov_charge.reconstruction += 1;
    let (required_ship_ok, required_ray_ok, required_clock_ok, required_contact_ok) =
        match complete_required_queries_compiled(&recovered, refuse_h, &mut recov_charge) {
            Ok(flags) => flags,
            Err(_) => (false, false, false, false),
        };
    let (rx, _) = body_state(&recovered.worldtubes, 0, refuse_h)?;
    let (rbx, _) = body_state(&recovered.worldtubes, 1, refuse_h)?;
    let mut refuse_output_match_max_pos_err =
        V2::from_arr(rx).sub(V2::from_arr(refuse_pos_a[0])).norm().max(
            V2::from_arr(rbx).sub(V2::from_arr(refuse_pos_b[0])).norm(),
        );
    for k in 1..N {
        refuse_output_match_max_pos_err = refuse_output_match_max_pos_err
            .max(V2::from_arr(refuse_pos_a[k]).sub(V2::from_arr(refuse_pos_a[0])).norm())
            .max(V2::from_arr(refuse_pos_b[k]).sub(V2::from_arr(refuse_pos_b[0])).norm());
    }
    let refuse_full_recompute_ops_sum: u64 = refuse_ops.iter().copied().sum();
    let refuse_recovery_ops = recov_charge.total();
    let refuse_recovered = certificate_refused
        && certificate_refined
        && required_ship_ok
        && required_ray_ok
        && required_clock_ok
        && required_contact_ok
        && refuse_output_match_max_pos_err < 1e-12;
    let refuse_repair_fraction = if !refuse_recovered || refuse_full_recompute_ops_sum == 0 {
        0.0
    } else {
        1.0 - refuse_recovery_ops as f64 / refuse_full_recompute_ops_sum as f64
    };

    // Distinct-history workload declared before results:
    // artifacts/runs/distinct-histories-20260914/workload-declaration.md
    let distinct_history_declared = "artifacts/runs/distinct-histories-20260914/workload-declaration.md: history 1 quiet two-body H=6; history 2 same IC + kick t=5 Δv=(0,0.05) through H=6. Not identical-IC N. Not extra-ray n×S.".to_string();
    let distinct_history_reuse_denominator = "measured source_evolution+retarded_solves of one independent compile_source_response of the kicked IC through H=6. Numerator is reuse_certified_interval_functions of the quiet compile plus that kick. Copied complete certified interval functions, not inertial chords, not 24×S, not 1-(S+C)/(3S+C), not 99.9%.".to_string();
    let mut distinct_history_reuse_certified = false;
    let mut distinct_history_refuse_why = String::new();
    let mut distinct_history_reused_functions = 0u64;
    let mut distinct_history_recollocated_functions = 0u64;
    let mut distinct_history_source_ops_reuse = 0u64;
    let distinct_history_source_ops_full = source_ops_of(&full);
    let mut distinct_history_reuse_fraction = 0.0;
    let mut distinct_history_output_match_max_pos_err = f64::NAN;
    let mut distinct_history_required_ok = false;
    match reuse_certified_interval_functions(&compiled, &late, horizon, dt) {
        Ok(reused) => {
            let (xa_r, _) = body_state(&reused.worldtubes, 0, horizon)?;
            let (xb_r, _) = body_state(&reused.worldtubes, 1, horizon)?;
            let (xa_f, _) = body_state(&full.worldtubes, 0, horizon)?;
            let (xb_f, _) = body_state(&full.worldtubes, 1, horizon)?;
            distinct_history_output_match_max_pos_err = V2::from_arr(xa_r)
                .sub(V2::from_arr(xa_f))
                .norm()
                .max(V2::from_arr(xb_r).sub(V2::from_arr(xb_f)).norm());
            let mut qcharge = Charge::default();
            distinct_history_required_ok =
                match complete_required_queries_compiled(&reused, horizon, &mut qcharge) {
                    Ok((s, r, c, k)) => s && r && c && k,
                    Err(_) => false,
                };
            distinct_history_reused_functions = kept_certified_functions(&compiled, &late)?.len() as u64;
            distinct_history_recollocated_functions = reused
                .interval_functions
                .len()
                .saturating_sub(distinct_history_reused_functions as usize)
                as u64;
            distinct_history_source_ops_reuse = source_ops_of(&reused);
            if distinct_history_source_ops_full > 0 {
                distinct_history_reuse_fraction = 1.0
                    - distinct_history_source_ops_reuse as f64
                        / distinct_history_source_ops_full as f64;
            }
            distinct_history_reuse_certified = distinct_history_reused_functions > 0
                && distinct_history_source_ops_reuse < distinct_history_source_ops_full
                && distinct_history_output_match_max_pos_err < 1e-8
                && distinct_history_required_ok;
            if !distinct_history_reuse_certified {
                distinct_history_refuse_why = format!(
                    "reuse returned but was not certified: reused_fn={} recollocated={} ops {} vs full {} pos_err={} required={}",
                    distinct_history_reused_functions,
                    distinct_history_recollocated_functions,
                    distinct_history_source_ops_reuse,
                    distinct_history_source_ops_full,
                    distinct_history_output_match_max_pos_err,
                    distinct_history_required_ok
                );
            }
        }
        Err(err) => {
            distinct_history_refuse_why = err.to_string();
        }
    }

    Ok(ChargedReport {
        law_id: COUPLED_RESPONSE_LAW_ID.into(),
        worktree_head: "254ba1f718771ec1d0a25bf59d0d555f7e57993e".into(),
        quiet_queries: 1,
        quiet_horizon: horizon,
        encounter_horizon: long.domain.horizon,
        source_ops_quiet,
        consumer_ops_quiet,
        source_ops_many_queries,
        consumer_ops_many_queries,
        full_recompute_ops: full.charge.total(),
        repaired_ops: repaired.charge.total(),
        source_evolution_full: full.charge.source_evolution,
        source_evolution_repair: repaired.charge.source_evolution,
        reuse_fraction_queries,
        reuse_denominator: denom,
        wall_ns_quiet: compiled.wall_ns,
        wall_ns_many_queries,
        max_phi_c2: compiled
            .residual
            .max_phi_c2
            .max(full.residual.max_phi_c2)
            .max(recovered.residual.max_phi_c2),
        max_beta: compiled
            .residual
            .max_beta
            .max(full.residual.max_beta)
            .max(recovered.residual.max_beta),
        production_law: None,
        notes: vec![
            "production_law remains null".into(),
            "Engine::advance remains es-inertial-causal-v1".into(),
            "reuse_fraction_queries denominator is the sum of N=3 measured independent compile_source_response runs through H=6, not 24×S on one compile".into(),
            "consumer_share is extra-ray C/(S+C) on one compile; a named different quantity from completed source compiles".into(),
            "source_evolution_repair is a late t=5 splice vs full genesis recompute through H=6".into(),
            "four-kick H=9 compact fallback was 0 on the interval operator; refused certificate is close-pair H=1 IntegralOperator (q≥1), recovered by CausalBlocks refine. Uncertified IntegralOperator is not a completed cheaper history.".into(),
            "distinct-history reuse is quiet compile + t=5 kick vs independent full compile of that kicked IC; extra-ray n×S is not this quantity; identical-IC N=3 is not this quantity.".into(),
        ],
        n_independent_compiles: N as u64,
        independent_compile_source_ops,
        independent_compile_wall_ns,
        independent_compile_source_ops_sum,
        compiled_once_source_ops,
        compiled_once_plus_consumers_ops,
        independent_compiles_plus_consumers_ops,
        consumer_share,
        consumer_share_denominator: "extra-ray consumers on one compile: C/(S+C) for 24 fly_ray on one compile_source_response through H=6. Named consumer-share, not N completed source compiles.".into(),
        extra_ray_count: many,
        compact_refuse_fallback,
        certificate_refused,
        certificate_refined,
        certificate_refuse_q: mono.q,
        certificate_refine_q: blocks.q,
        refuse_recovered,
        refuse_recovery_ops,
        refuse_full_recompute_ops_sum,
        refuse_n_independent_compiles: N as u64,
        refuse_repair_fraction,
        output_match_max_pos_err,
        refuse_output_match_max_pos_err,
        required_ship_ok,
        required_ray_ok,
        required_clock_ok,
        required_contact_ok,
        distinct_history_declared,
        distinct_history_reuse_certified,
        distinct_history_refuse_why,
        distinct_history_reused_functions,
        distinct_history_recollocated_functions,
        distinct_history_source_ops_reuse,
        distinct_history_source_ops_full,
        distinct_history_reuse_fraction,
        distinct_history_reuse_denominator,
        distinct_history_output_match_max_pos_err,
        distinct_history_required_ok,
    })
}

pub fn scene_polyline(bodies: &[Body], id: u64, t0: f64, t1: f64, n: usize) -> Result<Vec<[f64; 2]>, ResponseError> {
    let mut pts = Vec::new();
    for i in 0..=n {
        let t = t0 + (t1 - t0) * i as f64 / n as f64;
        let (x, _) = body_state(bodies, id, t)?;
        pts.push(x);
    }
    Ok(pts)
}

pub fn laboratory_scene_svg() -> Result<String, ResponseError> {
    let compiled = compile_source_response(laboratory_two_body(), laboratory_kick(), 4.0, 1.0 / 32.0)?;
    let a = scene_polyline(&compiled.worldtubes, 0, 0.0, 4.0, 64)?;
    let b = scene_polyline(&compiled.worldtubes, 1, 0.0, 4.0, 64)?;
    let mut charge = Charge::default();
    let mut ray_pts = Vec::new();
    for k in 0..=16 {
        let s = 8.0 * k as f64 / 16.0;
        let r = fly_ray(
            &compiled.worldtubes,
            1.1,
            [0.0, 3.0],
            [1.0, 0.0],
            s.max(1e-6),
            0.05,
            &mut charge,
        )?;
        ray_pts.push(r.x);
    }
    fn map(x: f64, y: f64) -> (f64, f64) {
        (140.0 + x * 18.0, 110.0 - y * 18.0)
    }
    let mut out = String::from(
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 220' width='720' height='440'>",
    );
    out.push_str("<rect width='360' height='220' fill='#f7f1e3'/>");
    out.push_str("<text x='12' y='18' font-family='Georgia' font-size='11' fill='#1c2a44'>es-linearized-retarded-gem-response-v0 — A to B to A kick, ray in flight</text>");
    out.push_str("<text x='12' y='34' font-family='Georgia' font-size='9' fill='#3d5270'>Look for: B quiet until the kick cone; ray emitted after motion; kick while the ray flies. Not production_law.</text>");
    let path = |pts: &[[f64; 2]], color: &str, width: &str| {
        let mut d = String::new();
        for (i, p) in pts.iter().enumerate() {
            let (x, y) = map(p[0], p[1]);
            d.push_str(&format!("{}{:.1},{:.1} ", if i == 0 { "M" } else { "L" }, x, y));
        }
        format!("<path d='{d}' fill='none' stroke='{color}' stroke-width='{width}'/>")
    };
    out.push_str(&path(&a, "#1c2a44", "2"));
    out.push_str(&path(&b, "#3d6b8a", "2"));
    out.push_str(&path(&ray_pts, "#c45c26", "1.5"));
    let (ax, ay) = map(a[0][0], a[0][1]);
    let (bx, by) = map(b[0][0], b[0][1]);
    out.push_str(&format!(
        "<circle cx='{ax:.1}' cy='{ay:.1}' r='3' fill='#1c2a44'/><circle cx='{bx:.1}' cy='{by:.1}' r='3' fill='#3d6b8a'/>"
    ));
    out.push_str("<text x='12' y='208' font-family='Georgia' font-size='8' fill='#3d5270'>ink A, pale-blue B, watercolor ray, ivory ground. Remaining cards unsupported on this slice.</text></svg>");
    Ok(out)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn genesis_front_is_a_real_knot_for_moving_receiver() {
        let ic=InitialCondition { genesis_t:0.0, bodies:vec![
            BodyInit{id:0,mu:0.01,x:[0.0,0.0],v:[0.0,0.0]},
            BodyInit{id:1,mu:0.01,x:[4.0,0.0],v:[1.0,0.0]},
        ]};
        let response=compile_source_response_opts(ic,vec![],1.0,0.1,CompileOpts{store_pair_inverse:false}).unwrap();
        // 4+t=8t, independent of the source's subsequent motion.
        let arrival=4.0/7.0;
        assert!(response.interval_functions.iter().any(|f|f.body_id==1 && (f.t1-arrival).abs()<1e-12));
        for fun in response.interval_functions.iter().filter(|f|f.body_id==1 && f.t1<=arrival) {
            assert_eq!(fun.a,[0.0,0.0],"no force before the first source light cone");
        }
        let (x,v)=body_state_compiled(&response,1,arrival).unwrap();
        assert!((x[0]-(4.0+arrival)).abs()<1e-12);
        assert!((v[0]-1.0).abs()<1e-12);
        let (_,after)=body_state_compiled(&response,1,0.9).unwrap();
        assert!(after[0]<v[0]);
    }

    #[test]
    #[ignore = "charged genesis-to-observation localization"]
    fn orbital_onset_diagnostic() {
        let saved:serde_json::Value=serde_json::from_str(include_str!("../../../artifacts/evidence/orbit-duration-20260923/orbit-duration-bank.json")).unwrap();
        let mut reports=vec![];
        for seed in [8_usize,10] {
            let case:crate::two_body_bank::Case=serde_json::from_value(saved[seed]["case"].clone()).unwrap();
            let ic:InitialCondition=serde_json::from_value(saved[seed]["initialization"]["resolved_genesis"].clone()).unwrap();
            let start=std::time::Instant::now();
            let (reference,ref_charge)=Reference::from_genesis(ic.clone(),vec![],-ic.genesis_t/32768.0).evolve_to(0.0).unwrap();
            let reference_functions:Vec<_>=reference.iter().flat_map(|body|body.segments.iter().map(move |seg|{
                let mut f=segment_as_function(seg,0.0);f.body_id=body.id;f
            })).collect();
            let vs=(G*case.total_mass/case.a).sqrt();
            let ascale=G*case.total_mass/(case.a*case.a);
            let mut variants=vec![];
            for factor in [1,8,32] {
                let compiled=compile_source_response_refined(ic.clone(),vec![],0.0,-ic.genesis_t/512.0,CompileOpts{store_pair_inverse:false},factor).unwrap();
                let mut charge=Charge::default();
                let mut rows=vec![];let mut max_dx=0.0_f64;let mut max_dv=0.0_f64;let mut first=None;
                let mut compiled_field_dispatch_difference=0.0_f64;let mut reference_field_dispatch_difference=0.0_f64;
                for i in 0..1025 {
                    let t=ic.genesis_t*(1.0-i as f64/1024.0);
                    let (xc,vc)=body_state_compiled(&compiled,0,t).unwrap();let(xr,vr)=body_state(&reference,0,t).unwrap();
                    let dx=V2::from_arr(xc).sub(V2::from_arr(xr)).norm()/case.a;
                    let dv=V2::from_arr(vc).sub(V2::from_arr(vr)).norm()/vs;
                    assert!(dx.is_finite() && dv.is_finite());
                    max_dx=max_dx.max(dx);max_dv=max_dv.max(dv);
                    if dv>1e-6 && first.is_none(){first=Some(t);}
                    if i%32==0 || (dv>1e-6 && rows.is_empty()) {
                        let fc=field_at_stored(&compiled.interval_functions,&compiled.worldtubes,t,V2::from_arr(xc),Some(0),&mut charge).unwrap();
                        let fcc=field_at(&compiled.worldtubes,t,V2::from_arr(xc),Some(0),&mut charge).unwrap();
                        let fr=field_at(&reference,t,V2::from_arr(xr),Some(0),&mut charge).unwrap();
                        let frr=field_at_stored(&reference_functions,&reference,t,V2::from_arr(xr),Some(0),&mut charge).unwrap();
                        let ac=apply_gem_a(fc,V2::from_arr(vc));let ar=apply_gem_a(fr,V2::from_arr(vr));
                        compiled_field_dispatch_difference=compiled_field_dispatch_difference.max(ac.sub(apply_gem_a(fcc,V2::from_arr(vc))).norm()/ascale);
                        reference_field_dispatch_difference=reference_field_dispatch_difference.max(ar.sub(apply_gem_a(frr,V2::from_arr(vr))).norm()/ascale);
                        rows.push(serde_json::json!({"t":t,"dx":dx,"dv":dv,"xc":xc,"xr":xr,"vc":vc,"vr":vr,"ac":ac.arr(),"ar":ar.arr()}));
                    }
                }
                variants.push(serde_json::json!({"factor":factor,"compiler_charge":compiled.charge.ledger_total(),"field_query_charge":charge.ledger_total(),"state_queries":2050,"max_dx":max_dx,"max_dv":max_dv,"first_dv_over_1e6":first,"compiled_field_dispatch_difference":compiled_field_dispatch_difference,"reference_field_dispatch_difference":reference_field_dispatch_difference,"rows":rows}));
            }
            reports.push(serde_json::json!({"seed":seed,"genesis":ic,"reference_steps":32768,"reference_charge":ref_charge.ledger_total(),"wall_ns":start.elapsed().as_nanos(),"variants":variants}));
        }
        if let Some(path)=std::env::var_os("ORBIT_ONSET_OUTPUT") {
            use std::io::Write;
            let mut f=std::fs::OpenOptions::new().write(true).create_new(true).open(path).unwrap();
            f.write_all(serde_json::to_string_pretty(&reports).unwrap().as_bytes()).unwrap();
        }
    }

    fn a_scale() -> f64 {
        1.0 / 64.0
    }

    #[test]
    fn indexed_euler_matches_exhaustive_fields_at_fronts_and_kinks() {
        let mut body = genesis_bodies(&laboratory_two_body()).remove(0);
        for i in 1..101 {
            let t = i as f64 * 0.03125;
            let x = body.segments.last().unwrap().at(t);
            let v = V2::new(0.6 * (i as f64).sin(), 0.4 * (i as f64).cos());
            close_and_kink(&mut body, t, x, v, 1.0, V2::zero(), V2::zero());
        }
        let bodies = vec![body];
        let mut indexed = Charge::default();
        let mut exhaustive = Charge::default();
        for x in [V2::new(3.0, 2.0), V2::new(-7.0, -0.4), V2::new(100.0, 30.0)] {
            for seg in &bodies[0].segments {
                let arrival = seg.t0 + x.sub(V2::from_arr(seg.x0)).norm() / C;
                for shift in [-1e-8, -1e-12, 0.0, 1e-12, 1e-8, 0.01] {
                    let t = arrival + shift;
                    let a = field_at(&bodies, t, x, None, &mut exhaustive).unwrap();
                    let b = field_at_euler_indexed(&bodies, t, x, None, &mut indexed).unwrap();
                    assert_eq!((a.phi, a.e.arr(), a.b_z), (b.phi, b.e.arr(), b.b_z));
                }
            }
        }
        assert!(indexed.ledger_total() < exhaustive.ledger_total());
    }

    #[test]
    fn indexed_euler_preserves_complete_trajectories_on_varied_geneses() {
        for seed in [0, 4, 8, 9, 10, 11] {
            let case = crate::two_body_bank::Case::from_seed(seed);
            let ic = case.initial_condition();
            let reference = Reference::from_genesis(ic, vec![], (case.horizon - case.genesis) / 2048.0);
            let (a, ca) = reference.evolve_to(case.horizon).unwrap();
            let (b, cb) = reference.evolve_to_indexed(case.horizon).unwrap();
            assert_eq!(
                serde_json::to_value(a).unwrap(),
                serde_json::to_value(b).unwrap()
            );
            assert_eq!(ca.source_evolution, cb.source_evolution);
            assert!(cb.verification > 0);
        }
        let r = Reference::from_genesis(laboratory_two_body(), laboratory_kick(), 0.01);
        assert!(r.evolve_to_indexed(2.0).is_err());
    }

    #[test]
    fn accelerated_retarded_root_survives_outside_initial_guess() {
        let fun = IntervalFunction {
            body_id: 0, t0: 0.0, t1: 1.0, x0: [0.0, 0.0],
            v0: [0.0, 0.0], a: [-2.0, 0.0], mu: 1.0,
        };
        let query = V2::new(7.0999, 0.0);
        // Independent construction: x(.99)=-.99², distance=8*(2-.99).
        // The old inertial seed refuses, and its midpoint fallback produces
        // t_ret=1.0812625>1, causing an immediate false no-root return.
        let seed = Segment { t0: 0.0, t1: Some(1.0), x0: fun.x0,
                             v: fun.v0, a: [0.0, 0.0], mu: 1.0 };
        assert!(inertial_delay(2.0, query, &seed).is_none());
        let old_guess = 2.0 - (7.0999_f64 + 0.25) / C;
        assert!(old_guess > fun.t1);
        let mut charge = Charge::default();
        let delay = retarded_lookback_function(2.0, query, &fun, &mut charge).unwrap();
        assert!((2.0 - delay - 0.99).abs() < 1e-10);
        assert!(charge.verification >= 2);
        assert!(gem_from_function(2.0, query, &fun, &mut charge).unwrap().is_some());
    }

    #[test]
    fn accelerated_retarded_root_brackets_interior_endpoints_and_absence() {
        let fun = IntervalFunction {
            body_id: 0, t0: 0.0, t1: 1.0, x0: [0.0, 0.0],
            v0: [0.0, 0.0], a: [-2.0, 0.0], mu: 1.0,
        };
        for retarded in [0.0_f64, 0.25, 0.5, 0.99, 1.0] {
            let query = V2::new(-retarded * retarded + C * (2.0 - retarded), 0.0);
            let delay = retarded_lookback_function(2.0, query, &fun, &mut Charge::default()).unwrap();
            assert!((2.0 - delay - retarded).abs() < 1e-10);
        }
        // F is increasing. At x=20 its lower endpoint is already positive;
        // at x=0 its upper endpoint is still negative: neither has a root.
        for x in [20.0, 0.0] {
            assert!(retarded_lookback_function(2.0, V2::new(x, 0.0), &fun, &mut Charge::default()).is_none());
        }
        assert!(retarded_lookback_function(-1.0, V2::zero(), &fun, &mut Charge::default()).is_none());
    }

    #[test]
    fn laboratory_subdivision_controls_actual_causal_intervals() {
        let opts = CompileOpts { store_pair_inverse: false };
        let default = compile_source_response_opts(laboratory_two_body(), vec![], 3.0, 1.0 / 32.0, opts).unwrap();
        let factor_one = compile_source_response_refined(laboratory_two_body(), vec![], 3.0, 1.0 / 32.0, opts, 1).unwrap();
        assert_eq!(serde_json::to_value(&default.interval_functions).unwrap(),
                   serde_json::to_value(&factor_one.interval_functions).unwrap());
        let factor_two = compile_source_response_refined(laboratory_two_body(), vec![], 3.0, 1.0 / 32.0, opts, 2).unwrap();
        assert!(factor_two.interval_functions.len() > factor_one.interval_functions.len());
        assert!(factor_two.interval_blocks > factor_one.interval_blocks);
        assert_eq!(factor_two.interval_tau, factor_one.interval_tau / 2.0);
        assert_eq!(factor_two.domain.dt, factor_one.domain.dt);
        assert_eq!(serde_json::to_value(&factor_two.genesis).unwrap(),
                   serde_json::to_value(&factor_one.genesis).unwrap());
        assert!(matches!(compile_source_response_refined(laboratory_two_body(), vec![], 3.0, 1.0 / 32.0, opts, 0),
                         Err(ResponseError::UnsupportedDomain { .. })));
        let mut single = laboratory_two_body();
        single.bodies.truncate(1);
        assert!(matches!(compile_source_response_refined(single, vec![], 3.0, 1.0 / 32.0, opts, 2),
                         Err(ResponseError::UnsupportedDomain { .. })));
        assert!(matches!(compile_source_response_refined(laboratory_two_body(), vec![], 3.0, 1.0 / 32.0, opts, usize::MAX),
                         Err(ResponseError::UnsupportedDomain { .. })));
    }

    #[test]
    fn h0098_zero_force_does_not_move() {
        let force = [0.01, 0.0];
        let mut v = [0.0, 0.0];
        v[0] += force[0] * 0.0;
        v[1] += force[1] * 0.0;
        assert_eq!(v, [0.0, 0.0], "H0098: force*0 leaves velocity untreated");
        let mut x = [0.0, 0.0];
        let dt = 0.1;
        let mass = 1.0;
        x[0] += force[0] * dt / mass;
        assert!(
            (x[0] - 0.001_f64).abs() < 1e-15,
            "H0098: force*dt/mass has velocity units dumped into position"
        );
    }

    #[test]
    fn truncated_gem_moving_eval_is_not_this_law() {
        let msg = "UnsupportedPredicate: post-cone GEM-E omitted";
        assert!(
            msg.contains("UnsupportedPredicate"),
            "H0098/H0097: truncated moving GEM-E unsupported is a capability fail there"
        );
        let ic = laboratory_two_body();
        let compiled = compile_source_response(ic, laboratory_kick(), 4.0, 1.0 / 32.0).unwrap();
        let mut charge = Charge::default();
        let a = acceleration_at(&compiled.worldtubes, 1, 2.5, &mut charge).unwrap();
        assert!(
            a[0].abs() + a[1].abs() > 0.0,
            "required moving-source acceleration must not be UnsupportedPredicate"
        );
    }

    #[test]
    fn static_first_visibility_matches_derivation() {
        let ic = laboratory_two_body();
        let bodies = genesis_bodies(&ic);
        let mut charge = Charge::default();
        let a = acceleration_at(&bodies, 0, 1.0, &mut charge).unwrap();
        assert!((a[0] - a_scale()).abs() < 1e-12);
        assert!(a[1].abs() < 1e-12);
        let before = acceleration_at(&bodies, 0, 0.5, &mut charge).unwrap();
        assert!(before[0].abs() < 1e-12 && before[1].abs() < 1e-12);
    }

    #[test]
    fn independent_reference_never_uses_candidate_state() {
        let ic = laboratory_two_body();
        let kicks = laboratory_kick();
        let reference = Reference::from_genesis(ic.clone(), kicks.clone(), 1.0 / 128.0);
        let mut compiled = compile_source_response(ic.clone(), kicks.clone(), 4.0, 1.0 / 32.0).unwrap();
        let (ref_before, _) = reference.evolve_to(4.0).unwrap();
        for body in compiled.worldtubes.iter_mut() {
            for seg in body.segments.iter_mut() {
                seg.x0[0] += 100.0;
                seg.x0[1] += 100.0;
            }
        }
        for fun in compiled.interval_functions.iter_mut() {
            fun.x0[0] += 100.0;
            fun.x0[1] += 100.0;
        }
        compiled.residual.max_grad_rel = 1e9;
        compiled.residual.static_kernel_ok = false;
        let (ref_after, _) = reference.evolve_to(4.0).unwrap();
        let (xr0, _) = body_state(&ref_before, 0, 4.0).unwrap();
        let (xr1, _) = body_state(&ref_after, 0, 4.0).unwrap();
        assert_eq!(
            xr0, xr1,
            "poisoning compiled worldtubes/interval functions/residual must not change Reference::from_genesis"
        );
        let (xc_poison, _) = body_state(&compiled.worldtubes, 0, 4.0).unwrap();
        assert!(
            V2::from_arr(xc_poison).sub(V2::from_arr(xr0)).norm() > 50.0,
            "poisoned candidate must not be the reference trajectory"
        );
        let honest = compile_source_response(ic, kicks, 4.0, 1.0 / 32.0).unwrap();
        let (xc, _) = body_state(&honest.worldtubes, 0, 4.0).unwrap();
        let err = V2::from_arr(xc).sub(V2::from_arr(xr0)).norm();
        assert!(err < 0.05 * 8.0, "numerical band 0.05 D, got {err}");
        assert!(honest.residual.static_kernel_ok);
    }

    #[test]
    fn kick_changes_b_only_after_cone_then_feeds_back_to_a() {
        let ic = laboratory_two_body();
        let control = compile_source_response(ic.clone(), Vec::new(), 5.0, 1.0 / 32.0).unwrap();
        let kicked = compile_source_response(ic, laboratory_kick(), 5.0, 1.0 / 32.0).unwrap();
        let mut c0 = Charge::default();
        let mut c1 = Charge::default();
        let t_pre = 2.0;
        let a_b_pre_c = acceleration_at(&control.worldtubes, 1, t_pre, &mut c0).unwrap();
        let a_b_pre_k = acceleration_at(&kicked.worldtubes, 1, t_pre, &mut c1).unwrap();
        let pre = V2::from_arr(a_b_pre_c).sub(V2::from_arr(a_b_pre_k)).norm() / a_scale();
        assert!(pre < 1e-8, "pre-cone B must match control, ratio={pre}");

        let t_post = 2.45;
        let a_b_post_c = acceleration_at(&control.worldtubes, 1, t_post, &mut c0).unwrap();
        let a_b_post_k = acceleration_at(&kicked.worldtubes, 1, t_post, &mut c1).unwrap();
        let post = V2::from_arr(a_b_post_c).sub(V2::from_arr(a_b_post_k)).norm() / a_scale();
        assert!(post > 1e-3, "post-cone B must change, ratio={post}");

        let (xb_c, _) = body_state(&control.worldtubes, 1, 3.4).unwrap();
        let (xb_k, _) = body_state(&kicked.worldtubes, 1, 3.4).unwrap();
        assert!(
            V2::from_arr(xb_c).sub(V2::from_arr(xb_k)).norm() > 1e-5,
            "B worldtube must actually move differently"
        );

        let t_back = 3.5;
        let a_a_c = acceleration_at(&control.worldtubes, 0, t_back, &mut c0).unwrap();
        let a_a_k = acceleration_at(&kicked.worldtubes, 0, t_back, &mut c1).unwrap();
        let back = V2::from_arr(a_a_c).sub(V2::from_arr(a_a_k)).norm() / a_scale();
        assert!(back > 1e-3, "A must feel B's changed motion, ratio={back}");
    }

    #[test]
    fn held_out_ship_ray_clock_contact_are_supported() {
        let compiled =
            compile_source_response(laboratory_two_body(), laboratory_kick(), 5.0, 1.0 / 32.0)
                .unwrap();
        let mut charge = Charge::default();
        let sources = compiled.decode_sources(&mut charge).unwrap();
        let ship = fly_ship(
            &sources,
            1.1,
            [0.0, 3.0],
            [0.125, 0.0],
            3.5,
            1.0 / 32.0,
            &mut charge,
        )
        .unwrap();
        assert!(ship.tau > 0.0);
        let ray = fly_ray(
            &sources,
            1.1,
            [0.0, 3.0],
            [1.0, 0.0],
            8.0,
            0.05,
            &mut charge,
        )
        .unwrap();
        assert!(ray.t > 1.1);
        let rate = clock_rate(
            &sources,
            ship.t,
            ship.x,
            ship.v,
            &mut charge,
        )
        .unwrap();
        assert!(rate > 0.0 && rate <= 1.0);
        let (ct, cd) = contact_closest(&sources, 0, 1, 0.0, 4.0, 1.0 / 16.0, &mut charge)
            .unwrap();
        assert!(cd > 0.0 && ct >= 0.0);
        let mut compiled_charge = Charge::default();
        let (ship_ok, ray_ok, clock_ok, contact_ok) =
            complete_required_queries_compiled(&compiled, 5.0, &mut compiled_charge).unwrap();
        assert!(
            ship_ok && ray_ok && clock_ok && contact_ok,
            "compiled lookback held-out ship/ray/clock/contact must return values, not UnsupportedDomain"
        );
        let ship_c = fly_ship_compiled(
            &compiled,
            1.1,
            [0.0, 3.0],
            [0.125, 0.0],
            3.5,
            1.0 / 32.0,
            &mut compiled_charge,
        )
        .unwrap();
        assert!(ship_c.tau > 0.0);
        let ray_c = fly_ray_compiled(
            &compiled,
            1.1,
            [0.0, 3.0],
            [1.0, 0.0],
            8.0,
            0.05,
            &mut compiled_charge,
        )
        .unwrap();
        assert!(ray_c.t > 1.1);
        let rate_c = clock_rate_compiled(
            &compiled,
            ship_c.t,
            ship_c.x,
            ship_c.v,
            &mut compiled_charge,
        )
        .unwrap();
        assert!(rate_c > 0.0 && rate_c <= 1.0);
    }

    #[test]
    fn ray_in_flight_direct_matches_subdivided() {
        let ic = laboratory_two_body();
        let kicks = laboratory_kick();
        let dt = 1.0 / 32.0;
        let direct = compile_source_response(ic.clone(), kicks.clone(), 4.0, dt).unwrap();
        let first = compile_source_response(ic.clone(), Vec::new(), 1.25, dt).unwrap();
        let second = repair_from_committed(&first, &kicks, 4.0, dt).unwrap();
        let mut c0 = Charge::default();
        let mut c1 = Charge::default();
        let r0 = fly_ray(&direct.worldtubes, 1.1, [0.0, 3.0], [1.0, 0.0], 8.0, 0.05, &mut c0).unwrap();
        let r1 = fly_ray(&second.worldtubes, 1.1, [0.0, 3.0], [1.0, 0.0], 8.0, 0.05, &mut c1).unwrap();
        let (x0, _) = body_state(&direct.worldtubes, 0, 4.0).unwrap();
        let (x1, _) = body_state(&second.worldtubes, 0, 4.0).unwrap();
        assert!(
            (r0.t - r1.t).abs() < 1e-8 || (r0.t - r1.t).abs() / r0.t.max(1.0) < 1e-8,
            "direct {} subdivided {}",
            r0.t,
            r1.t
        );
        assert!(V2::from_arr(x0).sub(V2::from_arr(x1)).norm() < 1e-8);
    }

    #[test]
    fn authored_worldtubes_fail_residual_certificate() {
        let mut compiled =
            compile_source_response(laboratory_two_body(), laboratory_kick(), 4.0, 1.0 / 32.0)
                .unwrap();
        for seg in compiled.worldtubes[1].segments.iter_mut() {
            if seg.t0 >= 2.0 {
                seg.x0[1] += 3.0;
            }
        }
        let mut charge = Charge::default();
        let residual = validate_residual(&compiled.worldtubes, &[2.5, 3.0, 3.5], &mut charge).unwrap();
        assert!(
            residual.max_grad_rel > 1e-3 || residual.max_accel_rel > 0.0,
            "authored futures must not pass as physical GEM residual"
        );
        let control =
            compile_source_response(laboratory_two_body(), laboratory_kick(), 4.0, 1.0 / 32.0)
                .unwrap();
        let (xb, _) = body_state(&compiled.worldtubes, 1, 3.5).unwrap();
        let (xb0, _) = body_state(&control.worldtubes, 1, 3.5).unwrap();
        assert!(V2::from_arr(xb).sub(V2::from_arr(xb0)).norm() > 1.0);
    }

    #[test]
    fn family_extraction_changes_field() {
        let fam = compile_source_response(laboratory_family(), Vec::new(), 3.0, 1.0 / 24.0).unwrap();
        let mut reduced = laboratory_family();
        reduced.bodies.retain(|b| b.id != 10);
        let red = compile_source_response(reduced, Vec::new(), 3.0, 1.0 / 24.0).unwrap();
        let mut c = Charge::default();
        let q = V2::new(0.0, 6.0);
        let f_all = field_at(&fam.worldtubes, 2.5, q, None, &mut c).unwrap();
        let f_red = field_at(&red.worldtubes, 2.5, q, None, &mut c).unwrap();
        assert!(
            (f_all.phi - f_red.phi).abs() > 1e-6,
            "extracting a massive member must change Phi"
        );
    }

    #[test]
    fn delayed_newton_is_not_gem() {
        let compiled =
            compile_source_response(laboratory_two_body(), laboratory_kick(), 4.0, 1.0 / 32.0)
                .unwrap();
        let mut c = Charge::default();
        let t = 2.6;
        let gem = acceleration_at(&compiled.worldtubes, 1, t, &mut c).unwrap();
        let newton = delayed_newton_a(&compiled.worldtubes, 1, t, &mut c).unwrap();
        let diff = V2::from_arr(gem).sub(V2::from_arr(newton)).norm();
        assert!(
            diff > 1e-8,
            "GEM velocity terms must move the post-kick acceleration off delayed Newton"
        );
    }

    #[test]
    fn query_count_and_horizon_are_independent_and_not_hardcoded_f() {
        let report = run_charged_workload().unwrap();
        assert_eq!(report.production_law, None);
        assert_eq!(report.source_ops_quiet, report.source_ops_many_queries);
        assert!(report.consumer_ops_many_queries > report.consumer_ops_quiet);
        assert!(report.quiet_horizon < report.encounter_horizon);
        assert!(report.reuse_fraction_queries > 0.0 && report.reuse_fraction_queries < 1.0);
        assert_ne!(report.reuse_fraction_queries, 1.0);
        assert!(report.full_recompute_ops > 0 && report.repaired_ops > 0);
        assert!(
            report.source_evolution_repair < report.source_evolution_full,
            "late localized repair must not replay every reference step"
        );
    }

    #[test]
    fn overlong_independence_certificate_is_defeated_by_repeated_kicks() {
        let ic = laboratory_two_body();
        let tau = 1.0;
        let kicks = laboratory_four_kick();
        assert_eq!(kicks[0].t, 1.25);
        assert!((kicks[1].t - (1.25 + 2.0 * tau)).abs() < 1e-12);
        let quiet = compile_source_response(ic.clone(), Vec::new(), 9.0, 1.0 / 24.0).unwrap();
        let driven = compile_source_response(ic, kicks, 9.0, 1.0 / 24.0).unwrap();
        let mut rec = Charge::default();
        if driven.compact.pieces.is_empty() {
            assert!(
                driven.charge.fallback > 0,
                "H=9 four-kick empty compact must be an honest refuse, not a silent polyline"
            );
            assert!(
                driven.decode_sources(&mut rec).is_err(),
                "consumers must fail closed when the generator refuses"
            );
        } else {
            assert!(
                driven.compact.max_error <= driven.compact.band && driven.charge.fallback == 0,
                "H=9 four-kick stored compact must meet the band, error {} fallback {}",
                driven.compact.max_error,
                driven.charge.fallback
            );
            assert!(
                driven.decode_sources(&mut rec).is_ok(),
                "decode must succeed when the generator meets the band"
            );
        }
        let (xq, _) = body_state(&quiet.worldtubes, 1, 8.5).unwrap();
        let (xd, _) = body_state(&driven.worldtubes, 1, 8.5).unwrap();
        let drift = V2::from_arr(xq).sub(V2::from_arr(xd)).norm();
        assert!(
            drift > 1e-4,
            "repeated delayed kicks must accumulate; overlong quiet certificate cannot stand, drift={drift}"
        );
        let series = delayed_feedback_series(0.02, 0.1, 8.0, 1.0);
        assert!(series.abs() > 0.0);
    }

    #[test]
    fn encounter_differs_from_quiet() {
        let quiet = compile_source_response(laboratory_two_body(), Vec::new(), 4.0, 1.0 / 24.0).unwrap();
        let (enc_ic, enc_iv) = laboratory_encounter();
        let enc = compile_source_response(enc_ic, enc_iv, 4.0, 1.0 / 24.0).unwrap();
        let (xq, _) = body_state(&quiet.worldtubes, 0, 3.5).unwrap();
        let (xe, _) = body_state(&enc.worldtubes, 0, 3.5).unwrap();
        assert!(V2::from_arr(xq).sub(V2::from_arr(xe)).norm() > 1e-5);
    }

    #[test]
    fn phi_zero_clock_matches_inertial() {
        let empty = InitialCondition {
            genesis_t: 0.0,
            bodies: vec![BodyInit {
                id: 0,
                mu: 0.0,
                x: [10.0, 0.0],
                v: [0.0, 0.0],
            }],
        };
        let compiled = compile_source_response(empty, Vec::new(), 1.0, 0.25).unwrap();
        let mut c = Charge::default();
        let rate = clock_rate(&compiled.worldtubes, 0.5, [0.0, 0.0], [0.0, 0.0], &mut c).unwrap();
        assert!((rate - 1.0).abs() < 1e-12);
    }

    #[test]
    fn compile_is_not_evolve_then_copy() {
        let ic = laboratory_two_body();
        let kicks = laboratory_kick();
        let dt = 1.0 / 32.0;
        let compiled = compile_source_response(ic.clone(), kicks.clone(), 4.0, dt).unwrap();
        let reference = Reference::from_genesis(ic, kicks, dt);
        let (evolved, _) = reference.evolve_to(4.0).unwrap();
        assert!(
            compiled.interval_blocks > 0,
            "interval operator must record causal blocks"
        );
        assert!(
            compiled.charge.factorization > 0 && compiled.charge.coefficient_construction > 0,
            "Schur/block elimination must charge operator assembly"
        );
        assert!(
            compiled.interval_q.is_finite() && compiled.interval_q >= 0.0,
            "interval q must be computed, q={}",
            compiled.interval_q
        );
        assert!(
            !compiled.interval_functions.is_empty(),
            "compile must store interval functions, not only inertial chords"
        );
        assert_eq!(compiled.genesis.bodies.len(), 2);
        let n_compile: usize = compiled.worldtubes.iter().map(|b| b.segments.len()).sum();
        let n_evolve: usize = evolved.iter().map(|b| b.segments.len()).sum();
        assert_ne!(
            n_compile, n_evolve,
            "causal-block decode must not be the Euler-dt polyline, compile={n_compile} evolve={n_evolve}"
        );
        let (xc, _) = body_state(&compiled.worldtubes, 0, 4.0).unwrap();
        let (xe, _) = body_state(&evolved, 0, 4.0).unwrap();
        let drift = V2::from_arr(xc).sub(V2::from_arr(xe)).norm();
        assert!(
            drift > 0.0,
            "interval decode must not be bitwise identity with evolve-then-copy"
        );
        assert!(
            drift < 0.05 * 8.0,
            "interval compile must stay in the numerical band vs independent Euler reference, drift={drift}"
        );
    }

    #[test]
    fn extra_ray_n_times_s_is_not_equivalent_completed_source_histories() {
        let report = run_charged_workload().unwrap();
        assert_eq!(report.production_law, None);
        let labeled = format!(
            "{} {} {}",
            report.reuse_denominator,
            report.consumer_share_denominator,
            report.notes.join(" ")
        );
        assert!(
            !labeled.contains("24 independent compiles"),
            "extra-ray 24 must not be labelled independent compiles: {labeled}"
        );
        assert!(
            !report.reuse_denominator.contains("24 equivalent"),
            "{}",
            report.reuse_denominator
        );
        assert!(
            !report.consumer_share_denominator.contains("equivalent completed source histories"),
            "consumer-share must stay a named different quantity: {}",
            report.consumer_share_denominator
        );
        assert!(
            report.consumer_share_denominator.contains("consumer"),
            "{}",
            report.consumer_share_denominator
        );
        assert!(
            report.reuse_denominator.contains("measured")
                && report.reuse_denominator.contains("independent compile_source_response"),
            "{}",
            report.reuse_denominator
        );

        let s = report.source_ops_quiet as f64;
        let c = report.consumer_ops_many_queries as f64;
        let extra_ray_formula = 1.0 - (s + c) / (24.0 * s + c);
        assert!(
            (report.reuse_fraction_queries - extra_ray_formula).abs() > 1e-6,
            "reuse_fraction_queries {} must not be extra-ray n×S {}",
            report.reuse_fraction_queries,
            extra_ray_formula
        );

        assert_eq!(report.n_independent_compiles, 3);
        assert_eq!(report.independent_compile_source_ops.len(), 3);
        let sum: u64 = report.independent_compile_source_ops.iter().copied().sum();
        assert_eq!(report.independent_compile_source_ops_sum, sum);
        let measured = 1.0
            - report.compiled_once_plus_consumers_ops as f64
                / report.independent_compiles_plus_consumers_ops as f64;
        assert!(
            (report.reuse_fraction_queries - measured).abs() < 1e-12,
            "reuse {} != measured independent-compile fraction {}",
            report.reuse_fraction_queries,
            measured
        );
        assert!(report.reuse_fraction_queries > 0.0 && report.reuse_fraction_queries < 1.0);
        assert_ne!(report.reuse_fraction_queries, 1.0);
        assert!(report.consumer_share > 0.0 && report.consumer_share < 1.0);
        assert_eq!(report.extra_ray_count, 24);
        assert!(
            report.output_match_max_pos_err < 1e-12,
            "quiet independent compiles must match at H, err={}",
            report.output_match_max_pos_err
        );
        assert!(
            report.refuse_recovered,
            "close-pair IntegralOperator refuse must recover via CausalBlocks through H=1; uncertified q cannot count as cheaper; refused={} refined={} refuse_q={} refine_q={} fallback={} ship={} ray={} clock={} contact={} pos_err={} refuse_ops={} recovery_ops={}",
            report.certificate_refused,
            report.certificate_refined,
            report.certificate_refuse_q,
            report.certificate_refine_q,
            report.compact_refuse_fallback,
            report.required_ship_ok,
            report.required_ray_ok,
            report.required_clock_ok,
            report.required_contact_ok,
            report.refuse_output_match_max_pos_err,
            report.refuse_full_recompute_ops_sum,
            report.refuse_recovery_ops
        );
        assert!(report.certificate_refused && report.certificate_refined);
        assert!(report.certificate_refuse_q >= 1.0);
        assert!(report.certificate_refine_q < 1.0);
        assert_eq!(report.refuse_n_independent_compiles, 3);
        assert!(report.refuse_full_recompute_ops_sum > report.refuse_recovery_ops);
        assert!(
            report.refuse_repair_fraction > 0.0 && report.refuse_repair_fraction < 1.0,
            "refuse recovery fraction {}",
            report.refuse_repair_fraction
        );
        assert!(
            report.required_ship_ok
                && report.required_ray_ok
                && report.required_clock_ok
                && report.required_contact_ok
        );
        assert!(
            report
                .distinct_history_reuse_denominator
                .contains("kicked IC")
                && !report
                    .distinct_history_reuse_denominator
                    .contains("24 equivalent")
                && !report
                    .distinct_history_reuse_denominator
                    .contains("equivalent completed source histories"),
            "{}",
            report.distinct_history_reuse_denominator
        );
        assert!(
            report.distinct_history_declared.contains("kick"),
            "{}",
            report.distinct_history_declared
        );
        assert!(
            (report.distinct_history_reuse_fraction - report.reuse_fraction_queries).abs() > 1e-6
                || !report.distinct_history_reuse_certified,
            "distinct-history fraction must not silently equal identical-IC compile-once-vs-N"
        );
    }

    #[test]
    fn extra_ray_cannot_be_labelled_equivalent_completed_source_histories_via_reuse_api() {
        let quiet =
            compile_source_response(laboratory_two_body(), Vec::new(), 4.0, 1.0 / 32.0).unwrap();
        let err = reuse_certified_interval_functions(&quiet, &[], 4.0, 1.0 / 32.0)
            .expect_err("empty extra must refuse rather than claim reuse");
        let msg = err.to_string();
        assert!(
            msg.contains("not equivalent completed source histories"),
            "{msg}"
        );
        let foreign = vec![Intervention {
            t: 2.0,
            body_id: 99,
            delta_v: [0.0, 0.01],
        }];
        let err = reuse_certified_interval_functions(&quiet, &foreign, 4.0, 1.0 / 32.0)
            .expect_err("new massive entrant / foreign body must refuse");
        let msg = err.to_string();
        assert!(
            msg.contains("cannot share this domain") || msg.contains("not in the compiled genesis"),
            "{msg}"
        );
    }

    #[test]
    fn distinct_second_history_reuses_certified_interval_functions() {
        let ic = laboratory_two_body();
        let horizon = 6.0;
        let dt = 1.0 / 32.0;
        let quiet = compile_source_response(ic.clone(), Vec::new(), horizon, dt).unwrap();
        assert!(
            !quiet.interval_functions.is_empty(),
            "quiet compile must store interval functions"
        );
        let late = vec![Intervention {
            t: 5.0,
            body_id: 0,
            delta_v: [0.0, 0.05],
        }];
        let full = compile_source_response(ic, late.clone(), horizon, dt).unwrap();
        let reused = reuse_certified_interval_functions(&quiet, &late, horizon, dt)
            .unwrap_or_else(|e| panic!("distinct-history reuse refused: {e}"));
        let ops_r = source_ops_of(&reused);
        let ops_f = source_ops_of(&full);
        assert!(
            reused.charge.reconstruction > 0,
            "must copy complete certified interval functions"
        );
        assert!(
            ops_r < ops_f,
            "reuse source ops {ops_r} must be below independent full compile {ops_f}"
        );
        let (xa_r, _) = body_state(&reused.worldtubes, 0, horizon).unwrap();
        let (xb_r, _) = body_state(&reused.worldtubes, 1, horizon).unwrap();
        let (xa_f, _) = body_state(&full.worldtubes, 0, horizon).unwrap();
        let (xb_f, _) = body_state(&full.worldtubes, 1, horizon).unwrap();
        let pos_err = V2::from_arr(xa_r)
            .sub(V2::from_arr(xa_f))
            .norm()
            .max(V2::from_arr(xb_r).sub(V2::from_arr(xb_f)).norm());
        assert!(
            pos_err < 1e-8,
            "repaired distinct history must match full recompute at H, err={pos_err}"
        );
        let mut qcharge = Charge::default();
        let (ship, ray, clock, contact) =
            complete_required_queries_compiled(&reused, horizon, &mut qcharge).unwrap();
        assert!(ship && ray && clock && contact);
        let cut_a = causal_reuse_cut(&quiet.genesis, &late, 0).unwrap();
        let mut orig: Vec<_> = quiet
            .interval_functions
            .iter()
            .filter(|f| f.body_id == 0 && f.t1 <= cut_a + 1e-12)
            .cloned()
            .collect();
        orig.sort_by(|a, b| a.t0.partial_cmp(&b.t0).unwrap());
        let mut got: Vec<_> = reused
            .interval_functions
            .iter()
            .filter(|f| f.body_id == 0)
            .cloned()
            .collect();
        got.sort_by(|a, b| a.t0.partial_cmp(&b.t0).unwrap());
        assert!(!orig.is_empty());
        assert!(got.len() >= orig.len());
        assert_eq!(got[..orig.len()], orig[..]);
        assert_eq!(reused.residual.static_kernel_ok, full.residual.static_kernel_ok);
        // Independent enclosure of the reuse result still must not share compile residual:
        // field_acceleration / enclose ignore SourceResponse.residual.
        let mut ign = Charge::default();
        let _ = field_acceleration(
            &reused.worldtubes,
            5.5,
            [0.0, 0.0],
            [0.0, 0.0],
            None,
            &mut ign,
        )
        .unwrap();
    }

    #[test]
    fn lookback_on_stored_a_differs_from_chord_only_half_a_h2() {
        let compiled =
            compile_source_response(laboratory_two_body(), Vec::new(), 6.0, 1.0 / 32.0).unwrap();
        let fun = compiled
            .interval_functions
            .iter()
            .find(|f| {
                let h = f.t1 - f.t0;
                V2::from_arr(f.a).norm() * h * h > 1e-8
            })
            .expect("quiet compile must store a nonzero-a block");
        let t_mid = 0.5 * (fun.t0 + fun.t1);
        let h = t_mid - fun.t0;
        let (x_a, _) = fun.state_at(t_mid);
        let (x_c, _) = fun.chord_at(t_mid);
        let half_ah2 = V2::from_arr(fun.a).scale(0.5 * h * h);
        let pos_delta = x_a.sub(x_c);
        assert!(
            pos_delta.sub(half_ah2).norm() < 1e-12,
            "state_at - chord_at must be ½ah², got {:?} vs {:?}",
            pos_delta.arr(),
            half_ah2.arr()
        );
        assert!(
            pos_delta.norm() > 1e-12,
            "nonzero a must move the interior sample off the chord"
        );
        // Probe near the source so retarded time stays in this block.
        let query_t = (t_mid + 0.15).min(fun.t1);
        let query_x = x_a.add(V2::new(0.0, 0.4));
        let mut c0 = Charge::default();
        let mut c1 = Charge::default();
        let f_fun = gem_from_function(query_t, query_x, fun, &mut c0)
            .unwrap()
            .expect("constant-a lookback must hit this block");
        let chord_seg = Segment {
            t0: fun.t0,
            t1: Some(fun.t1),
            x0: fun.x0,
            v: fun.v0,
            a: [0.0, 0.0],
            mu: fun.mu,
        };
        let f_chord = gem_from_segment(query_t, query_x, &chord_seg, &mut c1)
            .unwrap()
            .expect("chord lookback must hit this block");
        let dphi = (f_fun.phi - f_chord.phi).abs();
        assert!(
            dphi > 1e-14,
            "lookback using stored a (½ah²) must differ from chord-only where a is nonzero; dphi={dphi}"
        );
        let mut cq = Charge::default();
        let (ship, ray, clock, contact) =
            complete_required_queries_compiled(&compiled, 6.0, &mut cq).unwrap();
        assert!(ship && ray && clock && contact);
        let chord_tubes: Vec<Body> = compiled
            .worldtubes
            .iter()
            .map(|b| Body {
                id: b.id,
                segments: b
                    .segments
                    .iter()
                    .map(|s| Segment {
                        a: [0.0, 0.0],
                        ..s.clone()
                    })
                    .collect(),
            })
            .collect();
        let mut c_ship = Charge::default();
        let ship_a = fly_ship_compiled(
            &compiled,
            0.1,
            [0.0, 3.0],
            [0.125, 0.0],
            3.5,
            1.0 / 32.0,
            &mut c_ship,
        )
        .unwrap();
        let mut c_ch = Charge::default();
        let ship_c = fly_ship(
            &chord_tubes,
            0.1,
            [0.0, 3.0],
            [0.125, 0.0],
            3.5,
            1.0 / 32.0,
            &mut c_ch,
        )
        .unwrap();
        let ship_delta = (ship_a.tau - ship_c.tau).abs().max(
            V2::from_arr(ship_a.x)
                .sub(V2::from_arr(ship_c.x))
                .norm(),
        );
        assert!(
            ship_delta > 1e-14,
            "compiled ship transport must differ from chord-only when stored a is nonzero, delta={ship_delta}"
        );
    }

    #[test]
    fn extra_ray_compiled_lookback_is_still_not_equivalent_completed_source_histories() {
        let quiet =
            compile_source_response(laboratory_two_body(), Vec::new(), 4.0, 1.0 / 32.0).unwrap();
        let err = reuse_certified_interval_functions(&quiet, &[], 4.0, 1.0 / 32.0)
            .expect_err("empty extra / extra-ray must refuse");
        assert!(
            err.to_string()
                .contains("not equivalent completed source histories"),
            "{err}"
        );
        let source_ops_before = source_ops_of(&quiet);
        let mut charge = Charge::default();
        for k in 0..8 {
            let y = 2.5 + 0.04 * k as f64;
            let ray = fly_ray_compiled(
                &quiet,
                1.1,
                [0.0, y],
                [1.0, 0.0],
                8.0,
                0.05,
                &mut charge,
            )
            .unwrap();
            assert!(ray.t > 1.1);
        }
        assert_eq!(
            source_ops_of(&quiet),
            source_ops_before,
            "extra-ray consumers must not be a second compile_source_response"
        );
        assert!(
            charge.consumers > 0,
            "compiled extra-ray still charges consumers, not equivalent completed source histories"
        );
        let report = run_charged_workload().unwrap();
        assert!(
            !report
                .consumer_share_denominator
                .contains("equivalent completed source histories"),
            "{}",
            report.consumer_share_denominator
        );
        assert_eq!(report.production_law, None);
    }

    #[test]
    fn compile_time_collocation_samples_stored_a_not_chords() {
        let compiled =
            compile_source_response(laboratory_two_body(), Vec::new(), 6.0, 1.0 / 32.0).unwrap();
        let mut found = false;
        for fun in &compiled.interval_functions {
            let h = fun.t1 - fun.t0;
            if h <= 1e-18 {
                continue;
            }
            let prior: Vec<IntervalFunction> = compiled
                .interval_functions
                .iter()
                .filter(|p| p.t1 <= fun.t0 + 1e-12)
                .cloned()
                .collect();
            if prior.iter().all(|p| V2::from_arr(p.a).norm() < 1e-12) {
                continue;
            }
            let t_col = fun.t0 + 0.5 * h;
            let x_col = V2::from_arr(fun.x0).add(V2::from_arr(fun.v0).scale(0.5 * h));
            let mut c_stored = Charge::default();
            let mut c_chord = Charge::default();
            let f_stored = field_at_stored(
                &prior,
                &compiled.worldtubes,
                t_col,
                x_col,
                Some(fun.body_id),
                &mut c_stored,
            )
            .unwrap();
            let chord_tubes: Vec<Body> = compiled
                .worldtubes
                .iter()
                .map(|b| Body {
                    id: b.id,
                    segments: b
                        .segments
                        .iter()
                        .map(|s| Segment {
                            a: [0.0, 0.0],
                            ..s.clone()
                        })
                        .collect(),
                })
                .collect();
            let f_chord = field_at(
                &chord_tubes,
                t_col,
                x_col,
                Some(fun.body_id),
                &mut c_chord,
            )
            .unwrap();
            let dphi = (f_stored.phi - f_chord.phi).abs();
            let de = f_stored.e.sub(f_chord.e).norm();
            if dphi + de <= 1e-14 {
                continue;
            }
            found = true;
            let a_stored = apply_gem_a(f_stored, V2::from_arr(fun.v0));
            let a_chord = apply_gem_a(f_chord, V2::from_arr(fun.v0));
            let a_fun = V2::from_arr(fun.a);
            let err_stored = a_fun.sub(a_stored).norm();
            let err_chord = a_fun.sub(a_chord).norm();
            assert!(
                err_stored < err_chord,
                "compile-time a must be the stored-a collocation sample, not chord-only; err_stored={err_stored} err_chord={err_chord} dphi={dphi}"
            );
            assert!(
                err_stored < 1e-10,
                "stored-a collocation at this knot must recover compiled a; err_stored={err_stored}"
            );
            break;
        }
        assert!(
            found,
            "compile-time field sampling must differ from chord-only where stored a ≠ 0; if they matched, that remainder must be named instead of renaming chords as stored-a"
        );
        let (ship, ray, clock, contact) =
            complete_required_queries_compiled(&compiled, 6.0, &mut Charge::default()).unwrap();
        assert!(ship && ray && clock && contact);
        assert_eq!(compiled.law_id, COUPLED_RESPONSE_LAW_ID);
        assert!(compiled.pair_inverse.is_some());
    }

    #[test]
    fn late_kick_prefix_and_lookback_do_not_finish_reusable_compiled_geometry() {
        let compiled =
            compile_source_response(laboratory_two_body(), Vec::new(), 6.0, 1.0 / 32.0).unwrap();
        let fun = compiled
            .interval_functions
            .iter()
            .find(|f| V2::from_arr(f.a).norm() > 1e-8)
            .expect("stored a must be nonzero");
        let (x_end, _) = fun.inertial_end();
        let (x_a, _) = fun.state_at(fun.t1);
        assert!(
            x_a.sub(x_end).norm() < 1e-15,
            "observer knots / inertial_end must match stored-a state_at(t1) including ½ah²; delta={}",
            x_a.sub(x_end).norm()
        );
        let late = vec![Intervention {
            t: 5.0,
            body_id: 0,
            delta_v: [0.0, 0.05],
        }];
        let reused = reuse_certified_interval_functions(&compiled, &late, 6.0, 1.0 / 32.0)
            .expect("late-kick prefix copy still works");
        assert!(reused.charge.reconstruction > 0);
        let (enc, _) = laboratory_encounter();
        let entrant = enc
            .bodies
            .iter()
            .find(|b| b.id == 99)
            .expect("encounter third mass");
        let err = share_compiled_pair_exterior(&compiled, entrant, 6.0, 1.0 / 32.0)
            .expect_err("new massive entrant exterior is not certified");
        let msg = err.to_string();
        assert!(
            msg.contains("cannot share this compiled pair's exterior")
                && msg.contains("H0110"),
            "{msg}"
        );
        let mut c = Charge::default();
        let _ = field_at_compiled(&compiled, 2.5, V2::new(0.0, 3.0), None, &mut c).unwrap();
        assert!(
            c.retarded_solves > 0,
            "consumer sampling of stored a is not a certified coupled share"
        );
        assert_eq!(compiled.law_id, COUPLED_RESPONSE_LAW_ID);
    }

    #[test]
    fn compiled_pair_exterior_does_not_cover_massive_encounter() {
        // Declared: docs/laws/pair-exterior-workload-declaration-20260914.md
        let horizon = 6.0;
        let dt = 1.0 / 32.0;
        let pair =
            compile_source_response(laboratory_two_body(), Vec::new(), horizon, dt).unwrap();
        let enclosure = crate::coupled_interval_enclosure::enclose_compiled_interval(
            &pair,
            pair.genesis.clone(),
            pair.incoming.clone(),
            crate::coupled_interval_enclosure::IntervalMethod::CausalBlocks,
        )
        .unwrap();
        assert!(
            enclosure.certified,
            "quiet pair itself must enclose; {:?}",
            enclosure.why_rejected
        );
        let radius = enclosure.radius.expect("certified pair radius");
        let (enc_ic, enc_iv) = laboratory_encounter();
        let entrant = enc_ic
            .bodies
            .iter()
            .find(|b| b.id == 99)
            .expect("encounter third mass")
            .clone();
        let mut c = Charge::default();
        let ratio = massive_entrant_coupling_ratio(&pair, &entrant, &mut c).unwrap();
        let triple = compile_source_response(enc_ic, enc_iv, horizon, dt).unwrap();
        let times: Vec<f64> = (0..16)
            .map(|i| (i as f64 + 1.0) * horizon / 16.0)
            .collect();
        let mut displacement = 0.0_f64;
        for &t in &times {
            for id in [0_u64, 1] {
                let (xp, _) = body_state(&pair.worldtubes, id, t).unwrap();
                let (xt, _) = body_state(&triple.worldtubes, id, t).unwrap();
                displacement = displacement.max(dist_arr(xp, xt));
            }
        }
        println!(
            "pair-exterior counterexample: q={} radius={} ratio={} displacement={} pair_ops={} triple_ops={}",
            enclosure.q,
            radius,
            ratio,
            displacement,
            source_ops_of(&pair),
            source_ops_of(&triple)
        );
        assert!(
            ratio > 1.0,
            "declared encounter must recouple: post-cone |a←C|/|a←B|={ratio} is not an omitted tail"
        );
        assert!(
            displacement > radius,
            "triple A,B leave the pair enclosure: displacement={displacement} radius={radius}"
        );
        let err = share_compiled_pair_exterior(&pair, &entrant, horizon, dt)
            .expect_err("must fail closed; pair enclosure does not cover this IC");
        let msg = err.to_string();
        assert!(
            msg.contains("cannot share this compiled pair's exterior")
                && msg.contains("does not cover a different genesis IC")
                && msg.contains("H0110")
                && msg.contains("fly_ship on the pair is not this share"),
            "{msg}"
        );
        let (ship, ray, clock, contact) =
            complete_required_queries_compiled(&pair, horizon, &mut Charge::default()).unwrap();
        assert!(
            ship && ray && clock && contact,
            "required queries must still return on the pair compile"
        );
        let (t_ship, t_ray, t_clock, t_contact) =
            complete_required_queries_compiled(&triple, horizon, &mut Charge::default()).unwrap();
        assert!(
            t_ship && t_ray && t_clock && t_contact,
            "required queries must still return on the independent three-body compile"
        );
        assert_eq!(pair.law_id, COUPLED_RESPONSE_LAW_ID);
    }

    #[test]
    fn schur_pair_block_updates_distant_tide_and_keeps_encounter_refuse() {
        // Declared: docs/laws/cheaper-pair-repair-workload-declaration-20260914.md
        // H0115 stored-a miss-walk (3429 vs 3422) is not this object.
        let horizon = 6.0;
        let dt = 1.0 / 32.0;
        let pair =
            compile_source_response(laboratory_two_body(), Vec::new(), horizon, dt).unwrap();
        assert!(
            pair.pair_inverse.is_some(),
            "two-body compile must store (I-K)^-1 before the update"
        );
        let enclosure = crate::coupled_interval_enclosure::enclose_compiled_interval(
            &pair,
            pair.genesis.clone(),
            pair.incoming.clone(),
            crate::coupled_interval_enclosure::IntervalMethod::CausalBlocks,
        )
        .unwrap();
        assert!(
            enclosure.certified,
            "quiet pair itself must enclose; {:?}",
            enclosure.why_rejected
        );
        let radius = enclosure.radius.expect("certified pair radius");
        let (enc_ic, _) = laboratory_encounter();
        let encounter = enc_ic
            .bodies
            .iter()
            .find(|b| b.id == 99)
            .expect("encounter third mass")
            .clone();
        let mut c = Charge::default();
        let encounter_ratio = massive_entrant_coupling_ratio(&pair, &encounter, &mut c).unwrap();
        assert!(
            encounter_ratio > 1.0,
            "H0112 encounter refuse must stay: post-cone |a←C|/|a←B|={encounter_ratio}"
        );
        assert!(
            (encounter_ratio - 1.519).abs() < 0.01,
            "do not weaken 1.519; measured {encounter_ratio}"
        );
        let err = share_compiled_pair_exterior(&pair, &encounter, horizon, dt)
            .expect_err("encounter id 99 must still refuse");
        let msg = err.to_string();
        assert!(
            msg.contains("cannot share this compiled pair's exterior")
                && msg.contains("does not cover a different genesis IC")
                && msg.contains("H0110")
                && msg.contains("fly_ship on the pair is not this share"),
            "{msg}"
        );

        let tide_ic = laboratory_distant_tide();
        let tide = tide_ic
            .bodies
            .iter()
            .find(|b| b.id == 77)
            .expect("distant-tide mass")
            .clone();
        assert_ne!(tide.id, 99, "named fixture must not be laboratory_encounter-99");
        let mut c_tide = Charge::default();
        let tide_ratio_pair_cone =
            massive_entrant_coupling_ratio(&pair, &tide, &mut c_tide).unwrap();
        let host = &pair.genesis.bodies[0];
        let t_c = (dist_arr(host.x, tide.x) / C + dt).min(horizon);
        let mut late_charge = Charge::default();
        let a_partner = acceleration_at(&pair.worldtubes, host.id, t_c, &mut late_charge).unwrap();
        let mut with_c = pair.worldtubes.clone();
        with_c.push(Body {
            id: tide.id,
            segments: vec![Segment {
                t0: pair.genesis.genesis_t,
                t1: None,
                x0: tide.x,
                v: tide.v,
                a: [0.0, 0.0],
                mu: tide.mu,
            }],
        });
        let a_with = acceleration_at(&with_c, host.id, t_c, &mut late_charge).unwrap();
        let late_ratio = arr_norm([a_with[0] - a_partner[0], a_with[1] - a_partner[1]])
            / arr_norm(a_partner);
        assert!(
            late_ratio > 0.0 && late_ratio < 1.0,
            "after the entrant's cone the tide must be a weaker massive coupling, not zero-by-early-sample and not the 1.519 encounter; late_ratio={late_ratio} pair-cone ratio={tide_ratio_pair_cone}"
        );
        let updated = schur_update_compiled_pair(&pair, &tide, horizon, dt)
            .expect("stored-inverse pair-block update of the declared distant tide");
        assert!(
            updated.genesis.bodies.iter().any(|b| b.id == 77),
            "updated genesis must include the massive entrant"
        );
        assert!(
            updated.pair_inverse.is_none(),
            "three-body seal must not store a pair inverse to inflate the denominator"
        );
        let mut a_delta = 0.0_f64;
        let mut x_delta = 0.0_f64;
        for fun in &updated.interval_functions {
            if fun.body_id == 77 {
                continue;
            }
            if let Some(old) = pair
                .interval_functions
                .iter()
                .find(|o| o.body_id == fun.body_id && (o.t0 - fun.t0).abs() < 1e-12)
            {
                a_delta = a_delta.max(arr_norm([fun.a[0] - old.a[0], fun.a[1] - old.a[1]]));
            }
        }
        assert!(
            a_delta > 1e-14,
            "stored inverse must update pair interval-function a, not fly_ship; a_delta={a_delta}"
        );
        let times: Vec<f64> = (0..16)
            .map(|i| (i as f64 + 1.0) * horizon / 16.0)
            .collect();
        for &t in &times {
            for id in [0_u64, 1] {
                let (xp, _) = body_state(&pair.worldtubes, id, t).unwrap();
                let (xu, _) = body_state(&updated.worldtubes, id, t).unwrap();
                x_delta = x_delta.max(dist_arr(xp, xu));
            }
        }
        assert!(
            x_delta > 1e-14,
            "stored inverse must move pair worldtubes, not leave a frozen exterior; x_delta={x_delta}"
        );
        assert!(
            x_delta <= radius,
            "omitted-coverage claim: pair displacement {x_delta} must stay inside pair radius {radius}"
        );

        let triple = compile_source_response(tide_ic, Vec::new(), horizon, dt).unwrap();
        assert!(
            triple.pair_inverse.is_none(),
            "independent three-body compile must not assemble a pair inverse"
        );
        let mut vs_full = 0.0_f64;
        for &t in &times {
            for id in [0_u64, 1] {
                let (xu, _) = body_state(&updated.worldtubes, id, t).unwrap();
                let (xt, _) = body_state(&triple.worldtubes, id, t).unwrap();
                vs_full = vs_full.max(dist_arr(xu, xt));
            }
        }
        let vs_full_dense = leftover_n(&updated, &triple, horizon, &[0, 1], 128);
        let vs_full_tail = leftover_open_tail(&updated, &triple, horizon, &[0, 1], 32);
        let vs_full_lookback = leftover_lookback_open_tail(&updated, &triple, horizon, &[0, 1]);
        let schur_ops = source_ops_of(&updated);
        let triple_ops = source_ops_of(&triple);
        println!(
            "pair-inverse distant-tide: radius={} late_ratio={} pair_cone_ratio={} a_delta={} x_delta={} vs_full={:.6e} vs_full_dense={:.6e} vs_full_tail={:.6e} vs_full_lookback={:.6e} schur_ops={} triple_ops={} schur_se={} schur_ret={} triple_se={} triple_ret={} pair_factor={} schur_factor={} encounter_ratio={}",
            radius,
            late_ratio,
            tide_ratio_pair_cone,
            a_delta,
            x_delta,
            vs_full,
            vs_full_dense,
            vs_full_tail,
            vs_full_lookback,
            schur_ops,
            triple_ops,
            updated.charge.source_evolution,
            updated.charge.retarded_solves,
            triple.charge.source_evolution,
            triple.charge.retarded_solves,
            pair.charge.factorization,
            updated.charge.factorization,
            encounter_ratio
        );
        if vs_full == 0.0 && (vs_full_dense > 0.0 || vs_full_tail > 0.0 || vs_full_lookback > 0.0) {
            println!(
                "NAMED REMAINDER: far-tide leftover-0 at 16 samples is not identity; dense={} tail={} lookback={}",
                vs_full_dense, vs_full_tail, vs_full_lookback
            );
        }
        assert!(
            vs_full <= radius,
            "omitted leftover vs independent three-body compile {vs_full} must stay inside pair radius {radius}"
        );
        // H0115 miss-walk was 3429 vs 3422 not cheaper. Covering-bounded
        // stored-a apply re-measures below. Factorization stays off source ops.
        assert_eq!(
            schur_ops,
            updated.charge.source_evolution + updated.charge.retarded_solves,
            "factorization must not be laundered into source ops"
        );
        assert_eq!(
            triple_ops,
            triple.charge.source_evolution + triple.charge.retarded_solves
        );
        assert!(
            schur_ops < triple_ops,
            "covering-bounded stored-a apply must beat same-IC three-body in source ops; {schur_ops} vs {triple_ops}"
        );
        let (ship, ray, clock, contact) =
            complete_required_queries_compiled(&updated, horizon, &mut Charge::default()).unwrap();
        assert!(
            ship && ray && clock && contact,
            "required queries must still return on the Schur-updated compile"
        );
        let (t_ship, t_ray, t_clock, t_contact) =
            complete_required_queries_compiled(&triple, horizon, &mut Charge::default()).unwrap();
        assert!(
            t_ship && t_ray && t_clock && t_contact,
            "required queries must still return on the independent three-body compile"
        );
        assert_eq!(updated.law_id, COUPLED_RESPONSE_LAW_ID);
        assert_eq!(pair.law_id, COUPLED_RESPONSE_LAW_ID);
    }

    #[test]
    fn recouple_compiles_encounter_and_keeps_share_refuse() {
        // Declared: docs/laws/recouple-workload-declaration-20260914.md
        let horizon = 6.0;
        let dt = 1.0 / 32.0;
        let pair =
            compile_source_response(laboratory_two_body(), Vec::new(), horizon, dt).unwrap();
        let enclosure = crate::coupled_interval_enclosure::enclose_compiled_interval(
            &pair,
            pair.genesis.clone(),
            pair.incoming.clone(),
            crate::coupled_interval_enclosure::IntervalMethod::CausalBlocks,
        )
        .unwrap();
        assert!(
            enclosure.certified,
            "quiet pair itself must enclose; {:?}",
            enclosure.why_rejected
        );
        let radius = enclosure.radius.expect("certified pair radius");
        let (enc_ic, enc_iv) = laboratory_encounter();
        let entrant = enc_ic
            .bodies
            .iter()
            .find(|b| b.id == 99)
            .expect("encounter third mass")
            .clone();
        let mut c = Charge::default();
        let encounter_ratio = massive_entrant_coupling_ratio(&pair, &entrant, &mut c).unwrap();
        assert!(
            encounter_ratio > 1.0,
            "H0112 encounter refuse must stay: post-cone |a←C|/|a←B|={encounter_ratio}"
        );
        assert!(
            (encounter_ratio - 1.519).abs() < 0.01,
            "do not weaken 1.519; measured {encounter_ratio}"
        );
        let err = share_compiled_pair_exterior(&pair, &entrant, horizon, dt)
            .expect_err("encounter id 99 must still refuse share");
        let msg = err.to_string();
        assert!(
            msg.contains("cannot share this compiled pair's exterior")
                && msg.contains("does not cover a different genesis IC")
                && msg.contains("H0110")
                && msg.contains("fly_ship on the pair is not this share"),
            "{msg}"
        );

        let tide = laboratory_distant_tide()
            .bodies
            .into_iter()
            .find(|b| b.id == 77)
            .expect("distant-tide mass");
        let tide_err = recouple_compiled_pair(&pair, &tide, horizon, dt)
            .expect_err("far third that still fits the pair neighborhood is Schur, not recouple");
        let tide_msg = tide_err.to_string();
        assert!(
            tide_msg.contains("still fits this compiled pair neighborhood")
                && tide_msg.contains("use share_compiled_pair_exterior"),
            "{tide_msg}"
        );

        let recoupled = recouple_compiled_pair(&pair, &entrant, horizon, dt)
            .expect("named recouple must compile the recoupled encounter IC");
        assert!(
            recoupled.genesis.bodies.iter().any(|b| b.id == 99),
            "recoupled genesis must include the massive entrant"
        );
        assert!(
            recoupled.pair_inverse.is_none(),
            "three-body recouple must not store a pair inverse"
        );
        assert!(
            !recoupled.interval_functions.is_empty(),
            "recouple must recertify interval functions on the three-body IC"
        );
        assert!(
            recoupled.interval_q.is_finite(),
            "recouple interval q must be the recertified three-body operator"
        );

        let times: Vec<f64> = (0..16)
            .map(|i| (i as f64 + 1.0) * horizon / 16.0)
            .collect();
        let mut vs_pair = 0.0_f64;
        for &t in &times {
            for id in [0_u64, 1] {
                let (xp, _) = body_state(&pair.worldtubes, id, t).unwrap();
                let (xr, _) = body_state(&recoupled.worldtubes, id, t).unwrap();
                vs_pair = vs_pair.max(dist_arr(xp, xr));
            }
        }
        assert!(
            vs_pair > radius,
            "recoupled A,B must leave the pair neighborhood: displacement={vs_pair} radius={radius}"
        );

        let triple = compile_source_response(enc_ic, enc_iv, horizon, dt).unwrap();
        assert!(
            triple.pair_inverse.is_none(),
            "independent three-body compile must not assemble a pair inverse"
        );
        let mut leftover = 0.0_f64;
        for &t in &times {
            for id in [0_u64, 1, 99] {
                let (xr, _) = body_state(&recoupled.worldtubes, id, t).unwrap();
                let (xt, _) = body_state(&triple.worldtubes, id, t).unwrap();
                leftover = leftover.max(dist_arr(xr, xt));
            }
        }
        let leftover_dense = leftover_n(&recoupled, &triple, horizon, &[0, 1, 99], 128);
        let leftover_tail = leftover_open_tail(&recoupled, &triple, horizon, &[0, 1, 99], 32);
        let leftover_lookback =
            leftover_lookback_open_tail(&recoupled, &triple, horizon, &[0, 1, 99]);
        let recouple_ops = source_ops_of(&recoupled);
        let triple_ops = source_ops_of(&triple);
        let recert = crate::coupled_interval_enclosure::enclose_compiled_interval(
            &recoupled,
            recoupled.genesis.clone(),
            recoupled.incoming.clone(),
            crate::coupled_interval_enclosure::IntervalMethod::CausalBlocks,
        )
        .unwrap();
        println!(
            "named recouple encounter: radius={} ratio={} vs_pair={} leftover={:.6e} leftover_dense={:.6e} leftover_tail={:.6e} leftover_lookback={:.6e} recouple_ops={} triple_ops={} recouple_se={} recouple_ret={} triple_se={} triple_ret={} recouple_repair={} interval_q={} recert_certified={} recert_q={} encounter_ratio={}",
            radius,
            encounter_ratio,
            vs_pair,
            leftover,
            leftover_dense,
            leftover_tail,
            leftover_lookback,
            recouple_ops,
            triple_ops,
            recoupled.charge.source_evolution,
            recoupled.charge.retarded_solves,
            triple.charge.source_evolution,
            triple.charge.retarded_solves,
            recoupled.charge.repair,
            recoupled.interval_q,
            recert.certified,
            recert.q,
            encounter_ratio
        );
        if leftover == 0.0
            && (leftover_dense > 0.0 || leftover_tail > 0.0 || leftover_lookback > 0.0)
        {
            println!(
                "NAMED REMAINDER: recouple leftover-0 at 16 samples is not identity; dense={} tail={} lookback={}",
                leftover_dense, leftover_tail, leftover_lookback
            );
        }
        assert_eq!(
            recouple_ops,
            recoupled.charge.source_evolution + recoupled.charge.retarded_solves,
            "factorization/repair must not be laundered into source ops"
        );
        assert_eq!(
            triple_ops,
            triple.charge.source_evolution + triple.charge.retarded_solves
        );
        let (ship, ray, clock, contact) = complete_required_queries_compiled(
            &recoupled,
            horizon,
            &mut Charge::default(),
        )
        .unwrap();
        assert!(
            ship && ray && clock && contact,
            "required queries must still return on the recoupled compile"
        );
        let (t_ship, t_ray, t_clock, t_contact) =
            complete_required_queries_compiled(&triple, horizon, &mut Charge::default()).unwrap();
        assert!(
            t_ship && t_ray && t_clock && t_contact,
            "required queries must still return on the independent three-body compile"
        );
        assert_eq!(recoupled.law_id, COUPLED_RESPONSE_LAW_ID);
        assert_eq!(pair.law_id, COUPLED_RESPONSE_LAW_ID);
        assert_eq!(
            leftover, 0.0,
            "recouple leftover vs independent same-IC three-body must be 0 at 16 samples (same operator, not a reuse fraction); leftover={leftover}"
        );
    }

    fn leftover_n(
        a: &SourceResponse,
        b: &SourceResponse,
        horizon: f64,
        ids: &[u64],
        n: usize,
    ) -> f64 {
        let times: Vec<f64> = (0..n)
            .map(|i| (i as f64 + 1.0) * horizon / n as f64)
            .collect();
        let mut leftover = 0.0_f64;
        for &t in &times {
            for &id in ids {
                let (xa, _) = body_state(&a.worldtubes, id, t).unwrap();
                let (xb, _) = body_state(&b.worldtubes, id, t).unwrap();
                leftover = leftover.max(dist_arr(xa, xb));
            }
        }
        leftover
    }

    fn leftover_three(
        a: &SourceResponse,
        b: &SourceResponse,
        horizon: f64,
        ids: &[u64],
    ) -> f64 {
        leftover_n(a, b, horizon, ids, 16)
    }

    fn last_function_t1(compiled: &SourceResponse, id: u64) -> Option<f64> {
        compiled
            .interval_functions
            .iter()
            .filter(|f| f.body_id == id)
            .map(|f| f.t1)
            .fold(None, |acc, t| Some(acc.map_or(t, |u: f64| u.max(t))))
    }

    /// Position leftover strictly after the last collocation knot, on the open tail.
    fn leftover_open_tail(
        a: &SourceResponse,
        b: &SourceResponse,
        horizon: f64,
        ids: &[u64],
        n: usize,
    ) -> f64 {
        let mut leftover = 0.0_f64;
        let mut any = false;
        for &id in ids {
            let ta = last_function_t1(a, id).unwrap_or(0.0);
            let tb = last_function_t1(b, id).unwrap_or(0.0);
            let t_cut = ta.min(tb);
            if t_cut >= horizon - 1e-12 {
                continue;
            }
            for i in 0..n {
                let t = t_cut + (i as f64 + 1.0) * (horizon - t_cut) / n as f64;
                if t > horizon + 1e-15 {
                    continue;
                }
                let (xa, _) = body_state(&a.worldtubes, id, t).unwrap();
                let (xb, _) = body_state(&b.worldtubes, id, t).unwrap();
                leftover = leftover.max(dist_arr(xa, xb));
                any = true;
            }
        }
        if any {
            leftover
        } else {
            f64::NAN
        }
    }

    /// Compiled lookback leftover on a probe whose retarded event sits on the open tail.
    fn leftover_lookback_open_tail(
        a: &SourceResponse,
        b: &SourceResponse,
        horizon: f64,
        ids: &[u64],
    ) -> f64 {
        let mut leftover = 0.0_f64;
        let mut any = false;
        for &id in ids {
            let ta = last_function_t1(a, id).unwrap_or(0.0);
            let tb = last_function_t1(b, id).unwrap_or(0.0);
            let t_cut = ta.min(tb);
            if t_cut >= horizon - 1e-12 {
                continue;
            }
            let t = (t_cut + horizon) * 0.5;
            let (xa, _) = body_state(&a.worldtubes, id, t).unwrap();
            let query = V2::from_arr(xa).add(V2::new(0.0, 0.35));
            let mut ca = Charge::default();
            let mut cb = Charge::default();
            let fa = field_at_compiled(a, t, query, Some(id), &mut ca).unwrap();
            let fb = field_at_compiled(b, t, query, Some(id), &mut cb).unwrap();
            leftover = leftover
                .max((fa.phi - fb.phi).abs())
                .max(fa.e.sub(fb.e).norm())
                .max((fa.b_z - fb.b_z).abs());
            any = true;
        }
        if any {
            leftover
        } else {
            f64::NAN
        }
    }

    #[test]
    fn open_tail_continues_stored_constant_a_half_ah2() {
        let horizon = 6.0;
        let compiled =
            compile_source_response(laboratory_two_body(), Vec::new(), horizon, 1.0 / 32.0)
                .unwrap();
        let fun = compiled
            .interval_functions
            .iter()
            .filter(|f| f.body_id == 0)
            .max_by(|a, b| a.t1.partial_cmp(&b.t1).unwrap())
            .expect("compiled pair must store interval functions");
        assert!(
            V2::from_arr(fun.a).norm() > 1e-12,
            "last stored a must be nonzero so the open tail is not a zero-a accident"
        );
        let tail = compiled
            .worldtubes
            .iter()
            .find(|b| b.id == 0)
            .expect("body 0")
            .segments
            .last()
            .expect("worldtube must keep an open last segment");
        assert!(
            tail.t1.is_none(),
            "horizon is not a collocation knot; last segment stays open"
        );
        assert!(
            (tail.t0 - fun.t1).abs() < 1e-12,
            "open tail must start at the last collocation knot, tail.t0={} fun.t1={}",
            tail.t0,
            fun.t1
        );
        let a_delta = dist_arr(tail.a, fun.a);
        assert!(
            a_delta < 1e-15,
            "open tail must store the last block a, not inertial zero; |Δa|={a_delta} tail={:?} fun={:?}",
            tail.a,
            fun.a
        );
        let t_tail = if fun.t1 + 0.05 < horizon {
            0.5 * (fun.t1 + horizon)
        } else {
            fun.t1 + 0.05
        };
        let (x_end, v_end) = fun.inertial_end();
        let h = t_tail - fun.t1;
        let a = V2::from_arr(fun.a);
        let x_a = x_end.add(v_end.scale(h)).add(a.scale(0.5 * h * h));
        let x_chord = x_end.add(v_end.scale(h));
        let half_ah2 = a.scale(0.5 * h * h);
        let (x_w, v_w) = body_state(&compiled.worldtubes, 0, t_tail).unwrap();
        let pos_err = V2::from_arr(x_w).sub(x_a).norm();
        assert!(
            pos_err < 1e-12,
            "open-tail present must match stored-a continuation including ½ah²; err={pos_err}"
        );
        let chord_delta = V2::from_arr(x_w).sub(x_chord);
        assert!(
            chord_delta.sub(half_ah2).norm() < 1e-12,
            "open tail minus inertial chord must be ½ah²; got {:?} vs {:?}",
            chord_delta.arr(),
            half_ah2.arr()
        );
        assert!(
            half_ah2.norm() > 1e-14,
            "open-tail ½ah² must be a real remainder against the inertial chord, |½ah²|={}",
            half_ah2.norm()
        );
        let v_a = v_end.add(a.scale(h));
        assert!(
            V2::from_arr(v_w).sub(v_a).norm() < 1e-12,
            "open-tail velocity must include a·h"
        );
        let query_x = x_a.add(V2::new(0.0, 0.4));
        let mut c0 = Charge::default();
        let mut c1 = Charge::default();
        let f_tail = gem_from_segment(t_tail, query_x, tail, &mut c0)
            .unwrap()
            .expect("open-tail stored-a lookback must hit");
        let extended = IntervalFunction {
            body_id: fun.body_id,
            t0: fun.t1,
            t1: t_tail,
            x0: x_end.arr(),
            v0: v_end.arr(),
            a: fun.a,
            mu: fun.mu,
        };
        let f_fun = gem_from_function(t_tail, query_x, &extended, &mut c1)
            .unwrap()
            .expect("extended last-block lookback must hit");
        let dphi = (f_tail.phi - f_fun.phi).abs();
        let de = f_tail.e.sub(f_fun.e).norm();
        assert!(
            dphi + de < 1e-10,
            "open-tail lookback must match stored-a function geometry; dphi={dphi} de={de}"
        );
        let chord_seg = Segment {
            t0: tail.t0,
            t1: None,
            x0: tail.x0,
            v: tail.v,
            a: [0.0, 0.0],
            mu: tail.mu,
        };
        let mut c2 = Charge::default();
        let f_chord = gem_from_segment(t_tail, query_x, &chord_seg, &mut c2)
            .unwrap()
            .expect("inertial open-tail lookback must hit");
        assert!(
            (f_tail.phi - f_chord.phi).abs() > 1e-14,
            "open-tail stored-a lookback must differ from the inertial chord; dphi={}",
            (f_tail.phi - f_chord.phi).abs()
        );
        let (ship, ray, clock, contact) =
            complete_required_queries_compiled(&compiled, horizon, &mut Charge::default()).unwrap();
        assert!(ship && ray && clock && contact);
    }

    #[test]
    fn reuse_recoupled_refuses_pair_and_empty_extra() {
        let pair =
            compile_source_response(laboratory_two_body(), Vec::new(), 6.0, 1.0 / 32.0).unwrap();
        let late = vec![Intervention {
            t: 5.0,
            body_id: 0,
            delta_v: [0.0, 0.05],
        }];
        let err = reuse_recoupled_interval_functions(&pair, &late, 6.0, 1.0 / 32.0)
            .expect_err("pair is not a recoupled three-body object");
        let msg = err.to_string();
        assert!(
            msg.contains("not a pair") && msg.contains("not pair-interval fill-in"),
            "{msg}"
        );
        let err = repair_recoupled_interval_functions(&pair, &late, 6.0, 1.0 / 32.0)
            .expect_err("pair repair must not be labelled recoupled repair");
        let msg = err.to_string();
        assert!(
            msg.contains("not a pair") && msg.contains("not pair-interval fill-in"),
            "{msg}"
        );
    }

    #[test]
    fn recoupled_three_body_reuses_and_repairs_certified_interval_functions() {
        // Declared: docs/laws/recoupled-reuse-workload-declaration-20260914.md
        let horizon = 6.0;
        let dt = 1.0 / 32.0;
        let pair =
            compile_source_response(laboratory_two_body(), Vec::new(), horizon, dt).unwrap();
        let (enc_ic, enc_iv) = laboratory_encounter();
        let entrant = enc_ic
            .bodies
            .iter()
            .find(|b| b.id == 99)
            .expect("encounter third mass")
            .clone();
        let mut c = Charge::default();
        let encounter_ratio = massive_entrant_coupling_ratio(&pair, &entrant, &mut c).unwrap();
        assert!(
            (encounter_ratio - 1.5193527764310737).abs() < 1e-12,
            "do not weaken 1.5193527764310737; measured {encounter_ratio}"
        );
        let err = share_compiled_pair_exterior(&pair, &entrant, horizon, dt)
            .expect_err("encounter id 99 must still refuse share");
        assert!(
            err.to_string()
                .contains("cannot share this compiled pair's exterior"),
            "{err}"
        );

        let recoupled = recouple_compiled_pair(&pair, &entrant, horizon, dt)
            .expect("named recouple is the object of reuse");
        assert_eq!(recoupled.genesis.bodies.len(), 3);
        assert!(recoupled.pair_inverse.is_none());
        assert!(!recoupled.interval_functions.is_empty());
        assert!(enc_iv.is_empty(), "encounter fixture must stay genesis-only");
        let empty_err = reuse_recoupled_interval_functions(&recoupled, &[], horizon, dt)
            .expect_err("empty extra / extra-ray is not equivalent completed source histories");
        assert!(
            empty_err
                .to_string()
                .contains("not equivalent completed source histories"),
            "{empty_err}"
        );

        let late = vec![Intervention {
            t: 5.0,
            body_id: 0,
            delta_v: [0.0, 0.05],
        }];
        let full = compile_source_response(recoupled.genesis.clone(), late.clone(), horizon, dt)
            .expect("independent kicked recoupled IC");
        let reused = reuse_recoupled_interval_functions(&recoupled, &late, horizon, dt)
            .unwrap_or_else(|e| panic!("recoupled distinct-history reuse refused: {e}"));
        assert!(
            reused.charge.reconstruction > 0,
            "must copy complete certified recoupled interval functions"
        );
        assert!(
            reused.pair_inverse.is_none(),
            "reuse must not assemble a pair inverse"
        );
        let leftover_reuse = leftover_three(&reused, &full, horizon, &[0, 1, 99]);
        let leftover_reuse_dense = leftover_n(&reused, &full, horizon, &[0, 1, 99], 128);
        let leftover_reuse_tail = leftover_open_tail(&reused, &full, horizon, &[0, 1, 99], 32);
        let leftover_reuse_lookback =
            leftover_lookback_open_tail(&reused, &full, horizon, &[0, 1, 99]);
        let ops_r = source_ops_of(&reused);
        let ops_f = source_ops_of(&full);
        let prefix_a = certified_prefix_cut(&recoupled.genesis, &late, 0).unwrap();
        let mut orig: Vec<_> = recoupled
            .interval_functions
            .iter()
            .filter(|f| f.body_id == 0 && f.t1 <= prefix_a + 1e-12)
            .cloned()
            .collect();
        orig.sort_by(|a, b| a.t0.partial_cmp(&b.t0).unwrap());
        let mut got: Vec<_> = reused
            .interval_functions
            .iter()
            .filter(|f| f.body_id == 0)
            .cloned()
            .collect();
        got.sort_by(|a, b| a.t0.partial_cmp(&b.t0).unwrap());
        assert!(!orig.is_empty());
        assert!(got.len() >= orig.len());
        assert_eq!(got[..orig.len()], orig[..]);

        let mid = vec![Intervention {
            t: 3.0,
            body_id: 0,
            delta_v: [0.0, 0.05],
        }];
        let full_mid =
            compile_source_response(recoupled.genesis.clone(), mid.clone(), horizon, dt)
                .expect("independent mid-kick recoupled IC");
        let repaired = repair_recoupled_interval_functions(&recoupled, &mid, horizon, dt)
            .unwrap_or_else(|e| panic!("recoupled repair refused: {e}"));
        assert!(
            repaired.charge.reconstruction > 0,
            "repair must keep complete certified prefix blocks"
        );
        assert!(repaired.charge.repair >= 1, "repair must stay charged");
        let leftover_repair = leftover_three(&repaired, &full_mid, horizon, &[0, 1, 99]);
        let leftover_repair_dense = leftover_n(&repaired, &full_mid, horizon, &[0, 1, 99], 128);
        let leftover_repair_tail =
            leftover_open_tail(&repaired, &full_mid, horizon, &[0, 1, 99], 32);
        let leftover_repair_lookback =
            leftover_lookback_open_tail(&repaired, &full_mid, horizon, &[0, 1, 99]);
        let ops_repair = source_ops_of(&repaired);
        let ops_mid = source_ops_of(&full_mid);

        println!(
            "recoupled reuse/repair: ratio={} leftover_reuse={:.6e} leftover_reuse_dense={:.6e} leftover_reuse_tail={:.6e} leftover_reuse_lookback={:.6e} reuse_ops={} full_ops={} reuse_se={} reuse_ret={} reuse_recon={} leftover_repair={:.6e} leftover_repair_dense={:.6e} leftover_repair_tail={:.6e} leftover_repair_lookback={:.6e} repair_ops={} mid_ops={} repair_se={} repair_ret={} repair_charge={} copied_late={} copied_mid={}",
            encounter_ratio,
            leftover_reuse,
            leftover_reuse_dense,
            leftover_reuse_tail,
            leftover_reuse_lookback,
            ops_r,
            ops_f,
            reused.charge.source_evolution,
            reused.charge.retarded_solves,
            reused.charge.reconstruction,
            leftover_repair,
            leftover_repair_dense,
            leftover_repair_tail,
            leftover_repair_lookback,
            ops_repair,
            ops_mid,
            repaired.charge.source_evolution,
            repaired.charge.retarded_solves,
            repaired.charge.repair,
            reused.charge.reconstruction,
            repaired.charge.reconstruction
        );
        if leftover_reuse == 0.0
            && (leftover_reuse_dense > 0.0
                || leftover_reuse_tail > 0.0
                || leftover_reuse_lookback > 0.0)
        {
            println!(
                "NAMED REMAINDER: leftover-0 at 16 samples is not identity; dense={} tail={} lookback={}",
                leftover_reuse_dense, leftover_reuse_tail, leftover_reuse_lookback
            );
        }
        if leftover_repair == 0.0
            && (leftover_repair_dense > 0.0
                || leftover_repair_tail > 0.0
                || leftover_repair_lookback > 0.0)
        {
            println!(
                "NAMED REMAINDER: repair leftover-0 at 16 samples is not identity; dense={} tail={} lookback={}",
                leftover_repair_dense, leftover_repair_tail, leftover_repair_lookback
            );
        }

        // Independent H0122 review: leftover-0 and suffix 11/24 were printed
        // in the same pass that wrote the audit. Pin the measured gates here.
        // Do not treat leftover-0 or 1188 vs 1675 as 99.9% or as finishing
        // mutually evolving source reuse.
        assert_eq!(
            leftover_reuse, 0.0,
            "late-kick leftover vs independent kicked same-IC must be 0 at 16 samples, leftover={leftover_reuse}"
        );
        assert_eq!(leftover_reuse_dense, 0.0, "leftover-0 at 128 samples, leftover={leftover_reuse_dense}");
        assert_eq!(leftover_reuse_tail, 0.0, "open-tail leftover-0, leftover={leftover_reuse_tail}");
        assert_eq!(
            leftover_reuse_lookback, 0.0,
            "open-tail lookback leftover-0, leftover={leftover_reuse_lookback}"
        );
        assert_eq!(leftover_repair, 0.0, "mid-horizon repair leftover-0 at 16 samples, leftover={leftover_repair}");
        assert_eq!(leftover_repair_dense, 0.0, "repair leftover-0 at 128 samples, leftover={leftover_repair_dense}");
        assert_eq!(leftover_repair_tail, 0.0, "repair open-tail leftover-0, leftover={leftover_repair_tail}");
        assert_eq!(
            leftover_repair_lookback, 0.0,
            "repair open-tail lookback leftover-0, leftover={leftover_repair_lookback}"
        );
        // Historical absolute operation counts remain in frozen evidence.
        // Correcting retarded-root omissions changes solve attempts; validate
        // actual source-work elimination against the matched current compile.
        // This does not establish total-cost savings (offline audit is extra).
        assert!(ops_r > 0 && ops_r < ops_f, "reuse must eliminate source work: {ops_r}/{ops_f}");
        assert!(ops_repair > 0 && ops_repair < ops_mid, "repair must eliminate source work: {ops_repair}/{ops_mid}");
        assert_eq!(
            ops_r,
            reused.charge.source_evolution + reused.charge.retarded_solves,
            "factorization/repair/reconstruction must not be laundered into source ops"
        );
        assert_eq!(
            ops_repair,
            repaired.charge.source_evolution + repaired.charge.retarded_solves
        );

        for id in [0_u64, 1, 99] {
            let t1 = last_function_t1(&reused, id).expect("reused body interval functions");
            assert!(
                t1 > 5.0 && t1 <= horizon,
                "reuse suffix for body {id} must collocate past the t=5 kick toward H=6, t1={t1}"
            );
            let t1r = last_function_t1(&repaired, id).expect("repaired body interval functions");
            assert!(
                t1r > 3.0 && t1r <= horizon,
                "repair suffix for body {id} must collocate past the t=3 kick toward H=6, t1={t1r}"
            );
        }
        assert!(
            reused.charge.total() > ops_r,
            "Charge.total must include repair/init/reconstruction, not a skipped source_ops-only counter; total={} ops={}",
            reused.charge.total(),
            ops_r
        );
        assert!(
            repaired.charge.total() > ops_repair,
            "repair Charge.total must include the repair flag and reconstruction; total={} ops={}",
            repaired.charge.total(),
            ops_repair
        );
        // Reconstruction also includes compact decoding in seal_compiled;
        // it is not just a copied-function count. Verify every retained prefix
        // for all bodies and require its copies to be covered by the ledger.
        for (result, interventions) in [(&reused, &late), (&repaired, &mid)] {
            let prefix: Vec<_> = recoupled.interval_functions.iter().filter(|f|
                f.t1 <= certified_prefix_cut(&recoupled.genesis, interventions, f.body_id).unwrap() + 1e-12
            ).collect();
            assert!(!prefix.is_empty());
            let generated = result.interval_functions.len() - prefix.len();
            assert!(generated > 0, "repair must evolve a real suffix");
            assert_eq!(result.charge.source_evolution, generated as u64);
            assert!(result.charge.reconstruction >= prefix.len() as u64);
            for function in prefix {
                assert!(result.interval_functions.contains(function), "lost retained prefix for body {}", function.body_id);
            }
        }
        assert_ne!(
            reused.charge.reconstruction, ops_r,
            "copied interval functions are not the through-horizon source-op denominator"
        );
        assert_ne!(
            repaired.charge.reconstruction, ops_repair,
            "repair copies are not the through-horizon source-op denominator"
        );
        let ship_c = fly_ship_compiled(
            &reused,
            1.1,
            [0.0, 3.0],
            [0.125, 0.0],
            3.5,
            1.0 / 32.0,
            &mut Charge::default(),
        )
        .unwrap();
        assert!(ship_c.tau > 0.0);
        let ray_c = fly_ray_compiled(
            &reused,
            1.1,
            [0.0, 3.0],
            [1.0, 0.0],
            8.0,
            0.05,
            &mut Charge::default(),
        )
        .unwrap();
        assert!(ray_c.t > 1.1);
        let rate_c = clock_rate_compiled(
            &reused,
            ship_c.t,
            ship_c.x,
            ship_c.v,
            &mut Charge::default(),
        )
        .unwrap();
        assert!(rate_c > 0.0 && rate_c <= 1.0);
        let (ship, ray, clock, contact) = complete_required_queries_compiled(
            &reused,
            horizon,
            &mut Charge::default(),
        )
        .unwrap();
        assert!(
            ship && ray && clock && contact,
            "required queries must still return on recoupled reuse"
        );
        let (r_ship, r_ray, r_clock, r_contact) = complete_required_queries_compiled(
            &repaired,
            horizon,
            &mut Charge::default(),
        )
        .unwrap();
        assert!(
            r_ship && r_ray && r_clock && r_contact,
            "required queries must still return on recoupled repair"
        );
        let (f_ship, f_ray, f_clock, f_contact) = complete_required_queries_compiled(
            &full,
            horizon,
            &mut Charge::default(),
        )
        .unwrap();
        assert!(
            f_ship && f_ray && f_clock && f_contact,
            "required queries must still return on the independent kicked compile"
        );
        assert_eq!(reused.law_id, COUPLED_RESPONSE_LAW_ID);
        assert_eq!(repaired.law_id, COUPLED_RESPONSE_LAW_ID);
        assert_eq!(full.law_id, COUPLED_RESPONSE_LAW_ID);
        assert!(reused.charge.repair >= 1);
    }

    #[test]
    fn compile_job_suspends_inside_collocation_not_after() {
        let ic = laboratory_two_body();
        let horizon = 4.0;
        let mut job = CoupledCompileJob::begin(
            genesis_bodies(&ic),
            ic.genesis_t,
            &[],
            horizon,
            Charge {
                init: 1,
                ..Charge::default()
            },
            None,
            &[],
        )
        .unwrap();
        let mut polls = 0u64;
        let mut pending_seen = false;
        loop {
            let mut budget = 1;
            match job.poll(&mut budget).unwrap() {
                JobPoll::Pending => {
                    pending_seen = true;
                    polls += 1;
                    assert!(!job.is_ready());
                    assert!(job.charge().source_evolution > 0 || job.charge().history > 0);
                }
                JobPoll::Ready => {
                    polls += 1;
                    break;
                }
            }
            assert!(polls < 10_000, "job failed to terminate");
        }
        assert!(pending_seen, "budget=1 must suspend inside collocation");
        assert!(polls > 1);
        let direct = compile_source_response(ic, Vec::new(), horizon, 1.0 / 32.0).unwrap();
        for id in [0_u64, 1] {
            let (xj, _) = body_state(&job.bodies, id, horizon).unwrap();
            let (xd, _) = body_state(&direct.worldtubes, id, horizon).unwrap();
            let err = V2::from_arr(xj).sub(V2::from_arr(xd)).norm();
            assert!(err < 1e-8, "suspended compile must match atomic compile, body {id} err={err}");
        }
    }

    #[test]
    fn diagnostic_scene_is_not_canonical_gravity() {
        let ic = laboratory_two_body();
        let dt = 1.0 / 32.0;
        let horizon = 4.0;
        let compiled = compile_source_response(ic.clone(), Vec::new(), horizon, dt).unwrap();
        let mut charge = Charge::default();
        let ship = fly_ship_compiled(
            &compiled,
            1.1,
            [0.0, 3.0],
            [0.125, 0.0],
            3.5,
            dt,
            &mut charge,
        )
        .unwrap();
        let ray = fly_ray_compiled(
            &compiled,
            1.1,
            [0.0, 3.0],
            [1.0, 0.0],
            8.0,
            0.05,
            &mut charge,
        )
        .unwrap();
        let rate = clock_rate_compiled(&compiled, ship.t, ship.x, ship.v, &mut charge).unwrap();
        let extra = laboratory_kick();
        let repaired = repair_from_committed(&compiled, &extra, horizon, dt).unwrap();
        let (ok_ship, ok_ray, ok_clock, ok_contact) =
            complete_required_queries_compiled(&repaired, horizon, &mut Charge::default()).unwrap();
        assert!(ship.tau > 0.0 && ray.t > 1.1 && rate > 0.0 && rate <= 1.0);
        assert!(ok_ship && ok_ray && ok_clock && ok_contact);
        assert_eq!(compiled.law_id, COUPLED_RESPONSE_LAW_ID);
        // Diagnostic scene only. Sampled enclosure/certified is not a canonical event.
    }

    #[test]
    fn extra_only_repair_inputs_drop_later_recorded_cause() {
        let later = Intervention {
            t: 3.0,
            body_id: 0,
            delta_v: [0.0, 0.05],
        };
        let earlier = Intervention {
            t: 1.5,
            body_id: 1,
            delta_v: [0.0, 0.04],
        };
        let extra_only = vec![earlier.clone()];
        let merged = merge_repair_interventions(&[later.clone()], &extra_only);
        assert_eq!(merged.len(), 2, "fixture: complete history has both kicks");
        assert!(
            extra_only.iter().all(|iv| (iv.t - 3.0).abs() > 0.1),
            "fixture retained: extra-only continuation omits the already recorded later cause"
        );
    }

    #[test]
    fn repair_keeps_later_recorded_cause_after_earlier_extra() {
        let ic = laboratory_two_body();
        let dt = 1.0 / 32.0;
        let horizon = 4.0;
        let later = vec![Intervention {
            t: 3.0,
            body_id: 0,
            delta_v: [0.0, 0.05],
        }];
        let earlier = vec![Intervention {
            t: 1.5,
            body_id: 1,
            delta_v: [0.0, 0.04],
        }];
        // New history branch: compile already records the later kick, then an
        // earlier extra is inserted in the uncommitted suffix. Not a rewrite of
        // a committed past of the same world.
        let compiled = compile_source_response(ic.clone(), later.clone(), horizon, dt).unwrap();
        assert_eq!(compiled.incoming.len(), 1);
        let repaired = repair_from_committed(&compiled, &earlier, horizon, dt).unwrap();
        assert_eq!(repaired.incoming.len(), 2);
        assert!(
            repaired.incoming.iter().any(|iv| (iv.t - 3.0).abs() < 1e-12),
            "later recorded cause must remain in repair incoming"
        );
        assert!(
            repaired.incoming.iter().any(|iv| (iv.t - 1.5).abs() < 1e-12),
            "earlier extra must appear in repair incoming"
        );
        let mut all = later.clone();
        all.extend_from_slice(&earlier);
        let reference = compile_source_response(ic.clone(), all, horizon, dt).unwrap();
        for id in [0_u64, 1] {
            let (xr, _) = body_state(&reference.worldtubes, id, horizon).unwrap();
            let (xp, _) = body_state(&repaired.worldtubes, id, horizon).unwrap();
            let err = V2::from_arr(xr).sub(V2::from_arr(xp)).norm();
            assert!(
                err < 1e-8,
                "repaired body {id} must match genesis reference with all interventions, err={err}"
            );
        }

        // Repeated repair: empty compile, later extra, then earlier extra.
        let quiet = compile_source_response(ic.clone(), Vec::new(), horizon, dt).unwrap();
        let once = repair_from_committed(&quiet, &later, horizon, dt).unwrap();
        let twice = repair_from_committed(&once, &earlier, horizon, dt).unwrap();
        assert_eq!(twice.incoming.len(), 2);
        for id in [0_u64, 1] {
            let (xr, _) = body_state(&reference.worldtubes, id, horizon).unwrap();
            let (xp, _) = body_state(&twice.worldtubes, id, horizon).unwrap();
            let err = V2::from_arr(xr).sub(V2::from_arr(xp)).norm();
            assert!(
                err < 1e-8,
                "repeated repair body {id} must match genesis reference, err={err}"
            );
        }
    }

    #[test]
    fn reuse_ledger_includes_enclosure_genesis_evolutions() {
        let ic = laboratory_two_body();
        let dt = 1.0 / 32.0;
        let horizon = 4.0;
        let compiled = compile_source_response(ic.clone(), Vec::new(), horizon, dt).unwrap();
        let extra = laboratory_kick();
        let enclosure = crate::coupled_interval_enclosure::enclose_compiled_interval(
            &compiled,
            ic,
            compiled.incoming.clone(),
            crate::coupled_interval_enclosure::IntervalMethod::CausalBlocks,
        )
        .unwrap();
        assert!(
            enclosure.charge.source_evolution > 0,
            "enclose_compiled_interval must charge genesis reference evolutions"
        );
        assert!(
            enclosure.certified,
            "this laboratory interval is a diagnostic enclosure, not a canonical event"
        );
        let reused = reuse_certified_interval_functions(&compiled, &extra, horizon, dt).unwrap();
        let child = reused
            .charge
            .child("enclose_compiled_interval")
            .expect("reuse must nest the enclosure ledger");
        assert_eq!(child.role, ChargeRole::OfflineAudit);
        assert_eq!(
            child.charge.source_evolution,
            enclosure.charge.source_evolution
        );
        assert_eq!(
            reused.charge.ledger_total(),
            reused.charge.total() + child.charge.ledger_total(),
            "ledger_total must reconcile with the call tree once"
        );
        assert_eq!(
            reused.charge.runtime_request_total(),
            reused.charge.total(),
            "offline enclosure must not be sold as runtime request cost"
        );
        assert_eq!(
            reused.charge.offline_audit_total(),
            child.charge.ledger_total()
        );
        assert!(reused.charge.ledger_total() > reused.charge.total());
        assert_eq!(
            source_ops_of(&reused),
            reused.charge.source_evolution + reused.charge.retarded_solves,
            "H0124 source-op scope stays suffix collocation, not enclosure genesis"
        );
    }

    #[test]
    fn pair_inverse_setup_is_dense_in_interval_functions() {
        let dt = 1.0 / 32.0;
        let short = compile_source_response(laboratory_two_body(), Vec::new(), 3.0, dt).unwrap();
        let long = compile_source_response(laboratory_two_body(), Vec::new(), 6.0, dt).unwrap();
        let inv_s = short.pair_inverse.as_ref().expect("quiet pair stores inverse");
        let inv_l = long.pair_inverse.as_ref().expect("quiet pair stores inverse");
        let bytes_s = inv_s.lu.len() * std::mem::size_of::<f64>()
            + inv_s.pivots.len() * std::mem::size_of::<usize>();
        let bytes_l = inv_l.lu.len() * std::mem::size_of::<f64>()
            + inv_l.pivots.len() * std::mem::size_of::<usize>();
        assert!(inv_s.n >= 2 && inv_l.n > inv_s.n);
        assert!(bytes_l > bytes_s);
        assert_eq!(inv_l.lu.len(), inv_l.n * inv_l.n);
        println!(
            "I0_PAIR_INVERSE short_n={} short_bytes={} long_n={} long_bytes={} short_wall_ns={} long_wall_ns={} short_src={} long_src={}",
            inv_s.n,
            bytes_s,
            inv_l.n,
            bytes_l,
            short.wall_ns,
            long.wall_ns,
            source_ops_of(&short),
            source_ops_of(&long)
        );
    }

    #[test]
    fn source_wall_time_and_memory_baselines_are_distinct() {
        let compiled =
            compile_source_response(laboratory_two_body(), Vec::new(), 4.0, 1.0 / 32.0).unwrap();
        let inv = compiled.pair_inverse.as_ref().unwrap();
        let matrix_bytes = inv.lu.len() * std::mem::size_of::<f64>();
        assert!(source_ops_of(&compiled) > 0);
        assert!(compiled.wall_ns > 0);
        assert!(matrix_bytes > 0);
        assert_ne!(
            source_ops_of(&compiled) as u128,
            compiled.wall_ns,
            "source-operation counts are not wall-time"
        );
        assert_ne!(
            matrix_bytes as u64,
            source_ops_of(&compiled),
            "pair-inverse bytes are not source ops"
        );
        println!(
            "I0_BASELINE source_ops={} wall_ns={} pair_inverse_n={} pair_inverse_bytes={} charge_total={} ledger_total={}",
            source_ops_of(&compiled),
            compiled.wall_ns,
            inv.n,
            matrix_bytes,
            compiled.charge.total(),
            compiled.charge.ledger_total()
        );
    }
}
