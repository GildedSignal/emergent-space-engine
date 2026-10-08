Working...
Second check complete. **Grade: gold** — written to `check2.md`.

**Verdict basis:**

- **Full reproduction, bit-for-bit.** Every digest in the dossier regenerated from my own runs: jet-off `eccc7f5a…` matches the *unpatched rebuild from clean main* (I restored the tree and rebuilt — the "flag-off path untouched" claim is proven, not just asserted); jet-on state/replay digests match stored JSONs; B13 41/64 worst ΔE ∞ with `renewals=4077` exact; the lifecycle failure prints identical numbers (origin 7.7232e3 vs ship 6.2629e2, cos −0.07379). Speed: 2.76× (rtf 100) / 3.23× (rtf 30) with 4.79 %/5.8 % compiles per kick; increment 8.5 µs ≪ compile/2; probe error law matches to two digits.
- **Adversarial cases (3).** Seed 2: 1.86×, still clean. 200 members: 3.15×, 95 % renewals, 0 refusals. Re-anchor tightened 64×: the lifecycle failure is **bit-identical** — the secular cancellation lives below even that threshold, and B13's worst (5.29e-2) stays 2.5× shipped. This is stronger than the author's own 43× result and shuts the "tune the anchor" escape; the 5e-10 half-interval error excludes a per-event placement bug.
- **Novelty.** `git log --all -S ESE_JET` empty; nothing in HISTORY/board. The new facts: `Entry` carries no (E,L) derivatives (verified in code), so the silver's "one flag away" wiring was impossible as claimed, and the offset-only failure mode is cancellation (principle 13's mirror), threshold-independent.
- **Predictions.** Pre-dated the decisive data (file times); the refutation condition was pre-registered and honestly reported. One nit: prediction 4's band (5–30 %) was technically missed at 4.8 %.

The run kills a wrong premise before it reached the integrator and prices the prerequisite (the derivative half, with its two acceptance checks named) — adoptable in one read, nothing to build for the refutation itself. Tree restored clean; only `check2.md` added.
