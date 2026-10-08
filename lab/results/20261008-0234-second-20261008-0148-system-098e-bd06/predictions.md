# Predictions (written before the toy2 / smear_wide / bench runs)

Tuning state: the author's record (toy_news c30/c300/per, smear) has already
reproduced bit-identically in this folder — that part is not a prediction.
Everything below is decided before running toy2.py (the second-order exact
reference, the integer lag table, the two gate configs), smear_wide.py and
bench.py. I have read the checker's numbers for the gate configs but not run
them on the shipped mechanism.

## 1. Second-order exact reference (the instrument fix)

- c30 (16 seeds, 12 yr): exact(2nd-order arrival) vs cell stays within
  [1e-10, 3e-8] max |da|/a — the published 9.4e-9 was not an artifact of the
  first-order arrival. If it jumps above 1e-6, the record was an instrument
  artifact and the claim is refuted at its current strength.
- Laplace control still separates >= 1e4x from exact-vs-cell at c30.

## 2. The integer lag table (the shipped mechanism, cellint)

- c30: exact(2nd) vs cellint max |da|/a < 1e-7 (quantization adds <= one
  lattice time unit W0/c ~ 1e-3 yr of lateness on top of the geometric smear;
  response error is second order in the event, so same family as cell).
  Kill: > 1e-6 means the integer table is not behaviour-neutral — design fails.
- c300: < 5e-9 (scales ~1/c).
- per (periodic stress): < 5e-6.
- never_early holds for cellint everywhere (ceil + arrival-time cell).

## 3. The regime gates, on the shipped mechanism

- c3 (beta_source = 0.33): exact vs cellint >= 5e-7 — crosses the 1e-6
  family; the beta gate the design needs carries to the integer table.
- near (a0 = 1.15, ~2-3 cell widths): exact vs cellint >= 3e-7, laplace
  control explodes (>> 1e-5) while exact vs cell(int) stays below 1e-5 —
  the separation gate (exact pair layer below ~4 widths) carries.

## 4. Full-doll smear (both units)

- Lateness in SOURCE-cell crossings is unbounded on the full doll: max > 20
  (the dossier's 'at every separation' was a sampling artifact).
- In LARGER-cell crossings: med ~1.3, max <= 3.6 — the corrected invariant
  'never early; late by <= ~3 larger-cell light-crossings, independent of
  distance' holds at every separation. Kill: max > 5.
- Same-ring diametric pairs: ~2.0 larger-cell crossings.

## 5. Measured control (bench)

- tests/kick ratio ~ N/CELLS = 83x at 2^20, 662x at 2^23 (measured ops + ms,
  matching the author's arithmetic).
- state ratio 21x / 165x EXCLUDING the shared lag table; ~13x / ~100x
  INCLUDING it (int16 table, 2.5 MB, one per doll, c-independent).
