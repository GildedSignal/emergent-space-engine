Working...
Check complete. `check2.md` written; tree restored (only the pre-existing untracked `lab/results/` remains); nothing else in the run folder touched.

**Grade: gold.**

Evidence trail:
- **Reproduction, bit-exact.** Clean tree at `2906ffd`, applied `work/patch.diff`, ran all three dossier commands (49 s total): every non-timing field of all 57 output lines matches the author's JSONL exactly — blocks 157.39/157.37 bits/body with `rt_bad` 0, program 0.12592 bits/body at 2²⁰ and 0.01574 at 2²³, all KS/NN values identical; timings same order (eval 109–113 ns).
- **Predictions pre-registered** (file order: predictions 12 min → outputs 7–9 min → patch 6 min); the declared held-out case (2²³) passed everything. Two undisclosed but benign NN misses at the tuned sizes (median −6.25% vs ±5%; keyset-1 p1 −29% vs ±20%), one-cell/tail noise, exactly equal at 2²³ — named in the check.
- **My attacks strengthened the claim.** Cross-column 64×64 joint χ² plus serial tests — the gap in the author's battery, since the E/L two-sample KS is a deterministic function of (p,e) — put both author keysets and four random odd keysets at |z| ≤ 2.0, identical to an iid control (no tuning). Same-cell conjunction pairs at 2¹⁸: iid 129, mix 126, lattice 0. The lattice negative control is *understated*: its duplicated generator makes ω exactly the high half of p ((p,ω) χ² z = +185,319) — invisible to its own tests.
- **Premise flip verified:** the 121-bit "floor" is the cost of preserving one i.i.d. sample (121 bits → 15.1 GB, 72 bits brutal → 9.0 GB, neither fits 8 GB); `Prog::{Const,Affine}` + Boyer–Moore majority confirms form P rejects a belt today; B18's two-sided rule (`memory.rs:17`) would score a 16 KB billion-body belt as a false claim — the one adoption dependency for the integrator.
