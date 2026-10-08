Grade: gold

**Abstract.** Claim: on the shipped plane's real kick stream (24,520 engine kicks dumped through `emergent-universe`'s public API), the naive per-source news channel grows ∝ R² (1.957) while the cell-owned octave accumulator's rate saturates O(1) beyond the largest source's firable radius, because impulse news is 1/d³ — the silver's log R tightens to saturation. Reproduced bit-exact: both CSVs md5-identical from a clean build, stdout identical, JSON deterministic; massive-only streams bit-identical to the full plane (md5s match, ships massless, never sources). Gain 358× at 1024 AU at the engine's own Q (player registers verified: step 2²², quantum 2⁻⁷⁴), unbounded ∝ R². Cancellation (0.52–0.74) and aligned-grid correlation (≤1.09×) measured, both safe; my seed and burst attacks strengthen it. Adoptable: cursors inside per-mass-class r_b (4.8–970 AU), saturating accumulators beyond; far octaves at coarser cadence.

## Reproduction

- Clean tree, `work/patch.diff` empty (0 B), `git status` clean outside `lab/results/` — "no crate edits" verified. `cargo build --release` 18 s; `kickdump massive` 1.7 s and `kickdump full` 5.3 s both **md5-identical** to the stored CSVs (`8445e731…`, `89888a23…`). `news_engine.py --selftest` OK; main run stdout **byte-identical** to `run_out_engine.txt` (`d24f0b07…`); two re-runs give identical `news_engine.json` (md5 `0635c434…`, 7.6 s). Caveat: the dossier's commands run the script in place (`RUN="."`), so reproduction overwrites the stored JSON — I did so; the stdout identity plus determinism carry the proof.
- The masslessness premise holds: `massive_only` is a literal-faithful copy of `scenario::plane_with`'s massive construction; only planets (`add_doll`) and the moon (`make_source`) are sources; the full plane's massive-body streams are bit-identical to the massive-only run over the shared 2×10¹⁰ window (Cinder `347771aa…`, Home `d0a611c4…`, Moon `cac0bd29…`, Giant kick-free identically) — exactly the dossier's md5s. `AU_T` equals the engine constant `AU = 101_300_000`.
- Every headline number regenerates from `news_engine.json`: naive 3.07e-9→7.89e-6 tick⁻¹, exponent 1.957/1.956; saturation at Q·10³ 5.39→5.62→5.62e-10 (flat, 3 digits) and near-flat at Q_engine (2.19→2.20e-8; the 970 AU Giant tail); ratios 358 / 1.4×10⁴ / 3.9×10⁶; shell decay −0.973 = the shells-4–9 fit (−0.674 ln per log2), ratios 0.49–0.64 = shells 5–9; r_b 4.8/8.2/35/970 AU recompute exactly from `own_system` medians; s/Q = 565/2.2×10³/4.4×10⁴/8×10⁶; the player's step 2²² and quantum exponent −74 verified in the B-lines.
- Predictions: `predictions.md` mtime 20:00:03Z precedes all output (`news_engine.json` 20:09:10). Frozen P1, P3–P6 held; P2-as-frozen failed (increments halve, not hold) exactly as the timestamped addendum pre-declared, and the author reports the frozen text as the prediction of record failing — the right epistemics (H0183: diagnosed, not hidden). P5's ±5% band was exceeded at 9% (Q1: staggered/aligned 1.093), safe direction, cause named (flooring loss).

## Attack (my own cases)

