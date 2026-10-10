Working...
Check complete. `lab/results/20261009-2348-scout-3851/check.md` written: **Grade: gold**.

**What I did**

- **Reproduction:** ran `run-all.sh` in a clean `/tmp` copy — all four `results-*.json` (cal5, e0, e03, e06) regenerate **md5-identical** to the author's files; every command < 60 s (56 s under load 2.9). `work/patch.diff` was empty, so the tree is the shipped code.
- **Claims:** re-derived all seven dossier findings from the stored JSONs with independently written code, then confirmed with the author's `analyze.py` — every quoted number regenerates exactly (0/24 avg bands vs 12 truth-banded cases; hold32 55/58 worst 17%; kick32 erases a 0.646/orbit Hill loss at Ω_m = 1.410 vs edge 1.414, e = 0; hold4 40/42; 8/8 moon-range overlap; 1.55× drive widening; 16/16 vs 15/42 closed-form centers).
- **Truth attacked:** independent DOP853 monodromy agrees with the hand RK4 to 6×10⁻⁷ relative at the worst case; band chart invariant under 4× refinement; e = 0.9 pumps harder (12.8/orbit); no bands hidden above the 16×Ω_r grid ceiling; the crashing rp = 5 case is an unphysical orbit (L² < 0).
- **Novelty:** no Floquet/monodromy/parametric-resonance treatment anywhere in docs or the 50+ published lab branches; the prior fermi2 runs built the tide kernel and cadence, never member stability. Directly on board item 4; fences H0190's 114× averaging lever and corrects law.md's "exact integer kicks at epochs" (impulse reading fails even at e = 0).
- **Predictions:** pre-registered (00:05, before all held-out files); 4/8 held, 4 failed and disclosed, each failure itself a finding. Noted blemishes: P2 tallied "held" while its static-edge clause failed at 24.3% (printed as finding 2, so not concealment), and `results-e03.json`'s mtime postdates the dossier — immaterial given bit-identical regeneration.

Run folder otherwise untouched; temp dir removed.
