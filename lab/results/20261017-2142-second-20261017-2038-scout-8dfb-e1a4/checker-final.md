Working...
Check complete. **`check.md` written: Grade: gold.**

**What I did (45-min budget):**

1. **Reproduced**: `regen.sh` exit 0, output bit-identical to `regen.log` modulo the disclosed timing line. Every dossier number verified against the log (4.38e-14 / 3.67e-12 same worst row / 28 raw = 2.40 µs / 8 memoized = 0.86 µs, arithmetic checked / census 527-80-23 / LT 0.975–0.986). `orig-falsifier.py` byte-identical to the original branch's shipped instrument (git diff empty).

2. **Independent attacks, five outside the author's range**:
   - Own 50-dps quadrature (own code/nodes/solve-polish): worst |PURE − mine| = **2.7e-13** over 10 rows — 10× tighter than claimed; the record's 3.67e-12 is its own quadrature's precision, not the port's error.
   - Outside-range rows (a=0.998∧e=0.9∧θ=85 combined, a=0.9999, θ=5°, e=0.95, retro θ=175°): all ≤ 2.7e-13; the 8-kernel count holds on every one.
   - J identity in exact arithmetic on 13 adversarial (n,m) incl. n<0, n→1⁻, m≈n: worst 1.55e-13; m=0 limit checks against the textbook formula.
   - LT beyond p=30 (p=60/120/200, a∈{0.1,0.4}): 0.962–0.993, inside the freeze band, converging →1 with p.
   - **One overstatement found and fixed**: the census confinement "a ≤ 0.3 ∧ e ≥ 0.5 ∧ p ≤ 7.5" is a grid artifact — my probe puts a=0.45, p=6.5, e=0.9 in the same 4real/1below class (the grid never sampled 0.3 < a < 0.6). The refusal criterion itself is root-case-driven and unaffected.

3. **Novelty**: prior art inside the lab is cd6e's *incomplete equatorial* squared-pole reduction; this run's J is the *complete-integral* form the inclined compile needs — exactly the previous checker's named experiment. Cross-link added to the page.

4. **Page**: fold verified number-for-number; two in-place corrections applied (confinement bracket, cd6e credit). Nothing else in the run folder touched; no git operations.

The gold rests on: bit-for-bit reproduction, independent confirmation tighter than claimed, pre-registered predictions with honestly-reported misses (P5's mechanism clause self-refuted and reported — pre-registration working), and every deliverable of the silver's "one experiment" landed. Named gaps for the build: the a=0 degeneration is currently inexpressible (NaN polar constants), fsolve is fragile beyond the run's grids (101/270 failures in my sweep), and the 0.86 µs prices kernels only, not the surrounding float assembly.
