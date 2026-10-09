# Dossier — 20261009-0709-scout-5b6a

## Claim

In a 2D disk universe, a body's **billable** gravity-news cone saturates as the universe's
causal radius grows: the naive cone grows as R², but the quantum-gated significant set is a
property of the mass function's tail (not of N, not of universe age), and the far field's
actual news output at the probe is **0–2 events per orbit** whether the universe extends to
32 or to 8192 scale lengths — Julien's "we cannot handle the universe anymore" wall is not
at the light cone, provided the three doll rules (free fall absorbs the dipole, geometry
absorbs the smooth field, sub-quantum influences accumulate) are in force.

## Bottleneck

HANDOFF's unqueued top risk: "The light cone keeps growing (Julien: 'there will always be a
point where we cannot handle the universe anymore')". It sizes the load that the queued
`b-news-gravity` build (cursors per (body, source)) must carry: if the per-body significant
source set grew with game time T, that design would be dead at scale. Expected gain: deletes
the scaling fear for the news layer and bounds its cursor set to O(mass-function tail);
no new component — it confirms the existing doll rules are the mechanism.

## Evidence

All numbers from `cone.py` (static + generator accounting, ~3 s) and `cone_news.py`
(retarded news events, ~75 s), both under `lab/results/20261009-0709-scout-5b6a/`, on this
8-vCPU Linux box, numpy float64, seed 20261009, peak memory well under 2 GB. Reproduce:

```
cd lab/results/20261009-0709-scout-5b6a && python3 cone.py cone_results.json
python3 cone_news.py news_results.json
```

Scene: 2D disk (~4×10⁴ sources, circular orbits in the smoothed field), probe at r_p = R_d
on a circular orbit; billed tide = traceless in-plane l=2 (doll absorbs l=0/l=1); quantum
ε_q·τ_loc with τ_loc = Ω_p²; retardation by light-cone Newton iteration. ε_q ∈ {10⁻⁴, 10⁻⁶, 10⁻⁸}.

- **Naive cone (P1):** uniform disk, sources within R: 20 → 40 140 for R: 1 → 8192 (∝ R²).
  Reading everything in the cone is dead at scale.
- **Per-source significance saturates (P2):** beyond R_sat ≈ (Gm̄/ε_qτ_loc)^{1/3} no source
  bills alone. Uniform disk at ε_q = 10⁻⁶: 1 782 significant of 40 144 — the far 38 000
  never bill individually, at any universe age.
- **Significant set is the mass function's tail, not N (P2):** Pareto (dN/dm ∝ m⁻²)
  galaxies at N = 4×10⁵ vs 4×10⁶: individually-significant far sources 8 425 vs 8 064
  (N-invariant within noise); crumbs resolve 10× finer and change nothing.
- **Aggregate levels (P3):** billing dyadic levels: exponential 11–12, clump+companion
  17–18, uniform-to-8192 30 — log of the tide's dynamic range, not ∝ R.
- **Clump (P5):** a 0.1 M_d companion at 30 R_d bills as ~6 extra aggregate levels while
  its 15 000 member sources add zero individual cursors.
- **Compiled-generator size is R-invariant (P3):** kept Fourier lines (quantum-gated):
  exp R_max = 8192 vs 32: 20 755 vs 20 647 (ε 10⁻⁶); 12 229 vs 12 134 (ε 10⁻⁴).
- **Generator does not compress a flat mass function (found, negative):** kept lines ∝ N
  (20 755 → 203 603 → ~2.1 M for N = 4×10⁴ → 4×10⁶, equal masses): sub-quantum shot noise
  has ~n significant lines. Reconstructing the crumbs is the wrong representation; they
  must ride principle 6's accumulate-and-carry, which is what the next measurement bills.
