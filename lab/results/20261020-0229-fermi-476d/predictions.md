# Predictions (written before the 2e5 and 3e5 arms; the 1e5 s=17 arm was the calibration shakeout)

Question: 2d26 composed the wave-excess law "×2.37 per ×2 K" (α = 1.245) from two rungs
(1e5: 6,619 ms, 2e5: 15,686 ms) and extrapolated it to 1e9 (coverage 6e-5). cc9d's saturated
constants (kicks/gulp 0.16–0.17/body flat 1e4–2e5; 49.8–52.7 µs/kick flat) say excess must
relax to α = 1.0 (×2 per doubling). At 1e9 the two differ by (2.37/2)^12.29 ≈ 8×.

Instrument: my own print-only patch on `nladder` (independent of 2d26's), sustained onset
anchored offline from the per-frame CSV (their onset 458 = my sustained 456 at 1e5; the
stray first-over frames 74/119/132 are burn-start transients, excluded).

Arms (shipped burn scene, seed 1, rtf 2000, 12 ms, s=10 → 600 frames, matched windows):
100000, 200000, 300000. The 3e5 arm is held out (cc9d's checker has only its max_ms
2,840.8, no excess). 4e5 is unflightable under the 2 GB cap on shipped main (scan channel
∝ K walls before the game-time-locked onset at gs ≈ 15k) — the fence/split is the
prerequisite, stated as a domain bound.

- **P1 (reproduction):** my excess at 1e5 full window lands within ±10% of 2d26's 6,619 ms
  [measured: 6,654, +0.5% ✓ before registration; the registered half is the 2e5 arm:
  my matched-window ratio 2e5/1e5 ∈ (2.1, 2.6), i.e. the anchor reproduces].
- **P2 (decisive, the exponent):** the local exponent at [2e5, 3e5] (K-ratio 1.5):
  saturated law predicts ratio ≈ 1.50; 2d26's law predicts 2.37^log2(1.5) ≈ 1.66.
  I predict **ratio ∈ (1.42, 1.58)** — the exponent is falling toward 1.0, and the 1e9
  composition overstated by ~5–8×. **Kill criterion for my claim:** ratio ≥ 1.62 (α ≥ 1.18
  at the top rung, within noise of the 1.245 law) — then 2d26's extrapolation stands and
  my correction dies.
- **P3 (mechanism):** kicks/body inside the matched window at 3e5 ≤ 0.18 (saturating at
  cc9d's 0.16–0.17 band) and effective µs/kick in-window ≤ 65 µs; if BOTH are flat while
  the ratio still exceeds 1.58, the super-linearity is neither term I can see (name it as
  the open question, do not force an explanation).
- **P4 (composition):** with the measured top-rung exponent (P2), coverage at 1e9
  recomposed: at α = 1.0 from the 2e5 anchor, coverage(1e9) = 2.55 × (1e9/2e5)^-(1.0) ×
  K-flat ebb ≈ 2.55/5000 ≈ 5.1e-4 — a factor ~8 above 2d26's 6e-5; the "prepay dies by
  1e6, amortize ≤ ~3e5" boundaries move by less than one rung (they are set near 1 where
  the two laws differ least).
- **P5 (memory wall):** the 3e5 arm either completes 600 frames under 2 GB or is killed
  past the crest (gs > 16k); either way the CSV up to the kill decides P2 (the crest
  window carries most of the excess; validated by the w40 ratio at 1e5/2e5 vs the full
  ratio).
