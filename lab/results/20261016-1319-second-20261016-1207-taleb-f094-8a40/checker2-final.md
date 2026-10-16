Working...
Check complete. `check2.md` written; the author's wiki page corrected in place (nothing else in the run folder touched, scratch kept in `/tmp/c2`).

**Grade: gold** — my verdict as the blind second checker.

**What I did**
- **Reproduced**: runner's regen regenerates every count (leaver totals 43/43, 361/361, hs_max, lag caps, all prof call counts exact); wall µs within noise. My own determinism check is stronger than the author's claim: stripping ms/cost_us, det-1 ≡ det-2 bit for bit.
- **Predictions**: `predictions.md` (13:24:33) precedes every grid output and the dossier; 5/7 held, 2 magnitude misses disclosed with mechanism, kill criteria unfired.
- **Six adversarial arms of my own**: held-out seed 7 (348/348 identical, cap holds), level 12 (421 ms bill, hs 635, cap holds, latch recovers at 12 ms), belt 1e4/5 ms to f500 (totals identical, wave stretched, plateau ~3×), f300 long horizon (plateau is a steady state creeping 145→247, 8× under the 2048 cap), fleet 2000 to f400, and a prof-base400 attempt (blocked by a concurrent build lock — noted as unverified).
- **The one real find**: at fleet 2000 the composition stops being outcome-neutral — identical 824/824 through the opening, then the held burn hands out a second wave the coast never pays (1,907 vs 824 leavers by f400, fleet bill 1.59 s vs 0.94 s, promotion-priced again, lag still capped). The page's "totals still identical 824/824" residue line was an f150-window artifact; corrected.
- **Dossier flaws named**: the "~499 extra fits / ~195 µs each" decomposition contradicts the deterministic call counter (250→542 = 292 fits; ~330 µs a fit, ~433 µs a flush ≈ one hand-out bind); "dominant at served fleets" holds at 48 only (at 400: 207 vs 130 ms, hand-outs still own it); absolute µs bands are load-dependent (I measure ~1.1 ms/leaver on coast *and* burn at load 8.8 — the burn≈coast invariance is the stable fact). All corrected on the page.

**Why gold**: the named gold condition (the opening under burn) flown at the page's arms, pre-registered, reproduced by two independent parties, novel against the page and HISTORY, and adoptable in one step (page only, no engine change) — the premise "the opening's owner is the hand-out wave" is shown wrong under burn at the served fleet (4.8×), and no 1e6 smoothness term hides in the composition.
