Grade: silver

**Abstract.** The birth rail's missing two-thirds is `Universe::start`'s tick-0 replan+apply pass, not the compile path: at the ladder's true belt keys, build costs 42–44 µs/body on this box — draw+`add_body` 9.3–9.7 µs (22–24%), the plan pass 32.5–33.5 µs (76–78%) — flat from 10⁴ to 3×10⁵, digest-identical to pristine. Reproduced: regen exit 0 plus my own flights — seed 1 (42.0–42.5), held-out seed 7 (plan 35.0, 78%), 5×10⁵ beyond range (plan 34.2, RSS 1.17 GB), digests md5-equal. Re-prices the 10⁹ fill (~8 M1-core-hours, ~6 skippable by a program-store birth) and lazy birth (3.3× if promote-then-plan). Cost: nothing to merge; one M1 ratio re-measure. Defect: c4d3's 9.2 µs is a lab i7-4790 number, not M1.

## Reproduction

- The runner's regen.sh (fixed in the fix phase: a wrong repo-root climb and a digest diff that counted the wall-time column) ran end-to-end, exit 0; regen.log holds the full tables. The dossier's numbers regenerate: slope 42.7–43.4 (dossier 41.9–44.2), draw+add 9.60–9.70 (9.31–9.68), plan 32.88–33.63 (32.46–33.48), small terms ≤ 0.08 µs/body.
- I applied work/patch.diff myself, rebuilt, and re-flew: seed 1 at 10⁵ 42.0 µs/body (ES off: 42.5 — the instrument is inert); **held-out seed 7, registered in predictions.md and never flown by the author**: slope 45.1, plan 35.0 (78%), draw+add 9.8 — the split holds on the author's own held-out arm.
- **Beyond the author's domain** (rule 3): N = 5×10⁵ (author topped at 3×10⁵): plan 34.2 µs/body, draw+add 9.65, slope 46.0, peak RSS 1.17 GB. No cache cliff, exponent still ≈ 1; the claim's domain extends at least to 5×10⁵.
- Digest identity under my own hands: my `ladder_digest` run (13 cases × 4 schedules, ES off), wall-time column stripped, md5-equals the record's `ld_patched.txt` (`d8593cc4…`).
- Attribution verified in code: `step::replan` is documented "plan a body's first interval at its creation" (step.rs:867); `add_body` does not call it; `start()` runs replan+apply over every body at tick 0 (universe.rs). `ladder_ship`'s belt is exactly the claimed mix (a uniform in [2,3) AU, e re-drawn above 0.4; scenario.rs:338).
- The anchor is real: `artifacts/runs/nladder/ladder.txt` — "build 28-31 us a body … exponent 1.01", and break 4 prices 10⁷ promotions at "~250 s of compiles", i.e. the standing record did read birth CPU as compile CPU.

## Predictions

predictions.md (mtime 00:28) precedes the patch, the dossier and the wiki page (all 00:42). P1 held (41.9–44.2 inside 40–90, +5% over 30× against ±30%); P2 held sharply (22–24% vs ≤35, 76–78% vs ≥40, 0.2% vs ≤10); P4's arithmetic checks (42 µs × 10⁹ = 11.7 h this box; 28–31 µs → ~8 M1-core-hours, ~6 the plan pass). Kill criteria did not fire. Limitation: the author's own run logs were overwritten by regen's outputs, so the pre-registration order rests on file mtimes, not log order; the wide registered bands, the kill criteria and the never-flown seed-7 arm (held, by me) argue the registration was genuine. P3's kick-side comparator (the "0.3–0.4× one wave kick" clause) is not regenerable from the record — no command measures the kick side; the registered 0.3–3× band held regardless.

## Novelty

The nladder page (92 runs), HISTORY and ladder.txt contain no split of the build cost; c4d3 timed only `add_body`. The ladder's break-4 parenthetical already sketched that a lazy birth skips the first plan ("a lazy birth against a snapshot of those is bit for bit") — the idea existed, unpriced; this run supplies the missing price and corrects the compile-dominated reading. That is new and on-focus (board item 1, ladder break 4, shipped code at 10³–10⁶).

## Goal fit

Re-prices two standing decisions and corrects a premise: "Compute only surprises" (a body nothing touches is planned for nothing) and "Store the generator, not the generated" — the plan pass is the generated part. Measurement only; nothing to merge.

## Why silver, not gold

- **The portable number is single-box.** The adoption arithmetic (~6 of ~8 M1-core-hours) needs the 3.4× plan/add ratio to transfer to the M1. The dossier's offered cross-box corroboration is wrong: **c4d3's 9.2 µs was measured on a lab Linux i7-4790** (its dossier names the machine: "Linux x86 i7-4790"), not "on the M1". So the "integer compile side is near box-invariant" inference is unfounded; what stands is same-box-class agreement across two different harnesses (still real corroboration of the 9.x µs, and the 5 October lesson about shared harnesses is answered — the instruments differ). The dossier itself flags the M1 re-measure as required before quoting the 10⁹ arithmetic; until then the headline consequence is conditional.
- **The interior was left unattributed** (the dossier's own "what would make it wrong" branch). I measured it (temporary sub-instrumentation, reverted): at 10⁵ the pass is **`step::replan` 28.2 µs/body vs `apply` 4.2 (87/13)** — the floor-vs-deletable question is now localized to `plan_interval`'s search, but unanswered.

**The one experiment to gold:** the M1 re-measure of the split at one N (the integrator's, minutes): plan/add within ~±30% of 3.4× makes the 10⁹ re-pricing and the premise correction fully portable — gold as it stands. (The interior attribution changes the lever's size, not the claim.)

## What the author missed

1. c4d3's machine (its dossier states it) — the "on the M1" anchor and the box-invariance aside; corrected in the page.
2. The registered held-out seed 7 arm was never flown (only seed 3); I flew it — it holds.
3. The plan pass's interior (87/13 replan/apply, my probe) — the named next experiment is now one search to read, not a pass to split.
4. P3's comparator is unmeasured in the record; a future pricing run should include the kick arm it normalises against.
5. regen.sh overwrote the author's own logs (`run_main.log`, `run_seed3.log`), weakening the pre-registration audit; future runs should tee regen outputs to distinct names.
