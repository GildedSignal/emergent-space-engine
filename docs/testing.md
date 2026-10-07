# Testing: finding out fast that we are wrong

**Draft for Julien's validation (7 October). Not in force until he approves it.** Once approved, it absorbs [test-ladder.md](test-ladder.md), and AGENTS.md's "Evidence" and "Tests" bullets become one pointer here.

Julien, 7 October:
- "prevent big mistakes or many small ones", "on average, amortized";
- "it's really about epistemology … unknown unknowns of interactions so knowing what to test too matters tremendously";
- tests "reduce the time towards detecting when we're fooling ourselves, not to prevent issues, move fast break fast".

## The idea

Everything we already do is a conjecture meeting a refutation: a gate, a rung, a lab run, a red-team, Julien's flight. This protocol is their shared grammar, not a new activity.

A check exists to shorten the time between fooling ourselves and knowing it. Its measure is **detection latency**: from the change that introduced a mistake to the check that caught it.

The protocol names no files, mechanisms or number formats. Those change; the protocol does not.

## The loop

It applies to any change, at any scale.

1. **Conjecture.** In one sentence: what does this change make true? If it cannot be said, the change is not understood yet.
2. **Exposure.** What will be built on it, and how hard is it to undo? This decides the end of the barbell.
3. **Fastest refuter.** Find the cheapest observation that would come out differently if the conjecture were false. Look where the information is (below).
   - Prefer a generator to a case.
   - Prefer a property to an example.
   - Prefer the existing harness to a new one.
4. **Proof it can fail.** Plant the fault it is meant to catch. A refuter that misses its plant is a control.
5. **Placement.**
   - Cheap: the inner loop.
   - Expensive: the lab or the background.
   - One-way: the door.
6. **Aftermath.**
   - A surprise stops the work until it is explained.
   - An escape is named by its family, gets the family's generator, and fixes the process step that let it through. Its latency is recorded.

## What a check can know

