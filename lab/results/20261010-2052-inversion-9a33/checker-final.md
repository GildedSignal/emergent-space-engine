Working...
Check complete. `check.md` written; run folder otherwise byte-identical to the author's (verified with `cmp`; the three JSONs my reproduction accidentally overwrote were restored exactly — sizes and mtimes match the originals — and my stray `time`/`out` files removed).

**Grade: silver.**

What I did:
- **Reproduced** all five scenes from the dossier's commands in a clean copy: A, B1e-3, B1e-2, C byte-identical; B3e-3 identical in every discrete field (the one exception, disclosed in check.md: `clump_rms_radius` stored `…735899` vs regenerated `…738899`, 3×10⁻¹⁰, stable across three recomputations — caught precisely because of my overwrite/restore incident).
- **Predictions audit**: `predictions.md` (20:59:53) precedes the final `probe.py` (21:14:32) and every stored output (21:15+); pre-registered control on both sides; the one missed magnitude was reported by the author.
- **Four adversarial cases** (`adv.py`): the gold's *own* fleet parameters break rank 4 (59.8% miss, max rank 34, law predicts 30); aligned apsides still break it (77%); second seed holds (87.9%); the truth net leaks nothing (1,500 non-candidate pairs dense-scanned, min distance 71×ρ above threshold). The finding is robust — not a strawman.
- **Why not gold**: the in-flight build `wt/cx-b-coorbital-cert` landed 13:37 UTC, seven hours before this run, in the same checkout — its `phase.rs` derives spread-scaled k ("NEVER an assumed rank of four"), contains the equation-of-centre term that covers scene C's intercept gap, and has a concentration fallback. The dossier's "silent miss"/"trigger not public" framing attacks the gold's one-line premise, not the living artifact. What survives is the cost law: k → n at σ_e ≳ Δφ/12, i.e. when the phase tier degenerates back to quadratic.
- **Gold-making experiment named**: run scenes A/B/C through the actual build and measure misses plus max_k/work per scene.
- **Integrity flags recorded**: `vrel_max_seen` claimed but absent from code and JSONs; C's `clump_rms_radius` misquoted as "0.058 both" (its own JSON: 0.112); empty `run.log`.
