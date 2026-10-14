# Predictions (written before the decisive experiment)

Question: the checker's one-experiment-to-gold — re-derive the quantum gate's yield
with Kepler-true miss distributions (by exact Kepler propagation, not the author's
uniform model nor the checker's pooled-rescale approximation), and re-state the ledger
with the gate's own cost r priced against the cascade's per-pair work.

Method decided before running: per candidate pair, locate every close approach in the
10³-orbit horizon as a local minimum of |x₁(t)−x₂(t)| (exact Kepler: Newton on
d/dt d² from the mean-longitude conjunction times t_k = (2πk−ΔL₀)/Δn, ±half-orbit
windows, 3 starts), take the horizon's strongest impulse; deleted iff both members'
dE stay under one Q48 of E. Brute-force 4×10⁶-sample control on a subsample validates
the event method.

Registered predictions, on cases not tuned on:

1. **The checker's per-Δa medians reproduce** (their table was 8 seeds; mine will be
   exact-event): at Δa = 0.005 / 0.02 / 0.1 (e = 0.05, random ω, H = 10³ orbits)
   median min-miss ≈ 1×10⁻³ / 3–7×10⁻³ / 3×10⁻². My 8-seed brute-force spot check
   already gave 1.4×10⁻³ / 6.5×10⁻³ / 3.7×10⁻² — consistent with theirs within seed
   noise (their da=0.02 point is 24× below mine; 8-seed medians of a K≈4.6-event
   minimum are noisy — the exact distribution decides).
2. **The author's uniform miss model overestimates b by 10²–10⁴× at Δa ≤ 0.05**
   (checker's direction confirmed; exact magnitudes differ per Δa).
3. **Decisive exact yield lands between the two published numbers**: deletable
   0.97–0.999 on the author's three Dohnanyi spectra (checker's rescaled-uniform
   approximation said 0.955–0.978; the author's uniform model 0.9996–0.9999). The
   lower tail of the exact miss distribution (three-distance-type quasi-periodic
   revisits) is what decides survival, and it is thinner than the checker's rescaled
   uniform near b → 0 in my reading — but this is the uncertain one; if the exact
   tail is FATTER than rescaled-uniform, deletable could fall to the checker's range.
4. **The all-10-km negative control flips to ≈ 0.000 deleted** under exact misses
   (b_crit ≈ 5.6 a-units at D = 10 km dwarfs every real miss) — checker's flip
   confirmed.
5. **Real-belt mass (×52, total 1.2×10⁻⁹ M☉): deletable drops to 0.4–0.8** (heavier
   partners cross the quantum at larger b).
6. **The gate's own cost r**: exact-event check (K≈8 windows × Newton, tolerance
   1e-6) ~ 0.5–3 µs/pair scalar C — comparable to the cascade's 5.35 µs/pair, i.e.
   per-refresh wiring would eat the gate (f_r ~ 0.1–0.4); the honest wiring is
   event-scheduled (check at the pair's next scheduled conjunction), where amortized
   f_r ~ r_event×(P_refresh/P_syn)/5.35 µs ~ 10⁻³ — negligible. I predict the ledger
   is decided by the surviving fraction, not r, ONLY under event-scheduled wiring,
   and I will state both.
7. **Ledger (with exact yield + event-scheduled r): the top anchor (8.2×10³ cores
   ungated) lands above the 4-core budget** — my central estimate 10–100 cores gated,
   i.e. the gate's honest ceiling is ~20–800× and the flux split (62f7) stays
   required. If prediction 3 lands low (checker's range) this is 37–369 cores; if
   high, 2–30 cores — either way NOT comfortably under 4 at the top anchor.

What would make my method wrong: the event search missing local minima (validated
against brute force — if the validation shows misses > 1% of pairs with d error
> 10%, the method is broken and I fall back to brute force on smaller samples); the
impulse formula at threshold (author's RK4 control covers the weak regime; threshold
impulses are ~2⁻⁴⁹ of v — deeply weak); the mean-longitude window missing events
(±half-orbit windows with 3 starts; brute-force control counts every event).
