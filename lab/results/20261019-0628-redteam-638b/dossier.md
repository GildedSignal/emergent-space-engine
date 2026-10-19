# Dossier — 20261019-0628-redteam-638b

**Claim.** The view's strong-field half is unmeasured no longer: around a black hole —
the game's headline object — the letter's gather (one crossing per tube, Newton from the
previous frame, lensing as a scalar `deflection(b)` memo, `docs/representation.md` L57)
and the measured occlusion cure (22d1's per-row worldtube test, the r11 absence half)
fail by **type**, on four channels: the shadow (a scale-free 2.2–2.6× arc error, 14–25%
of the whole sky fabricated visible), the image census (every source has ≥3 images, 47%
with a >5% ghost, exactly 1 returned), the retarded times (+38–98 M on star rows, up to
16.8× on a beacon at 4 M), and the Newton seed's tangent (images move ≥10× the source
over a 90° rim band). No rung in `lab/rungs/` sees any of it. The shadow's cure is one
derivable line; the other three need the composed map the design's own memo already
feeds.

## Bottleneck

The board's "view" is the player's knowledge instrument and Julien's immersion goal
("I want the player to feel what a human would feel in space"). The page's census had
the strong-field tail explicitly unmeasured (representation-premises, open direction 4:
"strong-field occlusion near the photon sphere — unmeasured"). This run closes it and
moves the census's #2 item from "opacity half-measured" to a complete letter-amendment
with priced cures. Gain: not a 10× on a board number — a missing-behaviour find of the
class e59e/c78d (gold-blocking on the freeze, which this run pre-registers). What it
deletes: nothing yet; what it prevents: adopting 22d1's law as the absence half of the
eclipse rung without its strong-field arm, which would have frozen the 2.6× shadow error
into the law.

## Evidence

