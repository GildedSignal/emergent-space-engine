Working...
Check complete. **Grade: silver** — written to `lab/results/20261016-0213-fermi-1a1c/check.md`, with the author's wiki page corrected in place.

**What I did:**

- **Reproduced** from a clean tree (patch forward-applies to base `85adb7cf`): every deterministic number exact — 487-event true peak, 125,077 kicks, window 13,051–14,542, 2,348 B/body build, 475 MB end. Timing deltas (author 22.95 ms vs regen 36.14 ms max) are pure box load; verdict unaffected.
- **Proved the instrument artifact in both directions**: the identical 10⁵ flight flown with the 12-ms budget reads max **11.99 ms / 334 events** (worst-5 pinned at the cap line, ~240 events = 12 ms/50 µs) vs **487 events / 36.14 ms** budget-free. after2's 390/409-event readings are the same cap at the M1's 29.3 µs/event.
- **Flew outside the author's range** (3×10⁵ budget-free, the arm after2 could only fly capped): true peak **1,328 events / 71.7 ms** = 3.2× the letter at the M1 rate; scaling exponent 0.91 → break-N recomputes to 8.3×10⁴, confirming the author's 8.4×10⁴. Post-kick standing 4,700 B/body and window width 1,505 also confirm; all budget.py terms re-derived by hand.
- **Not gold**: the pre-registered break-N prediction (P2) failed ~3× (2–5×10⁵ predicted, honestly reported), nothing merges, and the staggered 10⁹ composition (2.7× vs 0.5×) stays unpinned — that stagger flight is the one named experiment to gold.
- **Page corrections**: the Refuted bullet now names 51b7's same-hour "the wave's frames hold" line (the literal quote was 51b7's, not after2's), carries both checker arms, and adds the exodus caveat ("first N-scaling break", M1-projected). Also noted: the author's residue rate is 3.4×10⁻⁵ measured, not 4.5×10⁻⁵ (bracket survives). Working tree left clean.
