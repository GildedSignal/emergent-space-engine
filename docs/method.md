# Method: a causal chain

**Draft for Julien's validation (7 October). Not in force until he approves it.** Once approved, it absorbs [test-ladder.md](test-ladder.md). AGENTS.md's "Evidence", "Tests" and "Start clean …" bullets then become one pointer here.

Julien, 7 October:
- "the way we work should be a sort of causal chain that way we can quickly iterate on the process and see where it fails";
- triggers "need to be where they will not be missed";
- "make the doc like our engine … once a certificate is broken you have to update and delete";
- "archive and not delete … never rewrite history";
- "proper feedback collection without feedback we're fooling ourselves with a simulacrum".

## How to read it

The method is built like the engine.
- **Events that always happen fire rules.** Each rule leaves a record. A record that breaks a certificate forces an update or an archive. Nothing relies on remembering.
- **Every rule has an id, a trigger, an action, a record and an origin.** A rule without a trigger is a wish: it gets a trigger or it is cut (section 10).
- **Machines write the records.** Agents write one line of why. Routines beat negotiating with oneself every day (Farnam Street).
- **Sketches are exempt.** Creativity stays free on branches and in the lab. The chain bites only at the doors to main and to a freeze.
- **Each rule is marked built, partial, or to build.** A rule still to build is a proposal and is never claimed as protection.

## 1. The chain

