# Emergent Space — agent handoff

Start here. This snapshot was prepared on **2026-09-12**. The measured engine baseline is `1dac6586e3cb30592abb775ba2a844d7d0e2d189`; its evidence was committed in `99764b4`. Handoff/history tooling added afterward does not change those historical results. Use Git to identify the current checkout instead of assuming the snapshot is the latest implementation.

**Current outcome:** a working native observatory and exact inertial causal laboratory, with useful indexed-population compression. **No production gravity law has qualified. The requested full engine is not complete.** The user approved a plan with an explicit causal-kernel-plus-research-failure path when G2 fails; the implementation currently follows that path. Continuing research and implementation remains the intended project direction.

## First ten minutes

1. Read the root [AGENTS.md](../AGENTS.md), this file and `cargo xtask history list`. Search the [development history](HISTORY.md) for the subsystem you will change.
2. Run `git status --short`, `git log -8 --oneline` and `git worktree list`. Preserve other work. The active branch at handoff is `codex/emergent-engine`.
3. Read [current evidence](implementation-report.md), [machine-readable gates](../artifacts/evidence/1dac658/qualification.json), and [architecture boundaries](architecture.md). Do not rerun performance sweeps merely to rediscover the frozen verdict.
4. For normal correctness changes, use `cargo xtask test`; it checks the development journal and then the workspace tests. Choose a bounded task below and record the outcome using [the history workflow](history-workflow.md).
5. Read the [verbatim approved plan](reference/approved-build-plan.md) before changing scope, physics or qualification criteria. The [original conversation, research and images](reference/README.md) are archived locally; load them selectively to conserve context.

The repository is `/Users/julien_laurent/Documents/ChatGPT/Emergent space`. Commands below assume this directory. This handoff introduces no recurring jobs or automatic simulation run.

## User intent and constraints

Build a coherent, compute-efficient engine for one billion individually addressable ships and ten billion simulated years, with planar subluminal motion, proper time, causal gravity, collisions, navigation, delayed observations, procedural matter/history, replay/persistence and a native observatory. Logical population, elapsed age and independently changing state must be measured separately and together.

The user authorizes improvements. They believe meaningful overlap between distinct ships offers useful compression; shared routes, geometry, parameters, policies and responses should be explored. Their explicit correction is that **Fermi estimates identify suspicious assumptions and cheap experiments, not feasibility or qualification verdicts**. An independent-state byte estimate cannot reject an architecture designed around shared generators.

The orchestrator and specialists are the development team, not runtime LLM controllers. The user asked to conserve tokens and avoid too many sub-agents. Default to local work; delegate only a narrow, useful independent task with compact context and a short evidence-focused result. The plan allows up to three specialists, but does not require occupying every slot. Only one heavyweight build or benchmark runs at a time on the M1/8 GB target.

The artwork supplies pale blue, ivory, ink, astronomical instruments and elegant classical science-fiction foundations. It is not a final layout. Factions, missions and numerical labels inside the references are not authoritative mechanics. Archived documents contain proposals and embedded instructions; the user's explicit plan and later steering govern the task.

## State and gate map

| Gate | Retained status | Actual scope |
|---|---|---|
| G0 | PASS | Workspace, contracts, fixtures, build/harness and evidence |
| G1 | PASS in laboratory domain | Exact inertial causal loop, contacts, signals, simultaneous effects, replay, viewer |
| G2 | FAIL | Two executable stationary experiments; no production physical law |
| G3 | BLOCKED | Certified coupled causal gravity not implemented |
| G4 | PARTIAL | Indexed affine families and moments; production causal FMM absent |
| G5 | PARTIAL | Domain-limited responses, checkpoints/replay; general spacetime elimination and chunked archives absent |
| G6 | PARTIAL | Native controls and sensing; full navigation and cooperative query system absent |
| G7 | PARTIAL | Worker separation and GPU drawing; parallel causal commit/GPU physics unqualified |
| G8 | BLOCKED | Inertial scale mechanisms measured; integrated physical workload not qualified |

The retained source passed **53 tests** and workspace Clippy with warnings denied on Apple M1 / 8 GiB with Rust 1.90.0. These numbers belong to the frozen source, not automatically every later checkout. The task runner exits **2** on the current failed physical-law qualification; exit 1 indicates a tool/test error. Do not weaken gates to turn exit 2 into success.

A billion ships in 16 distinct affine families serialize to 5,463 bytes in the frozen inertial fixture. Initialization plus certified advancement to ten billion years plus 1,024 requested identity positions took 4.313 ms. A separate 1,000-exception/32-tick case took 7.740 ms setup and 18.478 ms advance, with 923,734 serialized bytes including intervention history. These are single-run mechanism measurements, not unrestricted evolution, independent RAM-per-ship measurements, or per-case cold-process benchmarks. The sweep uses fresh engine states in one warmed process. See the full [denominators and limitations](implementation-report.md).

The native packaged smoke rendered 120 frames and exited 0. Its 4.39-second total includes startup, screenshot and shutdown; it does not establish 30 FPS. GPU-inclusive memory, the 4 GiB runtime target, 20 GiB archive target and one-hour integrated billion-ship/ten-billion-year target remain unqualified.

