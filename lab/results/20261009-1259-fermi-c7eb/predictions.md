# Predictions (written before any run of the encounters crate or the ledger arithmetic)

Run: 20261009-1259-fermi-c7eb, Fermi lens. Target: HANDOFF's unmeasured risk
"Distinctions created per game-second (H_live) ... not measured yet", plus the board's
10^9 budget question (which term breaks first).

The law's element quantum (from crates/encounters/src/kepler.rs, the law's own integer
grid): period is an integer in ticks, 2^32 ticks per time unit; periapsis time is an
integer mod period. At a=1 (mu=1, P = 2*pi time units): one period tick = Delta-a/a of
(2/3)/(2*pi*2^32) ~= 2.5e-11. A "distinction" on this grid = any encounter or kick whose
integer delta crosses >= 1 tick in P, tp, or the e/omega channels.

## Held-out cases (not tuned on)

P1. Encounter rate per body per orbit, measured on the repo's own belts (`verify a/b/d`,
    n=300..3000, rho=1e-4..1e-3, sigma_e=1e-3..3e-2): order 1e-3..1e-2 per body per
    orbit, rising with rho and sigma_e. (Basis: r8 v2's 427 truth encounters on belt 0,
    20 orbits.)

P2. Encounter-driven individualization of the belt is ~zero at game masses: for the
    largest belt body (Ceres ~1e-10 M_sun) the deflection at a rho-scale conjunction
    (b ~ 1e-4 AU, v_rel ~ n*a*e + shear ~ 1e-3 c_units) changes a by < 1 period tick
    (2.5e-11). Predicted: < ~1% of belt encounters cross one tick even for Ceres-mass
    participants; for ship masses (<= 1e-20 M_sun) essentially zero. So on the law's
    integer grid a smooth belt is an attractor: encounters are contact candidates, not
    distinction sources; the belt stays its birth program (0.126 bits/body) and needs no
    per-body recompiles from encounters.

P3. The 10^9 ledger's binding term is storage of per-body tubes in the current
    representation: 16 B x 10^9 = 16 GB > 8 GB unified (>= 2x over before OS/view
    overhead), while steady events (distinct kicks 0.3/orbit/body => ~7 recompiles/s at
    10^9; encounters ~1e2/s; both >= 1e4x under one core) and bandwidth (a full sweep
    is 0.27 s => per-frame sweeps impossible, but steady touches ~1e2/s bodies) are far
    under. With population programs (crates/shipmem) + observation-bounded identity the
    storage floor is ~16 MB + player-observation growth ~1e5..1e6 bits/game-second.

P4. H_live boundedness: created mainly by the player (thrust, contacts, resolved
    observations), not by belt self-evolution (P2). If identity storage is charged to
    consumers (light cones, replays) rather than to bodies, H_live growth <= ~1e6
    bits/s in active play (~0.45 GB per 10^4 s session) and is the only monotone term.

## Kill criteria for my own claims

- If measured encounter rates exceed ~1e-1 per body per orbit at belt densities, P1 is
  wrong and the encounter term enters the ledger as compute, not storage.
- If deflections at ship/Ceres masses cross period ticks for a non-negligible fraction
  of encounters, P2 dies: belt bodies recompile at the encounter rate and H_live grows
  as N x rate x scar-bits; the belt is not an attractor.
