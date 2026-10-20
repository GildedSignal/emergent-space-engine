Working...
Check complete. **Grade: gold** — written to `check2.md`, with the corrected page in the run's `wiki/`.

**What I did (independent of check 1):**

1. **Reproduced** `regen.sh` in a clean tree: every count bit-for-bit (T = 1 at N = 10⁴/10⁵ while the shipped tier BAILs; F = 470/4,209; offline 113,731/1,085/216,759 and 113,701/1,067/212,070). Walk 49–105 ns/body across four runs — the dossier's 64/105 sits inside the spread. `predictions.md` (11:26) predates the decisive raws (11:35).

2. **Six adversarial arms** (my own probe, since removed; tree clean):
   - **e readout is exact** — `|2^48/k − 1 − e_apsides| ≈ 9.7e-4` (one 2⁻¹⁰ draw quantum; `orbit.rs:33`: k is the mantissa of 1/(1+e)). The wiki note claiming `e/(1−e)` inflation was wrong — corrected on the page.
   - **Formation** (10⁴ crowd on the scanner's orbit): kept whole, 0 misses, linear — no taleb-09b5 quadratic ruin at the observer.
   - **Hot belt** (e-bulk 0.3): F floods to 42% for T = 23 — the 21–24× is e-bulk-bound, outside the author's range.
   - **Crosser sweep** 0.001–0.03 c: T = 0.065/0.51/4.5/21.7% — linear in v·h, as claimed.
   - **Index at 10⁷**: 0.062 µs/query (decade up).
   - **Standing anchor Δt > 0** (the author's named unflown check): with the stored n, 0 misses to Δt = 0.25 P; the example's bare-2c form loses half the truth at 0.05 P and all of it at 0.25 P — the n term is required and sufficient.

3. **Page corrected in place.** The author's page was destructive under `wiki.py apply`'s three-way merge (placeholders "(prior page's … unchanged)"; base commit == current published page, verified), which would have deleted the 5f36/b083/604c/0552/c439 blocks and all refuted lines. Restored full prior content with the 4f59 result folded in.

Soundness is theorem-grade given exact readouts (chord bound + range overlap — the same laws as `crates/encounters/src/phase.rs:39–44`, where the author's citation lands line-exactly); P3's ratio miss is disclosed and is the finding itself: the walk overreads N/T ≈ 10⁴–10⁵×. Moves live question 1's seam term ≥ 10×, adoptable in one step (schedule-only index, exact predicate unchanged).
