# Dossier — 20261014-2012-dynamics-71b4 (lens: dynamics and attractors)

**Claim.** The wiki's standing exception for state-fed-back cadence is dead: the
impulse-quantum trigger (524e's D) **walks in a bounded kernel** — slope median
0.89–0.92 at 400 parent orbits against the clock's ≤ 0.013 at matched kick
rates, D 11–13× the clock's measured frontier — and 524e's contrary evidence is
a machine artifact: its held-at-close kernel compounds for its own clock too
(slope ≈ 0.8, replicated), so "no differential walk" compared two walkers;
**what feeds back does not matter, state feedback of any kind walks** — the
524e-vs-54d9 contradiction is resolved and closed.

**Bottleneck.** The board's kick question ("fewer kicks per orbit at the same
behaviour") and the wiki's kick-cadence contradiction #3, named as "one
experiment decides". Expected gain: none to build — a kill. It deletes the
impulse-quantum trigger from the adoption path (the wiki's open direction 4
priced it "as shipped" with belt savings 2.6–2.9×) and redirects the cadence
lever to precomputed-from-constants rules only (54d9's surviving D scheme), and
it sharpens B12's replacement register: the walk slope must be exposed for
*every* event-triggered cadence, not only magnitude gates.

**Evidence.** One machine (harness2.py), 54d9's exact scene (planar CRTBP,
GM=1, μ_p=1e-3, R=1, the same 32 bodies, seed 20261011), second-order kernel:
exact Kepler drift between kicks, a fine sensor substeps the tide, the accrued
impulse is applied at the interval midpoint (rewind: drift half, kick, drift
half). Rules differ only in the interval end: **A** clock (K per parent orbit),
**C** 54d9's analytic gate (θ·|a|/|ȧ|), **Q** 524e's impulse quantum (fire when
accrued |∫g dt| ≥ q; crossing time solved by linear interpolation, not
grid-snapped). Oracle: the exact barycentric-rotation Jacobi, series rebuilt
post hoc from the fire log. slope = log-log slope of the running max of
|C−C0|/|C0| over the second half (0 = bounded, 1 = walk). Machine calibrated:
A converges at ratio 3.1–7.3 per rate doubling (second order, `runs/conv_A*.npz`);
C replicates 54d9 (slope 0.88 vs their 0.83–1.00).

Decisive batch (32 bodies, horizon 400 parent orbits; `runs/`, `python3 agg.py`):

| run | rate/orbit | D med | slope med | slope p90 | lock | dphi rad |
|---|---|---|---|---|---|---|
| A K=8 | 2.38 | 8.7e-4 | **0.000** | 0.13 | 0.00 | 0.00 |
| A K=16 | 4.75 | 1.8e-4 | **0.013** | 0.16 | 0.00 | 0.00 |
| A K=32 | 9.51 | 2.0e-5 | **0.001** | 0.07 | 0.00 | 0.00 |
| C θ=0.1 | 45.8 | 3.8e-3 | **0.881** | 1.64 | 0.32 | 0.18 |
| C θ=0.5 | 7.07 | 3.7e-2 | **0.646** | 1.34 | 0.27 | 0.71 |
| C θ=0.5, WS=512 | 7.13 | 3.4e-2 | **0.630** | 1.15 | 0.29 | 0.72 |
| Q q=1e-4 | 12.6 | 9.6e-3 | **0.920** | 1.09 | 0.12 | 0.26 |
| Q q=5e-4 | 3.07 | 1.1e-2 | **0.886** | 1.61 | 0.16 | 0.88 |
| Q q=5e-4, WS=512 | 3.18 | 3.5e-3 | **0.508** | 1.01 | 0.13 | 0.90 |

Matched-rate excess over the clock's measured frontier (D at H=400,
log-interpolated on A K=8..32): **Q 13× at rate 3.1, 11× at rate 12.6** (the
clock frontier is clamped at K=32, its finest measured point — the true excess
at rate 12.6 is larger); the gate 42× at rate 7.1; Q at WS=512 still 4× with
half the walk slope. The clock is bounded at every rate; both feedback rules
compound.

