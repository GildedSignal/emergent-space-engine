Working...
Check complete. `check.md` written to the run folder; nothing else there touched (all reproduction ran in `/tmp/check-cd52`).

**Grade: silver.**

**What I verified:**
- **Bit-exact reproduction** of every headline number: negative control (λ_raw 0.023030605, fb 0), positive control (λ_raw 9.63, dH 8.98, fb 63782), belt cell (fb 694730), horizon scan (fb 2026/9120/35742 at 5/10/25 orbits, λ_raw 7.054@5), and P5's exact fit (λ_exp 2.9895, R² 0.9915 vs 0.972). Selftest passes. The pre-fix binary rebuild reproduces matrix_raw's cad64_s1 bit-exactly — the bug disclosure is genuine (though its 10×/41× factors measure as 5.9×/17.8×).
- **Predictions genuinely predate the decisive matrix** (21:55:19 vs 21:56:03), with the caveat that P1's range was already measured in pilots.

**What I found that the author missed:**
1. **The sharpest claim (P5) is misattributed.** λ at μ=1e-5 is dt-robust (λ_exp 2.26/2.99/3.3 at spon 16/64/256 — no collapse with refinement), and λ/Ω ≈ 0.48 with Δa/R_H ≈ 0.16 puts this belt in the dense-ring Wisdom–Tremaine regime where λ_max ≈ 0.5Ω is *real* and mass-insensitive. The dossier's "manufactured chaos" reading is unsupported; coarse-cadence fb=0 is manufactured *cleanliness* (missed ejections).
2. **The claim they got right is even stronger than reported:** extending cadence to 512/orbit, corruption *worsens* monotonically (fb 7.6e4→1.85e6, λ_raw up to 70/orbit) — no cadence escapes.
3. **Record defects**: `results.json` is unregenerable (fit.py matched corrected-matrix result lines to buggy-era curve files via the `r_` naming mismatch); `matrix_raw.log`'s tail ran on the fixed binary (mixed provenance, undisclosed); dossier's fb "2.0e6" and λ "1.3–14.4" ranges aren't backed by the shipped log.

**Gold path:** one dt×N scan of λ_max at μ ≤ 1e-5 read against K = Δa/R_H — it settles whether game-scale belts carry real λ ~ 0.5Ω (H_live's physical floor) and regenerates the record.
