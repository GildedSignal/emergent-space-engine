Grade: silver

**Abstract.** Attribution reproduced: the play-time FLOW's growing path is the held-scans queue; each scan pins its candidate capture — measured 171 kB / 73 allocations (the code comment says 10 kB), declining to ~90 kB as the fleet dissolves; `SCAN_BACKLOG = 2048`'s force-answer matches 470f's ~78k-allocation bulk drop (ETA ≈21,000 presented game-s against their ~20,000; rate 0.096 scans/gs reproduced in two checker flights). Premises killed: prune starvation (prune is unconditional), per-body growth class. Checker, outside the author's 400-only range: at 1,600 members the pin reaches ~2 MB/scan, so the count latch bounds memory at multiple GB — the byte fence is necessary, not cosmetic. Adoption: one byte-budget constant + one stats line + digest check. Silver because the fence itself was never flown.

## Reproduction

- `regen.sh` exit 0 (runner), and its two logs (`regen.log`, `regen_verify.log`) agree: quiet arm flat (held 0, live 15.3/15.2 MB) even at box loadavg 7.6–8.0; load arm held 76/72, live 47.6/45.5 MB — the ≥1.5× separation holds. All dossier numbers regenerate.
- Census verified on shipped code, not the author's transcript: `SCAN_BACKLOG = 2048` (universe.rs:79) with the force-answer at :1017–1019 inside `advance`; `prune()` unconditional at :1082; the capture is the candidates `Vec<(usize, Binding, Scalar)>` (encounter.rs:174–195); `held_scans()` at :299; "about 10 KB each" at :77 — the 17× correction stands.
- Quotes: 5/5 byte-identical via `verify_quotes.py` (run twice), plus my own grep of the raw `readwise.json` (4,590 highlights) for three of the five fragments.
- Predictions: `predictions.md` (13:36) precedes the build (13:39), the wiki page (13:44) and the record logs (14:11). P1 half-held (the letter dead, the parenthetical right — honestly reported); P2 held and sharpened; P3/P4 held.

## Attack (three adversarial cases, one outside the author's range)

1. **N=1600, outside the author's 400-only range.** Under load, scans still accumulate (held 1→8 with births eating the budget). More telling: on the busy shared box with *no spinners of mine*, the 1,600-member birth phase self-saturates the 12 ms frame budget (frame_ms 11.8) and pins 93 scans / 225 MB in 1,200 frames — ≈2 MB per scan, ≈1.4 kB/body against ≈0.4 kB/body at 400. So the pin scales with the doll population and the 2,048-*count* latch bounds memory in the multi-GB range at fleet scale: the run's own recommendation (fence by bytes, not count) is necessary, and the page's "~1.5 GB at formations" was optimistic. I folded this into the page.
2. **The latch, directly.** Two flights (22,000 and 27,000 frames under 6 pinned spinners): maximum held 1,745 — the 2,048 force-answer never fired on this shared box (the author's "~5 min" was optimistic; presented time starves under load). The identity rests on convergent arithmetic instead: scan rate per *presented* game-s is 0.096/gs in both flights → latch ETA ≈21,300 presented gs against 470f's ~20,000-gs drop, and late-flight allocs/scan (31–40) matches 470f's 78k/2048 = 38. Strong, but not the direct observation the dossier named.
3. **Non-stationarity and the unit.** The pin is not 171 kB throughout: the author's own record log declines 146→88 kB/scan as the fleet dissolves (my long flight: 85–105 kB late; ~31–40 allocs/scan vs 73 early). 171 kB is the early-flight (worst-phase) average — the right number for a *peak* bound, but the page presented it as "the" pin. And the probe prints `now/6000` as "gs", which is ticks/6000 ≈ 33.9 game-s (`TICK_SECONDS` = 4.925 µs); `flow_arith.py` rightly ignores the column but uses *nominal* 5/3 gs/frame, while the load arm's presented time undershoots nominal ~1.3× (4,505 true gs vs 6,000 in the record arm). In presented game-s the ETA is ~21,000 — a *better* match to 470f than the quoted 26,629. Conclusions survive; the units must be stated.

## Novelty

The live page (updated by 470f) left the mechanism open ("the trigger is the wall-budget path, not the game state"); docs/HISTORY.md has no prior attribution. New here: the pin measured (17× the shipped comment), the latch↔bulk-drop identity, per-scan-not-per-body (killing the naive 27–39 MB/gs-at-10⁶ ruin extrapolation), and the load-arm instrument. Partially known in-tree: `frame_loop.rs:130–136` already asserts scans pile up with no idle time and that flushing is digest-neutral — the pile-up phenomenon was shipped knowledge; the memory pricing was not. And "no consumer reads the standing count" is slightly overstated: `frame_f1`'s TRACE line prints it (env-gated example), though no stats/memory instrument does.

## Goal fit

Memory row of the board ("within ~2× of the floor in the worst case; only what the ladder shows breaking") behind board #1. PRINCIPLES, Truth: canonical outcomes "independent of cache, partition, observation, schedule and hardware" — the fence is what makes peak memory canonical again; the load arm is the missing instrument axis (lesson 2). Respects via negativa: the adoption is one constant and one print, not a new component.

## Provenance note

The record logs' mtime is 14:11:02, but `regen.sh` says they were "flown 13:33-13:34 on a quiet stretch", and the 13:44 wiki page already carries their exact numbers — so an earlier flight existed and the 14:11 files are an undisclosed re-flight (on a busy box; the quiet arm is flat there anyway, and regen reproduces every claim independently). Numbers the shipped code cannot regenerate: none found. Wobble recorded, not grade-changing.

## The one experiment that would make it gold

Fly the fence: replace the count latch with a byte budget at a low water mark (e.g. 32 MB), and show (a) digests bit-identical across quiet/load/fleet arms, (b) the load arm's live_B flat, (c) peak RSS bounded at one fleet scene. That deletes the pin, closes 470f's bimodality, and makes wall numbers quotable — the run's own named falsifier, plus the P2 held-out case (one counting-allocator flight at 10⁶ under 8-way load) in the same rung.

## What the author missed

- The 216 B/candidate decomposition does not close (428 × 216 B = 92 kB ≠ 171 kB); the measured tuple cost is ≈400 B. Corrected in the page.
- The pin's phase dependence (fleet dissolution) unstated; "171 kB" is the worst-phase average.
- The gs unit conflation (probe column mislabeled; nominal vs presented game-s differ ~1.3× under load) — the ETA was unit-lucky and actually improves in presented gs.
- The count latch is not a memory fence at scale: at 1,600 members the pin is ~2 MB/scan → a multi-GB bound, worse than the page's formation estimate; only the byte fence bounds the peak (their lesson 1 already implied it; now measured).
- The latch was never observed firing, including by me (86% of the way); the "~5 min" confirmation cost was optimistic on a shared box.
- One flight per arm (the lens admits it); the accumulation *rate* per presented gs reproduced exactly across my two flights, but the incidence claim still rests on 470f's 37.
