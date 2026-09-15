# Full engine integration and optimization — 15 September 2026

Status: **implementation plan for review and agent handoff; implementation not dispatched by this document.** Replaces the previous bounded compiler assignment as the planning heading. H0124 remains evidence that its assigned laboratory exits were completed. It does not establish a complete engine.

## Direction

Build one working engine around the actual coupled-source compiler, then use it to test which representations eliminate the most work while preserving the game. Optimization starts with the first integrated scene: account for compilation, certification, repair, storage and observation together. Hardware tuning comes after identifying the work that must remain.

The organizing abstraction is a **causal response over an interval**: retained state and history, admitted incoming influences, reusable evolution, outgoing influences, demanded queries, and the conditions under which those answers remain valid. A body, a fleet and a celestial group can use this contract with different internal representations. This is a proposed software boundary, not a claim that every subsystem has a small response or that GR reduces to one easy formula.

The first milestone is an executable end-to-end loop: moving massive sources → shared geometry → ship, ray, clock and contact → received information → policy intervention → source feedback → repair → saved/reconstructed history. The same loop must work when compilation pauses, an observer asks an unexpected question, and an earlier prediction becomes invalid. The eventual engine extends that loop to hierarchies, galaxies and compact objects.

## Evidence and research being used

Reviewed live worktrees and journal through **H0124**, on baseline `254ba1f` plus distinct dirty overlays. No physics, benchmark or native build was run for this planning review. Source findings below require executable reproductions before being treated as measured failures.

