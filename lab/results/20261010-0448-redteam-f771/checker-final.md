Working...
Check written. Summary of the verification:

**Grade: silver.**

**Reproduced:** `python3 binet_probe.py` matches `probe-output.txt` bit-for-bit in a clean tree; empty patch.diff; predictions.md (04:56) precedes the run (05:13). The candidate is genuinely the frozen rung's own float64 configuration — r1-rings.md specifies float64, the exact in-band rotation, u/u′ continuity and the same dt/dφ rule.

**Central claim verified independently:** my Simpson-64 quadrature (own node placement) agrees with their Gauss-8 to 1.17e-5 on the worst case (r_p=7, e=0.99); oracle converged to 1e-8; the 1.93e-2 period error is model error at ~1650× the numerical noise. Band law, seed algebra and oracle physics all check out (weak-field precession → 6π/p with the expected 2PN-level excess; period → T_N(1+3/a)).

**Adversarial results beyond the dossier:**
- The author's own proposed fix, run at rung level (128 seeds, e log-uniform to 0.99): m16 **fails** `period_pass_fraction` (0.967 < 0.99); m32/m64 pass everything (median crossings 22/42) — the fix is a sampler + m decision, not one line.
- A second hole the dossier missed: m16's period also fails on near-circular strong-field seeds (r_p ≈ 11–13, e ≈ 0.01, up to 4.5e-3) — the hole is two-dimensional, and H0205's original m16 pass was fraction-luck.
- Error scales exactly m⁻² (bias lives in the band ODE, not the arithmetic); at e = 0.9999 the banded law misclassifies bound as unbound (u < 0); the widened domain draws hyperbolic bands the probe asserts on.
- Novelty holds (H0193 was oracle quadrature, H0183 the EIH protocol); attacks 2–4's record claims all verified verbatim (representation.md §2/§3/§6/§7 quotes, r5/r6 absent from `lab/rungs/`, taste-log numbers).

**Why silver:** real, reproduced, decision-relevant, but it stops at the hole — the remedy's consequences (m16 rung-level fail, m32 suffices, the low-e axis, the hyperbolic branch) had to be supplied by this check, half the deliverable is unmeasured Fermi/record findings, and 2/6 predictions failed. The gold experiment is named in check.md: run the re-frozen, widened r1 with the per-e period-band decision argued from the measured m⁻² law.
