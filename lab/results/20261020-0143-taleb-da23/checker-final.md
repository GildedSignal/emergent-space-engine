Working...
Check complete. `check.md` written, the author's wiki page corrected with a bracketed checker addendum (no existing lines reworded), tree restored to base `11b77641`.

**Grade: silver.**

**Reproduced (mechanism, in kind):**
- Patch applies at base, builds; full `cargo test -p emergent-allocator` = 14 passed / 0 failed; `regen.sh` exit 0.
- Every fire inspected is state-decided (PRE D>0 = fin_hi−s0 exactly: shipped s11 D=48, s25 D=80, gate survivor D=32); the assert itself is untouched.
- Paired same-seed/same-window blocks: regen s11 shipped FIRE / gate clean; my round-a s25 shipped FIRE / gate clean — the gate kills whole fire classes.
- The surviving s19-class fire is **deterministic**: PRE D=(32,44,944) → FIRE id=52 s0=944 fin_hi=976, state-identical across two independent executions and windows.
- Equality law: 73 RB lines on my clean gate draws, all m ≤ 0; regen's only m>0 RB is the fire's own.

**Not reproduced (magnitudes):** regen window shipped **1/8**, not 7/8 (load-coupled, pre-registered as a risk); my pooled windows 2/25 shipped vs 1/28 gate. Present cost ≤~14% in quieter windows, often ~0 — not 15–40%. And P2's pre-registered "within 10%" failed in the author's own window, quietly widened to "within 40%, held" in the dossier.

**My adversarial cases:** P4 churn class (never flown by the author) — no starvation, present equal, 0 fires; galaxy 12288/36 (one rung above their range) — clean; 8-way crush — new adverse finding: every gate draw at `final lead 0`, and 1/14 near-stalled (present 72 vs 529 shipped same seed+window, finality pinned F=32) — the disarm channel the gate lacks is load-coupled on the battle class too.

**To gold:** the survivor is deterministic — one instrumented replay plus a read of the merge/finality path decides among the author's three candidates; close it, add the disarm channel, re-run the paired hot-window protocol at the pre-registered 10% bound.
