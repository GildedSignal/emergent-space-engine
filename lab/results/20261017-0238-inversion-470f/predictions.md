# Predictions (written before the decisive flights)

The question, one sentence: the engine is guaranteed to fail if a battle that stays live turns
every one-time bill (fleet slices, handout tubes, rebind history, catalogue entries) into a rate —
does main's plane do exactly that, at how many kB per surviving member per game-second, and does
the event bill return to baseline once the battle dissolves?

Cases not tuned on: the horizon past the flown ones (every prior flight stops at 5,400–11,000
game-s; I fly to 12,000+ or to dissolution, whichever is later), members 400 (d3fe flew ~150–400
in the fork study; I take 400 and 48 as the shipped default), and the post-dissolution regime
(never reported: every standing number is "while the battle lives").

- **P1 (d3fe's ruin on main):** while the fleet is live, resident RSS grows ~linearly at
  0.05–0.5 kB per surviving member per game-second (d3fe's class, 6 October, pre-merges).
  Kill side: < 0.01 kB/member/game-s sustained over ≥ 2,000 game-s with the fleet live.
- **P2 (4fa8's unflown arm):** the events/game-second while the battle lives is ≥ 10% above the
  post-dissolution baseline at the same N (the one-time slice excess is actually a rate); or it
  is one-time (drops at dissolution and stays down).
- **P3 (saturation):** after dissolution the RSS slope falls below 10% of the live-battle slope
  within one chunk (500 game-s); if it does not, the growth is not the battle's bill but a
  session-long grower — the worse result.
- **P4 (linearity, held out):** the slope fitted on the first 2,000 game-s of the live regime
  predicts total RSS growth at 8,000+ game-s within ±30%. Superlinear (allocator amplification or
  quadratic rebind history) or saturating both fail this.
- **P5 (instrument honesty):** the shipped counters (n_bodies, catalogue_live, bytes_per_body ×
  bodies) account for < 30% of the RSS growth (c304: the dashboard under-reports ~20×); or the
  growth is visible in them (then the fix is a counter away).

Verdict rule: the ruin stands on main only if P1 holds at the shipped members (48) or at 400
through a live battle, AND P3 shows it is battle-coupled. If P1 holds but P3 fails, the grower is
the session, not the battle — reported as such (the worse class). If P1 fails everywhere, d3fe's
ruin is refuted on current main and the direction closes.
