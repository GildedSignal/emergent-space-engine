Done. GradeCheck complete. **Grade: silver** — written to `check.md`, page corrected in place, checker-final.md finalized.

**Verdict basis:**

- **Reproduced exactly (regen, both windows):** the checker-named liveness criterion — clumps 2695, mixed 2698, streams 2698 (v4: 2577-2624/819; v5 still stalls 0/0/1024), quiet 2698; crush 0/12 fires both arms, v6 median 1.9–2.6× v4; predictions pre-registered (mtimes 21:32:33 < protocol 21:36:43).
- **Not reproduced:** the 0-fire safety half. The runner's own regen fired v6 on battle s19 — the genuine finality assert (`rollback of region 53 from 816 would revise its published tick 896`, RB `m=80`), breaking P1 and P4 as window-free claims.
- **My attacks:** s19 re-flown ×4 under v6 + ×2 v4 control (all clean — rare interleaving, not a deterministic kill); fresh seed 41 (clean); 2× scale galaxy 17408/48, beyond the author's range (clean). Key diagnostic: 44 of 57 regen RB margins are exactly `m=0` — a zero-slack floor one interleaving away from positive; the unexamined suspects are the rollback re-capping only `restored.last()` (after the assert) and truths born after a floor computation.
- **One experiment to gold:** close the s19-class fire's publish path, then ≥3 battle windows (≥18 draws) at 0 fires with all RB `m ≤ 0`.
