# Dossier — 20261012-1117-redteam-4808 (premise red-team)

**Claim.** The design's kick layer — "a kick updates the cycle by a multiply-add" (docs/representation.md §3) — carries a one-signed truncation error whose gain diverges at the GR plunge separatrix (zoom-whirl orbits), which no rung tests; the Binet band representation and the flat-space light-cone gather, this red-team's other two targets, **survive** their held-out corners (e → 0.99: 0.008% precession error; β → 0.995: exactly one crossing).

**Bottleneck.** Board focus line 2/4 (the changeover, encounters → motion law v2) and the law's error model (§2, "one error budget"). Expected gain: not a speedup but the closing of a behaviour hole: post-encounter bodies near any black hole land just above the critical curve p_crit ≈ 6+2e, exactly where the multiply-add's phase error per kick diverges. It deletes nothing yet; it names the missing criterion.

## Ranked attacks

1. **Kicks near the plunge separatrix (premise 3) — MEASURED, no rung catches it.**
   The cycle's phase advance Δφ(L) is convex in L: every kick, either sign, leaves the same-sign residual (systematic drift, the exact thing "errors never compound" (P13) forbids). As p → p_crit⁺ (e = 0.9), for δL/L = 10⁻⁴:
   | p | Δφ/cycle | gain = |∂Δφ/∂L|·L/Δφ | residual (rad/kick, both signs) |
   |---|---|---|---|
   | 10 | 10.36 | 1.7 | +9.6e−7 |
   | 8.2 | 14.77 | 5.4 | +1.1e−5 |
   | 8.05 | 16.10 | 7.6 | +2.5e−5 |
   | 8.01 | 16.60 | 8.6 | +3.4e−5 |
   Diverging gain, one-signed error growing 36× from p=10 to p=8.01; at one kick per orbit, 3.4e−5 rad/orbit is 0.34 rad of apsidal drift after 10⁴ orbits — a player-visible wrong orbit near a black hole, where navigation "must be perfect" (P30). Encounters scatter bodies to just above p_crit (that is what a near-capture scatter is), so the regime is not exotic; it is the normal output of a battle near a mass.
   **Rung that should catch it: none.** r1 has no kicks; r4's kicks sit at e₀ = 0.02 resonance; r9's tides at e₀ ≤ 0.3, far from p_crit; B9 at e ≤ 0.99 measures cost (crossings), not kicked phase. Missing criterion (B12-style): a kick train at fixed δL/L on orbits with p → p_crit⁺, judging accumulated apsidal phase drift per 10³ orbits against the one-floor-unit budget.
2. **Binet band stitching at e > 0.7 (premise 2) — SURVIVES.** r1 sampled e ≤ 0.7; held-out to e = 0.99 at p = 13: precession error 0.008–0.013%, *better* than at e = 0.5 (0.024%, p = 10). Error grows only toward the critical curve (0.32% at p = 7.95) — still ≪ the 1% bar. **Caveat for the record:** these numbers come from the band model integrated as a piecewise-constant-coefficient ODE. My first implementation (exact in-band rotations with edge-event solving, the form the integer machine would actually take) produced a *systematic 12–14% cycle error that did not shrink with m* — the instrument bug: a body stepping exactly onto a shared band edge is re-assigned to the band it just left, whose oscillator then turns spuriously (periapsis 0.121 instead of 0.150). `falsifier.py` documents it. An exact-event implementation must reproduce the ODE numbers before r1's PASS is trusted on the machine path; that is one cheap r1 addendum (same criteria, event-stepped variant), no new criterion.
3. **The view gathered at the past light cone (premise 5) — SURVIVES in flat spacetime.** f(t_e) = t_obs − t_e − |x_e − x_o| has df/dt_e = −1 − n̂·v_e ∈ (−2, 0) strictly for |v| < c: exactly one crossing per gather, verified numerically at β = 0.995 with an orbiting emitter (roots 1 per gather; the 0s are window truncation). My prediction of multiple roots was wrong. Multiple images need lensing, which the design already routes through deflection(b). Residual untested risk: the Newton *seed* under k ≈ 20 time compression — r6 does not exist.
4. **Dense/sparse bit-identity (premise 4) — UNTESTED GAP.** r5 does not exist in lab/rungs/. No falsifier run here (time); flagged as the oldest untested load-bearing premise on the ladder.
5. **"Undisturbed orbits ≈ 0" (premise 6) — already contradicted by the record.** The 5 October correction: on distinct kicks the exact cycle memo hits 0%, and the plane recompiles on ~99% of kicks. §6's table row is optimistic against the plane's own measurements; cite, don't rerun.

## Evidence

All numbers: `python3 falsifier2.py` (≈ 8 s, float64, scipy; this machine). Exact GR oracle cross-checked against an independent fixed-step RK4 (agreement to 7 digits: Δφ = 10.055167 vs 10.055168 at p=10, e=0.5 — the 6π/p formula is only the weak-field term there, the exact advance is 3.77 rad/cycle). Files: `falsifier2.py` (decisive), `falsifier.py` (broken instrument, kept as documentation), `predictions.md`.

## Predictions (scorecard)

Written before the decisive run. **P1 wrong**: band stitching holds to e = 0.99 at 0.01%, no cliff in [0.9, 0.98]. **P2 half right**: the error is systematic and the gain diverges — but at the *plunge* separatrix (p → p_crit), not the Newtonian/comet one (measured gain ≈ 1.5 there; the Kepler T∝E^{−3/2} degeneracy caps it), so my g ≥ 10⁴ at e = 0.99 was wrong. **P3 wrong**: one root, not two. Two of three attacks failed in the design's favour — the design is more robust on these corners than this red-team expected.

## What would make it wrong

The multiply-add attack weakens if kicks near p_crit are rarer than I claim (capture scatters may overshoot to plunge or bounce well above p_crit — a rate measurement, not a proof); or if the motion law v2 re-derives the cycle exactly at each kick near the separatrix (cost, not correctness). The B numbers depend on δL/L = 10⁻⁴; the residual scales as δL², so smaller kicks shrink it quadratically — but the sign stays, so it compounds at any kick size given enough orbits.

**Cost of adoption:** one rung criterion (kick train at p → p_crit⁺, apsidal-drift budget) plus the law's rule for when a kick must re-derive the cycle instead of multiply-adding it. No new component.

**PRINCIPLES fit:** "basically we don't want errors that can compound that's the goal" (P13) — the measured residual is one-signed per kick. "A failed expectation is not automatically a failed method" (H0183): the multiply-add is not killed; its domain is.

**Lens blind spot:** premise red-teams overweight exotic corners — I spent the run's physics budget near black holes; the plain belt's regime (weak field, low e) may hide duller, likelier failures (e.g. the r5 gap). Two of my three held-out predictions broke *for* the design, which suggests the lens also underweights how much of the representation's strength is already real.

## Grade suggestion

Silver: the attack is measured and reproduced by an 8-second script, but the fix's trigger (how often encounters park bodies at p_crit⁺) is one named experiment away — the next run's pick.
