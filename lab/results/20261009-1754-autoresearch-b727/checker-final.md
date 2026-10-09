Working...
Check complete. `lab/results/20261009-1754-autoresearch-b727/check.md` written: **Grade: lead** (agreeing with the author's self-grade, on stronger evidence).

**What I verified:**

1. **Reproduction** — applied `work/patch.diff` to a clean tree; both digests regenerate exactly (`1f057b83…` tuning, `854b4b51…` held-out = `heldout_before.txt`); timings match the dossier's "after" row; all 97 space+universe release tests green.
2. **Timing A/B** — built base/patched binaries and interleaved them: bank −0.7…−1.6%, strong-field −4%, near-separatrix flat. The dossier's circular −13% is single-run baseline inflation (my interleaved base min is 3307 ns → real gain ~−3%).
3. **Adversarial attacks, all clean** — my own 3.3M-case `Scalar::add` differential vs the reconstructed original (0 mismatches, incl. gap 0/64, carry edges, exponent-32767 fallthrough); 8.0M-input isqrt property test (all exact floor-sqrt); a 72-combo adversarial orbit bank (near-parabolic k≈1, `newtonian`'s cached `half_time`, two Rebinding scales, error paths) — identical digest on both trees; and the shipped `xtask universe --kick-bench`: bit-identical digests, kick median −1.3% (noise).
4. **Predictions** — `predictions.md` mtime predates `heldout_before.txt`; invariants held, H1's 15–35% honestly reported failed (I confirmed the `weak_quad` dispatch explanation in source).
5. **Novelty — the deciding point** — commit `1932f6c` (1 Oct, gpt-6.1-sol, integrated) already did bit-identical micro-optimization of this same crate (kick median 25.75→23.71 µs, −8%) and added the very kick-bench the author didn't run; the taste log already holds "the lever is cadence". The run's real contribution is only the explicit "exhausted" measurement — one board line, as the author says.

Tree restored to clean (only untracked `lab/results/`); run-folder files untouched apart from `check.md`; no git commit/push.
