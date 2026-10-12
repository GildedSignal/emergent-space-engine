# Dossier — run 20261012-1340-second-20261012-1227-system-8685-2eb1 (second author)

## Claim

The checker's named experiment succeeds: rebuilding the between-window averaged
term **orbit-anchored** (one midpoint-sampled kick per mean-longitude segment on
a fixed grid of K per orbit, conjunction windows riding on top at fine cadence,
nothing dropped at transitions) removes the aliasing subharmonic at **every**
segment length (Δė 84–134 MADs → 0.01–0.11; Jacobi 48–175× the floor → 1.0×)
and closes the belt ϖ̇ break (+64% window-only → +2.5% at K=16, **+0.5% at
K=32**; ≤ 6.6% at K=8 across all W) — so the secular term does **not** have to
be continuous: a discrete orbit-anchored per-phase kick carries it, and the
deployable rule is "secular = one midpoint kick per fixed orbital-phase segment,
K ≥ 16 for percent-level precession, K = 2 forbidden"; the tick-anchored variant
stays dead at every segment length. The 64-seed encounter inversion (w0.5 2.78
vs count-matched u8 2.43 MADs — noise; u16 at 0.60 beats both) is reproduced in
this shipped record, retiring the original's impulsive-regime win.

## Bottleneck

Board bullet 1 (fewer kicks per orbit at the same behaviour; feeds the queued
q-cadence rung). Gain: not a new cost lever — a **component rule** for motion-law
v2: how the orbit-averaged secular term may be scheduled (discrete, orbit-
anchored, midpoint-sampled) and how it may not (tick-anchored, endpoint-sampled,
re-origined). What it deletes: any candidate design that quantizes the secular
term at a fixed time fraction, and the worry that event-scheduled variable
cadence walks Jacobi.

## Evidence

Same replica as the original run (2D test particle + circular planet, static
star; DKD Wisdom–Holman, exact Kepler drift; SyMBA shell refinement shared by
all variants). `window_clock.c` extends the original **without changing any
original variant** — all rerun cells are bit-identical to the committed record
(belt/encounter/resonant × u/w/seg8, sweeps; seeds 0–15 of the 64-seed truth
identical to `belt-truth.csv`). Truth = u2048 at **64 seeds** (convergence at
u4096: 0.37/0.50 MADs), fixing the original's 16-seed noise floor. Deviations in
truth-ensemble MADs; floor = u64's median Jacobi drift (1.18e-3).

Belt, 64 seeds (`analyze.py`, table 1):

| variant | k/orb | sol/orb | Δϖ̇ MAD | rel% | Δė MAD | Jacobi ×floor |
|---|---|---|---|---|---|---|
| u64 / u8 | 64 / 8 | 128 / 16 | 0.00 | −0.0 / −0.03 | 0.01 / 0.04 | 1.0 |
| w0.5 (windows only) | 10.2 | 128 | 6.74 | **+64.0** | 0.32 | 1.0 |
| w0.5seg4 / seg8 / seg16 | 20.9 / 14.5 / 10.6 | 122 / 114 / 105 | 0.67 / 5.83 / 11.40 | +6 / −55 / +108 | **4.2 / 134 / 84** | **49 / 121 / 175** |
| w0.5seg8m (midpoint only) | 16.1 | 128 | 8.23 | −78 | **163** | **2.5** |
| w0.5seg8n (no-drop only) | 13.9 | 105 | 2.63 | +25 | 23.6 | **195** |
| w0.5seg8mn (both) | 15.4 | 117 | 2.20 | +21 | 34.7 | 90 |
| w0.5p2 | 15.8 | 31.6 | 9.57 | +91 | 259 | 3.6 |
| **w0.5p4** | 18.2 | 36.4 | 3.47 | +33.0 | **0.11** | **1.0** |
| **w0.5p8** | 22.7 | 45.3 | 1.05 | +10.0 | **0.06** | **1.0** |
| **w0.5p16** | 31.5 | 63.0 | 0.26 | **+2.5** | **0.03** | **1.0** |
| **w0.5p32** | 49.2 | 98.4 | 0.05 | **+0.5** | **0.01** | **1.0** |

W-sweep (16 seeds, table 2): window-only ϖ̇ rel +45/+6/+61/+134/+61% at
W = 0.125/0.25/0.5/1.0/2.5 vs **p8: +4.5/+6.3/+6.6/+0.9/+4.0%** (Jacobi 1.1×
floor everywhere). Pure grid (`w0.01p8`, windows negligible): +2.0% at
15.1 k/orb — the K=8 windowed residual is a window–grid interaction of a few
percent, not grid quadrature. Encounter, 64 seeds vs u4096 truth (table 3):
Δė u8 = 2.43, **w0.5 = 2.78**, u16 = 0.60, w1.0 = 0.44, w0.25 = 6.08 — the
original's 16-seed "3.6× at matched count" is noise, as the checker found.

