Working...
**Grade: silver** — written to `lab/results/20261012-2257-scout-64e4/check.md`, with two corrections applied to the author's `wiki/frame-cost.md`.

**What I did:**

1. **Reproduced** from `work/patch.diff` in a restored tree: every deterministic number matches exactly (E1 digest triads `e38b245b…`/`35812c30…`/`2dbc92e4…` with divergent front-traces and frames 3637/3634/3636; E2 raw three digests per seed vs grid one; E0 timings within shared-runner noise, same shares).
2. **Verified the harness is faithful**: `raw` mode is verbatim `session.rs::step:79-80` (`input(now, keys)`); the patch touches only the switch, one gated `rekey()`, and a peek instrument — `digest`/`schedule`/`settle` untouched.
3. **Four adversarial cases, all held**: seed 7 at 1,600 members/60 s (4× the author's domain, 1,642 kicks, 662 encounters in flight) — identical digest ×3; 64-decision dense scripts (the lazy arm genuinely rekeys, closing the lazy≈never vacuity gap); threads=4 (wave/commit-cap path); same-cell grid flips (both decisions land in order, no drop). The presented-tick straddle behind their negative result verifies arithmetically (19,912,096 < 19·2²⁰ ≤ 20,250,432).
4. **Novelty**: the deadline-policy axis is new beyond 40c0's budgets/threads/pace; but the leak was known (40c0) and the fix was already built and held by a342 (`input_frame` + regression test, ungraded) — this run re-derives it independently and adds the wall-vs-presented negative.

**Why silver:** no 10× (switch alone ≤1.5×, drain/requeue own the tier), nothing deleted on the shipped path, and the headline "the only channel that ever made a lazy calendar break digests" overstates — 1537's break was its own-diagnosed fleet commit-cap + `pull`-stale-slot channel under a structural calendar change, no player keys. I softened that sentence and narrowed the direction-1 licence to "deadline-value policies on the shipped calendar structure" in the page.

**The gold experiment:** rebuild the tier's actual deletion (wt/frame's lazy calendar or 1537's tick-keyed variant) *with* canonical decision logging, on fleet-heavy scenes — match makes the licence cover the whole tier and "only channel" proof; break names the commit-cap channel. Either outcome meets a gold clause.

Tree left clean (patch reverted, my probe example removed); nothing outside `check.md` and the page corrections touched; no commits.
