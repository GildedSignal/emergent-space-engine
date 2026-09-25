# Emergent Space — agent handoff

**Current heading — 23 September 2026:** Continue the full integration plan. Recovered committed Cursor implementation `e510b2f` into durable worktree `/Users/julien_laurent/Research/emergent-integration`, branch `codex/integration-continuation-20260923`; temporary worktree files had disappeared. H0149 corrects the pressure oracle and RK2 integration, adds adversarial/multiple-IC tests, and removes unsupported held-out PASS claims. Full engine remains incomplete; `production_law` remains null. The sections below H0149 describe the retained September 15 snapshot unless explicitly superseded.

## Current plan (25 September 2026, after H0160)

The agreed direction is [work-allocation-principles.md](work-allocation-principles.md), with the GPU path on Metal. Build order, each step gated by the whole ladder with no regressions:
0. Commit pending work (with Julien's OK) and recover authentic missing evidence where possible.
1. Local event core in integer lattices, single core.
2. Bounded units, time-boxed frames and per-region slack.
3. Forecasts and the least-slack queue.
4. Performance and efficiency cores.
5. Metal chronon mode, with exact integer AMX/GPU slices.
6. Speculation (Neural Engine targeting) and recompression.
7. Gravity field certificates.

Parallel design threads: the aggregate combat law, the player's influence and input design, share codes, and ladder v5.

Status (25 September 2026, 23:30, H0161–H0163). Nothing is committed; step 0 still waits for Julien's OK.
- **Contract:** `crates/lattice` (law, CPU chronon reference, digests, `Stepper`) equals the independent gas reference.
- **Ladder:** [v5](../scenarios/scale-ladder-v5.json) is frozen; run it with `cargo run --release -p xtask -- ladder5 <dir> [track] --modes=chronon,event`.
- **Step 1 (event core, `crates/lattice-event`):** passes invariance, cost-per-event and useful-work gates. Its smooth gate fails; round 2 is in progress.
- **Step 5 (`crates/lattice-metal`) and steps 2–4 (`crates/allocator`):** being built by specialists (interrupted once by an API rate limit, resumed 23:10). New target from Julien: the gas at 1M ships must be trivial.
- **Relativistic bounce:** `crates/lattice/src/relativity.rs` is tested but not yet wired. Next: `World.law` and `Body.carry` once the specialists finish, then ladder v6.
- **Whole computer:** design §4b has the tier rule and silicon table, with the HEVC sensor measured.

## Current continuation — H0159 (25 September 2026)

Read [the work-allocation design](work-allocation-design.md) (proposed, awaiting Julien): integer lattices, a local event core, dense chronon mode on the GPU, light-cone deadlines, and frames that never block. An opt-in elastic lattice law (`Engine::with_elastic`, `Body::bounce`) now exists and equals an independent integer reference simulator exactly. Its energy error stays bounded (±0.11% over 1.3M collisions on the reference). The engine runs the gas about 70× slower than naive stepping. Ladder v4 adds the gas tracks C2, X5 and X6 ([test ladder](test-ladder.md)). Next: build the local event core.

## Current continuation — H0158 (25 September 2026)

Quick scale-ladder climb: `cargo run --release -p xtask -- ladder <out-dir>`, about 1 minute; add `--full` for qualification ([test ladder](test-ladder.md)). Every rung now reports frame p95/p99/max at the observatory's 24-operation budget and cores used. The engine uses one core of eight. Worst frames reach 138 ms, and dense scenes need thousands of frames per simulated tick. The resident-ship cap is now derived from the 4 GiB memory budget (about 1.4M ships). Approved next work, in order: an elastic bounce law (walls, momentum-exact rounded velocities, energy residual carry, mass-aware impulses) with a trapped-gas track; a spatial index over short time windows; bounded operations and time-boxed frames; and a multi-core compute-allocation scheduler.

## Current continuation — H0157 (25 September 2026)

Scale ladder v1 is frozen ([manifest](../scenarios/scale-ladder-v1.json)) and climbed with `cargo run --release -p xtask -- ladder <out-dir> [track]`; status per track is in the [test ladder](test-ladder.md). The chaotic stop-cascade track found two canonical-engine correctness bugs at 64 bodies. The results depended on the slice budget and disagreed with the audit. Both are fixed with mutation-checked [regression tests](../crates/engine/tests/contact_cascade.rs):
- A stop on a resting body is now a no-op.
- Repairs of changed bodies now finish before the next commit.

114 engine tests pass. The remaining limiters are structural: per-event repair compares every box, single-axis sweep grows N^1.5 to N², boxes are swept over the whole horizon, family near misses are bisected down to members, and charged operations are not bounded work (slices up to 7.9 s). Next step proposed and awaiting Julien: an incremental spatial index over bounded time slabs, measured on the same rungs. Orbit refinement work of 25 September is still uncommitted and unjournaled.

## Current continuation — H0156 (25 September 2026)

New repo rule from Julien: test like a Spartan trains, harder than the war. Every capability gets a [test ladder](test-ladder.md) of frozen rungs, each ~10× harder, climbed until one fails, with both isolated extremes and chaotic goal-scale scenes. The population benchmark (cost independent of ship count and age) is a control: every group shared one velocity. With any relative motion the collision search compares every pair of groups (32,640 of 32,640 at 256 groups, still 5–11 ms); the sweep axis is chosen by centre spread, which drift inflates along the lanes ([probe](../artifacts/evidence/scale-ladder-v1-20260925/relative-motion-probe/README.md)). 112 engine tests pass in release.

The 25 September [orbit refinement results](laws/orbit-refinement-20260924.md) are recorded late as H0164. All five original seeds now pass numerical screening; GEM-v0 still fails all five physically. The shortfall scales linearly with field strength at 8–15× the relativistic scale. The H0155 next action is done. The next step awaits Julien's choice between the scale ladder (freeze first rungs, then fix or replace the single-axis sweep) and a one-geometry gravity contract.

## Current continuation — H0155 (24 September 2026)

The [state-convergence audit](laws/orbit-state-convergence-20260924.md) now checks paired position, velocity, Newtonian energy and signed angular momentum, with strict provenance and invalid-data rejection. On saved Euler/block runs: seed4 passes all four; seeds8/9/10/11 fail velocity-reference resolution (finest changes0.00826–0.01072 versus0.005). Their energy/angular-momentum screens and comparisons pass. Compiler velocity differences below0.02 cannot qualify against insufficient references. Retrospective screen, not held-out evidence. No new evolution or physical-model changes; physical bank remains7 PASS/5 FAIL and production_law null.

115 law tests and five CLI rejection controls pass. Next refine Euler beyond1048576 steps on those four same geneses; do not weaken0.005 or infer a compiler/model defect from reference insufficiency. Charge additional rungs. If reference lookup cost blocks refinement, validate any acceleration against exhaustive history lookup first. Then independently audit equations/initialization. Historical evidence-path failure persists. This supersedes the H0154 next action.

## Current continuation — H0154 (24 September 2026)

The [genesis-onset diagnosis](laws/orbit-onset-20260924.md) resolves the measured positional discrepancy: midpoint blocks straddled the first incoming field wave. Added an analytic first massive-source genesis-light arrival knot for initially unforced, common-genesis receivers. Same-history field dispatch agrees near1e-13. With identical saved geneses and Euler references, all five cases now satisfy the existing0.02a numerical agreement band at subdivision8; worst difference0.003056a. Original full-orbit physical bank remains7 PASS/5 FAIL. No force-law or initializer change was used in this comparison.

111 law tests, final prefix-accounting regression and4 engine integration checks pass; disabling the boundary fails its regression. Prefix tests check actual retained functions and generated work, not historical counts; reconstruction also includes compact decoding. See retained failed intermediate assertions. Earlier receiver commands/changed velocity prefixes use existing cadence fallback; their precise front tracking is not qualified. Canonical gravity remains diagnostic-only, production_law null. History check still has inherited missing evidence.

Next establish velocity/invariant convergence with frozen gates, then audit shared GEM equations and initialization assumptions against independent physical anchors. Position agreement alone does not qualify those quantities or GR. The H0153 localization task below is superseded by this result.

## Current continuation — H0153 (24 September 2026)

The [same-genesis numerical experiment](laws/orbit-reference-20260924.md) is implemented and measured. All five failed seeds pass the Euler positional refinement screen (seed4 at262144 steps; others at1048576), yet retain orbital behavior failures. Real causal-block subdivisions1/2/4/8 are now available through an explicit laboratory API. Refined compiler/reference disagreement exceeds0.02a for seeds8/10, so numerical validation remains incomplete. A constructed accelerated light-cone root omission is fixed and mutation-tested, but it does not explain these orbital discrepancies. 110 law tests and two engine integration tests pass. New matrix/evidence remain separate from frozen results; production_law null.

Next isolate the FIRST disagreement during genesis-to-observation for seeds8/10, including velocity and field evaluations on matched source histories and source turn-on handling. Keep saved genesis and physical gates fixed. Do not infer a physical-model failure or re-shoot away the mismatch. The next-step entries below are historical and superseded by this measured result. History check still fails on inherited missing evidence.

## User-confirmed next step — H0152

Numerically validate failing orbital seeds 4, 8, 9, 10 and 11 under the existing retarded-GEM model. Freeze the exact resolved genesis, prehistory, equations and one-period horizon. Compare against an independent retarded-GEM reference at progressively finer resolution and/or genuinely refine the compiler causal blocks; stored dt is not a resolution control. Retain Kepler comparisons, all existing failures and frozen thresholds. Establish numerical convergence before attributing the discrepancy to the physical model or reconsidering initialization assumptions. This is the next experiment, not an executed result.

## Current continuation — H0151

The [one-period bank](laws/orbit-duration-20260923.md) extends the same short-horizon initialized geneses: **7 PASS / 5 FAIL**. Seeds 4/8/9/10/11 fail angular coverage; 8/9/10/11 also fail position. The I6 schema-3 matrix now retains this separate failed gate. Halving supplied dt is ineffective because collocation ignores that metadata for interval selection; it is not a convergence result. Next compare failing cases against an actually refined retarded-GEM reference or expose and freeze real causal-block refinement before blaming the model. Full-engine remains incomplete and production_law null. H0150's next-probe instruction below is superseded.

## Current continuation — H0150

The [versioned initializer report](laws/two-body-initialization-20260923.md) supersedes H0149's missing two-body bank: actual varied finite arcs now exist. Original initialization is 8 PASS/4 FAIL; fixed-point is 10 PASS/2 UNSUPPORTED; separately charged Newton is 12 PASS. All are retained in the new I6 matrix. 102 law tests and two engine integration tests pass; source interval functions survive budgets 1/256 on seeds 0/8/10. Solar/three-body/galaxy dynamics remain unsupported; no full orbit or canonical gravity promotion. Next run the [frozen one-period probe](laws/orbit-duration-20260923.md) with the SAME resolved genesis, not a horizon-specific reinitialization. History check still fails on inherited missing evidence.

## Current continuation — H0149

- Start in the durable worktree above. The original Documents checkout remains dirty and untouched. The recovered [plan](full-engine-integration-plan-20260915.md) is unchanged.
- Read [validation continuation](laws/integration-validation-20260923.md) and its new matrix/evidence. The old September 15 matrix stays immutable.
- Pressure correctness now matches all 471 contact facts, including family identities and revision changes. The independent predicate audit is retrospective on committed trajectories/emissions, not independent evolution; it cannot detect missing emission generation or certify gravity. Phase families and ambiguous simultaneous range histories refuse; identity/work caps fail explicitly.
- RK2 now passes second-order convergence against refined RK4. The old update ordering fails the same frozen test. This checks numerical integration under shared equations, not independent physical validity.
- Three formerly unsupported held-out behaviors now honestly report UNSUPPORTED. Merely varying a seed label or rotating a fixture is not a dynamical seed bank. The 12 varied inertial IC cases are compiler/contact validation only.
- Next physics work: replace held-out placeholders with actual moving-source behavioral ensembles and independent magnitude/physical anchors; fix the weak solar boundedness classifier. I1 gravity event authority still needs an integrated path, and I4 moving comparable-mass strong fields remain unsupported. Do not retry rejected galaxy quadrupole or promote a pressure correctness rung to target performance.
- Continuity blocker inherited from `e510b2f`: history check fails on missing historical referenced files (first `crates/law-lab/src/causal_kernel.rs`). A complete missing-path inventory is retained. Recover authentic evidence from backups; do not fabricate files or relax the checker.

## First ten minutes

1. Read the heading-check skill and living card at `~/.cursor/skills/heading-check/cards/emergent-space.md`, then preflight. Journal and integration worktree now live at `/Users/julien_laurent/Research/emergent-integration`; `/private/tmp/emergent-g2-law/docs` contains compatibility links.
2. Read [the integration plan](full-engine-integration-plan-20260915.md), especially Evidence, the four initial issues, and I0/I1. Run `cargo xtask history list` and search relevant entries. H0124 closed the previous prompt's assigned laboratory exits; I0 reproduced repair completeness and nested accounting on the clean worktree.
3. Inspect `git status --short`, `git log -8 --oneline`, and `git worktree list`. Do not merge cumulative packet branches wholesale or delete original worktrees.
4. I3 domain-exited (H0136). I4 family GEM KEEP (H0140). I5 CPU-only (H0141). I6 matrix run (H0142) then 1PN (H0143), GEM-to-horizon wrappers stopped (H0144), moving Schwarzschild 1PN laboratory PASS (H0145), Engine-hosted crossing PASS (H0146), envelope rungs measured (H0147), pressure sweep measured FAIL (H0148). Do not mint global `CANONICAL_GRAVITY_ACCEPTANCE`. Do not select `production_law`. Full-engine incomplete.
5. Read hypothesis notes when selecting a discriminating experiment. They are candidates, not prescriptions. Keep a plan change separate from a measured engine capability.

## Current capabilities and boundaries

- **I6 matrix (this worktree):** Envelope rungs: tiny-complete-loop **PASS**; connected-family-hierarchy **PASS**; pressure-sweeps **FAIL** (limiter sequential-query: independent inertial oracle 12.1 s and mismatched; RSS 5920 KB, wall 13.8 s, nested Charge 928, residual 158 KB; 217 yield pauses). Envelope-pressure / frozen-target still **UNSUPPORTED**. Held-out bank has compiler_exact, numerical_refinement, and physical_law contracts; re-seeding does not erase galaxy FAIL. Crossing **PASS**. Galaxy quadrupole, family-as-galaxy-skip, promotion still FAIL. Full-engine **false**. `production_law` **null**. [I6 matrix JSON](laws/i6-qualification-matrix-20260915.json), [I6 notes](laws/i6-qualification-20260915.md).
- **I5 CPU-only (this worktree):** Knowledge queries use a derived per-observer arrival index, not a full-history event scan. Equal `history_digest` and received signals. Cold 4.19 ms / warm 0.57 ms; process RSS 5216 KB; owned state 4566 B; GPU none. Lazy pair inverse. [I5 surviving](laws/i5-surviving-work-20260915.md).
- **I4 (this worktree):** Six-card crossing on one engine with solar GEM genesis. Galaxy: direct small-world GEM sums admitted; retarded quadrupole REJECT 0.478>0.05. Affine family moments KEEP as GEM sources (remainder 0, extract 127395 vs moment 1906); identities retained. BH: `es-schwarzschild-gem-interface-v0` clocks/deflection match; accel PN jump 0.10; moving multi-mass refused. Domain-local GEM field bound on solar interior unchanged. Engine canonical events stay inertial. [I4 family GEM](laws/i4-family-gem-20260915.md), [I4 six-card](laws/i4-six-card-crossing-20260915.md), [I4 GEM authority](laws/i4-gem-authority-20260915.md).
- **I3 domain exit:** Admitted: quiet kernel H=4..12, weak-kick resume H=8, H≤3 collocation vs Euler, prefix-repair, lazy inverse. Failure: Kepler ansatze, PERIOD, compact-after-the-fact, Schur tide, population-solved, strong kicks (resume Δx=0.216, patch Δx=0.218), close-entrant recouple. [I3 domain exit](laws/i3-domain-exit-20260915.md), [I3 amort/kick](laws/i3-kernel-amort-kick-evidence-20260915.md).
- **I2 composition:** One scene joins a massive affine family to the I1 hierarchy while a ray is in flight. Extraction, exact affine re-merge, range broadcast receptions, unequal certified cuts (now via `advance_region`), incremental archive seal/eviction/cold observation, restore/replay, collective mass, burst recovery and resident-history bytes are evidenced. Policy fires once. [I2 evidence](laws/i2-composition-evidence-20260915.md). Frozen H0130 leftovers about the one-clock overlay are closed by H0131; do not rewrite that file.
- **I1 increment 2:** Exact inertial contact/light-cone oracle matches compiled events on the connected scene. GEM 16-sample enclosure is not interval-wide and does not authorize events. Units/epoch/dt are separately versioned from `es-inertial-causal-v1`. [I1 increment 2 evidence](laws/i1-increment2-evidence-20260915.md).
- **I1 increment 1 (this worktree):** `Engine::advance` polls coupled collocation/residual/pair-inverse/enclosure/repair jobs with `WorkBudget`. Headless connected scene binds ship/ray/clock/contact to interval functions, received-knowledge course change, in-flight signal checkpoint, pause/resume, query order, cache clear, replay. `CANONICAL_GRAVITY_ACCEPTANCE = diagnostic-only`. Compact sidecar skipped on the diagnostic seal. [I1 notes](laws/i1-contract-notes-20260915.md).
- **I0 (this worktree):** Selected inertial foundation + coupled compiler; Packet 6 policy/archive types without `truncated_admission`. `repair_from_committed` continues with the complete ordered input history. `Charge` nested ledger records enclosure genesis/Picard as `OfflineAudit`. Source ops, wall-time and pair-inverse bytes are distinct. [I0 report](laws/i0-full-cost-report-20260915.md).
- **H0100–H0124:** Historical overlay `/private/tmp/emergent-coupled-response`. [H0124 evidence](laws/coupled-prompt-completion-evidence-20260915.md). Counts **1188 vs 1675** and **1126 vs 1722** still pass in historical scope on the I0 worktree.
- **Certificate authority:** Sampled f64 `certified: true` remains diagnostic. [I1 notes](laws/i1-contract-notes-20260915.md).
- **Dense setup:** Quiet pair `store_pair_inverse` still grows with interval-function count when stored (H=3 n=20 / ~3 kB; H=6 n=44 / 18125 B in I3 nested bytes). Lazy compile skips that LU until `ensure_pair_inverse`.
- **Default/canonical law:** `es-inertial-causal-v1`; `production_law` remains null. H0052/H0054 and `1dac658` unchanged.
- **Physics still missing:** Comparable-mass strong-field NR (ratio > 0.1 inside `r_if`). Compact host is diagnostic, not canonical gravity. Galaxy quadrupole skip (direct sums admitted). Family-moment N=4 is not an all-galaxy skip. Envelope targets (≤4 GiB / 30 FPS / billion-identity hour) unqualified — tiny/connected/pressure rungs are not that target. Packed-island independent oracle is a sequential-query limit and a FAIL, not a target pass. Combined simulation+rendering unpublished. `production_law` null.

## Direction, behavior and targets

One causal response/commit/query/history contract should support different representations for bodies, fleets and celestial systems. The first complete scene joins moving massive sources, shared geometry, a ship, ray, clock/contact, received-message policy, intervention, feedback, repair and save/reconstruction. Then join families, unequal causal cuts and selective history. Optimize actual remaining work under that composition.

The [six-card contract](laws/litmus-gallery-contract-20260914.md) is the visual instrument: fast ships/light/twins; solar hierarchy; three bodies; galaxy-like populations; black-hole/light/clock; fleet/asteroid/causal intervention, plus their crossing. Preserve qualitative look-for cues with physical magnitude anchors. Compiler changes preserve canonical facts; model/generator changes use their separate comparison rules. Never select seeds to erase a failure. Unconfirmed magnitude preferences remain visible.

Targets remain M1/8 GB, ≤4 GiB total runtime including GPU once, ≤20 GiB archive, 30 FPS at 1080p, ≤5 ms cooperative-yield target and a cold billion-identity/ten-billion-year workload within one hour including final verification. These are unqualified targets. Freeze independently changing state, interactions, queries and historical information alongside headcount and age. Development agents are the programmers, not runtime LLM factions.

Research context includes [entropy hypotheses](compiler-entropy-deferred-20260914.md), [architecture hypotheses](compiler-architecture-remainder-deferred-20260914.md), original research and additional related conversations cited in the plan. Julien explicitly clarified these are hypotheses to test. Their earlier turn-only deferrals are historical. Unappended draft H0125/H0126/H0127 labels are stale placeholders; regenerate the next history ID if any draft becomes an actual milestone. Do not append dumps merely to clear placeholders.

## Historical baseline contracts

The following code map describes the existing inertial foundation. I1/I2 deliberately extend its integration boundary; statements about current limitations are not prohibitions on that planned work.

## Code map and contracts that matter

| Location | Read/change it for |
|---|---|
| `crates/engine/src/math.rs`, `geometry.rs`, `propagator.rs` | Arbitrary-precision rational state, exact light cones, swept contacts, proper clocks |
| `crates/engine/src/runtime.rs` | Spacetime compiler: commands, scheduled/scripted IR, simultaneous batches, resumable charged scan construction, incremental SAP, overlap certificates, causal-component grouping, guarded family/IR traces, resumable sensor/occlusion queries, replay |
| `crates/engine/src/population.rs` | Indexed affine and phase/departure families, exact identity offsets/splitting, source moments, semantic randomness |
| `crates/engine/src/response.rs` | Domain/dependency checks, bounded transport cache, restricted min-plus composition |
| `crates/engine/src/storage.rs` | Atomic JSON checkpoints, checksum/law checks and recovery |
| `crates/engine/src/scenario.rs` | Relay, packed-overlap / war-island, frozen populations and native initial scene |
| `crates/engine/tests/causal_contract.rs` | Independent small-world oracles and representation/runtime invariance |
| `crates/law-lab/src/lib.rs`, `causal_kernel.rs`, `coupled.rs`, `compact.rs`, `exact_branch.rs`, `schwarzschild.rs`, `tiny_causal.rs`, `evolving_patch.rs`, `compiled_spacetime.rs`, `scenarios/law-gates.json`, `docs/laws/causal-retarded-gem-v0.md`, `docs/laws/evolving-spacetime-patch-v0.md`, `docs/laws/causal-compiled-spacetime-v1.md` | Executable physical experiments; isolated research kernels remain FAIL; G2 candidate `es-causal-compiled-spacetime-v1` |
| `crates/observatory/src/adapter.rs` | Worker-owned worlds: laboratory `advance_patch` (default) and the inertial engine; real commands, delayed knowledge and warning propagation |
| `crates/observatory/src/app.rs`, `bridge.rs` | Native rendering/camera and presentation interface |
| `xtask/src/bench.rs`, `scenarios/scale-gates.json` | Charged mechanism measurements and provenance |
| `xtask/src/history.rs`, `docs/HISTORY.md` | Operational development journal, separate from simulated history |
| `orchestration/tasks.json` | Dependency/ownership/acceptance packets; not completion evidence |

Canonical laboratory law: `es-inertial-causal-v1`. Events occur at nonnegative integer ticks in the runtime; geometry primitives also test hostile full-i128 ranges. Positions and velocities are normalized arbitrary-precision rationals, not the future production lattice. Widen before subtraction/products. Keep `serde_json`'s **float_roundtrip** feature: a manifest dyadic value previously parsed differently without it.

An inertial worldline is evaluable directly. A clock rate is floor(2^32 sqrt(1-v²))/2^32, computed exactly once per physical segment semantics. Splitting computation cannot add rounding. This rate has known continuum limitations at extreme speed and duration; do not market it as fully qualified relativistic clocks.

Contact tick k owns the continuous bin (k−1,k], including tangency and between-sample crossings. The scheduler certifies all earlier candidates before committing the next simultaneous batch. Received impulses add on pre-batch state; configured external stops take priority; the opposite linear momentum goes to an actuator ledger. This is controlled kinematics, not relativistic collision material/energy conservation. Newly emitted addressed signals are received no earlier than the next tick, preventing zero-time signal cascades.

Families preserve original parameter offsets and stable identities through splits. Affine families share velocity and require provably disjoint members. Phase/departure families share a route generator, a staggered departure sequence and a stable identity range; members need not share velocity. Extracted bodies are excluded from generated ranges in both interaction and occlusion searches. Shared co-moving bounds cancel common drift only when every family shares one velocity; mixed-velocity or phase families use a per-item worldtube in a shared lab or per-family frame. Do not restore linear scanning of families or count extracted ships twice. Semantic randomness is keyed by identity/event/seed/purpose, never packet allocation or execution order. A family member is extracted only when its future generator changes; `FamilyPhaseBurn` updates a phase-aligned partition in place.

`advance(target, WorkBudget)` commits only certified causal progress. The budget charges box construction, family-range subtraction, a resumable stable merge, active-list expiry, AABB compares, grouping, frontier enqueue, commit collect/accumulate/validate, candidate/heap reduction and refinement jobs; construction is resumable ([H0028](HISTORY.md)). After a burn/contact the co-moving SAP rebuilds selected boxes instead of always rebuilding the scan; current retesting still scans every box, with repeated linear lookup, so neighbor-local complexity is not established ([H0025](HISTORY.md)). Quiet commits keep certified overlap pairs and already-discovered later candidates; only dirty or uncertified pairs are re-enqueued. `observe_with_budget` is a WorkBudget-charged sensor continuation; incomplete queries are pending/warning, never a silent empty sky, and do not mutate `history_digest`. `inspect`/`position` require committed times; `decode` returns a generator and does not certify its future. `history_digest(through)` names a declared completed cut on the same branch. Drawing/query/cache order must not change it. `replay()` regenerates from genesis plus ordered external commands and compares complete canonical state; checkpoint restore/integrity verification alone is a different operation.

A later inexpensive audit remains: `rng_known_vector_and_purpose_separation` currently checks repeated draws and purpose/identity separation, but asserts no literal golden output despite its name. Preserve the frozen evidence as recorded and add an independently produced golden vector in a later change; it is not the next compiler task.

The native UI sends commands and receives snapshots from one worker. Float conversion is drawing/navigation input preparation; canonical velocity validation remains exact. Historical sensor mode must not reveal true present coordinates or silently swallow query failure. Initial IDs 1–5 are local; `10000` through `1000009999` are the billion-ship population. Time starts at 480 ticks in the native initial view. Current course setting is an external controlled heading, not an autonomous trajectory optimizer. HEAD also compiles `scripted-interaction-v1` IR: `Command::SetCourse`, `Command::SetCourseRange` (one hyperedge over `{lo..=hi}`), `Command::FamilyPhaseBurn` (sugar for an immediate family-extent range), addressed `Payload::SetCourse`, and the existing contact-stop/notify actuators. After SAP, connected components of the geometric overlaps are published as compile-island metadata on the finite horizon. They do not yet include every signal/group/field dependency and are not independently advanced causal partitions ([H0025](HISTORY.md)). Quiet space is many tiny components; the packed-overlap / war-island fixture forms one large component while independent far families stay outside it ([H0018](HISTORY.md)). Equivalence grouping is not interaction grouping: overlapping families are not merged. This is not a semantic battle mode and does not introduce per-region clocks. The integration plan now schedules uneven causal cuts; this baseline does not implement them. Each family or SAP item compiles one guarded segment (enclosure disjointness, next SetCourse/SetCourseRange, contact-stop, inbound signal) and jumps to the earliest conservative invalidation; a failed guard applies IR and recompiles. A family member is extracted only when its generator actually changes. Do not expand a shared course into a clique of per-ship commands. Per-region clocks and uneven committed cuts remain deferred.

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
cargo observatory -- --world inertial
CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo run -p emergent-law-lab --example playground --offline --locked
./scripts/package-macos.sh
```

Replace `<unique-run-name>` before execution. Do not overwrite retained evidence. `cargo xtask verify PATH` checks a checkpoint's envelope and history checksum; use `Engine::replay()` for regenerated-state validation.

The bundled native app is `artifacts/Emergent Space.app`; it is a local unsigned development build, not a published/notarized release. Current screenshot output is `artifacts/screenshots/observatory.png`. These generated outputs are ignored by Git and may need rebuilding; source and `artifacts/evidence/1dac658/` are retained.

Toolchain is pinned to Rust 1.90.0; Cargo build jobs are two. On this machine `target` points to `/Users/julien_laurent/.cache/emergent-space/target` because Documents/iCloud offloaded generated files and stalled reads. Verify `ls -ld target`, file flags and actual running processes if Cargo appears idle; do not diagnose a physics/build failure from a filesystem stall. Recreate a normal local target or use `CARGO_TARGET_DIR` if the link is unavailable elsewhere. A nonfatal global-cache auto-clean permission warning occurred; `CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never` avoids that unrelated cleanup attempt. Do not delete shared caches or other projects to solve it.

At handoff, old specialist worktrees existed at `/private/tmp/emergent-mechanics`, `/private/tmp/emergent-observatory`, `/private/tmp/emergent-law-lab`. Their code was committed/recovered and integrated with root changes. Do not blindly remerge them. Earlier agents exhausted usage; inspect actual commits rather than assuming an agent's final status proves completed integration. Temporary paths and running-app state may change.

## Keep this context alive

Follow [history-workflow.md](history-workflow.md). Root appends meaningful decisions and measured outcomes to [HISTORY.md](HISTORY.md); preserve committed entries and frozen evidence. Update this handoff and the living card when heading/capabilities change. Run `cargo xtask history check` before finalizing. A documentation check does not prove physics, performance or that historical tests were rerun.

No engine build, benchmark, automatic simulation, external message or new implementation task was launched by this planning update. I0 implementation lives on `/private/tmp/emergent-full-engine-integration`; journal IDs after H0125 record that work.
