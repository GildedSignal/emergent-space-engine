Working...
Check complete — verdict written to `lab/results/20261018-0722-second-20261018-0431-scout-b083-5f36/check.md`.

**Grade: gold.**

**What I did:**
- **Reproduced**: runner's `regen.sh` exit 0; re-applied `work/patch.diff` myself; deterministic flight counts bit-identical (window 32/32, ANSWERS 15→31→12, dw split 15/2/15). Verified `tier2.py`'s `hit_exact` matches `law::hit` branch-for-branch (law.rs:341–372 — `dw<0` required in every branch), and the flight's integer replica agrees with the engine member-for-member.
- **Adversarial, one decade beyond the author's range**: flew K=10⁶ (candidates 1,000,009 = 1.00·K+10; window 324 vs analytic 326; answers 146/158/147 ≈ half; **1.82–2.04 s/scan shipped answer measured directly** — the author's 1.9 s was extrapolation). Reconstructed the widened 1D curve independently (tier2.py doesn't emit it): **8.3% max miss** at e=0.1/σ_a=1e-5, |d|/near 0.83–1.0 — the dossier's 9% reproduces; at ρ=1e-5 the 1D curve misses 35–45%. The 2D selector stays sound out-of-range (0 misses at ρ=1e-5 and at σ_φ=0.002).
- **Predictions**: pre-registered, mostly held; A2/A3 misses disclosed honestly. One stain: B3's "sizes within ±25%" clause failed (15/31/12) yet is reported "held" — flagged in check.md.
- **Page corrected in place** (two overstatements): the eccentric arm is **e = 0.1** (`e_q48 = 2⁴⁸/10`), not "e = 0.05"; "read list = the phase window" now qualified to the scan's own interval (the author's own log shows 2.2e4/2.5e4 at intervals 2¹²/2²⁴).
- Tree restored (patch application reverted; only `lab/results/` untracked).

**Adoption debt named for the integrator**: fold the 9% number into `tier2.py`/regen before adoption; the answer-set instability is a law-level decision (quantization-signed answer vs same-key d·w ≡ 0 certificate) that halves or holds the tier's read count; probe path peaked at 2.3 GB RSS at K=10⁶.
