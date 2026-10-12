# Dossier — run 20261011-2306-dynamics-0b04 (lens: dynamics and attractors)

**Claim (one sentence).** In the canonical belt scene (Jupiter-mass secondary, μ = 10⁻³), the
( E, L ) key process of essentially every body is diffusive, not a returning attractor: at
engine-scale quanta (q ≤ 10⁻⁵) the key changes ~once per planet orbit per body (churn ≈ 1),
so the exact cycle memo cannot pay anywhere in the scene, the compile load is *uniform*
(top-5% most chaotic bodies carry 5–7% of distinct keys, i.e. no concentration), and the
work rate is ranked by the Lyapunov classifier (ρ = 0.74) but **not** by a resonance
distance computed from time-averaged elements (ρ = −0.05), while a slow-diffusion middle
regime makes every short-window bounded-error test lie.

**Bottleneck.** Board #1 (kicks dominate cost) and the memory question (H_live): the per-kick
recompile story ("the plane recompiles an orbit on about 99% of kicks"; exact memo 0% hits,
5 October) is shown to be the *steady state of the physical dynamics* at game-canonical μ,
not an artifact: element diffusion at μ = 10⁻³ covers the whole swept belt (0.55–1.9 a_J,
e₀ = 0.05) within 3 000 planet orbits. What it deletes: any design that recovers memo reuse
in perturbed belts by better keying — the reuse is not there to recover; only the adopted
jet (re-anchored offsets, ~0.05 compiles/kick) amortizes. What it measures: a floor for
H_live per body (≥ 1 key change per orbit ≈ a few bits/orbit/body in the canonical scene).

## Evidence

All commands from `lab/results/20261011-2306-dynamics-0b04/`, each run once, machine
shared (load 0.9–3.8, 8 vCPU), walls 70–80 s each (over the 60 s guidance; run in
background concurrently, memory ≈ 60 MB each):

```
python3 belt.py --mu 1e-3 --T 3000 --spf 24 --N 112 --e0 0.05 --amin 0.55 --amax 1.9 --seed 7 --tag m1m
python3 belt.py --mu 0   --T 3000 --spf 24 --N 112 --tag mu0        # instrument control
python3 analyse.py m1m                                            # scores P1–P7, writes analysis-m1m.json
python3 belt.py --mu 3e-4 ... --tag m3e4 ; python3 belt.py --mu 3e-3 ... --tag m3e3   # held out, see below
```

Scene: circular restricted three-body, star + planet on an exact circle; ships are
massless bodies integrated by **the design's own motion path in float**: exact Kepler
drift in the star's doll (universal variables; round-trip error 1.1e-16, energy conserved
to 3e-15 over 4 000 steps) + second-order kicks (direct + indirect term). Sampling: once
per planet orbit; statistics over the second half (steady state). Key = rounded (E, L)
at relative quantum q; `revisit` = fraction of samples whose key was seen earlier (memo
hit with lag); `churn` = distinct keys per orbit; `lam_hat` = ln(max shadow separation
d₀ = 10⁻⁹)/T of an *unrenormalized* shadow pair (regime classifier; shear bias and
saturation floor stated below).

- **Control (P1): μ = 0 → revisit = 1.000 for every body at every q, distinct keys = 1.**
  Mis-specification disclosed: I predicted lam_hat < 1e-4; measured 6.3e-4 — this is the
  Kepler-shear bias ln(c·T)/T (finite-horizon artifact), so the chaos discriminant is
  lam_hat ≫ 6e-4, with saturation ceiling ln(0.5/d₀)/T = 1.06e-3. λ̂ has a narrow but
  usable dynamic range and is used only as a regime classifier.
- **m1m (μ = 10⁻³, N = 112):** revisit histogram at q = 1e-4: 50 bodies at 0.0, a spread
  0.1–0.8, only 6 above 0.8 — **not bimodal** (P2 as written fails; see lens note).
  churn ≥ 0.5 for 81% of bodies at q = 1e-4, 100% at q = 1e-5 and 1e-6 (P4 holds: at
  engine quanta everyone churns ~1 key/orbit). Element ranges in the second half: median
  relative range 1.1e-2 — order μ but ×10 my guessed oscillation amplitude (P4's factor-3
  clause fails). Held-out μ sweep and second seed (T = 3 000, N = 112 each,
  revisit-only regime split — the λ̂ clause of my classifier saturates from the shear
  bias and is not used):

  | μ | rev<0.05 | rev>0.8 | churn≥0.5 @q=1e-4 | @q=1e-5 | top-5% key share | ejected/escaped |
  |---|---|---|---|---|---|---|
  | 3e-4 | 34% | 39% | 46% | **98%** | 10.7% | 3/112 |
  | 1e-3 | 45% | 5% | 81% | **100%** | 7.0% | 35/112 |
  | 1e-3, seed 11 | 41% | 4% | 78% | **100%** | 7.2% | 31/112 |
  | 3e-3 | 62% | 0% | 100% | **100%** | 5.7% | 64/112 |

  The regular sea exists at μ = 3e-4 (39% of bodies return at q = 1e-4) and vanishes
  by μ = 1e-3 (5%) — a gradient, not a boundary (P2/P3 as written fail). But even
  inside that regular sea, churn at engine quantum q = 1e-5 is ≥ 0.5 for 98% of
  bodies: **the memo's dead zone is everything below q ≈ element range, regular sea
  included**; the seed reproduces m1m to within 4 points. μ = 3e-3 disrupts the belt
  (57% escaped, churn 100%).
  Top-5% share of distinct keys: 7.0% / 5.4% / 5.4% at q = 1e-4/1e-5/1e-6
  — **work is uniform** (P5 fails in the informative direction: no thin chaotic tail at
  this μ; the compile load is flat ≈ 1 key/orbit/body). Spearman ρ(lam_hat, churn@1e-4)
  = 0.737, ρ(lam_hat, revisit) = −0.738 (P6 first clause holds); ρ(d_res, churn) = −0.05
  (P6 second clause fails). MSD-slope vs revisit cross-agreement 48% (P7 fails): the
  slow-diffusion middle. Chaotic fraction by zone: co-orbital |a−1|<0.12 → 100%;
  interior 0.55–0.60 → 86%; first-order resonance band 0.63–0.86 → 100%; outer edge
  1.69–1.9 → 0–38% with rev_med up to 0.8 (the only quasi-regular pocket, furthest from
  the perturber). Held-out details: `analysis-m3e4.json` / `analysis-m3e3.json` /
  `analysis-m1m_s11.json`.

