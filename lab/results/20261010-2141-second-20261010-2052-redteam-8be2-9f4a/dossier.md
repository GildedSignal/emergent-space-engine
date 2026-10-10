# Dossier — second author on 20261010-2052-redteam-8be2 (run 20261010-2141-...-9f4a)

**Claim.** The original run's claim **holds, strengthened, and its last open branch
closes**: the view premise is sound for static spherical dolls (regenerated
bit-identically, ≤ 0.6%) but broken as specified — and with checker 2's corrected
Kerr root the rotation kill is **3.31×, not 2.37×** (b_retro = 6.138/6.832/6.997 M
at χ = 0.5/0.9/0.998, verified a double root of R to 6·10⁻¹⁴, limits a→1 = +2/−7,
and internally consistent with α(−6 M) = capture) — while the **winding images
the scalar memo cannot place turn out invisible**: at every scene the game
promises they are ≤ 0.084 % of the brightest image's flux (7.7–9.8 mag fainter),
so the missing-image branch of P2 is harmless in practice, and the two-sense key
+ delay(b) proposal is adoptable verbatim. Bonus, unmeasured before: the exact
map breaks the geometric sum rule Σμ = 1 by 0.5 % → 8 % → 24 % → 36 % as the
observer descends 5000 → 50 → 10 → 6 M — a brightness defect of the same family,
10× the composition error at 10 M.

## Bottleneck

