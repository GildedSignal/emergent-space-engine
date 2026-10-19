# Dossier — 20261019-0435-second-20261019-0325-library-9147-1b3f (second author on 20261019-0325-library-9147)

## Claim

The checker's named experiment is flown and the library run's claim now holds on the shipped
record: **the per-reader `oldest` (only the items that can read body i hold its history) deletes
the far item's memory ruin on the shipped engine, and the deletion is bit-neutral** — with 4a71's
far pin live (the same binary, same scene), the global arm staircases on his measured law
(retained 2.50/body at D = 6×10⁹, 5.14/body and 385 MB and 612 frames over 12 ms at D = 1.2×10¹⁰)
while the per-reader arm sits at the control's 1.015–1.016 retained/body, 157 MB RSS, 0 frames
over, full game time, and kicks/events counts bit-identical to the control (211,442/394,163) —
the far item is present in the universe's calendar (gap = D exact) and holds nothing. The
soundness hole the library run named (cross-doll reads) is closed by measurement: the frozen
13-case `ladder_digest` suite is byte-identical flag on vs off, refusals are 0 everywhere, and a
doll-edge-crossing burn under flag+pin reproduces the control burn's handoffs, doll switch
(frame 948), kicks and events exactly.

## Bottleneck

Board item 1/4 (bodies toward 10⁹; memory at 10⁹), continuing 4a71's entry and 9147's pricing.
The 9147 checker kept it silver because "the deletion is priced, not flown, and the cross-doll
soundness hole stays open". Expected gain: the far-item term the library run priced at
7.78–10.75 MB/body (median 9.15 at 10⁶) is deleted by rule on shipped code — at the flown rung
the same pin that costs 229 MB and 11% of game time costs 0 MB and 0 frames.

## Evidence

All numbers regenerate by `regen.sh` (~11 min: 10 flights ≤ 100 s + the digest suite twice);
`work/analyze_out.txt` is the folded table, `work/digest-{off,on}.txt` the suite outputs
(md5-identical). Scene: shipped `nladder`, K = 3×10⁴, seed 1, coast rtf 800 (burn/5 ms arms as
marked), 12 ms budget, probe every 2,000 gs; `bodies = 30,028`. Reproduced: `regen.sh` ran
end-to-end a second time (~9 min) with the same verdicts — within each execution the per-reader
arms equal their control to the digit (second run: kicks 211,468 = 211,468) while the global arm
pays the staircase (5.40/body, 389 MB, 571 over); wall-truncated flight totals move a few counts
between executions (211,442 vs 211,468), the arm identities never do.

| arm | retained/body | hist_max | RSS MB | gap s | over 12 ms | p99 ms | game gs | kicks |
|---|---|---|---|---|---|---|---|---|
| control (shipped) | 1.016 | 37 | 156 | 0 (max 1,544 natural) | 0 | 11.94 | 79,142 | 211,442 |
| global pin 6×10⁹ | 2.502 | 1,447 | 282 | 29,553 | 59 | 11.97 | 77,987 | 209,643 |
| global pin 1.2×10¹⁰ | 5.135 | 2,877 | 385 | 59,106 | **612** | 20.82 | 70,211 | 178,712 |
| **per-reader + pin 6×10⁹** | **1.016** | 37 | 157 | 29,553 | **0** | 11.93 | 79,142 | **211,442** |
| **per-reader + pin 1.2×10¹⁰** | **1.015** | 37 | 157 | 59,106 | **0** | 11.93 | 79,138 | **211,442** |
| per-reader, no pin | 1.016 | 37 | 157 | 0 | 0 | 11.93 | 79,142 | 211,442 |
| negative: per-reader + D = 2²⁶ | 1.016 | 36 | 156 | 330 | 0 | 11.94 | (25 s arm) | — |
| control burn (SOI switch) | 0.021 | 17 | 98 | 0 | 0 | 10.83 | 2,398 | 5,651 |
| **burn + per-reader + pin 1.2×10¹⁰** | **0.021** | 17 | 101 | 59,106 | 0 | 10.84 | 2,398 | **5,651** |
| 5 ms corner + per-reader + pin | 0.022 | 24 | 82 | 59,106 | 3 | 4.49 | 1,360 | — |

- **The deletion (P1, P2, P7).** Same binary, same scene, same schedule: the global arm pays
  4a71's ratchet exactly (retained ≈ 1 + ⌊D/5.6×10⁹⌋ + birth structure: 2.50/5.14; +126/+229 MB
  over control = 2.8/1.85 KB per extra retained binding, his 1.9–2.2 KB band; the pin eats the
  frame: 612 over, p99 20.8, game time −11%). The per-reader arm under the same pins: census at
  the control's digits (1.015–1.016), RSS 157 MB, 0 frames over, full game time, and the far
  item's window still reads in the global calendar (`gap_s` = D exact, 59,105.9 s) — measured in
  the same run, the pin exists and holds nothing.
- **Outcome neutrality (P3).** Every per-reader arm's kicks/events/lost/held-refusals/seen equal
  the control's to the digit (211,442 kicks, 394,163 events, 13 lost, 0 held refusals, 30,046
  seen); the global-pin arms lose content only through lost game time (the frame term).
