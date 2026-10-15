# Predictions — 20261015-2147-scout-66ae (the flux accumulator's feedback loop)

Pre-registered before the decisive run. Toy: planar Kepler belt, G=1, star 1,
a ∈ [1.0, 1.6), Rayleigh e0 = 0.02, N = 2000, μ = 3e-8 per body (sub-quantum
regime: even the strongest impulses at the detection cut b0 are far below the
smallest quantum q1), T = 40 orbits, 60 steps/orbit oracle detection. Oracle =
continuous pairwise transverse impulses dv = 2μ/(b·v_rel), momentum-antisymmetric,
detected on a polar grid (b < b0 = 0.01). Window = 1 orbit for all accumulator arms.

Arms:
- A (the proposal): per-body VECTOR accumulator S_i, fed each window by the
  local-density flux f = 4·μ·ρ_cell·ln(b0/b_min)·Δt (2-D law; direction from a
  deterministic golden-angle rotation, integer-friendly remainder kept); a kick of
  size q is applied when |S_i| ≥ q, remainder carried (largest remainder per body).
- B (control that must pass): per-body Poisson sampling of physical encounters
  (Λ = 2ρ v_rel b0 Δt, b ~ p(b)∝b, dv = 2μ/(b v_rel), seeded).
- C (negative control that must fail): scalar coherent accumulator — applies
  kicks of size q whenever Σ|increments| ≥ q (magnitude-only).
- A_glob (second negative): arm A fed GLOBAL mean density instead of cell density.

Scenes: uniform belt (5 seeds); held-out clump scene (200 bodies in one tight
co-orbital band, same total N). Quantum sweep q ∈ {3e-4, 1e-3, 3e-3, 1e-2}.

## Pre-registered predictions

- P1 (quantum invariance, the load-bearing one): arm A's heating (⟨e⟩ growth and
  σ_e) at every q in the sweep stays within 1.5× of arm A at q1 AND within 2× of
  the oracle band on the uniform scene. Mechanism: a thresholded random walk
  preserves the velocity second moment per unit time exactly at leading order
  (q²·λ_q = ⟨δ²⟩·λ), so behaviour is quantum-invariant; the only correction is
  the renewal overshoot O(δ/q) → 0.
- P2 (control): arm B matches the oracle band (within 2× on heating rate, both
  scenes). It is unbiased by construction; if it fails my instrument is broken
  and the run is VOID.
- P3 (negative): arm C over-applies heating by ≥ 5× (the coherence factor —
  it sums magnitudes, so it pays Σ|δ| as coherent direction: overestimates the
  second moment by ~ λ_window·... — order √N_enc per window) on the uniform scene.
  If C passes, the instrument cannot separate coherent from diffusive and is VOID.
- P4 (held-out clump): arm A (local density) tracks the oracle's clump heating
  within 2×; A_glob under-heats the clump (clump ρ is ~20× global) by ≥ 5× and
  over-heats the field by ≥ 2×. The locality of the density read is the requirement.
- P5 (tail): arm A's p99 e stays within 2× of the oracle's p99 at q1 and q4;
  quantization lumps (exactly-q kicks) may fatten the tail modestly but must not
  change its order.

Kill bar: P1 failing at any q (behaviour depends on the quantum) kills the
per-body vector-remainder accumulator as the 10⁹ belt's solo dynamics; P4 failing
kills the global-density read; the page keeps whichever survives.
