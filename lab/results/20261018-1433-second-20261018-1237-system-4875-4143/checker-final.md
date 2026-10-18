Working...
Check complete. **Grade: gold** — written to `check.md`, one page correction applied, tree restored.

**Verdict basis:**

- **Reproduced:** `regen.sh` exit 0; my own reruns match every dossier number within load noise — collapse 264.6 → 1.20 ms p50 at 10,071 bodies (217–220× across three regens), engine digest `03abdbc9…` bit-identical with/without `--rows`, engine p99 4.4 ms inside budget, wire 26 KB vs ~2 MB, fill linear.
- **Predictions:** all 8 held (written before the matrix); both misses disclosed by the author (readout run-average, warm-up transient).
- **Adversarial:** 10⁵ bodies — outside the author's range — steady p50 **1.35 ms** and worst transient frame **677 ms ≈ the predicted 6.8 µs/body fill cohort**; held-out seed 3 audit **0/822 violations**; RSS 271 MB.
- **Novelty:** exactly the flyable-frame page's open direction #1; prior figure was example-harness authority. Board #1 bottleneck moved 220×; PRINCIPLES #1/#28/#3 all served.

**Two letter-level errors found (immaterial, named in check.md):** the audit *is* charged to the frame (code order contradicts the dossier; 36 hitches = 36 audit frames, p99 23.5 ms), and "tests pass" — 2 lib tests fail, but pre-existing at pristine HEAD (the documented cross-machine red), no patch regression. Page corrected: exactness band broadened from the single-run "0.32–0.39%" to "≤1% (0–0.98% across reruns and seeds)".
