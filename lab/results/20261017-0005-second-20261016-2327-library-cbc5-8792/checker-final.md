Working...
Check complete. **Grade: gold** — written to `check.md`, with the author's `wiki/promotion.md` corrected in place.

**What I did**

- **Reproduced**: `regen.sh` (runner, exit 0) matches `ledger_out.txt` on every digest and counter; timing deltas ≤ 0.1 µs. Re-derived the ledger arithmetic by hand (23.1 µs budget line, 0.78/2.0/16 cores, 7.5 gs dmax — all correct). Patch's dwell path is cache-policy-only, proven behaviourally: every arm at every dwell/seeds/N I flew prints its scene's ctl digest bit for bit.
- **Predictions audit**: `predictions.md` predates the flights and contains misses a post-hoc document wouldn't (P1/P2 lower edges violated at 10⁴, disclosed; P5's dwell-1000 ≥2× measured 1.76×). The decisive cells held: P3 dead-on (0.78 vs [0.8, 1.2]), P4, P6.
- **Adversarial (9 own flights, one outside the author's range)**:
  - *Dwell 40/60*: miss 72.1%/71.7% — flat with dwell-17's 73%, cliff is **between 60 and 100 gs**, monotone, sharper than claimed; verdict strengthened.
  - *Seed 2*: identity holds (one digest across arms); cliff reproduces (69.3%/13.7%); reads +5.5%; standing sets ≈ seed 1's.
  - *N = 2×10⁵*: retain reads 2,803,494 vs two-N-fit 2,807,130 (**−0.13%**) — the b = 11.48 constant and 5.74×10⁷ reads/s extrapolation stand on three N; dwell-100 standing N-linear, dwell-17 standing 167 at all three N. Peak RSS 1.17 GB.
- **Gold basis**: it is the predecessor page's named open experiment; it shows a premise wrong (ledger's 44 µs → measured 3.7–5.3 µs, ~8–10×, with a decision consequence: the delete lever drops out of the mint budget); adoption is one step (wire the coast dial).

**Two corrections to the page** (conclusions unchanged): the author's mint range 3.7–4.9 µs excluded their own worst arm (dwell-17 burn 10⁵ = 5.24 regen / 5.27 implied by their own 221-core line / 5.58 on seed 2) — now 3.7–5.3 µs, margin ≥4.4×; and the λ×dwell standing-resident law ("memory-feasible dwell ≤ 7.5 gs") is an artifact — their own dwell-1000 point and my 40/60 plateau show a burst-structured set (167 / ~6.7k / 8.2k). The no-dwell verdict survives on the robust legs: CPU cliff-left (~220 re-mint cores at ≥72% miss), memory cliff-right (~95 GB, N-linear at three N).

**Residuals**: one scene family, one burn cadence (single word at 1000 gs) — the 60–100 gs burst scale everything hangs on is untested on a formation scene; the sub-frame dwell class stays interpolated. Both named in check.md as the next probes.
