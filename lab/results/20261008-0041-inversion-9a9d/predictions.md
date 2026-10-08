# Predictions — 20261008-0041-inversion-9a9d (written before any run)

Inverted object: gold `20261006-0346-taleb-09b5` (co-orbital train certificate, k≈4).
Silent assumption under test: the guard "every real encounter lies within partner rank 4"
was measured as **distance-rank**, but the certificate it licenses is a **longitude-sorted
train** ("sort by longitude, watch k≈4 neighbours, rebuild on overtakes" — only a
mean-longitude sort has Diophantine overtakes). Distance-rank is close to tautological
(rank ≤ #bodies within ρ of the participant); sort-ranks are not.

Scenes: fleets (a=1±1e-5, ϖ clustered ±0.1 or uniform, λ uniform, e ~ Rayleigh(σ_e)),
ρ = 1e-4, all encounters adjudicated by the crate's independent truth (Halley +
conservative advancement), brute pairing binned by **true** longitude (the gold's own
lesson #6: mean-longitude binning misses encounters when e-spread ≫ ρ).

- **P1 (positive control, the gold's own fleet σ_e=0.001, nc=800):** distance-rank,
  true-λ-rank and mean-λ-rank all ≤ 4 for every adjudicated encounter. If this fails my
  instrument is broken, not the gold.
- **P2 (e-spread breaks the mean-λ train, σ_e=0.03, ϖ uniform, nc=800):** mean-λ-rank
  p90 > 4 and max > 16, while distance-rank stays ≤ 4 (both measured on the *same*
  encounters). Borderline held-out case σ_e=0.01: mean-λ max > 8.
- **P3 (sort-ranks grow with nc; fixed k is unsound at scale):** at σ_e=0.03, mean-λ-rank
  max at nc=1600 is ≥ 2× its value at nc=400 (roughly linear in nc); true-λ-rank ≤ 4 at
  both (window density nc·2ρ/2π ≪ 1 here). Arithmetic corollary at the design scale
  (nc=10⁶, no run): true-λ-rank ≈ nc·2ρ/(2π) ≈ 32 > 4, and mean-λ-rank ≈ nc·4σ_e/(2π)
  ≈ 2×10⁴ — neither sort supports a fixed k=4 at 10⁶.
- **P4 (the trigger's regime ≠ the ruin's regime):** clump number (max pairwise Binet
  distance / eps_u) > 10 at σ_e ∈ {0.01, 0.03} → the train is refused exactly where the
  pairwise tier pays the quadratic bill (cone candidates ≥ 0.9·nc²/2). Held-out:
  the gold's own σ_e=0.001 fleet already has clump number > 1 (trigger inconsistent with
  its own validation fleet).
- **P5 (crossers × fleet seam):** 40 eccentric crossers (pericentre sweeping the fleet's
  annulus) against the gold's 400-ship fleet: fleet×crosser cone candidates ≥ 0.9·40·400;
  true fleet×crosser encounters over 10 orbits O(10); pairwise setup work per real
  fleet×crosser encounter ≥ 10³× the intra-fleet figure — an outsider pays the fleet's
  cardinality. Held-out: the crosser's λ_true-rank among fleet members at encounter ≤ 4
  (a *global* true-λ train would cover crossers; the per-clump scoping is the hole).
- **P6 (misses):** the window tier's known miss class (4/233 in the gold) does not grow
  materially in the e-spread fleets or the crosser scene (misses ≤ 5% of adjudicated
  truth everywhere). If it does grow, that is a second result (soundness), reported.

Kill criteria: if P2 fails at nc=800/σ_e=0.03 I re-run at nc=1600 before claiming; if
P4's held-out sub-prediction fails (clump number ≤ 1 on the gold fleet) I report the
trigger as consistent and drop that line.