- **The soundness gate (P4).** `ladder_digest`, all 13 cases × 4 schedules: `ES_READER_OLDEST=1`
  vs off — **byte-identical outputs** (`work/digest-off.txt` ≡ `work/digest-on.txt`, md5 equal),
  including the belt-crossing cases where the player crosses into the star's doll (handoffs and
  scans against doll-0 bodies). Engine refusals 0 and held refusals 0 in every flight.
- **Doll-edge crossings (P5).** The burn arms cross Home's SOI (the player's doll [(0,2) →
  (948,0)] in both): handoffs 1 = 1, kicks 5,651 = 5,651, events 17,727 = 17,727, lost 23 = 23 —
  the centre-body reads at step.rs:795/804 never hit pruned history.
- **The negative control (P6).** D = 2²⁶ under the rule: census equal to the control's (the knob
  is inert below the natural gap), and per-reader without any pin equals the control too — at one
  star the rule changes nothing measurable, exactly the library run's "retained 1/body" row.
- **The adoption hazard, found in flight (this run's own finding).** The per-doll calendars the
  rule needs go **stale on handoffs**: a ship leaving doll d leaves its slot behind, pinning d's
  minimum at the handoff tick forever. Measured: doll 2's min walked to 15,641 s behind now,
  ~400 bodies' histories leaked (+54k segments by 50k gs, RSS 156 → 242 MB, bisected to the
  own-doll term with modes 2/3/4); the fix is one loop in `apply` (clear the foreign-doll
  slots). The one-calendar `child_ticks` cannot go stale this way — the pattern does not
  generalize for free, and the stale-slot failure mode is the very ruin the rule deletes,
  reappearing at doll scale.

Implementation (all in `work/patch.diff`): `doll_ticks: Vec<Calendar>` kept by `apply` (own doll
set, foreign cleared), `prune`'s threshold per body `min(now − keep, oldest_i − 2²⁶)` where
`oldest_i` = min over the body's own doll, the dolls it is a source of, and the dolls it centres
(each doll's minimum from its ship calendar plus the planets/moons/player folded in); 4a71's
probe verbatim (footprint, knobs, census/gap lines) plus `ES_PIN_OLDEST` unchanged. Off = shipped
bit for bit; the reader relation covers every history reader in the code (`ctx.state_of` via
`secondaries`, `ext::source`, the handoff centre reads, the scan's same-doll captures, the view's
keep term, the ramp walk's `len > 1` guard).

Commands (each ≤ 60 s where marked; the whole grid ≈ 10 min): `sh flights.sh` (the 10 arms),
`python3 analyze.py`, the digest pair in `regen.sh`.

## Predictions

`predictions.md` was written before the decisive flights (after the smoke test, before the grid).
P1 held (1.015–1.016 in the pre-registered [1.00, 1.10] band against the global arm's 2.50/5.14).
P2 held (0 ≤ 10 over, game time within 2%: 0.005%). P3 held to the digit. P4 held (byte-identical
suite). P5 held (948 = 948, 1 = 1 handoffs). P6 held. P7 held (gap = D exact in the reader arms).
No kill criterion fired. Two events the predictions did not cover, both disclosed: the shared
target-dir clobber (below) and the stale-slot leak (found by the pre-decisive check, fixed before
the grid; both flights shown in the log).

## What would make it wrong

1. **The pin is still simulated.** No far doll exists (`range` refuses past ~6 AU); the pin
   injects the far item into the global calendar and the rule scopes it out by construction. A
   real far-doll wiring (E9) must keep far ships out of near reader sets — the same one-line
   scope, but the day it lands is the day this closes for good.
2. **The reader relation is proven complete only against this code's read paths** (the tells:
   `Refused("history pruned")` at ctx.rs:62, ext.rs:134, observe.rs:157/189, step.rs:795/804, the
   scan's silent candidate skip, the digest). A new reader kind (the Binet cone, E9 fleets)
   re-opens the question; the digest suite is the standing gate.
3. **The 10⁶/10⁹ rows remain arithmetic** on the measured constants (the library run's band);
   this run measures the mechanism and its neutrality at 3×10⁴ and one star.

**Cost of adoption:** small and now measured — the rule, the calendars (one `Calendar` per doll,
the `child_ticks` pattern plus foreign-slot clearing), and the digest suite as the gate; frame
cost at the flown rung is nil (p99 11.93 both arms). **Fit with PRINCIPLES:** "his direct
influence is bounded and propagates at c at most… light cones partition compute" (P5) — retention
keyed on the reader's light cone is the same law; "a fix signals the wrong representation" (P19)
— the margin dial was the bandaid, the scope is the representation change; the stale-slot find is
P19 again, caught in the act.

## The lens

The second-author lens inherits the checker's one experiment and flies it; what it may have
missed is everything the experiment was NOT: no far-doll wiring, no 10⁶ rung (2.34 GB build, over
this window's cap), one seed, one scene shape. The run also pays the lab a process finding: the
family-default target dir (`lab-target-2`) is shared by the window's concurrent runs, and its
binaries are clobbered mid-flight — this run's first grid silently ran a foreign binary (caught
by the probe lines vanishing; the `prune:`/probe prints are the tell every future flight should
keep). The fix (a private `CARGO_TARGET_DIR`) is in `regen.sh`.
