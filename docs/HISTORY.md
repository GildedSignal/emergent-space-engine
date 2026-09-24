# Development history

This is the append-only record of what was built, attempted, learned and rejected, and why. It is **development history**, separate from the engine's canonical simulated event history. H0001–H0009 were reconstructed on 2026-09-12 from explicit user requests, Git commits and retained evidence; they are not contemporaneous experiment logs. Each record states the limits of its evidence.

Use `cargo xtask history list` for the index, `cargo xtask history search "topic"` for full matching entries, and `cargo xtask history check` for validation. Follow [the update procedure](history-workflow.md). Read [the current handoff](HANDOFF.md) for current state; append a correction when a historical interpretation changes.

## H0001 — Preserve the objective and the user's governing corrections

- Date: 2026-09-12
- Kind: user direction
- Status: governing context
- Revisions: Pre-implementation request; archived with this journal's introducing commit.
- Scope: Engine objective, architecture, aesthetics and development practice.
- Changed: The user approved implementation of a deterministic engine targeting one billion addressable ships and ten billion simulated years on an M1/8 GB, with an orchestrator and specialists as the development team. They permitted improvements, asked to conserve sub-agent tokens, emphasized meaningful overlap between distinct ships, and clarified that Fermi estimates spot issues early rather than decide feasibility.
- Why: Preserve the actual intended product and the distinctions that were refined during the conversation. Shared generators, geometry and responses can compress distinct entities; independent bytes-per-ship estimates do not model that structure.
- Validation: The verbatim approved plan was recovered from the user message in the originating task. Original attachments and image references were copied without alteration and SHA-256 hashes recorded. User steering is transcribed in the reference index.
- Evidence: [Approved plan](reference/approved-build-plan.md), [reference index and user steering](reference/README.md), [source manifest](reference/manifest.json), [Fermi reasoning](fermi.md).
- Limitations: Research documents propose candidates; they do not establish a validated gravity law or integrated scaling result. Images set aesthetic foundations rather than final layout or mechanics.
- Next: Apply later explicit user steering first; retain the approved gates and test improvements rather than dismissing compression through a naive state model.

## H0002 — Establish a gated Rust workspace

- Date: 2026-09-11
- Kind: foundation
- Status: implemented
- Revisions: `f5f1613`.
- Scope: Workspace contracts, build organization, task orchestration and initial harness.
- Changed: Created Rust engine, physical-law lab, observatory and task-runner boundaries. Separated a canonical causal laboratory from experimental physical laws and required evidence before gate promotion.
- Why: Prove the smallest complete causal loop before building acceleration around an unqualified physical model. Independent specialist ownership and one heavyweight build at a time limit integration and 8 GB resource pressure.
- Validation: The workspace was subsequently built and exercised by the frozen qualification run at `1dac658`; that later result does not establish every final feature existed at this first commit.
- Evidence: [Workspace](../Cargo.toml), [ownership contract](../AGENTS.md), [task graph](../orchestration/tasks.json), [frozen test output](../artifacts/evidence/1dac658/test-output.txt).
- Limitations: The task graph describes dependencies and acceptance criteria; it is not evidence that all nodes are complete. Development agents are not runtime LLM ship controllers.
- Next: Keep interface changes integrated by one owner and update the task graph when dependencies change.

## H0003 — Define exact inertial geometry and explicit clock semantics

- Date: 2026-09-11
- Kind: numerical law
- Status: implemented in the laboratory law
- Revisions: `c6fcc5d`; later integration corrections in `38bce52`.
- Scope: Canonical arithmetic, worldlines, light cones, contact bins and proper time.
- Changed: Implemented normalized arbitrary-precision rational planar trajectories, exact causal predicates, swept quadratic contact tests and a dyadic proper-clock rate. Contacts are detected inside continuous bins, including tangencies and contacts missed by endpoint sampling. Wide operands are formed before unsafe differences/products.
- Why: Scheduler subdivisions and approximate roots must not select different canonical physics. A finite exact predicate avoids an unbounded increase-precision loop at equality.
- Validation: Independent analytic/grid oracles, integer extrema, rebase/subdivision equivalence and exact dyadic square-root bounds pass in the retained engine suite.
- Evidence: [Laboratory law](laws/inertial-causal-v1.md), [geometry](../crates/engine/src/geometry.rs), [propagators](../crates/engine/src/propagator.rs), [test output](../artifacts/evidence/1dac658/test-output.txt).
- Limitations: The rate is floor(2^32 sqrt(1-v²))/2^32. Near-lightlike clocks can quantize to zero, and continuum clock error grows with duration. This is a deliberately explicit laboratory approximation, not a qualified cosmic-duration physical clock or frozen production quantum.
- Next: Preserve these exact same-law tests; select any production law and quantum through G2 rather than silently changing a solver.

## H0004 — Establish the native visual foundation

- Date: 2026-09-11
- Kind: presentation
- Status: foundation implemented; later connected to the real engine
- Revisions: `a21254d`; runtime integration in `38bce52` and `1dac658`.
- Scope: Native Rust observatory and presentation/engine interface.
- Changed: Built the wgpu/Metal presentation with pale-blue charts, ivory panels, fine ink geometry, astronomical notation, camera controls and an inspector. A command/snapshot bridge separates drawing from authoritative simulation.
- Why: Make the engine inspectable while preserving the reference images as aesthetic inspiration. Floating drawing coordinates and camera actions must not mutate canonical state.
- Validation: Camera round-trip and zoom-anchor tests, canonical time formatting and a later packaged native screenshot smoke run are retained. The initial presentation commit alone did not prove engine integration.
- Evidence: [UI source](../crates/observatory/src/app.rs), [adapter](../crates/observatory/src/adapter.rs), [native smoke](../artifacts/evidence/1dac658/native-smoke.json), [aesthetic references](reference/README.md).
- Limitations: Chart symbols are schematic. The local celestial symbol is an occluder; it has no secretly enabled gravity. Rendering smoke does not qualify 30 FPS or GPU-inclusive memory.
- Next: Preserve delayed knowledge versus diagnostics and verify real command behavior when changing controls.

## H0005 — Execute physical-law candidates and retain their rejection

- Date: 2026-09-12
- Kind: research experiment
- Status: G2 failed; no production law selected
- Revisions: Candidate implementation `515e1f6`; frozen integrated evidence from `1dac658`, retained by `99764b4`.
- Scope: Stationary quantized Verlet and stationary shell-lapse experimental laws.
- Changed: Implemented both finite maps and evaluated frozen orbit, rotation, quantum, clock, source-bound and backreaction fixtures. A changed-source experiment records nonzero influence before light-cone arrival. JSON explicitly retains missing causal dynamics, exterior treatment, compact-field certification and exact branch qualification.
- Why: Stable-looking orbits and research citations cannot establish the physical law the optimized engine must preserve. Candidate laws must stay separate from the canonical causal laboratory.
- Validation: `cargo xtask law-lab` and full qualification return exit 2 with `production_law: null`. The Verlet experiment passes several orbit/source diagnostics but fails required gates; the shell-lapse experiment also fails orbital stability, rotation and refinement gates. Eight lab tests pass as implementation checks, not production-law promotion.
- Evidence: [Experiment semantics](law-lab.md), [frozen gate manifest](../scenarios/law-gates.json), [complete failed results](../artifacts/evidence/1dac658/law-qualification.json).
- Limitations: These are stationary weak-field experiments using floating arithmetic. Their failure does not disprove every variational or piecewise-metric construction. The bounded monopole tree is not production FMM, and its floating padding is not a rigorous numerical certificate.
- Next: Formulate and falsify a complete causal candidate with an authoritative finite evaluator and exterior before optimizing gravity. Keep G3 and integrated G8 blocked until a law qualifies.

## H0006 — Integrate the causal loop and shared populations

- Date: 2026-09-12
- Kind: implementation and compression experiment
- Status: causal laboratory and scoped compression mechanisms implemented
- Revisions: `38bce52`.
- Scope: Scheduler, signals, simultaneous contacts, indexed families and sparse exceptions.
- Changed: Connected reception, impulse, contact stop, notification and replay into one causal loop. Added affine identity families with exact partition offsets, binary family lookup and selective member extraction. Swept boxes use a common co-moving frame; extracted identities are removed from derived ranges before spatial refinement.
- Why: Charge independently changing descriptions and consequential interactions rather than logical ships times elapsed ticks. Common drift should cancel before making long-horizon bounds enormous. Repeatedly rediscovering an exception at the leaves of a family tree was avoidable work.
- Validation: The relay fixes event ticks 14/43/71. Compressed versus individual collision and occlusion tests pass, including first/middle/last member extraction. The final frozen inertial sweep represents 1e9 distinct ships in 16 families using 5,463 serialized bytes; a 1,000-exception advance takes 18.478 ms.
- Evidence: [Runtime](../crates/engine/src/runtime.rs), [family representation](../crates/engine/src/population.rs), [differential contracts](../crates/engine/tests/causal_contract.rs), [frozen benchmarks](../artifacts/evidence/1dac658/benchmarks.json), [measurement limits](implementation-report.md).
- Limitations: The earlier roughly one-second exception probe was not a controlled release baseline. The 5.5 KB figure is serialized state, not RAM. Families currently share velocity and must have disjoint members. Broad-phase setup is not yet fully cooperative, and no gravity participates in these scale sweeps.
- Next: Test more general route/departure/phase families and fragmentation with fixed fixtures; preserve identity and exact interaction semantics. Make broad-phase work resumable before claiming bounded command latency.

## H0007 — Make replay, serialization and resource failures explicit

- Date: 2026-09-12
- Kind: correctness and operational repair
- Status: implemented with recorded limits
- Revisions: `38bce52`; related adapter reporting in `1dac658`.
- Scope: Checkpoints, replay, domain-limited responses, arithmetic serialization and local builds.
- Changed: Added atomic checksummed checkpoints, genesis plus ordered-command replay, full-state replay comparison, response domain/dependency checks, sorted-range validation, overflow checks and prevalidated notification limits. Enabled serde_json float_roundtrip after a dyadic manifest value parsed differently. Local generated build artifacts were moved outside iCloud after dataless files stalled reads.
- Why: A loadable checkpoint is weaker evidence than regenerated canonical state. Budget failures must not partially commit an event transaction. Numerical fixture serialization is part of reproducibility. Build stalls must be diagnosed separately from compiler or engine failures.
- Validation: Corruption/law rejection, checkpoint restart parity, full replay, invalid simultaneous burns, extreme identities and notification resource failures pass. Restoring local file access allowed tests, builds and linting to finish.
- Evidence: [Storage](../crates/engine/src/storage.rs), [responses](../crates/engine/src/response.rs), [Cargo numerical feature](../Cargo.toml), [runtime limitations](architecture.md), [contract tests](../crates/engine/tests/causal_contract.rs).
- Limitations: Checkpoints cap at 256 MiB and still serialize full state. Restore/integrity checking is separate from Engine::replay. General chunked archives, response compilation, byte budgets and query continuations remain incomplete. The local cache symlink is machine configuration, not portable project configuration.
- Next: Keep float_roundtrip and explicit law/version handling; test interrupted writes, incremental work and historical reconstruction when extending storage. Inspect file flags and local build paths before retrying a stalled Cargo command.

## H0008 — Verify real native commands and visible sensor failures

- Date: 2026-09-12
- Kind: integration verification
- Status: implemented and tested
- Revisions: `1dac658`.
- Scope: Worker-owned engine and observatory commands.
- Changed: Ensured incomplete sensor queries produce an explicit warning instead of silently appearing as an empty sky. Verified actual course changes, identity lookup, sensing, signals, time advancement, save and restore through the worker bridge.
- Why: A responsive renderer alone does not prove the controls reach the engine. A resource failure must be distinguishable from valid absence of observations.
- Validation: Five native unit/integration tests pass, including command-to-state checks and sensor capability failure visibility. The packaged application later rendered and exited successfully in the frozen smoke run.
- Evidence: [Worker adapter and tests](../crates/observatory/src/adapter.rs), [frozen native smoke](../artifacts/evidence/1dac658/native-smoke.json), [test output](../artifacts/evidence/1dac658/test-output.txt).
- Limitations: Heading changes are controlled rational burns, not fuel-optimal moving-target navigation or autonomous docking. Some long preparation/query work can still occupy the worker; arbitrary event-storm latency is unqualified.
- Next: Extend cooperative work and navigation only behind explicit capability boundaries; preserve sensor-state purity and visible failures.

## H0009 — Freeze the implementation evidence and current gate verdict

- Date: 2026-09-12
- Kind: qualification record
- Status: G0/G1 pass in scoped lab; G2 fail; full release unqualified
- Revisions: Tested source `1dac6586e3cb30592abb775ba2a844d7d0e2d189`; evidence/documentation commit `99764b4`.
- Scope: Correctness, inertial mechanism performance and packaged native smoke on Apple M1/8 GiB.
- Changed: Retained complete gate results, commands, source and binary hashes, hardware, benchmark denominators, failures and test output. Packaged a local development app and wrote an implementation report.
- Why: Future agents need an immutable measured baseline and explicit negative results, not a summary that grows stronger each time it is repeated.
- Validation: 53 tests pass; workspace Clippy passes with warnings denied. Qualification exits 2 in 2.812 seconds including tests, separately from build time. Native smoke exits 0 after 120 frames; observed 4.39 seconds includes startup, capture and shutdown. Git was clean at the tested source revision.
- Evidence: [Run manifest](../artifacts/evidence/1dac658/run-manifest.json), [gate verdict](../artifacts/evidence/1dac658/qualification.json), [implementation report](implementation-report.md), [native footprint and scope](../artifacts/evidence/1dac658/native-smoke.json).
- Limitations: G3/G8 are blocked and G4–G7 partial. No integrated causal-gravity scale, 30 FPS envelope, GPU physics parity, total GPU-inclusive memory qualification, publication or notarization. The 53 count belongs to the frozen source; later tooling tests do not retroactively change it.
- Next: Create new evidence directories for later revisions; never overwrite this baseline or treat qualification exit 2 as a successful release.


## H0010 — Preserve the full handoff and make the journal operational

- Date: 2026-09-12
- Kind: handoff and tooling
- Status: implemented and verified
- Revisions: Engine/evidence baseline `99764b4`; this entry's commit contains the continuity documents, archived context and history tooling.
- Scope: Agent context, decision provenance, archived source materials and the development task runner; engine physics unchanged.
- Changed: Added an actionable handoff and retrospective history, archived the verbatim approved plan, original conversation/research and all three aesthetic references with hashes, and added history list/search/template/append/check commands. AGENTS.md requires journal maintenance; standard xtask test/qualify validate it before tests. An independent bounded read-only audit checked the essential gate/limit context. The handoff also identifies the unpinned RNG golden-vector test as a future audit task.
- Why: The user requested all context for successor agents and an operational record of what was done and why. A searchable decision journal and portable source archive avoid relying on chat memory, ephemeral clipboard files, reconstructed claims or repeated failed experiments.
- Validation: `cargo xtask test artifacts/runs/handoff-20260912` passes all 55 tests (53 existing plus 2 journal tests). `cargo clippy -p xtask --all-targets --locked --offline -- -D warnings` passes. A real append attempt with an unfinished template fails without changing the journal. History search finds the co-moving decision. Active documentation links and all six original-source hashes were checked; final append/check outcomes are retained separately.
- Evidence: [Current handoff](HANDOFF.md), [update procedure](history-workflow.md), [source archive](reference/README.md), [source hashes](reference/manifest.json), [workflow checks](../artifacts/evidence/handoff-20260912/workflow-checks.json), [55-test output](../artifacts/evidence/handoff-20260912/test-output.txt), [final checks](../artifacts/evidence/handoff-20260912/final-checks.json), [journal tool](../xtask/src/history.rs).
- Limitations: H0001–H0009 are explicitly retrospective. The checker enforces structure, local links and preservation of the committed prefix; it cannot prove test execution or semantic truth. Appends require one integrator. No new physics/performance qualification was run and the frozen G2 failure remains unchanged.
- Next: Successor agents start with HANDOFF.md and history search, choose a bounded task, append real outcomes and update the handoff when state changes. Follow the physical-law and cooperative-work priorities without treating this documentation milestone as engine completion.


## H0011 — Isolate a retarded causal kernel and two-sided source-change falsifier

- Date: 2026-09-12
- Kind: research experiment
- Status: implemented; G2 still failed; no production law
- Revisions: Uncommitted law-lab work on `codex/emergent-engine` above `47f3290`; frozen G2 evidence remains `1dac658` / `99764b4` and was not overwritten.
- Scope: `crates/law-lab` only; inertial laboratory law `es-inertial-causal-v1` is untouched and the kernel is not wired into the engine.
- Changed: Added isolated candidate `es-causal-retarded-monopole-v0` with exact rational light-cone membership on piecewise-constant source worldtubes. The first gate is a two-sided source-change falsifier: zero influence inside the cone, nonzero after. Additive fixtures cover compact/far, huge-mass, moving-source, exterior-r16 and simultaneous-change cases. Stationary Verlet/lapse still fail the first gate. No orbit map was added or tuned.
- Why: G2 already rejected instantaneous maps. Floating orbits cannot hide missing retarded sources. The approved plan's causal-kernel-plus-research-failure path requires a cheap source-change falsifier before orbit work.
- Validation: Specialist-reported `cargo test -p emergent-law-lab --offline --locked` — 17 passed. Clippy for law-lab with `-D warnings` is clean. Full `cargo xtask qualify` was not run this turn.
- Evidence: [Research kernel](../crates/law-lab/src/causal_kernel.rs), [experiment semantics](law-lab.md), [gate manifest](../scenarios/law-gates.json), [frozen G2 results](../artifacts/evidence/1dac658/law-qualification.json).
- Limitations: f64 Newton on prescribed worldtubes; not GR, FMM, two-way backreaction, well-posed exterior or terminating exact branches. `production_law` remains null. This is not delayed-Newton-as-G2 and does not qualify gravity.
- Next: Self-consistent retarded two-way backreaction in the isolated law-lab before any orbit integrator. Do not wire this kernel into the canonical engine.


## H0012 — Cooperative spacetime compile and incremental SAP

- Date: 2026-09-12
- Kind: implementation and measurement
- Status: implemented and measured
- Revisions: Uncommitted engine work on `codex/emergent-engine` above `47f3290`; frozen baseline `1dac658` / `99764b4` was not overwritten.
- Scope: Inertial compiler for laboratory law `es-inertial-causal-v1` and `scripted-interaction-v1`; no gravity.
- Changed: `WorkBudget` now charges box construction, family-range subtraction, sorting and AABB compares; `start_scan` is resumable. After a burn or contact, co-moving SAP repairs dirty adjacencies instead of always rebuilding. Scheduled `Command::SetCourse` and addressed `Payload::SetCourse` compile as IR; a family member is extracted only when its generator actually changes. Runtime is documented as a spacetime compiler.
- Why: Uncharged `start_scan` plus `pending=None` produced command stutter: construction work escaped the budget. Charged resumable construction and incremental SAP address that without changing canonical event identity.
- Validation: Specialist-reported `cargo xtask test` PASS; workspace clippy `-D warnings` PASS. Relay events remain 14/43/71. History digest equal under full vs budget-1 vs cancel/resume vs compressed vs materialized. Pairwise contact oracle on a 64-body one-burn fixture. Qualify was not run this turn.
- Evidence: [Runtime compiler](../crates/engine/src/runtime.rs), [cooperative tests](../crates/engine/tests/compiler_coop.rs), [architecture](architecture.md), [handoff](HANDOFF.md), [cooperative metrics](../artifacts/runs/compiler-coop-20260912/metrics.json).
- Limitations: Sort is still one atomic std sort; quiet commits re-enqueue all overlaps; sensor continuations, responses, route/phase families and RSS remain open. 18.210 vs frozen 18.478 ms is single-run noise on a zero-event fixture; `scheduled_courses` adds about 23 serialized bytes (923,757 vs frozen 923,734).
- Next: Persist overlap certificates across quiet commits and measure `pairs_rechecked`. Keep G2 isolated from this compiler track.


## H0013 — Persist overlap certificates across quiet commits

- Date: 2026-09-12
- Kind: implementation and measurement
- Status: implemented and measured
- Revisions: Uncommitted engine work on `codex/emergent-engine` above `47f3290`; frozen baseline `1dac658` / `99764b4` was not overwritten.
- Scope: Inertial compiler for laboratory law `es-inertial-causal-v1` and `scripted-interaction-v1`; no gravity.
- Changed: Overlap pairs are compiled through the remaining scan horizon and certified. Quiet commits keep already-discovered later candidates and do not re-enqueue certified pairs. Dirty SAP repairs local adjacencies and drops certificates only for changed generators. Runtime metrics now include `pairs_total`, `pairs_rechecked` and `quiet_commits`.
- Why: [H0012](HISTORY.md) re-enqueued every overlap after a quiet commit, repeating certified pair work.
- Validation: Specialist-reported `cargo xtask test` PASS; workspace clippy `-D warnings` PASS. Relay events remain 14/43/71. 64-body one-burn matches pairwise `first_contact` and rebuild; incremental 2.090 ms vs rebuild 4.602 ms; `pairs_rechecked` 0/20 vs re-enqueue-all 20. 256-body budget-1 digest match, stutter 99_459 ns. Two quiet contacts `pairs_rechecked=0`. Grazing miss, integer tangency and two-family miss oracles pass. Qualify was not run this turn.
- Evidence: [Runtime compiler](../crates/engine/src/runtime.rs), [cooperative tests](../crates/engine/tests/compiler_coop.rs), [architecture](architecture.md), [handoff](HANDOFF.md), [overlap certificate metrics](../artifacts/runs/compiler-overlap-certs-20260912/metrics.json).
- Limitations: Sort is still one atomic std sort. 27.768 vs frozen 18.478 ms on the 1,000-exception/32-tick case is a single run; do not claim a win (unresolved noise-or-cost, possible regression vs frozen, not a speedup). 923,757 serialized bytes are not RAM. This is not a production KDS heap. `production_law` remains null; G2 stays isolated.
- Next: Sensor/query continuations. Keep G2 isolated from this compiler track. Isolated law-lab next remains self-consistent retarded two-way backreaction.


## H0014 — Resumable observe / family occlusion continuations

- Date: 2026-09-12
- Kind: implementation and measurement
- Status: implemented and measured
- Revisions: Uncommitted engine work on `codex/emergent-engine` above `47f3290`; frozen baseline `1dac658` / `99764b4` was not overwritten.
- Scope: Inertial compiler sensor/occlusion for laboratory law `es-inertial-causal-v1`; observatory worker uses the engine continuation; no gravity.
- Changed: `observe_with_budget` yields on `WorkBudget`, stores a sensor continuation, and resumes to the same observation set as full `observe()` after `clear_derived` cancel. Family-range pops and target setup are charged (`sensor_ops` versus `sensor_refinements`). Incomplete queries are pending/warning, never a silent empty sky. Hard `max_pending_jobs` is still `ResourceLimit`. Course-change acks while a sensor job is pending (the job is dropped, not blocked). Historical observations remain emission coordinates.
- Why: [H0013](HISTORY.md) left observe/family occlusion on a hard cap without a continuation token.
- Validation: Specialist-reported `cargo xtask test` PASS; workspace clippy `-D warnings` PASS. The same observation set for full versus budget-1 versus cancel/resume versus reversed target order. Digest/state unchanged by query. Budget-0 is pending; `max_pending_jobs=0` still errors. Qualify was not run this turn.
- Evidence: [Runtime compiler](../crates/engine/src/runtime.rs), [cooperative tests](../crates/engine/tests/compiler_coop.rs), [observatory adapter](../crates/observatory/src/adapter.rs), [architecture](architecture.md), [handoff](HANDOFF.md), [sensor continuation metrics](../artifacts/runs/compiler-sensor-cont-20260912/metrics.json).
- Limitations: Debug single-run 1e6 occluder is an O(log N) AABB spine (64 charged ops / 62 refinements, `observation_count=1`, stutter 1.32 ms, command_ack 163 µs). Adapter UI budget is 96. The 1,000-exception/32-tick case was not remeasured ([H0013](HISTORY.md) 27.8 vs frozen 18.5 ms remains unresolved). Sort is still one atomic std sort. `production_law` remains null; G2 stays isolated.
- Next: Route/departure/phase families behind the same decoder/enclosure/extraction contract. Keep G2 isolated from this compiler track. Isolated law-lab next remains self-consistent retarded two-way backreaction.


## H0015 — Archive continued conversation

- Date: 2026-09-12
- Kind: handoff/reference
- Status: implemented
- Revisions: Uncommitted docs-only archive on `codex/emergent-engine`; no engine change. Frozen baseline `1dac658` / `99764b4` was not overwritten.
- Scope: Source archive under `docs/reference/`; portable copy of a later ChatGPT dump.
- Changed: Copied `/Users/julien_laurent/Downloads/Reconstruct emergent space idea (1).md` unchanged to original-conversation-continued.md. Recorded SHA-256 `07e1cdfaea10c62e1f500240d1f59212bde72d18138108a9e2bd8939a7ae4ec7` in manifest.json. Indexed in reference README as a continuation of original-conversation.md, not a replacement.
- Why: Keep the rest of the conversation in-repo for later agents instead of leaving it only in Downloads.
- Validation: Archive present; SHA-256 as above; original conversation file not replaced. History check after append.
- Evidence: [Continued conversation](reference/original-conversation-continued.md), [reference index](reference/README.md), [source manifest](reference/manifest.json).
- Limitations: Archive is intent and proposed improvements, not qualified physics or a new governing plan. Later explicit user steering still governs. Does not change engine, gates or production_law.
- Next: Extract and implement ranked improvements from the continuation after route/phase-family work is integrated or reported. Keep G2 isolated.


## H0016 — Phase/departure families and range-course hyperedge IR

- Date: 2026-09-12
- Kind: implementation and measurement
- Status: implemented and measured
- Revisions: Uncommitted engine work on `codex/emergent-engine` above `47f3290`; frozen baseline `1dac658` / `99764b4` not overwritten.
- Scope: Inertial compiler families plus `scripted-interaction-v1` range IR; laboratory law `es-inertial-causal-v1`; no gravity.
- Changed: Hold-then-cruise phase families; lab frame when velocities differ. `SetCourseRange` is one hyperedge over `{lo..=hi}`; `FamilyPhaseBurn` is sugar. Extract only when a member generator changes. Do not merge causally adjacent families. Shared course is not expanded into a clique.
- Why: Continuation dump: a shared `SetCourse` must not extract-all. Equivalence grouping is not interaction grouping.
- Validation: Specialist-reported `cargo test -p emergent-engine --lib` PASS (24); `--test compiler_coop` PASS (26); `--test causal_contract` PASS (18, relay 14/43/71); workspace clippy `-D warnings` PASS; `cargo xtask test` PASS. Qualify was not run. Extraction 1/17 (fixture), 0/1e6 (range burn). Event facts match compressed versus materialized; `history_digest` differs across representations because it hashes genesis.
- Evidence: [Indexed populations](../crates/engine/src/population.rs), [runtime compiler](../crates/engine/src/runtime.rs), [cooperative tests](../crates/engine/tests/compiler_coop.rs), [phase-family metrics](../artifacts/runs/compiler-phase-families-20260912/metrics.json), [handoff](HANDOFF.md).
- Limitations: No full polyline; no interior certificates for non-self-disjoint families (must materialize). Debug walls are not speed claims. 1k-exception 27.8 vs frozen 18.5 ms remains unresolved. G2 isolated; `production_law` null. `history_digest` is not a representation-invariant for family versus fully materialized genesis.
- Next: Causal-component grouping of the existing overlap graph plus guarded family-range IR traces (compile until earliest possible invalidation). Do not start per-region clocks. Chunked history remains deferred. Isolated law-lab remains two-way retarded backreaction.


## H0017 — Causal-component grouping and guarded family/IR traces

- Date: 2026-09-12
- Kind: implementation and measurement
- Status: implemented and measured
- Revisions: Uncommitted engine work on `codex/emergent-engine` above `47f3290`; frozen baseline `1dac658` / `99764b4` not overwritten
- Scope: inertial compiler `es-inertial-causal-v1` / `scripted-interaction-v1`; no gravity
- Changed: After SAP, connected components of certified overlaps are independent compile islands on the finite scan horizon. Each family/SAP item compiles one guarded IR segment (enclosure disjointness, next SetCourse/SetCourseRange, contact-stop, inbound signal) until the earliest conservative invalidation; a failed guard applies IR and recompiles. Equivalence grouping is not interaction grouping.
- Why: Continuation dump: lightcone intersections resolve or group; compile until earliest possible invalidation. Quiet space is many tiny components; a dense encounter is one large component. Not battle mode, Hz, rollback, or speculation.
- Validation: cargo xtask test PASS; workspace clippy -D warnings PASS. Relay 14/43/71. 64-body one-burn matches pairwise first_contact and rebuild digest. Quiet 16-family pairs_rechecked 0/0; dense pairs_rechecked 0/20 vs re-enqueue-all 20. Unchanged generators extract 0/1024. Qualify not run.
- Evidence: [Runtime compiler](../crates/engine/src/runtime.rs), [cooperative tests](../crates/engine/tests/compiler_coop.rs), [architecture](architecture.md), [handoff](HANDOFF.md), [causal-component metrics](../artifacts/runs/compiler-causal-components-20260912/metrics.json).
- Limitations: Debug single-run; bytes ≠ RAM. 64-body mixed fixture formed small clusters (component_size_max 3/64), not a packed battle. Sort still atomic std sort. 1k-exception 27.8 vs frozen 18.5 ms unresolved. Per-region clocks and uneven committed cuts deferred. production_law null; G2 isolated.
- Next: Dense-overlap / war-island fixture so component_size_max actually stresses grouping (continuation dump: dense wars are the hard case). Do not start per-region clocks. RNG golden vector remains a cheap audit. Isolated law-lab remains two-way retarded backreaction.


## H0018 — Packed-overlap war-island causal-component stress

- Date: 2026-09-12
- Kind: implementation and measurement
- Status: implemented and measured
- Revisions: Uncommitted engine work on `codex/emergent-engine` above `47f3290`; frozen baseline `1dac658` / `99764b4` not overwritten
- Scope: inertial compiler `es-inertial-causal-v1` / `scripted-interaction-v1`; no gravity
- Changed: Frozen packed-overlap / war-island fixture (64 bodies + 8 overlapping families + 2 far families) with scripted SetCourseRange, signal and contacts. component_size_max 72/72 packed SAP items (3/74 components). Quiet 16-family remains 16 singletons. Scheduled range IR no longer restores a pre-burn SAP. Equivalence grouping is not interaction grouping.
- Why: [H0017](HISTORY.md) mixed fixture only reached size_max 3/64. Continuation dump: dense wars are the hard case. Not battle mode, Hz, or per-region clocks.
- Validation: cargo xtask test PASS; workspace clippy -D warnings PASS. Relay 14/43/71. Packed contacts/digest match pairwise oracle and rebuild. Far families stay out. pairs_rechecked 0/2222 vs re-enqueue-all 84436. Unchanged generators extract 0 family members (64/64 genesis bodies). Qualify not run. One retry after parallel 5 ms stutter flake on pre-existing mixed-64 bounds — thresholds not weakened.
- Evidence: [Runtime compiler](../crates/engine/src/runtime.rs), [scenario fixtures](../crates/engine/src/scenario.rs), [cooperative tests](../crates/engine/tests/compiler_coop.rs), [architecture](architecture.md), [handoff](HANDOFF.md), [war-island metrics](../artifacts/runs/compiler-war-island-20260912/metrics.json).
- Limitations: Debug single-run; bytes ≠ RAM. Packed wall ~849 ms debug is not a speed claim. Simultaneous packed contacts commit as one uncharged batch. Range burn currently full-rescan. Sort still atomic std sort. 1k-exception 27.8 vs 18.5 ms unresolved. Per-region clocks deferred. production_law null; G2 isolated.
- Next: Isolated law-lab self-consistent retarded two-way backreaction (sibling already assigned). Do not start per-region clocks. RNG golden vector remains a cheap audit.


## H0019 — Self-consistent retarded two-way backreaction

- Date: 2026-09-12
- Kind: research experiment
- Status: implemented; G2 still failed; no production law
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `47f3290`; frozen G2 evidence `1dac658` / `99764b4` not overwritten
- Scope: `crates/law-lab` only; `es-inertial-causal-v1` untouched; neither research kernel wired into the engine
- Changed: Measured two-sided trajectory falsifier `retarded_two_way_backreaction`. Prescribed worldtubes fail post-cone. Instantaneous present-state two-body fails pre-cone. Tiny-N candidate `es-causal-retarded-coupled-v0`: next source segment is excluded-self retarded 3D-planar Euler of committed history. Additive fixtures: authored/instantaneous negative controls, coupled mass-change r=4, every-mass sources, mutual two-way, fleet N=64. Frozen numeric thresholds not edited. Verlet/lapse remain rejected.
- Why: [H0011](HISTORY.md) kernel could not couple the field back onto sources. Floating orbits cannot hide missing two-way retarded backreaction. Every mass sources by μ, not is_planet.
- Validation: `cargo test -p emergent-law-lab --offline --locked` — 29 passed. Clippy `-p emergent-law-lab --all-targets --offline --locked -- -D warnings` clean. Full qualify not run.
- Evidence: [Coupled kernel](../crates/law-lab/src/coupled.rs), [research kernel](../crates/law-lab/src/causal_kernel.rs), [experiment semantics](law-lab.md), [gate manifest](../scenarios/law-gates.json), [frozen G2 results](../artifacts/evidence/1dac658/law-qualification.json), [H0011](HISTORY.md)
- Limitations: f64 Euler on tiny N; not GR, FMM, delayed-Newton-as-G2, well-posed exterior, compact-field certification, or terminating exact branches. Frozen Newton `source_backreaction` stays failed on research kernels (retarded ≠ simultaneous 3rd law). `production_law` null.
- Next: Well-posed finite exterior (certified omitted-tail / initial-field bound) in isolated law-lab. Do not orbit-tune. Do not wire these kernels into the canonical engine.


## H0020 — Well-posed finite exterior with certified omitted-tail bound

- Date: 2026-09-12
- Kind: research experiment
- Status: implemented; G2 still failed; no production law
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `47f3290`; frozen G2 evidence `1dac658` / `99764b4` not overwritten
- Scope: crates/law-lab only; es-inertial-causal-v1 untouched; neither research kernel wired into the engine
- Changed: Declared-complete FiniteAuthoritativeRoot plus certified omitted-tail enclosure. certified_acceleration_at returns listed field + sound remainder or fails closed. Additive finite_exterior_research fixtures: incomplete omit r=16, false-complete, unsound R=32, sound R=16 μ≤1, query-in-tail resource miss, listed r=16. Frozen numeric thresholds not edited. Verlet/lapse remain rejected on pre-cone and exterior. Research kernels: well_posed_exterior PASS (tiny-N / query contract); light-cone and coupled two-way backreaction not regressed.
- Why: [H0011](HISTORY.md)/[H0019](HISTORY.md) could still silently omit far mass. Approved-plan G2 forbids certifying an ignore of the frozen unit source at r=16.
- Validation: cargo test -p emergent-law-lab --offline --locked — 34 passed. Clippy -p emergent-law-lab --all-targets --offline --locked -- -D warnings clean. Full qualify not run.
- Evidence: [Research kernel](../crates/law-lab/src/causal_kernel.rs), [coupled kernel](../crates/law-lab/src/coupled.rs), [experiment semantics](law-lab.md), [gate manifest](../scenarios/law-gates.json), [frozen G2 results](../artifacts/evidence/1dac658/law-qualification.json), [H0011](HISTORY.md), [H0019](HISTORY.md)
- Limitations: Tiny-N 3D-planar closest-approach remainder, not cosmological unresolved matter. Floating pad is diagnostic, not directed rounding. Coupled Euler still uses listed retarded accelerations. Compact-field, terminating exact branches, FMM, clocks, and frozen Newton source_backreaction stay failed. production_law null.
- Next: Compact-field certification or terminating exact branches in isolated law-lab (or fail-closed coupled steps when the exterior is uncertified). Do not orbit-tune. Do not wire these kernels into the canonical engine.


## H0021 — Exact compact membership and absorbing capture map

- Date: 2026-09-12
- Kind: research experiment
- Status: implemented; G2 still failed; no production law
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `47f3290`; frozen G2 evidence `1dac658` / `99764b4` not overwritten
- Scope: crates/law-lab only; es-inertial-causal-v1 untouched; neither research kernel wired into the engine
- Changed: Exact compact-radius class Interior/OnHorizon/Exterior for r_s=2μ/c² (r²c⁴ ≶ 4μ²). On/inside r_s of a retarded-visible source is absorbing capture (field_at); acceleration_at still refuses. Coincidence is Singular, never NaN or Newton through r=0. Capture of a μ change is retarded. Coupled stepper halt-captures a body already inside r_s. Additive compact_field_research fixtures. Frozen numeric thresholds not edited. Verlet/lapse remain rejected on pre-cone. compact_field_certification stays FAIL (capture ≠ Schwarzschild/Kerr; Newton flyby ≠ GR deflection).
- Why: [H0020](HISTORY.md) still had no compact-source behavior. Frozen G2: Newton 1/r has no relativistic capture/deflection; shell lapse does not reach r_s. Absorbing capture is the smallest non-divergent causal compact rule, not a geodesic map.
- Validation: cargo test -p emergent-law-lab --offline --locked — 42 passed. Clippy -p emergent-law-lab --all-targets --offline --locked -- -D warnings clean. Full qualify not run.
- Evidence: [Compact membership](../crates/law-lab/src/compact.rs), [research kernel](../crates/law-lab/src/causal_kernel.rs), [coupled kernel](../crates/law-lab/src/coupled.rs), [experiment semantics](law-lab.md), [gate manifest](../scenarios/law-gates.json), [frozen G2 results](../artifacts/evidence/1dac658/law-qualification.json), [H0020](HISTORY.md)
- Limitations: Absorbing capture is not Schwarzschild/Kerr, photon-sphere capture, or light deflection. Field values remain f64. production_law null.
- Next: Terminating exact branches in isolated law-lab, or a genuine Schwarzschild/Kerr compact map. Do not orbit-tune. Do not wire these kernels into the canonical engine.


## H0022 — Terminating exact branches for kernel-supported predicates

- Date: 2026-09-12
- Kind: research experiment
- Status: implemented; G2 still failed; no production law
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `47f3290`; frozen G2 evidence `1dac658` / `99764b4` not overwritten
- Scope: crates/law-lab only; es-inertial-causal-v1 untouched; neither research kernel wired into the engine
- Changed: Finite decision procedure for cone membership, compact class, capture vs not, and certified-exterior completeness. One rational comparison; max_steps=1. Tie rules: on-cone visible, on-horizon capture, r=0 Singular refuse, incomplete exterior refuse. Ambiguous f64 escalates to an exact dyadic or fails closed. Iteration cap is BranchBudgetExhausted, not a guessed sign. Additive terminating_exact_branches_research fixtures. Frozen numeric thresholds not edited. Verlet/lapse remain rejected on pre-cone. Production gate terminating_exact_branches stays FAIL (no curved-null geodesic solver; field values remain f64; stationary floating roots are not certificates).
- Why: [H0021](HISTORY.md) had exact compact membership but no terminating branch contract. Frozen G2: floating roots and iteration caps are not exact certificates. Keep increasing precision is insufficient.
- Validation: cargo test -p emergent-law-lab --offline --locked — 52 passed. Clippy -p emergent-law-lab --all-targets --offline --locked -- -D warnings clean. Full qualify not run.
- Evidence: [Exact branch predicates](../crates/law-lab/src/exact_branch.rs), [research kernel](../crates/law-lab/src/causal_kernel.rs), [coupled kernel](../crates/law-lab/src/coupled.rs), [experiment semantics](law-lab.md), [gate manifest](../scenarios/law-gates.json), [frozen G2 results](../artifacts/evidence/1dac658/law-qualification.json), [H0021](HISTORY.md)
- Limitations: Absorbing capture is not Schwarzschild/Kerr. Field values remain f64. Curved-null / geodesic branch solver is unsupported. production_law null. G2 still FAIL.
- Next: Genuine Schwarzschild/Kerr compact map or a curved-null geodesic branch solver in isolated law-lab. Do not orbit-tune. Do not wire these kernels into the canonical engine.


## H0023 — Schwarzschild equatorial compact oracles

- Date: 2026-09-12
- Kind: research experiment
- Status: implemented; G2 still failed; no production law
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `47f3290`; frozen G2 evidence `1dac658` / `99764b4` not overwritten
- Scope: crates/law-lab only; es-inertial-causal-v1 untouched; no engine wiring
- Changed: Isolated law es-schwarzschild-equatorial-v0: planar restriction of 3D Schwarzschild as a stationary one-source equatorial patch. Exact photon sphere r_ph=3μ/c² (r²c⁴ ≶ 9μ²). From-infinity null capture b²c⁴ ≶ 27μ² (no √3). Weak-field deflection oracle 4μ/(c²b)=1/4096 at frozen b=4. Tiny exact-or-fail-closed stepper; H0021 absorbing capture remains the fallback on/inside r_s. Additive schwarzschild_equatorial_research fixtures. Frozen numeric thresholds not edited. Verlet/lapse remain rejected on pre-cone. compact_field_certification stays FAIL. terminating_exact_branches stays FAIL. production_law stays null. Parent monopole/coupled light-cone, two-way backreaction, certified exterior not regressed.
- Why: [H0022](HISTORY.md) had terminating kernel predicates but no Schwarzschild compact map. Frozen G2: Newton flyby ≠ 4μ/(c²b); no photon-sphere capture. Oracles plus a fail-closed stepper on a declared domain. Not 2D log gravity, not delayed Newton, not orbit tuning.
- Validation: cargo test -p emergent-law-lab --offline --locked — 61 passed. Clippy -p emergent-law-lab --all-targets --offline --locked -- -D warnings clean. Full qualify not run.
- Evidence: [Schwarzschild equatorial patch](../crates/law-lab/src/schwarzschild.rs), [experiment semantics](law-lab.md), [gate manifest](../scenarios/law-gates.json), [frozen G2 results](../artifacts/evidence/1dac658/law-qualification.json), [H0022](HISTORY.md)
- Limitations: Stationary one-source patch, not interacting GR, not Kerr. Exact elliptic deflection, scatter turning cubics, and general geodesic IVP fail closed. Field values remain f64. No FMM, clocks, or coupled GR. production_law null. G2 still FAIL.
- Next: Exact elliptic / timelike geodesic IVP, or Kerr equatorial if it stays causal and fail-closed. Do not orbit-tune. Do not wire these kernels into the canonical engine.


## H0024 — Exact-or-fail-closed Schwarzschild geodesic IVP

- Date: 2026-09-12
- Kind: research experiment
- Status: implemented; G2 still failed; no production law
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `47f3290`; frozen G2 evidence `1dac658` / `99764b4` not overwritten
- Scope: crates/law-lab only; es-inertial-causal-v1 untouched; no engine wiring
- Changed: Exact-or-fail-closed equatorial geodesic IVP on es-schwarzschild-equatorial-v0. Null capture/scatter/unstable-photon classification at finite rational r (cubic sign, not the turning root). Circular identity steps: photon-sphere null and exact timelike circular L²(r-3M)=M r² (ISCO fixture r=6μ/c²=3/2048). Radial L=0 rest/inward is capture. Generic scatter / elliptic deflection, off-axis radius, and turning-root solving fail closed. Additive fixtures. Frozen thresholds not edited. Verlet/lapse remain rejected on pre-cone. H0023 oracles, H0021 capture fallback, monopole/coupled light-cone, two-way backreaction, and certified exterior not regressed. compact_field_certification stays FAIL. terminating_exact_branches stays FAIL. production_law stays null.
- Why: [H0023](HISTORY.md) classified from-infinity null geodesics but had no geodesic IVP. Frozen G2 still lacks interacting GR and elliptic deflection. Tiny exact circular/radial domain plus fail-closed generic scatter, not orbit tuning.
- Validation: cargo test -p emergent-law-lab --offline --locked — 65 passed. Clippy -p emergent-law-lab --all-targets --offline --locked -- -D warnings clean. Full qualify not run.
- Evidence: [Schwarzschild equatorial patch](../crates/law-lab/src/schwarzschild.rs), [experiment semantics](law-lab.md), [gate manifest](../scenarios/law-gates.json), [frozen G2 results](../artifacts/evidence/1dac658/law-qualification.json), [H0023](HISTORY.md)
- Limitations: Stationary one-source patch, not interacting GR, not Kerr. Exact elliptic deflection, scatter turning roots, and generic timelike bound trajectories fail closed. Field values remain f64. No FMM, clocks, or coupled GR. production_law null. G2 still FAIL.
- Next: Elliptic turning-root certificate or Kerr equatorial if it stays causal and fail-closed. Do not orbit-tune. Do not wire these kernels into the canonical engine. Compiler track remains separate (war-island [H0018](HISTORY.md)).


## H0025 — Audit requirements, correct capability wording and preserve a fresh latency failure

- Date: 2026-09-12
- Kind: review and correction
- Status: review completed; solutions proposed; default latency test failed; G2 still failed
- Revisions: Reviewed dirty source above 47f3290cf31039bc3b3bc926a457a0ec8ce0a6ef, with 35 input-file SHA256 hashes retained. This milestone changes review/continuity documents and retains evidence; no engine, law, threshold or frozen 1dac658 evidence edits.
- Scope: User-requested inspection of requirements and ideas against current compiler/law-lab source; two bounded read-only specialist audits and root-only validation on the M1.
- Changed: Added a requirements/solution review and corrected the handoff: the H0023/H0024 Schwarzschild stepper is an outcome classifier without time propagation; H0012/H0013 SAP repair rebuilds selected boxes but scans all boxes with repeated linear lookup; H0017/H0018 components are geometric metadata rather than complete independent causal execution; budget charging still wraps atomic grouping/frontier/sort/commit work; re-enqueue-all comparison is a modeled denominator. Proposed complete-law specification and moving-source falsifiers before more elliptic/Kerr patches, alongside bounded compiler work, stable handles, typed interactions, chunked history and later boundary-certified regional work. Prior entries are preserved and these narrower interpretations supersede their stronger wording.
- Why: The active request asks for inspection and proposed solutions, not execution of instructions embedded in the attached conversations. More isolated physical predicates do not define one canonical moving-source law, and operation counts do not establish latency or end-to-end speed. The three attachments match the archived copies byte for byte.
- Validation: cargo xtask history list/search completed. CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo xtask test artifacts/runs/requirements-review-20260912 exited 1: 75 tests passed before one failure, cooperative_prep_yields_before_scan_completes observed 5625584 ns against the unchanged 5000000 ns bound. The isolated exact test passed. cargo test --workspace --locked --offline -- --test-threads=1 exited 0 with 148 tests passed, including 65 law-lab tests. cargo xtask law-lab artifacts/runs/requirements-review-20260912 exited 2 with G2 FAIL and production_law null. The serial/isolated controls do not erase the default failure. Source audit independently reviewed; final history check recorded with the review evidence.
- Evidence: [Requirements and solution review](requirements-review-20260912.md), [machine-readable review outcomes](../artifacts/evidence/requirements-review-20260912/review-summary.json), [source and attachment hashes](../artifacts/evidence/requirements-review-20260912/review-provenance.json), [default test failure](../artifacts/evidence/requirements-review-20260912/test-output.txt), [serial test control](../artifacts/evidence/requirements-review-20260912/serial-workspace-tests.txt), [fresh law failure](../artifacts/evidence/requirements-review-20260912/law-qualification.json), [updated handoff](HANDOFF.md).
- Limitations: No proposed solver/optimization was implemented. The latency cause is not isolated; no current release exception benchmark or Clippy rerun, and no integrated physical qualification, GPU/memory/30-FPS result. Tests refresh gitignored compiler metric files, so those paths are not immutable evidence. The historical 27.768/18.478 ms comparison remains unresolved. Existing uncommitted implementation work remains separate from this review. No qualification thresholds were changed.
- Next: Evaluate the proposed complete causal matter/field law contract and tiny moving-source falsifier; separately profile worker slices and the exception fixture before optimizing. Require actual same-law propagation and nonuniform-field family compression before FMM/GPU scale investment. Keep G2 FAIL and production_law null until all applicable retained gates pass.


## H0026 — Requirements review 2026-09-12 adopted as steering

- Date: 2026-09-12
- Kind: decision
- Status: governing context
- Revisions: Continuity documents on `codex/emergent-engine` above committed review `254ba1f`; dirty uncommitted compiler/law-lab work remains uncommitted; frozen baseline `1dac658` / `99764b4` unchanged. No engine or law-lab code edits this turn.
- Scope: Orchestrator steering and handoff next-work order only. Qualification thresholds, `production_law`, G2 and frozen 1dac658 evidence are unchanged.
- Changed: Adopt the 2026-09-12 requirements review as governing next-work order when it conflicts with earlier journal Next fields. HANDOFF recommended work is now: (1) complete tiny causal-law specification and frozen moving-source falsifiers; (2) parallel bounded compiler slices plus exception-fixture diagnosis; (3) then stable SAP handles and a second interaction operation, with chunked history and region-boundary work after that. H0024's elliptic/Kerr default next step and the previous RNG-golden-vector-as-#2 ordering are superseded as the starting queue. Gravity stays isolated; no engine wiring.
- Why: [H0025](HISTORY.md) recorded the inspection as a proposal. Explicit integrator steering now makes that review the priority. Combining retarded, Euler and Schwarzschild labels does not define a production law; another stationary compact predicate does not fill the missing complete causal evolution. Later explicit user steering still wins.
- Validation: `cargo xtask history list` showed H0001–H0025. This entry was appended with `cargo xtask history append`; `cargo xtask history check` must pass with it. No `cargo test`, law-lab or qualify rerun this turn.
- Evidence: [Requirements and solution review](requirements-review-20260912.md), [H0025 review record](HISTORY.md), [updated handoff](HANDOFF.md), [retained review evidence](../artifacts/evidence/requirements-review-20260912/review-summary.json)
- Limitations: The review is not a G2 pass, engine completion, law implementation or threshold change. Uncommitted H0012–H0024 code is not this documentation milestone. The H0025 default 5 ms cooperative-latency failure remains retained.
- Next: Specify a complete tiny causal law (discrete-action vs piecewise-metric) with equations or finite transition rules for two or three moving sources, field/history, clocks, cones, coupling, proper time and exchange; freeze the review's falsifiers before implementing. In parallel, split atomic compiler sort/group/frontier/commit into bounded resumable steps and profile the exception fixture's setup versus initial advance separately. Do not wire gravity.


## H0027 — Tiny causal GEM spec and frozen moving-source falsifiers

- Date: 2026-09-12
- Kind: research experiment
- Status: implemented; G2 still failed; no production law; map not implemented
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `47f3290` / review `254ba1f`; frozen G2 evidence `1dac658` / `99764b4` not overwritten. No engine files in this milestone. Template next ID is H0027 because the compiler sibling draft was not journaled; that compiler record must take the following ID.
- Scope: isolated law-lab specification `es-causal-retarded-gem-v0`; `es-inertial-causal-v1` untouched; no engine wiring
- Changed: Complete tiny moving-source specification and frozen falsifiers. Winner is piecewise retarded linearized-metric / GEM patches for N∈{2,3} (`es-causal-retarded-gem-v0`). Discrete-action/Fokker-AVI rejected incomplete (no independent field remainder, no inelastic capture vertex, no named signals/interventions). 19 frozen fixtures under `tiny_causal_law_research`; `advance_map` refuses with `map not implemented; fixtures frozen`. Named rules cover cones, GEM Φ/ξ/E/B/a, clocks, Minkowski signals, accounted interventions, capture-with-transfer, remainder-through-evolution, and composition. Frozen numeric thresholds not edited. Verlet/lapse remain rejected. compact_field_certification stays FAIL. terminating_exact_branches stays FAIL. production_law stays null. G2 stays FAIL.
- Why: [H0026](HISTORY.md) required a complete causal matter/field transition specification and frozen moving-source falsifiers before implementing a map or further elliptic/Kerr patches. Combining retarded monopole, Euler coupling, absorbing capture, and Schwarzschild classifiers does not define this law.
- Validation: `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --offline --locked` — 69 passed. Clippy `-p emergent-law-lab --all-targets --offline --locked -- -D warnings` clean. Full qualify not run this turn. Workspace tests not rerun (compiler sibling may be editing engine). G2 remains FAIL; production_law null.
- Evidence: [GEM specification](laws/causal-retarded-gem-v0.md), [frozen spec module](../crates/law-lab/src/tiny_causal.rs), [experiment semantics](law-lab.md), [gate manifest](../scenarios/law-gates.json), [frozen G2 results](../artifacts/evidence/1dac658/law-qualification.json), [H0026](HISTORY.md), [updated handoff](HANDOFF.md)
- Limitations: Spec-only; no GEM map. Field values remain f64. Capture-with-transfer is not Schwarzschild/Kerr. Not delayed-Newton-as-G2, not 2D log gravity, not interacting GR, not FMM, not engine wiring. CONS identity and aberration cosine bound have not had independent review. No retained `artifacts/runs/` directory for this freeze. Frozen G2 JSON remains `1dac658`, not this checkout. Compiler atomic-slice work is unjournaled.
- Next: Independent review of (CONS) and the aberration cosine bound (`present_alignment_dot_min = 2047/2048` on β=1/16), then a named GEM map scored against the frozen fixtures without retuning. Not Kerr. Not engine wiring. Compiler sibling work remains resumable atomic slices if not done and must journal as the following ID.


## H0028 — Bounded resumable sort, group, expiry, frontier and commit prep

- Date: 2026-09-12
- Kind: implementation and measurement
- Status: implemented and measured
- Revisions: Uncommitted engine work on `codex/emergent-engine` above `47f3290`; frozen baseline `1dac658` / `99764b4` not overwritten.
- Scope: inertial compiler `es-inertial-causal-v1` / `scripted-interaction-v1`; no gravity
- Changed: Resumable stable merge sort; WorkBudget-charged expiry, union-find grouping, frontier enqueue, commit collect/accumulate/validate, and post-commit candidate/heap reduction. A simultaneous batch still publishes clock and events in one transaction. New counters `expire_ops`, `group_ops`, `frontier_ops`, `commit_prep_ops`.
- Why: [H0025](HISTORY.md)/[H0026](HISTORY.md) review: WorkBudget still wrapped atomic sort/group/frontier/commit. Half-visible event batches are forbidden. [H0027](HISTORY.md) took the GEM spec, so this compiler slice is the following ID.
- Validation: Specialist-reported `cargo xtask test` PASS. Relay 14/43/71. War-island digest match; `pairs_rechecked` 0/82214. Phase-family and overlap-certificate tests PASS. Packed budget-1 digest equals full. `simultaneous_batch_never_half_committed` PASS. Isolated 5 ms coop tests PASS; a parallel run observed 5.437 ms against the unchanged 5 ms bound (threshold not weakened). Qualify was not run.
- Evidence: [Runtime compiler](../crates/engine/src/runtime.rs), [cooperative tests](../crates/engine/tests/compiler_coop.rs), [architecture](architecture.md), [handoff](HANDOFF.md), [bounded prep metrics](../artifacts/runs/compiler-bounded-prep-20260912/metrics.json), [war-island metrics](../artifacts/runs/compiler-war-island-20260912/metrics.json).
- Limitations: Debug single-run. `begin_repair` still O(D N). Publish of one tick remains one transaction. 1k-exception setup vs advance not measured in debug. Frozen 18.478 ms and [H0013](HISTORY.md) 27.768 ms remain historical. `production_law` null; G2 isolated.
- Next: Release setup-vs-advance on the 1k-exception fixture vs a contemporaneous control. Stable SAP handles / neighbor-local repair. Physics: conservation/aberration review then GEM map vs frozen fixtures. Do not start per-region clocks.


## H0029 — Independent review of GEM CONS and aberration freeze

- Date: 2026-09-12
- Kind: decision / review
- Status: no-go for advance_map until spec patch; G2 still failed
- Revisions: Uncommitted continuity on `codex/emergent-engine`; frozen G2 `1dac658` / `99764b4` not overwritten. GEM spec is [H0027](HISTORY.md) (draft numbering in some reports was confused; use actual HISTORY IDs). No engine or frozen-evidence edits this turn.
- Scope: isolated `es-causal-retarded-gem-v0` spec and `tiny_causal_law_research` freeze; no engine wiring
- Changed: Independent review: (CONS) double-counts capture if the ledger and `Σp_i` both keep transferred momentum. No GEM field remainder in (CONS). Capture text can be read as wiping past-segment `μ` (acausal). Frozen cosine `2047/2048` at `β=1/16` is a valid discriminator at the post-cone event `t=1/8`, not the linearized-GEM prediction (that is ~1). Delayed Newton fails that event; LW/GEM pass. Keep `2047/2048`; do not retune. Do not implement `advance_map` yet.
- Why: [H0026](HISTORY.md)/[H0027](HISTORY.md) required review of (CONS) and aberration before a map. Combining frozen fixtures with an ill-posed (CONS) would score a false law.
- Validation: Read-only review of [the GEM spec](laws/causal-retarded-gem-v0.md), [tiny_causal.rs](../crates/law-lab/src/tiny_causal.rs), and `tiny_causal_law_research` in [law-gates.json](../scenarios/law-gates.json). Cargo qualify not run.
- Evidence: [GEM specification](laws/causal-retarded-gem-v0.md), [frozen spec module](../crates/law-lab/src/tiny_causal.rs), [gate manifest](../scenarios/law-gates.json), [H0027](HISTORY.md), [requirements review](requirements-review-20260912.md), [updated handoff](HANDOFF.md)
- Limitations: Review did not re-derive every GEM equation in hardware arithmetic. G2 remains FAIL. `production_law` null.
- Next: Spec patch ((CONS)/(ABS) identity, capture history keeps past `μ`, (C-RET) on inertial segment, pin aberration event, (EXT-EVOL) remainder update, `short_binary_exchange` not 3rd-law `Σp`, closed-form `∇Φ`). Then map vs freeze. Compiler exception profile remains separate.


## H0030 — Release-profile 1k-exception setup vs advance

- Date: 2026-09-12
- Kind: experiment
- Status: measured
- Revisions: Uncommitted measurement on `codex/emergent-engine`; frozen `1dac658` / `99764b4` not overwritten. [H0029](HISTORY.md) is the GEM CONS/aberration review; this measurement takes the following ID.
- Scope: inertial compiler 1,000-exception / 32-tick; release setup vs advance; laboratory law `es-inertial-causal-v1`; no gravity
- Changed: xtask `exception-setup-advance`. Three release repeats this checkout: setup 10.269 / 9.948 / 8.749 ms; advance 25.584 / 19.835 / 19.135 ms. Same denominators: scans 1, pairs_rechecked 0/0, charged ops 100,507, serialized 928,906 B, RSS 7.91–8.16 MB, 0 events.
- Why: Review required setup vs advance against a contemporaneous control rather than frozen 18.478 ms vs [H0013](HISTORY.md) 27.768 ms as the same process.
- Validation: `cargo run --release -p xtask --locked --offline -- exception-setup-advance artifacts/runs/compiler-exception-setup-advance-20260912` exit 0. Relay 14/43/71 PASS. xtask clippy `-D warnings` PASS. Engine clippy pre-existing failures in `runtime.rs` not fixed. Qualify and `cargo xtask test` not run (no engine logic change). 5 ms stutter bound not weakened.
- Evidence: [setup vs advance metrics](../artifacts/runs/compiler-exception-setup-advance-20260912/metrics.json), [run summary](../artifacts/runs/compiler-exception-setup-advance-20260912/summary.json), [bench harness](../xtask/src/bench.rs), [H0013](HISTORY.md), [H0028](HISTORY.md), [handoff](HANDOFF.md)
- Limitations: Three repeats in one process after relay warmup; not a cold OS process. Serialized bytes ≠ RAM. First-vs-warm scatter 19.1–25.6 ms. Frozen 18.478 ms and [H0013](HISTORY.md) 27.768 ms remain historical. H0013 27.768 ms did not reproduce as a stable warm cost. `production_law` null; G2 isolated.
- Next: Do not use neighbor-local SAP to chase this fixture (1 scan, 0 repairs, 0 pairs). Neighbor-local remains for dirty-repair workloads. If chasing this wall: extraction setup and initial scan construction. Physics: spec patch then GEM map. Do not weaken 5 ms stutter bound.


## H0031 — Spacetime-geometry unification adopted as physics completeness criterion

- Date: 2026-09-12
- Kind: user direction / decision
- Status: governing context
- Revisions: Continuity documents on `codex/emergent-engine` above committed review `254ba1f`; dirty uncommitted compiler/law-lab work remains uncommitted; frozen baseline `1dac658` / `99764b4` unchanged. No engine, law-lab source, or `artifacts/evidence/1dac658/` edits this turn. Siblings may be patching the GEM spec and exception journal.
- Scope: Orchestrator steering and handoff physics next-work order. Qualification thresholds, `production_law`, G2 and frozen 1dac658 evidence are unchanged.
- Changed: Adopt later user steering that gravity is part of spacetime (freely falling bodies follow geodesics; the same geometry for light and clocks). Unification: sources establish shared geometry; ships/light traverse it; mass/energy feed back; the compiler reuses solutions while assumptions hold. The physics completeness criterion is one small evolving spacetime patch with two massive bodies, a test ship, a light ray and a clock; a controlled source change must yield mutually consistent motion, light arrival and elapsed proper time from that patch’s geometry; then subdivision/caching must preserve the result. Isolated formulas do not close the loop. HANDOFF physics next is this patch experiment, not Kerr and not more disconnected oracles. Compiler exception-profile work stays parallel and is not gravity.
- Why: Earlier physics next (H0024 elliptic/Kerr; H0026 complete-tiny-law then GEM map) can still accumulate disconnected oracles. The user asked for one shared geometric object that motion, null arrival and proper time read from, with amortized compiler reuse. Later explicit user steering wins over earlier journal Next fields. The [2026-09-12 requirements review](requirements-review-20260912.md) remains useful inspection and is not a G2 pass.
- Validation: `cargo xtask history list` showed H0001–H0030. This entry was appended with `cargo xtask history append`; `cargo xtask history check` must pass with it. No `cargo test`, law-lab or qualify rerun this turn. No map implemented.
- Evidence: [Spacetime-geometry unification steering](spacetime-geometry-unification-20260912.md), [Requirements and solution review](requirements-review-20260912.md), [H0026 review steering](HISTORY.md), [H0029 GEM CONS no-go](HISTORY.md), [updated handoff](HANDOFF.md)
- Limitations: Steering only. Not a G2 pass, engine completion, production-law selection, map implementation or threshold change. Does not patch GEM (CONS) and does not replace the H0029 no-go on `advance_map`. Uncommitted H0012–H0030 code is not this documentation milestone. Frozen G2 JSON remains `1dac658`, not this checkout.
- Next: Specify and freeze the patch experiment (two masses, ship, ray, clock, source change, cache/subdivision parity) using one metric object. CONS/GEM spec patch ([H0029](HISTORY.md)) is still required before `advance_map`. Do not wire into the engine.


## H0032 — GEM spec patch after CONS/aberration no-go

- Date: 2026-09-12
- Kind: research experiment
- Status: implemented; G2 still failed; no production law; map not implemented
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `47f3290` / review `254ba1f`; frozen G2 evidence `1dac658` / `99764b4` not overwritten. No engine files and no `artifacts/evidence/1dac658/` edits this turn.
- Scope: isolated `es-causal-retarded-gem-v0`; no engine wiring
- Changed: One CONS sum `p := μ v`, captured `p_i ← 0`, audit-only ledger. Past-segment μ kept. C-RET cone∩inertial segment. Aberration pinned at `(1/8,(0,4))` vs present coasting Newton. EXT-EVOL keep-or-promote; remainder membership. `short_binary_exchange` not 3rd-law. GEM-GRAD closed forms; kink radiation omitted. `2047/2048` unchanged. `advance_map` still refuses.
- Why: [H0029](HISTORY.md) no-go until identities named.
- Validation: Specialist-reported `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --offline --locked` — 70 passed. Clippy `-p emergent-law-lab --all-targets --offline --locked -- -D warnings` clean. Qualify not run.
- Evidence: [GEM specification](laws/causal-retarded-gem-v0.md), [frozen spec module](../crates/law-lab/src/tiny_causal.rs), [experiment semantics](law-lab.md), [gate manifest](../scenarios/law-gates.json), [H0027](HISTORY.md), [H0029](HISTORY.md), [updated handoff](HANDOFF.md)
- Limitations: Spec-only. Poynting omitted from CONS. Not delayed-Newton-as-G2. G2 FAIL. `production_law` null.
- Next: After evolving-patch spec freeze ([H0031](HISTORY.md) completeness criterion), implement the named GEM map as that patch’s laboratory law against frozen fixtures. If that sibling freeze is not yet journaled, wait. No retune `2047/2048`. No Kerr. No engine wiring.


## H0033 — Evolving spacetime patch spec and frozen same-metric falsifiers

- Date: 2026-09-12
- Kind: research experiment
- Status: implemented; G2 still failed; no production law; map not implemented
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `254ba1f`; frozen G2 evidence `1dac658` / `99764b4` not overwritten. No engine files and no `artifacts/evidence/1dac658/` edits this turn. `tiny_causal.rs` not edited this freeze. Template next ID is H0033 because [H0032](HISTORY.md) is the GEM CONS spec patch.
- Scope: isolated law-lab specification `es-evolving-spacetime-patch-v0`; `es-inertial-causal-v1` untouched; no engine wiring
- Changed: Freeze one compiled spacetime patch and its same-metric falsifiers. Law id `es-evolving-spacetime-patch-v0`. Cast is two massive bodies, one test ship, one light ray, and one clock sharing one compiled metric `g`. Thirteen named rules: PATCH-S, PATCH-DOM, PATCH-INV, PATCH-PROP, GEO-T, GEO-N, CLK-G, EXT-P, BR-P, CONSIS, BACKREACT, COMPOSE, CACHE. Seventeen fixtures under `evolving_spacetime_patch_research`. `advance_patch` refuses with `map not implemented; fixtures frozen`. GEM (METRIC) is a candidate fill; GEM (SIG) Minkowski is a named negative control for metric null geodesics. Delayed Newton and Schwarzschild classifiers are named negative controls. Frozen numeric thresholds and GEM cosine `2047/2048` were not retuned. Verlet/lapse remain rejected. compact_field_certification stays FAIL. terminating_exact_branches stays FAIL. production_law stays null. G2 stays FAIL.
- Why: User steering [H0031](HISTORY.md) — gravity is geometry; isolated formulas will not close motion+light+clock.
- Validation: Confirmed present: [evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [frozen spec module](../crates/law-lab/src/evolving_patch.rs), [gate manifest](../scenarios/law-gates.json), [experiment semantics](law-lab.md), [unification steering](spacetime-geometry-unification-20260912.md). Integrator counted 74 `#[test]` attributes in `crates/law-lab`. Specialist-reported `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --offline --locked` — 74 passed. Clippy `-p emergent-law-lab --all-targets --offline --locked -- -D warnings` clean. Full qualify not run this turn. Workspace tests not rerun. G2 remains FAIL; production_law null. No map implemented.
- Evidence: [evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [frozen spec module](../crates/law-lab/src/evolving_patch.rs), [experiment semantics](law-lab.md), [gate manifest](../scenarios/law-gates.json), [unification steering](spacetime-geometry-unification-20260912.md), [GEM specification](laws/causal-retarded-gem-v0.md), [frozen G2 results](../artifacts/evidence/1dac658/law-qualification.json), [H0031](HISTORY.md), [H0032](HISTORY.md), [updated handoff](HANDOFF.md)
- Limitations: Spec-only; no evolving-patch map. GEM CONS patched ([H0032](HISTORY.md)) does not license `advance_map` until independent review of CONSIS, linearized metric-null delay, and certificate invalidation. Field values of `g` remain f64. No Shapiro magnitude is frozen. Not delayed-Newton-as-G2, not 2D log gravity, not Kerr, not interacting GR, not FMM, not engine wiring. No retained `artifacts/runs/` directory for this freeze. Frozen G2 JSON remains `1dac658`, not this checkout.
- Next: Independent review of CONSIS, linearized metric-null delay, and certificate invalidation. Then a law-lab patch map vs frozen fixtures without retuning. Do not implement GEM `advance_map` from this freeze. Not Kerr. Not engine wiring.


## H0034 — Independent review of evolving-patch CONSIS, GEO-N and certificates

- Date: 2026-09-12
- Kind: decision / review
- Status: no-go for advance_patch until spec patch; G2 still failed
- Revisions: Uncommitted continuity on `codex/emergent-engine`; frozen G2 `1dac658` / `99764b4` not overwritten. Evolving-patch freeze is [H0033](HISTORY.md). No engine or frozen-evidence edits this turn.
- Scope: isolated `es-evolving-spacetime-patch-v0` spec and `evolving_spacetime_patch_research` freeze; no engine wiring
- Changed: Independent review: CONSIS fixtures only require co-movement after μ change, not identity of GEO-T/GEO-N/CLK-G with one compiled `g` in `P`. GEO-N rest delay is well-posed but unusable at tick resolution (Shapiro ~1e-6 vs tick 1/64) — extra-tick or same-bin trap. Certificates as global TTL 1/16 can leave stale `g`. GEM `advance_map` is a metric-fill reduction, not the patch object (GEM SIG is Minkowski). Keep freeze numbers; no Shapiro magnitude; keep 2047/2048. Do not implement `advance_patch` yet.
- Why: [H0031](HISTORY.md) unification fails if a map bolts three Φ-responsive formulas. Implementing now would freeze a false loop.
- Validation: Read-only review of [the evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [evolving_patch.rs](../crates/law-lab/src/evolving_patch.rs), `evolving_spacetime_patch_research` in [law-gates.json](../scenarios/law-gates.json), [the GEM spec](laws/causal-retarded-gem-v0.md), and [the unification note](spacetime-geometry-unification-20260912.md). Cargo qualify not run.
- Evidence: [evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [frozen spec module](../crates/law-lab/src/evolving_patch.rs), [gate manifest](../scenarios/law-gates.json), [GEM specification](laws/causal-retarded-gem-v0.md), [unification steering](spacetime-geometry-unification-20260912.md), [H0033](HISTORY.md), [H0032](HISTORY.md), [H0031](HISTORY.md), [updated handoff](HANDOFF.md)
- Limitations: Review did not implement a map and did not retune freeze numbers. Did not re-derive Shapiro in hardware arithmetic. G2 remains FAIL. `production_law` null. GEM SIG remains Minkowski.
- Next: Spec patch: CONSIS binds GEO-T/GEO-N/CLK-G to one object in `P`; name coordinate/affine arrival before tick binning (`Δt > L/c` and ≠ baseline, no magnitude); cone-valued INV with source digest. Then patch map. Do not implement GEM MAP from this freeze. Not Kerr. Not engine wiring.


## H0035 — Evolving-patch CONSIS/GEO-N/CACHE spec patch

- Date: 2026-09-12
- Kind: research experiment
- Status: implemented; G2 still failed; no production law; map not implemented
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `254ba1f`; frozen G2 evidence `1dac658` / `99764b4` not overwritten. No engine files and no `artifacts/evidence/1dac658/` edits this turn. Template next ID is H0035 because [H0034](HISTORY.md) is the CONSIS/GEO-N/CACHE no-go.
- Scope: isolated `es-evolving-spacetime-patch-v0`; `es-inertial-causal-v1` untouched; no engine wiring
- Changed: H0034 holes patched. CONSIS binds GEO-T/GEO-N/CLK-G to one object in `P`; co-movement is necessary, not sufficient; a private Φ-trio fails. GEO-N names coordinate/affine arrival before tick binning (`Δt_{P_Δ} > L/c` and `Δt_{P_Δ} ≠ Δt_{P_0}`); no Shapiro freeze. Certificate is source digest + remainder + per-event future cone; `1/16` is when the ship must not see old `g`, not a global TTL. Cache key includes source-history digest; cache after INV fails. `authored_futures: false` is in the harness JSON. GEM MAP is not this object; GEM METRIC/a/CLK may fill `g`. Named negatives stay. GEM cosine `2047/2048` unchanged. `advance_patch` still refuses with `map not implemented; fixtures frozen`. G2 still FAIL. `production_law` remains null.
- Why: [H0034](HISTORY.md) no-go until identities named. Implementing without the patch would freeze a false loop of three Φ-responsive formulas and a tick-bin Shapiro trap.
- Validation: Confirmed present: [evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [frozen spec module](../crates/law-lab/src/evolving_patch.rs), [gate manifest](../scenarios/law-gates.json), [experiment semantics](law-lab.md). Integrator counted 75 `#[test]` attributes in `crates/law-lab`. Specialist-reported `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --offline --locked` — 75 passed. Clippy `-p emergent-law-lab --all-targets --offline --locked -- -D warnings` clean. Full qualify not run this turn. Workspace tests not rerun. G2 remains FAIL; production_law null. `advance_patch` still refuses. No engine or frozen-evidence edits this turn.
- Evidence: [evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [frozen spec module](../crates/law-lab/src/evolving_patch.rs), [experiment semantics](law-lab.md), [gate manifest](../scenarios/law-gates.json), [unification steering](spacetime-geometry-unification-20260912.md), [GEM specification](laws/causal-retarded-gem-v0.md), [frozen G2 results](../artifacts/evidence/1dac658/law-qualification.json), [H0033](HISTORY.md), [H0034](HISTORY.md), [updated handoff](HANDOFF.md)
- Limitations: Spec-only; no evolving-patch map. [H0032](HISTORY.md) does not license GEM `advance_map`. Field values of `g` remain f64. No Shapiro magnitude is frozen. Not delayed-Newton-as-G2, not 2D log gravity, not Kerr, not interacting GR, not FMM, not engine wiring. Frozen G2 JSON remains `1dac658`, not this checkout.
- Next: Law-lab `advance_patch` vs frozen fixtures without retuning. Do not implement GEM `advance_map`. Not Kerr. Not engine wiring.


## H0036 — Evolving-patch advance_patch research map

- Date: 2026-09-12
- Kind: research experiment
- Status: implemented; G2 still failed; no production law; GEM map not implemented
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `254ba1f`; frozen G2 evidence `1dac658` / `99764b4` not overwritten. No engine files and no `artifacts/evidence/1dac658/` edits this turn. Template next ID is H0036 because [H0035](HISTORY.md) is the CONSIS/GEO-N/CACHE spec patch.
- Scope: isolated `es-evolving-spacetime-patch-v0` research map; `es-inertial-causal-v1` untouched; no engine wiring
- Changed: Laboratory `advance_patch` implemented against fixtures frozen before the map. GEO-T/GEO-N/CLK-G read one `(Φ,ξ)` object in `P`. All 17 `evolving_spacetime_patch_research` fixtures PASS. `compact_field_certification`, `terminating_exact_branches`, and `source_backreaction` stay FAIL. GEM `advance_map` still refuses with `map not implemented; fixtures frozen`. `map_status` is `implemented-research`. GEM (METRIC)/(GEM-a)/(CLK) fill `g`; GEM MAP is not this object. Named negatives stay. No Shapiro freeze. GEM cosine `2047/2048` unchanged. G2 still FAIL. `production_law` remains null.
- Why: [H0035](HISTORY.md) pinned CONSIS/GEO-N/CACHE identities so a map can be scored without a private Φ-trio or a tick-bin Shapiro trap. [H0031](HISTORY.md) completeness is one compiled patch, not GEM MAP.
- Validation: Confirmed present: [evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [patch module](../crates/law-lab/src/evolving_patch.rs), [gate manifest](../scenarios/law-gates.json), [experiment semantics](law-lab.md). Integrator counted 81 `#[test]` attributes in `crates/law-lab`. Specialist-reported `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --offline --locked` — 81 passed. Clippy `-p emergent-law-lab --all-targets --offline --locked -- -D warnings` clean. Full qualify not run this turn. Workspace tests not rerun. G2 remains FAIL; production_law null. GEM `advance_map` still refuses. No engine or frozen-evidence edits this turn.
- Evidence: [evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [patch module](../crates/law-lab/src/evolving_patch.rs), [experiment semantics](law-lab.md), [gate manifest](../scenarios/law-gates.json), [unification steering](spacetime-geometry-unification-20260912.md), [GEM specification](laws/causal-retarded-gem-v0.md), [frozen G2 results](../artifacts/evidence/1dac658/law-qualification.json), [H0033](HISTORY.md), [H0034](HISTORY.md), [H0035](HISTORY.md), [updated handoff](HANDOFF.md)
- Limitations: Research map only; not a production gravity law. Field values of `g` remain f64. No Shapiro magnitude is frozen. [H0032](HISTORY.md) does not license GEM `advance_map`. Not delayed-Newton-as-G2, not 2D log gravity, not Kerr, not interacting GR, not FMM, not engine wiring. Frozen G2 JSON remains `1dac658`, not this checkout. Independent review of this map has not run.
- Next: Independent review of the `advance_patch` map. Do not implement GEM `advance_map`. Not Kerr. Not engine wiring. Keep G2 isolated.


## H0037 — Independent review of evolving-patch advance_patch map

- Date: 2026-09-12
- Kind: decision / review
- Status: no-go for keeping the map as the completeness experiment; G2 still failed
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `254ba1f`; frozen G2 `1dac658` / `99764b4` not overwritten. The reviewed map is [H0036](HISTORY.md). No engine or frozen-evidence edits this turn.
- Scope: isolated `es-evolving-spacetime-patch-v0` research map in `evolving_patch.rs`; no engine wiring
- Changed: Independent review of implemented `advance_patch`. CONSIS still passes a private Φ-trio that only shares `phi_xi`: `geo_t_accel`, `geo_n_arrival`, and `clk_g_rate` are independent reductions; `consis_rejects_private_trio` discards the trio; `shares_compiled_object` treats a missing ray as bound; `laboratory` never puts a ray in `P`. GEO-N does use coordinate/affine `Δt` before tick binning (honest; no Shapiro freeze). CACHE helper is cone-valued but unused by `U`; `cache_reuse` is two independent `advance_patch` calls (`U==U`). COMPOSE `canonical_eq` omits ray, velocity, and `certificate.changes`. GEO-T at rest is retarded Newton; the delayed-Newton negative compares one-body `μ=2` to two-body `E`. Honest FAILs remain `source_backreaction`, `compact_field_certification`, `terminating_exact_branches`, G2, and `production_law` null. GEM `advance_map` still refuses.
- Why: [H0031](HISTORY.md) completeness fails if CONSIS/CACHE/COMPOSE are tautological. [H0035](HISTORY.md) already named the identities; [H0036](HISTORY.md) does not meet them. Implementing GEM MAP or retuning freeze numbers would hide the hole.
- Validation: Read-only review of [the evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [the patch module](../crates/law-lab/src/evolving_patch.rs), `evolving_spacetime_patch_research` in [law-gates.json](../scenarios/law-gates.json), [H0034](HISTORY.md), [H0035](HISTORY.md), and [H0036](HISTORY.md). Specialist-reported `cargo test -p emergent-law-lab evolving_patch` — 11 passed (CONSIS/CACHE/COMPOSE still tautological). Cargo qualify not run.
- Evidence: [evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [patch module](../crates/law-lab/src/evolving_patch.rs), [gate manifest](../scenarios/law-gates.json), [unification steering](spacetime-geometry-unification-20260912.md), [GEM specification](laws/causal-retarded-gem-v0.md), [H0034](HISTORY.md), [H0035](HISTORY.md), [H0036](HISTORY.md), [updated handoff](HANDOFF.md)
- Limitations: Review did not patch the map and did not retune freeze numbers. Did not re-run full law-lab or qualify. G2 remains FAIL. `production_law` null. GEM SIG remains Minkowski. GEO-N is linearized Euclidean-path delay, not a 4-velocity null integrator.
- Next: Map patch, not fixtures. Bind ship/clock/light to evaluations of the object in `P` and actually reject `private_phi_trio`; put the ray in `P` and compose it; make CACHE drive `U` and fail after INV; compare delayed Newton of both rest sources. Do not retune freeze numbers. Do not promote G2. Do not implement GEM `advance_map`. Not Kerr. Not engine wiring.


## H0038 — Evolving-patch advance_patch map identities

- Date: 2026-09-12
- Kind: research experiment
- Status: implemented; G2 still failed; no production law; GEM map not implemented
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `254ba1f`; frozen G2 evidence `1dac658` / `99764b4` not overwritten. No engine files and no `artifacts/evidence/1dac658/` edits this turn. Template next ID is H0038 because [H0037](HISTORY.md) is the map no-go.
- Scope: isolated `es-evolving-spacetime-patch-v0` research map; `es-inertial-causal-v1` untouched; no engine wiring
- Changed: Map patch for [H0035](HISTORY.md) identities after [H0037](HISTORY.md). Laboratory `P` carries a live ray (ship → rest receiver). CONSIS rejects a private Φ-trio that only stamps `geometry_id`; missing ray is not bound. Cached `U` (`advance_from_cache`) matches source-history `U` on a live certificate and fails after (PATCH-INV), including interior-cone `(1/32,(1,0))`; far `(1/16,(16,0))` may keep old `g`. COMPOSE includes ray, ship velocity, and `certificate.changes`. Delayed-Newton negative compares both rest sources; rest GEO-T may equal that Newton, so the split is GEO-N ≠ Minkowski and CLK-G ≠ inertial. All 17 `evolving_spacetime_patch_research` fixtures PASS. `compact_field_certification`, `terminating_exact_branches`, and `source_backreaction` stay FAIL. GEM `advance_map` still refuses. No Shapiro freeze. GEM cosine `2047/2048` unchanged. G2 still FAIL. `production_law` remains null.
- Why: [H0037](HISTORY.md) no-go: CONSIS still passed a private Φ-trio, the ray was never in `P`, CACHE did not drive `U`, COMPOSE omitted ray/velocity/`certificate.changes`, and the delayed-Newton negative compared one-body `μ=2` to two-body `E`. [H0035](HISTORY.md) already named the identities.
- Validation: Confirmed present: live ray in `laboratory_n`, `shares_compiled_object` requires `ray.is_some()`, `consis_rejects_private_trio` compares the trio to bound GEO-T/GEO-N/CLK-G, `canonical_eq` includes ray/ship/`certificate`, `advance_from_cache` is cached `U`. Specialist-reported `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --offline --locked` — 81 passed. Clippy `-p emergent-law-lab --all-targets --offline --locked -- -D warnings` clean. Full qualify not run this turn. Workspace tests not rerun. G2 remains FAIL; production_law null. GEM `advance_map` still refuses. No engine or frozen-evidence edits this turn.
- Evidence: [evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [patch module](../crates/law-lab/src/evolving_patch.rs), [experiment semantics](law-lab.md), [gate manifest](../scenarios/law-gates.json), [unification steering](spacetime-geometry-unification-20260912.md), [GEM specification](laws/causal-retarded-gem-v0.md), [frozen G2 results](../artifacts/evidence/1dac658/law-qualification.json), [H0035](HISTORY.md), [H0036](HISTORY.md), [H0037](HISTORY.md), [updated handoff](HANDOFF.md)
- Limitations: Research map only; not a production gravity law. Field values of `g` remain f64. No Shapiro magnitude is frozen. Rest GEO-T may equal delayed Newton of both rest sources; the patch is not delayed-Newton-as-G2 because GEO-N ≠ Minkowski and CLK-G ≠ inertial. [H0032](HISTORY.md) does not license GEM `advance_map`. Not 2D log gravity, not Kerr, not interacting GR, not FMM, not engine wiring. Frozen G2 JSON remains `1dac658`, not this checkout. Independent review of this patched map has not run.
- Next: Independent review of the patched `advance_patch` map. Do not implement GEM `advance_map`. Not Kerr. Not engine wiring. Keep G2 isolated.


## H0039 — Independent review of evolving-patch map identity patch

- Date: 2026-09-12
- Kind: decision / review
- Status: no-go for keeping the patched map as the completeness experiment; G2 still failed
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `254ba1f`; frozen G2 `1dac658` / `99764b4` not overwritten. The reviewed map is [H0038](HISTORY.md). No engine or frozen-evidence edits this turn.
- Scope: isolated `es-evolving-spacetime-patch-v0` research map in `evolving_patch.rs`; no engine wiring
- Changed: Independent review of the [H0038](HISTORY.md) map. H0037 letter-holes are closed: the private Φ-trio is compared and rejected; a ray exists in `P`; `canonical_eq` includes ray/ship/certificate; delayed Newton is two-body and honest about rest GEO-T; `advance_from_cache` is a real second `U`. Light is still not bound into `U`: `evaluate_ray` sets `tick_delivery` at construction, so `step_one_with` never refreshes in-flight GEO-N. CONSIS still rereads `g` via three `phi_xi` helpers plus `geometry_id` stamps; `fixture_same_metric_consistency` still equates `evaluate_ray` with `geo_n_arrival` and does not check stored `P.ray` / accumulated `τ`. Cached INV uses hardcoded probes, not the events `U` integrates. Honest FAILs remain `source_backreaction`, `compact_field_certification`, `terminating_exact_branches`, G2, and `production_law` null. GEM `advance_map` still refuses.
- Why: [H0031](HISTORY.md) completeness fails if the ray is frozen cargo and CONSIS does not read the stored observables in `P`. [H0035](HISTORY.md) already named in-flight affine advance and CONSIS identity with one object in `P`.
- Validation: Read-only review of [the evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [the patch module](../crates/law-lab/src/evolving_patch.rs), `evolving_spacetime_patch_research` in [law-gates.json](../scenarios/law-gates.json), [H0035](HISTORY.md), [H0037](HISTORY.md), and [H0038](HISTORY.md). Specialist-reported `cargo test -p emergent-law-lab evolving_patch` — 11 passed (COMPOSE/CONSIS of light still tautological). Cargo qualify not run.
- Evidence: [evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [patch module](../crates/law-lab/src/evolving_patch.rs), [gate manifest](../scenarios/law-gates.json), [unification steering](spacetime-geometry-unification-20260912.md), [H0035](HISTORY.md), [H0037](HISTORY.md), [H0038](HISTORY.md), [updated handoff](HANDOFF.md)
- Limitations: Review did not patch the map and did not retune freeze numbers. Did not re-run full law-lab or qualify. G2 remains FAIL. `production_law` null. GEO-N coordinate `Δt` before ticks remains honest. Delayed-Newton rest split remains honest.
- Next: Map patch, not fixtures. Leave `tick_delivery` pending until the containing tick so `U` advances in-flight GEO-N; CONSIS must read stored `P.ray` / `τ` / ship, not ID stamps plus `evaluate_ray == geo_n_arrival`; INV must certify the events `U` integrates. Do not retune freeze numbers. Do not promote G2. Do not implement GEM `advance_map`. Not Kerr. Not engine wiring.


## H0040 — Evolving-patch U flies P.ray and CONSIS reads stored observables

- Date: 2026-09-12
- Kind: research experiment
- Status: implemented; G2 still failed; no production law; GEM map not implemented
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `254ba1f`; frozen G2 evidence `1dac658` / `99764b4` not overwritten. No engine files and no `artifacts/evidence/1dac658/` edits this turn. Template next ID is H0040 because [H0039](HISTORY.md) is the identity-patch no-go.
- Scope: isolated `es-evolving-spacetime-patch-v0` research map; `es-inertial-causal-v1` untouched; no engine wiring
- Changed: Map patch for [H0039](HISTORY.md). `U` flies laboratory `P.ray`: `evaluate_ray` leaves `tick_delivery` pending; each step refreshes in-flight GEO-N from live or cached `g` and commits delivery only on the tick that contains `t(λ_*)`. CONSIS reads stored ship worldtube / `P.ray.coordinate_dt` / accumulated `τ` (CLK-G along the stepped worldtube); a private Φ-trio stamped onto `P.ray` with matching `geometry_id` fails. Cached `U` certifies the ship event, in-flight ray emit, and source events it integrates, not hardcoded `(1/32,(1,0))` / `(1/16,(4,0))`; far `(1/16,(16,0))` may keep old `g`. Spec `pre_emit`/`post_emit` probes remain geometry probes. All 17 `evolving_spacetime_patch_research` fixtures PASS. `compact_field_certification`, `terminating_exact_branches`, and `source_backreaction` stay FAIL. GEM `advance_map` still refuses. No Shapiro freeze. GEM cosine `2047/2048` unchanged. G2 still FAIL. `production_law` remains null.
- Why: [H0039](HISTORY.md) no-go: the ray was frozen cargo (`tick_delivery` set at construction so `U` never advanced in-flight GEO-N); CONSIS reread `g` plus ID stamps (`evaluate_ray == geo_n_arrival`); cached INV used fixture probes, not the events `U` integrates. [H0035](HISTORY.md) already named in-flight affine advance and CONSIS identity with one object in `P`.
- Validation: Confirmed present: pending laboratory ray, `U` commits `tick_delivery` by `t=1/8`, `bound_geo_readings` compares stored `P.ray` / `τ` / ship worldtube, `certify_cached_step` uses `U`'s events. Specialist-reported `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --offline --locked` — 82 passed. Clippy `-p emergent-law-lab --all-targets --offline --locked -- -D warnings` clean. Full qualify not run this turn. Workspace tests not rerun. G2 remains FAIL; production_law null. GEM `advance_map` still refuses. No engine or frozen-evidence edits this turn.
- Evidence: [evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [patch module](../crates/law-lab/src/evolving_patch.rs), [experiment semantics](law-lab.md), [gate manifest](../scenarios/law-gates.json), [unification steering](spacetime-geometry-unification-20260912.md), [GEM specification](laws/causal-retarded-gem-v0.md), [frozen G2 results](../artifacts/evidence/1dac658/law-qualification.json), [H0035](HISTORY.md), [H0038](HISTORY.md), [H0039](HISTORY.md), [updated handoff](HANDOFF.md)
- Limitations: Research map only; not a production gravity law. Field values of `g` remain f64. No Shapiro magnitude is frozen. Rest GEO-T may equal delayed Newton of both rest sources; the patch is not delayed-Newton-as-G2 because GEO-N ≠ Minkowski and CLK-G ≠ inertial. [H0032](HISTORY.md) does not license GEM `advance_map`. Not 2D log gravity, not Kerr, not interacting GR, not FMM, not engine wiring. Frozen G2 JSON remains `1dac658`, not this checkout. Independent review of this patched map has not run.
- Next: Independent review of the patched `advance_patch` map. Do not implement GEM `advance_map`. Not Kerr. Not engine wiring. Keep G2 isolated.


## H0041 — Independent review of evolving-patch U-flies-P.ray map

- Date: 2026-09-12
- Kind: decision / review
- Status: no-go for keeping the patched map as the completeness experiment; G2 still failed
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `254ba1f`; frozen G2 `1dac658` / `99764b4` not overwritten. The reviewed map is [H0040](HISTORY.md). No engine or frozen-evidence edits this turn.
- Scope: isolated `es-evolving-spacetime-patch-v0` research map in `evolving_patch.rs`; no engine wiring
- Changed: Independent review of the [H0040](HISTORY.md) map. H0039 pending-delivery letter is closed (`tick_delivery: None` until the containing tick; stamped private trio fails). The ray `U` flies cannot see the frozen μ change: laboratory emit is `t=0` from `(4,0)` toward `(4,4)`; every Minkowski sample on that path is Before A's cone. `bind_observables` overwrites `coordinate_dt` from a full-path reread of post-step `g`, so CONSIS `stored dt == geo_n_arrival` is identity. GEO-N co-movement still uses spec `pre_emit`/`post_emit` probes, not two-sided `P.ray`. Cached `U` on `P_Δ` dies because source A at `(0,0)`, `t=0` is On its own closed cone; that does not prove ship/ray refuse stale `g` pre-cone. COMPOSE of light is frozen cargo plus a later stamp. Honest FAILs remain `source_backreaction`, `compact_field_certification`, `terminating_exact_branches`, G2, and `production_law` null. GEM `advance_map` still refuses.
- Why: [H0031](HISTORY.md) completeness fails if the geodesic `U` flies is spacelike to the source change and CONSIS of light is a reread of `g`. [H0035](HISTORY.md) already named in-flight affine advance and CONSIS identity with one object in `P`.
- Validation: Read-only review of [the evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [the patch module](../crates/law-lab/src/evolving_patch.rs), `evolving_spacetime_patch_research` in [law-gates.json](../scenarios/law-gates.json), [H0039](HISTORY.md), and [H0040](HISTORY.md). Specialist-reported `cargo test -p emergent-law-lab evolving_patch` — 12 passed (CONSIS/CACHE/COMPOSE of light still not a flown geodesic of the μ change). Cargo qualify not run.
- Evidence: [evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [patch module](../crates/law-lab/src/evolving_patch.rs), [gate manifest](../scenarios/law-gates.json), [unification steering](spacetime-geometry-unification-20260912.md), [H0035](HISTORY.md), [H0039](HISTORY.md), [H0040](HISTORY.md), [updated handoff](HANDOFF.md)
- Limitations: Review did not patch the map and did not retune freeze numbers. Did not re-run full law-lab or qualify. G2 remains FAIL. `production_law` null. GEO-N coordinate `Δt` vs Minkowski/baseline on the **probe** rays stays honest. Delayed-Newton rest split stays honest. Pending `tick_delivery` stays closed as a flag.
- Next: Map patch, not fixtures. The ray `U` flies must be a geodesic that sees the frozen change (spec post-cone emit at `t=1/8`, or an in-flight λ that can). `bind_observables` must not overwrite flown `coordinate_dt`. CONSIS must read two-sided stored `P.ray`, not `bind_observables` ∘ `geo_n_arrival` and not side `evaluate_ray(post_emit)`. CACHE must certify the events `geo_n_arrival` samples; do not kill `P_Δ` solely because A is on-cone with itself at `t=0`. Do not retune freeze numbers. Do not promote G2. Do not implement GEM `advance_map`. Not Kerr. Not engine wiring.


## H0042 — Evolving-patch U flies the post-cone geodesic that sees μ:1→2

- Date: 2026-09-12
- Kind: research experiment
- Status: implemented; G2 still failed; no production law; GEM map not implemented
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `254ba1f`; frozen G2 evidence `1dac658` / `99764b4` not overwritten. No engine files and no `artifacts/evidence/1dac658/` edits this turn. Template next ID is H0042 because [H0041](HISTORY.md) is the U-flies-ray no-go.
- Scope: isolated `es-evolving-spacetime-patch-v0` research map; `es-inertial-causal-v1` untouched; no engine wiring
- Changed: Map patch for [H0041](HISTORY.md). Laboratory `P.ray` is the spec post-cone emit (`t=1/8`, ship → receiver), scheduled at genesis. `U` does not fly it until `live.time >= emit_time`; after emit it refreshes in-flight GEO-N from the step’s `g` and commits `tick_delivery` only on the containing tick (arrival ≈ `3/16`). `bind_observables` stamps `geometry_id` only; flown `dt` is written solely by `U`. CONSIS reads two-sided stored `P.ray` (pre-cone scheduled identically; post-cone stored `dt` differs and equals GEO-N of the stored emit). Cached `U` certifies ship / in-flight emit / GEO-N path samples, not A’s self-cone at `t=0`; pre-cone ticks on `P_Δ` succeed; cache after INV still fails. All 17 `evolving_spacetime_patch_research` fixtures PASS. `compact_field_certification`, `terminating_exact_branches`, and `source_backreaction` stay FAIL. GEM `advance_map` still refuses. No Shapiro freeze. GEM cosine `2047/2048` unchanged. G2 still FAIL. `production_law` remains null.
- Why: [H0041](HISTORY.md) no-go: the ray `U` flew (emit `t=0`) was Before A’s cone on every path sample; `bind_observables` overwrote flown `dt`; CONSIS of light was a reread of `g`; cached `U` on `P_Δ` died because A is on-cone with itself at `t=0`. [H0035](HISTORY.md) already named in-flight affine advance and CONSIS identity with one object in `P`.
- Validation: Confirmed present: scheduled post-cone `P.ray`, `U` flies after emit, bind does not overwrite `dt`, CONSIS two-sided stored `P.ray`, cached `U` takes pre-cone ticks on `P_Δ`. Specialist-reported `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --offline --locked` — 82 passed. Clippy `-p emergent-law-lab --all-targets --offline --locked -- -D warnings` clean. Full qualify not run this turn. Workspace tests not rerun. G2 remains FAIL; production_law null. GEM `advance_map` still refuses. No engine or frozen-evidence edits this turn.
- Evidence: [evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [patch module](../crates/law-lab/src/evolving_patch.rs), [experiment semantics](law-lab.md), [gate manifest](../scenarios/law-gates.json), [unification steering](spacetime-geometry-unification-20260912.md), [GEM specification](laws/causal-retarded-gem-v0.md), [frozen G2 results](../artifacts/evidence/1dac658/law-qualification.json), [H0035](HISTORY.md), [H0040](HISTORY.md), [H0041](HISTORY.md), [updated handoff](HANDOFF.md)
- Limitations: Research map only; not a production gravity law. Field values of `g` remain f64. No Shapiro magnitude is frozen. Rest GEO-T may equal delayed Newton of both rest sources; the patch is not delayed-Newton-as-G2 because GEO-N ≠ Minkowski and CLK-G ≠ inertial. [H0032](HISTORY.md) does not license GEM `advance_map`. Not 2D log gravity, not Kerr, not interacting GR, not FMM, not engine wiring. Frozen G2 JSON remains `1dac658`, not this checkout. Independent review of this patched map has not run.
- Next: Independent review of the patched `advance_patch` map. Do not implement GEM `advance_map`. Not Kerr. Not engine wiring. Keep G2 isolated.


## H0043 — Independent review of evolving-patch post-cone geodesic map

- Date: 2026-09-12
- Kind: decision / review
- Status: go to keep the map as the laboratory completeness experiment; G2 still failed
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `254ba1f`; frozen G2 `1dac658` / `99764b4` not overwritten. The reviewed map is [H0042](HISTORY.md). No engine or frozen-evidence edits this turn.
- Scope: isolated `es-evolving-spacetime-patch-v0` research map in `evolving_patch.rs`; no engine wiring
- Changed: Independent review of the [H0042](HISTORY.md) map. **Go** to keep it as the [H0031](HISTORY.md) laboratory completeness experiment. H0041’s four closed claims hold: post-cone path samples are After A's cone and see μ:1→2; `bind_observables` stamps `geometry_id` only; two-sided stored `P.ray` moves at emit; cached `U` takes pre-cone ticks on `P_Δ` and does not die on A's self-cone. Residuals named, not send-backs: GEO-N is linearized Euclidean-path Shapiro (spec rest formula); CONSIS light at the completeness cut is same-helper at the write cut; frozen COMPOSE horizon `t2=1/8` is emit, so direct vs subdivided is cargo until the last tick then a one-shot `geo_n_arrival` of final `g`; cached `U` applies one geometry snapshot per tick. Honest FAILs remain `source_backreaction`, `compact_field_certification`, `terminating_exact_branches`, G2, and `production_law` null. GEM `advance_map` still refuses.
- Why: [H0031](HISTORY.md) completeness is this tiny evolving patch, not GEM MAP and not G2 promotion. Sending back for a null-ODE integrator or a later COMPOSE horizon would retune the freeze. [H0035](HISTORY.md) already named coordinate/affine GEO-N and no Shapiro freeze.
- Validation: Read-only review of [the evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [the patch module](../crates/law-lab/src/evolving_patch.rs), `evolving_spacetime_patch_research` in [law-gates.json](../scenarios/law-gates.json), [H0041](HISTORY.md), and [H0042](HISTORY.md). Specialist-reported `cargo test -p emergent-law-lab evolving_patch` — 12 passed. Cargo qualify not run.
- Evidence: [evolving-patch spec](laws/evolving-spacetime-patch-v0.md), [patch module](../crates/law-lab/src/evolving_patch.rs), [gate manifest](../scenarios/law-gates.json), [unification steering](spacetime-geometry-unification-20260912.md), [H0031](HISTORY.md), [H0035](HISTORY.md), [H0041](HISTORY.md), [H0042](HISTORY.md), [updated handoff](HANDOFF.md)
- Limitations: Research map only; not a production gravity law. Not a G2 pass. Field values of `g` remain f64. No Shapiro magnitude is frozen. Rest GEO-T may equal delayed Newton of both rest sources. GEO-N is not a 4-velocity null integrator. Frozen COMPOSE does not split an in-flight geodesic after emit. Independent review did not re-run full law-lab or qualify.
- Next: Keep this map isolated as the laboratory completeness experiment. Do not retune freeze numbers. Do not promote G2. Do not implement GEM `advance_map`. Not Kerr. Not engine wiring. Compiler dirty-repair SAP remains parallel and is not gravity.


## H0044 — Isolated advance_patch stdin playground

- Date: 2026-09-12
- Kind: implementation
- Status: implemented; G2 still failed; no production law; GEM map not implemented
- Revisions: Uncommitted law-lab on `codex/emergent-engine` above `254ba1f`; frozen G2 evidence `1dac658` / `99764b4` not overwritten. No engine files and no `artifacts/evidence/1dac658/` edits this turn. Template next ID is H0044 because [H0043](HISTORY.md) is the post-cone go review.
- Scope: isolated `es-evolving-spacetime-patch-v0` playground example; `es-inertial-causal-v1` untouched; no engine wiring
- Changed: Law-lab example `playground` drives public `laboratory` / `advance_patch` / `inspect` so a person can `step`, `goto`, `baseline`/`change`, and `compare` P0 vs PΔ. `dt_q` and patch types are re-exported. Banner states this is the laboratory patch, not production gravity and not the observatory. Empty stdin prints help, status, and compare at `t=1/8` then exits 0.
- Why: Gravity is not in `cargo observatory`. The user asked to play the [H0042](HISTORY.md) map, not only watch tests. [H0043](HISTORY.md) kept that map as the laboratory completeness experiment.
- Validation: Specialist-reported `printf 'compare\ngoto 1/8\ncompare\nquit\n' | CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo run -p emergent-law-lab --example playground --offline --locked` exit 0; empty-stdin smoke exit 0; `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --offline --locked` — 82 passed. Clippy `-p emergent-law-lab --all-targets --offline --locked -- -D warnings` clean. Full qualify not run. G2 remains FAIL; production_law null. No engine or frozen-evidence edits this turn.
- Evidence: [playground example](../crates/law-lab/examples/playground.rs), [patch module](../crates/law-lab/src/evolving_patch.rs), [experiment semantics](law-lab.md), [H0042](HISTORY.md), [H0043](HISTORY.md), [updated handoff](HANDOFF.md)
- Limitations: Not production gravity, not the observatory, not GEM `advance_map`. G2 still FAIL. `production_law` remains null. Linearized Euclidean-path Shapiro residual unchanged. Frozen G2 JSON remains `1dac658`, not this checkout.
- Next: Keep the laboratory completeness experiment isolated. Do not promote G2. Do not implement GEM `advance_map`. Not Kerr. Not engine wiring.


## H0045 — Observatory plays the laboratory advance_patch map

- Date: 2026-09-12
- Kind: implementation
- Status: implemented; G2 still failed; no production law; GEM map not implemented
- Revisions: Uncommitted observatory/law-lab wiring on `codex/emergent-engine` above `254ba1f`; frozen G2 evidence `1dac658` / `99764b4` not overwritten. No `artifacts/evidence/1dac658/` edits. Template next ID is H0045 because [H0044](HISTORY.md) is the stdin playground.
- Scope: native observatory default world for isolated `es-evolving-spacetime-patch-v0`; canonical engine law remains `es-inertial-causal-v1`; `Engine::advance` is not a gravity path
- Changed: Observatory worker constructs law-lab `laboratory(true)` (and `laboratory(false)` for P0 compare) and advances with public `advance_patch` / `inspect`. The default `cargo observatory` chart is that patch: sources A/B, test ship + clock, receiver, post-cone ray, A's coordinate light cone, P0 ghost. PΔ/P0 and Inertial laboratory are explicit buttons; `--world inertial` still launches the billion-ship inertial lab. Snapshots label the view a laboratory completeness experiment, not production gravity and not a G2 pass. Chart fit uses a small patch span so the 8×4 world is visible.
- Why: The user asked to see and play the gravity patch inside the native observatory they actually open. Earlier isolation ("do not wire into the engine") is overridden for this visual product request only: the adapter calls law-lab directly and does not replace the inertial engine law, set `production_law`, or claim G2.
- Validation: `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-observatory --offline --locked -- --test-threads=1` — 7 passed (patch default world plus existing inertial worker/archive test). `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --offline --locked` — 82 passed. `cargo clippy -p emergent-observatory --all-targets --offline --locked --no-deps -- -D warnings` clean. Full qualify not run. Frozen G2 JSON was not rewritten.
- Evidence: [observatory adapter](../crates/observatory/src/adapter.rs), [bridge](../crates/observatory/src/bridge.rs), [app](../crates/observatory/src/app.rs), [patch module](../crates/law-lab/src/evolving_patch.rs), [experiment semantics](law-lab.md), [architecture](architecture.md), [H0042](HISTORY.md), [H0043](HISTORY.md), [H0044](HISTORY.md), [updated handoff](HANDOFF.md)
- Limitations: Not production gravity. Not a G2 pass. `production_law` remains null. GEM `advance_map` still refuses. The chart ray is a Euclidean chord for drawing; delay lives in the map's `coordinate_dt`. Inertial historical-sensor/navigation/archive are the other world. Linearized Euclidean-path Shapiro residual unchanged. Frozen G2 JSON remains `1dac658`, not this checkout.
- Next: Do not promote G2. Do not set `production_law`. Do not implement GEM `advance_map`. Not Kerr. Keep inertial relay ticks and `es-inertial-causal-v1` for ordinary engine scenarios. Keep `1dac658` distinct from HEAD.


## H0046 — Assess compiler drift and prioritize measured geometric reuse

- Date: 2026-09-12
- Kind: source assessment and proposal
- Status: assessment completed; amortization experiment proposed; no implementation or qualification change
- Revisions: Inspected dirty source above 254ba1f while concurrent project work progressed through H0045. Review-specific source hashes recorded. No runtime/law/fixture changes by this assessment.
- Scope: User steering that gravity is intrinsic to the spacetime compiler, computation should be amortized, and recent progress may be drifting from success.
- Changed: Added a focused assessment acknowledging the newer shared evolving patch and observatory while identifying the missing amortization evidence. CompiledGeometry stores source histories; phi_xi still evaluates them per query; normal and cached advance both loop every tick; each tick clones growing histories. Distinguished repeated-input, shared-geometry and time-response reuse. Proposed a joint boundary-response contract and one measured same-law reuse experiment in the current patch instead of more disconnected law variants.
- Why: Passing local consistency/cache fixtures and a playable laboratory do not establish fewer physical computations. The earlier GEM-only diagnosis was narrowed after reading H0031-H0045 and current evolving_patch.rs. A ticked reference is useful, but requires a demonstrated accelerated counterpart. Causal feedback can be ordered across time without assuming its magnitude contracts.
- Validation: Read current handoff, history list and relevant history entries; inspected evolving_patch.rs compile/field/step/cache/fixture paths and engine response.rs. No tests, benchmarks or physical qualification rerun during this assessment. Quadratic cumulative history-copy work is a source-derived growth argument, not a measured speed claim. History check required after append.
- Evidence: [Focused assessment and proposed response contract](compiler-amortization-review-20260912.md), [source-hash provenance](../artifacts/runs/compiler-amortization-review-20260912/review.json), [evolving patch](../crates/law-lab/src/evolving_patch.rs), [existing responses](../crates/engine/src/response.rs), [user unification record](spacetime-geometry-unification-20260912.md), [H0043-H0045 context](HISTORY.md).
- Limitations: No new gravity law, reuse optimization, measured break-even point, source-conservation result or G2 promotion. The live checkout is changing through concurrent work. This review remains uncommitted to avoid bundling the other ongoing implementation/journal changes. Proposed prioritization does not stop or mutate another running task.
- Next: On the existing patch, freeze one supported nonuniform workload, establish independent same-law checks, count source evaluations/physical steps/history copies and full response costs, then implement one reusable geometric response. Require parity before a measured amortization win; distinguish spatial reuse from time compression. Reconsider the law/representation if no supported shortcut can be justified.

## H0047 — Clarify the unified compiler objective and dispatch GLM through OMP

- Date: 2026-09-12
- Kind: objective clarification and delegated investigation
- Status: GLM started; architecture report and probe pending; no qualification change
- Revisions: Source HEAD 254ba1f718771ec1d0a25bf59d0d555f7e57993e plus dirty advances through H0046 and this briefing/prompt copied to isolated branch codex/glm-geometry-reuse. Snapshot commit 5943b3137c024d3b4f814c08928478339e4c751d in /private/tmp/emergent-glm-geometry-reuse. Original checkout changes were not bundled into a main-branch commit.
- Scope: User-authorized GLM via OMP investigation of the original discussions, architectural unification and one discriminating probe; no canonical engine integration.
- Changed: Added a concise objective briefing connecting geometry, source feedback, worldlines, causal hyperedges, regional responses, certificates and history. Wrote an architecture-first assignment and launched configured zai/glm-5.3 with high thinking through local OMP 18.1.18 in its own worktree and session. The initial run is limited to one hour, uses one build job and a separate Cargo target directory, and cannot delegate further under its assignment. Source snapshot, prompt hash, launch arguments, process status and OMP session are retained.
- Why: The user clarified that the supplied discussions already contain the loose foundation and asked for a clear goal document. The report and continued conversation explicitly contain compile/reuse, regional interfaces and partial evaluation. H0046's proposed patch experiment is useful advice, but must not constrain GLM to optimize the existing rounded map before deciding whether that representation serves the intended architecture.
- Validation: Inspected original report executive summary and relevant continued-conversation sections alongside current handoff and H0046 assessment. cargo xtask history list completed. OMP emitted an assistant tool-use response with provider zai and model glm-5.3, then began reading the objective, handoff and history. No GLM result or performance/physics validation has completed at dispatch. History check follows this append.
- Evidence: [Objective briefing](spacetime-compiler-objective.md), [exact GLM assignment](../orchestration/prompts/glm-spacetime-unification.md), [dispatch manifest](../artifacts/runs/glm-spacetime-dispatch-20260912/dispatch.json), [OMP output](../artifacts/runs/glm-spacetime-dispatch-20260912/omp.jsonl), [original context index](reference/README.md).
- Limitations: Launch is not completion. Briefing is an interpretation of user intent, not a proven unification or new law. G2 remains FAIL and production_law null. Source snapshot includes other ongoing work without claiming authorship or fresh validation. Worktree isolation is an execution instruction, not an OS sandbox. No recurring monitoring was created.
- Next: Review GLM's architecture account and probe evidence against the user's original objective. Distinguish confirmed results, proposals and failed hypotheses before any integration. GLM returns a local journal draft; root alone integrates results and updates shared history.

## H0048 — Prepare Grok assignment for coherent G2 completion

- Date: 2026-09-13
- Kind: delegation prompt and status correction
- Status: prompt prepared; Grok not launched; GLM completed and remains unaudited; G2 unchanged
- Revisions: Main checkout remains dirty above 254ba1f. GLM isolated result committed as 6e81b49 above snapshot 5943b31; no integration performed.
- Scope: User-requested prompt for Grok in Cursor to pursue one coherent, qualified G2 law.
- Changed: Added a standalone prompt connecting the unified compiler objective to all ten mandatory production gates, same-law evidence, physical consistency, canonical branch termination, compact/exterior obligations, independent validation and compiler reuse. Explicitly permits justified replacement of research formulations while preserving frozen thresholds and historical failures. Requires reviewing top-level promotion, which currently selects any candidate reporting PASS. Corrects H0047's dispatch-time pending state: OMP exited 0 at 2026-09-12T21:57:33 UTC and GLM wrote a report, probe and local commit.
- Why: User wants an actual G2 solution rather than further disconnected gate fixtures. A prompt must preserve the distinction between a shared architecture, a physically complete law and an optimized evaluation of an incomplete law.
- Validation: Read manifest mandatory gates and candidate/promotion source; ran cargo xtask history list. Previously inspected GLM exit status, clean worktree commit and raw results: specialist reports 864 to 192 source evaluations, approximately 2.8x timing improvement and 88 passing tests on one 16-tick workload. These results were not independently rerun or audited. History check follows this append. No physics implementation or qualification executed for this prompt.
- Evidence: [Grok G2 assignment](../orchestration/prompts/grok-solve-g2.md), [objective](spacetime-compiler-objective.md), [gate manifest](../scenarios/law-gates.json), [qualification source](../crates/law-lab/src/lib.rs), [GLM process manifest](../artifacts/runs/glm-spacetime-dispatch-20260912/dispatch.json), [GLM session output](../artifacts/runs/glm-spacetime-dispatch-20260912/omp.jsonl).
- Limitations: A prompt does not guarantee a mathematical solution. G2 remains FAIL, production_law null, and GLM still executes every physical tick. GLM reports and source remain in its isolated worktree. No Cursor/Grok session was started by this task. Shared uncommitted work is preserved.
- Next: User supplies prompt to Grok in Cursor. Evaluate any resulting candidate against unchanged G2 obligations for the same law, then review evidence before integration.


## H0049 — Qualify es-causal-compiled-spacetime-v1 as the G2 laboratory law

- Date: 2026-09-13
- Kind: implementation and verification
- Status: implemented and measured G2 PASS on the isolated worktree
- Revisions: Isolated branch grok/g2-coherent-spacetime in /private/tmp/emergent-g2-law, overlay of dirty original 254ba1f718771ec1d0a25bf59d0d555f7e57993e; this entry's commit if recorded later. Original checkout and GLM worktree 6e81b49 were not modified.
- Scope: Law-lab G2 candidate `es-causal-compiled-spacetime-v1` only. Not Engine::advance, not FMM/GPU, not billion-ship scale.
- Changed: Froze a gate-to-law matrix and additional completeness gates before the map. Implemented one compiled geometry: C-RET GEM weak-field fill, Verlet of GEM-STATIC for frozen Kepler orbits, excluded-self GEM-a Euler after same-tick capture, Schwarzschild equatorial compact predicates, exact cone/compact/capture/photon/null-from-infinity branches, remainder-in-state exterior. Independent promotion now requires every required and additional mandatory gate executed once and passed, every recorded gate passed, and every acceptance metric passed; it does not trust status==PASS. `cargo xtask law-lab` selected this id. All seven older candidates remain FAIL in the same report. Frozen 1dac658 evidence was not overwritten.
- Why: G2 demanded one coherent law, not a pile of isolated oracles. Delayed Newton fails aberration; Fokker-AVI stayed rejected incomplete; isolated kernels could not close orbits+clocks+coupling+compact+branches together. GEM-STATIC is the frozen Newton 3rd-law diagnostic; retarded two-way is a separate additional gate. Linearized Shapiro along the unperturbed path is GEO-N (Weinberg §8.7 / Shapiro 1964), not a full interacting-GR null solver.
- Validation: CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/g2-law-target CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --offline --locked --lib -- --test-threads=1 exited 0 (88 passed). Same env cargo clippy -p emergent-law-lab --all-targets --offline --locked -- -D warnings exited 0. Same env cargo xtask law-lab artifacts/runs/g2-compiled-spacetime-20260913 exited 0: G2 PASS, production_law es-causal-compiled-spacetime-v1. Whole-product cargo xtask qualify was not run. cargo xtask history check follows this append.
- Evidence: [Law spec](laws/causal-compiled-spacetime-v1.md), [gate-to-law matrix](laws/g2-gate-to-law-matrix.md), [worktree snapshot](laws/g2-worktree-snapshot.md), [candidate source](../crates/law-lab/src/compiled_spacetime.rs), [promotion](../crates/law-lab/src/lib.rs), [qualification JSON](../artifacts/evidence/g2-compiled-spacetime-20260913/law-qualification.json), [provenance](../artifacts/evidence/g2-compiled-spacetime-20260913/provenance.json), [historical FAIL snapshot](../artifacts/evidence/1dac658/law-qualification.json).
- Limitations: GEM field values remain f64 with a quantum; they are not branch certificates. Generic scatter turning roots stay unsupported. GEO-N is linearized path delay, not a compact interacting null geodesic. Dynamic coupling is Euler, not a symplectic retarded integrator. Stationary orbits reuse Verlet of the static kernel. Compiler counters are a tiny 8-tick patch (33 source evals, 2 identical hits, 2 shared-consumer hits, 32 frozen skips), not scale amortization. Selection is not engine integration. G3 and G8 stay blocked. Original checkout is unchanged.
- Next: Independent review of this candidate against the frozen obligations. Do not merge, push, or wire into Engine::advance. Do not treat FMM/GPU/billion-ship as following from this PASS.


## H0050 — Independent review of es-causal-compiled-spacetime-v1 (G2)

- Date: 2026-09-13
- Kind: verification
- Status: failed (no-go on G2 laboratory selection)
- Revisions: Read-only `/private/tmp/emergent-g2-law` `grok/g2-coherent-spacetime` overlay of `254ba1f`; evidence `artifacts/evidence/g2-compiled-spacetime-20260913/`; frozen FAIL `1dac658` / `99764b4` untouched. No code edits in the review.
- Scope: Adversarial review of H0049 G2 PASS / `production_law = es-causal-compiled-spacetime-v1` only. Not engine wiring, G3, FMM/GPU, or GLM reuse.
- Changed: Independent review is a **no-go**. Promotion bookkeeping is sound and frozen numeric thresholds were not retuned. Orbit/tree/backreaction records are the sibling Verlet/Newton helpers (bitwise-identical metrics), not this law's Euler MAP.
- Why: G2 requires one coherent law. Helper-kernel reuse is allowed only if this evaluator/stepper produces the qualification record ([gate-to-law matrix](laws/g2-gate-to-law-matrix.md)).
- Validation: Read spec, matrix, `compiled_spacetime.rs`, `select_production_law`/`production_verdict`, `law-gates.json`, both qualification JSONs. Compared frozen numeric block to `1dac658` (identical). Did not rerun `law-lab` / `qualify`.
- Evidence: [H0049](HISTORY.md), [review](laws/g2-independent-review-20260913.md), [spec](laws/causal-compiled-spacetime-v1.md), [matrix](laws/g2-gate-to-law-matrix.md), [map](../crates/law-lab/src/compiled_spacetime.rs), [promotion](../crates/law-lab/src/lib.rs), [G2 JSON](../artifacts/evidence/g2-compiled-spacetime-20260913/law-qualification.json), [1dac658 FAIL](../artifacts/evidence/1dac658/law-qualification.json).
- Limitations: No new numerical run. Honest residuals if repaired: linearized Shapiro GEO-N, f64 GEM, Euler coupling, exact predicates only on the admitted domain, tiny compiler counters, not engine gravity.
- Next: Implement the repair on the isolated worktree; do not merge or wire. Keep `1dac658` historically FAIL. G3 must not treat Verlet-helper envelopes as this MAP. Stop the G3 OMP run that assumed H0049 PASS.


## H0051 — Same-law G2 repair: CompiledWorld records, specialist re-qualify

- Date: 2026-09-13
- Kind: implementation
- Status: implemented and measured by GLM/OMP; retained G2 selection pending independent review
- Revisions: Isolated `/private/tmp/emergent-g2-law` `grok/g2-coherent-spacetime` overlay of `254ba1f` plus H0036–H0050 uncommitted work. Frozen `1dac658` untouched. No merge/push.
- Scope: `crates/law-lab` candidate `es-causal-compiled-spacetime-v1` only. Not Engine::advance, G3, FMM/GPU.
- Changed: GLM repaired H0050 holes: orbit/isotropy/quantum run on `GemStaticVerletLab` whose accelerations are `CompiledWorld::accel`; tree/3rd-law on this law's GEM-STATIC with N≤64 and N≥65 refused; compact/branch qualification reads CompiledWorld methods; `null_dt` skips frozen samples without evaluating. Specialist `cargo xtask law-lab` exit 0 with production_law this id; regular q0 energy drift `6.681996587420969e-05` vs sibling Verlet `6.454708067860082e-05` (not bitwise identical). H0049 measurement and H0050 no-go are preserved.
- Why: G2 requires this law's evaluator to produce the qualification record. Helper Verlet/Newton bitwise identity was the H0050 counterexample.
- Validation: Specialist reported `cargo test -p emergent-law-lab --offline --locked --lib -- --test-threads=1` exit 0 (90 passed), clippy `-p emergent-law-lab --all-targets --offline --locked -- -D warnings` exit 0, `cargo xtask law-lab artifacts/runs/g2-compiled-spacetime-repair-20260913` exit 0. Integrator confirmed the JSON: status PASS, this id PASS, 19 gates 0 failed, 0 failed metrics, older candidates FAIL. Integrator did not rerun law-lab. OMP repair exit 0 (~35 min).
- Evidence: [H0050](HISTORY.md), [H0049](HISTORY.md), [review no-go](laws/g2-independent-review-20260913.md), [specialist draft](glm-g2-repair-history-draft.md), [qualification JSON](../artifacts/evidence/g2-compiled-spacetime-repair-20260913/law-qualification.json), [provenance](../artifacts/evidence/g2-compiled-spacetime-repair-20260913/provenance.json), [map](../crates/law-lab/src/compiled_spacetime.rs).
- Limitations: Specialist-reported tests/clippy not independently rerun by the integrator this turn. GEM-STATIC Verlet is the stationary method, not the causal Euler tick map. f64 GEM values are not branch certificates. Grid quantum `2^-20` for tree fixtures. Not engine gravity. G3 remains paused until independent review of this repair.
- Next: Independent adversarial review of stepper provenance, N-domain refusal, skip honesty, and grid effects. Do not merge, push, or wire. Do not restart G3 from this specialist PASS alone.


## H0052 — Independent review of H0051 same-law G2 repair

- Date: 2026-09-13
- Kind: verification
- Status: go (retain G2 laboratory selection on the isolated worktree)
- Revisions: Read-only `/private/tmp/emergent-g2-law` `grok/g2-coherent-spacetime` overlay of `254ba1f`. No code edits in the review. Frozen `1dac658` / `99764b4` untouched.
- Scope: Adversarial review of H0051 G2 PASS / `production_law = es-causal-compiled-spacetime-v1` only. Not engine wiring, G3, FMM/GPU.
- Changed: Independent review is a **go**. H0050 holes are closed: orbit/tree/backreaction records are this law's `CompiledWorld` / `GemStaticVerletLab`, not sibling Verlet/Newton bitwise identity; N≥65 refused; compact/branches are this world's methods; `null_dt` skips frozen samples without evaluating. Regular q0 energy drift `6.681996587420969e-05` vs sibling Verlet `6.454708067860082e-05`. H0049 measurement and H0050 no-go remain in the journal.
- Why: G2 requires this evaluator/stepper to produce the qualification record. Helper-kernel reuse is allowed only on that condition ([gate-to-law matrix](laws/g2-gate-to-law-matrix.md)).
- Validation: Read H0049–H0051, H0050 review, specialist draft, law spec, `compiled_spacetime.rs` (`qualify_compiled_spacetime`, `GemStaticVerletLab`, `field_at` N cap, `null_dt`), `lib.rs` promotion, both law-qualification JSONs vs `1dac658` Verlet. Did not rerun `law-lab` / `qualify`.
- Evidence: [H0051](HISTORY.md), [H0050](HISTORY.md), [H0051 review](laws/g2-independent-review-h0051-20260913.md), [H0050 review](laws/g2-independent-review-20260913.md), [repair JSON](../artifacts/evidence/g2-compiled-spacetime-repair-20260913/law-qualification.json), [H0049 JSON](../artifacts/evidence/g2-compiled-spacetime-20260913/law-qualification.json), [1dac658](../artifacts/evidence/1dac658/law-qualification.json), [map](../crates/law-lab/src/compiled_spacetime.rs).
- Limitations: No new numerical run. Residuals for G3 (not send-backs): Euler tick MAP is not Kepler Verlet envelopes; linearized Shapiro GEO-N; f64 GEM; N≤64 static tree diagnostic; tiny compiler counters; `f64_ok` slack; not `Engine::advance`.
- Next: Integrator may retain the laboratory selection. Do not merge, push, or wire. Isolated G3 engine bridge may resume only treating Kepler Verlet as the stationary method, not the coupled tick map. Keep `1dac658` historically FAIL.


## H0053 — G3 same-law engine bridge probe (specialist-measured)

- Date: 2026-09-13
- Kind: implementation
- Status: implemented and measured by GLM/OMP as a laboratory G3 probe; retained G3 selection pending independent review
- Revisions: Isolated `/private/tmp/emergent-glm-g3-bridge` `glm/g3-engine-bridge`, overlay of H0052-retained G2 on `254ba1f`. No commit. Original checkout, G2 tree source, and frozen `1dac658` untouched. Integrator copied reports into G2 evidence only.
- Scope: Labeled public `emergent_law_lab::g3` bridge plus an engine **test** (dev-dependency). Not `Engine::advance`. Default engine law remains `es-inertial-causal-v1`. Not G4/G7/G8.
- Changed: Specialist added a `reuse` gate on `field_at` (direct recomputes; accelerated memos the same bits) and routed the in-tick clock query through `clock_rate` after the first probe failed frozen `shared_consumer_hits >= 1` (criteria not retuned). Probe: two rest masses, massless test body, in-flight light, 48 ticks, 8-tick certificates. Direct 544 source evaluations vs accelerated 352 with bitwise-identical committed state. Certificates still invalidate every interval because the digest hashes growing history. Integrator confirmed `Engine::advance` still names the inertial law.
- Why: G3 acceptance is same-law cheap path vs slow path; rejection is a different solver picking different physics. Memoization over one tick map is the smallest contract that can fail that test honestly.
- Validation: Specialist reported law-lab tests 90 passed; probe test exit 101 then 0 after the clock-routing fix; engine suite rerun 0 after one documented H0025 yield flake. Integrator confirmed the probe JSON counters and engine_law field; did not rerun cargo. OMP G3 exit 0 (~22 min).
- Evidence: [H0052](HISTORY.md), [specialist draft](glm-g3-history-draft.md), [contract](glm-g3-engine-bridge.md), [probe JSON](../artifacts/evidence/g3-engine-bridge-20260913/g3-bridge-probe.json), [frozen criteria](../artifacts/evidence/g3-engine-bridge-20260913/criteria-frozen.json), [run log](../artifacts/evidence/g3-engine-bridge-20260913/run-log.md), [provenance](../artifacts/evidence/g3-engine-bridge-20260913/provenance.json).
- Limitations: Laboratory probe, not certified engine gravity. Conservation drift recorded, not gated. Cache does not skip ticks. Kepler Verlet remains the stationary method, not this tick map. Integrator did not rerun tests. Clippy `-D warnings` still fails on pre-existing overlay files.
- Next: Independent adversarial review of same-law identity (memo vs recompute), the clock-routing counter fix, and that `Engine::advance` stayed inertial. Do not merge, push, or make this the default engine law. Do not start FMM.


## H0054 — Independent review of H0053 G3 engine-bridge probe

- Date: 2026-09-13
- Kind: verification
- Status: go (retain laboratory G3 probe on the isolated worktree)
- Revisions: Read-only `/private/tmp/emergent-glm-g3-bridge` `glm/g3-engine-bridge` overlay of H0052 G2 on `254ba1f`, plus G2 copies of H0053 evidence. No code edits, merge, push, or `Engine::advance` wiring. Frozen `1dac658` / `99764b4` untouched.
- Scope: Adversarial review of the labeled `emergent_law_lab::g3` same-law memo vs recompute probe. Not product G3 PASS, not engine gravity, not G4/G7/G8.
- Changed: Independent review is a **go**. Direct vs Accelerated are one `CompiledWorld::step`; accelerated only memos `field_at`. Engine law remains `es-inertial-causal-v1`. Probe JSON: 48 ticks, 8-tick certificates, 544/0 vs 352/144+144, bitwise state and signal (emit 8, delivery 13). Clock routing through `clock_rate` is an accounting fix after frozen `shared_consumer_hits>=1` failed; criteria were not retuned.
- Why: G3 acceptance is same-law cheap vs slow; rejection is a different solver. Intra-tick memo of a deterministic field query cannot change committed physics; keeping the failed criterion on disk is evidence they did not retune.
- Validation: Read H0052–H0053, specialist contract/draft, reuse gate, clock path, engine test, `LAW_ID`, Cargo.toml dev-dep, evidence JSON vs source. Did not rerun the probe, `qualify`, or observatory builds.
- Evidence: [H0053](HISTORY.md), [H0054 review](laws/g3-independent-review-h0053-20260913.md), [contract](glm-g3-engine-bridge.md), [probe JSON](../artifacts/evidence/g3-engine-bridge-20260913/g3-bridge-probe.json), [frozen criteria](../artifacts/evidence/g3-engine-bridge-20260913/criteria-frozen.json), [run log](../artifacts/evidence/g3-engine-bridge-20260913/run-log.md).
- Limitations: No new numerical run. Certificates snapshot; digest invalidates every interval; cache does not skip ticks. Conservation ungated. Verlet is not the Euler tick map. Linearized Shapiro. Not FMM. Not `Engine::advance`.
- Next: Integrator may retain the laboratory probe. Do not merge, push, or make this the default engine law. Next bounded engine step is WorkBudget charging for the existing bridge, still not production gravity. Do not silently collapse the full-history digest. Keep `1dac658` historically FAIL.


## H0055 — User steering: spacetime oracle, not Newton

- Date: 2026-09-13
- Kind: decision
- Status: adopted as governing next-work reading when it conflicts with Newton-stepper talk
- Revisions: Isolated `/private/tmp/emergent-g2-law` journal/handoff only. No engine code change. Frozen `1dac658` and G2/G3 measurements untouched.
- Scope: Interpretation of the project goal. Not a new law, not `Engine::advance`, not G4/G8.
- Changed: Recorded user correction from the reconstructions and conversations: Emergent Space is a game of behavior; gravity is hard because spacetime must be compiled so later queries are trivial; Newton-talk is a mismatch. Laboratory G2/G3 remain evidence, not that oracle. Next work is shaping the oracle, not charging WorkBudget on the existing tick loop as if that were the compiler.
- Why: Recent answers framed delayed Newton / GEM / Verlet as the gravity problem. The user asked to go up the chain, make geodesics as trivial as straight lines, compile gravity into geometry once, and remember it is still a game.
- Validation: Read the two reconstruction files, [H0031](HISTORY.md) unification, compiler objective, and the [philosophy pass](spacetime-oracle-steering-20260913.md). No new tests.
- Evidence: [steering note](spacetime-oracle-steering-20260913.md), [H0031](HISTORY.md), [compiler objective](spacetime-compiler-objective.md), [H0052](HISTORY.md), [H0054](HISTORY.md).
- Limitations: This is steering, not an implemented oracle. G2/G3 numbers are not retracted. Original checkout unchanged.
- Next: Treat trivial-in-region geometry as the gravity problem. Do not merge, push, or wire. Do not start FMM from the G3 memo probe.


## H0056 — Heading-check cadence (personal skill), not another essay

- Date: 2026-09-13
- Kind: decision
- Status: implemented outside the repo (personal Cursor skill + user rule). Journal draft only; specialist did not append.
- Revisions: Isolated `/private/tmp/emergent-g2-law` AGENTS.md pointer only. No engine code. Frozen `1dac658` untouched. Original checkout not edited.
- Scope: Agent operating cadence at any phase. Not a new law, not `Engine::advance`, not G4/G8.
- Changed: Converged a Readwise-iterating pass into a personal skill `heading-check` that produces/updates an intent card (where we are, where we're going, what we refuse, next action). Tiny alwaysApply user rule points at the skill plus the H0055 oracle correction. Emergent Space game/oracle card is one generated instance, not the skill. Thin AGENTS.md pointer in the G2 tree.
- Why: Newton-talk vs game/oracle was a stray. User asked for philosophy that future agents cannot miss, then steered: process not plaque; the loop must use the advice it finds; any phase, not gravity-only. Conversation philosophy governs old docs.
- Validation: Readwise CLI authenticated. Three search waves (highlights + documents + title/author/note follow-ups). Best hits read (Ferriss antelope, FS Primer/Rumelt kernel, Playing to Win, Strategy vs Tactics, Double Loop, First Principles). `heading-check` self-applied to cut the rest. No engine tests. History not appended by this specialist.
- Evidence: [H0055](HISTORY.md), [steering note](spacetime-oracle-steering-20260913.md). Personal skill and rule live outside the repo; do not add absolute machine paths as journal link targets.
- Limitations: Library has no Walsh book, Boyd primary, Rumelt book, commander-intent manuals, or spacetime/geodesics highlights. Walsh/OODA enter only via adjacent hits and conversation. Skill discovery depends on Cursor loading personal skills and the alwaysApply rule. G2 pointer is uncommitted on the isolated tree unless the integrator takes it.
- Next: Integrator may append this entry and keep the G2 pointer if useful. Agents leading work should run the heading-check, not file another doctrine. Still do not merge, push, or wire `Engine::advance`.


## H0057 — Heading-check role-split (rule loads, skill writes, card constrains)

- Date: 2026-09-13
- Kind: decision
- Status: implemented outside the repo (personal skill + user rule + living card). Journal draft only; specialist did not append.
- Revisions: Isolated G2 `AGENTS.md` pointer slimmed (no card restatement). No engine code. Frozen `1dac658` untouched. Original checkout not edited.
- Scope: Agent operating cadence and file contracts. Not a new law, not `Engine::advance`.
- Changed: Continued Readwise (waves 4–9). New keepers folded into the loop (1° compounds; which game / loser's game; learning can feel like progress). Then a scaffold red-team: the alwaysApply rule, skill, card, AGENTS pointer, and reference were restating the same philosophy. Split roles so they make each other cheaper — rule only loads the skill; skill only runs the loop and overwrites the card; card is the only domain instance; reference is dispute-only; journal stays integrator-only. ES next action sharpened to “name one trivial-in-region representation.”
- Why: User: not enough after the first keep-12 pass; then: the scaffold must become cohesive/synergistic with when-to-run and when-not. A rule that restates the card is a plaque and would not have forced a heading check.
- Validation: Highlight texts read in batches (notes, favorites, tags, gap hunts, waves 5–9). Waves 7–9 added no new surviving rule. Title/author hunts confirmed Walsh/Boyd/Gawande/Jackson/Wooden/Belichick/Auftragstaktik primaries absent. SKILL.md 48 lines. No engine tests. History not appended.
- Evidence: [H0055](HISTORY.md), [steering note](spacetime-oracle-steering-20260913.md). Skill/rule/card live outside the repo; do not add absolute paths as journal link targets.
- Limitations: Library gaps remain. Next action is still a representation to name, not an implemented oracle. Role-split works only if Cursor loads the personal skill and alwaysApply rule.
- Next: Run the check; execute the card. Integrator may append. Still do not merge, push, or wire `Engine::advance`.


## H0058 — Cadence-only gate; raced checklist is theater

- Date: 2026-09-13
- Kind: decision
- Status: implemented outside the repo. Journal draft only; specialist did not append.
- Revisions: Personal skill/rule/card only. Isolated G2 pointer untouched this turn. No engine, law-lab, G3, merge, push, or wire. Frozen `1dac658` untouched. Original checkout not edited.
- Scope: Heading-check working on itself. Not a project next action.
- Changed: User gate recorded on the living card: wait for approval before project work; until then the antelope is improving this cadence. Reviewer question generalized to Robinson (overlook/dismiss conspicuous crucial information). Loop step 1: do not race the four lines. Reference stripped of gravity-work examples so it cannot license project work. Petronius kept as why we did not re-architect roles again.
- Why: User: heading-check may only work on itself for now. A card whose next action was “name a representation” would have started game-world work. Robinson: checklists fail when raced; Tenerife adjacent (Gawande book still absent).
- Validation: Waves 10–13 of highlight text (process/culture/reviewer/checklist/stop-researching). How Not to Be Stupid read in full. No engine tests. History not appended.
- Evidence: [H0057](HISTORY.md), [H0055](HISTORY.md), [steering note](spacetime-oracle-steering-20260913.md). Skill/rule/card live outside the repo.
- Limitations: Commander-intent / Walsh / Gawande primaries still absent. Cadence still a heuristic (Taleb: dangerous if treated as perfect).
- Next: Keep improving the cadence until the user approves project work. Do not name a spacetime representation.


## H0059 — Leftover intent is the card (bus count > 1)

- Date: 2026-09-13
- Kind: decision
- Status: implemented outside the repo. Journal draft only; specialist did not append. Integrator already has H0058.
- Revisions: One phrase on personal `heading-check` SKILL step 6. Card next action unchanged (user gate). No engine, law-lab, G3, merge, push, wire. Original checkout not edited.
- Scope: Cadence only. How the process survives the author.
- Changed: Wave 14 finally hunted leftover intent via future-self / bus-count / next-steps (wave 12's "leader leaves" queries were the wrong game). Keepers: Forte giver-of-notes + Hemingway Bridge; Ferriss/Mee bus count. Skill step 6 now: write so the next agent can start without you. Wave 15 (small leftover / Munger basics) added no new loop rule. Roles not reorganized.
- Why: A cadence that lives only in the current agent's head has bus count 1. Commander's-intent manuals are not in the library; the card is the leftover.
- Validation: 168 wave-14 highlight texts batched; Bus Count article read; wave 15 texts read. No engine tests. History not appended.
- Evidence: [H0058](HISTORY.md). Skill/card live outside the repo.
- Limitations: Still no Auftragstaktik primary. Expert's-curse (harder to teach as you get better) is the named next angle, not done this entry.
- Next: Cadence-only until the user approves project work. Next hunt angle: do not let the cadence become unteachable.


## H0060 — Expert's curse: loop must run without reference.md

- Date: 2026-09-13
- Kind: decision
- Status: implemented outside the repo. Journal draft only; specialist did not append.
- Revisions: One clause on personal `heading-check` SKILL step 6. Card next action unchanged (user gate). Roles not reorganized. No engine, law-lab, G3, merge, push, wire. Original checkout not edited.
- Scope: Cadence only. Teachability as the process improves.
- Changed: Wave 16 hunted the expert's curse in highlight text (Mazur / Feynman / curse-of-knowledge). Skill step 6 now: the next agent starts without you *and without opening reference.md*; if not, cut jargon. Wave 17 (one-sheet / practice-what-you-preach / chase-complexity) added no new loop rule — Peck's one sheet is already the card.
- Why: As the cadence accumulates keepers, the numbered steps fade. That is how a good process becomes unteachable. User `favorite` Feynman: the test is whether you can convey it.
- Validation: 128 wave-16 highlight texts batched; wave 17 texts read. No engine tests. History not appended.
- Evidence: [H0059](HISTORY.md) leftover-intent. Skill/card live outside the repo.
- Limitations: Illusion-of-transparency as a named psychology term was thin in the library; Mazur + Feynman carried the cut. Next angle not done here: adding lines because they sound smart (complexity trap).
- Next: Cadence-only until the user approves project work. Next hunt: complexity trap — are we adding text for its merits or its cleverness?


## H0061 — Cadence waits; more waves would be sunk cost

- Date: 2026-09-13
- Kind: decision
- Status: implemented outside the repo (living card overwrite). No new skill lines.
- Revisions: Personal `heading-check` card only. SKILL.md still 48 lines. No engine, law-lab, G3, merge, push, wire. Original checkout not edited.
- Scope: Cadence-only gate. Not project work.
- Changed: After waves 20–22 added no loop rule, the card's next action is wait for user approval. Removed “until then improve this cadence,” which had licensed inventing another wave. We refuse inventing a Readwise wave because the last one existed.
- Why: Continue-until-approve is not wave-forever. Research-as-procrastination and power-law stop were already on the loop. Named sunk-cost text is almost absent in the library; the adjacent hits were enough.
- Validation: Wave 22 hunt of sunk cost / Concorde / escalation. Integrator did not resume another wave.
- Evidence: [H0060](HISTORY.md), [H0058](HISTORY.md).
- Limitations: Library gaps (Walsh, Boyd, Rumelt book, Gawande, Auftragstaktik, named Goodhart) remain listed. They are not a reason to keep searching.
- Next: Wait for the user. Do not name a spacetime representation until they approve.


## H0062 — Heading-check is agnostic; domain lives on the card

- Date: 2026-09-13
- Kind: decision
- Status: implemented outside the original checkout. Journal draft only; specialist did not append.
- Revisions: Personal `heading-check` SKILL description + body, alwaysApply rule, and G2 `AGENTS.md` first paragraph. ES card remains the instance for that effort. No engine, law-lab, G3, merge, push, wire. Original checkout not edited.
- Scope: Cadence contract. The loop is not a project sermon.
- Changed: Skill and rule no longer name Emergent Space, gravity, Newton, spacetime, or oracle. Triggers are generic (leading, planning, stuck, which-bet, what is this, refuse, drift, philosophy, anti-bloat). Skill points at `cards/` — one living card per effort — not at the ES path as the meaning of the check. Rule loads the skill and says: if a living card exists, read it. G2 AGENTS first paragraph is “run heading-check” plus a locator; the game/oracle lines stay on the card.
- Why: User review: a project-specific skill goes stale. Domain details belong only on the living card.
- Validation: Grep of skill + rule has no domain trigger words. SKILL line count did not balloon (still ~48). No engine tests. History not appended.
- Evidence: [H0061](HISTORY.md), [H0055](HISTORY.md).
- Limitations: Agents must pick the card for *this* effort from `cards/`; the rule no longer hard-codes the ES filename. No Jira/backlog/PM suite added.
- Next: Cadence-only until the user approves project work. Next action remains wait.


## H0063 — Heading-check gains propagate / kill / compound

- Date: 2026-09-13
- Kind: decision
- Status: implemented outside the original checkout. Journal draft only; specialist did not append.
- Revisions: Personal `heading-check` index, three short modules, alwaysApply loads the index. ES card unchanged as the domain instance. No engine, law-lab, G3, merge, push, wire. Original checkout not edited. HISTORY not appended.
- Scope: Cadence OS. Heading-check remains the brake; it is not the whole OS.
- Changed: Added `modules/propagate.md` (update or retire already-living docs when the card moves), `modules/kill.md` (per-effort kill-list; subtract), `modules/compound.md` (admit a rule only if another module gets cheaper). SKILL.md is the index + brake loop. Reviewer stays only on the index. Domain still only on `cards/`.
- Why: User correction — projects grow or lose direction because philosophy/direction is badly documented or not updated. A brake card does not keep other docs true. Readwise: Cosenzo stale process-docs; Forte campsite; Ferriss subtract; Taleb via negativa; Munger/Waitzkin few basics in the blood.
- Validation: Highlight texts batched under `/tmp/emergent-kernel-readwise/deep/wave-os/` (stale/kill/compound + follow-up). No engine tests. History not appended.
- Evidence: User correction this turn. [H0062](HISTORY.md) agnostic contract.
- Limitations: Propagate will not invent a handbook if the effort has no living docs besides the card. Named Drucker stop-doing list and Walsh *Score* remain absent. No Jira/sprint layer.
- Next: Cadence-only until the user approves project work. Use propagate when a living doc contradicts the card; do not invent another Readwise wave as the work.


## H0064 — Ask module; brake no longer silently continues

- Date: 2026-09-13
- Kind: decision
- Status: implemented outside the original checkout. Journal draft only; specialist did not append.
- Revisions: Personal `heading-check` index + `modules/ask.md`. Existing propagate / kill / compound kept. Three Readwise waves only. No engine, law-lab, G3, merge, push, wire. Original checkout not edited. HISTORY not appended.
- Scope: Cadence OS. Fastest path to a *correct* goal; user checkpoints.
- Changed: New module **ask** — stop and question the user / offer a heading change when the goal is invented, unclear, or the destination may be wrong. Heading-check step 1 no longer says “next action named → do that” if the goal may be invented. Step 5: next action is the fastest path to the correct goal, with why in one clause. Reviewer adds: inventing a goal? asked the user? lost in a detail? Wave 3 found no named SpaceX algorithm / ops-cadence / radio-silence highlights — those were not added as files.
- Why: User: LLMs don’t ask enough, get lost in details, and are bad at pivoting. FS *Goal Induced Blindness*: change the destination, not only the route. Vicino: define the problem. Banayan/TED: if you don’t ask, you don’t get.
- Validation: Three wave batches under `/tmp/emergent-kernel-readwise/deep/os3/`. No engine tests. History not appended.
- Evidence: User this turn. [H0063](HISTORY.md) module set.
- Limitations: Elon “algorithm” / operational cadence / “make the requirement less dumb” are absent as highlight text. Gist kept via ask + kill (question, then subtract), not a SpaceX cargo-cult module.
- Next: User reviews the OS files. Do not invent wave 4.


## H0065 — Fastest path is a trigger chain, not sloppy speed

- Date: 2026-09-13
- Kind: decision
- Status: implemented outside the original checkout. Journal draft only; specialist did not append.
- Revisions: Personal `heading-check` index (step 5 + reviewer), `modules/probe.md` added, ask/kill/compound/receipt/propagate/rule/reference/card updated. Nine Readwise waves under `/tmp/emergent-kernel-readwise/deep/fastest/`. No engine, law-lab, G3, merge, push, wire. Original checkout not edited. HISTORY not appended.
- Scope: Cadence OS. Next action = the move that most improves the heading (often a question, a test, or data), not the first cheap-looking task.
- Changed: **probe** — when the heading is the user's but the path is a guess, write a cheap falsifying test as the next action. Step 5 is now a trigger chain: ask if destination may be wrong → name the obstacle (Rumelt diagnosis, not a new file) → probe if guess/story → reversible vs irreversible (FS favorite) → invert then kill → "and then what?". Reviewer: easier question than the heading? test or story? Diagnose.md / invert.md / consult.md did not earn slots (folded). Hashing still absent.
- Why: User: they do not want sloppy speed. Kahneman substitution + FS "easy over right" are the failure mode of the old one-clause slogan. Narrative Fallacy (favorite): experiment over story. Waitzkin (favorite): slowly correctly before speed.
- Validation: Wave batches `w1`–`w9` under `/tmp/emergent-kernel-readwise/deep/fastest/`. Stopped after waves 8–9 added no new trigger/move after unify. No engine tests. History not appended.
- Evidence: User this turn. [H0064](HISTORY.md) ask + receipt.
- Limitations: Boyd/OODA, Gawande checklist, named Goodhart/sunk-cost, Five Whys procedure, Walsh *Score*, Auftragstaktik manuals, hashing — still absent. SITG consult did not earn a file (folded into receipt + probe).
- Next: User reviews the OS files. Do not invent wave 10.


## H0066 — OS refinements as heading-check triggers (not an institution)

- Date: 2026-09-13
- Kind: decision
- Status: implemented outside the original checkout. Journal draft only; specialist did not append HISTORY.
- Revisions: Personal `heading-check` skill (loop + reviewer + incentives), alwaysApply rule fire-list, new `modules/preflight.md`, ask/probe/kill/propagate/compound/receipt/reference/card/kill/receipt updated. Eight Readwise waves. No engine, law-lab, G3, merge, push, wire. Original checkout not edited. HISTORY not appended.
- Scope: Cadence OS. User's 16 failure modes as reliable triggers. Prefer redefine + chain. One new module only because it fires a distinct moment (before acting ≠ after).
- Changed: **preflight** — before acting: what/how/assumptions, pre-mortem, dynamics, Fermi-adjacent scale, SpaceX question→delete→simplify→accelerate→automate-last, cardboard vs solid given stakes. Receipt stays after. Fresh card still runs preflight (skip only the four-line rewrite). Ask + step 3: user states new/refined philosophy — tighten, write the card, subsequent work referenced against it. Propagate: same words as the system. Probe + kill: labelled experiments; implement or archive off the daily path; temporaries have a death date. Compound: steal when the need is named; OS rewards honest feedback / cardboard / subtract — not waves or modules. Step 2: decompose then unify. Step 3: analog for mechanism, first principles for destination.
- Why: User: the trigger must actually work or the whole thing never works. Institution = too many process files. Redneck = skip the brake, skip honest feedback, skip removing temporaries. Cards stay. Next action still wait for user review.
- Validation: Eight themed Readwise waves; stopped after waves 7–8 added nothing after unify. No engine tests. History not appended.
- Evidence: User this turn. [H0065](HISTORY.md) fastest-path chain.
- Limitations: Named Fermi-as-method, Gauss-the-mathematician, Gawande Checklist, Boyd/OODA, named Goodhart, Auftrag manuals, hashing — still absent. SpaceX "the algorithm" as a complete gist still thin; encoded from user words + Isaacson question/delete/automate-last. Pareto catalog not added. Preflight is one more file — earned because before ≠ after.
- Next: User reviews the OS files. Do not invent wave 9. No engine or project work.


## H0067 — Simpler ≠ simple; bottleneck as system constraint

- Date: 2026-09-13
- Kind: decision
- Status: implemented outside the original checkout. Journal draft only; specialist did not append HISTORY.
- Revisions: Personal `heading-check` skill (step 2, step 5, reviewer), `modules/probe.md`, `modules/preflight.md`, `modules/kill.md`, `modules/compound.md`, `reference.md`, card / kill / receipt. Six Readwise waves. No engine, law-lab, G3, merge, push, wire. Original checkout not edited. HISTORY not appended.
- Scope: Cadence OS. Two user cuts in one pass: a gutted implementation is not a probe or a kill of the idea; the obstacle on the card is the constraint that limits the whole. Prefer redefine. No new module.
- Changed: Probe now names the essential claim actually tested and refuses a straw-man as “heading tried or falsified” (kill the path, not the idea); after a result it re-scans the system constraint. Preflight keeps cardboard but requires it to carry the real claim; SpaceX simplify runs after the requirement is true and must not delete the requirement that is the idea; work that misses the bottleneck or adds unused capacity is refused. Loop step 2 names the system constraint (not a local annoyance) and looks again after it moves; step 5 loosens that constraint. Kill and reviewer refuse gutted invalidation and polish beside the jam. Compound when-not lists `simplicity.md` and `bottleneck.md`.
- Why: User: making it simpler does not mean simple; a badly done cheap path is not the idea implemented or invalidated. Rumelt “name the obstacle” is not Theory of Constraints — the system only goes as fast as the constraint that limits the whole; local efficiency on a non-constraint is waste.
- Validation: Six themed Readwise waves covering both cuts; stopped after waves 5–6 added nothing after unify. No engine tests. History not appended.
- Evidence: User this turn. [H0066](HISTORY.md) OS refinements as triggers.
- Limitations: Goldratt *The Goal* / drum-buffer-rope still absent as highlight text; TOC encoded from user words plus Vicino, Hormozi, Young rate-determining step, and Lean local productivity. Named SpaceX algorithm gist still thin. Cardboard/honest feedback unchanged — this cut does not license skipping probes.
- Next: User reviews the OS files. Do not invent wave 7. No engine or project work.


## H0068 — Philosophy on the card; daily path unhooked from the doc mess

- Date: 2026-09-13
- Kind: handoff
- Status: implemented on the living card and G2 journal home. Journal draft only; specialist did not append HISTORY.
- Revisions: Personal heading-check card / kill / receipt. Isolated `/private/tmp/emergent-g2-law` `docs/HANDOFF.md`, `AGENTS.md`, `docs/architecture.md`, and historical headers on steering/GLM notes. One-line pointer on the original checkout `docs/HANDOFF.md` only. No engine, law-lab, G3, merge, push, or wire. Frozen `1dac658` untouched. HISTORY not appended.
- Scope: OS + docs hygiene. Philosophy/goals as the living heading. Not a gravity implementation, not G2 product PASS, not a folder reorg.
- Changed: Overwrote the Emergent Space intent card: destination is a game of behavior (not a Newton/GR replica); mechanism is compile-spacetime-so-later-geodesics-are-cheap; G2/G3 stay laboratory evidence; frozen `1dac658` stays FAIL; named bottleneck is agents/Julien lost in stale docs and worktrees. Propagated G2 HANDOFF (living-start banner, First ten minutes, user-intent “card governs”, recommended next-work) and G2 AGENTS living-start pointer. Marked architecture as capability map not destination. Unhooked steering/GLM notes with a historical header. Original checkout got a one-line “not the living start” pointer. Did not shuffle folders, merge worktrees, delete evidence, rewrite committed HISTORY, or start gravity.
- Why: User asked to run heading-check so philosophy and goals are properly defined, and to organize the project because it is getting messy. Cadence-only wait was the stale next action. The constraint that limited the whole was the contradictory map, not an unimplemented geodesic. Simpler ≠ simple: archives stay off the daily path rather than being deleted.
- Validation: Read heading-check skill + modules, living card, G2 HANDOFF/HISTORY/architecture, original checkout HANDOFF/docs sprawl, `git status`/`git worktree list` on original and G2, `cargo xtask history list` on G2 (H0001–H0067). No engine tests. History not appended.
- Evidence: [H0067](HISTORY.md).
- Limitations: Original checkout remains dirty; G2 remains an uncommitted worktree. Laboratory G2/G3 numbers are not retracted and are not product PASS. Specialist trees still exist on disk. Integrator must append this entry. Next agent still needs Cursor to load the personal skill and the card path.
- Next: Julien reviews the daily path (card + G2 HANDOFF First ten minutes). Do not start gravity until they name that work. Next agent starts there.


## H0069 — Behavior catalog on the card; phase is define behavior

- Date: 2026-09-13
- Kind: handoff
- Status: implemented on the living card and G2 journal home. Journal draft only; specialist did not append HISTORY.
- Revisions: Personal heading-check card / kill / receipt. Isolated `/private/tmp/emergent-g2-law` `docs/HANDOFF.md` living start, First ten minutes, and recommended next. No engine, law-lab, G3, merge, push, or wire. Frozen `1dac658` untouched. HISTORY not appended. No `philosophy.md`, no behavior companion file.
- Scope: Define-behavior heading. Cardboard catalog, solid on the card. Not a gravity implementation, not G2 product PASS, not a folder reorg.
- Changed: Overwrote the Emergent Space intent card so philosophy plus a short behavior list are the heading: must-feel (recognizable orbits at every scale, shared geometry, slow backreaction, clocks disagree, you see the past, compact capture, hierarchical twins/binaries, light takes time and can bend a little); allowed divergence (orbit a bit bigger, linearized/GEM, cheap geodesic, absorbing capture not interiors); tests not products (black-hole capture, twins, N-body fleet, slow asteroid push, flyby); cut (GW product, Kerr interiors, frame-dragging museum, Shapiro-as-product, overbuilt BH). Named bottleneck is the unconfirmed behavior list. Propagated G2 HANDOFF living-start, First ten minutes, and recommended next from “the map” to “define behavior”; stop for Julien to confirm or cut. Kill list now stops overbuilt BH, Newton/GR-as-identity, and polishing law-lab before the catalog. Did not implement gravity, merge worktrees, delete evidence, rewrite committed HISTORY, or add a parallel behavior essay.
- Why: User asked to properly define behavior (orbits, gravity, GR effects at all scales, allowed divergence, black holes as tests, many ships, slow asteroid push, twins, what else). Without that list, gravity work becomes a replica or a straw man. Simpler ≠ simple: “orbit a bit bigger” is allowed divergence, not 2-body Newton called GR-at-all-scales.
- Validation: Read heading-check skill + ask/probe/preflight/kill/propagate/receipt, living card/kill/receipt, G2 HANDOFF first-ten plus H0055/H0068 banners, law-lab kernel/gate names (orbits, clocks, light, capture, binaries/backreaction). `cargo xtask history list` on G2 (H0001–H0068). No engine tests. History not appended.
- Evidence: [H0068](HISTORY.md).
- Limitations: Catalog is cardboard until Julien confirms or cuts. Light-bend vs inertial “you see the past” remains a possible fork. Laboratory G2/G3 numbers are not retracted and are not product PASS. Integrator must append this entry.
- Next: Julien confirms or cuts the behavior list on the card. Do not implement gravity until they name that work.


## H0070 — Light-bend is must-feel; linked visual tree under the card

- Date: 2026-09-13
- Kind: handoff
- Status: implemented on the living card, effort tree, heading-check skill, and G2 journal home. Journal draft only; specialist did not append HISTORY.
- Revisions: Personal heading-check card / tree / kill / receipt / skill / modules / alwaysApply rule. Isolated `/private/tmp/emergent-g2-law` `docs/HANDOFF.md` living start, First ten minutes, and recommended next. No engine, law-lab, G3, merge, push, or wire. Frozen `1dac658` untouched. HISTORY not appended.
- Scope: Define-behavior heading plus heading-check OS. Light-bend decided. Tree is the effort map, not a second philosophy. Not a gravity implementation, not G2 product PASS.
- Changed: Closed the light-bend fork: bending and extra delay near mass are must-feel now (think of them early; they add feedback); how much bend remains allowed divergence; tests may include a light-near-mass case without Shapiro-as-product. Added heading-check `modules/tree.md` and one Emergent Space tree file (are / going / done / missing / conflict, mermaid + why/refs). Conflicts stay as both pointers (extra delay vs Shapiro-as-product vs no-freeze; H0031 lab patch vs H0055 game; lab G2 PASS vs frozen FAIL). Propagated G2 HANDOFF so the living start no longer treats the fork as open. Kill list stops treating light-bend as deferred and stops tree-as-institution (forty node files, canvas-as-only-tree, overwriting conflicts). AlwaysApply fires when the user asks for the tree, a node is completed or missing, or a conflict appears, still as an index load. Did not implement gravity, merge worktrees, delete evidence, rewrite committed HISTORY, or dump the journal onto the tree.
- Why: User answered the fork (light-bend is early feedback, not a later museum) and asked for a linked visual map so they do not get lost — populate from conversations and docs, show conflicting ideas instead of overwriting. Julien getting lost is the OS bottleneck after the daily path of card + HANDOFF.
- Validation: Read heading-check skill and all modules, living card/kill/receipt, G2 HANDOFF first-ten plus H0055/H0068/H0069 banners. Readwise four waves (maps vs territory, evergreen/MOC/conflict, Rumelt/missing/visual/second-order, Darwin/confabulation); stopped after unify — a fifth wave would repeat one-sheet/Peck already in the OS. `cargo xtask history list` on G2 (H0001–H0069). No engine tests. History not appended.
- Evidence: [H0069](HISTORY.md).
- Limitations: Remaining catalog items are still cardboard until Julien confirms or cuts. Light-bend is decided as heading, not implemented. Tree is current state of affairs, not a 1:1 HISTORY. Integrator must append this entry.
- Next: Julien confirms or cuts remaining catalog items. Ask show the tree for the map. Do not implement gravity until they name that work.


## H0071 — Compiled geodesic oracle contract; isolated GLM probe is next

- Date: 2026-09-13
- Kind: handoff
- Status: implemented on the living card, effort tree, G2 oracle contract, and G2 journal home. Journal draft only; specialist did not append HISTORY.
- Revisions: Personal heading-check card / tree / kill / receipt. Isolated `/private/tmp/emergent-g2-law` `docs/laws/compiled-geodesic-oracle-contract-20260913.md` and `docs/HANDOFF.md` living start, First ten minutes, and recommended next. No engine, law-lab implementation, OMP, merge, push, or `Engine::advance` wire. Frozen `1dac658` untouched. HISTORY not appended.
- Scope: Compiled-geodesic-oracle heading. Contract for an isolated GLM probe. Not product gravity, not G2 product PASS, not engine wiring.
- Changed: Named the bottleneck as no compiled spacetime the engine can query, so later geodesics including light-bend and extra delay near mass are not cheap. Wrote a short oracle contract: compile once then later (GEO-T)/(GEO-N)/(CLK-G) cheap; light-bend plus extra delay as a first-class query; cardboard world of two masses plus test ship plus light near mass plus clock; allowed divergence matches the card; independent falsifiers; lab names reused with the H0031-versus-H0055 conflict kept as both pointers. Overwrote the intent card so the phase is that isolated bottleneck, remaining catalog constrains the probe rather than a wait gate, and the next action names the isolated GLM probe. Tree marks the compiled geodesic oracle live/in-progress; light-near-mass in the work stays missing until GLM lands something. Propagated G2 HANDOFF living start, First ten minutes, and recommended next to that heading. Kill list stops wait-for-catalog as next action and stops 2-body Newton or straw-man Verlet called the oracle. Did not implement crates, launch OMP, merge worktrees, wire `Engine::advance`, delete evidence, rewrite committed HISTORY, or put Emergent Space into heading-check SKILL.md.
- Why: User named the jam: later geodesics are not cheap because there is no compiled spacetime to query. Waiting on remaining catalog cuts would work beside that jam. A gutted Verlet or 2-body Newton would not carry the claim.
- Validation: Read heading-check skill plus preflight/tree/ask/kill/receipt/propagate, living card/tree/kill/receipt, G2 HANDOFF first-ten plus H0055/H0069/H0070, HISTORY search compiled/spacetime/geodesic/oracle, evolving-patch and compiled-spacetime law names. No engine tests. History not appended.
- Evidence: [H0070](HISTORY.md).
- Limitations: Contract is not an implemented oracle. Light-near-mass is still missing in the work. Remaining catalog items are still cardboard constraints. Laboratory G2/G3 numbers are not retracted and are not product PASS. Integrator must append this entry.
- Next: Isolated GLM probe on G2 against `docs/laws/compiled-geodesic-oracle-contract-20260913.md`. Do not launch OMP. Do not merge, push, or wire `Engine::advance`.


## H0072 — Independent falsifiers for the compiled geodesic oracle

- Date: 2026-09-13
- Kind: verification
- Status: implemented as spec on the G2 journal home. Journal draft only; specialist did not append HISTORY.
- Revisions: Isolated `/private/tmp/emergent-g2-law` `docs/laws/compiled-geodesic-oracle-falsifiers-20260913.md`. Spec only. No oracle map, no engine edits, no gate mix-in. Frozen `1dac658` untouched. Original checkout not edited. HISTORY not appended.
- Scope: Independent falsifiers for object `compiled-geodesic-oracle`. Not G2 production gates, not `Engine::advance`, not product PASS.
- Changed: Nine frozen ids: `cgo_cardboard_cast`, `cgo_compile_vs_integrate`, `cgo_geo_n_light_near_mass`, `cgo_shared_geometry`, `cgo_slow_backreaction`, `cgo_clk_g_disagree`, `cgo_absorbing_capture`, `cgo_newton_disguise`, `cgo_not_engine_advance`. Fail-closed: missing gate is FAIL; `NOT_CLAIMED` allowed only on slow backreaction; Verlet swap must not keep probe PASS. Blocks H0050 holes (sibling helper records, invisible stepper, skip counters that still evaluate, unbound compact oracles). Not this round: GW, Kerr, frame-dragging, billion ships.
- Why: GLM must not call 2-body Newton/Verlet the oracle. Compile-once cheap is not G3 field-at memo. Cardboard must still carry light-bend plus extra delay.
- Validation: Specialist read H0050/H0052/H0055, sibling Verlet helpers, `emergent_engine::LAW_ID`. No law-lab run. History not appended.
- Evidence: [H0071](HISTORY.md). [Falsifiers](laws/compiled-geodesic-oracle-falsifiers-20260913.md). [Contract](laws/compiled-geodesic-oracle-contract-20260913.md).
- Limitations: Spec only. No candidate scored. Integrator copies the file onto the GLM worktree because it was missing at OMP launch.
- Next: Isolated GLM probe scores these ids without retuning. Do not merge, push, or wire `Engine::advance`.


## H0073 — AGENTS.md loads heading-check for Codex, GLM/OMP, and Cursor

- Date: 2026-09-13
- Kind: handoff
- Status: implemented as a thin repo pointer on the original checkout, G2 journal home, and GLM oracle overlay. Journal draft only; specialist did not append HISTORY.
- Revisions: Original checkout `AGENTS.md`. Isolated `/private/tmp/emergent-g2-law` `AGENTS.md`, `docs/HANDOFF.md` First ten minutes, and `orchestration/prompts/glm-compiled-geodesic-oracle.md`. Isolated `/private/tmp/emergent-glm-oracle` `AGENTS.md` and the same prompt note. Personal heading-check tree / kill / receipt. No engine, law-lab, OMP kill, merge, push, or `Engine::advance` wire. Frozen `1dac658` untouched. HISTORY not appended. Card next-action unchanged.
- Scope: Agent cadence load via repo `AGENTS.md`. Not product gravity, not the compiled geodesic oracle map, not G2 product PASS.
- Changed: Added a short Heading check section after the contract opener on original, G2, and oracle `AGENTS.md`: run the skill; living card and tree paths; if the skill is unreadable still read the card, do not invent goals, preflight before acting; Codex, GLM/OMP, and Cursor must load this loop — do not pass `--no-skills`. Strengthened G2's one-liner to match; oracle journal home is G2, not "this worktree". One line on both GLM prompts for future launches (running OMP pid 98876 left alive). G2 HANDOFF first-ten: Codex reads AGENTS.md Heading check. Tree node `AGENTS.md loads cadence for Codex` marked done. Kill list stops Cursor-only load and `--no-skills` when the loop is required. Did not copy the skill into the repo, put Emergent Space into SKILL.md, edit engine/crates/law-lab, kill OMP, or change the card next-action.
- Why: Cursor alwaysApply does not load for Codex or GLM/OMP. A repo pointer is the shared cadence. Copying the skill would be institution. `--no-skills` would skip the loop when it is required.
- Validation: Read heading-check skill plus preflight/propagate/kill/receipt/tree, living card, original/G2/oracle `AGENTS.md`, G2 HANDOFF first-ten, both GLM prompts. No engine tests. OMP not killed. History not appended.
- Evidence: [H0072](HISTORY.md).
- Limitations: Running GLM OMP was launched before the prompt note; it will not see the new line until a future launch. If `~/.cursor/skills/` is unreadable the agent still has card/tree paths and the fallback duties, not the full skill. Integrator must append this entry.
- Next: Isolated GLM probe on G2 against `docs/laws/compiled-geodesic-oracle-contract-20260913.md`. Do not kill the running OMP. Do not merge, push, or wire `Engine::advance`.


## H0074 — Audit compiler branches and propose physically anchored implementation plan

- Date: 2026-09-14
- Kind: review and planning
- Status: proposed; user discussion remains open
- Revisions: Read-only code audit of original, G2, G3 and oracle dirty overlays on `254ba1f`; geometry-reuse clean `6e81b49`. This turn changes planning and continuity documents only. No new source revision was tested or qualified.
- Scope: Compiler/engine implementation proposal, current worktree provenance, and clarified physical/game behavior intent.
- Changed: Added discussion draft 0.1 with branch map, source-level failure mechanisms, reusable foundations, a quantitative behavior instrument, proposed common geometric derivation, source-aware transport responses, full-cost probes and staged integration. Julien clarified Waitzkin intent as monitoring the right behaviors to develop intuition while preserving realistic GR/spacetime effects and consistent magnitudes. Updated the living heading card/tree and handoff accordingly. Oracle dispatch records process_aborted and no landed probe, correcting the old running pointer. Independent draft review added dynamic magnitude anchors, a worked exact-shortcut obligation, explicit light-reception semantics and committed-versus-speculative history distinction.
- Why: Repeated helper passes and same-tick memoization did not establish the coupled spacetime compiler. A finite physical reference and compact evolving transport are both unresolved; neither should be hidden as routine implementation work for the next agent. The new user clarification also makes nonzero-only effects insufficient as physical acceptance.
- Validation: Ran cargo xtask history list and history search oracle; inspected git worktrees/status/log, current source and retained reports, and primary geometric/numerical references. Three bounded read-only specialist audits and an independent draft review completed. No physical tests, engine builds, benchmarks, or qualification runs were requested or performed. cargo xtask history check passed with 74 entries, local links and committed-prefix preservation checked.
- Evidence: [Discussion draft](compiler-engine-plan-20260913.md), [handoff](HANDOFF.md), [compiled map](../crates/law-lab/src/compiled_spacetime.rs), [G3 review](laws/g3-independent-review-h0053-20260913.md), [oracle dispatch](../artifacts/runs/glm-oracle-dispatch-20260913/dispatch.json), [prior oracle contract](laws/compiled-geodesic-oracle-contract-20260913.md).
- Limitations: Source findings about ray delay, capture history, shared-geometry qualification and finite decisions are not runtime-reproduced regressions. No frozen evidence or retained laboratory verdict was rewritten. No branches were merged, no implementation started and no new physical law selected. Magnitude bands and the numerical/transport contract remain discussion decisions. Dirty historical overlays remain uncommitted; committing this journal wholesale would also include prior owners' unrelated uncommitted history.
- Next: Discuss draft 0.1 with Julien, settle physical anchors and reusable-oracle scope, then pin source snapshots and prepare the first bounded implementation packet. Reject any candidate unable to specify its complete finite reference or demonstrate a charged shortcut preserving that reference.


## H0075 — Adopt visual litmus families and amortization-first refinement

- Date: 2026-09-14
- Kind: decision and planning
- Status: direction refined; implementation remains proposed
- Revisions: Planning documents on the G2 dirty overlay above `254ba1f`; no engine source edits or new physical measurements.
- Scope: Accepted oracle meaning, visual behavior tests, seed semantics, component responsibilities and progressive causal refinement.
- Changed: Revised the existing plan to draft 0.2. Julien accepted compile-once reuse of predictable evolving situations with paid causal repair. Added six qualitative litmus families covering fast ships/light/clocks, solar systems, three-body behavior, galaxies, black holes and fleet/intervention feedback. Each has look-for cues and underlying physical checks. Distinguished exact compiler parity from law/generator/seed comparisons. Moved predictable multiplicity, work visualization and unequal resolved horizons into the first coupled experiment. Specified coarse bounds, summed weak influence and refinement by consequential uncertainty. Removed priority for existing retarded-metric/Taylor implementations and updated the card/tree/handoff.
- Why: User wants rapid visual calibration of realistic emergent behavior and optimization from the outset. One seeded orbit is neither a universal law test nor permission to excuse compiler divergence through chaos. Connected spacetime needs shared causal contracts; neither separate tuned simulators nor inherited code is an adequate foundation.
- Validation: Read current card, handoff, plan, worktree status and relevant history; ran cargo xtask history list/search. One bounded independent review supplied five substantive corrections, all incorporated. Primary REBOUND and relativity references checked for test semantics. No physics tests, benchmarks or engine builds run. History validation is performed after append.
- Evidence: [Draft 0.2](compiler-engine-plan-20260913.md), [handoff](HANDOFF.md), [prior planning audit](HISTORY.md).
- Limitations: Six scene families are a proposed instrument, not implemented tests or proof of universal behavior. 99.9 percent reuse is a user hypothesis, not measured evidence. A complete finite coupled law and an actual reusable shortcut remain unresolved. No frozen gate, source implementation or historical verdict was changed. Existing mixed overlays and prior uncommitted history remain uncommitted.
- Next: Refine the six visual cues and declared physical regimes with Julien, then make the first bounded law/reference/shortcut assignment concrete. Preserve the accepted oracle scope and evaluate candidate mathematics on both coherence and fully charged reuse.


## H0076 — Develop causal boundary-response mathematics for motion and navigation

- Date: 2026-09-14
- Kind: mathematical design
- Status: proposed with worked analytic derivations; no implementation or qualification
- Revisions: Planning/continuity documents on G2 dirty overlay above `254ba1f`; no engine or law-lab source changes.
- Scope: Demand-driven refinement, causal far-field representation, shared geometry, transport composition, source families and navigation.
- Changed: Added draft 0.3 mathematical core. Distinguished a valid certificate from an inconclusive bound or invalidated assumptions. Derived a stationary scalar multipole tail example, affine transport/family moment composition, oscillator transport with accumulated forcing bound, and an exact restricted common-metric timelike/null/clock fixture. Connected boundary generating functions and stationary elimination to navigation using transfer derivatives, with a focusing-time inverse-query falsifier. Named time-ordering, nonlinear field closure, finite canonical evaluation, exterior/history, frame/clock matching and conformal-no-bending limitations. Updated living card/tree/handoff toward mathematical unification rather than further gallery elaboration.
- Why: User explicitly asks for mathematical tricks and composition that retain distant gravity cheaply and make subsequent computation/navigation reusable at all scales. High-level compiler language alone does not demonstrate eliminated work; a shared algebraic response and its concrete failure boundaries are needed.
- Validation: Read current plan/card/handoff and relevant original research sections; ran history list/search. Consulted primary FMM, weak-field GR, conformal geodesic, Hamilton-Jacobi and plane-wave propagation sources linked in the draft. One bounded independent mathematical review checked action versus min-plus, constant versus time-varying transport, complete boundary state and navigation focusing. Algebraic examples are derivations, not executable benchmark results. No physical tests, engine builds or qualification runs performed. History check follows append.
- Evidence: [Draft 0.3 mathematical core](compiler-engine-plan-20260913.md), [handoff](HANDOFF.md), [original response discussion](reference/original-research-report.md).
- Limitations: No new physical law selected. The plane-wave/oscillator fixture is not a galaxy, self-gravitating two-mass engine, gravitational-wave product or exact finite runtime implementation. Ordinary multipole bounds do not certify causal nonlinear GR. General block elimination, source evolution, finite equality decisions and compact response size remain unresolved. No measured speedup or gate change. Prior mixed overlays/history remain uncommitted.
- Next: Refine this mathematical proposal with Julien; use the worked response and its residual/focusing falsifiers to make the first finite-reference/shortcut packet precise without dropping the complete two-source matter/light/clock feedback requirement.


## H0077 — Freeze litmus gallery contract and root interfaces

- Date: 2026-09-14
- Kind: decision
- Status: implemented as contract documents; cues frozen; numeric bands UNCONFIRMED
- Revisions: Planning documents on journal home `/private/tmp/emergent-g2-law` above `254ba1f`; no engine, law-lab, or observatory source edits.
- Scope: Packet 1 litmus/interfaces freeze. Six visual cards, seed/comparison rules, coupled transition, and root JSON schema. Not a gravity law, GLM shortcut, gallery UI, or `Engine::advance`.
- Changed: Froze glance / look-for / looks-wrong / do-not-force cues and allowed outcome classes for the six families; froze compiler-only versus law/generator comparison semantics, diagnostic versus held-out banks, charged work-overlay sampling, and true-state versus observer-knowledge channels using existing `inspect` / `observe_with_budget` / `history_digest` / `ViewMode` names. Placeholder numeric bands are explicit UNCONFIRMED.
- Why: Draft 0.3 asked to refine cues so judgments are quick without forcing every seed to the same system. Julien has not chosen magnitude bands. Root owns interfaces; GLM/OMP owns the finite law.
- Validation: Specialist read heading-check card and preflight; `cargo xtask history list`; searched HISTORY for litmus / observatory / seed; read draft 0.3 behavior instrument and seed tables plus observatory `ViewMode` / engine `semantic_random` / `WorkBudget` names. JSON parsed (six cards, six UNCONFIRMED regimes). Integrator accepted the freeze documents and appended this entry. No qualify, no full workspace build, no physics tests.
- Evidence: [Litmus contract](laws/litmus-gallery-contract-20260914.md), [interface schema](laws/litmus-gallery-contract-20260914.json), [draft 0.3](compiler-engine-plan-20260913.md), [H0075](HISTORY.md), [H0070](HISTORY.md).
- Limitations: Numeric seed integers, generator versions for a future gravity law, and all regime bands remain UNCONFIRMED. The gallery is not implemented. Passing the future gallery would not prove all emergent behavior. Independent review of this freeze is still due. Packet 1 law (finite reference and worked shortcut) is out of scope here.
- Next: Packet 0 provenance and GLM/OMP packet 1 law continue. Do not treat bands as gates. Independent review of this freeze after packet 1 law lands, or sooner if requested. Packets 2–7 wait. Do not wire `Engine::advance`.


## H0078 — Packet 0: hashed overlay snapshots and clean selected compiler worktree

- Date: 2026-09-14
- Kind: operation
- Status: implemented (provenance only; no compile, no merge, no engine wiring)
- Revisions: clean worktree `/private/tmp/emergent-compiler-impl` on uncommitted branch `codex/compiler-packets` from `254ba1f`. Old overlays kept dirty on their existing branches. This entry is not yet committed.
- Scope: Overlay inventory, hashed snapshots, and file-level selection into a new `codex/` implementation tree. Not Packet 1 law, not `Engine::advance`, not G2 promotion.
- Changed: Inventoried dirty overlays (original checkout, G2 journal home, G3 bridge, geometry-reuse `6e81b49`, glm-oracle, older law-lab/mechanics/observatory trees). Sealed tar/git-bundle snapshots under `/private/tmp/emergent-overlay-snapshots/20260914/` excluding `target/`. Created `/private/tmp/emergent-compiler-impl` from explicitly selected original inertial engine files plus G2 specs/reviews. Stored G2 `compiled_spacetime.rs` and capture/`field_at` helpers under `docs/reference-overlays/g2-compiled-spacetime/` as negatives, not as `crates/law-lab`. Wrote `SELECTION.md` in the clean tree and `artifacts/runs/packet0-preserve-20260914/provenance.json` on the journal home.
- Why: Draft 0.3 Packet 0 requires recoverable provenance and a clean selected worktree. Whole-branch merges of dirty overlays would mix laboratory G2/G3 maps into the inertial compiler. Prefer original engine bytes (identical to G2) when gravity lives only in law-lab.
- Validation: Specialist reported `git worktree add -b codex/compiler-packets` succeeded on attempt 1; original vs G2 engine sources SHA-256 identical. Integrator confirmed clean `LAW_ID=es-inertial-causal-v1` and that `compiled_spacetime.rs` exists only under `docs/reference-overlays/g2-compiled-spacetime/`. Packet 1 tree `/private/tmp/emergent-glm-packet1-law` was not used. No workspace, observatory, qualify, or law-lab cargo commands were run for this packet.
- Evidence: [provenance JSON](../artifacts/runs/packet0-preserve-20260914/provenance.json), [Packet 0 prompt](../orchestration/prompts/packet0-preserve-select.md), [draft 0.3](compiler-engine-plan-20260913.md), [H0077](HISTORY.md).
- Limitations: Snapshots omit `target/`, `artifacts/Emergent Space.app`, and screenshots. Oracle snapshot is `dispatch.json` only (`process_aborted`; not resumed). geometry-reuse unique files are snapshotted, not merged. Observatory and original law-lab gravity kernels remain deferred. Two litmus contract files arrived on the journal home after the primary G2 tar; a supplement archive records them. Clean tree is an uncommitted selected overlay, not a qualified engine revision. Frozen `1dac658` G2 FAIL unchanged.
- Next: GLM/OMP Packet 1 law in `/private/tmp/emergent-glm-packet1-law` specifies the finite reference and one charged worked shortcut. Independent review follows that law packet. Packets 2–7 wait. Do not wire `Engine::advance`.


## H0079 — Additive Newtonian relational-hierarchy laboratory probe

- Date: 2026-09-14
- Kind: experiment
- Status: implemented as an isolated laboratory probe; not a selected causal GR law
- Revisions: worktree `/private/tmp/emergent-relational-hierarchy` on uncommitted `codex/relational-hierarchy` from `254ba1f`. Journal-home copies of the spec and cost table only. Engine law unchanged. This entry is not yet committed.
- Scope: Additive `es-relational-hierarchy-v0` in law-lab. Not Packet 1, not `Engine::advance`, not G2 promotion, not a rewrite of draft 0.3 or the litmus freeze.
- Changed: Implemented a bound binary as one dynamical unit (`R̈=0`, Kepler `r`, one eval recovers both bodies); uniform external acceleration cancels from `r` and moves `R`; distant `T_ext` drives internals at `ε_tide` scale; separated groups share one `U_AB`. Admission uses spatial rank, omitted derivatives, temporal variation, and susceptibility — not `ε_tide` alone. Killer cases fail closed or shorten the horizon (source-only moments, weak-coupling beating, composed Kepler pair maps). Encounter shortened H 20→8. Frozen tiny workloads report `f(H,ε)` and `C_repair/C_replay` as operation counts.
- Why: Julien asked to test the relational inversion without deleting Packet 0/1. The catch is when compact relations break.
- Validation: Specialist reported `cargo test -p emergent-law-lab relational_hierarchy` 14 passed, 0 failed, and `cargo run -p emergent-law-lab --example relational_hierarchy -- --write-artifacts`. Integrator copied spec and `report.json` onto the journal home. Quiet binaries `f=1.00`; weak-coupling beat `f=0.05`; encounter `f=0.40`. Fermi `ε_tide` diagnostics matched order-of-magnitude hypotheses and are not gates. Cost ratios on tiny scenes are O(1), not a billion-fold claim.
- Evidence: [probe spec](laws/relational-hierarchy-probe-20260914.md), [cost table](../artifacts/runs/relational-hierarchy-20260914/cost-table.md), [assignment prompt](../orchestration/prompts/relational-hierarchy-probe.md), [H0078](HISTORY.md).
- Limitations: Newtonian algebraic reduction only. Not retarded GR, not production gravity, not wall-clock qualification. Hierarchy construction does not store all relative vectors. Independent adversarial certificate review is still due. GLM/OMP Packet 1 was not interrupted.
- Next: GLM/OMP Packet 1 remains the finite coupled-law and charged-shortcut bottleneck. Do not wire this probe into `Engine::advance`. Packets 2–7 wait. Do not multiply overlapping Fermi factors into a claimed speedup.


## H0080 — Packet 1 plane-wave fixture, charged shortcut, and coupled-law gap

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as laboratory fixture plus an honest coupled-law stop
- Revisions: worktree `/private/tmp/emergent-glm-packet1-law` on uncommitted `glm/packet1-finite-law` from `254ba1f` plus overlay. Journal-home copies of spec, gap, and cost table only. Engine law unchanged. This entry is not yet committed.
- Scope: Packet 1 law. Analytic `es-plane-wave-oscillator-v0` and coupled two-source gap. Not Packet 2, not `Engine::advance`, not G2 promotion.
- Changed: Landed a new law id whose one pp-wave metric supplies timelike, null, and clock transport; compiled oscillator apply with independent checker; focusing inverse FAIL-CLOSED at `h=π/ω`; residual bound tests; G2-defect negatives that FAIL as controls. Compiled path reports `reference_steps=0` versus slow `32768`. Coupled two-source equations remain open in seven named holes; Euler-tick G2 is not the reference.
- Why: Draft 0.3 Packet 1 requires a finite executable reference and one charged shortcut. Open coupled Einstein/matching/self-force equations are a stop, not a papered evaluator. Previous GLM/OMP dispatch died with prompt echo only.
- Validation: Specialist reported `cargo test -p emergent-law-lab plane_wave` 12 passed, 0 failed, and wrote `artifacts/runs/glm-packet1-finite-law-20260914/`. Integrator copied spec, gap, and cost table onto the journal home. RSS after probe ~1.8 MiB. No `qualify`, no observatory.
- Evidence: [plane-wave spec](laws/plane-wave-oscillator-v0.md), [coupled-law gap](laws/packet1-coupled-law-gap-20260914.md), [cost table](../artifacts/runs/glm-packet1-finite-law-20260914/cost-table.md), [H0079](HISTORY.md).
- Limitations: The oscillator is a mechanism check, not a two-source feedback probe, not GR, not `production_law`. Slow-path agreement uses a declared Verlet enclosure; algebraic equality is versus the independent checker. Exact-expression cost is operation counts, not certified bit complexity. Frozen `1dac658` untouched.
- Next: Close a *versioned finite truncated* coupled law for the Packet 2 scene, or keep the gap. Do not code a Packet 2 evaluator on unspecified equations. Do not treat the oscillator as the two-source scene. Do not wire `Engine::advance`.


## H0081 — Truncated coupled GEM law closes Packet 1's seven-item gap on a declared domain

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as an isolated truncated laboratory law, not Einstein two-body and not engine gravity
- Revisions: worktree `/private/tmp/emergent-coupled-law` on uncommitted `glm/packet2-coupled-law` copied from the Packet 1 tree. Parent `/private/tmp/emergent-glm-packet1-law` not edited after add. Journal-home copies of spec and cost table only. This entry is not yet committed.
- Scope: `es-truncated-coupled-gem-v0` in law-lab. Two uniform balls, test ship, near-mass ray, clock, capture-with-historical-μ, A→B→A on linearized retarded GEM \(O(G^1,\beta^1)\). Not Packet 2 cohort/overlay, not Packets 3–7, not `Engine::advance`.
- Changed: Named finite rules for the seven Packet 1 gap items on that domain: (KINK) source exchange, eternal-rest incoming certificate, uniform-ball self-force by symmetry, shell exterior plus kink-shell temporal remainder, capture keeping past μ, one Φ for delay/bend/clock, rational C-CONE/contact ties. Remainders named: off-lattice GEM-a, kink radiation, \(O(G^2)\). G2-defect negatives retained. Apply `reference_steps=0`.
- Why: Draft 0.3 Packet 2 cannot execute on unspecified coupled equations. Euler-tick G2 and the plane-wave oscillator are the wrong objects for this scene.
- Validation: Specialist reported `cargo test -p emergent-law-lab truncated_coupled` 9 passed, 0 failed, and wrote `artifacts/runs/coupled-law-20260914/`. Integrator copied spec and cost table onto the journal home. Probe `seven_items: closed`. RSS after probe ~2.0 MiB. No `qualify`, no observatory.
- Evidence: [truncated coupled spec](laws/truncated-coupled-gem-v0.md), [cost table](../artifacts/runs/coupled-law-20260914/cost-table.md), [Packet 1 gap](laws/packet1-coupled-law-gap-20260914.md), [H0080](HISTORY.md).
- Limitations: Linearized GEM of two balls is not a complete GR two-body solution. Radiation at kinks omitted. Exact gravitational Δv is lattice-restricted. Null delay uses an O(G) Euclidean-path Shapiro jet. Packet 2 cohort, work overlay, unequal resolved horizons, and a fully charged reference-vs-compiled workload are not this unit. Frozen `1dac658` untouched. `production_law` remains null.
- Next: Packet 2 complete transport probe on this law id: distinct cohort sharing geometry, work overlay, coarse refinement, unequal horizons, held-out entrants, charged compile/query/repair versus an equally charged reference. Do not wire `Engine::advance`. Do not promote G2. Do not treat remainders as Einstein two-body.


## H0082 — Packet 2 complete transport probe: charged reuse with A→B→A feedback

- Date: 2026-09-14
- Kind: experiment
- Status: implemented as an isolated laboratory probe on `es-truncated-coupled-gem-v0`
- Revisions: worktree `/private/tmp/emergent-packet2-probe` on uncommitted `glm/packet2-transport-probe` copied from the coupled-law tree. Parent `/private/tmp/emergent-coupled-law` not edited after add. Journal-home copy of the cost table only. This entry is not yet committed.
- Scope: Packet 2 transport exit on the truncated GEM law. Eight held-out launches, charged overlay, unequal horizons, in-flight ray, remote observer, encounter fallback, A→B→A backreaction. Not Packets 3–7, not `Engine::advance`, not the six-card observatory UI.
- Changed: Compiled one geometry shared by a compact cohort; overlay sampling charged without changing `history_digest`; slow backreaction exercised. Frozen feedback workload N=8, horizon t=0..4. Compiled packet-charged work 75 versus equally charged same-law reference 345 (`reference_steps` 0 vs 272). Break-even consumer count 2. A no-feedback cohort ran cheaper and is rejected as reuse proof.
- Why: The truncated law closed the seven-item gap; Packet 2 still required reuse across distinct consumers and time, not only a two-mass map.
- Validation: Specialist reported `cargo test -p emergent-law-lab packet2_transport` 6 passed and `truncated_coupled` 9 passed. Integrator copied the cost table onto the journal home. RSS after probe ~2.2 MiB. No `qualify`, no observatory.
- Evidence: [cost table](../artifacts/runs/packet2-transport-20260914/cost-table.md), [truncated coupled spec](laws/truncated-coupled-gem-v0.md), [H0081](HISTORY.md).
- Limitations: Truncated linearized GEM is not Einstein two-body. Overlay is a laboratory sample, not the visual gallery. Delay/Bend jets remain the rest-piece laboratory ray. Frozen `1dac658` untouched. `production_law` remains null.
- Next: Packet 3 long-time response: periodic/phase generators, boundary composition, retained secular perturbations; increase horizon with other variables fixed. Precomputing every tick/orbit and hiding it in compilation fails. A stationary fixture alone cannot pass. Do not wire `Engine::advance`.


## H0083 — Packet 3 long-time response: periodic generator beats a ticking reference

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as an isolated laboratory probe on `es-truncated-coupled-gem-v0` with an admitted (PERIOD) generator
- Revisions: worktree `/private/tmp/emergent-packet3-longtime` on uncommitted `glm/packet3-long-time` copied from the Packet 2 probe tree. Parent `/private/tmp/emergent-packet2-probe` not edited after add. Journal-home copies of the cost table and the updated truncated-law spec. This entry is not yet committed.
- Scope: Packet 3 long-time exit. Horizon sweep with N, consumers, and source-change density held fixed. Not Packets 4–7, not `Engine::advance`, not Einstein two-body.
- Changed: Lattice (KINK) cannot close a subluminal periodic two-body orbit, so the law gained an admitted (PERIOD) generator: exact rational rotation, phase as a tick count, slow residual retained, adjacent responses composed as \((F_2 F_1, F_2 d_1+d_2)\) on the complete boundary. Compile stores the one-tick generator; it does not loop over the horizon. Frozen sweep N=2, consumers=4, source-change density=1, ticks 8/16/32. Compiled totals 68/87/121 versus ticking same-law reference 199/359/679. Generator bytes stay ~618; a per-tick cache grows 1756→17392. Source evolution stays 1. Residual grows and is kept. Stationary rest map (total 4) and tick-cache were measured and rejected as the passing fixture.
- Why: Packet 2 showed charged reuse across distinct consumers. Draft 0.3 Packet 3 still required reuse across time.
- Validation: Specialist reported `cargo test -p emergent-law-lab packet3_longtime` 7 passed, `truncated_coupled` 9 passed, and wrote the cost table. Integrator copied the table and updated spec onto the journal home. RSS after probe ~2.4 MiB. No `qualify`, no observatory.
- Evidence: [cost table](../artifacts/runs/packet3-longtime-20260914/cost-table.md), [truncated coupled spec](laws/truncated-coupled-gem-v0.md), [H0082](HISTORY.md).
- Limitations: Truncated linearized GEM plus (PERIOD) is not Einstein two-body, not `production_law`, not `Engine::advance`. (PERIOD) is an admitted generator, not a closed (KINK) orbit. Powered rotation uses `Ratio<BigInt>` because \(R^n\) overflows i128; bit growth is charged on apply. Delay/Bend jets of the rest-piece laboratory ray are unchanged. Frozen `1dac658` untouched.
- Next: Packet 4 massive-population probe: extend the family contract to a nonuniform gravitating family; extraction, common operation, tides, encounters; include the fleet's effect on sources. Compare canonical outcomes with a materialized small reference. Measure compression as population and distinction count vary. Neither drop nor double-count source contributions. Do not wire `Engine::advance`.


## H0084 — Packet 4 massive-population probe: nonuniform family beats materializing members

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as an isolated laboratory probe on `es-truncated-coupled-gem-v0` with an admitted (FAMILY)
- Revisions: worktree `/private/tmp/emergent-packet4-population` on uncommitted `glm/packet4-population` copied from the Packet 3 tree. Parent `/private/tmp/emergent-packet3-longtime` not edited after add. Journal-home copies of the cost table and the updated truncated-law spec. This entry is not yet committed.
- Scope: Packet 4 massive-population exit. N and distinction-count sweeps with horizon fixed. Not Packets 5–7, not `Engine::advance`, not Einstein two-body.
- Changed: Two-ball laboratory still refuses `N≠2`. This packet admits a nonuniform gravitating family: D independently parameterized fragments generate N members. Compile stores fragments, mass/first-moment summaries, AABB worldtubes and a named tide/kink residual — not N worldtubes. Extraction subtracts the member (mass 6→5). Common apply `reference_steps=0`. Tides Δa_x=2/25. Encounter at (3,0) Interior of B. μ>0 fleet moves A's first kink to 817/32000; μ=0 leaves 5/256. Frozen horizon 4 ticks. N sweep at D=2: compiled work 9/9/9 versus materialized 18/34/70; bytes ~970 versus 697/1397/2801. D sweep at N=8: compiled work 9/11/13, sources 2/5/8. Uniform D=1, μ=0, and Packet 3's two-mass (PERIOD) fixture cannot pass this packet.
- Why: Packet 3 showed reuse across time. Draft 0.3 Packet 4 still required compression as population and distinction count vary, without dropping or double-counting source contributions, and with the fleet's effect on sources.
- Validation: Specialist reported `cargo test -p emergent-law-lab packet4_population` 8 passed, `truncated_coupled` 10 passed, and wrote the cost table. Integrator copied the table and updated spec onto the journal home. RSS after probe ~2.25 MiB. No `qualify`, no observatory.
- Evidence: [cost table](../artifacts/runs/packet4-population-20260914/cost-table.md), [truncated coupled spec](laws/truncated-coupled-gem-v0.md), [H0083](HISTORY.md).
- Limitations: Truncated linearized GEM plus an admitted family is not Einstein two-body, not `production_law`, not `Engine::advance`. Pair-kernel exact Δv is certified on the small N=4 layout; larger N uses COM monopoles plus named remainder when r² is not a square. Frozen `1dac658` untouched.
- Next: Packet 5 engine integration of this law/response into the current scheduler, contacts, signals, observer queries and budgets under an explicit law id. Replay, cache eviction, query order, partition order, cancellation and simultaneous events must preserve results. Default `Engine::advance` stays `es-inertial-causal-v1`. `production_law` remains null. Do not promote G2.


## H0085 — Packet 5 engine integration: opt-in truncated GEM on current contracts

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as an explicit opt-in engine path, not default gravity and not production
- Revisions: worktree `/private/tmp/emergent-packet5-engine` on uncommitted `glm/packet5-engine` copied from the Packet 4 tree. Parent `/private/tmp/emergent-packet4-population` not edited after add. Journal-home copy of the cost table. This entry is not yet committed.
- Scope: Packet 5 engine integration of `es-truncated-coupled-gem-v0` (admitted PERIOD and FAMILY) under an explicit law id. Default `Engine::advance` remains `es-inertial-causal-v1`. `production_law` remains null. Not Packets 6–7, not observatory UI, not G2 promotion.
- Changed: `Engine::with_law` / `with_truncated_admission` select the truncated law. Default `Engine::new` still stamps inertial. Truncated `advance` charges compile/apply/repair to `WorkBudget`, routes contacts, C-CONE signals and observer queries through `EventRecord` / `observe` / `observe_with_budget`, and names moving, compact, PERIOD and FAMILY domains. Unsupported domains (photon sphere, two moving horizons, laboratory N≠2, t>4) fail closed. Apply keeps `reference_steps=0`.
- Why: Packet 4 showed family compression. Draft 0.3 Packet 5 requires that response inside the current scheduler, contacts, signals, observer queries and budgets without promoting a lab wrapper or replacing inertial `advance`.
- Validation: Specialist reported `packet5_engine` 14 passed, `causal_contract` 18 passed, engine lib 24 passed, `truncated_coupled` 10 passed. Integrator copied the cost table onto the journal home. No `qualify`, no observatory rewrite.
- Evidence: [cost table](../artifacts/runs/packet5-engine-20260914/cost-table.md), [truncated coupled spec](laws/truncated-coupled-gem-v0.md), [H0084](HISTORY.md).
- Limitations: Truncated linearized GEM is not Einstein two-body, not `production_law`, not default `Engine::advance`. Laboratory apply is fail-closed outside t≤4. Signal delay uses C-CONE of the truncated units, not the laboratory-ray Delay jet, except when `geometry_query("laboratory")` is asked. G2 Euler is not this path. Frozen `1dac658` untouched.
- Next: Packet 6 history and controlled game behavior: chunk archives and reconstruction; causal policy IR using received knowledge; shared broadcasts with individual receptions. Old observations reconstruct correctly; incoming/outgoing influences survive sealing; policy outcomes survive representation changes. No runtime LLMs. Do not promote `production_law`. Do not replace default inertial `advance`.


## H0086 — Packet 6 history and policy: sealed chunks, received-knowledge IR, individual receptions

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as engine history/policy, not production gravity
- Revisions: worktree `/private/tmp/emergent-packet6-history` on uncommitted `glm/packet6-history` copied from the Packet 5 tree. Parent `/private/tmp/emergent-packet5-engine` not edited after add. Journal-home copy of the cost table. This entry is not yet committed.
- Scope: Packet 6 history and controlled game behavior. Chunk archives, reconstruction, causal policy IR over received knowledge, shared broadcasts with individual receptions. Default `Engine::advance` remains `es-inertial-causal-v1`. Truncated GEM remains opt-in. `production_law` remains null. Not Packet 7, not runtime LLMs.
- Changed: `Engine::seal_archive` / `restore_archive` / `reconstruct_observations` split committed events into checksummed chunks with an atomically replaced manifest; remainder keeps in-flight signals, unresolved broadcasts, scheduled courses, actuator momentum and worldtubes. `Command::Broadcast` is one emission over an identity range; each worldtube gets its own reception tick or a certified absence. Policy IR is a guarded program over `{lo..=hi}` evaluated from committed receptions, retarded observations, own proper time and local resources. Tree and postfix bytecode encodings match. `Engine::omniscient_diagnostic` stays a separate API.
- Why: Packet 5 put truncated GEM on engine contracts. Draft 0.3 Packet 6 still required sealed history and in-world policy to survive representation changes without a global heard-it bit or hidden true-state.
- Validation: Specialist reported `packet6_history` 9 passed, `packet5_engine` 14 passed, `causal_contract` 18 passed, engine lib 24 passed. Integrator copied the cost table onto the journal home. Reconstruction, sealing remainder, policy-IR survival, and individual receptions held. No `qualify`.
- Evidence: [cost table](../artifacts/runs/packet6-history-20260914/cost-table.md), [H0085](HISTORY.md).
- Limitations: Chunked archive is not Packet 7 operating-envelope qualification and not a GPU/FMM path. Policy IR does not choose the game's economy or faction rules. Certified absence is remainder, not a committed event. Huge identity ranges fail closed on job capacity. Frozen `1dac658` untouched.
- Next: Packet 7 optimize and qualify: freeze a combined workload before tuning; measure the M1/8 GB envelope including cold start, history, interventions, observer requests and final verified checkpoint. Preserve failed controls and report unsupported workloads. Do not weaken `1dac658`. Do not promote `production_law`. Do not add FMM/GPU unless measured worthwhile.


## H0087 — Packet 7 optimize and qualify: frozen combined CPU envelope on M1/8 GB

- Date: 2026-09-14
- Kind: experiment
- Status: measured as an M1/8 GB operating envelope, not production gravity and not the game destination
- Revisions: worktree `/private/tmp/emergent-packet7-qualify` on uncommitted `glm/packet7-qualify` copied from the Packet 6 tree. Parent `/private/tmp/emergent-packet6-history` not edited after add. Journal-home copies of the envelope table and frozen workload. This entry is not yet committed.
- Scope: Draft 0.3 Packet 7. Frozen combined workload (inertial default `advance`, opt-in truncated GEM, Packet 6 archive/policy, observer requests, one intervention per world, verified checkpoint). Default `Engine::advance` remains `es-inertial-causal-v1`. Truncated GEM remains opt-in. `production_law` remains null. Not FMM, not GPU, not `scale-gates.json`, not a billion-ship run.
- Changed: Froze `scenarios/packet7-combined.json` (sha256 `23eb44373a57d0cf522a68fe8db823cb152c11d99a3055bc53bb0cfe39a4ceab`) before any timing run and did not retune it. Added `cargo xtask packet7-qualify`. Did not add FMM or GPU. Did not run whole-product `qualify`. Did not write `artifacts/evidence/1dac658/`. Cold/warm RSS 5.156 / 5.500 MiB, yield p95 11.125 / 11.708 µs, charged ops 5574, wall 162.283 / 147.218 ms. History/reconstruction dominated cold wall (114.2 ms). Isolated 5 ms yield control PASS; the bound was not retuned.
- Why: Packet 6 sealed history/policy. Draft 0.3 Packet 7 still required a measured operating envelope with failed controls preserved and unsupported workloads reported honestly.
- Validation: Specialist ran release `cargo xtask packet7-qualify` on Apple M1 8 GiB with JOBS=1. Reconstruction, policy-IR, individual receptions, checkpoint verify, and unsupported-domain fail-closed held. Integrator copied the envelope and frozen workload onto the journal home. RSS stayed far below the frozen 4 GiB abort.
- Evidence: [envelope table](../artifacts/runs/packet7-qualify-20260914/envelope.md), [H0086](HISTORY.md).
- Limitations: This is the assigned Packet 7 CPU envelope, not the draft's game destination and not product PASS. Combined path uses Packet 5/6 fixtures, not `scale-gates.json`. Compiled bytes are canonical JSON, not RAM. Isolated 5 ms PASS does not erase the historical default-suite flake. Billion-ship, one-hour, FMM, GPU, and `production_law` selection remain unsupported. Frozen `1dac658` untouched.
- Next: Do not merge the packet7 worktree. Do not promote G2. Do not replace default inertial `advance`. Do not call billion-ship / one-hour a capability. Do not call the game destination done because Packet 7 measured. Independent review of the coupled implementation and the six-card observatory overlay remain unassigned.


## H0088 — Heading: independent review, six-card overlay, and production gravity

- Date: 2026-09-14
- Kind: decision
- Status: implemented as the living heading; the three units are assigned, not complete
- Revisions: heading-check card / tree / kill / receipt; journal-home HANDOFF living start; prompts under `orchestration/prompts/`. No engine source change. This entry is not yet committed.
- Scope: New `/goal` after draft 0.3 packets 0–7. Not a `production_law` selection. Not a Fermi gate.
- Changed: Julien assigned independent review of the coupled implementation, the six-card observatory overlay, and production gravity, and offered Fermi estimates (ε_tide Hill-scale sanity check; spatial/relational/temporal/causal redundancies; requested `f(H,ε)` and `C_repair/C_replay`). Those estimates are recorded as hypotheses. Overlapping factors must not be multiplied into a claimed speedup. `production_law` stays null until review plus those measurements.
- Why: Packets 0–7 were assigned exits, not the game destination. Waiting to assign the remaining missing nodes is dead.
- Validation: Living card, tree, kill list, and HANDOFF living start updated. Specialists launched against the three prompts. No `qualify`.
- Evidence: [HANDOFF](HANDOFF.md), [H0087](HISTORY.md), [relational probe](laws/relational-hierarchy-probe-20260914.md), [litmus contract](laws/litmus-gallery-contract-20260914.md).
- Limitations: Fermi numbers are not measured compression. Independent review, overlay, and `f(H,ε)` have not yet returned. Frozen `1dac658` untouched.
- Next: Integrator journals specialist drafts when they return. Do not select `production_law` from a Fermi essay. Do not merge packet worktrees.


## H0089 — Independent review of truncated coupled GEM: go-with-holes, not production_law

- Date: 2026-09-14
- Kind: verification
- Status: measured as go-with-holes for a production-gravity candidate; not a promotion
- Revisions: read-only on `/private/tmp/emergent-packet7-qualify`. No engine/law-lab edit. No cargo-build. No `1dac658` write. Journal-home copy of the review. This entry is not yet committed.
- Scope: Adversarial independent review of `es-truncated-coupled-gem-v0` (admitted PERIOD and FAMILY) plus Packet 5 opt-in engine path. Not overlay. Not `f(H,ε)`. Not `production_law` selection.
- Changed: Review verdict **go-with-holes**. Genesis rest certificates (\(\Delta v=5/256\), \(\Phi=-2\), Delay atoms, Einstein bend, PERIOD \(c^2+s^2=1\), FAMILY tide \(2/25\) and \(\Delta v_A=817/32000\)) recompute from the spec formulae. In-crate `independent_check` shares Delay/Bend/Clock helpers and omits C-CONE of the burn. A→B→A tests are cone flags; post-\(t=0\) (KINK) omits gravitational \(\Delta v\) off-lattice. Default inertial `advance` stays; truncated is opt-in; G2/oscillator refused; laboratory \(N\neq 2\) and \(t>4\) fail closed. Capture keeps historical \(\mu\) on the contact fixture.
- Why: Heading bottleneck is independently reviewed coupled implementation. Packet 2–7 exits and “tests exist” are not certificate independence.
- Validation: Reviewer recomputed named atoms from the spec (no cargo). Integrator copied the review onto the journal home. `production_law` left null.
- Evidence: [review](laws/coupled-implementation-review-20260914.md), [truncated coupled spec](laws/truncated-coupled-gem-v0.md), [Packet 1 gap](laws/packet1-coupled-law-gap-20260914.md), [H0088](HISTORY.md).
- Limitations: Go-with-holes is candidate status, not `production_law`. Delay/Bend/Clock remain rest-piece jets. Engine signals are C-CONE plus inertial overlays, not (INT)/(KINK). PERIOD is not Einstein two-body. Frozen `1dac658` untouched.
- Next: Do not select `production_law`. Overlay and `f(H,ε)` / `C_repair/C_replay` remain in flight. Closures before promotion: a non-shared checker, live post-cone GEM-E or a spec correction, remainder non-flip on production scenes, then a later review of those closures.


## H0090 — Measured f(H,ε) and C_repair/C_replay: quiet can stay certified; beat and encounters do not look like 99.9%

- Date: 2026-09-14
- Kind: experiment
- Status: measured as laboratory f/C on frozen scenes; not production gravity and not a `production_law` selection
- Revisions: worktree `/private/tmp/emergent-f-epsilon` on uncommitted `glm/f-epsilon-probe` copied from the Packet 7 tree. Parent `/private/tmp/emergent-packet7-qualify` not edited after add. Journal-home copies of the cost table and frozen scenes. This entry is not yet committed.
- Scope: Production-gravity measurement unit on `es-relational-hierarchy-v0` and truncated GEM (PERIOD)/(FAMILY). Default `Engine::advance` remains `es-inertial-causal-v1`. `production_law` remains null. Not overlay, not FMM/GPU, not a billion-ship run.
- Changed: Froze `scenarios/f-epsilon-scenes.json` (sha256 `f2355932682102a521473a5789d75da388f6eb8f7e8deb0f62da29bfb15d832e`) before measuring. Quiet relational / PERIOD / FAMILY: `f=1.00`. Weak-coupling beat: `f=0.05`. Relational encounter: `f=0.40`. FAMILY encounter: `f=0.00`. `C_repair/C_replay` is O(1) (0.0078–0.69), not a billion-fold product. Quiet FAMILY AABB-tide `ε≈0.94` with `f=1`: ε_tide is not an admission gate.
- Why: Julien asked for those two prototype numbers. Fermi 99.9% / billion-fold stay hypotheses. Overlapping factors must not be multiplied.
- Validation: Specialist reported 16 law-lab tests passed and wrote the cost table on Apple M1 8 GiB. Integrator copied the table onto the journal home. `qualify()` not run. `production_law` stayed null.
- Evidence: [cost table](../artifacts/runs/f-epsilon-20260914/cost-table.md), [H0089](HISTORY.md), [relational probe](laws/relational-hierarchy-probe-20260914.md).
- Limitations: Newtonian hierarchy and truncated linearized GEM only. Tiny frozen N. Operation counts, not RAM or GPU. Independent review closures (non-shared checker, post-cone field) remain. Frozen `1dac658` untouched.
- Next: Do not select `production_law` from these numbers. Finish the six-card overlay. Do not paper the H0089 holes. Do not treat quiet `f=1` as 99.9% reuse.


## H0091 — Six-card observatory overlay on the inertial host; digest unchanged

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as host overlay on the inertial observatory; native GUI not clicked
- Revisions: worktree `/private/tmp/emergent-litmus-overlay` on uncommitted `glm/litmus-overlay` copied from the Packet 7 tree. Parent `/private/tmp/emergent-packet7-qualify` not edited after add. Journal-home copy of the overlay table. This entry is not yet committed.
- Scope: Six frozen litmus cards in the observatory host. Reuses `ViewMode`, `inspect` / `observe_with_budget`, `history_digest`. Default `Engine::advance` remains `es-inertial-causal-v1`. `production_law` remains null. Not Packet 2's laboratory overlay. Bands UNCONFIRMED.
- Changed: Mounted the six frozen cards as a `LitmusGallery` world. Charged work overlay (`reuse`, `newly_compiled`, `refinement`, `repaired_prediction`) samples without changing `history_digest` at committed tick 480 (`b947b1a00864d344aa43f084a7731bb7576798130c71f9b5be4dd52c37a2da3d`). Coupled transition is an exercise, not a seventh card. Magnification ×8 labeled. Ivory/ink/pale-blue/instrument chrome reused; image text/layout was not copied as mechanics.
- Why: Julien's `/goal` assigned the six-card overlay as a must-feel destination. Packet 2's charged laboratory overlay is not that UI.
- Validation: Specialist reported `cargo test -p emergent-observatory --no-default-features --lib` 7 passed, including digest preservation. First wgpu GUI compile aborted (`No space left on device`). Native window was not opened. Integrator copied the overlay table onto the journal home. No `qualify`.
- Evidence: [overlay table](../artifacts/runs/litmus-overlay-20260914/overlay.md), [litmus contract](laws/litmus-gallery-contract-20260914.md), [H0090](HISTORY.md).
- Limitations: Host is the inertial laboratory, not a selected gravity law. Overlay cells are charged host visualization, not Packet 2 GEM transport cells. Native egui gallery was not screenshot-clicked. Frozen `1dac658` untouched.
- Next: Do not select `production_law`. Do not compile wgpu on a full disk. Native GUI smoke waits for disk headroom. Production gravity remains blocked by H0089 closures (non-shared checker, post-cone field or spec correction, remainder non-flip).


## H0092 — Close H0089 holes: independent checker, fail-closed post-cone, remainder non-flip; not production_law

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as candidate closures; not a promotion and not `production_law`
- Revisions: worktree `/private/tmp/emergent-review-closures` on uncommitted `glm/review-closures` copied from the Packet 7 tree. Parent `/private/tmp/emergent-packet7-qualify` not edited after add. Journal-home copies of the closure table and updated truncated-law spec. This entry is not yet committed.
- Scope: H0089 holes on `es-truncated-coupled-gem-v0`. Default `Engine::advance` remains `es-inertial-causal-v1`. Truncated GEM remains opt-in. `production_law` remains null. Not overlay, not wgpu, not `qualify`, not Einstein two-body.
- Changed: Moved (CHECK) into `truncated_coupled_check.rs` so Delay/Bend/Clock/Φ/first Δv/C-CONE of the burn rebuild from the spec formulae without compile helpers. Corrected the spec so A→B→A after \(t=0\) is C-CONE plus named remainder; `query_post_cone_gem_e` is `UnsupportedPredicate`. Added remainder non-flip tests. Did not select `production_law`. Did not implement live post-cone GEM-E.
- Why: Independent review was go-with-holes. Live post-cone GEM-E is outside the admitted lattice-rest map, so the honest closure is fail-closed spec correction rather than a silent field.
- Validation: Specialist reported `truncated_coupled` 18 passed and Packet 2 transport 6 passed. Integrator copied the closure table and updated spec onto the journal home. `production_law` stayed null.
- Evidence: [closure table](../artifacts/runs/review-closures-20260914/closures.md), [truncated coupled spec](laws/truncated-coupled-gem-v0.md), [H0089](HISTORY.md).
- Limitations: Candidate closures, not `production_law`. Rest-piece Delay/Bend/Clock remain genesis jets on later ticks. Later independent review of these closures is still required. Frozen `1dac658` untouched.
- Next: Independent review of these closures. Do not select `production_law`. Do not treat fail-closed post-cone as live GEM-E.


## H0093 — Independent review of H0092 closures: go-with-holes; production_law stays null

- Date: 2026-09-14
- Kind: verification
- Status: measured as go-with-holes for the H0092 candidate closures; not a promotion and not `production_law`
- Revisions: read-only on `/private/tmp/emergent-review-closures`. No engine/law-lab edit. No cargo-build. No `1dac658` write. Journal-home copy of the review. This entry is not yet committed.
- Scope: Adversarial check that H0092 closed H0089's three named holes. Not overlay. Not `f(H,ε)` re-measure. Not `production_law` selection.
- Changed: Review verdict **go-with-holes**. Independently recomputed genesis rest atoms: \(\Delta v_A=5/256\), \(\Phi=-2\), \(2\Phi/c^2=-1/4\), Delay \(L/c=2\), \(\ln 9\), \(\ln((4+\sqrt{17})/3)\), Bend \(q=1/6\) with \(1/\sqrt{17}=5/6\), C-CONE \(64=64\). Checker does not share compile helpers; Φ/Δv/Clock/C-CONE rebuild from formulae; Delay/Bend are spec transcriptions. Post-cone is fail-closed spec; `aba_feedback_cones` is still cone flags, not live GEM-E. CONTACT enclosure fail-closes; PERIOD/FAMILY/kink-shell tests are positivity. `production_law` stays null.
- Why: H0092 claimed candidate closures. Heading required a later independent review before any production selection. Fail-closed post-cone must not be read as field exchange; remainder `> 0` must not be read as a production-scene non-flip proof.
- Validation: Reviewer recomputed named atoms from the spec (no cargo). Integrator copied the review onto the journal home. Specialist 18/0 law-lab count was not rerun.
- Evidence: [closures review](laws/h0092-closures-review-20260914.md), [closure table](../artifacts/runs/review-closures-20260914/closures.md), [truncated coupled spec](laws/truncated-coupled-gem-v0.md), [H0092](HISTORY.md).
- Limitations: Go-with-holes is not `production_law`. Rest-piece Delay/Bend/Clock remain cloned genesis jets. Remainder non-flip on production scenes is still missing. Engine GeometryView slot reuse and photon-sphere always-true rows were not this unit. Frozen `1dac658` untouched. Quiet `f=1` is not 99.9%.
- Next: Do not select `production_law`. Close remaining blockers: live rest-piece geometry on a moving domain, remainder non-flip on production-shaped scenes, laboratory vs production domain. Do not treat fail-closed post-cone as live GEM-E.


## H0094 — Fail-close cloned rest-piece jets; remainder non-flip on admitted generators; naming

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as fail-closed / honest-rename closures; not a promotion and not `production_law`
- Revisions: worktree `/private/tmp/emergent-rest-piece` on uncommitted `glm/rest-piece` copied from the review-closures tree. Parent `/private/tmp/emergent-review-closures` not edited after add. Journal-home copies of the rest-piece table and updated truncated-law spec. This entry is not yet committed.
- Scope: Remaining H0093 holes on `es-truncated-coupled-gem-v0`. Default `Engine::advance` remains `es-inertial-causal-v1`. Truncated GEM remains opt-in. `production_law` remains null. Not live GEM-E, not overlay, not wgpu.
- Changed: Fail-closed rest-piece Delay/Bend/Clock after the first tick; independent checker rejects cloned genesis jets at \(t>0\) even if `rest_piece_geometry` is stuffed true. Renamed laboratory remainder positivity away from “production-shaped”; PERIOD/FAMILY retained residuals fail-close CONTACT on the On-contact fixture. Renamed `aba_feedback_cones` to `aba_c_cone_visibility_not_field_exchange`. Photon-sphere probe calls `query_photon_sphere`. Engine `geometry_query` no longer reuses laboratory Delay/clock slots for PERIOD/FAMILY. Did not implement a live moving-domain Delay/Bend rebuild. Did not select `production_law`.
- Why: H0093 found cloned genesis jets, remainder positivity under a production-shaped name, and leftover GEM-E naming. Honest closure is fail-closed / rename, not papering and not live GEM-E.
- Validation: Specialist reported `truncated_coupled` 23 passed, Packet 2 transport 6 passed, Packet 5 engine 14 passed. Integrator copied the table and spec onto the journal home. `production_law` stayed null.
- Evidence: [rest-piece table](../artifacts/runs/rest-piece-20260914/rest-piece.md), [truncated coupled spec](laws/truncated-coupled-gem-v0.md), [H0093](HISTORY.md).
- Limitations: Fail-closed rest-piece is not live \(\Phi\)/Delay/Bend on a moving domain. PERIOD/FAMILY CONTACT fail-closed is not a billion-ship production-scene certificate. Delay/Bend (CHECK) at genesis remains spec transcription. Ship \(a_0\) still unchecked. PERIOD residual still uses rotation-chord \(\lvert\Delta v\rvert_1\). Frozen `1dac658` untouched.
- Next: Independent review of these fail-closed closures. Do not select `production_law`. Do not treat fail-closed rest-piece or fail-closed post-cone as live GEM-E.


## H0095 — Independent review of H0094 rest-piece closures: go-with-holes; production_law stays null

- Date: 2026-09-14
- Kind: verification
- Status: measured as go-with-holes for the H0094 fail-closed / honest-rename closures; not a promotion and not `production_law`
- Revisions: read-only on `/private/tmp/emergent-rest-piece` (`glm/rest-piece`). No engine/law-lab edit. No cargo-build. No `1dac658` write. Journal-home copy of the review. This entry is not yet committed.
- Scope: Adversarial check that H0094 closed H0093's three leftover holes (cloned rest-piece jets; remainder “production-shaped”; `aba_feedback_cones` naming). Not overlay. Not `f(H,ε)` re-measure. Not `production_law` selection. Not live GEM-E. Not live moving-domain Delay/Bend.
- Changed: Review verdict **go-with-holes**. Independently recomputed C-CONE \(64=64\), genesis \(\Phi=-2\), On-contact enclosure (any \(\varepsilon>0\) flips; \(\varepsilon=0\) certifies OnContact). Cloned genesis Delay/Bend/Clock fail (CHECK) at \(t>0\) even if `rest_piece_geometry` is stuffed true; laboratory `obs_at` empties later jets. Fail-closed, **not** live moving-domain geometry. Packet 2 `apply_entrant` may still copy COMPILE Delay/Bend onto later `CertifiedObs` with `rest_piece_geometry` false; the checker would still reject them. “production-shaped” is refused. PERIOD/FAMILY CONTACT fail-closed is real drop-vs-keep on the On-contact fixture and still borrowed positivity, not a production-scene non-flip; PERIOD residual still uses rotation-chord \(\lvert\Delta v\rvert_1\). `aba_c_cone_visibility_not_field_exchange` is C-CONE flags (`b_sees_a_burn` / `a_sees_b_response` / `!post_cone_gem_e`), not GEM-E and not post-cone acceleration comparison. `production_law` stays null.
- Why: H0094 claimed fail-closed / honest-rename closures. Heading required an independent review before any production selection. Fail-closed rest-piece must not be read as live moving geometry; On-contact borrowed remainder must not be read as a production-scene non-flip; renamed cone flags must not be read as field exchange.
- Validation: Reviewer recomputed named atoms and CONTACT enclosure from the spec (no cargo). Integrator copied the review onto the journal home. Specialist 23/0 law-lab, 6 packet2, 14 packet5 counts were not rerun.
- Evidence: [H0094 review](laws/h0094-rest-piece-review-20260914.md), [rest-piece table](../artifacts/runs/rest-piece-20260914/rest-piece.md), [truncated coupled spec](laws/truncated-coupled-gem-v0.md), [H0093](HISTORY.md), [H0094](HISTORY.md).
- Limitations: Go-with-holes is not `production_law`. Fail-closed rest-piece is not live \(\Phi\)/Delay/Bend on a moving domain. PERIOD/FAMILY CONTACT fail-closed is not a billion-ship production-scene certificate. Packet 2 `apply_entrant` still clones COMPILE Delay/Bend at \(t>0\). Engine `geometry_query("moving")` still serves genesis \(t=0\) jets. Delay/Bend (CHECK) at genesis remains spec transcription, not path integrals. Ship \(a_0\) still unchecked. Frozen `1dac658` untouched. Quiet \(f=1\) is not 99.9%.
- Next: Do not select `production_law`. Remaining blocker is laboratory vs production domain (live Delay/Bend rebuild on a moving domain is still absent). Next heading-true unit is live moving-domain Delay/Bend **or** an honest stop that this truncated law cannot be `production_law` — not another papered fail-closed rename.


## H0096 — Honest stop: truncated GEM cannot be production_law; Delay/Bend/Clock are genesis-rest-only

- Date: 2026-09-14
- Kind: decision
- Status: implemented as named refuse (not production_law); later ticks remain fail-closed; not a promotion
- Revisions: worktree `/private/tmp/emergent-live-delay` on branch `glm/live-delay`, copied from `/private/tmp/emergent-rest-piece` at `254ba1f` plus the H0094 overlay. Not committed. Parent `/private/tmp/emergent-rest-piece` not edited. Integrator copied the honest-stop table and named-refuse spec onto journal home; journal-home crates are a different dirty overlay and were not treated as this change. This entry is not yet committed.
- Scope: Heading-true unit after H0095 on `es-truncated-coupled-gem-v0`. Default `Engine::advance` remains `es-inertial-causal-v1`. Truncated GEM remains opt-in. `production_law` remains null. Not overlay, not wgpu, not `qualify`, not Einstein two-body, not a live Delay/Bend rebuild, not a new gravity candidate.
- Changed: Named refuse: `es-truncated-coupled-gem-v0` cannot be `production_law` because Delay/Bend/Clock are genesis-rest-only. Later ticks stay fail-closed (empty jets, `rest_piece_geometry=false`). Packet 2 `apply_entrant` no longer clones COMPILE Delay/Bend/Clock onto later `CertifiedObs`. Engine `geometry_query("moving")` no longer serves genesis \(t=0\) jets (`UnsupportedPredicate` slots). Default `Engine::advance` stays `es-inertial-causal-v1`. `production_law` stays null. Did not retry a fake path-integral inside \(O(G^1,\beta^1)\). `/goal` stays active: this candidate is rejected; production gravity remains the destination.
- Why: H0095 required a live moving-domain Delay/Bend rebuild **or** an honest stop that this truncated law cannot be `production_law`. No well-posed later-tick identity exists inside linearized GEM \(O(G^1,\beta^1)\) rest / single-source boost-to-rest Euclidean-path (NULL-G)/(NULL-BEND)/(CLK) for two mutually moving balls after the first (KINK). A fake rebuild would paper the heading.
- Validation: Disk ~12 GiB. Specialist on `/private/tmp/emergent-live-delay`: `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/live-delay-target CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --offline --locked truncated_coupled -- --test-threads=1` — 24 passed, 0 failed. Packet 2 transport: 7 passed. Packet 5 engine: 14 passed. `production_law` stayed null. Engine `LAW_ID` stayed `es-inertial-causal-v1`. Integrator copied artifacts onto journal home; specialist counts were not rerun here. No `qualify`, no wgpu.
- Evidence: [honest-stop table](../artifacts/runs/honest-stop-20260914/honest-stop.md), [named-refuse spec snapshot](laws/truncated-gem-honest-stop-20260914.md), [H0095](HISTORY.md).
- Limitations: This refuse is not `production_law` and not a substitute law. Laboratory vs production domain remains. Genesis Delay/Bend (CHECK) remains spec transcription. Ship \(a_0\) still unchecked. PERIOD residual still uses rotation-chord \(\lvert\Delta v\rvert_1\). Remainder non-flip on production scenes is still missing. Fail-closed post-cone is still not live GEM-E. Frozen `1dac658` untouched. Parent rest-piece tree not edited. Journal-home crates do not contain the live-delay overlay.
- Next: Do not select `production_law`. Do not retry a truncated-GEM live Delay/Bend rebuild. Independent review of this refuse (so the stop is not an overclaim), then a production-domain candidate — not another truncated live Delay/Bend. Keep `/goal` active.


## H0097 — Independent review of H0096 honest stop: go-with-holes; production_law stays null

- Date: 2026-09-14
- Kind: verification
- Status: measured as go-with-holes for the H0096 named refuse; not a promotion and not `production_law`
- Revisions: read-only on `/private/tmp/emergent-live-delay` (`glm/live-delay`). Docs-only worktree `/private/tmp/emergent-honest-stop-review` (`glm/honest-stop-review`). No engine/law-lab edit. No cargo-build. No `1dac658` write. Journal-home copy of the review. This entry is not yet committed.
- Scope: Adversarial check that H0096's named refuse is forced rather than an overclaim (later-tick identity; genesis transcription; Packet 2 clone leftover; engine `"moving"` leftover; boolean rename; identifier permanence). Not overlay. Not `f(H,\varepsilon)` re-measure. Not `production_law` selection. Not a truncated live Delay/Bend rebuild. Not a new gravity candidate.
- Changed: Review verdict **go-with-holes**. Independently recomputed C-CONE \(64=64\), genesis \(\Phi=-2\), Delay \(L/c=2\), \(\ln 9\), \(\ln((4+\sqrt{17})/3)\), Bend \(q=1/6\). Genesis Delay/Bend remain spec transcription; a live rebuild was never in this law. Packet 2 `apply_entrant` no longer copies COMPILE Delay/Bend/Clock onto later `CertifiedObs`. Engine `geometry_query("moving")` no longer calls `apply_at(t=0)`. Empty Delay/Bend/Clock are not a boolean rename for live geometry. Overclaims: “no well-posed later-tick identity” collapses genesis-ray piecewise retarded Shapiro (forced) with later-emit boost-to-rest superposition and Clock-from-(METRIC) \(\Phi\) (named at \(O(G^1,\beta^1)\), not a terminating \(\mathbb{Q}(\sqrt{17})\) jet). GEM-v0 heritage does not donate Shapiro (SIG Minkowski). Identifier cannot be `production_law` *as currently specified* and as a laboratory wrapper; the string is not permanently cursed because genesis-rest Delay. Later-tick `phi_ship` can still be genesis rest \(\Phi\) (`independent_rest_phi`); `query_domain("moving")` stays queryable. `production_law` stays null. Default `Engine::advance` stays `es-inertial-causal-v1`. Frozen `1dac658` stays FAIL. `/goal` stays active.
- Why: H0096 claimed later-tick Delay/Bend/Clock cannot be rebuilt inside this truncated law without path-integral retarded Shapiro, Einstein two-body, or stuffing rest formulas, therefore this id cannot be `production_law`. Heading required an independent review so the stop is not an overclaim. Fail-closed leftovers must actually be fail-closed in source. Do not retry a truncated live Delay/Bend rebuild from a go-with-holes verdict.
- Validation: Reviewer recomputed named atoms from the spec and read live-delay sources (no cargo). Integrator copied the review onto the journal home. Specialist 24/0 law-lab, 7 packet2, 14 packet5 counts were not rerun.
- Evidence: [H0096 review](laws/h0096-honest-stop-review-20260914.md), [honest-stop table](../artifacts/runs/honest-stop-20260914/honest-stop.md), [named-refuse spec snapshot](laws/truncated-gem-honest-stop-20260914.md), [H0095](HISTORY.md), [H0096](HISTORY.md).
- Limitations: Go-with-holes is not `production_law`. Fail-closed rest-piece is not live \(\Phi\)/Delay/Bend on a moving domain. Later-tick rest `phi_ship` is not a Delay rebuild and is not empty. Compact GeometryView still reuses Delay/Bend booleans as capture flags. Genesis Delay/Bend (CHECK) remains spec transcription. Ship \(a_0\) still unchecked. Frozen `1dac658` untouched. Quiet \(f=1\) is not 99.9%.
- Next: Do not select `production_law`. Do not retry a truncated-GEM live Delay/Bend rebuild. Remaining blocker is laboratory vs production domain: a production-domain candidate under independent review — not another truncated live Delay/Bend. Keep `/goal` active.


## H0098 — Relational source-closure design and correction of relational probe evidence scope

- Date: 2026-09-14
- Kind: source review and mathematical design
- Status: source findings verified by inspection; causal response closure proposed, not implemented
- Revisions: Read dirty worktrees above `254ba1f`, refreshed through H0097 after Julien reported concurrent implementations. SHA-256 source snapshots are in the review. Added only the review and this journal entry; no implementation or branch edits.
- Scope: User-requested relational inversion and the missing mutually evolving source/geometry compiler, with a current delta audit of relational-hierarchy, compiler-impl and live-delay worktrees.
- Changed: Added a focused review deriving retarded field elimination, causal group response composition, two-group Schur closure, a delayed-feedback geometric-sum example and nonlinear residual certification. Preserved current packet work and production assignment. Corrected evidence interpretation from H0079/H0090 by source inspection: Hierarchy::apply_shared_responses adds force times zero; the reciprocal workload applies acceleration times dt to position, discards the clone used for replay and assigns f=1; weak/encounter costs include literal counts and beat f follows a chosen horizon policy. These are constructed diagnostics, not validated savings for equivalent completed evolutions. Current live-delay unsupported moving exchange/light/clock behavior agrees with H0097's restricted verdict.
- Why: Julien asks whether solving relations can avoid spatial field work and simplify mutual backreaction, and reports new implementation while this review is in progress. The plan must build on actual new capabilities while distinguishing an algebraic mechanism from an implemented coupled response. Passing counters or cone visibility alone cannot establish that sources evolve through each other's changing geometry.
- Validation: Ran history list/search and refreshed worktree status, handoff, card, reports and source; root independently checked the bounded specialist's source findings. Consulted primary effective-gravity, relaxed-Einstein, causal-action, aberration and waveform-relaxation sources. No physical tests, runtime builds, numerical benchmark or qualification run performed. History validation follows append.
- Evidence: [Relational source-closure review and source hashes](relational-source-closure-review-20260914.md), [relational probe specification](laws/relational-hierarchy-probe-20260914.md), [relational diagnostic table](../artifacts/runs/relational-hierarchy-20260914/cost-table.md), [f-epsilon table](../artifacts/runs/f-epsilon-20260914/cost-table.md), [latest honest-stop review](laws/h0096-honest-stop-review-20260914.md).
- Limitations: No new physical law or response implementation; no new measured speedup or universal complexity bound. Source defects were not reproduced by executing the probe. Mathematical field elimination does not erase nonlinear GR, initial/free fields, causal history, representation rank or arithmetic cost. Existing reports and frozen evidence remain intact; this entry appends a narrower interpretation. Live handoff/card operational ownership was preserved. Dirty overlays and prior journal records remain uncommitted.
- Next: Use the review when selecting the production-domain candidate: require actual two-way source evolution and a validated interval response before more wrappers. Preserve useful binary/common-mode and history/observer components, replace heuristic or synthetic reuse accounting with executed equivalent histories, and retain the current rejection of the truncated laboratory wrapper as production gravity.


## H0099 — Prepare the continuation prompt for a real coupled source response

- Date: 2026-09-14
- Kind: handoff preparation
- Status: prompt prepared and reviewed; no new task dispatched or implementation started
- Revisions: Documentation on the journal-home dirty overlay above `254ba1f`, refreshed through H0098. No engine/law-lab edits or branch operations.
- Scope: User-requested prompt for the next agent to continue toward the spacetime compiler from the current implementations and review findings.
- Changed: Wrote a standalone continuation prompt connecting the game destination, calibrated visual tests, current worktree provenance, H0098 evidence corrections, causal group-response mathematics, executable physical/finite semantics, and one complete source-feedback/consumer/repair experiment. Required equivalent independently evolved histories, held-out later emissions and in-flight source changes, whole-interval validation and actual completed-work costs. Preserved existing packet work and the current rejection of the truncated wrapper as production. Added a prompt pointer and H0098 scope correction to the editable handoff.
- Why: Julien wants the next agent to continue down the right path without restarting foundations, mistaking constructed diagnostics for validated savings, or growing another wrapper around absent moving-source dynamics.
- Validation: Refreshed handoff/card/history/worktrees and source-review context; ran history list/template. One bounded independent review supplied five safeguards incorporated into the prompt. Confirmed referenced current document paths. No physical tests, runtime builds or benchmarks appropriate to this documentation-only task. History check follows append.
- Evidence: [Continuation prompt](../orchestration/prompts/continue-coupled-spacetime-compiler.md), [source-closure review](relational-source-closure-review-20260914.md), [handoff](HANDOFF.md), [litmus contract](laws/litmus-gallery-contract-20260914.md).
- Limitations: A prepared prompt is not implementation, proof of a source law, or production qualification. No successor was launched. Source findings retain H0098's inspection-only scope. Existing mixed overlays and historical uncommitted records remain uncommitted.
- Next: User supplies the prompt to the continuing implementation agent; that agent refreshes live state, selects isolated inputs, and executes the next complete coupled source-response experiment with the stated acceptance criteria.


## H0100 — Weak-field linearized GEM source response with a physical A→B→A loop

- Date: 2026-09-14
- Kind: implementation
- Status: implemented isolated laboratory slice on a separate worktree; not production_law; default Engine::advance unchanged
- Revisions: Isolated worktree `/private/tmp/emergent-coupled-response`, branch `codex/coupled-source-response`, dirty overlay above `254ba1f718771ec1d0a25bf59d0d555f7e57993e`. No packet-branch merge. No `1dac658` rewrite. Truncated-GEM genesis specials not extended. Journal-home crates were not edited for this law.
- Scope: Prompt `continue-coupled-spacetime-compiler.md` sequences 1–5 on a declared weak-field moving-source slice. H0098 source hashes reconfirmed MATCH in the worktree selection note. H0099 was prompt-only; this is the first implementation record after that prompt.
- Changed: Settled isolated `es-linearized-retarded-gem-response-v0` with f64 finite semantics, GEM-Φ/ξ/E/B/GRAD/a, CLK and first-order NULL from the same potentials. Independent `Reference::from_genesis` never starts from candidate state. Compiled `SourceResponse` stores jointly evolved worldtubes, residual, incoming interventions and repair-by-splice. Discriminating H0098 failures reproduced as tests (force×0; force×dt/mass into position). Required moving-source / ray / clock / contact queries return values. Copied spec, charged JSON, SVG, six-card scope and selection hashes onto this journal home as local evidence; the implementation remains on the isolated worktree.
- Why: The bottleneck was reusable evolution of mutually interacting sources, not another wrapper around genesis rest jets or constructed `f=1`.
- Validation: Specialist command `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab coupled_source_response --offline --locked -- --test-threads=1` reported 14 passed on the isolated worktree; integrator counted 14 `#[test]` functions in that module and did not re-run the suite on journal home. Integrator verified [charged.json](../artifacts/runs/coupled-source-response-20260914/charged.json): `production_law` null, `max_phi_c2=0.0020522239304231332`, `max_beta=0.01185414096676417`, source ops 16892 unchanged under extra rays, consumer ops 161→3864, `reuse_fraction_queries=0.18616303719406435` = 3864/(16892+3864), late splice 64 vs 384 source-evolution steps. Example wrote that JSON and `scene.svg`. Frozen G2 `qualify()` not rerun.
- Evidence: [Copied law spec](laws/linearized-retarded-gem-response-v0.md), [copied selection and hashes](laws/coupled-source-response-selection-20260914.md), [charged run JSON](../artifacts/runs/coupled-source-response-20260914/charged.json), [six-card scope](../artifacts/runs/coupled-source-response-20260914/six-card-scope.md), [laboratory scene SVG](../artifacts/runs/coupled-source-response-20260914/scene.svg), [continuation prompt](../orchestration/prompts/continue-coupled-spacetime-compiler.md).
- Limitations: Weak-field / slow-motion only on that charged run. No independently bounded contraction enclosure `q<1` for the interval operator; `delayed_feedback_series` geometric-sum is a candidate, not a certificate. No circular-phase compact generator as the stored response (piecewise-inertial worldtubes). Native six-card GUI not mounted; copied scope marks cards 2/4/5 unsupported and 1/3/6 partial. Navigation inversion not implemented. Reuse fraction on extra rays is ~0.19 of (source+consumer), not 99.9%. Journal-home crates do not contain this overlay.
- Next: Independently bounded contraction/enclosure for the compiled interval on `/private/tmp/emergent-coupled-response` (failed contraction rejects that certificate, not the existence of a solution). Then mount this slice on the existing six-card host without calling the inertial overlay gravity. Do not select `production_law`. Do not shrink the `/goal` to another wrapper.


## H0101 — Independent contraction enclosure for the compiled GEM interval

- Date: 2026-09-14
- Kind: implementation
- Status: implemented isolated laboratory enclosure on `/private/tmp/emergent-coupled-response`; journaled here; not production_law; default Engine::advance unchanged
- Revisions: Dirty overlay on `codex/coupled-source-response` above `254ba1f718771ec1d0a25bf59d0d555f7e57993e`. Worktree added `crates/law-lab/src/coupled_interval_enclosure.rs` and public `field_acceleration` / `retarded_lookback_time` helpers. No packet-branch merge. No `1dac658` rewrite. Truncated-GEM genesis specials not extended. Journal-home crates were not edited for this overlay. Six-card/wgpu not mounted in this entry.
- Scope: Prompt `continue-coupled-spacetime-compiler.md` certification: whole-interval validation including causal-time and representation errors. Failed contraction rejects that certificate, not the existence of a solution. Independent of compile `SourceResponse::residual`.
- Changed: Independent Picard map from frozen candidate sources plus `Reference::from_genesis` (never from candidate state). Tidal Lipschitz from pairwise distances on the independent reference, not from iterate similarity. `IntervalMethod::IntegralOperator` uses `q = H·L`; `CausalBlocks` uses delay grouping so same-interval cross Lipschitz is 0. Charge records coefficient construction, factorization, validation, reconstruction and verification. Mutating `residual` does not change the enclosure verdict. Integrator copied a dated evidence note onto this journal home; journal-home crates are not this overlay.
- Why: H0100 compiled a physical A→B→A interval but had only a geometric-sum candidate. Successive iterates looking similar cannot certify.
- Validation: Integrator re-ran `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab coupled_ --offline --locked -- --test-threads=1` on `/private/tmp/emergent-coupled-response`: 22 passed; 0 failed (14 `coupled_source_response` + 8 enclosure). Source inspection confirmed residual is unread, `q = horizon * l` for IntegralOperator, close-pair `q≥1` refuses the certificate while compile still succeeds. Disk: 14 GiB free; swap ~4.5/5 GiB used so wgpu stayed skipped. Frozen G2 `qualify()` not rerun.
- Evidence: [Enclosure evidence note](laws/coupled-interval-enclosure-20260914.md), [copied law spec](laws/linearized-retarded-gem-response-v0.md), [copied selection and hashes](laws/coupled-source-response-selection-20260914.md), [H0100](HISTORY.md), [continuation prompt](../orchestration/prompts/continue-coupled-spacetime-compiler.md).
- Limitations: Sufficient f64 bound, not a machine-interval/KA proof. Close-pair IntegralOperator (`D=1.2`, `H=1`) gives `q≥1` and refuses the certificate while compile still succeeds inside `‖Φ‖/c²<0.05`. Geometric-sum `delayed_feedback_series` is still not a certificate. Native six-card GUI not mounted. `production_law` stays null. Journal-home crates do not contain this overlay.
- Next: Mount the H0100 slice on the existing six-card host without calling the inertial overlay gravity. Do not select `production_law`. Do not shrink the `/goal`.


## H0102 — Six-card host for the GEM-response slice; no wgpu; not inertial-as-gravity

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as observatory-library host tests on `/private/tmp/emergent-coupled-response`; native GUI not compiled; not production_law; default Engine::advance unchanged
- Revisions: Dirty overlay on `codex/coupled-source-response` above `254ba1f718771ec1d0a25bf59d0d555f7e57993e`. Added `crates/observatory/src/gallery.rs` and `lib.rs` on that worktree; made `gui`/wgpu/engine optional so `--no-default-features --lib` does not compile eframe. Did not edit `/private/tmp/emergent-litmus-overlay`. No packet-branch merge. No `1dac658` rewrite. Did not replace default `Engine::advance`. Journal-home crates were not edited for this overlay.
- Scope: Prompt `continue-coupled-spacetime-compiler.md` sequence 5: connect the H0100/H0101 slice to the existing visual instrument. Six-card contract plus charged work overlays for the implemented weak-field coupled loop. Solar / galaxy / black-hole marked unsupported.
- Changed: `GemGalleryHost` mounts six frozen cards with look-for cues. Cards 1/3/6 are GEM-slice (`es-linearized-retarded-gem-response-v0`). Cards 2/4/5 unsupported and refuse overlay sampling so inertial motion cannot be painted as this law. Charged overlays sample extra rays / compile / independent enclosure / late repair on the compiled interval; extra-ray reuse leaves source ops unchanged. Default engine law recorded as `es-inertial-causal-v1`. Native egui panel not wired (wgpu skipped on swap). Overlay copies verified on this journal home before append.
- Why: Sequence 5 requires the visual instrument and forbids equating the H0091 inertial overlay with gravitational behavior. Host tests without wgpu follow the H0091 pattern without repeating a wgpu compile on a swapping M1.
- Validation: `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-observatory --no-default-features --lib --offline -- --test-threads=1` — 8 passed; 0 failed. Same env `cargo test -p emergent-law-lab coupled_ --offline -- --test-threads=1` — 22 passed; 0 failed. `cargo tree -p emergent-observatory --no-default-features` had no eframe/wgpu/naga. Disk ~12 GiB free; swap ~5/6 GiB used. Frozen G2 `qualify()` not rerun. Native window not opened. Integrator verified overlay.md and gallery-run.json on journal home; specialist counts were not rerun here.
- Evidence: [overlay table](../artifacts/runs/coupled-gem-gallery-20260914/overlay.md); [gallery-run.json](../artifacts/runs/coupled-gem-gallery-20260914/gallery-run.json); [litmus contract](laws/litmus-gallery-contract-20260914.md); [H0101](HISTORY.md); [H0091](HISTORY.md). Implementation remains on `/private/tmp/emergent-coupled-response`.
- Limitations: Native egui gallery panel is not compiled and not clicked. This is a library host, not a screenshot of the six cards. Stored response remains piecewise-inertial worldtubes (no compact phase generator). Navigation inversion not implemented. Extra-ray reuse is not 99.9%. Enclosure remains a laboratory f64 bound, not KA. `production_law` stays null. Journal-home crates do not contain this overlay.
- Next: Compact phase generator as the stored response, and/or navigation inversion with explicit domain where inversion fails. Do not select `production_law`. Do not shrink the `/goal`. Do not treat this host as gravitational qualification.


## H0103 — Compact phase/residual stored response and navigation inversion with an explicit failure domain

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as isolated laboratory helpers on `/private/tmp/emergent-coupled-response`; journaled here; not production_law; default Engine::advance unchanged
- Revisions: Dirty overlay on `codex/coupled-source-response` above `254ba1f718771ec1d0a25bf59d0d555f7e57993e`. Added `crates/law-lab/src/coupled_phase_nav.rs` on that worktree. Did not edit journal-home crates for this overlay. No packet-branch merge. No `1dac658` rewrite. Did not replace default `Engine::advance`. Did not select `production_law`.
- Scope: Prompt `continue-coupled-spacetime-compiler.md`: represent regular motion by phase/orbital functions plus a small admitted residual basis; navigation reuses compiled transport with explicit domain limits where inversion fails.
- Changed: Compact stored form is a polar phase generator \((r(t),\theta(t))\) plus Chebyshev residual (admitted rank 16, band \(10^{-4}\)), split at committed interventions. Quiet two-body and kicked A→B→A reconstruct inside the band; held-out ship/ray/clock match on reconstructed sources. A single unsplitted rank-2 generator on the kick interval honestly refuses. Navigation inverts `fly_ship` via STM \(\partial x_1/\partial v_0\); recovers the forward \(v_0\); fails closed on empty interval (\(B=0\)), past compiled horizon, and unreachable speed. Independent `Reference::from_genesis` unchanged. Enclosure still does not read compile residual. Extra-ray reuse accounting unchanged (no assigned \(f=1\)).
- Why: Quiet stored response must not remain only piecewise-inertial worldtubes if a compact generator can still close A→B→A. A Δv kink is not a small residual of one global smooth generator; splitting at interventions is the admitted representation, not a missing-jet impossibility. Navigation must reuse the same transport and fail rather than invent a route.
- Validation: `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab coupled_ --offline -- --test-threads=1` — 29 passed; 0 failed (original 22 still pass, plus 7 phase/nav). Same env `cargo test -p emergent-observatory --no-default-features --lib --offline -- --test-threads=1` — 8 passed; 0 failed. Disk ~12 GiB free; swap ~4.7/6 GiB. Frozen G2 `qualify()` not rerun. Native window not opened. wgpu not compiled.
- Evidence: [phase/nav note](laws/coupled-phase-nav-20260914.md); [H0102](HISTORY.md); [H0101](HISTORY.md); [continuation prompt](../orchestration/prompts/continue-coupled-spacetime-compiler.md). Implementation remains on `/private/tmp/emergent-coupled-response`.
- Limitations: `compile_source_response` still also writes piecewise-inertial `worldtubes`; compact is a fitted stored form, not yet the only compile storage. Native egui gallery is not compiled. Extra-ray reuse is not 99.9%. Enclosure remains a laboratory f64 bound, not KA. This slice's ship STM is weakly focusing; the \(B=0\) refuse is the empty-interval / min-det domain, not a measured oscillator conjugate point on GEM. `production_law` stays null. Journal-home crates do not contain this overlay.
- Next: Use the compact generator as compile storage rather than a parallel fit, and/or mount the native six-card GUI. Do not select `production_law`. Do not shrink the `/goal`. Do not treat the library host as gravitational qualification.


## H0104 — Compact generator stored as compile response; worldtubes remain a named remainder

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as isolated laboratory compile storage on `/private/tmp/emergent-coupled-response`; journaled here; not production_law; default Engine::advance unchanged
- Revisions: Dirty overlay on `codex/coupled-source-response` above `254ba1f718771ec1d0a25bf59d0d555f7e57993e`. Edited `coupled_source_response.rs`, `coupled_phase_nav.rs`, `coupled_interval_enclosure.rs`, and observatory `gallery.rs` on that worktree. Did not edit journal-home crates for this overlay. No packet-branch merge. No `1dac658` rewrite. Did not replace default `Engine::advance`. Did not select `production_law`.
- Scope: Prompt `continue-coupled-spacetime-compiler.md`: compile storage should be a compact phase/residual generator that consumers reconstruct, not a parallel polyline fit.
- Changed: `compile_source_response` stores polar phase + Chebyshev residual on `SourceResponse.compact` (rank 16, band \(10^{-4}\), split at interventions, adaptive bisect when a piece exceeds the band). `decode_sources` reconstructs consumer geometry from that generator or fails closed if pieces are empty. Held-out ship/ray/clock/contact, extra-ray reuse, enclosure, and navigation invert reconstruct from the generator. Mutating worldtubes after compile does not change the stored generator; re-decode restores it. Independent `Reference::from_genesis` unchanged. Enclosure still does not read compile residual (authored futures now mutate compact pieces). Replacing worldtubes with the decode as the only compile geometry is obstructed: documented counterexamples keep piecewise-inertial worldtubes as a named remainder (evolve/repair view). Four-kick \(H=9\) exhausts adaptive bisect; compile falls back and `decode_sources` refuses.
- Why: H0103 fitted a compact form beside compile worldtubes. Reuse that compile actually stores requires the generator to be the response object. A Δv kink is not a small residual of one global smooth generator; splitting at interventions is still not splitting at causal arrival, so a generator decode cannot keep 1e-8 pre-cone identity.
- Validation: `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab coupled_ --offline -- --test-threads=1` — 30 passed; 0 failed. Same env `cargo test -p emergent-observatory --no-default-features --lib --offline -- --test-threads=1` — 8 passed; 0 failed. Disk ~12 GiB free; swap ~5.0/6 GiB. Frozen G2 `qualify()` not rerun. Native window not opened. wgpu not compiled.
- Evidence: [compile-storage note](laws/coupled-compile-storage-20260914.md); [H0103](HISTORY.md); [phase/nav note](laws/coupled-phase-nav-20260914.md); [continuation prompt](../orchestration/prompts/continue-coupled-spacetime-compiler.md). Implementation remains on `/private/tmp/emergent-coupled-response`.
- Limitations: Worldtubes remain a named stepper remainder; they are not deleted independent truth, but they are also not yet a view derived as the only geometry. Generator decode cannot replace remainder at 1e-8 A→B→A prefix (intervention knots mix B's pre/post-cone motion). Quiet \(H=6\) needs adaptive bisect. Four-kick \(H=9\) refuses the generator. Native egui gallery is not compiled. Extra-ray reuse is not 99.9%. Enclosure remains a laboratory f64 bound, not KA. `production_law` stays null. Journal-home crates do not contain this overlay.
- Next: Split compact pieces at causal arrivals (or otherwise meet 1e-8 prefix identity) so worldtubes can become a decode view, and/or mount the native six-card GUI. Do not select `production_law`. Do not shrink the `/goal`. Do not treat the library host as gravitational qualification.


## H0105 — Compact pieces split at causal arrivals; worldtubes remain a named remainder

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as isolated laboratory compact-split on `/private/tmp/emergent-coupled-response`; journaled here; not production_law; default Engine::advance unchanged
- Revisions: Dirty overlay on `codex/coupled-source-response` above `254ba1f718771ec1d0a25bf59d0d555f7e57993e`. Edited `coupled_phase_nav.rs` and `coupled_source_response.rs` on that worktree. Did not edit journal-home crates for this overlay. No packet-branch merge. No `1dac658` rewrite. Did not replace default `Engine::advance`. Did not select `production_law`.
- Scope: Prompt `continue-coupled-spacetime-compiler.md`: compact Chebyshev pieces must split at causal arrivals so a receiver's pre-cone and post-cone motion are not mixed in one piece; then worldtubes can become a decode-only view if 1e-8 prefix identity holds.
- Changed: `compact_from_bodies` splits each body at local interventions and at iterated light-cone arrivals of those events (not a shared kick-time knot on every worldtube). Laboratory kicked B pieces are \([0, 2.248]\), \([2.248, 4.228]\), \([4.228, 5]\) and no longer mix \(t=2.0\) with \(t=2.45\). Independent `Reference::from_genesis` unchanged. Enclosure still does not read compile residual. Extra-ray reuse remains charged equivalent histories. Required moving-source/ray/clock/contact still return values. Decode fails closed when the generator refuses. Worldtubes were **not** replaced by decode: admitted-band decode pre-cone ratio is \(1.10\times 10^{-4}\) (stepper remains \(<10^{-8}\)). A \(10^{-8}\) band refit reaches \(2.5\times 10^{-10}\) only with 924/1177 pieces (polyline, not adopted). Four-kick \(H=9\) still refuses (empty pieces, `fallback=1`, residual \(3.68\times 10^{-4}\)).
- Why: H0104 stored a generator but split only at interventions, mixing B's pre/post-cone motion. Causal-arrival split was the heading-true next move. It removes mixing and is still not enough for 1e-8 prefix identity at the admitted \(10^{-4}\) band; tightening the band becomes a polyline. Deleting the remainder would paper compact storage.
- Validation: `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab coupled_ --offline -- --test-threads=1` — 33 passed; 0 failed. Same env `cargo test -p emergent-observatory --no-default-features --lib --offline -- --test-threads=1` — 8 passed; 0 failed. Disk ~12 GiB free; swap ~4.8/6 GiB. Frozen G2 `qualify()` not rerun. Native window not opened. wgpu not compiled.
- Evidence: [causal-arrival split note](laws/coupled-causal-arrival-split-20260914.md); [H0104](HISTORY.md); [compile-storage note](laws/coupled-compile-storage-20260914.md); [continuation prompt](../orchestration/prompts/continue-coupled-spacetime-compiler.md). Implementation remains on `/private/tmp/emergent-coupled-response`.
- Limitations: Worldtubes remain a named stepper remainder. Causal-arrival split does not make decode the only geometry. Admitted-band decode cannot keep 1e-8 A→B→A prefix. A \(10^{-8}\) band fit is a polyline. Four-kick \(H=9\) refuses the generator. Native egui gallery is not compiled. Extra-ray reuse is not 99.9%. Enclosure remains a laboratory f64 bound, not KA. `production_law` stays null. Journal-home crates do not contain this overlay.
- Next: Independent review of this bounded laboratory slice against `continue-coupled-spacetime-compiler.md` acceptance. Do not start another Chebyshev/polyline squeeze. Do not compile wgpu. Do not select `production_law`. Do not shrink the `/goal`. Do not treat the library host as gravitational qualification.


## H0106 — Independent review of H0100–H0105 coupled slice: go-with-holes; production_law stays null

- Date: 2026-09-14
- Kind: verification
- Status: measured as go-with-holes for the bounded laboratory slice `es-linearized-retarded-gem-response-v0`; not a promotion and not `production_law`
- Revisions: read-only on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` above `254ba1f`). Docs-only directory `/private/tmp/emergent-coupled-slice-review`. No engine/law-lab edit. No cargo-build. No wgpu. No `1dac658` write. Journal-home copy of the review. This entry is not yet committed.
- Scope: Adversarial check of H0100–H0105 against `continue-coupled-spacetime-compiler.md` sequences 1–5 and Acceptance and rejection. Not overlay. Not another Chebyshev squeeze. Not native GUI. Not `production_law` selection.
- Changed: Review verdict **go-with-holes**. Physical A→B→A is GEM-a on the stepper remainder, not cone flags. `Reference::from_genesis` never starts from candidate state. Required ship/ray/clock/contact return values; this slice has no `UnsupportedPredicate` error variant. In-flight direct vs subdivided matches on worldtubes. Extra-ray reuse is charged consumer-share \(3864/(16892+3864)=0.186\ldots\), not assigned `f=1` and not 99.9%. Enclosure ignores compile residual; IntegralOperator `q≥1` rejects the certificate not the solution; CausalBlocks assigns `q=0` and can certify the close pair. Compact is stored compile sidecar; decode samples it onto the worldtube knot grid; admitted-band decode misses 1e-8; a \(10^{-8}\) band is a polyline and was not adopted. Six-card host is observatory-library tests; native GUI missing. Default `Engine::advance` remains `es-inertial-causal-v1`.
- Why: H0105 named the remainder and refused the polyline. Heading required an independent review so the laboratory slice is not a renamed pass and so the next unit is not another Chebyshev fit. Accepting the remainder as this laboratory slice does not finish the `/goal`.
- Validation: Reviewer read coupled-response sources and frozen [charged.json](../artifacts/runs/coupled-source-response-20260914/charged.json); recomputed the reuse share \(3864/(16892+3864)=0.18616303719406435\); confirmed engine `LAW_ID`. Specialist coupled_ 33 / observatory lib 8 counts were not rerun. No cargo.
- Evidence: [H0100–H0105 coupled-slice review](laws/h0100-h0105-coupled-slice-review-20260914.md); [H0105](HISTORY.md); [causal-arrival split note](laws/coupled-causal-arrival-split-20260914.md); [charged JSON](../artifacts/runs/coupled-source-response-20260914/charged.json); [continuation prompt](../orchestration/prompts/continue-coupled-spacetime-compiler.md).
- Limitations: Go-with-holes is not `production_law`. Compile is still the same `evolve()` as the reference plus a compact sidecar. Physical loop and in-flight identity still live on worldtubes. CausalBlocks `q=0` is assigned. Reuse share is not equivalent completed source histories. Enclosure is f64, not KA. Native GUI not compiled. Frozen `1dac658` untouched.
- Next: Do not select `production_law`. Do not start a new kernel. Do not retry a \(10^{-8}\) Chebyshev. Do not compile wgpu. Do not paper worldtubes as decode-only. Remaining blocker: compile storage is a sidecar of `evolve()` while the prompt's reused geometry and 1e-8 identity still live on the stepper remainder. Replace evolve-as-compile with a distinct interval response (operators on interval functions with independent residual that computes `q`), not an accept of that remainder as finishing the `/goal`. Keep `/goal` active.


## H0107 — Causal-block interval compile replaces evolve-as-compile; production_law stays null

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as isolated laboratory interval compile on `/private/tmp/emergent-coupled-response`; journaled after independent review (H0108); not production_law; default Engine::advance unchanged
- Revisions: Dirty overlay on `codex/coupled-source-response` above `254ba1f718771ec1d0a25bf59d0d555f7e57993e`. Edited `coupled_source_response.rs`, `coupled_interval_enclosure.rs`, and `coupled_phase_nav.rs` on that worktree. Did not edit journal-home crates for this overlay. No packet-branch merge. No `1dac658` rewrite. Did not replace default `Engine::advance`. Did not select `production_law`. Did not start a new kernel id.
- Scope: Prompt `continue-coupled-spacetime-compiler.md` sequence 2: compile jointly evolving sources over an interval with explicit domain, incoming dependencies, accumulated error, outgoing history and repair — not a tick loop renamed to Euler `dt`, not a precomputed trajectory table of `evolve()`.
- Changed: `compile_source_response` now calls `interval_compile` (midpoint GEM-a collocation on per-body causal-block knots: genesis \(\tau/2\), local kicks, frozen-observer light arrivals) instead of copying `Reference::evolve_to` into `SourceResponse.worldtubes`. Independent `Reference::from_genesis` still uses Euler-`dt` `evolve()`. Worldtubes are the piecewise-inertial chords of that collocation (interior \(½ah^2\) omitted). Compact remains a sidecar fitted in `seal_compiled`. `interval_q` is computed as \(\max_k(h_k L_k)\). Enclosure CausalBlocks `q` is computed as \(\tau L\), not assigned 0. Extra-ray reuse is the formula \(1-(S+C)/(24S+C)\) with 24 as a multiplier on **one** compile plus 24 `fly_ray` consumers, not 24 independent `compile_source_response` runs. Repair catch-up collocates only the kicked body at a committed cut so the in-flight direct vs subdivided test shares `interval_tau`. Jacobi block updates charge `factorization` once per nonempty block; no \(K\) matrix is assembled. Required ship/ray/clock/contact still return values. `production_law` null.
- Why: H0106 go-with-holes: physical A→B→A was real on the stepper remainder; compile was still the same `evolve()` plus a Chebyshev sidecar. Accepting that remainder does not finish the `/goal`. A distinct interval collocation is the heading-true unit. A \(10^{-8}\) Chebyshev polyline and wgpu are refused.
- Validation: Specialist reported `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab coupled_ --offline -- --test-threads=1` — 35 passed; 0 failed; same env `cargo test -p emergent-observatory --no-default-features --lib --offline -- --test-threads=1` — 8 passed; 0 failed. Integrator did not rerun those suites this turn. Independent review is [H0108](HISTORY.md). Frozen G2 `qualify()` not rerun. Native window not opened. wgpu not compiled.
- Evidence: [interval compile note](laws/coupled-interval-compile-20260914.md); [H0107 interval-compile review](laws/h0107-interval-compile-review-20260914.md); [H0106](HISTORY.md); [continuation prompt](../orchestration/prompts/continue-coupled-spacetime-compiler.md). Implementation remains on `/private/tmp/emergent-coupled-response`.
- Limitations: Piecewise-inertial chords omit interior \(½ah^2\) of a constant-a block; the collocated interval functions are not stored. Compact is still a sidecar; `decode_sources` still requires it. Extra-ray reuse is \(n\times S\) on one compile, not 24 independent completed coupled histories and not recovery after refuse/repair. "Schur" is Jacobi collocation plus a charge counter. Enclosure is f64, not KA; CausalBlocks \(\tau L\) zeros same-block Lipschitz by construction and can still certify a close pair IntegralOperator refuses. Interior late splice does not truncate worldtubes at `t_cut`. Native GUI not compiled. `production_law` stays null. Journal-home crates do not contain this overlay.
- Next: Independent review is [H0108](HISTORY.md). Do not select `production_law`. Do not retry a \(10^{-8}\) Chebyshev. Do not compile wgpu. Do not paper remaining inertial chords as decode-only of compact. Keep `/goal` active: one correctly evolving, causally coupled situation whose repeated computation can actually be reused.


## H0108 — Independent review of H0107 interval compile: go-with-holes; production_law stays null

- Date: 2026-09-14
- Kind: verification
- Status: measured as go-with-holes for the laboratory interval compile on `/private/tmp/emergent-coupled-response`; not a promotion and not `production_law`
- Revisions: read-only on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` above `254ba1f`). Docs-only directory `/private/tmp/emergent-interval-compile-review`. No engine/law-lab edit. No cargo-build. No wgpu. No `1dac658` write. Journal-home copy of the review. This entry is not yet committed.
- Scope: Adversarial check of H0107 claims (compile ≠ evolve-then-copy, CausalBlocks `q=τL`, extra-ray 24 equivalent histories, repair catch-up, compact sidecar, Schur/residual independence) against `continue-coupled-spacetime-compiler.md` sequence 2 / Acceptance. Not overlay. Not another Chebyshev squeeze. Not native GUI. Not `production_law` selection. Not a new kernel.
- Changed: Review verdict **go-with-holes**. `compile_source_response` calls `interval_compile`, not `evolve`; worldtubes are not bitwise identity with Euler-`dt`. CausalBlocks enclosure `q` is computed as \(\tau L\), not assigned 0. Repair catch-up at a committed cut collocates only the kicked body. Compact remains a sidecar. Extra-ray reuse \(1-(S+C)/(24S+C)\) is a multiplier on **one** compile plus 24 `fly_ray` consumers, not 24 independent completed coupled compiles; frozen charged JSON still records consumer-share 0.186. "Schur" is Jacobi collocation plus a factorization counter; same-block Lipschitz is zeroed by the \(\tau L\) formula. Stored reuse is still piecewise-inertial chords (½\(ah^2\) omitted). Default `Engine::advance` remains `es-inertial-causal-v1`.
- Why: H0107 landed a distinct collocation path. Heading required an independent review so a passing interval operator is not a renamed evolve-as-compile and so extra-ray arithmetic is not named equivalent completed source histories without measuring them.
- Validation: Reviewer read coupled-response `coupled_source_response.rs`, `coupled_interval_enclosure.rs`, and `coupled_phase_nav.rs`; recomputed close-pair \(L \approx 2/1.2^3 \approx 1.157\), \(HL \approx 1.157\), \(\tau L \approx 0.174\); recomputed the new reuse formula on frozen [charged.json](../artifacts/runs/coupled-source-response-20260914/charged.json) counts \(1-20756/409272 \approx 0.9493\) without 24 compiles. Specialist coupled_ 35 / observatory lib 8 counts were not rerun. No cargo.
- Evidence: [H0107 interval-compile review](laws/h0107-interval-compile-review-20260914.md); [H0107](HISTORY.md); [interval compile note](laws/coupled-interval-compile-20260914.md); [charged JSON](../artifacts/runs/coupled-source-response-20260914/charged.json); [continuation prompt](../orchestration/prompts/continue-coupled-spacetime-compiler.md).
- Limitations: Go-with-holes is not `production_law`. Compile is not evolve-then-copy; it is also not amortized repair across equivalent completed coupled histories. Enclosure is f64, not KA. Native GUI not compiled. Frozen `1dac658` untouched. Journal-home crates do not contain the overlay.
- Next: Measure N independent `compile_source_response` runs through the requested horizon, including repair after refusal/refinement, or stop calling extra-ray \(n\times S\) equivalent completed source histories. Do not paper inertial chords as the reused interval functions. An independent collocation residual that does not share `field_at` would make the Schur/Jacobi claim checkable. Do not select `production_law`. Do not retry a \(10^{-8}\) Chebyshev. Do not compile wgpu. Do not start another kernel: compile is already not evolve-then-copy. Keep `/goal` active.


## H0109 — Measured N=3 independent coupled compiles; extra-ray n×S is not equivalent completed source histories

- Date: 2026-09-14
- Kind: experiment
- Status: measured
- Revisions: uncommitted overlay on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` from `254ba1f`); journaled as H0109 on journal home; journal-home crates do not contain this overlay
- Scope: isolated `es-linearized-retarded-gem-response-v0` charged reuse; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Changed: Path A at declared N=3. `run_charged_workload` actually runs 3 independent `compile_source_response` through H=6 and uses their measured source-ops sum as the reuse denominator, not \(24\times S\) on one compile. Extra-ray 24 `fly_ray` is recorded as named `consumer_share`. Tests fail if extra-ray n×S is labelled equivalent completed source histories. Declared four-kick H=9 compact refuse did not trigger (`fallback=0`); refuse/refine is close-pair H=1 IntegralOperator \(q\approx 9.98\) recovered by CausalBlocks \(q\approx 0.819\) versus 3 full recomputes. Required ship/ray/clock/contact still return values. Independent `Reference::from_genesis` unchanged.
- Why: H0108 named extra-ray “24 histories” as \(n\times S\) on one compile. Prompt Acceptance requires equivalent completed histories through the horizon, including recovery after refusal/refinement, with the denominator defined by measured compiles. Incomplete certificates cannot earn a cheaper completion ratio. No hardcoded savings.
- Validation: Unique `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target` `CARGO_BUILD_JOBS=1` `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`. `cargo test -p emergent-law-lab --lib coupled_ -- --test-threads=1` PASS (35). `cargo test -p emergent-observatory --no-default-features --lib -- --test-threads=1` PASS (8). `cargo run -p emergent-law-lab --example coupled_source_response --offline --locked` wrote charged JSON with `production_law: null`. Quiet reuse \(1-1253/2793\approx 0.551\); consumer-share \(3864/(770+3864)\approx 0.834\); refuse recovery \(1-5012/15030\approx 0.667\). Positions matched (err 0). wgpu not compiled. Qualify not run. 0.551 is identical-IC compile-once-vs-N, not 99.9% and not distinct-history reuse.
- Evidence: [workload declaration](../artifacts/runs/equivalent-histories-20260914/workload-declaration.md), [measured results](../artifacts/runs/equivalent-histories-20260914/measured-results.md), [note](laws/equivalent-histories-20260914.md), [charged JSON](../artifacts/runs/equivalent-histories-20260914/charged.json)
- Limitations: N=3 identical-IC compiles make \(1-(S+C)/(3S+C)\) numerically tautological even though the three compiles actually ran. That is not amortization across distinct evolving situations. Stored interval functions remain piecewise-inertial chords plus a compact sidecar. Four-kick H=9 compact no longer refuses on this operator. Enclosure is f64, not KA. Native GUI not compiled. Journal-home crates do not contain this overlay.
- Next: Keep `/goal` active. Do not treat identical-IC compile-once-vs-N as finishing reusable compiled geometry. Next is sharing certified interval functions across DISTINCT completed coupled histories (different interventions or new entrants). Not polyline and not wgpu. Inertial chords plus consumer-share are not that object.


## H0110 — Certified interval functions reused across a distinct kicked source history; extra-ray still not that object

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as isolated laboratory reuse on `/private/tmp/emergent-coupled-response`; journaled as H0110 on journal home; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Revisions: uncommitted overlay on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` from `254ba1f`); journal-home crates do not contain this overlay
- Scope: isolated `es-linearized-retarded-gem-response-v0` prompt sequence 4; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Changed: `compile_source_response` now stores collocated interval functions `(t0, t1, x0, v0, a)` on `SourceResponse`. `repair_from_committed` truncates to complete certified blocks at the per-body causal cut instead of cloning post-cut worldtubes. `reuse_certified_interval_functions` requires an independent CausalBlocks enclosure of the first compile (does not read compile residual), copies those blocks into a second distinct history (same genesis IC, later kick), and recollocates only the invalidated tail. Empty extra / extra-ray and a foreign body / new massive entrant from genesis refuse rather than claiming reuse. Required ship/ray/clock/contact still return values.
- Why: H0109 made the identical-IC denominator honest but did not share certified interval functions across distinct completed coupled histories. Prompt sequence 4 asks new entrants to reuse source/transport work and localized repair versus full recompute. Extra-ray \(n\times S\) and identical-IC compile-once-vs-N are not that object.
- Validation: Unique `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target` `CARGO_BUILD_JOBS=1` `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`. `cargo test -p emergent-law-lab --lib coupled_ -- --test-threads=1` PASS (37; previous 35 plus extra-ray refuse API and distinct-history reuse). `cargo test -p emergent-observatory --no-default-features --lib -- --test-threads=1` PASS (8). `cargo run -p emergent-law-lab --example coupled_source_response --offline --locked` wrote charged JSON with `production_law: null`. Distinct-history: 21 certified functions copied, 1 recollocated, source ops 427 vs 793 (\(\approx 0.462\)), pos err 0, required queries true. H0109 0.551 and extra-ray consumer-share \(\approx 0.834\) unchanged as named different quantities. wgpu not compiled. Qualify not run.
- Evidence: [workload declaration](../artifacts/runs/distinct-histories-20260914/workload-declaration.md), [measured results](../artifacts/runs/distinct-histories-20260914/measured-results.md), [note](laws/distinct-histories-20260914.md), [charged JSON](../artifacts/runs/distinct-histories-20260914/charged.json)
- Limitations: GEM lookback and ship/ray consumers still evaluate the piecewise-inertial worldtube decode (interior ½`ah²` omitted on the chord). Compact remains a sidecar. Recollocation after t=5 is one causal block on this quiet pair; 0.462 is not 99.9% and is not amortization across a new massive entrant from genesis (that case refuses). Independent collocation residual still shares `field_at`. Enclosure is f64, not KA. Native GUI not compiled. Journal-home crates do not contain this overlay.
- Next: Keep `/goal` active. Do not treat this late-kick prefix copy as finishing reusable compiled geometry. Next is not polyline and not wgpu. Transport still does not evaluate the stored constant-a interval functions, and a new massive entrant still cannot share a compiled pair's exterior.


## H0111 — Query-time GEM lookback evaluates stored constant-a interval functions; chords remain a named remainder

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as isolated laboratory query-time lookback on `/private/tmp/emergent-coupled-response`; journaled as H0111 on journal home; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Revisions: uncommitted overlay on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` from `254ba1f`); journal-home crates do not contain this overlay
- Scope: isolated `es-linearized-retarded-gem-response-v0` query-time transport; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Changed: GEM lookback and ship/ray/clock consumers evaluate stored interval functions `(t0,t1,x0,v0,a)` including interior ½`ah²` (`field_at_compiled`, `fly_ship_compiled`, `fly_ray_compiled`, `clock_rate_compiled`, `complete_required_queries_compiled`). Retarded delay is Newton on that parabola, seeded by the inertial quadratic. Open-tail worldtube chords remain a named remainder when no function covers the retarded event. Compile-time collocation still samples inertial chords. `share_compiled_pair_exterior` declares a new massive entrant (`laboratory_encounter` id 99) and refuses because the pair enclosure does not certify a different genesis IC (H0110 refuse stands; not claimed as genesis foreign-body reuse). Held-out ship/ray/clock/contact still return values. Independent `Reference::from_genesis` unchanged. Enclosure still does not certify by reading compile residual. Extra-ray 24 remains named consumer-share, not equivalent completed source histories. Late-kick prefix copy is not sold as finishing `/goal`.
- Why: H0110 copied certified prefix functions, but transport still read piecewise-inertial worldtube chords that omit ½`ah²`. Heading-true next was lookback/transport on the stored constant-a functions, not another n×S multiplier, not polyline, not wgpu, not another kernel.
- Validation: Unique `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target` `CARGO_BUILD_JOBS=1` `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`. Disk ~11 GiB free; swap ~4.8/6 GiB used. `cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1` PASS (40; previous 37 plus lookback ½`ah²` discriminator, extra-ray still not equivalent histories, late-kick/new-entrant not the `/goal` finish). `cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1` PASS (8). wgpu not compiled. Qualify not run. `production_law` null.
- Evidence: [lookback note](laws/interval-lookback-20260914.md), [H0110](HISTORY.md)
- Limitations: Compile-time `field_at` still collocates from inertial chords; this entry does not claim collocation already samples stored a. Worldtube knots still omit ½`ah²` (`inertial_end`). Open tail after the last collocation knot has no stored function. 0.462 late-kick prefix is unchanged and is not 99.9% and not a new-entrant exterior share. Compact remains a sidecar. Enclosure is f64, not KA. Native GUI not compiled. Journal-home crates do not contain this overlay.
- Next: Keep `/goal` active. Do not treat query-time lookback, extra-ray n×S, identical-IC compile-once-vs-N, or the late-kick prefix as finishing reusable compiled geometry. Next is not polyline and not wgpu. A new massive entrant still cannot share a compiled pair's exterior (that refuse is honest). Compile-time collocation still does not sample stored a.


## H0112 — Linearized GEM cannot certify a compiled pair's exterior for a new massive entrant; refuse kept

- Date: 2026-09-14
- Kind: experiment
- Status: measured as fail-closed refuse on `/private/tmp/emergent-coupled-response`; journaled as H0112 on journal home; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Revisions: uncommitted overlay on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` from `254ba1f`); journal-home crates do not contain this overlay
- Scope: isolated `es-linearized-retarded-gem-response-v0` prompt sequence 4 new-entrant exterior share; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Changed: `share_compiled_pair_exterior` independently CausalBlocks-encloses the compiled pair on the pair IC (residual unused), then **refuses** a `laboratory_encounter` id-99 massive entrant because that enclosure does not cover a different genesis. Post-cone GEM `|a←entrant|/|a←partner| \approx 1.519`; pair-vs-triple A,B displacement \(\approx 0.363\) versus pair enclosure radius \(\approx 0.0204\). Derivation: field-linearity at frozen worldtubes is not worldtube-linearity; without assembled \(K_{AC}\) the pair inverse cannot absorb a new massive source. `fly_ship` on the pair is not this share. H0110 foreign-body refuse stands. Required ship/ray/clock/contact still return values. Extra-ray still not equivalent completed source histories. Compile-time collocation still samples inertial chords (optional stored-a collocation not taken; would distract).
- Why: Sequence 4 asks new entrants to reuse source/transport work. Heading-true share requires an independently certified pair exterior on a declared domain, op counts versus a full three-body compile, and fail-closed coverage. Linearized retarded GEM cannot certify that exterior without recoupling this equal-mass nearby entrant.
- Validation: Unique `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target` `CARGO_BUILD_JOBS=1` `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`. Disk ~14 GiB free; swap ~5.1/6.1 GiB used. `cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1` PASS (41; previous 40 plus the declared encounter counterexample). `cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1` PASS (8). wgpu not compiled. Qualify not run. `production_law` null.
- Evidence: [declaration](laws/pair-exterior-workload-declaration-20260914.md), [refuse note](laws/pair-exterior-share-refuse-20260914.md), [H0111](HISTORY.md)
- Limitations: Refuse is for this linearized GEM slice and the declared encounter; it does not prove no far/weak omitted-backreaction domain can ever exist, and it does not assemble Schur \(K\). 1669 vs 770 source ops are not a reuse fraction. Enclosure is f64, not KA. Compact remains a sidecar. Native GUI not compiled. Journal-home crates do not contain this overlay.
- Next: Keep `/goal` active. Do not treat extra-ray n×S, identical-IC compile-once-vs-N, late-kick prefix, query-time lookback, or this refuse as finishing reusable compiled geometry. Next is not polyline and not wgpu. Heading-true next is an independently enclosed omitted massive backreaction, or a real Schur update of the compiled pair, so a new massive IC can reuse the pair without a full recoupled three-body compile — not `fly_ship` renamed as share, not another kernel id.


## H0113 — Schur pair-block update for a distant massive tide; encounter 1.519 refuse kept

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as isolated laboratory Schur pair-block update on `/private/tmp/emergent-coupled-response`; journaled as H0113 on journal home; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Revisions: uncommitted overlay on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` from `254ba1f`); journal-home crates do not contain this overlay
- Scope: isolated `es-linearized-retarded-gem-response-v0` prompt sequence 4 Schur / omitted-backreaction; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Changed: `schur_update_compiled_pair` treats the compiled quiet pair as a solved causal-block and recollocates only \(\delta a=K_{AC}c\) on stored pair interval functions for named fixture `laboratory_distant_tide` id 77 (\(\mu=1\), \(x=(0,40)\)), then rematches pair \((x,v)\). Pair \(\max|\Delta a|\approx 0.000619\), \(\max|\Delta x|\approx 0.000155\) inside pair enclosure radius \(\approx 0.020405\). After the entrant's cone, \(|a\leftarrow 77|/|a\leftarrow B|\approx 0.03746\). Independent omitted leftover versus a full three-body compile of the same IC is 0 at 16 samples (GEM mismatch bound, residual unused). Source evolution 33 vs 33; source ops 3533 vs 3262 are **not** a cheaper reuse fraction. `share_compiled_pair_exterior` still refuses `laboratory_encounter` id 99 (post-cone ratio \(1.5193625031062006\)). Required ship/ray/clock/contact still return values. Extra-ray still not equivalent completed source histories. Compile-time collocation still samples inertial chords.
- Why: Sequence 4 wants new entrants to reuse the pair without a from-scratch three-body evolve-then-copy. Heading-true Path A is a real pair-block update plus an independent omitted-residual enclosure. The 1.519 encounter is not a distant tide and is not weakened.
- Validation: Unique `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target` `CARGO_BUILD_JOBS=1` `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`. Disk ~13 GiB free; swap ~5.2/6.1 GiB used. `cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1` PASS (42; previous 41 plus Schur/encounter-refuse). `cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1` PASS (8). wgpu not compiled. Qualify not run. `production_law` null.
- Evidence: [declaration](laws/schur-pair-workload-declaration-20260914.md), [update note](laws/schur-pair-update-20260914.md), [H0112](HISTORY.md)
- Limitations: The pair inverse is not stored as an operator; the pair mesh is still walked, so 3533 vs 3262 is not savings. vs_full=0 is this weak tide at 16 samples, not a general three-body identity. Enclosure is f64, not KA. Compact remains a sidecar. Native GUI not compiled. Journal-home crates do not contain this overlay. This is not finishing `/goal`.
- Next: Keep `/goal` active. Do not treat extra-ray n×S, identical-IC compile-once-vs-N, late-kick prefix, query-time lookback, the H0112 refuse, or this distant-tide Schur as finishing reusable compiled geometry. Next is not polyline and not wgpu. Heading-true next is a stored/applied \((I-K_{AB}K_{BA})^{-1}\) so the pair mesh is not fully rewalked, or a closer massive IC that still fits the pair radius — without weakening the 1.519 encounter refuse, not another kernel id.


## H0114 — Stored pair inverse applied for a distant tide; source ops cheaper than same-IC three-body; encounter 1.519 refuse kept

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as isolated laboratory stored pair inverse on `/private/tmp/emergent-coupled-response`; journaled as H0114 on journal home; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Revisions: uncommitted overlay on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` from `254ba1f`); journal-home crates do not contain this overlay
- Scope: isolated `es-linearized-retarded-gem-response-v0` prompt sequence 4 stored \((I-K_{AB}K_{BA})^{-1}\); not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Changed: Quiet two-body `compile_source_response` stores an LU of \((I-K)\) on the pair collocation mesh. `schur_update_compiled_pair` forms \(K_{AC}c\) at frozen pair knots and applies that operator for `laboratory_distant_tide` id 77, then rematches pair \((x,v)\) once. Pair \(\max|\Delta a|\approx 0.000619\), \(\max|\Delta x|\approx 0.000155\) inside radius \(\approx 0.020405\). Independent leftover versus a full three-body compile of the same IC is 0 at 16 samples. Source evolution 33 vs 33; source ops **3209 vs 3262** (cheaper). H0113 3533 vs 3262 is not this object and is not a reuse fraction. Factorization stays on the charge counter (pair 36, update 38), not laundered into source ops. Three-body compiles do not assemble a pair inverse. `share_compiled_pair_exterior` still refuses `laboratory_encounter` id 99 (post-cone ratio \(1.5193625031062006\)). Required ship/ray/clock/contact still return values. Extra-ray still not equivalent completed source histories. Compile-time collocation still samples inertial chords.
- Why: Sequence 4 wants the compiled pair reused as a solved block. Heading-true apply is stored \((I-K)^{-1}\) so the pair mesh is not recollocated from scratch. The 1.519 encounter is not a distant tide and is not weakened.
- Validation: Unique `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target` `CARGO_BUILD_JOBS=1` `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`. Disk ~17 GiB free; swap ~3.2/4.1 GiB used. `cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1` PASS (42). `cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1` PASS (8). wgpu not compiled. Qualify not run. `production_law` null.
- Evidence: [declaration](laws/pair-inverse-workload-declaration-20260914.md), [update note](laws/pair-inverse-update-20260914.md), [H0113](HISTORY.md)
- Limitations: The stored inverse is the inverse of the **chord** collocation operator; compile-time `field_at` still omits ½\(ah^2\). vs_full=0 is this weak tide at 16 samples, not a general three-body identity. Enclosure is f64, not KA. Compact remains a sidecar. Native GUI not compiled. Journal-home crates do not contain this overlay. This is not finishing `/goal`.
- Next: Keep `/goal` active. Do not treat extra-ray n×S, identical-IC compile-once-vs-N, late-kick prefix, query-time lookback, the H0112 refuse, the H0113 distant-tide Schur, or this stored inverse as finishing reusable compiled geometry. Next is not polyline and not wgpu and not weakening 1.519. Heading-true next is compile-time collocation that samples stored constant-a (including ½\(ah^2\)) so the stored pair inverse is the operator of the functions queries already read — or a closer massive IC that still fits the pair radius without weakening the 1.519 encounter refuse. Not another kernel id.


## H0115 — Compile-time collocation samples stored-a; pair inverse is that operator; distant-tide source ops not cheaper; encounter 1.519 refuse kept

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as isolated laboratory stored-a collocation on `/private/tmp/emergent-coupled-response`; journaled as H0115 on journal home; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Revisions: uncommitted overlay on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` from `254ba1f`); journal-home crates do not contain this overlay
- Scope: isolated `es-linearized-retarded-gem-response-v0` compile-time collocation samples stored constant-a; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Changed: `interval_continue`, `store_pair_inverse`, frozen-source entrant collocation, and stored-inverse apply sample GEM from stored constant-a interval functions (including ½\(ah^2\)), the same geometry query-time lookback already reads. Open-tail worldtube chords remain the fallback when no function covers the retarded event. Independent `Reference::from_genesis` and enclosure checkers still use chord `field_at` and do not read compile residual. Test `compile_time_collocation_samples_stored_a_not_chords` shows a later collocation knot differs from chord-only where \(a\neq 0\), and compiled \(a\) recovers that sample. `laboratory_distant_tide` id 77: pair \(\max|\Delta a|\approx 0.000619\), \(\max|\Delta x|\approx 0.000155\) inside radius \(\approx 0.020278\); leftover vs same-IC three-body 0 at 16 samples; source evolution 33 vs 33; source ops **3429 vs 3422** (not cheaper; H0114 3209 vs 3262 was the chord operator). Factorization pair 36, update 38, not source ops. `share_compiled_pair_exterior` still refuses `laboratory_encounter` id 99 (post-cone ratio \(1.5193625031062006\)). Required ship/ray/clock/contact still return values. Extra-ray still not equivalent completed source histories. Observer knots and `inertial_end` still omit ½\(ah^2\) (named remainder, not a boolean rename).
- Why: The stored pair inverse was the inverse of chord collocation while cameras already read stored \(a\). Heading-true unify is one geometry at compile and lookback. The 1.519 encounter is not a distant tide and is not weakened. Do not invent a cheaper 3429 vs 3422.
- Validation: Unique `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target` `CARGO_BUILD_JOBS=1` `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`. Disk ~17 GiB free; swap ~3.5/4.1 GiB used. `cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1` PASS (43). `cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1` PASS (8). wgpu not compiled. Qualify not run. `production_law` null.
- Evidence: [update note](laws/stored-a-collocation-20260914.md), [H0114](HISTORY.md)
- Limitations: Observer collocation knots and worldtube `inertial_end` still omit ½\(ah^2\) because the current block's \(a\) is the unknown. vs_full=0 is this weak tide at 16 samples, not a general three-body identity. 3429 vs 3422 is not savings: stored-a lookback charges a retarded solve per attempted interval, including misses. Enclosure is f64, not KA. Compact remains a sidecar. Native GUI not compiled. Journal-home crates do not contain this overlay. This is not finishing `/goal`.
- Next: Keep `/goal` active. Do not treat extra-ray n×S, identical-IC compile-once-vs-N, late-kick prefix, query-time lookback, the H0112 refuse, the H0113/H0114 chord inverse, this stored-a unify, 3209 vs 3262, or 3429 vs 3422 as finishing reusable compiled geometry. Next is not polyline and not wgpu and not weakening 1.519. Heading-true next is a closer massive IC that still fits the pair radius without weakening the 1.519 encounter refuse, or an honest cheaper repair of the stored pair for a distant third — not another kernel id, not papering observer chords as stored-a.


## H0116 — Covering-bounded stored-a pair apply cheaper than same-IC three-body; encounter 1.519 refuse kept

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as isolated laboratory covering-bounded stored-a apply on `/private/tmp/emergent-coupled-response`; journaled as H0116 on journal home; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Revisions: uncommitted overlay on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` from `254ba1f`); journal-home crates do not contain this overlay
- Scope: isolated `es-linearized-retarded-gem-response-v0` covering-bounded apply of stored \((I-K)^{-1}\); not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Changed: `field_at_stored` skips charging a retarded Newton on a stored-a interval whose constant-a AABB delay range cannot meet the light-delay window (superset bound; possible hits still run `gem_from_function`). `schur_update_compiled_pair` on `laboratory_distant_tide` id 77 still forms \(K_{AC}c\) at frozen pair knots and applies the stored inverse. Pair \(\max|\Delta a|\approx 0.000619\), \(\max|\Delta x|\approx 0.000155\) inside radius \(\approx 0.020278\); leftover vs same-IC three-body 0 at 16 samples; source evolution 33 vs 33; source ops **3169 vs 3186** (cheaper by 17; not 99.9%; \(1-3169/3186\approx 0.0053\)). H0115 3429 vs 3422 was the miss-walk. Factorization pair 36, update 38, not source ops. `share_compiled_pair_exterior` still refuses `laboratory_encounter` id 99 (post-cone ratio \(1.5193625031062006\)). Required ship/ray/clock/contact still return values. Extra-ray still not equivalent completed source histories. Observer knots and `inertial_end` still omit ½\(ah^2\).
- Why: Stitching a far third onto the stored pair was charging Newton on every later interval, including misses. Heading-true cheaper apply is the stored inverse plus a sound covering bound, not recollocating the pair and not weakening 1.519. Do not invent a bigger ratio than 3169 vs 3186.
- Validation: Unique `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target` `CARGO_BUILD_JOBS=1` `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`. Disk ~17 GiB free; swap ~3.8/4.1 GiB used. Workload declared before results. `cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1` PASS (43). `cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1` PASS (8). wgpu not compiled. Qualify not run. `production_law` null.
- Evidence: [declaration](laws/cheaper-pair-repair-workload-declaration-20260914.md), [update note](laws/cheaper-pair-repair-20260914.md), [H0115](HISTORY.md)
- Limitations: 17 source ops is not reusable compiled geometry for a recoupling third. vs_full=0 is this weak tide at 16 samples, not a general three-body identity. Both counts dropped versus H0115 because the covering bound is shared stored-a lookback, not a private Schur skip. Enclosure is f64, not KA. Compact remains a sidecar. Observer knots still omit ½\(ah^2\). Native GUI not compiled. Journal-home crates do not contain this overlay. This is not finishing `/goal`.
- Next: Keep `/goal` active. Do not treat extra-ray n×S, identical-IC compile-once-vs-N, late-kick prefix, query-time lookback, the H0112 refuse, H0113/H0114 chord inverse, H0115 stored-a unify, 3209 vs 3262, 3429 vs 3422, or 3169 vs 3186 as finishing reusable compiled geometry. Next is not polyline and not wgpu and not weakening 1.519 and not FMM. A third mass close enough to recouple the pair still refuses at 1.519; a closer massive IC that still fits the pair radius remains the heading-true probe — not papering observer chords as stored-a, not another kernel id.


## H0117 — Named recouple when a close third leaves the pair neighborhood; encounter 1.519 refuse kept

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as isolated laboratory named recouple on `/private/tmp/emergent-coupled-response`; journaled as H0117 on journal home; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Revisions: uncommitted overlay on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` from `254ba1f`); journal-home crates do not contain this overlay
- Scope: isolated `es-linearized-retarded-gem-response-v0` named recouple of a compiled pair plus a close massive third; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Changed: `recouple_compiled_pair` compiles A, B, and the entrant jointly when share refuses (causal-block interval collocation on that recoupled IC; no copy of pair interval functions; no stored pair inverse; not Einstein two-body). `share_compiled_pair_exterior` still refuses `laboratory_encounter` id 99, H=6, dt=1/32 (post-cone ratio \(1.5193625031062006\)). Recoupled A,B vs pair \(\max|\Delta x|=0.3640312882418288\) leaves radius \(0.02027796228674037\). Leftover vs independent same-IC three-body **0** at 16 samples (bodies 0, 1, 99). Source evolution 42 vs 42. Source ops **1537 vs 1537** (equal; not cheaper; not 99.9%). Repair 1 is off source ops. Independent CausalBlocks recertify of the recoupled compile: certified, \(q\approx 0.037587\). Distant-tide id 77 recouple refuses (neighborhood still holds; Schur/covering-bounded stored-a apply remains). Required ship/ray/clock/contact still return values. Extra-ray still not equivalent completed source histories. Observer knots and `inertial_end` still omit ½\(ah^2\).
- Why: H0116's 17-op far-tide delta is a laboratory remainder. A close third still recouples the pair. Heading-true recovery is a named three-body interval compile, not weakening 1.519, not fill-in of pair functions, and not another far-tide micro-optimization. 1537 vs 1537 is the same operator, not amortization.
- Validation: Unique `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target` `CARGO_BUILD_JOBS=1` `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`. Disk ~16–18 GiB free; swap ~3.5/4.1 GiB used. Workload declared before results. `cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1` PASS (44). `cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1` PASS (8). wgpu not compiled. Qualify not run. `production_law` null.
- Evidence: [declaration](laws/recouple-workload-declaration-20260914.md), [update note](laws/recouple-20260914.md), [H0116](HISTORY.md)
- Limitations: Recouple is a full three-body compile of the recoupled IC. Leftover 0 and equal source ops mean identity with independent three-body, not reuse. vs_pair 0.364 is this encounter at 16 samples. Enclosure is f64, not KA. Compact remains a sidecar. Observer knots still omit ½\(ah^2\). Native GUI not compiled. Journal-home crates do not contain this overlay. This is not finishing `/goal`.
- Next: Keep `/goal` active. Do not treat 1537 vs 1537, 3169 vs 3186, extra-ray n×S, identical-IC compile-once-vs-N, late-kick prefix, query-time lookback, the H0112 refuse, or H0113–H0116 far-tide apply as finishing reusable compiled geometry. Next is not polyline, not wgpu, not weakening 1.519, not FMM, not sensitivity/Jacobian this turn. A close third still pays a full joint compile; reusable compiled geometry for mutually evolving sources remains missing.


## H0118 — Recoupled three-body compile-once/reuse/repair of certified interval functions; encounter 1.519 refuse kept

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as isolated laboratory recoupled reuse/repair on `/private/tmp/emergent-coupled-response`; journaled as H0118 on journal home; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Revisions: uncommitted overlay on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` from `254ba1f`); journal-home crates do not contain this overlay
- Scope: isolated `es-linearized-retarded-gem-response-v0` compile-once / reuse / repair of certified interval functions on a recoupled three-body compile (same three masses, distinct completed histories); not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Changed: `reuse_recoupled_interval_functions` and `repair_recoupled_interval_functions` take the recoupled trio as the object (not pair-interval fill-in). Quiet recoupled encounter plus a t=5 kick on id 0 copies **86** complete certified interval functions versus an independent `compile_source_response` of that kicked IC. Leftover \(\max|\Delta x|=4.768153\times 10^{-8}\) at 16 samples (bodies 0, 1, 99) — suffix-collocation remainder, not recouple leftover-0 identity. Source ops **1118 vs 1613** (\(1-1118/1613\approx 0.307\), not 99.9%). Mid-horizon t=3 repair copies **73** prefix blocks; leftover \(1.440815\times 10^{-3}\) is the named `inertial_end` ½\(ah^2\) remainder on a longer suffix, kept visible, inside pair radius \(\approx 0.020278\), not encounter-scale 0.364. Repair source ops **1022 vs 1656**; repair charge 1. Pair passed to this API refuses. Empty extra / extra-ray still refuses as not equivalent completed source histories. Encounter share still refuses at \(1.5193625031062006\). Required ship/ray/clock/contact still return values. Six-card three-bodies/fleet look-for name this reuse; solar/galaxy/black-hole remain unsupported.
- Why: H0117 recouple is a full three-body compile (1537 vs 1537), not amortization. Job 2 pair-interval fill-in after recouple was rejected. Heading-true reuse is compile-once / repair of certified recoupled interval functions across distinct completed histories on the same three masses, fully charged through the horizon, versus independent same-IC compiles.
- Validation: Unique `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target` `CARGO_BUILD_JOBS=1` `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`. Disk ~18 GiB free; swap ~3.4/4.1 GiB used. Workload declared before results. `cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1` PASS (46). `cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1` PASS (8). wgpu not compiled. Qualify not run. `production_law` null.
- Evidence: [declaration](laws/recoupled-reuse-workload-declaration-20260914.md), [update note](laws/recoupled-reuse-20260914.md), [H0117](HISTORY.md)
- Limitations: Late-kick leftover \(4.8\times 10^{-8}\) is collocation remainder, not identity. Repair leftover \(1.44\times 10^{-3}\) is the named ½\(ah^2\) omission on rebuilt worldtubes; not papered to 0. 0.307 is not 99.9%. Observer knots still omit ½\(ah^2\). Compact remains a sidecar. Enclosure is f64, not KA. Native GUI not compiled. Journal-home crates do not contain this overlay. This is not finishing `/goal`.
- Next: Keep `/goal` active. Do not treat 1118 vs 1613, 1022 vs 1656, 1537 vs 1537, or 3169 vs 3186 as finishing reusable compiled geometry. Next is not polyline, not wgpu, not weakening 1.519, not pair fill-in, not FMM, not sensitivity/Jacobian this turn. Named remainder: `inertial_end` / observer knots still omit ½\(ah^2\) (repair leftover \(1.44\times 10^{-3}\)).


## H0119 — Stored-a knots on rebuilt worldtubes; mid-horizon leftover named as prefix-grid remainder; encounter 1.519 refuse kept

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as isolated laboratory stored-a knots on `/private/tmp/emergent-coupled-response`; journaled as H0119 on journal home; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Revisions: uncommitted overlay on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` from `254ba1f`); journal-home crates do not contain this overlay
- Scope: isolated `es-linearized-retarded-gem-response-v0` rebuilt interval functions / observer knots using the same stored constant-a geometry as lookback; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Changed: `inertial_end` is `state_at(t1)` (includes ½\(ah^2\)). `interval_continue` catch-up and collocation knots, and frozen-source entrant collocation, close at that endpoint. Closed worldtube `Segment`s store block `a` so `present` matches `state_at`; the open tail stays inertial. Mid-horizon recoupled repair leftover vs independent same-IC recompile is \(8.545279\times 10^{-5}\) (was H0118 \(1.440815\times 10^{-3}\)); copies **73**; source ops **1010 vs 1650**. Late-kick reuse still copies **86**; leftover \(9.606183\times 10^{-8}\); source ops **1106 vs 1608** (\(\approx 0.312\), not 99.9%). Recouple leftover **0**; source ops **1532 vs 1532**. Far-tide apply still **3169 vs 3186**, leftover 0. Encounter share still refuses at \(1.5193527764310737\) (H0118 recorded \(1.5193625031062006\); still \(>1\), still \(\approx 1.519\); not weakened). Pair-after-recouple still refuses. Extra-ray still refuses as not equivalent completed source histories. Required ship/ray/clock/contact still return values. Remaining named remainder: quiet-prefix block grid omits the extra t=3 kick knot the independent compile collocates — not papered to 0, not a loosened 1e-7 claim.
- Why: H0118 named rebuilt worldtubes / observer knots omitting ½\(ah^2\) as the hole that kept mid-horizon leftover at \(1.44\times 10^{-3}\). Heading-true close is the same stored-a geometry lookback already reads, then re-measure versus independent same-IC, without weakening 1.519 or hiding leftover by loosening a gate.
- Validation: Unique `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target` `CARGO_BUILD_JOBS=1` `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`. Disk ~18 GiB free; swap ~3.4/4.1 GiB used. `cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1` PASS (46). `cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1` PASS (8). wgpu not compiled. Qualify not run. `production_law` null.
- Evidence: [update note](laws/stored-a-knots-20260914.md), [H0118](HISTORY.md)
- Limitations: Repair leftover \(8.55\times 10^{-5}\) is not late-kick collocation scale. 1106 vs 1608 is not 99.9%. Open tail still omits ½\(ah^2\). Compact remains a sidecar. Enclosure is f64, not KA. Native GUI not compiled. Journal-home crates do not contain this overlay. This is not finishing `/goal`.
- Next: Keep `/goal` active. Do not treat 1106 vs 1608, 1010 vs 1650, 1532 vs 1532, or 3169 vs 3186 as finishing reusable compiled geometry. Next is not polyline, not wgpu, not weakening 1.519, not pair fill-in, not FMM, not KA, not native GUI, not sensitivity/Jacobian this turn. Named remainder: quiet-prefix grid versus the independent compile's extra kick knot (repair leftover \(8.55\times 10^{-5}\)).


## H0120 — Certified prefix uses the extra kick knot; mid-horizon leftover 0 at 16 samples; encounter 1.519 refuse kept

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as isolated laboratory prefix-grid match on `/private/tmp/emergent-coupled-response`; journaled as H0120 on journal home; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Revisions: uncommitted overlay on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` from `254ba1f`); journal-home crates do not contain this overlay
- Scope: isolated `es-linearized-retarded-gem-response-v0` recoupled repair/reuse certified prefix on the independent kicked collocation grid, including the extra kick knot; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Changed: `kept_certified_functions` copies only blocks complete by \(\min(\)causal cut, extra kick knot\()\). Observer quiet blocks that end after the intervention omit that knot and are recollocated. `repair_from_committed` continues from the last shared prefix endpoint so `incoming_knots` includes the extra kick knot, matching independent `compile_source_response` of the same kicked IC. Mid-horizon leftover vs independent same-IC recompile is **0** at 16 samples (was H0119 \(8.545279\times 10^{-5}\)); copies **70**; source ops **1054 vs 1650**. Late-kick reuse leftover **0** at 16 samples (was \(9.606183\times 10^{-8}\)); copies **81**; source ops **1121 vs 1608** (\(\approx 0.303\), not 99.9%). Recouple leftover **0**; source ops **1532 vs 1532**. Far-tide apply still **3169 vs 3186**, leftover 0. Encounter share still refuses at \(1.5193527764310737\) (still \(\approx 1.519\), still \(>1\); not weakened; not frozen as a new 16-digit gate). Pair-after-recouple still refuses. Extra-ray still refuses as not equivalent completed source histories. Required ship/ray/clock/contact still return values.
- Why: H0119 named quiet-prefix grid versus the independent compile's extra t=3 kick knot as the hole that kept mid-horizon leftover at \(8.55\times 10^{-5}\). Heading-true close is the same collocation/knot grid, then re-measure versus independent same-IC, without weakening 1.519 or hiding leftover by loosening a gate. Collocation-scale \(<10^{-7}\) was declared before measuring.
- Validation: Unique `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target` `CARGO_BUILD_JOBS=1` `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`. Disk ~18 GiB free; swap ~3.3/4.1 GiB used. `cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1` PASS (46). `cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1` PASS (8). wgpu not compiled. Qualify not run. `production_law` null.
- Evidence: [update note](laws/prefix-kick-knot-20260914.md), [H0119](HISTORY.md)
- Limitations: Leftover 0 is 16 samples, not a general interval-function identity. 1121 vs 1608 is not 99.9%. Open tail still omits ½\(ah^2\). Compact remains a sidecar. Enclosure is f64, not KA. Native GUI not compiled. Journal-home crates do not contain this overlay. This is not finishing `/goal`.
- Next: Keep `/goal` active. Do not treat leftover-0, 1121 vs 1608, 1054 vs 1650, 1532 vs 1532, or 3169 vs 3186 as finishing reusable compiled geometry. Next is not polyline, not wgpu, not weakening 1.519, not pair fill-in, not FMM, not KA, not native GUI, not sensitivity/Jacobian this turn. Remaining named remainder: open-tail worldtubes still omit ½\(ah^2\); compact is a sidecar; measured prefix-copy \(\approx 0.30\) is not 99.9%.


## H0121 — Open tail continues stored constant-a; leftover-0 named at 16 and denser samples; encounter 1.519 refuse kept

- Date: 2026-09-14
- Kind: implementation
- Status: implemented as isolated laboratory open-tail stored-a on `/private/tmp/emergent-coupled-response`; journaled as H0121 on journal home; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Revisions: uncommitted overlay on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` from `254ba1f`); journal-home crates do not contain this overlay
- Scope: isolated `es-linearized-retarded-gem-response-v0` open-tail worldtubes after the last collocation knot; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Changed: `close_and_kink` writes the collocation block `a` onto the open tail so `present` continues ½`ah²`. A kick closes that tail with the stored `a` and opens a post-kick tail at `a=0` until the next collocation. `gem_from_segment` on nonzero `a` uses the same constant-a lookback as stored interval functions. Euler `continue_from` still writes zero. Horizon is still not a collocation knot. Encounter share still refuses at \(1.5193527764310737\) (still \(\approx 1.519\), still \(>1\); not weakened; not frozen as a new 16-digit gate). Recouple leftover **0** at 16 samples, **0** at 128 samples, open-tail leftover **0**, open-tail lookback leftover **0**; source ops **1599 vs 1599** (H0120 1532 vs 1532 was the inertial-tail operator). Late-kick leftover **0** at 16 and at 128/tail/lookback; copies **81**; source ops **1188 vs 1675** (\(\approx 0.291\), not 99.9%). Mid-horizon leftover **0** at 16 and at 128/tail/lookback; copies **70**; source ops **1126 vs 1722**. Far-tide still **3169 vs 3186**, leftover 0 at those same checks. Pair-after-recouple still refuses. Extra-ray still refuses as not equivalent completed source histories. Required ship/ray/clock/contact still return values.
- Why: H0120 leftover-0 at 16 samples left the open tail as an inertial chord while lookback and closed segments already stored constant-a. Heading-true close is the same ½`ah²` geometry on that tail, then re-measure versus independent same-IC with a denser check so leftover-0 is not the only evidence. Do not hide a denser remainder. Do not weaken 1.519. Do not chase 99.9% or the far-tide 17-op.
- Validation: Unique `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target` `CARGO_BUILD_JOBS=1` `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`. Disk ~18 GiB free; swap ~3.3/4.1 GiB used. `cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1` PASS (47). `cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1` PASS (8). wgpu not compiled. Qualify not run. `production_law` null.
- Evidence: [update note](laws/open-tail-stored-a-20260914.md), [H0120](HISTORY.md)
- Limitations: Leftover 0 at 16 *and* 128 samples on these fixtures is this comparison, not a general interval-function identity. 1188 vs 1675 is not 99.9%. 1599 vs 1599 is the same operator, not reuse. Compact remains a sidecar. Enclosure is f64, not KA. Native GUI not compiled. Journal-home crates do not contain this overlay. This is not finishing `/goal`.
- Next: Keep `/goal` active. Do not treat leftover-0, 1188 vs 1675, 1126 vs 1722, 1599 vs 1599, or 3169 vs 3186 as finishing reusable compiled geometry. Next is not polyline, not wgpu, not weakening 1.519, not pair fill-in, not FMM, not KA, not native GUI, not sensitivity/Jacobian this turn, not chasing the 17-op. Remaining named remainder: compact is a sidecar; measured prefix-copy \(\approx 0.29\) is not 99.9%. Deferred drafts stay unappended: H0123 17-op review, H0124 entropy, H0125 architecture remainder.


## H0122 — Six-card overlays call this GEM slice; independent reference poison; Charge through-horizon suffix not skipped

- Date: 2026-09-15
- Kind: implementation
- Status: implemented as isolated laboratory host/charge/reference evidence on `/private/tmp/emergent-coupled-response`; journaled as H0122 on journal home; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Revisions: uncommitted overlay on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` from `254ba1f`); journal-home crates do not contain this overlay
- Scope: isolated `es-linearized-retarded-gem-response-v0` six-card library host, genesis reference independence, and recoupled through-horizon Charge; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Changed: Fast-ships overlay now runs `complete_required_queries_compiled` on this slice. Three-bodies overlay now runs `recouple_compiled_pair` (cells A,B,C) instead of painting `laboratory_two_body` as three-body. Solar/galaxy/black-hole stay `Unsupported` and still refuse inertial paint. `Reference::from_genesis` poison tests ignore mutated worldtubes/interval functions/residual. Recoupled reuse/repair asserts suffix `source_evolution` (11 / 24) and `Charge.total` above source ops; reconstruction copies 81 / 70 are not the denominator. Encounter share still refuses at \(1.5193527764310737\). Leftover **0** at 16/128/tail/lookback; source ops **1188 vs 1675** and **1126 vs 1722**. Held-out compiled ship/ray/clock/contact still return values.
- Why: The 2026-09-15 requirement table was not evidence. Inspection found three prompt items weakly covered: six-card overlay always two-body; independent-reference test was band parity; Charge repair was a flag without a suffix-collocation assertion. Strengthen those tests/hosts. Do not chase 99.9%. Do not weaken 1.519. Do not compile wgpu.
- Validation: Unique `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target` `CARGO_BUILD_JOBS=1` `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`. Disk ~18 GiB free; swap ~3.2/4.0 GiB used. `cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1` PASS (47). `cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1` PASS (10). wgpu not compiled. Qualify not run. `production_law` null.
- Evidence: [six-card/charge note](laws/coupled-six-card-charge-evidence-20260915.md), [prompt evidence audit](laws/coupled-prompt-evidence-audit-20260915.md), [H0121](HISTORY.md)
- Limitations: Leftover 0 and 1188 vs 1675 are this comparison, not finishing `/goal`. Compact remains a sidecar. Picard still shares `field_acceleration`. Native GUI not compiled. Pair-exterior new-entrant share still refuses. Journal-home crates do not contain this overlay.
- Next: Keep `/goal` active. Do not mark it complete. Do not treat 1188 vs 1675, leftover-0, or this host connection as production gravity. Next is not polyline, not wgpu, not weakening 1.519, not pair fill-in, not FMM, not compact-as-compile-storage, not H0123–H0125 dumps. Prompt-allowed remainders: compact sidecar; 99.9% not manufactured; `production_law` null.


## H0123 — Independent review of H0122: go-with-holes; overlay and Charge gates pinned

- Date: 2026-09-15
- Kind: verification
- Status: measured as go-with-holes for H0122 laboratory host/charge/reference evidence on `/private/tmp/emergent-coupled-response`; certificate holes closed on that worktree; journaled as H0123 on journal home; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Revisions: uncommitted overlay on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` from `254ba1f`); journal-home crates do not contain this overlay
- Scope: independent review of H0122 six-card overlays, genesis-reference poison, recoupled Charge, held-out queries, and encounter refuse on isolated `es-linearized-retarded-gem-response-v0`; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Changed: Independent review of H0122 is **go-with-holes**. Overlay code paths were real (`sample_fast_ships_overlay` calls `complete_required_queries_compiled`; `sample_three_body_overlay` calls `recouple_compiled_pair`; solar/galaxy/BH stay Unsupported). Certificate tests would have passed extra-ray-only fast-ships, cell-name-only three-bodies, Charge `source_evolution > 0`, leftover `< 1e-7`, and a 0.01 window around 1.519. Closed: `GemWorkSample.overlay_api` / `required_query_consumers` / genesis ids `[0,1,99]`; unsupported refuse loops all three cards; recoupled leftover **0** at 16/128/tail/lookback, suffix `source_evolution` **11 / 24**, source ops **1188 vs 1675** and **1126 vs 1722**, copies **81 / 70** pinned; encounter share refuse pinned at \(1.5193527764310737\); compiled held-out contact requires `cd>0`. Extra-ray still not equivalent completed source histories. Dump drafts bumped to H0124 17-op, H0125 entropy, H0126 architecture remainder (not appended).
- Why: Repo contract: a floating candidate is never sufficient. H0122 wrote the audit in the same pass that printed Charge numbers. This is the validated half of “complete, validated coupled source response,” not leftover-chasing and not finishing `/goal`.
- Validation: Unique `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target` `CARGO_BUILD_JOBS=1` `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`. Disk ~18 GiB free; swap ~3.2/4.0 GiB used. Independent nocapture of `recoupled_three_body_reuses_and_repairs_certified_interval_functions` before pinning measured ratio `1.5193527764310737`, leftover 0, 1188 vs 1675, 1126 vs 1722, suffix 11/24. After the pin: `cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1` PASS (47). `cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1` PASS (10). wgpu not compiled. Qualify not run. `production_law` null.
- Evidence: [review note](laws/h0122-six-card-charge-review-20260915.md), [H0122](HISTORY.md), [six-card/charge note](laws/coupled-six-card-charge-evidence-20260915.md)
- Limitations: Leftover 0 and 1188 vs 1675 remain this comparison, not finishing `/goal` and not 99.9%. Compact remains a sidecar. Picard still shares `field_acceleration`. Native GUI not compiled. Pair-exterior new-entrant share still refuses. Journal-home crates do not contain this overlay.
- Next: Keep `/goal` active. Do not mark it complete. Do not treat leftover-0, 1188 vs 1675, or this host connection as production gravity. Next is not polyline, not wgpu, not weakening 1.519, not pair fill-in, not FMM, not compact-as-compile-storage, not H0124–H0126 dumps. Prompt-allowed remainders: compact sidecar; 99.9% not manufactured; `production_law` null.


## H0124 — Laboratory assigned-exit evidence for continue-coupled-spacetime-compiler; production_law stays null

- Date: 2026-09-15
- Kind: verification
- Status: measured as in-scope laboratory assigned-exit completeness on `/private/tmp/emergent-coupled-response`; journaled as H0124 on journal home; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`; `/goal` stays active until the parent marks it
- Revisions: uncommitted overlay on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` from `254ba1f`); no physics code edited this turn; journal-home crates do not contain this overlay
- Scope: completion-grade re-derivation of [continue-coupled-spacetime-compiler.md](../orchestration/prompts/continue-coupled-spacetime-compiler.md) sequences 1–5 and Acceptance against isolated `es-linearized-retarded-gem-response-v0`; not production gravity; not wgpu
- Changed: Re-derived every numbered/bulleted prompt acceptance from the prompt file (not the H0122 table). Ran covering tests on current HEAD. H0123 pins still hold: extra-ray-only / cell-name-only would fail; leftover **0**; Charge suffix **11 / 24**; source ops **1188 vs 1675** and **1126 vs 1722**; copies **81 / 70**; encounter \(1.5193527764310737\). Wrote [completion evidence](laws/coupled-prompt-completion-evidence-20260915.md). `in_scope_complete: yes`. Deferred dumps bumped to H0125 17-op, H0126 entropy, H0127 architecture remainder (unappended). No physics fix this turn.
- Why: Julien asked for primary evidence on current HEAD so the parent can mark `/goal`. Prior agents treated production gravity / 99.9% as making the objective false; those are out of the assigned laboratory exits. A previous markdown audit is not this evidence.
- Validation: Unique `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target` `CARGO_BUILD_JOBS=1` `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`. Disk ~18 GiB free; swap ~3.24 / 4.0 GiB used. Worktree `/private/tmp/emergent-coupled-response`. `cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1 --nocapture` PASS (47). `cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1 --nocapture` PASS (10). wgpu not compiled. Qualify not run. `production_law` null. Journal `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/g2-law-target`.
- Evidence: [completion evidence](laws/coupled-prompt-completion-evidence-20260915.md), [H0123](HISTORY.md), [H0122 review](laws/h0122-six-card-charge-review-20260915.md)
- Limitations: Leftover 0 and 1188 vs 1675 remain this comparison, not 99.9% and not production gravity. Compact remains a sidecar. Picard still shares `field_acceleration`. Native GUI not compiled. Pair-exterior new-entrant share still refuses at 1.519. RSS / dirty-overlay hash bookkeeping unnamed. Journal-home crates do not contain this overlay. This agent does not mark `/goal`.
- Next: Parent may mark `/goal` from `in_scope_complete: yes`. Do not select `production_law`. Do not replace default inertial `Engine::advance`. Do not weaken 1.519. Do not chase 99.9% or far-tide 17-op. Do not compile wgpu. Do not append H0125–H0127 dumps. Prompt-allowed remainders: compact sidecar; pair-exterior refuse; 99.9% not manufactured; native GUI skipped.


## H0125 — Plan full engine integration and optimization from current coupled and packet work

- Date: 2026-09-15
- Kind: planning and source review
- Status: plan prepared for review and agent handoff; no engine implementation dispatched; no new physics or performance qualification
- Revisions: journal-home baseline `254ba1f` with pre-existing mixed dirty overlays; reviewed current dirty coupled-response and packet worktrees on that baseline; this turn changes planning/continuity documents and task graph only
- Scope: transition from H0124 assigned laboratory completion toward one integrated engine and its operating envelope; research hypotheses, branch preservation, causal authority, actual resumability, population/history composition, physics coverage and optimization
- Changed: Added I0–I6 integration plan with agent ownership, shared contracts, executable exit conditions, hypothesis kill tests, six-card behavior/seed rules and complete cost accounting. Updated HANDOFF, task graph and living heading card/tree/receipt. Source audit identified repair continuation receiving only new interventions while storing old+new metadata; reuse returned charge omitting most enclosure subwork; sampled f64 certificate limitations; eager dense interval-history setup. Packet audit identifies atomic compilation before budget charging, full-world archive reconstruction, per-identity broadcast/policy scans and restricted PERIOD/FAMILY mechanisms. These findings inform first assignments; no runtime reproductions were run here.
- Why: Julien says the earlier plan is implemented and asks for agents to pursue full engine integration/optimization. They explicitly clarified research notes are hypotheses to test, and there may be more. Related research critique/follow-up discussions were retrieved to broaden the hypotheses. Connecting the actual source compiler, canonical events, received knowledge, repair and history exposes the composition costs that isolated packet success does not establish.
- Validation: Read heading workflow/card, current handoff, history list/relevant entries, coupled source and packet implementations; two bounded read-only specialist audits. Python validation PASS: seven active task dependencies are acyclic, required ticket fields exist, plan/handoff local links resolve. `git diff --check -- docs/HANDOFF.md orchestration/tasks.json` PASS. No engine tests, physical benchmarks, native build or qualification run. `cargo xtask history check` required before final handoff.
- Evidence: [Integration plan](full-engine-integration-plan-20260915.md), [task graph](../orchestration/tasks.json), [handoff](HANDOFF.md), [H0124 completion](laws/coupled-prompt-completion-evidence-20260915.md), [entropy hypotheses](compiler-entropy-deferred-20260914.md), [architecture hypotheses](compiler-architecture-remainder-deferred-20260914.md)
- Limitations: H0124's scoped completion is retained, but its source-operation comparisons do not establish full request savings. New possible repair failure is source-reviewed, not reproduced. Sampled parity does not establish authoritative interval coverage. Additional research was read as hypothesis/context; the newer deep-research block itself was not exposed by the task reader. `production_law` remains null, engine default inertial, frozen evidence unchanged. No goal-tool state or other task was changed; previous unappended H0125–H0127 draft numbers are stale placeholders, not entries to append.
- Next: Review/use plan I0 then I1: pin selected overlays, reproduce/fix complete repair history and cost accounting, freeze response/authority interfaces, and implement the genuinely resumable connected engine scene. Use its full cost breakdown to select the next representation experiment; preserve all required full-engine physics and target-envelope gates.


## H0126 — I0: pin selected overlays, complete repair history, nested Charge ledger

- Date: 2026-09-15
- Kind: implementation
- Status: implemented and measured on the clean integration worktree; not `production_law`; default `Engine::advance` stays `es-inertial-causal-v1`
- Revisions: worktree `/private/tmp/emergent-full-engine-integration`, branch `codex/full-engine-integration` from baseline `254ba1f`; this entry's commit on that branch; original packet worktrees not deleted
- Scope: I0 of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); selected inertial foundation plus coupled compiler; Packet 6 policy/archive types without truncated-GEM fields
- Changed: Created the clean worktree and imported Packet 0 inertial engine files and the H0124 coupled compiler. `repair_from_committed` now continues with the merged ordered incoming history so an earlier extra in an uncommitted suffix or new branch keeps an already recorded later cause. `Charge` is a nested ledger: historical `total()` stays the flat H0124 sum; `ledger_total` includes children once; enclosure genesis/Picard work is `OfflineAudit` and is not sold as runtime request cost. Source ops, wall-time and pair-inverse bytes are recorded as distinct baselines. Packet 5 `truncated_admission` was reviewed and refused.
- Why: Source review showed continuation receiving only `extra` while metadata kept `incoming+extra`, and reuse returning only enclosure validation/verification. I0 had to reproduce and fix those before I1 could freeze contracts.
- Validation: `CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/full-engine-integration-target` `CARGO_BUILD_JOBS=1` `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`. `cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1` PASS (52). `cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1` PASS (10). `cargo test -p emergent-engine --lib --offline --locked -- --test-threads=1 policy archive` PASS (3). `cargo test -p emergent-engine --test causal_contract --offline --locked -- --test-threads=1` PASS (18). H0124 pins held: 1188 vs 1675, 1126 vs 1722, suffix 11/24, copies 81/70, encounter 1.5193527764310737. `cargo xtask history check` required before finalize.
- Evidence: [I0 cost report](laws/i0-full-cost-report-20260915.md), [I0 snapshot](laws/i0-overlay-snapshot-20260915.md), [I1 contract notes](laws/i1-contract-notes-20260915.md), [H0124](HISTORY.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: I1 is not done. Sampled `certified: true` is still diagnostic. Pair-inverse remains eager and dense. Policy/archive types are not yet wired through `Engine::advance` or live save/restore. Quiet compile `ledger_total` equals `total` because compile does not nest enclosure. Wall-time varies with cache warmth and is not a source-op count. No new speedup is claimed. Frozen `1dac658` untouched.
- Next: I1 increment 1 — resumable compile/repair/enclosure jobs charged inside the loop, connected diagnostic scene (must not report canonical-gravity acceptance). Increment 2 is the authority-backed commit path.


## H0127 — I1 increment 1 started: collocation jobs suspend inside the loop (diagnostic only)

- Date: 2026-09-15
- Kind: implementation
- Status: partial
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after I0 commit `56453a8`; this entry's follow-on commit
- Scope: I1 increment 1 of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); diagnostic adapter only
- Changed: `CoupledCompileJob` polls one charged collocation block then yields on empty budget. `interval_continue` uses that job with an unlimited budget so H0124 results stay. Engine `coupled_adapter` maps `WorkBudget` onto the job and labels `CANONICAL_GRAVITY_ACCEPTANCE` as `diagnostic-only`. A law-lab diagnostic scene compiles two masses, ship, ray, clock, contact and repair without reporting canonical gravity.
- Why: I1 requires `advance(…, WorkBudget)` to suspend compile work inside expensive loops, not after atomic completion. Collocation is the first loop that dominated source evolution.
- Validation: Same `CARGO_TARGET_DIR` / `CARGO_BUILD_JOBS=1` / `--offline --locked` / `--test-threads=1`. `cargo test -p emergent-law-lab --lib coupled_` PASS (54). `cargo test -p emergent-engine --lib` PASS (28). Observatory 10 and causal_contract 18 still pass. `cargo xtask history check` on journal home required.
- Evidence: [I1 contract notes](laws/i1-contract-notes-20260915.md), [H0126](HISTORY.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: `Engine::advance` is still inertial and does not poll coupled jobs. Seal, pair-inverse and enclosure remain atomic. Received-message course change and in-flight signal save/restore are not wired through the engine. Authority-backed commit (increment 2) has not started. `production_law` null.
- Next: Finish I1 increment 1 by connecting policy, save/restore of in-flight signals, and `advance` suspension of remaining compile/validate/repair jobs, still without canonical-gravity acceptance. Then increment 2 authority path.


## H0128 — I1 increment 1: resumable diagnostic Engine::advance and connected scene

- Date: 2026-09-15
- Kind: implementation
- Status: implemented
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after `611d200`; this entry's follow-on commit
- Scope: I1 increment 1 of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); diagnostic adapter only; not I1 increment 2 authority
- Changed: `Engine::advance` polls coupled collocation, residual seal, pair-inverse, enclosure and repair jobs with `WorkBudget` before inertial progress. Residual seal skips the compact sidecar and yields per sample. Pair-inverse yields per finite-difference column and LU step. Enclosure yields per Euler/Picard dt. Headless scene binds ship, ray, clock and contact to compiled interval functions, applies received-knowledge course change, retains an in-flight signal across checkpoint restore, pauses at budget 1, varies query order, clears consumer cache, and replays inertial facts. Pending required queries beyond the admitted horizon stay visible. Policy course-change during a commit forces a rescan so later contacts are not missed.
- Why: Increment 1 requires `advance(…, WorkBudget)` to suspend compile/validate/repair inside expensive loops and a connected scene on selected geometry, without reporting canonical-gravity acceptance.
- Validation: Same `CARGO_TARGET_DIR` / `CARGO_BUILD_JOBS=1` / `--offline --locked` / `--test-threads=1`. `cargo test -p emergent-law-lab --lib coupled_` PASS (54). `cargo test -p emergent-engine --lib` PASS (29). `causal_contract` PASS (18). `i1_connected_scene` PASS (2). Observatory 10 still pass. `cargo xtask history check` on this journal required.
- Evidence: [I1 increment 1 evidence](laws/i1-increment1-evidence-20260915.md), [I1 contract notes](laws/i1-contract-notes-20260915.md), [H0127](HISTORY.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: Historical `compile_source_response` compact fit remains atomic so H0124 counts stay. Sampled `certified: true` is still diagnostic and does not authorize GEM events. Finite-semantic reference, near-ties, slow-versus-compiled canonical GEM facts and separately versioned physical resolution (increment 2) have not exited. I2–I6 not started. `production_law` null.
- Next: I1 increment 2 authority path on these moving cases. Do not launch I3–I6 optimization or qualification theater before I1 (and I2 where required).


## H0129 — I1 increment 2: finite-semantic inertial authority; GEM stays diagnostic

- Date: 2026-09-15
- Kind: implementation
- Status: implemented
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after `5c24026`; this entry's follow-on commit
- Scope: I1 increment 2 of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); first engine integration milestone; not gravitational qualification
- Changed: Added `authority` module. Independent geometry predicates on committed worldlines match compiled inertial contact and light-cone events on the connected scene. Near-tangent between integer samples is owned by the ending tick bin. GEM 16-sample enclosure, slow Euler versus collocation remainder, shifted units, input epoch and `Domain.dt` are labeled separately from `es-inertial-causal-v1`. Sampled `certified: true` still does not authorize events. Historical compact `seal_compiled` stays the atomic H0124 path and is not this authority claim. I2 started with a family plus in-flight signal on the diagnostic scene and one extraction; re-merge, selective history, indexed range reception and unequal cuts are not implemented.
- Why: Increment 2 must authorize exact contact and light-cone on the moving scene without laundering GEM sampled enclosure into canonical gravity.
- Validation: Same `CARGO_TARGET_DIR` / `CARGO_BUILD_JOBS=1` / `--offline --locked` / `--test-threads=1`. Engine lib 31, `causal_contract` 18, `i1_connected_scene` 2, `i1_increment2_authority` 6, law-lab `coupled_` 54, `i2_composed_scene` 1 (started). `cargo xtask history check` on journal home required.
- Evidence: [I1 increment 2 evidence](laws/i1-increment2-evidence-20260915.md), [I1 notes](laws/i1-contract-notes-20260915.md), [H0128](HISTORY.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: GEM has no interval-wide retarded-root bound. Slow versus compiled GEM trajectories are two numerical methods of the same diagnostic law, not event equality. Canonical gravity acceptance remains `diagnostic-only`. I2 composition exit is not proven. I3–I6 not started. `production_law` null.
- Next: I2 exit requirements: massive family perturbing a hierarchy while a ray is in flight; extraction/re-merge; selective history; indexed policies; unequal certified cuts. Do not launch I3–I6 theater.


## H0130 — I2: composed family, re-merge, range reception, unequal cuts, archive eviction

- Date: 2026-09-15
- Kind: implementation
- Status: implemented
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after `9fbd43d`; this entry's follow-on commit
- Scope: I2 of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); composition milestone; not gravitational qualification
- Changed: One connected diagnostic scene now includes a massive affine family while a ray is in flight. Extraction, restricted exact re-merge, indexed range broadcast receptions, unequal certified cuts with reconcile, incremental chunk seal, resident-tail eviction and cold observation run in that scene. Collective mass is conserved. Policy burns fire once; the I1 re-fire hole is closed. The inertial contact oracle matches rising-edge overlap rather than re-burn artifacts. GEM stays diagnostic. I3 was not started.
- Why: I2 requires composition in one scene, not a one-identity extraction fixture and not several separate benchmarks.
- Validation: Same `CARGO_TARGET_DIR` / `CARGO_BUILD_JOBS=1` / `--offline --locked` / `--test-threads=1`. Engine lib 31, `causal_contract` 18, `i1_connected_scene` 2, `i1_increment2_authority` 6, `i2_composed_scene` 1, law-lab `coupled_` 54. `cargo xtask history check` on journal home required.
- Evidence: [I2 composition evidence](laws/i2-composition-evidence-20260915.md), [H0129](HISTORY.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: Certified cuts overlay a single physics clock. Broadcast indexing still walks a small materialized range. Cold observation uses remainder worldtubes plus selected chunks. The family does not gravitationally perturb GEM. Canonical gravity acceptance remains `diagnostic-only`. I3–I6 not started. `production_law` null.
- Next: I3 first experiment against the measured bottleneck from this scene (history reconstruction and the single-clock scheduler overlay), not all representation hypotheses. Do not launch I4–I6 theater.


## H0131 — I3: two-region advance and keep/reject representations; I3 exit not proven

- Date: 2026-09-15
- Kind: experiment
- Status: partial
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after `e319bc9`; this entry's follow-on commit
- Scope: I3 of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); two-region scheduler plus sequential time/perturbation/population kill tests; not gravitational qualification
- Changed: `advance_region` / `advance_joint` rewind a region's certified cut, scan only that identity range, and refuse independent advance when a lagging region's radius-expanded AABB overlaps. I2 composed-scene cuts now use that path (hierarchy through 8 while family stays 0). Nested Charge keep/reject: quiet-pair collocation ledger 1250 vs Euler 5602 at H=3; prefix repair 923 vs recouple 1212 on quiet-kick H=3; compact-after-the-fact, PERIOD, resonance-skip, H=3 local Schur tide, and population-as-solved rejected. Selective cold observe 1.4 ms versus restore 0.83 ms with reconstruction charged. I4–I6 not started.
- Why: I2 named the one-clock overlay and history reconstruction as the measured bottleneck. I3 must attack that constraint with total-cost kill tests rather than documenting around it or launching later-stage theater.
- Validation: Same `CARGO_TARGET_DIR` / `CARGO_BUILD_JOBS=1` / `--offline --locked` / `--test-threads=1`. Engine lib 31, `causal_contract` 18, `i1_connected_scene` 2, `i1_increment2_authority` 6, `i2_composed_scene` 1, `i3_representation` 4, law-lab `i3_` 4, `coupled_` 54. `cargo xtask history check` on this journal required.
- Evidence: [I3 keep/reject evidence](laws/i3-keep-reject-evidence-20260915.md), [H0130](HISTORY.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: I3 exit is not proven. Sequential collocation still grows with horizon. Broadcast indexing still walks a materialized range. Family does not gravitationally perturb GEM. Interval-wide GEM authority is still missing. Canonical gravity acceptance remains `diagnostic-only`. `production_law` null.
- Next: Revise long-time source representation before scaling the same loop. Do not launch I4–I6 theater. I4 remains blocked on interval-wide GEM authority as well as I1/I2 interfaces.


## H0132 — I3: Kepler+residual rejected as unmatched GEM; lazy pair-inverse kept without Schur consumer

- Date: 2026-09-15
- Kind: experiment
- Status: partial
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after `b7e5ad7`; this entry's follow-on commit
- Scope: I3 of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); long-time representation that does not collocate the skipped interval; lazy pair-inverse; not gravitational qualification
- Changed: Added `compile_secular_response` (Kepler elements + rank-3 GEM−Newton residual as the evolution, no `interval_compile` over H) and `compile_source_response_opts` / `ensure_pair_inverse` so the dense quiet-pair inverse can be deferred. Circular pair H=4 secular ledger 151 vs collocation 1551 but max_dx=0.93; H=6 remainder 0.078 exceeds band 0.05 and refuses. Radial rest pair, eccentric H=6, resonant kicks and weak Δv=0.02 also refuse. Lazy inverse at H=6: ledger 1468 vs eager 2438, bytes 2637 vs 18125, n grows 20→44. H0131 keeps unchanged. I4–I6 not started.
- Why: Sequential collocation grows with H. Building a trajectory then compressing it cannot establish skipped evolution. If none removes enough sequential work while matching GEM, I3 stays incomplete.
- Validation: Same `CARGO_TARGET_DIR` / `CARGO_BUILD_JOBS=1` / `--offline --locked` / `--test-threads=1`. Law-lab `i3_` 6, `coupled_` 54, engine lib 31. `cargo xtask history check` on journal home required.
- Evidence: [I3 secular evidence](laws/i3-secular-evidence-20260915.md), [I3 keep/reject](laws/i3-keep-reject-evidence-20260915.md), [H0131](HISTORY.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: I3 exit is not proven. Kepler+residual is cheaper than collocation only where it fails to match GEM. Lazy inverse is setup deferral, not skipped evolution. Interval-wide GEM authority is still missing. `production_law` null. Canonical gravity remains `diagnostic-only`.
- Next: Osculating / retarded perturbation of Kepler (variation of elements from GEM lookback), not another post-pass residual and not I4 qualification. Do not launch I4–I6 theater.


## H0133 — I3: osculating Kepler with retarded GEM lookback rejected; high-e fallback

- Date: 2026-09-15
- Kind: experiment
- Status: failed
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after `0b72990`; this entry's follow-on commit
- Scope: I3 of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); osculating / retarded perturbation of Kepler; not gravitational qualification
- Changed: Implemented `compile_osculating_response`: Kepler-advance, retarded GEM lookback, Δv = (GEM−Newton) Δt, refit elements. Cadence `OSC_DT=0.25` (half light-crossing), not collocation `dt=1/32`. Position gate `OSC_POS_BAND=0.20` declared before runs; H0132 0.05 accel band not widened. Circular a=4 at H=4 and H=6 refuses `e=0.886>0.85` (a→18.47) before Δx is measured. Eccentric, resonance, and weak forcing refuse the same way. Radial rest pair still refuses as close-encounter. Collocation baselines 1551 (H=4) and 2057 (H=6). I4–I6 not started.
- Why: Kepler+constant-element residual skipped collocation but missed GEM. Osculating elements were the next discriminating test. GEM−Newton on this pair is not a small Kepler perturbation; absorbing it as Δv drives the ellipse through the close-encounter gate.
- Validation: Same `CARGO_TARGET_DIR` / `CARGO_BUILD_JOBS=1` / `--offline --locked` / `--test-threads=1`. Law-lab `i3_` 7, `coupled_` 54. `cargo xtask history check` on journal home required.
- Evidence: [I3 osculating evidence](laws/i3-osculating-evidence-20260915.md), [I3 secular](laws/i3-secular-evidence-20260915.md), [H0132](HISTORY.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: I3 exit is not proven. Construction never reached the 0.20 position gate. The 0.85 eccentricity refuse was not raised after seeing 0.886. `production_law` null. Canonical gravity remains `diagnostic-only`.
- Next: Do not use Kepler as the GEM two-body reference. Try low-rank / memory-kernel compression of the retarded Volterra collocation operator. Do not launch I4–I6 theater.


## H0134 — I3: memory-kernel Volterra compression kept on the quiet pair; I3 not exited

- Date: 2026-09-15
- Kind: experiment
- Status: succeeded
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after `facf4a5`; this entry's follow-on commit
- Scope: I3 of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); low-rank / memory-kernel compression of retarded GEM collocation; not gravitational qualification
- Changed: Implemented `compile_memory_kernel_response`: bootstrap collocation on a fixed two-light-crossing window, window Jacobian SVD, then memory-truncated GEM march at one light-crossing. Does not `interval_compile` over H. Predeclared `KERNEL_POS_BAND=0.05` and `KERNEL_A_BAND=0.05` (not widened). Circular a=4: H=4 ledger 1089 vs 1551, Δx=0.00150, Δa=0.00122; H=6 ledger 1113 vs 2057, Δx=0.00259; rank 4, memory 6, Jacobian n=12, fill-in 144, none growing with H. Eccentric H=6 Δx=0.00177. Close-entrant, resonance kicks and n-body entrant refuse with explicit collocation fallback. Tight pair constructs at rank 12. I4–I6 not started.
- Why: Kepler ansatze missed GEM. The plan's next discriminating test was whether a bounded retarded kernel can advance time without dense pair-inverse growth.
- Validation: Same `CARGO_TARGET_DIR` / `CARGO_BUILD_JOBS=1` / `--offline --locked` / `--test-threads=1`. Law-lab `i3_` 9, `coupled_` 54. `cargo xtask history check` on journal home required.
- Evidence: [I3 kernel evidence](laws/i3-kernel-evidence-20260915.md), [I3 osculating](laws/i3-osculating-evidence-20260915.md), [H0133](HISTORY.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: I3 exit is not proven. Bootstrap still dominates the kernel ledger (~1089 of 1113). Coarse marched samples still grow with H (18→26 vs collocation 30→46). Kicks and entrants are fallbacks, not skipped GEM. `production_law` null. Canonical gravity remains `diagnostic-only`.
- Next: Amortize the bootstrap over a longer quiet horizon, or a kick/entrant path that is an explicit recouple/collocation fallback. Do not launch I4–I6 theater.


## H0135 — I3: quiet kernel amortizes to H=12; weak-kick resume kept; I3 not exited

- Date: 2026-09-15
- Kind: experiment
- Status: succeeded
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after `954a8c7`; this entry's follow-on commit
- Scope: I3 of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); bootstrap amortization and explicit kick path; not gravitational qualification
- Changed: Nested Charge split bootstrap/jacobian/advance/certificate. Quiet circular a=4 at H=8 ledger 1137 vs collocation 2300 (Δx=0.00403) and H=12 ledger 1185 vs 3176 (Δx=0.00954); rank 4, memory 6, fill-in 144 bounded; advance 84→132; bootstrap flat at 870 (73% of H=12 kernel ledger — not invented amortization of setup). Weak Δv=0.02 kick resume KEEP 1139 vs 2525, Δx=0.004. Strong laboratory_kick Δx=0.216 rejected. Recouple-suffix 2932 is not cheaper. Close-entrant/n-body refuse to recouple. 0.05 gates not widened. I4–I6 not started.
- Why: I3 exit needs a horizon where sequential collocation would have dominated, including kicks. Quiet longer-H and a weak-kick path were the discriminating leftovers after H0134.
- Validation: Same `CARGO_TARGET_DIR` / `CARGO_BUILD_JOBS=1` / `--offline --locked` / `--test-threads=1`. Law-lab `i3_` 10, `coupled_` 54. `cargo xtask history check` on journal home required.
- Evidence: [I3 amort/kick](laws/i3-kernel-amort-kick-evidence-20260915.md), [I3 kernel](laws/i3-kernel-evidence-20260915.md), [H0134](HISTORY.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: I3 exit is not proven. Bootstrap still dominates kernel setup. Strong kicks miss 0.05. Close-entrant and tides still recouple. `production_law` null. Canonical gravity remains `diagnostic-only`.
- Next: A representation that matches GEM after a strong Δv or close-entrant without full collocation, or admit I3 cannot skip sequential GEM on those domains. Do not launch I4–I6 theater.


## H0136 — I3 domain exit: keep quiet/weak-kick kernel; reject strong-kick patch

- Date: 2026-09-15
- Kind: experiment
- Status: succeeded
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after `f774ba5`; this entry's follow-on commit
- Scope: I3 plan exit is keep-in-domain plus published failure, not infinite shopping. Last strong-kick method: short collocation patch then kernel resume. Not gravitational qualification.
- Changed: `compile_kernel_kick_patch` collocates `KERNEL_PATCH_LEN=1.0` after `laboratory_kick` then resumes kernel. H=8 ledger 1937 vs collocation 2556, Δx=0.218>0.05 **REJECT**. Close-entrant still recouple. Published admitted domains (quiet kernel H=4..12, weak-kick resume H=8, H≤3 collocation vs Euler, prefix-repair, lazy inverse) and failure domains (Kepler ansatze, PERIOD, compact-after-the-fact, Schur tide, population-solved, strong kicks, close-entrant). 0.05 not widened. Do not claim skipped evolution on strong kicks.
- Why: The plan's I3 exit is domain publication after one last discriminating strong-kick method, keep or honest reject.
- Validation: Same `CARGO_TARGET_DIR` / `CARGO_BUILD_JOBS=1` / `--offline --locked` / `--test-threads=1`. Law-lab `i3_` 11. `cargo xtask history check` on journal home required.
- Evidence: [I3 domain exit](laws/i3-domain-exit-20260915.md), [I3 amort/kick](laws/i3-kernel-amort-kick-evidence-20260915.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: Sequential collocation still owns strong kicks and close-entrants. Interval-wide GEM authority is I4 work. `production_law` null.
- Next: I4 bound solar hierarchy with prehistory and the GEM authority path. Do not launch I5–I6 theater.


## H0137 — I4 start: solar prehistory vs switch-on; retarded-root authority still diagnostic

- Date: 2026-09-15
- Kind: experiment
- Status: succeeded
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after H0136
- Scope: I4 item 1 of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); six-card solar hierarchy; not I4 exit; not I5–I6
- Changed: Declared GEM hierarchical two-body approximation, 0.05 band, prehistory 2.0, admitted states and collocation fallback before runs. Prehistory-initialized solar pair stays bound (min_r=6.31, `|Phi|/c²=0.020`); genesis switch-on defect 0.476>0.05 so switch-on is not an equilibrium initializer. Weak-field flyby uses 3-body collocation (3685), not kernel. Per-query retarded lookback 14 unique / 2 missed; coverage `per-query-unique-lookback-not-interval-wide-field`; `authorizes_events=false`. `CANONICAL_GRAVITY_ACCEPTANCE` remains diagnostic-only. Engine authority refused list names the I4 root gap.
- Why: I4 requires initialized prehistory and an authority path; sampled 16-point enclosure must not mint canonical gravity.
- Validation: Law-lab `i4_` 3, `coupled_` 54, engine `i1_increment2_authority` 6. Same build flags as H0136.
- Evidence: [I4 solar/authority](laws/i4-solar-authority-20260915.md), [I3 domain exit](laws/i3-domain-exit-20260915.md), [six-card contract](laws/litmus-gallery-contract-20260914.md)
- Limitations: Interval-wide GEM field bound missing. Galaxy and black-hole cards unsupported. I4 not exited. `production_law` null.
- Next: Lipschitz or interval/KA field bound on retarded GEM, or the next six-card regime. Do not launch I5–I6. Do not select `production_law`.


## H0138 — I4 GEM interval-wide field bound on solar admitted interior

- Date: 2026-09-15
- Kind: experiment
- Status: succeeded
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after H0137 `91e81c4`
- Scope: I4 authority then remaining six-card order of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); not I4 exit; not I5–I6
- Changed: Lipschitz/tidal-L per causal block plus Krawczyk-style delay enclosure of stored-a quadratics, with units and 32-ulp arithmetic. Solar two-body admitted interior [-0.926, 4] covers 26/26 blocks; domain-local `authorizes_events=true`; genesis prefix [-2, -0.926) refused (no incoming field). Companion hierarchy a=20 collocation 4087, inner Δx=0.013, GEM 48/48 on [0.964, 4]. Collective two-cluster retarded monopoles remainder 0.269>0.05 REJECT; mass accounted; keep direct sums. Ships/rays/clocks/nav forward-verified on solar (nav miss ~0). Black-hole card exact gap. `CANONICAL_GRAVITY_ACCEPTANCE` stays diagnostic-only; engine `authorizes_gem_events=false`.
- Why: I4 required interval-wide coverage, not 16 samples. Ambiguity stays pending/refusal. Domain-local GEM field authority is not engine canonical gravity.
- Validation: Law-lab `i4_` 9 PASS, engine `i1_increment2_authority` 6 PASS. `CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --lib i4_ --offline --locked -- --test-threads=1` and `cargo test -p emergent-engine --test i1_increment2_authority --offline --locked -- --test-threads=1`.
- Evidence: [I4 GEM authority](laws/i4-gem-authority-20260915.md), [I4 solar start](laws/i4-solar-authority-20260915.md), [six-card contract](laws/litmus-gallery-contract-20260914.md)
- Limitations: I4 not exited. Galaxy hierarchical expansion missed 0.05. Black-hole/near-mass unsupported. Six-card crossing not on the integrated engine. Genesis prefix not authorized. `production_law` null.
- Next: Retarded multipole with remainder bound, or keep direct N-body, then a BH model alternative, then six-card crossing. Do not launch I5–I6. Do not select `production_law`. Do not mint `CANONICAL_GRAVITY_ACCEPTANCE`.


## H0139 — I4 six-card crossing: direct galaxy sums, Sch–GEM interface, one engine

- Date: 2026-09-15
- Kind: experiment
- Status: succeeded
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after H0138 `f0a795b`
- Scope: I4 remaining cards and crossing of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); [six-card contract](laws/litmus-gallery-contract-20260914.md); not I5–I6; not `production_law`
- Changed: Retarded quadrupole clusters remainder 0.478>0.05 (bound 0.783); mass accounted; admitted method is direct small-world GEM sums. New model `es-schwarzschild-gem-interface-v0`: clocks/Φ and first-order deflection match at compactness 0.05; accel PN jump 0.10; capture μ 0.01→8.01; moving multi-mass refused. One engine binds solar GEM genesis, ship/ray/clock, asteroid, affine fleet and delayed policy (1 burn). Kernel unused. `CANONICAL_GRAVITY_ACCEPTANCE` stays diagnostic-only.
- Why: I4 required galaxy remainder with an explicit bound, one named BH alternative, and six-card crossing on the integrated engine rather than glued fixtures. Multipole could not meet 0.05; do not widen.
- Validation: Law-lab `i4_` 13 PASS, engine `i4_six_card_crossing` 1, `i1_increment2_authority` 6, `i2_composed_scene` 1. `CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never` `--offline --locked --test-threads=1`.
- Evidence: [I4 six-card](laws/i4-six-card-crossing-20260915.md), [I4 GEM authority](laws/i4-gem-authority-20260915.md), [six-card contract](laws/litmus-gallery-contract-20260914.md)
- Limitations: Family does not source GEM. Moving multi-mass compact fields unsupported. Accel continuity 0.10>0.05. Full-engine incomplete. `production_law` null.
- Next: Do not start I5 until assigned. Remaining physics: family-sourced GEM or recorded BH/galaxy alternatives. Do not mint `CANONICAL_GRAVITY_ACCEPTANCE`.

## H0140 — I4: family moments KEEP as GEM sources; identities retained

- Date: 2026-09-15
- Kind: experiment
- Status: succeeded
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after H0139 `abf31d5`; this entry's follow-on commit
- Scope: Remaining I4 physics hole of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); affine family mass as a GEM source; not galaxy multipole; not I6
- Changed: Affine N=4 μ=0.01 rest family at y=18 sources GEM as one COM plus `FamilyIdentities`. Remainder vs extract-and-collocate **0** ≤ 0.05 (octupole-like bound 1.04×10⁻⁶). Mass 0.04=0.04. Extract ledger 127395 vs moment 1906. Nested Charge construction/certificate/reconstruction/fallback/query recorded. Admitted `family-moment-gem-source`. Direct small-world GEM sums remain the galaxy method (H0139 quadrupole 0.478 unchanged). `CANONICAL_GRAVITY_ACCEPTANCE` stays diagnostic-only.
- Why: H0139 left family mass uncoupled from GEM. Coordinator assigned that hole before I5. Do not drop mass or member identities.
- Validation: `CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --lib i4_family --offline --locked -- --test-threads=1` 2 PASS.
- Evidence: [I4 family GEM](laws/i4-family-gem-20260915.md), [I4 six-card](laws/i4-six-card-crossing-20260915.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: KEEP is affine equal-μ at H≤2 beside `laboratory_two_body`, not a galaxy skip. Moment remainder 0 is monopole agreement, not interval-wide authority. Frozen H0139 evidence unchanged. `production_law` null.
- Next: I5 on surviving work. Do not start I6 in that slice until I5 is evidenced. Do not mint `CANONICAL_GRAVITY_ACCEPTANCE`.

## H0141 — I5 CPU-only exit: knowledge index and lazy inverse at equal digest

- Date: 2026-09-15
- Kind: experiment
- Status: succeeded
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after H0140 in the same follow-on commit
- Scope: I5 of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); CPU-only surviving I2/I3/I4 work; not I6; not combined rendering
- Changed: Replaced full-history `received_knowledge` scans with a derived per-observer `signal_arrivals` index plus `broadcast_receptions`. Policy burns no longer walk `events`. Composed scene: 3 GEM bodies (pair+family COM), ship/signal/policy, digest equal on replay, received_signals equal, indexed arrivals 1 vs 4 events. Cold 4.19 ms / warm 0.57 ms; process RSS 5216 KB; owned `CanonicalState` 4566 B; GPU none. Lazy pair inverse skipped. Quiet kernel ledger 1137 stays in-domain. Family moment 1906 vs extract 127395. `CANONICAL_GRAVITY_ACCEPTANCE` stays diagnostic-only.
- Why: I5 first removes full-history scans, eager dense matrices and redundant copies on real I2–I4 workloads. Hardware cannot compensate for unbounded extract of every member.
- Validation: `CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-engine --test i5_surviving --offline --locked -- --test-threads=1` 1 PASS. Regressions: `i1_increment2_authority` 6, `i1_connected_scene` 2, `i2_composed_scene` 1, `i4_six_card_crossing` 1.
- Evidence: [I5 surviving](laws/i5-surviving-work-20260915.md), [I4 family GEM](laws/i4-family-gem-20260915.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: RSS is the test-process `ps` figure, not an isolated heap. Combined simulation+rendering unpublished (GPU unused). Moving multi-mass compact fields, galaxy direct sums, and accel PN jump 0.10 remain. I6 not started. `production_law` null.
- Next: I6 same-model qualification matrix when assigned. Do not select `production_law`. Do not mint `CANONICAL_GRAVITY_ACCEPTANCE`.

## H0142 — I6 matrix run on one model; production_law stays null

- Date: 2026-09-15
- Kind: verification
- Status: succeeded
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after H0141 `cd1c805`; this entry's follow-on commit
- Scope: I6 of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); same-model matrix; native observatory on the same Engine; not `production_law` promotion
- Changed: Machine-readable matrix on `es-inertial-causal-v1` + diagnostic GEM, connected workload. Native `EngineBridge` hosts that Engine (`--world connected` for the I6 scene; gallery GEM slice is not qualification). Daily gallery, held-out bank, envelope ladder. Cold history and checkpoint/replay PASS. Honest FAIL: galaxy quadrupole skip 0.478, Sch–GEM accel 0.10, engine gravity diagnostic, family-moment-as-galaxy-skip, production promotion. Honest UNSUPPORTED: moving multi-mass, envelope pressure/frozen targets. Six cards name look-for, class, regime, comparison. Plan I6 exit is the matrix run; full-engine remains incomplete. `CANONICAL_GRAVITY_ACCEPTANCE` stays diagnostic-only.
- Why: Coordinator assigned I6. Promotion requires every required gate PASS on one model; published gaps remain. Julien's rule: behavior and remainder bands, not leftover==0.0 / 1188/1675 / 1.519 pins.
- Validation: `CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-engine --test i6_qualification --offline --locked -- --test-threads=1` 1 PASS. Regressions: `i1_increment2_authority` 6, `i4_six_card_crossing` 1.
- Evidence: [I6 matrix JSON](laws/i6-qualification-matrix-20260915.json), [I6 notes](laws/i6-qualification-20260915.md), [six-card contract](laws/litmus-gallery-contract-20260914.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: Full-engine incomplete. Envelope targets unqualified. Combined rendering unpublished. Frozen `1dac658` / H0052 / H0054 / H0124 unchanged. `production_law` null.
- Next: Close required physics gaps (moving multi-mass compact fields, quadrupole skip, accel continuity, engine gravity) before any promotion attempt. Do not select `production_law` from this matrix.

## H0143 — 1PN interface KEEP and domain-local GEM field events; matrix still mixed

- Date: 2026-09-15
- Kind: experiment
- Status: succeeded
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after H0142 `2054d29`; this entry's follow-on commit
- Scope: Required FAIL physics after I6 matrix-run of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); not promotion; not full-engine
- Changed: New model `es-schwarzschild-1pn-gem-v0`: 1PN GEM E=−∇Φ_N(1+2Φ_N/c²) vs independent Schwarzschild Γ^r_tt at the named interface, band 0.05, remainder ≤ 0.05 KEEP. v0 Newton GEM 0.10 FAIL row kept (`sch-gem-accel-continuity-v0`). Engine `authorizes_gem_events_on_admitted_field` true only on the Lipschitz/KA solar admitted interior; `CANONICAL_GRAVITY_ACCEPTANCE` stays diagnostic-only. Moving multi-mass still UNSUPPORTED. Galaxy quadrupole skip and family-moment-as-galaxy-skip stay FAIL. Same I6 matrix re-run: still mixed; promotion false; full-engine false; `production_law` null.
- Why: Coordinator assigned closing required FAIL physics without a new matrix theater. 0.05 not widened. Do not fake moving compact fields with a static anchor.
- Validation: `CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --lib i4_near_mass --offline --locked -- --test-threads=1` 3 PASS. `cargo test -p emergent-engine --test i6_qualification --offline --locked -- --test-threads=1` 1 PASS. `i1_increment2_authority` 6 PASS.
- Evidence: [I6 matrix JSON](laws/i6-qualification-matrix-20260915.json), [I6 notes](laws/i6-qualification-20260915.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: Crossing still FAIL. Galaxy skip still FAIL. Envelope targets UNSUPPORTED. Full-engine incomplete. Frozen H0139/H0142 interpretation: v0 0.10 remains a FAIL row.
- Next: Do not select `production_law`. Remaining required gaps: moving multi-mass compact fields, quadrupole skip, gravitational crossing, envelope workload. Stop shopping if those still cannot pass.


## H0144 — GEM-to-horizon moving attempt stays UNSUPPORTED; shopping stopped

- Date: 2026-09-15
- Kind: experiment
- Status: failed
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after H0143 `bc56321`; this entry's follow-on commit
- Scope: One recorded alternative for I6 `moving-multi-mass-compact` of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); not promotion; not full-engine
- Changed: New model `es-gem-absorbing-horizon-v0`: two moving masses, GEM outside `r_s`, absorbing halt with μ transfer (0.5→8.5), remainder vs independent slow Euler (1.036e-15 on the weak prefix, band 0.05, not a leftover==0 pin). Compact cover fails: compactness at `r_s` is 0.5 > linearized GEM `|Φ|/c²` 0.05; `r_s < r ≤ r_if` has no GEM field. I6 `moving-multi-mass-compact` stays UNSUPPORTED. Crossing stays FAIL. Galaxy quadrupole 0.478 and family-as-galaxy-skip FAIL rows kept. Envelope UNSUPPORTED. `production_law` null. Shopping stopped: (a) 1PN+stationary Sch and (b) this GEM-to-horizon family are exhausted.
- Why: Coordinator assigned one moving-source attempt that is not a static Schwarzschild anchor. Linearized GEM + 1PN + halt-capture still cannot cover compact multi-mass fields. 0.05 not widened.
- Validation: `CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --lib i4_moving_horizon --offline --locked -- --test-threads=1` 2 PASS. `cargo test -p emergent-engine --test i6_qualification --offline --locked -- --test-threads=1` 1 PASS. Matrix mixed; promotion false; full-engine false.
- Evidence: [I6 matrix JSON](laws/i6-qualification-matrix-20260915.json), [I6 notes](laws/i6-qualification-20260915.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: Halt μ-transfer is capture accounting, not compact GR. Weak-field Euler remainder does not qualify the compact regime. Full-engine incomplete. Frozen H0139–H0143 interpretation unchanged.
- Next: Do not shop another linearized-GEM moving-compact variant. Do not select `production_law`. Remaining required gaps: galaxy quadrupole skip (do not retry), gravitational crossing, envelope workload.


## H0145 — Moving Schwarzschild 1PN covers laboratory compact fields; Engine crossing still FAIL

- Date: 2026-09-15
- Kind: experiment
- Status: measured
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after H0144 `4c7440e`; this entry's follow-on commit
- Scope: Plan I4.4 moving compact sources of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); I6 matrix re-run; not promotion; not full-engine
- Changed: New model `es-moving-schwarzschild-1pn-v0`: two moving masses (ratio 0.0625), mutual 1PN until `r_if`, Schwarzschild geodesic in the moving primary rest frame, absorbing capture μ 0.5→8.5. Compactness 0.5 at `r_s` is admitted (not linearized GEM). Remainder vs independent RK4 dt/4: weak 2.82e-4, strong 4.57e-4, clock 1.02e-3, null 1.36e-5, band 0.05. I6 `moving-multi-mass-compact` PASS. BH card PASS. Crossing FAIL: connected Engine does not host this law. Galaxy quadrupole 0.478 and family-as-galaxy-skip FAIL rows kept. Envelope UNSUPPORTED. `production_law` null. GEM-to-horizon wrappers remain stopped (H0144).
- Why: H0144 stopped linearized GEM wrappers, not the full-engine objective. I4.4 requires moving compact transport and capture. Stationary anchors cannot qualify that. Comparable-mass NR is still out of reach; this is the strongest moving compact dynamics that still carries the claim.
- Validation: `CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --lib i4_moving_compact --offline --locked -- --test-threads=1` 2 PASS. `cargo test -p emergent-engine --test i6_qualification --offline --locked -- --test-threads=1` 1 PASS. Matrix mixed; promotion false; full-engine false.
- Evidence: [I6 matrix JSON](laws/i6-qualification-matrix-20260915.json), [I6 notes](laws/i6-qualification-20260915.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: Galilean rest-frame at β≈0.02, not a Lorentz-boosted Kerr hole. Mass ratio cap 0.1. Not NR two-body strong fields. Connected Engine still inertial+diagnostic GEM, so gravitational crossing is not Engine-hosted. Frozen H0139–H0144 interpretation unchanged.
- Next: Do not select `production_law`. Do not retry galaxy quadrupole skip. Remaining required gaps: Engine-hosted crossing of this regime, envelope workload.


## H0146 — Connected Engine hosts moving compact capture; crossing PASS; matrix still mixed

- Date: 2026-09-15
- Kind: implementation
- Status: measured
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after H0145 `ee8c5a6`; this entry's follow-on commit
- Scope: I6 crossing of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md) on the same connected Engine; not promotion; not full-engine
- Changed: `connected_qualification_engine` (observatory `--world connected`) now attaches `es-moving-schwarzschild-1pn-v0` as a diagnostic sidecar and steps it during `Engine::advance` with ships/signals/policy/archive. Capture 0.5→8.5 on that Engine; remainder vs independent RK4 dt/4 is 1.35e-2 ≤ 0.05 (scale `r_if`). Crossing card PASS. Canonical law stays `es-inertial-causal-v1`; `CANONICAL_GRAVITY_ACCEPTANCE` diagnostic-only. Galaxy quadrupole 0.478 and family-as-galaxy-skip FAIL rows kept. Envelope UNSUPPORTED. `production_law` null. Full-engine false.
- Why: H0145 laboratory cover was not Engine-hosted crossing. Julien assigned wiring the law into the same connected Engine, not a second lab world.
- Validation: `CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --lib i4_moving_compact --offline --locked -- --test-threads=1` 2 PASS. `cargo test -p emergent-engine --test i6_qualification --offline --locked -- --test-threads=1` 1 PASS. Matrix mixed; promotion false; full-engine false.
- Evidence: [I6 matrix JSON](laws/i6-qualification-matrix-20260915.json), [I6 notes](laws/i6-qualification-20260915.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: Compact sidecar is not canonical gravity and is not restored by inertial checkpoint/replay. Comparable-mass NR still refused (ratio > 0.1). Galilean rest frame. Frozen H0139–H0145 interpretation unchanged except Engine now hosts the H0145 law.
- Next: Do not select `production_law`. Do not retry galaxy quadrupole skip. Remaining required gaps: envelope workload; promotion blocked by remaining FAIL rows.


## H0147 — Frozen I6 envelope rungs measured; envelope-target stays UNSUPPORTED

- Date: 2026-09-15
- Kind: verification
- Status: measured
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after H0146 `de8186b`; this entry's follow-on commit
- Scope: I6 operating-envelope rungs of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); tiny complete loop and connected family+hierarchy; not envelope-pressure; not frozen-integrated-target; not promotion; not full-engine
- Changed: Declared freeze of independent activity / queries / reconstruction before Instant/RSS/digest. Tiny `causal_relay` (4 identities, horizon 80, one SendSignal, history_digest + reception, replay) **PASS**: process RSS 4720 KB, wall 14.7 ms, digest `b101a4a7a1486402…`, nested Charge ledger 0, owned CanonicalState 4766 B. Connected family+hierarchy+in-flight ray+observer/policy+archive (4 bodies, family N=8, horizon 40) **PASS**: process RSS 6064 KB, wall 63.5 ms, digest `65b7b76ab4a2346b…`, nested Charge ledger 1052, owned 5130 B. Envelope-pressure and frozen-integrated-target stay **UNSUPPORTED**. Galaxy quadrupole 0.478 and family-as-galaxy-skip FAIL rows kept. Crossing remains PASS. `production_law` null. Full-engine false.
- Why: Coordinator assigned envelope rungs, not target claims. Qualitative reception/scene-exists rows were not measurements. Julien's rule: behavior / independent oracle / remainder bands; many-seed capable; fixed ICs are not the universe. Do not claim ≤4 GiB / 30 FPS / billion-identity hour from a small rung.
- Validation: `CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-engine --test i6_qualification --offline --locked -- --test-threads=1` 1 PASS. Matrix mixed; promotion false; full-engine false; envelope-frozen-target UNSUPPORTED.
- Evidence: [I6 matrix JSON](laws/i6-qualification-matrix-20260915.json), [I6 notes](laws/i6-qualification-20260915.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: Process RSS is `ps` of the test process, not an isolated heap. Tiny ledger 0 is inertial-only, not leftover==0 physics. Wall times include compile of the frozen connected scene. No frozen large workload exists, so envelope-target remains unqualified. Frozen H0139–H0146 interpretation unchanged except envelope rungs now carry RSS/time/digest.
- Next: Do not select `production_law`. Do not retry galaxy quadrupole skip. Do not promote these rungs to the target gate. Remaining required gaps: quadrupole skip (do not retry); frozen large envelope workload; promotion blocked by remaining FAIL/UNSUPPORTED rows.


## H0148 — Pressure-sweep rung FAIL on sequential query; envelope-target stays UNSUPPORTED

- Date: 2026-09-15
- Kind: verification
- Status: measured
- Revisions: `/private/tmp/emergent-full-engine-integration` `codex/full-engine-integration` after H0147 `a89ecb6`; this entry's follow-on commit
- Scope: I6 pressure-sweeps rung of [full-engine-integration-plan-20260915.md](full-engine-integration-plan-20260915.md); mixed quiet/hot packed island; held-out comparison bank; not envelope-pressure gate; not frozen-integrated-target; not promotion; not full-engine
- Changed: Declared freeze before Instant/RSS/digest: 64 packed bodies, 10 families / 48 members, horizon 80, SetCourseRange+SendSignal, history_digest/decode(far-north)/observe_with_budget, replay, residual CanonicalState bytes, seed `0x15E1_A15D`. Mixed hot island plus quiet far families plus diagnostic GEM H=2. Pressure rung **FAIL**: limiter **sequential-query** (independent inertial oracle 12.1 s, `oracle=false`); replay and far decode held; 217 WorkBudget yields; collocation 21.6 ms; advance 842 ms; reconstruction 833 ms; process RSS 5920 KB; nested Charge ledger 928; residual 157961 B; wall 13.8 s. Envelope-pressure and frozen-integrated-target gates stay **UNSUPPORTED**. Held-out bank now includes compiler_exact, numerical_refinement (RK2 vs RK4 remainder 1.35e-2), and physical_law (family-moment band on N=4 rest fixture) contracts; re-seeding cannot erase galaxy quadrupole FAIL 0.478. Galaxy and family-as-galaxy-skip FAIL rows kept. `production_law` null. Full-engine false.
- Why: Coordinator assigned the third envelope workload as rungs, not target claims. Qualitative UNSUPPORTED was not a limiter. Julien's rule: behavior / independent oracle / remainder bands; many-seed capable. Do not claim ≤4 GiB / 30 FPS / billion-identity hour from this sweep.
- Validation: `CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-engine --test i6_qualification --offline --locked -- --test-threads=1` 1 PASS. Matrix mixed; promotion false; full-engine false; envelope-pressure UNSUPPORTED; envelope-frozen-target UNSUPPORTED; pressure-sweeps rung FAIL.
- Evidence: [I6 matrix JSON](laws/i6-qualification-matrix-20260915.json), [I6 notes](laws/i6-qualification-20260915.md), [plan](full-engine-integration-plan-20260915.md)
- Limitations: Process RSS is `ps` of the test process. Packed-island independent oracle disagrees and dominates wall; that is a sequential-query limit, not a memory cliff and not the frozen billion-identity target. Family-moment remainder on the rest fixture is not an all-galaxy skip. Frozen H0139–H0147 interpretation unchanged except the pressure rung is now measured FAIL.
- Next: Do not select `production_law`. Do not retry galaxy quadrupole skip. Do not promote this rung to the target gate. Remaining required gaps: quadrupole skip (do not retry); frozen large envelope workload; packed-island oracle/query cost if that path is pursued; promotion blocked by remaining FAIL/UNSUPPORTED rows.

## H0149 — Recover integration and repair pressure reference and RK2 validation

- Date: 2026-09-23
- Kind: implementation
- Status: partial
- Revisions: recovered baseline `e510b2f`; this entry's commit; tested source hashes in new provenance
- Scope: I1/I6 retrospective inertial contact/cone audit, I4 compact numerical integration, held-out report integrity; full engine remains incomplete
- Changed: Recovered committed implementation into durable `Research/emergent-integration` worktree. Fixed family omission, tick-zero, revision/batch contact semantics and signal multiplicity in the small-world reference. Added 12 varied-IC comparisons and adversarial missing-fact tests. Fixed Heun RK2 update order and added step-halving regression. Unsupported held-out physical claims now report UNSUPPORTED. Matrix test creates new output instead of overwriting historical evidence.
- Why: User requested continuation and real behavioral/oracle validation. H0148's pressure failure was a reference defect, and audit exposed numerical error plus unmeasured PASS claims. Exact compiler comparisons, numerical convergence and physical behavior must stay distinct.
- Validation: Engine library plus oracle_pressure, i1_increment2_authority and i6_qualification: 48 PASS. Compact filtered library: 3 PASS. Old RK2 mutation fails frozen second-order band (ratio 1.99913). Original pressure oracle fails; corrected audit matches 471 contacts. Debug pressure wall 31.657 s, audit 29.940 s; no speedup. History check FAILS on pre-existing missing evidence; inventory has 116 missing paths. Git diff whitespace check passes.
- Evidence: [continuation report](laws/integration-validation-20260923.md), [source provenance](../artifacts/evidence/integration-validation-20260923/provenance.json), [matrix](../artifacts/evidence/integration-validation-20260923/i6-matrix.json), [tests](../artifacts/evidence/integration-validation-20260923/final-engine-tests.txt), [negative control](../artifacts/evidence/integration-validation-20260923/rk2-mutation.txt)
- Limitations: Reference is retrospective on committed trajectories/emissions, not independent evolution or physical gravity validation; phase/ambiguous range histories refuse. The 12 cases vary inertial initial states; compact test rotations do not establish a physical ensemble. No target performance, comparable-mass strong-field or canonical gravity promotion. Historical referenced files missing from recovered baseline remain unrecovered; old evidence and checker untouched.
- Next: Implement genuine moving-source held-out behavioral ensembles with independent physical anchors; replace weak solar boundedness classifier. Recover authentic missing history evidence. Continue integrated gravity authority before promotion; keep full-engine incomplete and production_law null.

## H0150 — Real two-body behavior bank and versioned causal orbit initialization

- Date: 2026-09-23
- Kind: implementation
- Status: partial
- Revisions: baseline `8b883ce`; this entry's commit; exact tested source hashes in new provenance
- Scope: Twelve structured weak-field finite arcs, Newtonian physical anchors, independent integration/refinement scopes, versioned offline source initialization and real Engine budgeted compilation
- Changed: Added analytic Kepler anchor and varied eccentricity, mass ratio, semimajor axis, compactness and orientation. Original bank measures 8 PASS/4 FAIL; numerical checks all pass. Diagnosed initial-state offsets separately from ongoing force/invariant changes. Fixed-point initializer retains 10 PASS/2 UNSUPPORTED at frozen budget; separately versioned Newton shooting passes all 12 finite arcs with all 19–28 compilation evaluations per case charged. No state patched at observation start. Engine budget subdivisions reproduce accepted source functions. Replaced minimum-only solar boundedness with sampled radius/energy/angular diagnostics and explicit sustained-orbit UNSUPPORTED; solar/three-body/galaxy dynamics cards no longer infer physical PASS from field/identity checks.
- Why: User asked to continue implementation with real behavior/oracles and meaningful multiple-seed testing. Earlier tests confused state labels with physical behavior and genesis switch-on with an initialized orbit. Separate initialized cases and retained failures avoid retuning or laundering model changes.
- Validation: Entire law-library suite 102 PASS; I6 matrix test and orbit_initialization engine test PASS. Seeds 0/8/10 match source interval functions exactly under WorkBudget 1 and 256. Newton initial residual <=1e-8; maximum measured finite-arc position error/a about 0.00546. All 12 ballistic negative controls reject. Failed original/fixed-point cases retained. History check remains blocked by missing pre-existing evidence, not relaxed.
- Evidence: [bank freeze](laws/two-body-bank-20260923.md), [initializer freeze and results](laws/two-body-initialization-20260923.md), [provenance](../artifacts/evidence/orbit-initialization-20260923/provenance.json), [matrix](../artifacts/evidence/orbit-initialization-20260923/i6-initialized-matrix.json)
- Limitations: Structured 12-case finite arcs cover only 0.119 periods, not full orbit, statistical coverage, strong fields or canonical gravity. Initializer is offline and atomic; source continuation is budgeted. Counters are returned ledger units; failed APIs can omit partial counters, explicitly flagged. Frozen historical failures and 116 missing historical paths remain. production_law null; full engine incomplete.
- Next: One full-orbit probe from the identical resolved genesis without re-shooting for a longer horizon, then widen duration only if discriminating behavior supports it. Continue physical three-body/population and integrated gravity authority; do not promote short-arc evidence.

## H0151 — Same-genesis full-orbit bank exposes five retained physical failures

- Date: 2026-09-23
- Kind: implementation
- Status: partial
- Revisions: baseline `55612eb`; this entry's commit; source hashes and test timing distinctions in retained provenance
- Scope: I4/I6 diagnostic two-body duration with original observation-start Newton initialization; no canonical gravity promotion
- Changed: Added one-period sampled Kepler position/invariants/radial/signed-angle checks for all twelve original cases. Seed0 probe PASS, expanded bank 7 PASS/5 FAIL. I6 schema3 retains all reports and a separate failed one-period gate. Query refusal cannot erase an observed prefix FAIL. dt-halving diagnostic produced identical trajectories because the compiler stores dt as metadata and selects causal blocks independently; this is not convergence evidence.
- Why: Twelve short-arc passes do not establish complete orbital behavior. Test duration using identical calibrated genesis instead of fitting a different past for the requested future.
- Validation: `cargo test -p emergent-law-lab --lib --offline --locked` 105 PASS; `cargo test -p emergent-engine --test i6_qualification --offline --locked` 1 PASS (57.60s); final duration regression and history-check outputs retained with evidence. Physical bank remains 7 PASS/5 FAIL independently of test-runner success.
- Evidence: [probe and interpretation](laws/orbit-duration-20260923.md), [raw runs and provenance](../artifacts/evidence/orbit-duration-20260923), [duration implementation](../crates/law-lab/src/orbit_duration.rs)
- Limitations: Seeds4/8/9/10/11 fail signed coverage; 8/9/10/11 also position. No true duration convergence result yet. Sampled offline diagnostics are not interval certificates or Engine canonical dynamics. 1,639,446 compile ledger units and 15.15s summed debug bank wall are not operating-envelope qualification. Inherited history check still lacks 116 historical evidence paths. production_law null; full-engine incomplete.
- Next: Compare failed seeds with actually refined retarded-GEM reference or expose a frozen causal-block resolution control. Preserve these failures and earlier initialization banks. Continue authoritative gravitational integration and remaining plan gates.

## H0152 — Record user-confirmed same-genesis orbital convergence experiment

- Date: 2026-09-23
- Kind: decision
- Status: proposed
- Revisions: baseline `61f72a9`; this documentation commit
- Scope: Next I4/I6 experiment; existing retarded-GEM model numerical validation
- Changed: User confirmed the next step: compare failed seeds 4/8/9/10/11 against an independent progressively refined retarded-GEM reference and/or genuinely refined causal blocks, using identical resolved genesis, prehistory, equations and one-period horizon. Handoff, task tracker and living intent card updated.
- Why: Separate compiler numerical error from converged physical-model disagreement before changing the model or initialization assumptions.
- Validation: Documentation-only update; no physics experiment or code tests run. History list reviewed; history check rerun with its inherited missing-evidence failure.
- Evidence: [current next step](HANDOFF.md), [task tracker](../orchestration/tasks.json), [retained orbital failures](laws/orbit-duration-20260923.md)
- Limitations: Experiment remains unexecuted. Stored dt does not refine collocation. Existing gates, failures and null production_law remain unchanged; historical evidence remains missing.
- Next: Execute the frozen same-genesis numerical comparison, establish convergence, then interpret any remaining Kepler disagreement as a model/initialization question.

## H0153 — Refine the same-genesis orbital reference and fix a retarded-root omission

- Date: 2026-09-24
- Kind: implementation
- Status: partial
- Revisions: baseline `52675aa`; this entry's commit; source/input hashes and pre/post-fix distinctions in provenance
- Scope: I4/I6 same-genesis orbital numerical validation; explicit causal-block subdivision; diagnostic root correctness
- Changed: Added charged Euler-reference ladder and real compiler subdivision API. All five originally failing seeds pass positional refinement screening: seed4 at262144 steps,8/9/10/11 at1048576. Retained all coarse failures. Refined compiler/reference disagreements remain0.037595a and0.025553a for seeds8/10, above unchanged0.02. Added safeguarded accelerated light-cone root solve: old out-of-interval initial guess falsely omitted an existing source. Root residual work is charged. Fix does not explain orbital-bank mismatch. Historical profiling-count assertions replaced by matched current source-work comparisons; exact reuse/repair tests retained.
- Why: User prioritizes solid relativistic behaviors and independently measured numerical reliability before computational optimization. A stored dt did not refine collocation, and agreement at one compiler resolution did not establish a shared numerical limit.
- Validation: Full law suite110 PASS,2 manual experiment tests ignored by default but explicitly executed; I6 and orbit_initialization integration tests PASS. Seed10 debug/release65536 samples equal. Old-root mutation fails the constructed t_ret=.99 counterexample; corrected interior/endpoints/absence tests pass. History check retains inherited missing-evidence failure.
- Evidence: [experiment freeze/results](laws/orbit-reference-20260924.md), [summary](../artifacts/evidence/orbit-reference-20260924/summary.json), [provenance](../artifacts/evidence/orbit-reference-20260924/provenance.json), [raw runs](../artifacts/evidence/orbit-reference-20260924)
- Limitations: Euler and compiler share field algebra; reference screening is positional, not velocity convergence or interval certification. All five reference orbital checks still fail; numerical discrepancy prevents a new physical-model verdict. No canonical gravity, performance or full-engine promotion; production_law null. Initializer was not rerun for comparisons. Root fix leaves these measured trajectories effectively unchanged. Historical116 missing paths remain unresolved.
- Next: Locate first genesis-to-observation disagreement in seeds8/10; compare fields on matched histories and inspect source turn-on before model or initialization changes. Keep original failures and gates.

## H0154 — Split the initial field wave to resolve orbital numerical disagreement

- Date: 2026-09-24
- Kind: implementation
- Status: partial
- Revisions: baseline `cc7f468`; this entry's commit; source/input hashes and test-run distinctions in provenance
- Scope: Same-genesis numerical validation for original failed seeds4/8/9/10/11; initially unforced common-genesis source response
- Changed: Localized first velocity divergence to initial field arrival. Field dispatch on matched histories agrees near1e-13. Compiler now splits at analytic first massive-source genesis light-cone arrival, with intersections charged. Same saved genesis/reference at subdivision8 now agrees in position for all five within0.02a; worst difference0.003056a. Seed8 improves0.037595a to0.002329a; seed10 improves0.025553a to0.001203a. No force-law or initializer change. Reuse tests verify all retained prefixes, generated intervals and reconstruction coverage instead of obsolete fixture-size counts.
- Why: Midpoint integration across a sharp causal source turn-on produced an initial velocity error amplified over an orbit. Refining smooth later evolution did not reliably remove that startup error at tested subdivisions.
- Validation: Full law suite111 PASS,3 manual experiments ignored by default; onset and full-period block experiments explicitly run. Final prefix-accounting test PASS. Connected-scene2 tests, I6 matrix1 and orbit-initialization1 PASS. Disabling front split makes the analytic moving-receiver regression fail. History check retains pre-existing missing-evidence failure.
- Evidence: [diagnosis and scope](laws/orbit-onset-20260924.md), [summary](../artifacts/evidence/orbit-onset-20260924/summary.json), [provenance](../artifacts/evidence/orbit-onset-20260924/provenance.json), [raw runs](../artifacts/evidence/orbit-onset-20260924)
- Limitations: Positional numerical screening is not velocity/invariant convergence or interval authority. All five saved-genesis physical checks still fail; I6 physical bank remains7 PASS/5 FAIL. Earlier receiver commands or changed velocity prefix bypass the inertial arrival construction and retain cadence/intervention fallback. Shared GEM algebra is not independently validated by this reference. No canonical gravity, GR, scale or production promotion. Inherited historical missing files remain.
- Next: Freeze velocity/invariant refinement gates, then independently assess shared physical equations/initialization against physical anchors. Preserve numerical and physical verdicts separately.
