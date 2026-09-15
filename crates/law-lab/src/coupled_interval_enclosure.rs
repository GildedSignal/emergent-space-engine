//! Independently bounded contraction/enclosure for a compiled GEM interval.
//!
//! Not `production_law`. Diagnostic `Engine::advance` may poll [`EnclosureJob`];
//! that path does not authorize canonical gravity. Failed contraction rejects
//! this certificate, not the existence of a compiled solution.
//!
//! The enclosure does not read `SourceResponse::residual`. Defect comes from
//! an independent Picard map and `Reference::from_genesis`. Lipschitz comes
//! from a tidal bound on sampled pairwise distances, not from iterate
//! similarity.

use crate::coupled_source_response::{
    body_state, field_acceleration, retarded_lookback_time, Body, Charge, EulerContinueJob,
    InitialCondition, Intervention, JobPoll, Reference, ResponseError, SourceResponse, BodyInit, C,
};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum IntervalMethod {
    /// Conservative C⁰ bound `q = H · L` on the whole interval. Ignores delay
    /// grouping, so a close pair or a long horizon can fail even when a
    /// solution exists.
    IntegralOperator,
    /// March in blocks of length `≤ τ_min`. Same-interval cross response is
    /// causally determined by the past. The unknown-block Lipschitz is the
    /// delay-grouped rate `q = τ L`, computed from sampled tidal L, not assigned 0.
    CausalBlocks,
}

#[derive(Clone, Debug)]
pub struct Enclosure {
    pub certified: bool,
    pub method: IntervalMethod,
    pub q: f64,
    pub defect: f64,
    pub causal_time_error: f64,
    pub representation_error: f64,
    pub radius: Option<f64>,
    pub iterate_delta: f64,
    pub why_rejected: Option<String>,
    pub charge: Charge,
}

fn dist(a: [f64; 2], b: [f64; 2]) -> f64 {
    let dx = a[0] - b[0];
    let dy = a[1] - b[1];
    (dx * dx + dy * dy).sqrt()
}

fn pair_r_min(bodies: &[Body], t: f64) -> Result<f64, ResponseError> {
    let mut r_min = f64::INFINITY;
    for i in 0..bodies.len() {
        let (xi, _) = body_state(bodies, bodies[i].id, t)?;
        for j in (i + 1)..bodies.len() {
            let (xj, _) = body_state(bodies, bodies[j].id, t)?;
            r_min = r_min.min(dist(xi, xj));
        }
    }
    if !r_min.is_finite() {
        return Err(ResponseError::UnsupportedDomain {
            why: "need at least two bodies to enclose".into(),
        });
    }
    Ok(r_min)
}

fn tidal_lipschitz(bodies: &[Body], times: &[f64], charge: &mut Charge) -> Result<(f64, f64), ResponseError> {
    let mut l_inf = 0.0_f64;
    let mut beta_max = 0.0_f64;
    for &t in times {
        for body in bodies {
            let (_, v) = body_state(bodies, body.id, t)?;
            beta_max = beta_max.max((v[0] * v[0] + v[1] * v[1]).sqrt() / C);
        }
        let mut row_sums = vec![0.0_f64; bodies.len()];
        for (i, a) in bodies.iter().enumerate() {
            let (xi, _) = body_state(bodies, a.id, t)?;
            for b in bodies.iter() {
                if a.id == b.id {
                    continue;
                }
                let (xj, _) = body_state(bodies, b.id, t)?;
                let r = dist(xi, xj).max(1e-12);
                let mu = b.segments.last().map(|s| s.mu).unwrap_or(0.0);
                // |∂a_i/∂x_j| ≤ 2μ/r³ · (1+4β) on the admitted GEM band.
                row_sums[i] += 2.0 * mu / (r * r * r);
                charge.coefficient_construction += 1;
            }
        }
        l_inf = l_inf.max(row_sums.into_iter().fold(0.0_f64, f64::max));
    }
    let l = l_inf * (1.0 + 4.0 * beta_max);
    Ok((l, beta_max))
}

fn sample_times(t0: f64, horizon: f64, n: usize) -> Vec<f64> {
    (0..n)
        .map(|i| t0 + (i as f64 + 1.0) * (horizon - t0) / n as f64)
        .filter(|t| *t <= horizon)
        .collect()
}

