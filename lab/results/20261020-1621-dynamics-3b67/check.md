Grade: silver

**Abstract.** Claim: c644's self-quench is terminal — flown to 98,304 ch on c644's harness verbatim, the belt's escape hazard decays to zero (λ 0.21/0.12×10⁻⁵/ch), late deaths are skirt apocenter crossings, and the endpoint is a ~150-body sub-quantum clump carrying a 3.7–5.1k contacts/ch standing rattle at frozen ke_in. Reproduced bit-for-bit (digests `ed2783d6…`/`6483a3b2…`, every dossier number exact). Checker probes at 147k ch and seed 3 confirm the terminal verdict (7 deaths in 49k ch past 98k; three zero windows) but break two letters: the rattle is still rising at 147k (5805 c/ch, budget is horizon-bound) and seed 3 shows 3/33 late deaths core-resident <10q. Gain: the belt's lifetime cost is one storm plus a standing rattle; the death ledger retires at ~2× the storm. Adoption: nothing to build.

## Reasons

1. **Reproduction is exact.** Clean tree, patch applied fresh, own build: both arms' digests and contact totals identical (`ed2783d6…` 288,352,399 / `6483a3b2…` 267,106,591); `analyze_tail.py` regenerates every dossier number to the digit (tail deaths 35/18, λ 0.208/0.118 ×10⁻⁵, r² 0.92/0.86, last-8k contacts 5071/3693, ke ratios 1.0341/1.0162, late-death fracs and medians, prefix 492/63,461,214 and 498/88,881,906). The runner's regen and my independent flights agree.
2. **Predictions were pre-registered and honestly adjudicated in the main** (mtime 16:24, before the flight window; P4 reported as falsified, P1's standing-leak reading reported as falsified) — but P1's remnant clause named **n_in** at 98k in [240, 320]; measured n_in is 333/358, both outside, and the dossier adjudicated "remnant landed in range (273/284)" on **alive** without saying so. An undisclosed criterion swap on a sub-clause (the r3v3 lesson).
3. **Adversarial probes (three, one outside the author's range):**
   - **147,456 ch (3× c644's horizon, cold s1):** terminal verdict CONFIRMED — deaths past 98k total 7 (windows 4, 0, 0, 1, 1, 1); n_in ~332 stable. But the rattle does **not** station: last-window contacts/ch 5071 → 5805 (+15%), zones <2.1q 151 → 168 bodies, median live r 1.51 → 1.19q. The clump is still contracting at 147k — exactly the "second, slower contraction stage" the lens flagged. The "PERMANENT budget ~2.7–3.4k c/ch" is a lower bound at any finite horizon, not an asymptote.
   - **Cold seed 3 to 98k (new arm):** same class (λ 0.236×10⁻⁵, r² 0.97, rattle 3756 c/ch last-8k, ke 1.11) — but **3/33 late deaths are core-resident below 10q** (frac 0.091; frac<30q 0.273). "The sunk core EJECTS NOBODY" is a two-seed letter, not a law; the skirt still dominates (median late r 73q).
   - **Micro-state (from snaps):** the clump does not melt into fewer pairs — 149 hot bodies carry 99.6% of incidence with top-5 per-body rates 88–89/ch, matching the reported p90 85.5/max 88.1; the lens's "merge" worry is unfounded at 98k.
4. **Novelty:** c644's page named "the core's own evaporation tail past 49k" as the leftover; no run flew past 49k before (page Runs, docs/HISTORY.md, git log all silent on it). Not a repetition — it decides c644's open (a)/(b)/(c) question: (a) wins with a still-tightening rider.
5. **Page:** the fold-in is faithful and additive (c644's lines preserved, strikethroughs bracketed; the Runs-section change only de-duplicates a pre-existing double e56b line, fuller variant kept; the consolidated Open-directions item loses no record not present in the 9b3b entry). I corrected it in place: a checker block with the 147k non-stationarity, the seed-3 core leak, and the n_in letter.
6. **Instrument nit:** `analyze_tail.py`'s `alive[]` decrements once per death chronon, so same-chronon deaths collide (527 events on 514 chronons in B'): windows' `alive_end` reads 286 vs the true 273. The dossier text used correct body counts; hazard denominators shift <2%.
7. **Goal fit:** decides the belt page's re-birth/cost question and retires compute ("No work for no reason, so no ticks", PRINCIPLES 14; "Compute only surprises", 3 — the clump is the only surprise left). Belt is a board-named topic (memory at 10⁹). It kills a premise (the never-closing ledger), which is gold-shaped, but two of its own absolutist letters die under the probes above, so the sentence as written is not adoptable verbatim.

## The one experiment that would make it gold

Already half-flown here: extend the cold arm to ≥147k on ≥3 seeds (I flew s1@147k and s3@98k) and re-freeze the claim's letters on that data — "terminal quench, hazard ≤ ~0.2×10⁻⁵ and falling at 3× the storm horizon; standing rattle ≥ ~4–6k c/ch and still creeping; core leak ≤ ~10% of the (already tiny) tail". One 20-minute window, no new harness; everything else already reproduces bit-for-bit.

## What the author missed

- The rattle's non-stationarity is measurable inside their own budget: the 147k arm costs ~10 min more than a 98k one and would have shown the +15% creep — the "permanent budget" constant is not yet a constant.
- A third seed was cheap and is the difference between "ejects nobody" and "ejects almost nobody" (3/33 core-resident late deaths on s3).
- The P1 remnant clause was adjudicated on `alive` where the prediction said `n_in` (333/358 measured, both outside [240,320]) — undisclosed swap.
- The `alive[]` same-chronon collision in the analyzer's windows (527 vs 514) — cosmetic here, but the column is what a future reader will diff against.
