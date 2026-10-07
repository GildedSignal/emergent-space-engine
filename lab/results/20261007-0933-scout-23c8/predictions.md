# Predictions (written before the first run of any scene)

Cases below are un-tuned; numbers are Fermi estimates from theory (2-D diffusion,
Pesin). Time 60-minute window; machine 8 vCPU shared, 15 GB.

- **P0 — instrument zero (S0, μ=0):** H_q ≤ 0.05 bits at every sample; median|ΔE| ≤ 1e-13. If not, the element round trip is broken → VOID.
- **P1 — secular scene (S1):** diffusive law: H(1e-8) grows ≈ 1 bit per doubling of t (slope dH/dlog₂t ∈ [0.5, 1.5]) until the sampling cap (≤ log₂8192 ≈ 13 bits). frac(λT>1) ≤ 2% of shadows; Pesin mean λ⁺/body/orbit ≤ 0.02 bits.
- **P2 — near 2:1 (S2):** H at equal t ≥ 2× S1; frac(λT>1) ≥ 3× S1; pumping visible (≥ 10 bodies clamped at e=0.97); p99|ΔE| ≥ 5× median (fat tail).
- **P3 — crossing perturber (S3):** ≥ 10% of bodies within 3 R_H; H(t) arrives in bursts (the per-sample ΔH jumps at encounter epochs rather than rising smoothly); bits per encounter-affected body O(0.1–10).
- **P4 — the money number:** in every scene the ensemble scar production stays < 1 bit/body/orbit. A sustained > 1 bit/body/orbit anywhere would put the smooth-belt premise at 10⁹ in danger and must be reported as such.
- **P5 — held-out quantum signature (the sharpest, un-tuned):** once scars are smooth on the 1e-6 scale, the diffusive regime gives H(1e-8) − H(1e-6) → 2·log₂(100) ≈ 13.3 bits (2 dims × 2 decades). A chaotic-minority regime instead gives a gap ≤ log₂(outlier count), independent of q. The q-slope of H classifies diffusion vs chaos without any exponent fitting.

What would falsify the thesis (H_live = KS entropy rate, diffusion cheap / chaos linear): P1's slope near 0 with H large (structure without growth — instrument artifact); or S1 showing linear-in-t H with λ ≈ 0 (distinctions without chaos — then KS entropy is the wrong quantity for H_live and the dossier says so).
