# Dossier — 20261008-0041-inversion-9a9d (inversion lens)

**Claim.** The co-orbital train certificate (gold 20261006-0346-taleb-09b5) is unsound as
adopted on three counts, all measured on the gold's own scene plus one-parameter extensions:
its guard "partner rank ≤ 4" was measured as *distance*-rank (tautologically safe: it counts
bodies within ρ, and stays ≤ 4 in every scene here), while the sort the certificate must
deploy — mean longitude, the only one whose order changes by Diophantine overtakes — has
rank p90 = 30, max = 55 on the gold's own fleet (a k=4 train misses **79%** of its own
validated encounters), degrades to max ≈ nc at any e-spread ≥ 0.01, and its stated trigger
(Binet clump diameter ≤ eps_u) is violated **10–25× by the gold's own validation fleet**
(p50 4.16, max 24.09 at σ_e = 0.001), so the train is refused exactly where the pairwise
tier pays the quadratic bill (candidate fraction 1.000 of nc(n−1)/2 at every e-spread).

**Bottleneck.** Board item "candidate work must track real encounters" (the top scaling
risk) and the focus line "the co-orbital certificate" (also queued for Codex/GLM builds).
The adopted design's certificates do not compose: between "train triggered" (e-spread ≲
eps_u) and "pairwise affordable" (no shared-a clump) there is a desert — every same-a clump
at any e-spread — where work is quadratic with no sound cheap certificate; and any outsider
whose orbit crosses a clump adds ~0.25·n_clump pair-sections per outsider (measured
crossing fraction 1,994/8,000) for zero encounters at game densities.

## Evidence

