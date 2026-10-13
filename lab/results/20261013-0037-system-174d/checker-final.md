Working...
Check complete. **Grade: silver** — written to `lab/results/20261013-0037-system-174d/check.md`.

**What held (reproduced from a clean tree, patch applied, regen.sh):**
- Demand mode **bit-identical**: worst frames 42/579/1,036 (the published control), cadence formula 2,283/2,293 kicks, tide/burn 2.570×10⁻¹² / 2.819×10⁻¹¹ / 1.334×10⁻⁹, coast control 19/19.
- The replan-storm guess is refuted — verified in source (`decide` clears the plan, plans one kick; no refit) and behaviorally under key re-assertion.
- Predictions genuinely pre-registered (mtime 00:47 vs dossier 00:55; P2's letter *failed* and was reported as failed).

**What cost gold:** the author's own regen output contains `paced L15 … would mint ~26413 events` against ~990 burst items — my attacks confirm it robustly (28,448 at seed 7; 31,284 over 8 s; 47 plunge kicks carry 100% of the tide sum at ~5–7×10¹¹ quanta each). The headline "~0–2 field events" is demand-mode/L8–L12 only; at the paced L15 regime that owns the sweep's worst stutter, the fixed-granularity counterfactual inverts ~28×. The deletion there hinges on a regime-scaled tide cadence (~5×10¹¹/event, what today's kicks already deliver) that the run neither derives nor measures. Also: seed 7 widens the ratio to 10⁸–10¹⁰ (stated as 10⁹–10¹⁰).

**Page corrections (in place, attributed):** paced-L15 counterfactual added to current-best, refuted and direction 2 with demand scoping; dropped append-only run line `ae40` restored; undisclosed id edit `464c`→ reverted to committed `469c`.

**Gold path:** one experiment — derive/measure the plunge tide's per-event budget and re-price with a regime-scaled carry; then the claim holds at every level or carries an honest bound.

Worktree restored clean outside the run folder; nothing committed.
