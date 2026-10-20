# Predictions — 20261020-1815-library-a2c0 (library)

Written 2026-10-20 ~18:42 UTC, BEFORE compose.py runs. Composition-only run (no flight,
empty patch): every constant is page-cited (nladder.md / library-directions.md lines read
this session); the decisive experiment is compose.py's derivation against 23a6's two
published points (cold and warm), then the 1e9 ledger.

Constants (provenance in compose.py):
- 23a6: cold lump 3.86 µs/body at skip 10.9%; warm 0.041 (best 0.030) µs/body; 41
  belt-wide answers × 99,715 cand, mean skip 97.55%, over a 30,000-gs flight; CAP ALL
  0.267 µs/body (1e5); 3e5 cut at 19.5k gs.
- a0a1: answer read law 4.17–4.5 µs/body; capture ALL-walks 0.25–0.30 µs/body; 2,986 ms
  capture-channel time over 3,107 captures at 1e5; 126 ALL-walks at 3e5 (checker: 125).
- 9ed1: kick rate λ = 4.889e-5 kicks/body/gs (both stagger arms, 1e5).
- 8365: era = 27.9k gs. a31c: era budget 69.75 s (rtf 400); kick comb 12.75 h/era at 1e9;
  boundary comb 2.39 h/era.

## Pre-registered

- P1 (consistency, both sides): 23a6's cold point prices a miss-read at 3.86/(1−0.109) =
  4.33 µs/body — inside a0a1's 4.17–4.5 law within 4%. If it lands > 2× off the law, the
  miss model is wrong and the run keeps only the lump lesson.
- P2 (the named open, closed to a band): under uniform inter-answer gaps (30,000/41 = 732
  gs), the warm point implies the memo's dirty-per-kick ratio δ = miss/(λ·gap) lies in
  [0.05, 0.30] for check costs c_check ∈ [0, 0.03] µs/body (warm mean and best both
  fitted). Letter: δ < 0.5 under every c_check in range. Registered alternative: δ = 1
  (every kick dirties) and the warm answers' effective gaps are 3–5× shorter than uniform
  (clustering) — indistinguishable without the per-answer skip series. Kill: if no
  (δ, c_check) ∈ [0.02, 1] × [0, 0.04] reproduces both points, the memo model is wrong.
- P3 (reading of the page, corrected): 23a6's "mean skip 97.55%" is the 40-warm + 1-cold
  mixture; the warm-only skip implied by 0.041 µs/body is 99.0–99.5%. The mixture
  recomputed from the fitted warm skip and the one cold answer lands within 1 percentage
  point of 97.55%.
- P4 (the 1e9 extension is cadence-bound): at era cadence (one answer per 27.9k gs) the
  memo is 1−e^{−δλ·era} stale = 9–31% (δ band) up to 74% (δ=1), so the single
  warm-at-era answer costs 0.4–1.3 µs/body (δ band) to 3.2 (δ=1) = 390–1,330 s
  (5.6–19× the 69.75 s era budget; 46× at δ=1) — NOT the quoted 41 s. The per-era read
  bill is cadence-invariant (every dirtied body re-read once at the next answer): 414 s
  (δ=0.07) to 1,593 s (δ=0.27), 5.9–22.9× budget (85× at δ=1); closure check: 38
  answers/era × 41 s = 1,558 s must land on the δ≈0.27 branch.
- P5 (the ledger ordering): at 1e9, single doll, one thread: capture ALL-walks 96–180/era
  (96 = upper bound from 2,986 ms/28.9 ms scaled to the era at 1e5; 180 = the counted 126
  at 3e5 over 19.5k gs) × 0.267 µs × 1e9 = 25.6–48.1 ks/era = 7.1–13.4 h = 367–689× the
  era budget, in single 267-s frames ON the player's item; the kick comb 12.75 h (658×);
  the answer channel WITH the bound 0.115–1.64 h/era (≤ 8% of the 20.0–27.8 h/era total).
  The capture walk is 30–50% of the ledger and the bound touches none of it.
- P6 (frame-bust crossover): one ALL-walk busts the 12-ms frame above N = 12 ms/0.267 µs
  = 4.5×10⁴ — below every rung flown; a0a1's measured 28.9 ms walks at 1e5 sit on the
  law at 0.289 µs/body (inside the 0.25–0.30 band).
- P7 (quotes): the five lessons' quotes are byte-identical against a fresh export, 5/5
  by Readwise id (verify_quotes.py); every quote not so verified is marked UNVERIFIED
  and drops its lesson.

## What would make the composition wrong

Any measured per-answer skip series with uniform gaps and warm misses ≫ 3.5% of
candidates (kills δ<0.5 and revives every-kick-dirties at era scale, raising the
answer bill to the δ=1 row only — the ordering in P5 survives); a capture ALL-walk
count that scales with N (kills the 96–180/era premise and the ledger, not the
per-frame law P6).
