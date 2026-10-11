# Predictions (held out before the decisive run)

Run: 20261011-0614-redteam-a616, lens: premise red-team.
Decisive experiment: `falsifier.py` (float64, ≤ 60 s target) — the view gather
(representation.md §2, "Observables are emergent" / "Light is gathered at the
observer") around a Schwarzschild black hole, where the design sends the player
("feel what living at high c would feel like"; BHs are in the goal).

Scene: planar Schwarzschild M=1; one static star at r=500M, φ=0; the observer
on a circular orbit at r_o ∈ {6.5, 10, 20, 40}; one full orbit per radius,
32 frames per orbit; rays sampled at 0.1° of emission angle; winding capped at
4π (images of order ≥ 2 are e^{−2π} ≈ 1/535 dimmer, sub-threshold).
Truth = brute-force scan of the whole emission circle each frame.
Design mechanism = per-image Newton from the previous frame's root, seeded at
frame 0 with **all** true images (more generous than the design, which
specifies no seeding of lensing-added crossings at all).

## P1 — image count is not constant (caustic events)

The number of crossings of one star's tube with the observer's past light cone
changes as the observer orbits. Predicted caustic events per orbit:
- r_o = 6.5M: ≥ 4
- r_o = 10M: ≥ 2
- r_o = 20M: ≥ 1
- r_o = 40M: 0 (only the two persistent primary images; the premise holds far out)

If the count never changes at any radius, premise 5's "once + Newton" core
survives and this attack is downgraded to a documentation gap.

## P2 — the changing images are near-critical rays

Every created/destroyed image has |b| ∈ (3√3, 3√3 + 1) M (winding-1 relativistic
images hugging the shadow edge), not the two primary images.

## P3 — previous-frame Newton tracking loses images

Seeded with all images at frame 0, the tracker undercounts (true count >
tracked count) in:
- ≥ 30% of frames at r_o = 6.5M and 10M
- ≥ 1 loss event per orbit at every radius that shows events (P1)

Missed images are never recovered (no enumeration mechanism exists), so a loss
persists for the rest of the orbit. The missed images sit within ~2° of the
shadow edge — where the player is looking.

## P4 — the flat-space core survives (premise worth reporting as alive)

Flat space, observer thrusting with rapidity 1.5 → 3.5 (β 0.905 → 0.998) over
2 s, 200 inertially drifting emitters, Newton on the emission-time crossing
from the previous frame: converges in ≤ 6 iterations for 100% of star-frames,
zero wrong roots (f is monotone in τ). High β alone does not break the gather;
the break is lensing multiplicity.

## P5 — doc consistency (analytic, no tuning possible)

representation.md §1 still states the Minsky band-tangent Binet cell as "the
primary in-cell solution". For a circular orbit at band offset δ the band
precession is exactly 2π(1/√(1−6M·u_k) − 1) vs GR's 2π(1/√(1−6M·u) − 1):
relative error → δ as M·u → 0, i.e. a sawtooth of ±(2^{1/(2m)} − 1) ≈ ±2.16%
at m = 16, independent of field strength. law.md already records this
configuration as killed (30 September: "band-centre tangents carried a
first-order slope error in every cell holding a turning point"; viewer found
near-circular precession 1–7% off) and replaced by `space-darwin16-v1`.
Prediction: the closed-form sweep reproduces the ±2.16% banding, and 3 spot
integrations of the band equation agree with the closed form to < 5%.
