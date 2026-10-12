# Dossier — run 20261012-1524-dynamics-2b28 (lens: dynamics and attractors)

## Claim

The encounter-event rate of a many-body belt is set by its **phase-mixing
state**, not by orbit geometry: a pristine cached schedule is wrong by an
order of magnitude or more in **both directions** once coupling acts
(18x under-count in a belt at mass ratio 1e-9; ~40x over-count in a
phase-locked formation before it self-quenches), the feedback sign flips at
the board's own meso-motion number R = U/sqrt(mu_p/b) somewhere between 1
and 3.4, and no configuration cascades — so per-region event rates must be
treated as dynamical state read by the allocator, not as constants derived
from the candidate geometry.

## Bottleneck

The top scaling risk ("candidate pairs per body grow with N ... candidate
work must track real encounters", 5 October) and smoothness (p99, principle
12). What this run adds: even a **perfect** candidate tier (this toy's
conjunction times are exact) mis-predicts the *event load* by 1–2 orders of
magnitude, because the perturbations themselves move the rate. Expected gain
for the engine: the allocator and the schedule-cache/slack-skin get a
validity criterion (mixing state, R) instead of a geometry-only one; the
formation first-wave bomb gets a de-clustering rule. Order of magnitude: the
load planning error removed is 18–40x.

## Evidence

Machine: lab Linux x86, 8 vCPU, load 0.45 at start, all processes < 2.3 GB,
timings are orders of magnitude only. Model: `belt.py` — event-driven planar
Kepler belt (GM=1), encounters = conjunctions with miss distance < b, kicks
= exact hyperbolic impulses, no ticks; the control (`--nokick`) is the pure
pristine schedule. Conjunction counter validated flat (±0.4%) with b=1e-9;
element round-trip machine-exact (1.8e-15).

Belt: N=512, W=0.08, sig_e=0.015, b=4e-3, T=1500, 3 seeds; formation:
N=32, rank spacing 3e-3, T=3000. Full tables: `summary.md`; raw JSON per
run; reproduce with `bash runall.sh` (each command 30–170 s).

1. **Pristine belt under-counts; vanishing kicks unlock it.** Control rate
   4.51e-3 encounters/body/orbit, stationary (windows 4.35–4.67e-3), Fano
   0.96 (Poisson in time). At mu=1e-9 (R~50, e^2 flat to 1%, kicks 2e-8 of
   orbital velocity) the measured rate is **8.05e-2/body/orbit: A = 17.8x**
   (2 seeds, T=300), with Fano 70–80 — the unlock arrives in avalanches.
   Machine-precision noise alone (control) does **not** unlock it.
2. **The feedback sign flips near R ~ 1–3.** A(t) window means
   (early->end): mu=3e-8 (R_med 3.4): 1.44->1.34, sustained plateau;
   mu=3e-7 (R_med 1.0): 0.98->0.67; mu=2e-6 (R_med 0.4): 0.95->0.36.
   e^2 growth 1.12x / 2.12x / 3.89x; zero deaths. Stirring decomposition
   (mu=3e-7): measured d<e^2>/dt = 3.2e-7/orbit, between the random-walk
   (6.4e-8) and coherent-pumping (5.5e-7) bounds.
3. **No cascade anywhere.** No config has any 150-orbit window above 1.1x
   its first window; no exponential phase. The event process is
   self-quenching at strong coupling (A decays monotonically), never
   supercritical.
4. **Phase-locked formations over-count, then self-quench.** Weak coupling
   (mu=1e-11, R~45–48): peak/mean = 56 (aligned) / 46 (random) encounters
   per 50-orbit window, Fano 140 / 96, and the wave **persists** (peak 187
   in the first and last thirds) — the synodic lattice is commensurate
   (rank-m pairs conjunct at T_nearest/m), so the burst is structural, not
   an initial-condition artifact. Strong coupling (mu=1e-8, R~0.5–0.8):
   total encounters collapse 205->5 and 155->3, Fano -> 1: the first kicks
   dephase the lattice and the rate quenches ~40x.
