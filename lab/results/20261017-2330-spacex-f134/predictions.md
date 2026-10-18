# Predictions — 20261017-2330-spacex-f134 (spacex)

Written BEFORE the decisive composed flight (`both5400`). All flights N=1000 coast, rtf 100,
budget-free (budget 1e6 ms), seed 1, seed fixed by the harness; the arming controls (OFF,
SECULAR, CHAIN+STAGGER) must first reproduce the page's record numbers before `both5400` counts.

## Arming controls (must reproduce, else VOID)

- OFF 5,400 game-s: max events/frame ≈ 334 class, p99 ≈ 136; ledger events ≈ 22,219, kicks ≈ 9,217.
- SECULAR 5,400 game-s: max ≈ 131, p99 ≈ 26; events ≈ 6,580, kicks ≈ 1,382; residual beat at
  frame ≈ 3,173 (the spared standing set's comb).
- CHAIN+STAGGER 5,400 game-s: max ≈ 52, p99 ≈ 24; a one-time slice bill (≈ +20% total events
  early, events/game-s ≈ 3.16-3.17 past 1,900 s).

## The decisive arm: BOTH (ES_SECULAR + ES_CHAIN + ES_LOCAL_STAGGER)

- **P1 (the storm):** max events/frame < 52 (below the chain-alone floor class), p99 ≤ 26.
  Rationale: the delete removes ~86% of the doll population whose shared tick made the comb;
  the spared quarter's standing set (SECULAR's residual 131-beat at frame 3173) is exactly the
  population chain must de-phase, and no prior arm de-phased it (SECULAR alone leaves it locked).
  Kill: max > 131 (worse than delete alone) or p99 > 30 → the composition interferes (a
  re-phased spared set re-locks onto a new beat); report as composed-not-cheapest.
- **P2 (the ledger):** total events ≤ 7,500 and kicks ≤ 1,600 (at or under SECULAR's ledger;
  chain re-times events but adds no steady rate; the stagger's slice bill is slices, not events).
  Kill: events > 22,219's half (11,110) → the composition re-minted the comb's events.
- **P3 (N-flat):** BOTH at N=0 within the 51-class floor (max ≤ 55); at N=10⁴ max within 2× of
  N=1000's (the collapse is not N-bound).
- **P4 (wall, order of magnitude only):** engine p50 ≤ the OFF arm's p50 (no arm adds per-frame
  work; the ledger is cut).

## Held-out (not tuned on)

- N=0 and N=10⁴ under BOTH (the page's N-flat question for the composed arm).
- The digest identity control: patched-OFF vs the frozen record (13 cases × 4 schedules) —
  must be bit-identical or the composition's inertness claim is void.
