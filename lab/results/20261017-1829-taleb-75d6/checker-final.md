Working...
Check complete. `lab/results/20261017-1829-taleb-75d6/check.md` written; tree restored to the state I found it in (patch reverted, only `lab/results/` untracked).

**Grade: silver** — reproduced and decision-relevant, but the headline number is instrument-inflated and the mechanism claim fails its own predicted test.

**Reproduced (all of it):** patch applies cleanly and matches ed3a's hunk; my independent rerun of the staggered arm is byte-identical to the stored CSV; every dossier number verified in `analysis.json` (K2 22.9/14.5/14.3, K1 |z|≤1.05, K3 0.354 vs 0.414, wave width 210×10⁶→5,560×10⁶ ticks, C1–C3, P5).

**Four attacks, three landed outside the author's evidence:**

1. **Seed 3** (never seen by the author): fires harder — 86–200× vs the same ref8 ladder, all alive.
2. **A 4×-finer reference (step_log2 9, my arm):** the off band is 8.7×10⁻⁸, not 1.7×10⁻⁸ — ref8 shares tick-0 anchoring with the off arm (the dossier's named softener, now measured). **K2 falls 22.9× → 4.8×**; still over the 3× bar, but by margin, not by an order.
3. **Same-tick readout:** each arm reads at its own `t_wave_end + P_min`, and the stagger moves `t_wave_end` by 3.6×10⁻⁴ orbit *by design* — a readout-phase artifact contaminates every cross-arm comparison. Matched to one common tick, the on−off differential drops 3.2×10⁻⁷ → 2.1×10⁻⁷. That residual is ref-free and still ~5–10× any defensible shipped band, so **the kill direction is over-determined; the magnitude is not freezable**.
4. **The mechanism fit the author proposed and skipped:** it fails — ρ=0.23 between per-body error and offset; body 54 (offset 1.5% of Δs, off-arm error 1.4×10⁻⁹) pays 6.0×10⁻⁷. "Asymmetric first step" is unproven, so the named one-line symmetric cure is a hypothesis, not a result.

**Page corrected in place** (ratio range 14–23×, ref9 ladder numbers, same-tick artifact, successor marked unmeasured, mechanism marked unresolved). Novel (the birth-stagger page's own open direction 2), on-goal (PRINCIPLES #9, #13). Gold path: one common absolute readout tick + the symmetric arm under the same K1–K4.
