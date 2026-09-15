//! Diagnostic coupled-compiler adapter.
//!
//! Polls collocation, residual validation, pair-inverse factorization, enclosure
//! and repair jobs with [`WorkBudget`] from [`crate::runtime::Engine::advance`].
//! Does not report canonical gravity acceptance. Compact Chebyshev remains a
//! skipped sidecar on this path; consumers bind to interval functions.

use crate::{
    math::{r, Vec2},
    policy::{evaluate_policy, Guard, PolicyAction, PolicyProgram, PolicyRule, ReceivedKnowledge},
    propagator::Inertial,
    runtime::{
        Body, Engine, EngineError, Observation, WorkBudget,
    },
};
use emergent_law_lab::{
    coupled_interval_enclosure::{Enclosure, EnclosureJob, IntervalMethod},
    coupled_source_response::{
        body_state_compiled, clock_rate_compiled, complete_required_queries_compiled,
        contact_closest_compiled, fly_ray_compiled, fly_ship, fly_ship_compiled,
        laboratory_two_body, Charge, CoupledCompileJob,
        InitialCondition, Intervention, JobPoll, PairInverseJob, ResidualJob, ResponseError,
        ShipState, SourceResponse, RayState,
    },
};
use std::collections::BTreeSet;

/// Explicit non-acceptance. Increment 1 of I1 is diagnostic only.
pub const CANONICAL_GRAVITY_ACCEPTANCE: &str = "diagnostic-only";

pub const EMITTER_ID: u64 = 10;
pub const SHIP_ID: u64 = 11;
pub const BEACON_ID: u64 = 12;

pub fn poll_coupled_job(
    job: &mut CoupledCompileJob,
    budget: &mut WorkBudget,
) -> Result<JobPoll, ResponseError> {
    let mut ops = budget.operations as u64;
    let status = job.poll(&mut ops)?;
    budget.operations = ops as usize;
    Ok(status)
}

fn poll_u64(budget: &mut WorkBudget, f: impl FnOnce(&mut u64) -> Result<JobPoll, ResponseError>) -> Result<JobPoll, ResponseError> {
    let mut ops = budget.operations as u64;
    let status = f(&mut ops)?;
    budget.operations = ops as usize;
    Ok(status)
}

#[derive(Clone, Debug)]
enum Pipeline {
    Collocate {
        genesis: InitialCondition,
        incoming: Vec<Intervention>,
        dt: f64,
        job: CoupledCompileJob,
    },
    Residual(ResidualJob),
    PairInverse {
        compiled: SourceResponse,
        job: PairInverseJob,
    },
    Enclose {
        compiled: SourceResponse,
        job: EnclosureJob,
    },
    RepairCollocate {
        compiled: SourceResponse,
        extra: Vec<Intervention>,
        dt: f64,
        job: CoupledCompileJob,
    },
    Ready,
}

#[derive(Clone, Debug)]
pub struct BoundConsumers {
    pub ship: ShipState,
    pub ray: RayState,
    pub clock: f64,
    pub contact_t: f64,
    pub contact_d: f64,
    pub source0: ([f64; 2], [f64; 2]),
    pub source1: ([f64; 2], [f64; 2]),
    pub chord_ship_tau: f64,
}

#[derive(Clone, Debug)]
pub struct CoupledDiagnostic {
    pipeline: Pipeline,
    pub compiled: Option<SourceResponse>,
    pub enclosure: Option<Enclosure>,
    pub consumers: Option<BoundConsumers>,
    pub pending_required: Vec<String>,
    pub horizon: f64,
    pub dt: f64,
    pub max_uninterrupted_ns: u128,
    pub last_poll_ns: u128,
}

impl CoupledDiagnostic {
    pub fn from_ic(
        genesis: InitialCondition,
        horizon: f64,
        dt: f64,
    ) -> Result<Self, ResponseError> {
        let job = CoupledCompileJob::from_genesis(&genesis, &[], horizon)?;
        Ok(Self {
            pipeline: Pipeline::Collocate {
                genesis,
                incoming: Vec::new(),
                dt,
                job,
            },
            compiled: None,
            enclosure: None,
            consumers: None,
            pending_required: Vec::new(),
            horizon,
            dt,
            max_uninterrupted_ns: 0,
            last_poll_ns: 0,
        })
    }

