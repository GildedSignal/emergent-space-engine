Working...
**Grade: gold** — written to `check.md` as the second, blind check.

What I verified in the 45-minute window:

**Reproduction (all from a clean rebuild of the shipped `work/calendar-bench`):**
- Post-fix correctness: corner probe OK (tick 4194304), the full 42-run diff battery plus F/S long diffs — zero divergences.
- P3 record: all three stored 97bf rows regenerate with byte-identical digests and set counts, heap and wheel — the fix changes no path the old code got right (confirmed by diffing against the parent's pristine source from git commit 59f154f).
- Pre-fix: I rebuilt the parent's wheel plus only the corner/E/F/S grafts — the recorded failures reproduce **byte-for-byte** (corner FAIL 3145728 vs 4194304; F diverges at steps 4/6/39780). The bug and the fix are both real and minimal.
- Steady state: five digest-exact row reproductions; ratios 2.15–3.0× in the wheel's regimes, heap wins 1.9× in all-far — matching the regime-bounded claim. All 40 heap/wheel pairs in `steady.jsonl` digest-equal; table medians match the file.

**Adversarial:** 9 fresh-seed diff runs at 2²⁰ (seeds 5–17, up to 500k deliveries, including case D) — clean; fresh-seed steady E seed 5 → 2.4× (not cherry-picked) and F seed 7 → heap still wins.

**Gold basis:** the 10× arm is not met (2–3× steady); gold rests on the premise arm — the parent's "identical stream everywhere" was false in exactly the regime its lens missed, and its 4.5× headline was one-shot. Both closed, adoptable as a ~30-line fix plus a heap-fallback regime rule.

**Missed by the author** (recorded in check.md): the S 2²⁰ row's command is undocumented (I reconstructed it — it regenerates exactly), no tail data at all despite #12 being p95/99, and a stale `-t` comment/print that will mislead the next diff-mode reader. Build artifacts removed; nothing else in the run folder touched; no commits made.
