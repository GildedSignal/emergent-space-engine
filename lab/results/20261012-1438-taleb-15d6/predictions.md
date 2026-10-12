# Predictions (written before any run; the binary is compiled but no scenario has executed)

Question (one sentence): the gold 20261006-0346-taleb-09b5 replaced the quadratic encounter tier, inside co-orbital clumps, with a k≈4 phase-neighbour "train" certificate triggered only by a Binet-clump number — does that certificate survive the fleet densities it is adopted for (its own headline is a 10⁶-ship fleet in one cell), where pile-ups put more than k bodies within ρ of one ship?

## The derivation these predictions come from

A k-nearest watch catches a contact (i, j) only if, at the watch moment, fewer than k other bodies are closer to i than j (min over both directions, the gold's own metric). At closest approach d(i,j) ≤ ρ, so every body closer than j is itself within ρ of i: **a miss ⟺ a pile-up of ≥ k+1 bodies within ~ρ**. Expected neighbours within ρ of a fleet body:

  μ ≈ (2ρ / s) · (ρ / h),   s = local along-track spacing, h = radial breathing ≈ max(2e·a, ρ).

The gold's fleets: s ≥ 1.25ρ and e ~ 1e-3 ⇒ h ~ 10–20ρ ⇒ μ ≈ 0.01–0.16: pile-ups impossible, rank ≤ 4 nearly tautological. The gold's headline ruin scenario: 10⁶ ships on one orbit ⇒ s = 2π/10⁶ ≈ 0.063ρ ⇒ 2ρ/s ≈ 32; with tight formation e ≲ 1e-4 (h ≈ ρ) ⇒ μ ≈ 32 ⇒ typical contact rank ≈ μ/2 + 1 ≈ 17 ≫ 4. **The rank evidence and the ruin arithmetic were measured on opposite sides of the pile-up threshold μ ≈ k.**

## Scenarios (ρ = 1e-4, a = 1, a-spread ±1e-5, apsides ±0.1; truth = position-grid brute force, unbiased w.r.t. longitude; ranks at each contact's refined closest approach)

1. **control-uniform** (nc=200, λ uniform ⇒ s ≈ 314ρ, e ~ Rayleigh(1e-3)): the gold's regime. Predict: all contacts rank ≤ 4 (distance, mean-λ and true-λ agree here); ~10–40 contacts over 20 orbits.
2. **control-jam-loose-e** (s = 1.25ρ, e ~ 1e-3 ⇒ h ~ 10ρ): the gold's tightest measured case. Predict: rank ≤ 4 still holds (radial gating, μ ≈ 0.16).
3. **jam-tight-e-s0.375** (s = 0.375ρ, e ~ Rayleigh(1e-4) ⇒ h ≈ ρ): μ ≈ 5.3. Predict: **misses appear** — miss_frac_k4 in 10–50%, rank_max ≥ 6.
4. **jam-tight-e-s1.25** (s = 1.25ρ, h ≈ ρ): μ ≈ 1.6. Predict: miss_frac nonzero but small (1–10%), rank_max 5–6.
5. **jam-loose-e-s0.375** (s = 0.375ρ, e ~ 1e-3): μ ≈ 0.5. Predict: rank ≤ 4 with at most isolated exceptions (≤ 2%).
6. **scale** (λ uniform, e ~ Rayleigh(1e-5) ⇒ h ≈ 0.2ρ): nc = 3200 (s = 19.6ρ, μ ≈ 0.1) no misses; nc = 12800 (s = 4.9ρ, μ ≈ 0.4) marginal; nc = 51200 (s = 1.23ρ, μ ≈ 1.6) a few % misses. The boundary moves as μ says; extrapolated to 10⁶ (μ ≈ 32) the k=4 watch misses the large majority (> 80%) of contacts.
7. **espread** (s = 1.25ρ, e ~ Rayleigh(1e-2) ⇒ equation-of-center amplitude 2e ≈ 160 spacings): distance-rank ≤ 4 (radial gating, h ~ 100ρ) but **mean-longitude rank inflates ≫ 4** (max > 20, miss fraction > 30% for a mean-λ-sorted train); true-longitude rank stays ≤ 4 (contact ⟹ equal true longitude). The cheap static sort key is the wrong one; the gold never says which it meant.
8. **trigger**: for every tight-e fleet above (μ > k included), the Binet-clump number stays ≤ ~1 and the sections are ~all Full — the trigger fires "train regime" on both sides of the pile-up boundary and cannot see the failure. For espread it correctly refuses (Binet diameter is e-scale).

## Instrument notes (pre-registered)

- Sampling dt = 5e-4 with relative motion per step ≤ 2.5e-5 = ρ/4 (worst case espread) ⇒ the grid truth misses no sub-ρ dip; refine step 5e-6 locally, relative motion per refine sample ≤ 1.5e-8.
- Contacts are conjunctions below ρ in a mutual-gravity-free Kepler fleet, the same truth model the gold used; finding conjunctions is purely geometric, so this measures the certificate, not the contact law.
- Kill criterion for my own claim: if jam-tight-e and scale-51200 both show zero rank > 4 contacts, density does not break the k=4 watch in the physical fleet family, the gold's premise stands strengthened, and the dossier says so with the μ-formula as the reason it holds.
