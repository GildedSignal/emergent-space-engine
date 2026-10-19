Working...
`check2.md` written — **Grade: gold** — and the run's wiki page now carries my checker2 block. Tree restored (`?? lab/results/` only).

**What I did:**

1. **Reproduction.** Applied `work/patch.diff` in a clean tree, rebuilt, reran `mb400_bs2_s1`: digest `9355d32a…` identical. Wrote my own analyzer (no reuse of the author's) and regenerated every dossier number: mean×w = 438247/431510/426593/465824 across the 3× box, 15.55× vs matched control (31.9, F64 0.91), F64_late 1.29–2.61, walls_max 4–10 (controls 2–3), late wall rain 7.4×, 6400 blocks 3373→2286→2209, free arms walls=0, season peak 2075 = 65.0× cold, season length 14.7–15.1·extent, autocorr peaks at one window everywhere.

2. **Pre-registration.** `predictions.md` kill branches pre-stated; P1/P2 fired (no 4·w clock in either series — spacings 2752/2304 vs 3480 predicted) and the kills are the reported result; verdict rule honored.

3. **Attack, three cases outside both checkers' ranges:** H=32768 at n=1600 (2× the longest horizon, 4·w lag now in range: contacts r=−0.078, walls r=−0.057 — no clock; plateau stationary at 483–485); belt 4× colder (late 485.0 vs 496.0 — the standing rate is the fleet's energy, so 15.5× is a lower bound); n=12800 (walls ≤9/chronon against a block bounce's 6400). All confirm.

4. **Corrections verified independently:** the echo constant is 0.60–0.63 on a fixed window (my numbers 0.625/0.601/0.629) — the dossier's 0.31–0.35 is a trough artifact, already corrected on the page; the dossier's "≈1.35·per_row at both" overstates n=400 (1.15) — the page states it correctly.

5. **Novelty/goal fit.** The topic page named exactly these three unflown cases; no HISTORY entry covers them. Zero-code adoption, two premises killed (wall-reflection train; fleet-coherent-forever), one sizing rule delivered.
