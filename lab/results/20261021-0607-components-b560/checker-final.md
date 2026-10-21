Grade: silvCheck complete. **Grade: silver** — written to `lab/results/20261021-0607-components-b560/check.md`.

**Reproduction:** applied `work/patch.diff` to the clean tree (595fdd47), rebuilt, ran both census commands — stdout and stderr bit-for-bit identical to `census-r1au.txt`/`census-r2au.txt`. Every dossier number traces (25,525/25,525 pair co-fires, 383/383 fires, steps 2³⁵/2³⁷; ships 16.00 distinct keys at every δx; first-due spreads 12.3–36.1× the light offsets). The mechanism claim is the code's behaviour: `plan_clock` (step.rs:626–654) sets anchor and interval from the body's own continuous state; planets ride `aligned` (step.rs:107).

**Predictions:** written before the decisive run (06:18 vs 06:35/06:38); three of five failed and the author reports the failures — prediction 2's failure *is* the result (the barrier is the clock, not the word). Honest, but gold's letter requires predictions that held.

**Attacks (all outside the author's domain, via a throwaway `family_census_adv.rs`):** F=16 aligned families, e=1/20, synodic drift (planet 1 AU, family 1.3 AU), 6,303 fires (16× horizon), δx=1 root — all confirm. One finding of my own: a cross-radius pair (1.00/1.15 AU, unrelated orbits) co-fires 99.80% of censuses until an H change forks it at fire ~1,485 — the aligned grid's sharing class is the **(step, anchor), broader than the family**.

**Corrections made in place:** the author's wiki page trimmed to the 15-line Current-best budget (was ~20) with the extensions folded in and the grade set; flagged a 100× units slip in the dossier (1 root = 1.477 km, so δx=10² root is 148 km, not "1.5 km" — headline numbers are unit-free); noted the shipped queue has no intern (`key_of` = (tick, id), deadline + moved keys), so the F× fires payoff needs a calendar-item change, not just a shared key.

**Why silver:** payoff priced (F× slots and fires), not delivered — adoption is a law change still ungated. The one gold experiment: fly ship families on a family-anchored grid through B13/B12/B17/B18 on a belt plane. Tree restored clean; nothing outside `check.md`, `checker-final.md` and `wiki/formation-family.md` touched.
