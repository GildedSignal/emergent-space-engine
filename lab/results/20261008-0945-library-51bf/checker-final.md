Working...
Check complete. `check.md` written to `lab/results/20261008-0945-library-51bf/check.md` — nothing else in the folder touched, no git commands beyond read-only `show`/`for-each-ref`/`log`.

**Grade: lead.**

What I did and found:

**Reproduction — perfect.** The cached `decisive.jsonl`/`tuning.jsonl`/`verdict.py` are byte-identical to `origin/claude/lab-20261004-0555-quant-5022`. `probe.py` in a clean tree regenerates `metrics.json` exactly (mins T1 8, T2 64, T3 32, H1 64, H2 16, H5 16 → 1.92×; ladder misses T1 and H5 by two steps). My independent gate reimplementation and quant-5022's own `verdict.py` agree. scipy confirms the Spearman values. Timing is clean (predictions 09:51:34 → probe 09:53:00 → metrics 09:54:13), `patch.diff` empty, and the five quotes are verbatim in the 4,580-row corpus.

**Adversarial — the arithmetic holds, the interpretation doesn't.** Minima are robust across gate tolerances (ceiling 1.50×–2.82×; H5-vs-H1 inversion survives all variants), but the Spearman ranking is noise-level (p ≈ 0.5 on six points; leave-one-out swings ρ(e0) from 0.00 to +0.79), and the 1.92× ceiling is a property of six μ ≥ 3e-4 stress seeds: quant-5022's own published check measured 2 events/orbit at μ = 1e-5 (≥ 32× per-body), and the 27ce belt files the author fetched into `data/` and never read show min cadence 8.

**Novelty — pre-empted.** The redirect ("10× from the averaged layer, not cadence") is quant-5022's own published conclusion (HISTORY line 3130). The sensor conclusion is surpassed by `q-cadence-7d0d` (5 Oct, silver, published branch): it measured the frontier N* ∝ τ^0.57, flat in e, and read H1's 64 as resonance routing. The run's premise "q-cadence is queued" was false at run time — one `git for-each-ref` away — though board.md's stale taste log ("q-cadence queued") partly misled the author; I flagged that for the integrator.

Salvage noted for the integrator: lesson 4 (max-aware judging) is a real rung-writing input, and the H5-vs-H1 inversion is a compact falsifier for any e-only ladder at long horizons.
