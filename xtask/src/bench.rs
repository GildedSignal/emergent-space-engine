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
