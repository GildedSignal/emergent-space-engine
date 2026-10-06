Working...
Check complete. `check.md` written to the run folder; tree restored to clean (patch reversed, probe removed, nothing committed).

## Verdict: **gold**

**Reproduced** (clean tree + `work/patch.diff`): every counted number bit-for-bit — `adj`: 4 missed true sub-ρ (d_min 1.619e-5…8.603e-5, all cone:true), 193 extra all true, 0 false, rank_max 4, method evals exactly 7,402,534; belts/fleet/ranks/ranks2 all identical on counted fields (fleet-fleet 606 evals/pair median, 135× sea-sea work per real encounter). Only timings moved. `predictions.md` predates the evidence and contains claims the evidence then broke — genuine pre-registration; the decisive guard prediction (rank ≤ 4, no growth with n_c) held.

**My attacks** (independent O(n²) position sweep, no longitude binning, 8 scenarios):
- Misses persist across new seeds (3–5 of ~235) and reach **25/441 = 5.7%** in a tighter jam — "~2%" is a lower bound, not a rate.
- Found a **5th genuine miss** on the decisive seed that the author's own adjudication could not see (their dense sampler only runs on *disputed* pairs; a pair missed by both instruments is never checked — their own instrument lesson applies to their fix).
- **Mechanism correction**: 100% of 62 measured misses are horizon-edge conjunctions (t=0 or within 3e-4 of t1); the end-edge miss is *found* when the horizon doubles. The second tier drops boundary-straddling contacts (no interior local minimum), not mis-windowed tangential motion. Cheaper fix; persistent hole is t=0 initial-state contacts, relevant to canonical-tick replays.
- The train certificate survived everything: rank ≤ 4 held at e-spread ×10 (author's admitted weak point), σ_λ=0.005, and n_c=400 with 911 encounters — stronger than the author's own evidence.

Gold because it corrects a premise of an adopted result (q-candidate-degree's zero-miss claim fails under concentration), shows the pairwise representation is ruinous exactly in the board's named regime (40 TB / core-years vs O(n_c) true events), and supplies a measured guard with a dimensionless trigger — all reproduced, with the decisive predictions held. Residual obligations recorded in the check: the rank ≤ k proof and the train implementation, and the dossier's small number slips (5% Full not 10%; 0.273 not 0.18 µs/eval).
