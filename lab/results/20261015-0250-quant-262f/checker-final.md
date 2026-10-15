Working...
Check complete. **Grade: silver** — written to `lab/results/20261015-0250-quant-262f/check.md`, with four corrections applied to the author's `wiki/kick-jet.md` where it overstated.

**What reproduced:** `regen.sh` exit 0 (~16 s, well under 2 GB); exactness numbers bit-identical (t 3.45e-16, τ 3.59e-16, 6 iterations, recovered-u 8.9e-16); timing 12.74 µs/promotion on this box vs the author's 11.7 (shared-machine spread). I verified the integrand transcription symbolically against shipped `orbit.rs:314-343` and the belt mix against `scenario.rs:333-343` — both faithful. κ ≡ cd6e's formula confirmed on 200 random (n,M).

**What the attacks found:**
1. **Factor-2 slip in the timed batched arm** — `read_batch`'s t/τ are exactly 2.000× the Simpson-verified scalar channels (adv matches). Price, iterations and recovered-u are unaffected (self-consistent Newton, slope right to O(q)), but the batched path shipped value-unverified.
2. **Advance mis-attribution** — the 1.75e-8 persists at quad epsabs 1e-14, falsifying "Simpson's error"; mpmath at 40 dps proves the algebra exact to 7.7e-34 while the closed form's own f64 evaluation carries 1.3e-8 at belt q. It's 1/q-amplified f64 cancellation.
3. **Timing fairness** — excluded per-body coefficient solves add ~1.1 µs → ~12.8 µs honest (~9% understatement).
4. **Outside the author's domain** (e→0.999, q→1e-6): corners pass their own 1e-6 kill bar (t/τ ≤ 4.4e-13), but the 6-iteration Newton degrades to slow linear convergence at e=0.999 — belt-scoped, as claimed.

**Why silver, not gold:** measured win is ~2.5× against the ~30 µs compile anchor; the ≈4 µs native figure is still a projection, and prediction #4's own kill rule (batched/scalar ≥ 2×) never ran — no native scalar arm existed. The one experiment to gold: a single Rust arm timing shipped compile, native scalar, and native batched (setup included) at true belt keys.

Incidental: the `edit` tool refused to parse section headers for this exact wiki path while identical patterns worked on sibling files — reported to `xd://report_issue`; corrections applied byte-surgically via python instead. Nothing else in the run folder touched; no git operations.
