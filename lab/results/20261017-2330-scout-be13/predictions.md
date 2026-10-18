# Predictions (written before the decisive run)

Question: can multipole cells over 10^5-10^6 bodies *produce* the galaxy doll's smooth
Φ program at a fidelity below the disc-churn switch-on (eps_eff ≈ 0.008 relative,
2da8's measured boundary), with a program of ≪ per-body numbers, leaving only the
granularity residual (lumps) for the kick layer?

Cases I did NOT tune on (held out until after the decisive sweep):
1. **Azimuthal truncation.** The disc's Fourier spectrum falls off fast; I predict the
   field error at random test points stays below 0.008 relative for programs keeping
   |m| ≤ m* with m* ≈ 8-16 for a cold exponential disc, and the error at m* grows
   roughly exponentially in m beyond it.
2. **Radial cells.** Log-spaced radial cells: I predict ≥ 32 cells per decade are
   needed for < 0.008; below ~16 per decade the program's own error crosses the bar
   (the kernel is long-ranged in log r, so radial truncation hurts more than azimuthal).
3. **Shot-noise crossover.** The density spectrum flattens where discretisation noise
   (bodies per cell) meets the smooth signal: I predict the crossover sits at
   N_cell ≈ 10^3-10^4 bodies per azimuthal cell, so at 10^9 bodies in ~10^3-10^4 cells
   the program is noise-dominated-free (the smooth half is exact aggregate) while at
   10^5-10^6 bodies the lumps are comparable to the program's own truncation error.
4. **Program size.** Composed at 10^9: total program numbers ≤ 10^5-10^6 (≪ 10^9),
   i.e. ≤ ~8 MB at 64-bit — the field-held-by-cells representation costs no per-body
   bytes at galactic scale.
5. **Kill criterion (pre-registered):** the "cells produce the program" representation
   dies if holding the field below the 0.008 bar requires ≥ ~10^7 program numbers at
   N = 10^6 (≥ 1 number per 10 bodies), OR if the shot-noise crossover needs
   N_cell ≥ 10^5 (so cells ≈ bodies at 10^9 across a 30 kpc disc), OR if the
   program's error cannot be separated from the lumps (truncation and granularity
   residuals of the same size everywhere — then the smooth/kick split is not a
   separation of scales and Julien's "the aggregate is a source" has no cheap read).

## What happened (filled after the runs; numbers from galprogram.out / confirm.out,
## BOTH regenerated after the instrument fixes below)

**Instrument first — my first decisive run was killed by its own harness, twice, and
both bugs were caught by controls, not by theory:**
- **The mask bug (load-bearing).** The density grid dropped every body inside
  r < 0.02 R_d: 4.7% of the clusters scene's mass and ~2% of the smooth scene's,
  N-invariantly. It manufactured the first run's headline "an N-invariant ~1.8% floor
  at every resolution, 2.2x the bar" — that floor was my own mask, not physics. A
  mass-conservation control (grid.sum() vs total mass, now printed by galprogram.py
  as `mass-control ... 1.000000`) caught it; inner bodies now clip into ring 0.
- **The chunk bug.** A memory-saving edit changed the summation chunk *step* but not
  the slice *width*, double-counting every source (~4x forces, med errors jumped to
  0.68-0.76). Caught by the absurd magnitude; step and slice now share one CHUNK.
This is the lab's 5 October lesson lived again (agreement between runs is not
independence when they share a harness): the two "confirming" first runs shared the
mask. Every number below is from the fixed scripts, each rerun at least twice with
identical digits.

**The corrected outcomes:**
1. **m* = 8-16: wrong for the smooth scene, right-shaped for the clustered one.**
   Smooth N = 10^6 at 64x256: m = 2 already at the floor (0.0392) and flat through
   m = 128 (0.0389); m = 0 fails at 0.0443 (arms unmodelled — the control fails as
   it must). Clustered N = 10^6 at 64x256: m still pays all the way (m=0 0.0620 →
   m=2 0.0539 → m=128 0.0114) — clustered sub-cell structure is high-m.
2. **Radial cells: the lever, converging ~h².** With all mass gridded the error falls
   cleanly with the grid (smooth N = 10^6, all m, geometric centring): 64x256 →
   0.0389, 128x512 → 0.0115, 256x1024 → **0.00279 med / 0.0062 p90 — PASSES the
   0.008 bar** (ratios 3.4x, 4.1x per halving: quadratic in cell size). Program at
   the passing grid: ~2.6x10^5 numbers ≈ 2.1 MB at 64-bit.
3. **Shot-noise crossover: wrong — the coarse-grid residual is binning bias, not
   sampling.** Bodies-vs-program at the coarse 64x256 grid: smooth 0.0409 → 0.0389
   (10^5 → 10^6), clusters 0.0136 → 0.0114: N-weak, i.e. the cell's continuum
   quadrature error, killed by grid refinement (per 2), not by bodies. The spectrum
   noise floor does fall with N (2.0e-6 → 2.2e-7): on the clustered scene the arms
   sit at power/noise 2.7x (10^5) → 3.8x (10^6) — sampling-limited there; at 10^9
   the floor drops ~30x further [INFERENCE from the measured N-scaling].
4. **Program size: right.** 2.6x10^5 numbers at the passing grid — free in bytes,
   flat in N.
5. **Kill criterion: did NOT fire after the instrument fix.** The representation
   passes on the smooth two-arm scene at a priced grid. Two extra measured facts:
   dipole (centre-of-mass) centring is WORSE at every grid (0.0532/0.0267/0.0041 vs
   0.0389/0.0115/0.0028 — near cells punish displaced mass; the monopole at the
   geometric centre wins), and the softening couples to the grid: at 256x1024 with
   ε = 0.05 → 0.02 → 0.01 the error goes 0.0041 → 0.0268 → 0.0536 (a finer
   aggregate quantum demands finer cells, ~proportionally).