    pub fn laboratory() -> Result<Self, ResponseError> {
        Self::from_ic(laboratory_two_body(), 3.0, 1.0 / 32.0)
    }

    pub fn is_ready(&self) -> bool {
        matches!(self.pipeline, Pipeline::Ready) && self.compiled.is_some()
    }

    pub fn pending_jobs(&self) -> usize {
        if self.is_ready() {
            self.pending_required.len()
        } else {
            1 + self.pending_required.len()
        }
    }

    pub fn stage_name(&self) -> &'static str {
        match self.pipeline {
            Pipeline::Collocate { .. } => "collocate",
            Pipeline::Residual(_) => "residual",
            Pipeline::PairInverse { .. } => "pair-inverse",
            Pipeline::Enclose { .. } => "enclose",
            Pipeline::RepairCollocate { .. } => "repair",
            Pipeline::Ready => "ready",
        }
    }

    pub fn poll(&mut self, budget: &mut WorkBudget) -> Result<JobPoll, ResponseError> {
        let start = std::time::Instant::now();
        let status = self.poll_inner(budget)?;
        let ns = start.elapsed().as_nanos();
        self.last_poll_ns = ns;
        self.max_uninterrupted_ns = self.max_uninterrupted_ns.max(ns);
        Ok(status)
    }

    fn poll_inner(&mut self, budget: &mut WorkBudget) -> Result<JobPoll, ResponseError> {
        if matches!(self.pipeline, Pipeline::Ready) {
            return Ok(JobPoll::Ready);
        }
        loop {
            if budget.operations == 0 {
                return Ok(JobPoll::Pending);
            }
            match &mut self.pipeline {
                Pipeline::Collocate { job, .. } => {
                    if poll_coupled_job(job, budget)? == JobPoll::Pending {
                        return Ok(JobPoll::Pending);
                    }
                    let Pipeline::Collocate {
                        genesis,
                        incoming,
                        dt,
                        job,
                    } = std::mem::replace(&mut self.pipeline, Pipeline::Ready)
                    else {
                        unreachable!("collocate");
                    };
                    let (raw, functions, blocks, q, tau, charge, horizon) = job.collocation_parts()?;
                    self.pipeline = Pipeline::Residual(ResidualJob::start(
                        genesis, incoming, raw, functions, horizon, dt, blocks, q, tau, charge,
                    ));
                }
                Pipeline::Residual(job) => {
                    if poll_u64(budget, |ops| job.poll(ops))? == JobPoll::Pending {
                        return Ok(JobPoll::Pending);
                    }
                    let Pipeline::Residual(job) =
                        std::mem::replace(&mut self.pipeline, Pipeline::Ready)
                    else {
                        unreachable!("residual");
                    };
                    let compiled = job.take()?;
                    let quiet_pair = compiled.genesis.bodies.len() == 2
                        && compiled.incoming.is_empty()
                        && compiled.interval_functions.len() >= 2;
                    if quiet_pair {
                        let inv = PairInverseJob::start(&compiled)?;
                        self.pipeline = Pipeline::PairInverse { compiled, job: inv };
                    } else {
                        let enc = EnclosureJob::start(
                            &compiled,
                            compiled.genesis.clone(),
                            compiled.incoming.clone(),
                            IntervalMethod::CausalBlocks,
                        )?;
                        self.pipeline = Pipeline::Enclose { compiled, job: enc };
                    }
                }
                Pipeline::PairInverse { job, .. } => {
                    if poll_u64(budget, |ops| job.poll(ops))? == JobPoll::Pending {
                        return Ok(JobPoll::Pending);
                    }
                    let Pipeline::PairInverse { mut compiled, job } =
                        std::mem::replace(&mut self.pipeline, Pipeline::Ready)
                    else {
                        unreachable!("pair-inverse");
                    };
                    let (inv, inv_charge) = job.take()?;
                    compiled.pair_inverse = Some(inv);
                    compiled.charge.coefficient_construction += inv_charge.coefficient_construction;
                    compiled.charge.factorization += inv_charge.factorization;
                    compiled.charge.verification += inv_charge.verification;
                    let enc = EnclosureJob::start(
                        &compiled,
                        compiled.genesis.clone(),
                        compiled.incoming.clone(),
                        IntervalMethod::CausalBlocks,
                    )?;
                    self.pipeline = Pipeline::Enclose { compiled, job: enc };
                }
                Pipeline::Enclose { job, .. } => {
                    if poll_u64(budget, |ops| job.poll(ops))? == JobPoll::Pending {
                        return Ok(JobPoll::Pending);
                    }
                    let Pipeline::Enclose { compiled, job } =
                        std::mem::replace(&mut self.pipeline, Pipeline::Ready)
                    else {
                        unreachable!("enclose");
                    };
                    let enclosure = job.take()?;
                    // Sampled certified:true is diagnostic only.
                    self.enclosure = Some(enclosure);
                    self.compiled = Some(compiled);
                    self.pipeline = Pipeline::Ready;
                    return Ok(JobPoll::Ready);
                }
                Pipeline::RepairCollocate { job, .. } => {
                    if poll_coupled_job(job, budget)? == JobPoll::Pending {
                        return Ok(JobPoll::Pending);
                    }
                    let Pipeline::RepairCollocate {
                        compiled: prior,
                        extra,
                        dt,
                        job,
                    } = std::mem::replace(&mut self.pipeline, Pipeline::Ready)
                    else {
                        unreachable!("repair");
                    };
                    let (raw, functions, blocks, q, tau, charge, horizon) = job.collocation_parts()?;
                    let incoming = {
                        let mut all = prior.incoming.clone();
                        all.extend(extra);
                        all
                    };
                    self.pipeline = Pipeline::Residual(ResidualJob::start(
                        prior.genesis,
                        incoming,
                        raw,
                        functions,
                        horizon,
                        dt,
                        blocks,
                        q,
                        tau,
                        charge,
                    ));
                }
                Pipeline::Ready => return Ok(JobPoll::Ready),
            }
        }
    }

    pub fn start_repair(&mut self, extra: Vec<Intervention>) -> Result<(), ResponseError> {
        let compiled = self
            .compiled
            .clone()
            .ok_or(ResponseError::UnsupportedDomain {
                why: "repair requires a compiled diagnostic response".into(),
            })?;
        let job = CoupledCompileJob::from_repair(&compiled, &extra, self.horizon)?;
        self.consumers = None;
        self.enclosure = None;
        self.pipeline = Pipeline::RepairCollocate {
            compiled,
            extra,
            dt: self.dt,
            job,
        };
        Ok(())
    }

    pub fn bind_consumers(&mut self) -> Result<&BoundConsumers, ResponseError> {
        let compiled = self
            .compiled
            .as_ref()
            .ok_or(ResponseError::UnsupportedDomain {
                why: "consumers require compiled interval functions".into(),
            })?;
        if compiled.interval_functions.is_empty() {
            return Err(ResponseError::UnsupportedDomain {
                why: "no interval functions; adapter labels are not selected geometry".into(),
            });
        }
        let mut charge = Charge::default();
        let (ship_ok, ray_ok, clock_ok, contact_ok) =
            complete_required_queries_compiled(compiled, self.horizon, &mut charge)?;
        if !(ship_ok && ray_ok && clock_ok && contact_ok) {
            self.pending_required
                .push("complete_required_queries_compiled".into());
            return Err(ResponseError::UnsupportedDomain {
                why: "required compiled queries did not complete".into(),
            });
        }
        let ship = fly_ship_compiled(
            compiled,
            0.1,
            [0.0, 3.0],
            [0.125, 0.0],
            self.horizon.min(3.5).max(0.25),
            (self.horizon / 32.0).max(1.0 / 64.0),
            &mut charge,
        )?;
        let ray = fly_ray_compiled(
            compiled,
            0.1,
            [0.0, 3.0],
            [1.0, 0.0],
            8.0,
            0.05,
            &mut charge,
        )?;
        let clock = clock_rate_compiled(compiled, ship.t, ship.x, ship.v, &mut charge)?;
        let (contact_t, contact_d) = contact_closest_compiled(
            compiled,
            0,
            1,
            0.0,
            self.horizon.min(4.0),
            (self.horizon / 16.0).max(1.0 / 32.0),
            &mut charge,
        )?;
        let source0 = body_state_compiled(compiled, 0, self.horizon.min(2.0))?;
        let source1 = body_state_compiled(compiled, 1, self.horizon.min(2.0))?;
        let chord_ship = fly_ship(
            &compiled.worldtubes,
            0.1,
            [0.0, 3.0],
            [0.125, 0.0],
            self.horizon.min(3.5).max(0.25),
            (self.horizon / 32.0).max(1.0 / 64.0),
            &mut charge,
        )?;
        self.consumers = Some(BoundConsumers {
            ship,
            ray,
            clock,
            contact_t,
            contact_d,
            source0,
            source1,
            chord_ship_tau: chord_ship.tau,
        });
        Ok(self.consumers.as_ref().expect("just bound"))
    }

    pub fn query_beyond_horizon(&mut self, t: f64) {
        if t > self.horizon {
            self.pending_required
                .push(format!("required-query@{t}>horizon={}", self.horizon));
        }
    }

    pub fn clear_consumer_cache(&mut self) {
        self.consumers = None;
    }
}

