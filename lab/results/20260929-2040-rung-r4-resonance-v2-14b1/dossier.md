# Rung r4 v2 — arc-integrated kicks: KILL of arc-g8, arc-g16 and arc-g8-half

## Claim

First-order Gauss–Picard kicks integrated along the frozen arc between conjunctions do **not** reproduce mean-motion-resonance behaviour at m2/M = 3e-3: every candidate fails the pump band, the libration ratio, or the controls, and most runs die at the divergence guard long before the 200 synodic periods end.

## Bottleneck

Board #2 (stepping owned by cells, or no stepping) and #1 (what cells add). The event layer this rung tests is the design's cheap replacement for dense integration near resonance (H0190's kick layer). Expected gain if it had worked: 2400 dense steps per orbit → 0.65 kicks per orbit, about 3 orders of magnitude. What the kill deletes: the premise that a *first-order* windowed map can carry the resonant pump at this mass ratio; the pump is second-order feedback (the arc must feel its own drift within the window), so the event layer needs either second-order window information or sub-orbit windows.

## Evidence

Verdict (mechanical, `lab/verdict.py` with author metrics):

```
Verdict: KILL; no candidate passed every criterion; killed: arc-g8, arc-g16, arc-g8-half
arc-g8      candidate fail pumphi,lib,ctrl
arc-g16     candidate fail pumphi,lib,ctrl
arc-g8-half candidate fail lib,ctrl
truth-1200  positive pass
averaged    negative fail pumphi,ctrl
none        negative fail pump,ctrl
```

Key numbers (truth-2400 is the reference; full grid in `work/data/summary.jsonl`, per-case in `work/data/detail.json`):

| config | pump ratio (2 cases) | lib ratio min | controls | kicks/orbit | completed? |
|---|---|---|---|---|---|
| truth-1200 | 1.0000–1.0000 | 1.34 | 3/3 | 0 | yes |
| arc-g8 | 1.267–1.304 | 0.225 | 2/3 | 0.058 (nominal) | no: guard at 19 syn |
| arc-g16 | 1.287–1.320 | 0.183 | 2/3 | 0.059 | no: guard at 19 syn |
| arc-g8-half | 1.133–1.154 | 0.681 | 2/3 | 0.100 | no: guard at 18 syn |
| averaged | 3.27–6.70 | 1.90 | 2/3 | 0.653 | no: guard (e→0.95) |
| none | 0.058–0.071 | 2.91 | 2/3 | 0 | yes |

`dense_steps` = 0 for all law configs by construction: the arc is never integrated; quadrature nodes per window are 8 (arc-g8, arc-g8-half), 16 (arc-g16), 64 (averaged). `kicks_per_orbit` is the median over the five cases of window-ends divided by the *nominal* run length; for runs that died at the guard the true rate over their lived time is ~0.6–0.7 per orbit for arc-g8 (resync micro-windows after each kick add windows, not cost). The guard deaths are part of the result: max_e for a dead run is the maximum over its lifetime, not over 200 synodic periods.

Mechanism, isolated in one window (all in `work/r4v2.c`, `KICKDUMP=1`):

1. Over the **full synodic window at exact 2:1 with the conjunction-aligned start, the element-space first-order kick is identically zero in a and e** (|Δe| < 1.5e-17): the unperturbed arc closes the resonant configuration, so the first-order integral cannot see the pump at all. The truth gains Δe ≈ +0.02 in that same window. The pumping lives entirely in the second-order feedback (the arc drifts along-track by ~0.17 rad per window, which re-tunes the torque).
2. What the first-order integral *does* return per window is an O(1)–O(10) rotation of varpi_1 (Δϖ ≈ −2.7 rad on window 1 of res-2to1; −15.4 rad on a later window of ctrl-r2.15), which scrambles the resonant angle φ = 2λ2 − λ1 − ϖ1 from window to window; hence lib ratios 0.18–0.68.
3. The kick is not small compared with the state: on ctrl-r2.55 the first window returns Δe = −1.08e-2 against e1(0) = 0.01 (e goes negative, guard); on ctrl-r2.15 e swings 0.01 → 0.0009 → 0.019 in successive windows. Overpumping of the resonant cases (1.27–1.32× before dying) is the same disease.
4. The alternative faithful formulation — applying the integrated state correction (Δr, Δv) and refitting, instead of integrating the Gauss rates — overpumps window 1 by ~4.4× (e: 0.01 → 0.131 vs truth 0.0297), i.e. v1's failure mode. Both readings of "first-order integral along the unperturbed arc" fail.
5. Short-window control: at window = 1/8 synodic the same quadrature matches the true drift to a few per cent (machine-checked, `W=0.196: dr actual 1.379e-4 vs GL16 1.370e-4`). The machinery is correct; the window is too long for first order.
6. Not a small-e artifact: at e1(0) = 0.1 the same map still overpumps (arc-g8 max e 0.259 vs truth 0.138, guard death) — post-hoc diagnostic, not a criterion input.
7. Quadrature is not the bottleneck: g16 ≈ g8 on every metric (also GL-8 ≈ Simpson-2400 to 0.1% on window 1).

