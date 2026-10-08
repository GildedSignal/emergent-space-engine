# Dossier — 20261008-2031-second-20261008-1947-redteam-efb2-4d7e (second author)

**Claim.** The checker's named experiment is done and the original claim holds on a clean
instrument: rung r6 (view at γ, PASS, two independent metric sets) shows the design's
crossing solver survives every γ ≤ 2×10⁶ flyby-free in the doll frame while the view's
"one sample per pixel" fails the received-history truth from γ ≈ 4 (β_o = 0.3; γ ≈ 25 at
β_o = 0.05) — an order of magnitude below the wagon-wheel boundary — and the k-averaged
sprite (the doc's own "type × log k table" form) passes at every γ, its worst residual
0.067 being the intra-window arrival wobble at β_o = 0.3, inherent to any k-keyed sprite.

**Bottleneck.** The view/observation premise (representation.md §2), unchanged from the first
run. What this run adds: the failure is measured on a corrected instrument (exposure truth,
per-emitter statistics, flyby-free scenes), its onset is 10× lower than the first run's
frozen-percentage headline suggested, and the proposed fix is now implemented and gated, not
asserted.

## Evidence (counts and per-frame percentiles; every command ≤ 60 s, Linux x86, load 0.29)

```
cd lab/results/20261008-2031-second-20261008-1947-redteam-efb2-4d7e/work
python3 gather_falsifier.py   # 29 s: original record, JSON bit-identical to the first run's
python3 r6_run.py             #  8 s: metrics.json + r6_results.json (author)
python3 r6_check.py           # 10 s: metrics-check.json + check-validation.json (independent)
python3 ../../../verdict.py r6-view-gamma.md metrics-check.json metrics.json
```

Scene: 32 lighthouse emitters on a ring R = 0.2 ls at β_o; observer closes at γ; 200 frames
at 60/s proper time; **D0 = 2.1·γ·N·Δτ + 100 ls (flyby-free by construction)**. Truth roots:
bisection (author) / fixed-point contraction (checker). Truth brightness: the k-weighted
average of the emission over the light received in each frame — closed-form in the window
edges, k = dt_arr/dt_emit the local arrival slope; validated by the checker three ways
(dense low-k quadrature: 5.4×10⁻⁹; full-window high-k quadrature: 7.2×10⁻⁷; exact
line-of-sight quadrature: 4.8×10⁻⁵). Verdict: **PASS — kavg passes every criterion;
exact-exposure (positive) passes; instant fails bright; raw-obs fails solve-fail and
wrong-roots. No disputed outcome between author and checker.**

| config | iters | fail | wrong roots | bright p99 | fate |
|---|---|---|---|---|---|
| kavg (candidate) | 3.9 | 0 | 0 | **0.060** | pass |
| exact-exposure (positive) | 0 | 0 | 0 | 0.060 | pass |
| instant (negative) | 3.9 | 0 | 0 | **1.132** | fail bright |
| raw-obs (negative) | 3.1 | 0.03% | 12702 | 0.060 | fail solve |

Per-case bright p99, instant → kavg (orbits/frame in brackets): γ=2.24/β_o=0.3: 0.076 →
0.0003 (0.016); γ=22.4: 0.728 → 0.028 (0.17); γ=70.7: 1.324 → 0.067 (0.57); γ=125: 1.005 →
0.001 (1.0); γ=250: 1.005 → 0.001 (1.99); γ=2×10⁶: 1.000 → 0.000 (2.7×10³–1.6×10⁴);
β_o = 0.05 ladder: instant 0.098 (γ=22.4) → 0.31 (70.7) → 0.95–1.0 (250–2×10⁶); kavg ≤ 0.0074
everywhere. **Onset of the instant law's failure: orbits/frame ≈ 0.03–0.1 (γ ≈ 4 at β_o =
0.3, γ ≈ 25 at β_o = 0.05)** — motion-blur level, an order of magnitude below Nyquist; the
plane's working point γ ≈ 2.3 is still honest (0.076 at β_o = 0.3, 0.009 at 0.05), its
refusal limit γ ≈ 2000 is deep in the failure.

**Corrections to the first run's record** (all checker-named, all confirmed here):
- The 75–100 % "frozen" percentages were flyby + median-of-positions artifacts. On the
  per-emitter statistic, frozen is a knife-edge on the fractional orbit rate: 100 % frozen at
  0.995 orbits/frame (γ=125), 0 % at 1.99 and 2.03 (γ=250/255) — there the render creeps at
  0.19 rad/frame while the received stream sweeps 12.8 rad/frame; pooled above-boundary
  frozen is 17 %. The aliasing is real (bright p99 ≈ 1 from γ = 70.7 up, every frame
  approaching); "frozen" was the wrong word for most of it.
