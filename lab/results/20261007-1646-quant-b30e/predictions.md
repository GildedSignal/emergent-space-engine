# Predictions (written before the decisive runs)

Tuned on: `belt15` at n∈{16,32}, ≤2 orbits only (smoke). Everything below is held out.

Units: one "orbit" = the convoy's orbital period at r=1.5·sep (belt15/belt15w), 2:1 resonant
radius (belt21), or the planet's period (hill). "bits_col_med/p99/max" = zigzag bit widths of
member deviations from the family's affine program, columns [p(Q32), k(Q48), ω(Q32)].

1. **No reabsorption, no saturation of the scarred fraction** (belt15, n=16, 512 orbits):
   `clean` stays 0 from the first window on; nothing returns exactly to its program.
2. **Slow diffusion, not explosion** (same run): bits_col_med grows by about +2 to +6 bits
   from orbit 2 to orbit 512 (random-walk invariants: magnitude ~√t ⇒ bits ~ 0.5·log₂ t);
   scarlayer_bits_pm ends in the 130–170 range. A plateau (bounded oscillation) or an
   unbounded climb (>200 bits) would both be findings against my expectation.
3. **Linearity in μ** (belt15w = μ/256 vs belt15, n=64, 64 orbits): deviation widths ≈
   belt15's widths minus 8 ± 1 bits (kick impulse ∝ μ, deviation in bits = const + log₂μ).
4. **Resonance is worse** (belt21, n=64, 32 orbits): bits_col_p99 ≥ belt15's p99 at the same
   orbit count, and the growth with t is faster (locked conjunctions pump coherently).
5. **Hill belt departs** (hill, n=32, 16 orbits): `away` > 0 and monotonically non-decreasing
   (handoffs into the planet's doll are hysteresis: nobody comes back within 16 orbits).
6. **N-independence of per-member live bits** (belt15 n=32 vs n=512, 8 orbits):
   scarlayer_bits_pm differs by < 15% (EF ordinal overhead is ~log n and amortizes; kick
   environment per member is N-independent in the restricted problem).
7. **Event rate** stays ~466 kicks/ship/orbit at every N tested (it is per-ship, not pairwise).

Falsifier for the whole probe: if the orbit-0 window does not seal ≈0 scars (< 1 bit/member),
the accounting is broken and nothing above counts.
