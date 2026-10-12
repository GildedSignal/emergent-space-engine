# Dossier — 20261012-0036-scout-aac1 (scout lens)

## Claim

The galaxy doll can compile each orbit from (E, L) exactly as the star doll does — 1D radial
quadrature against the doll's Φ(r) is exact in 2D, costs ~700× less than stepping and reads back
with bounded error — **but the regime cannot be gated by a static resonance flag from the initial
cycle**: under a rotating m=2 perturbation, migration (resonance overlap) reaches 14% of a broad
disc population at a 3% bar and 55% at a 10% bar, concentrated from corotation outward, so (E, L)
drift must be owned by the kick layer with re-anchoring, and the quiet/churned boundary follows
the pattern speed in space, not per-orbit frequency tags.

## Bottleneck

Board focus item "fitting 10⁹ in 8 GB" / "Cost at a billion" at galaxy scale: representation.md
§1 currently answers "where no mass dominates" with Cartesian + kicks — per-orbit work for every
body, the ~190-core path. The star doll's own mechanism (cycle memo keyed by quantized (E, L),
positions derived, kicks carry perturbations) had never been tested against a galaxy potential.
Expected gain: per-orbit cost → ~0 for quiet bodies (compile once ≈ 0.5 ms, each read ≈ 15 µs,
vs ≈ 5.9 ms per radial period of DOP853), i.e. the difference between compiling the galaxy disc
and stepping it. PRINCIPLES 6 ("store the generator, not the generated") and 14 ("you don't
advance a ship tick by tick you just map where it wants to go").

## Evidence

All numbers from `python3 probe.py data/probe.json` (repo: `lab/results/20261012-0036-scout-aac1/`,
279 s wall, 1.9 GB RSS, load 1.7–3.3 on the shared 8-vCPU runner; DOP853 rtol 1e-10 truth).

- **The compile is exact enough and cheap.** Roots + 12 ψ-panels × 16 Gauss–Legendre nodes
  (the same Darwin-phase shape as `space-darwin16-v1`): 516 µs per orbit in pure Python;
  position readout by table lookup + mirror: 15 µs. Stepping the same orbit 60 radial periods:
  354 ms. **≈ 690× per 60 periods, growing with elapsed time** (compile is once). Readout error
  over 40 cycles: median 4.9×10⁻⁴, max 9.7×10⁻⁴ in r — table-resolution error that repeats every
  cycle (bounded, not compounding; the right error type, PRINCIPLES 2 and 13). A generic rosette
  precesses (Δφ = 4.547 ≠ 2π), and the cycle carries it — the galaxy doll needs no Stäckel fudge
  because 2D axisymmetric potentials are integrable by quadrature (in 3D they are not; Sanders &
  Binney 2015's fudge is the 3D answer, UNVERIFIED accuracy numbers).
- **The naive regime gate fails.** Detector min_k |2(Ω̄φ−Ωp)/Ωr − k| < w on frequencies compiled
  from the initial (E, L): best recall 13% at fpr 14% (main, ε=0.03, 380 orbits, 60 radial
  periods each; sweep in data/probe.json). Walkers (|slope|/se > 4 on L(t)) sit at median
  resonance-distance 0.317 — *farther* from integer resonance than quiet orbits (0.197), because
  migrated orbits carry their initial-cycle frequencies away from where they were trapped.
- **Where the churn actually is.** Walkers at ε=0.03: 0% inside R<1.8, 42% in [1.8,2.3]
  (corotation R_CR=2.18), 51% in [2.8,4.1] (OLR R=3.57 and beyond); dL median 17% (p90 30%) —
  real radial migration, the spiral-bar overlap mechanism (verified at source: Minchev-style
  "Spiral-Bar Resonance Overlap" radial migration, arXiv 2009). At Ωp+25% the churned band moves
  inward to [1.3,2.3] with the resonant rings, no retuning. At ε=0.10: 55% of the disc walks,
  dL median 66%, p90 146%.
- **Prior art verified at source** (arXiv API, 12 October): proper elements as quasi-integrals
  screening millions of objects (space-debris 2021, NEO resonances); Sanders & Binney 2015
  review of rapid action estimation; AGAMA (action-based galaxy modelling, 2025 docs). None of
  it addresses gating under resonance overlap at game timescales; that is this run's negative
  result.

## Predictions (predictions.md, written before the run)

- P1 (recall ≥ 80% at fpr ≤ 20%): **FAILED** — 13%.
- P2 (95% of non-flagged orbits bounded): **FAILED** — 14% of the population walks at ε=0.03
  (though 0% inside R < 1.8).
- P3 (≥ 10³× cost ratio): **held in spirit, missed the letter** — 690× per 60 periods, rising
  with elapsed sim time; eval-on-read is 2×10⁴× cheaper than stepping one period.
- P4 (flagged fraction < 50%): **moot** — the gate does not separate; the honest regime size is
  the measured churned fraction: 14% (ε=0.03) to 55% (ε=0.10).
- H1 (recall < 60% at ε=0.10): **held** — 6%, far worse than predicted.
- H2 (churn follows Ωp in R): **held** — band moved inward with the shifted pattern speed.

Instrument limit, reported as held: the slope t-stat cannot separate a true walk from a trapped
libration whose period exceeds the window (the r4/Clairaut lesson, and B12's open problem); some
of the 14% may be wide librators. Only longer windows (or the angle itself) can tell.

## What would make it wrong, cost of adoption, fit

Wrong if: the 60-period windows are simply too short and the walkers are librators (testable with
10× windows); or my bar model (rigid m=2, smooth A(r)) misrepresents the game's perturbation
spectrum. Adoption: none this run — the compile mechanism slots into the existing cycle-memo
shape (quantized (E, L) keys, ψ panels, mirror, re-anchor), but the regime selector must be
redesigned around what the evidence supports: the kick layer owns (E, L) drift everywhere (the
re-anchor rule, ~0.05 compiles per kick, already in law.md), and the quiet/dense boundary is
spatial and pattern-locked (doll edges at the churned band, moving with Ωp), not a per-orbit
resonance tag. PRINCIPLES fit: 32 ("symmetry is found, not given" — the annulus quadrature is
the galaxy's water for the star doll's fish), 33 ("a body resolves only the influences
significant at its own scale"), 19 ("a fix signals the wrong representation" — the static
resonance flag was the wrong representation of the regime boundary, and the probe killed it
before it became a bandaid).

## The lens

The scout lens surveys and probes; it did not build the integer version, did not test encounters
in (E, L) space (proper-element screening at galaxy scale), and ran one potential, one pattern,
two strengths. It also cannot see whether Opus's motion-law v2 already implies the re-anchor
cadence that this result requires — the integrator should check `lab/refs/opus-motion/memo.md`
before adopting anything. Floats explored here; no integer decided anything canonical.
