# Predictions — 20261020-2004-spacex-26fc

Written after one smoke arm (stock coast e=2, `logs/stock_coast.txt`) and before the decisive
arms. The smoke arm already answered the attribution question at bench depth: the 2 missing
emitters are fleet ids 1000025/1000047 — handed-out fleet members (bodies 10054/10069,
`from=Some((0,25))`/`(0,47)`) that died at 3,915/6,012 gs; `drop none` = 0 in 120 gathers;
alive-missing = 0. The predictions below are for the arms not yet flown.

- **P1 (attribution extends to depth, held-out):** on the deep burn arm (gather every 300
  frames, ~200k+ game-s), every missing id at every gather is a dead body (handed-out fleet
  member or belt ship that impacted); `alive-missing in 0` gathers, on both keeps. **Kill:** any
  alive id missing at any gather reopens od 2 with a real target.
- **P2 (the clamp fix is a no-op where nothing ails):** `ES_VIEW_CLAMP=1` on the stock coast arm
  changes no statistical line (same seen max/worst/attr, 0 `drop none`, readouts within ±5%) —
  the fix can only act on a crossing `eval → None`, which never happens on this bench.
- **P3 (keep-independence extends to the dead):** the same dead ids (and only dead ids) go
  missing at one leg (`ES_KEEP_LEGS=1`) as at two.
- **P4 (memory at depth):** at deep burn, one-leg halves the retained segments per body vs stock
  (c8d5's checker read 34.8 → 13.9 at 279k gs; I expect the same order, ≥ 30% cut), with the
  gather still complete for alive emitters.
- **P5 (the depth deaths are belt ships):** at deep burn, missing ids beyond the 28 battle
  members include `kind=Ship from=None` bodies (belt impacts), i.e. engine outcomes, not view
  defects.

What would change the adoption story: an alive-missing id at any depth would resurrect the
search-defect reading (od 2); a `drop none` line with `floor` far above `guess` would point at a
cache staleness defect instead of retention.
