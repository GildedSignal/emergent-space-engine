# Predictions (written before the b1/b2 runs; controls f1/ring already run)

Question: does the phase-neighbour certificate's premise ("every real encounter lies within
partner rank k along the orbit", O(n·k) replacing the quadratic tier under concentration) survive
the game's extreme event — two fleets meeting?

Controls already run (f1-formation, ring-dense): rank-local, kmax 15/5, 100% caught at k=16/8,
window tier 0 misses, outside_cone 0. The gold's regime is reproduced. These are not predictions;
they are the known side.

## Predictions for b1 (two equal-period formations on crossing orbits, co-located)

1. Cross-fleet pairs produce a large share of encounters: truth_cross / truth_enc ≈ 0.5.
2. A certificate grouped per element clump (each fleet its own group) catches only within-fleet
   encounters: caught_fleet_k plateaus at ≈ 1 − cross_frac ≈ 0.5, for every k. The other half of
   the battle is missed silently.
3. The union sort (both fleets merged — legitimate here because the periods are near-equal, so the
   sort is quasi-eternal) catches the battle: caught_union ≥ 0.99 by k ≤ 16, at every fleet size.
4. Every cross pair is a Binet candidate: cone_cross ≈ n_A·n_B (quadratic in fleet size).
5. Setup evals per cross encounter grow ∝ n (candidates ∝ n², encounters ∝ n): roughly doubling
   from n=75 to 150 and 150 to 300 per fleet.

## Predictions for b2 (interception: fleet B from a = 1.07 crosses A's packet at perihelion)

6. Cross-fleet encounters exist (one meeting epoch at t = 2 orbits): truth_cross ≥ 20 at n=300.
7. Per-clump certificate: same plateau as b1, ≈ 1 − cross_frac.
8. The union sort does NOT save it: cross partners' union rank is set by the fleets' phase
   separation at setup (~1.2 rad), not by proximity: kmed_union_cross ~ n_total/5, kmax ~ n_total/3.
   caught_union stays far below 1 for every k ≤ 256; the catching k scales with n, so the
   "certificate" degenerates to the quadratic tier.
9. cone_cross ≈ n_A·n_B again (the transfer orbit's r-range overlaps A's ring at perihelion).
10. Setup evals per cross encounter grow ∝ n, as in b1.
11. Window tier on the crossing pairs: miss_window_cross ≤ 5% (the crossing is slow and transversal;
    uncertain, could be 0).

## Kill criteria for this probe

- If caught_union at small k (≤ 16) catches ≥ 99% of b2's cross encounters, the fragility claim is
  wrong: the union phase sort survives even the interception, and the certificate is more robust
  than the gold claimed. That would be a positive surprise worth reporting as such.
- If b2 produces ~0 cross encounters (mistimed geometry), the probe is VOID for b2; I fix the
  timing and rerun, disclosing the change.
- Controls on the instrument: outside_cone = 0 and miss_window_within ≈ 0 in every scene; if not,
  the truth or the matchup is broken and nothing above counts.