Binary: `crates/encounters/src/bin/invert.rs` (+ `dispute.rs`), built
`cargo build --release -p emergent-encounters --bin invert --offline`; binary at
`/home/glmlab/lab-target-2/release/invert` (shared runner, orders of magnitude only).
Commands: `invert trigger`, `invert econ`, `invert base|e003|e010|e030|slope`, `invert cross`.
Encounters are the crate's `truth_pair` (Halley + conservative advancement, solver path
independent of the method) run over **every** cone pair, cross-checked by a brute binned by
*true* longitude (the gold's lesson #6 respected). ρ = 1e-4; every run ≤ 35 s except `cross` (≈ 3 min wall for truth over 2 orbits).

| scene (nc, σ_e) | truth enc. | dist ≤ 4 | λ_true ≤ 4 (max) | λ_mean ≤ 4 (p90, max) |
|---|---|---|---|---|
| base = gold's phalanx (200, 0.001) | 229 | 229/229 | 227/229 (5) | **47/229 (30, 55)** |
| e003 (200, 0.003) | 210 | 210/210 | 210/210 (4) | **15/210 (93, 152)** |
| e010 (200, 0.01) | 166 | 166/166 | 166/166 (4) | **0/166 (157, 196)** |
| e030 (200, 0.03) | 50 | 50/50 | 50/50 (2) | **0/50 (171, 193)** |
| slope (800, 0.03) | 852 | 852/852 | 833/852 (**8**) | **1/852 (715, 798)** |
| cross (200+40, 0.001) | 308 (0 fx) | 308/308 | 308/308 (4) | **57/308 (39, 75)** |

1. **The guard measured the wrong rank.** Distance-rank ≤ 4 everywhere (max ≤ 4 in all six
   scenes) — it can hardly fail: an encounter partner within ρ is by construction among the
   few bodies within ρ. Mean-longitude rank on the *same encounters*: p90 30 at the gold's
   own σ_e; 0% inside k=4 from σ_e = 0.01 up; max = 193 of nc = 200 and 798 of nc = 800 —
   it scales as nc·σ_e·(λ density), i.e. the mean-λ train at fixed k is the quadratic tier
   in disguise. True-longitude rank survives e-spread but grows with nc (max 2 → 8 for
   200 → 800) and exceeds 4 for 2/229 encounters even on the gold's own scene.
2. **The trigger refuses its own fleet.** `binet3/eps_u` on the gold's fleet: p50 4.16,
   p90 10.3, max 24.1 (ΔU-only: p50 0.041 — the a-spread is not the trigger's problem; the
   e-vector is, exactly the axis the gold's own "what would make it wrong" suspected). At
   σ_e = 0.03: p50 109, max 508. Full sections are 5.5% of the gold fleet's sections — the
   "all-Full condition" the trigger encodes does not describe its own validation scene.
3. **The ruin regime is broader than the certificate regime.** Cone candidate fraction of
   nc(n−1)/2 = **1.0000** at σ_e ∈ {0.001, 0.003, 0.01, 0.03} (79,800/79,800 at nc=400):
   every same-a clump is the complete graph, at any e-spread. At σ_e ≥ 0.01 the sections
   become ~all Cross (zero numeric-window evals — per-pair setup is *cheap*), but the store
   and the per-epoch query traffic are still 5×10¹¹ pair-sections at nc = 10⁶ (the gold's
   40 TB arithmetic, unchanged). The window tier itself was **sound everywhere here**:
   method missed = 0, extra = 0 on all five scenes (the gold's 4/233 soundness bug did not
   reproduce on the same scene and seed against an exact all-pairs truth).
4. **The seam.** 40 strikers (pericentre aligned to the fleet's bunch, q ∈ 1 ± 1e-3):
   1,994 of 8,000 fleet×striker pairs pass the cone (25%: the Binet cone does real work);
   those 1,994 pair-sections were certified and queried for **zero** encounters in 2 orbits
   (a fleet×striker conjunction is a 4-D coincidence at game densities). Extrapolated
   linearly in fleet size: any crossing population costs ~0.25·n_clump pair-sections per
   outsider per epoch — a 10⁶-body belt crossing a 10⁶ fleet is 2.5×10¹¹ pair-sections, the
   O(N²) ruin arriving through the composition, not either certificate alone.

5. **Instrument note, settled by a third instrument** (`dispute.rs`: dense scan +
   scan_minima + truth over 2 orbits): every brute-vs-truth dispute (4–5 per scene) is a
   t = 0 boundary coincidence — the bunched phalanx spawns some pairs already inside ρ at
   t = 0, which the truth excludes by its tm > 0 event convention. No instrument is blind;
   all counts here use the truth's convention.

## Predictions (predictions.md, written before the runs)

- P1 held: on the gold's fleet all distance-ranks ≤ 4 (and λ_true 227/229 — the 2 misses at
  rank 5 are the certificate's first crack).
- P2 held, harder than predicted: mean-λ p90 > 4 and max > 16 at σ_e = 0.03 **and already at
  the gold's own σ_e = 0.001** (max 55; I predicted base to pass — the mean-λ failure does
  not need e-spread, only the gold's own scene).
- P3 held: mean-λ max 193 → 798 for nc 200 → 800 (≈ nc); λ_true max 2 → 8. Design-scale
  arithmetic: λ_true-rank ≈ nc·2ρ/(bunch width) — at 10⁶ uniform, ≈ 32; k = 4 is unsound at
  scale for **both** sorts.
- P4 held, including the held-out sub-prediction: trigger ratio > 1 on the gold fleet
  (4.16 p50 — I predicted > 1, measured 4–24).
- P5 split: candidate clause **failed** as written (25%, not ≥ 90% of 40·nc: the Binet cone
  rejects non-crossing strikers — a correction in the design's favour, and the 25% crossing
  fraction is itself the measured constant for the seam arithmetic); the "zero fx
  encounters" clause of the economics held; the held-out λ_true-rank clause for crossers is
  unmeasurable here (0 fx encounters; a λ-sorted train's coverage of strikers is moot at
  these densities — the honest statement is the pair-count cost, not a rank claim).
- P6 held: no method misses anywhere (0/1,063 encounters across scenes); disclosed below:
  5–1 brute-vs-truth disputes per scene, adjudicated by a third instrument (dispute.rs).

## What would make it wrong

The rank claims are exact-minimum encounters from `truth_pair` over every cone pair at
nc ≤ 800; the nc-scaling is measured at two points plus arithmetic. What the λ_true-sort
fix would cost (order churn per orbit: λ_true − λ_mean swings ~2e per orbit vs inter-body
spacing ~1e-4 in a bunch, so a true-λ sort cannot be maintained by overtake events —
rebuild is per-orbit) is argued, not measured: a run that measures rebuild cost of a
true-λ sort at 10⁶ would complete the case. The seam economics extrapolate a measured 25%
crossing fraction linearly in n_clump; a skin (q-candidate-degree's slack) may amortize
re-certification across kicks and should be measured before adopting the arithmetic as ruin.

## Cost of adoption, fit with PRINCIPLES

Adoption is a *change to the certificate before it is built* (the co-orbital certificate is
queued for the Codex/GLM build week): (1) sort by true longitude, not mean — and budget a
per-orbit rebuild, not Diophantine overtakes; (2) size k by the dimensionless window count
nc·2ρ/(bunch width), never fix it at 4 (principle 4: "regimes are chosen by dimensionless
numbers"); (3) trigger the train on ΔU ≈ 0 (same-a identity — the measured ruin condition),
not on the e-vector clump diameter (the measured non-trigger); (4) the crossing-outsider
work must be priced into any clump certificate (0.25·n_clump pair-sections per outsider).
Fit: "a fix signals the wrong representation" (§19) — here the wrong representation is the
*guard's coordinate*, not the train idea; "write the kill criterion before the run" — the
gold's guard (distance-rank) was a control that could not fail, exactly the instrument
failure the README warns about.

## The lens

Inversion asks what the gold silently assumed: that the rank it could measure cheaply
(distance) is the rank the certificate must maintain (sort order). It assumed so without
stating the sort's coordinate. What this lens may have missed: I did not measure the
true-λ sort's *rebuild* cost at scale (argued only), and my crossers are one geometry
(pericentre strikers); crossing at mid-orbit radius or inclined... (2-D here) may change the
25% fraction but not the seam's form. My brute shares `state_at_mean` with the method's
solver path (Newton); the truth does not (Halley), and every reported encounter is the
truth's, so the shared-solver risk sits only in the dispute notes, not the ranks.
