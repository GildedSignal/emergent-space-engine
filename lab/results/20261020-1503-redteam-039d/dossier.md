# Dossier — 20261020-1503-redteam-039d: the chord occlusion law dies by type at every black hole

**Claim.** The letter's occlusion mechanism (L57's deflection gather × the per-row worldtube
chord predicate, 22d1's cure) is wrong **by type at every black hole, at every distance**:
the capture shadow is (3√3/2) = 2.598× the horizon silhouette in angular radius (a fixed
structural factor, not a size error), the chord test misses **100% of real eclipses** by
occluders near the hole (0.0% chord-blocked vs 6.9–11.9% truly eclipsed, deviation up to
9.3 M), and the naive-bearing composition fabricates far rows inside the shadow for
**66.7% of emitter azimuths at r_o = 6M and 100% at r_o ≤ 4M**. The cure is a **deletion**
(the horizon occludes nothing the gather serves: served rows have b > b_c by construction,
the shadow is emergent absence) plus occluder tests along the deflected path; the rim also
needs the deflection memo's b-key at 2⁻¹⁶–2⁻²⁰ relative resolution (a 12-bit key is
50–400× too coarse at r_o ≤ 6M). No rung sees any of it.

**Bottleneck.** View correctness (premise 5 of the lens's list; representation-premises
open direction 5, "strong-field occlusion near the photon sphere (e59e's rim domain) —
unmeasured"). Black holes are wanted gameplay ("I want black holes", CL 09-27); the player
flying within ~6M of one sees a third to half the sky mis-served. Nothing here is a cost
claim; it is a correctness-by-type claim (principle 13).

**Evidence** (float64, exact 2D Schwarzschild null geodesics: sin²u-substituted
Gauss–Legendre quadrature, per-branch bisection; `rim_occlusion.py`, 38 s, ≤ 60 s rule;
regen: `./regen.sh`, writes `results.json`):

- *Controls, both sides.* Shadow angle vs closed form sin α_sh = 3√3·√f_o/r_o:
  relerr 1.0e-9 / 1.3e-9 / 2.0e-9 / 6.4e-9 at r_o = 20/6/4/3.2 M. Weak-field half
  deflection at b = 10⁴M: 3.0e-4 rel (second-order term). turn(b_c⁺) = 3.0000024 M.
  Shadow fraction of the sky circle: 7.9% / 25.0% / 37.1% / 46.6% — the 6M value is
  e59e's "25% inside the shadow arc" reproduced exactly; the chord predicate (occluder
  radius 2M: horizon) blocks only 1.2% / 8.8% / 13.7% / 12.5% — it under-blocks by
  6.7 / 16.2 / 23.4 / 34.1 points of sky circle, and the factor is 2.598× in radius at
  **every** r_o, weak field included (7.9% vs 3.0% at 20M).
- *Channel 1, fabricated far rows (naive-bearing composition).* Fraction of emitter
  azimuths (r_e = 30M, 240 azimuths) whose flat row lands inside the capture shadow
  (b_flat < b_c): **16.7% at 20M, 66.7% at 6M, 100% at 4M and 3.2M**. The letter never
  names which frame occlusion is judged in; the flat option is dead everywhere near a hole.
- *Channel 2, missed eclipses (the shipped chord form, judged on the served row).* Observer
  at 6M, emitter at 30M at Φ = 2.6/2.9/3.1, primary image; occluder ring r_c = 5.5M,
  R_p = 0.2M, 1440 azimuths: **chord-ray blocks 0.0%; the true deflected path blocks
  11.9% / 8.8% / 6.9%**; max chord↔path separation 7.1 / 8.5 / 9.3 M. One-directional:
  near a hole the flat chord passes on the far side of the true path, so real eclipses are
  missed, never fabricated, at any occluder radius ≤ the deviation.
- *Channel 3, vanished near-side companions.* With the chord test applied to the direct
  row (r_e = 3.5M companion, r_o = 20M): 7.9% (R = 2M) / 11.3% (R = 3M) of the ring's
  azimuths lose their only visible image (direct row blocked, all others below the
  brightness floor). At r_o ≤ 6M the same cell reads 0.0 — **disclosed instrument limit**:
  the 1-D-map magnification (no sum rule) mis-picks the "best" image there; the geometric
  blocked window at 6M is Φ < 0.29 rad ≈ 9%, so the 0.0 is an under-count, not physics.
