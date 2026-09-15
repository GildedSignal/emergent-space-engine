//! Packet 6: chunk archives, received-knowledge policy IR, individual receptions.
//! Default `Engine::advance` remains `es-inertial-causal-v1`. Truncated GEM stays
//! opt-in. `production_law` is not promoted. No runtime LLMs.

use emergent_engine::{
    compile_policy,
    math::{r, Vec2},
    runtime::{Body, Payload},
    scenario, ArchiveManifest, BroadcastReception, Command, Engine, Guard, LAW_ID,
    PolicyAction, PolicyProgram, PolicyRule, TRUNCATED_COUPLED_LAW_ID, WorkBudget,
};
use std::{
    collections::BTreeMap,
    fs,
    path::{Path, PathBuf},
    time::Instant,
};

fn inertial_body(id: u64, name: &str, x: i128, y: i128) -> Body {
    Body::new(
        id,
        name,
        emergent_engine::propagator::Inertial::new(0, Vec2::new(x, y), Vec2::zero()).unwrap(),
        r(1) / r(8),
        r(1),
    )
}

fn broadcast_fleet() -> Engine {
    let emitter = inertial_body(1, "emitter", 0, 0);
    let near = inertial_body(2, "near", 8, 0);
    let mid = inertial_body(3, "mid", 24, 0);
    let far = inertial_body(4, "far", 0, 10_000);
    Engine::new(0x0006_1510, vec![emitter, near, mid, far], vec![]).unwrap()
}

fn scratch(tag: &str) -> PathBuf {
    let p = std::env::temp_dir().join(format!(
        "es-packet6-{tag}-{}-{}",
        std::process::id(),
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_nanos()
    ));
    fs::create_dir_all(&p).unwrap();
    p
}

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

fn fuel() -> BTreeMap<u64, emergent_engine::math::Rational> {
    let mut m = BTreeMap::new();
    m.insert(2, r(1));
    m.insert(3, r(1));
    m.insert(4, r(1));
    m
}

fn emit_ping(e: &mut Engine) -> String {
    e.intervene(
        1,
        Command::Broadcast {
            lo: 2,
            hi: 4,
            payload: Payload::Ping,
        },
    )
    .unwrap()
}

#[test]
fn default_advance_stays_inertial_and_truncated_stays_opt_in() {
    let mut inertial = scenario::causal_relay().unwrap();
    assert_eq!(inertial.law_id(), LAW_ID);
    inertial.advance_fully(14).unwrap();
    assert_eq!(inertial.law_id(), LAW_ID);
    let gem = scenario::truncated_laboratory().unwrap();
    assert_eq!(gem.law_id(), TRUNCATED_COUPLED_LAW_ID);
    assert_ne!(gem.law_id(), LAW_ID);
}

#[test]
fn old_observations_reconstruct_from_sealed_chunks() {
    let mut live = scenario::causal_relay().unwrap();
    live.advance_fully(40).unwrap();
    let early = live.observe(1, 20, &[2, 3, 4]).unwrap();
    let late = live.observe(4, 40, &[1, 2, 3]).unwrap();
    let digest = live.history_digest(40).unwrap();
    assert!(
        live.sorted_events().len() >= 2,
        "relay must produce multiple committed events"
    );
    let dir = scratch("reconstruct");
    let manifest = live.seal_archive(&dir, 1).unwrap();
    assert!(manifest.chunks.len() >= 2, "committed history must split");
    for (i, listing) in manifest.chunks.iter().enumerate() {
        let chunk = Engine::read_archive_chunk(&dir, i).unwrap();
        assert_eq!(chunk.payload_hash, listing.payload_hash);
        assert!(listing.bytes > 0);
        assert!(listing.bytes < 1024 * 1024);
    }
    let restored = Engine::restore_archive(&dir).unwrap();
    assert_eq!(restored.law_id(), LAW_ID);
    assert_eq!(restored.history_digest(40).unwrap(), digest);
    assert_eq!(restored.observe(1, 20, &[2, 3, 4]).unwrap(), early);
    assert_eq!(restored.observe(4, 40, &[1, 2, 3]).unwrap(), late);
    assert_eq!(
        Engine::reconstruct_observations(&dir, 1, 20, &[2, 3, 4]).unwrap(),
        early
    );
    fs::remove_dir_all(&dir).ok();
}

