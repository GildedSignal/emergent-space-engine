# Predictions — second author on 20261009-2120-taleb-8ea0

Written before any run of this session. The named gold experiment (check.md): make the bench's scripted
player *stay alive* at any depth (station-keeping / depth-matched decisions replacing the ∝rtf burns) and
make the run *report* instead of aborting on the lost-player view; then measure a living player at
hour-to-day horizons.

Bench patch (xtask only, no engine crate touched):
1. `--script jink|hold|coast`. `jink` is the original nominal-frame script, byte-identical path (old digests must not move). `hold` is depth-matched: forward, reverse, left, right, one 1/3-game-second burn per 4-game-second slot at canonical ticks — each adjacent pair cancels in rapidity (Δη = α·Δτ along an unturned heading), so the cycle nets zero to first order: station-keeping by symmetry. `coast` is the zero-decision control.
2. A failed view (player lost/unreadable) stops the presented frames and the run *reports* (`abort` field), settles to the canonical cut and prints the digest, instead of exiting non-zero with nothing.

## P1 — hold survival (decisive)
The hold player is alive at 3×10⁴ (8 h), 3×10⁵ (3.5 d) and 3×10⁶ game-s (35 d).
Kill: `player_alive: false` at any of those depths. Fallback: coast carries the ladder; the cliff is then thrust-driven at *any* burn spacing, which refutes "depth-matched station-keeping" as the fix and is itself the finding.

## P2 — coast survival
The coast player is alive at 3×10⁵ and 3×10⁶ game-s (nothing but tides, the moon and the fleet battle perturb it).
If coast dies too: the horizon ceiling is environmental, not thrust — a stronger harness defect than the script.

## P3 — the rtf-10⁵ rung now reports
The rung the author skipped and the checker saw crash (nondeterministic abort, no report) completes and prints a report with a digest, whatever the player's fate; wall ≤ 60 s for 30 nominal seconds (predict 5–40 s: cost follows events, and events/game-s declines with depth).

## P4 — living-frame cost at depth
With hold at every rung: view-gather p99 < 3 ms, zero hitches above 16.7 ms, worst frame < 16.7 ms; overflow frames grow with rtf (RTF-loss absorption, plane.md §7). events/game-s declines with depth (the quieting universe).

## P5 — canonicality survives the patch
(a) The three jink control cells reproduce the author's digests bit-for-bit on the patched bench (8ab0b55c…, 03e62d96…, 41343a14…). (b) The hold digest is identical paced vs unpaced (same seed, seconds, level), and identical across reruns under load.

## P6 — the memory slope is engine-side
The +12 MB/decade RSS slope (13.6→25.3 MB, 3×10⁴→3×10⁵ game-s) reappears on *coast* (empty decision log) at the same order of magnitude → it is not the decision machinery and not the player's thrust; it tracks game time (the checker's seed-2 evidence) with a mechanism still open. If coast is flat, the slope was script-coupled and must be re-attributed.

## P7 — memory of the instrument itself
The hold log itself costs memory (2 Vec entries per 4 game-s: ~2.4 MB at 3×10⁵, ~24 MB at 3×10⁶ game-s in the pending deque); memory-ladder cells therefore run on coast only, and I report hold and coast RSS separately so the instrument's own weight is visible, not hidden.
