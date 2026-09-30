# Rung r8: finding encounters without work per orbit

Frozen by the integrator on 30 September 2026, before any run. Design: [docs/representation.md](../../docs/representation.md) §3 and §6. The table there says undisturbed orbits cost about zero. But knowing that a body is undisturbed is itself work: something must certify that no neighbour comes close. No rung measures that certification yet. If it costs a few events per body per orbit, the cost at a billion (board bottleneck 3) is set by the broad phase, not by physics.

**Question.** In one doll (a single dominant mass, 2D, Newtonian Kepler motion is enough here), N bodies orbit in a belt. Every pair that comes within a radius ρ of each other is an encounter: a contact, a per-conjunction kick, or a perception threshold. Can every encounter be found, none missed, at a cost proportional to the true number of encounters, rather than to the number of orbits?

**Configurations.**
- `element-sort`: bodies are bucketed by semi-major axis a (from E) into bins no narrower than ρ. Within each bin and its reach (the bins whose radial ranges [a(1−e) − ρ, a(1+e) + ρ] overlap), bodies are kept in a kinetic list sorted by mean longitude, which advances linearly at n(a). An event is a swap of list neighbours (a conjunction candidate); at each swap, the exact distance at closest approach is checked against ρ. A body is touched only at swaps and at its own element changes.
- `shear-grid`: cells in (r, φ − n(r_bin)·t), co-moving with the local mean motion (a shearing sheet). Bodies change cell only by epicyclic excursion and by the shear between bins. An event is a cell change, or two bodies in one cell or adjacent cells coming within ρ.
- `oracle` (positive): it reads the true encounter list from the brute-force reference, and its cost is the number of true encounters. It must pass, or the criteria are unpassable.
- `ring-cells` (negative): fixed ring × spoke cells (m = 16, N = 128), where each body schedules its next cell crossing and checks the occupants of the new cell. It must fail the cost criterion.

**Cases** (sampler: Python `random.Random(20261008)`).
- 16 belts: N = 10⁴ bodies, a uniform in [1, 1.5] (units of the doll), e Rayleigh-distributed with σ_e drawn log-uniform in [10⁻³, 3×10⁻²], random periapsis angles and phases, ρ drawn log-uniform in [10⁻⁵, 3×10⁻⁴]. Each is run for 20 orbital periods at a = 1.
- Scaling: the same belt at N = 10³, 10⁴, 10⁵ and 10⁶, at σ_e = 10⁻² and ρ = 10⁻⁴·(10⁴/N), so that each body's true encounter rate stays fixed and the true total grows linearly in N. Sized to fit 60 s per script (fewer periods at larger N is fine; the metric is per orbit).
- **Reference:** exact Kepler positions (solve Kepler's equation to 10⁻¹⁴) for each pair whose radial ranges overlap within ρ, with pairwise minimum distance found per synodic conjunction to 10⁻¹² relative. A pair's approach below ρ is an encounter. The reference may be slow; it is the truth, not a candidate.

**Metrics,** one set per configuration:
- `missed_fraction`: encounters in the reference not found by the configuration, divided by all reference encounters, pooled over the 16 belts (0 for a correct configuration).
- `false_fraction`: reported encounters that the reference does not contain, divided by all reference encounters.
- `work_per_encounter`: events processed (swaps, cell changes, crossings, checks) divided by true encounters, median over the 16 belts. For the oracle this is 1.
- `events_per_body_orbit`: events processed per body per orbital period, median over the belts. Report it; it is not gated, because a belt dense in encounters needs work.
- `scale_exponent`: the fitted exponent of events processed against N over the scaling runs, where the true encounter count grows linearly.

**Output.** `metrics.json`, plus one picture: work per orbit against the true encounter rate per orbit, one point per belt and configuration, with the line y = x.

```configs
element-sort candidate
shear-grid candidate
oracle positive
ring-cells negative
```

```criteria
complete behaviour missed_fraction <= 0.0
sound behaviour false_fraction <= 0.0
cheap cost work_per_encounter <= 10
scales type scale_exponent <= 1.1
```
