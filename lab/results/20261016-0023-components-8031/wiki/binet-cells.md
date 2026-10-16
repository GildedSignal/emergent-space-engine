topic: binet-cells
status: open
closed-by:
valid-while:
updated: 20261016-0023-components-8031

# Binet cells: the in-cell law of r1, measured and margined

## Current best

**The frequency belongs to the orbit, not the band — and that mechanism is already the
shipped law: law.md §Motion 2 (`space-darwin16-v1`, 30 September, "it replaced the in-band
area-preserving map, whose band-centre tangents carried a first-order slope error in every
cell holding a turning point"), now `space-darwin16-scaled-v6-plunge` in `crates/space`,
which compiles each cycle once from (E, L) by the factored cubic and Darwin-phase
quadrature and is checked on the near-circular family by `tests/near_circular.rs`
(checker correction, 8031).** 8031's `agm` arm is an independent float re-derivation of
that shipped mechanism, not a new one; its advance exactness is by construction (the run
admits the metric is a wiring check). The
page's open direction 2 is answered and reframed: the per-orbit refit as worded (centre =
(u_peri+u_apo)/2) kills the near-circular first-order family (worst 4.7e-16, p = 6.5–1000)
but fails elsewhere — eccentric advance error ~(2e−0.92e²)/p (12.4% at the held-out
p = 8.5, e = 0.9) and the period read through the rung's dt/dφ rule collapses to 0.47 pass
(worst 6.8e-2); the invariant-only centre 1/L² fails the e=0 family (1% bar at p ≲ 30–35,
0.1% bar at p ≲ 60–100; checker-corrected from "p ≈ 300"). What
works: **delete the centre from the dynamics** — the cycle's frequency compiled from its own
two turning points (exact cubic from (E,L), closed form, then Darwin's
4√(p/d)K(4e/d)−2π by AGM, ~30 flops once per compiled cycle) makes the advance **exact to
8×10⁻¹⁶ at every m** (precession 256/256, errors m-independent to 1 ulp at m = 2/8/16; the
separatrix divergence as d→0 emerges), so m collapses from an accuracy dial (frozen needs
m=32 for a clean pass) to a pure cost dial: **m=2 gives 4 crossings/cycle against
frozen-m32's 78 — 19.5× fewer events, 12 orders better advance** (a comparison against the
replaced band law; the shipped law's m is a ψ-cut grid, not a frequency dial). The honest
residual moves to the period: the rotation's cosine shape mis-weights the periapsis peak at
O(e²u) (median 1.1e-3, worst 8.0e-2, 0.457 pass at the 0.1% bar; 44% at the separatrix
neighbour; checker: 26–46% at margins 0.2–0.02 outside the sampler) — but the shipped law
already has the shape word (dt/dψ in Darwin phase, periods ~1e-6 at m = 16, proven in
crates/space QUADRATURE.md); the run's period failure is its cosine strawman's, not an open
problem of the engine. Controls:
oracle ports validated to 2×10⁻¹³ against an independent RK4; the frozen control reproduces
the prior run's period pass fractions exactly (m8 0.9570, m16 0.9961) with no shared code;
frozen cycles repeat to 0.0 spread; ISCO pair passes on the band channel. Instrument
limitation disclosed: this port misclassifies 2 of 6 capture cases (L = 2.00, 3.88) — a
zero-length-cycle freeze at hyperbolic-band seams the frozen rung text does not specify;
the prior run's capture pass is not reproduced and the re-freeze must pin the seam rule.

r1 was executed once before, by its checker (H0205, 29 September, DISPUTED — never
graded): m16/m32 passed every criterion, m8 was too coarse. The red-team run
(20261015-1450-redteam-fe85, float64, oracle = ports of the shipped `gr_oracle.rs`
validated to 8.5e-11; checker-extended to the full frozen sampler) added the mechanism and
the margins. What stands: eccentric orbits are second order in band width (median advance
error 1.83e-4 at m=16, ÷4 per m-doubling to 1.68e-7 at m=512), strong field is comfortably
inside the 1% bar (held-out e=0.9 at p=8.5: 1.0e-3; separatrix margin p−(6+2e)=0.3:
2.4e-3), light is excellent (64/64, worst 2.4e-4; 9.9e-4 at b=5.5 near the photon sphere),
capture classifies both matter and photon cases to ±0.5% of threshold, ISO holds both
cases. What falls: near-circular orbits carry a FIRST-order band-centre error (advance
error = |2π(1/√(1−6u_k)−1) − Δφ_GR|/Δφ_GR, period error = √((1−6u)/(1−6u_k))−1, ratio
matched to 1.00; deterministic e=0 worst-offset circles fail the 0.1% period bar at p ≲ 60
(m=16) and p ≲ 35 (m=32)) — now deleted by the compiled-frequency law above, at every m.
The frozen `repeat` bar (1e-12 over 10⁴ cycles) is exceeded at the frozen horizon on float
(5.1e-12, 1.0e-11, two seeds) but H0205's implementation passed it, so the bar is
round-off-fragile, not float-unpassable; judge it in the law's integers. Crossings at the
full sampler: median 57 (m=16) / 117 (m=32) against the 512 bar (this run's port counts
38/78 — same scaling, edge-counting convention differs).

