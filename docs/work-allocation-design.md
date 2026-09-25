# Work allocation and the event core — design v0 (25 September 2026)

Status (25 September 2026, H0161): being built. The shared contract exists: the lattice law `es-lattice-elastic-v0`, the CPU chronon reference and mergeable digests in [crates/lattice](../crates/lattice/src/law.rs). It equals the independent integer gas reference bit for bit. Ladder [v5](../scenarios/scale-ladder-v5.json) runs every mode on v4's rungs. The event core (crates/lattice-event), Metal chronon mode (crates/lattice-metal) and the allocator (crates/allocator) are being built in parallel against that contract. GPU path decided: **Metal** (Julien, 25 September 2026): native 64-bit integers, unified memory, Apple target. The principles and whys are in [work-allocation-principles.md](work-allocation-principles.md). The ladder ([test-ladder.md](test-ladder.md)) judges every step, and no step may make another rung fail.

## Goal

Spend the least compute that preserves what matters, at every scale:

- the cost of one event is local, independent of world size;
- no frame ever waits on a spike;
- every core and the GPU are used;
- no approximation error can compound.

Measured starting point (H0158, H0159 draft):
- one core of eight used, no GPU;
- in the 4,096-ship pile-up, about 12,800 operations per collision, of which about 36 are the exact contact checks it actually needs;
- worst frame 138 ms;
- up to about 3,100 frames per simulated tick in dense scenes.

## 1. Numbers: fixed-size integers on chosen quanta

Julien: "even fp64 is quantized… what's the biggest quantization that we can get away with?" He also warned that once we are quantized, the order of operations matters.

- **State lives on lattices of fixed-size integers**:
  - positions in units of a position quantum;
  - velocities in units of 1/Q (Q a power of two);
  - time in chronons (integer ticks).
- **Positions stay exact without rounding**: a position at a tick is `x0 + v·T`, an exact integer on the lattice.
- **Every predicate is an exact integer computation of bounded width**: contact, cell exit and light-cone arrival. Coordinates are local to a region, so 64-bit values suffice, with 128-bit products where needed.
- **Integers, not floats.** Integer addition is associative, so a parallel sum gives the same bits in any order. That's what makes multi-core and GPU results identical to single-core results. Floats would make the answer depend on scheduling.
- **Rounding happens only in responses** (bounces, impulses), with the error-type rule below.
- **Why unlimited-size fractions are retired**: measured, exact bounces grow to 214,334-bit numbers after 34 bounces ([probe](../artifacts/evidence/scale-ladder-v3-20260925/gas_arithmetic_probe.py)).

This is a new law version. The current `es-inertial-causal-v1` keeps its fractions until the new core passes the whole ladder.

## 2. Error-type rule

Every approximation declares its error type. The ladder must include a long run proving the error stays bounded.

| Type | Rule |
|---|---|
| Bounded (oscillates, never grows) | allowed |
| Random walk (grows like √n) | allowed only with a correction that makes it bounded, e.g. the energy carry |
| Secular (drifts one way, grows like n) | forbidden |
| Chaotic divergence of exact paths | physics, not error; judged by statistics (temperature, pressure, speed distribution) |

## 3. The local event core (fixes the pile-up bookkeeping)

This replaces the global look-ahead window, the single-axis sweep, and the per-event re-survey. It follows event-driven gas simulation (Alder and Wainwright; Rapaport; Lubachevsky; Donev et al.).

- **Cells.** An adaptive grid, or quadtree, in space: big cells where space is empty, small where it is dense. A group (family) registers as a range over the cells its members cover, and is split only where something can tell its members apart.
- **Per-item events only**:
  - next contact with an item in the same or a neighbouring cell;
  - leaving its cell;
  - next scheduled command or signal arrival.
  
  Leaving a cell updates the item's neighbours. So an item's look-ahead is exactly as long as it stays in its neighbourhood: aeons for a quiet ship, a few chronons in a crowd. There is no global window to tune.
- **Event calendar** per region, a priority queue (O(log n), or O(1) with a calendar queue).
- **An event touches only its items and their neighbours.** Their next events are recomputed and nothing else. The target is cost per collision proportional to the number of neighbours, which does not depend on world size. Today it is ~12,800 operations and growing with N.
- **Piles become clusters.** Ships resting in contact form one rigid cluster: one entry, split when something acts on part of it. This prevents the "inelastic collapse" storm we hit (H0157).

## 4. Two execution modes, chosen by density

The dimensionless number is predicted collisions per item per chronon, κ. Kinetic theory gives it before any collision happens: collision rate per area ≈ ½·n²·σ·v̄_rel, where n is density, σ the collision cross-section (two diameters in 2D) and v̄_rel the mean relative speed.

