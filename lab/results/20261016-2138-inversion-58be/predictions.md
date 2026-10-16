# Predictions (written before the decisive long arms)

The question: does the merged plane's per-body memory stock stay at the letter's plateau
(4.85–5.06 kB/B, the constant behind the 1.2–1.65×10⁶ memory wall) over a playing horizon,
or does it grow with play? Tuning runs seen so far (not decisive): N=0 for 2,899 game-s
(rss 3.7→9.3 MB, catalogue 28→76), N=10³ for 19,899 game-s (flat 12.7→12.9 MB after
~1,500 game-s; catalogue saturates at 1,076; dashboard 1,675 B/body against truth 10,125).

Held-out arms (not yet run): N=10⁵ coast to 100,000 game-s (crosses the belt's first kick
wave at ~13–14.5k game-s and the second at ~73–74k); N=10⁴ coast to 100,000 game-s; the
battle-live arm (fleet 400 members, N=10³, 40,000 game-s).

- **P1 (the plateau holds):** at N=10⁵, past the first wave, truth B/body stays within
  ±10% of its post-wave value through 100,000 game-s and across the second wave; the
  post-wave plateau lands at 5.1–5.5 kB/B (letter: 4.85–5.06 measured on the M1; Linux
  allocator may sit slightly higher).
- **P2 (catalogue):** `catalogue_live` saturates — no per-kick churn; after the first wave
  it changes by < 1% of `bodies` per 10,000 game-s.
- **P3 (battle-live, d3fe's channel):** with 400 members the battle lives longer than the
  48-member one; if attrition completes within the horizon, memory after dissolution is
  flat. If a live battle still stands at 40,000 game-s, I expect visible growth (d3fe's
  ~0.2 kB per surviving member per game-s would be tens of MB); either outcome reported.
- **P4 (fixed churn):** the N=0-class fixed memory (battle, locals, arenas) saturates by
  ~5,000 game-s under 10 MB absolute at every N (no unbounded grower without a live battle).
- **P5 (the dashboard is not the instrument):** `bytes_per_body` under-reports truth RSS
  by ≥ 3× at every N (c304's class), so the letter must cite the footprint, not the dashboard.

**Kill criterion for the letter (pre-registered):** any arm whose truth B/body grows
monotonically past the first wave with slope > +0.1 kB/B per 10,000 game-s. At the page's
rtf 100 that slope runs ×36 over Julien's one-hour play budget, and the 1.2–1.65×10⁶ wall
computed from a static plateau is then unsound. A control that cannot pass: N=10³ past
20,000 game-s already shows flatness, so a leak found only at 10⁵ must scale with N to be
real (I will check the N-dependence before claiming).
