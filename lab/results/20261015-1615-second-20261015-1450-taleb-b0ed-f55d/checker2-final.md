Working...
**Grade: gold** — written to `check2.md`, with the author's wiki page corrected in place (a checker-2 bracket; no existing lines reworded).

**What I did:**
- **Reproduced** in a clean tree from `work/patch.diff`: `regen.sh` regenerates the full table; I re-flew two arms — every canonical counter and digest identical (`d3542eea…`; only timings differ on the shared box). Instrumentation verified env-gated, default-off. Tree restored clean afterward.
- **Six adversarial probes beyond the author's domain**, all digest-identical:
  - **N=250k** (out of range): ratio **7.832** at 0.65×N, **exactly 1.000** with 0 evictions at 1.31×N, bill = N+30,111 — the knee-scales-with-N law holds at a fourth N.
  - **cap 120,000 (1.2×N)**, the transition neither the author nor the razor flew: ratio 1.000, hits exactly global — falsifies "7.0–8.5 at every cap below 1.31×N", and cap 130,186 = bill−1 also serves everything, so the mint-bill razor is the no-eviction threshold, not the functional knee (which lies in (0.65×N, 1.2×N]).
  - **Doubled cut** at cap 65,536: ratio **72.5** (vs 6.95 at 20k), wall +77% — the band and the tax are matched-cut constants; the extra-promotions = hit-deficit identity stays exact (11,460,990 = 11,460,990).
  - **Seed 5**, **ONCE at the knee** (1.000 — degenerates to FIFO without pressure, mechanism-consistent), **who-decomposition at 2×10⁵** (mints 98.4% `apply`'s position walk, ~0 scan; ~85% of sampled hits the encounter scan — the share keeps growing with N).
- **Novelty/goal fit:** nothing in HISTORY; this closes b0ed's checker-named gold experiment (knee localization+scaling, call-site mechanism, admission kill are all new); moves the board's #1 bottleneck and hands over a real decision (no constant cap; the deletion is the phase-neighbour certificate).

Two secondary constants in the headline die under my probes; the law, mechanism, admission kill and handover decision survive all of them — hence gold, with the page corrected where it overstated.
