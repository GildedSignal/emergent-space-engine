Working...
Check complete. Verdict: **`Grade: gold`**, written to `lab/results/20261011-1600-fermi-13ad/check.md` (the only file I changed; scratch work in `/tmp/fermi13ad-check`).

**What I did:**

1. **Reproduced exactly** — `hlive_probe.py` rerun in a clean copy (237.5 s): all six configurations match the author's `hlive.json`/`run2.out` bit-for-bit (rate/N = 6.25/6.33/6.33×10⁻⁶, exponent 1.004); `analyze.py` regenerates every headline number including the 8.8–17.6 h contact wall and the disclosed r8-anchor failure.

2. **Verified the headline (P1) independently** — the stored `kicks.json` came from the superseded first-run sample (file times prove it: 16:42 vs the v2 probe at 16:44; n=6092 vs 7606 on the clean npy), so I re-measured it on the clean sample under five quantum conventions: ship–ship gravity = 0.000 bits, sub-quantum fraction 1.0 everywhere, walk to one quantum ≥ 2.2×10⁸ orbits even under the most adversarial convention. Channel A is dead.

3. **Attacked the contact extrapolation** — my strongest finding: the recorded impact parameter b systematically underestimates the true minimum distance at small b (median ratio 1.13 at b~10⁻⁴ growing to 65× at 10⁻⁸), so the author's own b-table slope (0.65) contradicts their α∈[1.0,1.25] bracket. But re-propagating all 6,783 events (machinery self-checked to 4×10⁻¹⁵) gives a **true d_min slope of 0.88–1.0** and a contact wall of 3–22 h — bracketing their 9–18 h. The conclusion survives; the derivation was lucky.

4. **Novelty** — first measurement of the board's "not measured yet" H_live item; nothing equivalent in HISTORY.md or docs.

**Why gold despite real defects:** the load-bearing claims all reproduce or survive independent re-measurement; P1 was a pre-registered point prediction confirmed with 4–8 orders of margin; the work deletes the encounter-skin constraint for ships and names the allocator's signal. The defects — stale kick table, unshipped sweep, unstated quantum convention, wrong α=1.25 arithmetic (22×, not 90×), "≥9 orders" overstatement at finest quanta — are all secondary and listed precisely in the check so the integrator isn't misled by the exact figures.
