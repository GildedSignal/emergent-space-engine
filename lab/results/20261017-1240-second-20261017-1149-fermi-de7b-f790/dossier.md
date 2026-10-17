# The checker's named experiment, flown: `BELT_SPLIT` carries the boundary comb — and the claim holds

## Claim

de7b's gold, second check. The run's two named misses are closed here, and the claim stands
on all of them: **(1) the transfer to `BELT_SPLIT` is no longer an inference from 98cb's
8.000× first-kick anchor — the actual split patch (98cb's `work/patch.diff`, crates side,
`BELT_SPLIT=1`) was flown with de7b's per-body comb instrument, and the boundary comb
stretched 8× with the kick comb, still welded at its midpoint, in 9,700/9,700 belt bodies**
(h p50 112,565 game-s = 8.0005× shipped; scan between the stretched crests: B/2h,
(K−B)/h, interval/2h all 1.0000; 4 fired events per body by 4.09 stretched intervals —
K,B,K,B from h, the exact shipped shape; per-body stream rate 0.1250× shipped = 1/8 exact).
**(2) One seed only:** seeds 2 and 3 at the shipped lever hold everything to the digit
(h p50 14,075 / 14,073; 9,700/9,700 welded; identities 1.0000; 4 events; dead 0). The
record itself regenerates: arm 7, arm 6 and arm 8 reproduce de7b's logs byte for byte on
the `ladder:` line, and the ledger recomputes unchanged (79.71/9.96/3.85 M1 riding,
15.67-core pinned floor, S\* = 19.9×). The 10⁹ ledger's riding branch is now measured on
the direct flight, not transferred by anchor: the ~15.7-M1-core boundary floor is dead.

## Bottleneck

The same one de7b answered (the board's 10⁹ row, kick-cadence open direction 1). What this
run removes is the residual risk the first checker named: the whole "closable at S\* ≈ 20×"
consequence rested on one indirect anchor (98cb's first-kick measurement) plus a mechanism
argument. If the split had stretched only the kick comb, the boundary alone would pin
~15.7 M1 cores at 10⁹ at every split — a factor-4 overshoot hiding behind an unflown
composition. The direct flight kills that possibility on the real patch, for the cost of
one 90-s run.

## Evidence

All numbers from this machine (Linux x86, shared, 8 vCPU), `IMPACT_GUESS=0` throughout,
`STAGGER_GENESIS` unset; the tree is shipped main + de7b's instrument (extended: `<seed>`
argument, h<60k/h≥60k genesis mixture counter, flight guard 55 s → 140 s — this box is
loaded and delivery is compute-bound at ~6,300 game-s/s) + 98cb's crates patch unmodified.

| arm | h p50 (game-s) | welded pairs at scan | B/2h | (K−B)/h | interval/2h | belt events/body | rate vs shipped |
|---|---|---|---|---|---|---|---|
| 6 (2× coarse) | 28,141 | 9,700/9,700 | 1.0000 | 1.0000 | 1.0000 | 2 | 0.2500× |
| 7 shipped, seed 1 | 14,071 | 9,700/9,700 | 1.0000 | 1.0000 | 1.0000 | 4 | 1.0000× |
| 7, seed 2 | 14,075 | 9,700/9,700 | 1.0000 | 1.0000 | 1.0000 | 4 | — |
| 7, seed 3 | 14,073 | 9,700/9,700 | 1.0000 | 1.0000 | 1.0000 | 4 | — |
| 8 (2× fine) | 7,035 | 9,621 + 79 kick-only | 3.0000 | 0.9999 | 0.9999 | 8 | 4.0003× |
| **`BELT_SPLIT` (= lever 4, 98cb patch)** | **112,565** | **9,700/9,700** | **1.0000** | **1.0000** | **1.0000** | **4 by 460,400 gs** | **0.1250×** |

- **The split flight** (`BELT_SPLIT=1`, N = 10⁴, rtf 24,000, scan 160,400, end 460,400):
  genesis first kicks h≥60k for **9,700/9,700** bodies (100% bulk at `BULK_HILL` = 4 in
  this scene — stricter than my ≥90% prediction), h p50 112,565 (p01 107,003, p99 115,784 —
  the split class is unimodal with the shipped ±3% spread). At the scan — past the
  stretched kick crest (p99 h = 115,784 < 160,400), before the stretched boundary crest
  (p01 2h ≈ 214,006 > 160,400) — every belt body holds the welded pair {Boundary at 2h,
  Kick at 3h}: B/2h p50 1.0000 (p01 0.9992, p99 1.0005), (K−B)/h and interval/2h 1.0000,
  (B mod iv)/iv 0.0003. By 460,400 game-s (= 4.09 stretched intervals) every body has
  fired 4 events — kick, boundary, kick, boundary at h, 2h, 3h, 4h — dead 0. **The
  falsifier pre-registered for the dead branch (B/2h ≈ 0.25, boundaries outnumbering kicks
  ~8:1) did not occur in a single body.** With the first checker's levers 5 and 9, the
  welding family now spans six octaves of the lever (4, 5, 6, 7, 8, 9), all exact.
- **Determinism/rtf-invariance in flight:** the split arm flew twice (rtf 12,000 and
  24,000) with byte-identical genesis and scan lines.
- **Record regeneration:** arm 7 seed 1 diffed against de7b's `arm7.txt` — identical
  except the added `seed=` field and build seconds; arms 6/8 at de7b's own scan points
  (40,000/58,000) print `ladder:` lines byte-identical to their `arm6-scan2.txt`/`arm8.txt`.
  `ledger.py` (copied, plus one anchor row) recomputes 143.4/17.9/6.9 x86 and
  79.71/9.96/3.85 M1 riding cores at S = 1/8/20.7, pinned floor 15.67, S\* = 19.9×, and now
  prints the split's measured anchor: rate 1.777e-5 events/gs/body = 0.1250× shipped.

## Predictions

`predictions.md` was written after the arm-7 record check matched (disclosed there) and
before every decisive arm. **Held:** seeds (S1: h within ±0.03% of 14,071, 100% pairs,
identities exact, 4 events, dead 0); the split's transfer (S2.4: 100% split-class vs my
≥90% floor, h within 60 game-s of the predicted 112,570); the boundary riding (S2.5, the
decisive one: all identities 1.0000 on the stretched h; falsifier absent); controls (S3.8:
arms 6/8 to the digit). **Missed, disclosed:** S2.6 labelled the per-body event count
"scan→end" — the instrument counts genesis→end (as in de7b's arms), so the completed
window reads 4 (K,B,K,B over 4.09 intervals), not the 2 I predicted for a scan→end window;
the substance (one boundary per kick, alternating from h, at the stretched cadence) held
exactly. Also S2.7's `ok=true` needed the guard raise: the first two split attempts (rtf
12,000 end 385k, rtf 24,000 end 460k) hit the 55-s guard at 351,600/335,600 game-s with
the decisive scan already complete; the recorded arm is the third, `ok=true` at 460,400.

