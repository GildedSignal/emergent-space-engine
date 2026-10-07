Working...
Check complete. `check.md` written: **Grade: silver.**

**Reproduced** (clean worktree at main 70f27a9, patch applied by me):
- B18b: FAIL `belt_birth is not implemented` → **PASS, 5 frozen runs**, statistics bit-identical to the dossier (chi2 2.80/4.5, serial 3.13/5, KS 0.56, birth 31 B, 32 B at 1e9, 9.7 B/scar); B18 FAIL unchanged before and after; frozen judge untouched by the patch.
- shipmem 5+2 tests, xtask 3+1 tests pass; two CLI invocations print identical bits.

**Adversarial** (all pass): unseen seeds 424242/777 at 2²⁰, unseen seed+size 555 at 2²³ (the author's thin bottom-reach margin — worst count z 1.86); restore fuzz (every single-byte mutation, truncations, trailing junk refused, no panic); wt/belt's frozen `E[0]=1174440` vs judge threshold ≈1062976 confirms the old table's bottom-tail kill (z ≈ −7.25, the dossier's number exactly).

**Why not gold — two record defects, both confirmed:**
1. Dossier claims tuning on a "non-frozen seed", but predictions.md itself discloses a pre-prediction judged run at seed **20261008 = frozen run #1** (`RUNS[0]`), which also ships as the patch's unit test. Honest disclosure, mislabelled summary; runs 2–5 were genuinely held out.
2. "cargo test --workspace — all pass except lattice-metal's fuzz" is not regenerable: 9 further xtask tests fail (B12-echo, handoff ×5, plane kick, behave_cli ×2). I ran all 9 on pristine main — identical failures, so the patch regresses nothing, but the quoted evidence line is false (likely a fail-fast aborted run misread: lattice-metal fails first and cargo skips xtask's suite).

One step to gold: append those two corrections to the record. The physics needs nothing — it deletes the frozen table, corrects the premise that the committed gold program was tail-safe, and is adoptable in one step.
