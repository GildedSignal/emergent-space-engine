# Testing: what to test, and how cheaply

**Draft for Julien's validation (7 October). Not in force until he approves it.** Once approved, it absorbs [test-ladder.md](test-ladder.md), and AGENTS.md's "Evidence" and "Tests" bullets shrink to a pointer here.

Julien, 7 October:
- tests "prevent big mistakes or many small ones", "on average, amortized", "maybe barbell tests?";
- then: "it's really about epistemology but also it needs to work for unknown unknowns of interactions so knowing what to test too matters tremendously".

## 1. What a test can know

1. **A test refutes; it never proves.** We know what is wrong with far more confidence than what is right (Popper, via Taleb and Bevelin).
   - Every test is an attempt to refute a named conjecture. Its kill criterion is written before it runs.
   - The instrument can itself be wrong, and so give a false "no".
2. **A pass is evidence only in proportion to how hard and how sensitively we looked** (Novella). A test that has never failed a planted fault proves nothing by passing. Its sensitivity is measured, not assumed.
3. **Risk lives in the future, not in past bug counts** (Taleb). Choose tests by exposure (what breaks, and what is built on top, if this is wrong), not by how often bugs showed up there.
4. **A result holds only inside the range it was observed in.** Extrapolating beyond it is perilous: the constraints out there are unknown by definition (Schmidt-Nielsen).
   - Every oracle and gate states its domain.
   - Every claim carries the range it was tested on.
   - "It scales to 10⁹" is a rung to climb, not a result.
5. **Agreement is not independence.** Backups that share a defect fail together (Bevelin). Runs that share a harness count as one.
6. **Plans fail by tunnelling:** they neglect uncertainty from outside the plan (Taleb). So some test inputs must come from outside the plan: random, adversarial, or the player.

## 2. Knowing what to test

The four quadrants, and what each gets:

| Quadrant | Here | What it gets |
|---|---|---|
| Known knowns | the law's invariants: exact registers, key order, conservation | asserted always (section 4, left end) |
| Known unknowns | named risks: the board's bottlenecks, red-team findings | targeted gates and ladders (section 4, right end) |
| Unknown unknowns | interactions nobody has named | structure and exposure, never prediction (section 3) |
| Unknown knowns | things we know and ignore (Julien asked for FMM 18 times; H0196) | the register, and the drift rule: a steer given twice and not followed is a failed test |

Aim where the information is. Six places, in order:

1. **Where the behaviour changes kind** (bifurcations, Strogatz). The bulk of a regime is cheap and boring; the topology of the motion changes at its edges. Our edges:
   - the innermost stable orbit;
   - capture at L = 4M;
   - the ergosphere;
   - plunges;
   - e ≈ 1 flybys;
   - β → 1;
   - a doll's boundary;
   - exact ties;
   - a register's word limit.

   Test on both sides of each edge and at it. Map these edges in the dimensionless numbers: non-dimensionalising cuts the parameters to the few that matter.
