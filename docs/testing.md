# Testing: detecting fast when we fool ourselves

**Draft for Julien's validation (7 October). Not in force until he approves it.** Once approved, it absorbs [test-ladder.md](test-ladder.md), and AGENTS.md's "Evidence" and "Tests" bullets shrink to a pointer here.

Julien, 7 October:
- tests should "prevent big mistakes or many small ones" and be "on average, amortized";
- "it's really about epistemology … unknown unknowns of interactions so knowing what to test too matters tremendously";
- tests "reduce the time towards detecting when we're fooling ourselves, not to prevent issues, move fast break fast".

**The purpose.** A test buys a shorter time between fooling ourselves and knowing it. It does not buy the absence of issues.
- **The metric is detection latency:** from the commit that introduced a mistake to the run that caught it. Every correction entry records it.
- **The ranking so far:**
  - The slowest catch was an unknown known: gravity drifted for weeks (H0196).
  - Next came a tunnelled one: the lab's shared harness went unnoticed overnight.
  - The fastest are tests that can fail, measured in seconds.

The full study of how critical fields test is in the [dossier](../artifacts/evidence/critical-software-testing-20261007/README.md).

## 1. What a test can know

1. **A test refutes; it never proves.** We know what is wrong far better than what is right (Popper, via Taleb and Bevelin). Each test refutes a named conjecture, and its kill criterion is written first. The instrument itself can lie.
2. **A pass is worth only the test's proven ability to fail** (Novella on absence of evidence). A test that never failed a planted fault proves nothing by passing.
3. **Risk lies in exposure, not in past bug counts** (Taleb). Aim where an error would cost the most and where the most is built on top.
4. **A result holds only inside its observed range** (Schmidt-Nielsen).
   - Every oracle and gate states its domain.
   - Every claim carries its tested range.
   - When a regime changes, old evidence expires. Ariane 5 flew Ariane 4's velocity range, and so did our v2 register.
5. **Agreement is not independence.**
   - Backups that share a defect fail together (Bevelin).
   - Independently written versions fail on the same hard inputs (Knight and Leveson). Coding agents repeat this, clustered on ambiguous parts of the spec (2026).
   - So a judge uses a different method, not only a different model, and an unambiguous spec is itself a test.
6. **Plans fail by tunnelling** (Taleb). Some inputs must come from outside the plan: random, adversarial, or the player.
7. **A partial failure that "passed" is a failure** (Challenger: normalisation of deviance). Every surprise is a stop until it is explained. A known red gate is a ratchet that may only improve; it is never described as passing (B13 at 60/64).

## 2. Knowing what to test

| Quadrant | Here | What it gets |
|---|---|---|
| Known knowns | the law's invariants | asserted always, at the source |
| Known unknowns | named risks: bottlenecks, red-team findings | targeted gates and ladders |
| Unknown unknowns | interactions nobody named | structure and exposure (section 3) |
| Unknown knowns | steers ignored (FMM asked 18 times; H0196) | the register; a steer given twice and not followed is a failed test |

Aim at, in order:

