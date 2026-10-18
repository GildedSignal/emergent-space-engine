Working...
Check complete. Summary of the verdict:

**Grade: gold** — `lab/results/20261016-1319-dynamics-e846/check.md` written.

**Reproduced.** The runner's `regen.sh` regenerated every dossier number; my independent recount of the JSONLs agrees on all (47 dead, 100% `planet_kick`, 19/47 vs 20/97 truths crossing, 15/47 at the death conjunction, 144/144 necks open, controls green).

**Independently confirmed with my own harness** (scipy DOP853 CRTBP, uniform-sphere planet interior — not the judge's code):
- Validated against the author's control IC to every printed digit; my only false alarm during checking (huge early-window distances) was a bug in my own IC scaling, caught by that control.
- Death-epoch window minima match the author's oracle to 4 decimals — including **0.0928 Rp at 11.89 P: the truth crossing the disk at exactly the conjunction where the plane kills**, the claim's strongest instance.
- Dead-set class: my 24/47 cross vs author's 19/47 — chaos scatter, same class; kept-set median 3676 Rp separates unambiguously.
- P/256 floors 26–36 Rp vs resolved 0.09–2.7 Rp on my own integrations: the b9be instrument could never have seen a crossing.
- **Outside the tested domain (μ = 1e-2)**: 45/144 truths cross — the transport channel stays thick; the class reading is not a μ = 1e-3 artifact.
- The author's unmeasured kill radius closed by wiring: `plane.rs:60` passes exactly `JUPITER.planet_radius` (4.84e4) through dyadic scales.

**Deviations recorded (none material):** the dossier's "J walk tiny" is true on the P/8 series but hides 2–4.3% death-tick J readings for 3/47 ships; q-at-death max is 1120, not 1088; `aggregate.py:33` prints `min(j_max)`. I corrected the wiki page in place for the two overstatements. The 47-vs-48 driver discrepancy is unverifiable in this checkout (b9be's branch absent) and stays a priced lead.

**Gold rationale:** pre-registered predictions were genuinely held out — P2's decisive failure (0% terminals vs ≥90% predicted) *is* the finding, honestly reported; the run refutes a recorded premise, decides the page's open direction 4, and adopts in one step (gate wording only, counters are print-parity).