2. **Where mechanisms meet.**
   - Interactions grow faster than parts. With five parts per subsystem, 82% of what drives the behaviour is interactions; with a hundred parts, 99% (Bevelin). A mechanism tested alone covers the small remainder.
   - Extreme outcomes come from several forces acting together, often past a breakpoint (Munger's lollapalooza).
   - So the unit of testing is a combination, not a feature.
3. **Where slow layers meet fast ones.** Slow constrains quick (Brand's shearing layers): the law, then the engine, then the view.
   - Test effort scales with how slow a layer is. The law gets the right end. The view gets almost nothing: Julien flies it.
   - Test across a layer's interface, never its internals, so fast layers can change without breaking tests.
4. **Where owners meet.** Integration is where problems begin. ASML: when the lens supplier says the lens is ready, the real trouble starts. Every interface between two agents' modules gets a contract test from both sides.
5. **Where the instrument could lie:** oracle domains, shared harnesses, stale binaries.
6. **Every claim beyond its tested range:** it becomes a rung.

## 3. Unknown unknowns of interactions

We cannot list them, so we test structure and exposure. All six methods are model-free.

1. **Fragility probes** (Taleb's asymmetry test).
   - Perturb a passing scene by δ and by 2δ along each dimensionless number.
   - If the harm (error, cost, refusals) grows faster than linearly, the scene is fragile there, even though it passes.
   - This finds a hidden interaction without naming it, and turns "it passes" into "how far is it from failing". Cost: three runs per dimension.
2. **Combinations by covering arrays.** List the mechanisms with a few regimes each:
   - thrust level;
   - doll transition;
   - tie;
   - spin;
   - gravity's news;
   - belt;
   - encounter;
   - observation;
   - replay;
   - partition.

   A pairwise covering array puts every pair of (mechanism, regime) into some scene. That takes about 15–20 scenes instead of 3¹⁰ = 59,049. Field data on real faults (outside the library) says most interaction faults involve two or three factors. Pairs run on the left end; triples, a few dozen scenes, run on the right. The 6 October regression was one such pair: the v2 clock and a burn held across a handoff.
3. **Swarm scenes.** Each random scene turns a random subset of mechanisms on. Mechanisms can mask each other's bugs, so all-on is not the hardest case.
4. **Commuting squares** (from the math memo). Symmetries hold for every input, including inputs nobody imagined.
5. **Generators from outside the plan.**
   - Random scenes, red-teams, and the player.
   - Every flight of Julien's is a log of decision bytes, and replay is exact. So every flight is saved as a regression test, for free.
   - Our best source of unknown unknowns is the person flying. ASML reports that half a machine's problems could not have been imagined before the factory floor.
6. **Escapes become classes.** For each escape, ask what family it belongs to and where the other members are. Add the family's generator, not the single case. Keep a checklist of standard causes (Munger).

## 4. The economics: a barbell

A test earns its place when **p(it catches) × cost(the mistake escaping)** exceeds **its cost** (writing it, every run, upkeep, false alarms).

An escape costs more the further it travels before it is caught: a 1° heading error misses by a mile every 60 miles. So:
- cheap checks run close to every change;
- expensive checks run where an escape would be ruin;
- the middle is cut.

**Left end: always on, seconds, every commit.** It catches the many small mistakes.
- The law's invariants are asserted where they live, exactly, with no tolerances.
- Digest replay: one hash compares the whole state.
- Commuting squares: relabel, translate, re-partition, reschedule, sparse against dense, observed or not.
- Rotating seeds:
  - fresh seeds each run, at small sizes, from a logged stream;
  - any failure is shrunk to its smallest seed, which is kept forever;
  - over a week this covers millions of seeds: the expensive search, paid in slices.
- The pairwise scenes.
- The scripted flight: L15 to β 0.999, an orbit, a flyby, a crash with its reason.
- Mechanical stops:
  - the merge command refuses on red;
  - a red main stops the line: revert first, fix second;
  - only a test's owner may weaken it, with a journal line.
- **Budget:** at most 60 s on the M1 for the touched crate, build included. A test over 5 s moves right or is cut. Today `motion.rs` (20.5 s) and `plane.rs` (17.7 s) take 80% of the universe suite's 48 s.

**Right end: rare, adversarial, at one-way doors only.** A one-way door is:
- freezing a law or a gate;
- merging a law change;
- changing a number format or a digest;
- a build Julien will fly.

There, decide slowly; branches, lab runs and view tweaks are two-way doors, decided fast. The right end consists of:
- gates frozen before their first run, each with planted mutants that must fail it and a control that must pass it;
- a premise-first red-team and the cheapest falsifying probe before any freeze;
- many seeds, judged at the worst case and the tail, never the mean;
- ladders climbed 10× per rung until one fails, with extreme and chaotic rungs;
- triple-wise and swarm scenes;
- fragility maps along each dimensionless number;
- judges from another model family with another harness: whoever builds a module never certifies it (segregation of duties);
- hours of simulation fuzzing on agonbox, where x64 Linux digests must equal the Mac's;
- cost gates run on the M1, heat-soaked.

The integrator reads verdicts only.

**The middle we cut:**
- tests that pin implementation details: they break on every change of representation, the change we most need;
- float snapshots and tuned tolerances;
- golden numbers the code cannot regenerate;
- tests that cannot fail;
- coverage targets;
- the same check duplicated across modules;
- slow tests in the inner loop;
- reading one failure as a method's death: a failure kills a configuration (H0183, H0196).

**The delete pass, at each phase end.** Every test names the mistake it prevents and a mutant it kills, or it goes. Musk's rule: if a tenth of what you deleted never has to come back, you did not delete enough.

## 5. What has actually hurt us

| When | Mistake | Quadrant | What would have caught it |
|---|---|---|---|
| H0156 | 10B ships "passed": every group shared one velocity | a test that could not fail | a planted case that must fail |
| H0189 | A lower-tier patch rewrote a principle; the review checked scope, not meaning | unforced | the owner reviews meaning |
| H0196 | One quadrupole failure was read as "FMM banned"; gravity drifted through four framings | unknown known | the register and the drift rule; a kill names the configuration it kills |
| 5 Oct | The lab's "memo hits 95–98%": five runs, one harness | agreement without independence | an independent harness |
| 5 Oct | E6 was judged with a stale mutant binary | the instrument lied | judges built from source, printing their hash |
| 5 Oct | B12 could not tell planted-bounded from planted-compound | insensitive gate | controls on both sides, at freeze |
| 5 Oct | B12/B13 references passed inside the planet | oracle outside its domain | the oracle asserts its own domain |
| 6 Oct | The v2 clock met a held burn across a handoff, at β → 1; the assertion was weakened and the merge chained | interaction at a bifurcation | a pairwise scene; never weaken; the merge stops on red |

None needed a slower test. Each needed a test that can fail, an independent instrument, a mechanical stop, or a scene that combines mechanisms at an edge.

## 6. Who does what

Builders write the left end with their code; the judge's family builds the right end; GLM runs fuzzing, red-teams and fragility maps; the integrator reads verdicts and merges only through the stopping merge command; lower tiers never weaken a test.

## 7. If approved, the changes

1. An `xtask` merge command that runs the touched suites and refuses on red.
2. Rotating seeds, plus a kept-seed file, in `behave`'s sampler and in the property tests.
3. The edge map: the plane's bifurcations in dimensionless numbers, each tested on both sides (Sonnet; Opus checks the list).
4. Pairwise covering scenes over the ten mechanisms on the left end; triples and swarm on the right (GLM explores, Sonnet builds).
5. Fragility probes in `behave` (δ and 2δ along each number), reported as convexity next to pass/fail.
6. The flight recorder: the page saves each of Julien's flights as a replayable regression log.
7. Contract tests at every interface between two owners.
8. Commuting-square digest tests, and agonbox digest parity on every push to main.
9. Split `motion.rs` and `plane.rs` into fast and slow parts. A delete pass lists every test that kills no mutant.
10. test-ladder.md folds into this file, and AGENTS.md's test bullets become one pointer.

## Sources

**Julien's books (Reader):**
- Taleb, *Incerto*: falsification, silent evidence, tunnelling, fragility as asymmetry, redundancy.
- Bevelin, *Seeking Wisdom*: interactions outnumbering parts, dependent backups, "assume I'm wrong, how will I know?".
- Munger, *Poor Charlie's Almanack*: lollapalooza effects, checklists, inversion.
- Strogatz, *Nonlinear Dynamics and Chaos*: bifurcations, non-dimensionalising.
- Brand, *How Buildings Learn*: shearing layers.
- Hijink, *Focus: The ASML Way*: integration, managing errors rather than preventing them, the factory floor.
- Schmidt-Nielsen, *Scaling*: no extrapolation beyond the observed range.
- Juarrero, *Dynamics in Action*: wholes constrain their parts, so parts tested alone miss the whole.

**His highlights (Readwise):** Novella (absence of evidence); Farnam Street (reversible against irreversible decisions, the 1° heading, the map is not the territory); Waitzkin (the error spiral); Feynman (you are the easiest person to fool); Kahneman (the speed and quality of feedback); Kaufman (segregation of duties); Isaacson's *Elon Musk* (delete, then add back); Ultralearning and Make It Stick (directness).

**Outside the library** (practitioners with skin in the game): NIST's combinatorial-testing data on how many factors real faults involve; swarm testing (Groce and Regehr); deterministic simulation (FoundationDB, TigerBeetle); shrinking (QuickCheck, Hypothesis); mutation testing; Toyota's andon cord.
