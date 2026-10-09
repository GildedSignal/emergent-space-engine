Working...
Run complete. Deliverables in `lab/results/20261009-0709-autoresearch-b2a0/`: `predictions.md` (pre-registered), `log.md`, `metrics.json`, `dossier.md`, `work/patch.diff` (30 lines in `crates/space`), `bench/` + `ab.sh` for reproduction.

**Verification:** 50/50 crate tests in release and debug; 64-bit output fingerprints bit-identical between baseline and patch on both the tuning and held-out populations (that fingerprint also caught a silently broken mid-run revert, disclosed in the log); interleaved A/B measured −4.7% total / −9% median (tune) and −5.3% (held-out).

**The claim, in one sentence:** the geodesic compiler's `fast_quad` hot path gives up ~5% total (−9% median, bit-identical outputs) to exact 128/64 word divisions, and the measurement shows its per-node cost is at its structural floor under bit-identity — four exact divisions plus `cos` per node, 93% of compile time in the quadrature, with the per-compile cost tracking band count (max/median ≈ 19×) — so the 10× lever for kicks is compiling less, not micro-speed (a lead, not gold).
