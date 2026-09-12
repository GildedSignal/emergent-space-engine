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
