# Dossier — 20261020-1002-inversion-0a46 (inversion lens)

## Claim

The "wave" the record prices once is a **standing comb**: the belt's own clock stream
arrives as a ~1.1-events-per-body era every 13.9-14k game-s, undecayed through four
eras (60k game-s) at two seeds and two rungs, present bit-for-bit on coast with no
player at all — so ca63's "13.2 h/wave at 1e9" is a **per-14k-gs recurring floor**, not
a one-time cost; and the freeze that rides it is a separate, alternating channel
(718/42/339/12 ms worst frame across four IDENTICAL-arrival eras), whose clean eras
measure the same arrivals at **~15-17 µs/event vs ~47-50 µs/event in freeze eras — a
3x path price the 1e9 composition has never split**.

## Bottleneck

Board #1 (bodies in the flyable engine, 28 vs 1e9) and PRINCIPLES #12 (smoothness):
every wave-cost composition on the nladder page (2d26's coverage, 476d's crest law,
ca63's 13.2 h/wave) is built on windows covering one, at most two, eras. The inversion:
ask what the newest gold silently assumes — that the wave is an *event*. It is a
*structure*. Gain: the 1e9 crest arithmetic gains a recurrence factor (one wave per
~35 s of wall at play rtf 400, forever) and a measured 3x served-path lever; the
stagger's target is re-specified (delete the standing comb, not "the burst"), and the
ledger (budget-1e9) gains the missing crest-concentration row (~63-75% of the belt's
stream inside ~29% of game time).

## Evidence

Shipped bits (`nladder`, L8 burn, 12 ms budget), my patch print-only
(`ES_FRAME_CSV=1` per-frame CSV; off = shipped — anchor below; Linux /proc footprint
stand-in, disclosed). All flights rtf 400 (play cadence), this Linux box, load ~1.

Anchor (instrument falsity check, CSV off): `nladder 100000 burn 10 2000 12` →
max_ms 817.6, held_max 1,858 — inside the record's shipanchor family
(811.6-817.4; held 1,867). The instrument does not move shipped numbers.

The four arms (2k-gs bins; full tables regenerate via `regen.sh` ~6 min):

| arm | era arrivals (ev/body) | era worst frame (ms) | era wall (s) | µs/event (net) |
|---|---|---|---|---|
| 1e5 burn s1 | 1.117 / 1.118 / 1.110 / 1.088 | **718 / 42 / 339 / 12** | 5.5 / 2.1 / 5.7 / 1.5 | 47 / 17 / 49 / 12 |
| 1e5 coast s1 | 1.110 / 1.122 / 1.047 / 1.092 | 17.6 whole flight (over 2) | 22.3 total | ~11 flat |
| 1.5e5 burn s1 | 1.078 / 1.078 / 1.071 | **1152 / 68 / 641** | 8.0 / 3.1 / 8.3 | 48 / 17 / 50 |
| 1e5 burn s2 | 1.308 / 1.315 / 1.134 / 1.115 | **720 / 43 / 367 / 12** | — | — |

1. **The comb stands.** Era onsets 12k/26k/40k/54k gs (period 13.94k); arrivals
   flat ±1.3% over four eras at 1e5 (1.117→1.088; −2.6% by era 4 — no shear dispersion
   at flight timescales), ±0.7% at 1.5e5. It is **not player-caused**: coast carries
   the same comb at the same period; total kick rate 4.89-5.24e-5/body/gs across all
   four arms = the ledger's λ to the digit. 63-75% of the whole event stream arrives
   inside the ~29% of game time the combs occupy.
2. **The freeze alternates on identical arrivals** (worst frame 17-60x apart across
   eras with the same 1.1/body), same alternation at both seeds and both rungs:
   structural, not a draw. Era-1 freeze follows the K-law (1151.6 ms / 150,028 =
   7.68 µs/body, cc9d's 8.1-9.5). Mechanism unprobed here (needs cc9d's
   items_by_class probe; the player's doll is static all flight, so it is not the doll
   boundary).
3. **The path split (new):** freeze eras serve their identical arrival at
   47-50 µs/event; clean eras at 12-17 µs/event (net of a ~0.25-0.3 s/600-frame
   baseline; raw era walls in the table). The 3x is the price of the gulped nested
   path vs the budgeted drain — measured on the *same* bodies, same arrivals, same
   scene, minutes apart.
4. **Presented time never stalls at play cadence:** 0/600 frames behind (lag = 0)
   in every era, every arm; the wave is paid as over-budget frames, not deferral.

Composition (derived, not flown): waves recur every ~14k gs ⇒ at play rtf 400 one era
per ~35 s of wall. At 1e9, flat-cost crest 13.2 h (ca63) **per 35 s of play**, and the
shipped freeze 7.7 µs × 1e9 ≈ 2.1 h **per 35 s of play** — recurrence, not amortization
of one wave, is what the 1e9 arithmetic must carry. The clean-era path says the crest
floor drops to ~1e9 × 1.11 × 16 µs ≈ 4.9 h/era if every era is served like era 2/4.

## Predictions

Written before any decisive flight (`predictions.md`): P1 HELD (era 3/4 ≥ 0.5/body:
1.110/1.088). P2 REFUTED on its letter (≥400 ms every era; eras 2/4 read 42/12 ms) —
the refutation is the finding: the freeze is a separate, alternating channel, not a
function of arrivals. P3 HELD, stronger than written (0 frames behind, not just
"recovers"). P4 resolved to its second branch (coast: comb without freeze — arrivals
and freeze are separable channels). P5's composition stands, with the recurrence
factor above.

## What would make it wrong

- The comb is this genesis's birth-phase lock; a belt born spread over game time would
  not have it. But the genesis is the shipped law (belt page: "the birth program
  stands, is wired into the law"), so the object measured is the object flown.
- Era-wall baselines (~0.3 s/600 frames) shift the µs/event split by ±5%; the 3x path
  gap survives any plausible baseline.
- x86, one box, load ~1, rtf 400 only: orders of magnitude, per the lab rules; the
  alternation and comb persistence are schedule-independent to the extent tested
  (two seeds, two rungs, burn and coast).
- 4 eras is not forever: decay −1%/period extrapolates to a ~70-period half-life, but
  that is extrapolation, not measurement.

Cost of adoption: zero code change — this re-prices existing numbers. Design
consequences: (1) the stagger must spread *clock phase* by ≥ the comb width (~4k gs),
or the comb re-forms; it is a standing-comb deletion worth ~2.6x crest concentration,
not a wave-1 patch; (2) the served-path 3x is a cheaper lever than any per-event-cost
work: make era 1 look like era 2 (budget-gated service of the crest) and the crest
floor drops 13.2 → ~4.9 h at 1e9 before any kick-cost work; (3) budget-1e9's stream
row needs a crest-concentration row (63-75% of events in 29% of time).

Fit with PRINCIPLES: #3 "Compute only surprises" — the comb is a clock, pure schedule,
the least surprising object in the engine, yet it is what spikes the p99; #12
"minimize spike compute... i care about the p95/99 results i want the game to be
smooth"; #22 "the simulation tells us what's next not us" — the comb is the simulation
telling us the schedule 14k gs in advance.

## The lens

Inversion asked what the newest gold (ca63) silently assumes: that the wave is an
event. It is a standing structure. What the lens may have made me miss: I did not
probe the freeze-alternation mechanism (needs cc9d's per-item probe — the named next
experiment), and I priced only the burn/coast plane scenes; the galaxy/handoff scenes
may comb differently.
