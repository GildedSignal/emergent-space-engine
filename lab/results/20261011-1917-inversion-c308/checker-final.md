Working...
Check complete. `check.md` written to the run folder — nothing else there touched, no git operations.

## Verdict: **Grade: silver**

**Reproduced** (clean tree, `/tmp`, `python3 probe.py 1` / `2`): part 1 (S0, A1–A4) and B1/C1/C2/E0 are **bit-for-bit identical** to the stored JSONs, including `k_exponent_vs_n` to 16 digits. E1's event count and all four rank blocks reproduce; only its post-hoc `validation`/`mean_rank_at_encounter` sample differ — the stored part-2 validation was written by an older code state (probe.py's mtime postdates results-part2.json), and the shipped replacement validation is a category error: a simultaneous-longitude root finder that cannot see track-crossing encounters (1 event vs the machinery's 123, matched 0). Eccentric recall at operating ρ was never measured → the 99.3% magnitude is unsound.

**What stands:** the scaling kill of the gold taleb-09b5's "rank 4" certificate — miss(4) follows k\* = 1.5·n·H·ρ (11.9% → 51.6% → 83.2% along the ladder, seed-robust at 83.1%). My independent adversarial run at the **gold's own motivating 10⁶-fleet formation** (never run by the author) confirms 93.8% miss at k\* = 150, and the repair (cadence ∝ 1/(nρ)) drops it to 7.1% with O(W/ρ) work per encounter — the certificate survives only if its trigger/k is the surprise-rate law 1.5nρH. Eccentric ϖ-spread breaks the mean-longitude sort key itself (rank ≈ 0.045·n at encounter, robust across three computations).

**Not gold:** no `dossier.md` (author-final.md stuck at "Working…"), several held-out predictions missed (A2 10× off, exponent 0.69 vs 1.0±0.1, P5 failed on the eccentric scene and was never adjudicated), and an undisclosed 30× scene change (W). The named experiment to gold: a correct brute-force truth bounding machinery recall at ρ = 3e-4, part 2 regenerated with the shipped code, plus the dossier.
