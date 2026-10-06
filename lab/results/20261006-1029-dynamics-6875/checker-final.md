Working...
Check complete. `lab/results/20261006-1029-dynamics-6875/check.md` written; nothing else in the run folder touched; no git mutations.

**Grade: silver** — real premise-kill, failing on the record, not the physics.

**What held under reproduction and attack:**
- **Bit-exact reproduction, 11/11 files** from the shipped `belt_sim.py` (av pair reconstructed from its JSON stats; the dossier's av command omits `--gm 5e-8 --orbits 400 --seed 7`).
- Regenerable columns match exactly: control resched/orbit 54, drift exactly 0; overlap +39–67%; encounters flat; work/real encounter 2.3–3.6×10⁵ vs 2.2×10³ (×10²); resched/conj 53–61 → 65–75.
- My 1600-orbit rerun **strengthens** the central claim: σ_e slope climbs 0.21 → 0.33 without saturating (κ = 0.13), work/encounter 4.3×10⁵. No steady state at fixed birth parameters.
- Avalanche wake bounded: burst +1.8k, tail +146/orbit ≈ 2.9% over 200 orbits, no cascade.

**Why silver:** the shipped `analyze.py` (edited post-run, 10:45) prints the headline table's header with no rows — the slopes/Fano table is not regenerable by the shipped code, contradicting the dossier's "everything regenerates"; its Fano column is encounter-based though P4 registered conjunction Fano; and my adversarial gm=5e-7 run crosses the author's own clustering line (detrended conjunction Fano 2.16), so "stays Poisson" is regime-dependent. Also found: the late-time exponent points past the predicted 1/4 toward 1/3 (rate ∝ overlap ∝ σ_e), which doesn't change the design conclusion.

**Gold path:** one record fix — a working analyzer with pinned windows, the registered conjunction Fano (plus detrended variant), and the ×87/×109 headline scoped to the whole-neighbourhood re-pay policy (×~2k under the 6 Oct rank-k certificate). No new physics needed.
