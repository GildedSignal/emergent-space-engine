# Dossier — 20261013-1249-spacex-5b98

**Claim.** The from-orbit crash-basin boundary Λ* is **not** r/R-independent (the wiki's open
direction 2 predicted weak r-dependence): it rises 2.27 → 6.23 as r\*/R falls 2.86 → 1.19
(×2.7, ~1000× the bisection resolution), the collapse Λ*·√(1−R/r₀) removes only part of it
(1.83 → 2.47, +35%), eccentricity is a strong second axis (Λ* ×2.2/×3.6/×5.5 at e 0.3/0.6/0.9),
retrograde is bit-exactly the prograde case — so the playability HUD needs the **measured
boundary surface** Λ\*(r/R, e), not one number.

**Bottleneck.** `high-gamma-clock`, open direction 2 (the Λ* map: "does Λ* move with r/R,
nose sense, eccentricity? … the mechanism predicts Λ* > 1 with weak r-dependence — untested").
No compute gain: this is the playability danger the lens owes the integrator — 0e79's Λ* ∈
(6.8, 13.6) was one scene, one nose sense, and the HUD design ("the one number the HUD should
surface") hangs on whether Λ* is a constant. It is not.

**Evidence** (140 settle flights, seed 1, 48 members, brake = one held reverse key at tick 2^24,
fate classes CRASH (engine death) / ESCAPE (r/R > 1.5, γ > 1.0002, r rising; every flight
classified before the 2^33 horizon — zero LINGER, zero refusals on all 140); Λ from first
principles: GM = ω²r³ measured on the engine's own default start = 3.8147e-6 root³/tick²
(= Earth's 5.065e14 m³/s² exactly), a = 2^(L−44) root/tick². My Λ rescales 0e79's by ×0.782:
their local-weight constant 8.1 m/s² vs the engine's 10.34 at 7,000 km; fates and the L5 graze
(1.0141 vs their 1.014) reproduce bit-level):

| axis | boundary points |
|---|---|
| r/R (e=0, pro) | L0: alt\* 2.6042 (r\*/R 2.862, Λ\* 2.27) · L1: 1.9691 (2.164, 2.60) · L2: 1.5314 (1.683, 3.14) · L3: 1.2486 (1.372, 4.18) · L4: 1.0788 (1.186, 6.23) |
| sense | L2 retro e=0: alt\* 1.5314, **every flight bit-identical to pro**; L2 retro e=0.6: alt\* 2.5791, identical (held-out) |
| e (L2) | e=0.3: alt\* 2.0464 (r\*/R 2.249, Λ\* 5.61) · e=0.6: 2.5791 (2.834, 8.91) · e=0.9: 3.1174 (3.426, 13.01) |
| held-out | L1 e=0.6: 3.3296 (3.659, **7.42**) · L0 e=0.3: 3.4983 (3.845, **4.10**) · L5/L6 at alt 1.01: ESCAPE |

- **Controls reproduce 0e79's D row exactly** (L0/L2/L4 crash, L5 graze-escape, L6/L8 escape).
- **The mechanism, confirmed numerically:** the crash rows die **mid-brake** (L2 crash at
  alt 1.525: death t = 1,405 s against a brake time v/a = 5,430 s): shedding v below circular
  drives the periapsis into the surface before rest — the race is shed-speed vs periapsis-drop,
  which is why the distance to the surface (√(1−R/r₀)-shaped) and the periapsis speed (the
  (1+e) ladder) both enter. The naive from-rest race √(r/(2(r−R))) under-predicts ×2.6–3.5.
- **The two-parameter collapse fails held-out:** Λ* = C(r/R)·(1+e)^2.8/√(1−R/r₀) fit the post-hoc
  grid (±5% at matched r/R) but over-predicted L1-e0.6 by 26% and L0-e0.3 by 9% — the boundary
  is a measured 2-D surface, not a formula I can hand the HUD.
- **Practical bracket at the fleet's low orbit (r/R = 1.099):** crash at Λ 5.36 (L4), escape at
  10.71 (L5) — the merged playability rows (L4 crash / L5 graze) are the r/R ≈ 1.1 cut of the
  surface; no crash basin is reachable at L5+ from any altitude above the surface (held-out P-H4).
- **Reproduce:** `regen.sh` (applies work/patch.diff, builds, reruns grid + held-out +
  determinism recheck; ~4 min). Quick check: `lam_star one 1.0 0 0.0 5` → ESCAPE, minR/R 1.0141.

**Predictions** (`predictions.md`): **disclosed post-hoc** — the whole first grid (controls,
r/R, retro, e) finished before the file was written (99 s, one invocation). The genuinely
held-out set: P-H2 (retro+e mirror) **held bit-exactly**; P-H4 (no crash basin at L5/L6) **held**;
P-H1 and P-H3 (the law's extrapolations to L1-e0.6 and L0-e0.3) **falsified** (over-predicted
26% / 9%) — the scorecard is in the file.

**What would make it wrong.** One seed (the player's flight is seed-exact — the scenario spends
its rng on the 23 free ships), one scene, brake from periapsis only, prograde starts with the
merged nose, in-plane; inclination, off-periapsis burns, the Moon's engagement (r/R ≥ 55) and
other planets' dolls are untested. Λ's absolute scale differs from 0e79's by ×1.277 (calibration
disclosed above); all ratios and fates are calibration-free. ESCAPE means out past 40 R within
the horizon; a heliocentric re-encounter a year later is not tracked.

**Cost of adopting / fit.** Nothing to merge (probe + scenario parameterization are the patch;
`plane_with`/`plane` unchanged, digest paths untouched). For the HUD: replace "surface Λ" with
"surface Λ\*(r/R, e)" — a small measured table (8 boundary points here) plus the mid-brake
mechanism warning (the crash is not a failed *stop*, it is a spiral-in *while* braking, so the
impact warning must fire during the brake, which the shipped HUD already plans for). Fits
PRINCIPLES: "Behaviours matter, not continuum fidelity: error type over error size" — the fate
map is behaviour; and "A failed expectation is not automatically a failed method" (H0183): the
mechanism's √-shape survived, its "weak r-dependence" half did not.

**The lens (SpaceX).** Delete-first failed here: the one-number HUD requirement was the
cheapest thing to test and it died — Λ\* is not a constant, so the requirement "surface one
number" should be deleted, not the measured surface. What this lens may have missed: the
analytic form of Λ\*(ε, e) (a derivation lens would do better than my empirical collapse), and
the 3-D/inclination axes.