| Event (always happens) | Rules fired | Record | Status |
|---|---|---|---|
| **E1 Session start** | M1: read HANDOFF ("In flight", reds, anomalies). A red main or a stale worktree comes first. | — | built |
| **E2 A task starts** | M2, the clean workspace: the branch's first commit is `clean:`. It archives what nothing reaches in the area and what the task will replace, or it says `clean: none`. The mess is bounded even if the end is lazy. | the clean commit | to build (checked at E5) |
| **E3 Any run** (check, gate, bench, flight, lab run) | M3: the harness writes the run record: the inputs for exact replay, each invariant's worst margin, and every refusal. A broken invariant or a new worst margin goes to the anomaly log automatically. | run record, anomaly log | partial |
| **E4 Any commit** (the hook) | M4: text budgets. M5: code commits carry `Built-by:` (model or person) and `Why:` (a register row, an H entry, a lens or an anomaly). M6: correction entries carry `Introduced:` and `Caught:` commits, an exposure class, a family, and the process step fixed. M14: an edited doc keeps its first line, which says what the doc is for and what it must not become. | the commit | M4 built; the rest to build |
| **E5 Merge to main** (one command, the only door) | M7: run the touched suites and replay every saved flight. Refuse on a new red, or on a worse number on a baselined red. M8: refuse without the branch's `clean:` commit, and print the area's unreached code so "none" can be checked. M9: print the net lines; a positive count needs a `Bought:` line. M10: refresh the derived state table and log which rules fired. | trailers, firing log | to build |
| **E6 A freeze** | M11: describe the behaviour first: what should happen, what must never happen, and what the tails look like, by regime. The red-team picks the planted pair. A premise red-team and an orthogonal judge are required. | the hash in law.md | mostly built |
| **E7 A lab window** | M12: generators, deletion lenses and red-teams run; a found anomaly is a graded result. | graded branches | built |
| **E8 A phase change** (the `Phase:` line in HANDOFF changes; the hook sees it) | M13 requires, since the last change: a deletion pass; the rule-firing report, where each silent rule is kept with a reason or archived; the archive's restore ratio; the retire candidates resolved; the rules edited more than twice; and the method's own numbers (the worst latency per exposure class, the inner loop's time, the trend in lines). | one journal entry | to build |

## 2. Certificates

As in the engine, a certificate is a claim plus its conditions, evidence, origin and owner. It stays valid until a condition breaks. The next event that sees the break forces either an update, re-derived from the goal, or an archive. Never ignore and never side-step: side-stepping is how the FMM steer was lost (H0196).

**Component state is derived from facts, never declared,** so it cannot drift. E5 prints the table into HANDOFF.

| State | The fact that defines it | What it owes |
|---|---|---|
| Sketch | exists only on a branch or in the lab | nothing |
| Flying | on main | cheap checks, the run record, the clean commits |
| Load-bearing | it has dependents, or a frozen gate or a recorded flight reaches it | an orthogonal judge, right-end checks, performance work |
| Frozen | a hash in law.md | planted pairs; changes only by a new version |
| Retired | a line in the archive ledger | — |

Investment follows the state. The firing log makes this doc's rules certificates too: a rule holds while it fires and catches.

## 3. Provenance, the archive and history

- **Who, why and from where.** M5 trailers go on every code commit, and rules carry their origin in parentheses.
  - The purpose is to trace an error to its cause, never to blame. Whoever made the error has learned the most from it (Julien's SpaceX story).
  - Musk puts a person's name, never a department's, on each requirement.
  - Today the Codex autopilot commits under Claude's name. M5 fixes that.
- **Archive; don't delete.** Removed code, docs and rules go to the archive with a ledger line: what it did well, why it went, and where it is. A restore cites its line. That makes Musk's calibration (some deletions should come back) a count taken at E8, not a memory.
- **History is never rewritten.** Committed entries stay and corrections are appended. Summaries may compress, but the originals stay in the archive. That record is battle-tested feedback on the method itself.

## 4. Changing the method without oscillating

- A change to a rule names the regime it was observed in: the state, the scale, and the evidence.
- **Hysteresis.** Undoing an earlier change must cite it and say what differs in the regime. If nothing differs, do not flip back: split the rule by state ("if Sketch … else …"). Most oscillation is a conditional rule that was made global.
- Chatter, meaning a rule edited more than twice in a phase (E8), is an anomaly about the method.
- Before any change, check its attractor (section 9): what will it select for at scale?

## 5. The loop for any change

1. **Conjecture:** one sentence on what the change makes true. The check's name states it.
2. **Exposure:** what is built on it, and how hard it is to undo.
3. **Fastest refuter:** the cheapest observation that would differ if we were wrong. Prefer a generator, a property, and the existing harness.
4. **Placement:** chosen by state and exposure, from the cheap end in the inner loop to the doors of E5 and E6.
5. **Aftermath:** an escape gets M6's entry and the generator for its family.

**Reds (M7).** A known red is baselined: it has an owner, it may only improve, and it is never called a pass.

## 6. Statistical etiquette

Enforced where the reports are made (E3 and E6):
1. **Describe the behaviour before choosing the tool** (M11). Assume fat tails until thin tails are shown (Taleb).
2. **Reports print the distribution, never a summary alone:** n, the minimum, the median, the 90th and 99th percentiles, the maximum, and the worst seeds with their replays. Never a mean ± sd alone, an average of ratios, or a p-value as a verdict.
3. **Verdicts are k of n beyond a frozen line, plus the worst case.** Worst cases are compared only at equal n.
4. **Never trim an outlier.** Count independent events, not runs: runs sharing a harness count as one.
5. **A result holds inside its observed range only.** A change of regime voids old evidence (Ariane 5).

## 7. Anomalies and unknown unknowns

- **An anomaly is the most important data point.**
  - The record flags it mechanically (E3): a broken invariant, a new worst margin, a refusal, or two representations disagreeing.
  - Logging one is free and blames no one.
  - It blocks only the claims that depend on it: E5 shows such a gate as "unexplained", not "pass".
  - Reproduce it, then explain it. Once explained, it becomes a family generator or a law fix; while unexplained, it stays in HANDOFF.
  - Chasing every other blip is the opposite stupidity (Novella).
- **Unknown unknowns: neither ignore nor hunt them.**
  - Fewer parts (section 8).
  - The run record: exact replay lets old runs answer new questions.
  - Orthogonal representations at Load-bearing.
  - Fast recovery.
- **The player is the sensor we cannot build.** When the player and the metrics disagree, the metric is presumed broken (Bezos). Every flight is recorded and replayed at E5.
- **For what we can name,** look at edges, at meetings of mechanisms, at layers and at owners. Generators run as lab lenses and enter the inner loop only after a catch.

## 8. Simplicity

Fewer lines mean fewer interactions, fewer tokens read, lower opportunity cost, clearer interfaces, and fewer places to hide. Musk's order applies: question the requirement, delete, simplify, accelerate, automate.

The triggers:
- E2 (the clean workspace);
- E5 (net lines, `Bought:`);
- E8 (the deletion pass, the restore ratio, the retire candidates).

A deletion that leaves every verdict and digest unchanged is proven correct by the existing checks, which is why checks never pin implementation. The inner loop's total stays under a minute on the M1 (E5).

## 9. Attractors

| Rule | What it could select for | Guard |
|---|---|---|
| M2/M8 clean commits | ritual "clean: none" | E5 prints the unreached code; a false "none" is visible |
| M5 trailers | boilerplate | two words each; machines fill `Built-by:` |
| M6 latency | gaming by trivial catches | worst case per exposure class; a tripwire, never a reward |
| M7 reds | hiding reds | the baseline is a number; worse means refused |
| M9 lines | code golf; deleting checks | verdicts unchanged; the whole tree counted; a tripwire |
| M11 freezes | ceremony | Frozen only |
| Anomalies | not seeing them | mechanical detection; free; no blame; graded |
| M13 phase report | paperwork | one entry, mostly machine-written numbers |

## 10. Cut from the earlier drafts (no trigger, or busy work)

- "Calibration (Musk)" became the ledger's restore ratio at E8.
- "Investment follows demonstrated use" became derived state.
- "Every check carries a conjecture, a fault and a cost" became the check's name.
- "Decide on fewer looks" was cut.
- "Every other doc, when next edited" became M14.
- "The doc cuts itself back" became M13's numbers.

## On approval

Build the smallest first:
1. the merge command (M7–M10);
2. the hook rules (M5, M6, M13, M14);
3. the run record (M3);
4. the derived state table.

Until a rule is built, it stays marked "to build".

**Sources:**
- Julien's books: Taleb's *Incerto*, Bevelin, Munger, Strogatz, Brand, *Focus: The ASML Way*, Schmidt-Nielsen.
- His highlights: Farnam Street (routines, incentives, Lindy); Isaacson's *Musk*; Asimov (rules that outlive their use); Taleb (bureaucracy separates people from consequences); Bezos; Novella.
- The [dossier](../artifacts/evidence/critical-software-testing-20261007/README.md).
- Two outside AI reviews.
