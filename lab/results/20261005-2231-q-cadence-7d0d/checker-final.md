Working...
Check complete. `check.md` written at `lab/results/20261005-2231-q-cadence-7d0d/check.md`; nothing else in the run folder touched, no git operations.

**Grade: silver.**

What I did and found:

**Reproduced** (clean tree, empty patch, own harness — my phases, scipy DOP853 rtol 10⁻¹² as reference):
- Drift exactness: ≤ 1.5×10⁻¹¹ over 2000 round trips — dossier's claim holds. `validate.py`'s own 10⁻³ "dE/E" output is a birth bug in that script (missing 1/(1−e·cosE) factor), and its classical block can't finish in 120 s here.
- Replica validated independently: N=256 ≡ DOP853 at ratio 1.0000, no ϖ-rotation (rebuilt the control the author described but didn't save).
- Micro-frontier: N* = 4, 4, 8, 8 at f = 0.2/0.3 × e = 0.1/0.3 — exact match, flat in e.
- The walk (central claim): N=8's apsidal deviation grows 4.4% → 9.7% from horizon 12 → 27 while the reference stays exact — the low-cadence error walks, confirmed by an independent integrator.

**Adversarial finds the author missed:**
- f = 0.45 R_H: in six phase draws, every draw ejects one phase — the N* = 16 point rides on bound-phase luck, and `cad.run` guard-crawls (>220 s, 3M-iteration cap) on escaping excursions.
- Out-of-sample miss: at (0.35, 0.1) the fitted rule predicts 16, measured 8 (bar-marginal 0.095 vs 0.10) — the τ-vs-synodic degeneracy bites.
- `rule.py` doesn't implement the dossier's rule: no Φ(f) term, `resonance_distance()` is a stub, GAMMA 4.7 vs RULE.json's 0.0; the frontier script itself was never saved.
- Horizon mismatch: fitted at 12 orbits, B14 judges at 50 — the run's own walk logic undercuts the headline gain at gate horizons.

Not gold because the decisive validation never ran (author-reported, corroborated by empty logs and absent `.npy` artifacts), held-out predictions are untested, and the record can't regenerate the headline numbers as shipped — the exact silver-failure mode in the taste log. The one experiment to gold: run the already-built `mixed.py`/`b12.py` suite plus the 240-job grid on a quiet machine, with `rule.py` actually implementing Φ(f) and routing, and an ejected-phase mask in the gate.
