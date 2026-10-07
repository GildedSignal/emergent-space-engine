# Predictions — run 20261007-2057-taleb-efc9

Written before the decisive grid. Not tuned on any sw*/bimodal/debris scene.
(Controls and sampling-convergence were checked: ctl-ring gives k*=3, miss4=0;
encounter counts identical at T=8192/16384/32768.)

Question: the phase-neighbour certificate (circular rank k in mean anomaly,
O(n·k)) is being built on the gold's claim "every encounter lies within partner
rank 4 along the orbit", measured on formations. What co-orbital workload
breaks it, and does the pairwise tier catch the survivors at affordable cost?

Setup: n=384 bodies, all a=1 (co-orbital; σ_a=0 so M-rank is frozen in time and
one period of dense sampling is a complete truth), R_enc = 0.005 a, T=8192
samples/orbit (≥4 samples per crossing at e≤0.6, verified). k* = max circular
M-rank over real encounter pairs. miss4 = fraction of encounter pairs with
rank > 4 (the gold's rank).

## Predictions

1. **Controls (ctl-ring-circ, ctl-arc, ctl-ring-e03-aligned): k* ≤ 4, miss4 = 0.**
   If this fails the instrument is broken → VOID.
2. **Aligned, e-dispersed (se002…se03): miss4 = 0 up to σ_e = 0.05. At σ_e ≥ 0.1
   misses appear (radial crossings of bodies at large anomaly separation) but
   k* stays ≤ 16.** Medium confidence.
3. **Apsidal dispersion at e=0.3: miss4 grows with σ_ω; at uniform ω, k* ≥ 48
   (n/8) — the certificate is dead, not merely widen-able — and miss4 > 30%.**
   High confidence. Mechanism: misaligned apsides meet at matched radius at
   anomalies far apart in M.
4. **Uniform-ω scales with e: miss4(e=0.1) > 5%, rising to e=0.6.** The failure
   needs a·e·Δω ≳ R_enc; even e=0.1 gives 0.1·1 rad ≫ 0.005. High confidence.
5. **Node dispersion (Ω uniform, i=15°, ω aligned): k* ≤ 16, miss4 < 10%.**
   Encounters confined to node crossings at matched anomaly → still phase-local.
   Medium confidence.
6. **Bimodal apsides (two sub-fleets, ω ∈ {0, π}): cross-fleet encounters need
   anomalies differing by ~π → k* ≈ n/2, miss4 ≈ fraction of encounters that
   are cross-fleet (> 50%).** High confidence.
7. **Debris ring (collision cloud: e∈[0.05,0.6], ω,Ω uniform, σ_i=10°):
   k* ≥ 48 and miss4 > 40%.** The physically-expected workload of a collision
   in the game kills the rank certificate. High confidence.
8. **Every same-a scene has shell-overlap setup ≈ n(n−1)/2 (≥ 95% of pairs):
   the miss-free pairwise tier has no sub-quadratic fallback at fixed a.**
   So if 3/6/7 hold, the two tiers leave a no-man's-land: concentrated enough
   that pairwise setup is unaffordable, phase-disordered enough that rank-k
   misses (silent lost encounters = corrupted canonical history, a ruin state).

## Kill criteria (decided before the run)

- The fragility claim is **killed** if every scene has k* ≤ 4 (cert generalizes
  beyond formations; report the envelope as the result).
- The **no-man's-land** (design hole) is confirmed if some scene has k* ≥ 16
  AND setup_shell/n_enc ≥ 100: neither tier serves it.
- If k* explodes but n_enc is so large that n·k/n_enc stays ≤ 10, the phase
  tier is still affordable by widening k — then the finding downgrades to
  "the rank must be sized by the group's apsidal dispersion, not fixed at 4".

## What the numbers must not do

- n_enc must be > 20 in every sw*/debris scene (else the miss fractions are
  noise; rerun with more bodies or larger R if not).