The walk is not a tick artifact, and solving the fire time does not remove it
(8-body pilots at q=5e-4, `runs/Q_ws*`): snapped fires at WS=512 read slope
0.028 at 100 orbits — clean-looking — but 0.356 at 400; fires solved by
interpolation read 0.140 at 100 orbits (WS=512) against the 32-body 0.508 at
400. A short horizon calls every fine-sensor variant bounded; the walk emerges
with horizon at both sensor rates and both fire-time treatments. The gate's
walk is sensor-rate-independent (0.646 → 0.630 from WS 128 → 512) while the
trigger's halves (0.886 → 0.508): part of the trigger's walk rate scales with
substep resolution, but it does not vanish — and 67f2's "timing error
forbidden" still generalises to trigger crossings as a design requirement
(the snapped H=100 readings differ from the solved ones).

Machine 1 (harness.py) replicates 524e's held-at-close kernel, 32 bodies, 100
orbits: **the clock itself compounds** — slope med 0.82 (A, 2.4 kicks/orbit),
0.83 (Q, 2.7) — matching 524e's checker (D ×2.27 vs ×2.41 per horizon doubling,
slopes ≈ 1.2/1.3): in that machine "no differential walk" is a comparison of
two walkers, and 524e's admitted-skipped P6 walk check is the hole. 524e's
kick-saving frontier (2.6–3.4× at matched error) is a 100-orbit statement in a
machine whose error compounds for every rule including its control.

Mechanism (measured split, P7): the gate's fires phase-lock — circular
concentration 0.27–0.32, increment spread 0.18 rad at high rate — while the
trigger's fires precess broadly (concentration 0.12–0.16, spread up to 0.90
rad) *and it still walks*: the trigger's walk is not the gate's attracting
fixed point. Candidate for the trigger: |g|-weighted firing selects
conjunction-like phases where the per-kick truncation error is largest and
one-signed — a selection bias a uniform clock does not have [INFERENCE,
untested; open direction 4].

**Predictions** (`predictions.md`, written before the decisive batch): P1
clock bounded (≤ 0.05) **held**; P2 gate walks (≥ 0.5) **held** (0.65–0.88); P3
trigger walks at both sensor rates (≥ 0.3) **held** (0.51–0.92); P4 walk
modulated by sensor rate for Q, not for C — **held** (Q: 0.89→0.51; C:
0.646→0.630, flat); P5 D ≥ 10× clock at matched rate **held** (13×); P6 kill
criterion (Q ≤ 0.1 at both WS) **did not fire**; P7 gate more phase-concentrated
than trigger **held** (0.27–0.32 vs 0.12–0.16).

**What would make it wrong.** One scene (54d9's), one μ, planar, tide-only,
midpoint kernel; the trigger's quantum is scalar-|∫g dt| with solved crossings
— a remainder-carrying (sigma-delta subtract-q) variant or a randomized/dithered
quantum could decorrelate the selection bias and is untested (open direction 4);
horizons to 400 parent orbits (walks measured on the second half); the
matched-rate excess uses a clock frontier clamped at K=32. Cost of adopting the
kill: zero — it deletes a candidate. PRINCIPLES fit: "basically we don't want
errors that can compound that's the goal" (13); "a failed experiment kills that
configuration, never the method" (9); "Measure before claiming" (10) — 524e's
own checker had the ×2.27 compounding clock in its record, and the folded wiki
row kept the trigger as the standing exception anyway.

**The lens.** The dynamics view (walk vs attractor, and the firing rule as a
return map) is what split the two walks apart and what flagged the transient:
the clean WS=512 median at 100 orbits is a slow-onset walk a short horizon
calls bounded — the lens's named blind spot, caught here by the horizon sweep.
What it may have missed: the trigger's exact mechanism is inferred, not
derived; and I did not chase the commensurability tongues of the quantum
(q vs per-cycle impulse), so a resonance-avoidance rule for q remains unmeasured.
