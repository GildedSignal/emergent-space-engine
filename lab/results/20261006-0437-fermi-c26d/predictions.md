# Predictions — 20261006-0437-fermi-c26d (written before the decisive run)

Question: how many bits of live distinguishing information per body does a real
belt create as mutual encounters heat it (game density: 1e9 bodies, asteroid
masses ~2e16 kg, belt volume ~6.6e33 m^3), at the law's behavioural quanta —
and does 1e9 bodies fit the ~6 GB engine share of 8 GB over the game horizon
(~2.5e9 orbits, 10 Gyr at 2.5 AU)?

Toy: impulsive Oepik/Gauss kicks, aggregated per orbit (CLT; per-body lambda of
encounters ~1e6/orbit >> 1). Belt per B18b: banded a, Rayleigh e/i, uniform
angles. Quanta swept q_rel in {1e-5, 1e-6, 1e-7} per column.

Held-out predictions (not tuned on):

- P1 (diffusion): per-orbit RMS velocity kick kappa_v in [2e-4, 2e-3] m/s
  (head estimate 6.5e-4). Belt stays stable: sigma_e < 0.01 and sigma_a/a
  < 0.01 at 2.5e9 orbits; no ejections; collision count reported separately.
- P2 (growth law): scar bits/body grows ~ (n_col/2) log2 T + const while
  unfenced. Values: at 1e6 orbits, joint bits/body in [8, 40] at q_rel=1e-6;
  at 1e9 orbits, in [30, 75].
- P3 (phase saturation): the mean-anomaly column saturates to uniform between
  1e4 and 1e7 orbits (head estimate ~1e5-1e6), pinning ~log2(2pi/q_M) bits.
- P4 (ceiling without repack): 70-110 bits/body at q_rel=1e-6 -> 9-14 GB at
  1e9 bodies: EXCEEDS a 6 GB budget. Crossing time of 48 bits/body (6 GB):
  between 1e3 and 1e8 orbits.
- P5 (coherence): joint entropy / sum-of-marginals in [0.5, 0.9] (one kick
  changes all six columns coherently).
- P6 (allocator): creation rate at 100x real time at 1e9 bodies < 1 MB per
  game-second (memory binds, not write bandwidth).
- P7 (repack): with an identity-reassigning repack every T_r orbits, the floor
  is H(walk since repack) and is monotone-bounded; holding <= 48 bits/body
  needs T_r >= ~1e3 orbits (cheap; belts would be repacked rarely).

Controls:
- positive: kappa=0 run must stay at 0 bits forever (instrument sanity);
- negative: 100x density run must grow clearly faster (sensitivity).

Kill criterion for the premise: if kappa_v lands > 100x above P1's band, the
belt destabilises (e or a walk past fencing) within the horizon — then the
game-density/mass premise is what dies, and the dossier reports the mass or
density ceiling the game must respect.

Decisive experiment: `python3 work/belt_heat.py` (this folder) producing
`work/heat.json` + tables below.
