Grade: silver

**Abstract.** Claim: the player's scan is the last per-event full walk; only 1.2–11.4% of walked candidate bindings changed, and 47% of burn captures are same-tick duplicates the memo checks only *after* the walk — so 1fd7's "cadence-invariant" scan row is implementation-coupled, information-coupled to kicks. Reproduced bit-for-bit (30k coast digest identical; counters match to wall jitter). Mechanism verified in shipped code (4/4 claims). My extensions: counters exactly N-invariant (10k coast = 30k; 3k burn = 30k burn), 20 s stable; capture priced at 108 µs/call coast, 20 µs/call burn (answers 790/178 µs/call dominate). Adoptable today: ~2-line pre-check (~18 µs/frame on burn arms). Not gold: the overpayment magnitude duplicates 687c/e9a1 (uncited); the desync composition (78×) is unflown.

## Reasons

**Reproduction (clean tree, patch applied by me).** regen.sh exit 0 (runner) and my own rerun: 30k coast bit-identical (digest `750cf21d…`, 96 scans, 171.8 cands/scan, news 0.11410, me 47, fallback 0, memo 0). 30k burn: 1,054 scans vs the author's 1,056, memo 499 vs 500, news 0.01206 vs 0.01203 — 10 s wall arms, jitter only. 3k coast identical (306.2 cands, 0.07008, fallback 86 = 90%). All dossier numbers regenerate; the instrumentation is provably read-only (counters and one `eprintln` gated on `SCAN_NEWS`; the memo block untouched).

**Predictions.** `predictions.md` mtime 14:49:57, flights 15:01 (work logs) — genuinely pre-registered. P1 wrong at 30k (0% fallback vs >90% predicted), right at 3k; reported honestly, both arms. P2 held on two arms, marginal miss at 30k coast (11.4% vs <10%); kill criterion (≥50%) never fired. P3 held exactly (49–51%). P4 (desync coupling) unflying without ddeb on main — stated as such, no overclaim.

**Adversarial cases (mine).**
1. *N=10,000 coast (inside the untested 3k–30k decade):* counters **identical to 30k to the fifth digit** (96 scans, 171.8, 0.11410, fallback 0). The walk's content is N-invariant on the fenced path — the belt never enters the candidates; the fence flip lies below 10k. Strengthens the result and sharpens the fence-domain question.
2. *N=3,000 burn (never flown by the author):* identical to 30k burn (1,056 scans, 64.7, 0.01203, memo 500, fallback **0**) — the duplicate structure and news are regime-robust; the fallback is a coast-only small-N failure.
3. *20 s horizon (2× the author's longest):* news 0.1009, me 0.497/scan — no drift; the kill criterion stays far away.
4. *Cost attribution (the author's admitted gap), clean tree, `--features prof`:* capture 9,381.6 µs/540 frames coast (107.8 µs a call, 17.4 µs/frame) and 20,738 µs/1,047 calls burn (19.8 µs a call, 38.4 µs/frame); held answers 790/178 µs a call. So the walk is real but the **answer half dominates on shipped arms** — the news-fed gain on today's plane is bounded by a ~17–38 µs/frame term; the ≥9× claim lives only in 1fd7's 10⁹ composition.

**Mechanism, read in shipped code (all verified).** `universe.rs:772` fires `encounters_for_player` on every player-item resolution; `encounter.rs:174-189` builds candidates with a `binding_at` per body before the memo test at 190-194; `same_inputs` (80-87) requires tick **and** interval **and** candidate equality — same-tick duplicates only; the doc comment (51-56) intends boundary/opening reuse that the tick equality cannot serve. The 47% figure is the memo's own hit count (500/1,056), not an approximation. The wiki CAUTION (coast same-tick re-captures with changed candidates → a dirty bit, not bare tick equality) is correct and honest.

**Novelty.** Three genuinely new things: the memo's exact domain and its after-the-walk ordering (47% of burn captures deletable in ~2 lines, digest-neutral by construction); the correction to 1fd7's "cadence-invariant" scan row (kick-coupled information); the fence's small-N failure refining budget-1e9 od 4. But the headline magnitude — walk overpays ~9–83× — was already standing on `scan-locality`: 687c (churn 0.6/scan, gain K/μ_win = 16× shipped / 85× ladder) and e9a1 (read-set deletion 65× burn, 132× coast). The dossier and the proposed page cite none of this; I added the prior-art line to the page in place. A corroboration at new coordinates, however clean, is not a 10× move on the bottleneck by itself.

**Goal fit.** Respects PRINCIPLES 14 ("No work for no reason… we only care about changes"): the scan is the one comb still walked as if everything changed. The board's macro row (kicks per body) is moved only via the unflown composition.

## The one experiment to gold

Execute the run's own od 2+od 3 together: wire the nothing-resolved-since dirty-bit pre-check (exact, the memo's own domain) and fly the news-fed window on the composed desync arm (ddeb's belt classes), showing the scan row's walk term falls with the kick dial — digest-neutral on the shipped gates, cost attributed. That converts "information-coupled" from a verified argument into a measured composition, and the 10⁹ ledger's scan row (111–311×) gets its dial.

## What the author missed

- The prior art above (687c, e9a1) — the page overstated novelty; corrected in place.
- The counters are exactly N-invariant on fenced paths (my 10k arm): the "belt-N-fragile" framing should read "small-N-fragile" — the flip is below 10k, and the fallback never fires on the burn path.
- The walk's wall time (priced here): on shipped arms the answer half (127–344 µs/frame) dwarfs the walk (17–38 µs/frame), so the pre-check's value today is order 0.1–3% of a 12 ms frame — its real payoff is only in the 1e9 ledger the run did not fly.
- `nladder` does not link on Linux (Darwin-only `proc_pid_rusage`); the scannews port was necessary — worth stating, since it explains why the prof stage was never run.
