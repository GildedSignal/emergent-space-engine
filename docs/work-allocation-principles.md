# Work allocation — principles and plan (v1, 25 September 2026)

Status: proposed for Julien's review. Supersedes §5 of [the work-allocation design](work-allocation-design.md) as the statement of *why*; that design remains the implementation sketch. GPU path: Metal (Julien, 25 September 2026).

## The rule in one sentence

**Keep the universe as claims with expiry dates, each in its cheapest representation. Always renew first the claim with the least slack before any observer could notice it expire. Do the work in small, pure units on the hardware that fits their shape, and spend spare capacity buying slack ahead.**

## Three primitives

Everything else is derived from these three.

| Primitive | What it is | Why it is primitive |
|---|---|---|
| **Certificate** | A claim ("nothing that matters changes here before time t"), its expiry t, its dependencies, and the representation that keeps it (explicit ship, family, cluster, response, field summary, chronon grid) | The engine's knowledge is only ever a set of claims that hold until they don't. Events are claims expiring. |
| **Slack** | For a certificate: its deadline minus now minus its forecast renewal cost. The deadline is the earliest moment its failure could reach an observer, which light cones give for free (distance / c, propagated through dependencies). | This is the one quantity that says what must happen next. Critical regions are simply the places with the least slack. |
| **Unit** | A bounded, pure piece of work: it reads committed inputs and produces a proposed renewal or commit. The same inputs always give the same bits. | Bounded means no frame can be hit by an avalanche. Pure means any unit can run anywhere, early, twice, or be thrown away. That is the freedom the allocator lives on. |

Derived concepts:
- a **region** is a set of certificates that depend on each other;
- an **event** is a certificate expiring;
- a **critical region** is least slack × highest forecast cost;
- the **buffer** is slack accumulated ahead of the deadlines;
- **speculation** is renewing before it is needed;
- **recompression** is making certificates last longer;
- **hardware choice** follows from a unit's shape.

## The rules, with their whys

1. **Only two constraints are hard: causality and the frame.** Everything else (global clocks, look-ahead windows, per-event re-surveys, lock-step ticking) is a recommendation, to be questioned and deleted.
   *Why:* Musk's first principle — "The only rules are the ones dictated by the laws of physics." Our physics is the light cone, and our product is the frame.

2. **No work without a requirement.** Every unit must name the certificate it renews and the observer deadline it protects. Work that protects no deadline is waste, and the useful-work ratio is measured.
   *Why:* question the requirement, then delete. In the 4,096-ship pile-up, 99.7% of operations protected nothing (~36 useful of 12,800 per collision).

3. **Separate *what* from *when and where*.** The canonical world is a pure function of inputs. The allocator only decides when and where units run. It may use wall-clock time, heuristics and forecasts, and none of it can change the world.
   *Why:* von Neumann and Goldstine's lesson from the first error analysis of machine arithmetic: correctness must follow from structure, not from luck in execution. Our structure is purity plus integer lattices: integer addition gives the same bits in any order, so any core, the GPU, or a re-execution agrees bit for bit. This is the causal-invariance licence to parallelise.

4. **Locality: a unit touches a neighbourhood, never the world.** Cost is proportional to the distinctions a change can affect, never to world size. Regions exchange boundary certificates ("nothing crosses before t"), and between those promises they are independent.
   *Why:* physics is local and light speed makes the locality exact. Event-driven gas simulation has done this since 1959.

5. **Least slack first.** Renew the certificate with the smallest slack (least-laxity-first). Deadlines propagate backwards through dependencies, like the critical path in a project plan or instruction scheduling in a compiler.
   *Why:* earliest-deadline-first is optimal on one processor when the load fits. Slack adds the forecast cost, so a big job that is due later can still go first. Aging is built in: as time passes, every region's slack shrinks, so nothing starves.

