Working...
Check complete. **Grade: gold** — written to `check2.md` (119-word abstract).

**What I did:**

1. **Reproduced**: ran `regen.sh` myself — exit 0, 23 s, **131/131 checks, byte-identical** to the author's stored log. Both shipped probes regenerate (`069c`'s `{'bounded': 100}` confirming its record defect; `6cfc`'s 0.967/0.920/0.499 exactly).

2. **Pre-registration verified**: mtime chain — `predictions.md` 23:01:45 → repro script 23:02:22 → page ~23:03 → `verify.sh` 23:06 → dossier 23:07 → decisive run 23:08. P1–P7 held; the one deviation (median alarm orbit 106 vs 9) was pre-committed with its handling, the page carries it, and my φ₀=π/2 arm explains it mechanically (median orbit 4 — the delay is initial-phase-dependent, the verdict is not).

3. **Adversarial, outside the author's domain**:
   - **A·ε boundary** (author's gap 0.002–0.02): 0.008 → 0/200, 0.012 → 200/200 — the breaking condition A·ε ≳ k holds at the edge, not a knife-edge artifact.
   - **Amplitude extremes**: A=2000 at A·ε=0.002 → 0/200 (safe side is product-governed); A=10⁶ exactly commensurate → 0/200 (tautology holds at 50,000× tested amplitude).
   - **Noise**: σ=0.5 trips the CUSUM 200/200 with *no signal* (per-orbit noise-mean sd > k) — the one new finding: the safe bracket is calibration-conditional; the full breaking condition is per-orbit drift ≳ k including σ/√P. Strengthens the kill; noted in "missed", no page correction needed.
   - **Census blind side**: my own scan of all 662 branches for check.md-heavy B12 content outside the ≥4-dossier set came back empty; the 3-mention band and sampled exclusions (450b, f045) are context-only. "Complete" survives.

4. **Novelty**: this run executed exactly the base silver's named one-experiment-for-gold, and exceeded it — its own sweep caught two B12-mechanism runs (2f89, 54d9-gold) the base checker's sweep itself missed, and e9f9's kill moved from single-harness to independently reproduced (the lab's "agreement is not independence" lesson). No HISTORY.md overlap.

5. **Page**: audited numbers beyond verify.sh's greps — all ground verbatim in their branches; mechanics (23 runs, 14 refuted, 1715 verbatim, no dangling placeholder) pass. Left untouched.

Folder state: only `check2.md` added; no commits, no pushes.
