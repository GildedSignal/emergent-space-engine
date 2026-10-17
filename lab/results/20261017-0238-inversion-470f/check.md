Grade: gold

**Abstract.** Claim: the plane's peak memory is wall-path-dependent, not canonical — the same 400-member coast flight either peaks at ~44 MB or grows live allocations to 220.9 MB (bulk-freed at ~20,000 gs; peak RSS retained at 206 MB) with every shipped counter flat. Reproduced in three independent sessions; regen itself flipped arms (40k flat, r1+r4 grew). My check: 9/9 flights grew under 9-way machine load (seeds 1 and 5; N=100 and N=800 also grow — 183 MB by 6,000 gs at 800), 0/3 run alone; flat path stable to 60,000 gs. d3fe's clean rate and 4fa8's unflown arm both refuted on main. Cost to adopt: zero code — annotate the 1.2–1.65×10⁶ letter with the load factor; wire the census into the ladder's CI arm.

## Reproduction

Tree at base `3dc6f621` (matches `base`), clean except `lab/results/`; the only change is the probe example (`work/patch.diff`, print-only + counting `GlobalAlloc`; the wrapper adds no allocations of its own, and the flat runs prove the instrument does not grow). The runner's regen exited 0 and — decisive for a stochastic claim — **flipped the arms**: the regenerated `out-400-coast-40k.txt` is flat (44.4 MB) while regenerated `r1` and `r4` both grow (RSS 46→95 MB and 47→99.5 MB, live 39.8→99.5 MB and 45.1→104.7 MB over 6,000 gs), same binary as the flats. One binary, both shapes, three sessions (author, runner, checker).

Verified against the preserved instance (`out-400-coast-40k-LEAKED-INSTANCE.txt`): live 220,862,318 B / 83,768 allocs at gs 20,000; bulk drop to 16.1 MB / 5,875–5,893 allocs by gs 24,000 (≈78k frees); hwm 206,976 kB, RSS ~206.5 MB flat to 40,000 gs and through settle (+0 kB); `[heap]` tracks live; mapping count constant 34; bodies/catalogue 428, `bytes_per_body` ~5.97–6.0 kB constant; slices frozen 14,080; held_scans 0, pending_handouts 0. Controls flat as stated (burn seeds 1–2, seed-2 coast, 48-member 40,000 gs at 9.2 MB, 3,000-body belt at 17.2 MB, fleet alive).

