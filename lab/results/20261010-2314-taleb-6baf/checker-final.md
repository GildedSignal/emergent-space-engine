Working...
Check written. Verdict summary:

**Grade: silver.**

**Reproduced exactly** — all 9 runs regenerate from the dossier's commands; `metrics-check.json` matches the stored `metrics.json` on 44/45 keys (only wall time differs on the shared machine). Controls pass both sides; half-life ≤0.4 P_p and ~10–14 smoothed key-events/ship/P_p (linear to 1200 P_p, my 4×-longer probe) are solid, new, and on-bottleneck (HANDOFF's "H_live: not measured yet").

**Two headline numbers are instrument artifacts**, both with the tell sitting in the author's own output:
- "Mature entropy floor ≈ 12.7 bits/ship" = an iid null draw with zero dynamics (12.673 vs 12.6686); the plug-in+Miller–Madow estimator is pinned at log2(4000)+0.72, and cells_last ≈ N said so.
- "Uniform, not fat-tailed" is counter clipping: p99 sat at 96% of the 16.2/P_p sampling ceiling. Same window, 4× headroom → **p99/med 2.58** (pre-registered tail prediction was right; naive bits20 median = 32.38 = exact ceiling).
- Plus a ~10⁴ bandwidth slip: 2×10⁴ events/wall-s at RTF 100, not 2–4×10⁸.

**What held**: deadband safe on the stirred belt (29.6 vs 31.7), long-run linearity, exact μ=0 control, determinism. The design consequence — re-absorb ≥10 events/ship/P_p, program carries the kick law — survives; the entropy-floor and MEDIOCRISTAN conclusions do not. Gold is one experiment away (unsaturated per-ship rates + N-scaling entropy), and my probe numbers can be folded in directly.
