topic: nladder
status: open
closed-by:
valid-while:
updated: 20261018-1717-inversion-d839

# The N ladder: 28 live bodies toward 10⁹

## Current best

**NEW (d839, inversion — the time axis flown past one full doll step): the per-body memory wall is a
constant, not a ratchet in play time.** The longest ladder-scale flight in the record (45,498 game-s
at 3×10⁴ and 10⁵, coast, rtf 100 — 2.3× the 20,000-gs horizon of every prior ladder-scale wave
flight [checker: the record's longest flight of any kind, 25,899 gs at K=10³ (acf2's checker),
still ends before the first step's boundary], and the first past a complete root-doll step) crosses
**three belt-wide item waves**: the mid-step kick wave (13.5–14.5k gs,
+30.5k/+99.9k kicks, footprint +2.2–2.4 KB per body: 2,348–2,378 B at build → 4,790–4,963 B steady),
the step-end `What::Boundary` wave (27.5–28.5k, +25k events, ~0 kicks, footprint flat), and the
**second kick wave (41–43.5k, +107k kicks at 10⁵): footprint +1–2 MB = +0.2–0.7%** — the scoreboard's
"~5,100 B after the first kick" is a constant of the kicked state, now measured through a repeated
cadence, not projected (ladder.txt break 2's "4 GiB at ~1.7×10⁶" stands as a body-count wall). The
compiled-orbit catalogue is constant across waves (30,076 / 100,076: retire releases the old key);
`Universe::prune`'s causality horizon (`now − 2·light_distance − 2²⁶`, `oldest` = nearest pending
item) drops each superseded binding within one wave-gap of margin ~5–9× [inference beyond the two
flown kick waves]; F1 holds at both kick waves (0 frames over 12 ms, max 11.8/11.97 at 3×10⁴/10⁵);
counters bit-identical across executions (kicks 131,047 twice). Two corrections to the rung's own
reading: the 20-s rung under-reads the steady per-body event rate ~11× (9.79e-5 over a full step at
10⁵ vs 8.5e-6 at 10⁶ over 20 s — break 1's CPU arithmetic should use the step-inclusive rate), and
the wave map is kick-mid / boundary-end per step, one step ≈ 27.6k game-s (belt first items
13,051–14,542; kick waves at 13–15k and 41–43.5k, boundary waves at 27.5–28.5k and 55–58k). Unflown by the author: the burn at this
horizon (13.5× mints, 2403) [checker: flown, see below], N ≥ 10⁶ (build ~2.4 GB > the lab cap),
a pinned-`oldest` scene (a certificate on `oldest ≥ now − margin` would close prune's freeze door),
and terms with periods above one step (45.5k gs ≈ 0.6% of a Cinder period) (20261018-1717-inversion-d839,
inversion; shipped `nladder` + print-only /proc probe every 500 game-s, `LADDER_CAP_S`; regen.sh ~3 min).**

[Checker d839, three fresh arms, all outside the author's grid. N=10⁴ (the author's held-out N)
coast to 45.5k gs: RSS 54–55 MB flat through kick₂, bpb 1,405–1,437, cat 10,076 constant, 0 over.
10⁵ coast to 58,500 gs — past a second step end: the boundary₂ wave (+~100k events, kicks flat)
moves RSS 0 MB at 479, so the "[inference beyond the two flown kick waves]" is now measured through
four belt-wide waves. The burn at 3×10⁴/45.5k gs (the named-unflown arm): the per-body terms hold
(bpb 1,410→1,477, cat 30,076, RSS flat 571 MB through kick₂) but resident memory grows 150→571 MB
between the waves (~+13–14 MB per 1k gs over 15k–40.5k gs, then flat; held 38→193) — a play-time
ratchet in the MINT channel (2403's λ·(K+38)·224 law), not in the history terms: the headline's
scope (coast; history+catalogue terms) is load-bearing, and dashboard bpb cannot referee it alone.]
[Second checker d839, blind; three fresh arms. 3×10⁴ coast to 75,898 gs (time, outside every prior
flight): boundary₂ (55–58k, +43k events) and the **third kick wave** (69–72k, +33k kicks ≈ one per
body) both crossed — RSS 149→150 MB, bpb back to 1,417 after kick₃, cat 30,076, held 0, 0 over:
the "[inference beyond the two flown kick waves]" is flown through five belt-wide waves. 3×10⁵ (the
next decade): build 705 → steady 1,431 MB (the same 2.0×), ≈5.0 KB/body steady RSS, bpb 1,409, cat
300,076, kicks 2.24/body, held 0. Burn 3×10⁴/45.5k re-flown independently: same numbers (bpb 1,477,
cat constant, RSS 571 flat through kick₂; growth ~15 MB/1k gs here — held is load-elastic). Caveat on
the rate correction: "~11×" divides 10⁵-with-locals by the 10⁶ rung; same-N, locals-out, the steady
belt rate is ≈6.3e-5 ev/b/gs ⇒ ~7.4× the rung's 8.5e-6 — the order and the mechanism (the rung's
2,000-gs window ends before the first wave) hold, the constant is convention-dependent.]

*[Prior best retained below — 2403's wildcard pacing, acf2's mint law, 96f6's frame decomposition,
7581's crowd cure, and the rest of the page's standing record are unchanged by this run.]*

## Refuted
- **"Memory per body might grow with every cadence wave" (this run's own pre-registered ratchet
  hypothesis, P2's falsifier — and the unspoken assumption behind quoting only first-kick bytes)**:
  measured flat through the second full kick wave and the boundary wave at 3×10⁴ and 10⁵
  (+0.2–0.7% per wave); the steady state is one retired + one current binding per body
  (20261018-1717-inversion-d839).

## Open directions
1. *(existing directions unchanged; add)* The burn flight past one full doll step (the burning
   wildcard's scan channel and the wave's memory under 13.5× mints, together unflown); and a
   pinned-`oldest` probe — a body whose nearest pending item sits in the past would freeze
   `prune`'s horizon and resurrect the ratchet; none exists on the ladder scene, and a certificate
   would close the class.

## Runs
- 20261018-1717-inversion-d839 (inversion, awaiting grade): memory through cadence waves is flat —
  second kick wave +107k kicks at 10⁵ moves footprint +0.2–0.7%; F1 holds at both waves; the steady
  per-body event rate is ~11× the 20-s rung's reading.
