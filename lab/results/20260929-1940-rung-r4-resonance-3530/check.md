# Check — rung r4 (run 20260929-1940-rung-r4-resonance-3530)

**Abstract (for the integrator).** Reproduced bit-exact: the author's command reproduces all 40 rows and `metrics.json`; `verdict.py` on my `metrics-check.json`: **KILL, undisputed**. But the implementation has a first-order sign error in the osculating-element formula (`+ rv/μ·v` for `−`): `none`'s max_e 0.051944 on a pure e=0.05 Kepler orbit (correct 0.050000); `rv2el` round-trip velocity error up to 8×10⁻² (correct formula 10⁻¹⁵); clean-room RK4 truth gives r21 max_e 0.076 (author 0.081) and angle concentration C=0.49 (author 0.07 — the angle **librates**; the lib criterion is live). Sign-fixed re-run still KILLs both candidates (2.0–8.9×, 5.7–12.2×). The KILL stands on corrected legs; the dossier's truth values, "no libration" search, and 3–11× quantification do not survive.

## Reasons

### 1. Reproduction — exact

- Author's command, clean tree, `work/patch.diff` empty: all numbers identical, none differ. Selftest 1.802e-09 as claimed. Timing 14.6 s vs claimed 15 s.
- `predictions.md` mtime 20:11:18; decisive run 20:17:40.1–54.9 (one process, `r4.c` 20:17:40.097 → 25 data files in program order → `run-output.txt` 20:17:54.98). Predictions genuinely preceded the decisive run.
- Predictions score: conj-quad 0.5–1.3 predicted vs 5.6–10.9 measured (miss, honestly reported); "oct halves the error" was an artifact of the bug (fixed: oct is *worse*, 5.7–12.2× vs quad 2.0–8.9×); negatives-fail and cost predictions held.

### 2. Independent implementation check — first-order sign bug

`osc()` (r4.c:248–249) and `rv2el()` (r4.c:75–76) compute the eccentricity vector as `(v²/μ − 1/r)r⃗ + (r·v/μ)v⃗`. The standard formula (BAC-CAB on `v⃗×h⃗/μ − r̂`) is **minus**: `(v²/μ − 1/r)r⃗ − (r·v/μ)v⃗`. Evidence:

- Pure Kepler, e=0.05, exact states from the code's own `orb_state`: the code's formula reads e ∈ [0.0487, 0.051944]; max 0.051944 is exactly the `none` config's "physics". Correct formula: 0.050000 constant.
- Round-trip `orb_state → rv2el → orb_state` on e=0.05: worst |Δr|=7.9×10⁻³, |Δv|=8.0×10⁻² (~10% of |v|), pericentre off by π at some phases; on e=0.20: |Δv|=3.3×10⁻¹. Correct formula: 10⁻¹⁵.
- Consequence: after **every** conjunction kick, `rv2el` misreads the post-kick state and the layer propagates a different orbit (wrong pericentre, wrong radial velocity). The rung's specified layer — "exact Kepler cycles between conjunctions, plus one analytic kick" — was not what ran. The kick kernel itself is correct: I verified analytically that the closed form is the exact l=2 and l=3 interior-perturber term of the disturbing function, and the selftest validates its (−∞,∞) Beta-integral against a trapezoid at 1.8×10⁻⁹.

### 3. Oracle values — clean-room RK4 (independent code, correct elements)

4800 and 9600 steps/orbit agree to 6 digits; dE/E ≤ 7×10⁻³.

| case | author truth max_e / C | RK4 truth max_e / C | sign-fixed Verlet |
|---|---|---|---|
| r21 | 0.0807 / 0.077 | **0.0760 / 0.493** | 0.0762 / 0.477 |
| r21b (w2=4) | 0.1830 / 0.067 | **0.1629 / 0.393** | 0.1627 / 0.379 |
| p5 | 0.0730 / 0.066 | 0.0726 / 0.032 | 0.0727 / 0.032 |
| p255 | 0.0728 / 0.055 | 0.0707 / 0.027 | 0.0707 / 0.027 |
| p215 | 0.0715 / 0.055 | 0.0684 / 0.011 | 0.0684 / 0.011 |

The truth *integration* (Verlet, 600/1200/2400, converged <0.5%) is sound; its *measurement* was sign-broken: max_e inflated 6–12% on resonant cases, ϖ₁ scrambled, libration destroyed.

### 4. Adversarial cases

