# Predictions — 20261011-1234-taleb-62f7 (written before the decisive sweeps)

Question: when two concentrated packets meet (the interception), the real contacts are
Θ(n_A·n_B). If so, no discovery certificate can save per-pair processing at fleet scale:
the *events themselves* are the workload. The escape must be a regime change — one
aggregate event per packet crossing. Predictions, frozen before running the x/w/angle
series (the belt control may run first):

1. **Contacts are quadratic in fleet size at fixed packet width.** Cross contacts vs n
   (n ∈ {50,100,200,400,800} per fleet, b2 geometry): log-log exponent 1.9–2.1. Per-ship
   contact load τ = contacts/n_A grows linearly in n (slope ≈ the per-pair probability
   3ebf measured, ~0.02–0.03).
2. **τ, not n, is the ruin number.** Extrapolated to 10⁶ ships/fleet at the measured
   per-pair rate: ≥ 10⁹ real contact events per crossing — pairwise exact processing is
   ruin in absolute terms even at 1 eval per contact (the certificates' "flat work per
   encounter" invariant is the wrong invariant; work per *ship per crossing* is the
   right one).
3. **The belt control sits orders below.** Uniform belt (n = 1000, a ∈ [1, 1.001],
   uniform phase): contacts per ship per orbit < 0.05 — the same dimensionless load
   separates the discrete regime from the fluid regime cleanly.
4. **Column-density law.** Halving packet width A (w = 0.5 → 0.125) at fixed n changes
   contacts by a factor 2–8 (uncertain: near-parallel relative flow makes the effective
   tube length, not w_A alone, set the count — measured, direction pre-committed as
   *increase* when the packet is denser).
5. **Aggregate (flux) total, no refit.** One formula per packet pair — λ_i =
   ρ_B,2D · 2R · L_i, ship i's straight chord through the opposing packet's measured
   rectangle at crossing time (all inputs measured from the actual body states at t*,
   O(n) total, zero free parameters) — predicts total cross contacts within ×[0.5, 2.0]
   of the truth in every scene, and the *held-out* crossing (a = 1.5, e = 0.4 transfer,
   genuinely non-parallel flow, different sin θ, different speed) within the same band
   with no refit. If it needs a per-scene fudge factor, the aggregate as specified is
   wrong and I report that.
6. **Per-ship distribution is not Poisson.** Var/mean of per-ship contact counts > 1.5
   (packet-edge taper: interior ships see the full chord, edge ships less) — so the
   aggregate must reproduce a *mixture* (per-ship λ_i), not one number; Pearson corr
   between predicted λ_i and measured c_i > 0.5.

Kill criteria: (K1) exponent < 1.8 → premise dead, certificates suffice asymptotically,
report that. (K2) flux ratio outside ×[0.5, 2.0] in any scene → aggregate broken as
specified; keep only the ruin law. (K3) belt load ≥ 0.05/ship/orbit → the number does
not separate regimes.
