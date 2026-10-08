# Predictions — 20261008-0945-taleb-48e5 (written before the decisive runs)

Question: does the two-tier Binet-cone candidate tier still track real encounters under
**radial concentration** (dN/da ∝ a^-gamma cusps, and a dense ring), and does the *mean*
per-body candidate degree lie about the worst body (the allocator's cell budget)?

Workloads (all sigma_e 0.05 Rayleigh capped 0.5, rho 1e-4, exact cone test for candidates;
real encounters by the crate's exact per-pair checks over a horizon):
- A: N=30k on a in [0.3, 3], gamma in {0,1,2,3}, horizon 500 orbits, truth on.
- B: e-tail: sigma_e in {0.05, 0.15} at gamma=1, same N and range.
- C: N-scaling of the degree tail at gamma=2: N in {10k, 30k, 100k}, truth off.
- D: dense ring: N=10k on a in [1.0, 1.01] (all mutual candidates), horizon 100.
- E: control: gamma=0 at the same N ladder as C (uniform belt, the silvers' regime).

## P1 — baseline (gamma=0, E and A)
cand_per_enc (candidate pairs per real encounter, per sampled body) is a smooth function
of a, rising outward by a factor 10–100 across [0.3, 3]; no radial bin is sterile
(cand_per_enc < 1e7 with hits > 0 in neighbouring bins at the same a).
deg_max / deg_mean in 3–8.

## P2 — radial concentration (A)
Inner bins' cand_per_enc *falls* with gamma at fixed a (denser neighbourhood → each
candidate more productive): tracking improves with density; no sterile candidate class
appears in a power-law cusp. If instead some inner bin's cand_per_enc exceeds ~1e7
(setup paid, no yield — the radial analogue of the co-orbital failure), the tier
under-tracks concentration: that is the kill.
deg_max / deg_mean grows with gamma, reaching ~10–30 at gamma=3 (inner degree ~
a_lo^{1-gamma} scaling), but stays a smooth function of local density — the tail is
physical (encounters rise with it), not an artifact.

## P3 — what sets the max (A, B)
At every gamma the max-degree body is a top-eccentricity body in the *sparse* half
(smoke run: deg_max 710 at a=1.25, e=0.17 vs mean 256; deg_of_emax 595). So the worst
cell is set by the Rayleigh e-tail (capped at 0.5) times local density — predictable,
budgetable. Predict deg_of_emax within 0.5–1× of deg_max. If sigma_e 0.15 pushes
deg_max/deg_mean above ~10 at gamma=1 while cand_per_enc stays smooth, the tail is
e-driven (an input law, not a tier failure).

## P4 — N-scaling of the tail (C vs E)
At fixed gamma=2: exponent of deg_max vs N ~ 1.0 ± 0.15 (physical: local density ~ N).
scanned per body grows ~ linearly in N (the U-window is a fixed fraction of the belt —
the known O(N^2) scan), reported as the standing risk number, not a new claim.

## P5 — the ring (D)
deg ~ N (all mutual candidates); cand_per_enc stays within ~3x of the gamma=0 value at
the same a (concentration per se does not break tracking — real encounters scale with
density too). The cost moves to per-kick setup: one kicked ring body re-certifies O(N)
pairs — the allocator's worst cell is the population within one eccentricity reach, not
the belt mean. If cand_per_enc in the ring exceeds ~1e6 while the same-a uniform bin is
~1e4, near-degenerate-a candidates are sterile and the ring needs the co-orbital
(phase-neighbour) certificate too.

## What would make me wrong
- Any bin with hits=0 over >=500 orbits x >=1000 candidate pairs while same-a bins at
  other gamma have hits: sterile class, tracking broken.
- deg_max jumping discontinuously between neighbouring gamma (structural cliff).
- The ring's cand_per_enc diverging (P5's kill).
