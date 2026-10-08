Working...
Check complete. Verdict written to `lab/results/20261008-2113-autoresearch-687b/check.md`: **Grade: silver**.

**What I reproduced in a clean tree** (`git apply work/patch.diff`, fresh release builds of both pristine and candidate binaries):
- Gates: 10/10 pass — though the dossier claims 11/11; the suite has 10 galaxy tests.
- Bench structure: 13,963 cycles and 1,706,760 far samples match exactly; splat ≈ 91–94% of frame.
- Plane-size diagnostic: 31.0/25.7/24.6 ns/sample at 480/960/1080p — flat-to-improving, confirming "not plane-cache-bound".
- My own interleaved paired A/B (3 reps + single-thread): median ratios far 0.917, mid 0.905, deep 0.913, threads1 0.88–0.94 — matches the reported 0.93 median. The ~7% gain is real and bounded as claimed.

**The adversarial find that blocks gold:** the magic division is provably wrong for power-of-two periods — `dmag = 2⁶⁴` truncates to 0 in the u64 cast, and `locate` collapses to q ∈ {0,1} (offline check: d=2, e=4 → q=1, r=2). So the dossier's "proved exact for all u64 dividends when period ≥ 2" is false. It's latent: I scanned 9,678 real periods across 6 seeds, zero powers of two, 483,900 differential divisions clean, and the frozen track gate would fail loudly if one ever occurred. One line fixes it (`e >> dsh` when the period is a power of two), but until then even the "adopt for exactness" path rests on a false proof.

**Why silver, not gold:** reproduced and honest, but ≤13% on the view instrument moves no board bottleneck 10×, deletes nothing, and the killed premise (scalar-bound readout) is one the run posed itself. The one experiment to gold: build the structural lever it points at (SoA-batched splat or plane tiling) on the same artifact and show ≥10× with gates green. Pre-registration of predictions.md could not be verified from file times (folder published at once) — noted in the check; log order and the disclosed outcome appendix are consistent.
