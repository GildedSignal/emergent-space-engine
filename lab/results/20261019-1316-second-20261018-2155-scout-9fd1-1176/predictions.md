# predictions.md — 20261019-1316-second-20261018-2155-scout-9fd1-1176

Written BEFORE the decisive grid run, after anchors + flips (the priors below
use those two tables; the grid has not run). The grid is the decisive
experiment: the epoch sim on the shipped tier's own dues (e87d's replica),
kick dial kappa, epoch dial E, time-coupling dial P (opportunities per touch;
belt-real ~2-5, bracketed by 1/4/16).

## Priors in hand (measured, not tuned on the grid)

- ANCHOR: w p50 53,920 ticks; pi p50 7.633e10; k_first p50 8.72e5; per-quantum
  kick: delta_c0 p50 5.5e4 = 1.02 w (e87d's missing constant — the near-phase
  is NOT anchor-protected), delta_d 2.39e4, delta_pi 1.9e4, delta_w ~ 0
  (reproduces e87d).
- FLIPS: dv=0 gives 0 flips at every H (negative control). For H >= 64 the
  flip rate per opportunity is ~1.1-1.4e-6 (~= 2w/pi, fresh-uniform) and
  kappa-INDEPENDENT over 2^-26..2^-14 (512x). At H in {1..16} rates are
  0-3 counts per 200k — consistent with fresh-uniform within noise: no
  protection at small horizons either.

## Pre-registered predictions for the grid

- P1 (controls): dv0 pass: 0 misses at every E; events = pairs with
  k_first <= T*P (~150 at P=4 by ARMED0(8192)~0.3%), all caught by the t=0
  book; noarm: miss fraction exactly 1.000; E=1: 0 misses at all (kappa, P).
- P2 (the E-law — decisive): NO zero-leak knee. At every kappa and P,
  miss_frac(E) ~ 1 - 1/E for E >= 2 (flat in E; e.g. E=2 -> 0.45-0.55,
  E=1024 -> 0.95-1.0), and leak_per_touch(E) ~ event_rate * (1 - 1/E) with
  event_rate ~ P * 1.3e-6 * 0.9. FALSIFIER (the other gold outcome): if
  leak -> 0 below some E, 08d0's knee transfers; its location and kappa
  scaling then become the result.
- P3 (kappa-law): event_rate and leak kappa-independent within +/-30% over
  2^-26, 2^-23, 2^-14 (the boundary flux is saturated at all flown kappa).
- P4 (P-law): events per touch proportional to P (1:4:16 within +/-25%).
- P5 (freeze readout): at belt-real (P=4, quantum), leak_per_touch ~ 4.7e-6
  for E >> 1; in 1a29's units (per candidate per CELL kick: x2/n = 1e-3 on
  the 2000-body cell) ~ 4.7e-9 — >= 100x under the 1e-6 budget at EVERY E.
  The leak budget does not bind: E* is cost-limited, not leak-limited
  (E_pair = 1024 -> E_cell ~ (n/2)*1024 ~ 1e6 cell kicks -> 355-core row to
  ~3.5e-4 cores).
- P6 (held-out): seed 424242 (never run before) reproduces P2-P4 within
  Poisson CI.

## What would make the verdict wrong

- The truth rule "event iff k_t == l <= P" treats the pair's two sections as
  one opportunity clock (both are pj-spaced); if the two sections' passages
  interleave the true rate is up to 2x the measured one (disclosed; the law,
  not the constant, is the claim).
- tau advances by P passages of j's CURRENT period (drifting ~1e-4 relative
  per quantum kick — negligible, disclosed).
- The k=0 fold (first_hit returning 0) never fired on this population
  (k0fold = 0 in anchors) — dead code in practice.