Sources: [assigned-exit evidence](laws/coupled-prompt-completion-evidence-20260915.md), [six-card contract](laws/litmus-gallery-contract-20260914.md), [earlier plan](compiler-engine-plan-20260913.md), [entropy hypotheses](compiler-entropy-deferred-20260914.md), [architecture hypotheses](compiler-architecture-remainder-deferred-20260914.md), and the [original research report](reference/original-research-report.md). Also reviewed the newer research critique and follow-up discussion in [Reconstruct emergent space idea](https://chatgpt.com/c/6a973e4f-7f90-83ed-81ab-6ab3a78bda04) and the candidate lessons in [Dwarf Fortress Optimization Lessons](https://chatgpt.com/c/6aa7db2c-69a4-83eb-a719-929bd52674a8). The newer deep-research response itself was not exposed by the task reader; its critique and subsequent hypotheses were. This is not a fresh literature validation, and the available notes are not an exhaustive research archive.

Julien's correction governs: **these are hypotheses to test, like the others**. No method earns implementation merely by appearing in research. The earlier notes' “not this turn” restrictions applied to the bounded laboratory task; they do not prohibit evaluating those ideas in this newly requested integration plan.

| Existing work | Preserve | What integration still needs |
|---|---|---|
| Selected compiler foundation, `/private/tmp/emergent-compiler-impl` | Exact inertial geometry, identities, indexed/phase families, scheduler, replay, Packet 0 selection inventory | Clean integration snapshot; gravity-capable event/observation paths |
| H0100–H0124, `/private/tmp/emergent-coupled-response` | Moving-source interval functions, A→B→A, held-out consumers, recouple, prefix reuse/repair, library gallery | Authoritative decisions, full cost accounting, actual resumability, compact long-time evolution, general boundary input |
| Packet 3, `/private/tmp/emergent-packet3-longtime` | Phase/composition APIs, boundary-carrying examples, arithmetic-growth controls | PERIOD is an added rational-rotation law; it is not coupled gravitational orbit evolution |
| Packet 4, `/private/tmp/emergent-packet4-population` | Family moments/bounds, extraction examples, materialized comparisons | General identities/extraction; real nonuniform gravity and bounded collective feedback. Current fixed layouts/COM residual are examples |
| Packet 5, `/private/tmp/emergent-packet5-engine` | Law admission and event/observation plumbing | Replace old truncated-law routing; compilation currently occurs atomically before budget charges are paid |
| Packet 6, `/private/tmp/emergent-packet6-history` | Archive integrity, pending-influence retention, received-knowledge policy semantics, individual broadcast reception | Incremental sealing/eviction, selective reconstruction, indexed policies and range-level reception work |
| Packet 7, `/private/tmp/emergent-packet7-qualify` | Frozen-manifest and measurement harness patterns | One connected gravitational workload. Existing yield measurements do not cover gravity compilation |

The coupled laboratory currently stores interval functions and worldtubes; Chebyshev compression remains a sidecar. Reported `1188 versus 1675` and `1126 versus 1722` source operations are scoped compile/repair counts. They are **not end-to-end savings**: the source review found validator work outside the returned aggregate. Preserve the historical numbers and add corrected measurements.

### Four issues to resolve before extending the compiler

1. **Repair completeness.** In `coupled_source_response.rs::repair_from_committed`, `compiled.incoming + extra` is retained in metadata, while continuation receives only `extra`. Reproduce an earlier inserted intervention followed by an already recorded later one, including repeated repairs. Establish whether execution drops that later cause, then fix the complete ordered input history.
2. **Hidden validation work.** `reuse_certified_interval_functions` calls `enclose_compiled_interval`, which performs two genesis reference evolutions and a Picard pass, then carries only validation/verification counters into the returned response. All executed work must appear in the full ledger. A runtime certificate must eventually be cheaper than replaying the entire history; offline verification must remain separately visible.
3. **Certificate authority.** The enclosure uses 16 sample times, sampled separations and floating arithmetic. Audit the phase-space norm, units and delay dependence behind `q = H·L` / `τ·L`. A sampled `certified: true` does not authorize an exact canonical event. Establish interval-wide coverage, retarded-root bounds and arithmetic error, or label the result diagnostic.
4. **Dense setup.** Quiet pair compilation eagerly stores a dense interval-history factorization through `store_pair_inverse`. Measure matrix dimension, allocated bytes and setup work as horizon grows. Make unnecessary setup lazy; test a bounded/block or matrix-free replacement only where a response consumer actually benefits. A dense boundary replacing a small source system can erase all reuse.

These are the first tests of the research's “zeros”: lost causes, unsafe decisions, hidden replay and expanding response state. They are not reasons to restart the entire project.

Other inspected costs belong in the initial profile: `field_at_stored` filters/sorts interval lists for queries; `incoming_knots` expands the horizon at a genesis light-crossing cadence; responses retain multiple forms of the same history. `coupled_phase_nav.rs::compile_ship_transport` performs five ship integrations and navigation rebuilds that transport during iteration. Those are useful implementations to improve, not established constant-cost lookup or general navigation reuse. Enforce query-horizon admission explicitly at the new adapter boundary.

## Contracts the integrator must settle

Keep the public engine vocabulary where useful: `advance`, `WorkBudget`, `observe_with_budget`, `inspect`, `decode`, `history_digest`, `replay`. Extend their implementation instead of maintaining an unrelated second game loop. Proposed internal types below are design names, not existing APIs.

| Contract | Required content and behavior |
|---|---|
| Model and authority | Law/version, units, admitted regimes, initial and incoming field history, self/source accounting, intervention balance, finite arithmetic and event equality/tie rules. Separate physical resolution from computational subdivision. |
| `ResponseDomain` | Stable source identities and membership, committed input cut, interval, spatial/query domain, incoming-history versions, supported consumers, and explicit unresolved/exterior bounds |
| `Response` | Evaluable source/transport functions plus sufficient boundary state/history; representation can be inertial, interval functions, phase+residual, aggregate or explicit. Store no mandatory per-logical-entity record. |
| Validation | Diagnostic enclosure versus authoritative certificate are distinct types. Bounds cover the whole admitted interval and composition, with units and assumptions. Ambiguity produces more work or explicit pending/refusal, never a guessed event. |
| Resumable work | Pollable compile/validate/repair/query/serialize jobs; cursors survive suspension inside expensive loops. Charge actual work before yielding, bound allocations, and expose pending status. |
| Commit and dependency | Mutable predictions are separate from immutable committed facts. Every reused response names dependencies and validity. A changed input repairs descendants; already committed facts cannot be rewritten by cache repair. |
| Representation conversion | Stable identity, mass, clocks, pending causes and history provenance survive split/extract/merge and explicit↔compressed transitions. Failed conversion retains a correct fallback. |
| Cost and lifetime | Owned/resident/temporary/archived bytes, CPU work/time, GPU residency, dependencies, reconstruction and retained causes are measurable. Eviction may remove derived data only if reconstruction remains possible. |

There are **three distinct comparison contracts**. A physical-law change compares behavior and magnitude anchors under identified initial states. Numerical refinement checks convergence under that model. A compiler-only change preserves canonical committed outcomes exactly. Do not turn a physical-step change into an optimization, or demand identical floating trajectories from two different numerical methods as a substitute for those contracts.

The production candidate needs a finite authoritative procedure that supports ordinary moving states, not only convenient genesis constants. The first law task must compare concrete finite-semantic options on that requirement. Fast floating evaluation may propose candidates; a sound bound or authoritative finite evaluator decides consequential branches. If no chosen procedure covers an admitted boundary, it is an unresolved capability, not a tolerance to hide in the renderer. The old floating laboratory remains available as a labeled diagnostic while this is built.

Commit ordering follows causal dependencies. Independent events may execute in either order; serialization can impose a stable presentation order without globally synchronizing physical advancement. Local proper time is an accumulated physical observable, not the scheduler's clock. A region's safe advance must account for already incoming influences, current fields, reachable source/receiver tubes and the model's propagation bounds—not just current distance divided by `c`.

## Implementation sequence

Each stage ends with a connected executable result and a decision. Later stages are conditional assignments; do not launch all of them immediately. Performance measurements accompany every stage. New commands named below are deliverables to implement, not commands claimed to exist today.

### I0 — Preserve, reproduce and establish the baseline

**Owner: integrator; independent reviewer for the four issues above.** Start from Packet 0's `SELECTION.md`; snapshot current tracked and untracked source overlays and required evidence. Record file hashes, source tree, base commit and tests. Create a clean `codex/full-engine-integration` worktree from the common baseline and import selected changes. Do not merge cumulative packet branches wholesale or delete the original worktrees.

Select the inertial foundation and current coupled compiler first. Extract Packet 5→6 policy/storage semantics as narrow deltas after reviewing old-law fields. Root owns Cargo manifests, exports, `runtime.rs`, storage schema and journal. Isolate new work into modules before assigning simultaneous writers.

Reproduce/fix repair input completeness and accounting; retain failing fixtures. Extend `Charge` into a nested ledger that totals every executed child operation, failed attempt, certificate, fallback and reconstruction once. Record offline audit cost separately from cost required for a normal runtime request; never subtract runtime validation from a performance claim.

An earlier inserted intervention in these repair tests is earlier than another predicted intervention, inside an uncommitted suffix or an explicitly new history branch. It does not authorize rewriting the committed past of the same world.

**Exit:** selected sources are reproducible; repeated/out-of-order repairs match a genesis reference with all interventions; full accounting reconciles with the call tree; source, wall-time and memory baselines are distinct. Existing H0124 tests still run in their historical scope. No claimed new speedup is required.

### I1 — Connect a genuinely resumable engine path

**Depends on I0. Owners: integrator plus law/validation and runtime specialists.** Freeze the shared contracts above and a small resolved initial-state fixture. Refactor the current interval compiler into continuation jobs, including retarded solves, coefficient construction, factorization, validation and repair. `advance(…, WorkBudget)` must suspend those operations, not charge them after they finish.

Connect two/three moving masses, a controlled test ship, a ray, a clock and a possible contact to existing events and observations. Add a received-message policy that changes a course, then observe delayed source feedback and repair. Retain an in-flight signal across save/restore. Bind all those consumers to the actual selected geometry; adapter names and labels do not satisfy this stage.

In parallel, implement the admitted finite-semantic reference and independent branch validation on these same moving cases. Start with contact/light-cone near-ties and full interval bounds. Do not require general strong-field GR before building the labeled experimental adapter. **No canonical gravity commitment is accepted until its authority path passes.**

Deliver I1 in two reviewable increments: first the resumable adapter and connected diagnostic scene, then the authority-backed commit path. The first can expose timing and integration faults while the second is being validated; it cannot report canonical-gravity acceptance. Keep algorithmic exactness checks separate from interval/model-accuracy checks. Exercise shifted units, moving near-tangent encounters between former sample times, input-epoch changes and queries just beyond the admitted horizon.

**Exit:** one headless connected scene supports pause/resume at internal job boundaries, different query orders, cache clearing, save/restore and replay. Slow versus compiled canonical facts agree; changing physical resolution is separately versioned/tested. Measure maximum uninterrupted operation duration including allocation/destruction and finalization. A pending required query stays visible. This is the first engine integration milestone, not full physics qualification.

### I2 — Join populations, history and causal scheduling

**Depends on I1. Owners: population and history specialists; integrator owns scheduler.** Expand the connected scene into a massive family perturbing a hierarchy while a ray is in flight. Initially use small materialized references; later grow logical membership independently of active exceptions.

Population work: stable procedural identity, general extraction, summed mass/moments with defensible residuals, family-level common transforms, and a restricted exact re-merge rule. Distinct histories may share future computation while retaining their histories and clock/policy differences. Permutation symmetry alone is not permission to merge interacting states.

History work: immutable incremental chunks and a replaceable manifest; bounded resident tails; indexes by identity/range and causal interval; selective reconstruction; dependency-aware retention of old source influence. Repair may require old emitted fields even after capture/removal. Do not restore the entire world to answer one historical observation. Repeated seal/restore must work without an empty new directory or copying all past events.

Policy/broadcast work: index committed receptions; group equivalent policy evaluations and shared effects; represent reception schedules over ranges where provable, extracting only distinctions that matter. Count logical receptions separately from stored records. Heterogeneous recipients still need their actual reception times; broadcast cannot become instantaneous or one unbounded loop.

Scheduler work: advance two regions to unequal certified cuts, then reconcile an arriving influence. Use a conservative finite-horizon dependency frontier first. No permanent independence from spatial overlap alone. Retain known incoming histories; detect lost lookahead, cyclic waiting and starvation. Bring tight dependencies into a joint solve when necessary. Expose a complete global cut only when all its required facts are resolved.

**Exit:** the coupled scene crosses extraction, re-merge, range reception, local advancement, history eviction and cold observation without changing canonical facts or omitting collective mass. Measure burst recovery and memory high-water marks. This stage tests composition, not several separate fixtures in one benchmark executable.

### I3 — Find the representations that remove evolution work

**Begins after I1 contracts; promotion requires the I2 composition scene. Owners: one numerical specialist and one representation specialist, sequential experiment families.** The immediate experiments are long-time source representation and perturbation response; neither must preserve the current implementation out of sunk cost.

**Time experiment:** compile a bound moving system over increasing dynamical durations; compare interval functions, phase+slow residual and the simplest relevant alternative. Include eccentricity, weak persistent forcing, resonance and a close-encounter transition. Building a whole trajectory before compressing it cannot establish skipped evolution. Measure construction, certificate, coefficient/bit growth, bytes, random-time evaluation, accumulated clocks and repair through the requested horizon. Packet 3 is an algebraic control, not the physical answer.

**Perturbation experiment:** compare full recouple, existing prefix repair, and a local response/sensitivity representation under a sweep of incoming weak tides and repeated changes. Charge basis/Jacobian/factorization construction and interval-wide remainder checks. The close-entrant share refusal stays a negative case; it must recover through recouple or another admitted solve. A noncontracting certificate may trigger a smaller interval or different method; it does not prove the physical solution impossible.

**Population experiment:** vary logical population, latent parameter variation, independent actions and exceptions separately. Exercise coherent orders, differential receptions, smooth perturbations, sparse outliers and repeated fragment/re-merge cycles. Measure bytes and work per represented distinction, plus query/extraction costs. A “war” label must not trigger fidelity or entropy changes.

**Exit:** keep only methods with matched behavioral/canonical outcomes and measured total-cost break-even in their admitted domain. Publish the domain and its failure case. Failure to beat the existing method is a useful rejection. If none removes enough sequential work, revise the representation before scaling the same loop to billions of years.

### I4 — Extend to connected physical regimes and far influence

**Depends on I1 authority and I2 interfaces; uses I3 findings. Owner: physics specialist, with independent verification.** This is required for full engine completion, not an indefinite “future research” bucket.

Use the six-card contract as the requirement list. Extend the admitted model in this order unless evidence changes the dependency:

1. Bound solar hierarchy and ordinary weak-field encounters, with initialized prehistory/incoming fields appropriate to that scene. The current genesis switch-on model is not automatically an equilibrium initializer.
2. Self-gravitating collective population: all represented mass contributes, including many small bodies. Compare direct small-world sums with candidate retarded hierarchical expansions or field modes; measure spatial rank, retained temporal history, derivatives, receiver sensitivity and repair costs. No distance cutoff justified only by “gravity decays.”
3. Fast test ships, rays, proper clocks and inverse navigation in moving geometry. Separate the source-speed approximation from the range of traveler speeds. Reuse existing navigation inversion as a starting control; qualify moving targets, burns, feasibility bounds and multiple/failed solution branches by forward verification.
4. Connected weak-to-strong near-mass transport and absorbing capture. Existing Schwarzschild predicates are anchors, not a complete propagator. Implement trajectories, light arrival/delay/bending and proper time, source/capture accounting, and a specified match to the exterior model. Test continuity and error/accounting across regime transitions. Stationary anchors cannot qualify moving multi-mass strong fields.

Each extension identifies its physical approximation, remainder, admitted states and fallback before results. Different numerical representations must agree in overlapping domains. A change to physical equations is a new model version; no per-card force law or independent bend/clock tuning. If a required regime cannot be matched, return the exact gap and two concrete model alternatives for review. Full-engine status remains incomplete until the required behavior is supported; a restricted release can only be a separately named scope.

**Exit:** all six cards and their crossing use the integrated engine; required queries return actual supported results. Quantitative anchors are proposed from independent derivations/reference data before candidate runs and presented for Julien's visual calibration. Unconfirmed game magnitude preferences remain visible; they do not permit post-hoc gate changes.

### I5 — Optimize the surviving work on the target machine

**Profiling starts at I0; this stage admits measured CPU/GPU changes once I2 supplies real workloads. Owner: systems specialist; root runs builds/benchmarks.** First remove full-history scans, repeated source evaluation, eager dense matrices, redundant copies and unbounded loops exposed by earlier stages. Then compare hot data layouts, cache-friendly blocks, arenas, reusable scratch, SIMD, conservative negative summaries and generation stamps on the kernels that dominate.

GPU work is conditional on a measured crossover: batch suitable field/candidate/transport work with bounded queue depth, retain CPU authority as required, and charge preparation, upload/residency, dispatch, synchronization, readback, verification and rendering contention. M1 shared memory is a shared budget. Keep responsive work out of long, noninterruptible batches. Do not require an arbitrary eightfold gain from eight unequal CPU cores.

**Exit:** end-to-end improvement at equal outcomes/quality; no worse unbounded tail, allocation spike or reconstruction debt. Publish CPU-only and combined simulation+rendering results, cold and warm, with RSS/owned-memory/GPU accounting explained. Hardware tuning cannot compensate for an unbounded representation.

### I6 — Qualify the engine and hand it to gameplay development

**Depends on I2–I5 and every required physics capability. Owner: independent verifier; root integrates.** Connect the native observatory to the same engine. Run a short daily gallery, a held-out behavior bank and the integrated operating-envelope ladder below. Verify cold history queries and final persisted/replayed state in the measured run.

Promotion requires a machine-readable matrix covering **all required gates on one identified model, implementation and workload**. A candidate with one PASS, independent passes from different laws, or unsupported required cards cannot select `production_law`. Keep `1dac658` and earlier laboratory reports unchanged; new results get new evidence paths.

“Full engine” means supported physical behaviors, causal navigation/observations, scalable shared populations, resumable work, selective persistence/replay and a native instrument working together within a declared operating envelope. The faction/economy design is not invented here. It receives received-information policy APIs, local resources/proper clocks, delayed actions and replayable consequences, and supplies later workloads that may expose new bottlenecks.

## Hypothesis queue and kill tests

This table is an experiment queue, not a list of promised implementations. Reorder by measured bottleneck and decision value. New research enters here with provenance and a distinguishing test.

| Hypothesis | First useful test / reason to reject |
|---|---|
| Small boundary responses replace interior dynamics | Sweep horizon, coupling and entrants; measure boundary rank, memory length, dense fill-in and total cost. Reject compression that moves work into a growing boundary. Projection/memory-kernel and circuit-reduction ideas are candidates to investigate here. |
| Shared causes plus innovations replace entity records | Same family under smooth forcing, shared orders and sparse exceptions. Reject if normal queries/extraction enumerate every identity or lose mass/individual history. |
| Restricted symmetry and re-merge prevent permanent fragmentation | Repeated split/recombine cycles with different clocks, messages and histories. Reject a merge that loses any future-relevant distinction. Start with provable generator equality, not general bisimulation machinery. |
| Sensitivity/low-rank response preserves reuse under change | Incoming-tide amplitude/frequency and repeated-kick sweep against full coupled solve. Reject at measured remainder growth or negative total-cost break-even. |
| Phase/secular or alternate field bases skip long quiet time | Increase horizon independently of population/query count; include resonance and encounters. Reject coefficient/history growth proportional to all skipped reference steps. |
| Finite-speed causal slack permits useful local advancement | Two unequal frontiers plus approaching influence, correlated broadcasts and tight recoupling. Measure valid lookahead, waiting and repair fan-out; reject unsafe distance-only bounds or starvation. |
| One-sided summaries avoid expensive negative queries | Reachability/contact/visibility or “possibly relevant” summaries with forced false positives. Any false negative rejects; track summary saturation and rebuild cost. |
| Lossless residual/XOR/succinct layouts help cold state | Real residual traces with random access, extraction and mutation. Compare encoded bytes plus index, decode and update cost; randomness cannot be compressed by wishing away distinctions. |
| Voxels/wavelets/modes beat source relations for a pressure | Local dense interaction or smooth collective field, with mass and delayed influence conserved by the admitted model. Charge conversion and boundary history; no mandatory universe-wide grid. |
| Incremental views make faction/policy work cheap | Shared received facts with individualized arrivals and changing views; reject omniscient shortcuts or repeated full-history scans. |
| Parallel-in-time or equality-saturation adds value | Only after sequential depth or representation selection is measured as limiting. Charge corrections/search/storage; do not build a generic framework to run one transformation. |

## Behavior and performance instrument

The user should be able to glance at the six familiar cards and recognize change. Each card shows its look-for, allowed outcome class, current model/regime, comparison type, and optional `reuse / newly_compiled / refinement / repaired_prediction` overlay. A failing input remains visible. Display magnification is labeled and never alters physical parameters.

Maintain resolved diagnostic initial states and a predeclared held-out bank. A compiler change uses identical states, law and interventions and must preserve canonical facts even in chaotic cases. A law/generator change records both versions; compare shared-state short-time physics separately from law-aware initialization and outcome ensembles. Re-seeding cannot erase a failure. Show invariant/magnitude drift and whole-system interactions underneath the qualitative cards; do not require every three-body seed to stay bound or every galaxy to spiral.

Every optimization runs on a workload vector: logical identities; represented families/modes; independently changing members; coupled component sizes; physical/dynamical duration; interventions and correlated arrivals; demanded observations/navigation queries; residual/history bytes. Deterministic information can still be expensive to reconstruct, so measure replay depth and dependency structure alongside compressed bytes.

Use four increasing workloads:

| Workload | Claim it can support |
|---|---|
| Tiny complete loop, explicit reference | Correctness and repair/authority semantics |
| Connected family + hierarchy + in-flight ray + observer/policy + archive | Composition and meaningful end-to-end optimization |
| Pressure sweeps and mixed quiet/hot regions | Break-even domains, fragmentation/rank/history/latency limits |
| Frozen integrated target workload | M1/8 GB operating-envelope qualification only for its declared activity/output distribution |

Retain the existing targets: **≤4 GiB total runtime memory including GPU once; ≤20 GiB archive; 30 FPS at 1080p; ≤5 ms cooperative-yield target; cold billion-identity/ten-billion-year run within one hour including final verification.** They remain targets, not measurements. Before the large run, freeze the independent-activity, behavioral, output and reconstruction workload so the benchmark cannot silently become an inertial age counter. Use intermediate rungs to find the limiting resource; do not extrapolate a small pass into a target pass.

Report total elapsed work/time for equivalent completed histories, separated into initial compile, runtime validation, source evolution, consumer queries, repair/fallback, history, reconstruction, verification and rendering. Report operation counts separately; they have unequal costs. A source-only saved fraction is never the end-to-end saved fraction, and overlapping gains are never multiplied. Include certificate size, dependency count, backlog, repair fan-out, storage read/write amplification, peak temporary memory, largest uninterrupted job, p50/p95/p99/max latency, and burst recovery. New gates are chosen before results; old evidence is immutable.

| Failure that can break the whole | Early warning and required response |
|---|---|
| Wrong canonical event or missing cause | Boundary/multi-repair falsifier; retain last sound cut and correct the path before promotion |
| Response/history no longer compresses | Rank, memory length, bytes and reconstruction-depth growth; change representation or expose the measured limit |
| One query materializes the world | Cold query amplification/peak memory; selective reconstruction and bounded continuations |
| Repair or refinement storm | Fan-out/backlog/failed-progress counters; shorten domains, recouple or fallback with explicit pending state |
| Allocation, serialization or GPU batch stalls the instrument | Worst uninterrupted work and combined-load traces; chunk/reschedule the actual operation |
| Mass, time or old influence disappears during conversion | Extraction/capture/eviction cross-tests; preserve boundary state and historical effects |
| Optimization creates a second bottleneck | Repeat the transformation through many split/merge/repair/query cycles; require stable memory/backlog or document the envelope |

Not every slowdown is a multiplicative zero. Distinguish wrong answers, unstable feedback, capacity cliffs and graceful throughput loss. An explicit overload pause preserves truth but still fails an operating-envelope target that required timely completion.

## Agent dispatch and ownership

The first dispatch is **I0 → I1**, not seven parallel subsystem rewrites. Root can run two narrowly scoped specialists alongside integration; only one heavy build/benchmark at a time, `CARGO_BUILD_JOBS=1` on the target. Specialists return code/evidence and a compact journal draft; root alone appends history.

| Assignment | Owned area | Concrete first return |
|---|---|---|
| Integrator | Selected worktree, Cargo/exports, public runtime and storage schemas, fixtures, task graph, journal | Pinned baseline, unified ledger, frozen connected-scene inputs and interface sketch; reconciled repair/charge findings |
| Law/validation specialist | Isolated response/validation module and its tests; no shared runtime writes | Reproduce multi-repair/certificate boundary cases; specify finite authority and interval proof obligations on ordinary moving states; implement one admitted path |
| Runtime specialist | New compiler continuation/job module and focused tests after interface freeze | Pause/resume real compile/validation/repair; demonstrate bounded work inside formerly atomic operations |
| Independent reviewer, after those returns | Read-only review or isolated adversarial tests | Attempt omitted-later-cause, between-sample encounter, unit/rescaling, stale dependency and hidden-cost counterexamples; no self-certification by shared labels |

Do not give two agents ownership of `coupled_source_response.rs` or `runtime.rs` simultaneously. Root first extracts narrow modules or serializes those changes. After I1, assign population and archive/view work in separate modules; root coordinates schema crossings. At I3, retain at most one competing optimization per pressure until the comparison is interpretable.

Each ticket includes the stage, exact source snapshot, prerequisites, owned files, supported model/domain, allowed approximations, budget, test commands, evidence destination and reject/fallback condition. Stop a hypothesis when its discriminating test rejects it; return the simpler fallback and result. An unexpected correctness hole is fixed before a new performance claim, not buried under more features.

Current baseline commands, run only after checking the selected overlay and available resources:

```sh
CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1
CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1
cargo xtask history check
```

I0 must add reproductions and a full-cost report; I1 must add the connected engine scenario and suspension/canonical tests. Subsequent tickets add their stage's tests to the same harness. The final integrator runs applicable workspace tests and the new integrated qualification matrix; a historical command's success cannot substitute for that work.

## First decision after implementation starts

After I0/I1, review one real scene and its full cost breakdown. Decide whether the next binding constraint is authoritative validation, source temporal work, response size, family fragmentation, history reconstruction or scheduling. I2 still connects the systems, but the first I3 experiment attacks that measured constraint. This keeps the plan directed toward the full engine while allowing an unsuccessful mathematical approach to be replaced promptly.
