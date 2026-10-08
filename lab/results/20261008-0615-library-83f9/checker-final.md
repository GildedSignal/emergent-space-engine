Working...
Check complete. `check.md` written; nothing else in the run folder changed (my reproduction overwrote the two JSONs with deterministic-identical output — every aggregate matched the stored values before the rerun — and my scratch files are removed; `patch.diff` is empty, git clean outside `lab/results/`).

**Grade: silver.**

What I did and found:

- **Reproduction:** `exp_cadence.py cold` (28 s) and `hot` (29 s) reproduce every stored number exactly. The dossier's interpolations recompute correctly: matching fixed16's median error costs ≈560k kicks (mag) and ≈500k (jerk) against the clock's 160k. The jerk trigger is strictly dominated at its best measured point — worse error than fixed16 at more kicks.
- **Adversarial cases (3, my own):**
  - *Truth convergence:* 512-vs-1024 floor is 9.6e-7, so the 6e-5 bar is ~60× above instrument noise.
  - *Perturber at 1.3 AU (2× field range):* triggers still lose (1.4–2.8× more kicks at matched median).
  - *Wide belt 0.7–1.45 AU (36× range):* triggers now genuinely allocate (k_p99/k_med up to 20) yet still lose 2.2–4× on median — but they **beat** the clock ~1.5× at matched p95. The kill is metric-dependent on heterogeneous scenes; the dossier argues median only.
- **Predictions audit:** P4 and P8 (pre-registered kills) fired; author honestly reports P1/P2/P5–P7 failing. **P3 is never reported** — from the stored JSONs it also failed.
- **Novelty:** no prior run tested event-triggered scheduling (the six cadence runs covered fixed rates, correctors, averaging); probe 1 killed per-body steps on error walking, a different axis. Lesson 5's citations (a9c2, dynamics-0c67) check out against the q-cadence lens. All six library quotes are verbatim in `highlights.tsv`.
- **Why silver, not gold:** the positive held-out predictions did not hold; the kill is measured on a surrogate, not the plane's kick layer; one of five lessons is measured; and "local derivatives carry no allocation information" overstates (they allocate — they just lose). The one experiment to gold: rerun the trigger family on the plane's own kick machinery (averaged tides, J2, resonant pair), judging B12/B14/B17 with both median and tail reported.
