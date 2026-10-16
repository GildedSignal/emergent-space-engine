# Predictions (written before the decisive runs)

The component: the player-scan candidate set (`PlayerNeighbourhood::capture` + `radial.rs`).
The question: how many bodies the finder READS per scan against how many it must read by
right (the true hits and their margin), on shipped flights. The runs: `nladder {0,1000,100000} burn 20`
and `nladder 1000 coast 20`, census patch print-only (`ES_SCAN_CENSUS=1`), seed 1 (the ladder's own).

Cases I have NOT tuned on (the ladder's published table gave me frame times only, never scan
internals; nothing below was measured by me before this file):

- P1 (the plane's own doll, N=0/1000 burn, player near Home until 15.8 s): the radial filter
  passes most of the doll — read fraction > 50% — because Home's doll is radially compact
  (locals at 5,200–166,000 root units vs the Moon's orbit). Hits per scan = 0; nearest
  non-hit miss > 10² × reach.
- P2 (the root doll, from 15.8 s, N=10⁵ burn, player at ~1 AU, belt at 2–3 AU): the
  window [r ± (|v_a|+|v_b|)·h] covers the belt, so the filter falls back to (nearly) every
  body: read fraction of the doll > 90%. If instead h (the player's step) is small enough
  that 1 AU of radial slack is not covered, read fraction < 1% and P2 FAILS — then the
  seam is not the finder and the dossier says so.
- P3 (emptiness of the kept set): in the root doll, hits = 0 and the nearest non-hit
  candidate stays > 10³ × reach away over the interval (the belt is 1 AU off and the
  interval is a fraction of an orbit): the kept set is empty by three orders, so a second
  (angular/phase) certificate on the key has ≥ 10³ of slack to cut with.
- P4 (the price of a read): the answer half costs 1–4 µs per read candidate (a cartesian
  readout per body), matching scan-queue's s = 1.7–4.2 µs/body; capture's cheap half
  (filter + clone) is ≤ 0.2 µs per body of the doll.

Kill criteria for the premise: P2's failure clause above; or hits-per-scan ≥ 1% of reads
(the kept set is genuinely dense — then no certificate can cut and the cost is honest).
Timing runs are Linux/x86 shared: orders of magnitude only; counts are exact integers.
