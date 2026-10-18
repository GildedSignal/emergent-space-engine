Grade: gold

Second checker, blind to the first: the 2403 fence-sizing claim holds on a regenerating record with the checkers' named 10⁶ experiment flown as the cap-forced slice. Three passes (author, runner regen exit 0, my own flights) agree: the mint stream is bit-identical from K = 10⁵ to 6.5×10⁵ — coast 145, burn 2,069 entries, census 66/1/64 and 1125/0/597, multiplier 16.8× at both K. My attacks at 3×10⁵ and 7×10⁵ (above the flown range) reproduce the streams bit-identically; held stays ~200 at 12 ms, 0 engine-held at 24 ms; b_per_body 2,338 B makes a 10⁶ build 2.34 GB, forcing the slice. 10⁶ burn wall: 42.8 game-s. Adoption: one requirement line — size the answer-or-expire fence for the burning wildcard (~0.8 distinct/game-s), never the 0.05 coast constant.

## Reasons

**Reproduction (independent of the author and of the first checker).**
- The runner's `regen.sh` passed (exit 0, log on record); I re-counted every arm from the raw `MINT`/`ladder` logs with my own awk (not `analyze2.py`): counts, cut censuses, held maxima and λ match `analysis2.json` and the dossier table exactly (k650 burn 12 ms this pass: 2,069/1,722, census 1125/0/597, λ_distinct 0.8348, held 275/266 — inside the disclosed elastic band 206–275).
- Bit-identity is stronger than the dossier states: the full `t=`/`cls=` sequence is byte-identical between the 10⁵ and 6.5×10⁵ arms, coast and burn (`cmp` after stripping `held=`; held differs, as load must).
- Digest-neutrality control re-verified: probe off/on digest `20a45aa4…` equal, 385 MINT lines. Binary md5 matches `out/binaries.md5`.
- Cross-check arm reproduces 2403's second checker's published 10⁵ coast flight: 193 MINT lines, held 1, game 1898.5 s, kicks 3624, events 11115, boundaries 3499.

**Predictions.** `predictions.md` (17:22:19) precedes the dossier (17:41) and the author's md5 records (17:26–27); the runner's regen overwrote the author's flight outputs, so mtime proof of the flights themselves is gone — but the runner's and my passes reproduce every deterministic number, and the failed P3 band (≥ 400; ~200 measured in every pass incl. mine) is itself evidence the bands were not tuned after the fact. P1 held exactly; P2 (the claim's core) held at 16.8 ∈ [6, 40]; P4 (31 ≤ 0.25×), P5 (2,338 ∈ [2200, 2500]; 1e6 build 2.34 GB > the 2 GB cap), P6 (+28 ∈ [+15, +250] > coast's +7) and P7 (42.8 ∈ [15, 150]) held. **P3 failed as written and is reported failed** — the honest-reporting bar both 2403 checkers asked for; its diagnosis (backlog slack-shaped, not K-shaped, below the per-answer crossover) is confirmed by my 7×10⁵ flight.

**Attacks (mine, all outside the author's grid; `out/chk-n{300,700}-*`).**
1. K = 3×10⁵ (fresh, in-bracket): coast and burn streams bit-identical to the record (145/131/66/1/64; 2,069/1,722/1125/0/597); multiplier 16.8×; b_per_body 2,340.
2. **K = 7×10⁵, one rung past the author's K_max**: burn 12 ms bit-identical (2,069/1,722/1125/0/597), held 199/186 (same band), p99 10.86 ms, alive, peak 1,666 MB — under the cap; burn 24 ms bit-identical (2,071/1,726), engine-held 0, probe push-peak 31/18 as at K_max — the bracket-from-below statement ("crossover to K-bound service sits near 10⁶") survives a rung higher; b_per_body 2,338 exactly.
3. Machine/load axis: three hosts of passes (author, runner, mine) with wandering 12 ms held (186–275) and never-moving arrivals — the claimed split (arrivals and census are the law; the marginal-budget arm is the machine) is exactly what I observe.

The claim's domain must read: measured 10⁵ → 7×10⁵, the last ~1.4× to 10⁶ extrapolated on the measured per-body law (three scales) and arrival K-flatness (now a 7× span); λ's absolute value is cadence-scoped (0.835 at 15 wall-s vs 0.728 at 20 s in 2403) — the ratio and census are the invariants, as the page now says.

**Novelty.** 2403 (awaiting grade, same day) measured the multiplier at 10⁴/10⁵ and its second checker measured coast K-flatness one decade; the unflown 10⁶ burn arm was the named gap. New here: burn-stream bit-identity across a 6.5× step with the mechanism (census class t — the player's event clock never reads K), the cap-forced slice at 6.5×10⁵, the budget pair at K_max, and the record correction — which I verified against 2403's published branch: its P1 ("0.05–0.15 in every arm outside burn windows") measured 0.0027/0.431, its P6 ("≥ +100 MB") measured +21 MB, while its headline said all six held. The correction is accurate.

**Page.** The proposed `wiki/nladder.md` is the published page plus the new paragraph and one runs line (diff: additions only); the first checker's in-place tightenings match the regen record (206–275, 707→701, p99 digits). I appended my bracket. No closure: 2403 is ungraded on the page, so three golds do not agree on a current best.

**Goal fit.** Board bottleneck "memory at 10⁹ / the nladder pin". The fence constant the answer-or-expire fix would inherit from coast is wrong by the measured 16.8×; the 10⁶ wall is 42.8 game-s under continuous L8 burn, not 687. PRINCIPLES #5: "The player is the only wildcard" — his throttle hand mints the same stream at every K, so no population statistic sizes the fence; #12: at K_max the burn is still the arrival spike and the p99 event in the same frames. Adoption cost: none in code.

## What the author missed

- The "peak 1.61 GB (VmHWM)" is monitor-only; no artifact carries it — the ladder's own VmHWM tops at 1,550 MB (my 7×10⁵ prints 1,666 MB). Immaterial to the cap argument, but it should not have been stated without a captured number.
- The 31's push-time mechanism could have been pinned for two lines of probe (a per-frame push log, as acf2's instrument did) instead of left as "the exact source … unpursued".
- The wall arithmetic inherits acf2's (K+38)·224 B walk law unmeasured at K_max; a one-line probe closes it.
- The 10⁶ point is impossible only under this window's 2 GB cap; the box has 15 GB, so a future window with a raised per-process cap can fly the true 10⁶ arm and delete the extrapolation entirely — worth naming as the next run.
