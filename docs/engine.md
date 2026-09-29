# The causal engine

How the engine decides what to compute, when and where. The law it evaluates is in [universe-quanta.md](universe-quanta.md) (numbers) and [gravity-law.md](gravity-law.md) (gravity). This file holds current truth only; its history is in the journal (H0156–H0181).

## What it computes

The universe's **events**: the places where a prediction breaks, and what happens there. Everything between events is a formula.

The state is certified generators, each with three parts:
- a formula (a worldline, a field, a region);
- a certificate: how long the formula stays exact;
- dependencies: who could break it, limited by c.

One operation: resolve the earliest broken certificate that something needs, exactly, then issue new formulas and notify the dependents. There is **one engine** (Julien, 29 September: "yes, why not one?"). Every evaluation order of the event graph (batch window, silicon, core count) gives the same bits, and the chronon reference survives only as a test judge.

**Cost follows surprise.**
- Compute is the entropy the demanded world produces. For contacts, about collision rate × log₂(2λ/r) bits (λ the mean free path, r the size); H0173 measured 4 bits per collision. For gravity, it's the acceleration the formula doesn't know ÷ the velocity quantum, in kicks per second.
- Memory is the entropy accumulated. Store high-entropy information and recompute low-entropy information: an undisturbed body is seed plus formula.

## Three primitives

| Primitive | What it is |
|---|---|
| **Certificate** | A claim ("nothing that matters changes here before t"): its expiry, its dependencies, and the representation that keeps it (an explicit body, a family, a cluster, a field summary, a lockstep grid). An event is a certificate expiring. |
| **Slack** | Time until the certificate's failure could first reach an observer, minus its forecast catch-up work ÷ throughput. Light cones give the first term, propagated through dependencies. The entropy forecast gives the second. |
| **Unit** | A bounded, pure piece of work: it reads committed inputs and proposes a renewal or commit. The same inputs always give the same bits, so a unit can run anywhere, early, twice, or be thrown away. |

**The rule in one sentence.** Keep the universe as certificates in their cheapest representation. Renew the least-slack one first. Do it in small pure units on the silicon that fits their shape, and spend spare capacity buying slack ahead.

## Rules

1. **Only causality and the frame are hard.** Global clocks, global windows, whole-world re-surveys and lockstep ticking are recommendations, to be questioned and deleted.
2. **No work without a requirement.** Every unit names the certificate it renews and the deadline it protects. The useful-work ratio is measured.
3. **Separate what from when and where.** The world is a pure function of inputs. The allocator may use clocks, heuristics and forecasts, and none of them can change the world: integer arithmetic is associative, and units are pure.
4. **Locality.** A unit touches a neighbourhood, never the world. Regions exchange boundary certificates ("nothing crosses before t").
5. **Least slack first.** Priority is slack, not proximity. A dense battle far away that can't catch up in time outranks a quiet planet next door: compute flows where it's harder. Every region's slack shrinks with time, so nothing starves.
6. **Forecast in aggregates, plan for the tail, never trust a forecast for correctness.** One surprise rate per region, computed from its macrostate (density, relative speeds, sizes, unknown acceleration), sets priority, batch window, cell size, silicon and storage. Every forecast is scored against measured cost. Sabotaged forecasts must leave digests unchanged.
7. **Barbell.** The frame never runs simulation: it draws the committed state inside the player's past light cone and never waits. Units are bounded (≈ 0.5 ms CPU, sized GPU dispatches), and publishing is a pointer swap. At the edge, speculation is free to discard.
8. **Keep headroom; sacrifice in a fixed order.** If the buffer drains: speculation stops, then off-screen regions lag (causal slack allows it), then time acceleration drops. The frame rate never drops. Waiting time explodes near 100% utilisation (Kingman).
9. **One engine, one continuous knob.** A region's batch window slides from event-driven (analytic jumps) to lockstep (a parallel pass on the GPU) as its surprise rate rises. Ladder v7's five modes (chronon, event, metal, hybrid, regions) merge into this one engine; the chronon stays only as the test judge every knob setting must match bit for bit. Aggregates (families, clusters, field summaries) stand in until a distinction reaches someone.
10. **Value of computation.** A unit's value is the new information it delivers before a deadline. Speculation is ranked by value × probability of use. Idle time goes to recompression, which lowers all future cost.
11. **One rule at every scale.** Every region, from a ship pair to the galaxy, exposes the same interface: frontier, next expiry, deadline, forecast, representation. New features are new certificate kinds, not new schedulers. Open: principle 7 makes multipoles the mechanism for causality regions too; the gravity cells hold them ([gravity-law.md](gravity-law.md)), but no region mechanism uses them yet.
12. **Correctness is proven independently of allocation.** Digests are identical across budgets, core counts, CPU and GPU, batch-window settings, the chronon judge, speculation on or off, and deliberately wrong forecasts. Build from long-proven algorithms: least-laxity scheduling (1973), calendar queues (1988), event-driven molecular dynamics (1959), Time Warp (1985), work stealing (1999).

