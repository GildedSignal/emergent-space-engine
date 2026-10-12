# Five lessons for B12-v2 (the instrument: bounded vs compounding error on chaotic ships)

Bottleneck argued for: HANDOFF risk "the instrument: B12 cannot yet tell bounded from compounding
error"; redesign in flight (`q-b12-design`, `b12-v2`) after the recurrence ratio failed. All quotes
verified verbatim from the Readwise export (`readwise-cache.json`).

1. Classify the scaling class, not the size.
   "Remember this: the Gaussian–bell curve variations face a headwind that makes probabilities drop
   at a faster and faster rate as you move away from the mean, while 'scalables,' or Mandelbrotian
   variations, do not have such a restriction." — Nassim Nicholas Taleb, The Black Swan.
   Mechanism: the diagnostic question is scale-free — does the error's range saturate, diffuse
   (√t), or run away (t, e^λt)? A global growth exponent mixes the three with the ramp transient.
   Change: B12-v2's statistic is Ĥ = slope of log R(k) vs log k (R(k) = median window range) over
   the top 3 dyadic octaves, per seed, verdict on the median seed; thresholds 0.33/0.67 frozen from
   a planted calibration (method.md #9). Test: `python3 probe_b12.py` (this run).

2. Shock it; don't only watch it.
   "And we can almost always detect antifragility (and fragility) using a simple test of asymmetry:
   anything that has more upside than downside from random events (or certain shocks) is
   antifragile; the reverse is fragile." — Nassim Nicholas Taleb, Antifragile.
   Mechanism: perturbation response beats passive observation (Lorenz twin runs; ensemble weather).
   Change: B12-v2 adds a twin arm on a few seeds — two runs differing by one quantum; the same Ĥ
   classifies the separation series (bounded law: separation saturates; compounding: diffuses).
   Test: run the classifier of `probe_b12.py` on the plane's twin-separation series (next run).

3. Sampling frequency sets the noise-to-signal ratio.
   "The more frequently you look at data, the more noise you are disproportionally likely to get
   (rather than the valuable part called the signal)..." — Farnam Street, 20 Aphorisms from Taleb.
   Mechanism: dense sampling feeds the gate the floor, not the law. Change: B12-v2 samples the
   Jacobi error at canonical dyadic ticks (matches replays-at-canonical-ticks, taste log 5 Oct).
   Test in this run: stride 1/7/11 changed the exponent only 0.122→0.142 — the risk did NOT bite
   the max-accumulate form; the lesson stays a caution for any denser statistic, not a measured
   failure.

4. Decide per seed, then take the median; never pool first.
   "By a law of probability called distribution of the maximum of random variables, the maximum of
   an average is necessarily less volatile than the average maximum." — Nassim Nicholas Taleb,
   Fooled by Randomness.
   Mechanism: pooling before the decision hides per-seed tails (the plane's 16 seeds are the
   sample, not one curve). Change: per-seed Ĥ with q10–q90 reported, gate verdict = median (the
   board's own criterion rule, now with its reason). Test: per-seed intervals in
   `probe_b12_metrics.json`.

5. A gate with knobs gets spent.
   "The more information you give someone, the more hypotheses they will formulate along the way,
   and the worse off they will be. They see more random noise and mistake it for information." —
   Nassim Nicholas Taleb, The Black Swan.
   Mechanism: every tunable parameter is a degree of freedom a builder consumes until the gate
   passes (B12's own history: threshold, floor, "among those whose error rises above").
   Change: B12-v2 ships zero tunable parameters — fixed dyadic octaves, thresholds frozen from the
   planted pair, integer gap in units of the calibration classes. Test: the calibration JSON is the
   frozen artifact; any retune is a redesign, not a pass.
