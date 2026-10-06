Working...
Check complete. `check.md` written: **Grade: silver**.

**What I did (35 min):**
- **Reproduced** from the dossier's commands on a clean 70f27a9 tree with `work/patch.diff` applied: seed 6 (player 47.74 / drain 46.60 / n=31, digest `b541ca2a` bit-identical, hitches [8,2,1] identical), seed 5 (`1bc35aa5`), e2b (n=64, 93 vs 92 hitches, `a73ef0f4`). All 40 stored JSONs match the dossier table.
- **Verified the mechanism in the shipped code**: budget checked only between items (universe.rs:811), player's `light_distance`=0 (:463), pending hand-out deadline = tick + root position (:468–482), player branch drains all earlier-tick hand-outs in one item (:577). Plane.md foundation 7's "nothing takes an unbounded synchronous claim" is exactly what breaks.
- **Adversarial**: seed 7 (outside their sweep — no giant, player 6.96 ms over budget via pull); clean-tree rebuild → `a73ef0f4` with no new JSON fields (patch measurement-only); 110c3e0 rebuild → `a0746ad1` a third time (matches their B2, kicks 9712); CSV giant frames 127/156 and 130/152, never within 3 frames of a burn.
- **Novelty**: hitch class known (H0213); new is the item naming, the queue-jump mechanism, the schedule-dependent batch size at fixed digest, the dial→drain growth, the paced-factor refutation (1.12×).

**Why silver, not gold:** reproduced and code-verified, but P1/P2/P5 half-failed (honestly scored), the worst-frame gain (34–51 → ≲12 ms) is projected — no fix was implemented — and the pull path (over budget on 6/6 seeds) is unexamined. Gold experiment: apply fix (1) (one line, outcome-invariant by the shipped comment), rerun the sweep, show ≲12 ms with unchanged digests.

**Caught the author missing:** their A control ran a stale binary (A-clean.json contains `engine_item_max`, impossible from the stashed tree — `| tail -1` hid the build failure; only A2 is valid); and their kicks/opens evidence for the cross-machine world split is invalid — their own B vs B2 differ 149 kicks at the same digest, so kick counts are schedule-dependent; only the digest split carries that claim. Tree restored to 70f27a9 clean, shared binary rebuilt, no commits.