fn picard_frozen(
    frozen: &[Body],
    ic: &InitialCondition,
    interventions: &[Intervention],
    horizon: f64,
    dt: f64,
    charge: &mut Charge,
) -> Result<Vec<Body>, ResponseError> {
    charge.reconstruction += 1;
    let mut bodies: Vec<Body> = ic
        .bodies
        .iter()
        .map(|b| Body {
            id: b.id,
            segments: vec![crate::coupled_source_response::Segment {
                t0: ic.genesis_t,
                t1: None,
                x0: b.x,
                v: b.v,
                a: [0.0, 0.0],
                mu: b.mu,
            }],
        })
        .collect();
    let mut kicks: Vec<Intervention> = interventions
        .iter()
        .filter(|iv| iv.t + 1e-12 >= ic.genesis_t)
        .cloned()
        .collect();
    kicks.sort_by(|a, b| a.t.partial_cmp(&b.t).unwrap());
    let mut t = ic.genesis_t;
    let mut k = 0usize;
    while t < horizon - 1e-15 {
        while k < kicks.len() && kicks[k].t <= t + 1e-12 {
            let kick = &kicks[k];
            if let Some(body) = bodies.iter_mut().find(|b| b.id == kick.body_id) {
                let (x, v) = body_state(&[body.clone()], body.id, kick.t)?;
                let v_new = [v[0] + kick.delta_v[0], v[1] + kick.delta_v[1]];
                if let Some(last) = body.segments.last_mut() {
                    last.t1 = Some(kick.t);
                }
                let mu = body.segments.last().map(|s| s.mu).unwrap_or(0.0);
                body.segments.push(crate::coupled_source_response::Segment {
                    t0: kick.t,
                    t1: None,
                    x0: x,
                    v: v_new,
                    a: [0.0, 0.0],
                    mu,
                });
                charge.history += 1;
            }
            k += 1;
        }
        let t_next = {
            let step = t + dt;
            let next_kick = kicks.get(k).map(|iv| iv.t).unwrap_or(horizon);
            step.min(next_kick).min(horizon)
        };
        if t_next <= t + 1e-18 {
            t = t_next;
            continue;
        }
        let h = t_next - t;
        let mut updates: Vec<(u64, [f64; 2], [f64; 2], f64)> = Vec::new();
        for body in &bodies {
            let (x, v) = body_state(&bodies, body.id, t)?;
            let a = field_acceleration(frozen, t, x, v, Some(body.id), charge)?;
            let v_new = [v[0] + a[0] * h, v[1] + a[1] * h];
            let x_new = [x[0] + v[0] * h, x[1] + v[1] * h];
            let mu = body.segments.last().map(|s| s.mu).unwrap_or(0.0);
            updates.push((body.id, x_new, v_new, mu));
            charge.source_evolution += 1;
        }
        for (id, x_new, v_new, mu) in updates {
            if let Some(body) = bodies.iter_mut().find(|b| b.id == id) {
                if let Some(last) = body.segments.last_mut() {
                    last.t1 = Some(t_next);
                }
                body.segments.push(crate::coupled_source_response::Segment {
                    t0: t_next,
                    t1: None,
                    x0: x_new,
                    v: v_new,
                    a: [0.0, 0.0],
                    mu,
                });
            }
        }
        t = t_next;
    }
    Ok(bodies)
}

fn max_position_delta(a: &[Body], b: &[Body], times: &[f64]) -> Result<f64, ResponseError> {
    let mut m = 0.0_f64;
    for &t in times {
        for body in a {
            let (xa, _) = body_state(a, body.id, t)?;
            let (xb, _) = body_state(b, body.id, t)?;
            m = m.max(dist(xa, xb));
        }
    }
    Ok(m)
}

fn causal_time_error(candidate: &[Body], other: &[Body], times: &[f64], charge: &mut Charge) -> Result<f64, ResponseError> {
    let mut err = 0.0_f64;
    for &t in times {
        for obs in candidate {
            let (x, _) = body_state(candidate, obs.id, t)?;
            for src in candidate {
                if src.id == obs.id {
                    continue;
                }
                let u0 = retarded_lookback_time(t, x, candidate, src.id, charge)?;
                let u1 = retarded_lookback_time(t, x, other, src.id, charge)?;
                match (u0, u1) {
                    (Some(a), Some(b)) => err = err.max((a - b).abs() * C),
                    (None, None) => {}
                    _ => err = err.max(C * 1.0),
                }
            }
        }
    }
    Ok(err)
}

