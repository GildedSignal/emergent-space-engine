Working...
`check2.md` written. Verdict: **Grade: silver.**

Summary of the check (all work in `/tmp/chk2`; the run folder untouched except `check2.md`):

**Reproduced** — `run-all.sh` regenerated every result file in ~45 s per sweep; every dossier number printed identically (0/24 avg parametric bands vs 62 truth bands, peaks 2.4–4.2/orbit, hold32 55/58, kick32 worst-peak error 100%, hold4 40/42, 8/8 moon overlap, 1.55×/0.97× P7 ratios). `predictions.md` (00:05:54) predates all held-out results (00:06:50–00:12:02), and the mid-run bug-fix disclosure matches the calibration file timeline.

**Independent verification** — my scipy solve_ivp monodromy agrees with the author's RK4 truth (0/25 band-membership disagreements at the worst case); I re-derived λ = u³(3γ²−1) from the Weyl tensor, confirming it is the frozen phase-2 eigenvalue, not an invented drive.

**Adversarial** — (1) r_p=10⁶, untested by the author and inside E9's grid: bands persist (4–10, peaks 2.35/4.15 per orbit) and the chart is Kepler-scale-free, strengthening the claim; (2) e=0.9, outside the grid: the truth's own convergence check fails honestly; (3) blindness robust to threshold 0.02→0.05.

**Held at silver** because the adoptable certificate is the 2-channel Marck monodromy (build `b-fermi-phase2`, unbuilt) — the scalar chart's centers can't ship — and 4/7 predictions failed as worded (each honestly reported and mined). The one gold experiment: the coupled 2×2 chart with quantized λ, showing blindness and edge-shift bounds there.
