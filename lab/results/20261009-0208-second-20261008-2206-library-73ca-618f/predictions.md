# Predictions (frozen before the decisive run)

The named experiment from check.md on 20261008-2206-library-73ca (silver): validate the
α-profile statistic on **B12's own scene** — circular restricted three-body, Jacobi constant,
doll-edge handoffs, median seed — with a planted bounded law and a planted compounding law as
controls on both sides.

## Scene (frozen)

- CRTBP, μ = 2⁻¹⁰ (Jupiter-like, the repo's own convention), rotating frame, sep = 1.
- Doll edge = sep/16 = 0.907 Hill — the engine's `2^(2·Δlog₂m/5)` rule (records.rs).
- Ships: retrograde irregular satellites, pericentre q ∈ U[0.55, 0.75] Hill, apocentre
  Q ∈ U[0.95, 1.05] Hill (straddles the edge), random orientation — the strong-solar-tide
  regime. 60 candidates, keep the 16 survivors with the most crossings (≥ 20 required; the
  gate's replacement rule). A heliocentric co-orbital population was tried first and dies
  entirely inside 10³ orbits (the Wisdom chaotic zone) — measured, and the reason for this one.
- dt_base = 2π/256 per planet orbit; horizon 10⁴ planet orbits; |ΔC/C₀| sampled per orbit.
- Doll bookkeeping in every law, every step inside the doll: doll-local coordinates and
  sources (the indirect term, law.md), rotation about the barycenter in local form.
- Laws: sym-fixed (symplectic split, fixed dt) = bounded plant; sym-var (same split, dt
  re-chosen from the state each step, 0.5–1.0 × dt_base taper over 2 Hill) = compounding
  plant (the plane's failure mode); rk4-fixed = non-symplectic compounding plant;
  sym-sched (sym-fixed at dt/4 until orbit 300, then dt) = bounded plant with a transient.

## Decision rule to freeze (B12 v2 proposal)

Convict ⟺ top-decade α (10³→10⁴ orbits, local slope of the running max of |ΔC/C₀|)
> 0.2 on the median seed (median by final error among survivors above the 10⁻¹² float-noise
floor). The full profile is reported for diagnosis; early-decade transients do not convict.
B12 v1's statistic, for comparison: one window-fitted slope over [1, 10⁴] (and [1, 10³]).

A 10³-orbit shakedown (instrumentation only, informing levels not slopes) measured:
sym-fixed band ≈ 3×10⁻⁵, crossings ≈ 3–7×10³ per 10³ orbits, sym-var ≈ 1×10⁻⁴ at 10³ orbits.

## Predictions

| # | Case | Prediction |
|---|---|---|
| P1 | sym-fixed (bounded plant) | median seed: α at top decade < 0.15, every decade d ≥ 1 < 0.2; final max error ∈ [10⁻⁶, 2×10⁻⁴]; verdict BOUNDED. Decade 0 (10→10²) may read high (band exploration) — explicitly non-deciding. |
| P2 | sym-var (compounding plant) | median seed: top-decade α > 0.2 (diffusive 0.3–0.7 or systematic ≳ 0.8); final error ≥ 10× sym-fixed's median final. |
| P3 | rk4-fixed (compounding plant) | median seed: top-decade α > 0.2 (type), regardless of level — its level may sit below the symplectic band while compounding (type vs size). |
| P4 | sym-sched (bounded + transient) | B12 v1 window slope over [1, 10³] > 0.2 on the median seed (false KILL — the 16× band jump at orbit 300), while the top-decade α < 0.15 (the α-profile acquits). |

Kill criteria: if P1's median has any decade d ≥ 1 with α > 0.2 (instrument convicts a
bounded law on B12's scene), or if sym-var's or rk4's median top-decade α ≤ 0.2 (instrument
acquits a compounding law), the α-profile is **refuted on B12's scene** and the dossier says
so. If fewer than 8 usable seeds survive (any law), the scene is inadequate — report, do not
grade.

Honest priors: P2's level separation is the least certain (the walk was only 3× above the
band at 10³ orbits in the shakedown); P1's decade-1 creep from chaotic band exploration is
the main overlap risk.
