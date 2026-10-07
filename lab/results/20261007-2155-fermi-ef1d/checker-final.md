Working...
Check complete. `lab/results/20261007-2155-fermi-ef1d/check.md` written — **Grade: silver**. Only that file was added; all reproduction ran in a scratch copy.

**What I did:**
- **Reproduced bit-for-bit**: `python3 hlive.py` in a clean copy regenerates `out/hlive.json` exactly — 96/96 config×metric pairs across all 32 rows (wall 110.5 s vs the author's 118 s). The disclosed post-run append of `control_D0` rows is honest: `dmul=0` never draws, so the rng stream is undisturbed.
- **Verified the instrument against independent analytic truth**: closed-form Chandrasekhar D = 3.0127×10⁻²² (exact match to the binned integral), t* = 2.63×10⁷ yr, max contact kick 0.0701 q, σ vs analytic at every rung, Elias-gamma accounting by hand.
- **Ran my own held-out attack** (pre-registered): dense ×100 to 2×10⁴ orbits — 1.751% scarred vs 1.745% predicted by the author's *corrected* first-crossing law, zero at 2000 orbits. Their two failed predictions were diagnosed correctly and the diagnosis independently confirmed — the failures genuinely strengthen the claim.
- **Novelty**: 98bc measured the program *stock*; nobody measured the distinction *flow* before. Fits the board's live question, PRINCIPLES §24/§3.

**Why silver, not gold:** the hot case rests on an assumed τ_L (author concedes), and I found the dossier's wrongness boundary is ~67× generous — single kicks cross q at m ≳ 1.5×10¹³ kg (not 10¹⁵), and just 10 peers of 10¹⁷ kg move t* from 2.6×10⁷ yr to ~2.8×10⁵ yr, so the headline is conditioned on the unstated equal-mass peer assumption. Also: `tail_kicks` is dead code with a stale docstring (it's exactly the sampler needed once peers grow past that boundary), and fermi.md's kick-rate term 4 is ×10² high as labeled. The one experiment to gold is the one the author names: measure τ_L and the perturber mass function on the plane's actual belt via `behave`.
