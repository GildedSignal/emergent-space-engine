Grade: silver

**Abstract.** Claim: the resonance gate is the guard-form certificate on a declared domain (j ∈ {1,2} below overlap, quanta ≤ cap); both predecessor gaps are closed. Everything reproduces: quad/calib bit-identical, four re-run scans array-identical, final.py regenerates final.json (only the two declared diffs, W.j2 0.0229→0.0305 among them), gate.json identical, predictions pre-registered. Measured: the guard form (switch at q_e/2) has 0 misses in 6,762 truth-failure events on 2:1/3:2 where the W-gate misses 542–1,120 — the deletion is free; the switch form is killed (66 misses above cap); one-per-family dies at 4:3 above cap (12 guard misses, pump 7× cap). Silver: the domain test's arithmetic is wrong (5:4 at +0.044, outside the grid, not +0.027) and the plane's kick layer remains unwired.

## Reproduction (clean tree /tmp, patch.diff empty — verified: the only edits to the shipped scripts are OUT made file-relative and the added `quadj` stage)

- `selftest` passes (ringing 4.395e-4, no drift). `quad`, `calib`: **bit-identical** to work/orig (md5).
- `scan 1 0.001`, `scan 2 0.0003`, `scan 3 0.0003`, `scan 3 0.001`, `quadj 3 0.0003 0.001`: **all arrays identical** (only `wall_s` differs, as expected); quad-j3.json identical. Edrift 3.2e-14 / 9.7e-13 on the new scans.
- `analyze.py`: P1 = 165, P4a = 0 (matches). `final.py`: regenerates final.json; diff vs the original run's file is exactly the two declared entries — the W slip reproduces (0.0305 with the 3:2 factor 1.5·(2/3); 0.0305·0.75 = 0.0229, the 2:1 factor) and the 0.52→0.53 rounding. Held-out-only capped law n = 270, 99.26% ✓.
- `gate.py` → gate.json **identical**; every dossier table number (c_H, cap, n_fail, miss columns, doll fractions) matches.
- predictions.md (mtime …015) precedes quad-j3.json (…191), both 4:3 scans, gate.json (…293). Pre-registered.

## Predictions

PA failed as written (40 switch-level misses at 2:1, 66 on 2:1/3:2), disclosed prominently; its guard half held exactly (zero on all five cases). PB held (4:3 misses at large q on the +δ side). PC held exactly (c_H = 18.76, doll-fraction 1.00, fails safe). PD held in guard form; PE held exactly (μ=0: ṗ_coh = 0 exactly → excursion 0; far controls exc 0.0027–0.0287 < q_e 0.021–0.109, no switch). No kill criterion triggered.

## Adversarial cases (mine)

