Working...
`check2.md` written: **Grade: silver.**

**What I did**

- **Reproduced** `python3 probe.py` in a clean tree (empty patch): output bit-identical to the stored `probe_out.json` — zero float diffs. All dossier numbers traced to the JSON exactly (C ∈ [1.89, 6.14], N_floor 178/18/2, exponent 1.9962, separatrix table, ISCO seed).
- **Verified the doc claims**: representation.md:67 quote verbatim; :32 still teaches the dead Minsky mechanism while law.md:20 records its kill; law.md:35 is the jet with an offset-only trigger and the 0.05 figure; r5/r6 absent from lab/rungs/; r1-rings.md:25 confirms the ISCO seed. Novelty holds — no HISTORY entry maps the jet's domain (df81 = one family).
- **Five adversarial cases**: 2PN ratios at p=500/1000 (quoted but not regenerable — I recomputed, they're right); a direct encounter kick α=1e-3 at the belt's home corner → **5.1e-3, 5000× floor** (the dossier only extrapolated this); C extrapolates to p=200/1000; separatrix numbers stable under h-refinement; channel decomposition.
- **Found a real defect**: the dossier's derivation is inverted — the coordinate period **T** carries the entire (r_apo·α)² error at all ten grid points; the Δφ/precession channel is the r_apo-free one (~15/4·α²). Headline numbers are channel maxima so none moves, and the proposed root-distance certificate is channel-agnostic, but "Derivation matches" is false as stated.

**Why silver, not gold**: wrong mechanism claim in Evidence, two unregenerable numbers, floats only — and the gold-making experiment is named (the integer-law kick rung: recompile-rate criterion, root-distance certificate as candidate, un-re-anchored jet as negative control). Run folder otherwise untouched; `check.md` never read; no git commands.