1. **It refutes; it never proves.** We know what is wrong far better than what is right (Popper, via Taleb). The instrument can also lie.
2. **A pass is worth only the check's proven ability to fail** (Novella on absence of evidence).
3. **Risk lies in exposure, not in past bug counts** (Taleb).
4. **A result holds only inside the range it was observed in** (Schmidt-Nielsen). When a regime changes, its old evidence expires: Ariane 5 flew on Ariane 4's ranges.
5. **Agreement is not independence.** Independent authors fail on the same hard inputs (Knight and Leveson). Coding agents do too, clustered where the spec is ambiguous (2026). Independence needs a different method, and an unambiguous spec is itself a check.
6. **Plans fail by tunnelling** (Taleb). Some inputs must come from outside the plan.
7. **A partial failure that "passed" is a failure** (Challenger's normalisation of deviance). A known red is a ratchet with an owner. It may only improve, and it is never called a pass.

## Where to look

| Quadrant | What it is | Refuted by |
|---|---|---|
| Known knowns | the law's invariants | assertions at the source, in every run and every flight |
| Known unknowns | named risks | gates and ladders |
| Unknown unknowns | interactions nobody named | generators (next section) |
| Unknown knowns | steers given and not followed | the register: a steer given twice and not followed is a failed check |

Information concentrates in five places:
1. **Where behaviour changes kind** (Strogatz's bifurcations). Physics has its edges, such as capture, the last stable orbit, plunges and β → 1. Every finite resource of the representation (a word, a budget, a frame's boundary) is an edge too. Test both sides of each, in dimensionless numbers.
2. **Where mechanisms meet.** With many parts, almost everything that drives behaviour is interaction (Bevelin). Extremes come from forces combining (Munger's lollapalooza). The unit of a check is a combination.
3. **Where slow layers meet fast ones.** Slow constrains quick (Brand). Effort scales with how slow a layer is, and checks cross interfaces rather than reading internals, so fast layers stay free to change.
4. **Where owners meet** (ASML; Mars Climate Orbiter). Interfaces carry their units in types and a contract checked from both sides.
5. **Where the instrument could lie:** domains, shared harnesses, stale builds.

## Generators for unknown unknowns

None of these needs a prediction.
1. **Fragility** (Taleb's asymmetry test). Perturb a passing scene by δ and by 2δ. If the harm is convex, the scene is fragile there, pass or not.
2. **Combinations.** Covering arrays put every pair of mechanism regimes into some scene, in tens of scenes instead of tens of thousands. Field data says most interaction faults involve two or three factors.
3. **The small scope** (Alloy). Most bugs have small counterexamples, so enumerate every case within a small bound, especially orderings.
4. **Rare made common** (FoundationDB, SQLite). In checks, shrink every finite resource and force the rare branches, so that limits are hit on every run instead of once a year of play.
5. **Swarm and symmetry.** Switch random subsets of mechanisms on. Use symmetries, which hold for every input, including inputs nobody imagined.
6. **Outside the plan.** Random scenes, red-teams, and the player. Replay is exact, so each recorded flight is a regression check for free.

## The barbell

A check earns its place when p(it catches) × cost(the escape) exceeds its cost. An escape costs more the further it travels: a 1° heading error misses by a mile every 60 miles.

**Cheap end.** On every change, in seconds:
- assertions;
- replay digests;
- symmetries;
- small generators with fresh seeds each run. Failures are shrunk and kept forever, so millions of seeds a week are paid in slices.

The inner loop stays under a minute on the M1. A check that outgrows a few seconds moves to the lab, or goes.

**Expensive end.** At one-way doors only:
- freezing a law or a gate;
- merging a law change;
- changing a number format or a digest;
- a build Julien will fly.

There run:
- frozen gates with planted faults and controls;
- a premise-first red-team;
- the worst case over many seeds;
- ladders climbed until one fails;
- the bigger generators;
- judges using another method;
- cost measured heat-soaked on the M1.

**Cut:**
- checks that pin implementation;
- float snapshots;
- golden numbers the code cannot regenerate;
- checks that cannot fail;
- coverage as a target;
- duplicated checks;
- reading one failure as a method's death (H0183).

## Stolen from fields that cannot break

They have skin in the game, so their heuristics are tested by consequences. The details are in the [dossier](../artifacts/evidence/critical-software-testing-20261007/README.md).
- **Stop at the first abnormality** (Toyota, Erlang, JPL's assertion density). Never carry on with corrupt state.
- **A simple monitor beside the clever channel** (Airbus; trading risk checks).
- **Make illegal states unrepresentable** (Jane Street). The compiler is the fastest check.
- **Differential checks** between two implementations on random inputs (Csmith; SQLite).
- **Deterministic simulation, accelerated time, one seed replays all** (TigerBeetle, FoundationDB).
- **Prototypes break; crewed vehicles do not** (SpaceX). Branches and the lab break fast; the law and main do not.
- **Error budgets** (Google SRE). When escapes rise, check effort rises; otherwise ship.
- **A change of regime voids the old analysis** (Ariane 5, the 737 MAX).
- **Never drop an independent check when adding a clever one** (Therac-25).
- **Fix the process step that let an escape through** (the Shuttle group). Log near-misses too (ASRS).

**Not stolen:** paperwork, coverage targets, whole-system proofs, N teams on one method, requirements frozen up front.

## Not busy work

- Every check carries one line: its conjecture, its planted fault, and its cost. A check missing any of the three goes.
- Reports are verdict lines. Nobody writes about checks.
- One generator replaces a suite of cases.
- **No retrofit campaign.** The protocol applies to the next gate, merge or escape. An old check is touched only when it fails, slows the loop, or meets the delete pass at a phase's end.
- Generators and long runs use the lab's and agonbox's time, never the integrator's.
- **The protocol is itself a conjecture.** If detection latency does not fall, or the inner loop outgrows its minute, the protocol is cut back.

## How it fits what we already do

| What exists | Its place in the loop |
|---|---|
| Frozen gates with planted faults | refuters of the law at one-way doors (steps 3–4) |
| Ladders | claims of range, climbed until one fails |
| GLM lenses with independent checkers | where the generators run, out of the integrator's time |
| Premise-first red-teams | refuters of the premise before a freeze |
| Judges from another family | independence; from now on, also another method |
| Julien's flights | the outside-the-plan generator; recorded and replayed |
| Correction entries in the journal | escape records, now with their latency |
| The register and the drift rule | the refuter of unknown knowns |
| HANDOFF's "In flight" | known reds, held as ratchets with owners |

## On approval

Three changes, because each removes work rather than adding it:
1. Merges stop on red, mechanically.
2. Correction entries record detection latency.
3. The generators become lab lenses.

Then test-ladder.md folds in, and AGENTS.md gets one pointer. Everything else applies as the work comes.

**Sources:**
- Julien's books: Taleb's *Incerto*; Bevelin's *Seeking Wisdom*; *Poor Charlie's Almanack*; Strogatz's *Nonlinear Dynamics and Chaos*; Brand's *How Buildings Learn*; Hijink's *Focus: The ASML Way*; Schmidt-Nielsen's *Scaling*; Juarrero's *Dynamics in Action*.
- His highlights: Novella; Farnam Street; Waitzkin; Feynman; Kahneman.
- The critical fields: the [dossier](../artifacts/evidence/critical-software-testing-20261007/README.md).
