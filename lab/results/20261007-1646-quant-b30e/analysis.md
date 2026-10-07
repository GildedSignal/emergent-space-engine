# Measured (all runs in data/, CSV; columns per probe header)

Machine: Linux x86 8 vCPU shared (loadavg 5.4 during runs), 15.9 GB RAM, ~2.2 GB used.
Cloud box: orders of magnitude only; the integrator re-measures on the M1.

## belt15 (mu=2^-10, r=1.5·sep, non-resonant) — the anchor family, n=16, 512 orbits

| orbits | clean | scarlayer bits/member | med | p99 | max | kicks |
|---|---|---|---|---|---|---|
| 0 | 15/16 | 0.9 | 0 | 2 | 2 | 0 |
| 0.5 | 0 | 127.5 | 39 | 57 | 57 | 3,733 |
| 8 | 0 | 121.0 | 40 | 57 | 57 | 59,737 |
| 64 | 0 | 128.0 | 41 | 56 | 56 | 477,905 |
| 256 | 0 | 128.5 | 42 | 56 | 56 | 1,912,013 |
| 512 | 0 | 130.5 | 42 | 57 | 57 | 3,824,004 |

0 handoffs / 0 lost / 0 refused. 467 kicks/ship/orbit. Flat store contrast: 1,408 bits/member
(176 B per `Binding`). Reproduced at n=32 (8 orbits: 128.5, med 41, p99 57) and n=512.

## belt15w (mu=2^-18 = belt15/256) — linearity control, n=64, 64 orbits

med 32–33, p99 48–49, scarlayer ~117 bits/member: **−8.0 bits vs belt15 on both med and p99**
(kick dv ∝ mu). Cadence self-throttles: 262 kicks/ship/orbit vs 467 at 256× mu.

## belt21 (2:1 resonance) — n=64, 32 orbits: the only growing layer

scarlayer 127.2 → 129.8 → 134.5 → 139.5 bits/member at orbits 2/8/16/32: monotone growth
(~+0.3 bits/member/orbit), vs belt15's +3 bits over 512 orbits.

## hill (1.5–2.5 Hill radii, alternating sides) — n=32, 16 orbits

No handoffs ever fire (prediction 5 wrong in the letter): departures appear as 1 lost + 1
refused by orbit 8, monotone. scarlayer 135–141. CAVEAT: this launch pattern (alternating ±
sides) is not affine, so its orbit-0 control fails by construction (64 bits/member at birth);
its absolute level carries that birth distortion. Weakest config; do not quote its level.

## belt15 n=512, 8 orbits — N-scaling

scarlayer 135.3 vs 128.5 (n=16) at orbit 8: +5% (EF ordinal overhead ~log n). Per-member
widths identical (med 41, p99 57); 466 kicks/ship/orbit, N-independent (no pairwise coupling
in the restricted problem at these N).

## Form P itself (shipmem's strict-majority `infer` + seal)

Alive only at orbit 0 (0.9 bits/member at n=16; amortizes to 8.2 bits/member at n=512).
Dead from the first kicked window on at every N: once any member deviates, no column keeps a
>50% exact majority. What keeps the layer bounded is my per-window median-affine program
refit (common-mode drift is absorbed by the program), not scar reabsorption.

## Predictions tally (predictions.md written before these runs)

1. clean stays 0, no reabsorption: **CONFIRMED** (to 512 orbits).
2. slow diffusion then plateau: **CONFIRMED as plateau** (+3 bits/member over 1,024× time).
3. mu/256 ⇒ −8 ± 1 bits: **CONFIRMED exactly** (−8 on med and p99).
4. resonance worse, growing: **CONFIRMED** (only growing layer, +0.3 bits/member/orbit).
5. hill departures monotonic via handoffs: **WRONG in the letter** (0 handoffs; departures
   are 1 lost + 1 refused instead; monotone). Reported as failed.
6. N-independence of per-member bits (<15%): **CONFIRMED** (+5% at n=512).
7. ~466 kicks/ship/orbit at every N: **CONFIRMED** (n=16, 32, 512).

## Arithmetic for the goal (10⁹ bodies in 8 GB)

- Steady scar layer at law-width invariants (p Q32, k Q48, ω Q32): ~130 bits/member ≈ 16.3 B.
- 10⁹ members × 16.3 B ≈ 16 GB: **over** the 8 GB budget on the scar layer alone, before
  programs, tubes and frames. Weakening kicks 256× buys only ~1.6 B/member (~14.6 GB):
  the width is set by the storage quantum, not the kick regime.
- Resonant families are worse and unbounded-ish (+0.3 bits/member/orbit).
- To fit 10⁹: store member distinctions below law width with exact reconstruction deferred
  (recompute from program + seed), or keep belts in quiet regimes as born programs; at the
  plane's cadence every kicked belt member is live at ~16 B.