- The γ 1–70.7 "clean" row is now genuinely clean on the per-emitter statistic:
  instant phase_below_p99 = 6.5×10⁻¹⁰ (the first run's own JSON had contradicted its table).
- The truth is local-geometry-derived throughout (crossing-to-crossing arrival slopes and the
  exact line-of-sight validation); the constant approaching k appears only in a diagnostic
  config.

## Predictions (predictions.md, written before the decisive run)

P1 ✓, P2 ✓ (β_o = 0.05: max 0.0074 ≤ 0.02), P3 ✓ (instant fails bright only, 1.132 ≥ 1.0;
below-Nyquist rotation honest per emitter), P4 ✓ (raw-obs fails the solve, passes bright —
at thousands of orbits per window a wrong root is invisible to the fluence criterion; the
two criteria are complementary and both needed), P5 ✓ (kavg vs exact-exposure differ by
< 10⁻⁹), P7 ✓ (kavg-global 0.008 ≤ 0.05: for whole-orbit windows the orbit-averaged arrival
compression equals √((1+β)/(1−β)), so the global k is a legitimate memo key for the fluence;
local geometry remains required for the crossing itself), P8 ✓ (flyby-free removes the only
stress; iters 3.9). **P6 ✗, and the miss is informative:** I predicted a broad frozen band
(≥ 0.8 at 2.03 orbits/frame); measured 0.0 there and 1.0 at 0.995 — the wagon wheel is a
resonance of the frame rate with the received period, not a band. The render's temporal
failure is better instrumented by the exposure truth (which fails smoothly from
orbits/frame ≈ 0.03) than by any frozen percentage.

## What would make it wrong

The truth's closed form drops the line-of-sight variation across a window (validated:
≤ 4.8×10⁻⁵ at the smallest D0 = 107 ls) and uses a linear arrival map within a window
(checked only through the exact-n quadrature, which shares it); a strongly accelerating
observer within one frame would need more. The 0.1 tolerance is 13× below instant's
measured p99 but only 1.7× above kavg's residual — if the integrator wants the sprite law
tighter than its own β_o-wobble, the sprite must key on more than k (sub-orbit structure),
which the design's memo does not have. Brightness is normalised: the DC beaming factor
(k⁴) is common to every law and cancels; a law that got k⁴ wrong would fail elsewhere
(B16's territory). β_o = 0 is not exercised (b constant — trivially honest); the γ ladder
is geometric, not continuous, and the frozen resonance at 0.995 shows the ladder can step
over narrow features — the exposure criterion is ladder-robust (monotone in orbits/frame),
frozen fractions are not.

## Cost of adopting, and fit with PRINCIPLES

(a) Commit `r6-view-gamma.md` (in `work/`, proposed for `lab/rungs/`) as rung r6 — the
checker's first named item. (b) One spec line in representation.md §2: aggregates crossing
the resolvability boundary render their k-averaged sprite (memo per type × log k), and the
crossing is solved in the tube's frame (the raw-magnitudes control fails at the queue's
γ = 10⁶). (c) One line in law.md's notes: rate extrapolation buys nothing over warm Newton
(equal at high γ, slightly worse mid-range) — the memo slope is a cost option, not a
correctness one. Fit: principle 28 — "The view is an instrument … your dials are made up
and hold no informations" — a render that shows a slow creep at 2×10³ orbits per frame is a
dial that lies; principle 32 — the doll-frame solve and the k-keyed sprite are the symmetry
made explicit; principle 34 — r6 judges the view's law, it does not size the view (the
per-pixel cap is untouched).

## The lens

Second-author lens: I inherited the first run's scene and its two latent flaws (fixed D0
flyby, median statistic) and nearly inherited a third — my first truth was a quadrature
that aliases exactly in the high-k regime it exists to judge (caught because the pilot's
kavg error tracked the node count, not the physics; replaced by the closed form). What I
may have missed: the exposure truth makes "one sample per pixel" fail at motion-blur level
(0.03 orbits/frame) — defensible (a frame is an exposure), but a integrator could
reasonably scope the criterion to orbits/frame ≥ 0.5 and keep instant sampling below; the
rung as frozen judges the strict form. The AI-perception extension (the same gather at each
AI's light cone) remains unmeasured, as in the first run.
