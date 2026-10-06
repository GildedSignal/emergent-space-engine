# Predictions (written before the decisive runs)

Held-out: the rung's belts (Python `random.Random(20261008)`, one stream) — I have not looked at
their encounter content. What I have seen: the crate's own verify on its belts (miss=0/false=0,
checks/hits ≈ 1.19), and its steady experiment at (b)'s parameters (rate 5.86–5.89e-3 per body
per orbit, stationary across horizons 100…1e5).

1. **(a) completeness & soundness, diophantine:** missed_fraction = 0.0 and false_fraction = 0.0
   pooled over all 20 belts, adversarial ones included. Risk: knife-edge encounters with d within
   ~1e-12 of ρ could split between my independent truth and the method; I expect at most one or
   two across ~1e4 encounters, and I will report any as boundary cases with their distances.
2. **conjunction-sampled** misses the conjunction-less encounters (r8 v2's leak): pooled
   missed_fraction over the 16 regular belts alone would be ~0.5–6%; with the four adversarial
   belts pooled in I predict 10–80% (the equalkeys belt has pairs with Δn = 0 exactly — no synodic
   conjunction ever — so every encounter of those pairs is missed). false_fraction = 0.
3. **element-sort**: the same leak (missed_fraction in the same range as 2), and it fails steady
   hugely: its events are swaps at mean-longitude conjunctions, ~0.5–1.6 per body per orbit on
   belt (b), against a truth rate of ~6e-3 → steady_ratio ~1e2–1e3.
4. **(b) steady, diophantine:** events = one-time setups + exact checks, over 1e5 orbits, divided
   by the truth's encounters per body per orbit: 1.2–1.5 (the crate's own seed gave 1.32; the
   setups amortize as 1/h and the checks carry a ~10% window-safety margin). Truth rate measured
   by my independent truth on a sub-horizon (stationary process; the method's own rate is flat
   across a 1000× horizon range).
5. **checks_per_encounter, diophantine, pooled over (a):** 1.05–1.35 (≤ 1.5).
6. **(c) scale_exponent:** diophantine ≈ 1.0 (checks track real encounters at fixed per-body
   rate; ρ ∝ 1/N holds the rate); element-sort and conjunction-sampled ≈ 2.0 (their checks are
   conjunctions, ∝ pairs ∝ N²).
7. **(d) kicks, diophantine:** kick_setup_ratio (median) = 1.0 ± 0.03 — the re-scan covers the
   kicked body's U-range, which holds its candidate partners and few others;
   other_certificates_touched = 0 (no pair of two untouched bodies is recomputed).
8. **oracle** passes every criterion (it reads the truth's list; its check work is the true
   encounter count, which grows ∝ N on (c) by design).

What would surprise me (and matter): any missed encounter in the narrow or co-orbital belt
(regime of the Wide/Full sections), a false report in the hot belt (σ_e = 0.1), or a
steady_ratio above 2 — that would mean the terminating first-hit queries or setups do not
amortize as the horizon grows.
