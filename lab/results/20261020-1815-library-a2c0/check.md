Grade: silver

**Abstract.** Composition-only, zero flights, and every number regenerates: my independent recomputation of P1–P7 matches `compose.py` byte-for-byte, and `python3 work/compose.py` reproduces the committed output exactly; quotes 5/5 on a fresh export (3 re-verified by direct corpus lookup). δ = 0.065–0.266 closes 23a6's named open to a band; the 41 s forward quote is cadence-bound (warm-at-era 286–1,455 s; per-era bill 295–1,773 s, cadence-invariant); the ledger gains the capture term (7.1–13.4 h/era, 27–67%), revising a31c's "the wall is ONE term" to two comparable terms. Adoption cost: none — holds tier→partition. Gold needs the pinning measurement: the per-answer skip series (possibly already in 23a6's logs) plus the ALL-walk count, whose own legs already show ~N^0.7 growth.

## Reproduction

- `regen.sh` exit 0 (runner) and my own `python3 work/compose.py` run: byte-identical to `work/compose_out.txt`. Every constant re-checked verbatim against the live `lab/wiki/nladder.md` (23a6: 3.86/10.9%/0.041/0.030/41 answers/97.55%; a0a1: 4.17–4.5 law, 28.9 ms, 2,986 ms/3,107, 126-vs-125 kept as a band; 9ed1 λ; 8365 era; a31c 69.75 s, 12.75 h, 2.39 h). Every dossier number P1–P7 regenerated in a separate script of my own — all match, including the 0.5% closure (38×41 = 1,563 s vs the δ=0.266 branch 1,571 s).
- Quotes: fresh 770-doc/4,590-highlight fetch, 5/5; I confirmed 3 of 5 ids by direct JSON lookup of the fetched corpus (fragment-exact, correct title/author).
- Read-only run confirmed: `work/patch.diff` empty, disclosed, nothing outside the run folder.

## Predictions

`predictions.md` mtime 18:22:37 precedes `compose.py` 18:23:09 — pre-registration stands. (The dossier says "18:42 UTC"; the mtime is 18:22 — a typo, immaterial to the ordering.) P1 (4.33 in law), P2 (δ < 0.5, band 0.065–0.266), P3 (0.65 pp), P7 (5/5) held. P4/P5 held in substance with disclosed letter-widenings; no kill bar fired.

## Record defects (numbers regenerate; labels wrong)

1. `compose.py:54` hardcodes `d_lo, d_hi = 0.05, 0.30` commented "fitted band across the four corners" — the four fitted corners give [0.065, 0.266]; [0.05, 0.30] is the pre-registered band. The dossier's explanation ("the fitted δ band reached its corners 0.05/0.30") repeats the mislabel. Effect is conservative: P4/P5 bands are wider than the fit supports, so both conclusions ("never 41 s", "answer ≤ 2.5%") only strengthen under the fitted band.
2. "Below every flown rung" (P6, and the page): the crossover is N > 4.49×10⁴, but 3e3 was flown (23a6, a0a1's checker) and sits below it. The claim holds for the ≥1e5 rungs; at 3e3 one walk costs ~0.8 ms.

## Adversarial cases (four, all run)

1. **δ = 1 (the registered alternative):** answer reads 5,909 s = 1.64 h/era — still the smallest term against kick 12.75 h and capture 7.1–13.4 h. The ledger ordering survives, as the dossier claims.
2. **The degenerate c_check corner:** the δ fit assumes the memo-check cost c_check ≤ 0.02–0.03 µs/body (a judgment, not a measurement). Pushing c_check up: 0.030 → era answer 400 s (busts); 0.035 → 223 s (busts); 0.0405 → 19 s (fits the budget — the only regime where 23a6's 41 s sentence stands, requiring kicks to essentially never dirty the memo, contradicting 23a6's own stated miss premise). The per-era bill at flight cadence is 38×41 = 1,563 s under every split. Conclusion robust in practice; the assumption should have been named as load-bearing.
3. **Capture-walk count vs N (outside the tested domain, from the run's own inputs):** the two legs are 96/era at 1e5 (upper bound) and 180/era at 3e5 (counted); a0a1's checker counted 86 walks/30k gs = 80/era at 1e5 seed 2. Counted-vs-counted, the walk *rate* grows 2.25× across a 3× rung ≈ N^0.74. If that trend holds toward 1e9 the capture term is ~5,400 h/era, ~200× the quoted band — the ledger's absolute numbers (20.0–26.6 h/era, 27–67%) are a floor conditional on N-flat counts. The author registered the premise as a kill condition but did not flag that the growth is already visible inside the band's own legs. Every direction of breakage raises the capture share and strengthens tier-first, so the adopt-order conclusion is safe.
4. **λ consistency:** 8365's payload (one kick comb per body per 27.9k-gs era) implies λ = 3.58e-5 against 9ed1's measured 4.889e-5 (1.37×). Harmless here — the bills pin only the product δ·λ, which the warm point fixes directly — but the run quotes both constants without noticing the tension.

## Novelty

Searched `docs/HISTORY.md` (no prior invalidation-rate work) and the wiki: the invalidation rate is 23a6's explicitly named open ("unmeasured directly"); a31c's ledger had no capture-walk term ("after the boundary comb is deleted, the 1e9 era wall is ONE term"); b57f priced the answer walk without the bound (60–63×). The δ band, the cadence-invariance argument, and the capture share (revising a31c's one-term sentence to two) are new. Not a repetition.

## Goal fit

Board #1 (28 → 10⁹). It deletes a would-be freeze — no window on bound tuning as a 1e9 lever (≤ 2.5% of the ledger) — and corrects a pending forward-quote before it hardens. PRINCIPLES 1 ("the cheapest compute is compute not done") and 3 ("Compute only surprises. Cost follows change and entropy" — the answer bill is the kick stream priced at the read). The page fold is faithful; every number in the new paragraph matches the evidence (checker line appended with the three corrections above).

## Why silver, not gold

Real and reproduced, but no measurement of its own: the central constant δ is a two-parameter fit on two points with an assumed c_check ceiling and one live degenerate alternative, and the pinning instrument was named but not flown. The ledger's newest term (capture 27–67%) rests on an N-flat walk-count premise whose trend its own legs contradict. It re-prices and re-ranks around existing constants; it does not itself move a bottleneck by 10× or delete a component.

**The one experiment for gold:** pin δ and the walk count. (a) The per-answer skip series: 23a6's instrument already counted 4.1×10⁶ bound decisions — if per-answer skips exist in its run artifacts (its own branch), δ is pinned by a log read, zero flights; else one flight with `ES_CARRY_BOUND` + skip-series logging decides uniform-gap δ vs the clustered-gap branch (mean warm miss vs λ·gap). (b) The ALL-walks-per-era count at 1e5 vs 3e5 (both possibly countable from a0a1/23a6 artifacts) fixes the capture term's N-scaling. With δ pinned and the count trend measured, this becomes a gold composition: the 41-s sentence's fate, and the ledger's true capture share, decided on evidence.

## What the author missed

1. The N-growth of the capture-walk rate is already measurable inside the run's own two legs (N^0.74) — treated as bound uncertainty, not as the trend it is; the absolute ledger should be quoted as conditional on N-flat counts.
2. The c_check ceiling is load-bearing and unmeasured; its degenerate corner (δ→0) is the one world where 23a6's sentence survives at era cadence. The cheapest rebuttal — reading 23a6's existing per-answer skip counts — is cheaper than the named "one flight" and was not attempted.
3. The λ tension (8365 vs 9ed1, 1.37×), harmless to the bills but worth a line since both constants are quoted.
4. "Byte-identical" quotes are substring-exact (the lesson quote is a fragment of the longer highlight) — same convention as a31c, but the wording overstates.
