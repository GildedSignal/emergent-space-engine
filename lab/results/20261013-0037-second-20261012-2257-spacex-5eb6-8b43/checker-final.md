Working...
Check complete. `check.md` written, the author's page corrected, tree restored to base `17ace3e6` (only `lab/results/` untracked, as found; no commits made).

## Verdict: silver — the fix is real at the gate's own scene, and falsified one seed away

**Reproduced (clean tree + `work/patch.diff`):** everything. `starve` both arms byte-identical (`7d1c6468…` one digest across budgeted/stepped/settled at seed 11; eager `c7acf6…`/`34c8…` exactly as recorded), `replay`/`storm` byte-identical, `quiet` digest identical (1.35 vs 1.36 µs = machine noise), the shipped gate test passes on the patched tree, suite 58/58. The legacy arm is the shipped `advance` verbatim (diffed against base).

**The finding that costs it gold:** my adversarial cases (probe = the gate's own construction; seed-11 control matches the author exactly) —

| case | lazy (patched) | legacy (shipped) |
|---|---|---|
| seeds 2, 5, 9 · b3 · t1 | **budgeted ≠ settled**, deterministic (seeds 2/9 with *zero* fleet-past-now frames) | holds |
| seed 11 · threads 4 | **all three digests differ** | holds, thread-deterministic |
| seed 11 · budget 1 / 500 frames | budgeted == settled; stepped ≠ settled returns | holds |

Mechanism: the fleet lands at the cut with equal kicks/encounters/contacts, but the budgeted arm carries +26–161 events in battle slices — stop-point history leaks into the digest. The author's own seed-11 record (985 vs 959 events) is the same signature with a lucky agreement. Seeds 2/9 break *without* any fleet-past-now frame, so the fixed mechanism isn't the binding one.

**Also recorded:** no `dossier.md` (author-final ends "Working…"); P1's mechanism and P2 of the predictions failed — the probe's own `fleet-past-now: 6 of 200` contradicted the "nothing resolves past what the frame can present" claim, and the stepped-arm agreement reported as "one better than shipped" was predicted to differ. Page corrected in place: merge-ready → scene-specific, direction 1 rewritten to "do not merge as-is; find the stop-point invariant", run line and timing quote fixed. The named experiment to gold: make `budgeted == settled` scene-independent (sweep seeds × threads × budgets, ~minutes), pinning the battle's committed state against its slicing history.