5. **Work shape.** Re-pay (window recomputation per kick) is 62–98% of all
   ops in every belt config (the plane's 92% window-setup share,
   independently reproduced). The N-scaling probe (fixed linear density)
   was **not run clean**: at sig_e ~ W/4 the belt is genuinely
   all-overlapping, so repayment churn grows with N; the N=1024/2048 runs
   were killed for time and memory, only N=512 is on the record, so no
   per-body exponent is claimed here.

## Predictions

`predictions.md` was written before the ensemble (pilots: T=300 at
mu=3e-7/2e-6, formation mu=1e-11 only). Scorecard: **P1 failed** — and that
failure is the headline: I predicted A in [0.8,1.1] at mu=1e-9, measured
17.8. **P2 failed** (predicted quench at R~9, measured enhancement 1.2–1.4
at R_med 3.4 — same mechanism, my a-priori R estimate was high). P3 passed
on A (0.67 in [0.4,0.85]), e^2 marginally out (2.12 vs <=2). P4 passed
(A_end 0.36 < 0.5, e^2 3.9x, no deaths, no early rise). P8 passed (no
cascade). P7a passed (belt Fano 0.96 in [0.5,2]); P7b passed (46–56 >= 20,
both phase variants); P7c passed with a different mechanism (outright quench
after the first wave, not gradual decay). **P5 not run** (the N-scaling
runs were killed for time and memory before any clean measurement; the
encounter-rate part of the probe was also ill-posed at mu=1e-9, since that
rate is exactly the mixing-state-dependent quantity this run identifies);
repay/enc = 1022 is an instrument artifact (the N=512 belt is genuinely
all-overlapping, sig_e ~ W/4; a clean degree-scaling test needs
sig_e << W). P6 measured only at N=512 (repay share 62–98%): not a
scaling claim.

## What would make it wrong

- **No apsidal precession in the toy** (frozen periapses): the pristine
  belt's quasi-periodic miss structure (law.md line 39 already knows
  conjunction misses are quasi-periodic) is artificially persistent, so the
  18x unlock is an upper bound; a real belt's J2/planetary precession mixes
  apsides for free on its own timescale. The effect then becomes "who mixes
  first, precession or coupling" — still a dynamical state, but the free
  mixer differs. The formation over-count is precession-robust (it comes
  from synodic commensurability, not apsides).
- Impulses only at conjunctions, 2D, no accretion (mass growth would
  strengthen coupling over time — AI/factions are off-plan), single central
  field, miss distance by parabolic local refinement (O(1) rate
  calibration; all claims are same-instrument ratios), pairs with synodic
  period > T excluded (~7% of pairs at W=0.08, T=1500).
- The mu=1e-9 long-horizon runs (T=1500) were killed at ~20 min wall
  (12.5M repay ops each); persistence of the unlock at that exact mu is
  evidenced at mu=3e-8 (plateau over 1500 orbits), not directly measured.

## Cost of adoption, and fit with PRINCIPLES

Cheap: a rule, not code. (1) The allocator reads rolling per-region
encounter counts (mixing state) instead of trusting geometric capacity from
cached schedules. (2) Schedule-cache validity is bounded by mixing, not by
kick size — a region's cache horizon shrinks with coupling strength and
with player stirring, flipping sign of correction at R ~ 1–3. (3) A
formation's first conjunction wave is a p99 bomb (56x mean load in one
50-orbit window) whose times are known exactly ahead (integer circle
rotations) — de-cluster in idle time. Fits "the simulation tells us what is
next not us, subtle but deadly" (OC#36, principle 22) and "compute only
surprises" (principle 3): the unlock avalanches are the surprises, and they
cluster. Against "measure before claiming": cloud toy, orders of magnitude
only; the integrator re-measures on the plane.

## The lens

The attractors lens found the phase-transition-like object (mixing state +
sign flip in a dimensionless number) and the absence of a cascade. What it
missed: frame-scale (ms) burst structure — probed only at 1–50 orbit
windows, so the p99 statement is about load planning, not about a single
frame; carry widths and memory untouched; no Lyapunov exponent computed
(diffusion proxy only); the unlock's microscopic mechanism (which reservoir
empties first) is asserted by elimination, not measured — a dmin
distribution probe was planned and cut for time.
