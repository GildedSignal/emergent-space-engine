topic: nladder
status: open
closed-by:
valid-while:
updated: 20261014-1719-system-3fc0

# The N ladder: 28 live bodies toward 10⁹

## Current best

**The wave's freeze is the player's doll, measured on shipped main: the shock a 20 s rung never
sees (F1's window ends 11,000 game-s before it) is absorbed as 1.45 s of lag when the player is out of
the root doll and as unbudgeted 0.3–1.2 s single frames when it is in it (20261014-1631-taleb-6138).**
Every belt body is born at tick 0 with one Δs, so the first kicks arrive as one smooth wave at
13,037–14,542 game-s; the budgeted drain saturates at ~235 events/frame; `pull_ships(key, !in_root)`
(`universe.rs:769`) resolves every ship below the player's item inside one item (up to 24,467 events).
*[checker 6138: the onset N is machine-conditional; the batch model misses its drain term.]*

**6138's named fix is built (`ES_PULL_MAX` + held scan, 20261014-1719-system-3fc0); the claimed kill
did not reproduce.** The author reported the bounded pull freezing the horizon at 2×10⁴ (tick 55,
within 1,200 frames) while pristine advances. Three independent runs on this box (the runner's regen
and checker re-runs at `ES_PULL_MAX`=256 and 64) show the opposite: the bounded arm advances on
pristine's own trajectory (now=1,048,715 by frame 1,200; 50×10⁶ ticks by frame ~15,000) and cuts the
worst frame ~12× (294.8 vs 3,439.9 ms, the regen pair), pulling ahead of pristine after the burn
(809M vs 336M ticks at frame 21,600). Every arm, pristine included, sits at now=55 at frame 600 (the
pre-burn unlock), so the reported freeze is the 600-frame stall detector crossing that unlock on a
loaded box — not structure: shipped `rekey` (`universe.rs:623-628`) moves due ships from `waiting`
into the frame's budgeted queue with no pull at all, and the drain demonstrably inherits the backlog.
At 5×10⁴ and 10⁵ **both arms stall identically** (now=111 / now=30; the onset moved below 10⁵ as the
box loaded through the window) — no bounded-vs-pristine dissociation exists anywhere measured, so the
fix is neither killed nor blessed at scale on this box; the wave (13,037+ game-s) is unreachable
here. P1 (bit-identity under a truncating pull) stays untested (checker attempt at cut 230 game-s:
no arm reached the cut in 210 s under load). Worst frames at 2×10⁴ pass 300 ms in every arm before
the wave — the monster is not the pull alone (P3 failed, the author's own criterion). Cross-box
frame-cost comparisons need the box's effective-rtf line reported with every flight (kept).

**The deletion program gets its method, priced from Julien's library mined verbatim for the first
time (20261014-1631-library-7f99).** 26 kills, 5 revival-shaped events; the frame path holds 0 add-backs
(below Musk's 10% quota); promotion collapses to a filter (the refit's refusal is the trigger);
automation last.

**Break #3's scan half is decomposed (20261014-1511-components-a2c1).** The player's scan walks its
certificate's poison: a monotone doll-wide speed cap (84×) and an inverted density rule (fires below
~9.4×10³ bodies); the window should widen per body, not per doll.

**Break #2's "representation's lever" is measured (20261014-1221-components-0e37).** The compiled
orbit is write-only memory for the engine, exactly its key; the view's ramp completion is its one real
reader; `Segment` drops `entry`, gains key + a two-word completion → ~520 B/body deleted.

**The smallest promotion is no promotion (20261014-0450-scout-b29a).** One belt event is a
stack-local function on the compact row (~38 µs, 12–40 B standing); the key-space arm 0.11 µs.

**The 10⁹ ledger is composed (20261014-0059-fermi-effb).** The kick gap is the hot rail's alone;
the cold rail is encounter-bound ~1.9×10³ skin-on; memory 2.6–5 GB quiet; rate = 2^step_log2/P.

**The rule-2 conflict is resolved by decomposition (20261014-0000-fermi-3071).** Rule 2 is dead as a
ladder rule; the live-set distribution is manufactured at birth (the compiled period ladder).

## Refuted

- "Hold the scan and let the budgeted drain resolve what the pull would have" (6138's named fix,
  built as `ES_PULL_MAX` + held scan), claimed killed by a horizon freeze at 2×10⁴
  (20261014-1719-system-3fc0): **the kill did not reproduce** — the bounded arm advances with the
  worst frame cut ~12× at 2×10⁴ (regen + two checker re-runs), and both arms stall together at
  5×10⁴/10⁵ on this box. `rekey`'s waiting→queue promotion (`universe.rs:623-628`) is the drain that
  inherits a truncated pull's backlog. The fix stands unjudged at wave scale (checker 3fc0).

- "The wave is the drain's problem": the drain holds the coast at 12.0 ms through the same wave
  (20261014-1631-taleb-6138).
- "The scan's walk is O(N) at ladder scale": doll-scoped, 194 bodies a call, except where the inverted
  density rule fires (N ≲ ~9.4×10³) (20261014-1511-components-a2c1).
- "The retired compiled orbit is needed by the engine between kicks": flight reads are O(1) in N; the
  belt's retired tables are read 0 times in a headless flight (20261014-1221-components-0e37).
- "Deleting the retired generation is free at today's view": the gather completes ≥1 row in 1 through
  the previous binding; needs the two-word completion (same run).

## Open directions

1. **Judge the fix by its certificate, not by a stall**: digest/encounters identity at a reached cut
   (P1/P2) with the truncation firing, then worst-frame and horizon-progress pairs on a quiet box at
   2×10⁴–10⁵ past the wave. The instrument is this run's `work/patch.diff` (env `ES_PULL_MAX`,
   `ES_PULL_FORCE_SCAN`) and probe; shipped `rekey`'s waiting→queue promotion (`universe.rs:623-628`)
   is the drain that inherits a truncated pull's backlog.
2. **The same lens on the remaining frame-path guards** (a2c1's cap, density rule, hull widening):
   each is a repair for a reader forcing synchronous work; the digest at the cut judges each deletion.

## Contradictions

None open among graded runs. (This run also folded the page's 14 October merge conflict
library-7f99 vs taleb-6138: both kept, side by side — independent results, no competition.)

## Runs
- 20261014-1719-system-3fc0 (lead): 6138's named fix built (`ES_PULL_MAX` + held scan) and claimed
  killed by a horizon freeze at 2×10⁴; the freeze did not reproduce (checker: bounded advances, worst
  frame −12×, both arms stall together ≥5×10⁴); P1 untested; the headline numbers were not
  regenerable from the run's own evidence file.
- 20261014-1631-library-7f99: the deletion program's method and quota audit.
- 20261014-1631-taleb-6138: the wave's freeze measured; the fix named, not built.
- 20261014-1511-components-a2c1: the scan's poison walk decomposed.
- 20261014-1221-components-0e37: the compiled orbit is write-only memory; the two-word completion.
- 20261014-0450-scout-b29a: the smallest promotion is no promotion.
- 20261014-0059-fermi-effb: the 10⁹ ledger composed; the cadence law verified in code.
- 20261014-0000-fermi-3071: rule 2 dead by decomposition; the surprise-rate census explained.
