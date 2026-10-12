Working...
Check complete. `check2.md` written; tree restored to clean at `a838a284` (only untracked `lab/results/` remains).

**Verdict: gold.** Summary of the check:

**Reproduction** — Applied `work/patch.diff` to the clean tree, rebuilt, reran all five dossier commands. Bit-exact: bench digest `41343a143a92f956…`, kick replay `0e02bf0f34481650…`, memo 1125/0.0%/51 keys/95.47%, and the three extended configs' replay digests identical to the saved JSONs; timings within noise (leavers rtf100: 100.8 vs 101.6 µs whole, 72.6% vs 72.5% share). The claimed bit-exactness with the origin run was independently confirmed against its branch `claude/lab-20261011-2306-system-3367`.

**Predictions** — Written before the decisive runs (mtime order corroborates the run-log); honestly scored: P4 held exactly (100% key match in all seven configs), P3 held, and the two misses (P2's ≥10×, P5) became the headline rather than being explained away.

**Attacks** — Three of my own configs: seed 3, members 500, rtf 10000. All consistent; rtf 10000 (a 33–200× longer horizon than any author config) *strengthens* the refutation — leaver whole 405 µs, implied jet 120 µs, machinery floor grows rather than shrinks.

**Methodology** — `Orbit::compile` has no memo cache (fresh on both sides of the subtraction); profiler zeros reproduce; the omitted `bind()`/warm-bias errors push the implied jet up but cannot bridge to 10× (would need ~17 µs of unmeasured rebind on a measured 75 µs).

**Named misses** — the ~26 µs floor and the "7–41 anchors at threshold/100" are config-scoped (rtf 10k gives ~120 µs and 519), non-Cycle leaver rebinds dominate at long horizons, and the player memo parenthetical (57–87%) isn't regenerable since `player_shapes` is never serialized. None touches the headline: the ~10× deletion does not exist; the jet wins 1.5×/3.7× and the law machinery owns the rest.
