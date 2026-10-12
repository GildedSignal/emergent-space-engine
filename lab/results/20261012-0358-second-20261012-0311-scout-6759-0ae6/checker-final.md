Working...
Check complete. **`check.md` written: Grade gold.**

**What I did** (45-min budget, all processes < 1 GB):

- **Reproduced every dossier command** in a clean scratch dir, seed 6759: `evolve` bit-exact against all scout anchors (scar words to 6 decimals; 256-kick entropy 51.440877076); `smoke` recovery 6.3×10⁻¹⁵; `control` payload ≡ 0; `analyze` → `reabs-results.json` **byte-identical**; `ss`, `B`, `pk` identical except `wall_s`.
- **Verified the unit correction**: Q_A = 6.6846×10⁻⁸ AU = 10.00002 km — the scout's "1 km" label was wrong; the correction strengthens the kill.
- **Three adversarial cases of my own**: (1) seed 4242 → P3 steady sup 56.18 (verdict unchanged, not seed luck); (2) a **per-epoch oracle** — P1's basis refit at every epoch of orbits 9–16 on the total deviation, strictly dominating any cadence — still leaves W = 71.9–74.0, so the miss is structural to the basis, not staleness; (3) arithmetic spot-checks (budget 34.36 bits, drift 1.11×10⁵ km/orbit, valve numbers).
- **Novelty**: no HISTORY entry covers scar reabsorption; H0209/H0212's belt results are the smooth unperturbed regime — this is the complementary kicked-belt steady state, and the checker-named decisive experiment.

**Why gold, not silver**: the premise "exact belt scars for 10⁹ bodies in 4 GiB at the law's quanta at some cadence" is killed across four program classes plus two oracle accountings, with ≥ 10-bit margins under both instruments; the two falsified predictions (Q1, Q3) missed in the direction that *widens* the kill — pre-registration working, not tuning; adoption is one informational step (B18 gate at per-population quanta; belt-store constants k = 1, c* = 256).

**Named in the check**: "best regenerable" overstates P3 (true-phase anchor; strictly regenerable best is P2 at 75.3); c* = 256 is W-instrument-dependent (entropy coding could put it near 64); the 4 GiB belt-share budget is inherited, not re-derived; the smoke flag's threshold is miscalibrated. None overturn the verdict.
