Grade: gold

**Abstract.** The adopted co-orbital gold's rank-4 phase-neighbour certificate is unsound outside a
single stream: two crossing co-orbital fleets (the game's core scene) give catch@4 = 0% in the
mean-anomaly ordering at every refresh cadence (median rank 0.34n, constant in time; 73
encounters/orbit, dense-brute-force verified); λ-ordering needs k growing ∝ n·v̄·lead (k99 = 9 at
P/32); and even on one stream k is not 4 but grows linearly in ρ·n (max 13 at ρ=1e-3, n=4000; ~10²
at a 10⁶ fleet). The concentration signature (2.0 vs 2.7×10⁴ candidates/encounter) cannot route the
scenes apart; the certifiable property is single-streamness, which the Binet cone already computes.
Cost: none — `b-coorbital-cert` is in flight (HANDOFF:18–19, :69); adopt before it lands.

**Reproduction** (clean copy, nothing in the run folder touched; `work/patch.diff` is empty):
`python3 harness.py` 13.4 s → `metrics.json` **bit-identical** to the stored file; `python3 s2_hot.py`
7.8 s → `s2_metrics.json` identical; `python3 probe_crossing.py` 9.3 s → dense Kepler brute force
(4001 samples/pair) finds 30+42 = 72 of the 73 truth encounters (one wrap-edge pair skipped by the
probe itself, disclosed). Timings match the dossier. S0's conjunction truth is exact
(max_d at conjunction 4.5e-13).

**Predictions.** `predictions.md` (mtime 11 min before `harness.py`, 4 min before the decisive
`metrics.json`) contains paper numbers that *differ* from the measured ones (0.17n vs 0.34n; 220 vs
73/orbit; max 6 vs 13; 37 vs 98.8/orbit) — the signature of genuine pre-registration, not post-hoc
fitting. P1–P6 all held on the measured numbers; the two guard misses are paper-arithmetic errors,
disclosed by the author (S0 scene widened from ±ρ/4 to ±ρ/2 after predictions, disclosed).

**My adversarial cases** (fresh code, `two_fleets` in /tmp, same truth method):
- A1 seed 42, original geometry: 70 enc/orbit, M catch@4 = 0.00 at all leads, median 685, 100% > n/8.
- A2 e=0.05, ϖ_B=π/3 (shallower crossing): 73 enc/orbit, M catch@4 = 0.00, median 354 = 0.18n; λ@4 =
  1.00 at lead P/32 but 0.00 at P/8 — shallow crossings rescue λ only at short lead, exactly the
  author's k ∝ n·v̄·lead law; the adopted k should be sized by crossing transverse speed too.
- A3 per-body a-spread ±ρ/2 (quasi-periodic; the case the author said the lens might miss): 69
  enc/orbit, M catch@4 = 0.00 at every lead, median 665; λ@4 = 0.59 at P/32, 0.00 at P/8+. Exact
  periodicity is not the cause of the kill.

**Novelty.** No H entry inverts 20261006-0346-taleb-09b5; the nearest priors are r8 v2's
conjunction-less encounters (truth completeness, a different defect) and the gold itself. HANDOFF:69
still carries the premise; the build queues (HANDOFF:18–19) still carry the certificate. Novel and
timely.

**Goal fit.** "Gates… judge a representation; they never size it": the correction names the property
(single-streamness) the certificate needs — and it is already a Binet-cone output, so no new
mechanism. "A failed expectation is not automatically a failed method": the gold's measurement
stands (S0 reproduces catch@4 = 100%, max rank 4); its domain claim is what falls. This is the
inversion lens working as designed: the adversarial scene class (two fleets engaging on one ring)
is the game, not a corner.

**Why gold and not silver.** Premise of an adopted gold shown wrong, reproduced bit-for-bit,
held-out predictions held, robust under my three adversarial variants, adoptable within one step
because the corrected build is still in flight. Nothing measured remains between it and adoption.

**What the author missed.**
- The pre-registered instrument guards failed as written (S0 rate 98.8 vs guard ≤ 74; S1 73 vs guard
  100–400). Correctly diagnosed as the guards' own paper arithmetic — the instruments are
  independently validated — but "fail ⇒ VOID" was not invoked; guard thresholds should be set from
  measured controls, not paper estimates.
- The k-law constant: measured k99/(ρ·n) runs 2.5–6, not 1.5; the 10⁶ extrapolation is order-correct
  (k ≈ 150–250) and the conclusion stands, but the "1.5" is fitted to the large-ρ·n corner.
- The corrected closest-approach slope "≈1.165|Δt|" is still below the probe's measured median slope
  (2.2–3.0); the 73/orbit rate is direct and dense-verified, so only the dossier's arithmetic aside
  is off.
- `run.log` is empty (record-keeping gap; harmless since metrics regenerate bit-identically).
- All scenes coplanar and prograde; a retrograde counter-fleet on the same ring (crossings at every
  longitude) would be an even stronger kill scene for the corrected gate's adverse set.
