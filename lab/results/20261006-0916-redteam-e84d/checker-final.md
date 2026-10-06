Working...
Check complete. `check.md` written to `lab/results/20261006-0916-redteam-e84d/` — nothing else in the run folder touched.

**Grade: silver.**

What I did, and found:

**Reproduction** — all five belt configs reproduce **bit for bit** (0.75% / 2.125% / 5.75% / 28.625% / 0.0% chaotic); `eob_2pn.py` reproduces its table exactly (10.19% at p=20M); `patch.diff` empty; `predictions.md` timestamps precede the decisive sweep.

**A1 (belt) survived everything I threw at it** — new seeds 5.6%/6.6%; threshold τ_a ±2× gives 5.1%/8.9%; the decisive mechanism control (sub-band [0.50,0.60] between first-order resonances) gives **0.125%** vs 5.75% full band — the chaos is the resonance network, not an instrument artifact. T=2400 shows steady-not-growing (3.5%). The gate gap is real: no belt+planet scene anywhere in the ladder.

**A2 collapsed under independent derivation:**
- The code contradicts its own docstring: doll = 3X(1+**3.5**X) vs `(1−6X)^{−1/2}−1 = 3X+13.5X²` (bracket **4.5**, or **6.5** in the paper's radial-frequency variable X_n).
- With 39/4 on x₂² (the heavier body), b1−b2 → 6.5 = exact Schwarzschild — the parse then *does* validate at ν→0; the author's version fails the very check they cite. At ν=0.25 the swap changes nothing, so the honest doll error is 0.3333X/(1+6.1667X) ≈ **1.27% at p=20M** (sign flipped), not 10.2%; the 1% boundary is p≈28M, not 267M.
- B11's tolerance (1% + 2·8/p) at p=20 is **81%** (a fraction — the 1PN oracle's own truncation, already recorded in H0203/H0206), not 1.8% — "exceeded 5×" is a unit misread.

**Silver because:** the author's own pre-registered kill criterion didn't fire at Jupiter μ (fires only at μ=1e-2), three held-out predictions failed (disclosed), and the second measured claim is wrong in its headline numbers. **Gold experiment:** the steady-state run (T≥5000, ejection-tracked) plus A2 refiled with the corrected parse.
