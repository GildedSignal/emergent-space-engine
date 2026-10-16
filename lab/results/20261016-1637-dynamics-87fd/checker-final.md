Working...
Check complete. `lab/results/20261016-1637-dynamics-87fd/check.md` written; tree restored.

**Grade: silver.**

Findings, in weight order:

1. **The record does not regenerate as shipped.** `work/patch.diff` is the same 522-line diff concatenated twice; `git apply` is atomic, so `regen.sh` exits 1 from any clean tree — exactly what the runner hit. The fix round caused it (it touched only untracked `regen.sh`, so its tree-save re-appended the author's identical diff), and `fix-final.md`'s "verified from the restored tree" is false — its verification ran with the author's edits still applied (the `grep ES_CHAIN` guard skips application). This is the lab's named gold-barrier ("results the shipped code could not regenerate").

2. **After dedup, everything reproduces bit-identically.** Patch applies cleanly at HEAD 2ac3c8d; all five flights byte-match the committed ones; every table number, the ensemble deviations (≤3×10⁻⁶), the seed band (3.46×10⁻²), the P2 band arithmetic, kicks +2.6%, census — all verified. Instrument is sound (print-only, shipped `readout`, index-matched drifts, env-gated engine diff default-off).

3. **My held-out cases:** seed 3 (the dossier's own named kill) *supports* it — OFF band tight at 2.06×10⁻⁶, channel replicates at 9.2×10⁻⁶; N=10⁴ identical to the digit. But the **2× horizon flips the headline**: the arms cross by 6,700 game-s and at 9,000 s OFF is *worse* (med 19.8 vs 19.4×10⁻⁶, max 1.28 vs 0.87×10⁻³). The "priced, named channel" is a closing transient — the shared tick delays drift onset without bounding it, and the midpoint-sampler mechanism can't be the whole story. Ensembles stay innocent at both horizons.

4. **Novelty holds:** 4fa8 measured the collapse, 21a7 the gates' blindness; this is the first adjudication on the doll-born population itself. Nothing in HISTORY.md or the wiki holds it.

I corrected the author's proposed page in three places (channel marked horizon-local with the crossing numbers; the growth-law "open question" marked answered — freeze the gate at the worst horizon; direction 4's channel marked transient) and noted the doubled patch there. The one experiment for gold: dedupe the patch so `regen.sh` exits 0 from a restored tree, plus fold in the horizon series — both within one short run.