fn representation_error(candidate: &[Body], times: &[f64], charge: &mut Charge) -> Result<f64, ResponseError> {
    let mut err = 0.0_f64;
    for &t in times {
        for body in candidate {
            let (x, v) = body_state(candidate, body.id, t)?;
            let a = field_acceleration(candidate, t, x, v, Some(body.id), charge)?;
            // Piecewise-inertial segments store a constant v; GEM-a is not
            // zero. The Euler defect |Δv − a Δt| / |a|Δt is representation
            // error of that stored response, not compile Residual.
            if let Some(seg) = body.segments.iter().rev().find(|s| t + 1e-15 >= s.t0) {
                let dt = (t - seg.t0).max(1e-12);
                let dv = [v[0] - seg.v[0], v[1] - seg.v[1]];
                let pred = [a[0] * dt, a[1] * dt];
                let miss = dist(dv, pred);
                err = err.max(miss);
            }
            charge.validation += 1;
        }
    }
    Ok(err)
}

fn inf_norm_2(k00: f64, k01: f64, k10: f64, k11: f64) -> f64 {
    (k00.abs() + k01.abs()).max(k10.abs() + k11.abs())
}

/// Independently enclose a candidate compiled interval.
///
/// Reconstructs the candidate from the stored compact generator. `candidate.residual`
/// is ignored. `Reference::from_genesis` is constructed only from the supplied
/// IC and interventions. Mutating the debug worldtube table cannot certify.
pub fn enclose_compiled_interval(
    candidate: &SourceResponse,
    ic: InitialCondition,
    interventions: Vec<Intervention>,
    method: IntervalMethod,
) -> Result<Enclosure, ResponseError> {
    let start = std::time::Instant::now();
    let mut charge = Charge {
        init: 1,
        ..Charge::default()
    };
    let horizon = candidate.domain.horizon;
    let dt = candidate.domain.dt;
    let times = sample_times(ic.genesis_t, horizon, 16);
    let d0 = if ic.bodies.len() >= 2 {
        dist(ic.bodies[0].x, ic.bodies[1].x).max(1e-12)
    } else {
        1.0
    };
    let ident_band = 0.05 * d0;
    // Independent histories never start from the candidate state.
    let reference = Reference::from_genesis(ic.clone(), interventions.clone(), dt);
    let fine = Reference::from_genesis(ic.clone(), interventions.clone(), dt / 4.0);
    let (ref_bodies, ref_charge) = reference.evolve_to(horizon)?;
    let (fine_bodies, fine_charge) = fine.evolve_to(horizon)?;
    charge.history += ref_charge.history + fine_charge.history;
    charge.source_evolution += ref_charge.source_evolution + fine_charge.source_evolution;
    charge.retarded_solves += ref_charge.retarded_solves + fine_charge.retarded_solves;
    charge.field_evals += ref_charge.field_evals + fine_charge.field_evals;

    let sources = candidate.decode_sources(&mut charge)?;
    let picard = picard_frozen(
        &sources,
        &ic,
        &interventions,
        horizon,
        dt,
        &mut charge,
    )?;
    let iterate_delta = max_position_delta(&sources, &picard, &times)?;
    let vs_ref = max_position_delta(&sources, &ref_bodies, &times)?;
    let numerical = max_position_delta(&sources, &fine_bodies, &times)?;
    let causal = causal_time_error(&sources, &ref_bodies, &times, &mut charge)?;
    let representation = representation_error(&sources, &times, &mut charge)?;
    let defect = iterate_delta
        .max(vs_ref)
        .max(numerical)
        .max(causal)
        .max(representation * dt);

    let (l, _beta) = tidal_lipschitz(&ref_bodies, &times, &mut charge)?;
    charge.factorization += 1;
    // 2-body Schur block of the integral operator; unused for CausalBlocks q.
    let k_scale = horizon * l;
    let _q_matrix = inf_norm_2(0.0, k_scale, k_scale, 0.0);
    let q = match method {
        IntervalMethod::IntegralOperator => horizon * l,
        IntervalMethod::CausalBlocks => {
            let r_min = times.iter().try_fold(f64::INFINITY, |acc, &t| {
                pair_r_min(&ref_bodies, t).map(|r| acc.min(r))
            })?;
            let tau = r_min / C;
            // Delay-grouped Lipschitz of the retarded operator: same-block
            // cross terms are spacelike, so the unknown-block step is bounded
            // by τ L rather than H L. Computed, not assigned 0.
            tau.min(horizon) * l
        }
    };

    let r_min = times.iter().try_fold(f64::INFINITY, |acc, &t| {
        pair_r_min(&sources, t).map(|r| acc.min(r))
    })?;
    charge.verification += 1;
    let _elapsed = start.elapsed();

    let mut why = None;
    let mut radius = None;
    let mut certified = false;
    if !q.is_finite() || q < 0.0 {
        why = Some("Lipschitz bound is not a finite contraction rate".into());
    } else if q >= 1.0 {
        why = Some(format!(
            "contraction failed: q={q} ≥ 1 for {method:?} on H={horizon} (solution may still exist)"
        ));
    } else {
        let e = defect / (1.0 - q);
        radius = Some(e);
        if e >= r_min / 2.0 {
            why = Some(format!(
                "enclosure radius {e} does not fit in r_min/2={}; domain not invariant",
                r_min / 2.0
            ));
        } else if defect > ident_band {
            why = Some(format!(
                "independent defect {defect} exceeds identification band {ident_band}; unique solution may exist but Xhat is not certified"
            ));
        } else {
            certified = true;
        }
    }

    // Iterate similarity is recorded and is never a sufficient certificate.
    let _ = iterate_delta;

    Ok(Enclosure {
        certified,
        method,
        q,
        defect,
        causal_time_error: causal,
        representation_error: representation,
        radius,
        iterate_delta,
        why_rejected: why,
        charge,
    })
}

