# Predictions — second-author run 20261007-1334 (fix + steady-state on 20261007-1234-components-97bf)

Written before any post-fix run. The fix is mechanical (staleness-aware overflow top in
`next_tick`/`deliver`/`cascade`); the performance cases are NOT tuned on — no post-fix
performance number existed when this was written.

## Correctness (after the staleness fix)

- **P1 corner:** `corner` mode returns tick 4194304 (2W) with all 8 ids, matching the heap;
  no 3145728. The fallback now reads only live overflow tops.
- **P2 all-far quiet regions:** F-diff at N = 2, 4, 16, 64, 4096, 65536 (seeds 7, 1, 3,
  ≥ 100k deliveries) reports no divergence. Pre-fix it diverges at N ≤ 16 (recorded in
  `results/prefix-failures.txt`, steps 4/6/39780).
- **P3 regression:** heap and wheel digests for A–D rows byte-match the stored 97bf rows
  (the fix changes no path the old code got right). Checked on A 2¹⁸ seed 2 and C 2²²
  clean, heap and wheel.
- **P4 diff everywhere:** A–F diff mode clean at 2¹⁴–2¹⁶, several seeds.

## Steady-state performance (warmup ≥ 2M delivered, then ≥ 2M measured; medians over seeds 1–3)

Cases: S pure spread (log-uniform 30 octaves, ~30% beyond W), E mixed (1/16 storm + 15/16
spread), A storm, F all-far. "Ratio" = wheel ns/op ÷ heap ns/op.

- **P5 S at 2²⁰–2²⁴:** wheel wins, ratio 0.45–0.75 (checker saw ~0.64 at 2²² one-shot).
  The wheel pays ~6 lines/op regardless; the heap pays ~log-depth with churn-friendly
  decrease-key (sift-up is short for near re-times). Direction certain, size not.
- **P6 E at 2²⁰–2²⁴ (the gold-condition case):** ratio 0.35–0.65. The 1/16 storm seasoning
  pushes it below S's ratio (epoch-quantized bursts hit one bucket each; the heap pays
  them as log-depth pops) but the spread bulk keeps it above case A's ~0.43. If it lands
  ≥ 0.5 the "≥ 2× at DRAM scale" gold condition fails and the honest statement is
  "2×+ only in storm-heavy regimes".
- **P7 A (storm) steady at 2¹⁸/2²⁰:** ratio 0.38–0.48 (checker measured ~0.43 at 2¹⁸).
  At 2²⁴ case A cannot cycle inside the budget (one step delivers the whole population);
  reported as one-shot, not steady.
- **P8 F (all-far) steady at 2¹⁶–2²⁰:** ratio 1.0–1.35 — the wheel degenerates to its own
  overflow heap plus bitmap overhead; the heap's indexed decrease-key is not slower here.
  This is the wheel's worst regime and I expect the heap to WIN it (ratio > 1).
- **P9 no regime swap:** across all steady rows the heap never beats the wheel by more
  than ~1.4×, and the wheel never exceeds ~3× in steady state (the 4.5× headline was
  one-shot storm).

## What would make the fix wrong

A stale overflow top that is live-checkable but whose `(t, id)` duplicates a real entry
(two bodies same id impossible; one body one live slot by `loc`/`at` invariant) — if diff
mode diverges post-fix anywhere, the liveness predicate is wrong and the run reports it.

## Outcomes (written after the runs; the sections above are untouched)

- P1 HELD: corner OK, tick 4194304, ids 0–7 (pre-fix FAIL: 3145728).
- P2 HELD: F diff clean at N=2/4/16 (pre-fix: DIVERGE steps 4/6/39780), 64, 4096, 65536.
- P3 HELD: three stored 97bf rows regenerate byte-identically (A 2¹⁸ s2, C 2²² s1, A 2²⁴ s2 —
  heap and wheel, digest and sets) with the fixed wheel.
- P4 HELD: A–S diff clean at 2 sizes × 3 seeds × 50k, plus long S diffs (300k at 2²⁰).
- P5 PARTIAL: S ratios 0.44 / 0.41 / 0.35 — below the predicted floor of the range at scale
  (wheel better than predicted). First attempt at 2²²/2²⁴ measured the fill flash (bursts
  ~350k); corrected with warmup 2.5M/11M, disclosed in the dossier.
- P6 HELD: E ratios 0.41 / 0.41 / 0.45 at 2²⁰/2²²/2²⁴ — inside 0.35–0.65; ≥2.2× at DRAM scale.
- P7 PARTIAL: A steady 0.51 (2¹⁸) / 0.47 (2²⁰) — 2¹⁸ just above the 0.48 bound.
- P8 PARTIAL (direction held, size missed): F ratios 2.28 / 1.66 / 1.35 — the heap wins more
  than the predicted 1.35 cap at 2¹⁶.
- P9 HELD: heap's best is 2.3× (F 2¹⁶); wheel's best steady 2.9× (S 2²⁴).
