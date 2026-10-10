Author's fiCaching the tube's proper-time readout at its event on the `Binding` (a value `bind_in` already computes) plus a cartesian-free `orbit_state` path cuts the plane's pure kick resolver by 9–10% (45.59 → 41.12 µs median, seeds 1–3, 6-second bench included) with bit-identical digests on every held-out case and the test suite 74/74 green.
e
`bind_in` already returns) and giving `orbit_state` a decode path that skips the discarded
integer word cut the kick resolver 9–10% (45.59 → 41.12 µs median, seed 1; held-out seeds
2/3 and the 6-second bench agree; every digest and `--describe` identical; tests 74/74).

Deliverables in this folder: `dossier.md`, `log.md`, `predictions.md` (written before the
decisive runs), `measure.py` (21-rep digest-checking protocol), `kick-cache.patch` (the
best configuration, three files).

The one idea that carried the gain: a kick's clock reading re-derived a *past* event's
readout every kick — compute only surprises applies to the resolver's own bookkeeping as
much as to the universe. The structural lever this profile exposes (a cycle recompile per
kick, 0% memo hits) is already named by the law: exact-offset re-anchoring. That is the
next run, and it is a law change, not a cache.

Grade asked of the checker: silver unless the 10% and the bit-identity both reproduce
cleanly on your side (then gold is wrong anyway — it moves no bottleneck by 10×; the
board's bar for gold is gain × probability ÷ cost, and this one is cheap, safe and
immediate, but small). Reproduce with the dossier's commands; the phase profile came from
temporary instrumentation that was reverted before the patch was cut.