#[test]
fn incoming_outgoing_influences_survive_sealing() {
    let mut live = broadcast_fleet();
    let id = emit_ping(&mut live);
    live.advance_fully(12).unwrap();
    assert!(matches!(
        live.broadcast_reception(&id, 2),
        Some(BroadcastReception::Received { tick: 8 })
    ));
    assert!(live.state.broadcasts.contains_key(&id), "mid still pending");
    assert_eq!(live.state.signals.len(), 0);
    let incoming_before = live.state.broadcasts.len();
    let dir = scratch("remainder");
    live.seal_archive(&dir, 1).unwrap();
    let restored = Engine::restore_archive(&dir).unwrap();
    assert_eq!(restored.state.broadcasts.len(), incoming_before);
    assert!(restored.state.broadcasts.contains_key(&id));
    assert!(matches!(
        restored.broadcast_reception(&id, 2),
        Some(BroadcastReception::Received { tick: 8 })
    ));
    assert!(!matches!(
        restored.broadcast_reception(&id, 3),
        Some(BroadcastReception::Received { .. })
    ));
    let mut continued = restored;
    continued.advance_fully(30).unwrap();
    assert!(matches!(
        continued.broadcast_reception(&id, 3),
        Some(BroadcastReception::Received { tick: 24 })
    ));
    fs::remove_dir_all(&dir).ok();
}

#[test]
fn shared_broadcast_keeps_individual_receptions() {
    let mut e = broadcast_fleet();
    let id = emit_ping(&mut e);
    e.advance_fully(30).unwrap();
    let near = e.broadcast_reception(&id, 2).cloned();
    let mid = e.broadcast_reception(&id, 3).cloned();
    let far = e.broadcast_reception(&id, 4).cloned();
    assert!(matches!(near, Some(BroadcastReception::Received { tick: 8 })));
    assert!(matches!(mid, Some(BroadcastReception::Received { tick: 24 })));
    assert!(matches!(
        far,
        Some(BroadcastReception::Absent { through }) if through >= 30
    ));
    assert_ne!(near, mid, "one emission, two reception times");
    let encoded = serde_json::to_value(&e.state.broadcasts.get(&id)).unwrap();
    if let Some(obj) = encoded.as_object() {
        assert!(!obj.contains_key("heard"), "no global heard-it bit");
    }
    let received_events: Vec<_> = e
        .sorted_events()
        .into_iter()
        .filter(|ev| ev.kind == "broadcast_received")
        .collect();
    assert_eq!(received_events.len(), 2);
    assert!(received_events.iter().any(|ev| ev.subjects[1] == 2 && ev.tick == 8));
    assert!(received_events.iter().any(|ev| ev.subjects[1] == 3 && ev.tick == 24));
    assert!(!received_events.iter().any(|ev| ev.subjects[1] == 4));
}

#[test]
fn policy_uses_received_knowledge_not_true_state() {
    let mut e = broadcast_fleet();
    let id = emit_ping(&mut e);
    e.advance_fully(12).unwrap();
    let program = ping_program(&id);
    let tree = e.evaluate_policy(&program, 12, &fuel()).unwrap();
    assert!(tree[&2].fired);
    assert!(!tree[&3].fired, "mid has not received yet");
    assert!(!tree[&4].fired);
    let omni = e.omniscient_diagnostic(12).unwrap();
    assert!(omni.true_positions.contains_key(&3));
    assert!(omni.pending_broadcast_ids.contains(&id) || omni.unresolved_receptions.contains_key(&id));
    assert!(
        omni.unresolved_receptions
            .get(&id)
            .is_some_and(|v| v.contains(&3)),
        "omniscient sees the pending mid reception; policy must not"
    );
    let k3 = e
        .received_knowledge(3, 12, &[], r(1))
        .unwrap();
    assert!(!k3.received_broadcasts.contains(&id));
}

#[test]
fn policy_outcomes_survive_archive_and_ir_encoding() {
    let mut live = broadcast_fleet();
    let id = emit_ping(&mut live);
    live.advance_fully(30).unwrap();
    let program = ping_program(&id);
    let bytecode = compile_policy(&program).unwrap();
    let tree = live.evaluate_policy(&program, 30, &fuel()).unwrap();
    let code = live
        .evaluate_policy_bytecode(&bytecode, 30, &fuel())
        .unwrap();
    assert!(Engine::policy_outcomes_match(&tree, &code));
    assert!(tree[&2].fired && tree[&3].fired && !tree[&4].fired);
    let dir = scratch("policy");
    live.seal_archive(&dir, 2).unwrap();
    let restored = Engine::restore_archive(&dir).unwrap();
    let tree2 = restored.evaluate_policy(&program, 30, &fuel()).unwrap();
    let code2 = restored
        .evaluate_policy_bytecode(&bytecode, 30, &fuel())
        .unwrap();
    assert!(Engine::policy_outcomes_match(&tree, &tree2));
    assert!(Engine::policy_outcomes_match(&tree2, &code2));
    fs::remove_dir_all(&dir).ok();
}

