topic: scan-queue
status: open
closed-by:
valid-while:
updated: 20261016-2229-quant-7343

# The player's scan queue: birth, service latch, and the ruin band

## Current best

**The read is priced from the inside and the cheap-reads cure is dead: the tube solve's own
arithmetic (`entry.trajectory.state`) carries 85–90% of an in-belt fallback read (3.3 µs of
a 3.7–4.0 µs read; 74–86% in kept/edge windows, where the non-solve stages peak at 26%),
warm≈cold (1.10–1.15×) with 7-knot tables and one compiled Entry per body (nothing shared,
nothing to keep hot), the integer predicate ~5%, the Scalar wrap ~2–4%, the turn+fit ≤1%,
and one checked Scalar `mul` is 3.3 ns — so the solve is ~10³ mul-equivalents and deleting
every wrapper around it buys ~1.15× mid-band (1.35× in the worst kept arm), never 2×
(20261016-2229-quant-7343, print-only `read_split.rs`, shipped decision path verbatim; 3
probes × seeds 1+2 × N = 10³/10⁴/10⁵; 3999's answers regenerated: 2.9/37–39/398–402 ms on
regen, 0 encounters everywhere; per-read 3.8–4.4 µs in the author's arms, and NOT a
constant — a held-out seed's kept edge window reads at 6.0 µs on 8.9-knot tables: the
price is population-dependent, the share is not).** Consequence: of 3999's three
named ways out, "~50× cheaper reads" cannot come from this representation's readout (a
trivial-math read would be a re-certified readout law, owning its full ~85–90%); the live
cures in the belt band are not-reading — the phase-neighbour rank (the encounters gold:
real encounters within rank 4) or the population-level answer. Two new small terms
measured: the capture **reuse** walk re-walks the whole candidate list before
`same_inputs` hits (`capture` builds its candidates before the memo check,
`encounter.rs:174–194`; 23 µs at 10³ kept, 2.1–3.1 ms at 10⁴, 30–34 ms at 10⁵ — under
69f3's λ = 14.4 mints/s that is 0.24–0.5 s/s of wall at 10⁵, duplicates-only to
all-mints), and the belt band's edges leak partial windows (out-of-band picks kept
87–1055 bodies, not single digits; per-read share unchanged there).
[Checker (gold): every load-bearing cell regenerates — clean re-run of seed 1, plus
held-out seed 3 and N = 10⁶ seed 3, one decade past the author's range: fallback at all
three probes, candidates = distinct entries = 999,714, 0 encounters, 3.87–3.94 µs/read,
traj 87–89%, warm 1.12–1.15×, reuse walk 310–321 ms. The dossier's 10³/10⁵ timing cells
and its "(89%)" annotation on the kept s2-lo row are the author's single runs (≤10% off
regen; that row computes 80%); the "per-read 3.6–4.5 µs everywhere" constancy is
falsified at seed 3's edge window (6.0 µs) — none of it touches the kill.]
[checker2: independent clean runs agree — seed 5 at 10⁴/10⁵ (share 85.5–89.6%, reuse 30–31 ms)
and 10⁶ seed 5, one decade past the author's range: fallback at all probes, candidates = distinct
entries = 999,714, 0 encounters, share 77.5–91.6%, warm 1.13–1.20×, reuse 330–358 ms (linear in N:
~5 s/s of wall at 10⁶ under 69f3's λ — the fix is worth more as N grows; a 10⁶ arm costs ~3.0 GB
RSS, stay ≤ 3×10⁵ inside a 2 GB box); the instrumented stages close against the untimed answer
path to 3%, and a reps-1 arm rules out the warm-loop artifact. kick-jet cd6e's whole-read timing
(shipped read ~4 µs flat in e, closed form at warm parity) independently corroborates the kill's
closed-form half.]

**The priced cure's first half is built and measured: an angular certificate on the tube's own
knot table (`ES_SCAN_CERT`, 20261016-1740-quant-1250) kills 66–80% of the answer's candidates
(89–91% of bound cycles) at 0.2–0.46 µs each — cdf0's 10–20 ns pricing was 20–45× optimistic —
with outcomes bit-identical on every scheduled flight and every unstarved wall-paced control
(checker: also fresh seeds +100, 10 s horizon); the answer bill falls 2.2–2.8× (coast N=1000:
1871→659 µs mean; burn: 776→345 µs), the burn backlog 13× at 10⁴ — but the latch at the
plane's own N=1000 burn survives (held 580→491): the drain gates on `2·max(scan_ns, 0.75 ms)`,
a running **max**, and the worst early answer (a fallback capture's whole-doll list, 61% of
whose surviving reads are Passage readouts the certificate cannot touch) still sets it. Mean
S < b/2 at every rung; the max-gate does not follow.** [1250's checker (silver): four
record cells do not regenerate (flight count, prediction 2's ~10×, the unconditional
bit-identity headline under load, the 26× N=300 backlog); the certificate itself was never
caught changing an outcome.]