## Code map and contracts that matter

| Location | Read/change it for |
|---|---|
| `crates/engine/src/math.rs`, `geometry.rs`, `propagator.rs` | Arbitrary-precision rational state, exact light cones, swept contacts, proper clocks |
| `crates/engine/src/runtime.rs` | Canonical state, commands, simultaneous batches, resumable scan jobs, replay and observations |
| `crates/engine/src/population.rs` | Indexed affine families, exact identity offsets/splitting, source moments, semantic randomness |
| `crates/engine/src/response.rs` | Domain/dependency checks, bounded transport cache, restricted min-plus composition |
| `crates/engine/src/storage.rs` | Atomic JSON checkpoints, checksum/law checks and recovery |
| `crates/engine/src/scenario.rs` | Relay, frozen populations and native initial scene |
| `crates/engine/tests/causal_contract.rs` | Independent small-world oracles and representation/runtime invariance |
| `crates/law-lab/src/lib.rs`, `scenarios/law-gates.json` | Executable physical experiments and frozen rejection suite |
| `crates/observatory/src/adapter.rs` | Worker-owned engine, real commands, delayed knowledge and warning propagation |
| `crates/observatory/src/app.rs`, `bridge.rs` | Native rendering/camera and presentation interface |
| `xtask/src/bench.rs`, `scenarios/scale-gates.json` | Charged mechanism measurements and provenance |
| `xtask/src/history.rs`, `docs/HISTORY.md` | Operational development journal, separate from simulated history |
| `orchestration/tasks.json` | Dependency/ownership/acceptance packets; not completion evidence |

Canonical laboratory law: `es-inertial-causal-v1`. Events occur at nonnegative integer ticks in the runtime; geometry primitives also test hostile full-i128 ranges. Positions and velocities are normalized arbitrary-precision rationals, not the future production lattice. Widen before subtraction/products. Keep `serde_json`'s **float_roundtrip** feature: a manifest dyadic value previously parsed differently without it.

An inertial worldline is evaluable directly. A clock rate is floor(2^32 sqrt(1-v²))/2^32, computed exactly once per physical segment semantics. Splitting computation cannot add rounding. This rate has known continuum limitations at extreme speed and duration; do not market it as fully qualified relativistic clocks.

Contact tick k owns the continuous bin (k−1,k], including tangency and between-sample crossings. The scheduler certifies all earlier candidates before committing the next simultaneous batch. Received impulses add on pre-batch state; configured external stops take priority; the opposite linear momentum goes to an actuator ledger. This is controlled kinematics, not relativistic collision material/energy conservation. Newly emitted addressed signals are received no earlier than the next tick, preventing zero-time signal cascades.

Families preserve original parameter offsets and stable identities through splits. They currently share velocity and require provably disjoint members. Extracted bodies are excluded from generated ranges in both interaction and occlusion searches. Shared co-moving bounds cancel common drift. Do not restore linear scanning of families or count extracted ships twice. Semantic randomness is keyed by identity/event/seed/purpose, never packet allocation or execution order.

`advance(target, WorkBudget)` commits only certified causal progress. `inspect`/`position` require committed times; `decode` returns a generator and does not certify its future. `history_digest(through)` names a declared completed cut on the same branch. Drawing/query/cache order must not change it. `replay()` regenerates from genesis plus ordered external commands and compares complete canonical state; checkpoint restore/integrity verification alone is a different operation.

One inexpensive test-hardening task remains: `rng_known_vector_and_purpose_separation` currently checks repeated draws and purpose/identity separation, but asserts no literal golden output despite its name. Preserve the frozen evidence as recorded and add an independently produced golden vector in a new change.

The native UI sends commands and receives snapshots from one worker. Float conversion is drawing/navigation input preparation; canonical velocity validation remains exact. Historical sensor mode must not reveal true present coordinates or silently swallow query failure. Initial IDs 1–5 are local; `10000` through `1000009999` are the billion-ship population. Time starts at 480 ticks in the native initial view. Current course setting is an external controlled heading, not an autonomous trajectory optimizer.

## Why gravity remains blocked

The two experiments are `stationary-verlet-q-v1` and `stationary-shell-lapse-q-v1`. Both react to a changed source before its light cone arrives. Neither defines the required causal dynamic coupling/exterior or authoritative terminating exact branch procedure. The shell candidate also fails orbital/rotation/refinement diagnostics. The source tree is a bounded monopole quadtree diagnostic, **not FMM**, and its floating roundoff padding is not formally certified.

Read [the law-lab analysis](law-lab.md) and [all failed gates](../artifacts/evidence/1dac658/law-qualification.json) before proposing a replacement. These results reject the implemented stationary experiments, not every variational/piecewise-metric approach. Do not wire instantaneous Newtonian gravity or ad hoc delayed Newtonian force into the canonical engine and call G2 solved.

