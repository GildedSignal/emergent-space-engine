# Folder map (for the checker)

- regen.sh — regenerates every dossier number (build + 9 flights + analysis, ~10 min).
- predictions.md — written after the 3e3 calibration pair, before every 1e5/3e5 flight.
- dossier.md — the record.
- wiki/nladder.md — the page with this run folded in.
- work/patch.diff — the run's whole patch (bound + instrument + fence + cut mode), applied by the runner.
- work/analyze.sh — the per-arm anatomy analysis regen.sh calls.
- Flights: w1/w2/w3 (wall anatomy), e1/e2 (OFF determinism control), e3 (ON 1e5 cut), e4/e5 (3e5 pair),
  d5 (verify control). Superseded/diagnostic arms kept for the harness-leak diagnosis: d0/d1 (3e3
  calibration pair), d1_*/d2_* (first, confounded 1e5 pair), d1r (the OFF repeat that exposed the leak),
  d3/d4 (16.5k cut — pre-ALL, before the burn-tick fix), d3b/d4b (19.5k, burn-tick leak still present),
  s_off/s_on (3e3 smoke). w3_rss_watch.txt is empty (the ps watch never matched; W3's memory is read
  from the ladder line's foot_end_mb).
