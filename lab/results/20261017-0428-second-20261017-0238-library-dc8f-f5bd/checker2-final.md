Working...
Check complete. **Grade: gold** — written to `check2.md`, blind to checker 1.

**Basis:**
- **Reproduction.** The runner's regen hit every calibration bit-exactly (OFF 5,400 gs 334/136, 22,219/9,217; ARM 131/26, 6,580/1,382; thread-4 states identical; traced set 477; exact-tick probe 2.620×10⁻⁴°/1.181×10⁻³°). Independently of the author's script, I re-parsed the flown 8×10⁶ traces: max 14.6516° at 7,414,159 gs, crossings 1°/0.1°/10⁻²° at 3.566×10⁵/9.03×10⁴/2.55×10⁴ gs (k* +3.7/+1.7/−0.1), median t^2.01, belt max 2.2×10⁻³°, no saturation — every headline number confirmed. Patch audited: all probes env-gated, OFF path untouched.
- **Adversarial.** (1) The 1,900-gs record point that regen.sh omits: re-flown, exact (240/146, 11,111/3,624). (2) **N=4000, outside the tested range**: the curve is population-flat to 0.3% — the fence kill is not an N=1000 artifact. (3) Mechanism: the max-debt is a handful of in-situ bodies (id 163 owns 33/96 horizons; top-5 at 11–15°), so the "staircase" is max-switching. (4) Late-fit spread: the 2^10 edge bar is 44–108° across fit windows vs the quoted ~70° — the band's death survives every fit.
- **Predictions.** Timestamped 04:44, before both decisive traces (04:53/05:07); verdict-bearing ones held, misses honestly reported.
- **Novelty.** Both killed constants are published and live (nladder page's "~2^16 carried kicks / ~10⁷ game-s" fence and the universal 2^10–2^12 band); dc8f's page said "flight pending" — this run is that arbiter.

**Corrections made:** one line on the author's wiki page (the 10⁻³° crossing sits inside the trace's frame-jitter band; true k* nearer 2^−1.5 than 2^−2.4 — no verdict changes), plus a repair of a duplication my own edit introduced. Nothing else in the run folder touched; the tree was restored to pristine after the patch; my leftover flights killed. The RES control (resonance exclusion off) did not fit the window — disclosed in check2.md as the one unflown falsifier.
