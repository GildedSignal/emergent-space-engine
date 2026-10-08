# Predictions (written before the decisive runs)

Tuned on ONE case only: c=30, impulsive, 3 seeds, 8 yr (smoke). Everything
below is held out: 16 seeds (worst included), 12 yr, c=300, the periodic
stress, and the smear/cost tables.

## Behaviour toy (`toy_news.py`, cell = max-distance lag, never early)

1. **c=30, impulsive dv=0.03 at t=5, 16 seeds, 12 yr:** exact vs cell
   max |da|/a < 1e-7 and max |de| < 5e-6 over the whole window and all seeds.
2. **c=300 (10x smaller delays), same scene:** exact vs cell max |da|/a < 2e-8
   (arrival error scales 1/c).
3. **Laplace control (retarded position, no tube) must fail:** its excess
   |da|/a over exact >= 1e-5 at c=30 by 12 yr, i.e. >= 10x the exact-vs-cell
   error at every c. If it does not separate, the instrument is too weak and
   the run is silver at best.
4. **Periodic stress (200 dv=+-5e-4 every 0.01 yr, period ~ smear, c=30):**
   exact vs cell max |da|/a < 5e-6; no resonant blow-up (alternating dv bounds
   the response). Held-out because it is the natural kill case for quantized
   timing: many events at the quantization timescale.
5. **Arrival deltas (exact - cell) all <= 0** (never early), |delta| <= ~4e-3 yr
   at c=30 (the smear: cell diameter / c).
6. **The plane today (instant) vs exact** differs by >= 10x more than exact vs
   cell at c=30: the quantization error is second order against the full
   light-travel delay the plane currently ignores.

## Smear geometry (`smear.py`, rings m=16, 128 spokes)

7. Relative smear (max-min)/min distance between cell pairs falls below ~10%
   beyond ~3-4 cell widths of separation and below ~2% beyond ~10; at 1-2
   cells it is O(1) -> the exact pair layer must own near encounters.

## Cost counts (analytic, belt scene: 0.7-50 AU doll, ~99 rings x 128 spokes
= ~1.26e4 cells; S = 10 sources; version-ring depth 4)

8. Per-pair cursors (the queued build's design): N*S state words and N*S
   integer tests per kick. Cell-owned rings: ~cells*S*D words, ~cells*S tests
   per epoch. At N = 2^20: >= 15x less state, >= 50x fewer tests; at 2^23:
   >= 100x / >= 300x.