6. **Forecast in aggregates, plan for the tail, never trust forecasts for correctness.** Every region carries a Fermi estimate of its cost rate: kinetic theory for contacts (≈ ½·n²·σ·v̄_rel), plus signal, command and field refresh rates. The estimate comes with a confidence band. Buffers and hardware are sized by the upper tail, not the mean.
   *Why:*
   - Fermi: a decomposed order-of-magnitude estimate is cheap and usually right to within a factor of a few.
   - Asimov: masses are predictable where individuals are not, so forecast per region, not per ship.
   - Taleb: tails can't be computed, but exposure can be bounded; and forecasters must be scored on their confidence, not just their estimate. Every forecast is scored against measured cost, and bad forecasters get wider bands.

7. **Barbell: a paranoid core, an aggressive edge.**
   - Paranoid core: the frame never runs simulation. It draws the latest committed state inside the player's past light cone. Units are bounded (≈0.5 ms CPU, sized GPU dispatches), and publishing is a pointer swap.
   - Aggressive edge: speculative compute-ahead where the player is likely to look or go. It is discarded for free when invalidated, because units are pure.
   *Why:* Taleb's antifragility is aggressiveness plus paranoia — clip the downside, let the upside run. The downside (a hitch, a wrong world) is ruin. The upside is smoothness and depth.

8. **Survival first: keep headroom.** Never plan to saturate the machine; reserve capacity for the tail. If the buffer drains, the order of sacrifice is fixed:
   1. speculation stops;
   2. off-screen regions lag (causal slack allows it);
   3. the time-acceleration factor drops.
   
   The frame rate never drops.
   *Why:*
   - Kelly and Taleb: avoid ruin before optimising.
   - Queueing theory (Kingman): waiting times explode as utilisation approaches 100%.
   - Goldratt's drum-buffer-rope: the drum is the frame, the rope is causality, the buffer is slack ahead of the drum.

