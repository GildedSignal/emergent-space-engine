# Predictions — 20261009-0521-inversion-b1c0 (written before the held-out run)

Question: does the adopted k=4 phase-neighbour ("train") certificate (gold 20261006-0346-taleb-09b5,
build spec `b-coorbital-cert.md`) survive scenes its author did not run — tighter bunching (jam),
blobs, and e-spread at fixed crowding?

Tuning scenes already run (anchors, not predictions): G-uniform (rank ≤ 1, 0.2 overtakes/body/orbit),
A-phalanx (236 encounters/orbit vs the gold's 233 on the same scene parameters, rank_long_max = 3 —
reproduces "rank ≤ 4"), B-espread (σ_e ×10: rank unchanged ≤ 3, overtakes 113/body/orbit).

Held-out scenes (ρ = 1e-4, a_hw = 1e-5, 1 orbit, seeds 101–106):
- C-jam5: n=400, σ_λ=3e-3   → predicted median spacing ≈ 2e-5, J = ρ/s ≈ 5
- D-jam16: n=400, σ_λ=1e-3  → J ≈ 15
- E-blob: n=400, σ_λ=3e-4   → J ≈ 50 (whole fleet within ~10ρ along-track)
- F-blob2x: n=800, σ_λ=3e-4 → J ≈ 100 (same extent, double density)
- H-mixed: n=800, σ_λ=2e-3, σ_e=5e-3 → J ≈ 25
- I-highe: n=400, σ_λ=1e-3, σ_e=3e-2 → J ≈ 15, radial breathing 60ρ

Predictions:

1. **Crowding law.** rank_long_max ≈ 1 + c·J with c ∈ [1, 3] (bodies between the pair at contact
   fill the along-track contact window ρ; Poisson clumping puts c above 1). So C ≈ 6–16,
   D ≈ 16–46, E ≈ 50–150, F ≈ 100–300, H ≈ 25–75, I ≈ D plus a small factor.
2. **k=4 misses.** miss_k4_long > 0 in every held-out scene, and the miss fraction is a rising
   function of J; by E/F the majority of encounters have longitude-rank > 4 (the "zero misses"
   property dies in the jam).
3. **Quadratic return in the blob limit.** F vs E (extent fixed, n doubled): rank_long_max about
   doubles, so train cost n·k grows like n² at fixed physical extent — the ruin state the
   certificate was adopted to remove returns exactly in the densest scene.
4. **The two watches come apart at high e.** rank_dist ≤ rank_long everywhere, both > 4 in D/E/F
   (in a jam the longitude-intermediates are also the 3D-close ones); in I (breathing 60ρ)
   rank_dist stays small (radially scattered intermediates are far) while rank_long stays jam-high.
5. **The stated trigger does not select anything.** trigger_binet_over_eps ≫ 1 in every scene
   including the validated phalanx (measured 19 there in tuning), so the all-Full condition never
   fires at these spreads; the dimensionless number that actually tracks the failure is the
   crowding J = ρ/along-track spacing, which the adopted design does not measure.
6. **Maintenance is not rare.** overtakes per body per orbit ≳ 10 in every bunched scene
   (epicycle passes), rising as spacing shrinks — the "rebuild on overtakes = a Diophantine
   event" assumption undercounts by orders of magnitude in a jam.

Kill criterion for my own claim: if rank_long_max ≤ 4 in D and E ( jams), the train certificate
survives crowding and my inversion fails — that would say along-track ordering is a robust
proximity certificate at any density.
