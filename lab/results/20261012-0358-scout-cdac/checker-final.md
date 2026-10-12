Working...
Check complete. `check.md` written to the run folder; nothing else touched (stored `metrics.json` md5-identical to my regeneration; timestamps preserved).

## Verdict: silver

**Reproduced** — bit-for-bit, 45 s wall, 77 MB RSS. Positive control (Γ=0 → 0 bits) passes; file order supports pre-registration (predictions 04:08 < script 04:16 < metrics 04:17).

**Predictions:** P2/P3/P4 held. P1 failed its band and P5's negative is weak — both honestly reported, and my instrumentation confirms P1's failure *is* the finding: 82.1% of scars are multi-kick accumulated escapes, the exponent deepens (0.937→0.875) when early transients are excluded, and 528 bodies escaped then returned. Structural, not a fit artifact.

**My attacks strengthened the result rather than killing it:**
- Γ sweep to 100: MB/h rises only 0.43→10.05 — **sub-linear** in Γ (s drops as kicks recycle scarred bodies); the toy is more contact-storm-robust than the author claimed.
- Saturation at m=10⁻⁶ (9 orbits) → D/N=0.9998; honest full store at 10⁹ = 0.5–2.1 GB vs the 4.29 GB budget. Conclusion survives even where the MB/h framing doesn't apply.
- N-invariance holds to 10⁶ (D/events 0.00727).

**Defects found:**
1. `metrics.json`'s `alpha_partial` = −0.418 fits the ε-saturated plateau; the dossier's α≈0.8 is correct (my partial-regime refit: −0.816) but the stored field contradicts it — a dashboard consumer gets the wrong lever.
2. The binding number for m≥10⁻⁸ scatterers is the saturation store, not a rate; the dossier's own S7 shows D/N 0.55–0.96 in 3 orbits but never states the 10⁹ endpoint.
3. Novelty confirmed (HANDOFF:70 "not measured yet"; components-98bc and H0173 answer different questions), but CRAM/git-pack was already a half-adopted lead — the new part is the measured rate law and fire-at-T_x timing.

**Not gold** because two of five pre-registered predictions failed and the law is measured on a rate-structure toy, not the design's encounter+kick path — the same gap that held the 29 Sep premise red-team at silver. The one experiment: wire this accounting into b-h-live's dashboard on the plane's real belt, state the saturation store against B18, and fix `alpha_partial`.
