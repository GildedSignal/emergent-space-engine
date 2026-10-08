Working...
Check complete. `check.md` written to `lab/results/20261008-1419-dynamics-5cbd/` — the only file changed there; all reproduction ran in `/tmp/chk5cbd`.

**Grade: silver** (one experiment from gold).

**Reproduced** — everything:
- Both decisive artifacts (`atlas.npz`, `backup.npz`) regenerate **bit-for-bit** from the shipped commands, including the disclosed JSON crash in `runs.py atlas` (after the npz save) and the backup save-crash rerun.
- Every derived dossier number matches my independent reconstruction: classes 166/102/16, quiet truth p95 3.29e-5, encounter median 2.00e-1, honest rule 11,936 vs 18,176 (1.52×), wall fit 1.197·μ^0.236 with LOO ≤ 0.0078, teeth 12×, h-instrument 0.291/92%.
- Predictions pre-registration order verified by mtimes and log order.

**Adversarial** (4 attacks, all survived on physics):
- μ=10⁻² wall extrapolation: 0.375 measured vs 0.405 extrapolated — law robust in order.
- e₀=0.02 shadow atlas on the "quiet" belt: 0/128 diverge — the k_req floor 16–32 is genuinely not chaos.
- Truth convergence through encounters: median 0.2 → 5.1e-2 at hdiv 2048 (~h², erratic per body) — saturation is convergent *instrument* error, sharpening (not breaking) the B12 conclusion.
- The "24" rung = per-bin median of ladder k_req — regenerable, though not printed by shipped scripts.

**Why not gold** — three record misreports, none load-bearing: the "matches Wisdom exactly at μ=10⁻⁵" sentence is false (0.080 vs 0.048, ×1.65; it lands on Wisdom only at μ=10⁻²); prediction (1)'s 0.80±0.02 clause holds only under the predictions' own wall definition, an undisclosed switch; prediction (2)'s ≥60%-censored clause failed (49%) and was silently dropped. Named gold experiment: own the truth-convergence ladder through the encounter class plus the record corrections — then the run is adoptable as gold inputs to q-cadence, q-b12-design and B18b.
