# Dossier — run 20261007-1550-dynamics-71a5 (lens: dynamics and attractors)

**Claim (one sentence).** The encounters certificate's premise — a pair's section is an
"exact integer circle rotation ... a certificate valid until a kick" (docs/law.md;
`crates/encounters` models fixed `pom`) — has a finite horizon under the law's own compiled
apsidal precession: equal precession ages nothing (a rigid rotation, measured exact), but
differential precession Δϖ̇ carries the pair's relative Binet angle to its next orbit-tangency
in t_tang = (angular distance to that tangency)/Δϖ̇, where the standing "never" certificate
dies (measured: 12/12 runs, every realized encounter lands after its tangency, none before)
and the active schedule decorrelates (measured: 27/27 proposals wasted at the highest rate) —
so sections must live in the pair's co-precessing frame (an O(1) angle update per pair from
the tubes' exact Δφ per cycle), which matters exactly in the strong field (≈ 40–400 orbits at
p ≈ 50 M for generic belt pairs; 4×10⁸ orbits in the weak-field scene, irrelevant there).

- **Bottleneck.** Board focus "finding encounters without work per orbit or per element
  change" and the top scaling risk (candidate work must track real encounters). The horizon
  bounds how long a standing certificate can stand — the forced per-pair setup rate the tier
  pays even when kicks never touch the pair.
- **Novelty.** No history entry couples precession to the encounter certificate (checked
  docs/HISTORY.md and law.md's encounters paragraph; r8 v2/v3, q-candidate-degree and
  components-4643 judge algorithms and setup cost, all on fixed elements).

## Evidence

Model: each body a uniformly precessing conic — the tube's float form (radial cycle exact,
apsidal advance per orbit; Δϖ(t) = Δϖ₀ + Δϖ̇·t exactly, so the drift studied is deterministic,
never noise). Truth: brute-force refined distance minima (grid 2²¹–2²², golden refinement).
Certificate: the pair frozen at t = 0, as `crates/encounters` builds sections; proposal =
frozen local minimum < 1.2ρ; MISS = true minimum < ρ with no proposal within 0.4 synodic
spacings. ρ = 4×10⁻³ (of a ≈ 1). Geometries: G6 crossing (cone gap −0.001), G4n non-crossing
near-tangent (gap +0.0089, m0 = 0.0069 > ρ), G2 transversal crossing (gap −0.138).
Machine state inside `work/results2.json`. Files: `work/cert.py`, `work/cert2.py`,
`work/results2.json`, `work/results3.json`, `work/run1.log`.

1. **Controls (prediction 1 held, both sides).** G6 and G4n, pure Kepler and absolute-equal
   precession Ω = 0.05 rad/time (0.31 rad/orbit) on both bodies: 0 misses, 0 waste, and
   m0_true equal to the frozen value to 6 digits (G6: 0.000083; G4n: 0.006934). Rigidly
   precessing the pair changes nothing the certificate predicts. (Run 1's coprec control said
   "0.3 per orbit" on both bodies — unequal rates for unequal periods, i.e. a differential
   case; it produced misses, consistent with the mechanism. Lesson recorded in `work/run1.log`.)
2. **The "never" certificate dies at the next tangency (prediction 3's law, corrected and
   confirmed).** For G4n the orbits become tangent at |Δϖ*| = 0.7268 rad (R(Δϖ*) = ΔU, the
   Binet cone's boundary). With body j precessing away from the near tangency (Δϖ₀ = 0.70,
   travel distance 1.427 rad), tangency is reached at t = 1.427/Δϖ̇. Brute force, 3 rates ×
   4 conjunction phases (`results3.json`): tangency at 2854 (Δϖ̇=5×10⁻⁴), 1427 (1×10⁻³),
   713.6 (2×10⁻³) — halving exactly with the rate — and all 7 realized sub-ρ encounters fall
   AFTER their tangency (by 4–2145; the near-tangency wide-arc phase makes realization quick
   for some phases, lucky for others), zero before, over 12 runs spanning 3 rates. The
   certificate says "never"; geometry says encounters from t_tang on.
3. **Active sections: the schedule decorrelates, then misses.** Ensemble of 12 conjunction
   phases on G6 at 5 rates (`results2.json` `A2_G6`): waste grows 9 → 21 → 25 → 27 → 27 of
   27 proposals — by Δϖ̇·T ≳ 0.5 rad every proposal points at a passage where no true
   encounter occurs — and the first missed true encounter appears at Δϖ̇ = 10⁻³
   (6×10⁻⁴ rad/orbit, well below strong-field belt values). Run 1's single-pair G2 sweep
   already showed misses at every rate ≥ 3×10⁻⁵ rad/time but its first-miss time was
   conjunction-luck-dominated (slope 0.45, nonmonotone) — the ensemble is the honest instrument.
4. **Mechanism constants.** Level drift under rigid relative rotation: dm0/dΔϖ = −0.109 (G2),
   −0.090 (G6) — the miss level moves by ~0.1 orbital radii per radian of relative Binet
   rotation. Cone-gap rate for near-tangent pairs: dR/dΔϖ ≈ 0.33 (G4n). The per-conjunction
   |Δd| vs t exponent could not be resolved (≤ 6 matched minima per run — the series is too
   sparse; prediction 2's t-exponent is untested, though the model's linearity in t is exact
   by construction).
