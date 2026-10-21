Working...
Check complete. `Grade: silver` written to `lab/results/20261021-1346-library-1fd7/check.md`, and the author's proposed wiki page corrected in place (14 current-best lines, 209 total — within budget).

**What I did:**

1. **Reproduced** — `regen.sh` exit 0 (~10 s), quotes 5/5 byte-identical against a fresh 4,590-highlight fetch, every input constant traced to its wiki page (nladder, kick-cadence/cbe6/7076, b30b, b57f, 8ffc), and both code citations verified in shipped source: `ext.rs:146` takes `kicks_log2` globally from `ctx.cfg` (step.rs:630/558), so "policy change, not algorithm" holds.

2. **Found the decisive flaw (adversarial recomposition).** The script divides the ledger's 12.75 h/era kick row by a headroom R built from λ_ship = 4.889e-5 — but those anchors never multiply back: 4.889e-5 × 27.9k gs × 45.5 µs × 10⁹ = **17.2 h/era, not 12.75**. The ledger's own rate is 3.6e-5 (1.01 kicks/B/era, matching the 0a46 census 1.09–1.12 and b30b's 3.33–3.50e-5); the board's 9,000/orbit anchor is the *two-comb* count (2.01 ev/B/era, 8ffc), ~2× the kick-only. The anchor-free floor cost (8/S)·era·N·payload gives **0.78× of budget (margin 1.3×)** at the page-measured payload — the author's 0.575×/1.74×/3.41-yr/1.57%/15× set is the same formula at an implied 33.6 µs/kick that contradicts the 45.5 µs the dossier itself cites. P2's registered bar (≤0.6×) **fails**; the row still closes (0.58–0.78× over the defensible payload range); P5's 173–373× landing survives unchanged.

3. **Two more adversarial cases:** the belt-edge S sweep (2 AU → S = 3.7 yr < corrected S_bar 4.6 yr: closure is outer-belt-only, not belt-wide), and the 77-d forcing — which per cf45 is the *shipped plane's own* P_D, not a hypothetical: on the plane as-is the row stays 15–20× over at the floor.

4. **Novelty:** the ~10³ headroom and census-as-missing-half are already cbe6's on the page (today, credited); new here are the budget landing, the two bars, and P7 — corrected to payload-conditional (f_fine ≤ 0.6–1.6%, S ≥ 3.4–4.6 yr) since a census passing the author's frozen bars could still leave the row ~1.7× over.

Silver, not gold: reproduced and real, but zero flights, the frozen bars (the deliverable) were miscalibrated 1.35× by one anchor mix, and one registered prediction fails. The gold-making experiment is named: the census/legality/payload flight on cbe6's harness with the composition re-derived anchor-free.
