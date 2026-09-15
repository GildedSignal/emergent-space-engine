//! Causal policy IR over received knowledge. Compilable as guarded programs
//! over identity ranges. In-world evaluation never reads hidden true-state or
//! future events. Omniscient diagnostics stay on a separate API.
use crate::{
    math::{r, Rational, Vec2},
    runtime::{
        digest, BroadcastReception, Command, Engine, EngineError, Observation, Payload,
    },
};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

/// Knowledge an in-world planner is allowed to use at a committed cut.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct ReceivedKnowledge {
    pub observer: u64,
    pub now: i128,
    pub received_broadcasts: BTreeSet<String>,
    pub received_signals: BTreeSet<String>,
    pub observations: Vec<Observation>,
    pub proper_time: Rational,
    pub resource: Rational,
}

/// Explicitly separate from [`ReceivedKnowledge`]. Hidden current state and
/// still-pending future arrivals live only here.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct OmniscientDiagnostic {
    pub now: i128,
    pub true_positions: BTreeMap<u64, crate::math::Vec2>,
    pub pending_signal_ids: Vec<String>,
    pub pending_broadcast_ids: Vec<String>,
    pub unresolved_receptions: BTreeMap<String, Vec<u64>>,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub enum Guard {
    Always,
    ReceivedBroadcast(String),
    ReceivedSignal(String),
    Observed { entity: u64 },
    ResourceAtLeast(Rational),
    ProperTimeAtMost(Rational),
    ProperTimeAtLeast(Rational),
    And(Box<Guard>, Box<Guard>),
    Or(Box<Guard>, Box<Guard>),
    Not(Box<Guard>),
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub enum PolicyAction {
    Hold,
    Burn { velocity: Vec2 },
    Broadcast { lo: u64, hi: u64, payload: Payload },
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct PolicyRule {
    pub guard: Guard,
    pub action: PolicyAction,
}

/// Tree encoding of a guarded program over `{lo..=hi}`.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct PolicyProgram {
    pub id: String,
    pub lo: u64,
    pub hi: u64,
    pub watch: Vec<u64>,
    pub rules: Vec<PolicyRule>,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub enum PolicyOp {
    PushTrue,
    PushReceivedBroadcast(String),
    PushReceivedSignal(String),
    PushObserved(u64),
    PushResourceAtLeast(Rational),
    PushProperTimeAtMost(Rational),
    PushProperTimeAtLeast(Rational),
    And,
    Or,
    Not,
}

/// Flattened postfix encoding of the same guarded program.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct PolicyBytecode {
    pub id: String,
    pub lo: u64,
    pub hi: u64,
    pub watch: Vec<u64>,
    pub rules: Vec<(Vec<PolicyOp>, PolicyAction)>,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct PolicyOutcome {
    pub observer: u64,
    pub fired: bool,
    pub action: PolicyAction,
    pub knowledge_digest: String,
}

pub fn compile_policy(program: &PolicyProgram) -> Result<PolicyBytecode, EngineError> {
    if program.lo > program.hi {
        return Err(EngineError::Invalid(
            "policy identity range must satisfy lo <= hi".into(),
        ));
    }
    let mut rules = Vec::new();
    for rule in &program.rules {
        rules.push((compile_guard(&rule.guard), rule.action.clone()));
    }
    Ok(PolicyBytecode {
        id: program.id.clone(),
        lo: program.lo,
        hi: program.hi,
        watch: program.watch.clone(),
        rules,
    })
}

fn compile_guard(guard: &Guard) -> Vec<PolicyOp> {
    match guard {
        Guard::Always => vec![PolicyOp::PushTrue],
        Guard::ReceivedBroadcast(id) => vec![PolicyOp::PushReceivedBroadcast(id.clone())],
        Guard::ReceivedSignal(id) => vec![PolicyOp::PushReceivedSignal(id.clone())],
        Guard::Observed { entity } => vec![PolicyOp::PushObserved(*entity)],
        Guard::ResourceAtLeast(v) => vec![PolicyOp::PushResourceAtLeast(v.clone())],
        Guard::ProperTimeAtMost(v) => vec![PolicyOp::PushProperTimeAtMost(v.clone())],
        Guard::ProperTimeAtLeast(v) => vec![PolicyOp::PushProperTimeAtLeast(v.clone())],
        Guard::And(a, b) => {
            let mut ops = compile_guard(a);
            ops.extend(compile_guard(b));
            ops.push(PolicyOp::And);
            ops
        }
        Guard::Or(a, b) => {
            let mut ops = compile_guard(a);
            ops.extend(compile_guard(b));
            ops.push(PolicyOp::Or);
            ops
        }
        Guard::Not(a) => {
            let mut ops = compile_guard(a);
            ops.push(PolicyOp::Not);
            ops
        }
    }
}

fn eval_guard(guard: &Guard, k: &ReceivedKnowledge) -> bool {
    match guard {
        Guard::Always => true,
        Guard::ReceivedBroadcast(id) => k.received_broadcasts.contains(id),
        Guard::ReceivedSignal(id) => k.received_signals.contains(id),
        Guard::Observed { entity } => k.observations.iter().any(|o| o.entity == *entity),
        Guard::ResourceAtLeast(v) => k.resource >= *v,
        Guard::ProperTimeAtMost(v) => k.proper_time <= *v,
        Guard::ProperTimeAtLeast(v) => k.proper_time >= *v,
        Guard::And(a, b) => eval_guard(a, k) && eval_guard(b, k),
        Guard::Or(a, b) => eval_guard(a, k) || eval_guard(b, k),
        Guard::Not(a) => !eval_guard(a, k),
    }
}

fn eval_ops(ops: &[PolicyOp], k: &ReceivedKnowledge) -> Result<bool, EngineError> {
    let mut stack = Vec::new();
    for op in ops {
        match op {
            PolicyOp::PushTrue => stack.push(true),
            PolicyOp::PushReceivedBroadcast(id) => stack.push(k.received_broadcasts.contains(id)),
            PolicyOp::PushReceivedSignal(id) => stack.push(k.received_signals.contains(id)),
            PolicyOp::PushObserved(entity) => {
                stack.push(k.observations.iter().any(|o| o.entity == *entity))
            }
            PolicyOp::PushResourceAtLeast(v) => stack.push(k.resource >= *v),
            PolicyOp::PushProperTimeAtMost(v) => stack.push(k.proper_time <= *v),
            PolicyOp::PushProperTimeAtLeast(v) => stack.push(k.proper_time >= *v),
            PolicyOp::And => {
                let b = stack.pop().ok_or_else(|| EngineError::Invalid("policy stack".into()))?;
                let a = stack.pop().ok_or_else(|| EngineError::Invalid("policy stack".into()))?;
                stack.push(a && b);
            }
            PolicyOp::Or => {
                let b = stack.pop().ok_or_else(|| EngineError::Invalid("policy stack".into()))?;
                let a = stack.pop().ok_or_else(|| EngineError::Invalid("policy stack".into()))?;
                stack.push(a || b);
            }
            PolicyOp::Not => {
                let a = stack.pop().ok_or_else(|| EngineError::Invalid("policy stack".into()))?;
                stack.push(!a);
            }
        }
    }
    if stack.len() != 1 {
        return Err(EngineError::Invalid("policy stack remainder".into()));
    }
    Ok(stack[0])
}

fn first_match_tree(program: &PolicyProgram, k: &ReceivedKnowledge) -> PolicyAction {
    for rule in &program.rules {
        if eval_guard(&rule.guard, k) {
            return rule.action.clone();
        }
    }
    PolicyAction::Hold
}

fn first_match_bytecode(
    code: &PolicyBytecode,
    k: &ReceivedKnowledge,
) -> Result<PolicyAction, EngineError> {
    for (ops, action) in &code.rules {
        if eval_ops(ops, k)? {
            return Ok(action.clone());
        }
    }
    Ok(PolicyAction::Hold)
}

fn outcome(observer: u64, action: PolicyAction, k: &ReceivedKnowledge) -> PolicyOutcome {
    let fired = !matches!(action, PolicyAction::Hold);
    PolicyOutcome {
        observer,
        fired,
        action,
        knowledge_digest: digest(k),
    }
}

impl Engine {
    /// Received knowledge at a committed cut. Built from committed receptions,
    /// retarded `observe` of `watch`, own proper time, and the caller's local
    /// resource. Does not read other bodies' current positions or pending futures.
    pub fn received_knowledge(
        &self,
        observer: u64,
        now: i128,
        watch: &[u64],
        resource: Rational,
    ) -> Result<ReceivedKnowledge, EngineError> {
        if now < 0 || now > self.state.clock {
            return Err(EngineError::Invalid("uncommitted observation".into()));
        }
        self.decode(observer)?;
        let mut received_broadcasts = BTreeSet::new();
        let mut received_signals = BTreeSet::new();
        for event in self.state.events.values() {
            if event.tick > now {
                continue;
            }
            match event.kind.as_str() {
                "broadcast_received" if event.subjects.get(1) == Some(&observer) => {
                    if let Some(id) = event.predecessors.first() {
                        received_broadcasts.insert(id.clone());
                    }
                }
                "signal_arrived" if event.subjects.get(1) == Some(&observer) => {
                    if let Some(id) = event.predecessors.first() {
                        received_signals.insert(id.clone());
                    }
                }
                _ => {}
            }
        }
        let observations = if watch.is_empty() {
            Vec::new()
        } else {
            self.observe(observer, now, watch)?
        };
        Ok(ReceivedKnowledge {
            observer,
            now,
            received_broadcasts,
            received_signals,
            observations,
            proper_time: self.decode(observer)?.proper_time(now)?,
            resource,
        })
    }

    /// Diagnostic true-state. In-world planners must not call this.
    pub fn omniscient_diagnostic(&self, now: i128) -> Result<OmniscientDiagnostic, EngineError> {
        if now < 0 || now > self.state.clock {
            return Err(EngineError::Invalid("uncommitted observation".into()));
        }
        let mut true_positions = BTreeMap::new();
        for id in self.state.bodies.keys().copied() {
            true_positions.insert(id, self.decode(id)?.at(now));
        }
        let mut unresolved = BTreeMap::new();
        for (id, b) in &self.state.broadcasts {
            let map = self
                .state
                .broadcast_receptions
                .get(id)
                .cloned()
                .unwrap_or_default();
            let pending: Vec<u64> = (b.lo..=b.hi)
                .filter(|r| *r != b.source)
                .filter(|r| !matches!(map.get(r), Some(BroadcastReception::Received { .. })))
                .collect();
            if !pending.is_empty() {
                unresolved.insert(id.clone(), pending);
            }
        }
        Ok(OmniscientDiagnostic {
            now,
            true_positions,
            pending_signal_ids: self.state.signals.keys().cloned().collect(),
            pending_broadcast_ids: self.state.broadcasts.keys().cloned().collect(),
            unresolved_receptions: unresolved,
        })
    }

    pub fn evaluate_policy(
        &self,
        program: &PolicyProgram,
        now: i128,
        resources: &BTreeMap<u64, Rational>,
    ) -> Result<BTreeMap<u64, PolicyOutcome>, EngineError> {
        let mut out = BTreeMap::new();
        for observer in program.lo..=program.hi {
            let resource = resources.get(&observer).cloned().unwrap_or_else(|| r(0));
            let k = self.received_knowledge(observer, now, &program.watch, resource)?;
            let action = first_match_tree(program, &k);
            out.insert(observer, outcome(observer, action, &k));
        }
        Ok(out)
    }

    pub fn evaluate_policy_bytecode(
        &self,
        code: &PolicyBytecode,
        now: i128,
        resources: &BTreeMap<u64, Rational>,
    ) -> Result<BTreeMap<u64, PolicyOutcome>, EngineError> {
        let mut out = BTreeMap::new();
        for observer in code.lo..=code.hi {
            let resource = resources.get(&observer).cloned().unwrap_or_else(|| r(0));
            let k = self.received_knowledge(observer, now, &code.watch, resource)?;
            let action = first_match_bytecode(code, &k)?;
            out.insert(observer, outcome(observer, action, &k));
        }
        Ok(out)
    }

    pub fn policy_outcomes_match(
        tree: &BTreeMap<u64, PolicyOutcome>,
        code: &BTreeMap<u64, PolicyOutcome>,
    ) -> bool {
        if tree.len() != code.len() {
            return false;
        }
        tree.iter().all(|(id, a)| {
            code.get(id).is_some_and(|b| {
                a.observer == b.observer
                    && a.fired == b.fired
                    && a.action == b.action
                    && a.knowledge_digest == b.knowledge_digest
            })
        })
    }
}

impl From<PolicyAction> for Option<Command> {
    fn from(action: PolicyAction) -> Self {
        match action {
            PolicyAction::Hold => None,
            PolicyAction::Burn { velocity } => Some(Command::SetVelocity { velocity }),
            PolicyAction::Broadcast { lo, hi, payload } => {
                Some(Command::Broadcast { lo, hi, payload })
            }
        }
    }
}
