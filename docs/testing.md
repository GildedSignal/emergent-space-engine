# Testing: the barbell

**Draft for Julien's validation (7 October). Not in force until he approves it.** Once approved, it absorbs [test-ladder.md](test-ladder.md), and the "Evidence" and "Tests" bullets in AGENTS.md shrink to a pointer here.

Julien, 7 October: tests should "prevent big mistakes or many small ones", be "on average, amortized", "maybe barbell tests?"

## The one rule

A test earns its place when **p(it catches a mistake) × cost(the mistake escaping)** exceeds **its cost** (writing it, every run, upkeep, false alarms).

The cost of an escape grows with how far the mistake travels before anyone sees it. A 1° heading error misses by a mile every 60 miles flown. Here, distance means what gets built on top: branches, gates, a law, Julien's flight.

So:
- Cheap checks run as close to every change as possible.
- Expensive checks run only where an escape would be ruin.
- A test that costs more than it catches is deleted.

The barbell follows from this rule rather than being imposed: escape costs are fat-tailed, and they track how hard a step is to undo.

## What has actually hurt us

| When | Mistake | Kind | Cheapest guard |
|---|---|---|---|
| H0156 | 10B ships "passed" because every group shared one velocity | a test that could not fail | a planted case that must fail |
| H0189 | A lower-tier patch rewrote a principle; it was merged after a scope-only review | unforced | the owner reviews meaning; diffs to principles are flagged mechanically |
| H0196 | One quadrupole failure was read as "FMM is banned"; gravity drifted through four framings | ruin (a good method killed) | every kill names the configuration it kills, never the method (H0183) |
| 5 Oct | The lab's "memo hits 95–98%": five runs shared one harness | agreement without independence | an independent harness; runs sharing one count as one |
| 5 Oct | E6 judged with a stale mutant binary | broken instrument | judges are built from source and print their hash |
| 5 Oct | B12's statistic could not tell planted-bounded from planted-compound | a gate that lies | planted controls on both sides, at freeze |
| 5 Oct | B12/B13 references passed inside the planet | oracle outside its domain | the oracle asserts its own domain |
| 6 Oct | A β > 0.99 assertion was weakened, a merge was chained after a red test, and v2 shipped a high-speed regression | unforced, three times | never weaken; merges stop on red; the player's path is a test |

