Working...
Check complete. `check.md` written; tree restored (patch reversed, probe and example removed; only `lab/results/` untracked).

**Grade: silver** — first line of `check.md`, with the abstract and reasons.

What I did and found:

**Reproduced** (clean tree + `git apply work/patch.diff`):
- 13,801 `from_state` calls → **24 distinct shape keys, hit rate 0.998**, digests `8f353a2b…`/`cb815b7e…` exactly matching the author's recorded baselines — and the control-only run is memo-off, so the interleaved A/B run producing identical digests proves bit-identity in-process.
- A/B: −12% median both seeds (author claimed 12–16%); stage shares match (secondaries 33%, bind 53%, physics ~2%, idiot index ≈ 49× here).
- All 50 space tests and all universe tests pass (three serial reruns; one unreproduced load flake on the first concurrent run).

**Adversarial probe** (own test, deleted after): the author's `ShapeMemo` ≠ `Orbit::compile` impurity is real — memo refuses unstable circles at q ∈ (1/6, 1/3) — and **worse than reported**: at exactly q = 1/6 the memo doesn't refuse but silently returns an orbit with `advance() ≠ 0` where compile's symbolic circle returns 0. The patch's `k == UNIT` pass-through is necessary, and the latent gap in `events/records.rs` is silent divergence, not just refusal.

**Not gold:** ~1.2× on the bottleneck, no demonstrated downstream failure from the impurity. The one gold experiment: land the three named levers and show ≥3× in the same A/B, or demonstrate a wrong binding through the events store's unstable-circle path.

**Author misses recorded:** the q=1/6 silent case, the promised held-out *order* never run, the overstated "api test asserts equivalence" claim, and instrumentation inflating absolute stage numbers.
