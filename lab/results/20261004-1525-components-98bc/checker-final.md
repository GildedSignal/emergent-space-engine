Working...
Check complete — `check.md` written, grade **gold**. Summary of what I did:

**Reproduction (exact).** Applied `work/patch.diff` to the clean tree, ran all three dossier commands (55 s total). Every deterministic number matched the stored jsonl bit-for-bit: blocks 157.39/157.37 bits/body, program 0.50366/0.12592/0.01574 (exact 1/n), scar counts, all KS/NN values, both keysets identical. Floor arithmetic independently verified (121 bits = 15.1 GB at 10⁹; 72 brutal-player bits = 9.0 GB; blocks = 19.7 GB — the lossless iid belt is arithmetically dead against 8 GB).

**Held-out check.** `predictions.md` mtime 15:37:03 predates all result files (15:40–15:42) and states the code hadn't run. Predictions held on every claim-bearing number; the one miss (blocks 1.30× vs ≤1.25× floor) was self-reported and secondary. The 2²³ run was genuinely held-out: mix passed, lattice kill grew with density.

**Adversaries (3, fresh code).** (1) 2-D χ² equidistribution in the (p, t_p) plane — mix 16,305 vs iid 16,107 at dof 16,383: the lattice-killer statistic does not fire on the mix. (2) Lag-1 and cross-column correlations ≤ 1.5×10⁻³ ≈ 1/√n — no counter structure. (3) Sustained churn over 12 epochs at 1%: scarred fraction grows as 1−(1−r)^k, per-scarred cost bounded 60–74 bits, reabsorption ≈ 0 — fills the gap the author admitted but didn't measure; saturates near 7.5 GB at 10⁹, so churn×epochs must stay ≪ 1.

**Novelty & fit.** `Prog` today carries only `Const`/`Affine`; the frozen B18 ladder has no belt rung. The B18 charge verified verbatim in `xtask/src/behave/memory.rs:17` — "under half the floor is also a failure" — so a 10 KB belt would fail B18 today while 19.7 GB blocks pass. Direct hit on board focus item 5, ~10³× measured.

**Gold because:** reproduced exactly, pre-dated predictions held, 1,246× on a live bottleneck, mechanism demonstrated end-to-end (eval 109–129 ns, form P's own seal codecs, fidelity behaviours), elegant alternative killed by measurement, misses disclosed. Author's blind spots named: column-correlated belts, churn steady state, the 10⁹ gather.

Tree restored (both example files removed; only `?? lab/results/` remains untracked).