Mechanism (measured, via the ablations): the seg failure decomposes into
(i) **endpoint sampling** — force evaluated at the last micro-step but weighted
by the full segment — owns the Jacobi blowup (seg8m fixes Jacobi to 2.5× floor
while leaving rates broken); (ii) the **tick anchor** — segment grid re-origined
at every window exit, pending gap discarded at entry — owns the rate break
(seg8n fixes neither; seg8mn still 90× floor because the entry catch-up kick is
itself endpoint-sampled). The p-variant fixes both plus anchors the grid to the
orbit, and is clean at every K ≥ 4: no subharmonic, no Jacobi walk (P4
re-confirmed for this schedule class), ϖ̇ converging monotonically in K.

Reproduce (deterministic; `work/` holds the CSVs, `machine-state.txt` the load):
```
cd lab/results/20261012-1340-second-20261012-1227-system-8685-2eb1
./reproduce.sh          # ~20-25 min shared 8-vCPU; rebuilds every CSV + tables
./window_clock belt w0.5p8 64   # any single cell, seconds
python3 analyze.py              # tables 1-3 above
```
Bit-compat spot checks: `cmp work/belt64-u64.csv <(…16 seeds)` etc. — see
session log; original cells regenerate with the same binary and commands.

## Predictions

`predictions.md` written before the decisive runs (after 1–2-seed smoke checks
of the machinery only). Scored:

- **PB2 (subharmonic gone at every length): HOLDS** — K ∈ {4,8,16,32}: Δė
  0.11/0.06/0.03/0.01 MADs, Jacobi 1.0× floor; K=2 fails exactly as predicted
  (Δė 259, ϖ̇ +91%: two samples per orbit cannot average the quadrupole's m=2
  harmonic).
- **PB3 (ablations): HOLDS** — seg8m Jacobi 2.5× ≤ 5× with ϖ̇ −78% > 20%; seg8n
  Jacobi 195× > 20×. Unanticipated bonus: seg8mn stays broken (90×) — matched
  sampling must hold at *every* transition, including catch-up kicks.
- **PB4 (no cost win): HOLDS** — uniform u8 carries the belt at 8 k/orb with
  0.04 MADs; no p-variant beats that ratio. The p-result is structure, not cost.
- **PB5 (encounter inversion): HOLDS exactly** — 2.43 vs 2.78 vs 0.60.
- **PB1 (ϖ̇ closes at K=8 ≤ 2%): letter FAILS** — +10.0% at K=8 (1.05 MADs,
  above the 64-seed noise floor); closure arrives one octave later than
  registered: +2.5% at K=16, +0.5% at K=32, ≤ 6.6% at K=8 across the W-sweep.
  Reported as a miss of my own calibration, not of the rebuild.

## What would make it wrong

Same limits as the original replica: static star, prescribed planet, float64,
one perturber, window detection from state rather than predicted from elements.
The K=16/+2.5% and K=32/+0.5% cells sit at 0.26/0.05 MADs — the K-scaling trend
(33→10→2.5→0.5%, consistent across 16/64-seed and W variants) is the evidence,
not any single cell. The window–grid few-percent interaction at K=8 is
unresolved in mechanism (measured, not derived). Many-source shrinkage remains
Fermi-only. A law whose errors live in libration spectra rather than median
rates could reorder the belt conclusions; the resonant scene was not re-run
here (the original's resonant kill stands unchallenged).

## Cost of adoption, and fit with PRINCIPLES

Adopt as a **rule for motion-law v2** (one step): the orbit-averaged secular
term is delivered as one midpoint-sampled kick per fixed mean-longitude segment
(K ≥ 16 for percent-level precession, K ≥ 4 to kill the subharmonic, K = 2
forbidden), conjunction windows layered at fine cadence, no re-origin, no
dropped gaps; tick-anchored quantization of the averaged term is rejected at
every segment length. No new component: the grid is computable from the
elements the scheduler already holds. Principle 14, "no work for no reason, so
no ticks" — the rule is now measured on both sides (tick-anchored aliases at
every length; orbit-anchored is clean). Principle 19, "a fix signals the wrong
representation" — seg8's re-origin and endpoint weighting were fixes for not
asking *where in its orbit* the body is when the averaged kick lands; keying to
phase removes them at a stroke. Principle 4 — the K choice is a number
(harmonic content of the averaged term), not a category.

## The lens

Second-author lens: I inherited the checker's hypothesis and confirmed it, so
independence is limited by construction — the decisive cells were specified
before I ran them (that is the rung's design, but a shared blind spot would
survive). What staring at anchors may have missed: the resonant scene under
p-cadence (a phase-anchored grid could interact with libration in ways the
uniform comparison does not), the many-source case, and whether the engine's
integer sigma-delta quantization changes the K=8 window–grid interaction. The
original's two record inaccuracies (scene correction not in predictions.md;
belt u2048 > 60 s) are not repeated here: predictions precede the decisive runs
and match what ran, and truth jobs are seed-split to ≤ ~4 min each (still not
≤ 60 s on a shared box — noted, not hidden).
