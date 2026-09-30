# Dossier — rung r4 v2: arc-integrated kicks vs resonance

Run: `20260930-0732-rung-r4-resonance-v2-0a18` (author GLM, 30 September 2026, cloud container 4 vCPU).

## Claim

First-order arc-integrated (Gauss–Picard) kicks applied at conjunction windows **do not** reproduce mean-motion-resonance behaviour: they over-pump eccentricity 2.4–4.5×, the resonant angle circulates instead of librating, and they excite spurious resonance 7.5 % off the 2:1 — while the positive control (truth-1200 vs truth-2400) passes every criterion. **KILL of the arc-g8 / arc-g16 / arc-g8-half configurations** (the configuration dies, not the method: the truth, the rates and the controls are all healthy).

## Bottleneck

Board #2 (stepping owned by cells, or no stepping): this was the rung named by the premise red-team as the experiment that would make its "kicks survive" half gold. It does not survive on the design's own cheap path. What it deletes: any event layer that applies the whole window-integrated Δ at the window end cannot self-limit a resonance; resonance behaviour needs the angle's feedback *inside* the window (or per-conjunction sub-stepping of the phase), which is a different, more expensive layer than the one specced. Expected gain of the dead config was 10²–10³× fewer events than dense integration; the honest cost of what remains is: quadrature 8–16 nodes per window (≈ 4–8 nodes per inner orbit at 2:1), ~0.5–4 window ends per orbit (see micro-window caveat below), zero dense dynamics steps.

## Setup (mine; the rung froze the rest)

