# Predictions — second-author run (written before the decisive experiments)

Question restated: the second checker kept run 20261007-1550-dynamics-71a5 at silver on three
measured gaps: (i) the pre-registered first-miss scaling H ∝ Δϖ̇⁻¹ was never fitted (misses at
exactly one of five rates, T-truncated); (ii) the co-precessing fix was probed only on G6,
where the pair un-crosses at Om = 10⁻³ (late windows vacuous) and nothing ran deeply crossing;
(iii) the shadowing sentence ("orbit-averaged kicks act once per orbit, the same order as the
40–400-orbit horizon" — off by 1.5–2.6 decades) is argued, not measured. This run: fit the
scaling with ≥3 miss-showing rates, ring the fix on the deep-crossing pair G2 (cone gap
−0.138, e = 0.4), and measure the re-cut cadence K that shadows aging. Same instrument as the
author (brute-force truth = `pair_minima`, certificate = frozen proposals, MISS = true minimum
< ρ with no valid proposal within 0.4 Psyn), extended to piecewise-frozen windows (staleness
θ): a window cut at t_k uses the pair frozen at its t_k elements (an exact time translation of
the frozen list, so one brute-force truth serves all policies).

Law to test: **staleness law** — a miss needs differential-rotation staleness s = |Δϖ̇|·(t −
t_cut) to exceed a geometry constant D_miss of the pair (independent of rate, while
|Δϖ̇|·Psyn ≪ arc scale). Then: frozen first-miss H ≈ D_miss/|Δϖ̇| + W(φ) (W = conjunction
realization waiting, rate-independent), piecewise-with-threshold-θ misses iff θ ≳ D_miss, and
the kick-cadence crossover K* ≈ D_miss/|Δϖ̇|. The checker's probe (0 misses at θ = 0.2, worst
A2 case) then implies D_miss(G6) > 0.2 rad and the om = 10⁻³ first miss at 1458.6 was
waiting-dominated (safety died at ≈ 0.2/10⁻³ = 200, realized 7× later).

Held-out predictions (none of these configurations was run by the author or either checker):

1. **G6 first-miss scaling (rates 1,2,3,5,10 × 10⁻³, 12 phases, T = 1500).** Misses in ≥ 3
   rates, most phases at the top rate. Fit of earliest (and median) first-miss vs rate:
   exponent in [−1.3, −0.4]; H·|Δϖ̇| grows with rate toward a ceiling D_miss (waiting
   contaminates the low rates), and D_miss read this way ∈ [0.2, 2] rad. Falsifier: exponent
   ≥ 0 (safety does not scale with rate — kills the staleness law) or misses at < 3 rates
   (instrument still too slow — report honestly).
2. **G4n safety-vs-realization split (rates 1,2,3,5 × 10⁻³, 6 phases, T = 3000, direction
   Om_j = −om as stored).** Every realized sub-ρ event after t_tang = 1.4268/om (0 before;
   adds to the author's 7 and checker's toward-direction events). Linear fit of t_first vs
   1/om over realized phases: slope = 1.4268 ± 0.03 (the exact far-side travel), intercept =
   median waiting W > 0, and W's spread across phases spans ≥ 100 time units (synodic luck).
   Falsifier: slope ≠ travel (tangency arithmetic wrong) or any pre-tangency event (the
   "never" certificate was never valid — a stronger kill).
3. **Co-precessing fix on deep-crossing G2 (om = 3×10⁻³ ≈ a belt pair at Δp/p ≈ 5%, 12
   phases, T = 1500).** Frozen: ≥ 3 misses over the ensemble (G2 crossed its miss threshold
   at every rate ≥ 3×10⁻⁵ in run 1's single pair). Piecewise θ = 0.2 rad: 0 misses (predicts
   D_miss(G2) > 0.2). Per-passage refresh (θ = |Δϖ̇|·Psyn, the exact co-precessing O(1)-update
   limit): 0 misses, waste ≤ structural baseline + 2, and the baseline is measured the same
   way (frozen pair vs itself, om = 0). Falsifier: any miss under per-passage refresh (the
   fix fails where non-vacuous — refutes the adoption step) or frozen shows 0 misses (the
   deep-crossing test is vacuous at this rate; report the measured D_miss instead).
4. **Shadowing crossover (G6, om = 3×10⁻³, re-cut every K ∈ {2π, 20, 62.8, 157, 314, 628,
   ∞} time units, 12 phases).** Misses fall to 0 for K ≤ K* and sit at the frozen level for
   K ≥ 2K*, with K* ≈ D_miss(G6)/om within a factor of 2 (the staleness law). The re-setup
   cost at the crossover is 1/K* per unit time per pair = |Δϖ̇|/D_miss per orbit — NOT once
   per orbit. Engine translation: the ACTIVE-certificate horizon is H_act = D_miss/Δϖ̇ ≈
   5–50 orbits at the 10%-belt rate (0.038 rad/orbit) for D_miss ≈ 0.2–2 rad — at or below
   the 40–400-orbit tangency band, i.e. the dossier's horizon was, if anything, generous for
   active pairs; kicks shadow aging only if they land on the pair at least every H_act
   orbits, which for a quiet pair is a population assumption, not a law. Falsifier: K* ≥
   3·D_miss/om (re-cuts shadow far beyond staleness — rescues the frozen certificate and
   kills the co-precessing adoption).
5. **Controls.** Piecewise machinery at om = 0 with any θ: bit-identical to the frozen
   run_case numbers (else my window code is broken). Equal absolute Om = 0.05 on both G2
   bodies: 0 misses, 0 waste, m0_true = m0_frozen to 6 digits (rigid rotation, re-checked on
   the deep-crossing geometry).

Kill criteria: if prediction 1's exponent is ≥ 0 or 4's crossover is absent, the staleness
law is wrong and this dossier reports the measured law (H vs rate, misses vs K) without the
D_miss story. If 3's frozen arm shows 0 misses, G2 at 3×10⁻³ does not age within T = 1500 and
the fix test is reported as vacuous with the measured threshold rate.