pub fn course_change_program(signal_id: &str) -> PolicyProgram {
    PolicyProgram {
        id: "es-i1-received-course-v0".into(),
        lo: SHIP_ID,
        hi: SHIP_ID,
        watch: vec![],
        rules: vec![PolicyRule {
            guard: Guard::ReceivedSignal(signal_id.into()),
            action: PolicyAction::Burn {
                velocity: Vec2 {
                    x: r(1) / r(4),
                    y: r(0),
                },
            },
        }],
    }
}

fn inertial_body(id: u64, name: &str, x: i128, y: i128, radius: i128) -> Body {
    Body::new(
        id,
        name,
        Inertial::new(0, Vec2::new(x, y), Vec2::zero()).unwrap(),
        r(radius),
        r(1),
    )
}

impl Engine {
    pub fn attach_connected_laboratory(&mut self) -> Result<(), EngineError> {
        let diag = CoupledDiagnostic::laboratory().map_err(|e| EngineError::Unsupported(e.to_string()))?;
        self.coupled = Some(Box::new(diag));
        Ok(())
    }

    /// Bind a chosen GEM genesis as this engine's selected geometry.
    /// Does not mint canonical gravity.
    pub fn attach_coupled_laboratory(
        &mut self,
        genesis: InitialCondition,
        horizon: f64,
        dt: f64,
    ) -> Result<(), EngineError> {
        let diag = CoupledDiagnostic::from_ic(genesis, horizon, dt)
            .map_err(|e| EngineError::Unsupported(e.to_string()))?;
        self.coupled = Some(Box::new(diag));
        Ok(())
    }