9. **Match the unit's shape to the hardware; memory is a resource.**
   - GPU (Metal): wide, uniform work — dense chronon regions, index building, candidate filtering, field sums, visibility, rendering.
   - Performance cores: branchy, latency-critical work — commits for low-slack regions, event mode near the player.
   - Efficiency cores: background work — compute-ahead for high-slack regions, archive sealing, forecasting.
   - AMX matrix coprocessors (Julien's M1 table: ~1.3–1.6 TFLOPS FP32 on the performance cluster, ~3 TFLOPS FP16): dense, matrix-shaped work next to the CPU caches, with no dispatch latency. That means gravity fields and multipole translations, response maps, and forecast models, reached through Accelerate. **Floats are integers in disguise while nothing exceeds the mantissa** (2^24 for FP32, 2^53 for FP64). Inside that range every product and sum is exact, so the result is exact and independent of summation order. Local coordinates keep lattice values small. Wider integers are split into slices whose partial products and accumulations stay inside the exact range, so each slice product is an exact floating-point matrix product: the Ozaki-scheme idea, used to emulate FP64 and integer matrix products on low-precision tensor units. The slice count is known in advance from the operand widths, so AMX (and Metal's FP32/FP16 units) compute canonical, bit-exact integer results, not just advice.
   - Rendering gets its GPU share first.
   - Bytes moved are budgeted like time: structure-of-arrays layouts and cache-sized units, because the bottleneck is memory, not arithmetic (von Neumann's bottleneck; Julien: "CPUs spend huge amounts of time waiting for memory").

10. **Representation is chosen by the certificate's lifetime.** One dimensionless number, κ (expected certificate expiries per item per chronon), decides:

    | Regime | Representation |
    |---|---|
    | κ ≪ 1 | event mode: jump analytically, on the CPU |
    | κ large, many items | chronon mode: a parallel pass per tick on the GPU |
    | lifetime ≫ any observer's need | aggregate (family, cluster, response, field summary) until a distinction matters |
    
    Switching representation never changes canonical results. The ladder proves it.
    *Why:* Musk's "the best part is no part": the cheapest correct representation is the one that computes least. Asimov: aggregates are exact enough until an individual distinction reaches someone.

11. **Value of computation breaks ties and prices speculation.** A unit's value is the new information it delivers to observers before their deadlines. Quiet, predictable regions carry almost no surprise and cost almost nothing. Speculation is ranked by value × probability of use. Idle time goes to recompression (clusters, families, responses), because recompressing lowers all future cost.
   *Why:* Shannon: information is surprise. Russell and Wefald: compute where it changes decisions. The project bet is H_causal ≪ V.

12. **One rule at every scale.** A region at any level (ship pair, cluster, fleet, system, sector, galaxy) exposes the same interface: frontier, next expiry, deadline, forecast, representation. A parent schedules its children by rule 5 and stands in for them as an aggregate until a distinction matters.
   *Why:* a scale-free rule is the only kind that survives 10¹⁰ ships and 10¹⁰ years. New features (gravity, agents, history) become new certificate kinds, not new schedulers.

13. **Don't fool yourself: correctness is proven independently of allocation.**
    - Every capability must give the same history digest across budgets, core counts, CPU/GPU, modes, speculation on or off, and deliberately wrong forecasts.
    - Components have skin in the game: each representation's and forecaster's measured cost and error is tracked, and poor ones are demoted automatically.
    - Build from long-proven algorithms (earliest-deadline and least-slack scheduling 1973, calendar queues 1988, event-driven MD 1959, Time Warp 1985, work stealing 1999); novelty only in how they are combined.
    *Why:* Feynman — you are the easiest person to fool. Taleb — skin in the game and the Lindy effect. The Spartan ladder.

## How one frame works

1. **Draw.** The frame draws the committed state inside the player's past light cone, from immutable snapshots, never waiting on a unit.
2. **Order.** The allocator holds one hierarchical queue of certificates ordered by slack. Workers pull units: performance cores take the least-slack CPU-shaped units, efficiency cores take high-slack and background units, and the GPU runs batched units per dense region.
3. **Commit or discard.** Results that renew certificates commit (pointer swap). Speculative results wait until their inputs commit; if an input changed, they are discarded.
4. **Learn.** Forecasts update from measured cost. Regions whose certificate lifetimes change switch representation.
5. **Watch.** Monitoring records, every frame:
   - frame p50/p95/p99/p99.9/max;
   - slack misses;
   - buffer level;
   - utilisation per core and GPU;
   - bytes moved;
   - useful-work ratio;
   - forecast error;
   - distinctions per second.

## Critical regions

A region is critical when its slack is small relative to its forecast cost. It needs work soon and the work is large.

Kinetic theory flags battles before their collisions happen (density and relative-speed maps). Light cones flag what the player is about to see. Their product ranks where compute goes. A critical region that stays critical changes representation rather than exhausting the budget: a pile becomes a cluster, a dense battle moves to GPU chronon mode.

## Inversion: how this would fail, and the defence

| Failure | Defence |
|---|---|
| The battle is on screen, so slack is small everywhere | GPU chronon mode; then less speculation; then lower time acceleration; never a hitch. Ladder rung: dense on-screen battle. |
| The forecast is wrong in the tail | Bounded units and buffers sized for the tail; correctness never depends on forecasts. Ladder rung: sabotaged forecasts. |
| A war merges regions until one exceeds a core | Chronon mode parallelises inside a tick; light-travel look-ahead splits large regions spatially. |
| A region never observed lags forever | Allowed: it is causally invisible. Its slack still shrinks with time, so it is renewed before anyone can notice. Its state stays compressed. |
| Speculation wastes the machine | Limited to headroom, ranked by value × probability; the waste ratio is measured. |
| Scheduling changes the world | Purity plus integer lattices; invariance rungs for budget, cores, GPU, mode and speculation. |
| Memory runs out | Bytes are budgeted; derived, reconstructible data is evicted first; family, cluster and response compression is preferred. |

## What this replaces in today's engine

| Today | Replacement |
|---|---|
| Global clock | Per-region frontiers |
| Global look-ahead window | Per-certificate expiry (cell exits, boundary promises) |
| Per-event re-survey of every box, island and pair | Local neighbourhood renewal |
| Operation counts as budget | Bounded pure units plus time-boxed frames |
| One core | Performance cores, efficiency cores and the GPU (Metal) |
| Exact fractions | Integer lattices |

## How it grows

| Future need | How it fits |
|---|---|
| Gravity | Field certificates (multipole or response valid until a source change arrives), with deadlines from their light cones |
| Agents, societies, AI factions | Agents are observers too (their decisions create deadlines) and regions (behaviour summaries as certificates, refined when a distinction matters) |
| Multiplayer | More observers, more hard deadlines; the same rule |
| History and archive | Sealed certificates evicted to cold storage, reconstructed on demand |
| Rendering and semantic zoom | The camera requests representation detail; causality alone decides what physics must resolve (design bible point 56) |
| Procedural generation | Detail is generated when a certificate needs it, keyed by seed and identity |

## How we will know

Scale-ladder rungs added for this plan:
- a dense battle on screen;
- a battle off screen while the player idles;
- sabotaged forecasts;
- speculation on vs off;
- 1 vs 8 cores;
- CPU vs Metal;
- event vs chronon mode;
- the memory wall.

Each reports the frame tail, slack misses, useful-work ratio and utilisation, and gates on identical digests.

## Build order

1. Local event core in integer lattices (single core); gas and pile-up rungs must pass.
2. Bounded units, time-boxed frames, snapshot publishing, per-region frontiers and slack.
3. Forecasts and the least-slack queue; monitoring on every rung.
4. Multiple cores (performance/efficiency split), with core-count invariance.
5. Metal chronon mode and GPU index building, with CPU/GPU invariance.
6. Speculation and recompression in idle time.
7. Gravity field certificates on the same queue.

## When is a messy estimate worth it?

A forecast is itself compute. It earns its place only when all of these hold (Russell and Wefald's value of computation, with Fermi's rule of thumb):

1. **Does the choice matter?** The best option must differ from the default by far more than the estimate costs.
2. **Are we unsure?** If the answer is already known to a factor of two, estimate no further.
3. **Is it cheap?** The estimate should cost under ~1% of the work it steers. Kinetic-theory rates from region densities and speeds are O(regions), not O(ships).
4. **Is a wrong guess cheap to undo?** Pure units make most mistakes free (discard and redo). Then act and measure, instead of planning.
5. **Does it repeat?** Choices made millions of times (representation per region, speculation targets) are worth learning a cheap rule for. One-off choices are not.
6. **Can a wrong guess cause ruin?** Then never gamble: take the deterministic safe path. Forecasts never touch correctness.

**MCTS.** The allocator's core is not an exploration problem: slack and costs are known well enough, so least-slack order needs no search. The only real exploration/exploitation choice is where to speculate with spare capacity (where will the player go or look?). There a cheap predictor (heading, history) plus a bandit that learns speculation hit rates is enough. MCTS rollouts would cost as much as the simulation they try to save. MCTS may still earn a place later as deterministic, seeded planning inside AI factions, which is gameplay, not allocation.

**Neural Engine (M1: 16 cores, ~11 TOPS at low precision, reachable only through Core ML).** It is not bit-reproducible across devices and OS versions and uses low precision, so it can never compute the world. It can advise:
- learned cost forecasts;
- player-intent prediction for speculation;
- rendering (upscaling, denoising).

It fits wherever a wrong answer costs speed, never correctness.

## The player's influence is bounded by a light cone

After genesis, the player is the only source of new information: AI factions and every other agent are seeded and deterministic. Every player action (a burn, a message, a launched probe, a trade) starts on the player's worldline and spreads at most at c. So:

- **Outside the future light cone of the player's present moment, the world is already fixed.** Computing there is never speculative and never wasted, however far ahead. This holds for every possible future action, because all of them happen inside that cone.
- **Inside the cone, results are provisional only where an actual action's own cone reaches.** Most of the inside is untouched in practice, because a single ship's influence is small and local. An action invalidates only its own cone from the moment it is taken, as in step 6 of the example below.
- **Actions arrive at human rate,** so repair is triggered rarely, and each repair is local.
- **Speculation targeting may use the Neural Engine.** It only chooses what to precompute; the precomputation itself runs deterministically on CPU and Metal, so the world stays bit-exact.

## Share codes: store consequences, not keystrokes

A code must carry exactly the information needed to rebuild the state, given the shared decoder (engine + dictionary). The world itself is its seed: ~36–48 bits, 4 words including a checksum word that also pins the edition (`turing newton light vega`). The hard part is what the player added. First principles:

- **Only consequences are information.** Two input histories are equivalent when every observer-receivable fact they produce is identical. The code needs only the shortest member of that equivalence class, not the recorded keystrokes.
- **The engine finds the shortest member, like a compiler optimising a program,** and verifies it by replay:
  - *dead-code elimination*: an order overwritten before any effect reached anyone is dropped;
  - *fusion*: consecutive commands with no observable consequence between them merge ("left, left, left" becomes one turn);
  - *commutation*: actions whose effects never meet can be listed as an unordered set, which saves log₂(n!) bits (the causal structure says exactly which ones commute);
  - *timing coarsening*: each action keeps only the time precision that changes some outcome.
  
  Every candidate is accepted only if replay reproduces the same observable state.
- **Then entropy-code what remains against the engine's own predictions.** Predictable choices ("continue", "go where you were heading", "repeat") cost almost nothing; surprising ones pay their log₂(1/probability).
- **The floor is honest.** A short what-if or a single decisive act fits in a few words. A long campaign contains genuinely many consequential decisions (Shannon) and becomes a file, or a 5-word registry hash where it was published.

| Code | Contents | Size |
|---|---|---|
| World | seed + edition/checksum | 4 words |
| Bookmark | + ranked landmark + log-scale time | ~6 words |
| Changed world | + minimal consequential history, entropy-coded | a few words per truly new decision |
| Campaign | registry hash or file | 5 words or a file |

Integer lattices make every code reproduce on any Mac. Every ladder failure and bug report emits a code that reproduces it.

## Worked extreme example

- The player is flying at 0.99c (γ ≈ 7.1) toward the Orion Gate, 50 light-years away.
- At the Gate, two fleets of 10⁸ ships each will meet in one year of world time and fight for a year.
- 30 light-years behind the player, a probe is steering an asteroid that will hit or miss a colony in 200 years.
- The player has just messaged a faction 20 light-years away.
- The rest of the galaxy is ~10¹⁰ ships in ~10⁴ groups.
- The game runs at 1 ship-day per real second.

1. **Everything is claims.** Quiet groups hold "no contact for millions of years": zero work. Each fleet is a few group claims that expire when the fleets' envelopes meet. The message is one claim expiring on arrival. The asteroid is one claim on its hit/miss margin.
2. **Deadlines come from light cones.**
   - The war begins at world year 1. Its light and the player close at 1.99c, so they meet around world year 25.6. That is ≈ 3.6 years of ship time, ≈ 1,300 real seconds. **The war has 22 minutes of slack before a single photon of it can reach the screen.**
   - The approach Doppler factor (≈ 14) means the player will then see that year-long war in about 26 real seconds, so all of it must be finished by then.
   - The asteroid and the message have decades of slack: efficiency-core background work, or nothing until arrival.
3. **The forecast costs two numbers.** From fleet density and relative speed (kinetic theory): ~1% of 2×10⁸ ships at the front, ≈ 2×10⁶ active ships × ~10 neighbour checks ≈ 2×10⁷ checks per tick ≈ 2 ms per tick on Metal. The war lasts 3.15×10⁷ one-second ticks ≈ 17 hours. **The forecast is ≈ 50× over its 22-minute slack.** It knows this 22 minutes before any frame is at risk.
4. **The rules respond:**
   - the fleets' interiors stay group claims (only the front is individual);
   - the war region gets Metal and the efficiency cores go to background work;
   - speculation elsewhere pauses.
   
   If it still does not fit, the frame never hitches: when the deadline arrives, time acceleration drops so the player's approach slows until the engine catches up. The real lever is representation. The collision outcomes are canonical (who survives, where wreckage lies), so they cannot be dropped. An aggregate combat law, with a declared bounded error and detail regenerated consistently when someone later looks closer, is the multiplicity principle applied to war. **This is an open law-design problem, to be qualified on the ladder like gravity.**
5. **The player turns around at ship-year 2.** The war's light now chases a receding player, so its deadline moves thousands of years out and war work drops to the background. Everything already computed stays valid, because the world never depends on where the player looks. Only the priorities changed.
6. **The player fires a relativistic projectile into the war.** Its light cone reaches the Gate at a known time. War results before that time stay committed; only the part inside the cone is recomputed.
7. **Throughout,** each frame draws the committed past light cone and never waits.

## Appendix — how this plan was derived

Ten passes, each probing one layer through one lens and required to change the plan; then three simplification passes.

| Pass | Layer | Lens | What changed |
|---|---|---|---|
| 1 | Unit of work | Musk: question requirements, delete | Work must name the certificate and deadline it protects; useful-work ratio becomes a metric; global windows, global re-surveys and the global clock are deleted |
| 2 | Arithmetic and determinism | von Neumann (error structure); Julien's quanta | Units become pure; *what* is separated from *when and where*; integer lattices make re-execution, speculation and work stealing free |
| 3 | Locality | Physics; event-driven gas simulation | Regions exchange boundary certificates; cell exits and boundary promises become the same mechanism |
| 4 | Forecasting | Fermi; Asimov; Taleb on confidence | Per-region Fermi cost estimates with confidence bands, scored against measurement; planning uses the tail, never the mean; forecasts never affect correctness |
| 5 | Time | Light cones; Goldratt; EDF | Deadlines come from light cones and propagate through dependencies; least-laxity-first; "critical region" defined as least slack × forecast cost; observers generalised beyond the player |
| 6 | Tails | Taleb: barbell, via negativa, antifragility; Kelly | Paranoid frame core plus aggressive speculative edge; four exposures removed (unbounded units, world-size work, unbounded regions, forecast-dependent correctness); spikes feed back into the forecasts |
| 7 | Hardware | Musk's first principles; von Neumann bottleneck | Shape-to-hardware mapping (GPU/Metal, performance cores, efficiency cores); render first on the GPU; bytes moved become a budgeted cost |
| 8 | Information | Shannon; Russell and Wefald | Value of computation ranks ties and speculation; recompression treated as an investment; distinctions per second becomes the health metric |
| 9 | Scale | Asimov; scale-free rules; Musk's "best part is no part" | One interface and one rule at every level; aggregates stand in until a distinction matters; new features become certificate kinds |
| 10 | Verification | Feynman; skin in the game; Lindy; Chesterton | Invariance rungs including sabotaged forecasts; components carry measured cost and error; proven algorithms; old engine kept until the ladder passes |

| Simplification | What merged |
|---|---|
| S1 — delete concepts | Events, cell exits, boundary promises, overlap guarantees, field validity and scheduled commands are all certificates with an expiry. One hierarchical queue replaces the separate event queue and region scheduler. |
| S2 — unify choices | Representation, execution mode and hardware all follow from one number: certificate lifetime relative to cost (κ). Semantic zoom, the event/chronon choice and the CPU/GPU choice become the same decision. |
| S3 — minimise | Three primitives (certificate, slack, unit) and one sentence. Everything else in this document is derived from them. |
