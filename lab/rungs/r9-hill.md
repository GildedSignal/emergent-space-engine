# Rung r9: the Hill regime, and where kicks stop

Frozen by the integrator on 30 September 2026. `docs/law.md` (tides and the regime selector): below a tidal ratio τ₀, the parent's tide is a kick on (E, L) that is orbit-averaged on a stable orbit. At or above τ₀, the doll's two-body symmetry is gone but another appears. The Hill problem in Hill units (distance in Hill radii, time in the planet's orbital period) is the same for every planet, and it keeps the Jacobi integral, so its motions might compile once for all planets. The dense order is the fallback where no compiled form exists. Julien, 30 September: "under the right representation many symmetries can appear"; the oracles are guards, not shepherds. τ₀ is set by measurement, not by hand.

**Question.**
1. Up to what tidal ratio do orbit-averaged tidal kicks on a planet's two-body doll keep a moon's behaviours: the bound or escaped class, the apsidal precession rate, and the forced eccentricity? That value is τ₀.
2. Beyond τ₀, what fraction of the Hill problem's phase space (moons at 0.2–0.9 Hill radii, prograde and retrograde) lies on quasi-periodic tori that a compiled two-frequency generator can follow, and what fraction is chaotic, where only the dense order will do?

**Configurations.**
- `kick-avg`: the planet's two-body doll (Kepler around the planet) with orbit-averaged tidal kicks from the star.
- `hill-torus`: in Hill units, a moon on a torus is represented by its two frequencies and its torus section (found by frequency analysis of the truth's first 20 planet orbits, then compiled). It is scored only on seeds the configuration declares tori; its declared-chaotic seeds count against `compiled_fraction`, not against behaviour.
- `truth` (positive): direct integration of the circular restricted three-body problem (the same reference as `behave` B14: planet mass ratio 10⁻³, Dormand–Prince at relative tolerance 10⁻¹², converged). It must pass.
- `no-tide` (negative): the two-body doll without tides. It must fail.

**Cases** (sampler: Python `random.Random(20261010)`): 256 moons at a/R_H uniform in [0.1, 0.9], half prograde and half retrograde, random phases, run for 50 planet orbits. The tidal ratio τ of each seed is 3·(a/R_H)³ at its apoapsis (the star's tidal acceleration over the planet's).

**Domains** (each candidate is judged where the law would use it). `kick-avg` and `no-tide` are scored on the clearly hierarchical seeds (a/R_H ≤ 0.3, τ ≤ 0.081). `hill-torus` is scored on the seeds with a/R_H > 0.3 that it declares tori. `truth` is scored on all seeds.

**Metrics,** one set per configuration, over its domain:
- `class_match_fraction`: over seeds whose truth is not chaotic (the truth's class is unchanged under a 10⁻⁶ relative change of a), the fraction whose bound or escaped class matches the truth's.
- `precession_match_fraction`: over bound seeds, the fraction whose apsidal precession rate over the run is within 10% of the truth's.
- `tau0`: for `kick-avg`, run on all seeds but reported only: the largest τ below which both fractions are ≥ 0.99.
- `compiled_fraction`: for `hill-torus`, the fraction of seeds with τ ≥ τ₀ that lie on tori it can follow with class and precession matching (reported, not gated).
- `dense_steps`: as in r4 (0 for candidates).

**Output.** `metrics.json`, plus one picture: class and precession error against τ for each configuration, with τ₀ marked, and a Poincaré section in Hill units showing tori and the chaotic sea.

```configs
kick-avg candidate
hill-torus candidate
truth positive
no-tide negative
```

```criteria
class behaviour class_match_fraction >= 0.99
prec behaviour precession_match_fraction >= 0.99
cheap type dense_steps <= 0
```
