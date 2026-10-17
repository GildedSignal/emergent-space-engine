# Predictions (written after the freeze, before the decisive run)

Rung frozen at sha256:
```
88b4dfaa14e623bfea6bfcd21acae20b60743826c7503bb0c6bf6d3d5f2aa0e3
```
(file: `r6-view.md` in this folder; bars `rows_found ≥ 0.999`, `readouts_median ≤ 2.2`, `readouts_p99 ≤ 3.2`.)

Pilot calibration (disclosed: two pilot sweeps ran before the freeze — one with a broken scene window whose Toward cases sat mostly before first light, one with the final window; the bars above were set from the final pilot so that they are passable in principle with margin, per the rung rules).

## What I expect on the frozen case set (not tuned on: these are reasoned, not read off the pilot rows I will report)

1. **warm passes all three bars.** The arrival-rate guess keeps the median near 1–2 readouts; the p99 stays under 3.2 (the racing frames where a 0.999c closing emitter's retarded time jumps ~10⁸ ticks per frame are a handful per case, and the bracket search absorbs them).
2. **cold drops rows.** The from-the-present search exhausts its 64-iteration budget on a few emitters per Toward case (I measured 12/38400 in the pilot window): rows_found ≈ 0.9997 — above the 0.999 bar by a hair, so cold is killed on cost, not rows. If the checker's rebuild drops more (different seed? no — fully deterministic), rows could kill it too.
3. **poisoned fails the p99 bar.** A stale or foreign cache still returns the same crossings (rows ≈ 1.0), but the tail cost blows past 3.2 (pilot: 5.1) — the doc's "any cache… gives the same view" is true for the view and false as a cost claim.
4. **amnesiac (negative) fails cost robustly** (median ≈ 2.5 > 2.2, p99 ≈ 4 > 3.2), rows ≈ 1.0.

## Held-out cases (not in the freeze; what a checker should try, with my predictions)

5. **A slower rtf (rtf 10, frame ≈ 3.4×10⁴ ticks):** warm's median drops toward 1.0 (the guess lands inside the acceptance window more often); cold's median drops too but stays above warm; the row drops vanish (the search walks less). Verdict unchanged: PASS with cold killed on cost only.
6. **A faster rtf (rtf 1000, frame ≈ 3.4×10⁶ ticks):** the Toward racing frames dominate; warm's p99 rises toward 4–6 and I would not hold the 3.2 bar — the tail bar is cadence-dependent and would need re-freezing at that cadence. The median bar holds.
7. **β_em = 0.6 mixed streams (Toward/Away/Across in one scene):** all configs pass cost; the rung's separation lives at β ≳ 0.9, where the arrival-rate window is the mechanism. A rung that must separate at low β needs the amnesiac-style negative, not bars on the shipped law.
8. **The bracket oracle at a smaller scale** (positions ~10⁶ root units): the f64 noise floor (~10⁻³ ticks there) drops below the acceptance window, and the tick-level light-cone bracket becomes checkable — I predict warm certifies ≥ 0.99 of rows there, which would let a future r6 v2 freeze exactness, not presence.
