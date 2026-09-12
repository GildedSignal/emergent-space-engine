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