1. **Sign-fixed re-run** (only change: two signs): metrics become conj-quad {1.961, 8.910, 0.766, 0, 0, 0.583}, conj-oct {5.713, 12.155, 0.079, 0, 0, 0.583}, averaged {0.474, 0.770, 0.116, 0.667, 0, 0.583}, none {0.307, 0.657, 2.076, 0, 0, 0}. `verdict.py`: **still KILL** (conj-quad fails pumphi/lib/ctrl; conj-oct fails pumphi/lib/ctrl; both negatives still fail). The verdict is robust; the dossier's numbers are not. Notably the fixed controls **damp** e (p5: 0.05 → 0.0024 min) instead of over-pumping 8–35× — the failure mode the author described for controls is an artifact.
2. **Phase scan** (RK4, 2:1, w2 = 0…6): C = 0.49, **0.92**, 0.09, 0.33, 0.39, 0.42, 0.56. At w2 = 1.0 the truth has C = 0.916 — essentially the red-team's 0.867 anchor. The author's headline "no librating resonant angle in any of the grids I searched" and "the lib criterion then compares circulation vs circulation" are measurement artifacts: the author's own chosen cases librate at C ≈ 0.49/0.39. The rung's lib criterion discriminated all along.
3. **Round-trip control** (§2) — the cheapest falsifying test, absent from the author's run: a pure-Kepler state must read back exactly.

### 5. Rung compliance

Configs and negatives as frozen; `lab/rungs/r4-resonance.md` matches the prompt's blocks; 200 synodic periods per case; truth converged 600/1200/2400 (<0.5% from 1200→2400); dense_steps = 0 is factual (the only quadrature is inside the analytic kick; the trapezoid lives in `--selftest` only); kicks_per_orbit median 0.41 (formula verified: events × (Prat−1)/(Prat·200)). The scene (pumped body exterior, perturber interior, λ₂(0)=π+w₂) is the author's reconstruction, frozen in `predictions.md` before any run; `e1_resonance.py` is indeed absent from this checkout, so the red-team's exact scene is unknowable here — but the anchor is *approximately* reachable (w2=1.0 → 0.92), so "not reproducible from the rung text" was the bug talking, not the rung.

### 6. Novelty

No prior test of resonance behaviour in `docs/HISTORY.md` or the docs. H0190's K1/K2 measured kick *rates* (32.5/orbit; 114× averaging cut), not mean-motion-resonance response; the red-team entry in the taste log named this exact experiment as the gold-maker. The KILL is new information for board bottleneck #2's "analytic generators + multipole kicks" path.

### 7. Goal fit

Moves board #2 and respects PRINCIPLES. "A failed experiment kills that configuration, never the method" (#9): the killed configuration — full-synodic-window straight-line impulse — is genuinely dead under *both* the buggy and corrected bookkeeping (over-pump 2.0–8.9× quad, 5.7–12.2× oct, controls damp). "Compute only surprises" (#3) survives: 0 dense steps, ~0.5 kicks/orbit against 3.8×10⁴–7.6×10⁴ truth steps. Caveat for adoption: the run cannot cleanly attribute the over-pump to the kernel, because the layer also omits all l≤1 terms of an interior perturber (documented choice) — the next rung must separate kernel width from monopole/dipole omission *and* carry a round-trip control.

### 8. What the author missed

- The `none` control **failed and was not read**: a no-op config reporting max_e ≠ e₁₀ on pure Kepler is a red flag the dossier walked past. "A test that cannot fail is a control" — this one failed and was treated as physics.
- The scene-search instrument (truth C) shared the same broken ϖ code as the law: instrument correlated with the system under test; ~450 scenes were searched with a broken thermometer.
- `r4.c` header comment contradicts the code ("outer perturber … inner test particle" vs interior perturber at a₂=1, exterior pumped body) — stale scene description, a misreading hazard for the corporal.
- No quantitative check that "oct halves the error" was kernel physics rather than bookkeeping error; it was bookkeeping.
- The picture and `data/*.csv` carry the sign-broken measurements; they should not be quoted as truth values.

**Bottom line.** Verdict: KILL, undisputed, and robust to the bug — but the run measured the author's broken bookkeeping, not the rung's layer. The next rung reruns r4 with the two-character fix, a Kepler round-trip control, the l≤1 terms assigned somewhere explicit, and the red-team scene at w₂ ≈ 1.0 (C ≈ 0.92) as the resonant case.
