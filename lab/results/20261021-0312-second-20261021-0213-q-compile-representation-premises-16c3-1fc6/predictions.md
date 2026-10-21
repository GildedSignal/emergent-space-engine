# Predictions — registered before any replay or publish ran

The 16c3 checker's named step to gold: land the dedup-preserving publish path
(6ccc's `fold_runs` patch on `lab/wiki.py`, checker-verified by 691b), resolve
the standing 16c3/901c conflict, then publish through a **real** `wiki.py
apply` — the index row must read the true distinct run count, not a scratch
overlay. Both colliding runs started from base `046d8d9c`; the committed page
(HEAD `fa431e16`) carries 2 marker blocks, 64 run bullets for 18 distinct ids,
285 lines. All predictions are falsifiable; kill criteria under each.

- **P1 (the accident reproduces from shipped code).** Replaying the two
  publishes in the publisher's order (`16c3` before `901c`, alphabetical),
  base `046d8d9c`, through the **shipped** `wiki.py` (sandbox copy, inputs
  from the two run branches) reproduces the committed page byte-for-byte:
  285 lines, 64 bullets / 18 distinct, exactly 2 `<<<<<<<` blocks, and the
  index flags `conflict to resolve` with run count 64.
  *Kill:* any byte diff beyond nothing → my model of the publish order or the
  shipped merge is wrong; I report the artifact and do not publish a wrong
  story.
- **P2 (the patch removes the amplifier and the marker leak).** The same
  replay through the **patched** `wiki.py` lands no marker line (conflicts
  render as labeled versions), and `## Runs` folds to 18 distinct id-keyed
  lines (no 63+1 union). The body still carries both versions unresolved —
  the patch keeps conflicts visible for the next run; it does not resolve
  content.
- **P3 (idempotence).** Re-running the patched `apply` over the same two runs
  changes nothing (the already-folded guard skips both).
- **P4 (the decisive publish).** With `fold_runs` landed on `lab/wiki.py` and
  the conflict resolved by hand into `lab/wiki/representation-premises.md`
  (16c3's verified 75-line compile + 901c's kink-law result folded in), a real
  `python3 lab/wiki.py apply` publish of this run's proposal yields:
  index row `representation-premises | open | 19`, **no** conflict flag and
  **no** over-budget flag; page 19 bullets / 19 distinct ids, 0 markers,
  Current best ≤ 15 non-empty lines, page ≤ 300 lines. (19 = 16c3's 17
  branch-true runs + 901c gold + this run; the checker's "17" predates 901c's
  simultaneous landing.)
  *Kill:* any flag, or bullets ≠ distinct ≠ 19 → the landed path does not
  preserve the dedup → the adoption claim is refuted and I report that.
- **P5 (no loss across the resolution).** The resolved page loses no numeric
  token against 16c3's side (0 missing, by construction it is that page plus
  additions) and none against 901c's body sections; tokens appearing only in
  stale run-line variants are listed and each traced to the final line that
  carries its claim.
- **P6 (negative control).** Deleting one load-bearing number from the
  resolved page makes the no-loss check report it MISSING and FAIL (the check
  can fail).

Time cost: all steps are sub-second file operations; nothing here touches the
crates, the gates or `main` (the tree edits land in `work/patch.diff`, which
`run.sh` saves and reverts).
