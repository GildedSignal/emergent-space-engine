Working...
Check complete. `check.md` written, page corrected in place.

**Grade: silver** — `lab/results/20261017-1447-dynamics-fd35/check.md`

What I did and found:

1. **Reproduced the core.** The runner's regen ran all 18 arm-processes, but regen.sh's summary step dies silently on a relative-path bug (`set -e` misses it behind the `tee`), so I ran `analyze.py` myself: the author's numbers match exactly (45 arms, 8,213 clashes, minD = maxD = 0, fires = 0, posA = 4/13,034; controls 4 vs ~1,300 rollbacks; replicate 1,305/1,326).

2. **Adversarial sweep, all outside the tested domain** — window 32, seeds 33/101, sab=6 + ahead=2.0 at rate 4800, 8 s: every one of 2,393 further clashes at D = 0, 0 fires. vmax 224/320 panic in the scene generator (beyond light speed) — vmax ≤ 160 was already the law's ceiling.

3. **Caught a provenance break the author missed:** the run's only armed lines (the headline "armed episode") come from `matrix/h_128_60`, whose `.out` is in the *old* SUM format — a pre-sabotage build regen.sh cannot rebuild, and regen.sh's `sab 0` argument actually maps to `Some(1)`, so its rerun produces a different scene (rgn0 1600 vs 1) that never arms. I rescued the finding: with sabotage genuinely disabled, the episode regenerates **stronger** — 17 armed publishes to A = 192, several episodes, all resolved by disarm at rb = 0. Corrected the proposed wiki page accordingly.

4. **Named the soundness gap:** the "over-arm, never miss" closure claim is asserted, not proven — rollback's `affected` can include snapshot-sharing siblings outside both lineages.

**One experiment from gold:** reproduce one firing assert on the selfchurn harness and show armed > 0 preceded it (P5), plus fix regen.sh's h-line and path bug.
