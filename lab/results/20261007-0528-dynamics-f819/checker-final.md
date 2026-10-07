Working...
`check.md` written — **Grade: gold**. Summary of the check:

**Reproduction (exact).** Clean rebuild; `redteam-plain`, `redteam-fma`, `permute-plain` all regenerate byte-identically (45.7/35.6/27.1 s). Per-ship step detail matches to the digit (z −4.91…+7.58, leak −3.42e-9…−1.40e-8; leak plant +3.00e-9 on 15/15 judged ships). Baseline matches the parent dossier (q-b12-design-9242, whose checker died on a 429 — this run also supplies its missing reproduction). Tree clean, patch empty as claimed. One transcription slip found: echo perm-sd is 0.95, not the dossier's 0.93 (range claim unaffected).

**Record.** `predictions.md` (05:41) written after the disclosed baseline (05:39), before every plant run (05:43+). The author's kill criterion fired (P1–P3 falsified) and was reported as the pre-registered negative result, with the mechanism (O(1) C_J-vs-synodic-phase gain in the rotating frame breaks the kernel argument).

**My three adversarial attacks, all on a scratch copy (`/tmp/adv-b12`, run folder untouched):**
1. **Switch-time sweep** (the run's own named missing experiment): the bounded step FAILs at 40/60/120/150/180 P on plain (z to +31.8) and at *all* switch times on fma; step80 flips like step95 (+4.01 PASS → +21.10 FAIL). The gray zone is the error class, not a 95P artifact — *stronger* than the dossier claimed.
2. **clock1e-8**: a second machine-dependent verdict (plain FAIL +6.69 → fma PASS +3.64).
3. **Sub-cap boundary**: the arrow still catches linear drift at 1e-8 (~0.02 R_H slip); the passing blind spot opens only where drift ≪ 0.1 R_H — confirming the cap-delegation bound the dossier states.

The author's proposed discriminator (per-ship leak coefficient) survived my worst case: step150 reads scattered negatives (−1.5e-9…−4.8e-9) vs the true leak's uniform +3.00e-9.

**Why gold:** exact reproduction, honest pre-registration, findings that survived independent attack, two premises falsified (the parent's two-path verdict identity; the author's own kernel premise), zero-code adoption — the freeze conditions the integrator needs before B12 re-freezes. Run folder otherwise unchanged; no commits, no pushes.
