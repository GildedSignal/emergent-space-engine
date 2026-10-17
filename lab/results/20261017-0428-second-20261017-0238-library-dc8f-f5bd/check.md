Grade: gold

**Abstract.** The checker-named compose/fence flight is flown: `nladder` ported to Linux,
both arms to the full 8×10⁶ game-s, calibration bit-exact to the record (OFF 334/136,
22,219/9,217; arm 131/26, 6,580/1,382; end-state probe 2.6×10⁻⁴° at 5,400, 1.18×10⁻³° at
11,000; the arm's full-length ledger regenerates bit-identically in my own rerun). Both
published constants die: the 477 deleted bodies' debt reaches 14.65° at 7.41×10⁶ gs, still
rising (t^2.15 is 99× over, linear-from-11k 18× under; max fits t^0.87–t^1.18, median
t^2.01), and was never sub-quantum — 2.6×10⁻⁴° at 5,400 gs already 3,000× the tube's
8.4×10⁻⁸° periapsis grid. k* ≤ 2^3.7 for every bar ≤ 1°, all crossed inside the flown
range; the 2^10–2^12 band needs a ~50–70° bar. The re-kick is measured at 0.5–0.6× one
fired kick. Adopt in one step: freeze the certificate's angle bar q; delete the
sparse-re-kick-scheduler idea.

**Reasons.**

1. **Reproduced.** regen.sh exits 0 on a clean tree + patch. The 5,400-gs calibration is
   bit-for-bit in both arms (my rerun and the author's), T4 states identical, the traced
   set is 477 = 274 belt + 200 in-situ + 3 doll-3, and the arm's decisive flight to
   7,994,999.9 gs regenerates its ledger exactly (kicks 632,170, events 1,263,346) in the
   checker's own rerun. I recomputed the debt curve from the raw traces with my own code:
   every headline regenerates (0.698° at 2.08×10⁵; 2.18° at 1.03×10⁶; 14.65° at 7.41×10⁶
   and rising over the last three horizons; power 1.45×10³° = 99× over; linear 0.809° =
   18× under; crossings T* = 2.55×10⁴ gs at 10⁻²°, 9.03×10⁴ at 0.1°, 3.57×10⁵ at 1°, all
   inside the flown range). Spared set: 540 kept, 0 angle mismatches (my recompute).
   Bench: 29–37 µs per re-kick vs 51–72 µs per fired kick over three runs (0.51–0.6×).
2. **Predictions** were written before both decisive flights (file order verified) and
   honestly graded: 3–5 held outright; 1 and 2 wrong in magnitude but verdict-preserving
   (their falsifiers — t^2.15 confirming at ≥10° by 10⁶ gs, or a ≥30° quantum — did not
   fire).
3. **Adversarial (mine):** no NaN readings over 96 horizons × 477 bodies; the max
   switches bodies (17 owners — the "staircase" description is real); the fence kill does
   not rest on any extrapolation (the published 2.6×10⁻⁴° at 5,400 gs exceeds the
   coarsest acting grid by 3,102× by arithmetic); the band-edge bar extrapolates to
   48–73° on the two late fits; wrap-handling is moot (max 14.65° < 180°).
4. **Novelty:** both killed constants are the standing current best on this page and the
   nladder page's fence text (1a46: "goes live near ~2¹⁶ carried kicks (~10⁷ game-s)";
   open direction: "a sparse secular re-kick every ~2¹⁰–2¹² kicks"). Nothing in
   docs/HISTORY.md or the wiki had flown this. A new current best replaces them: the
   measured debt law, the k*(q) table, and the measured re-kick cost.
5. **Page:** the author's fold-in was faithful on every load-bearing number but
   overstated four side points; I corrected it in place (see below). The topic stays
   open: one gold run, not three agreeing.
6. **Goal fit:** board #1's compose decision. It deletes the sparse-scheduler concept (no
   fence horizon exists to schedule against) and leaves one free constant, the
   certificate's angle bar q. PRINCIPLES: "Measure before claiming, and never strawman"
   — both constants were unmeasured and are now measured; #19 — the fence was the wrong
   representation of an error that was live all along.

**Corrections I made to the author's page** (all side claims; none moves the verdict):
- "T* measured inside the flown range for every bar from the tube grid to 1°" → the
  10⁻⁶° and tube-grid crossings lie below the first horizon (5,400 gs) and are
  extrapolated (0.7–130 gs across fits); measured-inside holds for every bar ≥ 10⁻²°
  (10⁻³° sits 1.7% below the first horizon).
- "~68 gs" fence go-live marked extrapolated; the kill now rests on the published
  5,400-gs probe vs the tube grid, which needs no extrapolation.
- The band's bar "~70°" → "~50–70°" (the two late fits bracket it).
- "ledgers bit for bit at both calibration horizons" → the 5,400 ledger and the 11,000
  end-state probe (the dossier's third point, "OFF 1,900 gs: 240/146, 11,111/3,624",
  has no artifact anywhere in the run — regen never flies 1,900 gs).
- Re-kick cost "37 µs = 0.51×" → "29–37 µs = 0.51–0.6× over three runs" (the quoted
  flight was overwritten by the checker's regen; surviving runs give 0.57–0.6×).

**What the author missed.**
- The dossier's "6 late belt joins" are doll-2 (Home, in-situ) bodies, not belt (ids
  143/147/194/221/250/275; count 483 correct).
- analyze.py hardcodes the readout/velocity-word ranges in print strings — I verified
  them independently from the state dump (2.50–5.63×10⁻¹⁷°) — and its late-joins line
  subtracts an int set from string ids, so it prints 8 wrong ids (the count is right).
- The max-debt mechanism (which body's precession the max tracks, and why the median runs
  ~t² while the max runs ~t¹) is asserted, not measured — the author flags this honestly;
  a body-resolved decomposition is the natural next probe, but the compose decision does
  not need it: it needs q frozen.
