# Dossier — 20261019-0325-second-20261019-0141-redteam-c78d-4ff1 (second author)

## Claim

The silver's named experiment is done: the corrected eclipse-parity **aggregate arm
exists as rung r11, frozen before its run and executed — Verdict: PASS** — the per-pixel
aggregate readout holds 5% eclipse parity against the exact Σk⁴ law at player β 0.5 in
both orientations (p99 1.6% at h = R_p/2/113 samples; 4.1% at h = R_p/29 samples), the
one-sample letter (representation.md L59, first clause) fails three bars mechanically
(p99 0.84, fmin dev 0.80, false-blink 0.058), the closed-form overlap passes as the
positive control — and c78d's β arm carried a doppler typo (β counted twice) whose
correction moves every β number ~1pp and no conclusion.

## Bottleneck

Not a board bottleneck: the named gap between c78d's silver and gold ("freeze the
corrected eclipse-parity aggregate arm … and execute it for a mechanical verdict; that
is the step 13c6 took for r6"). Gain: the refutation becomes a guard adoptable in one
move (commit `r11-eclipse-aggregate.md` to `lab/rungs/`), the cure is licensed with
measured numbers instead of argued ones, and the two criterion flaws the checkers
found (the R_f-specific cap, the β-blind fmin bar) are fixed in the frozen file and
validated by measurement (ratio 0.998–1.000 at R_f = 3/10/30·R_p).

## Evidence (all from `eclipse_rung.py`, deterministic seed 20261019, float64, Linux/x86;
two independent code paths — quadratic light-cone root + clipped-parameter predicate vs
monotone bisection + 3-case predicate — outcomes identical, metrics agreeing to solver
noise ~1e-12; validated pre-run: both solvers on the light cone to 3e-14, predicates
equal on 100% of a random sample)

Base record first: c78d's own script reruns **byte-identical** in this tree (13.2 s;
`orig-occlusion.py` → `orig-regen-output.txt`). Then the decisive run (27 s author path,
2 m 9 s check path):

| config | p99 err | fmin dev | false-blink | samples | vs bound π(R_f/h)² | verdict |
|---|---|---|---|---|---|---|
| pixel-h2 (h = R_p/2) | 0.0163 | 0.0088 | 0.000 | 113 | 0.999 | pass |
| pixel-h1 (h = R_p) | 0.0407 | 0.0351 | 0.000 | 29 | 1.026 | pass |
| one-sample (negative) | 0.8414 | 0.7999 | 0.0583 | 1 | 0.318 | fail p99,fmin,blink |
| overlap-disc (positive) | 0.0018 | 0.0019 | 0.000 | 1 | 0.318 | pass |

`verdict.py r11-eclipse-aggregate.md metrics-check.json metrics.json` →
**"Verdict: PASS; pixel-h2, pixel-h1 passed every criterion"** (`verdict.txt`); no
DISPUTED (author/checker outcomes identical). Frozen case: β 0.5, R_f = 3·R_p, impact 0,
worst of both orientations, truth N = 2×10⁴ exact per-ship predicates; the rung file is
hash-frozen (`rung.sha256`, de53f498…0506, checked before every invocation).

Diagnostics (`diagnostics.json`, 11 s), folding the checkers' off-record numbers into a
regenerating record and adding the ones nobody had measured:

- **β 0.9, both orientations:** one-sample peaks 0.705/0.859 (p99 0.671/0.850) — the
  checkers' numbers, now regenerating; the **cure holds**: pixel-h2 p99 0.027/0.016,
  zero false blink. f_true_min 0.568/0.777.
- **Cap-as-function (static, h = R_p/2):** R_f = 3/10/30·R_p → 113/1257/11289 samples,
  ratio to π(R_f/h)² = 0.999/1.000/0.998, p99 error 0.0241/0.0027/0.0004 — the pixel
  cure gets *cheaper per unit flux* as fleets grow (the checkers' 11,677 estimate was
  the same bound; the error scaling 1/R_f^~1.5 is new).