## Numbers and errors

- **State lives on fixed-size integer lattices** (see [universe-quanta.md](universe-quanta.md)). Predicates are exact integers of bounded width. Rounding happens only in responses, with carries that keep the ledgers exact.
- **Every approximation declares its error type:**
  - bounded: allowed;
  - random walk: allowed only with a correction that bounds it;
  - secular drift: forbidden;
  - chaotic divergence of exact paths: physics, judged by statistics.

## Silicon and tiers

A unit's guarantees decide which tier it may serve:
- **Canonical:** exact integer paths only.
- **Advisory:** anything; a wrong answer may cost speed but never change results.
- **Presentation:** anything.

| Silicon | Cheap primitive | Use | Tier |
|---|---|---|---|
| Performance cores | branchy, latency-critical logic | low-slack commits, the event core near the player | canonical |
| Efficiency cores | background logic | high-slack compute-ahead, sealing, forecasting | canonical |
| GPU (7-core M1, Metal) | data-parallel 32-bit integer work; 64/128-bit emulated | used heavily ("spacetime is fundamentally the most gpu thing"): cell moments and field passes, batched in-cell drifts, dense lockstep regions, binning, candidate pairs; rendering has first claim | canonical |
| AMX (through Accelerate) | C += A·B | far fields, multipole translation. Floats are exact integers while nothing exceeds the mantissa (2^24 / 2^53), and wider integers split into Ozaki slices | canonical through exact slices |
| Neural Engine | learned guesses | cost forecasts, where the player will look or go | advisory |
| Media engine (HEVC) | prediction + residual | surprise sensor in worldtube-intercept coordinates (free motion ≈ an empty frame, collisions 35–70× above; H0163), previews | advisory, presentation |

Bytes moved are budgeted like time: structure-of-arrays layouts and cache-sized units. The bottleneck is memory, not arithmetic.

## One frame

1. **Draw** the committed past light cone from immutable snapshots.
2. **Order:** one hierarchical queue by slack. Performance cores pull the least-slack CPU-shaped units, efficiency cores take background units, and the GPU runs batched dense regions.
3. **Commit or discard.** Speculative results wait for their inputs to commit and are dropped if an input changed.
4. **Learn:** forecasts update from measured cost, and regions move along the batch-window knob.
5. **Watch:**
   - frame p50, p99 and max;
   - slack misses;
   - buffer level;
   - utilisation;
   - bytes moved;
   - useful-work ratio;
   - forecast error;
   - distinctions per second;
   - the real-time factor.

## The player's light cone

After genesis the player is the only source of new information. Every other agent is seeded and deterministic.
- Outside the future light cone of the player's present, the world is already fixed: computing there is never wasted.
- Inside it, results are provisional only where an actual action's own cone reaches, and actions arrive at human rate.
- Speculation targeting may use the Neural Engine. It only chooses what to precompute.

## Share codes: store consequences, not keystrokes

A code carries only what rebuilds the observable state, given the engine.
- **The world** is its seed: 4 words, with a checksum pinning the edition.
- **Player history** is reduced to the shortest input history with identical observable consequences: dead-code elimination, fusion, commutation of causally independent actions, timing coarsening. It is then entropy-coded against the engine's own predictions, and every candidate is verified by replay.
- **Sizes:** a what-if takes a few words; a long campaign becomes a file or a registry hash.

## Ladder obligations

- A dense battle on screen, and a battle off screen while the player idles.
- Sabotaged forecasts, and speculation on versus off.
- 1 versus 8 cores, CPU versus Metal, and every point on the batch-window knob.
- The memory wall.

Each gates on identical digests and reports the frame tail, slack misses, useful work and the real-time factor. See [test-ladder.md](test-ladder.md).

**Fields to borrow from:** event-driven molecular dynamics, parallel discrete-event simulation (Chandy–Misra–Bryant, Time Warp), real-time garbage collection, game job systems, "The Tail at Scale", self-adjusting computation, queueing and the theory of constraints, self-organised criticality, value of computation, causal invariance.
