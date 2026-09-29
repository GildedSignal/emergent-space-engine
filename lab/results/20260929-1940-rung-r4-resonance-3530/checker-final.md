Working...
Check complete. Deliverables written to the run folder: `metrics-check.json` and `check.md` (nothing else touched, no git operations).

**Verdict: KILL, undisputed** — `verdict.py` on my metrics-check gives the same outcomes as the author's on every criterion.

**What I found:**

1. **Reproduction is bit-exact.** `gcc -O2 && ./r4` (14.6 s) reproduces all 40 rows and `metrics.json` with zero differences. `predictions.md` (20:11) genuinely preceded the decisive run (20:17:40–55, single process). Selftest 1.8×10⁻⁹ confirmed.

2. **A first-order sign bug invalidates the dossier's evidence, not its verdict.** `osc()`/`rv2el()` use `(v²/μ−1/r)r⃗ + (r·v/μ)v⃗`; the eccentricity vector is **minus**. Proven three ways: `none`'s max_e 0.051944 on a pure e=0.05 Kepler orbit (should be exactly 0.05); `rv2el` round-trip velocity error up to 8×10⁻² with pericentre flipping by π (correct formula: 10⁻¹⁵); so after *every* kick the event layer propagated a misread orbit — the rung's "exact Kepler cycles" never ran as specified.

3. **Clean-room RK4 oracle** (correct elements, two resolutions agreeing to 6 digits): r21 truth max_e 0.076 (author 0.081), r21b 0.163 (author 0.183), and the resonant angle **librates** — C = 0.49/0.39 where the author reported 0.07 circulation. A phase scan hits C = 0.92 at w₂ = 1.0, essentially the red-team's 0.867 anchor: the author's "~450-scene search found no libration" was a broken thermometer, and the lib criterion was live all along.

4. **Sign-fixed re-run still KILLs both candidates** (conj-quad 2.0–8.9×, conj-oct 5.7–12.2×, controls *damp* rather than over-pump 8–35×; negatives still fail). The kick kernel itself is correct — I verified analytically it is the exact l=2/l=3 interior-perturber tide, and the closed-form integral checks at 1.8×10⁻⁹.

Net for the integrator: the configuration (full-synodic-window straight-line impulse) is dead on corrected legs; the author's truth values, "no libration" conclusion, and 3–11× quantification should not be quoted. Next rung: two-character fix, a Kepler round-trip control, explicit l≤1 assignment, red-team scene at w₂ ≈ 1.0.