Oracle: exact Schwarzschild null geodesics, 2D plane (the game's sky is S¹, the view
record's sky-cell census), M = 1, static observer at r_o, ensemble RK4 in φ on
(du/dφ)² = 1/b² − u²(1−2u), dt/dφ = 1/(b·u²·(1−2u)), analytic escape tail
∫du/(u²(1−2u)) from u_c = 4h/b. Reproduce everything:

```
cd lab/results/20261019-0628-redteam-638b && ./regen.sh   # ~35 s, < 100 MB
```

All numbers below are in `results.json`; machine state (uptime, nproc) recorded there.
Shared runner, Linux/x86 — orders of magnitude only where timings matter (none do here;
all outcomes are census fractions and degree-class numbers).

**Controls (all pass).** Deflection at b = 100 M from r_o = 1000: 0.041011 vs the
shipped series 4/b + 15π/4b² = 0.041178 (0.41%), step-halving ratio 0.9994. Capture
boundary: b = 5.0 plunges, b = 5.5 escapes (b_c = 3√3 = 5.196, the same pair the
shipped oracle tests). Ensemble shadow census = the closed form to 1.4e-14°; shadow
step ratio 1.000. e59e's 25.0% of sky at r_o = 6 M reproduced exactly.

**(a) The shadow and the worldtube law.** Exact arc 2·arcsin(b_c√(1−2/r_o)/r_o) vs the
straight-row 2 M horizon tube (22d1's law applied verbatim to a hole):

| r_o (M) | exact | worldtube 2M | ratio | fabricated-visible |
|---|---|---|---|---|
| 3.2 | 167.83° (46.6%) | 77.36° | 2.169 | 25.1% of sky |
| 3.5 | 152.77° | 69.70° | 2.192 | 23.1% |
| 4.0 | 133.43° | 60.00° | 2.224 | 20.4% |
| 6.0 | 90.00° (25.0%) | 38.94° | 2.311 | 14.2% |
| 10 | 55.39° | 23.07° | 2.401 | 9.0% |
| 20 | 28.54° | 11.48° | 2.486 | 4.7% |
| 50 | 11.69° | 4.58° | 2.549 | 2.0% |

The ratio tends to b_c/2 = 2.598: the error is **scale-free** — the law is wrong at
every distance, not only deep in the field. The one-line cure (occlude the row whose
local-frame b < b_c, i.e. tube radius b_c·√(1−2/r_o)) reproduces the exact arc to 0°
everywhere (by construction: the shadow *is* the capture cross-section G4 already
gates), and cures none of (b)–(d).

**(b) The image census.** Observer at r_o = 6 M. Starfield (sources on the celestial
circle): every source has ≥3 images (max 4 within the instrument's 45-rad sweep;
deeper relativistic images are ≤1.7e-3 of the primary). The second image's flux (1D
magnification |dα/dc|): >5% of the primary for **339/716 = 47.3%** of sources, >1% for
94.4%; the ratio → 0.998 at 0.5° off perfect alignment (the equal-flux Einstein pair)
and is still 9.2% at 89° off-axis. A static beacon at r_s = 4 M: 3 images typically
(max 4): the direct image magnified up to 1.62× (α = 175.3° for the near-axis beacon),
plus a rim pair at α ≈ ±134.9°, just outside the 135° rim; the ghost carries up to
**24%** of the primary's flux (14/23 = 61% of longitudes above 5%). The letter's base
gather plus a one-deflection-per-ray memo returns exactly **1** image per source: the
missing images are real light the player should see (the ghost ship on the far side of
the hole, the ring at alignment).

**(c) Retarded times.** Star rows: t(geodesic) − t(flat cone to the same screen) =
+37.9 M median, **+98.0 M max** at α = 134.996° (the rim). The beacon at 4 M: its
direct image arrives at +42–69% of the flat time (t_flat 2.01 vs 3.40 M at the
near-axis longitude); its rim pair at **5.5–16.8×** flat. The letter's "Newton's method
finds the crossing" solves on the flat cone: the emission event it finds is the wrong
event — an error of type, growing without bound toward the rim (principle 13).

**(d) The Newton seed's tangent.** Image magnification dα/dc < 0.1 — the image moves
≥10× the source — over a **89.95°** band of sky adjacent to the rim (α from 90.05° to
135° at r_o = 6 M). The letter's iteration seeds from the previous frame's crossing:
across a quarter of the sky its linearisation is off by ≥10×, so near the rim it must
re-converge from a wrong seed every frame (branch-hopping flicker), where the true
behaviour is the smooth, diverging sweep of the Einstein pair merging at the rim.

## Predictions

`predictions.md` was written before the instrument ran once. 5 of 6 families held:
P2 (multiplicity and the ghost band — undersold: the >5% band is ~±90°, not ±30°), P3
(the beacon: 3–4 images ✓, ghost >5% on 61% of longitudes ✓, retarded ≥30% ✓), P4 (the
μ<0.1 band: measured 45× the registered floor), P5 (all controls), P6 (the b_c cure
exact and non-curative). P1 partially missed, honestly: the exact/tube ratio band
[2.3, 2.8] holds only at r_o ≥ 6 M (2.17–2.22 below 4 M), and the fabricated fraction
at 6 M is 14.2% against a registered ≥15%. **Instrument corrections, disclosed:** five
defects were found and fixed while reading the controls, before the census froze —
(1) a turning-point stall (sign-flip without progress), (2) the deflection control's
finite-radius comparator, (3) the magnification direction and the mirror accounting (a
mirrored ray serves the source at −c, not the same source; μ = |dα/dc|, not its
inverse), (4) a beacon double-count from crossings recorded on aborted steps, (5) the
escape-leg t garbage from RK4 stages at u ≈ 0 (cured by the analytic tail). Every
number above comes from the final instrument, `regen.sh`-reproducible.

## The ranked attacks (the lens's deliverable)

1. **[measured, this run]** The composed strong-field view — four channels above.
   Player visibility: maximal (the black hole is the poster object; its shadow, its
   ghost ships and the freeze at the rim are the GR "weirdness" the goal asks for).
   Rung that should have caught it: **none**. r6 gates the gather's cost/presence in
   weak field; r11's aggregate arm is fleet occlusion at player β in flat field; G3/G4
   gate single-ray deflection and capture but nothing composes the sky. Freeze-ready
   criterion (r12-strongfield-view): for a static observer at r_o ∈ {3.5, 6, 20} M
   around one M — (i) per-direction occlusion vs the exact null-geodesic map:
   fabricated-visible ≤ 5% of sky (negative: the 2 M worldtube row, which reads
   14.2%); (ii) image census: every source's second image above 1% flux present
   (negative: the one-deflection memo readout, 0 present); (iii) retarded time within
   one M-light-crossing per row at the rim (negative: the flat cone, off by up to 98 M
   and 16.8×).
2. **[from the record, argued — the named next experiment]** The merger band is the
   loudest, least-certified event: the two-body doll is licensed p̄ ≳ 65 M (r3 v3) and
   "below 12M wants NR-calibrated EOB"; L67's "inspiral by Peters' formula" is an
   orbit-averaged 2.5PN law — wrong by construction for the eccentric captures an
   emergent universe makes (per-periapsis burst loss vs the average; df81 already
   forced Peters into generator form; the handoff page's plunge census is
   "qualitative near p̄ ≈ 7M"). Player-visible: merger timing and chirp. Rung: r3's
   criteria end at bound orbits; the plunge band has no oracle. Not measured here —
   the window went to attack 1.
3. **[argued]** The dense/sparse regime selector is untyped: L71–72 choose the dense
   order "where a Knudsen-like number ≈ 1" — never defined. Principle 4 (regimes by
   dimensionless numbers) and 12 (p99: a misclassification is a spike of the crest
   class 4093 measured). r5/r5-starve prove the orders bit-identical once chosen;
   nothing tests the choice. Rung: none; allocator territory.
4. **[letter, trivial]** L28: "N ≈ 2πm/ln 2 spokes (m = 16, N = 128)" — 2π·16/ln2 =
   145.0, not 128. For the integrator's amendment pass, not a premise.

**A premise that survives, worth reporting:** the worldtube occlusion law is sound for
material occluders — its flown domain (planets at 2R approaches, fleets at player β) —
and the hole's failure has a one-line derivable cure, which is the representation doing
its job (the shadow is the capture cross-section the law already knows from G4). The
symmetry was there; the letter had the wrong occluder, not the wrong law (principle 32).

## What would make it wrong

The oracle is exact GR in the plane; the comparators are the letter's own constructions.
The attack fails if the game never renders a black hole from inside ~50 M (the board
says it will: "I want black holes"; the flyable frame already has doll primaries), or if
"the view is an instrument" is read as "the sky background need not be lensed" — but
then the ships near the hole (the beacon channel) still mis-time and double-image, and
those are gameplay objects, not backdrop. The census's μ bookkeeping is 1D (the game's
sky); a 3D port would need solid-angle magnification, changing the ghost-flux numbers
by O(1) factors, not the counts. The static-observer assumption is the strongest
simplification: an orbiting observer composes aberration with the strong-field map
(unmeasured; the comoving tail stands).

