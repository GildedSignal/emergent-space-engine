Working...
Check complete. `lab/results/20261014-2012-system-a669/check.md` written — **Grade: silver**.

**What I did:**

1. **Reproduced** — `regen.sh` exit 0, `work/key_quantum.out` regenerated bit-identically (59 s). All cited code facts verified on the shipped tree (`step.rs:424-433`, `binding.rs:419-448` unconditional `Orbit::compile`, `bind.rs` residual/slot catalogue, roster, cadence; the composed priors b29a/0e37/cf45 all trace to the nladder page). `predictions.md` (20:20:47) predates the decisive output (20:24:07); P1/P2/P5 held, P3/P4 honestly reported as failed.

2. **Four adversarial cases** (my own script, outside the author's range where possible):
   - Held-out seed + 96 bodies: every headline number reproduces (flip 0.299, |ΔL|/L p50 2.08×10⁻⁷).
   - Eccentric tail e∈[0.25,0.39]: unchanged.
   - Inner system 0.45–0.85 AU: still flips at any grain — unification broader than claimed.
   - Quarter cadence h/4: linear in h, **but** the p01 |ΔL|/L falls sub-quantum — the 100%-flip claim is cadence-thin (3.2× margin).

3. **Found three real corrections**, applied to the author's wiki page in place:
   - The L dial ("~2¹²–2¹³") was arithmetic on a diffusive assumption; measured it's linear — run 107 needs **~2¹⁵–2¹⁶**, so the composed "~10²× at 2⁵/2¹³" is ~3–4× optimistic (pair run ≈ 22).
   - The live tube key is `OrbitKey{periapsis: Scalar, k: Q48}` (orbit.rs:31), not the legacy Darwin E/L `Key` whose documented range the bracket uses — conclusion holds a fortiori, numbers describe legacy words.
   - Novelty: exact-key-never-recurs is standing record (`memo.rs` test, `law.md:36` "**Not adopted:** a quantized (E, L) memo… random walk (principle 13)", H0213) — the run's true delta is the flip gate + residual carry, and adoption needs B1/B2/B9 re-judged, not just B5/B12.

**Silver, not gold:** real, reproduced, mechanism robust — but measured on a replica, partially re-deriving known record, with the gain overstated at the stated settings. The one gold experiment is the author's own build (flip-gated rebind, digest held on non-flip kicks, gates re-judged at ≥2⁵(E)/2¹⁵(L)).