    pub fn poll_coupled(&mut self, budget: &mut WorkBudget) -> Result<JobPoll, EngineError> {
        let Some(diag) = self.coupled.as_mut() else {
            return Ok(JobPoll::Ready);
        };
        diag.poll(budget)
            .map_err(|e| EngineError::Unsupported(e.to_string()))
    }

    pub fn coupled_pending_jobs(&self) -> usize {
        self.coupled.as_ref().map_or(0, |d| d.pending_jobs())
    }

    pub fn apply_received_policy(&mut self) -> Result<bool, EngineError> {
        let Some(program) = self.policy.clone() else {
            return Ok(false);
        };
        let now = self.state.clock;
        let mut fired = false;
        for observer in program.lo..=program.hi {
            let already = self.state.policy_fired.contains(&(program.id.clone(), observer))
                || self.state.events.values().any(|e| {
                    e.kind == "burn" && e.tick == now && e.subjects.contains(&observer)
                });
            if already {
                continue;
            }
            let knowledge = self.received_knowledge(observer)?;
            let outcome = evaluate_policy(&program, &knowledge)?;
            if !outcome.fired {
                continue;
            }
            if let PolicyAction::Burn { velocity } = outcome.action {
                let before = self.decode(observer)?.flow().velocity.clone();
                self.apply_course_change(observer, now, velocity.clone())?;
                let e = crate::runtime::event(
                    now,
                    "burn",
                    vec![observer],
                    vec![outcome.knowledge_digest],
                    crate::runtime::digest(&(before, velocity.clone())),
                );
                self.state.events.insert(e.id.clone(), e);
                self.state
                    .policy_fired
                    .insert((program.id.clone(), observer));
                fired = true;
                self.force_rescan = true;
            }
        }
        Ok(fired)
    }

