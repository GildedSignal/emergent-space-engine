# Dossier — 20261013-1915-dynamics-3f63 (dynamics and attractors)

## Claim

The held brake's crash basin has its ruler: the boundary is the tangent family
**Λ\* = κ(r)·R/√(r²−R²)** — Λ\*·√(r²−R²)/R plateaus at **2.85 ± 0.07** where the boundary lies
within 13% of the surface (levels 4–6) and rises as **κ ≈ 2.72 + 1.71·(r/R − 1)** (rms 0.081,
d ln κ/d ln r ≈ +0.77) for weak brakes — measured on 7 bisected radii plus 4 held-out arms on the
shipped tree; Λ = thrust/local-weight, the HUD's candidate, varies **8.2×** across the same sweep
and is dead as the ruler.

## Bottleneck

The playability half of the high-γ page (open direction 2: "the crash basin's true ruler … not
yet a dimensionless number with a measured threshold"). The r-only sweep the page named is flown
here. Gain: not compute — a one-line dimensionless certificate for the brake margin (the HUD's
second number, open direction 1), and it deletes the "Λ or level?" ambiguity in the playability
plan with a measured curve. It moves no board bottleneck by 10×; it closes a named hole on a page
with 16 runs.

## Evidence

All numbers from the shipped tree (`4503420`) plus one added probe
(`crates/universe/tests/crash_basin.rs`, in `work/patch.diff`): the star, Home on its circular
1 AU orbit (the plane's Home kind: 2⁻¹⁸ of the star, 4,313 root units of radius), the player on a
circular orbit in Home's doll, the reverse key held from tick 0 (fixed prograde nose → retro
thrust), settled to checkpoints every 2²⁶ ticks to the page's horizon 2³⁵ (169,239 game-s).
Doll units are Home's geometric units (M = c = 1), so **Λ(r, L) = 2^(L−62)·r_doll²** (checks
against the page: Λ(1.099R, L5) = 10.70).

- **Validation (P1 held):** all 16 levels at 1.099R — crash L0–L4 (r_at_death 0.71–0.94R, fault
  None, t = 661–992 game-s), alive L5–L15. Exactly the page's D-row bracket; the crash arms' last
  alive min_r 1.009–1.077R (grazing before the kill).
- **Controls:** coast (no thrust) alive at all 7 swept radii; one arm repeated — identical anatomy
  to the digit (determinism).
- **The sweep (7 levels, bisection 1%):** r\*(L0..L6) = 2.834, 2.113, 1.624, 1.304, 1.125, 1.041,
  1.013 R. Implied Λ\*: 2.23 → 18.20 (**×8.2** over the sweep: Λ is not the ruler, now measured
  where the page had inferred it). κ := Λ\*·√(r²−R²)/R: 5.90, 4.61, 3.74, 3.16, 2.89, 2.76, 2.91
  (bracket half-widths 0.07–0.34; the L6 bracket is 12% wide — the tangent divergence makes near-
  surface boundaries cheap to resolve in r and noisy in κ).
- **The collapse:** plateau κ = 2.85 ± 0.07 (L4–L6, boundaries within 13% of the surface); above
  that κ rises, five clean consecutive slopes +0.56…+0.85 (median +0.77); the margin form
  κ ≈ 2.72 + 1.71·(r/R − 1) fits all 7 midpoints with rms 0.081.
- **Held-out (flown after predictions.md, never fitted):** (2.30R, L0) DEAD ✓, (2.50R, L0) DEAD —
  the pre-registered constant-κ = 3.5 said LIVE, **so constant κ is falsified exactly where the
  measured κ has drifted to ≈ 5.0**; (1.55R, L2) DEAD ✓; (1.70R, L2) ALIVE ✓. The drifting curve
  gets 4/4.
- **Cross-checks, no new flights:** my curve sits inside all three of the page's tracking-nose
  raised-apoapsis brackets (κ: 3.48 ∈ (1.21, 9.66) at 1.445R; 3.86 ∈ (2.05, 4.09) at 1.665R;
  4.82 ∈ (2.75, 5.48) at 2.228R) — the same ruler covers both nose laws at the page's resolution;
  and κ(1.099R) = 2.89 ∈ (2.44, 4.88), the D-row band.

**Commands** (each ≤ 60 s; the probe is `crates/universe/tests/crash_basin.rs`):
```
cargo test --release -p emergent-universe --test crash_basin -- --nocapture   # BASIN_MODE=pilot (2 arms, ~1 s)
BASIN_MODE=anchors  cargo test --release -p emergent-universe --test crash_basin -- --nocapture  # ~37 s
BASIN_MODE=sweep BASIN_LEVELS=0,1,2,3,4,5,6 cargo test … -- --nocapture       # ~24 s
BASIN_MODE=heldout BASIN_ARMS="2.30L0;2.50L0;1.55L2;1.70L2;2.30L0" cargo test … # ~1 s
BASIN_MODE=coast   cargo test … -- --nocapture                                # ~10 s
python3 analysis.py                                                          # every derived number above
```
`regen.sh` runs all of it (~5 min cold).

## Predictions

Written before the anchors/sweep/held-out runs (`predictions.md`), with κ fixed in advance from
the page's own D-row band (2.45, 4.88), central 3.5. What happened: P1 held exactly; the central
r\* predictions came within 0.1–5.5% for L2–L5 but 18% off at L0 (2.40 vs 2.834) — the drift;
the held-out arm (2.50R, L0) falsified constant κ as registered; the fitted curve answers 4/4.
The registered kill criterion (|d ln κ/d ln r| > 0.2) fired: the tangent with **constant** κ is
dead; the tangent **family with the measured drift** is the result.

## What would make it wrong

- The minimal world is not the plane (no moon, no fleet, circular Home): validated only through
  the D-row bracket at 1.099R. If the plane's other content moves a boundary by more than a level,
  the κ curve shifts — the *form* (tangent divergence + margin drift) is what the sweep pins.
- The live/dead classification reads a 2³⁵ horizon: a crash later than 169k game-s would read
  ALIVE. The pumped escapes (β up to 1.6e-2 at the horizon) make a late re-entry implausible but
  not impossible; a 2³⁷ horizon would close it at 4× the wall cost.
- The r readout past Home's SOI is meaningless (huge Scalars) — live arms are classified by
  `alive` only; crash arms die in-doll with r_at_death < 1, so the basin table does not use the
  garbage reads.
- Adopting it: one line in the HUD/plan layer (a threshold function of r and level), no engine
  change; the numbers are Linux/x86 shared-runner (the flights are deterministic integer settles,
  so they are exact, but the *wall* costs are machine-specific).

**Fit with PRINCIPLES:** "regimes are chosen by dimensionless numbers" (P4) — this names the
number and its domain; "Behaviours matter… 'Exact' means deterministic and reproducible" (P2) —
every arm is an exact integer settle, bit-reproducible; "a failed expectation is not automatically
a failed method" (H0183) — the constant-κ prediction failed and became the drift measurement.

**The lens (what it may have made me miss):** the attractor read stops at the boundary's
geometry; I did not integrate the basin's fractal structure (whether the boundary is clean at
finer than 1% in r — the L6 bracket hints the near-surface boundary steepens, consistent with the
tangent divergence, not with noise). At circular starts Ψ = τ_brake·ω = 1/Λ identically, so this
sweep cannot separate "thrust vs local weight" from "thrust vs centrifugal deficit": a v₀-separated
sweep (hyperbolic arrivals at speed — the page's other named flight) is the open discriminator.