Checker 2's named experiment to gold, done. Same bottleneck as the original
(principle 30/28: navigation and knowledge are the player's only instrument):
prevent a wrong view memo from being built and frozen. Cost of adoption
unchanged: one design-doc edit (key (b, sense|Q) + delay(b)) plus the corrected
retrograde table in the record; the magnification result *removes* a would-have-
been requirement (placing winding images) — the cheapest component is no
component.

## Evidence (float64, equatorial, M = G = c = 1; total runtime 10 s)

Record regenerates from shipped code in this folder:

```
cd lab/results/20261010-2141-second-20261010-2052-redteam-8be2-9f4a/work
python3 falsifier2.py > out2-repro.json   # 5 s: bit-identical to the run's out2.json
python3 falsifier3.py > out3.json         # 5 s: the one fix + verification block
python3 magnify.py      > magnify.json    # 4 s: winding magnification + controls
```

`out3.json` differs from `out2.json` in the Kerr block only — every
Schwarzschild scene, P4, the negative control and the selfcheck are
bit-identical, so the record carries the corrected table by construction.

**Corrected retrograde root (checker 2's numbers, replicated, plus my checks):**
b_retro = 6.1382/6.8323/6.9967, ratios 1.4985/2.4021/**3.3146** (checker 1's
"2.41" at χ=0.9 is a rounding slip; 6.8323/2.8444 = 2.402). R = 0 **and**
dR/dr = 0 to ≤ 6·10⁻¹⁴ on the chosen branch at every a (analytic R′; my first
attempt used a finite difference below R's float ulp and a wrongly-signed
rejected branch — both caught and fixed); the rejected root of R = 0 has
dR/dr = 0.4–190 (not circular); a → 1 gives +2.000077/−7.000000; a = 0 gives
±3√3 (degenerate — both branches coincide, the control the author over-trusted);
|b_retro|/b_crit = 1.18–1.35 ≥ 1 and b_crit/b_pro = 1.27–2.60 ≥ 1; and
kerr_alpha(−6, 0.9) = capture while α(−7) = 2.5893 — the original record's own
contradiction, now consistent.

**Winding magnification (the held-out part).** μ = (sin ψ / sin β)·(dψ/dβ) per
branch (family × winding k) by chain rule on the original's oracle. Controls:
primary matches the textbook point-lens μ₊ to 0.09–0.21 % at the weak scene
(u = 0.28–2.76); chain-rule μ matches direct finite differences of the image
position to ≤ 1.5 % (and the sums to 6 decimals at two step sizes); the image
inventory is complete — the outgoing launch branch (ψ > 90°) can sweep at most
75–105°, below the 140° minimum source azimuth, and higher windings are
geometrically suppressed (k=2/k=1 ≈ 1.5·10⁻³).

| scene (r_o/r_s) | brightest k=0 μ (off 0.5°) | max single winding ÷ brightest | winding pair share of total flux |
|---|---|---|---|
| weak 5000/20000 | 2.36 | ~0 (textbook regime) | ~0 |
| mid 50/200 | 17.8 | **1.2·10⁻⁴** (9.8 mag) | 1.2·10⁻⁴ |
| near 10/50 | 32.0 | **8.4·10⁻⁴** (7.7 mag) | 8.4·10⁻⁴ |
| deep 6/30 (adversarial) | 34.2 | **1.4·10⁻³** (7.2 mag) | 1.4·10⁻³ |

Nearly offset-independent from 0.02° to ~5° (every image's μ ∝ 1/β near
alignment), falling slowly to 40°. Per-winding suppression = (0.06–0.75)·e⁻²π
across scenes — the strong-deflection order (Bozza). The winding images hug the
shadow edge (27.715° vs shadow 27.695° at 10 M; 45.02° vs 45.00° at 6 M).

**Sum-rule deficit (new).** Σ signed μ over all images = 0.999/0.918/0.755/0.640
at weak/mid/near/deep — the geometric sum rule fails for the exact black-hole
map (its domain excludes the shadow), monotonically in compactness. Cross-check:
Σcosψ_i − cosβ is constant to 10⁻⁵ where Σμ is constant in β, exactly the
integral the deficit predicts. Interpretation for the view (flagged, not gated):
a composition that normalizes total brightness thin-lens-style overrenders by
1/(1−deficit) — 1.3× at 10 M, 1.6× at 6 M.

## Predictions

[predictions.md](../predictions.md) written 21:45, before falsifier3.py (21:53)
and magnify.py (22:00). Outcomes. Replication R1–R4: all held (R1 after two
bugs in my *verification code* — a finite difference below float ulp and a
wrongly-signed rejected branch — were caught by their own controls). Held-out:
M1's textbook control held (0.2 %); M1's Σμ ≈ 1 clause **failed** at strong
scenes (0.64–0.92) — root-caused above to real physics, not apparatus, via
three independent checks; M2 held at the bottom edge (predicted 0.1–5 % at the
near scene, measured 0.084 %); M3 **failed** (mid predicted 0.1–3 %, measured
0.012 % — I overestimated by ~10×); M4 half-held (deep is the largest, ✓, but
0.14 % < the predicted 0.5 %); M5 held. Net: my e⁻²π prior had the right shape
and the wrong prefactors.

## What would make it wrong

The magnifications rest on the original's quadrature oracle (independently
verified by both checkers and re-verified here against the textbook lens at
0.2 %); the winding μ share the validated code path, but their absolute scale
has no independent oracle — if they are wrong it is by the same factor as the
primaries, which the textbook control bounds at ~0.2 %. The visibility verdict
uses a flux-ratio threshold (0.1 %/1 %) chosen in predictions.md; a game could
choose otherwise, but 7+ magnitudes is beyond any display dynamic range. The
retrograde fix is closed-form and quadruple-verified; nothing observational
rests on it. The sum-rule deficit's *interpretation* (overrendering) assumes the
view normalizes thin-lens-style; if it never renders brightness, the deficit is
physics trivia, not a defect.

## Fit with PRINCIPLES

"The right representation always just feels right … like cutting butter" (19):
the corrected key is one bit, and now the winding branch it cannot place is
measured harmless — the fix is smaller than feared. "A game is an illusion
spectacle" (34): the oracle guards the view; here the guard says the missing
images are below the spectacle's floor. "Measure before claiming" (10): the
author argued visibility, the checkers demanded the measurement, and the
measurement sides with the author's design. "the biggest quantization we can
get away with" (16): flux ratios of 10⁻³ are the view's own quantum.

## The lens

A second author inherits the checkers' frame: I spent my adversarial budget on
the instrument (sum rule, outgoing branch, direct differences) rather than on
new scenes, and both bugs I found were in my own verification code — the
original's physics needed none. What this lens may miss: everything stays
single-lens, equatorial, geometric μ only — beaming ((g)⁴, the k⁴ the dossier
speculated) and multi-doll composition remain unmeasured, and the sum-rule
deficit is one measurement old, not a gated claim.
