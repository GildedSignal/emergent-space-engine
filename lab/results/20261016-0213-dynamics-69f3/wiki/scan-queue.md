topic: scan-queue
status: open
closed-by:
valid-while:
updated: 20261016-0213-dynamics-69f3

# The player's scan queue: birth, service latch, and the ruin band

## Current best

**The burn's scan backlog is a one-way service latch, not a load-sharing queue
(20261016-0213-dynamics-69f3, dynamics lens, shipped code + a print-only counter patch).**
`drain_scans` answers only while the frame's leftover room `≥ 2·max(scan_ns, 0.75 ms)` (the margin
floor), and `scan_ns` decays only through served answers — so once one answer costs more than half
the room (b = the engine budget; S = s·N, s = 1.7–4.2 µs/body across seeds **and runs** at the same
N+seed: 2.97 author / 4.20 regen / 3.35 checker; the latch holds the worst, coldest answer — steady
flush S is 2.1–2.5 µs/body) the drain freezes **permanently**, burn and coast alike (exactly
one answer ever, then none; checker: at b = 1 ms even that one never runs, the margin floor alone
freezes). Below the latch the seam is free: B ≤ 4 (one frame's mint before its drain), 0 at rest,
58/58 scans answered at N ≤ 1000 (seed 7).
Above it a pure linear birth: λ = 14.4 holds/s
(7.25 new mints + 7.25 duplicate reuses, N- and seed-independent — the player's own thrust-kick
rebinds; quiet coast mints 0), memory 115 B/body per held scan (= taleb-51b7's 113), ruin at
SCAN_BACKLOG (2048) or the box fence, ≈ 142 s at any N whose 2048-pin fits RAM. The freeze
boundary N_freeze(b = 5 ms) ∈ [600, 1470] (the spread is S's, seed- and run-fuzzy: the candidate
set is seed-dependent, and S moves ~1.4× across runs at one N+seed), straddled across seeds at
N = 1000 and across budgets at N = 1000 seed 1 (checker: frozen at b = 5 ms, serving at b = 12 ms,
frozen at N = 500 b = 1 ms — the threshold is the dimensionless S/(room/2), not N). Consequence for
taleb-51b7's ruin: no budget tuning reopens service at belt scale (at 10⁴ S ≈ 3–6× b, at 10⁵
≈ 60×) — the candidate-set cure's success criterion is **S < b/2 at the player's own N**, which
makes the seam free, not merely cheaper; fences stay guards.

## Refuted

- "The backlog grows because arrivals outpace a sharing service (Kingman near saturation)" —
  the natural reading of taleb-51b7's monotone growth: the death rate is not reduced at high
  load, it is **zero** (the latch), and below the latch there is no queue at all (20261016-0213).
- "A bigger engine budget softens the ruin band": it only moves the latch threshold
  N_freeze = b/(2s) linearly in b — at 10⁹-goal N nothing affordable reopens the drain
  (20261016-0213, code + measured s; the M1 numbers re-measure there).

## Open directions

1. **Reopen the drain by the candidate set**: measure S after a bounded-neighbourhood finder
   (the radial window's own certificate, or the co-orbital phase-neighbour tier) at the flown
   N — success is S < b/2, i.e. B = 0 under burn; that adoption deletes the answer bill and
   both caps' paths (nladder's open direction 2 gains its meter).
2. **The reuse traffic**: every mint is pushed twice (one `same_inputs` duplicate per new
   scan). Harmless here (the duplicate answers free through the memo), but a stationary-player
   workload would fill SCAN_BACKLOG with duplicates — which cap bites first then is unmeasured.
3. **The latch's escape**: `scan_ns`'s running-max decay (`universe.rs:1205`) could be fed by a
   periodic cheap re-answer or replaced by a per-scan estimate; whether any such change is
   outcome-free is a design question for the integrator (the freeze is load-blind by design:
   "idle time is spent on one only when it fits").

## Contradictions

None open. taleb-51b7's "the answers never fit the 12-ms budget" at 10⁵ is the latch read at
S ≈ 60× b/2; this run names the threshold and the free regime beneath it.

## Runs

- 20261016-0213-dynamics-69f3 (awaiting grade): the scan queue is a one-way latch at S = b/2 —
  free below (B = 0), pure linear birth above (λ = 14.4/s, 115 B/body/scan, N_freeze ≈ 0.8–1.5k
  at b = 5 ms).
