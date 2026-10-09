# Dossier — second author on 20261009-1504-redteam-2320 (the gather's enumeration hole)

## Claim (re-scoped, as the checker demanded)

representation.md §2's view gather ("Each visible tube crosses the observer's
past light cone once; Newton's method finds the crossing, starting from the
previous frame's. Lensing adds crossings…") has no mechanism that *enumerates*
images, and the checker's named experiment confirms this for **both lens
families in the goal, with the scope corrected**: for **compact lenses**
(r\* < b_E ≈ 80: the author's r\*=50 star *and* the r\*=3M black hole) the
second image is missed in **100% of the frames in which it exists** — for the
BH it exists from doll entry at *every* alignment (no occultation can kill
it), is ≥ 2% as bright as image 1 at every transit frame (3.5–77.6%), and
even a generously *handed* branch is lost after one frame step and never
recovered; for **normal stars/planets** (r\* ≥ b_E) there is no caustic birth
to miss (measured: zero two-image alignments) — the same hole manifests as
**absorbing emptiness**: after a plain transit's occultation the source never
reappears (36/36 post-occultation frames: truth 1 image, gather 0); the BH
**wrap family** exists at all alignments on both sides but at 3×10⁻⁶–2×10⁻⁴
of the primary's brightness — beneath any visibility bar, a benign residue.

## Bottleneck

Unchanged from the author: not a board row, but premise 5 of the lens list
(the view gathered at the past light cone) and "knowledge", which Julien
named must-be-perfect. Gain of fixing: zero compute, one design sentence +
one r6 criterion. Cost of not fixing: r6 freezes cost-only on a gather that
is blind to image birth (compact lenses) and to image *re*-acquisition after
occultation (the common case), and the BH — the goal's named object — makes
it worse: nothing ever occults the second image away, so the miss has no
natural end.

## Evidence

All numbers regenerate from shipped code in this folder. The instrument is
the author's `falsifier.py` imported unmodified (scene global R_STAR set per
part, as a config); brightness = 1/|ds/dθ| (absolute slope; downward
crossings counted — the author's positive-slope formula silently returned
`inf` on them), visibility bar = the author's 2%.

- **Record regenerates**: `python3 falsifier.py` (14.7 s; checker got 14.7 s,
  author 22.8 s) — summary identical to the author's stored JSON, wall time
  excepted. Star transit: 9/9 two-image frames missed, η_crit = 81.6,
  rel-mag 0.412–0.776.
- **BH transit, cold start** (`python3 bh.py`, 22 s; r\* = 3M opaque, η
  400→20→400, 59 frames, seed = the single no-lens crossing): truth has
  ≥ 2 images at **all 59** frames; continuation holds exactly 1 at all 59 —
  miss fraction **1.000**. Entry frame: 4 truth images (direct, 2 wraps,
  strong), 1 held. Missed strong image: **3.5–77.6%** of image 1, ≥ 2% at
  every frame. Held branch on-truth at every frame, ≤ 5 iterations (control
  passes).
- **BH transit, generous seed** (author's convention, all 4 truth roots
  handed at frame 0): the strong branch is **lost at frame 1** (η 400→386.9)
  and never recovers (held fraction 1.7%); the wrap seeds die at frame 0 —
  the shipped scalar march (1100 steps) ends before winding rays cross the
  source sphere (`python3 diag.py`, 0.1 s: shipped s = None, rmin = 3.65;
  a 40× extended march evaluates them). Frame-1 death cause, iteration by
  iteration: the design's own fallback step (t − s/8000, "ds/dθ ≈ source
  distance") is ~30× too shallow near the capture hole (true |ds/dθ| ≈
  2.5×10⁵), jumps to the domain clamp, and the secant then lands in the
  direct image's basin and exhausts its 6 iterations.
- **Wrap family** (`python3 wraps.py`, 11 s; zooms at the η-dependent capture
  edges θ_lens ± b_c/r0): roots on **both sides at all three alignments**
  (η = 1600, 400, 40), offsets 10⁻⁶–10⁻⁴ from the edge (deeper members at
  10⁻⁸), brightness **3.2×10⁻⁶ – 1.0×10⁻³** of the primary. Refinement check:
  dφ halving + 6001-point grid moves the root 6×10⁻⁹. Hold test: even with
  the 40× extended march, a handed wrap branch fails the shipped tolerance
  at the first frame (|ds/dθ| ~ 10⁷ there). Instrument caveat, stated: for
  winding rays the arrival tangent is taken at march exit, so wrap positions
  carry a ~10⁻⁴-rad systematic; existence and dimness are robust (found
  independently at 1600- and 6000-step marches and on the coarse transit
  grid).
