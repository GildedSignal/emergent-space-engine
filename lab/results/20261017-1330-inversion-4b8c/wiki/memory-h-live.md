topic: memory-h-live
status: open
closed-by:
valid-while:
updated: 20261017-1330-inversion-4b8c

# Memory at 10⁹ in 8 GB: live information per body (H_live), scars, the standing representation

## Current best

**The bimodality's mechanism is named and knob-controlled: the growth is the engine's cleanup
being wall-owned, not game-owned — the held encounter scans drain only while the frame's wall
budget has `2·max(scan_ns, 750 µs)` left (universe.rs:1190; the condition itself is prior art —
scan-queue's 69f3 froze it at belt/burn scale; here it is the play path's grower), and the
history prune runs only at
`frame_to`'s start, so a slow/loaded machine hoards ∝ game-s while the game state stays
digest-identical (20261017-1330-inversion-4b8c, inversion; Linux/x86, seed 1, threads 1,
`RUIN_PROBE` print-only).** Dose-response at members 400, rtf 100: engine-ms 50 → held 0, RSS flat
45.7 MB; 5.0 → flat on a quiet box (≤1 held) but grew held 8→83, RSS +8 MB in an earlier same-box
run under ambient load — the margin is marginal at the shipped default, which is 470f's bimodality
reproduced by knob; 0.5 → the game crawls (77.5 vs 1,610 game-s presented) and memory grows.
**Digests identical across all three budgets** (`2713edb5639d7a16…`): wall-path only, law innocent.
The play-phase channel is the scans themselves (one per resolved player item, universe.rs:772 →
`Held::capture`, each pinning `binding_at(j, t)` for every window candidate): members 100 →
**4.5 kB/game-s ≈ 84 kB per held scan** (the comment's "about 10 KB each" is 8× low at just 100
members), and **470f's 220.9 MB peak ≈ `SCAN_BACKLOG`(2048) × ~105 kB/scan — the cap, not a
leak** (arithmetic, consistent with 470f's own 11 kB/gs × 20,000 gs and the 78k-allocation bulk
drop; the cap was never observed engaged — held ≤ 172 in any arm here). The catch-up settle
spike at cut 27,500 game-s (+21.9 MB at m100, +117.6/117.9 at m400/"m800", digests equal) exceeds
the player-item scans' pin: the second channel is `settle`'s prune bypass (c304's ~10
kB/ship-kick; 4,751 ship items here) — one disease, two symptoms: cleanup scheduled behind the
wall. The "bound" is ∝ bodies-in-window, the concentrated-fleet case, not the spread belt (the
3,000-body belt's flatness is the window, not innocence).
**[Checker correction]** the "m400 = m800" identity is the CLI clamp, not saturation:
`--members` clamps at 400 (xtask/src/universe/mod.rs:40 — `--members 800 --describe` prints "1
fleet(s) of 400 members"), so the 800 arm is the 400 arm. The pin's N-scaling is sub-linear on
real arms: 89–100 kB/scan at 100 members, 112 at 200 (checker, ms 0.5 arm) — not ∝ N; the
concentration reading stands, the saturation evidence did not exist.

*[The standing record (the FLOW bimodality, the catalogue intern, the rate and scar results, the
wall ladder) is retained on main's page below this entry, unchanged.]*

## Refuted
- **"The growth path's mechanism is unknown (prune-starvation a lead)"** (the page's own open
  lead): knob-controlled and decomposed — the held-scan drain condition and the settle prune
  bypass, both wall-owned; the digest is invariant across the whole dose-response
  (20261017-1330-inversion-4b8c).
- **"`SCAN_BACKLOG` bounds the backlog at about 10 KB each" (universe.rs:77):** measured 84–100
  kB per held scan at 100 members and 112 at 200 (checker); ~105 at 400 is inferred from 470f's
  peak, not slope-measured (the 400 arm's play phase is too short); the bound is concentration's,
  not the comment's (20261017-1330-inversion-4b8c).

## Open directions
1. **Game-owned cleanup (the fix this names):** the prune on a game-s cadence (not only
   `frame_to`'s start — `settle` bypasses it, c304's half), and the held scans answered or
   *dropped* at a game-s cadence — their answer feeds only the count/log/hash
   (universe.rs:206), so a canonical drop (by tick, not by wall) keeps digests defined and
   deletes both the 2048-cap memory term and the catch-up spike. Scan answers are hashed, so the
   drop schedule must be canonical (a law-visible-none decision, like the comb cures).
2. Burn arm unflown here: thrust changes the player's item rate (the scan generation rate); the
   backlog under burn, and the belt's window occupancy at 10⁵-10⁶, price the cap's true scale.

## Contradictions
- None new. The 84 kB/scan is RSS-slope ÷ held-slope on one arm (a direct pinned-`Arc` count
  could move it ×2); the settle-spike split between scan pins and prune-bypassed history is
  arithmetic (c304's per-kick figure carries that half), not separately instrumented.

## Runs
- 20261017-1330-inversion-4b8c (awaiting grade): the growth's mechanism knob-controlled — wall-owned cleanup (scan drain + settle prune bypass), digest-invariant; 470f's 220 MB = the 2048-scan cap
