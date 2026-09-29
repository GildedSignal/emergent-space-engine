# Dossier — rung r4 (run 20260929-1940-rung-r4-resonance-3530)

**Claim.** The design's conjunction-kick event layer, implemented as an exact-Kepler
map with a closed-form multipole tidal impulse at each conjunction, over-pumps
eccentricity by 3–11x and crosses the perturber's orbit: `conj-quad` and
`conj-oct` are KILLED on the rung's pump criteria. The layer is genuinely cheap
(0 dense steps, ~0.4–0.6 kicks per orbit) and the phase-dependent kick does
drive eccentricity (a `none` control cannot), but the impulse approximation is
quantitatively wrong at the 2:1's conjunction distance.

**Bottleneck.** Board #2 (stepping owned by cells, or no stepping): the live path
is "analytic generators + multipole kicks" (H0190). This rung measures whether
the kick layer carries resonance. Verdict: it kills this *formulation* of the
kick (straight-line-approximated, full-synodic-window impulse), not the method.

**Scene** (frozen before any law run; the red-team's `e1_resonance.py` is not in
this checkout). Pumped test body exterior at exact P1/P2 = 2 (a1 = 2^{2/3}
units), interior perturber m2/m0 = 3e-3 on a circular orbit (a2 = 1), e1_0 =
0.05, lambda2(0) = pi + w2, 200 synodic periods. Controls at P = 5.0, 2.55,
2.15. Truth: barycentric velocity-Verlet float64, converged over 600/1200/2400
steps per orbit (max-e changes < 0.5% from 1200 to 2400; energy drift < 1e-2).
Truth behaviour: e1 pumps to 0.081 (r21) and 0.183 (r21b) and the controls stay
at ~0.073; the resonant angle 2*lam1 - lam2 - w1 circulates in truth (C = 0.07),
i.e. no libration anywhere in the grids I searched (interior-body 2:1 ejects at
this mass ratio; exterior 2:1 pumps but does not librate for ~450 scenes tried
in `predictions.md`'s search). The red-team anchor "libration concentration
0.867" was therefore not reproducible from the rung text alone — reported as a
gap, not papered over; the lib criterion then compares circulation vs
circulation and cannot discriminate here.

**Evidence** (`gcc -O2 -o r4 r4.c -lm && ./r4`, 15 s, 4 vCPU container, load 0.4,
16 GB RAM 5% used; `--selftest` validates the closed-form kick against a
trapezoid of the same analytic integrand to 1.8e-9):

| config | e_pump_ratio_min | e_pump_ratio_max | lib_ratio_min | ctrl_pass | dense_steps | kicks/orbit |
|---|---|---|---|---|---|---|
| conj-quad | 5.65 | 10.94 | 0.19 | 0.0 | 0 | 0.41 |
| conj-oct | 2.63 | 6.05 | 1.41 | 0.0 | 0 | 0.41 |
| averaged (neg) | 0.73 | 4.68 | 0.07 | 0.33 | 0 | 0.41 |
| none (neg) | 0.28 | 0.64 | 0.05 | 0.0 | 0 | 0 |

`lab/verdict.py lab/rungs/r4-resonance.md metrics.json` → **KILL** (conj-quad
fails pumphi, lib, ctrl; conj-oct fails pumphi, ctrl; both negatives fail as
required). Numbers in `metrics.json`, series in `data/*.csv`, picture in
`picture.svg` (e1(t) law-vs-truth per case + resonant-angle histograms).

**Predictions** (`predictions.md`, written before the decisive run): I predicted
pump ratios 0.5–1.3 for conj-quad and that octupole would move conj-oct closer
to truth. Wrong in magnitude — the over-pump is 6–11x (quad) and 3–6x (oct) —
but right in direction (oct halves the error) and right that both negatives fail
pump. The miss: I underestimated how badly integrating the linearized encounter
over the whole synodic window overcounts an encounter whose width is ~half the
synodic period itself at alpha = 0.63.

**What would make it wrong.** The scene is mine, not the red-team's: at their
(librating, C = 0.867) scene the pump ratios could differ, though the mechanism
of failure (impulse over-counting at wide conjunctions) is scene-independent —
the controls far from resonance fail by 8–35x too, and no phase tuning can fix a
3x-too-strong kernel. Cost of adoption: none (killed). The l<=1 terms of the
interior perturber (monopole breathing, dipole+indirect residual) were assigned
to the averaged layer, not the kick; including them would add phase-free
frequency drift, not fix the over-pump.

**Fit with PRINCIPLES.** "A failed experiment kills that configuration, never
the method" (#9): the killed configuration is the straight-line full-window
impulse; the surviving question is a windowed or curvature-corrected kernel
whose encounter width is the conjunction zone, not the synodic period — one
rung away. "Compute only surprises" and "no ticks" survived: ~200 events for
200 orbits against 10^5–10^6 truth steps is a 500x cost result even as the
behaviour fails. Errors here do not compound in the certificate sense — they
are a wrong-strength kernel, an error of model, not of drift.

**The lens** (directed rung, no lens choice): a falsification bias made me spend
the scene-search budget proving the red-team's libration anchor was not cheaply
reproducible rather than widening the kernel variants; a second configuration
(windowed impulse) would have been the higher-information experiment.
