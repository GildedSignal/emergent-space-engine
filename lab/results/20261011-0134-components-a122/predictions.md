# Predictions (written before the corrected decisive run)

Pilot (tuning, with a sign error in the Laplace denominator that made precession ~10^4× too
large) established: the store saturates at ~127 bits/body once every body carries a full-entropy
ω delta; `compact` with no events grows nothing; base belt = 120.03 bits/body (block form; the
bijection would replace this, not add to it). Encounter rates measured on the frozen scenes:
0.002 (rho 1e-4) to 0.02 (rho 1e-3) real encounters per body per orbit at n = 1000.

The corrected physics (Giant at 5.2 AU, μ = 2^-10; belt 2–3.5 AU, σ_e = 0.05):
advance ≈ 9.4e-4 rad/orbit at 2.75 AU, dominated by Laplace–Lagrange; GR ≈ 7e-8.
Orbits per wall-hour at rtf 100 (mid-belt period 4.56 yr): 2.5e-3.

Predictions for cases not tuned on (the corrected run is the first with right magnitudes):

- **P1 (control):** no events → zero growth. (Already confirmed in the pilot.)
- **P2 (common per band, variant 1):** every body's ω advances by its band's common rate
  (~1600 quanta after 1 wall-hour, 1.6e6 after 1000 h). The scar deltas within a band are
  constant across bodies. Prediction: the block codec captures this — growth stays under
  ~5 bits/body at all horizons up to 10^5 h (it should scale like the per-block bookkeeping,
  not like log2 of the drift range). If it instead grows toward log2(drift) ≈ 21+ bits at
  10^5 h, the scar layer does not see the band structure and the band schedule must be derived
  by the reader.
- **P3 (realistic differential, variant 0):** the e² differential within a band is
  ~2σ_e² ≈ 0.5% of the common drift: ~8 quanta after 1 wall-hour, ~8000 after 1000 h
  (~13 bits if stored raw). Prediction: growth ≈ log2(differential range) + O(1) —
  between 3 and 6 bits/body at 1 h and 13–20 bits/body at 10^5 h, far below the 127-bit
  saturation. If it jumps to ~127 bits/body at any play-reachable horizon (≤ 10^3 h),
  the design dies at 10^9 and the dossier says so.
- **P4 (encounter scars):** bits per scar (fraction 1e-2 and 1e-3) land near
  30–80 bits: a scar row (Elias–Fano ordinal + 5 delta columns) at low density.
  At 1e-2 the per-scar cost should be close to the 1e-3 one (the layer is sparse in both).
- **P5 (extrapolation):** at 10^9 bodies and a 1000-hour campaign (2.5 orbits), secular
  scars cost ≤ 2 GB and encounters ≤ 0.3 GB at the crate's rates — the store fits 8 GB;
  the binding term is the secular differential, and only if P3 fails does the store die.
- **P6 (rate table):** the derive-side table (rates to one-quantum precision over the
  horizon) stays under ~100 MB at all horizons ≤ 10^3 h but grows past ~1 GB by
  ~10^4–10^5 h — derivation wins at long horizons, storing wins at short ones.

Kill criterion: if P3's curve reaches ≥ 60 bits/body at ≤ 1000 wall-hours, the
programs-plus-scars store cannot hold 10^9 bodies in 8 GB on a real campaign, and the
representation must derive the secular drift instead of storing it.
