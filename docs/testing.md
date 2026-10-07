# Checks and simplicity: finding out fast that we are wrong

**Draft for Julien's validation (7 October). Not in force until he approves it.** Once approved, it absorbs [test-ladder.md](test-ladder.md). AGENTS.md's "Evidence", "Tests" and "Start clean …" bullets then become one pointer here.

Julien, 7 October:
- "prevent big mistakes or many small ones";
- "it's really about epistemology … unknown unknowns of interactions";
- "reduce the time towards detecting when we're fooling ourselves, not to prevent issues";
- "we need to not be stupid instead of smart … insitu data collection";
- "reduce the number of LOCs once a feature works … simplicity always win".

## The idea

Everything we already do is a conjecture meeting a refutation: a gate, a rung, a lab run, a red-team, Julien's flight. This doc is their shared grammar, not a new activity.

A check exists to shorten the time between fooling ourselves and knowing it.
- **The measure is detection latency:** from the change that introduced a mistake to the check that caught it.
- **It is read per exposure class, and by its worst case.** One average would hide one structural error behind a thousand instant catches. At a one-way door the target is "caught before integration"; reversible work may be caught later.

The doc names no files, mechanisms or number formats. Those change.

## The loop

It applies to any change, at any scale.
1. **Conjecture.** One sentence: what does this change make true?
2. **Exposure.** What will be built on it, and how hard is it to undo?
3. **Fastest refuter.** Find the cheapest observation that would differ if the conjecture were false.
   - Prefer a generator to a case.
   - Prefer a property to an example.
   - Prefer the existing harness to a new one.
4. **Proof it can fail.** Plant the fault it should catch. A refuter that misses its plant is a control.
5. **Placement.** Cheap: the inner loop. Expensive: the lab. One-way: the door.
6. **Aftermath.**
   - A surprise stops the work until it is explained.
   - An escape is named by its family, gets the family's generator, and fixes the process step that let it through. Its latency is recorded.