- *The rim wall.* Pixel placement (1e-3 rad) of the most sensitive visible image needs
  δb = 7.6e-6 (6M) … 3.2e-6 (3.2M) absolute = 1.2e-6–4.7e-6 relative; visible images sit
  0.029M from b_c at 3.2M (0.15M for the 3.5M companion at 20M); the ratio
  δb_1px/(b−b_c) = 1e-5–5e-5 (4–6M) to 1e-4–2e-4 (3.2M). A 12+12-bit memo key
  (2⁻¹² relative = 1.3e-3 absolute) is 50–400× too coarse; each wrap bunched
  exponentially (images within 0.6% of b_c at 3.2M).
- *Image counts.* 2–3 visible images per emitter (magnification window [1e-3, 1e3],
  k ≤ 3 solved): the k=0 pair is the visible set, windings excluded — consistent with
  6eae/8f00/9f4a; the companion ring at 3.5M shows 1.05–1.8.

**Predictions** (`predictions.md`, written before the run): P2 held in direction and was
**exceeded** (66.7%/100% vs the predicted 16%/34% — the correct emitter-level window is
b_flat < b_c, not the silhouette annulus); P4 half-held (measured 1.2e-6–4.7e-6 relative
vs predicted 1e-7–1e-9: the wall is coarser than guessed but still 50–400× past a 12-bit
key); P5 held (deletion cure: 0 misclassifications, by construction). **P1 and P3 did not
hold as written**: P1's close-r_o magnitudes read 0.0 (the magnification picker's weak
cell, disclosed above — the mechanism is measured at 20M); P3's "≥ 4 images" ignored that
only the k=0 pair clears a brightness floor (6eae counted raw solutions). Two of five
held, one exceeded, one half, two missed with causes named.

**What would make it wrong.** The truth is exact geodesics in the exterior of a static
Schwarzschild hole; Kerr dolls (the letter's rotating holes, B19) and a moving observer
(2fa4's instruments are exact, so aberration composes) are not flown here — both plausibly
widen the errors. The near-b_c GL accuracy degrades below b−b_c ≈ 1e-3 (the 1e-9 controls
bracket it); the magnification window [1e-3, 1e3] selects images, and a different window
moves Channel 3's numbers (not its sign). Occlusion of emitters by occluders is judged
geometrically (disc vs path); finite occluder worldtubes and retarded times (22d1's form)
only add the light-time offsets the chord already mishandles.

**Cost of adopting.** One deletion (no horizon occluder test — the shadow is the absence
of crossings; principle 1: the best part is no part) plus occluder rows tested against the
deflected path the gather already computes (the sweep is the same machinery as
deflection(b); ~300 path samples per row worst-case, cacheable per b-band). The memo's rim
clause: name the wrap cutoff with its b-resolution (2⁻¹⁶ at 6M, 2⁻²⁰ at 3.2M) or place
rim images by the closed form α(b_c) + exponential spacing. Fit with PRINCIPLES: "Nothing
bounces" already forbids the composer from paying per wrap; principle 2 ("error type over
error size") is exactly the chord law's failure; principle 34: the oracle (exact geodesics)
rejects what the player would see as wrong — here a third of the sky.

**Freeze-ready rung criterion (no rung sees this; verified: no file in lab/rungs/ names
occlusion, and r6/r11/r13 gate cost/aggregates, not the rim).**
`r14-rim-occlusion`: exact 2D Schwarzschild null geodesics (this run's instrument), static
observer r_o ∈ {20, 6, 4, 3.2}M, emitter rings r_e ∈ {30, 6.5, 3.5}M × 240 azimuths,
occluder ring (5.5M, R_p 0.2M) × 1440. **Candidate** (no horizon test + path-tested
occluders): misclassification 0 on all channels. **Negative** (the chord worldtube law):
must fail ≥ 3 channels — fabricated far rows ≥ 10% at r_o ≤ 4M, missed eclipses ≥ 5% at
6M, vanished near-side companions ≥ 2% at 20M; the 12-bit rim key must miss pixel
placement by ≥ 10× at r_o ≤ 6M. **Positive control**: the deletion cure reads 0 and the
shadow fraction matches 3√3·√f_o/πr_o to 1e-6.

**The lens.** The premise red-team's blind spot is exotic-case overweighting; I ranked by
player visibility and the winner is still the rim — but the honest limitation is the
opposite one this time: everything measured here is *static*, while the game's observer
flies (the comoving-occluder tail of direction 5 remains unmeasured). The magnification
picker's weak cell (Channel 3 at close r_o) is this instrument's own contribution to the
"agreement is not independence" ledger — a checker should re-derive with a 2-D flux model
before freezing Channel 3's constants.
