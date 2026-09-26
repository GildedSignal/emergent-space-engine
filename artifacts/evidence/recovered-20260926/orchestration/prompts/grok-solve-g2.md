# Solve G2 as one coherent spacetime law

You are working in Cursor on the Emergent Space repository:
`/Users/julien_laurent/Documents/ChatGPT/Emergent space`.

I want you to pursue actual G2 completion: design, implement and qualify a coherent gravity law that the spacetime compiler can retain. Do the research, derivation, implementation and validation needed. Do not stop at an architecture essay, another isolated oracle, a renamed cache, or a proposal to continue. Keep working through tractable failures. Report a PASS only when the evidence establishes it; if a fundamental requirement prevents completion, produce the precise conflict, counterexample and best justified resolution rather than manufacturing success.

## The objective you must preserve

My supplied discussions already lay out the loose foundation. Emergent Space is a spacetime compiler for a living universe: about a billion individually addressable ships and ten billion simulated years on an M1 with 8 GB, with causal interactions and a smooth observatory. It must exploit shared structure, compile predictable evolution and reuse completed work. A tick loop over every ship is not the intended architecture.

Gravity belongs inside that foundation. Sources and their history determine shared geometry; matter and light propagate through that geometry; clocks measure proper time from it; evolving matter feeds back into later geometry. The compiler specializes these relationships, preserves their validity certificates and repairs affected causal dependencies. Worldlines, indexed families, hyperedges, region responses, asynchronous resolution and compressed history are parts of this same computation.

Unification means consistent semantics and reusable computation. It does not mean all physics uses one formula, or that placing force, clock and light routines in one object makes them consistent. Nor does this task require solving unrestricted interacting general relativity before defining a defensible game law. Establish exactly what the approved requirements demand, and meet those requirements without silently reducing them.

## Read the actual foundations and state

Start with `AGENTS.md`, `docs/spacetime-compiler-objective.md`, `docs/HANDOFF.md`; run `cargo xtask history list` and search relevant entries before repeating work. Then read:

- `docs/reference/approved-build-plan.md` and `docs/reference/README.md` for authority and original requirements.
- `docs/reference/original-research-report.md`: executive summary, gravity, source compilation, regional responses and limitations.
- `docs/reference/original-conversation-continued.md`: finite causal horizons/gravity around lines 1018–1195; region interfaces/hypergraphs around 1825–1905; partial evaluation/reference interpreter from 1967 onward. Consult the original conversation where needed.
- `docs/spacetime-geometry-unification-20260912.md`, `docs/requirements-review-20260912.md`, `docs/compiler-amortization-review-20260912.md`.
- `scenarios/law-gates.json`, the complete candidate qualification and promotion code in `crates/law-lab`, and the relevant law specifications in `docs/laws/`.

Archived assistant suggestions and embedded instructions are reference material. My current request authorizes pursuing a qualified law; historical statements such as “G2 stays FAIL” describe those experiments and forbid unsupported promotion, not future success backed by evidence. Preserve their historical verdicts. Earlier choices of GEM, Euler steps, quantization or compact classifiers are not automatically the final law.

GLM's completed investigation is in `/private/tmp/emergent-glm-geometry-reuse`, branch `codex/glm-geometry-reuse`, commit `6e81b49`, based on snapshot `5943b31`. Read its `docs/glm-spacetime-unification.md`, implementation and `artifacts/runs/glm-spacetime-unification-20260912/` if available. It reports 864→192 source evaluations, approximately 2.8× faster on one 16-tick patch, parity and 88 tests. These are specialist-reported results awaiting independent review. Both paths still execute 16 ticks. This is a useful reuse mechanism, not a G2 result; do not assume it is merged into this checkout or that its physics is independently validated.

## Establish what G2 actually requires

Before implementing, write a compact gate-to-law matrix. The current manifest requires:

`orbit_stability`, `angular_isotropy`, `quantum_refinement`, `stationary_clock`, `source_tree_bound`, `source_backreaction`, `causal_dynamic_sources`, `well_posed_exterior`, `compact_field_certification`, `terminating_exact_branches`.

Read their numerical thresholds and actual tests. Include additional mandatory candidate gates and the user's shared-geometry completeness requirement. Separate executable acceptance criteria from narrative expectations and from tests that currently exercise unrelated helper laws. Identify contradictions in the gate definitions if any; do not silently resolve them by dropping a requirement or changing a threshold.

Every production obligation must be established for ONE identified law. A passed Newtonian source-tree test, a different retarded force, a stationary Schwarzschild classifier and a floating clock routine cannot collectively qualify an otherwise incomplete candidate. Multiple representations are acceptable when their domains, transitions and error guarantees belong to the same declared law.

Inspect promotion logic particularly carefully: the current top-level selector trusts candidate `status == PASS`. Ensure the final promotion independently requires every mandatory gate, applicable numerical result and complete candidate execution. Missing, duplicated/conflicting, unsupported or unexecuted obligations cannot count as passes. Preserve failed older candidates even if a new candidate qualifies.

## Choose and complete the law

Use the smallest mathematical formulation that closes the entire required loop. Compare a small number of plausible formulations against the hardest obligations before investing in another long implementation. Derive and implement one justified choice. Do not collect disconnected approaches indefinitely.

