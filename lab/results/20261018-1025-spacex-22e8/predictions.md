# Predictions (written before the decisive runs)

Runs: `orbitbytes <N> <coast|burn> <s> 100` — the ladder's own flight loop, N extras, seed 1,
single thread. The instrument: print-only census (`binding_at` clones split current/history,
`decode` knot evaluations attributed to the last body served) + a byte anatomy walk
(record / plan / compiled knots / entry / Arc / retired history, deep, Arc-sharing aware).
The wave of the belt's first kicks is at 13,051–14,534 game-s; 20 s at rtf 100 ≈ 2,000 game-s,
so these flights end before it by design (the belt's reads are measured in its quiet phase).

- **P1 (the cache with no reader):** over the engine flight at N=10⁴ coast, the fraction of
  belt bodies whose compiled orbit is ever decoded (`decode` attributed to the body) is < 1%;
  engine `decodes` concentrate on the planets, the moon, the locals and the player's near set.
- **P2 (the retired binding is read ~never by the engine):** engine `bind_hist` < 5% of
  `bind_cur`; belt bodies cloned from history: 0.
- **P3 (anatomy):** compiled knots are ≥ 50% of a belt body's held bytes at birth; the deep
  sum (record+plan+entry+arc+knots+history deep) per body is within ±15% of the ladder's
  process-level 2.4–2.6 kB/B at 10⁴.
- **P4 (the kick doubles by retention, not by sharing):** after the flight, kicked ladder
  bodies (the locals) hold ≥ 1 retired binding each with `hist_shared` = 0 (every retired
  orbit is its own allocation), so a kicked body's total ≈ 2× an unkicked one's.
- **P5 (the recompile price):** `Orbit::compile` from the key costs 3–10 µs; at P1's measured
  engine read rate the lazy-compile bill for the belt is < 1 ms per game-second at 10⁴.
- **Held-out arms:** the burn at L8 (12 s, N=10⁴) and N=10³ coast: P1/P2 hold within a factor
  2 on the decode rate (the player's own doll changes; the belt stays unread).

Kill criteria: P1 false (belt decoded at per-frame rates) kills "lazy compile is free";
P4 false (histories shared or empty) kills the "retention doubles bytes" reading of ladder
break 2.
