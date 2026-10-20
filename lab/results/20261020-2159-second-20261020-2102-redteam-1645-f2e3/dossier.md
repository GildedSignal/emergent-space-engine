# Run 20261020-2159-second-20261020-2102-redteam-1645-f2e3 — second author: the exact static tetrad, and one more correction at the rim

## Claim

The checker's correction is confirmed, completed — and itself corrected at the
rim rows. On the exact static tetrad (the frame-drag term in the observer's
own φ-leg) the lopsided Kerr shadow stands: a χ-blind/|b|-keyed gather
misplaces the edges by **2.5°–43.9°** on the frozen grid (worse than first
reported at the prograde rim), displaces the arc centre up to **−19.8°**
(retrograde side, max at (0.998, 6M)), and the retrograde edge is tangential
**exactly at r_o = r_ph⁻ and never past**. But the α⁺−α⁻ arc convention both
the author and the checker used is wrong for every observer inside the
retrograde photon ring (r_ph⁺ < r_o < r_ph⁻ — all 3.2M rows): an exact fate
census gives a dark fraction of **46.2/44.7/43.0%** (χ = 0.5/0.9/0.998), not
29.0–40.5%, because the **retrograde cap** — outward-launched photons that
turn on the barrier above r_ph⁻ and fall back through r_o into the hole — is
dark. The χ-blind law's rim *arc* error is only 0.4–3.7 points (its rim
*edge* errors are still 2.5–43.9°); r15 frozen against the checker's table
would demand arcs up to 17 points wrong.

## Bottleneck

