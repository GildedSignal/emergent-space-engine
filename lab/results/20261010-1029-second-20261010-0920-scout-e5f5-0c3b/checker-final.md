Working...
Check complete. `check.md` written — **Grade: silver**.

**What I did (45 min):**

1. **Reproduction** — ran the dossier's command in a clean tree: both error-bearing configs (`s32_q1_T12_dip_pre` and the scalar control `s32_q1_T12_sca_pre`) regenerated every digit of the shipped record — counters, flush-by-level, all six error snapshots each. Fine-q/s16 configs verified arithmetically against the shipped JSON; author's files untouched (md5 before/after).

2. **Canonical claim, independently** — my own re-derivation of the l*-partition: exact one-channel cover at both sizes, member counts 9/40/147/588/240 and 9/40/147/60, uniform over sources, and the θ_l = q·(1.5c_l)² geometry is tight-but-sound. Confirmed with zero shared code.

3. **Adversarial (3+ cases), which decided the grade:**
   - **Horizon** (the author's own wrong-maker #1, unmeasured by them): side 16, warm, extended past the light-cone fill — the error keeps walking (median ×2.9 over 5.5×, no plateau past t=32; two independent samples agree). "Bounded and near-stationary" is a window artifact: every shipped side-32 error number lives inside the fill transient (T=12 vs fill=64). The compounding kill itself stands (error class changed from ×79 multiplicative to diffusive).
   - **Overshoot constant**: the "new constraint" cites 0.042; measured 0.126 (closed form (a+b)/4). Wrong by 3× — though the stated floor q≈0.004 matches the *correct* constant, and the fine-q absolute errors confirm the mechanism.
   - **Strength-law extremes** (asserted, never run, by the author): both directions measured; error constant tracks the overshoot ratio, non-compounding holds at short horizon.

4. **Novelty/goal fit** — FMM is prior art in the repo's register; the new matter is the exact partition + member quanta + the floor. Not gold: the letter fails twice (3–9·Lq walking error; O(log N) at ~11×), and my probe converts the disclosed caveat into a measured refutation of the headline's stationary half. One experiment to gold: bound the walk (quadrupole members or flush re-biasing), demonstrated at T ≥ box/2, warm, two seeds.
