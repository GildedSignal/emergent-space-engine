# Dossier — run 20261009-1649-dynamics-ec3a (dynamics and attractors lens)

## Claim

In a stable belt under the design's own regime (exact compiled Kepler drift +
secondary tide as kicks), the per-body rate of element-quantum re-keys is
BROAD, not heavy-tailed (p99/mean ≈ 3.3, no hot minority), so a uniform tick
sized for the p99 body wastes ~70% of its re-key work — but two thirds of
that work is *predictable* (secular librators whose re-keys are schedulable
from the compiled drift), only ~1/3 is genuine surprise (chaotic walkers),
and the parent's J2 freezes 81% of the belt outright.

## Bottleneck

Board item 1 (fewer kicks per orbit — "cadence is the lever", six runs killed
correctors) and the unmeasured risk "distinctions created per game-second
(H_live) decide whether 10^9 fit in 8 GB". Expected gain: an order-of-magnitude
map of where the belt's re-key work actually lives, telling q-cadence whether
to chase concentration (no) or predictability (yes). Deletes the assumption
that belt work concentrates in a hot minority.

## Evidence

Oracle = the design's own split: exact Kepler drift (universal variables,
machine-precision: 4e-14 over 2000 drifts) + shared-step kick-drift-kick tide
(+ indirect term, optional planar J2), planar restricted, secondary on an
exact orbit. Secular elements = double average (own period, then synodic),
exact-width rings, settled-gated. Quantum crossings of the (E,L)-native grids:
q_a = QA·a0² (fixed dE grid), q_e absolute; a crossing = one memo re-key =
one distinction/kick. Law-scale quanta: q_a ≈ 1e-3·a, q_e = 1e-2, mults
{1, 3.16, 10} tracked in-run.

Main numbers (mult 1; T = 2400 ≈ 1700 mid-belt orbits, N = 1024):

| config | live | key-rate mean / med / p99 (per orbit) | S=p99/mean | waste@p99 | frozen / librarian / walker | burst |
|---|---|---|---|---|---|---|
| C0 m'=0.03 e'=0.05 | 0.97 | 0.91 / 0.71 / 3.0 | 3.3 | 0.70 | 0.08 / 0.56 / 0.33 | 1.4 |
| C1 m'=0 (negative) | 1.00 | 0 / 0 / 0 | — | — | 1.00 / 0 / 0 | — |
| C2 edge e'=0.15 | 0.03 | 9.3 / 9.6 / 14 | 1.5 | 0.34 | (97% ejected) | 5.2 |
| H1 m'=0.06 | 0.94 | 1.57 / 1.27 / 5.5 | 3.5 | 0.72 | 0.02 / 0.64 / 0.28 | 1.3 |
| H2 e'=0.3 | 0.06 | 2.4 / 2.4 / 3.0 | 1.2 | 0.19 | (94% ejected) | 8.3 |
| H3 J2=0.01 | 1.00 | 0.48 / 0.21 / 2.3 | 4.7 | 0.79 | 0.81 / 0.11 / 0.08 | 1.0 |