    pub fn received_knowledge(&self, observer: u64) -> Result<ReceivedKnowledge, EngineError> {
        let now = self.state.clock;
        let mut received_signals = BTreeSet::new();
        let mut received_broadcasts = BTreeSet::new();
        for event in self.state.events.values() {
            if event.kind == "signal_arrived" && event.tick <= now && event.subjects.contains(&observer)
            {
                for pred in &event.predecessors {
                    received_signals.insert(pred.clone());
                }
            }
            if event.kind == "broadcast_received"
                && event.tick <= now
                && event.subjects.get(1) == Some(&observer)
            {
                for pred in &event.predecessors {
                    received_broadcasts.insert(pred.clone());
                }
            }
        }
        let observations = if now > 0 {
            self.observe(observer, now, &[EMITTER_ID, BEACON_ID])
                .unwrap_or_default()
        } else {
            Vec::<Observation>::new()
        };
        let proper_time = self
            .decode(observer)
            .ok()
            .and_then(|b| b.proper_time(now).ok())
            .unwrap_or_else(|| r(0));
        Ok(ReceivedKnowledge {
            observer,
            now,
            received_broadcasts,
            received_signals,
            observations,
            proper_time,
            resource: r(1),
        })
    }

    pub fn start_coupled_repair(&mut self, extra: Vec<Intervention>) -> Result<(), EngineError> {
        let diag = self
            .coupled
            .as_mut()
            .ok_or_else(|| EngineError::Unsupported("no coupled diagnostic".into()))?;
        diag.start_repair(extra)
            .map_err(|e| EngineError::Unsupported(e.to_string()))
    }
}

pub fn connected_laboratory_engine() -> Result<Engine, EngineError> {
    let emitter = inertial_body(EMITTER_ID, "emitter", 0, 0, 0);
    let mut ship = inertial_body(SHIP_ID, "test-ship", 8, 0, 1);
    ship.stop_on_contact = true;
    let mut beacon = inertial_body(BEACON_ID, "beacon", 14, 0, 1);
    beacon.stop_on_contact = true;
    let mut engine = Engine::new(0x11C0_11EC, vec![emitter, ship, beacon], vec![])?;
    engine.attach_connected_laboratory()?;
    Ok(engine)
}

#[cfg(test)]
mod tests {
    use super::*;
    use emergent_law_lab::coupled_source_response::{laboratory_two_body, EulerContinueJob};

    #[test]
    fn adapter_does_not_report_canonical_gravity() {
        assert_eq!(CANONICAL_GRAVITY_ACCEPTANCE, "diagnostic-only");
        let ic = laboratory_two_body();
        let mut job = CoupledCompileJob::from_genesis(&ic, &[], 3.0).unwrap();
        let mut budget = WorkBudget::new(1);
        let mut pending = 0;
        loop {
            match poll_coupled_job(&mut job, &mut budget).unwrap() {
                JobPoll::Pending => {
                    pending += 1;
                    budget = WorkBudget::new(1);
                }
                JobPoll::Ready => break,
            }
            assert!(pending < 10_000);
        }
        assert!(pending > 0);
        assert!(job.is_ready());
    }

    #[test]
    fn euler_and_pair_inverse_jobs_yield() {
        let ic = laboratory_two_body();
        let mut euler = EulerContinueJob::from_genesis(&ic, &[], 1.0, 1.0 / 32.0);
        let mut ops = 1u64;
        let mut pending = 0;
        while euler.poll(&mut ops).unwrap() == JobPoll::Pending {
            pending += 1;
            ops = 1;
            assert!(pending < 10_000);
        }
        assert!(pending > 0);

        let mut compile = CoupledCompileJob::from_genesis(&ic, &[], 3.0).unwrap();
        let mut b = u64::MAX;
        while compile.poll(&mut b).unwrap() == JobPoll::Pending {}
        let (raw, funs, blocks, q, tau, charge, horizon) = compile.collocation_parts().unwrap();
        let mut residual = ResidualJob::start(ic.clone(), vec![], raw, funs, horizon, 1.0 / 32.0, blocks, q, tau, charge);
        let mut ops = u64::MAX;
        while residual.poll(&mut ops).unwrap() == JobPoll::Pending {}
        let compiled = residual.take().unwrap();
        let mut inv = PairInverseJob::start(&compiled).unwrap();
        let mut ops = 1u64;
        pending = 0;
        while inv.poll(&mut ops).unwrap() == JobPoll::Pending {
            pending += 1;
            ops = 1;
            assert!(pending < 10_000);
        }
        assert!(pending > 0);
        assert!(inv.is_ready());
    }
}
