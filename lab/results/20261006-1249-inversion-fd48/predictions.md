# Predictions — inversion-fd48 (written before any run of the decisive experiments)

The inverted claim (from gold taleb-09b5, adopted 6 October): "every real encounter lies within
partner rank 4 along the orbit, so a phase-neighbour certificate at O(n·k) replaces the quadratic
tier, triggered by a dimensionless number (max pairwise Binet distance / eps_u ≤ 1)."

My inversion: partner rank is not a constant of the regime; it is a **local contact-band
multiplicity** — the number of bodies inside a ρ-disc — which the trigger (a Binet-diameter number)
does not bound. The gold's own evidence sat at the dilute edge (measured spacing ≥ ~ρ, radial
spread ~20ρ ⇒ expected bodies within ρ < 1), so "max rank 4" was the cliff's edge, not a plateau.
Their dossier flags exactly this hole as untested ("radial spread ≲ ρ·c ... which I did not write").

Scenes (all inside the firing domain: max pairwise |Δbinet|/eps_u ≤ 1, checked, not assumed):

1. **E1 echelon (deterministic):** 6 ships, e = 0, ϖ = 0, a spaced to put them in one radial file
   at t = 1: i at 1−0.45ρ, four middles at 1−0.2ρ, 1−0.1ρ, 1+0.1ρ, 1+0.2ρ, j at 1+0.45ρ, longitudes
   staggered by 0.02ρ of arc. All 15 pairs are true sub-ρ contacts (mutual distance ≤ 0.91ρ).
   - Prediction: the i–j pair has distance-rank 5 from i AND 5 from j (four middles are closer to
     both), longitude-rank 5 both ways too. A k = 4 watch (either metric, either side) misses this
     real encounter silently. Truth from the crate's own `truth_pair` on all radial pairs.
2. **E2 phalanx jam (seeded, the natural scene):** n_c = 800, a half-width 1.5e-5, e ~ Rayleigh(5e-5),
   ϖ uniform, λ ~ N(0, σ_λ) with σ_λ ∈ {0.01, 0.004}, ρ = 1e-4, a = 1, horizon 3 time units
   centred so the designed bunch sits at t = 1.
   - Prediction (σ_λ = 0.004): max partner distance-rank ≈ m̂ = πρ²·(peak linear density)/(radial
     band) ≈ 10, p90 rank > 4, and a k = 4 watch misses a double-digit % of true encounters
     (pairs missed on both directions).
   - Prediction (σ_λ = 0.01, control at the gold's own bunching): max rank ≈ 4–6, misses ≈ 0–10%
     (reproduces their "max = 4" at the cliff edge).
3. **E3 trigger domain (computed from definitions, no integration):** the gold's own rank scenes
   (e ~ Rayleigh(1e-3), ϖ ± 0.1) have Binet diameter ≈ 1.4e-3 against eps_u ≈ 1.5e-4: ratio ≈ 9–13.
   - Prediction: the trigger as specified (ratio ≤ 1) does NOT fire on the scenes that produced the
     rank ≤ 4 evidence; the firing domain is roughly e ≲ 1e-4, Δa ≲ 1e-4 at ρ = 1e-4 — and inside
     that domain the radial band is ~2ρ wide, which is precisely what makes the band multiplicity
     (and rank) unbounded as σ_λ tightens. Rank scales ∝ n_c/σ_λ at fixed ρ and band.
4. **Misses are false negatives only:** the watch never invents encounters; the failure is silent
   drops of true sub-ρ contacts in the exact regime the certificate was adopted for.

Kill criterion (pre-registered): the k = 4 train is unsound as adopted iff any scene with trigger
ratio ≤ 1 yields ≥ 1 true encounter with rank > 4 on both directions. If no such scene exists in
E1–E2, the adoption stands and I report the band-multiplicity number only as its missing invariant.

What would save the adoption: rank staying ≤ 4 in E2's jam (would mean the radial band cannot
stack bodies at these densities — i.e. my multiplicity estimate is wrong by an order of magnitude).
