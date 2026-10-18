Working...
Check complete — `check.md` written with **Grade: gold**, one correction applied to the proposed wiki page.

**What I did:**

1. **Reproduced** — `regen.sh` exit 0 in 30 s; every deterministic line byte-identical across the author's `run-log.txt`, the runner's `regen.log`, and my own execution (only the price arm varies, 6.8–10.9 ms — order-of-magnitude as claimed). The comparison baselines (`eclipse_parity_orig.py`, `-out-orig.json`) byte-match the published 22d1 commit, so the PG "unchanged parts" check (violations: []) and the artifact column are against genuine baselines. `patch.diff` empty.

2. **Re-derived the physics from scratch** — all four onset closed forms (W1 = −R/β, W3 = d − R√(1+β²)/β, W2 = √(d²+R²) − R/β, W2p = d − R/β), the W3 arc root-interval, the general oblique predicate (confirming the frame-time-distance anchoring), and the 1/γ mechanism. My own solver confirms the author's refined onsets to ≤1e-4 s and the closed forms to my grid floor.

3. **Attacked outside the domain** — 11 new cells through the author's own code: transverse β 0.99/0.999 (the game flies to 0.9999; the run stopped at 0.9), oblique 20°/70°/135° including approaching vₓ<0 at β 0.9, sign-flipped v. **0 mismatched rows everywhere**; Jaccard = 0.1411 at 10R β0.99 (√(1−β²) to 4 digits); sprite = γd exact at every β. The mechanism extends; nothing broke. Domain facts recorded: the W2 onset error sups at 0.650 s at β→1/2R (the 0.62 bar is correctly scoped β≤0.9), egress has the mirrored bounded form (−0.334 s at 10R β0.9, verified), and √(1−β²) is a transverse-only bar — I added that qualifier to the frozen rung bar in the wiki page, since oblique Jaccards run 0.53–0.99 and a rung implementer would mis-fail those cells.

4. **Record verified** — predictions pre-registered 19 min before the decisive run; the PB sub-clause refutation and PD's disclosed certificate fixes are honest and are physics (I confirmed the one-sided terms are the grazing-point-on-segment conditions), not tuning. Novelty: this is 22d1's checker-named one-experiment path to gold, completed — not a repetition; the checker-supplied-numbers defect that held 22d1 at silver is gone.

**Verdict:** the kill of every cheap occlusion wiring now stands on corrected, regenerable, per-row-exact physics, with freezable exact negative-control bars — gold, adoptable at one exact quadratic per row per occluder.
