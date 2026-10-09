# Predictions (written before the decisive run)

Question: as the universe's causal radius R(T) = c·T grows, does the set of sources that can
bill a given body (tide above the kick quantum ε_q) saturate, or grow without bound?

Scene (2D disk of sources with 3D-falloff tides, the game's plane): probe body at r_p = R_d
on a circular orbit; sources on circular orbits; tide billed is the l=2 (traceless in-plane)
part, since the doll's free fall absorbs l=0/l=1; normalization τ_loc = Ω_p².

Held-out predictions (not tuned; the constants especially):

- P1 (the fear, confirmed): the naive cone (every source within R read per kick) grows as
  ~R² for a uniform disk and saturates only at the disk's edge for an exponential one. The
  per-(body, source) cursor design of `b-news-gravity` cannot use the naive set.
- P2 (saturation): the per-source significant count N_sig(ε_q) saturates with R once
  R > R_sat ≈ (G m̄ / (ε_q·Ω_p²))^{1/3}; for a star-scale mass function and ε_q = 10⁻⁶,
  R_sat is a few R_d and N_sat is O(10²), not O(10⁶).
- P3 (aggregation): with dyadic annuli (nested dolls), the number of billing levels grows
  only as the log of the tide's dynamic range (~10–40), and each level's news rate (quantum
  crossings per unit time) falls with level, so the total news rate per body is bounded and
  independent of R_max beyond saturation.
- P4 (adversarial, uniform infinite disk): naive diverges as R²; significant still
  saturates, because the ring-summed tide ∫ 2πΣ G dr /r² converges (tail ∝ 1/R).
- P5 (adversarial, clumps): a companion-scale clump (0.1 M_d at ~30 R_d) bills as O(1)
  aggregates regardless of its internal source count.

Kill criterion: if N_sig or the news rate grows with R_max at fixed ε_q (no saturation in
the uniform case), the claim is dead and Julien's "we cannot handle the universe anymore"
is quantified as a wall at R ≈ that value.

What I expect to be weakest: the constants (N_sat, the rate). The convergence exponent
(1/R tail) I derived by hand and expect to see exactly; if the measured tail is flatter
than 1/R, my tide normalization or the l=2 projection has a bug.
