Working...
Check complete. **Grade: gold** — written to `lab/results/20261009-1259-constraint-2666/check.md`; tree restored clean.

**Reproduction** (patch applied to clean tree, all dossier commands):
- 30 s rtf 100: crossing 2.696 of bodies 2.805 ms (96.1% vs author's 96%), readouts/frame 63.5, surprise 57.2, lt_150m = 1.000 — same conclusions.
- 417 bodies: gather 61.8% share (author 61%), overflow 337/1200 (author 338), lt_150m 0.999.
- Kick-bench: exact — 32 samples, median 47.3 µs, 0.056 s of 20 s wall (kicks = 0.3%).
- rtf 1000: lt_150m 0.715 vs author's 0.716.

**Attacks** (3 of my own): unpaced — crossing still 96.8% of the loop, so not a pacing artifact; unseen seed 7 — shares and extrapolation hold; purity control — release suite green with probes (54/0), debug failures are pre-existing on the clean tree (lattice `law.rs:346` overflow), patch-independent.

**Predictions**: 1 and 2 held numerically; 3 refuted and disclosed, then converted into the measured advance-then-refresh mechanism — the claim doesn't rest on the refuted form.

**Novelty**: H0210 knew the gather dominated the frame and H0211 shipped the memo; the new, measured facts are the memo's ceiling (the exact readout itself is the cost), the skip refutation at player floors, and the advance viability with horizon scaling — a premise correction adoptable in one builder step.

**Main caveats recorded**: the 25–40× is assembled from measured components, not a built cadence (one-frame advance from a fresh base ≠ k-frame survival); the player floors are asserted, not derived per doll scale; the "green" test claim is release-only.
