# Dossier — 20261018-0143-dynamics-80fe

## Claim

The encounter-parity certificate (chaos-shadowing direction 2, e846's named successor) has its
rate form, and its shape is decided: the encounter process is a **burst, not a homogeneous
hazard** — before chaos decorrelates the trajectories the plane is **exact** (μ = 1e-2, ≤ 4 P:
8/8 first events the same ICs in plane and truth, all `planet_kick`, epochs matched to ≤ 0.014 P,
inside the plane's P/64 epoch grid); at the control μ = 1e-3 parity holds on the full ensemble
at the count level (47 plane kills against 40 truth first-entries, ratio 1.175, survival curves
within the 95% bootstrap band everywhere, max |ΔS| = 0.062 at 488 P); but the rate itself **falls
4× per synodic period from μ = 1e-3 to μ = 1e-2** (0.0076 → 0.0019/syn; first-entries 40 → 32,
recrossers 16 → 7, hazard ratio 1.6 → 16.9 across 128 P) — the thicker planet eats the layer
rather than feeding it, so no single-μ rate law exists and the certificate must carry the
per-synodic clock. The instrument is ensemble-stable and per-IC-scrambled exactly as the
shadowing clause predicts (rtol 1e-12 vs 1e-13: 40 vs 38 counts, max |ΔS| 0.028, but crossing
membership agrees on only 104/144 ICs). And a cost wall enters the record: the plane at μ = 1e-2
has a runaway tail after its first conjunctions (16 P unfinished for 144 ICs in 120 s on 2
workers; 64 P ≈ 2 ICs in ~6 min at 4 workers) despite a comparable median kick load per P.

## Bottleneck

Not a board bottleneck by bodies or kick cost: the instrument risk in HANDOFF ("B12 cannot yet
tell bounded from compounding on chaotic ships") and chaos-shadowing's named next step. Gain:
the B12-family survival bar now has (a) its statistic — first-event survival per synodic period,
resolved truth entries against plane kills, both error directions countable; (b) its exact
positive control (the pre-chaos burst); (c) its μ-domain (portable only with the synodic clock);
(d) a new plane-side cost wall at μ = 1e-2 for the board's smoothness line.

## Evidence

Ensemble: e846's (144 ICs = 12 synodic angles × du ∈ {±0.35…±1.45}·band, band = √(8μ/3)),
horizon 512 P truth / 512 P plane at μ = 1e-3, 4 P plane at μ = 1e-2 (the wall, below). Truth =
shipped `Integrator::until_crossing` on Model::Full (rtol 1e-12; every disk entry resolved, no
grids). Plane = shipped plane, step 7, e846's census counters. All commands in `regen.sh`
(~12 min; shared-host timings are orders of magnitude only). Raw: `work/{ev,pl}-*.jsonl`,
analysis `work/parity.py` → `work/parity.txt`, `work/burst.py` → `work/burst.txt`.

- **μ = 1e-3, full 144 ICs (this tree, my run):** plane 47 kills, 100% `planet_kick`, 0 refusals
  (channels identical to e846). Truth: 40 first-entries, 68 total entries, 16 recrossers
  (max 7), median first epoch 147 P ≈ 4 synodic. Parity: first-event counts 47/40 = 1.175
  (per-P Poisson band ±~0.3 at k≈45); per-synodic 0.0089 vs 0.0076/syn; survival curves inside
  the 95% bootstrap band at all 64 epochs, max |ΔS| = 0.062 at 488 P (the plane slightly ahead
  at late times — its 512 P misses convert to kills at later encounters, e846 checker2's 527–950 P
  conversions). Hazard 0–128 P vs 128–512 P: truth 1.61, plane 2.24 — the mixture is mild at
  μ = 1e-3 (my frozen P4 said ≥ 2; it fails narrowly at 1.61 — a single early/late split does
  not separate the ensemble here).
- **μ = 1e-2 (unrun before):** truth 32 first-entries (median 41 P, earliest 0.33 P), 39 entries,
  7 recrossers; hazard 1.5e-3/P before 128 P against 9e-5/P after — ratio 16.9, a burst then
  quiet. Per-synodic rate 0.0019/syn (1389 syn exposure) against 0.0076/syn at μ = 1e-3 (5283
  syn): **the portable rate falls 4×**. Frozen P1 (≥ 50% crossing fraction) failed: 22% against
  28% at μ = 1e-3.
- **The burst is exact (the positive control):** at μ = 1e-2, ≤ 4 P — the same 8 ICs die in the
  plane (all `planet_kick`) and enter the disk in the truth; |Δepoch| ≤ 0.014 P against the
  plane's P/64 = 0.016 P refinement grid (`work/burst.txt`, all eight rows).
- **Instrument (P5 held):** rtol 1e-12 vs 1e-13: first-entries 40 vs 38, total entries 68 vs 67,
  max |ΔS| = 0.028 — but per-IC membership agrees on 104/144 only, and both-crossing epochs
  scramble (median 178 P). The curve and the rate are certificate-grade; membership is not
  (e846 checker2's scipy result, reproduced with the shipped instrument itself).
- **Driver check (P6 held):** this tree (third machine, later HEAD, identical `crates/`+
  `xtask` code since b07f5a0b) kills exactly e846's 47 ICs with max |Δepoch| = 0.0000 P at P/64
  resolution. The engine is deterministic across trees/drivers as built; b9be's 3-IC difference
  (φ = 105°) is a difference between those two runs' code state or environment, not driver
  sensitivity.
- **The μ = 1e-2 cost wall:** median kick load per P is comparable (231 kicks/P at 4 P against
  267 kicks/P at μ = 1e-3 over 512 P — my measured `kicks` fields), but the 16 P arm did not
  finish 144 ICs in 120 s (2 workers; the 4 P arm takes ~6 s), and a 64 P attempt completed ~2
  ICs in ~6 min at 4 workers (contended host): individual ICs grind unboundedly after their
  first conjunctions (~6–11 P). 512 P would be hours: not run. Positive control of the wall:
  the 4 P arm completes and its deaths match the truth exactly (above), so the wall is a tail,
  not a rate shift.

## Predictions

`predictions.md` was frozen before the decisive runs. **P2 held** (parity ratio 1.175 ∈ [0.8,
1.4]). **P5 held** (counts ±2, curve stable, epochs scramble). **P6 held** (identical dead set
and epochs). **P1 failed decisively** — the crossing fraction falls (22% at μ = 1e-2 against
28%), and the per-synodic rate falls 4×: my Hill-thickness reasoning ignored that the same
encounter manifold that feeds crossings also ejects crossers (recrossers 16 → 7) and that the
band-unit ensemble samples different Hill fractions at the two μ. **P4 failed narrowly**
(truth hazard ratio 1.61 < 2 at μ = 1e-3; the mixture is real but mild) while its μ = 1e-2
reading was too weak — the burst there is far sharper than predicted (16.9). **P3's plane half
was unreachable** (the wall); its burst prediction — epoch-matched kills at early times — is
exactly what held.

## What would make it wrong

- The truth's entries are the judge's model of the planet (pull regularized inside a uniform
  sphere, e846's caveat): a porous or layered planet re-reads every "entry" as a conjunction
  class, not a surface event. Same domain as e846; unchanged.
- The ensemble is one μ pair at one radius and one grid (band units); the 4× rate fall is a
  property of *this* ensemble definition — that is the finding (the certificate must carry its
  ensemble), not a universal μ-law claim. A Hill-unit grid at μ = 1e-2 would sample a different
  fraction of the encounter manifold and is the natural follow-up.
- The μ = 1e-2 plane horizon is 4 P: the parity statement there is burst-only. The 512 P claim
  lives at μ = 1e-3 only.
- Wall timings on a shared cloud host: orders of magnitude only (the integrator re-measures on
  the M1). The wall's *existence* is deterministic (an IC that does not settle does not settle
  anywhere), its duration is not.
- Nothing here is adoptable engine code: the probe (`work/patch.diff` = e846's census counters +
  the `events` arm + `TROJAN_MU`) is stats-only, zero outcome bits, per e846's disposition.

## The lens

The dynamics lens framed the certificate as a birth–death process and asked for its hazard: the
answer is the deliverable — a non-homogeneous, μ-dependent, ensemble-level point process whose
per-IC identity is meaningless (104/144 across a tolerance pair) but whose curve is exact where
chaos has not acted (8/8 epochs) and count-level honest where it has (1.175). What the lens may
have missed by hunting the rate: the plane-side cost wall at μ = 1e-2 is an allocator/p99
finding that arrived as a side observation; and the recrossing structure (16 vs 7, max 7
entries) suggests the miss channel (e846's 20/97) is concentrated in the recrossing
sub-population, which the first-event statistic deliberately censors — the certificate may want
a second, recrossing-aware arm before freeze.

## Grade

Silver, self-assessed: real, reproduced on shipped code, held-out predictions half-held with the
misses reported, and it builds e846's named successor statistic end to end at the control μ —
but the negative control (a deliberately skipping law must fail the certificate) is not yet run,
and the μ = 1e-2 side is burst-only behind the cost wall. Both are one run each.
