Grade: silver

**Abstract.** Claim: the shipped engine already owns the calendar's family intern key — two same-orbit planets on the doll split's aligned grid co-fire at one key through 383 fires (25,525/25,525 censuses; r = 2 AU: 25,526/25,526) — but the belt's chained fictitious clock derives interval and anchor from each body's own continuous state, so 16 same-orbit ships hold 16 distinct keys from the first due at every δx = 10²–10⁶ root; the barrier is the clock's representation, upstream of a877's word. Reproduced bit-for-bit. Gain: F× calendar slots and F× fires per family epoch (families row) — priced, not delivered. Cost: a family-anchored-grid law change, gated with od 1. Checker extended the domain (F = 16, e = 1/20, synodic drift, 6,303 fires, δx = 1 root): all confirm; sharing class is the (step, anchor), not the family.

## Reasons

**1. Reproduction.** Clean tree at 595fdd47; applied `work/patch.diff` (a new example only, no law change); rebuilt (6.7 s); ran both census commands from `regen.sh`. stdout and stderr are bit-for-bit identical to `census-r1au.txt` / `census-r2au.txt`. The runner's regen also exited 0. Every dossier number traces: 25,525/25,525 pair co-fires, 383/383 fires, steps 2³⁵ (r = 1 AU) and 2³⁷ (r = 2 AU); clone control one distinct key, 350/370 fires, zero spread; ship arms `mean_distinct_dues = 16.00`, `anchors_eq = steps_eq = false`, first-due spreads 18,415–5.4×10⁸ ticks (12.3×–36.1× the light offsets 1,500–1.5×10⁷), last-due spreads to 1.9×10¹⁰.

**2. Predictions.** `predictions.md` (06:18) predates the final census script (06:35) and all outputs; the author's original census files were overwritten by the runner's regen, so timing rests on content — and the content is decisive against tuning: predictions 2, 3 and 5 **failed** and the author reports them as failures; prediction 2's failure (g_fork = 0 at every δx, for a stronger reason than the 61-bit word: the per-body continuous clock) *is* the result. Prediction 1 (clone control bit-identical) held — instrument valid. Honest work; but gold's letter requires held-out predictions that held, and three did not.

**3. Attacks (all outside the author's tested domain; a separate `family_census_adv.rs`, kept out of the run folder).**
- **F = 16 aligned families** (author tested 2), δx = 10³ and 10⁶: co-fire 41,328/41,328 censuses, 1,513 fires, identical steps 2³⁵, no stream fork.
- **e = 1/20 pair** (the plane's real Giant e): co-fires identically.
- **Synodic drift** — the dossier's own named untested regime: source planet at 1 AU, family at 1.3 AU. Aligned16 still co-fires 39,886/39,886; ships still 16 distinct keys from the first due.
- **Horizon × 16:** 6,303 fires — no fork, no step change in any group. The factor-2 fork the dossier feared did not trigger at any flown F or e.
- **Below the ladder:** δx = 1 and 10 root — ships fork at the first due (16.00 distinct).
- **Cross-radius pair** (1.00 vs 1.15 AU — different orbits, unrelated bodies, both H quantized to 2³⁵): co-fires 99.80% of 41,328 censuses, stream forking at fire ~1,485 when an H change slips the grid. **The aligned grid's sharing class is the (step, anchor), broader than the family** — the adoption framing "family-anchored" understates what the grid already interns.
Every attack **confirms** the claim and extends its domain.

**4. Mechanism, in code.** `plan_clock` (step.rs:626–654) sets `anchor = t` (the body's own event tick) and `interval = 2·ext.ticks(ext.time(y, ds))` from the body's own continuous state; `on_clock` routes root-doll ships/players there while planets keep the aligned split (step.rs:19, `aligned` at step.rs:107). The dossier's reading is the code's behaviour.

**5. Novelty.** The standing page's od 2 (the engine-side key census) was open; a877 measured the word half off-engine. docs/HISTORY.md's "family" entries are the pre-pivot engine's identity families — a different mechanism. Not a repetition.

**6. Page.** The proposed page folded the result faithfully (Refuted entry matches the evidence; clone control kept as the control). Corrections made in place: Current best was ~20 physical lines — trimmed to 2 long lines under the 15-line budget; the checker extensions folded in; the Runs entry graded. Not three gold runs — the topic stays open.

**7. Goal fit.** The board's families row (~10² memory, ~10 kicks): the run prices the unshared idiot index (F×) and shows the engine already runs the fix's mechanism for doll bodies. PRINCIPLES 33 ("a body resolves only the influences that are significant at its own scale" — at the parent's scale the family is one body); PRINCIPLES 19 ("a fix signals the wrong representation" — here the fix already exists in the same engine). The harness is the restricted problem, honestly scoped.

**Why silver, not gold:** the payoff is priced, not delivered — no scoreboard row moved yet; adoption is a law change still ungated (od 1); and three of five pre-registered predictions failed (informatively, but gold requires predictions that held).

## The one experiment that would make it gold

Fly root-doll ship families on a family-anchored grid — each member reads the family reference's aligned step; its own chained clock refines only when its certificate Ξ crosses — through the plane's gates B13/B12/B17/B18, measuring the actual slot and fire reduction on a belt plane. One rung; the design is already written in the dossier's adoption paragraph.

## What the author missed

- **A units slip:** 1 root = 1.477 km (AU = 1.013×10⁸ root), so δx = 10² root is 148 km, not "1.5 km"; the "(1.5 km to 1.5 Mm)" parenthetical is off by 100× (the "million km" at δx = 10⁶ root is right). All decisive numbers are unit-free (root, ticks, ratios) — cosmetic, dossier only.
- **The queue has no intern at all:** `key_of` returns `(tick, id)` and the queue keys by deadline + `moved` (position-dependent), so two co-firing members are always two entries at different deadlines. The F× **fires** payoff therefore needs a calendar-item change (one resolution serving the family), beyond the shared due key; the author flagged only the merge direction.
- **The sharing class is the step, not the family** (cross-r evidence above): "family-anchored grid" is one instance; the grid interns step-class neighbours across unrelated orbits, which both widens the payoff and changes what the gate must judge.
- `fleet.rs` doll members (free interning today?) remain unflown, as the author says.
