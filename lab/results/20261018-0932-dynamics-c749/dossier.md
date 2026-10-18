# Dossier — 20261018-0932-dynamics-c749 (dynamics lens)

## Claim

The finality fire's internal state is now measured on the game's own fleet battle
(allocator-ratchet od 5's named next step): on `worlds::galaxy` battles every fire is
state-decided at certify — PRE's D equals the assert's own violation exactly, 6/6 fires
across two executions with race-moved incidence — the sibling-closure hole (`out=`)
never opens under the battle's merge/split topology (0/267 rollbacks), and the violated
region is a merged giant descendant of the armed pair, not either armed lineage itself;
but two halves of e517's selfchurn record do **not** transfer: publication does not ride
the boundary exactly (94/261 non-fatal restores land strictly inside it, slack to −432
chronons), and the publish-side armed certificate (A ≤ 0) is blind to 1/6 fires — the
certify-side D is the complete decider, so the fix's test must gate certifies.

## Bottleneck

allocator-ratchet direction 5, second half: "the fire's internal state (which lineage
crossed the published tick)" — the page's named next step, the evidence the engine-side
fix (od 1) will be written against. Gain: not a 10× compute move; it converts the fix's
soundness argument from "proven on a synthetic churn harness" to "proven on the game's
own scene class", and it corrects two claims that would have mis-shaped the fix (the
attractor and the publish-side gate). What it lets us delete: any thought of gating
publication alone (hold-while-armed on publishes), which 1/6 fires pass through unseen.

## Evidence

All numbers regenerate with `regen.sh` (≤ 2 min; applies `work/patch.diff` = e517's
print-only instrument verbatim + bf83's `exposure.rs` verbatim + this run's disclosed
extensions: three battle args — fleets, galaxy size, seconds — and a bbox print on the
FIRE line). Instrument is print-only; the assert is untouched; exit 101 = fire.

- **Protocol**: `exposure battle <seed> 2400 32 8192 0.5 [fleets] [galaxy]` — bf83's fire
  protocol (rate 2400, min_region 32, margin 0.5), galaxies 4352/12 fleets (6 seeds) and
  8704/24 (8 seeds), plus the shipped-default margin 2.0 (2 seeds) and 2 replicates.
- **Incidence is the wall-clock race; the law is not.** Execution 1 (record/): 3 fires/8
  at 8704 (seeds 11, 19, 21), 0/6 at 4352, 0/2 at margin 2.0; replicates of the two
  fired seeds did not refire (12/14 rollbacks, all absorbed). Execution 2 (regen, same
  commands, different load): 2/8 at 8704 (21, 23) and 1/6 at 4352 (seed 11 — the class
  bf83 pooled at 4/62). Pooled 6 fires, all obey the law below.
- **Fire ⇒ PRE D > 0, exact, 6/6.** The PRE line immediately before each rollback burst
  carries D = (violation, truth lineage, s0) with violation = the FIRE line's own
  fin_hi − s0 and s0 identical (violations 16–96 chronons = 1–6 windows of 16). The
  last pre-fire HAZ armed pair names the fatal clash: exact (same busy region, truth
  lineage, margin, s0) in 4/6; same lineage and identical margins in 1/6 (a split moved
  the busy id between publish and certify); **publish-blind in 1/6** (regen g8704_s23:
  the fatal pair 53↔36 at s0 704, violation 96, never appears armed at its own margins;
  lineage 36 was armed only in an earlier episode of a different shape, A = 112–256 at
  s0 256, long resolved) — e517's soundness note ("the A ≤ 0 publish-side half misses
  strides dispatched between publishes, which D still covers") is now a measured
  game-scene fact, not an argument.
- **m > 0 ⟺ fire.** All 6 fatal RB lines have m = 48/16/80/48/32/96 > 0 (and the assert
  fires); every non-fatal restore passes with m ≤ 0 (261/261 across both executions).
- **The boundary attractor does not transfer.** e517's equality law (every realized
  non-fatal clash restores at exactly m = 0) holds on 167/261 non-fatal RBs; **94/261
  restore strictly inside the boundary** (record execution: m ∈ [−432, −48], median
  −224). The churn harness's "publication rides the boundary" was its own scene's
  property; the battle restores with slack. Safe direction — but the fix's test cannot
  assume the boundary as the typical restore point.
