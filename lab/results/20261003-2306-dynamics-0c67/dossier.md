# Dossier — run 20261003-2306-dynamics-0c67 (lens: dynamics and attractors)

## Claim

In the plane's fleet regime (test bodies interior to a circular secondary), element-unpredictability
is not a resonance web but a wall: every body with a < a_wall ≈ 1 − 1.0·μ^{1/4} holds its osculating
elements predictable (twin decorrelation < 10⁻³·a over 120 orbits) at e ≤ 0.05 — including exactly on
the 3:1 and 2:1 commensurabilities — and at e = 0.2 everywhere except the 2:1's inner wing (7/180
twin pairs), while beyond the wall everything decorrelates within 2–18 orbits and is ejected; so the
orbit-averaged kick layer is valid through the entire interior (≈100× fewer kicks for a fleet at
lunar-scale μ, matching H0190's rate), and the regime boundary scales as μ^{1/4}, not the μ^{2/3}
per-resonance half-width the law's selector assumes (B17).

## Bottleneck

Board #1, "fewer kicks per orbit at the same behaviour: kicks dominate the engine's cost", and the
regime selector that decides who pays them. Expected gain: ~10²× on kick work for interior fleets
(the plane's fleet battle, LEO-to-MEO scale); it deletes the resonance-exclusion bookkeeping for
every interior body (no per-body commensurability check needed below the wall).

## Evidence

- μ = 0.0123 (Earth–Moon), a ∈ [0.30, 0.85], e ∈ {0, 0.05, 0.2}, 120 orbits, 12 phases per shell:
  interior (a ≤ 0.65): zero decorrelations at e = 0 and e = 0.05 (0/360), and 7/180 at e = 0.2 — all
  in the 2:1's inner wing at 0.60–0.65, three of which decorrelate only after ~120 orbits (T_d at the
  detection horizon); wall band [0.68, 0.85]: 100% decorrelate (Td median 2–6 orbits) and are ejected
  (deaths 100%), at every e. Whole-belt chaotic fraction 0.348.

- Wall position (e = 0.05, first shell with ≥50% decorrelation): μ = 10⁻³ → 0.825; 0.0123 → 0.675;
  0.03 → 0.60; 0.05 → 0.525; 0.1 → 0.475. Fit: 1 − a_wall ≈ 1.0·μ^{0.25} (α = 0.244), residual ≤ 0.03
  over three decades; at μ = 10⁻⁴ no wall inside 0.85 (predicted 0.9, outside the swept range).
- Interior stays clean at every μ up to 0.1 (max interior decorrelation fraction 0.000 everywhere).
- Controls: near-regular floor run (μ/1000): 1.1% decorrelation, all at the outermost shells; step
  halving 128→256 (μ = 0.0123, e = 0.05): identical classification (0.3333 vs 0.3333, deaths 0.3194
  both).
- Work: uniform 32 kicks/orbit vs averaged 0.3/orbit (H0190 K1/K2): interior fleet 107× less kick
  work; belt including wall and web only 3× (the web's cost is real there — that is r4/r9's regime).

Reproduce (each ≤ 60 s, 2 vCPU):
```
cd lab/results/20261003-2306-dynamics-0c67
python3 ftle2.py main      # 27 s: the geography, e=0/0.05/0.2
python3 ftle2.py sweep     # 38 s: mu = 1e-4, 1e-3, 3e-2
python3 ftle2.py heldout   # 12 s: mu = 0.05, 0.1 (held-out)
python3 ftle2.py floor     # 27 s: mu/1000 control
python3 ftle2.py step      # 12 s: 128 vs 256 steps/orbit control
python3 analyze.py         # wall fit, intermittency, work numbers
```
(requires numpy; `pip install numpy`)

## Predictions

`predictions.md` was written before the decisive run. What happened:
- P1 (resonance peaks at (p/(p+q))^{2/3}): **failed in the interior** — no enhanced decorrelation at
  0.48 (3:1) or 0.63 (2:1) at e ≤ 0.05; only the 2:1's inner wing shows at e = 0.2. The web is a wall.
- P2 (chaotic fraction 5–15% at e = 0.05): **failed in size** — 34.8%, all from the wall, not from
  distributed resonance widths; the e = 0 half held (clean interior).
- P3 (web measure ∝ μ^α, α ∈ [0.4, 0.7]; held-out > 60% at μ = 0.05, > 80% at 0.1): **failed and
  replaced**: α = 0.25; held-out fractions 56% and 67%. This failure is the result.
- P4 (intermittency, laminar duty > 50%): **failed** — the interior has zero surprise (no bursts to
  schedule around); the wall band decorrelates slowly (Td 9–29, 81% survive 120 orbits) but beyond it
  nothing survives. No adaptive cadence wins here; classification alone does the work.
- P5 (surprise-informed schedule ≥ 10× cheaper): **held** — 107× for an interior fleet.
- Method note, disclosed: the first implementation (variational tangent) was killed by a cross-check
  against a shadow-orbit pair (25× discrepancy, `ftle.py`); the shipped metric is the twin-shadow
  element decorrelation (`ftle2.py`). Predictions were written before either ran.

## What would make it wrong

- 2D and a circular secondary: the real Moon (e = 0.055) and the Sun's tide (H0190 included it) pump
  free eccentricity and can widen the 2:1 wing and fray the wall inward; an eccentric-secondary run
- RK4 is not symplectic: Jacobi drift median ≤ 9·10⁻⁶ on every run with μ ≤ 0.03; at μ = 0.1 the
  median is O(1), driven by close encounters among the 67% that decorrelate anyway (their
  classification is unaffected; the interior shells there still show zero decorrelation); the
  step-halving control leaves the classification unchanged.
- Adoption cost: one float probe (eccentric secondary + solar tide) and one rung on the integer law —
  averaged kicks everywhere with a < 1 − μ^{1/4}, judged by r4-style resonance gates at the 2:1 wing
  (e = 0.2) — before the selector's rule changes. Fit with PRINCIPLES: "cost follows change and
  entropy. Nothing is evolved that can be derived when looked at" (P3) and "regimes are chosen by
  dimensionless numbers" (P4): the μ^{1/4} wall is exactly such a number, the same law at every scale
  of secondary (P33).

## The lens

The dynamics lens measured where surprise lives and found a step function, not a spectrum — so the
attractor-flavoured half of my toolkit (duty cycles, burst scheduling, KS-entropy floors) had nothing
to grip: there is no intermittent attractor to follow inside, and outside nothing lasts. What this
lens may have missed: the cost *inside* the wall (r9's 4.6% compilable tori — a representation
question, not a predictability one), and transient chaos slower than the horizon. The KS floor is
therefore degenerate in this regime: Σλ⁺ is either 0 or saturated by ejecta.