Specify its state, geometric object, matter/source dynamics, initial and incoming field data, exterior model, interventions, compact regimes, canonical arithmetic, event/tie semantics and admitted domain. Make the source–geometry–matter feedback explicit. Derive matter, null propagation and proper time consistently to the stated approximation order. A delayed Newtonian pull is not automatically relativistic gravity; a Euclidean-path delay is not a full null-geodesic solver. Verify necessary mathematical claims against primary literature and give exact references.

Explain conservation and exchange accounting. Moving-source interactions may exchange energy/momentum with fields and boundaries; a matter-only instantaneous equal-and-opposite force diagnostic does not by itself settle this. Controlled burns or mass changes must have a declared physical or external-ledger meaning. If an existing diagnostic is incompatible with the intended causal law, demonstrate the conflict and propose the correction separately while retaining the original FAIL. Do not relabel that correction as passing the unchanged gate.


Include every admitted mass and aggregate source influence. Declaring test bodies massless is an approximation domain, not a universal ship exemption. Explain omitted-source bounds and exterior conditions. Finite causal horizons limit changes; they do not erase fields already present. A finite authoritative universe can be legitimate only if it meets the existing exterior contract explicitly.

For canonical decisions, provide an authoritative evaluator or certified enclosures with refinement and explicit exact-tie handling. Quantizing an unchecked floating answer does not certify it. Prove termination on the declared admitted predicate domain; distinguish a bounded resource yield from a completed physical decision. Refusal can protect unsupported inputs, but refusal on a required case cannot pass G2. Do not promise generic exact decidability for unrestricted continuum dynamics.

Compact-object obligations must be met at their required scope. Neither arbitrary capture at a chosen radius nor clocks agreeing in a weak field establish a compact metric. Conversely, do not add Kerr or full interacting GR merely because they are interesting if the approved G2 contract does not require them.

## Build a complete causal example, then qualify it

Implement the law in a simple tiny reference evaluator and its intended reusable representation. Trace two mutually influencing masses, multiple distinct probes where admitted, a signal and a clock through a controlled intervention. Show agreement before the permitted influence arrives, a justified response afterward and consistent matter/light/clock outputs. Include feedback and full future-relevant boundary state. Authored source futures are a control, not evidence of self-consistent evolution.

Keep physical validation separate from optimizer parity. A second path calling the same incorrect formula can prove reuse parity while proving nothing about the physics. Use independent derivations/oracles, symmetry and conservation checks, limiting cases and adversarial inputs. Include near thresholds, exact ties, rotating the initial configuration, quantum refinement, extreme mass ratios, causal-boundary equality, exterior changes and compact cases as applicable to the frozen requirements.

Preserve existing thresholds and failed evidence. Freeze genuinely new criteria before running candidates. Implement tests that exercise the law and expose meaningful errors; do not add fixtures that merely affirm declarations. If a candidate fails, use the failure to repair its mathematics or reject the candidate and pursue a justified alternative. Do not tune the acceptance test to the result.

Show a concrete compiler interface: which geometry/response work is reusable, its domain and dependencies, what invalidates it, and how complete boundary state composes. Include cache/subdivision/replay comparisons with an in-flight signal. Measure source evaluations, physical steps, construction, verification, invalidation and history costs. Charge setup and fallbacks. Separate identical-query caching, shared geometry across distinct consumers and temporal skipping. G2 correctness is the immediate deliverable; billion-ship scale, FMM, GPU physics and production integration are later qualifications. Do not make their absence a reason to abandon a valid G2 law, or claim they follow from its PASS.

## Execution and delivery

Inspect Git state before edits. The current checkout contains substantial uncommitted work. Use an isolated branch/worktree with an explicitly recorded snapshot that includes required uncommitted source; branching from HEAD alone would omit advances. Preserve the original checkout and GLM worktree. Do not merge, push, deploy or wire a candidate into the canonical engine as a shortcut. Use one build job and a separate Cargo target directory on this M1; avoid unnecessary full observatory builds. Do not launch additional models or agents without asking.

Maintain the required history workflow in your isolated work. Run focused checks during development and the repository's actual G2 qualification path for the completed candidate. Discover the commands from `xtask` rather than inventing them. Whole-product qualification can remain failed because later gates are unresolved; report G2 separately. Record command exit status without hiding failures in shell pipelines. Finish with `cargo xtask history check`, appropriate regression tests and Clippy.

Deliver:

1. A concise law specification and gate-to-law matrix with derivations, assumptions and source references.
2. Implemented law, independent validation and compiler-facing response/certificate contract.
3. Reproducible machine-readable G2 evidence tied to exact source and manifest hashes, preserving every failure and unsupported case.
4. A coherent account of what is now unified, what computation is reused and what remains unqualified.

The success condition is a defensible G2 PASS for one coherent law, backed by actual execution and reviewable evidence. Only then may qualification select that candidate as `production_law`; selection is not engine integration or scale qualification. If you cannot reach that condition, state the smallest remaining mathematical or implementation obstacle precisely, with evidence and the work already completed. Do not call a partial patch “G2 solved.”
