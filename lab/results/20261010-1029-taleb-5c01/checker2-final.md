Working...
Check 2 complete. `check2.md` written; nothing else in the run folder or repo touched.

## Verdict: **Grade: gold**

**Reproduction (bit-for-bit, clean worktree = main + `work/patch.diff`):** all three dossier controls (5/234, 284/1407, 281/2250), the 20-orbit run (162/8279), the full sweep battery, and the k=256 probe — including `setup_evals` counters (48158654/734999), proving the author's edit-then-revert experiment was genuine. `method_only = 0` everywhere: the tier is sound but incomplete.

**My adversarial work beyond the dossier:**
- Independent numpy-Kepler adjudication of **193 missed pairs** (author did 8): all minima at t≈0 or t≈H, zero interior, zero false truths — across five scenes including the gold-adjacent geometry and a uniform-phase scene (19% miss without any bunching).
- Fresh seeds 77/91 → 21.1/21.9%; seed 91's 79 `check`-verdict misses (a possible second mechanism) adjudicated edge-located like the rest.
- **Reconciliation verified in code, not inference:** `matchup` on main (`crates/encounters/src/main.rs:97`) filters truth events with `t > 0.05 && t < t_end − 0.05` before counting misses — 0306-taleb-8af8's "zero misses" structurally excluded the edge band. The shared-harness blindness is on main and will corrupt future judging too.
- Contract violation confirmed: `pair_events`'s doc promises all minima in `[t0, t1]`; under horizon refresh a straddling encounter is reported by neither adjacent horizon.

**Noted for the integrator:** the dossier's aggregate "window 546" doesn't reconstruct (I count 566; per-scene numbers all exact), and "vanish at R1≥30" is loose — the supported statement is "no monotone guard exists". The fix (two unconditional edge checks per horizon refresh) is one step; `matchup`'s `inside` predicate should be patched alongside it.