- **The game's own shape (400-ship arc, r = 3·R_p, 60°):** one-sample peak = p99 =
  1.000 (centroid behind, every ship visible — both checkers' finding, regenerating).
  The pixel readout must resolve the *thinnest support dimension* (0.3·R_p band):
  3 samples (h = 0.5) → p99 0.63; 41 (h = 0.15) → 0.083; **168 (h = 0.075) → 0.038**
  at 2.4× fewer predicates than per-ship (400). This is the shape-general clause the
  first checker asked for: cost = min(N, support pixels at the resolving pitch); a
  sub-pixel aggregate pays exact per-ship sums — the readout is one law over a
  representative set either way.

**Instrument correction (disclosed):** c78d's β arm weighted k⁴ = 1/(γ(1+β²·px/q)) —
cosang defined with β (that is v·n̂) then multiplied by β again: the doppler's β counted
twice. Exact SR is k = 1/(γ(1 − v⃗·n̂)) = 1/(γ(1 + β·px/q)), used on both paths here.
The β-arm numbers move ~1pp (sky f_true_min 0.8150 → 0.7999; transit 0.535 → 0.523;
one-sample sky peak 0.835 → 0.843) — every c78d conclusion is geometric (the blink is
the representative point's predicate vs the fleet's extent) and stands. Note for the
record: both checkers "reproduced f_true_min = 0.535 exactly" from the same described
formula — agreement between reimplementations of one description is not independence
(the lab's own 5-October lesson, caught here by making my two paths differ in physics
formula only by construction and seeing the 0.012 mismatch).

## Predictions

`predictions.md` (written after the rung was hashed and the solvers cross-validated,
before any config ran). Held: pixel-h2 all five numbers (p99 ≤ 0.04 → 0.016; fmin
≤ 0.03 → 0.0088; blink 0; samples 113; ratio 1.00); one-sample fails all three
behaviour/type bars with the predicted magnitudes (p99 ≥ 0.5 → 0.841; blink ≈ 0.06 →
0.058; fmin 0.815 → 0.800 after the SR fix); overlap-disc p99 ≤ 0.005 → 0.0018; the
verdict (PASS); β 0.9 cure (p99 ≤ 0.05 → 0.027/0.016); static scaling (ratio ≈ 1.00,
errors below the predicted ceilings); arc one-sample = 1.000. Missed, both disclosed:
**pixel-h1 passes** (p99 0.041 ≤ 0.05; I predicted FAIL 0.05–0.10 from the static *peak*
7.7% — at p99 semantics the >5% spikes occupy <1% of the path; the frozen bar is p99,
matching the lab's B15 preference, and it licenses the 29-sample readout: the record's
145-sample cure was conservative); **arc at h = 0.15 misses 5%** (0.083 vs my ≤ 0.05 —
a thin band is nearly all edge; the h = 0.075 arm, added after seeing this, lands
0.038, pinning the resolving-pitch rule at h ≈ w/4).

## What would make it wrong

- The frozen case is one (β, R_f, impact, shape) triple plus two orientations; a
  different regime (strong-field occluder, comoving observer, occluding *aggregates*)
  is unmeasured — the rung's domain line says the transit must be resolved on screen,
  and direction 4 keeps those tails open.
- p99 semantics license spikes: at h = R_p a single frame can err ~8% (peak). If the
  integrator wants per-frame worst case, re-freeze the behaviour bar as peak ≤ 5%
  (pixel-h2 measured peak 0.030 static / 0.027 β 0.9 — it passes either way; only
  pixel-h1's license changes).
- The doppler correction is mine against the record's stored numbers: if c78d's formula
  was an intentional convention (β pre-folded), the ~1pp shift is moot; nothing in the
  dossier or checkers says so, and SR is unambiguous here.

Cost of adoption: commit r11 to `lab/rungs/` (one file, criteria already
machine-checked); wire the occlusion readout as per-pixel exact predicates when the view
gains opacity — O(pixels) per aggregate per frame, no per-ship loop (principle 3: the
occluded fraction is derivable at pixel resolution; principle 17: no part where
29–113 predicates replace 10⁵). PRINCIPLES fit: the refutation *defends* principle 28
("the view is an instrument… it's a space clock literally" — an instrument that blinks
out whole fleets carries no information); the rung is principle 21's "rough first,
refine when a certificate could break", executed as principle 10's simplest falsifying
test made mechanical.

## The lens

The second-author lens sees only the named gap; it did not sweep exotic regimes
(photon-sphere occluders, fleet-on-fleet eclipses, sub-pixel fleets at high γ) —
direction 4 keeps them. Its blind spot here: trust in the record's described physics —
caught once (the doppler) only because the two paths were built to differ; any number
of mine that both paths share a formula for (the segment-vs-disc law, the lens area)
has the same exposure. The rung file, once committed, is the integrator's to re-freeze
at the plane's own speeds (β 0.9 arm measured here as the next decade's evidence).
