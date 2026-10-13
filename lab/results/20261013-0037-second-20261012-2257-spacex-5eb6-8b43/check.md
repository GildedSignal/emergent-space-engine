Grade: silver

**Abstract.** The second author closed 5eb6's named gap at its own parameters: a deadline-ordered due pass, a slack-subtracted fleet cap with a proximity park, and rekeys at the pull and at park-induced stalls. Everything reproduces byte-identically (starve one digest `7d1c6468…` across three arms at seed 11; the shipped gate passes; suite 58/58, 2 ignored; quiet 1.36 µs flat to 4×10⁵; fly/storm/fast/replay digests identical across arms). Not adoptable: on held-out seeds 2, 5, 9 and at threads 4, budgeted ≠ settled — deterministically, with equal kicks — where the shipped loop holds every case. The closure is scene-specific. No dossier.md was written; two of six predictions failed.

**Reasons.**

1. **Reproduction (clean tree at base `17ace3e6` + `work/patch.diff`).** `starve` both arms: byte-identical to the author's `starve-lazy.txt`/`starve-eager.txt`. `replay`, `storm`: byte-identical. `quiet` n=428: digest identical, timing 1.35 vs 1.36 µs (shared-machine noise). The gate test `work_per_frame_is_bounded_and_overflow_is_a_dip_not_a_hitch` passes on the patched tree; `regen.sh` exit 0 (runner) with all numbers matching the tee'd JSONs. The legacy arm is the shipped `advance` verbatim (diffed against base).

2. **Predictions** (file times: `predictions.md` ~1 h before the decisive outputs). P3 (digest identity across arms/schedules), P4 (quiet medians unchanged), P6 (no freeze) held. P1 half-failed: the author's own instrumentation prints the fleet past the presented `now` in **6 of 200 frames** (first at frame 23: fleet 23,068,671 vs now 22,020,433, ≤ 4.8 % ahead), so the stated mechanism — "the fleet's committed tick never passes the frame's presented time" — is false, and the escape hatch ("if the pull path commits past, the gate still fails") is false: work-ahead commits happened and the gate passed. P2 failed: stepped-settle **agreed** at seed 11 (reported in the wiki as "one better than shipped" without flagging the miss); it differs again at budget 1 and at 500 frames, so neither the prediction nor the bonus generalizes. P5 roughly held (fly rekeys 86–306 vs the predicted 1–219).

3. **Adversarial cases (mine; probe = the gate's own construction plus a stepped arm; the seed-11 control reproduces the author's digest exactly).**
   - Seeds 2, 5, 9 (3-event budget, rtf 5×10⁶, 200 frames, threads 1): **budgeted ≠ settled** on all three, deterministic across reruns. Seeds 2 and 9 do it with **zero** fleet-past-now frames — the fixed mechanism is not the binding one.
   - Threads 4, seed 11: all three digests differ. The shipped arm is thread-deterministic and holds.
   - Budget 1 (300 frames) and 500 frames at seed 11: budgeted == settled holds; stepped ≠ settled returns.
   - The legacy arm holds budgeted == settled on **all seven** cases. The patch's closure swaps the break's location rather than removing it.
   - The gate's other assertions (presented monotone and ≤ target, events ≤ budget + 64, no stall) hold in every case, both arms.
   - Mechanism on the failing seeds: the fleet lands exactly at the cut with equal kicks, encounters, contacts and lost; the budgeted arm carries +26–161 events and +26–156 slices — the battle's stop-point history leaks into the digest. The author's own seed-11 record has the same signature (985 vs 959 events, 347 vs 321 slices) with a lucky digest agreement.

4. **Novelty.** No `docs/HISTORY.md` entry; the published page's conflict block carries 5eb6's checker finding (the hole). The fix machinery (slack cap, park, pull/stall rekey) is new. Not a repetition.

5. **The page.** Corrected in place where it overstated: the "merge-ready"/"hole closed" headline and direction 1 now state the scene-specific closure and name the checker break; the "nothing resolves past what the frame can present" parenthetical now carries the measured 6-frame work-ahead dip; "one better than shipped" is marked as an accident of the case; the domain note, the run line and the legacy timing quote (15.8 µs → 29.6 ms, the regenerable record) were fixed; a duplicated direction number was repaired.

6. **Goal fit.** On-goal (frame-cost bottleneck; the fixed-tier deletion is the board's named lever). PRINCIPLES: "a failed expectation is not automatically a failed method: diagnose which one broke (H0183)" — the lazy deletion stands; this fix is insufficient. Against: "Measure before claiming" — the closure was measured on one scene (the gate's own seed) and claimed generally.

**Why silver, not gold:** the central generalization is falsified by held-out cases where shipped holds, so it cannot be adopted within one step — merging would regress the starvation digest invariant on 3 of 4 nearby seeds and at threads 4. **Why not lead:** the seed-11 closure is real, reproduced, and is exactly 5eb6's named experiment; the machinery is the standing scaffolding for the next run; and the falsification sharpens the topic's real question (the battle's stop-point invariant).

**The one experiment to gold:** make budgeted == settled scene-independent under sustained starvation. Sweep the three-arm starve across seeds (1–16) × threads (1, 4) × budgets (1, 3) — minutes of compute — and find the invariant that pins the battle's committed state at a cut independent of its slicing history (fingerprint: equal kicks with extra slice events). When it holds on all seeds, the gate generalizes and the tier deletion is genuinely merge-ready.

**What the author missed.**
- No `dossier.md` at all (`author-final.md` ends "Working…") — the README's own documented way to lose a grade; the wiki page carried the claims instead.
- The starvation case was tuned and reported on one seed (11, the gate's own) and one thread count; the fly suite's seeds (1/3/7) were never starved.
- The probe's own `fleet-past-now frames: 6 of 200` output was never reconciled with the "nothing resolves past what the frame can present" claim — a headline the log contradicts.
- The stepped-arm agreement was presented as a property while `predictions.md` expected the opposite.
- Minor: "legacy 15.6 µs → 30.1 ms" is not regenerable from the record (15.76 µs → 29.58 ms); the `ES_EAGER` arm rekeys twice per frame (`rekey_lazy` plus the legacy branch), so its "1,719–80,005 shipped" rekey counts overstate shipped ~2× (immaterial to the A/B timings at 428 bodies: 15.76 µs vs the published shipped ~15 µs).
