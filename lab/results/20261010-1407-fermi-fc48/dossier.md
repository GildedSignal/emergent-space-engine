# Dossier — H_live: what stirring a belt actually costs at 10⁹

## Claim

H_live of a belt is not a rate problem and not a runaway — it is a step: one
Jovian conjunction pass (~1–2 orbits) takes every belt body off its program's
manifold, after which **no exact encoding at the tube's own quanta fits 8 GB at
10⁹ bodies** (raw scars 107 bits/body = 13.4 GB; best possible, sorted
microstate, 75.5–76.1 bits/body = 9.4–9.5 GB), so the 10⁹-in-8 GB promise holds
only with a requantization law for stirred populations, coarser than the tube
quantum by ~3 orders, with sub-quantum deltas carried (principle 6), plus t_p
re-anchored at kicks instead of scarred.

## Bottleneck

Board risk "Distinctions created per game-second (H_live): they, not the body
count, decide whether 10⁹ fit in 8 GB; not measured yet" (HANDOFF, risks).
Gain: it decides `crates/shipmem`'s belt design and names the clause B18 needs
before belts scale. It deletes the assumption that program+scars is a stable
storage form for belts (measured: scars lose to a plain sorted catalogue after
the first scarring pass, 126 vs 75.5 bits/body).

## Evidence

Model: the repo's own belt (`crates/encounters/src/belt.rs`: a ~ U[1, 1.5] AU,
Rayleigh e, σ_e = 0.01), Jupiter (a_J = 5.2 AU, 9.55e-4 M_⊙), hyperbolic
impulse 2Gm_J/(v_rel·d) at each synodic conjunction, Gauss equations to first
order in e. Quanta from the tube spec (law.md line 12): E, L 32-bit over the
belt's ranges (q_a ≈ 1.1e-10 AU, q_L ≈ 8.4e-11), periapsis angle 32-bit,
periapsis time 64-bit per radial cycle. Scars = a body's exact difference from
its program (law.md line 13).

Commands (from this folder): `python3 hlive.py` (75 s, one seed 20261010;
writes hlive.json + final_state.npz) then `python3 floor.py` (0.2 s).
`hlive.py` slightly exceeds the 60 s preference; the decisive numbers (row
"orbits 1" and the floor) reproduce with `T_ORBITS = 2` in ~2 s.

| t (orbits) | f_kicked | kicks/body/orbit | H_a | H_(L,ϖ) joint | H_t_p mod | fields |
|---|---|---|---|---|---|---|
| 1 | 0.845 | 0.85 | 20.0 | 53.4 | 53.0 | 126.4 |
| 2 | 1.000 | 0.85 | 20.8 | 54.9 | 53.0 | 128.6 |
| 1024 | 1.000 | 0.85 | 25.2 | 60.2 | 63.9 | 149.3 |

- Scarring is a step, not a drift: f_kicked = 1.000 by 2 orbits (0.85
  conjunctions/body/orbit, inside H0190's 0.3–32 kicks/orbit band).
- Growth after the step is logarithmic: **2.95 bits per doubling of t**
  (fit, t ≥ 8 orbits) — σ_e only doubles in 10³ orbits (0.0066 → 0.0189 std).
- Conditioning the e-dof deltas on 64 bins of a removes **< 1%** (55.9 vs
  55.6 bits at 32 orbits): the surprise is per-body (quasi-random phases),
  not a shared smooth field — group certificates cannot absorb it.
- t_p diverges through one full cycle by ~100–300 orbits, saturating its
  64-bit mod-cycle field; raw (unanchored) it grows past the field.
- Sorted-microstate floor (any exact encoding, converged across coarse-grain
  2²⁰–2²⁶): **75.5 bits/body at birth dispersion, 76.1 after 10³ orbits** —
  9.4–9.5 GB at 10⁹, over the 8 GB budget *independently of scarring policy*.
- Rate side (analytic, from measured 0.85 kicks/orbit, P_ref = 4.1e7 game-s):
  2.1e-8 kicks/body/game-s → 20.6 kicks/game-s at 10⁹ → ~33 KB/s of scar
  writes at rtf 100, six orders under the M1's bandwidth. The wall is the
  level, never the rate.

## Predictions

All six in `predictions.md` written before the run. Held: P1 (0.845 ≥ 0.8 at
1 orbit, 1.000 by 2), P3 (t_p saturation ~100 orbits vs "~100" — measured
100–300), P4 (slope 2.95 in [1.5, 4]; conditioning < 25% — measured < 1%),
P6 (floor ≥ 60 — measured 75.5). Marginal: P2 (e-dof 53.4 at orbit 1 vs
predicted 40–55, at the top edge). Faster than predicted: P5 said the 64-bit
budget crosses in 2–4 orbits; measured ~0.5–1 orbit (the first pass already
carries 107 bits/body). The kill criterion (best encoding < 40 bits/body)
did not trigger: 75.5.

## What would make it wrong

- The impulse model is first order in e and ignores resonant pumping; the
  belt [1, 1.5] sits among 5:1–7:1 Jovian resonances, so real heating is
  likely faster — this makes the verdict conservative, not fragile.
- Quanta assume E and L each span exactly the belt's range in 32 bits. A
  doll that stores them over a range R× wider shifts each dof by log2 R
  (±6 bits/dof for a system-wide doll); the wall moves by under one order,
  the step does not disappear.
- One seed, N = 65536; entropies converged across coarse-grain factors, and
  the per-orbit hand check (25.3 + 29.2 ≈ 54.5 predicted vs 53.4 measured)
  agrees. A checker should vary the seed.
- The floor is for *generic* microstates. A belt kept on a program manifold
  (no stirring, or stirring exactly recomputable on read) pays 0.126
  bits/body — that is the gold `components-98bc` number, cross-checked here
  from the entropy side, and it is exactly what ~1 orbit of stirring
  destroys.

## Cost of adopting, and fit with PRINCIPLES

Adoption = a law decision, not a storage tweak: a stirred-population doll
whose storage quantum is ~2⁹–2¹² coarser than the tube's (floor 75.5 − 27 ≈
48 bits/body ≈ 6.1 GB at 2⁹, with headroom), remainders carried as integers
until they cross the coarse quantum (r2's carries; "rebinding with its
remainder carried and never dropped"), and t_p re-anchored at kicks (the kick
event already recomputes the tube through the current position), never stored
as a 64-bit scar. Anchors: principle 6 "influences below one quantum
accumulate"; principle 5 "the floor is what the player can differentiate"
(no player differentiates 1e-10 AU of semi-major axis on a belt body);
principle 24 "the memory floor is information" — measured, that floor is 9.4
bytes/body once structure is gone. B18's frozen bar (≤ 2× floor + 2 bytes,
reported at 10⁹) is passable only for populations near their programs; a
stirred clause is needed before belts scale.

## The lens (Fermi) and what it missed

The estimate-before-building lens fixed the decomposition (rate × size →
level × growth type) and killed the rate hypothesis before running. It may
have under-weighted the replay-cache: since the whole evolution is
deterministic, "store nothing, recompute 0.85·t kicks on read" caps memory at
a window, paying compute instead — I dismissed it on query-cost grounds
without measuring; whether encounter certificates tolerate it is a design
question, not a measured one. It also says nothing about fleet/contact
distinctions (the co-orbital gold's territory).