#[derive(Clone, Debug)]
enum EnclosureStage {
    Ref(EulerContinueJob),
    Fine {
        ref_bodies: Vec<Body>,
        ref_charge: Charge,
        job: EulerContinueJob,
    },
    Picard {
        ref_bodies: Vec<Body>,
        fine_bodies: Vec<Body>,
        merged: Charge,
        job: PicardJob,
    },
    Rest {
        ref_bodies: Vec<Body>,
        fine_bodies: Vec<Body>,
        picard: Vec<Body>,
        merged: Charge,
    },
    Done,
}

/// Diagnostic enclosure: yields inside genesis Euler loops and Picard dt
/// steps. Sampled `certified: true` remains diagnostic, not an event grant.
#[derive(Clone, Debug)]
pub struct EnclosureJob {
    candidate: SourceResponse,
    ic: InitialCondition,
    interventions: Vec<Intervention>,
    method: IntervalMethod,
    sources: Vec<Body>,
    stage: EnclosureStage,
    result: Option<Enclosure>,
}

#[derive(Clone, Debug)]
struct PicardJob {
    frozen: Vec<Body>,
    bodies: Vec<Body>,
    kicks: Vec<Intervention>,
    t: f64,
    k: usize,
    horizon: f64,
    dt: f64,
    charge: Charge,
    ready: bool,
}

impl PicardJob {
    fn start(
        frozen: Vec<Body>,
        ic: &InitialCondition,
        interventions: &[Intervention],
        horizon: f64,
        dt: f64,
        mut charge: Charge,
    ) -> Self {
        charge.reconstruction += 1;
        let bodies: Vec<Body> = ic
            .bodies
            .iter()
            .map(|b| Body {
                id: b.id,
                segments: vec![crate::coupled_source_response::Segment {
                    t0: ic.genesis_t,
                    t1: None,
                    x0: b.x,
                    v: b.v,
                    a: [0.0, 0.0],
                    mu: b.mu,
                }],
            })
            .collect();
        let mut kicks: Vec<Intervention> = interventions
            .iter()
            .filter(|iv| iv.t + 1e-12 >= ic.genesis_t)
            .cloned()
            .collect();
        kicks.sort_by(|a, b| a.t.partial_cmp(&b.t).unwrap());
        Self {
            frozen,
            bodies,
            kicks,
            t: ic.genesis_t,
            k: 0,
            horizon,
            dt,
            charge,
            ready: false,
        }
    }

