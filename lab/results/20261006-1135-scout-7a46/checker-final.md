Working...
Check complete. `lab/results/20261006-1135-scout-7a46/check.md` written; nothing else in the run folder touched (reproduction ran in `/tmp/check7a46` against a copy).

**Grade: gold.**

- **Reproduced** bit-identically: 181 floats, worst relative difference 0.0, 9 s, < 50 MB. The 18–93× column derives exactly from results.json (18.4/26.4/28.5/29.1/93.1).
- **Predictions** held where the claim needs them (exactness everywhere incl. L=0/E=0/through r=0; A's 70× degradation; ≥10× cost-to-match); two boundary misses honestly reported.
- **My attacks strengthened it**: with a fairer depth-aware step rule (dt ∝ √(r³/μ), calibrated on the same case) A still pays 18×→52×→**211×→268×** as q drops to 10⁻⁴ r_H; C stays flat one order below the author's grid; DOP853 provably cannot pass r=0 (status −1 at r=8.3e-12) while LC exits at 1.2e-15; no exit-point error cancellation; all code and memo citations verified, including opus-math:291's verbatim LC rejection.
- **Gold bar**: ≥10× on a live HANDOFF open item (`NoBoundOrbit` freeze Julien hit while flying), deletes the stepping fallback on that set, and corrects a standing memo premise. The named gap to full adoption: the integer/Q48 drift is designed, not measured.