**Reading.** Most of these were unforced errors (Julien's tennis highlight: amateurs lose 80% of points that way). They were caught late. None needed a slower or bigger test. Each needed one of three things:
- a test that can fail;
- an independent instrument;
- a mechanical stop.

More example tests in the middle would have caught none of them.

## Left end: always on, seconds, every commit

This end is most tests by count and little of the wall time. It catches the many small mistakes while they are still close to the change.

1. **The law checks itself.** Integer registers, key order, ranges and conservation are asserted where they live. They are exact because the law is exact: no tolerances.
2. **Digest replay.** One hash compares the whole state. Replaying the log gives the same digest. It is the cheapest whole-system oracle we have.
3. **Commuting squares** (metamorphic tests, from the math memo). The digest stays the same under any of these:
   - relabelling body ids;
   - translating the scene;
   - re-partitioning or rescheduling;
   - the sparse order against the dense one;
   - observing or not observing.

   They need no oracle, and each one kills a whole class of bugs.
4. **Rotating seeds** (the expensive search, paid in slices).
   - Each run draws fresh seeds at small sizes, from a logged stream.
   - A failure is shrunk to its smallest seed, and that seed joins a permanent regression file. The cemetery is kept.
   - Over a week the cheap suite sees millions of seeds. Small, frequent stressors: hormesis, not one big audit.
5. **The player's path.** One scripted flight, under 60 s:
   - burn at L15 to β 0.999;
   - an orbit;
   - a flyby;
   - a crash that says why.

   It tests the thing as it is used (directness). It would have caught 6 October's regression.
6. **Mechanical stops,** never discipline:
   - A merge command runs the touched suites and refuses on red. No hand-chained merges.
   - A red main stops the line: revert first, fix second. The first mistake rarely kills you; the spiral after it does.
   - Only a test's owner may weaken its assertion, and the change gets a journal line.

**Budget.** The whole left end of the touched crate runs in at most 60 s on the M1, build included. Any single test over 5 s moves to the right end or is cut.

Today `motion.rs` (20.5 s) and `plane.rs` (17.7 s) take 80% of the universe suite's 48 s, so they are the first to split.

## Right end: rare, adversarial, at one-way doors, off the critical path

**Make reversible decisions fast and irreversible ones slow.** These are the one-way doors here:
- freezing a law or a gate;
- merging a law change into main;
- changing a number format or a digest;
- a new build Julien will fly.

A branch, a lab run or a view tweak is a two-way door: it gets the left end only.

1. **Gates are frozen before their first run.** Each has planted mutants that must fail it and a control that must pass it. A gate that no mutant fails is a control, not a gate.
2. **Before any freeze:** a premise-first red-team, plus the cheapest falsifying probe.
3. **Fat tails.**
   - Use many seeds.
   - Judge the worst case and the tail, never the mean.
   - Climb ladders 10× per rung until one fails, with extreme rungs and chaotic rungs (the rules in [test-ladder.md](test-ladder.md) stand).
4. **Independent judges.**
   - A judge comes from another model family and uses another harness.
   - Redundancy "seems like a waste if nothing unusual happens"; something unusual usually does (Taleb).
   - Segregation of duties: whoever builds a module never certifies it.
5. **Long simulation fuzzing** on agonbox.
   - Hours of random scenes under sabotaged schedules; every failure shrinks to one seed.
   - Running on x64 Linux is also a free cross-hardware check: by law its digests must equal the Mac's.
6. **Cost gates** run on the M1, heat-soaked, with the machine state recorded.

These run on agonbox, in the lab or in the background. The integrator reads verdicts only.

## The middle we cut

- Tests that pin implementation details. They break on every change of representation, which is the change we most need ("gates judge a representation; they never size it").
- Float snapshots, tuned tolerances, and golden numbers that the shipped code cannot regenerate.
- Tests that cannot fail, coverage targets, and the same check duplicated across modules.
- Slow tests in the inner loop.
- Reading a failure as the death of a method. A failure kills a configuration; a method dies only by a named argument.

**The delete pass, at each phase end.** Every test names the mistake it prevents and a mutant it kills, or it goes. "If you do not end up adding back at least 10% of them, then you didn't delete enough" (Musk).

## Who does what

- **Builders** write their left end with their code.
- **The judge's family** builds the right end.
- **GLM** runs the rotating seeds, the fuzzing and the red-teams.
- **The integrator** reads verdicts and merges only through the stopping merge command.
- **Lower tiers** never weaken a test.

## If approved, the changes

1. A merge command in `xtask` that runs the touched suites and refuses on red.
2. Rotating seeds, plus a regression-seed file, in `behave`'s sampler and in the property tests.
3. The scripted flight test in `crates/universe`, grown from `tests/throttle.rs`.
4. Commuting-square digest tests: relabel, translate, reschedule, sparse against dense.
5. On every push to main, agonbox runs the suite and compares digests with the Mac's.
6. `motion.rs` and `plane.rs` split into a fast part (left end) and a slow part (right end).
7. A delete pass by Sonnet: list every test that kills no mutant.
8. test-ladder.md folds into this file, and AGENTS.md's test bullets become one pointer, a net cut.

## Sources

**From Julien's library (Readwise):**
- Taleb: the barbell, redundancy, hormesis, ruin first.
- Farnam Street: reversible against irreversible decisions; inversion; the 1° heading.
- Sahil Bloom: the loser's game.
- Waitzkin: the error spiral.
- Feynman: you are the easiest person to fool.
- Kaufman: segregation of duties.
- Isaacson's Musk: delete, then add back 10%.
- Ultralearning and Make It Stick: directness; testing as retrieval.
- Kahneman: the speed and quality of feedback.

**Not in his library** (Readwise holds almost nothing on software testing): practitioners with skin in the game.
- FoundationDB and TigerBeetle: deterministic simulation and seeds.
- QuickCheck and Hypothesis: shrinking.
- Mutation testing: testing the tests.
- Toyota's andon cord: stop the line.
