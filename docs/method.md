# Method: attractors, states, checks and simplicity

**Draft for Julien's validation (7 October). Not in force until he approves it.** Once approved, it absorbs [test-ladder.md](test-ladder.md). AGENTS.md's "Evidence", "Tests" and "Start clean …" bullets then become one pointer here.

Julien, 7 October: "prevent big mistakes or many small ones"; "it's really about epistemology … unknown unknowns of interactions"; tests "reduce the time towards detecting when we're fooling ourselves"; "insitu data collection"; "simplicity always win"; "we need to create attractors that forces us towards simplicity, performance and compactness … without putting in branch in our wheel"; "treat anomalies as our most important data points"; "Taleb shall be proud of us just how i loathe averages".

## 1. Attractors, not rules

Any rule, repeated by many agents over time, selects for something. That selection is its attractor, and it can betray the rule's purpose. Testing our tests, for example, selects for bloat.

So every rule, in every doc, states four things:
- what it is for;
- what it selects for at scale;
- the state in which it applies (section 2);
- what would cut it.

A rule whose attractor betrays its purpose is rewritten or cut.

1. **Budgets, not targets.** A fixed, scarce budget forces candidates to compete, and the useful survive. Our budgets: the inner loop's minute, the 60-second check, the text caps, the window.
   - Systems learn by eliminating what lowers the fitness of the whole (Taleb).
   - A target gets gamed: show me the incentive and I'll show you the outcome (Munger), and set goals breed cheating (Farnam Street).
   - Measures here are tripwires that alarm. They are never rewards.
2. **The attractors we want:** toward the finished product; toward contact with reality (the player, the physics); toward simplicity, compactness and performance; toward cheap reversal; toward independent evidence.
3. **Messy by default.** Nothing below applies to a sketch. Rules switch on with state, when something needs them.

## 2. States

Every component is in exactly one state: a module, a gate, a law, a tool, a lens, or a rule of this doc. HANDOFF shows each one's state, so nothing gets lost in the sauce.

| State | What it is | What it owes | Promoted when |
|---|---|---|---|
| Sketch | a question being tried, on a branch or in the lab | only to leave main and frozen things alone | it works end to end once |
| Flying | works, on main | cheap checks, the in-situ record, a deletion pass | something builds on it, or Julien relies on it |
| Load-bearing | others depend on it | an orthogonal judge, right-end checks, performance work | it becomes a one-way door |
| Frozen | a versioned law, gate or format | red-team-chosen planted faults; changed only by a new version | — |
| Retired | archived | one line on what it did well | — |

- **Investment follows demonstrated use** (Lindy). What has proved useful earns work to get better; the rest does not get polished.
- **Unused through a phase means retired.**
- **Promotion is by evidence, never by hope.**

## 3. The loop

A check exists to shorten the time between fooling ourselves and knowing it. Gates, rungs, lab runs, red-teams and flights all follow one loop:
1. **Conjecture:** one sentence on what the change makes true.
2. **Exposure:** what is built on it, and how hard it is to undo.
3. **Fastest refuter:** the cheapest observation that would differ if we were wrong. Prefer a generator, a property, and the existing harness.
4. **Placement:** the inner loop, the lab, or the door, by state and exposure.
5. **Aftermath:**
   - An escape is named by its family, gets the family's generator, and fixes the process step that let it through.
   - Its detection latency is recorded with its exposure class.

**Reds.** A new red, or a worse number on a known red, blocks the merge. A known red is baselined: it stays red, has an owner, and may only improve. It is never called a pass, and it never freezes the rest of the work.

## 4. Statistical etiquette

1. **Describe the behaviour before choosing a tool.** In words and dimensionless numbers, say:
   - what should happen, and in which regimes;
   - what must never happen;
   - what each tail should look like.

   The description picks the statistic, never the reverse.
2. **Assume Extremistan.** Complexity implies fat tails (Taleb), so thin tails must be shown before any mean is used. A river four feet deep on average still drowns you.
3. **Report the distribution, not a summary:** n, the minimum, the median, the 90th and 99th percentiles, the maximum, and the worst seeds with their replays. Never a mean ± sd alone, an average of ratios, or a p-value as a verdict.
4. **Verdicts are counts against frozen thresholds** (k of n beyond the line) plus the worst case. Compare worst cases only at equal n, since the maximum grows with n.
5. **Never trim an outlier.** The worst case is the most important data point: explain it, never drop it.
6. **Count independent events, not runs.** Runs sharing a harness count as one. Agreement is not independence (Knight and Leveson).
7. **Record always; decide on fewer looks.** The more often one looks, the more noise one sees (Taleb).
8. **A result holds only inside its observed range** (Schmidt-Nielsen). A change of regime voids old evidence (Ariane 5).
9. **A statistic is calibrated on a planted pair before it freezes** (the B12 lesson). This applies at Frozen only.

## 5. Anomalies are the most important data

