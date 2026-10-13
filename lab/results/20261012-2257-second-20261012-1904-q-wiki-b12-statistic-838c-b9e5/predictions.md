# Predictions — 20261012-2257-second-…-b9e5 (second author on 20261012-1904-q-wiki-b12-statistic-838c)

Written before the page edit, the extended verify.sh, and the reproduction scripts.
Already observed while reading (not predictions, recorded for honesty): the six named
runs' grades (c13b, 9c2f, 6cfc, a2a5, 069c, e9f9 all silver); 2f89 silver; 54d9 gold;
the dossiers' headline numbers. The full-branch sweep ran before this file (that is how
the two extra runs were found); its classification is therefore also observation, and
P3 below pins its mechanically re-checkable shape.

- **P1 (the fold's sampled numbers).** Every number I put on the page from the eight
  folded runs (the six checker-named + 2f89 + 54d9) appears verbatim in that run's
  `check.md` or `dossier.md` on its own branch. Tested by the extended verify.sh
  (grep patterns derived from the page text only, against fresh `git show` dumps).
- **P2 (page mechanics after the edit).** 23 run lines (15 + 8), five sections in
  schema order, header intact with `status: open` and `updated:` set to this run, the
  1715 run line kept verbatim, the checker's in-place census sentence replaced by the
  folded one (no dangling "not yet folded in").
- **P3 (sweep shape, re-checkable).** Over all 662 `claude/lab-*` branches, exactly 37
  dossiers mention B12 ≥ 4 times; of those, 15 are already on the prior page, 6 are the
  checker-named runs, 2 are folded by this run (2f89, 54d9 — B12-mechanism content the
  checker's sweep missed), 1 is the 1904 compiler run itself, and 13 are citation-only
  or context (B12 as a broken instrument, a queue item, or a scene borrower); the
  3-mention band (5 runs) is context-only; nothing below 3 mentions is substantive.
- **P4 (069c's record defect, held out).** Its checker says the recorded
  "bounded_jumps 99 bounded, 1 void" does not regenerate (script edited after the run).
  I predict the shipped `b12probe.py short` prints 100/100 bounded at the recorded
  seeds, confirming the record defect named in its check.md.
- **P5 (6cfc's bake-off, held out).** Re-running its shipped `probe_b12stat.py`
  reproduces mean-slope AUC 0.967 > max-slope 0.920 at T=1000 and both ≈ 0.50 at
  T=100, bit-identically (it is seeded).
- **P6 (e9f9's detuned false-alarm kill, independently reproduced — the decisive
  held-out case).** The e9f9 fold's load-bearing claim (the only fast-detection
  candidate dies on physically-native detuning) currently rests on e9f9's checker's
  numbers alone. I reimplement the mechanism from scratch (per-orbit mean of
  A·sin(2πt/(P(1+ε))) fed to a two-sided CUSUM with e9f9's frozen k=0.01, h=0.03391,
  P=1234 ticks/orbit, 200 seeds, 512 orbits) and predict:
  - A=20, ε=1e-3 (A·ε = 0.02 ≳ k): false alarms ≈ 200/200, median alarm orbit ≈ 9
    (the checker's numbers; my independent harness should agree to order of magnitude
    — if it does not, the kill itself is harness-dependent and the page must say so);
  - A=20, ε=1e-4 (A·ε = 0.002 < k): no false alarms (the breaking condition is
    A·ε ≳ k, not amplitude alone);
  - exactly commensurate ε=0 at A=20: no false alarms at any amplitude (the
    tautology the checker named: the per-orbit mean is identically zero).
- **P7 (the census sentence).** After the fold, the refuted-candidate count on the
  page is 14 (11 prior + e9f9's CUSUM-as-frozen + 069c's blocked-F-as-shipped +
  a2a5's VR+trend on the checker's adversarial families), and the live candidates
  each carry a named missing requirement: the observable (9c2f: which element the
  budget lives in; c13b: the matching coordinate), the minimum leak c (e9f9's k),
  the window (6cfc's E[actuations] ≳ 10), the horizon (060f), the per-ship verdict
  (5dcb). If any of these turns out miscounted when verify.sh runs, the sentence is
  wrong, not the count.
