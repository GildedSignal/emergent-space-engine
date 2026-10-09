Working...
Check complete. `check.md` written: **Grade: silver.**

**What I did and found:**

- **Reproduction (exact):** applied `work/patch.diff` in a clean tree, built (22.5 s), ran all four commands from `commands.md`. Every output JSON is identical to the stored ones field-for-field, digest `83d96bed…` included — cross-build determinism confirmed. Each run < 1 s.
- **Predictions genuinely held out:** `predictions.md` at 17:58:54 vs decisive runs at 18:03:35–38. 3/6 held; the three failures (P(dv=0)=0.0, bits/binding 94–121 vs predicted 15–90, bytes_per_body 4786 vs 60–300) are honestly reported in the dossier.
- **Adversarial case 1 — dead stream:** `pop.dperi` is never fed in the bench loop, yet the dossier claims "periapsis-time delta 0 (never moved)". I fed it (one line): it moves on **every** binding at 15.2 bits (made, p_zero 0.0). Corrected: 136.6/101.3 bits per binding, 0.93 bits/ship/game-s, 68.7 s saturation — the headline survives and strengthens, but the per-stream table is partly false.
- **Adversarial case 2 — quiet scene** (`--members 4`, no fleet): rate 0.67, saturation 95.5 s. Not battle-bound.
- **Adversarial case 3 — long horizon** (rtf 400, 6 000 game-s): stationary bits/binding, no diffusion blow-up.
- **Adversarial case 4 — patch regression:** the patch *replaces* the `--kick-bench` flag arm, so the existing cadence instrument now errors with "unknown universe argument". Unreported adoption cost.
- **Novelty:** HANDOFF says H_live "not measured yet"; law.md's "+62/−60" is an unmeasured guess. No HISTORY entry measures the live rate.
- **Gold denied because:** the shipped instrument isn't final (dead stream, broken flag), one evidence claim is false, the EMA only bounds mean-style refits, and the 10⁹-ship extrapolation is unstated in the claim line. The named gold experiment: belt scene with true per-body program refits at reabsorption, instrument completed.

Tree restored to pristine (`xtask/src/universe/mod.rs` reverted, `hlive_bench.rs` removed); only `check.md` added to the run folder.
