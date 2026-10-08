Working...
Check complete: `lab/results/20261008-2206-library-73ca/check.md` written, **Grade: silver**.

**What I did:**
- **Reproduced** `python3 horizon_exponent.py`: 18.4 s, <50 MB, every number bit-identical to the dossier and `exponents.json` (disclosed: the reran command regenerates `exponents.json`; values matched my pre-rerun read — only mtime changed). Frozen probe code untouched — `work/patch.diff` is two `__pycache__` files only; tracked tree clean.
- **Held-out verified**: `predictions.md` (22:12:15) precedes the script (22:14:18) and results; probe-1 verdicts frozen 29 September. P1/P2/P4/P5 held; P3's partial failure honestly reported.
- **Adversarial (8 cases)**: order-4 physics separates cleanly (α 0.98 vs 0.00 — strengthens the claim); delayed-onset leak caught (0.00→0.52→1.00); e=0.9 reads non-flat but **no bounded control can run there** (frozen fixed-dt convention detects no orbits); unbounded k^0.05–0.1 and log-k leaks read "bounded" — invisible at any horizon; a transient saturating beyond the window (τ≈5000, window 10⁴) still convicts at 0.68 — acquittal requires the transient dead in-window; single-seed profiles bounce across bands (needs median-seed, per existing rung rules). My 3×10⁴-orbit rerun confirms the frozen saturation level 8.65e-4 exactly — the KILL stood on level, so the α-profile complements, not replaces, B12's size criterion.
- **Novelty**: premise known (H0215, board 6 Oct) and cited; the α-profile statistic itself appears nowhere prior. Lesson 4's fact-check confirmed independently (no crate depends on `shipmem`/`encounters`; B18 freezes the ladder as constants) but only re-measures the handoff's 7 Oct record.

**Why silver, not gold:** validated on one integrable two-body energy series plus synthetics; B12's own chaotic Jacobi/handoff scene untouched; bands soft (e=0.5 top-decade 0.32 between bands). The one experiment: freeze the α-profile on the CRTBP Jacobi/handoff scene with planted bounded and compounding controls on both sides — the author's own named next step.

No commits, no pushes; nothing outside `check.md` changed in the run folder.