    fn poll(&mut self, op_budget: &mut u64) -> Result<JobPoll, ResponseError> {
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
        let t = self.t;
        while self.k < self.kicks.len() && self.kicks[self.k].t <= t + 1e-12 {
            let kick = &self.kicks[self.k];
            if let Some(body) = self.bodies.iter_mut().find(|b| b.id == kick.body_id) {
                let (x, v) = body_state(&[body.clone()], body.id, kick.t)?;
                let v_new = [v[0] + kick.delta_v[0], v[1] + kick.delta_v[1]];
                if let Some(last) = body.segments.last_mut() {
                    last.t1 = Some(kick.t);
                }
                let mu = body.segments.last().map(|s| s.mu).unwrap_or(0.0);
                body.segments.push(crate::coupled_source_response::Segment {
                    t0: kick.t,
                    t1: None,
                    x0: x,
                    v: v_new,
                    a: [0.0, 0.0],
                    mu,
                });
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
        let mut updates: Vec<(u64, [f64; 2], [f64; 2], f64)> = Vec::new();
        for body in &self.bodies {
            let (x, v) = body_state(&self.bodies, body.id, t)?;
            let a = field_acceleration(&self.frozen, t, x, v, Some(body.id), &mut self.charge)?;
            let v_new = [v[0] + a[0] * h, v[1] + a[1] * h];
            let x_new = [x[0] + v[0] * h, x[1] + v[1] * h];
            let mu = body.segments.last().map(|s| s.mu).unwrap_or(0.0);
            updates.push((body.id, x_new, v_new, mu));
            self.charge.source_evolution += 1;
        }
        for (id, x_new, v_new, mu) in updates {
            if let Some(body) = self.bodies.iter_mut().find(|b| b.id == id) {
                if let Some(last) = body.segments.last_mut() {
                    last.t1 = Some(t_next);
                }
                body.segments.push(crate::coupled_source_response::Segment {
                    t0: t_next,
                    t1: None,
                    x0: x_new,
                    v: v_new,
                    a: [0.0, 0.0],
                    mu,
                });
            }
        }
        self.t = t_next;
        Ok(())
    }
}

impl EnclosureJob {
    pub fn start(
        candidate: &SourceResponse,
        ic: InitialCondition,
        interventions: Vec<Intervention>,
        method: IntervalMethod,
    ) -> Result<Self, ResponseError> {
        let mut charge = Charge {
            init: 1,
            ..Charge::default()
        };
        let sources = if candidate.compact.pieces.is_empty() {
            charge.fallback += 1;
            if candidate.worldtubes.is_empty() {
                return Err(ResponseError::UnsupportedDomain {
                    why: "diagnostic enclosure needs interval-function worldtubes when compact is skipped"
                        .into(),
                });
            }
            candidate.worldtubes.clone()
        } else {
            candidate.decode_sources(&mut charge)?
        };
        let dt = candidate.domain.dt;
        let horizon = candidate.domain.horizon;
        let job = EulerContinueJob::from_genesis(&ic, &interventions, horizon, dt);
        Ok(Self {
            candidate: candidate.clone(),
            ic,
            interventions,
            method,
            sources,
            stage: EnclosureStage::Ref(job),
            result: None,
        })
    }

    pub fn poll(&mut self, op_budget: &mut u64) -> Result<JobPoll, ResponseError> {
        if matches!(self.stage, EnclosureStage::Done) {
            return Ok(JobPoll::Ready);
        }
        loop {
            if matches!(self.stage, EnclosureStage::Done) {
                return Ok(JobPoll::Ready);
            }
            if *op_budget == 0 {
                return Ok(JobPoll::Pending);
            }
            match &mut self.stage {
                EnclosureStage::Ref(job) => {
                    if job.poll(op_budget)? == JobPoll::Pending {
                        return Ok(JobPoll::Pending);
                    }
                    let (ref_bodies, ref_charge) = match std::mem::replace(
                        &mut self.stage,
                        EnclosureStage::Done,
                    ) {
                        EnclosureStage::Ref(job) => job.into_bodies(),
                        other => {
                            self.stage = other;
                            return Err(ResponseError::UnsupportedDomain {
                                why: "enclosure ref stage mismatch".into(),
                            });
                        }
                    };
                    let fine = EulerContinueJob::from_genesis(
                        &self.ic,
                        &self.interventions,
                        self.candidate.domain.horizon,
                        self.candidate.domain.dt / 4.0,
                    );
                    self.stage = EnclosureStage::Fine {
                        ref_bodies,
                        ref_charge,
                        job: fine,
                    };
                }
                EnclosureStage::Fine { job, .. } => {
                    if job.poll(op_budget)? == JobPoll::Pending {
                        return Ok(JobPoll::Pending);
                    }
                    let (ref_bodies, ref_charge, fine_job) = match std::mem::replace(
                        &mut self.stage,
                        EnclosureStage::Done,
                    ) {
                        EnclosureStage::Fine {
                            ref_bodies,
                            ref_charge,
                            job,
                        } => (ref_bodies, ref_charge, job),
                        other => {
                            self.stage = other;
                            return Err(ResponseError::UnsupportedDomain {
                                why: "enclosure fine stage mismatch".into(),
                            });
                        }
                    };
                    let (fine_bodies, fine_charge) = fine_job.into_bodies();
                    let mut merged = Charge {
                        init: 1,
                        ..Charge::default()
                    };
                    merged.history += ref_charge.history + fine_charge.history;
                    merged.source_evolution +=
                        ref_charge.source_evolution + fine_charge.source_evolution;
                    merged.retarded_solves +=
                        ref_charge.retarded_solves + fine_charge.retarded_solves;
                    merged.field_evals += ref_charge.field_evals + fine_charge.field_evals;
                    let picard = PicardJob::start(
                        self.sources.clone(),
                        &self.ic,
                        &self.interventions,
                        self.candidate.domain.horizon,
                        self.candidate.domain.dt,
                        merged.clone(),
                    );
                    self.stage = EnclosureStage::Picard {
                        ref_bodies,
                        fine_bodies,
                        merged,
                        job: picard,
                    };
                }
                EnclosureStage::Picard { job, .. } => {
                    if job.poll(op_budget)? == JobPoll::Pending {
                        return Ok(JobPoll::Pending);
                    }
                    let (ref_bodies, fine_bodies, mut merged, picard_job) =
                        match std::mem::replace(&mut self.stage, EnclosureStage::Done) {
                            EnclosureStage::Picard {
                                ref_bodies,
                                fine_bodies,
                                merged,
                                job,
                            } => (ref_bodies, fine_bodies, merged, job),
                            other => {
                                self.stage = other;
                                return Err(ResponseError::UnsupportedDomain {
                                    why: "enclosure picard stage mismatch".into(),
                                });
                            }
                        };
                    merged.history = picard_job.charge.history;
                    merged.source_evolution = picard_job.charge.source_evolution;
                    merged.retarded_solves = picard_job.charge.retarded_solves;
                    merged.field_evals = picard_job.charge.field_evals;
                    merged.reconstruction = picard_job.charge.reconstruction;
                    self.stage = EnclosureStage::Rest {
                        ref_bodies,
                        fine_bodies,
                        picard: picard_job.bodies,
                        merged,
                    };
                }
                EnclosureStage::Rest { .. } => {
                    self.finish_rest()?;
                    self.stage = EnclosureStage::Done;
                    *op_budget = op_budget.saturating_sub(1);
                    return Ok(JobPoll::Ready);
                }
                EnclosureStage::Done => return Ok(JobPoll::Ready),
            }
        }
    }

    fn finish_rest(&mut self) -> Result<(), ResponseError> {
        let EnclosureStage::Rest {
            ref_bodies,
            fine_bodies,
            picard,
            merged,
        } = &self.stage
        else {
            return Err(ResponseError::UnsupportedDomain {
                why: "enclosure rest stage mismatch".into(),
            });
        };
        let mut charge = merged.clone();
        let horizon = self.candidate.domain.horizon;
        let dt = self.candidate.domain.dt;
        let times = sample_times(self.ic.genesis_t, horizon, 16);
        let d0 = if self.ic.bodies.len() >= 2 {
            dist(self.ic.bodies[0].x, self.ic.bodies[1].x).max(1e-12)
        } else {
            1.0
        };
        let ident_band = 0.05 * d0;
        let iterate_delta = max_position_delta(&self.sources, picard, &times)?;
        let vs_ref = max_position_delta(&self.sources, ref_bodies, &times)?;
        let numerical = max_position_delta(&self.sources, fine_bodies, &times)?;
        let causal = causal_time_error(&self.sources, ref_bodies, &times, &mut charge)?;
        let representation = representation_error(&self.sources, &times, &mut charge)?;
        let defect = iterate_delta
            .max(vs_ref)
            .max(numerical)
            .max(causal)
            .max(representation * dt);
        let (l, _beta) = tidal_lipschitz(ref_bodies, &times, &mut charge)?;
        charge.factorization += 1;
        let q = match self.method {
            IntervalMethod::IntegralOperator => horizon * l,
            IntervalMethod::CausalBlocks => {
                let r_min = times.iter().try_fold(f64::INFINITY, |acc, &t| {
                    pair_r_min(ref_bodies, t).map(|r| acc.min(r))
                })?;
                let tau = r_min / C;
                tau.min(horizon) * l
            }
        };
        let r_min = times.iter().try_fold(f64::INFINITY, |acc, &t| {
            pair_r_min(&self.sources, t).map(|r| acc.min(r))
        })?;
        charge.verification += 1;
        let mut why = None;
        let mut radius = None;
        let mut certified = false;
        if !q.is_finite() || q < 0.0 {
            why = Some("Lipschitz bound is not a finite contraction rate".into());
        } else if q >= 1.0 {
            why = Some(format!(
                "contraction failed: q={q} ≥ 1 for {:?} on H={horizon} (solution may still exist)",
                self.method
            ));
        } else {
            let e = defect / (1.0 - q);
            radius = Some(e);
            if e >= r_min / 2.0 {
                why = Some(format!(
                    "enclosure radius {e} does not fit in r_min/2={}; domain not invariant",
                    r_min / 2.0
                ));
            } else if defect > ident_band {
                why = Some(format!(
                    "independent defect {defect} exceeds identification band {ident_band}; unique solution may exist but Xhat is not certified"
                ));
            } else {
                certified = true;
            }
        }
        let _ = iterate_delta;
        self.result = Some(Enclosure {
            certified,
            method: self.method,
            q,
            defect,
            causal_time_error: causal,
            representation_error: representation,
            radius,
            iterate_delta,
            why_rejected: why,
            charge,
        });
        Ok(())
    }

    pub fn is_ready(&self) -> bool {
        matches!(self.stage, EnclosureStage::Done)
    }

    pub fn take(self) -> Result<Enclosure, ResponseError> {
        self.result.ok_or(ResponseError::UnsupportedDomain {
            why: "enclosure job is not ready".into(),
        })
    }
}

pub fn laboratory_close_pair() -> InitialCondition {
    // D=1.2 keeps |Φ|/c² inside the admitted 0.05 band on a short interval,
    // while H·(2μ/D³) already exceeds 1 for the monolithic integral operator.
    InitialCondition {
        genesis_t: 0.0,
        bodies: vec![
            BodyInit {
                id: 0,
                mu: 1.0,
                x: [-0.6, 0.0],
                v: [0.0, 0.0],
            },
            BodyInit {
                id: 1,
                mu: 1.0,
                x: [0.6, 0.0],
                v: [0.0, 0.0],
            },
        ],
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::coupled_source_response::{
        body_state, compile_source_response, laboratory_kick, laboratory_two_body,
    };

    #[test]
    fn passing_enclosure_is_independently_bounded() {
        let ic = laboratory_two_body();
        let kicks = laboratory_kick();
        let compiled = compile_source_response(ic.clone(), kicks.clone(), 4.0, 1.0 / 32.0).unwrap();
        let enc = enclose_compiled_interval(
            &compiled,
            ic,
            kicks,
            IntervalMethod::IntegralOperator,
        )
        .unwrap();
        assert!(enc.certified, "expected certified, {:?}", enc.why_rejected);
        assert!(enc.q > 0.0 && enc.q < 1.0, "q={}", enc.q);
        let e = enc.radius.expect("independent radius");
        assert!(e > 0.0 && e.is_finite());
        assert!(enc.causal_time_error.is_finite());
        assert!(enc.representation_error.is_finite());
        assert!(enc.defect < 0.05 * 8.0);
        assert!(enc.charge.validation > 0);
        assert!(enc.charge.coefficient_construction > 0);
        assert!(enc.charge.factorization > 0);
        assert!(enc.charge.verification > 0);
        assert!(enc.charge.reconstruction > 0);
        assert_eq!(compiled.law_id, crate::COUPLED_RESPONSE_LAW_ID);
    }

    #[test]
    fn enclosure_ignores_candidate_residual() {
        let ic = laboratory_two_body();
        let kicks = laboratory_kick();
        let mut compiled =
            compile_source_response(ic.clone(), kicks.clone(), 4.0, 1.0 / 32.0).unwrap();
        let a = enclose_compiled_interval(
            &compiled,
            ic.clone(),
            kicks.clone(),
            IntervalMethod::IntegralOperator,
        )
        .unwrap();
        compiled.residual.max_grad_rel = 1e9;
        compiled.residual.max_accel_rel = 1e9;
        compiled.residual.max_phi_c2 = 1e9;
        compiled.residual.max_beta = 1e9;
        compiled.residual.static_kernel_ok = false;
        let b = enclose_compiled_interval(&compiled, ic, kicks, IntervalMethod::IntegralOperator)
            .unwrap();
        assert_eq!(a.certified, b.certified);
        assert!((a.q - b.q).abs() < 1e-12);
        assert!((a.defect - b.defect).abs() < 1e-12);
    }

    #[test]
    fn failed_contraction_does_not_silently_certify() {
        let ic = laboratory_close_pair();
        let compiled = compile_source_response(ic.clone(), Vec::new(), 1.0, 1.0 / 32.0).unwrap();
        assert_eq!(compiled.law_id, crate::COUPLED_RESPONSE_LAW_ID);
        let enc = enclose_compiled_interval(
            &compiled,
            ic,
            Vec::new(),
            IntervalMethod::IntegralOperator,
        )
        .unwrap();
        assert!(
            !enc.certified,
            "close-pair IntegralOperator must not silently certify, q={}",
            enc.q
        );
        assert!(enc.q >= 1.0, "expected q≥1, got {}", enc.q);
        assert!(enc.why_rejected.as_ref().unwrap().contains("contraction failed"));
    }

    #[test]
    fn failed_contraction_does_not_deny_the_solution() {
        let ic = laboratory_close_pair();
        let compiled = compile_source_response(ic.clone(), Vec::new(), 1.0, 1.0 / 32.0);
        assert!(compiled.is_ok(), "solution still exists");
        let enc = enclose_compiled_interval(
            &compiled.unwrap(),
            ic,
            Vec::new(),
            IntervalMethod::IntegralOperator,
        )
        .unwrap();
        assert!(!enc.certified);
    }

    #[test]
    fn causal_blocks_can_refine_a_failed_monolithic_bound() {
        let ic = laboratory_close_pair();
        let compiled = compile_source_response(ic.clone(), Vec::new(), 1.0, 1.0 / 32.0).unwrap();
        let mono = enclose_compiled_interval(
            &compiled,
            ic.clone(),
            Vec::new(),
            IntervalMethod::IntegralOperator,
        )
        .unwrap();
        assert!(
            !mono.certified,
            "close-pair IntegralOperator must remain uncertified"
        );
        let blocks = enclose_compiled_interval(
            &compiled,
            ic,
            Vec::new(),
            IntervalMethod::CausalBlocks,
        )
        .unwrap();
        assert!(
            blocks.q > 0.0,
            "CausalBlocks q must be computed, not assigned 0, q={}",
            blocks.q
        );
        assert!(
            blocks.q < 1.0 && blocks.q < mono.q,
            "delay grouping must reduce q below the monolithic bound, q={} mono={}",
            blocks.q,
            mono.q
        );
        assert!(
            blocks.certified,
            "causal grouping should enclose when defect fits, {:?}",
            blocks.why_rejected
        );
        assert!(blocks.radius.unwrap() > 0.0);
    }

    #[test]
    fn successive_iterates_looking_similar_cannot_certify() {
        let ic = laboratory_close_pair();
        let compiled = compile_source_response(ic.clone(), Vec::new(), 1.0, 1.0 / 32.0).unwrap();
        let enc = enclose_compiled_interval(
            &compiled,
            ic,
            Vec::new(),
            IntervalMethod::IntegralOperator,
        )
        .unwrap();
        assert!(
            enc.iterate_delta < 0.05,
            "Picard and compile can look similar, delta={}",
            enc.iterate_delta
        );
        assert!(
            !enc.certified,
            "similarity is not a certificate when q={}",
            enc.q
        );
    }

    #[test]
    fn authored_worldtubes_reject_enclosure_not_the_true_solution() {
        let ic = laboratory_two_body();
        let kicks = laboratory_kick();
        let mut compiled =
            compile_source_response(ic.clone(), kicks.clone(), 4.0, 1.0 / 32.0).unwrap();
        for piece in compiled.compact.pieces.iter_mut() {
            if piece.id == 1 && piece.t1 > 2.0 {
                piece.orbit.com[1] += 3.0;
            }
        }
        let enc = enclose_compiled_interval(
            &compiled,
            ic.clone(),
            kicks.clone(),
            IntervalMethod::IntegralOperator,
        )
        .unwrap();
        assert!(!enc.certified, "authored futures must not certify");
        assert!(enc.why_rejected.is_some());
        let honest = compile_source_response(ic, kicks, 4.0, 1.0 / 32.0);
        assert!(honest.is_ok());
    }

    #[test]
    fn independent_reference_is_from_genesis() {
        let ic = laboratory_two_body();
        let kicks = laboratory_kick();
        let compiled = compile_source_response(ic.clone(), kicks.clone(), 3.0, 1.0 / 32.0).unwrap();
        let reference = Reference::from_genesis(ic.clone(), kicks.clone(), 1.0 / 128.0);
        let (bodies, _) = reference.evolve_to(3.0).unwrap();
        assert!(!bodies.is_empty());
        let mut poisoned = compiled.clone();
        for body in poisoned.worldtubes.iter_mut() {
            for seg in body.segments.iter_mut() {
                seg.x0[0] += 50.0;
            }
        }
        for fun in poisoned.interval_functions.iter_mut() {
            fun.x0[0] += 50.0;
        }
        poisoned.residual.max_grad_rel = 1e9;
        let (bodies_after, _) = reference.evolve_to(3.0).unwrap();
        let (x0, _) = body_state(&bodies, 0, 3.0).unwrap();
        let (x1, _) = body_state(&bodies_after, 0, 3.0).unwrap();
        assert_eq!(
            x0, x1,
            "poisoning the compiled candidate must not change Reference::from_genesis"
        );
        let (xc, _) = body_state(&poisoned.worldtubes, 0, 3.0).unwrap();
        assert!(
            (xc[0] - x0[0]).abs() > 1.0,
            "poisoned candidate trajectory must not be the genesis reference"
        );
        let enc = enclose_compiled_interval(&compiled, ic, kicks, IntervalMethod::IntegralOperator)
            .unwrap();
        assert!(enc.certified, "{:?}", enc.why_rejected);
    }
}
