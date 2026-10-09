Working...
Check complete. `check.md` written; nothing else in the run folder touched (adversarial script kept in `/tmp`, probes print to stdout only).

**Grade: silver.**

Verification performed:
- **Reproduction, exact:** both probes regenerate every dossier number bit-for-bit. Timeline confirms `predictions.md` (19:02:18) preceded the decisive probe (19:04:39 → output 19:05:05); `work/patch.diff` is empty.
- **Three adversarial cases:** (1) eccentric belt — the author's own named untested mode — degrades the headline τ-rank concentration from 0.59 to **0.35** frac≤4 at σ_e=0.2; (2) N-independence survives my extension to 16k/32k (flat 0.594/0.596); (3) a Poisson(4) control predicts frac≤4=0.863 vs measured 0.594 — the concentration is an over-dispersed load-tail statistic, not key localization.
- **Quote fidelity:** all five library quotes verbatim in `readwise_dump.ndjson`.
- **Two interpretation defects found:** the "missed fraction decays with N (self-averaging)" series halves exactly per N doubling — a mechanical 1/N normalization, flat on the fixed-density axis; and the toy has no selectivity (window ≈ encounter width), so the O(N²)→O(N·k) bottleneck claim structurally cannot fail there — it was asserted, not tested. `probe_index.py` also never completes its last case (author's own output truncates identically), contradicting the "2.8 s each" claim.
- **Novelty:** τ-as-key composes r8 v2's Diophantine next-conjunction lead with the 28 Sept LSM/matching-engine lead; the needed comparison against the adopted 6-Oct phase-neighbour certificate was not run.

Gold blocker, named in the check: re-run the τ-book on a selectivity truth (real minima, e up to 0.9) with kick-churn measured against the adopted certificate — constant work per real encounter or a clean loss, either way adoptable.