Numbers that differ (all minor, none load-bearing):
- **Growth rate.** Least-squares on the LEAKED live bytes over gs 3,000–20,000: **9.0 kB/gs** (allocs 3.35/gs, blob 2.69 kB). The stated ~11 kB/gs is the first-6,000-gs window rate (my loaded 400 runs: 11.6; the author's 6k growers: 11.9). Order and mechanism unaffected; the long-run rate should read ~9–12, not ~11 flat.
- **"~516 B/body" (dossier point 5) is a typo for 516 kB/body** (220.9 MB / 428 bodies). The understatement makes the transient *worse* (~86× the 2.55 MB store), not better.
- **Frequency.** "5 of 15 (~33%)" is a quiet-machine number only (see Attack 1).

## Predictions

`predictions.md` predates the decisive flights (file times 1 h before the final artifacts; the preserved instance is the only pre-regen survivor, as designed). P1: both pre-registered sides observed, and the author disclosed the unpredicted coin flip rather than hiding it. P2 (4fa8's unflown arm): refuted cleanly — events/game-s 16.9→~1.9 through dissolution, slices frozen; **but note the belt arm's fleet stays alive to 6,000 gs**, so the dossier's summary "fleets dissolve by ~3,000 gs at every size flown" overstates its own point 4, which states the belt correctly. P3: the pre-registered failure branch fired ("the grower is the session, not the battle") and was reported as such. P4: verified by my arithmetic — RSS slope over the first 2,000 gs (9.2 kB/gs) predicts RSS growth at 8,000 gs within 5% and at 20,000 gs within ~13%. P5: held — only the census sees the growth.

## Attack (my own cases)

1. **Load is the knob, not a coin (outside the author's quiet-machine range).** Nine concurrent flights on this shared box: **9/9 grew** — six seed-1 400-member coasts (RSS 93–98 MB at 6,000 gs), one seed-5 coast (96.7 MB; a seed the author never flew coast), N=100, N=800. Run alone afterwards: **0/3 grew** (two 6k flights flat at 44.3–44.4 MB, one 60,000-gs flight flat and stable to its end). Growing flights under load presented 99.6–116.0M ticks at gs 1,000 vs 129.3–137.7M for the quiet flights; every flight below ~129M grew (6/6), while the 129–138M band splits 3/3. So heavy debt makes growth certain, mild timing variance keeps it stochastic — the author's hedged "debt-triggered cache remains possible" is the right hedge, and the realistic player condition (the lab's own rule: heat and load are part of reality) sits in the 9/9 regime. Total tally across all sessions: 12 growing / 24 coast flights at 400.
2. **N outside the tested range.** The author flew 48, 400, and a 3,000-body belt. N=100 (loaded): live 14.9→34.0 MB over 6,000 gs (~3.9 kB/gs). N=800 (loaded): live 41.6→188.6 MB (~29.4 kB/gs), RSS 183 MB by 6,000 gs — extrapolating the growing path to 20,000 gs gives ~600 MB. Growth is **not** 400-specific and its rate scales with N, on the exact axis the N ladder is climbing. The claim survives with a wider domain than stated.
3. **Horizon.** 60,000 gs (1.5× the author's maximum): the flat path is stable flat end-to-end. A growing instance past its bulk drop was not re-flown (my 60k took the flat path); whether growth re-triggers in a second cycle stays open — the peak-RSS-retained claim is unaffected either way.
4. **Instrument artifact ruled out.** The counting allocator allocates nothing; the per-chunk `/proc` reads and CSV strings are freed; the flat runs bound the instrument's own footprint.

## Novelty

`docs/HISTORY.md` has no d3fe/4fa8 entries; the standing claims live on the wiki pages. d3fe (memory-h-live, silver, 6 October): "peak RSS grows ~0.2 kB per surviving member per game-second through any battle that stays live" — this run kills the rate as stated (fleets dissolve by ~3,000 gs; the slice bill is one-time; +0.001 kB/gs over 40,000 gs in flat runs) while showing a stochastic, load-gated growth of the same class survives. 4fa8 (nladder, silver): "the long-lived-battle case where the one-time slice excess becomes a rate — unflown" — now flown and refuted. The bimodality itself appears on no page; allocator-ratchet is a different mechanism (rollback margin escalation in `crates/allocator`). Not a repetition: it corrects two standing silvers and adds a new measured phenomenon on the board's top topic.

## The page

`wiki/memory-h-live.md` differs from HEAD by exactly `fold.py`'s hunks; every number traces to an artifact. Corrected in place where it overstated: the "(~33%)" frequency (now marked load-dependent, with my counts) and the 400-member framing (now carries N=100/800 and the seed-5 result, attributed to the checker). Appended a checker line to Runs.

## Goal fit

Board: "memory at 10⁹" and the N ladder's axis; this shows the premise behind every single-run memory measurement is wrong — the peak measures the wall path, not the game (4.7× at 400 members, ~3.7×+ at 800 and unbounded in horizon). PRINCIPLES: "Canonical outcomes are exact and independent of cache, partition, observation, schedule and hardware" — measured violation on the schedule clause, in the channel that sets the memory wall; and "Errors never compound" — a 9 kB/gs accumulation held 20,000 gs is the compounding class even though it later frees. Zero code change asked; adoption (annotate the 1.2–1.65×10⁶ letter; census on the ladder's CI arm) is one step, instrument already written.

## What the author missed

- **Load as the deterministic knob** — everything was flown sequentially on a quiet machine, turning the strongest lever into a coin flip and making "~33%" the least reproducible number in the dossier. The author hedged the right direction ("if fresh runs never grow, the frequency is the fragile number"); the truth is the opposite and stronger: fresh loaded runs *always* grow.
- **The N-domain** — 100 and 800 members both grow, with the rate scaling in N; the claim is bigger than stated on the exact axis it flags.
- **The mechanistic lead sitting on the page they folded into**: c304's every-64-frames rebind-history prune (`settle` bypasses it) is the natural candidate both for the retained blobs (~10 kB/ship-kick there vs 2.7 kB here) and for the bulk drop (≈78k frees in one window ≈ a starved prune finally running). My debt data points the same way. The next run should count prune invocations per chunk and backtrace one blob at the drop.
- Seed 5 (grows), and a post-drop horizon flight (my 60k took the flat path, so re-triggering is untested).