## Cost of adopting, and fit with PRINCIPLES

Adoption is three priced pieces: (i) the b_c occluder — one line, derivable (principle
3: "Nothing is evolved that can be derived when looked at — clocks, redshift, views");
(ii) the image census — the same `deflection(b)` memo read once per wrap k, the number
of visible wraps decided by the flux bar (additions in log form; principle 32: the
symmetry is found, not paid for); (iii) the retarded times — the delay integral stored
beside the deflection in the same memo, one quadrature per key. Nothing is simulated
that can be derived; the oracles (gr_oracle's quadratures, G4's capture) already guard
every ingredient. Against the letter: L57's "crosses once" and L48's single-interface
framing get the same amendment treatment e59e/c78d already earned; L28's spoke count is
fixed in passing.

**Principles quoted:** 30 ("what really matters is navigation, knowledge and dynamics
those need to be perfect … I want the player to feel what a human would feel in space");
2 (the shadow, the pair and the freeze are behaviours, not continuum fidelity); 3
(views are derived, not evolved); 13 (the retarded-time error grows without bound
toward the rim — errors that compound); 19 (the b_c occluder is the boat, not the
patched car: "the right representation always just feels right").

## The lens

A red-team overweighted the exotic: this run spent its window on the strong-field sky
at the cost of the mundane tail (occluder+observer comoving, unmeasured still). The
observer is static (a thrusting hoverer), the hole is Schwarzschild (Kerr's D-shaped,
spin-shifted shadow and its two-sided rim are unmeasured), the starfield is at
infinity, and the census's flux bookkeeping is 1D. The strongest thing this lens may
have missed is not physics but adoption: the view record's cost machinery (sky cells,
running sums) is where these cures must land, and a cost-lens run — not a red-team —
should price the composed map per frame at 10⁹.
