# The boundary comb rides the step lever with the kick comb — the 10⁹ ledger's razor resolves to "closable"

## Claim

The belt's boundary comb has no metronome of its own: it is welded to the same per-body step
`full` that the kick closes (`step.rs` `kick_clock`: boundary at `t + full/2`, kick at
`t + full`, one `full`), so **any step-length lever — the shipped `Config::step_log2`, and any
cadence split built the same way, `BELT_SPLIT` included — stretches both combs together**,
boundary always at the kick's midpoint. Measured on shipped code across three octaves of the
lever (N = 10⁴: per-body rate 0.2500× / 1.0000× / 4.0003× shipped, `h` p50 28,141 / 14,071 /
7,035 game-s, all welding identities exact to 4 decimals, 100% of belt bodies). The 10⁹
ledger's negative branch (a boundary floor no split can remove, ~15.7 M1 cores) is dead; the
riding branch stands: **9.96 M1 cores at split 8, closable at S\* ≈ 19.9×** — 4e2d's
recomposition (10.3, S\* = 20.7) confirmed, and the composed stream's boundary term is only
the ~+25% CPU correction (both combs ÷ S), never a floor.

## Bottleneck

The board's "scale to 10⁹ on the M1" row, via the kick-cadence page's open direction 1 (the
named one-flight experiment from 20261017-0005-dynamics-8ffc). At stake was a factor with no
lever: if `BELT_SPLIT` stretched only the kick comb, the boundary comb (1.00 event/body/
interval at ~13 µs) alone would pin ~15.7 M1 cores at 10⁹ rtf 100 at every split. Decided
here for ~0 extra compute: the boundary rides, so the one dial (split ≥ ~20×) that 4e2d named
closes CPU after all. What it deletes: the "the composed ledger's miss is the boundary
majority" hypothesis, and any need for a separate boundary-cadence invention.

## Evidence

Mechanism (source, shipped main): `kick_clock` computes one `full = ext.ticks(ext.time(y,
ext.ds))` (`step.rs:705`) and schedules BOTH items from it — boundary at `t + full/2`
(`step.rs:717`), next kick at `t + full` (`step.rs:718`); `boundary_clock` (`step.rs:725`)
plans nothing ("the next kick is already planned"). `ds` comes only from `ext::constants`
(`ext.rs:146`): `Δs = P_D/(2^step_log2·f'(c))`, doll-wide from the fastest source. There is
no second scheduler to stretch independently.

Flight (new example `belt_combs.rs`, print-only over shipped state, `plane_extra` seed 1,
N = 10⁴, belt = 9,700, rtf 2400, `Budget::unlimited`; per-body plans scanned between the
combs and after two intervals; per-body fired events from `BodyRec::events`):

| step_log2 | h p50 (game-s) | welded pairs at scan | B/2h | (K−B)/h | interval/2h | events/body ~56.3k | rate vs shipped |
|---|---|---|---|---|---|---|---|
| 6 (coarse) | 28,141 | 9,700/9,700 | 1.0000 | 1.0000 | 1.0000 | 2 (1 kick + 1 boundary) | 0.2500× |
| 7 (shipped) | 14,071 | 9,700/9,700 | 1.0000 | 1.0000 | 1.0000 | 4 (2 + 2) | 1.0000× |
| 8 (fine) | 7,035 | 9,621/9,700 | 3.0000 (= 6h) | 1.0000 | 1.0000 | 8 (4 + 4) | 4.0003× |

p01–p99 of every identity within ±0.0004; `(B mod interval)/interval` ≤ 0.0004 (the boundary
at the interval's edge, the kick half an interval later — 8ffc's two combs, now read per
body). The 79 non-pairs at arm 8 are bodies already past their third boundary (scan point,
not structure). h p50 at the shipped lever is 14,071 game-s = 8ffc/3294's 14,071–14,072 to
the digit. Dead 0, refusals 0, deterministic seed.

