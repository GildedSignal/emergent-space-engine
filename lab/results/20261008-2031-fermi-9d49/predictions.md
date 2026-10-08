# Predictions (written before the decisive runs)

Run folder: `lab/results/20261008-2031-fermi-9d49/`. Decisive experiments:
(A) `cargo run --release -p emergent-shipmem --example measure` on `convoy`, `formation`, `random`, with and without kicks;
(B) the analytic rate script `fermi_hlive.py` (scattering cross-sections vs the law's quanta, budget arithmetic).

## A. Store measurement (cases not tuned on)

1. **Convoy pristine** (a perfect launch program, geometric(12) gaps): I estimate ~13.5 bits/member entropy floor, so measured **14–24 bits/member**. (Prediction: inside [12, 26].)
2. **Random** (fully individual, no program, E Q48 + L Q32 + t_p + kind + ω): raw ~185 bits/body; sorted-order delta coding and the exchangeable correction buy back ~30 bits → **measured 130–200 bits/body**. (Prediction: inside [120, 210].)
3. **Cost per kick with compaction** (convoy, 2×10⁵ kicks on 10⁶ members, ~20% scarred once): the scar is a sparse index (Elias–Fano ≈ 3–4 bits at 20% density) plus deviation fields (11–17 bits × 4 columns) → **40–100 bits per kicked member**, i.e. `bits_after − bits_before` ≈ **8–20 bits/member** at that density. (Prediction: inside [5, 25].)
4. **Re-kicking is bounded**: a second kick on an already-scarred member updates its scar in place (deviation random-walks; its width grows ~1 bit per 4× more kicks). At the same update count on half as many distinct members, bits_after is within **±3 bits/member** of case 3. I cannot force ship count with the shipped CLI, so this one is checked only if time allows (an edit would be needed); otherwise it stays a stated inference.
5. **Formation ≥ convoy** pristine bits/member (the grid adds jitter columns): prediction **convoy ≤ formation ≤ formation+8** bits.

## B. Analytic rates (held-out numbers, from physics not fits)

6. **Belt–belt mutual encounters promote nobody.** For 1-km rocks (10¹² kg) at belt density (≈10⁶ bodies in an AU-scale annulus), a close encounter at b = 10⁶ km, v_rel = 5 km/s gives δv ≈ 2Gm/(b·v_rel) ≈ 3×10⁻¹¹ m/s, and even the accumulated random walk over 10⁶ orbits stays ≥ 5 orders of magnitude below any behaviour quantum (≥10⁻⁶·v ≈ 2×10⁻² m/s). Prediction: promotion rate **< 10⁻⁶ per body per 10⁶ yr of game time**.
7. **Fleet gravity does not scar a belt.** A 10¹⁵ kg aggregate fleet at 20 km/s needs b < ~400 m to move a rock by a 10⁻⁶-relative quantum; swept volume through a 10⁹-body belt gives **< 10⁻² promotions per game-year per fleet**. Prediction: < 1 per year, i.e. negligible on any play timescale.
8. **The dominant promotion source is resonance/chaos in the belt** (first crossing time ≈ Lyapunov time × ln(1/q_e) ≈ 14 τ_L; τ_L ~ 10²–10⁴ orbits at resonance edges, chaotic fraction f_c ~ 1–10% of a Rayleigh belt near first-order resonances). Prediction: a belt's chaotic members are all promoted within **10³–10⁵ orbits** of game time, one 60–190-bit scar each, monotone thereafter.
9. **Budget verdict.** 4 GiB (ABP's open budget) over 10⁹ bodies = 34.4 bits/body. With programs at 15–25 bits and individuals at 130–200, the fraction that may ever be individual is **f_indiv ≤ (34.4 − 20)/(170 − 20) ≈ 10%**. All-individual is 17–25 GB: the 10⁹-individuals premise is dead on arrival **not** because of event volume but because per-body state saturates at ~16–24 bytes. Prediction: measured numbers land so that f_indiv_max < 15%.
10. **Event rate ≠ distinction rate.** representation.md's ~6×10⁴ kicks/game-second are compute events; each updates E, L in place and creates **0** new bits unless it is that body's first quantum crossing. H_live/s = promotion rate × ~scar width + births × individual width − retirements × same. Prediction: the ratio (distinction bits created) / (kick events) in the plane's steady belt is **< 10⁻³**.

## What would make me wrong

- If `random` measures below ~120 bits/body, individuals are affordable (f_indiv_max > 25%) and the tension relaxes; if above ~210, even 8% promotion breaks 4 GiB.
- If `bits_after − bits_before` per kick exceeds ~25 bits/member at 20% density, transient scars (not promotions) dominate and the scar layer, not the individual width, is the budget breaker.
- If the compaction oracle shows scars do NOT stay in place (members moved to a loose group), the scar-vs-individual distinction I use collapses; the whole budget then rides on the loose-group width.
