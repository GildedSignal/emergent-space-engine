# dossier.md — library lens, run 20261008-0945-library-51bf

**Claim.** For the cadence bottleneck (q-cadence), the practitioner library says the ladder is
the easy part and the sensor is the load-bearing one — and the only published per-seed cadence
data (quant-5022) confirms it: no recorded dimensionless number orders a body's needed kick
rate (e0 ρ=+0.36, a0 +0.67, μ +0.27), an e-only ladder misses a held-out seed by two ×2 steps,
and per-body tuning alone caps at 1.92× even-weighted on quiet hierarchical seeds, so the
queue's 10× must come from deletion (the averaged layer), not rate tuning.

**Bottleneck.** Board #1: "fewer kicks per orbit at the same behaviour... kicks dominate the
engine's cost"; the taste log names cadence the lever; `q-cadence` is queued. What this run
changes: the cadence rule's gold criterion (sensor inputs to record; max-aware judging;
~2× ceiling for tuning on quiet scenes) and its risk order.

**Evidence.** All quotes verbatim from Julien's Readwise export (cached: `rw-page-0..8.json`,
9 pages; flattened `highlights.tsv`, 4,580 highlights). Deliverable: `lessons.md` (5 lessons,
each with quote, mechanism, change, test). Decisive probe, reproducible in < 1 s:

```
cd lab/results/20261008-0945-library-51bf
for f in decisive.jsonl tuning.jsonl; do git show \
  origin/claude/lab-20261004-0555-quant-5022:lab/results/20261004-0555-quant-5022/$f > data/quant-5022-$f; done
python3 probe.py          # writes metrics.json
```

Gate logic copied verbatim from quant-5022's `verdict.py` (apsis within 10% of its 1024-events
reference, emax ≤ 1.2×, maxdJ ≤ 10× its 64-cadence control); B1/H3/H4 stay judged-out as the
author ruled. Per-seed minimum kdk cadence (events/orbit): T1 (a .55, e .05) **8**; T3 (1.70,
.05) **32**; T2 (.70, .20) **64**; H1 (.62, .30, near 2:1) **64**; H2 (.48, .10, μ 3e-4)
**16**; H5 (.55, .60) **16**. Sum 200 vs uniform 384 → ceiling **1.92×**. Eccentricity is not
the driver (H5 at e 0.60 needs 16; H1 at e 0.30 needs 64); perturbation strength and resonance
distance — the numbers quant-5022 did not record — are.

**Predictions.** `predictions.md` written before `probe.py` ran. P1 held (4 of 6 seeds below
64; my "≥ 2×" inference landed at 1.92× — near-miss, disclosed). P2 and P3 were wrong and
informatively so: I predicted e0 would order the rate (ρ = 1); it does not (ρ = +0.36), and the
e-only ladder fitted on T1–T3 misses H5 by two steps and even T1 in-sample. The fallback clause
fired: no single recorded number is the sensor. A failed expectation about a lesson, not about
the method (H0183): the thermostat lesson survives with its sensor requirement sharpened.

**What would make it wrong.** Six seeds from one run's 2D prototype (circular planet, massless
ship, kdk only), μ nearly fixed, Spearman on six points; minima inherit that run's tolerances.
If the integer engine's grid or tolerances move the minima, the sensor ranking could change —
but H5-vs-H1 (e inverted) is a two-step gap, robust to tolerance jitter. Cost of adopting:
nothing to build; a criterion for q-cadence: record τ, synodic detuning and Hill-gap per body,
judge gains max-aware, and expect tuning to buy ~2× on quiet scenes (more only via deletion or
population-weighted spread: a belt of T1-like bodies under one H1-like body would gain ~8× on
the quiet fraction). Fit with PRINCIPLES: "Compute only surprises" (3); "a fix signals the wrong
representation" (19); "a body resolves only the influences that are significant at its own
scale" (33).

**The lens.** Analogies are cheap: I kept only lessons whose test ran on real published data,
and two of my three pre-registered expectations failed — the library suggests structures, the
probe decides. The corpus holds no Kelly or Shannon text, so ruin/entropy entered only through
Taleb and Forte; I did not weight quotes by Julien's goodreads ratings, which a reread should
do. Nothing here edits the crates or gates; grades welcome a checker's blind reproduction.
