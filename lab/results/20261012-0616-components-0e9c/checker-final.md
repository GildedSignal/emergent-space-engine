Working...
Check complete. `check.md` written to `lab/results/20261012-0616-components-0e9c/` — **Grade: silver**.

**What held up:**
- Bit-identical reproduction in a clean tree (`python3 hlive.py`, 45.6 s, seed-fixed; only machine state differs). All headline arithmetic re-derived by hand (180.6 GB/h, crossovers 2.4–7.3×10⁻⁷, contacts 0.23 MB/h).
- Seed-stable (±1.2% at seed 777), sub-grid-refinement insensitive (+0.7%), approach law α = 1.079 matches 2-D kinetic theory within 1.6×, and the D³ big-body tail is real (measured q32 rate collapses 50× without >10-km bodies).
- Novel: zero H_live mentions in HISTORY.md; HANDOFF line 70 says "not measured yet"; the law.md quote is accurate.

**Why not gold:**
- Pre-registration was credible (P1/P3 stake the opposite of the result and are reported as failures), but 3 of 5 held-out predictions failed, including the headline magnitude — silver by the lab's own 1-October calibration.
- The physics bite: my event dump shows **zero** q32 events inside the pair's Hill radius (median b/r_t = 695). Every counted event is a distant conjunction — the neighbours'-moments regime the author's own P5 calls "no scars in principle" and the design's kick layer already owns. The 180 GB/h is an upper bound whose distance from the true scar rate is the open question; the unpublished 7-Oct `b-h-live` attempt (Grade: missing) had rejected this exact channel as beyond-tidal-radius artifact.
- Two number bugs: the drive statistic omits the events-per-pair rate (92× inflated, plus 12× seed instability), and the sub-resolution extrapolation is hardcoded to the 100-km scale (it adds 829/yr even to a belt with no body above 10 km — 42% of the headline).

**The gold experiment:** a signed-impulse ledger on the same stream — accumulate departures against the deterministic secular baseline and count quantum crossings of the *residual*. One run of the same code decides whether the belt inversion stands or the comfortable reading returns.