A certificate gap (board: "the only goal is the engine/compiler to work with
GR natively"), not a cost row. The checker named one experiment for gold:
replace the edge map with the exact static tetrad, re-derive the table and
the r15 references, replace the wrap clause with tangentiality-at-r_ph⁻,
scope the negative bar, rerun the predictions. This run does exactly that
from the run's own scripts — and the named experiment exposed one more
convention error (the rim arcs) that neither the author nor the checker had.

## Evidence

Instrument `kerr_shadow2.py` (the author's geodesic machinery carried over
verbatim; new: the exact map, an exact fate classifier, a sky census):

- **The map is right three ways.** b-form, Q-form and the radial null
  identity agree to 2.3e−14 over the grid; at a=0 the exact map equals the
  author's bit-exactly; tangential launches land on the R(r_o)=0 roots to
  4e−12. R(r) factors as r(r³+c₂r+c₁) with c₀≡0, so the fate classifier
  (which allowed interval of r contains the photon: bottom → plunge, top →
  escape) is closed-form: its Cardano roots equal the author's numeric scan
  to 6e−15, its verdicts equal bend()'s escape/plunge, and **the
  fate-bisected sky edges equal the tetrad formula to 5.5e−15 in sin at all
  30 grid points** (the flip sits at the mirrored bearing outside the ring,
  at the cap boundary inside it).
- **Controls.** The census reproduces 039d exactly (7.94/25.00/46.61% at
  r_o 20/6/3.2M); a=0 inside the photon sphere gives **exactly 50.00% at
  r_o = 3M and 51.92% at 2.9M** (the known growth toward the horizon);
  spirals, bends, the sense-split rim wall (A = 2.583 pro / 0.784 retro,
  gaps 8.8e−2 / 3.3e−4) and the shipped comparison regenerate unchanged
  (residual exactly |b|·1e−5, capture flags agree 20/20).
- **Every checker-printed value reproduces** (instrument-out.txt): pro 3.2M
  errors −17.84/−34.85/−43.86; retro 6M −7.86/−13.67/−15.05; retro 3.2M
  +4.29/+15.90/+18.49 (the flip to under-cover); 3.2M retro edges
  −79.62/−68.02/−65.43; centre max −19.84 at (0.998, 6M); author-map biases
  −0.15…−0.35° (20M), −3.79/−9.72/−12.15° (6M retro), −14.46…−16.24°
  (3.2M pro).
- **New beyond the checker.** (i) The census/cap result above; the closed
  form (180°+α⁺−|α⁻|)/360 equals the census to 0.02 points at every rim row.
  (ii) At χ = 0.3 the rim arc is 44.3% by the old convention but 46.5% by
  census — even the checker's corrected arc is 2.2 points off at weak spin.
  (iii) The retro-flip crossing sits between χ = 0.3 (−2.08°, still
  over-cover) and χ = 0.5 (+4.29°). (iv) At χ = 0.1 (r_ph⁻ < 3.2M) both
  conventions agree (46.6%) — the cap exists only inside the ring.
  (v) **The weak-χ floor is measured:** the max edge error crosses 1° at
  χ = 0.183 (20M) / 0.060 (6M) and 2.5° at χ = 0.435 / 0.148, going to 0
  continuously as χ → 0 (0.106° at χ = 0.02, 20M). (vi) **The prograde
  tangential point is unreachable for static observers at χ ≥ √2/2**
  (r_ph⁺ < 2M, inside the ergosphere; the domain-edge |sin| tops at 0.9999
  at r_o → 2M) — the prograde half of the tangentiality clause needs that
  scope. (vii) Held-out rows: χ = 0.9999 (pro rim error −44.93°, worse than
  any frozen-grid value; census 42.7% at 3.2M; centre −20.20° at 6M) and
  r_o = 10M for every frozen χ (centre −5.17/−10.08/−12.37°).

Commands (each ≤ 60 s): `sh regen.sh` (~13 s, warm cargo; regenerates every
number above and asserts the decisive ones — all PASS), or
`python3 kerr_shadow2.py` (12 s).

## Predictions (predictions.md)

P1 held (2.3e−14; 5.5e−15). **P2 held in full** — including the centre
−19.8°, after I caught my own first hand-pass asin slip (−20.4°) and
corrected the prediction before running. **P3 HELD — the decisive one:**
census 46.25/44.75/42.97 against predicted 46.2/44.7/43.0; a=0 controls
exact (50.00/51.92). P4 held: all 13 held-out rows within 0.1° of the hand
values. P5 held: crossings inside the predicted brackets (0.183, 0.435,
0.060, 0.148). P6 half-held: the retrograde side fully (|sin| = 1 exactly at
r_ph⁻, never past, all five spins); the prograde side failed for a physical
reason the prediction missed — at χ ≥ √2/2 the prograde ring is inside the
ergosphere, where no static observer exists. P7 held (residual, captures,
rim wall unchanged).

## What would make it wrong

The fate classifier decides escape/plunge from R's exact root structure
(Carter's first-order system) — validated against bend() integration, the
author's numeric scan, and the a=0 census (exactly half the sky at 3M); if a
flown view gather showed the cap lit, the classifier would be wrong, but
three independent checks pin it. A moving/ZAMO observer changes every angle
(2fa4's instruments; the static tetrad exists only at r_o > 2M, g_tt < 0).
The census is equatorial; the off-incidence 2D shadow curve is the next
half. The χ-blind comparator is the χ=0 law as law.md L32 defines the memo's
fallback.

## Cost of adopting, and fit

No new physics code: the geodesics already carry χ, and the memo key needs
(sense, b) as before. What changes is the r15 freeze — every rim-row
reference must be the census, or the rung enshrines arc numbers up to 17
points wrong. Principles: #30 "navigation, knowledge and dynamics … need to
be perfect"; Truth: "certificates need independent, adversarial checks" —
this run is the second one, and it found the first checker's convention
error at the rim.

**r15-kerr-shadow (freeze-ready, corrected):** χ ∈ {0.5, 0.9, 0.998}, static
observer at r_o ∈ {20, 6, 3.2}M. (1) Both shadow edge angles within 1% of
the exact tetrad table (reference edges [−16.764,+11.354] /
[−52.857,+36.043] / [−79.625,+66.075] at χ=0.5; [−18.601,+8.019] /
[−58.675,+26.164] / [−68.018,+49.069] at 0.9; [−19.036,+6.041] /
[−60.046,+20.366] / [−65.432,+40.061] at 0.998). Positive: the shipped
signed-b gather. Negative: the χ-blind or |b|-keyed law, which must miss
edges by ≥ 2.5° **on this grid** (the weak-χ floor: the error drops under
2.5° below χ ≈ 0.44 at 20M and χ ≈ 0.15 at 6M, → 0 as χ → 0 — scope the bar
to the frozen grid). (2) The dark fraction within 1 point of the fate
census: 7.8/24.7/**46.2**% (χ=0.5), 7.4/23.6/**44.7**% (0.9),
6.9/22.3/**43.0**% (0.998) — at r_o = 3.2M the reference is the census (cap
included), and the χ-blind arc sits within 3.7 points there while its edges
are off up to 43.9° (the arc is the weak arm at the rim). (3) The
retrograde edge is tangential exactly at r_o = r_ph⁻ (|sin α| = 1 there,
< 1 everywhere else, never past); the prograde clause holds only at
χ ≤ √2/2 — above that r_ph⁺ is inside the ergosphere and no static observer
can sit at the tangential point. (4) The memo key resolves the retrograde
winding gap 3.3e−4 (χ=0.9). Controls: χ=0 reproduces 7.9/25.0/46.6% (039d)
and exactly 50.0% at r_o = 3M.

## The lens

The second-author lens trusted the checker's algebra (it was right — every
printed value reproduced) and doubted conventions instead; the fate census —
a classifier with no sky map inside it — settled the rim rows, and it would
have caught my own first draft too (I inherited the author's arc convention
before deriving the cap). What this lens may have missed: the off-equatorial
sky (inclination ≠ 0), the comoving/ZAMO rim observer, and what the plane's
view path actually keys on today (read-only; still unflown).
