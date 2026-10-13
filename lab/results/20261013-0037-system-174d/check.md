Grade: silver

**Abstract.** Reproduced from a clean tree (patch applied, regen.sh): demand mode is bit-identical — worst frames 42/579/1,036, cadence formula 2,283/2,293, tide/burn min 2.570×10⁻¹² / median 2.819×10⁻¹¹ / max 1.334×10⁻⁹, coast 19/19. The replan-storm guess is refuted (code-verified: `decide` clears the plan, plans one kick); the burst is the burn-cadence chain, and the carry-the-burn lever is new and priced. But the price "~0–2 field events" holds in demand mode and at L8–L12 only: the author's own paced-L15 output mints ~26,413 events (checker: 28,448 at seed 7, 31,284 over 8 s) against ~1,000 burst items — 44–147 plunge kicks carry 100% of the tide sum. The deletion near the plunge depends on a regime-scaled tide cadence the run neither derives nor measures. One experiment from gold.

## Reproduction

- Clean tree at 17ace3e6, `git apply work/patch.diff`, `bash regen.sh` (exit 0, ~22 s + build).
- **Demand section identical to the runner's regen.log and to every dossier number**: worst frames 42 (frame 62, L8), 579 (frame 60, L12), 1,036 (frame 60, L15); kinds kick0/boundary/open/decide as claimed; cadence check "thrust kicks 2293; mismatches 10"; ratio min 2.570e-12 median 2.819e-11 max 1.334e-09; coast control fires 19/19 at median 5.72×10⁸ (paced) / 5.24×10⁸ (demand) quanta.
- **Paced arm** reproduces in kinds and order of magnitude; wall-clock numbers move on the shared box (lag 1.587–1.667 s across reruns; strong-tide kick count 32–49), consistent with the page's own note that paced wall cost varies while item counts stay deterministic.
- `predictions.md` (00:47:26) predates `dossier.md` (00:55:31); its decisive content (P2's `tide_q == 0` letter) **failed** and is reported as failed — post-hoc predictions do not fail. P1, P3, P4, P5, P6 hold; P2's intent holds by 9–10 orders.

## Adversarial cases (mine)

1. **Seed 7** (author tested seed 1 only): composition identical (kick0 556 / boundary 554 / open 0 / decide 1 at L8; counterfactual ~0 events). The ratio range widens: L8 max **7.6×10⁻⁹** — "10⁹–10¹⁰ times less" is seed-1-demand; the honest cross-seed range is **10⁸–10¹⁰**. Mechanism unaffected.
2. **Paced L15, 8 s** (author: 2–4 s): alive 480/480; strong-tide kicks 49→147; counterfactual ~31,284. The plunge tail grows with flight length; per-kick tide saturates (~6.8×10¹¹ max, identical across seeds — the physics converges).
3. **Keys re-asserted every frame** (the real-client pattern, untested by the author): waterfall unchanged — kick0 554 + boundary 552 = 1,106, exactly the one-input total; only `decide` items add (181, outside `stats.items`). Confirms the `same`-keys flush path in code and behavior.
4. **The decisive attack**: the author's own regen output contains "paced L15 … would mint ~26413 events" (runner's log; my rerun 28,800) against 973–990 burst items. 47 late kicks carry **100%** of the tide sum (per-kick ~5–7×10¹¹ quanta vs the coast's 4.98×10⁸/event divisor). Under the run's own fixed-granularity counterfactual, the deletion **inverts** (~28× more events) at the very level whose 1,036-item burst is the sweep's worst stutter. The dossier's "mints ~0–2 events" and the bottleneck's "reduce to ~0–10 field events" are demand-mode/L8–L12 numbers presented as general; "more at higher levels" is wrong for paced L15.

## Novelty

docs/HISTORY.md has no waterfall entry; the live page's old direction 2 said "Unmeasured: why the replan mints that many items" — this run answers it and refutes quant-32ab's mechanism guess (`decide` verified in source: `plan.clear()` + one `plan_interval`, no refit of scheduled kicks). The carry-the-burn proposal is new as a priced lever; law.md's retired jet and reader ramps are precedent it cites, not the same claim.

## The page

Fold-in faithful in structure and the conflict resolution is chronologically right (5eb6's side), but I corrected it in place: (a) the current-best block, the refuted line and direction 2 now carry the paced-L15 counterfactual (~2.6–3.1×10⁴) with demand-mode scoping, and the seed-7 ratio maximum; (b) restored the dropped append-only run line `20261010-2141-constraint-ae40`; (c) reverted an undisclosed one-character id edit (`469c`→`464c`) to the committed `469c`. Not three agreeing golds — topic stays open.

## Goal fit

Moves `frame-cost` open direction 2 and prices the lever the in-flight fix builds would otherwise chase. PRINCIPLES fit is direct: "Compute only surprises … Nothing is evolved that can be derived when looked at" (3) and "you don't advance a ship tick by tick you just map where it wants to go" (14) — an exactly-solvable burn sampled into word-sized rebinds is compute-not-needed; "Store the generator, not the generated" (6).

## The one experiment for gold

Derive or measure the tide's per-event budget near the plunge and re-price the counterfactual with a regime-scaled carry: today's plunge kicks already deliver ~5×10¹¹ quanta/event (vs the coast's ~5×10⁸), under which the deletion wins ~30× even at paced L15 — or it does not, and the claim's domain gets that bound. Then "~0–10 field events" holds at every level or is honestly re-scoped, and the lever is adoptable within one step.

## What the author missed

- The 26,413 in his own regen output against the "~0–2" headline — the omission that costs the grade.
- Seed sensitivity of the ratio range (domain note says one seed; the range is stated as if general).
- The demand-mode turn flight never reaches its burn (script fires at 2.5 s; demand flights are 2 s) — P6's demand evidence is a pure turn; the paced arm covers it, but the blind spot is undisclosed.
- "49 late-flight kicks" is wall-clock variable (runner's regen: 32; my rerun: 49), stated as a fixed count.
- Page hygiene: the dropped ae40 run line and the silent id edit.
