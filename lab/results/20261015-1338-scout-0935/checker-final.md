Working...
Check complete. **Grade: gold** — written to `check.md`, with the author's wiki page corrected in place.

**What was done:**

**Reproduction** — `regen.sh` rerun: exit 0, 36.5 s, output identical to the runner's log; every dossier number regenerated exactly (R2b/β² = 1.4–1.7 flat across 200→12 M, R1_perp = (0.61–1.0)·β, kill bar fired at 4.431e-2, held-out rows exact). The author's stored `beta_scan.json` matches to the last digit.

**Independent instrument verification** (beyond the author's own controls):
- The claimed-but-unshipped 2.0e-16 boost control rebuilt from scratch (own Lorentz transform + static KS): **2.2e-16–6.6e-16 at β up to 0.5** — real.
- b1a transcription verified term-by-term against the fetched Carlip paper (gr-qc/9909087).
- New Ricci probe: static/free-fall at the 4.5e-10 vacuum floor; under burn R_mn = c·σ_μσ_ν (null dust, linear in thrust) — the constant-m burn oracle is a genuine exact Einstein solution whose matter is the exhaust. The author never stated this; it strengthens the oracle.

**Adversarial, outside the tested domain** — all held: β = 0.7 (R2b = 1.35·β², RX 2.7e-8), r = 8 M (RX ≤ 5.4e-9, R2 up to 0.73), 32-phase searchlight scan (max 1.21·β²), lateral burn a ⊥ v0 with a rebuilt vector-acceleration source (RX ~1e-10 — payload completeness holds for arbitrary burn direction).

**Predictions** — predate the stored decisive outputs; P1–P3 held, and P4's kill criterion fired against the author's own hoped outcome and was reported as such.

**Page corrections:** the "dm/ds term implemented" claim was false (m is constant throughout the code) — corrected with the null-dust finding; burn-channel coefficient (1–4)·a·r → (1–6)·a·r (author's own extreme point measures 5.8); boost control annotated as reproduced-but-unshipped. Flagged for the integrator: the boost control belongs in `news_strong.py`'s self-test — the one record gap between this and a fully self-regenerating instrument.
