# Predictions (c304, second author on spacex-3463)

Written before the decisive runs. The checker's named experiment: separate the construction-spill
regime from battle churn, and decide whether the ~400 kB–5 MB per-handout growth is retained state
or allocator transients, so the true steady-state marginal (17–60 kB vs ~330 kB) that the 20,000×
idiot index is computed from is fixed.

Seen before writing (disclosed): m4/m48 S=8 digest reproduction (both match the author), and one
S=1 instrument-tuning smoke of the `--gap 2000` lever at m4000 (kicks=0 battle-wise, slices=1,
leavers stream; the smoke showed `live_kb` tracking `rss_kb` within ~15%, with d_live bursts
starting exactly where ship kicks/encounter counters start, and `hist` struct bytes far below the
gap — hence the retired-segment trajectory charge added to the account). Nothing at S=8, no
m40000, no seed 2, no trim result has been seen.

## The arms (all `xtask universe --bench --rtf 100 --unpaced --seed S --members N [--gap G]`, release, shared box)

- **A (churn)**: `--members 4000 --seconds 8 --seed 1` — the author's headline run.
- **B (no battle, same N)**: `--members 4000 --gap 2000 --seconds 8 --seed 1` — the gap puts every
  member outside the frame's extent rule (4,740q/32 ≈ 148q) at genesis: ~4,000 construction
  handouts at the first slice, the frame dissolves, no battle ever runs.
- **C (10× N, stock)**: `--members 40000 --seconds 8 --seed 1` — the author's undisclosed run,
  now reported; a 1.7 GB guard aborts if the box cap is approached.
- **D**: A and B at `--seed 2 --seconds 4` (behaviour over seeds).

## Held-out predictions

1. **Retained, not transients (the decisive half).** In A, the counting allocator's live bytes
   track the RSS within ~25% through the run, and end-of-run `malloc_trim` returns < 30% of the
   resident set. The honest account (current trajectories + retired history trajectories + plans)
   explains ≥ 60% of the live growth.
2. **The marginal tracks the leaver's history, not N.** B's per-handout Δrss over the burst stays
   ≤ 60 kB/handout — at least 5× below A's late marginal — and B's final RSS is < half of A's
   despite ~2× more handouts resolved.
3. **The growth in A is per rebind, and it keeps growing while ships kick:** A's d_rss per
   handout rises ≥ 10× between the first 500 handouts and the last 500, tracking the kick count,
   not the body count alone (body count alone cannot explain it: ~2.3–4k bodies × any per-body
   constant < 150 MB even at 40 kB/body).
4. **C stays in the construction regime** (presented tick ≪ the fleets' meeting tick): flat
   ≤ 60 kB/handout through ≥ 12,000 handouts, final RSS within ±30% of the author's 241 MB file,
   guard not hit; kicks ≈ 0, dissolved early or never.
5. **The instrument lie is confirmed measured:** honest per-body bytes (current + history share)
   ≥ 15× the dashboard's `bytes_per_body` at A's end (the flat-4096 Passage charge plus uncharged
   history trajectories).
6. **Seed 2 keeps the orders** (D): same signs, marginals within 3×.

## What would falsify the corrected claim

- B's marginal ≈ A's late marginal (then body count, not churn/rebinds, sets the marginal).
- live_kb flat while rss climbs, or trim frees most of the peak (then transients dominate; the
   steady-state marginal is the construction one and the idiot index drops to ~10³).
- C blows past the guard while still kicks ≈ 0 (then construction itself superlinear at 10× N).