Transfer to `BELT_SPLIT` (98cb's patch, not in main): their own anchor — first-kick p50
14,072 → 112,574 = 8.000× — is a step-length lever by measurement (a "skip 7 of 8" split
would leave the first kick at 14,072), and this run shows every step-length lever carries the
boundary with the kick. So the split's boundary comb stretches 8×; the composed stream is
(kicks + boundaries)/S with the +25% CPU term, at every S.

Ledger (`ledger.py`, constants page-cited: kick 52.7 µs x86 / 29.3 M1, boundary 12.9 /
7.17 [inferred at the M1 kick ratio], interval 28,141.5 gs, survival 0.615, rtf 100):
riding: 143.4/17.9/6.9 x86 and 79.7/9.96/3.85 M1 cores at S = 1/8/20.7; S\* = 19.9× to
4 M1 cores. Pinned branch (dead): 15.67 M1 cores at every S.

## Predictions

Written before any arm ran (`predictions.md`). **Held:** the lever control (h moves exactly
2× per octave — 2.0002×/0.4999×), boundaries/kicks = 1.00 per body at every octave, both
combs' rates scale with the lever together, the welding identities (B = 2h·j, K − B = h,
interval = 2h, B ≡ 0 mod interval) hold per body, ≥ 99.9% welded pairs (measured 100%).
**Missed, disclosed:** I labelled `step_log2 = 8` as the coarse arm — it is the fine one
(2^k kicks per period), so prediction 1 as written ("h doubles at arm 8") failed on my knob
direction while the control itself passed on arm 6; also my first smoke run (N = 3,000, for
instrument debugging) ran after predictions were written and before the decisive arms, and
revealed the plan lifecycle (a fired boundary leaves a kick-only plan) that fixed the scan
design. A 3,000-body debug run is not a tuned case: no parameter of the decisive arms was
adjusted on it beyond the scan point, which is set by h (published, not fitted).

## What would make it wrong

The flight evidence is one scene (`plane_extra`), one seed, one N — but the claim is
mechanistic (one `full`, two items), and a mechanism claim is scene-free; a counterexample
would be any body whose boundary is not at the midpoint of its own step (none in 3 × 9,700
bodies scanned, and the counts are exact integers per body: 2/4/8 events, no tails). The
ledger side inherits its constants (costs from 8ffc/e7ef, survival from 1a46): if the
boundary's M1 cost is not 7.17 µs the floor moves proportionally, but the branch structure
(riding vs pinned) does not depend on any cost. The transfer to `BELT_SPLIT` assumes 98cb's
split enters through the step (their 8.000× first-kick anchor says it does); a split built as
kick-skipping would not transfer — that is now a build constraint to state, not an open
question: **cadence splits must coarsen Δs, never skip planned kicks.**

## Cost of adopting, and fit with PRINCIPLES

Nothing to adopt in code (the example is an instrument; the conclusion retires a worry).
The design consequence: the split dial closes the 10⁹ belt CPU ledger alone (S\* ≈ 20×
against B-gates legality, which is 7f97/1db4's question, not re-flown here) — so the 10⁹
critical path stays where e7ef/4e2d put it: the compact store's wiring and the encounter
routing, not the boundary. Fit: "we just need to have the right representation so that math
is trivial" (CL 09-27) — the two combs were one dial all along; and via negativa: a
boundary-cadence component that some branch feared necessary has no part to play ("the best
part is no part").

## The lens

The Fermi estimate ran both branches before the flight (the razor was 10.3 vs ≥ 15.7 M1
cores, a 10⁰ difference that no other measured lever covered) — but I initially priced the
knob backwards (prediction 1's sign error), and a pure paper run would have shipped that
error: the flight caught it in one column. What the lens may have missed: costs were
imported, not re-measured (a cost lens would time the boundary on the M1); and the
legality of S ≈ 20 (B-gates at 20× coarser belt steps) is priced by citation only.

## Reproduce

`lab/results/20261017-1149-fermi-de7b/regen.sh` (build + three arms + ledger; ~3 min).
Arms also logged verbatim in `arm6.txt`/`arm7.txt`/`arm8.txt` (arm6.txt holds the first,
mistimed scan; the corrected arm-6 rerun is in the dossier table and regenerates via
regen.sh).
