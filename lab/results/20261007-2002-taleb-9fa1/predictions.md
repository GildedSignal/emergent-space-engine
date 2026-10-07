# Predictions (written before the `main` and `scale` runs)

Only the `smoke` scene (n=60, σ_e=3e-3, 5 orbits, seed 999) has been run: it verified the
plumbing and showed λ-rank 1 vs mean-anomaly-rank 29 on its 2 encounters. Nothing below is
tuned on any of these scenes. Scenes: co-orbital bundle, a ∈ [1, 1+1e-4], Rayleigh e with
spread σ_e, ϖ uniform (their belt convention), λ uniform, ρ = 1e-3, 30 orbits, n = 300,
seed 20261007 (s1e-2 repeated with seed 20261008). Keys sorted at t = 0; miss_k = fraction
of true encounters with circular rank distance > k. Truth: the crate's `truth_pair` on all
pairs (exact radial prefilter).

Derivation to check (the fish's water): two bodies can be close only at true-longitude
alignment, Δθ ≲ ρ/a; so at encounter Δλ = Δϖ + ΔM = O(e_i + e_j) + ρ/a while ΔM ≈ −Δϖ.
Needed rank in λ ≈ n·(2(e_i+e_j) + ρ/a)/τ. In mean anomaly the partner sits at rank
≈ n·|Δϖ|/τ — arbitrary.

1. **gold-corner** (σ_e=3e-4, the gold's own co-orbital corner): λ miss4 = 0 (positive
   control). Mean-anomaly miss4 > 50% even here.
2. **s1e-2** (σ_e=1e-2): λ miss4 in [30%, 70%]; median λ-rank 2–5.
3. **s3e-2** (σ_e=3e-2): λ miss4 > 80%; median λ-rank 8–15.
4. **aligned-s3e-2** (σ_e=3e-2 but all ϖ equal): λ miss4 < 10%, median rank ≤ 4 — same
   thickness, same concentration, different answer; isolates apsidal spread as the mechanism.
5. **gate-s1e-2-r1e-2** (σ_e=1e-2, ρ=1e-2): λ miss4 improves but stays > 10% — raising ρ
   toward the thickness does not restore rank 4, because 4σ_e, not ρ, dominates the rank
   budget. (This falsifies my own first-draft gate "S = thickness/ρ ≲ 1"; the gate has to
   budget the rank itself.)
6. **shear-da1e-2-s3e-4** (a-spread 1e-2, thin e): encounters only among near-equal-a
   pairs; λ miss4 small but > 0 at 30 orbits, ≈ 0 in the first 5 orbits (drift grows with
   the horizon at fixed sort).
7. **scale** (σ_e=1e-2, ρ=1e-3, 20 orbits): median λ-rank scales ∝ n: ≈2 at n=300, ≈4 at
   n=600, ≈8 at n=1200; miss4 rises from tens of percent toward ≳90%.
8. **Encounter-time geometry** (all scenes): median |Δθ(t_enc)| ≲ ρ/a; median
   |Δλ(t_enc)| ≈ 2·(e-scale); |ΔM(t_enc)| follows Δϖ (uniform-ish).
9. **Rank law**: median λ-rank ≈ n·median|Δλ(t_enc)|/τ within a factor ~2 across scenes.

**Kill criterion for the adopted claim** (gold 20261006-0346, feeding b-coorbital-cert):
"under co-orbital concentration every real encounter lies within partner rank 4 along the
orbit" is killed as a general rule if any scene with C = thickness/spacing ≲ 1 (the
fleet-on-one-orbit regime the trigger is meant to detect) shows λ miss4 > 5%. The positive
control failing (gold-corner λ miss4 > 0) would void the instrument instead.
