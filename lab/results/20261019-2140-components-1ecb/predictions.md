# Predictions (written before any flight; the code was built, never run)

Scene: shipped `nladder 100000 burn <s> 2000 12`, seed 1, `LADDER_RSS_MB=1600`, `ES_SCAN_CENSUS=1`.
Arms: OFF (shipped record) vs ON (`ES_SCAN_INTERN=1`, the 12-byte interned candidate record).

- **P1 (OFF reproduces the channel):** the OFF arm guard-trips (rss > 1,600 MB) before 45 s of wall,
  at game-s in the 25-45k band, with held scans ~100-250 and summed held candidates ~5-10M —
  7b6f's census (171 scans, 9.85M candidates, 82-100% of the wall) on this box.
- **P2 (ON deletes the wall):** the ON arm flies the full 45 s (≥ 85k game-s) with no guard trip;
  end RSS ≤ 900 MB (scan channel ≤ ~150 MB against the OFF arm's ≥ 1.3 GB), held candidates the
  same order (the record is smaller, not the work), `cand_mb` ≈ cands × 12 B.
- **P3 (identity at a fixed horizon):** on a 12 s (≈ 24k game-s) pair, both arms complete; the
  digest strings are equal. Control: OFF run twice — if OFF ≠ OFF across reruns the digest is
  schedule-elastic and identity falls to the structural argument plus equal encounter counts.
- **P4 (the pool's shape, held-out):** at every ON probe, `pool_live` ≤ ~2× the per-scan candidate
  count (the dedup ceiling: each binding is captured by ~2 successive held scans); `pool_slots`
  (ever) grows past it as bodies rebind.
- **P5 (no cost regression):** ON's p50/p99 frame ms within run-to-run wobble of OFF's (the pool
  is read in idle time; capture pays one lock and a HashMap probe per candidate).

Kill criteria: ON digest ≠ OFF digest at a fixed horizon with OFF stable across reruns (the record
is not answer-identical — dead); or the ON arm guard-trips with cand_mb at the shipped scale (the
intern does not hold — dead).
