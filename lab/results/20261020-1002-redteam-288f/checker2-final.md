Working...
Check complete. **Grade: gold** — written to `lab/results/20261020-1002-redteam-288f/check2.md`, with one correction to the author's wiki page.

**What I did:**

1. **Reproduced exactly** — `bash regen.sh`: ALL PASS (7.6 s); every dossier number traces bit-for-bit to results.json. `work/patch.diff` empty (pure probe, nothing to apply).

2. **Verified the physics independently** — re-derived all closed forms from the Schwarzschild static-orthonormal Riemann: radial γ²(2+β²)/2, along-motion exactly 1× (γ⁴(1−β²)², the tθ cross-term load-bearing), out-of-plane γ²(1+2β²), radial-infall channels exactly Newtonian; trace-free at every β; the circular limit equals E9's frozen w(3γ²−1) identically. The script's contraction matrix and Fermi-frame machinery are correct GR.

3. **Four adversarial cases**, one outside the author's range: an **oblique 45° β=0.7 flyby** (their launches were all axis-aligned; the cure's cross-term structure holds — letter matrix 152% wrong vs cure 29%, exit 16.3% vs 1.8%); **β=0.95** (letter still 12× off; the cure's [th] channel inverts — license boundary at 0.9 is real); **r=20M β=0.5** (1.511 vs closed 1.496 — amplification is purely kinematic); **mirrored member** (odd symmetry clean).

4. **Citations all real**: frame.rs ships the Newtonian tensor with `ORBIT_SPEED_DIV=4` and the O((nR/c)²) budget line; B15 flies 0.9c fleets as free-fall dolls (the collision); γ≈120 red line is HANDOFF's baselined row. Novelty holds: the wiki names the Schwarzschild-tide seam unprobed; E9 owns only the circular case, cited honestly.

5. **Blemishes named** (none load-bearing): P6 counted "held" though its conservation clause is violated at β 0.999 (6×10⁻⁸ vs 10⁻⁹, disclosed in Evidence but not the Predictions summary); the claim sentence reads the β 0.99/0.999 closed-form rows as measured; the printed coefficient table's header is off by one column. Wiki page tightened in place (od 3 now carries the measured 0.95 boundary and the oblique confirmation); topic stays open (one gold, not three).

The kill is the red-team lens's exact job: the shipped interior law is wrong by an error of *type* at its own legality boundary (10% coefficient / 30–115% per orbit where the letter budgets 6.25%), the cure is the same integer kick with closed-form coefficients, and the hyperbolic E9 arm is freeze-ready — adoptable in one integrator step.
