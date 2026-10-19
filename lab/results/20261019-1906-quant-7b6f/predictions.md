# Predictions (written before the decisive flights)

Scene: shipped `nladder`, K = 10⁵ (and 3×10⁴ for the cross-check), L8 burn, seed 1, rtf 100,
12 ms budget, guard 1,600 MB, probe every 2,000 game-s. Arms: A = shipped loop; B = A +
`ES_SCAN_TTL_S=16` (e181's answer-or-expire fence, reimplemented here, env-gated). Binary:
the run's patch (Linux /proc footprint, print-only census `probe:` lines, the fence). No digit
below was tuned on: the first 10⁵ flight flown in this run is arm A itself.

The question: 3eb3 read the 10⁵ rung's wall as **kick machinery, 5.3–9.9 KB retained per kick**
(by subtraction: rss − base − 2.1 KB×hist). Five independent constants in the record point at a
different channel: the held scans pin ~224 B × candidates each (b77d's law), the interstellar
player's cheap tests pass the whole root doll (~60–95 B/body/scan at 3×10⁴, 7.36 MB/scan at 10⁵
— 527a; ~9 MB per held scan at 10⁵ — e181's slope). 3eb3's subtraction never removed the scan
channel.

- **P1 (the channel).** In arm A, at probes past the interstellar departure, each held scan pins
  ~4–9 MB (scan_cand ≈ root-doll bodies, ×224 B), and the scan channel accounts for ≥ 60% of
  (rss − build_base − Δstore) at the guard. Falsifier: scan_mb < 30% of the residual.
- **P2 (the subtraction reproduces).** Arm A reproduces 3eb3's subtraction reading:
  (rss − base − 2.1 KB×hist_total)/kicks lands at 3–12 KB/kick at the guard — the reading is
  real arithmetic on the wrong channel (kicks and scan mints are wave-coupled, so per-kick and
  per-held-scan are collinear regressors on the same bytes).
- **P3 (the fence arm is flat).** Arm B holds rss slope < 0.05 MB/1k game-s past ~20k gs,
  rss < 850 MB at 60k gs, and the counter identity mints = answered + expired + held holds
  exactly at every probe (answered = encounters-side count; identity checked on mints − expired − held
  vs the answer count's own bookkeeping).
- **P4 (the decisive split — the machinery question).** Define residual(t) = rss − base − Δstore −
  scan_mb in arm B. Its slope per kick is < 0.3 KB/kick (i.e. no retained kick-minted machinery
  beyond the body store's own growth): the "kick machinery wall at 10⁵" reading dies and the
  rung's wall is the scan channel, which has a named, measured fix (byte-capped scans + TTL).
  Falsifier (3eb3 stands): arm B staircases ≥ +1 MB/1k gs with scans expired and store flat.
- **P5 (cross-check at the flightable rung).** At 3×10⁴ burn the fence arm sits in the record's
  band (first-wave history saturation: gt1 ≈ 30k bodies; rss ≈ f80a/e181's fence bands, well
  under the guard), and the shipped arm's decomposition shows the same channel mix as arm A
  with store/hist dominant — matching "bindings ≈ 95% of RSS at 3×10⁴" (3eb3).

What each outcome means: P1+P3+P4 holding kills the kick-machinery reading and makes the 10⁵
rung flightable on shipped code plus the fence (adoption arithmetic in the dossier). P4's
falsifier holding confirms genuine kick machinery and hands the mem job the per-kick byte bill.