#[test]
fn packet6_parity_table_and_artifacts() {
    let t0 = Instant::now();
    let mut relay = scenario::causal_relay().unwrap();
    relay.advance_fully(40).unwrap();
    let live_obs = relay.observe(1, 20, &[2, 3]).unwrap();
    let live_digest = relay.history_digest(40).unwrap();
    let relay_dir = scratch("table-relay");
    let relay_manifest = relay.seal_archive(&relay_dir, 1).unwrap();
    let reconstructed = Engine::reconstruct_observations(&relay_dir, 1, 20, &[2, 3]).unwrap();
    let restored_relay = Engine::restore_archive(&relay_dir).unwrap();
    let reconstruction_held = reconstructed == live_obs
        && restored_relay.history_digest(40).unwrap() == live_digest
        && relay_manifest.chunks.len() >= 2;

    let mut fleet = broadcast_fleet();
    let bid = emit_ping(&mut fleet);
    fleet.advance_fully(12).unwrap();
    let mid_pending = fleet.state.broadcasts.contains_key(&bid);
    let fleet_dir = scratch("table-fleet");
    let fleet_manifest = fleet.seal_archive(&fleet_dir, 1).unwrap();
    let mut restored_fleet = Engine::restore_archive(&fleet_dir).unwrap();
    let remainder_kept = restored_fleet.state.broadcasts.contains_key(&bid);
    restored_fleet.advance_fully(30).unwrap();
    let sealing_held = mid_pending
        && remainder_kept
        && matches!(
            restored_fleet.broadcast_reception(&bid, 3),
            Some(BroadcastReception::Received { tick: 24 })
        );

    let mut policy_world = broadcast_fleet();
    let pid = emit_ping(&mut policy_world);
    policy_world.advance_fully(30).unwrap();
    let program = ping_program(&pid);
    let bytecode = compile_policy(&program).unwrap();
    let tree = policy_world.evaluate_policy(&program, 30, &fuel()).unwrap();
    let code = policy_world
        .evaluate_policy_bytecode(&bytecode, 30, &fuel())
        .unwrap();
    let policy_dir = scratch("table-policy");
    policy_world.seal_archive(&policy_dir, 2).unwrap();
    let restored_policy = Engine::restore_archive(&policy_dir).unwrap();
    let tree2 = restored_policy.evaluate_policy(&program, 30, &fuel()).unwrap();
    let policy_held = Engine::policy_outcomes_match(&tree, &code)
        && Engine::policy_outcomes_match(&tree, &tree2);
    let individual = matches!(
        policy_world.broadcast_reception(&pid, 2),
        Some(BroadcastReception::Received { tick: 8 })
    ) && matches!(
        policy_world.broadcast_reception(&pid, 3),
        Some(BroadcastReception::Received { tick: 24 })
    ) && !matches!(
        policy_world.broadcast_reception(&pid, 4),
        Some(BroadcastReception::Received { .. })
    );

    assert!(reconstruction_held);
    assert!(sealing_held);
    assert!(policy_held);
    assert!(individual);
    assert_eq!(relay.law_id(), LAW_ID);
    assert_eq!(
        scenario::truncated_laboratory().unwrap().law_id(),
        TRUNCATED_COUPLED_LAW_ID
    );

    write_artifacts(
        &relay_dir,
        &fleet_dir,
        &policy_dir,
        &relay_manifest,
        &fleet_manifest,
        reconstruction_held,
        sealing_held,
        policy_held,
        individual,
        t0.elapsed().as_nanos(),
        live_digest,
        tree[&2].fired,
        tree[&3].fired,
        tree[&4].fired,
        relay_manifest.chunks.iter().map(|c| c.bytes).sum(),
        fleet_manifest.chunks.iter().map(|c| c.bytes).sum(),
    );

    fs::remove_dir_all(&relay_dir).ok();
    fs::remove_dir_all(&fleet_dir).ok();
    fs::remove_dir_all(&policy_dir).ok();
}

