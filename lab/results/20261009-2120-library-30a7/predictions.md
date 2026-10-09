# predictions.md (written before the probe runs)

Bottleneck targeted (board, 5 October): candidate pairs grow as O(N²) at fixed
distribution; candidate work must track real encounters. Board's own "next"
note: a pair's miss distance at successive conjunctions is quasi-periodic, so
its next close conjunction is a Diophantine approximation (continued
fractions), plus group certificates paid once while envelopes are disjoint.
The probe tests the first half of that note — the librarian's version of
"compute only surprises": pay once per element change, not per orbit scan.

## Probe (cf_probe.py), cases not tuned on

Setup: inner circular orbit r1=1; outer eccentric orbit a2 in [1.05,2.0],
e2 in [0.05,0.5], random periapsis; K=600 successive conjunctions; the close
conjunctions are those whose longitude lands near the outer periapsis.
Predictor: continued-fraction convergent denominators q of the mean phase
advance per conjunction (and their small multiples), computed once per pair.

- P1: median over 40 seeds of f_close (fraction of the closest 5% of
  conjunctions within a ±3-index window of a convergent multiple) ≥ 0.8.
- P2: the single closest conjunction index is CF-aligned in ≥ 65% of seeds.
- P3: seeds where α (phase advance / 2π) is within 1e-4 of a rational with
  denominator ≤ 50 (near commensurability) have f_close < 0.5 — the
  degeneration r4 v2 already logged ("detune or use libration amplitude").
- P4: f_close is insensitive to eccentricity: |median(e2 ≤ 0.2) −
  median(e2 ≥ 0.3)| < 0.1 (the beat geometry, not the orbit shape, decides).
- P5 (quotes): every string quoted verbatim in dossier.md is an exact
  substring of the cached Readwise export (readwise-pages/page-*.json).

Failure meaning: P1/P2 failing kills the CF shortcut as the per-pair
predictor for this rung (configuration kill, not method kill); P3 passing
confirms commensurability must be a trigger, not a smooth case.
