# Architecture and current qualification boundaries

## Reality and evaluation

`CanonicalState` contains the law, seed, normalized generator commitment, committed causal cut, physical trajectory changes, interventions, outstanding signals and event facts. Search jobs, co-moving broad-phase boxes and UI snapshots are derived. A hash names an explicitly completed causal cut; it does not hash memory layout or unfinished evaluation coverage.

`Engine::advance(target, WorkBudget)` resumes a pending discovery pass. The pass certifies all possible earlier contacts and message arrivals before committing the next simultaneous batch. A complete empty pass jumps directly to the requested cut. Each actual trajectory change invalidates the derived pass. The engine never loops over elapsed ticks or conceptual population size.

The broad phase sweeps exact enclosing boxes in a shared co-moving frame. This cancels common drift before it inflates a billion-year worldtube. Family ranges refine only where a pair remains ambiguous. The present implementation uses a sweep and family bisection, not a production spacetime FMM. The hierarchical spacetime address type is available; general block compilation remains downstream of physical-law selection.

## Laboratory event law

The numeric primitives are specified in `laws/inertial-causal-v1.md`. The runtime adds these explicit semantics:

- Time starts at tick zero. A newly emitted addressed signal can be received no earlier than the next tick; otherwise reception is the earliest integer tick in the emission's light cone. There are no zero-time message cascades.
- Contacts use continuous swept geometry within half-open tick bins, including tangencies and contacts between endpoint samples.
- Default contacts are reported once for a pair of unchanged trajectory revisions. A contact may activate an explicitly configured external stop actuator and an outgoing notification.
- Simultaneous received impulses add on the pre-batch state. A configured contact stop takes precedence. The complete batch is validated before any change commits. Subluminal velocity is required.
- External burns/stops transfer the opposite linear momentum to the explicit actuator ledger. This is a controlled kinematic laboratory, not a model of collision material, relativistic propulsion energy, or a closed gravitating system.
- Proper time uses a law-defined dyadic rate per physical segment; querying or caching a segment does not add rounding.

`inspect` accepts only committed times. `decode` reconstructs a generator/identity without claiming its uncomputed future is certified. Sensor queries return retarded emissions and test moving finite-radius occluders, including unmaterialized family members; diagnostic queries expose true coordinate-time state. No observation changes the world.

## Compression and identities

An affine family stores an identity range, an original parameter offset, shared motion, spatial stride, radius and mass. Split ranges preserve the original parameter and RNG identity. Canonical initialization normalizes adjacent compatible partitions. A binary identity-range lookup avoids scanning every family.

An intervention extracts one member into the sparse body map. Other members remain represented by the family, and geometric search excludes extracted identities from the original range. Exact total mass and first moments remain evaluable for untouched families. Full source compilation must additionally account for exceptions; no production gravity path currently consumes incomplete summaries.

The current family law requires provably disjoint members sharing velocity. More general route/departure/phase distributions and interacting family interiors are future representations behind the same certificate requirements. This limitation is explicit, not statistical merging.

## Persistence and responses

Checkpoints have a schema/law identifier, payload checksum and canonical history checksum. Writes use a same-directory temporary file, data sync, atomic rename and directory sync. Restore validates the envelope and engine structure and rebuilds search state. `Engine::replay()` starts from retained initial generators and ordered external commands, regenerates causal events, and compares the complete canonical state. A 256 MiB checkpoint read/write cap prevents uncontrolled allocations; chunked long-history archives are not yet implemented.

Transport responses carry a time domain, full inertial boundary state and dependency versions. Composition rejects mismatched boundary velocity, position or versions. The bounded cache evicts reconstructible entries. The min-plus utility is limited to fixed complete discrete boundary states. It is not advertised as a general fuel-aware navigator or a complete nonlinear block eliminator.

## Native observatory

The UI speaks only `UiCommand` and `UiSnapshot` to its engine worker. Rational-to-float conversion is for drawing. Navigation converts a selected heading to an explicit rational controlled velocity, which the canonical layer validates. It does not claim fuel-optimal routing or automatic arrival. Snapshots identify the active laboratory law and committed/pending time.

## Research gate and retained work

G0/G1 are tested independently. The law laboratory runs quantized velocity-Verlet and stationary piecewise-lapse experiments, including orbit/rotation/quantum checks and a direct moving-source causality counterexample. Neither may be promoted merely for stable orbits. A causal dynamic source law, well-posed unbounded exterior, compact-field treatment and terminating exact branch evaluator remain mandatory production gates.

The plan explicitly permits a verified causal kernel plus a named failed law gate. This repository follows that failure path. G3 and integrated G8 stay blocked; family, persistence and observatory mechanisms are useful partial work, not substitute qualification. No instantaneous gravity is silently wired into the canonical engine.

## Remaining runtime engineering

The operation budget currently counts queued signal/contact refinement jobs. Initial broad-phase construction, sorting and swept-box comparisons have separate metrics and capacity limits but are not yet resumable at each operation. Sensor family refinement has a work cap and returns an explicit resource error; it does not yet return a continuation token. Both execute on the UI worker. This protects the render thread but does not establish bounded command latency under arbitrary event storms. General query continuations, incremental broad-phase preparation, byte-based allocation limits and chunked archives remain required before full G6/G8 qualification.

The current native smoke test establishes successful rendering and real command-to-engine integration. It does not establish a 30 FPS / 1080p operating envelope, total GPU-inclusive memory, or parallel/GPU physics parity. The CPU benchmark reports process peak RSS separately from serialized state.
