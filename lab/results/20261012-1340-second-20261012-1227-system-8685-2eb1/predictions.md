# Predictions — run 20261012-1340-second (second author on 20261012-1227-system-8685)

Written before the decisive runs. Instrument checks already done (1–2 seeds, smoke
only): the p-variant machinery steps exactly to mean-longitude grid multiples,
caps at window boundaries, regenerates all original cells bit-identically, and a
trace confirmed the schedule (windows every ≈1.09 body orbits in the belt scene,
0.17 orbits each). No 16/64-seed cell below has been run.

Task (the checker's named experiment): rebuild the between-window averaged term
**orbit-anchored** — `w<W>p<K>`: outside conjunction windows the body drifts
exactly to the next mean-longitude grid multiple of 2π/K and takes one kick kw=h
evaluated at the step midpoint; inside windows fine P/64 kicks; nothing dropped
at transitions. Sweep K and W. Gold condition: subharmonic gone at every segment
length AND belt ϖ̇ break closed (147% → u64-level). If it cannot close, the
averaged term must be continuous — a hard constraint on motion-law v2.

Truth: belt u2048 at 64 seeds (first 16 must be bit-identical to the original
`belt-truth.csv`), convergence at u4096 (8 seeds). Deviations in truth-ensemble
MADs; ϖ̇ also in % of the truth median (the original's sweep metric). Jacobi
floor = u64's median max-drift (1.3e-3 in the original 16-seed record).

Mechanistic bets (from the seg8 rule as shipped): the seg failure has two
independent parts — (i) the force is sampled at the *last* micro-step of each
segment with the full segment weight (endpoint rectangle, breaks Jacobi), and
(ii) the segment grid is re-origined at every window exit and the pending gap is
*discarded* at every window entry (breaks the secular rate). The p-variant fixes
both plus anchors the grid to the orbit.

## Registered predictions

- **PB1 (anchor closes ϖ̇):** belt `w0.5p8` 64-seed Δϖ̇ ≤ 0.3 MADs and rel-err
  ≤ 2% (vs w0.5-only +66%, seg8 −56%, sweep max 147%). Across the W-sweep
  (W ∈ {0.125, 0.25, 0.5, 1.0, 2.5}), `w W p8` stays ≤ 5% at every W where the
  window-only variant was 43–147% off.
- **PB2 (subharmonic gone at every length):** belt `w0.5pK` for K ∈ {4, 8, 16}:
  Δė ≤ 2 MADs (vs seg4/8/16 = 4.7/165/105) and Jacobi ≤ 5× the u64 floor at
  every K. **K = 2 is predicted to FAIL** (two samples per orbit cannot average
  the quadrupole's m=2 harmonic — both samples see the same sign); K = 32 also
  ≤ 2 MADs. If any K ∈ {4,8,16} shows Δė > 10 MADs or Jacobi > 20× floor, the
  discrete orbit-anchored average is falsified → "must be continuous" outcome.
- **PB3 (mechanism ablations):** `seg8m` (midpoint sampling only) brings Jacobi
  to ≤ 5× floor but does NOT close ϖ̇ (rel-err > 20%); `seg8n` (no-drop only)
  leaves Jacobi > 20× floor. I.e. sampling owned the Jacobi blowup, anchoring
  owns the rate. If `seg8mn` (both fixes, still re-origined grid) closes ϖ̇ too,
  the anchor itself was irrelevant and only sampling+drop mattered.
- **PB4 (no cost win claimed):** on the belt, uniform u8 already holds behaviour
  at 8 kicks/orbit; p8 (~20/orbit incl. window cadence, but ~40 drift solves vs
  u8's 8, vs u64's 64/64) is a *structure* result (windows + orbit-anchored
  secular in one schedule), not a new cost lever. I predict no p-variant beats
  u8's behaviour-to-count ratio on belt.
- **PB5 (encounter inversion stands at 64 seeds):** against u4096 truth, the
  original 16-seed "w0.5 beats u8 3.6×" on Δė inverts to noise (both within
  ~±1 MAD of each other; u16 clearly better than both) — reproducing the
  checker's adversarial result in this shipped record.

Kill criterion for the rebuild claim: if `w0.5p8` fails PB1 (ϖ̇ not closed) the
orbit-anchored discrete average is killed *as a secular carrier* and the dossier
reports "the averaged term must be continuous" as the outcome the checker asked
for (still a decisive result, either branch clears the bar).

Noise floor: medians at 64 seeds carry ≲0.3 MAD SE; I will not quote as a
finding any margin below 1 MAD (the original's failure mode).
