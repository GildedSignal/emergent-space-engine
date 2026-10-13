Working...
Check complete. **Grade: gold** — written to `check2.md`, with one page correction applied.

**What I verified:**

- **Reproduction:** `regen.sh` end-to-end in a clean tree (109 s). Every deterministic number matches the dossier bit-for-bit: all four scene blocks (CV/Gini/Zipf rows, player shares 21.1/17.9/70.6/0.2%, haulers 0–2 kicks, member mean 20.6/max 174/p50 5), store rows (12.347/48.38 bits, 0 mismatches, 2,570 repacks). Timing-only rows vary run-to-run inside noise, as expected on the shared runner. Digest neutrality re-proven independently: `e0972a1c…` identical base vs patched; tree clean afterward.
- **Pre-registration:** `predictions.md` (22:57) predates the patch (23:11) and captures (23:15+); the content shows genuine priors with honest misses (P3's <20% idle bar missed at 21.1% on seed 1 — my seeds 7/11 give 17.9%/17.5%, i.e. seed noise at the bar).
- **Four adversarial cases, two outside the author's range:** seed 11 idle (tube CV 0.200 ✓); burn L15/keys-3 — player takes **100.0%** of body kicks (315,640 in 200 game-s), the driver-head at its extreme; **40,000 members** (10× the author's max) — member kicks p50 29 = max 29, top-1 0.006%, even flatter than at 4,000; burn seed 7 (66.1%, 816 sub-kicks ✓, and the page's 10/38, 8/37, 22/3,769 member sub-kick counts all verify on the raw captures).
- **Novelty:** this was the nladder page's own open direction 1; the flat-bulk half was near-known by construction (27ce's 1/128 — the author concedes this in the lens section), the new content is the measured head and rule 2's death.

**Page correction:** `step_for` is 1/2⁷ of the period (`step_log2` defaults to 7), not the dossier's 1/2⁶; added seed 11 to the confirmed list.

**Missed by the author (recorded in check2.md):** the 1/2⁶ slip; the deep-burn cost regime (~0.42 s wall per game-s, compute-bound on the player's stream); the 222 s wall for a 300 game-s settle at 40k members (a free ladder data point); hauler per-orbit numbers remain 1-kick extrapolations; the belt revival path unmeasured.
