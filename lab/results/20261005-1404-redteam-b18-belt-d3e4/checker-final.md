Working...
Check written to `lab/results/20261005-1404-redteam-b18-belt-d3e4/check.md`. **Grade: silver.**

What I did in the 30 minutes:

- **Reproduced** both dossier commands in a clean shell: all 13 gate verdicts identical, margins matching (crush85 shape-KS 0.078 vs 0.121 at 2²³; crush75/67 fail only there; crush60/50 fail reach on seed 20261010; table12's 0-of-105). `patch.diff` empty; `predictions.md` (14:13) predates `evidence.log` (14:21); both honest prediction misses confirmed.
- **Verified mirror fidelity** against `wt/b18-belt:xtask/src/behave/belt.rs` line by line — stream, statistics, thresholds, RUNS, stop-at-first-fail all match; the belt-only z's match the author's quoted Rust values.
- **Found a mirror bug the author didn't disclose**: `probe.py:139` never computes the tail-count z — it tests and prints a stale serial-cross z. I recomputed the true z = (X−K)/√(2K) from the logged counts for every plant/run: all within ±3.66 (limit 4.5), so no verdict changes — but the author's "exactly the judge's statistics" claim is false for that line, and the calibration never exercised the count statistic.
- **Ran my own adversarial cases**: four fresh reference draws for crush85/table20 at 2²³ (all PASS, worst D 0.089 vs ~0.122 — the PCG64-vs-xoshiro objection is bounded), and read F4 straight off the judge's code: charge ≥ info, ≤ 2·info+2, growth ≤ 16 B are the only bindings, so the 4 MB table passes exactly as claimed.

**Not gold, by the taste log's own pattern** ("silvers fell short of gold on the record, not the physics"): the Rust-judge run is asserted with no artifact, and the four headline adversaries never ran on the real judge — only on the mirror. The named gold experiment: port the four plants into `belt.rs`'s `Flaw` enum (~3 lines each) and log the frozen judge's own verdicts.