- Controls: C1 gives EXACTLY zero crossings at every quantum (instrument
  floor is machine-level). C2 was mistuned past the true S-type stability
  edge (a_c ≈ 0.36 for e' = 0.15): 97% ejected, so it stopped being the
  intended "concentrated but stable" control (see Predictions).
- Robustness: seed 8 → mean 0.885, S 3.22 (vs 0.907, 3.30). dt halved →
  rate scale ×1.7 (sampling-grid systematic of the leakage floor below),
  S 3.02, classification within 10 pp — the SHAPE is converged, the absolute
  scale is order-of-magnitude only (cloud x86; treat as OoM per AGENTS).
- Structure: the e-key (forced-e oscillation) is the near-uniform layer
  (S_e ≈ 2.7); the a-key carries all the structure (S_a 3.6 → 4.6 as q grows;
  under J2 S_a → 14.9 at mult 10 with 81% frozen). Time-burstiness ≤ 1.8 in
  every stable config: re-keys arrive smoothly (no Kingman tail here).
- Plots: `rates_vs_a.png` (rates vs a with MMR lines), `traces.png`
  (hottest 8 walkers vs coldest 8 bounded librators).

Reproduce (each ~4–8 min, one core, < 300 MB):

```
cd lab/results/20261009-1649-dynamics-ec3a
python3 belt_surprise.py --out runs/C0_main  --tmax 2400 --nbody 1024 --dtper 32 --dsamp 0.05 --qa 3e-3 --qe 1e-2
python3 belt_surprise.py --out runs/C1_nomass --tmax 2400 --nbody 1024 --dtper 32 --dsamp 0.05 --qa 3e-3 --qe 1e-2 --mprime 0
python3 belt_surprise.py --out runs/C2_edge   --tmax 2400 --nbody 1024 --dtper 32 --dsamp 0.05 --qa 3e-3 --qe 1e-2 --amin 0.36 --amax 0.46 --eprime 0.15
python3 belt_surprise.py --out runs/H1_mass2x --tmax 2400 --nbody 1024 --dtper 32 --dsamp 0.05 --qa 3e-3 --qe 1e-2 --mprime 0.06
python3 belt_surprise.py --out runs/H2_ee03   --tmax 2400 --nbody 1024 --dtper 32 --dsamp 0.05 --qa 3e-3 --qe 1e-2 --eprime 0.3
python3 belt_surprise.py --out runs/H3_j2     --tmax 2400 --nbody 1024 --dtper 32 --dsamp 0.05 --qa 3e-3 --qe 1e-2 --j2 0.01
python3 belt_surprise.py --out runs/S0_seed8  --tmax 2400 --nbody 1024 --dtper 32 --dsamp 0.05 --qa 3e-3 --qe 1e-2 --seed 8
python3 belt_surprise.py --out runs/V0_dtconv --tmax 2400 --nbody 1024 --dtper 64 --dsamp 0.05 --qa 3e-3 --qe 1e-2   # dt halved
python3 analyze.py   # table + plots
```

## Predictions

`predictions.md` was written before these runs (calibration used only a
T=300 short run). What happened:

- HELD: P1 (negative control exactly zero), P3 (m'×2 → rate ×1.73 in
  [1.5, 2.6]; S stable), P7 (C0 S = 3.3 ∈ [3,10]; walkers 0.33 ∈ [0.25,0.75]),
  P6 (burst ≤ 3 in all stable configs; H2 = 8.3 and C2 = 5.2 flagged as
  predicted for the unstable ones).
- FAILED, with cause: P2 (positive control S ≥ 8) and P4's e-scaling — both
  configs collapsed (97% / 94% ejected) past the S-type stability edge I
  mis-estimated when writing them (used the e'=0.05 edge for e'=0.15/0.3).
  The survivors are a biased stable sample; concentration among them is LOW,
  not high. The ejection-fraction half of P4 held.
- PARTIAL: P5 — rates scale ∝ 1/quantum everywhere (amplitudes ≫ quanta) and
  S grows mildly with q as predicted, but frac_zero stays 0 in stable belts
  (freeze-out appears only under J2, 81%).

## What would make it wrong

- The absolute rate scale carries a ×1.7 sampling-grid systematic (mixed
  tide terms p·n − q·n' leak through any time-domain average; the design's
  analytic orbit-average would not leak — my instrument approximates it).
  The load-bearing numbers (S, waste, classification, burst) are stable
  across seed, dt and quantum.
- Classification cuts are conventional (frozen ≤ 2 quanta range; walker =
  net drift > 25% of range): a different cut moves fractions ~10 pp.
- Planar restricted model: no inclination, no belt self-gravity (B18b's
  populations), single secondary. A belt near MMR overlap — what C2 meant
  to be — could concentrate far more; that control needs redesign just
  inside its true edge (a_c from Holman–Wiegert at the actual e').
- T ≈ 1700 orbits: chaotic diffusion has memory, so the walker fraction is
  a lower bound on the long-run surprise load (the lens's own blind spot).

## Cost of adoption, and fit with PRINCIPLES

No new crate; one judge/policy input. For q-cadence: size the tick or the
event budget to the MEAN secular rate (0.7–0.9/orbit at law quanta here),
not the p99 — a uniform p99 policy spends 70% of its work on bodies whose
elements did not cross a quantum ("No work for no reason, so no ticks";
"compute only surprises"). For the allocator: tier by PREDICTABILITY, not
hotness — librators' re-keys are exact consequences of the compiled drift
(event keys: zero polling), walkers (1/3) are the genuine surprises. J2
(H0190: "J2 must be in the formula") doubles as a surprise suppressor:
81% frozen, S_a → 15 at coarse quanta. For H_live: the first measured
shape — broad, smooth in time, mass-linear in the secondary — so 10^9-body
memory tiering should not bank on a hot minority in belts.

## The lens

I read the belt as element-space attractors (frozen / bounded librator /
random walker) and treated the re-key rate as the engine's surprise measure.
Missed: Lyapunov/KS spectra (the walker rate is their shadow, not their
measure), allocator queue dynamics under real loads, and transients beyond
~1700 orbits. The biggest thing this lens nearly hid: the difference between
*concentrated* work and *predictable* work — the first is what I went
looking for (and mostly did not find), the second is what the engine can
actually exploit.

## Grade (author's self-assessment)

Silver: reproduced, controlled, half the held-out predictions held and both
misses are explained and physically meaningful; the 10× adoption bar is not
met in the stable-belt regime. The named gold step: a predictability-tiered
cadence policy (event keys for librators, slack skin for walkers) judged by
the plane's cost judge at equal behaviour, plus the corrected
just-inside-the-edge control.
