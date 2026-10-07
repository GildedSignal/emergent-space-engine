# Bottleneck: H_live (distinctions per game-second) — requirements as numbers

HANDOFF risk (6 Oct): "they, not the body count, decide whether 10⁹ fit in 8 GB; **not measured yet**."

## Requirements (tied to PRINCIPLES)

| # | Requirement | Number | Principle |
|---|---|---|---|
| R1 | Bodies that must fit | 10⁹ (#24 memory floor is information) | goal |
| R2 | Memory budget | 8 GB → ≤ 64 bits/body all-in | goal, M1 |
| R3 | Program cost (already measured) | 0.126 bits/body (gold components-98bc) | #6 store the generator |
| R4 | Scar headroom | ≈ 63 bits/body minus catalogue/event share | #6 |
| R5 | Exact tube fallback | 16 bytes = 128 bits/body (law.md) | law |
| R6 | Certificate accuracy | ~10⁻⁶ relative per orbit shape (B5) → scar quantum | #13 errors never compound |
| R7 | Test budget | each scene ≤ 60 s, < 2 GB RAM (this runner) | AGENTS |

## Question restated in one sentence

At what bits/body/orbit does a doll's flow create distinctions no program can absorb, and does that rate force reabsorption faster than the game can pay?

## The candidate answer from other fields (scout thesis)

**H_live is the metric (Kolmogorov–Sinai) entropy rate of the doll's flow**, h_KS = ∫Σλ⁺ dμ (Pesin's formula; verified, scholarpedia / arXiv:1812.04308). Two regimes with different memory laws:

- **Diffusive (near-integrable) bodies:** scar spread ∝ √t → scar bits ∝ ~½·log₂t·(dims); memory *saturates* at the belt's own width in quanta. Belt chaotic diffusion is the astronomers' regime (Morbidelli 1999; "stable chaos" Milani). MD practitioners paid for the same law: round-off × Lyapunov decorrelates MD in ~1500 steps (Toxvaerd, JCP 2012).
- **Chaotic bodies (λ > 0):** any program loses h_KS·t bits, linearly, irreducibly. These must be re-programmed at cadence quantum/λ or stored exactly (R5).

## Instrument (this run)

Vectorized float64 restricted N-body (star GM=1, belt at a≈1, period 2π), exact-Kepler drift in osculating elements + perturber kicks with the indirect term (the law's own split, law.md "the doll's origin falls"). Scar = (ΔE, ΔL) from birth program, quantized; scar entropy H_q(t); Benettin shadows (256/scene) for finite-time λ distribution.

Scenes: S0 control (μ=0), S1 secular (a_p=5.2, μ=10⁻³), S2 near 2:1 (belt at 1.311, a_p=2.08), S3 crossing perturber (q_p=0.74, μ=10⁻⁴).

Floats explore; this is a falsifier on behaviour (growth laws, tails), not a canonical outcome.
