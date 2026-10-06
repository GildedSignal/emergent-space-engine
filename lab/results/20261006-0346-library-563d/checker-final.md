Working...
Check complete. `check.md` written to `lab/results/20261006-0346-library-563d/`; nothing else in the run folder touched.

**Grade: silver.**

What I did, in order:

1. **Reproduction (exact).** Clean-tree rerun of `allocator_probe.py 5000 10` (20.4 s): all 90 cells bit-identical to the author's JSON, 0 control violations, only `wall_s` differs. `patch.diff` is empty; `run.log` is empty.
2. **Engine correctness, two independent ways.** A from-scratch discrete-event re-implementation matches lateness multisets within 1e-6 and Lmax to 4 decimals; theorem checks (EDF Lmax-dominance, SRPT mean-flow dominance, clairvoyant-Lmax dominance) over 270+ configs: 0 violations.
3. **Numbers.** Every primary dossier number verified from the JSON, including the ≤1.18× LL/EDF parity on pooled *and* worst-seed p99, and 0.87% vs 30.78% misses. Predictions pre-freeze is supported by mtimes (probe → predictions → results → dossier); 4/5 held, P3's failure honestly diagnosed.
4. **Adversarial cases (4).** ρ=0.99, α=1.1, tight one-decade slack all confirm the headline directions — but **slack correlated with unit size** (the run's own named blind spot) breaks the P2 constant: EDF beats LeastLaxity 2.1× on p99 there.
5. **Novelty.** H0172 already *measured* six scheduler lessons on the real allocator, contradicting "no HISTORY entry measures allocator disciplines"; compute-ahead was already in the design (H0159, plane.md #7). New here: the ordering-vs-forecast split and the SRPT starvation magnitude.

Why silver, not gold: the 10× is synthetic-model headroom against a clairvoyant upper bound that ignores speculation discards — no engine number moved; the ordering-closed constant fails in the engine's likely slack regime; three secondary statements are not regenerable from the shipped JSON (SRPT "643–2753 in capped cells" includes an uncapped cell; "7/9 at 2.8–39×" is really 6/9 at 2.4–39.5; "every online policy misses 46–63%" excludes SRPT at 15–22%). Gold experiment, named in the check: wire compute-ahead into the plane's slack queue and read B10 before/after.
