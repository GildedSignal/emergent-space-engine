# Predictions (written before the decisive runs)

Model: conjunction map of a coplanar belt (exact Kepler drift about one dominant mass; impulses
2Gm/(v_rel·d) at conjunctions; the law's own drift+kick structure, Newtonian regime where the
Binet cone applies). Parameters frozen after one calibration run (fix body mass m so a typical
kick changes e by ~σ_e/4); the decisive runs then use frozen parameters on cases not tuned on.

## Held-out claims (not tuned on; decisive run judges these)

- **H1 (relaxation).** The per-body kick rate does NOT decay to 0 in the elastic regime; it
  relaxes from its geometric initial value to a steady floor of the same order (within 3×) over
  ~10² orbits, because elastic scattering conserves energy and the crossing set keeps being
  repopulated by stirring. If instead the rate decays → 0 (elements freeze), the design's
  "no work per orbit in the steady state" is CONFIRMED and my expectation killed.
- **H2 (the re-setup floor).** Above-quantum element changes per body per orbit at the law's
  own m=16 band grid (Δu/u = ln2/16 ≈ 4.3%) are ≥ 0.1 per body per orbit, i.e. the pair
  re-setup work per orbit (crossing rate × candidate degree) is within one order of magnitude
  of the real-encounter rate (r8 measured 1.1 events/body/orbit), not → 0.
- **H3 (burstiness).** The arrival process is over-dispersed but short-memory: Allan factor
  plateaus below 2 (no avalanche criticality elastically); branching-ratio proxy < 0.3.
  Controls: a synthetic Poisson series gives Allan ≈ 1; a synthetic supercritical Hawkes
  process gives Allan growing with window (estimator validated both sides).
- **H4 (fragmentation criticality).** With contacts replacing bodies by K fragments, there is
  a critical K×(areal crowding) where the contact-rate growth exponent crosses 0: K=0 decays
  (negative control), K ≥ 2 at crowding ≥ ~10 bodies per b_max slot grows (positive control).
  The transition is sharp (crosses within a factor ≤ 2 in density or one unit of K).

## Calibration (allowed before freezing)

One short run fixes m (target: median per-kick |Δe| ≈ σ_e/4) and the horizon (target: ≥ 100
encounters per body total). No claim is read off calibration runs.

## Frozen after calibration (30-orbit N=512 probe, mass 1e-8: 0 ejections, |E drift| 2e-5)

- Body mass m = 5e-8 (median kick dv 3.6e-4 at 1e-8 -> ~1.8e-3, i.e. de ~ sigma_e/4 per kick).
- Elastic decisive runs: N=768, 240 orbits, seeds 1,2,3 (sigma_e=0.02, a in [1,1.4], bmax=2 mutual Hill).
- Density scaling run: N=1536 seed 1, 120 orbits (same geometry, 2x density).
- Fragmentation sweep: mass 1e-8, N in {512,1024,2048} x K in {0,1,2,3}, seed 1, 120 orbits, frag-dv 3e-3.
- Estimator controls: Poisson -> Allan ~ 1 (measured 0.86-1.10); supercritical Hawkes (m=1.5) -> Allan
  ~ 1e4 growing with window (measured). Both sides behave.