- **Census** (in `bh-out.json`): the strong image's impact parameter runs
  b ≈ 7.9 (η=1600, 0.15% bright) → 18.5 (η=400, 3.6%): it exists at every
  alignment, dims outward, and crosses the 2% bar between η = 600 (1.7%) and
  400 (3.6%). Its birth is exactly doll entry; for the BH there is no η at
  which the sight-line has only one image once the doll is on.
- **Normal star, occultation** (`python3 star-extra.py`, 25 s; r\* = 100,
  η 400→5→400): held before occultation; 7 occulted frames; **36/36**
  post-occultation frames have truth = 1 image and gather = 0. Emptiness is
  absorbing. (Checker's #3, reproduced.)
- **Envelope** (`python3 envelope.py`, 17 s; r\* ∈ {50…100}, 23 alignments):
  two-image alignments 6, 5, 4, **0, 0, 0** — the visible secondary exists
  only for r\* < b_E ≈ 80. (Checker's #1, reproduced: the author's "plain
  star-transit" was in fact the compact-lens case.)
- **Held branch near the fold** (in `star-extra-out.json`; r\* = 50, both
  images seeded at η = 40): secondary dropped at η = **45** against truth's
  η_crit = 81.6. (Checker's #2, reproduced.)

## Predictions

[predictions.md](predictions.md) was written before any BH/envelope/
occultation run. What happened:

- **P1 held** (miss 1.000 from entry; strong image 3.5–77.6%, ≥ 2% every
  frame — I predicted 2–10% at entry rising to 30–100%).
- **P2 REFUTED, in the strengthening direction**: I predicted the generously
  seeded gather would hold both n=0 images through the transit. Measured:
  the strong branch dies at frame 1 (fallback slope ~30× wrong near the
  capture hole) and never recovers. The BH case is *more* fragile than the
  star case, not less.
- **P3 band missed low, verdict held**: I predicted demagnification per
  winding in [10⁻³, 10⁻¹]; measured 3.2×10⁻⁶–1.0×10⁻³. The pre-registered
  decision rule ("< 2% ⇒ benign mechanism gap, report as such") held: the
  wrap family is invisible.
- **P4 (control) held**; **P5 held** (36/36); **P6 held** (hard zero at
  r\* ≥ 80); **P7 held** (drop at 45, predicted 45–60).

## What would make it wrong

Same escape hatches as the author's, plus two new ones. (1) If the intended
gather is per-pixel backward rays (§5), images are enumerated for free and
§2's sentence is dead weight — but law.md:53 still describes the per-tube
gather, so the doc carries the contradiction either way. (2) The BH cold
start seeds the no-lens crossing; a designer could seed the gather at doll
entry from the doll's own ±b branches — that *is* the fix sentence, adopted
in advance. (3) My occultation reading assumes the tracker keeps no
unlensed fallback when empty; if the design re-seeded from the undeflected
direction whenever the tracker is empty, post-occultation recovery would
work — again an enumeration mechanism the doc does not name. (4) The wrap
positions carry the ~10⁻⁴-rad exit-tangent systematic above; if that
systematic were adversarial it could hide a *bright* wrap, but the measured
brightnesses sit 20–10⁴× below the bar, so the verdict has margin.

## Cost of adoption, and fit

Adopt the author's fix, now with the BH numbers behind it: enumerate both ±b
branches per lensing doll per sight-line (pruned by occlusion b > r\* and by
magnification), or make the gather per-pixel. Freeze r6 as a behaviour gate
on **two** transits: a compact-lens transit with a cold-started continuation
gather (must fail: image count vs exact backward trace) and a normal-star
transit through occultation and back out (must fail: source must reappear).
The BH adds a third, cheap criterion: a *handed* branch must survive a frame
step at entry-like alignment — today it does not (the fallback slope near a
compact lens is ~30× wrong). Fit: principle 30 ("what really matters is
navigation, knowledge and dynamics those need to be perfect") and principle
19 — branch enumeration per lensing doll is the representation;
threshold-triggered probe rays or empty-tracker rescues are the bandaid.

## The lens

The second-author lens made me verify rather than explore: I did not test
multiple lenses on one sight-line (two dolls overlapping — the ±b enumeration
combinatorics the fix must bound), nor 3D sight-line geometry (all images
here live in the transit plane), nor the AI-perception reading of the same
gather (off-plan). The wrap-family demagnification was measured at three
alignments, not derived; its exponential structure is inferred from two
resolved members per side at best.
