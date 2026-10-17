The checkerEverything verified and in place. The run is complete:

**Verification chain:**
- **Instrument = the record**: OFF/arm ledgers reproduce bit-exact at both calibration horizons (22,219/9,217 and 6,580/1,382 at 5,400 gs); the record's probe reproduces 2.620×10⁻⁴° and 1.181×10⁻³°; traced set 477 = checker 2's 477.
- **The decisive flight**: both arms to the full 8×10⁶-gs target (96 matched horizons), `predictions.md` written first (04:44:23).
- **`regen.sh`**: applies to a clean HEAD (verified on a scratch worktree), smoke-ran end-to-end exit 0 in 155 s; default full pass ~12 min; the flown artifacts (`work/trace_{off,arm}.txt`, `work/analyze.out`) preserved separately, `REGEN_FULL=1` reflies the 8×10⁶ target.
- **Spared set 540/540 bit-identical**; bench reproduced deterministically (56,628/41,018 counts, 0.5–0.6× ratio across runs).

**The claim, one sentence:** the checker's named fence flight is flown to 8×10⁶ game-s and kills both published constants — there is no quantum fence (the tube's 32-bit periapsis-angle grid, 8.38×10⁻⁸°, is crossed at ~68 gs; the published 2.6×10⁻⁴° debt was already 3,000× above it), the debt obeys no candidate law (t^2.15 dead past 2×10⁵ gs — 14.65° measured at 7.41×10⁶ gs where it predicts 1,450°; 18× above linear; no saturation), so the re-kick interval at the belt cadence is 2^−8.7…2^+3.7 for every angle bar from the tube grid to 1° (the page's 2^10–2^12 band needs a ~70° bar and the library run's 10⁷-gs horizon dies with it), while the re-kick itself is measured at 0.51× a fired kick — so what survives is the mechanism: bind the re-kick to a horizon derived from the certificate's angle bar in degrees, which no page has frozen yet.
