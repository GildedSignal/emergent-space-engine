Grade: lead

**Abstract.** Claim: the fleet doll's Clohessy–Wiltshire closed form is a law for a fraction of a parent orbit, not a session. Reproduced bit-identically (10.4 s). The circular-parent headline is a metric artifact: truth and CW share the along-track drift to 1.3% (−37.2 vs −37.7 offsets per period); the one-period "7.7×" is 7.71a of pure flat-frame curvature, and the arc-mapped model error is 1.85a (1 period) and 50a (100 periods), not 3818a. Inside a 5-offset doll the error stays below 0.1a; formation keepers drift 3π(a/R)·a per period, which the doc's "carry the quadratic term" hedge already covers. At e = 0.3 the failure is real (drift rate off 2.3×) but known (H0203) and already designed around (law.md's Fermi-normal dense frame).

## Reproduction

`python3 lab/results/20261009-0208-redteam-e369/falsifier_cw.py` → output **bit-identical** to `run-output.json`, 10.4 s single-threaded (dossier: 10.7 s). `work/patch.diff` is empty and `git status` shows no tree edits outside the run folder. `predictions.md` (mtime −13 min) precedes the script and `run-output.json` (−4 min); ordering is consistent with pre-registration, though `run.log` is empty so nothing else corroborates it. P4's instrument controls confirmed (closed form vs numerical CW 4×10⁻¹²; half-step identical).

## Predictions

P1 failed and the failure is disclosed honestly — but it fails against the artifact, not the law (below). P2/P3 held only under the author's metric; P5 correctly did not trigger on the eccentric leg, which is the part that survives scrutiny.

## Attacks (3+ adversarial cases of my own)

Probe (plain Python, same RK4 truth, 5.5 s, <100 MB): for each case I computed (i) the author's Euclidean local-frame error, (ii) the **arc-mapped** error — the doll maps the CW offset to a position by rotating the parent by y/R instead of straightening the tangent — which removes pure flat-frame geometry, (iii) the **unwrapped along-track drift slopes** of truth and CW, (iv) the error **inside a 5a-extent doll** before the first exit (an overset Chimera disc hands an escaper over at its edge; law.md's dense order is Fermi-normal, so the rotating-frame reading is the weakest steelman the premise still admits).

| case (a/R = 0.01) | author 1P / 100P | arc 1P / 100P | curvature term at 1P | truth vs CW drift slope |
|---|---|---|---|---|
| e=0 rest | 7.68 / 3818 | **1.85 / 49.9** | 7.71 | −37.2 vs −37.7 a/P (1.3% apart) |
| e=0 ellipse | 0.09 / 9.1 | 0.09 / 9.1 | 0.00 | 0.1 a/P vs 0 (keeper) |
| e=0.3 rest | 90.7 / 3863 | **109.6 / 214** | 68.9 | −86.4 vs −37.7 a/P (**2.3× wrong**) |
| e=0.3 ellipse | 50.9 / 160 | 65.7 / 185 | 12.8 | −36.1 vs −37.7 a/P |
| e=0 ellipse, a/R=10⁻³ | — | 0.0094 a/P | — | matches 3π(a/R) = 0.00942 |

1. **The e=0 headline counts a drift the model predicts as model error.** At one period the truth member is 0.394 rad behind; `R(1−cos δ)` alone is 7.71a, i.e. the entire "7.7×". Truth and CW drift **together** (−37.2 vs −37.7 a/P), so the "unbounded ~38a/period" law the dossier fits is the CW drift term itself. The genuine law error at e=0 grows at ~0.5a/period (49.9a at 100 P), **77× slower than claimed**; the "~13 re-anchors per orbit" is ~2 per orbit (arc error crosses 1a at 0.5 P), and ~11 periods for keepers.
2. **The domain rule was never enforced.** CW requires offset ≪ R; the author's 100-period numbers hold a member whose offset reaches 38×R. A doll of extent 5a hands such a member over after ~0.13 period — one event per escape, with in-box error < 0.1a at e=0. The measured e=0 configuration is one no design would run.
3. **The e>0 leg is real and survives the fair metric** (drift rate 2.3× wrong at e=0.3; ~50–110a within one period, cadence ~50/orbit) — the strongest content in the dossier. But see novelty.
4. **The "carry the quadratic term" hedge covers the circular case exactly.** The keeper drift is second order in a/R (Δa/a = −(a/R)²; 0.0914 measured vs 3π(a/R) = 0.0942 leading order — the dossier's "exactly 3π(a/R)·a" is itself 3% off). At a/R = 10⁻³ keepers hold 1a for ~106 periods: a session, not "a fraction of one parent orbit".

## Novelty

- The attacked sentence **already contains the finding it is attacked with**: "That is only first order: … off by 7.7× their offset after one period (red-team, H0203), so members re-anchor … or carry the quadratic term." H0203 (29 September) adopted "Clohessy–Wiltshire is first order only".
- **law.md's dense order (30 September) already replaced the frame this run kills**: "The frame is Fermi normal coordinates along an exact tube … not a linear epicycle about a circle … no Coriolis terms … (Clohessy–Wiltshire is its Newtonian, circular limit) … Re-anchoring is recentring plus rebinding the tube … with the exact remainder." The dossier never mentions Fermi normal coordinates; its proposed deletion ("quiet members are parent-doll tubes") is already the live design — its own cost-of-adopting concedes this ("already the live path — the co-orbital certificate of the 6 October gold").
- New relative to the record: the 100-period horizon, the eccentric multiplier (~e^1.3–1.6), and the r5 drift criterion (positive control a parent-doll tube, negative the closed form) — useful, but attached to a headline that does not survive the domain check.

## Goal fit

On-goal in aim (the "undisturbed ≈ 0" cost row is worth attacking), but the circular verdict strawmans by construction ("Measure before claiming, and never strawman"): the run measures the closed form 38×R outside its domain and bills the shared drift as model error. The 5 October taste-log lesson applies here in reverse: this run and H0203 share a harness and a metric convention, so their agreement on "7.7×" is not independent confirmation of a law failure.

## What the author missed

- The CW validity domain (offset ≪ R) and the handoff at the doll's edge; the first diagnostic should have been **truth-vs-CW drift slopes** — one line that exposes the shared drift at e=0 and the genuine 2.3× failure at e=0.3.
- law.md's dense-order paragraph: the live design already demoted CW to a limit and moved to Fermi-normal coordinates with re-anchoring, so the premise as attacked is a draft sentence, not the design.
- That the doc's "carry the quadratic term" hedge is exactly the measured circular keeper drift (both second order in a/R), so the hedges *do* cover e=0; their insufficiency holds only at e>0.
- If re-derived: measure re-anchor cadence for quiet members in the **Fermi frame of law.md** (or Tschauner–Hempel) at belt eccentricities — an O(1)/orbit cost there is the result that would actually break the "≈ 0" row and earn the doc edit plus the r5 criterion. That experiment, not this one, decides the premise.
