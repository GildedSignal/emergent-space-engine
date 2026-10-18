# Predictions — 20261018-0308-second-…-e38a (frozen before the decisive runs)

The checker's named experiment (silver → gold): the encounter-parity certificate's **negative
control**. A plane variant that provably skips at conjunction must FAIL the parity statistic while
the shipped arm (step 7) still passes it. Instrument note, measured before freezing: the knob is
`Config::step_log2` = ~2^step_log2 kicks per radial period, so **coarser is LOWER** (the checker's
"step 9–10" is finer, not coarser): median kicks/P over the 144-IC ensemble at μ = 1e-3, 4 P is
1095 (step 9) / 274 (step 7) / 68 (step 5) / 17 (step 3) — a live knob, no MIN_STEP saturation, 0
refusals, 0 deaths in all four arms at 4 P (both sides have zero first events ≤ 4 P at μ = 1e-3,
so the 4 P knob arms are instrument-only).

Ensemble and truth side unchanged from 80fe (144 ICs, `until_crossing` entries, rtol 1e-12). The
negative arms: plane at step 5 (4× coarser) and step 3 (16× coarser), μ = 1e-3 horizon 512 P, and
the μ = 1e-2 burst at 4 P. Certificate bands (frozen by 80fe): count parity ratio ∈ [0.8, 1.4],
survival curve inside the 95% bootstrap band (+0.02 slack), burst = same IC set with
max |Δepoch| ≤ P/64 = 0.016 P.

- **N1 (the count leaves the band, direction: down).** At μ = 1e-3, 512 P the coarser arms'
  first-event (kill) counts fall below the truth's 40 first-entries by more than the parity band:
  step 5 kills **< 32** (ratio < 0.8) and step 3 kills **< 24** (ratio < 0.6). Mechanism: the kill
  is a surface check at a kick tick inside the planet's doll, and the doll's own kick cadence
  scales with step_log2 — 4× (16×) fewer surface samples per conjunction dive, and the inter-kick
  trajectory error decorrelates the dive from the truth's. Honest alternative, which would break
  parity the other way: bigger inter-kick errors could drive spurious dives (kills RISE above 56,
  ratio > 1.4). Either exit counts as the certificate catching the skipping law; my call is the
  fall.
- **N2 (the curve leaves the band).** The step-5 and step-3 survival curves exit the truth's 95%
  bootstrap band at some epoch (step 7 stays inside everywhere, 80fe's result), with the coarser
  arm strictly further outside (max |ΔS| larger than step 7's 0.062, monotone in coarseness).
- **N3 (the burst match breaks at μ = 1e-2).** Against the truth's 8 entries ≤ 4 P: step 7 keeps
  8/8 ICs with max |Δepoch| ≤ 0.016 P (80fe's positive control, must reproduce); step 5 keeps
  **≤ 7 of the 8 ICs** with max |Δepoch| **> 0.03 P** (the death epoch lands on the doll's coarser
  kick grid, drift mostly late); step 3 keeps **≤ 6 ICs**, max |Δepoch| **> 0.06 P**, at least one
  IC's kill moving past 4 P entirely (the skip: a real ≤ 4 P encounter the variant never sees).
- **N4 (the certificate stays specific: the fine side).** Step 9 at μ = 1e-2, 4 P (2× finer than
  shipped, ~4× the kicks) still matches the burst 8/8 with max |Δepoch| ≤ 0.016 P — the
  certificate must not fail every cadence change, only ones that skip; if step 9 also breaks the
  match, the burst clause is cadence-sized, not skip-sized, and the certificate must say so.
- **N5 (the μ = 1e-2 cost wall is a fine-cadence wall).** The 80fe runaway tail was measured at
  step 7; at step 5 the same 16 P / 144-IC arm that died at 120 s on 2 workers **completes within
  the same 120 s budget** (4× fewer kicks) — the wall is cadence-bound, not μ-bound. (A cost
  observation for the board's smoothness line, not a parity claim: step 5 is a different law.)

Kill criteria: any negative arm with > 10% refused-at-build ICs (instrument/domain wall, report,
not a parity number); the step-7 arms failing to reproduce 80fe's 47 kills / 8-for-8 burst (VOID —
the control must pass before the negative counts); fewer than 144 completed ICs in any 512 P arm
(report n, parity on the common subset, as 80fe did).