## Commands (each well under 60 s on the cloud container)

```
cd lab/results/20260929-2040-rung-r4-resonance-v2-14b1/work
gcc -O2 -o r4v2 r4v2.c -lm
./r4v2 selftest                      # osculating round-trip: 4.6e-13 (rung bound 1e-12)
python3 run_all.py                   # full grid: 5 cases x 8 configs, ~4 s; writes ../metrics.json
python3 picture.py                   # writes ../picture.svg
python3 ../../../verdict.py ../author-prompt.md ../metrics.json
```

Setup (frozen before the decisive grid; reconstruction, see *Predictions*): restricted 3-body, coplanar, G = 1, primary M = 1, test particle m1 = 0 with a1 = 1, e1(0) = 0.01, ϖ1(0) = 0, M1(0) = 0; perturber m2 = 3e-3 on a circular orbit with ϖ2 = 0 and w2 = λ2(0) = 0 (base) / 4.0 (shifted); period ratio exactly 2:1 (a2 = ((1+m2)/n2²)^(1/3), n2 = n1/2); controls at period ratios 5.00, 2.55, 2.15; duration 200 synodic periods; truth = barycentric RK4 N-body at 600/1200/2400 steps per orbit (max_e converged to 3e-6 relative across resolutions). Sampling: 25 samples per inner orbit; concentration = |Σ e^{iφ}|/N.

Truth anchors for the resonant cases: max e1 = 0.1417 (base) and 0.1713 (shifted; the rung's anchor is 0.175), both bounded, clear pumping (14× and 17× the initial e). Known weakness: the truth's concentration is **not** resolution-converged (base 0.53 @1200 vs 0.34 @2400; shifted 0.29 vs 0.22) — the resonant angle is chaotic on the 200-synodic timescale, so lib-ratio values carry ±0.3 of noise. This cannot rescue the candidates: their angle histograms are qualitally wrong (wrong libration centres), not just differently concentrated.

## Predictions

See `predictions.md` (written before any law run). What happened: the negative controls behaved as predicted (averaged: pump 3.3–6.7× — it destabilises rather than flattens; none: 0.06), the positive control passed exactly as predicted, and the arc candidates failed as the risk column anticipated, but by a sharper mechanism than predicted: I expected possible chaotic decorrelation of the concentration; the actual failure is more fundamental — zero first-order pump over closed windows plus O(1)-radian pericentre kicks. The reconstruction caveat also belongs here: the red-team's `e1_resonance.py` is not in this container, so the case is rebuilt from the rung text (m2 = 3e-3, 2:1, w2 = 4.0, ≥200 synodic); the anchors match to 2% (0.171 vs 0.175) and the concentration anchor (0.867) was not matched (my truth's is 0.22–0.34 — its wide-libration case), which is why I report the conc non-convergence explicitly rather than tuning ICs after seeing the law fail.

## What would make it wrong

- The window definition: I read "windows between conjunctions" as the full synodic window and "two windows per synodic period" as alignment mod π. If the intended window were instead keyed to the *particle's* orbit (e.g. pericentre to pericentre — my `averaged` config shows that variant is stable and still fails), the pump conclusion stands but the numbers move.
- The w2 reading: if w2 = 4.0 was the perturber's *pericentre* (eccentric perturber) rather than its initial longitude, the shifted case is a different trajectory; the base case and the mechanism (closure-zero pump, O(1) Δϖ) are unaffected.
- If the truth's own ICs differed in a way that makes its angle statistics regular (conc converged), the lib-ratio numbers would firm up; the pump failure would not move (max_e is converged to 3e-6).
- Adoption cost of the kill: none — it removes a candidate layer. The next candidate must carry second-order information per window (e.g. a two-iteration Picard pass, or windows short enough that ε(nW)² ≪ 1, which at 3e-3 means W well under half an orbit and hence more kicks per orbit than the ≤8 budget allows at 2:1) — that trade-off is the real content of this kill for the design.

Fit with PRINCIPLES: "A failed experiment kills that configuration, never the method" (#9); "Measure before claiming" — the mechanism is measured at one-window resolution, not inferred; "no trajectory identity" — judged on behaviours (pump band, concentration, controls) against a converged truth, per the r2 lesson; the falsifier was cheap (~4 s per full grid).

## The lens

This run came through a directed rung, not a free lens; the lens bias to declare is the author's: I calibrated ICs on the truth's anchors *before* running the law, but I did explore (and reject) re-tuning after seeing the candidates fail — the anchors, not the law, kept the setup frozen. What the lens may have missed: only the red-team's exact ICs (absent here) could confirm the 0.867 concentration anchor; and I did not test second-order window variants (out of the frozen configs), so "what would fix it" is argument, not measurement.
