Working...
Check complete. `check.md` written to the run folder; tree restored (patch reverse-applied, scratch probe removed; only untracked `lab/results/` remains, as found).

**Grade: gold.**

**Reproduced** (my own runs, patch applied by me, private target dir): probe output diff-empty vs `probe.txt`; flight censuses sd2on / ship400on / sd2m400on `cmp`-identical to the author's; ship400 digest on==off==`4fb49739…10ed`; the factored `exchange` is bit-identical to the shipped inline form by construction (verified in source: the original site shadows `four_momentum` with `momentum(law,…)`).

**Predictions**: pre-registered (mtime order 20:58 → 21:01 → 21:13 → 21:21); P1/P2/P4/P5 held, P3 half-failed as worded and is reported as a miss with a correct diagnosis — the load-bearing half (fix on: ghosts → 0) held exactly.

**Attack results** — all strengthen the claim:
- Closing ~2c (above the tested β 0.99 ceiling): 6,796 fires, 0 flips, 0 disagreements.
- Reach 2×10⁷–2×10⁹ (decades above the battle window, k drops to 14–17): 27,935 fires, 0 flips.
- 300k grazing-biased in-domain pairs: 299,908 fires, 0 flips — ~317k fired pairs total without one boundary flip.
- Double-fire corner closed structurally: receding pairs never pass `hit`, which also answers 6362's "bare D ≥ 0 fires on consumed/future roots" warning.
- Slow gas (v≈Q/1000, a decade below the author's slowest arm): clean, ledgers exact.

One mid-check false alarm worth recording: my first `bigr` harness reported 27,935 "flips" — a match-guard fallthrough in my own code; the printed fix/oracle values were identical. Corrected, reran: zero.

**Missed by the author** (in check.md): the structural bound making bit-identity a near-theorem (target perturbation ≈ 2^(1−k)/reach quanta, below the grid for every legal reach); the same-machinery caveat bounds every fire, not just the 4 contaminated ones; classification agreement is near-tautological; gate (c) priced but unsolved; single-seed 30 s flight arms. The proposed wiki page is faithful — no corrections needed.
