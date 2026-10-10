# Dossier — premise red-team of the view (run 20261010-2052-redteam-8be2)

**Claim.** The design's view premise — "each visible tube crosses the observer's past
light cone once; lensing adds crossings from the doll's memoized deflection(b)"
(representation.md §2; law.md line 53) — is measured **sound for a static spherical
doll** (≤ 0.6% image error even with the observer at 10 M) but **broken in its memo
key**: the one-argument deflection(b) cannot represent a rotating doll at all
(critical impact parameters differ by 2.37× between senses at χ = 0.998; the two
senses bend by 0.58 rad differently at the same |b|), and the cone's curvature in
*time* is never memoized (ignoring the Shapiro delay mis-places a 0.5 c emitter by
9.8° in a scene the game promises) — and no frozen gate anywhere tests the composed
view's behaviour.

## Bottleneck

Board focus item "the engine's live questions" and principle 30 ("navigation,
knowledge and dynamics those need to be perfect") make the player's only instrument
(principle 28) load-bearing. The gain is not OoM speed: it is preventing a wrong
representation of the view memo from being built and frozen (a two-argument memo key
and a delay table cost almost nothing *now*; retrofitting after the visual layer
exists is what "temp solutions tend to stay that way" warns about). It also deletes
nothing — it *adds* one memoized function (delay) and one key bit (sense), the
cheapest possible fix in the design's own idiom.

## Evidence (float64, equatorial, M = G = c = 1; runtime 5.0 s)

Oracle: exact null geodesics by periastron quadrature (`work/falsifier2.py`;
self-check α(b=100) = 0.04123 ≥ 4/b in the weak field, matching the B3-style
regime). Construction = the most charitable reading of the design: flat retarded
crossing + point-lens equation with flat trig distances, fed the **exact** two-point
bend of the true path at each screen angle, so only composition error can appear.

| Case (r_o / r_s from hole) | exact images (k=0) | construction error, primary | secondary |
|---|---|---|---|
| weak control 5000 / 20000 | 2 (Einstein ring ±1.47°) | 0.000° | 0.000° |
| 50 / 200 | 2 | ≤ 0.025° (0.13%) | ≤ 0.13° |
| 10 / 50 | 2 (ring at ±42°) | ≤ 0.29° (0.59%) | ≤ 0.25° |

**Survives:** the composed image is right to half a percent with the observer at
10 M, across β from behind-the-hole (0.02°) to 40° off. The exact gather also finds
winding images (k=1 pair at ±27.7°, *inside* the bright pair, at 10 M) that a
thin-lens reading of the memo does not place; their visibility (magnification) was
not measured — a named open case, not a kill.

**Kerr, equatorial (closed-form circular photon orbits, verified at a = 0 → 3√3
both senses):**

| χ | b_pro | b_retro | ratio |
|---|---|---|---|
| 0.5 | 4.10 M | 4.83 M | 1.18 |
| 0.9 | 2.84 M | 4.95 M | 1.74 |
| 0.998 | 2.11 M | 5.00 M | 2.37 |

At |b| = 8 M, χ = 0.9: α_pro = 0.676 rad, α_retro = 1.254 rad — **the same |b|, two
bends 33° apart**. A photon arriving at the same screen angle on either side of the
hole queries the same memo key and gets one answer. B19 promises the lopsided
shadow "emerging"; the doll's geodesics can produce it, but the view's scalar memo
cannot show it. Off the equator (every view direction that is not in the plane) the
bend also depends on the Carter constant Q: the key is (b, sense) in-plane and
(b, Q) in general.

**Shapiro delay (the cone is curved in time too):** emitter behind the hole,
v = 0.5 c tangential:

| observer / emitter | Δt_Shapiro | shown-position error if flat-timed | vs lens displacement |
|---|---|---|---|
| 10 M / 15 M | 8.58 M | **9.84°** | 27% |
| 10 M / 50 M | 9.95 M | 4.75° | 12% |
| 50 M / 200 M | 11.29 M | 1.29° | 9% |

The design memoizes the bend; the crossing solve ("Newton's method finds the
crossing") needs the *delay* as well, or every fast body near a compact mass is
shown displaced along its track by an angle of the same order as the lensing it
*does* correct. Control: a static emitter (v = 0) has zero position error by
construction — the error is exactly the motion during the unmodeled delay.

**Negative control:** with α = 0 the construction returns the flat direction
exactly (23.98468° = β), single image — the gap is the strong-field composition,
not the oracle.

**Gate audit (which rung should have caught this): none.** B3 gates the *bend*
accuracy of a static mass; B16 gates the *bend* of a moving (boosted
Schwarzschild) lens — spherical only, direction only, no timing, no image
composition; B19 gates the doll's Kerr geodesics (tubes, capture, dragging), not
the view's memoized deflection(b). r6 as scoped in representation.md §7 ("Newton
iterations and samples per frame") is cost-only, and **r6 and r5 were never
frozen** (lab/rungs/ holds r1–r4, r7–r10; law.md line 88 still lists r5/r6 open).
Premises 1–3 were checked against the record and survive: EOB-1PN ν-only-in-energy
(r3 v3: 1024/1024, 632/632; B11), Binet bands (H0205: every r1 criterion, 38
crossings/cycle), kicks/cycle-derivatives (plane gates; re-anchoring adopted 6
October).

## Predictions

Held-out set and expectations in [predictions.md](predictions.md). Outcome: **P1
refuted** (predicted >1% and >5° near the shadow edge; measured ≤0.59% and 0.29°) —
the blind-spot warning in my own lens applies to me; the composition is better than
I estimated. **P2 partially refuted** (both bright images placeable; winding branch
unplaced, visibility unmeasured). **P3 held** (scalar memo impossible; my ">1 rad at
the same b" threshold measured 0.578 rad at b = 8 M — direction held, magnitude
overestimated; b = 6 M retrograde is near-critical and the quadrature diverged).
**P4 held for near scenes** (27% and 12%), borderline for the 50 M scene (9%).

## What would make it wrong

My construction is a reconstruction: the design never states how deflection(b)
composes into an image angle, so I used the standard point-lens equation with exact
α. If the intended mechanism is per-doll ray integration instead (each doll's Binet
light solution is exact, per r1's own light model), then P1/P2 are moot and only
the memo *key* claims (P3) and the missing delay (P4) stand — those do not depend
on my reconstruction. The magnification of the winding images is unmeasured, so
"missing images the player would see" remains open, not claimed.

## Fit with PRINCIPLES

- "the right representation always just feels right it does the job like cutting
  butter" (19): a scalar deflection(b) is the wrong key for rotating dolls; the
  right one, (b, sense|Q) + delay(b), is one bit and one table — butter.
- "A step is a certificate: the interval over which a description reproduces the
  law" (§3): the view's description has no certificate at all, and its two known
  defects (P3, P4) are exactly what one would have caught.
- "Gates are frozen before the first run" — the two premises without gates (view,
  dense/sparse bit-identity) are the two whose rungs were never frozen; the §7
  ladder is also stale against the live rung set (r8/r9/r10 ran with kills, are
  absent from the doc).

## The lens

A premise red-team overweights exotic cases; I inverted that and measured before
claiming, which refuted my own strongest numeric expectation (P1). What this lens
may still have missed: magnification/brightness (beaming k⁴, aggregate sampling)
and the off-plane (Q) behaviour were argued, not integrated; and everything here is
single-lens — multi-doll composition of two bends plus one delay was not measured.

## Reproduce

```
cd lab/results/20261010-2052-redteam-8be2/work
python3 falsifier2.py > out2.json   # 5 s, numpy+scipy only
```
