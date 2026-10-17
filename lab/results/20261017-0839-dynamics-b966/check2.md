Grade: silver

The frames-mode claim is true and reproduced. The shipped finality assert (`alloc.rs:1451`, "rollback … would revise its published tick") fires in `run_frames` itself: 3 crashing draws on disk in the author's window (f1–f3), the runner's n=240 draw (nA, 768→816), and my fresh window 3/6 at the decisive arm (rate 600, n=120; 592→624, 592→608, 656→720 — gaps 16–64, 1–4 strides). Chunked batch crashed again 2/2; single-call batch, quiet, n=60 and n=480 survived. The page's open direction 2 (9b46: "one `run_frames` run decides it") is decided: the crash is player-reachable, so the publish/rollback fix (direction 1) outranks every performance question. Silver, not gold: the dossier's "never with slack (rate 300: 0/6)" is contradicted by the run's own `out/` (two uncounted, undisclosed panics labelled r300a/r300b) and by my fresh window (1/6 crash at rate 300); the author-window 10/14 count and "surviving frontier > 2100" (actual 1408–1456) are not backed by artifacts.

## Reproduction

Applied `work/patch.diff` myself (tree had been reverted after the runner's regen; patch = one new example file, no engine edit — verified), built, ran (author's binary, my outputs in /tmp/check2-out):

| arm | mine | author on disk | runner regen |
|---|---|---|---|
| `drift chunks 120 1800 150` | **2/2 crash** (256→300 twice) | 1/1 (256→300) | 3/3 |
| `drift frames` rate 600, n=120 | **3/6 crash** | 3/4 (f1–f3) | 0/5 |
| `drift frames` rate 300 | **1/6 crash** (chk-g6: 608→624) + 0/2 at 6 s | 0/3 counted, **2 uncounted crashes (r300a/b)** | 0/3 |
| `drift frames` n=240 rate 600 | — | 0/3 | 1/3 |
| `drift batch` / `quiet frames` | — | survive | survive |

All panic shapes match: `fin_hi − s0` = 16–48 on every panic on disk (dossier: 16–64). The mechanism claim is verified in the code: `assert!(r.fin_hi <= s0)` at `alloc.rs:1451` inside `certify`'s stride-start walk (1437–1443), worker publication at 1759/1777, ahead cap via `release_cap` at 1752 — the race the dossier describes exists exactly as written.

## Predictions

Pre-registration order verified by mtime: `predictions.md` 08:45:49, first drift artifact (`drift_chunks_120_1800_150.err`, already a panic) 08:45:55. P1 held (chunked crash, now 12/12 across four sessions), P2 held (frames crash — the decisive answer), P3/P4 held, P5 held in shape with the ≥900 guess honestly reported wrong. Pre-registration is clean.

## Novelty

The published page's open direction 2 said frames mode was "untested" (9b46); this run decides it. Not in HISTORY.md before. The chunked-batch reachability half alone would be a repeat of 9b46; the frames half is the new, decisive content.

## Why not gold

1. **"Never with slack" is false, and the run's own evidence says so.** `out/r300a.err` and `out/r300b.err` (08:48:50–08:49:00, between the counted f- and s-series) are finality-assert panics from runs named rate-300; `out/r1200a.err` likewise. None is counted in the dossier table (which uses only the later s-series: 0/3 at 300, 1/3 at 1200) or disclosed. My fresh window then crashed 1/6 at rate 300 with the author's binary and args. Rate-300 total across all windows: 3/22 — rare, not never. The "keeping-up band" survives as an incidence gradient, not a wall; the reachability conclusion is strengthened, but the printed sub-claim is contradicted by the run's own log.
2. **Counts not regenerable from artifacts.** The author window's "10/14" at rate 600 has 4 draws on disk (3 crashes); "3/3" chunked has 1 on disk. The regen-window row (1/5 at rate 600) was overwritten by the runner's 0/5. Both windows' verbatim numbers cannot be re-derived; only the direction reproduces.
3. **"Surviving frontier > 2100" is wrong**: on-disk rate-300 survivors read 1408–1456 (s300a–c), 1248 (gA).

None of this touches the core claim, which reproduces; it is the reporting bar ("numbers the shipped code cannot regenerate… a headline the log contradicts") that gold requires.

## One experiment to gold

Recount the rate-300 arm with disclosure: acknowledge r300a/r300b, run ≥6 fresh draws at rate 300 (seconds 5 and 6), and restate the incidence as a gradient (crash possible at every load; band = higher incidence). My 1/6 plus the author's own 2 hidden draws suggest it lands immediately. The reachability core needs nothing more — it already reproduced in three independent windows.

## What the author missed

- The ahead cap was declared irrelevant ("survival tracks load, not the cap") from one knob value. My same-window sweep: 3/6 crash at ahead 0.25 s but 0/3 at each of 0.05 s and 1.0 s (checker instrument `finframe2.rs`, ahead + closing-speed args; removed after use). Three draws per arm is thin, but the cap's role is unsettled, not dismissed.
- Outside-range probes ran clean in my hands (n=480 → 1,920 bodies: 0/2, behind-present protection held one decade up; n=60: 0/2; Q/4 closing: 0/3) — the author could have had these cheaply.
- The dossier's own "what would make it wrong" says incidence is not a parameter, then the wiki page (and abstract) lean on window-specific counts (11/19, 11/29); I have rewritten the page's current-best to 14/35 across five windows, rate 300 3/22, and flagged the band-as-gradient correction plus the ahead-cap and n=480 results in open direction 2.

Goal fit: board item 4; a reachable panic in the live path is ruin — "not making mistakes matters more than doing things efficiently" (§25) — and the assert polices finality the wrong way round for "the oracles are guards, not shepherds" (§34).