- **Sparse (κ ≪ 1): event mode.** Jump analytically from event to event on the CPU. Quiet time costs nothing.
- **Dense (κ large): chronon mode.** A data-parallel pass per chronon on the GPU:
  1. bin items into cells (counting sort);
  2. generate candidate pairs from neighbouring cells;
  3. run the exact integer contact predicates;
  4. resolve responses with the deterministic simultaneous-batch rule;
  5. advance.
  
  Events are already defined per chronon bin, so within one chronon everything is independent. Only the order of chronons is sequential. That is why "ordering events is branchy and sequential" was the wrong framing for dense regions.
- **Both modes give identical canonical results.** The ladder checks it (mode invariance), like budget invariance today.
- **Measured motivation (H0159):** for the 64-ship gas (10% fill, 1,024 ticks), a naive integer simulator that steps every tick and checks every pair finishes in 0.06 s. The current event engine takes 4.3 s. At that density, plain stepping already beats the event engine by about 70 times.

GPU work beyond dense regions:
- building the cell index for all regions;
- filtering candidate pairs;
- gravity field sums and multipoles;
- evaluating groups;
- sensors and visibility (ray casts);
- rendering.

The M1 shares memory between CPU and GPU, so no copies are needed. The CPU keeps orchestration, sparse event logic, history and commits.

## 4b. Use the whole computer

Julien, 25 September 2026: "I paid for the whole computer, I'm going to use the whole computer." The working principle: don't assign work to hardware; transform each world problem until some piece of silicon already solves it. A unit's numerical guarantees decide which tier it may serve:

| Tier | May use | Why |
|---|---|---|
| Canonical (the universe) | exact integer paths only: CPU cores; the GPU in 64-bit integers; AMX through exact slices | must be bit-identical across modes, cores and machines (§2, §6) |
| Advisory (what to compute first) | anything, including lossy or non-deterministic units | a wrong forecast may cost speed but may never change results; the ladder sabotages forecasts to prove it |
| Presentation (what the player sees) | anything | discardable caches built from canon |

| Silicon | Primitive it does absurdly cheaply | Where it occurs in Emergent Space | Tier |
|---|---|---|---|
| P and E cores | branchy sequential logic | sparse events, commits, bookkeeping | canonical |
| GPU compute | data-parallel integer work | dense chronon mode, binning, candidate pairs | canonical |
| GPU depth test | per-pixel argmin over candidates | earliest causal arrival T(x) = min over sources of t_i + \|x − x_i\|/c (cones plus depth test is the classic graphics-hardware Voronoi construction): per-tile safe horizons for regions | advisory, or canonical only if biased conservatively (never later than the true arrival) |
| GPU tile memory | binning geometry into tiles, local processing | broad phase as a render pass | measure first: only if compute binning is bandwidth-bound |
| GPU samplers and mip levels | interpolation across space and scale | the representation hierarchy (ships, groups, fleets, aggregates), response tables | representation: canonical as exact sufficient statistics; hardware filtering: advisory or presentation only |
| AMX | C += A·B | low-rank interaction operators K ≈ U·Vᵀ (gravity far field, multipole translation, sensor response) | canonical through exact integer slices; step 7 |
| Neural Engine | learned guesses | speculation targeting | advisory |
| Media engine (HEVC, motion estimation, frame interpolation) | prediction plus residual | surprise sensor (below); rewindable visual memory; far-sky impostors; clips | advisory and presentation |

**The HEVC surprise sensor, measured** ([evidence](../artifacts/evidence/hevc-proxy-20260925/summary.txt), [probe](../tools/hevc-probe/main.swift)). Setup:
- six worlds of 16,384 ships, each with a known count of committed events;
- rasterised three ways and encoded on the hardware HEVC encoder at fixed quality, about 500 frames/s at 512×512.

Bytes per predicted frame:

| World | Events per frame | Position (x, y) | Phase (x, vx) | Worldtube intercept (x − vx·t, vx) |
|---|---|---|---|---|
| gas | 1,515 | 11,541 | 9,406 | 6,247 |
| shock | 1,468 | 6,296 | 4,505 | 3,199 |
| free random (pass-through contacts) | 157 | 8,956 | 3,675 | 100 |
| uniform translation | 0 | 4,673 | 92 | 91 |
| swirl | 0 | 4,587 | 3,752 | 100 |
| static | 0 | 109 | 91 | 91 |