G = M = a₁ = 1, m₂/M = 3e-3, coplanar; particle massless (restricted), circular outer perturber, q = P₂/P₁ exact, e₁₀ = 0.05, ϖ₁₀ = λ₁₀ = 0. Resonant cases: λ₂₀ = 0 (base; truth concentration R = 0.84) and λ₂₀ = 4.0 rad (the rung's w₂ = 4.0, read as radians; truth R = 0.23). Truth: leapfrog N-body (central + perturber + particle, barycentric), fixed step, 600/1200/2400 steps per inner orbit. Law: elements frozen within each window (conjunctions in mean longitude; `arc-g8-half` uses fixed P_syn/2), Gauss planetary rates (direct + indirect perturbing acceleration) integrated by Gauss–Legendre 8/16 nodes, applied as a jump at the window end; `averaged` = same windows, double orbit-average over both mean anomalies (H0190 K2); `none` = no perturbation. Resonant angle φ = 2λ₂ − λ₁ − ϖ₁; concentration = mean resultant length. 200 synodic periods per case, both sides sampled 50× per orbit.

## Evidence

| config | pump_min (≥0.8) | pump_max (≤1.25) | lib_min (≥0.8) | ctrl (≥1.0) | dense (≤0) | kicks (≤8) | verdict |
|---|---|---|---|---|---|---|---|
| arc-g8 | **2.42** | **3.90** | **0.040** | **0.33** | 0 | 3.98 | FAIL |
| arc-g16 | **4.10** | **4.54** | **0.019** | **0.33** | 0 | 4.07 | FAIL |
| arc-g8-half | **2.96** | **4.27** | **0.088** | **0.33** | 0 | 1.33 | FAIL |
| averaged (neg) | **0.28** | 0.38 | 1.12 | 0.33 | 0 | 2.66 | FAIL (as required) |
| none (neg) | **0.28** | 0.38 | 1.20 | 0.33 | 0 | 0.54 | FAIL (as required) |
| truth-1200 (pos) | 1.000 | 1.000 | 1.000 | 1.00 | 0 | 0 | **PASS** |

Truth max-e: 0.1317 (base), 0.1809 (shift); the arc laws pump to 0.44–0.74. Truth convergence: truth-600 vs 2400 max |Δe_max|/e_max = 1.0e-3, truth-1200 vs 2400 = 2.3e-4; |ΔR| ≤ 1.3e-4 at 1200. Controls: far control (q = 5.00) matches to 1e-4 in the envelope; q = 2.55 matches the envelope top (0.0501 vs 0.0500) but the truth's e dips to 0.036 transiently and the law's dives to ~0; q = 2.15 the truth stays ≤ 0.05 (dipping once to 0.0004) while arc laws pump to 0.15–0.50. Osculating elements round-trip position/velocity to 1.1e-13 (300 random states; gate 1e-12). The Gauss rates themselves were validated against a finite-difference of the true restricted dynamics (RK4, ±2e-4 centered): all four rates agree to 5 digits at two independent geometries — the kill is not a sign error (r4 v1's failure mode).

Quadrature nodes (reported separately per the rung): 8 or 16 per window; at 2:1 a conjunction window is 2 inner orbits, i.e. **4 (g8) or 8 (g16) nodes per inner orbit**; arc-g16 pumps harder than arc-g8, so the failure is not quadrature undersampling. Halving the window (arc-g8-half) reduces but does not remove the spurious pump (0.15 vs 0.44–0.50 at q = 2.15).

**Micro-window caveat (honest accounting):** the element jump shifts mean longitude by O(μ), which un-crosses the conjunction phase, so each real conjunction spawns ~3 near-zero-length window ends (e.g. 996 vs 204 window ends for `none` at q = 5.00). Their kicks scale with window length (≤ 1e-6 of a real kick), so dynamics are unaffected, but the raw `kicks_per_orbit` (~4) over-counts real kicks (~0.8–1 per orbit). Even raw counts pass the ≤ 8 gate; effective counts pass it far more comfortably.

**Commands** (each ≤ 60 s, cloud x86; orders of magnitude only):
```
pip3 install -q numpy matplotlib        # once
python3 r4v2.py sanity                  # ~1 s: round-trip 1.1e-13, GL checks, short overlays
python3 r4v2.py ics                     # ~4 s: IC scan (libration appears after λ₂ fix)
python3 r4v2.py truth                   # ~22 s: 600/1200/2400 × 5 cases
python3 r4v2.py law arc-g8              # ~2 s; likewise arc-g16, arc-g8-half, averaged, none
python3 metrics.py                      # metrics.json + verdict table
python3 picture.py                      # picture.svg / picture.png
```
Data: `samples/*.npz` (decimated to ≤ 4000 points/run), summaries in `truth*.json`, `law-*.json`, `ic.json`, `ic-scan.json`.

## Predictions

See [predictions.md](predictions.md), written before the 200-synodic runs. **Held.** All four numbered predictions were correct in direction and mostly in magnitude: candidates fail pump_max (2.4–4.5×), libration (0.02–0.09) and controls (1/3); `averaged` and `none` fail pump (≈ 0.28); truth-1200 passes everything. Misses: I predicted control_pass_fraction ≈ 2/3 for the arc laws (expected only q = 2.15 to fail); it is 1/3 because the q = 2.55 control fails on the envelope *bottom* (truth's transient dip to e = 0.036, law dives to ~0) — my envelope test bounds both ends (see metrics.py). I also did not predict `averaged`'s lib_min = 1.12 "pass": at exact q = 2.0 the angle drift 2n₂ − n₁ − ϖ̇ is slow, so even a non-librating angle concentrates over 200 synodic periods; it is a kinematic artifact of exact commensurability, not resonance capture (the histogram shows slow drift, not libration).

## What would make it wrong; cost; fit

Wrong if my window semantics differ from the design's intent (mean-longitude conjunctions, whole-window integral applied at the end — both as the rung froze them), or if the resonant ICs are unrepresentative (the rung pinned m₂ = 3e-3 and w₂ = 4.0; e₁₀ = 0.05 and λ₂₀ = 0 are mine; the IC scan shows libration quality varies with phase, but the over-pump held for every phase and eccentricity tried in setup, e₁₀ ∈ [0.05, 0.25]). Cost of adoption: none — nothing is adopted; the surviving facts (validated Gauss-rate layer, truth ladder, control behaviour at 2.15/2.55) are reusable pieces. Fit with PRINCIPLES: "A failed experiment kills that configuration, never the method" (#9) — this KILL is of the arc-kick event layer as specified; "Measure before claiming" (#10) — rates validated to 5 digits before any long run; "Compute only surprises" (#3) — the surprise budget was ~1 event per conjunction and it was spent without capturing the resonant surprise, which is exactly the kind of evidence the integrator needs for bottleneck 2. The rung's own r2 lesson was respected: no trajectory identity was demanded; behaviours and statistics only.

## What this run may have missed

I did not test windows shorter than P_syn/2 (the trend arc-g16 → arc-g8-half suggests shorter windows help but not enough); did not test second-order Picard (arc updated mid-window), which is the natural next candidate but is no longer "first order" as frozen; did not test eccentric outer perturbers or inclined geometry (the red-team's cases were coplanar too); the resonant-angle concentration metric is degenerate at exact commensurability (see the `averaged` artifact) — future rungs should add a small detuning or use libration-amplitude metrics. Two implementation bugs were found and fixed *before* the decisive runs (mutual-gravity sign; λ₂ missing its periapse term), both caught by controls — the r2 criterion lesson working as designed.
