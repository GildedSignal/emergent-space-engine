Working...
Check complete. `check2.md` written, the author's wiki page corrected in place, tree otherwise clean (only untracked: the author's applied patch plus my two checker examples, which the checker-patch mechanism captures).

**Grade: silver** — the physics is gold-grade, the cost instrument was not.

What I did:

1. **Reproduced** — applied `work/patch.diff` in a clean tree, re-ran `regen.sh`: every physics number bit-identical; walls shift only with load (191→254 µs at e 0.999).
2. **Verified independently** — derived the closed form myself from the integral table ($\int_0^\pi \frac{d\psi}{\sqrt{a-b\cos\psi}} = \frac{2K(m)}{\sqrt{a+b}}$ gives exactly the probe's $A$, $m$; the shipped `scale(1)` confirms the factor 2), then checked with mpmath at 50 dps from the keys' **exact integer fields** — no shared harness. Agreement 3–4×10⁻¹⁰ everywhere the author claimed, and beyond: e = 0.99999 (3.4×10⁻¹⁰), m = 0.947 (8.7×10⁻¹¹), the weak/strong cut, first-order 6πM/p. My own τ/t closed forms match to 7×10⁻¹⁴–2.4×10⁻¹⁰ — the τ/t reduction the dossier only cited is now verified twice independently.
3. **Attacked and found real defects** — the 37–39 ns wall is dead-code elimination (8.6 ns in the probe's own loop shape vs **418 ns** with `black_box`; a 27-deep serial sqrt chain cannot run in 37 ns); the spread trajectory is linear ×4/step, not the quadratic one quoted (true count 27–30); the 5-term series uses unnormalized e2 (measured coefficient −0.206 vs Carlson's −E₂/10 — harmless at full convergence, fatal for the early stop the "~6 iterations" claim needs); each step is three sqrts, not "adds + one isqrt". Honest per-channel gain: ~50× small-e to ~3×10³× on the tail.
4. **New domain edge** — at the true separatrix (1−m = 3.5×10⁻⁹) the shipped walk's own error grows to 6.7×10⁻⁷ while the closed form stays exact, and panels grow only as log(1/P): the explosion is in e, not m — the closed form *beats* the walk exactly where the walk's certificate stops holding.

The one experiment to gold: an honest Carlson kernel (E₂-normalized series, ~6-iteration stop, black_box) delivering φ/τ/t as a drop-in with its certified bound, priced on the leaver tail.