- **Position space measures visual incoherence, not dynamics.** A pure translation costs almost as much as a shock.
- **Worldtube-intercept space fixes it.** Free motion is exactly static there, so free worlds sit at the empty-frame floor (91–100 bytes). Colliding worlds sit 35–70× above it. "Residual bitrate ≈ new dynamical information" holds once the picture is drawn in the engine's own prediction coordinates.
- **Where it adds information.** For individually simulated ships, the engine's own event counters are exact and free, so the sensor would only re-measure them. It adds information where no microstate is simulated: aggregated regions, cheap coarse previews, far regions updated rarely. There it is a candidate forecaster for the allocator. It must beat the kinetic forecast and the engine's own event rates on the ladder (deadline misses, buffer drains) before it earns a place.
- **Never canonical.** It is lossy, 8–10-bit and not promised to be identical across devices or OS versions.

## 5. The allocator

**Units of work: regions.** A region is an island whose future cannot touch another's before a known time. Each region has:
- its own clock (frontier);
- a deadline;
- a predicted cost rate, from κ and recent event counts;
- a priority.

**Deadlines from light cones.** A region's deadline is the earliest moment its consequences can reach an observer that matters: the player's present (distance / c), or another region that depends on it. A region whose news cannot reach the player for 10 years may lag 10 years (causal slack). What the player is looking at is prioritised first.

**Scheduling:**
- earliest deadline first across all regions;
- regions spread over performance cores, efficiency cores and the GPU, with work stealing;
- regions merge when their light cones intersect and split when they separate.

**How the frame is made immune to spikes.** The work tail cannot be removed; avalanches are physics. The frame's exposure to it can be bounded:
1. **The frame never runs simulation.** It renders the latest committed state inside the player's past light cone. Simulation runs on workers.
2. **Bounded work units.** No unit may exceed about 0.5 ms of CPU time; GPU dispatches are sized the same way. Large simultaneous batches are prepared in chunks and published with a pointer swap (double buffering), so publishing costs O(1).
3. **Compute-ahead buffer.** In quiet periods, workers simulate ahead of the player's present. A spike drains the buffer instead of the frame. The buffer target is sized from the forecast (κ maps) and the measured avalanche tail.
4. **Graceful degradation, never a hitch.** If the buffer drains, off-screen regions lag, which causal slack allows. As a last resort, the time-acceleration factor drops. The frame rate does not.
5. **Slack.** Workers are kept below saturation. Queueing theory says waits explode as utilisation approaches 100%.

**Monitoring on every ladder rung:**
- utilisation per core and for the GPU;
- queue depths and buffer level;
- deadline misses;
- frame p50/p95/p99/p99.9/max;
- simulated ticks per wall-clock second.

## 6. Invariances the ladder checks

Every capability must give the same history digest when any of these changes:
- slice budget (today);
- core count (1 vs 8);
- CPU vs GPU mode;
- event vs chronon mode;
- cache eviction and replay.

This is the causal-invariance licence to run in parallel: if the order of updates cannot change the result, updates can run anywhere.

## 7. Build order (each step gated by the whole ladder)

1. Elastic bounce law, walls, momentum-exact lattice rounding with energy carry, mass-aware impulses, and the trapped-gas track C2. Built on the current engine as the harshest benchmark and as the first lattice-arithmetic experience. In progress with this design.
2. Local event core (§3) in fixed-size integers, single core. It must match an independent reference simulator and pass every existing rung.
3. Bounded work units, time-boxed frames, compute-ahead buffer, region clocks (§5).
4. Multiple cores with core-count invariance.
5. GPU chronon mode and GPU index building, with CPU/GPU invariance.
6. Groups and gravity on the new core (the gravity contract).

## References to mine for each step

| Field | What to take |
|---|---|
| Event-driven molecular dynamics | cells, neighbour lists, calendar queues, delayed states, inelastic collapse |
| Parallel discrete-event simulation (Chandy–Misra–Bryant, Jefferson's Time Warp) | safe look-ahead between regions; optimistic execution with rollback |
| Real-time garbage collection (Baker; Metronome) | a guaranteed maximum pause by bounding each unit of work |
| Game job systems and fibres; "The Tail at Scale" (Dean and Barroso) | small units, frame budgets, latency-aware scheduling |
| Incremental and self-adjusting computation (Acar) | cost proportional to what changed |
| Queueing and the theory of constraints | Little's law; slack; the buffer in front of the bottleneck; small batches |
| Self-organised criticality (Bak) | avalanche workloads are power-law; buffer them rather than fight them |
| Information theory; value of computation (Russell and Wefald) | spend compute where the most new information will reach an observer |
| Wolfram's causal invariance | order-independent updates can run anywhere |