fn write_artifacts(
    relay_dir: &Path,
    fleet_dir: &Path,
    policy_dir: &Path,
    relay_manifest: &ArchiveManifest,
    fleet_manifest: &ArchiveManifest,
    reconstruction_held: bool,
    sealing_held: bool,
    policy_held: bool,
    individual: bool,
    wall_ns: u128,
    digest: String,
    near_fired: bool,
    mid_fired: bool,
    far_fired: bool,
    relay_chunk_bytes: u64,
    fleet_chunk_bytes: u64,
) {
    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../..")
        .join("artifacts/runs/packet6-history-20260914");
    fs::create_dir_all(&root).unwrap();
    let remainder_relay = fs::metadata(relay_dir.join("remainder.json"))
        .map(|m| m.len())
        .unwrap_or(0);
    let remainder_fleet = fs::metadata(fleet_dir.join("remainder.json"))
        .map(|m| m.len())
        .unwrap_or(0);
    let remainder_policy = fs::metadata(policy_dir.join("remainder.json"))
        .map(|m| m.len())
        .unwrap_or(0);
    let table = format!(
        "# Packet 6 history / policy parity\n\n\
Default `Engine::advance` stayed `es-inertial-causal-v1`. Truncated GEM remained opt-in.\n\
`production_law` was not promoted. No runtime LLMs. No scripted wars or orbits.\n\n\
| claim | live | restored / alt encoding | held |\n\
|---|---|---|---|\n\
| old observations reconstruct from sealed chunks | observe(1,20) | restore_archive + reconstruct_observations | {reconstruction} |\n\
| incoming/outgoing influences survive sealing | mid pending at t=12 | remainder keeps broadcast; reception at t=24 | {sealing} |\n\
| policy outcomes survive archive + IR encoding | tree at t=30 | bytecode and restored archive | {policy} |\n\
| one broadcast, individual receptions | near t=8, mid t=24, far absent | not a global heard-it bit | {individual} |\n\n\
| archive | chunks | chunk bytes | remainder bytes | sealed_through |\n\
|---|---|---|---|---|\n\
| causal_relay t=40, 1 event/chunk | {relay_n} | {relay_bytes} | {remainder_relay} | {relay_cut} |\n\
| broadcast remainder t=12, 1 event/chunk | {fleet_n} | {fleet_bytes} | {remainder_fleet} | {fleet_cut} |\n\
| policy archive t=30 | (see restored match) |  | {remainder_policy} | 30 |\n\n\
Policy fired: near={near_fired}, mid={mid_fired}, far={far_fired} (far never received).\n\
History digest (relay t=40): `{digest}`\n\
Wall ns for table fixture: {wall_ns}\n\
`production_law` remains null. Packet 7 not started. No qualify.\n",
        reconstruction = reconstruction_held,
        sealing = sealing_held,
        policy = policy_held,
        individual = individual,
        relay_n = relay_manifest.chunks.len(),
        relay_bytes = relay_chunk_bytes,
        remainder_relay = remainder_relay,
        relay_cut = relay_manifest.sealed_through,
        fleet_n = fleet_manifest.chunks.len(),
        fleet_bytes = fleet_chunk_bytes,
        remainder_fleet = remainder_fleet,
        fleet_cut = fleet_manifest.sealed_through,
        remainder_policy = remainder_policy,
        near_fired = near_fired,
        mid_fired = mid_fired,
        far_fired = far_fired,
        digest = digest,
        wall_ns = wall_ns,
    );
    fs::write(root.join("cost-table.md"), table).unwrap();
    let report = serde_json::json!({
        "packet": 6,
        "date": "2026-09-14",
        "worktree": "/private/tmp/emergent-packet6-history",
        "branch": "glm/packet6-history",
        "parent": "/private/tmp/emergent-packet5-engine",
        "default_advance_stayed_inertial": true,
        "default_law": LAW_ID,
        "truncated_opt_in": TRUNCATED_COUPLED_LAW_ID,
        "production_law": null,
        "runtime_llms": false,
        "reconstruction_held": reconstruction_held,
        "sealing_held": sealing_held,
        "policy_ir_survival_held": policy_held,
        "individual_receptions": individual,
        "relay_chunks": relay_manifest.chunks.len(),
        "relay_chunk_bytes": relay_chunk_bytes,
        "qualify": false,
        "packet7_started": false,
        "parent_edited_after_add": false
    });
    fs::write(root.join("report.json"), serde_json::to_vec_pretty(&report).unwrap()).unwrap();
}

#[test]
fn inertial_replay_without_broadcasts_stays_byte_identical() {
    let mut e = scenario::causal_relay().unwrap();
    e.advance_fully(20).unwrap();
    e.intervene(
        4,
        Command::SetVelocity {
            velocity: Vec2 {
                x: r(1) / r(8),
                y: r(0),
            },
        },
    )
    .unwrap();
    e.advance_fully(40).unwrap();
    let rebuilt = e.replay().unwrap();
    assert_eq!(e.law_id(), LAW_ID);
    assert_eq!(
        serde_json::to_vec(&e.state).unwrap(),
        serde_json::to_vec(&rebuilt.state).unwrap()
    );
}

#[test]
fn budgeted_advance_still_commits_individual_receptions() {
    let mut e = broadcast_fleet();
    let id = emit_ping(&mut e);
    loop {
        let r = e.advance(30, WorkBudget::new(1)).unwrap();
        if r.complete {
            break;
        }
    }
    assert!(matches!(
        e.broadcast_reception(&id, 2),
        Some(BroadcastReception::Received { tick: 8 })
    ));
    assert!(matches!(
        e.broadcast_reception(&id, 3),
        Some(BroadcastReception::Received { tick: 24 })
    ));
}
