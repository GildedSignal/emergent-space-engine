# Dossier — 20261021-1443-system-9b03 (lens: the whole system)

## Claim

The player's scan is the last per-event full walk in the shipped engine: per player item it re-walks the window's whole candidate list although only 1.2–11.4% of those bindings changed, and on the burn arm 47% of its captures are exact same-tick duplicates whose memo is checked only *after* the walk — so the scan row (1fd7's post-desync wall, "cadence-invariant") is implementation-coupled but information-coupled to the kick stream, and a news-fed window (the boundary comb's 16ec certificate, not a new mechanism) puts it on the same dial as the cadence cut.

## Bottleneck

Board row "Macro, kicks per body" and 1fd7's post-desync ledger: after the cadence cut lands, the composed wall moves to the scan channel (walks 111–311× + answers 61× at 10⁹). Measured on shipped code, the walk's information content is ≤ 11.4% today and 1.2% where the player matters most (burn, the flyable regime): the walk overpays 9–83× today, and under the belt desync (78×, ddeb) the overpayment grows toward the desync factor because candidate bindings change only at kicks. Expected gain if adopted: the scan row rides the cadence dial (≥ 9–78× on the walk term) plus an exact, immediate duplicate delete where the captures aretrue duplicates (47% of burn captures are memo hits); it deletes nothing else — the answer half stays (the predicate reads moved bodies at t, honestly).

## Evidence

Instrumentation: pure counters in `encounter.rs::capture` (bindings compared by the shipped `same()`), example `scannews.rs` (nladder's flight loop verbatim, minus the Darwin-only footprint call), `SCAN_NEWS=1` per-scan lines. Digests printed per arm; no behaviour change (counters read only; the memo path is untouched).

| arm (10 s wall, rtf 100, 12 ms) | scans | cands/scan | changed/scan | news_frac | me changed | clean | fallback | memo hits |
|---|---|---|---|---|---|---|---|---|
| 30,028 bodies, coast | 96 | 171.8 | 19.6 | **0.114** | 47 (49%) | 0 | 0 | 0 |
| 30,028 bodies, burn L8 | 1,056 | 64.7 | 0.8 | **0.0120** | 542 (51%) | 501 (47%) | 0 | **500 (47%)** |
| 3,028 bodies, coast | 96 | 306.2 | 21.5 | 0.0701 | 47 (49%) | 0 | **86 (90%)** | 0 |

Reproduce: `lab/results/20261021-1443-system-9b03/regen.sh` (≤ 4 min; prints the table rows). Mechanism, read from shipped code: `universe.rs:772` — `encounters_for_player()` fires on **every** resolution of the player's item; `encounter.rs:190-194` — the reuse memo requires `self.t == t` (`same_inputs`), so it can only catch same-tick re-captures, and it runs after `capture` has already built the candidate list (a `binding_at` per candidate — the walk the ledger prices); `encounter.rs:53-56` documents the intended domain (boundaries/openings rebind nothing) but the tick equality reduces it to duplicates only.

## Predictions (predictions.md)

- P1 (fallback > 90% of scans at N = 30,000) — **wrong at 30k (0%), right at 3k (90%)**: the radial fence is scene-fragile with the *belt's own N*, the reverse of the expected direction. Both arms reported; od 4's fallback-on-belt-arm reading holds on the 3k arm.
- P2 (news fraction < 10%) — held on two arms (1.2%, 7.0%); the 30k coast arm is marginally above (11.4%). The kill criterion (news ≥ 50%) did not fire anywhere.
- P3 (half the scans have the player's binding unchanged) — held exactly (49%, 51%, 49%).
- P4 (news concentrated in kick waves; sign check) — not separated per-scan in the window; untested, stated as such.

## What would make it wrong

- If `binding_at(j, t)` on an unchanged binding is already O(1)-cheap and *not* the walk's cost term (the ledger attributes the walk to the candidate build + pin, 224 B/cand), the duplicate delete still stands (it removes the whole walk + tuple build) but the news-fed ceiling shrinks to the build term only. Attribution of the walk's internal cost (lookup vs build vs radial query) is the one unflown measurement; the fallback arm (3k, 306 cands) is where to price it.
- If the desync keeps the player's own cadence fine (it must: navigation) and the window's *membership* churns for a reason other than kicks (births, hand-outs, doll crossings), the news-fed form needs those channels too — births are already events (the hand-out), so this is wiring, not physics.
- The same-tick duplicates could be an artifact of my flight loop (the burn arm's thrust path calls `resolve_body(player)` twice per item via `input`'s pull plus the frame's advance). Even so, the memo-after-walk ordering is the finding: whatever re-captures at a tick, the walk is paid before the check that would have skipped it.

Cost of adoption: small — move the `(body, t, interval)` equality test before the candidate build (exact, deletes the duplicate walks today), then feed the window from kick events (the news channel) instead of rebuilding per scan. Fit with PRINCIPLES: "No work for no reason, so no ticks… we only care about changes" (14); the kick comb is 100% news and the boundary comb 0.12% (225d/16ec) — the scan is the one comb still walked as if everything changed.

## The lens

What it may have missed: I priced the walk's *information*, not its *nanoseconds* (the prof stage `ENCOUNTERS` exists but was not run with `--features prof`); and the 10⁹ extrapolation rides 1fd7's anchors rather than a flight at the ladder's top (memory cap). The elegant unification (one news dial for kicks and scans) could hide the hard special case the lens was warned about: a window that *grows* into a dense region (the player flying into the belt) — membership churn is then real news at the very moment C is largest, and the news-fed form's gain collapses exactly there. The 3k fallback arm is the cheap probe of that corner.