- **Containment holds under real merge topology**: `out=` (affected ids outside PRE's
  descendants closure) empty and mo = 0 on **every** RB line, fires included, both
  executions (0/267) — rollback's union-find `affected` never left PRE's closure even
  with the battle's 8–12 merges and 3+ splits per draw.
- **Which lineage crosses**: the violated region (FIRE ids 45, 48, 44, 9, 35, 52) is in
  every case a *merged giant* — bbox 302–2553 units wide where the scene's ordinary
  regions are fleet-scale — carrying the armed pair's descendants' max fin_hi 16–96
  chronons above an old stride's start (the stride spans 80 chronons; the partner's
  lineage merged ahead and published past it). The identity to watch is the closure's
  max fin_hi, which is exactly PRE's box.
- **Armed ≠ incidence, at both margins**: 3,148 armed publishes (A > 0) without fire
  pooled; 17 PRE D > 0 without fire. At the shipped default margin 2.0: armed at > half
  of publishes (120/194, 97/181) yet **zero rollbacks** — the planner absorbs every
  meeting; the fire is a margin-0.5-class exposure (bf83's reading, confirmed from
  inside the state).
- Machine: Linux x86, 8 vCPU shared, load 0.5–3.2 across the runs, no swap pressure.
  Files: `record/` (execution 1 draws), `draws/` (execution 2), `analysis-record.txt`,
  `regen.txt` (per-fire verdicts), `analyze.py`.

## Predictions

`predictions.md` was written before the decisive draws. Held: P1 (fire ⇒ PRE D > 0
matching fin_hi − s0 — 6/6), P2 in substance (armed precedes fire at lineage level with
identical margins, 5/6; the 6th is publish-blind, a case P2's letter did not name but
e517's soundness note predicted), P4 (`out=` never opens, 0/267), P6 (margin 2.0: no
fires, A ≤ 0 or '-' never contradicted... measured: armed A > 0 is common at 2.0 but no
clash realizes — P6's "never arm" letter is wrong, its no-fire half holds), P7's
direction (8704 fired 3/8 vs 4352 0/6 in execution 1; execution 2 fired a 4352 seed —
incidence is scale-coupled in expectation, a race per draw). **Missed as pre-registered**:
P3 (all non-fatal m = 0) — 94/261 land at m < 0; this is the equality attractor's
failure to transfer, the run's second finding. P5's letter (b ∈ affected of the fatal
RB) — the violated region is a descendant carrier, not an armed lineage; the correct
statement is the closure one.

## What would make it wrong

The instrument is e517's code, not an independent implementation: a shared bug in what
PRE computes (its box: fin maxed over `descendants([stride, truth])`, danger margin) or
in what HAZ's armed margin measures would fool both runs — agreement between this run
and e517 is not independence on that half (the memo-artifact lesson). The independence I
can claim: a different scene family (galaxy battles vs loose-gas churn), a second
execution whose incidence moved (different seeds fired, same law), and the m<0/slack
finding which *contradicts* the shared instrument's earlier record rather than agreeing
with it. A checker should re-derive PRE's D for one fire by hand from the RB/FIRE lines
(fin_hi − s0), which my analysis already does mechanically (match_d), and probe the
publish-blind class further (is it always a between-publish dispatch, or can an armed
pair also go blind?).

Cost of adoption: zero code (print-only; assert untouched). The decision it serves: the
engine-side fix (od 1) should gate at certify (D ≤ 0), not at publish (A ≤ 0); its test
scene stays the converging-fleet battle at margin ≤ 0.5, and its soundness argument
cannot lean on the boundary-attractor reading.

Fit with PRINCIPLES: "a failed expectation is not automatically a failed method:
diagnose which one broke" (the P3 miss is a scope correction to e517's record, not a
kill of the certificate); "agreement is not independence: several results from one
harness share its bugs" (declared above); "the simulation decides; heuristics schedule"
(the planner absorbing every meeting at margin 2.0 while armed is the scheduler doing
the work — the defect is the publish/rollback boundary, exactly the page's standing
verdict).

## The lens

Dynamics read: the fire is a state-decided instability whose *incidence* is a race but
whose *occurrence* is fully determined at certify — an attractor question answered with
a certificate rather than Monte Carlo. What the lens may have missed: the load-coupling
of incidence (Kingman-side) I recorded but did not model; and the cost side of the
fix (hold-while-armed starvation) is e517's measurement, not re-flown here.
