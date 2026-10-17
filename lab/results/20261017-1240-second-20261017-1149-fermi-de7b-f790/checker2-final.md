Working...
**Grade: gold** — written to `check2.md`. Verification summary:

**Reproduced**
- Runner's `regen.sh` (exit 0): every dossier number matches `regen.log`; author's and runner's regen runs agree byte-for-byte on all 24 `combs:` lines.
- Re-applied `work/patch.diff` to a clean tree, rebuilt, and flew three adversarial cases myself:
  - **Plain `step_log2=4`** (lever 4 had only been seen through the split path): genesis h distribution *bit-identical* to the split arm (112,565/107,003/115,784), 9,700/9,700 welded, identities exact — the split is a pure step lever on the bulk.
  - **Split, seed 42** (author flew seed 1 only): h p50 112,595, all identities 1.0000, 4 events, dead 0.
  - **Split at base lever 6 → effective lever 3** (octave below the tested 4–9 family): h p50 225,130 = 8.0002× lever 6, welded 9,700/9,700, 3 events K,B,K — the family now spans seven octaves, four seeds, both paths.

**Record regeneration** — verified against `remotes/origin/claude/lab-20261017-1149-fermi-de7b`: arm 7/6/8 ladder lines byte-identical to de7b's artifacts, diffs limited to the disclosed instrument extensions; doubles as the toggle-off control.

**Predictions** — mtime 12:45:51 precedes every flight log (12:50+); held including the decisive S2.5 falsifier-absence; the two misses disclosed honestly.

**Ledger** — arithmetic checks by hand (79.71 riding, 15.67 pinned floor, S\* = 19.9×); constants page-cited as disclosed.

**Page** — faithful; no correction needed. Tree restored clean; nothing else in the run folder touched.

Named remaining gaps (in the check): missing `arm7.txt` artifact, unmeasured mixed-belt case inside `BULK_HILL` = 4, and the M1 boundary cost as x86-ratio inference — all disclosed by the author, none load-bearing for the riding-vs-pinned branch structure this run measured.
