Grade: gold

**Abstract (for the integrator).** The strong-field gravity-news question is decided: the (x,v,a) version payload is **complete** at r = 12–200 M — the exact Kinnersley field from retarded (x,v,a) alone matches the FD oracle at 1.3e-10–5.7e-9 — while Carlip's cheap b3 readout is **not** (missing −2m/R = 17% at 12 M; a burn channel ≈ (1–6)·a·r, percent at 20 M; the pre-registered kill bar fired at 4.4e-2). The strong-field readout is the closed retarded-field evaluation itself (~tens of flops). Adoption: one clause in law.md's causality primitive; no payload change, no jerk slot. Verified independently (boost control ≤6.6e-16 from scratch, b1a vs the fetched paper, Ricci probe) and extended (β 0.7, r 8 M, lateral burns) — all held.

**Reasons.**

1. **Reproduction, bit-identical.** `bash regen.sh`: exit 0, 36.5 s, output identical to the runner's log and to every dossier number (R2b/β² = 1.4–1.7 flat in r over 200→12 M; R1_perp = (0.61–1.00)·β at every radius; R0−R2 gentle r20 = 2.13e-3 vs ½aR 2.34e-3; held-out rows 6.79e-2 / 6.28e-2 / 6.3e-3 exact). The author's stored `beta_scan.json` matches regen to the last digit. All commands ≤ 60 s.

2. **The instrument, verified independently at three levels.**
   - The claimed 2.0e-16 boost control is *not in regen.sh*; I rebuilt it from scratch (own Lorentz transform + static KS, touching none of their retarded machinery): **2.2e-16–6.6e-16 at β ∈ {0.01, 0.1, 0.3, 0.5}** — the claim is real and extends to β = 0.5.
   - b1a transcription checked against the fetched paper (gr-qc/9909087): all four constant-m terms of eq. (b1a) match exactly; the dropped dm/ds term is consistent with m = const.
   - New probe (author did not run it): FD Ricci of the shipped metric. Static and free fall sit at the 4e-10 vacuum floor; under burn R_mn = c·σ_μσ_ν (fit residual 1.6e-5; linear in thrust, ×4.1 for a ×4) — textbook null dust, exactly Carlip's statement that the stress-energy vanishes only for m const **and** a straight line. So the burn oracle is a genuine exact Einstein solution whose matter is the exhaust stream — a strengthening, not a defect (PRINCIPLES #6: aggregates as sources).

3. **Adversarial cases, at and beyond the author's domain** (grid β ≤ 0.3/r ≥ 12 M, RX β ≤ 0.5; thrust ‖ coast):
   - β = 0.7 (next decade), r = 30: ρ(R2b) = 1.35·β² median, ρ(RX) ≤ 2.7e-8 — the β² law and payload completeness extend.
   - r = 8 M (below the 12 M floor): ρ(R2b) = 1.08–1.19·β², ρ(RX) ≤ 5.4e-9; ρ(R2) up to 0.73 — the full-field readout clause holds deeper still.
   - Fine phase scan (β 0.3, r 20, 32 phases): max 1.21·β² downbeam, min 1.02·β² — no searchlight blow-up.
   - **Lateral burn** (a ⊥ v0, vector-acceleration source rebuilt on their metric/solver): FD-vs-analytic ≤ 1.3e-10, ρ(RX) ≤ 2.1e-10, ρ(R2b) 0.7–3.8% — completeness holds for arbitrary burn direction, as Carlip's "every term depends only on the retarded position, velocity, and acceleration" requires.
   - R0−R2 ≈ ½aR recomputed on all six burn rows: ratios 0.76–2.69 (the dossier's "within 1–2.5×" is slightly understated at the hard-r50 corner; order-of-magnitude claim intact).

4. **Predictions.** predictions.md predates every stored decisive output (folder mtimes 10 min vs 6 min; consistent, not cryptographic). P1 held (control), P2 held with the honest refinement (2m/R, not ε, separates R2 from R2b at small β), P3 held (0.76–2.69×), and **P4's kill criterion fired against the author's own hoped outcome and was reported as such** — the strongest kind of pre-registration. The one invalid jerk scene is disclosed as a build bug, fixed and rerun.

5. **Novelty.** The topic page's open direction 4 named exactly this question ("the strong-field consumer — unmeasured"); d947 was the weak-field scalar toy, 7ab4 the rebind scar, and docs/HISTORY.md holds no prior strong-field Kinnersley measurement. The run answers it with an exact oracle rather than a toy — a genuine step up, and it converts the page's remaining "unmeasured" clause into a decided readout clause.

6. **Goal fit.** PRINCIPLES #30 ("we need to build towards GR that's the goal") — the black-hole consumer certified at representation level; #23 ("Nothing past c") — every arm consumes retarded data only; #2 ("Exact physics is the oracle, not the implementation") — here oracle and implementation coincide for tens of flops. It kills a premise (b3-as-strong-field-readout) and deletes a would-be component (any strong-field payload extension or jerk slot). Not a 10× on a cost axis, but the gold bar's "shows that a premise is wrong" and "deletes a component" clauses are met, and adoption is one law.md clause.

**Page corrections made** (wiki/gravity-news.md): the b1a dm/ds term is **not implemented** (m is constant throughout the code; the dossier's lens section also misstates this — flag for the integrator); the burn-channel coefficient corrected to (1–6)·a·r (author's own r=12, 4× gentle point measures 5.8); the boost control annotated as reproduced-but-unshipped; the null-dust finding added.

**What the author missed.**
- The strongest instrument control (boost identity) is cited in Evidence but absent from regen.sh — the one record gap; a 10-line addition to the self-test closes it. (I reproduced it, so the number now stands on the record.)
- The dm/ds "implemented" claim is false as stated, and with it the mass-loss channel (real rockets: ṁ ≠ 0) is not just unexercised but absent — worth one line in the dossier's wrong-if.
- The burn field's own matter content (null dust ∝ thrust) was never stated; it is the physical reason the constant-m burn oracle is exact, and it is the engine's exhaust story — the run undersold its oracle.
- Minor numeric looseness: "100–800×" R2/R2b gap at β ≤ 0.03 (the shipped grid shows 8–31× at β = 0.03 and 780–13000× at β = 0.003); "2m/R exactly" at 12 M is 1.2×; RX lower bound 1.3e-10 vs measured 3.8e-11 (conservative direction). None affects a conclusion.
- `work/sweep_extra.json` is an uncited leftover (jerk-vs-t scan); harmless clutter.
