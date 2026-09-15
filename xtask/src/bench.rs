use emergent_engine::{
    math::{r, Vec2},
    population::semantic_random,
    propagator::Inertial,
    runtime::Body,
    scenario, Command, Engine,
};
use serde::Deserialize;
use serde_json::{json, Value};
use std::{
    fs,
    path::Path,
    process::Command as Process,
    time::{Instant, SystemTime, UNIX_EPOCH},
};
type Result<T> = super::Result<T>;
#[derive(Deserialize)]
struct ScaleManifest {
    seed: u64,
    population: Vec<u64>,
    families: Vec<usize>,
    age_years: Vec<i128>,
    exception_counts: Vec<usize>,
    explicit_counts: Vec<usize>,
    random_identity_queries: u64,
}
fn shell(program: &str, args: &[&str]) -> String {
    Process::new(program)
        .args(args)
        .output()
        .ok()
        .filter(|o| o.status.success())
        .map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string())
        .unwrap_or_default()
}
pub fn provenance() -> Value {
    let diff = Process::new("git")
        .args(["diff", "HEAD"])
        .output()
        .map(|o| o.stdout)
        .unwrap_or_default();
    json!({"revision":shell("git",&["rev-parse","HEAD"]),"working_tree_status":shell("git",&["status","--porcelain"]),
 "working_tree_diff_hash":blake3::hash(&diff).to_hex().to_string(),"law":emergent_engine::LAW_ID,
 "profile":if cfg!(debug_assertions){"debug"}else{"release"},"unix_seconds":SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs(),
 "rustc":shell("rustc",&["--version"]),"hardware":shell("sysctl",&["-n","machdep.cpu.brand_string"]),"memory_bytes":shell("sysctl",&["-n","hw.memsize"]),
 "manifest_hash":blake3::hash(include_bytes!("../../scenarios/scale-gates.json")).to_hex().to_string()})
}
fn peak_rss() -> u64 {
    let mut usage = std::mem::MaybeUninit::<libc::rusage>::uninit();
    // SAFETY: getrusage initializes the out pointer on success.
    unsafe {
        if libc::getrusage(libc::RUSAGE_SELF, usage.as_mut_ptr()) == 0 {
            let n = usage.assume_init().ru_maxrss as u64;
            if cfg!(target_os = "macos") {
                n
            } else {
                n * 1024
            }
        } else {
            0
        }
    }
}
fn current_rss_bytes() -> u64 {
    let pid = std::process::id().to_string();
    shell("ps", &["-o", "rss=", "-p", &pid])
        .split_whitespace()
        .next()
        .and_then(|s| s.parse::<u64>().ok())
        .map(|kb| kb.saturating_mul(1024))
        .unwrap_or(0)
}
fn apply_exception_interventions(e: &mut Engine, exceptions: usize) -> Result<()> {
    for i in 0..exceptions {
        e.intervene(
            10000 + i as u64 * 17,
            Command::SetVelocity {
                velocity: Vec2 {
                    x: r(1) / r(4),
                    y: r(1 + (i % 3) as i128) / r(1024),
                },
            },
        )?;
    }
    Ok(())
}
fn metric_view(m: &emergent_engine::runtime::Metrics) -> Value {
    json!({
        "search_operations": m.search_operations,
        "scans": m.scans,
        "broadphase_boxes": m.broadphase_boxes,
        "broadphase_pairs": m.broadphase_pairs,
        "box_builds": m.box_builds,
        "sort_steps": m.sort_steps,
        "expire_ops": m.expire_ops,
        "group_ops": m.group_ops,
        "frontier_ops": m.frontier_ops,
        "commit_prep_ops": m.commit_prep_ops,
        "aabb_compares": m.aabb_compares,
        "family_range_ops": m.family_range_ops,
        "sap_repairs": m.sap_repairs,
        "invalidated_pairs": m.invalidated_pairs,
        "quiet_commits": m.quiet_commits,
        "pairs_total": m.pairs_total,
        "pairs_rechecked": m.pairs_rechecked,
        "committed_events": m.committed_events,
        "components": m.components,
        "component_size_max": m.component_size_max,
        "ir_nodes": m.ir_nodes
    })
}
fn delta_u64(after: u64, before: u64) -> u64 {
    after.saturating_sub(before)
}
/// Release-profile the frozen 1,000-exception / 32-tick fixture with setup vs
/// advance timed separately. Repeats are contemporaneous controls on this
/// process; frozen 18.478 ms and H0013 27.768 ms are historical labels only.
pub fn exception_setup_advance() -> Result<Value> {
    let mut relay = scenario::causal_relay()?;
    relay.advance_fully(100)?;
    let relay_labels: Vec<String> = [("signal_arrived", 14), ("contact", 43), ("signal_arrived", 71)]
        .into_iter()
        .map(|(kind, tick)| {
            if relay
                .sorted_events()
                .iter()
                .any(|x| x.kind == kind && x.tick == tick)
            {
                Ok(format!("{kind}@{tick}"))
            } else {
                Err(format!("missing {kind}@{tick}").into())
            }
        })
        .collect::<Result<_>>()?;
    const EXCEPTIONS: usize = 1000;
    const HORIZON: i128 = 32;
    const REPEATS: usize = 3;
    let mut rows = Vec::new();
    for repeat in 0..REPEATS {
        let rss_before = current_rss_bytes();
        let peak_before = peak_rss();
        let t_setup = Instant::now();
        let mut e = scenario::population_fixture(1_000_000_000, 16)?;
        apply_exception_interventions(&mut e, EXCEPTIONS)?;
        let setup_ns = t_setup.elapsed().as_nanos();
        let setup_metrics = e.metrics.clone();
        let extracted = e.state.bodies.len();
        let setup_serialized = serde_json::to_vec(&e.state)?.len();
        let rss_after_setup = current_rss_bytes();
        let peak_after_setup = peak_rss();
        let t_adv = Instant::now();
        let result = e.advance_fully(HORIZON)?;
        let advance_ns = t_adv.elapsed().as_nanos();
        let final_metrics = e.metrics.clone();
        let encoded = serde_json::to_vec(&e.state)?;
        rows.push(json!({
            "repeat": repeat,
            "process_state": if repeat == 0 {
                "first_1k_exception_after_relay_warmup"
            } else {
                "fresh_engine_warm_process"
            },
            "setup_ns": setup_ns,
            "advance_ns": advance_ns,
            "extracted_ships": extracted,
            "advance_operations": result.operations,
            "advance_complete": result.complete,
            "canonical_serialized_bytes_after_setup": setup_serialized,
            "canonical_serialized_bytes_after_advance": encoded.len(),
            "rss_bytes_before_case": rss_before,
            "rss_bytes_after_setup": rss_after_setup,
            "rss_bytes_after_advance": current_rss_bytes(),
            "process_peak_rss_bytes_before_case": peak_before,
            "process_peak_rss_bytes_after_setup": peak_after_setup,
            "process_peak_rss_bytes_after_advance": peak_rss(),
            "setup_metrics": metric_view(&setup_metrics),
            "advance_delta_metrics": {
                "search_operations": delta_u64(final_metrics.search_operations, setup_metrics.search_operations),
                "scans": delta_u64(final_metrics.scans, setup_metrics.scans),
                "pairs_total": delta_u64(final_metrics.pairs_total, setup_metrics.pairs_total),
                "pairs_rechecked": delta_u64(final_metrics.pairs_rechecked, setup_metrics.pairs_rechecked),
                "box_builds": delta_u64(final_metrics.box_builds, setup_metrics.box_builds),
                "sort_steps": delta_u64(final_metrics.sort_steps, setup_metrics.sort_steps),
                "expire_ops": delta_u64(final_metrics.expire_ops, setup_metrics.expire_ops),
                "group_ops": delta_u64(final_metrics.group_ops, setup_metrics.group_ops),
                "frontier_ops": delta_u64(final_metrics.frontier_ops, setup_metrics.frontier_ops),
                "commit_prep_ops": delta_u64(final_metrics.commit_prep_ops, setup_metrics.commit_prep_ops),
                "aabb_compares": delta_u64(final_metrics.aabb_compares, setup_metrics.aabb_compares),
                "family_range_ops": delta_u64(final_metrics.family_range_ops, setup_metrics.family_range_ops),
                "sap_repairs": delta_u64(final_metrics.sap_repairs, setup_metrics.sap_repairs),
                "quiet_commits": delta_u64(final_metrics.quiet_commits, setup_metrics.quiet_commits),
                "committed_events": delta_u64(final_metrics.committed_events, setup_metrics.committed_events)
            },
            "final_metrics": metric_view(&final_metrics)
        }));
    }
    Ok(json!({
        "schema": 1,
        "provenance": provenance(),
        "scope": "1,000-exception / 32-tick inertial fixture; setup (fixture+interventions) vs initial advance timed separately; no gravity",
        "fixture": {
            "logical_ships": 1_000_000_000u64,
            "families": 16,
            "exceptions": EXCEPTIONS,
            "horizon_ticks": HORIZON,
            "intervention": "SetVelocity on identities 10000 + i*17",
            "interventions_before_timed_advance": true
        },
        "relay": {"status": "PASS", "events": relay_labels},
        "accounting": "setup_ns includes population_fixture plus 1,000 SetVelocity interventions. advance_ns is the subsequent advance_fully(32). Repeats use fresh Engine states in one process. Repeat 0 follows only the causal-relay check; it is not the frozen full scale-gates sweep warmup. Serialized bytes are canonical JSON, not RAM. RSS is process-resident (ps rss) and peak is cumulative getrusage ru_maxrss. search_operations are WorkBudget-charged ops.",
        "historical_labels_not_matched_process": {
            "frozen_1dac658_setup_ms": 7.740,
            "frozen_1dac658_advance_ms": 18.478,
            "frozen_serialized_bytes": 923734,
            "h0013_advance_ms": 27.768,
            "h0013_serialized_bytes": 923757,
            "note": "Do not treat frozen 18.478 ms and H0013 27.768 ms as the same process. This file is the contemporaneous control on this checkout."
        },
        "rows": rows
    }))
}
pub fn reference() -> Result<Value> {
    let mut e = scenario::causal_relay()?;
    e.advance_fully(100)?;
    for (kind, tick) in [
        ("signal_arrived", 14),
        ("contact", 43),
        ("signal_arrived", 71),
    ] {
        if !e
            .sorted_events()
            .iter()
            .any(|x| x.kind == kind && x.tick == tick)
        {
            return Err(format!("missing {kind}@{tick}").into());
        }
    }
    Ok(
        json!({"provenance":provenance(),"scenario":"causal-relay-v1","status":"PASS","events":e.sorted_events(),"history_hash":e.history_digest(100)?,"metrics":e.metrics}),
    )
}
pub fn run(out: &Path) -> Result<Value> {
    let manifest: ScaleManifest =
        serde_json::from_slice(include_bytes!("../../scenarios/scale-gates.json"))?;
    if scenario::population_fixture(1, 1)?.state.seed != manifest.seed {
        return Err("scenario seed differs from frozen manifest".into());
    }
    let start_all = Instant::now();
    let mut rows = Vec::new();
    for &count in &manifest.population {
        for &families in &manifest.families {
            let start = Instant::now();
            let mut e = scenario::population_fixture(count, families)?;
            let init_us = start.elapsed().as_micros();
            let t = Instant::now();
            let result = e.advance_fully(scenario::TEN_BILLION_YEARS)?;
            let advance_us = t.elapsed().as_micros();
            let t = Instant::now();
            let mut hash = blake3::Hasher::new();
            for lane in 0..manifest.random_identity_queries {
                let id = 10000 + semantic_random(42, lane, b"benchmark", "lookup", 0) % count;
                hash.update(&serde_json::to_vec(
                    &e.position(id, scenario::TEN_BILLION_YEARS)?,
                )?);
            }
            let lookup_us = t.elapsed().as_micros();
            let encoded = serde_json::to_vec(&e.state)?;
            rows.push(json!({"kind":"population-and-time","logical_ships":count,"families":e.state.families.len(),"extracted_ships":e.state.bodies.len(),"years":10_000_000_000u64,
   "initialization_us":init_us,"advance_us":advance_us,"lookup_1024_us":lookup_us,"total_case_us":start.elapsed().as_micros(),
   "canonical_serialized_bytes":encoded.len(),"process_peak_rss_bytes":peak_rss(),"metrics":e.metrics,"completion":result.complete,
   "query_digest":hash.finalize().to_hex().to_string(),"history_digest":e.history_digest(scenario::TEN_BILLION_YEARS)?}));
        }
    }
    for years in manifest.age_years {
        let start = Instant::now();
        let mut e = scenario::population_fixture(1_000_000_000, 16)?;
        e.advance_fully(years * scenario::JULIAN_YEAR_TICKS)?;
        rows.push(json!({"kind":"age","years":years,"cold_us":start.elapsed().as_micros(),"canonical_serialized_bytes":serde_json::to_vec(&e.state)?.len(),"metrics":e.metrics}));
    }
    for exceptions in manifest.exception_counts {
        let start = Instant::now();
        let mut e = scenario::population_fixture(1_000_000_000, 16)?;
        apply_exception_interventions(&mut e, exceptions)?;
        let setup_us = start.elapsed().as_micros();
        let t = Instant::now();
        let result = e.advance_fully(32)?;
        rows.push(json!({"kind":"exception-fragmentation","exceptions":exceptions,"setup_us":setup_us,"advance_us":t.elapsed().as_micros(),"operations":result.operations,
   "canonical_serialized_bytes":serde_json::to_vec(&e.state)?.len(),"metrics":e.metrics,"process_peak_rss_bytes":peak_rss()}));
    }
    for n in manifest.explicit_counts {
        let start = Instant::now();
        let bodies = (0..n)
            .map(|i| {
                Body::new(
                    i as u64,
                    "independent",
                    Inertial::new(
                        0,
                        Vec2::new((i * 10) as i128, (i % 7 * 10) as i128),
                        Vec2::zero(),
                    )
                    .unwrap(),
                    r(1),
                    r(1),
                )
            })
            .collect();
        let mut e = Engine::new(42, bodies, vec![])?;
        e.advance_fully(1_000_000)?;
        rows.push(json!({"kind":"independent-state","bodies":n,"cold_us":start.elapsed().as_micros(),"metrics":e.metrics,"canonical_serialized_bytes":serde_json::to_vec(&e.state)?.len(),"process_peak_rss_bytes":peak_rss()}));
    }
    let mut e = scenario::population_fixture(1_000_000_000, 256)?;
    e.advance_fully(scenario::TEN_BILLION_YEARS)?;
    let path = out.join("billion-ships.checkpoint");
    let t = Instant::now();
    e.checkpoint(&path)?;
    let write_us = t.elapsed().as_micros();
    let t = Instant::now();
    let restored = Engine::restore(&path)?;
    let read_us = t.elapsed().as_micros();
    if e.history_digest(e.state.clock)? != restored.history_digest(restored.state.clock)? {
        return Err("checkpoint parity failure".into());
    }
    Ok(
        json!({"schema":1,"provenance":provenance(),"scope":"exact inertial indexed families; integrated gravitational scale unqualified","rows":rows,
 "checkpoint":{"bytes":fs::metadata(path)?.len(),"write_us":write_us,"restore_verify_us":read_us},"total_benchmark_seconds":start_all.elapsed().as_secs_f64(),"peak_rss_bytes":peak_rss(),
 "accounting":"RSS is cumulative CPU process peak. Serialized bytes are not RAM. Initialization, queries, checkpoint and restore are charged separately. Build time excluded."}),
    )
}
pub fn fermi() -> Value {
    let cases:Vec<_>=[(1_000u64,10_000u64),(100_000,1_000_000),(1_000_000,10_000_000)].into_iter().map(|(g,e)|json!({"shared_generators":g,"exceptions":e,"illustrative_record_bytes":g*512+e*256})).collect();
    json!({"purpose":"Expose assumptions and select cheap tests. Revise when structure is found. These estimates are not a feasibility or qualification oracle.",
 "memory_model":"G*b_generator + E*b_exception + C*b_certificate + D*b_dependency + responses + resident_history + renderer",
 "work_model":"construction + unresolved interactions + refinement + invalidation + requested decoding; not entities times elapsed ticks",
 "illustrative_cases":cases,"assumptions":"Illustrative 512-byte generators, 256-byte exceptions; excludes all metadata, limbs, graphics and caches.",
 "type_layout_lower_bounds":{"family_shallow_bytes":std::mem::size_of::<emergent_engine::population::Family>(),"body_plus_one_segment_shallow_bytes":std::mem::size_of::<Body>()+std::mem::size_of::<Inertial>()},
 "naive_tick_work":"10^9 ships × 3.15576e17 seconds = 3.15576e26 updates. Generator-native execution avoids this product.",
 "early_probes":["Sweep generator count separately from ship count to expose pair enumeration.","Test a shared co-moving frame before accepting huge worldtube bounds.","Sweep independent exceptions and historical interventions.","Charge random identity decoding, metadata, checkpoint and restore.","Profile useful batches before adding GPU physics."]})
}