1. **Placement seeds 777 and 313:** naive exponents 1.959/1.990; saturation intact (Q3 4.57→4.57e-10 and 4.09→4.09e-10; Q0 +0.5% over 512→1024 AU). The shell exponent ranges 0.87–0.97 across seeds — see Missed #1.
2. **Burst tail (the author's admitted unmeasured case):** ×1000 dv on 0.1% of kicks moves the accumulator at Q_engine by +1.4% (2.23 vs 2.20e-8). Even a Jupiter-class dv burst stays absorbed; breaking saturation needs a large *fraction* of kicks to be huge. The blind spot is quantitatively small.
3. **Correlation range re-check:** aligned ≤ staggered at every Q (Q0–Q3: 0.92–0.99×; Q4 0.84; Q5 0.55) — the inflation bound holds everywhere, though the dossier quotes only the Q0–Q3 window.
4. **Extrapolation arithmetic:** at a 10⁶ AU horizon, naive = 7.53/tick → 5.0×10⁴ per 33 ms frame ✓, but the accumulator at Q_engine is 2.2e-8 × 6710 = **1.5×10⁻⁴/frame**, not the dossier's "4×10⁻⁶" (that is the Q·10³ saturated rate × frame). Wrong by ~40×, same conclusion (both free; the gap is ~10⁸).

## Novelty

Builds on today's scout-141c (silver, `claude/lab-20261008-1859-scout-141c`), whose checker named this exact experiment and this exact π defect; the correction matches. No HISTORY entry measures news scaling on engine events; b-news-gravity is the in-system cursor mechanism, not the scaling law. The deltas are real: engine event stream, engine-anchored Q from the player's registers, measured cancellation and correlation, the log→saturation tightening.

## Goal fit

Answers the growing-cone risk (OC#50) on the engine's own stream, and corrects a claim of record (the silver's log R → O(1) saturation): "shows that a premise is wrong". PRINCIPLES: P6 ("influences below one quantum accumulate" — now on engine events), P3/P14 (compute only surprises), P23 (arrivals at t_e + d), P33 (r_b is the scale's own quantum crossover). Deletes the per-source cursor as a galaxy-scale structure and bounds the 2.6 GB accumulator Fermi to an upper bound. It is a design input, adoptable in one step, same standing as the co-orbital gold.

## Why gold despite the defects below

Reproduced bit-exact from shipped code; predictions frozen before output with the one failure honestly pre-declared and diagnosed; the two engine-physics falsifiers the silver's checker named (directional cancellation, correlated kicks) were measured, one surprised within its band and neither killed; my adversarial seeds and the burst tail strengthen the claim; and it corrects the record's law (saturation, not log). The defects are peripheral, safe-direction, and none touches a load-bearing number.

## What the author missed

1. **The −0.973 exponent is constructed, not discovered.** s ≡ s_loc/d³ by definition and systems are placed uniformly, so expected shell sums ∝ 1/r (exponent −1) identically; my seeds give 0.87–0.97 around it. Calling it "measured" repeats the scout's closed-form-in-MC-dress weakness in miniature. What is genuinely measured is the bounded kick sizes, rates, directions and grid alignment — say so.
2. The **declared negative control** (Q_engine·10⁻⁴ → accumulator = naive) never ran; the sweep only goes coarser (10⁰–10⁹).
3. The 10⁶ AU extrapolation mixes Q's (4×10⁻⁶ is Q·10³'s accumulator; Q_engine's is 1.5×10⁻⁴/frame) — the only headline number the record cannot regenerate as stated.
4. "24,525 kicks" contradicts the record's own headers (24,520; predictions repeat the wrong count).
5. The aggregate-crossover "slope −0.301" is an octave-grid artifact (three points at 16/32/64 AU, then pinned at the sweep floor 16 AU for Q ≥ Q·10² — the JSON's all-Q slope is −0.046). The load-bearing content is the exact per-source algebra r_b = (s_loc/Q)^{1/3} and the pre-registered −1/3-vs−−1/2 discriminator, which held.
6. The addendum's timestamp (20:25Z) is inconsistent with its file mtime (20:00:03Z, which is what actually precedes the 20:09:10 output). State clock evidence, not asserted timestamps.
7. Correlation quoted as "0.92–0.99×" is the Q0–Q3 subset; at Q4–Q5 the effect is larger (0.84, 0.55) in the same safe direction — report the full range.
8. Saturation at Q_engine itself is only measured over the half-octave past the Giant's 970 AU tail within the 1024 AU sweep; it is directly measured at Q·10³ and consistent at Q0 (+0.5%), but the headline conflates the two.
