Working...
Check complete. `check.md` written to the run folder; nothing else in `lab/results/20261008-1947-redteam-efb2/` touched; no commits or pushes; all my probe scripts stayed in `/tmp` and stayed well under the memory cap.

**Grade: silver.**

What I did, in order:

1. **Reproduced bit-identically** — `gather_falsifier.py` reran in 30 s, JSON identical to the stored results, every dossier number matches the log.
2. **Independently confirmed the solver claims** with my own code and a float128 truth (no shared harness): B (doll frame) ≤ 1.6×10⁻⁸ s error, 0 wrong roots at γ = 2×10⁶; A (raw observer frame) median 2×10⁴ s wrong roots — and I verified the ulp/slope mechanism analytically (slope ≈ −2.5×10⁻⁷ vs ulp(8×10¹³ s) = 0.0156 s ⇒ ~10⁴ s ambiguity). One bug found on the way was mine, not the author's (an inverted bracket-expansion condition).
3. **Adversarial split of the aliasing claim** — the decisive finding: the γ = 125–300 sweeps are flyby-contaminated (D0 = 100 ls, observer passes the system mid-run). Pre-flyby frames at γ = 125/250 are 100 % Nyquist-broken and render 96–98 % frozen — the wagon wheel is real; post-flyby frames (the majority) are *honestly* frozen (receding Doppler; apparent = local truth to 9×10⁻⁶ rad), so the dossier's 75–98 % aggregates overstate the failure against a truth column that uses the approaching k throughout. The γ = 2×10⁶ rows are flyby-free and genuinely aliased.
4. **Broke the frozen statistic** — median-of-wrapped-positions false-positives below the author's own boundary (its JSON says 94–99 % frozen at γ = 22.4–70.7, β_o = 0.05, where my per-emitter circular mean shows the render exact); the dossier's "= true (clean)" table row is contradicted by its own log.
5. **Verified every anchor** — B11's tolerance formula and arithmetic, the doc-rot claims (representation.md:31–32 vs law.md's `space-darwin16-v1` kill, missing df81 re-anchor), r6 unwritten, the "γ to 10⁶" queue lens, and novelty (no prior aliasing work; B16 is a different failure). Predictions genuinely preceded the decisive run, and the falsified P3/P5 were reported honestly.

**The one experiment to gold:** run r6 as proposed — flyby-free scenes, per-emitter statistic, local truth, and the k-averaged sprite law actually implemented, passing where the instant-sample law fails.