## What this means for the engine (the adoptable part)

1. **The memo is dead in perturbed belts at any quantum below the element range; the
   range is order μ and *grows* under diffusion** (median 1.1e-2 relative here over
   1 500 orbits). The 5 October plane measurement (exact memo 0% on distinct kicks) was
   not a scene artifact — it is the belt's physical steady state. Design consequence:
   keep the jet (re-anchored offsets, already adopted) as the only amortizer; do not
   spend a build making memo keys smarter at strong μ.
2. **The compile budget is predictable and flat at canonical μ**: ~1 element-key change
   per body per orbit (bounded below by my 1/orbit sampling, above by the plane's
   per-kick 99%). No p99 smoothing problem arises from chaos concentration — the
   allocator's enemy here is the flat N× rate, i.e. cadence (board #1), not tails.
3. **H_live gets a measured floor** (the risk HANDOFF flags as unmeasured): ≥ 1
   key-change per orbit per body ≈ a few bits/orbit/body in the canonical scene; a 2²⁰
   belt accumulates distinctions at that rate under perturbation — the population store
   (B18b) must reabsorb at it. This is the dynamics-side number the directed b-h-live
   build can consume.
4. **A danger for B12's redesign (and any bounded-vs-compounding instrument):** the
   slow-diffusion regime (bounded-looking MSD at ≤ 128-orbit lags, zero key returns)
   defeats any windowed boundedness test; error statistics must aggregate over horizons
   comparable to the certificate's, or compare distributions, not windows. This is a
   mechanism, not a gate proposal (B12's redesign is owned elsewhere).
5. **The resonance detector cannot be fed averaged elements**: ρ(d_res from mean a,
   churn) ≈ 0. The law's per-kick detector evaluates *current* frequencies, which my
   proxy cannot falsify; but any scheduler that ranks work by time-averaged resonance
   state will misallocate in exactly the diffusive (canonical) case. Rank by a
   separation-growth classifier instead — it carried ρ = 0.74 with a near-binary
   dynamic range.

## Predictions vs outcome (details in predictions.md)

Held: P1 (control, with the disclosed λ threshold miss), P4 main clause, P6-λ
(ρ(lam_hat, churn) = 0.74). Failed: P2 (no bimodality — a μ-graded gradient instead),
P3 (d_res does not separate; interior not regular), P5 (no concentration), P6-d_res,
P7 (48%). Held-out (P8), run and scored after the decisive run and disclosed as such:
μ = 3e-4 grows the regular sea (39% returning at q = 1e-4) yet 98% churn at q = 1e-5;
μ = 3e-3 disrupts the belt (57% escaped); seed 11 reproduces m1m within 4 points
(`analysis-m3e4.json` / `analysis-m3e3.json` / `analysis-m1m_s11.json`). The checker
should re-score them independently (commands above).

## What would make it wrong

- Float, not the integer law: my trajectory is the design's motion path in float64; the
  law's quantized elements see the same physical diffusion (≫ quanta) but its key sizes
  and kick phasing differ — the *churn rate per kick* could differ from my per-orbit
  floor by the kick cadence factor (measured bounds given above).
- One perturber, planar, circular, e₀ = 0.05, horizon 3 000 orbits: longer horizons and
  eccentric/inclined/multiple secondaries only add resonance web density — they cannot
  reduce diffusion. The weaker-μ case (3e-4) *did* grow a regular sea (39% returning at
  q = 1e-4) and still churns at engine quantum (98% at q = 1e-5), so the memo's dead
  zone is as claimed, not larger.
- The λ̂ classifier's narrow range (shear bias 6e-4 to saturation 1.1e-3) is a
  horizon artifact; with T = 3×10⁴ the ordering claim (ρ = 0.74) should sharpen, not
  flip.

**Cost of adopting:** none — this deletes a hope (smart memo keys in perturbed belts)
and hands two numbers (flat compile rate ~1/orbit/body; H_live floor) to the cadence
and belt builds. **Fit with PRINCIPLES:** "Compute only surprises" (#3) — the surprises
in a perturbed belt are the element diffusion itself, and their rate is the budget;
"the simulation decides; heuristics schedule" (#22) — rank by measured separation
growth, not averaged resonance state; "Errors never compound" (#13) — the compounding
here is *physical* (information created), which is why the store, not the integrator,
must absorb it.

**The lens:** dynamics framing found the attractor structure absent where the design
hoped for it (returning keys), and found the transient trap (slow diffusion) the lens's
own blind spot warns about. What it may have missed: the per-kick key dynamics *inside*
one orbit (my sampling is per-orbit), and the integer law's exact rounding behaviour on
top of these trajectories.