**The belt-bin regime is measured and it latches at every flown N: the player's scan inside
the belt (root doll, r ∈ [1.75, 3.0) AU) falls back and reads N − 314 doll-0 bodies per answer
at 4.07–4.85 µs a read — 2.9–3.1 ms at 10³, 41 ms at 10⁴, 415–419 ms at 10⁵, ZERO encounters
(nearest candidate 2.1×10⁶–5.7×10⁷ × reach away) and the capture walk at 0.046–0.111 µs/body
(20261016-1740-spacex-3999, `belt_scan_probe.rs` on `plane_with_extra`, seeds 1 + 2).** The
fallback is **belt-band occupancy, not window width**: the `bodies/4 + 64` rule flips at
1.75 AU and releases at 3.0 AU, the edges moving with N; the belt's eccentricity tails
(Rayleigh σ_e = 0.07, redrawn ≤ 0.4) register every body's whole [peri, apo] hull, so it is an
every-N disease in-band. A sound mean-longitude certificate keeps 4.5–9% of the circle ≈
19–38 ms at 10⁵ (8–15× over the bar); the tight true-longitude axis is itself the 4.2 µs
readout. Measured ways out: ~50× cheaper reads, phase-neighbour rank, or a population-level
answer. [7343: the first is now killed — see above; the read cannot get cheaper by deletion
(the closed-form kernel's cheaper read survives only as a re-certified law, not an
optimization of this readout).]

**The latch's S is decomposed into its two halves on shipped flights (20261016-1120-cdf0):
the answer half reads 46–481 bodies per hit at 4.5–8.5 µs a read while the nearest non-hit
candidate sits at a median ~10³ × reach — the certificate slack — and the capture half's O(N)
term at the plane's N is a fallback that walks and clones every body (0.12–0.19 ms at N=10³,
95% of coast captures) before rejecting by doll.** Home's compact doll trips the N-relative
rule exactly at the plane's flown N (threshold 71–333) and never at 10⁵ (threshold 25,081;
the apsidal filter returns 6 of 100,071 there) — the plane's fallback is a small-N disease;
the belt band's is not.

**The burn's scan backlog is a one-way service latch, not a load-sharing queue
(20261016-0213-dynamics-69f3): `drain_scans` answers only while the frame's room ≥
2·max(scan_ns, 0.75 ms), `scan_ns` decays only through served answers, and once one answer
costs more than half the room the drain freezes permanently** (exactly one answer ever, then
none). Below the latch the seam is free; above it a pure linear birth λ = 14.4 holds/s
(N- and seed-independent), memory 115 B/body per held scan, ruin at SCAN_BACKLOG (2048),
≈ 142 s at any N whose pin fits RAM. No budget tuning reopens service at belt scale; the
criterion is **S < b/2 at the player's own N**.

## Refuted

- **"Reads get ~50× cheaper" (3999's first named way out, as a deletion on the shipped
  readout): killed — the tube solve is 85–90% of a fallback read (74% in the cheapest kept
  arm), warm≈cold (tables 7 knots), every candidate a distinct compiled Entry, one Scalar
  mul 3.3 ns (the solve is ~10³ ops), and all non-solve stages total 10–26%, never the 50%
  a 2× needs (20261016-2229-quant-7343). A cheaper read is a new certified readout law,
  not an optimization.**
