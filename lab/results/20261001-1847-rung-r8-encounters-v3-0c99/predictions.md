# predictions.md — r8 v3 (written before the decisive case runs)

Tuned on: smoke (400 pairs of belt a00, 6 orbits: truth = method = 1 encounter, times
equal to 1e-17) and the bring-up cross-checks on a13/adv-equalperiod/adv-coorbital/
adv-narrow subsamples (2500–3000 pairs each), where three truth bugs were found and
fixed (the crate was right each time).

Held-out expectations for the runs I had not looked at when writing this:

1. **Controls.** oracle: missed = false = 0, steady_ratio exactly 1, checks/encounter
   exactly 1, scale exponent ≈ 1 (it reads the truth). If the oracle misbehaves, VOID.
2. **diophantine complete/sound.** missed = false = 0 pooled over (a), including the
   four adversarial belts. Known residual risk: shallow double minima inside one
   component (near-tangency), where the crate's grid (24/64/256 samples per window)
   and my component walk (0.1ρ displacement, 2e-3 s cap) could each resolve a wiggle
   the other misses. I predict zero such flips on these belts; one flip would show as
   exactly one extra false + one missed.
3. **element-sort and conjunction-sampled fail as designed.** Both fail `steady`
   (events/body/orbit ≈ conjunction rate ≈ 1–2 at N=10³, vs truth ~1e-2) and `scales`
   (exponent ≈ 2). conjunction-sampled additionally fails `complete` on adv-narrow:
   with |Δn|·T < 2π for ~every pair, most encounters happen with no conjunction in
   the window — I predict missed_fraction ∈ [0.3, 0.9] pooled, dominated by that belt
   (r8 v2 measured 78% conjunction-less on its adversarial belt against a
   conjunction-based reference; my truth has no such blind spot).
4. **Steady (b).** Truth rate (128 sampled pairs, 1e5 orbits) within ~10% of the
   crate's own hit rate (~5.9e-3/body/orbit at these parameters). steady_ratio for
   diophantine ∈ [1.1, 1.5]: setups amortise over the horizon, checks/hits ≈ 1.10.
   Both negatives: ratio ~10²–10³.
5. **Scaling (c).** diophantine exponent ∈ [0.9, 1.15] (checks/body/orbit flat at
   ≈ 0.04 under ρ ∝ 1/N); oracle ≈ 1 ± sampling; negatives ≈ 2.
6. **Kicks (d).** kick_setup_ratio ∈ [0.97, 1.05] for the cone re-scan (a 1e-3 kick
   moves U by ~1.5e-3·U while the cone's reach is ~e/p ≈ 1e-2: only edge pairs flip);
   other certificates touched = 0 for every configuration (each recomputes only the
   kicked body's pairs by construction).
7. **What I do not expect to hold.** The truth's dip-suspicion recursion certifies
   "no sub-ρ dip" only down to 1e-13·ρ of displacement resolution; and component
   interiors are resolved at 2e-3 s structure. If the crate's Full-section grid
   (T/256 ≈ 0.027) lands inside a wiggle my walk misses, prediction 2 breaks by one
   event. I accept that as the honest boundary of a sampled truth.
