//! Received-knowledge policy IR extracted from Packet 6 as a narrow module.
//!
//! In-world evaluation never reads hidden true-state or future events.
//! Engine wiring, broadcasts on `CanonicalState`, and archive seal/restore
//! remain I1. Packet 5 `truncated_admission` is not part of this schema.
//! Not `production_law`. Default `Engine::advance` stays inertial.

use crate::{
    math::{Rational, Vec2},
    runtime::{EngineError, Observation, Payload},
};
use serde::{Deserialize, Serialize};
use std::collections::BTreeSet;

/// One shared emission toward an identity range. Reception is per-receiver.
/// There is no aggregate heard-it bit on this object.
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct Broadcast {
    pub id: String,
    pub source: u64,
    pub lo: u64,
    pub hi: u64,
    pub tick: i128,
    pub position: Vec2,
    pub payload: Payload,
}

/// Individual reception or certified absence for one worldtube.
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub enum BroadcastReception {
    Received { tick: i128 },
    /// No light-cone intersection on this receiver through `through`.
    /// Horizon growth may replace this; it is not a committed event.
    Absent { through: i128 },
}

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
/// still-pending future arrivals live only here. I1 must not feed this to
/// in-world policy.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct OmniscientDiagnostic {
    pub now: i128,
    pub true_positions: std::collections::BTreeMap<u64, Vec2>,
    pub pending_signal_ids: Vec<String>,
    pub pending_broadcast_ids: Vec<String>,
    pub unresolved_receptions: std::collections::BTreeMap<String, Vec<u64>>,
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

fn digest<T: Serialize>(value: &T) -> String {
    blake3::hash(&serde_json::to_vec(value).expect("serializable canonical facts"))
        .to_hex()
        .to_string()
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
                let b = stack
                    .pop()
                    .ok_or_else(|| EngineError::Invalid("policy stack".into()))?;
                let a = stack
                    .pop()
                    .ok_or_else(|| EngineError::Invalid("policy stack".into()))?;
                stack.push(a && b);
            }
            PolicyOp::Or => {
                let b = stack
                    .pop()
                    .ok_or_else(|| EngineError::Invalid("policy stack".into()))?;
                let a = stack
                    .pop()
                    .ok_or_else(|| EngineError::Invalid("policy stack".into()))?;
                stack.push(a || b);
            }
            PolicyOp::Not => {
                let a = stack
                    .pop()
                    .ok_or_else(|| EngineError::Invalid("policy stack".into()))?;
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

pub fn evaluate_policy(
    program: &PolicyProgram,
    k: &ReceivedKnowledge,
) -> Result<PolicyOutcome, EngineError> {
    let action = first_match_tree(program, k);
    Ok(PolicyOutcome {
        observer: k.observer,
        fired: !matches!(action, PolicyAction::Hold),
        action,
        knowledge_digest: digest(k),
    })
}

pub fn evaluate_policy_bytecode(
    code: &PolicyBytecode,
    k: &ReceivedKnowledge,
) -> Result<PolicyOutcome, EngineError> {
    let action = first_match_bytecode(code, k)?;
    Ok(PolicyOutcome {
        observer: k.observer,
        fired: !matches!(action, PolicyAction::Hold),
        action,
        knowledge_digest: digest(k),
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::math::r;

    fn ping_program(broadcast_id: &str) -> PolicyProgram {
        PolicyProgram {
            id: "es-received-ping-v0".into(),
            lo: 2,
            hi: 4,
            watch: vec![],
            rules: vec![PolicyRule {
                guard: Guard::And(
                    Box::new(Guard::ReceivedBroadcast(broadcast_id.into())),
                    Box::new(Guard::ResourceAtLeast(r(1))),
                ),
                action: PolicyAction::Burn {
                    velocity: Vec2 {
                        x: r(1) / r(8),
                        y: r(0),
                    },
                },
            }],
        }
    }

    fn knowledge(has_broadcast: bool) -> ReceivedKnowledge {
        let mut received_broadcasts = BTreeSet::new();
        if has_broadcast {
            received_broadcasts.insert("ping-1".into());
        }
        ReceivedKnowledge {
            observer: 2,
            now: 12,
            received_broadcasts,
            received_signals: BTreeSet::new(),
            observations: vec![],
            proper_time: r(0),
            resource: r(1),
        }
    }

    #[test]
    fn tree_and_bytecode_match_on_received_knowledge() {
        let program = ping_program("ping-1");
        let code = compile_policy(&program).unwrap();
        let heard = knowledge(true);
        let silent = knowledge(false);
        let tree = evaluate_policy(&program, &heard).unwrap();
        let bytes = evaluate_policy_bytecode(&code, &heard).unwrap();
        assert!(tree.fired && bytes.fired);
        assert_eq!(tree.action, bytes.action);
        let hold = evaluate_policy(&program, &silent).unwrap();
        assert!(!hold.fired);
        assert_eq!(hold.action, PolicyAction::Hold);
    }

    #[test]
    fn omniscient_diagnostic_is_a_distinct_type() {
        let k = knowledge(true);
        let _diag: Option<OmniscientDiagnostic> = None;
        assert!(k.received_broadcasts.contains("ping-1"));
    }
}