1. **Fresh seeds** (shift 0.3 rad, j2 μ=1e-3, the case with the one real switch miss): n_fail = 1,417, switch misses 13, **guard misses 0**, same above-cap/grid-edge mode. The zero-miss headline survives a seed attack.
2. **The 5:4 location is wrong.** The dossier's δ ≈ +0.027 "inside the ±0.032 grid" is a mis-computation: by its own formula, (2/3)·(1/((j+1)(j+2)))/pr = 0.0444 (exact (0.8/0.75)^(2/3)−1 = 0.0440). The 5:4 center is **outside** the grid; its old-W zone [0.034, 0.054] still plausibly pumps the +0.032 edge (median band 0.093 > cap 0.052 there), so the mechanism survives qualitatively, but the domain-test table entry (0.027) is wrong, and with correct numbers the test's "false for 4:3" verdict survives only by an unstated ~7% margin (5:4 at 0.044 vs the guard's zone ≈ 0.047 at the design quantum; vs the saturated zone 0.0236 it flips to "in domain"). The "most valuable number here cost 70 seconds" is wrong by 1.6×.
3. **The 4:3 refutation is above-cap.** All 12 guard misses at 4:3 μ=3e-4 sit at q ∈ {0.117, 0.16} > cap = 0.052. At quanta ≤ cap the guard has **zero misses on all seven cases, including 4:3**. So "cleanly refuted as one-per-family at 4:3" refutes the domain boundary, not the guard on its declared quantum domain; and the design quantum can exceed the cap (j2 μ=1e-3: q_e = 0.109 > cap = 0.094), so "quanta ≤ cap" is not guaranteed at the engine's own design points — the honest boundary is the guard's non-empty zone (q ≤ 2·cap) plus non-marginality, which is what actually separates 4:3 (real pumping, 3–7× cap) from 2:1/3:2 (marginal).
4. **Regime undercount.** Librating systems are 47/63/58/55/50/53/32 per case, not "~10–15"; librating-kept-outside pairs concentrate at the top 1–2 quanta (j1 μ=3e-4: all 47 at q = 0.16 only) — above cap, outside the declared domain, zero at design quanta. B17's "regime matches 100%" is violated only above cap on these grids, but the disclosure's number is 4× off.
5. **Cost table mixes forms.** The stored dollfrac_cert is the switch form: at j2 μ=1e-3's design quantum it is **0.00** (empty zone) — the strongest single argument for the guard form, dropped from the "cert 0.87–1.00" range. The guard form covers the whole grid at all five design quanta (1.00 vs old-W 0.73–1.00). Also "all 66 switch misses sit above the cap": 65 of 66 (one marginal, sev = 0, at q = 0.0626 < cap = 0.074).

## Novelty

The predecessor silver (checked this morning) established the certificate and its numbers; its checker had already found 4:3 P4a violations (4 cells) and c_H = 0.78/18.8 — both reproduced here (0.779/18.76). New: the record regeneration (final.py — closes the 5 October lesson), the gate-level wiring with truth-failure events and the old-W comparison (0 vs 542–1,120 over 6,762 events), the guard/switch distinction (principle 34 made concrete and measured), the W conversion slip (0.0305: the crossing does not derive B17's convention at 3:2 — 2.7×), and the full 4:3 scans. No HISTORY entry duplicates this (H0203 is the nearest).

## Goal fit

Board focus lines 1–2 (changeover near a secondary; fewer kicks). Deletes the classifier + W table on a measured-free domain: "The cheapest compute is compute not done. Delete before optimizing" (1); "Regimes are chosen by dimensionless numbers" (4); "A failed experiment kills that configuration, never the method" (9 — 4:3 kills one-per-family, the certificate survives bounded); "the oracles are guards, not shepherds" (34 — the guard form is the guard; the switch form is a shepherd and under-predicts above cap). Genuine fit; the stand-in is honestly labelled (the crates are off-limits to the lab).

## The one experiment for gold

Wire the guard-form certificate into the motion law's resonance gate (crates — outside the lab's power): classifier and W table deleted, j ∈ {1,2} below overlap, cap from the one-column exact-resonance calibration, judged by B17's full standard (pump ratio, libration amplitude, regime match at the design quanta, controls) on r4 v3's cases; and freeze the domain test only after correcting its arithmetic (next family at +0.211/+0.082/+0.044; compared against the guard's zone at the design quantum, margin stated — currently ~7% at 4:3). Gold if behaviours are unchanged and the corrected test's margin holds.

## What the author missed

- The 5:4 arithmetic error and its consequence: the domain test, correctly computed, does not exclude 4:3 by the grid argument given; the exclusion rests on above-cap non-marginality and the μ=1e-3 degeneration.
- Guard-at-q≤cap is clean at 4:3 too — the domain story is about q vs cap (design quanta can exceed it), not about j per se.
- The switch form's empty zone at j2 μ=1e-3's design quantum (dollfrac 0.00) — the cleanest argument for the guard form, absent from the cost claim.
- The regime-miss undercount (47–63 per case, not 10–15).
- The negative control's frac_fail 0.88 against the code's own "must be 1.0" — inherited from the predecessor and still unflagged.

## The lens

The second-author frame ("wire it and see") was right and produced the decisive numbers; what it hid is the same edge as before: the domain test was computed, not checked, and the headline numbers were read off the stored metric without asking which form they belonged to. The run's own lesson — PA's failure teaching that the cap's collapse is the blind spot of a [0.3, 3] headline — applies equally to its domain test.
