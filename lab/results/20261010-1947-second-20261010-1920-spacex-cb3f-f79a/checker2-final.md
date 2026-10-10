Working...
Second check complete: **Grade: gold** — written to `check2.md`, tree restored clean at a838a28, nothing else in the run folder touched.

**What I did** (45-min window, all runs single-threaded, well under 2 GB):

1. **Reproduction.** `work/patch.diff` is self-contained (subsumes the original's); applied alone to clean a838a28, built in 10 s against `lab-target-3`. Baseline `d4413b80…` exact; the 9/9 safe-filter matrix at 5e8 exact including pair and rejection counts; 3×10¹⁰ digests identical at both places (3 019 749 pairs, 3.98–4.02 µs/pair, 611 777 co-radial contacts, +8.5% co-radial overhead); both frontier digest breaks `cad102e0…` and `a27c2800…` regenerate **bit for bit** under my rebuild of the 2⁶¹ tightening.

2. **Adversarial.** Fresh seeds 31337/99 × 3 places: 6/6 safe, zero misses. The 2⁶¹ bound misses 2–4 real encounters on *every* separated-annulus seed I ran — including seed 7, which the dossier wrongly calls safe (kill strengthened). Cohort 100→400: µs/pair flat 3.96–4.15 — the linear ~4 s/item wall at 10⁶ stands. `FASTDOLL`: bit-safe but only 1.5×, not the predicted 3× — the author's demotion to lead was correct.

3. **One self-inflicted artifact**: my tight-bound rebuild raced a background 3×10¹⁰ run, producing a false mismatch; the clean rerun is identical. Flagged in check2.md for transparency.

4. **Record defects named** (non-load-bearing): stale "0 rejected" P-files (shipped patch rejects 36), the non-regenerable "92%"/`8c84c079` variant, the "0.07–9%" comment contradicting its own artifact, empty `run.log` — predictions order carried by mtimes (19:58 < 20:01+).

The gold rests on the pre-registered criterion from the original's checker — "a safe ≥10× on the scan intercept, **or a kill**, is gold" — with the premise correction (rejection information lives inside the decode) reproduced on both sides of the safety frontier.