5. **Engine translation (prediction 5 held, stronger).** Schwarzschild δ = 6πM/p per orbit;
   belt of width Δp/p gives Δϖ̇ ≈ δ·Δp/p. At p ≈ 50 M (δ = 0.38 rad/orbit; B17's original
   scene's regime): generic pair horizon = travel-to-tangency (uniform in ~[0, π], typical
   ~1.5 rad)/Δϖ̇ ≈ **40 orbits (Δp/p = 10%) to 400 (1%)**; near-tangent pairs arbitrarily
   sooner (0.027 rad ⇒ < 1 orbit). At the weak-field B12–B14 scene (p = 5.27×10⁸ M):
   Δϖ̇ ≈ 3.6×10⁻⁹ ⇒ **~4×10⁸ orbits** — irrelevant. The strong field is where the law is
   native; there, every standing certificate re-sets on orbit timescales.

## Predictions (predictions.md, written before the decisive run)

Held: 1 (both controls exact), 5 (strong field ≪ 10³ orbits — 40–400; weak field ≫ 10⁶).
Failed as written: 3 — first, my analytic t_cross = 0.027/Δϖ̇ assumed travel toward the NEAR
tangency while the run traveled the far one (the zone is symmetric in Δϖ); the corrected law
t_tang = (path distance to tangency)/Δϖ̇ is confirmed by the exact halving across rates.
Second, H = time of first MISS conflated the certificate's *safety* (wrong from t_tang,
scales exactly as 1/Δϖ̇) with *realization* (a conjunction must land in the moved arc: a
waiting time set by geometry, not by Δϖ̇). Prediction 2's t-exponent: unresolvable with this
instrument (too few matched minima); the rate-proportionality is carried by construction.
Prediction 4 (resonance shelf): not run — time; the shelf modifies realization waiting (l*),
not t_tang, so the safety statement stands without it.

## What would make it wrong

The truth model is a uniformly precessing conic, not integrated GR — but that is exactly the
tube's compiled form (radial cycle exact, uniform apsidal advance per cycle), so the
certificate is being tested against the design's own dynamics, not a proxy. Wrong if: (a) the
kick cadence re-sets elements so often that precession is shadowed — orbit-averaged kicks act
once per orbit, the same order as the 40–400-orbit horizon at 50 M, so it is NOT shadowed
there; (b) encounters never run in dolls with δ ≳ 10⁻² rad/orbit (a scope decision, not
physics); (c) tangency travel is bounded because real Δϖ̇ keeps one sign per pair and
|Δϖ| saturates — no, GR precession is monotone, so every pair cycles through both tangencies
every π rad of relative Binet rotation.

## Cost of adopting, and fit with PRINCIPLES

Adopt: parameterize each pair's sections by Δϖ(t) tracked exactly from the two tubes' Δφ per
cycle (integer adds) — i.e. cut sections in the **co-precessing frame**, where the offset
rotation stays an exact integer circle rotation and U, V·cosΔϖ, V·sinΔϖ geometry rides the
rotation. Cost: one angle add per pair per cycle boundary; a window rebuild only when the
differential rotation since the last rebuild exceeds the arc width (every H orbits); no
per-orbit window-setup re-evaluation — which matters because window setup is 92% of per-kick
evals (components-4643, 6 October). Principle 32 ("under the right representation many
symmetries can appear"): the co-precessing frame restores the symmetry the inertial frame
loses. Principle 13: the aging error is not compounding, but it is unbounded and silent —
exactly the type a certificate must bound. The re-setup rate this forces at p ≈  50 M is
~1/(40–400) per pair per orbit — the tier's "no work per orbit" becomes "no work per orbit
in the weak field; O(1) angle updates in the strong field."

## The lens may have made me miss

Two bodies only: the aggregate tier cost (re-setup rate × candidate count) is derived, not
simulated. The resonance shelf (prediction 4), mutually perturbing pairs (encounters that
kick elements mid-drift), retrograde/inclined cases, and e > 0.7 are untested. The
realization-waiting statistics after tangency are consistent with wide-arc phasing but were
not fitted. A rung would need the co-precessing section implemented in `crates/encounters`
and judged against the brute-force truth used here.

## Reproduce (Linux/x86, orders of magnitude only; each command's wall time noted)

    cd lab/results/20261007-1550-dynamics-71a5/work
    python3 cert2.py    # controls, A2 ensemble, B2, drift, mechanism constants (~3.7 min)
    python3 cert.py     # run 1: malformed-control lesson + single-pair A sweep (~1 min, known crash at end)
    python3 - <<'EOF'   # B2 realization: 3 rates x 4 phases (~50 s)
    from cert import *
    nn = lambda a: a**-1.5
    G4n = (body(1.0,0.30,0.3,nn(1.0)), body(0.8,0.30,1.00,nn(0.8)))
    for om in (5e-4, 1e-3, 2e-3):
        for k in range(4):
            bj = dict(G4n[1], Om=-om, M0=k*TAU/4)
            print(om, k, first_below(pair_minima(G4n[0], bj, 3000.0, 1<<22, 0.05), 0.004))
    EOF
