Grade: silver

**Abstract.** The premise-kill reproduces exactly: the probe regenerates byte-identically, all eleven exponent rows of table 1 match, the frozen config-A column matches on 15/15 laws (state-only max 1.31, walk-13 2.31, refs 13.3/17.0/4.8), the one-ulp ranges match, and the real harness agrees — the ignored probe test fails today (leak 1.094 below bounded-a 1.103; walk control 3.1e5), planted drift/bounded/compound read 1.355/0.353/0.416, and echo fails B12 on this box (1 unconverged, 1 inside; 0 of 14 judged above the floor). But detector B, half the proposed replacement, has no shipped code: under six natural readings of "within-cell median spread" its table does not regenerate, and one positive control flips across the threshold. The physics is gold; the record is not.

## Reproduction (clean tree, empty patch.diff; all commands from the dossier)

- `cd probe && cargo run --release`: 3.2 s, all seven `out/*.f64` byte-identical (md5).
- `python3 stats.py`: every table-1 exponent matches exactly (r11/r12/r13 1.408/1.229/1.806; bounded-a/e/r2 0.277/0.332/0.395; compound 0.301; plane-jump 0.599; drift/leak 1.001; noise 0.157; periodic 0.057; walk-13 0.527). Draft-cell ratios match (bounded-e 1.75, r2 1.34). r12-vs-r13 agreement median 2e-11, max 2.4e-9 ✓. Per-ship bounded-a scatter over nudges 0.14–0.36 ✓. **The shipped fate section crashes** (`meta[str(s)]` KeyError — the meta parser is broken), so §3's fate numbers are not regenerable from the shipped scripts.
- `python3 sstar.py`: bounded-a S* = 2.90 ✓ (worse than cells, as claimed).
- My independent implementation of frozen config A (cells 0.02/0.005, near 4–16, far 64–200.1, p90 floored): **15/15 laws match the dossier** (0.95, 1.04, 1.31, 1.01, 2.31, 3.09, 3.10, 2.37, 9.35, 1.87, 13.30/16.96/4.80), and the four one-ulp ranges match exactly (walk 2.92–3.78, compound 6.38–13.29, plane-jump 9.56–19.75, bounded-a 0.92–0.93, bounded-e 1.03–1.07, ref-r12 6.0–168.5). Every pass/fail decision stable across nudges, as claimed.
- Real harness: `cargo test -p xtask the_recurrence_ratio_separates -- --ignored` **fails today** exactly as claimed — leak 1.094 < bounded-a 1.103, walk control 309135 — independently confirming the blind spot. `cargo run -p xtask -- behave --law echo --gates B12`: **FAIL, "1 not converged, 1 inside the planet; 0 of 14 judged ships rise above the floor"** — §3's echo claim verbatim. (My port of the convergence count reads 2+3; the port is not the gate, and the disagreement is itself §3's fragility thesis.)

## Numbers that differ

1. **Detector B does not regenerate.** No code shipped. Under MAD-of-cell with ≥2 early and ≥2 late visits, far-field only: bounded-a 1.20 (dossier 0.96), bounded-e 1.19 (1.07), bounded-r2 0.83 (0.53), noise 0.62 (0.53), walk-13 1.02 (1.05), compound 16.6 (4.64), saturating 16.6 (4.63), plane-jump 10.6 (2.90), true-leak 1.87 (1.97), periodic 2.95 (2.61). Other readings (no far-field mask; ≥1 visit; median-pairwise spread) move values further (compound 9.2–9817; plane-jump 6.9–5.9e5) and **bounded-r2 flips across the 1.5 line** (0.83 with ≥2 visits, 1.96 with ≥1). Under the median-pairwise spread the true leak passes BOTH probes (A 1.17, B 1.15) — the pair's central invariant depends on an unstated definition. Decisions match under the MAD reading; the dossier's margins (29%/31%) do not (mine 20%/25%).
2. **True leak A = 1.17 in my faithful port** (velocities × (1+1e-12·t/P), Jacobi recomputed, recompute checked to 1.6e-15) vs 1.55 in the dossier; exponent 1.245 vs 1.13 (the real harness's leak reads 1.195). Verdict identical (passes A, fails B), but the margin to 1.8 is implementation-dependent.
3. **Fate: "ships 1, 4 and 13 flip inside/outside" not reproduced** under any reading (vs r12: 14 distinct ships flip across the four nudges; r12-vs-r13 flips 6). "Closest moves >50% on 16/16" holds only as the union over nudges (min union ratio 2.94). The direction is confirmed and stronger; the specifics are not regenerable.

## Predictions

`predictions.md` (07:48) precedes the decisive statistics (stats.py modified 07:51, imported 07:53; data 07:47–48) — pre-registered in order. Qualitatively held: the reference fails at all tolerances (P1), cannot-separate (P2), periodic false positive 4.51 (P4, predicted ≥2), saturating disagreement (P5), ulp chaos (P6, stronger), floor below reference noise (P7). But P1's range (0.2–0.6 at r12; actual 1.229) and P2's (bounded-a 0.45–0.55; actual 0.277) were wrong; the dossier reports P1 as "held, stronger" without flagging the missed range. The three self-reported misses (draft cells on bounded-e, S*, the leak's hiding) are honest and are the run's best finding.

## Adversarial cases (mine)

Coarser e-cells (the under-resolution mechanism: bounded-e 1.75 at 0.05 vs 1.04 at 0.005); six B-definition variants (above); the leak plant reconstructed from the harness formula rather than the idealized linear drift (above); ulp stability of every A decision (held).

## Novelty

docs/law.md B12 (6 October) already had the bounded/compound inversion (P2) and the draft recurrence ratio, and awaited this red-team by name; HISTORY has no prior cell-drift, leak-hiding, or reference-fails-at-all-tolerances result. New here: the exponent is a level test (the gate's own reference fails at every tolerance, and the bounded/compound ordering is machine-fragile — 0.353 < 0.416 here vs law.md's 0.493 > 0.305); the draft ratio's two blind spots (e-cell resolution; the v²-oscillating leak); the two-probe replacement; S* negative.

## Goal fit

The motion law v2 is designed against B12 (HANDOFF), so the deciding statistic is load-bearing. The run enforces principle 13 as error *type*, which is what "types of errors and not just errors" (OC#42) asks, and respects gate discipline: no threshold moved, dispositions addressed to the integrator, `main` untouched. One caveat on wording: replacing the exponent is a freeze change, not "no threshold loosened" — correctly left to the integrator.

## The one experiment that would make it gold

Freeze detector B in code inside the shipped scripts (exact spread definition, min visits, far-field mask), regenerate its full table — plants, true leak, one-ulp replicas (B was never nudge-tested) — with the margins, and run one real law (`behave --law plane`) through A+B rather than only synthetic plants. All from commands the dossier lists.

## What the author missed

- The record gap itself: B, the true leak and the fate numbers have no regenerable code, and a shipped command crashes — the lab's known gold-killer (taste log, 5 October).
- B's decisions are sensitive to unstated parameters (min-visits flips bounded-r2 across 1.5); the freeze must pin them, and the "pair" reading silently releases the true leak.
- The probes pool all 16 ships, including the 2 the gate itself excludes (unconverged/inside); the frozen replacement should judge the judged set.
- Noise-11 passes today's exponent at 0.157 — a 22% margin on the positive side, worth stating when calling iid a pass.
- Single scene (Jupiter, circular), synthetic plants, one machine — admitted in the lens note, and the real plane was never run through the replacement.