- **"The fallback is a small-N disease of the plane's own regime" (cdf0's scoping), as a general
  reading: in the belt band it is an every-N disease — the eccentricity tails' range-hull
  registration fills every in-band window past bodies/4 from N ≈ 700 (measured 10³/10⁴/10⁵,
  seeds 1+2, and 10⁶ + seed 3 by checker2; band [1.75, 3.0) AU at 10⁵, edges move with N)
  (20261016-1740-spacex-3999).** [7343 sharpens the edges: partial windows leak 87–1055 kept
  bodies at the band boundary — not a cliff; the traj share is unchanged there, the per-read
  price is not (6.0 µs on a held-out seed's edge population, checker).]
- **"The angular certificate reopens the drain at the player's own N" (cdf0's pricing, 1250's
  prediction 3, half-right): the certificate is real, conservative and cheap (bit-identical
  outcomes, 66–80% kills), and the answer **mean** falls under b/2 at every rung — but the
  drain gates on the running max `scan_ns`, which the unkillable Passage readouts keep above
  room/2 at N=1000 burn (held 580→491). Means do not reopen a max-gated latch
  (20261016-1740-quant-1250).**
- **Open direction 1's price as stated ("an angular certificate on the key … S falls from
  0.15–2.7 ms to ~tens of µs"): unsound as worded at belt e — the mean-longitude axis must
  carry max|ν−M| ≈ 2e, keeping 4.5–9% of the circle; the tight true-longitude axis is itself
  the 4.2 µs readout, so no pre-read cut exists on it (20261016-1740-spacex-3999).**
- "The backlog grows because arrivals outpace a sharing service (Kingman near saturation)" —
  the death rate is not reduced at high load, it is **zero** (the latch); below the latch
  there is no queue at all (20261016-0213).
- "A bigger engine budget softens the ruin band": it only moves N_freeze = b/(2s) linearly —
  nothing affordable reopens the drain at 10⁹-goal N (20261016-0213).
- "The root-doll finder is the belt-scale seam" (cdf0's P2): at its floor only OUTSIDE the
  belt band; inside, fallback at every flown N (20261016-1740-3999).
- "Some rung or gate would catch a missing impulse"-class readings: see contact-speed; the
  ledgers stay exact through whatever the scan skips.

## Open directions

1. **Reopen the drain by the candidate set.** The certificate half is done (1250: built,
   measured, outcome-free; the answer mean is under b/2 at every rung — the max-gate is the
   binding term). What remains, re-priced by 7343: **(a)** in the belt band the only live
   cuts are not-reading — the phase-neighbour rank (encounters gold `20261006-0346`: real
   encounters within rank 4 along the orbit; O(n·k) reads at 3.7 µs each) or a
   population-level answer for the belt doll; a cheaper read must be a re-certified readout
   law (85–90% of the read is the solve); **(b)** the answer tail at plane N — Passage readouts
   carry no bound cycle (a passage-side certificate or exclusion); **(c)** the capture
   fallback (95% of burn captures at N=1000) still walks and clones every body; and now
   **(d)** the reuse walk — the memo hit re-walks N bodies per duplicate mint (30–34 ms at
   10⁵, 0.24–0.5 s/s under burn, duplicates-only to all-mints): memo the candidate list per
   (body, t, interval) instead, an
   outcome-free scheduler-side fix for the integrator to judge. Then re-measure the latch's
   worst answer.
2. **The reuse traffic**: every mint is pushed twice (one duplicate per new scan). With (d)
   above the duplicate becomes free; without it, a stationary player fills SCAN_BACKLOG with
   duplicates — which cap bites first is unmeasured.
3. **The latch's escape**: `scan_ns`'s running-max decay could be fed by a periodic cheap
   re-answer or replaced by a per-scan estimate (candidates × a measured per-candidate cost —
   7343's stage table is that price list: 3.7 µs/read in-band, 0.2 µs a certified candidate
   by 1250). Whether any such change is outcome-free is a design question for the integrator.

## Contradictions

None open. 1250's max-vs-mean reading refines cdf0's success bar; 3999 extends the fence into
the belt band and re-prices the cure there; 7343 kills the cheaper-reads third of that price
and leaves the other two. 3999's "kept 3–7 outside the band" and 7343's kept 87–1055 at the
band boundary are the same edge at different distances out (partial windows whose position
moves with N and seed); recorded so no run reads the band as a cliff.

## Runs
- 20261016-0213-dynamics-69f3 (awaiting grade): the scan queue is a one-way latch at S = b/2 —
- 20261016-1120-components-cdf0 (awaiting grade): the scan's candidate set censused —
- 20261016-1740-quant-1250 (awaiting grade): the angular certificate built on the knot
- 20261016-1740-spacex-3999 (awaiting grade): the belt-bin regime measured — in-belt fallback at
- 20261016-2229-quant-7343 (this run, awaiting grade): the in-belt read decomposed — 85–90%
  is the tube solve's own arithmetic, warm≈cold, non-solve stages 10–26%; the
  ~50×-cheaper-reads cure dead; reuse walk 30–34 ms a duplicate mint at 10⁵.
