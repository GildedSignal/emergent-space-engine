# Dossier — 20261011-0614-redteam-a616 (lens: premise red-team)

## Claim

The design's view gather cannot discover lensed images: around a black hole every background star's image set changes twice per orbit (a photon-ring image is born and dies at the shadow rim, at every radius measured from 6.5M to 40M), and the stated mechanism — "each tube crosses the past light cone once; Newton from the previous frame" — misses 100% of newborn images even when granted a perfect ray oracle and full seeding; no rung gates it, because r6 is named in the falsifier ladder but was never frozen.

## Bottleneck

Not on the board's list: this is a premise of `docs/representation.md` §2 (the view is an instrument, principle 28), aimed at the game's marquee experience (black holes and high-c travel are in the goal). The gain is not compute: it is correctness of the one surface the player stares at, plus the unfreezing of r6 before the view gets built wrong. What it lets us delete: nothing; what it prevents: building the per-tube gather without an enumeration rule and freezing r6 without a multiplicity criterion.

## Evidence

All numbers from `python3 falsifier.py` (7 s, float64, numpy 1.26.4, Linux cloud — orders of magnitude only), in this folder; raw JSON in `falsifier-results.json`, per-frame table for r_o=10M in `evidence-r10-perframe.txt`.

**Instrument controls (all pass):** flat-space initial-condition mapping reproduces straight-line exit angles to 6×10⁻⁸ rad; deflection at b=20M is 0.2091 rad (expected 4/b + (15π/4)/b² = 0.20–0.24); the photon capture threshold at b = 3√3 is exact on both sides; halving the step changes Φ by ≤ 2.5×10⁻⁶ rad.

**Scene:** Schwarzschild M=1, planar (the game plane); one static star at r=500M; observer on a circular orbit at r_o ∈ {6.5, 10, 20, 40} M; one orbit, 32 frames; emission circle scanned at 0.1°; winding capped at 4π (images of order ≥ 2 are e⁻²π ≈ 1/535 dimmer — sub-threshold). Truth = brute force over the whole emission circle each frame. Tracker = the design's mechanism, made as generous as possible: seeded at frame 0 with **all** true images, Newton on the crossing evaluated against the current frame's own perfect Φ(α) table, continuity-tracked directions, deaths handled cleanly by Newton failure.

| r_o | images (min–max) | set changes / orbit | frames wrong | missed image b (min/med/max) | missed distance to rim (median) |
|---|---|---|---|---|---|
| 6.5M | 2–3 | 2 | 12/31 (39%) | 5.20 / 5.21 / 5.25 | 0.17° |
| 10M | 2–3 | 2 | 11/31 (35%) | 5.21 / 5.22 / 5.27 | 0.16° |
| 20M | 2–3 | 2 | 7/31 (23%) | 5.23 / 5.25 / 5.29 | 0.16° |
| 40M | 2–3 | 2 | 4/31 (13%) | 5.26 / 5.29 / 5.31 | 0.13° |

Critical impact parameter b_c = 3√3 = 5.196: **every missed image is born within 0.12 of b_c and within 0.2° of the shadow rim.** Zero ghosts, zero collapsed tracks, zero losses of surviving images: the tracker is perfect except that it cannot find a crossing it was not told about. The lifecycle at r_o=10 (`evidence-r10-perframe.txt`): the winding image at 208° slides into the shadow and dies between frames 11→12; a fresh one is born at 152.2° (b=5.207) at frame 21 and stays unrendered through the end of the orbit — nothing re-seeds it, ever. With a field of stars behind the hole (the real sky), each star has its own birth/death schedule, so rim births happen every frame; the photon-ring band is systematically under-populated. Individual winding images are demagnified ~e⁻²π (standard result, not measured here), so the visible damage concentrates in the ring band — the iconic region — and in bright transients (flares, beacons) behind the hole.

**The premise that survives (reported as alive):** the flat-space core. Observer thrusting with rapidity 1.5→3.5 (β 0.905→0.998) over 2 s past 200 drifting emitters: Newton from the previous frame converges in ≤ 3 iterations, 0 failures, 0 wrong roots (f(τ) is monotone). High c does not break the gather; lensing multiplicity does.

**The doc check (measured):** representation.md §1 still presents the Minsky band-tangent Binet cell as "the primary in-cell solution". Closed form: a circular orbit at band offset δ precesses by 2π(1/√(1−6M·u_k)−1) instead of 2π(1/√(1−6M·u)−1), a sawtooth of **−2.6% … +2.6% at m=16** over p ∈ [20, 80] (weak-field limit ±ln2/(2m) ≈ ±2.2%), independent of field strength; in-band spot checks confirm the orbit stays in one band (oscillation ≤ 0.2% of band width) so the closed form is the actual error of the stated mechanism. law.md already killed this configuration on 30 September ("band-centre tangents carried a first-order slope error in every cell holding a turning point"; the viewer found near-circular precession 1–7% off) and replaced it with `space-darwin16-v1` (error ~10⁻⁶). The law is healthy; the design doc teaches the corpse as the primary.

## Predictions

