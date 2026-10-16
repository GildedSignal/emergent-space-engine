Grade: silver

The claim: the named gold step flown — ES_STAGGER armed fails B13 catastrophically and changes all 13 ladder digests, killing the parent's adopt-as-birth-default direction. Reproduced bit-exact on a clean tree (patch applied by me): B13 armed 0/64, worst ΔE/ΔL 4.65e0, vs off 60/64 at 2.12e-2; 13/13 armed digests change with values bit-identical to the record; off == pristine; probe analysis identical; stagger_hash(1) = 0.56656. My adversarial bounded variant (quarter fraction, always inside the first step) still fails B13 at 2/64 — the kill is generic, not the unlucky 0.5666 draw. Not gold: the shipped regen.sh never rebuilds xtask (target filter), so the runner's own regen printed armed == off; the headline's shipped reproduction path is broken and its env-drop diagnosis is wrong.

## Reasons

**Reproduction (all first-hand, clean tree + `work/patch.diff`):**
- B13 off: `60/64, worst ΔE 2.12e-2` — matches the baseline and the author bit-for-digit. B13 armed (`env ES_STAGGER=1`): **`0/64, worst ΔE 4.65e0 ΔL 4.65e0`** — the dossier's headline, exact.
- `ladder_digest` off + armed re-run: **13/13 case digests change armed**; my outputs are byte-identical to the author's `digest/*.cut` files; 4 cases change kick counts (wave 32,537 → 31,973 etc.). Off-vs-pristine identity per regen (and by construction: unarmed → offset 0).
- `analyze.py` re-run on the probe files: output identical to `probe_analysis.txt`. Moon rates recomputed: seed 1 |armed−off|/|ref| = 2.92e-2 (max), both arms inside B14's 10% wherever off already is; seed 1's law-vs-reference gap 0.064 dominates; escape classes 3/3/3 across off/armed/reference — the dossier's Evidence 4 numbers all check.
- Mechanism verified: `xtask/src/behave/plane.rs:65-73` births the ship bare (`add_body_state(Kind::Ship, …)` + `start()`), so `plan_clock` takes the staggered path; the author's armed trace prints engagement 64/64; `stagger_hash(1)/2⁶⁴ = 0.566561` matches the trace's off/(2·half) exactly.
- `ES_STAGGER=0` == off exactly (arming edge correct). Engaged B14 armed: timeout 60.0 s — P3 holds engaged.

**Predictions:** `predictions.md` predates every decisive artifact (46 min vs 21/16/14 min). P2, P3 held; P4 held on class with an honest band miss (2.92e-2 vs 1e-2, disclosed); P1 and P5 failed as written, disclosed as failures, both in the kill direction; the kill criterion was pre-registered and fires on the measured number. Honest reporting throughout.

**Adversarial cases (mine):**
1. **Bounded stagger, outside the author's tested range** (the author's own named next falsifier, unflying it): `>>64` → `>>66` (fraction ≤ 0.25, first kick always inside the first step, never past the boundary). B13 armed: **2/64, worst 1.47e0**. The kill is not the 0.5666 draw nor my first suspicion (past-boundary placement) — it is first-order in any first-kick phase shift of an aperiodic assist, exactly as the dossier's mechanism sentence claims. This strengthens the kill to the configuration class.
2. `ES_STAGGER=0` == off (exact).
3. Engaged B14 armed: timeout (above).
4. **The regen artifact probed at the root:** touching `step.rs` and running regen.sh's build line compiles 0 times `xtask` — the `--example` target filter drops the `-p xtask` targets, so a warm target dir silently keeps a pre-stagger xtask. That is why the runner's regen (exit 0) printed `B13 armed: … 60/64 …` identical to off — through the `env ES_STAGGER=1` form, which cannot drop a variable. The record as shipped (regen.log, gates/B13_armed.txt) therefore contradicts the dossier's headline, and the author's "env-drop fluke" mechanism is refuted: no POSIX shell loses `VAR=1 cmd`'s assignment; a stale binary explains every instance, including the checker's armed-digest identity they cited.

**Novelty:** the standing `lab/wiki/nladder.md` has no B13-armed kill; docs/HISTORY.md has none; the parent's adoption direction (post-hoc first-kick mover as birth default) is now refuted, and the parent's frame record is preserved. The page folds the result in faithfully; I corrected its Refuted entry in place (env-drop → stale-xtask mechanism, plus the bounded-variant result).

**Goal fit:** board focus 1 (bodies 28 → 10⁹): a wrong birth default killed before it was wired, and the cure routed to the birth program (B18's domain), leaving single-birth scenes untouched. PRINCIPLES 9: "A failed experiment kills that configuration, never the method." PRINCIPLES 2: the gate judges behaviours, and the stagger changes the assist's error type (first-order), not its size.

**Why silver, not gold:** the physics is real, decisive and reproduced, but the run's own reproduction script does not regenerate its headline — on the runner's execution it printed the opposite verdict, silently, because regen.sh's build line never rebuilds xtask. Per this lab's own standard (taste log, 5 October: "results that the shipped code could not regenerate"; "a headline the log contradicts… the checker finds them, and the run loses its grade"), that is a record defect, not a physics one. The author observed the phenomenon (their "env-drop fluke"), misattributed it, and shipped a regen that reproduces the phenomenon.

## The one experiment that would make it gold

Fix regen.sh — build xtask without the example filter (a separate `cargo build --release -p xtask`) and add an engagement canary to the armed B13 step (e.g. run it under `PLANE_TRACE` and assert the kick-count change, or assert the armed ≠ off verdict line) — then re-fly regen end-to-end so the run's own regen.log prints the engaged `0/64`. Correct the dossier's env-drop diagnosis to the stale-xtask mechanism while at it.

## What the author missed

1. The build-target-filter/stale-binary mechanism: both their own fluke and the checker's armed-identity artifact are one cause, not two; because of it, `regen.sh` on any warm target dir is a coin flip on the armed verdict — the shipped record contradicts itself (gates/B13_armed.txt vs gates/B13_armed_trace.txt).
2. The bounded variant they named as "the natural next falsifier" was one 40-second build away: quarter fraction → 2/64, confirming the kill is first-order and generic; worth one line in the dossier's "what would make it wrong".
3. The flyby probe could never have shown the gate kill (its judgment points sit past the SOI exit, error scale ~1e-1, dominated by the law's own error) — only the gate itself could decide; their lens note gestures at this but does not state that the probe's design cannot answer the question the gate answered.
4. Minor: the wiki Refuted entry carried the unproven env-drop mechanism (corrected in place by me, with the bounded-variant result added).
