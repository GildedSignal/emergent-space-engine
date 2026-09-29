# check2 — second checker, blind to the first

## Abstract (for the integrator)

Reproduction is bit-exact: `truth_summary.txt`, `metrics.json`, the machinery checks and wall times all match. My independent RK4 truth (from scratch, different scheme, 2400 and 4800 steps/orbit) confirms every oracle value: maxe1 within 0.03%, conc to the fourth decimal, all five cases. **But the kick layer's tidal field is sign-inverted**: the code implements (m₂/R³)(r − 3(r·ĥ)ĥ), the negative of the Newtonian quadrupole (octupole likewise). The exact impulse at R1's first conjunction is +1.89e-2; the code's is −1.41e-2. With the corrected sign, both candidates are **killed** by the frozen gates (pumphi 1.51–1.56, C3 ctrl 0.44–0.45) — and the corrected layer then reproduces what the author's misses (C3 phase-lock conc 0.85 vs truth 0.87; R1 libration centre 176° vs truth 157°, author's 355°). The reported PASS rests on magnitude-only gates that cannot see a π-shifted libration centre. R2's reconstruction also never reaches the rung's frozen truth conc 0.867 (0.514). Do not adopt on this evidence.

## What I did

Clean copy of the run folder in `/tmp/check2`; `gcc -O2` build; `rung_r4.py truth|check|metrics` — every number identical (`diff` clean, both directions). `verdict.py` on my reproduced file: PASS (candidates pass; negatives fail pump,ctrl), same as the author's claim. `patch.diff` is empty and the repo tree is clean, so the run folder is self-contained.

## The sign inversion (the finding that matters)

`rung_r4.py` line 116: `ax = c * (x - 3.0 * dot * hx)` with `c = M2/R³`, `dot = r·ĥ`. The Newtonian tidal field is `+(3(r·ĥ)ĥ − r)·m₂/R³` (stretches along the perturber line); the code is its exact negative, and the octupole branch (lines 117–120) is negated with it — equivalent to m₂ < 0. Four independent confirmations:

1. **Series expansion** of `(R−r)/|R−r|³ − R/R³` to O((r/R)³): the code is minus the standard l=2 and l=3 terms (magnitudes correct).
2. **Exact impulse at R1's first conjunction**, GL48 over the same synodic window and Kepler arcs: exact +1.8896e-2 (toward the perturber), author's l=2 −1.4066e-2, negated +1.4066e-2 (residual to exact 4.8e-3, the expected l≥4 truncation at a₁/a₂ = 0.63).
3. **Generic asymmetric points**: dot(exact, code) < 0 at every probe.
4. **Behavioural**: the author's own dossier laments the controls' missing phase-locking — the corrected sign delivers it (C3: conc 0.849/0.808 vs truth 0.874, author's 0.19/0.21; libration centre 1.2° vs truth 9.4°, author's 181°), and moves R1's centre from 355° to 176° against truth's 157°.

## Consequence for the frozen gates

Corrected-sign candidates through the same `write_metrics` path (`conj-quad`: pump 1.316/1.557, lib 0.850, ctrl 0.667, kpo 0.575; `conj-oct`: 1.411/1.508, 1.468, 0.667, 0.562) → `verdict.py`: **KILL; killed: conj-quad, conj-oct** (both fail pumphi and ctrl — C3 envelope 0.45×/0.44×). The author's PASS survives only because maxe1 and |⟨e^{iψ}⟩| are nearly invariant under field negation: the quadrupole (even-harmonic) resonance mirrors about ψ → ψ+π, keeping magnitudes while inverting the physics. The layer as shipped models the *repulsive* tidal field and still passes — that is a property of the gates, not of the layer.

## Other checks

- **Oracle**: my RK4 (own element extraction; my first version had its own ν-sign bug and a meaningless dE — both mine, fixed, and worth recording because they show how easily this class of bug slips in). Note the author's `dE` diagnostic omits all test-particle terms (m₁ = 0), so it only monitors the star–perturber pair; harmless here because 600/1200/2400 convergence and my cross-check cover the trajectories.
- **R2 fidelity**: the rung freezes "truth conc 0.867". I tried three readings of "w2 = 4.0": (e₂=.05, ϖ₂=4) → 0.514 (author's), (λ₂(0)=4, circular) → 0.199, (λ₂=4, e₂=.05) → 0.311. None reaches 0.867; the red-team's ICs are simply not in this container. Ratios are internally consistent (own truth), but the frozen case is not the one the rung names.
- **Adversarial cases** (conj-oct, my RK4 truth): period ratio 2.05 — truth maxe 0.1015, author's layer 1.80×, corrected 2.67×; μ = 1e-2 at 2:1 — truth 0.2275, author's 1.64×, corrected 2.02×. The layer's envelope accuracy is narrow around the frozen nominal points, in either sign.
- **Spec conformance otherwise**: exact Kepler cycles, one conjunction-anchored analytic kick (24-node Gauss–Legendre of the analytic truncated field over a tiling synodic window — quadrature, not stepping; `dense_steps = 0` honest, and the author flags the letter himself), ≥ 200 synodic periods, converged truth, metrics as frozen, `kicks_per_orbit` ≈ 0.53–0.58, walls < 1.2 s per config.
- **Predictions**: existed before the metric runs (file order and timestamps consistent); negatives and costs held; the conj-quad over-pump prediction (1.4–2.2×) in fact matches the *corrected*-sign result (1.32–1.56×) — the surprise the author reported came from the sign error, not from the truncation he blamed.
- **Novelty**: the rung is the red-team's named experiment (taste log, 29 Sept); `averaged` is H0190 K2. No prior H-entry measures resonance on the kick layer.

## Recommendation

`verdict.py` says PASS on my reproduced numbers, but the candidates do not implement the physics the rung specifies — they implement its negative, and the physical version is killed by the same gates. Treat the PASS as void of adoption value: rerun r4 with the corrected sign (expected KILL at these gates), freeze a phase-sensitive criterion with an upper bound (the author's own "what would make it wrong" asks for exactly this), and put the red-team's actual ICs into the R2 case before it counts.