An anomaly is the best data point we have.
- **Detection is mechanical, never a judgement call.** The record flags four things: a broken invariant, a new worst margin, a refusal, and a disagreement between two representations.
- **It costs nothing to log, and it blames no one** (ASRS immunity).
- **It blocks only the claims that depend on it,** never a person's other work. So nobody gains by not seeing one.
- **Reproduce first** (exact replay), then explain. No story before the replay (the narrative fallacy).
- **Explained** anomalies become a family generator or a law fix. **Unexplained** ones sit in HANDOFF with what they block.
- In the lab, a found anomaly is a graded result.
- **The opposite stupidity is chasing every blip** (Novella's anomaly hunting). Only the four mechanical classes block a claim; everything else is just recorded.

## 6. Where to look, for what we can name

| Quadrant | Refuted by |
|---|---|
| Known knowns (the law's invariants) | assertions at the source, in every run and flight |
| Known unknowns (named risks) | gates and ladders, at Load-bearing and Frozen |
| Unknown knowns (steers given, not followed) | the register: a steer given twice and not followed is a failed check |
| Unknown unknowns | section 7 |

Look:
- where behaviour changes kind (Strogatz): physics edges, and every finite resource of the representation;
- where mechanisms meet (Bevelin; Munger);
- where slow layers meet fast ones (Brand);
- where owners meet, with units in types (Mars Climate Orbiter);
- where the instrument could lie.

Generators along named coordinates: fragility (δ and 2δ, convexity), covering combinations, the small scope, rare made common, swarm, symmetries. They run as lab lenses, and enter the inner loop only after they catch something.

## 7. Unknown unknowns: neither ignore them nor hunt them

They are infinite from where we stand, so we work on exposure, not prediction (Taleb), in four plain moves:
1. **Fewer places to hide.** Interactions grow roughly as the square of the parts, so simplicity (section 8) is the first defence.
2. **Sense in situ, always on.**
   - Every run writes one fixed-size record: the inputs that make replay exact; each invariant's worst margin, never an average; every anomaly.
   - Replay is exact, so old runs answer tomorrow's questions with tomorrow's probes.
   - Margins shrink before things break, as the O-rings did before Challenger.
3. **Ask from another representation**, at Load-bearing and above. Use an analytic limit, conserved quantities, a symmetry, or an independent fine reference. Prefer the small ones to a second implementation.
4. **Recover fast.** Exact replay, cheap reverts and the last good state.

**The player is the sensor we cannot build.** When the anecdote and the metrics disagree, find the broken metric (Bezos). When published data are wrong, build your own wind tunnel (the Wright brothers, via Founders). Every flight is recorded and replayed.

**What gets in the way:**
- explaining away;
- averaging;
- silencing an alarm;
- switching instruments off for speed;
- testing only the lab's distribution (the ludic fallacy);
- reading many passes as safety (the turkey);
- letting the code grow.

## 8. Simplicity

Fewer lines mean fewer interactions, fewer tokens on every read, lower opportunity cost, clearer interfaces, less storage, and fewer places for unknowns to hide.

The order is Musk's: question the requirement, delete, simplify, accelerate, then automate.
- **When.** A Flying component gets its deletion pass before the next feature lands on its layer. A phase ends with one.
- **Safe by construction.** Unchanged verdicts and digests prove a deletion correct. This is why checks never pin implementation.
- **Measured as a tripwire, never a reward.** The history check prints live lines for the product, judges and tools together, so moving code around games nothing. A merge that adds lines says what they bought.
- **First to go:** what nothing reaches, retired paths (to the archive), and duplicates.
- **Calibration** (Musk): if nothing deleted ever comes back, too little was deleted.
- **Who.** Deletion patches are lab lenses and Sol's work. The owner merges.

## 9. The barbell

**Cheap end, on every change:** assertions, replay digests, symmetries, small generators with fresh seeds (failures shrunk and kept), and the in-situ record.

The inner loop's total stays under a minute on the M1. A check outgrowing it moves to the lab, or goes.

**Expensive end, at one-way doors only:** freezing, merging a law change, changing a format or digest, a build Julien flies. There run frozen gates, red-teams, the worst case over many seeds, ladders, the bigger generators, orthogonal judges, and heat-soaked cost.

**Stolen and not stolen:** see the [dossier](../artifacts/evidence/critical-software-testing-20261007/README.md).

## 10. This doc's own attractors

| Rule | What it could select for | Guard |
|---|---|---|
| Detection latency | many trivial instant catches; gaming | worst case per exposure class; a tripwire, never a reward |
| Anomalies block claims | reluctance to see them | mechanical detection; free to log; no blame; a graded result |
| Planted faults | easy-to-make faults; tests of tests (bloat) | only at Frozen, chosen by the red-team as the failure that matters |
| Line counts | code golf; deleting checks | verdicts unchanged; a tripwire; whole tree counted |
| The inner loop's minute | slow checks left to rot in the lab | the lab runs them; their verdicts gate one-way doors |
| Orthogonal judges | duplicate implementations | from Load-bearing up; small representations first |
| Generators | harness sprawl | lab lenses first; promoted only after a catch |
| States | ceremony | five states; one column in HANDOFF; promotion by evidence |

The doc is itself a Sketch. If worst latencies do not fall, if the inner loop outgrows its minute, or if lines keep rising, it is cut back.

## 11. How it fits, and what changes on approval

It reuses what exists: frozen gates (Frozen); ladders (range claims); GLM lenses (generators, deletions, red-teams); judges from another family (orthogonal, by method); Julien's flights (the sensor); journal corrections (latency and class); the register (unknown knowns); and HANDOFF (states, baselined reds, anomalies, the line trend).

On approval, five changes:
1. Merges stop on a new or worse red.
2. HANDOFF gets a state column.
3. Corrections record latency and class.
4. The history check prints live lines.
5. Generators and deletion become lab lenses.

Then every other doc gets the attractor treatment as it is next edited, with no campaign. test-ladder.md folds in here.

**Sources:**
- Julien's books: Taleb's *Incerto*, Bevelin, Munger, Strogatz, Brand, *Focus: The ASML Way*, Schmidt-Nielsen, Juarrero.
- His highlights: Founders and How to Take Over the World; Bezos; Isaacson's *Musk*; Novella; Farnam Street (incentives, goals, Lindy); Feynman.
- The critical fields: the [dossier](../artifacts/evidence/critical-software-testing-20261007/README.md).
- Two outside AI reviews (the orthogonal refuter, latency per class, the rule for reds, this doc's attractors).
