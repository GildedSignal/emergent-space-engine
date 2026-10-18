# 20261018-1433-fermi-1309 (fermi lens) — the 10⁷ rung's margin is a legality cliff, not a margin

## Claim

Today's 10⁷-rung decision composition (20261018-1126-library-686f + the ef63 fix) is
arithmetically right and premise-flipped: its "lazy birth + the RES delete passes EVERY
term with ≥3× margin" (10⁷) and its "at 10⁹ ... NOT cleared on one thread" are the same
number read under two opposite assumptions about ONE unmeasured legality call — the RES
widened delete's belt survival 0.56% vs the frozen exclusion's 61%, worth **108.5×** on
the stream at every scale. Under the frozen exclusion the 10⁷ rung does not pass on the
shipped single thread at the ladder's own rtf 100.

## Bottleneck

The board's #1 (bodies in the flyable engine; the 10⁷ rung is the next flight). The
audit does not move CPU by itself; it moves the rung's **decision**: what a green 10⁷
flight certifies (the legality assumption, not the rung), and which lever is forced if
the assumption dies (rtf ≲ 65, a second thread, or the cadence dial ~24×). It also
corrects the 10⁹ CPU verdict: under RES legality the 10⁹ stream+wave clear 71–119× and
3–5×, leaving memory (15.75 GB birth / 28.4 GB live), the re-kick (0.55 s/s) and
encounters as the only CPU-class blockers.

## Evidence (all from `python3 compose_check.py`, < 10 s, no flight)

Every published cell of 686f/ef63 closes under exactly one survival s per row
(cost bands 30.9–51.7 µs and 34.6–60.1 µs back-implied from two anchor cells — the 10⁷
shipped stream and the ES_SECULAR-without-RES wave — then every OTHER cell closes
independently):

| published cell | closes at | my value | s required |
|---|---|---|---|
| 10⁷ shipped steady 1.08–1.81 s/s | exact | 1.081–1.809 | 1.0 |
| 10⁷ lazy+RES steady 0.006–0.010 s/s | exact | 0.006–0.010 | **0.56%** |
| 10⁷ ES_SECULAR-only wave 19.8–34.3× | exact | 19.75–34.31 | **61%** |
| 10⁷ lazy+RES wave 0.2–0.3× | ✓ | 0.18–0.32 | **0.56%** |
| 10⁹ steady spared 0.61–1.02 s/s | ≤8% | 0.659–1.103 | **61%** |
| 10⁹ wave 18.1–31.4× | ≤9% | 19.75–34.31 | **61%** |

The stream is N·rtf invariant (10⁷×rtf100 = 10⁹×rtf1 — ladder.txt's own conversion
"357 kicks a game-second = 36,000 a wall second"), so under one legality the two rows'
stream/wave cells must be **equal**; they differ by 108.5× = 61%/0.56%, i.e. by exactly
the legality call. Independent anchors: ladder.txt's own "~1.4 cores" at 10⁷ sits inside
the shipped band 1.08–1.81 s/s; the cadence 3.5×10⁻⁵ ev/B/gs is ladder.txt's own
357/10⁷ plus b30b's end-to-end 3.33–3.50×10⁻⁵, and the law's shape is in shipped code
(`step_log2: 7`, ctx.rs; 2⁷ steps per P_D, ext.rs, belt_first.rs).

Corrected margins (one legality each way):
- **RES legal (s=0.56%):** 10⁷ steady 0.006–0.010 s/s (71–119× margin; wave 3–5× is the
  weak term — "≥3×" was true but understated 20×); AND 10⁹ steady 0.006–0.010 s/s,
  10⁹ wave 0.18–0.32× — both clear; the 10⁹ "not cleared on one thread" sentence dies.
- **Frozen legality (s=61%):** 10⁷ steady 0.659–1.103 s/s = **0.65–1.09× the 0.72
  single-thread budget** (parity, not ≥3×); unstaggered wave fails 19.8–34.3×; the
  birth stagger (already in the composed law, load-bearing here) merges the wave into
  the stream at 1.04–1.81×. One thread holds to rtf ≈ 65 (band worst). The shipped
  plane runs 1 thread (ladder.txt).
- The frozen exclusion's 61% sparing is **geometrical**, re-derived from scenario.rs
  alone (belt a∈[2,3) AU uniform, e Rayleigh 0.07 capped 0.4, q>1.2 AU; Home a=1.020,
  Giant a=5.300 from the shipped PlanetSpec literals; rule "q/r ≤ 8 within 2%"):
  spared **58.4%** in period space, **75.0%** in a-space (200k samples). Cinder
  contributes nothing to a 2–3 AU belt (P_b/P_C > 11 > 8). So the RES widening deletes
  a majority near-resonant population — the exact class where "resonance kills
  averaging" (the adopted 30-Sept rule; law.md's own kick rule excludes resonant
  classes from averaging).

## Predictions

predictions.md was written before the checks. P1 held (law's shape in code; rate band
anchored by ladder.txt/b30b). P2 held (geometry 58–75% brackets the measured 61%).
P3 held — the s-mixing closes every cell, two exactly. P4 held (all corrected margins
as pre-computed). P5 stands as the named falsifier. The kill criterion for my own
reading (cells must close under the assigned s within 2×) was met everywhere (worst
9%, on the two 10⁹ cells whose cost band I did not fit).

## What would make it wrong

- compose_rung.py (on 686f's branch, not in this container) could compute some cell in
  a third convention that happens to close my two-s fit; the reproduction is from the
  published cells, not the script. The checker should re-derive from the script itself.
- My s assignment rests on 1a46's frozen record (274/712 deleted frozen, 708/712 via
  RES, both measured on the N=10³ ladder scene). If the 10⁷ belt's frozen survival
  differed (the draw is seeded and scales with N), the cliff ratio moves, not the
  structure (both survivals are far from each other and from 1).
- If the plane is routinely flown multi-threaded (scenario takes `threads`), the
  frozen-legality failure softens to a thread-count question; ladder.txt's record is
  1 thread.

## Cost of adoption

Zero code. Two decisions: (1) sequence the legality probe (doll_probe on the RES-only
434-class, ≥ one wave recurrence 14,167 gs) BEFORE the 10⁷ rung flight — a green flight
before the probe certifies the assumption; (2) carry the corrected 10⁹ row (under RES,
CPU clears one thread except the re-kick; memory busts either way) into the next
composition instead of the mixed one.

## Fit with PRINCIPLES

- "A failed expectation is not automatically a failed method: diagnose which one
  broke" — the composition's arithmetic is confirmed; the premise is the finding.
- "Gates are frozen before the first run" / "Certificates need independent,
  adversarial checks" — the rung's pass currently embeds an ungated legality call.
- "resonance kills averaging" (the register's own adopted rule) — the RES widening
  crosses exactly that boundary; the probe must earn it.

## The lens

Fermi attack #3 (check a claim): the estimate came first, and it AGREED with the
multiplication — the >10× disagreement lived in which premise the two rows multiply
by, invisible to cell-by-cell checking and exactly the class of error the r2/r3/r8
criteria and ef63's rtf² correction made before. What this lens may have missed: no
flight was run (Linux, 60-min window; every constant is frozen-measured, and the
composition's own numbers are the audited object); the checker with 686f's actual
compose_rung.py can close the last 9% and confirm no third convention exists.