1. **Where behaviour changes kind** (Strogatz's bifurcations). Our edges:
   - the innermost stable orbit;
   - capture;
   - the ergosphere;
   - plunges;
   - e ≈ 1;
   - β → 1;
   - a doll's boundary;
   - ties;
   - a word's limit.

   Test on both sides of each edge, mapped in dimensionless numbers.
2. **Where mechanisms meet.** With 100 parts per subsystem, 99% of what drives behaviour is interactions (Bevelin). Extremes come from forces combining past a breakpoint (Munger's lollapalooza). The unit of test is a combination.
3. **Where slow layers meet fast ones.** Slow constrains quick (Brand): the law, then the engine, then the view. Effort scales with how slow a layer is. Test across interfaces, never internals.
4. **Where owners meet.** Integration is where problems begin (ASML). Units go into types at interfaces (Mars Climate Orbiter). Every interface between two agents' modules gets a contract test from both sides.
5. **Where the instrument could lie:** domains, shared harnesses, stale binaries.
6. **Any claim beyond its range:** it becomes a rung.

## 3. Unknown unknowns of interactions

1. **Fragility probes** (Taleb's asymmetry test). Perturb a passing scene by δ and by 2δ along each dimensionless number. If the harm is convex, the scene is fragile there, even though it passes.
2. **Covering arrays.** Take ten mechanisms with three regimes each:
   - thrust;
   - doll transition;
   - tie;
   - spin;
   - gravity's news;
   - belt;
   - encounter;
   - observation;
   - replay;
   - partition.

   Pairwise coverage takes about 15–20 scenes instead of 59,049. Field data says most interaction faults involve two or three factors. The 6 October regression was one pair: the v2 clock and a burn held across a handoff.
3. **The small scope** (Alloy). Most bugs have small counterexamples, so enumerate every ordering of the events of at most four bodies within a bound. The cores that are hairy and sensitive to order get this treatment, where AWS used TLA+: ties, handoffs, gravity's cursor. AWS found a bug whose shortest trace was 35 steps.
4. **Make rare things common** (FoundationDB's BUGGIFY, SQLite's fault injection). Test knobs force:
   - ties;
   - worst-tick handoffs;
   - registers shrunk to a few bits;
   - tiny slice budgets.

   Edges that take years to reach in play are then hit every run.
5. **Swarm scenes:** random subsets of mechanisms switched on. **Commuting squares:** symmetries that hold for every input.
6. **From outside the plan:** random scenes, red-teams, and the flight recorder. Each of Julien's flights is a log of decision bytes, and replay is exact, so it becomes a regression test for free.
7. **Escapes become classes.** Find the family an escape belongs to and add its generator, not the single case. Fix the process step that let it through (the Shuttle group). Log near-misses, not only escapes (ASRS).

## 4. Stolen from fields that cannot break

| Field | Their heuristic | Ours |
|---|---|---|
| JPL, TigerBeetle, SQLite | dense assertions, on the positive and the negative space, kept on | the law asserts its invariants in every run and every flight; violations refuse with a reason |
| Toyota, Erlang | stop on the first abnormality; let it crash | never continue on corrupt state; fall back to the last good state |
| Airbus, trading risk checks | a simple monitor beside the clever channel | an envelope monitor (β < 1, signs, frames, ticks) outside the step |
| Jane Street | make illegal states unrepresentable | frames, exponents and ticks as types |
| Csmith, SQLite's SLT | random differential testing | sparse against dense, chronon against engine, on random scenes |
| TigerBeetle, FoundationDB | deterministic simulation, accelerated time, one seed replays all | overnight simulation fuzzing on agonbox; seeds kept |
| SQLite | "veryquick" per check-in, full per release | the barbell below |
| SpaceX | prototypes fly to learn; crewed vehicles do not break | branches and the lab break fast; the law, main and frozen gates do not |
| Google SRE | error budgets | a fooling budget: when escapes per window rise, test effort rises; otherwise ship |
| Ariane 5, the 737 MAX | a change of regime or authority voids the old analysis | when a range changes, each affected test's domain is re-checked |
| Therac-25 | never drop an independent interlock; plain messages | keep the old check when adding a clever one; the loss report is plain |

**Not stolen:** certification paperwork; coverage as a target (it is a tool for finding untested code); whole-system proofs (seL4's cost); N teams using one method; requirements frozen up front.

## 5. The economics: a barbell

A test earns its place when p(it catches) × cost(the escape) exceeds its cost. An escape costs more the further it travels: a 1° heading error misses by a mile every 60 miles.

**Left end: every commit, seconds.**
- Invariant assertions.
- Digest replay.
- Commuting squares.
- Pairwise scenes.
- Rare-made-common knobs.
- Rotating seeds: fresh seeds each run, failures shrunk and kept forever. Millions of seeds a week, paid in slices.
- The scripted flight (L15 to β 0.999, an orbit, a flyby, a crash with its reason).
- Mechanical stops:
  - the merge command refuses on red;
  - a red main stops the line, revert first;
  - only a test's owner may weaken it.

**Budget:** at most 60 s on the M1 for the touched crate, build included. A test over 5 s moves right or is cut. Today `motion.rs` (20.5 s) and `plane.rs` (17.7 s) take 80% of the universe suite's 48 s.

**Right end: at one-way doors only.** A one-way door is:
- freezing a law or a gate;
- merging a law change;
- changing a number format or a digest;
- a build Julien will fly.

What runs there:
- Gates frozen first, with planted mutants that must fail and controls that must pass.
- A premise-first red-team and the cheapest probe.
- The worst case over many seeds.
- Ladders climbed 10× per rung until one fails.
- Triple-wise scenes, small-scope enumeration and fragility maps.
- Judges of another family and another method.
- Overnight fuzzing on agonbox, with Linux digests equal to the Mac's.
- Heat-soaked cost gates on the M1.

**Cut:**
- tests that pin implementation;
- float snapshots and tuned tolerances;
- golden numbers the code cannot regenerate;
- tests that cannot fail;
- coverage targets;
- duplicated checks;
- slow tests in the inner loop;
- reading one failure as a method's death (H0183, H0196).

**The delete pass, at each phase end:** every test names the mistake it catches and a mutant it kills, or it goes.

## 6. What has actually hurt us

| When | Mistake | Pattern | Fast detector |
|---|---|---|---|
| H0156 | 10B ships "passed": one shared velocity | a test that could not fail | a planted case |
| H0189 | A principle was rewritten; the review checked scope only | unforced | the owner reviews meaning |
| H0196 | One failure read as "FMM banned"; four framings | an unknown known (weeks) | the register; kills name configurations |
| 5 Oct | The lab's "95–98%": one shared harness | agreement without independence | another method |
| 5 Oct | E6 judged with a stale mutant binary | the instrument lied | judges print their source hash |
| 5 Oct | B12 blind to its planted pair | an insensitive gate | controls on both sides |
| 5 Oct | B12/B13 references inside the planet | outside the domain | the oracle asserts its domain |
| 6 Oct | The v2 clock meets a held burn at β → 1; the assertion weakened; the merge chained | Ariane 5: a regime change | a pairwise scene; shrunk registers; the merge stops on red |

## 7. If approved, the changes

1. An `xtask` merge command that refuses on red.
2. Detection latency recorded in every correction entry.
3. Rotating, kept seeds in `behave` and the property tests.
4. The edge map in dimensionless numbers, each edge tested on both sides.
5. Pairwise scenes on the left end; triples and swarm on the right.
6. Small-scope enumeration of event orderings (ties, handoffs, the gravity cursor).
7. Test knobs that make rare things common: shrunk registers, forced ties, tiny budgets.
8. Fragility probes in `behave`, reporting convexity next to pass/fail.
9. An envelope monitor, and types for frames, exponents and ticks.
10. The flight recorder, so every flight becomes a test.
11. Contract tests between owners; commuting squares; agonbox digest parity.
12. Split `motion.rs` and `plane.rs`; a delete pass; test-ladder.md folds in; AGENTS.md gets one pointer.

## Sources

**Julien's books:**
- Taleb, *Incerto*.
- Bevelin, *Seeking Wisdom*.
- Munger, *Poor Charlie's Almanack*.
- Strogatz, *Nonlinear Dynamics and Chaos*.
- Brand, *How Buildings Learn*.
- Hijink, *Focus: The ASML Way* (the line: "It's not about preventing errors, but how well you manage them").
- Schmidt-Nielsen, *Scaling*.
- Juarrero, *Dynamics in Action*.

**His highlights:** Novella; Farnam Street; Waitzkin; Feynman; Kahneman; Kaufman; Isaacson's *Musk*.

**The critical fields:** in the [dossier](../artifacts/evidence/critical-software-testing-20261007/README.md), with links.
