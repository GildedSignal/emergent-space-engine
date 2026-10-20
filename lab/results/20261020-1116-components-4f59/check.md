Grade: gold

**Abstract.** 4f59 prices promotion od 1(b), the phase/along-orbit second axis, at the belt seam.
Reproduced bit-for-bit: the shipped tier BAILs in-band and reads all N while the exact window
holds T = 1 at N = 10⁴/10⁵ (overread N/T ≈ 10⁴–10⁵×); the sound filter (0 misses everywhere,
including my 10 adversarial arms) reads 4.7%/4.2% of N — **21–24× resident, 100× cold** — served
by a θ-index in 0.18 µs at 10⁶. Crosser bound: at 0.03 c the truth itself is 21% of the belt
(v·h = 1.6 AU) — that lever is the interval h, not the index. Deletes 396d's "(a) local bail"
patch. Adoption: one index beside `Radial`, per-body caps, `hit` unchanged — one step. My arms
held soundness everywhere; one domain boundary (hot belt) and one number corrected below.

## Reasons

**Reproduction.** Applied `work/patch.diff` to a clean tree, ran all three dossier commands. Every
count reproduces exactly: engine T=1, F=470/4,209, misses=0, ρ/r=0.0066, ω=0.0032 rad, offline
T/F/e-graded all identical (belt 22/113,731/226,977; cold 22/1,085/193,110; crosser 216,759→
212,070 across the two invocations). Timings jitter with load (walk 57–103 ns/body across
regen/mine; dossier's 64/105 same order). The truth window is radial.rs's own certificate law
(|d| ≤ near + (v_a+v_b)·h is the exact `hit`'s sound superset — verified against
encounter.rs:130–155 and the doc at radial.rs:7–11); the phase cut is phase.rs's own bound
(ω = 2·asin(ρ/2·r_min), centre = e + 2·asin(e/(1+√(1−e²))), phase.rs:39–49). F ⊇ T is forced by
the triangle inequality given `range_of`'s lo/hi are true current-radius bounds — and it held
empirically at every arm.

**Predictions.** predictions.md predates the decisive outputs (file times; run order). P1, P2, P4,
P5, P6 held; P3's ratio (|F|/|T| ≤ 2.5) missed by ~3 orders (470–5,170) — honestly reported, and
the miss *is* the finding: at encounter-sparse density T = O(1) and the filter's dilution (the
e-bulk, not the drift) is the design constraint. P3's kill criterion (a soundness miss) never
fired.

**Adversarial (mine, 10 arms beyond the author's 5; `seamscan_adv`, same laws, removed after).**
- *Formation (taleb-09b5's invariant, the unflown arm):* a 10⁴-ship crowd on the scanner's own
  orbit — kept whole, 0 misses, F/T = 12.3 with the crowd as signal. The phase axis does NOT
  reproduce the pairwise tier's concentration ruin. The author's "by construction it keeps them"
  now has a number.
- *Hot belt (e Rayleigh σ=0.3, redraw 0.9):* F = 48.7% of M for T = 4. The 21–24× cut is a
  property of the shipped belt's cold e-bulk (F ≈ (ω + 2c(ē))/2π); on a hot belt the axis buys
  ~2×. The claim is scoped to the flown mix, and the page now carries the boundary (my correction).
- *e-cap 0.7/0.9 at σ=0.07:* F unchanged (11.3%) — the redraw cap is immaterial; the Rayleigh tail
  is empty. The author's e ≤ 0.4 domain limit doesn't bind.
- *Radially-spread family* (the author's sits at periapsis, disclosed): T=18 vs 22, F identical —
  the disclosed optimism is immaterial.
- *Crosser sweep 0.001/0.003/0.01 c:* T = 0.09%/0.67%/6.2%, F = 12.1/13.7/19.4% — the lever dies
  smoothly; 396d's 0.03 c is the continuous end, not a cherry-pick.
- *Index at 10⁷ (a decade beyond):* 0.29 µs, O(log) holds.
0 misses in every arm.

**Novelty.** The page's prior phase-axis work measured concentration (b083: rigid rings, the
offset compare; 5f36: keys fleets, the answer residual); 4f59 prices the axis on the diffuse
shipped belt at the band — the regime 396d's seam flight exposed and named "(b)". New: T = O(1)
at flyable rungs on shipped code (the ~10²× overread framing corrected to N/T ≈ 10⁴–10⁵×), the
cold-belt collapse (396d's named unflown arm), the crosser bound (premise correction on the od 1b
letter), the e-graded pricing, and the deletion of fix (a). Not a repetition of b083/5f36; it
composes with them.

**Page.** Faithful except one number: "class caps read 2–20× more" — the e-graded column reads
2.0× (belt), 1.3× (crosser) and **178×** (cold: 193,110 vs 1,085 — class caps destroy the 100×
collapse). Corrected in place; the correction *strengthens* the per-body-cap constraint the author
names. Checker bracket with my arms appended.

**Fit.** PRINCIPLES 33 ("a body resolves only the influences that are significant at its own
scale" — the scan reads only the angular window that can matter) and 5 (priority is slack, not
proximity); board live question 1, the seam's full-universe walk. The print-only probe changed no
engine path; the tree restored after regen.

## What the author missed
- The e_j readout in the engine arm is `2^48/k − 1 = e/(1−e)`, not the orbit's e = `1 − k` (from
  `range_of`'s apo = peri/(2k−1)). Conservative (widens `centre`, keeps soundness), but the
  kept-e percentiles are inflated (reported p50 0.116 → true ≈ 0.104).
- The dossier's offline table mixes the two invocations without saying so (resident/cold from the
  10⁴ run, crosser 212,070/351,922 from the 10⁵ run). Both regenerate; undisclosed mixing.
- The offline arms print no miss count (0 by construction — bodies at periapsis sit exactly on the
  bound's edge); verified 0 empirically here.
- The formation arm was the one named invariant left unflown; it holds (above), and it is the
  page's strongest addition now that it is measured.
- The answer channel downstream of |F| is unpriced: at 10⁶, |F| = 113,731 × ~4.4 µs ≈ 0.5 s a
  scan at 604c's class — the filter cuts the channel 21–24× but does not close it; the page names
  this next, correctly.
