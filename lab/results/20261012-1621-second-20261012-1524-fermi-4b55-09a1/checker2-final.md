Done — `c**Grade: gold** — `check2.md` written; author's wiki page needed no corrections (every checkable line matches evidence, including the hot-belt caveat, which I re-derived independently).

**What I did as the blind second checker:**

- **Reproduced** in a clean `/tmp` copy: `regen.sh` exit 0 (238 s, <200 MB), all four stored artifacts diff clean. Verified the sign bug analytically — residual `λ_body − n_p·t` has derivative `−dn`, so `orig/crosscheck.py:139`'s `t −= dth/dn` diverges and the one-line `+=` fix converges (0.91× brute force).
- **Predictions**: file times in the right order; the genuinely held-out controls (dt halvings +0.7%/+0.3%, seed 43 +2.2%, 60/200-orbit windows ±0.5%) all held; the corrected 1.31×10⁻² lands inside the original run's pre-registered P3 range. Re-derived every 10⁹-table row analytically — all match; the "460×" decomposition is exact (36.5/0.0798 = 457×; sign bug 2.19×).
- **Four adversarial regimes**, all outside the author's range: hot belt σ_e=0.05 (truth ×1.32, dt-converged; Newton degrades to 0.34×, anchor to 4.0× — only the brute-force instrument carries, confirming the page); μ_p=10⁻² (×4.76, superlinear in R_SOI — the census matters by mass, not count); planet at the belt edge (0.60×, instrument stable); N×5 bodies (1.002× — the density-independence the 10⁹ extrapolation rests on).

**Gold rationale**: first measured H_live on the `memory-h-live` bottleneck (HANDOFF: "not measured yet"), shows the silver premise wrong (rebind headline 457× high, player "nil" → co-dominant), redirects the 8 GB question to mixed entropy, adoptable in one step with no engine change.

**Author's misses** (recorded in check2.md): ambiguous "460×" phrasing (total-headline ratio is 2,014×); unperturbed-Kepler transit counting with O(1) deflection unquantified; "×k secondaries" asserted not tested; the inherited "~5 orders" refuted-line not regenerable from this record; ~2% t=0 episode inflation.
