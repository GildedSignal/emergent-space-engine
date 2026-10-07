# Dossier — run 20261007-0933-scout-23c8 (lens: scout)

## Claim (one sentence)

H_live, the number the board says decides whether 10⁹ bodies fit in 8 GB, is **not** the Lyapunov/KS rate: in the plane's belt regimes it is the **stationary scar entropy** — the secular belt saturates at ~6 bits/body (quantum 10⁻⁶) within ~2 orbits and then creates ~0 bits/body/orbit ("stable chaos": T_Lyap ≈ 1.2 orbits with flat memory), while resonant and encounter belts sustain ~0.1–0.6 bits/body/orbit — so the 64-bit/body budget holds everywhere measured, and the real decision is *which shipmem form* each doll needs (program+scars where H_live ≈ 0; packed per-body blocks where mixing saturates).

## Bottleneck

Board item "fitting 10⁹ in 8 GB … decided by distinctions created per game-second"; HANDOFF risk "not measured yet". First measurement, orders of magnitude, on the plane's own regime family (restricted, planar, star+ belt + one perturber). Expected gain: turns B18/shipmem from a bytes question into a per-doll entropy readout with a form-chooser rule; deletes the fear that chaos linearly burns memory at 10⁹.

## Evidence

Instrument (`h_live.py`, numpy float64, exact-Kepler drift in elements + perturber kicks with the indirect term — law.md's own split; scar = (ΔE,ΔL) from the birth program, plug-in entropy of the quantized scar distribution; 256 Benettin shadows). Machine: 8 vCPU shared (load 1.0–1.8), 15 GB, numpy 1.26.4. Reproduce, each ≤ 60 s:

```
cd lab/results/20261007-0933-scout-23c8
python3 h_live.py S0    # ~6 s  control: instrument floor 1.06 bits, |dE|~1e-14
python3 h_live.py S1    # ~28 s secular    (mu=1e-3, a_p=5.2)
python3 h_live.py S1b   # ~28 s secular off-resonance (a_p=4.75)
python3 h_live.py S2    # ~28 s near 2:1   (belt at 2.08*2^-2/3)
python3 h_live.py S3    # ~35 s crossing perturber (q_p=0.74, mu=1e-4)
```

Raw curves in `h_live_S*.json`. Numbers that matter (N=8192, sampling cap 13 bits):

| regime | transient | sustained H_live | T_Lyap | scar spread |
|---|---|---|---|---|
| S0 Kepler | 0 | ~0 | — | 1e-14 (round trip) |
| S1/S1b secular | ~6–7 bits @1e-6 in 2 orbits | ≤ 0.02 bits/orbit (consistent with 0) | ~1.2 orbits | p99 1.3e-5, **flat** |
| S2 near 2:1 | ~6 bits @1e-4 by t=1 | ~0.13 @1e-4, spread still growing to belt width | < 1 orbit (94%) | p99 1.3e-3 → 3.5e-3 = full belt |
| S3 encounters | 2.6 bits @1e-3 in 1 orbit | ~0.4–0.55/orbit, **bursty**: flat t=1→2, jumps at the encounter wave (8.5% → 24.5% → 45.5% bodies within 3 R_H) | < 1 orbit (100%) | p99 2.8e-2 per encounter epoch |

- **Stable chaos is the load-bearing surprise:** S1 shadows diverge exponentially (median ln-growth 0.86/orbit, 98% saturated; identical off-resonance in S1b, killing my 12:1-MMR hypothesis) **while scar entropy is flat** — prediction P1's λ estimate failed 60× and the memory consequence of that failure is the result. λ forbids any "predict from a similar neighbour" shortcut but costs no memory.
- **Quantum signature (held-out P5):** saturated H rises 4.4–5.5 bits per decade of q (1e-5→1e-7), between a 1-D manifold (3.32) and smooth 2-D diffusion (6.64): the scar cloud is a thickened ~1.4-dimensional secular manifold — neither a chaotic point set nor full diffusion. The q-slope is the classifier, as predicted.
- Fat tail: p99/median |ΔE| ≈ 4 in S2/S3 — the top 1% of bodies carry multiples of the typical scar; reabsorption should target them first.

## Predictions

`predictions.md` was written before any scene ran. P0 ✓ (instrument zero). P1: half-held (H-slope in range early; the λ estimate failed 60× — reported, diagnosed, and it became the finding). P2 mostly ✓ (6× entropy, 94% vs 0% short-T_Lyap, p99 grows; clamped-count prediction wrong: pumping showed in |ΔE|, not in e-clamping). P3 ✓ (bursts, enc_frac 45.5% by t=10, ~5 bits per encounter-affected body). P4 ✓ (no regime above ~1 bit/body/orbit). P5 ✓ (slope strictly between the two pure regimes).

## What would make it wrong; cost; PRINCIPLES fit

- Windows are 16 orbits: real-belt Lyapunov times are 10³–10⁵ orbits (UNVERIFIED values; sources qualitative), and slow Arnold diffusion could lift the secular saturation later — orders of magnitude only; the M1 re-measures. A Kepler-only program makes the 6-bit transient an **upper bound**; the law's averaged-kick program absorbs part of it.
- Restricted/planar/Newtonian, one perturber, fixed orbit; the galaxy doll and GR-strong dolls untested. Float64 falsifier, not the integer law.
- Cost of adopting: cheap — the instrument is ~200 lines on the engine's scenes; the rule it buys: **B18 and shipmem's form-chooser read per-doll stationary scar entropy + q-slope, not Lyapunov exponents; reabsorption cadence = scar budget / H_live** (principle 12's allocator, fed by the simulation itself: "the simulation tells us what is next not us"). Principle 6 ("Store the generator, not the generated"): the generator survives exactly where H_live → 0, and that is measurable per doll. Principle 24 ("The memory floor is information-theoretic"): the floor per doll *is* the stationary scar entropy at the law's quantum.

## The lens

Scout searched chaos theory (Pesin — verified), belt astronomy (stable chaos, chaotic diffusion) and MD (Toxvaerd 2012 round-off×Lyapunov) and ran the falsifier — but a scout optimises for the best *known* method, and the result inverts the literature's emphasis (KS rate) for our quantity. May have missed: information-theoretic work on trajectory compression under rate-distortion (the scar floor is formally a rate-distortion function at the certificate's distortion); GR/relativistic dolls where λ and tides couple differently; and the player as a source of distinctions (off-plan: AI), though the same instrument measures a player-driven scene unchanged.