- **Far-field news output (P4, decisive):** tidal work W(t) on the probe (dipole removed —
  the doll's free fall owns it), retarded sources, 40 orbits: **0.99–2.0 events/orbit
  across all scenes, both ε_q, and both universe radii** (exp 8192/32: 0.99/1.07 at
  ε 10⁻⁴; unif 8192/32: 1.75/1.66). maxW/q = 0.0 everywhere: the far field never pumps
  one full kick quantum into the probe's orbit; the ~1 event is the t = 0 transient.
  With the dipole included (wrong billing) the rate is ~10⁵/orbit — the dipole is exactly
  what the doll's origin-fall absorbs at one vector per epoch, amortized over members.

## Predictions

`predictions.md` was written before the decisive run. P1, P2, P4, P5 held as predicted,
including the constants' orders. P3 held as log-growth (predicted "10–40 levels"; measured
8–30). Two honest misses: (a) my first news metric (quantum crossings of the aggregate
tide's value) was the wrong cost model — it charges derivable evolution that principle 3
makes free (~10⁸ events/orbit); replaced by the work-output metric above. (b) I did not
predict that line-level reconstruction fails to compress flat mass functions; it is the
run's one negative finding and rules out a per-level Fourier store for the crumbs.

## What would make it wrong

- Restricted approximation (Toomre–Toomre style): the probe stays on a smoothed circle.
  Real orbits have epicycles, so **resonances** with the far field's pattern speeds can
  pump; the law's existing resonance rule (detected from compiled frequencies) must gate
  those, and a follow-up should test an eccentric probe. This is the likeliest real leak.
- Newtonian tides with 3D falloff through the plane, not GR news; the far-zone radiative
  multipole structure is the same (Thorne 1980) but GR corrections are UNVERIFIED here.
- Annuli centered on the disk are a proxy for mass-centered dolls; constants change, the
  convergence argument does not. In 3D the ring-tide sum diverges logarithmically — 2D is
  not just cheaper, it is convergent; if the game ever grows a third dimension the wall
  returns.
- ε_q was parametrized (10⁻⁴–10⁻⁸), not derived from the law's integer widths.

## Cost of adopting

Nothing to build: it confirms the design's three doll rules as the answer and bounds
`b-news-gravity`'s cursor set to the significant tail (≈10³–10⁴ per galactic scene at
ε 10⁻⁶, ≈10² at ε 10⁻⁴), shared through doll moments rather than per-body. It deletes the
"cone grows forever" scaling fear from the risk list, replaced by a named residual:
far-field resonances on eccentric orbits.

## Fit with PRINCIPLES

- "Light cones partition compute" (5) — measured: the partition is finite because the tide
  quantum cuts it.
- "Influences below one quantum accumulate" (6) — the crumbs' 10⁵-quanta reconstruction is
  unnecessary; their output is < 1 quantum per orbit.
- "Each scale resolves only what matters at that scale… smaller ones enter as an aggregate"
  (33) — the significant set is the mass function's tail, invariant under 10× refinement.
- "Compute only surprises" (3) — the smooth far field's evolution is free; only work
  output above a quantum is an event.

## Prior art (the lens's survey)

- **Toomre & Toomre 1972** (ApJ 178:623, verified): restricted three-body treatment of
  galaxy tides — far-field perturbations on test orbits, the practice this probe inherits.
- **Thorne 1980** (Rev. Mod. Phys. 52, "Multipole expansions of gravitational radiation",
  verified to exist/scope): far-zone fields as radiative multipoles — the GR-native version
  of one aggregate per scale. UNVERIFIED beyond scope.
- FMM (Greengard–Rokhlin): well-separated interactions through aggregates only — same
  convergence structure. UNVERIFIED at source this run.
- Largest-remainder accumulation for sub-quantum remainders: already a lead on the board
  (polymath scan).

## The lens (what scout may have missed)

A scout reads the literature's requirements, not ours: none of these fields bills gravity
news at a fixed quantum for gameplay determinism, so the constants here are ours alone.
The bigger risk is strawman physics: circular orbits everywhere, one probe radius, no
self-consistency (sources answer to the same field), no GR. The resonance residual is
where I would attack this dossier first.
