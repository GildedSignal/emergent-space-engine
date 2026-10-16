topic: scan-queue
status: open
closed-by:
valid-while:
updated: 20261016-1740-spacex-3999

# The player's scan queue: birth, service latch, and the ruin band

## Current best

**The belt-bin regime is measured and it latches at every flown N: the player's scan inside the
belt (root doll, r ∈ [1.75, 3.0) AU, a real belt body's own window) falls back and reads
N − 314 doll-0 bodies per answer at 4.07–4.85 µs a read — 2.9–3.1 ms at N = 10³ (the ladder's own rung; the
answer-latch crossing is N ≈ 9×10² (pass = N − 314)), 41 ms at 10⁴, 415–419 ms at 10⁵, with ZERO encounters (nearest
candidate 2.1×10⁶–5.7×10⁷ × reach away, its angular separation 4.2×10⁴–1.1×10⁵ × reach) and the
capture walk — inside the player's item on the frame path, `universe.rs:772` — at 0.046–0.111
µs/body, itself over the 2.5 ms bar from N ≈ 2.5×10⁴ (10.0–11.3 ms at 10⁵)
(20261016-1740-spacex-3999, spacex; print-only `belt_scan_probe.rs` on `plane_with_extra`, seeds
1 + 2 held-out, no engine file touched, per-read reproduces cdf0's 4.5–8.5 µs band and the
player's Home-doll window reproduces its "6 of 100,071" class: kept 8, no fallback at 10⁵).**
The fallback is **belt-band occupancy, not window width**: a radius sweep (one body's v, h) flips
the `bodies/4 + 64` rule at 1.75 AU and releases it at 3.0 AU (kept 3–7 outside the band, 11,184
at 3.0 AU, 10,881 at 1.67 AU) — the edges sit where hit ≈ bodies/4 and so move with N (at 10⁶ the
inner release is 2.0 AU, where the 1.75-AU window keeps 170,188 bodies short of the fallback
[checker2: even outside the rule's trip, the tail windows keep ~0.17·N]); the window itself is narrow (~0.04 AU ≈ 0.36 bins) — what fills
the in-band windows past bodies/4 (the rule's own test: each window spans ~2 bins) are the belt's
eccentricity tails (Rayleigh σ_e = 0.07, redrawn ≤ 0.4) registering every body's whole [peri, apo]
hull, so cdf0's "small-N disease of the plane's own regime" is, in
the belt band, an every-N disease. **And the priced cure's price is wrong as stated:** open direction
1's "an angular certificate on the key … S falls to ~tens of µs" cannot hold soundly — the cheap
axis (mean longitude, from the key + a linear rate) must carry the anomaly margin max|ν−M| ≈ 2e
(exact: 0.1401 rad at e = 0.07, 0.816 at e = 0.4 — already above 2e, so a sound certificate uses
the exact bound and the price only grows [checker2]),
~50× the sweep term 2.9×10⁻³ rad, so a sound
mean-longitude window keeps 4.5–9% of the circle ≈ 4.5–9 × 10³ reads ≈ 19–38 ms at 10⁵ — 8–15×
over the bar; the tight axis (true longitude, ~0.1% kept, 0.4 ms) is itself the 4.2 µs readout,
i.e. no pre-read cut exists on it. The measured ways out: reads ~50× cheaper (the closed-form
kernel's 4.2 → ~0.5 µs lands the fat-but-sound cut at ~2.4 ms, marginal at 10⁵), phase-neighbour
rank along the orbit (the encounters gold `20261006-0346-taleb-09b5`: real encounters within rank
4), or a population-level answer for the belt doll. The flown boundary: the scenario pins the
player to Home's doll, so the end-to-end frame trace with the player resident in the belt is not
flown — every window, walk and read is the shipped decision path, timed on it.

**The latch's S is decomposed into its two halves on shipped flights, and the cure has its
measured slack: the answer half reads 46–481 bodies per hit found (4.5–8.5 µs a read, one
cartesian readout each) while the nearest non-hit candidate sits at a median ~10³ × reach
— three orders of certificate slack a second, key-side angular cut can take — and the capture
half's O(N) term at the plane's own N is a fallback that walks and binding-clones every body of the
universe (0.12–0.19 ms at N=10³, 95% of coast captures) before rejecting by doll
(20261016-1120-components-cdf0, print-only census on the ladder's own flights, seed 1; outcomes
unchanged).** The mechanism is `radial.rs`'s N-relative fallback rule (`hit + unbounded >
bodies/4 + 64` — the density rule a2c1 censused first, 20261014-1511): Home's compact doll trips
it exactly at the plane's flown N (threshold 71–333 at the flown 28–1,076 bodies, against 94–344
kept) and never at 10⁵ (threshold 25,081) — so 69f3's S = s·N is a small-N disease of the plane's
own regime, not a belt-scale one, and at 10⁵ the apsidal filter returns **6 of 100,071** root-doll
bodies (5 candidates after the doll check; [checker]) — the finder is at its floor away from the
belt's bins. Priced cure: an angular certificate on the key (dθ/dt bounded by L/peri²; conjunction
needs the phase separation to close to ~(reach+|w|)/r within h) at ~10–20 ns a candidate, no
readout, no clone — S falls from 0.15–2.7 ms to ~tens of µs, comfortably under b/2 at any plane N
(69f3's open direction 1 success bar), and the held-scan memory (115 B/body held, ~0.45 MB a held
scan at the plane's N) falls with it. [3999's belt-bin measurement supersedes the "at any plane N"
half of this price inside the belt band: at 10⁵ in-belt the same two halves cost 10 ms + 418 ms,
and the angular certificate's sound form keeps 4.5–9%, not ~0.1% — see above.]
[Checker (silver): every deterministic cell reproduced bit-exact on a clean rebuild, and two
out-of-range flights hold the mechanism — N=10⁴ burn: fallback 0%, reads/hit 46 (the disease
ends between 10³ and 10⁴); N=10⁵ coast: fallback 0% (vs 95% at 10³) while the answer half
persists (kept 183, reads/hit 267, min-miss 487). The capture-half mechanism and the
write-once speed_cap window poisoning (a2c1, 20261014-1511, nladder.md) precede this run;
the flown universe peaks at 1,076 bodies (threshold ≤ 333, not the dossier's 597), and the
belt-bin regime stays unmeasured. [Superseded by 3999: now measured — see above.]]

**The burn's scan backlog is a one-way service latch, not a load-sharing queue
(20261016-0213-dynamics-69f3, dynamics lens, shipped code + a print-only counter patch).**
`drain_scans` answers only while the frame's leftover room `≥ 2·max(scan_ns, 0.75 ms)` (the margin
floor), and `scan_ns` decays only through served answers — so once one answer costs more than half
the room (b = the engine budget; S = s·N, s = 1.7–4.2 µs/body across seeds **and runs** at the same
N+seed: 2.97 author / 4.20 regen / 3.35 checker; the latch holds the worst, coldest answer — steady
flush S is 2.1–2.5 µs/body) the drain freezes **permanently**, burn and coast alike (exactly
one answer ever, then none; checker: at b = 1 ms even that one never runs, the margin floor alone
freezes). Below the latch the seam is free: B ≤ 4 (one frame's mint before its drain), 0 at rest,
58/58 scans answered at N ≤ 1000 (seed 7). Above it a pure linear birth: λ = 14.4 holds/s
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
"at 10⁴ S ≈ 3–6× b" reading: at those N both halves are ∝ N through the fallback and the
whole-doll answer; away from the plane's regime the filter keeps the root doll near its floor, and
what S is at 10⁴–10⁵ depends on which doll the player is in — re-measure per doll before pricing a
cure there. [3999: measured — in the belt doll, S = (N − 314) × 4.2 µs at every N; the "≈ 60× b at
10⁵" figure is in fact ~340× b/2 in-band.]]

## Refuted

- **"The fallback is a small-N disease of the plane's own regime" (cdf0's scoping), as a general
  reading: in the belt band it is an every-N disease — the eccentricity tails' range-hull
  registration fills every in-band window past bodies/4 (each spans ~2 bins) from N ≈ 700, so the
  `bodies/4 + 64` rule trips
  for any in-belt window at every flown N (measured 10³/10⁴/10⁵, seeds 1+2, and 10⁶ + seed 3 by
  checker2; the radius sweep pins
  the band to [1.75, 3.0) AU at 10⁵ — the edges move with N, see above) (20261016-1740-spacex-3999).**
- **Open direction 1's price as stated ("an angular certificate on the key … S falls from
  0.15–2.7 ms to ~tens of µs"): unsound as worded at belt e — the mean-longitude axis must carry
  max|ν−M| ≈ 2e (0.1401 rad at e = 0.07; the exact max runs slightly above 2e — see above), ~50× the 2.9×10⁻³ rad sweep term, keeping 4.5–9% of the
  circle ≈ 19–38 ms of reads at 10⁵; the tight true-longitude axis (~0.1%, 0.4 ms) is itself the
  4.2 µs readout, so no pre-read cut exists on it (20261016-1740-spacex-3999; the sweep term
  itself is cdf0's, unchallenged).**
- "The backlog grows because arrivals outpace a sharing service (Kingman near saturation)" —
  the natural reading of taleb-51b7's monotone growth: the death rate is not reduced at high
  load, it is **zero** (the latch), and below the latch there is no queue at all (20261016-0213).
- "A bigger engine budget softens the ruin band": it only moves the latch threshold
  N_freeze = b/(2s) linearly in b — at 10⁹-goal N nothing affordable reopens the drain
  (20261016-0213, code + measured s; the M1 numbers re-measure there).
- "The root-doll finder is the belt-scale seam" (cdf0's own P2, pre-registered): in the 20 s
  ladder flights the apsidal filter returns 6 of 100,071 root-doll bodies (5 candidates) — the finder is at its
  floor there; the O(N) terms live in Home's compact doll and in the fallback rule, both
  plane-regime (20261016-1120). [Half-reopened by 3999: the root-doll finder is at its floor only
  OUTSIDE the belt band; inside [1.75, 3.0) AU it falls back at every flown N.]

## Open directions

1. **Reopen the drain by the candidate set**: measure S after a bounded-neighbourhood finder
   (the radial window's own certificate, or the co-orbital phase-neighbour tier) at the flown
   N — success is S < b/2, i.e. B = 0 under burn; that adoption deletes the answer bill and
   both caps' paths (nladder's open direction 2 gains its meter). [cdf0 prices it: the slack
   is there (median min-miss ~10³ reach, reads/hit 46–481), the certificate is angular on the
   key (L/peri² bounds dθ/dt; no readout), and the capture fallback it must also delete is
   named (the N-relative `bodies/4 + 64` rule). The exact integer form and the belt-bin flight
   are the remaining work.] [3999 re-prices it in the belt band: the belt-bin flight is done
   (this run) and the sound mean-longitude form keeps 4.5–9% (19–38 ms at 10⁵) — the certificate
   alone cannot clear the bar there; compose it with the phase-neighbour rank or ~50× cheaper
   reads, or answer the belt doll at population level. Outside the band the price stands.]
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
filter is near-floor away from the belt — regime, not contradiction. 3999 extends the same fence
into the belt band (occupancy-driven fallback, every N) and re-prices the cure there; cdf0's
plane-N price stands outside the band, and its belt-bin prediction slot is now filled with a
measurement.

## Runs
- 20261016-0213-dynamics-69f3 (awaiting grade): the scan queue is a one-way latch at S = b/2 —
- 20261016-1120-components-cdf0 (awaiting grade): the scan's candidate set censused —
- 20261016-1740-spacex-3999 (awaiting grade): the belt-bin regime measured — in-belt fallback at
  every flown N, answer (N − 314)×4.2 µs (latch from N≈9×10²), zero encounters, and the angular
  cure's sound price is 4.5–9% kept, not ~0.1%
