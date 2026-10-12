Working...
Check complete. `check.md` written to the run folder; nothing else touched, scratch stayed in `/tmp/check-aac1`.

**Grade: silver.**

What I did and found:

**Reproduction** — `python3 probe.py` in a clean tree (patch.diff empty): all 380/182/182 orbit records, walk fractions (13.9% / 55.5% / 11.0%), the full gate sweeps (best recall 13.2% @ fpr 14.4%) and readout errors (4.89×10⁻⁴ / 9.67×10⁻⁴) came back **bit-identical** to the stored data. Timings within load noise (237 s vs 279 s, ratio 659× vs 687×). Memory stayed under budget.

**Predictions** — H1 and H2 held; P1/P2 failed and are honestly reported as the result. But `predictions.md` mtime (00:57) postdates the decisive data (00:55) — outcomes were appended, so pre-registration is unverifiable from file times; run.log is empty. Content reads genuine (failed thresholds, "missed the letter" admissions).

**Adversarial** — (1) 600-period re-runs: 6/8 walkers keep walking (to +172% dL), 2 flatten — the libration caveat is real for a minority; decisively, 2/4 *quiet* controls start walking, so the 14% churn is a 60-period lower bound and the gate kill is **stronger** than claimed. (2) High-e rosette: precession carried exactly (Δφ 4.5248 vs truth 4.5252), error bounded and non-compounding (cycle-1 = cycle-40). (3) The spatial gate they propose is testable on their own data (recall 1.00 @ fpr 0.51).

**Why silver, not gold** — the dossier misreports its own log in five places: the walker bins (corotation bin holds 8%, not 42% — the 42% belongs to [2.3,2.8]), H2's band ([1.8,2.8], not [1.3,2.3]), the OLR radius (3.37, not 3.57), the "2×10⁴×" label (that's per 60-period block; per period it's ~384×), and the undisclosed nfail=19 — exactly the de=0 circular row, a real compile edge at zero amplitude. The physics survives all of it; the prose doesn't. One experiment from gold: the churn census vs window with an angle-based libration classifier on a second potential — that turns the lower bound into the adoptable doll-edge design number.
