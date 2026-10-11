# Dossier — 20261011-2235-library-54d9 (lens: Julien's library)

**Claim.** Per-body kick cadence fed back from the body's own state (a significance gate: next
interval `theta*|a|/|a_dot|`) turns the bounded second-order kick layer into a walking first-order
one — 10^3–10^4x worse at matched evaluation count — while per-body cadence *precomputed from the
body's constants* stays exactly on the fixed-cadence error/cost curve; the cadence lever is therefore
precomputed-from-constants (per body or per cell), never state-dependent, and B12's replacement
register should expose the log-log walk slope, not a magnitude.

**Bottleneck.** Board item 1 (kicks dominate the engine's cost; six runs say cadence is the lever)
plus queue top `q-b12-design`. Expected gain was >=2x fewer kicks at equal behaviour; measured
result kills the state-gated branch (the expected deletion does not exist) and confines the lever
to precomputed cadences (~1.1-1.2x here, i.e. nothing at belt scale) — redirecting the deletion
budget to the slack skin (12.6x, components-4643).

**Evidence.** Planar circular restricted 3-body (primary GM=1, parent mu=1e-3, R=1), exact-Kepler
drift + midpoint tidal kicks (indirect term included), 32 bodies, a in [0.25,0.55], e in [0,0.4],
seed 20261011, horizon 100 parent orbits. Oracle: the exact Jacobi integral (verified: fixed
cadence converges at ratio 4.0 per halving; the unshifted variant drifts 3.9e-4 and does not
converge, so it was rejected by the control). D = max_t |J-J0|/|J0|, median over bodies;
"rate" = kick evaluations per body-orbit; "slope" = log-log slope of |J-J0| vs t over the second
half of the horizon (0 = bounded, 1 = walk).

| scheme | gate | rate/orbit | med D | slope | note |
|---|---|---|---|---|---|
| A fixed | none | 2.2 → 141 | 1.2e-3 → 5.4e-8 | 0.03–0.08 | D ~ rate^-2.42; 14 evals reach D=1e-5 |
| B fd-gated | delayed | 4.1 → 161 | 1.2e-2 → 4.3e-4 | 0.75–0.98 | 21,668 evals reach D=1e-5: 1,548x A |
| C analytic gate | none | 17.6 → 83.7 | 5.2e-3 → 8.0e-4 | 0.83–1.00 | delay removed, still walks: state-feedback is the cause |
| D precomputed/body | none | 2.9 → 46.3 | 1.5e-3 → 5.7e-7 | 0.03–0.07 | on A's curve (1.1e-5 at 11.6 evals vs A's 14 for 1e-5) |

Behaviour, not just the invariant: at ~4x A's evaluations, B@theta=0.1 ends with median final
longitude error 1.16 rad and |dln a| 7.6e-3 (A@32: 0.017 rad, 8.8e-6). Mechanism: the gate holds
the field's fractional change per event constant, which phase-locks each event's truncation error
to the orbital phase — the same mistake every synodic cycle, slope ~1 — while fixed (globally
incommensurate) and precomputed cadences let the errors decorrelate and saturate. This is the
kick-layer echo of Calvo and Sanz-Serna (state-dependent steps are never symplectic; prior-art row)
and of probe 1 (per-body dynamical steps walk), now measured with a bounded-error oracle and split
into state-dependent (walks) vs precomputed (safe).

Reproduce (each command < 60 s, Linux/x86, orders of magnitude only):
```
cd lab/results/20261011-2235-library-54d9
for K in 8 16 32 64 128 256 512; do python3 sim.py jA$K.json A $K; done   # ~21 s total
for th in 0.02 0.05 0.1 0.2 0.5;    do python3 sim.py jB$th.json B $th; done  # ~20 s
for th in 0.05 0.1 0.2;            do python3 sim.py jC$th.json C $th; done   # ~11 s
for m in 4 8 16 32 64;             do python3 sim.py jD$m.json D $m; done     # ~6 s
python3 agg.py                                                            # table above
```
Kepler drift exactness self-test: round-trip 800 steps -> r error 6e-13; energy drift over 300
orbits 3.7e-14.

**Predictions** (`predictions.md`, written before the decisive sweep): P1 (gated >=2x cheaper at
equal D) **failed** — inverted by 10^3x. P2 (slopes < 0.5) failed for B and C, held for A and D.
P3 (theta=0.5 degrades worse than linearly) held. P4 (gain shrinks with e) moot — no gain at any e;
the worst bodies were the outer, synodic-slow ones (a~0.5). P5 (p99/mean wake-rate ratio >= 3x)
failed — measured 1.35–1.47. Two optimistic held-out predictions failed and are reported as failed.

**What would make it wrong.** One seed, one mass ratio (mu=1e-3), planar, tide-only (no encounters,
no kicks from close pairs), midpoint-quadrature kernel, gate rule = relative field change, 100
parent orbits. If the engine's kick is a residual against an exact generator whose error
decorrelates on its own, the phase-lock may not transfer; an anti-correlated interval rule
(alternating long/short) might break the lock — untested; a longer horizon could reveal walks in
the coarse precomputed points (D@m=8 already shows slope 0.37). Adoption cost: none for the kill;
the B12 slope statistic is free (running max plus a sampled fit). Fit with PRINCIPLES: "basically
we don't want errors that can compound that's the goal" (13); "error type over error size" (2);
"a failed experiment kills that configuration, never the method" (9).

**The lens.** Practitioner analogies re-derived known numerical analysis here (Calvo–Sanz-Serna
was already on the board); what the lens added is the decision discipline — delete-and-calibrate
(the Musk lesson) redirects the deletion budget away from cadence, and slope-not-magnitude (the
Waitzkin lesson) is the statistic B12 should freeze. The lens may have under-weighted what only
math sees: whether an anti-phase gate or a cell-level feedback exists that walks slower. Five
lessons with verbatim quotes: `lessons.md`; Readwise cache: `readwise.json` (770 items).

Grade suggested: **silver** — reproduced controls on both sides and a decisive kill of a
configuration, but the held-out gain predictions failed (honest miss), and no 10x gain was found.
