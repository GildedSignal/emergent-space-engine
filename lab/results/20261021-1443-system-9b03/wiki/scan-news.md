topic: scan-news
status: open
closed-by:
valid-while: crates/universe@08f5a3eb + this run's patch (encounter.rs counters, examples/scannews.rs)
updated: 20261021-1443-system-9b03

# The player's scan: the one comb still walked as if everything changed

## Current best
**The scan walk is not news-fed on shipped code [9b03]: per player item (`universe.rs:772`) `capture` rebuilds the whole candidate list (a `binding_at` per candidate), and only 1.2–11.4% of those bindings changed since the previous scan — 0.0120 on the burn arm (1,056 scans, 64.7 cands, 0.8 changed), 0.114 coast at 30k (96 scans, 171.8 cands, 19.6), 0.070 at 3k (306 cands, the radial fallback firing on 90% of scans; at 30k coast it fences, 0% — the fallback is belt-N-fragile, od 4's reading holds only on the small arm). The player's own binding changes on 49–51% of scans everywhere (kicks rebind; boundaries/openings do not, as documented at `encounter.rs:53`). The reuse memo (`same_inputs`) demands the identical tick, so it catches only same-tick re-captures — 47% of captures on the burn arm (500/1,056 memo hits, 501 clean) — and it is checked *after* the walk it could have skipped (`encounter.rs:190-194`).**
> Prior art the page must carry (checker, 20261021): the overpayment *magnitude* was already standing on
> `scan-locality` — 687c's window-membership record (churn 0.6 entry/exit a scan under burn, gain law
> K/μ_win = 85× ladder / 16× shipped) and e9a1's read-set deletion (65× burn, 132× coast) — 9b03's news
> fraction corroborates these; what 9b03 *adds* is the kick-coupling (the 1fd7 correction), the memo's
> exact domain (tick+interval+candidates equality, checked after the walk; 47% of burn captures), and the
> fence's small-N failure (0% fallback at 10k and 30k coast, 90% at 3k — the flip lies below 10k).
Consequence for the composed ledger: the scan row 1fd7 named as the post-desync wall ("walks 111–311× + answers 61×, cadence-invariant") is cadence-invariant only in implementation — the information is kick-coupled (candidates change only at kicks), so a news-fed window (update membership at kick/birth events, evaluate the predicate per scan) rides the same dial as the cadence cut: the walk's overpayment is 9–83× today and grows toward the desync factor (78×, ddeb). CAUTION on the exact half: same-tick re-captures are not all duplicates — coast arms re-capture at the same tick with changed candidates (48/96 pairs, 0 memo hits; bodies resolved in between), so the pre-check needs a nothing-resolved-since dirty bit (16ec's key-range shape), not bare tick equality; where it holds (burn, 47% memo hits) the whole walk of the duplicate is deletable exactly.

## Refuted
- (none yet)

## Open directions
1. **Attribute the walk's internal cost** (lookup vs tuple build vs radial query vs 224 B/cand pin, memory-h-live's fence): the 3k fallback arm (306 cands) is the cheap probe; decides whether the news-fed ceiling is the whole walk or only its build term.
2. **Fly the growing-window corner** (the player flying into the belt): membership churn is real news exactly where C is largest — the lens's named blind spot; if news_frac stays low there, the news-fed form closes the 10⁹ scan row with the cadence dial.
3. **Wire the pre-check** (exact, ~2 lines): deletes 47–50% of captures' walks on burn and settle paths today, digest-neutral by construction (the memo's own domain).

## Contradictions
- None open. Noted: od 4 (budget-1e9) reads the fallback on every m48 belt arm; 9b03 finds it scene-fragile with the belt's N (0% at 30k coast, 90% at 3k) — both stand, the fence's domain is the open question.

## Runs
- 20261021-1443-system-9b03 (system): the scan walk measured for news on three arms — news_frac 0.012–0.114, memo 47% same-tick on burn, radial fence belt-N-fragile; the scan row is information-coupled to the kick dial.