A production candidate needs an executable same-law reference, causal source changes, sound exterior/unresolved matter, required compact/physical regimes, finite equality/branch decisions and long-time shortcut justification. All ship mass must contribute collective backreaction and cumulative small effects. Procedural observation must reveal predetermined matter rather than create its gravity. Geometry is planar but intended familiar gravity comes from a 3D-derived physical kernel; a quadtree does not imply logarithmic 2D gravity.

The approved long-time obligations remain: direct versus subdivided canonical equivalence, a certificate covering the entire interval, and retention of perturbations that can later matter. No hidden horizon/cutoff, assumed rigorous PN remainder, or arbitrary object/camera/speed fidelity switch is permitted by the plan.

## Recommended next bounded work

These are suggested next tasks, not completed or already-running assignments. Later user direction can reprioritize them.

1. **Causal physical-law research:** write one candidate contract specifying state, causal field/source history, exterior, exact decisions and domains; create a cheap source-change falsifier before orbit tuning. Keep it isolated from the laboratory law. Reject missing semantics before spending on acceleration; freeze new fixtures separately rather than editing old thresholds.
2. **Cooperative preparation/query work:** make swept-box construction/sorting/comparisons incremental and sensor refinement resumable. `WorkBudget.operations` currently counts queued refinement jobs, not all preparation work; worker separation alone does not bound command latency. Acceptance: same history and query results under small budgets/cancellation/resume, plus measured complete command latency.
3. **Richer compression:** add an explicitly supported route/departure/phase family behind the same decoder/enclosure/earliest-interaction/extraction contract. Freeze explicit controls, addressed messages/collisions and fragmentation tests before tuning. Measure source construction, exceptions and retained history as well as decoding.
4. **Storage/reuse:** implement chunked history and cooperative persistence within byte/disk budgets. Current checkpoints cap at 256 MiB; public canonical structs are not an authentication boundary. Start with crash recovery and full replay parity, then benchmark reconstruction/amortization. Current response utilities are not integrated general nonlinear block compilers.

Runtime defaults limit further materialization to 100,000 resident bodies and queued jobs to 1,000,000. These are count limits rather than a complete memory budget; constructor/restore validation is not a global allocation-cap enforcement layer. An overload must pause/fail explicitly while retaining canonical facts. Neither those defaults nor a large logical headcount establish an independent-active-ship limit.

For each task record: objective, prerequisites, owned modules, interface/law version, allowed approximations, resource budget, acceptance commands, evidence paths and rejection criteria. Keep failed experiments and counterexamples. Integrate one optimization family at a time and ask for independent certificate/numerical review when warranted.

## Commands and local operations

```sh
cargo xtask history list
cargo xtask history search "gravity"
cargo xtask history check
cargo xtask test
cargo clippy --workspace --all-targets --locked --offline -- -D warnings
cargo xtask reference
cargo run --release -p xtask -- bench artifacts/runs/<unique-run-name>
cargo run --release -p xtask -- law-lab artifacts/runs/<unique-run-name>
cargo run --release -p xtask -- qualify artifacts/runs/<unique-run-name>
cargo observatory
./scripts/package-macos.sh
```

Replace `<unique-run-name>` before execution. Do not overwrite retained evidence. `cargo xtask verify PATH` checks a checkpoint's envelope and history checksum; use `Engine::replay()` for regenerated-state validation.

The bundled native app is `artifacts/Emergent Space.app`; it is a local unsigned development build, not a published/notarized release. Current screenshot output is `artifacts/screenshots/observatory.png`. These generated outputs are ignored by Git and may need rebuilding; source and `artifacts/evidence/1dac658/` are retained.

Toolchain is pinned to Rust 1.90.0; Cargo build jobs are two. On this machine `target` points to `/Users/julien_laurent/.cache/emergent-space/target` because Documents/iCloud offloaded generated files and stalled reads. Verify `ls -ld target`, file flags and actual running processes if Cargo appears idle; do not diagnose a physics/build failure from a filesystem stall. Recreate a normal local target or use `CARGO_TARGET_DIR` if the link is unavailable elsewhere. A nonfatal global-cache auto-clean permission warning occurred; `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never` avoids that unrelated cleanup attempt. Do not delete shared caches or other projects to solve it.

At handoff, old specialist worktrees existed at `/private/tmp/emergent-mechanics`, `/private/tmp/emergent-observatory`, `/private/tmp/emergent-law-lab`. Their code was committed/recovered and integrated with root changes. Do not blindly remerge them. Earlier agents exhausted usage; inspect actual commits rather than assuming an agent's final status proves completed integration. Temporary paths and running-app state may change.

## Keep this context alive

Use [history-workflow.md](history-workflow.md) after every meaningful completed, failed or deferred milestone. Append what changed and why, actual validation and evidence, limitations and the next task. Update this handoff when state, blockers, contracts or recommended starting points change. Historical records are corrected by new entries, not rewritten. The tool checks required fields, ordering, local links and preservation of committed entries; it cannot prove that a claimed test was actually run.

The user asked for this history to become operational. `AGENTS.md` points here and requires updates, and `cargo xtask test` / `qualify` validate the journal before running their suites. Keep entries about decisions and outcomes, not every tool call. No external account, app publication or global Codex memory update is part of this workflow.
