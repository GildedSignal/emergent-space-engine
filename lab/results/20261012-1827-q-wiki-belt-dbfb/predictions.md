# Predictions — run 20261012-1827-q-wiki-belt-dbfb (compile `lab/wiki/belt.md`)

Written before the page is written. My decisive act is the compilation, not a new
experiment; these are the claims a checker can falsify.

- **P1 (routing).** Of the 14 clustered runs, 11 belong on the belt page and 3 route
  out entirely: `20261009-0208-redteam-e369` (fleet-doll CW — encounters),
  `20261007-1032-second-…-system-0510-53f6` (conjunction kick form — kick-jet),
  `20261009-1858-second-…-spacex-c6d8-71bd` (bits/binding ledger — memory-h-live).
  `20261010-0352-second-…-spacex-acb2-7b82` stays (its Λ closed-form kill is a
  belt conjunction-rate claim) with its q_v* correction flagged to memory-h-live.
- **P2 (missing runs).** The branch search finds ≥ 4 belt-relevant runs the keyword
  cluster missed, including `20261004-1525-components-98bc` (gold, the birth
  program), `20261005-1404-redteam-b18-belt-d3e4`, `20261006-2240-b-belt-wire-a733`,
  and at least one of {dynamics-04d7, system-5a2c/af34, components-6273}.
- **P3 (traceability).** Every number on the page appears, at the stated precision,
  in the cited run's `check.md` or `dossier.md` on its `claude/lab-<id>` branch;
  `verify_claims.sh` prints each source line and reports 0 missing.
- **P4 (no probe needed).** No two belt runs contradict in a way a cheap experiment
  must decide. The two apparent tensions resolve in the record: 0b04's "the exact
  memo cannot pay" (chaotic (E,L) diffusion below q ≈ range) vs 6baf's phase-lock
  absorbing churn to 0.55 updates/P_p (the *synodic* sweep, derived not chaotic);
  and af34's "≤ 0.6 GB via rebands" vs scout-ab9d's "4.8–5.2 GB at q24" (common-mode
  shear vs real chaotic flybys at a finer quantum). So: compiler, no new experiment.
- **P5 (gaps in the compiled memory-h-live page).** Today's `lab/wiki/memory-h-live.md`
  cites the originals but not the seconds for two of my cluster's corrections:
  fc22-a7d0's planar 209 MB/game (the ≤ 1 MB line holds only in 3-D) and acb2's
  q_v* ≈ 3.8×10⁻⁷·v_K. Both are flagged in my dossier for that topic's next run.
- **P6 (merge).** `wiki.py apply` against base abaf0627 merges my page cleanly (the
  base belt page is an empty placeholder); the dry-run merge-file shows no conflict
  markers.

## What happened

All six held. P1: exactly 11 kept / 3 routed, acb2 cross-flagged. P2: 7 missing
belt-relevant runs found (98bc, d3e4, a733, 04d7, 5a2c, af34, 6273; plus 23c8 via
the compiled memory-h-live page). P3: 62/62 (`verify_claims.sh`; three initial
misses were line-wrap artifacts in my grep patterns, not wrong numbers, plus one
duplicate check — fixed, then 62/62). P4: no probe run; both tensions written into
`## Contradictions` with their in-record resolutions. P5: confirmed — both
memory-h-live gaps flagged in the dossier. P6: merge dry-run exit 0, zero conflict
markers, output identical to the proposed page.
