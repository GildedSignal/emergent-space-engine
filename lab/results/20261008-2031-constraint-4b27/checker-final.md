Working...
Check complete. `lab/results/20261008-2031-constraint-4b27/check.md` written; tree restored clean (only `check.md` added to the run folder).

**Grade: silver.**

What I did and found:

**Reproduced (clean tree, patch applied myself):**
- Baseline benches: digest `41343a14…`, gather shares 0.737 (rtf 1) / 0.693 (rtf 100) — match stored.
- Gated bench: digest **bit-identical** to baseline, share 0.29, engine now top share — the constraint moves exactly as claimed.
- Profiler at rtf 100 and rtf 1: readouts 4/0 per frame, gather 83.6/46.5 µs, display diffs, gate counters, worst offender — **bit-for-bit the stored output**.
- Exactly the two disclosed cache-purity tests fail, at the ~1e-4 tolerance.
- Predictions genuinely pre-registered (mtimes: baselines 20:33–34 → predictions 20:42 → gated runs 20:55–58).

**Why not gold:**
1. Held-out prediction 3 breached both bounds (direction 13% over; light-seconds 10× over), and the author's own pre-registered kill criterion says that kills the mechanism as built — it was disclosed but not invoked; the re-derivation is post-hoc.
2. My adversarial 5400-frame run pushes display error to **1.675e-4** — past the claimed 1e-4 ceiling, worst offender a *planet* (long event-free arc), showing the one-probe curvature cap is not a bound. (240-member and rtf-400 cases hold; the span mechanism works.)
3. The 7× frame headline mixes machine states: the stored baseline leg was uniformly ~4.7× slow (engine p99 5.25 vs my 1.36 ms). Matched-state: frame 3.1×, gather 6.9×.
4. Adoption requires an integrator decision to relax the frozen cache-purity contract — not one step.

Gold path named in the check: consistent tolerance bounds from one display quantum, a two-sided/re-probed cap that survives ≥5400 frames and rtf ≥400, and a same-machine-state bench pair.
