Check complCheck complete. **Grade: silver** — full report in `lab/results/20261018-0035-second-20261017-2330-scout-be13-cf6f/check2.md`.

**Reproduction (exact).** Clean rerun of `confirm2.py` + `bugdemo.py` (6:44 wall, 1.24 GB peak, under the cap) matches the shipped record digit-for-digit — third agreeing record. Every dossier number I checked (D1–D5, controls, be13's regenerated geom row, the 148599-vs-221937 bugdemo) is as claimed.

**The core claim survived every attack**, including two outside the author's tested range: a new scene shape (35% bulge + disc: COM wins, inner p90 0.00061 vs geom 0.00498) and N = 10⁷ (256×1024 PASS, COM 0.00126/0.00324).

**Two shipped overstatements found and corrected on the page:**
1. **"No m-truncation passes p90 / the tail is white shot-noise" is refuted** — extending the author's own sweep past m ≤ 8: error decays monotonically (signal, not noise); **COM m ≤ 64 passes med AND p90 on 3 seeds and at N = 10⁷** (m ≤ 96 with headroom; even geom passes at m ≈ 96). This opens an unmeasured ~5–8× bytes lever (coefficient store, 129–193 of 1024 numbers per ring) — the named gold experiment.
2. **"COM beats geom at every grid"** — the 1.05× coarsest-grid margin is within seed noise: geom wins 1 of 6 fresh seeds at 64×256 and at N = 10⁷. Holds at every grid ≥ 128×512.

**Caveats recorded:** predictions.md's only mtime is 97 s *after* the timed run ended (pre-registration unverifiable; the honest m ≤ 8 miss argues genuineness); the inversion conclusion was already on the live page from be13's checker, so this run's own delta is the h³ order, the m ≤ 8 kill, the clusters-128×512 pass, and the shipped controls — confirmation-with-instrumentation, not a 10×/delete/premise-kill move.
