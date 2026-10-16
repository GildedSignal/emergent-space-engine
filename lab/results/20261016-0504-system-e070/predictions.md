# Predictions (written before the decisive flights)

Run: 20261016-0504-system-e070, lens: the whole system.
Question: is the locals' pre-wave storm (917c: 334 events/frame at every N, vs 51 at N=0)
birth synchrony — every ladder local (ships in Home's doll, `min(extra/2,300)` of them) is
planned by `Universe::start()` at tick 0, so their first kicks land on shared
`aligned(step,0)/2` terraces — and does the same one-step spread law that cured the belt's
wave (ed3a) collapse it?

Instrument: `xtask universe --bench --unpaced --engine-ms 100000 --extra N --rtf 1000
--seconds S` (budget-free, coast, script of short burns unchanged), per-frame engine event
counts (`frame_events`) plus a tick-level trace of the worst frames. This box is Linux/x86
shared: orders of magnitude only.

Held-out cases (not tuned on): seed 7 at 1e4; N = 1e5.

## Predictions

1. **Anatomy (F0, extra=1e4, seed 1):** the pre-wave maximum frame holds ≥ 250 events,
   and ≥ 80% of them are first kicks/boundaries of ship ids in the ladder-locals range
   (the first `min(extra/2,300)` ship ids after the plane's own), in Home's doll, whose
   event ticks fall in ≤ 3 distinct tick terraces within one frame window.
2. **No-locals control (F1):** with the locals deleted (`ES_NO_LOCALS=1`, same belt size
   by construction — the belt takes all extra bodies), the pre-wave max drops to ≤ 80
   (the 917c N=0 floor is 51; the belt's own pre-wave contribution stays small because
   the belt's first kicks are days out, past a 30k game-s cut).
3. **The spread (F2, `ES_STAGGER_LOCALS` = per-id offset of the first plan over 2^24
   ticks ≈ 82 s):** the pre-wave max collapses to ≤ 120 (≈ floor + 1/2^? of the storm);
   if it stays ≥ 250, the storm is NOT synchrony and 917c's "one law, one lever" reading
   is wrong.
4. **N-flatness (F3, extra=1e5):** the storm max is flat in N within ±25% (it is the
   300 locals, not the belt), both arms.
5. **Off-arm identity:** with every env unset and `--extra 0`, the patched tree's digest
   at the canonical cut equals the pristine tree's digest (same seed, rtf, seconds), and
   the byte count of `frame_events` aside the report is identical.
6. **Cost of the spread:** total resolved events over the flight rise by ≤ 5% (the
   offset changes no step sizes; only anchor phases move).

What would make me wrong: the storm's events are not ships of the locals range (anatomy
fails), or the spread leaves the peak standing (then the pile is in the queue/scan
machinery, not the plans — a different, structural cause; that would REFUTE the one-law
reading and point at `requeue`).
