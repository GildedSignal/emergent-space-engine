# Predictions (written before the decisive runs)

Runs: the crate's `kick` (N=10⁴, baseline, budget CDF) and my `burn` sweep
(N = 10³, 3·10³, 10⁴, 3·10⁴ at the fixed belt distribution; eps = 1e-5 … 1e-1).
None of these N or eps values was tuned on; the belt spec is the crate's own.

1. **Wake size:** pairs re-set-up per kick ≈ candidate degree, growing ~linearly
   with N at the fixed distribution (≈ 96 at 10³, ≈ 870 at 10⁴, ≈ 2,600 at 3·10⁴);
   exponent of µs-per-kick vs N in [0.95, 1.1].
2. **Capacity:** with the crate's 2.5–24 µs per pair, one kick's wake crosses a
   3.3 ms frame share (20% of a 16.7 ms frame) between N = 10³ and N = 10⁴, and a
   full 16.7 ms frame below N = 3·10⁴ — two orders of magnitude below the game's 10⁹.
3. **Tail across bodies:** p99/p50 of per-kick wake ≤ 2 (degree varies smoothly
   across the belt); max/p50 ≤ 5.
4. **Skin saves thermal, not burns:** slack-skippable fraction ≥ 0.8 at eps ≤ 1e-7
   (drift 1.5·eps ≪ budget p10), falling through ~0.5 near eps ≈ 1e-5 … 1e-4, and
   < 0.1 at eps ≥ 1e-2 (a player burn of seconds at 0.35 g is δa/a ≈ 2e-3; at the
   plane's throttle up to 11,561 g it exceeds 1). Any single skin width s sized for
   thermal kicks is crossed instantly by a player burn.
5. **Urgency split:** the cone re-scan (which pairs can meet) costs < 5% of the wake
   and is the only immediately-urgent part; ≥ 80% of re-set-up pairs have no hit
   within the first 10 orbits after the kick, so the expensive re-certification is
   smeareable by earliest-deadline (least-slack), not a burst.

Kill criterion for the premise "the skin is the lever for the wake": if the
slack-skippable fraction at eps ≥ 1e-3 is < 0.2, the skin alone cannot absorb
player burns; if it is > 0.6, it can, and my premise is wrong.

## Outcome (after the runs, 2026-10-12)

1. Held: pairs slope 0.98, us slope 1.00–1.07 (pred 0.95–1.1).
2. Held: 3.3 ms crossed at N≈5e3 (pred "between 1e3 and 1e4"); full frame at N≈2.4e4 (pred "below 3e4").
3. Held: p99/p50 ≤ 2.9 (smallest N), ≤ 1.9 at N≥3e3; max/p50 ≤ 2.8.
4. Partial miss: skippable at eps=1e-7 is 0.575, not ≥0.8 (at 1e-9 it is 0.946). At eps≥1e-3 it is
   0.0025 < 0.1 — the kill criterion fired: the skin alone cannot absorb player burns. Bonus the
   predictions did not contain: 5 slack_skip_violations at eps=1e-3 (the drift-budget rule is
   unsound at burn magnitude).
5. Held, stronger: scan 1.3–2.1% of the wake (pred <5%); 99.95% of setups have no hit within 10
   orbits (pred ≥80%). New: first post-kick conjunction inside 10 orbits for ~0% of pairs, inside
   100 for ~48% — the deadline stream.
