# predictions.md — run 20261007-2246-second-20261007-2155-fermi-ef1d-fa84

Written before the decisive measurement (`python3 measure_taul.py full` + the `hlive2.py`
recompute). What I have tuned on so far: nothing — the smoke run (512 bodies, 10^3 yr) and
the no-planets negative (0/2048 chaotic, tau = inf, stepper floor clean, massive-body energy
drift 4.4e-15 after the concatenate-axis bug was fixed).

Scene, from the shipped code (not chosen by me): Giant mu = 2^-10 = 9.77e-4 Msun at a =
5.196 AU e = 0.05; Home 2^-18 at 1.000 AU; Cinder 2^-21 at 0.390 AU; belt 2.0-2.5 AU
(B18b SPEC band ratio 1.25), e Rayleigh(0.07) cap 0.6. In-band resonances with Giant:
3:1 at ~2.50 AU (order 2), 4:1 at ~2.06 (order 3), 7:2 at ~2.15 (order 5); no first-order
resonance inside the band. Period ratios 2.8-4.7.

## Held-out predictions

P1. Chaotic fraction of the belt at 10^4 yr (tau_L < 3e4 yr): **between 0.05% and 3%**,
   concentrated at the 3:1 (2.50 AU) and 4:1 (2.06 AU) strips — versus the toy's assumed
   100% at tau_L = 300 orbits.

P2. Median measured tau_L among chaotic members: **between 30 and 3000 belt orbits**
   (10^2-10^4 yr). The toy's 300-orbit guess is the right order for the strip members, but
   it applies to a strip, not the belt.

P3. Regular majority: bounded a-residual (after per-body linear drift removal) with
   **rms < 2e-3 AU**, which converts to **< 1 velocity quantum (q_v ~ 1.18e-3 m/s at
   2.25 AU)** for >= 99.5% of bodies — so the zero-crossings cold case is now measured
   against the real planets, not assumed. The planets' secular signal is re-fittable
   drift + bounded spread; it creates no quantum crossings within 10^4 yr on its own.

P4. e-cap exceedance (e > 0.6, outside the program's support) **< 1%**; a-band exits
   **< 2%** of bodies.

P5. dt/2 control (2048 bodies): chaotic fraction moves by **< 2x**, median tau_L by
   **< 2x** — no integrator-driven false chaos (the negative control already pins the
   stepper floor at tau = inf).

## Recompute predictions (hlive2.py, the H_live flow on measured inputs)

P6. Bits/body at 10^4 yr falls **>= 20x below the toy's 6.57** (all-tau-300 assumption):
   total < 0.3 bits/body, dominated by f_chaos x ~6-8 bits per chaotic member; at 10^9
   bodies that is **< 0.3 GB** of live distinctions at 10^4 yr, with tube-outs
   (16 B each) < f_chaos x 10^9 x 16 B. The 34 bits/body (4 GiB) line moves from
   ~1.5e4 yr (assumed) to **>= 1e5 yr** (measured mix), if it is crossed at all inside
   the resonance-saturation regime.

P7. The zero-H_live cold headline survives measurement: the peer-encounter t* =
   2.6e7 yr is unchanged (peers still 10^12 kg, no shipped size hierarchy), and the
   planets add no diffusion of their own on 10^4 yr (P3).

## Record repairs (arithmetic, no experiment needed)

P8. Single-kick boundary m_cross = q_v b_min v_rel / (2G) = 1.5e13 kg at the code's
   BMIN = 10^3 m (the dossier's 1e15 kg claim was ~67x generous — the checker's number).
P9. fermi.md term 4's "200-2e4 kick-events/s" is ~100x high as labeled; recomputed and
   restated.
P10. Re-fit delta: 6.5667 -> 6.5661 bits = 0.009%, not 0.02%.

If P1 or P2 fails badly (say f_chaos > 10%), the toy's hot case was closer to right than
the resonance picture and the claim's 1.5e4-yr line stands; if P3 fails (regular bodies
cross quanta), the cold-belt zero-H_live headline itself is wrong and this dossier says so.
