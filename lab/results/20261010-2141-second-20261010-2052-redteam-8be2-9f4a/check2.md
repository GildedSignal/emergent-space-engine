# Check 2 — run 20261010-2141 (second author on 20261010-2052-redteam-8be2)

Grade: gold

**Abstract.** Checker 2's named experiment is done and decisive. Corrected Kerr
retrograde root: b_retro = 6.138/6.832/6.997 M at χ = 0.5/0.9/0.998, ratios
1.50/2.40/3.31 — R and dR/dr both zero to 1e-13, Bardeen limits +2/−7, consistent
with α(−6) = capture / α(−7) = 2.589. Winding images the scalar memo cannot place
measure ≤ 0.084 % of the brightest image's flux at every promised scene
(7.7 mag fainter; 0.14 % at the adversarial 6 M observer, still 7× below the
pre-registered 1 % visibility bar) — the winding-placement requirement is deleted,
and the two-sense key (b, sense|Q) + delay(b) proposal is adoptable in one
design-doc edit. All three scripts reproduce exactly from the shipped folder
(~5 s each). New, ungated: the exact map breaks Σμ = 1 by 8–36 % at 10–6 M.

## Reproduction

Clean run of the dossier's three commands in `work/`: `falsifier2.py`,
`falsifier3.py`, `magnify.py` each regenerate the stored JSON exactly, except
`runtime_s` (4.13/4.14/2.49 s vs 5.02/7.9/4.39 s) — no physics byte differs.
`out3.json` vs `out2.json` differ exactly in the Kerr block plus the added
verification block, as claimed. `patch.diff` empty: no tree edits. File order:
`predictions.md` 21:45:43 < `falsifier3.py` 21:53:16 < `magnify.py` 22:00:38 <
outputs 22:01 — the decision rule and ranges were fixed before both decisive runs.

## Independent verification (my own attacks)

- **Kerr root, closed form by hand:** Bardeen r_ph^retro = 3.532/3.910/3.998 at
  a = 0.5/0.9/0.998 and b_retro = −6.138/−6.832/−6.997 reproduce by hand
  computation; a → 1 gives b = +2.000077/−7.0000, a = 0 gives ±3√3. The rejected
  branch has dR/dr = 0.41–190 (not circular). Checker 1's "2.41" is correctly
  recomputed as 2.402 (6.8323/2.8444).
- **Magnification instrument:** I re-derived μ by direct finite differences of
  the image position ψ(β) (via `geom_beta`, not offset-linearized) at 5
  scenes/offsets, both families, k = 0,1: agreement with the chain rule is
  **0.0000 relative** everywhere — better than the dossier's claimed ≤ 1.5 %.
  Textbook control: 0.09–0.21 % (4 rows). Primary μ ∝ 1/β near alignment
  (790.0 → 31.96 ≈ β ratio).
- **Inventory completeness:** audited the outgoing-branch bound code (monotonic
  P > 0 branch, ∫du/√P maximized over b: 75–105° < 140° minimum source azimuth —
  correct); probed k = 3,4 myself — brentq's bracket is exhausted because b must
  approach b_c as e^{−πk}, so higher windings are ~1e-6 of k = 2: no missing
  images. k=2/k = 1 = 1.3–1.9e-3, the Bozza e^{−2π} order, as claimed.
- **Sum-rule deficit:** confirmed from the JSON (0.994/0.918/0.755/0.640 at
  off 0.5°, weak/mid/near/deep), flat in offset (0.7546→0.7817 over 0.02°–40°),
  and since the k = 0 pair alone gives 790.02 − 789.27 = 0.75 at near, it is a
  property of the primary pair, not missing windings. Root cause (capture cone
  removes launch directions, so the point-lens identity need not close) is sound.

## Predictions

R1–R4 (replication) all held. Held-out M1's Σμ ≈ 1 clause, M3 (mid 0.1–3 % vs
measured 0.012 %), M4's lower bound failed — each reported as a failure with a
root cause; M2 landed just under its range (0.084 % vs ≥ 0.1 %); M5 held. The
misses are in the author's prefactor priors, not in the instrument, and the
decisive quantity (visibility vs the pre-registered 1 % bar) holds with 7–12×
margin. Honest bookkeeping: nothing re-tuned, outputs deterministic.

## Blemishes (none load-bearing)

1. The deficit chain's "0.5 %" first link uses the best weak row (off 5°,
   0.9985); at off 0.5° it is 0.9941 (0.59 %).
2. "≤ 6·10⁻¹⁴" is ≤ 1.1·10⁻¹³ at a = 0.998 (still machine precision on R's
   scale).
3. By the pre-registered decision rule the verdict is technically "borderline"
   (deep scene 0.137 %, between 0.1 % and 1 %), not the "< 0.1 % everywhere"
   branch; the dossier's scoping to promised scenes (≤ 10 M, 0.084 %) is fair and
   the deep number is reported in the table.

## Novelty and fit

No HISTORY entry covers the view memo key, magnification, or winding images;
the lineage is the original run's own branch (20261010-2052, silver, "one
experiment to gold" — this is that experiment). Fit: principle 30 ("navigation,
knowledge and dynamics those need to be perfect") and 28 (the view is the
player's instrument); 34 ("the oracles are guards, not shepherds") — the guard
here says the missing images are below the spectacle's floor, and the fix stays
one bit plus one table. Principle 1: the measurement *removes* a would-have-been
requirement.

## What the author missed

- The Σμ deficit's overrendering interpretation assumes the view ever normalizes
  brightness; today's gather renders positions only, so until brightness exists
  the deficit is navigationally inert — the abstract still headlines "brightness
  defect". The caveat is in the dossier but not the headline.
- Still single-lens, equatorial, geometric μ only: beaming (g⁴/k⁴) and
  multi-doll composition remain unmeasured (acknowledged).
- No scene between 6 M and 10 M to locate where (if anywhere) windings cross the
  0.1 % line — the trend says nowhere above 6 M.
