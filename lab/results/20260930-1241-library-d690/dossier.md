# Dossier — 20260930-1241-library-d690 (lens: Julien's library)

- **Claim:** His own library argues the causal automaton's decision layer should be absorbing binary threshold flips with an occupancy rule for aggregates (n* = (1/ε_count)²), and both claims carry measured support: 6–17× tighter aggregates across independent populations and 3–4.5× lower sustained aggregate fluctuation at N up to 10⁶, with no smoothness inversion.

- **Bottleneck:** 0 (representation: the law's form), feeding 3 (cost at a billion) and 4 (smoothness). Expected gain: order of magnitude fewer aggregate surprises to schedule and store — faction state that has stopped changing costs nothing, forever ("compute only surprises"). It lets us delete the graded-AI evaluation layer (utilities recomputed every look) in favour of threshold crossings.

- **Evidence:** `work/experiment.py` (numpy), full run ~8 min; checker mode `FAST=1 python3 experiment.py` = 40 s, same calibration. Readwise export cached at `work/readwise.json` (758 books, 4,484 highlights; 9 API pages).
  - Laws matched at N=10³ only (same mean faction fraction 0.30, same activity 0.356 flips·agent⁻¹·step⁻¹), all else held out. Full-run numbers:
    - cross-population SD of the aggregate: binary 8.1e-4 / 3.6e-4 / 7.3e-5 at N=10⁴/10⁵/10⁶ vs graded 1.4e-2 / 2.2e-3 / 4.4e-4 (17× / 6.1× / 6.0×).
    - sustained time-SD (ongoing surprise generation): binary 7.2e-3 → 2.1e-3 vs graded 3.0e-2 → 9.7e-3 (graded keeps diffusing — a compounding error, P13).
    - flip-rate tail p99/p50 ≈ 1.0–1.2 for both: no avalanche catastrophe (B4 not endangered).
    - 1% forced flips (player wildcard) at 10⁵: no amplification for either law (1.2e-4 vs 2.2e-4).
    - Poisson dipole fluctuation × √n constant to 5.8% over n = 10²–10⁴; n*(2⁻⁸) = 6.55e4.
  - Reproduce: `cd lab/results/20260930-1241-library-d690/work && FAST=1 python3 experiment.py` (40 s) or without FAST (~8 min).

- **Predictions:** `predictions.md`, written before the run. Held: 1 (binary < half graded at every held-out N — in fact ≤⅙), 2 (same attractor 0.295±0.01 at every N), 3 (tails ≤ 3×, no inversion). Half-miss: 4 — graded did *not* amplify under 1% forced noise; the stress case was too weak to discriminate. Marginal: 5 — 1/√n constancy 5.8% against a predicted 5%, driven by the n=10² point. 6 is an identity checked via 5's scaling.

- **What would make it wrong:** the toy laws are contagion/averaging, not physics; a graded law with a restoring force (not linear renegotiation) could close the gap, and critical-density regimes (avalanches) were not probed — a binary law near a percolation threshold may yet grow heavy tails. Adopting lesson 1 costs one design decision (dyadic thresholds on AI state) and nothing else; lesson 2 needs the count quantum chosen, which is B5's open question anyway.

- **Fit with PRINCIPLES:** lesson 1 — "Nothing is evolved that can be derived when looked at" and "we only care about changes" (P3/P14): an absorbed flip is never re-derived. Lesson 2 — "Store the generator, not the generated… ships' aggregate mass can become a source" (P6). Lesson 3 — "a fix signals the wrong representation" (P19). Lesson 4 — "no work for no reason, so no ticks" (P14). Lesson 5 — "Spacetime, not space plus time… gravity is compiled into geometry held by cells" (P7).

- **The lens:** his Readwise highlights are dominated by self-improvement and business books; the practitioners closest to our problem (Kelly Johnson, Boyd, Jaynes, Dörner, Perrow, Minsky, Hayek) sit unread on the goodreads to-read shelf, so this run leans on Taleb/Asimov/Ries/Graham plus one toy experiment. Four of five lessons sharpen candidates already on the board rather than overturn one; the new content is the variance numbers, the n* formula, and the interior-blindness invariant for sheets. A physics-lens run must repeat the law-form comparison with a real faction layer before adoption.

- **Grade suggested:** silver — real, reproducible in ≤ 60 s, predictions pre-written; one named experiment away from gold (the same comparison on the engine's own faction aggregates at billion scale).
