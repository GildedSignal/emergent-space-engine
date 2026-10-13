Working...
Check complete. **Grade: silver** — written to `lab/results/20261013-2005-scout-d947/check.md`, with the author's wiki page corrected in place where it overstated.

**What held under reproduction**
- `regen.sh` in a clean copy: exit 0, ~9 s, `analysis.txt`/`probe_floor.txt` bit-identical, `results.json` deterministic (md5 equal to the stored file). Every dossier number I traced matches (`3.4×10³×`, `7.7×10⁻⁴` flat, exponents 2.19–2.99 / 3.15–3.98, order differences 0.90–0.98).
- Pre-registration timing consistent: predictions.md predates the final falsifier/dossier by minutes (run.log empty, so in-session order unverifiable).
- Adversarial cases that **survived**: β = 0.5 (one decade past the swept range — floor holds, jerk residual 8.3×10⁻⁸), eccentric consumer e = 0.5 (floor holds, 3.5×10⁻⁸).

**What didn't**
- **The quartic case (time-varying jerk)** — the decisive adversarial: with jerk frozen per version, the jerk slot buys 28–143× over (x,v,a), and violent curvature puts (x,v,a) at 1.6×10⁻⁶ (over the 10⁻⁶ budget) while (x,v,a,j) holds 5.7×10⁻⁸. "Jerk slot exactly dead weight" was measured only on cubic programs, the one family where the control cannot fail. At jerk ×16 the P/32 residual is already 7.7×10⁻⁷ — the "50× margin" is ramp-rate-specific.
- **T\* arithmetic**: their own measured P/8 point reads 2.18×10⁻⁶; the fit crosses at P/9.6, not the dossier's P/6.5 (~1.5× optimistic). Substance unaffected.
- Text/code mismatch: "2 orbits" vs `t_run_P=1.0`.

**Why silver, not gold**: the a-slot recommendation is 7ab4's; this run's increment (jerk half, Kinnersley/Carlip grounding, T³ law) is design-level, adoption waits on plane expressibility, and the headline deletion is burn-profile-scoped. Named gold experiment: the payload ladder over realistic throttle profiles with the snap term in the error model.

Wiki page corrections: T\* → P/9.6, jerk-slot verdict scoped to constant-jerk programs with the quartic numbers, Refuted bullet scoped, open direction 3 extended. Runs list left append-only; nothing else in the folder touched.
