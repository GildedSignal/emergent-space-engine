Working...
Check complete. **Grade: silver** — written to `lab/results/20261012-1827-q-wiki-encounters-e8e3/check.md`.

**What held (reproduced independently):**
- `regen.sh` passes in 0.34 s from a foreign cwd; partition 65 = 51 page + 9 routed + 5 no-record.
- All 51 page grades match their branch `check.md` (my own `git show` re-derivation, not just the author's script); 9/9 routed grades match the dossier; dead branches and VOID rungs confirmed.
- 12 in-text claim samples of my own — disjoint from the author's 6, spread across Current best and Refuted — every number verbatim in its cited run. `88ee`'s "66/495" correctly lives in `8716`, which the line cites first.
- `predictions.md` (18:33:03) precedes the page (18:36:41); zero overlap with the `coorbital-cert` page; the placeholder in `lab/wiki/` confirms this is the topic's first fill; run lines all ≤ 20 words.

**The attack that bit (outside-range, per the author prompt's own warning to search refs):** the Runs list omits graded on-topic runs outside the integrator's cluster — `20261006-0030-rung-r8-encounters-v3-3501` (silver, **inside** the 6–12 Oct window; corroborates the tier line, nothing inverts) and `20261002-0539-q-skin-bd86` (silver, cited in-text for its 12.6× yet unlisted, contradicting the lens note's "cited only through the board"). Nothing on the page is unfaithful; the certificate undercounts its corpus, so one mechanical edit (append those lines, fold 3501's numbers, extend `ids.txt`, re-run regen) separates it from gold. I left the page untouched: adding lines myself would break `verify.py`'s P1 partition assertion and leave the run internally inconsistent — the named fix includes the scripts.
