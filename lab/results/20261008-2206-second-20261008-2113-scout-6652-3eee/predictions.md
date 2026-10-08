# predictions.md — run 20261008-2206-second-20261008-2113-scout-6652-3eee
# (written BEFORE the decisive run; a smoke test at NP=3 per family fixed the
# instruments and revealed the F3x alias hole and the F5 width scale — those
# findings are above; the numbers below are pre-registered for the full run)

Question: does the travel-time-difference window, with the two soundness holes
closed (sweep-extended pooled-range admissibility; alias completion over the
passage lattice), decide Wide sections with zero misses at >= 10x lower wall cost
than the crate's numeric window, on the checker's named families (F3x high-e,
F5 wide-crossing) plus the original's regression families (F1, F2, F4)?

Held-out predictions (not tuned on; full run, fresh sections beyond the smoke):

- P1 (soundness, load-bearing): missB3 = 0 and bad_route = 0 on ALL five families
  against the certified truth (fires with D < rho; unresolved windows carry the
  disclosed floor D >= rho - Sigma*t_cap/2 ~ 0.955*rho, so any fire >= 4.5% deep is
  provably detected). Any missB3 > 0 or bad_route > 0 kills this configuration.
- P2 (F3x, the checker's kill): all sections get windows (routes-out ~ 0, vs the
  original's 6/6 routed with 3 false); width ratio median <= 5x (smoke section 0:
  1.67x); evalsA ~ 600-3000 vs evalsB3 ~ 60-120.
- P3 (F5, the unmeasured half): zero misses, but width ratio 20-100x (sound and
  fat: the along-track sweep tolerance is the wrong certificate at transversal
  crossings, where the crate's linear cross_window geometry is tight). Count ratio
  ~ 6-8x; wall ratio >= 15x.
- P4 (census): under the uniform-du tangency law, wide-crossing is 40-50% of Wide
  sections (not a corner case); median e_max ~ 0.15 on both Wide halves.
- P5 (wall clock): per-call ratio mean_at_longitude/state_at_mean ~ 2.5-4.5x
  (smoke: 3.64x); end-to-end per-section wall ratio median >= 10x on every family
  (smoke: 18-68x). If the F1/F3x median wall ratio lands < 10x, the "91% tail at
  >= 10x" claim dies and only the count ratio stands.
- P6 (regression): F1 width ~ 2.5-3.5x (sound margins vs the original's 2.57x);
  F2 ~ 5-8x; F4 no noradial routes; evalsB3 median 60-110 everywhere.

Kill criteria (pre-registered): P1 violated anywhere -> the margined certificate
is unsound, KILL as a replacement (and the original's method stays dead as built).
Median wall ratio < 10x on F1 or F3x -> drop the 10x claim, keep counts. F5 width
> 100x median -> the h-window is routing-only on wide-crossing arcs.

Expected mechanism checks: A (the numeric window) misses zero on all families
(replica fidelity); fires cluster inside B3's hull with the alias structure
visible on F3x (components ~ 2-4 per section before hull).