## Refuted

- "The per-orbit u_k refit (centre = the orbit's own ū) as worded" (open direction 2):
  deletes the e=0 first-order family but the period collapses to 0.47 pass and the
  eccentric corner pays ~(2e−0.92e²)/p advance error — measured, with the held-out 12.4% at
  (8.5, 0.9) matching the pre-registered 1PN estimate (20261016-0023-components-8031). The
  escape that works is deleting the centre, not choosing it.
- "The invariant-only centre 1/L²": 3u² off at e=0 — fails the 1% bar at p ≲ 30–35, the
  0.1% bar at p ≲ 60–100 (20261016-0023-components-8031; bar boundaries corrected by its
  checker: measured 1.23e-2 at p=30, 8.75e-3 at p=35, 9.6e-4 at p=100, 1.0e-4 at p=300).
- "A cosine-shaped cycle can hold the 0.1% period bar": 0.457 pass at the sampler, worst
  8.0e-2, 44% at the separatrix neighbour — the shape, not the frequency, is the residual
  channel (20261016-0023-components-8031; the pre-registered period prediction failed and
  is the finding).
- "m=16 fails r1's frozen period criterion" (an earlier headline, 95/96 on a subsample):
  at the frozen 256 seeds m=16 passes 255/256 (checker of fe85).
- "r1 was frozen and never run" (fe85's premise): H0205 records the checker execution;
  m16/m32 passed every criterion there too.
- "The freeze error is second order in band width" (fe85's own prior, from the eccentric
  family): first order on the near-circular family, law verified on deterministic circles
  (fe85 + checker) — and killed entirely by the compiled-frequency law (8031).
- "Strong field / separatrix / photon sphere is where the band map breaks" (fe85's
  pre-registered attack): all inside 2.4e-3 at m=16 — a negative result worth keeping.

## Open directions

1. **Re-freeze r1 with the compiled-frequency law, m as a cost dial (2 ≤ m ≤ 16), a
   deterministic near-circular row (now exact at every m), the Darwin shape word priced
   (direction 2), and the hyperbolic seam rule specified** — then run it for grade at the
   full 256-seed sampler with no cuts; the lab has still never graded r1 (H0205's open
   limitation). fe85's expected numbers plus 8031's row are the reference.
2. ~~**The cycle's shape word**~~ (checker: already implemented in the shipped law —
   dt/dψ in Darwin phase with the truncation bound proven in crates/space QUADRATURE.md,
   periods ~1e-6 at m=16; law.md §Motion 2). What remains open is only r1's re-freeze
   text adopting the shipped mechanism, priced by 8031's row as the cosine's counterfactual.
3. The capture channel's hyperbolic-band seams: the zero-length-cycle freeze
   (20261016-0023-components-8031, instrument limitation) against the prior run's pass —
   the rule must be pinned before any re-freeze counts capture_misclassified.
4. The multiply-add cycle update on the separatrix family (kick-cadence's territory):
   unguarded by any rung.

## Contradictions

- The capture channel: fe85 reports ±0.5% of threshold on all cases; 8031's independent
  port misclassifies 2/6 through a seam freeze the rung text does not determine. Both are
  ports of an underspecified rule; open direction 3 resolves it. (6765's galaxy-doll page
  notes near-radial orbits converge algebraically; the near-CIRCULAR family was the
  measured weak flank — different families, composed.)
- The strong-eccentric corner: fe85's port measures the frozen law at (8.5, 0.9) to
  1.0e-3 advance; 8031's port returns NOCYCLE there (hyperbolic band at the periapsis,
  event 0, rattles forever — checker-confirmed). The frozen text does not determine the
  turn/root rule inside unstable bands; same root as the capture seam above.

## Runs

- H0205 checker execution, 29 September (DISPUTED, never graded): m16/m32 pass every r1
  criterion, m8 too coarse, river killed; r1 still lacks a graded verdict.
- 20261015-1450-redteam-fe85 (silver): first-order near-circular law measured (ratio
  1.00, deterministic rows exact); m16 passes the frozen sampler with one seed of
  margin, m8 fails twice; repeat bar exceeded at the frozen horizon; m=16-FAIL headline
  and "never run" premise corrected by the check.
- 20261016-0023-components-8031 (lead, checker): the refit row — the centre deleted from
  the dynamics; advance exact (8e-16) at every m, m a pure cost dial (4 crossings at m=2 vs
  78 at frozen-m32); the literal refit and 1/L² priced and failed; the period is the
  residual channel on the run's cosine shape; capture seam freeze disclosed. Lead because
  the compiled-cycle mechanism is the shipped law (30 September), not a discovery; what is
  new here is the refit pricing, the seam underdetermination (extended by the checker to
  the frozen NOCYCLE at (8.5, 0.9)) and the sampler control.