**Reds.** A new red, or a worse number on a known red, blocks the merge. A known red is baselined: it stays red, it has an owner, and its numbers may only improve. It is never called a pass (Challenger's normalisation of deviance), and it never freezes the rest of the work.

## What a check can know

1. It refutes; it never proves (Popper, via Taleb). The instrument can lie.
2. A pass is worth only the check's proven ability to fail (Novella).
3. Risk lies in exposure, not in past bug counts (Taleb).
4. A result holds only inside its observed range (Schmidt-Nielsen). A change of regime voids old evidence (Ariane 5).
5. Agreement is not independence (Knight and Leveson; coding agents, 2026). An unambiguous spec is itself a check.
6. Plans fail by tunnelling (Taleb). Some inputs must come from outside the plan.

## Where to look, for what we can name

| Quadrant | What it is | Refuted by |
|---|---|---|
| Known knowns | the law's invariants | assertions at the source, in every run and every flight |
| Known unknowns | named risks | gates and ladders |
| Unknown knowns | steers given and not followed | the register: a steer given twice and not followed is a failed check |
| Unknown unknowns | everything else | the next section |

Information concentrates in five places:
1. **Where behaviour changes kind** (Strogatz). That means physics edges, and every finite resource of the representation.
2. **Where mechanisms meet.** Interactions dominate (Bevelin). Extremes come from forces combining (Munger).
3. **Where slow layers meet fast ones** (Brand). Effort scales with how slow a layer is.
4. **Where owners meet** (ASML; Mars Climate Orbiter). Interfaces carry units in types and contracts checked from both sides.
5. **Where the instrument could lie:** domains, shared harnesses, stale builds.

Generators along the coordinates we can name:
- fragility (δ and 2δ; convex harm means fragile);
- covering combinations;
- the small scope;
- rare made common (shrink every finite resource, force the rare branches);
- swarm;
- symmetries.

## Unknown unknowns: neither ignore them nor hunt them

They are infinite from where we stand, so enumerating them is the smart-and-stupid move. Taleb's answer is to work on exposure, not prediction: cut the downside first, and judge the range of outcomes, not the expected one. In practice that means four plain moves.

1. **Fewer places to hide.**
   - Interactions grow roughly as the square of the parts, so every part deleted removes many unknowns at once.
   - Simplicity (below) is the first defence. No check reaches what an absent part would have done.
2. **Sense in situ, always on.** Every run writes the same small record: flights, benches, lab runs and checks alike. It holds:
   - the inputs that make replay exact;
   - each invariant's closest approach to its limit, meaning its worst margin, never an average;
   - every refusal and surprise.

   Because replay is exact, a recorded run can be asked tomorrow's questions with tomorrow's probes: we collect data for questions not yet known. A new record, the worst margin ever seen, is a surprise (step 6). Margins shrink before things break, as the O-rings eroded before Challenger.
3. **Ask from another representation.** At high exposure, one judge derives its answer in a representation that shares none of the conjecture's machinery:
   - an analytic limit;
   - conserved quantities;
   - a symmetry transform;
   - an independent fine reference;
   - the player's flight.

   It is the only check not bound to coordinates we chose.
4. **Recover fast.** Exact replay, cheap reverts and the last good state mean an unknown unknown costs one bisection, not a week.

**The player is the in-situ sensor we cannot build.**
- When the player's anecdote and the metrics disagree, trust the anecdote and find the broken metric (Bezos).
- When the published data are wrong, build your own wind tunnel (the Wright brothers, via Founders).
- Each recorded flight is kept and replayed.

**What gets in the way** (be consistently not stupid; Munger):
- explaining a surprise away;
- explaining it before reproducing it (the narrative fallacy);
- averaging the record;
- silencing an alarm by weakening a check, widening a tolerance, or catching and carrying on;
- switching instruments off for speed;
- testing only the lab's distribution, never the player's (the ludic fallacy);
- reading many passes as safety (the turkey);
- reading agreement as independence;
- letting the code grow;
- not looking.

The opposite stupidity is chasing every blip (Novella's anomaly hunting). Intelligence is also ignoring what is irrelevant (Taleb). So only a broken invariant or a new record stops the work; everything else is just recorded.

## Simplicity: the cheapest check is code that does not exist

Fewer lines mean fewer interactions, fewer tokens on every read, lower opportunity cost, clearer interfaces, less storage, and fewer places for an unknown to hide.

The order is Musk's: question the requirement, delete, simplify, then accelerate, then automate. Deletion comes before optimisation. Perfection is when nothing is left to take away (Saint-Exupéry).

1. **When.** A feature whose gates pass gets a deletion pass before the next feature lands on the same layer. A phase ends only after its deletion pass.
2. **Safe by construction.** A deletion that leaves every gate verdict and every digest unchanged bit for bit is correct by the existing checks, so it needs no new ones. This is why checks never pin implementation: such checks would forbid exactly this.
3. **Measured.** The history check prints the live lines for the product, the judges and the tools, and HANDOFF shows the trend. A merge that adds lines says in one line what they bought.
4. **First to go:** code that no product or judge reaches; retired paths, which go to the archive; and duplicated logic.
5. **Calibration** (Musk): if nothing deleted ever has to come back, too little was deleted.
6. **Who.** Deletion patches are cheap work for a lab lens ("delete, verdicts unchanged") and for Sol. The owner merges them.

## The barbell

A check earns its place when p(it catches) × cost(the escape) exceeds its cost.

**Cheap end, on every change, in seconds:**
- assertions;
- replay digests;
- symmetries;
- small generators with fresh seeds, where failures are shrunk and kept forever;
- the in-situ record.

The inner loop stays under a minute on the M1. A check that outgrows a few seconds moves to the lab, or goes.

**Expensive end, at one-way doors only.** The doors are:
- freezing a law or a gate;
- merging a law change;
- changing a number format or a digest;
- a build Julien will fly.

What runs there:
- frozen gates with planted faults and controls;
- a premise-first red-team;
- the worst case over many seeds;
- ladders climbed until one fails;
- the bigger generators;
- orthogonal judges;
- cost measured heat-soaked on the M1.

**Stolen from fields that cannot break** (see the [dossier](../artifacts/evidence/critical-software-testing-20261007/README.md)): stop at the first abnormality (Toyota, Erlang, JPL); a simple monitor beside the clever channel (Airbus); make illegal states unrepresentable (Jane Street); differential checks (Csmith, SQLite); deterministic simulation with accelerated time (TigerBeetle, FoundationDB); prototypes break, crewed vehicles do not (SpaceX); error budgets (Google SRE); never drop an independent check when adding a clever one (Therac-25); fix the process step that let the escape through (the Shuttle group); log near-misses (ASRS).

**Not stolen:** paperwork, coverage targets, whole-system proofs, N teams on one method, requirements frozen up front.

## Not busy work

- Every check carries one line: its conjecture, its planted fault, and its cost. A check missing any of the three goes.
- Reports are verdict lines.
- There is no retrofit campaign. The doc applies to the next gate, merge, escape or deletion pass.
- Long runs use the lab's and agonbox's time, never the integrator's.
- The doc is itself a conjecture. If the worst latency per exposure class does not fall, if the inner loop outgrows its minute, or if the line count keeps rising, it gets cut back.

## How it fits what we already do

| What exists | Its place |
|---|---|
| Frozen gates with planted faults | refuters at one-way doors |
| Ladders | claims of range |
| GLM lenses with checkers | the generators and deletion patches, out of the integrator's time |
| Red-teams | refuters of the premise |
| Judges from another family | orthogonal refuters: another method, not only another model |
| Julien's flights | the in-situ sensor, recorded and replayed |
| Journal corrections | escapes, with latency and exposure class |
| The register | the refuter of unknown knowns |
| HANDOFF | baselined reds and their owners; the line count's trend |

## On approval

Four changes, each of which removes work or makes it visible:
1. Merges stop on a new or worse red, mechanically.
2. Correction entries record latency and exposure class.
3. The history check prints live lines.
4. Generators and deletion become lab lenses.

Then test-ladder.md folds in, and AGENTS.md gets one pointer.

**Sources:**
- Julien's books: Taleb's *Incerto*; Bevelin's *Seeking Wisdom*; *Poor Charlie's Almanack*; Strogatz; Brand; *Focus: The ASML Way*; Schmidt-Nielsen's *Scaling*; Juarrero.
- His highlights: Founders and How to Take Over the World (the Wright brothers); Lex Fridman with Bezos (anecdotes over metrics); Isaacson's *Musk*; Saint-Exupéry via *The 4-Hour Body*; Novella; Farnam Street; Feynman; Munger.
- The critical fields: the [dossier](../artifacts/evidence/critical-software-testing-20261007/README.md).
- The orthogonal refuter, latency per exposure class and the rule for reds came from an outside AI review, adopted.