## What would make it wrong

Same frame as de7b: the flight is one scene (`plane_extra`), but now four seeds deep
(1, 2, 3 at the shipped lever; 1 at split) and the mechanism (one `full`, two items) has
no scene freedom left — a counterexample would be any body whose boundary is not the
midpoint of its own step, and 4 × 9,700 scanned bodies hold none. The split's legality at
S ≈ 20 (B-gates) is unchanged and still 7f97/1db4's question. The M1 boundary cost
(7.17 µs) remains an x86-ratio inference: no M1 exists in this lab, so the +25% CPU term
cannot be pinned here — noted as the one named miss not runnable, and it is
cost-independent for the branch structure (riding vs pinned), as the first checker said.

## Cost of adopting, and fit with PRINCIPLES

Nothing to adopt in code (the split patch is 98cb's, not in main; the instrument is
print-only). The design consequence hardens from "transfers by anchor" to "measured on the
actual patch": the one dial (split ≈ 20×) closes the belt's 10⁹ CPU ledger, and the build
constraint stands — splits must coarsen Δs, never skip planned kicks. Fit: PRINCIPLES #1
(less is more — the boundary-cadence component stays deleted, "the best part is no part")
and #20 (behaviours over many seeds — the welding now has three seeds and six lever
octaves, not one).

## The lens

The second-author lens pushes to the named miss first, and the cheapest decisive part of
it was the whole of it here (the split flight cost one build plus 90 s). What it may have
missed: I did not re-derive the split's regime test (98cb's `BULK_HILL` = 4) — a belt
whose inner edge sits inside 4 Hill radii of a source band would hold a shipped-class
minority; this scene's belt has none (9,700/9,700 bulk), so the mixture counter was never
exercised against a real minority, and the identities for a mixed belt are untested (each
class should weld on its own h, but that is inference, not measurement).

## Reproduce

`regen.sh` (build + six flights + ledger; ~5 min unloaded, ~10 min loaded; every flight
≤ 140 s guard). Flights logged verbatim in `arm7.txt` (seed 1), `arm6.txt`, `arm8.txt`,
`seed2.txt`, `seed3.txt`, `split.txt`; ledger in `ledger.txt`.
