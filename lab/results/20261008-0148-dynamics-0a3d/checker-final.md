Working...
Check complete. **Grade: silver** — written to `lab/results/20261008-0148-dynamics-0a3d/check.md`; tree restored to clean (patch applied for reproduction, then removed; nothing else in the run folder touched).

**What I did:**
- **Reproduced bitwise** from `reproduce.sh` + `patch.diff`: cold belt 16682 events and fleet 15303 byte-identical including the truth counters; ceiling run 95842 exact; λ sweep, F table, co-orbital shares (18.6%/28.2%), warm gap/T_syn = 1.0005, and all cascade.json numbers re-derived independently from the raw streams. Poisson controls at F = 0.94–1.03 everywhere. Runs 8–56 s, ≤26 MB.
- **Three adversarial cases:** third cold seed → F(10) = 2.18 (seed range 1.58–2.25, above Poisson p99 each time); N=1000 saturation → λ_max doubles to 0.956, confirming λ_max ∝ N (the "0.48 ceiling" is per-belt); ρ=1e-2 cold → F shifts to 1.6–1.9 (F is ρ-dependent).
- **Found a mechanism mislabel:** the cold-belt F(10)=2.25 is 61% co-orbital near-conjunction chatter (gap ≈ 1 orbit ≪ T_syn), not the claimed synodic-locked trains — the k·T_syn story holds for warm/hot belts only. Also: the pre-registered kill criterion (F(1) < 1.2 for cold AND concentrated) formally fires (1.18 and 0.13), reported only as "marginal"; and the dossier's "Poisson p99 of F: 1.57" doesn't match the shipped stats (1.422).
- **Novelty:** no HISTORY entry measures exact-stream arrival statistics; complements gold 20261006-0346 (setup cost) with the timing half.

**Why silver, not gold:** two of five held-out predictions falsified (honestly, and P4's falsification is the valuable premise-kill) plus the mis-registered criterion; the adoptable constants are per belt-family (N, ρ), not the two universal numbers claimed; the no-avalanche closure is analytic, not self-consistent. The gold-making experiment: stir the belt with the measured kicks, re-run truth, and show λ/F track the closure across seeds under a corrected multi-orbit criterion.
