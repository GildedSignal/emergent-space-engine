topic: scan-queue
status: open
closed-by:
valid-while:
updated: 20261016-1120-components-cdf0

# The player's scan queue: birth, service latch, and the ruin band

## Current best

**The latch's S is decomposed into its two halves on shipped flights, and the cure has its
measured slack: the answer half reads 46–481 bodies per hit found (4.5–8.5 µs a read, one
cartesian readout each) while the nearest non-hit candidate sits at a median ~10³ × reach
— three orders of certificate slack a second, key-side angular cut can take — and the
capture half's O(N) term at the plane's own N is a fallback that walks and binding-clones
every body of the universe (0.12–0.19 ms at N=10³, 95% of coast captures) before rejecting
by doll (20261016-1120-components-cdf0, print-only census on the ladder's own flights,
seed 1; outcomes unchanged).** The mechanism is `radial.rs`'s N-relative fallback rule
(`hit + unbounded > bodies/4 + 64` — the density rule a2c1 censused first, 20261014-1511):
Home's compact doll trips it exactly at the plane's flown N (threshold 71–333 at the flown
28–1,076 bodies, against 94–344 kept) and never at 10⁵ (threshold 25,081) — so
69f3's S = s·N is a small-N disease of the plane's own regime, not a belt-scale one, and
at 10⁵ the apsidal filter returns **6 of 100,071** root-doll bodies (5 candidates after
the doll check; [checker]) — the finder is at its floor away from the belt's bins. Priced cure: an angular certificate on
the key (dθ/dt bounded by L/peri²; conjunction needs the phase separation to close to
~(reach+|w|)/r within h) at ~10–20 ns a candidate, no readout, no clone — S falls from
0.15–2.7 ms to ~tens of µs, comfortably under b/2 at any plane N (69f3's open direction 1
success bar), and the held-scan memory (115 B/body held, ~0.45 MB a held scan at the
plane's N) falls with it.
[Checker (silver): every deterministic cell reproduced bit-exact on a clean rebuild, and two
out-of-range flights hold the mechanism — N=10⁴ burn: fallback 0%, reads/hit 46 (the disease
ends between 10³ and 10⁴); N=10⁵ coast: fallback 0% (vs 95% at 10³) while the answer half
persists (kept 183, reads/hit 267, min-miss 487). The capture-half mechanism and the
write-once speed_cap window poisoning (a2c1, 20261014-1511, nladder.md) precede this run;
the flown universe peaks at 1,076 bodies (threshold ≤ 333, not the dossier's 597), and the
belt-bin regime stays unmeasured.]

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
makes the seam free, not merely cheaper; fences stay guards. [cdf0's decomposition relocates the
"at 10⁴ S ≈ 3–6× b" reading: at those N both halves are ∝ N through the fallback and the whole-doll
answer; away from the plane's regime the filter keeps the root doll near its floor, and what S is
at 10⁴–10⁵ depends on which doll the player is in — re-measure per doll before pricing a cure
there.]

## Refuted

- "The backlog grows because arrivals outpace a sharing service (Kingman near saturation)" —
  the natural reading of taleb-51b7's monotone growth: the death rate is not reduced at high
  load, it is **zero** (the latch), and below the latch there is no queue at all (20261016-0213).
- "A bigger engine budget softens the ruin band": it only moves the latch threshold
  N_freeze = b/(2s) linearly in b — at 10⁹-goal N nothing affordable reopens the drain
  (20261016-0213, code + measured s; the M1 numbers re-measure there).
- "The root-doll finder is the belt-scale seam" (cdf0's own P2, pre-registered): in the 20 s
  ladder flights the apsidal filter returns 6 of 100,071 root-doll bodies (5 candidates) — the finder is at its
  floor there; the O(N) terms live in Home's compact doll and in the fallback rule, both
  plane-regime (20261016-1120). The belt-bin regime (the player inside the belt) stays unmeasured.

## Open directions

1. **Reopen the drain by the candidate set**: measure S after a bounded-neighbourhood finder
   (the radial window's own certificate, or the co-orbital phase-neighbour tier) at the flown
   N — success is S < b/2, i.e. B = 0 under burn; that adoption deletes the answer bill and
   both caps' paths (nladder's open direction 2 gains its meter). [cdf0 prices it: the slack
   is there (median min-miss ~10³ reach, reads/hit 46–481), the certificate is angular on the
   key (L/peri² bounds dθ/dt; no readout), and the capture fallback it must also delete is
   named (the N-relative `bodies/4 + 64` rule). The exact integer form and the belt-bin flight
   are the remaining work.]
2. **The reuse traffic**: every mint is pushed twice (one `same_inputs` duplicate per new
   scan). Harmless here (the duplicate answers free through the memo), but a stationary-player
   workload would fill SCAN_BACKLOG with duplicates — which cap bites first then is unmeasured.
3. **The latch's escape**: `scan_ns`'s running-max decay (`universe.rs:1205`) could be fed by a
   periodic cheap re-answer or replaced by a per-scan estimate; whether any such change is
   outcome-free is a design question for the integrator (the freeze is load-blind by design:
   "idle time is spent on one only when it fits").

## Contradictions

None open. taleb-51b7's "the answers never fit the 12-ms budget" at 10⁵ is the latch read at
S ≈ 60× b/2; 69f3 names the threshold and the free regime beneath it; cdf0 names which doll
and which half carries S at the plane's N (the plane-regime fallback), and that the root-doll
filter is near-floor away from the belt — regime, not contradiction.

## Runs

- 20261016-0213-dynamics-69f3 (awaiting grade): the scan queue is a one-way latch at S = b/2 —
  free below (B = 0), pure linear birth above (λ = 14.4/s, 115 B/body/scan, N_freeze ≈ 0.8–1.5k
  at b = 5 ms).
- 20261016-1120-components-cdf0 (this run, awaiting grade): the scan's candidate set censused —
  reads/hit 46–481, µs/read 4.5–8.5, median min-miss ~10³ reach; the O(N) capture term is the
  N-relative radial fallback walking the universe at the plane's N (0.12–0.19 ms at 10³, 95% of
  coast captures); root-doll filter returns 6/100,071 in these flights; the angular key certificate
  priced with three orders of slack.
