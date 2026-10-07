Working...
Check complete. `check2.md` written to the run folder — **Grade: gold** — nothing else in the run folder touched, no git operations.

**What I did:**

1. **Reproduction (bit-for-bit):** all three scripts rerun in a clean scratch tree — `hlive_probe2.py` (22 s, rows byte-identical to shipped), `twin.py` (173 s, only `wall_s` differs), `followup.py` (12 s, only `wall_s` differs). Empty `work/patch.diff`, nothing to apply.

2. **Predictions:** `predictions.md` (11:28) predates `twin.json` (11:33); smoke tests disclosed inside it. 4 of 8 predictions held, 4 falsified **and reported** — the pre-registered kill criteria fired and the author reported the refutation rather than the hoped-for absorption.

3. **Adversarial attacks (all passed):**
   - *Field level:* the twin's ring table ≡ my independent 512-node double-average to median 6×10⁻⁷ — the "explains none" verdict is not an artifact of a wrong twin. Indirect term's exclusion is exactly right (averages to zero).
   - *Dynamics:* propagation under my direct average reproduces Laplace–Lagrange secular precession to 1.1–1.2% at two radii. (My first attempt forgot solar gravity and "agreed" for a broken reason — caught, redone.)
   - *Horizon:* median |Δa| pinned at 1.764×10⁻³ AU through **120 yr** (2× the author's bound); E-bits p50 flat at 36.3.
   - *Clones:* u32-quantum divergence still sub-linear at 40 yr (7.6 bits mean); determinism exact.
   - *Record corrections verified:* the hardcoded `control_mu0_scarred` (`if False else 0` at line 178), void 1-phr row (coverage 0.0026), corrected play-hour ranges.

4. **Warts (noted in check2.md, none material):** dossier's "~66×" should be 42× per its own JSON; "15.5 bits flat" is E-only (total shears via M); the rms growth is a broader resonant tail than "encounter tail"; the author never validated the ring field's absolute correctness — only convergence.

The claim (twin refutes "program absorbs"; belt drift is bounded, deterministic, kick-layer machinery) moved the named board bottleneck question to a decision at zero adoption cost — gold on my independent evidence.
