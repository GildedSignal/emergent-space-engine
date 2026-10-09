# predictions.md — run 20261009-1504 (second author on 20261009-1345-system-136a)

Written before the decisive experiment (exp2, the checker's named gold experiment: the Δϖ rotation
and (a,e) drift the crate's cached `sections()` tolerate, against exact re-setup, plus wall-clock
re-setup cost). Tuned on: nothing — exp2 has not run yet. Mechanism reasoning is recorded with each
prediction so a miss is diagnosable.

The claim under test (original dossier): per-pair section caches keyed by (bucket, bucket, Δϖ-band)
amortize per-element-change setup ×43 (fine band 2.4e-4) to ×2705 (wide band 1.5e-2) at the
unaveraged cadence (32 kicks/orbit), with differential apsidal drift 1.77e-4 rad/orbit (regenerated
`exp.py` [B]). The checker's risk 2: if sections tolerate only ~1e-4, ×43 shrinks toward ×13.

- **P1 (fine band):** at dpom = 2.4e-4 rad, cached sections miss **0** events over the 2048-pair
  belt sample (20-orbit horizon). Mechanism: the arc around θ_c is ~sqrt(ε_u/R) ~ 0.1 rad wide, two
  orders above any rotation-induced shift of the crossing longitude; the s-window (~ρ/c, c the
  crossing closing speed) exceeds the s-shift (~δ·O(1)); the per-passage check is exact, so a stale
  window can only miss, never invent.
- **P2 (fragility ordering):** the first misses as δ grows are **Cross** sections (narrowest
  windows); Wide/Full stay at zero misses up to ≥ 5e-2 rad.
- **P3 (wide band):** at dpom = 1.5e-2 there ARE misses (some fragile near-tangential Cross pair
  with amplified dθ ~ δ·(e_i/p_i)/|Δ(V,W)|). So δ*_zero ∈ [2.4e-4, 1.5e-2), and the ×2705 wide-band
  number does not survive as zero-miss; adoptable band = δ*_zero, savings ∝ δ*_zero.
- **P4 (radial half of the key):** zero misses up to de_rel = 2.44e-4 (half a k-bucket, k =
  1/(1+e), bucket ln-width ln(1+2⁻¹¹) ≈ 4.883e-4); misses appear only at ~the full bucket width,
  where the real cache re-keys anyway. Combined corner (da_rel 1e-4, de_rel 2.44e-4): zero or few.
- **P5 (control, both sides):** exact re-setup matches brute-force `truth_pair` on drifted pairs
  (δ ∈ {0, 2.4e-4, 1.5e-2}, 32 pairs each): 0 missed. If this fails the reference is unsound and
  everything is VOID.
- **P6 (extras):** extra events (cache-found, exact-setup-unmatched) ≈ 0 everywhere: the check is
  an exact distance-minimum scan, and stale arcs point at genuine encounters only.
- **P7 (wall-clock):** `sections()` re-setup med ~2–20 µs/pair on this Linux/x86 box (r8 v3's
  2.5–24 µs), evals tens per setup. Cloud box ⇒ orders of magnitude only.

Pre-registered interpretation:
- P1 holds ⇒ the ×43 unaveraged amortization converts from drift-count model to measurement
  (band 2.4e-4, residence 2.4e-4/1.77e-4 ≈ 1.36 orbits, 32 kicks/orbit).
- P1 fails ⇒ caching half refuted at the fine band; report δ*_zero and savings 32·δ*_zero/1.77e-4.
- Either way the wide-band ×2705 is replaced by the measured δ*_zero and its savings.
