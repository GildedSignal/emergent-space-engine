Working...
Check complete. `check2.md` written to the run folder; nothing else touched, no git operations.

## Verdict: gold

**Reproduced:** `hlive_probe.py` rerun in a clean copy under a 2 GB cap — all six belt lines bit-identical (event counts, rates, slopes), `hlive.json` identical modulo wall times; `analyze.py` regenerates every headline number (6.33×10³ encounters/body/orbit at 10⁹, contacts 2.79×10⁻², close-in walls 17.6/8.8 h at 64/128 bits, 1.5-AU wall ≥1445 h). `predictions.md` (16:13) precedes all decisive artifacts (16:34–16:48).

**Adversarial cases run:**
- **A1 — P1 beyond the sample:** physical bound Δv ≤ 2·v_rel (no impulse approximation) gives max |ΔE| ≈ 4×10⁻² of the coarsest quantum at contact range over *all* approach speeds — ship–ship gravity is sub-quantum even in the co-orbital regime the sim never sampled.
- **A2 — the extrapolation:** α=1 is independently corroborated by a 2D mean-field estimate (3.4×10⁻² vs 2.8×10⁻²); the shipped data's own slope (0.59–0.64) would only shorten the wall.
- **A4 — conventions:** dedupe window 0.3→2.0 shifts the rate 0.06%; fresh seed 1.6%.

**Blemishes recorded (none load-bearing):** `kicks.json` was built from run1's pre-fix event set and its sweep script wasn't shipped, so the floor-limited rows don't regenerate (12.57→12.89 bits) — though the ship row, the claim that matters, regenerates exactly; the α=1.25 branch has an arithmetic slip (1.3×10⁻³ / 22×, not 3×10⁻⁴ / 90×); the [1.0, 1.25] bracket isn't what the shipped data shows. The failed P3 (cold-belt anchor) was pre-registered, disclosed, and correctly quarantined to the convention — the flyby-regime numbers carry the claims.
