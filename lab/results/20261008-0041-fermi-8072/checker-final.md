Working...
Check complete. `lab/results/20261008-0041-fermi-8072/check.md` written; nothing else in the run folder touched (work/patch.diff was empty — all work ran in the results folder; I reproduced from copies in `/tmp/check-8072`).

**Verdict: gold.**

**Reproduction** — all five runs (A1, A2, B, C, D) regenerate **bitwise** (states and snapshots); shipped `analyze.py` regenerates every headline number; `mk_synth.py` rebuilds D identically; wall times match to shared-machine order. Controls hold: drift-only C gives |Δa/a| exactly 0.0; my independent P_J/256 run (9.1×10⁻⁴ vs 7.8×10⁻⁴) confirms the osculating spread is dt-independent.

**Predictions** — `predictions.md` (T+0 by mtime) predates every final run. P1/P2/P3 held (P1's marker replacement was disclosed and dt-controlled); P4's growth arm failed honestly with the Myr boundary pre-registered.

**Adversarial (5 of my own)** — permutation tests: synth KS(a) p=0.29, KS(e) p=0.11 (indistinguishable; my first bootstrap was buggy and briefly suggested otherwise); the synthetic's KS deviation is inherited from its birth fit and does not grow (stronger than the dossier claims); per-resonance drift structure matches A/D/B; a symmetric-kick map variant leaves the P1 structure unchanged (not an integrator artifact); gap-depth difference is 1.5σ Poisson.

**Blemishes recorded** — `metrics.json`'s `f_chaos_series` is stale (all 1.0, pre-fix formula) while shipped code gives 0.103–0.122, and `analyze.py` was edited after `metrics.json` without disclosure (the dossier number *is* regenerable — the inverse of the usual failure); the dossier's "11.2–12.2%" understates the min (10.3%); the dt-control artifact lived only in /tmp.

**Why gold** — first measurement of the board's explicitly unmeasured decider (H_live, HANDOFF:70), kills the birth-frozen program premise (100% scarring), decides the 8 GB question across ~800× (16 GB fails → 2 GB drift-program → tens of MB shuffle), adoptable in one step; exchangeability boundary (massless, 71 kyr) honestly scoped.