`predictions.md` was written before the run. P2 hit (all missed images b ∈ (b_c, b_c+1); measured even tighter: b_c+0.12, rim distance ≤0.2°). P3 hit where it applied (39%/35% of frames wrong at 6.5M/10M ≥ 30%; ≥1 unrecovered birth per orbit at every radius). P4 hit exactly (3 iterations, 0 wrong). P5 hit (±2.6% sawtooth, spots agree). **P1 missed twice, both times in the direction of more prevalence, not less:** events per orbit are exactly 2 at every radius (I predicted ≥4 at 6.5M, and 0 at 40M); the photon-ring image is born and dies once per orbit per star regardless of distance from 6.5M out to 40M and beyond — the effect does not fade with radius, only the phase fraction during which the image exists shrinks (39%→13%).

## What would make it wrong, cost of adoption, fit

**Wrong if:** the intended mechanism for "lensing adds crossings" is per-pixel ray casting of the rim band (Wolfenstein's observer rays are cited in §5), which finds images for free — then the attack reduces to: the stated per-tube Newton is the wrong mechanism for lensed directions, and the doc must say which regime uses which. My falsifier cannot read intent; it proves the stated mechanism fails. It would also be wrong if winding-1 images were ruled beneath the brightness floor the game sets — that is a Julien decision, not a derivation; the photon ring's integrated flux (many stars) is the counter-argument.

**Cost of adoption:** a view-layer fix, no law change: for each doll whose rim band is on screen, spawn candidate roots in the rim annulus (or ray-cast it), at a cost bounded by the design's own "≤ 1 sample per pixel per frame" cap. Plus freezing r6 with an image-multiplicity criterion: all images above a brightness floor found per frame versus a brute-force truth, for an observer orbiting at 6.5–40M. Adoptable in one step.

**Fit with PRINCIPLES:** principle 2, "Behaviours matter, not continuum fidelity: error type over error size" — a missing image is a behaviour error, not a rounding one. Principle 28: "The view is an instrument… your dials are made up and hold no informations" — an instrument that drops real images holds wrong information. Principle 21: "Rough first, refine when a certificate could break" — there is today no certificate on image multiplicity that could break. Principle 18: the right question for the gather is not "how many Newton iterations" (r6's named metric) but "which crossings exist".

## Ranked attacks (the lens's deliverable), with the rung that should have caught each

1. **View gather cannot enumerate lensed crossings (premise 5) — confirmed by the falsifier above.** Rung that should catch it: r6, named in representation.md §7 and law.md's build list, **does not exist in lab/rungs/**; and as named ("Newton iterations and samples per frame") it would not catch a wrong image set even if run. Needed: a multiplicity criterion.
2. **The design doc's stated primary in-cell solution is the configuration its own law killed (premise 2 as written).** Measured ±2.6% banding at m=16; law.md's Darwin compile replaced it. Rung: r1 caught it (precession, cycle repetition); the doc was never updated — a "text has a cost" violation, one paragraph to fix.
3. **Two of the six premises in my brief are ungated: r5 (dense order bit-identity) and r6 (view) have no rung files**, though representation.md §7 claims "kill criteria are frozen in lab/rungs/" and law.md assigns both to GLM. For r5 there is also a representation-level risk to gate: the sparse order works in doll coordinates, the dense in Fermi normal coordinates (law.md), on different quantization grids — identical bits require that broad-phase detection only ever produces false candidates, never misses, in both grids. No rung tests it.
4. **Two-body doll at strong field (premise 1): not falsified, analytic note only.** The 1PN ν-only-in-energy map errs at O(ν(M/p)²); B11's oracle slack (1% + 16/p) absorbs it at p ≥ 20; below p ≈ 20 with comparable masses nothing gates it (r3 v3 tested p 20–1000). Player exposure is binary black holes near merger; ships are ν ≈ 0 test bodies. A rung would be an r3 extension at p ∈ [10, 20], ν ∈ {0.1, 0.25}, against a 2PN oracle — worth it only if comparable-mass close binaries enter the game.
5. **Kicks and cycle derivatives (premise 3): alive as redesigned** (r4/r9 killed the bad variants; jet + re-anchor adopted, one-checker gold, second check pending). Open edge for that second check: ∂(cycle time)/∂E diverges logarithmically as e→1, so the multiply-add cycle update is worst exactly on flyby-born orbits; the re-anchor certificate should carry e.
6. **Costs ≈ 0 for undisturbed bodies (premise 6): alive** (compiled cycles are additions; kick rates measured in H0190; my P4 confirms the gather's flat core at β→0.998). The unmeasured multiplier is image count per tube per intervening doll — bounded by the pixel cap only once the enumeration of attack 1 exists.

## The lens (what this red-team may have missed)

Red-teams overweight exotic cases; I ranked by player likelihood, but the star of this dossier is still a black-hole close orbit, not the everyday system view. The planar idealisation (one star, one BH, circular observer, static star, 0.1° grid, winding ≥ 2 excluded) means event counts are lower bounds; a 3D sky with proper aberration, elliptical orbits and many dolls has more birth channels, not fewer. I did not measure magnification (the e⁻²π demagnification is textbook, not mine), did not test the moving-lens interplay with image multiplicity (B16 gates deflection only), and did not touch premise 4 beyond the analytic note — testing dense/sparse bit-identity needs the real crates, which exceeded this window. The strongest counter-argument to the whole dossier is intent: if the rim band was always meant to be ray-cast per pixel, the design is right and its text is wrong; either way the text and r6 must change.
