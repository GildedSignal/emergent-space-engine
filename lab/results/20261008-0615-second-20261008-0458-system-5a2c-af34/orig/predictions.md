# Predictions (written before the decisive experiment)

Scene: belt of N = 16,384 test bodies (a ∈ [2.1, 3.3] AU, e Rayleigh σ = 0.07) around a 1 M☉ star,
perturbed by a Jupiter (μ = 9.55×10⁻⁴, a = 5.204 AU, e = 0.049), heliocentric leapfrog,
T = 2,400 yr ≈ 510 belt orbits at 2.7 AU, dt = P_J/150. One body in two is a twin of its
neighbour, born with r_p offset by 0.4 of the law's 12-bit relative quantum (they share or
border a memo-key cell). Keys follow `crates/space`: scale = round(log2(r_p)·2¹²),
shape = round(log2(1−e)·2¹²) (MEMO_SHAPE_BITS = MEMO_SCALE_BITS = 12).

Held-out cases (not tuned on):

1. **Naive static-program billing saturates fast.** With the program frozen at birth, ≥ 80%
   of bodies leave their birth key within ≤ 60 belt orbits, because Jupiter's forced
   eccentricity (|Δe| ~ 0.03–0.08) moves r_p by hundreds of 12-bit quanta per secular cycle.
2. **The smooth flux is not information.** Twin pairs (born in the same key cell) mostly stay
   together: the median twin separation grows by < 2 quanta over the whole run; the fraction
   of same-cell pairs separated by ≥ 2 quanta at t_end is < 20%, concentrated in the mean-motion
   resonance bands (2:1 at 3.28 AU, 3:1 at 2.50 AU, 5:2 at 2.82 AU).
3. **Flux is cadence-invariant.** Total key crossings per body per orbit at dt and dt/2 agree
   within 10% (the flux is an integral; averaging/resampling does not change it).
4. **Key occupancy scales with N.** Distinct occupied keys grow sub-linearly (t ~ N^0.3–0.7
   over N = 1k→16k in-scene); the belt's occupied key space at these quanta is of order 10⁶–10⁷
   cells, so at the goal's 10⁹ bodies each key is shared by ~10² bodies and a per-key kick/flow
   store is O(occupied keys), not O(N).

Kill criteria for my claim (either result is a finding):
- If twin separation is fast and broad (median ≥ 2 quanta, ≥ 50% of pairs split), the smooth
  flow is NOT re-absorbable at the 12-bit width: per-key billing dies, and the naive store is
  honest — H_live really is ~ one scar per body per secular time.
- If ≥ 50% of bodies are still on their birth key at t_end, the static program is fine as-is
  and H_live is a non-problem for belts (the 8 GB worry moves elsewhere).

Numbers are cloud/Linux float64 — orders of magnitude only; crossings and occupancy counts
are integers.
