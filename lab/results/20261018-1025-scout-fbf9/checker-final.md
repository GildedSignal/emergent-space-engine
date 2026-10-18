Working...
Check complete. `check.md` written with `Grade: silver`; the author's page corrected in place (3 `[checker]` marks); nothing else in the run folder touched; `regen.out` left byte-identical to my independent reproduction (sha256 match).

**Grade: silver** — real, reproduced, one named flight from gold.

**What held:**
- Reproduction is bit-exact: my scratch rerun of `toy.py` matches the stored `regen.out` hash-for-hash; every dossier number regenerates (slope-1 candidates 99/999/9999, flips 0, band 0.03–0.065 at n=10⁴ across seeds, controls B/C/D: 11/11 with 0 missed, negative control loses 2 and 5 events, standing 543.2).
- Predictions predate the code and dossier by mtime, amendments disclosed in-file; the class-D "0.27·n" prediction verifies independently (my mean-field 589 vs measured 543).
- My held-out cases all hold: anchor seed 31337 (armed 700, churn 0.75×/1.25×/2.0× across dv), hot belt e≈0.3 (band 0.045, flips 0), 64× kicks at dilute cells (flips 0 at margins +2/+8/+64).
- Novelty: it answers the wiki's open direction 1 (cd3b's "singular number"), and refutes its own first model (intra-cell due-space slack) — not a repetition of b509/fe6b.

**Two corrections (page fixed, mechanism untouched):**
1. **The n² off-centre constants are a ×10-per-decade slip.** My n=10⁵ flight — one decade outside the author's range — measures band **4.67**/body/kick vs the quoted 0.34. The mean-field law is exactly ×100 per decade (0.034→3.4), so the *shape* is confirmed (4.67 vs 3.4–6.8 mean-field) while the quoted constant is refuted by 14×; downstream, "cells may grow to ~10⁵" dies — the 0.34 µs/body level is crossed at n≈3–4×10⁴.
2. **The "~6 orders (≈197 → ≈2×10⁻⁴ cores)" headline doesn't reproduce under its own assumptions** (1 µs/arm, 1 kick/body/interval): 12.3 → 1.2×10⁻³ cores = **4 orders** in arm-evals (346→0.034). Still decisive for the row; the endpoints are a clock-convention muddle (toy "28141.5 game-s" vs SI 2.82×10⁷ s).

Also noted: the +2-interval band margin is quantum-kick-only (in-horizon dues walk 4.6 intervals at 2⁻¹⁷ — the margin must scale with kick size, consistent with b509), and "match to the digit" overstates a 0.030–0.065 seed spread.

**To gold:** one flight — the due-band per-kick rule on the shipped tier (`tier::arm_pair`'s callers) at 10⁴-occupancy cells, measuring re-arms/kick; Θ(n) would kill the toy's window model, with the standing/dwell class (control D) the place to look.
