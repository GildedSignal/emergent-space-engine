Working...
Check complete. Summary of the 30-minute pass:

**Grade: silver** — written to `lab/results/20261007-1032-quant-7578/check.md`.

**Reproduction** — patch applied to a clean tree, all dossier commands rerun:
- Every deterministic field **bit-for-bit identical** at n=10³/10⁴ (both seeds) and at 10⁵ (seed 888: pairs_total 430,382,945; deg_mean 8607.66; evals max 19825; qsteps p999 28).
- Control `scale n 10000`: 4,352,071 cone pairs / 870.41 per body — matches 4.35M/870.
- Timings same order; my less-loaded pass gave 10⁵ re-pay p99 64 ms vs the author's 87 ms — the frame-bust claim survives both directions.
- Pre-registration holds: predictions.md 10:41:43 → decisive run 10:41:46–10:46:05 (259 s, matching the logged phase times); P1–P6 held, P7 failed and is reported as failed.

**My adversarial cases** (verify sets the author didn't run): `narrow-adversarial` busts a frame at only N=400 (re-pay p50 20 ms); `equal-period-keys` turns the burst into a p90 load; σ_e=0.1 saturates degree toward N; σ_e=0.2 `mixed` confirms the author's flagged global-`e_max` suspicion — the scan (not the candidates) goes to N−1. Also verified by arithmetic that "median candidate pair pays zero numeric evals" is literally true.

**Why not gold**: exactly reproducible and the first tail/latency measurement of a board-#4 bottleneck, but it's measurement feeding designs, not a 10× mover or premise reversal — degree ∝ N confirms the board's declared scaling risk. The gold experiment is named: same-ρ ladder + sliced per-pair re-pay demonstrating the p99.9 frame stays in budget with the burst present.

Tree left carrying only the author's patch (my temporary `tailset` instrumentation reverted, rebuild verified); nothing else in the run folder touched; no git commands run.
