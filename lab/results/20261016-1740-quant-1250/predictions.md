# Predictions (written before the decisive runs)

The angular certificate (knot-panel phase arc + swept-angle and chord bounds, `ES_SCAN_CERT`
toggle, patch in `work/patch.diff`) is applied to the scan's answer half only. Cases below are
not tuned on; the tuned-on case is N=1000 coast, seed 1 (the ladder's flight).

1. **Outcomes are bit-identical.** Every flight run in both arms (`ES_SCAN_CERT=0` vs on) prints
   the same `digest …` line. A single differing digest falsifies the certificate's conservatism
   and kills the configuration.
2. **The answer bill falls ~10×, not ~100×.** cdf0 priced the angular cut at ~10–20 ns a
   candidate (reads/hit → ~1). I predict the panel arc (~2π/86 wide, plus the travel term
   v·h/r) kills ~85–95% of Cycle candidates, not ~99%: reads/hit falls from 46–481 to ~5–40,
   and the certificate itself costs ~0.3–0.8 µs a candidate (Scalar ops + a 43-entry scan),
   so the answer half's per-answer cost falls ~10–20×.
3. **The latch reopens at the plane's N.** At N=1000 (fallback regime, candidates ≈ all
   bodies) the mean per-answer cost falls from ~1–4 ms to ≤ ~0.5 ms, comfortably under b/2
   (2.5 ms at the 5 ms budget; the 12 ms frame budget's margin floor is 0.75 ms), and
   `held_max` stays small under burn.
4. **Held-out N=300 and N=10000:** the kill fraction stays ≥ ~80% (the arc's width is set by
   the compiled knot count and the scan horizon, not N), reads/hit ~5–40 both, digests
   identical. At N=100000 (root doll, filter at its floor per cdf0) the certificate still
   kills ≥ 80% of Cycle candidates — the belt's registered hulls are wide but its phases are
   uniform.
5. **What would make it wrong:** an arc term missing a widening (a digest difference — check
   the advance/excess convention and the inbound mirror first), or the certificate's own cost
   eating the gain (its Scalar getters per candidate — `range_of`, `period`, `advance` — must
   stay ≪ a readout).
