Working...
Check complete. `check2.md` written; the run folder is otherwise untouched (a stray `metrics.json` my kernel import dropped at the repo root is removed).

**Grade: silver** — summary of the evidence:

**Held up under reproduction and attack**
- `python3 falsifier.py` reproduces `falsifier-out.txt` bit-identically (3.5 s); `predictions.md` predates the decisive run by 7 minutes (mtimes).
- The simulation is exactly the closed form ε = (5/8)(δE/|E|)²n³ — it predicts 543/342/25 kicks at e = 0/0.5/0.99, the sim's numbers to the kick. My kick-size sweep (EPS 1e-6, 1e-8) confirms ratio invariance (0.068/0.074) and the δ^(−2/3) horizon law; e = 0.999 gives n* = 5 vs closed form 4.9.
- Belt stats survive re-derivation without the author's power-law fit (13% share, 44× p99.9, ~97× e = 0.99 body vs 15%/46×/112×).
- Every doc citation verified in-tree: representation.md's "multiply-add" with a resonance carve-out but no separatrix one; law.md's df81 (730 kicks, floor 1e-6, 0.05 budget); B5 median-seed, B9 creation-cost-only at e ≤ 0.99, B11/B14/B17/r1's low-e seeds; r1's light b log-uniform [10, 1000] vs b_c = 3√3; r5/r6 named but absent; the stale Binet "primary" text. No prior history entry measures recompile-vs-e or deflection near b_c. A2's Darwin/Synge numbers recomputed by hand — correct.

**What breaks gold**
- The belt arithmetic — the smoothness headline — uses Rayleigh σ = 0.3 uncapped, attributed to "B18b's own scene", but the frozen spec is **σ = 0.07 with e capped at 0.6** (`xtask/src/behave/belt.rs:117`). There the tail share is 0 and p99 concentration ~2×; sensitivity is sharp (share 0%/13%/36% at σ = 0.2/0.3/0.4). The 15%/46×/112× numbers belong to a hypothetical hot belt no gate freezes.
- Softer gaps: correlated-δE is asserted as the belt's actual kick mode though secular averaging conserves E; the 0.04-vs-0.05 budget comparison mixes float and quantum kick scales; no jet exists in the crates yet, so the per-cycle-vs-global trigger question is undecidable in code.

**Gold path:** run the horizon on the shipped `space-darwin16-v1` integer cycle across the e-tail, on belt scenes that actually exist in the tree, as the author's own proposed rung with the global-rate negative control.
